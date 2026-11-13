# R3 剩余角色 Employee 与 Model Binding Architecture Review

Issue：`issues/20260717_workspace_r3_remaining_role_employee_binding_set_l2_gate.md`  
Run：`wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`  
范围：只读核对；未创建、未修改、未启动、未出网。  
结论：`PASS`（仅集合与创建边界，仍需安全复核及总负责人批准）。

## 核对结论

固定证据已表明当前 tenant-a/company-a 研发部门只有现有 Tech Lead 与 binding `bind-e222f21e-09de-43a6-aff5-0c1ae8b6555d`。Step 2→6 的五个角色没有可复用的当前 enabled、可执行 Employee + binding，因此五个结果均为“唯一官方 template + 待 API 创建单实例”，不是复用 Tech Lead。

官方模板均来自现有 EmployeeTemplate 种子，现有 R3 模型 capability 为 `official.openai.gpt-5.4-mini-2026-03-17`；不新增 Provider、Model、Gateway 或 Tool。

## 五个唯一结果

| Step | 角色 | 唯一模板 | Employee 结果 | 唯一 binding |
| --- | --- | --- | --- | --- |
| 2 | Product Manager / `product_manager` | `official.employee.product_manager` | 待创建单实例，API 返回实际 UUID；不得预造 ID | 待创建 1 条 active binding，绑定该 Employee + approved model capability |
| 3 | Architect / `architect` | `official.employee.architect` | 待创建单实例，API 返回实际 UUID；不得预造 ID | 待创建 1 条 active binding，绑定该 Employee + approved model capability |
| 4 | Frontend Engineer / `frontend_engineer` | `official.employee.frontend_engineer` | 待创建单实例，API 返回实际 UUID；不得预造 ID | 待创建 1 条 active binding，绑定该 Employee + approved model capability |
| 5 | Backend Engineer / `backend_engineer` | `official.employee.backend_engineer` | 待创建单实例，API 返回实际 UUID；不得预造 ID | 待创建 1 条 active binding，绑定该 Employee + approved model capability |
| 6 | QA Engineer / `qa_engineer` | `official.employee.qa_engineer` | 待创建单实例，API 返回实际 UUID；不得预造 ID | 待创建 1 条 active binding，绑定该 Employee + approved model capability |

## Binding 唯一范围

每一条 binding 必须同时满足：

- `tenant_id=tenant-a`；
- `company_id=company-a`；
- 当前研发 Department ID（从固定 Run/Project 读取，不手填）；
- `project_id=project-e84e06d4-f014-4326-abcd-e6d9aea6ff95`；
- `employee_id` 为该角色 API 创建后返回的唯一 ID；
- `capability_source=official`、`capability_type=model`、`capability_id=official.openai.gpt-5.4-mini-2026-03-17`；
- `workflow_template_id=official.workflow.software_rnd_sop`；
- 仅允许对应 Step role：Step 2 `product_manager`、Step 3 `architect`、Step 4 `frontend_engineer`、Step 5 `backend_engineer`、Step 6 `qa_engineer`。

运行器仍按当前 Step role 查找 Employee；binding 不得跨角色、跨 Department、跨 Company、跨 Project 或绑定其他 capability。Step 7 继续复用现有 Tech Lead 与 `bind-e222f21e-09de-43a6-aff5-0c1ae8b6555d`，不创建第二 Tech Lead。

## 创建顺序与稳定性

仅在总负责人批准后按以下顺序执行，且每步先读后写：

1. 校验 tenant-a、company-a、当前研发 Department、固定 Project、Run 状态和可信 CEO/scope；任何不一致停止。
2. 按 Step 2→6 顺序读取同 Department 内相同 role 的 enabled Employee；若出现多个合法候选，停止，不自行选择。
3. 对缺失角色调用既有 Employee 单实例创建 API，使用对应 official template、固定 company/department、`enabled=true`、可执行状态 `idle`；API 返回的实际 Employee ID 才是后续唯一引用。
4. 对每个新 Employee 写入一条现有 capability binding API 记录；binding ID 使用 API 返回值，不预造或拼接。
5. 每次写入后重新读取并校验完整 scope；全部五个 Employee + binding 通过后，才允许把集合提交给后续质量核对。

幂等键是 `(tenant, company, department, role, template)` 对 Employee 和 `(tenant, company, department, project, employee, workflow, step role, capability)` 对 binding。重复执行若已存在唯一同值记录则复用；空缺才创建；多条、冲突、disabled、deprecated 或跨 scope 记录立即停止。现有 binding API 会替换指定 Employee 的 binding 集合，因此只能对新建 Employee 使用，不能对现有 Tech Lead 调用以免破坏已批准 binding。

## 六项最终清单

1. 现有 Tech Lead：现有 Employee ID（固定 Run 当前记录） + `bind-e222f21e-09de-43a6-aff5-0c1ae8b6555d`，Step 1/7 既有范围；不改。
2. Product Manager：API 返回 Employee ID + 新 binding ID，Step 2。
3. Architect：API 返回 Employee ID + 新 binding ID，Step 3。
4. Frontend Engineer：API 返回 Employee ID + 新 binding ID，Step 4。
5. Backend Engineer：API 返回 Employee ID + 新 binding ID，Step 5。
6. QA Engineer：API 返回 Employee ID + 新 binding ID，Step 6。

预期总量为 6 Employee、6 active model binding；其中第 1 项是既有记录，第 2–6 项各新增一条。实际 UUID/binding ID 必须由 API 返回，不能在 Review 中伪造。

## 撤销、回滚与无出网验收

任一 Employee 或 binding 被撤销、disabled、deprecated、scope 不一致或 capability inactive，相关 Step 在 Adapter 前 fail-closed；不删除或改写当前 Run、首 Step、StepResult、Execution、UsageEvent。回滚只撤销本次新建的五个 Employee/binding，保留现有 Tech Lead；若无法精确识别本次新增记录，停止回滚并保持阻塞。

不出网 focused 验收必须证明：五个角色各有且仅有一个 enabled Employee；每个 binding 的 tenant/company/department/project/employee/capability/workflow/role 全匹配；Tech Lead binding 未变化；Step 2→6 按顺序各取对应 Employee；伪造 Header、跨 scope、错误 capability、重复候选、撤销记录均在 Adapter 前拒绝；未触发模型调用。

Handoff: sent to 安全边界席复核，并回传产品规划席；安全 PASS 与总负责人批准前不得创建实例或 binding。
