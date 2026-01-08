"""
Test cases for DynamoDB client module.
Tests both mock mode and mocked boto3 interactions.
"""
import pytest
from unittest.mock import patch, MagicMock
from decimal import Decimal
from app.dynamodb_client import DynamoDBClient


class TestDynamoDBClientInitialization:
    """Test suite for DynamoDBClient initialization"""

    def test_client_initialization_mock_mode(self):
        """Test DynamoDBClient initializes in mock mode"""
        client = DynamoDBClient(
            table_name="ShoeInventory",
            region="us-east-1",
            mock_mode=True
        )
        assert client.table_name == "ShoeInventory"
        assert client.region == "us-east-1"
        assert client.mock_mode is True
        assert client._table is None

    def test_client_initialization_with_boto3(self):
        """Test DynamoDBClient initializes with boto3 in non-mock mode"""
        with patch('app.dynamodb_client.boto3.resource') as mock_boto:
            client = DynamoDBClient(
                table_name="ShoeInventory",
                region="us-east-1",
                mock_mode=False
            )
            assert client.mock_mode is False
            mock_boto.assert_called_once_with("dynamodb", region_name="us-east-1")

    def test_client_uses_default_region(self):
        """Test DynamoDBClient uses default region if not provided"""
        client = DynamoDBClient(table_name="ShoeInventory", mock_mode=True)
        assert client.region == "us-east-1"


class TestMockMode:
    """Test suite for mock mode operations"""

    @pytest.fixture
    def mock_client(self):
        """Create DynamoDBClient in mock mode"""
        return DynamoDBClient(
            table_name="ShoeInventory",
            region="us-east-1",
            mock_mode=True
        )

    def test_get_all_products_mock(self, mock_client):
        """Test get_all_products returns mock data"""
        products = mock_client.get_all_products()

        assert isinstance(products, list)
        assert len(products) > 0

    def test_mock_products_have_required_fields(self, mock_client):
        """Test mock products have all required fields"""
        products = mock_client.get_all_products()

        required_fields = ["shoe_id", "name", "brand", "type", "color", "sizes", "price"]
        for product in products:
            for field in required_fields:
                assert field in product, f"Missing field: {field}"

    def test_filter_by_type_mock(self, mock_client):
        """Test filtering by type in mock mode"""
        products = mock_client.get_products_by_filters(type="running")

        assert len(products) > 0
        for product in products:
            assert product["type"] == "running"

    def test_filter_by_color_mock(self, mock_client):
        """Test filtering by color in mock mode"""
        products = mock_client.get_products_by_filters(color="red")

        assert len(products) > 0
        for product in products:
            assert product["color"] == "red"

    def test_filter_by_size_mock(self, mock_client):
        """Test filtering by size in mock mode"""
        products = mock_client.get_products_by_filters(size=10.0)

        for product in products:
            assert 10.0 in product["sizes"]

    def test_filter_by_price_range_mock(self, mock_client):
        """Test filtering by price range in mock mode"""
        products = mock_client.get_products_by_filters(price_min=50.0, price_max=100.0)

        for product in products:
            assert 50.0 <= product["price"] <= 100.0

    def test_filter_by_multiple_criteria_mock(self, mock_client):
        """Test filtering by multiple criteria in mock mode"""
        products = mock_client.get_products_by_filters(
            type="running",
            price_max=100.0
        )

        for product in products:
            assert product["type"] == "running"
            assert product["price"] <= 100.0

    def test_get_product_by_id_mock(self, mock_client):
        """Test getting a product by ID in mock mode"""
        # First get all products to get a valid ID
        all_products = mock_client.get_all_products()
        shoe_id = all_products[0]["shoe_id"]

        product = mock_client.get_product_by_id(shoe_id)

        assert product is not None
        assert product["shoe_id"] == shoe_id

    def test_get_product_by_id_not_found_mock(self, mock_client):
        """Test getting a non-existent product returns None"""
        product = mock_client.get_product_by_id("nonexistent-id")

        assert product is None

    def test_get_featured_products_mock(self, mock_client):
        """Test getting featured products in mock mode"""
        products = mock_client.get_featured_products()

        assert len(products) > 0
        for product in products:
            assert product["featured"] is True

    def test_get_categories_mock(self, mock_client):
        """Test getting categories in mock mode"""
        categories = mock_client.get_categories()

        assert "types" in categories
        assert "colors" in categories
        assert len(categories["types"]) > 0
        assert len(categories["colors"]) > 0


