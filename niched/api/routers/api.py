from fastapi import APIRouter

from niched.api.routers import auth, group, event, thread, user, comment

router = APIRouter()
router.include_router(auth.router, prefix="/auth")
router.include_router(group.router, prefix="/group")
router.include_router(thread.router, prefix="/thread")
router.include_router(event.router, prefix="/event")
router.include_router(user.router, prefix="/profile")
router.include_router(comment.router, prefix="/comment")
