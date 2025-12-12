"""
Bedrock client for invoking AWS Bedrock agents.
Handles natural language queries and returns agent responses with product results.
"""
import boto3
import json
from typing import Optional, Dict, List, Any
from botocore.exceptions import ClientError


class BedrockClient:
    """Client for interacting with AWS Bedrock Agent"""

    def __init__(
        self,
        agent_id: str,
        agent_alias_id: str,
        region: str = "us-east-1",
        mock_mode: bool = False,
    ):
        """
        Initialize Bedrock client.

        Args:
            agent_id: The Bedrock agent ID
            agent_alias_id: The agent alias ID
            region: AWS region (defaults to us-east-1)
            mock_mode: If True, returns mock data instead of calling AWS
        """
        self.agent_id = agent_id
        self.agent_alias_id = agent_alias_id
        self.region = region
        self.mock_mode = mock_mode

        # Initialize boto3 client only if not in mock mode
        if not self.mock_mode:
            self._client = boto3.client(
                "bedrock-agent-runtime",
                region_name=self.region,
            )
        else:
            self._client = None

    def invoke_agent(
        self, query: str, session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Invoke the Bedrock agent with a natural language query.

        Args:
            query: Natural language search query
            session_id: Optional session ID for conversation continuity

        Returns:
            Dictionary containing:
                - agent_response: Natural language response from agent
                - products: List of matching products
                - session_id: Session ID for future queries

        Raises:
            ValueError: If query is empty or None
            Exception: If Bedrock API call fails
        """
        # Validate query
        if not query or query.strip() == "":
            raise ValueError("Query cannot be empty")

        # Handle mock mode
        if self.mock_mode:
            return self._mock_invoke_agent(query)

        # Prepare invocation parameters
        invoke_params = {
            "agentId": self.agent_id,
            "agentAliasId": self.agent_alias_id,
            "inputText": query,
        }

        # Add session ID if provided
        if session_id:
            invoke_params["sessionId"] = session_id

        try:
            # Invoke the agent
            response = self._client.invoke_agent(**invoke_params)

            # Parse the response
            result = self._parse_response(response)

            # Add session ID to result if present
            if "sessionId" in response:
                result["session_id"] = response["sessionId"]

            return result

        except ClientError as e:
            raise Exception(f"Bedrock API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error invoking agent: {str(e)}")

    def _parse_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse the Bedrock agent response.

        Args:
            response: Raw response from Bedrock API

        Returns:
            Parsed response with agent_response and products

        Raises:
            Exception: If response parsing fails
        """
        agent_response = ""
        products = []

        try:
            # Process completion stream
            if "completion" in response:
                for event in response["completion"]:
                    if "chunk" in event:
                        chunk_data = event["chunk"]["bytes"]

                        # Decode bytes to string
                        if isinstance(chunk_data, bytes):
                            chunk_str = chunk_data.decode("utf-8")
                        else:
                            chunk_str = str(chunk_data)

                        # Parse JSON from chunk
                        try:
                            chunk_json = json.loads(chunk_str)

                            # Extract response text
                            if "response" in chunk_json:
                                agent_response += chunk_json["response"]

                            # Extract products
                            if "products" in chunk_json:
                                products = chunk_json["products"]

                        except json.JSONDecodeError as e:
                            raise Exception(f"Failed to parse chunk JSON: {str(e)}")

            return {
                "agent_response": agent_response,
                "products": products,
            }

        except Exception as e:
            raise Exception(f"Error parsing response: {str(e)}")

    def _mock_invoke_agent(self, query: str) -> Dict[str, Any]:
        """
        Generate mock response for development.

        Args:
            query: Natural language search query

        Returns:
            Mock response with sample data
        """
        # Generate a simple mock response based on query keywords
        query_lower = query.lower()

        # Mock products
        mock_products = [
            {
                "shoe_id": "mock-001",
                "name": "Mock Running Shoe",
                "brand": "Nike",
                "type": "running",
                "color": "red",
                "sizes": [9.0, 10.0, 11.0],
                "price": 89.99,
                "image_url": "https://example.com/shoe1.jpg",
                "description": "Mock running shoe for testing",
                "featured": False,
                "rating": 4.5,
                "stock": True,
            },
            {
                "shoe_id": "mock-002",
                "name": "Mock Casual Sneaker",
                "brand": "Adidas",
                "type": "casual",
                "color": "blue",
                "sizes": [8.0, 9.0, 10.0],
                "price": 75.50,
                "image_url": "https://example.com/shoe2.jpg",
                "description": "Mock casual sneaker for testing",
                "featured": True,
                "rating": 4.3,
                "stock": True,
            },
        ]

        # Filter mock products based on query keywords
        filtered_products = []
        for product in mock_products:
            if any(keyword in query_lower for keyword in [product["type"], product["color"], product["brand"].lower()]):
                filtered_products.append(product)

        # If no specific keywords matched, return empty list
        # (simulating no results for nonsense queries)

        # Generate response text
        if filtered_products:
            agent_response = f"I found {len(filtered_products)} shoes matching your query: '{query}'. Here are the results:"
        else:
            agent_response = f"I couldn't find any shoes matching your query: '{query}'. Please try a different search."

        return {
            "agent_response": agent_response,
            "products": filtered_products,
            "session_id": "mock-session-123",
        }