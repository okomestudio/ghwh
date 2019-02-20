from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request

from .. import __version__
from .. import callbacks
from .. import config
from .utils import signatures_match


webhook = Blueprint("webhook", __name__.split(".", 1)[0])


def _resp(payload, status_code=200):
    return make_response(jsonify(payload), status_code)


@webhook.route("/", methods=["GET"])
def index():
    return _resp({"message": f"ghwh v{__version__}"})


@webhook.route("/webhook", methods=["POST"])
def post_webhook():
    payload = request.get_json()
    headers = request.headers
    event = headers["X-GitHub-Event"]
    guid = headers["X-GitHub-Delivery"]

    secret = headers.get("X-Hub-Signature")
    if config.webhook_secret:
        if not signatures_match(request.data, secret, config.web_secret):
            raise Exception("Signature mismatch")

    try:
        callbacks.run(event, headers, payload)
    except callbacks.NoCallbackError:
        raise
    return _resp(
        {"status": "Accepted", "message": "Commit message received", "guid": guid}, 202
    )
