# Curis V1 Final UI Surface Inventory

Status: Review  
Authority Class: REVIEW / EVIDENCE  
Date: 2026-09-09  
Owner: Main Development  
Disposition: CURRENT UI INVENTORY FOR CEO REVIEW; not final visual acceptance.  
Source: CEO CURRENT UI INVENTORY / GAP AUDIT instruction; current packaged UI; registered UI acceptance records; current source route inventory.  
Next Gate: CEO / ChatGPT Final UI Review. No implementation authorized by this report.

## 1. Counting and evidence boundary

**76 core Surface/state-family inventory entries** below: **53 observed in native screenshots, 22 source-only, 1 domain-family unverified**. These are not 76 different routes and not a claim that every possible state was rendered. Shared controls are counted once; an empty/loading/error family is one audit unit, explicitly expanded in §4. There are **42 physical `ceo-office/**/page.js` route definitions**, listed in §5; legacy/deep links are not silently called Current primary products.

**The exact total of all user-reachable state combinations remains UNVERIFIED.** The read-only instance cannot safely supply running, archived/restored, failure, empty-company, full historical Meeting, and professional-domain populated states. No synthetic state, cloud execution, archive/restore or error injection was performed to inflate coverage. This inventory is a counted lower-bound portfolio, not an exhaustive interaction certification.

Classification totals (including clearly marked provisional source-only dispositions):

| A FINAL-READY | B POLISH | C RECONCILE | D REDESIGN REQUIRED | E LEGACY / SUPERSEDED | F MISSING VISUAL |
|---:|---:|---:|---:|---:|---:|
|2|18|20|9|4|23|

A applies only to the captured state, not its entire module. C is based on registered accepted composition/pattern differences plus current screenshots, **not live pixel comparison with Figma**. F on source-only rows means no sufficiently registered final visual for that required state was found; it does not prove no Figma draft exists anywhere. B on source-only rows is a preservation recommendation, not visual PASS.

### Audit instance

- App: `/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app`.
- Binary SHA-256: `fe66764ff1ae6e2e62aa29ccd534be5ebb26ac82027373989baf7d24d160bd1d`.
- Existing fresh build from the preceding packaged acceptance; **no rebuild in this read-only audit**.
- External root: `/tmp/curis-ceo-native.ydOJRf`; SQLite: `/tmp/curis-ceo-native.ydOJRf/data/curis.sqlite`.
- Native window screenshots: 1228×768 raster; Light/system theme. This is not a 1440×900 pixel-equivalence certification.
- Workspace/gateway/frontend remain the isolated instance on 8002/8080/3010 (PIDs 2783/2790/2785 observed).
- 34 native screenshots, under `artifacts/ui-final-inventory/`.
- In-app Browser auxiliary attempt timed out; no Browser measurement or Browser PASS is claimed. Native audit continued.
- Figma was not opened or modified. Baseline coverage derives from named Frozen registration documents.
- UI navigation only: no form submission, no recruitment/import/decision/Work control, no secret inspection. Result viewing and automatic page recovery may use existing application seams in isolated state; **this is not a claim that isolated state is byte-identical**. The three protected DBs are checked separately.

## 2. Source and Figma key

Routes below are relative to `/ceo-office`; `*` means shared across areas. Source keys resolve to exact files below. Screenshot links identify the actual captured image; S = source-only, U = unverified runtime instance. Source references are for locating consumers, not authority.

All registered frame IDs refer to Figma file `2Fh7DgPPfLgdbvNtnzPnk9`.

- CEO: `CURIS_V1_CEO_DESK_OPERATING_UI_ACCEPTANCE.md`: 69:3. Expanded Decision/Evidence/Assistant and higher density explicitly outside that bounded frame.
- Organization: `CURIS_V1_ORGANIZATION_CENTER_UI_ACCEPTANCE.md`: 106:3 / 106:230 / 106:457. Employee Detail/Edit is not covered by those three frames.
- Insights: `CURIS_V1_OPERATING_INTELLIGENCE_UI_ACCEPTANCE.md`: 172:3 / 172:277 / 172:551 / 172:825.
- Knowledge: `CURIS_V1_KNOWLEDGE_LIBRARY_UI_ACCEPTANCE.md`: 187:2 / 187:276 / 187:550 / 187:824.
- Meeting: `CURIS_V1_MEETING_ROOM_UI_ACCEPTANCE.md`: 214:3 / 247:2 / 214:279 / 214:555 / 214:831.
- App Entry: `CURIS_V1_APP_ENTRY_UI_ACCEPTANCE.md`: 13 registered frames, not proof of dynamic model/credential state visual completeness.
- Business/Talent: current implementation and product contract found; no exact final per-state frame registration found in the consumed record. Direction D alone is not a final page.
- `CURIS_V1_CURRENT_UI_FOUNDATION.md` is **Review / Candidate foundation**, not another Frozen UI Blueprint.
- `CURIS_VISUAL_STANDARD_V1.md` is Frozen visual language, **not frozen page composition or final numerical typography tokens**.

