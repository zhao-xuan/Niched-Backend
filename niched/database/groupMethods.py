import logging
from typing import Optional

from pymongo.collection import Collection

from niched.models.schema.groups import GroupData

logger = logging.getLogger(__name__)


def create_group(groups: Collection, group_details: GroupData) -> bool:
    group_dict = group_details.dict()
    try:
        groups.insert_one(group_dict)
        logger.info(f"Group {group_details.name} created successfully!")
        return True
    except Exception as e:
        logger.error(f"Cannot create group {group_details.name}, exception raised {e}")
        return False


def get_group(groups: Collection, group_id: str) -> Optional[GroupData]:
    try:
        group_json = groups.find_one({"group_id": group_id})
        return GroupData(**group_json) if group_json else None
    except Exception as e:
        logger.error(f"Exception raised when fetching group {group_id}: {e}")
        return None
