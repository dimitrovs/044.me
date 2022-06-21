from browser import alert
from browser.template import Template

import api

servers_tmpl = []
model = {}


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
        "servers-stat", [delete_server]))

    def servers_response_handler(response):
        if "error" in response:
            alert(response["error"])
        else:
            model["servers"] = response
        model["loaded"] = True
        servers_tmpl[0].render(model=model)

    servers_tmpl[0].render(model=model)
    api.get_servers(servers_response_handler)
