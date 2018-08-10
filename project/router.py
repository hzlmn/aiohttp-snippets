import injections


class BaseRouter:
    def __init__(self):
        self.handlers = set()

    def __injected__(self):
        for handler in self.handlers:
            injections.propagate(self, handler)


class Router(BaseRouter):
    users = None
    sms = None

    def setup_sms_handler(self):
        from .handlers import SmsHandler

        handler = SmsHandler()
        self.handlers.add(handler)
        self.sms = handler

        return handler

    def setup_users_handler(self):
        from .handlers import UsersHandler

        handler = UsersHandler()
        self.handlers.add(handler)
        self.users = handler

        return handler
