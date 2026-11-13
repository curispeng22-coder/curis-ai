from __future__ import annotations

import importlib.util
from pathlib import Path


def test_packaged_gateway_waits_for_bounded_provider_retry_window(monkeypatch):
    monkeypatch.delenv("CURIS_GATEWAY_UPSTREAM_TIMEOUT_SECONDS", raising=False)
    path = Path(__file__).resolve().parents[2] / "desktop" / "runtime" / "gateway.py"
    spec = importlib.util.spec_from_file_location("curis_desktop_gateway_continuity", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    assert module.UPSTREAM_TIMEOUT_SECONDS == 135
    assert module.UPSTREAM_TIMEOUT_SECONDS > 2 * 60
