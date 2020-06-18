import os
import unittest
from unittest.mock import patch

from src.config import Config


class TestConfig(unittest.TestCase):
    def test_instantiation(self):
        config = Config()
        self.assertIsNotNone(config)
        self.assertIsNotNone(config.app_env)

    @patch.dict(os.environ, {"APP_ENV": "testing"})
    @patch.dict(os.environ, {"APP_NAME": "bot"})
    @patch.dict(os.environ, {"APP_REGION": "eu-west-1"})
    @patch.dict(os.environ, {"USER_POOL_ID": "123"})
    @patch.dict(os.environ, {"APP_CLIENT_ID": "456"})
    @patch.dict(os.environ, {"APP_CLIENT_SECRET": "789"})
    def test_all_os_env_variables_present(self):
        config = Config()
        self.assertEqual(config.app_env, "testing")
        self.assertEqual(config.app_name, "bot")
        self.assertEqual(config.app_region, "eu-west-1")
        self.assertEqual(config.user_pool_id, "123")
        self.assertEqual(config.app_client_id, "456")
        self.assertEqual(config.app_client_secret, "789")
