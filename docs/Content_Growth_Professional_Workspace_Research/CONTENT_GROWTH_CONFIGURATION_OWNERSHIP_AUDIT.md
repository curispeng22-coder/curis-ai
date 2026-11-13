# CONTENT GROWTH — CONFIGURATION OWNERSHIP AUDIT
### 逐项配置/动作所有权审计 · Round 2「CEO 替 Employee 工作」步骤清单与修正方案（不新增功能）

Status: **RESEARCH / EXPERT RECOMMENDATION**（非 Frozen，非 Authority 修改）
Companion: `CONTENT_GROWTH_AI_COMPANY_OPERATING_EXPERIENCE.md`（CEO/AI/确认/Expert 归属总览 + 重跑 Journey + 真实用户测试）
前置：Round 2 全部 5 份交付；Frozen `Curis_Content_Growth_Domain_Authority.md`。

---

## 0. 红线与纪律

- 本轮**只审计所有权归属**，不新增功能、不画 UI / IA / Figma / 前端 / Runtime / Schema / DB / Authority。
- 所有结论消费 Frozen 不变量（见 Companion §0），不重定义。
- 目标：把专业配置/操作从 CEO 侧移回 AI 员工侧（A/B 最大化，C/D 最小化，E 隐藏）。

---

## 1. 分类维度定义

| 标记 | 名称 | 定义 | CEO 是否出现 |
|---|---|---|---|
| **A** | AI AUTO | AI 员工自己决定并执行，不惊动 CEO | 否 |
| **B** | AI RECOMMEND → USER CONFIRM | AI 给专业答案，CEO 只确认重大方向 | 是（看建议+采用/调整/讨论） |
| **C** | USER FACT REQUIRED | 只有用户自己知道的事实，必须问 | 是（提供事实） |
| **D** | EXTERNAL AUTHORIZATION | OAuth / 平台授权等必须用户操作 | 是（点一次授权） |
| **E** | EXPERT OVERRIDE | 默认隐藏，高级用户主动深入才手工配置 | 否（默认）；主动进才见 |

---

## 2. 逐项配置/动作所有权审计

> Current Owner = Round 2 实际归属；Correct Owner = 本轮裁定；A/B/C/D/E = 正确归属分类。
> 引用：Round 2 步骤号（Doc 编号见 Companion）。

### 2.1 经营/内容策略类

| # | Configuration / Action | Current Owner (Round 2) | Correct Owner | 分类 | Why |
|---|---|---|---|---|---|
| 1 | **Office Positioning（经营定位）** | 王颖建议，用户 A07「采用/修改/跳过」 | AI 分析后建议，CEO 确认 | **B** | AI 据主题+对标+参考推断；属重大方向，CEO 一眼确认即可，不填空白字段 |
| 2 | **Audience（受众）** | A02 问用户或推断 | AI 推断，建议确认 | **B** | AI 从内容主题+参考互动画像推断；用户仅必要时纠偏 |
| 3 | **Tone（调性）** | A07 建议，用户采纳 | AI 推断，建议确认 | **B** | 同 Audience；不要求用户配 Tone 词 |
| 4 | **Brand Context（品牌语境）** | A07 建议 | AI 从参考/目标推断；用户有品牌则 C | **B** (有品牌时 **C**) | 多数用户无显式品牌，AI 据参考推导；真有品牌事实才问 |
| 5 | **Keyword（关键词）** | A07 王颖派生 8 个，用户「采用」 | AI 自动派生并维护 | **A** | 纯专业派生，用户无需看；出现于 Expert 区 |
| 6 | **Content Strategy（内容策略）** | 隐含在 Brief | AI 基于定位+参考生成 | **A** | 策略是 AI 核心责任 |
| 7 | **Goal / Purpose（经营目的）** | A02 问「主要目的」 | 用户说一句目的 | **C** | 目的影响方案方向，且只有用户知道 → 必问（给推荐+其他） |

### 2.2 情报/研究类

