#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    checks = [
        _path("backend app", ROOT / "backend" / "app" / "main.py"),
        _path("backend venv python", ROOT / "backend" / ".venv" / "bin" / "python"),
        _path("frontend package", ROOT / "frontend" / "package.json"),
        _path("frontend node_modules", ROOT / "frontend" / "node_modules"),
        _path("phase7 seed", ROOT / "docs" / "demo" / "phase7-demo-seed.json"),
        _path("phase7 e2e", ROOT / "tools" / "phase7_stable_demo_e2e.py"),
        _command("node"),
        _command("npm"),
        _command("rg"),
    ]
    ok = all(item["ok"] for item in checks)
    print(json.dumps({"ok": ok, "checks": checks}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


def _path(name: str, path: Path) -> dict[str, object]:
    return {"name": name, "type": "path", "target": str(path), "ok": path.exists()}


def _command(name: str) -> dict[str, object]:
    path = shutil.which(name)
    version = None
    if path:
        try:
            result = subprocess.run([name, "--version"], check=False, capture_output=True, text=True, timeout=5)
            version = (result.stdout or result.stderr).strip().splitlines()[0] if (result.stdout or result.stderr).strip() else None
        except Exception as error:  # pragma: no cover - environment diagnostics only
            version = f"version check failed: {error}"
    return {"name": name, "type": "command", "target": path, "version": version, "ok": bool(path)}


if __name__ == "__main__":
    raise SystemExit(main())
