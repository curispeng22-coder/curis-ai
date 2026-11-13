/* ============================================================
   RD Professional Workspace — 渲染与交互（视觉探索）
   全局命名空间 RD。消费 window.RD_DATA。
   严格对齐：RECONCILIATION / RD_PRODUCT_TRANSLATION §5·§6 / RD_INSTANCE §1.1·§1a·§7。
   不画 IDE/Terminal/Git/CI/部署工具；Provider 是能力提供方，Employee 是责任归属者。
   ============================================================ */
(function () {
  'use strict';
  var D = window.RD_DATA;

  var RD = {
    state: {
      projectId: 'p-default',
      expanded: {},          // empId -> bool
      activeWork: {},        // empId -> workId（多 Work 员工当前 Work）
      utility: null,         // refId
      utilMode: 'diff',      // 当前 Utility 子模式
      theme: 'dark',
      ctxOpen: true,
      jobs: {},              // workId -> { start, provider, dur, liveKey, done }
      draft: {},             // workId -> composer 草稿
      decisionResolved: {}   // projectId -> 'approved'|'rejected'|'instructed'
    },
    _liveSeq: 0,
    _ticker: null
  };
  window.RD = RD;

  /* ---------------- 工具 ---------------- */
  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
  function proj() { return D.projects.filter(function (p) { return p.id === RD.state.projectId; })[0]; }
  function emp(id) { return D.employees[id]; }
  function work(id) { return D.works[id]; }
  function ref(id) { return D.refs[id]; }

  function urgentWork(e) {
    // 该员工最「紧急」的 Work（与展示状态同源，避免紧凑行与状态标签说两件事）
    var order = D.statusOrder, best = null, bestK = 99;
    e.works.forEach(function (wid) {
      var w = work(wid); if (!w) return;
      var k = (order[w.status] != null) ? order[w.status] : 99;
      if (k < bestK) { bestK = k; best = w; }
    });
    return best || work(e.works[0]);
  }

  function empDisplayStatus(e) {
    // 取该员工最「紧急」的 Work 状态作为展示状态
    var w = urgentWork(e);
    return w ? w.status : 'idle';
  }

  function counts(p) {
    var c = { working: 0, waiting: 0, blocked: 0, needs_ceo: 0, review: 0, complete: 0, idle: 0, total: 0 };
    p.employees.forEach(function (eid) {
      emp(eid).works.forEach(function (wid) {
        var w = work(wid); if (!w) return;
        c.total++; c[w.status] = (c[w.status] || 0) + 1;
      });
    });
    return c;
  }

  function statusLabel(s) {
    return ({ working: '工作中', needs_ceo: '需 CEO', review: 'Review', blocked: '阻塞', waiting: '等待', complete: '已完成', idle: '空闲' })[s] || s;
  }
  function statusColor(s) {
    return ({ working: 'var(--ui-accent)', needs_ceo: 'var(--ui-warning)', review: 'var(--ui-text-2)', blocked: 'var(--ui-danger)', waiting: 'var(--ui-text-2)', complete: 'var(--ui-success)', idle: 'var(--ui-text-2)' })[s] || 'var(--ui-text-2)';
  }

  /* ---------------- 顶部导航（七区） ---------------- */
  function renderNav() {
    var nav = $('#nav-pane');
    var items = D.nav.map(function (label, i) {
      var active = (label === '业务空间');
      var badge = (label === '业务空间' && proj().decision) ? '<span class="badge">1</span>' : '';
      var ico = ['◆', '▣', '◇', '□', '◎', '▤', '◷'][i] || '•';
      return '<a class="nav-item ' + (active ? 'active' : '') + '" data-action="nav" data-label="' + esc(label) + '">' +
        '<span class="ico">' + ico + '</span><span>' + esc(label) + '</span>' + badge + '</a>';
    }).join('');
    nav.innerHTML =
      '<div class="brand"><span class="mark">C</span><span>Curis</span></div>' +
      '<nav class="nav-list">' + items + '</nav>' +
      '<div class="nav-foot">' +
        '<a class="nav-item"><span class="ico">○</span><span>设置</span></a>' +
        '<a class="nav-item"><span class="ico">?</span><span>帮助与反馈</span></a>' +
      '</div>';
  }

  /* ---------------- 顶栏（window bar） ---------------- */
  function renderWinbar() {
    var p = proj();
    var bar = $('#winbar');
    bar.innerHTML =
      '<div class="traffic"><i class="r"></i><i class="y"></i><i class="g"></i></div>' +
      '<span class="wtitle">RD 专业工作区</span>' +
      '<div class="proj-switch">' +
        '<span class="cur" data-action="toggle-proj"><span class="dot"></span><b>' + esc(p.name) + '</b><span>▾</span></span>' +
        '<div class="menu" id="proj-menu" hidden>' +
          D.projects.map(function (pp) {
            return '<button class="opt ' + (pp.id === p.id ? 'active' : '') + '" data-action="switch-project" data-pid="' + pp.id + '">' +
              esc(pp.name) + '<span class="sub">' + esc(pp.stage) + ' · ' + pp.version + ' · 进度 ' + pp.progress + '%</span></button>';
          }).join('') +
        '</div>' +
      '</div>' +
      '<div class="crumbs"><span>业务空间</span><span class="sep">/</span><span>研发 · <b>' + esc(p.name) + '</b></span></div>' +
      '<span class="spacer"></span>' +
      '<button class="winbtn" data-action="toggle-ctx" id="ctx-btn">⟨ 资源</button>' +
      '<button class="winbtn" data-action="toggle-util" id="util-btn">工具 ⟩</button>' +
      '<button class="winbtn" data-action="toggle-theme" id="theme-btn">' + (RD.state.theme === 'dark' ? '☀ 浅色' : '🌙 深色') + '</button>' +
      '<button class="winbtn" data-action="ceo-view">CEO 视图</button>';
  }

  /* ---------------- Project Operating Header ---------------- */
  function renderProjectHeader() {
    var p = proj();
    var c = counts(p);
    var needsCEO = p.decision ? 1 : 0;
    var html =
      '<div class="proj-header">' +
        '<div class="top">' +
          '<div>' +
            '<h1>研发 · ' + esc(p.name) + '</h1>' +
            '<p class="goal">' + esc(p.goal) + '</p>' +
          '</div>' +
          '<button class="addbtn" data-action="add-work">＋ 分配新工作</button>' +
        '</div>' +
        '<div class="proj-meta">' +
          meta('当前版本', p.version) +
          meta('当前阶段', p.stage) +
          meta('本轮目标', p.roundGoal) +
          meta('Work 总数', String(c.total)) +
        '</div>' +
        '<div class="proj-counts">' +
          chip('working', '进行中', c.working) +
          chip('complete', '已完成', c.complete) +
          chip('blocked', '阻塞', c.blocked) +
          chip('needs', '需 CEO', needsCEO) +
        '</div>' +
        '<div class="proj-progress">' +
          '<div class="bar"><i style="width:' + p.progress + '%"></i></div>' +
          '<span class="pct">' + p.progress + '%</span>' +
        '</div>' +
        '<div class="judge-row">' +
          '<div class="cell"><div class="k">Leader 判断</div><div class="v">' + esc(p.leaderJudgment) + '</div></div>' +
          '<div class="cell"><div class="k">下一步检查</div><div class="v">' + esc(p.nextCheck) + '</div></div>' +
        '</div>' +
      '</div>';
    $('#proj-header').innerHTML = html;
  }
  function meta(k, v) { return '<div class="mi"><span class="k">' + esc(k) + '</span><span class="v">' + esc(v) + '</span></div>'; }
  function chip(cls, label, n) { return '<span class="count-chip ' + cls + '">' + label + ' <span class="n">' + n + '</span></span>'; }

  /* ---------------- Decision Banner（Needs CEO） ---------------- */
  function renderDecision() {
    var box = $('#decision');
    var p = proj();
    if (!p.decision) { box.innerHTML = ''; box.hidden = true; return; }
    box.hidden = false;
    var d = p.decision;
    var prov = function (k) { return d.provenance && d.provenance[k] ? ' <span class="prov">' + d.provenance[k] + '</span>' : ''; };
    var opts = d.options.map(function (o) {
      return '<div class="opt"><span class="lbl">' + esc(o.label) + '</span><span class="d">' + esc(o.detail) + '</span></div>';
    }).join('');
    box.innerHTML =
      '<div class="decision">' +
        '<div class="head">' +
          '<span class="tag">⚠ 需要你拍板</span>' +
          '<span class="what">' + esc(d.what.split('，')[0]) + '</span>' +
          '<span class="eta">等待 ' + esc(d.eta) + '</span>' +
        '</div>' +
        '<div class="body">' + esc(d.what) + '</div>' +
        '<div class="grid">' +
          cell('为何 AI 不能自决' + prov('impact'), d.why) +
          cell('影响' + prov('impact'), d.impact) +
          cell('风险' + prov('risk'), d.risk) +
          cell('Employee 建议' + prov('recommendation'), d.recommendation + '（' + esc(d.recommendationReason) + '）') +
        '</div>' +
        '<div class="opts">' + opts + '</div>' +
        '<div class="body" style="margin-top:8px;color:var(--ui-text-2)">你只需做：' + esc(d.ceoChoice) + '。拍板后 AI 自动继续：' + esc(d.after) + '</div>' +
        '<div class="actions">' +
          '<button class="btn btn-primary" data-action="approve-decision">批准并执行（A）</button>' +
          '<button class="btn btn-secondary" data-action="reject-decision">拒绝</button>' +
          '<button class="btn btn-secondary" data-action="instruct-decision">提供指示</button>' +
        '</div>' +
      '</div>';
  }
  function cell(k, v) { return '<div class="cell"><div class="k">' + k + '</div><div class="v">' + esc(v) + '</div></div>'; }

  /* ---------------- Employee Work Surface ---------------- */
  function renderWorkSurface() {
    var p = proj();
    var emps = p.employees.slice().sort(function (a, b) {
      return D.statusOrder[empDisplayStatus(emp(a))] - D.statusOrder[empDisplayStatus(emp(b))];
    });
    var html = '<div class="ws-section-label">员工工作表面 · 当前团队 ' + p.employees.length + ' 人</div><div class="ws">';
    emps.forEach(function (eid) {
      var e = emp(eid);
      var st = empDisplayStatus(e);
      if (RD.state.expanded[eid]) html += renderEmpExpanded(e, st);
      else html += renderEmpCompact(e, st);
    });
    html += '</div>';
    $('#work-surface').innerHTML = html;
  }

  function renderEmpCompact(e, st) {
    var w = urgentWork(e);   // 与展示状态同源的 Work，保证「阻塞」标签旁边就是阻塞原因
    var one = w ? (w.title + (w.blocker ? ' · ' + w.blocker : '')) : '当前无进行中工作';
    return '<div class="emp-compact" data-action="toggle-emp" data-eid="' + e.id + '">' +
      avatar(e, 'av') +
      '<div><div class="nm">' + esc(e.name) + '</div><div class="rl">' + esc(e.role) + '</div></div>' +
      '<span class="status-pill ' + st + '">' + statusLabel(st) + '</span>' +
      '<span class="one" title="' + esc(one) + '">' + esc(one) + '</span>' +
      '<span class="chev">▾</span>' +
    '</div>';
  }

  function renderEmpExpanded(e, st) {
    var uw = urgentWork(e);
    var activeWid = RD.state.activeWork[e.id] || (uw ? uw.id : e.works[0]);
    var w = work(activeWid);
    var tabs = '';
    if (e.works.length > 1) {
      tabs = '<div class="work-tabs">' + e.works.map(function (wid) {
        var tw = work(wid);
        var dot = '<span class="dot" style="background:' + statusColor(tw.status) + '"></span>';
        return '<span class="work-tab ' + (wid === activeWid ? 'active' : '') + '" data-action="set-work" data-eid="' + e.id + '" data-wid="' + wid + '">' +
          dot + esc(tw.code) + ' · ' + esc(tw.title) + ' <span class="prov">' + esc(tw.provider) + '</span></span>';
      }).join('') + '</div>';
    }
    var body = renderWorkBody(e, w);
    return '<div class="emp" data-eid="' + e.id + '">' +
      '<div class="head" data-action="toggle-emp" data-eid="' + e.id + '">' +
        avatar(e, 'av') +
        '<div><div class="nm">' + esc(e.name) + '</div><div class="rl">' + esc(e.role) + ' · ' + esc(e.responsibility) + '</div></div>' +
        '<span class="status-pill ' + st + '">' + statusLabel(st) + '</span>' +
        '<span class="chev">▾</span>' +
      '</div>' +
      tabs +
      body +
    '</div>';
  }

  function renderWorkBody(e, w) {
    var conv = renderConversation(e, w);
    var side = renderWorkSide(w);
    return '<div class="work-body"><div class="conv-col">' + conv + '</div><div class="side-col">' + side + '</div></div>';
  }

  function renderConversation(e, w) {
    var msgs = w.conversation.map(function (m, i) {
      var cls = m.who; // employee | provider | ceo | review
      var av = (m.who === 'employee') ? avatar(e, 'av') :
        (m.who === 'provider') ? '<div class="av" style="background:var(--ui-accent);color:#0c0c0d">' + esc((m.name || 'P')[0]) + '</div>' :
        (m.who === 'review') ? '<div class="av" style="background:#ef6f9e;color:#fff">' + esc((m.name || 'R')[0]) + '</div>' :
        '<div class="av" style="background:var(--ui-surface-2);color:var(--ui-text)">你</div>';
      var refs = (m.refs && m.refs.length) ? '<div class="refs">' + m.refs.map(function (rid) {
        var r = ref(rid); if (!r) return '';
        return '<span class="ref" data-action="open-ref" data-ref="' + rid + '">' + esc(r.title) + '</span>';
      }).join('') + '</div>' : '';
      var live = m.live ? '<div class="provider-live" id="live-' + m.live + '"><span class="spin"></span><span class="lt">' + esc(m.liveText || '执行中…') + '</span></div>' : '';
      return '<div class="msg ' + cls + '">' + av +
        '<div class="bubble"><div class="who"><b>' + esc(m.name || (m.who === 'ceo' ? '你（CEO）' : '')) + '</b><span>' + esc(m.t || '') + '</span></div>' +
        '<div class="txt">' + esc(m.text) + '</div>' + refs + live + '</div></div>';
    }).join('');

    // Composer（中性，消费 Frozen Shell 槽位）
    var draft = RD.state.draft[w.id] || '';
    var composer =
      '<div class="composer" data-eid="' + e.id + '" data-wid="' + w.id + '">' +
        '<div class="ctx-line">在「研发 · ' + esc(proj().name) + '」下回复 ' + esc(e.name) + ' · ' + esc(w.code) + '</div>' +
        '<div class="row">' +
          '<textarea data-action="composer-input" data-wid="' + w.id + '" rows="1" placeholder="回复 ' + esc(e.name) + '，或下达指令…">' + esc(draft) + '</textarea>' +
          '<button class="send" data-action="send" data-eid="' + e.id + '" data-wid="' + w.id + '">发送</button>' +
        '</div>' +
        '<div class="slots">' +
          '<span class="slot add" data-action="exec-provider" data-eid="' + e.id + '" data-wid="' + w.id + '">▶ 执行 ' + esc(w.provider) + '</span>' +
          '<span class="slot">＋ 添加</span>' +
          '<span class="slot">访问权限 · 默认</span>' +
          '<span class="slot">工作模式 · 连续</span>' +
          '<span class="slot">已选资源 · ' + esc(w.responsibility) + '</span>' +
          '<span class="slot">Model·Agent · ' + esc(workProviderShort(w.provider)) + '</span>' +
          '<span class="slot">🎙 Voice</span>' +
        '</div>' +
      '</div>';

    return '<div class="conv">' + msgs + '</div>' + composer;
  }

  function workProviderShort(p) { return ({ 'Codex': 'Codex', 'Claude Code': 'Claude Code', 'Copilot': 'Copilot', 'GitHub Actions': 'CI' })[p] || p; }

  function renderWorkSide(w) {
    var kv =
      '<div class="kv">' +
        kvRow('责任', w.responsibility) +
        kvRow('Provider', w.provider) +
        kvRow('状态', statusLabel(w.status)) +
        kvRow('Holder', emp(w.responsibilityHolder).name) +
        kvRow('当前执行', w.currentExecutor === 'none' ? '—（无）' : emp(w.currentExecutor).name) +
        (w.blocker ? kvRow('阻塞', w.blocker, true) : '') +
        kvRow('下一步', w.nextStep) +
      '</div>';
    var refs = (w.resultRefs && w.resultRefs.length) ?
      '<div style="margin-top:10px"><div class="ctx-sec-title">结果引用</div>' + w.resultRefs.map(function (rid) {
        var r = ref(rid); if (!r) return '';
        return '<span class="ref" data-action="open-ref" data-ref="' + rid + '" style="display:flex;width:100%;margin-bottom:6px">' + esc(r.title) + '</span>';
      }).join('') + '</div>' : '';
    var learning = w.learning ? '<div style="margin-top:10px"><div class="ctx-sec-title">复盘笔记</div><div class="work-overview" style="background:var(--ui-surface-2)">' + esc(w.learning) + '</div></div>' : '';
    return '<div class="work-overview"><span class="lbl">工作概览</span>' + esc(w.overview) + '</div>' + kv + refs + learning;
  }
  function kvRow(k, v, block) { return '<div class="k">' + esc(k) + '</div><div class="v' + (block ? ' block' : '') + '">' + esc(v) + '</div>'; }

  function avatar(e, cls) {
    return '<div class="' + cls + '" style="background:' + e.color + '">' + esc(e.avatar) + '</div>';
  }

  /* ---------------- Context pane（文件与对象） ---------------- */
  function renderContext() {
    var p = proj();
    var ctx = D.context[p.id] || { files: [], recent: [] };
    var files = ctx.files.map(function (f) {
      var rid = refIdForFile(f.name);
      return '<div class="ctx-file" data-action="ctx-file" data-wid="' + esc(f.work) + '"' + (rid ? ' data-ref="' + rid + '"' : '') + '>' +
        '<span class="fi">⌗</span><span>' + esc(f.name) + '</span><span class="meta">' + esc(f.meta) + '</span></div>';
    }).join('');
    var recent = ctx.recent.map(function (r) {
      return '<div class="ctx-recent"><div class="item" data-action="ctx-rec" data-wid="' + esc(r.work) + '">◷ ' + esc(r.name) + '</div></div>';
    }).join('');
    $('#ctx-pane').innerHTML =
      '<div class="pane-head">文件 · 最近对象 <button class="x" data-action="toggle-ctx">✕</button></div>' +
      '<div class="ctx-body">' +
        '<div class="ctx-sec-title">相关文件（当前 Project）</div>' + files +
        '<div class="ctx-sec-title" style="margin-top:14px">最近对象</div>' + recent +
      '</div>';
  }
  function refIdForFile(name) {
    var hit = null;
    Object.keys(D.refs).forEach(function (rid) { if (D.refs[rid].file === name) hit = rid; });
    return hit;
  }

  /* ---------------- Utility pane ---------------- */
  function renderUtility() {
    var pane = $('#util-pane');
    var rid = RD.state.utility;
    if (!rid) {
      pane.hidden = false;
      pane.innerHTML = '<div class="pane-head">工具面 · Utility</div>' +
        '<div class="util-empty"><div class="ic">⌗</div><div>点击对话中的「查看差异 / 测试 / PR / Build」引用，<br>在此查看代码、测试、PR 与构建结果。<br><br>Curis 不实现专业编辑——修改仍回 Employee → Provider。</div></div>';
      return;
    }
    var r = ref(rid);
    pane.hidden = false;
    var owner = '<div class="util-owner">所属责任 <b>' + esc(r.responsibility) + '</b> · Work <b>' + esc(r.workId) + '</b></div>';
    var tabs = utilTabs(r);
    var body = utilBody(r);
    pane.innerHTML =
      '<div class="pane-head">工具面 · Utility <button class="x" data-action="close-util" style="margin-left:auto;border:0;background:none;color:var(--ui-text-3);cursor:pointer">✕</button></div>' +
      tabs + owner + '<div class="util-body">' + body + '</div>' +
      '<div class="util-foot"><button class="btn btn-secondary" data-action="close-util">返回 Conversation</button></div>';
  }
  function utilTabs(r) {
    var modes = [];
    if (r.type === 'diff') modes = [['diff', '差异'], ['source', '源码']];
    else if (r.type === 'test') modes = [['test', '测试'], ['preview', '预览']];
    else if (r.type === 'pr') modes = [['pr', 'PR']];
    else if (r.type === 'build') modes = [['build', '构建']];
    return '<div class="util-mode-tabs">' + modes.map(function (m) {
      return '<span class="util-mode ' + (RD.state.utilMode === m[0] ? 'active' : '') + '" data-action="util-mode" data-ref="' + r.__rid + '" data-type="' + m[0] + '">' + m[1] + '</span>';
    }).join('') + '</div>';
  }
  function utilBody(r) {
    var mode = RD.state.utilMode;
    if (r.type === 'diff') {
      if (mode === 'source') return sourceView(r);
      return diffView(r);
    }
    if (r.type === 'test') {
      if (mode === 'preview') return '<div class="test-sum">预览：集成测试在预发环境跑通，报告见 CI。无独立预览窗口——Curis 不启动浏览器。</div>';
      return testView(r);
    }
    if (r.type === 'pr') return prView(r);
    if (r.type === 'build') return buildView(r);
    return '';
  }
  function diffView(r) {
    var oldN = 0, newN = 0;
    var lines = r.diff.map(function (ln) {
      if (ln.k === 'add') { newN++; return '<div class="ln add"><span class="old"></span><span class="new">+' + newN + '</span><span>' + esc(ln.t) + '</span></div>'; }
      if (ln.k === 'del') { oldN++; return '<div class="ln del"><span class="old">-' + oldN + '</span><span class="new"></span><span>' + esc(ln.t) + '</span></div>'; }
      if (ln.k === 'warn') return '<div class="ln warn"><span class="old"></span><span class="new"></span><span>' + esc(ln.t) + '</span></div>';
      oldN++; newN++;
      return '<div class="ln ctx"><span class="old">' + oldN + '</span><span class="new">' + newN + '</span><span>' + esc(ln.t) + '</span></div>';
    }).join('');
    return '<div class="diff"><div class="file"><span class="ic">⌗</span>' + esc(r.file) + ' · 查看差异</div><pre>' + lines + '</pre></div>';
  }
  function sourceView(r) {
    if (r.sourceFull) {
      var code = r.sourceFull.map(function (l) {
        return '<div class="ln ctx"><span class="old"></span><span class="new"></span><span>' + esc(l) + '</span></div>';
      }).join('');
      return '<div class="diff"><div class="file"><span class="ic">⌗</span>' + esc(r.file) + ' · 源码（当前）</div><pre>' + code + '</pre></div>';
    }
    var code2 = r.diff.filter(function (l) { return l.k === 'add' || l.k === 'ctx'; }).map(function (l) { return esc(l.t); }).join('\n');
    return '<div class="diff"><div class="file"><span class="ic">⌗</span>' + esc(r.file) + ' · 源码（当前）</div><pre><div class="ln ctx"><span class="old"></span><span class="new"></span><span>' + code2 + '</span></div></pre></div>';
  }
  function testView(r) {
    var rows = r.tests.map(function (t) {
      return '<div class="test-row"><span class="st ' + t.s + '">' + (t.s === 'pass' ? '✓' : '✕') + '</span><span>' + esc(t.n) + '</span></div>';
    }).join('');
    return '<div class="test-sum">' + esc(r.summary) + '</div><div class="test-list">' + rows + '</div>';
  }
  function prView(r) {
    var p = r.pr;
    return '<div class="pr-card"><div><span class="num">PR #' + p.number + '</span><span class="state">' + esc(p.state) + '</span></div>' +
      '<div style="margin-top:6px;font-size:var(--ui-fs-2)">' + esc(p.title) + '</div>' +
      '<div class="meta"><span>改动 <b>+' + p.additions + ' / -' + p.deletions + '</b></span><span>Checks <b>' + esc(p.checks) + '</b></span><span>评论 <b>' + p.comments + '</b></span></div>' +
      '<div class="meta" style="margin-top:6px"><span>来源 <b>GitHub API_SYNC</b></span><span>Job <b>run_' + (1000 + p.number) + '</b></span></div></div>';
  }
  function buildView(r) {
    return '<div class="build-log">' + esc(r.log.join('\n')) + '</div>';
  }

  /* ---------------- 全量渲染 ---------------- */
  function render() {
    document.documentElement.setAttribute('data-theme', RD.state.theme);
    var shell = $('#shell');
    shell.classList.toggle('no-ctx', !RD.state.ctxOpen);
    shell.classList.toggle('no-util', !RD.state.utility && shell.classList.contains('no-util'));
    renderNav();
    renderWinbar();
    renderProjectHeader();
    renderDecision();
    renderWorkSurface();
    renderContext();
    renderUtility();
  }
  // 仅重渲染主区（provider 结果到达时，避免清掉 composer 焦点）
  function renderMain() {
    renderProjectHeader(); renderDecision(); renderWorkSurface();
  }

  /* ============================================================
     交互
     ============================================================ */
  function toggleEmp(eid) {
    RD.state.expanded[eid] = !RD.state.expanded[eid];
    renderWorkSurface();
  }
  function setWork(eid, wid) {
    RD.state.activeWork[eid] = wid;
    if (!RD.state.expanded[eid]) RD.state.expanded[eid] = true;
    renderWorkSurface();
  }
  function switchProject(pid) {
    if (pid === RD.state.projectId) { closeProjMenu(); return; }
    RD.state.projectId = pid;
    RD.state.utility = null;
    // 进入新 Project：展开 working/needs_ceo/review 员工
    RD.state.expanded = {};
    proj().employees.forEach(function (eid) {
      var st = empDisplayStatus(emp(eid));
      if (st === 'working' || st === 'needs_ceo' || st === 'review') RD.state.expanded[eid] = true;
    });
    closeProjMenu();
    render();
    toast('已切换到 Project Context：' + proj().name);
  }
  function closeProjMenu() { var m = $('#proj-menu'); if (m) m.hidden = true; }

  function openRef(rid) {
    var r = ref(rid); if (!r) return;
    r.__rid = rid;
    RD.state.utility = rid;
    RD.state.utilMode = r.type === 'diff' ? 'diff' : r.type === 'test' ? 'test' : r.type;
    $('#shell').classList.remove('no-util');
    renderUtility();
  }
  function closeUtil() { RD.state.utility = null; renderUtility(); }

  /* ---- Provider 异步执行（不随切换丢失） ---- */
  function execProvider(eid, wid) {
    var w = work(wid);
    if (RD.state.jobs[wid]) return; // 已在跑
    var liveKey = 'L' + (++RD._liveSeq);
    RD.state.jobs[wid] = { start: Date.now(), provider: w.provider, dur: 4500, liveKey: liveKey, done: false };
    var e = emp(eid);
    w.conversation.push({
      who: 'provider', name: w.provider, t: nowTime(),
      text: w.provider + ' 正在执行「' + w.title + '」…', live: liveKey, liveText: w.provider + ' 执行中… 0.0s'
    });
    renderMain();
    startTicker();
    toast(w.provider + ' 执行中：' + w.title);
  }
  function finalizeJob(wid) {
    var job = RD.state.jobs[wid]; if (!job || job.done) return;
    job.done = true;
    var w = work(wid);
    // 把 running 消息转为完成
    w.conversation.forEach(function (m) { if (m.live === job.liveKey) { m.live = null; m.text = w.provider + ' 执行完成：已生成「' + w.title + '」的改动与结果，见下方引用。'; } });
    // 追加结果引用（若该 Work 有 resultRefs）
    var lastMsg = w.conversation[w.conversation.length - 1];
    if (w.resultRefs && w.resultRefs.length) lastMsg.refs = (lastMsg.refs || []).concat(w.resultRefs);
    else lastMsg.refs = (lastMsg.refs || []).concat(['ref-build-230']);
    delete RD.state.jobs[wid];
    renderMain();
    toast(w.provider + ' 已返回结果：' + w.title);
  }
  function startTicker() {
    if (RD._ticker) return;
    RD._ticker = setInterval(function () {
      var any = false;
      Object.keys(RD.state.jobs).forEach(function (wid) {
        var job = RD.state.jobs[wid];
        var el = $('#live-' + job.liveKey);
        var elapsed = ((Date.now() - job.start) / 1000).toFixed(1);
        if (el) { var lt = el.querySelector('.lt'); if (lt) lt.textContent = job.provider + ' 执行中… ' + elapsed + 's'; any = true; }
        else any = true; // 不在当前视图，但仍在跑
        if (Date.now() - job.start >= job.dur) finalizeJob(wid);
      });
      if (!Object.keys(RD.state.jobs).length) { clearInterval(RD._ticker); RD._ticker = null; }
    }, 400);
  }

  /* ---- Conversation 发送（双向） ---- */
  function send(eid, wid, text) {
    var w = work(wid), e = emp(eid);
    text = (text || '').trim();
    if (!text) return;
    w.conversation.push({ who: 'ceo', name: '你（CEO）', t: nowTime(), text: text });
    RD.state.draft[wid] = '';
    // 员工真实回复（含计划）
    var plan = employeeReply(w, e, text);
    w.conversation.push({ who: 'employee', name: e.name, t: nowTime(), text: plan.text, refs: plan.refs });
    renderMain();
    // 若涉及执行，触发 Provider
    if (plan.exec) {
      setTimeout(function () { execProvider(eid, wid); }, 350);
    }
  }
  function employeeReply(w, e, ceoText) {
    // 基于 Work 生成合理的员工回复
    if (/迁移|切换|授权|数据库/.test(ceoText) && w.id === 'W-233') {
      return { text: '收到。若今晚低峰执行，我会先双写校验、再切读路径、最后停写旧表，全程盯盘 90s 回滚窗口。已就绪待你授权。', refs: ['ref-diff-233'] };
    }
    if (/测试|集成|验证/.test(ceoText) && w.id === 'W-240') {
      return { text: 'W-230 合入后我立即跑影子流量回放，预期 24 条 E2E 全绿即出 Verification 结论。', exec: true };
    }
    // 通用：把 Work 拆成并行子任务（演示徐川式多 Work）
    if (/拆|并行|分成|两条/.test(ceoText)) {
      return { text: '已拆成两个并行 Work：W-231 走 Codex、W-232 走 Claude Code，互不干扰。两个 Provider 会分别回报。', exec: true };
    }
    return {
      text: '明白。我按当前责任继续推进「' + w.title + '」，需要落代码时让 ' + w.provider + ' 执行，结果会回到这条 Conversation。',
      exec: true
    };
  }

  /* ---- 决策：批准 / 拒绝 / 指示 ---- */
  function approveDecision() {
    var p = proj(); if (!p.decision) return;
    var d = p.decision;
    // 效果：架构师 blocked Work → Working；下游测试 Waiting → Working；进度 +8
    var w233 = work(d.workId); w233.status = 'working'; w233.currentExecutor = w233.responsibilityHolder; w233.blocker = null;
    var w240 = work('W-240'); if (w240) { w240.status = 'working'; w240.currentExecutor = w240.responsibilityHolder; w240.blocker = null; }
    p.progress = Math.min(100, p.progress + 8);
    RD.state.decisionResolved[p.id] = 'approved';
    p.decision = null;
    // 展开受影响员工，让变化可见
    RD.state.expanded['e-lixiang'] = true;
    RD.state.expanded['e-wangyu'] = true;
    render();
    toast('决策已批准：迁移进入授权窗口执行，王雨启动集成测试，进度 +8%');
  }
  function rejectDecision() {
    var p = proj(); if (!p.decision) return;
    p.decision = null; RD.state.decisionResolved[p.id] = 'rejected';
    work('W-233').blocker = 'CEO 已拒绝授权：迁移方案回到架构师重评估。';
    render();
    toast('已拒绝：迁移方案退回架构师重评估');
  }
  function instructDecision() {
    var p = proj(); if (!p.decision) return;
    // 打开李翔对话并预填指示
    RD.state.expanded['e-lixiang'] = true;
    RD.state.activeWork['e-lixiang'] = 'W-233';
    RD.state.utility = null;
    render();
    RD.state.draft['W-233'] = '请先补充回滚演练的录像证据，再提交执行窗口。';
    var ta = $('.composer[data-wid="W-233"] textarea');
    if (ta) { ta.value = RD.state.draft['W-233']; ta.focus(); }
    toast('已转入李翔对话，可写下你的指示');
  }

  /* ---- 杂项 ---- */
  function toggleTheme() { RD.state.theme = (RD.state.theme === 'dark') ? 'light' : 'dark'; render(); }
  function toggleCtx() { RD.state.ctxOpen = !RD.state.ctxOpen; render(); }
  function toggleUtil() {
    var shell = $('#shell');
    if (RD.state.utility) { closeUtil(); shell.classList.add('no-util'); }
    else { shell.classList.toggle('no-util'); }
    renderWinbar();
  }
  function nowTime() {
    var d = new Date(); var h = ('0' + d.getHours()).slice(-2); var m = ('0' + d.getMinutes()).slice(-2);
    return h + ':' + m;
  }
  function toast(msg) {
    var t = $('#toast'); if (!t) { t = document.createElement('div'); t.id = 'toast'; t.className = 'toast'; document.body.appendChild(t); }
    t.textContent = msg; t.classList.add('show');
    clearTimeout(t._tm); t._tm = setTimeout(function () { t.classList.remove('show'); }, 2200);
  }

  /* ---------------- 事件委托 ---------------- */
  function onClick(ev) {
    var t = ev.target.closest('[data-action]');
    if (!t) return;
    var a = t.getAttribute('data-action');
    var ds = t.dataset;
    switch (a) {
      case 'nav': /* 七区导航占位（视觉探索不跳转） */ toast('「' + ds.label + '」为全局导航占位（本探索仅研发工作区可交互）'); break;
      case 'toggle-proj': closeProjMenu(); var m = $('#proj-menu'); if (m) m.hidden = !m.hidden; break;
      case 'switch-project': switchProject(ds.pid); break;
      case 'toggle-emp': toggleEmp(ds.eid); break;
      case 'set-work': setWork(ds.eid, ds.wid); break;
      case 'open-ref': openRef(ds.ref); break;
      case 'close-util': closeUtil(); break;
      case 'util-mode': RD.state.utility = ds.ref; RD.state.utilMode = ds.type; renderUtility(); break;
      case 'exec-provider': execProvider(ds.eid, ds.wid); break;
      case 'approve-decision': approveDecision(); break;
      case 'reject-decision': rejectDecision(); break;
      case 'instruct-decision': instructDecision(); break;
      case 'add-work': toast('（Mock）分配新工作面板——视觉探索未实现表单'); break;
      case 'ceo-view': toast('（Mock）CEO 视图——聚合跨 Business 待裁决'); break;
      case 'toggle-theme': toggleTheme(); break;
      case 'toggle-ctx': toggleCtx(); break;
      case 'toggle-util': toggleUtil(); break;
      case 'ctx-file':
        if (ds.ref) openRef(ds.ref);
        else if (ds.wid) { RD.state.expanded[work(ds.wid).employeeId] = true; RD.state.activeWork[work(ds.wid).employeeId] = ds.wid; renderWorkSurface(); }
        break;
      case 'ctx-rec':
        if (ds.wid) { RD.state.expanded[work(ds.wid).employeeId] = true; RD.state.activeWork[work(ds.wid).employeeId] = ds.wid; renderWorkSurface(); }
        break;
    }
  }
  function onInput(ev) {
    var t = ev.target.closest('[data-action="composer-input"]');
    if (!t) return;
    RD.state.draft[t.getAttribute('data-wid')] = t.value;
    // 自适应高度
    t.style.height = 'auto'; t.style.height = Math.min(120, t.scrollHeight) + 'px';
  }
  function onKey(ev) {
    if (ev.key === 'Enter' && !ev.shiftKey) {
      var t = ev.target.closest('[data-action="composer-input"]');
      if (t) { ev.preventDefault(); var wid = t.getAttribute('data-wid'); var comp = t.closest('.composer'); send(comp.getAttribute('data-eid'), wid, t.value); }
    }
  }
  function onDocClick(ev) { if (!ev.target.closest('.proj-switch')) closeProjMenu(); }

  /* ---------------- 初始化 ---------------- */
  function init() {
    // 初始展开 working/needs_ceo/review 员工
    proj().employees.forEach(function (eid) {
      var st = empDisplayStatus(emp(eid));
      if (st === 'working' || st === 'needs_ceo' || st === 'review') RD.state.expanded[eid] = true;
    });
    render();
    document.addEventListener('click', onClick);
    document.addEventListener('input', onInput);
    document.addEventListener('keydown', onKey);
    document.addEventListener('click', onDocClick);
    console.info('[RD] 工作区已初始化 · Project=' + proj().name + ' · 主题=' + RD.state.theme);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  // 暴露给自测脚本
  RD.api = {
    send: send, execProvider: execProvider, approveDecision: approveDecision,
    switchProject: switchProject, openRef: openRef, state: RD.state, work: work, proj: proj, counts: counts
  };
})();
