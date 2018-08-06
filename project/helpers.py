import asyncio
import json
from functools import partial, wraps
from pathlib import Path


def run_in_executor(loop_="loop", executor_="executor"):
    def factory(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cls = args[0]
            loop = getattr(cls, loop_, asyncio.get_event_loop())
            executor = getattr(cls, executor_, None)
            return await loop.run_in_executor(executor, partial(func, *args, **kwargs))

        return wrapper

    return factory


def load_config(config_path, decoder=json.loads):
    with Path(config_path).open() as fd:
        config = decoder(fd.read())

    return config
