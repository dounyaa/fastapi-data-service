import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response

from app.core.request_context import reset_request_id, set_request_id

REQUEST_ID_HEADER = "X-Request-ID"


async def request_id_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    incoming = request.headers.get(REQUEST_ID_HEADER)
    incoming = (incoming or "").strip()
    request_id = incoming if incoming else uuid.uuid4().hex

    token = set_request_id(request_id)
    request.state.request_id = request_id

    try:
        response = await call_next(request)
    finally:
        reset_request_id(token)

    response.headers[REQUEST_ID_HEADER] = request_id
    return response
