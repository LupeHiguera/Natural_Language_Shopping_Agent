"""
Pydantic models for request/response validation.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from decimal import Decimal


# Product Models
class ShoeProduct(BaseModel):
    """Model representing a shoe product"""

    shoe_id: str
    name: str
    brand: str
    type: str
    color: str
    sizes: list[float]
    price: float
    image_url: str
    description: str
    featured: bool = False
    rating: float = Field(ge=0.0, le=5.0)
    stock: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "shoe_id": "nike-air-max-270-001",
                "name": "Nike Air Max 270",
                "brand": "Nike",
                "type": "running",
                "color": "red",
                "sizes": [9.0, 9.5, 10.0, 10.5, 11.0],
                "price": 99.99,
                "image_url": "https://example.com/nike-air-max.jpg",
                "description": "Comfortable running shoes with air cushioning",
                "featured": True,
                "rating": 4.5,
                "stock": True,
            }
        }


class ProductDetail(ShoeProduct):
    """Extended product model for detail view (can add more fields later)"""

    pass


# Filter Models
class ProductFilter(BaseModel):
    """Model for filtering products"""

    type: Optional[str] = None
    color: Optional[str] = None
    size: Optional[float] = None
    price_min: Optional[float] = Field(None, ge=0.0)
    price_max: Optional[float] = Field(None, ge=0.0)

    @field_validator("price_max")
    @classmethod
    def validate_price_range(cls, v, info):
        """Ensure price_max is greater than price_min if both are provided"""
        if v is not None and info.data.get("price_min") is not None:
            if v < info.data["price_min"]:
                raise ValueError("price_max must be greater than or equal to price_min")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "type": "running",
                "color": "red",
                "size": 10.0,
                "price_min": 50.0,
                "price_max": 150.0,
            }
        }


# Response Models
class ProductListResponse(BaseModel):
    """Response model for list of products"""

    products: list[ShoeProduct]
    count: int = 0

    def __init__(self, **data):
        super().__init__(**data)
        if self.count == 0:
            self.count = len(self.products)

    class Config:
        json_schema_extra = {
            "example": {
                "products": [
                    {
                        "shoe_id": "nike-air-max-270-001",
                        "name": "Nike Air Max 270",
                        "brand": "Nike",
                        "type": "running",
                        "color": "red",
                        "sizes": [9.0, 10.0, 11.0],
                        "price": 99.99,
                        "image_url": "https://example.com/nike.jpg",
                        "description": "Great running shoe",
                        "featured": True,
                        "rating": 4.5,
                        "stock": True,
                    }
                ],
                "count": 1,
            }
        }


# Search Models
class SearchRequest(BaseModel):
    """Model for natural language search request"""

    query: str = Field(..., description="Natural language search query")
    session_id: Optional[str] = Field(
        None, description="Session ID for conversation continuity"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "query": "red running shoes under $100",
                "session_id": "abc123-session-id",
            }
        }


class SearchResponse(BaseModel):
    """Model for search response from Bedrock agent"""

    agent_response: str = Field(..., description="Natural language response from agent")
    products: list[ShoeProduct] = Field(default_factory=list)
    session_id: Optional[str] = Field(None, description="Session ID for future queries")

    class Config:
        json_schema_extra = {
            "example": {
                "agent_response": "I found 5 red running shoes under $100 for you. Here are the top results:",
                "products": [
                    {
                        "shoe_id": "nike-revolution-5-001",
                        "name": "Nike Revolution 5",
                        "brand": "Nike",
                        "type": "running",
                        "color": "red",
                        "sizes": [9.0, 10.0, 11.0],
                        "price": 79.99,
                        "image_url": "https://example.com/nike-revolution.jpg",
                        "description": "Affordable running shoe",
                        "featured": False,
                        "rating": 4.2,
                        "stock": True,
                    }
                ],
                "session_id": "abc123-session-id",
            }
        }


# Category Models
class CategoriesResponse(BaseModel):
    """Response model for available categories"""

    types: list[str]
    colors: list[str]

    class Config:
        json_schema_extra = {
            "example": {
                "types": ["running", "casual", "formal", "athletic", "boots"],
                "colors": ["red", "blue", "black", "white", "brown"],
            }
        }


# Health Check Model
class HealthResponse(BaseModel):
    """Health check response"""

    status: str
    message: Optional[str] = None

    class Config:
        json_schema_extra = {"example": {"status": "healthy", "message": "All systems operational"}}