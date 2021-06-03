from datetime import datetime
from typing import Optional

from pydantic import constr, BaseModel, HttpUrl


class ThreadFormData(BaseModel):
    group_id: constr(regex=r'^[a-zA-Z0-9][-a-zA-Z0-9]*[a-zA-Z0-9]*$')
    title: constr(min_length=1, max_length=50)
    description: constr(min_length=0, max_length=120)


class ThreadDataDB(ThreadFormData):
    creation_date: datetime
