# CURIS PRODUCT BLUEPRINT CHANGE PLAN

> **2026-09-15 CEO Acceptance / Consumption record**
> 本报告整体仲裁已由CEO接受；F1人工接续≠Decision，F2选择Option A（opt-in本地后台目标）。批准子集已由本轮Product Truth Consolidation写回唯一Blueprint / Master Map / UI Blueprint / Shared / Domain。
> 本文件继续 **Status: Review · Authority Class: PROVENANCE / REVIEW HISTORY**，不是Current Router或Implementation Acceptance。下文保留审查当时的候选/F2待决/本轮不写入等原文，仅为历史时间点；不得重新开放已决定方向。
> Disposition: CONSUMED BY CURRENT PRODUCT TRUTH。Owner: Product Authority。Next Action / Gate: [Consolidation Review](CURIS_PRODUCT_TRUTH_CONSOLIDATION_REVIEW.md) → CEO FINAL PRODUCT TRUTH REVIEW。G1-V～G6-V仍NOT RUN。


Status: Review  
Authority Class: REVIEW / PROPOSED CHANGE PLAN  
Disposition: PLAN ONLY — REQUIRES CEO ACCEPTANCE AND SEPARATE EXECUTION AUTHORIZATION  
Date: 2026-09-15  
Owner: CEO / Product Blueprint Authority  
Source: [Deep Reconciliation](CURIS_PRODUCT_BLUEPRINT_DEEP_RECONCILIATION.md)  
Target Authority: existing canonical Product / Shared / Domain chain  
Next Gate: CEO FINAL RECONCILIATION REVIEW  
Boundary: NO AUTHORITY EDIT / NO IMPLEMENTATION / NO UI / NO COMMIT / NO PUSH

## 1. Scope / Preconditions

这不是新的Blueprint，也不是待自动执行的补丁。主报告110项裁决、77项Settings分层与本计划共同供CEO审阅。只有CEO接受仲裁并明确授权下一轮Consolidation后才实施。

唯一未定方向：**F2：opt-in用户级Local Background Service目标，还是App-bound执行目标**。F1人工接续按已有P1人工反馈和Frozen ADR-0046技术授权≠CEO Decision修正Shell绝对句；不要求CEO重新选择是否允许正常技术授权，但Frozen编辑仍须在接受本轮方案后执行。

所有目标能力都与Current Implementation分开。G1-V～G6-V没有执行；不能因为本计划写ADD就更新CURRENT_STATE为Implemented。本计划不修改Autonomous V1 / Business Spine Issue，也不修改Package Technical Architecture。

## 2. 文件编号与精确路径

编号与主报告一致；以下仅列可能受影响的正式载体。适用Shared尚未分成独立文件的内容，先放已有Owner的明确章节；如阅读/责任边界确实要求独立合同，再由CEO在Consolidation范围中确认，不能默认G1–G6各建新文件。

