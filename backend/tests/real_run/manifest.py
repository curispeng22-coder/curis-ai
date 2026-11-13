"""真实研发闭环 fixture manifest：待验证 Issue 列表（步骤②脚手架）。

每个 Issue 含：
- issue_id       ：唯一标识
- difficulty     ：难度（易 / 中 / 难）
- target_file    ：目标源码文件（相对仓库根），须纳入 LocalRDToolset allow_paths
- issue          ：问题描述，映射到 RealRDExecutor 的 instructions
- expected_test  ：受验 pytest 用例路径（须位于 backend/tests/ 下，供
                   LocalRDToolset command_registry 注册）

具体 diff 由 executor(LLM) 生成；本清单只描述题目与期望。
"""
from __future__ import annotations

from typing import Any

ISSUES: list[dict[str, Any]] = [
    {
        "issue_id": "rd-fixture-a",
        "difficulty": "易",
        "target_file": "tools/real_rd_fixture/target_a.py",
        "issue": "将模块常量 BETA 由 2 修正为 3（typo / 常量修正，单文件单 hunk）。",
        "expected_test": "backend/tests/test_real_rd_fixture_a.py",
    },
    {
        "issue_id": "rd-fixture-b",
        "difficulty": "中",
        "target_file": "tools/real_rd_fixture/target_b.py",
        "issue": (
            "重构 greet_all：用空格连接 'hello <name>'，空列表返回空字符串"
            "（去掉分号与尾部空格）；并修正 add 为 a + b（当前为 a - b）。"
        ),
        "expected_test": "backend/tests/test_real_rd_fixture_b.py",
    },
]
