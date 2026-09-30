"""Bedrock search integration and a deterministic local catalog search."""
import codecs
import json
import os
import re
from uuid import uuid4

import boto3

from app.dynamodb_client import DynamoDBClient


class BedrockClient:
    def __init__(self, agent_id, agent_alias_id, region=None, mock_mode=False):
        self.agent_id = agent_id
        self.agent_alias_id = agent_alias_id
        self.region = region or os.getenv("AWS_REGION", "us-east-1")
        self.mock_mode = mock_mode
        self._client = None if mock_mode else boto3.client(
            "bedrock-agent-runtime", region_name=self.region
        )

    def invoke_agent(self, query, session_id=None):
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
        session_id = session_id or str(uuid4())
        if self.mock_mode:
            result = self._mock_invoke_agent(query)
        else:
            response = self._client.invoke_agent(
                agentId=self.agent_id,
                agentAliasId=self.agent_alias_id,
                sessionId=session_id,
                inputText=query.strip(),
                enableTrace=True,
            )
            result = self._parse_response(response)
            session_id = response.get("sessionId", session_id)
        return {**result, "session_id": session_id}

    def _parse_response(self, response):
        # Bedrock chunks may split JSON (or UTF-8 characters) at any byte.
        decoder = codecs.getincrementaldecoder("utf-8")()
        parts = []
        traced_products = []
        for event in response.get("completion", []):
            if "chunk" in event:
                value = event["chunk"]["bytes"]
                parts.append(decoder.decode(value) if isinstance(value, bytes) else str(value))
            elif "trace" in event:
                trace = event["trace"].get("trace", {})
                observation = trace.get("orchestrationTrace", {}).get("observation", {})
                output = observation.get("actionGroupInvocationOutput", {}).get("text")
                if output:
                    try:
                        payload = json.loads(output)
                    except json.JSONDecodeError:
                        continue
                    candidates = payload if isinstance(payload, list) else payload.get("products", []) if isinstance(payload, dict) else []
                    if isinstance(candidates, list):
                        traced_products = candidates
            elif any(key.endswith("Exception") for key in event):
                raise RuntimeError("Bedrock could not complete the search")
        text = "".join(parts) + decoder.decode(b"", final=True)
        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
        if not text.startswith(("{", "[")):
            return {"agent_response": text, "products": traced_products}
        # Also accept legacy streams containing consecutive JSON objects.
        json_decoder = json.JSONDecoder()
        message, products = "", traced_products
        structured_products = False
        remaining = text
        while remaining:
            payload, end = json_decoder.raw_decode(remaining)
            if not isinstance(payload, dict):
                raise ValueError("Agent response must be a JSON object")
            message += payload.get("agent_response", payload.get("response", ""))
            if "products" in payload:
                if not isinstance(payload["products"], list):
                    raise ValueError("Agent products must be a list")
                if not structured_products:
                    products = []
                    structured_products = True
                products.extend(payload["products"])
            remaining = remaining[end:].lstrip()
        return {"agent_response": message, "products": products}

    def _mock_invoke_agent(self, query):
        products = DynamoDBClient("ShoeInventory", mock_mode=True).get_all_products()
        text = query.lower()
        filters = {}
        for field in ("type", "color", "brand"):
            values = {product[field].lower() for product in products}
            # Unsupported colors should produce zero results, not broad matches.
            if field == "color":
                values |= {"purple", "pink", "green", "yellow", "white", "brown", "gray"}
            elif field == "type":
                values |= {"athletic", "boots", "sandals"}
            matches = [value for value in values if re.search(r"\b" + re.escape(value) + r"\b", text)]
            if matches:
                filters[field] = matches
        if "type" not in filters and re.search(r"\b(sneakers?|trainers?)\b", text):
            filters["type"] = ["running", "casual", "athletic", "sneakers"]
        size = re.search(r"\bsize\s*(\d+(?:\.\d+)?)\b", text)
        upper = re.search(r"\b(under|below|up to|at most)\s*\$?\s*(\d+(?:\.\d+)?)", text)
        lower = re.search(r"\b(over|above|at least)\s*\$?\s*(\d+(?:\.\d+)?)", text)
        between = re.search(r"\bbetween\s*\$?\s*(\d+(?:\.\d+)?)\s*(?:and|-)\s*\$?\s*(\d+(?:\.\d+)?)", text)
        for field, values in filters.items():
            products = [product for product in products if product[field].lower() in values]
        if size:
            products = [product for product in products if float(size[1]) in product["sizes"]]
        if upper:
            limit = float(upper[2])
            products = [p for p in products if p["price"] < limit or (upper[1] in ("up to", "at most") and p["price"] == limit)]
        if lower:
            limit = float(lower[2])
            products = [p for p in products if p["price"] > limit or (lower[1] == "at least" and p["price"] == limit)]
        if between:
            products = [p for p in products if float(between[1]) <= p["price"] <= float(between[2])]
        if not (filters or size or upper or lower or between or re.search(r"\b(shoes?|footwear|all|everything)\b", text)):
            products = []
        count = len(products)
        message = f"Found {count} {'pair' if count == 1 else 'pairs'} matching your search." if products else "No matches this time. Try another color, size, or budget."
        return {"agent_response": message, "products": products}
