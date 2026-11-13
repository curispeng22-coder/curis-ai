# CURIS MASTER DEVELOPMENT STATE

Status: Draft
Authority Class: EVIDENCE / CURRENT (Implementation Truth snapshot)
Owner: Main Development Session
Date: 2026-09-03
Scope: BOOTSTRAP ONLY — 未修改任何代码 / 未 commit / 未 stage / 未 push / 未改动数据库

所有结论均来自本次实地勘察（文件、git、sqlite 只读查询、运行时探测），可直接作为证据引用。

---

## Project

- workspace: `/Users/yy/Documents/Curis AI Workspace`
- repository: `https://github.com/curispeng22-coder/curis-ai-workspace.git`（remote `origin`）
- branch: `main`
- HEAD: `c797db840` — `test(runtime): prove cross-professional multi-work operation`，2026-08-22 01:22:03 +0800，作者 `Curis Local Snapshot`
- git status: **686 个变更文件**
  - `??` 未跟踪 **566**，已修改 `M` **118**，已删除 `D` **2**，已 staged **0**
  - 目录分布：`docs/` 335、`backend/` 101（另 20 个带引号的 backend 路径）、`frontend/` 56、`issues/` 45、根目录 39、`desktop/` 22、`artifacts/` 22、`.workbuddy/` 20、`reviews/` 11、`data/` 7
- worktrees: **22 个**（`/private/tmp/*` 与 `~/.codex/worktrees/*` 中 17 个标记 `prunable`；本地 `.worktrees/` 4 个：ai-secretary-planning / company-runtime-office-view / phase1c-ceo-office-first-slice / phase1c-company-project-bootstrap-ui）
- stash: **1 条** — `On feat/093-readonly-catalog-routes: WIP: workspace in-progress shared-backend changes`

---

## Architecture

### frontend
- Next.js **16.2.10**（App Router）+ React **19.2.7** + Tailwind **3.4.17**，纯 JS（无 TypeScript），ESLint 9 + `eslint-config-next`
- 脚本：`dev` / `build` / `start` / `lint`；产物 `frontend/.next`，BUILD_ID `KCdDhovvCgSzdnX0d9db9`，构建时间 2026-09-02 02:51（评审记录 46 routes）
- 一级导航真源：`frontend/components/v1/V1Sidebar.js:10-18`，**7 项**，与产品基线完全一致：
  `CEO 工作台 /ceo-office` · `业务空间 /ceo-office/business` · `组织中心 /ceo-office/organization` · `人才与能力 /ceo-office/talent-market` · `经营洞察 /ceo-office/analytics` · `资料库 /ceo-office/knowledge` · `会议 /ceo-office/meeting`
- 颜色在组件内硬编码（`#806BE5`、`#dde2e7`），非 token 驱动；`components/terra/TerraIcons.js` 仍在被引用
- 测试：27 个 `*.test.mjs`（含 `meetingRoomProductization.test.mjs`、`knowledgeLibraryProductization.test.mjs`、`organizationCenter.test.mjs`、`operatingIntelligence.test.mjs` 等）

### backend
- FastAPI 单体，`backend/app/main.py` **5899 行**，`create_app()` 在 `main.py:1005`；`backend/app/*.py` 共 101 个模块
- 路由挂载点：`main.py:2195`（task job）、`2201`（memory）、`2203`（capability registry）、`2205`（ai capability）、`2206`（ai usage）、`2222`（ceo day）、`2410`、`4921`（quickstart）、`4927`（home）、`5557`（runtime foundation）、**`5559`（meeting）**、`5579`（frontend v1）、`5582`（workspace package）、`5588`（ceo evidence）、`5592`（pipeline）
- 实测运行路由 **319 条**（:8002 `/openapi.json`）：`/api/workspace` 194、`/api/platform` 43、`/api/ceo-day` 20、`/api/pipeline` 12、`/api/catalog` 9、`/api/auth` 8、`/api/task` 7、`/api/ceo` 7、`/api/credential` 3、`/api/results` 3 等
- 启动前由 `_load_local_dotenv()`（`main.py:17-43`）读入 gitignored 的 `deploy/new-api/.env` 注入进程环境

