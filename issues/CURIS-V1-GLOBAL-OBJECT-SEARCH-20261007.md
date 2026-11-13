# CURIS-V1-GLOBAL-OBJECT-SEARCH-20261007

## 1. 目标 / Objective

Core P1「Global Object Search」首版切片——接通 Frozen Shell Contract 已冻结、但生产端诚实 disabled 的公司级对象搜索。

出处与 Authority：

- **Product Truth（Frozen）**：[Curis_Workspace_Shell_Contract_And_Shared_Patterns.md](../docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md) §1.5.4（S5 Company-wide Object Search，2026-08-15 APPROVED FOR FREEZE）：入口 = Navigation Pane Header 右侧 🔍 icon → Search Surface；语义 = Object-first, Task-capable；v1 = 基础对象搜索（输入 → 按对象类型分组结果）；RESERVED（不做）= 复杂 NL 关系查询 / AI 问答 / Command Palette / 高级过滤器 / 搜索语法。
- **Backlog 登记**：[Execution Backlog](../docs/reviews/CURIS_V1_EXECUTION_BACKLOG.md) 2026-09-09 Phase B closure「Remaining Core P1：Global Object Search」；2026-09-08 seven-area acceptance 登记 follow-up「global search remains truthfully disabled」。

现状调研（Implementation Truth，2026-10-07）：

- **入口与 Surface 壳已就位**：[WorkspacePaneShell.js](../frontend/components/workspace/WorkspacePaneShell.js) L153 Nav Header `搜索公司对象` icon（全部 ceo-office 页面经 [TerraShell.js](../frontend/components/terra/TerraShell.js) L54 消费本壳）+ L184-187 Search Surface dialog 当前为诚实 disabled 文案「全公司搜索尚未接入」；CSS `.searchShade`/`.searchDialog` 已就位（[WorkspacePaneShell.module.css](../frontend/components/workspace/WorkspacePaneShell.module.css) L25-27）；Esc/遮罩关闭与焦点回退已接线。
- **后端零搜索端点**：全 backend 无公司级对象检索路由。
- **可检索存储地图**（全部既有表，零 schema 需求）：`canonical_businesses`（Business）、`workspaces`（Workspace）、`runtime_entities` entity_type=`AI_EMPLOYEE`（Employee）/ `PACKAGE_DOMAIN_OBJECT`（Business Object）/ `DECISION_PACKET`（Decision）、`knowledge_entries`（Knowledge）、`strategy_meetings`（Meeting）、`tasks`（Task）、`artifacts`（Result/Artifact）。

本切片目标：**Nav Header 🔍 → Search Surface → 输入 → 后端只读聚合 → 按对象类型分组结果 → 点击进入对象** 的最小真实全链。空查询态显示诚实输入提示；**Recent（最近访问）与 Capability（Expert/Skill/Connector）两组本切片不做**（理由见 §3.2 注记），不伪造。

- Status: Draft → 实施后 Review。Disposition: REVIEW_REQUIRED。

## 2. Allowed Files / Directories

- `backend/app/object_search_service.py`（**新增**：只读聚合单一真源）
- `backend/app/api/object_search_router.py`（**新增**：单端点 router）
- `backend/app/main.py`（仅新增 include_router 最小 hunk；既有端点零改动）
- `backend/tests/test_object_search.py`（**新增**）
- `frontend/lib/objectSearchState.mjs`（**新增**：纯映射——分组标签/上下文文案/href 规则，可单测）
- `frontend/lib/v1FrontendApi.js`（仅新增 object-search 取数方法 hunk）
- `frontend/components/workspace/WorkspacePaneShell.js`（仅搜索 dialog 段 hunk：disabled 文案 → 真实 Surface；入口/Esc/遮罩既有逻辑零改动）
- `frontend/components/workspace/WorkspacePaneShell.module.css`（仅新增 Surface 结构类，全部 --ui-* token，禁止硬编码色值）
- `frontend/tests/objectSearch.test.mjs`（**新增**）
- `artifacts/tasks/CURIS-V1-GLOBAL-OBJECT-SEARCH-20261007/**`
- 本 Issue、`docs/00_Context/CURRENT_STATE.md`、`docs/08_Change_Log/CHANGE_LOG.md`（仅追加）

