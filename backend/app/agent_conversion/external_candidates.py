"""人才市场公开专家 Candidate 投影。"""

from __future__ import annotations

from typing import Any

from .production_line import scan_local_resource_pool


def list_external_candidates() -> list[dict[str, Any]]:
    """返回生产线扫描后的 Agent Candidate；不写库、不自动招募。"""
    return [
        item
        for item in scan_local_resource_pool()["resources"]
        if item["resource_type"] == "agent"
    ]
