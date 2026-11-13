# CURIS PRODUCT BLUEPRINT DEEP RECONCILIATION

> **2026-09-15 CEO Acceptance / Consumption record**
> 本报告整体仲裁已由CEO接受；F1人工接续≠Decision，F2选择Option A（opt-in本地后台目标）。批准子集已由本轮Product Truth Consolidation写回唯一Blueprint / Master Map / UI Blueprint / Shared / Domain。
> 本文件继续 **Status: Review · Authority Class: PROVENANCE / REVIEW HISTORY**，不是Current Router或Implementation Acceptance。下文保留审查当时的候选/F2待决/本轮不写入等原文，仅为历史时间点；不得重新开放已决定方向。
> Disposition: CONSUMED BY CURRENT PRODUCT TRUTH。Owner: Product Authority。Next Action / Gate: [Consolidation Review](CURIS_PRODUCT_TRUTH_CONSOLIDATION_REVIEW.md) → CEO FINAL PRODUCT TRUTH REVIEW。G1-V～G6-V仍NOT RUN。


Status: Review  
Authority Class: REVIEW / PROPOSED PRODUCT RECONCILIATION  
Disposition: READY WITH CEO DECISIONS — NOT CURRENT PRODUCT AUTHORITY  
Date: 2026-09-15  
Owner: CEO / Product Blueprint Authority  
Target Authority: 唯一 Product Blueprint 与适用 Shared / Domain Contracts（本轮不写入）  
Next Action: CEO裁决F2，审阅F1治理修正及本报告全部建议；接受后单独授权一次性Consolidation  
Next Gate: CEO FINAL RECONCILIATION REVIEW  
Implementation: NO IMPLEMENTATION / NO UI / NO COMMIT / NO PUSH

## 1. Background / Executive verdict

**B. READY WITH CEO DECISIONS。** Company OS、Company→Department→Business→Workspace、统一Employee、责任驱动经营、七区、Four-Pane、Package First不需要重建。新研究主要补齐真实工作所需的共享能力与安全合同，而非创造“另一个Curis”。

110个议题的建议分布：KEEP OLD 39，CLARIFY OLD 22，MERGE 30，MOVE DOWN 13，ACCEPT NEW 3，REJECT NEW 2，CEO DECISION REQUIRED 1。**这是议题计数，不是产品改变百分比**；同一主题可能跨多个议题。三个ACCEPT NEW是Interactive Browser完整产品能力、外部效果确定性恢复、完整备份恢复目标合同；唯一未定方向是退出UI后后台运行承诺；P4按既有ADR修正，不重决人工授权原则。Model等已有能力的完整化属于MERGE，不谎称以前没有模型。

本报告中的“Final Truth / 最终裁决 / ACCEPT NEW”均指**本轮推荐的目标真相**，尚待CEO接受；Current仍由P0→P1→P2/P3→适用Frozen定义。本轮没有supersede任何Authority。Frozen conflict的后续编辑必须明确授权。

### 1.1 三个必须防止的误读

- N1/E2所称Expression V1是**研究版Expression V1**，不是旧Frozen Blueprint。不能把其缺项直接算旧Product Authority缺项。
- N5记录CEO接受经营推导及四项修正；N6/N8/N4仍Research/Review/Candidate，未由Pointer消费为Current。文件在01_Product也不自动有Authority。
- N4的B合同闭合更新的是研究问题状态；G1-V～G6-V未运行。I1已接受的真实链不能被新研究抹掉，也不能据N4升级成全App能力完成。

### 1.2 证据范围

本轮读取仓库主入口、适用Current合同与点名新推导；只在冲突处追读候选生命周期、方法论、RD及研究反证。没有重跑业务测试、调用平台、读取秘密或重新研究竞品。N8外部平台描述是其2026-09-14记录的源码/只读观察结论，**不是本轮重新核验的线上能力**。

阅读时Git HEAD为 `78cacbd0857cc36c9f3fe0e4b11346489993b728`。工作树既有大量未提交资料；本报告引用的是本机当前文件内容，不声称clean HEAD含有全部研究。引用编号在下表给唯一文件；矩阵的§/C/V/S编号是原文件定位，不是新canonical ID。

## 2. Old Product Truth Baseline / New Candidate Baseline

|Source|SOURCE FILE|STATUS / AUTHORITY|适用边界|
|---|---|---|---|
|P0|[PRODUCT_DOCUMENT_POINTER.md](../../docs/00_Context/PRODUCT_DOCUMENT_POINTER.md)|Frozen / TRUTH ROUTER；2026-09-13 Current Required Input|唯一默认入口；后部Reference Ledger非默认|
|P1|[Curis_Product_Blueprint.html](../../docs/01_Product/Curis_Product_Blueprint.html)|Frozen / CURRENT；正文5.6，含9月9日Phase A/A.1及结构基线修订|唯一产品定义；优先消费明确supersession，不能孤立读旧段|
|P2|[Curis_Product_Master_Map.md](../../docs/01_Product/Curis_Product_Master_Map.md)|Frozen / CURRENT；3.2|展开页面字段，不独立创造产品|
|P3|[Curis_Product_UI_Blueprint.html](../../docs/01_Product/Curis_Product_UI_Blueprint.html)|Frozen / CURRENT；含Phase A/A.1和Pre-Design基线|结构承载；旧Figma登记不覆盖后续视觉暂停|
|P4|[CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md](../../docs/01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md)|Frozen / CURRENT PRODUCT STRUCTURE；2026-09-10|结构汇总而非第二Blueprint；Final Visual未批准|
|P5|[Curis_Product_Context.md](../../docs/01_Product/Curis_Product_Context.md)|Frozen；2026-09-13|模块入口；部分旧措辞未与Phase A完全同步，见冲突台账|
|S1|[Curis_Company_OS_Shared_Authority.md](../../docs/03_Design/Curis_Company_OS_Shared_Authority.md)|Frozen / CURRENT；Phase A.1优先|Employee/Responsibility/Context/Package共享语义；内部⑨仍Candidate|
|S2|[Curis_Workspace_Shell_Contract_And_Shared_Patterns.md](../../docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md)|Frozen / CURRENT|Four-Pane、Main、Composer、P1–P7；P4绝对句需提案消歧|
|S3|[CURIS_VISUAL_STANDARD_V1.md](../../docs/03_Design/CURIS_VISUAL_STANDARD_V1.md)|Frozen / DESIGN；2026-08-27|Iris视觉语言；不冻结页面composition，不参与产品能力裁决|
|S4|[CURIS_CORE_PRODUCT_AUTHORITY_REPAIR.md](../../docs/reviews/CURIS_CORE_PRODUCT_AUTHORITY_REPAIR.md)|Frozen / CEO CURRENT DECISION；Phase A.1覆盖其历史人数Gate|官方6+1与Assistant、Generic、四scope和浮动身份；历史实施状态不重开|
|D1|[Curis_Content_Growth_Domain_Authority.md](../../docs/03_Design/Curis_Content_Growth_Domain_Authority.md)|Frozen / DOMAIN；2026-08-24|Channel/Account/Intent/Variant/Publication；§5向Shared提升仍Candidate|
|D2|[Curis_Content_Growth_Operating_Strategy_UX_Translation.md](../../docs/03_Design/Curis_Content_Growth_Operating_Strategy_UX_Translation.md)|Review / APPROVED CANDIDATE；T1–T5已收敛|账号经营策略已有研究依据，非Frozen页面；不能把引用升级|
|D3|[CONTENT_GROWTH_CEO_AUTHORITY_DECISION_RECONCILIATION.md](../../docs/reviews/CONTENT_GROWTH_CEO_AUTHORITY_DECISION_RECONCILIATION.md)|Review / CEO DECISION APPLIED，STOP FOR CEO REVIEW（登记文件原状态）|Workspace唯一身份；CG Professional Candidate；默认经营结果Surface；8/4仍研究候选|
|D4|[Curis_RD_Workspace_Instance_Spec_v1.md](../../docs/03_Design/Curis_RD_Workspace_Instance_Spec_v1.md)|RD INSTANCE APPROVED；Current Shared Rule Supersession明确|仅研发对象/责任解剖；旧Main工位栈不能覆盖新版Shell|
|D5|[Curis_RD_Design_Phase_Closeout_2026-08-15.md](../../docs/03_Design/Curis_RD_Design_Phase_Closeout_2026-08-15.md)|Accepted design closeout / EVIDENCE；9月13日边界|历史设计验收，不是当前Shared UI或最终视觉|
|W1|[Curis_Workspace_Engineering_Methodology.md](../../docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Methodology.md)|Review / APPROVED CANDIDATE；含CEO已消费语义|Package First、方法Handoff、按需研究；整篇不升级Frozen|
|W2|[CURIS_WORKSPACE_ENGINEERING_PRODUCT_HANDOFF.md](../../docs/05_Workspace_Engineering/CURIS_WORKSPACE_ENGINEERING_PRODUCT_HANDOFF.md)|Review / READY FOR PRODUCT TRANSLATION；2026-08-16|方法交接；旧Office、Package未实现是历史输入，不覆盖Current|
|L1|[CURIS_OPERATING_LIFECYCLE_CONTRACT_CANDIDATE.md](../../docs/reviews/CURIS_OPERATING_LIFECYCLE_CONTRACT_CANDIDATE.md)|Status Frozen / Authority Class REVIEW；CEO ACCEPTED APPROVED CANDIDATE|accepted产品候选；不是Runtime验收；single active Workspace Cycle|
|I1|[CURRENT_STATE.md](../../docs/00_Context/CURRENT_STATE.md)|Frozen / IMPLEMENTATION TRUTH ROUTER；9月13日置顶|四scope/Phase B仍Accepted Candidate；其他能力按各自Accepted边界|
|N1|[CURIS_FULL_APP_CAPABILITY_COMPLETENESS_DERIVATION.md](../../docs/research/full-app-completeness-2026-09-14/CURIS_FULL_APP_CAPABILITY_COMPLETENESS_DERIVATION.md)|Review / RESEARCH；C01–C48|跨五类工作和失效场景的推导＋静态检查，非E2E|
|N2|[CURIS_FULL_PRODUCT_EXPRESSION_V2.md](../../docs/research/full-app-completeness-2026-09-14/CURIS_FULL_PRODUCT_EXPRESSION_V2.md)|Review / CANDIDATE|29面、48能力、77设置与字段建议；不直接冻结UI|
|N3|[CURIS_FULL_PRODUCT_EXPERIENCE_MAP.md](../../docs/research/full-app-completeness-2026-09-14/CURIS_FULL_PRODUCT_EXPERIENCE_MAP.md)|Review / RESEARCH|体验关系图，不是新的生命周期|
|N4|[CURIS_G1_G6_CAPABILITY_CONTRACT_CLOSURE.md](../../docs/research/g1-g6-contract-closure-2026-09-15/CURIS_G1_G6_CAPABILITY_CONTRACT_CLOSURE.md)|Review / PROPOSED CONTRACT；B CLOSED WITH EXPLICIT IMPLEMENTATION VALIDATION|G1-V～G6-V均未运行；合同建议收敛≠产品接受≠实现|
|N5|[CURIS_CONTENT_GROWTH_BUSINESS_LOGIC_V2.md](../../docs/01_Product/CURIS_CONTENT_GROWTH_BUSINESS_LOGIC_V2.md)|Draft / REVIEW；记录CEO ACCEPT WITH 4 CORRECTIONS|接受经营推导不等Current Domain正式消费；路径在01_Product不改变等级|
|N6|[CURIS_CONTENT_GROWTH_PRODUCT_LANGUAGE_V2.md](../../docs/research/content-growth-product-language-2026-09-14/CURIS_CONTENT_GROWTH_PRODUCT_LANGUAGE_V2.md)|Review / V2 CANDIDATE READY FOR CEO REVIEW|修正旧V1重型表达；127项归并，不是127页面|
|N7|[CURIS_CONTENT_GROWTH_AI_USER_OPERATING_BOUNDARY.md](../../docs/01_Product/CURIS_CONTENT_GROWTH_AI_USER_OPERATING_BOUNDARY.md)|Draft / 经营边界分析|能力模式有价值；百分比、L3、自主策略绝对句不继承|
|N8|[CURIS_AITO_EARN_SOCIAL_PLATFORM_EXECUTION_PROVIDER_REVIEW.md](../../docs/research/aitoearn-execution-provider-2026-09-14/CURIS_AITO_EARN_SOCIAL_PLATFORM_EXECUTION_PROVIDER_REVIEW.md)|Review；C部分Provider候选 / D不得作为主要依赖|只读产品、固定源码、文档、报告者Issue；未发布/故障复现|
|N9|[CURIS_2026_09_14_FULL_PRODUCT_RETHINK_REVIEW.md](../../docs/research/full-product-rethink-2026-09-14/CURIS_2026_09_14_FULL_PRODUCT_RETHINK_REVIEW.md)|Review / 全局反证研究|纠正盈利限定、单点能力独占、右栏工作等；非Authority|
|E1|[FIRST_PASS_AND_ADVERSARIAL_REVIEW.md](../../docs/research/full-app-completeness-2026-09-14/FIRST_PASS_AND_ADVERSARIAL_REVIEW.md)|Review / SUPPORTING RESEARCH|两轮纸面失效压力测试，不是测试执行记录|
|E2|[V1_COMPARISON.md](../../docs/research/full-app-completeness-2026-09-14/V1_COMPARISON.md)|Review / COMPARISON|比较的是研究Expression V1，不是Frozen Blueprint V1；不得混称旧Authority|
|S5|[AI_Capability_UI_Contract.md](../../docs/01_Product/AI_Capability_UI_Contract.md)|Review / CAPABILITY ECOSYSTEM REVIEW REQUIRED；§5.6受ADR-0046冻结|已有CapabilityProfile三态/来源/evidence、requested/effective；整篇不升级Frozen|
|S6|[ADR-0046-local-agent-computer-access-authority.md](../../docs/07_Decisions/ADR-0046-local-agent-computer-access-authority.md)|Frozen / CEO DECISION；2026-08-15|三档极简访问；技术授权≠CEO Decision；resume重新核验；不是Runtime完成|
|S7|[CURIS_EMPLOYEE_CONVERSATION_MODEL_EXPERIENCE_CONTRACT.md](../../docs/reviews/CURIS_EMPLOYEE_CONVERSATION_MODEL_EXPERIENCE_CONTRACT.md)|Review / READY FOR CEO REVIEW；部分模式已由P3消费|模型配置/使用分离；不凭自称冻结将全文升Authority|
|S8|[CURIS_SETTINGS_PRODUCT_CONFIGURATION_RESEARCH.md](../../docs/reviews/CURIS_SETTINGS_PRODUCT_CONFIGURATION_RESEARCH.md)|Review / RESEARCH；2026-08-17|六类设置研究、默认与政策候选；类别已被P1采用，全文非Current|

## 3. Reconciliation method

编号消歧：来源表的P4是Product Structure Baseline；“Shell P4 / P5 / P7”是S2内部Shared Pattern编号（自动执行 / Handoff / Decision），不是来源表的同名编号。涉及人工接续的F1只指S2的Pattern P4绝对句。

1. 先识别Current与明确supersession；旧文内已经被页首Phase A/A.1覆盖的句子不再当Current。
2. 比较经营责任与事实Owner，再比较能力和UI承载。缺独立页面不等缺能力；有字段/按钮也不等合同完整。
3. 每项只给一个指定Judgment。旧明确理由只引用已记录原则；未记载“为什么当时不做某能力”的原因统一UNKNOWN，不猜测资源或版本动机。
4. Matrix给逐项旧/新/证据/冲突/建议/去向。§5评估表与每个ID绑定，回答Simplicity、Reality、Operating、1/5/20业务Scale、UX、Future；不是评分或运行通过证明。
5. 分层标记：BLUEPRINT=长期关系；SHARED=跨域产品合同；DOMAIN=专业语义；UI INPUT=信息责任与交互验收；IMPLEMENTATION=技术映射/库/验证。多个去向表示核心原则与下层细节拆开，不复制Truth Owner。
6. “新增”仅是产品合同提案，不自动创建表、enum、页面、Runtime或Issue；现有经营周期、P7、Work、Usage优先复用。

## 4. Complete Reconciliation Matrix