- `shell`: [frontend/components/terra/TerraShell.js](</Users/yy/Documents/Curis AI Workspace/frontend/components/terra/TerraShell.js>)
- `nav`: [frontend/components/v1/V1Sidebar.js](</Users/yy/Documents/Curis AI Workspace/frontend/components/v1/V1Sidebar.js>)
- `quick`: [frontend/components/v1/ConversationQuickAccess.js](</Users/yy/Documents/Curis AI Workspace/frontend/components/v1/ConversationQuickAccess.js>)
- `conversation`: [frontend/components/v1/EmployeeConversation.js](</Users/yy/Documents/Curis AI Workspace/frontend/components/v1/EmployeeConversation.js>)
- `conversationPage`: [frontend/app/ceo-office/conversation/page.js](</Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/conversation/page.js>)
- `composer`: [frontend/components/v1/SharedConversation.js](</Users/yy/Documents/Curis AI Workspace/frontend/components/v1/SharedConversation.js>)
- `assistant`: [frontend/components/assistant/GlobalAssistant.js](</Users/yy/Documents/Curis AI Workspace/frontend/components/assistant/GlobalAssistant.js>)
- `model`: [frontend/app/ceo-office/capabilities/page.js](</Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/capabilities/page.js>)
- `states`: [frontend/components/runtime/RuntimeStates.js](</Users/yy/Documents/Curis AI Workspace/frontend/components/runtime/RuntimeStates.js>)
- `primitives`: [frontend/components/terra/TerraPrimitives.js](</Users/yy/Documents/Curis AI Workspace/frontend/components/terra/TerraPrimitives.js>)
- `ceo`: [frontend/app/ceo-office/page.js](</Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/page.js>)
- `result`: [frontend/components/v1/ResultReferenceView.js](</Users/yy/Documents/Curis AI Workspace/frontend/components/v1/ResultReferenceView.js>)
- `business`: [frontend/app/ceo-office/business/page.js](</Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/business/page.js>)
- `workspace`: [frontend/app/ceo-office/workspace/page.js](</Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/workspace/page.js>)
- `studio`: [frontend/app/ceo-office/workspace/studio/page.js](</Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/workspace/studio/page.js>)
- `general`: [frontend/components/v1/GeneralWorkspaceOperating.js](</Users/yy/Documents/Curis AI Workspace/frontend/components/v1/GeneralWorkspaceOperating.js>)
- `domain`: [frontend/components/runtime/WorkspaceRuntimeView.js](</Users/yy/Documents/Curis AI Workspace/frontend/components/runtime/WorkspaceRuntimeView.js>)
- `org`: [frontend/app/ceo-office/organization/OrganizationCenter.js](</Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/organization/OrganizationCenter.js>)
- `employee`: [frontend/app/ceo-office/organization/employees/[id]/page.js](</Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/organization/employees/[id]/page.js>)
- `employeeEdit`: [frontend/app/ceo-office/organization/employees/[id]/EmployeeEditDrawer.js](</Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/organization/employees/[id]/EmployeeEditDrawer.js>)
- `talent`: [frontend/app/ceo-office/talent-market/page.js](</Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/talent-market/page.js>)
- `insights`: [frontend/app/ceo-office/analytics/OperatingIntelligence.js](</Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/analytics/OperatingIntelligence.js>)
- `knowledge`: [frontend/app/ceo-office/knowledge/page.js](</Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/knowledge/page.js>)
- `knowledgeDetail`: [frontend/app/ceo-office/knowledge/entries/[id]/page.js](</Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/knowledge/entries/[id]/page.js>)
- `meeting`: [frontend/app/ceo-office/meeting/page.js](</Users/yy/Documents/Curis AI Workspace/frontend/app/ceo-office/meeting/page.js>)

## 3. Surface inventory

P0/P1/P2 are **Final UI priorities**, not newly reopened Runtime priorities. For E, retire the old user-facing composition; do not delete its canonical functionality.

