from hmac import new as hmac_new

from ghwh.api.utils import signatures_match


class TestUtils:
    def test_signatures_match(self):
        data = b"data"
        digest = "sha1"
        key = b"key"
        signature = hmac_new(key, data, digest).hexdigest()
        assert signatures_match(data, key, digest, signature) is True

    def test_signatures_does_not_match(self):
        data = b"data"
        digest = "sha1"
        key = b"key"
        signature = hmac_new(key, data, digest).hexdigest() + "abcd"
        assert signatures_match(data, key, digest, signature) is False
