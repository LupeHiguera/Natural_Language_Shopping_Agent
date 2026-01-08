import boto3
import json
from decimal import Decimal
from boto3.dynamodb.conditions import Attr


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            if obj % 1 == 0:
                return int(obj)
            return float(obj)
        return super().default(obj)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ShoeInventory')

def scan_table(shoe_parameters):
    filter_expression = None

    # Shoe Parameters
    shoe_type = shoe_parameters.get('type')
    shoe_color = shoe_parameters.get('color')
    shoe_size = shoe_parameters.get('size')
    shoe_min_price = shoe_parameters.get('min_price')
    shoe_max_price = shoe_parameters.get('max_price')

    if shoe_type:
        condition = Attr('type').eq(shoe_type)
        if filter_expression is None:
            filter_expression = condition
        else:
            filter_expression = filter_expression & condition

    if shoe_color:
        condition = Attr('color').eq(shoe_color)
        if filter_expression is None:
            filter_expression = condition
        else:
            filter_expression = filter_expression & condition

    if shoe_size:
        condition = Attr('size').eq(shoe_size)
        if filter_expression is None:
            filter_expression = condition
        else:
            filter_expression = filter_expression & condition

    if shoe_min_price:
        condition = Attr('price').gte(shoe_min_price)
        if filter_expression is None:
            filter_expression = condition
        else:
            filter_expression = filter_expression & condition

    if shoe_max_price:
        condition = Attr('price').lte(shoe_max_price)
        if filter_expression is None:
            filter_expression = condition
        else:
            filter_expression = filter_expression & condition

    if filter_expression:
        objects = table.scan(FilterExpression=filter_expression)
    else:
        objects = table.scan()
    return objects['Items']

def lambda_handler(event, context):
    print("Received event:", json.dumps(event, default=str))

    try:
        # Check if this is a Bedrock Agent invocation
        if 'agent' in event or 'actionGroup' in event:
            # Bedrock Agent format
            action_group = event.get('actionGroup', '')
            function = event.get('function', '')
            parameters = event.get('parameters', [])

            print(f"Action Group: {action_group}, Function: {function}")
            print(f"Parameters: {parameters}")

            # Convert parameters list to dict
            shoe_parameters = {}
            for param in parameters:
                name = param.get('name', '')
                value = param.get('value', '')
                if name and value:
                    # Convert numeric strings to numbers
                    if name in ['size', 'min_price', 'max_price']:
                        try:
                            value = float(value)
                        except:
                            pass
                    shoe_parameters[name] = value

            print(f"Shoe parameters: {shoe_parameters}")

            scanned_objects = scan_table(shoe_parameters)
            print(f"Found {len(scanned_objects)} shoes")

            # Format response for Bedrock Agent
            result_text = json.dumps(scanned_objects, cls=DecimalEncoder)

            return {
                'messageVersion': '1.0',
                'response': {
                    'actionGroup': action_group,
                    'function': function,
                    'functionResponse': {
                        'responseBody': {
                            'TEXT': {
                                'body': result_text
                            }
                        }
                    }
                }
            }
        else:
            # API Gateway format
            body = event.get('body', '{}')
            if isinstance(body, str):
                body = json.loads(body)

            shoe_parameters = body.get('ShoeParameters', {})
            scanned_objects = scan_table(shoe_parameters)

            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(scanned_objects, cls=DecimalEncoder)
            }

    except Exception as e:
        print(f"Error: {str(e)}")
        # Return error in Bedrock format if it looks like a Bedrock request
        if 'agent' in event or 'actionGroup' in event:
            return {
                'messageVersion': '1.0',
                'response': {
                    'actionGroup': event.get('actionGroup', ''),
                    'function': event.get('function', ''),
                    'functionResponse': {
                        'responseBody': {
                            'TEXT': {
                                'body': json.dumps({"error": str(e)})
                            }
                        }
                    }
                }
            }
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }
