"""FastAPI application with enhanced error handling and validation."""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.config import settings
from app.models import (
    ShoeProduct,
    ProductDetail,
    ProductListResponse,
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



# Configure CORS - Only allow specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # Only configured origins, no wildcard
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Only methods we actually use
    allow_headers=["Content-Type", "Authorization"],  # Only headers we need
)

# Initialize clients
dynamodb_client = DynamoDBClient(
    table_name=settings.dynamodb_table_name,
    region=settings.aws_region,
    mock_mode=settings.mock_mode,
)

bedrock_client = None
if settings.bedrock_agent_id and settings.bedrock_agent_alias_id:
    bedrock_client = BedrockClient(
        agent_id=settings.bedrock_agent_id,
        agent_alias_id=settings.bedrock_agent_alias_id,
        region=settings.aws_region,
        mock_mode=settings.mock_mode,
    )
else:
    bedrock_client = BedrockClient(
        agent_id="mock-agent-id",
        agent_alias_id="mock-alias-id",
        region=settings.aws_region,
        mock_mode=True,
    )


# Health Check Endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    try:
        return HealthResponse(status="healthy", message="All systems operational")
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


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
    """
    try:
        # Validate price range
        if price_min is not None and price_max is not None and price_min > price_max:
            raise HTTPException(
                status_code=400, detail="price_min cannot exceed price_max"
            )

        # Validate size range (optional)
        if size is not None and (size < 6 or size > 13):
            raise HTTPException(status_code=400, detail="size must be between 6 and 13")

        if any([type, color, size, price_min, price_max]):
            products = dynamodb_client.get_products_by_filters(
                type=type,
                color=color,
                size=size,
                price_min=price_min,
                price_max=price_max,
            )
        else:
            products = dynamodb_client.get_all_products()

        shoe_products = [ShoeProduct(**product) for product in products]
        return ProductListResponse(products=shoe_products)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving products: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error retrieving products: {str(e)}"
        )


@app.get("/api/products/{shoe_id}", response_model=ProductDetail)
async def get_product_by_id(shoe_id: str):
    """
    Retrieve a single product by its ID.
    """
    try:
        product = dynamodb_client.get_product_by_id(shoe_id)
        if product is None:
            raise HTTPException(
                status_code=404, detail=f"Product with ID '{shoe_id}' not found"
            )
        return ProductDetail(**product)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving product {shoe_id}: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error retrieving product: {str(e)}"
        )


@app.get("/api/featured", response_model=ProductListResponse)
async def get_featured_products():
    """
    Retrieve featured products for homepage display.
    """
    try:
        products = dynamodb_client.get_featured_products()
        shoe_products = [ShoeProduct(**product) for product in products]
        return ProductListResponse(products=shoe_products)
    except Exception as e:
        logger.error(f"Error retrieving featured products: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error retrieving featured products: {str(e)}"
        )


@app.get("/api/categories", response_model=CategoriesResponse)
async def get_categories():
    """
    Retrieve all available categories (types and colors).
    """
    try:
        categories = dynamodb_client.get_categories()
        return CategoriesResponse(
            types=categories["types"],
            colors=categories["colors"],
        )
    except Exception as e:
        logger.error(f"Error retrieving categories: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error retrieving categories: {str(e)}"
        )


# AI Search Endpoint
@app.post("/api/search", response_model=SearchResponse)
async def search_products(request: SearchRequest):
    """
    Natural language search using Bedrock agent.
    """
    try:
        # Validate query presence
        if not request.query or request.query.strip() == "":
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        # Validate query length (optional)
        if len(request.query.strip()) > 200:
            raise HTTPException(status_code=400, detail="Query exceeds maximum length")

        # Ensure bedrock client is configured
        if not bedrock_client:
            raise HTTPException(status_code=500, detail="Bedrock client not configured")
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
        logger.error(f"Validation error in search request: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing search: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error processing search: {str(e)}"
        )


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint with API information.
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
