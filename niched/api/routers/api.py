from fastapi import APIRouter

from niched.api.routers import auth, group, user

router = APIRouter()
router.include_router(auth.router, prefix="/auth")
router.include_router(group.router, prefix="/group")
router.include_router(user.router, prefix="/profile")
