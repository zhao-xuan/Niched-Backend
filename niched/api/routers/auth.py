import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm

from niched.database.authentication import create_user, get_user
from niched.database.mongo import conn
from niched.models.schema.users import UserDetailsDB

router = APIRouter()


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    users_collection = conn.get_users_collection()
    user = get_user(users_collection, username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if bcrypt.checkpw(password.encode("utf-8"), user.password.encode('utf-8')):
        # TODO: Implement appropriate token generation using jwt
        return {"access_token": username, "token_type": "bearer"}

    raise HTTPException(status_code=400, detail="Incorrect username or password")


@router.post("/signup")
def signup(username: str = Form(..., description="Unique account username, used for log-in"),
           password: str = Form(..., description="Password")):

    users_collection = conn.get_users_collection()

    if get_user(users_collection, username) is not None:
        raise HTTPException(status_code=400, detail="Username already exists")

    hash_pwd = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    userdb = UserDetailsDB(username=username, password=hash_pwd.decode("utf-8"))

    if create_user(users_collection, userdb):
        return {"username": username}

    raise HTTPException(status_code=500, detail="User creation failed! Please try again later!")
