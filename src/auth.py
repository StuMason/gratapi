import base64
import hashlib
import hmac
import logging

import boto3

from src.config import Config


class Auth:
    def __init__(self):
        config = Config()
        self.USER_POOL_ID = config.user_pool_id
        self.CLIENT_ID = config.app_client_id
        self.CLIENT_SECRET = config.app_client_secret
        self.cognito_client = boto3.client("cognito-idp")

    def get_secret_hash(self, username):
        msg = username + self.CLIENT_ID
        digest = hmac.new(
            str(self.CLIENT_SECRET).encode("utf-8"),
            msg=str(msg).encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()
        dec = base64.b64encode(digest).decode()
        return dec

    def initiate_auth(self, username, password):
        try:
            resp = self.cognito_client.admin_initiate_auth(
                UserPoolId=self.USER_POOL_ID,
                ClientId=self.CLIENT_ID,
                AuthFlow="ADMIN_NO_SRP_AUTH",
                AuthParameters={
                    "USERNAME": username,
                    "SECRET_HASH": self.get_secret_hash(username),
                    "PASSWORD": password,
                },
                ClientMetadata={"username": username, "password": password},
            )
        except self.cognito_client.exceptions.NotAuthorizedException as e:
            logging.exception(e)
            return None, "The username or password is incorrect"
        except self.cognito_client.exceptions.UserNotFoundException as e:
            logging.exception(e)
            return None, "The username or password is incorrect"
        except Exception as e:
            logging.exception(e)
            return None, "Unknown error"
        return resp, None

    def refresh_auth(self, username, refresh_token):
        try:
            resp = self.cognito_client.admin_initiate_auth(
                UserPoolId=self.USER_POOL_ID,
                ClientId=self.CLIENT_ID,
                AuthFlow="REFRESH_TOKEN_AUTH",
                AuthParameters={
                    "REFRESH_TOKEN": refresh_token,
                    "SECRET_HASH": self.get_secret_hash(username),
                },
                ClientMetadata={},
            )
        except self.cognito_client.exceptions.NotAuthorizedException as e:
            logging.exception(e)
            return None, "The username or password is incorrect"
        except self.cognito_client.exceptions.UserNotFoundException as e:
            logging.exception(e)
            return None, "The username or password is incorrect"
        except Exception as e:
            logging.exception(e)
            return None, "Unknown error"
        return resp, None

    def enticate(self, event_body):

        username = event_body["username"]
        if "password" in event_body:
            resp, msg = self.initiate_auth(username, event_body["password"])

        if "refresh_token" in event_body:
            resp, msg = self.refresh_auth(username, event_body["refresh_token"])
        if msg is not None:
            return {"status": "fail", "msg": msg}

        response = {
            "status": "success",
            "id_token": resp["AuthenticationResult"]["IdToken"],
        }

        if "password" in event_body:
            response["refresh_token"] = resp["AuthenticationResult"]["RefreshToken"]

        return response
