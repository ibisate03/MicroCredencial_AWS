import json
import uuid
import os
from datetime import datetime

import boto3

dynamodb = boto3.resource("dynamodb")
events_client = boto3.client("events")

TABLE_NAME = os.environ["TABLE_NAME"]

table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        customer_email = body.get("customerEmail")
        product = body.get("product")
        quantity = body.get("quantity")

        if not customer_email or not product or quantity is None:
            return response(400, {"message": "Faltan campos"})

        order_id = str(uuid.uuid4())

        item = {
            "Id": order_id,
            "customerEmail": customer_email,
            "product": product,
            "quantity": quantity,
            "status": "PENDING",
            "createdAt": datetime.utcnow().isoformat()
        }

        table.put_item(Item=item)

        events_client.put_events(
            Entries=[
                {
                    "Source": "shop.orders",
                    "DetailType": "OrderCreated",
                    "Detail": json.dumps({
                        "orderId": order_id,
                        "customerEmail": customer_email,
                        "product": product,
                        "quantity": quantity
                    })
                }
            ]
        )

        return response(201, {
            "orderId": order_id,
            "status": "PENDING"
        })

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