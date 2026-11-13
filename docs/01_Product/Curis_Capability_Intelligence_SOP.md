# Curis 人才与能力情报专项 · 一站式维护 SOP

Status: Frozen（运营规程，CEO 2026-08-18 通过）  
Owner: 人才与能力情报负责人（WorkBuddy 侧）  
关联文档：`Talent_Library_Expansion_Report.md`、`Curis_Talent_Market_Resource_Audit.md`、`Curis_Talent_Market_Product_Map.md`、`Curis_Talent_Market_Integration_Contract.md`、`Curis_Talent_Candidate_Package_2026-08-18.md`

> 本文件是「职责与流程」规程，不是候选 Registry。所有候选数据仍落在既有生产线（`backend/app/agent_conversion/`）、候选包与 4 份 Talent Market 文档中。本文件不重复登记任何候选。

---

## 0. 职责升级登记（CEO 2026-08-18 通过）

初轮（08-14 / 08-18）仅负责 Candidate Discovery（发现→调研→整理→提供可导入候选）。  
**即日起升级为 Curis 人才与能力库长期一条龙维护**：

```
发现 → 扫描 → 去重 → 分类 → License/Security Gate
→ Curis 适配 → Expert/Skill/Connector 能力组合
→ 真实任务验证 → Evidence → 成熟度判断
→ 合格后进入现有 Curis 人才与能力库
```

继续消费并复用既有：
- 既有人才生产线 `backend/app/agent_conversion/`（CanonicalAgentSpec / 只读扫描 / Adapter）
- `Candidate Queue`（候选包 + 生产线去重键 `duplicate_key`）
- `CURIS_READY` 规则与成熟度投影 `MATURITY = DISCOVERED/CANDIDATE/COMPOSED/VALIDATED/CURIS_READY/BLOCKED`

**红线：禁止建立第二套 Registry / Candidate Queue / Capability Truth。**

---

## 1. 各阶段定义与判据

| 阶段 | 动作 | 产出 / 判据 | 责任方 |
|---|---|---|---|
| 发现 | 广域扫描生态源 | 真实可抓取的 Source URL；不伪造 | 本专项 |
| 扫描 | 拉取+解析（Adapter） | CanonicalAgentSpec 归一 | 本专项（复用生产线） |
| 去重 | `duplicate_key` 比对 | 已存在则跳过，不重复登记 | 本专项 |
| 分类 | 行业/职能/类型映射 | Expert / Expert-Team / Skill / Connector(MCP) / Tool 严格分离 | 本专项 |
| License/Security Gate | 闸门复核 | 非商用/无 SPDX → `BLOCKED`；凭据/注入/夸大 → `SECURITY REVIEW`→必要时 `BLOCKED` | 本专项 |
| Curis 适配 | 映射到 Curis 部门/资产模型 | 提出 `composition`（skills/tools/mcp/connector/model 需求） | 本专项 |
| 能力组合 | 绑定所需 Skill/Tool/Connector | 组合方案；标记缺失依赖 | 本专项（建议）→ Codex（执行） |
| 真实任务验证 | 在 Curis 运行时跑真实工作任务 | 可见 Result / Evidence；失败可恢复 | Codex 运行时（本专项定义验证用例） |
| Evidence | 留存运行证据 | 任务输入输出/日志摘要 | Codex 运行时 |
| 成熟度判断 | 综合闸门+验证 | 晋级或保持 Candidate/Review/Blocked | 本专项 |
| 入库 | 进入 Curis 人才与能力库 | `CURIS_READY`；可招募/可绑定 | Codex 发布链 |

### 1.1 CURIS_READY 晋级硬标准（本专项可主导，但必须满足）
不得因「来源知名 / README 优秀 / 营销描述完整」直接标 `CURIS_READY`。必须全部满足：
1. License 通过（商用可用，或已获明确授权）
2. Security 通过（无凭据泄漏 / 无提示注入 / 无能力夸大）
3. Curis 适配完成（部门/资产映射清晰）
4. 所需 Skill / Tool / Connector 已绑定或明确可得
5. 真实工作任务执行通过
6. 可检查 Result / Evidence 留存
7. 成熟度判断结论为合格

无法验证的，继续保持 `Candidate / Review / Blocked`。

### 1.2 与 Codex 能力专项的边界
- **本专项（WorkBuddy 侧）**：人才与能力内容本身、长期扫描、验证规划、入库判定、中文产品化。
- **Codex 能力专项**：「人才与能力」产品页面、交互、Runtime / 生产线能力开发、必要的抽样审计。
- **不让 Codex 成为每条候选入库的人工流水线**：抽样审计即可，不逐条卡。

