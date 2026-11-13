# CURIS FIRST-RUN AND BUSINESS ENTRY MODEL

> Status: Review
> Authority Class: REVIEW / PRODUCT MODEL
> Scope: 任意业务创建、General Business Workspace、Professional Template 与首次使用入口
> Disposition: 本文件只澄清产品入口语义，不新增 Authority、页面设计或实现合同。

## 1. 产品结论先行

### A. Curis 是否允许创建任意业务？

**是。** Curis 首先是一家可以承载和经营任意个人业务的 AI 公司。用户可以说“我要开始做跨境电商”“我要经营一家宠物用品品牌”“我想做一个教育产品”，即使 Curis 还没有对应的专业业务模板，也应该能创建自己的 Business 和 Workspace 并开始工作。

### B. 没有 Professional Template 是否仍然可以工作？

**可以。** 没有模板时使用 General Business Workspace。它复用 Curis 的共享公司能力：目标、团队、责任、对话、当前工作、Result、Evidence、Artifact、Decision、Handoff、History、Evaluation、Capability / Tool、Context 和 Four-Pane。

General Workspace 不是空白聊天框。AI Team 仍能理解目标、研究情况、制定计划、讨论、调用已有能力、产出结果、交接、复盘和继续下一轮。它只是没有某个专业领域预先定义好的对象、视图、方法和评估结构。

### C. Professional Template 增加什么价值？

专业模板把 Curis 在某类成熟业务中已经整理好的能力带进 Workspace：专业对象、常见工作方法、业务视图、动作、结果表达、评估边界和可按需展开的深度能力。

因此：

```text
General Workspace       = 能够经营任意业务
Professional Workspace  = 在某类业务上经营得更专业、更高效、更结构化
```

专业模板降低专业起步成本，但不决定用户能不能开始业务。

### D. 第一次打开 Curis 是否知道该做什么？

**应该知道。** 第一入口只需让用户理解两件事：可以直接告诉 Curis 想做什么，也可以查看 Curis 已准备好的专业业务能力。最自然的主语义是：

> **开始一个业务**

这个入口同时容纳“直接说目标”和“使用专业业务能力”，而不是先把用户送进模板目录。

### E. 模板是否容易发现但不强迫选择？

**是。** 模板应该在“开始一个业务”中被推荐，也应在用户之后新增业务时继续可发现；但用户不必先选模板。匹配不到模板时继续创建 General Business Workspace，不能出现“没有模板所以无法创建”。

### F. Curis 是否仍然是 AI Company，而不是模板 SaaS 集合？

**是。** 模板是帮助公司更快拥有专业能力的资产，不是 Curis 的产品中心。Company、Business、Workspace、Team、Employee、Responsibility、Work、Result 和 Decision 才构成持续经营关系；模板不能取代这些关系。

## 2. 第一次打开 Curis：最小产品入口

新用户没有 Business、Workspace 或 Employee operating history。第一入口应让他立刻明白：

1. Curis 可以帮我经营一项业务；
2. 我可以用自己的话直接开始；
3. Curis 也准备了一些成熟业务能力，可以帮助我更快开始。

### 主入口：开始一个业务

入口的用户语言应接近：

> **你想开始做什么？**

用户可以直接输入：

- “我想做 AI 科技内容。”
- “我要开发一个 App。”
- “我要开始做跨境电商。”
- “帮我经营个人品牌。”

同一个入口根据意图判断：

- 有匹配的 Professional Template：推荐“使用内容增长专业能力开始”，说明它能带来什么帮助；
- 没有匹配的 Template：说明“可以先用通用业务工作空间开始”，不阻断创建；
- 用户不想判断：由 Curis 推荐一个起点，但不替用户决定他的 Business identity。

### 同一入口中的第二路径：查看专业业务能力

在“开始一个业务”中，用户也可以看到少量 Curis 已准备好的专业业务能力，例如：

