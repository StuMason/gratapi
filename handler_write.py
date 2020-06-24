import json
import logging
import urllib
from datetime import datetime

from src.gratitude.create_gratitude import CreateGratitude
from src.response import Response


def handle(event, context):
    try:
        event_body = urllib.parse.unquote_plus(event["body"])
        event_body = json.loads(event_body)

        gratitudes = CreateGratitude()
        create = gratitudes.create(
            event["requestContext"]["authorizer"]["claims"]["email"],
            datetime.fromtimestamp(event["requestContext"]["requestTimeEpoch"]),
            event_body[0],
        )

        return Response.handle(create, 200)

    except Exception as e:
        msg = f"Unable to process request: {str(e)}"
        logging.exception(msg)
        return Response.handle({"error": msg}, 500)
