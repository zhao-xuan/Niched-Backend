import logging
from datetime import datetime
from typing import List

from bson import ObjectId
from pymongo.collection import Collection

from niched.models.schema.comments import CommentOut, CommentIn, CommentDB, OID
from niched.models.schema.users import UserDetails

logger = logging.getLogger(__name__)


def convert_comment_db_to_out(comment) -> CommentOut:
    return CommentOut(comment_id=str(comment['_id']), thread_id=str(comment['thread_id']),
                      user_name=comment['user_name'], creation_date=comment['creation_date'], body=comment['body'])


def check_comment_id_exist(comments_coll: Collection, comment_id: str) -> bool:
    return ObjectId.is_valid(comment_id) and comments_coll.count_documents({"_id": ObjectId(comment_id)}) > 0


def get_comments_in_thread(comments_coll: Collection, thread_id: str) -> List[CommentOut]:
    results = comments_coll.find({"thread_id": ObjectId(thread_id)})
    return [convert_comment_db_to_out(comment) for comment in results]


def create_comment(comments_coll: Collection, comment: CommentIn, user: UserDetails) -> CommentOut:
    comment_db = CommentDB(
        **comment.dict(exclude={"thread_id"}),
        user_name=user.user_name,
        thread_id=OID(comment.thread_id),
        creation_date=datetime.utcnow())

    result = comments_coll.insert_one(comment_db.dict())
    logger.info(f"Comment {str(result.inserted_id)} created successfully!")
    return CommentOut(comment_id=str(result.inserted_id), creation_date=comment_db.creation_date, **comment.dict())


def get_comment_with_id(comments_coll: Collection, comment_id: str) -> CommentOut:
    result = comments_coll.find_one({"_id": ObjectId(comment_id)})
    return convert_comment_db_to_out(result)


def remove_comment(comments_coll: Collection, comment_id: str):
    res = comments_coll.delete_one({"_id": ObjectId(comment_id)})
    return res.deleted_count > 0
