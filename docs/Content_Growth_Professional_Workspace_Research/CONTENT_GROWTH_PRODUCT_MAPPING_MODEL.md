# CONTENT GROWTH — PRODUCT MAPPING MODEL
### Domain → Curis Product Object · CEO / Surface / Employee / Runtime 层级

Status: **RESEARCH / EXPERT RECOMMENDATION**（非 Frozen，非 Authority 修改）
Companion: `CONTENT_GROWTH_PRODUCT_EXPERIENCE_MODEL.md` · `CONTENT_GROWTH_USER_JOURNEY_MODEL.md` · `CONTENT_GROWTH_CURRENT_UI_RECONCILIATION.md`
前置研究：本轮前 5 份 Content Growth 领域交付（Domain Operating Model / Operating Matrix / Shared vs Channel / CEO Experience / Unit Economics）。

---

## 0. 本模型的性质与红线

- **是**：把已完成的「内容增长领域运营模型」翻译成 **Curis 产品对象与层级**，让业务模型可被产品/IA/后续 UI 研究消费。
- **不是**：UI 设计、Figma、前端、Runtime 实现、Schema、DB、Blueprint、任何 Frozen 文档的修改。
- **红线（本轮 + STOP GATE 双重约束）**：
  - **禁止发明新 Runtime primitive**。Domain 概念若现行 Curis 对象无干净归处，标记为 **GAP** 并建议「复用现有对象」，**不**新造 Signal/Opportunity/Topic 等运行时类型。
  - 只**消费** Frozen Authority：`Curis_Company_OS_Shared_Authority.md`、`Curis_Content_Growth_Domain_Authority.md`、Opportunity→Intent→Target→Variant→Publication 链、Package v2、Autonomous Operating、Canonical/Child/Multi-Work、Result/Evidence/Handoff/Decision/Cycle、Employee/Responsibility。
  - 本研究所有结论为 **RESEARCH / EXPERT RECOMMENDATION**，待 CEO REVIEW。

证据标记沿用：`[CURIS-AUTH]`=现行 Frozen 语义（消费非修改）·`[CAND]`=候选建议·`[INF]`=推断·`[COMP]`=竞品/第三方·`[REAL]`=已验证。

---

## 1. 产品层级模型（回答本轮 §2）

```
CEO Experience（投影层）
  ↓ 只投影 Result / Decision / Handoff 等现有对象，不暴露内部复杂度
Workspace Main（默认入口 = 经营驾驶舱）
  ↓ 是 Surface 之一，但语义特殊：只呈现「经营结果类型」投影
Professional Surface（深入工作面，Employee 主用、CEO 按需）
  ↓ 只声明 Responsibility Requirement（WHAT），不绑定 Employee
Employee Work Area（员工按 Responsibility 执行）
  ↓ 消费
Work / Result / Evidence / Handoff / Decision / Cycle（Company OS 执行真源）
  ↓ 由
Runtime（Autonomous Operating · Canonical/Child/Multi-Work · Responsibility Router · Capability · Connector）
```

### 1.1 每层负责什么 / 不负责什么

| 层 | 负责 | 不负责 |
|---|---|---|
| **CEO Experience** | 把员工结果投影为「价值/风险/建议/待决」；只呈现 Result/Decision 类型 | 不做任何执行；不展示原始 Signal/Analytics/草稿 |
| **Workspace Main** | 默认呈现 8 类经营结果类型（见 OUTPUT 2）；是「经营驾驶舱」 | 不承载全量池/库/Dashboard；不做深度编辑 |
| **Professional Surface** | 围绕特定专业对象/判断组织观察与工作面；声明所需 Responsibility | 不绑定 Employee ID；不新建 Surface Runtime/Agent/Cycle/Result；不解释行业方法（`NO_SURFACE_RUNTIME` `[CURIS-AUTH]`） |
| **Employee Work Area** | 员工经 Assignment 按 Responsibility 在此执行、产出 Work/Result/Evidence | 不决定 WHO（WHO 由 Organization Routing 解）；不拥有 Workspace 上下文 |
| **Work / Result / Evidence** | 公司 OS 执行真源；原子释放与聚合；投产回 Workspace Truth | 不重复造第二套 Task/Workflow/Runtime（Autonomous Operating `[CURIS-AUTH]`） |
| **Runtime** | 确定性执行：Cycle bounded+Close、Responsibility Router、Capability·Connector、Channel 发布 | 不解释「内容增长应如何经营」（那是本研究/Empirical Layer 的内容） |

