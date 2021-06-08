import logging
from typing import Optional

from pymongo.collection import Collection

from niched.models.schema.users import UserDetails, UserDetailsUpdate

logger = logging.getLogger(__name__)


def check_user_id_exist(users_collection: Collection, user_name: str) -> bool:
    return users_collection.count_documents({"user_name": user_name}) > 0


def get_user_profile(users_coll: Collection, user_name: str) -> UserDetails:
    user_db_json = users_coll.find_one({"user_name": user_name})
    del user_db_json["password"]

    return UserDetails(**user_db_json)


def update_user_profile(users_coll: Collection, user_name: str, new_details: UserDetailsUpdate) -> Optional[UserDetails]:
    user_query = {"user_name": user_name}
    new_values = new_details.dict(exclude_none=True)
    new_values_query = {"$set": new_values}

    result = users_coll.update_one(user_query, new_values_query)
    if not result.acknowledged:
        logger.error(f"Failed to update user [{user_name}] with new fields [{new_values}]")
        return None

    new_user_details_json = users_coll.find_one(user_query)
    del new_user_details_json["password"]

    return UserDetails(**new_user_details_json)