# CURIS PRODUCT DERIVATION — ROUND 1 CORRECTION LOG

> Status: Draft（第一轮推导修正记录 · 供 CEO 核对）
> Authority Class: REVIEW — 记录"原结论为什么有问题 → 新结论是什么 → 为什么修改"；不修改任何 Authority。
> Updated: 2026-09-14 · 覆盖 CEO 指令 1–18 · 主文档与 GAP REGISTER 已同步回写。
> 关联：CURIS_PRODUCT_DERIVATION_REBUILD.md（修正已用 `ROUND 1 CORRECTION` 标记回写，原结论保留短注）；CURIS_PRODUCT_DERIVATION_GAP_REGISTER.md（Correction Status 列已加）。

## 修正总表

| ID | Original Conclusion（原结论） | Problem（为什么有问题） | Corrected Conclusion（新结论） | Impact（影响） |
|---|---|---|---|---|
| C-01 | Department = 编制归属，可属可不属（B·3.3） | 收口过早；未检验"职能归属/能力之家/共享能力中心"等可能 | **已证明的最小结论**：Department 现阶段仅被证明三件事——①承载部门级职责与 Assignment（原装两部门职责链挂部门范围：空间工程/数据分析对公司负责）；②员工的行政分组与组织呈现；③公司级支撑职能的组织容器。Department **不**限制跨业务服务、**不**授权能力、**不**是招聘前提。"Department=能力之家/职能矩阵"仅为 CANDIDATE → **DEPARTMENT–EMPLOYEE RELATIONSHIP — NOT YET FINAL** | 组织中心表述不依赖未证概念；V1 不建职能矩阵；Open Question 登记 |
| C-02 | "该范围的使用授权"写进 Assignment 字段（B·3.5） | 混淆组织任职与资源授权；授权变更频率高于任职（新增账号→新授权，不改任职） | **Assignment 与 Grant 拆开**：Employee → Assignment（范围×岗位×当前责任）→ Responsibility（声明所需能力与权限=授权需求）→ Grant（主体×范围×对象×动作，独立记录，可先于任职存在如公司级工具授权）；责任缺授权 = 诚实的"执行准备缺口" | G-09 语义成立；工位"运行准备卡"获得模型依据；CROSS-BUSINESS MODEL 收口句已改 |
| C-03 | 每员工一条正式"个人线 Identity Conversation"（B·3.6） | 证据不足；未验证独立持续对话与 Detail 问答哪个满足需求 | **降级 CANDIDATE**：需求（谈能力/负荷/成长/跨业务表现）成立；形态（A 独立对话 / B Detail+scoped / C 两者）**NOT FINAL**；已证主体仍是 scoped conversations。现行产品资料提及 Identity Conversation 的事实保留 | 对话类型清单不新增正式类型；Open Question 登记 |
| C-04 | Quick Access 六字段平铺（B·3.7） | 信息过载；未区分显示层级 | **CONVERSATION QUICK ACCESS INFORMATION MODEL**（只定优先级）：Primary 直接显示 = 员工+所属业务+注意状态（需要我/结果就绪/新消息/进行中）；Secondary 弱化 = 最新 Topic/Work；Hover/展开 = 责任线、状态原因、时间、dismiss。主要第二层判定：**Topic/Work 优先于 Responsibility**（快捷区首要任务是"恢复刚才在谈的事"；责任线是稳定背景） | G-01 → REFINED；不画 UI |
| C-05 | Employee Detail 四段平铺：身份→任职→能力→结果（B·3.8） | 有变成"员工后台大页"的风险 | **首层** = 身份 + 任职列表（各线：业务/岗位/当前责任/状态）+ 能力摘要；**折叠/次层** = 履历、完整能力、历史结果、配置；**从任职线进入** = 该线对话/工作/结果。Detail 只回答"是谁/在哪负责什么/能力如何"；保持 Conversation-first（Detail 永不承载对话） | G-02 → REFINED；Detail 范围收敛 |
| C-06 | External Agent = Capability Provider（与 Model 平级一类，C·4.1⑤） | 把"谁提供能力"与"是否有自主执行生命周期/自带工具与环境"压成一层；GPT API 与 Codex 是不同物种 | **五层拆分**：Capability（能做什么）/ Provider（谁提供：**Model Provider** 或 **Agent Runtime Provider**）/ Agent Runtime（自主执行生命周期——Runtime Provider 的属性）/ Execution Environment（在哪执行——属性）/ Tool Access（能调用什么——属性）。**Codex/Zcode/Claude Code = Agent Runtime Provider；GPT API 类 = Model Provider**；Curis 不重建，经 Adapter 消费真实项 | G-04 按此细化；Registry/健康/授权字段按 Provider 类型区分 |
| C-07 | 多 Provider 协作只发生在不同步骤（串行）（C·5.3） | 过窄；排除并行/对比/候选/验证等真实形态 | 支持 **Sequential / Parallel / Review / Compare / Candidate generation / Verification**；结构 = Work → Execution（可多个）→ Executor（员工或系统自动化）+ Provider + Contribution（具体贡献部分）+ Status；Result 由可归因贡献组成（含候选选用记录）。核心不是"必须串行"，而是**每一份执行贡献可追踪、可追责** | 执行记录从"步骤链"改为"贡献归因" |
| C-08 | Result 属于 Employee（C·5.5） | 自动化 Work（无员工）无法表达，除非伪造员工；多员工协作归属含糊 | **Result ∈ Work ∈ Business**；Employee = Responsible Producer（责任产出者，可为"系统自动化"——用 System Activity 表达，不造假员工）；Executor/Provider = 实际执行者（执行记录归因）。四场景压测：单员工单 Provider ✓ / 单员工多 Provider ✓ / 多员工协作 ✓ / 自动化 Work ✓ | Result 字段模型修正；与 P3 System Activity 兼容 |
| C-09 | Provider/参数/成本/哈希放 Evidence（C·5.6） | Evidence 变 Runtime Debug Panel；用户证据与技术审计混层 | **两层但关联**：Evidence（用户层：发布回执/测试通过/外部链接/平台数据/审核记录）与 Execution Audit / Technical Trace（技术层：Provider/Model/Tool/成本/哈希/时间/环境，默认折叠=Blueprint L4）；经 Result↔Execution 关联；Audit 喂养用量账 | CEO 看到的证据保持纯净；审计能力不丢 |
| C-10 | "获得≠接入≠授权≠使用≠记账"只是放置原则一句话（C·3） | 未成正式模型；缺 Install/Bind/Observe/Disable | **CAPABILITY LIFECYCLE**：`Discover → Acquire/Install → Connect → Authorize → Bind → Use → Observe/Cost → Disable/Remove`。四类验证：Model ✓ / Skill ✓（Connect 可 N/A）/ External Agent ✓ / Connector ✓（Acquire 可 N/A）。每步有入口与诚实状态；放置按 A.4 规则 | 放置规则从口号变检查单；G-05 依赖此模型 |
| C-11 | 竞品账号与自己的账号都用 Account 语言（D.2） | 污染后续模型：竞品对象绝不能有 Connection/Grant/对外动作 | **两类对象**：**Owned/Operated External Object**（实际经营、可执行：自己的账号/Store/Repo；可有 Connection、Grant、动作记录、一方数据）与 **Observed External Entity**（只读观察：竞品账号/店铺/产品；只有平台画像+公开快照，必带来源与新鲜度；**绝不能有** Connection/Grant/动作记录）。共享仅：平台、公开画像、公开指标（出处不同） | 权限模型不被观察对象稀释；D.2 描述已改 |
| C-12 | 发布前强制 Review；发布一律高风险（D.3/D.4 10.10） | 一刀切把 CEO 变审批机器人（违背 P4 与"日均动作<3"） | **ACTION RISK & REVIEW MODEL**：Review/审批需求 = 业务政策 × 动作类型 × 账号状态 × 员工授权级 × 规模（批量升级）× CEO 偏好；三档：**自动执行（留痕）/ 执行前 Review（审核责任者把关，非 CEO）/ CEO Decision（不可逆/大额/首次新渠道/敏感/批量超阈值）**；新账号首次动作默认升一档 | 10.10/10.11 修订；CEO 注意力保护；G-09 的 Constraints 字段有依据 |
| C-13 | 账号默认归 Business，少数 Company 共享（G-07/10.4/10.5，P0） | 官方账号/Repo 多业务共用时 Model A 需搬家或复制；业务关闭时对象失家；与现行 Authority 冲突 | **采用 Model B**：**External Object 身份/所有权登记在公司层；Business 通过 Operating Binding 获得经营权**（通常一个对象一条活跃 binding；用户看到的"这门生意的账号"=当前 binding 的表述投影）。七维比较（简单性/共享/权限/历史/转移/业务关闭/审计）Model B 全胜或平；**与现行 Authority（Company 资产经 Binding 服务）一致——推导收敛到权威，无需改 Authority** | G-07 → **RESOLVED**；10.4/10.5/E·15 已改写；业务关闭/转移语义干净 |
| C-14 | 平台规则归 Platform 层（10.6，未提来源/新鲜度） | 规则会变；旧规则让专业现场按过期约束工作 | **Platform Rule 必带 Source / Updated At / Verification state（已验证/声称/已过期）/ 适用范围（地区/账号类型，若适用）**。判定："事实带来源与新鲜度"是 COMPANY OS 通用 Truth 原则；**规则库本身属 Platform Capability Facts / Channel Registry（INFRA 层）** | 频道档案字段要求明确 |
| C-15 | 授权类型列表含 MCP（10.8：OAuth/API Key/MCP/Connector…） | MCP 是集成/工具协议，不是认证授权方式；前后不一致 | **两层**：认证/授权方式 = OAuth、API Key、本地会话、人工确认；集成/工具协议 = MCP、REST API、本地工具桥、连接器。一条连接 = 一种授权方式 + 一种或多种协议 | Connection 字段模型修正；10.8 已改写 |
| C-16 | Action Grant = 员工×外部对象×动作 三元组（G-09/10.9） | 缺范围/期限/审批要求/风险级/来源，表达不了"自动授权到期""需审批生效" | **ACTION GRANT MINIMUM SEMANTICS**：`{Subject, Object, Action, Scope, Effect, Constraints(风险级/政策), Expiry, Approval requirement, Source(CEO/负责人/策略默认/继承), Status(active/revoked/expired)}`。示例：林墨×小红书官方号×publish×内容业务×日常自动×到期随任职×CEO 授予；开发员工×Repo×merge×需审批 | G-09 → REFINED；语义先行，不设计 UI |
| C-17 | "Publication-like Record"（G-06） | 内容业务化命名；共性未推清就命名 | 四案例（内容发布/电商上架/软件 Deploy/小说章节发布）推出共性骨架：**Intent → Action → External Target → Execution → Receipt → State（已计划/执行中/成功/失败/已撤回，含"已发生不回滚"）→ Metrics/Feedback**——七段全部跨业务成立；专业对象保留为实例：Publication/Listing/Deployment/Chapter Release。通用命名（External Action vs External Operation）**待 CEO 选定** | G-06 → REFINED；Evidence 层获得统一承载结构 |
| C-18 | G-12 停在表达层 | 未分类记忆、未给可携规则 | **MEMORY PORTABILITY MODEL — DRAFT**：四类记忆——①Employee Personal Experience（默认可跨、显式注入、禁带业务数据）②Business Knowledge（业务私有，禁跨）③Client/Account Sensitive Context（最严：仅当前 Operating Binding 上下文内，禁跨业务/账号，不入个人经验）④Responsibility-specific Memory（默认不跨；有共性价值时经脱敏提炼升级为公司知识/方法，需 Leader 提出+CEO 确认=公司级学习入口）。Open Questions：①"不含业务数据"的自动判定标准；②升级提炼由谁执行 | G-12 → REFINED（仍含 Open Questions）；为第二轮公司学习铺路 |

