from flask import Blueprint, request, jsonify, abort

# app libraries
from app import db
from app.security import auth_required
from app.ssh import execute_command
from web.static.models import Server

servers = Blueprint("servers", __name__)


@servers.route("/", methods=['GET'])
@auth_required
def get_servers(user):
    return jsonify(db.get_servers_by_owner(user["_id"]))


@servers.route("/<server_id>", methods=['GET'])
@auth_required
def get_server(user, server_id):
    result = db.get_server_by_id(user["_id"], server_id)
    if result:
        return jsonify(result)
    else:
        abort(404)


@servers.route("/", methods=['POST'])
@auth_required
def create_server(user):
    data = request.get_json()
    data["owner_id"] = user["_id"]
    try:
        result, error = execute_command(
            Server.fromJSON(data), "ls")
        if result:
            server_id = db.insert_server(data)
            data["_id"] = server_id
        else:
            data = {"success": False, "error": error}
        return jsonify(data)
    except Exception as e:
        print(e)
        return abort(400)


@servers.route("/<server_id>", methods=['DELETE'])
@auth_required
def delete_server(user, server_id):
    result = db.delete_server(user["_id"], server_id)
    if result:
        return jsonify({"success": True})
    else:
        abort(404)