---

## 2. 中文产品化强制标准（面向中文用户）

所有最终进入 Curis 人才与能力库、需展示给用户的条目（Expert / Expert-Team / Skill / Connector / Tool）**必须具有中文产品展示信息**，参考 WorkBuddy / Coze 的表达方式。

### 2.1 必须生成的中文展示字段（Product-facing Presentation）
- 中文名称
- 一句话简介
- 详细介绍
- 能力分类
- 擅长什么
- 适合做什么
- 典型使用场景
- 需要的工具 / 连接（仅当用户确实需要知道时展示）
- 来源
- 必要的安全 / 权限提示

### 2.2 表达要求
简单、直接、自然、面向普通用户，像「人才市场 / 技能商店」的商品介绍。
- ❌ “Provides semantic multi-stage retrieval orchestration with configurable context pipelines.”
- ✅ “帮助员工搜索和整理大量资料，并从中找到与当前任务最相关的信息。”
- ❌ “GitHub PR autonomous review agent with AST-aware analysis.”
- ✅ “自动检查代码改动，发现潜在问题，并给出代码审查建议。”

技术细节（MCP 协议、Adapter 字段、Prompt 术语、GitHub 工程描述）保留在内部 Metadata / Source / Integration 信息中，**不作为用户默认看到的介绍**。

### 2.3 原始信息不得被翻译覆盖（Source Truth 保留）
每条必须同时保留（内部 Metadata，不展示给用户默认视图）：
- `Original Name`
- `Original Description`
- `Source URL`
- `Version / Digest`
- `License`
- `Original Metadata`（原始分类、依赖、原始仓库结构等）

中文名称与中文介绍属于 **Product-facing Presentation**，不是新的 Source Truth。翻译/改写**不得改变原能力边界，不得把不存在的能力写进去**。

---

## 3. 默认职能人才优先验证（当前阶段硬任务）

Curis 正式产品需要默认职能组织。优先从当前候选池验证：

| 部门 | 优先验证角色 | 本专项动作 |
|---|---|---|
| 空间工程部 | 默认空间工程核心 Employee | 候选池核验；无外部候选则报告 Gap（属 Curis 内置职能，不得冒充外部 Expert） |
| 数据分析部 | 默认 Company Analyst / 公司经营分析师 | 候选池核验；可组合则给组合方案，否则报告 Gap |
| （储备） | Data Analyst / Business Analyst / BI Analyst / Analytics Engineer / Data Visualization / Research Analyst | 候选池核验；记录组件级覆盖与 Gap |

**无合格外部候选时明确报告 Gap。Curis 后续可定义内置 Employee，但不得将自定义 Employee 冒充外部市场 Expert。**

详见 `Curis_Default_Functional_Talent_Verification_2026-08-18.md`。

---

## 4. 长期持续扫描政策

- 不以 08-18 的 ~250 候选为结束，持续扩大 Universe。
- 空闲时继续扫描：WorkBuddy / Coze / OpenAI·Codex / Claude·Anthropic / MCP / GitHub / ClawHub / Agent·Skill marketplaces / 新出现高质量来源。
- 不受 Curis 当前 Business 限制；当前业务只影响推荐优先级。
- 已建立每周自动化「人才与能力库持续扫描（情报专项）」：聚焦 1–2 个新来源，抽取真实候选、对现有候选包去重、追加同格式条目、报告计数。
- 每次扫描均遵守 License/Security 闸门与中文产品化标准。

---

## 5. 交付与汇报纪律

- 不新建第二套人才库文档体系；优先更新既有 4 份 Talent Market 文档 + 候选包。
- 终态汇报须含：新扫描来源数、新资源数、Expert/Skill/MCP 数、去重后数量、License BLOCKED 数、Security Review 数、分类覆盖、新高价值来源、推荐优先导入候选。
- 严禁把「发现候选」冒充 `CURIS_READY`。
- 每轮结束以固定落款收束（见候选包末节）。

---

## 6. 当前阶段状态（2026-08-18 起）

- 初始 Universe 扩充：ACCEPTED（CEO 通过）。
- 一站式流水线：ACTIVE。
- 持续情报：ACTIVE（每周自动化 + 空闲增量）。
- 中文产品化：Batch1 进行中（见 `Curis_Talent_Chinese_Productization_Batch1.md`）。
- 默认职能人才：空间工程核心 Employee = Gap；数据分析部 = 部分组件覆盖 / 待组合（见验证文档）。
- CURIS_READY 晋级：0（候选池仍为 Candidate；晋级需运行时真实任务 + Evidence）。