|ID|Topic|Old Truth|Old Authority|New Candidate|New Evidence|Conflict|Judgment|Final Truth（推荐）|Destination|Blueprint Change|
|---|---|---|---|---|---|---|---|---|---|---|
|R001|Product North Star|一人AI公司，真实结果和持续成长|P1§1/11–12；P5§1|装配成熟AI能力组织真实经营|N9§19–24；N2§1|无根本冲突|CLARIFY OLD|组织AI员工持续经营真实业务、获得可核验价值；不宣称最强单点AI|BLUEPRINT|CLARIFY|
|R002|一人AI公司|真实CEO＋统一AI员工，不是Agent集合|P1§1；P5§2|通用任何业务，不等赚钱工具|N9§1–8|旧方案已正确|KEEP OLD|目标包括品牌、研究、产品、服务等；一人指当前真实Owner不是单员工|BLUEPRINT|NO CHANGE|
|R003|Company|公司级身份、组织、事实边界|P4§4–5；S4 Phase A.1|新推导按业务链组织|N2 V01–04/C31|不能把全部事实压入Business|KEEP OLD|Company级工作/分析合法，Business可以0|BLUEPRINT|NO CHANGE|
|R004|Department|长期Business必归Department；Employee招聘不以前者为前置|P1§5；P4§4/6–7|新图省略Department|N5关系图；N6§3.2|省略非授权删除|KEEP OLD|层级保留；系统协助合法归属，不让CEO先配置组织图|BLUEPRINT|NO CHANGE|
|R005|Business|canonical持续经营身份＋整体目标/Workspace组合|P1§5；P4§4；P2 Current Contract|Goal到外部反馈持续经营|N5§1；N2 V04/C31|不是只有分类标签，也非运行全部团队的母Workflow|CLARIFY OLD|Business领导整体方向与价值；具体工作在合法scope承载|BLUEPRINT|CLARIFY|
|R006|Workspace|实际工作环境；可Generic/Professional|P4§12–15；S4§4|账号经营/工具丰富|N6§3；N2 V05|不能让账号/工具替代Workspace|KEEP OLD|Business至少一个Workspace；一个Workspace多个合法账号不复制身份|BLUEPRINT|NO CHANGE|
|R007|Fixed / Built-in Departments|空间工程部、数据分析部＋6工程/至少1分析员工＋同Assistant|S4 Phase A.1；P4§5–8|新推导未重复原装组织|N2 V01/06|遗漏不等废除|KEEP OLD|原装组织保持；不是永久人数上限，不等用户业务|BLUEPRINT|NO CHANGE|
|R008|Operating Business activation|模糊意图合法；reuse/propose/必要Gate/原子Business首Workspace|P1§2；P4§12|V03要求名称/目标/Dept等字段|N2 V03/C01/C31|若要求CEO逐项填则冲突|MERGE|内部形成必要事实；用户不必填全部，准备不足不能假成功|BLUEPRINT＋SHARED|CLARIFY|
|R009|Generic / Professional|三轴Form/Provenance/Assurance分离；专业≠Verified|P5§1.1B；P4§13|无模板仍可工作，未知能力先研究|N1 C31；N6§16|已有正确目标|KEEP OLD|Generic合法；专业深度不能被通用聊天吞并，未知行业可诚实拒绝|BLUEPRINT|NO CHANGE|
|R010|Employee Identity|稳定公司员工身份；原装/招聘/自建统一|S1§0.1/1.4；P4§8–9|可装配多种AI能力|N2 C30/V07；N6§12|不是新Employee|CLARIFY OLD|Identity不随Model/Agent/Avatar/责任变化复制|BLUEPRINT|CLARIFY|
|R011|Shared Employee|同员工可多个scope Assignment；服务≠归属|S1§1.2–1.4/3；P2 Leadership|跨Business多个投影|N6§12/14；N2 C30|旧已明确，不得新增共享员工类型|KEEP OLD|目录一个Employee，业务多处责任投影；历史Context不串用|BLUEPRINT＋SHARED|NO CHANGE|
|R012|Responsibility|长期责任Requirement/Holder/Executor分离|S1§0.1；S2§3.10；D4§1a|员工经营不同账号承担不同责任|N6§12|兼容，不把Job等于一次执行|CLARIFY OLD|责任可持续/换Holder；当前Executor可none，数据源不是Holder|SHARED|CLARIFY|
|R013|Assignment|Employee×Role×canonical Scope|S1§0.1/1.3；P4§16|Account context随工作|N6§3.2/12|Account不是第五execution scope|KEEP OLD|账号作为Domain对象引用/绑定；Assignment仍同canonical scope|SHARED＋DOMAIN|NO CHANGE|
|R014|Leader|普通Employee责任角色；经营领导≠异常路由器|S1§0.1/9；P4§10|负责策略计划分析下一轮|N5责任表；N6§12|旧已明确|KEEP OLD|持续领导；only-on-exception只约束路由调用，不削弱经营责任|BLUEPRINT＋SHARED|NO CHANGE|
|R015|Team|Workspace一个accountable responsibility boundary；人数按责任|S1§9；P4§10|研究/生产/发布/分析职责|N5责任修正；N6§12|不能变每行业固定五人|KEEP OLD|职责可兼任/多Employee承担，原装六员工例外不套用Domain|SHARED＋DOMAIN|NO CHANGE|
|R016|Business Map|Department Container / Business-first /渐进RoleStaffing|P3§2/12；P4§4/8|树和多业务投影|N2 V06|不得把Employee墙或完整物理树当主视觉|KEEP OLD|组织归属与跨业务服务关系分层，Workspace次级|BLUEPRINT＋UI INPUT|NO CHANGE|
|R017|Employee Directory|Employee→责任/Role→Business→Department|P3§12；P2 Employee合同|统一身份反查工作能力|N2 V07/C30|兼容|KEEP OLD|真实身份目录；非Agent配置表，Model按能力管理入口配置|BLUEPRINT＋SHARED|NO CHANGE|
|R018|Capability|能力需求/来源/安装/授权/绑定/可执行不等|P1§6–7/12；S1§0A；P5§1.3|细化48项真实工作依赖|N1 C01–48；N4§2|覆盖增强，不新增48个canonical实体|MERGE|DEFINE FIRST→REUSE BEFORE BUILD；按责任和工作验证能力，不全员全工具|BLUEPRINT原则＋SHARED细节|CLARIFY|
|R019|Model|真实发现/选择已在；Review已有CapabilityProfile三态及来源|P3§12/17；S5§3/5.2–5.4；I1 Current|能力metadata/测试/用途路由/受控fallback|N4§4；N1 C02–08|能力三态非新增；多连接/用途测试/受控fallback需完整化|MERGE|连接Health不证明Vision/Tool；逐能力supported/unsupported/unknown及来源时效|SHARED MODEL|ADD|
|R020|External Agent|Employee可Agent-backed，不等Employee|S2§3.5；P1§7|作为可替换执行能力，安装/版本/限制|N1 C09；N4§7|兼容|CLARIFY OLD|Agent原生能力受Curis scope/permission约束；不复制其任务系统|SHARED CAPABILITY|CLARIFY|
|R021|Skill|可装配职业能力；安装不等绑定|P1§6–7；P5§1.3|版本、依赖、权限、适用工作|N1 C10/C44|旧能力组合正确，升级需复验|MERGE|同Skill机制，升级新增权限不能静默生效|SHARED CAPABILITY|CLARIFY|
|R022|MCP|连接/工具能力来源，不是经营对象|P1§12；P3§17|发现schema/工具范围/调用取消/错误|N1 C11；N8§7|技术协议不能升级产品导航|MOVE DOWN|用户按连接能力理解；协议完整度在适配合同验收|SHARED边界＋IMPLEMENTATION|MOVE TO SHARED CONTRACT|
|R023|Connector|定义≠授权连接≠执行；维护由设置承载|P1§6/12；P3§12|逐动作健康权限与回执|N6§5/8；N1 C28–29|补细节，保留现有Owner|CLARIFY OLD|发现入口在人才；实际连接/秘密管理同源，工作就地返回|SHARED CONNECTION|CLARIFY|
|R024|Provider|能力供给/执行来源；身份和结果仍Curis|P1§7/12；S2§3.5|外部平台、数据、模型、Agent多种供给|N8§17/19；N9§19–24|价值定位澄清非新架构|CLARIFY OLD|Provider≠Employee≠Business；外部结果需验证映射|BLUEPRINT原则＋SHARED|CLARIFY|
|R025|Browser|成熟能力接入原则/工具入口，未有完整交互浏览合同|P1§7/12；P3§17|独立Interactive Browser capability和安全接管|N1 C14–15；N4§3|不是概念全无；动作合同新增|ACCEPT NEW|正式目标能力：隔离浏览、可观察、受控操作、人工接管、效果核验|SHARED BROWSER；Blueprint能力概述|ADD|
|R026|Web / Search|外部资料研究；Global Search另为公司对象检索|P1§9/12；S2§1.3|Search结果与来源、费用/覆盖真实|N1 C12；N4§3|不能两种Search混同|CLARIFY OLD|Web Search供Employee研究，不新增一级区，不假全网实时|SHARED BROWSER/WEB|CLARIFY|
|R027|Reader|资料阅读/Reference已存在|P1§9；P3资料库合同|网页读取抽取、来源/截断/权限|N1 C13；N4§3|Reader≠Search≠Interactive Browser|MERGE|只读获取保留来源；外链可达不等已读取或可信|SHARED BROWSER/REFERENCE|ADD|
|R028|Computer|三档请求访问；requested≠effective；技术授权非业务Decision|S6 Decision/Truth boundaries；S5§5.6|屏幕读取、系统控制、模型适配/OS授权交集|N1 C16；N4§3/7|旧访问边界已明确；GUI/模型/适配实际能力仍须逐项验|MERGE|计算机能力独立验收；OS授权不产生能力，不能绕过平台安全|SHARED CAPABILITY|ADD|
|R029|File|Artifact/Reference/工作文件有不同用途|P1§9；P3§12/17|受限读写、输出位置、覆盖与版本|N1 C17–18；N4§7|不是再建资料库|MERGE|工作文件不自动成为Knowledge；写入/冲突/导出受权限并保版本|SHARED FILE/RESULT|ADD|
|R030|Terminal|RD有Reserved范围，成熟执行复用|P3§研发首版/12；D4 Shared supersession|多个Domain所需真实终端执行|N1 C19；N4§7|目标能力可补，不能宣布旧首版设计已包含|MOVE DOWN|Employee工具：目录/环境/停止/输出合同；复杂持续工作Main，用户不必学CLI|SHARED TOOLS＋专业UI INPUT|MOVE TO SHARED CONTRACT|
|R031|Git|RD对象/专业工具，非公司根|P3§12/17；D4§1a|dirty-safe读写/提交推送独立权限|N1 C20；N4§7|新安全粒度，非人人Git|MOVE DOWN|按RD或需要版本库的责任绑定；不把commit当公司业务完成|WORKSPACE CAPABILITY＋IMPLEMENTATION|MOVE TO SHARED CONTRACT|
|R032|Preview|Result/Artifact Utility；复杂工作Main|S2§0/3.4；P3§12|真实进程、端口、访问控制和浏览验证|N1 C21；N4§7|截图不证明运行；保留空间规则|MERGE|辅助预览Utility，复杂验证Main；localhost能力明确授权|SHARED TOOLS/RESULT|ADD|
|R033|Document / OCR|资料库已有md/txt和阅读引用|P3资料库登记；I1 Current|PDF/OCR页级失败与原文对照|N1 C22；N4§7|新增格式能力目标，不追认实现|MOVE DOWN|解析能力按格式/页/质量声明；提取成功≠正确，引用保原始出处|SHARED CAPABILITY/REFERENCE|MOVE TO SHARED CONTRACT|
|R034|Data|经营洞察消费canonical事实，无第二Analytics Truth|P1§经营洞察；P3同节|专业外部数据只读快照/查询/口径|N1 C23；N4§7|不是任意数据库管理器|MERGE|数据访问能力与经营分析产品分开；未知/过期不填0|SHARED DATA＋DOMAIN|ADD|
|R035|Media|专业内容成品/素材/预览|P3 Channel示例；D1§1.5|理解、生成、编辑、转写、格式校验分能力|N1 C42；N4§7|旧素材字段不证明生产能力|MOVE DOWN|按具体工作装配；看图≠生成图，转码≠视频生成|SHARED TOOLS＋DOMAIN|MOVE TO SHARED CONTRACT|
|R036|Knowledge|Company Reference Space、scope、UsedBy、版本引用|P1§9；P3资料库；P4§26|外部文件/新鲜度/恶意输入防护|N1 C36/C41/C45|旧不是缺失RAG平台|MERGE|保留ReferenceSpace，外部输入不自动成为可信指令或永久学习|SHARED REFERENCE|CLARIFY|
|R037|Package / Methodology|Domain Operating Capability Package；methodmetadata gap；无新Playbook|S1§0A/9；W1§10.1；P5§1.3|更多工具与专业方法组成|N1 C10/31；N4§9–12|不足以重建Package或Playbook|KEEP OLD|声明式组合复用；新工具不改变Package First及Core边界|BLUEPRINT＋既有Package合同|NO CHANGE|
|R038|持续经营|责任持续、bounded Cycle、显式Next Decision|L1§1–5；P1§11|Goal→ExternalReality→Learning→NextCycle|N5；N9§19；N3经营链|旧已具备骨架|CLARIFY OLD|固定必需Truth/Gate，不固定每条工作箭头；持续不等不间断进程|BLUEPRINT|CLARIFY|
|R039|自我进化|Evidence/Review/Promotion后版本化能力；未接受建议不生效|P5§1.3；P1§14；L1§4|真实业务反馈改后续方法|N6§9/12；N1 C44–45|不可一次AI输出永久Skill|KEEP OLD|学习限定scope和适用性；可复用能力晋升需额外验证，不自动改Core|BLUEPRINT＋SHARED|NO CHANGE|
|R040|Goal|Business-level与Workspace-level目标分层；保护变更CEO|P5§1.1/1.2；L1§6|价值可品牌/线索/产品/研究/收入|N6§3/11；N9§1–8|不应收窄全部赚钱|KEEP OLD|目标及SuccessContract明确；初始模糊意图可先理解再形成|BLUEPRINT|NO CHANGE|
|R041|Strategy|Approved Strategy Envelope内Leader可调整|L1§6.3；P1§11|平台/账号打法及AI建议|N5§1；N7 B3/B13；N6§12|N7一律CEO调策略过度；N6已纠正|KEEP OLD|保留Leader授权自治，改Goal/定位/受众/重大预算承诺才Gate|BLUEPRINT＋DOMAIN|NO CHANGE|
|R042|Plan / Cycle|固定版本计划→既有Work；single active Workspace Cycle|L1§1/4–5|AccountOperatingCycle和完整经营链|N5；N6§3.2；N4§5–6|不能等同第五Runtime scope|MERGE|账号节奏/复盘为Domain计划语义；既有Workspace控制周期承载多个账号Work|SHARED LIFECYCLE＋DOMAIN|CLARIFY|
|R043|Work|由Goal/Plan/Result/Trigger/判断产生，CEO不逐项派发|P5 Work来源；P1§8|完整任务材料、权限、下一动作|N2 C31–33；N4§6|旧已正确|KEEP OLD|唯一Work，Provider任务仅执行引用；用户可主动提出和接管|BLUEPRINT＋SHARED|NO CHANGE|
|R044|Execution|Work执行尝试与Employee身份分离；事实归scope|P4§16–17；S1；I1 Current|外部动作快照/回执/本地执行边界|N4§6–7|加强契约不是第二Execution|MERGE|本地运行、远端接受、最终效果分开；实现仍按证据等级|SHARED EXECUTION|ADD|
|R045|Decision|已有P7，决定≠Handoff；Viewed≠Accepted|S2§3.3/3.13；P4§29|同一经营Decision驱动后续Work|N2 V09；N6§10/12|不能把所有人工动作塞P7|KEEP OLD|决策继续P7；材料补充/登录是工作接续，不等新决策|SHARED DECISION|NO CHANGE|
|R046|Approval|高风险有方案/影响/证据/确认|S2§3.13；L1§6|批准绑定动作/内容版本/目标/预算，实质变化失效|N1 C39；N4§6；N8§16|完整动作快照不足，补强必要|MERGE|同一Decision/授权语义固定具体动作；无关变化不滥发重审|SHARED EXECUTION/DECISION|ADD|
|R047|Result|真实产出，成品/内部完成≠外部业务结果|P1§11；S2§3.4；P4§29|成品、回执、数据、分析分型|N6§7–9；N4§6|旧已明确，分型补足|CLARIFY OLD|同Result体系；不要求每个Result归Business，Company/Dept工作合法|BLUEPRINT＋SHARED|CLARIFY|
|R048|Evidence|来源/时效/范围/可信状态，非AI口头成功|P1§11；S2 P7；L1§4|原始存在性、采样/抓取时间、版本与外部ID|N8§12–13/17；N4§6|原原则有，准确性细化|MERGE|参考事实与推断分离；截图/用户报告按证据等级不自动Verified|SHARED EVIDENCE|ADD|
|R049|Business Result|外部Feedback/Outcome、人工回填合法|P1§9/11；P5§3|账号收益/线索/价值，不等平台数值|N6§9/11；N8§13|不是新财务真源|CLARIFY OLD|口径完整才谈利润/归因；外部结果未知可保留，不阻止诚实报告|BLUEPRINT＋DOMAIN|CLARIFY|
|R050|Learning|Result→Signal→Interpretation→AuthorizedReview→acceptedLearning|L1§4；P5§1.3|账号历史支撑策略变化|N6§9/14；N5§1|保留证据门，不从AI总结跳Strategy|KEEP OLD|账号学习可Scoped；迁移到他账号/公司需适用性复核和批准|SHARED＋DOMAIN|NO CHANGE|
|R051|Human Handoff|人工反馈/接管已有，但Shell P4只允许Decision动作|P1§9/11；S2§3.11–12；S6 Truth boundaries|正常人工登录/实拍/平台确认与继续|N7边界；N8§15；N6§10|P4绝对句与已有技术授权/人工反馈不一致|MERGE|修正P4绝对句并补人工接续合同；技术授权≠Decision，人工接续≠自动P5责任转移|BLUEPRINT原则＋SHARED；F1|REPLACE|
|R052|Background Runtime|LocalDesktop/持久化恢复；无明确退出UI后服务承诺|P5§1；P4§30；L1§8|opt-in用户级Local Background Service|N4§5；N1 C25|新增用户运行承诺，不只是选调度库|CEO DECISION REQUIRED|建议启用后关UI可继续；睡眠/关机/登出不虚构运行；显式停止全部工作|SHARED BACKGROUND；F2|ADD|
|R053|Scheduling / Trigger|三类触发/有界WAIT/nextCheckAt；不是通用规则引擎|L1§4/5；P1§8|时区/错过触发/重复合并/恢复重审|N4§5；N1 C26|细化不另造SchedulerTruth|MERGE|Trigger只是请求检查；错过合并为一次检查，不补跑所有外部写|SHARED LIFECYCLE|ADD|
|R054|Notification / Attention|Brief/Matters/异常/结果；跨日承接；无事安静|P1§10–11；P2跨日合同|能力阻塞/恢复/外部待人，隐私/静默时段|N1 C27；N2 V01/C47|不要重复每条Work通知|MERGE|同Attention投影，已应用Decision降注意力；系统策略决定提醒不新通知中心|SHARED ATTENTION|CLARIFY|
|R055|Recovery / EFFECT_UNKNOWN|重启恢复/幂等/权限失效已有|L1§8；P1§11；S2 P7|外部效果未知不等失败，先核对再重试|N1 C40；N4§6；N8§16|旧未完整覆盖远端已接受本地丢回执|ACCEPT NEW|正式目标效果确定性；同Work恢复；不承诺外部exactly-once，不预设enum|SHARED EXECUTION；Blueprint安全原则|ADD|
|R056|CEO|Goal/StrategyBoundary/关键Decision；可直接找员工|P4§11；S1§9；P1§10|Information/Analysis/Recommendation/Decision/Execution分开|N7；N6§12|既不逐项审批，也不能要求人永不操作|MERGE|普通调整由Leader；真实人身/法律/现场动作由用户，范围可明确说明|BLUEPRINT＋SHARED|CLARIFY|
|R057|Employee operating context|稳定能力与scoped执行Context分层|S1§1.4/5；L1§7|按工作检索工具/方法/知识|N1 C07/30；N6§12|不复制Leader全部Context给员工|KEEP OLD|reference/summary-first，按需检索；输入不是隐式权限|SHARED CONTEXT|NO CHANGE|
|R058|Global CEO Assistant|same canonical Employee，全局浮动/持久Conversation，协调非专家|P4§22；S4§7；P1§10|理解/协调discovery/proposal/跟进|N2 V23；N6§12|不能吞并Leader、Executor或右栏对话|KEEP OLD|合法当前Context；未知专业问题交合法责任者，缺能力坦诚说明|BLUEPRINT＋SHARED|NO CHANGE|
|R059|Business Exit / commitment|Pause/Reduce/Transfer/Close/Merge/Split保护责任/历史|P2 Exit合同；P1§11|在途效果/共享连接/排程/备份退出|N1 C48；N4§6/8|旧经营内核已在，不新建Exit页|MERGE|退出需处理未完成承诺、责任交接和外部效果；归档不取消远端事实|SHARED LIFECYCLE|CLARIFY|
|R060|Capacity / Allocation|Capability≠Capacity，服务关系不自动授权|P5§6；S1§1.2–3/7|跨员工资源占用/并发/预算|N1 C38；N4§5–7|不把技术lease升为公司新组织对象|MERGE|用户看真实占用/等待及谁能解除，底层资源协调下沉|SHARED资源约束＋IMPLEMENTATION|CLARIFY|
|R061|Business Duplication / Template|复用方法配置，不复制identity/secret/history/runtime|P2 Duplication；P1§5|跨账号复用策略素材|N6§7/14；N1 C48|复制不自动带他账号授权或学习|KEEP OLD|Copy Preview和重新绑定保留；Template非未知行业能力证明|BLUEPRINT＋DOMAIN|NO CHANGE|
|R062|Seven Navigation Areas|七个主要公司工作区固定|P4§3；S2§1.1/1.3|更多能力和29面|N2 V01–29；N3|能力数量不推出导航数量|KEEP OLD|七区全部KEEP；Browser/Model/Recovery等不得升第八区|BLUEPRINT|NO CHANGE|
|R063|CEO Desk|公司注意力、简报、结果、下一决定|P1§3/10；P4§3|加就绪与恢复摘要|N2 V01；N6§4|不得变AI配置或Dashboard墙|CLARIFY OLD|条件性needs，跨业务看经营；复杂修复转原Owner并可返回|BLUEPRINT＋UI INPUT|CLARIFY|
|R064|Business Space|Department/Business/Workspace经营入口目录|P2 OperatingWorkDirectory；P1§5|聚合账号当前工作和结果|N2 V02/04；N6§4|账号专业投影不能改全局目录成平台目录|KEEP OLD|Business整体方向/状态/Workspace目录/团队摘要；专业执行仍原scope|BLUEPRINT＋DOMAIN|NO CHANGE|
|R065|Organization Center|公司版图＋员工目录，非日常领导聊天后台|P3§12；S4 Phase A.1|更完整多业务身份投影|N2 V06/07|保留双Tab，不恢复HR或Capability admin|KEEP OLD|岗位/服务/责任按需；Workstation讨论进入Main|BLUEPRINT|NO CHANGE|
|R066|Talent & Capability|招聘创建员工、Skill/Capability扩展；Model配置另设置|P3§12；P4§28|CapabilityCatalog完整化|N2 V18/C09–11|不能吞并全部模型/工具设置|KEEP OLD|发现/安装/绑定生命周期同源；原装员工已在公司，不待招聘|BLUEPRINT＋SHARED|NO CHANGE|
|R067|Operating Intelligence|分析工作面，Company Analyst负责、canonical数据|P4§27；P1经营洞察|模型质量/成本/外部结果比较|N1 C35；N6§9|不新AnalyticsRuntime/排行榜|KEEP OLD|深度比较/归因/报告，成本速度质量失败验收分别可解释|BLUEPRINT＋SHARED|NO CHANGE|
|R068|Knowledge Library|Company Reference Space；Reading/UsedBy|P4§26；P3资料库|PDF/来源更新/检索增强|N1 C22/36/45；N2 V22|不可退化FileManager/RAGconsole|KEEP OLD|核心阅读/引用/回程不变，新格式由能力合同验收|BLUEPRINT＋SHARED|NO CHANGE|
|R069|Meetings|persistent operating discussion，CEO离开不结束|P4§25；P3§14|能力就绪/失败/责任结果回流|N1 C34；N2 V19|普通群聊≠独立Task系统|KEEP OLD|Overlay创建→sameMeeting→P7/责任Work/Result；记录能力缺口|BLUEPRINT＋SHARED|NO CHANGE|
|R070|Settings / Connections|既有类别/头像入口，不占七区|P1§3；P3§12|77设置、模型与连接完整字段|N2§7/8|完整≠全部暴露；分类草稿不直接改IA|MOVE DOWN|按Owner与场景组织；普通少量，事实自动发现，高级参数按需|SHARED SETTINGS＋UI INPUT|MOVE TO SHARED CONTRACT|
|R071|Four-Pane|职责模型，默认Navigation＋Main|P4§18–24；S2§0–2|复杂能力需要可用工作面|N2§4/V15–17；N6§15|整体兼容，不改成固定四列|KEEP OLD|四Pane及独立浮动Assistant保持，复杂功能按职责落位|BLUEPRINT＋SHELL|NO CHANGE|
|R072|Left Context|当前Domain对象/局部导航/范围|S2§0/3.12；P4§18|账号集合/文件等按需|N6§14–15；N2 V05|不能放完整对话或全公司树|KEEP OLD|筛选≠修改执行范围；Main独立显示合法工作身份|SHELL＋DOMAIN UI INPUT|NO CHANGE|
|R073|Main|selectedProfessionalSurface＋SharedWorkArea；完整工作/Conversation|S2§0.1；P4§19/23|Browser调试/模型复杂配置/账号工作|N2 V13/15/17/27；N6§15|旧RD Main=整个工位栈只可历史投影|CLARIFY OLD|复杂持续工作在Main；Workspace专业对象仍主视觉，不强制所有页面聊天|SHELL＋DOMAIN|CLARIFY|
|R074|Right Utility|辅助Detail/Evidence/Result/Reference/Preview，可max阅读|S2§0/3.4/3.12；P4§18|工具观察/结果并看|N2 V10/15；N6§15|不得第二完整聊天或复杂经营后台|KEEP OLD|短辅助查阅；转完整编辑/调试进入Main，保留来源回程|SHELL|NO CHANGE|
|R075|Conversation / Work|持久关系/多话题/逐消息scope；不是执行日志|P4§21/23；S4§5|上下文/能力/停止/回执表达|N2 V08；N6§12/14|P5旧Conversation按Assignment硬分需同步而非恢复|CLARIFY OLD|Conversation承接请求和解释，Work管承诺执行；浏览切换不改消息授权|SHARED CONVERSATION|CLARIFY|
|R076|Shared Composer|完整Frozen语义槽位；Model-backed/Agent-backed区分|S2§3.5；P3§17|Text/References/发送/状态细化|N2 F13/V08；N3|简写不得删除访问权限/工作模式/已选资源等|KEEP OLD|保留功能合同；实际附件/Voice能力诚实；布局与消息节奏仍设计开放|SHELL＋SHARED|NO CHANGE|
|R077|Conversation Quick Access|全局持久对话最近/搜索/reopen/dismiss非delete|P4§21；S4§5|更多对象深链|N2 V24；N6§12|不是Assistant也非第二消息系统|KEEP OLD|同Employee多topic、真实活动排序、scope合法回程|SHARED NAVIGATION|NO CHANGE|
|R078|Employee status / Workstation|员工三态；运行状态不驱动展开|S2§3.1；D4页首|N2 C30 employee states含等待|N2 C30/F02/V07|若作为SharedEmployeeStatus则冲突|REJECT NEW|Employment/readiness/Work状态分开；员工仅空闲/工作中desc/阻塞cause|SHELL；N2修正后才下游|NO CHANGE|
|R079|Visual / IA authority|DirectionD语言Frozen；FinalUI暂停、19Figma只结构参考|P4§31–35；S3§1–2；P3§1|字段、Drawer/Tabs/按钮建议|N2全稿；N6§4/6|不得以更详细研究冻结像素/所有专业Tab|KEEP OLD|继承结构，UI-ready数据责任不等常驻组件，具体视觉不在本轮|UI DESIGN INPUT|NO CHANGE|
|R080|Content Growth identity|Professional Workspace Candidate；不是平台Workspace|D1§0.1；D3§1；P4§14|内容经营业务团队持续负责|N5；N6§2–3|经营完整不等Verified专业Package|CLARIFY OLD|用户启用的Business/专业组合，产品形态与实际能力验收分开|DOMAIN；Blueprint例证|CLARIFY|
|R081|Platform / Channel|Channel≠Workspace≠ChannelAccount|D1§0.1/1.2；D3§1|平台策略/规格/能力事实|N5§1；N6§5|Platform作Channel同义，不新canonical父层|CLARIFY OLD|平台是Domain渠道与规则来源；动态规则带地区账号时效|DOMAIN|CLARIFY|
|R082|Account / Channel Account|Company资产；合法Workspace绑定；已有账号定位策略|D1§1.2/4；D2§2.2|长期经营对象，独立目标策略历史表现学习|N5§1；N6§3/6|有旧基础但责任/周期闭环需正式扩展|MERGE|扩已有ChannelAccount经营合同；资产Owner不变，经营投影注明本次scope|DOMAIN|ADD|
|R083|Account Operating Cycle|Workspace单activeCycle；账号是对象不是scope|L1§1/4；D1§1.2|账号级计划→生产→结果→Review→下一轮|N5§1；N6§3.2/6|若新并行Account Runtime Cycle则冲突|MERGE|账号周期=Domain cadence/plan/review关系，映射既有Work/WorkspaceCycle；不新增scope/Runtime|DOMAIN＋SHARED引用|ADD|
|R084|Content Intent|Company可共享WHY/WHAT/Goal；不含私有Prompt/CoT|D1§1.3|选题为经营目标服务|N6§3/7；N5内容链|兼容；不是每次平台改写新Intent|KEEP OLD|同核心意图允许多账号完全不同表达；目的改变才新Intent|DOMAIN|NO CHANGE|
|R085|Platform Form|Variant已有素材/平台发布约束|D1§1.5/§7|平台形态先于各账号定稿|N5§1；N6§7|细化，不需要新canonical对象|CLARIFY OLD|作为Variant生产约束/能力要求，规格按真实来源与有效能力交集|DOMAIN|CLARIFY|
|R086|Account Context|账号隔离、绑定与策略|D1§1.2/3；S1§5|同平台不同定位受众/语气/历史|N5；N6§7/14|共享Intent不能共享私有账号上下文|KEEP OLD|本次执行带合法账号引用；跨账号只显式共享允许资料|DOMAIN＋SHARED|NO CHANGE|
|R087|Variant|逐Account；HIGH_REUSE/FULL_DIVERGENCE|D1§1.5|Intent×平台形态×账号语境→定稿|N6§7；N5内容链|拒绝完全重产就必须另Intent的旧研究限制|CLARIFY OLD|账号版本保留原Intent lineage、版本及审核；非所有平台同一内容|DOMAIN|CLARIFY|
|R088|Publishing Employee|责任由Curis真实Employee承担；Provider执行外部动作|S1；D1§4；P1§7|校验定稿/目标/权限、提交、核对、恢复|N6§8；N8§17/19|不用Provider Agent替代公司员工|CLARIFY OLD|发布职责保留Curis，人数按实际Assignment；工具调用不是新员工|DOMAIN＋SHARED|CLARIFY|
|R089|Publication / partial success|逐账号回执；BEST_EFFORT/ALL_REQUIRED；外部成功不回滚|D1§1.4–1.5/3|操作ID/最终作品ID/可见性/超时分别表达|N8§12/16；N6§8|不能默认全组重发或所有成功即公开|MERGE|逐账号确定性/回执、按原分发政策处理未执行项，保留既成事实|DOMAIN＋SHARED恢复引用|ADD|
|R090|Analytics Employee|经营分析责任；CompanyAnalyst和业务Assignment|S4 Phase A.1；P1洞察；D2§2.4|数据→证据→解释→学习|N6§9/12；N8§13|系统采集≠分析员工；无双Owner|CLARIFY OLD|Provider回数据；Employee解释/报告，系统采集不伪造员工Presence|DOMAIN＋SHARED|CLARIFY|
|R091|Analytics data quality|Unknown≠0；source/freshness/口径|P1洞察；D1§5；P3洞察|normalized0与observed0、采样/抓取时间区分|N8§13；N6§9|重要细化，不能由零快照推经营失败|MERGE|有原始存在性和适用时窗才分析；跨账号仅同口径派生聚合|DOMAIN＋SHARED EVIDENCE|ADD|
|R092|Monetization boundary|真实价值/外部反馈，不是统一钱包/CRM|P1§1/11；P5§1|资格/机会/收益/回填|N7；N6§11；N9§11–18|早期重型资格地图/统一结算过度|REJECT NEW|保留目标相关外部条件和收益证据，不建钱包/收益Runtime或全量资格后台|DOMAIN|NO CHANGE|
|R093|AiToEarn boundary|Provider可复用，未指定唯一底座|P1§12；D1§4–5|部分平台发布/数据执行供给|N8§1/25|研究支持C不支持主依赖A|MOVE DOWN|仅候选Provider，源代码/在线观察≠Curis集成；不能写进核心产品定义|IMPLEMENTATION / PROVIDER RESEARCH|MOVE TO IMPLEMENTATION CONTRACT|
|R094|Engagement / external leads|反馈作为经营信号；高影响外部承诺受控|P1§11；P5§3；D2§2.4|评论/私信/商业线索接续|N6§11/13 C16；N8§14|不保证全平台统一收件箱/CRM|MERGE|能力逐动作验证，拟答≠发送；真实线索可交合法责任，成交未知保留|DOMAIN|CLARIFY|
|R095|Account responsibility / shared asset|资产Company；服务Binding；Employee多责任|D1§4；S1§1.2–1.4|无需唯一Account专员，允许多经营上下文|N5修正；N6§3.2/6|不应无责任Owner或跨scope随意同时写|MERGE|由当前合法责任解析执行者；共享账号保留scope/版本/资源仲裁，无新身份|DOMAIN＋SHARED资源|CLARIFY|
|R096|Platform schedule|Domain scheduled_at仅平台支持；分发政策不等Scheduler|D1§3；L1§4|本地到点提交/Provider排程/平台原生时间|N8§8；N6§8；N4§5|若同字段混义则冲突|CLARIFY OLD|区分计划时间、提交时间、平台接受排程/实际发布；不把新本地trigger冒称原生排程|DOMAIN＋SHARED|CLARIFY|
|R097|Backup / Recovery|备份恢复作为应用/数据能力，已有局部实现记录|P1§3/15；N1 C43静态边界|DB＋ManagedFiles＋Manifest＋preflight/reconnect/resumecheck|N4§8；N1 C43|旧标题/DB包不足以证明公司可恢复|ACCEPT NEW|完整目标恢复合同；不含Credential/Cookie/Keychain；恢复后外写默认待核验|SHARED BACKUP；Blueprint连续性|ADD|
|R098|Update / version compatibility|immutable定义/Package版本，保护运行中Truth|S1§9；L1§1/4；P5§1.1B|模型下架/能力升级/新增权限重新测试|N1 C44；N4§4/7|已有原则，跨能力升级需补|MERGE|版本变更保历史引用，受影响能力复验，不能静默扩大权限|SHARED CAPABILITY＋IMPLEMENTATION|ADD|
|R099|Network / proxy / TLS|连接按真实状态，不伪授权|P3§2/12；P1§12|每Provider出口、代理/证书/本地远端边界|N1 C37；N2 S075–077|网络诊断不应成为全局核心经营对象|MOVE DOWN|必要连接配置高级可达；不禁用TLS安全；不同连接分别健康|SHARED CONNECTION＋IMPLEMENTATION|MOVE TO SHARED CONTRACT|
|R100|Resource conflict / concurrency|Capacity与Assignment有效范围；队列⑨非全部Frozen|S1§7；P5§6|文件/浏览账号/进程资源争用|N1 C38；N4§3/5/7|不能把技术锁计作已接受组织Capacity系统|MOVE DOWN|最小安全资源协调；用户看谁占用/为何等/恢复；lease内部化|SHARED EXECUTION＋IMPLEMENTATION|MOVE TO SHARED CONTRACT|
|R101|External trust / prompt injection|Context隔离/引用权限/不注入全部历史|S1§5；L1§7|网页/文件/Skill中恶意指令不能提权|N1 C41；N4§3/7|原则补强，不能声称已保证免疫|MERGE|不可信内容不是授权指令；来源可追，工具调用仍合法检查|SHARED CONTEXT/SECURITY|ADD|
|R102|Permission / data egress|scope隔离、角色不等权限、provider真实授权|S1§3/5；S2§3.5；S6|resource∩Employee∩Work∩data∩capability|N4§3–7；N2 S060–063|不能只显示一个授权绿灯|MERGE|逐动作有效权限；数据外发/不可逆动作独立边界，不全员授所有工具；不逐项弹python/node/git/npm技术批准|SHARED SECURITY|ADD|
|R103|Accessibility / input behavior|UI progressive和共享交互，最终视觉未定|P3§2/17；P4§31/34|IME/键盘/缩放/状态可读|N1 C46；N2全局交互|有用户价值但不增加产品对象|MOVE DOWN|交互验收要求保留；像素和键位留设计验证，不用鼠标原型证明可用|SHARED INTERACTION＋UI INPUT|MOVE TO SHARED CONTRACT|
|R104|Diagnostics / safe export|真实Evidence/隐私/权限|P1§11；S1§5|选范围、脱敏、预览、单独发送|N1 C47；N2 V25|日志更多不等用户价值|MOVE DOWN|帮助/Settings按需诊断，不默认上传秘密/所有对话/Providertrace|SHARED SUPPORT＋IMPLEMENTATION|MOVE TO SHARED CONTRACT|
|R105|State taxonomy / Conflict|P5§6说Conflict；P1/P3 DataTrust要求来源/Unknown/需核实|P5§6；P1洞察；S2 P7|模型/工作/员工多状态及冲突字段|N2 F02/C30/C45；N6§9|旧Current措辞也有歧义，不能统一成新全局enum|CLARIFY OLD|区分来源不一致、资源冲突、工作等待、Employee三态；各语义不并成GlobalConflictState|SHARED契约；P5消歧|CLARIFY|
|R106|Discovery / product derivation method|Blueprint/Map末段先一级产品→动作→页面→AI→能力|P1§13；P2规划顺序；W1§2/6|真实工作→能力/边界→产品表达再验结构|N1/E1；N9；N2§1|绝对page-first不足；W1已有业务先行依据|MERGE|业务证据先行确定需要，现有公司/导航约束承载；不得Runtime对象反推导航|BLUEPRINT方法注释＋W1|CLARIFY|
|R107|Product Expression V2 layering|Blueprint核心，Map字段，UI承载，Shared/Domain各有权威|P0；P1§15；P3§1|字段按钮设置及G验证混一研究稿|N2全稿；N4|不能全文复制进Blueprint|MOVE DOWN|逐内容分层消费，研究稿保provenance；只把稳定关系写核心|SHARED/DOMAIN/UI/IMPLEMENTATION|MOVE TO SHARED CONTRACT|
|R108|OSS reuse choices|成熟复用、PackageFirst、不重建每行业能力|P1§12；W1§2/6；S1§9|Playwright/models.dev/APScheduler/Docling/FFmpeg等|N4§9–12|技术选项不是产品承诺|MOVE DOWN|库/API/License/版本/性能由实现合同核验；不进产品名词或固定依赖|IMPLEMENTATION CONTRACT|MOVE TO IMPLEMENTATION CONTRACT|
|R109|Current vs Target|目标≠已实现；AcceptedCandidate不升级Accepted|P0 CurrentRequired；I1顶部；P1§15|N4合同B闭合但G1-V～G6-V未执行|N4§15–16；N1静态检查|不得以研究完备宣布产品/Runtime全完成|KEEP OLD|保留已接受链及未验证边界，未来产品合同接受后单独实施验证|GOVERNANCE|NO CHANGE|
|R110|No second systems|唯一Employee/Work/Execution/Result/Decision/Usage/CompanyTruth|S1§3；L1§1；P4§16/29|能力大清单、Provider有自己的Flow/Task|N4§11–12；N8§17/19|Provider引用不得升级第二公司任务本体|KEEP OLD|只映射外部执行引用；HumanAction/AccountCycle/Method不因命名新增Runtime|BLUEPRINT＋SHARED|NO CHANGE|

