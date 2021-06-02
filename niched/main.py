from fastapi import FastAPI

from niched.api.routers.api import router as api_router


def create_app():
    fast_app = FastAPI()

    # Add event handlers or middlewares here

    fast_app.include_router(api_router)
    return fast_app


app = create_app()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}

    