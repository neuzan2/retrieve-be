from fastapi import FastAPI

from src.config.config import settings
from src.config.logging import setup_logging
from src.config.urls import include_router
from src.core.exceptions.handlers import add_exception_handlers
from src.core.middleware.request_id import RequestIdMiddleware


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

    # Add exception handlers
    add_exception_handlers(app)

    # Include API router
    include_router(app=app)

    return app


app = create_app()
