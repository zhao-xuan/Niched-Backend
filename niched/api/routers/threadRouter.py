import logging
from niched.database.threadMethods import create_thread
from typing import Dict

from fastapi import APIRouter, HTTPException

from niched.database.threadMethods import create_thread
from niched.database.mongo import conn
from niched.models.schema.threads import ThreadDataDB, ThreadFormData

router = APIRouter()

logger = logging.getLogger(__name__)

"""
Thread endpoint functions. The following functions should be created:
1. get_threads_in_group()
2. get_thread()
3. create_thread()

"""


# @router.get("/{group_id}", response_model=Dict[str, GroupDataDB])
# def get_threads_in_group(group_id: str):
#     groups_collection = conn.get_groups_collection()
#     all_groups = {}
#     for i, group in enumerate(groups_collection.find({})):
#         all_groups[i] = group

#     return all_groups


# @router.get("/{group_id}", response_model=GroupDataDB)
# def get_group_with_id(group_id: str):
#     groups_collection = conn.get_groups_collection()
#     group_data = get_group(groups_collection, group_id)
#     if group_data is None:
#         raise HTTPException(status_code=400, detail="Group does not exist")

#     return group_data


@router.post("/new")
def create_new_thread(thread_details: ThreadFormData):
    threads_collection = conn.get_threads_collection()

    try:
        create_thread(threads_collection, thread_details)
    except Exception as e:
        logger.error(f"Cannot create new thread {e}")
        raise HTTPException(status_code=400, detail=f"Failed to create new thread {e}")
