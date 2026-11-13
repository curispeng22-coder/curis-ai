# CURIS MISSING CAPABILITY REGISTER

> Authority Class: RESEARCH / EVIDENCE
> Status: v1 COMPLETE（来源：CURIS_PRODUCT_CAPABILITY_GAP_MATRIX.md + CURIS_CURRENT_UI_AUDIT.md + 各 FUNCTION_INVENTORY 的 GAP 笔记；升级为 RECOMMENDATION CANDIDATE 的门槛见 MASTER_PLAN §2）
> Date: 2026-09-12
> 用途：登记"竞品已普及且 Curis 缺失"与"Curis 独有但只有 Runtime 没有产品面"的能力缺口。**本登记不自动成为开发任务**；进入开发需正式 Issue + Authority Gate。

## 1. 缺失的产品能力（竞品标配，Curis 缺失或仅 Runtime）

| ID | 能力 | 竞品证据 | Curis 现状 | 建议级别 |
|---|---|---|---|---|
| M-01 | 全局对象搜索 / ⌘K 命令面 | ChatGPT/Claude/Cursor/Linear 全员标配 | NOT IMPLEMENTED（CURRENT_STATE P1） | RECOMMENDATION CANDIDATE（Frozen 已要求，多产品验证） |
| M-02 | 结构化 Composer（附件/模型选择/工具开关/@引用/命令） | 全员 | 合同 Frozen 但实现/证据薄 | RECOMMENDATION CANDIDATE（直接解决明确缺陷） |
| M-03 | 员工工作进度可视化（计划→步骤→工具→完成） | Zcode todo、Manus task list、Devin plan pane | Runtime 有 Work/Task；无进度面 | RECOMMENDATION CANDIDATE |
| M-04 | Result / Artifact 消费面（预览/版本/下载/引用） | Claude Artifacts、Manus deliverables | Result→Evidence 链在 Runtime；最终工作面是 Current P1 | RECOMMENDATION CANDIDATE（Frozen 已要求） |
| M-05 | Employee Detail / 完整工作站页 | Workbuddy Expert 详情、Coze Agent 配置、Devin member 页 | Phase B 部分实现；"最终工作面"是 Current P1；无 UI 资产 | RECOMMENDATION CANDIDATE（Frozen 已要求） |
| M-06 | 人才发现/市场语言（浏览/分类/详情/安装） | Workbuddy 专家中心+SkillHub、Coze 商店、GPT Store | 有招聘/Skill 安装实现，无市场语言；Capability 用户语言 P1 | RECOMMENDATION CANDIDATE |
| M-07 | 完整 Settings IA（模型/Provider/员工默认/权限/隐私/数据/通知/快捷键/关于） | 全员（见 SETTINGS_MATRIX） | 仅公司档案草稿 | RECOMMENDATION CANDIDATE |
| M-08 | Usage/成本消费面（每员工/每工作用量） | Cursor usage、Coze credits、Devin ACU、Manus credits | 唯一 Usage Ledger RUNTIME ONLY | RECOMMENDATION CANDIDATE |
| M-09 | 权限政策面（这个员工能做什么/工具白名单/授权历史） | Claude tool perms、Cursor allowlist、Devin policy | Scope/授权 RUNTIME ONLY | RECOMMENDATION CANDIDATE |
| M-10 | 通知中心（结果就绪/需要决定/员工阻塞） | 全员 | 仅 CEO Desk attention 投影 | RECOMMENDATION CANDIDATE |
| M-11 | Automation / 定时任务 / 触发器 | ChatGPT Tasks、Manus schedules、Workbuddy automations（本地一手证据） | NOT DESIGNED | OBSERVATION（等用途验证后再升） |
| M-12 | Memory 产品面（公司记忆/偏好查看与编辑） | ChatGPT Memory、Manus knowledge、Coze 记忆 | 共识归档 RUNTIME ONLY | OBSERVATION |
| M-13 | 并行工作面（多员工/多 Work 并行视图） | Devin parallel sessions、Manus 并行、Zcode background | parallel multi-Work NOT IMPLEMENTED | OBSERVATION（依赖 Runtime 缺口） |
| M-14 | Computer Access 产品面 | Claude/Manus/Devin/Zcode | ADR-0046 冻结 authority，未实现 | 按裁决路径走（先 Runtime Delta Plan） |
| M-15 | 桌面壳能力（全局快捷键/菜单栏/overlay/原生窗口感） | ChatGPT/Claude/Zcode desktop | NOT DESIGNED | RECOMMENDATION CANDIDATE（Desktop App 定位必需） |
| M-16 | Dark / 1024 / 无障碍 | 竞品标配 | P2 债务 | RECOMMENDATION CANDIDATE |
| M-17 | 知识接入面（连接器/格式/同步） | Coze Knowledge、Claude connectors | bounded gap（有登记） | 已在既有 gap 登记，不重复升级 |
| M-18 | 外部发布/渠道面（内容发布到平台） | Coze channels、Manus 发布 | Channel 模型 Frozen，执行未验收 | 已在既有 gap 登记 |
| M-19 | 协作/多人（真实人多角色） | Coze 团队空间、Devin org | v1 单 CEO 红线，NOT DESIGNED | 裁决性缺席，不登记为缺陷 |
| M-20 | Voice / 语音输入 | ChatGPT/Coze | NOT DESIGNED | OBSERVATION |

## 2. Curis 独有、竞品没有的能力（保护清单——重设计时不可丢失）

1. Employee = 真实公司成员身份（Definition → Instance → Holder），非 agent 配置记录。
2. Department → Business → Workspace 责任链与 canonical scope（四层执行归属）。
3. Leader（Employee × Role × Scope Assignment）与 only-on-exception 路由。
4. Meeting：Proposal → P7 → CEO Decision → Work → Result → Evidence → Leader 再评估 的经营讨论闭环。
5. Result → Evidence 溯源与"事实先于观点"约束。
6. Company Analyst（经营洞察）与六维公司脉搏。
7. Package First 的 Workspace Engineering（专业形态可安装、可演化）。
8. 唯一 Usage Ledger 四层贯通。
9. 原装公司经营组织（fresh Company 自带两部门 + 七名原装员工）。

## 3. 明确不做（按既有裁决，防止研究越权重启）

- 独立 Admin 产品、物理多租户、计费订阅、模板商城、Marketplace 开放生态（v1 self-use 红线 + L2 Gate）。
- 多真实员工协作 seat（v1 单 CEO）。
- Project ≠ Business、Channel ≠ Workspace、Office 已退出语义——不得回潮。