|ID|文件|建议处置|
|---|---|---|
|P0|[docs/00_Context/PRODUCT_DOCUMENT_POINTER.md](../../docs/00_Context/PRODUCT_DOCUMENT_POINTER.md)|按下表必要章节处理，不能整篇升级状态|
|P1|[docs/01_Product/Curis_Product_Blueprint.html](../../docs/01_Product/Curis_Product_Blueprint.html)|按下表必要章节处理，不能整篇升级状态|
|P2|[docs/01_Product/Curis_Product_Master_Map.md](../../docs/01_Product/Curis_Product_Master_Map.md)|按下表必要章节处理，不能整篇升级状态|
|P3|[docs/01_Product/Curis_Product_UI_Blueprint.html](../../docs/01_Product/Curis_Product_UI_Blueprint.html)|按下表必要章节处理，不能整篇升级状态|
|P4|[docs/01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md](../../docs/01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md)|按下表必要章节处理，不能整篇升级状态|
|P5|[docs/01_Product/Curis_Product_Context.md](../../docs/01_Product/Curis_Product_Context.md)|按下表必要章节处理，不能整篇升级状态|
|S1|[docs/03_Design/Curis_Company_OS_Shared_Authority.md](../../docs/03_Design/Curis_Company_OS_Shared_Authority.md)|按下表必要章节处理，不能整篇升级状态|
|S2|[docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md](../../docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md)|按下表必要章节处理，不能整篇升级状态|
|S3|[docs/03_Design/CURIS_VISUAL_STANDARD_V1.md](../../docs/03_Design/CURIS_VISUAL_STANDARD_V1.md)|保留；仅必要scoped引用/历史适用性，不自动修改|
|S4|[docs/reviews/CURIS_CORE_PRODUCT_AUTHORITY_REPAIR.md](../../docs/reviews/CURIS_CORE_PRODUCT_AUTHORITY_REPAIR.md)|保留；仅必要scoped引用/历史适用性，不自动修改|
|D1|[docs/03_Design/Curis_Content_Growth_Domain_Authority.md](../../docs/03_Design/Curis_Content_Growth_Domain_Authority.md)|按下表必要章节处理，不能整篇升级状态|
|D2|[docs/03_Design/Curis_Content_Growth_Operating_Strategy_UX_Translation.md](../../docs/03_Design/Curis_Content_Growth_Operating_Strategy_UX_Translation.md)|按下表必要章节处理，不能整篇升级状态|
|D3|[docs/reviews/CONTENT_GROWTH_CEO_AUTHORITY_DECISION_RECONCILIATION.md](../../docs/reviews/CONTENT_GROWTH_CEO_AUTHORITY_DECISION_RECONCILIATION.md)|保留；仅必要scoped引用/历史适用性，不自动修改|
|D4|[docs/03_Design/Curis_RD_Workspace_Instance_Spec_v1.md](../../docs/03_Design/Curis_RD_Workspace_Instance_Spec_v1.md)|按下表必要章节处理，不能整篇升级状态|
|D5|[docs/03_Design/Curis_RD_Design_Phase_Closeout_2026-08-15.md](../../docs/03_Design/Curis_RD_Design_Phase_Closeout_2026-08-15.md)|保留；仅必要scoped引用/历史适用性，不自动修改|
|W1|[docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Methodology.md](../../docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Methodology.md)|保留；仅必要scoped引用/历史适用性，不自动修改|
|W2|[docs/05_Workspace_Engineering/CURIS_WORKSPACE_ENGINEERING_PRODUCT_HANDOFF.md](../../docs/05_Workspace_Engineering/CURIS_WORKSPACE_ENGINEERING_PRODUCT_HANDOFF.md)|保留；仅必要scoped引用/历史适用性，不自动修改|
|L1|[docs/reviews/CURIS_OPERATING_LIFECYCLE_CONTRACT_CANDIDATE.md](../../docs/reviews/CURIS_OPERATING_LIFECYCLE_CONTRACT_CANDIDATE.md)|按下表必要章节处理，不能整篇升级状态|
|I1|[docs/00_Context/CURRENT_STATE.md](../../docs/00_Context/CURRENT_STATE.md)|保留；仅必要scoped引用/历史适用性，不自动修改|
|S5|[docs/01_Product/AI_Capability_UI_Contract.md](../../docs/01_Product/AI_Capability_UI_Contract.md)|按下表必要章节处理，不能整篇升级状态|
|S6|[docs/07_Decisions/ADR-0046-local-agent-computer-access-authority.md](../../docs/07_Decisions/ADR-0046-local-agent-computer-access-authority.md)|保留；仅必要scoped引用/历史适用性，不自动修改|
|S7|[docs/reviews/CURIS_EMPLOYEE_CONVERSATION_MODEL_EXPERIENCE_CONTRACT.md](../../docs/reviews/CURIS_EMPLOYEE_CONVERSATION_MODEL_EXPERIENCE_CONTRACT.md)|按下表必要章节处理，不能整篇升级状态|
|S8|[docs/reviews/CURIS_SETTINGS_PRODUCT_CONFIGURATION_RESEARCH.md](../../docs/reviews/CURIS_SETTINGS_PRODUCT_CONFIGURATION_RESEARCH.md)|保留；仅必要scoped引用/历史适用性，不自动修改|

## 3. Blueprint Change Plan

Judgment列引用主报告唯一裁决；Action严格限定为本表的动作，不授权Runtime或UI设计。P1只保核心关系/原则；字段细节下沉，不把全部ADD都加进Blueprint。

