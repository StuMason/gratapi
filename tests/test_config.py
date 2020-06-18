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
    def test_all_os_env_variables_present(self):
        config = Config()
        self.assertEqual(config.app_env, "testing")
        self.assertEqual(config.app_name, "bot")
        self.assertEqual(config.app_region, "eu-west-1")