class TestRealModeWithMockedBoto:
    """Test suite for real mode with mocked boto3"""

    @pytest.fixture
    def client_with_mocked_boto(self):
        """Create DynamoDBClient with mocked boto3"""
        with patch('app.dynamodb_client.boto3.resource') as mock_boto:
            mock_table = MagicMock()
            mock_boto.return_value.Table.return_value = mock_table
            client = DynamoDBClient(
                table_name="ShoeInventory",
                region="us-east-1",
                mock_mode=False
            )
            yield client, mock_table

    def test_get_all_products_real(self, client_with_mocked_boto):
        """Test get_all_products calls DynamoDB scan"""
        client, mock_table = client_with_mocked_boto

        mock_items = [
            {"shoe_id": "1", "name": "Nike Air", "type": "running", "price": Decimal("99.99")},
            {"shoe_id": "2", "name": "Adidas Ultra", "type": "running", "price": Decimal("120.00")}
        ]
        mock_table.scan.return_value = {"Items": mock_items}

        products = client.get_all_products()

        mock_table.scan.assert_called()
        assert len(products) == 2
        # Verify Decimal was converted to float
        assert isinstance(products[0]["price"], float)

    def test_get_all_products_pagination(self, client_with_mocked_boto):
        """Test get_all_products handles pagination"""
        client, mock_table = client_with_mocked_boto

        # Simulate pagination
        mock_table.scan.side_effect = [
            {
                "Items": [{"shoe_id": "1", "name": "Shoe 1", "price": Decimal("50")}],
                "LastEvaluatedKey": {"shoe_id": "1"}
            },
            {
                "Items": [{"shoe_id": "2", "name": "Shoe 2", "price": Decimal("60")}]
            }
        ]

        products = client.get_all_products()

        assert mock_table.scan.call_count == 2
        assert len(products) == 2

    def test_get_product_by_id_real(self, client_with_mocked_boto):
        """Test get_product_by_id calls DynamoDB get_item"""
        client, mock_table = client_with_mocked_boto

        mock_item = {
            "shoe_id": "test-123",
            "name": "Nike Air Max",
            "brand": "Nike",
            "price": Decimal("99.99")
        }
        mock_table.get_item.return_value = {"Item": mock_item}

        product = client.get_product_by_id("test-123")

        mock_table.get_item.assert_called_with(Key={"shoe_id": "test-123"})
        assert product is not None
        assert product["shoe_id"] == "test-123"

    def test_get_product_by_id_not_found_real(self, client_with_mocked_boto):
        """Test get_product_by_id returns None for missing item"""
        client, mock_table = client_with_mocked_boto

        mock_table.get_item.return_value = {}

        product = client.get_product_by_id("nonexistent-id")

        assert product is None

    def test_get_products_by_filters_real(self, client_with_mocked_boto):
        """Test get_products_by_filters applies filter expressions"""
        client, mock_table = client_with_mocked_boto

        mock_items = [
            {"shoe_id": "1", "name": "Nike Air", "type": "running", "color": "red", "price": Decimal("85.00")}
        ]
        mock_table.scan.return_value = {"Items": mock_items}

        products = client.get_products_by_filters(type="running", color="red")

        mock_table.scan.assert_called()
        # Verify filter was applied
        call_kwargs = mock_table.scan.call_args[1]
        assert "FilterExpression" in call_kwargs

    def test_get_featured_products_real(self, client_with_mocked_boto):
        """Test get_featured_products filters by featured=True"""
        client, mock_table = client_with_mocked_boto

        mock_items = [
            {"shoe_id": "1", "name": "Featured Shoe", "featured": True, "price": Decimal("99.99")}
        ]
        mock_table.scan.return_value = {"Items": mock_items}

        products = client.get_featured_products()

        mock_table.scan.assert_called()
        call_kwargs = mock_table.scan.call_args[1]
        assert "FilterExpression" in call_kwargs

    def test_get_categories_real(self, client_with_mocked_boto):
        """Test get_categories extracts unique types and colors"""
        client, mock_table = client_with_mocked_boto

        mock_items = [
            {"shoe_id": "1", "type": "running", "color": "red"},
            {"shoe_id": "2", "type": "casual", "color": "blue"},
            {"shoe_id": "3", "type": "running", "color": "black"},
            {"shoe_id": "4", "type": "formal", "color": "brown"}
        ]
        mock_table.scan.return_value = {"Items": mock_items}

        categories = client.get_categories()

        assert "types" in categories
        assert "colors" in categories
        assert len(categories["types"]) == 3  # running, casual, formal
        assert len(categories["colors"]) == 4  # red, blue, black, brown
        assert "running" in categories["types"]


class TestDecimalConversion:
    """Test suite for Decimal to float conversion"""

    @pytest.fixture
    def client_with_mocked_boto(self):
        """Create DynamoDBClient with mocked boto3"""
        with patch('app.dynamodb_client.boto3.resource') as mock_boto:
            mock_table = MagicMock()
            mock_boto.return_value.Table.return_value = mock_table
            client = DynamoDBClient(
                table_name="ShoeInventory",
                region="us-east-1",
                mock_mode=False
            )
            yield client, mock_table

    def test_decimal_conversion(self, client_with_mocked_boto):
        """Test that Decimal values are converted to float"""
        client, mock_table = client_with_mocked_boto

        mock_items = [
            {
                "shoe_id": "1",
                "name": "Test Shoe",
                "price": Decimal("99.99"),
                "rating": Decimal("4.5")
            }
        ]
        mock_table.scan.return_value = {"Items": mock_items}

        products = client.get_all_products()

        assert isinstance(products[0]["price"], float)
        assert products[0]["price"] == 99.99
        assert isinstance(products[0]["rating"], float)
        assert products[0]["rating"] == 4.5


class TestErrorHandling:
    """Test suite for error handling"""

    @pytest.fixture
    def client_with_mocked_boto(self):
        """Create DynamoDBClient with mocked boto3"""
        with patch('app.dynamodb_client.boto3.resource') as mock_boto:
            mock_table = MagicMock()
            mock_boto.return_value.Table.return_value = mock_table
            client = DynamoDBClient(
                table_name="ShoeInventory",
                region="us-east-1",
                mock_mode=False
            )
            yield client, mock_table

    def test_get_all_products_handles_error(self, client_with_mocked_boto):
        """Test get_all_products raises exception on error"""
        client, mock_table = client_with_mocked_boto

        mock_table.scan.side_effect = Exception("DynamoDB error")

        with pytest.raises(Exception, match="Error retrieving products"):
            client.get_all_products()

    def test_get_product_by_id_handles_error(self, client_with_mocked_boto):
        """Test get_product_by_id raises exception on error"""
        client, mock_table = client_with_mocked_boto

        mock_table.get_item.side_effect = Exception("DynamoDB error")

        with pytest.raises(Exception, match="Error retrieving product"):
            client.get_product_by_id("test-id")
