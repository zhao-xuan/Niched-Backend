from fastapi import APIRouter, HTTPException
from starlette.status import (
    HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
)

from niched.database.events import create_event
from niched.database.mongo import conn
from niched.models.schema.events import EventIn, EventOut

router = APIRouter()


@router.post("/", response_model=EventOut, status_code=HTTP_201_CREATED, name="event:create")
def new_event(event_data: EventIn):
    event_coll = conn.get_events_collection()

    event = create_event(event_coll, event_data)

    if not event:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to create event, check logs for more detail!")

    return event
