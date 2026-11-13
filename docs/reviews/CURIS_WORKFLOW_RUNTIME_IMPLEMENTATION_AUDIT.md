# CURIS WORKFLOW / RESPONSIBILITY RUNTIME AUDIT

Authority Class: REVIEW  
Status: Review  
Disposition: PENDING CEO REVIEW  
Date: 2026-08-19  
Audit type: READ-ONLY IMPLEMENTATION TRUTH  
Repository snapshot: `b4344972562484692fb93a05720cccde371a2504`

## 1. Executive conclusion

Curis 当前不存在一个统一的 `Responsibility Assignment + Default Flow + Dynamic Routing`
Runtime。仓库里同时存在四类彼此独立的执行机制：

1. `WorkflowRuntime`：**A. Deterministic Sequence**。官方 Software R&D Template 明确是
   `process_type=sequential`；Runtime 每次取第一个 `pending` Step，前一步失败则整个 Run
   失败，不读取 Edge / Condition / Next / Return。
2. `Orchestrator`：一个 Task 内部的确定性 Tool Step 序列。它可以暂停到
   `AWAITING_INPUT / HUMAN_HANDOFF`，但这里的 Handoff 是同一个 Task 的人工接管状态，
   不是 Workspace Responsibility 转移。
3. `TaskGraph + PipelineRuntime`：**B. DAG / Graph Routing**，支持依赖、就绪节点、重试、
   换能力、有限重规划与 CEO escalation；它是单独注册的 Pipeline 子系统，不是当前
   Workspace Workflow / Responsibility Runtime。
4. `WorkspaceRuntime`：RD 与 XHS 已有真实、持久化、**Domain-scoped** Responsibility、
   Artifact Review、Handoff、Decision Packet 和 Result 引用。它局部接近
   **C. Responsibility-driven Routing**，但路由规则写在 RD/XHS Domain 方法中，不从
   通用 Workflow Edge 或 Canonical Responsibility Assignment 动态求解。

因此，若以“整个仓库”分类，只能称为**多个机制并存**；不能称为一个已实现的 E Hybrid
Workflow。若问题特指 `/api/workspace/workflows` 的当前 Workflow Runtime，答案是明确的
**A：强制顺序执行**。

当前真实距离目标模型仍有一个核心断层：Role、Employee、Step Assignment、Workspace
`workContext`、Domain Handoff 都已存在，但尚无统一持久化的
`Employee × Role × Scope = Responsibility Assignment`，也没有根据 Result / Problem /
Need 动态选择下一 Assignment 的 Router。`CURRENT_STATE.md` 已将 Leadership Assignment、
Assignment-scoped Conversation、Result 回收和自动 Next Operating Cycle 明确列为
Product → Implementation Gap。

## 2. Audit boundary and evidence

### 2.1 Current implementation evidence

- `docs/00_Context/CURRENT_STATE.md:56-74,90-102,208-252`
- `issues/RD-WORKSPACE-INSTANCE-001.md`
- `reviews/RD-PHASE-2B-ARTIFACT-REVIEW-001_review.md`
- `reviews/RD-PHASE-2B-HANDOFF-001_review.md`
- `reviews/RD-PHASE-2B-P7-DECISION-001_review.md`
- `reviews/RD-PHASE-2B-E2E-CLOSURE-001_review.md`
- `reviews/SHARED-EMPLOYEE-EXECUTION-TRUST-001_review.md`
- `reviews/PRESERVED-MIXED-SOURCE-INTEGRATION-BASELINE-001_review.md`
- 当前源码、Schema 和 focused tests，具体位置见下文。

`CURRENT_STATE.md:262` 只说明 long-running reliability closure 本身不能升级 Phase 2B；
后续独立 Phase 2B Reviews 和 clean-baseline integration commit 已提供 Artifact Review、
Handoff、P7 与 Provider-native ACK 的 bounded acceptance。两者按 Issue scope 阅读并不冲突，
但 Current State 尚未把这些独立 Phase 2B 结果汇总成一个简明条目，属于状态汇总滞后。

### 2.2 Historical comparison only

`docs/pmo/workflow.md` 与 `docs/team-v2/WORKFLOW.md` 仅按本 Audit 要求用于历史对照；它们
不是 Current Runtime Authority。

### 2.3 Actions not performed

