from celery import Celery

from ghwh import init_app
from ghwh.celery import init_celery


class TestCelery:
    def test_init_celery(self):
        app = init_app()
        celery = init_celery(app)
        assert isinstance(celery, Celery)
