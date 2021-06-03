import logging
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm

from niched.database.groupMethods import create_group, get_group
from niched.database.mongo import conn
from niched.models.schema.groups import GroupData

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/groups", response_model=GroupData)
def get_all_groups():
    groups_collection = conn.get_groups_collection()
    for group in groups_collection.find({}):
        logger.info(group)
    logger.info("HERE")


@router.get("/{group_id}", response_model=GroupData)
def get_all_groups(group_id: str):
    groups_collection = conn.get_groups_collection()
    group_data = get_group(groups_collection, group_id)
    if group_data is None:
        raise HTTPException(status_code=400, detail="Group does not exist")

    return group_data


@router.post("/new")
def create_new_group(group_details: GroupData):
    groups_collection = conn.get_groups_collection()

    try:
        create_group(groups_collection, group_details)
    except Exception as e:
        logger.error(f"Cannot create new group {e}")
        raise HTTPException(status_code=400, detail="Failed to create new group")