|Target|Section|Current Truth|Judgment|Proposed Final Truth|Action|Downstream Impact|
|---|---|---|---|---|---|---|
|P1|§1/12/14 North Star / 三层|一人AI公司/成熟复用已有|R001/018/024|强调装配成熟能力形成经营责任与真实结果，不自称最强模型|CLARIFY|P2定义/P3用户语言，S1 Owner不变|
|P1/P2|§13 / 产品规划顺序|一级产品→动作→页面→能力绝对顺序|R106 / F3|经营证据→能力边界→在既有结构落位；仍禁止Runtime主导导航|CLARIFY|W1方法引用；非新IA|
|P1/P4|Company/Dept/Business/Workspace及原装组织|canonical链＋6+1/Assistant＋Business0|R003–009|保留；补能力不能删除Department或强制CEO先填组织|NO CHANGE|所有Shared/Domain继续消费|
|P1/P5/S1|Employee/责任/Provider|同员工多Assignment，Provider供给能力|R010–015/020/024/057|明确多处投影同身份，能力可变；角色≠系统权限|CLARIFY|Map Employee/Profile、UI真实身份|
|P5|§1.1 Conversation与§2默认组织|部分旧句仍强分Conversation/可无初始Dept|R007/075；旧残留台账|按P4/S4现有裁决同步；消息/引用scope隔离，原装部门真实存在|REPLACE|仅模块入口，非新产品模型|
|P5|Office隐喻/旧平台Workspace/版本引用|尚可误读旧用户identity|R006/080–081；D3|Workspace用户身份；Office历史provenance；版本引用当前canonical|CLARIFY|不rename Runtime字段或历史文件|
|P1/S2|人工参与/P4 §3.11|Human action only at Decision Gates|R051 / F1 / S6|自治默认但必要人工执行/授权/补材料合法；不得伪装P7或自动P5|REPLACE|S1责任/Domain交接/Map恢复动作；需CEO接受本次窄幅Frozen修正|
|P1|能力范围概述|有成熟工具原则，无完整Browser承诺|R025/027/028|Search/Reader/Interactive Browser目标能力分开、按权限可用|ADD|具体合同下沉S5及适用Shared，不Browser一级区|
|S5/S6|Browser/Computer相关共享能力合同|Review已有Profile；S6三档访问Frozen|R025–028/102|安全浏览、账号隔离、接管/恢复；复用S6技术授权与真实生效区别|ADD|不改三档；GUI-only Agent需外部配置的限制不被Browser候选绕过|
|S5/S7|§3/5 Model/Provider与配置使用|三态/来源已在Review；P3采用配置使用分离|R019/023/024|多连接/发现完整性/用途测试/fallback合同，保无逐员工手配前置|ADD|P2模型字段；P3配置Main/使用Composer；审过内容才成为Shared真值|
|P1/P5|Background目标承诺|LocalDesktop和restart不等关UI继续|R052 / F2|若CEO选A，opt-in本地后台与显式停全体；否则保持App-bound并明确限制|ADD|F2批准前不执行；影响退出/Settings/恢复说明|
|L1/适用Shared|调度/WAIT/恢复|bounded Cycle/三触发/nextCheckAt已有|R042/053/055|补后台边界、错过合并检查、效果未知恢复，不变one-active合同|ADD|技术持久化/lease另Gate；不改Autonomous V1 Issue|
|S1/适用Shared|Execution/Decision/Result|已有Work/P7/证据恢复|R044–048/055|动作快照、授权失效、远端效果确定性、原Work恢复|ADD|Implementation必须先映射现有字段，不本轮建enum/表|
|P1|真实结果/安全原则|内部完成≠外部结果已有|R047–050/055|保留并指出未知副作用不能以失败重试制造新事实|CLARIFY|S1/S2引用共享恢复；Business/Company结果归属不变|
|S5/适用Shared|File/Tools/Reference能力|已有局部专业工具和md/txt接受|R029–036|文件版本/冲突；Terminal/Git/Preview/OCR/Data/Media按动作能力合同|ADD|RD/CG采用，Library不变文件后台；实现G5-V|
|P1/P2/P3|专业工具细节去向|RD旧DESIGN NOW/Reserved是范围记录|R030–035|目标工具能力不强塞Blueprint或假当前可用；专业工作按Main/Utility职责|MOVE TO SHARED CONTRACT|后续正式页面合同消费新能力，不追认旧设计完成|
|适用Shared / Settings|Backup/Recovery|现有备份字样与局部机制|R097|DB/ManagedFiles/manifest/preflight/reconnect/resumecheck，秘密排除|ADD|P2恢复字段；P3状态/返回；实现G6-V|
|S1/S5/适用Shared|资源/数据外发/更新/诊断|scope与权限原则已有|R098–104|限定资源冲突、版本复验、数据来源、诊断脱敏/单独发送|ADD|内部锁/owner/lease/库参数下沉，不增加管理中心|
|P1/P2/P3|七区与Four-Pane|七区/独立浮动Assistant/工作Main|R062–079|保留；新工具就地进入，不新增一级导航、不强制四列|NO CHANGE|UI composition仍开放|
|P2|Company/Business/Employee/Settings字段合同|已有字段展开；不是空白Map|R018–036/042–060/097–104|仅追加已接受能力字段和失败/恢复/来源/权限/回程，标Target vs delivered|ADD|不复制77字段或所有实现参数|
|P3|能力/模型/对话/工具/恢复信息责任|继承Shell Slots；旧实施/Figma登记有时间边界|R070/073–079|按已接受Shared表达真实状态，复杂操作Main、辅助Utility|CLARIFY|不画UI，不冻结具体Drawer/卡数/像素|
|P3/P5/S2引用|Employee状态/Conflict术语|三态与其他状态易混|R078/105|保持员工三态；来源不一致=需核实；工作/资源冲突不升Global enum|CLARIFY|N2受影响字段修正后才可作UI输入|
|D1|§1.2/4 Channel Account|Company资产/账号策略/WorkspaceBinding已有|R080–083/095|扩长期经营目标/策略/节奏/计划/反馈/学习关系，不新增execution scope|ADD|P2 Domain字段；P3账号对象视图；L1不建Account控制Runtime|
|D1|§1.3–1.5 Intent/Variant/Publication|共享Intent、逐账号Variant/回执已有|R084–089/096|平台形态＋账号语境、批准版本/目标、结果确定性、排程时间分型|CLARIFY|技术Provider映射另验；不硬冻平台数值|
|D1|§4/5 Provider/Analytics/人工|数据未知与职责Owner已有|R088–095|员工负责发布/分析，Provider供给动作与数据；真0/未采集/失效/过期分开|ADD|Human接续引用Shared；无第二Analytics/钱包|
|D2/N5/N6|候选经营体验|账号策略体验已有Approved Candidate/Review|R080–096|消费必要语义到D1后研究保留，不并列为新Current Domain|MOVE TO DOMAIN CONTRACT|不冻结8状态/4桶/8Tab，N6本身不自动Approved|
|D4/D5|Main工位栈/旧首版Shared规则|页首已明确Shell优先|R030–032/073/079|对象责任保留，旧Main=整个工位栈明确历史适用；专业对象Main优先|CLARIFY|不重研RD，不恢复旧Compact Composer/视觉Token|
|W1/W2|专业方法/Package|W1更新，W2部分旧交接状态|R037/106|Package First不变；新工具按能力接入；历史W2不默认必读|NO CHANGE|不修改Package Technical Architecture，不新增Playbook|
|P0|Current Required Input / scoped routing|唯一Current入口已可用|R107/109/110|CEO消费后链接唯一Shared/Domain内容；Research只provenance|CLARIFY|本轮不改；future link/authority checks|
|Change Log / Review disposition|此次Consolidation登记|本报告尚未消费|全部提案|未来仅记录实际接受/实际变更及supersession，不写研究已实现|ADD|I1只登记真实实现与Target Gap，不运行/实现|
|N4/技术合同|G1–G6 OSS/验证细节|PROPOSED，G-V NOT RUN|R108/109|保持技术候选与验证门；不复制进Blueprint|MOVE TO IMPLEMENTATION CONTRACT|选型/许可/版本/隔离实测另Scope，非本轮授权|
|N2|全稿§7/§8/V面/组件数量|研究Expression不是Current UI|R070/107|按主报告§13/14提取；拒绝全部配置/新中心等解读|MOVE TO SHARED CONTRACT|UI-ready仅消费被接受子集；原文保留Research|

