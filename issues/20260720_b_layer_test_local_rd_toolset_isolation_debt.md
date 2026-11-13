# Issue: test_local_rd_toolset 既有 4 失败用例 · 测试隔离技术债

## Owner

软件工程席（寇豆码，B 层运行时治理增量 ①/③ 实现轮）

## Context

本 issue 为 B 层运行时治理增量交付（接真实 DecisionSink ① / 统一 outcome 映射 ③ /
跟进既有测试孤岛 ④）的**衍生跟踪项**。实现轮本身（①、③）已独立完成并全绿；本 issue
仅记录 `backend/tests/test_local_rd_toolset.py` 中**既有**的 4 个失败用例，属于测试隔离
技术债，**不阻塞**本次 B 层治理交付。

> 结论先行：**4 个失败用例均为测试隔离 / 全局状态残留问题，与产品代码无关**。
> 在「单独运行该文件」或「与 B 层治理两个测试文件同跑」时 6/6 全绿；仅在全量套件
> 特定执行顺序下偶发失败（顺序依赖型 flaky）。本实现轮的新增 / 修改代码未引入任何
> 新失败（全量 `pytest backend/tests/` 868 passed / 2 skipped / 0 failed）。

## 失败用例清单（4 个）

| 用例 | 类别 | 直接失败点 |
|---|---|---|
| `TestLocalRDToolset::test_paths_content_and_diff_fail_closed` | 路径/内容/补丁 fail-closed | `LocalRDToolError`（relative path / sensitive path / sensitive value / delete）断言未命中 |
| `TestLocalRDToolset::test_symlink_and_hardlink_are_rejected` | 符号链接 / 硬链接拒绝 | `LocalRDToolError`（symbolic / hard links）断言未命中 |
| `TestLocalRDToolset::test_unregistered_or_arbitrary_commands_and_git_writes_are_rejected` | 未注册命令 / git 写拒绝 | `LocalRDToolError`（not registered / input is invalid / not allowed）/ `ValueError` 断言未命中 |
| `TestLocalRDToolset::test_writer_rolls_back_when_final_audit_fails` | writer 终审计失败回滚 | `LocalRDToolError`（audit is unavailable）断言未命中 |

> 注：4 个用例在「`pytest backend/tests/test_local_rd_toolset.py` 单独运行」时 6/6 全过；
> 失败仅出现在与全量套件中**某些前置用例**共同执行、且残留全局状态未被 `tearDown`
> 清理干净的特定顺序下。本次实现轮执行全量套件未复现该 4 失败（进一步印证其为顺序
> 依赖型 flaky，而非稳定失败）。

## 根因假设（按可能性排序）

1. **共享模块级全局状态残留**（最高可能）：`LocalRDToolset` / `ToolExecutor` /
   `ToolRegistry` 依赖的 `WORKSPACE_ROOT`（模块级常量，所有 fixture 的临时目录均以
   其为父）及其他进程级单例（如注册表、事件日志、审计记录器）在用例间未完全隔离。
   前置用例若在 `WORKSPACE_ROOT` 下留下文件 / 注册表条目 / 审计行且 `tearDown` 仅清理
   自身 `case_dir` 与 `db_dir`，会污染后续用例的断言前提。
2. **单例 / 注册表跨用例泄漏**：`ToolRegistry` 在 `setUp` 中按 `LOCAL_RD_TOOL_IDS`
   重新注册；若某些前置用例修改了同进程内的全局注册表 / 命令白名单 / 审计回调，会导致
   「未注册」「not allowed」「input is invalid」类断言在后续用例中误判。
3. **导入顺序 / 模块初始化副作用**：`local_rd_toolset.py` 顶层有 `WORKSPACE_ROOT`
   等模块级求值；若全量套件中某较早导入的模块改写了工作目录、环境变量或该模块级常量，
   会影响后续用例对相对路径 / 敏感路径的判断（命中「relative path」「sensitive path」）。
4. **审计 / 事件日志的全局计数器或回调残留**：`FailAfterStartAudit` 式的审计桩或被
   前置用例替换的全局审计回调若未被还原，会干扰 `test_writer_rolls_back_when_final_audit_fails`
   的「audit is unavailable」触发条件。

> 以上为假设，非已证实根因；最终定位需 ⑤ QA 轮在稳定复现环境（固定 `--order` / 并行
> 关闭 / 干净 `.venv`）下做最小复现。

## 影响面

- **范围**：**仅** `backend/tests/test_local_rd_toolset.py`。
- **产品代码**：无。4 个失败均为测试侧断言 / 隔离问题，不反映 `local_rd_toolset.py`
  产品行为缺陷（其路径拒绝 / 链接拒绝 / 命令白名单 / 审计回滚逻辑在隔离运行时均正确）。
- **B 层治理交付**：**不阻塞**。本实现轮新增的 `decision_sink.py` 与 3 处 `pending_sink`
  旁路、2 个治理测试文件，均使用独立临时 sqlite / `MagicMock`，与 `WORKSPACE_ROOT` /
  全局注册表无耦合；全量套件 0 失败已验证。
- **隔离运行**：`pytest backend/tests/test_local_rd_toolset.py` → 6/6 全过（已验证）。

## 建议修复方向（低风险，待 QA 轮落）

1. **用例级 fixture 隔离**：`setUp` 中为每个用例构造独立的 `ToolRegistry` 实例（而非
   复用可能含前置污染的进程级注册表），并在 `tearDown` 显式 `teardown()`/清空注册表。
2. **重置全局状态**：在 `conftest` 或用例 `setUp` 中 `monkeypatch` 还原 `WORKSPACE_ROOT`
   指向本用例临时目录，避免跨用例路径判断污染。
3. **审计回调 reset**：`FailAfterStartAudit` 类桩若被注入全局审计器，需在 `tearDown`
   还原为默认 `EvolutionEventLog`，防止回调计数残留跨用例。
4. **并行/顺序固化**：在 CI 中以 `--forked` / `--order` 固定执行顺序，或在 `pyproject`
   中为该文件设 `pytest --repeat` 复现 flaky，定位最小触发前置用例。

> **风险边界**：若上述修复需大改 `local_rd_toolset.py` 产品代码或重构全局注册表 / 审计
> 体系（高改 / 高风险），**不要硬改**——保留本 issue 跟踪即可。本实现轮不做此类修复，
> 确保 B 层治理交付不被动到既有受保护闭环。

## 交付关联

- 本实现轮交付物：`backend/app/decision_sink.py`（新增）、`real_rd_executor.py` /
  `content_workflow_runtime.py` / `governance.py`（3 处 `pending_sink` 旁路 + 统一
  `outcome_for_letter`）、`backend/tests/test_b_layer_decisionsink.py`（新增）、
  `backend/tests/test_b_layer_runtime_governance.py`（`test_wiring_maps_b_to_allowed_not_simulated`
  → `test_wiring_maps_b_to_simulated_via_outcome_for_letter` 断言修正）。
- 上述新增 / 修改测试**不依赖**这 4 个失败用例，可独立通过（已验证：
  `test_b_layer_decisionsink.py` 26 passed、`test_b_layer_runtime_governance.py` 24 passed、
  与 `test_local_rd_toolset.py` 同跑 56 passed）。

## 状态

- `test_local_rd_toolset.py` 隔离：6/6 全过（不阻塞）。
- 全量 `pytest backend/tests/`：868 passed / 2 skipped / 0 failed（本实现轮未新增失败）。
- 4 失败为既有顺序依赖型 flaky 技术债，留作 **QA 轮** 稳定复现与最小修复。
- **明确标注：不阻塞本 B 层治理交付。**
