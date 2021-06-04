import json
import logging
from typing import Dict

from bson import json_util
from fastapi import APIRouter, HTTPException, status

from niched.database.groupMethods import get_group
from niched.database.mongo import conn
from niched.database.threadMethods import create_thread, get_thread
from niched.models.schema.threads import ThreadDataDB, ThreadFormData

router = APIRouter()

logger = logging.getLogger(__name__)


def parse_json(data):
    return json.loads(json_util.dumps(data))


"""
Thread endpoint functions. The following functions should be created:
1. get_threads_in_group()
2. get_thread()
3. create_thread()
"""


@router.post("/new", response_model=ThreadFormData, status_code=status.HTTP_201_CREATED, name="thread:create")
def create_new_thread(thread_details: ThreadFormData):
    threads_collection = conn.get_threads_collection()
    groups_collection = conn.get_groups_collection()
    # check thread_details.group_id is a valid group first!
    group_data = get_group(groups_collection, thread_details.group_id)
    if group_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group does not exist")

    _id = create_thread(threads_collection, thread_details)
    # check if an object ID was returned, and not empty
    if _id:
        return thread_details
    else:
        logger.error(f"Failed to assign object ID (insertion into database failed)")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Server failed to create new thread")


@router.get("/{thread_id}/", response_model=ThreadDataDB, name="thread:getByID")
def get_thread_with_id(thread_id: str):
    threads_collection = conn.get_threads_collection()

    thread_data = get_thread(threads_collection, thread_id)

    if thread_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread ID does not exist")

    return thread_data


@router.get("/by_group/{group_id}", response_model=Dict[str, ThreadDataDB], name="thread:getAllThreadByGroup")
def get_threads_in_group(group_id: str):
    threads_collection = conn.get_threads_collection()
    return [thread for thread in threads_collection.find({"group_id": group_id})]
