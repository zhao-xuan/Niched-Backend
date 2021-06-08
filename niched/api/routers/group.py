import logging
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import constr
from starlette.status import (HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT,
                              HTTP_500_INTERNAL_SERVER_ERROR)

from niched.database.events import get_events_by_group
from niched.database.groupMethods import create_group, get_group, check_group_id_exist
from niched.database.mongo import conn
from niched.models.schema.events import EventOut
from niched.models.schema.groups import GroupDataDB, GroupFormData

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
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Group does not exist")

    return group_data


@router.post("/new", response_model=GroupFormData, status_code=HTTP_201_CREATED, name="group:create")
def create_new_group(group_details: GroupFormData):
    groups_collection = conn.get_groups_collection()

    if group_details.image_url == "":
        group_details.image_url = None

    if check_group_id_exist(groups_collection, group_details.group_id):
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail="Group ID already in used!")

    if not create_group(groups_collection, group_details):
        logger.error(f"Cannot create new group with details {group_details.dict()}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unexpected Error! Server failed to create new group")

    return group_details


@router.get("/{group_id}/events", response_model=List[EventOut], status_code=HTTP_200_OK, name="group:events")
def get_all_events_in_group(group_id: constr(regex=r'^[a-zA-Z0-9][-a-zA-Z0-9]*[a-zA-Z0-9]*$')):
    groups_collection = conn.get_groups_collection()
    events_collection = conn.get_events_collection()

    if not check_group_id_exist(groups_collection, group_id):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Group ID not found!")

    return get_events_by_group(events_collection, group_id)
