# CONTENT GROWTH — IA ROUND 2 OBJECT MODEL

> Status: Research / IA Design  
> Authority Class: RESEARCH  
> Scope: Core object and interaction structure; low-fidelity only  
> Round 1: CEO Accepted  
> Current Capability: consume Channel Capability Evidence Audit; do not promote Target Capability

## 0. Round 2 boundary

本轮不重做 Shared Workspace Shell、Main、Universal Conversation、Content Growth identity、Capability Truth 或 Round 1 结论。

本轮只回答：CEO 从经营结果面下钻后，如何查看、干预、继续和返回核心业务对象；专业复杂度如何留在 Deep View；对象之间如何携带 Context。

对象关系是 IA 关系，不新增 Runtime primitive：

```text
Signal / Opportunity → Topic → Research → Content → Variant → Publication → Feedback → Evaluation → Next Work / Topic
       │                 │         │         │        │           │             │          │
       └─ Source         └─ Goal   └─ Evidence└─ Asset └─ Channel/Account       └─ Result  └─ Employee / Work
```

`Signal / Opportunity` 是来源于研究或外部输入的领域投影；不要求新建独立页面。`Result`、`Evidence`、`Work`、`Employee` 继续消费 Curis 既有对象语义。

## 1. Surface 删除 / 合并裁决

| Candidate Surface | 裁决 | 原因 |
|---|---|---|
| Topic Pool | **KEEP · ON-DEMAND** | 完整池解决搜索、历史、暂缓、放弃、恢复、重复识别与用户指定；但 CEO 默认只看推荐子集，不强迫维护。 |
| Topic Detail | **KEEP · 同一 Topic Surface 的详情态** | Topic 的经营判断需要独立 Context、证据、负责人和下一步；不再增加另一套导航。 |
| Research | **KEEP · ON-DEMAND Deep View** | “为什么 / 不同意 / 再查”需要结论、证据、Unknown、Contradiction 和 Research History；不是一级入口。 |
| Source Management | **ON-DEMAND · Research Deep View 内的 Source View** | Source 是 Employee 工具；CEO 主要通过对话表达意图，只有主动进入时才管理。 |
| Content Library + Asset Library | **MERGE** | 用户要找的是“以前做过什么、能否复用、素材在哪、是否发布”。统一 Content Surface 检索 Content 与附属 Asset；Asset 作为抽屉/关系视图，不另造后台。 |
| Content Detail + Editing | **KEEP · 同一 Content Surface 的两种深度** | CEO 默认看推荐成品与建议；直接编辑是按需进入，不默认打开复杂编辑器。 |
| Channel + Publishing | **MERGE · Publishing Target Deep View** | 目标结构必须区分 Channel、Account、Variant、Publication、Receipt，但 CEO 不需要两个后台。当前能力矩阵与目标对象结构并置表达。 |
| Evaluation + Feedback | **MERGE** | Feedback 是 Evaluation 的证据输入与归一结果；CEO 先看 Goal 锚定结论，不先看指标墙。 |
| Employee Current Work | **SHARED SHELL** | 使用 Shared Employee Pattern；Domain 只投影关联 Topic / Research / Content / Publication / Evaluation 与 Handoff。 |

最终用 6 个可理解的结构证明：

1. Topic Pool + Topic Detail
2. Research Result / Evidence + Source Deep View
3. Content Detail / Editing + Asset Drawer
4. Publishing Target Structure
5. Evaluation / Feedback
6. Shared Employee Current Work with Domain Context

## 2. Topic Pool / Topic

### 2.1 CEO View

默认只显示 AI 推荐子集，每项第一眼回答：

- 选题是什么
- 为什么值得做
- 与 Goal 的关系
- 时效与价值
- Risk / Unknown
- 当前 Responsibility / 员工
- 当前状态
- 建议下一步

推荐、候选、调研中、暂缓、已采用、已放弃、历史/重复是 Topic 的状态或筛选语义，不是六个固定 Tab。

### 2.2 Deep View

用户主动进入完整 Topic Pool 后可搜索、筛选、排序、查看历史、暂缓、放弃、恢复、识别重复、合并，批量操作只在存在明确重复劳动时出现。

AI Employee 负责日常发现、去重、状态维护与推荐；CEO 主要查看、干预、指定、恢复历史，不承担池维护。

### 2.3 Actions and entry paths

| 输入 | 进入同一 Topic 模型的方式 |
|---|---|
| AI 推荐 | Opportunity / Signal 被评估后生成 Topic candidate，带来源、理由与 Goal |
| 用户直接说一个选题 | Conversation 解析为 Topic candidate；缺少信息时只追问必要决策 |
| Opportunity 转 Topic | 用户或 Employee 选择“采用为选题”，保留 Opportunity provenance |
| 结果卡 | `查看依据` 进入 Topic Detail；`按建议继续` 创建/继续 Work |

