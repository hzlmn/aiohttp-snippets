import aioelasticsearch
import injections
from aiohttp import web

from .trafarets import UsersOutputTrafaret
from .twilio import TwilioGateway


@injections.has
class UsersHandler:
    elastic = injections.depends(aioelasticsearch.Elasticsearch)

    index = "users"
    doc_type = "document"

    async def search(self, request):
        q = request.query.get("query")

        query = {"query": {"match_all": {}}}

        if q is not None:
            query = {"query": {"match": {"name": q}}}

        resp = await self.elastic.search(
            index=self.index, doc_type=self.doc_type, body=query
        )

        if not resp:
            raise web.HTTPNotFound

        users = [doc["_source"] for doc in resp["hits"]["hits"]]

        return web.json_response({"users": UsersOutputTrafaret(users)})


@injections.has
class SmsHandler:
    twilio_gateway = injections.depends(TwilioGateway)

    async def send_sms(self, request):
        await self.twilio_gateway.send_sms("test message")
        return web.json_response({"status": "ok"})
