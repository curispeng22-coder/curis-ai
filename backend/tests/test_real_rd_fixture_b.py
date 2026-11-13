"""真实研发闭环 fixture：中难度回归用例（Issue B）。

源码改动前 FAIL（add 返回 a-b；greet_all 带分号与尾部空格），改动后 PASS。

被 backend/tests/conftest.py 的 ``collect_ignore`` 排除于常规收集之外；
由 executor 通过显式路径运行。
"""
from __future__ import annotations

import pathlib

_TARGET = (
    pathlib.Path(__file__).resolve().parents[2]
    / "tools"
    / "real_rd_fixture"
    / "target_b.py"
)


def _load_namespace() -> dict:
    namespace: dict = {}
    code = _TARGET.read_text(encoding="utf-8")
    exec(compile(code, str(_TARGET), "exec"), namespace)  # noqa: S102 - 受控 fixture 源码
    return namespace


def test_add_is_correct() -> None:
    ns = _load_namespace()
    assert ns["add"](2, 3) == 5


def test_greet_all_joins_with_spaces() -> None:
    ns = _load_namespace()
    assert ns["greet_all"](["a", "b"]) == "hello a hello b"
    assert ns["greet_all"]([]) == ""
