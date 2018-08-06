import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps

import aioelasticsearch
import injections
import trafaret as t
from aiohttp import web

from .handlers import UsersHandler
from .helpers import load_config, run_in_executor
from .middlewares import validation_middleware
from .routes import setup_routes
from .twilio import TwilioGateway

logger = logging.getLogger(__name__)


class AiohttpServer:
    def __init__(self, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()

        self.loop = loop

    def setup(self):
        self.config = load_config("config/settings.json")

        self.executor = ThreadPoolExecutor(max_workers=10)

        self.middlewares = [validation_middleware]

        self.app = web.Application(loop=self.loop, middlewares=self.middlewares)

        self.elastic = aioelasticsearch.Elasticsearch()
        self.twilio_gateway = TwilioGateway(loop=self.loop, **self.config["twilio"])
        self.handler = UsersHandler()

        setup_routes(self.app, self.handler)

        inj = self.setup_injections()
        inj.inject(self.handler)

    def setup_injections(self):
        inj = injections.Container()

        inj["loop"] = self.loop
        inj["executor"] = self.executor
        inj["elastic"] = self.elastic
        inj["twilio_gateway"] = self.twilio_gateway

        inj.interconnect_all()

        return inj

    def start(self):
        web.run_app(self.app, port=9002)

    async def stop(self):
        self.loop.close()
        self.executor.shutdown()
        await self.elastic.close()