## 4. KEEP / 无需改写的核心结构

保留R002–017、R037–043等行中明确KEEP的目标；完整39项KEEP见主报告。尤其不改变：

- Company→Department→Business→Workspace、Business至少一个Workspace、Business0的Company初态。
- 原装空间工程6员工、至少1 Company Analyst与same canonical Assistant；增减/替换不复制身份。
- Employee×Role×Scope，Holder≠Executor；已有四scope基础设施不等四层自治验收。
- Work / Execution / Result / Evidence / P7 / Usage唯一；Provider对象只作执行引用。
- 七区、Four-Pane、浮动Assistant、对话持续性；共享Composer全部功能槽位。
- Approved Strategy Envelope、bounded Cycle、one active Workspace Cycle、显式Next、PAUSE/STOP分离。
- Package First、方法引用组合、不新增Playbook；Generic合法、专业≠Verified。

不因为新研究未复述上述内容就REMOVE。没有推荐删除任何一级产品区或canonical对象。

## 5. Frozen edit boundary

F1修改P4绝对句，不改P5 Handoff成万能人工队列、不改变P7决定Owner。F2仅在CEO选定后写产品承诺。F3方法顺序澄清不能从工具清单反推导航。F4扩Channel Account现有合同不建Account execution scope。F5只是必要Shared能力契约，不等技术库Frozen。

