from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class TenantContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware to extract tenant information from request headers.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        client_id = request.headers.get("X-Client-ID")
        project_id = request.headers.get("X-Project-ID")

        request.state.client_id = client_id
        request.state.project_id = project_id

        response = await call_next(request)
        return response