| ID | Area | Surface / State | Route | Current Source | Existing Figma Baseline | Class | Severity | Evidence | Main Gap | Recommended Action |
|---|---|---|---|---|---|---|---|---|---|---|
|S01|Global|App Shell / Window / scrolling|`*`|`shell`|FIGMA DIRECTION ONLY|D|P0|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/business/06-cancelled.png>)|长页滚动带走一级导航；顶部齐与CEO身份显示不一致|保留七区IA，确定壳的滚动与身份呈现|
|S02|Global|Navigation / selected area|`*`|`nav`|FIGMA DIRECTION ONLY|B|P2|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/ceo/01-default-attention.png>)|选中可辨，图标与文本偏小|保留结构并校准密度|
|S03|Global|Recent Conversation / search|`*`|`quick`|FIGMA DIRECTION ONLY|B|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/global/02-conversation-reference.png>)|条目轻量，但标题与元信息过密、移除符号小|明确长标题与溢出行为|
|S04|Global|Persistent Employee Conversation|`/conversation?conversation_id=…`|`conversation`|FIGMA PARTIAL|D|P0|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/global/02-conversation-reference.png>)|正文像未分组日志，责任范围原生select夹在消息与Composer间|补最终对话工作面，不改持久化|
|S05|Global|New Conversation|`/conversation`|`conversationPage`|NO FIGMA (未找到登记)|F|P0|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/global/03-new-conversation.png>)|整页仅两行默认表单，无最终视觉层级|补最小新对话视觉|
|S06|Global|Shared Composer / disabled controls|`*`|`composer`|FIGMA PARTIAL|C|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/global/02-conversation-reference.png>)|同一基础组件在不同宿主中选择器、提示密度不同|统一基础与宿主扩展边界|
|S07|Global|Global Assistant floating panel|`*`|`assistant`|FIGMA PARTIAL|E|P0|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/global/01-assistant-drawer.png>)|旧嵌套卡和双入口叠在当前CEO面上|退役旧视觉投影，保留canonical快捷入口|
|S08|Global|Model Management / saved-unverified|`/capabilities`|`model`|FIGMA PARTIAL|C|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/global/04-model-saved-unverified.png>)|已连接与等待重新验证并列且缺说明；当前租户默认、SQLite外露|翻译状态层级，不改变验证事实|
|S09|Global|Shared loading|`*`|`states`|FIGMA PARTIAL|F|P1|S|源码骨架与对话单行loading两套；未录到稳定截图|补统一加载状态样板|
|S10|Global|Shared error / forbidden|`*`|`states`|FIGMA PARTIAL|F|P1|S|运行状态读取失败通用文案，页面inline alert另一路|统一用户可读错误与恢复，不制造故障|
|S11|Global|Reference / return|`/knowledge?pick_for=…`|`knowledge`|FIGMA FINAL/ACCEPTED BASELINE EXISTS · 187:824|C|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/knowledge/07-work-reference-picker.png>)|返回依附添加动作；未选条目时缺清楚的取消返回|补不写入的返回呈现|
|S12|Global|Modal / drawer system|`*`|`primitives`|FIGMA PARTIAL|C|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/knowledge/04-new-overlay.png>)|会议居中宽弹层与员工/资料窄抽屉尺寸、focus、footer不同|明确二者适用与共用控件|
|S13|CEO|Default / populated|`/`|`ceo`|FIGMA FINAL/ACCEPTED BASELINE EXISTS · 69:3|C|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/ceo/01-default-attention.png>)|主次虽分明但卡占比大、长工作原文直接当标题|按accepted层级适配真实长文|
|S14|CEO|Waiting Decision Attention|`/`|`ceo`|FIGMA FINAL/ACCEPTED BASELINE EXISTS · 69:3|B|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/ceo/01-default-attention.png>)|需决定入口可辨，事项名缺摘要层|保留source lifecycle，补摘要/长文规则|
|S15|CEO|Result Attention|`/`|`ceo`|FIGMA PARTIAL|C|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/ceo/01-default-attention.png>)|同一结果同时占持续关注和重要结果视觉位置|收敛视觉重复，不新建Attention truth|
|S16|CEO|Result opened / return|`/`|`result`|FIGMA PARTIAL|F|P1|S|本轮未打开未读CEO结果以免新增Viewed事实；展开态未实测|复用结果阅读标准，后续合法状态验收|
|S17|CEO|CEO Assistant inline Conversation|`/`|`composer`|FIGMA PARTIAL|C|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/ceo/01-default-attention.png>)|首屏Composer被推后，技术性模型说明抢占页头|保留对话，压低配置说明|
|S18|CEO|Empty / load / error / return|`/`|`ceo`|FIGMA PARTIAL|F|P1|S|无关注空态及故障未在本隔离数据安全重现|纳入关键状态Master，不沿用旧PASS|
|S19|Business|Business overview|`/business`|`business`|FIGMA DIRECTION ONLY|D|P0|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/business/01-overview.png>)|重复统计、重复业务名称、大卡层叠|保持四块合同，重建信息层级|
|S20|Business|Workspace directory within Business|`/business`|`business`|FIGMA DIRECTION ONLY|B|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/business/01-overview.png>)|目录关系清楚，但原始时间串与重复标题|统一目录行和时间格式|
|S21|Business|Standalone Workspace directory|`/workspace`|`workspace`|FIGMA DIRECTION ONLY|F|P1|S|源码卡网格并出现canonical Business说明，未原生打开|补目录最终视觉并实测|
|S22|Business|Studio / Workspace create|`/workspace/studio`|`studio`|FIGMA DIRECTION ONLY|F|P1|S|未进入创建流程；不能从功能验收推定最终视觉|纳入创建/回到业务的设计覆盖|
|S23|Business|General Workspace default / team|`/workspace?workspace_id=…`|`general`|FIGMA DIRECTION ONLY|D|P0|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/business/02-workspace-work-states.png>)|指标卡与大Composer主导，实际工作后置，右栏闲置|不变业务模型，重建工作优先层级|
|S24|Business|Work expanded / completed|`/workspace?workspace_id=…#work-…`|`general`|FIGMA DIRECTION ONLY|D|P0|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/business/03-paused-completed-dense.png>)|长文连排、按钮成排、状态竖向断行|建立可读Work/结果摘要与动作优先级|
|S25|Business|Work paused|`/workspace?workspace_id=…`|`general`|FIGMA DIRECTION ONLY|D|P0|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/business/03-paused-completed-dense.png>)|暂停徽章压窄，停止执行事实与大段结果难扫描|保留事实，调整密度和徽章约束|
|S26|Business|Work cancelled|`/workspace?workspace_id=…`|`general`|FIGMA DIRECTION ONLY|D|P0|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/business/06-cancelled.png>)|已停止换行、归档与结果重复入口拥挤|补终止态工作面|
|S27|Business|Work running / failure|`/workspace?workspace_id=…`|`general`|FIGMA PARTIAL|F|P1|S|当前无RUNNING；未启动云任务制造截图|后续用合法运行证据验收状态呈现|
|S28|Business|Work archived / restored|`/workspace?workspace_id=…`|`general`|FIGMA PARTIAL|F|P1|S|本轮不归档/恢复修改对象，历史功能证据不作视觉通过|补状态变化与恢复反馈|
|S29|Business|Result preview / focus|`/workspace?workspace_id=…`|`result`|FIGMA PARTIAL|D|P0|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/business/04-result-open.png>)|点击结果后可见区未转到上方结果面|明确结果打开的焦点/阅读位置|
|S30|Business|Result Evidence / technical detail|`/workspace?workspace_id=…`|`result`|FIGMA PARTIAL|D|P0|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/business/05-result-evidence-expanded.png>)|窄栏原始JSON，多层滚动，缺专业正文呈现|建立用户摘要→证据→技术元数据层级|
|S31|Business|Workspace Conversation / return|`/workspace?workspace_id=…`|`general`|FIGMA PARTIAL|C|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/business/02-workspace-work-states.png>)|员工入口和公司助理Composer视觉关系不够清楚|明确交流对象，不改变Employee执行归属|
|S32|Business|Workspace empty / invalid parent / error|`/workspace`|`workspace`|FIGMA PARTIAL|F|P1|S|源码仍有Parent Resolver/Domain等说明；异常未实机触发|补可恢复空态/归属异常视觉|
|S33|Business|RD / XHS / Shortvideo professional entry|`/workspace/software ; /workspace/xhs ; /workspace/shortvideo`|`domain`|FIGMA PARTIAL|F|P1|U|本隔离实例没有这些合法实例，不能继承旧验收当本轮UI证据|分别核对专属accepted基线，暂不裁决域UI|
|S34|Business|Cross-Workspace return|`/workspace?workspace_id=…`|`workspace`|FIGMA DIRECTION ONLY|B|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/business/06-cancelled.png>)|A/B标题和归属可区分；没有足够清楚的面内返回路径|统一当前业务/Workspace弱导航|
|S35|Organization|Company Map / partial staffing|`/organization`|`org`|FIGMA FINAL/ACCEPTED BASELINE EXISTS · 106:3|B|P2|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/organization/01-company-map.png>)|Department容器与Business-first成立，稀疏数据留白过大|保留构图，校准稀疏密度|
|S36|Organization|Business Focus|`/organization`|`org`|FIGMA FINAL/ACCEPTED BASELINE EXISTS · 106:230|B|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/organization/02-business-focus.png>)|结构可复用，岗位事实等元说明过多|保留Focus，替换工程解释|
|S37|Organization|Employee Directory|`/organization`|`org`|FIGMA FINAL/ACCEPTED BASELINE EXISTS · 106:457|B|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/organization/03-employee-directory.png>)|名字/角色过小，多责任范围语义易混|校准层级和多归属标注|
|S38|Organization|Employee Detail / cross-area entry|`/organization/employees/[id]`|`employee`|NO FIGMA (未找到登记)|E|P0|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/organization/04-employee-detail.png>)|关联项目、模板与能力框占主面，员工工作不居中|退役admin投影，沿用现有身份/详情能力|
|S39|Organization|Employee Edit drawer|`/organization/employees/[id]`|`employeeEdit`|NO FIGMA (未找到登记)|E|P0|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/organization/05-employee-edit.png>)|Capability Profile、tenant_private、model catalog直接暴露|替换普通用户编辑呈现，保留高级能力事实|
|S40|Organization|Empty / search / error|`/organization`|`org`|FIGMA PARTIAL|F|P1|S|没有完整空公司及错误截图，只有局部未设置状态|補空态/异常状态，不猜岗位|
|S41|Organization|Vacancy → Talent|`/organization`|`org`|FIGMA PARTIAL|F|P1|S|当前无真实vacancy，未点击招聘来源链|用有来源的合法空缺补最终视觉证明|
|S42|Talent|Experts catalog / detail|`/talent-market`|`talent`|FIGMA DIRECTION ONLY|B|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/talent/01-experts.png>)|三段浏览结构可用，英文模板与字母头像偏工程库|保留结构，中文职责与资源层级收敛|
|S43|Talent|Recruitment overlay|`/talent-market`|`talent`|FIGMA DIRECTION ONLY|C|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/talent/02-recruitment-avatar-overlay.png>)|薄select与大input不同密度，CTA/说明分散|套用最终表单标准|
|S44|Talent|Employee Avatar chooser|`/talent-market`|`talent`|FIGMA PARTIAL|B|P2|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/talent/02-recruitment-avatar-overlay.png>)|上传/8预设/跳过已有，尺寸和选中需微调|保留当前资产，不重新生成|
|S45|Talent|Company Employees|`/talent-market`|`talent`|FIGMA DIRECTION ONLY|F|P1|S|本轮未捕获该Tab，不能用目录截图替代|确认与canonical目录的轻量差异|
|S46|Talent|Skills catalog / unavailable|`/talent-market`|`talent`|FIGMA DIRECTION ONLY|C|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/talent/03-skills.png>)|英文分类、同名条目难区分、状态颜色强度不统一|收敛目录行与不可用解释|
|S47|Talent|Installed Skills entry|`/talent-market`|`talent`|FIGMA DIRECTION ONLY|C|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/talent/05-installed-link-shows-catalog.png>)|点已安装0项仍看到完整目录；路径预期不明|明确筛选/回退提示，不新建库|
|S48|Talent|Skill binding|`/talent-market`|`talent`|FIGMA DIRECTION ONLY|F|P1|S|没有安装状态，未做绑定写入|补已安装/未绑定/绑定反馈视觉|
|S49|Talent|Connectors unavailable|`/talent-market`|`talent`|FIGMA DIRECTION ONLY|E|P0|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/talent/04-connectors-unavailable.png>)|代码项目名、Create/Publish规划与patchright面向普通用户|退役开发目录文案，保留未连接边界|
|S50|Talent|Empty / loading / failure / return|`/talent-market`|`talent`|FIGMA PARTIAL|F|P1|S|未主动注入网络错误或提交招聘|补失败保留输入与返回状态样板|
|S51|Insights|Overview / Unknown metrics|`/analytics`|`insights`|FIGMA FINAL/ACCEPTED BASELINE EXISTS · 172:3|C|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/insights/01-overview-unknown.png>)|结论优先但大卡/多层tonal/指标重复、私有圆角|按accepted层级压缩视觉容器|
|S52|Insights|Scoped analysis|`/analytics`|`insights`|FIGMA FINAL/ACCEPTED BASELINE EXISTS · 172:277|B|P1|S|有已登记基线与源码，但本轮未展开实机|保留基线，单独做scope稀疏态核对|
|S53|Insights|Explore / Benchmark|`/analytics`|`insights`|FIGMA FINAL/ACCEPTED BASELINE EXISTS · 172:551|B|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/insights/02-explore-benchmark.png>)|未知值诚实；零样本下大指标框占空间|保留口径，补稀疏数据密度|
|S54|Insights|Reports empty|`/analytics`|`insights`|FIGMA PARTIAL|C|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/insights/03-reports-empty.png>)|空态直接解释分析Artifact和示例，像验收说明|改成资料来源与下一步的产品空态|
|S55|Insights|Report detail / Decision continuity|`/analytics`|`insights`|FIGMA FINAL/ACCEPTED BASELINE EXISTS · 172:825|B|P1|S|当前无真实报告，不能拿空态替代详情验收|单独验证报告/P7引用读层|
|S56|Insights|Data Trust / metric evidence|`/analytics`|`insights`|FIGMA PARTIAL|B|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/insights/01-overview-unknown.png>)|未知值保留正确；证据专业展开未捕获|保留UNKNOWN，补证据层呈现|
|S57|Insights|Loading / error|`/analytics`|`insights`|FIGMA PARTIAL|F|P1|S|未安全触发错误；源码模式需与Shared统一|补无数据与故障区分|
|S58|Knowledge|Overview|`/knowledge`|`knowledge`|FIGMA FINAL/ACCEPTED BASELINE EXISTS · 187:2|C|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/knowledge/01-overview.png>)|低密度状态大卡空白；计数占据高层级|回到Reading-first|
|S59|Knowledge|Browse / search / scope|`/knowledge?view=browse`|`knowledge`|FIGMA FINAL/ACCEPTED BASELINE EXISTS · 187:276|C|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/knowledge/02-browse.png>)|筛选容器与一条资料各成大卡，选择器过薄|对齐Reference Rows与控件标准|
|S60|Knowledge|Search empty|`/knowledge?view=browse`|`knowledge`|FIGMA PARTIAL|C|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/knowledge/06-search-empty.png>)|大空态卡且展示不会用示例资料等工程保证|用简短无结果解释|
|S61|Knowledge|Reading / source / Used By empty|`/knowledge/entries/[id]`|`knowledgeDetail`|FIGMA FINAL/ACCEPTED BASELINE EXISTS · 187:550|C|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/knowledge/03-reading-detail.png>)|摘要与正文重复，正文卡强制大白区，侧栏多卡|正文优先，控制摘要重复|
|S62|Knowledge|Work reference picker|`/knowledge?pick_for=…`|`knowledge`|FIGMA FINAL/ACCEPTED BASELINE EXISTS · 187:824|C|P0|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/knowledge/07-work-reference-picker.png>)|复用整页统计/大筛选；无选择不能直接返回|恢复compact picker与独立取消返回|
|S63|Knowledge|New Knowledge drawer|`/knowledge`|`knowledge`|FIGMA PARTIAL|F|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/knowledge/04-new-overlay.png>)|Memory术语外露，缺最终表单/底部动作规范|补标准新建抽屉|
|S64|Knowledge|Import unavailable drawer|`/knowledge`|`knowledge`|FIGMA PARTIAL|F|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/knowledge/05-import-unavailable.png>)|资料根/相对路径无来源时仅禁用按钮，缺可理解恢复路|保留支持格式，设计未配置表达|
|S65|Knowledge|Load More / loading / error|`/knowledge`|`knowledge`|FIGMA PARTIAL|F|P1|S|只有1条资料，无加载更多；不伪造分页或失败|后续真实密度与错误验收|
|S66|Knowledge|Source stale / unavailable / archived|`/knowledge/entries/[id]`|`knowledgeDetail`|FIGMA PARTIAL|F|P1|S|现有资料可用，未改数据制造过期/归档|补状态视觉，不新增来源能力|
|S67|Knowledge|Result / Work reference and return|`/knowledge/entries/[id]`|`knowledgeDetail`|FIGMA FINAL/ACCEPTED BASELINE EXISTS · 187:550|B|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/knowledge/03-reading-detail.png>)|返回浏览可用；Used By非空未证明|保留返回，补非空引用密度|
|S68|Meeting|Overview / active list|`/meeting`|`meeting`|FIGMA FINAL/ACCEPTED BASELINE EXISTS · 214:3|A|P2|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/meeting/01-overview.png>)|当前单条列表层级克制，未见明显发布级漂移|可直接纳入Master，保留多行密度复核|
|S69|Meeting|History empty|`/meeting`|`meeting`|FIGMA PARTIAL|B|P2|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/meeting/01-overview.png>)|空态简洁可用；历史非空未观察|保留，不伪造历史|
|S70|Meeting|Start Meeting overlay|`/meeting`|`meeting`|FIGMA FINAL/ACCEPTED BASELINE EXISTS · 247:2|A|P2|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/meeting/02-start-overlay.png>)|议题/背景/参与/主次操作清楚|可复用当前结构|
|S71|Meeting|Participant picker|`/meeting`|`meeting`|FIGMA FINAL/ACCEPTED BASELINE EXISTS · 247:2|B|P2|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/meeting/02-start-overlay.png>)|真实两人选择可辨；多参与者密度未测|保留，补溢出规则|
|S72|Meeting|Active Conversation / waiting|`/meeting?meeting=…`|`meeting`|FIGMA FINAL/ACCEPTED BASELINE EXISTS · 214:279|C|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/meeting/03-decision-conversation.png>)|决策包把讨论与Composer推下屏；当前只有稀疏测试记录|对齐多人讨论层级，不重开Runtime|
|S73|Meeting|Proposal / P7 Decision moment|`/meeting?meeting=…`|`meeting`|FIGMA FINAL/ACCEPTED BASELINE EXISTS · 214:555|C|P1|[Native](</Users/yy/Documents/Curis AI Workspace/artifacts/ui-final-inventory/meeting/03-decision-conversation.png>)|可选方案清楚但长包与对话分割，来源标签密|保留provenance，补紧凑层级|
|S74|Meeting|Work / Result return|`/meeting?meeting=…`|`meeting`|FIGMA FINAL/ACCEPTED BASELINE EXISTS · 214:831|B|P1|S|本会议尚未形成Work，非空最终读层未验证|使用后续真实结果核对，不造工作|
|S75|Meeting|Evidence request / blocked|`/meeting?meeting=…`|`meeting`|FIGMA PARTIAL|F|P1|S|当前只有WAITING_CEO，无补证据状态|补状态视觉，不发云请求|
|S76|Meeting|History detail / loading / error / return|`/meeting`|`meeting`|FIGMA PARTIAL|F|P1|S|当前无历史详情/故障截图；返回总览已操作|补未覆盖状态，不复跑会议|

