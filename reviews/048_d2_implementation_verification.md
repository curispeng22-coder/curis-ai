# D2 Evolution Governor Sandbox 实现验证 (质量运行席)

- Date: 2026-07-07
- Reviewer seat: 质量运行席 (CONV-SEAT-QUALITY-001)
- Target: issues/046 + ADR-0021 + changed files (backend/app/governor_sandbox.py 新; backend/app/evolution_governor.py 增量 demonstrate(); backend/tests/test_d2_sandbox.py 新)
- Verdict: PASS

## Evidence

- **测试计数**：`python -m unittest discover -s tests -p "test_*.py"` → **Ran 63 tests … OK**，0 失败，无回归。
- **git diff 范围**：`git diff --name-only HEAD -- backend frontend` 仅列出 5 个已修改的 backend/app 文件（database.py、evolution_governor.py、main.py、orchestrator.py、result_store.py）；未跟踪新增为 evolution_event_log.py、governor_sandbox.py、tests/test_d2_sandbox.py、tests/test_d3_event_log.py —— 与预期完全一致（D2 自身仅贡献 governor_sandbox.py + demonstrate() + test_d2_sandbox.py；evolution_event_log.py / test_d3_event_log.py / main.py 端点均属 D3 切片 047）。
- **git diff --check**：`git diff --check HEAD -- backend frontend` 退出码 **0**（无空白/尾部空格问题）。
- **禁止域扫描**：对 backend/app 扫描 `Employee CRUD|employee expansion|multi-agent|agent abstraction|company organization|ROI|business module|external channel|dashboard|automatic code self-modification|task-role|task evidence|vector database|embeddings|external memory|implicit default|tool selection|route work|change task state|trigger evolution` → **ZERO 命中**。
- **沙箱不写权威状态扫描**：对 backend/app/governor_sandbox.py 扫描 `Database|ResultStore|connect(|save_|insert into|update |delete from|.sqlite` → **ZERO 命中**（沙箱从不触及权威状态）。

## Behavior-contract fidelity

- **Verdict: PASS**
- `GovernorSandbox.run()` 仅写于 `tempfile.mkdtemp(prefix="curis-sandbox-")` 一次性 OS temp 目录（不在项目/repo 下）；`applied_state` 含 `_sandbox_proposal` 标记，`rollback_snapshot` 精确等于原始输入快照；`_apply_proposal` 为纯函数，不修改入参。test_run_produces_evidence / test_throwaway_under_os_temp / test_rollback_restores_exactly_and_apply_differs / test_apply_proposal_is_pure 全部通过。✓
- `EvolutionGovernor.demonstrate()` 为增量封装（构建 `list_architecture_locks()` 快照 → 调 `GovernorSandbox.run()`），未触碰 `evaluate()` 决策逻辑；test_demonstrate_does_not_change_evaluate_behavior 确认 demonstrate 前后 `evaluate()` 决策输出一致。✓
- `demonstrate()` 对权威 SQLite 写 0 字节（DB 文件 size 前后一致）、不发出任何 evolution 事件；test_demonstrate_writes_zero_bytes_to_authoritative_db 通过。✓
- **无新增端点**：D2 自身未向 main.py 增加任何路由。main.py diff 中出现的唯一端点 `@app.get("/api/evolution-events")` 属于 D3 Evolution Event Log 切片（047，ADR-0016 唯一的被允许 append-only 日志/模式新增），非 D2 引入；D2 仅交付沙箱模块 + 增量 demonstrate() + 测试，符合 ADR-0021「No API endpoint」约束。✓
- 63 测试全过，无回归；`evaluate()` 自有测试仍通过。✓

## Known gaps / open questions

1. （承袭 reviews/046）ADR-0021 禁止列表宜显式补列 PROJECT_HANDOFF 禁止区项「Architecture lock bypass / uncontrolled architecture changes」与「Mock data or simulation substitution for release verification」——两者实际未违反（沙箱只读锁、用真实 throwaway 副本），但枚举缺失，建议产品规划席接受时一并补列。
2. （观察，非阻断）main.py 中已存在 D3 引入的 `@app.get("/api/evolution-events")` 端点，与 D2 无关；记录于此以免 D2 验收与 D3 端点混淆。D2 自身零端点，符合约束。

## Next

若 PASS → 路由 **产品规划席** 接受实现；接受后 D2 切片关闭，ADR-0016 三切片（D1 → D3 → D2）全部完成。
