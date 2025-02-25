from typing import Any

import asyncio
from celery import Task
from typing import ParamSpecArgs, ParamSpecKwargs


class AsyncTask(Task):
    """Base task class to run children asynchronously in Celery."""

    def __call__(self, *args: ParamSpecArgs, **kwargs: ParamSpecKwargs) -> Any:
        coro = super().__call__(*args, **kwargs)

        if asyncio.iscoroutine(coro):
            return self._run_async(coro)

        return coro

    def _run_async(self, coro):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(coro)
