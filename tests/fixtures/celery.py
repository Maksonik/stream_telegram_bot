import pytest
from celery import Celery


@pytest.fixture
def celery_app():
    app = Celery("test_app")
    app.conf.update(
        broker_url="redis://localhost:6379/0",
        result_backend="redis://localhost:6379/0",
        task_always_eager=True,
    )
    return app