- 内容增长；
- 软件研发；
- 未来可能增加视频制作、电商、销售等。

这里的心智不是 App Store、插件市场、工具货架或模板商城，而是：

> **Curis 已准备好的专业业务**

它让用户知道“我可以直接从成熟能力开始”，但仍然保留直接表达目标的主路径。

## 3. 官方 Template、Business、Workspace 的关系

这三个概念必须分开：

| 概念 | 普通用户理解 | 产品作用 |
|---|---|---|
| Business | 我要经营的业务 | 用户自己的业务身份、方向、目标与结果归属 |
| Workspace | 这项业务真正工作的地方 | 承载目标、团队、责任、工作、结果和专业内容 |
| Professional Template | Curis 已准备好的某类业务能力 | 帮助初始化某个 Workspace 的专业结构，不是身份 |

例子：

```text
Business：我的个人品牌
Workspace：AI 科技内容增长
Template：内容增长
```

用户选择“内容增长”不是创建一个叫“内容增长”的固定 Business，而是使用 Content Growth Professional Template 初始化自己的 Workspace。同一个 Template 可以服务不同用户、不同 Business 和不同 Workspace instance。

Template 不能成为 Business 的上级，也不能取代 Workspace。没有 Template 时，Business 仍可拥有 General Workspace。

## 4. Path A：直接告诉 Curis 我要做什么

### 用户输入

> “我要做一个宠物用品品牌，先卖给养猫的人，以后再扩大。”

用户不必先填写受众表、渠道表、Team、Workflow、Source 或专业参数。Curis 先理解：这是一项要经营的业务，目标、受众、时间和商业计划仍可能不完整。

### Curis 的回应

Curis 应该：

1. 确认正在帮助用户开始一项新业务；
2. 说明是否发现匹配的 Professional Template；
3. 有匹配时给出“推荐使用”与“先用通用工作空间”的清楚选择；
4. 无匹配时直接继续创建 General Business Workspace；
5. 只追问开始经营所必需的目标、限制或高影响决定；
6. 让 AI Team 补充研究、提案、责任和第一步工作。

这里的关键不是自动生成一套宠物电商软件，而是让这家公司先能够经营：有目标、有责任、有工作、有结果，并能随着业务成熟再增加专业能力。

### General Workspace 起点

第一次进入 General Workspace，用户至少应能理解：

- 这是什么业务；
- 当前目标或初始 Proposal 是什么；
- AI Team / Responsibility 谁在处理什么；
- 当前正在进行的 Work；
- 最近或第一个重要 Result / Artifact；
- 哪些需要 CEO 决定，哪些仍然 Unknown；
- 从哪里继续 Conversation、查看 Evidence、进入 History 或开始下一 Work。

它不应退化成“几个员工 + 一个聊天框”，也不应假装拥有不存在的宠物电商专业页面。专业能力缺口应透明表达，已有通用能力仍然可用。

## 5. Path B：使用 Curis 已准备好的专业业务

### 用户选择 Content Growth

用户可以从“开始一个业务”看到“内容增长”并选择它。此时用户不是加入 Curis 的固定内容公司，也不是创建一个模板身份，而是用专业能力初始化自己的 Workspace。

### 用户最少提供什么

最小输入是：

- **Intent**：想做什么、希望达到什么结果；
- **Reference（可选）**：喜欢的账号、文章、风格或链接；
- **Constraint（必要时）**：不能做什么、必须遵守什么、哪些风险要避免。

例如：

> “我想做 AI 科技内容，先涨粉，以后接广告。”
>
> 可选：“我喜欢这个账号。”

不要求用户先填写 Audience、Channel、Source、Workflow 或 Employee 配置表。

### AI Team 补什么

AI Team 负责把不完整意图转成一个可经营的起点：理解目标、发现机会、推荐 Topic、规划 Research、配置和使用必要 Source、生成 Content、保留 Version / Asset、提出 Publishing 建议、收集 Feedback、做 Evaluation，并把需要 CEO 的决定明确提出。

