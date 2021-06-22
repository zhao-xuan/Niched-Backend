import logging
from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from niched.database.comment_utils import get_comments_in_thread
from niched.database.group_utils import check_group_id_exist
from niched.database.mongo import conn
from niched.database.thread_utils import create_thread, get_thread, check_thread_id_exist, remove_thread
from niched.database.user_utils import check_user_id_exist
from niched.models.schema.comments import CommentOut, CommentIn
from niched.models.schema.threads import ThreadIn, ThreadOut

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("", response_model=ThreadOut, status_code=status.HTTP_201_CREATED, name="thread:create")
def create_new_thread(thread_details: ThreadIn):
    threads_collection = conn.get_threads_collection()
    groups_collection = conn.get_groups_collection()
    users_collection = conn.get_users_collection()

    if not check_group_id_exist(groups_collection, thread_details.group_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Group does not exist"})

    if not check_user_id_exist(users_collection, thread_details.author_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Invalid user ID"})

    thread_out = create_thread(threads_collection, thread_details)
    if thread_out:
        return thread_out
    else:
        logger.error(f"Failed to create new thread (insertion into database failed)")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"msg": "Server failed to create new thread"})


@router.get("/{thread_id}", response_model=ThreadOut, status_code=HTTP_200_OK, name="thread:getByID")
def get_thread_with_id(thread_id: str):
    threads_collection = conn.get_threads_collection()

    if not check_thread_id_exist(threads_collection, thread_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Thread ID does not exist"})

    try:
        return get_thread(threads_collection, thread_id)
    except Exception as e:
        logger.error(f"Server failed to create new thread, exception raised {e}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"msg": "Server failed to create new thread"})


@router.delete("/{thread_id}", status_code=HTTP_200_OK, name="thread:remove")
def remove_thread_with_id(thread_id: str):
    threads_collection = conn.get_threads_collection()
    comments_collection = conn.get_comments_collection()

    if not check_thread_id_exist(threads_collection, thread_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Thread ID does not exist"})

    if remove_thread(threads_collection, comments_collection, thread_id):
        return JSONResponse(status_code=HTTP_200_OK, content={
            "detail": {
                "msg": "Thread removed successfully"
            }
        })

    logger.error(f"Server failed to delete thread with ID {thread_id}")
    raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                        detail={"msg": "Server failed to delete new thread"})


@router.get("/{thread_id}/comments", response_model=List[CommentOut], status_code=HTTP_200_OK,
            name="thread:getComments")
def get_all_comments_in_thread(thread_id: str):
    threads_collection = conn.get_threads_collection()
    comments_collection = conn.get_comments_collection()

    if not check_thread_id_exist(threads_collection, thread_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Thread ID does not exist"})

    return get_comments_in_thread(comments_collection, thread_id)

