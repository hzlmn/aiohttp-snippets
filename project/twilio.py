from concurrent.futures import ThreadPoolExecutor

import injections
from twilio.rest import Client

from .helpers import run_in_executor


@injections.has
class TwilioGateway:
    executor = injections.depends(ThreadPoolExecutor)

    def __init__(self, loop, account_id, auth_token):
        self.loop = loop
        self.account_id = account_id
        self.auth_token = auth_token
        self.client = Client(self.account_id, self.auth_token)

    @run_in_executor()
    def _send_sms(self, message, callback=None):
        self.client.messages.create(
            body=message,
            from_="+12248367880",
            status_callback=callback,
            to="+380974219029",
        )

    async def send_sms(self, message, callback=None):
        return await self._send_sms(message, callback)
