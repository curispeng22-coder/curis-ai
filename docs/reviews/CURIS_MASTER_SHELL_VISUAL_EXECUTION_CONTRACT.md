# CURIS MASTER SHELL — VISUAL EXECUTION CONTRACT

> Status: Review
> Authority Class: REVIEW / DESIGN INPUT
> Scope: Trae 临时 Visual Designer qualification test
> Disposition: Contract only · no design · no implementation

## 1. Purpose

Trae 只执行已确认的 **Curis Desktop Master Shell** 视觉设计，不重新理解 Curis、不重新决定产品结构、不修改 Product Truth / UI Blueprint / Frozen Shell，也不顺便设计业务页面。

## 2. Source of Truth

**Trae qualification core reading set is exactly two files:** this contract and `docs/03_Design/CURIS_TRAE_VISUAL_DESIGN_RULES.md`. The upstream files below are authority provenance for the Product / Design owner; Trae does not need to reconstruct them or read historical exploration.

按以下顺序消费：

1. `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md`
2. `docs/01_Product/Curis_Product_Blueprint.html`
3. `docs/01_Product/Curis_Product_Master_Map.md`
4. `docs/01_Product/Curis_Product_UI_Blueprint.html`
5. `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`
6. `docs/03_Design/Curis_Company_OS_Shared_Authority.md`
7. `docs/reviews/CURIS_V1_UI_FRONTEND_RECONCILIATION_AUDIT.md`
8. `docs/reviews/CURIS_V1_CURRENT_UI_FOUNDATION.md`
9. `docs/reviews/CURIS_V1_UI_GAP_MAP.md`

旧 Prototype / Flow Pack / Figma exploration 只可作 reference，不是 Current UI authority。若发现 Current Authority 冲突，停止并报告，不自行取舍。

## 3. Locked product structure

### Navigation

固定七区，顺序不可变：

1. CEO 工作台
2. 业务空间
3. 组织中心
4. 人才与能力
5. 经营洞察
6. 资料库
7. 会议

搜索、最近工作、通知/待处理、CEO Assistant 是 **Global Capability**，不是第八个一级区，也不等于 Global Topbar。七项可以有视觉层次，但不得隐藏到“更多”或改回旧五/六区。

### Four-Pane responsibility model

`Navigation | Context | Main | Utility` 是职责模型，不是四根永久等权栏：

- Navigation：稳定的公司导航。
- Context：Main 左侧，自适应、可折叠，按需提供业务上下文。
- Main：绝对 Primary Focus；Context / Utility 关闭后仍独立成立。
- Utility：Main 右侧，自适应、可折叠，承载详情、编辑、证据或工具。

每个 Pane 使用自己的 Pane-local Header。禁止一个横跨全 App 的 Global Topbar。

### Main contract

`Main = selected Professional Surface + Shared Work Area`。

本次资格测试不设计任何 Professional Workspace，只用中性 fixture 证明：Main 有清晰主焦点，Shared Work Area 可以存在，Employee Workstation 不吞掉 Main，Context / Utility 打开后 Main 仍是主体。

### Employee / Conversation

只证明共享 presence。Employee 不是页面主体，Conversation 不是卡片墙，Composer 只消费 Shared Composer Pattern。禁止三个员工并排成为 Main、Employee roster 冒充 Workspace、Conversation 承担全部产品语义。

## 4. Visual direction

目标是“简洁但不寡淡、克制但有焦点、信息丰富但不平均用力”：第一眼知道 Primary Focus，感觉像一家安静、专业、正在工作的 AI 公司，而不是 SaaS Admin、Dashboard、Agent Console、Task Manager、文件库、IDE、Notion Clone 或 Card Wall。

明确四级层次：

- **PRIMARY**：当前最重要的工作 / 结果 / 对象。
- **SECONDARY**：责任、上下文、下一步。
- **TERTIARY**：状态和辅助信息。
- **QUIET**：无需 CEO 处理的运行状态。

消费当前 Frozen Visual Standard `CURIS_VISUAL_STANDARD_V1.md` 与其 Neutral Foundation / theme 规则。Primary Brand Accent 固定为 `#806BE5`；`#32f08c` 是 Legacy Implementation Token，不得作为当前品牌 accent。实现迁移不在本合同执行。禁止全灰白无焦点、高饱和 Dashboard、泛滥渐变和发光 AI 界面。

Curis 需要完整业务产品的合理信息密度；用层级、留白、字体和渐进披露控制复杂度，不得靠删除业务信息伪造“简洁”。

## 5. Qualification output

一次输出 **Direction A / Direction B / Direction C**。三者必须有真实差异：spatial rhythm、typography、density、surface treatment、hierarchy、navigation treatment、pane relationship；不能只是换颜色。产品结构必须完全相同。

每个方向必须展示同一 Shell 的三个状态：

1. **Default**：Navigation + Main；Context、Utility 收起。
2. **Context Expanded**：Navigation + Context + Main；Utility 收起。
3. **Deep Work**：Navigation + Context + Main + Utility；Main 仍保持 Primary Focus。

不要为三个状态设计三套产品。

## 6. Neutral fixture

所有方向只使用以下最小中性内容，并明确标注 `DESIGN FIXTURE ONLY — NOT PRODUCT CONTRACT`：

- Workspace：品牌增长
- Main Primary：本周增长方向已更新
- Secondary：团队完成了第一轮市场研究
- Action：查看结果
- Context：当前目标 / 当前工作
- Utility：Result / Evidence 轻量预览
- Employee：一个负责人引用

不得使用三个员工、完整 Content Growth、完整 RD、大量 KPI 或复杂 Dashboard 掩盖 Shell 设计能力。

## 7. Trae freedom

Trae 可自由决定 typography、grid、spacing、pane width、折叠处理、icon、divider/surface、depth、selected state、accent usage、visual rhythm、density 与 micro-interaction concept；但不得违反本合同的 Locked Structure 和 Frozen token 纪律。

## 8. Forbidden

`NO PRODUCT REDESIGN` · `NO NEW NAVIGATION` · `NO GLOBAL TOPBAR` · `NO DASHBOARD` · `NO CARD WALL` · `NO EMPLOYEE WALL` · `NO RUNTIME CONSOLE` · `NO WORKFLOW GRAPH` · `NO NEW BUSINESS MODULE` · `NO CONTENT GROWTH DESIGN` · `NO RD DESIGN` · `NO FIRST RUN DESIGN`。

## 9. One-shot qualification gate

Round 1 只输出 A/B/C，CEO 选择 A、B、C 或 NONE。若选择一个，只允许一次 bounded correction；必须证明能准确理解修改、保持选择方向、遵守 Locked Structure，并且不通过增加 Card 解决问题。

- 一次修正仍明显跑偏：`TRAE VISUAL DESIGN QUALIFICATION = FAIL`，停止投入。
- 通过一次修正：`TRAE VISUAL DESIGN QUALIFICATION = PASS`，之后才可进入 First Run、CEO 工作台、General Workspace、RD、Content Growth 等专项。

本合同不授权任何 Frontend、Prototype、Figma、Runtime、Schema、数据库或产品模型变更。

— CURIS MASTER SHELL VISUAL EXECUTION CONTRACT · STOP FOR CEO REVIEW
