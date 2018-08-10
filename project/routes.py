def setup_routes(app, router):
    if router.users:
        app.router.add_route("GET", "/api/v1/users/search", router.users.search)

    if router.sms:
        app.router.add_route("POST", "/api/v1/users/send_sms", router.sms.send_sms)