### Screenshot interpretation notes

- `business/04-result-open.png` deliberately records the **unchanged visible Work region after clicking Result**. AX exposed the result higher on the page; it is not a screenshot of the result body. The actual expanded body/JSON is `business/05-result-evidence-expanded.png`.
- `talent/05-installed-link-shows-catalog.png` is the catalog visible after selecting “已安装技能 0 项”, **not a false installed-empty screenshot**.
- Meeting content explicitly labels itself pre-existing navigation test content. It proves layout only; not autonomous or cloud proposal quality.
- Employee/Business names and long test prompts are isolated sample content. Findings concern handling of legitimate long text, not asking to ship those names.
- Current protected-DB safety does not turn previous functional UI registrations into final visual acceptance.

## 4. Required state coverage reconciliation

| Area | Native-observed states | Present in source / not safely observed | Not claimed |
|---|---|---|---|
|Global|selected navigation; recent conversation; new-conversation form; populated chat; disabled send/voice; assistant panel; model saved/unverified; result technical expansion|loading/error/forbidden; empty recent subset; overflow with many conversations; removal reappearance; result-unavailable|No complete search/keyboard/console certification; no new conversation or send|
|CEO|default; Decision Attention; Result Attention; Assistant inline; entry/return via navigation|empty company/no attention; result attention disposition during this audit; full Decision/Result return; load/error|No new Viewed receipt proof or Attention acceptance rerun|
|Business|Business overview/directory; A/B workspace; completed; paused; cancelled; holder without executor; result focus failure; technical evidence; cross-workspace navigation|RUNNING; FAILED; archived; restored; empty; invalid-parent; Studio; professional domains|No executing/pausing/cancelling/archiving/restoring or synthetic E2E|
|Organization|Map; Focus; Directory; partial staffing; Employee detail; edit drawer; cross-area entry|empty company/directory; true vacancy; search no-result; load/error; many assignments|No staffing mutation or fake risk/vacancy|
|Talent|Experts; recruitment/avatars open; Skills unavailable; installed entry; Connectors unavailable|company employee Tab; populated skill binding; upload error; successful recruitment; loading/error/return after save|No install/bind/recruit/upload|
|Insights|overview; Unknown; benchmark; report empty; visible trust summary|scoped detail; metric evidence overlay; populated report/Decision; load/error|No fake analytics/report/zero-cost inference|
|Knowledge|overview; browse; search no-result; read; source; unused-by state; new/import unavailable drawer; Work picker; return to browse|Load More; error; stale/unavailable/archived source; Used By nonempty; submitted picker return|No import/save/archive/reference write|
|Meeting|overview; current waiting meeting; history empty; start overlay; participant choices; existing proposal/P7 options; work/result empty; return to overview|autonomous running; evidence-request; nonempty Work/Result return; historical detail; stopped/closed; loading/error|No new meeting/cloud discussion/Decision|

