from fastapi import Request
from fastapi.responses import JSONResponse

from app.main import app
from app.logging_config import logger
from app.exceptions.base import AppException


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):

    logger.exception(
        "Exception on %s %s: %s",
        request.method,
        request.url.path,
        exc
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": str(exc)
        }
    )