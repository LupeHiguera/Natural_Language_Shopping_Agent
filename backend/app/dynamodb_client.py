"""
DynamoDB client for interacting with the ShoeInventory table.
Handles product queries, filtering, and retrieval operations.
"""
import boto3
from typing import Optional, Dict, List, Any
from decimal import Decimal
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError


class DynamoDBClient:
    """Client for interacting with DynamoDB ShoeInventory table"""

    def __init__(
        self,
        table_name: str,
        region: str = "us-east-1",
        mock_mode: bool = False,
    ):
        """
        Initialize DynamoDB client.

        Args:
            table_name: Name of the DynamoDB table
            region: AWS region (defaults to us-east-1)
            mock_mode: If True, returns mock data instead of calling AWS
        """
        self.table_name = table_name
        self.region = region
        self.mock_mode = mock_mode

        # Initialize boto3 resource only if not in mock mode
        if not self.mock_mode:
            dynamodb = boto3.resource("dynamodb", region_name=self.region)
            self._table = dynamodb.Table(self.table_name)
        else:
            self._table = None

    def get_all_products(self) -> List[Dict[str, Any]]:
        """
        Retrieve all products from the table.

        Returns:
            List of all products

        Raises:
            Exception: If DynamoDB query fails
        """
        if self.mock_mode:
            return self._get_mock_products()

        try:
            products = []
            scan_kwargs = {}

            # Handle pagination
            while True:
                response = self._table.scan(**scan_kwargs)
                products.extend(response.get("Items", []))

                # Check if there are more items to fetch
                if "LastEvaluatedKey" not in response:
                    break

                scan_kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]

            return self._convert_decimals(products)

        except ClientError as e:
            raise Exception(f"DynamoDB error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error retrieving products: {str(e)}")

    def get_products_by_filters(
        self,
        type: Optional[str] = None,
        color: Optional[str] = None,
        size: Optional[float] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve products with filters applied.

        Args:
            type: Filter by shoe type (running, casual, etc.)
            color: Filter by color
            size: Filter by available size
            price_min: Minimum price filter
            price_max: Maximum price filter

        Returns:
            List of filtered products

        Raises:
            Exception: If DynamoDB query fails
        """
        if self.mock_mode:
            return self._get_mock_products(
                type=type, color=color, size=size, price_min=price_min, price_max=price_max
            )

        try:
            # Build filter expression
            filter_expression = None

            if type:
                filter_expression = Attr("type").eq(type)

            if color:
                color_filter = Attr("color").eq(color)
                filter_expression = (
                    color_filter if filter_expression is None else filter_expression & color_filter
                )

            if size:
                size_filter = Attr("sizes").contains(size)
                filter_expression = (
                    size_filter if filter_expression is None else filter_expression & size_filter
                )

            if price_min is not None:
                price_min_filter = Attr("price").gte(Decimal(str(price_min)))
                filter_expression = (
                    price_min_filter
                    if filter_expression is None
                    else filter_expression & price_min_filter
                )

            if price_max is not None:
                price_max_filter = Attr("price").lte(Decimal(str(price_max)))
                filter_expression = (
                    price_max_filter
                    if filter_expression is None
                    else filter_expression & price_max_filter
                )

            # Execute scan with filter
            products = []
            scan_kwargs = {}
            if filter_expression:
                scan_kwargs["FilterExpression"] = filter_expression

            # Handle pagination
            while True:
                response = self._table.scan(**scan_kwargs)
                products.extend(response.get("Items", []))

                # Check if there are more items to fetch
                if "LastEvaluatedKey" not in response:
                    break

                scan_kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]

            return self._convert_decimals(products)

        except ClientError as e:
            raise Exception(f"DynamoDB error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error filtering products: {str(e)}")

    def get_product_by_id(self, shoe_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single product by its ID.

        Args:
            shoe_id: The shoe product ID

        Returns:
            Product dictionary or None if not found

        Raises:
            Exception: If DynamoDB query fails
        """
        if self.mock_mode:
            mock_products = self._get_mock_products()
            for product in mock_products:
                if product["shoe_id"] == shoe_id:
                    return product
            return None

        try:
            response = self._table.get_item(Key={"shoe_id": shoe_id})

            if "Item" in response:
                return self._convert_decimals([response["Item"]])[0]

            return None

        except ClientError as e:
            raise Exception(f"DynamoDB error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error retrieving product: {str(e)}")

    def get_featured_products(self) -> List[Dict[str, Any]]:
        """
        Retrieve only featured products.

        Returns:
            List of featured products

        Raises:
            Exception: If DynamoDB query fails
        """
        if self.mock_mode:
            mock_products = self._get_mock_products()
            return [p for p in mock_products if p.get("featured", False)]

        try:
            filter_expression = Attr("featured").eq(True)

            products = []
            scan_kwargs = {"FilterExpression": filter_expression}

            # Handle pagination
            while True:
                response = self._table.scan(**scan_kwargs)
                products.extend(response.get("Items", []))

                # Check if there are more items to fetch
                if "LastEvaluatedKey" not in response:
                    break

                scan_kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]

            return self._convert_decimals(products)

        except ClientError as e:
            raise Exception(f"DynamoDB error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error retrieving featured products: {str(e)}")

    def get_categories(self) -> Dict[str, List[str]]:
        """
        Retrieve all unique categories (types and colors).

        Returns:
            Dictionary with 'types' and 'colors' lists

        Raises:
            Exception: If DynamoDB query fails
        """
        if self.mock_mode:
            return {
                "types": ["running", "casual", "formal", "athletic", "boots"],
                "colors": ["red", "blue", "black", "white", "brown"],
            }

        try:
            products = []
            scan_kwargs = {}

            # Handle pagination
            while True:
                response = self._table.scan(**scan_kwargs)
                products.extend(response.get("Items", []))

                # Check if there are more items to fetch
                if "LastEvaluatedKey" not in response:
                    break

                scan_kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]

            # Extract unique types and colors
            types = set()
            colors = set()

            for product in products:
                if "type" in product:
                    types.add(product["type"])
                if "color" in product:
                    colors.add(product["color"])

            return {"types": sorted(list(types)), "colors": sorted(list(colors))}

        except ClientError as e:
            raise Exception(f"DynamoDB error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error retrieving categories: {str(e)}")

    def _convert_decimals(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Convert Decimal types to float for JSON serialization.

        Args:
            items: List of items from DynamoDB

        Returns:
            List with Decimals converted to floats
        """
        converted_items = []
        for item in items:
            converted_item = {}
            for key, value in item.items():
                if isinstance(value, Decimal):
                    converted_item[key] = float(value)
                else:
                    converted_item[key] = value
            converted_items.append(converted_item)
        return converted_items

    def _get_mock_products(
        self,
        type: Optional[str] = None,
        color: Optional[str] = None,
        size: Optional[float] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Generate mock product data for development.

        Args:
            type: Filter by shoe type
            color: Filter by color
            size: Filter by available size
            price_min: Minimum price filter
            price_max: Maximum price filter

        Returns:
            List of mock products (filtered if criteria provided)
        """
        mock_products = [
            {
                "shoe_id": "mock-001",
                "name": "Mock Running Shoe",
                "brand": "Nike",
                "type": "running",
                "color": "red",
                "sizes": [9.0, 10.0, 11.0],
                "price": 89.99,
                "image_url": "https://example.com/shoe1.jpg",
                "description": "Mock running shoe for testing",
                "featured": True,
                "rating": 4.5,
                "stock": True,
            },
            {
                "shoe_id": "mock-002",
                "name": "Mock Casual Sneaker",
                "brand": "Adidas",
                "type": "casual",
                "color": "blue",
                "sizes": [8.0, 9.0, 10.0],
                "price": 75.50,
                "image_url": "https://example.com/shoe2.jpg",
                "description": "Mock casual sneaker for testing",
                "featured": False,
                "rating": 4.3,
                "stock": True,
            },
            {
                "shoe_id": "mock-003",
                "name": "Mock Formal Shoe",
                "brand": "Clarks",
                "type": "formal",
                "color": "black",
                "sizes": [9.0, 10.0, 11.0, 12.0],
                "price": 120.00,
                "image_url": "https://example.com/shoe3.jpg",
                "description": "Mock formal shoe for testing",
                "featured": False,
                "rating": 4.7,
                "stock": True,
            },
            {
                "shoe_id": "mock-004",
                "name": "Mock Running Trainer",
                "brand": "Nike",
                "type": "running",
                "color": "black",
                "sizes": [9.0, 10.0, 11.0],
                "price": 95.00,
                "image_url": "https://example.com/shoe4.jpg",
                "description": "Mock running trainer for testing",
                "featured": True,
                "rating": 4.6,
                "stock": True,
            },
        ]

        # Apply filters
        filtered_products = mock_products

        if type:
            filtered_products = [p for p in filtered_products if p["type"] == type]

        if color:
            filtered_products = [p for p in filtered_products if p["color"] == color]

        if size:
            filtered_products = [p for p in filtered_products if size in p["sizes"]]

        if price_min is not None:
            filtered_products = [p for p in filtered_products if p["price"] >= price_min]

        if price_max is not None:
            filtered_products = [p for p in filtered_products if p["price"] <= price_max]

        return filtered_products