# D1 execute() 完整闭环 — 实现 Issue（范围 A）

> **状态**：APPROVED（总控 gate 2026-07-20：先做 A，通过后 B）
> **关联提案**：`issues/20260719_d1_execute_full_loop_proposal.md`（GATE_APPROVED，范围 A）
> **关联前置**：D1 工具链解冻 A+B（commit `aadef60c`，已推 `origin/feat/roadmap-r1r2`）
> **分支**：`feat/roadmap-r1r2`
> **铁律**：脱敏红线（启动/warning/日志/`/health` 绝不泄露路径/堆栈/Key/参数）；不引多 Agent；单主执行；复用既有模块不重写

---

## 一、范围

- **仅选项 A**：最小真实调用。P0 全量 = execute() 真实调用 R3 网关跑通**单模型 + 单任务类型**；脱敏 + 回退开关 + 契约稳定。
- **不含**：落库、可观测、错误分类增强 UI（均属 B 二期）。

## 二、任务列表（A1–A5，源自提案第二节）

| 编号 | 任务名 | 涉及文件 | 依赖 | 阻塞安全边界席 |
|---|---|---|---|---|
| A1 | 扩展 D1 配置开关 | `app/d1_config.py` | 无 | 否（仅加 `execute_enabled` 开关，不含凭证） |
| A2 | 定义 R3 网关客户端契约 | `app/d1_gateway_client.py` | 无（依赖既有 `ModelGatewayAdapter`） | **是**（仅定义接口契约，不读 Key） |
| A3 | 实现 execute 编排 + 错误分类 + 降级状态 | `app/d1_execute.py` | A1, A2 | 否（逻辑可独立完成） |
| A4 | D1 路由接入编排层 | `app/main.py` | A3 | 否 |
| A5 | 契约/降级单测 | `tests/test_d1_execute.py` | A3, A4 | **是（真实网关端到端待凭证裁定；mock + 降级先行）** |

**执行顺序**：A1、A2 可并行起步 → A3 → A4 → A5（mock 部分先于真实部分）。`execute_enabled=false` 时编排层整体降级（与 frozen 同效），保证未拍板/未裁定前不触发真实调用。

## 三、凭证阻塞说明（关键）

- 🔴 **R3 网关凭证接入方式仍待安全边界席裁定**（已飞书升级 Curis 开发通知群 `oc_1b559ad633e40345229275d15f7e8d42`，未回）。
- **本 Issue 实现策略**：
  1. A1–A4 全部实现（不依赖真实凭证）。
  2. A5 先实现并运行 **mock `http_post` 真实调用成功路径 + 全部降级/分类测试**（frozen→503、凭证缺失→受控降级、网关不可达→分类降级、TASK_INVALID→422/409）。
  3. A5 的**真实网关端到端验证**标注为「待安全边界席凭证裁定后补」，**不硬编 Key**、不读真实凭证。
- `execute_enabled` 默认 **false**（与 `CURIS_D1_FROZEN` 叠加）；未裁定前编排层整体降级，不触发真实调用。

## 四、文件清单（相对 `backend/`）

| 文件 | 类型 | 职责 |
|---|---|---|
| `app/d1_config.py` | 修改 | 在既有 `D1ToolchainConfig`/`load_d1_config` 追加 `execute_enabled` 开关与 `execute_task_type` 常量；frozen 语义不变 |
| `app/d1_gateway_client.py` | **新增** | R3 网关客户端适配：仅定义接口契约与调用形态（包装既有 `ModelGatewayAdapter`）；`is_configured()` 判凭证就绪但不暴露 Key；不读 Key |
| `app/d1_execute.py` | **新增** | execute() 真实调用编排 + 错误分类（四类枚举）+ 降级状态判定（READY/DEGRADED/FROZEN）+ 脱敏异常；复用既有单主占锁 |
| `app/main.py` | 修改 | D1 路由内接 `D1ExecutionOrchestrator`，复用既有 503 守卫与脱敏；`/health` 不变 |
| `tests/test_d1_execute.py` | **新增** | 契约/降级/分类单测：frozen→503、凭证缺失→受控降级、网关不可达→分类降级、mock 真实调用成功路径（真实网关端到端受凭证裁定阻塞） |

> 既有模块（`build_d1_toolchain` / `D1SingleModelToolchain` / `ModelGatewayAdapter` / `LocalRDToolset` / `EvolutionEventLog`）**不重写**，仅被编排层消费。

## 五、验收口径（QA 专项）

- **P0-1**：execute() 真实调用能力就位（代码路径贯通；真实端到端待凭证裁定）。
- **P0-2**：脱敏红线——warning/日志/`/health` 零泄露（QA 专项静态 + 运行抽检）。
- **P0-3**：`CURIS_D1_FROZEN=true` 整体降级 503；网关不可达安全降级；无裸错。
- **P0-4**：契约/接口稳定，单测覆盖（mock + 降级全绿）。
- **纪律**：无新增 pip 依赖；不引多 Agent；零新增 UI；单主执行。

## 六、交付流（工程师 → QA → 主理人）

1. 工程师批量写代码（A1–A4 + A5 mock/降级），完成后 IS_PASS 全局一致性审查。
2. QA 专项验证（含脱敏抽检），智能路由判定（源码 Bug → 回工程师；测试 Bug → 自修）。
3. A 通过后主理人汇报，再开 **B 实现 Issue**（B0–B5）走标准 SOP。

## 七、红线与升级纪律

- 若实现过程发现需触碰 L2 七项任一项 → 立即停，升级安全边界席 → 飞书 → 等总控。
- 真实网关端到端验证**不得**在凭证裁定前自行启用；`execute_enabled` 保持 false 直至安全边界席裁定回填。
- 提交严格只含本 Issue 文件；不串 R3/093/095 等其他 issue 挂起改动（各自 owner 提交）。
