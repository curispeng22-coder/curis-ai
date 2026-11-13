"""Curis Business Runtime —— 统一 API 响应契约（A5）。

本包是「拆单体」的第一步：把原本散落在 ``main.py`` 各处、形如
``JSONResponse({"detail": ...})`` 的跨切面响应逻辑，集中到独立模块。

契约要点（**前端接入前必须定死**，见 A5）：

- 所有新建接口统一返回 ``ApiResponse[T]`` 信封：
  ``{code, message, data, trace_id, timestamp}``，``code==0`` 为成功。
- 业务错误抛 ``BusinessError`` 子类（``NotFoundError`` / ``ConflictError`` /
  ``IllegalTransitionError`` / ``EscalationRequiredError`` …），由
  ``register_exception_handlers`` 统一转成信封，绝不裸抛堆栈。
- 分页统一用 ``Page[T]``。
- 历史遗留接口（返回 ``{"detail": ...}`` 或裸 dict）保持原状，留待后续
  Issue 迁移；本契约只约束 A5 之后新增的 runtime / CEO-day 等接口。

注意：本包**不**覆盖 FastAPI 默认的 ``HTTPException`` / ``RequestValidationError``
处理器，以免改变既有 Workspace UI 的错误响应形状。
"""

from .envelope import ApiResponse, ok, fail
from .pagination import Page, paginate
from .errors import (
    ErrorCode,
    BusinessError,
    ValidationError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    ConflictError,
    IllegalTransitionError,
    EscalationRequiredError,
    DependencyMissingError,
)
from .handlers import register_exception_handlers

__all__ = [
    "ApiResponse",
    "ok",
    "fail",
    "Page",
    "paginate",
    "ErrorCode",
    "BusinessError",
    "ValidationError",
    "UnauthorizedError",
    "ForbiddenError",
    "NotFoundError",
    "ConflictError",
    "IllegalTransitionError",
    "EscalationRequiredError",
    "DependencyMissingError",
    "register_exception_handlers",
]
