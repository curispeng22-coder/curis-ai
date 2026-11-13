# CURIS CONTENT GROWTH — FULL PRODUCT CAPABILITY DERIVATION

> Status: Draft（内容增长完整产品能力推导 · 供 CEO / ChatGPT 核对）
> Authority Class: REVIEW — 站在普通用户真实经营角度推导"可建立、可操作、可理解、可持续、可恢复"所需的全部产品能力；不决定页面/导航/Four-Pane/UI。
> Updated: 2026-09-14 · 首轮 88 项 + 对抗反证补漏 7 项 = 95 项 · STOP FOR CEO / CHATGPT REVIEW
> 上游：CURIS_CONTENT_GROWTH_BUSINESS_LOGIC_V2.md（ACCEPT WITH 4 CORRECTIONS）· Method V2 · Capability Ledger CAP-001~023 · Gap Register G-01~G-31。
> 级别：**CORE**（没有它业务无法正常经营）/ **OPERATING**（不影响开业但长期经营明显需要）/ **EDGE**（特殊场景）。
> 置信：**VERIFIED**（真实业务强推出）/ **STRONG**（证据充分但有设计选择）/ **CANDIDATE**（可能需要）。
> 归属原则：**ONE CAPABILITY OWNER — MULTIPLE CONTEXTUAL ENTRY POINTS**（一个能力只有一个正式 Owner；业务上下文只放入口）。

---

# 1. 推导方法

视角：不问"需要什么对象"，只问"我经营这门业务时会遇到什么问题→Curis 怎样帮我完成/理解/判断/恢复"。每个业务环节继续追问到决策深度（示例：发布后取数据——有 API？没有 API？部分数据？谁填？在哪填？填累计还是周期？第二次覆盖还是新增快照？填错怎么改？改史保不保留？多久算 stale？来源怎么区分？没数据显示 0 还是 Unknown？源失效怎么提醒？分析怎么知道可信度？）。每能力检查六面：正常/替代路径/异常/长期使用/规模变化/用户错误。能力归属用"唯一 Owner+多上下文入口"防重复。第一轮完成后强制做 12 例对抗反证（A–L），二轮补漏不得只标 Future——正常经营必须的补进清单，纯 Edge 标 EDGE。

---

# 2. 首轮完整产品能力推导（最终清单，含反证补充标记 ⟲）

## 2A. 业务建立与经营基础
| ID | 能力（用户语言） | 级别 | 置信 | Owner | Context 入口 |
|---|---|---|---|---|---|
| PC-001 | 创建 Content Growth 业务（说意图→提案→确认） | CORE | VERIFIED | Business Management | 工作台/助理对话 |
| PC-002 | 定义目标与成功定义（约束/预算/停止条件） | CORE | VERIFIED | Business | 业务设置/对话 |
| PC-003 | 制定与调整 Strategy（打法，版本化） | CORE | VERIFIED | Business | 业务/对话 |
| PC-004 | 平台组合策略（选平台/定角色/投入级别/退出休眠） | CORE | VERIFIED | Business Strategy | 业务设置/洞察入口 |
| PC-005 | 经营责任分配与调整（责任覆盖，员工数量可变） | CORE | VERIFIED | Business Team | 团队视图/对话 |
| PC-006 | 周期性内容规划（月度目标→周计划→组合→库存水位） | CORE | STRONG | Business Planning | 业务现场/节奏触发 |
| PC-007 | 业务预算与超限政策（硬停/降级/仅提醒） | OPERATING | STRONG | Business 设置 | 预算页/通知/发起处 |
| PC-008 | 业务经营事实面（五类事实分层） | CORE | STRONG | Business | 业务第一面 |

## 2B. 平台
| PC-009 | 平台能力事实档案（形态/规则/来源/更新时间/验证状态） | CORE | STRONG | Platform Facts | 适配现场/业务 |
| PC-010 ⟲ | 平台自动化能力范围显示（哪些环节可自动/需人工） | OPERATING | STRONG | Platform Facts | 连接页/适配/发布 |
| PC-011 | 平台官方后台入口（创作者中心/开发者后台/活动中心/规则页/申诉/认证/商业化 Deep Link+最后访问记录） | OPERATING | STRONG | Platform Facts | 账号面/业务 |
| PC-012 | 平台规则变化感知与影响评估（公告入口/手动确认 VERIFIED；自动监测 CANDIDATE；变化→受影响账号/未发内容/计划提示） | OPERATING | STRONG | Platform Facts+Leader | 通知/业务 |
| PC-013 ⟲ | 规则变化后未发内容重新校验 | OPERATING | STRONG | 发布准备 | 队列 |
| PC-014 | 平台能力下线/地区差异/账号类型差异记录 | EDGE | CANDIDATE | Platform Facts | 档案 |

## 2C. Account（长期经营单元）
| PC-015 | 添加账号（选平台→身份→连接引导） | CORE | VERIFIED | Business | 账号列表 |
| PC-016 | 连接/重连/断开/换方式（OAuth/API/浏览器/人工） | CORE | VERIFIED | Settings/Connections | 业务失败提示直达 |
| PC-017 | Account Strategy 编辑（定位/受众/语气/结构/节奏） | CORE | VERIFIED | Account | 账号经营面/对话 |
| PC-018 | 账号成长阶段管理（冷启动→成长→成熟→衰退） | OPERATING | STRONG | Account | 账号面 |
| PC-019 | 账号责任归属与调整（可一人多项/多人分摊） | CORE | STRONG | Business Team | 账号面/团队视图 |
| PC-020 | 账号暂停/恢复经营 | OPERATING | VERIFIED | Account | 账号面 |
| PC-021 | 账号转移/共享（多 Business Usage Binding） | OPERATING | STRONG | Company | Settings/业务 |
| PC-022 | 账号健康一览（连接/限流/违规/封禁/数据新鲜度） | CORE | STRONG | Account | 账号列表/事实面 |
| PC-023 | 账号异常处理（限流排查/违规整改/封禁应对——资产保留/迁移） | OPERATING | STRONG | Account | 账号面/通知 |
| PC-024 | 账号时间线与最近变化（内容/数据/异常/策略） | OPERATING | STRONG | Account | 账号面 |
| PC-025 | 账号生命周期查看（策略变更史/阶段史/异常史） | OPERATING | STRONG | Account | 账号面 |
| PC-026 | 多账号列表与按平台筛选 | CORE | VERIFIED | Business | 账号列表 |
| PC-027 ⟲ | 账号分组/标签（20 账号规模才需要） | EDGE | CANDIDATE | Business | 账号列表 |
| PC-028 | 跨账号比较（数据/趋势对比） | OPERATING | STRONG | Operating Intelligence | 业务/洞察 |
| PC-029 | Account Identity 与 Connection 区分表达（换连接不改身份/历史） | CORE | VERIFIED | 原则 | 账号面/连接页 |
| PC-030 ⟲ | 重复添加检测（同平台同账号） | OPERATING | STRONG | Business | 添加流程 |