> 关键纪律：`Process asks WHAT / Org decides WHO / Capability determines HOW` `[CURIS-AUTH]`。Surface 与 Workspace Main 只声明 WHAT（Responsibility Requirement），WHO/HOW 由下层解析。

---

## 2. Domain Concept → Curis Product Object 映射（回答本轮 §21）

> 原则：Domain 概念尽量落在 **已有 Curis 对象**；若仅是「领域数据对象」而非 Runtime 类型，则**通过 Surface 投影 + 以 Artifact/Work 产物承载**，不新造 primitive。GAP 行给出复用建议。

| # | Domain Concept（领域概念） | 归属层 | 映射到现有 Curis 对象 | 说明 / 标记 |
|---|---|---|---|---|
| 1 | **Signal（信号）** | SHARED | **Artifact**（领域数据对象）+ 由「信息与机会」Surface 投影 | Signal 不是 Runtime primitive；它是 Information Gathering Work 的产物，以结构化 Artifact 存在于 Workspace Truth。`[CAND][CURIS-AUTH: Artifact=共享Truth]` |
| 2 | **Opportunity（机会）** | SHARED | **Artifact**（Content Opportunity，Frozen 已定义 `[CURIS-AUTH]`）+ 「信息与机会」Surface 投影 | Opportunity 已是 Frozen 内容域对象（§1.5）；SHARED 上游，服务多 Intent |
| 3 | **Topic（选题，选题池项）** | SHARED | **Artifact**（curated Opportunity）+ 「选题」Surface；高价值进 **Decision**（CEO Gate） | 选题 = 经评分入选的 Opportunity；池本身 = Surface 上的 Artifact 集合，非新对象 |
| 4 | **Research（调研对象）** | SHARED | **Work**（Research Work）+ 闭合后 **Result** + **Evidence**；Deep Research = 同 Work 的深 Scope 变体 | 研究是 Work，不是数据对象；深度由 Scope 决定，不新造「Research 对象」`[CURIS-AUTH: Work/Result]` |
| 5 | **Brief / Content Intent** | SHARED | **Content Intent**（Frozen `Curis_Content_Intent_Contract_Candidate`）+ 由 Brief Work 产出 **Result**；「内容」Surface 投影 | Intent = 共享上游（WHY/WHAT/GOAL），不存推理 `[CURIS-AUTH: INTENT_EXCLUDES_INFERENCE]` |
| 6 | **Draft（草稿）** | SHARED | **Artifact**（work-in-progress 内容）+ 挂在对应 Work 下 | 草稿是 Artifact，版本管理由 Work/Artifact 机制承载 |
| 7 | **Asset（素材/资产）** | SHARED(核心)+CHANNEL(格式) | **Artifact**（可复用，进成果库）+ 「资产与知识」Surface | 核心创意跨渠道复用；格式包按 Channel 分 `[COMP]` |
| 8 | **Variant（账号变体）** | CHANNEL | **Content Variant**（Frozen `Curis_Content_Variant_Publication_Contract_Candidate`）+ 由 Channel Adaptation Work 产出；绑单一账号 | ⑪ 分叉点产物；HIGH_REUSE/FULL_DIVERGENCE `[CURIS-AUTH]` |
| 9 | **Publication（发布真相）** | CHANNEL | **Result**（per-Account 真相）+ receipt 由 **Connector** 回填 `[CURIS-AUTH: RECEIPT_FROM_CONNECTOR]` | 发布不是终点；Publication 是事实记录，回流 Evaluation |
| 10 | **Feedback（用户反馈）** | CHANNEL(收件)→SHARED(信号) | CHANNEL **Module** 收件箱采集 → 归一化为 **Signal(Artifact)** 回流；「反馈」Surface 投影归一后结果 | 采集属 Channel；归一后 Signal 属 SHARED |
| 11 | **Evaluation（效果评估）** | SHARED | **Result**（Evaluation Work 产物）+ 「增长与评估」Surface | 归因+判断，跨渠道可比 `[COMP]` |
| 12 | **Learning / Strategy Adjustment** | SHARED | **Knowledge**（知识库更新）+ **Approved Strategy Envelope**（Frozen 概念）更新 | Learning = 更新 Knowledge/信封；信封越界→CEO Gate `[CURIS-AUTH §0.2]` |

