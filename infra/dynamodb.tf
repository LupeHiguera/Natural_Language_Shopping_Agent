resource "aws_dynamodb_table" "shoe-inventory-table" {
  name           = "ShoeInventory"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "shoe_id"

  attribute {
    name = "shoe_id"
    type = "S"
  }
}