Transient loading labels were observed in native AX during navigation; no stable loading screenshot was captured. They remain source/AX evidence, not visual acceptance.

## 5. Full route-definition boundary ledger

All 42 current source route definitions were enumerated. A source route existing is not proof it is linked in seven-area navigation, nor permission to migrate it into the Final Master. Current main navigation directly targets CEO, Business, Organization, Talent, Analytics, Knowledge, Meeting; conversation/model are utilities.

- `/ceo-office/analytics` → `frontend/app/ceo-office/analytics/page.js`
- `/ceo-office/brainstorm` → `frontend/app/ceo-office/brainstorm/page.js`
- `/ceo-office/brainstorm/sessions/[id]` → `frontend/app/ceo-office/brainstorm/sessions/[id]/page.js`
- `/ceo-office/business` → `frontend/app/ceo-office/business/page.js`
- `/ceo-office/calendar` → `frontend/app/ceo-office/calendar/page.js`
- `/ceo-office/capabilities/[type]/[id]` → `frontend/app/ceo-office/capabilities/[type]/[id]/page.js`
- `/ceo-office/capabilities` → `frontend/app/ceo-office/capabilities/page.js`
- `/ceo-office/company-runtime` → `frontend/app/ceo-office/company-runtime/page.js`
- `/ceo-office/conversation` → `frontend/app/ceo-office/conversation/page.js`
- `/ceo-office/decisions` → `frontend/app/ceo-office/decisions/page.js`
- `/ceo-office/execution` → `frontend/app/ceo-office/execution/page.js`
- `/ceo-office/execution/pipeline/[taskId]` → `frontend/app/ceo-office/execution/pipeline/[taskId]/page.js`
- `/ceo-office/execution/pipeline` → `frontend/app/ceo-office/execution/pipeline/page.js`
- `/ceo-office/execution/runs/[id]` → `frontend/app/ceo-office/execution/runs/[id]/page.js`
- `/ceo-office/execution/tasks/[id]` → `frontend/app/ceo-office/execution/tasks/[id]/page.js`
- `/ceo-office/finance` → `frontend/app/ceo-office/finance/page.js`
- `/ceo-office/help` → `frontend/app/ceo-office/help/page.js`
- `/ceo-office/knowledge/entries/[id]` → `frontend/app/ceo-office/knowledge/entries/[id]/page.js`
- `/ceo-office/knowledge/memory` → `frontend/app/ceo-office/knowledge/memory/page.js`
- `/ceo-office/knowledge` → `frontend/app/ceo-office/knowledge/page.js`
- `/ceo-office/meeting` → `frontend/app/ceo-office/meeting/page.js`
- `/ceo-office/organization/departments/[id]` → `frontend/app/ceo-office/organization/departments/[id]/page.js`
- `/ceo-office/organization/employees/[id]` → `frontend/app/ceo-office/organization/employees/[id]/page.js`
- `/ceo-office/organization/employees` → `frontend/app/ceo-office/organization/employees/page.js`
- `/ceo-office/organization` → `frontend/app/ceo-office/organization/page.js`
- `/ceo-office` → `frontend/app/ceo-office/page.js`
- `/ceo-office/projects/[id]` → `frontend/app/ceo-office/projects/[id]/page.js`
- `/ceo-office/projects` → `frontend/app/ceo-office/projects/page.js`
- `/ceo-office/reports/[id]` → `frontend/app/ceo-office/reports/[id]/page.js`
- `/ceo-office/reports` → `frontend/app/ceo-office/reports/page.js`
- `/ceo-office/runtime-trace` → `frontend/app/ceo-office/runtime-trace/page.js`
- `/ceo-office/settings` → `frontend/app/ceo-office/settings/page.js`
- `/ceo-office/strategy-room` → `frontend/app/ceo-office/strategy-room/page.js`
- `/ceo-office/talent-market` → `frontend/app/ceo-office/talent-market/page.js`
- `/ceo-office/workspace/department/[id]` → `frontend/app/ceo-office/workspace/department/[id]/page.js`
- `/ceo-office/workspace/department` → `frontend/app/ceo-office/workspace/department/page.js`
- `/ceo-office/workspace/installed/[workspaceId]` → `frontend/app/ceo-office/workspace/installed/[workspaceId]/page.js`
- `/ceo-office/workspace` → `frontend/app/ceo-office/workspace/page.js`
- `/ceo-office/workspace/shortvideo` → `frontend/app/ceo-office/workspace/shortvideo/page.js`
- `/ceo-office/workspace/software` → `frontend/app/ceo-office/workspace/software/page.js`
- `/ceo-office/workspace/studio` → `frontend/app/ceo-office/workspace/studio/page.js`
- `/ceo-office/workspace/xhs` → `frontend/app/ceo-office/workspace/xhs/page.js`