### desktop
- Tauri 2（`tauri.conf.json` schema v2），`productName: Curis`，`version: 0.1.0`，`identifier: com.curis.desktop`
- 窗口 1440×900，最小 1024×700；`bundle.targets: ["app","dmg"]`；`frontendDist: ../desktop/static`（占位，真实前端由 sidecar 提供）
- sidecar（`desktop/src/lib.rs`）：
  - **guardian**（`lib.rs:85`）
  - **workspace** backend `:8002`（`lib.rs:120-130`，`CURIS_CREDENTIAL_BACKEND=macos-keychain`、`CURIS_IDENTITY_MODE=selfuse`、`CURIS_TENANT_ID=selfuse`）
  - **gateway** `:8080`（`lib.rs:133-143`）
  - **frontend** `:3010`（`lib.rs:145-161`，`node frontend/server.js`）
  - 退出统一 `kill_sidecars()`（`lib.rs:182`，SIGTERM → 3s → SIGKILL）
- 构建产物：`desktop/target/release/bundle/macos/Curis.app`（2026-09-02 02:52，二进制 sha256 `cabc9d9be89ec65af2511c3670ace505a6668979d542ca7c062d0b2c943c5f5a`）
- **未安装**于 `/Applications`；bundle 目录另存 `CurisCopy.app`（2026-08-09，陈旧副本）

### database
SQLite，当前 **4 类库 + 垃圾文件**：

| 路径 | 大小 | mtime | SHA-256 | integrity | 说明 |
|---|---:|---|---|---|---|
| `backend/data/curis.sqlite` | 1,277,952 | 2026-08-15 16:47:39 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | ok | 仓库活跃库 A，96 表 |
| `data/curis.sqlite` | 1,232,896 | 2026-08-16 17:42 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | ok | 仓库活跃库 B |
| `~/Library/Application Support/com.curis.desktop/data/curis.sqlite` | 1,507,328 | 2026-09-02 18:55:30 | `80c8ff225cdd5fc90cc55516daf541f0d356d4edee6f77f987873ac3f5909c70` | ok | **已安装 App 真实运行时库**，109 表 |
| `desktop/target/release/runtime/workspace/_internal/backend/data/curis.sqlite` | 1,277,952 | 2026-08-31 00:46:22 | `a9d96a95…` | ok | 打包运行时副本，与 `backend/data/curis.sqlite` **字节完全一致** |
| `backend/tests/data/curis.sqlite` | 192,512 | 2026-07-08 04:48 | `1ee37420…` | — | 测试库 |
| `backend/curis.sqlite` / `backend/curis_dev.db` | 0 | 2026-08-08 | `e3b0c442…` | — | 空文件残留 |

已在 09-02 评审 §21 中登记的两个活跃库 SHA-256 与本次实测**逐字节一致** → 基线未被改动。

**已安装 App 运行时库实际业务数据（只读查询）**：
- `companies` = 1（`Curis AI Company`，tenant `selfuse`）
- `employee_instances` = **0**、`knowledge_entries` = **0**、`workspaces` = **0**、`departments` = **0**、`strategy_meetings` = **0**
- 仅目录/模板数据：`tool_templates` 115、`default_capability_definitions` 106、`skill_templates` 55、`workflow_contents` 36、`workflow_templates` 18、`employee_templates` 13、`business_metrics` 9、`department_types` 7、`persona_templates` 6

### provider / model / connector
- 统一入口 `ModelGatewayAdapter` + 单一 `ai_usage_records` 账本（会议每个 Employee/Leader 调用都过账）
- 打包 App 凭证后端 = **macOS Keychain**（`CURIS_CREDENTIAL_BACKEND=macos-keychain`）；开发态走 `deploy/new-api/.env`（权限 0600，525 B）
- `.env` 变量名：`DEEPSEEK_API_KEY`、`CURIS_MODEL_GATEWAY_BASE_URL` / `_ID` / `_MODEL` / `_API_KEY` / `_ESTIMATED_COST_PER_1K_TOKENS`、`NEW_API_*`
- **值是否存在未由我验证**（沙箱策略禁止读取 `.env` 内容）。确认方式只能是 App 内 Model Management 的真实 Health / discovery 结果，不得以文件读取替代