## 2D. 内容生产
| PC-031 | 选题管理（记录/信号转/批量/淘汰） | CORE | VERIFIED | 内容工作面 | 现场/对话 |
| PC-032 | 选题库存与安全水位（防断粮） | OPERATING | STRONG | Planning | 规划面/STATE 提示 |
| PC-033 | Brief 创建与引用 | CORE | VERIFIED | 内容工作面 | 选题行 |
| PC-034 | 生产委托与对话调整 | CORE | VERIFIED | Conversation/Composer | 工位 |
| PC-035 | 本次执行切换（模型/Agent，本次生效） | CORE | VERIFIED | Composer | 执行选择器 |
| PC-036 | 停止与运行中干预（Steering） | OPERATING | STRONG | Conversation | 运行中行 |
| PC-037 | 视觉生产（图像 Provider，依赖 G-31） | CORE | STRONG | 员工能力 | 对话 |
| PC-038 | 平台适配 Variant 生成（Platform Form × Account Context） | CORE | VERIFIED | 发布准备 | 发布流 |
| PC-039 | Variant 追加/移除（后补账号/某账号不需要） | OPERATING | STRONG | 内容包 | 内容包 |
| PC-040 | Variant 重新生成/差异查看/Final 标注 | OPERATING | STRONG | 内容包 | Variant 列表 |
| PC-041 | 旧内容翻新（更新版/续集） | OPERATING | STRONG | 内容包/素材 | 归档内容 |
| PC-042 | 内容归档（定稿归档/已发归档） | OPERATING | STRONG | 内容包 | 内容列表 |

## 2E. 素材资产
| PC-043 | 素材库（收集/上传/AI 生成入库） | OPERATING | STRONG | 内容工作面 | 生产引用 |
| PC-044 | 模板库（封面/脚本结构/排版） | OPERATING | STRONG | 内容工作面 | 生产引用 |
| PC-045 | 品牌素材与规范（logo/色/字体/口径） | CORE | STRONG | Business/Knowledge | 生产引用 |
| PC-046 | 版权红线标注与发布前检查 | OPERATING | STRONG | 素材+发布 | 素材/发布流 |
| PC-047 | 素材引用溯源（一份素材被哪些内容用过） | OPERATING | STRONG | 素材 | 素材详情 |

## 2F. 审核与发布
| PC-048 | 发布政策设置（内容类型×账号→三档） | CORE | VERIFIED | Business | 业务设置 |
| PC-049 | 审核执行（批/驳/改；待审队列） | CORE | VERIFIED | 内容现场/通知 | 待审项 |
| PC-050 | 排期与发布（多账号/日历/立即） | CORE | VERIFIED | 发布队列 | 内容包 |
| PC-051 ⟲ | 排期改期/换账号/受阻处理 | OPERATING | STRONG | 发布队列 | 队列行 |
| PC-052 | 逐账号回执与部分成功处理 | CORE | VERIFIED | 发布队列 | 队列行 |
| PC-053 | 失败重试/换通道 | CORE | VERIFIED | 队列行 | 队列行 |
| PC-054 ⟲ | 人工代发与回执回填（无 API 通道：Curis 备齐→用户贴发→回填链接为回执） | CORE | VERIFIED | 发布流 | 队列行/Variant |
| PC-055 | 发布队列聚合查看（按账号/状态） | OPERATING | STRONG | 发布队列 | 队列 |
| PC-056 | 平台删除已发内容（新对外动作+确认） | OPERATING | VERIFIED | 队列/内容包 | 已发行 |
| PC-057 ⟲ | 账号不可用时排期内容改派建议 | OPERATING | STRONG | 发布队列/Leader | 队列受阻行 |

## 2G. 数据（专项深推见 §7）
| PC-058 | 自动采集（API/Connector 可用时） | OPERATING | STRONG | Connections+采集 | 业务表现 |
| PC-059 | Browser 采集（无 API，授权档位内） | OPERATING | STRONG | 采集 | 表现 |
| PC-060 | 手工录入（该平台原生指标的周期快照） | CORE | VERIFIED | 表现缺口行 | 表现 |
| PC-061 | CSV/文件导入 | EDGE | CANDIDATE | 表现 | 表现 |
| PC-062 | 截图/文件作为人工数据凭证（Evidence） | OPERATING | STRONG | 录入流程 | 录入 |
| PC-063 | 数据 Snapshot 与时间序列（累计值自动差分为周期值） | CORE | VERIFIED | 数据层 | 表现/分析 |
| PC-064 | 数据修正与修改历史（人工可改且留原值；自动数据不可手改） | OPERATING | VERIFIED | 数据行 | 表现 |
| PC-065 | 数据来源区分（API/Browser/人工/导入，逐条带 Source） | CORE | VERIFIED | 数据层 | 全部数据面 |
| PC-066 | Freshness/Stale 政策（按平台节奏默认阈值可配） | CORE | STRONG | 数据层/业务 | 表现/分析 |
| PC-067 | Unknown/部分缺失表达（未到时间/未连接/未录入/源失效四因区分，≠0） | CORE | VERIFIED | 数据层 | 全部数据面 |
| PC-068 | 多来源数据冲突处理（并排+裁决） | EDGE | CANDIDATE | 数据层 | 表现 |
| PC-069 ⟲ | 人工修正与自动数据并存（不覆盖，标注分析采用哪个） | EDGE | STRONG | 数据层 | 表现 |
| PC-070 | 数据失效提醒（源断/采集失败→告警+重试） | OPERATING | STRONG | 通知/事实面 | 事实面 |
| PC-071 | 分析引用数据的可信度呈现（来源/新鲜度/样本） | OPERATING | VERIFIED | 洞察/报告 | 报告 |

## 2H. 互动
| PC-072 | 互动流查看（按账号聚合） | OPERATING | STRONG | 业务现场 | 互动 |
| PC-073 | 回复（拟/政策/发送对外动作） | OPERATING | STRONG | 互动行 | 互动 |
| PC-074 | 互动转机会/选题 | OPERATING | STRONG | 互动行 | 互动 |
| PC-075 | 敏感互动升级 | OPERATING | STRONG | 互动行 | 互动 |

## 2I. 分析与实验
| PC-076 | 分析报告与追问 | CORE | VERIFIED（已实现） | Operating Intelligence | 业务 scoped 入口 |
| PC-077 | 跨账号比较分析 | OPERATING | STRONG | 洞察 | 业务/洞察 |
| PC-078 | 增长实验记录（假设/设计/结果/结论→Learning） | OPERATING | STRONG | 复盘/业务 | 数据/复盘 |
| PC-079 | 实验可信度标注（对照实验 vs 经验尝试） | EDGE | CANDIDATE | 实验 | 实验记录 |

## 2J. Learning
| PC-080 | 复盘结论落地（应用到打法/账号/员工，勾选确认） | OPERATING | VERIFIED | 复盘 | 复盘 |
| PC-081 | Learning 升级公司知识（两级确认） | OPERATING | STRONG | 复盘→Knowledge | 复盘 |
| PC-082 | Learning 浏览与追溯（当初为什么这么做） | OPERATING | STRONG | 业务/Knowledge | 业务 |

## 2K. Employee / Conversation
| PC-083 | 找到在工作的员工（按业务/账号过滤+谁需要我） | CORE | VERIFIED | Conversation Quick Access | 侧栏/业务 |
| PC-084 | 对话中当前 Account Context 标识（本次服务哪个账号） | OPERATING | STRONG | Conversation | 对话头/Composer |
| PC-085 | 同一员工多 Work 并行查看 | OPERATING | STRONG | 工位 | 员工行 |
| PC-086 | 员工默认能力管理（长期可用什么） | CORE | VERIFIED | Employee Management | 工位缺口入口 |
| PC-087 | Result 回到账号经营上下文（产出↔账号关联） | OPERATING | STRONG | Result/内容包 | Result |

