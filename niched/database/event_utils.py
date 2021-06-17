import logging
from datetime import datetime
from typing import Optional, List

from bson import ObjectId
from pymongo.collection import Collection

from niched.models.schema.events import EventIn, EventOut, EventDB, EventMembers, EventMembersGroup
from niched.models.schema.users import UserDetails

logger = logging.getLogger(__name__)


class EventException(Exception):
    """ Exceptions for event """


class InvalidEventException(EventException):
    """Exceptions in Event"""

    def __init__(self, message):
        self.message = message


def create_event(events_collection: Collection, event: EventIn, user: UserDetails) -> EventOut:
    event_db = EventDB(
        **event.dict(),
        author_id=user.user_name,
        creation_date=datetime.utcnow(),
        members=EventMembers(going=[], interested=[])
    )

    if event.event_date <= datetime.now():
        raise InvalidEventException("Cannot create event in the past")

    result = events_collection.insert_one(event_db.dict())
    logger.info(f"Event {str(result.inserted_id)} created successfully!")
    return EventOut(event_id=str(result.inserted_id), **event_db.dict())


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


def add_event_member(events_collection: Collection, event_id: str, group: EventMembersGroup,
                     user: UserDetails) -> bool:
    for event_group in EventMembersGroup:
        events_collection.update_one({"_id": ObjectId(event_id)},
                                     {"$pull": {f"members.{event_group}": user.user_name}})

    res = events_collection.update_one({"_id": ObjectId(event_id)},
                                       {"$addToSet": {f"members.{group}": user.user_name}})
    return res.matched_count > 0


def remove_event_member(events_collection: Collection, event_id: str, group: EventMembersGroup,
                        user: UserDetails) -> bool:
    res = events_collection.update_one({"_id": ObjectId(event_id)},
                                       {"$pull": {f"members.{group}": user.user_name}})
    return res.matched_count > 0
