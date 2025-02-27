import asyncio
from scr.celery.app import app
from scr.celery.atask import AsyncTask


class DummyAsyncTask(AsyncTask):
    async def run(self, x, y):
        await asyncio.sleep(0.01)
        return x * y


dummy_async_task = app.register_task(DummyAsyncTask())


async def test_async_behavior():
    result = dummy_async_task.apply(args=(2, 3))
    assert await result.get() == 6
