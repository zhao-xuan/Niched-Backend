from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class EventMembers(BaseModel):
    going: List[str]
    interested: List[str]


class EventMembersGroup(str, Enum):
    going = "going"
    interested = "interested"


class EventIn(BaseModel):
    group_id: str
    title: str
    description: str
    tags: List[str]
    event_date: datetime

    class Config:
        schema_extra = {
            "example": {
                "group_id": "csgo",
                "title": "LAN party 5v5",
                "description": "ICL vs UCL BO5",
                "tags": ["csgo", "esports", "icl", "ucl"],
                "event_date": "2021-06-04T13:00:00"
            }
        }


class EventDB(EventIn):
    author_id: str
    members: EventMembers
    creation_date: datetime


class EventOut(EventDB):
    event_id: str

    class Config:
        schema_extra = {
            "example": {
                "group_id": "csgo",
                "event_id": "60bf5d2433989999921a476c",
                "title": "LAN party 5v5",
                "description": "ICL vs UCL BO5",
                "tags": ["csgo", "esports", "icl", "ucl"],
                "author_id": "bob",
                "event_date": "2021-06-04T13:00:00",
                "creation_date": "2021-06-12T20:18:20.454000",
                "members": {
                    "going": ["gavin", "leo"],
                    "interested": ["tom", "alice"]
                }
            }
        }
