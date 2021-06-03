import logging
from datetime import datetime
from typing import Optional, List

from pymongo.collection import Collection

from niched.models.schema.threads import ThreadFormData, ThreadDataDB

logger = logging.getLogger(__name__)


def create_thread(threads: Collection, thread_details: ThreadFormData) -> bool:
    thread_data_insert = ThreadDataDB(
        group_id=thread_details.group_id,
        title=thread_details.title,
        description=thread_details.group_id,
        creation_date=datetime.utcnow())

    thread_dict = thread_data_insert.dict()

    try:
        threads.insert_one(thread_dict)
        logger.info(f"Thread {thread_details.title} created successfully!")
        return True
    except Exception as e:
        logger.error(f"Cannot create thread {thread_details.title}, exception raised {e}")
        return False


# def get_group(groups: Collection, group_id: str) -> Optional[GroupDataDB]:
#     try:
#         group_json = groups.find_one({"group_id": group_id})
#         return GroupDataDB(**group_json) if group_json else None
#     except Exception as e:
#         logger.error(f"Exception raised when fetching group {group_id}: {e}")
#         return None


# def get_all_groups_in_db(groups: Collection) -> List[GroupDataDB]:
#     try:
#         groups = groups.find({})
#         return [group for group in groups]
#     except Exception as e:
#         logger.error(f"Exception raised when fetching all groups in database {e} ")
#         return []
