import pytest

from ghwh import __version__
from ghwh import callbacks


class APITestCase:
    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(cls, request, flask_cli):
        callbacks.register("push", lambda x: x)
        type(cls).cli = flask_cli
        yield


class TestAPI(APITestCase):
    def test_basic(self):
        resp = self.cli.get("")
        payload = resp.get_json()
        assert __version__ in payload["message"]

    def test_routing(self):
        payload = {"k": 3}
        headers = {
            "X-GitHub-Event": "push",
            "X-GitHub-Delivery": "72d3162e-cc78-11e3-81ab-4c9367dc0958",
            "X-Hub-Signature": "sha1=7d38cdd689735b008b3c702edd92eea23791c5f6",
        }
        resp = self.cli.post("webhook", json=payload, headers=headers)
        # assert 0
