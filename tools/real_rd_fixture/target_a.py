"""真实研发闭环 fixture：易难度题目（Issue A）。

题目：将模块常量 BETA 由 2 修正为 3（typo / 常量修正，单文件单 hunk）。
executor 生成 unified diff 改 BETA 后，backend/tests/test_real_rd_fixture_a.py
由 FAIL 转为 PASS。

演示改动可用以下命令撤销：
    git checkout tools/real_rd_fixture/target_a.py
"""
from __future__ import annotations


ALPHA = 1
BETA = 2  # BUG：应为 3


def greet(name: str) -> str:
    """返回对 name 的问候语。"""
    return f"hello {name}"


def triangle_area(base: float, height: float) -> float:
    """返回直角三角形面积。"""
    return base * height / 2
