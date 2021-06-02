import logging
from typing import Optional

from pymongo.collection import Collection

from niched.models.schema.groups import GroupDetailsDB

logger = logging.getLogger(__name__)


def create_group(groups: Collection, group_details: GroupDetailsDB) -> bool:
    group_dict = group_details.dict()
    try:
        groups.insert_one(group_dict)
        logger.info(f"User {group_details.name} created successfully!")
        return True
    except Exception as e:
        logger.error(f"Cannot create user {group_details.name}, exception raised {e}")
        return False


def get_group(groups: Collection, name: str) -> Optional[GroupDetailsDB]:
    try:
        group_json = groups.find_one({"name": name})
        return GroupDetailsDB(**group_json) if group_json else None
    except Exception as e:
        logger.error(f"Exception raised when fetching group {name}: {e}")
        return None
