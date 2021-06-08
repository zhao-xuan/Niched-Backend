import logging
from typing import Optional

from pymongo.collection import Collection

from niched.models.schema.users import UserDetailsDB, UserDetails

logger = logging.getLogger(__name__)


def create_user(users: Collection, user_details: UserDetailsDB) -> bool:
    user_dict = user_details.dict()
    try:
        users.insert_one(user_dict)
        logger.info(f"User {user_details.username} created successfully!")
        return True
    except Exception as e:
        logger.error(f"Cannot create user {user_details.username}, exception raised {e}")
        return False


def get_user_login_details(users: Collection, username: str) -> Optional[UserDetailsDB]:
    try:
        user_json = users.find_one({"username": username})
        return UserDetailsDB(**user_json) if user_json else None
    except Exception as e:
        logger.error(f"Exception raised when fetching user {username}: {e}")
        return None


def get_user_details(users: Collection, username: str) -> Optional[UserDetails]:
    user_login_details = get_user_login_details(users, username)
    if user_login_details is None:
        return None
    return UserDetails(**user_login_details.dict(exclude={"password"}))