- 未运行或写入任何数据库；活动 SQLite 未打开。
- 未运行测试；本报告引用当前源码测试与正式 Accepted Review 中已有证据。
- 未修改源码、Schema、Product Authority、Frozen Contract 或其他文档。
- 未 stage、commit 或 push。

## 3. Current Workflow Runtime truth

### 3.1 Official Workflow is a mandatory sequence

`backend/app/database.py:2607-2658` 将官方研发 Template 固定为 7 个有序步骤；
`backend/app/database.py:2662-2665` 保存 `process_type='sequential'`。
`backend/app/workflow_runtime.py:67-71` 拒绝非 `sequential software_rnd` Template。

执行时：

- `backend/app/workflow_runtime.py:441-448` 取 `run.steps` 中第一个 `pending` Step；
- `backend/app/workflow_runtime.py:449-451` 发现任何已失败 Step 就失败整个 Run；
- `backend/app/workflow_runtime.py:505-509` 只有全部 Step 成为 `succeeded/skipped` 才完成；
- `backend/tests/test_phase6_workflow_mvp.py:61-72,74-139` 明确断言 sequential Template 和
  7 个固定 Role 顺序。

这里的 `step_order` 是 **Mandatory Runtime Route**，不是 Default Handoff Hint。
Schema/Runtime 中没有 Workflow Edge、Condition、Next、Return 或动态 Role 选择。

### 3.2 Workflow Node actual fields

| Layer | Actual fields | Runtime truth |
| --- | --- | --- |
| `workflow_templates` | `id`, `name`, `description`, `source`, `tenant_id`, `department_type`, `process_type`, `steps_json`, `status`, timestamps | `process_type` 被强制检查为 `sequential`；`steps_json` 生成有序 Step。见 `database.py:866-879`、`workflow_runtime.py:67-71`。 |
| Template Step JSON | `step_order`, `step_type`, `step_name`, `employee_role`, `required_capability_types`; `wt_rd_pipeline` 的 code Step 另有 `code_change_spec` | 通用 `WorkflowRuntime` 持久化并执行前四项；它不读取 `required_capability_types` 来做集合匹配，只取 Employee 的 preferred binding。`code_change_spec` 由独立 legacy `RdWorkflowRuntime` 使用。见 `database.py:2609-2658,3031-3050`。 |
| `workflow_steps` | `workflow_step_id`, `tenant_id`, `workflow_run_id`, `step_order`, `step_type`, `step_name`, `employee_role`, `status`, `input`, `output`, `error`, `started_at`, `completed_at`, timestamps | 全部是当前顺序执行记录。见 `database.py:913-930`。 |
| `step_assignments` | `step_assignment_id`, `tenant_id`, `workflow_step_id`, `employee_id`, `employee_role`, `capability_binding_id`, `status`, `created_at` | 是真实 Step execution assignment；不是 Product 语义的 Responsibility Assignment。见 `database.py:932-941`、`workflow_runtime.py:728-748`。 |
| `step_results` | `step_result_id`, `tenant_id`, `workflow_step_id`, `employee_id`, `result`, `status`, `created_at` | 前序结果被后续 Step Context 读取。见 `database.py:943-951`、`workflow_runtime.py:794-814`。 |

明确不存在于该 Workflow Node/Step Schema：

- `responsibility_id` / `responsibility_assignment_id`
- `next` / `return`
- `edge` / `condition`
- `next_role` / `next_employee`
- `owner` / `leader`
- 多 Capability / Tool / Model refs（只有一次实际选中的 `capability_binding_id`）
- Conversation scope

### 3.3 Employee Binding enters execution directly through Role

当前通用 Workflow 的真实调用链是：

```text
Workflow Step
  -> employee_role
  -> first enabled employee_instances row matching tenant + department + role
  -> employee preferred capability binding
  -> step_assignments row
  -> AIEmployee.execute_step()
  -> executions + step_results
```

证据：

- Role 查 Employee：`workflow_runtime.py:523-537`；
- 取 preferred Capability：`workflow_runtime.py:453-457`；
- 建 Step Assignment：`workflow_runtime.py:469,728-748`；
- 执行并归因：`workflow_runtime.py:480-499,943-961`。

它不是：

```text
Node -> Role -> Responsibility -> Assignment -> Employee
```