禁止：数据库 schema/新表/写路径/事件发射；Provider/CLI/外部调用；Shell Contract 与任何产品文件改动；既有端点与既有服务业务逻辑改动；Git 写；前端硬编码 hex。

## 3. 验收证据 / Acceptance Evidence

1. **后端只读端点** `GET /api/workspace/companies/{company_id}/object-search?q=…`：
   - company 不存在 → 404；跨公司隔离（B 公司对象零泄漏进 A 结果，逐组探针）。
   - `q` 去空白后为空 → 200 空分组（诚实，不报错）；长度上限（≤64 字符，超出 422）；LIKE 通配符（`%`/`_`/`\`）转义不注入。
   - 分组返回九类：**Business / Workspace / Employee / BusinessObject / Knowledge / Meeting / Decision / Task / Result**；每组上限 8 条，总量封顶；每条 `{type, id, title, context}`（context = 组织/业务归属，如「数据分析部 · 公司经营分析师」「内容增长办公室 · Note」）。
   - 零写、零事件、零新表、零外部调用；只读 SQL（sqlite_master 探针实证无新表）。
2. **类型覆盖与不做项**：
   - 九类逐类至少一条真实种子/构造对象可被搜到并按分组返回。
   - **不做（交后续门，Issue 登记理由）**：Recent 最近访问（需跨页面访问追踪真值源，sessionStorage 伪造访问史不诚实）；Capability 组（Expert/Skill/Connector 为租户级共享目录而非公司对象，「搜全目录 vs 公司已启用能力」语义需产品裁定，本切片不猜）；NL/AI/过滤器/语法（Frozen RESERVED）。
3. **前端 Search Surface**（替换 disabled 文案，复用既有 dialog 壳）：
   - 输入框 autofocus；输入即查（防抖）；分组渲染（组标题 + 图标 + 标题 + 上下文 + 类型标签）。
   - 键盘：↑/↓ 移动、Enter 进入选中对象、Esc 关闭（既有）；遮罩点击关闭（既有）；关闭后焦点回退触发 icon（既有）。
   - 底部提示条：「↵ 进入对象 · Esc 关闭 · 仅对象搜索 v1」。
   - 空查询态：诚实提示「输入关键词以搜索公司对象」；无结果态：诚实「未找到匹配对象」；后端错误态：诚实错误提示不静默。
   - 点击/Enter → 关闭 Surface 并跳转对象路由（href 规则集中在 objectSearchState.mjs 纯映射，逐类对既有路由核验：business→/ceo-office/business、workspace→/ceo-office/workspace/installed/[id]、employee→/ceo-office/organization/employees/[id]、knowledge→/ceo-office/knowledge/entries/[id]、meeting→/ceo-office/meeting、decision→/ceo-office/decisions、task→/ceo-office/execution/tasks/[id]、result→/ceo-office/reports/[id]、business_object→其归属 workspace 页）。
4. **测试**：后端新 pytest 覆盖 §3.1/§3.2 全分支；与关联合跑全绿；全量回归失败集与改动前精确基线 IDENTICAL（手工摘除 hunk 构造基线，失败集逐项 diff 为空 + 恢复指纹一致）。前端 objectSearchState 纯函数单测 + WorkspacePaneShell 搜索段静态断言；前端全量维持既有基线（204 pass / 9 既有失败，零新增）；切片文件 eslint 0 error；生产 build 成功。
5. **独立 QA**：隔离 sqlite + 隔离端口 + forbidden 网关零外发 + 真实浏览器：九类对象逐类构造→搜索→分组断言→点击进入对象页；跨公司零泄漏；空/无结果/错误三态；键盘全路径；冷重启后行为一致；PREHASH=POSTHASH（受保护文件）；零 5xx；DB 探针（无新表/无写行）；清理进程/端口//tmp。
6. **登记**：QA_REPORT + DEVELOPMENT_RETURN（含不做项）+ Issue §6 + CURRENT_STATE + CHANGE_LOG 追加。

## 4. 输出

- object_search_service.py + object_search_router.py + main.py hunk + test_object_search.py；
- objectSearchState.mjs + v1FrontendApi.js hunk + WorkspacePaneShell.js 搜索段 hunk + module.css 类 + objectSearch.test.mjs；
- `artifacts/tasks/CURIS-V1-GLOBAL-OBJECT-SEARCH-20261007/qa/QA_REPORT.md`、DEVELOPMENT_RETURN.md；
- Issue §6、CURRENT_STATE、CHANGE_LOG 追加。

## 5. Stop 条件

- 发现需要新 schema / 新表 / 新 primitive → STOP ARCHITECTURE REVIEW。
- 发现必须改动既有服务/投影/端点业务逻辑才能聚合 → STOP 登记追认，不静默改。
- 发现某类对象无 canonical 公司归属字段、隔离判定只能靠猜 → 该类如实移出本切片并登记，不放宽隔离。
- Owner/产品裁定 Capability 组或 Recent 必须进本切片 → STOP 上报产品裁定（本切片授权范围不含）。
- 需要真实外部 Provider/网络才能验收 → 不做，如实标注 NOT RUN。

## 6. Execution Record

**实施日期**：2026-10-07
**状态**：Accepted（全部验收证据通过）

### 6.1 交付文件

- `backend/app/object_search_service.py`（新增）— ObjectSearchService 只读聚合器，9 类对象，每组上限 8，LIKE 通配符转义
- `backend/app/api/object_search_router.py`（新增）— GET /api/workspace/companies/{company_id}/object-search?q=
- `backend/app/main.py`（hunk）— include_router(build_object_search_router(database))
- `backend/tests/test_object_search.py`（新增）— 8 tests
- `frontend/lib/objectSearchState.mjs`（新增）— OBJECT_GROUPS / groupMeta / objectHref 纯映射
- `frontend/lib/v1FrontendApi.js`（hunk）— searchCompanyObjects(companyId, query)
- `frontend/components/workspace/WorkspacePaneShell.js`（hunk）— 真实 Search Surface 替换 disabled 文案
- `frontend/components/workspace/WorkspacePaneShell.module.css`（hunk）— search surface 样式（--ui-* token）
- `frontend/tests/objectSearch.test.mjs`（新增）— 4 tests

### 6.2 验收证据

| 项 | 结果 |
|----|------|
| 后端 pytest | 8/8 pass |
| 后端全量回归 | 48 failed / 1886 passed（IDENTICAL-FAIL-SET，+8 新增） |
| 前端 eslint | 0 errors |
| 前端测试 | 4/4 新增 pass（9 既有失败不变） |
| 前端 build | 成功 |
| QA probe | 21/21 pass |
| 浏览器 QA | 搜索按钮→对话框→9 分组→键盘导航→Enter 跳转→Esc 关闭→焦点回退，全部通过 |
| 冷重启 | 行为一致 |
| 指纹 | PREHASH=POSTHASH（仅 Allowed Files 修改） |
| 零 5xx / 零新表 / 零外发 | 通过 |

### 6.3 不做项（已登记理由）

1. **Recent 最近访问组** — 需跨页面访问追踪真值源，sessionStorage 伪造访问史不诚实
2. **Capability 组** — Expert/Skill/Connector 为租户级共享目录，「搜全目录 vs 公司已启用能力」语义需产品裁定
3. **NL / AI / CommandPalette / 过滤器 / 语法** — Frozen Shell Contract §1.5.4 明确 RESERVED

### 6.4 QA 报告

详见 `artifacts/tasks/CURIS-V1-GLOBAL-OBJECT-SEARCH-20261007/qa/QA_REPORT.md` 与 `DEVELOPMENT_RETURN.md`。