| # | Configuration / Action | Current Owner (Round 2) | Correct Owner | 分类 | Why |
|---|---|---|---|---|---|
| 8 | **Source 发现（初始池）** | A03 让用户粘 5 个 URL | AI 自动发现（主题+对标+公开搜索） | **A** | Round 2 让用户供 URL 是 CEO 替 Employee 找米；AI 应自找 |
| 9 | **Source 增删/分类/优先级/监控策略** | B01–B05 对话自然语言 + B06–B07 专业区 | AI 维护（对话自然语言快捷保留） | **A** (对话快捷 C 轻量说) | 专业维护归 AI；用户「重点看这个」属自然语言，非配置 |
| 10 | **Source 专业管理界面** | B06–B07 CEO 可见低频区 | Employee Working Area | **E** | 底层字段默认隐藏，Expert 主动进才见 |
| 11 | **Competitor / 对标账号发现** | A07 王颖公开搜索 5 个 | AI 自动发现并监控 | **A** | 纯专业发现 |
| 12 | **Research Scope（研究范围）** | C03 用户可加来源；AI 设主 Scope | AI 按 Work 设；用户可自然语言补 | **A** (补 Source 轻量说) | 范围判断是 AI 责任 |
| 13 | **Monitoring frequency（监控频率）** | 默认 + 可改 | AI 按信号量自调 | **A** (E 可改) | AI 设合理默认并随负载调 |
| 14 | **Research depth / Cost（研究深度/成本）** | Unit-Economics Auto-Selector 约束 | AI 自动选档 | **A** (E 可改) | 成本/深度由 Auto-Selector 管，不烦 CEO |

### 2.3 渠道/账号类

| # | Configuration / Action | Current Owner (Round 2) | Correct Owner | 分类 | Why |
|---|---|---|---|---|---|
| 15 | **Channel strategy（渠道组合）** | E01 用户点平台连 | AI 推荐渠道（内容类型+目标+参考） | **B** | AI 据内容判断主发平台；用户确认 |
| 16 | **Connect Channel（连渠道）** | 用户点 OAuth | 用户点一次授权 | **D** | 外部授权必用户操作 |
| 17 | **Account 历史分析 / 定位推断** | E02 用户命名+配定位 | AI 读历史→分析→建议定位 | **A** | 分析是 AI 责任 |
| 18 | **Account 命名** | E02 用户命名「AI科技主号」 | AI 建议命名 | **A** (E 可改名) | 命名可由 AI 基于分析生成 |
| 19 | **Account 角色/用途** | 隐含 | AI 推荐角色 | **A** (B 确认) | AI 判断账号用途 |
| 20 | **Default Account（默认账号）** | STEP 07 用户设默认 | AI 推荐默认并随表现自调 | **A** | 默认选择 AI 负责 |
| 21 | **Account 授权状态维护** | 系统标红+用户重授权 | 系统标红+AI 提示；用户点授权 | **D** (状态 A) | 失效 AI 检测；重连需用户 OAuth |
| 22 | **匹配/不匹配放行（覆盖发布）** | F01 STEP 11 用户确认覆盖 | AI 检测并提示；Expert 才手动放行 | **E** (提示 A) | 普通用户不应处理定位不匹配 |

### 2.4 内容生产类

| # | Configuration / Action | Current Owner (Round 2) | Correct Owner | 分类 | Why |
|---|---|---|---|---|---|
| 23 | **Brief 生成** | B01 李想生成；B03 用户可编辑字段 | AI 生成；CEO 看成品 | **A** (深编 E) | Brief 是 AI 责任；默认 CEO 不填 |
| 24 | **Draft 生成 + 版本（1–3 版）** | D01 用户点「生成草稿」 | AI 自动出推荐版 | **A** | 生成是 AI 责任；点一下是确认入口 |
| 25 | **版本选择 / 比稿** | D02/D03 用户并排比稿选推荐版 | AI 推荐推荐版+标备选 | **A** (深比稿 E) | 选版是 AI 判断；CEO 看推荐版 |
| 26 | **内容修改（说话改/直接改）** | E01/E02 用户改 | AI 按一句意见改 | **A** (轻量说 C) | 用户说一句，AI 执行 |
| 27 | **素材生成 / 选择** | A01/A02 用户选生成几版/上传/库选 | AI 生成并选；CEO 看结果 | **A** (深管 E) | 素材是 AI 责任 |
| 28 | **审核五项（品牌/事实/合规/AI标识/渠道规则）** | R01/R02 用户看五项+点一键修改 | AI 自检并自动修复 | **A** | AI 自检自修；仅风险知情 CEO |
| 29 | **Content format（内容格式）** | 隐含在 Brief | AI 按渠道+参考选 | **A** | 格式判断 AI 责任 |