因为这条链中没有独立 Responsibility 或 Scope Assignment 记录。`step_assignments` 只绑定
一次 Workflow Step execution。

## 4. Other execution mechanisms must not be conflated with Workflow

### 4.1 Orchestrator: one Task, sequential internal steps

`backend/app/orchestrator.py:32-106` 为一个 Task 生成/读取 Workflow Plan；
`orchestrator.py:310-431` 在同一个 Task 内按 List 顺序执行 Step。每个 Step 完成后把完整
`previous_output` 和累计文本上下文传给下一 Step；最终 `result_store.py:287-352` 更新同一
Task 的 Workflow 状态，`orchestrator.py:118-142` 保存一个最终 Execution 并把 Task 标为
`COMPLETED`。

这条链没有 Role/Responsibility Assignment。它是 Agent/Tool orchestration substrate。

### 4.2 TaskGraph/Pipeline: real DAG, separate subsystem

`backend/app/task_graph.py:69-108` 的 Node 有 `deps/input_refs/output_ref/trigger/
cap_requirement/employee_id/status`；`task_graph.py:164-190,218-268` 实现 Edge、Ready 和
Topological Order。`backend/app/pipeline_runtime.py:94-191` 对单 Node 做执行、审核、重试、
换能力、有限重规划；`pipeline_runtime.py:272-313` 把耗尽结果登记为 CEO escalation。

但是：

- `backend/app/main.py:5271-5275` 将它作为单独 Pipeline Router 注册；
- 它不消费 `workflow_templates/workflow_steps/step_assignments`；
- 它不消费 Workspace `workContext.responsibilityEmployeeRef`；
- 它的 `employee_id` 用于 CapabilityResolver 偏好，不形成
  `Employee × Role × Scope` Assignment；
- 它的 escalation 是 Pipeline failed node → CEO record，不是
  Employee → Workspace Leader → Business Leader → Department Leader → CEO。

所以仓库中“存在 DAG”不等于 Current Workspace Workflow 是 DAG。

### 4.3 Task human handoff: same Task control state

`backend/app/task_execution_control.py:236-300` 将同一 Task 标为 `HUMAN_HANDOFF`，保存
`current_step/question/context_summary/handoff_assignee_id/resume_parameters` 并允许 accept 或
reassign。`orchestrator.py:373-393` 在 Agent 返回 `human_handoff` signal 时触发这条路径。

它：

- 不创建 `HANDOFF` Runtime Entity；
- 不改变 Workspace Responsibility Holder；
- 不创建新 Task；
- 接受后仍需显式 resume 同一个 Task；
- 是 execution-control pause，不是业务责任交接。

## 5. Workspace Responsibility truth

### 5.1 Current persisted model

Shared Runtime 使用通用 `runtime_entities` 与 `runtime_links`：字段包括 tenant/company/
workspace/parent/owner/lifecycle/presence/capability/execution/version/evidence/data JSON，见
`backend/app/runtime/models.py:138-183`。该表能承载 `ROLE_SLOT`、`AI_EMPLOYEE`、`HANDOFF`、
`DECISION_PACKET`、`EVIDENCE` 等对象，但并没有专门的 Canonical
`RESPONSIBILITY_ASSIGNMENT` entity/table。

RD/XHS 当前通过 Domain Object 的 `data_json.workContext` 持久化：

- `responsibilityEmployeeRef`
- `responsibilityRoleSlotRef`
- `currentExecutorRef`
- activity/status/systemActivity

这是已实现的 Domain-scoped current responsibility projection，不是可跨 Workspace 动态求解
的通用 Assignment Registry。

### 5.2 RD real execution assignment

RD 的执行链以 Cycle `workContext` Holder 为业务责任事实，再通过现有 Role/Capability Binding
选择唯一 Agent Runtime；`backend/app/runtime/workspace.py:1433-1449` 解析执行 assignment，
`workspace.py:1451-1494` 只在真实执行开始时设置 Current Executor。

真实 Provider execution 还经过：

```text
Runtime AI_EMPLOYEE (canonical business identity)
  -> explicit Company Employee execution bridge
  -> persisted Task assignment event
  -> active Capability Binding
  -> Provider Task / Session / usage.task_execution
  -> verified callback provenance
```

