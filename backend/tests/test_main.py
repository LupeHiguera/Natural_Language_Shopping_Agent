"""
Test cases for FastAPI main application endpoints.
Uses mock mode for testing without AWS dependencies.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


class TestHealthEndpoint:
    """Test suite for health check endpoint"""

    def test_health_check(self, client):
        """Test GET /health returns healthy status"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestRootEndpoint:
    """Test suite for root endpoint"""

    def test_root_returns_api_info(self, client):
        """Test GET / returns API information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "endpoints" in data


class TestProductsEndpoints:
    """Test suite for /api/products endpoints"""

    def test_get_all_products(self, client):
        """Test GET /api/products returns all products"""
        response = client.get("/api/products")
        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        assert "count" in data
        assert isinstance(data["products"], list)
        assert len(data["products"]) > 0

    def test_get_products_with_type_filter(self, client):
        """Test GET /api/products with type filter"""
        response = client.get("/api/products?type=running")
        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        for product in data["products"]:
            assert product["type"] == "running"

    def test_get_products_with_color_filter(self, client):
        """Test GET /api/products with color filter"""
        response = client.get("/api/products?color=red")
        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        for product in data["products"]:
            assert product["color"] == "red"

    def test_get_products_with_price_range(self, client):
        """Test GET /api/products with price range filters"""
        response = client.get("/api/products?price_min=50&price_max=100")
        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        for product in data["products"]:
            assert 50 <= product["price"] <= 100

    def test_get_products_with_size_filter(self, client):
        """Test GET /api/products with size filter"""
        response = client.get("/api/products?size=10")
        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        for product in data["products"]:
            assert 10.0 in product["sizes"]

    def test_get_products_invalid_price_range(self, client):
        """Test GET /api/products with invalid price range returns 400"""
        response = client.get("/api/products?price_min=100&price_max=50")
        assert response.status_code == 400
        assert "price_min cannot exceed price_max" in response.json()["detail"]

    def test_get_products_invalid_size(self, client):
        """Test GET /api/products with size outside valid range returns 400"""
        response = client.get("/api/products?size=20")
        assert response.status_code == 400
        assert "size must be between 6 and 13" in response.json()["detail"]

    def test_get_single_product_by_id(self, client):
        """Test GET /api/products/{shoe_id} returns single product"""
        # First get all products to get a valid ID
        all_products = client.get("/api/products").json()
        shoe_id = all_products["products"][0]["shoe_id"]

        response = client.get(f"/api/products/{shoe_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["shoe_id"] == shoe_id
        assert "name" in data
        assert "brand" in data
        assert "price" in data

    def test_get_single_product_not_found(self, client):
        """Test GET /api/products/{shoe_id} with invalid ID returns 404"""
        response = client.get("/api/products/invalid-shoe-id-12345")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestFeaturedEndpoint:
    """Test suite for /api/featured endpoint"""

    def test_get_featured_products(self, client):
        """Test GET /api/featured returns featured products only"""
        response = client.get("/api/featured")
        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        assert len(data["products"]) > 0
        for product in data["products"]:
            assert product["featured"] is True


class TestCategoriesEndpoint:
    """Test suite for /api/categories endpoint"""

    def test_get_categories(self, client):
        """Test GET /api/categories returns all available categories"""
        response = client.get("/api/categories")
        assert response.status_code == 200
        data = response.json()
        assert "types" in data
        assert "colors" in data
        assert isinstance(data["types"], list)
        assert isinstance(data["colors"], list)
        assert len(data["types"]) > 0
        assert len(data["colors"]) > 0


class TestSearchEndpoint:
    """Test suite for /api/search endpoint"""

    def test_search_with_natural_language(self, client):
        """Test POST /api/search with natural language query"""
        search_query = {"query": "red running shoes under $100"}
        response = client.post("/api/search", json=search_query)
        assert response.status_code == 200
        data = response.json()
        assert "agent_response" in data
        assert "products" in data
        assert isinstance(data["agent_response"], str)
        assert isinstance(data["products"], list)
        assert len(data["agent_response"]) > 0

    def test_search_with_session_id(self, client):
        """Test POST /api/search with session ID for continuity"""
        search_query = {
            "query": "show me formal shoes",
            "session_id": "test-session-123"
        }
        response = client.post("/api/search", json=search_query)
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert data["session_id"] is not None

    def test_search_empty_query(self, client):
        """Test POST /api/search with empty query returns 400"""
        search_query = {"query": ""}
        response = client.post("/api/search", json=search_query)
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()

    def test_search_missing_query(self, client):
        """Test POST /api/search without query field returns 422"""
        response = client.post("/api/search", json={})
        assert response.status_code == 422

    def test_search_whitespace_only_query(self, client):
        """Test POST /api/search with whitespace-only query returns 400"""
        search_query = {"query": "   "}
        response = client.post("/api/search", json=search_query)
        assert response.status_code == 400

    def test_search_query_too_long(self, client):
        """Test POST /api/search with overly long query returns 400"""
        search_query = {"query": "a" * 250}
        response = client.post("/api/search", json=search_query)
        assert response.status_code == 400
        assert "length" in response.json()["detail"].lower()
