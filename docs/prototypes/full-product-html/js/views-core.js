/* ============================================================
   Curis Full Product HTML Design Prototype — views-core.js
   P2 CEO 工作台 / P5 组织中心 / P6 Employee Detail / P7 人才与能力
   P11 经营洞察 / P9 资料库 / P10 会议 / P12 Settings
   页面返回 { crumbs, html, ctxTitle?, ctxHtml?, states? }
   ============================================================ */
window.V = window.V || {};
(function () {
  const { I, ico } = C;

  /* ---------- P2 CEO 工作台（去后台化：今日简报→待决定→正在运行→最新结果） ---------- */
  V.ceo = function () {
    const b = FX.ceoBrief;
    const kindIcon = { decision: I.gear, result: I.doc, progress: I.spark, meeting: I.cal };
    const kindName = { decision: '需要决定', result: '结果', progress: '进行中', meeting: '会议' };
    const briefRows = b.items.map(it => `
      <div class="row" data-action="${it.kind === 'decision' ? 'open-decision' : it.kind === 'result' ? 'open-result' : it.kind === 'progress' ? 'open-work' : 'open-meeting'}" data-arg="${it.go.split('/').pop()}">
        <span class="tag" style="min-width:56px;justify-content:center">${kindName[it.kind]}</span>
        <span class="grow"><div class="title">${it.title}</div><div class="meta">${it.who} · ${it.why}</div></span>
        <span class="end">${ico(I.chev, 14)}</span>
      </div>`).join('');
    const running = b.running.map(r => C.workCard(FX.work(r.w))).join('');
    const latest = FX.results.slice(0, 3).map(C.resultCard).join('');
    const states = {
      normal: { brief: briefRows },
      emptyFirst: {
        brief: '', empty: C.emptyState('这里是你的 CEO 工作台', '完成公司创建后，简报、需要你决定的事项和最新结果会出现在这里。',
          [{ t: '创建第一个业务', action: 'go', arg: '#/business' }, { t: '把意图交给空间工程部', action: 'go', arg: '#/business/biz-new' }],
          '<button class="btn primary" data-action="go" data-arg="#/business">开始创建公司</button>'),
      },
      needsCEO: { brief: briefRows, banner: C.decisionBanner(FX.decisions[0]) },
      error: { brief: briefRows, error: true },
    };
    return {
      crumbs: C.crumbs([{ t: 'Curis' }, { t: 'CEO 工作台' }]),
      states,
      html: (s) => `
        <div class="page-head"><h1>今日经营</h1><div class="sub">${b.date} · 简报只呈现需要你注意的事，全部有事实来源</div></div>
        ${s.error ? `<div class="error-banner" style="margin-bottom:16px"><div class="eb-title">简报同步失败</div><div class="eb-body">无法获取最新运行数据（网络原因）。其余区域数据为本机缓存。</div><div class="decision-actions"><button class="btn sm primary">重试</button><button class="btn sm ghost">使用缓存</button></div></div>` : ''}
        ${s.banner || ''}
        <div class="section"><div class="section-head"><h2 class="section-title">今日简报</h2><span class="section-more">按影响排序 · ${b.items.length} 项</span></div>
          ${s.empty ? s.empty : `<div class="rowlist">${s.brief}</div>`}</div>
        <div class="section"><div class="section-head"><h2 class="section-title">正在运行</h2><span class="section-more">${b.running.length} 个工作 · ${new Set(b.running.map(r => FX.work(r.w).employee)).size} 位员工</span></div>
          <div class="grid c2">${running}</div></div>
        <div class="section"><div class="section-head"><h2 class="section-title">最新结果</h2><a class="section-more" href="#/results">成果库 →</a></div>
          <div class="rowlist">${latest}</div></div>
        <div class="section"><div class="section-head"><h2 class="section-title">公司脉搏</h2><span class="section-more">次级信息 · 点击展开</span></div>
          <div class="rowlist">
            ${[['价值','两条主线：内容获客（增长验证中）、产品交付（v1.4 联调）'],['执行','3 个工作运行中 · 1 个阻塞待你'],['供给','模型用量 54% / 预算 · 连接器 2 个待授权'],['风险','825 选题合规边界（今日内）'],['方向','行业洞察新业务激活建议将在下午提交'],['连续性','周报已归档 · 上周决议 2 项已闭环']].map(r => `
              <div class="row"><span style="flex:0 0 56px;font-weight:600">${r[0]}</span><span class="grow muted" style="font-size:13px">${r[1]}</span></div>`).join('')}
          </div></div>`,
    };
  };

  /* ---------- P5 组织中心 ---------- */
  V.org = function (params) {
    const tab = params.tab || 'map';
    const empRowFull = e => C.empRow(e, { openAction: 'open-employee' });
    /* Variant A · Department Container：Department 是容器，Business 是主要经营节点，人员渐进展开 */
    const mapHtml = FX.org.departments.map(d => {
      const members = FX.employees.filter(e => e.dept === d.name);
      const leader = FX.emp(d.leader);
      const bizs = (d.businesses || []).map(id => FX.biz(id)).filter(Boolean);
      const bizRows = bizs.length ? bizs.map(b => `
        <div class="row" data-action="go" data-arg="#/business/${b.id}">
          <span class="fc-ico">${ico(C.I.briefcase, 14)}</span>
          <span class="grow"><div class="title">${b.name}</div>
            <div class="meta">Business 负责人 ${FX.emp(b.leader).name} · ${(b.workspaces||[]).length} 个 Workspace · ${b.stage}</div></span>
          <span class="end">${ico(C.I.chev, 14)}</span></div>`).join('')
        : `<div class="row"><span class="grow muted" style="font-size:13px">${d.builtin ? '原装能力部门 · 不经营自有 Business；按需承接经营意图（如宠物寄养激活）' : '暂无 Business'}</span></div>`;
      return `<div class="section"><div class="section-head"><h2 class="section-title">${d.name}${d.builtin ? ' <span class="tag">原装</span>' : ''}</h2>
        <span class="section-more">Department Leader：${leader ? leader.name : '空缺'} · ${members.length} 名员工 · <a href="#" data-action="org-expand" data-arg="${d.id}">展开人员</a></span></div>
        <div class="rowlist">${bizRows}${d.id === 'dept-data' ? `<div class="row" data-action="go" data-arg="#/insights"><span class="fc-ico">${ico(C.I.chart, 14)}</span><span class="grow"><div class="title">经营洞察（司衡工作位）</div><div class="meta">公司级分析 · Decision support</div></span><span class="end">${ico(C.I.chev, 14)}</span></div>` : ''}</div>
        <div class="rowlist ${'org-members-' + d.id} hidden" style="margin-top:8px">${members.map(empRowFull).join('')}</div></div>`;
    }).join('');
    const dirHtml = `<div class="rowlist">${FX.employees.map(empRowFull).join('')}</div>`;
    return {
      crumbs: C.crumbs([{ t: 'Curis' }, { t: '组织中心' }]),
      html: `
        <div class="page-head" style="display:flex;align-items:flex-end;gap:16px">
          <div><h1>组织中心</h1><div class="sub">公司版图与员工目录 · 结构与行政视图（工作在业务空间内进行）</div></div>
          <span class="spacer"></span>
          <div class="segmented">
            <button class="${tab === 'map' ? 'active' : ''}" data-action="go" data-arg="#/org/map">公司版图</button>
            <button class="${tab === 'dir' ? 'active' : ''}" data-action="go" data-arg="#/org/dir">员工目录</button>
          </div>
        </div>
        ${tab === 'map' ? mapHtml : dirHtml}`,
    };
  };

  /* ---------- P6 Employee Workstation（Conversation-first；Detail 在 Utility） ---------- */
  window.EMP_PROFILE = function (e) {
    const myWorks = FX.works.filter(w => w.employee === e.id);
    const myResults = FX.results.filter(r => r.employee === e.id);
    return `
      <div style="display:flex;gap:10px;align-items:center;margin-bottom:10px">${C.avatar(e, 'lg')}
        <div><div style="font-weight:650">${e.name}</div><div class="muted" style="font-size:12px">${e.role} · ${e.dept}${e.leader ? ' · Leader' : ''}</div></div></div>
      <div class="dl-row"><span class="k">身份</span><span>Company Employee（canonical，非 Agent 配置）</span></div>
      <div class="dl-row"><span class="k">部门 / 角色</span><span>${e.dept} · ${e.role}</span></div>
      <div class="dl-row"><span class="k">长期责任</span><span>${e.responsibility.longTerm}</span></div>
      <div class="dl-row"><span class="k">当前责任</span><span>${e.responsibility.current}</span></div>
      <div class="dl-row"><span class="k">责任范围</span><span>${e.responsibility.scope}</span></div>
      <div class="dl-row"><span class="k">能力</span><span>${e.capability.map(c => `<span class="tag">${c}</span>`).join(' ')}</span></div>
      <div class="dl-row"><span class="k">Skill 绑定</span><span>${e.skills.map(sid => FX.skill(sid).name).join(' · ')}</span></div>
      <div class="dl-row"><span class="k">默认模型</span><span>${e.model}</span></div>
      <div class="dl-row"><span class="k">当前工作</span><span>${myWorks.filter(w => w.status === 'working').map(w => w.title).join('；') || '无运行中工作'}</span></div>
      <div class="dl-row"><span class="k">最近结果</span><span>${myResults.map(r => `<span class="result-ref" data-action="open-result" data-arg="${r.id}">${r.title}</span>`).join(' ') || '—'}</span></div>`;
  };
  V.employee = function (params) {
    const e = FX.emp(params.id) || FX.emp('e-zhen');
    const myWorks = FX.works.filter(w => w.employee === e.id);
    const myResults = FX.results.filter(r => r.employee === e.id);
    const section = params.sec || 'conv';
    const threadKey = 'emp:' + e.id;
    const tabs = [['conv', '对话'], ['work', '当前工作'], ['resp', '责任'], ['cap', '能力'], ['result', '结果'], ['set', '设置']];
    let body = '';
    if (section === 'conv') body = `
      <div class="conversation" id="emp-conv">${RT.renderThread(threadKey, { emptyTitle: `与 ${e.name} 开始协作`, emptySub: '对话锚定当前责任与工作；发送即进入处理，完成后 Result 引用会回到这里。' })}</div>
      ${RT.composer('c-' + threadKey, { thread: threadKey, placeholder: `与 ${e.name} 对话，或直接交代一件事…`, exec: `执行 · ${e.name}`, model: e.model })}`;
    if (section === 'work') body = myWorks.length
      ? `<div class="grid c2">${myWorks.map(w => C.workCard(w)).join('')}</div>`
      : C.emptyState('当前没有运行中的工作', '可以派一件新工作，或从对话里直接交代。', [], '<button class="btn primary" data-action="go" data-arg="#/employee/' + e.id + '/conv">去对话交代</button>');
    if (section === 'resp') body = `
      <div class="card"><div class="dl-row"><span class="k">长期责任</span><span class="grow">${e.responsibility.longTerm}</span></div>
      <div class="dl-row"><span class="k">当前责任</span><span class="grow">${e.responsibility.current}</span></div>
      <div class="dl-row"><span class="k">责任范围（Scope）</span><span>${e.responsibility.scope}</span></div></div>`;
    if (section === 'cap') body = `
      <div class="card" style="margin-bottom:12px"><div class="section-title" style="margin-bottom:8px">能力（用户语言）</div>
        ${e.capability.map(c => `<span class="tag" style="margin:0 6px 6px 0">${c}</span>`).join('')}</div>
      <div class="section-title" style="margin:0 0 8px">Skill 绑定</div>
      <div class="rowlist">${e.skills.map(sid => { const sk = FX.skill(sid); return `<div class="row"><span class="grow"><div class="title">${sk.name}</div><div class="meta">${sk.publisher} · ${sk.type} · ${sk.perm}</div></span><span class="end"><a href="#/skill/${sk.id}">详情</a></span></div>`; }).join('')}</div>
      <div class="hr"></div>
      <div class="dl-row"><span class="k">默认模型</span><span>${e.model}</span><button class="btn sm" data-action="go" data-arg="#/models">在模型配置中管理</button></div>`;
    if (section === 'result') body = myResults.length
      ? `<div class="rowlist">${myResults.map(r => `<div class="row" data-action="open-result" data-arg="${r.id}"><span class="grow"><div class="title">${r.title}</div><div class="meta">证据 ${r.evidence.length} 条 · 被引用 ${r.usedBy.length} 处</div></span><span class="end">${C.statusMeta(r.status)[1]}</span></div>`).join('')}</div>`
      : C.emptyState('还没有产出结果', '结果会在工作完成后出现在这里，并附证据链。');
    if (section === 'set') body = `
      <div class="card"><div class="dl-row"><span class="k">默认模型</span><span>${e.model}</span><span class="switch on"><i></i></span></div>
      <div class="dl-row"><span class="k">执行授权</span><span>最小权限（写操作需 CEO 确认）</span><button class="btn sm" data-action="go" data-arg="#/settings/permissions">调整</button></div>
      <div class="dl-row"><span class="k">完成通知</span><span class="switch on"><i></i></span></div>
      <div class="dl-row"><span class="k">阻塞升级</span><span class="switch on"><i></i></span></div></div>`;
    return {
      crumbs: C.crumbs([{ t: '组织中心', go: '/org/dir' }, { t: e.dept }, { t: e.name }]),
      ctxTitle: '工作范围',
      /* Context 只承载 bounded navigation，不放完整档案（完整档案在 Utility） */
      ctxHtml: `<div class="nav-group">当前工作范围</div>
        ${myWorks.map(w => `<button class="nav-item ${w.status === 'working' ? 'active' : ''}" data-action="open-work" data-arg="${w.id}">${w.title}</button>`).join('') || `<div class="faint" style="padding:4px 8px;font-size:12px">暂无运行中工作</div>`}
        <div class="nav-group">相关结果</div>
        ${myResults.slice(0, 3).map(r => `<button class="nav-item" data-action="open-result" data-arg="${r.id}">${r.title}</button>`).join('')}
`,
      util: { title: '员工档案', tabs: ['档案'], active: '档案', html: EMP_PROFILE(e) },
      html: `
        <div class="page-head" style="display:flex;gap:14px;align-items:center">
          <span data-action="emp-util" data-arg="${e.id}" style="cursor:pointer" title="打开完整档案（Utility）">${C.avatar(e, 'lg')}</span>
          <div><h1>${e.name}</h1><div class="sub">${e.role} · ${e.dept} ${e.leader ? '· <b style="color:var(--ui-accent)">Leader</b>' : ''} · ${C.stFull(e)}</div></div>
          <span class="spacer"></span>
          <button class="btn primary" data-action="go" data-arg="#/employee/${e.id}/conv">进入对话</button>
        </div>
        <div class="tabs" style="margin-bottom:16px">${tabs.map(t => `<button class="tab ${section === t[0] ? 'active' : ''}" data-action="emp-tab" data-arg="${t[0]}">${t[1]}</button>`).join('')}</div>
        ${body}`,
    };
  };

  /* ---------- P7 人才与能力（人才市场：发现和扩展公司外部能力） ---------- */
  const EXPERTS = [
    { id:'x-growth', name:'增长运营专家', src:'curis', tag:'Curis-ready', desc:'Curis 官方 EmployeeTemplate：内容获客节奏与转化复盘。', caps:['内容策略','增长判断'], ver:'v1.0 · 官方' },
    { id:'x-data', name:'数据分析师', src:'curis', tag:'Curis-ready', desc:'Curis 官方 EmployeeTemplate：经营数据清洗、看板与周报。', caps:['数据分析','报表'], ver:'v1.2 · 官方' },
    { id:'x-doc', name:'长文写作专家', src:'curis', tag:'Curis-ready', desc:'Curis 官方 EmployeeTemplate：长结构文档撰写与改稿。', caps:['写作','编辑'], ver:'v1.0 · 官方' },
    { id:'x-seo', name:'SEO 内容专家', src:'ext', tag:'外部 Candidate', desc:'来源：agency-agents-zh · 固定版本 + 文件摘要校验后可招募。', caps:['SEO','关键词'], ver:'r4 · 外部' },
    { id:'x-ops', name:'电商运营专家', src:'ext', tag:'外部 Candidate', desc:'来源：外部 Candidate 包 · 待安装验证（不可直接执行）。', caps:['电商','选品'], ver:'r7 · 外部' },
    { id:'x-qa', name:'测试工程师', src:'ext', tag:'外部 Candidate', desc:'来源：外部 Candidate 包 · 许可证复核中。', caps:['测试','用例'], ver:'r2 · 外部' },
  ];
  V.talent = function (params) {
    const tab = params.tab || 'exp';
    const q = (typeof params.q === 'string' ? params.q : (params.q && params.q.q) || '').toLowerCase();
    const cat = params.cat || (params.q && params.q.cat) || '全部';
    let items, cardFn, cats, featured;
    if (tab === 'skill') {
      cats = ['全部', '方法', '工具', '能力', '社区精选'];
      items = FX.skills.filter(s => (cat === '全部' || s.type === cat || (cat === '社区精选' && s.source === 'community')) && (!q || s.name.toLowerCase().includes(q) || s.desc.includes(q)));
      cardFn = s => `
        <div class="sk-card">
          <div class="sk-head"><span class="sk-ico ${s.installed ? 'av-2' : 'av-7'}">${s.type === '工具' ? 'T' : s.type === '方法' ? 'M' : 'C'}</span>
            <div class="sk-name">${s.name}</div><span class="spacer"></span>
            <button class="btn sm ${s.installed ? '' : 'primary'}" data-action="install-skill" data-arg="${s.id}">${s.installed ? '已安装' : '+ 安装'}</button></div>
          <div class="sk-desc">${s.desc}</div>
          <div class="sk-meta">${s.publisher} · ${s.perm} · 绑定 ${s.bound.length} 人</div>
        </div>`;
      featured = FX.skills.filter(s => s.source === 'official').slice(0, 3);
    } else if (tab === 'conn') {
      cats = ['全部', '已连接', '需授权', '未连接'];
      items = FX.connectors;
      cardFn = c => `
        <div class="card talent-card">
          <div class="tc-head"><span class="avatar sm ${c.status === 'connected' ? 'av-2' : c.status === 'needs-auth' ? 'av-3' : 'av-7'}">${c.name[0]}</span>
            <div style="min-width:0"><div class="tc-name">${c.name}</div><div class="tc-sub">${c.status === 'connected' ? '已连接' : c.status === 'needs-auth' ? '需要授权' : '未连接'}</div></div>
            <span class="spacer"></span>
            <button class="btn sm ${c.status === 'connected' ? '' : 'primary'}" data-action="noop">${c.status === 'connected' ? '管理' : c.status === 'needs-auth' ? '去授权' : '连接'}</button></div>
          <div class="tc-desc">${c.desc}</div>
          <div class="tc-foot"><span class="tag">范围：${c.scope}</span></div>
        </div>`;
      featured = [];
    } else {
      cats = ['全部', 'Curis-ready', '外部 Candidate'];
      items = EXPERTS.filter(x => (cat === '全部' || x.tag === cat) && (!q || x.name.includes(q) || x.desc.includes(q) || x.caps.join().includes(q)));
      cardFn = x => `
        <div class="xb-card" data-action="noop">
          <div class="xb-head"><span class="xb-av ${x.src === 'curis' ? 'av-2' : 'av-3'}">${x.name[0]}</span>
            <div class="xb-id"><div class="xb-name">${x.name}</div><div class="xb-sub">${x.src === 'curis' ? 'Curis 官方' : '外部来源'}</div></div></div>
          <div class="xb-desc">${x.desc}</div>
          <div class="xb-tags">${x.caps.slice(0, 3).map(c => `<span class="tag">${c}</span>`).join('')}</div>
          <div class="xb-foot"><span class="xb-ver">${x.ver}</span><span class="spacer"></span>
            <button class="btn sm ${x.src === 'curis' ? 'primary' : ''}" data-action="noop">${x.src === 'curis' ? '招募装配' : '安装验证'}</button></div>
        </div>`;
      featured = EXPERTS.filter(x => x.src === 'curis');
    }
    const featuredTitle = tab === 'exp' ? 'Curis-ready（官方模板，可直接招募装配）' : '精选';
    const featuredHtml = featured.length && cat === '全部' && !q ? `
      <div class="section"><div class="section-head"><h2 class="section-title">${featuredTitle}</h2>
        <button class="section-more" data-action="talent-refresh">换一换</button></div>
        <div class="grid c4">${featured.map(cardFn).join('')}</div></div>` : '';
    return {
      crumbs: C.crumbs([{ t: 'Curis' }, { t: '人才与能力' }]),
      html: `
        <div class="page-head" style="display:flex;align-items:center;gap:12px;flex-wrap:wrap">
          <div><h1>人才与能力</h1><div class="sub">发现和扩展公司外部能力：专家招募 · 技能安装 · 连接器（公司内部员工在 组织中心 → 员工目录）</div></div>
          <span class="spacer"></span>
          <div class="segmented">
            <button class="${tab === 'exp' ? 'active' : ''}" data-action="talent-tab" data-arg="exp">专家</button>
            <button class="${tab === 'skill' ? 'active' : ''}" data-action="talent-tab" data-arg="skill">技能</button>
            <button class="${tab === 'conn' ? 'active' : ''}" data-action="talent-tab" data-arg="conn">连接器</button>
          </div>
          <input class="input" style="width:220px" placeholder="搜索专家 / 技能 / 连接器" value="${typeof params.q === 'string' ? params.q : ''}" data-action="talent-search">
        </div>
        ${featuredHtml}
        <div class="section">
          <div class="section-head"><div class="chip-row">
            <span class="chip active">${cat}</span>
            ${cats.filter(c => c !== cat).map(c => `<span class="chip clickable" data-action="talent-cat" data-arg="${c}">${c}</span>`).join('')}
          </div><span class="spacer"></span>
            <div class="segmented"><button class="active">综合</button><button>最热</button><button>最新</button></div></div>
          <div class="grid c3" style="margin-top:12px">${(() => {
              const featIds = (featured.length && cat === '全部' && !q) ? featured.map(x => x.id || x.name) : [];
              const visible = items.filter(x => !featIds.includes(x.id || x.name));
              return visible.map(cardFn).join('') || (items.length ? '<div class="faint" style="padding:12px;font-size:12px">以上即全部条目</div>' : C.emptyState('没有匹配项', '换一个筛选条件，或清空搜索。'));
            })()}</div>
        </div>
        <div class="faint" style="font-size:11px;margin-top:8px">外部 Candidate 需固定版本、文件摘要与逐项安装验证后才可转为可招募（TALENT_MARKET 边界）；安装连接器后去设置完成授权。</div>`,
    };
  };

  V.skill = function (params) {
    const s = FX.skill(params.id) || FX.skills[0];
    return {
      crumbs: C.crumbs([{ t: '人才与能力', go: '/talent/skill' }, { t: '技能' }, { t: s.name }]),
      util: { title: '绑定员工', html: `<div class="rowlist">${s.bound.map(id => { const e = FX.emp(id); return `<div class="row" data-action="open-employee" data-arg="${id}">${C.avatar(e, 'sm')}<span class="grow"><div class="title">${e.name}</div><div class="meta">${e.role}</div></span><span class="end">${C.ico(C.I.chev, 14)}</span></div>`; }).join('')}</div>` },
      html: `
        <div class="page-head" style="display:flex;gap:14px;align-items:center">
          <span class="avatar lg ${s.installed ? 'av-2' : 'av-7'}">${s.name[0]}</span>
          <div><h1>${s.name}</h1><div class="sub">${s.publisher} · ${s.type} · ${s.source === 'community' ? '社区来源' : '官方'} · ${s.perm}</div></div>
          <span class="spacer"></span>
          <button class="btn ${s.installed ? '' : 'primary'}" data-action="install-skill" data-arg="${s.id}">${s.installed ? '已安装 · 管理' : '安装'}</button>
        </div>
        <div class="section"><div class="section-title" style="margin-bottom:6px">它会做什么（用户语言）</div>
          <div class="card" style="font-size:14px;color:var(--ui-text-2)">${s.desc}</div></div>
        <div class="section"><div class="section-title" style="margin-bottom:6px">什么时候会被用到（触发方式）</div>
          <div class="card" style="font-size:14px;color:var(--ui-text-2)">当工作内容与「${s.type}」相关时，绑定员工可在执行中调用；对话中也可用 /${s.name} 显式调用。</div></div>
        <div class="section"><div class="section-title" style="margin-bottom:6px">权限</div>
          <div class="card"><div class="dl-row"><span class="k">使用范围</span><span>${s.perm}</span></div>
          <div class="dl-row"><span class="k">数据边界</span><span>只读公司资料 · 不外发</span></div></div></div>
        <div class="section"><div class="section-title" style="margin-bottom:6px">已绑定员工（${s.bound.length}）</div>
          <div class="rowlist">${s.bound.map(id => { const e = FX.emp(id); return `<div class="row" data-action="open-employee" data-arg="${id}">${C.avatar(e, 'sm')}<span class="grow"><div class="title">${e.name}</div><div class="meta">${e.role} · ${e.dept}</div></span><button class="btn sm ghost">解绑</button></div>`; }).join('')}</div></div>`,
    };
  };

  /* ---------- P11 经营洞察 ---------- */
  V.insights = function () {
    return {
      crumbs: C.crumbs([{ t: 'Curis' }, { t: '经营洞察' }]),
      util: { title: '报告 · 九月第二周', html: `<div class="doc-preview"><h3>经营周报（摘要）</h3><p>内容获客：关注转化验证中，825 图文今日发布。</p><p>产品交付：登录模块 v1.3 联调通过；v1.4 进入回归。</p><p>建议：批准 825 语气方案 A，以保证今日发布。</p><div class="hr"></div><span class="result-ref" data-action="open-result" data-arg="r-weekly">查看完整报告（附证据）</span></div>` },
      html: `
        <div class="page-head"><h1>经营洞察</h1><div class="sub">司衡 · 公司经营分析师 · 消费唯一经营数据，不产生第二套 Truth</div></div>
        ${C.decisionBanner({ id: 'd-weekly', title: '周报建议：批准 825 教程向发布', body: '教程向互动中位数高 34%（EST）；建议本篇教程向、9/19 复测后固化规则。', options: ['采纳并转给陈真', '我再想想'] })}
        <div class="section"><div class="section-head"><h2 class="section-title">互动趋势（7 天 · EST）</h2><span class="section-more">数据含 provenance · Connector 对账前为估算</span></div>
          <div class="card">${C.lineChart([{k:'9/6',v:1200},{k:'9/7',v:1500},{k:'9/8',v:1350},{k:'9/9',v:1800},{k:'9/10',v:2400},{k:'9/11',v:2100},{k:'9/12',v:2650}])}</div></div>
        <div class="section"><div class="section-head"><h2 class="section-title">渠道贡献（近 7 天互动）</h2></div>
          <div class="card">${C.bars([['AI 科技',1100,'1.1k'],['抖音',180,'180 · 无回执'],['公众号',0,'未连接']])}</div></div>
        <div class="section"><div class="section-head"><h2 class="section-title">分析师洞察</h2><span class="section-more">每条附证据引用</span></div>
          <div class="rowlist">
            <div class="row"><span class="grow"><div class="title">「教程 + 工具清单」组合互动中位数高 34%</div><div class="meta">证据：竞品选题结构周报（8/12–8/19）· 120 篇样本</div></span><button class="btn sm" data-action="go" data-arg="#/knowledge/k-2">来源</button></div>
            <div class="row"><span class="grow"><div class="title">抖音渠道无回执：连接器需授权，当前为人工填报（EST）</div><div class="meta">证据：连接器状态 · 授权记录缺失</div></span><button class="btn sm" data-action="open-decision" data-arg="d-connector">去授权</button></div>
          </div></div>
        <div class="section"><div class="section-head"><h2 class="section-title">关键指标（7 天 · 同口径对比上周）</h2></div>
          <div class="kpi-row" style="margin-bottom:12px">
            <div class="kpi"><div class="n">3 篇</div><div class="l">本周发布 · +1</div></div>
            <div class="kpi"><div class="n">1,842</div><div class="l">评论抽样分析</div></div>
            <div class="kpi"><div class="n">v1.3</div><div class="l">研发联调基线</div></div>
            <div class="kpi"><div class="n">54%</div><div class="l">模型预算已用</div></div>
          </div>
          <div class="rowlist">
            <div class="row"><span class="grow"><div class="title">内容获客线：关注转化验证中</div><div class="meta">证据：3 篇已发布内容数据 · 李然/林月研究简报</div></span><span class="end">增长验证中</span></div>
            <div class="row"><span class="grow"><div class="title">产品交付线：v1.4 回归准备</div><div class="meta">证据：登录模块 v1.3 联调记录 · 单测 22 passed / 0 failed</div></span><span class="end">正常</span></div>
          </div></div>`,
    };
  };

  /* ---------- P9 资料库 ---------- */  /* ---------- P9 资料库 ---------- */
  V.knowledge = function (params) {
    const id = params.id;
    if (id) {
      const k = FX.knowledge.find(x => x.id === id) || FX.knowledge[0];
      return {
        crumbs: C.crumbs([{ t: '资料库', go: '/knowledge' }, { t: k.title }]),
        util: { title: '被引用', html: `<div class="rowlist">${k.usedBy.map(u => `<div class="row"><span class="grow"><div class="title">${u}</div><div class="meta">Work / Result 引用</div></span></div>`).join('')}</div>` },
        html: `
          <div class="page-head"><h1>${k.title}</h1><div class="sub">${k.scope} · 更新 ${k.updated} · 来源：${k.source}</div></div>
          <div class="doc-preview"><h3>内容摘要</h3><p>（阅读视图）本资料为 ${k.scope} 引用来源。AI 只能引用有来源、权限范围内的资料；引用会保留来源与版本。</p>
          <p>资料更新后，旧产出不会被静默改写；下一次运行会标注版本变化并请求复核。</p></div>
          <div class="section" style="margin-top:16px"><div class="section-title" style="margin-bottom:6px">使用方式</div>
          <div class="card muted" style="font-size:13px">在业务空间的对话或工作中选择知识范围 → 引用会带入当前步骤，并保留原始链接。</div></div>`,
      };
    }
    return {
      crumbs: C.crumbs([{ t: 'Curis' }, { t: '资料库' }]),
      html: `
        <div class="page-head" style="display:flex;align-items:center"><div><h1>资料库</h1><div class="sub">公司引用空间 · AI 只引用有来源、权限范围内的资料</div></div>
          <span class="spacer"></span><button class="btn">导入资料</button><button class="btn primary">连接外部来源</button></div>
        <div class="section"><div class="chip-row">
          <span class="chip active">全部</span><span class="chip clickable">公司级</span><span class="chip clickable">业务范围</span><span class="chip clickable">文档</span><span class="chip clickable">表格</span>
        </div></div>
        <div class="rowlist">
          ${FX.knowledge.map(k => `<div class="row" data-action="go" data-arg="#/knowledge/${k.id}">
            <span class="fc-ico">${k.type === 'doc' ? 'DOC' : 'XLSX'}</span>
            <span class="grow"><div class="title">${k.title}</div><div class="meta">${k.scope} · 更新 ${k.updated} · 被 ${k.usedBy.length} 处引用</div></span>
            <span class="end">${k.source}</span></div>`).join('')}
        </div>`,
    };
  };

  /* ---------- P10 会议（Meeting Room：参与者/讨论/证据/Proposal→决议） ---------- */
  V.meeting = function (params) {
    const id = params.id;
    if (id) {
      const m = FX.meetings.find(x => x.id === id) || FX.meetings[0];
      const tk = 'meeting:' + m.id;
      if (!RT.S.threadSeeded[tk]) {
        RT.threadSeed(tk);
        RT.appendMsg(tk, { role: 'ai', emp: m.participants[0], text: '议程三项已就绪：①定位调整证据门槛 ②下周排期 ③归因结论确认。何川的归因数据已附在证据区。', model: 'GLM-5.3', cost: '◇ 0.6' });
        RT.appendMsg(tk, { role: 'user', text: '先看第一项。教程向的数据够不够下结论？' });
        RT.appendMsg(tk, { role: 'ai', emp: m.participants[3], text: '归因：教程向互动中位数高 34%（EST，样本 120 篇 + 1,842 条评论）。单看本周够方向性；建议本周教程向、下周复测一次再固化规则。', citations: ['选题研究简报', '竞品选题结构周报'], model: 'DeepSeek-V4.1', cost: '◇ 0.9' });
        RT.appendMsg(tk, { role: 'ai', emp: m.participants[0], text: 'Proposal：本篇按教程向发布，9/19 复盘后再定长期规则。请 CEO 确认。', model: 'GLM-5.3', cost: '◇ 0.4' });
      }
      return {
        crumbs: C.crumbs([{ t: '会议', go: '/meeting' }, { t: m.title }]),
        ctxTitle: '会议材料',
        ctxHtml: `<div class="nav-group">证据（会议引用）</div>
          ${['选题研究简报', '竞品选题结构周报', '上周发布数据'].map(k => `<button class="nav-item" data-action="go" data-arg="#/knowledge/k-2">${k}</button>`).join('')}
          <div class="nav-group">相关对象</div>
          ${m.related.map(r => { const w2 = FX.work(r); return w2 ? `<button class="nav-item" data-action="open-work" data-arg="${r}">${w2.title}</button>` : `<button class="nav-item" data-action="open-decision" data-arg="${r}">定位调整 Decision</button>`; }).join('')}`,
        util: { title: '决议与去向', tabs: ['决议'], active: '决议', html: `
          <div class="card" style="margin-bottom:10px"><div class="section-title" style="font-size:13px;margin-bottom:6px">Proposal（待 CEO 确认）</div>
            <div style="font-size:12.5px;color:var(--ui-text-2)">本篇按教程向发布；9/19 复盘后再定长期规则。</div>
            <div class="decision-actions" style="margin-top:8px"><button class="btn sm primary" data-action="noop">确认 Proposal</button><button class="btn sm" data-action="noop">修改</button></div></div>
          <div class="dl-row"><span class="k">决议→Work</span><span>确认后转 排期发布</span></div>
          <div class="dl-row"><span class="k">决议→资料</span><span>规则确认后沉淀公司记忆</span></div>` },
        html: `
          <div class="page-head" style="display:flex;align-items:center"><div><h1>${m.title}</h1>
            <div class="sub">${m.when} · ${m.status === 'done' ? '已结束' : '已排期'} · 议程 ${m.agenda.length} 项</div></div>
            <span class="spacer"></span><span class="chip">${m.participants.length} 人</span></div>
          <div class="section"><div class="section-head"><h2 class="section-title">参与者</h2></div>
            <div class="rowlist">${m.participants.map(p => { const pe = FX.emp(p); return `<div class="row" data-action="open-employee" data-arg="${p}">${C.avatar(pe, 'sm')}<span class="grow"><div class="title">${pe.name}</div><div class="meta">${pe.role} · ${C.stFull(pe)}</div></span></div>`; }).join('')}</div></div>
          <div class="section"><div class="section-head"><h2 class="section-title">讨论</h2><span class="section-more">员工准备背景与事实 · CEO 确认承诺与决议</span></div>
            <div class="conversation" style="margin:0">${RT.renderThread(tk)}</div>
            ${RT.composer('c-' + tk, { thread: tk, placeholder: '在会议中发言或追问…', exec: '执行 · 会议', model: 'GLM-5.3' })}</div>`,
      };
    }
    return {
      crumbs: C.crumbs([{ t: 'Curis' }, { t: '会议' }]),
      html: `
        <div class="page-head" style="display:flex;align-items:center"><div><h1>会议</h1><div class="sub">把必须讨论的事留在一圈有边界的对话里：员工准备背景与事实，CEO 确认承诺与决议</div></div>
        <span class="spacer"></span><button class="btn primary" data-action="noop">发起会议</button></div>
        <div class="rowlist">
          ${FX.meetings.map(m => `<div class="row" data-action="go" data-arg="#/meeting/${m.id}">
            ${C.st(m.status)}
            <span class="grow"><div class="title">${m.title}</div><div class="meta">${m.when} · ${m.participants.length} 人 · 议程 ${m.agenda.length} 项</div></span>
            <span class="end">${ico(C.I.chev, 14)}</span></div>`).join('')}
        </div>`,
    };
  };

  /* ---------- P12 Settings ---------- */
  V.settings = function (params) {
    const sec = params.sec || 'personal';
    const q = typeof params.q === 'string' ? params.q : (params.q && params.q.q) || '';
    const nav = [
      ['personal', '个人偏好'], ['company', '公司设置'], ['models', '模型'], ['providers', 'Provider 与凭据'],
      ['skills', '技能'], ['mcp', 'MCP'], ['connectors', '连接器'], ['permissions', '权限与数据'],
      ['memory', '记忆'], ['usage', '运行与成本'], ['notifications', '通知'], ['appearance', '外观'],
      ['shortcuts', '快捷键'], ['about', '关于'],
    ];
    let body = '';
    const dl = rows => `<div class="card">${rows.map(r => `<div class="dl-row"><span class="k">${r[0]}</span><span class="grow">${r[1]}</span>${r[2] || ''}</div>`).join('')}</div>`;
    if (sec === 'personal') body = `
      <div class="card" style="max-width:520px">
        <div class="field"><span class="f-label">显示名</span><input class="input" value="CEO"></div>
        <div class="field"><span class="f-label">语言</span><input class="input" value="简体中文"></div>
        <div class="field"><span class="f-label">启动页</span><input class="input" value="CEO 工作台"></div>
        <button class="btn primary sm" data-action="settings-save">保存</button><span class="faint" style="margin-left:8px;font-size:11px">DESIGN FIXTURE · 本地草稿态</span>
      </div>`;
    if (sec === 'company') body = dl([['公司名称', FX.org.company], ['行业', '空间设计 / AI 服务'], ['品牌主题', '跟随系统'], ['管理员', 'CEO（你）']]);
    if (sec === 'models') body = `
      <div class="rowlist">${[['GLM-5.3', '已连接 · 默认 · 视觉/推理', true], ['DeepSeek-V4.1', '已连接 · 员工默认可切换', true], ['GPT 系列', '未配置 Endpoint', false]].map(m => `
        <div class="row"><span class="grow"><div class="title">${m[0]}</div><div class="meta">${m[1]}</div></span>
        <span class="switch ${m[2] ? 'on' : ''}"><i></i></span></div>`).join('')}</div>
      <div class="faint" style="margin-top:8px;font-size:11px">每员工默认模型在 员工详情 → 能力 中设置。</div>`;
    if (sec === 'providers') body = dl([
      ['内置网关', '已连接 · 健康检查通过 · Keychain 保管'],
      ['自定义 Provider', 'DeepSeek · Endpoint https://api.deepseek.com · <span class="dot ok"></span> 已连接'],
      ['新增 Provider', '<button class="btn sm">添加 Endpoint</button>'],
    ]);
    if (sec === 'skills') body = `<div class="rowlist">${FX.skills.map(s => `<div class="row"><span class="grow"><div class="title">${s.name}</div><div class="meta">${s.publisher} · ${s.type} · 绑定 ${s.bound.length} 人</div></span><a class="end" href="#/skill/${s.id}">详情</a></div>`).join('')}</div>`;
    if (sec === 'mcp') body = dl([
      ['company-docs (HTTP)', 'https://mcp.internal/docs · 已连接 · 工具 6 个'],
      ['fs-local (stdio)', '本地文件索引 · 已连接 · 工具 3 个'],
      ['添加 MCP Server', '<button class="btn sm">URL 或命令</button>'],
    ]);
    if (sec === 'connectors') body = `<div class="rowlist">${FX.connectors.map(c => `<div class="row"><span class="grow"><div class="title">${c.name}</div><div class="meta">${c.desc} · 范围：${c.scope}</div></span>${C.st(c.status === 'connected' ? 'done' : c.status === 'needs-auth' ? 'review' : 'idle')}</div>`).join('')}</div>`;
    if (sec === 'permissions') body = `
      <div class="card" style="margin-bottom:12px"><div class="section-title" style="margin-bottom:6px">执行授权档位（全员默认）</div>
        <div class="rowlist" style="border:0">
          <div class="row"><span class="grow"><div class="title">最小权限（当前）</div><div class="meta">读公司资料可用；写操作与外发需 CEO 确认</div></span><span class="dot ok"></span></div>
          <div class="row"><span class="grow"><div class="title">按白名单放行</div><div class="meta">自然语言规则：如「允许只读外部网页检索」</div></span><span class="dot idle"></span></div>
          <div class="row"><span class="grow"><div class="title">完全访问</div><div class="meta">不推荐：所有工具自动放行并留审计</div></span><span class="dot idle"></span></div>
        </div></div>
      ${dl([['高危动作阈值', '批量删除 > 50 条需 CEO 批准'], ['升级规则', '超出责任范围 → 通知 CEO（含 IM 渠道）'], ['审计', '所有放行/拦截留痕，可导出'], ['数据隔离', 'Company / Department / Business / Workspace 四层 Scope 隔离（Curis 唯一 Usage Ledger 同源）']])}`;
    if (sec === 'memory') body = `
      <div class="card" style="margin-bottom:12px"><div class="section-title" style="margin-bottom:6px">公司记忆（可逐条查看与编辑）</div>
        <div class="rowlist" style="border:0">
          <div class="row"><span class="grow"><div class="title">品牌语气：克制、事实先于观点</div><div class="meta">来源：品牌表达手册 v2 · 9/02 更新</div></span><button class="btn sm ghost">编辑</button></div>
          <div class="row"><span class="grow"><div class="title">发布节奏：每周三 / 五</div><div class="meta">来源：沈书言 · 8/29 会议决议</div></span><button class="btn sm ghost">编辑</button></div>
          <div class="row"><span class="grow"><div class="title">研发发布窗口：周五</div><div class="meta">来源：825 会议（昨天）</div></span><button class="btn sm ghost">编辑</button></div>
        </div></div>
      ${dl([['记忆开关', '<span class="switch on"><i></i></span>'], ['敏感主题', '需逐条 opt-in，保存时通知你'], ['导出', '<button class="btn sm">导出全部记忆</button>']])}`;
    if (sec === 'usage') body = `
      <div class="kpi-row" style="margin-bottom:16px"><div class="kpi"><div class="n">${FX.usage.total}</div><div class="l">${FX.usage.month} 总消耗</div></div>
        <div class="kpi"><div class="n">${FX.usage.delta}</div><div class="l">对比上月同期</div></div>
        <div class="kpi"><div class="n">54%</div><div class="l">${FX.usage.budget}</div></div></div>
      <div class="section-title" style="margin-bottom:6px">按员工</div>
      <div class="rowlist" style="margin-bottom:16px">${FX.usage.byEmployee.map(r => `<div class="row" data-action="open-employee" data-arg="${FX.emp(r[0]) ? FX.emp(r[0]).id : ''}"><span class="grow"><div class="title">${r[0]}</div><div class="meta">${r[2]}</div></span><span class="end mono">${r[1]}</span></div>`).join('')}</div>
      <div class="section-title" style="margin-bottom:6px">按模型</div>
      <div class="rowlist">${FX.usage.byModel.map(r => `<div class="row"><span class="grow"><div class="title">${r[0]}</div></span><span class="end mono">${r[1]}</span></div>`).join('')}</div>`;
    if (sec === 'notifications') body = dl([
      ['结果就绪', '<span class="switch on"><i></i></span>'], ['需要我决定', '<span class="switch on"><i></i></span>'],
      ['员工阻塞', '<span class="switch on"><i></i></span>'], ['会议开始前 10 分钟', '<span class="switch on"><i></i></span>'],
      ['升级渠道', '系统通知 + IM（飞书 Webhook，DESIGN FIXTURE）'],
    ]);
    if (sec === 'appearance') body = dl([
      ['主题', '<div class="segmented"><button data-action="set-theme" data-arg="light">浅色</button><button data-action="set-theme" data-arg="dark">深色</button><button data-action="set-theme" data-arg="system">跟随系统</button></div>'],
      ['信息密度', '安静高密度（Frozen 纪律）'], ['字号下限', '12px'],
    ]);
    if (sec === 'shortcuts') body = dl([['全局搜索', '⌘ K'], ['全局助理', '⌘ J'], ['会话内搜索', '⌘ F'], ['收起/展开 Context', '⌘ \\']]);
    if (sec === 'about') body = dl([['版本', 'Prototype 0.1 · DESIGN FIXTURE'], ['更新渠道', '无（原型）'], ['原型说明', '本页为设计原型，不接 Runtime、不写任何真实数据']]);
    return {
      crumbs: C.crumbs([{ t: 'Curis' }, { t: '设置' }, { t: nav.find(n => n[0] === sec)[1] }]),
      html: `
        <div class="page-head"><h1>设置</h1><div class="sub">个人偏好 / 公司 / AI 与能力 / 权限与数据 / 运行与成本 分开管理</div></div>
        <div class="settings-wrap">
          <div>
            <input class="input" style="margin-bottom:8px" placeholder="搜索设置…" value="${q}" data-action="settings-search">
            <div class="settings-nav">${nav.filter(n => !q || n[1].includes(q)).map(n => `<button class="nav-item ${sec === n[0] ? 'active' : ''}" data-action="go" data-arg="#/settings/${n[0]}">${n[1]}</button>`).join('')}</div>
          </div>
          <div style="min-width:0">${body}</div>
        </div>`,
    };
  };
})();

  /* ---------- 模型配置（左下 CEO 头像菜单 → 模型配置 / AI 能力设置）---------- */
  const PROVIDERS = [
    ['OpenAI', 'api.openai.com', 'sk-…'], ['Anthropic', 'api.anthropic.com', 'sk-ant-…'],
    ['Gemini', 'generativelanguage.googleapis.com', 'AIza…'], ['DeepSeek', 'api.deepseek.com', 'sk-…（已连接）'],
    ['通义 Qwen', 'dashscope.aliyuncs.com', 'sk-…'], ['豆包', 'ark.cn-beijing.volces.com', '…'],
    ['智谱 GLM', 'open.bigmodel.cn', '…（已连接）'], ['MiniMax', 'api.minimaxi.com', '…'],
    ['Kimi', 'api.moonshot.cn', '…'], ['Mistral', 'api.mistral.ai', '…'],
    ['xAI', 'api.x.ai', '…'], ['Groq', 'api.groq.com', '…'], ['硅基流动', 'api.siliconflow.cn', '…'],
  ];
  V.models = function () {
    return {
      crumbs: C.crumbs([{ t: '模型配置 / AI 能力设置' }]),
      html: `
        <div class="page-head"><h1>模型配置</h1><div class="sub">主流厂商与模型已内置，填入 API Key 保存即可用（Key 存本机 Keychain）· 入口：左下角头像菜单</div></div>
        <div class="grid c3">
          ${PROVIDERS.map(p => {
            const ok = p[2].includes('已连接');
            return `<div class="card talent-card">
              <div class="tc-head"><span class="avatar sm ${ok ? 'av-2' : 'av-7'}">${p[0][0]}</span>
                <div style="min-width:0"><div class="tc-name">${p[0]}</div><div class="tc-sub">${p[1]}</div></div>
                <span class="spacer"></span>${ok ? '<span class="dot ok"></span>' : ''}</div>
              <div class="field" style="margin:8px 0 0"><input class="input" placeholder="API Key" value="${ok ? '••••••••（已保存）' : ''}"></div>
              <div class="tc-foot"><button class="btn sm ${ok ? '' : 'primary'}" data-action="noop">${ok ? '测试连接' : '保存并测试'}</button>
                <span class="faint" style="font-size:11px">${ok ? '启用 · 模型自动发现' : '未配置'}</span></div>
            </div>`; }).join('')}
        </div>
        <div class="section" style="margin-top:16px"><div class="section-title" style="margin-bottom:6px">高级 / 本地</div>
          <div class="rowlist">
            <div class="row"><span class="grow"><div class="title">聚合网关（OpenRouter / New API / OpenAI Compatible）</div><div class="meta">自定义 Base URL + Key</div></span><button class="btn sm" data-action="noop">添加</button></div>
            <div class="row"><span class="grow"><div class="title">本地模型（Ollama · 127.0.0.1:11434）</div><div class="meta">已发现 3 个模型</div></span><span class="switch on"><i></i></span></div>
          </div></div>
        <div class="faint" style="font-size:11px">模型在对话内随时切换（Composer 模型选择器）；创建 Employee 不要求逐个绑定模型。措辞消费 MODEL_PROVIDER_REGISTRY / EMPLOYEE_CONVERSATION_MODEL_EXPERIENCE_CONTRACT。</div>`,
    };
  };
