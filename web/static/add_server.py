from browser import alert, document, window
from browser.template import Template

import api
import header
from models import Server

servers_tmpl = []
model = {"loaded": True}


def change_auth_mode(ev, el):
    el.data.model["auth_method"] = ev.target.value


def add_server(ev, el):
    auth_method = el.data.model.get("auth_method", "password")
    server = Server(document["add_server_username"].value,
                    document["add_server_host"].value,
                    document["add_server_port"].value,
                    auth_method, document["add_server_password"].value,
                    document["add_server_key"].value)

    def add_server_response_handler(response):
        if "error" in response:
            alert(response["error"])
        else:
            window.location.href = "index.html"

    el.data.model["loaded"] = False
    servers_tmpl[0].render(model=model)
    api.create_server(server.toJSON(), add_server_response_handler)


servers_tmpl.append(Template(
    "add-server-form", [add_server,
                        change_auth_mode]))
servers_tmpl[0].render(model=model)