---

## 跨业务复验（Round 1 修正后，CEO 指令 22）

判定规则：至少两个完全不同业务通过才标 **CROSS-BUSINESS VALIDATED**。

| 共性抽象 | 内容增长 | 研发 RD | 电商 | 小说 | 判定 |
|---|---|---|---|---|---|
| Employee 跨业务身份与任职线 | ✓ | ✓ | ✓ | ✓ | **CROSS-BUSINESS VALIDATED** |
| Assignment（任职，独立于授权） | ✓ | ✓ | ✓ | ✓ | **VALIDATED** |
| Permission / Grant（独立记录+最小语义） | ✓ 发布权 | ✓ merge/deploy | ✓ 上架权 | ✓ 发布权 | **VALIDATED** |
| External Object + Operating Binding（Model B） | ✓ 内容账号 | ✓ Repo | ✓ Store | ✓ 连载账号 | **VALIDATED** |
| Provider（Model Provider vs Agent Runtime Provider 分层） | ✓ 写作/图像模型 | ✓ 模型+Codex | ✓ 文案模型 | ✓ 写作模型 | **VALIDATED** |
| External Agent（Agent Runtime Provider） | ✓ 研究/视觉验证 Browser Agent（较弱） | ✓✓ Codex 强需求 | △ 运营自动化（弱） | △ | **VALIDATED**（RD+内容两业务成立；电商/小说弱需求如实标注） |
| Result ∈ Work + 责任产出者 + 执行归因 | ✓ | ✓ | ✓ | ✓（含自动化取数） | **VALIDATED** |
| Evidence（用户层）vs Execution Audit（技术层） | ✓ 发布回执 | ✓ 测试报告/构建日志 | ✓ 订单回执 | ✓ 发布记录 | **VALIDATED** |
| Action Grant 最小语义 | ✓ | ✓ | ✓ | ✓ | **VALIDATED** |
| Connection（授权方式×协议 两层） | ✓ | ✓ | ✓ | ✓ | **VALIDATED** |
| Memory 四类可携性 | ✓ | ✓ | ✓ | ✓ | **VALIDATED（DRAFT，含 2 个 Open Questions）** |
| Capability Lifecycle | ✓ | ✓ | ✓ | ✓ | **VALIDATED**（Skill/Connector 有 N/A 步） |

