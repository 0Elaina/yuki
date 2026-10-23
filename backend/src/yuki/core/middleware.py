import logging
from contextvars import Token
from time import perf_counter
from uuid import uuid4

from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from yuki.infra.logging import request_id_var

logger = logging.getLogger(__name__)


class RequestContextMiddleware:
    """请求上下文中间件"""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id: str = uuid4().hex
        started_at: float = perf_counter()
        status_code: int | None = None
        scope.setdefault("state", {})["request_id"] = request_id

        async def send_with_request_id(message: Message) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
                headers = MutableHeaders(scope=message)
                headers["X-Request-ID"] = request_id
            await send(message)

        token: Token[str] = request_id_var.set(request_id)
        try:
            await self.app(scope, receive, send_with_request_id)
        except Exception:
            if status_code is None:
                status_code = 500
            raise
        finally:
            duration_ms = (perf_counter() - started_at) * 1000
            request_id_var.reset(token)
            logger.info(
                "请求处理结束 method=%s path=%s status_code=%s duration_ms=%.2f",
                scope["method"],
                scope["path"],
                status_code if status_code is not None else "-",
                duration_ms,
                extra={"request_id": request_id},
            )