## 2L. 新用户与长期经营
| PC-088 | 首次业务引导（平台差异理解/选平台——对话式+事实卡片，非强制向导） | OPERATING | STRONG | 工作台/业务 | 首次进入 |
| PC-089 | 首次账号添加与连接引导（需要准备什么就地提示） | CORE | VERIFIED | 账号添加 | 添加流 |
| PC-090 | 首次内容到发布引导（第一次完整链） | OPERATING | STRONG | 业务 | 首次生产 |
| PC-091 | 责任与员工补充引导（缺口诚实+入口） | OPERATING | STRONG | 团队 | 团队视图 |
| PC-092 | 历史内容/决定检索 | OPERATING | STRONG | 搜索 | 全局/业务 |
| PC-093 | 策略版本对比与回看（当初为什么） | OPERATING | STRONG | Strategy | 打法历史 |
| PC-094 ⟲ | 停用对象归档与恢复（删除=归档可恢复；真删需确认+不可逆说明） | OPERATING | VERIFIED | 各对象 | 对象菜单 |
| PC-095 | 数据膨胀治理（旧数据归档/聚合） | EDGE | CANDIDATE | 数据层 | 设置 |

⟲ = 对抗反证轮补充（7 项：PC-010/013/027/030/051/054/057/064/069/094 中，010/013/027/030/051/054/057/069/094 共 9 项含反证深化；其中全新能力 7 项：010/013/027/030/051/054/057，见 §14）。首轮 88 项，二轮补漏后 95 项。

---

# 3. 平台专项

平台在用户眼里是"有规则、有能力、会变的外部舞台"。检查清单（指令 4）逐项落位：支持内容形态/发布规则→PC-009；规则来源与更新时间与验证状态→PC-009（来源=官方规则页/用户确认，验证状态=已验证/声称/已过期）；API/OAuth 能力→PC-009/010（决定哪些环节自动）；创作者中心/开发者后台/活动中心/激励/商业化/公告/申诉/认证→PC-011 官方 Deep Link+最后访问记录；能力下线/地区差异/账号类型差异→PC-014（EDGE）。规则变化后的影响评估→PC-012：变化事实→受影响账号（该平台全部）→未发内容（PC-013 重新校验）→计划组合建议→通知 Leader→按政策产生 Work→重大组合变更须 CEO 确认。**Curis 自动获取 vs 官方入口的判定**：涉及身份/资金/申诉的操作永远跳官方（认证、商业化、申诉、提现）；可自动的只有公开规则与（未来）API 数据；规则变化自动监测标 CANDIDATE（可靠性存疑），手动确认入口 VERIFIED。

# 4. Account 专项（长期经营单元）

首添（PC-015/089）：选平台→账号身份→就地提示"需要准备什么"→连接引导。多账号管理（PC-026/027）：列表按平台筛选；规模大才要分组（EDGE）。Identity 与 Connection 区分（PC-029）：换授权方式/换密码不改账号身份与内容历史——表达上"这个账号"永远同一个。Account Strategy 编辑（PC-017）：定位/受众/语气/结构/节奏，对话提案或经营面 inline。责任归属（PC-019）：Business Leader 直接承担/一人多项/多人分摊；账号不能没人负责但不强制单一个人。暂停/恢复（PC-020）、转移/共享（PC-021，Usage Binding 多业务）、异常（PC-023：限流排查支持→违规整改记录→封禁=经营暂停+资产保留+迁移建议）、健康一览（PC-022）、时间线/最近变化（PC-024）、生命周期（PC-025）、重复检测（PC-030）、跨账号比较（PC-028，Owner=洞察）。**快速找到该账号最近的内容/数据/互动/Learning** = 账号时间线（PC-024）统一承载。

# 5. 内容生产专项（指令 7 深推）

什么时候选 Platform/Account：**选题时定平台与账号（计划组合已分配）→ Brief 带账号语境 → 生产按 Platform Form×Account Context → 发布前可追加/移除账号**（PC-038/039：可以一开始多选，也可以后追加；某账号不需要→移除该 Variant 留痕）。核心内容先生成还是按账号生成：由平台差异决定——同形态平台可先生成核心内容再适配；差异大平台按账号独立生成（业务逻辑 1.2 模式 A/B）。规则变化时旧内容：已发的不可改（事实），未发的进重新校验（PC-013）。Variant 重新生成（PC-040）、差异查看（版本并排）、Final 标注（每个 Variant 恰一个 Final，重生成后旧版留痕）。某账号需要完全不同内容→该账号走独立生产 Work（不是 Variant 而是新内容，同选题关联）。继续让 Employee 修改某一版本→在该 Variant 上发起对话（引用具体 Variant）。多版本归档→内容包统一归档（PC-042），版本历史随行。

# 6. Conversation / Employee 专项（指令 8）

从哪找到在工作的员工→Quick Access+业务过滤+谁需要我（PC-083）；同一员工跨业务→任职线标识（已有结论）；同一业务不同账号→**对话必须标注当前 Account Context**（PC-084——本轮新发现：不仅"哪门生意"，还有"哪个账号"）；同一员工多 Work→工位并行列表（PC-085）；哪个需要我→注意状态；当前 Composer 用什么→执行选择器（PC-035）；临时切换→本次生效；不可用→换执行者（CAP-008）；员工默认能力→员工管理（PC-086，Owner=Employee Management，工位只放入口）；当前 Work 为什么用了这个 Provider→执行归因记录；Result 出来→回到账号经营上下文（PC-087：产出自动关联内容包与账号）。

# 7. 数据专项（指令 2/9 逐问回答）

有 API→自动采集（PC-058，按平台节奏定时）；没有 API→两条替代：Browser 采集（授权档位内，PC-059）+手工录入（PC-060，主通道）；只能拿到部分数据→部分快照+Unknown 补齐原因（PC-067）；需要用户手动填→是（无 API 时），在哪填→业务表现页的数据缺口行（就地）；填哪些指标→该平台**原生指标**（定义来自平台事实档案 PC-009，最少集=曝光/互动/涨粉）；不同平台指标不同→原生指标按平台，分析层映射统一维度；多久填一次→按该账号发布节奏（发布后 48h/7d 的复盘点+周期点）；累计还是周期→**按平台后台习惯填累计值，系统由相邻快照差分出周期值**（也可直接填周期值，标注）；第二次填写→**新增 Snapshot**（时间序列 PC-063），绝不覆盖；填错→人工数据可修正且保留原值+原因（PC-064），修改历史保留；自动数据不可手改→不一致时添加人工修正值并标注分析采用哪个（PC-069，EDGE）；多久算 stale→按平台节奏默认阈值（如周更 7 天）可配（PC-066）；API/人工/Browser 数据区分→逐条 Source（PC-065）；没数据→Unknown（四因：未到时间/未连接/未录入/源失效），绝不 0（PC-067）；源失效→告警+事实面 Unknown+重试（PC-070）；分析可信度→报告引用带来源/新鲜度/样本（PC-071）；CSV 导入（创作者中心导出）→EDGE/CANDIDATE（PC-061）；截图/文件→人工数据的凭证 Evidence（PC-062）；多来源冲突→EDGE（PC-068：并排+裁决）。**判定：不需要为"数据"单独造一套系统——它是表现页的数据层+采集通道+诚实语义，Owner 分属 Connections（采集）与业务（录入/查看）。**

