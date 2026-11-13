# CURIS V1 APP READINESS AUDIT

Status: Review  
Authority Class: REVIEW  
Date: 2026-08-26  
Scope: Current repository truth only; read-only audit  
Disposition: V1 NOT READY

## 1. Executive Summary

Curis 已经拥有相当扎实的 Company OS / Runtime 底座，但还没有装配成普通用户可以从首次打开一直使用到结果复盘的完整 V1。当前最强的是 canonical Business、Workspace、Employee/Responsibility、真实 Codex 执行、Artifact/Evidence、Team Operating、有限 Autonomous Operating 和动态 Workspace Package；最弱的是首次进入后的自然业务创建、通用业务 Workspace、凭证重启连续性、外部 Channel 能力，以及一条基于 fresh packaged Desktop 的全产品纵向验收。

**结论：工程功能完成度约 67%，但产品可交付状态为 `V1 NOT READY`。** 67% 不等于可日用；当前关键路径存在 P0 断点，普通用户仍无法稳定完成：首次打开 → 创建业务 → 进入通用 Workspace → 员工真实执行 → 查看结果 → 重启后继续。

### 1.1 Scoring Method

- `DONE = 1`
- `PARTIAL = 0.5`
- `MISSING / BROKEN / NOT PROVEN = 0`
- `TARGET NOT V1` 不进入分母
- 每个功能项等权；百分比来自下文逐项 ledger，不以代码量、路由数或文档数量代替产品完成度。

| Area | Scored Items | Points | Readiness |
|---|---:|---:|---:|
| Frontend product assembly | 25 | 15.5 | 62% |
| Backend / Runtime | 25 | 22.0 | 88% |
| Company OS | 16 | 13.5 | 84% |
| General Business Workspace | 15 | 9.0 | 60% |
| Content Growth | 15 | 7.0 | 47% |
| RD Professional Workspace | 15 | 12.5 | 83% |
| Capability / Connector | 20 | 6.5 | 33% |
| App infrastructure | 19 | 10.5 | 55% |
| Testing / reliability | 15 | 10.5 | 70% |
| **Total** | **160** | **106.5** | **67%** |

### 1.2 Five P0 Product Blockers

1. **First Run 未闭环到业务**：当前 onboarding 真实持久化 Company 与 CEO Assistant，但没有把用户意图自然转成 canonical Business、First Workspace 和可进入的工作现场。
2. **General Business Workspace 未形成普通用户闭环**：动态 Package substrate 已证明，但“任意业务目标 → 团队/责任 → Work → Result/Evidence → Decision/Next Cycle”尚未作为通用产品入口装配。
3. **模型凭证重启连续性不足**：当前 `LocalDevCredentialBackend` 是进程内存实现；目录、Health 与执行底座存在，但安装包重启后的安全 Secret 连续性没有成为 V1 已证明能力。
4. **Shared 工作体验未组装成一条主线**：Employee、Responsibility、Conversation、Current Work、Result Reference、Decision、History 分别存在，尚未在 CEO Desk + General Workspace 中形成同一日常经营路径。
5. **缺少 fresh packaged whole-app E2E**：已有 Business Spine、XHS、RD、Package 等纵向证据，但没有同一 fresh 用户数据完成首次进入到重启恢复的全链验收。

## 2. Evidence Boundary

### 2.0 Repository Snapshot

- Audited HEAD: `c797db840bad285d7e9f1962d06eac61aa28508b`
- Frontend page routes: 57
- Backend API route decorators: 327
- Backend Python modules: 150
- Backend test files / test functions: 180 / 387
- Frontend `.test.mjs` files / test declarations: 19 / 108
- These are inventory measurements, not completion evidence. A route, module, or test count does not prove an ordinary-user journey.
- `CURRENT_STATE.md` contains an older baseline reference than audited HEAD; this audit therefore uses current code plus accepted evidence for Implementation Truth and does not silently rewrite Current Authority.

### 2.1 Counted as Current Implementation Evidence

