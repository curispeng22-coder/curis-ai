# Curis 官方 Skill 能力库 v1（Official Skill Catalog）

> 阶段：Phase-1 Skill Foundation Bootstrap（Design Only · 研究 + 资产文档，零代码、零运行时改动）
> 维护者：产品经理（许清楚 / Xu）
> 适用：Admin 官方 Skill 资产库（非 Marketplace、非交易、不修改 Workspace Runtime）

---

## 一、研究来源与方法说明

本 v1 的能力来源，是通过**自行检索并研究**下列公开生态，**提取其中可复用的"职业 Skill 模式"**（而非复制具体 Agent 实现）。目标是从成熟框架中抽象出"专业知识 + 工作方法 + 执行流程 + 工具建议 + 输出标准"五元结构，沉淀为 Curis 的官方职业能力资产。

参考的外部生态（已在各 Skill 的 `source` 字段如实标注）：

- **MetaGPT SOP**（github.com/geekan/MetaGPT）：软件公司型多智能体，内建 ProductManager / Architect / ProjectManager / Engineer / QAEngineer 五角色与结构化交付链（PRD → 架构图 → 任务 → 代码 → 测试）。提取了需求分析、PRD、竞品象限图、系统设计、API 设计等职业 SOP。
- **ChatDev workflow**（OpenBMB/ChatDev，清华）：瀑布模型 + ChatChain，角色含 CEO/CTO/CPO/Programmer/Tester/Reviewer，强调"两人对辩"纠错与自反思质量门禁。提取了编码-测试-评审-文档的细粒度执行流程。
- **CrewAI example**（docs.crewai.com/examples）：通用型 crew，含 Marketing / Social Media / Support / Analysis / Recruitment 等角色与 Flow（Content Creator Flow、Lead Score Flow）。提取了内容策划、选题、市场分析、销售线索评分、竞品监控等商业化角色能力。
- **AutoGen pattern**（microsoft/autogen）：可对话智能体与 Group Chat / Human-in-the-loop 编排。提取了多角色协同评审、人在回路校验、反思式质量门禁等机制。
- **industry SOP**：内容营销 7 步工作流（research→brief→create→review→publish→distribute→measure）、GTM 八步框架（ICP→竞品→定价→通路→KPI→上市→迭代）、单位经济模型（LTV:CAC≥3:1）、财务建模与 SaaS 增长方法论。提取了内容运营与商业运营的标准流程。
- **Curis internal**：仅用于标注 Curis 平台原生、无直接外部对应、由本阶段新定义的能力（如与 Curis Runtime / Employee Runtime 强绑定的交付规范）。

**提取方法**：对每个生态，先识别其"角色职责 + 关键交付物 + 协作顺序 + 质量门禁"，再映射为 Curis 的 Skill 字段；凡涉及具体框架私有实现的部分一律抽象为能力描述，避免污染 Skill 资产。

---

## 二、Skill 定位声明（务必贯彻）

> **Skill 不是 Prompt 集合。Skill 是 AI 员工的职业能力资产。**

Skill 的结构定义为：
`Skill = 专业知识 + 工作方法 + 执行流程 + 工具建议 + 输出标准`

- **专业知识**：该职业背后的领域知识、模型与范式（如 KANO、MoSCoW、CAP 定理、漏斗/飞轮、LTV:CAC）。
- **工作方法**：解决该类问题的可复用套路与决策原则。
- **执行流程**：拿到什么输入、按什么顺序产出什么交付物。
- **工具建议**：推荐的系统和工具（非强制绑定）。
- **输出标准**：交付物格式与质量门槛，使下游角色/人类可直接消费。

本文件是 Curis **第一版官方 Skill 能力库**，定位为 Admin 侧资产库，供后续编排 AI 员工、绑定 Employee Runtime 时引用。**不**开发 Skill Marketplace、**不**开发 Skill 交易、**不**修改 Workspace Runtime。

---

# Pack A — AI 研发公司 Skill Pack

> 面向 AI 研发型公司的研发全链路职业资产。共 **52** 个 Skill，覆盖：产品 / 架构 / 开发 / 测试 / DevOps / 数据 / 安全。

---

### requirement_analysis  `产品`
- **description**: 将模糊的用户诉求拆解为结构化、可验证的产品需求。
- **target_role**: Product Manager
- **target_department**: 产品部
- **capability_instruction**: 专业知识——掌握需求工程、KANO 模型与 MoSCoW 优先级法。工作方法——用 5W1H 与原问题澄清区分"用户要的"与"用户真正的问题"。执行流程——接收一句话/一段需求 → 澄清干系人与原问题 → 输出功能/非功能/约束清单与优先级，交付架构与开发。
- **recommended_tools**: [Jira, Figma, 需求池, 用户访谈纪要]
- **output_standard**: 需求清单含功能点、优先级(P0/P1/P2)、验收口径；歧义点标注 Open Questions；可被下游直接消费。
- **version**: 1.0.0
- **source**: MetaGPT SOP

### prd_design  `产品`
- **description**: 撰写产品需求文档，定义目标、范围与验收标准。
- **target_role**: Product Manager
- **target_department**: 产品部
- **capability_instruction**: 专业知识——掌握 PRD 结构（背景/目标/范围/用户故事/需求池/验收）。工作方法——以用户价值与业务目标驱动，用竞争象限图辅助定位。执行流程——基于需求分析 → 产出 PRD（目标、用户故事、需求池、竞品象限、验收标准）→ 评审后交付架构师。
- **recommended_tools**: [Figma, Miro, Confluence, 竞争象限图]
- **output_standard**: 完整 PRD 含可量化目标、≥3 条用户故事、P0/P1/P2 需求池、验收标准；结构可被架构设计直接引用。
- **version**: 1.0.0
- **source**: MetaGPT SOP

### user_story_writing  `产品`
- **description**: 以"作为…我想要…以便…"格式编写可验收的用户故事。
- **target_role**: Product Manager
- **target_department**: 产品部
- **capability_instruction**: 专业知识——掌握 INVEST 原则与验收场景(AC)写法。工作方法——从角色视角拆解价值流，每个故事绑定一个可验证收益。执行流程——接收功能清单 → 按角色拆分故事 → 补充分支/异常的验收场景 → 进入需求池。
- **recommended_tools**: [Jira, 需求池, Confluence]
- **output_standard**: 每条用户故事含角色/诉求/收益三要素与可测试验收场景；粒度满足单迭代可交付。
- **version**: 1.0.0
- **source**: MetaGPT SOP

### competitive_analysis  `产品`
- **description**: 研究竞品并产出竞争格局与差异化机会。
- **target_role**: Product Manager
- **target_department**: 产品部
- **capability_instruction**: 专业知识——掌握竞品象限（功能完整度×易用性/市场份额）与评价维度。工作方法——选取 5–7 个对标对象，按统一维度打分与差距分析。执行流程——明确对标范围 → 检索/整理竞品能力 → 产出象限图与差距清单 → 反馈到 PRD 与定位。
- **recommended_tools**: [竞争象限图, WebSearch, 对标表]
- **output_standard**: 含 ≥5 竞品、统一维度评分、象限图、≥3 条差异化机会；结论可被产品定位引用。
- **version**: 1.0.0
- **source**: MetaGPT SOP

### product_roadmap  `产品`
- **description**: 制定分版本的产品路线图与里程碑。
- **target_role**: Product Manager
- **target_department**: 产品部
- **capability_instruction**: 专业知识——掌握路线图分层（愿景/主题/版本/迭代）与 Now/Next/Later 法。工作方法——以业务目标与用户价值排序主题，权衡依赖与资源。执行流程——聚合需求池与战略 → 排定版本主题与时间盒 → 输出路线图 → 周期复盘调整。
- **recommended_tools**: [Jira, 路线图看板, 需求池]
- **output_standard**: 路线图含版本主题、时间盒、关键里程碑、依赖风险；与需求池可追溯。
- **version**: 1.0.0
- **source**: Curis internal

### acceptance_criteria_design  `产品`
- **description**: 为需求定义可测试的验收标准（DoD/AC）。
- **target_role**: Product Manager / QA
- **target_department**: 产品部 / 测试部
- **capability_instruction**: 专业知识——掌握 Given/When/Then 与 Definition of Done。工作方法——从正向路径、异常路径、边界条件三类覆盖验收。执行流程——接收用户故事 → 编写验收场景 → 与开发/测试对齐 DoD → 进入测试设计。
- **recommended_tools**: [Jira, 测试用例库]
- **output_standard**: 每个故事含 ≥1 正向 + ≥1 异常验收场景；DoD 明确且可判定通过/失败。
- **version**: 1.0.0
- **source**: MetaGPT SOP

