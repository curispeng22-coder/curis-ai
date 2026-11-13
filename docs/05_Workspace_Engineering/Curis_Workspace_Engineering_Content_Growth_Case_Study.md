# Curis · Workspace Engineering — Content Growth Case Study（内容增长案例复盘）

**Status**: `Review`
**Methodology State**: `WORKSPACE ENGINEERING METHODOLOGY APPROVED CANDIDATE`
**类型**: 方法论 · Case Study（正确链复盘）
**日期**: 2026-08-16
**上位**: `Curis_Workspace_Engineering_Methodology.md` · Lifecycle · Gates
**配套**: Handoff 协议（Doc 4）· RD Gap（Doc 6）
**真实素材**（均不修改，仅引用）:
- `docs/Content_Growth_Research/Curis_Content_Growth_Operating_Strategy_Product_Handoff.md`（PRODUCT DESIGN HANDOFF FINAL）
- `docs/03_Design/Curis_Content_Growth_Operating_Model.md`（上层运营模型）
- `docs/03_Design/Curis_Content_Growth_Product_Model_Closure.md`（产品模型收敛）
- `docs/03_Design/Curis_Content_Growth_Operating_Strategy_UX_Translation.md`（运营策略→产品体验翻译）
- `docs/03_Design/Curis_Content_Growth_User_Terminology_Map.md`（术语映射）
- `docs/03_Design/Curis_Content_Growth_*_Contract_Candidate.md`（9 契约 APPROVED CANDIDATE）
- `docs/03_Design/Curis_Company_OS_Shared_Authority.md` / `Curis_Content_Growth_Domain_Authority.md`（Frozen）

---

## 0. 阅读指引

本文复盘 Content Growth 这条**已经走通的正确链**，目的不是重复业务结论，而是提炼：

1. 这条链如何对应 Workspace Engineering 生命周期（Lifecycle 14 步）；
2. 哪些步骤**值得成为 Workspace Engineering 的标准**；
3. 反向检查：RD 是否跳过了其中关键的一步（详见 Doc 6）。

---

## 1. 正确链全景（Content Growth 实际走过的）

```text
[Business Intent]
  CEO 经营目标：内容增长（多平台/多账号经营）
        ↓
[Domain Expert Research]  ← 关键：真实领域专家介入
  Social Media Growth & Content Operations Expert
  → 7~9 份运营研究 + Review（增长总论/情报/选题/受众社区/发布平台/分析进化/总体框架）
        ↓
[Operating Model]
  《Content Growth 上层运营模型》：八步飞轮 + 五层策略归属
  + Office/Intent/Account 三层（Office 与 Organization 正交）
        ↓
[Product Handoff]  ← 关键：收敛为单份
  《Operating Strategy Product Handoff》（唯一入口，9 份研究作索引）
        ↓
[Product Translation]  ← 关键：专业→用户语言
  《Operating Strategy UX Translation》+ 《User Terminology Map》
  + 《Product Model Closure》（Office→「经营方向」；内部原语全隐藏）
        ↓
[Semantic Model + Shared/Domain Capability Review]
  9 契约设计（Batch A/B/C）→ 升格 Frozen：
  Company OS Shared Authority（⑥⑧⑦ + Context Isolation）
  Content Growth Domain Authority（①②③④⑤）
  注：这里升格是因为语义跨多个 Instance 复用并成为官方 Domain 标准，
      不是每个 Workspace 都必须 Frozen Domain Authority
        ↓
[Workspace Composition]
  Business Home + Professional Workspace（按需 Adaptive Surface 进入）
  + Connected Accounts；不做超级 Workspace
        ↓
[Workspace Design / Package Composition]
  XHS Instance APPROVED；Content Growth 产品模型 Closure 待高保真；
  动态 Workspace Package Runtime 尚未实现
        ↓
[后续：Implementation / Acceptance / Go Live / Operating Learning]
  （本 Case Study 只复盘到 Translation+Authority；实现/验收按 Lifecycle 后续步骤推进）
```

---

## 2. 逐环对照 Lifecycle