- 当前源码与 tracked commits。
- Accepted / Implemented Review 中可定位的 Browser、Packaged Desktop、isolated SQLite、restart、failure/recovery 证据。
- 当前可定位的 API、Runtime model、frontend route、tests。

### 2.2 Not Counted as Done

- Product Blueprint、Research、Candidate、Prototype、Visual Reference 单独存在。
- 有 class / schema / method，但没有被当前用户路径调用。
- mock/fixture 测试代替真实 Provider、Connector 或外部平台结果。
- Browser 通过代替 Packaged Desktop。
- 已安装 Curis 中必须修改 Core 源码和重新 build 才能获得的新 Workspace。

## 3. Current Implementation Inventory

### 3.1 Real Foundations

| Foundation | Status | Evidence / Truth |
|---|---|---|
| Company → Department → Business → Workspace | DONE | canonical persistence、外键/原子创建、Parent Resolver、Business Read Model；Business Spine accepted review。 |
| Dynamic Workspace Package substrate | DONE | Package discover/validate/install/register/render/persist/update/rollback 基础及 sample work surface 已有 accepted evidence。 |
| Workspace-scoped Employee / Responsibility | DONE | canonical Employee、assignment provenance、holder/executor 分离、callback trust。 |
| Team Operating | DONE | Work → employee → provider session → result/evidence → router wake-up / next employee；本地 deterministic provider 已验收。 |
| Real Codex execution | DONE | RD 已证明真实 session、文件变化、diff、test evidence、result reference、restart/failure truth。 |
| Computer Access truth | DONE | requested/configured/effective 分离；resume UNKNOWN/UNVERIFIED；Full unsupported fail-closed。 |
| Autonomous Operating bounded core | DONE | cycle、work、evidence、evaluation、leader decision、successor control、两周期与 evidence-bound learning 的 bounded proof。 |
| XHS instance v1 internal loop | DONE | Calendar/Note/version/handoff/P7/schedule/capability truth；不含真实发布和 analytics。 |

### 3.2 Important Partial Assemblies

| Assembly | Status | Current Truth |
|---|---|---|
| First Run | PARTIAL | FoundingRun、Company、Assistant 可持久化；仍暴露内部术语，未创建 Business/Workspace/Team。 |
| CEO Desk | PARTIAL | 有运行、人员、供给、异常等聚合入口；不是完整普通用户 Operating Day。 |
| Workspace Studio | PARTIAL | RD/XHS/TTK 模板草拟存在；仍使用 legacy/free-form `business_ref`，无 General/no-template canonical flow。 |
| General Workspace | PARTIAL | generic package renderer 和 shared shell 存在；缺少用户可创建、可经营、可回访的通用业务闭环。 |
| Content Growth | PARTIAL | legacy XHS 实例真实；当前 Content Growth Professional Workspace 仍是 Candidate/IA 阶段。 |
| Capability Center | PARTIAL | 目录、连接/Health/Binding truth 存在；用户化、持久 Secret、真实外部 Connector 证据不足。 |

## 4. Full V1 Journey Audit

### 4.1 First Run

| Functional Item | Status | Evidence / Gap |
|---|---|---|
| Local owner / CEO identity | DONE | onboarding 与 Company context 有真实持久化。 |
| Resume same FoundingRun | DONE | 同一 run 可读取；刷新路径存在。 |
| Natural-language intent capture | PARTIAL | 有输入与提案状态，但仍偏 Runtime form，不是完成的 Assistant guided experience。 |
| Company + CEO Assistant atomic materialization | DONE | 当前 FoundingRun 可创建 Company 和首位 Assistant。 |
| Choose verified default model | PARTIAL | Provider/Health 路径存在；普通用户动线和 Secret restart truth 未闭合。 |
| Recommend business / template | MISSING | 当前 First Run 不做基于意图的推荐。 |
| No-template General fallback | MISSING | 没有 canonical General Business 创建路径。 |
| Canonical Business + First Workspace | MISSING | onboarding 不调用 Business Spine 原子创建。 |
| First employee/team readiness | PARTIAL | Assistant 存在；专业员工与责任不在 First Run 中建立。 |
| Safe landing after founding | PARTIAL | 可进入 CEO Office，但没有首项业务时仍偏空/基础层。 |

