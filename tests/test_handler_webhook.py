import json
import unittest
from unittest.mock import patch

from handler_webhook import handle


def apigw_challenge_event():
    return {
        "body": '{"challenge":"foo"}',
    }


def apigw_bot_event():
    return {
        "body": json.dumps(
            {"event": {"text": "Hello", "channel": "platform", "bot_id": "123"}}
        ),
    }


def apigw_text_event():
    return {
        "body": '{"event": {"text":"Hello", "channel":"platform"}}',
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "identity": {"apiKey": "", "sourceIp": "127.0.0.1", "accountId": ""},
            "stage": "prod",
        },
        "queryStringParameters": {"foo": "bar"},
        "pathParameters": {"proxy": "/examplepath"},
        "httpMethod": "POST",
        "stageVariables": {"baz": "qux"},
        "path": "/examplepath",
    }


class TestHandlerWebhook(unittest.TestCase):
    def test_handler_webhook_challenge(self):
        ret = handle(apigw_challenge_event(), "")
        body = json.loads(ret["body"])
        self.assertEqual(ret["statusCode"], "200")
        self.assertEqual(body, "foo")

    def test_ignores_bot_message(self):
        ret = handle(apigw_bot_event(), "")
        body = json.loads(ret["body"])
        self.assertEqual(ret["statusCode"], "204")
        self.assertEqual(body, "")

    @patch("src.slack_respond.SlackRespond.send")
    def test_handler_webhook_text(self, mock_send):
        event = {"text": "Hello", "channel": "platform"}
        text_response = "Tickr bot says: Hello"
        ret = handle(apigw_text_event(), "")
        body = json.loads(ret["body"])
        self.assertEqual(ret["statusCode"], "204")
        self.assertEqual(body, "")
        mock_send.assert_called_with(text_response, event)

    @patch("logging.exception")
    @patch("src.slack_respond.SlackRespond.send")
    def test_handle_webhook_exception(self, mock_send, mock_logging):
        mock_send.side_effect = Exception("broke")
        ret = handle(apigw_text_event(), "")
        body = json.loads(ret["body"])
        self.assertEqual(ret["statusCode"], "500")
        self.assertEqual(body, {"error": "Unable to process request: broke"})
        mock_send.assert_called()
        mock_logging.assert_called()