# 8. 外部后台 / 官方入口专项（指令 10）

判定规则：**涉及账号身份、资金、申诉、官方资质的动作永远跳官方**——认证、商业化后台、活动报名、提现、申诉；Curis 只提供 Deep Link+最后访问记录（PC-011）。用户什么时候跳出去：账号异常申诉、活动激励报名、官方规则确认、开发者权限申请。回来怎么继续：跳转前 Curis 记录来源上下文，返回后从原任务继续（返回契约）。外部处理完的事实（如违规已申诉）由用户在 Curis 标注/或下次采集反映。官方入口清单按平台维护在平台事实档案（PC-009/011）。

# 9. 新用户专项（指令 11）

"我要开始做小红书和抖音"→逐项检查：理解平台差异→事实卡片（小红书=图文+搜索流量、抖音=视频+推荐流量——一句话差异+产能要求）；选平台→平台组合提案；创建/添加账号→PC-015；连接→PC-016 引导；Account Strategy→对话提案补齐（不懂行业也能从模板起步）；节奏/责任/员工/能力→缺口诚实提示+入口（PC-091）；第一次选题→从信号/模板起步（PC-090 首次链引导）；第一次发布→走完整链+政策默认档（保守：首次发布建议确认）；第一次数据→录入提示+截图凭证。**不做强制 Wizard**：全部以"就地提示+缺口入口+对话可问"存在，用户可跳过任何引导（引导缺失不阻塞开业）。

# 10. 长期经营专项（指令 12）

3 个月～1 年：对象变多→检索（PC-092：旧内容/旧决定）+账号筛选（PC-026/027）；Strategy 改过多次→版本对比与回看（PC-093"当初为什么"）+Learning 追溯（PC-082）；Employee 变化→责任归属调整（PC-005/019）+历史不改写；平台规则变化→PC-012/013；历史账号停用→归档不删（PC-094）+休眠状态（PC-020）；Learning 越来越多→按范围浏览（PC-082）；素材越来越多→素材库+溯源（PC-043/047）；数据越来越多→归档/聚合（PC-095，EDGE）。**主动发现的长期能力**：策略版本对比（PC-093）、Learning 追溯（PC-082）、停用归档恢复（PC-094）——首轮遗漏，专项补齐。

# 11. 异常 / 恢复专项（指令 3 汇总）

授权过期→重连（PC-016）+受阻排期处理（PC-051）；平台发布失败→重试/换通道/人工代发（PC-053/054）；账号封禁→PC-023（资产保留+迁移）；数据缺失→PC-067/070；填错→PC-064；误删→PC-094（归档可恢复）；重复创建→PC-030；员工/Provider 不可用→CAP-008+责任临时调整；CEO 长期缺席→CAP-016 摘要。恢复原则：**失败以后从原任务继续，不是重新开始**——每个异常就地提供恢复入口，返回保留上下文。

# 12. Capability Owner 分析（指令 15）

| 能力 | 唯一 Owner | 业务上下文只提供 |
|---|---|---|
| 员工创建/管理 | Employee Management（人才+员工） | 缺口入口（"需要一名剪辑员工→去人才"） |
| Provider 接入 | Settings/Connections | Composer 只"本次使用"；业务只显示健康 |
| 账号 Connection | Settings/Connections | 业务显示状态+Reconnect 直达 |
| 账号经营 | Business（账号经营面） | Settings 不显示经营字段 |
| 深度分析 | Operating Intelligence | 业务只 scoped 入口，不复制报告 |
| 搜索/通知/缺席摘要 | 全局能力 | 各上下文只放入口 |
| 平台事实档案 | Platform Facts（Curis 维护+用户补充） | 各现场只读引用 |
| 学习升级 | Knowledge | 业务只发起 |

原则执行检查：本轮清单中无一项双 Owner；"渠道管理"旧页面概念被拆为 账号经营（Business）+连接（Settings）+平台事实（档案）三 Owner，不继承旧页。

# 13. Adversarial Product Review（12 例）

| Case | 情景 | 检查结果 |
|---|---|---|
| A | 没有 API | 手工录入（060）+Browser（059）+**缺口发现：人工代发发布**→新增 PC-054 ✓ |
| B | API 只支持部分功能 | 部分自动+部分手工混合→来源区分（065）+Unknown（067）✓；**缺口：用户需要知道"该平台当前哪些环节能自动"**→新增 PC-010 ✓ |
| C | 授权过期 | 重连（016）✓；**缺口：已排期内容受阻怎么办**→新增 PC-051（改期/换账号）✓ |
| D | 平台规则改变 | 感知与影响（012）✓；**缺口：未发内容重新校验**→新增 PC-013 ✓ |
| E | 经营 20 个账号 | 筛选（026）/比较（028）✓；重复检测（030）✓；分组（027，EDGE）登记 ✓ |
| F | 同一内容发 10 个账号 | Variant（038-040）+逐账号回执（052）+聚合（055）✓；部分自动部分人工适配（010）✓ |
| G | 账号被封 | 异常处理（023）✓；**缺口：该账号排期内容改派**→新增 PC-057 ✓ |
| H | 数据一个月没更新 | Stale（066）+失效提醒（070）✓；分析引用带可信度（071）✓；休眠账号状态（020）✓ |
| I | 手工数据填错 | 修正+历史（064）✓；**深化：自动数据不可手改→人工修正值并存**→PC-069 ✓ |
| J | 员工/Provider 突然不可用 | 换执行者（CAP-008）+责任调整（005/019）✓ |
| K | CEO 一个月没打开 | 缺席摘要（CAP-016）+策略变更线（093）+预算（007）✓ |
| L | 第一次用 AI 工具的新手 | 引导四件套（088-091）✓；内部词不进用户语言（原则）✓ |

# 14. 第二轮补漏（7 项新能力，全部进入清单）

PC-010 平台自动化能力范围显示；PC-013 规则变化后未发内容重新校验；PC-027 账号分组（EDGE）；PC-030 重复添加检测；PC-051 排期改期/受阻处理；PC-054 人工代发与回执回填（升 CORE——无 API 时这是唯一发布通道）；PC-057 账号不可用改派。另深化：PC-064/069（数据修正语义）、PC-094（删除=归档原则明确化）。**未发现需要推翻的既有能力。**

# 15. 最终 Product Capability Inventory（汇总）

- **总数 95**：CORE **36**（001-006、008、009、015-017、019、022、026、029、031、033-035、037、038、045、048-050、052-054、060、063、065-067、083、086、089）；OPERATING **52**；EDGE **7**（014、027、061、068、069、079、095）。
- **置信**：VERIFIED 41 / STRONG 45 / CANDIDATE 9。
- **全新发现（此前所有轮次未出现）**：平台自动化能力范围显示、官方后台 Deep Link+最后访问、规则变化后重新校验、排期受阻处理与改派、人工代发回执回填、数据快照/差分/修正历史语义、对话 Account Context 标识、策略版本对比"当初为什么"、删除=归档可恢复。
- **重复/合并**："渠道管理"旧概念拆为三 Owner；业务内 Dashboard 与洞察分工防重；通知/摘要/待决三分不重复建系统。
- **仅 Contextual Entry**：员工创建、Provider 接入、账号连接、深度分析、公司级预算总账。
- **无法确定（待 CEO）**：自动规则监测是否投入（可靠性）；CSV 导入优先级；实验可信度标注形态；数据膨胀治理时机；账号分组阈值。

