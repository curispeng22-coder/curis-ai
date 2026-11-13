# RD Product Language Candidate

Authority Class: RESEARCH
Status: Review
Date: 2026-09-21
Disposition: PRODUCT LANGUAGE CANDIDATE — CEO REVIEW REQUIRED
Owner: CEO / Product
Next Gate: 接受候选后纳入Visual Language Baseline输入；不自动Frozen或实施。

来源简称与权威级别见[本轮研究索引](../CURIS_PRODUCT_LANGUAGE_RECONCILIATION_INDEX.md)。

## 1. Business性质：围绕软件项目持续交付

RD帮助团队把目标变成可运行、可验证、可长期维护的软件。它不是IDE、Coding Agent、Issue管理台或编排框架。组织与持续责任属于Curis，编码/测试执行由合法Provider或现成工具完成。[R1,R2,R3]

Business可以有多个Software Project；项目是专业对象，不插入Company→Department→Business→Workspace层级，不恢复公司级Project Center。[A1,A2,R2]

## 2. 长期核心对象：Software Project

项目保持稳定身份、目标、阶段、上下文、工程资产、已接受变化、发布与历史。Work只是一次改变或验证项目的工作；完成一个Work不关闭Project。一个项目可关联多个仓库，仓库也不应未经关系声明就等同项目；多仓治理精确规则仍UNKNOWN。

进入已选研发Workspace，先看到当前/最近Project Overview：已接受基线、当前目标、进行中的变化、等待谁决定、下一步；多项目用Workspace内部选择与列表，0项目提供新建/接入已有项目，不能种假项目。

## 3. Project模型与经营的关系

分类为**Project-dominant**。发布后用户反馈、安全问题、技术债会形成新Work，因此有长期经营循环；这不使Workflow成为主导航。Project Overview与Current Work是核心工作面，不是需求→架构→开发→测试→部署五个固定区域。

## 4. Employee模型

Employee是长期责任承担人，不是终端、Provider会话或Coding Agent。一个Employee可承担多个Work；每件有独立目标、范围、状态与返回点。人员更替只改变当前Assignment，旧结果保留实际作者/执行来源。

Provider在执行详情和相关结果来源中出现，不做Curis员工头像或对话发言者。直接指定员工交流不能静默替换为Work Owner。

## 5. Responsibility与Assignment

需求澄清、方案、实现、验证、发布维护是可分配的长期责任，不强制五名员工或五页。依据规模与独立权限/交付需求组织团队；没有合法负责人应显示缺口。

**术语修正**：R3 §2把Assignment称作一次Provider会话指派；本候选不采用此定义。按Shared Authority §0.1，Assignment承载Employee×Role×Scope责任。一次Work可以有多次Execution及Provider尝试；它们引用责任，不重新发明Assignment。[A4]

## 6. Work模型与并行

Work至少有项目引用、目标、边界、输入基线、负责人、验收依据、依赖、结果和状态。按钮“处理这个问题”和自然语言进入同一Work，不能形成双系统。

并行实现：各自隔离执行位置、输入基线与变更范围；认领任务不等于文件锁；worktree不等于安全沙箱。多个Employee可同时改不同部分，一个Work也可用多个执行能力；收口仍由具名责任承担。Provider切换保Work identity，新增执行来源记录。[R3 §3 Q11–16]

## 7. Artifact / Candidate / Result

| 名称 | 生命周期与归属 |
|---|---|
| 工程资产 | 项目代码、文档、测试、架构，长期属于业务下该项目；不属于员工 |
| 候选变更 | 针对明确基线的一组修改；可审阅/退回/替代，尚未进入接受基线 |
| Result | 这次Work做了什么、改变什么、验证什么、未解决什么；引用产物与Evidence |
| Evidence | 测试/Build/Review/预览证据，绑定实际revision、环境与时间，不能拿旧绿灯证明新代码 |
| Accepted Project Change | 合法验收与接纳发生后，记录新的项目基线与相关Decision；不等于已部署 |

Work完成条件按目标区分：研究Work可由已接受报告完成；实现Work需要满足约定的集成/验证合同；生产发布Work还需外部效果核验。Provider退出、生成Diff、测试全绿、PR打开都不独立等于Work完成。

## 8. Conversation

项目级讨论用于明确目标；Work对话围绕当前变化；选中文件/产物交流携带该版本。共享员工身份与既有Conversation，不复制一个“项目Agent”。保持当前Project、Work与来源返回锚点；可以在不关闭Work的情况下查看证据再返回交流。

讨论阶段Conversation可为主要操作面；审阅阶段实际Diff/Preview成为主要专业内容。不要把“Conversation永远最大”或“Diff永远最大”当产品真相。

## 9. Context与交接

Project Context回答项目长期是什么；Work Context回答本次改变什么；Execution Context记录某次Provider实际运行；Conversation Context保留交流来源与责任。Business/专业方法是上游授权背景，不自动全量发送给Provider。

