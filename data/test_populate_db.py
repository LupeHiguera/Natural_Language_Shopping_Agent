"""
Test cases for populate_db.py script.
Following TDD - these tests should fail initially.
"""
import pytest
import json
from unittest.mock import Mock, patch, mock_open
from decimal import Decimal
import sys
import os

# Add parent directory to path to import populate_db
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestLoadSeedData:
    """Test suite for loading seed data from JSON"""

    def test_load_seed_data_from_file(self):
        """Test loading shoe data from JSON file"""
        from populate_db import load_seed_data

        # Mock file content
        mock_json = json.dumps([
            {
                "shoe_id": "1",
                "name": "Nike Air Max",
                "brand": "Nike",
                "type": "running",
                "color": "red",
                "sizes": [9, 10, 11],
                "price": 99.99,
                "image_url": "https://example.com/shoe1.jpg",
                "description": "Great running shoe",
                "featured": True,
                "rating": 4.5,
                "stock": True
            }
        ])

        with patch('builtins.open', mock_open(read_data=mock_json)):
            data = load_seed_data("seed_data.json")

        assert len(data) == 1
        assert data[0]["shoe_id"] == "1"
        assert data[0]["name"] == "Nike Air Max"

    def test_load_seed_data_file_not_found(self):
        """Test handling of missing seed data file"""
        from populate_db import load_seed_data

        with pytest.raises(FileNotFoundError):
            load_seed_data("nonexistent_file.json")

    def test_load_seed_data_invalid_json(self):
        """Test handling of invalid JSON in seed data file"""
        from populate_db import load_seed_data

        with patch('builtins.open', mock_open(read_data='{invalid json')):
            with pytest.raises(json.JSONDecodeError):
                load_seed_data("seed_data.json")

    def test_load_seed_data_validates_required_fields(self):
        """Test that seed data validates required fields"""
        from populate_db import load_seed_data, validate_shoe_data

        mock_json = json.dumps([
            {
                "shoe_id": "1",
                "name": "Nike Air Max"
                # Missing required fields
            }
        ])

        with patch('builtins.open', mock_open(read_data=mock_json)):
            data = load_seed_data("seed_data.json")
            with pytest.raises(ValueError):
                validate_shoe_data(data[0])


class TestValidateShoeData:
    """Test suite for validating shoe data structure"""

    def test_validate_complete_shoe_data(self):
        """Test validation passes for complete shoe data"""
        from populate_db import validate_shoe_data

        shoe = {
            "shoe_id": "1",
            "name": "Nike Air Max",
            "brand": "Nike",
            "type": "running",
            "color": "red",
            "sizes": [9, 10, 11],
            "price": 99.99,
            "image_url": "https://example.com/shoe.jpg",
            "description": "Great shoe",
            "featured": True,
            "rating": 4.5,
            "stock": True
        }

        # Should not raise exception
        result = validate_shoe_data(shoe)
        assert result is True

    def test_validate_missing_required_field(self):
        """Test validation fails when required field is missing"""
        from populate_db import validate_shoe_data

        shoe = {
            "shoe_id": "1",
            "name": "Nike Air Max"
            # Missing other required fields
        }

        with pytest.raises(ValueError, match="Missing required field"):
            validate_shoe_data(shoe)

    def test_validate_invalid_price(self):
        """Test validation fails for invalid price"""
        from populate_db import validate_shoe_data

        shoe = {
            "shoe_id": "1",
            "name": "Nike Air Max",
            "brand": "Nike",
            "type": "running",
            "color": "red",
            "sizes": [9, 10, 11],
            "price": -50,  # Invalid negative price
            "image_url": "https://example.com/shoe.jpg",
            "description": "Great shoe",
            "featured": True,
            "rating": 4.5,
            "stock": True
        }

        with pytest.raises(ValueError, match="Price must be positive"):
            validate_shoe_data(shoe)

    def test_validate_invalid_sizes_array(self):
        """Test validation fails for invalid sizes array"""
        from populate_db import validate_shoe_data

        shoe = {
            "shoe_id": "1",
            "name": "Nike Air Max",
            "brand": "Nike",
            "type": "running",
            "color": "red",
            "sizes": [],  # Empty sizes array
            "price": 99.99,
            "image_url": "https://example.com/shoe.jpg",
            "description": "Great shoe",
            "featured": True,
            "rating": 4.5,
            "stock": True
        }

        with pytest.raises(ValueError, match="Sizes array cannot be empty"):
            validate_shoe_data(shoe)


