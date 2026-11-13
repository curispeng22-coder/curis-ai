# Issue — CURIS V1 Composer 模型选择贯通 + 引用全量化

Status: Accepted
Authority Class: IMPLEMENTATION ISSUE
Disposition: APPROVED / READY_TO_EXECUTE（Owner 2026-10-06 盘点 §6 决策 5 授权）
Task ID: CURIS-V1-COMPOSER-MODEL-REFERENCE-20261006
Recorded: 2026-10-06
Owner: Main Development
Decision Owner: Curis V1 Delivery Owner
依据：盘点 §2（控件 2/5）、§7-P0

## 1. Objective

1. **模型选择对员工对话真正生效**：现状 CEO 助理模型选择生效，员工回复只认员工绑定、忽略前端选择（backend/app/conversation_service.py prepare() 约 L426-434；MessageIn 无模型字段）；prepare() 已预留 execution_selection 接缝（约 L360、L389-399）。本切片将前端所选 provider/model 经合法 execution_selection 透传 gateway；**无选择时维持现语义（员工绑定→租户默认）**；选择在本租户未配置/无健康绑定→诚实错误，禁止静默回退假成功。
2. **「添加」引用全量化**：员工对话已有真实引用链（EmployeeConversation.js 约 L101；kind 白名单 conversation_router.py L9-18；≤8）。本切片让共享对话/员工对话的引用入口一致可达：可浏览并选择同工作区 WORK/RESULT/KNOWLEDGE（及现有合法 kind）、可见已选列表与删除、空态诚实；长文选区引用沿用 FOUR-FORM revision-02 口径（CEO 消息体 ≤2000 字，原文全量 basis 留 execution/provenance，不扩 8000 Shared 上限）。

**不在本切片**：文件/图片上传（multipart+Tauri 插件，P1 独立切片）；Agent 型员工对话执行（另一 M 切片）；访问权限/工作模式/Auto/语音；模型选择的服务端持久化（维持 sessionStorage+租户默认；如需加列→STOP）。

## 2. Allowed Files / Directories（开工前登记全部目标 SHA256）

