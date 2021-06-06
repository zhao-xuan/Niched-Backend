from typing import Optional

from pydantic import BaseModel


class UserToken(BaseModel):
    access_token: str
    token_type: str


class UserDetails(BaseModel):
    username: str
    age: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "username": "gavin-123-456",
                "age": 50
            }
        }


class UserDetailsDB(UserDetails):
    password: str
