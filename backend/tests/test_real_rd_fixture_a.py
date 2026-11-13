"""真实研发闭环 fixture：易难度回归用例（Issue A）。

该用例在源码改动（BETA 修正为 3）前 FAIL、改动后 PASS。

被 backend/tests/conftest.py 的 ``collect_ignore`` 排除于常规
``pytest backend/tests/`` 收集之外（其初始失败是设计意图）；由 executor 通过
显式路径运行（见 backend/tests/real_run/manifest.py 与 run_real_issues.py）。
"""
from __future__ import annotations

import pathlib

_TARGET = (
    pathlib.Path(__file__).resolve().parents[2]
    / "tools"
    / "real_rd_fixture"
    / "target_a.py"
)


def _load_namespace() -> dict:
    namespace: dict = {}
    code = _TARGET.read_text(encoding="utf-8")
    exec(compile(code, str(_TARGET), "exec"), namespace)  # noqa: S102 - 受控 fixture 源码
    return namespace


def test_target_a_beta_is_correct() -> None:
    ns = _load_namespace()
    assert ns["BETA"] == 3


def test_target_a_greet_is_stable() -> None:
    ns = _load_namespace()
    assert ns["greet"]("curis") == "hello curis"
