# CURIS COMPETITIVE PATTERN LIBRARY（含 Pattern Translation Matrix）

> Authority Class: RESEARCH / EVIDENCE
> Status: v1——收录 Zcode / Coze / Workbuddy(本地) / Claude·Cursor·ChatGPT·Manus·Devin 的**通用模式**（后五者来自公开共识与既有研究档案，⏳ 标记待清单返回后逐条落源）；翻译列给出"若引入 Curis 应落在哪里"，**不构成产品裁决**。
> 升级规则（MASTER_PLAN §2）：只有 ≥2 成熟产品共同验证、或直接解决 Curis 已登记缺陷、或 Frozen 已要求但实现缺失的模式，才可升级为 RECOMMENDATION CANDIDATE（⭐）。

## A. 组织与多智能体模式

| ID | Pattern | 来源（≥1 产品） | 翻译到 Curis 的落点 | 级别 |
|---|---|---|---|---|
| P-A1 | **场景路由用户解释**：让用户看懂"为什么派给 TA"（路由依据=职责描述+名称） | Coze P1 | Leader 分工画面/Work 卡显示"依据的责任"字段 | 观察 |
| P-A2 | **节点级身份隔离**：每个子 agent 独立模型/技能/提示词，故障域隔离、可单点调试重跑 | Coze P2/O2；Zcode subagent | Employee 级"重跑这次工作/只跟 TA 说"（Quick Panel 已有旁路对话） | ⭐（多源+解决缺陷） |
| P-A3 | **规则安全阀**：少量硬规则优先于自动路由 | Coze O10 | only-on-exception 的用户语言化："这件事必须先问我"规则 | 观察 |
| P-A4 | **项目容器共享资产**：人+多 agent 同项目，会话/文件/任务/记忆默认共享 | Coze P4 | 已有（Workspace 共享 Context/Utility，Phase B）——保持 | 已有 |
| P-A5 | **席位/升级链治理**：agent 超出权限→升级到人（外部通道） | Workbuddy 本地证据；Devin org policy ⏳ | "员工请示 CEO"一等事件 + Decision Banner + 通知 | ⭐ |
| P-A6 | **会议制度化多 agent 协作** | Curis 独有 | 保护，不翻译（竞品无对等） | 保护 |
| P-A7 | **团队=模板化组织**（角色组合一键建队） | Coze 模板 ⏳；Workbuddy 团队 | 与原装组织冲突风险高——仅在用户自建业务时提供"岗位模板" | 观察 |

## B. 工作执行与进度模式

| ID | Pattern | 来源 | 翻译落点 | 级别 |
|---|---|---|---|---|
| P-B1 | **Todo/步骤清单为进度第一公民** | Zcode Z1；Manus task list ⏳；Devin plan ⏳ | Work 卡计划段（§Direction 2.6） | ⭐ |
| P-B2 | **计划先行+权限预算申报**（执行前对齐） | Zcode Z3；Devin plan edit ⏳ | Work 创建时"怎么做"确认（可选，按 Work 模式） | 观察 |
| P-B3 | **过程细节默认折叠**（摘要行+点开看工具流） | Zcode Z2 | Conversation 过程折叠（Audit G-09） | ⭐ |
| P-B4 | **后台并行+完成通知注入** | Zcode Z6；Devin parallel ⏳ | 并行 Work + 通知中心（依赖 Runtime 并行能力） | 观察（先 Runtime） |
| P-B5 | **执行记忆/自动化自判失效**（automation 有自己的 memory，可判 SKIPPED/PAUSED/DELETE） | Workbuddy 本地 | 未来 Automation 对象的形态约束（若立项） | 观察 |
| P-B6 | **任务状态机+主动汇报**（待执行/执行中/完成/暂停/失败 + Agent 主动回播） | Coze P6/O5 | Work 状态词典 + 完成汇报叙事 | ⭐ |
| P-B7 | **replay/回放作为证据** | Devin session replay ⏳；Manus replay ⏳ | Work→Evidence 已是溯源强项；补"执行轨迹回放"视图 | 观察 |

## C. 结果与知识模式

