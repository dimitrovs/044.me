import json
from browser import ajax, window
from browser.session_storage import storage

API = "/api"


def make_request(url, method, data, response_handler):
    def auth_handler(req):
        if req.status == 401:
            window.location.href = "login.html"
        elif req.status == 200:
            response_handler(req.json)
        else:
            response_handler({"error": req.status})

    if method == "GET":
        ajax.get(url, mode="json",
                 headers={"Content-Type": "application/json",
                          "Authorization": f"Bearer {storage['jwt']}"},
                 oncomplete=auth_handler)
    elif method == "POST":
        ajax.post(url, mode="json",
                  headers={"Content-Type": "application/json",
                           "Authorization": f"Bearer {storage['jwt']}"},
                  data=json.dumps(data),
                  oncomplete=auth_handler)
    else:
        print(f"Unsupported request method: {method}")


def login(email, password, response_handler):
    ajax.post(f"{API}/user/", mode="json",
              headers={"Content-Type": "application/json"},
              data=json.dumps({"email": email, "password": password}),
              oncomplete=response_handler)


def get_user(response_handler):
    make_request(f"{API}/user/", "GET", None, response_handler)


def get_servers(response_handler):
    make_request(f"{API}/servers/", "GET", None, response_handler)


def create_server(data, response_handler):
    make_request(f"{API}/servers/", "POST", data, response_handler)
