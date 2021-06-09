import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_401_UNAUTHORIZED,
    HTTP_202_ACCEPTED
)

from niched.core.config import ACCESS_TOKEN_EXPIRE_MINS, ACCESS_TOKEN_SECRET_KEY
from niched.database.authentication import create_user, get_user_login_details
from niched.database.mongo import conn
from niched.models.schema.users import UserDetailsDB, UserDetails, UserToken
from niched.utilities.token import create_access_token

router = APIRouter()


@router.post("/login", status_code=HTTP_202_ACCEPTED, response_model=UserToken, name="auth:login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_name = form_data.username
    password = form_data.password

    users_collection = conn.get_users_collection()
    user_db = get_user_login_details(users_collection, user_name)

    if not user_db:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    if not bcrypt.checkpw(password.encode("utf-8"), user_db.password.encode('utf-8')):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    user_no_passwd = UserDetails(**user_db.dict(exclude={"password"}))
    token = create_access_token(user_no_passwd, ACCESS_TOKEN_EXPIRE_MINS, ACCESS_TOKEN_SECRET_KEY)
    return UserToken(access_token=token, token_type="bearer")


@router.post("/signup", status_code=HTTP_201_CREATED, response_model=UserDetails, name="auth:signup")
def signup(user_name: str = Form(..., description="Unique account username, used for log-in"),
           password: str = Form(..., description="Password")):
    users_collection = conn.get_users_collection()

    if get_user_login_details(users_collection, user_name) is not None:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail="Username already exists")

    hash_pwd = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user_details = UserDetails(user_name=user_name)
    userdb = UserDetailsDB(**user_details.dict(), password=hash_pwd.decode("utf-8"))

    if create_user(users_collection, userdb):
        return user_details

    raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="User creation failed! Please try again later!")
