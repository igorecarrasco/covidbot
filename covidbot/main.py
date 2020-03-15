"""
Cloud-scheduler HTTP trigger for 50CentBot
"""
from datetime import datetime
from typing import Dict, Optional, Text

from flask import Request, jsonify

from local.covid import Covid
from local.twitter import Twitter

t = Twitter()
c = Covid()


def main(request: Request):
    """
    Responds to an HTTP request.

    Parameters:
    ----------
    request (flask.Request):
        HTTP request object.
    """

    t.post(tweet_rate)

    return jsonify({"sucess": True})


if __name__ == "__main__":
    print(c.world_data)
    main("foo")
