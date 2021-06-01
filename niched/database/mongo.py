import logging

from pymongo import MongoClient

from niched.core.config import DB_CONNECTION_STRING, DB_DATABASE

logger = logging.getLogger(__name__)


class MongoConnection:

    client = MongoClient(DB_CONNECTION_STRING)
    db = client[DB_DATABASE]

    @staticmethod
    def get_users_collection():
        return MongoConnection.db["users"]


conn = MongoConnection()
