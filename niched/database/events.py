import logging
from datetime import datetime
from typing import Optional, List

from pymongo.collection import Collection

from niched.models.schema.events import EventIn, EventOut, EventDB

logger = logging.getLogger(__name__)


def create_event(events_collection: Collection, event: EventIn) -> Optional[EventOut]:
    event_db = EventDB(
        **event.dict(),
        creation_time=datetime.utcnow(),
    )

    try:
        result = events_collection.insert_one(event_db.dict())
        logger.info(f"Event {str(result.inserted_id)} created successfully!")
        return EventOut(event_id=str(result.inserted_id), **event_db.dict())
    except Exception as e:
        logger.error(f"Cannot create event [{event.title}] in group [{event.group_id}], exception raised {e}")
        return None


def get_events_by_group(events_collection: Collection, group_id: str) -> List[EventOut]:
    events = events_collection.find({"group_id": group_id})

    def convert_event_db_to_out(event):
        return EventOut(event_id=str(event['_id']), **event)

    return [convert_event_db_to_out(e) for e in events]
