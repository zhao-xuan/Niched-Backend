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
    group_details_json = groups_collection.find_one({"name" : group_id})
    return GroupData(**group_details_json)

@router.post("/new")
def create_new_group(group_details: GroupData):
    groups_collection = conn.get_groups_collection()

    try:
        create_group(groups_collection, group_details)
    except Exception as e:
        logger.error(f"Cannot create new group {e}")
        raise HTTPException(status_code=400, detail="Failed to create new group")

@router.get("/groupinfo", response_model=GroupData)
def group_info(name: str = Form(..., description="Name for the group to be queried in the database")):

    groups_collection = conn.get_groups_collection()

    group_details = get_group(groups_collection, name)

    if group_details:
        return group_details

    raise HTTPException(status_code=400, detail="Group search failed.")



# @router.post("/creategroup")
# def new_goup(name: str = Form(..., description="Unique space name, for identifying a group"),
#            description: str = Form(..., description="Description for the space")):

#     groups_collection = conn.get_groups_collection()

#     if get_group(groups_collection, name) is not None:
#         raise HTTPException(status_code=400, detail="Group already exists")

#     groupdb = GroupData(name=name, description=description)

#     if create_group(groups_collection, groupdb):
#         return {"name": name}

#     raise HTTPException(status_code=500, detail="Group creation failed! Please try again later!")