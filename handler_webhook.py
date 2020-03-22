import json
import logging
import urllib

from src.response import Response
from src.slack_respond import SlackRespond

slack_response = None


def handle(event, context):
    global slack_response
    try:
        event_body = urllib.parse.unquote_plus(event["body"])
        event_body = json.loads(event_body)

        if "challenge" in event_body:
            return Response.handle(event_body["challenge"], 200)

        slack_event = event_body["event"]

        if "bot_id" in slack_event:
            print("Ignore integration bot message")
        else:
            text = slack_event["text"]
            response = "Tickr bot says: " + text

            if slack_response is None:
                slack_response = SlackRespond()

            slack_response.send(response, slack_event)

        return Response.handle("ok", 200)

    except Exception as e:
        msg = f"Unable to process request: {str(e)}"
        logging.exception(msg)
        return Response.handle({"error": msg}, 500)
