"""Coze 外部 Agent 的最小安全适配契约。

只保存外部引用和不透明 credential_ref；真实请求由已授权的 transport 注入，
本模块不复制 Prompt/Knowledge/Credential，也不自行发起网络请求。
"""

from __future__ import annotations

from typing import Any, Callable

from ..catalog_constants import is_valid_credential_ref


class CozeAdapter:
    name = "coze"

    @staticmethod
    def binding(external_ref: str, credential_ref: str) -> dict[str, str]:
        external_ref = str(external_ref or "").strip()
        credential_ref = str(credential_ref or "").strip()
        if not external_ref:
            raise ValueError("Coze external_ref is required")
        if not is_valid_credential_ref(credential_ref):
            raise ValueError("Coze credential_ref must be an opaque env/kms/vault reference")
        return {
            "adapter": CozeAdapter.name,
            "external_ref": external_ref,
            "credential_ref": credential_ref,
        }

    @staticmethod
    def normalize_response(payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "status": str(payload.get("status") or "unknown"),
            "output": payload.get("output"),
            "evidence": payload.get("evidence") or {},
            "usage": payload.get("usage") or {},
        }

    def invoke(
        self,
        binding: dict[str, str],
        prompt: str,
        transport: Callable[[str, str, str], dict[str, Any]],
    ) -> dict[str, Any]:
        checked = self.binding(binding.get("external_ref", ""), binding.get("credential_ref", ""))
        return self.normalize_response(transport(checked["external_ref"], checked["credential_ref"], prompt))
