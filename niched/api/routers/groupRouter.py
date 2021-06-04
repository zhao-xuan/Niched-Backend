import logging
from typing import Dict

from bson.objectid import ObjectId

from fastapi import APIRouter, HTTPException

from niched.database.groupMethods import create_group, get_group, get_all_groups_in_db
from niched.database.mongo import conn
from niched.models.schema.groups import GroupDataDB, GroupFormData

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/all", response_model=Dict[str, GroupDataDB])
def get_all_groups():
    groups_collection = conn.get_groups_collection()
    all_groups = {}
    for i, group in enumerate(groups_collection.find({})):
        all_groups[i] = group

    return all_groups


@router.get("/{group_id}", response_model=GroupDataDB)
def get_group_with_id(group_id: str):
    groups_collection = conn.get_groups_collection()
    group_data = get_group(groups_collection, group_id)
    if group_data is None:
        raise HTTPException(status_code=400, detail="Group does not exist")

    return group_data


@router.post("/new")
def create_new_group(group_details: GroupFormData):
    groups_collection = conn.get_groups_collection()

    try:
        create_group(groups_collection, group_details)
    except Exception as e:
        logger.error(f"Cannot create new group {e}")
        raise HTTPException(status_code=400, detail="Failed to create new group")
