# CURIS FULL PRODUCT EXPERIENCE MAP

Authority Class: RESEARCH
Status: Review
Disposition: CANDIDATE MAP — NOT AUTHORITY / NOT UI DESIGN
Date: 2026-09-15 Asia/Shanghai

读法：V编号对应同目录Expression V2的Surface；C编号对应完整18步推导。箭头表示入口、引用或工作连续性，**不表示所有关系都是父子Schema，也不表示图中的能力已经实现**。七导航保持；Settings、搜索、通知和CEO Assistant是全局辅助。所有新合同待CEO Review及Blueprint仲裁。

## 图1 — Curis Full Product Architecture

```mermaid
flowchart TB
    app[Curis Company OS] --> nav[Global Navigation 七区]
    app --> util[全局辅助能力]
    nav --> desk[V01 CEO工作台]
    nav --> business[V02 业务空间]
    nav --> org[V06 组织中心]
    nav --> talent[V18 人才与能力]
    nav --> insights[V21 经营洞察]
    nav --> library[V22 资料库]
    nav --> meeting[V19 会议]
    util --> setting[V12 Settings 六类]
    util --> quick[V24 搜索与最近对话]
    util --> attention[V24 Attention与通知]
    util --> assistant[V23 同一CEO Assistant浮层]
    business --> operating[V04 Business经营]
    operating --> workspace[V05 Workspace专业工作]
    workspace --> work[V08 Work与Conversation]
    desk --> work
    org --> employee[V07 Employee身份与能力]
    employee --> work
    meeting --> work
    assistant --> work
    work --> execution[既有Execution与工具活动]
    execution --> result[V10 Result与Evidence]
    result --> decision[V09 合法Decision与修改]
    decision --> work
    result --> insights
    result --> library
    setting --> capability[V13与V14 连接和能力验证]
    capability --> execution
    work --> recovery[V20 状态核验与恢复]
    recovery --> work
```

## 图2 — Employee Capability Architecture

```mermaid
flowchart TB
    identity[同一Employee身份] --> role[Role与Responsibilities]
    role --> assignment[Assignment与真实范围]
    identity --> purposes[按工作用途选择能力]
    purposes --> models[Model Profile与用途路由 C02至C08]
    purposes --> agent[External Agent C09]
    purposes --> skill[Skill与Plugin C10]
    purposes --> mcp[MCP工具 C11]
    purposes --> web[Search Reader Browser C12至C15]
    purposes --> computer[Computer操作 C16]
    purposes --> files[文件与工作环境 C17至C24]
    purposes --> knowledge[合法Knowledge与Reference C36]
    models --> connection[唯一Connection实例与Credential引用]
    agent --> connection
    mcp --> connection
    web --> connection
    connection --> verify[声明与实测分开]
    models --> verify
    computer --> os[本机OS许可与执行适配器]
    os --> verify
    files --> verify
    verify --> effective[本次Work有效能力交集]
    assignment --> effective
    policy[Company策略及Work动作授权 C29] --> effective
    context[输入兼容与数据外发边界 C07 C24] --> effective
    effective --> ready{可完成所需操作吗}
    ready -->|是| run[同一Work执行并记录实际能力]
    ready -->|否| gap[缺能力 缺权限 未验证 需登录分别显示]
    gap --> fix[精准设置入口 保留原Work]
    fix --> verify
```

## 图3 — Business Operating Experience

```mermaid
flowchart LR
    intent[CEO经营意图] --> reuse{复用还是新建}
    reuse --> existing[已有Business]
    reuse --> proposal[V03 目标与策略提案]
    proposal --> relation[合法Department Business 首Workspace]
    existing --> goal[Goal与成功标准]
    relation --> goal
    goal --> strategy[Strategy与约束]
    strategy --> team[Team与Responsibility]
    team --> resources[能力 账号 文件 数据 权限检查]
    resources --> cycle[Cycle计划与检查点]
    cycle --> work[Work与真实Execution]
    work --> effect[外部动作及回执核验]
    work --> fail[缺能力或失败]
    fail --> repair[修复或人工介入]
    repair --> work
    effect --> result[Result与Evidence]
    effect --> unknown[效果未知 禁止盲重试]
    unknown --> check[只读核验或人工证据]
    check --> result
    result --> analysis[Analysis与Review]
    analysis --> learning[有依据的Learning候选]
    learning --> next{下一经营决定}
    next -->|继续或调整| cycle
    next -->|等条件| wait[等待或排程]
    wait --> cycle
    next -->|需CEO| decision[原Decision与责任]
    decision --> strategy
```