---

# STOP GATE

已完成 15 节结构与 12 例对抗反证；翻译台账已增补（Owner/Context/Priority/Confidence 矩阵 + T-CG-027~050）。未进入 RD/Product Structure/Navigation/UI/HTML/Figma；未改 Authority。

**STOP FOR CEO / CHATGPT REVIEW**——等待判定 **CONTENT GROWTH PRODUCT CAPABILITY COMPLETE ENOUGH**；通过后进入 PRODUCT EXPERIENCE / INTERACTION DESIGN。

---

# PART II — COMPREHENSIVE PRODUCT DERIVATION（ROUND 3：从"完成内容生产"到"真正可经营"）

> 触发（CEO 指令）：95 项能力覆盖了"内容生产与发布任务"，但没有覆盖"经营"。账号的价值创造方式（带货/商单/激励/付费/直播/私域）、平台商业机会、成长阶段与机会联动、收益数据、能力覆盖透明度——这些才是长期经营的主循环。本轮含真实平台研究（抖音/YouTube/TikTok 已查证官方与行业源；小红书/B站 查证超时，按行业通行规则写入并标注"以官方后台为准"）。

## 16. 重新理解"经营账号"：Account Goal = 价值创造方式

用户经营一个账号，最终通过什么创造价值：**获得流量、建立品牌、获取客户（线索）、广告商单、商品带货、团购带货、平台激励、付费内容、直播、私域导流、商业合作**及平台特有方式。不同账号目的完全不同（官方号=品牌+线索；IP 号=信任+商单；带货号=佣金）。→ 涨粉/互动只是**信号**，不是目的。

**PC-096｜Account Goal（价值创造目标）**：每账号可设主目标+次目标（从上述价值方式选择），随成长阶段演进；Goal 决定该账号"什么数据重要、什么机会相关、什么内容该做"。级别 CORE / VERIFIED / Owner: Account / Context: 账号经营面·对话。**修正 PC-017**：Account Strategy 编辑包含 Account Goal。

## 17. 抖音深推案例（真实研究结论）

抖音一个创作者账号当前实际拥有的经营能力（查证来源见文末）：
- **内容与数据**：创作者服务中心（creator.douyin.com）——内容管理、互动管理、数据中心、授权管理；
- **商品带货**：商品橱窗/小黄车——开通条件＝账号正常+实名认证+**粉丝≥1000**+缴纳作者保证金；选品中心选品→视频/图文挂车→按成交佣金；
- **本地生活**：团购带货；
- **商单**：星图平台（xingtu.cn）——达人入驻（有粉丝分级门槛）→接品牌任务→结算；创作者服务中心内"星图商单"任务列表；
- **官方任务**：全民任务（无高门槛，任务广场参与赚现金）；
- **直播**：直播打赏+直播带货；
- **其他**：小程序/游戏推广等任务；中视频伙伴计划已进入调整期（以官方公告为准）；
- **付费推广**：DOU+/上热门（花钱方向——经营成本而非收益）。

**关键业务发现**：小账号（1000 粉）即可进入真实商业循环（橱窗佣金+全民任务），**不需要百万粉才开始"经营"**。这些不是 Edge，是账号经营主循环的一部分。

## 18. 小账号赚钱场景 → Account Operating Loop 扩展

真实日常（研究归纳）：打开创作者中心 → **查看可参与的变现机会**（任务/商品/活动）→ 看佣金/门槛/适配 → 筛选候选商品 → 研究相关热门内容 → 选定机会 → 制定带货内容 → 生成脚本 → 制作 → 发布 → 查看点击/成交/佣金 → 分析哪种商品/内容转化更好 → 下一轮继续筛选。
→ **Account Operating Loop 在"发布→数据"之间多了一整段"机会循环"**：机会发现→筛选→研究→内容→发布→收益→复盘。这不是"打开官方后台"的便利功能，是经营主循环（CEO 指令 3 确认）。

## 19. 大账号与成长阶段 × 机会联动

大账号经营重心上移：品牌商单（星图/花火/BrandConnect）、直播、自有商品、付费内容、品牌长期合作。**阶段×机会矩阵**（以查证门槛为例）：
| 阶段 | 可用机会（示例） | 经营重点 | 数据重点 |
|---|---|---|---|
| 冷启动（<1k 粉） | 抖音全民任务、TikTok Shop affiliate（1k 粉）、公众号流量主（低门槛） | 验证内容方向、求基线 | 完播/互动率、涨粉效率 |
| 成长（1k–10k） | 橱窗带货、蒲公英/星图视门槛、B站激励（≥1k 粉） | 放量+**测试变现** | 转化率、佣金、粉丝质量 |
| 成熟（10k+） | 星图/花火商单、TikTok Rewards/Series（10k 粉+100k 播放）、直播、自有商品、YouTube YPP 全档 | 商单/带货/商业化组合 | 收益结构、商单履约、ROI |
| 衰退/转型 | 机会收缩 | 转型或休眠 | 流失原因 |
→ **PC-097 账号变现资格与门槛跟踪**：各变现方式开通条件 vs 当前数据差距（"还差 400 粉可开橱窗"）——OPERATING/STRONG。**PC-098 成长阶段与机会联动**：阶段决定可用机会/建议关注/数据重点/动作——OPERATING/STRONG（**修正 PC-018**：阶段不是标签，是经营参数）。

## 20. 平台全面研究框架与首批 Platform 清单

**Platform 研究 14+ 维度**（指令 6）：Content（形态）/ Distribution（流量逻辑）/ Account（类型/等级/状态）/ Data（经营数据）/ Interaction（评论/私信/粉丝）/ **Monetization（变现）** / **Opportunity（活动/任务/激励/商品/团购/商单）** / Creator Tools / Developer Capability（API/OAuth/开放平台）/ Official Backends / Rules / Policy Change / Restrictions（地区/等级/认证/粉丝门槛）/ Failure & Risk（限流/违规/封禁/资格取消）。比"发布规则"多出的核心维度：**Monetization 与 Opportunity——本轮新增**。

**首批 Platform 清单**（按形态代表性/经营价值/商业化能力/数据能力/API 能力/Curis 可提供的经营价值，不按用户量排名）：
| 级别 | 平台 | 理由 |
|---|---|---|
| **Launch P0** | 小红书 | 图文社区代表；蒲公英商单+买手电商；获客与信任主阵地（查证超时，门槛以官方后台为准：蒲公英通行要求≥1000 粉） |
| **Launch P0** | 抖音 | 短视频代表；**商业闭环最全**（橱窗/星图/团购/全民任务/直播）——已查证 |
| **Launch P0** | 微信公众号 | 长文私域代表；流量主+付费内容+商业合作；信任沉淀与线索 |
| P1 | 微信视频号 | 短视频+私域联动（创作分成计划），与公众号同生态 |
| P1 | B站 | 中长视频社区；创作激励（≥1k 粉或播放）+花火商单+充电（查证超时，以官方为准） |
| P1 | YouTube | 海外长视频；最强广告/会员体系（YPP 两档已查证） |
| P1 | TikTok | 海外短视频；Rewards/Shop/Series 分层资格（已查证） |
| P1 | 今日头条/头条号 | 图文信息流；低门槛流量分成+商品卡 |
| Later | 知乎（专业问答）、快手（与抖音同构/直播电商重）、微博（热点分发弱经营）、播客（形态差异大）、百家号/网易号（经营价值低）、X（海外分散） | 进入理由不充分或与已有平台同构 |

