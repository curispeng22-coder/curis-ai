# CURIS-V1-OI-ANALYST-REPORT-AUTHORING-20261007

## 1. 目标 / Objective

P2「GAP1 后续：analyst authoring + reports 接线」切片——补上 Operating Intelligence 已 ACCEPTED 缺口登记表中的有界缺口「automated analyst/report authoring」（[V1-P1-012 验收登记](../docs/reviews/CURIS_V1_OPERATING_INTELLIGENCE_IMPLEMENTATION_ACCEPTANCE.md) §Evidence boundary / [Productization Review](../docs/reviews/CURIS_V1_OPERATING_INTELLIGENCE_PRODUCTIZATION_REVIEW.md) §19 / [Execution Backlog](../docs/reviews/CURIS_V1_EXECUTION_BACKLOG.md) P2「Insights external Outcome/Feedback and automated analysis/report authoring」）。

产品契约已在 Frozen Blueprint 存在（非本切片新设计）：报告由 Company Analyst 围绕范围/周期/来源/证据完成；Report 至少记录范围、周期、责任、作者员工、部门/业务、触发、数据源、Model/Agent provenance、创建时间与复核；正文分 FACT / INTERPRETATION / UNKNOWN / RECOMMENDATION / EVIDENCE。

现状调研（Implementation Truth，2026-10-07）：

- **投影侧已 ACCEPTED**：[operating_intelligence.py](../backend/app/operating_intelligence.py) `read()` 投影 `analysis_report` artifact（L132-138）、`_reports()` 内容契约校验（L300-318：scope/period/facts/analysis/unknown/recommendation/evidenceRefs/author/createdAt 必填）、`submit_report_decision()` P7 决策连续性（L320-407，decisionCandidate 严格校验已验收）。
- **生产零 authoring 路径**：全 backend 仅测试 fixture（[test_operating_intelligence_projection.py:102-138](../backend/tests/test_operating_intelligence_projection.py)）创建 `analysis_report` artifact；`ResultStore.save_artifact` 默认 `execution_result`，无任何生产调用方传 `analysis_report`。投影/决策链就绪但永远无真实输入。
- **Analyst 解析已 canonical**（D09 已闭合）：L144-154 用 `department_assignments` + `responsibilityKey=data.analytics.company_analysis` 取唯一 Holder，不靠 role 文本；非唯一/缺失时如实回退中性占位。
- **执行底座就绪**（GAP1 首切片 2026-10-07 DONE/QA PASS）：tenant_private agent 能力经安全分派器真实执行（local-cli/mcp/http/codex-cli/openai-compatible）+ ai_usage 统一记账；`Orchestrator.run(task_id)` 为现有生产任务执行路径（main.py 多处 `asyncio.to_thread(asyncio.run, orchestrator.run(task_id))` 范式）；员工→能力绑定在 `employee_capability_bindings`（capability_source/capability_type/capability_id/enabled，[music_service.py:54](../backend/app/music_service.py) 有同款消费先例）。

本切片目标：接通 **CEO 手动触发 → Analyst 员工经其已绑定能力真实撰写 → 结构校验 → `analysis_report` artifact 落库 → 既有投影/P7 决策链直接消费** 的后端全链。触发为手动 API（最小诚实切片）；自动/周期调度、UI 按钮、外部 Outcome connector 均明确交后续门。

- Authority Inputs：
  - Product Truth（Frozen）：Product Blueprint 经营洞察节（报告契约、作者员工、Model/Agent provenance）。
  - Owner 缺口登记：V1-P1-012 acceptance / Productization Review §19 / Execution Backlog P2（见上）。
  - Implementation：GAP1 分派器（[agent_executor_dispatch.py](../backend/app/agent_executor_dispatch.py)）、[orchestrator.py](../backend/app/orchestrator.py)、[result_store.py](../backend/app/result_store.py) `save_artifact`、报告内容契约（本 Issue §1 现状调研）。
- Status: Draft → 实施后 Review。Disposition: REVIEW_REQUIRED。

## 2. Allowed Files / Directories

- `backend/app/analyst_authoring.py`（**新增**：authoring 服务，单一真源）
- `backend/app/api/runtime_foundation_router.py`（仅新增：`build_runtime_foundation_router` 签名加可选 `task_runner=None` 参数 + 一个 POST 端点 hunk；既有端点零改动）
- `backend/app/main.py`（仅 L5652 `include_router` 调用处最小 hunk：传入 task_runner；其余零改动）
- `backend/tests/test_analyst_report_authoring.py`（**新增**）
- `artifacts/tasks/CURIS-V1-OI-ANALYST-REPORT-AUTHORING-20261007/**`
- 本 Issue、`docs/00_Context/CURRENT_STATE.md`、`docs/08_Change_Log/CHANGE_LOG.md`（仅追加）

禁止：operating_intelligence.py 投影/决策既有逻辑改动（若实测必须微调，STOP 并登记追认）；orchestrator.py / result_store.py / agent_executor_dispatch.py / capability_adapters.py 业务逻辑改动；前端任何改动；数据库 schema；真实 provider/CLI 二进制调用；Git 写。