证据：`backend/app/employee_execution_identity.py:41-100,102-149,220-321`。
Responsibility Holder、Current Executor、Company execution Employee 和 callback actor 被严格
区分；Provider callback 不能自行改变 Holder。

### 5.3 Artifact Review is not Handoff

RD Artifact Review 是 Cycle-scoped `artifactReview` persisted record：

- `workspace.py:1563-1629` 创建 Request，保留 `originalHolderRef`，指定真实 Reviewer；
- `workspace.py:1631-1673` 只把 Review 的 Current Executor 设为 Reviewer；
- `workspace.py:1705-1795` 保存 Reviewer Task Result、Evidence 与 Result refs；
- Developer Responsibility Holder 不变。

`reviews/RD-PHASE-2B-ARTIFACT-REVIEW-001_review.md` 的真实 Codex evidence 证明第二个 Reviewer
Task 存在，但 Handoff/Decision count 均为 0。

## 6. Handoff truth

### 6.1 RD Responsibility Handoff is real and persisted

RD 的 Handoff 是一个真实 `HANDOFF` Runtime Entity，并同时在 Cycle `data_json` 保留
projection：

1. **Producer**：API/CEO 显式给出目标 Employee、责任摘要和原因；
   `workspace.py:1992-2075` 验证目标是同 Workspace、不同且 AVAILABLE 的 Employee，创建
   `CREATED` Handoff。
2. **Send**：`workspace.py:2077-2122` 将同一对象转为 `SENT`；Holder 此时不变。
3. **Consumer/ACK**：CEO/manual response 或 Provider-native verified ACK 调用
   `workspace.py:2124-2235`。
4. **Provider trust**：`employee_execution_identity.py:323-367` 验证当前 SENT target、
   canonical Employee bridge、Task、Capability、UsageEvent 和 Provider Session；Verifier 本身
   不转状态。Router 在 `runtime_foundation_router.py:820-850` 验证后调用 Domain transition。
5. **Transfer point**：只有 `ACKNOWLEDGE` 完成时，
   `workspace.py:2192-2201` 才把 Holder/RoleSlot 改为接收方；Current Executor 仍为 none。

### 6.2 What RD Handoff does not do

- 不依据 Workflow Edge 选择目标；目标由请求显式给出。
- 不读取 `step_order/next/return/condition`。
- 不自动创建下一 Task 或 Execution。
- Provider-native ACK 要求事前已有匹配目标 Employee 的 Provider Task/Session；Handoff
  transition 自身不产生该 Task。
- `RETURN/REJECT` 保留原 Holder；这是真实回退结果，但不是通用 Workflow Back Edge。
- 没有路由到 Workspace/Business/Department Leader 的通用方法。

### 6.3 XHS automatic Handoff is real but domain-coded

XHS `ContentItem` 在创作执行完成后：

- 读取 `workContext.nextResponsibilityEmployeeRef`；
- 创建 `HANDOFF`，`inputRefs` 只传 ContentVersion，`outputRefs` 只传 Evidence；
- 在同一 Domain transaction 记录 `CREATED -> SENT -> ACKNOWLEDGED`；
- 将 ContentItem 从 `DRAFT` 推到 `IN_REVIEW`，把 Reviewer 设为 Holder/Executor。

证据：`workspace.py:3543-3631`。

这是一个已实现的固定专业域路由，不是从通用 Workflow Default Edge 动态选择。若缺少
`nextResponsibilityEmployeeRef`，Runtime 直接 fail closed。

## 7. Dynamic routing assessment

| Scenario | Current real behavior | Verdict |
| --- | --- | --- |
| 需求不清 → 产品 Role | 官方 sequential Workflow 固定第二步为 Product Manager；Task control 可暂停等待输入。没有执行中根据 Need 动态查找产品 Responsibility Assignment。 | PARTIAL |
| 架构问题 → 架构 Role | 官方 sequential Workflow 固定 Architect Step；没有从异常/Result 动态路由 Architect。 | PARTIAL |
| 测试失败 → 开发 Role | Pipeline 子系统可 retry/switch/replan；RD Cycle failure 可 PAUSE/RESUME 同一 Holder；但没有通用 QA Result → Developer Assignment Router。 | PARTIAL |
| 经营异常 → Leader | Scheduler/Pipeline 可记录 CEO escalation；Workspace 可创建 P7 Decision Packet。Workspace/Business/Department Leader Assignment chain 未实现。 | PARTIAL to CEO only / Leader chain NOT IMPLEMENTED |
| Decision Gate → CEO | RD 与 XHS 有真实 `DECISION_PACKET`，CEO choice 后 Domain Runtime 自动继续或转状态；Decision 明确不是 Handoff。 | IMPLEMENTED in accepted RD/XHS domains |

