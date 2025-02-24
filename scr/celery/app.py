import logging

from celery import Celery

from scr.celery.celeryconfig import get_celery_config

app = Celery("tasks")
app.config_from_object(get_celery_config())


if __name__ == "__main__":
    logging.log(level=logging.INFO, msg="Start application")
    app.start()
