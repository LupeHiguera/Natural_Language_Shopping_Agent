# Script to populate DynamoDB - to be implemented
import decimal

import boto3
import json

data = json.load(open('seed_data.json'), parse_float=decimal.Decimal)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ShoeInventory')


for shoe in data:
    table.put_item(Item=shoe)