## 21. 各平台"为什么经营它"（不可压成"发布+看数据"）

- **抖音**：流量入口+全链商业（佣金/商单/激励/直播）——查证 ✓
- **YouTube**：广告分成+会员+Super Thanks+Shopping+BrandConnect——查证 ✓
- **TikTok**：Rewards+Shop affiliate+Series 付费合集+LIVE——查证 ✓
- **小红书**：蒲公英商单+笔记带货/买手+搜索长尾获客——行业通行（待官方核对）
- **B站**：创作激励+花火商单+充电+付费视频——行业通行（待官方核对）
- **公众号**：流量主广告+付费文章+赞赏+私域线索
- **头条号**：流量分成+商品卡+付费专栏
→ **PC-106 平台经营维度档案扩展**：把 Monetization/Opportunity types/Account types 与门槛/Creator tools/Developer capability/Restrictions/规则变化史并入平台事实档案（**升级 PC-009**）。**PC-107 平台商业能力矩阵**：每平台各变现方式×开通门槛×该账号当前资格——OPERATING/STRONG。

## 22. Opportunity 重新验证：从 Insight 到 Actionable

平台商业机会证明：**Actionable Opportunity 是真实、持续、需要跟踪的经营事实**（某团购商品、某高佣商品、某平台活动、某商单——有来源/有效期/收益条件/适用账号/行动状态/结果），区别于研究里一句"值得关注"的 **Ephemeral Insight**。
→ 能力集：
**PC-099 机会发现与查看**（来源：官方后台人工确认/Browser/API）OPERATING/STRONG；
**PC-100 机会筛选/收藏/比较**（按账号适配/门槛/佣金/有效期）OPERATING/STRONG；
**PC-101 手动创建机会**（链接+条件+截图证据）OPERATING/STRONG；
**PC-102 机会→内容**（分配员工研究→选题→生产→发布→追踪）CORE/VERIFIED；
**PC-104 机会有效期与失效提示** EDGE/STRONG；
**PC-105 机会复盘**（哪个机会值得继续）OPERATING/STRONG。
（Ephemeral Insight 维持轻量，不对象化。）

## 23. 机会数据拿不到怎么办（沿用数据纪律）

平台常无 API 提供佣金/商单/活动数据：①Browser 采集（授权档位内）可行但标 CANDIDATE（反爬风险）；②**手动录入+截图凭证**为主通道（VERIFIED）；③只提供官方入口（选品/商单中心）；④收藏机会链接；⑤手动创建机会；⑥收益低频回填（月账单也合法——快照语义兼容）。

## 24. 官方入口与用户意图关联（不是链接集合）

**PC-115 意图关联官方入口**（**升级 PC-011**）：账号被封→申诉入口；想带货→选品中心；商单→星图/花火；规则疑问→官方规则页；数据→创作者中心/数据后台；活动→活动中心。入口跟随"用户此刻想做什么"，并保留**最后访问记录**与**返回原上下文**。

## 25. 规则变化检测分层（指令 13）+ 面向未来的信息结构

四层比较：**Manual Verification**（用户查看官方来源并确认——VERIFIED，零成本）→ **Cheap Detection**（官方公告 RSS/Feed/页面更新时间——OPERATING/CANDIDATE，低成本）→ **Browser Monitoring**（低频检测——CANDIDATE，反爬/稳定性风险）→ **AI Analysis（只在变化被检出后调用）**：解释变了什么/哪些账号受影响/哪些内容受影响/计划是否要调/是否值得改 Strategy——**AI 用来解释变化，不用来无变化巡检烧 Token**（原则 VERIFIED）。
**面向未来（指令 14）**：今天手动确认、明天自动发现——用户关心的信息结构不变：**当前状态/来源/最近验证时间/变化内容/影响/下一步**。PC-012 的字段即按此设计，未来切换检测层不改产品。

## 26. Platform Definition 可扩展 + 新平台进入方案（指令 15/16）

**PC-113 Platform Definition**（从真实平台归纳，非最终 Schema）：identity（含品牌中立 ID）/region/账号类型与等级门槛/content forms/原生 metrics/rules（来源+验证状态+历史）/monetization 方式与门槛/opportunity types/official links（按意图分类）/connection methods/automation capabilities（每能力档位）/restrictions/freshness 政策。
**新平台进入方案比较**：
| 方案 | 用户难度 | 适配质量 | 安全 | 更新 | 扩展速度 | 维护成本 | 建议 |
|---|---|---|---|---|---|---|---|
| Curis Official Built-in | 零 | 高 | 高 | Curis 负责 | 慢（排队） | 高 | **主通道（P0/P1 平台）** |
| User-defined Platform | 中（填表） | 低（仅通用能力） | 中 | 用户自理 | 快 | 低 | **轻量占位**（新平台先手动经营） |
| Connector-provided | 低-中 | 中 | 依赖第三方 | 第三方 | 快 | 低 | 未来 |
| Workspace Package | 中 | 中-高 | 中 | 打包方 | 中 | 中 | 长期方向 |
| Hybrid（内置+用户补充） | 低 | 高 | 高 | 混合 | 中 | 中 | **推荐组合**：内置平台+用户补充事实 |

## 27. Automation Maturity 与 Capability Coverage（指令 26/27）

**PC-108 平台/账号能力覆盖视图**：连接一个抖音账号后，用户必须能理解——当前 Curis 对这个账号：**可以自动发布？自动取数据？读评论？回复？读商单？读选品？哪些必须手工？哪些只能跳官方后台？**——这是 CORE 问题（用户不知道能做什么=能力不存在）。
**PC-109 自动化成熟度四档标注**：**MANUAL**（Curis 备齐，用户去官方完成）/ **ASSISTED**（提供入口+准备数据+回来回填）/ **AUTOMATED**（Connector/API/Browser 完成）/ **AUTONOMOUS**（员工在政策内持续执行并反馈）——每平台×每能力标当前档；用户可见、可预期。不是每项都到最高档；档位随平台能力与实现演进。

## 28. 收益数据与三层绩效（指令 28/29）

**PC-111 收益数据类型**：Revenue/Commission（佣金）/Order（订单）/Conversion（转化）/Leads（线索）/Deal（商单）/Incentive reward（激励）——按平台不同；归属三层：**Platform 原生指标**（播放/点赞/涨粉）、**Account 经营指标**（佣金/订单/商单/粉丝资产/转化）、**Business 级结果**（总收入/线索数/ROI）。来源仍是快照+Source 纪律（低频账单合法）。
**PC-112 三层绩效区分表达**：一条视频表现好≠账号经营好；账号涨粉≠业务赚钱；业务赚钱可能来自商单而非内容直接转化。用户在三层分别判断：内容层=这条内容行不行（完播/互动）；账号层=这个号在成长/变现轨道上吗（粉丝质量/收益结构/阶段目标）；业务层=内容投入在为业务创造什么（线索/收入/品牌）。**这决定后续表达：不能把三层压成一张排行榜。**

## 29. Account 日常/周/月经营深推（指令 17）与账号间共享隔离（指令 18）

