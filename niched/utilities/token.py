from datetime import datetime, timedelta
from typing import Union

import jwt
from jwt import ExpiredSignatureError

from niched.database.authentication import get_user_login_details
from niched.database.mongo import conn
from niched.models.schema.users import UserDetails


class TokenException(Exception):
    """Base class for exceptions in token"""


class ExpiredTokenException(TokenException):
    """Exception thrown when token has expired """


class InvalidTokenValue(TokenException):
    """Invalid value in token"""


def create_access_token(user_details: UserDetails, expiration_mins: int, secret_key: Union[str, bytes]) -> str:
    expiration = datetime.utcnow() + timedelta(minutes=expiration_mins)
    data = {
        "sub": user_details.user_name,
        "exp": expiration
    }
    return jwt.encode(data, secret_key)


def check_token_valid(token: str) -> bool:
    try:
        jwt.decode(token)
        return True
    except ExpiredSignatureError:
        return False


def get_user_details_from_token(token: str) -> UserDetails:
    username = jwt.decode(token).get("sub")

    users_collection = conn.get_users_collection()
    user_details = get_user_login_details(users_collection, username)
    if user_details is None:
        raise InvalidTokenValue("Invalid username in token")

    return user_details
