"""
Bedrock Agent Client - Invokes AWS Bedrock Agent for natural language search.

TODO (Day 2, Block 4 of Learning Plan):
- This is currently a placeholder with mock responses
- You will implement real Bedrock Agent invocation after creating the agent in AWS console
- Key Bedrock Agent Runtime API method: invoke_agent()
- Required params: agentId, agentAliasId, sessionId, inputText

Interview talking point:
"The Bedrock Agent parses natural language queries and invokes my Lambda action group
to search the product database. I iterated on the agent instructions to handle
ambiguous queries like 'comfortable shoes' or 'something for a wedding'."
"""

import os
import uuid
import json
import boto3
from typing import Optional

BEDROCK_REGION = os.getenv("AWS_REGION", "us-east-1")


class BedrockClient:
    """Client for invoking AWS Bedrock Agent."""

    def __init__(
        self,
        agent_id: str,
        agent_alias_id: str,
        region: Optional[str] = None,
        mock_mode: bool = False,
    ):
        self.agent_id = agent_id
        self.agent_alias_id = agent_alias_id
        self.region = region or BEDROCK_REGION
        self.mock_mode = mock_mode

        if not self.mock_mode:
            # TODO: This client will be used after you create your Bedrock Agent
            # in AWS console (Day 2, Block 1-2 of Learning Plan)
            self._client = boto3.client(
                "bedrock-agent-runtime",
                region_name=self.region
            )
        else:
            self._client = None

    def invoke_agent(self, query: str, session_id: Optional[str] = None) -> dict:
        """
        Invoke the Bedrock Agent with a natural language query.

        Args:
            query: Natural language search query from user
            session_id: Optional session ID for conversation continuity

        Returns:
            dict with keys:
                - agent_response: The agent's natural language response
                - products: List of matching products
                - session_id: Session ID for follow-up queries
        """
        if not query or query.strip() == "":
            raise ValueError("Query cannot be empty")

        current_session_id = session_id or str(uuid.uuid4())

        if self.mock_mode:
            # Mock response for local development without AWS
            return self._get_mock_response(query, current_session_id)

        try:
            response = self._client.invoke_agent(
                agentId=self.agent_id,
                agentAliasId=self.agent_alias_id,
                sessionId=current_session_id,
                inputText=query,
                enableTrace=True  # Enable trace to get Lambda response
            )
            completion = ""
            products = []

            for event in response.get("completion"):
                # Capture agent's text response
                if 'chunk' in event:
                    chunk = event["chunk"]
                    completion += chunk["bytes"].decode()

                # Extract products from trace (Lambda response)
                if 'trace' in event:
                    trace_data = event['trace']
                    trace = trace_data.get('trace', {})
                    orchestration = trace.get('orchestrationTrace', {})

                    # Check for function invocation output
                    if 'observation' in orchestration:
                        observation = orchestration['observation']
                        if 'actionGroupInvocationOutput' in observation:
                            output = observation['actionGroupInvocationOutput']
                            if 'text' in output:
                                try:
                                    # Parse the JSON product data from Lambda
                                    products = json.loads(output['text'])
                                    print(f"Extracted {len(products)} products from Lambda")
                                except json.JSONDecodeError:
                                    pass

            return {
                "agent_response": completion,
                "products": products,
                "session_id": current_session_id
            }
        except Exception as e:
            print(f"Error invoking agent: {e}")
            return self._get_mock_response(query, current_session_id)


    def _get_mock_response(self, query: str, session_id: str) -> dict:
        """Generate mock response for development/testing."""
        # Simple keyword matching for demo purposes
        query_lower = query.lower()

        mock_products = []
        response_text = ""

        if "running" in query_lower:
            response_text = f"I found some great running shoes for you based on '{query}'."
            mock_products = [
                {"shoe_id": "mock-run-1", "name": "Air Speed Runner", "brand": "Nike", "type": "running", "color": "red", "price": 89.99, "sizes": [8, 9, 10, 11], "image_url": "https://placehold.co/300x300?text=Nike+Runner", "description": "Fast and comfortable running shoes", "rating": 4.5},
                {"shoe_id": "mock-run-2", "name": "Ultra Boost", "brand": "Adidas", "type": "running", "color": "black", "price": 129.99, "sizes": [9, 10, 11, 12], "image_url": "https://placehold.co/300x300?text=Adidas+Boost", "description": "Premium cushioned running shoes", "rating": 4.7},
            ]
        elif "formal" in query_lower or "wedding" in query_lower or "dress" in query_lower:
            response_text = f"Here are some formal options based on '{query}'."
            mock_products = [
                {"shoe_id": "mock-form-1", "name": "Oxford Classic", "brand": "Clarks", "type": "formal", "color": "black", "price": 149.99, "sizes": [9, 10, 11], "image_url": "https://placehold.co/300x300?text=Oxford", "description": "Classic formal oxford shoes", "rating": 4.6},
            ]
        else:
            response_text = f"Here's what I found for '{query}'. Let me know if you'd like to narrow down by type, color, or price."
            mock_products = [
                {"shoe_id": "mock-1", "name": "Casual Comfort", "brand": "Nike", "type": "casual", "color": "white", "price": 79.99, "sizes": [8, 9, 10, 11, 12], "image_url": "https://placehold.co/300x300?text=Casual", "description": "Everyday casual shoes", "rating": 4.3},
                {"shoe_id": "mock-2", "name": "Street Style", "brand": "Puma", "type": "sneakers", "color": "gray", "price": 99.99, "sizes": [9, 10, 11], "image_url": "https://placehold.co/300x300?text=Puma", "description": "Trendy street sneakers", "rating": 4.4},
            ]

        return {
            "agent_response": response_text,
            "products": mock_products,
            "session_id": session_id,
        }


if __name__ == "__main__":
    # Quick test in mock mode
    client = BedrockClient(
        agent_id="test-agent-id",
        agent_alias_id="test-alias-id",
        mock_mode=True,
    )
    result = client.invoke_agent("Show me red running shoes under $100")
    print(f"Agent response: {result['agent_response']}")
    print(f"Products: {result['products']}")
