from hmac import compare_digest
from hmac import new as hmac_new
from hashlib import sha1


def signatures_match(data, signature, key):
    h = hmac_new(key, data, sha1)
    return compare_digest("sha1=" + h.hexdigest(), signature)
