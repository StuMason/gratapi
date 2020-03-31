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

        if slack_response is None:
            slack_response = SlackRespond()

        slack_event = event_body["event"]

        if "bot_id" not in slack_event:
            text = slack_event["text"]
            response = "I am tickrbot."
            if "hello" in text:
                response = "Hello!"
            if "cycle" in text:
                response = "Returns Cycle Time"
            if "deply" in text:
                response = "Deploy!!!"

            print(response)
            print(slack_event)

            slack_response.send(response, slack_event)

        return Response.handle("", 204)

    except Exception as e:
        msg = f"Unable to process request: {str(e)}"
        logging.exception(msg)
        return Response.handle({"error": msg}, 500)
