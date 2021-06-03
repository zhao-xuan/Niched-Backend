from fastapi import APIRouter

from niched.api.routers import auth, groupRouter

router = APIRouter()
router.include_router(auth.router, prefix="/auth")
router.include_router(groupRouter.router, prefix="/group")