### test stack
- 后端：pytest，`backend/tests/*.py` **203 个**测试文件
- 前端：27 个 `*.test.mjs`（Node 原生 runner）
- 会议相关：`backend/tests/test_v1_meeting_autonomous_discussion.py`、`backend/tests/test_v1_meeting_room_productization.py`、`frontend/tests/meetingRoomProductization.test.mjs`
- 测试隔离约定（Backlog Rules）：测试使用**仓库外部** SQLite，通过 `CURIS_DB` / `CURIS_DB_PATH` / `CURIS_WORKSPACE_DB` 指定

---

## Product State

真源：`docs/00_Context/CURRENT_STATE.md`（Status: Frozen，Updated 2026-09-02，Baseline `main @ c0e1855f`）+ `docs/reviews/CURIS_V1_EXECUTION_BACKLOG.md`（2026-09-02）

| 模块 | 状态 | Figma 基线 | 备注 |
|---|---|---|---|
| CEO 工作台 | IMPLEMENTED / ACCEPTED（Batch 1，带 P1 边界） | `69:3` | 全 App Live AI 已 08-30 接受；Conversation/Composer/Model Selector 仍 Partial |
| 业务空间 | **未确认**（导航项存在，无独立验收记录） | — | 入口 `/ceo-office/business` |
| 组织中心 | IMPLEMENTED / ACCEPTED（2026-08-31） | `106:3 / 106:230 / 106:457` | Dark / 1024 / 无障碍 / Search-Filter 接线 / 旧结构清理为 P2 |
| 人才与能力 | IMPLEMENTED / ACCEPTED（2026-09-01） | — | Avatar 走共享 `employee_instances.avatar_ref`，不存二进制；Connector 真实状态 `未连接 / 需要授权` |
| 经营洞察 | IMPLEMENTED / ACCEPTED（2026-08-31） | `172:3 / 172:277 / 172:551 / 172:825` | 外部 Outcome/Feedback connector、自动分析师为界外缺口 |
| 资料库 | IMPLEMENTED / ACCEPTED（2026-09-01） | `187:2 / 187:276 / 187:550 / 187:824` | 105 条规模已验证；仅手工/.md/.txt，PDF/DOCX/Web/Connector/向量检索未实现 |
| 会议 | **Product/UX/UI ACCEPTED（2026-09-02）· 实现待产品化收口** | `214:3 / 247:2 / 214:279 / 214:555 / 214:831` | Backlog `V1-P1-015 = UI ACCEPTED / IMPLEMENTATION PENDING` |

---

## Meeting Autonomous Discussion

**代码位置**：`backend/app/meeting_service.py`（1302 行，`MeetingService`）+ `backend/app/api/meeting_router.py`（166 行），挂载前缀 `/api/workspace/runtime/foundation`

**机制（实测代码，非文档推断）**：

```
EVENT → TURN EVALUATION → SPEAKER CANDIDATES → SPEAKER SELECTION
      → RESPONSE → LEADER EVALUATION
      → CONTINUE / PROPOSAL / EVIDENCE / CEO DECISION / STOP
```

- **候选人打分是确定性规则，不是模型自选发言人**（`_candidate_evaluation`，`meeting_service.py:626-678`）：
  - CEO/推进负责人点名 **+100**
  - 持有本轮新增事实/结果所有权 **+40**
  - 岗位/责任与议题相关性 **+min(30, 8 + 3n)**
  - 会议 leader **+5**
  - 上一轮已发言 **−20**
  - 无相关性时标注「当前没有可证明的新增相关性」；最高分 ≤ 0 → `noProgressCount++`
