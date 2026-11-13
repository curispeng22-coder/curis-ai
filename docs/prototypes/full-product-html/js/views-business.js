/* ============================================================
   Curis Full Product HTML Design Prototype — views-business.js
   P3 业务空间 / Workspace 工作面（Content Growth · RD · Generic）
   Work（Agent Progress）/ Decision / Result·Utility / 成果库 / Conversation
   结构消费：BUSINESS_WORK_SURFACE_PAGE_CONTRACT（四部分）+ 08/09 D 代 anatomy
           + CURIS_MULTI_SURFACE_PROFESSIONAL_WORKSPACE_UX_REVIEW（六 Surface 作 Domain Navigation）
   ============================================================ */
window.V = window.V || {};
window.CONV = (function () {
  const threads = {
    'e-zhen': [
      { role:'ai', emp:'e-zhen', text:'本周 AI 科技的重点是把「教程 + 工具清单」结构跑通。林月的调研快出结果了，我建议等她 3 个选题落地后再排下期。', model:'GLM-5.3', cost:'◇ 1.1' },
      { role:'user', text:'定位调整的事你怎么看？' },
      { role:'ai', emp:'e-zhen', text:'这是 Leader 职权边缘的判断：何川的归因（EST）支持教程向，但我们连续测评向做了 3 篇。我按规则升级给 CEO 了，建议是本篇教程向、下两篇回测评。', citations:['选题研究简报','竞品选题结构周报'], model:'GLM-5.3', cost:'◇ 0.8' },
    ],
    'e-linan': [
      { role:'ai', emp:'e-linan', text:'调研进入对比分析：5 个对标账号里「教程 + 工具清单」组合互动中位数高 34%（EST，样本 120 篇）。预计 30 分钟后给出 3 个选题。', steps:[{t:'评论样本收集',done:true},{t:'对标内容结构对比',done:true},{t:'输出选题（3 个）',done:false}], model:'DeepSeek-V4.1', cost:'◇ 2.2' },
      { role:'user', text:'好，选题出来先给陈真过目。' },
      { role:'ai', emp:'e-linan', text:'收到，会走「交接至 内容运营」的默认交接，附研究简报引用。', model:'DeepSeek-V4.1', cost:'◇ 0.4' },
    ],
    'e-zlan': [
      { role:'ai', emp:'e-zlan', text:'v1.4 联调：错误码 4012 的前端映射已对齐，单测 22/22。还差异常分支（限流触发）的真实环境验证。', tools:[{n:'编辑 auth.service.ts',d:'validatePassword() 增加错误码 4012'},{n:'运行单测',d:'auth 22 passed / 0 failed'}], model:'DeepSeek-V4.1', cost:'◇ 3.4' },
      { role:'user', text:'联调完成后直接交接给赵敏做回归。' },
      { role:'ai', emp:'e-zlan', text:'收到。交接会带 Diff 与单测证据，赵敏那边等这个信号就可以开始。', result:'r-login', model:'DeepSeek-V4.1', cost:'◇ 0.3' },
    ],
  };
  const generic = e => [
    { role:'ai', emp:e.id, text:`这里是与 ${e.name} 的工作对话。当前责任：${e.responsibility.current}。`, model:e.model, cost:'◇ 0.2' },
  ];
  return { forEmployee(id){ return threads[id] || generic(FX.emp(id) || { id:'e-shen', name:'员工', responsibility:{current:'—'}, model:'GLM-5.3' }); } };
})();

