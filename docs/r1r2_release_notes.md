# R1/R2 发布说明：真实研发闭环 hardening

## 本次改了什么

解除 `LocalRDToolset.run_test` 对 `/usr/bin/sandbox-exec` 的**硬依赖**，改为可配置
的 `SandboxMode` 策略（步骤③），并把该开关透传到 `RealRDExecutor`（步骤①），使真实
研发闭环可在代码库内一键复跑（不再依赖 `/tmp/real_rd_prove.py` 的覆写）。

### 核心变更

1. **`SandboxMode` 三态**（新增于 `backend/app/local_rd_toolset.py`）
   - `AUTO`（默认）：sandbox-exec 存在则走隔离；缺失则降级为直跑，审计标记 `sandbox_degraded=True`。
   - `OFF`：关闭隔离，直接执行注册命令（仅本地 / 受信 CI）。
   - `ENFORCE`：强制隔离；sandbox-exec 缺失时直接拒绝（`sandbox_unavailable`，fail-closed）。

2. **`LocalRDToolset.__init__(sandbox_mode=None)`**：仅关键字、默认 None（解析为 auto）；
   `command_registry` 位置参数不变（向后兼容）。

3. **`run_test` 降级逻辑**：`command_not_registered` 校验仍在 sandbox 检查之前
   （fail-closed 不变）；sandbox 走 / 不走由 `use_sandbox` 决定，argv 已含（或不含）
   sandbox 前缀，交 `_run_process` 时不再二次包装。两分支**均经过既有 `_execute` /
   `_audit` / `_safe_process_output`**，审计 / 脱敏 / 路径白名单完全一致。

4. **`RealRDExecutor(model, event_log, *, sandbox_mode=None)`**：将 `sandbox_mode`
   原样透传给 `_build_toolsets` 构造的三个 `LocalRDToolset` 实例（read / write / git）。

### 新增文件

- `backend/tests/fakes_rd.py`：`FakeLocalToolset` 测试替身（捕获 `_run_process` 的 argv）。
- `backend/tests/test_local_rd_toolset_sandbox.py`：run_test 三分支单测。
- `backend/tests/test_real_rd_executor.py`：新增 `sandbox_mode` 透传用例（FakeToolset 同步
  增加 `sandbox_mode` 关键字参数）。
- `backend/scripts/run_real_rd.py`：本地一键复跑 CLI（加载 `deploy/new-api/.env`，构造
  `ModelGatewayAdapter` + 真实 `LocalRDToolset` + `RealRDExecutor`）。
- `backend/docs/real_rd_local_run.md`：开关使用文档与安全红线说明。
- `backend/tests/real_run/{manifest.py, run_real_issues.py}`：端到端实跑脚手架（QA 严过关阶段执行）。
- `tools/real_rd_fixture/{target_a.py, target_b.py}` + `backend/tests/test_real_rd_fixture_{a,b}.py`：
  真实 TDD 夹具（易 / 中难度，fail-before-pass）；被 `conftest.collect_ignore` 排除于绿闸收集。
- `backend/scripts/pre_merge_check.py`：合入前置校验（非零退出即阻断）。
- `docs/merge_checklist.md`、`docs/r1r2_release_notes.md`：合入清单与发布说明。

## 如何本地复跑

```bash
# 1) 单元 / 集成（应全绿）
backend/.venv/bin/python -m pytest -q \
  backend/tests/test_real_rd_executor.py \
  backend/tests/test_local_rd_toolset_sandbox.py \
  backend/tests/test_local_rd_toolset.py

# 2) 一键复跑真实闭环（需本地 New API 可达）
python backend/scripts/run_real_rd.py --issue spec.json
python backend/scripts/run_real_rd.py --issue spec.json --no-sandbox   # OFF

# 3) 端到端实跑 fixture（需本地 New API + 模型；QA 严过关阶段）
python backend/tests/real_run/run_real_issues.py

# 4) 合入前置校验
python backend/scripts/pre_merge_check.py
```

issue 规格示例（stdin）：
```json
{"issue_id":"rd-001","target_file":"tools/real_rd_fixture/target_a.py",
 "issue":"Change BETA = 2 to BETA = 3",
 "expected_test":"backend/tests/test_real_rd_fixture_a.py"}
```

## 如何合入

见 `docs/merge_checklist.md`。由主理人执行：本地提交完成后运行 `pre_merge_check.py`，
全绿后 `git merge --no-ff feat/roadmap-r1r2` 到 `main`（工程师不自行 merge）。

## 安全边界（重申）

> ⚠️ `OFF` 与 `AUTO` 缺失下**失去网络隔离**能力。仅限本地开发 / 受信 CI。
> **生产多租户环境必须 `ENFORCE`，或确保 `/usr/bin/sandbox-exec` 真实存在**；
> 切勿在生产用 `OFF` / `AUTO` 跑不可信输入。

## 最小化变更确认

- 受保护文件 `model_gateway.py` / `evolution_event_log.py` / `d1_gateway_client.py` **未改动**。
- `read_file` / `apply_diff` / `search` / `git_read` 的既有行为未变（`_run_process` 仅新增
  `use_sandbox` 保留参数，逻辑不变）。
- 向后兼容：`command_registry` 保持位置参数；`sandbox_mode` 仅关键字、默认 None。