## 3. 验收证据 / Acceptance Evidence

1. **authoring 全链（pytest + 独立 QA 双重）**：
   `POST /api/workspace/runtime/foundation/companies/{company_id}/operating-intelligence/reports`（body：可选 `business_id`、`days` 默认 30；`Idempotency-Key` 可选）→
   - 经 canonical Assignment 解析唯一 Analyst Holder（复用 operating_intelligence 同款解析，不重写选择逻辑）；非唯一/缺失 → 如实失败（能力/组织缺口语义，不猜人）。
   - 解析 Analyst `employee_capability_bindings` 已启用绑定（enabled=1，按 priority；model 或 agent）；无绑定/绑定能力非 active → 如实失败，**零任务零 artifact**。
   - 接地 prompt 只组装既有投影真源（metrics/scopes/evidence refs/company/business/period），authoring 服务自身不产出任何经营数据。
   - 创建任务（analyst employee + company/workspace scope + 绑定 capability 字段）并经由注入的 `task_runner`（生产 = orchestrator.run 同路径）同步执行。
   - 输出 JSON 严格校验 §1 报告内容契约（必填键齐全、provenance ∈ {FACT,POLICY,EVIDENCE,EST,UNK}、decisionCandidate 若存在则过 submit_report_decision 同级校验、evidenceRefs 非空且全部指向当前 Company scope 内已知 ref）；任一不合法 → 任务 FAILED、**零 artifact**、错误如实返回。
   - 合法 → `save_artifact(artifact_type="analysis_report", source_ref="operating-analysis:authoring[:<idempotency-key>]")` 落库；响应返回 artifact + task + 报告内容。
   - GET 投影随即出现该报告（复用既有 `_reports`，零投影改动）；decisionCandidate 合法时 `submit_report_decision` 直接可消费（P7 连续性回归）。
   - ai_usage 账本恰好一条 success 记录（capability_id 精确、capability_type=agent/model、task_id 匹配）。
2. **幂等**：带相同 Idempotency-Key 重复 POST 返回同一 artifact，不产第二任务/第二 artifact/第二账本记录。
3. **诚实失败矩阵**：无 Analyst Assignment / 多 Holder / 无启用绑定 / 绑定非 active / 能力执行失败 / 输出契约不合法 / evidenceRefs 越界——逐一如实错误，零假报告零半成品 artifact。
4. **测试**：新增 pytest 覆盖 §1 全分支（含桩 agent 真实子进程执行范式，沿用 GAP1 测试桩手法）；与 test_operating_intelligence_projection 合跑全绿；全量回归失败集与改动前精确基线 IDENTICAL（零新增）。
5. **独立 QA**：隔离 sqlite + 隔离端口 + /tmp 白名单桩 CLI（GAP1 桩复用范式）；端到端 HTTP 跑通 authoring→投影→decision 全链；冷重启后报告/决策持久；零真实外发（forbidden 网关守卫）；PREHASH=POSTHASH（受保护文件）；DB 探针核对 artifact/usage/decision 行数；清理进程/端口//tmp。
6. **登记**：QA_REPORT + DEVELOPMENT_RETURN（含「不做项」：自动/周期调度、authoring UI、外部 Outcome/Feedback connector、Business Analyst 广域 allocation、真实 provider 语义）；Issue §6、CURRENT_STATE、CHANGE_LOG 追加。

## 4. 输出

- analyst_authoring.py + runtime_foundation_router.py 端点 hunk + main.py 接线 hunk + 新 pytest；
- `artifacts/tasks/CURIS-V1-OI-ANALYST-REPORT-AUTHORING-20261007/qa/QA_REPORT.md`、DEVELOPMENT_RETURN.md；
- Issue §6 Execution Record、CURRENT_STATE、CHANGE_LOG 追加。

## 5. Stop 条件

- 发现必须改动 operating_intelligence.py 既有投影/决策逻辑、或 result_store/orchestrator/分派器业务逻辑 → STOP 登记追认，不静默改。
- 发现报告落库需要新 schema/primitive（artifact 表现有字段不足）→ STOP ARCHITECTURE REVIEW。
- 发现产品意图实为自动/周期调度 authoring 而非手动触发 → STOP 上报产品裁定（本切片只授权手动触发）。
- 发现 analyst 绑定解析与现行 canonical Assignment 语义冲突 → STOP，上报 Authority 冲突。
- 需要真实外部 provider/CLI 才能验收 → 不做，用桩证据交差并如实标注 NOT RUN。

## 6. Execution Record

**2026-10-07 — 实施 + 独立 QA 完成。Status: Draft → Review。Disposition: REVIEW_REQUIRED（工程确认登记，待 Owner 接受）。**

实施（均在 §2 Allowed Files 内）：

