from scr.internal.tasks import task_healthcheck


def test_add(celery_app):
    result = task_healthcheck.delay()  # Запускаем задачу
    assert result.get(timeout=10) == {"status": "ok"}
