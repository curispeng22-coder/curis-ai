# CURIS SHARED VISUAL FRAMEWORK + CONTENT GROWTH FIGMA CONTRACT

> Status: Review  
> Authority Class: REVIEW  
> Scope: IA → Visual Product Translation  
> Decision: **READY FOR FIGMA VISUAL DESIGN**

## 1. CURIS SHARED FRAMEWORK

Figma 的对象是 **Curis 整体产品 + Content Growth 第一套 Professional Workspace 实例**，不是孤立的内容运营后台。

### Shared product contract

- `Workspace` 是唯一 canonical user/product identity；Business、Workspace、Channel 不混用。
- `Main = Domain Business Surface + Shared Work Area`；Main 必须在 Context / Utility 关闭时仍能独立表达当前业务。
- Four-Pane 是职责模型，不是四根永久物理栏：Navigation、Context、Main、Utility；Context / Utility 是 Adaptive Surface。
- Universal Conversation、Employee Workstation、Composer、Result / Artifact、Handoff、Evidence、Quick Path 是 Shared Company Patterns，不能由 Domain 重造。
- 进入具体 Employee 后，Main 使用统一的 Conversation-first Employee Workstation：自然对话、工作状态、Tool / Action 状态、Result / Artifact、Composer。
- Employee 三入口保持：直接对话、当前工作、员工资料；Conversation 不进入 Context，也不塞进 Employee Detail。
- Context 跨对象 / 对话连续，但只携带本次 bounded context；不自动注入完整员工历史或全部 Knowledge。
- Responsibility ≠ Employee；Headcount、Assignment、真实能力不由视觉稿冻结。
- CEO 不配置 Workflow、Agent 或专业参数；Quick Path 不被 Domain Workflow 污染。

### Shared visual mother language

统一表达层级：

```text
PRIMARY FOCUS      当前最重要的 Result / Decision / Action
SECONDARY CONTEXT  谁负责、为什么重要、下一步
SUPPORTING DETAIL  Context / Work / Risk / Unknown
DEEP EVIDENCE      Evidence / Source / History / Technical detail
QUIET BACKGROUND   无需 CEO 处理的运行状态
```

统一研究维度：Global / Workspace hierarchy、Shell density、content rhythm、typography、accent、selected / active / focus、Employee presence、Conversation、Result、Decision、Context reveal、Deep-view transition、Quiet、Error / Unknown、Capability unavailable、Shared object header、Composer、action hierarchy。

## 2. FOUR-PANE PRODUCT FRAMEWORK

### CEO TERMINOLOGY CORRECTION

本任务语境中的“Curis 四范式”即 **Curis Four-Pane Product Framework**：

```text
Navigation | Context | Main | Utility
```

它不是四种工作模式、四种 Conversation，也不是四种 Workspace 类型。四区职责稳定，但不要求四区永久同时展开；Context / Utility 是 Adaptive / Collapsible Surface。

### Four-Pane translation

| 区域 | 稳定职责 | Figma 状态表达 |
|---|---|---|
| Navigation | 全局 / 产品导航区域 | 默认保留，表达“我在哪里” |
| Context | Main 左侧按需上下文：Workspace、当前对象、Work、决策支撑 | 默认可收起；需要上下文时展开 |
| Main | 核心工作主区域；当前 selected Professional Surface + Shared Work Area | 始终保持 Primary Focus |
| Utility | Main 右侧按需辅助：Artifact、Evidence、Tool、Action、Detail / Editor | 默认可收起；当前对象需要时展开 |

### Adaptive states of the same framework

- **Default / simple state**：Navigation + Main 是主要可见结构；Context / Utility 收起。
- **Context-needed state**：展开 Context，承载当前对象、Workspace、Work 等必要上下文；不承载 Employee Conversation。
- **Utility-needed state**：展开 Utility，承载当前工作需要的辅助能力；不取代 Main 的 Primary Focus。
- **Deep working state**：Context / Main / Utility 可以共同工作，但 Main 始终保持 Primary Focus，辅助区不升级为第二个主工作区。