- **Employee 发言是真实 LLM 调用**（`_speaker_prompt`，`meeting_service.py:924-936`），要求「必须带来新事实/专业判断/风险/反对意见/Evidence 请求」，禁止总结前文或只说同意
- **Leader 评估是第二次 LLM 调用**（`_leader_prompt`，`meeting_service.py:938-951`），只允许 9 种结果：`CONTINUE_DISCUSSION / REQUEST_SPECIFIC_EMPLOYEE / REQUEST_EVIDENCE / UPDATE_PROPOSAL / WAIT_FOR_WORK / NEEDS_CEO_DECISION / DISCUSSION_SUFFICIENT / BLOCKED / UNKNOWN`
- **无轮询**：评审 §4 记录三员工验证中 Research 先发言、无关 Finance 全程静默、`@林舟` 可强制覆盖
- **边界**（`LIMITS`，`meeting_service.py:37-45`）：单次推进 6 轮、每人连续 1 轮、无进展上限 2 次、12 次模型调用、8000 confirmed tokens、USD 1 成本、300 秒
- **并发/幂等**：`_claim_advance`（`:893`）单事务活跃 claim，并发争抢只有 1 个赢家；已完成事件保留 processed-event identity；子工作 `release_key = meeting:{id}:{event}:{purpose}:{employeeRef}`
- **CEO 离开继续**：FastAPI `BackgroundTasks` 在 HTTP 响应后拥有进程内继续权，React 轮询只观察持久化状态（`meeting_router.py:49-64`）
- **重启**：Browser 与 fresh packaged 均已验证不重放（评审 §16）
- **上下文隔离**：最近 10 条消息、最多 3 条 Knowledge 摘录、最多 12 个合法引用，全公司/全历史/跨公司 hydration 被拒（`_bounded_context`，`:680-727`）

**各方验证结论**（`docs/reviews/CURIS_V1_MEETING_AUTONOMOUS_DISCUSSION_REVIEW.md`，2026-09-02 18:37，Disposition: IMPLEMENTED / PARTIAL）：

| 项 | 结论 |
|---|---|
| MEETING TURN ORCHESTRATION | **VERIFIED** |
| CEO LEAVE → TEAM CONTINUE | **VERIFIED**（限当前单进程 Runtime） |
| CEO DECISION GATE | **VERIFIED** |
| PACKAGED FAILURE / RESTART TRUTH | **VERIFIED** |
| LIVE EXTERNAL MODEL PACKAGED E2E | **NOT VERIFIED** |
| MEETING AUTONOMOUS DISCUSSION | **IMPLEMENTED / PARTIAL** |
| MEETING ROOM BASE PRODUCTIZATION | **IMPLEMENTED / ACCEPTED CANDIDATE** |

- **real model — BLOCKED**：评审 §23 原文 `REAL CLOUD MODEL E2E BLOCKED — VALID EXTERNAL MODEL CREDENTIAL REQUIRED.` 打包 App 内 DeepSeek 显示 `未连接`，唯一可用动作是已存在的原生 Keychain API-Key 输入框；因无合法外部凭证，本次 gate **未创建任何 Meeting / Employee turn / Proposal / Decision / Work / Result**
- **packaged desktop**：新构建 PASS（sha256 `cabc9d9b…5f5a`），隔离 app data `/tmp/curis-meeting-cloud-e2e.XbOY79`；此前隔离包内首次 Employee 响应未通过 Meeting Result contract，UI 诚实显示讨论停止 → 属**有效失败真值**，不是成功证据
- **current blocker**：fresh packaged 隔离运行时内没有合法可用的外部模型凭证（Keychain 未录入）

### ⚠ 阻塞状态更正（本次实测，晚于评审文档）

评审 §23 写于 2026-09-02 18:37。**18:56（评审落盘 19 分钟后）该隔离实例已录入凭证并完成发现**：

