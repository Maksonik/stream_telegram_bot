import os

from dotenv import load_dotenv


def get_celery_config() -> dict:
    load_dotenv()

    return dict(
        broker_url=os.environ["REDIS_URL"],
        enable_utc=True,
        include=["scr.celery.tasks", "scr.internal.tasks"],
        beat_schedule={
            "add-every-30-seconds": {
                "task": "sync_notify_about_first_youtube_video",
                "schedule": 30.0,
            },
            "healthcheck": {
                "task": "healthcheck",
                "schedule": 5.0,
            },
        },
    )