### feature_prioritization  `产品`
- **description**: 用结构化方法对功能需求做优先级排序。
- **target_role**: Product Manager
- **target_department**: 产品部
- **capability_instruction**: 专业知识——掌握 RICE / MoSCoW / KANO / 价值-成本矩阵。工作方法——以影响面、信心、成本三维量化排序，避免拍脑袋。执行流程——汇集候选需求 → 打分与加权 → 输出 P0/P1/P2 队列 → 同步路线图。
- **recommended_tools**: [需求池, 优先级矩阵表]
- **output_standard**: 每个需求含评分维度值与最终优先级；排序逻辑可解释、可复核。
- **version**: 1.0.0
- **source**: Curis internal

### user_research  `产品`
- **description**: 通过访谈/问卷/数据挖掘理解用户真实问题。
- **target_role**: Product Manager / UX Researcher
- **target_department**: 产品部
- **capability_instruction**: 专业知识——掌握定性（访谈/观察）与定量（问卷/行为数据）研究方法。工作方法——先假设后验证，用亲和图归纳洞察。执行流程——定义研究问题 → 选方法采样 → 执行并提炼洞察 → 输出 personas 与痛点清单。
- **recommended_tools**: [问卷工具, 数据分析平台, 访谈纪要, 亲和图]
- **output_standard**: 产出 personas、top 痛点、证据来源；洞察可追溯到具体用户原话或数据。
- **version**: 1.0.0
- **source**: CrewAI example

### product_metrics_definition  `产品`
- **description**: 定义北极星指标与分层产品度量体系。
- **target_role**: Product Manager
- **target_department**: 产品部
- **capability_instruction**: 专业知识——掌握 AARRR/漏斗、北极星指标、护栏指标。工作方法——指标与用户价值因果对齐，避免虚荣指标。执行流程——明确价值假设 → 选北极星与分层指标 → 定义口径与采集点 → 交付数据团队。
- **recommended_tools**: [数据分析平台, 指标字典]
- **output_standard**: 含北极星指标、≥3 层漏斗指标、口径定义、负责人；可落地采集。
- **version**: 1.0.0
- **source**: industry SOP

### release_planning  `产品`
- **description**: 规划版本发布范围、节奏与回滚预案。
- **target_role**: Product Manager / Project Manager
- **target_department**: 产品部 / 研发部
- **capability_instruction**: 专业知识——掌握发布火车、特性开关、灰度策略。工作方法——以最小可发布单元(MVP)控制风险。执行流程——汇总就绪需求 → 定发布窗口与范围 → 编写发布说明与回滚预案 → 协调上线。
- **recommended_tools**: [Jira, 发布看板, 特性开关平台]
- **output_standard**: 发布含范围、时间窗、发布说明、回滚方案、负责人；与路线图一致。
- **version**: 1.0.0
- **source**: Curis internal

### system_design  `架构`
- **description**: 设计整体系统架构与模块交互。
- **target_role**: Architect
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握分层架构、领域驱动设计、CAP 与伸缩原则。工作方法——以质量属性（性能/可用/可维护）驱动取舍。执行流程——基于 PRD → 产出架构图、模块边界、交互序列 → 评审后交付 PM 拆任务。
- **recommended_tools**: [架构图工具, C4/序列图, ADR]
- **output_standard**: 含架构图、模块职责、关键时序、技术约束；可被任务拆解直接引用。
- **version**: 1.0.0
- **source**: MetaGPT SOP

### api_design  `架构`
- **description**: 设计清晰、可演进的 API 接口契约。
- **target_role**: Architect / Backend Engineer
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握 REST/GraphQL、版本化、幂等、错误模型。工作方法——以消费者契约与向后兼容为原则。执行流程——定义资源与边界 → 编写接口契约（路径/字段/错误码）→ 评审 → 交付开发。
- **recommended_tools**: [OpenAPI/Swagger, Postman, 接口文档]
- **output_standard**: 含接口契约、字段定义、错误码、示例；向后兼容规则明确。
- **version**: 1.0.0
- **source**: MetaGPT SOP

### database_design  `架构`
- **description**: 设计数据模型、表结构与索引策略。
- **target_role**: Architect / Backend Engineer
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握范式、反范式、索引、分库分表。工作方法——以读写分布与一致性需求选型（OLTP/OLAP）。执行流程——建模实体关系 → 设计表/索引/约束 → 评审性能 → 交付开发。
- **recommended_tools**: [数据库建模工具, ER 图, 慢查询分析]
- **output_standard**: 含 ER 图、表结构、索引策略、容量估算；满足性能与一致性目标。
- **version**: 1.0.0
- **source**: MetaGPT SOP

### tech_selection  `架构`
- **description**: 基于约束做技术栈与中间件选型。
- **target_role**: Architect
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握选型评估维度（成熟度/生态/团队/成本/风险）。工作方法——以评分矩阵对比候选，附权衡记录。执行流程——明确约束（规模/时延/预算）→ 列候选与打分 → 产出选型建议与 ADR → 评审。
- **recommended_tools**: [技术雷达, ADR, 评分矩阵]
- **output_standard**: 选型含对比矩阵、推荐项、风险与回退；决策可追溯。
- **version**: 1.0.0
- **source**: MetaGPT SOP

### performance_design  `架构`
- **description**: 在设计阶段预留性能与容量方案。
- **target_role**: Architect
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握缓存、异步、批处理、限流、压测模型。工作方法——先定 SLO/SLI，再反推架构。执行流程——定义性能目标 → 识别瓶颈点 → 设计缓存/队列/分片 → 交付开发与测试。
- **recommended_tools**: [压测工具, APM, 容量模型]
- **output_standard**: 含 SLO、瓶颈对策、容量估算；目标可被性能测试校验。
- **version**: 1.0.0
- **source**: ChatDev workflow

### security_design  `安全`
- **description**: 在设计阶段嵌入安全与合规控制。
- **target_role**: Architect / Security Engineer
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握 OWASP Top 10、最小权限、加密与鉴权模型。工作方法——以威胁建模（STRIDE）识别风险点。执行流程——梳理资产与信任边界 → 威胁建模 → 定义认证/授权/数据保护方案 → 交付开发。
- **recommended_tools**: [威胁建模, 密钥管理, 安全扫描]
- **output_standard**: 含威胁清单、控制措施、合规映射；无高危未处置项。
- **version**: 1.0.0
- **source**: Curis internal

### architecture_review  `架构`
- **description**: 对方案做架构评审与质量门禁。
- **target_role**: Architect / Tech Lead
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握评审清单（可演进性/韧性/可观测性）。工作方法——多角色 Group Chat 式评审，记录决策与异议。执行流程——收方案 → 按清单评审 → 提修改项与 ADR → 出具评审结论。
- **recommended_tools**: [ADR, 评审清单, 架构图]
- **output_standard**: 评审含通过/有条件通过结论、修改项清单、ADR；结论可归档。
- **version**: 1.0.0
- **source**: AutoGen pattern

### microservice_design  `架构`
- **description**: 设计微服务边界、通信与治理。
- **target_role**: Architect
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握领域驱动（限界上下文）、服务网格、事件驱动。工作方法——以业务能力而非技术层拆分，避免分布式单体。执行流程——识别限界上下文 → 定义服务契约与通信 → 设计治理（熔断/链路追踪）→ 交付。
- **recommended_tools**: [服务网格, 消息队列, 链路追踪]
- **output_standard**: 含服务边界、契约、通信模式、治理策略；耦合度可接受。
- **version**: 1.0.0
- **source**: Curis internal

### data_modeling  `数据`
- **description**: 面向分析与应用设计数据模型与口径。
- **target_role**: Data Engineer / Architect
- **target_department**: 研发部 / 数据部
- **capability_instruction**: 专业知识——掌握维表/事实表、星型模型、数据分层(ODS/DWD/DWS)。工作方法——以业务过程为中心建模，统一口径。执行流程——梳理业务过程 → 设计模型与口径 → 评审 → 交付数据开发。
- **recommended_tools**: [数据仓库, 元数据/口径字典]
- **output_standard**: 含模型图、字段口径、分层说明；可被分析直接消费。
- **version**: 1.0.0
- **source**: Curis internal

### integration_design  `架构`
- **description**: 设计第三方/内部系统对接方案。
- **target_role**: Architect / Backend Engineer
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握同步/异步、Webhook、幂等、重试与对账。工作方法——以契约与失败处理优先。执行流程——定义对接边界与数据 → 设计协议与容错 → 评审 → 交付开发。
- **recommended_tools**: [API 网关, 消息队列, 契约测试]
- **output_standard**: 含对接协议、失败处理、对账方案；边界与责任清晰。
- **version**: 1.0.0
- **source**: Curis internal