### Legacy and deep-link risks not silently counted as final products

- Source `/reports` contains `SAMPLE_REPORTS`; `/decisions` has a local placeholder handler; `/projects` describes Project-as-Business. These are **legacy route risks**, not proof the Current canonical reports/Decision/Business surfaces behave that way.
- `/finance`, `/calendar`, `/workspace/department` explicitly show “规划中/v1暂不建设” source placeholders. Do not add them as new V1 products to fill a design board.
- `/strategy-room`, `/brainstorm`, `/company-runtime`, `/runtime-trace`, `/execution/**`, `/settings`, department detail and memory routes require incoming-link review before retire/redirect. This read-only audit does not delete or certify their presentation.
- `analytics/page.js` retains old source, but its actual exported page returns `OperatingIntelligence`; old source comments are **not current rendered UI evidence**.
- RD/XHS routes consume dedicated components, while Shortvideo consumes `WorkspaceRuntimeView`. No legitimate populated professional instance existed in the inspected root. Keep their historical approved design separate; final-current native coverage remains U.
- Onboarding/App Entry is outside the signed-in seven-area route count. It has 13 registered Figma baseline frames; this audit did not reset Company state to reopen it.

## 6. Ownership / preservation

This is an audit portfolio, not a replacement Pointer, Page Map or Product Blueprint. Integration Owner: Main Development. Final visual decisions: CEO / design owner. Existing domain owners retain Runtime and professional UI scope.

