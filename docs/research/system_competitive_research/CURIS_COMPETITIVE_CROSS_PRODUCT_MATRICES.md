# CURIS COMPETITIVE CROSS-PRODUCT MATRICES（横向九矩阵）

> Authority Class: RESEARCH / EVIDENCE
> Status: v3（COMPLETE）——九产品列全部回填：Curis / Zcode / Coze(扣子) / Workbuddy / Claude / Cursor / ChatGPT / Manus / Devin。单元格细节见各清单对应章节，标 ⚡ 处为清单中字段级证据。
> Date: 2026-09-12
> 来源清单：`CURIS_RESEARCH_ZCODE_FUNCTION_INVENTORY.md`、`CURIS_RESEARCH_COZE_FUNCTION_INVENTORY.md`、`CURIS_RESEARCH_WORKBUDDY_LOCAL_EVIDENCE.md`、`CURIS_CURRENT_UI_AUDIT.md`、`CURIS_PRODUCT_CAPABILITY_GAP_MATRIX.md`。其余：`CURIS_RESEARCH_{CLAUDE,CURSOR,CHATGPT,MANUS,DEVIN,WORKBUDDY}_FUNCTION_INVENTORY.md`。

---

## 矩阵 1：Composer Matrix（输入区字段级）

| 字段/能力 | Curis（合同/现状） | Zcode | Coze/扣子 | Workbuddy | Claude ⚡ | Cursor ⚡ | ChatGPT ⚡ | Manus ⚡ | Devin ⚡ |
|---|---|---|---|---|---|---|---|---|---|
| 多行文本输入 | ✅（X10 合同） | ✅ | ✅ | ✅ | | | | | |
| 附件/文件上传 | ✅ 合同槽位（实现薄） | ✅ 图片粘贴 | ✅ 文件/图片 | ✅ | ✅ 文件/截图（500MB/文件口径） | ✅ | ✅ 文件/截图 | ✅ | ✅ |
| @引用（对象/文件） | ❌ 无证据 | ✅ @文件 | ✅ 引用知识库/插件 | UNKNOWN | ✅ @-mentions 全清单 | ✅ @-mentions | 见清单 | 见清单 | 见清单 |
| 模型选择器 | ✅ Conversation 内切换（Partial 实现） | ✅ 会话级 | ✅ 每 Agent 节点级 | ✅ 对话内快选+三档调度+思考强度 | ✅ 模型+effort+thinking 独立 toggle | ✅ 双模型池+Auto 路由 | ✅ 模型选择 | ✅ 1.6 Lite/Max | UNKNOWN |
| 执行者选择（Agent≠模型） | ✅ Frozen 语义槽位"执行·<Agent>"（D 代已实现） | 主/子 agent 隐式 | ✅ 智能体节点 | ✅ 专家选择 | ✅ Chat↔Cowork↔Code 模式切换+Dispatch | ✅ 四 mode+Custom Modes+Cloud Agents | ✅ Chat/Work/Codex 三区 | ✅ Chat↔Agent 模式 | ✅ Ask↔Agent 模式 |
| 工作模式/权限槽位 | ✅ "访问权限/工作模式"槽位（D 代） | ✅ permission mode / plan mode | PARTIAL | ✅ 权限模式（默认权限/安全沙箱） | ✅ Cowork 三模式 / Code 五模式 | ✅ 三档 Run Modes + permissions.json | ✅ Work Plan mode | ✅ Allow Once/Always | ✅ plan-first |
| 命令/斜杠命令 | ❌ | ✅ /skills | ❌ | UNKNOWN | PARTIAL（快捷键生态） | ✅ /goal /side /best-of-n /automate | | | |
| 快捷键发送/换行 | ✅ | ✅ | ✅ | ✅ | | | | | |
| 建议提示（suggested prompts） | ❌ | ❌ | ✅ 用户问题建议 | UNKNOWN | UNKNOWN | UNKNOWN | 见清单 | 见清单 | 见清单 |