| 检查项 | 实测结果 |
|---|---|
| `GET /api/workspace/credentials` | 1 条 active：`cred-040a0430…`，name `deepseek 当前会话凭证`，provider `deepseek`，`storage: macos_keychain`，`status: active` |
| `GET /api/workspace/ai-capabilities/providers` | **`deepseek: configured = True`**（其余 17 个 provider 全为 `False`） |
| `GET /api/workspace/model-gateway` | 发现租户私有模型 `user.deepseek.052e4fc0bc88e2a5` = `deepseek-v4-pro`，`status: active` |
| `GET /api/workspace/model-preference` | 默认模型**已设为** `user.deepseek.052e4fc0bc88e2a5`（deepseek-v4-pro） |

→ **「缺合法外部凭证」这一阻塞项在该实例中已解除**。但：

1. `configured: True` 只证明凭证存在且发现成功，**不证明真实 completion 调用可用**（本次 bootstrap 未执行 `credentials/{id}/test`，那是真实外部调用，属开发动作）。
2. 该隔离库 **`companies = 0`**（连公司都没建）、`employee_instances = 0`、`workspaces = 0`、`strategy_meetings = 0` → 要跑会议链必须**从零搭**：建公司 → 招 3 名员工 → 建 Workspace → Start Meeting。
3. 该实例在 `/tmp` 下且已运行 27 小时，**占用 :8080 / :8002 / :3010**，会阻塞任何新的打包启动或 dev run。
- **final gate**：`fresh packaged Curis.app → Start Meeting → 3+ AI Employees → 真实云模型 → 自主判断发言 → Evidence → Proposal → CEO Decision Gate → Work → Result → 会议继续 → CEO 离开后台继续 → Restart 无重复执行`

---

## Database Safety State

本次 bootstrap 全程**只读**，未执行任何 reset / delete / truncate / vacuum / migration。

- 两个仓库活跃库 SHA-256 与 09-02 评审登记的 preflight 基线**逐字节一致**（`a9d96a95…`、`2ea2506f…`），`integrity_check = ok`
- 打包运行时副本与 `backend/data/curis.sqlite` 字节一致
- 已安装 App 运行时库 `80c8ff22…` integrity ok，但**不含任何业务数据**（0 员工 / 0 知识 / 0 workspace / 0 会议）

---

## Verification

- backend 测试文件：203（pytest）
- frontend 测试文件：27（`*.test.mjs`）
- 最近一次 Next 生产构建：2026-09-02 02:51（BUILD_ID `KCdDhovvCgSzdnX0d9db9`）
- 最近一次 Tauri 打包：`desktop/target/release/bundle/macos/Curis.app`，2026-09-02 02:52
- 09-02 评审登记的会议专项：`4 passed` 聚焦 + `43 passed` 回归 + 前端 `2 passed` + Python compile PASS + ESLint PASS + Next build PASS + Tauri PASS + `git diff --check` PASS
- **运行时当前在跑**：gateway `:8080` /health `{"status":"ok"}`，workspace `:8002` /health `{"status":"ok"}`，frontend `:3010` `/ceo-office` HTTP **200**
- **运行实例身份已查实**（`lsof -p 31888/31895` 的 `cwd`）：

  | 项 | 值 |
  |---|---|
  | 进程 | `curis-gateway`(31888) / `curis-workspace`(31895) / `node`(31889) |
  | 数据根 | **`/private/tmp/curis-meeting-cloud-e2e.XbOY79`**（隔离，非默认 App 数据区） |
  | 二进制 | `desktop/target/release/bundle/macos/Curis.app/Contents/Resources/runtime/{gateway,workspace}/…` |
  | 已运行 | 自 2026-09-02 18:56 起，约 **27 小时**未关闭 |

  → 这是 **09-02 cloud E2E gate 的遗留实例**，不是日常用户实例。默认 App 数据区（`~/Library/.../data/curis.sqlite`）自 2026-09-02 18:55 起未被写入。

---

## Current Risks（只列已实证的问题）