class TestConvertToDynamoDBFormat:
    """Test suite for converting shoe data to DynamoDB format"""

    def test_convert_price_to_decimal(self):
        """Test converting price from float to Decimal for DynamoDB"""
        from populate_db import convert_to_dynamodb_format

        shoe = {
            "shoe_id": "1",
            "name": "Nike Air Max",
            "price": 99.99
        }

        converted = convert_to_dynamodb_format(shoe)

        assert isinstance(converted["price"], Decimal)
        assert converted["price"] == Decimal("99.99")

    def test_convert_rating_to_decimal(self):
        """Test converting rating from float to Decimal for DynamoDB"""
        from populate_db import convert_to_dynamodb_format

        shoe = {
            "shoe_id": "1",
            "name": "Nike Air Max",
            "price": 99.99,
            "rating": 4.5
        }

        converted = convert_to_dynamodb_format(shoe)

        assert isinstance(converted["rating"], Decimal)
        assert converted["rating"] == Decimal("4.5")

    def test_convert_preserves_other_fields(self):
        """Test conversion preserves all other fields"""
        from populate_db import convert_to_dynamodb_format

        shoe = {
            "shoe_id": "1",
            "name": "Nike Air Max",
            "brand": "Nike",
            "type": "running",
            "sizes": [9, 10, 11],
            "price": 99.99,
            "featured": True
        }

        converted = convert_to_dynamodb_format(shoe)

        assert converted["shoe_id"] == "1"
        assert converted["name"] == "Nike Air Max"
        assert converted["brand"] == "Nike"
        assert converted["sizes"] == [9, 10, 11]
        assert converted["featured"] is True


class TestPopulateDatabase:
    """Test suite for populating DynamoDB table"""

    @pytest.fixture
    def mock_dynamodb_table(self):
        """Create mock DynamoDB table"""
        with patch('populate_db.boto3.resource') as mock_boto:
            mock_table = Mock()
            mock_boto.return_value.Table.return_value = mock_table
            yield mock_table

    def test_populate_database_batch_write(self, mock_dynamodb_table):
        """Test batch writing items to DynamoDB"""
        from populate_db import populate_database

        shoes = [
            {
                "shoe_id": "1",
                "name": "Nike Air Max",
                "brand": "Nike",
                "type": "running",
                "color": "red",
                "sizes": [9, 10, 11],
                "price": Decimal("99.99"),
                "image_url": "https://example.com/shoe.jpg",
                "description": "Great shoe",
                "featured": True,
                "rating": Decimal("4.5"),
                "stock": True
            }
        ]

        populate_database(shoes, mock_dynamodb_table)

        # Verify batch_writer was called
        mock_dynamodb_table.batch_writer.assert_called_once()

    def test_populate_database_handles_empty_list(self, mock_dynamodb_table):
        """Test populating database with empty list"""
        from populate_db import populate_database

        shoes = []

        result = populate_database(shoes, mock_dynamodb_table)

        # Should handle gracefully and return 0 items written
        assert result == 0

    def test_populate_database_counts_items(self, mock_dynamodb_table):
        """Test that populate returns correct count of items written"""
        from populate_db import populate_database

        shoes = [
            {"shoe_id": str(i), "name": f"Shoe {i}", "price": Decimal("99.99")}
            for i in range(10)
        ]

        result = populate_database(shoes, mock_dynamodb_table)

        assert result == 10


class TestMainFunction:
    """Test suite for main execution function"""

    @patch('populate_db.load_seed_data')
    @patch('populate_db.populate_database')
    @patch('populate_db.boto3.resource')
    def test_main_execution_flow(self, mock_boto, mock_populate, mock_load):
        """Test main function executes complete flow"""
        from populate_db import main

        # Mock data
        mock_shoes = [
            {
                "shoe_id": "1",
                "name": "Test Shoe",
                "brand": "Nike",
                "type": "running",
                "color": "red",
                "sizes": [10],
                "price": 99.99,
                "image_url": "https://example.com/shoe.jpg",
                "description": "Test",
                "featured": False,
                "rating": 4.5,
                "stock": True
            }
        ]
        mock_load.return_value = mock_shoes
        mock_populate.return_value = 1

        result = main()

        assert result == 1
        mock_load.assert_called_once()
        mock_populate.assert_called_once()

    @patch('populate_db.load_seed_data')
    def test_main_handles_file_not_found(self, mock_load):
        """Test main function handles missing seed file"""
        from populate_db import main

        mock_load.side_effect = FileNotFoundError("seed_data.json not found")

        with pytest.raises(FileNotFoundError):
            main()

    @patch('populate_db.load_seed_data')
    @patch('populate_db.boto3.resource')
    def test_main_handles_dynamodb_error(self, mock_boto, mock_load):
        """Test main function handles DynamoDB errors"""
        from populate_db import main

        mock_load.return_value = [{"shoe_id": "1"}]
        mock_boto.side_effect = Exception("DynamoDB connection failed")

        with pytest.raises(Exception, match="DynamoDB connection failed"):
            main()


class TestDryRunMode:
    """Test suite for dry-run mode"""

    def test_dry_run_validates_without_writing(self):
        """Test dry-run mode validates data without writing to DynamoDB"""
        from populate_db import main

        with patch('populate_db.load_seed_data') as mock_load:
            mock_load.return_value = [
                {
                    "shoe_id": "1",
                    "name": "Test Shoe",
                    "brand": "Nike",
                    "type": "running",
                    "color": "red",
                    "sizes": [10],
                    "price": 99.99,
                    "image_url": "https://example.com/shoe.jpg",
                    "description": "Test",
                    "featured": False,
                    "rating": 4.5,
                    "stock": True
                }
            ]

            # Should validate but not write
            result = main(dry_run=True)

            # In dry run, should return number of items that would be written
            assert result == 1