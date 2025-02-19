import os

from dotenv import load_dotenv


def get_celery_config() -> dict:
    load_dotenv()
    return dict(
        broker_url=os.environ["REDIS_URL"],
        enable_utc=True,
        include=["scr.celery.tasks"],
        beat_schedule={
            "add-every-5-seconds": {
                "task": "scr.celery.tasks.add",
                "schedule": 2.0,
                "args": (16, 16),
            },
            "add-every-1-minute": {
                "task": "scr.celery.tasks.check_youtube_channel",
                "schedule": 60.0,
            },
        },
    )
