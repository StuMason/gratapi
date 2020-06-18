import base64
import hashlib
import hmac

from src.authenticate.auth_initiate import AuthInitiate
from src.authenticate.auth_refresh import AuthRefresh
from src.config import Config


class Auth:
    def __init__(self):
        self.config = Config()

    def get_secret_hash(self, username):
        msg = username + self.config.app_client_id
        digest = hmac.new(
            str(self.config.app_client_secret).encode("utf-8"),
            msg=str(msg).encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()
        dec = base64.b64encode(digest).decode()
        return dec

    def initiate_auth(self, username, password):
        initiate = AuthInitiate()
        return initiate.handle(
            username,
            password,
            self.get_secret_hash(username),
            self.config.user_pool_id,
            self.config.app_client_id,
        )

    def refresh_auth(self, username, refresh_token):
        refresh = AuthRefresh()
        return refresh.handle(
            username,
            refresh_token,
            self.get_secret_hash(username),
            self.config.user_pool_id,
            self.config.app_client_id,
        )

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
