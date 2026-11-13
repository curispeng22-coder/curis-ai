"""Wave-1 验收：验证项 6（前端 CEO Office 页面语法检查）。

运行方式（在 backend/ 目录下，使用项目 .venv）：
    ../.venv/bin/python -m pytest tests/test_v1_wave1_frontend.py -v

用 esbuild（JSX loader）对 ``frontend/app/ceo-office/page.js`` 做转译/打包，
验证无语法错误。esbuild 通过 ``npx --yes`` 获取；若因网络受限无法下载，
测试自动 skip，不阻塞后端验收。
"""
from __future__ import annotations

import subprocess
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))  # 使 v1_wave1_helpers 可导入

import pytest

from v1_wave1_helpers import FRONTEND_PAGE, REPO_ROOT


def test_ceo_office_page_jsx_syntax_ok():
    """page.js 经 esbuild（JSX）转译无语法错误。"""
    if not FRONTEND_PAGE.exists():
        pytest.skip("frontend/app/ceo-office/page.js 不存在")

    out = Path("/tmp") / "ceo_page_bundle_check.js"
    result = subprocess.run(
        [
            "npx",
            "--yes",
            "esbuild",
            str(FRONTEND_PAGE),
            "--loader:.js=jsx",
            "--bundle",
            "--external:react",
            "--external:react-dom",
            "--external:next",
            f"--outfile={out}",
        ],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )

    if result.returncode != 0:
        # 网络受限导致 esbuild 无法下载时跳过，不阻塞验收。
        err = (result.stderr or "").lower()
        if any(k in err for k in ("enotfound", "eai_", "network", "getaddrinfo", "npm error")):
            pytest.skip("esbuild 无法下载（网络受限），跳过前端语法检查")
        pytest.fail(f"page.js JSX 语法检查失败:\n{result.stderr}")

    assert out.exists(), "esbuild 未产出 bundle"
