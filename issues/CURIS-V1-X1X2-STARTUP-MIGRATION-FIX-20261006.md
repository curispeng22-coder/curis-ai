# CURIS V1 — X1/X2 启动迁移自检误伤治理 + 数据态联调目验 Issue

Status: Review
Authority Class: CURRENT / IMPLEMENTATION ISSUE
Disposition: ACCEPTED / CLOSED（2026-10-06，R2 独立 QA PASS，GAP2 闭合，S4-QA-1 随之闭合）
Task ID: CURIS-V1-X1X2-STARTUP-MIGRATION-FIX-20261006
Parent: CURIS-V1-VISUAL-BASELINE-IMPLEMENTATION-20261005（总控）§17 S4 唯一保留 P2（S4-QA-1：X1/X2 数据态目验受阻）
Owner: Main Development
Decision Owner: Curis V1 Delivery Owner
Created: 2026-10-06
Authorization: Owner 2026-10-06「按这个方案执行」（X1/X2 联调窗口治理：迁移冲突修复 + 隔离数据根灌真实业务数据后补数据态像素目验）

## 1. Objective

修复后端启动时 workspace package 实例唯一约束迁移的自检误伤，使含历史遗留 FK 孤儿行的库副本可连续 cold start；随后在**仓库外隔离数据根**经 canonical API 灌入真实业务数据，补齐 X1/X2 数据态像素目验（组织三视图 / 会议真实徽章 / DT 报告列表 / CeoDesk 主视图 + 三业务真实 workspace），闭合总控 S4 保留 P2。

## 2. Root Cause（只读调查已核实，2026-10-06）

- `PackageConflictError` 定义于 `backend/app/workspace_package_runtime.py:170`；抛出点为 `_migrate_instance_uniqueness()`（701–795）的 **L760 全库 `pragma foreign_key_check`**。
- 启动链：`main.py:6044 create_app()` → `main.py:5732 build_workspace_package_router` → `workspace_package_api.py:62` 构造 Runtime → 抛错 → `main.py:6048 SystemExit(1)`。
- 触发机制：隔离副本继承源库 legacy 孤儿行（`artifacts/workflows/tool_traces` 等自演化表引用已删除 task）；**首次启动**父表不存在 → L728–732 早退成功并建表；**二次启动**父表已是新形状，流程推进到 L760 全库检查，被与 package 无关的孤儿行炸掉。已用 /tmp 副本实证：first boot OK / second boot FAIL。

## 3. Scope / Allowed Files

| # | 文件 | 拥有的改动范围 |
|---|---|---|
| 1 | `backend/app/workspace_package_runtime.py` | 仅 `_migrate_instance_uniqueness()` 内两个 hunk：(a) 把「已是新形状」早退（现 L764–766）移至 L760 全库 FK 检查**之前**（schema 形状/依赖校验全部保留在早退之前）；(b) L760 与 L784 两处全库 `pragma foreign_key_check` 改为对 parent + 4 children 逐表 `pragma foreign_key_check(<table>)`。其余逻辑（快照比对、integrity_check、回滚、FK 设置恢复）逐字不动 |
| 2 | `backend/tests/test_workspace_package_runtime_p0.py` | 新增回归用例：①无关表孤儿 + 父表新形状 → 启动成功；②package 域表（parent/children）孤儿 → 仍拒绝；③旧形状 + 无关表孤儿 → 真实重建成功且表级 FK 校验保留。不得改动既有用例断言语义 |
| 3 | `artifacts/tasks/CURIS-V1-APP-VISUAL-INTERACTION-COMPLETION-20261005/development-return/` | 证据输出：X1X2_RETURN.md、X1X2_QA_REPORT.md、灌数脚本（x1x2-seed.*）、截图 shots-x1x2/、指纹记录 |

其余文件零改动。frontend、desktop、受保护 DB、Frozen 文档均不在范围内。

## 4. 明确不做

- 不清理 legacy 孤儿行（属数据卫生，另立 backlog，本 Issue 不碰任何受保护 DB 内容）。
- 不改 `main.py` 启动链降级（掩盖真实损坏的方案 B 已否决）。
- 不动 frontend / desktop / 测试既有断言 / Git；不调用真实云模型（会议种子用本地/test provider 绑定）。
- 灌数只在 `/tmp` 隔离数据根；禁止 migrate/init/seed 任何仓库内 DB。

