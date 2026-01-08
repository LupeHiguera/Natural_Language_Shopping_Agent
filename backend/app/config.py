"""
Configuration module for backend application.
Handles environment variables and application settings.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # AWS Configuration
    aws_region: str = "us-east-1"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None

    # DynamoDB Configuration
    dynamodb_table_name: str = "ShoeInventory"

    # Bedrock Configuration
    bedrock_agent_id: Optional[str] = None
    bedrock_agent_alias_id: Optional[str] = None

    # Application Configuration
    app_name: str = "Shoe Shopping Agent"
    debug: bool = False

    # CORS Configuration - Add your S3/CloudFront URL here when deployed
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        # Add your S3 bucket URL here, e.g.:
        # "http://your-bucket-name.s3-website-us-east-1.amazonaws.com",
        # Or CloudFront URL:
        # "https://d1234567890.cloudfront.net",
    ]

    # Mock Mode (for development before AWS setup)
    mock_mode: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()