它不应擅自决定 Goal、受保护的定位、重大预算、不可逆外部承诺或未知商业归因。平台连接、账号和真实发布能力不足时，要如实说明等待、未授权、Unknown、人工未验证或不可用。

### 什么时候进入 Workspace

当用户确认业务目标或接受一个可工作的初始提案后，Curis 进入该用户自己的 Content Growth Workspace。模板提供专业能力，Business / Workspace 仍属于用户自己的公司关系。

### 第一次进入 Content Growth Workspace

第一眼不应只有员工列表、工作状态和对话。用户应该感受到自己进入了一个真正的内容增长产品：

- 当前经营目标和最值得关注的 Result；
- 推荐 Topic，以及为什么值得做；
- Research 结论、风险和 Unknown；
- 推荐 Content / Version 与下一步；
- AI Team 正在做什么、何时需要 CEO；
- 内容、素材、渠道、发布准备、反馈和评估确实存在，但不把完整后台一次铺开。

专业对象仍可按需深入：Topic Pool、Source、Evidence、Contradiction、History、Editor、Version、Asset、Channel、Account、Variant、Publication、Receipt、Metric、Feedback 和 Attribution。小白先看结果，专业用户进入 Deep View；Simple by default 不等于 Capability missing。

## 6. 已经在使用 Curis：新增业务的长期入口

用户已经有“AI 科技内容增长”“产品研发”和“个人项目”后，再说：

> “我还想做视频业务。”

长期稳定的主入口应是 Company 级的：

> **新增业务** / **开始一个业务**

它应位于用户理解为“我的公司现在有哪些业务、我要再开始什么”的 Company / Business 入口，而不是设置，也不应只藏在某个 Workspace 内。进入后仍使用同一个开始流程：直接输入目标，同时推荐匹配的 Professional Template。

### Business 与 Workspace 的选择

- 如果是一个新的经营方向，例如“视频制作业务”：创建新的 Business，并初始化一个 General 或 Professional Workspace；
- 如果是在已有 Business 下增加一个实际工作单元，例如同一品牌的第二个市场：在该 Business 中创建新的 Workspace；
- 如果用户不确定：让 Curis 根据意图解释“新业务”与“已有业务下的新工作空间”的区别，必要时再让 CEO 决定；
- Workspace switcher 可以提供“新增工作空间”快捷入口，但不应成为模板发现的唯一入口，也不应把模板当成 Workspace identity。

因此入口优先级是：

| 级别 | 入口 | 结论 |
|---|---|---|
| PRIMARY ENTRY | Company / Business 的“开始一个业务” | 同时支持直接表达目标和专业能力推荐 |
| SECONDARY ENTRY | 已有 Workspace / Business 中的“新增业务 / 新增工作空间” | 保持上下文，适合复用已有 Business |
| NOT RECOMMENDED | 独立模板中心、模板商城、设置里的模板入口 | 会把 Curis 误解成模板 SaaS / 工具市场 |

## 7. 多业务 Company 级信息优先级

用户打开已有公司时，Company 级别首先帮助他回答：

1. 我现在有哪些 Business / Workspace；
2. 哪些正在正常工作，哪些有重要变化；
3. 哪些需要我做决定、授权、恢复或接管；
4. 最近有什么重要 Result、Risk 或 Unknown；
5. 如何进入某个 Workspace；
6. 如何开始新的 Business / Workspace。

这不是 Workspace 卡片墙、Dashboard 或项目列表。它是公司的经营入口：突出少量重要事项，提供进入真实 Workspace 的路径，把不需要 CEO 处理的工作保持安静。

## 8. 小白与专业用户的双层体验

### Professional Workspace

小白路径是：

```text
表达目标 → AI Team 工作 → 看到 Result / Risk / Unknown → 做 Relevant Decision
```

专业用户路径是：