## 5. Per-topic reasoning / 六维压力检验

每个ID与§4的具体Old/New/证据/裁决合读。Old Rationale仅引用已记录的一般原则；本项专门历史取舍未记载时为UNKNOWN。1/5/20 Business规模栏是产品压力推理，不是运行测试。

|ID / Topic|OLD RATIONALE|SIMPLICITY|REALITY|OPERATING|SCALE 1 / 5 / 20|UX|FUTURE|
|---|---|---|---|---|---|---|---|
|R001 Product North Star|旧明确理由：稳定公司归属、责任连续及NO_DUPLICATION（P1/S1）；未额外推测历史动机；专门取舍未记载则UNKNOWN|解释旧价值比更换品牌模型简单|不声称AI能力领先|经营结果而非调用次数|1可单业务；5/20保同公司聚合|CEO理解公司经营而非工具装配|模型升级不动公司语义|
|R002 一人AI公司|旧明确理由：稳定公司归属、责任连续及NO_DUPLICATION（P1/S1）；未额外推测历史动机；专门取舍未记载则UNKNOWN|单CEO心智胜多Agent后台|真实CEO不等无人参与|收入并非唯一成功目标|1/5/20业务仍一Owner治理|普通语言“交给Curis”|未来多人不是当前默许|
|R003 Company|旧明确理由：稳定公司归属、责任连续及NO_DUPLICATION（P1/S1）；未额外推测历史动机；专门取舍未记载则UNKNOWN|不把Company压成Business容器|Business0也有真员工|公司级分析/建设可先工作|1起步；5/20同源汇总|初始组织非空而业务可空|不依赖示例行业|
|R004 Department|旧明确理由：稳定公司归属、责任连续及NO_DUPLICATION（P1/S1）；未额外推测历史动机；专门取舍未记载则UNKNOWN|保层级不让用户填层级表|合法parent必须解析|组织支持持续业务归属|1也可复用Department；20可按需分组|系统准备归属而非CEO工程化配置|不恢复orphan Business|
|R005 Business|旧明确理由：稳定公司归属、责任连续及NO_DUPLICATION（P1/S1）；未额外推测历史动机；专门取舍未记载则UNKNOWN|持续identity胜只分类标签|真实业务不能靠列表完成|整体策略统筹Workspace|1正常；5/20组合目录不合并执行|用户看整体方向/结果|不随项目和账号更名|
|R006 Workspace|旧明确理由：稳定公司归属、责任连续及NO_DUPLICATION（P1/S1）；未额外推测历史动机；专门取舍未记载则UNKNOWN|保实际工作环境|Generic能真实工作但非万能|专业对象与团队持续共处|单空间可多账号；多空间独立|账号数不强迫建空间|专业增强不换Business身份|
|R007 Fixed / Built-in Departments|旧明确理由：稳定公司归属、责任连续及NO_DUPLICATION（P1/S1）；未额外推测历史动机；专门取舍未记载则UNKNOWN|复用原装定义不造新员工系统|无模型员工仍真实存在|建设/分析责任先于用户业务|初始6+1非永久上限|不要求先招聘工程团队|Holder可变历史保留|
|R008 Operating Business activation|旧明确理由：稳定公司归属、责任连续及NO_DUPLICATION（P1/S1）；未额外推测历史动机；专门取舍未记载则UNKNOWN|提案胜必填组织表|准备不完整不能假成功|成立后有Leader责任|1快速开始；5/20优先reuse|CEO只补不能代理事实|陌生领域可研究/拒绝|
|R009 Generic / Professional|旧明确理由：稳定公司归属、责任连续及NO_DUPLICATION（P1/S1）；未额外推测历史动机；专门取舍未记载则UNKNOWN|Generic与专业不是两套Core|模板存在不等能力Verified|专业深度不被聊天替代|1合法起步；20各需适用方法|无需模板商城门禁|可演进不承诺一句话生成专业软件|
|R010 Employee Identity|旧明确理由：稳定公司归属、责任连续及NO_DUPLICATION（P1/S1）；未额外推测历史动机；专门取舍未记载则UNKNOWN|一身份胜每工具一员工|换模型不创造新人|历史责任和Conversation延续|1/5/20不复制Profile|用户识别人而非Provider|头像/名称变动不换ID|
|R011 Shared Employee|旧明确理由：稳定公司归属、责任连续及NO_DUPLICATION（P1/S1）；未额外推测历史动机；专门取舍未记载则UNKNOWN|共享Assignment胜共享全部Context|同名/同人不授跨域权限|跨业务协作可持续|1无矩阵负担；5/20按需查服务|目录一人业务多处引用|员工能力变化不迁移组织|
|R012 Responsibility|旧明确理由：稳定公司归属、责任连续及NO_DUPLICATION（P1/S1）；未额外推测历史动机；专门取舍未记载则UNKNOWN|Requirement/Holder/Executor分型必要|等待时Executor可none|无人执行不等无人负责|20业务仍可定位具体责任|说谁负责与当前谁工作|换人不抹历史|
|R013 Assignment|旧明确理由：稳定公司归属、责任连续及NO_DUPLICATION（P1/S1）；未额外推测历史动机；专门取舍未记载则UNKNOWN|一个Assignment模型足够|Account引用不是第五scope|同员工不同责任合法|20业务不按账号再造身份层|隐去Assignment内部ID|新增Domain沿用scope|
|R014 Leader|旧明确理由：稳定公司归属、责任连续及NO_DUPLICATION（P1/S1）；未额外推测历史动机；专门取舍未记载则UNKNOWN|Leader不另造Employee类型|路由自动不代表业务无人领导|目标/整合/下一步持续负责|多层只在最低有效scope解决|问策略找Leader非Router|更强自动路由不取消领导|
|R015 Team|旧明确理由：稳定公司归属、责任连续及NO_DUPLICATION（P1/S1）；未额外推测历史动机；专门取舍未记载则UNKNOWN|职责分工胜固定五员工模板|未绑定不伪造Team|团队拥有真实交付责任|1可兼任；20按责任扩编|不让CEO画DAG|行业差异不重建Shared|
|R016 Business Map|旧明确理由：稳定公司归属、责任连续及NO_DUPLICATION（P1/S1）；未额外推测历史动机；专门取舍未记载则UNKNOWN|CompanyMap投影胜第二组织表|没有Risk来源不推测|看到业务扩张非HR树|20业务按需展开Role|Business-first避免Employee墙|可加视图不改Owner|
|R017 Employee Directory|旧明确理由：稳定公司归属、责任连续及NO_DUPLICATION（P1/S1）；未额外推测历史动机；专门取舍未记载则UNKNOWN|Employee-first反查足够|Catalog不是公司员工|招聘后责任/工作连续|20业务仍同一员工目录|身份/能力/工作各有入口|以后更复杂组织不换身份|
|R018 Capability|旧明确理由：成熟能力复用、能力≠授权≠执行；具体能力细分不足处的历史原因UNKNOWN；专门取舍未记载则UNKNOWN|分能力合同不分48新实体|需求/安装/授权/执行分开|缺口有恢复而非假完成|5/20复用绑定不全员安装|就地说明能做什么|Provider可替换|
|R019 Model|旧明确理由：成熟能力复用、能力≠授权≠执行；具体能力细分不足处的历史原因UNKNOWN；专门取舍未记载则UNKNOWN|补现有Profile比另模型中心简单|chat不证明其他能力|用途合格才能继续|多业务用途不同仍同连接机制|默认自动选合格模型|版本更新重新判能力|
|R020 External Agent|旧明确理由：成熟能力复用、能力≠授权≠执行；具体能力细分不足处的历史原因UNKNOWN；专门取舍未记载则UNKNOWN|复用Agent适配不再造Runtime|安装/认证/执行各自证明|Session恢复仍归原Work|多员工调用不共享私有context|不强迫理解Agent实现|换Agent不迁移员工|
|R021 Skill|旧明确理由：成熟能力复用、能力≠授权≠执行；具体能力细分不足处的历史原因UNKNOWN；专门取舍未记载则UNKNOWN|沿用Skill版本/组合|描述好不代表可执行|能力更新不切断旧Work|共享安装不自动共享Grant|发现/安装/绑定分层|新增权限需复审|
|R022 MCP|旧明确理由：成熟能力复用、能力≠授权≠执行；具体能力细分不足处的历史原因UNKNOWN；专门取舍未记载则UNKNOWN|协议下沉更简单|工具清单不证明工具可用|错误/取消回原Work|多业务通过同连接入口|普通用户不学MCP schema|传输可变产品不变|
|R023 Connector|旧明确理由：成熟能力复用、能力≠授权≠执行；具体能力细分不足处的历史原因UNKNOWN；专门取舍未记载则UNKNOWN|同连接Owner多入口|OAuth存在不等当前授权|断连保历史与等待工作|共用连接须合法scope|恢复连接后回原现场|新Provider不建新设置系统|
|R024 Provider|旧明确理由：成熟能力复用、能力≠授权≠执行；具体能力细分不足处的历史原因UNKNOWN；专门取舍未记载则UNKNOWN|外部供给不另公司组织|Provider成功码非业务成功|公司持续负责结果|20业务不复制Provider任务本体|展示员工工作和必要来源|换供给不换Business|
|R025 Browser|旧明确理由：成熟能力复用、能力≠授权≠执行；具体能力细分不足处的历史原因UNKNOWN；专门取舍未记载则UNKNOWN|补浏览能力不建Browser产品|WebView/安装库非浏览E2E|登录/接管/回执才能续工作|多业务隔离账号和写控制|看现场与必要接管|执行器可替换|
|R026 Web / Search|旧明确理由：成熟能力复用、能力≠授权≠执行；具体能力细分不足处的历史原因UNKNOWN；专门取舍未记载则UNKNOWN|区分Web搜与公司搜|不承诺全网/实时覆盖|结果需Reader核实|20业务query不能带无关秘密|按问题研究非搜索后台|换搜索服务不换资料引用|
|R027 Reader|旧明确理由：成熟能力复用、能力≠授权≠执行；具体能力细分不足处的历史原因UNKNOWN；专门取舍未记载则UNKNOWN|Reader独立于Browser写|抽取截断/权限需说明|来源能回读才支撑研究|跨业务引用需授权|读内容不看抓取日志|解析升级保旧出处|
|R028 Computer|旧明确理由：成熟能力复用、能力≠授权≠执行；具体能力细分不足处的历史原因UNKNOWN；专门取舍未记载则UNKNOWN|保三档意图不逐命令弹窗|OS/Agent/模型能力交集|接管后重验目标再续|多任务不能并抢控制|真实生效与用户选择分开|新Adapter仍apply/verify|
|R029 File|旧明确理由：成熟能力复用、能力≠授权≠执行；具体能力细分不足处的历史原因UNKNOWN；专门取舍未记载则UNKNOWN|不把每工作目录变Library|读写授权和真实路径|文件版本关联Result|多员工写冲突不能覆盖|原生选择/明确输出|外部编辑保历史对照|
|R030 Terminal|旧明确理由：成熟能力复用、能力≠授权≠执行；具体能力细分不足处的历史原因UNKNOWN；专门取舍未记载则UNKNOWN|工具能力非新终端中心|命令退出码不等业务交付|可取消/恢复输出|并发进程和目录需限制|CEO只看工作结果/缺口|专业工具可替换|
|R031 Git|旧明确理由：成熟能力复用、能力≠授权≠执行；具体能力细分不足处的历史原因UNKNOWN；专门取舍未记载则UNKNOWN|专业工具非全员必修|读diff不证明安全push|交付保commit/review证据|多员工dirty worktree需隔离|技术细节按需|仓库工具变化不改Company|
|R032 Preview|旧明确理由：成熟能力复用、能力≠授权≠执行；具体能力细分不足处的历史原因UNKNOWN；专门取舍未记载则UNKNOWN|预览引用不复制结果|真实端口/进程才叫可运行|验证回原Work|不同业务预览地址要隔离|辅助看Utility复杂验证Main|承载方式可演进|
|R033 Document / OCR|旧明确理由：成熟能力复用、能力≠授权≠执行；具体能力细分不足处的历史原因UNKNOWN；专门取舍未记载则UNKNOWN|解析不造第二知识系统|OCR可错/页可缺|引用保页/原文便复核|多业务资料scope保持|读者看缺页/低置信而非假全文|新格式逐个验收|
|R034 Data|旧明确理由：成熟能力复用、能力≠授权≠执行；具体能力细分不足处的历史原因UNKNOWN；专门取舍未记载则UNKNOWN|访问与分析Owner分开|SQL生成不证明安全正确|口径快照支撑复盘|多业务数据不可乱join|默认只读/解释结论|数据源变动保版本|
|R035 Media|旧明确理由：成熟能力复用、能力≠授权≠执行；具体能力细分不足处的历史原因UNKNOWN；专门取舍未记载则UNKNOWN|生产工具按工作装配|看图≠生图/转码≠生成|产出回读验规格|20业务不共享私有素材|需求语言而非FFmpeg参数|模型与工具可换|
|R036 Knowledge|旧明确理由：成熟能力复用、能力≠授权≠执行；具体能力细分不足处的历史原因UNKNOWN；专门取舍未记载则UNKNOWN|保ReferenceSpace胜RAG后台|有文本不代表可信知识|UsedBy连工作/结果|多业务引用合法范围|找到→读→带入工作|检索增强不改Owner|
|R037 Package / Methodology|旧明确理由：成熟能力复用、能力≠授权≠执行；具体能力细分不足处的历史原因UNKNOWN；专门取舍未记载则UNKNOWN|已有Package/Method足够|官方≠Verified，方法元数据仍gap|方法经证据晋升|20行业用组合非Core硬编码|未知业务不让CEO拼包|不新增Playbook对象|
|R038 持续经营|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|复用既有Lifecycle不增一条链|Cycle闭合不证明外部价值|责任连续而执行有界|多业务分别调度防饿死|看下一步而非Cycle面板|保留显式下一轮裁决|
|R039 自我进化|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|保留证据晋升不加自进化按钮|一次AI输出不是已验证能力|Learning经Review再复用|跨业务复用需适用性核验|CEO只审关键晋升|版本与撤回比自动记忆稳定|
|R040 Goal|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|保留上下层Goal不加覆盖机制|成功需可观察条件|Goal约束Plan与Review|Workspace目标服务Business方向|表达目标无需配技术字段|Goal版本可追溯|
|R041 Strategy|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|Approved Envelope比全策略开关简单|证据不足不能自主改策略|战术调整与改方向分开|多业务各有预算边界|重大方向找CEO普通调整不找|保护边界可随授权演进|
|R042 Plan / Cycle|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|复用Plan和bounded Cycle|计划不是实际执行记录|一次仅一个合法后继|Account分析不制造并行第二循环|不要求用户管理循环枚举|固定真相不固定业务步骤|
|R043 Work|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|保留同一Work|创建Work不等于完成|来自计划结果与员工判断|多员工共享引用而非复制任务|CEO可提出工作但非派单员|来源扩展不重造Task|
|R044 Execution|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|保留Execution与Work分离|Provider回调需验真|恢复接续原责任|并发执行仍受Scope权限|进度与结果分开展示|执行器可替换身份不变|
|R045 Decision|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|保留canonical P7|看到或回复不等于Decision生效|决策回写原工作链|同一Decision避免多页面副本|关键问题一次决定|新增宿主复用原真源|
|R046 Approval|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|动作快照比笼统批准清晰|目标或预算实变要重批|批准后执行仍需效果核验|多账号不能借一次许可横扫|只在真正风险边界询问|权限可收紧失效|
|R047 Result|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|Result与任务状态分离|生成文件不等于业务成功|回到原责任供Review|聚合保留每个来源|先结论后证据|新结果类型仍可引用|
|R048 Evidence|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|Evidence引用不复制正文|来源时间完整性不能靠AI描述|支持接受恢复与复盘|跨业务读取仍需授权|可追问为什么|Provider更换不失历史证据|
|R049 Business Result|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|执行结果与外部结果分开|发布成功不等于增长收入|经营Review等待观察窗口|跨账号比较先验口径|未知不显示零|接入新数据不改Result身份|
|R050 Learning|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|复用accepted Learning|AI总结不能直接变永久真相|评价链先于策略调整|避免把一业务经验强加全公司|显示学到什么及依据|可撤回与版本化|
|R051 Human Handoff|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|分清操作接续决策与责任移交|MFA现场确认确实需要人|人在环但责任不失联|按Scope路由到合法操作者|不把每次操作叫CEO Decision|自动化增强可减少但不删除接续|
|R052 Background Runtime|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|需CEO选App绑定或可选后台|睡眠关机不能承诺在线|后台继续须显式停机恢复合同|并发预算防业务互相挤占|清楚告知关窗后是否工作|服务实现可替换承诺不能偷变|
|R053 Scheduling / Trigger|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|复用三类既定Trigger|时钟错过不能补发所有外部动作|到期先核验再释放工作|合并风暴不重复后继|显示计划时间与实际状态|不要冻结调度库|
|R054 Notification / Attention|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|合并Attention不加通知中心真源|无真实Risk不推断提醒|已处理Decision退出高关注|20业务需聚合与优先级|打扰限真正需要行动|渠道扩展不改Matter|
|R055 Recovery / EFFECT_UNKNOWN|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|增加效果未知语义不造新执行器|超时不能证明外部没发生|先查外界再重试|每个目标动作独立核验|说明待核验而非假失败|远端能力差异保留|
|R056 CEO|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|CEO不配DAG与路由|AI不能代理所有重大承诺|目标边界与重大决定归CEO|多业务用负责人减少逐项干预|普通语言讨论意图|能力增强不取消责任|
|R057 Employee operating context|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|按需上下文比全量历史简单|可见不等于可用权限|Assignment输入输出保持边界|同员工跨业务防泄漏|员工不是模型配置表|模型切换不改变员工历史|
|R058 Global CEO Assistant|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|保持一个全局Assistant|协调不等于行业能力|跟进Bootstrap而非默认执行者|跨区持续但按授权获取信息|全局可达不冒充Leader|外观可变身份Conversation稳定|
|R059 Business Exit / commitment|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|沿用业务退出生命周期|停止工作不撤销已发外部承诺|转交释放资源并留历史|合并拆分不能抹掉原责任|清楚说明未完事项|退出不依赖单一Domain|
|R060 Capacity / Allocation|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|Capability与Capacity分开|会做不等于现在有时间预算|分配冲突进入负责人判断|同员工20业务不能隐式无限并发|需要时提示资源约束|避免固定企业级排程|
|R061 Business Duplication / Template|旧明确理由：持续责任、有界运行、证据先于学习（L1§1/4）；不是永续进程；专门取舍未记载则UNKNOWN|复用Operating Model不克隆员工|凭证历史结果不可复制|新身份重新绑定后经营|多账号不自动拆业务|Copy Preview说明复用与缺失|模板仍独立于Runtime建表|
|R062 Seven Navigation Areas|旧明确理由：Low Surface Complexity / Main自成立 / adaptive（P3§2/S2§0–3）；专门取舍未记载则UNKNOWN|七区不随能力膨胀|能力存在不需独立一级入口|公司经营主域保持稳定|多业务仍靠局部导航|用户无需理解工具清单|未来工具增加不改主导航|
|R063 CEO Desk|旧明确理由：Low Surface Complexity / Main自成立 / adaptive（P3§2/S2§0–3）；专门取舍未记载则UNKNOWN|Desk是注意力不是总仪表墙|事实缺失要诚实Empty|异常结果决定形成日连续|跨业务聚合不过载|低表面复杂度高信息密度|新指标下沉洞察|
|R064 Business Space|旧明确理由：Low Surface Complexity / Main自成立 / adaptive（P3§2/S2§0–3）；专门取舍未记载则UNKNOWN|Business聚合Workspace|Business不是平台账号别名|方向资源结果属于持续业务|单或多Workspace都成立|先业务再专业工作对象|不靠固定模板限定经营|
|R065 Organization Center|旧明确理由：Low Surface Complexity / Main自成立 / adaptive（P3§2/S2§0–3）；专门取舍未记载则UNKNOWN|保留双Tab而非三套组织视图|canonical投影不猜空岗风险|看责任承载和成长|员工多位置是同一身份|公司版图不是HR后台|角色展开不锁死树形数据库|
|R066 Talent & Capability|旧明确理由：Low Surface Complexity / Main自成立 / adaptive（P3§2/S2§0–3）；专门取舍未记载则UNKNOWN|招聘能力装配分开|Catalog存在不等于可执行|安装绑定权限到执行可用|不能全员自动获所有Skill|默认不暴露Provider管理|外部Catalog可换不复制员工|
|R067 Operating Intelligence|旧明确理由：Low Surface Complexity / Main自成立 / adaptive（P3§2/S2§0–3）；专门取舍未记载则UNKNOWN|保留分析面不抢Desk|不做合成健康分或模型榜|结论证据建议接Decision|比较需同范围时窗口径|问题驱动图表|数据增加不制造Analytics真源|
|R068 Knowledge Library|旧明确理由：Low Surface Complexity / Main自成立 / adaptive（P3§2/S2§0–3）；专门取舍未记载则UNKNOWN|保留Reference Space|读取格式支持不能夸大|Work使用关系回到Result|按Scope隔离共享资料|先找读再带入工作|检索实现换代不改资料身份|
|R069 Meetings|旧明确理由：Low Surface Complexity / Main自成立 / adaptive（P3§2/S2§0–3）；专门取舍未记载则UNKNOWN|同Meeting持续对象|聊天展示不证明团队会持续运行|Decision责任WorkResult返回原会议|多人参与不造联系人系统|CEO离开不等于结束|群聊样式与持久合同解耦|
|R070 Settings / Connections|旧明确理由：Low Surface Complexity / Main自成立 / adaptive（P3§2/S2§0–3）；专门取舍未记载则UNKNOWN|六类导航不变设置按Owner下沉|可配置必须有真实生效途径|运行控制与个人偏好分开|公司默认不等于所有员工覆盖|只在必要时显示Advanced|更多参数不增技术后台|
|R071 Four-Pane|旧明确理由：Low Surface Complexity / Main自成立 / adaptive（P3§2/S2§0–3）；专门取舍未记载则UNKNOWN|四职责不是四列常驻|空间展开展示不是Runtime状态|工作在Main辅助按需|多业务上下文切换不串Scope|默认Navigation加Main|视觉重做不改空间职责|
|R072 Left Context|旧明确理由：Low Surface Complexity / Main自成立 / adaptive（P3§2/S2§0–3）；专门取舍未记载则UNKNOWN|局部对象导航不建全局重复菜单|切换上下文需真实目标|保留返回路径|多账号层级按需展开|避免无限树与Tabs|不同Domain可自定局部对象|
|R073 Main|旧明确理由：Low Surface Complexity / Main自成立 / adaptive（P3§2/S2§0–3）；专门取舍未记载则UNKNOWN|真正工作优先|专业表面不能是假Dashboard|Conversation编辑与业务工作合法承载|复杂业务最大面积留工作对象|不是Employee Wall|专业能力变化仍保留工作主面|
|R074 Right Utility|旧明确理由：Low Surface Complexity / Main自成立 / adaptive（P3§2/S2§0–3）；专门取舍未记载则UNKNOWN|辅助详情不抢主工作|完整Conversation不是Utility|证据引用回工作|多来源详情按需查看|复杂阅读可升Main|同对象多表面不复制真源|
|R075 Conversation / Work|旧明确理由：Low Surface Complexity / Main自成立 / adaptive（P3§2/S2§0–3）；专门取舍未记载则UNKNOWN|持续Conversation与Work关联不合并|聊天不是执行日志或执行成功|话题可持续工作可闭合|同Employee多话题Context隔离|从讨论到结果有明确链接|消息实现不决定责任模型|
|R076 Shared Composer|旧明确理由：Low Surface Complexity / Main自成立 / adaptive（P3§2/S2§0–3）；专门取舍未记载则UNKNOWN|复用Frozen基础槽位|不可用附件语音不能假支持|输入引用权限与执行状态一致|宿主扩展不造多Composer合同|渐进呈现不是删功能|视觉可重做语义继续|
|R077 Conversation Quick Access|旧明确理由：Low Surface Complexity / Main自成立 / adaptive（P3§2/S2§0–3）；专门取舍未记载则UNKNOWN|Quick Access不是Assistant|只列合法持久Conversation|关闭入口不删除讨论|同Employee多话题可复开|最近活动降低查找负担|排序变化不影响身份|
|R078 Employee status / Workstation|旧明确理由：Low Surface Complexity / Main自成立 / adaptive（P3§2/S2§0–3）；专门取舍未记载则UNKNOWN|三种Shared UI状态足够|Task完成不能投影Employee完成|工作描述阻塞原因引用事实|同员工并行责任不能乱汇总|不以状态强制展开收起|Runtime枚举扩展不污染UI|
|R079 Visual / IA authority|旧明确理由：Low Surface Complexity / Main自成立 / adaptive（P3§2/S2§0–3）；专门取舍未记载则UNKNOWN|产品结构与视觉分开|Figma通过不等于Runtime通过|研究暂停不丢已验收能力|密度需真实数据验证|竞品可借节奏不改CompanyOS|Iris语言不冻结页面布局|
|R080 Content Growth identity|旧明确理由：共享Intent、逐账号版本/回执、账号隔离（D1§1–4）；账号周期完整化动机旧Frozen未详记；专门取舍未记载则UNKNOWN|Professional Candidate边界保留|产品提供专业环境不等于全渠道Verified|经营对象不等于实现模板|多平台同业务不复制Workspace|用业务语言不是平台型Workspace|专业Domain可扩展|
|R081 Platform / Channel|旧明确理由：共享Intent、逐账号版本/回执、账号隔离（D1§1–4）；账号周期完整化动机旧Frozen未详记；专门取舍未记载则UNKNOWN|Platform作为Channel沿用|平台能力按账号授权核验|发布限制属于平台合同|多平台共同表达不同能力|平台不成为一级工作区|增加平台不增Core enum|
|R082 Account / Channel Account|旧明确理由：共享Intent、逐账号版本/回执、账号隔离（D1§1–4）；账号周期完整化动机旧Frozen未详记；专门取舍未记载则UNKNOWN|Account长期经营聚合已有根基|账号归属授权数据真实性独立|目标策略结果按账号持续|一Workspace多账号合法|账号管理不是再建办公室|不升第五级Scope|
|R083 Account Operating Cycle|旧明确理由：共享Intent、逐账号版本/回执、账号隔离（D1§1–4）；账号周期完整化动机旧Frozen未详记；专门取舍未记载则UNKNOWN|Account Cycle用Domain方法|研究闭环不是新Runtime证明|映射既有Cycle与Work|多账号不违反单活跃Scope合同|看账号经营进展非Cycle后台|并行将来需单独合同|
|R084 Content Intent|旧明确理由：共享Intent、逐账号版本/回执、账号隔离（D1§1–4）；账号周期完整化动机旧Frozen未详记；专门取舍未记载则UNKNOWN|Content Intent保留共享与私有边界|想法不等于可发成品|意图经形式账号适配产出|跨账号复用有权限|同一想法避免手动复制|新媒介仍保留创作意图|
|R085 Platform Form|旧明确理由：共享Intent、逐账号版本/回执、账号隔离（D1§1–4）；账号周期完整化动机旧Frozen未详记；专门取舍未记载则UNKNOWN|平台形式归Domain|能写不代表能生成或发布视频|形式影响输出和验收|平台差异不写进Core|用户理解图文视频等业务形式|新格式由Adapter扩展|
|R086 Account Context|旧明确理由：共享Intent、逐账号版本/回执、账号隔离（D1§1–4）；账号周期完整化动机旧Frozen未详记；专门取舍未记载则UNKNOWN|Account Context引用不复制|私有提示凭证不共享|定位语气约束当前产出|隔离账号同时允许合法共用|展示当前账号清楚|调整定位需要相应Gate|
|R087 Variant|旧明确理由：共享Intent、逐账号版本/回执、账号隔离（D1§1–4）；账号周期完整化动机旧Frozen未详记；专门取舍未记载则UNKNOWN|Final Variant归账号|同文案不代表同一平台输出合法|校验后各自发布与回收|多个Variant分别追踪|只展示需要审阅的差异|复用程度可变身份不变|
|R088 Publishing Employee|旧明确理由：共享Intent、逐账号版本/回执、账号隔离（D1§1–4）；账号周期完整化动机旧Frozen未详记；专门取舍未记载则UNKNOWN|发布责任仍由Curis员工承担|Provider成功回执需验证|审批执行回执失败恢复闭环|各账号权限和副作用独立|用户不必理解底层服务|替换Provider不换员工|
|R089 Publication / partial success|旧明确理由：共享Intent、逐账号版本/回执、账号隔离（D1§1–4）；账号周期完整化动机旧Frozen未详记；专门取舍未记载则UNKNOWN|保留部分成功而非假事务|一处成功不能远程回滚假装没发|核验剩余再恢复|多账号全要求是策略非原子性|明确哪些已发待处理|平台幂等能力可不同|
|R090 Analytics Employee|旧明确理由：共享Intent、逐账号版本/回执、账号隔离（D1§1–4）；账号周期完整化动机旧Frozen未详记；专门取舍未记载则UNKNOWN|分析责任仍是员工|数据拉取不等于经营判断|依据Signal评价策略|跨账号分析需可比口径|先结论与依据|Provider数据源可替换|
|R091 Analytics data quality|旧明确理由：共享Intent、逐账号版本/回执、账号隔离（D1§1–4）；账号周期完整化动机旧Frozen未详记；专门取舍未记载则UNKNOWN|数据质量单列不强行归一|缺失不能归零时间戳需区分|观察窗支持Review|口径不同拒绝假排名|标待连接较旧人工记录|来源增多仍可追溯|
|R092 Monetization boundary|旧明确理由：共享Intent、逐账号版本/回执、账号隔离（D1§1–4）；账号周期完整化动机旧Frozen未详记；专门取舍未记载则UNKNOWN|商业化结果不许过度承诺|内容增长不保证收入|反馈收入按真实来源核验|跨Business不能强套广告模式|边界用普通语言说明|未来交易能力需新授权|
|R093 AiToEarn boundary|旧明确理由：共享Intent、逐账号版本/回执、账号隔离（D1§1–4）；账号周期完整化动机旧Frozen未详记；专门取舍未记载则UNKNOWN|AiToEarn保持可替换候选|静态源码不证明真实发布接通|只承接可验证平台执行数据|账号租户映射需验证|不向CEO暴露为经营主体|不锁定唯一Provider|
|R094 Engagement / external leads|旧明确理由：共享Intent、逐账号版本/回执、账号隔离（D1§1–4）；账号周期完整化动机旧Frozen未详记；专门取舍未记载则UNKNOWN|互动线索是Domain扩展|回复私信交易风险分别核验|必要人工与授权门处理|多平台不能同一权限通吃|不可用明确不假开关|不把所有互动纳当前首版|
|R095 Account responsibility / shared asset|旧明确理由：共享Intent、逐账号版本/回执、账号隔离（D1§1–4）；账号周期完整化动机旧Frozen未详记；专门取舍未记载则UNKNOWN|角色与资产共享有界|同员工不等于全账号可读|责任各自结果关联|共享素材权限与私有账号隔离|组织图多引用非多员工|未来更细权限可下沉|
|R096 Platform schedule|旧明确理由：共享Intent、逐账号版本/回执、账号隔离（D1§1–4）；账号周期完整化动机旧Frozen未详记；专门取舍未记载则UNKNOWN|计划时间与平台定时分开|无平台定时能力不可假支持|本地到期先查权限效果|风暴错过不一口气补发|显示计划与实际执行|调度实现可更换|
|R097 Backup / Recovery|旧明确理由：权限、证据、失败恢复；具体故障窗口/缺字段的旧原因UNKNOWN；专门取舍未记载则UNKNOWN|DB文件Manifest统一恢复|备份成功不代表可还原|恢复后重连核验再继续|多业务必须保持引用一致|给恢复预览不是数据库面板|版本兼容与secret边界稳定|
|R098 Update / version compatibility|旧明确理由：权限、证据、失败恢复；具体故障窗口/缺字段的旧原因UNKNOWN；专门取舍未记载则UNKNOWN|版本与回退进入系统支持|签名与安装状态需真实证据|升级前保护未完Work|所有Scope一致恢复|普通用户看版本与风险|不把Beta限制冒充稳定发布|
|R099 Network / proxy / TLS|旧明确理由：权限、证据、失败恢复；具体故障窗口/缺字段的旧原因UNKNOWN；专门取舍未记载则UNKNOWN|网络设置仅连接需要时|代理TLS不是业务权限|失败区分网络与Provider|不同租户凭证隔离|默认系统网络高级按需|不冻结库与代理实现|
|R100 Resource conflict / concurrency|旧明确理由：权限、证据、失败恢复；具体故障窗口/缺字段的旧原因UNKNOWN；专门取舍未记载则UNKNOWN|资源限额不做企业排程台|本地资源不是无限|限流等待须可恢复|多业务公平预算需验证|仅必要限制与解释|容量策略可演进|
|R101 External trust / prompt injection|旧明确理由：权限、证据、失败恢复；具体故障窗口/缺字段的旧原因UNKNOWN；专门取舍未记载则UNKNOWN|外部内容当数据非指令|网页文档可能恶意注入|权限执行依据受信合同|跨Scope检索防扩散|不用让CEO审每条内容|新Provider仍守信任边界|
|R102 Permission / data egress|旧明确理由：权限、证据、失败恢复；具体故障窗口/缺字段的旧原因UNKNOWN；专门取舍未记载则UNKNOWN|申请权限与有效权限分开|本地Agent可能缺真实沙箱|高风险动作按有效边界执行|跨业务访问不继承展示可见性|显示实际可用而非假权限|Provider能力增强再放开|
|R103 Accessibility / input behavior|旧明确理由：权限、证据、失败恢复；具体故障窗口/缺字段的旧原因UNKNOWN；专门取舍未记载则UNKNOWN|可访问性是交互质量非新导航|设计图不证明键盘可用|错误恢复也必须可操作|密集数据不牺牲导航|普通用户与辅助技术皆可用|不锁定视觉组件库|
|R104 Diagnostics / safe export|旧明确理由：权限、证据、失败恢复；具体故障窗口/缺字段的旧原因UNKNOWN；专门取舍未记载则UNKNOWN|诊断用引用摘要不暴露日志墙|Secret与私有内容必须脱敏|故障可追根并回原Work|多租户诊断隔离|提供可理解原因与导出边界|不要新增第二UsageLedger|
|R105 State taxonomy / Conflict|旧明确理由：权限、证据、失败恢复；具体故障窗口/缺字段的旧原因UNKNOWN；专门取舍未记载则UNKNOWN|不新增全局Conflict状态|来源不一致不证明对象冲突|Unknown与Review-needed容纳核验|多来源保留各自事实|表述需要核实而非新枚举|Domain细分不污染Shared|
|R106 Discovery / product derivation method|旧明确理由：Product≠Implementation、Research不覆盖Current（P0/AGENTS）；专门取舍未记载则UNKNOWN|从真实工作推导补合同|纸面压力测试不是交付证据|覆盖异常恢复才闭环|跨域验证避免CG特化|设计不再自行脑补核心逻辑|方法保留但不成为Runtime|
|R107 Product Expression V2 layering|旧明确理由：Product≠Implementation、Research不覆盖Current（P0/AGENTS）；专门取舍未记载则UNKNOWN|分层比巨型Blueprint简单|字段是要求不是已可采集|SharedDomain各有唯一Owner|能力增加不膨胀主导航|按钮样式留设计|日常会话不读全部研究|
|R108 OSS reuse choices|旧明确理由：Product≠Implementation、Research不覆盖Current（P0/AGENTS）；专门取舍未记载则UNKNOWN|库名下沉实现|仓库代码存在不等于可用验收|按能力合同选择复用|替换依赖不改公司身份|用户不选底层框架|允许技术升级|
|R109 Current vs Target|旧明确理由：Product≠Implementation、Research不覆盖Current（P0/AGENTS）；专门取舍未记载则UNKNOWN|目标与已交付两条路线|G-V未运行不得写支持|验收逐能力逐环境|一个Domain通过不能推广全部|能力缺口诚实表达|后续验收只升级证据覆盖范围|
|R110 No second systems|旧明确理由：Product≠Implementation、Research不覆盖Current（P0/AGENTS）；专门取舍未记载则UNKNOWN|禁止新TaskEmployeeResult系统|新命名不能掩盖重复真源|连续链复用现有对象|多业务通过引用隔离扩展|用户不面对多个管理后台|新能力先扩合同再证明必要|

