import logging

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from niched.core.config import DB_CONNECTION_STRING, DB_DATABASE

logger = logging.getLogger(__name__)


class MongoConnection:
    try:
        logger.info("Initiating connection to mongoDB")
        client = MongoClient(DB_CONNECTION_STRING)
        logger.info(f"Connected to cluster, now attempting to access database {DB_DATABASE}")
        db = client[DB_DATABASE]
        logger.info(f"Connected to {DB_DATABASE} successfully!")

        # Tests to see if connection is alive
        client.admin.command("ismaster")
    except ConnectionFailure:
        logger.error("Failed to establish connection with database")

    @staticmethod
    def get_users_collection():
        return MongoConnection.db["users"]

    @staticmethod
    def get_groups_collection():
        return MongoConnection.db["groups"]

    @staticmethod
    def get_threads_collection():
        return MongoConnection.db["threads"]

    @staticmethod
    def get_events_collection():
        return MongoConnection.db["events"]

    @staticmethod
    def get_comments_collection():
        return MongoConnection.db["comments"]

conn = MongoConnection()