### 2.1 关键映射裁定

- **Signal / Opportunity / Topic 不是新 Runtime 对象**：它们一起被「信息与机会 + 选题」两个 Surface 投影，底层以 **Artifact** 承载。理由：Frozen Authority 已声明 Artifact 为共享 Truth 之一 `[CURIS-AUTH]`，且明确「禁止 Surface 新造 Result/Session/Runtime」`[CURIS-AUTH]`。新造会破坏该不变量。
- **Research / Brief / Evaluation / Publication 是 Work/Result**：已有完备 Work/Result/Evidence/Cycle 机制，直接复用（PARTIAL：需定义 Content 域的 Work 子类型与 Result 类型枚举，属 Extension/Contract 层，非新 primitive）。
- **Variant / Publication 已是 Frozen 内容域契约**：直接消费，不重定义。
- **Channel（XHS/Douyin）= Channel 对象 + Module + Connector**：发布执行与回执由 **Capability·Connector** 承担，契约只引用回执 `[CURIS-AUTH]`。

### 2.2 GAP 清单（不发明，只标记）

| GAP | 描述 | 复用建议（非新造） |
|---|---|---|
| G1 | 无独立「Signal 类型」运行时对象 | 以 Artifact + Signal Schema（结构约定）承载；Surface 投影 |
| G2 | 无独立「Topic/选题」运行类型 | Artifact（curated）+ 选题 Surface 集合视图 |
| G3 | 内容域 Work/Result 子类型枚举未定义 | 在 Extension/Contract 层定义（Content Research Work / Content Brief Work / Channel Publish Work / Evaluation Work 等），复用 Canonical/Child Work |
| G4 | 「经营驾驶舱」Main 的 Result 聚合视图 | 复用 Result/Decision/Handoff 对象的投影，不新造聚合 primitive |

---

## 3. CEO / Surface / Employee / Runtime 四级职责落点（对照本轮 §2/§4/§18）

| 概念 | 出现在哪层 | 谁生成 | 谁消费 |
|---|---|---|---|
| 员工结果（Employee Result） | Work/Result（Runtime）→ 投影至 Workspace Main（CEO Experience） | Employee（按 Responsibility） | CEO（投影）/ Employee（追溯） |
| 需 CEO 决定的事（Decision / Gate） | Decision（Runtime Cycles 的 CONTINUE/ADJUST/WAIT/ESCALATE）+ CEO Gate | 高价值/超信封/不可逆由系统标记→CEO | CEO（批准/调整/讨论/暂停） |
| 专业工作面（Surface） | Professional Surface | 声明 Responsibility Requirement；Employee 经 Routing 进入 | Employee（主）/ CEO（按需） |
| 渠道动作（Channel） | Channel Module + Connector（Runtime） | Channel Operator（Employee） | 用户仅 awareness 时进入 |
| 三入口（对话/当前工作/员工资料） | CEO Assistant（对话）+ Current Work + Employee Quick Detail（Utility） | 现有 Company OS 三入口模型 | CEO |

---

## 4. 与现有架构的复用结论（回答本轮 §22）

