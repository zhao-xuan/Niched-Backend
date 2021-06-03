import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm

from niched.database.groupMethods import create_group, get_group
from niched.database.mongo import conn
from niched.models.schema.groups import GroupDetailsDB

router = APIRouter()


@router.post("/groupinfo")
def group_info(name: str = Form(..., description="Name for the group to be queried in the database")):

    groups_collection = conn.get_groups_collection()

    group_details = get_group(groups_collection, name)

    if group_details:
        return group_details

    raise HTTPException(status_code=400, detail="Group search failed.")


@router.post("/creategroup")
def new_goup(name: str = Form(..., description="Unique space name, for identifying a group"),
           description: str = Form(..., description="Description for the space")):

    groups_collection = conn.get_groups_collection()

    if get_group(groups_collection, name) is not None:
        raise HTTPException(status_code=400, detail="Group already exists")

    groupdb = GroupDetailsDB(name=name, description=description)

    if create_group(groups_collection, groupdb):
        return {"name": name}

    raise HTTPException(status_code=500, detail="Group creation failed! Please try again later!")