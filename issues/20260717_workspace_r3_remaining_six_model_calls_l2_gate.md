# Workspace R3 剩余六步模型调用 L2 Gate

- 日期：2026-07-17
- 状态：BLOCKED_L2 — WORKFLOW_CONTEXT_BUDGET_REQUIRED
- Parent：`issues/20260717_workspace_r3_ai_rd_vertical_e2e.md`
- Run：`wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`
- Owner：产品规划席
- Next Seat：安全边界席 → 总负责人 → 系统交付席 → 质量运行席 → 产品规划席

## 先说结论

当前 Run 首 Step 已真实成功，剩余 Step 2→7 均为 model 类型，现有运行器没有无出网完成路径。产品选择复用既定真实模型路径，不新增临时本地执行器；现申请把该 Run 的调用上限从 1 次精确扩大到 7 次，即最多再执行 6 次，严格一 Step 一次、顺序推进、失败即停。

## 固定执行顺序

仅允许当前 Run 按 pending 最小顺序执行：

1. `requirement_clarification`
2. `architecture_design`
3. `frontend_execution`
4. `backend_execution`
5. `qa_verification`
6. `final_report`

不得跳步、并行、重置 succeeded Step、创建第二 Run 或改写历史记录。

## 保持不变的安全契约

- SHA：`718af2c463e39820ac6928681b16818a9fbccc25`。
- tenant / project / binding / Run scope 全部不变。
- Provider / Gateway / Model：`OpenAI / newapi / gpt-5.4-mini-2026-03-17`。
- 唯一受控出口、隐藏 Key 注入、可信 CEO UsageContext、日志脱敏不变。
- 每次输入 8,192、输出 2,048、总 Token 10,240；60s；0 重试；429 不重试；无 Fallback。
- 每个 Step 最多一次 outbound；任一失败、超限、身份/资源错配或审计失败立即停止，不继续下一 Step。

## 成本边界

- 已发生首步真实成本：`USD 0.001707`。
- 按批准价格，单次 Token 理论最大成本：`USD 0.01536`。
- 剩余 6 次理论最大成本：`USD 0.09216`。
- 整个 Run 理论最大累计成本：`USD 0.093867`，仍低于既有 R3 总成本硬上限 `USD 0.10`。
- 因此本 Gate 不申请修改价格或成本上限；累计成本达到 `USD 0.10` 前必须 fail-closed。

## 安全边界席必须确认

1. 调用额度按当前 Run + 精确 Step 计数，而不是放宽为任意 Workflow 或任意重复调用。
2. 已 succeeded 的首 Step 永久计数；每个剩余 Step 最多一次 outbound，已有 UsageEvent 时再次请求必须拒绝。
3. 每次调用前重新验证 active membership、可信 CEO、tenant/company/project/run/binding、当前最小 pending Step 与前序 succeeded。
4. 预算按该 Run 所有成功/失败 outbound 的累计成本检查；价格、Token 或审计缺失均不得继续。
5. 失败后 Run/Step 保持真实终态；禁止自动重试、人工重置、Fallback 或继续后续 Step。
6. 日志和持久化继续禁止 Key、Authorization、Cookie、完整 subject、prompt、原始响应和模型原文。
7. 执行结束后立即停止含凭据环境。

## 实施边界

- 只允许为上述精确 Run/Step 次数约束所需的最少后端与 focused tests。
- 不改模型、网关、出口、价格、成本上限、前端、Admin、Workflow 定义、Artifact 或项目状态实现。
- 实施与 focused 验证阶段不注入 Key、不启动真实环境、不调用模型。
- 安全 PASS 和总负责人批准后，系统交付席实施；质量运行席按一次一 Step 顺序执行，任何一次失败即停止并回传。

## 验收

- focused 无出网测试证明：正确下一 Step 允许一次；重复、跳步、错 Run、错 scope、前序未完成、累计预算超限均在 Adapter 前拒绝。
- 真实执行必须形成 Step 2→7 各自唯一 StepResult、UsageEvent、Token、模型和成本；最终 Run=succeeded、final_report 非空。
- 本 Gate PASS 只闭合七步执行，不代替 Parent R3 的独立 Artifact 与项目状态落点验收。

## 安全复核

- Security Review：`reviews/20260717_workspace_r3_remaining_six_model_calls_security_review.md`。
- 结论：`PASS`（仅六步有限调用安全契约，不等于已执行）。
- 可信 CEO 映射前置已由正式 `CLOSED — PASS` 证据解除。
- 固定顺序、单 Run + Step 计数、失败即停、0 重试、无 Fallback、逐步 scope / CEO / 预算 / UsageEvent 校验成立。
- 未实施、未启动、未注入 Key、未出网；等待总负责人批准。

## 总负责人批准

