from __future__ import annotations

import hashlib
from typing import Any

from .database import Database
from .model_gateway import redact_model_gateway_text
from .tenant_context import TenantContext


class TenantModelPreferenceResolver:
    """Tenant-scoped default preference over verified model metadata."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def professional_grant(self, configured, company, workspace, model_key, *, attempt_id=None, connection=None):
        if configured is not None:
            return configured  # Explicit server composition, including controlled offline fixtures.
        from .company_execution_policy import CompanyExecutionPolicy
        return CompanyExecutionPolicy(self.database).current_grant(company, workspace, model_key, attempt_id=attempt_id, connection=connection)

    def require_professional_grant(self, grant, company, workspace, model_key, *, attempt_id=None):
        """Validate the existing server-owned bounded grant; never manufacture one."""
        import math
        import json
        from .runtime import RuntimeScopeError
        tenant = TenantContext.current_tenant_id()
        if (not isinstance(grant, dict) or grant.get("tenant_id") != tenant
                or grant.get("company_id") != company or grant.get("workspace_id") != workspace
                or grant.get("model_key") != model_key or not grant.get("grant_ref")
                or grant.get("effective_system_authorization") is not True
                or type(grant.get("max_input_bytes")) is not int or not 1 <= grant["max_input_bytes"] <= 50000
                or type(grant.get("max_output_tokens")) is not int or not 1 <= grant["max_output_tokens"] <= 2048
                or not grant.get("price_version") or any(type(grant.get(k)) not in {int, float}
                    or not math.isfinite(grant[k]) or grant[k] < 0 for k in
                    ("max_cost_usd", "price_upper_bound_usd_per_input_byte", "price_upper_bound_usd_per_output_token"))):
            raise RuntimeScopeError("当前专业员工回复尚无可验证的费用与系统授权；输入已保留。")
        self._require_eligible_model(tenant, model_key)
        with self.database.connect() as con:
            rows = con.execute("select payload from evolution_events where tenant_id=? and event_type='conversation.execution_bound' "
                "and json_extract(payload,'$.execution_selection.grant.grant_ref')=?",
                (tenant, grant["grant_ref"])).fetchall()
        if any(json.loads(row[0]).get("attempt_id") != attempt_id for row in rows):
            raise RuntimeScopeError("原专业回复授权已使用，请先查询原请求。")
        return dict(grant)

    def prepare_employee_model(self, company, workspace, employee_ref, model_key, grant):
        """An explicit send may resolve an internal binding only after real authorization."""
        from .employee_execution_identity import EmployeeExecutionIdentity
        from .employee_templates import EmployeeTemplateContract
        self.require_professional_grant(grant, company, workspace, model_key)
        model = self._require_eligible_model(TenantContext.current_tenant_id(), model_key)
        identities = EmployeeExecutionIdentity(self.database)
        identity = identities.resolve(company_id=company, workspace_id=workspace, runtime_employee_ref=employee_ref)
        employee = identity["company_employee_ref"]
        service = EmployeeTemplateContract(self.database)
        bindings = service.list_employee_capability_bindings(employee)["bindings"]
        matches = [b for b in bindings if b["enabled"] and b["capability_type"] == "model"
                   and b["capability_source"] == model["source"] and b["capability_id"] == model_key]
        if not matches:
            bindings = service.set_employee_capability_bindings(employee, [*bindings,
                {"capability_source": model["source"], "capability_type": "model", "capability_id": model_key,
                 "enabled": True, "priority": 1}])["bindings"]
            matches = [b for b in bindings if b["enabled"] and b["capability_type"] == "model"
                       and b["capability_source"] == model["source"] and b["capability_id"] == model_key]
        if len(matches) != 1:
            raise ValueError("所选模型没有唯一可验证的内部执行绑定。")
        if identity["identity_status"] != "VERIFIED_EXPLICIT_BRIDGE" or (identity.get("bridge") or {}).get("status") != "VERIFIED":
            identities.bind(company_id=company, workspace_id=workspace, runtime_employee_ref=employee_ref,
                            company_employee_ref=employee, employee_capability_binding_ref=matches[0]["id"])
        return matches[0]

    def read_current(self) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        return {
            "preference": self._validated_preference(tenant_id),
            "available_models": self.available_models(),
        }

    def set_current(self, model_key: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        model = self._require_eligible_model(tenant_id, model_key)
        preference = {
            "tenant_id": tenant_id,
            "model_key": model_key,
            "gateway_ref": model["gateway_ref"],
            "model_name": model["model_name"],
            "source": model["source"],
        }
        self._require_metadata_only(preference)
        self.database.save_tenant_model_preference(**preference)
        return self.read_current()

    def clear_current(self) -> dict[str, Any]:
        self.database.delete_tenant_model_preference(TenantContext.current_tenant_id())
        return self.read_current()

    def resolve_runtime_model(self) -> dict[str, str] | None:
        preference = self._validated_preference(TenantContext.current_tenant_id())
        if preference is None:
            return None
        return {
            "gateway_id": preference["gateway_ref"],
            "model_name": preference["model_name"],
            "source": preference["source"],
            "capability_id": preference["model_key"],
        }

    def available_models(self) -> list[dict[str, Any]]:
        tenant_id = TenantContext.current_tenant_id()
        models = []
        for model in self.database.list_all_official_models(include_inactive=False):
            if (
                model.get("source") != "official"
                or model.get("gateway_ref") == "freellmapi.experimental"
            ):
                continue
            model_name = self._model_name(model)
            if not model_name:
                continue
            models.append(
                {
                    "model_key": model["model_key"],
                    "provider_id": model["provider_id"],
                    "display_name": model["display_name"],
                    "gateway_ref": model["gateway_ref"],
                    "model_name": model_name,
                    "source": model["source"],
                    "status": model["status"],
                    "updated_at": model["updated_at"],
                }
            )
        for capability in self.database.list_tenant_private_capabilities(
            tenant_id, capability_type="model", include_inactive=True
        ):
            model = self._eligible_private_model(tenant_id, capability["capability_id"])
            if model is not None:
                models.append(model)
        return models

    def _validated_preference(self, tenant_id: str) -> dict[str, Any] | None:
        row = self.database.get_tenant_model_preference(tenant_id)
        if row is None:
            return None
        model = self._eligible_model(tenant_id, row["model_key"])
        if model is None:
            return None
        if (
            row["gateway_ref"] != model["gateway_ref"]
            or row["model_name"] != model["model_name"]
            or row["source"] != model["source"]
        ):
            return None
        return row

    def _require_eligible_model(self, tenant_id: str, model_key: str) -> dict[str, Any]:
        model = self._eligible_model(tenant_id, model_key)
        if model is None:
            raise ValueError("model_key must reference an eligible model for this tenant")
        return model

    def _eligible_model(self, tenant_id: str, model_key: str) -> dict[str, Any] | None:
        official = self.database.get_active_official_model(model_key)
        if official is not None:
            model_name = self._model_name(official)
            if not model_name:
                return None
            return {
                "model_key": official["model_key"],
                "provider_id": official["provider_id"],
                "display_name": official["display_name"],
                "gateway_ref": official["gateway_ref"],
                "model_name": model_name,
                "source": "official",
                "status": official["status"],
                "updated_at": official["updated_at"],
            }
        return self._eligible_private_model(tenant_id, model_key)

    def _eligible_private_model(
        self, tenant_id: str, model_key: str
    ) -> dict[str, Any] | None:
        capability = self.database.get_tenant_private_capability(
            tenant_id, "model", model_key
        )
        if capability is None or capability.get("status") != "active":
            return None
        metadata = capability.get("metadata") or {}
        provider_id = str(metadata.get("provider_type") or "")
        model_name = str(metadata.get("model_name") or "")
        verification = metadata.get("discovery_verification") or {}
        discovery_id = str(verification.get("discovery_id") or model_name)
        expected_key = (
            f"user.{provider_id}."
            f"{hashlib.sha256(discovery_id.encode('utf-8')).hexdigest()[:16]}"
        )
        if (
            not provider_id
            or not model_name
            or model_key != expected_key
            or verification.get("status") != "verified"
            or verification.get("provider_id") != provider_id
            or verification.get("model_id") != model_name
        ):
            return None
        if verification.get("requires_credential"):
            credential_ref = str(metadata.get("credential_ref") or "")
            credential = next(
                (
                    item
                    for item in self.database.list_credential_metadata(tenant_id)
                    if item.get("credential_ref") == credential_ref
                ),
                None,
            )
            if (
                credential is None
                or credential.get("status") != "active"
                or credential.get("provider") != provider_id
            ):
                return None
        return {
            "model_key": model_key,
            "provider_id": provider_id,
            "display_name": capability.get("display_name") or model_name,
            "gateway_ref": provider_id,
            "model_name": model_name,
            "source": "tenant_private",
            "status": capability["status"],
            "updated_at": capability["updated_at"],
        }

    def _model_name(self, model: dict[str, Any]) -> str:
        if model.get("default_model"):
            return str(model["default_model"])
        supported_models = model.get("supported_models") or []
        if supported_models:
            return str(supported_models[0])
        return ""

    def _require_metadata_only(self, preference: dict[str, Any]) -> None:
        for key, value in preference.items():
            if redact_model_gateway_text(value) != str(value):
                raise ValueError(f"{key} must not contain secret-like material")
