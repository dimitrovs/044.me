import config
from pymongo import MongoClient
from bson.objectid import ObjectId

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
