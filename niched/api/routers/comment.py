import logging

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from niched.database.comment_utils import create_comment, check_comment_id_exist, remove_comment, get_comment_with_id
from niched.database.mongo import conn
from niched.database.thread_utils import check_thread_id_exist
from niched.models.schema.comments import CommentIn, CommentOut
from niched.models.schema.users import UserDetails
from niched.utilities.token import get_current_active_user

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/", name="comment:postComment")
def post_comment_to_thread(comment: CommentIn, current_user: UserDetails = Depends(get_current_active_user)):
    threads_collection = conn.get_threads_collection()
    comments_collection = conn.get_comments_collection()

    if not check_thread_id_exist(threads_collection, comment.thread_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Thread ID does not exist"})

    return create_comment(comments_collection, comment, current_user)


@router.get("/{comment_id}", response_model=CommentOut, status_code=HTTP_200_OK, name="comment:getComment")
def post_comment_to_thread(comment_id: str):
    comments_collection = conn.get_comments_collection()

    if not check_comment_id_exist(comments_collection, comment_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Comment ID does not exist"})

    comment_details = get_comment_with_id(comments_collection, comment_id)
    if comment_details is None:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"msg": "Server has encountered an error while trying to find comment"})

    return comment_details


@router.delete("/{comment_id}", name="comment:deleteComment")
def delete_comment_with_id(comment_id: str):
    comments_collection = conn.get_comments_collection()

    if not check_comment_id_exist(comments_collection, comment_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "comment ID does not exist"})

    if remove_comment(comments_collection, comment_id):
        return JSONResponse(status_code=HTTP_200_OK,
                            content={
                                "detail": {
                                    "msg": f"Comment {comment_id} removed!"
                                }
                            })
    return HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Server failed to process request"})
