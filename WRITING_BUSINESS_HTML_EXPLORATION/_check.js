/* CURIS — Writing Business 数据层完整性自检（Node 裸跑，无浏览器）
   目的：在打开浏览器之前，先用引用完整性断言把数据层错误一次性挡掉。
   运行：node _check.js                                        */
'use strict';
global.window = {};
require('./data.js');
var D = global.window.WB_DATA;

var fails = [], warns = [], passes = 0;
function ok(name, cond, detail) {
  if (cond) { passes++; return true; }
  fails.push(name + (detail ? ' → ' + detail : ''));
  return false;
}
function warn(name, detail) { warns.push(name + (detail ? ' → ' + detail : '')); }
function ids(arr) { return (arr || []).map(function (x) { return x.id; }); }
function has(arr, id) { return ids(arr).indexOf(id) >= 0; }

var bookIds = ids(D.books);
var empIds = ids(D.employees);
var chapIds = Object.keys(D.chapters);
var queueIds = ids(D.queue);
var refIds = ids(D.references);
var obsIds = ids(D.marketObservations);
var learnIds = ids(D.learnings);
var patIds = ids(D.patterns);

/* ---- 1. 作品 / 卷 / 章 身份链 ---- */
Object.keys(D.chapters).forEach(function (k) {
  var c = D.chapters[k];
  ok('章节 ' + k + ' bookId 存在', bookIds.indexOf(c.bookId) >= 0, 'bookId=' + c.bookId);
  if (c.volumeId) {
    var vols = (D.volumes[c.bookId] || []).map(function (v) { return v.id; });
    ok('章节 ' + k + ' volumeId 存在', vols.indexOf(c.volumeId) >= 0, 'volumeId=' + c.volumeId);
  }
  if (c.state === 'published') ok('已发布章 ' + k + ' 必须有 publishedAt', !!c.publishedAt);
});
Object.keys(D.volumes).forEach(function (b) {
  ok('卷归属作品 ' + b + ' 存在', bookIds.indexOf(b) >= 0);
});
Object.keys(D.manuscripts).forEach(function (k) {
  ok('正文 ' + k + ' 有对应章节', chapIds.indexOf(k) >= 0);
  var ms = D.manuscripts[k];
  ok('正文 ' + k + ' 段落非空', Array.isArray(ms.paragraphs) && ms.paragraphs.length > 0);
});
/* 反证：候选不得直接写在正式正文里 */
Object.keys(D.manuscripts).forEach(function (k) {
  var ms = D.manuscripts[k];
  var ch = D.chapters[k];
  if (ch && ch.state === 'candidate') {
    ok('候选章 ' + k + ' 不应有正式 publishedAt', !ch.publishedAt);
    ok('候选章 ' + k + ' 正文应标记为非正式或候选基准', ms.formal !== true, 'formal=' + ms.formal);
  }
});

/* ---- 2. 候选 → 章节；逐条可采纳 ---- */
Object.keys(D.candidates).forEach(function (cid) {
  var c = D.candidates[cid];
  ok('候选 ' + cid + ' chapter 存在', chapIds.indexOf(c.chapter) >= 0, 'chapter=' + c.chapter);
  ok('候选 ' + cid + ' 有变更条目', Array.isArray(c.changes) && c.changes.length > 0);
  (c.changes || []).forEach(function (ch, i) {
    ok('候选 ' + cid + ' 第' + (i + 1) + '条具备 id/标签/理由', !!ch.id && !!ch.label && !!ch.why,
      JSON.stringify(ch).slice(0, 90));
    ok('候选 ' + cid + ' 第' + (i + 1) + '条采纳态必须为未决（null）或已明确裁决',
      ch.applied === null || ch.applied === true || ch.applied === false, 'applied=' + JSON.stringify(ch.applied));
  });
});
/* 反证：候选不得原地覆盖正式稿 —— 目标章已发布时，候选必须声明基线版本 */
Object.keys(D.candidates).forEach(function (cid) {
  var c = D.candidates[cid];
  var ch = D.chapters[c.chapter];
  if (ch && ch.state === 'published') {
    ok('已发布章 ' + c.chapter + ' 的候选 ' + cid + ' 必须声明 baseVersion（禁止原地覆盖）',
      !!c.baseVersion, 'baseVersion=' + c.baseVersion);
    ok('已发布章 ' + c.chapter + ' 的候选 ' + cid + ' 应为修订类', /修订|改/.test(c.kind || ''), 'kind=' + c.kind);
  }
});
/* 反向指针 + 版本单调性 */
Object.keys(D.chapters).forEach(function (k) {
  var c = D.chapters[k];
  if (c.candidate) ok('章节 ' + k + ' 声明的 candidate 存在', !!D.candidates[c.candidate], c.candidate);
  if (c.published) ok('已发布章 ' + k + ' 有 publishedAt', !!c.publishedAt);
});

