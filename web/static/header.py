from browser import document, window
from browser.template import Template
from browser.session_storage import storage


def is_logged_in():
    if storage.get("jwt"):
        return True
    else:
        return False


def toggle_menu(ev, element):
    ev.target.classList.toggle("is-active")
    document["navMenu"].classList.toggle("is-active")


if not is_logged_in():
    window.location.href = "login.html"
else:
    Template("header", [toggle_menu]).render()
