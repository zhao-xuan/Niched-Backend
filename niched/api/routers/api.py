from fastapi import APIRouter

from niched.api.routers import users

router = APIRouter()
router.include_router(users.router, prefix="/users")