| ID | Pattern | 来源 | 翻译落点 | 级别 |
|---|---|---|---|---|
| P-C1 | **Artifacts 式富预览**（文档/代码/表格即时预览+版本+remix） | Claude Artifacts ⏳ | Result Utility 消费面（M-04） | ⭐ |
| P-C2 | **记忆对用户透明可编辑**（列表/增删改/范围） | Coze P5；Workbuddy MEMORY.md；ChatGPT Memory ⏳ | 公司记忆/共识归档的查看与编辑面（M-12） | ⭐ |
| P-C3 | **项目级知识注入**（项目说明+文件自动入上下文） | Claude Projects ⏳ | Workspace Context 注入已存在；补"引用来源可见"（Knowledge UX P1） | 已有/补 UX |
| P-C4 | **引用行不铺全文**（对话内 Result/知识只留引用，点开 Utility） | Curis Frozen（独有，与 Coze 一致） | 保护+落实现 | 保护 |

## D. 人才与能力模式

| ID | Pattern | 来源 | 翻译落点 | 级别 |
|---|---|---|---|---|
| P-D1 | **三目录结构：专家/技能/连接器** | Workbuddy（140+/7万+/连接器市场）；Coze 商店 | 人才与能力区三分区（D 代骨架已是） | ⭐ |
| P-D2 | **能力用户语言卡**（面向普通用户的"会做什么"，点开才是技术绑定） | Zcode Z5；GPT Store ⏳ | Capability 用户语言 P1（M-06） | ⭐ |
| P-D3 | **安装即入职**叙事（招募→实例化→分配责任） | Curis 独有 | 保护（竞品无） | 保护 |
| P-D4 | **发布/渠道矩阵**（一个产物多渠道分发+能力降级表） | Coze O6 ⏳ | Channel 模型已有；Channel Account 执行面为既有 gap | 观察 |

## E. 对话与 Composer 模式

| ID | Pattern | 来源 | 翻译落点 | 级别 |
|---|---|---|---|---|
| P-E1 | **执行者≠模型**（选择"谁做"与"用什么模型"分离） | Curis Frozen X10（D 代已实现）；Zcode | 保护+落实现 | 保护 |
| P-E2 | **@引用与斜杠命令**作为输入第一语法 | Zcode；Slack 系共识 | Composer 引用槽位（对象引用：员工/业务/资料/结果） | ⭐ |
| P-E3 | **建议提示**（suggested prompts/replies） | Coze；ChatGPT ⏳ | Composer 空态建议行（低成本高感知） | 观察 |
| P-E4 | **全局可唤起助理**（快捷键/overlay，任何页面上文感知） | ChatGPT/Claude ⏳；Zcode | Phase B 浮层助理 + 全局快捷键（M-15） | ⭐ |

## F. 视觉与桌面模式

| ID | Pattern | 来源 | 翻译落点 | 级别 |
|---|---|---|---|---|
| P-F1 | **安静高密度**（排版/灰度建立层级，克制色块） | Linear/Notion 学派（D 代已采纳） | 保护（延续 D 代纪律） | 已采纳 |
| P-F2 | **单一 accent 全域一致** | 全竞品共识 | V1 `#806BE5` 迁移完成（G-01 收口） | ⭐ |
| P-F3 | **状态三件套**（状态点+词典文字+左指示线，语义色小面积） | 竞品共识 | 状态词典统一（G-08） | ⭐ |
| P-F4 | **空态=主行动+叙事**（禁零值仪表盘） | 竞品共识 | 空态规范（G-04） | ⭐ |
| P-F5 | **浮层材质分层**（页面平面、Popover/Drawer/Modal 才有阴影） | 竞品共识 | Material 规范（§Direction 3.3） | ⭐ |
| P-F6 | **桌面性四件套**（全局快捷键/菜单栏/通知/Dock 徽标） | ChatGPT/Claude/Zcode | M-15 | ⭐ |

## Translation 汇总：⭐ RECOMMENDATION CANDIDATE 清单（12 项，少而精）

P-A2、P-A5、P-B1、P-B3、P-B6、P-C1、P-C2、P-D1、P-D2、P-E2、P-E4、P-F2、P-F3、P-F4、P-F5、P-F6（合并去重后对应 MISSING REGISTER 的 M-01~M-16 子集，不新增对象体系）。

