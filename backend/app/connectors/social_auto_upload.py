"""social-auto-upload 连接器（Wave 2 · C1 / D2）。

自托管 social-auto-upload MIT 作为发布执行端（patchright 浏览器自动化），
覆盖抖音/小红书/视频号/B站/快手/TikTok/YouTube 等。Curis 工作流在「发布」步
调用本连接器，把 ContentPublishPackage 推送到指定平台。

模式：
- ``mock``：本地模拟发布成功，返回与真实端点同构的回执（无需 docker）。
- ``real``：经内网 HTTP POST 到 ``SAU_URL``（默认 http://localhost:8090）的
  ``/api/publish``；per-platform cookie 来自 Vault，由编排层解析后注入，
  **不注册任何平台原生 OAuth App**（cookie 登录即最小感知路径）。

设计红线：创始人自有 cookie 仅来自 local-dev Vault，绝不写入代码/DB；
零第三方 SaaS；仅发布执行，不触 Relay。
"""

from __future__ import annotations

import os
from typing import Any

from .base import ConnectorError, ServiceConnector
from ..content_publish_package import ContentPublishPackage


class SocialAutoUploadConnector(ServiceConnector):
    name = "social_auto_upload"
    kind = "publisher"
    description = "自托管 social-auto-upload（MIT）：patchright 浏览器真实发布。"

    def __init__(self, *, mode=None, base_url: str | None = None) -> None:
        super().__init__(mode=mode)
        self.base_url = (base_url or os.getenv("SAU_URL", "http://localhost:8090")).rstrip("/")

    def publish(
        self,
        package: ContentPublishPackage,
        *,
        platform: str,
        cookie: str | None = None,
        account: str = "founder",
    ) -> dict[str, Any]:
        """把发布包推送到指定平台；返回发布回执（契约统一格式）。

        ``cookie`` 为创始人该平台的 cookie（Vault 解析后的明文，仅本次请求使用）。
        缺失 cookie 在 mock 模式可降级（仅记录告警），real 模式则报错。
        """
        if self.is_real():
            return self._publish_real(package, platform=platform, cookie=cookie, account=account)
        return self._publish_mock(package, platform=platform, cookie=cookie)

    # ── mock ─────────────────────────────────────────────────────
    def _publish_mock(self, package: ContentPublishPackage, *, platform: str, cookie: str | None) -> dict[str, Any]:
        cookie_note = "ok" if cookie else "no-cookie(mocked)"
        return {
            "connector": self.name,
            "mode": "mock",
            "status": "published",
            "platform": platform,
            "package_id": package.package_id,
            "post_id": f"mock-{platform}-{package.package_id[:8]}",
            "message": f"[mock] 已模拟发布到 {platform}；cookie={cookie_note}",
            "artifacts": len(package.artifacts),
        }

    # ── real ────────────────────────────────────────────────────
    def _publish_real(
        self,
        package: ContentPublishPackage,
        *,
        platform: str,
        cookie: str | None,
        account: str,
    ) -> dict[str, Any]:
        if not cookie:
            raise ConnectorError(f"真实发布到 {platform} 缺少 cookie（应从 Vault 解析）")
        try:
            import requests
        except ImportError as error:  # pragma: no cover
            raise ConnectorError("requests 不可用，无法调用真实 social-auto-upload 端点") from error

        url = f"{self.base_url}/api/publish"
        payload: dict[str, Any] = {
            "platform": platform,
            "account": account,
            "cookie": cookie,
            "package": package.to_dict(),
        }
        try:
            resp = requests.post(url, json=payload, timeout=180)
            resp.raise_for_status()
            data = resp.json()
        except Exception as error:  # noqa: BLE001
            raise ConnectorError(f"social-auto-upload 真实端点调用失败：{error}") from error
        return {
            "connector": self.name,
            "mode": "real",
            "status": data.get("status", "published"),
            "platform": platform,
            "package_id": package.package_id,
            "post_id": data.get("post_id", ""),
            "message": data.get("message", ""),
        }