### 4.2 General Business Operating Journey

| Functional Item | Status | Evidence / Gap |
|---|---|---|
| Browse canonical Businesses | DONE | `/ceo-office/business` 消费 canonical read model。 |
| Browse Workspace Directory | DONE | Business detail 返回 canonical workspace directory。 |
| Create arbitrary Business from UI | MISSING | backend API 有，current frontend API/flow 未接。 |
| Atomic first DRAFT Workspace | DONE | backend Business Spine 已证明。 |
| Open generic installed Workspace | DONE | `InstalledWorkspaceRuntime` 可打开 declarative package work surface。 |
| Describe goal in ordinary language | PARTIAL | package/work object substrate 有；产品入口未装配。 |
| Materialize team / responsibilities | PARTIAL | Team Operating 可用；General flow 未自动绑定。 |
| Shared conversation | PARTIAL | projection/summary 存在；缺完整 durable General conversation product。 |
| Current Work | PARTIAL | Work/Task/Execution truth 存在；通用 UI 仍技术化。 |
| Result / Evidence references | DONE | ResultStore、Artifact/Evidence 与 shared projections 已真实存在。 |
| Decision / wait / failure | PARTIAL | Shared/P7/bounded runtime 可用；General product flow 未完整接线。 |
| Handoff | PARTIAL | Runtime 真实；General UI/flow 未证明。 |
| Next cycle / improvement | PARTIAL | autonomous bounded core 真实；未成为普通用户可控 General journey。 |
| Restart continuity | PARTIAL | foundations 分别证明；whole General journey 未证明。 |
| Daily revisit / history | MISSING | 没有完整普通用户经营历史入口的 packaged proof。 |

### 4.3 Content Growth

| Functional Item | Status | Evidence / Gap |
|---|---|---|
| Professional Workspace authority / IA direction | PARTIAL | Product Candidate 与 IA review 存在，不是 current implemented product。 |
| XHS Calendar / Note / version | DONE | accepted v1 implementation。 |
| XHS employee responsibility | DONE | real employee references、handoff、decision 已证明。 |
| Content review / Needs CEO | DONE | same Decision Packet / P7 已证明。 |
| Internal scheduling | DONE | reaches SCHEDULED truthfully。 |
| Real XHS publish | MISSING | no verified Connector / receipt E2E。 |
| Real XHS analytics | MISSING | unavailable/no data truth。 |
| Douyin/TikTok execution | NOT PROVEN | catalog/contracts do not prove external E2E。 |
| YouTube/Bilibili execution | NOT PROVEN | no accepted real-world evidence。 |
| Multi-account isolation | MISSING | no accepted per-account auth/publication/receipt proof。 |
| Cross-channel research | PARTIAL | research/tool substrate exists, not verified channel operating chain。 |
| Content Growth multi-surface product | PARTIAL | package/authority research exists; frontend implementation not accepted。 |
| Growth feedback loop | PARTIAL | internal result/evaluation substrate exists; external metrics absent。 |
| Manual result input | PARTIAL | some manual/unverified receipt semantics exist; not a complete channel product. |
| Channel capability truth UI | PARTIAL | waiting/unavailable can be expressed; current integrated product not closed。 |

### 4.4 RD Professional Workspace

