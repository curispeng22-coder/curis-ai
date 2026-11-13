/* ============================================================
   rt.js — HIFI 共享运行时 v2（Prototype 内存态，不接 Runtime）
   Frozen Shell §3.5 Composer 槽位 + Final Decisions Z044–Z075 / EV04·EV06·EV10
   修复 Codex INT-01~05：Send 启用、Stop 取消回复、Queue 真实消费、
   More 菜单真实动作、菜单 body 级 containment、Settings 搜索接线。
   ============================================================ */
window.RT = (function () {
  const FILES = [
    { name: '竞品选题结构周报 8/12–8/19.xlsx', meta: '表格 · 38 KB · 公司资料库' },
    { name: '品牌表达手册 v2.pdf', meta: 'PDF · 1.2 MB · 公司资料库' },
    { name: 'auth.service.ts', meta: '代码 · product-platform/src/auth' },
    { name: '损坏文件.docx', meta: '无法读取 · 上传将失败' },
  ];
  const REFS = [
    { kind: 'emp', label: '@林月', sub: '调研 / 文案' },
    { kind: 'emp', label: '@周岚', sub: '开发工程师' },
    { kind: 'file', label: '#登录模块验收口径', sub: '资料库' },
    { kind: 'result', label: '#登录模块 v1.3 联调结果', sub: 'Result' },
  ];
  const S = {
    composers: {}, threads: {}, threadSeeded: {}, threadActive: {},
    settings: { ceoName: 'CEO', lang: '简体中文', startup: 'CEO 工作台' },
    touch: function (key) { this.threadActive[key] = Date.now(); },
  };

  function composer(cid, opt) {
    opt = opt || {};
    const st = S.composers[cid] || (S.composers[cid] = {
      text: '', attachments: [], refs: [],
      model: opt.model || 'GLM-5.3', exec: opt.exec || '执行 · 自动选择',
      perm: '最小权限', permNote: '', mode: '对话',
      status: 'idle', queue: 0, queuedTexts: [], runToken: 0,
    });
    if (opt.model && st.model === 'GLM-5.3') st.model = opt.model;
    if (opt.exec && st.exec === '执行 · 自动选择') st.exec = opt.exec;
    st.opt = opt;
    const canSend = st.text.trim().length > 0 && (st.status === 'idle' || st.status === 'stopped');
    const isRunning = st.status === 'running' || st.status === 'sending';
    const chip = (label, act, cls) => '<button class="chip clickable ' + (cls || '') + '" data-rt="' + act + '" data-cid="' + cid + '">' + label + '</button>';
    const attachHtml = st.attachments.map(function (a, i) {
      const icoHtml = a.failed ? '<span class="dot err"></span>' : (a.uploading ? '<span class="dot idle"></span>' : C.ico(C.I.doc, 12));
      const stat = a.uploading ? ' <span class="faint">上传中…</span>' : (a.failed ? ' <span class="faint" style="color:var(--ui-danger)">失败</span>' : '');
      const rm = a.uploading ? '' : '<span class="chip-x" data-rt="rm-attach" data-cid="' + cid + '" data-i="' + i + '">×</span>';
      return '<span class="chip attach">' + icoHtml + ' ' + a.name + stat + rm + '</span>';
    }).join('');
    const refHtml = st.refs.map(function (r, i) {
      return '<span class="chip attach ref">' + r.label + '<span class="chip-x" data-rt="rm-ref" data-cid="' + cid + '" data-i="' + i + '">×</span></span>';
    }).join('');
    return '<div class="composer cx-anchor" id="' + cid + '" data-running="' + (isRunning ? 1 : 0) + '" data-thread="' + (opt.thread || '') + '">' +
      ((st.attachments.length || st.refs.length) ? '<div class="attach-strip">' + attachHtml + refHtml + '</div>' : '') +
      '<textarea class="cx-input" rows="1" data-rt="input" data-cid="' + cid + '" placeholder="' + (opt.placeholder || '给 TA 一句指令，或 @ 员工 / # 引用文件与结果') + '">' + st.text + '</textarea>' +
      '<div class="cx-bar">' +
      '<button class="iconbtn" data-rt="menu-add" data-cid="' + cid + '" title="添加附件">' + C.ico(C.I.clip, 16) + '</button>' +
      '<button class="iconbtn" data-rt="menu-ref" data-cid="' + cid + '" title="@ 员工 / # 引用">' + C.ico(C.I.at, 16) + '</button>' +
      chip(C.ico(C.I.gear, 12) + ' ' + st.perm, 'cycle-perm', st.perm === '完全访问' ? 'warn' : '') +
      chip(C.ico(C.I.spark, 12) + ' ' + st.mode, 'menu-mode') +
      '<span class="spacer"></span>' +
      chip(C.ico(C.I.users, 12) + ' ' + st.exec, 'menu-exec') +
      chip(st.model + ' ' + C.ico(C.I.down, 11), 'menu-model', 'cx-model') +
      (isRunning
        ? '<button class="cx-send stop" data-rt="stop" data-cid="' + cid + '" title="停止（保留已完成部分）">' + C.ico(C.I.stop, 14) + '</button>'
        : '<button class="cx-send" data-rt="send" data-cid="' + cid + '" title="发送"' + (canSend ? '' : ' disabled') + '>' + C.ico(C.I.send, 14) + '</button>') +
      '</div>' +
      (isRunning ? '<div class="costline"><span class="dot run"></span>运行中' + (st.queue ? ' · 队列 ' + st.queue + ' 条' : '') + ' · 发送将排队（Steering）</div>' : '') +
      (st.status === 'stopped' ? '<div class="costline"><span class="dot warn"></span>已停止 · 已完成部分保留</div>' : '') +
      (st.permNote ? '<div class="costline">' + st.permNote + '</div>' : '') +
      '</div>';
  }

  function threadSeed(key) {
    if (!S.threads[key]) {
      S.threads[key] = [];
      if (key.indexOf('emp:') === 0) S.threads[key] = CONV.forEmployee(key.slice(4)).slice();
      else if (key === 'assistant') S.threads[key] = FX.assistantThread.map(function (m) { return { role: m.role, text: m.text }; });
    }
    return S.threads[key];
  }
  function renderThread(key, opt) {
    opt = opt || {};
    const msgs = threadSeed(key);
    if (!msgs.length) return C.emptyState(opt.emptyTitle || '开始这段对话', opt.emptySub || '发送第一条消息；对话锚定当前工作。', []);
    return msgs.map(function (m) { return C.msg(m); }).join('');
  }
  function appendMsg(key, m) { S.touch(key); threadSeed(key).push(m); }

  function employeeReply(key, empId, userText, token, onDone) {
    const e = FX.emp(empId);
    setTimeout(function () {
      const cancelled = Object.keys(S.composers).some(function (c) { return (S.composers[c].runToken || 0) > token; });
      if (cancelled) return;
      appendMsg(key, {
        role: 'ai', emp: empId,
        text: '收到：「' + (userText || '').slice(0, 24) + (userText.length > 24 ? '…' : '') + '」。' + (e ? '我当前责任是「' + e.responsibility.current + '」，先按这个口径推进，完成后把 Result 引用发回这里。' : ''),
        model: e ? e.model : 'GLM-5.3', cost: '◇ 0.3',
        tools: [{ n: '读取工作上下文', d: '当前 Work / 责任范围 / 相关资料（Prototype 演示）' }],
      });
      if (onDone) onDone();
    }, 1400);
  }
  function drainQueue(cid) {
    const st = S.composers[cid];
    if (!st || !(st.queuedTexts || []).length || st.status === 'running' || st.status === 'sending') return;
    st.text = st.queuedTexts.shift(); st.queue = st.queuedTexts.length;
    setTimeout(function () { handle('send', { dataset: { cid: cid } }); }, 80);
  }

  function openMenu(anchor, items, current, onPick) {
    document.querySelectorAll('.menu-pop').forEach(function (x) { x.remove(); });
    const pop = document.createElement('div');
    pop.className = 'menu-pop';
    pop.innerHTML = items.map(function (it) { return '<button class="mi ' + (it === current ? 'sel' : '') + '">' + (it === current ? C.ico(C.I.check, 13) + ' ' : '') + it + '</button>'; }).join('');
    document.body.appendChild(pop);
    const ar = anchor.getBoundingClientRect();
    pop.style.position = 'fixed'; pop.style.visibility = 'hidden';
    const pr = pop.getBoundingClientRect();
    let top = ar.bottom + 6;
    if (top + pr.height > window.innerHeight - 8) top = Math.max(8, ar.top - pr.height - 6);
    pop.style.top = top + 'px';
    pop.style.left = Math.max(8, Math.min(ar.left, window.innerWidth - pr.width - 8)) + 'px';
    pop.style.visibility = 'visible';
    pop.querySelectorAll('.mi').forEach(function (el, i) {
      el.addEventListener('click', function () { onPick(items[i]); pop.remove(); });
    });
    setTimeout(function () {
      document.addEventListener('click', function close(e) { if (!pop.contains(e.target)) { pop.remove(); document.removeEventListener('click', close); } });
    }, 0);
  }

  function isRunning(st) { return st.status === 'running' || st.status === 'sending'; }

  function handle(act, el) {
    const cid = el.dataset.cid;
    const st = cid ? S.composers[cid] : null;
    const key = st && st.opt ? st.opt.thread : null;
    function rerender() { if (st && st.opt && st.opt.onChange) st.opt.onChange(); else if (window.PROTO) PROTO.render(); }
    switch (act) {
      case 'input': {
        st.text = el.value; el.style.height = 'auto';
        el.style.height = Math.min(el.scrollHeight, 160) + 'px';
        const send = el.closest('.composer').querySelector('.cx-send');
        if (send && el.closest('.composer').dataset.running !== '1') send.disabled = !st.text.trim();
        return true;
      }
      case 'menu-add': {
        openMenu(el, FILES.map(function (f) { return f.name; }), null, function (name) {
          const f = Object.assign({}, FILES.find(function (x) { return x.name === name; }));
          f.failed = name.indexOf('损坏') === 0; f.uploading = !f.failed;
          st.attachments.push(f); rerender();
          if (f.uploading) setTimeout(function () { f.uploading = false; rerender(); }, 900);
        }); return true;
      }
      case 'menu-ref': {
        openMenu(el, REFS.map(function (r) { return r.label; }), null, function (label) {
          st.refs.push(REFS.find(function (r) { return r.label === label; })); rerender();
        }); return true;
      }
      case 'rm-attach': st.attachments.splice(+el.dataset.i, 1); rerender(); return true;
      case 'rm-ref': st.refs.splice(+el.dataset.i, 1); rerender(); return true;
      case 'menu-model': {
        openMenu(el, ['GLM-5.3', 'DeepSeek-V4.1', 'GPT（未配置 · 需输入 Key）'], st.model, function (v) {
          if (v.indexOf('未配置') > -1) { st.permNote = '该模型未配置：在 左下头像菜单 → 模型配置 输入 Key 后可用（unavailable 需解释并禁用）。'; rerender(); return; }
          st.model = v; st.permNote = ''; rerender();
        }); return true;
      }
      case 'menu-exec': {
        openMenu(el, ['执行 · 自动选择', '执行 · 负责人', '执行 · 指定员工…', '仅讨论，不执行'], st.exec, function (v) { st.exec = v; rerender(); }); return true;
      }
      case 'menu-mode': {
        openMenu(el, ['对话', '派工作', '研究', '审查'], st.mode, function (v) { st.mode = v; rerender(); }); return true;
      }
      case 'cycle-perm': {
        const perms = ['最小权限', '白名单放行', '完全访问'];
        st.perm = perms[(perms.indexOf(st.perm) + 1) % perms.length];
        st.permNote = st.perm === '完全访问'
          ? 'requested：完全访问 · configured：已启用 · effective：本会话生效（写操作留审计）。档位 ≠ 沙箱生效，详见 设置 → 权限与数据。'
          : (st.perm === '白名单放行' ? 'requested：白名单放行 · effective：仅「只读外部检索」在白名单内生效。' : '');
        rerender(); return true;
      }
      case 'send': {
        if (!st.text.trim()) return true;
        if (isRunning(st)) {
          st.queue = (st.queue || 0) + 1;
          st.queuedTexts.push(st.text);
          if (key) appendMsg(key, { role: 'sys', text: '已排队（第 ' + st.queue + ' 条）· 当前运行结束后自动发送' });
          st.text = ''; rerender(); return true;
        }
        const text = st.text; st.text = '';
        if (st.status === 'stopped' && key) appendMsg(key, { role: 'sys', text: '继续上次中断的任务（已完成部分保留）' });
        if (key) appendMsg(key, { role: 'user', text: text, atts: st.attachments.map(function (a) { return a.name; }), refs: st.refs.map(function (r) { return r.label; }) });
        st.attachments = []; st.refs = [];
        const myToken = ++st.runToken;
        st.status = 'running';
        if (key === 'assistant') {
          rerender();
          setTimeout(function () {
            if (st.runToken !== myToken) return;
            appendMsg(key, { role: 'ai', text: '已处理：「' + text.slice(0, 30) + '」。当前 3 个工作运行中、1 项待你决定（AI 工具测评定位调整）。需要我展开哪一项？', model: st.model, cost: '◇ 0.2' });
            st.status = 'idle'; drainQueue(cid); rerender();
          }, 1600);
        } else {
          const empId = key && key.indexOf('emp:') === 0 ? key.slice(4) : null;
          if (key) appendMsg(key, { role: 'sys', text: '已发送 · Employee 开始处理', model: st.model });
          rerender();
          employeeReply(key, empId, text, myToken, function () { if (st.runToken !== myToken) return; st.status = 'idle'; drainQueue(cid); rerender(); });
        }
        rerender(); return true;
      }
      case 'stop': {
        st.runToken = (st.runToken || 0) + 1;
        st.status = 'stopped';
        if (key && key.indexOf('emp:') === 0) appendMsg(key, { role: 'ai', emp: key.slice(4), text: '【已停止】已完成部分保留，未完成部分不再继续；发送新指令即可继续。', model: st.model, cost: '◇ 0.1' });
        rerender(); return true;
      }
      case 'msg-copy': if (navigator.clipboard) navigator.clipboard.writeText(el.dataset.text || ''); el.title = '已复制 ✓'; return true;
      case 'msg-regen': {
        if (el.closest('.as-body')) {
          const st2 = S.composers['assistant'];
          if (st2) {
            st2.status = 'running'; rerender();
            setTimeout(function () { appendMsg('assistant', { role: 'ai', text: '（已重新生成）换个角度：优先解阻塞——回归测试被联调卡住，释放它即可进入发布检查。' }); st2.status = 'idle'; rerender(); }, 1200);
          }
        }
        return true;
      }
      case 'msg-more': {
        const host = el.closest('[data-thread]');
        const key2 = host ? host.dataset.thread : (el.closest('.as-body') ? 'assistant' : null);
        openMenu(el, ['复制全文', '引用到新指令', '升级给我（CEO）', '标记问题'], null, function (v) {
          if (v === '复制全文') { if (navigator.clipboard) navigator.clipboard.writeText((el.closest('.msg') || document).textContent.trim()); return; }
          if (v === '引用到新指令') {
            const c = document.querySelector('#main-content .composer textarea.cx-input');
            if (c) { const b = el.closest('.msg'); c.value += ' 「' + (b ? b.querySelector('.bubble').textContent.slice(0, 20) : '') + '…」'; c.dispatchEvent(new Event('input', { bubbles: true })); c.focus(); }
            return;
          }
          if (key2) { appendMsg(key2, { role: 'sys', text: v + ' · 已记录（原型）' }); rerender(); }
        }); return true;
      }
    }
    return false;
  }

  document.addEventListener('click', function (ev) {
    const el = ev.target.closest('[data-rt]');
    if (!el || el.dataset.rt === 'input') return false;
    ev.stopPropagation();
    return handle(el.dataset.rt, el);
  });
  document.addEventListener('input', function (ev) {
    const el = ev.target.closest('[data-rt="input"]');
    if (el) handle('input', el);
    const ss = ev.target.closest('[data-action="settings-search"]');
    if (ss) {
      const base = location.hash.split('?')[0];
      const sec = base.indexOf('/settings/') > -1 ? base.split('/settings/')[1] : 'personal';
      clearTimeout(window.__ssT);
      window.__ssT = setTimeout(function () { location.hash = '#/settings/' + (sec || 'personal') + '?q=' + encodeURIComponent(ss.value); }, 250);
    }
  });
  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Enter' && !ev.shiftKey) {
      const el = ev.target.closest('[data-rt="input"]');
      if (el) { ev.preventDefault(); handle('send', { dataset: { cid: el.dataset.cid } }); }
    }
  });

  return { S: S, composer: composer, threadSeed: threadSeed, renderThread: renderThread, appendMsg: appendMsg, handle: handle, openMenu: openMenu, FILES: FILES, REFS: REFS };
})();
