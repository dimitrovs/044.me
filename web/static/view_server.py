from browser import alert, document, window
from browser.template import Template

import api
import header
from models import Server

add_server_tmpl = []
model = {}


def toggle_menu(ev, element):
    ev.target.classList.toggle("is-active")
    document["server-options"].classList.toggle("is-active")


def delete_server(ev, el):
    server_id = el.data.model["server"]._id

    def delete_server_response_handler(response):
        if "error" in response:
            alert(response["error"])
        else:
            window.location.href = "index.html"
        model["loaded"] = True
        add_server_tmpl[0].render(model=model)

    el.data.model["loaded"] = False
    api.delete_server(server_id, delete_server_response_handler)


def load_server(server_id):
    add_server_tmpl.append(Template(
        "server-view", [delete_server, toggle_menu]))

    def servers_response_handler(response):
        if "error" in response:
            alert(response["error"])
        else:
            model["server"] = Server.fromJSON(response)
        model["loaded"] = True
        add_server_tmpl[0].render(model=model)

    add_server_tmpl[0].render(model=model)
    api.get_server(server_id, servers_response_handler)


load_server(document.query["_id"])
