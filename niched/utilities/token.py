import logging
from datetime import datetime, timedelta
from typing import Union, List

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, PyJWTError
from starlette.status import HTTP_401_UNAUTHORIZED

from niched.core.config import ACCESS_TOKEN_ALGORITHM, ACCESS_TOKEN_SECRET_KEY
from niched.database.mongo import conn
from niched.database.user_utils import get_user_profile
from niched.models.schema.users import UserDetails

logger = logging.getLogger(__name__)


class TokenException(Exception):
    """Base class for exceptions in token"""


class ExpiredTokenException(TokenException):
    """Exception thrown when token has expired """


class InvalidTokenValue(TokenException):
    """Invalid value in token"""


def create_access_token(user_details: UserDetails, expiration_mins: int, secret_key: Union[str, bytes],
                        algorithm: str = ACCESS_TOKEN_ALGORITHM) -> str:
    expiration = datetime.now() + timedelta(minutes=expiration_mins)
    data = {
        "sub": user_details.user_name,
        "exp": expiration
    }
    return jwt.encode(data, secret_key, algorithm=algorithm)


def check_token_valid(token: str) -> bool:
    try:
        jwt.decode(token)
        return True
    except ExpiredSignatureError:
        return False


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_active_user(token: str = Depends(oauth2_scheme)) -> UserDetails:
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM])
        exp = payload.get("exp")
        if exp is None:
            raise credentials_exception
        if exp < datetime.now().timestamp():
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Session has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        username = payload.get("sub")
        if username is None:
            raise credentials_exception

    except PyJWTError as e:
        logger.debug(f"JWT failed to decode token, exception raised {e}")
        raise credentials_exception

    users_collection = conn.get_users_collection()
    user = get_user_profile(users_collection, username)
    if user is None:
        raise credentials_exception

    return user
