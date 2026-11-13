/* ============================================================================
   Writing Business HTML Exploration — 应用骨架
   职责：状态与持久化、路由与返回、Chrome（导航/面包屑/高频入口/上下文侧栏）、
        抽屉 / 弹层 / 提示、员工对话、以及所有会改变原型状态的行动 API。
   约束：无后端、无网络请求、不改真实对象；localStorage 仅保存本机演示状态。
   ========================================================================== */
window.WB = (function () {
  var D = window.WB_DATA;
  var STORE_KEY = 'curis.writing.exploration.v1';
  var BACKUP_PREFIX = 'curis.writing.exploration.backup.';
  /* w3：正文三态（草稿 / 正式稿 / 线上稿）真实分离，各自保留可回查的正文快照；
         讨论成为真实过程（作者要求 → 员工接管范围 → 可编辑提案 → 部分接受/拒绝/继续讨论）。
     w4：创作选择词库 L01–L24 进入定位与章节要求；三栏（左 Context / 中 Main / 右 Utility）
         可收起、可调宽；完整员工 Conversation 移入 Main 的 Shared Work Area（不再是右侧抽屉）。
     w5：新开书成为可继续的创作过程（从想法 / 导入旧稿 / 先手写三条起步路径）；作者原话构思
         原样存入 positioning.seed，编辑据此给出含具体故事内容与取舍的方向候选；员工入口提到
         当前对象首屏（不再埋在长内容末尾）。
     迁移策略：备份旧状态 → 保留用户既有编辑 → 只在缺失处补齐结构，绝不清空本地状态。 */
  var VERSION = 'w5';

  /* ---------------- 基础工具 ---------------- */
  function clone(o) { return JSON.parse(JSON.stringify(o)); }
  function mixParams(p, extra) {
    var o = {}, k;
    for (k in (p || {})) if (Object.prototype.hasOwnProperty.call(p, k)) o[k] = p[k];
    for (k in (extra || {})) if (Object.prototype.hasOwnProperty.call(extra, k)) o[k] = extra[k];
    return o;
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function now() {
    var d = new Date();
    function p(n) { return (n < 10 ? '0' : '') + n; }
    return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate()) + ' ' + p(d.getHours()) + ':' + p(d.getMinutes());
  }

  /* ---------------- 状态 ---------------- */
  var S = null;
  var storageOK = true;

  function blankState() {
    var s = clone(D);
    s.__runtime = {
      createdBooks: [], stock: { 'B-01': { publishable: 0, planned: 1, draft: 1 } },
      toasts: [], fixes: {}, log: [], pendingReceipt: {}, newWorks: 0
    };
    s.craftProposals = [];
    s.reviewRuns = [];
    s.discussProps = {};   /* 讨论产生的提案（带逐项裁定状态），键 = DP-n */
    s.__route = { area: 'operate', view: 'home', params: {} };
    s.__scope = { bookId: 'B-01' };
    s.__sel = {};
    s.__hist = [];
    /* 三栏是可使用的空间，不是永久占位：左 Context / 中 Main / 右 Utility 各自可开合。
       右 Utility 默认收起（§17.1）；Main 保底显示当前书/章/页面名与打开入口。 */
    s.__ui = { rail: true, aside: false, railW: null, asideW: null };
    /* 完整员工 Conversation 在 Main 的 Shared Work Area（不是右侧抽屉）：可收起但不停工。 */
    s.__conv = { open: false, empId: null, obj: null, objLabel: null, collapsed: false };
    s.__pick = null;       /* 创作选择弹框草稿：{ scopeKey, dims:{}, dirty } —— 关弹框回原草稿 */
    s.__msDraft = {};      /* 正文手写未保存缓冲（按章键）；只有保存或取消才清空 */
    return s;
  }

  /* 版本迁移：升级本地结构时保留用户已存编辑。
     不以「清空 localStorage」换取测试通过——已存的裁决、版本、对话与手写稿都保留。
     迁移前先把旧载荷整体备份到 BACKUP_PREFIX + 旧版本号（轻量备份，可回查）。 */
  function adoptOld(old) {
    var s = blankState();                                   /* 新版默认结构（含 craft / craftProposals 等） */
    Object.keys(old || {}).forEach(function (k) { s[k] = old[k]; });   /* 用户原有值整体保留 */
    return s;
  }
  var MIGRATIONS = { w1: adoptOld, w2: adoptOld, w3: adoptOld, w4: adoptOld };

  /* 正文三态读取：草稿（paragraphs）/ 正式稿快照（formal）/ 线上稿快照（published）。
     旧结构里正文即正式/线上稿，这里只补齐只读快照，便于三态并置与回退；
     w3 以后由确认流程写入快照，此处不覆盖既有快照。 */
  function msOf(ck) {
    var ms = S.manuscripts[ck];
    if (!ms) return null;
    if (!Array.isArray(ms.paragraphs)) ms.paragraphs = [];
    if (!Array.isArray(ms.versions)) ms.versions = [];
    var ch = S.chapters[ck] || null;
    if (!ms.formal && ms.formalVersion) {
      ms.formal = { version: ms.formalVersion, paragraphs: ms.paragraphs.slice(),
        acceptedAt: (ch && ch.formalAcceptedAt) || null,
        note: '（由既有数据补齐：该章当前正文即正式稿快照）' };
    }
    if (!ms.published && ch && ch.published) {
      ms.published = { version: ch.published,
        paragraphs: (ms.formal ? ms.formal.paragraphs : ms.paragraphs).slice(),
        at: ch.publishedAt || null, note: '（由既有数据补齐：核验时的线上版本快照）' };
    }
    return ms;
  }
  /* 新建正文容器（首次手写 / 生成候选 / 导入）：草稿为空、无正式稿、无线上稿。
     起始占位记录**不携带正文快照**（paragraphs: null）：它只是「尚无正文」的说明，
     若携带空数组会被版本历史当成「0 段可读快照」并可被取回，从而把草稿清空。 */
  function msEnsure(ck, bookId, title, note) {
    if (!S.manuscripts[ck]) {
      S.manuscripts[ck] = { bookId: bookId, no: (S.chapters[ck] || {}).no || 0,
        title: title || '', paragraphs: [], draftNote: note || '作者草稿（未确认）',
        formalVersion: null, formal: null, published: null,
        versions: [{ v: '草稿 r1', at: now(), kind: 'draft',
          note: (note || '作者手写起始') + '；此时尚未写入正文（不提供取回）', paragraphs: null }] };
    }
    return msOf(ck);
  }
  /* 草稿与正式稿是否已分叉（用于三态并置提示，不用于自动合并） */
  function draftDiverged(ck) {
    var ms = msOf(ck);
    if (!ms || !ms.formal) return false;
    return ms.paragraphs.join('\n') !== (ms.formal.paragraphs || []).join('\n');
  }
  /* 历史快照是否携带可读正文（早期版本无快照时如实标注，不假装有） */
  function snapshotOf(ck, vi) {
    var ms = msOf(ck);
    if (!ms) return null;
    var v = ms.versions[vi];
    return v || null;
  }
  function normalizeAll() {
    if (!Array.isArray(S.marketSnapshots)) S.marketSnapshots = clone(D.marketSnapshots);
    (S.watches || []).forEach(function (w) {
      if (!w.scope) w.scope = w.name;
      if (!w.focus) w.focus = '题材、新书与指定作品';
      if (!w.window) w.window = '最近 7 日';
      if (!w.metrics) w.metrics = '排名；其他字段按来源可得性';
    });
    if (!S.employees.some(function(e){return e.id==='E-05';})) S.employees.push({id:'E-05',name:'许清禾',role:'独立审校编辑',initials:'许',color:'#60766b',resp:['R-REVIEW 审稿与校对']});
    if (!S.responsibilities.some(function(r){return r.id==='R-REVIEW';})) S.responsibilities.push({id:'R-REVIEW',name:'审稿与校对',owner:'E-05',area:'book'});
    Object.keys(S.manuscripts || {}).forEach(function (k) { msOf(k); });
    /* w5：为所有书补齐「作者原话构思」与「起步过程」。只补缺失字段，不覆盖作者既有内容。 */
    allBooks().forEach(function (b) {
      var p = craftOf(b.id).positioning;
      if (p.seed === undefined) p.seed = null;
      if (p.seedAt === undefined) p.seedAt = null;
      if (p.seedBy === undefined) p.seedBy = null;
      if (!p.fields) p.fields = {};
      if (p.fields.seed === undefined) p.fields.seed = p.seed ? 'confirmed' : 'empty';
      onbOf(b.id);
    });
  }

  /* ---------------- 创作选择词库 L01–L24（读取 / 归一化 / 转写作要求） ----------------
     约束：词库是「定位 / 写作偏好 / 章节要求」的字段，不新建第二套标签 Runtime；
           旧数据（w1–w3）没有 tags 时得到空对象——只是「还没有选择」，绝不清空任何用户值。 */
  var TAG_BY_ID = {};
  (D.writingTags || []).forEach(function (t) { TAG_BY_ID[t.id] = t; });
  function tagDef(id) { return TAG_BY_ID[id] || null; }
  function writingTags() { return D.writingTags || []; }
  function tagGroups() { return D.tagGroups || []; }
  function tagSuggestions() { return D.tagSuggestions || []; }
  /* 新书起步（D05）：三条起步方式与编辑的方向候选模板，来自 data.js 单一来源 */
  function startPaths() { return D.startPaths || []; }
  function startDirections() { return D.startDirections || []; }
  function tagEntryNorm(v) {
    if (Array.isArray(v)) return { sel: v.slice(), note: '', req: '', custom: '' };
    if (v && typeof v === 'object') {
      var o = {}; Object.keys(v).forEach(function (k) { o[k] = v[k]; });
      if (o.sel != null && !Array.isArray(o.sel)) o.sel = [];
      return o;
    }
    return {};
  }
  function tagEntry(id, v) {
    var def = tagDef(id) || {};
    var e = tagEntryNorm(v);
    if (def.optGroups && e.sel == null) e.sel = null;     /* 组合维度用分组键存，不用 sel */
    return e;
  }
  /* 组合维度的分组键：L05 → L05a / L05b；单选维度用 L67a 形式以避免与 L04 等真实 ID 冲突 */
  function tagSubKey(id, gi) { return 'L' + id.replace(/^L/, '') + String.fromCharCode(97 + gi); }
  function tagsOf(c) {
    if (!c) return {};
    if (!c.positioning) c.positioning = {};
    var pos = c.positioning;
    if (!pos.tags || typeof pos.tags !== 'object') pos.tags = {};
    if (!pos.tagScope) pos.tagScope = 'book';
    Object.keys(pos.tags).forEach(function (id) { pos.tags[id] = tagEntry(id, pos.tags[id]); });
    return pos.tags;
  }
  /* 某一维度在本书的已选（展平，含组合维度各分组）；returns { sel:[], groups:[[],..] } */
  function tagPicked(tags, id) {
    var def = tagDef(id) || {}, e = tags[id] || {}, sel = [], groups = [];
    if (Array.isArray(e.sel)) sel = sel.concat(e.sel);
    (def.optGroups || []).forEach(function (g, gi) {
      var k = tagSubKey(id, gi), arr = Array.isArray(e[k]) ? e[k] : [];
      groups.push(arr); sel = sel.concat(arr);
    });
    sel = sel.filter(function (x) { return x && x !== '（待定）'; });
    return { sel: sel, groups: groups };
  }
  /* 维度是否已被作者选择过（用于「少量关键已选项」与覆盖统计） */
  function tagTouched(tags, id) {
    var e = tags[id];
    if (!e) return false;
    if (e.undecided) return true;                        /* 「待定」也是作者的一次显式选择 */
    if (Array.isArray(e.sel) && e.sel.length) return true;
    if (typeof e.custom === 'string' && e.custom.trim()) return true;
    if (typeof e.note === 'string' && e.note.trim()) return true;
    var def = tagDef(id) || {};
    for (var gi = 0; gi < (def.optGroups || []).length; gi++) {
      var a = e[tagSubKey(id, gi)];
      if (Array.isArray(a) && a.length) return true;
    }
    return false;
  }
  /* 已选 → 可编辑的自然语言写作要求（标签不是终点：选择必须能转成要求并被修改） */
  function tagRequirement(tags, id, scopeLabel) {
    var def = tagDef(id) || {}, e = tags[id] || {};
    var p = tagPicked(tags, id), sel = p.sel;
    if (typeof e.req === 'string' && e.req.trim()) return e.req.trim();
    if (!sel.length && !e.custom && !e.note) return '';
    var parts = [];
    if (sel.length) parts.push(sel.join('、'));
    if (e.custom) parts.push('自定义：' + e.custom);
    if (typeof e.note === 'string' && e.note.trim()) parts.push(e.note.trim());
    return '【' + (scopeLabel || def.name || id) + '】' + parts.join('；') +
      '。（转成本次要遵守的写作要求；可直接改写这句话。）';
  }
  /* 本书全部已选 → 写作依据摘要（D12/D06 共用；只读，不写回） */
  function tagBrief(c, ids) {
    var tags = tagsOf(c), out = [];
    (ids || Object.keys(tags)).forEach(function (id) {
      var def = tagDef(id); if (!def) return;
      var p = tagPicked(tags, id);
      if (p.sel.length) out.push({ id: id, name: def.name, sel: p.sel });
    });
    return out;
  }
  /* 章级临时覆盖：chapters[ck].tagOverride = { <Lxx>: {sel|subkeys...}, _on:true } */
  function chapterTagOverride(ck, id) {
    var ch = S.chapters[ck]; if (!ch || !ch.tagOverride || !ch.tagOverride._on) return null;
    return ch.tagOverride[id] || null;
  }

  function load() {
    try {
      var raw = window.localStorage.getItem(STORE_KEY);
      if (raw) {
        var p = JSON.parse(raw);
        if (p && p.v === VERSION) { S = p.s; normalizeAll(); return; }
        if (p && p.v && MIGRATIONS[p.v]) {
          try {
            window.localStorage.setItem(BACKUP_PREFIX + p.v, raw);
          } catch (e2) { /* 备份失败不阻断迁移，但要在日志里说清 */ logStep('旧状态备份失败（存储配额）：迁移仍继续'); }
          S = MIGRATIONS[p.v](p.s);
          normalizeAll();
          logStep('演示状态已从 ' + p.v + ' 迁移到 ' + VERSION + '（保留既有编辑；旧状态已备份至 ' + BACKUP_PREFIX + p.v + '）');
          save(); return;
        }
        logStep('已存在的演示状态版本不一致且无迁移路径，重新初始化');
      }
    } catch (e) { storageOK = false; }
    S = blankState();
    save();
  }
  function save() {
    if (!storageOK) return;
    try { window.localStorage.setItem(STORE_KEY, JSON.stringify({ v: VERSION, s: S })); }
    catch (e) { storageOK = false; toast('浏览器存储不可用，本次改动只保留在内存中（刷新会丢失）', 'warn'); }
  }
  function reset() {
    try { window.localStorage.removeItem(STORE_KEY); } catch (e) {}
    S = blankState(); save();
  }
  function logStep(t) { S.__runtime.log.push({ at: now(), t: t }); if (S.__runtime.log.length > 60) S.__runtime.log.shift(); }

  /* ---------------- 读取助手 ---------------- */
  function byId(arr, id) { for (var i = 0; i < arr.length; i++) if (arr[i].id === id) return arr[i]; return null; }
  function book(id) { return byId(S.books, id) || byId(S.__runtime.createdBooks, id); }
  function allBooks() { return S.books.concat(S.__runtime.createdBooks || []); }
  function emp(id) { return id ? byId(S.employees, id) : null; }
  function chapter(key) { return S.chapters[key] || null; }
  function candidate(id) { return S.candidates[id] || null; }
  function decision(id) { return byId(S.decisions, id); }
  function learning(id) { return byId(S.learnings, id); }
  function watch(id) { return byId(S.watches, id); }
  function queueItem(id) { return byId(S.queue, id); }
  function analysis(id) { return byId(S.analyses, id); }
  function scopeBook() { return book(S.__scope.bookId); }

  /* ---------------- 创作内核读取 ----------------
     创作对象一律绑定本书：找不到本书资料时返回空结构（TO_EXPLORE + 空数组），
     绝不回退到另一本作品的样例。 */
  function blankCraftFor(bookId, title) { return D.blankCraft(bookId, title); }
  function craftOf(bookId) {
    var b = book(bookId);
    if (!S.craft) S.craft = {};
    if (!S.craft[bookId]) S.craft[bookId] = blankCraftFor(bookId, b ? b.title : null);
    var c = S.craft[bookId];
    /* 容错：补齐可能缺失的子键（迁移或手工数据） */
    if (!c.positioning) c.positioning = blankCraftFor(bookId, b ? b.title : null).positioning;
    ['world', 'outline', 'characters', 'importRecords', 'reviewRuns', 'impactLog'].forEach(function (k) { if (!c[k]) c[k] = []; });
    if (!c.scenes) c.scenes = {};
    if (!c.arc) c.arc = blankCraftFor(bookId, b ? b.title : null).arc;
    if (!c.bookId) c.bookId = bookId;
    return c;
  }
  /* ---------------- 新书起步过程（D05：开书不是只建空卡） ----------------
     每本书有一条起步记录：走了哪条路、作者原话是什么、编辑接手到哪一步。
     「下一步」不靠存死状态，而是从本书真实资料推导 —— 中断回来自然能继续，也不会反复新建书。 */
  function onbOf(bookId) {
    var b = book(bookId);
    if (!b) return null;
    if (!b.onboarding || typeof b.onboarding !== 'object') {
      b.onboarding = { path: b.imported ? 'import' : 'write', step: 'idle', seed: null, dirId: null,
        planSkipped: false, startedAt: b.startedAt || null, updatedAt: null };
    }
    var o = b.onboarding;
    if (o.step === undefined) o.step = 'idle';
    if (o.dirId === undefined) o.dirId = null;
    if (o.seed === undefined) o.seed = null;
    if (o.planSkipped === undefined) o.planSkipped = false;
    return o;
  }
  /* 起步阶梯：顺序是建议不是门禁——任何一步都可跳过，未填不阻止写作 */
  var ONB_STEPS = [
    { id: 'idea', name: '写下你的想法', owner: 'R3',
      hint: '一两句话就够，不用先定读者、题材、平台。编辑会据此提出方向候选。' },
    { id: 'dir', name: '选定一个方向', owner: 'R3',
      hint: '编辑给出两三种方向（含具体故事内容、差异与取舍）；你可以改、可以选、也可以先不定。' },
    { id: 'base', name: '补这本书要用的少量设定', owner: 'R3',
      hint: '只补这一章真的会用到的：一个背景规则，或一个人物的动机。其余留待探索，不必先建满。' },
    { id: 'plan', name: '定走向，或直接准备第一章', owner: 'R3',
      hint: '可从主支线或结局起步，也可以跳过规划直接手写——跳过不等于缺失。' },
    { id: 'first', name: '拿到第一章候选', owner: 'R3',
      hint: '先试一个开头：结果进草稿或候选，逐项采纳即可。生成 ≠ 定稿 ≠ 发布。' }
  ];
  function onbState(bookId) {
    var c = craftOf(bookId), p = c.positioning, o = onbOf(bookId) || {};
    var chs = Object.keys(S.chapters || {}).filter(function (k) { return S.chapters[k].bookId === bookId; });
    var hasSeed = !!(p.seed || p.coreOriginal);
    var hasDir = !!(p.coreOriginal && (p.genres || []).length);
    var hasBase = (c.world || []).length > 0 || (c.characters || []).length > 0;
    /* 「已定走向」只认走向这一步自己的产物：大纲节点 / 支线 / 结局，或显式跳过。
       故事前提（arc.premise）属于「方向」；主线（arc.mainLines）可能由「补设定」写入，
       两者都不能拿来当作已经定过走向——否则采纳设定后会直接跳过「定走向」。 */
    var hasPlan = (c.outline || []).length > 0 ||
      !!((c.arc && (((c.arc.subLines || []).length) || ((c.arc.endings || []).length)))) || !!o.planSkipped;
    var hasMs = chs.some(function (k) { var m = S.manuscripts[k]; return !!(m && m.paragraphs && m.paragraphs.length); });
    var cands = Object.keys(S.candidates || {}).filter(function (x) {
      return S.candidates[x].chapter && S.chapters[S.candidates[x].chapter] &&
        S.chapters[S.candidates[x].chapter].bookId === bookId; }).length;
    var idx = 0;
    if (hasSeed) idx = 1;
    if (hasDir) idx = 2;
    if (hasBase) idx = 3;
    if (hasPlan) idx = 4;
    if (hasMs || cands) idx = 5;
    return { idx: idx, done: idx >= ONB_STEPS.length, step: idx < ONB_STEPS.length ? ONB_STEPS[idx] : null,
      hasSeed: hasSeed, hasDir: hasDir, hasBase: hasBase, hasPlan: hasPlan, hasMs: hasMs, cands: cands,
      chapters: chs.length, planSkipped: !!o.planSkipped };
  }
  /* 事实状态标签：计划不是已发生事实；推断必须显式标注 */
  var FACT_LABEL = {
    CONFIRMED_CANON: ['已确认设定', 'published'], MANUSCRIPT_FACT: ['正文已发生', 'working'],
    PLANNED: ['仅计划', 'wait'], AI_INFERRED: ['推断待确认', 'choice'],
    CONFLICTED: ['存在冲突', 'rejected'], TO_EXPLORE: ['待探索', 'unknown'], empty: ['待填写', 'unknown'],
    confirmed: ['作者已确认', 'published'], tentative: ['暂定', 'choice'],
    applied: ['已应用', 'published'], proposed: ['候选待确认', 'choice']
  };
  function factBadge(state) {
    var m = FACT_LABEL[state] || FACT_LABEL.empty;
    return stBadge(m[0], m[1]);
  }

  function ownerHtml(empId, opts) {
    opts = opts || {};
    var e = emp(empId);
    if (!e) return '<span class="own none">' + (opts.gapText || '缺责任人') + '</span>';
    return '<span class="own"><span class="av sm" style="background:' + e.color + '">' + e.initials + '</span>' + esc(e.name) + '</span>';
  }
  function st(label, cls) { return '<span class="st st-' + cls + '">' + esc(label) + '</span>'; }
  function stBadge(label, cls) { return '<span class="st st-badge st-' + cls + '">' + esc(label) + '</span>'; }
  function unknown(text) { return '<span class="unknown">' + esc(text || '未采集') + '</span>'; }
  function money(n) { return n == null ? null : '¥' + n.toFixed(2); }

  /* 章节状态标签。注意三态互不替代：
     草稿 drafting ≠ 正式稿 formal（作者已确认，未发布）≠ 已排期 queued ≠ 已上线 published。
     确认正式稿不再顺手把章节写成「已排期」。 */
  function chapState(c) {
    return ({ published: ['已上线', 'published'], formal: ['正式稿待发布', 'working'],
      queued: ['发布队列中', 'wait'], candidate: ['候选待决定', 'choice'],
      rejected: ['平台退回', 'rejected'], unknown: ['外部状态未知', 'unknown'], outline: ['仅大纲', 'wait'],
      draft: ['起草中', 'wait'], empty: ['空书 · 尚无章节', 'wait'] })[c.state] || ['—', 'wait'];
  }

  /* ---------------- 派生 ---------------- */
  function candidateState(cid) {
    var c = candidate(cid);
    if (!c) return { adopted: 0, rejected: 0, open: 0, total: 0, all: false, applied: false };
    var a = 0, r = 0, o = 0;
    c.changes.forEach(function (ch) {
      if (ch.applied === true) a++; else if (ch.applied === false) r++; else o++;
    });
    return { adopted: a, rejected: r, open: o, total: c.changes.length, all: o === 0, applied: !!S.__runtime.fixes[cid] };
  }
  function areaBadges() {
    var b = {};
    b.operate = S.decisions.filter(function (d) { return d.status === 'pending'; }).length;
    b.market = S.watches.filter(function (w) { return w.state === 'failed'; }).length;
    b.book = Object.keys(S.candidates).filter(function (k) { return candidateState(k).open > 0; }).length +
      (S.craftProposals || []).filter(function (p) { return p.state === 'open'; }).length;
    b.publish = S.queue.filter(function (q) { return ['unknown', 'rejected', 'scheduled'].indexOf(q.state) >= 0; }).length;
    b.audience = S.dataEntries.filter(function (d) { return d.status === 'pending'; }).length +
      S.works.filter(function (w) { return !w.owner && w.status === 'wait'; }).length;
    b.learning = S.learningUsage.filter(function (u) { return u.decision === 'pending'; }).length;
    return b;
  }
  /* 库存实时派生：库存只算「可发布的正式章」；未采纳候选不计库存；
     已提交但回执未核验（unknown）与已排期（queued）都不重复计入可发布库存。 */
  function stockOf(bookId) {
    var st = { publishable: 0, planned: 0, draft: 0 };
    Object.keys(S.chapters).forEach(function (k) {
      var c = S.chapters[k];
      if (c.bookId !== bookId) return;
      if (c.state === 'queued') st.planned++;
      else if (c.formal && !c.published && ['unknown', 'rejected'].indexOf(c.state) < 0) st.publishable++;
      else if (!c.formal && ['draft', 'candidate', 'outline'].indexOf(c.state) >= 0) st.draft++;
    });
    return st;
  }

  /* ---------------- 导航定义 ---------------- */
  var NAV = [
    { area: 'operate', name: '经营', icon: '◈', views: [['home', '业务首页'], ['plan', '计划与决定']] },
    { area: 'market', name: '市场与方向', icon: '⌕', views: [['observations', '市场观察'], ['watches', '持续关注'], ['references', '参考与拆解'], ['direction', '创作方向']] },
    { area: 'book', name: '作品', icon: '▤', views: [['library', '我的书架'], ['overview', '本书创作'], ['craft', '构思与规划'], ['manuscript', '章节创作'], ['review', '章节审校'], ['import', '导入旧稿'], ['story', '故事资料']] },
    { area: 'publish', name: '连载发布', icon: '⇪', views: [['queue', '发布队列'], ['receipts', '提交与回执'], ['accounts', '账号与映射']] },
    { area: 'audience', name: '读者与收益', icon: '◔', views: [['performance', '表现总览'], ['entry', '数据补录'], ['comments', '评论洞察'], ['attribution', '内容归因'], ['revenue', '收益明细']] },
    { area: 'learning', name: '写作经验', icon: '✦', views: [['library', '按书分析与经验']] }
  ];
  function navName(area) { for (var i = 0; i < NAV.length; i++) if (NAV[i].area === area) return NAV[i].name; return area; }
  function viewName(area, view) {
    if(area==='market'&&view==='reference')return '参考拆解';
    for (var i = 0; i < NAV.length; i++) if (NAV[i].area === area)
      for (var j = 0; j < NAV[i].views.length; j++) if (NAV[i].views[j][0] === view) return NAV[i].views[j][1];
    return view;
  }

  /* ---------------- 视图注册 ---------------- */
  var views = {};   // 'area.view' -> {render(ctx), aside(ctx)}
  var on = {};      // data-action -> handler(el, dataset)
  function register(key, def) { views[key] = def; }

  /* ---------------- 路由 ---------------- */
  function key() { return S.__route.area + '.' + S.__route.view; }
  function go(area, view, params, opts) {
    opts = opts || {};
    params = params || {};
    if(area==='audience'&&view==='attribution'){var target=S.analyses.find(function(a){return a.bookId===S.__scope.bookId&&(!params.id||a.id===params.id);});area='learning';view='library';params=target?{analysis:target.id,dimension:'rhythm'}:{};}
    if(params.bookId&&book(params.bookId)){if(params.bookId!==S.__scope.bookId)S.__ui.bookPanel='positioning';S.__scope.bookId=params.bookId;}
    if(area==='book'&&view==='craft'&&WB.craftPanel&&!params.full){ if(params.bookId)S.__scope.bookId=params.bookId; S.__ui.bookPanel=params.mode||'positioning'; S.__ui.aside=true; S.__ui.discuss=false; if(S.__route.area!=='book'||S.__route.view==='library'){S.__route={area:'book',view:'overview',params:{bookId:params.bookId||S.__scope.bookId}};} save();render();return;}
    if (area === 'book' && view === 'review') { view = 'manuscript'; params = mixParams(params, { stage: 'review' }); }
    if (S.__ui) { S.__ui.discuss = false; if(area==='book')S.__ui.aside=view!=='library'; }
    if (!opts.replace) S.__hist.push({ area: S.__route.area, view: S.__route.view, params: clone(S.__route.params || {}) });
    if (S.__hist.length > 40) S.__hist.shift();
    S.__route = { area: area, view: view, params: params || {} };
    save(); render();
  }
  function back() {
    var p = S.__hist.pop();
    if (!p) { toast('已回到入口位置'); return; }
    S.__route = p; S.__ui.discuss=false; save(); render();
  }
  function rerender() { save(); render(); }

  /* ---------------- 渲染 ---------------- */
  function el(id) { return document.getElementById(id); }

  function renderRail() {
    var b = areaBadges(), html = '';
    NAV.forEach(function (n) {
      var on = S.__route.area === n.area;
      html += '<button class="nav-item' + (on ? ' on' : '') + '" data-action="nav.area" data-area="' + n.area + '">' +
        '<span class="ni-ico">' + n.icon + '</span><span class="ni-n">' + esc(n.name) + '</span>' +
        (b[n.area] ? '<span class="nav-badge">' + b[n.area] + '</span>' : '') + '</button>';
      if (on) {
        html += '<div class="nav-sub">';
        n.views.forEach(function (v) {
          if (n.area === 'book' && (v[0] === 'library' || v[0] === 'review' || v[0] === 'import' || S.__route.view === 'library')) return;
          if (n.area === 'book' && v[0] === 'overview') html += '<div class="nav-book-label">' + esc(scopeBook().title) + '</div>';
          html += '<button class="' + (S.__route.view === v[0] ? 'on' : '') + '" data-action="nav.view" data-area="' + n.area + '" data-view="' + v[0] + '">' + esc(v[1]) + '</button>';
        });
        if(n.area==='book'&&S.__route.view!=='library')html+='<details class="nav-chapters" open><summary>本书章节</summary>'+Object.keys(S.chapters).filter(function(k){return S.chapters[k].bookId===S.__scope.bookId;}).sort(function(a,b){return S.chapters[a].no-S.chapters[b].no;}).map(function(k){var c=S.chapters[k];return '<button data-action="flow.stage" data-chapter="'+esc(k)+'" data-stage="write">'+c.no+' · '+esc(c.title)+'</button>';}).join('')+'</details>';
        html += '</div>';
      }
    });
    el('nav').innerHTML = html;
  }

  function renderCrumb() {
    var b = scopeBook();
    el('crumb').innerHTML =
      '<span>写作经营</span><span class="csep">/</span><b>' + esc(navName(S.__route.area)) + '</b>' +
      '<span class="csep">/</span><span>' + esc(S.__route.area==='learning'&&S.__route.view==='detail'?'经验详情':viewName(S.__route.area, S.__route.view)) + '</span>' +
      (b && S.__route.area === 'book' && S.__route.view !== 'library' ? '<span class="csep">·</span><span>' + esc(b.title) + '</span>' : '');
    el('btnBack').disabled = S.__hist.length === 0;
  }

  function renderQuickbar() {
    el('quickbar').innerHTML = '';
  }

  function renderScope() {
    var b = scopeBook();
    el('scopeBox').innerHTML = '<span class="prototype-label">本地探索 · 模拟数据</span>';
  }

  var renderedRoute='';
  function render() {
    keepConvDraft();
    var routeKey=JSON.stringify(S.__route), sameRoute=routeKey===renderedRoute, scrollBefore=el('viewport')?el('viewport').scrollTop:0; renderedRoute=routeKey;
    var v = views[key()];
    applyChrome();
    renderRail(); renderCrumb(); renderQuickbar(); renderScope();
    if (!v) { el('main').innerHTML = mainBar() + '<div class="empty"><b>该工作面尚未实现</b>' + esc(key()) + '</div>'; return; }
    /* 共享工作区紧贴 Main 顶部（工具条之下、正文之上）：员工嵌在「当前工作」里，
       不是页尾的通用聊天。收起时只留一行「他仍在处理 X」，不遮挡内容。 */
    var content = v.render({ route: S.__route, params: S.__route.params || {}, scope: S.__scope });
    el('main').dataset.area = S.__route.area;
    el('main').dataset.view = S.__route.view;
    el('main').innerHTML = content;
    el('main').scrollTop = 0;
    var a = v.aside ? v.aside({ route: S.__route, params: S.__route.params || {}, scope: S.__scope }) : '';
    if(WB.bookUtility && S.__route.area==='book'&&S.__route.view!=='library')a=WB.bookUtility();
    el('aside').innerHTML = a || '';
    el('aside').classList.toggle('hide', !a);
    if (S.__ui && S.__ui.aside && a) el('aside').classList.remove('hide');
    if (S.__ui && !S.__ui.aside) el('aside').classList.add('hide');
    if(S.__conv&&S.__conv.open&&S.__ui.discuss){
      var anchor=el('main').querySelector('.editor-line');
      if(anchor)anchor.insertAdjacentHTML('afterend',sharedDock());
      else el('main').insertAdjacentHTML('afterbegin',sharedDock());
      renderConvMsgs();
    }
    el('viewport').scrollTop=sameRoute?scrollBefore:0;
  }

  /* 三栏是可使用的空间：左/右各自可开合、可调宽；状态持久化在本机。 */
  function applyChrome() {
    var u = S.__ui || (S.__ui = { rail: true, aside: false, railW: null, asideW: null });
    var app = el('app');
    if (!app) return;
    app.classList.toggle('rail-off', !u.rail);
    app.classList.toggle('aside-off', !u.aside);
    if (u.railW) app.style.setProperty('--rail-w', u.railW + 'px'); else app.style.removeProperty('--rail-w');
    if (u.asideW) app.style.setProperty('--aside-w', u.asideW + 'px'); else app.style.removeProperty('--aside-w');
    var rb = el('btnRail'), ab = el('btnAside');
    if (rb) { rb.classList.toggle('on', !!u.rail); rb.setAttribute('aria-expanded', String(!!u.rail));
      rb.title = (u.rail ? '收起' : '展开') + '左栏 · Context（我在哪 / 查看哪一项）'; }
    if (ab) { ab.classList.toggle('on', !!u.aside); ab.setAttribute('aria-expanded', String(!!u.aside));
      ab.title = (u.aside ? '收起' : '展开') + '右栏 · Utility（属性 / 证据 / 版本）'; }
    var rh = el('railResize'), ah = el('asideResize');
    if (rh) rh.setAttribute('aria-hidden', String(!u.rail));
    if (ah) ah.setAttribute('aria-hidden', String(!u.aside));
  }

  /* Main 保底信息条：左栏收起后仍知道当前书/章/页面、保存状态，并仍能打开导航与选择器。 */
  function mainBar() {
    var b = scopeBook();
    var ck = (S.__route.params && S.__route.params.chapter) || null;
    var ch = ck ? S.chapters[ck] : null;
    var ms = ck ? msOf(ck) : null;
    var stTxt = ms ? (ms.formal ? '正文有正式稿' : '仅草稿') : (ch ? '尚未写入正文' : '');
    var u = S.__ui || {};
    return '<div class="mainbar" id="mainBar">' +
      '<span class="mb-ico">▤</span>' +
      '<b>' + esc(b ? b.title : '—') + '</b>' +
      (ch ? '<span class="t4">·</span><span>' + esc(ch.title || ck) + '</span>' : '') +
      '<span class="t4">·</span><span class="t3">' + esc(navName(S.__route.area) + ' / ' + viewName(S.__route.area, S.__route.view)) + '</span>' +
      (stTxt ? '<span class="t4">·</span><span class="t3">' + esc(stTxt) + '</span>' : '') +
      '<span class="spacer"></span>' +
      (u.rail ? '' : '<button class="btn sm ghost" data-action="ui.rail" data-on="1">展开左栏</button>') +
      '<button class="btn sm ghost" data-action="ui.bookSwitch">切换作品</button>' +
      '<button class="btn sm ghost" data-action="craft.picker" data-book="' + esc(b ? b.id : '') + '" data-scope="book">创作选择</button>' +
      (u.aside ? '' : '<button class="btn sm ghost" data-action="ui.aside" data-on="1">辅助信息</button>') +
      '</div>';
  }

  /* ---------------- 上下文侧栏件 ---------------- */
  function asBlock(title, body, extra) {
    return '<div class="as"><div class="as-h"><span>' + esc(title) + '</span>' + (extra || '') + '</div>' + body + '</div>';
  }
  function workHtml(w, opts) {
    opts = opts || {};
    var stMap = { done: ['已回原对象', 'published'], working: ['进行中', 'working'], wait: ['等待中', 'wait'], choice: ['待决定', 'choice'], blocked: ['受阻', 'blocked'] };
    var s = stMap[w.status] || ['—', 'wait'];
    return '<div class="as-w' + (opts.clickable === false ? '' : ' clickable') + '"' +
      (opts.clickable === false ? '' : ' data-action="work.open" data-id="' + w.id + '"') + '>' +
      '<div class="wt">' + esc(w.title) + '</div>' +
      '<div class="ws">' + ownerHtml(w.owner, { gapText: '缺责任人' }) + ' · ' + st(s[0], s[1]) + '</div>' +
      '<div class="ws">产物：' + esc(w.artifact) + '</div>' +
      '<div class="ws">下一步：' + esc(w.next) + '</div></div>';
  }

  /* ---------------- 抽屉 / 弹层 / 提示 ---------------- */
  var overlayEpoch = 0;   /* 每次打开叠层自增，用于判断某个行动是否另开了新叠层 */
  function openDrawer(o) {
    overlayEpoch++;
    var d = el('drawer');
    d.className = 'drawer open' + (o.wide ? ' wide' : '');
    d.setAttribute('aria-hidden', 'false');
    d.innerHTML =
      '<div class="drawer-h"><div><div class="drawer-t">' + esc(o.title) + '</div>' +
      (o.sub ? '<div class="drawer-s">' + o.sub + '</div>' : '') + '</div><div class="spacer"></div>' +
      '<button class="btn icon sm" data-action="close-drawer" title="关闭">✕</button></div>' +
      '<div class="drawer-body" id="drawerBody">' + o.body + '</div>' +
      (o.footer ? '<div class="drawer-f">' + o.footer + '</div>' : '');
    el('drawerBackdrop').classList.add('on');
  }
  function closeDrawer() { el('drawer').classList.remove('open'); el('drawer').setAttribute('aria-hidden', 'true'); el('drawerBackdrop').classList.remove('on'); }
  /* overlayEpoch：每次打开叠层自增，用于判断某个行动是否另开了新叠层 */
  function modal(o) {
    overlayEpoch++;
    var m = el('modal');
    m.className = 'modal-root on';
    m.innerHTML = '<div class="modal"><div class="modal-h"><span>' + esc(o.title) + '</span>' +
      '<button class="btn icon sm" data-action="close-modal">✕</button></div>' +
      '<div class="modal-body">' + o.body + '</div>' +
      '<div class="modal-f">' + (o.footer || '<button class="btn" data-action="close-modal">关闭</button>') + '</div></div>';
  }
  function closeModal() { var m = el('modal'); m.className = 'modal-root'; m.innerHTML = ''; }
  function toast(msg, kind) {
    var t = document.createElement('div');
    t.className = 'toast ' + (kind || '');
    t.textContent = msg;
    el('toasts').appendChild(t);
    setTimeout(function () { if (t.parentNode) t.parentNode.removeChild(t); }, 4200);
  }

  /* ---------------- 员工对话：真实讨论过程（有对象、有版本、可落到对象） ----------------
     规则（硬约束）：
       · 输入框永远为空：由作者提出真实要求，不用预制文本冒充「讨论」。
       · 员工先说明接管了哪个范围（对象 / 版本 / 当前状态），再给具体回复与提案。
       · 提案可编辑、可逐项采纳 / 拒绝；采纳只落到显式对象，未采纳绝不进入正式稿。
       · 多轮讨论延续同一议题；已裁定的部分不再重复改动（只处理剩余范围）。
       · 演示未覆盖的意图如实说「演示未模拟」，不假装理解。
   */
  function convKey(empId, obj) { var bid=objBookId(obj); return bid && empId==='E-01' ? empId+'|book:'+bid : empId+'|'+(obj||'-'); }
  function keepConvDraft(){var cv=S.__conv||{},ta=el('convInput');if(cv.obj&&ta){S.__convDrafts=S.__convDrafts||{};S.__convDrafts[cv.empId+'|'+cv.obj]=ta.value;}}
  function migrateBookConversation(empId,obj){
    var bid=objBookId(obj),key=convKey(empId,obj);if(!bid||empId!=='E-01')return;
    S.__conversationImported=S.__conversationImported||{};
    Object.keys(S.conversations).forEach(function(k){if(k===key||S.__conversationImported[k]||k.split('|')[0]!==empId)return;
      var oldObj=k.slice(k.indexOf('|')+1);if(objBookId(oldObj)!==bid)return;
      var old=(S.conversations[k]||[]).map(function(m){return Object.assign({},m,{obj:m.obj||oldObj,ctx:m.ctx||oldObj});});
      S.conversations[key]=(S.conversations[key]||[]).concat(old);S.__conversationImported[k]=true;
    });
  }
  /* 对话对象归属哪本书：切书时用来判断「这条对话是否该跟着走」。
     认不出来就返回 null —— 不猜，也不强行关掉看不清归属的对话。 */
  function objBookId(obj) {
    var s = String(obj == null ? '' : obj);
    if(book(s))return s;
    var parts=s.split(':');if(parts.length>1&&book(parts[1]))return parts[1];
    var mh = /^([^#|]+)#p\d+$/.exec(s);
    if (mh && S.chapters[mh[1]]) return S.chapters[mh[1]].bookId;
    if (S.chapters[s]) return S.chapters[s].bookId;
    return null;
  }
  /* 完整 Conversation 在 Main 的 Shared Work Area（§17.3），不是右侧 Utility，也不是通用 Chatbot：
     它挂在当前对象/工作上，随导航跟随；可收起但不会停止；右栏永远不放完整对话。 */
  function convCtxHtml(e, obj, objLabel) {
    var ctx = WB.discussContext ? WB.discussContext(obj) : null;
    return '<div class="conv-ctx"><b>'+esc(e.name)+'</b> · '+esc(e.role)+'<br>'+esc(objLabel||obj||'当前工作')+(ctx?' · '+esc(ctx.state):'')+(ctx&&ctx.preview?'<div class="context-excerpt">当前引用：'+esc(String(ctx.preview).slice(0,220))+'</div>':'')+'</div>';
  }
  function sharedDock() {
    var cv = S.__conv || {};
    if (!cv.open || !cv.empId) return '';
    var e = emp(cv.empId) || { name: '—', role: '' };
    var label = cv.objLabel || cv.obj || '当前工作面';
    return '<section class="sarea' + (cv.collapsed ? ' is-collapsed' : '') + '" id="sharedArea">' +
      '<div class="sarea-h"><span class="sarea-t">与 ' + esc(e.name) + '</span>' +
      '<span class="sarea-s">' + esc(label) + '</span><span class="spacer"></span>' +
      '<button class="btn sm ghost" data-action="conv.toggleCollapse">' + (cv.collapsed ? '展开' : '收起') + '</button>' +
      '<button class="btn sm ghost" data-action="conv.close">结束讨论</button></div>' +
      (cv.collapsed
        ? '<div class="sarea-min sm t3">对话记录已保留：' + esc(e.name) + ' · 「' + esc(label) + '」。' +
          '<button class="btn sm ghost" data-action="conv.toggleCollapse" style="margin-left:8px">展开对话</button></div>'
        : '<div class="sarea-body">' + convCtxHtml(e, cv.obj, label) +
          '<div class="conv-msgs" id="convMsgs"></div>' +
          '<div class="sarea-f"><textarea class="ta" id="convInput" data-input="conv.draft" placeholder="' + (String(cv.obj).indexOf('analysis:')===0?'讨论这次表现、可能原因或替代解释；结论由你确认。':'直接写你的要求，例如：这一段再短一点；把重复的修饰词删掉；这个场景的出场人物漏了顾晚。') + '">' + esc((S.__convDrafts||{})[cv.empId+'|'+cv.obj]||'') + '</textarea>' +
          '<button class="btn primary" data-action="conv.send" data-emp="' + esc(cv.empId) + '" data-obj="' + esc(cv.obj || '-') + '">发送</button></div>' +
          '</div>') +
      '</section>';
  }
  function openConv(empId, obj, objLabel) {
    var e = emp(empId);
    if (!e) { toast('该责任暂无在岗员工，无法发起对话', 'warn'); return; }
    keepConvDraft(); migrateBookConversation(empId,obj);
    var k = convKey(empId, obj);
    if (!S.conversations[k]) S.conversations[k] = [];
    var oldInput=el('convInput');if(oldInput)oldInput.removeAttribute('id');
    S.__conv = { open: true, empId: empId, obj: obj || '-',
      objLabel: objLabel || obj || '当前工作面', collapsed: false };
    S.__ui.discuss = true;
    save(); render();
    toast('已在当前工作中展开与 ' + e.name + ' 的协作（对象：' + (objLabel || obj || '当前工作面') + '）', 'ok');
  }
  function convCollapse(on) {
    if (!S.__conv || !S.__conv.open) return;
    S.__conv.collapsed = (on == null ? !S.__conv.collapsed : !!on);
    S.__ui.discuss = true;
    save(); render();
  }
  function convClose() {
    if (!S.__conv) return;
    S.__conv.open = false; S.__conv.collapsed = false; S.__ui.discuss = false;
    save(); render();
    toast('本次协作已收起（对话记录仍保存在本机，可再从对象处打开）');
  }
  function convMsgHtml(m, empId) {
    var av = '<span class="av sm" style="background:' +
      (m.who === 'me' ? '#3A4A52' : ((emp(empId) || {}).color || '#666')) + '">' +
      (m.who === 'me' ? '你' : esc(((emp(empId) || {}).name || '').slice(0, 1))) + '</span>';
    var demo = m.demo ? ' <span class="st st-badge st-unknown">演示</span>' : '';
    var prop = '';
    if (m.propId && S.discussProps && S.discussProps[m.propId]) {
      prop = propCard(m.propId, S.discussProps[m.propId]);
    }
    return '<div class="msg ' + (m.who === 'me' ? 'me' : '') + '">' + av +
      '<div><div class="bd">' + esc(m.text) + demo + '</div>' +
      (m.ctx ? '<div class="sm t3" style="margin-top:3px">上下文：' + esc(m.ctx) + '</div>' : '') +
      (m.took ? '<div class="sm t3" style="margin-top:3px">' + esc(m.took) + '</div>' : '') +
      prop +
      (m.next ? '<div class="sm t3" style="margin-top:4px">下一步：' + esc(m.next) + '</div>' : '') +
      '<div class="mt">' + esc(m.at) + '</div></div></div>';
  }
  function propCard(pid, p) {
    var items = p.items.map(function (it) {
      var cls = it.applied === true ? ' adopted' : (it.applied === false ? ' rejected' : '');
      var badge = it.applied === true ? stBadge('已采纳', 'published')
        : it.applied === false ? stBadge('已拒绝', 'rejected') : stBadge('待决定', 'choice');
      var acts = '<span class="diff-acts">' + badge +
        (it.applied == null
          ? '<button class="btn sm primary" data-action="conv.acceptItem" data-pid="' + pid + '" data-item="' + it.id + '">' +
              (it.kind === 'dir' ? '用这个方向' : '采纳') + '</button>' +
            '<button class="btn sm dark" data-action="conv.rejectItem" data-pid="' + pid + '" data-item="' + it.id + '">' +
              (it.kind === 'dir' ? '不用这个' : '拒绝') + '</button>' +
            '<button class="btn sm ghost" data-action="conv.editItem" data-pid="' + pid + '" data-item="' + it.id + '">改后再采纳</button>'
          : '') + '</span>';
      /* 方向候选：必须给出具体故事内容、差异与取舍，而不是只给一组标签 */
      if (it.kind === 'dir') {
        var d = it.dir || {};
        var tagBits = Object.keys(d.tags || {}).map(function (id) {
          var t = tagDef(id);
          return '<b>' + esc(t ? t.name : id) + '</b>：' + esc((d.tags[id] || []).join('、'));
        }).join('；');
        return '<div class="diff-i' + cls + '">' +
          '<div class="diff-h"><span class="idx">' + esc(it.id) + '</span>' +
          '<span class="diff-why">' + esc(it.label) + '</span>' + acts + '</div>' +
          '<div class="diff-txt">' +
          '<div class="lbl">故事前提</div><div class="after">' + esc(d.premise || '') + '</div>' +
          (d.conflict ? '<div class="lbl" style="margin-top:6px">主要冲突</div><div class="after">' + esc(d.conflict) + '</div>' : '') +
          (d.viewpoint ? '<div class="lbl" style="margin-top:6px">叙事视角</div><div class="after">' + esc(d.viewpoint) + '</div>' : '') +
          (d.why ? '<div class="lbl" style="margin-top:6px">为什么它贴你的构思</div><div class="before">' + esc(d.why) + '</div>' : '') +
          (d.tradeoff ? '<div class="lbl" style="margin-top:6px">代价 / 取舍</div><div class="before">' + esc(d.tradeoff) + '</div>' : '') +
          (tagBits ? '<div class="lbl" style="margin-top:6px">采纳后会一并记录的方向</div><div class="after">' + tagBits + '</div>' : '') +
          '</div></div>';
      }
      return '<div class="diff-i' + cls + '"><div class="diff-h"><span class="idx">' + esc(it.id) + '</span>' +
        '<span class="diff-why">' + esc(it.label) + '</span>' + acts + '</div>' +
        '<div class="diff-txt">' + (it.before ? '<div class="lbl">改前</div><div class="before">' + esc(it.before) + '</div><div class="mid"></div>' : '') +
        '<div class="lbl">改后</div><div class="after">' + esc(it.after) + '</div></div></div>';
    }).join('');
    /* 未裁定 = applied 为 null / undefined（提案项漏写 applied 时不得被当成「已裁定」） */
    var open = p.items.filter(function (x) { return x.applied == null; }).length;
    return '<div class="note choice" style="margin-top:8px">' +
      '<b>' + esc(p.id) + ' · 第 ' + p.round + ' 轮提案</b> ' +
      stBadge(open ? '待决定 ' + open + ' / 共 ' + p.items.length : '本轮已全部裁定', open ? 'choice' : 'published') +
      '<div class="sm t3" style="margin-top:3px">落到：' + esc(p.targetLabel) + '（只落该对象；正式稿与线上稿不变）</div>' +
      '<div class="diff" style="margin-top:6px">' + items + '</div>' +
      '<div class="sm t3" style="margin-top:4px">依据：' + esc(p.basis) + '</div>' +
      '<div class="btnrow" style="margin-top:6px">' +
      (open ? '<button class="btn sm" data-action="conv.acceptRest" data-pid="' + p.id + '">剩余全部采纳</button>' : '') +
      '<button class="btn sm ghost" data-action="conv.continue" data-pid="' + p.id + '">继续讨论（只改剩下的）</button>' +
      '</div></div>';
  }
  function renderConvMsgs() {
    var host = el('convMsgs');
    if (!host) return;
    var cv = S.__conv || {};
    if (!cv.open || !cv.empId) return;
    var empId = cv.empId;
    var k = convKey(empId, cv.obj);
    var msgs = S.conversations[k] || [];
    host.innerHTML = msgs.length ? msgs.map(function (m) { return convMsgHtml(m, empId); }).join('')
      : '<div class="empty">还没有对话。发出的内容与由此产生的改动都保存在本机演示状态里。</div>';
    host.scrollTop = host.scrollHeight;
  }
  /* 一条要求的完整链路：记录作者原话 → 员工先声明接管的范围 → 给具体回复与可裁定提案。
     抽成 convAsk 是为了让「新书起步」等页内入口也从同一个输入发出同一条链路，
     而不是再造一个页尾通用聊天（§3：员工嵌入当前工作）。 */
  function convAsk(empId, obj, req, opts) {
    opts = opts || {};
    var e = emp(empId);
    if (!e) { toast('该责任暂无在岗员工，无法发起对话', 'warn'); return null; }
    if (!req || !String(req).trim()) { toast('请先写你的要求——讨论由你发起', 'warn'); return null; }
    req = String(req).trim();
    var o = obj || '-';
    if (!S.conversations[convKey(empId, o)]) S.conversations[convKey(empId, o)] = [];
    var already = !!(S.__conv && S.__conv.open && S.__conv.empId === empId && S.__conv.obj === o);
    if (!already) {
      openConv(empId, o, opts.objLabel || obj || '当前工作面');
      if (!S.__conv || !S.__conv.open || S.__conv.obj !== o) return null;
    }
    S.__conv.collapsed = false; S.__ui.discuss=true;
    var k = convKey(empId, o);
    S.conversations[k].push({ who: 'me', text: req, at: now(), obj:o, ctx:(S.__conv.objLabel||o)+' · '+convCtxTag() });
    var res = WB.discussEngine ? WB.discussEngine(empId, o, req, opts) : null;
    if (!res) {
      S.conversations[k].push({ who: 'emp', at: now(),
        text: '这条我暂时没有可模拟的处理路径。你的原话已经保留在这条对话里，不会被丢弃。' });
    } else if (!res.supported) {
      S.conversations[k].push({ who: 'emp', at: now(), demo: true, took: res.took || '',
        text: res.reply, next: res.next || '你可以换一种说法，或直接在正文 / 创作对象里手改。' });
    } else {
      S.conversations[k].push({ who: 'emp', at: now(), demo: true, took: res.took, text: res.reply,
        propId: res.propId || null, next: res.next });
    }
    if(res&&res.propId&&S.discussProps[res.propId])S.discussProps[res.propId].sourceObj=o;
    save();
    if (already && !opts.rerender) renderConvMsgs(); else render();
    return res;
  }
  function convSend(empId, obj) {
    var inp = el('convInput');
    if (!inp || !inp.value.trim()) { toast('请先写你的要求——讨论由你发起', 'warn'); return; }
    var req = inp.value.trim();
    var cv = S.__conv || {};
    inp.value = ''; S.__convDrafts=S.__convDrafts||{};S.__convDrafts[cv.empId+'|'+cv.obj]='';
    convAsk(empId || cv.empId, obj || cv.obj, req);
  }
  /* 每条要求随附上下文标签（本书 / 本章 / 对象 / 版本 / 选区），避免切书后串台 */
  function convCtxTag() {
    var b = scopeBook(), ck = S.__route.params && S.__route.params.chapter;
    var ms = ck ? msOf(ck) : null;
    var parts = [];
    if (b) parts.push('书 ' + b.id);
    if (ck) parts.push('章 ' + ck);
    if (ms) parts.push('草稿 r' + ((ms.versions || []).length));
    var sel = S.__sel && S.__sel.text;
    if (sel) parts.push('选区 ' + String(sel).slice(0, 12) + (String(sel).length > 12 ? '…' : ''));
    return parts.join(' · ');
  }
  function convApplyItem(pid, itemId, overrideText) {
    var p = S.discussProps[pid];
    if (!p) return false;
    var it = byId(p.items, itemId);
    if (!it || it.applied != null) return false;
    var wrote = WB.discussApply ? WB.discussApply(p, it, overrideText) : false;
    if (!wrote) { toast('未能写入目标对象：对象可能已被删除或改名。改动未生效', 'warn'); return false; }
    it.applied = true;
    it.appliedAt = now();
    if (overrideText != null) it.after = overrideText;
    logStep('讨论提案 ' + pid + ' 的 ' + itemId + ' 已采纳并写入 ' + p.targetLabel);
    return true;
  }

  /* ---------------- 行动 API（唯一状态写入口） ---------------- */
  var act = {
    decideChange: function (cid, chId, val) {
      var c = candidate(cid);
      c.changes.forEach(function (ch) { if (ch.id === chId) ch.applied = val; });
      S.learningUsage.forEach(function (u) {
        if (u.target.indexOf(cid) >= 0) {
          var m = /C\d+-(\d)/.exec(u.target);
          if (m && chId === cid.replace('C-', 'C') + '-' + m[1]) { /* keep */ }
        }
      });
      logStep('候选 ' + cid + ' 的 ' + chId + ' 标为' + (val ? '采纳' : '拒绝'));
      rerender();
    },
    applyCandidate: function (cid) {
      var c = candidate(cid), st = candidateState(cid);
      if (st.open > 0) { toast('还有 ' + st.open + ' 项未决定，先逐项采纳或拒绝', 'warn'); return; }
      var ch = chapter(c.chapter);
      var ms = msOf(c.chapter) || msEnsure(c.chapter, c.bookId, '第 ' + ch.no + ' 章');
      /* 基线护栏：候选声明基于哪个正式版本；正式稿已前进时要求先比对，不静默套用 */
      if (c.baseVersion && ms.formalVersion && c.baseVersion !== ms.formalVersion) {
        toast('该候选基于 ' + c.baseVersion + '，本章正式稿已到 ' + ms.formalVersion + '：请先在版本历史里比对，再重新形成候选', 'warn');
        logStep('候选 ' + cid + ' 基线过期（' + c.baseVersion + ' → ' + ms.formalVersion + '），未套用');
        return;
      }
      S.__runtime.fixes[cid] = { at: now(), adopted: st.adopted };
      if (st.adopted > 0) {
        /* 采纳项先落到草稿（工作副本），再由作者确认快照为正式稿 */
        c.changes.forEach(function (x) {
          if (x.applied === true && x.after) {
            var pi = (x.para || (ms.paragraphs.length + 1)) - 1;
            if (pi < ms.paragraphs.length) ms.paragraphs[pi] = x.after;
            else ms.paragraphs.push(x.after);
          }
        });
        var base = ms.formalVersion || ch.formal || 'v0';
        var nextV = 'v' + ((parseInt(String(base).replace(/\D/g, ''), 10) || 0) + 1);
        var note = '由候选 ' + cid + ' 确认生成（采纳 ' + st.adopted + ' 项，拒绝 ' + st.rejected + ' 项）';
        ms.formalVersion = nextV; ms.updatedAt = now();
        ms.formal = { version: nextV, paragraphs: ms.paragraphs.slice(), acceptedAt: now(), note: note };
        ms.versions.push({ v: nextV, at: now(), kind: 'formal', note: note, paragraphs: ms.paragraphs.slice() });
        ch.formal = nextV;
        ch.formalAcceptedAt = now();
        ch.state = ch.published ? 'published' : 'formal';
      }
      // 采纳记录回写到 Learning 使用记录
      S.learningUsage.forEach(function (u) {
        if (u.target.indexOf(cid) >= 0) {
          var seg = u.target.split('·')[1];
          if (seg) {
            var id = cid.replace('C-', 'C') + '-' + seg.trim().replace('C', '').replace(/-/, '');
            var found = c.changes.filter(function (x) { return x.id === seg.trim(); })[0];
            if (found) u.decision = found.applied ? 'applied' : 'rejected';
          }
        }
      });
      logStep('确认候选 ' + cid + '：采纳 ' + st.adopted + ' 项，拒绝 ' + st.rejected + ' 项');
      toast('已生成正式版本 ' + (ch.formal || '') + '（草稿与正式稿同源）；线上仍是 ' +
        (ch.published || '未发布') + '，不会自动改变', 'ok');
      rerender();
    },
    /* 手写稿 / 无候选稿：作者直接把当前草稿确认为正式稿（R5）。
       确认 ≠ 发布：线上版本不变，仍需另走发布流程。 */
    msConfirmFormal: function (chapterKey) {
      if (WB.canFinalize && !WB.canFinalize(chapterKey)) return;
      var S2 = S, ch = chapter(chapterKey);
      if (!ch) { toast('找不到该章节', 'err'); return; }
      var ms = msOf(chapterKey);
      if (!ms || !ms.paragraphs.length) { toast('本章草稿为空：先手写正文再确认正式稿', 'warn'); return; }
      var base = ms.formalVersion || ch.formal || 'v0';
      var nextV = 'v' + ((parseInt(String(base).replace(/\D/g, ''), 10) || 0) + 1);
      var note = '作者确认手写草稿为正式 ' + nextV + '（' + ms.paragraphs.length + ' 段）';
      ms.formalVersion = nextV;
      ms.formal = { version: nextV, paragraphs: ms.paragraphs.slice(), acceptedAt: now(), note: note };
      ms.versions.push({ v: nextV, at: now(), kind: 'formal', note: note, paragraphs: ms.paragraphs.slice() });
      ms.updatedAt = now();
      ch.formal = nextV;
      ch.formalAcceptedAt = now();
      ch.state = ch.published ? 'published' : 'formal';
      logStep('手写草稿确认正式稿 ' + chapterKey + ' → ' + nextV);
      toast('已确认为正式 ' + nextV + '（' + ms.paragraphs.length + ' 段）。确认 ≠ 发布：线上仍是 ' +
        (ch.published || '未发布'), 'ok');
      rerender();
    },
    /* 版本回退：把某次历史快照取回为草稿（历史不删，只追加一次回退记录）。
       只接受**真有正文**的快照：空快照取回等于清空草稿，属于数据保护红线，必须 fail-closed。 */
    msRestore: function (chapterKey, vi) {
      var ms = msOf(chapterKey);
      var v = ms && ms.versions[Number(vi)];
      if (!v) { toast('该历史版本没有可读正文快照（早期版本），无法回退', 'warn'); return; }
      if (!Array.isArray(v.paragraphs) || !v.paragraphs.length) {
        toast('该历史版本不含正文快照：取回会把草稿清空，已阻止', 'warn'); return;
      }
      ms.paragraphs = v.paragraphs.slice();
      ms.updatedAt = now();
      ms.versions.push({ v: '草稿 r' + (ms.versions.filter(function (x) { return x.kind === 'draft'; }).length + 1),
        at: now(), kind: 'draft', note: '由 ' + v.v + '（' + (v.at || '时间未知') + '）回退取回为草稿；原版本保留',
        paragraphs: ms.paragraphs.slice() });
      logStep('正文 ' + chapterKey + ' 回退到 ' + v.v + '（草稿）');
      toast('已把 ' + v.v + ' 的正文取回为草稿；正式稿与线上稿均未改变', 'ok');
      rerender();
    },
    /* 章节改名：按稳定内部键（ck）关联，改名不破坏大纲关联 */
    chapRename: function (chapterKey) {
      var ch = chapter(chapterKey);
      var inp = document.getElementById('chTitleInp');
      var v = inp ? String(inp.value || '').trim() : '';
      if (!v) { toast('标题不能为空', 'warn'); return; }
      var old = ch.title;
      ch.title = v;
      var ms = msOf(chapterKey);
      if (ms) ms.title = '第 ' + ch.no + ' 章 · ' + v;
      logStep('章节 ' + chapterKey + ' 改名：' + old + ' → ' + v);
      toast('已改名：关联按稳定章节键保持，大纲与场景归属不受影响', 'ok');
      closeModal(); rerender();
    },
    rejectCandidate: function (cid) {
      candidate(cid).changes.forEach(function (ch) { ch.applied = false; });
      S.__runtime.fixes[cid] = { at: now(), adopted: 0 };
      toast('已整份拒绝并保留原正式稿；理由已记录', '');
      rerender();
    },
    queueAdd: function (chapterKey) {
      var ch = chapter(chapterKey);
      if (!ch.formal) { toast('该章尚无正式稿，无法加入发布队列', 'warn'); return; }
      if (S.queue.filter(function (q) { return q.chapter === chapterKey && q.state !== 'live'; }).length) { toast('该章已在队列中'); return; }
      S.queue.push({ id: 'Q-' + (100 + S.queue.length), bookId: ch.bookId, chapter: chapterKey,
        title: '第 ' + ch.no + ' 章 · ' + ch.title, version: ch.formal, account: book(ch.bookId).accountId, target: book(ch.bookId).platform,
        plannedAt: null, submittedAt: null, state: 'draft', evidence: '由正文工作面加入' });
      ch.state = 'queued';
      logStep('章节 ' + chapterKey + ' 加入发布队列');
      toast('已加入发布队列，等待排期', 'ok'); rerender();
    },
    schedule: function (qid, when) {
      var q = queueItem(qid);
      q.plannedAt = when || '2026-09-23 20:00';
      q.state = 'scheduled';
      logStep(qid + ' 排期至 ' + q.plannedAt);
      toast('已排期 ' + q.plannedAt + '（本地计划，不等于平台定时任务）', 'ok'); rerender();
    },
    pauseSchedule: function (qid) {
      var q = queueItem(qid);
      q.state = q.submittedAt ? q.state : 'draft';
      q.plannedAt = null;
      toast('已暂停排期。注意：若平台侧已有定时任务，需另行在平台核验，本地暂停不代表平台撤销', 'warn'); rerender();
    },
    submit: function (qid) {
      var q = queueItem(qid);
      q.submittedAt = now();
      q.state = 'waiting';
      S.receipts[qid] = { kind: 'pending', note: '已按人工路径提交（本原型为 Mock），回执需在平台正常后台核验后登记。' };
      logStep(qid + ' 提交（人工路径 · Mock）');
      toast('已登记“人工提交”。提交 ≠ 上线：请在平台核验后登记回执', '');
      rerender();
    },
    verify: function (qid) {
      var q = queueItem(qid);
      q.state = 'live'; q.verifiedAt = now(); q.publishedVersion = q.version;
      S.receipts[qid] = { kind: 'verified', screens: ['平台章节页（' + now() + ' 核对）'], onlineVersion: q.version };
      var ch = chapter(q.chapter);
      if (ch) { ch.state = 'published'; ch.published = q.version; ch.publishedAt = q.plannedAt || now(); }
      logStep(qid + ' 回执核验为已上线');
      toast('已核验：线上版本 = 本地 ' + q.version + '；观察窗可建立', 'ok'); rerender();
    },
    waitReceipt: function (qid) {
      var q = queueItem(qid);
      q.state = 'waiting';
      S.receipts[qid] = { kind: 'pending', note: '平台回执未到。等待 ≠ 失败；到点后核验，不重发。' };
      toast('已登记为等待回执（不重发）', ''); rerender();
    },
    watchToggle: function (id) {
      var w = watch(id);
      w.state = w.state === 'paused' ? 'active' : 'paused';
      if (w.state === 'paused') { w.next = null; w.pausedBy = '作者'; } else { w.next = '2026-09-23 09:00'; w.state = 'active'; }
      if (w.state === 'active') w.state = 'active';
      logStep('关注 ' + id + ' → ' + w.state);
      toast(id + ' 已' + (w.state === 'paused' ? '暂停（保留历史快照）' : '恢复')); rerender();
    },
    watchRemove: function (id) {
      S.watches = S.watches.filter(function (w) { return w.id !== id; });
      logStep('移除关注 ' + id);
      toast('已移除关注；历史快照保留在市场观察中', ''); rerender();
    },
    watchCheck: function (id) {
      var w = watch(id);
      if (!w.scope || !w.source) { toast('先设置来源与观察范围，再执行检查', 'warn'); return; }
      if (w.state === 'failed') { toast('该渠道本轮不可读，保持失败与原因；不代替阅读', 'warn'); return; }
      if (w.state === 'paused') { toast('该关注已暂停，先恢复再检查', 'warn'); return; }
      w.last = now(); w.next = '2026-09-23 09:00'; w.result = '本次检查为 Mock：未产生新的公开页面读数';
      S.works.unshift({ id: 'W-1' + (10 + S.works.length), title: '立即检查 · ' + w.name, owner: 'E-02', status: 'wait', at: now(),
        artifact: '有界扫描记录（Mock）', next: '按频率等待下次；不连续抓取', area: 'market', obj: w.id });
      toast('已登记一次有界检查（Mock），并更新下次检查时间', 'ok'); rerender();
    },
    watchAdd: function () {
      S.watches.push({ id: 'W-' + Date.now(), name: '新关注（待配置）', kind: '榜单', source: '公开页面', scope: '', focus: '', window: '最近 7 日', metrics: '排名', cadence: '每周一 09:00',
        method: '正常授权浏览器浏览公开页面', state: 'paused', last: null, next: null, result: '尚未运行' });
      toast('已添加待配置关注；设置范围后再恢复检查', 'ok'); rerender();
    },
    refSave: function (id) {
      var r = byId(S.references, id);
      r.saved = !r.saved;
      toast(r.saved ? '已保存到参考列表（带来源与范围）' : '已取消保存'); rerender();
    },
    refToDirection: function (id) {
      S.__sel.refForDirection = id;
      go('market', 'direction', { from: id });
      toast('已把参考 ' + id + ' 带入方向提案，可继续修改', 'ok');
    },
    directionDecide: function (id, kind) {
      var d = byId(S.directions, id);
      if (kind === 'accept') {
        d.status = 'accepted'; d.acceptedAt = now();
        if (!d.bookId) {
          var nid = 'B-0' + (allBooks().length + 1);
          S.__runtime.createdBooks.push({ id: nid, title: '雾港来信（新建）', genre: d.genre, platform: d.platform,
            accountId: 'ACC-02', model: '付费订阅', status: '新建 · 未开写', startedAt: now().slice(0,10),
            positioning: d.core, audience: d.reader, volumeCount: 0, publishedCount: 0, formalStock: 0,
            goal: d.goal, origin: 'direction', originRef: d.id, imported: false });
          d.bookId = nid;
          S.__runtime.stock[nid] = { publishable: 0, planned: 0, draft: 0 };
          /* 已接受的方向进入本书定位（来源可追溯），其余定位字段待作者后补 */
          var nc = craftOf(nid);
          nc.positioning.genres = String(d.genre || '').split(/\s*[\/·、]\s*/).filter(Boolean);
          nc.positioning.coreOriginal = d.core || null;
          nc.positioning.platform = d.platform || null;
          nc.positioning.readerPromise = d.goal || null;
          nc.positioning.origin = 'direction'; nc.positioning.originRef = d.id; nc.positioning.updatedAt = now();
          nc.positioning.fields = { coreOriginal: 'confirmed', perspective: 'empty', style: 'empty',
            lengthPlan: 'empty', readerPromise: 'confirmed', genres: 'confirmed', readerPartition: 'empty' };
          toast('方向已接受，并创建了新 Book 身份（定位已带入，其余待后补）。历史作品与正文不受影响', 'ok');
        } else {
          S.works.unshift({ id: 'W-2' + (10 + S.works.length), title: '按方向 ' + id + ' 更新后续 Outline 提案', owner: 'E-01',
            status: 'working', at: now(), artifact: 'Outline 提案（未改历史章）', next: '作者确认后生效', area: 'book', obj: d.bookId });
          toast('方向已接受：后续 Outline 提案已生成；历史章不改动', 'ok');
        }
      } else {
        d.status = 'rejected'; d.decidedAt = now();
        toast('已拒绝该方向，理由保留；参考仍在参考列表中', '');
      }
      logStep('方向 ' + id + ' → ' + d.status); logStep('方向决定已记录'); rerender();
    },
    decision: function (id, key2) {
      var d = decision(id);
      d.status = key2 === 'defer' ? 'deferred' : 'applied';
      d.decision = key2; d.decidedAt = now(); d.appliedAt = now();
      if (id === 'DEC-01' && key2 === 'slow') {
        var b = book('B-01'); b.goal = '卷三完结第一卷主线，节奏调整为周更 2 章（作者已确认）';
        toast('已确认节奏调整：更新后续计划与下一检查；平台已排任务需单独核验', 'ok');
      } else if (id === 'DEC-01' && key2 === 'keep') {
        toast('已确认保持周更 3 章；ch44 的 Canon 冲突须先解决', 'ok');
      } else if (key2 === 'defer') {
        toast('已暂缓：待决不假装执行，研究与他书工作可继续', '');
      } else if (id === 'DEC-03') {
        var q = S.queue.filter(function (x) { return x.chapter === 'ch42'; })[0];
        if (q) { q.fixCandidate = 'R-42'; q.state = 'draft'; q.rejectReason = null; }
        toast('已授权重新提交（Gate 批准 ≠ 已上线）：请走人工路径提交并等待回执', 'ok');
      } else if (id === 'DEC-02') {
        toast('先处理候选逐项采纳，再回到正文工作面确认正式版本', '');
      }
      logStep('决定 ' + id + ' → ' + key2); rerender();
    },
    learningDecide: function (id, kind) {
      var l = learning(id);
      if (kind === 'accept') { l.accepted = 'author'; l.acceptedAt = now(); l.deactivated = false; toast('已接受：仅在你限定的范围内可用', 'ok'); }
      if (kind === 'deactivate') { l.deactivated = true; toast('已停用；旧的使用记录与历史分析保持不变', ''); }
      if (kind === 'question') { toast('已标记为待质疑：下次使用时会显示反例与未排除项', ''); }
      logStep('经验 ' + id + ' → ' + kind); rerender();
    },
    learningUse: function (id, where, reason) {
      var l = learning(id);
      if (!l || l.deactivated || l.accepted !== 'author' || !reason || !reason.trim()) { toast('经验需要作者接受、明确目标与具体改动，才能带入写作依据', 'warn'); return; }
      l.used++;
      S.learningUsage.push({ id: 'LU-' + (S.learningUsage.length + 1), learningId: id, where: where,
        target: '写作依据（' + where + '）', at: now(), decision: 'applied', reason: reason.trim(),
        source: l.evidence.slice(), scope: l.scope, counter: l.counter });
      toast('已带入 ' + where + ' 的写作依据；正文和大纲尚未自动改写，后续需回访验证', 'ok'); rerender();
    },
    entryResolve: function (id) {
      var e = byId(S.dataEntries, id);
      e.conflicts = 0; e.status = 'done'; e.resolvedAt = now();
      toast('已确认来源与时间窗，该行进入正式对比；原记录保留', 'ok'); rerender();
    },
    entryCorrect: function (id) {
      var e = byId(S.dataEntries, id);
      if (e.kind !== 'correction') { toast('该条不是订正记录'); return; }
      e.status = 'done';
      toast('订正已生效：原值保留在记录中，报表按订正后值显示', 'ok'); rerender();
    },
    assignOwner: function (workId, empId) {
      var w = byId(S.works, workId);
      w.owner = empId; w.next = '已指派，等待执行';
      toast('已指派给 ' + emp(empId).name + '；此前为缺责任人状态', 'ok'); rerender();
    },
    commentToEditor: function (cid) {
      var c = byId(S.comments.clusters, cid);
      var w = { id: 'W-3' + (10 + S.works.length), title: '评论反馈 → 修订问题 · ' + c.topic, owner: 'E-01', status: 'working', at: now(),
        artifact: '修订问题（' + c.anchor.chapter + '）· 样本 ' + c.size + ' 条', next: '编辑评估，回原分析', area: 'audience', obj: cid };
      S.works.unshift(w);
      logStep('评论簇 ' + cid + ' 转为编辑 Work');
      toast('已交给编辑；读者猜测不会写入 Canon', 'ok'); rerender();
    },
    confirmAnchor: function (cid) {
      var c = byId(S.comments.clusters, cid);
      c.anchor.conf = 'confirmed';
      toast('定位置信已改为「已确认」（依据：读者原文 + 编辑核对）'); rerender();
    },
    analysisToLearning: function (aid) {
      var a = analysis(aid);
      var d = a.layers.learningDraft;
      if (!d) { toast('本条只有书级数据 → 不生成章节经验', 'warn'); return; }
      modal({
        title: '生成经验候选 · 先声明适用边界',
        body: '<p>经验在被采用前必须写清「适用范围」与「尚未排除的干扰」；未声明的经验不会被接受，也不会自动套用到其他作品。</p>' +
          '<div class="inline" style="align-items:flex-start;margin-bottom:6px"><span class="t3 sm" style="min-width:74px">经验</span><span class="sm" style="flex:1"><b>' + esc(d.text) + '</b></span></div>' +
          '<div class="inline" style="align-items:flex-start;margin-bottom:6px"><span class="t3 sm" style="min-width:74px">适用范围</span><span class="sm" style="flex:1">' + esc(d.scope) + '</span></div>' +
          '<div class="inline" style="align-items:flex-start"><span class="t3 sm" style="min-width:74px">尚未排除</span><span class="sm" style="flex:1">' + esc(d.exclude) + '</span></div>' +
          '<div class="note danger" style="margin-top:10px"><b>反例随行：</b>' + esc(a.layers.counter) + '</div>' +
          '<div class="note bound">来源分析 ' + esc(a.id) + '（' + esc(a.window || '—') + '）；未经后续验证前记为「待验证」。</div>',
        footer: '<button class="btn" data-action="close-modal">取消</button>' +
          '<button class="btn primary" data-action="act.l" data-fn="learningCreate" data-a1="' + aid + '">确认生成经验候选</button>' });
    },
    learningCreate: function (aid) {
      var a = analysis(aid);
      var d = a.layers.learningDraft;
      if (!d) { toast('缺少适用范围声明，已取消', 'err'); return; }
      var l = { id: 'L-0' + (S.learnings.length + 1), text: d.text, kind: '正向',
        scope: d.scope, platform: '番茄', stage: '待验证',
        evidence: [aid], counter: a.layers.counter.slice(0, 60), used: 0, verified: 0,
        usedNote: '新候选：尚未应用与验证，先记录为待验证创作经验。',
        accepted: 'pending', acceptedAt: null, deactivated: false, notExcluded: d.exclude };
      S.learnings.push(l);
      a.learningId = l.id;
      logStep('分析 ' + aid + ' 生成经验候选 ' + l.id + '（范围：' + d.scope + '）');
      closeModal();
      toast('已生成经验候选 ' + l.id + '（待验证，未接受）：范围与反例已随行', 'ok'); rerender();
    },
    analysisToObservation: function (aid) {
      S.works.unshift({ id: 'W-4' + (10 + S.works.length), title: '观察计划 · ch45 受控观察', owner: 'E-04', status: 'wait', at: now(),
        artifact: '观察计划（同观察年龄 + 记录曝光）', next: 'ch45 发布后 7 日执行', area: 'audience', obj: aid });
      toast('已建立后续观察计划（不因单次数据改全书节奏）', 'ok'); rerender();
    },
    analysisToLeader: function (aid) {
      go('operate', 'plan', { focus: aid });
      toast('已带到经营计划与决定：显示依据、影响范围与选项');
    },
    revenueNote: function (bookId) {
      toast('已登记差异待办。缺财务责任人 → 只登记不对账，提现/税务留在平台', 'warn');
      S.works.unshift({ id: 'W-5' + (10 + S.works.length), title: '收益差异待办 · ' + bookId, owner: null, status: 'wait', at: now(),
        artifact: '差异待办（缺责任人）', next: '指派后才能核对', area: 'audience', obj: 'REV-DIFF' });
      rerender();
    },
    openEvidence: function (title, body, wide) {
      openDrawer({ title: title, sub: '证据审阅（Utility 最大化路径）', body: body, wide: !!wide,
        footer: '<span class="t3 sm">完整证据在此检查；返回后保留原筛选、选区与版本。</span>' });
    },
    bookScope: function (bookId) {
      S.__scope.bookId = bookId;
      var r = S.__route;
      craftOf(bookId);   /* 确保本书创作内核存在；空书得到真实空结构，不借他作样例 */
      logStep('切换作品范围 → ' + bookId);
      save();
      /* 对话也按作品隔离：上一本书的协作不跟着搬到新书（记录仍留在本机，切回即可继续） */
      if (S.__conv && S.__conv.open) {
        var cvBook = objBookId(S.__conv.obj);
        if (cvBook && cvBook !== bookId) { S.__conv.open = false; S.__conv.collapsed = false; S.__ui.discuss = false; }
      }
      if (r.area === 'book') {
        /* 切作品时清掉上一本书的章 / 选区，避免跨书串稿 */
        S.__sel = {};
        go('book', r.view, mixParams(r.params, { bookId: bookId, chapter: null }));
      } else render();
      toast('已切换作品：正文 / 大纲 / 人物 / 对话 / 审校按作品隔离，不串台', 'ok');
    },
    /* 开新书不是「直接建一张空卡」：先选起步方式，三条路都落到同一本 Book 身份（D05） */
    createBook: function () {
      var paths = startPaths();
      if (!paths.length) { toast('起步方式未加载', 'err'); return; }
      modal({ title: '开一本新书 · 先选从哪儿开始',
        body: '<div class="sm t2" style="margin-bottom:10px">从你现在手里有的内容开始。' +
          '<b>没有必填项</b>：任何一步都可以先跳过，未填不阻止写作。</div>' +
          paths.map(function (p) {
            return '<div class="note ' + (p.primary ? 'choice' : 'bound') + '" style="margin-bottom:8px">' +
              '<b>' + esc(p.name) + '</b> ' + (p.primary ? stBadge('推荐', 'choice') : '') +
              '<div class="sm t2" style="margin-top:3px">' + esc(p.desc) + '</div>' +
              '<div class="btnrow" style="margin-top:6px">' +
              '<button class="btn sm ' + (p.primary ? 'primary' : '') + '" data-action="act.b" data-fn="createBookPath" data-a1="' + esc(p.id) + '">从这里开始</button>' +
              '</div></div>';
          }).join(''),
        footer: '<button class="btn" data-action="close-modal">取消</button>' });
    },
    createBookPath: function (pathId) {
      closeModal();
      var pid = pathId || 'idea';
      var nid = 'B-0' + (allBooks().length + 1);
      S.__runtime.createdBooks.push({ id: nid, title: '新建作品（未命名）', genre: '待定', platform: '未选择', accountId: null,
        model: '—', status: '空书 · 可手写', startedAt: now().slice(0,10), positioning: '由作者直接手写，或先定方向', audience: '待定',
        volumeCount: 0, publishedCount: 0, formalStock: 0, goal: '待定', origin: 'manual', imported: false });
      S.__runtime.stock[nid] = { publishable: 0, planned: 0, draft: 0 };
      craftOf(nid);   /* 空书得到真实空创作结构：定位待填写、世界/大纲/人物为空 */
      var o = onbOf(nid);
      o.path = pid; o.step = 'idea'; o.startedAt = now(); o.updatedAt = now(); o.created = true;
      S.__scope.bookId = nid;
      save();
      go('book', 'overview', { bookId: nid });
      if (pid === 'write') {
        toast('已建立 Book 身份：直接开第 1 章手写，定位与方向稍后再补', 'ok');
        act.newChapter(nid);
        return;
      }
      if (pid === 'import') {
        toast('已建立 Book 身份；接着确认接入范围与章映射（不按书名自动匹配）', 'ok');
        act.importBook();
        return;
      }
      toast('已建立 Book 身份。在起步区写一句构思，编辑会接住它并给出具体方向候选', 'ok');
      var n = el('onbSeed');
      if (n && n.focus) n.focus();
    },
    /* 空书开写第一章：新建的是「草稿」，既不是候选也不是正式稿 */
    newChapter: function (bookId) {
      var b = book(bookId);
      var seq = Object.keys(S.chapters).filter(function (k) { return S.chapters[k].bookId === bookId; })
        .map(function (k) { return S.chapters[k].no || 0; });
      var no = (seq.length ? Math.max.apply(null, seq) : 0) + 1;
      if (!S.volumes[bookId] || !S.volumes[bookId].length) {
        S.volumes[bookId] = [{ id: 'V-01', name: '卷一 · 起', open: true, chapters: ['ch1', 'ch998'] }];
      }
      var nid = 'ch-' + bookId + '-' + no;
      S.chapters[nid] = { bookId: bookId, vol: S.volumes[bookId][0].id, no: no, title: '未命名',
        formal: null, published: null, candidate: null, state: 'draft', createdAt: now(), authoredBy: 'author' };
      b.volumeCount = S.volumes[bookId].length;
      logStep('新建章节 ' + nid + '（草稿，未发布）');
      S.__scope.bookId = bookId;
      toast('已新建第 ' + no + ' 章：草稿状态，尚未成为正式稿', 'ok');
      go('book', 'manuscript', { bookId: bookId, chapter: nid });
    },
    importBook: function () {
      modal({ title: '接入已有平台作品',
        body: '<p>接入既有连载的操作：</p><ol style="padding-left:18px;line-height:1.8">' +
          '<li>填写平台与作品外部 ID（不按书名自动匹配）</li><li>确认可用正文范围（只导入公开元数据不等于拥有全文）</li>' +
          '<li>逐条确认内部章与平台章的映射</li><li>缺正文的历史段落不做精确归因</li></ol>' +
          '<div class="note bound">不会另建「平台书」与「创作书」两套身份；导入完成后仍是同一个 Book。</div>',
        footer: '<button class="btn" data-action="close-modal">取消</button><button class="btn primary" data-action="act.bk" data-fn="importConfirmed">确认接入（示例）</button>' });
    },
    importConfirmed: function () {
      closeModal();
      S.__scope.bookId = 'B-02';
      toast('已接入《白鹭洲纪事》：映射 18 章已确认，第 19 章为本地新章', 'ok');
      go('book', 'overview', { bookId: 'B-02' });
    },
    resetDemo: function () {
      modal({ title: '重置演示数据',
        body: '<p>将清除本机浏览器中保存的演示状态（候选采纳、队列改动、关注配置、数据补录、经验接受、对话等），恢复到初始样例。</p>' +
          '<div class="note bound">只影响本原型的 localStorage，不影响任何 Curis 文档、代码或平台账号。</div>',
        footer: '<button class="btn" data-action="close-modal">取消</button><button class="btn dark" data-action="act.rst" data-fn="resetConfirmed">确认重置</button>' });
    },
    resetConfirmed: function () { closeModal(); reset(); render(); toast('演示数据已重置', 'ok'); }
  };

  /* ---------------- 讨论的行动入口（作者驱动；采纳只落到显式对象） ---------------- */
  on['conv.draft']=function(_,d){keepConvDraft();save();};
  on['conv.send'] = function (elm, d) { convSend(d.emp, d.obj); };
  on['conv.acceptItem'] = function (elm, d) {
    if (convApplyItem(d.pid, d.item)) {
      save(); render(); renderConvMsgs();
      toast('已采纳并写入目标对象；其余项保持不变，正式稿与线上稿未变', 'ok');
    }
  };
  on['conv.rejectItem'] = function (elm, d) {
    var p = S.discussProps[d.pid]; if (!p) return;
    var it = byId(p.items, d.item);
    if (!it || it.applied != null) return;
    it.applied = false; it.appliedAt = now();
    save(); renderConvMsgs();
    toast('该项已拒绝；目标对象未改动（拒绝与采纳一样会被记录）', '');
  };
  on['conv.editItem'] = function (elm, d) {
    var p = S.discussProps[d.pid], it = p && byId(p.items, d.item);
    if (!it) return;
    modal({ title: '改后再采纳 · ' + it.id,
      body: '<div class="fld"><label>提案文字（你可以直接改）</label><textarea class="ta" id="propEdit" rows="5">' + esc(it.after) + '</textarea></div>' +
        '<div class="note bound">改写后再采纳：只落到该对象；正式稿与线上稿不会被改动。</div>',
      footer: '<button class="btn" data-action="close-modal">取消</button>' +
        '<button class="btn primary" data-action="conv.editItemDo" data-pid="' + d.pid + '" data-item="' + d.item + '">改后采纳</button>' });
  };
  on['conv.editItemDo'] = function (elm, d) {
    var v = (document.getElementById('propEdit') || {}).value;
    if (!v || !v.trim()) { toast('内容不能为空', 'warn'); return; }
    var ok = convApplyItem(d.pid, d.item, v.trim());
    closeModal();
    if (ok) { save(); render(); renderConvMsgs(); toast('已按你的改写采纳并写入目标对象', 'ok'); }
    else save();
  };
  on['conv.acceptRest'] = function (elm, d) {
    var p = S.discussProps[d.pid]; if (!p) return;
    var n = 0;
    p.items.slice().forEach(function (it) { if (it.applied == null && convApplyItem(p.id, it.id)) n++; });
    save(); render(); renderConvMsgs();
    toast(n ? ('已采纳剩余 ' + n + ' 项并写入 ' + p.targetLabel) : '没有剩余可采纳项', n ? 'ok' : 'warn');
  };
  on['conv.continue'] = function (elm, d) {
    var p = S.discussProps[d.pid]; if (!p) return;
    var cv = S.__conv || {};
    var empId = p.by || cv.empId, obj = p.sourceObj || cv.obj;
    if(obj!==cv.obj){openConv(empId,obj,p.targetLabel);toast('已回到这条建议的讨论范围，请输入后继续。');return;}
    if (!empId) { toast('协作区未打开：请先在对象或正文选区处发起讨论', 'warn'); return; }
    var inp = el('convInput');
    var req = inp ? String(inp.value || '').trim() : '';
    if (!req) {
      toast('继续讨论要你再提一句要求（例如：再短一点）——输入框在等你', 'warn');
      if (inp && inp.focus) inp.focus();
      return;
    }
    inp.value = '';S.__convDrafts=S.__convDrafts||{};S.__convDrafts[empId+'|'+obj]='';
    var k = convKey(empId, obj);
    S.conversations[k].push({ who: 'me', text: req, at: now() });
    var res = WB.discussEngine ? WB.discussEngine(empId, obj, req, { continueOf: p.id }) : null;
    if (!res || !res.supported) {
      S.conversations[k].push({ who: 'emp', at: now(), demo: true, took: (res && res.took) || '',
        text: (res && res.reply) || '这条我暂时没有可模拟的处理路径。',
        next: '本轮只处理尚未裁定的范围；已裁定的项不会被再次改动。' });
    } else {
      S.conversations[k].push({ who: 'emp', at: now(), demo: true, took: res.took, text: res.reply,
        propId: res.propId || null, next: res.next });
    }
    save(); renderConvMsgs();
  };

  /* ---- 三栏（左 Context / 中 Main / 右 Utility）开合与对象切换 ---- */
  function truthy(v) { return v === '1' || v === 1 || v === true || v === 'true'; }
  on['ui.rail'] = function (elm, d) {
    S.__ui.rail = (d.on === undefined || d.on === '') ? !S.__ui.rail : truthy(d.on);
    save(); render();
  };
  on['ui.aside'] = function (elm, d) {
    S.__ui.aside = (d.on === undefined || d.on === '') ? !S.__ui.aside : truthy(d.on);
    if (!S.__ui.aside) closeAsideDraft();
    save(); render();
    if (S.__ui.aside) toast('右栏（Utility）已展开：属性 / 证据 / 版本在需要时才占空间');
  };
  on['ui.bookSwitch'] = function () { openBookSwitch(); };
  on['conv.toggleCollapse'] = function () { convCollapse(); };
  on['conv.close'] = function () { convClose(); };
  /* 切换作品：不改任何稿件与选择，只换当前 Book 范围 */
  function openBookSwitch() {
    var cur = scopeBook();
    var rows = allBooks().map(function (b) {
      return '<button class="btn' + (cur && cur.id === b.id ? ' primary' : '') + '" style="display:block;width:100%;text-align:left;margin-bottom:6px" ' +
        'data-action="ui.pickBook" data-id="' + esc(b.id) + '">' + esc(b.title) +
        '<span class="sm t3" style="display:block">' + esc(b.id) + ' · ' + esc(b.status || '') + '</span></button>';
    }).join('');
    modal({ title: '切换当前作品', body: '<div class="sm t2" style="margin-bottom:8px">切换只改变当前工作范围，不改动任何书稿、候选或创作选择。</div>' + rows,
      footer: '<button class="btn" data-action="close-modal">取消</button>' });
  }
  on['ui.pickBook'] = function (elm, d) {
    /* 与 act.bookScope 走同一条切换逻辑：稿件 / 选区 / 对话都按作品隔离，不串台 */
    closeModal();
    act.bookScope(d.id);
  };
  /* 右栏是有边界的检查栏：切对象前保存或取消未保存的有限编辑，不静默丢弃 */
  function closeAsideDraft() {
    var ta = el('aside') && el('aside').querySelector('textarea[data-draft]');
    if (ta && ta.value && String(ta.value).trim()) {
      S.__asideDraft = S.__asideDraft || {};
      S.__asideDraft[ta.getAttribute('data-draft')] = ta.value;
      toast('右栏未保存的编辑已暂存为草稿（重新展开可继续）', 'warn');
    }
  }

  function chBookKey(k) { var c = chapter(k); return c ? c.bookId : null; }

  /* ---------------- 事件分发 ---------------- */
  function handleAction(elm) {
    var name = elm.getAttribute('data-action');
    var d = {};
    for (var i = 0; i < elm.attributes.length; i++) {
      var a = elm.attributes[i];
      if (a.name.indexOf('data-') === 0) d[a.name.slice(5).replace(/-([a-z])/g, function (m, c) { return c.toUpperCase(); })] = a.value;
    }
    if (name === 'close-drawer') { closeDrawer(); return; }
    if (name === 'close-modal') { closeModal(); return; }
    if (name === 'nav.area') { go(d.area, NAV.filter(function (n) { return n.area === d.area; })[0].views[0][0]); return; }
    if (name === 'nav.view') { var params={}; ['bookId','chapter','mode','stage','id','full'].forEach(function(k){if(d[k])params[k]=d[k];}); go(d.area, d.view, params); return; }
    if (name === 'back') { back(); return; }
    if (name.indexOf('act.') === 0) {
      var fn = act[d.fn];
      var args = [];
      for (var k = 1; k <= 4; k++) if (d['a' + k] !== undefined) args.push(coerce(d['a' + k]));
      if (typeof fn === 'function') {
        /* 叠层内的行动：完成后回到原上下文。若该行动另行打开了新叠层，则不干预。 */
        var inModal = el('modal').classList.contains('on');
        var inDrawer = el('drawer').getAttribute('aria-hidden') !== 'true';
        var epoch = overlayEpoch;
        fn.apply(null, args);
        if (overlayEpoch === epoch) {
          if (inModal && el('modal').classList.contains('on')) closeModal();
          if (inDrawer && el('drawer').getAttribute('aria-hidden') !== 'true') closeDrawer();
        }
      } else toast('未实现的行动：' + d.fn, 'err');
      return;
    }
    var h = on[name];
    if (h) h(elm, d); else toast('未实现的行动：' + name, 'err');
  }
  function coerce(v) {
    if (v === 'true') return true;
    if (v === 'false') return false;
    if (v === 'null') return null;
    return v;
  }

  /* ---------------- 初始化 ---------------- */
  /* 拖动调宽：只在拖动期间改样式，松手后写回状态；不触发整页重建，避免正文选区丢失。 */
  function bindResize(handleId, apply, measure) {
    var h = el(handleId);
    if (!h) return;
    h.addEventListener('mousedown', function (ev) {
      ev.preventDefault();
      var startX = ev.clientX, startW = measure();
      var app = el('app');
      function onMove(e2) {
        var nx = apply(e2.clientX - startX, startW);
        var prop = handleId === 'railResize' ? '--rail-w' : '--aside-w';
        if (nx) app.style.setProperty(prop, nx + 'px');
      }
      function onUp() {
        document.removeEventListener('mousemove', onMove);
        document.removeEventListener('mouseup', onUp);
        save(); render();
      }
      document.addEventListener('mousemove', onMove);
      document.addEventListener('mouseup', onUp);
    });
  }
  function init() {
    load();
    document.addEventListener('click', function (e) {
      var t = e.target.closest ? e.target.closest('[data-action]') : null;
      if (t) { e.preventDefault(); handleAction(t); }
    });
    document.addEventListener('change', function (e) {
      var t = e.target.closest ? e.target.closest('[data-change]') : null;
      if (!t) return;
      var name = t.getAttribute('data-change'), h = on[name];
      var d = { value: t.value, id: t.getAttribute('data-id') };
      if (h) h(t, d); else toast('未实现的变更：' + name, 'err');
    });
    /* 实时输入（搜索框 / 自然语言要求草稿）：只更新草稿，不重建整页，避免打断输入 */
    document.addEventListener('input', function (e) {
      var t = e.target.closest ? e.target.closest('[data-input]') : null;
      if (!t) return;
      var name = t.getAttribute('data-input'), h = on[name];
      var d = { value: t.value, id: t.getAttribute('data-id') };
      if (h) h(t, d);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { closeDrawer(); closeModal(); }
    });
    /* 调宽把手：左栏 / 右栏都可拖动改变宽度，状态写回本机（不改变任何稿件或选择） */
    bindResize('railResize', function (dx, startW) {
      S.__ui.railW = Math.max(180, Math.min(420, startW + dx));
      return S.__ui.railW;
    }, function () { return el('rail').getBoundingClientRect().width; });
    bindResize('asideResize', function (dx, startW) {
      S.__ui.asideW = Math.max(260, Math.min(560, startW - dx));
      return S.__ui.asideW;
    }, function () { return el('aside').getBoundingClientRect().width; });
    render();
    if (!storageOK) toast('浏览器存储不可用：改动只保留在内存中', 'warn');
  }

  return {
    D: D, get S() { return S; }, act: act, on: on, register: register, views: views,
    init: init, go: go, back: back, rerender: rerender, render: render,
    save: save, now: now, esc: esc, clone: clone,
    book: book, allBooks: allBooks, emp: emp, chapter: chapter, candidate: candidate, decision: decision,
    learning: learning, watch: watch, queueItem: queueItem, analysis: analysis, byId: byId,
    scopeBook: scopeBook, ownerHtml: ownerHtml, st: st, stBadge: stBadge, unknown: unknown, money: money,
    craftOf: craftOf, blankCraftFor: blankCraftFor, factBadge: factBadge, mixParams: mixParams,
    chapState: chapState, candidateState: candidateState, areaBadges: areaBadges, stockOf: stockOf,
    navName: navName, viewName: viewName, NAV: NAV,
    openDrawer: openDrawer, closeDrawer: closeDrawer, modal: modal, closeModal: closeModal, toast: toast,
    openConv: openConv, convSend: convSend, convAsk: convAsk, asBlock: asBlock, workHtml: workHtml,
    onbOf: onbOf, onbState: onbState, onbSteps: function () { return ONB_STEPS; },
    startPaths: startPaths, startDirections: startDirections,
    msOf: msOf, msEnsure: msEnsure, draftDiverged: draftDiverged, snapshotOf: snapshotOf,
    renderConvMsgs: renderConvMsgs, convKey: convKey, convApplyItem: convApplyItem,
    sharedDock: sharedDock, convCollapse: convCollapse, convClose: convClose, convCtxTag: convCtxTag,
    tagDef: tagDef, writingTags: writingTags, tagGroups: tagGroups, tagSuggestions: tagSuggestions,
    tagsOf: tagsOf, tagPicked: tagPicked, tagTouched: tagTouched, tagRequirement: tagRequirement,
    tagBrief: tagBrief, tagSubKey: tagSubKey, tagEntry: tagEntry, chapterTagOverride: chapterTagOverride,
    applyChrome: applyChrome, mainBar: mainBar,
    VERSION: VERSION, STORE_KEY: STORE_KEY, BACKUP_PREFIX: BACKUP_PREFIX,
    ownerOpts: function () { return S.employees.map(function (e) { return { id: e.id, name: e.name }; }); },
    submitModes: D.submitModes
  };
})();
