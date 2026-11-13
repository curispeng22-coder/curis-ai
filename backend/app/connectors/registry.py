"""连接器注册表（Wave 2 · C1）。

集中管理已注册的连接器实例；workflow_runtime 通过 ``get_connector(name)``
取用，不必关心端点与模式。模式由连接器自身在构造时从环境变量解析。
"""

from __future__ import annotations

from typing import Dict

from .aitoearn_client import AiToEarnClient
from .base import ServiceConnector
from .social_auto_upload import SocialAutoUploadConnector


_REGISTRY: Dict[str, ServiceConnector] = {}


def register_connector(connector: ServiceConnector) -> None:
    """注册（或覆盖）一个连接器实例。"""
    _REGISTRY[connector.name] = connector


def get_connector(name: str) -> ServiceConnector:
    """按名字取用连接器；未注册抛 KeyError。"""
    connector = _REGISTRY.get(name)
    if connector is None:
        raise KeyError(f"connector {name!r} is not registered")
    return connector


def list_connectors() -> list[dict]:
    """列出所有已注册连接器的目录条目（不含任何凭证）。"""
    return [c.as_catalog_entry() for c in _REGISTRY.values()]


def register_defaults() -> None:
    """注册 Wave 2 默认连接器集合（幂等，可重复调用）。"""
    register_connector(AiToEarnClient())
    register_connector(SocialAutoUploadConnector())


# 兼容旧命名的轻量别名（避免 workflow_runtime 侧改动）。
ConnectorRegistry = type("ConnectorRegistry", (), {"get": get_connector, "list": list_connectors})
