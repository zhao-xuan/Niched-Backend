from typing import Optional, List

from pydantic import BaseModel, EmailStr


class UserDetails(BaseModel):
    user_name: str
    email: Optional[EmailStr]
    age: Optional[int]
    subscribed_groups: List[str] = []
    interests: List[str] = []

    class Config:
        schema_extra = {
            "example": {
                "user_name": "gavin-123-456",
                "email": "gavin@gmail.com",
                "age": 50,
                "subscribed_groups": [],
                "interests": [],
            }
        }


class UserToken(BaseModel):
    access_token: str
    token_type: str
    user_details: UserDetails


class UserDetailsDB(UserDetails):
    password: str


class UserDetailsUpdate(BaseModel):
    email: Optional[EmailStr]
    age: Optional[int]
    interests: Optional[List[str]]

    class Config:
        schema_extra = {
            "example": {
                "age": 50,
                "interests": ["badminton", "php", "js"]
            }
        }
