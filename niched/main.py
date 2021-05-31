from fastapi import FastAPI

from niched.api.routers.api import router as api_router

app = FastAPI()
app.include_router(api_router)