交接最小包：目标、当前基线、允许范围、已完成/未完成、实际变更引用、证据、未决Decision、下一动作。日志不能替代包。区分同Work换执行体、Work间交接、候选进入项目基线三类。[R3 §4.3]

## 10. Decision

方案选择是Choice；合并/敏感修改/生产发布按授权边界是Gate；跨项目优先级和资源调整是Operating Decision。RD并非只有“低频异常Gate”。每次需判定实际风险和已有授权，不能要求CEO批准每个工具调用，也不能把技术访问权限当合并授权。

## 11. Human Participation

用户可提需求、讨论设计、查看预览、要求返工、确认重要变化。普通讨论不冻结执行；输入基线/目标实质改变时形成影响与版本确认。测试不能替代产品取舍；CEO不必亲自读每行代码，但可查看独立验证及未决项。

## 12. Provider

Employee→Work→Execution→Provider→Result→Verification→Accepted Project Change。Curis复用编码、沙箱、Git、CI；负责责任、合法路由、结果关联与接纳状态，不另造Coding Framework。

R3中的具体CLI版本、四槽适配器和默认换Provider验证都是历史研究/实现建议，不作为本轮功能承诺。独立Verification强调独立依据与责任；换模型本身不证明独立或正确。

## 13. Long-running State与恢复

第二天先恢复项目接受基线、在办Work、待决事项、实际执行证据。能否恢复Provider会话需核实；无信号显示未知活动，不等于闲置/失败。未提交修改先保留再判断；已发出外部写操作效果未知时先核验，不自动重发。已通过的旧revision证据保留，新基线变动需重新检查。

本地关机不保证执行继续；后台必须启用且能力真实可用。项目不断续不等于进程永远存活。[A4,R3 §4.4]

## 14. Business Working Space资产

逻辑归属：业务→Software Project→代码/文档/测试/架构/接受历史。Canonical Project Root是RD工程资产位置；Execution Workspace是临时执行位置，不是组织Workspace。接受后的资产不能只留在Provider目录。[B1]

worktree位于资产根外、Adopt原目录、具体根路径均仍是B1候选，不在本轮设目录/Schema。全局不把Git强加给Writing/Music。业务资产归属不排斥既有Company/Department合法共享资料。

## 15. Navigation / Surface / Utility

| 层级 | 内容 | 用户动作 / 返回 |
|---|---|---|
| Workspace内项目选择 | 最近项目/项目列表/新建或接入入口 | 选择后回同Project Overview，不创建Sub-Workspace |
| 长期Surface 1：Project Overview | 当前目标、接受版本、在办变化、真实待决、下一工作 | 继续Work/提出变更/查看结果 |
| 长期Surface 2：Current Work | 目标、责任人、当前产物、讨论、证据与接纳状态 | 查看差异/交流/退回/验收→项目 |
| 对象/模式 | 需求、候选变更、Release、某个Review、Decision | 从相关工作进入，不升为独立导航 |
| Utility | Source/Diff/Preview、当前判断所需Test/Build/PR引用、执行详情 | 保Work与版本，关闭回原位置 |

“长期”指稳定产品工作面类型，不保证每个Work永远打开。正式首版Utility范围仍受A3限制，PR/Build不因本候选变成永久Tabs。

## 16. 完整路径与反证

客户反馈→项目Overview提出修复→负责人形成Work与验收范围→两名员工分别实现/验证→Provider隔离执行→候选变更→基线发生变化则重验→提出方案取舍→授权者接受→合入项目→按发布权限发布→核验线上版本→反馈产生下一Work。第二天从项目恢复，不从聊天中猜当前代码。

反证：A测试通过但B同时改接口，A不可直接接纳旧证据；Provider死亡不删除未合入变化；只做研究不强制建PR；两个项目使用同员工不互相默认泄露文件。以上均可由本候选关系解释，不需新增Project Center。

## 17. 明确不做

IDE、代码编辑器平台、Git/CI替代品、Agent编排框架、全局Project层、五区八页、统一Task Console、凭据管理副本、真实执行与迁移。

## 18. UNKNOWN

多仓Project的精确绑定与接纳边界；生产合并授权默认值；隔离实现选型；不同Provider真实交接恢复；Business Working Space物理布局。Owner为后续产品/执行验证。它们不得伪装“已实现”；前两项在涉及相应场景的详细设计前需明确。

## 19. 对Visual Language的要求

专业对象、当前工作、责任人、产物与交流形成连续关系。计划/执行/验证/已接受/已发布可区分；无依据进度百分比不作为完成证据。Project State与执行状态分开。不冻结位置、颜色或组件。

## 20. Readiness与15问结论

RD核心Product Language可提交冻结Review；本轮不冻结。15问分别由§2入口/多项目、§9 Context、§14工作资产、§4–6员工并行、§12 Provider、§7完成与Result、§15 Diff等、§10 Gate、§13次日继续、§14文件归属、§15最小两面回答。

可进入Visual/Product Baseline Candidate，但多仓/生产授权/执行实现不能据此宣布Ready。现有视觉证据只验证表达，不证明多Agent真实E2E。[V1]
