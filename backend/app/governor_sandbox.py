from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any


class GovernorSandbox:
    """Throwaway-copy sandbox for demonstrating a controlled governor proposal.

    The sandbox copies a snapshot of the current state to a throwaway directory
    (OS temp, never the project/repo), applies a proposal there, captures
    apply + rollback evidence, and rolls the throwaway copy back exactly. It
    NEVER writes to the authoritative repo or SQLite. Any real production
    mutation remains gated behind an explicit human-approval path outside this
    sandbox (unchanged by this module).
    """

    def __init__(self, state_snapshot: dict[str, Any] | None = None):
        self.state_snapshot = dict(state_snapshot or {})

    def run(self, proposal: dict[str, Any], *, dry_run: bool = True) -> dict[str, Any]:
        throwaway = Path(tempfile.mkdtemp(prefix="curis-sandbox-"))
        snapshot_path = throwaway / "state_snapshot.json"
        applied_path = throwaway / "state_applied.json"
        evidence_path = throwaway / "evidence.json"
        rollback_path = throwaway / "state_rolledback.json"

        snapshot = dict(self.state_snapshot)
        snapshot_path.write_text(
            json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        applied = self._apply_proposal(snapshot, proposal)
        applied_path.write_text(
            json.dumps(applied, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        evidence = {
            "dry_run": dry_run,
            "proposal": proposal,
            "throwaway_path": str(throwaway),
            "applied_state": applied,
            "rollback_snapshot": snapshot,
        }
        evidence_path.write_text(
            json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        # Rollback: restore the throwaway copy exactly to the original snapshot.
        rollback_path.write_text(
            json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        return {
            "dry_run": dry_run,
            "throwaway_path": str(throwaway),
            "applied_state": applied,
            "rollback_snapshot": snapshot,
            "evidence_path": str(evidence_path),
            "rolled_back": True,
        }

    @staticmethod
    def _apply_proposal(snapshot: dict[str, Any], proposal: dict[str, Any]) -> dict[str, Any]:
        applied = dict(snapshot)
        applied["_sandbox_proposal"] = {
            "proposal_type": proposal.get("proposal_type"),
            "target_module": proposal.get("target_module"),
            "change_summary": proposal.get("change_summary"),
            "applied_in_sandbox": True,
        }
        return applied
