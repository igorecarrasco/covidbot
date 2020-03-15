"""
Interactions with Twitter API
"""
import os
import time
from base64 import b64encode

from twython import Twython, TwythonError


class Twitter:
    def __init__(self):
        self.twitter: Twython = Twython(
            os.getenv("TWITTER_API_KEY"),
            os.getenv("TWITTER_API_SECRET_KEY"),
            os.getenv("TWITTER_ACCESS_TOKEN"),
            os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
        )

    def post(self, text: str):
        self.twitter.update_status(status=text)

