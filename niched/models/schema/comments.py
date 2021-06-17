from datetime import datetime

from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel


class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(str(v))
        except InvalidId:
            raise ValueError("Not a valid ObjectId")


class CommentIn(BaseModel):
    thread_id: str
    body: str


class CommentDB(CommentIn):
    thread_id: OID
    user_name: str
    body: str
    creation_date: datetime


class CommentOut(CommentIn):
    comment_id: str
    creation_date: datetime
