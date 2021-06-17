from datetime import datetime
from typing import Optional, Union, List

from pydantic import constr, BaseModel, HttpUrl


class NewGroupIn(BaseModel):
    group_id: constr(regex=r'^[a-zA-Z0-9][-a-zA-Z0-9]*[a-zA-Z0-9]$')
    author_id: str
    name: constr(min_length=1, max_length=50)
    description: constr(min_length=0, max_length=120)
    image_url: Optional[Union[HttpUrl, constr(min_length=0, max_length=0)]]
    tags: Optional[List[constr(to_lower=True, strip_whitespace=True)]] = []

    class Config:
        schema_extra = {
            "example": {
                "group_id": "csgo",
                "author_id": "alice",
                "name": "Counter Strike: Global Offsensive",
                "description": "CSGO players number 1!",
                "image_url": "http://media.steampowered.com/apps/csgo/blog/images/fb_image.png?v=6"
            }
        }


class GroupDataDB(NewGroupIn):
    members: List[str]
    creation_date: datetime


class GroupMemberIn(BaseModel):
    user_name: str
