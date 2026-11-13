"""连接器基类（Wave 2 · C1）。

定义 ``ConnectorMode``（mock↔real 切换）与 ``ServiceConnector`` 基类。
所有具体连接器继承此类，保证工作流侧只依赖统一接口。
"""

from __future__ import annotations

import os
from enum import Enum
from typing import Any, Callable


class ConnectorMode(str, Enum):
    """连接器运行模式。

    - ``MOCK``：本地合成与真实端点同构的契约结果，无需 docker / 外部依赖。
    - ``REAL``：经内网 HTTP 调用自托管服务（AITOEARN_URL / SAU_URL）。
    """

    MOCK = "mock"
    REAL = "real"

    @classmethod
    def parse(cls, value: str | None) -> "ConnectorMode":
        normalized = (value or "mock").strip().lower()
        if normalized in ("real", "live", "production"):
            return cls.REAL
        return cls.MOCK


# 运行期模式提供者：由应用层（main.py）注入，读取持久化设置。
# 未注入时退回环境变量 ``CURIS_CONNECTOR_MODE``（缺省 mock）。
# 注意：该 hook 只存在于连接器层，工作流代码仍然完全不感知模式来源。
_MODE_PROVIDER: "Callable[[], str | None] | None" = None


def set_connector_mode_provider(provider: "Callable[[], str | None] | None") -> None:
    """注入模式提供者（返回 ``"mock"``/``"real"``/``None``）。传 ``None`` 撤销注入。"""
    global _MODE_PROVIDER
    _MODE_PROVIDER = provider


def current_connector_mode() -> ConnectorMode:
    """解析当前全局模式：优先注入的提供者，其次环境变量（缺省 mock）。"""
    if _MODE_PROVIDER is not None:
        try:
            resolved = _MODE_PROVIDER()
        except Exception:  # 提供者异常不得阻塞连接器构造
            resolved = None
        if resolved:
            return ConnectorMode.parse(resolved)
    return ConnectorMode.parse(os.getenv("CURIS_CONNECTOR_MODE"))


class ConnectorError(RuntimeError):
    """连接器调用失败：真实端点不可达 / 契约不匹配 / 必需凭证缺失。"""


class ServiceConnector:
    """Curis → 自托管服务的连接器基类。

    mock 模式产出与真实端点同构的契约结果，使工作流代码无需改动即可在
    mock↔real 间切换。具体连接器实现各自的领域方法（如 ``generate`` /
    ``publish``），并共享 ``mode`` 与 ``is_real``。
    """

    # 子类覆盖
    name: str = "base"
    kind: str = "service"
    description: str = ""

    def __init__(self, *, mode: ConnectorMode | None = None) -> None:
        self.mode = mode or current_connector_mode()

    def is_real(self) -> bool:
        return self.mode == ConnectorMode.REAL

    def as_catalog_entry(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "kind": self.kind,
            "description": self.description,
            "mode": self.mode.value,
        }
