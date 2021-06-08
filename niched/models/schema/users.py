from typing import Optional, List

from pydantic import BaseModel, EmailStr


class UserToken(BaseModel):
    access_token: str
    token_type: str


class UserDetails(BaseModel):
    user_name: str
    mail: Optional[EmailStr]
    age: Optional[int]
    subscribed_groups: List[str] = []
    interests: List[str] = []

    class Config:
        schema_extra = {
            "example": {
                "username": "gavin-123-456",
                "age": 50
            }
        }


class UserDetailsDB(UserDetails):
    password: str


class UserDetailsUpdate(BaseModel):
    mail: Optional[EmailStr]
    age: Optional[int]
    subscribed_groups: Optional[List[str]]
    interests: Optional[List[str]]

    class Config:
        schema_extra = {
            "example": {
                "age": 50,
                "subscribed_groups": ["ramen", "csgo"],
                "interests": ["badminton", "php", "js"]
            }
        }
