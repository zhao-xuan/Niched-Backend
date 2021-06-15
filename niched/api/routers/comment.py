import logging

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from niched.database.comment_utils import create_comment, check_comment_id_exist, remove_comment
from niched.database.mongo import conn
from niched.database.thread_utils import check_thread_id_exist
from niched.models.schema.comments import CommentIn

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/", name="comment:postComment")
def post_comment_to_thread(comment: CommentIn):
    threads_collection = conn.get_threads_collection()
    comments_collection = conn.get_comments_collection()

    if not check_thread_id_exist(threads_collection, comment.thread_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Thread ID does not exist"})

    return create_comment(comments_collection, comment)


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