| Lifecycle 步骤 | Content Growth 实际做法 | 评价 |
|---|---|---|
| 1 BUSINESS INTENT | CEO 内容增长经营目标（多平台经营） | ✅ 意图清晰，未混淆成功能诉求 |
| 2 DOMAIN EXPERT RESEARCH | 真实 Social Media Growth Expert 做 7~9 份研究 | ✅ **正确链的关键**：真实领域专家、真实世界研究 |
| 3 OPERATING MODEL | 八步飞轮 + 五层策略归属 + Office/Intent/Account 三层 | ✅ 回答了「如何长期运行并变更好」 |
| 4 PRODUCT HANDOFF | 收敛为单份《Operating Strategy Product Handoff》 | ✅ **正确链的关键**：单份入口，9 份研究作索引 |
| 5 PRODUCT TRANSLATION | UX Translation + 术语映射 + 产品模型 Closure | ✅ Office→「经营方向」；内部原语全隐藏；复杂度默认隐藏 |
| 6 CAPABILITY REVIEW | 9 契约 Batch A/B/C → Frozen Shared + Domain Authority | ✅ REUSE/EXTEND 明确；本案例满足跨 Instance / 官方标准升级条件 |
| 7 COMPOSITION | Business Home + Professional Workspace（非超级 WS） | ✅ 由业务反推空间 |
| 8 SEMANTIC MODEL + WORKSPACE DESIGN | Content Growth 对象语义明确；XHS Instance APPROVED；CG Closure 待高保真 | ✅ 引用 Frozen 不重定义 |
| 9 PACKAGE COMPOSITION | 当前无可安装 Content Growth Package | ⏳ Target Runtime `NOT IMPLEMENTED`，不得把 Instance 设计冒充 Package |
| 10–14 | Expressibility / 验收 / 激活 / 学习 / 进化 | ⏳ 按 Lifecycle 后续推进 |

---

## 3. 哪些步骤值得成为 Workspace Engineering 标准（候选标准）

从这条正确链提炼出 **5 条候选 Workspace Engineering 标准**（非强制模板，是「值得复用的方法」）：

### 候选标准 A · 真实领域专家前置（对应步骤 2）
> 任何新 Business Space 必须先调用真实 Domain Expert 研究真实世界经营实践，**不得**用「竞品 UI 交互模式研究」冒充「行业经营方法研究」。

### 候选标准 B · 单份收敛 Handoff（对应步骤 4）
> 领域研究必须先收敛为**一份**《Product Handoff》作为唯一入口；原始研究仅作参考索引，不得整批直投产品专家。（即 Doc 4 协议）

### 候选标准 C · 用户语言翻译 + 内部原语隐藏（对应步骤 5）
> 产品专家把专业经营方法翻译为自然语言问题；Office / Routing / Queue / Token 等内部原语**默认隐藏**；复杂度默认隐藏；用户不学行业架构、不学 Curis Primitive。

### 候选标准 D · Semantic Model Before Instance（对应步骤 6–8）
> 搭 Workspace 前先明确对象、关系、状态、责任与关键业务真相。默认由 Package Domain Schema 承载局部语义；只有跨多个 Instance 复用、成为官方 Domain 标准、影响 Company OS 或需要长期兼容保证时，才升格 Domain Authority / Frozen。Instance 只做专业实现，不反向升格 Shell / Shared。

### 候选标准 E · 由业务反推空间、拒绝超级 Workspace（对应步骤 7）
> 空间组合由经营方法决定；Business Home 做聚合与轻操作，深度工作交给按需进入的 Professional Workspace；**不把一切塞进一个超级 Workspace**。

---

## 4. 这条链体现的「方法论纪律」正面清单

- ✅ 不画八步飞轮流程图给用户（UX Translation §1 第一原则）
- ✅ 不画五层策略配置树（用户面只说「默认这样运行 / 这个账号单独设置 / 这一次例外」）
- ✅ 平台事实四态（VERIFIED/CONDITIONAL/UNKNOWN/UNAVAILABLE），禁止写死研究数字
- ✅ 两套交互（对话驱动 + 直接编辑）修改同一份底层经营方法，禁止两套存储
- ✅ 不固定创建 5 个 Employee；一个员工可承担多职责，增长再拆
- ✅ Content Growth 的 Domain Authority 升格有跨 Instance / 官方标准理由，不把这条路径机械套给普通自定义 Workspace
- ✅ 不修改 Frozen Authority / Blueprint / XHS·RD / Runtime / Connector / 代码 / UI

---

## 5. 反向检查（指向 Doc 6）

Content Growth 走通了步骤 2（Domain Expert Research）与步骤 4（收敛 Handoff）。

**需追问**：RD Workspace 是否同样走通了步骤 2？——即，它是否先研究了「优秀软件研发组织到底如何经营研发业务」，再进入设计？

初步判断（详见 **Doc 6 · Curis_RD_Methodology_Gap_Review**）：RD Workspace 的《Reference Synthesis》研究的是 **Codex / Claude Code / Cursor / VS Code / Linear / Relevance AI 的产品 UI 交互模式**，这是**工具交互研究**，不是**研发业务经营研究**。两者不等价。RD 可能跳过了「优秀研发组织如何经营研发业务」这一 Domain Expert Research 阶段。

本文不下最终结论——Gap 判定见 Doc 6。

---

## 6. 状态

```text
CONTENT GROWTH CASE STUDY APPROVED CANDIDATE
```

*Curis Workspace Engineering — Content Growth Case Study · APPROVED CANDIDATE / Review（非 Frozen · 仅复盘）*
