import json
import logging
import urllib

from src.gratitude.search_gratitude import SearchGratitude
from src.response import Response


def handle(event, context):
    try:
        event_body = urllib.parse.unquote_plus(event["body"])
        event_body = json.loads(event_body)

        gratitudes = SearchGratitude()
        create = gratitudes.search(event["requestContext"]["search"],)

        return Response.handle(create, 200)

    except Exception as e:
        msg = f"Unable to process request: {str(e)}"
        logging.exception(msg)
        return Response.handle({"error": msg}, 500)
