"""
Cloud-scheduler HTTP trigger for COVID-19 Bot
"""
from datetime import datetime
from typing import Dict, Optional, Text

from flask import Request, jsonify

from local.alerts import Alerts

a = Alerts()


def main(request: Request):
    """
    Responds to an HTTP request.

    Parameters:
    ----------
    request (flask.Request):
        HTTP request object.
    """

    a.generate()

    return jsonify({"sucess": True})


if __name__ == "__main__":
    pass
    # main("foo")