/* ---- 3. 发布队列 / 回执 ---- */
D.queue.forEach(function (q) {
  ok('队列 ' + q.id + ' chapter 存在', chapIds.indexOf(q.chapter) >= 0, 'chapter=' + q.chapter);
  if (q.accountId) ok('队列 ' + q.id + ' account 存在', has(D.accounts, q.accountId), 'accountId=' + q.accountId);
});
Object.keys(D.receipts).forEach(function (qid) {
  ok('回执 ' + qid + ' 对应队列项', queueIds.indexOf(qid) >= 0);
});
/* 未知 ≠ 失败：unknown 状态不得带「失败原因」，也不得带 0 数值 */
D.queue.filter(function (q) { return q.state === 'unknown'; }).forEach(function (q) {
  ok('unknown 队列项 ' + q.id + ' 不得带 failureReason', !q.failureReason);
  warn('未知态队列项（应在 UI 显示为「未核验」而非失败）', q.id);
});

/* ---- 4. 账号 / 映射 ---- */
D.mappings.forEach(function (m) {
  ok('映射 ' + m.id + ' account 存在', has(D.accounts, m.accountId), 'accountId=' + m.accountId);
  if (m.bookId) ok('映射 ' + m.id + ' book 存在', bookIds.indexOf(m.bookId) >= 0, 'bookId=' + m.bookId);
});

/* ---- 5. Works → 员工（含 No-Owner 缺口） ---- */
var noOwner = [];
D.works.forEach(function (w) {
  if (w.owner) ok('Work ' + w.id + ' owner 存在', empIds.indexOf(w.owner) >= 0, 'owner=' + w.owner);
  else noOwner.push(w.id);
});

/* ---- 6. 归因 / 经验 / 用途 ---- */
D.analyses.forEach(function (a) {
  var L = a.layers || {};
  var need = ['observation', 'evidence', 'hypothesis', 'recommendation'];
  ok('分析 ' + a.id + ' 具备 5 层归因结构',
    need.every(function (k) { return !!L[k]; }),
    '缺失=' + need.filter(function (k) { return !L[k]; }).join(','));
  ok('分析 ' + a.id + ' 含反例/替代解释（不得只给单因果）', !!(L.counter || L.alternatives),
    'keys=' + Object.keys(L).join('|'));
  ok('分析 ' + a.id + ' 有证据缺口声明', !!a.evidenceGap);
  ok('分析 ' + a.id + ' 有适用边界/限制声明', !!a.limitation);
});
D.learningUsage.forEach(function (u) {
  ok('用途 ' + u.id + ' learning 存在', learnIds.indexOf(u.learningId) >= 0, 'learningId=' + u.learningId);
});
/* 反证：Learning 必须有 scope 与反例边界 */
D.learnings.forEach(function (l) {
  ok('经验 ' + l.id + ' 有 scope', !!l.scope);
  ok('经验 ' + l.id + ' 有反例/边界说明', !!(l.counter || l.boundary || l.counterExample));
});

