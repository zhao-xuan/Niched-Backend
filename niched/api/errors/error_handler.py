import logging

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


logger = logging.getLogger(__name__)


def validation_error_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Request: {request}, \n Errors captured: {exc.errors()}")
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            "detail": exc.errors()[0]
        })
    )
