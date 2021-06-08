from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from bson.objectid import ObjectId


class EventIn(BaseModel):
    group_id: str
    title: str
    description: str
    tags: List[str]
    author_id: Optional[str]
    event_time: datetime

    class Config:
        schema_extra = {
            "example": {
                "group_id": "csgo",
                "title": "LAN party 5v5",
                "description": "ICL vs UCL BO5",
                "tags": ["csgo", "esports", "icl", "ucl"],
                "author_id": "london_esports_comm",
                "event_time": "2021-06-04T13:00:00"
            }
        }


class EventDB(EventIn):
    creation_time: datetime


class EventOut(EventDB):
    id: str
