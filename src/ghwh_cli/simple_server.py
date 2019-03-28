from ghwh import init_app
from ghwh import register


def handler(headers, payload):
    print(headers)
    print(payload)


def main():
    register("push", handler)
    app = init_app()
    app.run()
