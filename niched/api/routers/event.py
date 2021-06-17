from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST
)

from niched.database.event_utils import (create_event, check_event_id_exist, get_event_with_id, InvalidEventException,
                                         add_event_member, remove_event_member)
from niched.database.mongo import conn
from niched.models.schema.events import EventIn, EventOut, EventMembersGroup
from niched.models.schema.users import UserDetails
from niched.utilities.token import get_current_active_user

router = APIRouter()


@router.post("/", response_model=EventOut, status_code=HTTP_201_CREATED, name="event:create")
def new_event(event_data: EventIn, current_user: UserDetails = Depends(get_current_active_user)):
    event_coll = conn.get_events_collection()
    users_coll = conn.get_users_collection()

    try:
        event = create_event(event_coll, event_data, current_user.user_name)
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


@router.post("/{event_id}/members", status_code=HTTP_201_CREATED, name="event:join")
def add_member_to_event(event_id: str, group: EventMembersGroup,
                        current_user: UserDetails = Depends(get_current_active_user)):
    event_coll = conn.get_events_collection()

    if not check_event_id_exist(event_coll, event_id):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail={"msg": "Invalid event id"})

    if add_event_member(event_coll, event_id, group, current_user):
        return JSONResponse(status_code=HTTP_201_CREATED,
                            content={
                                "detail": {
                                    "msg": f"User @{current_user.user_name} added to {group.group.upper()}"
                                }
                            })
    return HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Server failed to process request"})


@router.delete("/{event_id}/members", status_code=HTTP_200_OK, name="event:leave")
def add_member_to_event(event_id: str, group: EventMembersGroup,
                        current_user: UserDetails = Depends(get_current_active_user)):
    event_coll = conn.get_events_collection()

    if not check_event_id_exist(event_coll, event_id):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail={"msg": "Invalid event id"})

    if remove_event_member(event_coll, event_id, group, current_user):
        return JSONResponse(status_code=HTTP_201_CREATED,
                            content={
                                "detail": {
                                    "msg": f"User @{group.user_name} removed from {group.group.upper()}"
                                }
                            })
    return HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Server failed to process request"})
