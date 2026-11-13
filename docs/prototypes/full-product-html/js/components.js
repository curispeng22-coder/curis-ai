/* ============================================================
   Curis Full Product HTML Design Prototype — components.js
   渲染辅助组件（纯字符串模板；事件用 data-action 委托）
   ============================================================ */
window.C = (function () {
  const ico = (path, size) => `<svg class="ico" ${size ? `style="width:${size}px;height:${size}px;flex-basis:${size}px"` : ''} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${path}</svg>`;
  const I = {
    home: '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/>',
    briefcase: '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>',
    org: '<rect x="3" y="3" width="8" height="8" rx="1"/><rect x="13" y="3" width="8" height="8" rx="1"/><rect x="3" y="13" width="8" height="8" rx="1"/><rect x="13" y="13" width="8" height="8" rx="1"/>',
    users: '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8M17.5 14.4a6.5 6.5 0 0 1 4 5.6"/>',
    chart: '<path d="M4 20V10M10 20V4m6 16v-7"/><path d="M2 20h20"/>',
    book: '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5v14z"/><path d="M4 19.5A2.5 2.5 0 0 0 6.5 22H20v-5"/>',
    video: '<rect x="3" y="5" width="13" height="14" rx="2"/><path d="m16 10 5-3v10l-5-3"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
    check: '<path d="m5 12 5 5L20 7"/>',
    chev: '<path d="m9 6 6 6-6 6"/>',
    down: '<path d="m6 9 6 6 6-6"/>',
    search: '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    dot: '<circle cx="12" cy="12" r="4"/>',
    send: '<path d="M12 19V5m0 0-6 6m6-6 6 6"/>',
    stop: '<rect x="7" y="7" width="10" height="10" rx="1.5"/>',
    clip: '<path d="m21 12-8.5 8.5a5 5 0 0 1-7-7L14 5a3.3 3.3 0 0 1 4.7 4.7L10 18.4a1.7 1.7 0 0 1-2.4-2.4L16 7.7"/>',
    at: '<circle cx="12" cy="12" r="4"/><path d="M16 8v5a3 3 0 0 0 6-1 10 10 0 1 0-4 8"/>',
    doc: '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/>',
    sheet: '<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M4 10h16M10 4v16"/>',
    code: '<path d="m8 8-4 4 4 4m8-8 4 4-4 4m-3-10-2 12"/>',
    gear: '<circle cx="12" cy="12" r="3"/><path d="M19 12a7 7 0 0 0-.1-1.2l2-1.5-2-3.5-2.3 1a7 7 0 0 0-2-1.2L14 3h-4l-.6 2.6a7 7 0 0 0-2 1.2l-2.3-1-2 3.5 2 1.5A7 7 0 0 0 5 12c0 .4 0 .8.1 1.2l-2 1.5 2 3.5 2.3-1a7 7 0 0 0 2 1.2L10 21h4l.6-2.6a7 7 0 0 0 2-1.2l2.3 1 2-3.5-2-1.5c.1-.4.1-.8.1-1.2z"/>',
    bell: '<path d="M18 8a6 6 0 1 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/>',
    spark: '<path d="M12 3v4m0 10v4M3 12h4m10 0h4M5.6 5.6l2.8 2.8m7.2 7.2 2.8 2.8M5.6 18.4l2.8-2.8m7.2-7.2 2.8-2.8"/>',
    file: '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
    refresh: '<path d="M21 12a9 9 0 1 1-2.6-6.3M21 4v5h-5"/>',
    share: '<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="m8.3 10.8 7.4-3.6m-7.4 6 7.4 3.6"/>',
    hand: '<path d="M8 13V5.5a1.5 1.5 0 0 1 3 0V12m0-1.5v-6a1.5 1.5 0 0 1 3 0V12m0-1a1.5 1.5 0 0 1 3 0v5a6 6 0 0 1-6 6h-.8a6 6 0 0 1-4.6-2.1L3.5 16.6a1.6 1.6 0 0 1 2.4-2.1L8 16.5"/>',
    x: '<path d="M18 6 6 18M6 6l12 12"/>',
    minus: '<path d="M5 12h14"/>',
    msg: '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    cal: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 11h18"/>',
  };

  const statusMeta = s => ({ working:['run','工作中'], idle:['idle','空闲'], blocked:['err','阻塞'], done:['ok','已完成'], review:['warn','待确认'], scheduled:['idle','已排期'], needs_ceo:['warn','需要 CEO'], activating:['warn','激活中'], running:['run','运行中'] }[s] || ['idle', s]);
  const st = s => { const [c, t] = statusMeta(s); return `<span class="status"><span class="dot ${c}"></span>${t}</span>`; };
  const stFull = e => e.status === 'working' ? `<span class="status"><span class="dot run"></span>工作中 · ${e.statusDesc}</span>`
    : e.status === 'blocked' ? `<span class="status"><span class="dot err"></span>阻塞 · ${e.statusDesc}</span>`
    : e.status === 'done' ? `<span class="status"><span class="dot ok"></span>已完成 · ${e.statusDesc}</span>`
    : `<span class="status"><span class="dot idle"></span>空闲</span>`;

  const avatar = (e, cls) => `<span class="avatar ${cls || ''} av-${e.av}">${e.name[0]}</span>`;
  const avatarById = (id, cls) => { const e = FX.emp(id); return e ? avatar(e, cls) : `<span class="avatar ${cls || ''} av-7">?</span>`; };

  const empRow = (e, opt = {}) => `
    <div class="emp-row ${opt.open ? 'open' : ''} ${opt.selected ? 'selected' : ''}" data-emp="${e.id}">
      <div class="emp-row-head" data-action="${opt.openAction || 'open-employee'}" data-arg="${e.id}">
        <span data-action="${opt.utilAction || opt.openAction || 'open-employee'}" data-arg="${e.id}" style="display:contents">${avatar(e)}</span>
        <span class="emp-id"><span data-action="${opt.utilAction || opt.openAction || 'open-employee'}" data-arg="${e.id}" style="display:contents"><span class="emp-name" style="${opt.utilAction ? 'cursor:pointer;text-decoration:underline dotted var(--ui-text-3);text-underline-offset:3px' : ''}">${e.name}</span></span><span class="emp-role">${e.role}${e.leader ? ' · <b style="color:var(--ui-accent)">Leader</b>' : ''}</span></span>
        <span class="emp-status">${stFull(e)}</span>
        <span class="emp-chevron">${ico(I.chev, 14)}</span>
        <span class="emp-duty">${e.duty}</span>
      </div>
      <div class="emp-body">${opt.body || `当前责任：${e.responsibility.current}<br>能力：${e.capability.map(c => `<span class="tag">${c}</span>`).join(' ')}`}</div>
    </div>`;

  const todoList = plan => `<div class="todo">${plan.map(p => `
    <div class="ti ${p.current ? 'current' : ''} ${p.done ? 'done' : ''}">
      <span class="tbox ${p.done ? 'done' : ''} ${p.current ? 'current' : ''}">${p.done ? '✓' : ''}</span>${p.t}
    </div>`).join('')}</div>`;

  const progressBar = pct => `<div class="progressbar"><i style="width:${pct}%"></i></div>`;

  const workCard = (w, opt = {}) => {
    const done = w.plan.filter(p => p.done).length;
    const pct = Math.round(done / w.plan.length * 100);
    const e = FX.emp(w.employee);
    return `<div class="work-card" data-work="${w.id}">
      <div class="wk-head">${st(w.status)}<span class="wk-title">${w.title}</span>
        <span class="spacer"></span>
        ${opt.link !== false ? `<button class="btn sm ghost" data-action="open-work" data-arg="${w.id}">查看工作</button>` : ''}
      </div>
      <div class="status">${avatarById(w.employee, 'sm')} ${e.name} · ${e.role} ${w.ws ? '· ' + FX.ws(w.ws).name : ''}</div>
      ${todoList(w.plan)}
      ${progressBar(pct)}
      <div class="status faint" style="font-size:12px">${w.status === 'working' ? `当前：${w.current}` : w.status === 'blocked' ? `阻塞：${w.current}` : '已完成'} · ${w.elapsed} · ${w.cost}</div>
      ${w.tools && w.tools.length ? `<details class="tool-block"><summary>工具活动（${w.tools.length}）· 默认折叠</summary><div class="tool-body">${w.tools.map(t => `▸ ${t.n} — ${t.d}`).join('\n')}</div></details>` : ''}
      ${w.handoff ? `<div class="step-line">${ico(I.hand, 14)} ${w.handoff}</div>` : ''}
      ${w.result ? `<div style="margin-top:6px"><span class="result-ref" data-action="open-result" data-arg="${w.result}">${ico(I.doc, 13)} 查看结果 · ${FX.result(w.result).title}</span></div>` : ''}
    </div>`;
  };

  const msg = m => {
    if (m.role === 'sys') return `<div class="step-line" style="justify-content:center">${m.text}</div>`;
    if (m.role === 'user') return `<div class="msg user"><div class="bubble">${m.text}${(m.atts && m.atts.length) ? `<div class="filecard-grid">${m.atts.map(a => `<div class="filecard"><span class="fc-ico">${a.endsWith('.xlsx') ? 'XLSX' : a.endsWith('.ts') ? 'TS' : 'DOC'}</span><span><span class="fc-name">${a}</span><br><span class="fc-meta">引用 · 点击在 Utility 打开</span></span></div>`).join('')}</div>` : ''}${(m.refs && m.refs.length) ? `<div style="margin-top:6px;display:flex;gap:6px;flex-wrap:wrap">${m.refs.map(r => `<span class="chip">${r}</span>`).join('')}</div>` : ''}</div></div>`;
    const e = m.emp ? FX.emp(m.emp) : null;
    return `<div class="msg">${e ? avatar(e, 'sm') : ''}<div style="min-width:0">
      ${e ? `<div class="who">${e.name} · ${e.role} ${stFull(e)}</div>` : ''}
      <div class="bubble" style="max-width:100%">${m.text}</div>
      ${m.fileCards ? `<div class="filecard-grid">${m.fileCards.map(f => `
        <div class="filecard" data-action="open-result" data-arg="${f.result || ''}"><span class="fc-ico">${f.ext}</span>
          <span><span class="fc-name">${f.name}</span><br><span class="fc-meta">${f.meta}</span></span>
          <span class="spacer"></span><span class="iconbtn">${ico(I.share, 14)}</span></div>`).join('')}</div>` : ''}
      ${m.citations ? `<div style="margin-top:6px;display:flex;gap:6px;flex-wrap:wrap">${m.citations.map(c => `<span class="chip">来源 · ${c}</span>`).join('')}</div>` : ''}
      ${m.result ? `<div style="margin-top:8px"><span class="result-ref" data-action="open-result" data-arg="${m.result}">${ico(I.doc, 13)} ${FX.result(m.result).title}</span></div>` : ''}
      ${m.tools ? `<details class="tool-block"><summary>工具活动（${m.tools.length}）</summary><div class="tool-body">${m.tools.map(t => `▸ ${t.n} — ${t.d}`).join('\n')}</div></details>` : ''}
      ${m.thinking ? `<details class="tool-block"><summary>思考过程</summary><div class="tool-body">${m.thinking}</div></details>` : ''}
      ${m.steps ? m.steps.map(s => `<div class="step-line">${s.done ? '<span class="dot ok"></span>' : '<span class="dot idle"></span>'} ${s.t}</div>`).join('') : ''}
      ${m.error ? `<div class="error-banner" style="margin-top:8px"><div class="eb-title">出错了 · ${m.error}</div><div class="eb-body">内容没有变化，可以直接重试；也可以换个说法。</div>
        <div class="decision-actions"><button class="btn sm">重新生成</button><button class="btn sm ghost">换个说法</button></div></div>` : ''}
      ${m.actions !== false ? `<div class="msg-actions">
        <button class="iconbtn" title="复制全文" data-rt="msg-copy" data-text="${(m.text || '').replace(/"/g, '&quot;')}">${ico(I.doc, 13)}</button>
        <button class="iconbtn" title="引用">${ico(I.at, 13)}</button>
        <button class="iconbtn" title="重新生成">${ico(I.refresh, 13)}</button>
        <button class="iconbtn" title="分享">${ico(I.share, 13)}</button>
        <button class="iconbtn" title="更多" data-rt="msg-more">${ico(I.down, 13)}</button>
        <span class="costline" style="margin:0">${m.cost ? `共消耗 ${m.cost}` : ''}${m.model ? ` · ${m.model}` : ''}</span>
      </div>` : ''}
    </div></div>`;
  };

  /* Composer — Frozen X10 semantic slots: 输入/添加/访问权限/工作模式/执行者/发送 */
  const composer = (opt = {}) => `
    <div class="composer cx-anchor" id="${opt.id || 'composer'}" data-running="${opt.running ? '1' : ''}">
      ${opt.attach ? `<div class="attach-strip"><span class="chip">${ico(I.doc, 12)} ${opt.attach}</span></div>` : ''}
      <textarea class="cx-input" rows="${opt.rows || 1}" placeholder="${opt.placeholder || '给 TA 一句指令，或 @ 员工 / 资料 / 结果'}">${opt.value || ''}</textarea>
      <div class="cx-bar">
        <button class="iconbtn" data-action="cx-attach" title="添加附件">${ico(I.clip, 16)}</button>
        <button class="iconbtn" data-action="cx-ref" title="@ 引用">@</button>
        <span class="chip warn clickable" data-action="cx-perm">${ico(I.gear, 12)} ${opt.perm || '最小权限'}</span>
        <span class="chip clickable" data-action="cx-mode">${ico(I.spark, 12)} ${opt.mode || '对话'}</span>
        <span class="spacer"></span>
        <span class="chip clickable" data-action="cx-exec">${ico(I.users, 12)} ${opt.exec || '执行 · 自动选择'}</span>
        <span class="chip clickable cx-model" data-action="cx-model">${opt.model || 'GLM-5.3'} ${ico(I.down, 11)}</span>
        ${opt.running
          ? `<button class="cx-send stop" data-action="cx-stop" title="停止">${ico(I.stop, 14)}</button>`
          : `<button class="cx-send" data-action="cx-send" title="发送" ${opt.disabled ? 'disabled' : ''}>${ico(I.send, 14)}</button>`}
      </div>
      ${opt.status ? `<div class="costline">${opt.status}</div>` : ''}
    </div>`;

  const resultCard = r => {
    const e = FX.emp(r.employee);
    return `<div class="filecard" style="padding:12px" data-action="open-result" data-arg="${r.id}">
      <span class="fc-ico">${r.type === 'doc' ? 'DOC' : r.type === 'code' ? 'CODE' : 'XLSX'}</span>
      <span class="grow"><span class="fc-name">${r.title}</span><br>
        <span class="fc-meta">${e ? e.name + ' · ' : ''}${r.status === 'done' ? '已完成' : '待确认'} · 证据 ${r.evidence.length} 条 · 被 ${r.usedBy.length} 处引用</span></span>
      <span class="iconbtn">${ico(I.chev, 14)}</span></div>`;
  };

  const decisionBanner = d => `
    <div class="decision-banner" id="decision-${d.id}">
      <div class="db-title">需要 CEO 决定 · ${d.title}</div>
      <div class="db-body">${d.body}</div>
      <div class="decision-actions">${d.options.map((o, i) => `<button class="btn sm ${i === 0 ? 'primary' : ''}" data-action="decide" data-arg="${d.id}" data-opt="${i}">${o}</button>`).join('')}</div>
    </div>`;

  const emptyState = (title, sub, ideas = [], primary) => `
    <div class="empty">
      <div class="e-title">${title}</div>
      <div class="e-sub">${sub}</div>
      ${primary ? `<div style="margin-top:4px">${primary}</div>` : ''}
      ${ideas.length ? `<div class="e-ideas">${ideas.map(x => `<button data-action="${x.action || 'noop'}" data-arg="${x.arg || ''}">${ico(I.spark, 14)} ${x.t}</button>`).join('')}</div>` : ''}
    </div>`;

  const crumbs = parts => parts.map((p, i) => i === parts.length - 1 ? `<b>${p.t}</b>` : `<a href="#${p.go || ''}">${p.t}</a>`).join('<span class="sep">/</span>');

  return { I, ico, st, stFull, avatar, avatarById, empRow, todoList, progressBar, workCard, msg, composer, resultCard, decisionBanner, emptyState, crumbs, statusMeta };
})();

