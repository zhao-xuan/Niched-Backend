from fastapi import APIRouter

from niched.models.schema.users import UserDetails

router = APIRouter()

dummy_db = {
    "leo": {
        "username": "leo",
        "age": 12
    },
    "gavin": {
        "username": "gavin",
        "age": 10
    }
}


@router.get("/{userid}", response_model=UserDetails)
def get_user(userid: str):
    return dummy_db[userid]