## 5. 灌数 Canonical 路径（调查确认）

1. 组织三视图：`POST /api/workspace/quickstart`（`workspace_quickstart_api.py:168`，一步建 company+dept+project+employee）。
2. 三业务 workspace：`POST /api/workspace/packages/install`，`source_path` 指 `backend/app/bundled_workspace_packages/{writing_authoring,content_growth,music}`（参考 `test_canonical_business_spine_runtime.py:200-229`）。
3. knowledge_entries：`POST /api/workspace/knowledge/entries`（`main.py:3042`）。
4. 会议：`POST /api/workspace/runtime/foundation/companies/{cid}/meetings`（`meeting_router.py:86`）；种子范式 `backend/scripts/e2e_meeting_real_deepseek.py:94-171`（绑本地 provider，禁真实云调用）。
5. outcomes / DT 报告：cycle 流 `runtime_foundation_router.py:650→676→702→1085`；读出 `GET .../operating-intelligence`（:556）；CeoDesk 用 `GET /api/workspace/v1/presentation` + `GET /api/workspace/ceo/operating-day`。

合规隔离启动：`CURIS_DB=/tmp/<root>/curis.sqlite CURIS_ENV=test CURIS_IDENTITY_MODE=test CURIS_WORKSPACE_PACKAGE_STORE=/tmp/<root>/workspace-packages .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8017`。

## 6. 验收证据

- 含孤儿的 /tmp 副本**连续两次 cold start 成功**，无 `PackageConflictError`。
- 修复前后同一副本 `pragma foreign_key_check` 输出一致（未掩盖、未改数）。
- 新增回归测试通过；`backend/tests/test_workspace_package_runtime_p0.py` 全文件测试 PASS。
- 四数据态对应 GET 均 200 且含真实条目。
- X1/X2 像素目验：四数据态 + 三业务真实 workspace × light/dark/system × 1440×900/1280×800 截图（shots-x1x2/），无白屏/编译错误/横向溢出；独立 QA 执行并出报告。
- 全程 `backend/data/curis.sqlite` 等受保护 DB 指纹不变；无 Git 写操作。

## 7. Stop 条件

修复 hunk 超出 §3 范围；测试需改既有断言语义；灌数必须触碰仓库内 DB；发现第二处启动阻断（先回报再决策）；需真实云模型/外部费用。

## Task Output Manifest

| 输出 | Disposition |
|---|---|
| issues/CURIS-V1-X1X2-STARTUP-MIGRATION-FIX-20261006.md（本文件） | ACTIVE |
| development-return/X1X2_RETURN.md | REVIEW_REQUIRED（实施后） |
| development-return/X1X2_QA_REPORT.md + shots-x1x2/ | REVIEW_REQUIRED（独立 QA 后） |

### 独立 QA 登记（2026-10-06，R1）

Verdict：**CONDITIONAL PASS**。报告：development-return/X1X2_QA_REPORT.md（37 张截图 shots-x1x2/ + probe-results.json、boot5-qa.log、fk_check_qa_boot5.txt、X1X2_DB_FINGERPRINTS_QA.txt、gets-qa/）。