这些是同一 Four-Pane Framework 的自适应状态，不是四套视觉系统或四种独立产品范式。

### Shared patterns inside Four-Pane

- Universal Conversation、Meeting Conversation、Workspace Thread 与 Employee Workstation Conversation 各自有清晰归属，不形成中央群聊。
- 进入具体 Employee 后，Main 使用统一的 Conversation-first Employee Workstation；Domain 只改变周边专业对象、Tool、Artifact、Context 和 Utility。

## 3. CONTENT GROWTH INSTANCE

Content Growth 只向 Shared Framework 提供：

- 默认 selected Surface：经营结果 / Domain Result projection。
- Domain objects：Topic、Research、Source、Content、Version、Asset、Channel、Account、Variant、Publication、Receipt、Evaluation、Feedback。
- Domain Result projection、Domain actions、Domain Context。

消费已接受 IA：

```text
Signal / Opportunity → Topic → Research → Content → Variant → Publication
       → Feedback → Evaluation → Next Work / Topic
```

视觉翻译：

| 对象 | Primary focus | 默认隐藏 / 按需展开 |
|---|---|---|
| 经营结果 | 当前最值得关注的 Result / Decision / Action | 运行细节、完整对象池、技术状态 |
| Topic | 选题、为什么值得做、Goal 关系、建议 | 完整 Pool、历史、重复、合并 |
| Research | 结论、意味着什么、建议 | Evidence、Source、Contradiction、History |
| Content | 推荐成品、必要风险、下一步 | Editor、Version、审核、Asset |
| Publishing | Employee 推荐方案与原因 | Channel / Account / Variant / Publication / Receipt 细节 |
| Evaluation | 经营结论、Goal 关系、下一步 | Metric、Feedback、Evidence、归因细节 |
| Employee Current Work | 在做什么、为什么、Result、下一步、是否等待 CEO | 完整 Work trace / 内部运行细节 |

## 4. LOCKED

- Workspace identity、Business / Workspace / Channel hierarchy。
- Shared Shell、Main 合同、Universal Conversation、Employee Pattern、Employee 三入口。
- Context 连续性；Result → Evidence / 问员工 / 按建议继续。
- Surface 不拥有独立 Runtime / Work / Team / Result Truth。
- Content Growth 不新增 Shell、Conversation、Employee system、Work system 或 Runtime truth。
- Topic Pool = ON-DEMAND；Research = 结论优先；Source = Employee tool / Deep View。
- Content + Asset 合并表达；Version / Recommended Version 关系保持。
- Channel + Publishing 合并为 Target Object Structure；Evaluation + Feedback 合并。
- Responsibility ≠ Employee；Headcount 不冻结。
- 现有 IA HTML 只可作 `STRUCTURAL REFERENCE ONLY — VISUAL NOT ACCEPTED`。

## 5. VISUAL GOAL

让 CEO 首先感到：一家 AI 公司正在替我经营；其次才看到专业信息。视觉应简洁但不寡淡、信息丰富但有单一焦点、专业深度按需出现。

禁止把产品视觉做成 Dashboard、文件库、Agent 控制台、Task Manager、CMS 编辑器或 SaaS 后台。

## 6. MUST SHOW

- 当前 Workspace identity 与当前责任范围。
- 一个明确的 Primary Focus。
- Result / Decision / Action 的价值、风险或 Unknown、下一步。
- 负责 Responsibility 与 Employee presence；进入员工后使用 Shared Workstation。
- 当前对象 Context 的轻量入口，以及可返回原对象的锚点。
- Conversation 的自然入口与共享 Composer 语义槽位。
- Deep View 的进入 / 返回、Evidence / Source / History 的渐进展开。
- Error、Unknown、等待、失败恢复、Capability unavailable 的诚实状态。
- Content Growth 的 Target 与 Current Capability 分离。

## 7. DEFAULT HIDDEN

