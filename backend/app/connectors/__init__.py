"""Curis 连接器模块（Wave 2 · C1 Connector 真实化）。

把 Curis 编排层连接到自托管的 AiToEarn（生成地基）与 social-auto-upload
（发布执行端）。两段均为本地 docker compose 内网服务，零第三方 SaaS、
零 Relay。

核心约定：
- 每个连接器支持 ``mock`` ↔ ``real`` 两种模式。模式解析优先级：
  应用层注入的提供者（``set_connector_mode_provider``，读持久化设置）
  > 环境变量 ``CURIS_CONNECTOR_MODE=mock|real`` > 缺省 ``mock``；
  真实端点分别取自 ``AITOEARN_URL`` / ``SAU_URL``。
- 工作流代码**只依赖连接器接口**，不感知端点；切真实端点无需改工作流。
- mock 模式产出与真实端点同构的契约结果（ContentPublishPackage / publish 回执），
  用于无 docker 环境下先验证 schema 串联。
"""

from __future__ import annotations

from .base import (
    ConnectorError,
    ConnectorMode,
    ServiceConnector,
    current_connector_mode,
    set_connector_mode_provider,
)
from .registry import (
    ConnectorRegistry,
    get_connector,
    list_connectors,
    register_connector,
    register_defaults,
)
from .aitoearn_client import AiToEarnClient
from .social_auto_upload import SocialAutoUploadConnector

__all__ = [
    "ConnectorError",
    "ConnectorMode",
    "ServiceConnector",
    "current_connector_mode",
    "set_connector_mode_provider",
    "ConnectorRegistry",
    "register_connector",
    "get_connector",
    "list_connectors",
    "register_defaults",
    "AiToEarnClient",
    "SocialAutoUploadConnector",
]


# 导入即注册默认连接器（aitoearn + social_auto_upload），供 workflow_runtime 直接取用。
register_defaults()
