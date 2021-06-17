import logging
from datetime import datetime
from typing import Optional, List

import pymongo
from bson import ObjectId
from pymongo.collection import Collection

from niched.models.schema.events import EventIn, EventOut, EventDB, EventMembers, EventMemberIn, EventMembersGroup

logger = logging.getLogger(__name__)


class EventException(Exception):
    """ Exceptions for event """


class InvalidEventException(EventException):
    """Exceptions in Event"""

    def __init__(self, message):
        self.message = message


def create_event(events_collection: Collection, event: EventIn) -> EventOut:
    event_db = EventDB(
        **event.dict(),
        creation_date=datetime.utcnow(),
        members=EventMembers(going=[], interested=[])
    )

    if event.event_date <= datetime.now():
        raise InvalidEventException("Cannot create event in the past")

    result = events_collection.insert_one(event_db.dict())
    logger.info(f"Event {str(result.inserted_id)} created successfully!")
    return EventOut(event_id=str(result.inserted_id), **event_db.dict())


def get_all_events(events_collection: Collection, skip: int, limit: int) -> List[EventOut]:
    events = events_collection.find({}).sort("creation_date", pymongo.DESCENDING).skip(skip).limit(limit)
    return [EventOut(event_id=str(e['_id']), **e) for e in events]


def get_events_by_group(events_collection: Collection, group_id: str) -> List[EventOut]:
    events = events_collection.find({"group_id": group_id})

    def convert_event_db_to_out(event):
        return EventOut(event_id=str(event['_id']), **event)

    return [convert_event_db_to_out(e) for e in events]


def get_event_with_id(events_collection: Collection, event_id: str) -> Optional[EventOut]:
    """ Pre-condition: event_id is valid """
    event_json = events_collection.find_one({"_id": ObjectId(event_id)})

    if not event_json:
        logger.error(f"Cannot retrieve event with id {event_id}!")
        return None

    event_details = EventOut(event_id=str(event_json['_id']), **event_json)
    return event_details


def check_event_id_exist(events_collection: Collection, event_id: str) -> bool:
    return ObjectId.is_valid(event_id) and events_collection.count_documents({"_id": ObjectId(event_id)}) > 0


def add_event_member(events_collection: Collection, event_id: str, member: EventMemberIn) -> bool:
    for event_group in EventMembersGroup:
        events_collection.update_one({"_id": ObjectId(event_id)},
                                     {"$pull": {f"members.{event_group}": member.user_name}})

    res = events_collection.update_one({"_id": ObjectId(event_id)},
                                       {"$addToSet": {f"members.{member.group}": member.user_name}})
    return res.matched_count > 0


def remove_event_member(events_collection: Collection, event_id: str, member: EventMemberIn) -> bool:
    res = events_collection.update_one({"_id": ObjectId(event_id)},
                                       {"$pull": {f"members.{member.group}": member.user_name}})
    return res.matched_count > 0
