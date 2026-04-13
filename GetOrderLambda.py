import json
import os
import boto3

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME"]

table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        order_id = event.get("pathParameters", {}).get("id")

        if not order_id:
            return response(400, {"message": "Falta el id del pedido"})

        result = table.get_item(Key={"Id": order_id})
        item = result.get("Item")

        if not item:
            return response(404, {"message": "Pedido no encontrado"})

        return response(200, item)

    except Exception as e:
        return response(500, {"message": str(e)})

def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }