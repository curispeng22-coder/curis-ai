# CURIS_HTML_CURRENT_TRUTH_DRIFT_RECHECK

> Authority Class: RESEARCH / EVIDENCE · Date: 2026-09-13
> 逐项消费 CURIS_HTML_CURRENT_TRUTH_DRIFT_AUDIT.md 25 Surface 裁决后的复检结果。

| Surface | 修复前 | 修复后 | 证据 |
|---|---|---|---|
| Primary Navigation | CURRENT | CURRENT（保持七区，未加 Task Center 导航） | 全局 |
| Company/Business 关系 | PARTIAL（generic 混 CG context） | **CURRENT**：generic/宠物寄养 context 为自身域；无业务间共享 fixture | 22/29 |
| CEO Desk | MIXED（计数/空态混合） | **CURRENT**：简报 4 项=4 行；emptyFirst 独立空 fixture；needsCEO 独立 | 01/25 |
| CG identity | CURRENT | CURRENT（内容增长工作空间） | 03 |
| CG 专业链 | PARTIAL | **CURRENT（结构级）**：五段对象链逐层呈现，逐账号资格/回执分离 | 04 |
| CG Account | PARTIAL | **CURRENT**：Target≠Eligibility 显式；断连账号保留历史目标 | 04 |
| CG calendar | PARTIAL | PARTIAL（保留：日历切换为 P1，不冒充完成） | 04 |
| RD 工作面 | PARTIAL | **CURRENT（结构级）**：Holder≠Executor、ReviewRequest≠Handoff 独立块 | 19 |
| RD 状态 | MIXED | **CURRENT**：全局单一来源（联调中 80%/回归阻塞），banner 与 header 一致 | 05/21 |
| RD Decision | WRONG | **CURRENT**：Layer0 仅 查看方案/暂缓；Approve/Reject/Choice→Layer1 | 05/21 |
| Four-Pane Shell | PARTIAL | PARTIAL→大部分 CURRENT：开关位置正确、Utility 最大化+Esc、1024 折叠；divider resize/宽度记忆 未做（P1 如实保留） | 06/29 |
| Context | WRONG | **CURRENT**：员工 Context=bounded 工作范围；完整档案在 Utility；generic 无 CG context | 08/28 |
| Employee entry | STALE | **CURRENT**：Main 默认对话；姓名→Utility 档案；header 按钮有效（进入对话 Tab） | 08 |
| Employee UI Status | CURRENT | CURRENT（三态不回退） | 08 |
| Employee Current Work | MIXED | **CURRENT**：header 状态与详情工作同源 fixtures | 08/28 |
| Shared Composer | STALE | **CURRENT（语义级）**：RT 状态机消费完整槽位；运行不消失；附件/引用为对象；requested≠effective 说明 | 08/17 |
| Model / Permission | PARTIAL | **CURRENT（语义级）**：未配置模型解释并禁用；权限 requested/configured/effective 说明行 | 24/08 |
| Agent Work | PARTIAL | **CURRENT（结构级）**：首层六问概览（Context）+计划/当前动作/工具折叠/协作/交接；Env/Git 未做次层 Inspector（Utility=工具列表，P1） | 19 |
| Result / Evidence | PARTIAL | **CURRENT（结构级）**：Preview/Source 真切换、Follow-up 回对话；Evidence 仍为字符串列表（结构化对象 P1） | 27 |
| Talent / Skill | PARTIAL | **CURRENT**：专家/技能独立卡；外部 Candidate 边界标注 | 09/10 |
| Settings | PARTIAL | PARTIAL（左类右容保持；搜索/保存 Runtime 接线 P1） | 15 |
| Search | PARTIAL | **CURRENT**：键盘闭环+真实预览；Command 预留未越权 | 17 |
| CEO Assistant | WRONG | **CURRENT**：展开正常、四态、输入保持、无 console error | 26 |
| Visual | CURRENT | CURRENT（Iris #806BE5 唯一 accent） | 全部 |
| Empty / Error | MIXED | **CURRENT**：emptyFirst 独立 fixture；error 隐藏"已同步"并显示同步失败；Retry 重新触发发送 | 01 |

**总计：WRONG 3→0 · STALE 4→0 · MIXED 4→1（保留 1 项：State Switcher 下静态侧栏计数不随叙事状态变化——设计工具定位，理由如上） · 其余 PARTIAL 如实保留并登记 P1。**

## 视觉重构轮追加复检（2026-09-13 第二次）

- 本轮纯视觉重构 + 六项补完（Meeting Room / Insights chart / CG 日历 / Settings 搜索与保存反馈 / Message Actions More / 附件上传失败态 / Utility divider resize）。
- Product Truth：WRONG 0 · STALE 0（未回退任何已固化结论；七区/Office/Channel/三态/Iris 全部保持）。
- MIXED 1 项维持（State Switcher 静态侧栏计数），理由同前。
- 新增交互全部消费 Current Authority：CG 日历=Operating 週期视图（Candidate）；Meeting Room 消费 Structure Baseline §10 语义（Proposal→决议→Work）；Insights 消费 EST/provenance 纪律。

## CEO 第三轮纠偏（2026-09-13 · 导航与信息架构）

| 指正 | 依据 | 修正 |
|---|---|---|
| 导航被自创分为"工作区/组织与运营"两类 | Structure Baseline：七个一级区固定，"后续视觉研究不得自行增删一级区" | 导航改为七区**平铺**，删除所有自创分组 |
| 侧栏缺少对话 Quick Access（与员工直接对话常驻，不因离开页面消失） | Structure Baseline §94：Navigation 承载七区 + Conversation Quick Access + CEO/settings utility | 侧栏新增"对话 · Quick Access"：员工对话常驻（状态 dot + 角色），点击直达对话 |
| 左下应为 CEO 头像+名称（用户信息），上拉弹出模型配置/设置 | EMPLOYEE_CONVERSATION_MODEL_EXPERIENCE_CONTRACT（左下 CEO 头像菜单）+ Structure Baseline（CEO/settings utility） | 左下=头像 + CEO + 公司名；上拉弹出：模型配置/AI 能力设置、个人设置、公司设置 |
| "成果库"是哪一版的？ | 七区不含成果库；Result/Evidence 属 Workspace/对象链 | 从导航移除；Result 经 Result Reference/员工/工作路由到达（#/results 保留为对象列表路由） |
| 每个 Surface 页都重复"工作区"是否正确 | Frozen Shell Delta-X9：Main=Surface+共享工作区；B 代各 Surface 实拍中工作区不逐页重复 | 共享工作区只在经营总览呈现；其他 Surface 专注域对象，Context 提供"员工工作区"入口 |