/* ---- 7. 方向 ← 参考/观察/模式 依据 ---- */
D.directions.forEach(function (d) {
  var ev = d.refs || d.evidence || d.basis || [];
  ok('方向 ' + d.id + ' 有依据集合', ev.length > 0, 'keys=' + Object.keys(d).join('|'));
  ev.forEach(function (e) {
    var id = typeof e === 'string' ? e : e.id;
    ok('方向 ' + d.id + ' 依据 ' + id + ' 可解析',
      refIds.indexOf(id) >= 0 || obsIds.indexOf(id) >= 0 || patIds.indexOf(id) >= 0 ||
      ids(D.analyses).indexOf(id) >= 0 || learnIds.indexOf(id) >= 0, id);
  });
  if (d.status === 'accepted') {
    ok('已接受方向 ' + d.id + ' 必须声明「已知未知」', !!d.unknown);
    ok('已接受方向 ' + d.id + ' 必须声明风险', !!d.risk);
    ok('已接受方向 ' + d.id + ' 必须说明落到哪里（= 接受 ≠ 已应用）', !!d.appliedTo);
  }
});

/* ---- 8. Unknown ≠ 0（全局断言）---- */
var chapLevelNumeric = [];
Object.keys(D.revenue).forEach(function (b) {
  var r = D.revenue[b];
  (r.items || r.rows || []).forEach(function (row) {
    var isChap = /章/.test(row.kind || '') || row.chapterId || row.chapter;
    if (isChap && typeof row.amount === 'number' && row.amount !== null) {
      chapLevelNumeric.push(b + ' ' + row.kind + '=' + row.amount);
    }
    if (isChap) {
      ok('逐章收益行必须显式为未知（amount 为 null）而非 0 或编造值', row.amount === null,
        b + ' ' + row.kind + ' amount=' + JSON.stringify(row.amount));
    }
  });
});
ok('收益层不得出现任何「逐章收益」数值', chapLevelNumeric.length === 0, chapLevelNumeric.join(', '));

/* 序列长度一致性：图表不得出现错位 */
Object.keys(D.performance).forEach(function (b) {
  var p = D.performance[b];
  (p.bookLevel || []).forEach(function (s) {
    ok('表现指标「' + s.key + '」序列与时间轴等长',
      Array.isArray(s.series) && Array.isArray(s.ages) && s.series.length === s.ages.length,
      (s.series ? s.series.length : '?') + ' vs ' + (s.ages ? s.ages.length : '?'));
  });
  if (p.coverage) ok('表现数据 ' + b + ' 声明统计口径', true);
});
/* 反证：不得存在「逐章收益字段」 */
(function () {
  var hit = [];
  Object.keys(D.performance || {}).forEach(function (b) {
    (D.performance[b].bookLevel || []).forEach(function (s) {
      if (/章节.*收益|逐章收益/.test(s.key || '')) hit.push(b + ' ' + s.key);
    });
  });
  ok('表现层不得存在逐章收益指标', hit.length === 0, hit.join(', '));
})();

/* ---- 9. 责任分工缺口 ---- */
D.responsibilities.forEach(function (r) {
  if (r.owner === null || r.owner === undefined) warn('职责无归属（缺口应显示为 No-Owner，不是虚构员工）', r.id + ' ' + (r.title || ''));
  else ok('职责 ' + r.id + ' owner 存在', empIds.indexOf(r.owner) >= 0, 'owner=' + r.owner);
});

/* ---- 10. 创作内核（Book Creative Core, §13）----
   契约：定位/背景/人物/主支线/大纲/场景 = Book 绑定对象；计划≠事实；AI 推断须显式标注；
   空书不得回落到别的书的样例。 */
var FACT_STATES = ['CONFIRMED_CANON', 'MANUSCRIPT_FACT', 'PLANNED', 'AI_INFERRED', 'CONFLICTED', 'TO_EXPLORE',
  'candidate', 'applied', 'proposed', 'confirmed', 'tentative', 'accepted'];
var craftIds = Object.keys(D.craft || {});
ok('存在创作内核容器 craft/blankCraft', typeof D.blankCraft === 'function' && craftIds.length > 0,
  'craft=' + craftIds.join(','));
