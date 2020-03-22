import unittest
from unittest.mock import patch

from src.slack_respond import SlackRespond


class TestSlackRespond(unittest.TestCase):
    @patch("urllib.parse")
    @patch("urllib.request")
    def test_slack_send(self, mock_urlib_parse, mock_urlib_request):
        client = SlackRespond()
        response = "text response"
        event = {"channel": "foo"}
        client.send(response, event)
