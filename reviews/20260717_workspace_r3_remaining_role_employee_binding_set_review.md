# R3 剩余角色 Employee 与 Binding 集合质量 Review

- Issue：`issues/20260717_workspace_r3_remaining_role_employee_binding_set_l2_gate.md`
- 固定分支/修订：`feat/roadmap-r1r2` @ `f7aa3bd1935e164ac0a46ccdc338bf219150ebc8`
- 数据源：`deploy/curis/gateway/.generated/data/quality.sqlite`（只读）
- 结论：`BLOCKED_L2`

## 结论

五个角色 Employee 与五条 active model binding 的 API 创建结果复核通过；现有 Tech Lead 未变，当前数据正好形成 6 Employee + 6 active approved model binding，Run 的下一步仍是 Step 2。

但当前模型闸门仍只接受单个 `CURIS_R3_APPROVED_CAPABILITY_BINDING_ID`，无法接受本次批准的六 binding 集合。Step 2 使用 Product Manager binding 时会在 Adapter 前被拒绝，因此当前 Run 尚不具备下一步执行前置，最终状态为 `BLOCKED_L2`。

## 已通过证据

### 五个新增角色

| Step | 角色 | Employee | Binding | template slug |
| --- | --- | --- | --- | --- |
| 2 | Product Manager | `emp-75f8934f-cfb9-4c9f-a759-bdfe942f15db` | `bind-6d5b31e1-1b69-49a6-bd80-d2be741d6530` | `product-manager` |
| 3 | Architect | `emp-6d60d1b3-729e-4765-8b05-02cf7cf94e2d` | `bind-b476f200-6bfc-4d8e-b1d7-c2c6e4e5f938` | `architect` |
| 4 | Frontend Engineer | `emp-5ced522e-bced-432f-9a8b-a79497161f6c` | `bind-7275893a-7588-4f71-b780-ab55bef7db1d` | `frontend-engineer` |
| 5 | Backend Engineer | `emp-9dbb9c28-e244-41d4-b7bb-99ddf1ee44db` | `bind-e2cbbcb3-b940-4bbd-bd09-1225b86a0eb3` | `backend-engineer` |
| 6 | QA Engineer | `emp-bca9eaba-68fe-4c06-a4ca-2289b04c4174` | `bind-c04accdf-4567-4715-b9a3-46adf0eea40f` | `qa-engineer` |

- 五个 Employee 均为 `tenant-a/company-a/dept-9c7bb4ae-5145-43fe-948d-68afec2f3a28`，状态 `idle`、`enabled=1`。
- exact template_id 分别为 `official.employee.product_manager/architect/frontend_engineer/backend_engineer/qa_engineer`；source 均为 `official`，实际 slug 与总负责人批准的连字符形式一致。
- Step 2→6 五个角色未创建任何 `et_*` 家族实例，计数为 0。
- 每个 Employee 恰有 1 条 binding；均为 `official/model/official.openai.gpt-5.4-mini-2026-03-17/priority=1/enabled=1`，无重复或冲突。
- 现有 Tech Lead `emp-7417237e-2f30-4268-807f-88eaaf951bf8` 与 `bind-e222f21e-09de-43a6-aff5-0c1ae8b6555d` 保持 1 Employee + 1 active binding。
- Company 为 active `tenant-a/company-a`；Department 为 active/enabled；Project 为 active 且 company/department 匹配。
- Run 仍为 `wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`，模板 `official.workflow.software_rnd_sop`，状态 running；Step 1 succeeded，Step 2 pending，Step 3→7 pending。项目内另两条 Run 均为既有 failed 记录，未发现新的 pending/running Run。
- 历史唯一真实 UsageEvent 仍属于 Step 1 与 Tech Lead binding，`outbound_attempted=1/status=success`。

## 唯一阻塞

`backend/app/main.py` 当前把批准 binding 读取为单个环境变量，并要求当前 Step 的 `capability_binding_id` 必须与该单值完全相等；累计审计又要求当前 Run 的所有既有 UsageEvent 都使用同一个单值 binding。

因此不存在可用配置：

- 保持 `bind-e222...`：Step 2 的 PM binding 与批准单值不一致，返回 scope rejected；
- 改为 PM binding：Step 1 既有 UsageEvent 使用 `bind-e222...`，被计为 invalid audit，返回 cost rejected。

该闸门尚不能表达“当前 Run 的六个批准 Employee-binding 对，并按 Step role 精确匹配”的集合契约。未调用 `run-next-step`，未用真实调用验证该必然失败路径。

## 环境与范围

- `3000/3100/8001/8002/8080` 均为 CLOSED。
- 未启动服务、未注入或读取 Key、未出网、未调用模型、未创建 Run。
- 未跑全量、未修改代码或数据；仅新增本 Review。

## 状态

- Employee + binding 数据集合：`VERIFIED — PASS`
- 当前 Run 下一 Step 模型闸门：`FAILED — SINGLE_BINDING_ONLY`
- 最终：`BLOCKED_L2`
- 唯一下一步：系统交付席将闸门改为固定 Run 内按 Step/role/employee 精确允许批准 binding 集合，并保持历史 Step 1 binding 审计有效；随后质量运行席无出网复核。
- Next Seat：产品规划席
- Handoff：sent to 产品规划席