**结论**：Curis Composer 的**槽位设计在合同层已对标竞品**（执行者/权限/模式三槽位是亮点，竞品少有把"访问权限"做成一等槽位），缺的是实现成熟度与引用/命令两个高频字段。

## 矩阵 2：Conversation Matrix（对话面）

| 能力 | Curis | Zcode | Coze | Workbuddy | Claude ⚡ | Cursor ⚡ | ChatGPT ⚡ | Manus ⚡ | Devin ⚡ |
|---|---|---|---|---|---|---|---|---|---|
| 流式输出 | ✅ | ✅ | ✅ | ✅ | | | | | |
| 消息操作（重试/编辑/分支） | PARTIAL | ✅ 编辑重发 | ✅ | UNKNOWN | ✅ edit→branch、原位编辑 | ✅ queue/steer 非破坏介入 | | | |
| 结构化回复卡（结果引用/决定包） | ✅ Result Reference→Utility（Frozen）；实现薄 | 工具卡 | ✅ 卡片消息 | UNKNOWN | | | | | |
| 过程细节折叠 | ❌ 全铺或全无 | ✅ 工具卡可折叠 | PARTIAL | PARTIAL（任务过程可展开） | PARTIAL（Cowork 步骤可视） | ✅ 工具调用卡+Review | | | |
| 多话题/主题隔离（按 Assignment） | ✅ 事件化 topic（独有） | ❌ 单会话流 | ❌ | ❌ | | | | | |
| 长会话持续（摘要/compact） | UNKNOWN | ✅ compact/handoff | ✅ 长期记忆 | ✅ 每晚自动摘要+可编辑/导入导出 | ✅ topic 级 memory+chat search | ✅ Memories（自动+注入警示） | | | |
| 已读/注意力（Viewed/Attention） | ✅ 独有 | ❌ | ❌ | ❌ | | | | | |
| 用量归属到消息 | ✅ 唯一 Usage Ledger（独有） | ❌ | ✅ token 统计 | UNKNOWN | | | | | |

**结论**：Curis 对话的**事件模型（topic/attention/usage 归属）领先**；**呈现层（折叠/结构卡/降密度）落后**——"像日志"的根源是缺过程折叠与卡片化，不是缺事件模型。

## 矩阵 3：Agent Progress Matrix（工作进度呈现）

| 能力 | Curis | Zcode | Coze | Workbuddy | Claude ⚡ | Cursor ⚡ | ChatGPT ⚡ | Manus ⚡ | Devin ⚡ |
|---|---|---|---|---|---|---|---|---|---|
| 计划先行（plan→确认→执行） | UNKNOWN（Runtime 无对应产品机制证据） | ✅ plan mode + 权限预算 | ❌ | ✅（自动化先判定后动作） | ✅ Cowork 先建 plan 拆 subtasks | ✅ Plan mode + plan→approve 门 | ✅ Work Plan mode | PARTIAL（todo 先行） | ✅ plan-first + plan 可编辑 |
| 步骤清单（todo）可见 | ❌（Work/Task 在 Runtime，无投影） | ✅ todo list 第一公民 | PARTIAL（工作流节点） | ✅ 任务 6 状态+执行历史 | ✅ subtasks 并行可视 | ✅ 任务看板 In Progress/Ready for Review | ✅ Work plan/tasks | ✅ Computer 面板 todo 第一公民 | ✅ Progress 工具+计划步骤 |
| 当前动作实时显示 | ❌ | ✅ 工具卡流 | PARTIAL | ✅（日志） | | | | | |
| 阻塞/需人介入态 | ✅ UI Status 投影三态+阻塞（Frozen）；面薄 | ✅ approval 提示 | ✅ | ✅ 四级审批梯度（含 IM 远程批准） | ✅ 权限请求+course-correct | ✅ 三道硬保护闸+Auto-review | UNKNOWN | ✅ Take Over（浏览器接管） | ✅ takeover（shell/browser/机器） |
| 完成→结果通知 | PARTIAL（CEO Desk attention） | ✅ 后台通知注入 | ✅ 任务回播 | ✅ 汇报三段式 | | | | | |
| 失败重试可见 | PARTIAL | ✅ | ✅ 节点重试 | ✅ 自动化重派 | | | | | |
| 执行重放/审计（replay/trace） | PARTIAL（Evidence 链可溯源，无回放面） | 会话史即回放 | ✅ 日志/trace | ✅ 自动化 memory | PARTIAL（会话史） | ✅ checkpoints/diff 审计 | UNKNOWN | ✅ replay（?replay=1） | ✅ session replay + Session Insights |