## 6. Deep arbitration — 决定性的七处对照

### 6.1 价值与经营链：旧骨架赢，新证据补执行深度

P1§1/11、P5§1/3、L1§1/4已经包含一人AI公司、持续经营、真实外部结果、Review/accepted Learning、下一周期。N9纠正“必须拥有最强AI”和“所有业务都为短期赚钱”的推断，不是在更换北极星。W1§2/6甚至早已要求Operating Model先于专业界面与Package。

旧不足是P1§13/P2末尾把“一级区→页面→AI→能力”写成唯一推导顺序，容易把工作能力留给UI猜。建议改为：真实经营/工作证据确定需求和边界→在既有产品结构中落位→补合同→UI/实现验证；仍禁止从Runtime表反推导航。这是方法消歧，不删除现有七区。

### 6.2 Employee与Context：新不是第二种“共享员工”

S1§1.2–1.4/3已明定同一Employee多Assignment、Functional Affiliation≠服务范围、持久员工知识≠执行Context。P4§21/23和Phase A允许same Employee multiple topics以及同一Conversation跨Assignment的合法消息；P5§1.1旧的Identity/Assignment Conversation强制分割措辞需同步，不能用其否决后续决定。

1个业务不需要员工配置矩阵；5个业务可以一个分析员工承担多个Assignment；20个业务的聚合不赋予其读取全部资料的权限。浏览B账号不把正在写的A消息或已批准动作自动切到B。跨业务投影多处出现的是同一身份，不是可相互覆盖的20份Profile。

