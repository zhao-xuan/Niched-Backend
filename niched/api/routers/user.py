from fastapi import APIRouter, HTTPException
from starlette.status import (
    HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND, HTTP_200_OK
)

from niched.database.mongo import conn
from niched.database.user_utils import check_user_id_exist, get_user_profile, update_user_profile
from niched.models.schema.users import UserDetails, UserDetailsUpdate

router = APIRouter()


@router.get("/{username}", response_model=UserDetails, status_code=HTTP_200_OK, name="user:profile")
def get_profile_by_username(username: str):
    users_coll = conn.get_users_collection()

    if not check_user_id_exist(users_coll, username):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User ID does not exist")

    user_profile = get_user_profile(users_coll, username)

    if not user_profile:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error, check logs for more detail!")

    return user_profile


@router.post("/{username}", status_code=HTTP_200_OK, name="user:updateDetails")
def update_profile_by_username(username: str, user_details: UserDetailsUpdate):
    users_coll = conn.get_users_collection()

    if not check_user_id_exist(users_coll, username):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User ID does not exist")

    new_profile = update_user_profile(users_coll, username, user_details)
    if not new_profile:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Record failed to update for user {username}")

    return new_profile