### scalability_design  `架构`
- **description**: 设计可水平扩展的架构方案。
- **target_role**: Architect
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握无状态、分片、CDN、弹性伸缩。工作方法——以单点瓶颈与状态外置为切入点。执行流程——识别扩展瓶颈 → 设计无状态/分片/缓存 → 定义弹性策略 → 交付。
- **recommended_tools**: [容器编排, 负载均衡, 缓存]
- **output_standard**: 含扩展策略、瓶颈对策、弹性指标；可应对目标峰值。
- **version**: 1.0.0
- **source**: Curis internal

### python_development  `开发`
- **description**: 使用 Python 实现后端/脚本/算法功能。
- **target_role**: Backend Engineer
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握 Python 生态、类型注解、虚拟环境与测试。工作方法——以可读性与类型安全优先，遵循 PEP8。执行流程——收接口/任务 → 实现并自测 → 跑单测 → 提交 Code Review。
- **recommended_tools**: [Git, pytest, ruff, Poetry]
- **output_standard**: 代码通过类型检查与单测；符合团队规范；含必要注释。
- **version**: 1.0.0
- **source**: ChatDev workflow

### react_development  `开发`
- **description**: 使用 React 实现前端组件与页面。
- **target_role**: Frontend Engineer
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握组件化、Hooks、状态管理与可访问性。工作方法——以组件职责单一与受控/非受控清晰为原则。执行流程——收 UI/接口 → 拆组件 → 实现与联调 → 自测 → 提交。
- **recommended_tools**: [Git, Vite, MUI, Tailwind, Storybook]
- **output_standard**: 组件可被 Storybook 验证；通过 lint 与基础测试；符合设计稿。
- **version**: 1.0.0
- **source**: Curis internal

### backend_development  `开发`
- **description**: 实现服务端逻辑、接口与数据访问。
- **target_role**: Backend Engineer
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握服务端分层、事务、鉴权与错误处理。工作方法——以契约驱动实现，保证幂等与可观测。执行流程——收接口契约 → 实现业务逻辑与数据访问 → 自测 → 提交。
- **recommended_tools**: [Git, 框架(如 FastAPI/Spring), 数据库客户端]
- **output_standard**: 接口满足契约与错误模型；含日志与单测；通过 Review。
- **version**: 1.0.0
- **source**: ChatDev workflow

### frontend_development  `开发`
- **description**: 实现前端页面、交互与性能优化。
- **target_role**: Frontend Engineer
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握渲染策略、响应式、性能与可访问性。工作方法——以核心Web指标(LCP/CLS/INP)为准。执行流程——收设计稿/接口 → 实现页面与交互 → 性能自测 → 提交。
- **recommended_tools**: [Git, Vite, 浏览器 DevTools, Lighthouse]
- **output_standard**: 页面符合设计稿与响应式；核心指标达标；通过 Review。
- **version**: 1.0.0
- **source**: Curis internal

### debugging  `开发`
- **description**: 定位并修复缺陷与异常。
- **target_role**: Engineer
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握日志、断点、复现与二分定位法。工作方法——先稳定复现，再缩小范围，避免猜测式修改。执行流程——读报错与日志 → 构造最小复现 → 定位根因 → 修复并补回归测试。
- **recommended_tools**: [调试器, 日志平台, 单测框架]
- **output_standard**: 根因明确；修复含回归测试；同类问题不再复发。
- **version**: 1.0.0
- **source**: ChatDev workflow

### refactoring  `开发`
- **description**: 在不改行为前提下改善代码结构。
- **target_role**: Engineer
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握重构手法（提取/重命名/消除重复）与坏味道识别。工作方法——小步提交、测试护航、红绿重构。执行流程——识别坏味道 → 以测试护航小步重构 → 验证行为不变 → 提交。
- **recommended_tools**: [Git, 单测框架, Linter]
- **output_standard**: 行为等价（测试全绿）；复杂度下降；无明显新坏味道。
- **version**: 1.0.0
- **source**: ChatDev workflow

### code_review  `开发`
- **description**: 对代码变更做质量、安全与规范评审。
- **target_role**: Engineer / Tech Lead
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握评审清单（正确性/安全/可读性/测试）。工作方法——多审评审（Group Chat），给出可行动建议而非主观偏好。执行流程——读 diff 与上下文 → 按清单评审 → 提修改项 → 给出批准/驳回结论。
- **recommended_tools**: [Git PR, Linter, 静态扫描]
- **output_standard**: 评审含结论与具体修改项；高危/合规问题必须拦截。
- **version**: 1.0.0
- **source**: AutoGen pattern

### concurrency_programming  `开发`
- **description**: 实现并发/并行与异步任务处理。
- **target_role**: Backend Engineer
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握线程/协程/锁/队列与竞态规避。工作方法——以最小共享状态与明确所有权降低复杂度。执行流程——识别并发点 → 选型（线程/async/队列）→ 实现并压测 → 提交。
- **recommended_tools**: [并发框架, 压测工具, 单测]
- **output_standard**: 无死锁/竞态；吞吐达标；含并发测试。
- **version**: 1.0.0
- **source**: Curis internal

### algorithm_implementation  `开发`
- **description**: 实现与优化算法与数据结构。
- **target_role**: Engineer
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握复杂度分析、常见算法与数据结构取舍。工作方法——先正确后优化，以基准测试验证收益。执行流程——明确问题与约束 → 选算法 → 实现并测复杂度 → 优化提交。
- **recommended_tools**: [基准测试, 单测,  profiling]
- **output_standard**: 正确且复杂度可解释；含边界用例；性能达标。
- **version**: 1.0.0
- **source**: Curis internal

### api_implementation  `开发`
- **description**: 按契约实现并自测 API。
- **target_role**: Backend Engineer
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握请求校验、鉴权、限流与错误响应。工作方法——契约优先，保证幂等与向后兼容。执行流程——读接口契约 → 实现 + 中间件 → 契约测试 → 提交。
- **recommended_tools**: [OpenAPI, Postman, 契约测试]
- **output_standard**: 通过契约测试；错误码与示例一致；含基础鉴权。
- **version**: 1.0.0
- **source**: MetaGPT SOP

### sql_development  `开发`
- **description**: 编写高效、正确的 SQL 与数据访问层。
- **target_role**: Backend Engineer / Data Engineer
- **target_department**: 研发部 / 数据部
- **capability_instruction**: 专业知识——掌握索引、执行计划、事务隔离。工作方法——以集合思维替代行级循环，关注慢查询。执行流程——明确查询意图 → 写 SQL → 看执行计划优化 → 自测提交。
- **recommended_tools**: [数据库客户端, 慢查询分析, EXPLAIN]
- **output_standard**: SQL 命中索引、结果正确；含必要注释与边界处理。
- **version**: 1.0.0
- **source**: Curis internal

### test_driven_development  `开发`
- **description**: 以测试先行驱动实现。
- **target_role**: Engineer
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握红-绿-重构循环与测试金字塔。工作方法——先写失败测试定义行为，再实现使其通过。执行流程——写失败单测 → 实现至通过 → 重构 → 提交。
- **recommended_tools**: [单测框架, Mock, Coverage]
- **output_standard**: 覆盖率达标；测试先于实现；行为被锁定。
- **version**: 1.0.0
- **source**: ChatDev workflow

### typescript_development  `开发`
- **description**: 使用 TypeScript 实现类型安全的应用。
- **target_role**: Frontend/Fullstack Engineer
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握类型系统、泛型与编译期约束。工作方法——以严格模式减少运行时错误。执行流程——定义领域类型 → 实现 → 类型检查 → 提交。
- **recommended_tools**: [tsc, ESLint, Git]
- **output_standard**: 通过严格类型检查；无 any 滥用；含必要类型文档。
- **version**: 1.0.0
- **source**: Curis internal

### git_workflow  `开发`
- **description**: 规范分支管理与协作提交。
- **target_role**: Engineer
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握 trunk-based / feature-branch 与 rebase/merge。工作方法——小步提交、清晰 message、PR 模板。执行流程——建分支 → 小步提交 → 提 PR → 经 CI 与 Review 合并。
- **recommended_tools**: [Git, CI, PR 模板]
- **output_standard**: 提交历史清晰；通过 CI；无大杂烩 PR。
- **version**: 1.0.0
- **source**: Curis internal

### mobile_development  `开发`
- **description**: 实现移动端（iOS/Android）功能与适配。
- **target_role**: Mobile Engineer
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握原生/跨端、生命周期与离线/同步。工作方法——以平台规范与电量/流量敏感为先。执行流程——收需求 → 实现与适配 → 真机自检 → 提交。
- **recommended_tools**: [Xcode/Android Studio, 跨端框架, 真机]
- **output_standard**: 多机型适配通过；性能达标；符合平台规范。
- **version**: 1.0.0
- **source**: Curis internal

