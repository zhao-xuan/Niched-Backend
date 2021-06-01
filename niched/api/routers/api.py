from fastapi import APIRouter

from niched.api.routers import auth

router = APIRouter()
router.include_router(auth.router, prefix="/auth")
