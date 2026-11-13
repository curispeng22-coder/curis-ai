#!/usr/bin/env python3
"""合入前置校验（步骤④）：非零退出即阻断合入。

逐项检查（任一失败即非零退出）：
1. 工作区干净：``git status --porcelain`` 为空。
2. 测试全绿：三个 hardening 测试文件 pytest 全绿
   （test_real_rd_executor.py / test_local_rd_toolset_sandbox.py / test_local_rd_toolset.py）。
3. 与 main 无冲突：``git fetch`` + ``git merge --no-commit --no-ff main`` 干净，随后 ``--abort`` 撤销。
4. 提交归属线：``git log 83f017bf..HEAD`` 每 issue 独立提交（打印供人工复核）。
5. 受保护文件未动：``git diff --name-only 83f017bf..HEAD`` 不含
   model_gateway / evolution_event_log / d1_gateway_client（仅 local_rd_toolset.py 等允许变更）。

用法：
    python backend/scripts/pre_merge_check.py
    python backend/scripts/pre_merge_check.py --base 83f017bf --main main
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
VENV_PYTHON = REPO_ROOT / "backend" / ".venv" / "bin" / "python"

# 受保护文件（禁止改动）。
_PROTECTED = {
    "backend/app/model_gateway.py",
    "backend/app/evolution_event_log.py",
    "backend/app/d1_gateway_client.py",
}

# hardening 相关测试文件（必须全绿）。
_TEST_FILES = [
    "backend/tests/test_real_rd_executor.py",
    "backend/tests/test_local_rd_toolset_sandbox.py",
    "backend/tests/test_local_rd_toolset.py",
]


def _run(args, *, check=True, capture=True):
    return subprocess.run(
        args,
        cwd=str(REPO_ROOT),
        check=check,
        capture_output=capture,
        text=True,
    )


def _py():
    return str(VENV_PYTHON) if VENV_PYTHON.is_file() else sys.executable


def check_clean_tree() -> tuple[bool, str]:
    res = _run(["git", "status", "--porcelain"])
    dirty = res.stdout.strip()
    if dirty:
        return False, f"工作区不干净：\n{dirty}"
    return True, "git status --porcelain 为空"


def check_tests_green() -> tuple[bool, str]:
    cmd = [_py(), "-m", "pytest", "-q", *_TEST_FILES]
    res = _run(cmd, check=False)
    if res.returncode != 0:
        tail = "\n".join(res.stdout.strip().splitlines()[-15:])
        return False, f"pytest 非零退出（{res.returncode}）：\n{tail}"
    return True, "三个 hardening 测试文件全绿"


def check_no_main_conflict(main: str) -> tuple[bool, str]:
    # 仅在工作区干净时做合并演练（合并需要干净树）。
    status = _run(["git", "status", "--porcelain"]).stdout.strip()
    if status:
        return True, "跳过（工作区不干净，合并演练需干净树）；请在干净工作区复跑"
    _run(["git", "fetch"], check=False)
    res = _run(["git", "merge", "--no-commit", "--no-ff", main], check=False)
    try:
        if res.returncode != 0:
            return False, f"与 {main} 合并存在冲突：\n{res.stdout}\n{res.stderr}"
        return True, f"与 {main} 无冲突（合并演练干净）"
    finally:
        # 无论结果如何，撤销合并演练，恢复工作区。
        _run(["git", "merge", "--abort"], check=False)


def check_commit_attribution(base: str) -> tuple[bool, str]:
    res = _run(["git", "log", "--oneline", f"{base}..HEAD"], check=False)
    if res.returncode != 0:
        return False, f"无法列举 {base}..HEAD 提交（基准不存在？）：{res.stderr}"
    lines = [ln for ln in res.stdout.splitlines() if ln.strip()]
    if not lines:
        return False, f"{base}..HEAD 无任何提交"
    return True, "提交归属线（每 issue 独立提交，供人工复核）：\n" + "\n".join(
        f"  - {ln}" for ln in lines
    )


def check_protected_untouched(base: str) -> tuple[bool, str]:
    res = _run(["git", "diff", "--name-only", f"{base}..HEAD"], check=False)
    if res.returncode != 0:
        return False, f"无法列举 {base}..HEAD 变更文件：{res.stderr}"
    changed = [ln.strip() for ln in res.stdout.splitlines() if ln.strip()]
    touched = [f for f in changed if f in _PROTECTED]
    if touched:
        return False, "受保护文件被改动（禁止）：\n" + "\n".join(f"  - {f}" for f in touched)
    allowed_note = "允许变更（含 local_rd_toolset.py / real_rd_executor.py / tests / docs / scripts / fixtures）"
    return True, f"受保护文件未动；变更 {len(changed)} 个文件。{allowed_note}"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="合入前置校验（非零退出即阻断）")
    parser.add_argument("--base", default="83f017bf", help="提交归属 / 变更比对基准")
    parser.add_argument("--main", default="main", help="合入目标分支")
    args = parser.parse_args(argv)

    checks = [
        ("工作区干净", check_clean_tree),
        ("测试全绿", check_tests_green),
        ("与 main 无冲突", lambda: check_no_main_conflict(args.main)),
        ("提交归属线", lambda: check_commit_attribution(args.base)),
        ("受保护文件未动", lambda: check_protected_untouched(args.base)),
    ]

    print("=" * 72)
    print("合入前置校验（步骤④）")
    print(f"  base={args.base}  main={args.main}  repo={REPO_ROOT}")
    print("=" * 72)

    failed = 0
    for name, fn in checks:
        try:
            ok, detail = fn()
        except Exception as error:  # noqa: BLE001 - 单项错误不应中断整体校验
            ok, detail = False, f"校验异常：{type(error).__name__}: {error}"
        mark = "PASS" if ok else "FAIL"
        failed += 0 if ok else 1
        print(f"[{mark}] {name}")
        for line in detail.splitlines():
            print(f"      {line}")
    print("=" * 72)
    print(f"结论：{'全部通过，可合入' if failed == 0 else f'{failed} 项未通过，阻断合入'}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
