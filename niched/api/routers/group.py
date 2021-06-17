import logging
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import (HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT,
                              HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED)

from niched.database.event_utils import get_events_by_group
from niched.database.group_utils import create_group, get_group, check_group_id_exist, group_add_new_member, \
    check_member_in_group, group_remove_member, InvalidGroupOperation
from niched.database.mongo import conn
from niched.database.thread_utils import get_all_thread_in_group
from niched.database.user_utils import check_user_id_exist
from niched.models.schema.events import EventOut
from niched.models.schema.groups import GroupDataDB, NewGroupIn, GroupMemberIn
from niched.models.schema.threads import ThreadOut

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/all", response_model=List[GroupDataDB], name="group:getAllGroups")
def get_all_groups():
    groups_collection = conn.get_groups_collection()
    return [group for group in groups_collection.find({})]


@router.get("/{group_id}", response_model=GroupDataDB, status_code=HTTP_200_OK, name="group:getByID")
def get_group_with_id(group_id: str):
    groups_collection = conn.get_groups_collection()
    group_data = get_group(groups_collection, group_id)
    if group_data is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={"msg": "Group does not exist"})

    return group_data


@router.post("/new", response_model=NewGroupIn, status_code=HTTP_201_CREATED, name="group:create")
def create_new_group(group_details: NewGroupIn):
    groups_collection = conn.get_groups_collection()

    if group_details.image_url == "":
        group_details.image_url = None

    if check_group_id_exist(groups_collection, group_details.group_id):
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail={"msg": "Group ID already in used!"})

    if not create_group(groups_collection, group_details):
        logger.error(f"Cannot create new group with details {group_details.dict()}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"msg": "Unexpected Error! Server failed to create new group"})

    return group_details


@router.get("/{group_id}/events", response_model=List[EventOut], status_code=HTTP_200_OK, name="group:events")
def get_all_events_in_group(group_id: str):
    groups_collection = conn.get_groups_collection()
    events_collection = conn.get_events_collection()

    if not check_group_id_exist(groups_collection, group_id):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={"msg": "Group ID not found!"})

    return get_events_by_group(events_collection, group_id)


@router.post("/{group_id}/members", status_code=HTTP_201_CREATED, name="group:addMember")
def add_member_to_group(group_id: str, new_member: GroupMemberIn):
    groups_collection = conn.get_groups_collection()
    users_collection = conn.get_users_collection()

    if not check_group_id_exist(groups_collection, group_id):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={"msg": "Group ID not found!"})

    if not check_user_id_exist(users_collection, new_member.user_name):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={"msg": "User ID does not exist!"})

    if check_member_in_group(groups_collection, group_id, new_member.user_name):
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail={"msg": "User already in group"})

    if not group_add_new_member(groups_collection, users_collection, group_id, new_member):
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"msg": "Server failed to process request, check logs for more detail"})

    return JSONResponse(status_code=HTTP_201_CREATED, content={"detail": {"msg": "User added to group successfully"}})


@router.delete("/{group_id}/members", status_code=HTTP_200_OK, name="group:removeMember")
def get_member_in_group(group_id: str, new_member: GroupMemberIn):
    groups_collection = conn.get_groups_collection()
    users_collection = conn.get_users_collection()

    if not check_group_id_exist(groups_collection, group_id):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={"msg": "Group ID not found!"})

    if not check_user_id_exist(users_collection, new_member.user_name):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={"msg": "User ID does not exist!"})

    if not check_member_in_group(groups_collection, group_id, new_member.user_name):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={"msg": "User is not in group"})

    try:
        if not group_remove_member(groups_collection, users_collection, group_id, new_member):
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                                detail={"msg": "Server failed to process request, check logs for more detail"})
    except InvalidGroupOperation as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                            detail=e.message)

    return JSONResponse(status_code=HTTP_200_OK, content={"detail": {"msg": "User removed from group successfully"}})


@router.get("/{group_id}/threads", response_model=List[ThreadOut], status_code=HTTP_200_OK, name="group:getAllThreads")
def get_all_threads_in_group(group_id: str):
    threads_collection = conn.get_threads_collection()
    groups_collection = conn.get_groups_collection()

    if not check_group_id_exist(groups_collection, group_id):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={"msg": "Group ID not found!"})

    try:
        return get_all_thread_in_group(threads_collection, group_id)
    except Exception as e:
        logger.error(f"Server crashed while trying to retrieve threads from group {group_id}, exception raised {e}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"msg": "Server crashed while trying to retrieve threads"})