- 新增 `backend/app/analyst_authoring.py`：authoring 单一真源——`department_assignments` 解析唯一 Analyst Holder（非唯一/缺失如实 422）→ 启用绑定解析（priority 首个；无绑定/非 active/official 非 model 如实 422，零任务零 artifact）→ 执行归属 workspace 解析（business→该业务首个 RESOLVED workspace；company→公司首个，无则 422）→ 接地 prompt（只组装既有投影真源）→ WORK 实体直插 SQL（RuntimeFoundation.create 无 WORK 状态机，采 child_work 同款形状 PLANNED/UNVERIFIED/MISSING，仅作账本归因落位）→ ResultStore 任务 + canonical 身份桥（identity_bound + team.execution_task_bound）→ 注入 task_runner 同步执行（生产 = orchestrator.run 同路径）→ 报告契约严格校验（必填键 / provenance 枚举 / evidenceRefs 非空且全部 in Company known_refs 否则 RuntimeScopeError / author==analyst / decisionCandidate 过 P7 同级校验）→ save_artifact(analysis_report, source_ref=operating-analysis:authoring[:<idempotency-key>])。
- `runtime_foundation_router.py` 最小 hunk：签名加可选 `task_runner=None`、OperatingReportAuthoringIn（extra=forbid）、POST `/companies/{company_id}/operating-intelligence/reports`（task_runner 未接线→503；端点内显式错误映射 404/403/422/500，共享 safe() 零改动；既有端点零改动）。
- `main.py` 单处 hunk：include_router 传入 `task_runner=lambda task_id: asyncio.run(orchestrator.run(task_id))`。
- 新增 `backend/tests/test_analyst_report_authoring.py`：10 个测试覆盖 §3.1 全链（业务+投影+P7 决策+幂等+账本精确归因）、幂等重放、公司级、Holder 缺失/多 Holder、无绑定、绑定非 active、执行失败、契约不合法、证据越界、跨租户 404。

验收证据（§3 逐条）：

1. **authoring 全链**：pytest 10/10 PASS；独立 QA full phase 37/37 marks PASS（qa/harness_evidence.json）——端到端 HTTP 跑通 authoring→投影→P7 决策全链，ai_usage 恰好一条 success（capability_id 精确、type=agent、task_id 匹配、canonical 归因经 identity_bound/execution_task_bound 双事件）。
2. **幂等**：相同 Idempotency-Key 重复 POST 返回同一 artifact，零第二任务/第二 artifact/第二账本记录（pytest + QA M4 双重）。
3. **诚实失败矩阵**：无 Holder / 多 Holder / 无绑定 / 绑定非 active / 执行失败（零 artifact + 任务非 COMPLETED）/ 契约不合法 / evidenceRefs 越界（RuntimeScopeError→404）/ 跨租户 404——逐一验证。
4. **测试**：新增 10/10；Issue §3.4 点名合跑（+ test_operating_intelligence_projection）16/16；全量回归 48 failed / 1878 passed / 3 skipped。**IDENTICAL-FAIL-SET 逐项比对 PASS**：手工摘除本切片 4 处 hunk 构造改动前精确基线重跑得 48 failed / 1868 passed（与 GAP1 登记基线一致），基线与当前失败集逐项 diff 为空（零新增零消失，证据 qa/FAILSET_BASELINE.txt / FAILSET_CURRENT.txt）；比对后 4 文件恢复、sha256 指纹逐项一致（qa/RESTORE_SHA256.txt）、authoring 10/10 复绿。
5. **独立 QA**（qa/，隔离 sqlite + 端口 8031 + stub claude CLI + ModelGateway http_post 硬失败守卫）：full 37/37、冷重启 restart 9/9（报告/决策/账本持久）、PREHASH=POSTHASH IDENTICAL（13 链上文件零漂移）、零真实 Provider（forbidden-outbound.log 不存在）、零 5xx、DB 探针 P1-P7 全过。QA_REPORT.md 结论 **PASS**。
6. **登记**：QA_REPORT.md + DEVELOPMENT_RETURN.md（含不做项）+ 本 §6 + CURRENT_STATE + CHANGE_LOG 追加。

已知边界（如实登记，均不阻塞本切片验收）：公司级报告执行归属公司首个 RESOLVED workspace（投影 business_id 由落位推导属既有契约）；CliAdapter 非零退出为 pass-through 语义（orchestrator 不因此 FAIL 任务，账本如实记 cli_exit_N）；test 身份模式固定 role=test，403 分支在 HTTP 层不可测（改验跨租户隔离）；多 Holder 无自动仲裁；真实 Provider 语义 NOT RUN（桩证据交差）。

不做项（交后续门）：自动/周期调度、authoring UI、外部 Outcome/Feedback connector、Business Analyst 广域 allocation。

输出清单与 Disposition：analyst_authoring.py / runtime_foundation_router.py hunk / main.py hunk / test_analyst_report_authoring.py → REVIEW_REQUIRED（待 Owner 接受）；artifacts/tasks/CURIS-V1-OI-ANALYST-REPORT-AUTHORING-20261007/** → 保留于任务工区（证据），待 Owner 裁定 PROMOTE/ARCHIVE。