当前没有一个 Runtime 方法能接收任意 `Result / Problem / Need`，解析 Responsibility，查询
Scope Assignment，再选择下一 Employee。所谓 Dynamic Routing 只存在于明确 Domain command、
Pipeline capability fallback 或人工选择目标中。

## 8. Default flow / arrow / next semantics

当前有三种完全不同的“箭头”语义：

1. `workflow_steps.step_order`：**强制执行顺序**。不是 Hint。
2. `TaskGraph.deps`：**强制 DAG readiness dependency**。不是 Responsibility Handoff。
3. Workspace Domain 的 `nextResponsibilityEmployeeRef` / explicit Handoff target：**Domain-owned
   concrete target**。XHS 自动转给已配置 Reviewer；RD 由调用者显式选接收方。

当前不存在“Default Handoff Hint，可被 Runtime 按上下文跳过/改道”的通用字段或解释器。
Product 文档中的 Workflow arrows 若被理解为默认关系，Implementation 尚未支持该语义。

## 9. Task / Issue / Execution granularity

### 9.1 Legacy WorkflowRuntime

- 一个业务输入创建/复用 **一个 Task**；见 `workflow_runtime.py:163-165`。
- 一个 Task 对应一个 Workflow Run，Run 下有多个 Step。
- 每个 Step 创建一个 `step_assignments` 和一个 `executions` row；不会每 Step 创建新 Task。
- Step 之间复用同一 Task requirement，并读取前序 Step Results。
- 最后 Step 完成后 Run 生成 Final Report 并结束；不会自动创建下一工作。

### 9.2 Orchestrator

- 一个 Task 下连续执行多个 Tool Step。
- `AWAITING_INPUT/HUMAN_HANDOFF` 暂停同一 Task；resume 继续同一 Workflow Plan。
- 不为普通小故障自动拆 Task。

### 9.3 RD Workspace

- Developer real work：一个 Cycle 创建一个真实 Provider Task/Execution；同 Cycle 可按 accepted
  revision/P7 continuation 建新的 Task，同时把旧 refs 归档到 history。
- Artifact Review：明确创建第二个 Reviewer Task，因为它是独立 Employee 的独立执行，不是
  Handoff。
- Responsibility Handoff：Handoff 本身不创建 Task；Provider-native ACK 所需 Task 由调用方先
  建立并归因。

因此当前没有“每次 Handoff 必然拆新 Task”的全局规则。Task 数增加发生在真实独立 Provider
执行，而不是仅因 Holder 变更。

## 10. Context cost audit

### 10.1 Legacy Workflow context

`workflow_runtime.py:539-692` 为每个后续 Step 重新构造 Prompt：

- 重复当前 CEO requirement；
- 传当前 Step metadata；
- 传所有前序 Result 的 id/order/type/status/hash/reference metadata；
- 内联最近两个 Result body，并在剩余额度中内联更早结果；
- 使用全局 byte budget 截断。

这不是完整数据库复制，但每个 Step 都会重新发送一份 bounded historical context，Step 数增加
会带来重复 Token 成本。

`Orchestrator._build_step_input()` 在 `orchestrator.py:627-635` 直接带入 previous output 与
accumulated context，也有随 Step 增长的重复上下文成本。

### 10.2 Workspace Handoff context

RD Responsibility Handoff 主要传引用：`workspace.py:2047-2051` 的 `contextRefs` 指向 Task、
Review Request 和 Result refs；XHS Handoff 使用 `inputRefs/outputRefs` 指向 ContentVersion 与
Evidence（`workspace.py:3596-3609`）。这两条链本身不复制完整 Conversation/Artifact。

但是，接收方真正启动 Provider Task 时仍需由 Domain executor 解析 refs 并组装最小 Context。
当前 RD Artifact Review 会读取指定 Artifact 并把内容截断后注入 Reviewer Task
（`main.py:4846-4910`）；这是一项受控重建，不是共享 Assignment Context Runtime。