/* SVG 折线图与条形（Operating Intelligence；安静无装饰） */
C.lineChart = function (series, opt) {
  opt = opt || {};
  const w = opt.w || 560, h = opt.h || 140, max = Math.max.apply(null, series.map(function (x) { return x.v; })) * 1.15;
  const pts = series.map(function (s2, i) { return [24 + i * ((w - 40) / (series.length - 1)), h - 24 - (s2.v / max) * (h - 40)]; });
  const path = pts.map(function (p, i) { return (i ? 'L' : 'M') + p[0].toFixed(1) + ',' + p[1].toFixed(1); }).join(' ');
  const area = path + ' L' + pts[pts.length - 1][0] + ',' + (h - 24) + ' L' + pts[0][0] + ',' + (h - 24) + ' Z';
  return '<svg width="100%" viewBox="0 0 ' + w + ' ' + h + '" style="display:block">' +
    '<path d="' + area + '" fill="var(--ui-accent-soft)"/>' +
    '<path d="' + path + '" fill="none" stroke="var(--ui-accent)" stroke-width="2" stroke-linejoin="round"/>' +
    pts.map(function (p) { return '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="2.5" fill="var(--ui-accent)"/>'; }).join('') +
    series.map(function (s2, i) { return i % 2 ? '' : '<text x="' + (24 + i * ((w - 40) / (series.length - 1))) + '" y="' + (h - 6) + '" font-size="10" fill="var(--ui-text-3)" text-anchor="middle">' + s2.k + '</text>'; }).join('') +
    '</svg>';
};
C.bars = function (items) {
  const max = Math.max.apply(null, items.map(function (i) { return i[1]; }));
  return '<div style="display:flex;flex-direction:column;gap:8px">' + items.map(function (i) {
    return '<div style="display:flex;align-items:center;gap:10px;font-size:12px">' +
      '<span style="flex:0 0 72px;color:var(--ui-text-2)">' + i[0] + '</span>' +
      '<span style="flex:1;height:8px;border-radius:999px;background:var(--ui-surface-2);overflow:hidden"><i style="display:block;height:100%;width:' + (i[1] / max * 100).toFixed(1) + '%;background:var(--ui-accent);opacity:.8;border-radius:999px"></i></span>' +
      '<span class="mono" style="flex:0 0 54px;text-align:right;color:var(--ui-text-2)">' + (i[2] || i[1]) + '</span></div>';
  }).join('') + '</div>';
};
