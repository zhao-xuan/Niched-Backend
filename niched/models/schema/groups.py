from typing import Optional

from pydantic import BaseModel


# class UserDeta(BaseModel):
#     name: str
#     description: str


class GroupData(BaseModel):
    name: str
    description: str
    image_url:Optional[str]