1. **工作区是唯一记录**：最后提交 2026-08-22，此后 12 天的已接受工作全部只存在于 686 个未提交变更中（566 个未跟踪）。一旦误 reset/clean 即不可逆。
2. **App 运行时库无业务数据**：0 员工 / 0 知识 / 0 workspace / 0 会议，而文档记录的 105 条知识验证发生在**隔离库**。这不是回归，但极易被误判为回归。
3. **两个仓库活跃库内容不同**（`backend/data` 96 表 vs `data/` 另一套），mtime 相差一天，「哪个是权威」未登记。
4. **Database 对象被当路径写入**：根目录 16 个 + `backend/` 约 20 个名为 `<app.database.Database object at 0x...>` 的文件，每个 1,159,168 B（合计约 40 MB）。这是真实 bug，不是缓存。bootstrap 阶段**未删除**。
5. **22 个 worktree（17 个 prunable）+ 1 个 stash**（`feat/093` 的共享后端 WIP），分支/工作区切换有踩踏风险。
6. **`CurisCopy.app` 陈旧副本**（2026-08-09）与真产物同目录，存在验证/分发错包风险。
7. ~~会议 Gate 卡在外部凭证~~ **已更正**：该隔离实例的 DeepSeek 凭证已 active 且 `configured=True`，默认模型已设为 `deepseek-v4-pro`。**新阻塞**变为：隔离库零业务数据（0 公司 / 0 员工 / 0 workspace），需从零搭建才能跑会议链。恢复路径仍受评审限定：不得用环境变量 / 文件 / mock provider / 改源码绕过。
7b. **遗留隔离实例占用端口**：`/tmp/curis-meeting-cloud-e2e.XbOY79` 已运行约 27 小时，占用 `:8080 / :8002 / :3010`。在做任何新的打包启动 / `tauri build` / dev run 之前必须先关闭它，否则端口冲突；且 `/tmp` 会被系统清理，不能当长期环境。
8. **导航外孤岛路由**：`frontend/app/ceo-office/` 下有 20 个子路由，仅 7 个在一级导航内。`reports` / `brainstorm` / `runtime-trace` / `strategy-room` / `company-runtime` / `execution` / `decisions` / `calendar` / `finance` / `capabilities` / `help` / `settings` / `projects` 均不在 `V1Sidebar.NAV` 中；`frontend/app/org-center/`、`platform/`、`employees/`、`projects/`、`control/`、`dev-console/` 为根级残留。
9. **分发未完成**：目标 GitHub Beta；Developer ID / 公证为 Stage B 推迟项；App 未安装进 `/Applications`。

---

## Recommended Next Step（唯一）

**收口 `MEETING ROOM PRODUCTIZATION CLOSURE`（Backlog `V1-P1-015`）剩下的唯一一项。**

由于阻塞项已从「缺凭证」变为「隔离实例零业务数据」，实际动作序列调整为：

1. **确认凭证可用**（唯一未验证项）：对运行中的隔离实例调用一次 `POST /api/workspace/credentials/cred-040a0430…/test`，确认 DeepSeek 真实 completion 可用。这是**真实外部调用**，bootstrap 阶段未执行，需你授权。
2. **在同一隔离实例内从零搭建**：建公司 → 招 3 名不同岗位员工 → 建 Workspace → Start Meeting。
3. **重跑那条 E2E 链**：3+ 员工自主发言 → Evidence → Proposal → P7 Decision → Work/Result → CEO 离开后台继续 → Restart 无重放。
4. 收尾前关闭该遗留实例，释放 `:8080 / :8002 / :3010`。

评审确认当前证据**不指向任何 Runtime 重新设计**。

**需你决策的一项**：是复用这个已配好 DeepSeek 的 `/tmp` 隔离实例（快，但环境易失、已跑 27 小时），还是关闭它、用默认 App 数据区重开一个 fresh packaged 实例并在 Keychain 重新录一次凭证（慢，但干净且符合评审「fresh packaged」措辞）。我倾向后者——评审的 gate 措辞是 **fresh packaged**，复用 27 小时旧实例在验收上不严谨。
