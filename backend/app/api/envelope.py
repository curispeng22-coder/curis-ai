"""统一响应信封（A5 契约核心）。

所有 A5 之后新增接口的成功响应都包成 ``ApiResponse[T]``：

.. code-block:: json

    {
      "code": 0,
      "message": "ok",
      "data": { ... },
      "trace_id": "a1b2c3d4",
      "timestamp": "2026-08-03T18:30:21+08:00"
    }

错误响应由 ``handlers.register_exception_handlers`` 把 ``BusinessError``
转成同一信封（``code != 0``）。
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _gen_trace_id() -> str:
    return uuid.uuid4().hex[:16]


class ApiResponse(BaseModel, Generic[T]):
    """统一响应信封。"""

    code: int = 0
    message: str = "ok"
    data: Optional[T] = None
    trace_id: Optional[str] = Field(default_factory=_gen_trace_id)
    timestamp: str = Field(default_factory=_now_iso)

    @classmethod
    def build(
        cls,
        *,
        code: int = 0,
        message: str = "ok",
        data: Optional[T] = None,
    ) -> "ApiResponse[T]":
        return cls(code=code, message=message, data=data)


def ok(data: Optional[T] = None, message: str = "ok") -> ApiResponse[T]:
    """成功响应。"""
    return ApiResponse.build(code=0, message=message, data=data)


def fail(code: int, message: str, data: Optional[T] = None) -> ApiResponse[T]:
    """失败响应（业务错误统一走 ``BusinessError``，此处用于显式构造）。"""
    return ApiResponse.build(code=code, message=message, data=data)