### documentation_writing  `开发`
- **description**: 编写技术文档、README 与接口说明。
- **target_role**: Engineer / Tech Writer
- **target_department**: 研发部
- **capability_instruction**: 专业知识——掌握文档分层（概念/操作/参考）与最小必要原则。工作方法——以读者视角组织，配套示例。执行流程——明确受众 → 写结构 + 示例 → 校验可运行 → 归档。
- **recommended_tools**: [Markdown, 文档站, 代码注释]
- **output_standard**: 文档可独立理解；含运行示例；与代码同步。
- **version**: 1.0.0
- **source**: Curis internal

### data_pipeline_development  `数据`
- **description**: 开发数据采集、清洗与调度管道。
- **target_role**: Data Engineer
- **target_department**: 数据部
- **capability_instruction**: 专业知识——掌握 ETL/ELT、调度、幂等与数据质量。工作方法——以可重跑与监控为默认要求。执行流程——定义源/口径 → 开发管道 → 加质量校验 → 调度上线。
- **recommended_tools**: [调度系统, 数据质量, 数据仓库]
- **output_standard**: 管道可重跑、数据质量达标；含监控与告警。
- **version**: 1.0.0
- **source**: Curis internal

### test_design  `测试`
- **description**: 设计覆盖需求与风险的测试用例集。
- **target_role**: QA Engineer
- **target_department**: 测试部
- **capability_instruction**: 专业知识——掌握等价类、边界值、场景法与正交法。工作方法——以验收标准与风险驱动覆盖。执行流程——读 PRD/AC → 设计用例（正向/异常/边界）→ 评审 → 入用例库。
- **recommended_tools**: [测试用例库, 需求文档]
- **output_standard**: 用例覆盖 AC 与主要风险；含预期结果；可被执行。
- **version**: 1.0.0
- **source**: ChatDev workflow

### automated_testing  `测试`
- **description**: 编写并执行自动化测试（单元/接口/UI）。
- **target_role**: QA / SDET
- **target_department**: 测试部
- **capability_instruction**: 专业知识——掌握测试金字塔、Page Object、断言与 Mock。工作方法——稳定可重复，减少脆弱测试。执行流程——选测试层 → 编写脚本 → 接 CI → 维护与去脆。
- **recommended_tools**: [pytest, Playwright, CI, Mock]
- **output_standard**: 自动化套件稳定通过；覆盖关键路径；接入 CI 门禁。
- **version**: 1.0.0
- **source**: ChatDev workflow

### performance_testing  `测试`
- **description**: 设计并执行性能/压测与容量验证。
- **target_role**: QA / Performance Engineer
- **target_department**: 测试部
- **capability_instruction**: 专业知识——掌握并发模型、思考时间、SLA 与瓶颈定位。工作方法——先定目标再压测，逐步加压。执行流程——定义场景与目标 → 建脚本 → 压测与监控 → 出报告与瓶颈。
- **recommended_tools**: [压测工具, APM, 监控]
- **output_standard**: 报告含吞吐/时延/拐点；对比 SLA；给瓶颈与建议。
- **version**: 1.0.0
- **source**: ChatDev workflow

### integration_testing  `测试`
- **description**: 验证多模块/多服务协作正确性。
- **target_role**: QA Engineer
- **target_department**: 测试部
- **capability_instruction**: 专业知识——掌握契约测试、端到端链路与数据准备。工作方法——以接口契约与关键链路为重点。执行流程——梳理链路 → 准备数据与桩 → 执行集成 → 报告缺陷。
- **recommended_tools**: [契约测试, 集成环境, 测试数据]
- **output_standard**: 关键链路通过；缺陷可复现；含环境要求说明。
- **version**: 1.0.0
- **source**: Curis internal

### regression_testing  `测试`
- **description**: 回归验证避免改动引入退化。
- **target_role**: QA Engineer
- **target_department**: 测试部
- **capability_instruction**: 专业知识——掌握回归范围选择（全量/风险基/影响面）。工作方法——以变更影响分析收窄范围、保障核心。执行流程——分析变更影响 → 选回归集 → 执行 → 出通过/失败报告。
- **recommended_tools**: [回归套件, CI, 缺陷系统]
- **output_standard**: 核心路径全绿；失败项可定位到变更；报告可追溯。
- **version**: 1.0.0
- **source**: ChatDev workflow

### test_retrospective  `测试`
- **description**: 对测试过程与缺陷做复盘与改进。
- **target_role**: QA Lead
- **target_department**: 测试部
- **capability_instruction**: 专业知识——掌握缺陷分布、逃逸分析与质量门禁。工作方法——以数据找根因，沉淀预防动作。执行流程——汇总缺陷与指标 → 归因 → 提流程改进 → 跟踪闭环。
- **recommended_tools**: [缺陷系统, 质量看板]
- **output_standard**: 复盘含根因、改进项、负责人；可度量改进效果。
- **version**: 1.0.0
- **source**: ChatDev workflow

### dockerization  `DevOps`
- **description**: 将应用容器化并优化镜像。
- **target_role**: DevOps / Backend Engineer
- **target_department**: 研发部 / 运维部
- **capability_instruction**: 专业知识——掌握多阶段构建、最小镜像与层缓存。工作方法——以可复现与体积优先。执行流程——写 Dockerfile → 多阶段构建 → 扫描与瘦身 → 入库。
- **recommended_tools**: [Docker, 镜像仓库, 扫描器]
- **output_standard**: 镜像可构建可运行；体积合理；无高危漏洞。
- **version**: 1.0.0
- **source**: ChatDev workflow

### cicd_pipeline  `DevOps`
- **description**: 搭建持续集成与持续交付流水线。
- **target_role**: DevOps Engineer
- **target_department**: 运维部
- **capability_instruction**: 专业知识——掌握流水线阶段（build/test/scan/deploy）与门禁。工作方法——失败快、反馈快，门禁防劣化。执行流程——定义阶段与触发 → 接测试/扫描 → 设门禁 → 启用。
- **recommended_tools**: [CI/CD, 制品库, 扫描器]
- **output_standard**: 流水线可自动跑通；含测试/扫描门禁；失败可阻断。
- **version**: 1.0.0
- **source**: ChatDev workflow

### deployment  `DevOps`
- **description**: 执行安全可控的应用部署。
- **target_role**: DevOps Engineer
- **target_department**: 运维部
- **capability_instruction**: 专业知识——掌握蓝绿/滚动发布、回滚与健康检查。工作方法——以可回滚为先，零停机为目标。执行流程——准备发布物 → 选发布策略 → 执行并校验 → 就绪/回滚。
- **recommended_tools**: [容器编排, 发布平台, 健康检查]
- **output_standard**: 发布成功且健康；回滚预案可用；含发布记录。
- **version**: 1.0.0
- **source**: ChatDev workflow

### monitoring  `DevOps`
- **description**: 建设指标/日志/链路三位一体可观测性。
- **target_role**: DevOps / SRE
- **target_department**: 运维部
- **capability_instruction**: 专业知识——掌握 SLI/SLO、黄金指标与告警分级。工作方法——以用户感知指标为顶层，分层下钻。执行流程——定义 SLO → 接指标/日志/链路 → 配告警 → 出看板。
- **recommended_tools**: [Prometheus/Grafana, 日志平台, APM]
- **output_standard**: 含 SLO、关键看板、有效告警；误报/漏报可控。
- **version**: 1.0.0
- **source**: Curis internal

### canary_release  `DevOps`
- **description**: 以灰度发布控制上线风险。
- **target_role**: DevOps / SRE
- **target_department**: 运维部
- **capability_instruction**: 专业知识——掌握流量切分、指标对比与自动回滚。工作方法——小流量验证后再放大，异常即停。执行流程——定灰度比例 → 放量并对比指标 → 决策扩量/回滚。
- **recommended_tools**: [服务网格, 发布平台, 监控]
- **output_standard**: 灰度含比例、判停阈值、回滚；指标对比明确。
- **version**: 1.0.0
- **source**: Curis internal

### infrastructure_as_code  `DevOps`
- **description**: 用代码声明与管理基础设施。
- **target_role**: DevOps / Platform Engineer
- **target_department**: 运维部
- **capability_instruction**: 专业知识——掌握 IaC 原则（声明式/幂等/版本化）。工作方法——以模块复用与变更评审为准。执行流程——定义资源模板 → 计划(plan)校验 → 应用并版本化 → 审计。
- **recommended_tools**: [Terraform, 云 CLI, 状态后端]
- **output_standard**: 基础设施可重建、变更可评审；状态受控。
- **version**: 1.0.0
- **source**: Curis internal

