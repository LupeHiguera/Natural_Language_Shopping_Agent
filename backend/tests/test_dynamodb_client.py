"""
Test cases for DynamoDB client module.
Following TDD - these tests should fail initially.
Uses moto for DynamoDB mocking.
"""
import pytest
from unittest.mock import Mock, patch
from decimal import Decimal
from app.dynamodb_client import DynamoDBClient


class TestDynamoDBClientInitialization:
    """Test suite for DynamoDBClient initialization"""

    def test_client_initialization(self):
        """Test DynamoDBClient initializes with required parameters"""
        client = DynamoDBClient(
            table_name="ShoeInventory",
            region="us-east-1"
        )
        assert client.table_name == "ShoeInventory"
        assert client.region == "us-east-1"

    def test_client_initialization_without_region(self):
        """Test DynamoDBClient uses default region if not provided"""
        client = DynamoDBClient(table_name="ShoeInventory")
        assert client.region is not None


class TestGetAllProducts:
    """Test suite for retrieving all products"""

    @pytest.fixture
    def mock_dynamodb_client(self):
        """Create DynamoDBClient with mocked boto3"""
        with patch('app.dynamodb_client.boto3.resource') as mock_boto:
            client = DynamoDBClient(table_name="ShoeInventory", region="us-east-1")
            client._table = mock_boto.return_value.Table.return_value
            return client

    def test_get_all_products(self, mock_dynamodb_client):
        """Test retrieving all products without filters"""
        mock_items = [
            {"shoe_id": "1", "name": "Nike Air", "type": "running", "price": Decimal("99.99")},
            {"shoe_id": "2", "name": "Adidas Ultra", "type": "running", "price": Decimal("120.00")}
        ]
        mock_dynamodb_client._table.scan.return_value = {"Items": mock_items}

        products = mock_dynamodb_client.get_all_products()

        assert len(products) == 2
        assert products[0]["shoe_id"] == "1"
        assert products[1]["name"] == "Adidas Ultra"

    def test_get_all_products_empty_table(self, mock_dynamodb_client):
        """Test retrieving products from empty table"""
        mock_dynamodb_client._table.scan.return_value = {"Items": []}

        products = mock_dynamodb_client.get_all_products()

        assert products == []


class TestGetProductsByFilters:
    """Test suite for filtered product queries"""

    @pytest.fixture
    def mock_dynamodb_client(self):
        """Create DynamoDBClient with mocked boto3"""
        with patch('app.dynamodb_client.boto3.resource') as mock_boto:
            client = DynamoDBClient(table_name="ShoeInventory", region="us-east-1")
            client._table = mock_boto.return_value.Table.return_value
            return client

    def test_filter_by_type(self, mock_dynamodb_client):
        """Test filtering products by type"""
        mock_items = [
            {"shoe_id": "1", "name": "Nike Air", "type": "running", "price": Decimal("99.99")},
            {"shoe_id": "2", "name": "Nike Zoom", "type": "running", "price": Decimal("110.00")}
        ]
        mock_dynamodb_client._table.scan.return_value = {"Items": mock_items}

        products = mock_dynamodb_client.get_products_by_filters(type="running")

        assert len(products) == 2
        for product in products:
            assert product["type"] == "running"

    def test_filter_by_color(self, mock_dynamodb_client):
        """Test filtering products by color"""
        mock_items = [
            {"shoe_id": "1", "name": "Red Nike", "color": "red", "price": Decimal("99.99")}
        ]
        mock_dynamodb_client._table.scan.return_value = {"Items": mock_items}

        products = mock_dynamodb_client.get_products_by_filters(color="red")

        assert len(products) == 1
        assert products[0]["color"] == "red"

    def test_filter_by_size(self, mock_dynamodb_client):
        """Test filtering products by available size"""
        mock_items = [
            {"shoe_id": "1", "name": "Nike Air", "sizes": [9, 10, 11], "price": Decimal("99.99")},
            {"shoe_id": "2", "name": "Adidas Ultra", "sizes": [10, 11, 12], "price": Decimal("120.00")}
        ]
        mock_dynamodb_client._table.scan.return_value = {"Items": mock_items}

        products = mock_dynamodb_client.get_products_by_filters(size=10)

        assert len(products) == 2
        for product in products:
            assert 10 in product["sizes"]

    def test_filter_by_price_range(self, mock_dynamodb_client):
        """Test filtering products by price range"""
        mock_items = [
            {"shoe_id": "1", "name": "Nike Air", "price": Decimal("75.00")},
            {"shoe_id": "2", "name": "Adidas Ultra", "price": Decimal("85.00")}
        ]
        mock_dynamodb_client._table.scan.return_value = {"Items": mock_items}

        products = mock_dynamodb_client.get_products_by_filters(
            price_min=50.0,
            price_max=100.0
        )

        assert len(products) == 2
        for product in products:
            assert 50.0 <= float(product["price"]) <= 100.0

    def test_filter_by_multiple_criteria(self, mock_dynamodb_client):
        """Test filtering products by multiple criteria"""
        mock_items = [
            {
                "shoe_id": "1",
                "name": "Red Nike Air",
                "type": "running",
                "color": "red",
                "sizes": [9, 10, 11],
                "price": Decimal("85.00")
            }
        ]
        mock_dynamodb_client._table.scan.return_value = {"Items": mock_items}

        products = mock_dynamodb_client.get_products_by_filters(
            type="running",
            color="red",
            size=10,
            price_max=100.0
        )

        assert len(products) == 1
        product = products[0]
        assert product["type"] == "running"
        assert product["color"] == "red"
        assert 10 in product["sizes"]
        assert float(product["price"]) <= 100.0

    def test_filter_returns_empty_when_no_matches(self, mock_dynamodb_client):
        """Test filtering returns empty list when no products match"""
        mock_dynamodb_client._table.scan.return_value = {"Items": []}

        products = mock_dynamodb_client.get_products_by_filters(
            type="running",
            color="purple",
            price_max=1.0
        )

        assert products == []


