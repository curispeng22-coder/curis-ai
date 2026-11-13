/* ============================================================
   Curis Full Product HTML Design Prototype — DESIGN FIXTURE
   全部数据为 DESIGN FIXTURE，不是 Product Truth、不接 Runtime。
   语义消费：Structure Baseline（Frozen）+ PROFESSIONAL_BUSINESS_EXISTING_TRUTH.md
   （Content Growth / RD 命名与团队取 D 代原型 fixture：AI 科技 / Curis 研发；
     新业务激活 fixture：宠物寄养；员工姓名均为 DESIGN FIXTURE）
   ============================================================ */
window.FX = (function () {
  const org = {
    company: '知行创意（fixture 公司）',
    departments: [
      { id: 'dept-space', name: '空间工程部', leader: 'e-shen', desc: 'Curis 原装部门：把 CEO 的经营意图变成可运行的 Business 与 Workspace（可委托，非唯一入口）', businesses: [], builtin: true },
      { id: 'dept-cg', name: '内容增长部', leader: 'e-zhouning', desc: '一组内容类业务的最小管理单位', businesses: ['biz-cg'] },
      { id: 'dept-rd', name: '研发部', leader: 'e-lin', desc: '统一对外的版本节奏、研发质量与工程资源调配', businesses: ['biz-rd'] },
      { id: 'dept-data', name: '数据分析部', leader: 'e-siheng', desc: '公司级经营分析与 Decision support（Curis 原装部门）', businesses: [] },
    ],
  };

  const employees = [
    /* —— 空间工程部（原装 6 人，Structure Baseline §3.2；姓名 DESIGN FIXTURE）—— */
    { id:'e-shen',  name:'沈砚', role:'空间工程负责人', dept:'空间工程部', av:1, status:'working', statusDesc:'承接宠物寄养业务激活', duty:'把 CEO 意图转译为 Business / Workspace / 团队责任', leader:true,
      responsibility:{ longTerm:'承接 CEO 经营意图，复用或提议 Business，组建团队并交付可运行 Workspace', current:'为「宠物寄养」新业务完成激活建议与首个 Workspace', scope:'空间工程部' },
      capability:['Workspace Engineering','经营方法','团队组建'], skills:['sk-method','sk-doc'], model:'GLM-5.3', workload:76 },
    { id:'e-gu',    name:'顾行', role:'行业研究专家', dept:'空间工程部', av:2, status:'working', statusDesc:'宠物寄养行业研究', duty:'行业事实、竞品与受众研究，产出可引用证据', leader:false,
      responsibility:{ longTerm:'为新业务提供行业研究支持', current:'宠物寄养市场与定价研究', scope:'空间工程部' },
      capability:['行业研究','竞品分析','受众分层'], skills:['sk-research','sk-report'], model:'DeepSeek-V4.1', workload:52 },
    { id:'e-cem',   name:'策明', role:'经营方法专家', dept:'空间工程部', av:3, status:'idle', statusDesc:'', duty:'把经营目标翻译为目标→策略→可执行责任', leader:false,
      responsibility:{ longTerm:'为每个 Business 校准经营方法与目标拆解', current:'待分配', scope:'空间工程部' },
      capability:['目标拆解','策略边界'], skills:['sk-method'], model:'GLM-5.3', workload:12 },
    { id:'e-suge',  name:'苏格', role:'空间设计专家', dept:'空间工程部', av:4, status:'working', statusDesc:'设计宠物寄养 Workspace 结构', duty:'设计 Workspace 的 Surface / 对象 / 流程结构', leader:false,
      responsibility:{ longTerm:'设计专业 Workspace 结构与共享模式', current:'设计「宠物寄养」首个 Workspace', scope:'空间工程部' },
      capability:['Workspace 设计','信息架构'], skills:['sk-doc'], model:'GLM-5.3', workload:58 },
    { id:'e-liang', name:'梁筑', role:'搭建实施专家', dept:'空间工程部', av:5, status:'idle', statusDesc:'', duty:'把 Workspace 设计落地为可运行环境', leader:false,
      responsibility:{ longTerm:'实施 Workspace 与工具接线', current:'待设计完成', scope:'空间工程部' },
      capability:['实施','接线'], skills:['sk-web'], model:'DeepSeek-V4.1', workload:15 },
    { id:'e-chen',  name:'程验', role:'质量验证专家', dept:'空间工程部', av:6, status:'idle', statusDesc:'', duty:'验证 Workspace / Work 结果是否符合验收口径', leader:false,
      responsibility:{ longTerm:'质量验证与验收口径维护', current:'待分配', scope:'空间工程部' },
      capability:['验收','测试'], skills:['sk-check'], model:'DeepSeek-V4.1', workload:10 },
    /* —— 内容增长部（D 代 fixture：周宁/陈真/苏晴/何川/林月）—— */
    { id:'e-zhouning', name:'周宁', role:'内容增长部部长', dept:'内容增长部', av:2, status:'working', statusDesc:'跨平台节奏复盘', duty:'跨平台节奏统一、公私域联动', leader:true,
      responsibility:{ longTerm:'内容增长部经营节奏与公私域联动', current:'十月跨平台节奏规划', scope:'内容增长部' },
      capability:['内容策略','平台节奏'], skills:['sk-data','sk-report'], model:'GLM-5.3', workload:70 },
    { id:'e-zhen',  name:'陈真', role:'资深运营', dept:'内容增长部', av:3, status:'working', statusDesc:'统筹 AI 科技内容节奏', duty:'统筹内容增长工作空间目标、内容节奏、团队结果与下一轮经营', leader:true,
      responsibility:{ longTerm:'对内容增长 Business 的经营结果负责（多渠道账号分发）', current:'8 月种草节奏复盘 + 选题 vs 转化归因', scope:'内容增长 / 内容增长工作空间' },
      capability:['内容策略','运营统筹'], skills:['sk-xhs','sk-report'], model:'GLM-5.3', workload:88 },
    { id:'e-linan', name:'林月', role:'调研 / 文案', dept:'内容增长部', av:1, status:'working', statusDesc:'AI 工具实测数据收集', duty:'AI 工具实测数据收集；测评稿文案起草', leader:false,
      responsibility:{ longTerm:'调研与文案两工位：实测数据收集 + 测评稿起草', current:'《AI 工具测评》文案撰写中', scope:'AI 科技' },
      capability:['调研','文案'], skills:['sk-doc','sk-research'], model:'DeepSeek-V4.1', workload:82 },
    { id:'e-suqing',name:'苏晴', role:'视觉', dept:'内容增长部', av:4, status:'idle', statusDesc:'', duty:'封面风格与视觉规范', leader:false,
      responsibility:{ longTerm:'封面 + 排版视觉', current:'待《AI 工具测评》文案完成后出封面', scope:'AI 科技' },
      capability:['封面设计','排版'], skills:['sk-xhs'], model:'DeepSeek-V4.1', workload:24 },
    { id:'e-hechuan',name:'何川', role:'数据分析', dept:'内容增长部', av:5, status:'working', statusDesc:'选题归因分析', duty:'数据分析、选题归因', leader:false,
      responsibility:{ longTerm:'发布数据回收与选题归因', current:'上周内容互动归因（进行中）', scope:'AI 科技' },
      capability:['数据分析','归因'], skills:['sk-data'], model:'DeepSeek-V4.1', workload:55 },
    /* —— 研发部（D 代 fixture：林涛/王琳/周岚/赵敏/孙浩）—— */
    { id:'e-lin',   name:'林涛', role:'研发部部长 / Tech Lead', dept:'研发部', av:1, status:'working', statusDesc:'登录模块 v1.4 发布检查', duty:'对研发 Business 的交付质量与版本节奏负责', leader:true,
      responsibility:{ longTerm:'研发交付、架构决策与版本节奏', current:'登录模块 v1.4 发布检查准备', scope:'研发部 / Curis 产品研发' },
      capability:['架构','全栈'], skills:['sk-code','sk-check'], model:'GLM-5.3', workload:85 },
    { id:'e-sunhao',name:'孙浩', role:'Workspace 负责人', dept:'研发部', av:7, status:'working', statusDesc:'联调收口与发布门禁', duty:'统筹版本节奏、联调收口与发布质量', leader:true,
      responsibility:{ longTerm:'Curis 研发工作空间的联调收口与发布门禁', current:'登录模块 v1.4 发布门禁检查', scope:'Curis 研发' },
      capability:['发布门禁','联调'], skills:['sk-check'], model:'GLM-5.3', workload:66 },
    { id:'e-wanglin',name:'王琳', role:'产品经理', dept:'研发部', av:4, status:'idle', statusDesc:'', duty:'需求澄清与验收标准', leader:false,
      responsibility:{ longTerm:'需求澄清与验收标准维护', current:'待分配', scope:'Curis 产品研发' },
      capability:['需求','验收标准'], skills:['sk-doc'], model:'DeepSeek-V4.1', workload:18 },
    { id:'e-zlan',  name:'周岚', role:'开发工程师', dept:'研发部', av:5, status:'working', statusDesc:'登录接口联调', duty:'登录接口联调与异常分支修复', leader:false,
      responsibility:{ longTerm:'服务端接口实现与联调', current:'登录模块 v1.4 接口联调（进行中）', scope:'Curis 研发' },
      capability:['服务端','联调'], skills:['sk-code'], model:'DeepSeek-V4.1', workload:90 },
    { id:'e-zhao',  name:'赵敏', role:'QA', dept:'研发部', av:6, status:'blocked', statusDesc:'等待联调完成后回归', duty:'测试验证与质量证据', leader:false,
      responsibility:{ longTerm:'回归测试与质量证据', current:'登录模块回归测试（被联调阻塞）', scope:'Curis 研发' },
      capability:['测试','用例'], skills:['sk-check'], model:'DeepSeek-V4.1', workload:35 },
    /* —— 数据分析部（原装：司衡）—— */
    { id:'e-siheng',name:'司衡', role:'公司经营分析师', dept:'数据分析部', av:7, status:'working', statusDesc:'九月第二周经营周报', duty:'公司级经营分析、报告与 Decision support', leader:true,
      responsibility:{ longTerm:'跨 Business 经营分析、Data Trust、报告与 Decision support', current:'九月第二周经营周报（进行中）', scope:'数据分析部（工作位：经营洞察）' },
      capability:['经营分析','归因','报告'], skills:['sk-data','sk-report'], model:'GLM-5.3', workload:40 },
  ];
  const emp = id => employees.find(e => e.id === id);

  const businesses = {
    'biz-cg': { id:'biz-cg', name:'内容增长', dept:'内容增长部', leader:'e-zhen', stage:'运行中', desc:'内容获客持续经营：统一工作空间内复用内容，按 Channel Account 分发发布',
      workspaces:['ws-cg'], brief:'本周：验证 AI 工具实测内容的关注转化；《AI 工具测评》复用至三个渠道账号。' },
    'biz-rd': { id:'biz-rd', name:'Curis 产品研发', dept:'研发部', leader:'e-lin', stage:'运行中', desc:'Curis 桌面产品的迭代交付',
      workspaces:['ws-rd'], brief:'本周：登录模块 v1.4 联调中；回归测试被联调阻塞。' },
    'biz-pet': { id:'biz-pet', name:'宠物寄养（激活中）', dept:'空间工程部', leader:'e-shen', stage:'激活中', desc:'CEO 新经营意图 → 空间工程部承接激活中',
      workspaces:['ws-pet'], brief:'意图已捕获：研究（顾行）与 Workspace 设计（苏格）进行中，激活建议稍后提交。', activating:true },
  };
  const biz = id => businesses[id];

  const workspaces = {
    'ws-cg': { id:'ws-cg', name:'内容增长工作空间', business:'biz-cg', type:'professional', domain:'内容增长（多渠道）', leader:'e-zhen',
      channels:[{n:'小红书 · AI 科技',st:'已连接',est:true},{n:'抖音 · 知行创意',st:'需授权',est:false},{n:'公众号 · 知行创意',st:'未连接',est:false}],
      surfaces:[
        { id:'overview', name:'经营总览', desc:'当前经营五要素 + CEO Operating Result 投影' },
        { id:'research', name:'研究与洞察', desc:'趋势、竞品、受众、证据' },
        { id:'content', name:'内容运营', desc:'选题、制作、排期、发布（列表 / 日历）' },
        { id:'growth', name:'增长与评估', desc:'数据回收、转化验证、归因' },
        { id:'feedback', name:'反馈', desc:'评论与私信信号回流' },
        { id:'commercial', name:'商业化', desc:'线索与转化承接（Optional）' },
      ],
      flow:['选题','调研','文案','视觉','发布'],
      team:['e-zhen','e-linan','e-suqing','e-hechuan'] },
    'ws-rd': { id:'ws-rd', name:'Curis 研发', business:'biz-rd', type:'professional', domain:'产品研发', leader:'e-sunhao',
      surfaces:[
        { id:'overview', name:'交付总览', desc:'当前研发状态、Blocker、最近 Result' },
        { id:'dev', name:'开发', desc:'模块开发与联调' },
        { id:'review', name:'评审', desc:'代码与方案评审' },
        { id:'test', name:'测试验证', desc:'用例、执行与质量证据' },
        { id:'release', name:'发布', desc:'版本与发布门禁' },
      ],
      flow:['产品','架构','开发','测试'],
      team:['e-sunhao','e-lin','e-wanglin','e-zlan','e-zhao'] },
    'ws-pet': { id:'ws-pet', name:'宠物寄养工作空间', business:'biz-pet', type:'generic', domain:'本地生活服务（筹备）', leader:'e-shen',
      surfaces:[ { id:'overview', name:'经营总览', desc:'业务刚创建 · 激活进度' }, { id:'work', name:'工作区', desc:'团队工作与协作' } ],
      flow:[], team:['e-shen','e-gu','e-suge'] },
  };
  const ws = id => workspaces[id];

  /* Work / Agent Progress fixtures（plan 步骤措辞消费各域 Authority 的流程语言） */
  const works = [
    { id:'w-research', title:'AI 工具选题机会研究', employee:'e-linan', ws:'ws-cg', surface:'research', status:'working', elapsed:'18 分钟', cost:'◇ 4.2',
      plan:[{t:'收集近 7 天相关笔记评论样本 + 搜索词热度（信号）',done:true},{t:'对比 5 个对标账号近 30 天内容结构',done:true},{t:'输出 3 个可执行选题与理由（Intent 候选）',done:false,current:true},{t:'交接至 内容运营：排期制作',done:false}],
      current:'正在对比「教程 + 工具清单」组合的互动率数据', tools:[{n:'检索对标笔记',d:'抓取 5 个对标账号 30 天内 120 篇笔记标题与评论'},{n:'评论抽样分析',d:'对 1,842 条评论做主题聚类'}],
      handoff:'交接至 内容运营：生成 3 个实测选题（默认下一 Responsibility，非强制 DAG）', result:null, collaboration:['e-zhen'] },
    { id:'w-tuwen', title:'《AI 工具测评 · 极简风》图文制作（复用至 3 个渠道账号）', employee:'e-linan', ws:'ws-cg', surface:'content', status:'needs_ceo', statusLabel:'需要 CEO', elapsed:'42 分钟', cost:'◇ 7.8',
      plan:[{t:'实测数据收集（调研）',done:true},{t:'测评稿文案（文案工位）',done:false,current:true},{t:'视觉：封面与排版（苏晴）',done:false},{t:'发布（Channel Account：AI 科技主账号）',done:false}],
      current:'定位调整建议在你的 Approved Strategy Envelope 内，但涉及第三观察窗口的证据门槛', tools:[],
      decision:{ id:'d-xhs', title:'定位调整：本篇按「教程向」还是「测评向」发布', body:'李然研究与何川归因都指向「教程 + 工具清单」组合互动更优（EST）；但连续三篇测评向更利于人设积累。此调整在 Leader 职权边缘，按规则升级给你。', options:['采纳建议：本篇教程向','保持测评向','看完整归因数据'] },
      result:null },
    { id:'w-login', title:'登录模块重构 v1.4', employee:'e-zlan', holder:'e-sunhao', ws:'ws-rd', surface:'dev', status:'working', elapsed:'1 小时 12 分', cost:'◇ 12.6',
      plan:[{t:'产品 / 需求确认（王琳）',done:true},{t:'架构确认（林涛）',done:true},{t:'Runtime 实现',done:true},{t:'Frontend Adapter 与接口联调',done:false,current:true},{t:'交接至 测试：回归测试与质量证据',done:false},{t:'Review / 发布门禁（孙浩）',done:false}],
      current:'正在联调登录接口错误码与前端提示映射（异常分支修复）', tools:[{n:'编辑 auth.service.ts',d:'修改 validatePassword() 增加错误码 4012（declared-file change）'},{n:'运行单测',d:'auth 模块 22 passed / 0 failed'},{n:'启动本地预览',d:'登录页 Preview 已就绪'}],
      handoff:'交接至 测试验证（赵敏）→ Review / 发布门禁（孙浩）', result:'r-login', collaboration:['e-lin','e-sunhao'] },
    { id:'w-test', title:'登录模块回归测试', employee:'e-zhao', holder:'e-sunhao', ws:'ws-rd', surface:'test', status:'blocked', elapsed:'—', cost:'◇ 0.4', reviewReq:'e-zlan', reviewReqNote:'周岚已发起 Review Request（代码评审）——评审≠交接，交接仍以 Handoff 为准。' ,
      plan:[{t:'准备回归用例（12 条）',done:true},{t:'等待联调完成',done:false,current:true},{t:'执行测试并留证据（Test Evidence）',done:false}],
      current:'被阻塞：等待 登录模块重构 v1.4 联调完成（waiting ≠ idle）', tools:[], blockedBy:'w-login' },
    { id:'w-weekly', title:'九月第二周经营周报', employee:'e-siheng', ws:null, surface:null, status:'done', elapsed:'26 分钟', cost:'◇ 3.1',
      plan:[{t:'聚合各 Business 本周数据（唯一 Usage Ledger 口径）',done:true},{t:'同口径对比上周',done:true},{t:'输出报告与建议（附证据）',done:true}],
      current:'已完成', result:'r-weekly' },
    { id:'w-pet', title:'宠物寄养市场与定价研究', employee:'e-gu', ws:'ws-pet', surface:'overview', status:'working', elapsed:'32 分钟', cost:'◇ 5.5',
      plan:[{t:'行业事实：本地生活服务宠物寄养供给与定价带',done:true},{t:'竞品：3 个平台型竞品的服务结构',done:false,current:true},{t:'受众：养宠人群分层与付费意愿（EST）',done:false},{t:'输出行业研究简报（可引用证据）',done:false}],
      current:'正在对比 3 个平台型竞品的服务结构', tools:[{n:'检索行业报告',d:'收集 2 份行业报告与本地生活平台公开数据'},{n:'竞品服务结构整理',d:'结构化 3 家竞品的 SKU 与价格'}],
      handoff:'交接至 空间设计（苏格）：作为 Workspace 设计输入', result:null },
  ];
  const work = id => works.find(w => w.id === id);

  const results = [
    { id:'r-research', title:'选题研究简报 · AI 工具机会', employee:'e-linan', ws:'ws-cg', type:'doc', status:'done',
      evidence:['近 7 天 120 篇笔记评论抽样 + 搜索词热度','5 个对标账号 30 天内容结构分析'], usedBy:['《AI 工具测评》选题 Intent'] },
    { id:'r-tuwen', title:'《AI 工具测评 · 极简风》图文 v0.9', employee:'e-linan', ws:'ws-cg', type:'doc', status:'review',
      evidence:['引用：选题研究简报','平台规则检查（sk-xhs）'], usedBy:['待发布（发布回执只能来自 Connector）'] },
    { id:'r-login', title:'登录模块重构 v1.3 联调通过', employee:'e-zlan', ws:'ws-rd', type:'code', status:'done',
      evidence:['auth 模块单测 22 passed / 0 failed','Diff +34 / -93（declared-file change）','登录页本地预览冒烟通过'], usedBy:['v1.4 回归基线'] },
    { id:'r-weekly', title:'九月第二周经营周报', employee:'e-siheng', ws:null, type:'doc', status:'done',
      evidence:['各 Business 7 天经营数据（唯一 Usage Ledger 口径）','上周同期对比'], usedBy:['CEO 周会'] },
    { id:'r-pet', title:'宠物寄养行业研究简报（草稿）', employee:'e-gu', ws:'ws-pet', type:'doc', status:'review',
      evidence:['2 份行业报告','3 家竞品 SKU 结构'], usedBy:['Workspace 设计输入'] },
  ];
  const result = id => results.find(r => r.id === id);

  const decisions = [
    { id:'d-xhs', title:'定位调整：本篇按「教程向」还是「测评向」发布', from:'e-linan', ws:'ws-cg', urgency:'today',
      body:'研究（李然/林月）与归因（何川）指向教程向互动更优（EST）；连续测评向利于人设积累。Leader 职权边缘，按规则升级给你。', options:['采纳建议：教程向（推荐）','保持测评向','看完整归因数据'] },
    { id:'d-release', title:'灰度发布：登录模块 v1.4 首批 5% 用户', from:'e-sunhao', ws:'ws-rd', urgency:'today',
      body:'发生了什么：v1.4 联调进行中（Adapter 80%）、回归被联调阻塞。为何升级：生产发布不可逆（高风险），且前置条件（回归全绿）未满足。员工推荐：孙浩的灰度方案（5% · 观察 24 小时错误率）已就绪。本层（Layer 0）只能 查看方案 / 暂缓；批准入口在回归全绿后的 Decision Layer 1。', options:['查看发布方案','暂缓'] },
    { id:'d-connector', title:'授权小红书开放平台连接器', from:'e-hechuan', ws:'ws-cg', urgency:'thisweek',
      body:'授权后可自动回收互动数据（当前手工填报，EST 标注）；建议只读授权。发布回执必须来自 Connector。', options:['只读授权（推荐）','暂不授权'] },
  ];

  const meetings = [
    { id:'m-1', title:'周五复盘：AI 科技内容转化', status:'scheduled', when:'今天 16:00', participants:['e-zhen','e-linan','e-suqing','e-hechuan'],
      agenda:['定位调整证据门槛','下周排期','归因结论确认'], related:['w-tuwen','d-xhs'] },
    { id:'m-2', title:'登录模块 v1.4 发布检查', status:'done', when:'昨天', participants:['e-lin','e-sunhao','e-zlan','e-zhao'],
      agenda:['联调结果','回归范围','发布窗口'], related:['w-login'], outcome:'决议：联调完成后进入回归；灰度方案提交 CEO；发布窗口周五。' },
  ];

  const knowledge = [
    { id:'k-1', title:'小红书平台规则合集（9 月版）', type:'doc', scope:'公司级', updated:'9/10', usedBy:['《AI 工具测评》排版检查','选题研究'], source:'导入' },
    { id:'k-2', title:'竞品选题结构周报 8/12–8/19', type:'sheet', scope:'小红书运营', updated:'8/19', usedBy:['选题研究简报'], source:'林月 研究' },
    { id:'k-3', title:'品牌表达手册 v2', type:'doc', scope:'公司级', updated:'8/30', usedBy:['图文排版检查'], source:'导入' },
    { id:'k-4', title:'登录模块验收口径', type:'doc', scope:'研发部', updated:'9/08', usedBy:['登录模块回归测试'], source:'赵敏' },
  ];

  const skills = [
    { id:'sk-research', name:'行业研究', publisher:'Curis 官方', type:'方法', desc:'围绕一个行业问题收集事实、竞品与受众证据，输出可引用简报。', bound:['e-gu','e-linan'], installed:true, source:'official', perm:'公司内可用' },
    { id:'sk-doc', name:'长文档写作', publisher:'Curis 官方', type:'能力', desc:'长结构文档的撰写、改稿与一致性检查。', bound:['e-linan','e-shen','e-suge','e-wanglin'], installed:true, source:'official', perm:'公司内可用' },
    { id:'sk-data', name:'数据看板生成', publisher:'Curis 官方', type:'工具', desc:'从经营数据生成可读看板与周报口径（EST 自动标注）。', bound:['e-zhouning','e-hechuan','e-siheng'], installed:true, source:'official', perm:'公司内可用' },
    { id:'sk-xhs', name:'小红书排版规范', publisher:'社区', type:'方法', desc:'按平台规则检查图文排版、标签与敏感词。', bound:['e-zhen','e-suqing'], installed:true, source:'community', perm:'内容增长部' },
    { id:'sk-code', name:'代码工程', publisher:'Curis 官方', type:'工具', desc:'代码阅读、修改、测试与评审辅助（declared-file change）。', bound:['e-lin','e-zlan'], installed:true, source:'official', perm:'研发部' },
    { id:'sk-check', name:'验收清单', publisher:'Curis 官方', type:'方法', desc:'按验收口径逐条验证工作结果并留证据。', bound:['e-chen','e-zhao','e-sunhao'], installed:true, source:'official', perm:'公司内可用' },
    { id:'sk-browse', name:'Web Access（浏览器自动化）', publisher:'社区', type:'工具', desc:'读取公开网页并提取结构化信息。', bound:['e-gu'], installed:false, source:'community', perm:'需授权' },
    { id:'sk-method', name:'经营方法', publisher:'Curis 官方', type:'方法', desc:'目标→策略→责任拆解的经营方法包。', bound:['e-shen','e-cem'], installed:true, source:'official', perm:'公司内可用' },
    { id:'sk-report', name:'报告生成', publisher:'Curis 官方', type:'工具', desc:'把分析结果排版为带证据引用的报告。', bound:['e-siheng','e-zhouning'], installed:true, source:'official', perm:'公司内可用' },
    { id:'sk-web', name:'Workspace 实施', publisher:'Curis 官方', type:'工具', desc:'按 Workspace 设计落地结构与接线。', bound:['e-liang'], installed:true, source:'official', perm:'空间工程部' },
  ];
  const skill = id => skills.find(s => s.id === id);

  const connectors = [
    { id:'c-xhs', name:'小红书开放平台', status:'needs-auth', desc:'自动回收笔记互动数据；发布回执唯一来源', scope:'建议只读' },
    { id:'c-wx', name:'微信公众号', status:'disconnected', desc:'多平台分发（规划中）', scope:'—' },
    { id:'c-notion', name:'Notion', status:'connected', desc:'资料库外部来源', scope:'只读' },
    { id:'c-github', name:'GitHub', status:'connected', desc:'研发仓库与 PR', scope:'研发部' },
  ];

  const notifications = [
    { id:'n1', kind:'result', title:'结果就绪：登录模块 v1.3 联调通过', body:'周岚 · Curis 研发 · 附 3 条证据', time:'10 分钟前', go:'#/result/r-login' },
    { id:'n2', kind:'decision', title:'需要你确认：AI 工具测评定位调整', body:'林月 · AI 科技 · 制作被阻塞', time:'25 分钟前', go:'#/decision/d-xhs' },
    { id:'n3', kind:'blocked', title:'阻塞：赵敏回归测试等待联调完成', body:'Curis 研发 · waiting ≠ idle', time:'1 小时前', go:'#/work/w-test' },
    { id:'n4', kind:'meeting', title:'今天 16:00：周五复盘 · AI 科技内容转化', body:'4 人参与 · 议程 3 项', time:'2 小时前', go:'#/meeting/m-1' },
  ];

  const usage = {
    month:'9 月（截至今日）', total:'◇ 214.6', delta:'+12% vs 上月同期',
    byEmployee:[['周岚','◇ 66.2','研发部'],['陈真','◇ 34.0','内容增长部'],['林月','◇ 28.4','内容增长部'],['沈砚','◇ 25.3','空间工程部'],['司衡','◇ 18.6','数据分析部'],['顾行','◇ 12.1','空间工程部']],
    byModel:[['GLM-5.3','◇ 128.4'],['DeepSeek-V4.1','◇ 86.2']],
    budget:'预算上限 ◇ 400 / 月 · 已用 54%',
  };

  const assistantThread = [
    { role:'ai', text:'上午好。两件事值得注意：登录模块 v1.3 已联调通过（可作回归基线，周岚出品）；《AI 工具测评》卡在定位调整上——研究指向教程向（EST），但连续测评向利于人设，这在你职权授权的边缘，按规则升级给你。' },
    { role:'user', text:'先处理测评这篇。' },
    { role:'ai', text:'已置顶到你的待决定。我的建议：本篇按教程向发布，下两篇回到测评向——既吃到「教程+工具清单」的互动结构，又不打断人设积累。需要我把何川的归因数据展开吗？' },
  ];

  const ceoBrief = {
    date:'9 月 12 日 周五',
    items:[
      { kind:'decision', title:'《AI 工具测评》定位调整待你确认', who:'林月 · 内容增长部 · AI 科技', why:'制作被阻塞；研究指向教程向（EST）', go:'#/decision/d-xhs' },
      { kind:'decision', title:'灰度发布：登录模块 v1.4 首批 5%', who:'孙浩 · 研发部 · Curis 研发', why:'生产发布不可逆，需你批准', go:'#/decision/d-release' },
      { kind:'result', title:'登录模块 v1.3 联调通过', who:'周岚 · 研发部', why:'可作 v1.4 回归基线', go:'#/result/r-login' },
      { kind:'progress', title:'选题研究进入对比分析阶段', who:'林月 · AI 科技', why:'预计 30 分钟后输出 3 个选题', go:'#/work/w-research' },
      { kind:'progress', title:'宠物寄养：行业研究与 Workspace 设计进行中', who:'顾行 / 苏格 · 空间工程部', why:'激活建议将在下午提交', go:'#/business/biz-pet' },
      { kind:'meeting', title:'16:00 周五复盘 · AI 科技内容转化', who:'陈真 组织 · 4 人', why:'议程含定位调整确认', go:'#/meeting/m-1' },
    ],
    running:[{ w:'w-research' },{ w:'w-login' },{ w:'w-pet' }],
  };

  const cgChain = {
    opportunity: { id:'opp-1', title:'AI 工具类内容互动上升（信号）', source:'评论抽样 + 搜索词热度', score:'高', date:'9/10' },
    intent: { id:'int-1', title:'AI 工具实测选题（WHY：教程向互动更优 / WHAT：单工具上手 / GOAL：关注转化）', note:'Intent 不存推理与中间草稿（INTENT_EXCLUDES_INFERENCE）' },
    targetAccounts: [
      { n:'小红书 · AI 科技', st:'已连接', eligible:true, receipt:'回执可自动回收' },
      { n:'抖音 · 知行创意', st:'需授权', eligible:false, note:'连接器未授权 → 不具备发布资格（Target ≠ Eligibility）' },
      { n:'公众号 · 知行创意', st:'未连接', eligible:false, note:'未连接' },
    ],
    variants: [
      { v:'《AI 工具测评》教程向 Variant', reuse:'HIGH_REUSE：同素材微调', per:[['小红书 · AI 科技','制作中（文案）','—'],['抖音 · 知行创意','待资格（连接器授权）','—'],['公众号 · 知行创意','不适用本期','—']] },
    ],
    publications: [
      { acc:'小红书 · AI 科技', st:'已排期 9/21', receipt:'回执只能来自 Connector（未到发布时刻）' },
      { acc:'《效能工具上手指南》 · 小红书 · AI 科技', st:'已发布 9/10', receipt:'回执已回收 · 阅读 2.4w / 互动 1.1k（EST，待 Connector 对账）' },
    ],
  };
  return { org, employees, emp, businesses, biz, workspaces, ws, works, work, results, result, cgChain,
    decisions, meetings, knowledge, skills, skill, connectors, notifications, usage, assistantThread, ceoBrief };
})();
