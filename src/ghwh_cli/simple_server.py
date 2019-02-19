from ghwh import register_callback
from ghwh import start


def handler(payload):
    print(payload)


register_callback("push", handler)


def main():
    start()