(function () {
  const { I, ico } = C;

  /* ---------- P3 业务空间：Business 列表 ---------- */
  V.business = function () {
    const rows = Object.values(FX.businesses).map(b => {
      const d = FX.org.departments.find(x => x.name === b.dept);
      return `<div class="row" data-action="go" data-arg="#/business/${b.id}">
        ${C.st(b.activating ? 'activating' : 'running')}
        <span class="grow"><div class="title">${b.name}</div>
          <div class="meta">${d ? d.name : ''} · Leader ${FX.emp(b.leader).name} · ${b.workspaces.length} 个 Workspace · ${b.desc}</div></span>
        <span class="end">${ico(I.chev, 14)}</span></div>`;
    }).join('');
    return {
      crumbs: C.crumbs([{ t: 'Curis' }, { t: '业务空间' }]),
      html: `
        <div class="page-head" style="display:flex;align-items:center"><div><h1>业务空间</h1><div class="sub">每个 Business 是一条持续经营的业务线，归属部门，至少拥有一个 Workspace</div></div>
          <span class="spacer"></span><button class="btn primary" data-action="go" data-arg="#/activate">提出新业务意图</button></div>
        <div class="rowlist">${rows}</div>
        <div class="faint" style="margin-top:10px;font-size:11px">经营在 Workspace 内进行；Business 页只做目录、聚合与进入（BUSINESS_WORK_SURFACE_PAGE_CONTRACT）。</div>`,
    };
  };

  /* ---------- Business 详情（四部分合同）---------- */
  V.businessDetail = function (params) {
    const b = FX.biz(params.id) || FX.biz('biz-cg');
    const d = FX.org.departments.find(x => x.name === b.dept);
    const wss = b.workspaces.map(id => FX.ws(id));
    const team = [...new Set(wss.flatMap(w => w.team))];
    const activation = b.activating ? `
      <div class="section"><div class="section-head"><h2 class="section-title">激活进度（CEO intent → Business → Workspace → Operating）</h2></div>
        <div class="rowlist">
          ${[['CEO 意图捕获', true, '「我想在小区周边做宠物寄养」'],
             ['空间工程部承接（可委托，非唯一入口）', true, '沈砚承接 · 组合研究/设计/实施/质量'],
             ['行业研究（顾行）', true, '宠物寄养市场与定价 · 竞品结构（进行中）'],
             ['Workspace 设计（苏格）', false, '首个 Workspace 结构设计中'],
             ['激活建议 → CEO Gate', false, '稍后提交：Business 定义 + 团队 + 首个 Workspace'],
             ['开始经营', false, '待你批准激活建议']].map(r => `
            <div class="row"><span class="dot ${r[1] ? 'ok' : 'idle'}"></span>
              <span class="grow"><div class="title" style="${r[1] ? '' : 'color:var(--ui-text-2)'}">${r[0]}</div><div class="meta">${r[2]}</div></span></div>`).join('')}
        </div></div>` : '';
    return {
      crumbs: C.crumbs([{ t: '业务空间', go: '/business' }, { t: b.dept }, { t: b.name }]),
      html: `
        <div class="page-head" style="display:flex;align-items:center"><div><h1>${b.name}</h1>
          <div class="sub">${d.name} · 业务负责人 ${FX.emp(b.leader).name} · ${b.stage} · ${b.desc}</div></div>
          <span class="spacer"></span><button class="btn" data-action="go" data-arg="#/conversation/${b.leader}">和负责人对话</button></div>
        <div class="section"><div class="section-head"><h2 class="section-title">当前经营状态</h2></div>
          <div class="card">${b.brief}</div></div>
        ${activation}
        <div class="section"><div class="section-head"><h2 class="section-title">Workspace 目录</h2></div>
          <div class="rowlist">${wss.map(w => `<div class="row" data-action="go" data-arg="#/workspace/${w.id}">
            <span class="tag">${w.type === 'professional' ? '专业' : '通用'}</span>
            <span class="grow"><div class="title">${w.name}</div><div class="meta">负责人 ${FX.emp(w.leader).name} · ${w.surfaces.length} 个 Surface · ${w.domain}</div></span>
            <span class="end">进入 ${ico(I.chev, 14)}</span></div>`).join('')}
            <div class="row" data-action="noop"><span class="grow faint" style="font-size:13px">+ 新建 Workspace（设计原型入口）</span></div></div></div>
        <div class="section"><div class="section-head"><h2 class="section-title">业务团队</h2><span class="section-more">团队在 Workspace 内运转；此处为聚合视图</span></div>
          <div class="rowlist">${team.map(id => C.empRow(FX.emp(id), { openAction: 'open-employee' })).join('')}</div></div>`,
    };
  };

  /* ---------- 新业务激活（FLOW C）---------- */
  V.activate = function () {
    return {
      crumbs: C.crumbs([{ t: '业务空间', go: '/business' }, { t: '提出新业务意图' }]),
      html: `
        <div class="page-head"><h1>告诉 Curis，你想开始做什么</h1><div class="sub">默认入口是对话：CEO 只需说意图；Curis 负责 复用→组合→研究→建议→激活（CREATE_BUSINESS_FLOW_CONTRACT）</div></div>
        <div style="max-width:680px">
          ${RT.composer('c-activate', { thread: 'activate', placeholder: '例如：我想在小区周边做宠物寄养生意…' }).replace('<textarea class="cx-input" rows="1"', '<textarea class="cx-input" rows="2"')}
          <div class="card" style="margin-top:16px"><div class="section-title" style="margin-bottom:8px">Curis 的理解（进行中）</div>
            <div class="rowlist" style="border:0">
              ${[['理解意图', true, '宠物寄养 · 本地服务 · 小规模起步'],
                 ['查找可复用的 Business / Workspace', true, '无既有业务可复用 → 走研究路径'],
                 ['研究与能力发现', true, '顾行：行业研究进行中（宠物寄养市场与定价）'],
                 ['经营建议（Operating Proposal）', false, '待研究完成后由空间工程部提交'],
                 ['CEO Gate：批准激活', false, '批准后 → 归属部门 → 首个 Workspace → 团队责任 → 开始经营']].map(r => `
                <div class="row"><span class="dot ${r[1] ? 'ok' : 'idle'}"></span>
                  <span class="grow"><div class="title">${r[0]}</div><div class="meta">${r[2]}</div></span></div>`).join('')}
            </div></div>
          <div class="faint" style="margin-top:8px;font-size:11px">DESIGN FIXTURE · 流程措辞消费 Structure Baseline §5 / CREATE_BUSINESS_FLOW_CONTRACT / Shared Authority §9.5</div>
        </div>`,
    };
  };

  /* ---------- Workspace 工作面（Four-Pane）---------- */
  V.workspace = function (params) {
    const w = FX.ws(params.id) || FX.ws('ws-cg');
    const surf = w.surfaces.find(s => s.id === params.surface) || w.surfaces[0];
    const b = FX.biz(w.business);
    const myWorks = FX.works.filter(x => x.ws === w.id);
    const ctxHtml = `
      <div class="nav-group">Surface（Domain Navigation）</div>
      ${w.surfaces.map(s => `<button class="nav-item ${s.id === surf.id ? 'active' : ''}" data-action="ws-surface" data-arg="${s.id}">${s.name}</button>`).join('')}
      <div class="nav-group">共享工作区</div>
      <button class="nav-item ${surf.id === 'overview' ? 'hidden' : ''}" data-action="ws-surface" data-arg="overview">员工工作区（谁在做什么）</button>
      <div class="nav-group">${w.domain === '产品研发' ? '代码与责任' : '选题库'}</div>
      ${w.id === 'ws-rd' ? `
        <div class="ctx-item mono" style="padding:6px 8px;font-size:12px;color:var(--ui-text-2)">▸ product-platform/src</div>
        <div class="ctx-item mono" style="padding:6px 8px 6px 20px;font-size:12px;color:var(--ui-text-2)">▸ auth/</div>
        <div class="ctx-item mono active" style="padding:6px 8px 6px 32px;font-size:12px">login.ts</div>
        <div class="ctx-item mono" style="padding:6px 8px 6px 32px;font-size:12px;color:var(--ui-text-2)">session.ts</div>
        <div class="hr" style="margin:8px 0"></div>
        <div style="padding:4px 8px;font-size:12px;color:var(--ui-text-2)">责任：登录模块重构 · 接口联调</div>
        <div style="padding:4px 8px;font-size:12px;color:var(--ui-text-2)">Recent：login.ts · 34-93<br>联调结果 v1.3</div>`
      : `
        <div style="padding:4px 8px;font-size:12px;color:var(--ui-text-2)">信号：AI 工具类搜索量上升 · 竞品爆文 ×2</div>
        <div style="padding:4px 8px;font-size:12px;color:var(--ui-text-2)">素材：实拍图 ×12 · 用户证言 ×3</div>
        <div style="padding:4px 8px;font-size:12px;color:var(--ui-text-2)">内容日历：9 月第 3 周 · 3 篇排期</div>`}`;
    const op5 = `
      <div class="grid c2" style="margin-bottom:16px">
        <div class="card"><div class="faint" style="font-size:11px;margin-bottom:4px">经营状态</div><div style="font-weight:600">${b.stage} · ${b.brief.split('；')[0]}</div></div>
        <div class="card"><div class="faint" style="font-size:11px;margin-bottom:4px">本轮重点</div><div>${w.domain === '产品研发' ? '登录模块 v1.4：联调收口 → 回归 → 灰度' : '验证「教程 + 工具清单」结构的关注转化'}</div></div>
        <div class="card"><div class="faint" style="font-size:11px;margin-bottom:4px">最新判断</div><div>${w.domain === '产品研发' ? 'v1.3 可作回归基线；灰度方案已升级 CEO' : '教程向互动中位数高 34%（EST，何川归因）'}</div></div>
        <div class="card"><div class="faint" style="font-size:11px;margin-bottom:4px">下一步</div><div>${w.domain === '产品研发' ? '回归全绿后灰度 5%（待 CEO 批准）' : '周五复盘会确认定位调整'}</div></div>
      </div>`;
    const teamOp = `
      <div class="section"><div class="section-head"><h2 class="section-title">团队运转</h2><span class="section-more">默认流程 · A→B 只表示默认下一责任，不是强制 DAG</span></div>
        <div class="card"><div class="chip-row">${w.flow.map((f, i) => `<span class="chip ${i === 0 ? 'active' : ''}">${f}</span>${i < w.flow.length - 1 ? '<span class="faint">→</span>' : ''}`).join('')}</div></div></div>`;
    const workarea = `
      <div class="section"><div class="section-head"><h2 class="section-title">工作区</h2><span class="section-more">点击员工展开对话 · 点击姓名进员工详情</span></div>
        <div class="rowlist">${w.team.map(id => {
          const e = FX.emp(id);
          const ew = myWorks.find(x => x.employee === id);
          const tk = 'emp:' + id;
          return C.empRow(e, {
            openAction: 'toggle-emp-conv', utilAction: 'emp-util',
            body: `<div style="margin-bottom:8px">${ew ? C.todoList(ew.plan).replace('class="todo"', 'class="todo" style="font-size:12px"') : `当前责任：${e.responsibility.current}`}</div>
              <div class="emp-conv hidden" data-empconv="${id}" style="margin-bottom:8px">
                <div class="conversation" style="max-width:none;padding:0">${RT.renderThread(tk)}</div>
                ${RT.composer('c-ws-' + id, { thread: tk, placeholder: `与 ${e.name} 对话，或直接交代一件事…`, exec: `执行 · ${e.name}`, model: e.model })}
              </div>`,
          });
        }).join('')}</div></div>`;
    /* Surface-specific Main 内容 */
    let surfaceMain = '';
    if (w.id === 'ws-cg') {
      if (surf.id === 'overview') surfaceMain = op5;
      if (surf.id === 'research') surfaceMain = `
        <div class="section"><div class="section-head"><h2 class="section-title">研究对象</h2><span class="section-more">3 个对象 · 2 个进行中</span></div>
          <div class="grid c3">
            ${[['趋势 · 8/18','AI 工具实测内容的机会','证据：近 7 天 120 篇笔记评论抽样','w-research'],
               ['竞品 · 8/19','同类账号选题结构对比','证据：5 个对标账号 30 天内容结构','w-research'],
               ['受众 · 8/15','AI 科技受众兴趣分层','证据：问卷 200 份 + 评论区意图标注','w-research']].map(r => `
            <div class="card"><div class="faint" style="font-size:11px;margin-bottom:6px">${r[0]}</div>
              <div style="font-weight:600;margin-bottom:4px">${r[1]}</div>
              <div class="muted" style="font-size:12px;margin-bottom:8px">${r[2]}</div>
              <div style="display:flex;gap:6px;align-items:center"><span class="chip">${ico(C.I.hand, 12)} 交接至 内容运营</span><span class="spacer"></span>${C.avatarById('e-linan','sm')}</div></div>`).join('')}
          </div></div>`;
      if (surf.id === 'content') { const cg = FX.cgChain; const view = params.q.view || 'list'; surfaceMain = `
        <div class="section"><div class="section-head"><h2 class="section-title">内容对象</h2>
          <div class="seg-pill"><button class="${view === 'list' ? 'active' : ''}" data-action="ws-view" data-arg="list">列表</button><button class="${view === 'cal' ? 'active' : ''}" data-action="ws-view" data-arg="cal">日历</button></div></div></div>
        <div class="section"><div class="section-head"><h2 class="section-title" style="font-size:14px">① Opportunity（信号）</h2></div>
          <div class="rowlist"><div class="row"><span class="grow"><div class="title">${cg.opportunity.title}</div><div class="meta">来源：${cg.opportunity.source} · 评分 ${cg.opportunity.score} · ${cg.opportunity.date}</div></span></div></div></div>
        <div class="section"><div class="section-head"><h2 class="section-title" style="font-size:14px">② Intent（WHY / WHAT / GOAL）</h2></div>
          <div class="rowlist"><div class="row"><span class="grow"><div class="title">${cg.intent.title}</div><div class="meta">${cg.intent.note}</div></span></div></div></div>
        <div class="section"><div class="section-head"><h2 class="section-title" style="font-size:14px">③ Target Account Set（Target ≠ Eligibility）</h2></div>
          <div class="rowlist">${cg.targetAccounts.map(t => `<div class="row">
            <span class="grow"><div class="title">${t.n}</div><div class="meta">${t.eligible ? t.receipt : t.note}</div></span>
            ${t.eligible ? '<span class="tag" style="color:var(--ui-success)">具备资格</span>' : '<span class="tag" style="color:var(--ui-warning)">不具备资格</span>'}${C.st(t.st === '已连接' ? 'done' : t.st === '需授权' ? 'review' : 'idle')}</div>`).join('')}</div></div>
        <div class="section"><div class="section-head"><h2 class="section-title" style="font-size:14px">④ Content Variant（按账号复用）</h2></div>
          ${cg.variants.map(v => `<div class="card" style="margin-bottom:10px"><div style="font-weight:600;margin-bottom:2px">${v.v}</div>
            <div class="faint" style="font-size:11px;margin-bottom:6px">${v.reuse}</div>
            <div class="rowlist" style="border:0">${v.per.map(pp => `<div class="row"><span style="flex:0 0 170px" class="muted">${pp[0]}</span><span class="grow">${pp[1]}</span><span class="end">${pp[2]}</span></div>`).join('')}</div></div>`).join('')}</div>
        <div class="section"><div class="section-head"><h2 class="section-title" style="font-size:14px">⑤ Publication（逐账号 · 回执只能来自 Connector）</h2></div>
          <div class="rowlist">${cg.publications.map(pp => `<div class="row">
            <span class="grow"><div class="title">${pp.acc}</div><div class="meta">${pp.receipt}</div></span>
            <span class="end">${pp.st}</span></div>`).join('')}
          </div>
          <div class="faint" style="font-size:11px;margin-top:6px">聚合"已发布"不替代逐账号状态；断连账号保留历史目标，仅当前不具备发布资格。</div></div>`; }
      if (surf.id === 'content' && (params.q.view || 'list') === 'cal') { surfaceMain = `
        <div class="section"><div class="section-head"><h2 class="section-title">内容排期 · 本周（9/15–9/19）</h2><span class="section-more">Channel Account：小红书 · AI 科技（唯一具备发布资格）</span></div>
          <div class="cal">
            ${[['周一 9/15',[['选题确认（林月→陈真）','done'],['《效能工具上手指南》数据回收','done']]],
               ['周二 9/16',[['测评稿完稿（林月）','']]],
               ['周三 9/17',[['封面与排版（苏晴）',''],['平台规则复审','warn']]],
               ['周四 9/18',[['CEO 发布检查（陈真）','warn'],['排期发布 · AI 科技账号','']]],
               ['周五 9/19',[['复盘会输入准备（何川）','']]]].map(d => `
            <div class="day"><h4>${d[0]}</h4>${d[1].map(e => `<div class="ev ${e[1]}">${e[0]}</div>`).join('')}</div>`).join('')}
          </div></div>`; }
      if (surf.id === 'growth') surfaceMain = `
        <div class="section"><div class="section-head"><h2 class="section-title">增长与评估</h2><span class="section-more">数据标注 EST · 回执只能来自 Connector</span></div>
          <div class="kpi-row" style="margin-bottom:12px"><div class="kpi"><div class="n">2.4w</div><div class="l">近 7 天阅读 · EST</div></div>
            <div class="kpi"><div class="n">1.1k</div><div class="l">互动 · EST</div></div><div class="kpi"><div class="n">3.8%</div><div class="l">转化 · EST</div></div></div>
          <div class="rowlist"><div class="row"><span class="grow"><div class="title">归因任务：上周 3 篇的互动来源</div><div class="meta">何川 · 进行中 · 引用选题研究简报</div></span>${C.st('working')}</div>
          <div class="row"><span class="grow"><div class="title">连接器未授权提醒</div><div class="meta">自动数据回收需要小红书开放平台只读授权</div></span><button class="btn sm" data-action="open-decision" data-arg="d-connector">去授权</button></div></div></div>`;
      if (surf.id === 'feedback') surfaceMain = `<div class="section">${C.emptyState('反馈回流', '评论区与私信信号会在发布后回流到这里（需连接器授权后自动收集）。', [])}</div>`;
      if (surf.id === 'commercial') surfaceMain = `<div class="section">${C.emptyState('商业化（Optional Surface）', '线索与转化承接。此 Surface 按需启用。', [])}</div>`;
    } else if (w.id === 'ws-rd') {
      if (surf.id === 'overview') surfaceMain = `
        <div class="decision-banner">
          <div class="db-title">CEO Decision · Layer 0 · 灰度发布：登录模块 v1.4 首批 5% 用户</div>
          <div class="db-body">发生了什么：v1.4 联调进行中（Adapter 80%）、回归被联调阻塞。为何升级：生产发布不可逆（高风险），前置条件（回归全绿）未满足。员工推荐：孙浩的灰度方案（5% · 观察 24 小时错误率）已就绪。<b>本层只能：查看方案 / 暂缓。批准入口在回归全绿后的 Decision Layer 1。</b></div>
          <div class="decision-actions"><button class="btn" data-action="go" data-arg="#/decision/d-release/layer1">查看发布方案（Layer 1）</button><button class="btn" data-action="rd-defer" data-arg="d-release">暂缓</button><span class="faint" style="align-self:center;font-size:11px">Approve / Reject / Choice → Layer 1（P7 决策分层）</span></div>
        </div>
        <div class="section"><div class="section-head"><h2 class="section-title">当前研发</h2></div>
          <div class="rowlist">
            ${[['产品 / 需求','已确认（王琳）','done'],['架构','已确认（林涛）','done'],['Runtime','已完成','done'],['Frontend Adapter','80% · 联调中（周岚）','working'],['Test','回归等待联调（赵敏 · waiting）','blocked'],['Review / 发布门禁','待回归（孙浩）','idle']].map(r => `
            <div class="row"><span style="flex:0 0 140px" class="muted">${r[0]}</span><span class="grow">${r[1]}</span>${C.st(r[2])}</div>`).join('')}
          </div></div>
        <div class="section"><div class="section-head"><h2 class="section-title">当前 Blocker 与需要你</h2></div>
          <div class="rowlist"><div class="row" data-action="open-work" data-arg="w-test"><span class="grow"><div class="title">回归测试被联调阻塞（waiting ≠ idle）</div><div class="meta">赵敏 · Curis 研发</div></span>${C.st('blocked')}</div></div></div>`;
      if (surf.id === 'dev') surfaceMain = myWorks.filter(x => x.surface === 'dev').map(x => C.workCard(x)).join('<div style="height:12px"></div>') || op5;
      if (surf.id === 'test') surfaceMain = myWorks.filter(x => x.surface === 'test').map(x => C.workCard(x)).join('<div style="height:12px"></div>') || `<div class="section">${C.emptyState('暂无测试工作','回归用例已就绪，等待联调完成。',[])}</div>`;
      if (surf.id === 'review' || surf.id === 'release') surfaceMain = `<div class="section"><div class="section-head"><h2 class="section-title">${surf.name}</h2></div>
        <div class="rowlist"><div class="row"><span class="grow"><div class="title">登录模块 v1.4 · 发布门禁检查</div><div class="meta">孙浩 · 灰度方案已升级 CEO（不可逆操作）</div></span>${C.st('review')}</div></div></div>`;
    } else {
      surfaceMain = surf.id === 'overview' ? `
        <div class="section"><div class="section-head"><h2 class="section-title">当前工作</h2></div>
          <div class="grid c2">${myWorks.map(x => C.workCard(x)).join('')}</div></div>` : '';
    }
    return {
      crumbs: C.crumbs([{ t: '业务空间', go: '/business' }, { t: b.name, go: '/business/' + b.id }, { t: w.name }, { t: surf.name }]),
      ctxTitle: w.name,
      ctxHtml,
      states: { normal: {}, emptyFirst: { emptyFirst: true }, working: {}, error: {} },
      html: (s) => s.emptyFirst ? `
        <div class="page-head"><h1>${w.name}</h1><div class="sub">${w.type === 'professional' ? '专业工作空间' : '通用工作空间'} · ${w.domain}</div></div>
        ${C.emptyState('工作空间已创建，还没有开始工作', `把第一件事交给 ${FX.emp(w.leader).name}（负责人），或从下面的建议开始。`,
          [{ t: '派一件工作给负责人', action: 'focus-conv' }, { t: '先看团队与责任', action: 'noop' }])}`
      : `
        <div class="page-head" style="display:flex;align-items:center"><div><h1>${w.name}</h1>
          <div class="sub">${w.type === 'professional' ? '专业工作空间' : '通用工作空间'} · ${w.domain} · 负责人 ${FX.emp(w.leader).name} · 目标：${b.brief}</div></div>
          <span class="spacer"></span><button class="btn" data-action="open-employee" data-arg="${w.leader}">负责人</button></div>
        ${surf.id === 'overview' ? '' : `<div class="crumbs" style="margin-bottom:12px">当前 Surface：<b>${surf.name}</b> · ${surf.desc}</div>`}
        ${surfaceMain}
        ${surf.id === 'overview' ? (teamOp + workarea) : ''}`,
      util: UTIL.forWorkspace(w, surf),
    };
  };

  /* Utility 内容：CG=图文预览/审核/数据 · RD=Diff/Source/Preview · 通用=Employee Quick Panel */
  window.UTIL = window.UTIL || {};
  UTIL.forWorkspace = function (w, surf) {
    const emp = FX.emp(w.team[0]);
    if (w.id === 'ws-rd') return { title: '登录模块 · 变更', tabs: ['Diff', 'Source', 'Preview'], active: 'Diff', html: `
      <div class="muted" style="font-size:12px;margin-bottom:8px">变更归属责任：登录模块重构 · 接口联调（周岚）</div>
      <div class="doc-preview mono" style="font-size:12px;line-height:1.6">
        <div style="color:var(--ui-danger)">- if (pwd.length < 8) return err('PWD_SHORT')</div>
        <div style="color:var(--ui-success)">+ if (pwd.length < 8) return err(4012, 'PWD_SHORT')</div>
        <div style="color:var(--ui-success)">+ if (rateLimit.hit(ip)) return err(4029, 'TOO_MANY')</div>
      </div>
      <div class="muted" style="font-size:11px;margin:8px 0">+34 / −93 · declared-file change · 证据已入 Result</div>
      <div style="display:flex;gap:8px"><button class="btn sm primary">提交变更</button><button class="btn sm">请求协审</button></div>` };
    if (w.id === 'ws-cg') return { title: '《AI 工具测评》', tabs: ['图文预览', '审核', '数据'], active: '图文预览', html: `
      <div class="doc-preview"><h3>AI 工具测评 · 极简风</h3><p>（封面占位）极简封面：工具截图 + 一句利益点。</p>
        <p>正文结构：痛点引入 → 工具演示 → 行动建议。标签：#AI工具 #效率 #教程</p>
        <p class="faint" style="font-size:11px">排版检查：通过（sk-xhs）· 敏感词：0</p></div>
      <div class="hr"></div><div class="faint" style="font-size:11px">发布后：数据 tab 显示 EST；回执来自 Connector。</div>` };
    return { title: '快速协作', tabs: ['面板'], active: '面板', html: `
      ${C.avatar(emp)}<div style="font-weight:650;margin-top:8px">${emp.name}</div>
      <div class="muted" style="font-size:12px">${emp.role} · ${C.stFull(emp)}</div>
      <div class="hr"></div>
      <div style="font-size:12px;color:var(--ui-text-2);line-height:1.7">当前责任：${emp.responsibility.current}<br>最近成果：${(FX.results.find(r => r.employee === emp.id) || {}).title || '—'}</div>
      <div class="hr"></div>${RT.composer('c-qk-' + emp.id, { thread: 'emp:' + emp.id, placeholder: '直接对话…', exec: `执行 · ${emp.name}`, model: emp.model })}` };
  };

  /* ---------- Work（Agent Progress 专题页）---------- */
  V.work = function (params) {
    const w = FX.work(params.id) || FX.work('w-login');
    const e = FX.emp(w.employee);
    const done = w.plan.filter(p => p.done).length;
    return {
      crumbs: C.crumbs([{ t: w.ws ? FX.ws(w.ws).name : '公司级', go: w.ws ? '/workspace/' + w.ws : '/ceo' }, { t: '工作' }, { t: w.title }]),
      ctxTitle: '工作概览（首层）',
      ctxHtml: `<div style="padding:8px 4px;font-size:12px;line-height:1.8">
        <div><b>谁在做</b>：${e.name}（${e.role}）${w.holder ? `<br><b>Holder</b>：${FX.emp(w.holder).name}${w.holder !== w.employee ? '（Executor：' + e.name + '）' : ''}` : ''}</div>
        <div style="margin-top:6px"><b>做什么</b>：${w.title}</div>
        <div style="margin-top:6px"><b>当前动作</b>：${w.current}</div>
        <div style="margin-top:6px"><b>等什么</b>：${w.status === 'blocked' ? '被「' + FX.work(w.blockedBy).title + '」阻塞' : w.status === 'working' ? '执行中，不等待' : '—'}</div>
        <div style="margin-top:6px"><b>做到哪里</b>：${w.plan.filter(p => p.done).length}/${w.plan.length} 步 · ${w.elapsed}</div>
        <div style="margin-top:6px"><b>产生什么</b>：${w.result ? FX.result(w.result).title : '完成后产生 Result + Evidence'}</div>
        <div class="hr"></div>
        <div class="faint" style="font-size:11px">次层 Inspector（环境/来源/Git）在 Utility。为什么由 TA 做：责任「${e.responsibility.longTerm.split('，')[0]}」解析到 ${e.name}。</div></div>`,
      util: { title: '工具活动', tabs: ['工具'], active: '工具', html: w.tools.length ? `
        <div class="rowlist">${w.tools.map(t => `<div class="row"><span class="grow"><div class="title">${t.n}</div><div class="meta">${t.d}</div></span>${C.st('done')}</div>`).join('')}</div>
        <div class="faint" style="margin-top:8px;font-size:11px">默认折叠 · 在对话中以摘要行呈现</div>` : '<div class="faint" style="font-size:12px">本工作暂无工具活动。</div>' },
      html: `
        <div class="page-head" style="display:flex;align-items:center">
          ${C.avatar(e)}<div><h1>${w.title}</h1>
          <div class="sub">${e.name} · ${e.role} ${w.ws ? '· ' + FX.ws(w.ws).name : ''} · ${C.st(w.status === 'needs_ceo' ? 'review' : w.status)}</div></div>
          <span class="spacer"></span>
          <span class="chip">${ico(C.I.cal, 12)} ${w.elapsed}</span><span class="chip">${w.cost}</span>
          <button class="btn" data-action="go" data-arg="#/conversation/${e.id}">对话</button>
        </div>
        ${w.status === 'blocked' ? `<div class="error-banner" style="margin-bottom:16px"><div class="eb-title">被阻塞 · 等待 ${FX.work(w.blockedBy).title}</div>
          <div class="eb-body">这是「等待」状态（waiting ≠ idle）：不能推进，也不会被当作空闲分配新工作。</div>
          <div class="decision-actions"><button class="btn sm" data-action="open-work" data-arg="${w.blockedBy}">查看阻塞源</button><button class="btn sm ghost">通知我解除时</button></div></div>` : ''}
        ${w.decision ? C.decisionBanner(w.decision) : ''}
        <div class="section"><div class="section-head"><h2 class="section-title">计划与进度</h2><span class="section-more">${done}/${w.plan.length} 步 · 员工自主维护，可被打断改向</span></div>
          <div class="card">${C.todoList(w.plan)}<div style="margin-top:10px">${C.progressBar(Math.round(done / w.plan.length * 100))}</div></div></div>
        <div class="section"><div class="section-head"><h2 class="section-title">当前动作</h2></div>
          <div class="card"><div style="display:flex;gap:8px;align-items:center"><span class="dot run"></span><span style="font-weight:550">${w.current}</span></div></div></div>
        ${w.collaboration ? `<div class="section"><div class="section-head"><h2 class="section-title">协作</h2></div>
          <div class="rowlist">${w.collaboration.map(id => { const c = FX.emp(id); return `<div class="row" data-action="open-employee" data-arg="${id}">${C.avatar(c, 'sm')}<span class="grow"><div class="title">${c.name}</div><div class="meta">${c.role} · 关注此工作 / 可被咨询</div></span></div>`; }).join('')}</div></div>` : ''}
        ${w.reviewReq ? `<div class="section"><div class="section-head"><h2 class="section-title">Review Request（≠ Handoff）</h2></div>
          <div class="card" style="font-size:13px">${w.reviewReqNote}</div></div>` : ''}
        ${w.handoff ? `<div class="section"><div class="section-head"><h2 class="section-title">交接（Handoff 契约）</h2></div>
          <div class="card" style="display:flex;gap:10px;align-items:center">${ico(C.I.hand, 16)}<span>${w.handoff}</span><span class="spacer"></span>${C.st('idle')}</div></div>` : ''}
        ${w.result ? `<div class="section"><div class="section-head"><h2 class="section-title">结果（自然过渡）</h2></div>
          <div class="rowlist">${C.resultCard(FX.result(w.result))}</div></div>` : ''}`,
    };
  };

  /* ---------- Decision ---------- */
  V.decision = function (params) {
    const d = FX.decisions.find(x => x.id === params.id) || FX.decisions[0];
    if (params.layer1) {
      return {
        crumbs: C.crumbs([{ t: 'CEO 工作台', go: '/ceo' }, { t: '决定' }, { t: d.title }, { t: 'Layer 1 · 发布方案' }]),
        util: { title: '门禁检查', tabs: ['门禁'], active: '门禁', html: '<div class="rowlist">' + [['回归测试','12/12 通过（赵敏）'],['错误率观察','24h < 0.1%（预算）'],['回滚预案','v1.3 镜像就绪']].map(r => '<div class="row"><span class="grow"><div class="title">' + r[0] + '</div><div class="meta">' + r[1] + '</div></span><span class="dot ok"></span></div>').join('') + '</div>' },
        html: `
          <div class="page-head"><h1>Layer 1 · 发布方案（灰度 5%）</h1><div class="sub">前置条件已满足：回归全绿。此处可执行批准 / 驳回（Layer 0 只能查看/暂缓）</div></div>
          <div class="section"><div class="section-title" style="margin-bottom:8px">方案内容</div>
            <div class="card" style="line-height:1.8;font-size:13.5px">
              ① 首批灰度 5% 用户（按设备尾号），观察 24 小时错误率与登录成功率。<br>
              ② 指标阈值：错误率 < 0.1%、成功率 > 99.5%；异常即自动回滚至 v1.3 镜像。<br>
              ③ 全量节奏：灰度 24h 后逐步 25% → 100%，每步间隔 12 小时。<br>
              ④ 证据留存：发布回执、监控截图、回滚演练记录 → Result Evidence。
            </div></div>
          <div class="section"><div class="section-title" style="margin-bottom:8px">执行</div>
            <div class="decision-actions"><button class="btn primary" data-action="noop">批准灰度发布</button><button class="btn" data-action="noop">驳回（附意见）</button></div></div>`,
      };
    }
    return {
      crumbs: C.crumbs([{ t: 'CEO 工作台', go: '/ceo' }, { t: '决定' }, { t: d.title }]),
      util: { title: '技术证据', tabs: ['证据'], active: '证据', html: `<div class="muted" style="font-size:12px;margin-bottom:8px">白话 Decision 在此；技术证据在 Result Reference / Utility。</div>
        <div class="rowlist">${(FX.result('r-research') ? [['选题研究简报', 'r-research'], ['竞品选题结构周报', null]] : []).map(r => `<div class="row"><span class="grow"><div class="title">${r[0]}</div></span>${r[1] ? `<button class="btn sm" data-action="open-result" data-arg="${r[1]}">打开</button>` : '<span class="end">资料库</span>'}</div>`).join('')}</div>` },
      html: `
        <div class="page-head"><h1>${d.title}</h1><div class="sub">来自 ${FX.emp(d.from).name} · ${FX.emp(d.from).role} · 升级原因：${d.body}</div></div>
        ${C.decisionBanner(d)}
        <div class="section" style="margin-top:16px"><div class="section-title" style="margin-bottom:6px">背景与选项说明</div>
          <div class="card muted" style="font-size:13px;line-height:1.8">
            你只需要做一件事：选择方向。技术证据、数据与执行细节由员工与 Leader 准备，附在同一 Decision Reference 下。<br>
            决定后：工作自动解除阻塞并继续；本决定进入公司记录（Result → Evidence 溯源）。
          </div></div>`,
    };
  };

  /* ---------- Result / Utility ---------- */
  V.result = function (params) {
    const r = FX.result(params.id) || FX.results[0];
    const e = FX.emp(r.employee);
    const isCode = r.type === 'code';
    return {
      crumbs: C.crumbs([{ t: r.ws ? FX.ws(r.ws).name : '公司级', go: r.ws ? '/workspace/' + r.ws : '/ceo' }, { t: '结果' }, { t: r.title }]),
      states: { normal: {}, loading: { loading: true }, error: {} },
      html: (s) => s.loading ? `
        <div class="page-head"><h1>${r.title}</h1><div class="sub">正在加载结果…</div></div>
        ${'<div class="skeleton" style="margin-bottom:10px"></div>'.repeat(6)}`
      : `
        <div class="page-head" style="display:flex;align-items:center">
          <span class="fc-ico" style="width:44px;height:44px;font-size:12px">${isCode ? 'CODE' : 'DOC'}</span>
          <div><h1>${r.title}</h1><div class="sub">${e.name} · ${e.role} · ${C.statusMeta(r.status)[1]} · 被 ${r.usedBy.length} 处引用</div></div>
          <span class="spacer"></span>
          <button class="btn" data-action="open-utility-result" data-arg="${r.id}">在 Utility 中打开</button>
          <button class="btn primary" data-action="go" data-arg="#/conversation/${e.id}">问 TA</button>
        </div>
        <div class="section"><div class="section-head"><h2 class="section-title">证据链（Result → Evidence）</h2><span class="section-more">事实先于观点</span></div>
          <div class="card">${r.evidence.map(ev => `<div class="ev-item"><span class="dot ok" style="margin-top:5px"></span><span>${ev}</span></div>`).join('')}</div></div>
        <div class="section"><div class="section-head"><h2 class="section-title">被引用</h2></div>
          <div class="rowlist">${r.usedBy.map(u => `<div class="row"><span class="grow">${u}</span><span class="end">引用</span></div>`).join('')}</div></div>
        <div class="section"><div class="section-head"><h2 class="section-title">继续</h2></div>
          <div style="display:flex;gap:8px;flex-wrap:wrap">
            <button class="btn" data-action="go" data-arg="#/conversation/${e.id}">基于此结果继续工作</button>
            <button class="btn" data-action="noop">导出</button>
            <button class="btn" data-action="noop">查看历史版本</button>
          </div></div>`,
      util: RESULT_UTIL(r),
    };
  };
  function RESULT_UTIL(r) {
    const isCode = r.type === 'code';
    const emp = FX.emp(r.employee);
    const followup = `<div class="hr"></div>${RT.composer('c-res-' + r.id, { thread: 'emp:' + r.employee, placeholder: '继续追问或派后续工作（携带本结果引用回到对话）…', exec: `执行 · ${emp ? emp.name : ''}` })}`;
    if (isCode) return { title: r.title.slice(0, 14), tabs: ['Preview', 'Source'], active: 'Preview', content: {
      'Preview': `<div class="doc-preview" style="text-align:center;padding:32px"><div class="faint" style="font-size:12px">登录页本地渲染（示例数据）</div>
        <div style="margin:16px auto;max-width:240px;border:1px solid var(--ui-line);border-radius:8px;padding:16px">
          <div class="skeleton" style="margin-bottom:8px"></div><div class="skeleton" style="margin-bottom:8px"></div>
          <div style="height:30px;border-radius:6px;background:var(--ui-accent);opacity:.85;margin-top:8px"></div></div>
        <div class="faint" style="font-size:11px;margin-top:10px">Follow-up 发送后携带本结果引用返回与 ${emp ? emp.name : '员工'} 的对话。</div></div>${followup}`,
      'Source': `<div class="doc-preview mono" style="font-size:12px;line-height:1.7"><div class="faint" style="margin-bottom:6px">product-platform/src/auth/login.ts · 34-93</div>
        <div>export async function login(req: LoginReq) {</div>
        <div style="padding-left:14px">const v = validatePassword(req.password)</div>
        <div style="padding-left:14px">if (v.code === 4012) throw new AuthError(4012, 'PWD_SHORT')</div>
        <div style="padding-left:14px">if (rateLimit.hit(req.ip)) throw new AuthError(4029, 'TOO_MANY')</div>
        <div style="padding-left:14px">return issueSession(req.user)</div>
        <div>}</div>
        <div class="faint" style="margin-top:8px">+34 / −93 · declared-file change · 证据已入 Result</div></div>${followup}` } };
    return { title: r.title.slice(0, 14), tabs: ['阅读'], active: '阅读', html: `<div class="doc-preview"><h3>${r.title}</h3><p>（阅读视图）本结果由真实工作产出，证据见主区证据链；引用保留来源与版本。</p><p class="faint" style="font-size:11px">WorkBuddy 阅读器参考：正文 + 顶部文件动作 + 打开关系。</p></div>${followup}` };
  }

  /* ---------- 成果库 ---------- */
  V.results = function () {
    return {
      crumbs: C.crumbs([{ t: 'Curis' }, { t: '成果库' }]),
      html: `
        <div class="page-head"><h1>成果库</h1><div class="sub">全部 Result · 附证据链与被引用关系</div></div>
        <div class="rowlist">${FX.results.map(r => {
          const e = FX.emp(r.employee);
          return `<div class="row" data-action="open-result" data-arg="${r.id}">
            <span class="fc-ico">${r.type === 'doc' ? 'DOC' : r.type === 'code' ? 'CODE' : 'XLSX'}</span>
            <span class="grow"><div class="title">${r.title}</div><div class="meta">${e.name} · ${r.ws ? FX.ws(r.ws).name : '公司级'} · 证据 ${r.evidence.length} 条 · 被 ${r.usedBy.length} 处引用</div></span>
            <span class="end">${C.statusMeta(r.status)[1]}</span></div>`; }).join('')}
        </div>`,
    };
  };

  /* ---------- 独立对话页（CEO → 员工）---------- */
  V.conversation = function (params) {
    const e = FX.emp(params.emp) || FX.emp('e-zhen');
    return {
      crumbs: C.crumbs([{ t: '对话' }, { t: e.name }]),
      html: `
        <div class="page-head" style="display:flex;align-items:center;gap:12px">${C.avatar(e)}
          <div><h1>${e.name}</h1><div class="sub">${e.role} · ${e.dept} · ${C.stFull(e)}</div></div>
          <span class="spacer"></span><button class="btn ghost" data-action="open-employee" data-arg="${e.id}">员工详情 →</button></div>
        <div class="conversation">${RT.renderThread('emp:' + e.id)}</div>
        <div style="position:sticky;bottom:0;background:var(--ui-bg);padding:8px 0 4px">
          ${RT.composer('c-conv-' + e.id, { thread: 'emp:' + e.id, placeholder: `与 ${e.name} 对话，或直接交代一件事…`, exec: `执行 · ${e.name}`, model: e.model })}
        </div>`,
    };
  };
})();
