import json


class Response:
    @staticmethod
    def handle(message, status_code=200):
        return {
            "statusCode": str(status_code),
            "body": json.dumps(message),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        }
