from fastapi import APIRouter

from niched.api.routers import auth, group

router = APIRouter()
router.include_router(auth.router, prefix="/auth")
router.include_router(group.router, prefix="/group")