No source/CSS/Runtime/schema edits; no tests added or run; no Figma actions; no staging/commit/push/release. Only the two requested documents and screenshot directory are output. Cross-state gaps remain visible in the inventory rather than being relabeled PASS.

See [Final UI Gap Review](</Users/yy/Documents/Curis AI Workspace/docs/reviews/CURIS_V1_FINAL_UI_GAP_REVIEW.md>) for top ten, component/typography evidence, proposed Master frame list and DB fingerprints.


## 7. Core Product Authority Audit — appended 2026-09-09

Status: Review. Authority Class: REVIEW / EVIDENCE. Source: CEO Core Product Truth Audit; [Authority reconciliation](CURIS_CORE_PRODUCT_AUTHORITY_RECONCILIATION.md). Original 76 rows and original visual scores are preserved. This is a separate dimension, not a replacement Product Authority.

**21 AUTHORITY DRIFT / 36 VISUAL GAP ONLY AT THIS ROW / 19 UNVERIFIED.** Shared root causes are not 21 independent bugs. Visual-only means no additional row-specific authority violation established; it does not certify inherited global Shell compliance. Source-only findings are not new native evidence. Unverified is never converted into PASS.

|Surface ID|Second dimension|Evidence interpretation|
|---|---|---|
|S01|AUTHORITY DRIFT|D04/D07：Shared Shell职责与身份/导航分叉|
|S02|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S03|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S04|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S05|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S06|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S07|AUTHORITY DRIFT|D05：floating能力应保留；宿主缺拖动与连续聊天，不是退役能力|
|S08|AUTHORITY DRIFT|D14：内部SQLite/租户状态语言进入默认模型面|
|S09|UNVERIFIED|原行缺完整状态证据；不推定违反或符合，保留后续验收。|
|S10|UNVERIFIED|原行缺完整状态证据；不推定违反或符合，保留后续验收。|
|S11|AUTHORITY DRIFT|D13：Reference返回/取消路径不完整|
|S12|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S13|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S14|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S15|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S16|UNVERIFIED|原行缺完整状态证据；不推定违反或符合，保留后续验收。|
|S17|AUTHORITY DRIFT|D05：Desk内对话正确，但不能替代跨区floating对话|
|S18|UNVERIFIED|原行缺完整状态证据；不推定违反或符合，保留后续验收。|
|S19|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S20|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S21|AUTHORITY DRIFT|D03/D08：目录进入旧Studio；Department工作入口未闭合|
|S22|AUTHORITY DRIFT|D03：源码提交拼接Business ref，后端要求canonical父关系|
|S23|AUTHORITY DRIFT|D04：固定readiness/team/result aside不等于按需Utility|
|S24|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S25|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S26|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S27|UNVERIFIED|原行缺完整状态证据；不推定违反或符合，保留后续验收。|
|S28|UNVERIFIED|原行缺完整状态证据；不推定违反或符合，保留后续验收。|
|S29|AUTHORITY DRIFT|D10：Result打开焦点/专业阅读职责未正确消费|
|S30|AUTHORITY DRIFT|D10：技术JSON主导专业证据投影|
|S31|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S32|AUTHORITY DRIFT|D14：Parent Resolver/Domain内部说明泄漏；错误态未重新触发|
|S33|AUTHORITY DRIFT|D07/D12：source确认六区shared nav；域内容本轮仍未native复验|
|S34|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S35|AUTHORITY DRIFT|D01：真实projection保留，但缺默认支撑部门不是稀疏视觉而已|
|S36|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S37|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S38|AUTHORITY DRIFT|D10：Employee admin面不等于conversation-first工作面|
|S39|AUTHORITY DRIFT|D10/D14：内部Capability/tenant配置主导|
|S40|UNVERIFIED|原行缺完整状态证据；不推定违反或符合，保留后续验收。|
|S41|UNVERIFIED|原行缺完整状态证据；不推定违反或符合，保留后续验收。|
|S42|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S43|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S44|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S45|UNVERIFIED|原行缺完整状态证据；不推定违反或符合，保留后续验收。|
|S46|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S47|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S48|UNVERIFIED|原行缺完整状态证据；不推定违反或符合，保留后续验收。|
|S49|AUTHORITY DRIFT|D14：技术connector目录不是普通用户能力发现投影|
|S50|UNVERIFIED|原行缺完整状态证据；不推定违反或符合，保留后续验收。|
|S51|AUTHORITY DRIFT|D09：分析师role文本匹配不证明组织责任；不指控指标造假|
|S52|UNVERIFIED|原行缺完整状态证据；不推定违反或符合，保留后续验收。|
|S53|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S54|AUTHORITY DRIFT|D14：Artifact技术说明主导空态；报告生成不外推|
|S55|UNVERIFIED|原行缺完整状态证据；不推定违反或符合，保留后续验收。|
|S56|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S57|UNVERIFIED|原行缺完整状态证据；不推定违反或符合，保留后续验收。|
|S58|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S59|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S60|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S61|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S62|AUTHORITY DRIFT|D13：compact reference picker/独立返回缺口|
|S63|AUTHORITY DRIFT|D13：Memory术语进入资料产品主流程|
|S64|AUTHORITY DRIFT|D13：文件根/相对路径成为导入的用户心智|
|S65|UNVERIFIED|原行缺完整状态证据；不推定违反或符合，保留后续验收。|
|S66|UNVERIFIED|原行缺完整状态证据；不推定违反或符合，保留后续验收。|
|S67|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S68|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S69|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S70|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S71|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S72|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S73|VISUAL GAP ONLY AT THIS ROW|保留原行视觉/密度/状态覆盖说明；未证明本项独立产品模型错误。|
|S74|UNVERIFIED|原行缺完整状态证据；不推定违反或符合，保留后续验收。|
|S75|UNVERIFIED|原行缺完整状态证据；不推定违反或符合，保留后续验收。|
|S76|UNVERIFIED|原行缺完整状态证据；不推定违反或符合，保留后续验收。|

S07原E只可指旧宿主投影，不得指floating Assistant产品能力应删除。S23右栏空白不能授权删除Pane。S19四块canonical Business表面合法，其视觉大卡不等于Business identity丢失。S68/S70 A仍仅限捕获状态，不代表全局Shell/Product已通过。Final UI Master Batch 1 remains PAUSED pending Authority Repair.