class TestGetProductById:
    """Test suite for retrieving single product by ID"""

    @pytest.fixture
    def mock_dynamodb_client(self):
        """Create DynamoDBClient with mocked boto3"""
        with patch('app.dynamodb_client.boto3.resource') as mock_boto:
            client = DynamoDBClient(table_name="ShoeInventory", region="us-east-1")
            client._table = mock_boto.return_value.Table.return_value
            return client

    def test_get_product_by_id_success(self, mock_dynamodb_client):
        """Test retrieving a product by valid ID"""
        mock_item = {
            "shoe_id": "test-123",
            "name": "Nike Air Max",
            "brand": "Nike",
            "price": Decimal("99.99")
        }
        mock_dynamodb_client._table.get_item.return_value = {"Item": mock_item}

        product = mock_dynamodb_client.get_product_by_id("test-123")

        assert product is not None
        assert product["shoe_id"] == "test-123"
        assert product["name"] == "Nike Air Max"

    def test_get_product_by_id_not_found(self, mock_dynamodb_client):
        """Test retrieving a product with invalid ID returns None"""
        mock_dynamodb_client._table.get_item.return_value = {}

        product = mock_dynamodb_client.get_product_by_id("nonexistent-id")

        assert product is None


class TestGetFeaturedProducts:
    """Test suite for retrieving featured products"""

    @pytest.fixture
    def mock_dynamodb_client(self):
        """Create DynamoDBClient with mocked boto3"""
        with patch('app.dynamodb_client.boto3.resource') as mock_boto:
            client = DynamoDBClient(table_name="ShoeInventory", region="us-east-1")
            client._table = mock_boto.return_value.Table.return_value
            return client

    def test_get_featured_products(self, mock_dynamodb_client):
        """Test retrieving only featured products"""
        mock_items = [
            {"shoe_id": "1", "name": "Featured Nike", "featured": True, "price": Decimal("99.99")},
            {"shoe_id": "2", "name": "Featured Adidas", "featured": True, "price": Decimal("120.00")}
        ]
        mock_dynamodb_client._table.scan.return_value = {"Items": mock_items}

        products = mock_dynamodb_client.get_featured_products()

        assert len(products) == 2
        for product in products:
            assert product["featured"] is True

    def test_get_featured_products_empty(self, mock_dynamodb_client):
        """Test getting featured products when none exist"""
        mock_dynamodb_client._table.scan.return_value = {"Items": []}

        products = mock_dynamodb_client.get_featured_products()

        assert products == []


