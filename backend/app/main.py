"""
FastAPI application with endpoints for shoe shopping.
Provides browsing, filtering, and AI-powered search functionality.
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from typing import Optional

from app.config import settings
from app.models import (
    ShoeProduct,
    ProductDetail,
    ProductFilter,
    ProductListResponse,
    SearchRequest,
    SearchResponse,
    CategoriesResponse,
    HealthResponse,
)
from app.dynamodb_client import DynamoDBClient
from app.bedrock_client import BedrockClient

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Backend API for shoe shopping with AI-powered search",
    version="1.0.0",
)

# Custom middleware to add CORS headers for testing
class CORSHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Always add CORS header for testing (in production, FastAPI CORS middleware handles this)
        if "access-control-allow-origin" not in response.headers:
            response.headers["access-control-allow-origin"] = "*"
        return response

# Add custom CORS header middleware
app.add_middleware(CORSHeaderMiddleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins + ["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
dynamodb_client = DynamoDBClient(
    table_name=settings.dynamodb_table_name,
    region=settings.aws_region,
    mock_mode=settings.mock_mode,
)

# Initialize Bedrock client only if credentials are provided
bedrock_client = None
if settings.bedrock_agent_id and settings.bedrock_agent_alias_id:
    bedrock_client = BedrockClient(
        agent_id=settings.bedrock_agent_id,
        agent_alias_id=settings.bedrock_agent_alias_id,
        region=settings.aws_region,
        mock_mode=settings.mock_mode,
    )
else:
    # Use mock mode if no credentials
    bedrock_client = BedrockClient(
        agent_id="mock-agent-id",
        agent_alias_id="mock-alias-id",
        region=settings.aws_region,
        mock_mode=True,
    )


# Health Check Endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify API is running.

    Returns:
        HealthResponse with status
    """
    return HealthResponse(status="healthy", message="All systems operational")


# Products Endpoints
@app.get("/api/products", response_model=ProductListResponse)
async def get_products(
    type: Optional[str] = Query(None, description="Filter by shoe type"),
    color: Optional[str] = Query(None, description="Filter by color"),
    size: Optional[float] = Query(None, description="Filter by available size"),
    price_min: Optional[float] = Query(None, ge=0.0, description="Minimum price"),
    price_max: Optional[float] = Query(None, ge=0.0, description="Maximum price"),
):
    """
    Retrieve all products with optional filters.

    Args:
        type: Filter by shoe type (running, casual, formal, etc.)
        color: Filter by color
        size: Filter by available size
        price_min: Minimum price filter
        price_max: Maximum price filter

    Returns:
        ProductListResponse containing filtered products

    Raises:
        HTTPException: If database query fails
    """
    try:
        # Check if any filters are provided
        if any([type, color, size, price_min, price_max]):
            # Use filtered query
            products = dynamodb_client.get_products_by_filters(
                type=type,
                color=color,
                size=size,
                price_min=price_min,
                price_max=price_max,
            )
        else:
            # Get all products
            products = dynamodb_client.get_all_products()

        # Convert to Pydantic models
        shoe_products = [ShoeProduct(**product) for product in products]

        return ProductListResponse(products=shoe_products)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving products: {str(e)}")


@app.get("/api/products/{shoe_id}", response_model=ProductDetail)
async def get_product_by_id(shoe_id: str):
    """
    Retrieve a single product by its ID.

    Args:
        shoe_id: The unique shoe product ID

    Returns:
        ProductDetail for the requested shoe

    Raises:
        HTTPException: If product not found or database error
    """
    try:
        product = dynamodb_client.get_product_by_id(shoe_id)

        if product is None:
            raise HTTPException(status_code=404, detail=f"Product with ID '{shoe_id}' not found")

        return ProductDetail(**product)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving product: {str(e)}")


@app.get("/api/featured", response_model=ProductListResponse)
async def get_featured_products():
    """
    Retrieve featured products for homepage display.

    Returns:
        ProductListResponse containing only featured products

    Raises:
        HTTPException: If database query fails
    """
    try:
        products = dynamodb_client.get_featured_products()
        shoe_products = [ShoeProduct(**product) for product in products]

        return ProductListResponse(products=shoe_products)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving featured products: {str(e)}")


@app.get("/api/categories", response_model=CategoriesResponse)
async def get_categories():
    """
    Retrieve all available categories (types and colors).

    Returns:
        CategoriesResponse with lists of types and colors

    Raises:
        HTTPException: If database query fails
    """
    try:
        categories = dynamodb_client.get_categories()

        return CategoriesResponse(
            types=categories["types"],
            colors=categories["colors"],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving categories: {str(e)}")


# AI Search Endpoint
@app.post("/api/search", response_model=SearchResponse)
async def search_products(request: SearchRequest):
    """
    Natural language search using Bedrock agent.

    Args:
        request: SearchRequest containing natural language query

    Returns:
        SearchResponse with agent response and matching products

    Raises:
        HTTPException: If query is invalid or agent invocation fails
    """
    try:
        # Validate query
        if not request.query or request.query.strip() == "":
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        # Invoke Bedrock agent
        result = bedrock_client.invoke_agent(
            query=request.query,
            session_id=request.session_id,
        )

        # Convert products to Pydantic models
        products = [ShoeProduct(**product) for product in result.get("products", [])]

        return SearchResponse(
            agent_response=result.get("agent_response", ""),
            products=products,
            session_id=result.get("session_id"),
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing search: {str(e)}")


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint with API information.

    Returns:
        Dictionary with API details
    """
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "description": "Backend API for shoe shopping with AI-powered search",
        "endpoints": {
            "health": "/health",
            "products": "/api/products",
            "product_detail": "/api/products/{shoe_id}",
            "featured": "/api/featured",
            "categories": "/api/categories",
            "search": "/api/search",
        },
    }