- 修复维度全过：两文件 SHA256 与 POSTHASH 逐字一致，diff 仅授权两 hunk（早退移位 + 两处逐表 FK 检查），测试纯增量；p0 全文件 5 passed；同库第 5 次 cold start 成功、零 PackageConflictError；FK 对照未掩盖未改数（12 行 legacy 孤儿逐字一致，package 域 5 表逐表全 0，父表 legacy unique 约束确认移除）。
- 灌数维度全过：四 GET 均 200 含真实条目（组织 2 部门/5 员工/4 业务；会议徽章字段齐；operating-day matters=1/timeline=8；presentation 200）。
- 像素矩阵质量项全绿：37 张（7 页 × light/dark × 双视口 + system 抽样 9 张）无白屏/编译错误/横向溢出，主题 token 逐张正确（light 紫 #806be5 / dark 绿 #32f08c / system 随 CDP emulate）；三业务真实 workspace 渲染 PASS。
- **GAP1（复验属实）**：cycle→outcomes/DT 报告受 codex-cli agent 基底 409 阻断，reports=0，reports 页呈诚实 mock；维持 backlog 登记，不阻塞。
- **GAP2（QA 新发现，灌数路径缺口，非修复回归）**：quickstart 不建 FOUNDING_RUN/CEO_ASSISTANT，而 `_runtime_company_collection`（runtime_foundation_router.py:1588-1612）要求公司存在两实体才入列 → 前端 bootstrap 公司列表为空，四数据态页未呈现灌入数据（/ceo-office→302 /welcome、org/meeting 永久 loading、reports=mock）。canonical 补救只允许物化全新公司（materialize_for_existing_company 亦要求既有 CEO_ASSISTANT），无法回溯挂接 quickstart 公司。
- 指纹：8+1 受保护 DB 与 PRE/POST 逐行零变化；三进程与 /tmp 隔离根已清理；零 Git 写、零仓库改动、零真实云调用。

### GAP2 处置登记（2026-10-06，Owner 授权规则·工程判断直接推进）

裁定：**R2 补灌 founding-run 基底后复验四数据态像素维度**。依据：本 Issue §1 已授权目标即"经 canonical API 灌入真实业务数据，补齐数据态像素目验"，补灌属同一目标延续；零代码改动、零外部资源、仍只在 /tmp 隔离根。

- canonical 路径（已核实）：`POST /founding-runs` → transitions（capture_intent → request_clarification → propose_company → confirm_company）→ `POST /founding-runs/{id}/materialize-company`（foundation.py:390；物化全新公司 + CEO_ASSISTANT + builtin 组织，要求 run 处于 CEO_CONFIRMED）。R2 将全部种子数据（三 package、knowledge、会议）灌入物化的新公司，不再使用 quickstart。
- 影响告知：接受 = S4-QA-1 完全闭合（GAP1 DT 报告除外，维持 backlog）；不接受 = 四数据态页像素维度证据永久缺口，S4 保留 P2 无法闭合。
- R2 产物：x1x2-seed-r2.py、X1X2_QA_REPORT_R2.md + shots-x1x2-r2/（独立 QA 复验后登记）。

### R2 独立 QA 登记（2026-10-06）

Verdict：**PASS（GAP2 闭合）**。报告：development-return/X1X2_QA_REPORT_R2.md（27 张截图 shots-x1x2-r2/ + probe-results-r2.json、boot3-r2-qa.log、frontend-r2-qa.log、X1X2_DB_FINGERPRINTS_QA_R2.txt、gets-qa-r2/）。

- boot3-r2 同库独立 cold start 成功，零 PackageConflictError；六 GET 全 200，bootstrap-companies 含且仅含物化公司「X1X2 联调目验公司」（org 2部门/10员工/3业务、会议 WAITING_CEO 徽章+decision、OI metrics=4/reports=0）。
- 像素矩阵 **27/27 全过**（四数据态页 × 三主题 × 双视口 24 张 + 三业务 workspace 回归 3 张）：/ceo-office 不再 302→/welcome、org/meeting 脱离永久 loading 呈现真实数据、reports 维持诚实 mock（GAP1 维持 backlog，符合预期）；无白屏/编译错误/横向溢出，主题 token 逐张正确。
- 指纹：8+1 受保护 DB 与 QA/PRE/POST 三份逐行零变化；8017/3000 进程已 kill，/tmp/curis_x1x2 与 /tmp/curis_pw 已删；零仓库改动、零 Git 写、零真实云模型调用。

### Owner 接受登记（2026-10-06）

Owner Verdict：**ACCEPTED / CLOSED**。依据 R2 独立 QA PASS（GAP2 闭合，全部验收证据达成）+ 2026-10-06 授权规则（QA 通过后的接受属工程确认，直接登记）。R1/R2 全部证据 REVIEW_REQUIRED→PROMOTE 至本 Issue 证据链。GAP1（DT reports=0，无 canonical 生产路径）维持 backlog 登记，不随本 Issue 关闭。总控 Issue §17 S4-QA-1 同步闭合。
