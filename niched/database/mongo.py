import logging

from pymongo import MongoClient

from niched.core.config import DB_CONNECTION_STRING

logger = logging.getLogger(__name__)

client = MongoClient()


def db_connect():
    global client
    logger.info("Initiating connection with database...")
    try:
        client = MongoClient(DB_CONNECTION_STRING)
        logger.info("Established connection with database")
    except Exception as e:
        logger.error("Failed to establish connection with database: ", e)


def db_terminate():
    global client
    client.close()