### 6.3 Human Handoff：真正的Frozen绝对句，而非“旧产品没有人工”

P1§9/11明确人工外部Feedback与接管，S6明确技术权限请求不得包装为CEO Decision；S2§3.11却写“CEO/用户只在Decision Gate操作”。N8§15的登录/MFA/手机确认、N7现场生产事实表明：有些动作不是经营决策，而是人才能完成或当前能力无法代理的执行。将它们一律包装为P7会污染Decision；解释成P5又会把每个登录都变成员工责任转移。

推荐F1（MERGE，不新增CEO方向问题）：按S6既有Frozen边界修正P4，保留automation by default；允许必要人工执行/补材料/接管，说明原因、目标、已准备材料、完成判据、回程；用户“完成”只是报告，需要核验后续事实。**不新增HumanWork/HandoffV2，也不声明现有P5 schema已经能表达全部人工接续**。UI可共用“需要你”，底层动作类别仍分清；技术映射另审。

### 6.4 Model与Browser：旧能力不是零，新细分也不能成为配置后台

P3已有Provider、发现、模型选择、能力/健康；I1保留DeepSeek真实连续性接受。N1 C04的模型profile probe是合成输入的静态分支检查，不是线上模型失败率；它能反证“空metadata就默认chat”等推断，不能否定已验真实调用。

