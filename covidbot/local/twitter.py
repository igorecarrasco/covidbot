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

    def post(self, text: str, media_ids: list = []):
        if not media_ids:
            self.twitter.update_status(status=text)
        else:
            self.twitter.update_status(status=text, media_ids=media_ids)

    def upload_image(self, path) -> str:
        """
        Uploads image to Twitter. Returns its media id
        """
        with open(path, "rb") as f:
            img = b64encode(f.read())
            i = 0
            while i < 10:
                try:
                    upload: dict = self.twitter.upload_media(
                        media=img, media_type="image/png"
                    )
                    media_id: str = upload.get("media_id_string", "")
                except TwythonError as e:
                    print(str(e))
                    time.sleep(2)
                    continue
                else:
                    return media_id
            else:
                raise ValueError("Couldn't upload media.")