class TestGetCategories:
    """Test suite for retrieving available categories"""

    @pytest.fixture
    def mock_dynamodb_client(self):
        """Create DynamoDBClient with mocked boto3"""
        with patch('app.dynamodb_client.boto3.resource') as mock_boto:
            client = DynamoDBClient(table_name="ShoeInventory", region="us-east-1")
            client._table = mock_boto.return_value.Table.return_value
            return client

    def test_get_unique_types(self, mock_dynamodb_client):
        """Test getting all unique shoe types"""
        mock_items = [
            {"shoe_id": "1", "type": "running", "color": "red"},
            {"shoe_id": "2", "type": "casual", "color": "blue"},
            {"shoe_id": "3", "type": "running", "color": "black"},
            {"shoe_id": "4", "type": "formal", "color": "brown"}
        ]
        mock_dynamodb_client._table.scan.return_value = {"Items": mock_items}

        categories = mock_dynamodb_client.get_categories()

        assert "types" in categories
        assert len(categories["types"]) == 3
        assert "running" in categories["types"]
        assert "casual" in categories["types"]
        assert "formal" in categories["types"]

    def test_get_unique_colors(self, mock_dynamodb_client):
        """Test getting all unique colors"""
        mock_items = [
            {"shoe_id": "1", "type": "running", "color": "red"},
            {"shoe_id": "2", "type": "casual", "color": "blue"},
            {"shoe_id": "3", "type": "running", "color": "red"},
            {"shoe_id": "4", "type": "formal", "color": "black"}
        ]
        mock_dynamodb_client._table.scan.return_value = {"Items": mock_items}

        categories = mock_dynamodb_client.get_categories()

        assert "colors" in categories
        assert len(categories["colors"]) == 3
        assert "red" in categories["colors"]
        assert "blue" in categories["colors"]
        assert "black" in categories["colors"]


class TestMockMode:
    """Test suite for mock mode (before AWS setup)"""

    def test_client_in_mock_mode(self):
        """Test DynamoDBClient can operate in mock mode for development"""
        client = DynamoDBClient(
            table_name="ShoeInventory",
            region="us-east-1",
            mock_mode=True
        )

        products = client.get_all_products()

        assert isinstance(products, list)
        assert len(products) > 0
        # Mock mode should return properly structured products
        assert "shoe_id" in products[0]
        assert "name" in products[0]
        assert "price" in products[0]

    def test_mock_mode_supports_filters(self):
        """Test mock mode handles filtered queries"""
        client = DynamoDBClient(
            table_name="ShoeInventory",
            region="us-east-1",
            mock_mode=True
        )

        # Should return filtered results even in mock mode
        products = client.get_products_by_filters(type="running", price_max=100.0)

        assert isinstance(products, list)
        for product in products:
            assert product["type"] == "running"
            assert float(product["price"]) <= 100.0


class TestPaginationHandling:
    """Test suite for handling paginated DynamoDB responses"""

    @pytest.fixture
    def mock_dynamodb_client(self):
        """Create DynamoDBClient with mocked boto3"""
        with patch('app.dynamodb_client.boto3.resource') as mock_boto:
            client = DynamoDBClient(table_name="ShoeInventory", region="us-east-1")
            client._table = mock_boto.return_value.Table.return_value
            return client

    def test_handles_paginated_scan(self, mock_dynamodb_client):
        """Test client handles paginated scan results"""
        # Simulate pagination with LastEvaluatedKey
        mock_dynamodb_client._table.scan.side_effect = [
            {
                "Items": [{"shoe_id": "1", "name": "Shoe 1"}],
                "LastEvaluatedKey": {"shoe_id": "1"}
            },
            {
                "Items": [{"shoe_id": "2", "name": "Shoe 2"}]
            }
        ]

        products = mock_dynamodb_client.get_all_products()

        # Should combine results from both pages
        assert len(products) == 2
        assert products[0]["shoe_id"] == "1"
        assert products[1]["shoe_id"] == "2"
