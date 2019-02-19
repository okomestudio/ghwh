from argparse import ArgumentParser

import requests

from ghwh_data import load


def get_headers(event):
    headers = {
        "X-GitHub-Event": event,
        "X-GitHub-Delivery": "72d3162e-cc78-11e3-81ab-4c9367dc0958",
        "X-Hub-Signature": "sha1=7d38cdd689735b008b3c702edd92eea23791c5f6",
    }
    return headers


def clargs():
    p = ArgumentParser()
    p.add_argument("-e", "--event", choices=("push",))
    p.add_argument("--endpoint", default="http://localhost:5000/webhook")
    return p.parse_args()


def main():
    args = clargs()
    event = args.event
    endpoint = args.endpoint
    headers = get_headers(event)
    payload = load(event + ".json")
    resp = requests.post(endpoint, json=payload, headers=headers)
    print(resp)
