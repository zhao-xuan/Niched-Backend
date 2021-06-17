import logging
from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from pymongo.collection import Collection

from niched.models.schema.threads import ThreadIn, ThreadDB, ThreadOut

logger = logging.getLogger(__name__)


def convert_db_thread_to_out(raw_json) -> ThreadOut:
    return ThreadOut(**raw_json, thread_id=str(raw_json["_id"]))


def create_thread(threads_collection: Collection, thread_details: ThreadIn) -> ThreadOut:
    thread_data_insert = ThreadDB(**thread_details.dict(), creation_date=datetime.now())
    thread_dict = thread_data_insert.dict()

    # collection.insert returns the id of the new object inserted into the database
    thread_id = threads_collection.insert_one(thread_dict)
    raw_thread = threads_collection.find_one({"_id": thread_id.inserted_id})
    return convert_db_thread_to_out(raw_thread)


def get_thread(threads_collection: Collection, thread_id: str) -> ThreadOut:
    raw_thread = threads_collection.find_one({"_id": ObjectId(thread_id)})
    return convert_db_thread_to_out(raw_thread)


def check_thread_id_exist(thread_collection: Collection, thread_id: str) -> bool:
    return ObjectId.is_valid(thread_id) and thread_collection.count_documents({"_id": ObjectId(thread_id)}) > 0


def remove_thread(threads_collection: Collection, thread_id: str) -> bool:
    """ [thread_id] should be valid"""
    thread_query = {"_id": ObjectId(thread_id)}
    res = threads_collection.delete_one(thread_query)
    return res.deleted_count > 0


def get_all_thread_in_group(threads_collection: Collection, group_id: str) -> List[ThreadOut]:
    raw_threads = threads_collection.find({"group_id": group_id})
    return [convert_db_thread_to_out(thread) for thread in raw_threads]