| Functional Item | Status | Evidence / Gap |
|---|---|---|
| Four-pane professional shell | DONE | accepted RD Phase 2A design fidelity。 |
| Project / Cycle / Task | DONE | real persisted RD objects。 |
| Employee workstation | DONE | holder/executor/progress/result first。 |
| Real Codex binding/session | DONE | real adapter/session evidence。 |
| Real file/code change | DONE | isolated project diff evidence。 |
| Artifact / Evidence / Result Reference | DONE | separate persisted truth。 |
| Failure truth | DONE | failure does not become completed。 |
| Long-running async reliability | DONE | submit/observe/final state closure accepted。 |
| Artifact review | DONE | persisted reviewer request/task/result path accepted。 |
| Handoff | DONE | provider-native ACK / responsibility transfer evidence accepted。 |
| P7 CEO Decision | PARTIAL | runtime proof exists; full current packaged product flow needs final assembly. |
| Multi-employee product UX | PARTIAL | runtime accepted; ordinary-user end-to-end productization incomplete。 |
| Computer Access truth | DONE | P0 truth semantics retained。 |
| Canonical Business creation entry | PARTIAL | Business Spine exists; First Run/Studio integration incomplete。 |
| Current package/multi-surface migration | MISSING | approved product package is not fully assembled as V1 entry. |

## 5. Layer Readiness Ledgers

### 5.1 Frontend Product Assembly — 15.5/25 = 62%

| # | Item | Status |
|---:|---|---|
| 1 | Desktop shell/navigation | DONE |
| 2 | Shared four-pane shell | DONE |
| 3 | Resizable panes | DONE |
| 4 | Search | DONE |
| 5 | Utility maximize | DONE |
| 6 | Canonical Business directory | DONE |
| 7 | Canonical Workspace directory | DONE |
| 8 | Parent path / deep route | DONE |
| 9 | XHS accepted instance | DONE |
| 10 | RD accepted professional view | DONE |
| 11 | Generic package renderer | DONE |
| 12 | First Run product language | PARTIAL |
| 13 | Model setup | PARTIAL |
| 14 | CEO Desk assembly | PARTIAL |
| 15 | Assistant continuous partner | PARTIAL |
| 16 | Business creation UI | MISSING |
| 17 | General Workspace creation | MISSING |
| 18 | General Workspace conversation | PARTIAL |
| 19 | General current-work/result UI | PARTIAL |
| 20 | General decision/recovery UI | PARTIAL |
| 21 | Team materialization UI | PARTIAL |
| 22 | Content Growth current IA implementation | MISSING |
| 23 | Durable notification center | PARTIAL |
| 24 | Backup/update/release UI | MISSING |
| 25 | Whole-app ordinary-user flow | MISSING |

### 5.2 Backend / Runtime — 22/25 = 88%

| # | Item | Status |
|---:|---|---|
| 1 | Canonical Company | DONE |
| 2 | Department | DONE |
| 3 | Canonical Business | DONE |
| 4 | Workspace relation | DONE |
| 5 | Atomic Business + first Workspace | DONE |
| 6 | Parent Resolver | DONE |
| 7 | Legacy quarantine | DONE |
| 8 | Canonical Employee identity | DONE |
| 9 | Responsibility holder/executor | DONE |
| 10 | Assignment provenance | DONE |
| 11 | Real provider callback verification | DONE |
| 12 | Work / Task / Execution | DONE |
| 13 | Child/multi-work sequential | DONE |
| 14 | Artifact / Evidence / Result | DONE |
| 15 | Handoff | DONE |
| 16 | Decision P7 | DONE |
| 17 | Acceptance / evaluation | DONE |
| 18 | Bounded autonomous successor control | DONE |
| 19 | Dynamic Workspace Package lifecycle | DONE |
| 20 | Long-running async execution | DONE |
| 21 | General first-run orchestration | MISSING |
| 22 | Durable conversation/history | PARTIAL |
| 23 | Cost/token observation and enforcement | PARTIAL |
| 24 | Global autonomous depth/calibration | PARTIAL |
| 25 | External connector execution substrate | PARTIAL |

### 5.3 Company OS — 13.5/16 = 84%

| Item | Status |
|---|---|
| Company identity | DONE |
| Department identity | DONE |
| Business identity | DONE |
| Workspace identity | DONE |
| Employee identity | DONE |
| Responsibility | DONE |
| Decision | DONE |
| Result/Evidence | DONE |
| Capability truth | DONE |
| Parent context | DONE |
| Tenant/company isolation | DONE |
| Legacy quarantine | DONE |
| CEO Desk operating projection | PARTIAL |
| Assistant continuity | PARTIAL |
| Cross-workspace history/attention | PARTIAL |
| Ordinary-user first company assembly | MISSING |

