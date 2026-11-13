# Curis Core Product Deviation Register

Status: Review
Authority Class: REVIEW / EVIDENCE
Date: 2026-09-09
Owner: Main Development
Disposition: CEO REVIEW REQUIRED / NO IMPLEMENTATION
Source: `CURIS_CORE_PRODUCT_TRUTH_LEDGER.md` + current source and earlier same-day native inventory.
Next Gate: existing Product Authority reconciliation, not new UI design.

P0=核心产品/组织/空间契约违反；P1=已有模型未正确投影或接线；P2=不改核心心智的细节。不同surface共用root cause，不累加成多个独立系统故障。Unknown/未覆盖不自动算已发现故障。

|ID|Domain|Accepted Truth|Current Reality|Deviation Type|Severity|Root Cause|Fix Layer|Release Impact|
|---|---|---|---|---|---|---|---|---|
|D01|Company bootstrap|每个新Company有空间工程部/数据分析部，用户Business可空|`foundation.py:293–385`只创建Company/Assistant；FirstRun另外创建业务部门；当前隔离库仅两业务部|BOOTSTRAP / ORGANIZATION / RUNTIME|P0|支撑部门要求未进入物化路径，关系fixture验收未覆盖freshCompany组织|既有bootstrap+canonical departments，Owner Main / Product|阻塞完整Company产品验收；不授权补活动库|
|D02|Workspace Engineering|默认工程部门真实Leader/研究/经营/设计/搭建/Quality承接，交付OperatingTeam|有Package substrate，无被审默认工程组织/责任链；Studio不能替代|ORGANIZATION / PRODUCT|P0|技术包生命周期验收未覆盖组织主体/业务移交|Shared已有Assignment/Work及产品入口；不得新建引擎|阻塞完整空间工程产品承诺，不否定Package验收|
|D03|Business creation seam|新Workspace必须引用现存canonical Business|Business/Workspace链接Studio，Studio发送`business-${type}`；Runtime查canonical表拒绝无效ref|PRODUCT / LEGACY / PROJECTION|P0|旧create UI继续作为Current入口，父关系迁移未贯穿调用端|Frontend integration，保留backend fail-closed|正常新增专业Workspace路径不能被称已闭环|
|D04|Shared spatial shell|四职责+可收起context/utility、统一header/T1–T3|TerraShell缺统一Adaptive seams；General固定readiness/team/result aside；专业Pane另一路|SPATIAL / PROJECTION|P0|逐页壳与专业壳并存，未做合同交集复验|Shared Shell boundary，非Runtime重构|阻塞Final UI；不是要求4列常驻|
|D05|CEO Assistant|全局floating可拖动/收起，同Conversation不必回Desk|GlobalAssistant fixed corner，无drag；只有简报/链接CEO Desk聊天|PRODUCT / SPATIAL|P0|Legacy host disposition被混读成全局产品形态退役|现有globalhost+同Assistant holder|核心全局交互缺口；不建第二Assistant|
|D06|Current registration|局部实现PASS与完整Product compliance分开|多个Current载体2026-09-08写PRODUCT COMPLETE/no blocking P1，未列D01–05|DOCUMENTATION|P0|验收覆盖范围扩大成全产品结论|Product/Implementation治理Owner；仅提修正|阻止沿旧完成结论直接发布|
|D07|Navigation|七区共享、Global Object Search、avatar settings|WorkspacePaneShell为六区并叫人才市场；V1Sidebar七区但search disabled；TerraShell静态齐|PROJECTION / UI|P1|重复导航数据/身份投影未统一|Shared navigation/identity consumer|需核心跨域一致性验收；localsearch不是globalsearch|
|D08|Operating Directory / leadership|Department/Business/Workspace直接工作入口，Leader持续经营|Current Business四块可读，但Department Work Surface规划态、完整领导入口未交付|PRODUCT / PROJECTION|P1|Business读目录替代了完整OperatingDirectory覆盖|现有领导assignment和work surface|功能版图未闭合；不重建Business|
|D09|Analyst responsibility|CompanyAnalyst属于数据分析部，scope由Assignment证明|`operating_intelligence.py:144`匹配role中分析/经营取第一员工，无责任/部门校验|ORGANIZATION / PROJECTION|P1|真实employee存在性被用于推定专业归属|现有analyst read projection / assignment|作者责任不能依名字；指标本身不因此为假|
|D10|Employee / Result|Main conversation-first，Utility专业详情/证据，L4技术按需|Employee Detail/admin编辑暴露Project/Capability；General结果固定aside且rawJSON显著|SPATIAL / PROJECTION / UI|P1|独立admin详情未消费sharedworkstation/detail层级|现有Frontend projection|保留identity/result事实；需层级/return修正|
|D11|Legacy escape|诊断/历史不作为CEO默认经营路径|RD→execution/tasks→execution→pipeline；Project→旧decision；reports含sample|LEGACY|P1|保留历史入口但未封闭跨路径用户返回|明确compat/deep-link adapter，不盲删|可把用户带回旧产品心智；不得称所有旧href当前可见|
|D12|Professional identity|Channel≠Workspace；Generic不吞Professional；Package声明专业面|XHS/TTK旧入口保留历史空间命名；尚无Current完整CG native覆盖|PRODUCT / DOCUMENTATION|P1|域实现验收早于专业产品identity reconciliation|Domain owner迁移边界，Shared保持|不能把旧XHS验收当完整ContentGrowth通过|
|D13|Knowledge reference|阅读/引用/返回，不让用户先理解文件根/Memory|Memory/relativepath copy；Work picker复用整页，无清楚独立取消返回|PROJECTION / UI|P1|后台操作投影和sharedpicker未完成用户层适配|现有Knowledge UI，非RAG新系统|影响引用主路径；保留数据与引用验收|
|D14|Capability user language|专家/技能/连接器职责和可用性优先|模型页SQLite/租户说明；catalog技术项目名、CapabilityProfile外露|PROJECTION / UI|P1|catalog内部元数据直接上主面|用户语言/渐进详情|真实性保留；不得加假功能掩盖缺能力|
|D15|Authority consistency|唯一Current规则，明确旧例/候选/实现证明范围|Generic终态措辞、account例、Assignment-history、modal例、旧待实现段共存|DOCUMENTATION|P1|追加reconciliation未清楚限定所有旧段适用范围|Product Owner窄范围裁决，不另建Blueprint|Phase A Gate，不能由前端自行决定|
|D16|Visual adaptation|Direction D、可读密度、稀缺card与清晰操作|真实数据长文/稀疏状态、窄徽章、重复统计/卡片、表单密度不一致|UI|P2|有限frame样本未覆盖完整真实数据密度|FinalMaster后适配|不能以此单独断言Runtime缺失；Dark/1024按既有后续边界|

