"""真实研发闭环 fixture：中难度题目（Issue B）。

题目：
1) 重构 greet_all：用空格连接 'hello <name>'，空列表返回空字符串
   （去掉分号与尾部空格）。
2) 修正 add 为 a + b（当前为 a - b）。

涉及单文件、2–3 hunk。executor 修复后 backend/tests/test_real_rd_fixture_b.py
由 FAIL 转为 PASS。

演示改动可用以下命令撤销：
    git checkout tools/real_rd_fixture/target_b.py
"""
from __future__ import annotations


def add(a: int, b: int) -> int:
    return a - b  # BUG：应为 a + b


def greet_all(names: list[str]) -> str:
    result = ""
    for name in names:
        result = result + "hello " + name + "; "
    return result
