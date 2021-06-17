from datetime import datetime

from pydantic import constr, BaseModel


class ThreadIn(BaseModel):
    group_id: constr(regex=r'^[a-zA-Z0-9][-a-zA-Z0-9]*[a-zA-Z0-9]*$')
    author_id: str
    title: constr(min_length=1, max_length=50)
    description: constr(min_length=0, max_length=500)


class ThreadDB(ThreadIn):
    creation_date: datetime


class ThreadOut(ThreadDB):
    thread_id: str
