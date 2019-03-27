from json import dumps

import pytest

import ghwh.config
from ghwh import __version__
from ghwh import callbacks
from ghwh.api.utils import get_hexdigest


class APITestCase:
    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(cls, request, flask_cli):
        def cb(headers, payload):
            return payload

        callbacks.register("push", cb)
        type(cls).cli = flask_cli
        yield
        callbacks.deregister("push", cb)


class TestAPI(APITestCase):
    def test_get_index(self):
        resp = self.cli.get("")
        payload = resp.get_json()
        assert __version__ in payload["message"]

    def post(self, json, headers=None):
        webhook_secret = b"somesecret"
        ghwh.config.webhook_secret = webhook_secret
        digest = "sha1"
        sig = get_hexdigest(webhook_secret, dumps(json).encode(), digest)
        hdrs = {
            "X-GitHub-Event": "push",
            "X-GitHub-Delivery": "72d3162e-cc78-11e3-81ab-4c9367dc0958",
            "X-Hub-Signature": digest + "=" + sig,
        }
        if headers:
            hdrs.update(headers)
        return self.cli.post("webhook", json=json, headers=hdrs)

    def test_post_webhook(self):
        payload = {"k": 3}
        resp = self.post(payload)
        jd = resp.json
        assert "status" in jd
        assert "Accepted" in jd["status"]

    def test_post_webhook_with_bad_key(self):
        payload = {"k": 3}
        resp = self.post(payload, {"X-Hub-Signature": "sha1=abcd"})
        jd = resp.json
        assert "status" in jd
        assert "Rejected" in jd["status"]

    def test_post_webhook_with_bad_event(self):
        payload = {"k": 3}
        resp = self.post(payload, {"X-GitHub-Event": "pull"})
        jd = resp.json
        assert "status" in jd
        assert "Rejected" in jd["status"]