### log_analysis  `DevOps`
- **description**: 通过日志定位问题与异常模式。
- **target_role**: DevOps / SRE
- **target_department**: 运维部
- **capability_instruction**: 专业知识——掌握日志结构、聚合查询与关联分析。工作方法——以时间线与上下文关联定位根因。执行流程——界定问题时间窗 → 聚合检索 → 关联链路 → 输出结论。
- **recommended_tools**: [日志平台, APM, 查询语言]
- **output_standard**: 结论含根因线索与证据；可复现检索；附建议。
- **version**: 1.0.0
- **source**: Curis internal

### incident_response  `DevOps`
- **description**: 对线上故障做响应、止损与复盘。
- **target_role**: SRE / On-call
- **target_department**: 运维部
- **capability_instruction**: 专业知识——掌握事件分级、止损优先与无责复盘。工作方法——先恢复后深究，沟通透明。执行流程——接告警分级 → 止损与定位 → 恢复 → 出复盘与改进行动。
- **recommended_tools**: [告警, 值班, 复盘模板]
- **output_standard**: 事件有分级、时间线与复盘；改进行动有负责人。
- **version**: 1.0.0
- **source**: Curis internal

---

# Pack B — AI 内容运营 Skill Pack

> 面向内容/新媒体/增长型公司的内容运营全链路资产。共 **31** 个 Skill，覆盖：内容策划 / 选题 / 脚本 / 视频 / 设计 / 分发 / 数据 / 运营 / SEO / 直播 / 审核。

---

### viral_analysis  `内容分析`
- **description**: 拆解爆款内容的成功要素与可复制结构。
- **target_role**: Content Operator / Analyst
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握内容要素（钩子/结构/情绪/价值）与平台调性。工作方法——以拆解模板逐维度归因，区分偶然与可复制。执行流程——选爆款样本 → 逐维度拆解 → 提炼可复用模式 → 输出洞察。
- **recommended_tools**: [数据分析平台, 内容库, 竞品监控]
- **output_standard**: 含样本、要素拆解、可复制要点；结论有证据支撑。
- **version**: 1.0.0
- **source**: industry SOP

### topic_planning  `选题`
- **description**: 规划选题方向与月度选题池。
- **target_role**: Content Operator
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握选题矩阵（人设/痛点/热点/系列）。工作方法——以选题准入规则（合规/人设一致）过滤。执行流程——沉淀内容方向 → 生成选题池 → 打标签与排期 → 输出选题表。
- **recommended_tools**: [选题表, 内容日历, 热点工具]
- **output_standard**: 含选题标题、关键词、平台、责任人、状态；符合准入规则。
- **version**: 1.0.0
- **source**: CrewAI example

### content_planning  `内容策划`
- **description**: 制定单篇/系列内容策略与 Brief。
- **target_role**: Content Strategist
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握内容 Brief（受众/意图/关键信息/CTA）。工作方法——以目标与漏斗阶段匹配内容形态。执行流程——明确目标与受众 → 写 Brief（结构/要点/CTA）→ 评审 → 交付创作。
- **recommended_tools**: [内容 Brief 模板, 内容日历]
- **output_standard**: Brief 含受众/意图/结构/CTA/成功指标；可被创作直接消费。
- **version**: 1.0.0
- **source**: CrewAI example

### script_writing  `脚本`
- **description**: 撰写短视频/口播/长视频脚本。
- **target_role**: Script Writer
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握脚本结构（钩子-展开-转折-收尾）与节奏。工作方法——先钩子后正文，控制前 3 秒留存。执行流程——收 Brief → 写钩子与大纲 → 成稿（台词/画面/字幕）→ 自审。
- **recommended_tools**: [脚本模板, 分镜表]
- **output_standard**: 脚本含钩子、分镜、台词、字幕点；时长与节奏可控。
- **version**: 1.0.0
- **source**: industry SOP

### video_optimization  `视频`
- **description**: 从完播/互动角度优化视频呈现。
- **target_role**: Content Operator / Editor
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握完播率驱动要素（节奏/字幕/封面/前 3 秒）。工作方法——以数据指标反推剪辑决策。执行流程——看数据短板 → 调结构/字幕/节奏 → 出优化版 → 验证。
- **recommended_tools**: [剪辑软件, 数据分析平台]
- **output_standard**: 优化含改动点与预期指标；前后可对比验证。
- **version**: 1.0.0
- **source**: industry SOP

### data_retrospective  `数据分析`
- **description**: 对内容表现做周期复盘与策略迭代。
- **target_role**: Content Analyst
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握内容指标（播放/完播/互动/涨粉/转化）。工作方法——以周/月维度找模式与归因。执行流程——拉指标 → 找高/低表现模式 → 提迭代动作 → 反馈选题。
- **recommended_tools**: [数据分析平台, 内容看板]
- **output_standard**: 复盘含模式、归因、动作；指标口径一致可追溯。
- **version**: 1.0.0
- **source**: industry SOP

### cover_design_advice  `设计`
- **description**: 给出封面/缩略图的设计建议以提升点击。
- **target_role**: Content Operator / Designer
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握封面三要素（对比/人脸/文字/情绪）。工作方法——以 A/B 思维给出多方案。执行流程——明确平台规格与卖点 → 给构图/配色/文案建议 → 多版备选。
- **recommended_tools**: [设计工具, 平台规格表]
- **output_standard**: 含 ≥2 方案与点击卖点说明；符合平台尺寸规范。
- **version**: 1.0.0
- **source**: industry SOP

### title_optimization  `文案`
- **description**: 优化标题/文案以提升点击与搜索。
- **target_role**: Copywriter
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握标题类型（数字/疑问/干货/场景）与禁词。工作方法——以利益点与好奇心平衡，避免标题党。执行流程——列候选标题 → 评估卖点与合规 → 给推荐与理由。
- **recommended_tools**: [标题库, 禁词表]
- **output_standard**: 含 ≥3 候选与推荐理由；无违规/夸大。
- **version**: 1.0.0
- **source**: industry SOP

### multi_platform_distribution  `分发`
- **description**: 制定多平台分发与形态适配策略。
- **target_role**: Content Operator
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握各平台调性、画幅与算法差异。工作方法——一源多用、按平台改形态与钩子。执行流程——定源内容 → 适配各平台规格/文案 → 排期分发 → 追踪。
- **recommended_tools**: [多平台后台, 内容日历, 调度工具]
- **output_standard**: 含平台清单、形态差异、发布时间；避免简单搬运。
- **version**: 1.0.0
- **source**: industry SOP

### fan_operation  `运营`
- **description**: 运营粉丝关系与社群活跃。
- **target_role**: Community Operator
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握社群生命周期、互动节奏与用户分层。工作方法——以价值供给与情感连接驱动留存。执行流程——分层粉丝 → 设计互动机制 → 运营社群/评论 → 复盘活跃。
- **recommended_tools**: [社群工具, 私域, 数据分析]
- **output_standard**: 含分层、互动计划、活跃指标；运营动作可执行。
- **version**: 1.0.0
- **source**: Curis internal

### livestream_script  `直播`
- **description**: 撰写直播流程与话术脚本。
- **target_role**: Live Operator / Host
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握直播节奏（暖场/卖点/逼单/留存）。工作方法——以转化漏斗设计环节与话术。执行流程——定目标与货品 → 写流程与话术 → 排互动点 → 彩排。
- **recommended_tools**: [直播脚本模板, 商品表]
- **output_standard**: 含流程、话术、互动点、应急；与目标对齐。
- **version**: 1.0.0
- **source**: Curis internal

### seo_optimization  `SEO`
- **description**: 优化内容搜索可见度与关键词布局。
- **target_role**: SEO Specialist
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握关键词研究、搜索意图与站内 SEO。工作方法——以意图匹配而非堆词。执行流程——研究关键词与意图 → 给标题/结构/内链建议 → 跟踪排名。
- **recommended_tools**: [关键词工具, 搜索控制台, 数据分析]
- **output_standard**: 含关键词表、优化点、排名目标；符合搜索意图。
- **version**: 1.0.0
- **source**: industry SOP

### content_calendar  `内容策划`
- **description**: 维护 30–90 天内容日历与产能排期。
- **target_role**: Content Operator
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握日历分层（已定/已批/储备）与产能匹配。工作方法——以稳定节奏优先于强度。执行流程——汇总选题 → 排期到天/周 → 绑责任人与状态 → 滚动更新。
- **recommended_tools**: [内容日历, Notion/Airtable, 调度工具]
- **output_standard**: 含主题/格式/关键词/阶段/责任人/日期/状态；可滚动。
- **version**: 1.0.0
- **source**: industry SOP

