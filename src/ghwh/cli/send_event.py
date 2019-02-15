import requests


headers = {
    "X-GitHub-Event": "push",
    "X-GitHub-Delivery": "72d3162e-cc78-11e3-81ab-4c9367dc0958",
    "X-Hub-Signature": "sha1=7d38cdd689735b008b3c702edd92eea23791c5f6",
}


payload = load_payload("push")


def main():
    resp = requests.post("http://localhost:5000/webhook", json=payload, headers=headers)
    print(resp)
