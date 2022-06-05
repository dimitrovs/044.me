from flask import Blueprint, request

# app libraries
from security import auth_required

servers = Blueprint("servers", __name__)


@servers.route("/", methods=['GET'])
@auth_required
def get_servers(user):
    return {}


@servers.route("/", methods=['POST'])
@auth_required
def create_server(user):
    data = request.get_json()
    data["owner_id"] = user["_id"]

    return data