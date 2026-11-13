# CURIS_HIFI_HTML_BASELINE_CONFIRMATION

> Authority Class: RESEARCH / EVIDENCE
> Status: CONFIRMED — 本轮 HIFI HTML 修复开始前的最小 Baseline 重读证明
> Date: 2026-09-13
> 方法：放弃上一轮会话缓存；AGENTS.md → PRODUCT_DOCUMENT_POINTER.md → Current Required Input 实读（Structure Baseline / Frozen Shell §2.3·§3.1·§3.5·§3.13·§3.14 / Visual Standard V1 / CG Authority / RD Instance 顶部 Supersession / CURRENT_STATE 头部），并完整读取 5 份 Codex 审计（codex-phase-2-verification/）。受控基线 commits a9bd736e9…/15e081a26…/2fabe5569…/78cacbd08… 已确认存在。

| Domain | Current Source | 本轮必须遵守的 Truth | 上一版 HTML 是否存在偏差 |
|---|---|---|---|
| Product Structure | Structure Baseline（Frozen） | 七个一级区；Company→Department→Business→Workspace；Business≠Workspace；Channel≠Workspace | 无偏差（七区/关系正确）；Business 数量与原装部门已按 CEO 纠偏修正 |
| Company OS | Shared Authority（Frozen） | Employee=公司身份；Leader=Employee×Role×Scope；Responsibility/Handoff 语义 Curis Original | Employee 目录/人才市场混淆已修；本轮不再回退 |
| Workspace | Frozen Shell Contract（§2.3 T1–T3、pane ownership） | 四 Pane 各自 header；Runtime State 不驱动展开；UI state 独立；scope 记忆 | PARTIAL：T 控件迁移/resize/maximize/记忆缺失 → 本轮修 |
| Employee | Shell §3.1/§3.14 | 三态：空闲 / 工作中·desc / 阻塞·cause；Conversation-first workstation；Detail→Utility；Holder≠Executor | STALE：默认进 profile、Context 放完整档案、header 按钮无效 → 本轮修 |
| Conversation | Shell §3.5 + WorkBuddy/ChatGPT/Cursor 参考（Final Decisions Z044–Z061） | 任务型结构；用户消息 bubble 局部 L4；AI 正文流；工具摘要折叠；动作行有真实 handler；发送追加 | STALE：发送不追加、动作无 handler、draft 丢失 → 本轮修 |
| Composer | Shell §3.5 Shared Composer（Frozen 槽位）+ RD Supersession（禁 Compact） | 槽位：Input / +Add / 访问权限▾（requested≠configured≠effective）/ 工作模式▾ / 已选资源 / 执行选择（Model≠Agent）▾ / Voice 可选 / Send；运行时 Composer 不消失 | STALE：固定控件、运行时整体替换、硬编码附件 → 本轮重写为共享状态机 |
| CEO Assistant | Structure Baseline（Global Floating） | 不属 Four-Pane；durable identity；展开/收起/输入保持/working/result-ready；无 console error | WRONG：`ico is not defined` 展开即崩、路由残留 → 本轮修（根因：app.js 未引入 ico 符号） |
| Content Growth | CG Domain Authority + CEO Reconciliation | Opportunity→Intent→TargetAccountSet→Variant→Publication；逐账号 eligibility/receipt；Candidate≠Verified；聚合 DOC 不替代逐账号状态 | PARTIAL：只有聚合 DOC → 本轮补逐账号发布链 |
| RD | RD Instance 顶部 Current Shared Rule Supersession + §1a | Holder≠Executor；ReviewRequest≠Handoff；状态来源唯一；Layer0 只能 查看方案/暂缓；Shared Composer 完整槽位 | WRONG/PARTIAL：高风险可直接批准、状态自相矛盾 → 本轮修 |
| Visual | Visual Standard V1（Frozen，Direction D / Iris #806BE5） | #806BE5 唯一 accent；#32f08c 仅 Legacy Implementation Token | 无偏差（Iris 已用）；继续小面积纪律 |
| Competitive Reference | CURIS_FINAL_COMPETITIVE_REFERENCE_DECISIONS.md（唯一有效登记） | 7 类局部 L4（WorkBuddy Expert/Skill/FileRef/MsgActions、Claude Model Selector、ChatGPT User Bubble、Linear Nav Rhythm）；EvoFlow EV01–EV10；旧 Matrix 仅 provenance | PARTIAL：0/24 L4 VERIFIED → 本轮按 M1/M2 实测重建 Expert/Skill 卡 |
| State/fixture 一致性 | Codex Drift Audit §Empty/Error | 同一 state 所有 Surface 一致；empty 不得混 running；error 不得显示已同步 | MIXED → 本轮修 fixture/state 系统 |

**结论：未发现无法解决的 Current/Frozen 冲突 → 立即继续 HIFI 实现（-1.6）。**
已固化不再重开：七区、Workspace vs Office、Iris vs legacy green、Employee 三态、RD Compact Composer 废止、Runtime 驱动 Pane 废止、CG Channel/Account identity、canonical Master Map/UI Blueprint 路径。
