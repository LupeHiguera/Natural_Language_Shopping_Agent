"""
Test cases for Bedrock client module.
Tests both mock mode and mocked AWS interactions.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from app.bedrock_client import BedrockClient


class TestBedrockClientInitialization:
    """Test suite for BedrockClient initialization"""

    def test_client_initialization_mock_mode(self):
        """Test BedrockClient initializes in mock mode"""
        client = BedrockClient(
            agent_id="test-agent-id",
            agent_alias_id="test-alias-id",
            region="us-east-1",
            mock_mode=True
        )
        assert client.agent_id == "test-agent-id"
        assert client.agent_alias_id == "test-alias-id"
        assert client.region == "us-east-1"
        assert client.mock_mode is True
        assert client._client is None

    def test_client_initialization_with_boto3(self):
        """Test BedrockClient initializes with boto3 in non-mock mode"""
        with patch('app.bedrock_client.boto3.client') as mock_boto:
            client = BedrockClient(
                agent_id="test-agent-id",
                agent_alias_id="test-alias-id",
                region="us-east-1",
                mock_mode=False
            )
            assert client.mock_mode is False
            mock_boto.assert_called_once_with(
                "bedrock-agent-runtime",
                region_name="us-east-1"
            )

    def test_client_uses_default_region(self):
        """Test BedrockClient uses default region if not provided"""
        client = BedrockClient(
            agent_id="test-agent-id",
            agent_alias_id="test-alias-id",
            mock_mode=True
        )
        assert client.region is not None


class TestInvokeAgentValidation:
    """Test suite for agent invocation input validation"""

    @pytest.fixture
    def mock_client(self):
        """Create BedrockClient in mock mode"""
        return BedrockClient(
            agent_id="test-agent-id",
            agent_alias_id="test-alias-id",
            region="us-east-1",
            mock_mode=True
        )

    def test_invoke_agent_with_empty_query(self, mock_client):
        """Test invoking agent with empty query raises ValueError"""
        with pytest.raises(ValueError, match="Query cannot be empty"):
            mock_client.invoke_agent("")

    def test_invoke_agent_with_none_query(self, mock_client):
        """Test invoking agent with None query raises ValueError"""
        with pytest.raises(ValueError, match="Query cannot be empty"):
            mock_client.invoke_agent(None)

    def test_invoke_agent_with_whitespace_query(self, mock_client):
        """Test invoking agent with whitespace-only query raises ValueError"""
        with pytest.raises(ValueError, match="Query cannot be empty"):
            mock_client.invoke_agent("   ")


class TestMockMode:
    """Test suite for mock mode responses"""

    @pytest.fixture
    def mock_client(self):
        """Create BedrockClient in mock mode"""
        return BedrockClient(
            agent_id="mock",
            agent_alias_id="mock",
            region="us-east-1",
            mock_mode=True
        )

    def test_mock_mode_returns_valid_response(self, mock_client):
        """Test mock mode returns properly structured response"""
        result = mock_client.invoke_agent("red running shoes under $100")

        assert "agent_response" in result
        assert "products" in result
        assert "session_id" in result
        assert isinstance(result["agent_response"], str)
        assert isinstance(result["products"], list)
        assert len(result["agent_response"]) > 0

    def test_mock_mode_running_shoes_query(self, mock_client):
        """Test mock mode returns running shoes for running query"""
        result = mock_client.invoke_agent("show me running shoes")

        assert len(result["products"]) > 0
        assert "running" in result["agent_response"].lower()
        # Mock products should include running shoes
        for product in result["products"]:
            assert product.get("type") == "running"

    def test_mock_mode_formal_shoes_query(self, mock_client):
        """Test mock mode returns formal shoes for formal query"""
        result = mock_client.invoke_agent("I need formal shoes for a wedding")

        assert len(result["products"]) > 0
        assert "formal" in result["agent_response"].lower()

    def test_mock_mode_generic_query(self, mock_client):
        """Test mock mode handles generic queries"""
        result = mock_client.invoke_agent("show me some shoes")

        assert len(result["products"]) > 0
        assert len(result["agent_response"]) > 0

    def test_mock_mode_generates_session_id(self, mock_client):
        """Test mock mode generates a session ID"""
        result = mock_client.invoke_agent("show me shoes")

        assert result["session_id"] is not None
        assert len(result["session_id"]) > 0

    def test_mock_mode_uses_provided_session_id(self, mock_client):
        """Test mock mode uses provided session ID"""
        result = mock_client.invoke_agent(
            "show me shoes",
            session_id="test-session-123"
        )

        assert result["session_id"] == "test-session-123"

    def test_mock_products_have_required_fields(self, mock_client):
        """Test mock products have all required fields"""
        result = mock_client.invoke_agent("running shoes")

        required_fields = ["shoe_id", "name", "brand", "type", "color", "price"]
        for product in result["products"]:
            for field in required_fields:
                assert field in product, f"Missing field: {field}"


class TestRealModeWithMockedBoto:
    """Test suite for real mode with mocked boto3 responses"""

    @pytest.fixture
    def client_with_mocked_boto(self):
        """Create BedrockClient with mocked boto3"""
        with patch('app.bedrock_client.boto3.client') as mock_boto:
            client = BedrockClient(
                agent_id="test-agent-id",
                agent_alias_id="test-alias-id",
                region="us-east-1",
                mock_mode=False
            )
            yield client, mock_boto.return_value

    def test_invoke_agent_calls_bedrock(self, client_with_mocked_boto):
        """Test that invoke_agent calls bedrock API correctly"""
        client, mock_boto_client = client_with_mocked_boto

        # Mock the response from Bedrock
        mock_response = {
            "completion": iter([
                {"chunk": {"bytes": b"Here are some shoes for you"}}
            ])
        }
        mock_boto_client.invoke_agent.return_value = mock_response

        result = client.invoke_agent("show me running shoes")

        mock_boto_client.invoke_agent.assert_called_once()
        call_kwargs = mock_boto_client.invoke_agent.call_args[1]
        assert call_kwargs["agentId"] == "test-agent-id"
        assert call_kwargs["agentAliasId"] == "test-alias-id"
        assert call_kwargs["inputText"] == "show me running shoes"
        assert call_kwargs["enableTrace"] is True

    def test_invoke_agent_with_session_id(self, client_with_mocked_boto):
        """Test invoke_agent passes session ID correctly"""
        client, mock_boto_client = client_with_mocked_boto

        mock_response = {
            "completion": iter([
                {"chunk": {"bytes": b"Following up on your search"}}
            ])
        }
        mock_boto_client.invoke_agent.return_value = mock_response

        client.invoke_agent("what about size 10?", session_id="test-session-123")

        call_kwargs = mock_boto_client.invoke_agent.call_args[1]
        assert call_kwargs["sessionId"] == "test-session-123"

    def test_invoke_agent_handles_error_gracefully(self, client_with_mocked_boto):
        """Test invoke_agent falls back to mock on error"""
        client, mock_boto_client = client_with_mocked_boto

        mock_boto_client.invoke_agent.side_effect = Exception("Bedrock API error")

        # Should fallback to mock response, not raise
        result = client.invoke_agent("test query")

        assert "agent_response" in result
        assert "products" in result