### 10.3 Cost conclusion

- **Workflow Step handoff**：存在重复 bounded context，频繁 Step 会放大 Token。
- **RD/XHS persisted Handoff**：Reference-first，Handoff record 本身成本低。
- **New Provider Employee execution**：仍会建立新 Task/Session并重建必要 Context；成本取决于
  Domain assembler，不存在统一 Context Package cache。
- **Assignment-scoped Conversation**：未实现，因此还不能证明跨 Assignment 只恢复必要上下文。

## 11. Leader and escalation truth

当前 Runtime 能识别的相关事实包括：

- legacy `department_instances.manager_employee_id`；
- Pipeline/Scheduler 的 CEO escalation record；
- RD/XHS `DECISION_PACKET owner_ref='CEO'`；
- Domain Cycle/ContentItem 的当前 Holder/Role Slot。

当前 Runtime 不具备：

- Workspace Leader / Business Leader / Department Leader 的 Canonical Responsibility
  Assignment；
- Problem/Result 沿 Employee → Workspace Leader → Business Leader → Department Leader → CEO
  的 scope-aware escalation chain；
- Result 自动回收到 Operating Leader；
- Leader 按 Assignment 继续/调整/升级/开下一 Cycle。

所以 Leader 参与 Runtime Routing 的结论是 **DOC ONLY / NOT IMPLEMENTED**。直接找 CEO 的
Domain Decision 和 Pipeline escalation 不能替代中间 Leader Assignment chain。

## 12. Result to next work

| Runtime | Result write | Next decision | End behavior |
| --- | --- | --- | --- |
| `WorkflowRuntime` | `step_results` + `executions`; final report 写 `workflow_runs.final_report` | 代码固定选择下一个 pending Step | 最后 Step 后 Run=`succeeded`，停止；不创建 Next Work。 |
| `Orchestrator` | workflow traces + execution + Task output/artifact | 同一 Plan 的 for-loop | Task=`COMPLETED/FAILED/PAUSED`，停止；不创建下一 Responsibility。 |
| `TaskGraph/Pipeline` | Node result/trace/project aggregate | ready deps + retry/switch/replan；耗尽时 CEO escalation | Graph 完成或停在 escalation；不是 Workspace Leader loop。 |
| RD Workspace | Artifact/Evidence/Result refs 写回 Cycle | 明确 API command：Review、Revision、Handoff、P7、Acceptance/Close | 可在同 Cycle 自动继续 accepted P7/revision；没有通用 Result Router 或自动 Next Operating Cycle。 |
| XHS Workspace | Evidence/Result refs 写回 ContentItem | Domain stage rules：Creator→Reviewer→CEO→Schedule | 专业域内自动继续；缺 Connector 时等待，不创建通用 Next Work。 |

是的，legacy Workflow 存在“最后一个节点完成 → Execution/Run 结束 → 全部停机”。RD/XHS 的
闭环更长，但其下一步由 Domain command/state hard-code，不由 Default Workflow Flow 解释器决定。

## 13. Historical five-seat comparison

历史 `docs/pmo/workflow.md` 定义产品规划席、总控决策席、系统交付席、质量运行席、安全边界席，
并强调 Single Main Execution Thread、Issue scope、紧凑 Handoff 和里程碑验收。

| Historical idea | Current code truth |
| --- | --- |
| 一个目标内连续诊断/修复/focused验证 | 在一个 Orchestrator Task 内连续 Step、RD 同 Cycle execution/revision 中仍可见；不是由五席 Runtime 实现。 |
| 普通小故障不逐席 Gate | Orchestrator 内部 retry/continue、Pipeline retry/switch/replan 保留这一思想。 |
| 质量独立审核 | RD Artifact Review 用真实 Reviewer Employee + 独立 Task 实现了相近产品能力，但不是历史“质量席”对象。 |
| 总控/CEO Gate | RD/XHS P7 Decision Packet、Pipeline CEO escalation 有替代实现；没有“总控决策席”Runtime identity。 |
| 安全边界 | Capability/Computer Access/Provider trust 以 Runtime guard 存在；没有安全边界席参与通用 Routing。 |
| Handoff 传最小引用 | RD/XHS Handoff refs 与历史 compact handoff 思路一致。 |
| 五席顺序流程 | 未作为当前 Runtime 模型保留；历史 seat names 不应映射成当前 Role/Employee。 |