经营链复用同一Work/Result/Decision；继续不是无条件创建新Cycle，已存在则打开原对象。Account是外部资源，Project/文件夹是工作资源，二者均不代替Workspace。

## 图4A — CEO工作台与全局辅助展开

```mermaid
flowchart LR
    nav[Global Navigation] --> desk[V01 CEO工作台]
    desk --> readiness[Section 公司身份与用途就绪]
    readiness --> missing[Object 缺能力的工作用途]
    missing --> setup[Action 配置工作能力]
    setup --> model[V13 连接 发现 Profile 测试]
    desk --> attention[Section 需你处理]
    attention --> decision[Object Decision或人工动作]
    decision --> process[Action 继续处理]
    process --> detail[V09 版本 目标 影响 证据]
    desk --> return[Section 上次离开后]
    return --> work[Object 未完Work]
    work --> check[Action 核验后恢复 V20]
    nav --> global[全局辅助 非第八区]
    global --> search[V24 搜索]
    search --> object[有权对象分组结果]
    object --> open[键盘打开与返回查询]
    global --> assistant[V23 Assistant]
    assistant --> context[引用当前页面 显式scope]
    context --> send[发送意图与打开原工作面]
    global --> notifications[V24 通知Drawer]
    notifications --> unread[已读与已解决分别处理]
    global --> settings[V12 Settings]
```

## 图4B — 业务空间展开

```mermaid
flowchart LR
    nav[业务空间] --> directory[V02 部门 业务 工作空间目录]
    directory --> create[开始一项业务 V03]
    create --> proposal[意图 目标 策略 责任 资源提案]
    proposal --> save[确认结构与缺口后创建]
    directory --> business[V04 Business]
    business --> definition[Definition 目标与规则]
    business --> status[Operating Status 重点与判断]
    business --> spaces[Workspace Directory]
    business --> team[Business Team 责任投影]
    definition --> amend[讨论或修订 版本与Decision]
    spaces --> workspace[V05 Workspace]
    workspace --> plan[本轮计划 输入 输出 Review 检查点]
    plan --> schedule[V20 安排时间与条件]
    workspace --> work[V08 Work与Conversation]
    workspace --> resources[V16 文件与数据资源]
    resources --> grant[选择目录 只读或输出授权]
    workspace --> tools[V17 Terminal Git Preview]
    tools --> test[运行 检查差异 打开真实页面]
    workspace --> results[V10 Result]
    results --> review[查看证据 接受或要求修改]
    workspace --> shutdown[V11 暂停归档与交接]
```

## 图4C — 组织与人才展开

```mermaid
flowchart LR
    org[组织中心] --> map[V06 公司版图]
    map --> hierarchy[Company Department Business Workspace]
    hierarchy --> operating[进入经营或查看责任]
    org --> directory[V06 员工目录]
    directory --> create[创建员工 姓名与职责]
    directory --> employee[V07 同一Employee]
    employee --> profile[资料与组织关系]
    employee --> responsibility[多范围责任]
    responsibility --> assign[安排Holder与交接影响]
    employee --> capabilities[用途能力与缺口]
    capabilities --> binding[V14 绑定与有效权限]
    binding --> route[固定或受限自动 默认与Fallback]
    binding --> verify[V13 连接与用途测试]
    employee --> record[工作 结果 学习记录]
    record --> work[V08 进入Main工作]
    talent[人才与能力] --> catalog[V18 外部候选]
    catalog --> inspect[来源 版本 许可 依赖]
    inspect --> recruit[招募为canonical Employee]
    inspect --> install[纳入公司能力资源]
    install --> binding
    recruit --> directory
```

## 图4D — 洞察、资料库与会议展开

