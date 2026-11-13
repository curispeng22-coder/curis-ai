"""Wave 2 验证项 6（前端语法）。

frontend/app/control/secret-vault.* 与 frontend/app/platform/results.* 经
SWC（Next.js 自带 @next/swc 原生绑定）转译无语法错误。

实现：定位本地 .pnpm 中的 @next/swc 原生 .node 绑定，写一个临时 Node 脚本按
next-swc 的 ``transformSync(src, isModule:bool, optionsBuffer)`` 签名调用，
要求 ecmascript + jsx 解析。若本机无 node / 该原生绑定则跳过（标注未真跑）。
"""
from __future__ import annotations

import glob
import json
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FRONTEND = REPO_ROOT / "frontend"
SWC_CANDIDATES = sorted(
    glob.glob(
        str(
            FRONTEND
            / "node_modules"
            / ".pnpm"
            / "@next+swc-darwin-arm64*"
            / "node_modules"
            / "@next"
            / "swc-darwin-arm64"
            / "next-swc.darwin-arm64.node"
        )
    )
)

FRONTEND_FILES = [
    FRONTEND / "app" / "control" / "secret-vault" / "page.js",
    FRONTEND / "app" / "platform" / "results" / "page.js",
]

NODE_BIN = shutil.which("node")


def _write_node_checker(tmp_path: Path, binding: str) -> Path:
    script = r"""
const fs = require('fs');
const path = require('path');
const nativePath = process.argv[2];
const files = process.argv.slice(3);
const swc = require(nativePath);
const opts = {
  jsc: { parser: { syntax: 'ecmascript', jsx: true },
         transform: { react: { runtime: 'automatic' } } },
  module: { type: 'es6' },
};
const optBuf = Buffer.from(JSON.stringify(opts));
let ok = true;
for (const f of files) {
  const code = fs.readFileSync(f, 'utf8');
  try {
    swc.transformSync(code, false, optBuf);
    console.log('OK ' + f);
  } catch (e) {
    ok = false;
    console.log('SYNTAX_ERROR ' + f + '\n' + e.message);
  }
}
process.exit(ok ? 0 : 1);
"""
    p = tmp_path / "jsx_check.cjs"
    p.write_text(script, encoding="utf-8")
    return p


@pytest.mark.skipif(NODE_BIN is None, reason="本机无 node，跳过前端转译验证")
@pytest.mark.skipif(not SWC_CANDIDATES, reason="本机未找到 @next/swc 原生绑定，跳过前端转译验证")
def test_frontend_files_transpile_without_syntax_error(tmp_path):
    binding = SWC_CANDIDATES[0]
    checker = _write_node_checker(tmp_path, binding)
    args = [NODE_BIN, str(checker), binding, *[str(f) for f in FRONTEND_FILES]]
    r = subprocess.run(args, capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, f"前端转译失败：\n{r.stdout}\n{r.stderr}"


def test_frontend_files_present():
    for f in FRONTEND_FILES:
        assert f.exists(), f"待验收前端文件不存在：{f}"
