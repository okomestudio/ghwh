from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request

from .. import config
from ..tasks.on_commit import on_commit
from .utils import require_secret


app = Flask(__name__.split(".", 1)[0])
app.config.update(
    CELERY_BROKER_URL=config.webhook_celery_broker,
    CELERY_RESULT_BACKEND=config.webhook_celery_backend,
)


@app.route("/")
def index():
    from localshop_webhook import __version__

    return f"Hello, world! This is localshop-webhook {__version__}."


@app.route("/webhook", methods=["POST"])
@require_secret
def post_webhook():
    payload = request.get_json()
    on_commit.delay(payload)
    resp = {"status": "Accepted", "message": "Commit message received"}
    return make_response(jsonify(resp), 202)