- 完整 Topic Pool、Source 管理、Research Evidence 资料库、版本历史、Asset 选择器。
- Channel / Account / Variant / Publication / Receipt 矩阵。
- Metric、Feedback 原始流、归因细节、技术诊断。
- Workflow、Agent、Retry、Timeout、Cost、State Machine、Execution Graph。
- 不影响当前决策的 Work trace、内部状态和专业参数。

## 8. FIGMA FREE

Figma 可自由决定：layout、grid、spacing、typography、density、surface treatment、focus、component geometry、progressive disclosure、transition、motion idea、accent / color strategy。

但所有自由只发生在 Locked Structure 之内，并使用 Frozen visual tokens；不得把当前 IA HTML 的卡片、灰白配色、badge、bottom nav、spacing 或 typography 当作视觉答案。

## 9. FORBIDDEN

- 不新增一级 Domain 导航、第二套 Shell、Conversation、Employee、Work、Result 或 Runtime。
- 不把 Four-Pane 画成永久四栏。
- 不把 Employee 放进 Context Sidebar；不把 Conversation 放进 Employee Detail / Utility。
- 不把 8 States / 4 Buckets、固定卡片数量或固定阈值画成系统合同。
- 不把示例员工画成冻结 Headcount。
- 不把 Target Capability 画成 Current Capability。
- 不伪造 Connected account、Live Publish、Published URL、Live Analytics、Live Comments、Multi-account。
- 不把 Topic / Research / Source / Asset / Publishing / Evaluation 各自扩成后台页面墙。
- 不直接把 Topic、Research、Evidence、Publication、Variant 等内部术语当作小白用户主语言。

## 10. CURRENT TRUTH

Figma 必须消费以下 Current Capability Truth：

- 五个平台没有任何 audited `VERIFIED` capability。
- Auth：`PARTIAL`，不等于平台 OAuth 或账号归属已验证。
- Publish：`CONDITIONAL`，无 live publication evidence。
- XHS Schedule / Publication Status / Receipt / Comments：`PARTIAL`，内部或人工未验证。
- XHS Analytics：`UNAVAILABLE`。
- 其他平台多数 Schedule / Status / Analytics / Comments：`UNKNOWN`。
- Multi-account：`UNAVAILABLE`。

视觉状态应表达：未连接 / 未授权 / Unknown / 等待能力 / 人工未验证 / 失败 / 部分能力存在；不得显示假成功。

## 11. TARGET ONLY

以下可以作为虚线、Future、Target Scenario 展示，但不得冒充当前能力：

```text
Content → Channel → Account → Variant → Publication → Receipt
```

包括账号定位、跨渠道 Variant、真实发布、平台回执 / URL、Analytics、Comments、Multi-account、Employee 推荐发布矩阵。所有相关 Frame 必须显式标记：`TARGET SCENARIO / NOT CURRENT CAPABILITY`。

## 12. FIRST-PASS FRAME LIST

### GROUP A — CURIS SHARED FRAMEWORK

1. Curis Four-Pane Shell · Default（Navigation + Main；Context / Utility 收起）
2. Four-Pane · Context Expanded
3. Four-Pane · Utility Expanded
4. Universal Conversation / Shared Composer
5. Employee Conversation-first Workstation

### GROUP B — CONTENT GROWTH INSTANCE

1. Content Growth · 经营结果
2. Topic / Research · 结果优先下钻
3. Content · 推荐成品 + 按需修改
4. Evaluation · 经营结论
5. Publishing · Current Capability Truth / Target Structure
6. Source / Topic Pool Deep View（如需要）

## Final decision

# READY FOR FIGMA VISUAL DESIGN

Four-Pane Product Framework 的术语与自适应状态已按 CEO 纠正完成；没有因此产生新的产品结构 Blocker。Figma 可从完整 Curis Four-Pane Framework 开始，并将 Content Growth 的全部 Frame 装入同一视觉母体。

**STOP FOR CEO REVIEW.**
