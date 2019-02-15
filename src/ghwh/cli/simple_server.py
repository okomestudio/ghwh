from ghwh.callbacks import register
from ghwh.app import start


def handler(payload):
    print(payload)


register("push", handler)


def main():
    start()
