import logging
from datetime import datetime
from typing import Optional

from pymongo.collection import Collection

from niched.models.schema.groups import GroupDataDB, GroupFormData

logger = logging.getLogger(__name__)


def create_group(groups: Collection, group_details: GroupFormData) -> bool:

    group_data_insert = GroupDataDB(
        group_id     = group_details.group_id,
        name         = group_details.name,
        description  = group_details.group_id,
        image_url    = group_details.image_url,
        creation_date=datetime.utcnow()  ) # group_details.dict()

    group_dict = group_data_insert.dict()

    try:
        groups.insert_one(group_dict)
        logger.info(f"Group {group_details.name} created successfully!")
        return True
    except Exception as e:
        logger.error(f"Cannot create group {group_details.name}, exception raised {e}")
        return False


def get_group(groups: Collection, group_id: str) -> Optional[GroupDataDB]:
    try:
        group_json = groups.find_one({"group_id": group_id})
        return GroupDataDB(**group_json) if group_json else None
    except Exception as e:
        logger.error(f"Exception raised when fetching group {group_id}: {e}")
        return None
