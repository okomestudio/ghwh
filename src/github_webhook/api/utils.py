import hashlib
import hmac
from functools import wraps

from flask import request
from flask import Response

from .. import config


def require_secret(f):
    fail_response = Response("Secret mismatch", 400)

    def signatures_match(request, key):
        h = hmac.new(key, request.data, hashlib.sha1)
        return hmac.compare_digest(
            "sha1=" + h.hexdigest(), str(request.headers["X-Hub-Signature"])
        )

    @wraps(f)
    def wrapper(*args, **kwargs):
        if config.webhook_secret:
            if "X-Hub-Signature" not in request.headers or not signatures_match(
                request, config.webhook_secret
            ):
                return fail_response
        else:
            if "X-Hub-Signature" in request.headers:
                return fail_response
        return f(*args, **kwargs)

    return wrapper
