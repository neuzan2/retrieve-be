from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.exceptions.handlers import add_exception_handlers
from app.core.logging import setup_logging
from app.core.middleware.request_id import RequestIdMiddleware
from app.core.middleware.tenant_context import TenantContextMiddleware


def create_app() -> FastAPI:
    """
    Create the FastAPI application.
    """
    # Setup logging
    setup_logging()

    # Create FastAPI app
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
    )

    # Add middleware
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(TenantContextMiddleware)

    # Add exception handlers
    add_exception_handlers(app)

    # Include API router
    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
