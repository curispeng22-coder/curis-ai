# Workspace R3 精确 Binding Scope 集合 L2 Gate

- 日期：2026-07-17
- 状态：CLOSED — PASS
- Parent：`issues/20260717_workspace_r3_remaining_six_model_calls_l2_gate.md`
- Run：`wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`
- Owner：产品规划席
- Next Seat：架构边界席 → 安全边界席 → 总负责人
- 类型：模型调用授权 scope

## 先说结论

五角色 Employee + binding 数据集合已 PASS，但现有 R3 模型闸门只接受一个批准 binding ID，不能同时验证 Tech Lead 历史首步与 Step 2→6 的五个角色。不能关闭历史审计校验，也不能让一个 binding 跨角色复用。

本 Gate 只把当前 Run 的批准 binding scope 从单值升级为固定 role→binding 集合，并保持每个 Step 只能使用对应 binding；不实施、不启动、不注入 Key、不出网。

## 唯一固定集合

| Step role | 批准 binding |
| --- | --- |
| `tech_lead`（Step 1 / 7） | `bind-e222f21e-09de-43a6-aff5-0c1ae8b6555d` |
| `product_manager`（Step 2） | `bind-6d5b31e1-1b69-49a6-bd80-d2be741d6530` |
| `architect`（Step 3） | `bind-b476f200-6bfc-4d8e-b1d7-c2c6e4e5f938` |
| `frontend_engineer`（Step 4） | `bind-7275893a-7588-4f71-b780-ab55bef7db1d` |
| `backend_engineer`（Step 5） | `bind-e2cbbcb3-b940-4bbd-bd09-1225b86a0eb3` |
| `qa_engineer`（Step 6） | `bind-c04accdf-4567-4715-b9a3-46adf0eea40f` |

## 架构边界席唯一任务

1. 只读现有单 binding 配置、scope 校验、UsageEvent 历史审计与 Step role 取 binding 流程。
2. 给出最小兼容方案：配置中保存上述精确集合；每次按当前 Step role 选择唯一 binding，再执行现有 tenant/company/department/project/employee/capability/workflow 校验。
3. 首步历史 UsageEvent 必须继续用 Tech Lead binding 通过一致性检查；预算累计校验必须接受集合中不同 Step 的合法 binding，但拒绝集合外、角色错配或同角色多 binding。
4. 明确配置格式、缺失/重复/未知角色/错误 ID/空集合/客户端覆盖的 fail-closed、旧单值模式的生产行为、回滚和 focused 验收。
5. 不得改 Workflow 定义、Employee/binding 数据、历史 Run/UsageEvent、Provider/Model/Gateway/成本规则。

## 禁止范围

- 不修改代码、数据、配置或部署，不启动、不注入 Key、不出网、不调用模型。
- 不用通配符、任意列表、客户端传入 binding、数据库自动发现全部 binding 或按 Employee 随机选择。
- 不允许一个 binding 跨 role，也不允许同 role 多个批准 binding。
- 不新增第二 Run、第二 Provider、Fallback、重试或 RBAC 系统。

## Gate 输出

- Architecture Review：唯一配置/选择/校验方案、最少文件、兼容与回滚、focused 测试，结论 PASS 或唯一 BLOCKED_L2。
- 安全边界席复核：集合不可扩大、客户端不可覆盖、历史审计与累计预算不降级。
- 安全 PASS 与总负责人批准后，系统交付席才能实施并只做无出网 focused 验证。

## 架构与安全复核

- Architecture Review：`reviews/20260717_workspace_r3_exact_binding_scope_set_architecture_review.md`，结论 `PASS`（仅配置/边界契约）。
- 唯一配置为服务端固定、显式、无通配符的六角色 role→binding JSON 映射；当前 Step role 是唯一选择键。
- 历史单值仅兼容 Tech Lead 首步；新集合存在但缺失或错误时 fail-closed，不回退旧单值。
- Security Review：`PASS`（仅配置/边界契约，不授权实施或出网）。
- 未改代码、数据、部署；未启动、未注入 Key、未出网。等待总负责人批准。

## 总负责人批准

- 决策：`APPROVED`，仅批准固定六角色 role→binding 服务端配置与最小实现。
- 必须保持显式集合、逐 Step 唯一选择、全量 scope 校验，缺失/错配/覆盖/跨 scope 全部 fail-closed；不回退单值。
- 不改数据库、Workflow、Provider、Model、Gateway、成本、网络、前端或 Admin。
- 仅无出网 focused 验证；实施阶段不启动、不注入 Key、不出网。

## 首轮质量复核

- 实现修订：`9a790746782240aaa5e6e45f39272073e4521553`；服务端 R3 focused `13 passed`。
- 唯一阻塞：`deploy/curis/workspace.env.example` 的 role→binding JSON 未整体引用，经现有 `run-workspace-backend.sh` 使用 shell `source` 后双引号丢失，`json.loads` 失败，运行闸门会报 scope invalid。
- 只允许修正该环境变量引用方式，并补充“经现有启动脚本 source 后仍是合法 JSON 且等于批准集合”的无出网验证；不得改后端授权逻辑或其他范围。

## 最终质量收口

- 修复修订：`250fc6833e5b40ca5876d63bea654c6b407a1cef`；仅修正 `deploy/curis/workspace.env.example` 的 JSON 整体单引号。
- 按现有启动脚本 `source` 语义后 `json.loads` PASS，六角色精确相等，roles=6，raw bytes=360。
- R3 focused：`13 passed`；端口全关闭，未启动、未注入 Key、未出网。
- Review：`reviews/20260717_workspace_r3_exact_binding_scope_set_l2_gate_review.md`，结论 `PASS`。
- 产品验收：本 Gate 关闭；Parent 剩余六步可以进入安全启动前置，但不得自行调用。
