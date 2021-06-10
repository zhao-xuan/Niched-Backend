from fastapi import APIRouter, HTTPException
from starlette.status import (
    HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND, HTTP_200_OK
)

from niched.database.event_utils import create_event, check_event_id_exist, get_event_with_id
from niched.database.mongo import conn
from niched.models.schema.events import EventIn, EventOut

router = APIRouter()


@router.post("/", response_model=EventOut, status_code=HTTP_201_CREATED, name="event:create")
def new_event(event_data: EventIn):
    event_coll = conn.get_events_collection()
    event = create_event(event_coll, event_data)

    if not event:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"msg": "Failed to create event, check logs for more detail!"})

    return event


@router.get("/{event_id}", response_model=EventOut, status_code=HTTP_200_OK, name="event:getById")
def get_event_by_id(event_id: str):
    event_coll = conn.get_events_collection()

    if not check_event_id_exist(event_coll, event_id):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail={"msg": "Invalid event id"})

    event_details = get_event_with_id(event_coll, event_id)
    if event_details is None:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"msg": "Server has encountered an error while trying to find event"})

    return event_details
