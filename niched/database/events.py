import logging
from datetime import datetime
from typing import Optional

from bson import ObjectId
from pymongo.collection import Collection

from niched.models.schema.events import EventIn, EventOut, EventDB

logger = logging.getLogger(__name__)


def create_event(events: Collection, event: EventIn) -> Optional[EventOut]:
    event_db = EventDB(
        **event.dict(),
        creation_time=datetime.utcnow(),
    )

    try:
        result = events.insert_one(event_db.dict())
        logger.info(f"Event {str(result.inserted_id)} created successfully!")
        return EventOut(id=str(result.inserted_id), **event_db.dict())
    except Exception as e:
        logger.error(f"Cannot create event [{event.title}] in group [{event.group_id}], exception raised {e}")
        return None
