"""Reference legacy executors without importing their lifecycle into Foundation."""

from __future__ import annotations

from .foundation import RuntimeFoundation


ALLOWED_EXECUTION_TYPES = frozenset({"workflow_run", "workflow_step", "content_workflow_run"})


class LegacyExecutionAdapter:
    def __init__(self, foundation: RuntimeFoundation):
        self.foundation = foundation

    def attach(self, entity_id: str, *, execution_type: str, execution_id: str, legacy_status: str = "") -> dict:
        if execution_type not in ALLOWED_EXECUTION_TYPES:
            raise ValueError(f"unsupported legacy execution type: {execution_type}")
        before = self.foundation.get(entity_id)
        result = self.foundation.attach_execution_ref(
            entity_id,
            f"{execution_type}:{execution_id}",
            {"legacyExecutionStatus": legacy_status} if legacy_status else {},
        )
        if result["lifecycle_status"] != before["lifecycle_status"]:
            raise RuntimeError("legacy execution status changed Foundation lifecycle")
        return result
