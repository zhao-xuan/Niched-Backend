from fastapi import FastAPI

from niched.api.routers.api import router as api_router
from fastapi.middleware.cors import CORSMiddleware


def create_app():
    fast_app = FastAPI()

    origins = ["*"]

    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add event handlers or middlewares here

    fast_app.include_router(api_router)
    return fast_app


app = create_app()

    
