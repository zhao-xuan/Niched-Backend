from fastapi import FastAPI

from niched.api.routers.api import router as api_router
from niched.database.mongo import db_connect, db_terminate


def create_app():
    fast_app = FastAPI()

    fast_app.add_event_handler("startup", db_connect)
    fast_app.add_event_handler("shutdown", db_terminate)

    fast_app.include_router(api_router)
    return fast_app


app = create_app()