| 现有架构对象 | 复用判定 | 说明 |
|---|---|---|
| Autonomous Operating（自主运行） | **REUSE** | 直接承载 Operating Loop；Cycle bounded+Close，不第二套 Runtime |
| Canonical / Child / Multi-Work | **REUSE** | Research Work + Content Work + Channel Publish Work 同 Cycle 跨 Surface（Multi-Work 已证明）`[CURIS-AUTH]` |
| Result / Evidence / Handoff / Decision | **REUSE** | 全部 16 阶段以这些对象承载；Handoff = 员工间真实结果传递 |
| Cycle（CONTINUE/ADJUST/WAIT/ESCALATE） | **REUSE** | 下一周期决策直接用；PAUSE/STOP 边界明确 |
| Professional Workspace / Package v2 | **REUSE** | Content Growth = 一个 Professional Workspace Package（多 Surface）；XHS/Douyin = 其下 Channel |
| Employee / Responsibility（WHAT→WHO→HOW） | **REUSE** | 最小可行团队 4 责任类（Strategist/Research&Intel/Producer/Channel Operator） |
| Opportunity→Intent→Target→Variant→Publication | **REUSE（Frozen）** | 直接消费，不重定义 |
| Surface（NO_SURFACE_RUNTIME 等不变量） | **REUSE** | 新 Surface 仅声明 Responsibility，不绑 Employee/不新 Runtime |
| Artifact / Knowledge / Capability / Channel / Connector | **REUSE** | Signal/Opportunity/Topic/Asset/Draft 以 Artifact 承载；发布以 Connector 执行 |
| **新 Runtime primitive** | **NOT NEEDED** | 严禁发明；GAP 以复用解决（§2.2） |

---

## 5. 本轮 FINAL 13 QUESTIONS — 逐条回答

**Q1. 用户打开 Content Growth 第一眼看到什么？**
→ 经营驾驶舱（Workspace Main）= 员工最新结果 + 当前经营重点 + 需关注变化(3条级) + 需决定事项 + 重要在途工作 + 增长变化 + 下一步推荐。不是信息池/选题池/Dashboard。详见 OUTPUT 2 §1。

**Q2. 用户今天怎么知道「该做什么」？**
→ 驾驶舱的「需关注变化」+「需决定事项」+「下一步推荐」三块；由员工结果投影与 Decision/Handoff 对象生成。系统主动提示 WAIT/SKIP/STOP（`[CURIS-AUTH]`），不要求用户翻池。

**Q3. 信息池/选题池谁用，CEO 什么时候看？**
→ 信息池=Research&Intel Employee 在专业 Surface 操作；选题池=Employee Working View（推荐子集+完整池）。CEO 默认只看「推荐 3 个选题」投影；仅在想深究时进入完整池（Employee Working View 与 CEO Review View 同对象不同投影深度，不复制数据）。

**Q4. Employee Result 如何进入默认 Main？**
→ Work 闭合产出 Result/Evidence → 经 CEO Projection 规则（内部复杂度→员工结果→CEO 投影，OUTPUT 2 §3）压缩为驾驶舱卡片 → 作为 Result 对象的投影呈现，不新造聚合 primitive。

**Q5. CEO 批准一个方向后系统如何自然继续？**
→ CEO 在 Decision 上选 批准/调整/讨论/暂停 → 系统创建 exactly one next Cycle（ADJUST 须在新信封内且有 Evidence）`[CURIS-AUTH]` → 经 Handoff 把结果传给下一 Responsibility → 下一 Stage Work 自动起。全程复用现有 Cycle/Handoff/Decision，不第二套流程。

**Q6. 16 阶段如何压缩成少量 Professional Surfaces？**
→ 7 个 Surface：信息与机会(①②③)/选题(④⑤)/研究与洞察(⑥)/内容(⑦⑧⑨⑩⑪)/增长与评估(⑬⑮⑯)/反馈(⑭)/渠道(⑫+渠道原始)。组合理由见 OUTPUT 2 §4。Calendar 为内容 Surface 内视图（OPEN QUESTION Z1/Z7）。

