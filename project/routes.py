def setup_routes(app, handler):
    app.router.add_route("GET", "/api/v1/users/search", handler.search)
    app.router.add_route("POST", "/api/v1/users/send_sms", handler.send_sms)

