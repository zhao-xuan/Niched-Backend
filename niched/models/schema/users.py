from typing import Optional

from pydantic import BaseModel


class UserDetails(BaseModel):
    username: str
    age: Optional[int]
