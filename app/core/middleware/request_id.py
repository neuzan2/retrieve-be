import uuid
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
import structlog.contextvars


class RequestIdMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add a request ID to each request.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        structlog.contextvars.clear_contextvars()

        request_id = request.headers.get("X-Request-ID")
        if not request_id:
            request_id = f"{uuid.uuid4()}-{uuid.uuid4()}"
        else:
            parts = request_id.split("-")
            if len(parts) > 1:
                request_id = f"{parts[0]}-{uuid.uuid4()}"
            else:
                request_id = f"{request_id}-{uuid.uuid4()}"

        structlog.contextvars.bind_contextvars(request_id=request_id)

        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        return response
