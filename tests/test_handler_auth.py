import json
import unittest
from unittest.mock import patch

from handler_auth import handle


def apigw_text_event():
    return {
        "body": '{"event": {"username":"Name", "password":"Password"}}',
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


class TestHandlerAuth(unittest.TestCase):
    @patch("src.auth.Auth.enticate")
    def test_handler_auth_user(self, mock_auth):
        mock_auth.return_value = {"response": "good"}
        ret = handle(apigw_text_event(), "")
        body = json.loads(ret["body"])
        self.assertEqual(ret["statusCode"], "200")
        self.assertEqual(body, {"response": "good"})
        mock_auth.assert_called()

    @patch("logging.exception")
    @patch("urllib.parse.unquote_plus")
    def test_handle_auth_exception(self, mock_urllib, mock_logging):
        mock_urllib.side_effect = Exception("broke")
        ret = handle(apigw_text_event(), "")
        body = json.loads(ret["body"])
        self.assertEqual(ret["statusCode"], "500")
        self.assertEqual(body, {"error": "Unable to process request: broke"})
        mock_urllib.assert_called()
        mock_logging.assert_called()
