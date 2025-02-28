from typing import Literal, TypedDict

import celery


class HealchcheckDict(TypedDict):
    status: Literal["ok"]


@celery.shared_task(name="healthcheck")
def task_healthcheck() -> HealchcheckDict:
    """Healthcheck for the Celery service."""
    return {"status": "ok"}
