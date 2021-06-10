from fastapi import APIRouter, HTTPException
from starlette.status import (
    HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND, HTTP_200_OK
)

from niched.database.mongo import conn
from niched.database.user_utils import check_user_id_exist, get_user_profile, update_user_profile
from niched.models.schema.users import UserDetails, UserDetailsUpdate

router = APIRouter()


@router.get("/{user_name}", response_model=UserDetails, status_code=HTTP_200_OK, name="user:profile")
def get_profile_by_user_name(user_name: str):
    users_coll = conn.get_users_collection()

    if not check_user_id_exist(users_coll, user_name):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={"msg": "User ID does not exist"})

    user_profile = get_user_profile(users_coll, user_name)

    if not user_profile:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"msg": "Internal server error, check logs for more detail!"})

    return user_profile


@router.post("/{user_name}", status_code=HTTP_200_OK, name="user:updateDetails")
def update_profile_by_user_name(user_name: str, user_details: UserDetailsUpdate):
    users_coll = conn.get_users_collection()

    if not check_user_id_exist(users_coll, user_name):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={"msg": "User ID does not exist"})

    new_profile = update_user_profile(users_coll, user_name, user_details)
    if not new_profile:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"msg": f"Record failed to update for user {user_name}"})

    return new_profile