**结论**：进度呈现是**全产品最大呈现缺口**（GAP MATRIX M-03）；Curis 的 Evidence 溯源是独特资产，但"正在工作"的实时面为零。

## 矩阵 4：Multi-Agent Matrix（多智能体/组织）

| 能力 | Curis | Zcode | Coze | Workbuddy | Claude ⚡ | Cursor ⚡ | ChatGPT ⚡ | Manus ⚡ | Devin ⚡ |
|---|---|---|---|---|---|---|---|---|---|
| 组织语义（角色/部门/层级） | ✅ 独有（Company OS 全套） | ❌ | PARTIAL（团队空间，无层级） | ✅ 席位链（用户自定义） | PARTIAL（org 上界+Skills 共享） | PARTIAL（Teams 归属三档） | ❌ | PARTIAL（Collab，owner-only credits） | PARTIAL（Knowledge org 范围+Run-as+机器指派） |
| 持久 Leader/主管 | ✅ 独有 | ❌ | ❌ | PARTIAL（总控席） | | | | | |
| 责任指派（Assignment 持续关系） | ✅ 独有 | ❌ | ❌（实时路由非指派） | PARTIAL（任务派发） | | | | | |
| 路由机制 | ✅ Responsibility routing + only-on-exception | 主 agent 自行派发 | ✅ LLM 场景路由+全局跳转 | ✅ 专家团团长拆解 | ✅ Dispatch（Cowork→Code） | ✅ Projects coordinator+Auto 路由 | ❌（模式切换） | ❌ | PARTIAL（Automations Triage/触发路由） |
| Handoff 契约（交接说明/打包） | ✅ Handoff 定义 | ❌ | ❌ 隐式跳转 | PARTIAL | | | | | |
| 单成员旁路对话 | ✅ Quick Panel 直接对话 | subagent 派发 | ✅ 单节点直连 | ✅ | | | | | |
| 群体讨论机制 | ✅ 会议（独有制度） | ❌ | ❌ | ❌ | | | | | |
| 成员级调试/重跑 | PARTIAL | ✅ subagent 重试 | ✅ 节点级调试 | ✅ 成员重派 | ✅ sub-agents+会话级 review | ✅ subagents+Agent Review（Quick/Deep） | UNKNOWN | ✅ Take Over | ✅ Side Chats+takeover+按任务重跑 |
| 并行多工作 | ❌ NOT IMPLEMENTED | ✅ 后台任务 | PARTIAL | ✅ 专家团并行（积分 3-5x） | ✅ 并行 sub-agents | ✅ worktrees+best-of-n | PARTIAL（Work 任务） | ✅ Wide Research（并行至 250 项） | ✅ 并行 sessions + Managed Devins 编排 |

**结论**：组织模型 Curis 全面领先（Coze 无 Leader/Assignment/会议/契约化 Handoff；16.3 已证）；**运营能力落后**在并行执行、成员级调试的产品面。

## 矩阵 5：Talent & Capability Matrix（人才与能力）

