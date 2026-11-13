# CURIS-V1-COMPOSER-ACCESS-READONLY-20261007

## 1. 目标 / Objective

F1 Composer 七控件真实化的下一步：将 Shared Composer 的「访问权限」固定槽位从统一的「访问权限 · 即将推出」假占位，升级为**只读、消费服务端真值**的诚实投影（Frozen Shell §3.5「访问权限（固定显性入口）：必须消费真实 Computer Access / Provider 权限能力；不支持的权限不得伪造为可选」；ADR-0046 用户侧真值状态）。

当前对话执行链只允许显式桥接的**模型绑定**（CONVERSATION_REPLY，P0 已验收），External Local Agent 不参与对话执行、ADR-0046 明确「当前不实现 Runtime，不修改真实 Agent 权限」。因此本切片所有可达状态都是只读的：模型执行 → 不适用；无桥接 → 无法确认。**不提供三档选择、不产生 requested_intent、不改任何 Agent 权限**。

「工作模式」「Auto」「语音」不在本切片：工作模式被产品合同阻塞（无 Runtime 模式真值源）；Auto 无对话级真值/API 且本地后台合同标 NOT IMPLEMENTED；语音离线版需外部资源（whisper sidecar/模型下载/麦克风声明）。三项在 DEVELOPMENT_RETURN 中作为 Owner Decision Gate 上报。

- Authority Inputs：
  - Frozen：[Curis_Workspace_Shell_Contract_And_Shared_Patterns.md](../docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md) §3.5（2026-08-17 Delta-X10）
  - Frozen：[ADR-0046](../docs/07_Decisions/ADR-0046-local-agent-computer-access-authority.md)（User-facing truth states；Requested≠Configured≠Effective；当前不实现 Runtime）
  - Backlog/Evidence：V1_APP_COMPLETION_INVENTORY F1（「访问权限：先只读落 Composer 为 S/M；✓ effective 如实 UNKNOWN」）、CURRENT_STATE backlog。
- Status: Draft → 实施后 Review。Disposition: REVIEW_REQUIRED（Owner 接受 Gate）。

## 2. Allowed Files / Directories

后端：

- `backend/app/conversation_service.py`（新增只读投影方法）
- `backend/app/api/conversation_router.py`（read/topic_read 载荷附带 `computer_access`）
- `backend/tests/test_conversation_computer_access.py`（新增）

前端：

- `frontend/lib/computerAccess.mjs`（新增，ADR-0046 真值→普通语文案纯映射）
- `frontend/components/v1/SharedConversation.js`（新只读槽位组件；默认导出传模型不适用真值）
- `frontend/components/v1/EmployeeConversation.js`（消费服务端 `computer_access`）
- `frontend/components/workspace/SharedEmployeeWorkArea.js`（控件行去重，改由固定槽位投影既有 `composer.computer_access` 真值）
- `frontend/components/delivery/d1/EmployeeConversationView.js`（同上，去重并由槽位投影）
- `frontend/tests/computerAccessSlot.test.mjs`（新增）
- `frontend/tests/d1EntryCompatibility.test.mjs`（越界追认：SSR 测试 seam 的 localRequire 增加 computerAccess.mjs 映射，2 行）

登记与任务区：

- `artifacts/tasks/CURIS-V1-COMPOSER-ACCESS-READONLY-20261007/**`
- 本 Issue、`docs/00_Context/CURRENT_STATE.md`、`docs/08_Change_Log/CHANGE_LOG.md`（仅追加）

禁止：main.py 挂载改动（router 已挂载）、任何写端点/requested_intent 持久化、Agent Adapter/权限 Runtime、工作模式/Auto/语音控件行为、产品 Frozen 文档、Git 写。

## 3. 验收证据 / Acceptance Evidence

