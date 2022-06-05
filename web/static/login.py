from browser import alert, document, window
from browser.template import Template
from browser.session_storage import storage

import api


def response_handler(req):
    if "error" in req.json:
        alert(req.json["error"])
    else:
        storage["jwt"] = req.json.get("jwt")
        window.location.href = "index.html"


def login(ev, element):
    ev.preventDefault()
    email = document["email"].value
    password = document["password"].value
    api.login(email, password, response_handler)


# Delete previous session on load
if storage.get("jwt"):
    del storage["jwt"]

# Render page
Template("login", [login]).render()
