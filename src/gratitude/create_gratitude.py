from datetime import datetime

import boto3


class CreateGratitude:
    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")
        self.table = self.dynamodb.Table("gratitudes")

    def create(self, email: str, request_datetime: datetime, gratitude: str) -> dict:
        put = self.table.update_item(
            Key={"email": email, "day": request_datetime.strftime("%Y-%m-%d")},
            UpdateExpression="SET gratitudes = list_append(if_not_exists(gratitudes, :empty_list), :new_grat)",
            ExpressionAttributeValues={":new_grat": [gratitude], ":empty_list": []},
        )

        return {
            "email": email,
            "day": request_datetime.strftime("%Y-%m-%d"),
            "gratitudes": [gratitude],
            "status_code": put["ResponseMetadata"]["HTTPStatusCode"],
        }
