from browser import alert, document
from browser.template import Template

import api

servers_tmpl = []
model = {}


def toggle_add_server(ev, el):
    el.data.model["add_server_mode"] = not el.data.model.get(
        "add_server_mode", False)


def change_auth_mode(ev, el):
    el.data.model["auth_method"] = ev.target.value


def add_server(ev, el):
    auth_method = el.data.model.get("auth_method", "password")
    data = {"username": document["add_server_username"].value,
            "host": document["add_server_host"].value,
            "port": document["add_server_port"].value,
            "auth_method": auth_method,
            "password": document["add_server_password"].value,
            "ssh_key": document["add_server_key"].value
            }

    def add_server_response_handler(response):
        if "error" in response:
            alert(response["error"])
        if "servers" not in model:
            model["servers"] = []
        print(response)
        model["servers"].append(response)
        model["loaded"] = True
        servers_tmpl[0].render(model=model)

    el.data.model["loaded"] = False
    el.data.model["add_server_mode"] = False
    api.create_server(data, add_server_response_handler)


def load_servers():
    servers_tmpl.append(Template(
        "servers-stat", [add_server, toggle_add_server, change_auth_mode]))

    def servers_response_handler(response):
        if "error" in response:
            alert(response["error"])
        model["loaded"] = True
        servers_tmpl[0].render(model=model)

    servers_tmpl[0].render(model=model)
    api.get_servers(servers_response_handler)
