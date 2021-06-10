import logging

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from niched.api.errors.error_handler import validation_error_handler
from niched.api.routers.api import router as api_router

logger = logging.getLogger(__name__)


def create_app():
    fast_app = FastAPI()

    # Add middlewares here
    origins = ["*"]

    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add exception handlers here
    fast_app.add_exception_handler(RequestValidationError, validation_error_handler)

    fast_app.include_router(api_router)
    return fast_app


app = create_app()
