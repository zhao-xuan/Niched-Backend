from fastapi import APIRouter, HTTPException
from starlette.status import (
    HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST
)

from niched.database.event_utils import create_event, check_event_id_exist, get_event_with_id, InvalidEventException
from niched.database.mongo import conn
from niched.database.user_utils import check_user_id_exist
from niched.models.schema.events import EventIn, EventOut

router = APIRouter()


@router.post("/", response_model=EventOut, status_code=HTTP_201_CREATED, name="event:create")
def new_event(event_data: EventIn):
    event_coll = conn.get_events_collection()
    users_coll = conn.get_users_collection()

    if not check_user_id_exist(users_coll, event_data.author_id):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail={"msg": "Invalid user ID!"})

    try:
        event = create_event(event_coll, event_data)
        return event
    except InvalidEventException as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail={"msg": e.message})


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
