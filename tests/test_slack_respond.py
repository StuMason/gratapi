import os
import unittest
from unittest.mock import patch

from src.slack_respond import SlackRespond


class TestSlackRespond(unittest.TestCase):
    @patch.dict(os.environ, {"BOT_OAUTH_TOKEN": "bar"})
    @patch("urllib.parse.urlencode")
    @patch("urllib.request")
    def test_slack_send(self, mock_urlib_request, mock_urlencode):
        client = SlackRespond()
        response = "text response"
        event = {"channel": "foo"}
        client.send(response, event)
        mock_urlencode.assert_called_once_with(
            (("token", "bar"), ("channel", "foo"), ("text", response))
        )