补查S5§5.2发现SUPPORTED/UNSUPPORTED/UNKNOWN、evidence_source、context_limit、cost unknown早已存在于旧Review合同，S6还冻结requested/configured/effective和resume重新核验。因此不能声称这些是这两天首次提出。真正补的是连接、目录、模型、具体用途测试、可执行权限的完整闭合；发现不完整不能让所有模型下架；supported/unsupported/unknown有来源、版本、时效。用户说“让他看这张图”，系统先选合格能力，不要求CEO掌握context window/top-p；没有合格能力坦诚阻塞，不偷偷丢图片。

Browser必须区分Search/Reader/Interactive。能显示WebView、研究者在Chrome操作成功、安装Playwright，均不证明Curis员工已可安全浏览。产品合同需规定账号隔离、人工接管、有效权限、现场观察、结果核验；Profile隔离不等完整安全沙箱。Browser不是第八导航或全新通用Agent产品。

### 6.5 外部效果与后台：持久化恢复不是持续运行承诺

L1已有restart/幂等/WAIT，但N8§16记录“远端接受、本地未保存ID、重试可能重复”的窗口；固定来源源码与Issue是风险证据，不是本轮故障复现。需要将**是否已产生外部效果**与本地attempt错误分开。不能为了更少状态做FAILED→RETRY，也不能承诺所有外部系统exactly-once。

N4 G3选择opt-in用户级Local Background Service，会改变用户对关窗口/退出App的预期，是F2真实产品决定。后台不是永久Agent Session；休眠/关机/登出不能工作，恢复先核验。重开同root可恢复旧Work的证据，不能证明关UI后仍运行。

### 6.6 Content Growth：Account闭环是扩已有合同，不是重排Company层级

D1§1.2已有账号定位和语气；D2§2.2已有Account Goal/策略/节奏/表现，但D2是Approved Candidate。D1§1.5早有逐账号Variant及FULL_DIVERGENCE。新研究把这些连接成Account长期经营的计划、结果、复盘和下一轮，属于Domain合同完整化，不能宣称过去只懂生产。

建议Account继续Company资产；Business→Platform→Account是经营观察/策略视角，**不是canonical父子链**。账号级周期指节奏、计划与评估关系，不新增第五执行scope、不要求每Account一个Workspace，不引入与L1 single-active Workspace Cycle冲突的第二循环Runtime。若未来真的要求同Workspace每账号独立并发control-cycle，另提Architecture/Product Delta，不从当前文字自动授权。

N5“没有跨账号合并一条数据”的绝对表达应限定为“不覆盖/混淆逐账号原始事实”；合法同口径派生分析仍允许。N5新平台决策也应服从Approved Strategy Envelope：重大方向/承诺才Gate，不把每次低风险渠道实验变CEO审批。

### 6.7 包与专业工具：保留最小Core，不把行业流程写死

S1/W1已有Package承载专业语义、Surface、能力和方法引用。Terminal/Git/OCR/Data/Media能服务不同工作，不必成为公司一级业务域。技术库选型只能帮助实现这些合同；Playwright/APScheduler/Docling/FFmpeg/LiteLLM/DBOS/Temporal/browser-use都不成为Blueprint名词或必装清单。

研发复杂编辑/调试需要Main，不代表把Curis变IDE；资料阅读保留Reading Main，不代表资料库变RAG后台；模型完整配置在Settings，不代表Curis变LLM Gateway。未知宠物寄养仍须真实行业研究、现场/法律/人力条件，不能靠安装上述库自称会经营。

## 7. MATERIAL PRODUCT CHANGES — 真正需要接受的合同变化

这些是**拟改变目标合同**，不是已发生Authority更新。六组覆盖增量，不把110行当110项新功能。

|变化|OLD → Proposed NEW|WHY / evidence|User impact|接受/实施边界|
|---|---|---|---|---|
|M1 人工参与边界|人工反馈已有但P4绝对限制 → 必要人工接续与Decision分开|N8§15真实平台交接机制；S2§3.11矛盾|不反复假批准，不要求AI假装登录/实拍/认证|F1按已有ADR治理修正；现有Work/P7/P5映射后另验|
|M2 Browser完整合同|工具/成熟能力原则 → Search/Reader/Interactive各有边界，账号隔离/接管/恢复|N1 C12–16；N4 G1|知道AI能访问什么、当前为何需自己操作|目标Shared合同；G1-V未运行|
|M3 Model能力完整度|真实发现/选择已在 → 来源明确逐能力测试、用途选择、受限fallback|N1 C04–06；N4 G2|不把能聊天误当能看图/调工具；不要求复杂首次配置|保留已有接受；G2-V未运行|
|M4 后台承诺|能恢复不等离开UI继续 → opt-in本地后台＋可解释停止/睡眠/恢复|N4 G3；N1 C25|关UI后是否继续可预测，不虚假24/7|F2 CEO决定；G3-V未运行|
|M5 安全执行与公司恢复|概括失败恢复/备份 → 效果未知先对账、批准快照、managed files/reconnect/resumecheck|N8§16；N4 G4/G6|避免重复外发/恢复后自动重放；备份不误承诺带回秘密|Shared细化，G4/G6验证独立|
|M6 账号经营合同完整化|已存在Account策略/Variant/回执 → 同一账号目标、节奏、计划、反馈、Learning连续关系|D1§1.2；D2§2.2；N5/N6|账号不只是发布目的地；看下一步而非管理流程树|Domain扩展，非新Account runtime/新Core层级|

Professional Tools是现有能力体系的合同覆盖扩展；每一种工具是否进入当前交付需按真实依赖验证，不据此增加七区或全员默认安装。

## 8. CLARIFICATIONS ONLY

以下不应营销为“新产品模型”：一人AI公司/任意业务；持续责任与bounded Cycle；Evidence先于Learning；Company→Department→Business→Workspace；原装组织/Business=0；同员工跨业务责任；Leader经营领导；CEO不逐任务派发；Assistant协调不代专业者；Provider非Employee；成熟复用/Package First；Generic合法；专业≠Verified；七区/Four-Pane；对话持续性；每账号Variant/Publication；未知不填0；业务退出保护承诺与历史。

旧Blueprint也不是“只有页面标题”：P2已经有Company/Department/Business/Role/Employee/Expert/Skill/Connector/Meeting/Settings/Duplicate及经营洞察字段合同。真实缺口是特定能力的输入、权限、输出、状态、失效与恢复覆盖，而非再列全部页面或再造Field Registry。

## 9. REJECTED NEW IDEAS / rejected interpretations

并非下列每项都是N2最终仍坚持的主张；明确区分原候选与被误用的解读。N6已主动拒绝的表达继续拒绝，不把它们算本报告新发现。

|候选/解读|证据定位|裁决理由与保留的需求|
|---|---|---|
|全部能力变新导航/中心，48能力=48产品对象|N2 V01–29/C01–48的膨胀风险|REJECT；同Owner按需入口，不裁掉真实工具能力|
|77设置全对CEO开放、首次配置全套参数|N2§7；V03 required facts误读|REJECT；§13逐项分层，内部必需事实不等用户必填|
|Employee等待/完成作为Shared状态|N2 C30与S2§3.1|REJECT；Work/readiness/雇佣状态可表达但不改Employee三态|
|Account=Workspace或第五execution scope；所有业务一条团队Workflow|N5简链误读；N6§3.2已经纠正|REJECT；保留Account长期经营语义和canonical parent|
|每次策略调整/新平台均CEO批准|N7 B3/B13；N5§1.1绝对句|KEEP OLD envelope；CEO已授权的日常实验无需重复Gate|
|全部Result只能归Business|N9对旧研究的纠正；P4§16|REJECT；Company/Department合法工作同样有Result|
|整套聊天放右Context、Assistant代专业执行|N6§1对V1的纠正|REJECT；完整工作Main，浮动Assistant只协调|
|资格地图/统一机会状态机/钱包结算/利润必达|N6§1/11；N9反证|REJECT；保留目标相关条件、来源与真实收益证据|
|所有账号数据完全不能汇总|N5§1.4|REJECT绝对句；同口径派生比较合法，原始事实不混|
|AI能力百分比/L3足以宣布自主经营|N7 B13/B14；N8未执行边界|REJECT；纸面分工、真实员工调用、完整外部闭环各自验收|
|AiToEarn唯一/主要全平台底座；或它只有发布没有Analytics|N8§25|两者均拒绝；部分Provider候选，逐平台逐动作实证|
|chat成功证明Vision/Tool；OS授权证明Computer已可执行|N1 C04/C16；N4 G1/G2|REJECT；具体能力证明不可替代|
|失败就retry/fallback、恢复就重放、stop可撤销外部事实|N4 G4/G6；N8§16|REJECT；先确定效果与授权，未知可等待|
|PlaybookV2/ProviderWorkV2/AnalyticsV2/新Usage账本|S1§0A/3；N4§11–12|REJECT新增系统；复用当前Owner和引用|
|强制某OSS库/固定token数/固定批次/每面固定卡数成为Blueprint|N4技术候选；N2§7–8；E2|MOVE DOWN；工程测试目标/设计待验证，不产品永久常量|

## 10. Final Product Truth Summary — proposed, not registered

Curis帮助一个真实CEO，用真实且稳定的AI Employee组织持续经营；AI能力可由成熟模型、Agent、Skill、工具、Provider、Package和Knowledge供给。Company拥有同源身份、组织、责任、工作与证据；Business承担持续经营方向，Workspace承载具体工作，Employee通过合法Assignment承责。Provider能做的动作与Curis承担的经营责任不能互换。

经营关系是Goal/Strategy/Responsibility→Plan/Work→真实执行→Result/Evidence→Review/accepted Learning→显式下一步；不是统一固定行业DAG。人处理不能合理代理的事实、操作和重要Decision；Leader在批准边界内继续经营。未知能力、未知结果和外部不可用均可诚实表达与恢复。

所有新能力必须满足同一身份、权限、Context、证据、版本和恢复边界。通用合同置Shared、专业规则置Domain、实现库置Technical。目标完整性不要求普通CEO看到内部全部字段。

## 11. Seven Navigation / Four-Pane final arbitration

|一级区|判断|继续负责|不吸收|
|---|---|---|---|
|CEO工作台|KEEP|公司注意力/简报/结果/下一决定|配置后台、全部Work监控|
|业务空间|KEEP|Department/Business/Workspace经营入口与专业工作|全平台账号管理根|
|组织中心|KEEP|公司版图＋员工目录|日常Leader聊天或第二组织Truth|
|人才与能力|KEEP|招聘/创建/发现/扩展能力|Model与所有连接配置副本|
|经营洞察|KEEP|趋势/比较/归因/报告/决策支持|第二Analytics/Usage账本|
|资料库|KEEP|Company Reference Space、阅读引用与UsedBy|文件系统/RAG控制台|
|会议|KEEP|持久多人经营讨论及责任结果连续性|Calendar或审批后台|

Browser、Model、Provider、Background、Notification、Recovery、Professional Tools均**不ADD一级导航**：分别进入Workspace能力/Settings/原Work/Attention及情境入口。没有证据支持REMOVE任何七区。

Four-Pane全部KEEP：Navigation公司级；Context局部对象；Main真正工作；Utility辅助读取/详情/预览。Utility可放大阅读不代表它是第二Main工作系统。独立浮动Assistant保持same identity/conversation；“跨公司入口”不解释为新增多Company切换产品，当前是公司级跨七区协调。Conversation-first是工作的持续关系，不要求CEO Desk/账号经营摘要先打开聊天才能看懂。

## 12. Capability final ownership / layering

