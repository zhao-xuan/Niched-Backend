from typing import Optional

from pydantic import BaseModel


# class UserDetails(BaseModel):
#     name: str
#     description: str


class GroupDetailsDB(BaseModel):
    name: str
    description: str
