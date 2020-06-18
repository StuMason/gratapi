import os
import unittest
from unittest.mock import patch

from src.authenticate.auth import Auth


class TestAuth(unittest.TestCase):
    @patch.dict(os.environ, {"USER_POOL_ID": "123"})
    @patch.dict(os.environ, {"APP_CLIENT_ID": "456"})
    @patch.dict(os.environ, {"APP_CLIENT_SECRET": "789"})
    def test_auth_inits(self):
        client = Auth()
        self.assertEqual(client.config.user_pool_id, "123")
        self.assertEqual(client.config.app_client_id, "456")
        self.assertEqual(client.config.app_client_secret, "789")

    @patch.dict(os.environ, {"APP_CLIENT_ID": "456"})
    @patch.dict(os.environ, {"APP_CLIENT_SECRET": "789"})
    def test_get_secret_hash(self):
        client = Auth()
        dec = client.get_secret_hash("username")
        self.assertEqual(dec, "L7HBAEqO7YNtemCVKhp70wmpjcC+n5lEFIw66UZtVDA=")

    @patch("src.authenticate.auth.Auth.initiate_auth")
    def test_authenticate_password(self, mock_auth):
        mock_auth.return_value = (
            {"AuthenticationResult": {"IdToken": "123", "RefreshToken": "456"}},
            None,
        )
        auth = Auth()
        response = auth.enticate({"username": "test", "password": "password"})
        self.assertEqual(
            response, {"status": "success", "id_token": "123", "refresh_token": "456"}
        )
        mock_auth.assert_called_with("test", "password")

    @patch("src.authenticate.auth.Auth.refresh_auth")
    def test_authenticate_refresh(self, mock_auth):
        mock_auth.return_value = {"AuthenticationResult": {"IdToken": "123"}}, None
        auth = Auth()
        response = auth.enticate({"username": "test", "refresh_token": "token"})
        self.assertEqual(response, {"status": "success", "id_token": "123"})
        mock_auth.assert_called_with("test", "token")

    @patch("src.authenticate.auth.Auth.refresh_auth")
    def test_authenticate_refresh_fail(self, mock_auth):
        mock_auth.return_value = (
            {"AuthenticationResult": {"IdToken": "123"}},
            "failed to auth",
        )
        auth = Auth()
        response = auth.enticate({"username": "test", "refresh_token": "token"})
        self.assertEqual(response, {"status": "fail", "msg": "failed to auth"})
        mock_auth.assert_called_with("test", "token")
