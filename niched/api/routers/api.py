from fastapi import APIRouter

from niched.api.routers import auth, groupRouter, threadRouter

router = APIRouter()
router.include_router(auth.router, prefix="/auth")
router.include_router(groupRouter.router, prefix="/group")
router.include_router(threadRouter.router, prefix="/thread")
