# D1 工具链解冻 — 实现 Issue（A+B 范围）

> **状态**：APPROVED / IN_PROGRESS
> **Gate**：总控 2026-07-19 批准（越 ADR-0017 design-only 预授权）
> **关联提案**：`issues/20260719_d1_toolchain_unfreeze_proposal.md`（§二 技术实现方案 / T1–T5）
> **铁律**：启动信号 / warning / 日志 / `/health` 绝不泄露路径、堆栈、Key、参数。
> **实现方式**：标准 SOP（工程师实现 → QA 验收）。

## 目标

把 D1 本地研发工具链从「容器内弹性降级（`d1_toolchain=None`）」解冻为「容器内真实可用」：
- 容器内 `WORKSPACE_ROOT` 解析不再依赖 macOS 宿主机硬编码路径；
- 支持 `CURIS_D1_WORKSPACE_ROOT` 覆盖 + `CURIS_ENV` 多环境 profile 配置化（B 范围）；
- 保留 `CURIS_D1_FROZEN`（默认 `false`）回退 kill-switch；
- D1 路由在非冻结且 toolchain 就绪时返回**真实工具结果**（E2E 0/1 → 1/1）；
- `/health` 维持 HTTP 200；脱敏红线不变。

## 范围（B，含 A）

| 任务 | 文件 | 要点 |
|---|---|---|
| **T1** 配置解析层 | `backend/app/d1_config.py`（新） | `D1ToolchainConfig` dataclass（frozen, workspace_root_override）+ `load_d1_config()`；读 `CURIS_D1_FROZEN`（默认 false）、`CURIS_D1_WORKSPACE_ROOT`（默认 None）、`CURIS_ENV`（dev/test/prod，默认从 env 推导或 "prod"）；多环境 profile 表（每 profile 一份 workspace_root 策略 + 安全 fallback）；统一脱敏常量 `D1_UNAVAILABLE_MESSAGE`。 |
| **T2** local_rd_toolset 改造 | `backend/app/local_rd_toolset.py` | 移除 line 21 硬编码 macOS 路径；新增模块级 `_DERIVED_ROOT = Path(__file__).resolve().parents[2]`、`_WORKSPACE_ROOT_OVERRIDE: str | None = None`、`_resolve_workspace_root(override=None)` 受控解析（解析失败抛脱敏 `LocalRDToolError`，绝不抛裸 `FileNotFoundError` 穿透启动）；`__init__` 与 `_assert_root` 改用受控解析；覆盖位在 build 时由 config 注入。 |
| **T3** main.py 接线 | `backend/app/main.py`、`backend/app/d1_single_model_toolchain.py` | `create_app` 启动时 `load_d1_config()` 一次全局缓存；`build_d1_toolchain(model, event_log, config=None)` 增 `config` 参数，`config.frozen` → 返回 `None`（kill-switch），并把 `config.workspace_root_override` 注入 `local_rd_toolset._WORKSPACE_ROOT_OVERRIDE`；D1 路由收敛 503 守卫（`d1_toolchain is None or config.frozen`）。保留现有 `try/except` 弹性降级 + 脱敏 warning。 |
| **T4** E2E 测试 | `backend/tests/test_d1_unfreeze.py`（新） | (a) 非冻结 + root 存在 → `build_d1_toolchain` 成功、路由返回 `status=succeeded` 真实结果（E2E 1/1）；(b) root 缺失/非法 → 503 回退；(c) `CURIS_D1_FROZEN=true` → `build_d1_toolchain` 返回 `None`、路由 503；不触发模型调用、不触网络。 |
| **T5** QA 脱敏专项 | `reviews/20260719_d1_unfreeze_qa.md`（新） | warning/日志/`/health`/启动信号无路径/堆栈/Key 泄露；frozen 回退有效；不引入 L2 七项新范围；全量聚焦测试通过。 |

## 跨文件约定（必守）

- 脱敏文案统一：`D1_UNAVAILABLE_MESSAGE = "D1 toolchain unavailable; service continues without it"`（warning 与 QA 文案统一，禁止含路径/堆栈/Key）。
- 配置键：`CURIS_D1_FROZEN`（bool 默认 false）、`CURIS_D1_WORKSPACE_ROOT`（str 默认 None）、`CURIS_ENV`（str 默认 "prod"）。
- frozen 默认值 `false`（解冻态）；设 `true` 即整体回退降级（→ None → 503）。
- `WORKSPACE_ROOT` 推导：`Path(__file__).resolve().parents[2]`（宿主=原硬编码值，容器内=挂载仓库根）；`CURIS_D1_WORKSPACE_ROOT` 为可选覆盖。
- 503 守卫：仅当 `d1_toolchain is None` 或 `config.frozen is True` 触发，就绪时返回真实结果。
- 异常边界：`LocalRDToolset` 解析失败一律抛 `LocalRDToolError`（脱敏），绝不抛未捕获 `FileNotFoundError` 穿透 `create_app`。
- 日志纪律：warning/`/health`/启动信号只输出脱敏常量，禁用 `logger.exception` 打印堆栈。

## 禁止区（铁律）

- 不接外部平台 / 外部服务与凭证；
- 不自动改生产代码、不引入自动改生产码能力（D1 工具集仅用其既有 read/search/apply_diff/run_test/git_read）；
- 不触 L2 Gate 七项；
- 不做 Employee CRUD、多 Agent、真实隔离、复杂 UI、向量库；不实现 instantiation/ROI/员工。

## 验收标准（来自提案 PRD §9）

- [ ] 非冻结配置下，D1 路由返回真实工具结果（非 503、非 None）；
- [ ] D1 端到端测试 0/1 → 1/1 通过；
- [ ] `/health` 维持 HTTP 200（sentinel 实测）；
- [ ] 脱敏红线不变：warning/日志/`/health` 无路径、堆栈、Key 泄露（QA 专项核验）；
- [ ] `CURIS_D1_FROZEN=true` 可整体回退到降级态（503）；
- [ ] 未引入 L2 Gate 七项任何新范围；
- [ ] 无新增第三方依赖。

## 提交纪律

- 一个 Issue 一个提交（或按 T1–T5 分提交，但最终可 squash 为一个语义提交）。
- 提交信息含 `Refs: issues/20260719_d1_toolchain_unfreeze_implement.md` 与 `issues/20260719_d1_toolchain_unfreeze_proposal.md`。
- 不混入本 Issue 外的其他未提交改动。
