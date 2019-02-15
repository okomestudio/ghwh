from flask import Flask
from flask.testing import FlaskClient

import pytest

from github_webhook.api.webhook import webhook


@pytest.fixture(scope="session")
def flask_cli():
    app = Flask(__name__.split(".", 1)[0])
    app.url_map.strict_slashes = False
    app.register_blueprint(webhook)
    app.testing = True
    app.test_client_class = FlaskClient
    return app.test_client()