分类是责任分层，不是五套重复目录。Employee绑定可以调用同一共享能力；专业面是入口，不拥有第二实现。
|Capability|最终责任层|用户主入口/情境入口|Provider implementation|不可混淆|
|---|---|---|---|---|
|Model|共享能力；Employee用途选择|模型设置/会话选择|模型Provider|不等Employee或身份|
|External Agent|Employee执行能力|员工能力/工作现场|Agent适配|不拥有Company Work|
|Skill|Employee能力组合|人才与能力/Employee详情|Skill包|安装≠绑定≠有效|
|MCP|Provider传输/工具暴露|连接/高级能力|MCP适配|不作为CEO业务概念|
|Connector|共享连接能力|人才发现→设置维护|授权/接口适配|定义≠已连|
|Browser|共享执行能力，按Employee授权|Work现场观察/必要Main|隔离浏览器或合法桥|账号与控制权隔离|
|Search|共享Web研究能力|工作搜索/来源|搜索Provider|非公司Global Search|
|Reader|共享只读获取能力|Reference/Work|页面读取适配|非Interactive|
|Computer|共享受限操作能力|OS授权/工作接管|本机控制适配|模型/Adapter/OS三者交集|
|File|共享工作资源能力|当前Work/合法文件选择|文件系统适配|工作文件≠自动Knowledge|
|Terminal|专业工作可装配能力|必要专业Main/输出详情|受控进程执行|非全公司终端中心|
|Git|Workspace专业能力|研发/相关Work|Git工具|commit/push独立授权|
|Preview|共享结果/专业工具能力|辅助Utility/复杂Main|真实本地或远端预览|截图≠运行|
|OCR / Document Parser|共享材料处理能力|导入/阅读/提取Work|解析Provider|逐格式/页验证|
|Data|共享访问能力＋Domain分析方法|数据工作/洞察|只读/受控查询适配|不复制Metrics Truth|
|Media|共享生产/处理能力＋Domain约束|内容Work/成品预览|生成/转写/转码Provider|各能力单独证明|
|Social Publish|CONTENT GROWTH DOMAIN能力|Publication/原Work|平台/候选AiToEarn|发布Employee保留Curis|
|Analytics Provider|Domain外部数据来源|资料/账号/洞察引用|逐平台数据适配|解释/Review属于Employee|
|Notification|COMPANY共享注意力能力|Desk/系统通知|本机通知设施|多入口同一Matter|
|Scheduler|共享触发控制职责|当前工作/运行偏好|时间调度库|不拥有第二Work或业务Cycle|
|Backup|COMPANY/应用连续性能力|Settings数据与应用|一致性备份恢复机制|不备份普通secret/cookie|
|Knowledge|COMPANY共享Reference能力|资料库/工作Picker|现有存储检索/未来解析|scope/UsedBy同源|
|Package / Method|专业组合/Employee方法输入|Workspace/必要高级详情|现有Package机制|Core不写行业Flow|

## 13. Settings final boundary — 77项逐项收敛

下表七类是**Owner/权限语义维度，不是替换Current Settings的七个导航Tab**。继续消费既有Settings分类和头像入口。普通用户只看到对当前任务必要的选择、真实状态、权限和修复；自动发现的事实不能伪装为可编辑参数。Settings清单中的测试、选资料、接管、恢复等实际是动作，不能因列入台账就变长期配置。

所有S编号来自N2§7。下表是候选去向，不代表Current已实现；没有读取实际个人设置，当前值仍UNVERIFIED。系统强制安全规则不能被Advanced开关关闭。工作/员工/Company的多处入口消费同一有效配置，不复制存储。N2§8模型事实（context/price/capability等）有来源才显示；用户只可在允许条件下收紧软预算，不能编造硬能力。S6已冻结请求批准/自动处理/完全访问三档；新工具清单不得重新变成逐项CLI授权表。

|N2 ID|候选设置|Owner层|普通/自动/高级/不暴露|仲裁与最小保留|
|---|---|---|---|---|
|S001|CEO显示名与头像|USER / PERSONAL|普通可编辑|姓名/头像共享身份，不改Employee/Model identity|
|S002|界面语言|USER / PERSONAL|普通可编辑|界面语言不修改业务资料和外部内容事实|
|S003|个人显示时区|USER / PERSONAL|普通可编辑|显示时区与经营排程时区分开|
|S004|外观与减少动画|USER / PERSONAL|普通可编辑|外观消费Current语言；减少动画，不冻结新视觉|
|S005|Composer发送方式|USER / PERSONAL|普通偏好|中文IME组合输入不能误发送，快捷键需验证|
|S006|通知事件|USER / PERSONAL|普通可编辑|通知类型偏好不等Work/Decision授权|
|S007|OS通知与锁屏内容|USER / PERSONAL|必要OS授权＋隐私偏好|锁屏敏感内容保护；不能假装已获系统许可|
|S008|Quiet hours|USER / PERSONAL|普通可编辑|安静时段不绕过风险Gate；不逐Work轰炸|
|S009|Digest与移动渠道|USER / PERSONAL|摘要偏好/移动按真实能力|不因配置字段存在就承诺移动推送已接通|
|S010|Company名称与经营时区|COMPANY|普通可编辑|公司身份/经营时区变化需解释影响|
|S011|公司目标与运行边界|COMPANY|经营上下文编辑|Goal/约束从提案形成；不转复杂初始化表单|
|S012|费用预算与超限行为|COMPANY|普通经营设置|预算界限可编辑；缺实际成本显示unknown|
|S013|Provider连接名称|PROVIDER / CONNECTION|普通名称|同品牌不同连接可区分；连接不等模型|
|S014|Provider类型与认证方式|PROVIDER / CONNECTION|连接向导按需|只提供适配实际支持的认证方式|
|S015|API Base URL|PROVIDER / CONNECTION|自定义时高级|Base URL合法校验；普通用户用已知服务入口|
|S016|Provider凭证|PROVIDER / CONNECTION|必要授权|凭据只显示引用/状态；不回显Secret|
|S017|Provider Organization / Project|PROVIDER / CONNECTION|Provider要求时|组织/项目只在真实需要时要求|
|S018|Provider Region|PROVIDER / CONNECTION|真实需要可见|地域/隐私边界不静默跨区fallback|
|S019|模型发现与手动Model ID|PROVIDER / CONNECTION|发现自动＋受限补充|手动ID不是自证可用；部分发现不全量下架|
|S020|Model别名与能力声明|CAPABILITY ADVANCED SETTINGS|名称可编辑/能力只读来源|用户声明不自动Verified；显示声明/测试差异|
|S021|Context与输入硬限覆盖|CAPABILITY ADVANCED SETTINGS|只读事实＋高级软限制|不得扩大真实context硬上限；候选已写软限制，不误批为任意override|
|S022|Company用途默认|COMPANY|用途默认按需|普通用户少量默认；系统按任务选择可用能力|
|S023|Employee用途选择模式|EMPLOYEE|按职责可选|非全员强制配置；同一用途规则同源|
|S024|Fallback策略|CAPABILITY ADVANCED SETTINGS|高级受限|回退需能力/隐私/预算兼容；未知外部效果禁止换Provider重发|
|S025|Temperature|CAPABILITY ADVANCED SETTINGS|高级|仅模型支持时；默认省略用服务默认|
|S026|Top P|CAPABILITY ADVANCED SETTINGS|高级|不默认要求与Temperature同时调|
|S027|Reasoning effort|CAPABILITY ADVANCED SETTINGS|高级/情境|按Provider真实枚举；不伪装思维全文|
|S028|Max output|CAPABILITY ADVANCED SETTINGS|高级|真实上限与Work预算约束|
|S029|请求Timeout|CAPABILITY ADVANCED SETTINGS|高级受限|Timeout不等远端未执行|
|S030|Retry规则|CAPABILITY ADVANCED SETTINGS|内部安全默认/高级下调|不能用户勾重试就绕过EFFECT_UNKNOWN|
|S031|Context policy|EMPLOYEE|自动必要Context/高级偏好|reference-first；不得静默丢关键材料；token预算不是CEO必填|
|S032|Tool policy|EMPLOYEE|上下文授权＋高级清单|工具选择不能覆盖更高权限|
|S033|并发与Rate Limit覆盖|PROVIDER / CONNECTION|只读实际限制＋高级降低|unknown不编配额；不提供无证据扩大上限|
|S034|模型测试项目|PROVIDER / CONNECTION|动作：测试|不是长期Setting；按用途必要项目，不首次强跑全套收费测试|
|S035|External Agent安装与执行环境|WORKSPACE|按需安装/就绪|环境自动探测优先；可执行路径手填放高级，不普通门禁|
|S036|External Agent启动参数|CAPABILITY ADVANCED SETTINGS|高级|启动参数/环境白名单；不继承所有shell秘密|
|S037|Skill / Plugin安装和启用|EMPLOYEE|动作：发现/安装/启用|来源版本权限按人才/能力机制，不复制设置商店|
|S038|能力更新策略|CAPABILITY ADVANCED SETTINGS|高级策略＋更新动作|新增权限重审，版本固定仅支持时|
|S039|MCP连接|PROVIDER / CONNECTION|现成连接普通/自定义高级|stdio命令/远端传输参数不让小白从零填|
|S040|MCP工具范围|EMPLOYEE|范围授权可见/schema高级|参数由工具合同约束，不能随意改变schema|
|S041|Web Search连接与范围|PROVIDER / CONNECTION|连接＋Work研究筛选|站点语言时间是本次研究参数，不全公司设置副本|
|S042|Page Reader与来源保存|WORKSPACE|动作：选/读/引用|提取范围/保存出处属于Work；不固定长期设置|
|S043|浏览环境与账号绑定|PROVIDER / CONNECTION|账号连接/核验|Profile自动隔离；用户不管理底层profile路径|
|S044|Browser执行方式|CAPABILITY ADVANCED SETTINGS|系统解析/高级诊断|合法已验路径自动匹配；不强迫用户选择浏览引擎|
|S045|Browser站点与动作权限|EMPLOYEE|情境授权|只读/上传/发布等权限明确；不是一键全电脑|
|S046|浏览会话保留与占用|CAPABILITY ADVANCED SETTINGS|保留偏好高级；接管是动作|占用状态自动；lease/锁不用户配置|
|S047|浏览观察与调试采集|WORKSPACE|动作：观察/诊断|现场观察可见；Console/Network高级且脱敏|
|S048|屏幕读取与辅助控制|USER / PERSONAL|必要OS授权动作|读屏/控制独立；系统授权不等执行能力|
|S049|文件读取授权|WORKSPACE|动作：选文件/目录授权|默认最小只读，不授权任意路径|
|S050|输出目录与写入授权|WORKSPACE|按Work设置输出|用户可选目标；不默认覆盖输入|
|S051|文件冲突策略|WORKSPACE|冲突时决策|新版本/另存/合并按支持；默认不破坏原件|
|S052|运行环境与登记命令|CAPABILITY ADVANCED SETTINGS|高级|环境/命令范围与权限，普通用户不配完整Shell|
|S053|进程超时与输出限制|SYSTEM / RUNTIME|内部默认＋高级资源边界|进程树/owner/lease由实现，非CEO必填|
|S054|仓库和变更交付|WORKSPACE|专业上下文|Git读/写/commit/push分开，不推广所有Business|
|S055|Preview启动与访问|WORKSPACE|专业上下文|实际端口/进程由系统识别；外网暴露需授权|
|S056|解析/OCR与导出|CAPABILITY ADVANCED SETTINGS|自动识别＋必要修正|解析语言/格式按需；不以OCR工具名称做产品入口|
|S057|媒体生产规格|CAPABILITY ADVANCED SETTINGS|Work制作需求＋高级|尺寸/格式来自目标平台或交付；不全公司强制媒体参数|
|S058|数据库/数据连接|PROVIDER / CONNECTION|连接时必要|数据源认证/范围；默认只读不假安全|
|S059|查询额度与口径|WORKSPACE|数据工作按需|查询/快照本次Scope；高风险写另Gate|
|S060|数据外发与执行位置|COMPANY|政策＋动作级说明|外发内容/目的地明确，不能开全公司任意外传|
|S061|授权范围与有效期|EMPLOYEE|授权范围可见|有效权限交集；Organization Role不等技术Grant|
|S062|敏感动作确认|COMPANY|政策/风险门|Approval快照，不强制每Work逐项CEO批准|
|S063|外部内容与插件信任|SYSTEM / RUNTIME|强制安全默认|不可信输入不当指令，不能设置关闭信任边界|
|S064|关闭与后台运行行为|USER / PERSONAL|明确opt-in（F2待决）|关UI/停所有工作含义可见；后台进程参数不露|
|S065|Work排程与触发|WORKSPACE|经营节奏可编辑|真实时区/下一检查，内部cron可高级，不逼CEO写表达式|
|S066|错过与重叠策略|SYSTEM / RUNTIME|安全默认＋必要偏好|错过只合并检查，不能自动补跑过期外部写|
|S067|共享资源并发上限|SYSTEM / RUNTIME|占用可见/资源偏好高级|调度lease/锁Owner不设普通字段|
|S068|备份范围与目标|COMPANY|动作＋备份偏好|选择位置/范围；排除秘密；加密无实现不假勾选|
|S069|恢复选项|COMPANY|动作：恢复|preflight/影响/重连/Resume Check；非第二公司初始化|
|S070|存储容量与缓存维护|SYSTEM / RUNTIME|存储事实＋安全清理|保留Evidence/managed assets；缓存清理不删经营历史|
|S071|资料时效与保留|COMPANY|按Domain规则/高级|freshness依数据口径，不全公司一个随意TTL|
|S072|诊断与日志保留|SYSTEM / RUNTIME|动作：诊断导出|范围预览脱敏；发送单独授权，不自动全量日志|
|S073|App版本与更新|SYSTEM / RUNTIME|只读版本＋升级动作|版本事实不能编辑；升级不重建身份|
|S074|归档与停用影响选择|COMPANY|原对象生命周期动作|归档/退役保责任承诺和历史，不当全局切换|
|S075|后台网络与Proxy|PROVIDER / CONNECTION|高级|按连接出口诊断，不读/泄露秘密|
|S076|企业证书与连接诊断|PROVIDER / CONNECTION|高级受控|证书信任需合法；不提供禁用TLS万能修复|
|S077|Browser上传与下载|WORKSPACE|情境文件授权＋高级限制|Browser上传下载继承当前Work/账号/文件范围；不是无限传输授权|

## 14. Product Expression V2 — 内容逐类去向

N2不应整体晋升。下表覆盖其主要内容类；C01–C48在矩阵及能力表对应，S001–S077在上一节逐项处理。

|N2内容|建议分类|保留什么|裁掉/下沉什么|
|---|---|---|---|
|§1产品原则/价值/范围|BLUEPRINT|稳定关系、完整能力不等技术后台|全产品完成/默认AI能干的推断不接收|
|全局交互/状态/字段语言（F类）|SHARED PRODUCT CONTRACT|输入→动作→状态→失败→恢复、来源、引用|状态词不自动变enum；标签不等新canonical对象|
|Main/Utility/Modal/Drawer/Context职责|SHARED PRODUCT CONTRACT|服从S2的任务空间责任|固定大小/所有对象同一Drawer/对话右栏拒绝|
|V01–V29各面信息责任/入口/返回|UI DESIGN INPUT|同源对象、必要动作/未知/回程、复杂度限制|不得按29编号增29常驻页面或重冻Composition|
|C01–C48工作能力完整合同|SHARED PRODUCT CONTRACT为主|跨域输入/输出/Owner/权限/恢复|行业方法进DOMAIN，技术参数进IMPLEMENTATION|
|CG V26–29及账号/版本/发布|DOMAIN CONTRACT|D1既有对象扩展、账号经营/逐账号效果|不改变全局层级、Main或造结算Runtime|
|§7 S001–S077|SHARED＋UI INPUT＋IMPLEMENTATION|上一节分类后的最小可操作管理合同|把所有参数在普通Settings平铺的解读REJECT|
|§8 Model/Profile/Connection字段|SHARED MODEL CONTRACT|能力方向、来源/测试/时效、发现完整性、真实成本|具体协议映射/模型库选型/默认数值下沉|
|G1–G6后续验证/测试目标|IMPLEMENTATION CONTRACT|失败注入/恢复/权限/一致性验收|未执行不称PASS，不写入CurrentState完成|
|行业研究、功能清单、OSS比较、历史例子|PROVENANCE / RESEARCH|定位来源，保留被拒绝理由|不进入日常设计必读链；不是另一Authority|

N2有价值的不止UI细节：Browser隔离/外部效果未知/后台边界/备份重连会影响产品承诺，不能全推给开发；反过来约30–50批次、token预算、默认进程超时、库名称也不能全塞核心Blueprint。Map展开被接受字段，UI Blueprint消费承载，二者不自行补产品。

## 15. Authority / file governance decision

**本轮分类不改变文件实际状态。** “TO BE UPDATED”指下一轮候选动作；“SUPERSEDED”仅在已有明确后续Authority或未来CEO接受后才成立。全量文件清单和动作见Change Plan。

