from datetime import datetime
from typing import Optional

from pydantic import constr, BaseModel, HttpUrl


class GroupFormData(BaseModel):
    group_id: constr(regex=r'^[a-zA-Z0-9][-a-zA-Z0-9]*[a-zA-Z0-9]*$')
    name: constr(min_length=1, max_length=50)
    description: constr(min_length=0, max_length=120)
    image_url: Optional[HttpUrl]

    class Config:
        schema_extra = {
            "example": {
                "group_id": "csgo",
                "name": "Counter Strike: Global Offsensive",
                "description": "CSGO players number 1!",
                "image_url": "http://media.steampowered.com/apps/csgo/blog/images/fb_image.png?v=6"
            }
        }


class GroupDataDB(GroupFormData):
    creation_date: datetime