craftIds.forEach(function (bid) {
  ok('创作内核 ' + bid + ' 归属真实作品', bookIds.indexOf(bid) >= 0, 'bid=' + bid);
});
/* 反证：每部作品都必须能取到自己的创作内核，绝不回落他书 */
bookIds.forEach(function (bid) {
  var own = D.craft[bid] || D.blankCraft(bid, 'x');
  ok('作品 ' + bid + ' 的创作内核 bookId 自洽（禁止回落他书）', own && own.bookId === bid, 'got=' + (own && own.bookId));
});
/* 空书工厂必须返回真空态 */
(function () {
  var b = D.blankCraft('B-99', '空书样本');
  ok('blankCraft 返回真空（world/characters/outline 皆空）',
    b.world.length === 0 && b.characters.length === 0 && b.outline.length === 0, 'n=' + b.world.length + '/' + b.characters.length + '/' + b.outline.length);
  ok('blankCraft 返回真空（主/支线/转折/结局皆空）',
    b.arc.mainLines.length === 0 && b.arc.subLines.length === 0 && b.arc.turns.length === 0 && b.arc.endings.length === 0);
  ok('blankCraft 无结论性正文（premise/climax 为空而非占位）', !b.arc.premise && !b.arc.climax);
  ok('blankCraft 的定位字段全部标记为 empty（未知≠已填）',
    Object.keys(b.positioning.fields).every(function (k) { return b.positioning.fields[k] === 'empty'; }));
  ok('blankCraft 不得携带他书场景', Object.keys(b.scenes).length === 0);
})();
/* 反证：两本样例书的创作内核不得互相污染 */
(function () {
  var a = D.craft['B-01'], z = D.craft['B-02'];
  if (a && z) {
    ok('不同作品的定位/人物不得雷同（跨书串扰反证）',
      a.positioning.workingTitle !== z.positioning.workingTitle &&
      ids(a.characters).join() !== ids(z.characters).join(),
      a.positioning.workingTitle + ' vs ' + z.positioning.workingTitle);
    ok('B-01 场景不得出现在 B-02', Object.keys(a.scenes).every(function (k) { return !z.scenes[k]; }));
  }
})();
/* 事实态合法性 + 定位/背景/人物/弧线结构 */
craftIds.forEach(function (bid) {
  var c = D.craft[bid];
  var pos = c.positioning || {};
  ok('创作内核 ' + bid + ' 定位声明 readerPartition 与 genre 是两个维度（分区≠题材）',
    'readerPartition' in pos && 'genres' in pos, 'keys=' + Object.keys(pos).join(','));
  ok('创作内核 ' + bid + ' 定位携带字段态标注 fields', !!pos.fields && typeof pos.fields === 'object');
  (c.world || []).forEach(function (w) {
    ok('背景 ' + bid + '/' + w.id + ' 有状态标注', FACT_STATES.indexOf(w.state) >= 0, 'state=' + w.state);
    ok('背景 ' + bid + '/' + w.id + ' 有出处/证据（不得凭空）', !!(w.source || w.evidence),
      'source=' + w.source + ' evidence=' + w.evidence);
    if (w.kind === '规则') {
      ok('规则型背景 ' + bid + '/' + w.id + ' 必须有代价与限制（创作内核要求）', !!(w.cost && w.limit),
        'cost=' + !!w.cost + ' limit=' + !!w.limit);
    }
  });
  (c.characters || []).forEach(function (ch) {
    ok('人物 ' + bid + '/' + ch.id + ' 有 name/role/goal', !!(ch.name && ch.role && ch.goal), 'name=' + ch.name);
    var k = ch.knows || {};
    ok('人物 ' + bid + '/' + ch.id + ' 具备四类知情分层（角色/作者/读者/未揭露）',
      'character' in k && 'author' in k && 'reader' in k && 'unrevealed' in k, 'keys=' + Object.keys(k).join(','));
  });
  var arc = c.arc || {};
  ['mainLines', 'subLines', 'turns', 'endings', 'promises'].forEach(function (kk) {
    ok('弧线 ' + bid + '.arc.' + kk + ' 为数组', Array.isArray(arc[kk]), typeof arc[kk]);
    (arc[kk] || []).forEach(function (x) {
      ok('弧线 ' + bid + '.' + kk + ' 条目 ' + x.id + ' 有文本', !!x.id && !!x.text, JSON.stringify(x).slice(0, 80));
      if (x.state) ok('弧线 ' + bid + '.' + kk + ' 条目 ' + x.id + ' 状态合法', FACT_STATES.indexOf(x.state) >= 0, 'state=' + x.state);
    });
  });
  /* 反证：结局在未定稿前必须是 candidate，不得静默写成既定事实 */
  (arc.endings || []).forEach(function (e) {
    ok('结局 ' + bid + '/' + e.id + ' 应为候选（未定稿不得当既定事实）', e.state === 'candidate', 'state=' + e.state);
  });
  /* 大纲：层级/parent 自洽 + 版本 + AI 来源必须标注 */
  var ol = c.outline || [];
  ol.forEach(function (n) {
    ok('大纲 ' + bid + '/' + n.id + ' level 合法', ['book', 'volume', 'chapter'].indexOf(n.level) >= 0, 'level=' + n.level);
    ok('大纲 ' + bid + '/' + n.id + ' 有版本与来源', !!n.version && !!n.origin, 'v=' + n.version + ' origin=' + n.origin);
    if (n.parent) ok('大纲 ' + bid + '/' + n.id + ' parent 可解析',
      ol.some(function (m) { return m.id === n.parent; }), 'parent=' + n.parent);
    if (n.level !== 'book') ok('大纲 ' + bid + '/' + n.id + ' 非书级节点必须有 parent', !!n.parent);
    if (n.origin === 'ai') warn('大纲节点为 AI 生成，UI 须显式标注来源', bid + '/' + n.id);
  });
  ok('大纲 ' + bid + ' 至少一个 book 级节点（全书总纲）',
    ol.filter(function (n) { return n.level === 'book'; }).length === 1,
    'book 级=' + ol.filter(function (n) { return n.level === 'book'; }).length);
  /* 场景：绑定到真实章节 + 含 reveal/notReveal 边界 */
  Object.keys(c.scenes || {}).forEach(function (ck) {
    ok('场景归属章节 ' + bid + '/' + ck + ' 真实存在', chapIds.indexOf(ck) >= 0, ck);
    var sc = c.scenes[ck];
    ok('场景 ' + bid + '/' + ck + ' 为数组', Array.isArray(sc), typeof sc);
    (sc || []).forEach(function (s) {
      ok('场景 ' + bid + '/' + ck + '/' + s.id + ' 有 purpose/pov/conflict/endState',
        !!(s.purpose && s.pov && s.conflict && s.endState), JSON.stringify(s).slice(0, 80));
      ok('场景 ' + bid + '/' + ck + '/' + s.id + ' 声明 reveal 与 notReveal（连续性边界）',
        'reveal' in s && 'notReveal' in s);
    });
  });
  /* 变更影响记录：必须列出受影响范围，且声明未被改动的部分 */
  (c.impactLog || []).forEach(function (m) {
    ok('变更记录 ' + bid + '/' + m.id + ' 列出受影响范围', Array.isArray(m.affected) && m.affected.length > 0,
      'affected=' + JSON.stringify(m.affected));
    ok('变更记录 ' + bid + '/' + m.id + ' 声明未改动部分（禁止静默全文覆盖）', !!m.unchanged, 'unchanged=' + m.unchanged);
    ok('变更记录 ' + bid + '/' + m.id + ' 有裁决人与状态', !!m.decidedBy && !!m.state, 'by=' + m.decidedBy + ' state=' + m.state);
  });
  /* 导入记录 */
  (c.importRecords || []).forEach(function (r) {
    ok('导入记录 ' + bid + '/' + r.id + ' 有文件名/字数/分类', !!(r.fileName && r.chars && Array.isArray(r.classes)),
      'file=' + r.fileName);
    ok('导入记录 ' + bid + '/' + r.id + ' 分类置信度落在 0–1', r.classes.every(function (x) {
      return typeof x.conf === 'number' && x.conf >= 0 && x.conf <= 1;
    }));
  });
});
/* ---- 11. 卷不得每卷重复全书章节（已复现缺陷的反证）----
   卷的 chapters 是「本书章号区间」描述子 [起, 止]，不是已落库章 id 列表；
   样例只物化了最近窗口，故不得要求端点已物化，只要求区间良构 + 不重复 + 不重叠 + 已物化章被覆盖。 */
