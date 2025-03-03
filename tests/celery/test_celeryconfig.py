from scr.celery.app import app
from scr.celery.celeryconfig import get_celery_config


def test_get_celery_config(settings):
    config = get_celery_config()

    assert config["broker_url"] == settings.REDIS_URL
    assert config["enable_utc"] is True
    assert "scr.celery.tasks" in config["include"]
    assert "add-every-30-seconds" in config["beat_schedule"]
    assert "healthcheck" in config["beat_schedule"]


def test_celery_app_config(settings):
    assert app.conf.broker_url == settings.REDIS_URL
    assert app.conf.enable_utc is True
    assert "scr.celery.tasks" in app.conf.include
