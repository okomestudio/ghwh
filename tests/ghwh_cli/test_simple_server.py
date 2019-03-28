from unittest import mock

from ghwh_cli.simple_server import handler
from ghwh_cli.simple_server import main


class TestSimpleServer:
    def test_handler(self, capsys):
        headers = '{"headers": 1}'
        payload = '{"payload": 2}'
        handler(headers, payload)
        captured = capsys.readouterr()
        assert headers in captured.out
        assert payload in captured.out

    def test_main(self):
        with mock.patch("ghwh_cli.simple_server.app") as app:
            main()
            app.run.assert_called()
