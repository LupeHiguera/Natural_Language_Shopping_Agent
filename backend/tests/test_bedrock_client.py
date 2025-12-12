"""
Test cases for Bedrock client module.
Following TDD - these tests should fail initially.
"""
import pytest
from unittest.mock import Mock, patch
from app.bedrock_client import BedrockClient


class TestBedrockClientInitialization:
    """Test suite for BedrockClient initialization"""

    def test_client_initialization(self):
        """Test BedrockClient initializes with required parameters"""
        client = BedrockClient(
            agent_id="test-agent-id",
            agent_alias_id="test-alias-id",
            region="us-east-1"
        )
        assert client.agent_id == "test-agent-id"
        assert client.agent_alias_id == "test-alias-id"
        assert client.region == "us-east-1"

    def test_client_initialization_without_region(self):
        """Test BedrockClient uses default region if not provided"""
        client = BedrockClient(
            agent_id="test-agent-id",
            agent_alias_id="test-alias-id"
        )
        assert client.region is not None


class TestInvokeAgent:
    """Test suite for agent invocation"""

    @pytest.fixture
    def mock_bedrock_client(self):
        """Create BedrockClient with mocked boto3"""
        with patch('app.bedrock_client.boto3.client') as mock_boto:
            client = BedrockClient(
                agent_id="test-agent-id",
                agent_alias_id="test-alias-id",
                region="us-east-1"
            )
            client._client = mock_boto.return_value
            return client

    def test_invoke_agent_with_simple_query(self, mock_bedrock_client):
        """Test invoking agent with a simple query"""
        # Mock the response from Bedrock
        mock_response = {
            "completion": [
                {"chunk": {"bytes": b'{"response": "Here are some running shoes"}'}},
                {"chunk": {"bytes": b'{"products": [{"shoe_id": "123", "name": "Nike Air"}]}'}}
            ]
        }
        mock_bedrock_client._client.invoke_agent.return_value = mock_response

        result = mock_bedrock_client.invoke_agent("show me running shoes")

        assert "agent_response" in result
        assert "products" in result
        assert isinstance(result["agent_response"], str)
        assert isinstance(result["products"], list)

    def test_invoke_agent_with_empty_query(self, mock_bedrock_client):
        """Test invoking agent with empty query raises ValueError"""
        with pytest.raises(ValueError, match="Query cannot be empty"):
            mock_bedrock_client.invoke_agent("")

    def test_invoke_agent_with_none_query(self, mock_bedrock_client):
        """Test invoking agent with None query raises ValueError"""
        with pytest.raises(ValueError, match="Query cannot be empty"):
            mock_bedrock_client.invoke_agent(None)

    def test_invoke_agent_handles_bedrock_error(self, mock_bedrock_client):
        """Test invoking agent handles Bedrock API errors gracefully"""
        mock_bedrock_client._client.invoke_agent.side_effect = Exception("Bedrock API error")

        with pytest.raises(Exception, match="Bedrock API error"):
            mock_bedrock_client.invoke_agent("test query")

    def test_invoke_agent_with_session_id(self, mock_bedrock_client):
        """Test invoking agent with session ID for conversation continuity"""
        mock_response = {
            "completion": [
                {"chunk": {"bytes": b'{"response": "Based on your previous query..."}'}},
            ],
            "sessionId": "test-session-123"
        }
        mock_bedrock_client._client.invoke_agent.return_value = mock_response

        result = mock_bedrock_client.invoke_agent(
            "what about size 10?",
            session_id="test-session-123"
        )

        assert "agent_response" in result
        mock_bedrock_client._client.invoke_agent.assert_called_with(
            agentId="test-agent-id",
            agentAliasId="test-alias-id",
            sessionId="test-session-123",
            inputText="what about size 10?"
        )

    def test_invoke_agent_returns_session_id(self, mock_bedrock_client):
        """Test that invoke_agent returns session_id for future use"""
        mock_response = {
            "completion": [
                {"chunk": {"bytes": b'{"response": "Here are results"}'}},
            ],
            "sessionId": "new-session-456"
        }
        mock_bedrock_client._client.invoke_agent.return_value = mock_response

        result = mock_bedrock_client.invoke_agent("show me shoes")

        assert "session_id" in result
        assert result["session_id"] == "new-session-456"


class TestResponseParsing:
    """Test suite for parsing Bedrock agent responses"""

    @pytest.fixture
    def mock_bedrock_client(self):
        """Create BedrockClient with mocked boto3"""
        with patch('app.bedrock_client.boto3.client') as mock_boto:
            client = BedrockClient(
                agent_id="test-agent-id",
                agent_alias_id="test-alias-id",
                region="us-east-1"
            )
            client._client = mock_boto.return_value
            return client

    def test_parse_response_with_products(self, mock_bedrock_client):
        """Test parsing response that includes product results"""
        mock_response = {
            "completion": [
                {"chunk": {"bytes": b'{"response": "I found 5 red running shoes"}'}},
                {"chunk": {"bytes": b'{"products": [{"shoe_id": "1", "name": "Nike"}, {"shoe_id": "2", "name": "Adidas"}]}'}}
            ]
        }
        mock_bedrock_client._client.invoke_agent.return_value = mock_response

        result = mock_bedrock_client.invoke_agent("red running shoes")

        assert len(result["products"]) == 2
        assert result["products"][0]["shoe_id"] == "1"
        assert result["products"][1]["name"] == "Adidas"

    def test_parse_response_no_products_found(self, mock_bedrock_client):
        """Test parsing response when no products match"""
        mock_response = {
            "completion": [
                {"chunk": {"bytes": b'{"response": "Sorry, I could not find any matching shoes"}'}},
                {"chunk": {"bytes": b'{"products": []}'}}
            ]
        }
        mock_bedrock_client._client.invoke_agent.return_value = mock_response

        result = mock_bedrock_client.invoke_agent("purple polka dot shoes")

        assert result["products"] == []
        assert "could not find" in result["agent_response"].lower()

    def test_parse_response_with_malformed_json(self, mock_bedrock_client):
        """Test parsing handles malformed JSON gracefully"""
        mock_response = {
            "completion": [
                {"chunk": {"bytes": b'{invalid json}'}},
            ]
        }
        mock_bedrock_client._client.invoke_agent.return_value = mock_response

        # Should handle error gracefully, not crash
        with pytest.raises(Exception):
            mock_bedrock_client.invoke_agent("test query")


class TestMockMode:
    """Test suite for mock mode (before AWS setup)"""

    def test_client_in_mock_mode(self):
        """Test BedrockClient can operate in mock mode for development"""
        client = BedrockClient(
            agent_id="mock",
            agent_alias_id="mock",
            region="us-east-1",
            mock_mode=True
        )

        result = client.invoke_agent("red running shoes under $100")

        assert "agent_response" in result
        assert "products" in result
        assert isinstance(result["products"], list)
        # Mock mode should return some sample products
        assert len(result["products"]) > 0

    def test_mock_mode_various_queries(self):
        """Test mock mode handles various query types"""
        client = BedrockClient(
            agent_id="mock",
            agent_alias_id="mock",
            region="us-east-1",
            mock_mode=True
        )

        queries = [
            "running shoes",
            "formal shoes under $150",
            "size 10 casual shoes",
            "red sneakers"
        ]

        for query in queries:
            result = client.invoke_agent(query)
            assert "agent_response" in result
            assert "products" in result
            assert len(result["agent_response"]) > 0