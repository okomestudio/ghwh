import requests

from ghwh_data import render


headers = {
    "X-GitHub-Event": "push",
    "X-GitHub-Delivery": "72d3162e-cc78-11e3-81ab-4c9367dc0958",
    "X-Hub-Signature": "sha1=7d38cdd689735b008b3c702edd92eea23791c5f6",
}


payload = render('push.json')


def main():
    print(payload)
    resp = requests.post("http://localhost:5000/webhook", json=payload, headers=headers)
    print(resp)
