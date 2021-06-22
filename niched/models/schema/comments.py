from datetime import datetime

from pydantic import BaseModel

from niched.models.schema.oid import OID


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
