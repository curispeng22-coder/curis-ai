# Review 20260719 — D1 create_app_failed 最小修复（里程碑验收）

- Review date: 2026-07-19
- Reviewer seat: 软件 QA 工程师（independent milestone acceptance，单主执行模式移交）
- Subject: commit `82ca429d`（`backend/app/main.py`，+13 行）对 workspace 容器 `create_app_failed` 的最小修复
- Related: `issues/20260719_workspace_create_app_failed_d1_toolchain_minimal_fix.md`、`docs/pmo/20260719_quota_handoff_plan.md`（唯一目标：处理 `create_app_failed`，恢复 `/health`）
- 修复责任人：主理人（寇豆码两次 turn-limit 失败后由主理人直接完成最小修复）

## 验收范围

1. `/health` 是否已恢复（目标 `http_code=200 health_ok` 可复现）。
2. 脱敏红线是否未被破坏：启动失败信号仍只含 `exception_type` + `failed_stage` + `failure_code` + `failure_signal`；新增 `logger.warning` 为固定脱敏句，无异常原文/堆栈/参数/路径/Key/环境变量泄漏。
3. D1 真实 E2E 是否仍冻结（`0/1`）：本修复为「弹性降级」而非「启用 D1」，不得把 D1 路由接上真实工具链。
4. 两道坎（硬编码 macOS 路径 + 缩进 bug）是否在修复后正确处置，且未越界修改其他文件。

---

## 复现步骤与结果

### A. 代码改动核对（磁盘真实状态 == 提交 82ca429d）
- `main.py:6` — `import logging`（新增）。
- `main.py:117` — `from .local_rd_toolset import LocalRDToolError`（新增；`D1ToolchainError` 已于 `:116` 导入）。
- `main.py:170` — `logger = logging.getLogger(__name__)`（新增模块级 logger）。
- `main.py:906-910` — `create_app` 内 `build_d1_toolchain` 包韧性 try/except：
  ```python
  try:
      d1_toolchain = build_d1_toolchain(default_executor, event_log)
  except (FileNotFoundError, OSError, D1ToolchainError, LocalRDToolError) as error:
      logger.warning("D1 toolchain unavailable at startup; continuing without it (D1 frozen)")
      d1_toolchain = None
  ```
- `main.py:2044-2053` — D1 路由 `run_d1_single_model_toolchain`（`@app.post(D1_ROUTE)`，位于 `create_app` 内）函数体内守卫：
  ```python
  try:
      if d1_toolchain is None:
          raise HTTPException(status_code=503, detail="D1 toolchain unavailable")
      return d1_toolchain.execute()
  except D1ToolchainError as error:
      raise HTTPException(status_code=409, detail="D1 toolchain rejected") from error
  ```
  关键：`:2048` 的 `try:` 缩进为 8 空格，处于 `async def`（`:2045`，4 空格）函数体内 —— **第二道坎（缩进 bug）已修复**，503 守卫不再掉出路由体变成 `create_app` 顶层代码。

### B. /health 恢复（采用证据日志核对法，团队授权「或核对证据日志」）
- 证据日志 `deploy/curis/gateway/.generated/runtime/gateway-startup-20260719T112354Z-46137-summary.log`：
  ```
  event=sentinel_health
  component=gateway
  phase=sentinel
  http_code=200
  failure_class=health_ok
  timestamp=2026-07-19T11:23:54Z
  redaction_status=passed
  ```
- 同次运行（run `46137`）三服务日志：`workspace`/`egress`/`gateway` 均 `state=running`、`exit_code=0`，gateway `health=healthy` —— 容器启动期不再抛 `create_app_failed`，`/health` 返回 200。
- 说明：未另行重建镜像并重跑 sentinel（环境较重，且交付席证据为同提交、带时间戳的确定性产物）；/health 恢复由「代码路径（弹性降级使 `create_app` 不再中断）+ 证据日志 + 独立 compile/test」三方交叉确认。

### C. 脱敏红线核对
- **启动失败信号路径未被触及**：本提交仅改 `main.py` 13 行，信号构建函数（`_STARTUP_FAILURE_CODES` / `_startup_failure_signal` / `_classified_signal` / `_signal_for_startup_error`，位于 `:13-55`）一字未动；信号字典仍只含 `failed_stage` / `failure_signal` / `failure_code` / `exception_type` 四类固定字段。
- **新增 `logger.warning` 为固定脱敏句**：全文件 grep `logger.(warning|error|...)` 仅 1 处（`:909`），文案为字面量 `"D1 toolchain unavailable at startup; continuing without it (D1 frozen)"`，**不拼接 `str(error)` / 路径 / traceback / 参数 / Key**。
- 全文件 grep `traceback` / `format_exc` / `str(error)` / `repr(error)` / `f"D1` / `f'D1`：**零命中**（`str(error)` 仅存在于路由层 `HTTPException` detail，与本启动失败信号无关，且本提交未新增）。
- 证据日志 `redaction_status=passed`，与代码核对一致。

### D. D1 真实 E2E 冻结（0/1）核对
- `d1_toolchain` 仅在 `create_app` 内 `:907` 构建一次；容器内因 `local_rd_toolset` 硬编码 macOS 路径 → `FileNotFoundError`，被 `:908` 捕获 → `d1_toolchain = None`。
- `main.py:2051` 的 `d1_toolchain.execute()` 仅在该变量非 `None` 时执行，且位于**请求时**的路由体内；容器内为 `None` → 任何 D1 请求返回 `503`，**不接真实工具链**。
- 全文件 `d1_toolchain` 引用仅 `:907 / :910 / :2049 / :2051`，无启动期真实调用、无新依赖/新镜像。
- 结论：D1 真实 E2E 仍冻结，符合决策；本次为弹性降级。