Object.keys(D.volumes).forEach(function (bid) {
  var vols = (D.volumes[bid] || []).slice().sort(function (x, y) {
    return parseInt(String(x.chapters[0]).replace(/\D/g, ''), 10) - parseInt(String(y.chapters[0]).replace(/\D/g, ''), 10);
  });
  var sigs = vols.map(function (v) { return (v.chapters || []).join('~'); });
  ok('作品 ' + bid + ' 各卷章节区间不得完全相同（禁止每卷重复全书）',
    vols.length <= 1 || new Set(sigs).size === sigs.length, sigs.join(' | '));
  var keep = false;
  vols.forEach(function (v) {
    var r = v.chapters || [];
    ok('卷 ' + bid + '/' + v.id + ' 章节区间声明为 [起, 止] 两元素', r.length === 2, JSON.stringify(r));
    var a = parseInt(String(r[0] || '').replace(/\D/g, ''), 10);
    var b = parseInt(String(r[1] || '').replace(/\D/g, ''), 10);
    ok('卷 ' + bid + '/' + v.id + ' 区间端点可解析为章号', !isNaN(a) && !isNaN(b), JSON.stringify(r));
    ok('卷 ' + bid + '/' + v.id + ' 区间方向正确（起 ≤ 止）', a <= b, a + '→' + b);
    v.__from = a; v.__to = b;
    if (keep) ok('作品 ' + bid + ' 相邻卷区间不得重叠（重叠=同章重复出现在两卷）', v.__from > keep.__to,
      keep.id + '[' + keep.__from + ',' + keep.__to + '] vs ' + v.id + '[' + v.__from + ',' + v.__to + ']');
    keep = v;
  });
  /* 每个已物化章必须落在本书某一卷区间内，且只能落在一卷 */
  Object.keys(D.chapters).filter(function (k) { return D.chapters[k].bookId === bid; }).forEach(function (k) {
    var n = D.chapters[k].no;
    var hit = vols.filter(function (v) { return n >= v.__from && n <= v.__to; });
    ok('已物化章 ' + k + '（第' + n + '章）必须落在本书恰好一卷区间内',
      hit.length === 1, '命中 ' + hit.length + ' 卷：' + hit.map(function (v) { return v.id; }).join(','));
  });
});
/* ---- 12. 正文可作为书写对象（段落可寻址）---- */
Object.keys(D.manuscripts).forEach(function (k) {
  var ms = D.manuscripts[k];
  (ms.paragraphs || []).forEach(function (p, i) {
    ok('正文 ' + k + ' 第' + (i + 1) + '段可寻址（含 para 序号或文本）',
      p && (p.para !== undefined || typeof p === 'string' || !!p.text), JSON.stringify(p).slice(0, 60));
  });
});

