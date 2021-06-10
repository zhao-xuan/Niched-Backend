import json
import logging

from bson import json_util
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from niched.database.group_utils import get_group, check_group_id_exist
from niched.database.mongo import conn
from niched.database.thread_utils import create_thread, get_thread, check_thread_id_exist, remove_thread
from niched.models.schema.threads import ThreadDB, ThreadIn, ThreadOut

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


@router.post("/", response_model=ThreadOut, status_code=status.HTTP_201_CREATED, name="thread:create")
def create_new_thread(thread_details: ThreadIn):
    threads_collection = conn.get_threads_collection()
    groups_collection = conn.get_groups_collection()

    if check_group_id_exist(groups_collection, thread_details.group_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group does not exist")

    thread_out = create_thread(threads_collection, thread_details)
    # check if an object ID was returned, and not empty
    if thread_out:
        return thread_out
    else:
        logger.error(f"Failed to create new thread (insertion into database failed)")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Server failed to create new thread")


@router.get("/{thread_id}/", response_model=ThreadOut, status_code=HTTP_200_OK, name="thread:getByID")
def get_thread_with_id(thread_id: str):
    threads_collection = conn.get_threads_collection()

    if check_thread_id_exist(threads_collection, thread_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread ID does not exist")

    try:
        return get_thread(threads_collection, thread_id)
    except Exception as e:
        logger.error(f"Server failed to create new thread, exception raised {e}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Server failed to create new thread")


@router.delete("/{thread_id}/", status_code=HTTP_200_OK, name="thread:remove")
def remove_thread_with_id(thread_id: str):
    threads_collection = conn.get_threads_collection()

    if check_thread_id_exist(threads_collection, thread_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread ID does not exist")

    if remove_thread(threads_collection, thread_id):
        return JSONResponse(status_code=HTTP_200_OK, content={
            "detail": "Thread removed successfully"
        })

    logger.error(f"Server failed to delete thread with ID {thread_id}")
    raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Server failed to delete new thread")