- 决策：`APPROVED`。
- 仅当前 Run `wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc` 从已消费 1 次扩大到全 Run 最多 7 次。
- 仅剩余 6 个 Step 各一次、固定顺序、0 重试、无 Fallback、失败即停；不得跳步、重置或创建第二 Run。
- 身份、可信 CEO、tenant/project/binding、Provider/Model/Gateway、出口、Token 和总成本硬上限 `USD 0.10` 全部不变。
- 先完成最小实现与无出网 focused 验证；完成前不启动、不注入 Key、不出网。

## 实施前真实阻塞

- 当前 Run 所属部门只有 Tech Lead 员工及 binding `bind-e222f21e-09de-43a6-aff5-0c1ae8b6555d`。
- Step 2→6 所需 Product Manager、Architect、Frontend Engineer、Backend Engineer、QA Engineer 均缺合法 Employee 与 capability binding；在“binding 不变”契约下 Step 2 会在 Adapter 前失败。
- 系统交付席未修改文件、未启动、未注入 Key、未出网，未通过放宽角色/绑定校验绕过。
- 总负责人维持 `BLOCKED_L2`，不批准自动新增员工或 binding；须先完成 `issues/20260717_workspace_r3_remaining_role_employee_binding_set_l2_gate.md` 的精确契约与单独审批。

## 角色集合已完成后的唯一阻塞

- 五角色 Employee + binding 数据集合已质量 `PASS`，合计 6 Employee + 6 active binding。
- 当前模型闸门仍只接受单一 `CURIS_R3_APPROVED_CAPABILITY_BINDING_ID`：保留 Tech Lead binding 会拒绝 Step 2 的 PM；改成 PM binding 又会让首步 Tech Lead UsageEvent 审计失配。
- 不允许通过关闭历史审计校验或让一个 binding 跨角色复用解决。
- 唯一下一步：完成 `issues/20260717_workspace_r3_exact_binding_scope_set_l2_gate.md`，把批准 scope 从单 binding 精确升级为当前 Run 的固定 role→binding 集合。

## 固定 Binding 集合已收口

- 子 Issue：`issues/20260717_workspace_r3_exact_binding_scope_set_l2_gate.md`，状态 `CLOSED — PASS`。
- 固定修订：`250fc6833e5b40ca5876d63bea654c6b407a1cef`。
- 六角色集合、历史首步审计、Step 唯一选择、全量 scope、累计预算、缺失/重复/错配 fail-closed 均通过无出网质量复核。
- 唯一下一步：系统交付席准备包含 `CURIS_R3_APPROVED_CAPABILITY_BINDINGS` 的隐藏 Key 启动命令，并只读复核当前 Run 仍为 Step 2 pending、已调用 1 次、累计成本未越界；负责人启动后由质量席逐 Step 执行，失败即停。

## 最终启动前置

- Preflight PASS：SHA `250fc6833e5b40ca5876d63bea654c6b407a1cef`；Run=running；Step 1 succeeded；Step 2 为唯一最小 pending；Step 3→7 pending。
- 已有 outbound=1、累计成本 `USD 0.001707`；历史 Tech Lead binding、模型、价格、可信 CEO、company/project 审计完整。
- 6 Employee / 6 role / 6 active unique binding 完整；端口和相关容器全部关闭。
- 最终更正命令已通过 Bash syntax、Compose 9 项环境合并、六角色 JSON 精确相等、0600 临时文件清理验证；未启动、未读 Key、未调用。
- 负责人只可执行系统交付席最后一条“更正上一条命令的转义展示”版本；上一条含反斜杠的展示作废。

## 安全启动确认

- 负责人已确认固定 SHA 与六角色 binding 集合环境启动成功；Key 未通过消息、Issue、Review 或仓库传递。
- 质量运行席只可对当前 Run 从 Step 2 开始按固定顺序最多调用 6 次；每次调用后必须核对当前 Step succeeded、唯一 UsageEvent、binding、Token、成本与累计预算，再进入下一 Step。
- 任一调用失败、超限、scope/审计异常或状态不一致立即停止；不得重试、重置、跳步或创建第二 Run。
- 结束后无论 PASS/BLOCKED 都必须先交系统交付席停止含凭据环境，确认端口/容器全部关闭后再回产品规划席。

## 真实执行结果与唯一阻塞

- Step 2→5：各自唯一 Gateway HTTP 200，Step/StepResult/UsageEvent succeeded。
- Step 6 `qa_verification`：唯一调用 HTTP 422，原因 `input exceeds approved limit`；`outbound=0`，未重试。
- Step 7 未调用；Run 终态 failed。
- 本 Run 成功 outbound 总数 5（含首步），累计 7,758 tokens，累计成本 `USD 0.01516350`。
- 环境已停止并独立确认端口、容器和后台进程全部清空。
- Review：`reviews/20260717_workspace_r3_remaining_six_model_calls_l2_gate_review.md`，结论 `BLOCKED_L2`。
- 当前失败 Run 不得重置、重试、删除或改写。唯一下一步：完成 `issues/20260717_workspace_r3_workflow_context_budget_l2_gate.md`，解决前序输出无限累积导致的输入超限；之后另行审批新 Run。
