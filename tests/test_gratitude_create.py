import unittest
from datetime import datetime

import boto3
from moto import mock_dynamodb2

from src.gratitude.create_gratitude import CreateGratitude


class TestCreateGatitude(unittest.TestCase):
    @mock_dynamodb2
    def test_creates_gratitude(self):

        dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")

        table = dynamodb.create_table(
            TableName="gratitudes",
            KeySchema=[
                {"AttributeName": "email", "KeyType": "HASH"},
                {"AttributeName": "day", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "email", "AttributeType": "S"},
                {"AttributeName": "day", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )

        email = "user@email"
        request_datetime = datetime.today()
        gratitude = "I am grateful for tests"
        client = CreateGratitude()
        response = client.create(email, request_datetime, gratitude)
        expected = {
            "email": "user@email",
            "day": request_datetime.strftime("%Y-%m-%d"),
            "gratitudes": ["I am grateful for tests"],
            "status_code": 200,
        }
        self.assertEqual(response, expected)

        result = table.get_item(
            Key={"email": email, "day": request_datetime.strftime("%Y-%m-%d")}
        )

        print(result)

    @mock_dynamodb2
    def test_update_supports_list_append_with_nested_if_not_exists_operation(self):
        dynamo = boto3.resource("dynamodb", region_name="us-west-1")
        table_name = "test"

        dynamo.create_table(
            TableName=table_name,
            AttributeDefinitions=[{"AttributeName": "Id", "AttributeType": "S"}],
            KeySchema=[{"AttributeName": "Id", "KeyType": "HASH"}],
            ProvisionedThroughput={"ReadCapacityUnits": 20, "WriteCapacityUnits": 20},
        )

        table = dynamo.Table(table_name)

        table.put_item(Item={"Id": "item-id", "nest1": {"nest2": {}}})
        table.update_item(
            Key={"Id": "item-id"},
            UpdateExpression="SET nest1.nest2.event_history = list_append(if_not_exists(nest1.nest2.event_history, :empty_list), :new_value)",
            ExpressionAttributeValues={":empty_list": [], ":new_value": ["some_value"]},
        )
        table.get_item(Key={"Id": "item-id"})["Item"].should.equal(
            {"Id": "item-id", "nest1": {"nest2": {"event_history": ["some_value"]}}}
        )