### 2.5 发布/分发类

| # | Configuration / Action | Current Owner (Round 2) | Correct Owner | 分类 | Why |
|---|---|---|---|---|---|
| 30 | **Distribution target（发哪些平台/账号）** | F01 STEP 10 用户勾 Channel→Account 树 | AI 推荐目标账号集 | **B** | AI 据内容+策略+历史+Eligibility 推荐；CEO 确认 |
| 31 | **Variant 适配档位（轻/重/完全不同）** | STEP 14–17 用户看预览 | AI 按账号定位自动选档 | **A** (E 可改) | 适配判断 AI 责任 |
| 32 | **发布时间（立即/定时）** | STEP 18 用户逐账号设 | AI 建议时间；默认立即 | **A** (精调 E) | 时间建议 AI 给；CEO 确认 |
| 33 | **发布确认（Human-in-the-loop）** | STEP 19 用户确认 | 用户一次确认 | **B / D 边界** | 不可逆外部动作，必须 CEO 确认 |
| 34 | **失败重试 / 驳回重提** | STEP 25/26/24 用户点重试 | AI 自动重试/提示 | **A** (CEO 知情) | 重试是 AI 责任；CEO 看结果 |
| 35 | **Distribution Execution Policy（BEST_EFFORT/ALL_REQUIRED）** | 默认 + 可配 | CEO 定信封边界；默认 AI 推荐 | **C** (默认 B) | 策略信封属 CEO 重大边界，但默认由 AI 提 |
| 36 | **Publishing frequency（发布频率）** | 默认 + 可改 | AI 按平台限频自设节奏 | **A** (E 可改) | 频率 AI 守平台规则 |

### 2.6 评估/治理类

| # | Configuration / Action | Current Owner (Round 2) | Correct Owner | 分类 | Why |
|---|---|---|---|---|---|
| 37 | **Evaluation（什么有效/为什么/建议）** | G01 周明做 | AI 做 | **A** | 评估是 AI 责任 |
| 38 | **下一轮建议/自动起周期** | G02 用户点「按建议继续」 | AI 自动起；CEO 确认 | **B** | AI 起下一轮，CEO 点确认 |
| 39 | **Strategy Envelope 越界（变现/换道/超预算）** | 触发 CEO Gate | CEO 裁决 | **C** | 越界属 CEO 重大方向/预算 |

---

## 3. EMPLOYEE OWNERSHIP 证明（每个 AI AUTO 项如何被真正完成）

> 不是「AI 自动配置」四个字结束。逐关键项证明 AI 员工如何完成专业工作。

### 3.1 Source 发现（项 8，A）
- **谁负责**：王颖(Research&Intel)。
- **如何判断**：从 Office 主题（AI 科技）+ 参考账号（若贴链接）→ 公开搜索相关官网/媒体/RSS/对标账号；按相关性初筛。
- **依据 Evidence**：主题关键词命中、参考账号互链、行业媒体权威性。
- **错了怎么纠正**：用户说「别看这个」→ 降优先级/移除；用户说「重点看这个」→ 升优先。
- **何时自调**：监控 2 周信号稀疏 → 自动扩展公开搜索并标「扩展」；信号过载 → 收紧。
- **何时升级 Leader**：需跨 Office 共享情报源策略 → 报周明。
- **何时找 CEO**：几乎不找；仅当用户明确要求「只盯我给的这几个」且限制研究范围时知情。

### 3.2 Account 定位/命名/默认（项 17–20，A）
- **谁负责**：陈帆(Channel Operator) 协同 王颖。
- **如何判断**：读账号历史内容（类型/互动/更新/增长）→ 推断定位/受众/调性 → 比对 Office 整体定位 → 建议命名（如「AI科技主号」）+ 角色 + 默认。
- **依据 Evidence**：历史帖子主题分布、高互动内容特征、粉丝画像（平台可得部分）。
- **错了怎么纠正**：用户「调整」→ 改该账号定位/命名；不影响其他账号（Frozen `NO_CROSS_ACCOUNT_CONTEXT_LEAK`）。
- **何时自调**：某账号表现持续优于默认 → 自动提升为默认候选；掉线/失效 → 降级（Frozen `OAUTH_FAILURE_KEEPS_ACCOUNT`）。
- **何时升级 Leader**：矩阵需分组（如 KOS）且涉合规同质化 → 报周明。
- **何时找 CEO**：仅当用户要「换大方向」（如账号转做带货）→ Strategy Envelope 越界（项 39，C）。