| 能力 | Curis | Workbuddy | Coze | ChatGPT(GPTs) ⚡ | Claude ⚡ | Zcode |
|---|---|---|---|---|---|---|
| 人才发现目录（浏览/分类/搜索） | PARTIAL（D 代骨架） | ✅ 专家中心 140+专家/12 行业 | ✅ 商店 | ✅ GPT Store | | ✅ plugin marketplace |
| 专家卡片字段 | 骨架（身份/擅长/能力/案例/来源） | UNKNOWN（网络清单待补） | ✅ bot 卡 | ✅ | | |
| 详情页深度 | 骨架 | UNKNOWN | ✅ 配置全字段 | ✅ | | |
| 安装/招募流 | ✅ IMPLEMENTED（招募→Employee 实例） | ✅ 安装 | ✅ 添加 | ✅ | | ✅ install |
| 技能市场规模语言 | ❌ | ✅ SkillHub 7 万+ | ✅ 插件/模板市场 | ✅ | | PARTIAL |
| Skill↔人的绑定 | ✅ Employee Capability Binding（独有：绑定到"员工"而非 bot） | UNKNOWN | ✅ 节点级挂载 | ❌ | | ✅ |
| 连接器目录 | PARTIAL（Registry Review；truth 未连接） | ✅ 连接器市场 | ✅ 插件/MCP | ✅ | | ✅ MCP |
| 用户语言能力描述 | ❌（P1） | ✅ 面向普通用户 | PARTIAL | ✅ | | PARTIAL |
| 人才=组织成员（非工具） | ✅ 独有（Definition→Instance→Holder） | PARTIAL（专家近雇佣叙事） | ❌ | ❌ | | ❌ |

**结论**：Curis 的"招聘入职成为真员工"叙事独有；发现/安装/理解的**市场语言与规模感**是最大落差（对 Workbuddy 直接对标）。

## 矩阵 6：Result / Artifact Matrix

| 能力 | Curis | Claude ⚡ | Manus ⚡ | Devin ⚡ | Zcode | Coze |（ChatGPT 对照：Work 的 Sites/Library/Templates 为交付物面，见其清单）|
|---|---|---|---|---|---|---|
| 结果对象化（独立于对话） | ✅ Result 对象（独有链路） | ✅ Artifacts | ✅ 交付物 | ✅ PR/文件 | PARTIAL（diff/文件） | PARTIAL |
| 预览（文档/代码/表格/网页） | PARTIAL（Utility 打开） | ✅ Artifacts 预览/Excel/PPT/文档 | ✅ 交付物/演示文稿 | ✅ PR/文件 | ✅ diff | PARTIAL |
| 版本/历史 | PARTIAL | ✅ 版本 | UNKNOWN | ✅ git | ✅ checkpoint+Artifacts 版本 | ✅ 发布历史 |
| 下载/导出 | UNKNOWN | ✅ | ✅ | ✅ | ✅ | PARTIAL |
| 引用回对话/工作 | ✅ Result Reference→Utility（Frozen） | ✅ remix/publish/嵌入 | UNKNOWN | ❌ | ✅ | PARTIAL |
| 证据链（为什么是这个结果） | ✅ 独有 Result→Evidence | ❌ | ✅ replay（?replay=1） | ✅ session replay+Session Insights | PARTIAL | ❌ |
| 归档库（成果库） | PARTIAL（nav 存在，视图缺） | ✅ Artifacts 列表 | ✅ | ✅ | ❌ | ✅ |

**结论**：Evidence 溯源独有；预览/版本/下载的**消费三件套**需补齐（M-04）。

## 矩阵 7：Desktop Shell Matrix

