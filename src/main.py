from fastapi import FastAPI

from src.core.exceptions.handlers import add_exception_handlers
from src.core.middleware.request_id import RequestIdMiddleware
from src.core.middleware.tenant_context import TenantContextMiddleware
from src.config.config import settings
from src.config.logging import setup_logging


def create_app() -> FastAPI:
    """
    Create the FastAPI application.
    """
    # Setup logging
    setup_logging()

    # Create FastAPI app
    app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, debug=settings.DEBUG, )

    # Add middleware
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(TenantContextMiddleware)

    # Add exception handlers
    add_exception_handlers(app)

    # Include API router
    # app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
