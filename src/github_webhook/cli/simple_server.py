from github_webhook.callbacks import register
from github_webhook.app import start


def handler(payload):
    print(payload)


register("push", handler)


def main():
    start()