## Count and release interpretation

16 entries: P0 **6**, P1 **9**, P2 **1**. D01/D02是同一支撑组织缺口的bootstrap/经营承接两面；D04/D07是共享壳/导航两面，不能相加为独立Runtime故障数。当前Product release BLOCKED不意味着所有P2变P0。

## Unresolved details, not invented defects

- 两支撑部门的固定Workspace、人数、删除/隐藏/改名政策：未找唯一已接受细节，不写假缺陷。
- Reading/Working/Operating完整逐对象容器矩阵与数值：现有原则支持，缺完整唯一映射，不用Research数字代替。
- Assistant snap/position memory/快捷键等：本轮CEO明确最低行为，其余未恢复不补设计。
- 全部其它worktree/历史code作者/交接丢失原因：本轮未取证，不猜Root Cause归人。
- 当前专业域完整native状态：旧accepted chain保持，本轮没有合法populatedRD/XHS再验收，不据截图空缺说功能不存在。

## No-rewrite boundary

Keep canonical Business/Workspace resolver、Shared identity/provenance、Team/Routing/Autonomy、Conversation/Usage、ResultViewed/Attention、Knowledge、Meeting core、General lifecycle、Package finite lifecycle/migration。修正必须复用它们；本register不授权实施、测试写入、Figma或Current文档改写。

STOP FOR CEO / CHATGPT CORE PRODUCT REVIEW.
