from fastapi import APIRouter

from niched.api.routers import auth, group, thread, events

router = APIRouter()
router.include_router(auth.router, prefix="/auth")
router.include_router(group.router, prefix="/group")
router.include_router(thread.router, prefix="/thread")
router.include_router(events.router, prefix="/events")