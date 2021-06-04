from typing import Optional

from pydantic import BaseModel


class UserToken(BaseModel):
    access_token: str
    token_type: str


class UserDetails(BaseModel):
    username: str
    age: Optional[int]


class UserDetailsDB(UserDetails):
    password: str
