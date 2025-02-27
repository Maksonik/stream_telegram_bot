import asyncio
from celery import Task
from typing import ParamSpecArgs, ParamSpecKwargs


class AsyncTask(Task):
    """Base task class to run children asynchronouosly.

    See https://docs.celeryq.dev/en/stable/userguide/application.html#abstract-tasks
    """

    def __call__(self, *args: ParamSpecArgs, **kwargs: ParamSpecKwargs) -> object:
        coro = super().__call__(*args, **kwargs)
        try:
            return asyncio.run(main=coro)
        except RuntimeError:
            return coro
