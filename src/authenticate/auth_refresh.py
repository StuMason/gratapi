import logging

import boto3


class AuthRefresh:
    def __init__(self):
        self.cognito_client = boto3.client("cognito-idp")

    def handle(self, username, refresh_token, secret, user_pool_id, client_id):
        try:
            resp = self.cognito_client.admin_initiate_auth(
                UserPoolId=user_pool_id,
                ClientId=client_id,
                AuthFlow="REFRESH_TOKEN_AUTH",
                AuthParameters={"REFRESH_TOKEN": refresh_token, "SECRET_HASH": secret},
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
