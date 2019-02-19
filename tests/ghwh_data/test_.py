from ghwh_data import load
from ghwh_data import render


class TestRender:
    def test_load(self):
        loaded = load("push.json")
        assert isinstance(loaded, dict)
        assert "ref" in loaded

    def test_render(self):
        rendered = render("push.json")
        assert isinstance(rendered, str)
