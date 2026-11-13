# Workspace R3 剩余角色 Employee 与 Binding 集合 L2 Gate

- 日期：2026-07-17
- 状态：CLOSED — DATA_SET_PASS
- Parent：`issues/20260717_workspace_r3_remaining_six_model_calls_l2_gate.md`
- Run：`wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`
- Owner：产品规划席
- Next Seat：架构边界席 → 安全边界席 → 总负责人
- 类型：角色执行主体与能力绑定范围

## 先说结论

当前 Run 只有 Tech Lead 与一个已批准 binding，无法合法执行 Step 2→6。不能通过修改计数、复用 Tech Lead 身份或放宽角色校验绕过。本 Gate 只确定五个缺失角色的精确 Employee + model capability binding 集合及边界，不实施、不写数据、不启动、不注入 Key、不出网。

## 固定角色与 Step

| Step | 角色 | Step key |
| --- | --- | --- |
| 2 | Product Manager | `requirement_clarification` |
| 3 | Architect | `architecture_design` |
| 4 | Frontend Engineer | `frontend_execution` |
| 5 | Backend Engineer | `backend_execution` |
| 6 | QA Engineer | `qa_verification` |

Step 7 `final_report` 继续使用现有 Tech Lead；不得新增第二个 Tech Lead 或替换现有成功首步主体。

字段说明：上表的 `product_manager / frontend_engineer / backend_engineer / qa_engineer` 是 Workflow `step_role` 标识，不是 EmployeeTemplate slug。实际批准模板的 API slug 分别为 `product-manager / architect / frontend-engineer / backend-engineer / qa-engineer`；两者不得混用。

## 架构边界席唯一任务

1. 只读核对 R2 已实例化资产、官方 Employee templates、当前 Company/Department/Project/Run 与现有 employees/bindings。
2. 对五个角色逐一给出唯一来源：优先复用当前 `company-a` 同一研发部门内已存在、enabled 且状态可执行的 Employee；若不存在，明确唯一批准 template_id 与应创建的单实例。
3. 每个 Employee 只绑定现有 approved model capability，不新增 Provider/Model/Gateway/Tool；给出唯一 binding scope：tenant/company/department/project/employee/capability/workflow/step role。
4. 明确五个 Employee 与五个 binding 的稳定 ID 生成/返回方式、唯一性、幂等、冲突停止、撤销与回滚；不得预先伪造实际 ID。
5. 确认 final_report 继续使用现有 Tech Lead binding，形成总计 6 Employee + 6 active binding 的精确集合。

## 必须保持的边界

- 仅 `tenant-a + company-a + 当前研发 department + project-e84e06d4-f014-4326-abcd-e6d9aea6ff95 + 当前 Run`。
- Employee 必须 enabled，状态仅允许既有可执行域 `idle / assigned`；disabled、跨部门、跨 Company 或跨 Project 必须 fail-closed。
- 每个 binding 只允许对应角色 Step 的 model capability；不得让一个 Employee 冒充多个角色，不得使用 Admin token 或客户端 Header 决定角色。
- 继续使用可信 membership/CEO、固定 OpenAI/newapi/model/egress、Token/成本、0重试、无Fallback 契约。
- 不改变 Workflow 7 Step 定义，不删除或改写现有 Run、StepResult、Execution、UsageEvent。

## 禁止范围

- 不修改代码、数据库、seed、fixture、配置或前端。
- 不自动创建 Employee/binding，不启动服务，不创建 Run，不注入或读取 Key，不调用模型。
- 不新增通用角色系统、RBAC、员工市场、自动招聘或跨项目共享 binding。
- 不用 mock/stub、默认员工、Tech Lead 复用或直接改库绕过缺失角色。

## Gate 输出

Architecture Review 必须给出：

- 五个角色各自唯一的“复用 Employee ID”或“批准 template_id + 待 API 创建单实例”；
- 五个 binding 的精确 scope 和创建顺序；
- 与现有 Tech Lead 合并后的 6 Employee / 6 binding 清单；
- additive/idempotent、冲突停止、撤销/回滚、无出网 focused 验收；
- 结论 `PASS` 或唯一 `BLOCKED_L2`。