### 3.3 Distribution target（项 30，B）
- **谁负责**：陈帆(Channel Operator)。
- **如何判断**：内容定位 + Channel Strategy + 各 Account Positioning + 历史表现 + Eligibility（失效/未授权 BLOCKED）+ Distribution Policy → 推荐账号集。
- **依据 Evidence**：账号历史表现、定位匹配度、Eligibility 状态、平台限频。
- **错了怎么纠正**：用户「调整」→ 增减账号；不匹配账号默认灰显不强行（项 22，E）。
- **何时自调**：某账号近期表现好 → 后续默认优先；频率触顶 → 自动错峰。
- **何时升级 Leader**：跨 Channel 排期冲突（Calendar Gap/Conflict）→ 报周明。
- **何时找 CEO**：仅不可逆外部动作需确认（项 33，B/D 边界）；越信封才 Gate（项 39）。

### 3.4 Brief / Draft / 版本（项 23–25，A）
- **谁负责**：李想(Producer)。
- **如何判断**：基于 Intent + Research Evidence 起草 Brief；生成 1–3 版 Draft，按渠道/风格差异标注；推荐一版为推荐版、余为备选。
- **依据 Evidence**：Research 结论、参考账号表达风格、平台格式规范。
- **错了怎么纠正**：用户说一句（「更口语」）→ Patch；用户「调整」→ 改 Brief 重生成。
- **何时自调**：某版互动预期高 → 提为推荐版；版本达上限（5）→ 提示选定/合并。
- **何时升级 Leader**：内容涉合规红线 → 报陈帆/周明。
- **何时找 CEO**：仅发布确认（项 33）与越信封（项 39）。

### 3.5 Review 五项（项 28，A）
- **谁负责**：李想(Producer) 自检 + 陈帆(Channel Operator) 提供渠道规则。
- **如何判断**：跑品牌/事实/合规/AI标识/渠道规则五项；失败项自动补标识/核事实/改词。
- **依据 Evidence**：平台禁词库、事实来源可信度、合规骨架。
- **错了怎么纠正**：员工修后复审；仍无法核实的事实 → 提示删表述/补来源，不强制过。
- **何时自调**：渠道规则更新 → 自动同步。
- **何时找 CEO**：几乎不找；仅风险需知情（如「已发布但平台可能复审」）。

---

## 4. CEO DECISION TEST（每次想问 CEO 前先过三关）

> 引用 Companion §1 三句话门槛。落地为可执行的判定顺序：

1. **AI 能根据 Goal + Reference + Existing Assets + Evidence + Strategy Envelope 合理判断吗？** → 能则不问（A/B）。
2. **是用户独有事实吗？**（目的/愿露脸/已有产品/账号/预算时间/个人偏好）→ 是才问（C）。
3. **是不可逆外部动作吗？**（发布/OAuth/重大预算方向风险）→ 是才确认（B/D）或 Gate（C）。

**CEO 主要保留**：目标 · 真实限制 · 个人偏好 · 重大方向 · 重大预算 · 重要风险 · 不可逆外部动作 · Strategy Envelope 越界。其余一律归 AI。

---

## 5. ROUND 2「CEO 替 Employee 工作」步骤清单与修正方案

> 这是本轮核心交付：列出 Round 2 中仍让小白 CEO 做专业工作的步骤，逐一给修正。

