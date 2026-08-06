from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

from app.logging_config import logger
from app.exceptions.base import AppException


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    def app_exception_handler(request: Request, exc: AppException):

        logger.error(
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