| 能力 | Curis | ChatGPT ⚡ | Claude ⚡ | Cursor ⚡ | Zcode | Manus ⚡ | Devin ⚡ |
|---|---|---|---|---|---|---|---|
| 原生桌面 App | ✅ Tauri（packaged 验收过） | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 全局快捷键/overlay | ❌ | ✅（option-space + Classic companion） | ✅ Quick Entry 浮层（输入/截图/窗口附带/语音） | PARTIAL（命令面板） | PARTIAL | UNKNOWN | ❌ |
| 菜单栏/tray | ❌ | ✅ | PARTIAL（Chrome side panel+手机接力） | ❌ | ❌ | UNKNOWN | ❌ |
| 通知中心 | ❌ | ✅（task 通知） | UNKNOWN | ✅ | PARTIAL | UNKNOWN | ✅（Slack 通道） |
| 离线/连接态 | PARTIAL（D 代 states 页有离线态设计） | ✅ | UNKNOWN | ✅ | ✅ | UNKNOWN | ❌ |
| sidecar/后台进程管理 | ✅（Tauri guardian，内部） | ❌ | ❌ | ❌ | ✅ | ❌ | ✅（云端 fleet） |
| 本地文件访问 | ✅（Runtime） | ✅ | ✅ | ✅ | ✅ | ✅ | ✅（VM 内） |
| Computer Use | ❌（ADR-0046 未实现） | PARTIAL（Agent mode 已被 Work 取代） | ✅ | ❌ | ✅ | ✅ Cloud Computer（24/7 VM）+My Computer | ✅（浏览器/shell/机器指派） |

**结论**：Curis 桌面壳"有壳无桌面性"——打包/重启/recovery 这些最难的部分已验收，缺的是用户可见的桌面能力层（M-15）。

## 矩阵 8：Settings Matrix

→ 独立文件：`CURIS_COMPETITIVE_SETTINGS_MATRIX.md`（字段级）。

## 矩阵 9：Visual System Matrix（视觉系统）

| 维度 | Curis 现状（四代） | 竞品共识（2026 桌面 AI） |
|---|---|---|
| Accent | `#32f08c`（实现/旧 Spec）/ `#806BE5`（V1 Frozen，未消费）/ 黑绿（A 代） | 单一克制的品牌 accent（Claude 橙、Cursor 蓝紫、Linear 紫）——**单选且全域一致** |
| 主题 | 深色默认（tokens）+ A 代双主题；B/C 无 Dark | 双主题标配，深色优先普遍 |
| 密度 | D 代"安静高密度"方向正确，落地为标签堆叠 | 中高密度 + 固定行高节奏（40±4px） |
| 层级手段 | 排版/灰度/分隔（D 代纪律好） | 同左 + 少量语义色小面积信号 |
| 卡片纪律 | A 代卡片泛滥；D 代克制（列表行优先）✅ | 列表行优先，卡片仅聚合容器 |
| 圆角 | 4/8/12/999 四档（Frozen）；实际 10-12 混用 | 6-10px 为主，全站一档系 |
| 阴影 | 几乎无 | 页面平面、浮层阴影（层级靠 z 轴材质） |
| 字体 | system-ui 栈（D3） | 系统栈 + 等宽用于数据/代码 |
| 动效 | 无规范 | 150-250ms ease-out；状态动效集中 |
| 状态表达 | chip 泛滥、色义漂移 | 状态点+文字+左指示线三件套，词典唯一 |
| 品牌人格 | 标语口号入 UI（A 代） | 产品内零营销文案 |

**结论**：视觉层不需要发明新方向——D 代纪律 + V1 token + 本表修正项（accent 迁移、状态词典、密度节奏、浮层材质）即构成 Curis Desktop Design Language。

---

## 更新记录

- 2026-09-12 v1：以 Curis/Zcode/Coze/Workbuddy(本地) 建版。
- 2026-09-12 v2：回填 Claude/Cursor/Workbuddy(网络) 列（⚡=字段级证据在清单内）。
- 2026-09-12 v3：回填 ChatGPT/Manus/Devin 列；九矩阵 COMPLETE。关键新增事实：ChatGPT 桌面重构为 Chat/Work/Codex 三区、Agent mode 被 Work 取代、个人账号停建 GPT；Manus Cloud Computer（24/7 VM）、Wide Research（并行 250 项）、Meeting Minutes（线下会议纪要+说话人识别）、replay；Devin Playbooks（五段结构）、Scheduled Sessions（Run-as 身份）、Automations（8 触发源×4 动作）、Managed Devins、Session Insights（ACU/XS-XL 规模）。
