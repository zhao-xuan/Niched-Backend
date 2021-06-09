import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from niched.main import app

logger = logging.getLogger(__name__)


@app.add_event_handler(RequestValidationError)
def validation_error_handler(request: Request, exc: RequestValidationError):
    logger.error(exc.errors())
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "request": request.json(),
            "error": exc.raw_errors
        }
    )
