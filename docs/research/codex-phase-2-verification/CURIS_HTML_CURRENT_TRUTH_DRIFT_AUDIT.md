# CURIS HTML CURRENT TRUTH DRIFT AUDIT

Authority Class: RESEARCH / EVIDENCE
Status: Review
Date: 2026-09-13
Disposition: FOR CEO / CHATGPT REVIEW — recommendations only; NO IMPLEMENTATION

本报告直接消费 Current Authority，不重新评价其正确性。A1–A5链接及版本边界见[Reference Verification](CURIS_COMPETITIVE_REFERENCE_VERIFICATION.md#evidence--current-inputs)。以下是 **PRODUCT → HTML PROTOTYPE GAP**，不是 Runtime 当前交付结论。CURRENT仅限所观察字段，不代表整页通过。

| Surface | Disposition | 具体证据 / 错误 | Current Authority Source | 建议修复（本轮未执行） |
|---|---|---|---|---|
| Primary Navigation | CURRENT | H03七区；Conversation/Search/Settings是utility | A1；A2 §2.3 | 保持七区，勿为EvoFlow Task Center增一级导航 |
| Company/Business关系 | PARTIAL | H04专业Business入口存在；generic Workspace出现CG context | A1对象关系；A4 | 按Business/Workspace实例提供context，不共享业务fixture |
| CEO Desk | MIXED | Brief标题4项实有6行；工作人数与身份数不一致；H29空态混有已有工作 | A1 CEO operating model | 同一状态fixture保持对象、计数、empty一致 |
| Content Growth identity | CURRENT | H05以Content Growth Workspace为业务工作面；未观察Office/Channel替代Workspace标题 | A4 CG canonical Workspace | 保留；旧文件名xhs不能单独作为UI违规证据 |
| Content Growth专业链 | PARTIAL | H06一个DOC聚合发布状态；未显现按账号Variant/Publication/receipt/eligibility | A4 Opportunity→Intent→TargetAccountSet→Variant→Publication | 实现当前domain对象关系及详情；Candidate不可写Verified |
| Content Growth Account | PARTIAL | 已连接/未连接账号可见；target包含未连接账号 | A4连接与资格、目标集分离 | 保留target历史；独立展示eligibility与connector receipt，不能把聚合已发布当逐账号成功 |
| Content Growth calendar | PARTIAL | H07点击日历无变化；只是可见按钮 | A4默认Operating与共享工作区 | 补可验交互；不把按钮当Calendar完成 |
| RD专业工作面 | PARTIAL | H08代码/测试/评审/发布区与CG真实不同；Holder/Executor未独立完整呈现 | A5 §1a current supersession；RD实例 | 使用current实例字段与持有人/执行人分离；ReviewRequest不等于handoff |
| RD工作状态 | MIXED | Header联调中/回归阻塞，与Banner联调完成/回归进行中矛盾 | A5 runtime projection | 同一工作状态来源一致；状态不得自动决定Pane展开 |
| RD Decision | WRONG | H08高风险发布Banner可直接批准 | A2 §3.13 P7 | Layer0仅查看方案/暂缓；选择放Layer1，保留Decision与Handoff区分 |
| Four-Pane Shell | PARTIAL | H09 widths220/256/588/360；Context/Utility可开关，并非始终四列；无resize/maximize/记忆闭环 | A2 T1–T3与pane contract；A5 supersession | 修T1导航header、T2 Main常驻、T3迁移；关闭不另造X；按scope记忆宽度与可见性 |
| Context | WRONG | H12完整员工profile占Context；H25普通Workspace带CG选题/内容日历 | A2 Context职责与Detail归属 | Context只承载导航/工作范围，完整Detail进Utility；专业上下文分域 |
| Employee entry | STALE | H12默认Main profile/work而非Conversation；header对话按钮实测无效 | A2 §3.1/§3.14 | Main默认Conversation；avatar/name打开Utility Detail |
| Employee UI Status | CURRENT | H34使用空闲/工作中·desc/阻塞·cause | A2 Employee三态 | 保持；Work/Result“已完成”合法，不误报Employee违规 |
| Employee Current Work | MIXED | header工作中，但详情提示无Current Work | A2员工身份与工作投影 | 统一数据与选中工作；身份不合并Agent配置 |
| Shared Composer | STALE | H14固定模型/员工/权限按钮，H15运行时控件全替换；附件常量、send不追加、draft重绘丢失 | A2 §3.5 shared composer；A5禁止旧Compact规则 | 一个共享实现消费Input/Add/Access/WorkMode/Context/Model语义，先完整状态后量像素 |
| Model / Permission | PARTIAL | H16未配置模型可选；权限只是轮换文字，不区分effective | A2 §3.5；Shared Patterns provider truth | 请求/配置/实际生效分离；unavailable应解释并禁用 |
| Agent Work | PARTIAL | H21 Context与Main重复计划；缺真正tool进度与停止/继续 | A2工作投影；A1 Work/Result | 计划/当前动作/等待/结果分层；EvoFlow反例要求保留停止输出 |
| Result / Evidence | PARTIAL | H26正文与usedBy存在；H27tabs无动作；继续讨论不携带Result；Evidence仅字符串 | A1 Result→Evidence；A2 Utility | 可追溯证据、Source/Preview和对象引用返回Conversation；不复制媒体编辑器到所有结果 |
| Talent / Skill | PARTIAL | H17/H18区分入口但共享大卡；外部Candidate标签存在 | A1 Talent/Employee区别；A2共享pattern | 专家与技能分别匹配对象/动作，招入不等于启动AI |
| Settings | PARTIAL | H22左类右表单有结构；无搜索、保存未接Runtime | A2设置/global utility；A3 | 按当前Curis设置范围修交互，不复制Cursor旧MCP分类 |
| Search | PARTIAL | H19对象搜索浮层存在；Enter无动作、preview占位文本 | A2 §2.3.1 | 只做对象搜索闭环；Command仍预留，不擅自加派工/会议动作 |
| CEO Assistant | WRONG | H23全局入口正确，但展开抛ico错误，只剩空白面；路由切换仍残留 | A1 global floating；A2 Assistant | 修现有全局宿主的展开/收起/输入/恢复，不改Drawer或Pane |
| Visual | CURRENT | Iris #806BE5已使用；本轮可见Surface未发现绿品牌主色 | A3 Frozen Visual Standard | 保留品牌；视觉CURRENT不等于密度/交互验收 |
| Empty / Error | MIXED | H29空态与工作混合；H30失败同时显示已同步；H28选择Error却显示普通Result | A2 shared状态与反馈 | 每个宿主拥有一致empty/loading/error/retry，错误不能只是fixture selector |

## 专业 Business 的 P0 裁决

**Same Company OS, Different Professional Workspaces：PARTIAL，未通过完整验收。** 二者共享七区/Shell，并且CG真实呈现内容/账号、RD呈现代码/测试/评审/发布，故不是“只换标题”，也没有做成两套软件。但专业对象连续性与状态真实性不足。

Content Growth **部分消费最新Authority**：Workspace命名和Operating投影正确，账号与连接状态已有入口；当前聚合DOC不足以证明Opportunity→Intent→TargetAccountSet→逐账号Variant/Publication，更无按账号receipt验证。连接断开不应抹去历史目标，target包含断连账号不是本身错误；错误在把聚合成功替代具体发布资格/结果。没有将Candidate升级为Verified的证据。

RD **部分消费当前实例，未完整消费Frozen Shell supersession**：专业上下文存在，Shared Composer/T控件/Pane交互仍旧实现。高风险直接批准、同一任务冲突状态是优先问题。旧RD正文规则已被顶部Current Supersession覆盖，不因此重新发起Authority冲突。固定宽度不等于已观察到runtime autoexpand；本轮未以不可复现的自动展开作事实。

## 明确排除的误报

- “小红书”作为账号/内容渠道名合法；不能以历史文件名含xhs就宣称Channel=Workspace。
- Result v1.3被v1.4引用可以是正确baseline关系，不单独判旧数据。
- Employee之外的Task、Review阶段、Result完成状态不是Employee三态违规。
- 未验证1024 viewport；H31/H32实际1440，不能写响应式通过或失败。
- 本轮不读竞品私有内部Schema；也不把静态HTML Save当Runtime持久化。

## 实现定位

[views-business.js](../../prototypes/full-product-html/js/views-business.js)：123–138 Context fallback；178 Calendar；179–184 CG聚合内容；195 release banner；198阶段；216状态；267计划；316–350 Result；375 Conversation。
[views-core.js](../../prototypes/full-product-html/js/views-core.js)：CEO empty/error与Employee详情。
[app.js](../../prototypes/full-product-html/js/app.js)：95–124 Pane/render；115–117 Utility tabs；155–184 Search；197–223 Assistant；258–267 send；315–335控件。
[components.js](../../prototypes/full-product-html/js/components.js)：99–137 Conversation/Composer；146 Decision。
[curis.css](../../prototypes/full-product-html/css/curis.css)：37–54布局；143行；182 Conversation；206–214 Composer；254 Search。

这些定位用于下一轮正式修复Issue拆分，不构成修改授权。本轮未修改上述文件。