核心动作：`按建议继续`、`先调研`、`直接生成`、`问员工`、`调整`、`暂缓`、`放弃`。`批准`是进入 Content 的决策，不是 Topic Pool 维护动作。

### 2.4 Continue vs new Research

- 同一 Topic、同一经营问题、同一 Scope：继续原 Research Work，保留历史版本与追加证据。
- 研究问题、Scope、目标或 Source Authority 改变：创建新 Research，链接原 Research，不覆盖旧结论。
- 用户说“我不同意”但仍讨论同一问题：进入原 Research 的反驳 / 补查分支；若改变问题，再创建新 Research。

这是 IA 的可解释分流，不是新增 Workflow 页面或固定 Runtime 状态机。

## 3. Research / Evidence / Source

### 3.1 默认顺序

```text
结论 → 为什么 → 意味着什么 → 风险 / Unknown → 建议
```

Evidence、Source、Research Question、Scope、Contradiction、History 通过展开进入，不默认铺成资料库。

### 3.2 Core actions

- `为什么`：展开 Evidence 与 Source provenance。
- `这个结论我不同意`：进入原 Research 的反驳 / 补查入口。
- `再查一下`：同一问题继续原 Research；若改变 Scope，则新 Research。
- `重点看这 3 个网站`：把用户意图交给 Employee；不要求用户打开设置。
- `只用官方来源重新查`：创建带 Source Constraint 的新 Research，链接原结论并显示差异。

### 3.3 Source

Source 默认是 Employee 工具。Conversation 是主要入口：

> “以后重点看这个网站。”

Employee 自己完成添加、暂停、恢复、来源约束与失效处理，并将变更结果回到经营结果或 Research Context。

主动进入 Source Deep View 时支持：添加、批量添加、暂停、恢复、删除/归档、来源类型、可信度、最近采集、使用中的 Research、失效/授权状态。它不是 CEO 默认后台入口。

## 4. Content / Draft / Version / Asset

### 4.1 Object semantics

| 对象 | IA 含义 | 不是 |
|---|---|---|
| Content | 一个内容工作成果及其经营上下文，关联 Topic / Research / Goal | 不是每个平台各复制一份独立内容 |
| Draft | Content 当前可编辑的生命周期表示 | 不是新的 Runtime primitive |
| Version | Content 的可恢复修订记录 | 不是默认需要 CEO 管理的版本库 |
| Recommended Version | 当前建议 CEO 采用的 Version 关系 | 不是新的 Content |
| Asset | Content 使用或可复用的图片、视频、引用等素材对象 | 不是必须独立进入的素材后台 |

### 4.2 CEO View → Deep View

默认看到：推荐成品、为什么这样做、当前素材、必要风险、建议下一步。

按需进入：直接编辑、对话修改、再来一版、恢复上一版、查看历史版本、替换/生成/上传/选择历史素材、审核问题、准备发布。

“直接说话修改”默认产生新 Version 并保留上一版；`恢复上一版` 改变 Recommended Version 指针，不销毁历史。Asset Drawer 只解决找素材、预览、替换和复用，不生成第二个 Library Surface。

## 5. Channel / Account / Variant / Publication / Receipt

### 5.1 Target Product Structure

```text
Content → Channel → Account → Variant → Publication → Receipt
```

- Channel：平台对象。
- Account：平台内账号及 Account Positioning；目标结构存在，当前 Multi-account `UNAVAILABLE`。
- Variant：针对 Channel / Account / 地区 / 语言 / 格式 / 规则的内容变体。
- Publication：一次目标发布记录与其状态。
- Receipt：平台回执、URL 或人工回执 provenance。

CEO 默认不管理矩阵。Employee 推荐“发哪里、哪个账号、什么时候、为什么”；CEO 确认、调整或讨论；Target Deep View 才展开具体对象关系。

### 5.2 Current Capability Truth

当前五平台没有任何 audited `VERIFIED` capability。IA 只按 Audit 消费：

- Auth：五平台 `PARTIAL`，不等于 OAuth 或账号归属已验证。
- Publish：五平台 `CONDITIONAL`，没有 live publication evidence，不显示为默认可用。
- XHS Schedule / Publication Status / Receipt / Comments：`PARTIAL`，内部或人工未验证。
- XHS Analytics：`UNAVAILABLE`。
- 其他平台多数 Schedule / Status / Analytics / Comments：`UNKNOWN`。
- Multi-account：`UNAVAILABLE`。

