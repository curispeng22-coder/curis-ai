"""业务错误码与异常（A5 契约）。

新建接口**不要**直接 ``raise HTTPException``，而是抛对应的
``BusinessError`` 子类；``handlers.register_exception_handlers`` 会把它转成
统一的 ``ApiResponse`` 信封（``code != 0``），并带上 ``http_status``。

错误码命名空间（与常见 HTTP 语义对齐，便于前端映射）：

- ``400xx`` 客户端/参数
- ``401xx`` 未认证
- ``403xx`` 无权限/越界
- ``404xx`` 资源不存在
- ``409xx`` 冲突 / 非法状态机流转
- ``424xx`` 依赖缺失（如未授权导致无法继续）
- ``428xx`` 需要 CEO 介入（升级契约）
- ``429xx`` 限流
- ``500xx`` 服务器内部
"""

from __future__ import annotations

from typing import Any, Optional

from .envelope import ApiResponse, fail


class ErrorCode:
    OK = 0
    BAD_REQUEST = 40000
    VALIDATION = 42200
    UNAUTHORIZED = 40100
    FORBIDDEN = 40300
    NOT_FOUND = 40400
    CONFLICT = 40900
    ILLEGAL_TRANSITION = 40910
    DEPENDENCY_MISSING = 42400
    ESCALATION_REQUIRED = 42800
    RATE_LIMITED = 42900
    INTERNAL = 50000


class BusinessError(Exception):
    """所有业务错误的基类。"""

    code: int = ErrorCode.INTERNAL
    http_status: int = 500

    def __init__(
        self,
        message: str,
        *,
        code: Optional[int] = None,
        http_status: Optional[int] = None,
        data: Optional[Any] = None,
    ) -> None:
        self.message = message
        self.code = code if code is not None else self.code
        self.http_status = http_status if http_status is not None else self.http_status
        self.data = data
        super().__init__(message)

    def to_response(self, trace_id: Optional[str] = None) -> ApiResponse:
        return fail(self.code, self.message, self.data).model_copy(
            update={"trace_id": trace_id} if trace_id else {}
        )


class ValidationError(BusinessError):
    code = ErrorCode.VALIDATION
    http_status = 422


class UnauthorizedError(BusinessError):
    code = ErrorCode.UNAUTHORIZED
    http_status = 401


class ForbiddenError(BusinessError):
    code = ErrorCode.FORBIDDEN
    http_status = 403


class NotFoundError(BusinessError):
    code = ErrorCode.NOT_FOUND
    http_status = 404


class ConflictError(BusinessError):
    code = ErrorCode.CONFLICT
    http_status = 409


class IllegalTransitionError(BusinessError):
    code = ErrorCode.ILLEGAL_TRANSITION
    http_status = 409


class DependencyMissingError(BusinessError):
    code = ErrorCode.DEPENDENCY_MISSING
    http_status = 424


class EscalationRequiredError(BusinessError):
    code = ErrorCode.ESCALATION_REQUIRED
    http_status = 428
