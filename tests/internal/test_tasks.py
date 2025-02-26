from scr.internal.tasks import task_healthcheck


def test_add(celery_app):
    result = task_healthcheck.delay()
    assert result.get(timeout=10) == {"status": "ok"}
