import logging
from uuid import uuid4 as uuid

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

logger = logging.getLogger(__name__)


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    def transform_validation_errors(errors: list) -> list:
        details = []

        for err in errors:
            # Extract field name (last element of loc)
            field = err.get("loc", [])[-1]

            # Prefer ctx.error message if available
            ctx = err.get("ctx", {})
            issue = str(ctx.get("error")) if ctx.get("error") else err.get("msg")

            details.append({"field": field, "issue": issue})

        return details

    trace_id = getattr(request.state, "trace_id", str(uuid()))
    details = transform_validation_errors(exc.errors())

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Input validation failed",
                "details": details,
                "trace_id": trace_id,
            }
        },
    )


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("unhandled_exception", exc_info=exc)
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


def add_exception_handlers(app):
    app.add_exception_handler(
        RequestValidationError, request_validation_exception_handler
    )
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