| # | Round 2 步骤 | 当时让 CEO 做了什么 | 问题 | 修正方案（本轮） | 归属变化 |
|---|---|---|---|---|---|
| R1 | A03 补 Source | 让用户粘 5 个 website URL 作初始 Source | AI 应自己找米，不该让用户供 URL | AI 自动发现初始 Source 池（主题+对标+公开搜索）；用户零输入起步；仅「重点看这个/别看这个」自然语言快捷 | CEO→AI (A) |
| R2 | A02 三问（受众/渠道/账号） | 问用户「主要面向谁/主要在哪发/已有账号吗」 | 这些可 AI 推断，不应提问 | 三问全改 AI 推断；仅「目的」与 USER FACT（愿露脸/有产品/有账号/预算）才问，且可全跳过 | CEO问→AI推断 (A/B) |
| R3 | A07 定位/关键词/对标展示 | 用户看空白建议卡并「采用」 | 近似合理，但应直接填好不待填 | AI 已填好 growth_context；CEO 只见「建议这样」结果卡+采用/调整/讨论，无空白字段 | 维持 B，去「待填」感 |
| R4 | E02 STEP 06 命名+定位 | 用户命名账号+选/配 Audience/Tone | 命名与定位是 AI 责任 | AI 读历史→建议命名+定位+角色+默认；CEO 只见「建议这样用」卡 | CEO→AI (A)+确认(B) |
| R5 | STEP 07 设默认账号 | 用户手动设默认 | 默认选择 AI 负责 | AI 推荐默认并随表现自调 | CEO→AI (A) |
| R6 | F01 STEP 10 发布目标树 | 用户展开 Channel→Account→Variant 树手动勾选 | 小白不该管账号矩阵 | AI 推荐「发哪些平台/账号/何时」建议卡；CEO 一次确认 | CEO→AI (A)+确认(B) |
| R7 | B06–B07 专业 Source 管理区 | CEO 可见低频区，可增/分类/搜/批量 | 底层字段应隐藏 | 降级 EXPERT ONLY / Employee Working Area | CEO→EXPERT (E) |
| R8 | Doc3 B03 编辑 Brief | 用户编辑 Brief 六字段 | Brief 应 AI 产，CEO 看成品 | 默认 AI 产 Brief；深度改 Brief 降 EXPERT | CEO→AI (A)+EXPERT(E) |
| R9 | Doc3 D02/D03 选版本/比稿 | 用户并排比稿选推荐版 | 选版是 AI 判断 | AI 推荐推荐版+标备选；深度比稿降 EXPERT | CEO→AI (A)+EXPERT(E) |
| R10 | Doc3 A01/A02/A03 素材 | 用户选生成几版/上传/库选 | 素材 AI 责任 | AI 生成并选；深度素材库管理降 EXPERT | CEO→AI (A)+EXPERT(E) |
| R11 | Doc3 R01/R02 审核 | 用户看五项+点「一键让员工修改」 | 应 AI 自检自修 | AI 自检五项并自动修复；仅风险知情 CEO | CEO→AI (A) |
| R12 | STEP 18/19 发布时间 | 用户逐账号设时间 | 时间建议 AI 给 | AI 建议时间/默认立即；逐账号精调降 EXPERT | CEO→AI (A)+EXPERT(E) |
| R13 | STEP 11 不匹配覆盖 | 用户确认覆盖发布 | 普通用户不处理定位不匹配 | AI 检测灰显；手动放行降 EXPERT | CEO→EXPERT (E) |
| R14 | C03 补 Source（日常） | 用户粘 URL 入 Scope | 保留为自然语言快捷，但非必经 | 保留「重点看这个」自然语言；默认 AI 管 Scope | 维持（轻量说 C） |

**总判定**：Round 2 共 14 处让 CEO 替 Employee 工作，本轮全部反转为 **A（AI AUTO）/ B（AI 建议+确认）/ E（Expert 隐藏）**。CEO 在常态经营中不再做任何专业配置。

---

## 6. 不可逾越的红线（仍必须由用户/CEO 操作）

即便最大化 AI 责任，以下仍不可自动化（对应 Frozen 与产品纪律）：
- **OAuth 授权**（D）：连渠道/重授权必须用户点一次。
- **发布确认**（B/D 边界）：内容出站是不可逆外部动作，必须 CEO 一次确认（Human-in-the-loop）。
- **Strategy Envelope 越界**（C）：变现/换赛道/超预算/重大风险 → CEO Gate。
- **用户独有事实**（C）：目的/愿露脸/已有产品/账号/预算时间/个人偏好。
- **已发生事实不回滚**（Frozen `FACT_NOT_ROLLED_BACK`）：发布成功/失败状态不可篡改。
- **账号失效不删**（Frozen `OAUTH_FAILURE_KEEPS_ACCOUNT` / `TARGET_NE_ELIGIBILITY`）：失效仅 BLOCKED，禁静默删。

---

*CONTENT_GROWTH CONFIGURATION OWNERSHIP AUDIT — RESEARCH / EXPERT RECOMMENDATION — STOP FOR CEO REVIEW*
