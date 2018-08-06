import logging

from aiohttp import web

from trafaret import DataError

logger = logging.getLogger(__name__)


@web.middleware
async def validation_middleware(request, handler):
    try:
        return await handler(request)
    except DataError as exc:
        logger.error(exc, exc_info=exc)
        raise web.HTTPBadRequest(reason=str(exc))