|文件集合|建议治理归属|当前有效性/后续动作|
|---|---|---|
|P0–P4|CURRENT AUTHORITY / TO BE UPDATED（必要处）|保留唯一入口与三Canonical正文；本报告不成为默认入口|
|P5|TO BE UPDATED|模块入口纠正旧Assistant/Office/Conversation/默认组织/版本表述；不另立产品|
|S1/S2|CURRENT SHARED / TO BE UPDATED|保留Owner与空间；F1按S6既有决定窄修P4（本轮不执行）；G能力按职责扩共享合同|
|S5/S6|共享产品投影候选 / CURRENT FROZEN ADR|S5能力三态与产品字段按已消费范围继承；S6技术授权≠CEO Decision保持。不能将S5全文随§5.6一起冻结|
|S7/S8|REVIEW / 已消费部分继续有效|Conversation模型选择、Settings分类按P1/P3消费范围保留；旧实现状态与未接受建议不升级Authority|
|S3|CURRENT VISUAL LANGUAGE|本轮NO CHANGE；视觉语言与未批准Final Composition不同|
|S4|CURRENT accepted decision + REVIEW HISTORY|读取Phase A.1；下部旧Gate按已标historical保留|
|D1|CURRENT DOMAIN / TO BE UPDATED|账号经营和回执/数据/人工边界最小扩展；平台事实不静态冻结|
|D2|APPROVED CANDIDATE / PROVENANCE|其账号策略与体验理由供本轮消费；以后不默认并列Authority|
|D3|REVIEW / CEO decision applied evidence|保留已有身份裁决来源，不把STOP REVIEW登记文件升级Frozen|
|D4/D5|scoped RD domain / ACCEPTED HISTORY|对象/Holder语义继承；Main工位占满等已被S2限定的条款仅历史|
|W1|APPROVED CANDIDATE，部分产品语义已由S1/P1消费|复用而非重建；新增工具不要求Package体系改版|
|W2|PROVENANCE / 历史方法交接|旧Office、Package NOT IMPLEMENTED不作为Current入口要求|
|L1|CEO ACCEPTED APPROVED CANDIDATE|生命周期产品基础保留；运行候选细节不是全部Frozen implementation|
|I1|CURRENT IMPLEMENTATION ROUTER|不改；后续产品Delta不得自动改实现接受等级|
|N1/N3/E1/E2|PROVENANCE / RESEARCH|保留推导与反证；不作为未来普通UI默认必读|
|N2|PROVENANCE / UI-ready candidate input|接受部分经分层消费后才成为下游输入；原全稿不自动Approved|
|N4|PROPOSED shared/implementation合同来源|产品语义提取，G-V留技术验证；B结论不是Authority替代|
|N5/N6|DOMAIN候选/研究provenance|接受的Domain增量写入D1，不能保留两套Current CG|
|N7|REVIEW HISTORY / 研究边界来源|比例/成熟度/全量CEO调整等不消费；其人工边界证据保留|
|N8|PROVIDER IMPLEMENTATION CANDIDATE / RESEARCH|逐版本/平台证据；不进入全局必读，不“停掉所有自研”|
|N9|REVIEW HISTORY / PROVENANCE|全局反证理由留档，非第二Product Blueprint|

未来必要路由仍为P0→P1→适用Shared/Domain。新增Shared文件的确切命名与拆分**不是本轮默认要求**：优先在既有契约载体内增加明确章节，只有独立Owner/阅读负担证明必要才拆分。不得为六个G编号机械建六套系统或六份并行Authority。

## 16. Frozen Challenges / existing stale clauses

### 16.1 FROZEN AUTHORITY CHANGE PROPOSALS

|ID|Current Frozen / 旧理由|新证据/为何改|建议范围|下游影响|
|---|---|---|---|---|
|F1|S2§3.11 Human action only at Decision Gates；理由明确：不让CEO手点下一步|P1已有人工反馈；S6明确技术授权≠CEO Decision；N8手机确认/MFA、N7现场动作进一步检验该边界|将绝对句改为默认自治＋必要人工接续；保留P5≠P7，允许同Work等待与核验|P1原则、S1责任边界、S2 P4、Domain发布/交接、Map/UI状态；不直接改schema|
|F2|LocalDesktop+恢复合同，无退出UI持续运行的完整承诺；旧未选择服务模式的原因UNKNOWN|N1 C25静态检查/N4 G3：关UI与持续Work存在真实交付选择|接受opt-in用户级本地后台目标，明确设备不可运行时暂停与恢复核验|P1承诺、Shared生命周期/Settings、退出交互、实施G3-V；不影响七区|
|F3|P1§13/P2固定page-first推导顺序；理由是防Runtime主导导航|E1五工作链暴露页面清单不足，W1早已业务先行|澄清为经营证据先行＋现有结构约束，非以工具反推公司产品|仅产品方法注释/Map路由，不重建IA；本报告MERGE建议等待整包接受|
|F4|D1既有账号策略/Variant/Publication；不完整账号周期合同|N5/N6把账号长期目标计划反馈闭合|扩已有Channel Account Domain关系，维持Company资产/绑定/Workspace单cycle边界|D1与专业Map/UI输入；没有新execution scope|
|F5|S2§3.5 Provider适配、P1能力原则；具体测试/效果/备份合同不全|N4 G1/G2/G4/G6提供产品层可验证边界|补Shared能力/证据/恢复内容，技术实现下沉；不改变现有Slot或Owner|P1概述、Shared产品合同、Map字段、UI真状态；不能用文档代验收|

F3–F5为本轮有证据支持的推荐，并非还需重复研究的方向难题；CEO接受报告时一并确认才可改Frozen。F1由S6与P1已有决定支持，是窄幅治理修正而非新的产品方向；只有F2需明确选择，见§17。

### 16.2 旧文内部残留，不应误算“NEW胜出”

|位置|残留/歧义|已经存在的约束|建议治理动作（未执行）|
|---|---|---|---|
|P5§2 Department不要求第一天创建；§1/3旧办公室隐喻|可能抹掉原装两部或恢复Office产品身份|S4 Phase A.1、P4§5–8；D3身份裁决|限定按需的是其他组织扩展；Office仅provenance|
|P5§1.1 Conversation强制Identity/Assignment分离|可能要求每换scope新建Conversation|P4§21/23、S4 Phase A§5|历史隔离以消息/引用scope校验，不强制identity断开|
|P5§6 Conflict / P3消息Conflict / N2 C45|不同层的冲突被误当全局DataTrust enum|P1/P3 Unknown/需核实、S2证据语义|分别描述来源不一致/责任冲突/资源占用；不新增全局状态|
|D4§1.1 Main=Employee栈；P3旧研发片段|可能否定Professional Surface主视觉|S2当前§0.1、D4页首Shared supersession、P4|明确旧图是局部/历史实例，不能冻结整个Main|
|P3旧Batch1 Runtime gaps、旧Figma design baseline|旧checkpoint可能覆盖后续scope接受/视觉暂停|P3 Phase A修订、P4、I1 Current|标注适用日期，不重开旧Keychain等blocker|
|W2旧Office/Package未实现/固定研究步骤|方法交接被误作当前实现或固定模板流程|W1更新、S1/P1、I1|保留历史证据；非默认Current input|
|S2§3.11自动发布→Analytics / §3.12系统Analytics|可能被误读为所有平台已接通，或分析不得有员工|P4§27真实Analyst；P1能力真相|自动流程受能力/授权/数据实际状态；采集系统活动≠员工分析责任|

没有以词频宣称“所有stale已清除”：本轮只识别与仲裁有关的残留，Authority原文未改。

## 17. Remaining CEO Decisions

|Decision|Option A|Option B|证据与推荐|影响|
|---|---|---|---|---|
|F2 离开UI之后的运行承诺|接受opt-in用户级本地后台目标；睡眠/关机/登出不运行，显式停全体|维持App-bound执行；离开UI会中断，依恢复合同重开，后台只Future|推荐A：符合持续经营用途，但N4 G3-V未运行；A是产品目标而非实施授权|Settings/退出/恢复说明及未来本机服务验证；B也可闭环但用户必须保持App运行|

不再向CEO询问已由证据裁决的问题：Account不是Workspace；Provider不是Employee；七区不增；具体库不进Blueprint；不同目标/权限的fallback不能默许。若CEO要求Account新并发Runtime scope或云端24/7，那是超出本次推荐的新Delta，不在此强行兼容。

## 18. Current Implementation vs proposed target

|主题|Current可据本轮来源说什么|不能说什么|下一验证|
|---|---|---|---|
|Company/四层scope/Phase B|I1明确IMPLEMENTED / ACCEPTED CANDIDATE|四层自主经营全部Accepted|按I1原CEO Gate；本轮不重验|
|Cloud/模型发现/默认/重启|I1与其Accepted路线有真实DeepSeek纵向接受|所有Provider/所有模型能力/用途fallback已验|N4 G2-V|
|Browser/Web|N1记录已有局部工具/WebView；完整安全浏览闭环未证|研究工具成功=Curis Employee可用|N4 G1-V|
|后台|已有持久化/restart链；没有本报告新service验收|退出UI后本地服务已保证运行|N4 G3-V|
|Execution/外部恢复|既有Work/Router/Result恢复保留|远端效果未知恢复/所有Provider exactly-once已证|N4 G4-V|
|专业工具|已有RD受限代码/工具能力，Knowledge md/txt链Accepted|任意shell/Git写/PDFOCR/Media/数据处理全交付|N4 G5-V逐能力|
|备份恢复|N1/N4指出既有DB/manifest机制及未闭合边界|managed files+secret重连+安全恢复全通过|N4 G6-V|
|CG发布/分析|N7/N8记录Publishing/Analytics未连/不可用；AiToEarn部分候选|真实发布、收益、各平台全自动经营已验|授权后的逐平台执行/数据/恢复证据|
|知识/会议/洞察/Talent|I1接受其限定范围；会议自主讨论仍Candidate|因新研究就否定全部旧验收，或宣布所有未来能力完成|原范围验证保留，新能力单列|

本表不是新Completion Audit，不更新I1，也不读取真实个人配置；配置当前值UNVERIFIED。G1–G6并非一包实现许可，也不借本轮扩大Autonomous V1 Issue。

## 19. FINAL ADVERSARIAL RECONCILIATION PASS

已进行一轮完整反证，以下修正已进入矩阵/方案，不留待UI自行补。

|攻击|发现的失败|本轮修正|剩余证明边界|
|---|---|---|---|
|全部接受NEW|77设置/29面变管理员产品，能力词数量代替用户工作|R070/R107下沉；§13不把参数全暴露|实际设计密度未验证|
|全部保留OLD|安全Browser/模型用途/外部效果/后台/恢复仍靠设计猜|R025/R055/R097等补Shared，F1按已有Authority修正、F2显式Gate|G-V均未运行|
|所谓完整只是技术完备|lease、数据库schema、库选择不回答CEO经营问题|R100/R108技术下沉|不预建通用服务框架|
|旧简单靠脑补|“失败恢复/能力”标题没有说明外部已成功时怎么做|R046/R055快照与效果合同|未来fault injection|
|一个对象两个Owner|AccountCycle被当第五scope；ProviderFlow当CurisWork|R042/R083/R110限定Domain投影/引用|并发多账号控制设计另审|
|同能力两个Surface|Talent和Settings都配置模型；账号/Insights重复分析|R066/R067/R070/§12 canonical owner＋情境入口|导航实现未改|
|第二Work/Result/Employee/Usage|人工动作或Provider映射另建执行队列|R051/R110拒绝新系统|现有载体不足须精准Architecture Gate|
|Target写成Current|N4 B闭合、N7百分比被当可用证明|R109、§18区分研究/实现|不升级任何验收|
|Domain污染Core|Platform→Account挤掉Dept/Workspace；收入成全业务成功标准|R003–R008/R081–R082/R092拒绝|陌生业务仍需真实方法/人力|
|实现库污染语言|Browser=Playwright，Media=FFmpeg|R109下沉；产品只说能力|选型/许可仍技术Review|
|Conversation-first被过度解释|所有业务摘要只能聊天；反方向专业聊天挤右栏|R073–R076保Main工作与经营面并存|具体节奏/布局开放|
|所有Result归Business|新经营图漏Company/Department工作|R003/R047保四scope归属|不是所有scope自主经营已验|
|Account真相被私有化|按Workspace复制Company Account；跨账号绝不汇总|R082/R091/R095保资产/绑定/派生分析|跨scope写协调另验|
|安全过度变审批地狱|所有模型测试/研究/策略小改都CEOGate|R041/R046保Envelope与按需测试|高风险阈值按合法policy|
|未知业务只叫用户配工具|把探索缺口转交CEO填写77项|R008/R009/R037保研究/组装/必要人类事实；可拒绝|不承诺任意行业已会经营|

上述ID是定位辅助；具体结论以§4 Topic同名行及其来源为准。所有尺度判断均为产品压力推理，不是20业务并发实测。

### 19.1 跨业务反证：不是运行验收

|压力场景|如果只保留旧抽象会断在哪里|如果全部接受新细节会过度到哪里|本次保留的最小合法闭环 / 失败出口|
|---|---|---|---|
|内容账号：发布超时后收到迟到回执|可能FAILED后重复发布|为每个账号建独立Core Cycle和Provider员工|同Work记录动作目标与Evidence；先核验Publication，无法确认标效果未知；Provider回执不等于增长Result|
|研发：共享Employee在两个Business修不同仓库|“员工会开发”不能说明cwd、权限、dirty tree及预览|把Curis变IDE，所有用户必配Git/Terminal|Assignment绑定合法Scope、仓库与输入输出；Terminal/Git是按需能力；写入前权限和变更核验；最终Result经测试/Review|
|研究/写作：来源网页含恶意指令、PDF只解析部分|资料存在被误作已完整理解|要求每次阅读CEO审批所有技术参数|Reader/Parser提供来源、可读取范围与Partial；网页是数据不是授权；Employee给有证据的结论，不足则补研究或明确Unknown|
|数据分析：两账号费用口径不一致、一个没有外部收入|执行Usage被当成商业价值|统一伪健康分/强制补齐77设置|同口径才比较；Cost/Speed/Quality/外部Outcome分列；缺失不补零；Analyst承担解释，结论接原Decision|
|宠物寄养：需要现场接收动物，系统无实体执行者|抽象自治承诺可能假装现场工作完成|为了全能给Core增加宠物行业流程|先Research/Capability Discovery；有合法人类执行者则明确人工接续、证据与责任；无成立条件则Cannot operate yet，不把同意当完成|
|20个Business共享5个Employee，机器睡眠且触发积压|稳定Identity被误读成无限容量、永远在线|每业务克隆Employee或全量补发所有Work|一个Employee、多Assignment、Context隔离；资源有限可等待；恢复先核验与合并触发，不重放外部副作用；后台承诺由F2决定|

这些案例支持合同必要性与边界，不声称已实测未知行业、20业务容量或G1–G6。若未来实测推翻产品假设，须记录新Evidence再走Delta。

## 20. CEO的20个问题

1. **改变多少？** 110议题中61项KEEP/CLARIFY；其余多为合并细化/下沉。实质是六组合同增量，不是重做公司架构，计数不代表实现工作量。
2. **旧Blueprint早已正确的？** 公司层级、统一员工、责任、经营周期、Evidence/Learning、七区/Four-Pane、Package First、真实结果和Unknown。
3. **只是解释清楚的？** 能力装配价值、跨业务员工、Provider非员工、账号/渠道非Workspace、学习与外部业务价值。
4. **真正新增原则？** 完整浏览能力、效果未知恢复、备份重连；逐能力测试和审批快照补强；人工边界需治理修正，后台承诺需CEO。
5. **新明显优于旧的？** 真实失败条件：错账号、chat≠vision、远端已成功超时、缺指标假0、恢复后权限丢失。
6. **旧明显优于新的？** 已接受结构、统一对象Owner、渐进披露、Envelope自治；优于重型表单/账号新scope/全面CEO审批。
7. **拒绝哪些？** 新中心/统一钱包/静态成熟度百分比/全量设置/Provider当Employee/无条件retry/实现库进产品定义。
8. **North Star？** 让真实CEO组织AI员工持续经营真实业务、获得可核验结果并在授权边界内学习成长。
9. **Company/Department/Business/Workspace？** canonical长期层级不变；Business持续方向，Workspace实际环境；Company或Department员工工作不要求假Workspace。
10. **Employee/Responsibility/Assignment？** 一身份，多责任；Assignment绑定角色与合法scope，Holder与当前Executor分开。
11. **Capability/Agent/Provider？** Capability是工作能力；Agent/Provider供给执行或信息，不拥有公司员工身份和业务真相。
12. **Conversation/Work/Execution？** 持久讨论关系、工作责任载体、具体执行尝试分离；上下文引用贯通而非三套任务。
13. **Result/Evidence/BusinessResult/Learning？** 成品/事实依据/外部价值/经Review接受的经验；不能由内部完成一步跳学习成功。
14. **AI/User/Provider全局原则？** 推荐正式Shared化；人工参与不能合理代理部分，F1按已有ADR修改Frozen绝对句后才成立为一致Current。
15. **Browser/Model/Background层级？** Blueprint仅原则/能力承诺；Shared完整产品合同；UI按需入口；实现库与G-V下沉。
16. **CG正式新定义？** 本轮尚无新的Current；推荐扩已有Account长期经营合同、周期关系、逐账号定稿/回执/数据质量与接续。
17. **AiToEarn？** 部分平台Provider候选；不是Curis本体/唯一底座，未通过Curis真实执行集成验收。
18. **七区/Four-Pane？** 全部成立；不增一级区，完整工作Main、辅助Utility、浮动Assistant独立。
19. **什么进Blueprint/什么下沉？** 稳定身份关系/价值边界进核心；能力交互Shared；账号/发布Domain；字段布局UI输入；库/技术映射/验证Implementation。
20. **能更新唯一Blueprint吗？** **B：READY WITH CEO DECISIONS**；待F2以及本报告整包Review接受后，下一轮才Consolidation。现在不改。

## 21. Final verdict / handoff

Verdict: **B. READY WITH CEO DECISIONS**  
Disposition: PROPOSED RECONCILIATION — NO AUTHORITY CONSUMPTION YET  
Owner: CEO / Product Authority  
Next Action: 决定F2并接受F1治理修正、接受或修正本报告与Change Plan  
Target Authority: P1及必要Shared/Domain，P2/P3只消费  
Next Gate: CEO FINAL RECONCILIATION REVIEW → separately authorized PRODUCT TRUTH CONSOLIDATION

没有修改唯一Blueprint、Master Map、UI Blueprint、Shared/Domain/Frozen Authority或Pointer；不把本报告加入Current required route。没有UI、代码、运行、集成、提交或推送。

### Document-only verification

- 110个矩阵ID唯一；110项六维分析；77项Settings逐项分类；三个交付文件本地链接0 missing。
- Markdown代码围栏成对、空白检查通过；git diff --check通过。
- 对照开工快照，315个Context/Product/Design/Workspace Engineering文件hash未变；HEAD未变、staged为空。
- 工作树差异仅新增本轮三份Review交付，既有dirty文件保留。没有重新验证Runtime、平台、G1–G6或UI；这些不计为本轮PASS。

STOP FOR CEO FINAL RECONCILIATION REVIEW。
