/* ============================================================
   Curis Full Product HTML Design Prototype — app.js
   Router / Four-Pane 管理 / 搜索 / 通知 / Floating CEO Assistant
   / State Switcher（设计测试工具）/ 事件委托
   ============================================================ */
(function () {
  const $ = s => document.querySelector(s);
  const app = $('#app');

  /* ---------- conversation demo state ---------- */
  const convState = {}; // routeKey -> messages appended at runtime

  /* ---------- router ---------- */
  const ROUTES = [
    [/^#?\/?$/, () => ({ page: 'ceo' })],
    [/^#\/ceo$/, () => ({ page: 'ceo' })],
    [/^#\/business$/, () => ({ page: 'business' })],
    [/^#\/business\/([\w-]+)$/, m => ({ page: 'businessDetail', id: m[1] })],
    [/^#\/activate$/, () => ({ page: 'activate' })],
    [/^#\/workspace\/([\w-]+)$/, m => ({ page: 'workspace', id: m[1] })],
    [/^#\/workspace\/([\w-]+)\/([\w-]+)$/, m => ({ page: 'workspace', id: m[1], surface: m[2] })],
    [/^#\/org(?:\/(\w+))?$/, m => ({ page: 'org', tab: m[1] || 'map' })],
    [/^#\/employee\/([\w-]+)$/, m => ({ page: 'employee', id: m[1] })],
    [/^#\/employee\/([\w-]+)\/(\w+)$/, m => ({ page: 'employee', id: m[1], sec: m[2] })],
    [/^#\/talent$/, () => ({ page: 'talent' })],
    [/^#\/talent\/(\w+)$/, m => ({ page: 'talent', tab: m[1] })],
    [/^#\/skill\/([\w-]+)$/, m => ({ page: 'skill', id: m[1] })],
    [/^#\/insights$/, () => ({ page: 'insights' })],
    [/^#\/knowledge$/, () => ({ page: 'knowledge' })],
    [/^#\/knowledge\/([\w-]+)$/, m => ({ page: 'knowledge', id: m[1] })],
    [/^#\/meeting$/, () => ({ page: 'meeting' })],
    [/^#\/meeting\/([\w-]+)$/, m => ({ page: 'meeting', id: m[1] })],
    [/^#\/settings(?:\/(\w+))?$/, m => ({ page: 'settings', sec: m[1] || 'personal' })],
    [/^#\/models$/, () => ({ page: 'models' })],
    [/^#\/work\/([\w-]+)$/, m => ({ page: 'work', id: m[1] })],
    [/^#\/decision\/([\w-]+)$/, m => ({ page: 'decision', id: m[1] })],
    [/^#\/decision\/([\w-]+)\/layer1$/, m => ({ page: 'decision', id: m[1], layer1: true })],
    [/^#\/result\/([\w-]+)$/, m => ({ page: 'result', id: m[1] })],
    [/^#\/results$/, () => ({ page: 'results' })],
    [/^#\/conversation\/([\w-]+)$/, m => ({ page: 'conversation', emp: m[1] })],
  ];
  function parse() {
    const raw = location.hash || '#/ceo';
    const [path, query] = raw.split('?');
    const q = {}; (query || '').split('&').filter(Boolean).forEach(kv => { const [k, v] = kv.split('='); q[k] = decodeURIComponent(v || ''); });
    for (const [re, fn] of ROUTES) { const m = path.match(re); if (m) { const r = fn(m); r.q = q; return r; } }
    return { page: 'ceo', q };
  }

  /* ---------- nav ---------- */
  function renderNav(route) {
    const items = [
      ['ceo', 'CEO 工作台', C.I.home, '#/ceo'],
      ['business', '业务空间', C.I.briefcase, '#/business'],
      ['org', '组织中心', C.I.org, '#/org'],
      ['talent', '人才与能力', C.I.users, '#/talent'],
      ['insights', '经营洞察', C.I.chart, '#/insights'],
      ['knowledge', '资料库', C.I.book, '#/knowledge'],
      ['meeting', '会议', C.I.video, '#/meeting'],
    ];
    /* Conversation Quick Access：与员工的直接对话常驻侧栏（不因离开页面而消失） */
    const convKeys = Object.keys(RT.S.threads).filter(k => k.startsWith('emp:'))
      .sort((a, b) => (RT.S.threadActive[b] || 0) - (RT.S.threadActive[a] || 0));
    const convIds = [...new Set(convKeys.map(k => k.slice(4)))];
    let html = '';
    for (const [id, t, ic, go] of items) {
      const active = route.page === id || (id === 'business' && ['businessDetail', 'workspace', 'activate', 'work', 'decision', 'result', 'results', 'conversation'].includes(route.page));
      html += `<button class="nav-item ${active ? 'active' : ''}" data-action="go" data-arg="${go}"><span class="ico" style="display:grid;place-items:center">${C.ico(ic, 18)}</span>${t}</button>`;
      if (id === 'business' && active) {
        html += `<div class="nav-children">` + Object.values(FX.businesses).map(b =>
          `<button class="nav-item ${route.id === b.id || (route.page === 'workspace' && FX.ws(route.id) && FX.ws(route.id).business === b.id) ? 'active' : ''}" data-action="go" data-arg="#/business/${b.id}">${b.name}</button>`).join('') + `</div>`;
      }
    }
    /* Quick Access：始终展示有对话的员工 + 各工作空间负责人（conversation-first 宿主） */
    const quick = [];
    for (const id of convIds) { const e = FX.emp(id); if (e) quick.push(e); }
    if (route.page === 'workspace' || quick.length === 0) {
      ['ws-cg', 'ws-rd'].forEach(wid => { const w = FX.ws(wid); if (w) quick.push(FX.emp(w.leader)); });
    }
    const seen = new Set();
    const quickList = quick.filter(e => e && !seen.has(e.id) && seen.add(e.id)).slice(0, 6);
    if (quickList.length) {
      html += `<div class="nav-group" style="margin-top:14px">对话 · Quick Access</div>`;
      html += quickList.map(e => {
        const st = e.status === 'working' ? 'run' : e.status === 'blocked' ? 'err' : 'idle';
        return `<button class="nav-item ${route.page === 'employee' && route.id === e.id ? 'active' : ''}" data-action="go" data-arg="#/employee/${e.id}/conv"><span class="dot ${st}" style="margin:0 2px"></span><span style="overflow:hidden;text-overflow:ellipsis">${e.name}</span><span class="faint" style="font-size:10.5px;margin-left:auto">${e.role.split(' / ')[0]}</span></button>`;
      }).join('');
    }
    html += `<div class="nav-spacer"></div>
      <div class="nav-user">
        <button class="nav-item" data-action="avatar-menu" style="gap:10px">
          ${C.avatar({ name: 'C', av: 7 }, 'sm')}
          <span style="display:flex;flex-direction:column;align-items:flex-start;line-height:1.25">
            <b style="font-size:12.5px">CEO</b>
            <span class="faint" style="font-size:10.5px">${FX.org.company}</span>
          </span>
        </button>
      </div>`;
    $('#nav-content').innerHTML = html;
  }

  /* ---------- render ---------- */
  const stateStore = {};
  const utilState = {};
  function render() {
    try { renderInner(); } catch (err) {
      console.error(err);
      $('#nav-content').innerHTML = '';
      $('#main-content').innerHTML = `<div class="error-banner"><div class="eb-title">原型渲染错误（DESIGN PROTOTYPE）</div>
        <div class="eb-body">${err.message}</div><pre class="mono" style="font-size:11px;white-space:pre-wrap">${(err.stack || '').split('\n').slice(0, 4).join('\n')}</pre></div>`;
    }
  }
  function renderInner() {
    const route = parse();
    if (route.q.util === '1') sessionStorage.setItem('util-open', '1');
    if (route.q.util === '0') sessionStorage.setItem('util-open', '0');
    const view = V[route.page](route);
    const key = location.hash || '#/ceo';
    const state = stateStore[key] || 'normal';
    renderNav(route);
    $('#main-crumbs').innerHTML = view.crumbs || '';
    const html = typeof view.html === 'function' ? view.html(view.states?.[state] || {}) : view.html;
    $('#main-content').innerHTML = html;
    $('#main-content').scrollTop = 0;
    /* context pane */
    const ctxOpen = !!view.ctxHtml && !sessionStorage.getItem('ctx-closed');
    $('#pane-context').classList.toggle('hidden', !ctxOpen);
    app.classList.toggle('has-context', ctxOpen);
    if (ctxOpen) { $('#ctx-crumbs').textContent = view.ctxTitle || '上下文'; $('#ctx-content').innerHTML = view.ctxHtml; }
    $('#btn-ctx-show').style.display = view.ctxHtml && !ctxOpen ? '' : 'none';
    /* utility pane */
    const utilOpen = (!!view.util && sessionStorage.getItem('util-open') === '1');
    $('#pane-utility').classList.toggle('hidden', !utilOpen);
    app.classList.toggle('has-utility', utilOpen);
    if (utilOpen && view.util) {
      const ustate = utilState[location.hash || '#/ceo'] || {};
      const tabs = view.util.tabs || ['面板'];
      const active = ustate.tab || view.util.active || tabs[0];
      const content = (view.util.content && view.util.content[active]) || view.util.html || '';
      $('#util-tabs').innerHTML = tabs.map(t =>
        `<button class="util-tab ${t === active ? 'active' : ''}" data-action="util-tab" data-arg="${t}">${t}</button>`).join('')
        + `<span class="faint" style="margin-left:6px;font-size:11px">${view.util.title || ''}</span>
           <button class="iconbtn" data-action="util-max" title="最大化（Esc 还原）">${C.ico(C.I.spark, 14)}</button>`;
      $('#util-content').innerHTML = content;
    }
    $('#btn-util').textContent = utilOpen ? '收 Utility' : 'Utility';
    /* state switcher */
    const ss = $('#ss-select');
    const states = Object.keys(view.states || {});
    if (states.length) {
      $('#state-switcher').style.display = '';
      ss.innerHTML = states.map(s => `<option value="${s}" ${s === state ? 'selected' : ''}>${s}</option>`).join('');
    } else { $('#state-switcher').style.display = 'none'; }
    renderAssistant();
    $('#global-status').innerHTML = state === 'error'
      ? '<span class="dot err"></span><span style="font-size:11px">同步失败</span>'
      : '<span class="dot ok"></span><span style="font-size:11px">已同步</span>';
  }

  /* ---------- search ---------- */
  function searchIndex() {
    const idx = [];
    FX.employees.forEach(e => idx.push({ type: '员工', t: e.name + ' · ' + e.role, go: '#/employee/' + e.id, m: e.dept, obj: { prev: [['部门', e.dept], ['状态', C.stFull(e)], ['当前责任', e.responsibility.current], ['能力', e.capability.join(' · ')]] } }));
    Object.values(FX.businesses).forEach(b => idx.push({ type: '业务', t: b.name, go: '#/business/' + b.id, m: b.dept }));
    Object.values(FX.workspaces).forEach(w => idx.push({ type: '空间', t: w.name, go: '#/workspace/' + w.id, m: w.domain }));
    FX.works.forEach(w => idx.push({ type: '工作', t: w.title, go: '#/work/' + w.id, m: C.statusMeta(w.status)[1], obj: { prev: [['谁在做', FX.emp(w.employee).name + ' · ' + FX.emp(w.employee).role], ['当前动作', w.current], ['进度', w.plan.filter(p => p.done).length + '/' + w.plan.length], ['用时 / 成本', w.elapsed + ' · ' + w.cost]] } }));
    FX.results.forEach(r => idx.push({ type: '结果', t: r.title, go: '#/result/' + r.id, m: r.evidence.length + ' 条证据', obj: { prev: [['负责人', FX.emp(r.employee).name], ['证据', r.evidence.length + ' 条'], ['被引用', r.usedBy.join(' · ')]] } }));
    FX.knowledge.forEach(k => idx.push({ type: '资料', t: k.title, go: '#/knowledge/' + k.id, m: k.scope }));
    FX.skills.forEach(s => idx.push({ type: '技能', t: s.name, go: '#/skill/' + s.id, m: s.publisher, obj: { prev: [['来源', s.publisher], ['类型', s.type], ['使用范围', s.perm], ['绑定', s.bound.length + ' 名员工']] } }));
    FX.meetings.forEach(m => idx.push({ type: '会议', t: m.title, go: '#/meeting/' + m.id, m: m.when }));
    FX.decisions.forEach(d => idx.push({ type: '决定', t: d.title, go: '#/decision/' + d.id, m: '待 CEO' }));
    return idx;
  }
  let searchSel = 0; let searchRows = [];
  const TYPE_ICON = { '员工': C.I.users, '业务': C.I.briefcase, '空间': C.I.org, '工作': C.I.spark, '结果': C.I.doc, '资料': C.I.book, '技能': C.I.gear, '会议': C.I.video, '决定': C.I.check };
  function openSearch() {
    const p = $('#search-panel');
    p.classList.remove('hidden');
    $('#overlay').classList.add('open');
    p.innerHTML = `
      <div class="sp-input">${C.ico(C.I.search, 18)}<input id="sp-q" placeholder="搜索员工、业务、工作、结果、资料…（⌘K）" autofocus></div>
      <div class="sp-filters">
        ${['全部', '员工', '业务', '空间', '工作', '结果', '资料'].map((f, i) => `<span class="chip ${i === 0 ? 'active' : ''} sp-f" data-f="${f}">${f}</span>`).join('')}
      </div>
      <div class="search-body"><div class="search-results" id="sp-results"></div><div class="search-preview" id="sp-preview"><span class="faint" style="font-size:12px">选择一个对象查看预览</span></div></div>`;
    const q = $('#sp-q');
    q.addEventListener('input', () => renderSearch(q.value, '全部'));
    p.querySelectorAll('.sp-f').forEach(c => c.addEventListener('click', () => {
      p.querySelectorAll('.sp-f').forEach(x => x.classList.remove('active')); c.classList.add('active');
      renderSearch(q.value, c.dataset.f);
    }));
    renderSearch('', '全部');
    q.focus();
  }
  function renderSearch(q, filter) {
    q = (q || '').toLowerCase();
    let rows = searchIndex().filter(r => !q || r.t.toLowerCase().includes(q) || r.m.toLowerCase().includes(q));
    if (filter !== '全部') rows = rows.filter(r => r.type === filter);
    searchRows = rows.slice(0, 24); searchSel = 0;
    $('#sp-results').innerHTML = searchRows.map((r, i) => `
      <div class="sp-row ${i === 0 ? 'sel' : ''}" data-go="${r.go}" data-i="${i}"><span class="type">${r.type}</span><span class="t">${r.t}</span><span class="m">${r.m}</span></div>`).join('') || '<span class="faint" style="padding:12px;font-size:12px">没有匹配结果</span>';
    $('#sp-results').querySelectorAll('.sp-row').forEach(el => {
      el.addEventListener('click', () => { location.hash = el.dataset.go; closeSearch(); });
      el.addEventListener('mouseenter', () => { searchSel = +el.dataset.i; markSel(); previewRow(searchRows[searchSel]); });
    });
    if (searchRows[0]) previewRow(searchRows[0]);
  }
  function markSel() {
    $('#sp-results').querySelectorAll('.sp-row').forEach(el => el.classList.toggle('sel', +el.dataset.i === searchSel));
    const sel = $('#sp-results').querySelector('.sp-row.sel');
    if (sel) sel.scrollIntoView({ block: 'nearest' });
  }
  function previewRow(r) {
    const obj = r && r.obj ? r.obj : null;
    const rows = obj ? obj.prev : [['类型', r.type], ['负责人 / 来源', r.m], ['状态', '见对象']];
    $('#sp-preview').innerHTML = `<div style="font-weight:650;margin-bottom:8px">${r.t}</div>
      ${rows.map(x => `<div class="dl-row" style="padding:6px 0"><span class="k" style="flex:0 0 84px">${x[0]}</span><span>${x[1]}</span></div>`).join('')}
      <div class="faint" style="margin-top:8px;font-size:11px">↑↓ 选择 · Enter 打开 · Esc 关闭</div>`;
  }
  function closeSearch() { $('#search-panel').classList.add('hidden'); $('#overlay').classList.remove('open'); }

  /* ---------- notifications ---------- */
  function toggleNotifications() {
    const p = $('#notif-panel');
    if (!p.classList.contains('hidden')) { p.classList.add('hidden'); $('#overlay').classList.remove('open'); return; }
    p.classList.remove('hidden'); $('#overlay').classList.add('open');
    const kindName = { result: '结果', decision: '需决定', blocked: '阻塞', meeting: '会议' };
    p.innerHTML = `<div style="padding:12px 14px;border-bottom:1px solid var(--ui-line);font-weight:650">通知</div>` +
      FX.notifications.map(n => `<div class="notif-item" data-action="go" data-arg="${n.go}" style="cursor:pointer">
        <span class="dot ${n.kind === 'result' ? 'ok' : n.kind === 'decision' ? 'warn' : n.kind === 'blocked' ? 'err' : 'idle'}" style="margin-top:5px"></span>
        <span><div class="n-title">${n.title}</div><div class="n-body">${n.body}</div></span><span class="n-time">${n.time}</span></div>`).join('');
  }

  /* ---------- floating CEO assistant ---------- */
  const asStates = ['collapsed', 'expanded', 'working', 'result-ready'];
  let asState = 'collapsed';
  function renderAssistant() {
    const a = $('#assistant');
    a.dataset.state = asState;
    a.className = 'assistant ' + (asState === 'collapsed' ? 'collapsed' : 'expanded');
    if (asState === 'collapsed') {
      a.innerHTML = `<button class="as-pill" data-action="as-expand"><span class="dot run"></span>CEO 助理 · 1 件需要你</button>`;
      return;
    }
    const cst = RT.S.composers['assistant'] || { status: 'idle' };
    const msgs = RT.renderThread('assistant');
    a.innerHTML = `
      <div class="as-head" id="as-drag">${C.avatar({ name: 'C', av: 7 }, 'sm')}
        <div><div class="as-name">CEO 助理</div><div class="as-sub">公司级 · 同一 canonical 身份 · 跨区可用</div></div>
        <span class="spacer"></span>
        ${cst.status === 'running' ? '<span class="status"><span class="dot run"></span>整理中…</span>' : ''}
        <button class="iconbtn" data-action="as-min" title="收起">${C.ico(C.I.minus, 14)}</button>
      </div>
      <div class="as-body">${msgs || C.emptyState('问我任何公司的事', '我会整理事实、风险和下一步；涉及执行或验收的，仍由你在业务现场确认。', [])}
      ${asState === 'working' ? '<div class="as-msg ai"><span class="skeleton" style="display:block;width:80%"></span><span class="skeleton" style="display:block;width:60%;margin-top:6px"></span></div>' : ''}
      ${asState === 'result-ready' ? `<div class="as-msg ai">登录模块 v1.3 已联调通过（附 3 条证据）。要现在查看，还是等 16:00 复盘会？<div style="margin-top:8px"><span class="result-ref" data-action="open-result" data-arg="r-login">查看结果</span></div></div>` : ''}</div>
      ${asState !== 'working' ? `<div class="as-suggest">${['把今天的阻塞列出来', '定位调整你建议选哪个？'].map(t => `<button data-rt="as-suggest-text" data-arg="${t}">${t}</button>`).join('')}</div>` : ''}
      <div class="as-composer">${RT.composer('assistant', { thread: 'assistant', placeholder: '问我任何公司的事…', exec: '执行 · CEO 助理' })}</div>`;
    a.querySelector('.as-body').scrollTop = 1e6;
  }
  function cycleAssistant(next) {
    asState = next || asStates[(asStates.indexOf(asState) + 1) % asStates.length];
    renderAssistant();
  }
  /* drag */
  (function enableDrag() {
    document.addEventListener('pointerdown', ev => {
      const head = ev.target.closest && ev.target.closest('#as-drag');
      if (!head) return;
      const a = $('#assistant');
      const r = a.getBoundingClientRect(), ox = ev.clientX - r.left, oy = ev.clientY - r.top;
      const move = e2 => {
        a.style.right = 'auto'; a.style.bottom = 'auto';
        a.style.left = Math.max(8, e2.clientX - ox) + 'px';
        a.style.top = Math.max(8, e2.clientY - oy) + 'px';
      };
      const up = () => { document.removeEventListener('pointermove', move); document.removeEventListener('pointerup', up); };
      document.addEventListener('pointermove', move); document.addEventListener('pointerup', up);
    });
  })();

  /* legacy composer interactions superseded by rt.js (handlers removed) */
  function composerSend(composerEl) {
    composerEl.dataset.running = '1';
    const bar = composerEl.querySelector('.cx-bar');
    bar.innerHTML = `<span class="status"><span class="dot run"></span>工作中 · 已排队</span><span class="spacer"></span><button class="cx-send stop" data-action="cx-stop" title="停止">${C.ico(C.I.stop, 14)}</button>`;
    setTimeout(() => {
      if (!composerEl.isConnected) return;
      composerEl.dataset.running = '';
      bar.innerHTML = `<span class="status"><span class="dot ok"></span>已发送 · 员工已开始（原型演示）</span>`;
      setTimeout(() => { if (composerEl.isConnected) render(); }, 1500);
    }, 2200);
  }

  /* ---------- event delegation ---------- */
  document.addEventListener('click', ev => {
    const rtEl = ev.target.closest('[data-rt="as-suggest-text"]');
    if (rtEl) {
      const st = RT.S.composers['assistant']; if (st) st.text = rtEl.dataset.arg;
      asState = 'expanded'; renderAssistant();
      const ta = document.querySelector('#assistant .cx-input'); if (ta) { ta.focus(); ta.selectionStart = ta.value.length; }
      return;
    }
    const el = ev.target.closest('[data-action]');
    if (!el) return;
    const act = el.dataset.action, arg = el.dataset.arg;
    const composerEl = el.closest('.composer');
    switch (act) {
      case 'go': location.hash = arg; break;
      case 'noop': break;
      case 'open-employee': location.hash = '#/employee/' + arg; break;
      case 'toggle-emp-conv': { const row = el.closest('.emp-row'); const conv = row && row.querySelector('.emp-conv');
        if (conv) { conv.classList.toggle('hidden'); row.classList.toggle('open'); const ta = conv.querySelector('.cx-input'); if (ta && !conv.classList.contains('hidden')) ta.focus(); }
        break; }
      case 'emp-util': { sessionStorage.setItem('util-open', '1');
        const route = parse(); const e = FX.emp(arg); route.id = arg; route.page = 'employee'; route.empId = arg;
        const v = V.employee(route);
        $('#util-tabs').innerHTML = `<span class="faint" style="font-size:11px">员工档案 · ${e.name}</span><button class="iconbtn" data-action="close-utility">${C.ico(C.I.x, 14)}</button>`;
        $('#util-content').innerHTML = EMP_PROFILE(e);
        $('#pane-utility').classList.remove('hidden'); app.classList.add('has-utility');
        $('#btn-util').textContent = '收 Utility'; break; }
      case 'open-work': location.hash = '#/work/' + arg; break;
      case 'open-result': location.hash = '#/result/' + arg; break;
      case 'open-decision': location.hash = '#/decision/' + arg; break;
      case 'open-meeting': location.hash = '#/meeting/' + arg; break;
      case 'open-skill': location.hash = '#/skill/' + arg; break;
      case 'open-utility-result': sessionStorage.setItem('util-open', '1'); render(); break;
      case 'emp-tab': location.hash = location.hash.replace(/(\/employee\/[\w-]+).*$/, '$1/' + arg); break;
      case 'talent-tab': location.hash = '#/talent/' + arg; break;
      case 'talent-cat': { const [base] = location.hash.split('?'); location.hash = base + '?cat=' + encodeURIComponent(arg); break; }
      case 'talent-search': break;
      case 'talent-refresh': render(); break;
      case 'org-expand': { const list = document.querySelector('.org-members-' + arg); if (list) list.classList.toggle('hidden'); break; }
      case 'avatar-menu': { document.querySelectorAll('.menu-pop.nav').forEach(x => x.remove());
        const pop = document.createElement('div'); pop.className = 'menu-pop nav'; pop.style.cssText = 'position:fixed;left:12px;bottom:64px;z-index:96';
        pop.innerHTML = `<button class="mi" data-nav="models">${C.ico(C.I.spark,14)} 模型配置 / AI 能力设置</button>
          <button class="mi" data-nav="#/settings/personal">个人设置</button>
          <button class="mi" data-nav="#/settings/company">公司设置</button>`;
        document.body.appendChild(pop);
        pop.querySelectorAll('.mi').forEach(mi => mi.addEventListener('click', () => { location.hash = mi.dataset.nav === 'models' ? '#/models' : mi.dataset.nav; pop.remove(); }));
        setTimeout(() => document.addEventListener('click', function close(e){ if(!pop.contains(e.target)){pop.remove();document.removeEventListener('click',close);} }),0); break; }
      case 'install-skill': { const s = FX.skill(arg); s.installed = !s.installed; render(); break; }
      case 'ws-surface': location.hash = '#/workspace/' + parse().id + '/' + arg; break;
      case 'toggle-context': sessionStorage.setItem('ctx-closed', '1'); render(); break;
      case 'toggle-context-show': sessionStorage.removeItem('ctx-closed'); render(); break;
      case 'toggle-utility': sessionStorage.setItem('util-open', sessionStorage.getItem('util-open') === '1' ? '0' : '1'); render(); break;
      case 'close-utility': sessionStorage.setItem('util-open', '0'); render(); break;
      case 'util-tab': utilState[location.hash || '#/ceo'] = { tab: arg }; render(); break;
      case 'util-max': document.getElementById('pane-utility').classList.toggle('maximized'); break;
      case 'ws-view': { const [base] = location.hash.split('?'); location.hash = base + '?view=' + arg; break; }
      case 'settings-save': { el.textContent = '已保存 ✓'; el.disabled = true; setTimeout(() => { el.textContent = '保存'; el.disabled = false; }, 1400); break; }
      case 'rd-defer': {
        const st = stateStore[location.hash] || 'normal'; stateStore[location.hash] = 'deferred';
        render(); break; }
      case 'confirm-proposal': {
        const tk = 'meeting:' + arg;
        RT.appendMsg(tk, { role: 'sys', text: 'Proposal 已确认（CEO）→ 转为 Work：教程向发布排期（9/18）· 完成后 Result 回流本会话' });
        RT.appendMsg(tk, { role: 'ai', emp: 'e-zhen', text: '决议已登记：本篇教程向发布。我已建立发布 Work（陈真统筹、苏晴封面、何川数据回收），完成后 Result 会引用回本会话，9/19 复盘会继续。', model: 'GLM-5.3', cost: '◇ 0.5' });
        PROTO.render(); break; }
      case 'toggle-search': openSearch(); break;
      case 'toggle-notifications': toggleNotifications(); break;
      case 'toggle-theme': { const cur = document.documentElement.dataset.theme; document.documentElement.dataset.theme = cur === 'dark' ? 'light' : 'dark'; break; }
      case 'set-theme': document.documentElement.dataset.theme = arg; break;
      case 'as-expand': cycleAssistant('expanded'); break;
      case 'as-live': break;
      case 'as-min': cycleAssistant('collapsed'); break;
      case 'as-suggest': cycleAssistant('working'); setTimeout(() => cycleAssistant('result-ready'), 1600); break;
      case 'cx-ref': { const input = composerEl.querySelector('.cx-input'); input.value += ' @'; input.focus(); break; }
      case 'focus-conv': { const t = $('#emp-conv') ? null : null; const c = document.querySelector('#main-content .composer .cx-input'); if (c) { c.focus(); } break; }
      case 'decide': { el.closest('.decision-banner').querySelectorAll('button').forEach(b => { b.classList.remove('primary'); b.disabled = true; });
        el.classList.add('primary');
        stateStore[location.hash] = 'decided';
        el.textContent += ' · 已确认';
        el.closest('.decision-banner').querySelectorAll('.btn').forEach(b => { if (b !== el) b.disabled = true; });
        break; }
    }
  });
  document.addEventListener('change', ev => {
    if (ev.target.id === 'ss-select') { stateStore[location.hash || '#/ceo'] = ev.target.value; render(); }
  });
  document.addEventListener('keydown', ev => {
    if ((ev.metaKey || ev.ctrlKey) && ev.key.toLowerCase() === 'k') { ev.preventDefault(); $('#search-panel').classList.contains('hidden') ? openSearch() : closeSearch(); }
    if ((ev.metaKey || ev.ctrlKey) && ev.key.toLowerCase() === 'j') { ev.preventDefault(); cycleAssistant(); }
    if (!$('#search-panel').classList.contains('hidden')) {
      if (ev.key === 'ArrowDown' || ev.key === 'ArrowUp') {
        ev.preventDefault();
        searchSel = Math.min(searchRows.length - 1, Math.max(0, searchSel + (ev.key === 'ArrowDown' ? 1 : -1)));
        markSel(); previewRow(searchRows[searchSel]); return;
      }
      if (ev.key === 'Enter' && searchRows[searchSel]) { ev.preventDefault(); location.hash = searchRows[searchSel].go; closeSearch(); return; }
    }
    if (ev.key === 'Escape') { closeSearch(); $('#notif-panel').classList.add('hidden'); $('#overlay').classList.remove('open'); document.getElementById('pane-utility').classList.remove('maximized'); }
  });
  $('#overlay').addEventListener('click', () => { closeSearch(); $('#notif-panel').classList.add('hidden'); });
  window.addEventListener('hashchange', () => { sessionStorage.removeItem('util-open'); render(); });

  /* ---------- utility divider resize（min 300 · localStorage 记忆） ---------- */
  document.addEventListener('pointerdown', ev => {
    if (ev.target.id !== 'util-resize') return;
    ev.preventDefault();
    const handle = ev.target; handle.classList.add('active');
    const move = e2 => {
      let w = window.innerWidth - e2.clientX - (document.getElementById('app').classList.contains('has-context') ? 256 : 0);
      w = Math.max(300, Math.min(560, w));
      document.getElementById('app').style.setProperty('--util-w', w + 'px');
    };
    const up = () => { handle.classList.remove('active'); localStorage.setItem('curis.utilw', document.getElementById('app').style.getPropertyValue('--util-w')); document.removeEventListener('pointermove', move); document.removeEventListener('pointerup', up); };
    document.addEventListener('pointermove', move); document.addEventListener('pointerup', up);
  });
  try { const uw = localStorage.getItem('curis.utilw'); if (uw) document.getElementById('app').style.setProperty('--util-w', uw); } catch (e) {}

  /* ---------- boot ---------- */
  renderAssistant();
  render();
  const bootQ = parse().q || {};
  if (bootQ.state) { stateStore[location.hash || '#/ceo'] = bootQ.state; }
  if (bootQ.util === '1' && bootQ.tab) { utilState[location.hash || '#/ceo'] = { tab: bootQ.tab }; }
  renderAssistant();
  render();
  if (bootQ.search === '1') setTimeout(openSearch, 50);
  if (bootQ.assistant) { cycleAssistant(bootQ.assistant === '1' ? 'expanded' : bootQ.assistant); }
  if (bootQ.demo) setTimeout(() => {
    const first = document.querySelector('#main-content .composer');
    const cid = first && first.id;
    const st = cid && RT.S.composers[cid];
    if (!st) return;
    if (bootQ.demo === 'attach') { st.attachments.push(RT.FILES[0]); st.refs.push(RT.REFS[2]); }
    if (bootQ.demo === 'running') { st.status = 'running'; st.queue = 1;
      const tk = st.opt.thread; RT.appendMsg(tk, { role: 'user', text: '先把对比分析发我，选题今天要出。' });
      RT.appendMsg(tk, { role: 'ai', emp: tk.startsWith('emp:') ? tk.slice(4) : undefined, text: '正在对比 5 个对标账号的互动结构，已完成 3/5；预计 6 分钟后给出结论与 3 个选题候选。', steps: [{ t: '评论样本聚类', done: true }, { t: '对标结构对比 3/5', done: false }], model: 'DeepSeek-V4.1' }); }
    if (bootQ.demo === 'perm') { st.perm = '完全访问'; st.permNote = 'requested：完全访问 · configured：已启用 · effective：本会话生效（写操作仍留审计）。档位 ≠ 沙箱生效，详见 设置 → 权限与数据。'; }
    PROTO.render();
    const mc = document.querySelector('#main-content'); if (mc) mc.scrollTop = mc.scrollHeight;
    if (bootQ.demo === 'focus') { const ta = document.querySelector('#main-content .composer .cx-input'); if (ta) ta.focus(); }
  }, 120);
  window.PROTO = { render, parse, cycleAssistant, openSearch };
})();
