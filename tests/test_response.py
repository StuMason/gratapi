import unittest

from src.response import Response


class TestResponse(unittest.TestCase):
    def test_response(self):
        results = Response.handle("Foo", 200)
        self.assertDictEqual(
            {
                "statusCode": "200",
                "body": '"Foo"',
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
            },
            results,
        )
