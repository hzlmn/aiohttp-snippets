import asyncio
from project.server import AiohttpServer

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    server = AiohttpServer(loop=loop)
    server.setup()
    try:
        server.start()
    except KeyboardInterrupt:
        loop.run_until_complete(server.stop())
