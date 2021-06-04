import logging
from datetime import datetime
from typing import Optional, List


from pymongo.collection import Collection

from niched.models.schema.threads import ThreadFormData, ThreadDataDB

logger = logging.getLogger(__name__)



def create_thread(threads_collection: Collection, thread_details: ThreadFormData) -> str:
    thread_data_insert = ThreadDataDB(
        group_id=thread_details.group_id,
        title=thread_details.title,
        description=thread_details.group_id,
        creation_date=datetime.utcnow())

    thread_dict = thread_data_insert.dict()

    try:
        # collection.insert returns the id of the new object inserted into the database
        _id = threads_collection.insert(thread_dict)
        logger.info(f"Thread {thread_details.title} created successfully!")
        print(_id)
        return _id
    except Exception as e:
        logger.error(f"Cannot create thread {thread_details.title}, exception raised {e}")
        return ""


def get_thread(threads_collection: Collection, thread_id: str) -> Optional[ThreadDataDB]:
    try:
        thread_json = threads_collection.find_one({"_id": thread_id})
        return ThreadDataDB(**thread_json) if thread_json else None
    except Exception as e:
        logger.error(f"Exception raised when fetching thread {thread_id}: {e}")
        return None


# def get_all_groups_in_db(groups: Collection) -> List[GroupDataDB]:
#     try:
#         groups = groups.find({})
#         return [group for group in groups]
#     except Exception as e:
#         logger.error(f"Exception raised when fetching all groups in database {e} ")
#         return []
