import urllib

from .config import Config


class SlackRespond:
    def __init__(self):
        self.config = Config()

    def send(self, response, slack_event):
        channel_id = slack_event["channel"]
        data = urllib.parse.urlencode(
            (
                ("token", self.config.bot_token),
                ("channel", channel_id),
                ("text", response),
            )
        )
        data = data.encode("ascii")
        request = urllib.request.Request(
            "https://slack.com/api/chat.postMessage", data=data, method="POST"
        )
        request.add_header("Content-Type", "application/x-www-form-urlencoded")
        urllib.request.urlopen(request).read()