**Q7. XHS/Douyin 在产品里到底怎么出现？**
→ 作为 **Channel 对象**：Channel switch（用户 awareness 时）/ Publishing target / Channel-specific Module（格式/发布/分析/反馈）/ Context filter。不默认做成 XHS Tab/Douyin Tab；系统多在后台自动处理，用户仅在需要选渠道/看渠道真相时意识到。`[CAND]` 详见 OUTPUT 2 §6。

**Q8. Quick Path 如何保持最简单？**
→ 用户对话 → 系统按价值/复杂度自动选 Quick/Structured/Deep（OUTPUT 2 §7）。用户说「帮我写篇 GPT-5.6 小红书笔记」仍停留在 Conversation；系统后台可能创建 Structured Work，用户无需知道/选择 Workflow。

**Q9. Structured/Deep 如何在后台升级而不增加用户负担？**
→ 检测到多平台/品牌/合规/需测量时，系统以非阻塞提示（如「这个主题值得先做调研，预计复用到 3 渠道」），用户只需 继续/直接生成/讨论；不展示 16 阶段内部流程（OUTPUT 2 §7）。

**Q10. Current Work / Result / Evidence / Handoff 如何复用现有 Company OS？**
→ 全部 16 阶段以现有对象承载（见 §4 REUSE 表）；Handoff = 员工间真实结果传递（非 CEO 升级）；Evidence 回流 Workspace Truth 且执行时仅 task-scoped 检索（Context Isolation `[CURIS-AUTH]`）。

**Q11. 现有 XHS 页面哪些应该被淘汰或重组？**
→ 见 OUTPUT 4：overview/research/content/growth/feedback → REPURPOSE 为 Content Growth 共享 Surface（去 XHS 化）；commercial → DEMOTE 为 Channel Module；calendar → KEEP 视图；rdcheck → REMOVE；旧 workspace-runtime-xhs → DEMOTE 为 Channel 视图；平台 nav「小红书运营办公室」应改为 Content Growth 下的 Channel 入口（Office 隐喻已 deprecated `[CURIS-AUTH §3.2]`）。

**Q12. 还缺哪些 Product 能力？**
→ 非新 primitive，但需 Extension/Contract 定义：内容域 Work/Result 子类型（G3）、Signal Schema 结构约定（G1）、CEO Projection 聚合规则、Unit-Economics Auto-Selector、Channel Connector Framework（XHS/Douyin Module）。详见 OUTPUT 4 §5。

**Q13. 下一步到底应该进入 IA/低保真，还是仍需研究？**
→ 领域与产品映射研究已完成且自洽；建议**下一步进入 IA / 低保真结构稿**（非高保真/Figma），消费本模型 + OUTPUT 2/3 的语义。仍有 OPEN QUESTION 需 CEO 裁决（见 §6）后方可动手。

---

## 6. OPEN QUESTIONS FOR CEO（待裁决，不自行推进）

1. **Workspace 边界**：采纳「Content Growth = Professional Workspace；XHS/Douyin = Channel」？（影响 Package 设计与平台 nav）
2. **Surface 集合**：采纳 7 Surface 划分（信息与机会/选题/研究与洞察/内容/增长与评估/反馈/渠道）？
3. **CEO Gate 阈值**：哪些「高价值机会/重大投入/不可逆外部动作」强制进 Gate（建议清单见 OUTPUT 2 §2）？
4. **Human-in-the-loop 默认**：发布默认需人类确认，仅三条件齐备才受控自动发布，是否采纳？
5. **平台 nav 改造**：是否将「小红书运营办公室」改为 Content Growth Workspace 下的 Channel 入口（Office 隐喻 deprecated）？
6. **Channel Connector 扩展顺序**：XHS → Douyin → 公众号/视频号/B站？
7. **单位经济红线**：是否设单内容 Token/成本上限与复用次数阈值作为 Worth-Doing 自动判定输入？

---

*CONTENT GROWTH PRODUCT MAPPING MODEL — RESEARCH / EXPERT RECOMMENDATION — STOP FOR CEO REVIEW*