### hook_writing  `文案`
- **description**: 批量撰写高留存开头钩子。
- **target_role**: Copywriter / Script Writer
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握钩子类型（反差/悬念/痛点/利益）。工作方法——先钩子后脚本，批量产出择优。执行流程——明确受众痛点 → 批量写钩子 → 自评前 3 秒吸引力 → 推优。
- **recommended_tools**: [钩子库, 脚本模板]
- **output_standard**: 含 ≥10 钩子与类型标注；前 3 秒吸引力可判。
- **version**: 1.0.0
- **source**: industry SOP

### copywriting  `文案`
- **description**: 撰写各类平台的正文与推广文案。
- **target_role**: Copywriter
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握 AIDA/ PAS 文案结构与品牌语调。工作方法——以用户收益与情绪驱动。执行流程——明目标与受众 → 写正文（引入-价值-行动）→ 校验语调。
- **recommended_tools**: [文案模板, 品牌语调手册]
- **output_standard**: 文案含结构、CTA、语调一致；目标可达成。
- **version**: 1.0.0
- **source**: CrewAI example

### brand_voice  `品牌`
- **description**: 塑造并维护账号人设与品牌语调。
- **target_role**: Brand Strategist
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握人设维度（基调/价值观/语言风格）。工作方法——以一致性建立认知资产。执行流程——定义人设卡 → 沉淀语调规范 → 审稿对齐 → 迭代。
- **recommended_tools**: [人设卡, 语调手册]
- **output_standard**: 含人设卡与语调规范；内容可被一致性校验。
- **version**: 1.0.0
- **source**: Curis internal

### thumbnail_strategy  `设计`
- **description**: 制定缩略图策略以最大化点击。
- **target_role**: Designer / Content Operator
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握缩略图视觉权重与信息密度。工作方法——以 A/B 与系列化降低认知成本。执行流程——定卖点 → 给构图/色彩/文字方案 → 多版测试。
- **recommended_tools**: [设计工具, A/B 测试]
- **output_standard**: 含方案与卖点；可量化点击对比。
- **version**: 1.0.0
- **source**: industry SOP

### content_series_planning  `内容策划`
- **description**: 规划内容系列以提升期待与复看。
- **target_role**: Content Strategist
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握系列化（栏目/连续剧/挑战）的留存逻辑。工作方法——以固定栏目训练用户预期。执行流程——定系列主题 → 拆集与节奏 → 排入日历 → 跟踪。
- **recommended_tools**: [内容日历, 栏目模板]
- **output_standard**: 含系列主题、集纲、节奏；可被持续生产。
- **version**: 1.0.0
- **source**: industry SOP

### trend_research  `选题`
- **description**: 研究热点与平台趋势以指导创作。
- **target_role**: Content Researcher
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握趋势信号（上升词/音频/玩法）与适配判断。工作方法——借势不盲从，贴合人设。执行流程——监测趋势 → 评估适配度 → 转选题建议 → 反馈。
- **recommended_tools**: [热点工具, 数据分析, 竞品监控]
- **output_standard**: 含趋势、适配判断、选题建议；来源可追溯。
- **version**: 1.0.0
- **source**: industry SOP

### editing_guidance  `视频`
- **description**: 给出剪辑思路与节奏指导。
- **target_role**: Editor / Content Operator
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握剪辑节奏、转场、字幕与情绪曲线。工作方法——以完播曲线定位剪辑改动点。执行流程——看素材与数据 → 给结构/节奏/字幕建议 → 批量剪辑。
- **recommended_tools**: [剪辑软件, 数据分析]
- **output_standard**: 含剪辑方案与改动点；可被 editor 执行。
- **version**: 1.0.0
- **source**: industry SOP

### community_management  `运营`
- **description**: 管理评论区与私信互动。
- **target_role**: Community Operator
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握互动话术、危机应对与情绪识别。工作方法——以真诚与及时建立信任。执行流程——监控评论/私信 → 分级回复 → 处理负面 → 沉淀话术。
- **recommended_tools**: [社群工具, 私信后台, 话术库]
- **output_standard**: 含回复分级、话术、危机预案；响应及时。
- **version**: 1.0.0
- **source**: Curis internal

### content_audit  `审核`
- **description**: 对内容进行合规与质量三级审核。
- **target_role**: Content Reviewer
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握敏感词、极限词、违规话术与平台规则。工作方法——机器初审+人工复审+负责人终审。执行流程——跑敏感词筛查 → 人工复核 → 负责人终审 → 出结论。
- **recommended_tools**: [敏感词库, 审核清单, 平台规则]
- **output_standard**: 审核含结论与修改项；合规红线零容忍。
- **version**: 1.0.0
- **source**: industry SOP

### content_repurposing  `分发`
- **description**: 将单篇内容二创为多种形态复用。
- **target_role**: Content Operator
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握一源多用（视频→图文→金句→播客）。工作方法——以平台形态适配而非搬运。执行流程——提取核心资产 → 改写为多形态 → 排期分发 → 追踪。
- **recommended_tools**: [内容库, 多平台后台, 调度工具]
- **output_standard**: 含复用形态清单与排期；资产利用率提升。
- **version**: 1.0.0
- **source**: industry SOP

### platform_algorithm_research  `数据分析`
- **description**: 研究平台算法逻辑以优化分发。
- **target_role**: Content Analyst
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握推荐/分发信号（完播/互动/时效/标签）。工作方法——以实验与数据反推，而非臆测。执行流程——定义信号假设 → 小实验验证 → 提炼规律 → 反馈创作。
- **recommended_tools**: [数据分析平台, A/B 测试]
- **output_standard**: 含信号假设、实验、结论；可指导策略。
- **version**: 1.0.0
- **source**: industry SOP

### email_newsletter  `分发`
- **description**: 策划与撰写私域邮件/ newsletter。
- **target_role**: Content Operator / CRM
- **target_department**: 内容部 / 商业部
- **capability_instruction**: 专业知识——掌握邮件节奏、打开率与分层推送。工作方法——以价值优先、控制频率避免取关。执行流程——定主题与节奏 → 写内容 → 分层推送 → 看打开/转化。
- **recommended_tools**: [邮件工具, 私域, 数据分析]
- **output_standard**: 含主题、节奏、分层；打开/转化可追踪。
- **version**: 1.0.0
- **source**: industry SOP

### ugc_campaign  `运营`
- **description**: 策划用户生成内容(UGC)活动。
- **target_role**: Community Operator
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握活动机制（话题/激励/评选）与传播。工作方法——以低门槛参与与奖励驱动。执行流程——定主题与机制 → 设计激励 → 发起与传播 → 复盘。
- **recommended_tools**: [话题页, 激励工具, 数据分析]
- **output_standard**: 含机制、激励、传播计划；参与与曝光可量化。
- **version**: 1.0.0
- **source**: Curis internal

### influencer_collab  `运营`
- **description**: 策划并执行达人/博主合作。
- **target_role**: Partnership / Content Operator
- **target_department**: 内容部 / 商业部
- **capability_instruction**: 专业知识——掌握选号（调性/粉丝质量/性价比）与 Brief。工作方法——以匹配度而非纯粉丝量选人。执行流程——定目标与预算 → 选号与 Brief → 执行跟进 → 复盘 ROI。
- **recommended_tools**: [达人库, 数据平台, 合同]
- **output_standard**: 含选号、Brief、KPI；ROI 可复盘。
- **version**: 1.0.0
- **source**: CrewAI example

### content_performance_dashboard  `数据分析`
- **description**: 搭建内容数据看板与指标追踪。
- **target_role**: Content Analyst
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握内容指标分层与看板设计。工作方法——以决策问题导向选取指标。执行流程——定义指标与口径 → 搭看板 → 设预警 → 周报。
- **recommended_tools**: [数据分析平台, 看板工具]
- **output_standard**: 含指标口径、看板、预警；可被决策直接使用。
- **version**: 1.0.0
- **source**: industry SOP

### paid_promotion  `投放`
- **description**: 给出内容投放与付费推广建议。
- **target_role**: Growth / Media Buyer
- **target_department**: 内容部 / 商业部
- **capability_instruction**: 专业知识——掌握投放漏斗、出价与素材轮换。工作方法——以小预算快测、优胜劣汰。执行流程——定目标与受众 → 给素材与出价建议 → 跑量优化 → 复盘。
- **recommended_tools**: [广告平台, 数据分析]
- **output_standard**: 含计划、素材建议、优化动作；ROI 可追踪。
- **version**: 1.0.0
- **source**: CrewAI example