完成后交安全边界席复核。只有安全 PASS 与总负责人批准后，系统交付席才能通过批准 API 创建缺失实例/绑定，并先做无出网核对。

## 架构与安全复核

- Architecture Review：`reviews/20260717_workspace_r3_remaining_role_employee_binding_set_architecture_review.md`，结论 `PASS`（仅集合与创建边界）。
- 五个角色均无可复用合法实例；唯一集合为五个 official Employee template 各通过现有 API 创建单实例，并各绑定现有 approved model capability。
- Security Review：`PASS`（仅集合/创建安全边界，不授权实施）。
- tenant/company/department/project/workflow/Step role scope、唯一性、撤销、回滚和 Adapter 前 fail-closed 已明确；现有 Tech Lead 与 binding 不变。
- 未写数据、未启动、未注入 Key、未出网；等待总负责人批准创建。

## 总负责人批准与模板消歧

- 总负责人 `APPROVED`：仅允许通过现有批准 API 创建/核对上述五个角色 Employee 与各自唯一 active model binding；严格先读后写、实际 ID 回传、同值复用、冲突即停。
- 预检发现每个角色同时存在 `et_{role}` 与 `official.employee.{role}` 两条 enabled official 模板，且共享实际 slug；不得按 slug 自行选择。
- 批准申请中列出的 `official.employee.product_manager`、`official.employee.architect`、`official.employee.frontend_engineer`、`official.employee.backend_engineer`、`official.employee.qa_engineer` 均解释为精确 `template_id`，不是 slug。
- 创建时只允许按上述 exact template_id 各命中 1 条，并校验实际 API slug 分别为 `product-manager / architect / frontend-engineer / backend-engineer / qa-engineer`；`et_*` 模板全部排除。0 条、多条或 slug 不一致立即停止。
- 最终目标仍为 6 Employee + 6 active binding，Step 7 继续现有 Tech Lead；不得跨角色复用、改代码、启动、注入 Key、出网或影响历史 Run。

## API 创建结果

- Product Manager：`emp-75f8934f-cfb9-4c9f-a759-bdfe942f15db` / `bind-6d5b31e1-1b69-49a6-bd80-d2be741d6530`。
- Architect：`emp-6d60d1b3-729e-4765-8b05-02cf7cf94e2d` / `bind-b476f200-6bfc-4d8e-b1d7-c2c6e4e5f938`。
- Frontend Engineer：`emp-5ced522e-bced-432f-9a8b-a79497161f6c` / `bind-7275893a-7588-4f71-b780-ab55bef7db1d`。
- Backend Engineer：`emp-9dbb9c28-e244-41d4-b7bb-99ddf1ee44db` / `bind-e2cbbcb3-b940-4bbd-bd09-1225b86a0eb3`。
- QA Engineer：`emp-bca9eaba-68fe-4c06-a4ca-2289b04c4174` / `bind-c04accdf-4567-4715-b9a3-46adf0eea40f`。
- 五个 exact template_id 均对应批准的连字符 API slug（`product-manager / architect / frontend-engineer / backend-engineer / qa-engineer`）、source=official、enabled=true；未使用 `et_*` 新建。Workflow step_role 仍使用既有下划线标识，不作修改。
- 当前总量 6 Employee + 6 active approved model binding；现有 Tech Lead/binding 不变。
- 未启动、未注入 Key、未创建 Run、未出网；等待质量运行席独立无出网复核。

## 质量收口

- Review：`reviews/20260717_workspace_r3_remaining_role_employee_binding_set_review.md`。
- 五角色 exact template / 连字符 slug、5 Employee + 5 binding 与既有 Tech Lead 合计 6 + 6，数据集合 `PASS`。
- 当前 Run 仍为原 Run，Step 2 pending；未创建第二 Run。
- 本 Issue 只负责数据集合，现已关闭。运行时仍只接受单 binding 的独立阻塞转入 `issues/20260717_workspace_r3_exact_binding_scope_set_l2_gate.md`。