- backend/app/conversation_service.py
- backend/app/api/conversation_router.py
- frontend/components/v1/SharedConversation.js
- frontend/components/v1/EmployeeConversation.js
- frontend/lib/ 下 conversation/model 相关模块（开工定位 exact 文件后登记 hash；如需新增辅助模块仅限同目录）
- backend/app/model_gateway.py（**仅在**接缝透传确需最小 hunk 时；优先零改动）
- backend/tests/、frontend/tests/ 下 conversation 相关测试（开工定位 exact 文件；新增测试文件限同目录）
- artifacts/tasks/CURIS-V1-COMPOSER-MODEL-REFERENCE-20261006/**

**不授权**：DB schema/migration（接缝已存在；发现必须加列→STOP）；其他五控件；其他业务域；8+1 受保护 DB；Git。

## 3. Acceptance Evidence

- pytest conversation 相关全绿 + 新用例：①员工对话带显式选择→gateway 实际收到该 provider/model（mock gateway 断言）；②无选择→员工绑定；③未配置/失效选择→明确错误、不 fallback、不扣费；④引用 kind 白名单、≤8、跨租户/跨公司/跨工作区拒绝；⑤长文选区 CEO 体 ≤2000、全量 basis 不出 Shared 消息。
- 真实 UI QA（隔离 root/DB 范式，NEXT_PUBLIC_API_BASE 指向测试后端，端口非 3000/3001 时配 CURIS_ALLOWED_ORIGINS）：员工对话选模型发送并在 UI 看到实际所用模型回执；引用选择器从两条对话入口可达、添加/删除/空态；长文选区引用；无真实云模型调用（Ollama/mock provider）。
- 前端构建/lint 通过；新代码一律 `--ui-*` token，禁硬编码 hex、禁依赖 Tailwind `dark:` 变体。
- 受保护 DB 前后指纹（8+1）；QA 期 frontend 冻结；结束 kill 进程、清 /tmp。

## 4. Stop Conditions

发现 execution_selection 接缝不足以承载（需持久化或改 schema）；发现引用授权服务（resolve_references）语义将被改变 → STOP 报告，不扩权。

## 5. Workload / 依赖

M + S ≈ 2–3 人日（含独立 QA）。无外部凭证依赖（本地 Ollama/mock）。与 FOUR-FORM 切片共享 frontend，须串行 QA。

## 6. Execution Record（2026-10-06，Owner 已 ACCEPT）

### 6.1 实际改动文件与 POST SHA256（[POSTHASH.txt](file:///Users/yy/Documents/Curis%20AI%20Workspace/artifacts/tasks/CURIS-V1-COMPOSER-MODEL-REFERENCE-20261006/POSTHASH.txt)）

| 文件 | POST SHA256 | 性质 |
|---|---|---|
| backend/app/conversation_service.py | `93a826f6bcc669192ac4574f89013901c5b1fc9bc12b611509943a3b66e39d3b` | Allowed |
| backend/app/api/conversation_router.py | `02a22abdd4d9f05256ce9aa0bfc26a5953f0adc5e972de28627601d76564dc30` | Allowed |
| frontend/components/v1/EmployeeConversation.js | `687816b5225c1c9f4aebba8a1c34735a86ab9b812bb0106a7bca4c1ca0b9b266` | Allowed |
| backend/tests/test_employee_conversation.py | `755717d038bbf1752035e5557145c9122a27e22e3f0bd37050f01326d55b2b71` | Allowed |
| backend/app/orchestrator.py | `36b60e0508f147600af76176bb4a3013d527e9edeeec425a2a7050d040c7c46a` | **§6.2 越界追认** |
| backend/app/main.py | `473ef5a3ee04f1232811f9d8ba0664cc770d7b9d46fef7d789265d7282c732e1` | **§6.2 越界追认** |

### 6.2 Allowed Files 越界登记（Owner 2026-10-06 已追认；不停工理由：执行链事实必需的最小 hunk）

§2 未列 orchestrator.py / main.py。实现中实证：仅在接缝与 DTO 透传后，新 purpose `CONVERSATION_REPLY` 仍被两处既有白名单拦截，不改则该 purpose 在系统内不可执行（白名单 fail-closed，非接缝可绕过）：

- `orchestrator.py`：`_writing_reply_selection()` purpose 白名单 + 单步 reply workflow 的 purpose→文案映射两处各加 `CONVERSATION_REPLY`（共 2 行级 hunk，L79/L225）。
- `main.py execute_model_gateway`：①执行前第二道服务端验证分流（CONVERSATION_REPLY 走 ConversationService.validate_conversation_selection，其余 purpose 原路径不变，L1170-1179）；②direct_conversation 标志跳过 grant 成本上限块、跳过 grant max_output_tokens 调用（走 `executor.execute(prompt)` 默认合同），outbound 幂等 claim 以 `conversation.outbound.claimed` 前缀纳入同一「一 Task 一物理尝试」机制，purpose 白名单/前缀映射各加一项（L1160-1161/L1268/L1279/L1281/L1290）。无 schema、无 grant、无 fallback 语义变化；既有 4 purpose 与无选择路径行为零变化（回归 77 测试全绿佐证）。

请 Owner 在接受时一并追认两文件；若不追认则本切片无法成立，需回滚整个切片。

**追认与接受（2026-10-06）**：Owner 已追认 orchestrator.py / main.py 两越界文件，并接受本切片（以指示「追认并继续执行 WQA-20 回程修复」为准）。QA 产物按 Output Manifest 由 REVIEW_REQUIRED 转为归档保留；本切片正式关闭。

### 6.3 交付内容

- **后端**：新 purpose `CONVERSATION_REPLY`（DTO extra=forbid、scope 必含 company_id+workspace_id、source 枚举）；服务端 fail-closed 校验（VERIFIED_EXPLICIT_BRIDGE + 绑定行 tenant/company_employee_ref/enabled/id/source/capability_id 全匹配 + scope 双校验）；source_class 服务端固定注入 EMPLOYEE_BINDING；幂等比较排除 source_class（同 selection 重试不冲突、换模型 409）；GET conversation / topic_read 返回 `execution_models`（显式桥+enabled，priority,id 排序）；无员工 topic 带 selection →409；orchestrator/main 执行链贯通（真实绑定、usage 唯一、fallback_from_model=NULL、provenance 回写）。
- **前端**（仅 EmployeeConversation.js，未改 SharedConversation/useConversationModel——CEO 助理 provider 选择不在本切片）：模型下拉数据来自 `view.execution_models`，仅员工对话显示；选择内存态（受既有静态测试约束禁 localStorage/sessionStorage），员工切换重置；发送 payload 带 execution_selection，retry 用 attempt 上的 selection 剥除 source_class 原样带回；绑定失效/409/404 分情况中文诚实错误；无桥员工琥珀提示；引用选择器两入口本已完整，仅回归验证未过度开发。
- **测试**：test_employee_conversation.py 新增 6 个用例（execution_models 列表、幂等/换模型、他人物理绑定/跨公司/停用拒绝、create_app+mock gateway 真实执行+usage 实证+409/422、无员工 topic 409、Q-1 生产形态回归）。conversation 三套件 + CG/Writing/Music selected-execution 等回归 **77 passed**；唯一失败 test_music_operating_chain 为既有 cwd 相对路径问题（仓库根下存在该 preimage 目录，从 backend/ 跑才报错，与本切片无关）。
- **前端静态/构建**：employeeConversation + conversationProductization 5/5 pass；`npm run build` 成功。全量 node 测试中 V1Sidebar「全局搜索暂未开放」断言失败为既有基线问题，未触碰该文件。

### 6.4 独立真实 QA：PASS 10/10

报告：[QA_REPORT.md](file:///Users/yy/Documents/Curis%20AI%20Workspace/artifacts/tasks/CURIS-V1-COMPOSER-MODEL-REFERENCE-20261006/qa/QA_REPORT.md)（隔离 root、:8023/:3023、双 mock 网关 :8031/:8032、17 截图、网关日志 13 次出站与 ai_usage_records 13 行全对账、fallback 全 NULL、负向零出站、8 受保护 DB 指纹零差异、进程/tmp 已清）。

**Q-1 处置（开发裁定：NOT A DEFECT，待 Owner 复核）**：QA 报无桥员工经员工详情页（公司员工 id）GET conversation 404。核查结论：生产全部 runtime AI_EMPLOYEE 创建路径（employee_templates 实例化、general_workspace_delivery L193-196、writing_entry_service L194-195）都写 `companyEmployeeRef`，owner() 现有反查已覆盖；QA 种子用 foundation.create 裸建了不带 companyEmployeeRef 的孤儿 runtime 实体（qa-rt-n≠qa-emp-n），该形态生产不可达，且 employee_instances 无反向列可关联孤儿实体，所建议反查无事实依据。已加生产形态回归测试 `test_unbridged_employee_with_company_ref_reads_via_detail_entry`（带 ref 的无桥员工经公司员工 id →200、execution_models=[]）。L-1（公司 C UNRESOLVED 造数限制）非缺陷。

### 6.5 遗留与下一步

- 无代码遗留。本切片完成后 P0 剩余：WQA-20 回程修复、CG 素材库+学习面。
- QA 产物 disposition=REVIEW_REQUIRED，Owner 接受后 PROMOTE/归档按 Output Manifest 处理。