### competitor_content_watch  `数据分析`
- **description**: 持续监控竞品内容动态与打法。
- **target_role**: Content Analyst
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握竞品内容矩阵与节奏监测。工作方法——以差异化而非跟风为决策。执行流程——建竞品池 → 定期抓取与归类 → 提炼打法 → 反馈策略。
- **recommended_tools**: [竞品监控, 内容库]
- **output_standard**: 含竞品动态、打法总结、差异建议；周期更新。
- **version**: 1.0.0
- **source**: CrewAI example

### content_brief_writing  `内容策划`
- **description**: 为创作者撰写可执行的单篇内容 Brief。
- **target_role**: Content Strategist
- **target_department**: 内容部
- **capability_instruction**: 专业知识——掌握 Brief 必备字段（目标/受众/结构/约束）。工作方法——以"创作零歧义"为验收。执行流程——聚合需求与选题 → 填 Brief 模板 → 评审 → 交付。
- **recommended_tools**: [Brief 模板, 内容日历]
- **output_standard**: Brief 含目标/受众/结构/CTA/合规；创作者可直接开干。
- **version**: 1.0.0
- **source**: industry SOP

---

# Pack C — AI 商业运营 Skill Pack

> 面向商业/增长/商业化公司的商业运营资产。共 **22** 个 Skill，覆盖：市场 / 用户研究 / 销售 / 商业计划 / 财务 / 定价 / 渠道 / 客户成功 / 增长 / 融资 / 竞争。

---

### market_analysis  `市场`
- **description**: 分析市场规模、趋势与结构。
- **target_role**: Business Analyst / Strategist
- **target_department**: 商业部
- **capability_instruction**: 专业知识——掌握 TAM/SAM/SOM、波特五力与趋势研判。工作方法——以一手与二手数据交叉验证。执行流程——界定市场 → 测算规模与增速 → 析结构与驱动 → 出报告。
- **recommended_tools**: [行业报告, 数据分析, 报表]
- **output_standard**: 含规模测算、结构、趋势与机会；数据有出处。
- **version**: 1.0.0
- **source**: CrewAI example

### user_research_biz  `用户研究`
- **description**: 研究客户画像、需求与付费意愿。
- **target_role**: User Researcher / PMM
- **target_department**: 商业部 / 产品部
- **capability_instruction**: 专业知识——掌握定性访谈与定量调查、jobs-to-be-done。工作方法——以证据建 personas 与痛点。执行流程——定研究问题 → 采样执行 → 提炼画像与意愿 → 出洞察。
- **recommended_tools**: [问卷, 访谈, 数据分析]
- **output_standard**: 含 personas、痛点、付费意愿；洞察可追溯。
- **version**: 1.0.0
- **source**: CrewAI example

### sales_strategy  `销售`
- **description**: 制定销售策略与打法。
- **target_role**: Sales Lead
- **target_department**: 商业部
- **capability_instruction**: 专业知识——掌握销售模型（PLG/自销/内部/外部）与方法论（MEDDIC）。工作方法——以单元经济匹配销售投入。执行流程——定 ICP 与模型 → 设流程与阶段 → 配方法论 → 出打法。
- **recommended_tools**: [CRM, 销售看板, 话术库]
- **output_standard**: 含模型、流程、方法论、目标；可落地执行。
- **version**: 1.0.0
- **source**: CrewAI example

### business_plan  `商业计划`
- **description**: 撰写商业计划书（BP）。
- **target_role**: Founder / Strategy
- **target_department**: 商业部
- **capability_instruction**: 专业知识——掌握 BP 结构（问题/方案/市场/模型/团队/财务）。工作方法——以证据链串联，避免空泛。执行流程——明确叙事主线 → 写各模块 → 对齐财务 → 出 BP。
- **recommended_tools**: [BP 模板, 财务模型, 市场数据]
- **output_standard**: 含完整模块与数据支撑；逻辑自洽可路演。
- **version**: 1.0.0
- **source**: industry SOP

### financial_analysis  `财务`
- **description**: 分析经营财务与盈利质量。
- **target_role**: Financial Analyst
- **target_department**: 商业部 / 财务部
- **capability_instruction**: 专业知识——掌握三大报表、毛利/净利与现金流。工作方法——以趋势与结构分析定位问题。执行流程——取账务数据 → 比率与趋势分析 → 归因 → 出建议。
- **recommended_tools**: [财务系统, 报表, 数据平台]
- **output_standard**: 含关键比率、趋势、归因与建议；口径一致。
- **version**: 1.0.0
- **source**: industry SOP

### pricing_strategy  `定价`
- **description**: 设计定价与套餐（good-better-best）。
- **target_role**: PMM / Pricing Lead
- **target_department**: 商业部
- **capability_instruction**: 专业知识——掌握定价法（价值/竞争/成本）与包装策略。工作方法——以支付意愿与感知价值定档。执行流程——研竞品与意愿 → 设档位与权益 → 定价 → 验单元经济。
- **recommended_tools**: [定价研究, 竞品, 财务模型]
- **output_standard**: 含档位、权益、价格、依据；与单元经济一致。
- **version**: 1.0.0
- **source**: industry SOP

### channel_management  `渠道`
- **description**: 管理与优化销售/分销渠道。
- **target_role**: Channel Manager
- **target_department**: 商业部
- **capability_instruction**: 专业知识——掌握直营/代理/市场/伙伴等渠道 economics。工作方法——以渠道 ROI 与冲突管理为先。执行流程——盘渠道与表现 → 定政策与激励 → 优化结构 → 复盘。
- **recommended_tools**: [CRM, 渠道报表, 合同]
- **output_standard**: 含渠道表现、政策、优化项；ROI 可追踪。
- **version**: 1.0.0
- **source**: industry SOP

### customer_success  `客户成功`
- **description**: 设计客户 onboarding、健康度与续费扩量。
- **target_role**: Customer Success Manager
- **target_department**: 商业部
- **capability_instruction**: 专业知识——掌握时间到价值(TTV)、健康分与 land-expand。工作方法——以主动干预降流失、提扩展。执行流程——设计 onboarding → 建健康分 → 预警干预 → 扩量续费。
- **recommended_tools**: [CS 平台, 健康分, CRM]
- **output_standard**: 含 onboarding、健康分、干预动作；续费/扩展可量化。
- **version**: 1.0.0
- **source**: industry SOP

### growth_hacking  `增长`
- **description**: 以实验驱动用户与营收增长。
- **target_role**: Growth Manager
- **target_department**: 商业部
- **capability_instruction**: 专业知识——掌握 AARRR、增长循环与实验方法论。工作方法——以小成本快实验、数据择优。执行流程——定增长目标 → 列假设与实验 → 跑量分析 → 放大胜者。
- **recommended_tools**: [数据分析, A/B 测试, 漏斗工具]
- **output_standard**: 含假设、实验、结果、放大建议；可复现。
- **version**: 1.0.0
- **source**: industry SOP

### fundraising_materials  `融资`
- **description**: 撰写融资材料（BP/Teaser/数据室）。
- **target_role**: Founder / Strategy
- **target_department**: 商业部
- **capability_instruction**: 专业知识——掌握投资人关注点（市场/壁垒/单位经济/团队）。工作方法——以叙事+数据双轴说服。执行流程——定受众与轮次 → 写核心材料 → 备数据室 → 路演打磨。
- **recommended_tools**: [BP 模板, 财务模型, 数据室]
- **output_standard**: 含 BP/Teaser/数据室；逻辑与数据经得起尽调。
- **version**: 1.0.0
- **source**: industry SOP

### competitor_monitoring  `竞争`
- **description**: 持续监控竞品动态与战略。
- **target_role**: Strategy / Competitive Intel
- **target_department**: 商业部
- **capability_instruction**: 专业知识——掌握竞品情报维度（产品/定价/融资/招聘）。工作方法——以结构化情报支撑决策。执行流程——建竞品池 → 定期采集归类 → 析动向 → 出简报。
- **recommended_tools**: [竞品监控, 行业报告, 新闻]
- **output_standard**: 含竞品动态、影响判断、建议；周期更新。
- **version**: 1.0.0
- **source**: CrewAI example

### gtm_strategy  `市场`
- **description**: 制定市场进入(GTM)策略与上市计划。
- **target_role**: GTM Manager / PMM
- **target_department**: 商业部
- **capability_instruction**: 专业知识——掌握 GTM 八步（ICP→竞品→定价→通路→KPI→上市→迭代）。工作方法——以数据为底座、跨部门对齐。执行流程——定 ICP 与价值主张 → 选模型/通路/定价 → 设 KPI → 上市迭代。
- **recommended_tools**: [GTM 模板, CRM, 财务模型]
- **output_standard**: 含 ICP、定位、模型、KPI、里程碑；可被执行。
- **version**: 1.0.0
- **source**: industry SOP