## G. v2 增补（Claude / Cursor / Workbuddy 网络证据落源）

> 编号续接；每条含来源（清单章节）。⭐ 判定同前。

| ID | Pattern | 来源 | 翻译到 Curis 的落点 | 级别 |
|---|---|---|---|---|
| P-A8 | **三层能力模型**：Skill（能做什么）→ Expert（人设+方法论+工具链）→ Expert Team（团长拆解+并行+整合，成本倍率明示 3-5x） | Workbuddy O1 | 人才与能力区的三层公开模型与各自成本口径（对照 Curis Capability/Skill/Employee/Team） | ⭐ |
| P-A9 | **召唤制 + 成果反查导购**：专家卡极简 3-4 字段、"召唤"而非安装；"灵感做同款"从成果反向加载人才+技能+配置 | Workbuddy O2 | 人才卡理解成本压缩；"从 Result 反查是哪个员工/能力做的"（Curis 有 Result→Employee 链，天然可做） | ⭐ |
| P-A10 | **授权边界而非配置面板**：角色不自带权限，按调用边界逐层授权；公共/个人票据双轨，协作任务禁用个人票据 | Workbuddy O4 | 权限政策面（M-09）的具体形态：员工→Skill/MCP→连接器→数据范围逐层授权 | ⭐ |
| P-A11 | **四级审批梯度**：对话内确认（内容/影响/理由三要素）→ 阈值规则（批量删除 50）→ IM 远程批准 → 审计中心留痕 | Workbuddy O5 | CEO 请示/批准事件的分级设计（结合 P-A5 升级链） | ⭐ |
| P-A12 | **记忆归用户、技能归资产**：个人记忆与能力资产分开演进；"进化"=记忆沉淀为可复用 Skill | Workbuddy O7 | 公司记忆（M-12）与 Skill 资产化的归属切法参考 | 观察 |
| P-A13 | **组织人才治理五能力位**：项目默认值注入 / 置顶 / 配置变更广播 / 版本化 / ROI 看板 | Workbuddy O8 | Workspace 级"默认团队配置"与变更可见性（对照 Assignment 模型） | 观察 |
| P-B8 | **非破坏介入**：运行中任务可 queue/steer（插队指令不改结构） | Cursor；Claude course-correct | Work 运行中"补充指令/改向"输入（对照 P-B2 计划先行） | ⭐ |
| P-B9 | **checkpoint 时间线**：执行节点可回滚对比 | Cursor P3 | Work 执行轨迹 + Evidence 的时间线化（先 Runtime 盘点） | 观察 |
| P-B10 | **任务看板 + 工时摘要**：In Progress / Ready for Review 看板；"Worked for 14m"人话摘要 | Cursor P9 | CEO 工作台"正在运行"区与 Work 卡完成摘要（用户语言时长/成本） | ⭐ |
| P-B11 | **automations 归属三档**：Private / Team Visible / Team Owned + 计费身份绑定 | Cursor | 若做 Automation（M-11）的组织归属设计 | 观察 |
| P-C5 | **结果=真文件**：输出可预览的真实交付物（Excel/PPT/diff），聊天只是驱动器 | Claude P4；Manus 交付物 | Result 消费面（M-04）的"产物中心"原则 | ⭐ |
| P-C6 | **上下文三层**：全局指令 → 项目（指令+知识+独立 memory）→ 会话，每层可单独编辑 | Claude P5 | 公司级指令 / Workspace Context / 会话 三层用户语言（对照 Scope 模型） | ⭐ |
| P-C7 | **隐身/敏感边界显式化**：incognito 会话（不进历史/记忆/检索）、敏感记忆 opt-in+通知 | Claude P8 | 公司敏感经营数据的"不入库会话"形态（隐私面缺失 M 系） | 观察 |
| P-E5 | **三入口合一壳**：Chat / Work(agentic) / Code 同壳模式切换，轻→重迁移成本≈0 | Claude P1 | CEO Assistant（对话）与 Employee Work（执行）同壳衔接，避免两个割裂入口 | ⭐ |
| P-E6 | **Usage 贴近操作点**：模型选择器旁 usage ring 双显 + "哪些操作耗用量"教育 | Claude P7；Workbuddy 积分倍率明示 O9 | Usage 面（M-08）+ Work 卡成本预估就地显示 | ⭐ |
| P-F7 | **Settings 五分 IA + org/个人双层**：能力开关/个性化/接入/用量/组织管理分开；org 上界内个人自选 | Claude P10/P11 | Settings IA（§Direction 2.7）+ 未来组织管理的双层结构 | ⭐ |
| P-F8 | **权限四层体系**：档位模式 × 粒度白名单（自然语言规则）× sandbox × 硬红线（高危特殊保护） | Claude P3；Cursor P1；Workbuddy O5 | M-09 权限政策面的完整形态（2.2 对照表已证 Curis 缺三层） | ⭐ |
| P-F9 | **规则文件工程化**：Rules 多档应用+优先级链，可版本管理 | Cursor P5 | 与 Curis"业务规则/标准"对象的关系待产品定义（不新建第二体系） | 观察 |