```text
结果面 → Domain Object → Deep View → 修改 / 指定 / 查看 Evidence → 返回原对象
```

两者使用同一个 Workspace 和同一套业务事实。不同之处是披露深度，不是两套产品。

### General Workspace

小白通过 Conversation + Result 经营，不需要先学习专业系统。专业用户可以深入 Current Work、Artifact、Evidence、Tool、History、责任和决定；但如果某个行业专业 UI 尚不存在，产品不应假装它存在。通用 Workspace 的价值是“真实可经营”，而不是“视觉上像某个行业软件”。

## 9. Four-Pane 在首次入口中的位置

首次入口不需要先向用户解释 Four-Pane，但产品应使用同一个共享空间框架：

- **Navigation**：我在哪里，去公司、业务或工作空间；
- **Context**：我正在开始或处理哪项业务、目标和当前背景；
- **Main**：我真正要做的核心工作或看到的经营结果；
- **Utility**：按需提供来源、证据、预览、设置、版本或其他辅助能力。

第一次简单状态主要显示 Navigation + Main。Context / Utility 在需要时出现或收起，不把首次使用变成配置后台。选择模板、开始 General Workspace、查看 Result 和问负责员工，都应留在同一共享产品关系中。

## 10. 完整示例一：匹配专业模板

```text
新用户第一次打开 Curis
→ 输入：“我想做 AI 科技内容，先涨粉，以后接广告。”
→ Curis 识别到 Content Growth Professional Template
→ 用普通话说明：这个专业能力可以帮助你做选题、研究、内容和评估
→ 用户确认目标，可选提供喜欢的账号链接
→ AI Team 理解目标、形成初始建议并开始第一项工作
→ 进入用户自己的 Content Growth Workspace
→ 用户先看到经营目标、当前重点和员工正在做什么
→ 出现第一个 Research / Topic / Content Result
→ 用户查看依据、问负责员工或做必要决定
→ 继续内容、发布准备、反馈、评估和下一轮经营
```

这里 Template 帮助专业化，但 Business identity 和 Workspace identity 属于用户，不属于模板。

## 11. 完整示例二：没有专业模板

```text
用户第一次打开 Curis
→ 输入：“我要做宠物用品品牌。”
→ Curis 没有匹配的宠物用品 Professional Template
→ 说明：可以先用通用业务工作空间开始，不需要等待模板
→ 建立用户自己的 Business 与 General Business Workspace
→ AI Team 理解目标、研究市场、提出初始经营建议
→ 用户看到目标、Proposal、责任、Current Work 和第一个 Result
→ 用户可以继续 Conversation、查看 Evidence、做 Decision、保留 History
→ 业务成熟后，未来可接入新的专业能力，但当前经营不中断
```

这里没有“无法创建”，也没有“自动生成一套完美宠物电商 SaaS”。Curis 首先让业务真实运转，再在有依据时增加专业化。

## 12. 最终模型

```text
任何用户意图
→ 创建 / 选择自己的 Business
→ 创建自己的 Workspace
→ 若有匹配：推荐 Professional Template
→ 若无匹配：使用 General Business Workspace
→ AI Team 组织责任、工作、结果和依据
→ CEO 处理目标、边界、风险和重要决定
→ 业务继续经营并逐步获得更多专业能力
```

模板是加速器，不是门槛；General Workspace 是可经营的真实起点，不是失败状态；Professional Workspace 是在成熟业务上的更深产品能力，不是 Curis 唯一的业务形式。

## FINAL DECISION

# PRODUCT ENTRY MODEL COHERENT

Curis 仍然允许创建任意业务；没有 Professional Template 仍然可以工作；Professional Template 提供专业效率和结构化深度；首次打开可以同时提供“直接告诉 Curis”和“使用 Curis 已准备好的专业业务”两条路径；模板容易发现但不强迫选择；Curis 仍然是 AI Company，而不是模板 SaaS 集合。

**STOP FOR CEO REVIEW.**
