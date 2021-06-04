import logging
from niched.database.threadMethods import create_thread
from bson.objectid import ObjectId
from typing import Dict

from bson import json_util
import json 

from fastapi import APIRouter, HTTPException, Body, FastAPI, status
from fastapi.responses import JSONResponse

from niched.database.threadMethods import create_thread, get_thread
from niched.database.groupMethods import get_group
from niched.database.mongo import conn
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

 
"""
---- returns a HTTP 201 status code, with header containing ObjectID of new thread.
Success: HTTP 201 with response body:
{
  "$oid": "60ba0e2233aa9e2863ab2185"
}
"""
@router.post("/new")
def create_new_thread(thread_details: ThreadFormData):
    threads_collection = conn.get_threads_collection()
    groups_collection = conn.get_groups_collection()
    # check thread_details.group_id is a valid group first!
    group_data = get_group(groups_collection, thread_details.group_id)
    if group_data is None:
        raise HTTPException(status_code=400, detail="Group does not exist")

    try:
        _id = create_thread(threads_collection, thread_details)
        # check if an object ID was returned, and not empty
        if _id:
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=parse_json(_id))
        else:
            logger.error(f"Failed to assign object ID (insertion into database failed)")
            raise HTTPException(status_code=400, detail=f"Failed to create new thread")
    except Exception as e:
        logger.error(f"Cannot create new thread {e}")
        raise HTTPException(status_code=400, detail=f"Failed to create new thread {e}")


@router.get("/{thread_id}/", response_model=ThreadDataDB)
def get_group_with_id(thread_id: str):
    threads_collection = conn.get_threads_collection()

    thread_data = get_thread(threads_collection, thread_id)

    if thread_data is None:
        raise HTTPException(status_code=400, detail="Thread does not exist")

    return thread_data


@router.get("/by_group/{group_id}", response_model=Dict[str, ThreadDataDB])
def get_threads_in_group(group_id: str):
    threads_collection = conn.get_threads_collection()
    groups_collection = conn.get_groups_collection()

    group_threads = {}

    for i, thread in enumerate(threads_collection.find({"group_id": group_id})):
        group_threads[i] = thread

    return group_threads