### ⭐ 清单更新（v2）

新增升级：P-A8、P-A9、P-A10、P-A11、P-B8、P-B10、P-C5、P-C6、P-E5、P-E6、P-F7、P-F8。
合并后 RECOMMENDATION CANDIDATE 全集与 MISSING REGISTER 的对应关系不变（均为 M-01~M-16 的具体化），不新增对象体系。

## H. v3 增补（ChatGPT / Manus / Devin 落源）

| ID | Pattern | 来源 | 翻译到 Curis 的落点 | 级别 |
|---|---|---|---|---|
| P-A14 | **从"市场"转向"工作台"**：ChatGPT Agent mode 被 ChatGPT Work 取代（Plan mode/Templates/Sites/Library 交付物面）；个人账号停建 GPT | ChatGPT 清单 | 对 Curis 方向的利好信号：组织化工作台 > 开放市场；人才与能力区应把重心放在"员工工作面"而非货架 | ⭐ |
| P-A15 | **Playbook 五段结构**：Procedure / Specifications / Advice / Forbidden Actions / Required from User——可复用责任模板 | Devin | Responsibility/作业规范的用户化字段结构（对照 Curis Responsibility Definition；不新建第二体系，仅字段参考） | ⭐ |
| P-A16 | **自动化的身份归属**：Scheduled Sessions 有 Run-as（以某成员身份运行） | Devin | 若做 Automation（M-11），任务必须归属 Employee 身份——与唯一 Usage Ledger 天然一致 | ⭐ |
| P-A17 | **知识的触发描述**：Knowledge 条目带 Trigger Description（"何时使用这条知识"） | Devin | 资料库 Knowledge 条目的"适用范围/何时引用"字段（Curis 已有适用范围语言，缺触发语义） | ⭐ |
| P-B12 | **持久工作环境**：Cloud Computer 24/7 常驻 VM，长任务不随会话消失 | Manus | Work 执行环境的持久性语义（Runtime 层对照，观察） | 观察 |
| P-B13 | **大规模并行研究**：Wide Research 并行至 250 项 | Manus | 并行 Work 的上限心智（依赖 Runtime parallel multi-Work） | 观察 |
| P-B14 | **会议纪要进入竞品**：Manus Meeting Minutes（线下会议+说话人识别） | Manus | 竞品首次触及"会议"，但仍是工具性纪要；Curis Meeting 制度仍独有——纪要/转写可作为未来输入能力，不改会议模型 | 观察 |
| P-C8 | **记忆来源可解释**：ChatGPT memory summary 带 sources（这条记忆从哪来） | ChatGPT | 公司记忆条目带 Evidence 来源——Curis Evidence 链天然支持，应在 Memory 面呈现 | ⭐ |

## 更新记录

- 2026-09-12 v1：Zcode/Coze/Workbuddy 本地已落源；⏳ 项待清单返回后补源与修订级别。
- 2026-09-12 v2：Claude（§15）/Cursor（§12）/Workbuddy 网络（§16）落源，新增 P-A8~P-F9；⭐ 升级 12 项。
- 2026-09-12 v3：ChatGPT/Manus/Devin 落源，新增 P-A14~P-C8；⭐ 再升级 5 项。PATTERN LIBRARY COMPLETE。
