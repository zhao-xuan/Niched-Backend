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


class EventMemberIn(BaseModel):
    user_name: str
    group: EventMembersGroup


class EventIn(BaseModel):
    group_id: str
    title: str
    description: str
    tags: List[str]
    author_id: str
    event_time: datetime

    class Config:
        schema_extra = {
            "example": {
                "group_id": "csgo",
                "title": "LAN party 5v5",
                "description": "ICL vs UCL BO5",
                "tags": ["csgo", "esports", "icl", "ucl"],
                "author_id": "bob",
                "event_time": "2021-06-04T13:00:00"
            }
        }


class EventDB(EventIn):
    members: EventMembers
    creation_time: datetime


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
                "event_time": "2021-06-04T13:00:00",
                "members": {
                    "going": ["gavin", "leo"],
                    "interested": ["tom", "alice"]
                }
            }
        }