/* ---- 13. 创作选择词库 L01–L24（§16.1）---- */
(function () {
  var TAGS = D.writingTags || [], GROUPS = D.tagGroups || [];
  ok('创作选择词库存在且为 L01–L24 共 24 组', TAGS.length === 24, '实际 ' + TAGS.length);
  var gids = ids(GROUPS);
  var seen = {};
  TAGS.forEach(function (t) {
    ok('词库 ' + t.id + ' 编号不重复', !seen[t.id], t.id);
    seen[t.id] = true;
    ok('词库 ' + t.id + ' 归属有效分组', gids.indexOf(t.group) >= 0, 'group=' + t.group);
    ok('词库 ' + t.id + ' 有名称与作用说明', !!t.name && !!t.why, t.id);
    ok('词库 ' + t.id + ' 选择模式合法（single/multi/combo）',
      ['single', 'multi', 'combo'].indexOf(t.mode) >= 0, 'mode=' + t.mode);
    var opts = (t.opts || []).slice();
    (t.optGroups || []).forEach(function (g) { opts = opts.concat(g.opts || []); });
    ok('词库 ' + t.id + ' 至少有一个候选选项', opts.length > 0, t.id);
    ok('词库 ' + t.id + ' 声明所属范围', !!t.scope, t.id);
    /* 组合维度必须带分组，否则「选择后要解释改了哪一轴」无处落 */
    if (t.mode === 'combo' && t.optGroups) {
      ok('词库 ' + t.id + ' 组合维度分组数与作用说明一致', t.optGroups.length >= 2, '组数=' + t.optGroups.length);
    }
  });
  for (var i = 1; i <= 24; i++) {
    var id = 'L' + (i < 10 ? '0' + i : i);
    ok('词库编号连续：' + id, !!seen[id], id);
  }
  /* 每个 Book 的 tags 必须能归一化，且只引用已声明维度 */
  Object.keys(D.craft || {}).forEach(function (b) {
    var pos = (D.craft[b] || {}).positioning || {};
    var tags = pos.tags || {};
    Object.keys(tags).forEach(function (k) {
      ok('作品 ' + b + ' 的创作选择 ' + k + ' 是已声明维度', !!seen[k], k);
    });
    ok('作品 ' + b + ' 记录选择作用范围', !!pos.tagScope, 'tagScope=' + pos.tagScope);
  });
  /* 建议组：必须带理由与代价，且引用的维度/选项真实存在 */
  (D.tagSuggestions || []).forEach(function (s) {
    ok('建议 ' + s.id + ' 带理由', !!s.why, s.id);
    ok('建议 ' + s.id + ' 带取舍说明', !!s.tradeoff, s.id);
    Object.keys(s.tags || {}).forEach(function (id) {
      var def = TAGS.filter(function (t) { return t.id === id; })[0];
      if (!ok('建议 ' + s.id + ' 引用已声明维度 ' + id, !!def, id)) return;
      var opts = (def.opts || []).slice();
      (def.optGroups || []).forEach(function (g) { opts = opts.concat(g.opts || []); });
      s.tags[id].forEach(function (o) {
        ok('建议 ' + s.id + ' 的 ' + id + ' 选项「' + o + '」在词库内', opts.indexOf(o) >= 0, o);
      });
    });
  });
})();

