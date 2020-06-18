import os
import unittest
from unittest.mock import patch

from src.auth import Auth


class TestAuth(unittest.TestCase):
    @patch.dict(os.environ, {"USER_POOL_ID": "123"})
    @patch.dict(os.environ, {"APP_CLIENT_ID": "456"})
    @patch.dict(os.environ, {"APP_CLIENT_SECRET": "789"})
    def test_auth_inits(self):
        client = Auth()
        print(client.client_id)
        self.assertEqual(client.user_pool_id, "123")
        self.assertEqual(client.client_id, "456")
        self.assertEqual(client.client_secret, "789")

    @patch.dict(os.environ, {"USER_POOL_ID": "123"})
    @patch.dict(os.environ, {"APP_CLIENT_ID": "456"})
    @patch.dict(os.environ, {"APP_CLIENT_SECRET": "789"})
    def test_get_secret_hash(self):
        client = Auth()
        dec = client.get_secret_hash("username")
        self.assertEqual(dec, "L7HBAEqO7YNtemCVKhp70wmpjcC+n5lEFIw66UZtVDA=")
