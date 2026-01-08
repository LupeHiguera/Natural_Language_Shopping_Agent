"""
Lambda handler for FastAPI application using Mangum.
This allows the FastAPI app to run on AWS Lambda.
"""
from mangum import Mangum
from app.main import app

# Create the Lambda handler
handler = Mangum(app, lifespan="off")
