from unittest import mock
import pytest

from ghwh import callbacks
from ghwh.callbacks import deregister
from ghwh.callbacks import NoCallbackError
from ghwh.callbacks import register
from ghwh.callbacks import run


def cb():
    return


class TestCallbacks:
    @pytest.fixture(autouse=True)
    def setup(self):
        yield
        for k in list(callbacks._callbacks.keys()):
            del callbacks._callbacks[k]

    def test_register(self):
        register("push", cb)
        assert "push" in callbacks._callbacks
        assert callbacks._callbacks["push"] is cb

    def test_deregister(self):
        register("push", cb)
        assert "push" in callbacks._callbacks
        assert callbacks._callbacks["push"] is cb
        deregister("push", cb)
        assert "push" not in callbacks._callbacks

    def test_run(self):
        cb = mock.Mock()
        register("push", cb)
        headers = {"a": 1}
        payload = {"b": 2}
        run("push", headers, payload)
        cb.assert_called_with(headers, payload)

    def test_run_for_nonexisting_event(self):
        with pytest.raises(NoCallbackError):
            run("pull", {}, {})
