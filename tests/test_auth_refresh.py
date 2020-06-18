import unittest
import uuid

import boto3
from moto import mock_cognitoidp

from src.authenticate.auth_refresh import AuthRefresh


class TestAuthRefresh(unittest.TestCase):
    @mock_cognitoidp
    def test_refreshes_auth(self):
        details = self.create_pool_and_user()

        client = AuthRefresh()
        resp, msg = client.handle(
            details["username"],
            details["token"],
            "secret",
            details["user_pool_id"],
            details["client_id"],
        )

        self.assertIsNotNone(resp["ResponseMetadata"]["HTTPStatusCode"])
        self.assertIsNone(msg)

    def create_pool_and_user(self):
        conn = boto3.client("cognito-idp", "eu-west-1")

        username = str(uuid.uuid4())
        temporary_password = str(uuid.uuid4())
        user_pool_id = conn.create_user_pool(PoolName=str(uuid.uuid4()))["UserPool"][
            "Id"
        ]
        user_attribute_name = str(uuid.uuid4())
        user_attribute_value = str(uuid.uuid4())
        client_id = conn.create_user_pool_client(
            UserPoolId=user_pool_id,
            ClientName=str(uuid.uuid4()),
            ReadAttributes=[user_attribute_name],
        )["UserPoolClient"]["ClientId"]

        conn.admin_create_user(
            UserPoolId=user_pool_id,
            Username=username,
            TemporaryPassword=temporary_password,
            UserAttributes=[
                {"Name": user_attribute_name, "Value": user_attribute_value}
            ],
        )

        result = conn.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=client_id,
            AuthFlow="ADMIN_NO_SRP_AUTH",
            AuthParameters={"USERNAME": username, "PASSWORD": temporary_password},
        )

        new_password = str(uuid.uuid4())

        result = conn.respond_to_auth_challenge(
            Session=result["Session"],
            ClientId=client_id,
            ChallengeName="NEW_PASSWORD_REQUIRED",
            ChallengeResponses={"USERNAME": username, "NEW_PASSWORD": new_password},
        )

        return {
            "username": username,
            "token": result["AuthenticationResult"]["RefreshToken"],
            "user_pool_id": user_pool_id,
            "client_id": client_id,
        }