保留的是“一个目标持续执行、必要时才升级、独立验收、最小交接”的运行思想；五席组织本身没有
成为 Current Runtime。

## 14. Current Runtime flows

### 14.1 Official Workflow endpoint

```text
[IMPLEMENTED] CEO/API creates Workflow Run + one parent Task
    |
    v
[IMPLEMENTED] ordered workflow_steps (process_type=sequential)
    |
    v
[IMPLEMENTED] first pending Step
    |
    v
[IMPLEMENTED] employee_role -> first enabled Department Employee
    |
    v
[IMPLEMENTED] preferred Capability Binding -> step_assignment
    |
    v
[IMPLEMENTED] AIEmployee.execute_step -> execution + step_result
    |
    +---- failure ----> [IMPLEMENTED] Step + Run failed; stop
    |
    +---- success ----> [IMPLEMENTED] next ordered pending Step
                              |
                              v
                       [IMPLEMENTED] final_report; Run succeeded; stop

[NOT IMPLEMENTED] Result/Problem -> Responsibility Assignment Router
[NOT IMPLEMENTED] Default Edge override / dynamic Role route
[NOT IMPLEMENTED] Operating Leader result recovery / Next Operating Cycle
```

### 14.2 Accepted RD Workspace path

```text
[IMPLEMENTED] Project / Cycle / workContext Responsibility Holder
    |
    v
[IMPLEMENTED] Role/Capability Binding + canonical Employee execution bridge
    |
    v
[IMPLEMENTED] Provider Task / Codex Session / Current Executor
    |
    v
[IMPLEMENTED] Artifact + Evidence + Result Reference; Executor clears
    |
    +--> [IMPLEMENTED] Artifact Review Request
    |        -> independent Reviewer Task
    |        -> review Evidence/Result
    |        -> original Holder unchanged
    |
    +--> [IMPLEMENTED] explicit RD Responsibility Handoff
    |        -> CREATED -> SENT -> verified/manual ACK
    |        -> Holder changes only on completion
    |
    +--> [IMPLEMENTED] P7 Decision Packet
             -> WAITING_CEO -> CEO choice -> APPLIED
             -> original Holder resumes existing async execution path

[PARTIAL] Next action requires Domain command/rule; no generic Responsibility Router
[NOT IMPLEMENTED] Leader Assignment chain / automatic Next Operating Cycle
```

### 14.3 Separate Pipeline path

```text
[IMPLEMENTED] Pipeline Plan -> TaskGraph nodes/dependencies
    -> ready node -> CapabilityResolver -> execute -> review
    -> retry -> switch capability -> limited replan
    -> done OR CEO escalation

[NOT IMPLEMENTED] integration with Workspace Responsibility Assignment/Handoff
```

## 15. Gap matrix

| # | Target | Verdict | Current evidence / gap |
| --- | --- | --- | --- |
| 1 | Role / Responsibility | PARTIAL | Workflow has `employee_role`; Workspace has Role Slot + `workContext` Holder. No canonical Responsibility object/definition used by a router. |
| 2 | Employee Binding | IMPLEMENTED | Workflow Role→Employee + Capability Binding; Workspace Role/Employee/Capability and canonical execution bridge are real. Scope differs by runtime. |
| 3 | Responsibility Assignment | PARTIAL | `step_assignments` and Domain `workContext` are persisted, but neither is the current Product `Employee × Role × Scope` Assignment primitive. |
| 4 | Default Workflow Order | IMPLEMENTED, but mandatory | `step_order` and DAG `deps` are enforced routes. There is no Default Hint semantics. |
| 5 | Dynamic Handoff | PARTIAL | RD explicit target and XHS fixed next target are real; no Result-driven generic Assignment lookup. |
| 6 | Return / Retry | PARTIAL | Task resume, Pipeline retry/replan, RD Handoff return/reject and RD revision exist independently; no common Workflow return edge. |
| 7 | Leader Escalation | DOC ONLY | CEO escalation/Decision exists, but Workspace/Business/Department Leader Assignment chain does not. |
| 8 | Result → Next Work | PARTIAL | Legacy Flow advances fixed Step; RD/XHS Domain rules can continue. No generic Result Router or automatic Next Operating Cycle. |
| 9 | One Goal / Continuous Execution | PARTIAL | One Task can run several internal Steps; RD can continue in same Cycle. It stops at terminal Run/Cycle and does not guarantee cross-cycle continuous operation. |
| 10 | Context-efficient Handoff | PARTIAL | RD/XHS Handoff is reference-first; Workflow/Orchestrator rebuild bounded textual history; no shared Assignment Context assembler. |
| 11 | Assignment-scoped execution | PARTIAL | Real Step assignment, Task Employee provenance and Domain Holder/Executor exist; no canonical scope Assignment governs all execution. |
| 12 | Assignment-scoped conversation | DOC ONLY | Domain Cycle/ContentItem stores conversation summaries, but no Conversation keyed/routed by canonical Responsibility Assignment. `CURRENT_STATE.md:99` records the gap. |

