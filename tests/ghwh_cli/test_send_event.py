from unittest import mock

from argparse import ArgumentParser

from ghwh_cli.send_event import argparser
from ghwh_cli.send_event import get_headers
from ghwh_cli.send_event import load
from ghwh_cli.send_event import main


class TestSendEvent:
    def test_clargs(self):
        parser = argparser()
        assert isinstance(parser, ArgumentParser)

    def test_get_headers(self):
        headers = get_headers("push")
        assert headers["X-GitHub-Event"] == "push"

    def test_main(self, capsys):
        json = load("push.json")
        headers = get_headers("push")
        return_value = "returned"

        with mock.patch("ghwh_cli.send_event.post") as post:
            post.return_value = return_value
            main("push".split())
            post.assert_called_with(
                "http://localhost:5000/webhook", json=json, headers=headers
            )

        captured = capsys.readouterr()
        assert return_value + "\n" == captured.out