### 5.4 Capability / Connector — 6.5/20 = 33%

| Item | Status |
|---|---|
| Provider catalog visibility | DONE |
| Connection/Health state separation | DONE |
| Ollama local discovery/call | DONE |
| Codex real execution | DONE |
| Cloud BYOK connection UX | PARTIAL |
| Durable secure credential | MISSING |
| MCP stdio manifests | PARTIAL |
| MCP real external E2E | NOT PROVEN |
| Browser automation | PARTIAL |
| Generic social uploader bridge | PARTIAL |
| XHS real auth | NOT PROVEN |
| XHS real publish/receipt | MISSING |
| Douyin real publish/receipt | NOT PROVEN |
| TikTok real publish/receipt | NOT PROVEN |
| YouTube real publish/receipt | NOT PROVEN |
| Bilibili real publish/receipt | NOT PROVEN |
| Real analytics | MISSING |
| Real comments/feedback | MISSING |
| Multi-account isolation | MISSING |
| Capability gap / unavailable truth | PARTIAL |

### 5.5 App Infrastructure — 10.5/19 = 55%

| Item | Status |
|---|---|
| Tauri Desktop shell | DONE |
| Workspace backend sidecar | DONE |
| Gateway sidecar | DONE |
| Frontend standalone sidecar | DONE |
| Guardian/readiness | DONE |
| Instance lock | DONE |
| Local logs | DONE |
| Fresh local packaged build | PARTIAL |
| macOS signing/notarization | MISSING |
| Auto update | MISSING |
| Backup | MISSING |
| Restore | MISSING |
| Secret persistence | MISSING |
| Crash/restart recovery | PARTIAL |
| DB integrity/fail-fast test safety | DONE |
| Local profile/auth | PARTIAL |
| OS notification | NOT PROVEN |
| Diagnostics/support export | PARTIAL |
| Release installation acceptance | PARTIAL |
| Cross-platform distribution | TARGET NOT V1 |

### 5.6 Testing / Reliability — 10.5/15 = 70%

| Item | Status |
|---|---|
| Backend focused tests | DONE |
| Frontend focused tests | DONE |
| Python compile | DONE |
| Frontend production build | DONE |
| Active DB fail-fast | DONE |
| Isolated SQLite patterns | DONE |
| Restart evidence for core runtime | DONE |
| Failure truth evidence | DONE |
| Duplicate/idempotency evidence | DONE |
| Business Spine packaged E2E | PARTIAL |
| XHS packaged E2E | PARTIAL |
| RD packaged E2E | PARTIAL |
| Fresh whole-app V1 E2E | MISSING |
| Real cloud provider E2E | NOT PROVEN |
| Real channel connector E2E | NOT PROVEN |

## 6. Real V1 Definition

Curis V1 不是“所有 Runtime 都完成”，也不是“所有 Channel 都接通”。V1 应当是一个普通用户可以在单机 Desktop 中稳定完成的最小 Company OS：

1. 首次打开，确认本地 CEO 身份。
2. 可浏览模型目录，并安全连接至少一个可用模型；重启后凭证仍安全可用。
3. 用自然语言描述第一项业务；系统生成可修改 Proposal。
4. 原子创建 Company、CEO Assistant、canonical Business、First Workspace。
5. 没有专业模板时进入 General Business Workspace，而不是空白或失败。
6. 建立最小 Team / Responsibility，员工可以接手一个真实 Work。
7. 执行产生可追溯 Result / Evidence；失败、等待、UNKNOWN 都诚实可见。
8. 需要 CEO 时使用同一 Decision；选择后自动继续。
9. 重启 Desktop 后可回到同一 Business、Workspace、Work、Result 与历史。
10. 至少一个专业 Workspace（建议 RD）从创建入口到真实结果完成 packaged E2E。

## 7. What Not to Rebuild

以下已证明，V1 只应集成，不应重新研究或重造：