```mermaid
flowchart LR
    insights[经营洞察] --> scope[V21 范围与周期]
    scope --> trust[Section 数据完整性与口径]
    trust --> metric[Object 指标与来源快照]
    metric --> analysis[Action 请分析师分析]
    analysis --> report[Report 事实 解释 未知 建议]
    report --> evidence[V10 核对依据与复核]
    library[资料库] --> browse[V22 类型 范围 搜索]
    browse --> source[Object 文件 来源 版本 UsedBy]
    source --> read[Action 阅读或引用到工作]
    read --> composer[V08 草稿引用预检]
    source --> refresh[核对时效与冲突 新修订]
    meeting[会议] --> list[V19 进行中与已结束]
    list --> create[Action 创建议题与参与者]
    create --> discussion[Section 讨论与分歧]
    discussion --> decision[V09 建议转合法决定]
    decision --> followup[Section 决定与跟进]
    followup --> work[Object 原责任Work与结果]
```

## 图4E — Settings六类到实际设置

```mermaid
flowchart LR
    settings[V12 Settings 全局辅助] --> personal[个人与外观]
    personal --> p[身份 语言 时区 主题 IME 通知 Quiet hours Digest]
    p --> paction[保存个人偏好 OS通知独立检查]
    settings --> company[公司设置]
    company --> c[资料 目标 预算 排程默认 退役影响]
    c --> caction[修订或Decision 不改独立业务策略]
    settings --> ai[模型与AI]
    ai --> a[Provider Model用途 Agent Skill MCP Web 媒体 数据工具]
    a --> aaction[连接 发现 测试 绑定 复验]
    settings --> security[权限与安全]
    security --> sec[文件 浏览账号 站点 OS 授权 外发 审批 信任边界]
    sec --> saction[授予最小范围 撤销并列受影响Work]
    settings --> data[应用与数据]
    data --> d[后台 网络Proxy 容量 备份恢复 版本保留 资源并发]
    d --> daction[检查实际进程 预检恢复包 核验后续做]
    settings --> help[账户与帮助]
    help --> h[App版本 更新 诊断与安全导出]
    h --> haction[预览诊断包 本地保存 不自动发送]
```

每个设置详见Expression V2内S001–S077，共77条14字段合同。某个Work的排程/素材规格属于对象内输入，Settings只提供继承规则及定位，不另存一份同名值。

## 图5 — 三条Browser工作链与返回

```mermaid
flowchart TB
    research[研究目标] --> search[Web Search]
    search --> reader[Page Reader或交互Browser]
    reader --> source[保存来源快照与时间]
    source --> evidence[Evidence与Result引用]
    dev[研发目标] --> process[启动受控Preview进程]
    process --> local[核验设备与localhost]
    local --> interact[真实点击 输入 DOM状态]
    interact --> debug[Console Network脱敏 Screenshot]
    debug --> change[修改并再测 同版本证据]
    external[外部经营目标] --> env[选择隔离账号环境]
    env --> identity{账号身份有效吗}
    identity -->|否| human[真人正常登录与MFA]
    human --> recheck[核对身份 交还员工]
    recheck --> permission[验证动作和版本授权]
    identity -->|是| permission
    permission --> action[执行并核验回执]
    action --> unknown[超时则效果未知 先查询]
    action --> result[原Work结果]
    debug --> result
    evidence --> result
    observer[查看现场是观察 接管是控制权转移] --> env
```

## 图6 — 模型就绪与运行状态

```mermaid
flowchart LR
    connection[安全连接配置] --> auth[认证检查]
    auth --> discovery[完整发现或手动未验证]
    discovery --> profile[Model Profile 声明 来源 硬限]
    profile --> test[按用途低风险测试]
    test --> partial[文本 工具 图片 音频等分别结果]
    partial --> route[Company与Employee用途路由]
    route --> preflight[Work输入 权限 预算 地域 资源预检]
    preflight --> running[实际选择并运行]
    preflight --> blocked[缺项精准恢复入口]
    running --> output[Result与Usage实际记录]
    running --> uncertain[中断或副作用未知]
    uncertain --> inspect[核验再续做 不盲Fallback]
    updated[模型或配置变化] --> stale[相应测试过期]
    stale --> test
```

## Gate

地图覆盖所有七导航及全局辅助、Employee能力架构、Business运行链、Browser和Model依赖。它是一份候选地图，不能作为Runtime能力存在的证明。G1–G6的产品合同和可交付边界须CEO Review后进入Blueprint Deep Reconciliation。结论仍为 **C. NOT READY — CAPABILITY GAPS REMAIN**；**STOP FOR CEO REVIEW**。