1. 后端：GET 员工对话与 topic 载荷含精确形状 `computer_access`（extra 字段受控）：有启用模型桥接 → `state="MODEL_EXECUTOR_NOT_APPLICABLE"`、`selectable=false`、effective/verification=`NOT_APPLICABLE`；无桥接员工 → `state="NO_EXECUTION_BRIDGE"`、`UNKNOWN/UNVERIFIED`；CEO-only 对话（无员工）同模型不适用；跨公司读取维持 404。
2. 后端：`execution_models` 载荷形状与现有测试断言**零变化**；新增 pytest 全绿，且与 test_employee_conversation.py / test_conversation_productization.py 合跑全绿。
3. 前端：ConversationComposer 不再出现「访问权限 · 即将推出」；槽位为 disabled 只读按钮，普通语文案 + title 真值说明；模型宿主（CEO 助理/General Workspace/会议/Writing/D1/WorkArea 模型员工）显示「模型不适用」，无桥员工显示「无法确认」，已有 CONFIGURED/GRANTED 快照的 Agent 员工显示对应真值（已配置待确认/已验证）；不渲染任何 select/可点击选项。
4. 前端：node --test 新增与既有 composer/conversation/d1 测试全绿；eslint 0 error；`npm run build` 成功；CSS 仅用 --ui-* token（无新色值硬编码）。
5. 独立 QA：隔离 sqlite + 独立端口 + 真实 Chromium，覆盖三类宿主（CEO 助理、有桥/无桥员工对话、WorkArea 展开）；DOM 断言槽语文案/非交互/无「即将推出」；API 形状与跨公司 404；PREHASH=POSTHASH 对 §2 之外产品文件零改动声明；受保护 DB 指纹前后一致；零外发。
6. 回归：Music/Writing QA 后基线不回退（后端关联测试合跑、前端全量既有失败集与登记一致）。
7. 清理：进程退出、端口释放、/tmp 删除；DEVELOPMENT_RETURN 含 Task Output Manifest 与 Auto/语音/工作模式 Decision Gate。

## 4. 输出

- 服务端真值投影 + 前端只读槽位 + 两侧测试；
- `artifacts/tasks/CURIS-V1-COMPOSER-ACCESS-READONLY-20261007/qa/QA_REPORT.md` 与 DEVELOPMENT_RETURN；
- Issue §6 Execution Record、CURRENT_STATE、CHANGE_LOG 追加。

## 5. Stop 条件

- 发现需要写 requested_intent 或改 Agent 权限才能满足宿主 → STOP（超出 ADR-0046 Runtime 边界）。
- 发现对话执行链已接入 Agent 型绑定而投影无法诚实表达 → STOP 上报，不自造 Adapter 真值。
- Owner 未对 Auto/语音方向决策前，不实施这两项。

## 6. Execution Record（2026-10-07，Status: Review）

- 实现：后端两常量 + `ConversationService.computer_access()`（无 employee_ref 或存在启用模型桥接 → MODEL_EXECUTOR_NOT_APPLICABLE；否则 NO_EXECUTION_BRIDGE）；conversation_router 员工 read 与 topic_read 载荷附带精确 7 键投影。前端新增 lib/computerAccess.mjs 纯映射 + ComputerAccessSlot（disabled 只读按钮，--ui-* token）；默认 SharedConversation/EmployeeConversation/SharedEmployeeWorkArea/D1 EmployeeConversationView/WritingChapterMain 五宿主接线；移除 WorkArea/D1 控件行重复的旧 accessLabel 文案（本地详情面板与 d1State 单测依赖的旧函数保留未删）。
- 越界追认：frontend/tests/d1EntryCompatibility.test.mjs SSR seam 增加 computerAccess.mjs localRequire 映射（2 行，已在 §2 登记）。
- 测试：后端新文件 6/6、关联合跑 48 passed；前端新增 4/4，全量 208 pass / 9 fail（既有基线，与本切片无关）；eslint 0 error；生产 build 成功。
- 独立 QA：[artifacts/tasks/CURIS-V1-COMPOSER-ACCESS-READONLY-20261007/qa/QA_REPORT.md](../artifacts/tasks/CURIS-V1-COMPOSER-ACCESS-READONLY-20261007/qa/QA_REPORT.md) —— 41 marks 全过（API A1–A8 27、浏览器 B0–B3 14）+ 冷重启 A1–A8 复验；0 5xx、0 messages POST、零外发（forbidden-outbound.log 不存在）；PREHASH=POSTHASH（11 文件）、受保护指纹 before=after；隔离库无 computer_access 列、零 message 事件；8026/3025 已停、/tmp/composer-access-q1 已删。
- 证据边界：SharedEmployeeWorkArea 默认导出当前无页面挂载（A8 投影真值 + 单测覆盖，未伪造浏览器宿主）；D1 由 SSR seam + 同 props 接线覆盖；VERIFIED/CONFIGURED 文案分支由纯函数单测覆盖（当前栈无可验证 Agent 快照，不造数据）。
- Stop 事件：无。未写 requested_intent、未改 Agent 权限、未碰 main.py、无 Git 写。
- Owner Gate：工作模式 / Auto / 语音三项阻塞与多选一选项见 [DEVELOPMENT_RETURN.md](../artifacts/tasks/CURIS-V1-COMPOSER-ACCESS-READONLY-20261007/DEVELOPMENT_RETURN.md) §5；裁决前保持诚实占位。
- Disposition：11 个产品文件 REVIEW_REQUIRED（待 Owner 接受为 Implementation Truth）；任务工件 REVIEW_REQUIRED 留存。
