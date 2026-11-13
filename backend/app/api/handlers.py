"""统一异常处理（A5 契约装配）。

把 ``BusinessError`` 与未捕获异常转成 ``ApiResponse`` 信封。**不**覆盖
FastAPI 默认的 ``HTTPException`` / ``RequestValidationError`` 处理器，以保留
既有 Workspace UI 的错误响应形状。

在 ``create_app`` 末尾调用 ``register_exception_handlers(app)`` 即可生效。
"""

from __future__ import annotations

import logging
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .envelope import ApiResponse, fail
from .errors import BusinessError, ErrorCode

logger = logging.getLogger("curis.api")


def _trace_id(request: Request) -> str:
    return request.headers.get("X-Request-Id") or uuid.uuid4().hex[:16]


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(BusinessError)
    async def _business(request: Request, exc: BusinessError) -> JSONResponse:
        body = exc.to_response(_trace_id(request)).model_dump()
        return JSONResponse(status_code=exc.http_status, content=body)

    @app.exception_handler(Exception)
    async def _unexpected(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("未处理的异常：%s", exc)
        body = fail(
            ErrorCode.INTERNAL, "服务器内部错误"
        ).model_copy(update={"trace_id": _trace_id(request)}).model_dump()
        return JSONResponse(status_code=500, content=body)