---

## 第一轮修正完成自检（CEO 指令 23）

- **Employee**：这个人是谁（稳定身份：人+能力清单+个人经验）→ 在哪些 Business 服务（任职列表）→ 每条线负责什么（Assignment + Responsibility）→ 被允许使用什么（Grant，独立记录）→ 当前在做什么（各线 Work/状态）。**五问互不打架 ✓**
- **Capability**：会什么（能力清单）→ 由什么 Provider 提供（Model Provider / Agent Runtime Provider）→ 在哪接入（Settings，Lifecycle 的 Connect 步）→ 谁被允许用（Binding + Grant）→ 本次 Work 到底用了什么（Execution 记录 + Execution Audit）。**一致 ✓**
- **External Object**：对象是谁的（公司层身份）→ 哪个 Business 正在经营（Operating Binding）→ 谁可以对它执行什么（Action Grant）。**一致 ✓**
- **Result**：属于哪个 Work/Business（Result ∈ Work）→ 谁负责（Responsible Producer，可为系统）→ 谁实际执行（Execution/Provider 归因）→ 什么 Evidence 证明真实（用户层证据，Audit 分层）。**一致 ✓**
- **Context**：什么可跨（个人经验，显式注入）→ 什么必须隔离（业务知识/账号敏感/任职线记忆）→ 什么需批准（记忆升级为公司知识、批量导出）。**一致 ✓**