S6现有三档Computer Access保持：请求批准/自动处理/完全访问均是意图与真实生效分离；不能用本轮Browser候选绕过GUI-only Agent需要外部配置等现有限制。真新Adapter能力须独立授权验证。S5整篇目前Review，只能将接受部分明确消费，不能一键改全篇Frozen。

## 6. 最小执行顺序（仅计划）

1. CEO确认主报告/F2，并固定本次被消费内容清单。未选定前保留两个后台选项，不用默认实现掩盖产品选择。
2. 先落Shared必要合同与D1 Domain增量，保留现有对象Owner/状态等级；关键字段、失败/恢复和scope关系必须写清。
3. P1压缩登记核心原则/目标能力与明确指针；P5/P4仅同步受影响概述。不要另建Blueprint V2。
4. P2展开被接受字段/动作/Entry/Reverse Entry/Unknown与source；不把全部S077等技术参数抄成普通设置。
5. P3仅同步结构承载/真实状态/Shared引用；旧Figma与研究不能升级Final Visual，NO DESIGN。
6. 最后P0与Change Log登记真实消费，研究文件保持provenance；必要的旧句明确supersession。
7. 按下一节完整验证后才宣布PRODUCT TRUTH FROZEN FOR UI INPUT。若实现载体需要新primitive，单列Architecture Gate，不自行实现。

整个过程是一次有边界的Consolidation；没有权限创建第二Work/Result/Employee/Usage、Account Runtime或任意Provider框架。

## 7. Required validation before future freeze

|检查|通过条件|
|---|---|
|Authority一致性|P1/P2/P3/P4/P5/S1/S2/D1适用Current句一致，旧段有明确scope/supersession|
|Pointer|Current Required只指Current/明确适用Accepted子集，0 missing；Research不是隐含必读|
|Current vs Target|G-V未验项仍未交付；保留既有Accepted与Candidate原等级，不扩大完成度|
|Blueprint vs Shared|核心原则不与三档权限/Composer/P4/P5/P7相冲突，Shared只有一个Owner|
|Blueprint vs Domain|Account/Channel不是Workspace或execution scope；平台规则/Provider不污染Core|
|UI-ready|关键输入/输出/状态/权限/恢复/返回已明确；字段不等固定Card/Tab|
|重复系统|没有第二Work/Execution/Result/Employee/Decision/Usage/Company Truth|
|产品语言|内部机制不强迫普通CEO配置；不把SDK/协议/lease写成业务操作|
|Frozen gate|F2方向记录，F1等修改有明确CEO接受来源；没有Research静默覆盖|
|实施边界|无Runtime/Schema/DB/前端改动，未修改既有Autonomous V1 Scope/Start Gate|
|文件验证|Markdown本地目标存在、HTML解析、git diff --check；只触及授权exact paths|

## 8. Research / supersession处理

当前N1–N9/E1/E2保留原状态。未来CEO接受后，登记“哪些段被哪份Current合同消费”，而不是把整份研究标Current。被拒绝的方案保留拒绝理由；已有superseded旧Shared/Office/Figma只按已有决定引用，不机械删除历史。

Source-of-truth路由仍是AGENTS→P0→P1→必要Shared/Domain；不会新增Manifest或平行Development Pointer。主报告/计划/Target Map均是Review，不得作为实施已经获准的凭据。

## 9. Handoff

Verdict: **PLAN READY — SUBJECT TO CEO RECONCILIATION ACCEPTANCE**  
Owner: CEO / Product Authority  
Disposition: NOT EXECUTED  
Next Action: 确认F2及仲裁建议，另授权PRODUCT TRUTH CONSOLIDATION  
Next Gate: CEO FINAL RECONCILIATION REVIEW

STOP。本轮只交付计划，不修改Authority、代码、UI、数据库，不commit/push。
