from pymongo import MongoClient
from bson.objectid import ObjectId

from app import config

client = MongoClient(config.MONGODB_URI)
db = client[config.DB_NAME]


def get_user_by_id(id: str):
    if not id:
        print("get_user_by_id called without id")
        return
    collection = db["users"]
    return collection.find_one(ObjectId(id))


def get_user_by_email(email: str):
    if not email:
        print("get_user_by_email called without email")
        return
    collection = db["users"]
    return collection.find_one(({"email": email}))


def insert_user(user):
    if not user:
        print("insert_user called without user")
        return
    collection = db["users"]
    print(f"Creating user {user}")
    result = collection.insert_one(user)
    print(f"Insert user with id: {str(result.inserted_id)}")
    return str(result.inserted_id)


def get_servers_by_owner(owner_id: str):
    if not owner_id:
        print("get_servers_by_owner called without owner_id")
        return
    collection = db["servers"]
    return list(collection.find({"owner_id": owner_id}))


def insert_server(server):
    if not server:
        print("insert_server called without server")
        return
    if "owner_id" not in server or not server["owner_id"]:
        print(f"insert_server called with invalid owner_id: {server}")
    if "_id" in server and server["_id"] != None:
        print(f"_id found in server to insert, this is not expected: {server}")
        del server["_id"]
    collection = db["servers"]
    print(f"Creating server {server}")
    result = collection.insert_one(server)
    print(f"Inserted server with id: {str(result.inserted_id)}")
    return str(result.inserted_id)


def delete_server(owner_id: str, server_id: str):
    if not owner_id:
        print("delete_server called without owner_id")
        return
    if not server_id:
        print("delete_server called without server_id")
        return
    collection = db["servers"]
    return collection.delete_one({
        "owner_id": owner_id,
        "_id": ObjectId(server_id)}).deleted_count
