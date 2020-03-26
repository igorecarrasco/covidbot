"""
Cloud-scheduler HTTP trigger for COVID-19 Bot
"""
from datetime import datetime
from typing import Dict, Optional, Text

from flask import Request, jsonify

from local.alerts import Alerts


def main(request: Request):
    """
    Responds to an HTTP request.

    Parameters:
    ----------
    request (flask.Request):
        HTTP request object.
    """
    a = Alerts()
    a.generate()

    return jsonify({"sucess": True})