## 16. Direct answers A–G

### A. 当前 Workflow 是不是强制顺序执行？

是。`WorkflowRuntime` 只接受 sequential Software R&D Template，并按第一个 pending Step 强制
推进。仓库另有独立 DAG Pipeline，但它不是该 Workflow Runtime。

### B. 箭头 / Next 的真实 Runtime 语义是什么？

Workflow 的真实语义是 `step_order` mandatory sequence；Pipeline 的 Arrow 是 `deps` mandatory
readiness；Workspace Handoff 目标是明确 Employee ref。当前没有 Default Handoff Hint。

### C. 当前是否已按 Responsibility 动态调度？

没有全局实现。RD/XHS 有 Domain-scoped Holder/Executor/Handoff/Decision，属于局部、明确规则；
没有根据任意 Problem/Need 动态查找 Assignment 的通用 Router。

### D. Employee Binding 实际如何进入执行？

Legacy Workflow：Step Role 直接查 Department Employee，再取 preferred Capability Binding。
Workspace RD：Role/Capability Binding + Runtime Employee Holder，经 canonical identity bridge 映射到
Company execution Employee，再创建真实 Provider Task/Session并验证 callback provenance。

### E. 当前 Handoff 是否会产生频繁 Task / Context 切换？

Handoff record 本身不会自动创建 Task。RD Provider-native ACK 需要事前真实目标 Task；Artifact
Review 会因独立 Reviewer execution 创建新 Task。Workspace Handoff 传 refs，成本较低；新的
Provider execution 仍需重建必要 Context。Legacy sequential Step 不拆 Task，但每步重发 bounded
历史文本。

### F. 旧五席哪些运行思想仍在？

一个目标连续执行、普通失败就地 retry、独立 Reviewer、必要时 CEO Gate、最小 refs Handoff、
scope/security guard 仍能在不同 Runtime 中找到。五席身份、固定 seat route 和旧组织流程没有成为
Current Runtime。

### G. 距离 `Responsibility Assignment + Default Flow + Dynamic Routing` 还有多远？

现有底座已经具备 Role Slot、Employee、Capability Binding、Holder/Executor 分离、真实 Provider
provenance、Domain Handoff、P7 Decision、Artifact/Evidence/Result refs。缺的不是执行器，而是三项
连接能力：

1. Canonical scoped Responsibility Assignment persistence/read model；
2. Workflow Default relationship（Hint 而非 mandatory sequence）的明确 Runtime representation；
3. Result/Problem/Need → Assignment resolution → next Employee/Leader 的动态 Router，以及
   Assignment-scoped Conversation / Result recovery / Next Operating Cycle。

在这三项完成前，空间工程或 Workspace UI 即使画出 Role/Arrow，也不能宣称 Runtime 已按责任动态
调度。当前成熟度应定义为：**domain-proven responsibility transfer on top of multiple execution
substrates; no unified responsibility-routing runtime**。

## 17. Review stop state

`CURIS WORKFLOW RUNTIME — CURRENT IMPLEMENTATION AUDITED — WORKFLOW EXECUTION SEMANTICS IDENTIFIED — HANDOFF / ROUTING TRUTH IDENTIFIED — CONTEXT COST PATH IDENTIFIED — NO IMPLEMENTATION CHANGES — STOP FOR CEO REVIEW`