每账号经营面回答：当前目标/当前策略/当前阶段/内容计划/发布节奏/内容表现/粉丝变化/互动/**Opportunity/Monetization/Revenue**/异常/Learning/下一步（PC-024 时间线承载）。账号间：内容可共享（多账号分发）、素材可共享、**Opportunity 按适用账号共享但行动按账号**、Learning 分层（账号 Learning 不自动共享；方法迁移=显式提炼，同 C-18 精神）；跨平台数据可比较但**必须标注不可比性**（平台指标不同）；**收益按账号分别记录**（PC-103），业务级只做汇总比较。

## 30. 95 项复检结果（指令 31）

逐项检查结论：**修正/升级 4 项**——PC-009（扩展经营维度）、PC-011（升级为意图关联入口）、PC-017（加入 Account Goal）、PC-018（升级为阶段×机会联动）；**扩展 3 项**——PC-058/059/060（收益数据类型并入数据层）、PC-031（机会驱动选题来源）、PC-024（承载商业信息）；**删除 0 项**；**新增 22 项**（见 §34）；其余 89 项复检通过（含 Owner/Context 复核）。诚实标注：机会/收益类能力的自动化成熟度目前多为 MANUAL/ASSISTED 档。

## 31. Product Expression Options 比较（指令 19–24；只比较方案，不画 UI）

**① 多账号管理**（1/5/20 账号测试）：
| 方案 | 适合 | 优 | 缺 | 规模表现 |
|---|---|---|---|---|
| List | 少量账号 | 简单直接 | 信息扁平 | 20 账号靠筛选 |
| Cards | 中量 | 扫描快 | 占空间 | 中 |
| Platform→Account Tree | 多平台多账号 | 层级清晰 | 点击深 | 20+好 |
| Context Selector | 聚焦单账号 | 上下文稳定 | 全局感弱 | 好 |
| Search | 找具体账号 | 快 | 不适合浏览 | 好 |
| **Hybrid（列表+树+选择器+搜索）** | 全部 | 各取所长 | 复杂度 | **推荐方向** |

**② Platform 表达**：独立列表+详情（重）/仅账号属性（轻）/Context Pane 事实（中）/Utility Facts（中）。倾向：**平台事实作为账号与业务的属性+事实档案按需打开**，不默认独立页面。
**③ 发布 Calendar**：单 Calendar+账号筛选 / Context Selector / Account lanes / Platform lanes / 层级 Calendar / **Calendar+Queue 组合**。20 账号时 lanes 爆炸→筛选+聚合是必需；失败/改期/暂停账号在 Queue 表达比日历自然。倾向：**Calendar（时间感）+Queue（执行感）组合，lanes 作为小规模可选**。
**④ 生产 Context**（Topic→Form→AccountContext→Variant）：先选 Platform/Account / 先核心内容 / Platform Tabs / Account Tabs / **Variant Matrix（选题×账号）** / Master+Variants / Hybrid。测试：单平台（Tabs 足够）、多平台（Matrix 清晰）、同平台多账号（Account Context 区分）、后追加（追加入口）、完全独立内容（独立 Work）。倾向：**Master 内容+Variant 列表（含矩阵视图选项）**。
**⑤ 数据表达**：查看=表现页快照流；补录=缺口行就地+批量录入表；修正=值旁历史；历史=快照时间线；来源=Source 标签；缺失=Unknown 四因。**功能保留，复杂交给设计简化**。
**⑥ Conversation 经营上下文**：Header（重）/Context chips（轻）/Breadcrumb（中）/Composer context（准）/标题（弱）/Hover（省）。倾向：**chips+Composer context 为主，Hover 展开**——不默认全显示。

## 32. 便利能力专项（指令 25：LOW COST / HIGH CONVENIENCE）

**PC-116 便利动作集**：打开已发内容（平台原文）｜打开账号主页｜复制账号 ID｜打开数据后台｜打开规则来源｜打开选品/商单中心｜返回 Curis 原 Context｜最近账号｜记忆上下文。每项成本极低、高频价值高；不都是 CORE，但清单登记防遗漏。

## 33. Adversarial Review Round 2（新 8 例）

| Case | 情景 | 检查结果 |
|---|---|---|
| M | 想带货但粉丝不够开通橱窗 | **缺口**：资格/门槛跟踪→PC-097（"还差 400 粉"）✓ |
| N | 激励活动结束 | PC-104 机会有效期与失效 ✓ |
| O | 商单在星图后台 | 官方入口（115）+手动/Browser 回填（103）✓ |
| P | 新平台突然爆火 | Platform Definition（113）+进入方案（114）✓ |
| Q | 官方号想兼做人设 | 一个账号一个定位（业务规则）；需要人设→另一账号 ✓ |
| R | 跨平台同主题表现差异大 | 跨平台比较必须标注不可比性（028/111）✓ |
| S | 收益只有月账单 | 低频回填+快照语义兼容（103/063）✓ |
| T | 先收藏一个还不确定的机会 | 机会收藏（100）轻量路径 ✓ |

# 34. 新增能力清单（PC-096 ~ PC-117，22 项）

| ID | 能力 | 级别 | 置信 | Owner |
|---|---|---|---|---|
| PC-096 | Account Goal（价值创造目标：品牌/获客/带货/商单/激励/付费/直播/私域/合作） | CORE | VERIFIED | Account |
| PC-097 | 账号变现资格与门槛跟踪（条件 vs 当前差距） | OPERATING | STRONG | Account |
| PC-098 | 成长阶段×机会联动（阶段决定可用机会/重点/动作） | OPERATING | STRONG | Account |
| PC-099 | 机会发现与查看（活动/任务/激励/商品/团购/商单） | OPERATING | STRONG | Business/Account |
| PC-100 | 机会筛选/收藏/比较 | OPERATING | STRONG | Business/Account |
| PC-101 | 手动创建机会（链接+条件+证据） | OPERATING | STRONG | Account |
| PC-102 | 机会→内容（研究→选题→生产→发布→追踪） | CORE | VERIFIED | Business/Account |
| PC-103 | 收益追踪（Revenue/Commission/Order/Conversion/Leads/Deal/Incentive；按账号记录；低频回填合法） | CORE | STRONG | Account/数据层 |
| PC-104 | 机会有效期与失效提示 | EDGE | STRONG | Account |
| PC-105 | 机会复盘（值得继续吗） | OPERATING | STRONG | Account/复盘 |
| PC-106 | 平台经营维度档案扩展（Monetization/Opportunity/门槛/Restrictions/变化史）——升级 PC-009 | CORE | STRONG | Platform Facts |
| PC-107 | 平台商业能力矩阵（变现方式×门槛×账号资格） | OPERATING | STRONG | Platform Facts/Account |
| PC-108 | 平台/账号能力覆盖视图（自动发布？自动数据？读评论？哪些手工/官方？） | CORE | STRONG | Platform Facts/Account |
| PC-109 | 自动化成熟度四档标注（MANUAL/ASSISTED/AUTOMATED/AUTONOMOUS） | CORE | STRONG | Platform Facts |
| PC-110 | 规则检测分层策略（Manual=VERIFIED/Cheap=CANDIDATE/Browser=CANDIDATE/AI 只解释变化=VERIFIED） | OPERATING | STRONG | Platform Facts |
| PC-111 | 收益数据类型与三层归属（Platform 原生/Account 经营/Business 结果） | CORE | STRONG | 数据层 |
| PC-112 | 三层绩效区分表达（内容≠账号≠业务） | CORE | STRONG | 表达原则 |
| PC-113 | Platform Definition（可扩展平台定义，从真实平台归纳） | CORE | STRONG | Platform Facts |
| PC-114 | 新平台进入方案（内置/用户自定义/Connector/Package/Hybrid 比较） | OPERATING | STRONG | Platform Facts |
| PC-115 | 意图关联官方入口（升级 PC-011） | OPERATING | STRONG | Platform Facts/Account |
| PC-116 | 便利动作集（打开原文/主页/复制 ID/数据后台/规则来源/返回上下文/最近账号） | OPERATING | STRONG | 各上下文 |
| PC-117 | 经营视角切换（整个业务/单平台/单账号/跨账号比较） | CORE | STRONG | Business |

