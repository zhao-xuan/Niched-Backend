import logging
from typing import Optional

from pymongo import MongoClient

from niched.models.schema.users import UserDetailsDB

logger = logging.getLogger(__name__)


def create_user(client: MongoClient, user_details: UserDetailsDB) -> bool:
    user_dict = user_details.dict()
    client["users"].insert_one(user_dict)
    try:
        logger.info(f"User {user_details.username} created successfully!")
        return True
    except Exception as e:
        logger.error(f"Cannot create user with details {user_details.json()}, exception raised {e}")
        return False


def get_user(client: MongoClient, username: str) -> Optional[UserDetailsDB]:
    try:
        users_coll = client["users"]
        user_json = users_coll.find_one({"username": username})
        return UserDetailsDB(**user_json) if user_json else None
    except Exception as e:
        logger.error(f"Exception raised when fetching user {username}: {e}")
        return None