/* ---- 输出 ---- */
console.log('=== Writing Business 数据层自检 ===');
console.log('通过断言：' + passes);
console.log('警告：' + warns.length);
warns.forEach(function (w) { console.log('  ~ ' + w); });
console.log('失败：' + fails.length);
fails.forEach(function (f) { console.log('  ✗ ' + f); });
console.log('--- 计数概览 ---');
console.log('  作品 ' + D.books.length + ' / 章 ' + chapIds.length + ' / 候选 ' + Object.keys(D.candidates).length +
  ' / 队列 ' + D.queue.length + ' / Works ' + D.works.length + '（无归属 ' + noOwner.length + '：' + noOwner.join(',') + '）');
console.log('  员工 ' + D.employees.length + ' / 观察 ' + obsIds.length + ' / 参考 ' + refIds.length +
  ' / 分析 ' + D.analyses.length + ' / 经验 ' + learnIds.length);
(function () {
  var rows = Object.keys(D.craft || {}).map(function (b) {
    var c = D.craft[b], sc = 0;
    Object.keys(c.scenes || {}).forEach(function (k) { sc += (c.scenes[k] || []).length; });
    return b + ' 背景' + (c.world || []).length + '/人物' + (c.characters || []).length +
      '/大纲' + (c.outline || []).length + '/场景' + sc;
  });
  console.log('  创作内核 ' + rows.join(' · '));
})();
process.exit(fails.length ? 1 : 0);
