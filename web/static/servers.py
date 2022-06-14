from browser import alert, document
from browser.template import Template

import api
from models import Server

servers_tmpl = []
model = {}


def toggle_add_server(ev, el):
    el.data.model["add_server_mode"] = not el.data.model.get(
        "add_server_mode", False)


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
            if "servers" not in model:
                model["servers"] = []
            model["servers"].append(response)
        model["loaded"] = True
        servers_tmpl[0].render(model=model)

    el.data.model["loaded"] = False
    el.data.model["add_server_mode"] = False
    api.create_server(server.toJSON(), add_server_response_handler)


def delete_server(ev, el):
    server_id = ev.target.id

    def delete_server_response_handler(response):
        if "error" in response:
            alert(response["error"])
        else:
            model["servers"] = [server for server in model["servers"]
                                if server["_id"] != server_id]
        model["loaded"] = True
        servers_tmpl[0].render(model=model)

    el.data.model["loaded"] = False
    api.delete_server(server_id, delete_server_response_handler)


def load_servers():
    servers_tmpl.append(Template(
        "servers-stat", [add_server, delete_server,
                         toggle_add_server, change_auth_mode]))

    def servers_response_handler(response):
        if "error" in response:
            alert(response["error"])
        else:
            model["servers"] = response
        model["loaded"] = True
        servers_tmpl[0].render(model=model)

    servers_tmpl[0].render(model=model)
    api.get_servers(servers_response_handler)