### icp_definition  `用户研究`
- **description**: 定义理想客户画像(ICP)与买家角色。
- **target_role**: PMM / Sales Lead
- **target_department**: 商业部
- **capability_instruction**: 专业知识——掌握 ICP 与 buyer persona 维度（角色/痛点/决策）。工作方法——以赢单客户反推最优画像。执行流程——取赢单/输单数据 → 提炼共性 → 定义 ICP 与角色 → 对齐。
- **recommended_tools**: [CRM, 数据分析, 赢单库]
- **output_standard**: 含 ICP 标准与角色卡；可被销售精准触达。
- **version**: 1.0.0
- **source**: industry SOP

### unit_economics  `财务`
- **description**: 测算单位经济（LTV:CAC、回收期）。
- **target_role**: Financial / Strategy
- **target_department**: 商业部
- **capability_instruction**: 专业知识——掌握 CAC、LTV、回收期与 LTV:CAC≥3:1。工作方法——以分渠道单元经济决策可扩展性。执行流程——取获客与营收数据 → 算单元指标 → 判可持续性 → 给建议。
- **recommended_tools**: [财务模型, CRM, 数据分析]
- **output_standard**: 含 CAC/LTV/回收期与分渠道；可支撑 GTM 决策。
- **version**: 1.0.0
- **source**: industry SOP

### revenue_operations  `运营`
- **description**: 搭建营收运营(RevOps)协同体系。
- **target_role**: RevOps Lead
- **target_department**: 商业部
- **capability_instruction**: 专业知识——掌握营销-销售-成功的数据/流程/系统对齐。工作方法——以单一数据源与流程打通降摩擦。执行流程——盘现有流程与系统 → 定义统一口径 → 设自动化 → 出看板。
- **recommended_tools**: [CRM, 数据平台, 自动化]
- **output_standard**: 含流程、口径、系统图；跨部门可协同。
- **version**: 1.0.0
- **source**: industry SOP

### churn_analysis  `客户成功`
- **description**: 分析客户流失原因与挽留策略。
- **target_role**: CS / Analyst
- **target_department**: 商业部
- **capability_instruction**: 专业知识——掌握流失信号、同期群与挽留杠杆。工作方法——以同期群定位高危节点。执行流程——取留存/流失数据 → 同期群与归因 → 定挽留动作 → 跟踪。
- **recommended_tools**: [CS 平台, 同期群, 数据分析]
- **output_standard**: 含流失归因、高危节点、挽留动作；可量化改善。
- **version**: 1.0.0
- **source**: industry SOP

### partnership_development  `渠道`
- **description**: 拓展与管理战略合作伙伴。
- **target_role**: Partnership Manager
- **target_department**: 商业部
- **capability_instruction**: 专业知识——掌握伙伴类型（渠道/技术/生态）与共赢模型。工作方法——以价值互补与可量化收益驱动。执行流程——定伙伴战略 → 筛选与触达 → 谈机制 → 落地复盘。
- **recommended_tools**: [CRM, 合同, 数据平台]
- **output_standard**: 含伙伴清单、机制、KPI；合作可量化。
- **version**: 1.0.0
- **source**: Curis internal

### brand_strategy_biz  `品牌`
- **description**: 制定品牌定位与传播策略。
- **target_role**: Brand Strategist
- **target_department**: 商业部
- **capability_instruction**: 专业知识——掌握定位、品牌资产与信息屋(message house)。工作方法——以差异化与一致性建设认知。执行流程——定定位与价值 → 建信息屋 → 配传播 → 测认知。
- **recommended_tools**: [品牌手册, 调研, 内容平台]
- **output_standard**: 含定位、信息屋、传播计划；可被内容承接。
- **version**: 1.0.0
- **source**: Curis internal

### business_kpi_design  `运营`
- **description**: 设计商业指标体系与北极星。
- **target_role**: Strategy / Analyst
- **target_department**: 商业部
- **capability_instruction**: 专业知识——掌握指标分层（北极星/漏斗/护栏）与 OKR。工作方法——以因果关系而非虚荣指标选指标。执行流程——定战略假设 → 选指标与口径 → 设目标 → 搭看板。
- **recommended_tools**: [数据平台, 看板, OKR 工具]
- **output_standard**: 含指标体系、口径、目标；可驱动决策。
- **version**: 1.0.0
- **source**: industry SOP

### sales_enablement  `销售`
- **description**: 为销售提供培训、内容与工具赋能。
- **target_role**: Sales Enablement
- **target_department**: 商业部
- **capability_instruction**: 专业知识——掌握销售周期各阶段的内容与能力需求。工作方法——以缩短周期、提升胜率为目标。执行流程——盘能力差距 → 产培训/话术/案例 → 配工具 → 测效果。
- **recommended_tools**: [CRM, 知识库, 培训平台]
- **output_standard**: 含赋能资产与效果指标；可提升胜率/周期。
- **version**: 1.0.0
- **source**: industry SOP

### crm_management  `运营`
- **description**: 规范 CRM 数据与销售过程管理。
- **target_role**: Sales Ops
- **target_department**: 商业部
- **capability_instruction**: 专业知识——掌握销售漏斗、阶段定义与数据卫生。工作方法——以流程标准化提升可预测性。执行流程——定阶段与字段 → 规范录入 → 看板与预测 → 纠偏。
- **recommended_tools**: [CRM, 报表, 自动化]
- **output_standard**: 含阶段定义、字段规范、预测；数据可信。
- **version**: 1.0.0
- **source**: Curis internal

### financial_modeling  `财务`
- **description**: 搭建财务预测与情景模型。
- **target_role**: Financial Analyst / FP&A
- **target_department**: 商业部 / 财务部
- **capability_instruction**: 专业知识——掌握三线表联动、假设驱动与情景分析。工作方法——以假设透明、可敏感性测试为先。执行流程——定假设与驱动 → 建模型 → 跑情景 → 出结论。
- **recommended_tools**: [表格/模型工具, 财务系统, 数据平台]
- **output_standard**: 含假设、模型、情景与结论；可支撑决策。
- **version**: 1.0.0
- **source**: industry SOP

---

## 三、验收速览（Acceptance Overview）

### 各 Pack Skill 数量（均满足最低要求）
| Pack | 最低要求 | 实际数量 | 达标 |
|---|---|---|---|
| Pack A — AI 研发公司 Skill Pack | ≥50 | **52** | ✅ |
| Pack B — AI 内容运营 Skill Pack | ≥30 | **31** | ✅ |
| Pack C — AI 商业运营 Skill Pack | ≥20 | **22** | ✅ |
| **合计** | **≥100** | **105** | ✅ |

### 类别分布（categories）
- **Pack A**：产品(10) · 架构(9) · 开发(16) · 测试(6) · DevOps(8) · 数据(2) · 安全(1) — 共 7 类
- **Pack B**：内容分析(1) · 选题(2) · 内容策划(4) · 脚本(1) · 视频(2) · 设计(2) · 分发(3) · 数据分析(4) · 运营(4) · 文案(3) · 品牌(1) · SEO(1) · 直播(1) · 审核(1) · 投放(1) — 共 15 类
- **Pack C**：市场(2) · 用户研究(2) · 销售(2) · 商业计划(1) · 财务(3) · 定价(1) · 渠道(2) · 客户成功(2) · 增长(1) · 融资(1) · 竞争(1) · 运营(3) · 品牌(1) — 共 13 类

### source 分布（来源标注）
- **MetaGPT SOP**：10（需求/PRD/用户故事/竞品/验收/架构/API/DB/选型/API实现）
- **ChatDev workflow**：14（Debug/Refactor/编码-测试-评审-文档-容器-流水线-部署等）
- **CrewAI example**：11（选题/内容策划/文案/市场分析/用户研究/销售/竞品监控/达人合作/投放等）
- **AutoGen pattern**：2（架构评审 Group Chat、Code Review 多审评审）
- **industry SOP**：36（内容营销 7 步、GTM 八步、单位经济、财务建模、SEO、增长等）
- **Curis internal**：32（Curis 原生/通用研发与平台强绑定的交付规范）
- 合计：105（与总 Skill 数一致，每个 Skill 仅标注一个主来源）

### 红线核查
- ✅ 未开发 Skill Marketplace
- ✅ 未开发 Skill 交易
- ✅ 未修改 Workspace Runtime
- ✅ 仅建设 Admin 官方 Skill 资产库（本文件即资产库 v1 内容）
- ✅ 本阶段未写任何代码、未创建运行时源文件（除本 markdown 文档外）、未执行 git 提交（由主理人落盘与提交）

---

*文档状态：v1 Draft（Design Only）。后续如需扩展某 Pack，应保持"专业知识 + 工作方法 + 执行流程 + 工具建议 + 输出标准"五元结构，并在 source 字段如实标注来源。*