必须能表达：等待能力、未授权、UNKNOWN、人工未验证回执、失败、部分能力存在。任何 Target Publish 流程都标记 `TARGET SCENARIO / NOT CURRENT CAPABILITY`。

## 6. Evaluation / Feedback

Evaluation Surface 默认顺序：

```text
结果是什么 → 为什么 → 与 Goal 的关系 → 什么有效 → 什么没证明 → 下一步建议
```

Feedback 是输入与证据：Content、Topic、Channel、时间、Metric、评论或人工记录，并保留 source / freshness / unknown provenance。Employee 先归一反馈，只有值得 CEO 关注的结论才投影回经营结果。

Deep View 才展开 Content、Topic、Channel、时间、Metric、Feedback、Evidence。Evaluation 的“按建议继续”进入 Next Work 或下一 Topic，不自动把平台指标当作 Business Value。

带货、品牌、个人 IP 的归因不足时，显示 `UNKNOWN / Attribution not proven`，不能把浏览、点赞、粉丝直接写成 Business Value。

## 7. Employee Current Work

Employee Current Work 不是任务列表，而是 Shared Shell 的 Work Area 投影：

- 当前在做什么、为什么做
- 关联 Topic / Research / Content / Publication / Evaluation
- 当前进展、已有 Result、Evidence、下一步
- 等待谁 / 是否等待 CEO
- Handoff 与返回对象

三入口不变：直接对话、当前工作、员工资料。对象进入员工对话时携带 `Workspace + Responsibility + 当前对象 + Result / Evidence refs`；用户不重述背景。Employee 完成后回写原对象并可回到经营结果。

## 8. Cross-object context contract

| 进入 | 自动携带 | 返回 |
|---|---|---|
| Result → Topic | Result、Goal、Topic refs、当前建议 | 原经营结果位置 |
| Topic → Research | Topic、Goal、Research Question、Source constraints | Topic Detail |
| Research → Content | Conclusion、Evidence、Risk / Unknown、Topic | Research Result / 经营结果 |
| Content → Publishing | Content、Recommended Version、Asset refs、目标策略 | Content Detail |
| Evaluation → Topic | Evaluation conclusion、Goal、next recommendation、Topic refs | Evaluation / 经营结果 |
| Object → Employee Conversation | Workspace、Responsibility、对象、Result、Evidence refs | 原对象 |
| Employee Current Work → Object | Work、Handoff、Result、Evidence、对象 refs | Current Work / 经营结果 |

任何返回都保留原对象、原 Result 与当前滚动位置语义；不得要求 CEO 再解释“刚才是哪个选题”。

## 9. Low-fidelity acceptance paths

### A. 推荐选题 → Research → Content

经营结果推荐 Topic → 查看理由 → 按建议继续 / 先调研 → Research 结论 → “我不同意”或“只用官方来源再查” → 补查结果 → CEO 批准 → 进入 Content。

### B. 推荐成品 → 修改 → Asset → Publishing

推荐 Content → 一句话修改 → 新 Version → 恢复上一版 → 打开 Asset Drawer / 替换素材 → 准备发布 → Target Publishing 结构与 Current Capability Truth。

### C. Conversation → Source

用户说“以后重点看这个网站” → Employee 接受 Source 意图 → Employee 管理 Source → 返回确认结果；不进入设置页。

### D. Deep capability

用户主动进入完整 Topic Pool 或 Source Deep View 时，可以搜索、筛选、历史、暂停、恢复、归档；这些能力不出现在默认 CEO View。

### E. Evaluation

用户问“最近效果怎么样？” → 先看 Evaluation 经营结论 → 再展开 Feedback / Evidence / Metric → 按建议进入 Next Work 或 Topic；不先显示 Dashboard。

### F. Object → Employee

任意对象点击“问负责员工” → 直接打开带 Context 的 Conversation → 员工继续原 Work / 返回 Result → 回到原对象。

### G. Capability shortage

当前能力不足时，UI 同时显示清楚的 Current Truth 与 Target Structure；Target 不得触发假成功、假 URL 或假 Analytics。

## 10. Round 2 non-goals

- 不冻结六个 Topic 状态为六个 Tab。
- 不增加 Topic、Research、Source、Asset、Publishing、Evaluation 的后台一级导航。
- 不新增 Runtime primitive、Workflow、Agent、执行状态机或成本阈值。
- 不把 Current Capability 未验证的多账号、真实发布、回执、Analytics、Comments 画成已完成能力。
- 不把 Employee 示例团队写成固定 Headcount。

