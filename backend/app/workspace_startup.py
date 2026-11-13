from __future__ import annotations

import json
import sys


def _emit(signal: dict[str, str]) -> None:
    print(json.dumps(signal, separators=(",", ":"), sort_keys=True), file=sys.stderr)


def _load_workspace_app():
    import uvicorn

    from .main import app

    return uvicorn, app


def main() -> int:
    try:
        uvicorn, app = _load_workspace_app()
    except SystemExit:
        raise
    except ImportError:
        _emit(
            {
                "failed_stage": "module_import",
                "failure_signal": "import_exception",
                "failure_code": "import_failed",
            }
        )
        return 1
    except Exception:
        _emit({"failure_code": "unknown"})
        return 1

    try:
        uvicorn.run(app, host="0.0.0.0", port=8002)
    except SystemExit:
        raise
    except Exception:
        _emit({"failure_code": "unknown"})
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