### E. 两道坎根因处置核对
- 第一道坎根因 `local_rd_toolset.py:21`（`WORKSPACE_ROOT = Path("/Users/yy/Documents/Curis AI Workspace")`）与 `:83`（`WORKSPACE_ROOT.resolve(strict=True)`）**保持原样未改**；`git show 82ca429d -- local_rd_toolset.py` 为空（本提交只动 `main.py`）。符合「不修改 `WORKSPACE_ROOT`」决策（属独立议题）。
- 第二道坎（缩进 bug）已修复（见 A 节 `:2048` 缩进）。

---

## 测试通过率

- `python3 -m py_compile backend/app/main.py` → **OK**（独立复跑）。
- `pytest tests/test_workspace_startup_stage_signal.py` → **7 passed**（独立复跑；启动信号增强行为未被破坏，含新增 in-file 运行期 handler 冒烟测试）。
- 现有测试套件未触及 D1 启动路径；D1 降级逻辑由代码核对 + 证据日志覆盖。

---

## 已知问题（Known Issues）

1. **D1 真实 E2E 仍冻结（`0/1`）** —— 这是**设计意图**（决策明确「不启用 D1」），非缺陷。容器启动期 D1 toolchain 构建失败被降级为 `None`，所有 D1 请求返回 `503`。仅在总控决策解冻后才会接真实工具链。
2. **根因（硬编码 macOS 路径 `local_rd_toolset.py:21`）未修** —— 按决策**故意保留**（属独立议题，不在本次最小修复范围）。本次仅在 `main.py` 做弹性降级兜底，未改 `WORKSPACE_ROOT`，故 Linux 容器内 D1 toolchain 仍会因 `FileNotFoundError` 降级为 `None`（符合预期，不影响 `/health`）。
3. **`/health` 恢复采用证据日志核对法** —— 未由本 QA 另行重建镜像重跑 sentinel（环境较重）；若需 100% 独立容器复跑，可后续补一次 sentinel（同提交、环境齐备时）。

---

## 结论（Verdict）

**PASS_WITH_NOTES — 验收通过（含设计性 Known Issues 说明）。**

**结论**：commit `82ca429d` 的 D1 `create_app_failed` 最小修复达成唯一目标——workspace 容器启动期不再因 D1 toolchain 构建失败而中断 `create_app()`，`/health` 恢复为 `http_code=200 health_ok`（证据日志 + 三服务 `state=running exit_code=0` 确认）；脱敏红线未被破坏（启动信号字段集不变、新增 `logger.warning` 为固定脱敏句、全文件无 `traceback`/`format_exc`/`str(error)` 泄漏）；D1 真实 E2E 仍冻结（`0/1`），本次仅为弹性降级，未接真实工具链。两道坎均正确处置，且未越界修改 `local_rd_toolset.py` 以外的文件。

**原因**：
- 修复精准：仅用 13 行在 `create_app` 内对 `build_d1_toolchain` 做异常兜底（捕获 `FileNotFoundError/OSError/D1ToolchainError/LocalRDToolError` → `d1_toolchain=None`），并把 503 守卫正确收回路由函数体内（修复缩进 bug）。
- 脱敏合规：新增日志仅为固定字面量，信号构建函数零改动，符合「红线：不输出异常原文/堆栈/参数/路径/Key/环境」与「分类仅由固定 `(stage,signal)→failure_code` 映射决定」。
- 范围守纪：未启用 D1、未改 `WORKSPACE_ROOT`、未引入新依赖/镜像/域名，严格落在「禁止范围」内。
- 可复现性：证据日志 `redaction_status=passed` 与代码核对一致；`py_compile` 与 `pytest 7/7` 独立复跑通过。

**建议**：
1. 维持现状即可合入/继续 D1 真实研发工具闭环的下一步；本 issue 可标记 `DONE`（启动韧性目标达成）。
2. 后续若总控决定解冻 D1，应在独立议题中处理 `local_rd_toolset.py:21` 的 macOS 硬编码路径（改由环境变量/运行时解析 `WORKSPACE_ROOT`），而非在本次降级逻辑上叠加。
3. （可选）若团队要求对 `/health` 做 100% 独立容器复跑，可在同环境再跑一次 sentinel 以补充本 QA 的证据链；当前证据已充分。

## Verification（本验收依据）
- 读取真实磁盘文件 `backend/app/main.py`、`backend/app/local_rd_toolset.py`，核对 diff 与提交 `82ca429d` 一致。
- git 核对：`82ca429d` 仅改 `main.py`（13 行）；`local_rd_toolset.py` 未触碰。
- grep 全文件 `traceback`/`format_exc`/`str(error)`/`repr(error)`/`logger.*`/`f"D1`/`f'D1` → 仅 1 处固定 `logger.warning`。
- 独立 `py_compile` + `pytest tests/test_workspace_startup_stage_signal.py`（7 passed）。
- 核对 sentinel 证据日志 `gateway-startup-20260719T112354Z-46137-summary.log` 及同 run 三服务日志。

## Next Curis seat
- 本 QA 验收完成；issue 可交回主理人/总控标记 DONE 并继续 D1 闭环后续。
- 解冻 D1 的真实修复归独立议题（改 `WORKSPACE_ROOT`），不在本次范围。

## Handoff status
RESOLVED → 改动 ACCEPTED（PASS_WITH_NOTES）
- 非阻塞后续：① 总控解冻 D1 时处理 `WORKSPACE_ROOT` 硬编码（独立议题）；② 可选补一次独立 sentinel 复跑。
- 验收产物：`reviews/20260719_workspace_create_app_d1_minimal_fix_qa.md`。
