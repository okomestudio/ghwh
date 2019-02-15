from flask import Flask

from . import config
from .api.webhook import webhook


app = Flask(__name__.split(".", 1)[0])
app.register_blueprint(webhook)
app.config.update(
    CELERY_BROKER_URL=config.celery_broker,
    CELERY_RESULT_BACKEND=config.celery_backend,
)


def start():
    app.run()