**判定：ROUND 1 CORRECTION COMPLETE — 待 CEO 确认 "ROUND 1 CORRECTED" 后进入第二轮。**

仍未定义清单（不阻塞第二轮，带题进入）：
1. Department–Employee 完整关系（C-01：NOT YET FINAL）；
2. Identity Conversation 形态（C-03：CANDIDATE）；
3. 对外动作共性结构的通用命名（C-17：External Action vs External Operation 待选定）；
4. 记忆升级的执行者与"不含业务数据"判定（C-18 Open Questions）；
5. 通知/待处理独立结构（第一轮遗留 G-03）。

## ROUND 2 CORRECTION NOTES（2026-09-14 · CEO 6 点窄幅修正涉及本文件的 3 条）

- **C-01（Department–Employee）**：员工侧关系由 CEO 确认**关闭**——Employee Identity 在 Company 层唯一；AI Employee 不要求唯一 Department/Business 归属，可同时出现在多个 Department/Business/Team 节点，每次出现=独立 Assignment/Responsibility，不复制 Employee；Employee Directory 表达"人"、Business/Organization Map 表达"组织关系"。仅剩"Department 本身承担什么公司级职责"待场景推导（OPEN）。
- **C-13（External Object Binding）**："通常一条活跃 binding"修正——通常一条 **Primary Operating Responsibility**（谁对对象整体经营负责）；**Business Usage Binding 可多条**（公司官方账号、共享 Repo 可被多业务合法共用）；各业务视图=按动作发起归因过滤的投影；Ownership（公司层）与 Employee Action Grant（正交）不变。
- **C-17（对外动作骨架）**：骨架收窄为六段通用核心 `Intent → Action → External Target → Execution → Receipt → State`；**Metrics/Feedback 移出动作骨架**——它属于动作之后的业务反馈层（专业对象**引用**动作，可迟到/人工/缺席），不为统一强绑。

（ROUND 1 CORRECTION 完 · STOP FOR CEO REVIEW）