- Canonical Business Spine。
- Workspace-scoped Employee / Responsibility / holder-executor truth。
- Team Operating real employee loop。
- RD Codex / Artifact / Evidence / Computer Access truth。
- Long-running submit/observe execution。
- Dynamic Workspace Package substrate。
- P7 Decision、Handoff、Result Reference。
- Bounded Autonomous Operating 与 evidence-bound learning。
- XHS v1 对发布/analytics 的 fail-closed truth。
- Channel capability negative evidence：无证据就是 UNKNOWN。

## 8. Product Claims That Are Not Yet Implemented

- “普通用户描述任意业务即可获得可经营 Workspace”。
- “Assistant 会完整引导创办并推荐/生成第一项业务”。
- “General Workspace 已具备完整团队经营闭环”。
- “Content Growth 当前 Professional Workspace 已实现”。
- “主流社媒可真实发布、回执、分析、评论、多账号”。
- “模型 Key 在正式 Desktop 中跨重启安全持续可用”。
- “系统具备可靠的成本预算、固定 retry/timeout、无限长期自主经营”。
- “安装版 Curis 可无 Core rebuild 自动生成任意专业 UI”。

## 9. V1 Cuts

以下不应阻塞首个可用 V1：

- 所有社媒 Channel 的真实接入与多账号。
- Template Marketplace。
- 自动生成任意高自由度专业 UI。
- 通用 DAG / Workflow Engine / parallel scheduler。
- 无限自主 Cycle、自动 Strategy 改写、完整成本优化。
- Full Computer Access。
- 所有 Agent / Provider / Tool / Connector 广度。
- Content Growth 全渠道完成度。

## 10. Final Answers

**A. Curis 当前实际上能做到哪一步？** 真实 Company OS 与 execution substrate 已相当完整；可以持久化 canonical Business/Workspace，运行真实员工/Codex，形成 Artifact/Evidence/Decision，并在 XHS/RD/Package 样例中证明多个纵向切片。

**B. 当前为什么还不是 V1？** 用户主路径没有装配：First Run 不到 Business/Workspace，General Workspace 不完整，Secret 重启连续性不足，缺 whole-app packaged E2E。

**C. 离普通用户日用还有多远？** V1 计分项约剩 33%，但真正距离由 5 个 P0 阻断决定；这些闭合前不能用 67% 推断“基本可用”。

**D. 当前最接近完整的专业 Workspace？** RD。它已有真实 Codex、Artifact/Evidence、failure/restart、专业 UI、review/handoff/P7 底座。XHS 内部产品形态真实，但外部结果能力缺失且当前 Content Growth authority 已演进。

**E. General Business 的真实缺口？** 不是缺 Runtime primitive，而是缺普通用户创建入口、team/responsibility materialization、通用 conversation/current work/result/decision/history 的产品装配。

**F. Capability 最大风险？** 目录存在被误当作可用；尤其 Secret persistence、cloud provider、MCP 和 Channel connectors 没有足够真实 E2E。

**G. 最短 V1 路径？** 先闭合 First Run + canonical General Business，再装配 General operating loop，随后把已成熟 RD 接入同一入口，最后补 packaged whole-app/release gate；不要先扩 Provider 或 Channel 广度。

**H. 第一项开发任务？** `V1-P0-001`：复用 FoundingRun、Business Spine 和 generic Workspace Package，把“用户经营意图 → Proposal → canonical Business + First General Workspace → 可回访 Workspace”接成一条真实、原子、可重启的产品路径。

## 11. Final Decision

`CURIS V1 APP READINESS — NOT READY`

Reason: Runtime foundation is strong, but the ordinary-user product spine is not yet closed.

### Read-only Safety Record

No source, Runtime, Schema, test, or SQLite data was changed by this audit.

| Active SQLite | Size | mtime (epoch) | SHA-256 | integrity_check |
|---|---:|---:|---|---|
| `data/curis.sqlite` | 1232896 | 1786873339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | ok |
| `backend/data/curis.sqlite` | 1277952 | 1786783659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | ok |