**升级既有 4 项**：PC-009/011/017/018（见 §30）。**最终总数：95+22=117 项**（CORE 44 / OPERATING 64 / EDGE 9）。

# 35. 汇总汇报

第一轮（上轮）95 项；本轮全面推导**新增 22 项、升级 4 项、删除 0 项**。最大发现：①**账号的价值创造方式（Account Goal）此前完全缺失**——涨粉只是信号，带货/商单/激励/付费/私域才是目的；②**小账号（1000 粉）即进入真实商业循环**——机会循环是经营主循环的一部分而非 Edge；③**能力覆盖透明度**（用户必须知道 Curis 能替他做什么、处在哪档自动化）是 CORE 而非便利功能；④**AI 用于解释变化而非巡检**。仍无法确定：各平台商业门槛的持续准确性（平台随时调整，需以官方后台为准+定期人工验证机制）、Browser 采集的可行边界、机会数据的自动化程度演进（CURRENT=手动为主/NEXT=官方入口+回填/FUTURE=Connector 自动）。

**平台研究来源**：[抖音创作者中心官网](https://creator.douyin.com/)、[星图达人入驻手册（官方）](https://www.xingtu.cn/help-center/author/109194)、[抖音商品橱窗开通条件（蝉妈妈）](https://www.chanmama.com/yunyingquan/question/3602.html)、[2025 抖音变现全图谱（知乎）](https://zhuanlan.zhihu.com/p/1984718016253032223)、[YouTube Partner Program（官方）](https://www.youtube.com/creators/earn/youtube-partner-program/)、[YPP 门槛（Google Support）](https://support.google.com/youtube/answer/72851)、[TikTok Creator Rewards（官方 Academy）](https://www.tiktok.com/creator-academy/article/creator-rewards-program)、[TikTok Shop Creator Eligibility（官方）](https://seller-us.tiktok.com/university/essay?knowledge_id=6939143037667118&lang=en)。小红书/B站/公众号：中文查证超时，按行业通行规则写入，**以官方后台为准**（已标注）。

**STOP FOR CEO / CHATGPT REVIEW**——不进入 UI/RD；等待判定本轮 COMPREHENSIVE DERIVATION 是否通过。

---

# 36. PART III 增补 — DOUYIN MONETIZATION DEEP DIVE 新增能力（2026-09-13）

Authority Class: RESEARCH→候选能力登记（Draft，待 CEO 判定 Monetization Operating Model 后转正）
来源：CURIS_DOUYIN_REAL_PLATFORM_OPERATING_DEEP_DIVE.md PART III（M1–M33）+ CEO 手机截图 L1 + Web 已登录 L1 + 官方 L3。

| ID | Scenario | User Need | Product Capability | Owner | Context | Priority | Confidence | Evidence | Platform/Core | 当前成熟度 |
|---|---|---|---|---|---|---|---|---|---|---|
| PC-118 | 账号接管后 CEO 问"我离赚钱还差什么" | 知道每种变现的资格差距与下一步 | Monetization Qualification Map（九字段：Qualification/Current/Gap/Next Action/Source/Last Verified/Rule Version/Region/Account Type） | Account | 账号面/变现 | CORE | STRONG | L1 截图+L3 门槛 | Core | MANUAL→ASSISTED |
| PC-119 | 机会只在 App 里，CEO 想把它带进 Curis | 低摩擦把 App 机会变 Curis Opportunity | Opportunity Intake 多通道（Share 链接/Screenshot 识别/Manual 快填/DeepLink 导航） | Account | 机会库 | CORE | STRONG | L1 任务卡字段规整 | Core | MANUAL |
| PC-120 | 佣金 T+15、任务下月 15、商单验收后——钱在哪一步了 | 知道每笔钱的结算状态 | Revenue Settlement State Machine（应计/待结算/可提现/已提现/已到账/Deduction，按变现方式异质周期） | Account/数据层 | 收益面 | CORE | STRONG | L3 结算规则 | Core | ASSISTED |
| PC-121 | 带货收入 500 但保证金+DOU+ 先花 800 | 知道真赚了多少 | Cost & Profit 视图（收入/成本/ROI/Profit/到账现金流分层） | Account/数据层 | 收益/复盘 | OPERATING | STRONG | L3 保证金+L1 上热门 | Core | MANUAL |
| PC-122 | 选品中心每天几百个商品选哪个 | 结构化对照而非拍脑袋 | 选品决策对照（佣金/阶梯动态/销量/竞争/受众适配/内容难度六维对照卡，非评分） | Account | 选品/机会 | OPERATING | STRONG | L3 阶梯佣金+L4 | Douyin-first 可泛化 | ASSISTED |
| PC-123 | CEO 截了张任务卡给 Curis | 截图变可执行机会 | 任务 Brief 结构化（截图→名称/类目/结算方式/收益上限/截止→衔接选题生产） | Account/生产 | 机会→内容包 | OPERATING | STRONG | L1 卡片字段 | Core | MANUAL→ASSISTED |
| PC-124 | 报名/投稿/挂车必须 App 操作 | 不迷路、有回执 | Mobile-Only 执行包（DeepLink/QR 导航+App 步骤清单+回执回填） | Account | 发布/机会执行 | OPERATING | STRONG | L1 App-only 事实 | Douyin-first | MANUAL |
| PC-125 | CEO 要开第一场直播 | 开播前有准备、播后有复盘 | 直播 ASSISTED 包（预告内容/脚本/排品/话术/直播后数据与收益登记；明确不含实时场控） | Employee/Account | 直播 | EDGE | CANDIDATE | L4/L5 | Core | ASSISTED |
| PC-126 | 平台激励计划经常变（中视频已停发） | 不被过时激励误导 | 平台激励计划跟踪（现行计划资格+收益登记+Rule Version） | Account | 变现/机会 | EDGE | CANDIDATE | L3 停发实证+L4 | Douyin-first | MANUAL |
| PC-127 | 任务"按有效播放结算""奖励已瓜分0%" | 理解非标准结算语义 | 瓜分制/有效播放/核销结算语义建模（奖池余量、计量单位、核销前提） | 数据层 | 收益/机会 | EDGE | STRONG | L1 截图+L4 核销 | Douyin-specific | MANUAL |

**既有能力升级（本 PART 判定）**：PC-097→升格为 PC-118 载体；PC-103→结算状态机化；PC-099→Intake 化；PC-018→VERIFIED BY DOUYIN（App"创作阶段"实证）；PC-059→DEMOTE（变现核心页 App-only）；PC-022→并入账号状态徽章与信用分。

**总数更新：117+10=127 项候选**（待 CEO 判定 PART III 后生效）。
