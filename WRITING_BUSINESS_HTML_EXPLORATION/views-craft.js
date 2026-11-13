/* ============================================================================
   views-craft.js — Book 创作内核 + 审校与质量 + 旧稿接续
   依据：docs/research/writing-business-product-structure-2026-09-21
         §13 Book创作内核补充合同（Authority Class: RESEARCH / Status: Review）
   原则（硬约束）：
     · 创作对象一律绑定本书；缺本书资料 → 真实空状态 + 创建入口，绝不回退他作样例。
     · 计划（PLANNED）不是已发生事实；正式稿不是线上稿；候选 ≠ 作者决定。
     · 讨论 → 具体候选 → 作者确认 → 写入目标对象 → 下游可引用。
     · 审稿 / 校对 / 表达质量是三类不同工作，不可互相替代；无证据不自动改稿；
       不提供检测规避、不虚构「去AI率」。
     · 变更先列影响范围，不静默全书覆盖；旧版本与已发事实保留。
   ========================================================================== */
(function () {
  var ui = WB.ui;

  /* ================= 常量 ================= */
  var CRAFT_MODES = [
    ['positioning', '定位'], ['world', '世界'], ['characters', '人物'],
    ['arc', '主支线与结局'], ['outline', '大纲'], ['scenes', '场景准备']
  ];
  var REVIEW_KINDS = [['review', '审稿'], ['proof', '校对'], ['style', '表达质量']];
  var POS_FIELDS = [
    ['workingTitle', '书名 / 暂名', 'text'], ['readerPartition', '读者分区', 'text'],
    ['genres', '题材', 'list'], ['coreOriginal', '原创核心', 'text'],
    ['perspective', '叙事视角', 'text'], ['style', '风格', 'text'],
    ['lengthPlan', '篇幅意向', 'text'], ['platform', '目标平台', 'text'],
    ['taboos', '作者禁区', 'list'], ['readerPromise', '读者承诺', 'text']
  ];
  var FIELD_LABEL = {
    workingTitle: '书名 / 暂名', readerPartition: '读者分区', genres: '题材', coreOriginal: '原创核心',
    perspective: '叙事视角', style: '风格', lengthPlan: '篇幅意向', platform: '目标平台',
    taboos: '作者禁区', readerPromise: '读者承诺',
    kind: '类别', name: '名称', cond: '条件 / 表现', cost: '代价', limit: '限制', exception: '例外',
    state: '事实状态', source: '来源', role: '角色定位', goal: '目标', motivation: '动机',
    weakness: '弱点', abilityLimit: '能力限制', arc: '成长弧线', voice: '说话方式', first: '首次出现',
    status: '状态', title: '标题', purpose: '目的', events: '关键事件', emotion: '情绪推进',
    level: '层级', origin: '来源（作者 / AI）', version: '版本', premise: '故事前提',
    mainConflict: '主要冲突', climax: '高潮', text: '内容', cast: '出场人物', place: '地点',
    conflict: '冲突', reveal: '要揭示', notReveal: '不能揭示', endState: '结束状态', length: '长度意向',
    pov: '视角'
  };
  function label(k) { return FIELD_LABEL[k] || k; }

  /* ================= 读取助手 ================= */
  function curBook() {
    var p = WB.S.__route.params || {};
    var b = WB.book(p.bookId || WB.S.__scope.bookId) || WB.scopeBook();
    WB.S.__scope.bookId = b.id;
    return b;
  }
  function curCraft() { return WB.craftOf(curBook().id); }
  function bookChapters(bookId) {
    return Object.keys(WB.S.chapters).filter(function (k) { return WB.S.chapters[k].bookId === bookId; })
      .sort(function (x, y) { return WB.S.chapters[x].no - WB.S.chapters[y].no; });
  }
  function outlineChildren(c, parentId) { return c.outline.filter(function (n) { return n.parent === parentId; }); }
  function outlineOfLevel(c, lvl) { return c.outline.filter(function (n) { return n.level === lvl; }); }
  /* 大纲 ↔ 章节：只用显式声明关联（chapterKey 优先，其次显式 chapterNo）。
     绝不用标题正则猜章——改名、换号、中文标题都不会断开关联，也不会误连到别的章。 */
  function chapterForOutline(c, bookId, node) {
    if (!node) return null;
    var ks = bookChapters(bookId);
    if (node.chapterKey) {
      var hit = ks.filter(function (k) { return k === node.chapterKey; })[0];
      if (hit) return hit;
    }
    if (node.chapterNo != null && node.chapterNo !== '') {
      var hit2 = ks.filter(function (k) { return WB.S.chapters[k].no === Number(node.chapterNo); })[0];
      if (hit2) return hit2;
    }
    return null;
  }
  /* 旧数据（w1/w2）里靠标题正则隐式关联的章级节点：一次性固化为显式关联，之后不再猜 */
  function ensureOutlineLinks(b, c) {
    var fixed = 0;
    (c.outline || []).forEach(function (n) {
      if (n.level !== 'chapter' || n.chapterKey || (n.chapterNo != null && n.chapterNo !== '')) return;
      var m = /(\d+)\s*章/.exec(n.title || '');
      if (!m) return;
      var no = Number(m[1]);
      var hit = bookChapters(b.id).filter(function (k) { return WB.S.chapters[k].no === no; })[0];
      if (hit) { n.chapterKey = hit; n.chapterNo = no; n.linkMigrated = '由旧标题固化'; fixed++; }
    });
    if (fixed) WB.save();
    return fixed;
  }
  function byId(arr, id) { for (var i = 0; i < (arr || []).length; i++) if (arr[i].id === id) return arr[i]; return null; }
  function twoDigit(n) { var s = String(n); return s.length < 2 ? '0' + s : s; }

  /* 对象读取 / 写入（直接编辑用） */
  function objectOf(c, kind, id, extra) {
    if (kind === 'positioning') return c.positioning;
    if (kind === 'world') return byId(c.world, id);
    if (kind === 'character') return byId(c.characters, id);
    if (kind === 'outline') return byId(c.outline, id);
    if (kind === 'arc') return c.arc;
    if (kind === 'ending') return byId(c.arc.endings, id);
    if (kind === 'scene') return byId((c.scenes[(extra && extra.chapter)] || []), id);
    if (kind === 'manuscript') return { paragraphs: (WB.S.manuscripts[id] || {}).paragraphs || [] };
    return null;
  }
  function readField(c, kind, id, field, extra) {
    var o = objectOf(c, kind, id, extra);
    return o ? o[field] : null;
  }
  function writeField(c, kind, id, field, value, extra) {
    if (kind === 'positioning') {
      c.positioning[field] = value;
      if (!c.positioning.fields) c.positioning.fields = {};
      c.positioning.fields[field] = 'confirmed';
      c.positioning.updatedAt = WB.now();
      syncPositioningToBook(c.bookId, field);
      return true;
    }
    if (kind === 'manuscript') {
      var pi = Number(extra && extra.para) - 1;
      var ms = WB.msOf(id);
      if (!ms || ms.paragraphs[pi] == null) return false;
      ms.paragraphs[pi] = value;
      ms.updatedAt = WB.now();
      pushDraftVersion(ms, '直接写入（第 ' + (pi + 1) + ' 段）');
      return true;
    }
    var o = objectOf(c, kind, id, extra);
    if (!o) return false;
    o[field] = value;
    return true;
  }
  function readFieldRaw(c, kind, id, field, extra) {
    var o = objectOf(c, kind, id, extra);
    return o ? o[field] : undefined;
  }
  function asList(v) { return Array.isArray(v) ? v : (v == null || v === '' ? [] : String(v).split(/\s*[、,]\s*/).filter(Boolean)); }

  /* ================================================================================
     讨论引擎（作者要求 → 员工接管范围 → 具体回复 + 可编辑提案 → 逐项裁定 → 落到对象）
     硬约束：
       · 一切素材取自「当前这本书」的创作内核；本书没有素材就如实说，绝不借用他书
         （例如把《夜行灯》的记忆代价 / 人物名搬到新书里）。
       · 支持的动作都是真变换（删减、删修饰词、修标点、把书内已有对象接上），
         不是给一段预写文本让作者「假装在讨论」。
       · 不支持的意图显式返回「演示未模拟」，并保留作者原话。
       · 采纳只写到该对象（正文落到草稿 / 创作对象落到本字段）；正式稿与线上稿不动。
     ================================================================================ */

  /* 目标寻址：'chapter:B-01:ch43' / 'para:B-01:ch43:3' / 'scene:B-01:ch44:SC-44-1'
                'char:B-01:CH-01' / 'world:B-01:WD-01' / 'outline:B-01:O-C44'
                'pos:B-01:coreOriginal' / 'book:B-01' / 'cand:B-01:C-43' */
  function parseObj(s) {
    var str = String(s || '');
    var p = str.split(':');
    var S2 = WB.S;
    if (p.length >= 2) {
      var bid = p[1];
      if (p[0] === 'book') return { kind: 'book', bookId: bid };
      if (p[0] === 'chapter') return { kind: 'chapter', bookId: bid, ck: p[2] };
      if (p[0] === 'para') return { kind: 'para', bookId: bid, ck: p[2], para: Number(p[3]) };
      if (p[0] === 'scene') return { kind: 'scene', bookId: bid, ck: p[2], id: p[3], field: p[4] || 'purpose' };
      if (p[0] === 'char') return { kind: 'char', bookId: bid, id: p[2], field: p[3] || 'arc' };
      if (p[0] === 'world') return { kind: 'world', bookId: bid, id: p[2], field: p[3] || 'cond' };
      if (p[0] === 'outline') return { kind: 'outline', bookId: bid, id: p[2], field: p[3] || 'purpose' };
      if (p[0] === 'pos') return { kind: 'pos', bookId: bid, field: p[2] || 'coreOriginal' };
      if (p[0] === 'cand') return { kind: 'cand', bookId: bid, id: p[2] };
    }
    /* 兼容早期写法 */
    if (S2.chapters[str]) return { kind: 'chapter', bookId: S2.chapters[str].bookId, ck: str };
    var mh = /^([^#]+)#p(\d+)$/.exec(str);
    if (mh && S2.chapters[mh[1]]) return { kind: 'para', bookId: S2.chapters[mh[1]].bookId, ck: mh[1], para: Number(mh[2]) };
    if (WB.book(str)) return { kind: 'book', bookId: str };
    return null;
  }
  /* 本书自有素材（唯一来源；没有就为空）
     seed = 作者在起步区/讨论里写下的原话，是本书最早的素材，不是他作内容。 */
  function ownMaterial(c) {
    var chars = (c.characters || []).map(function (x) { return x.name; });
    var worlds = (c.world || []).map(function (x) { return x.name; });
    var nodes = c.outline || [];
    var planNode = nodes.filter(function (n) { return n.level === 'book'; })[0] || null;
    var pos = c.positioning || {};
    return { chars: chars, worlds: worlds, premise: (c.arc && c.arc.premise) || null,
      seed: pos.seed || null, dirId: pos.dirId || null,
      plan: (planNode && planNode.purpose) || null };
  }
  function targetLabelOfKind(t) {
    var S2 = WB.S;
    if (!t) return '当前工作面';
    if (t.kind === 'chapter') { var ch = S2.chapters[t.ck] || {}; return '第 ' + (ch.no || '?') + ' 章《' + (ch.title || '') + '》正文（草稿）'; }
    if (t.kind === 'para') { var ch2 = S2.chapters[t.ck] || {}; return '第 ' + (ch2.no || '?') + ' 章第 ' + t.para + ' 段（草稿）'; }
    if (t.kind === 'scene') return '场景 ' + t.id + ' · ' + label('purpose');
    if (t.kind === 'char') { var c = WB.craftOf(t.bookId), x = byId(c.characters, t.id); return '人物 ' + (x ? x.name : t.id); }
    if (t.kind === 'world') { var c2 = WB.craftOf(t.bookId), w = byId(c2.world, t.id); return '世界 · ' + (w ? w.name : t.id); }
    if (t.kind === 'outline') { var c3 = WB.craftOf(t.bookId), n = byId(c3.outline, t.id); return '大纲 · ' + (n ? n.title : t.id); }
    if (t.kind === 'pos') return '本书定位 · ' + label(t.field);
    if (t.kind === 'book') { var b = WB.book(t.bookId); return '作品 ' + (b ? b.title : t.bookId); }
    if (t.kind === 'cand') return '候选 ' + t.id;
    return t.kind;
  }
  function readTarget(t) {
    var S2 = WB.S, c = WB.craftOf(t.bookId);
    if (t.kind === 'para') { var ms = WB.msOf(t.ck); return ms && ms.paragraphs[t.para - 1] != null ? ms.paragraphs[t.para - 1] : null; }
    if (t.kind === 'chapter') { var ms2 = WB.msOf(t.ck); return ms2 ? ms2.paragraphs.join('\n') : null; }
    if (t.kind === 'scene') { var s = byId((c.scenes[t.ck] || []), t.id); return s ? s[t.field] : null; }
    if (t.kind === 'char') { var x = byId(c.characters, t.id); return x ? x[t.field] : null; }
    if (t.kind === 'world') { var w = byId(c.world, t.id); return w ? w[t.field] : null; }
    if (t.kind === 'outline') { var n = byId(c.outline, t.id); return n ? n[t.field] : null; }
    if (t.kind === 'pos') return c.positioning[t.field];
    if (t.kind === 'book') { var b = WB.book(t.bookId); return b ? (b.positioning || null) : null; }
    return null;
  }
  function pushDraftVersion(ms, note) {
    var n = ms.versions.filter(function (x) { return x.kind === 'draft'; }).length + 1;
    ms.versions.push({ v: '草稿 r' + n, at: WB.now(), kind: 'draft', note: note, paragraphs: ms.paragraphs.slice() });
  }
  /* 讨论期间对象当前状态（显示在对话顶部：对象 / 版本 / 状态相邻） */
  WB.discussContext = function (objStr) {
    var t = parseObj(objStr);
    if (!t) return { owns: '当前工作面', state: '—' };
    var S2 = WB.S, b = WB.book(t.bookId), owns = '本书创作内核与正文';
    var state = '—';
    if (t.kind === 'chapter' || t.kind === 'para') {
      var ch = S2.chapters[t.ck] || {}, ms = WB.msOf(t.ck);
      owns = '第 ' + ch.no + ' 章《' + ch.title + '》的正文与候选';
      state = '草稿 ' + ((ms && ms.paragraphs.length) || 0) + ' 段 · 正式 ' +
        ((ms && ms.formalVersion) || '无') + ' · 线上 ' + (ch.published || '未发布');
    } else if (t.kind === 'scene') {
      owns = '本章场景计划（目的 / 视角 / 出场人物 / 引用资料 / 结束状态）';
      state = '场景 ' + t.id;
    } else if (t.kind === 'char') {
      owns = '本书人物档案与认知域'; state = '人物 ' + t.id;
    } else if (t.kind === 'world') {
      owns = '本书背景与世界规则'; state = '条目 ' + t.id;
    } else if (t.kind === 'outline') {
      owns = '本书多级大纲与章节关联'; state = '节点 ' + t.id;
    } else if (t.kind === 'pos') {
      owns = '本书定位与作品摘要'; state = '字段 ' + label(t.field);
    } else if (t.kind === 'book') {
      owns = '本书规划、定位与整体目标'; state = (b ? b.status : '—');
    } else if (t.kind === 'cand') {
      owns = '本章候选的逐项裁决与理由'; state = '候选 ' + t.id;
    }
    return { owns: owns, state: state, preview:readTarget(t) };
  };

  /* 真变换：删减 / 删修饰词 / 修标点 */
  var WEAK_WORDS = ['轻轻地', '其实', '非常', '十分', '似乎', '仿佛', '有点', '一些', '大概', '或许'];
  function shortenOnce(text) {
    var t = String(text == null ? '' : text).trim();
    if (!t || t.length < 10) return null;
    var parts = t.split('，');
    if (parts.length >= 2) {
      var cut = parts.slice(0, parts.length - 1).join('，').replace(/[，、；：]$/, '');
      if (cut.length >= 8) return cut + '。';
    }
    if (t.length > 18) {
      var keep = Math.max(10, Math.floor(t.length * 0.62));
      return t.slice(0, keep).replace(/[，、；：]$/, '') + '。';
    }
    return null;
  }
  function dedupeOnce(text) {
    var t = String(text == null ? '' : text);
    for (var i = 0; i < WEAK_WORDS.length; i++) {
      if (t.indexOf(WEAK_WORDS[i]) >= 0) return t.split(WEAK_WORDS[i]).join('');
    }
    if (t.indexOf('，，') >= 0) return t.split('，，').join('，');
    if (/[\u4e00-\u9fa5][,;:!?]/.test(t)) {
      return t.replace(/([\u4e00-\u9fa5])([,;:!?])/g, function (mm, a, b) {
        return a + ({ ',': '，', ';': '；', ':': '：', '!': '！', '?': '？' }[b] || b);
      });
    }
    return null;
  }
  /* 正文选区改写：只做确定性改写（去重复修饰 / 压缩句子），绝不跨作品注入人物、不虚构情节。
     返回 null 表示这一轮没有可执行的确定性改写 —— 调用方必须如实说明「演示未模拟」。 */
  WB.selRewriteOf = function (text) {
    var t = String(text == null ? '' : text).trim();
    if (!t) return null;
    var d = dedupeOnce(t);
    if (d && d !== t) return { after: d, why: '去掉重复修饰与重复标点（确定性改写）' };
    var s = shortenOnce(t);
    if (s && s !== t) return { after: s, why: '压缩句子长度（确定性改写）' };
    return null;
  };
  /* 从作者的一段话里分离「构思」与「指令」。
     作者常把要求写在构思后面（例：……请先与我讨论两种方向，不要写正文）。
     构思按原话保留（作者原话就是本书最早的素材）；指令只用来判意图，不进故事前提。 */
  function seedExtract(req) {
    var raw = String(req == null ? '' : req).trim();
    if (!raw) return null;
    var parts = raw.split(/[。；\n]/).map(function (s) { return s.trim(); }).filter(Boolean);
    var keep = parts.filter(function (s) {
      if (/^(请|麻烦|帮我|帮我先|我要你|你先|先帮我|先|不要|别|不用)/.test(s)) return false;
      if (/讨论|方向|不要写正文|不用写正文|先给|给几[个种]|两种|几个方向|草稿/.test(s)) return false;
      return true;
    });
    var use = keep.length ? keep : parts;
    var premise = use.join('。').replace(/^我(想|要|准备|打算|计划)/, '').trim();
    if (premise && !/[。！？?]$/.test(premise)) premise += '。';
    return { raw: raw, premise: premise || raw };
  }
  /* 方向候选匹配：按作者原话里的关键词给分，取最贴的 2–3 条。
     一条都匹配不上时给出候选全集并如实说明——绝不返回空、也不硬凑。 */
  function matchDirections(text, limit) {
    var dirs = WB.startDirections ? WB.startDirections() : [];
    if (!dirs.length) return [];
    var s = String(text || '');
    var scored = dirs.map(function (d) {
      var hit = 0;
      (d.keys || []).forEach(function (k) { if (k && s.indexOf(k) >= 0) hit++; });
      return { d: d, hit: hit };
    });
    var top = scored.filter(function (x) { return x.hit > 0; });
    if (!top.length) return dirs.slice(0, limit || 2);
    return top.slice(0, limit || 2).map(function (x) { return x.d; });
  }
  /* 意图判定：只认能真做的动作，其余一律「未模拟」 */
  function classifyIntent(req) {
    var r = String(req || '');
    if (/再短|更短|短一点|短些|精简|压缩|删掉|去掉|缩减/.test(r)) return 'shorten';
    if (/重复|啰嗦|赘|冗|修饰词|旁白|解释性|标点|全角|半角/.test(r)) return 'dedupe';
    if (/更长|展开|扩写|加细节|补一|补上|详细|丰富/.test(r)) return 'expand';
    if (/出场人物|人物漏|cast|谁出场/.test(r)) return 'cast';
    if (/引用|依据|资料|设定引用|世界/.test(r)) return 'ref';
    if (/为什么|依据是什么|依据|解释一下|说明一下|怎么判断/.test(r)) return 'explain';
    /* 方向讨论放在最后：具体改写意图优先，只有都不匹配时才按「谈方向」处理。
       且只在书级 / 定位级对象上成立（见 discussEngine），段落上的「方向」字样仍按未模拟。 */
    if (/方向|构思|想法|创意|写什么|写一部|我想写|题材|讲什么|故事怎么/.test(r)) return 'direction';
    return null;
  }
  function nextPropId() { return 'DP-' + (Object.keys(WB.S.discussProps || {}).length + 1); }

  /* 提案项必须显式带 applied：null = 未裁定 / true = 已采纳 / false = 已拒绝。
     漏写该字段会让该项在 UI 里被当成「已裁定」——按钮不出现、余项采纳跳过它，
     作者看到「本轮已全部裁定」却什么都没写进本书（第 5 轮真实缺陷）。
     所有提案注册统一走这里兜底，不依赖每个分支自己记得写。 */
  function normItems(items) {
    return (items || []).map(function (it) {
      if (it && it.applied === undefined) it.applied = null;
      return it;
    });
  }

  WB.discussEngine = function (empId, objStr, req, opts) {
    opts = opts || {};
    var t = parseObj(objStr);
    if (!t) return { supported: false, took: '', reply: '这条对话没有绑定具体对象，我无法确定要改哪里。',
      next: '请从具体对象（正文段落 / 场景 / 人物 / 定位字段）发起讨论。' };
    var b = WB.book(t.bookId);
    if (!b) return { supported: false, took: '', reply: '找不到这本书，无法接管范围。', next: '请先切换到这本书。' };
    var c = WB.craftOf(t.bookId);
    var own = ownMaterial(c);
    var ctx = WB.discussContext(objStr);
    var took = '已接管范围：' + ctx.owns + '（' + ctx.state + '）';
    var literal=String(req).match(/^(?:请)?(?:改为|改成)[：:\s]+([\s\S]+)$/);
    if(literal&&['pos','char','world','outline','scene','para'].indexOf(t.kind)>=0){
      var pid=nextPropId(),before=readTarget(t);WB.S.discussProps[pid]={id:pid,by:empId,round:1,target:t,targetLabel:targetLabelOfKind(t),basis:'作者给定文本的局部替换，待确认；非模型生成',items:[{id:'C1',label:label(t.field||'text'),before:before==null?'':String(before),after:literal[1],applied:null}]};
      return {supported:true,propId:pid,took:took,reply:'已整理为局部修改建议。确认后只写回这项，其他内容保持不变。'};
    }
    var intent = classifyIntent(req);
    /* 「方向」只在书级 / 定位级成立：段落与场景上的「方向」字样仍按未模拟处理，不冒充理解 */
    var bookLevel = (t.kind === 'book' || t.kind === 'pos');
    if (intent === 'direction' && !bookLevel) intent = null;

    /* 书级方向讨论：作者给一句构思 → 编辑接住，存下作者原话，并给出 2–3 条
       含具体故事内容 / 差异 / 取舍的方向候选。这是新书起步的真正入口，
       不再是「演示未模拟这类要求」。候选逐条采纳，采纳即写进本书前提与创作选择。 */
    if ((intent === 'direction' || opts.force === 'direction') && bookLevel) {
      var seed = seedExtract(req);
      if (!seed) return { supported: false, took: took,
        reply: '我还没读到你的构思——先写一句你想写的故事，我才能提方向。',
        next: '例如：一个档案员每天收到印着明天日期的报纸。' };
      var pos0 = c.positioning;
      /* 作者原话只记第一次写进本书的那句。后续追问（例如「这个方向能不能再给一条支线？」）
         同样会被判为「方向」意图，但不得把本书里已存的作者原话覆盖掉——原话是这本书最早的素材，
         要能被反复引用与回显。新要求本身照常进入讨论记录与提案。 */
      if (!pos0.seed) { pos0.seed = seed.premise; pos0.seedRaw = seed.raw; pos0.seedAt = WB.now(); pos0.seedBy = 'author'; }
      var o0 = WB.onbOf ? WB.onbOf(t.bookId) : null;
      if (o0) { o0.seed = pos0.seed; o0.updatedAt = WB.now(); }
      var cands = matchDirections(seed.premise + ' ' + seed.raw, 2);
      if (!cands.length) return { supported: false, took: took,
        reply: '我接住了你的构思（已存进本书）。但演示里没有可对照的方向模板，我不替你现编方向。',
        next: '可以自己写一句故事前提，或先在「调整创作方向」里手动记录。' };
      var pidD = nextPropId();
      WB.S.discussProps[pidD] = { id: pidD, at: WB.now(), by: empId, round: 1, kind: 'dir',
        target: t, targetLabel: '本书构思方向 · ' + b.title,
        basis: '只依据你写下的构思（你的原话，已存进本书）与本书已记录的选择；不引入其他作品的人物或设定。',
        items: normItems(cands.map(function (d, i) {
          return { id: 'D' + (i + 1), kind: 'dir', dirId: d.id, dir: d,
            label: '方向 ' + (i + 1) + '：' + d.name,
            before: '', after: d.premise, applied: null, op: 'dirAdopt', value: d.id };
        })) };
      return { supported: true, took: took, propId: pidD,
        reply: '我接住了你的构思，已经把它存进本书（作为你自己的原话，不是我改写的版本）。' +
          '按它我挑了 ' + cands.length + ' 条方向，每条都写了具体的故事前提、主要冲突、叙事视角、为什么贴你的构思，以及代价。' +
          '你可以逐条「改后再采纳」，可以选一条，也可以都不用——选完之后我再帮你补这本书真正要用的少量设定，然后直接准备第一章。',
        next: '采用一个方向后，故事前提与创作选择会写进本书；接着可以让编辑补一条背景规则或一个人物动机，再准备第一章候选。' };
    }

    /* 起步 · 补必要设定（正文编辑入口显式发起，不看关键词猜意图）：
       只补这一章真的会用到的少量对象 —— 一条背景规则、一个人物、一条主线。
       全部落进本书自己的创作内核；状态是「仅计划」，要到正文里成为事实仍须作者写。 */
    if (opts.force === 'base' && bookLevel) {
      var ownB = ownMaterial(c);
      var baseTxt = ownB.premise || ownB.seed;
      if (!baseTxt) return { supported: false, took: took,
        reply: '本书还没有故事前提：这时候补设定就是凭空编，我不做。先写一句构思，或采用一个方向。',
        next: '在起步区写一句构思，或先采用一个方向候选。' };
      var dirB = (WB.startDirections() || []).filter(function (x) { return x.id === c.positioning.dirId; })[0] || null;
      var ruleName = dirB ? dirB.name.split('·')[1].trim() + '的规则' : '核心规则';
      var heroName = '主角';
      var itemsB = [
        { id: 'B1', kind: 'obj', op: 'objAdd', addKind: 'world', value: ruleName, data: {
            name: ruleName, kind: '规则',
            cond: dirB ? dirB.premise : String(baseTxt).slice(0, 60),
            cost: dirB ? dirB.conflict : '（待你写：行使这条规则的代价）',
            limit: '（待你写：一次能用到什么程度）', exception: '（待你写：什么条件下不成立）' },
          label: '背景规则 · ' + ruleName,
          before: '本书世界条目：' + ((c.world || []).length) + ' 条',
          after: '新增 1 条规则（含条件 / 代价 / 限制），状态「仅计划」。条件取自你采用的' + (dirB ? '方向 ' + dirB.name : '构思'),
          applied: null, source: '编辑按本书构思起草（候选已采纳，仍属计划，未进正文）' },
        { id: 'B2', kind: 'obj', op: 'objAdd', addKind: 'character', value: heroName, data: {
            name: heroName, role: '主角（称谓待你改）',
            goal: dirB ? dirB.conflict : '（待你写：他这一章想拿到什么）',
            motivation: String(baseTxt).slice(0, 60),
            weakness: '（待你写：会让他在这一章吃亏的东西）', voice: '（待你写：他的说话方式）' },
          label: '人物 · ' + heroName,
          before: '本书人物：' + ((c.characters || []).length) + ' 个',
          after: '新增 1 个人物档案（目标 / 动机 / 弱点 / 声纹槽位），状态「仅计划」',
          applied: null, source: '编辑按本书构思起草（候选已采纳，仍属计划）' },
        { id: 'B3', kind: 'obj', op: 'objAdd', addKind: 'mainLine', value: '主线', data: {
            text: (dirB ? dirB.conflict : String(baseTxt).slice(0, 40)) },
          label: '主线 · 一条',
          before: '本书主支线：' + (((c.arc || {}).mainLines || []).length) + ' 条',
          after: '新增 1 条主线（只写一句，状态「仅计划」）',
          applied: null, source: '编辑按本书构思起草（候选已采纳，仍属计划）' }
      ];
      var pidB = nextPropId();
      WB.S.discussProps[pidB] = { id: pidB, at: WB.now(), by: empId, round: 1, kind: 'base',
        target: t, targetLabel: '本书要用的少量设定 · ' + b.title,
        basis: '只依据你写下的构思' + (dirB ? '与已采用的方向「' + dirB.name + '」' : '') + '；不引入其他作品的人物或设定。',
        items: normItems(itemsB) };
      return { supported: true, took: took, propId: pidB,
        reply: '按你的构思我列了 ' + itemsB.length + ' 项要用的设定：一条背景规则（含代价与限制）、一个人物档案、一条主线。' +
          '它们只落到本书创作内核，状态是「仅计划」——不是正文事实，也不会自动写进稿子。' +
          '（' + '人物名字与细节留了槽位给你改：我不替你定主角叫什么。）',
        next: '逐项采纳或拒绝；采纳后可以继续「定走向」或直接准备第一章候选。' };
    }

    /* 起步 · 定走向（正文编辑入口显式发起）：主支线两句 + 第 1 章段纲三点，
       全部落成创作内核里的计划对象。跳过也不算缺失。 */
    if (opts.force === 'plan' && bookLevel) {
      var ownP = ownMaterial(c);
      var planTxt = ownP.premise || ownP.seed;
      if (!planTxt) return { supported: false, took: took,
        reply: '本书还没有故事前提：这时候拆主支线就是凭空编。先写一句构思，或采用一个方向。',
        next: '在起步区写一句构思，或先采用一个方向候选。' };
      var dirP = (WB.startDirections() || []).filter(function (x) { return x.id === c.positioning.dirId; })[0] || null;
      var itemsP = [
        { id: 'P1', kind: 'obj', op: 'objAdd', addKind: 'mainLine', value: '主线', data: {
            text: dirP ? dirP.conflict : '主线冲突：' + String(planTxt).slice(0, 40) },
          label: '主线 · 一句', before: '本书主支线：' + (((c.arc || {}).mainLines || []).length) + ' 条',
          after: '新增 1 条主线（状态「仅计划」）', source: '编辑按本书构思与方向起草（候选已采纳，仍属计划）' },
        { id: 'P2', kind: 'obj', op: 'objAdd', addKind: 'subLine', value: '支线', data: {
            text: '支线：与主线直接相关的一段关系变化（待你补具体人物）' },
          label: '支线 · 一句', before: '本书支线：' + (((c.arc || {}).subLines || []).length) + ' 条',
          after: '新增 1 条支线（状态「仅计划」）', source: '编辑按本书构思与方向起草（候选已采纳，仍属计划）' },
        { id: 'P3', kind: 'obj', op: 'objAdd', addKind: 'outline', value: '第 1 章段纲', data: {
            title: '第 1 章 · 段纲', level: 'chapter', purpose: (dirP ? dirP.drivers.join(' / ') : '把读者放进故事前提'),
            events: '① 用一件具体的事把前提摆出来；② 让代价/冲突第一次显形；③ 章末留一个必须翻页的问题。' },
          label: '第 1 章段纲 · 三点', before: '本书大纲节点：' + ((c.outline || []).length) + ' 个',
          after: '新增 1 个章级大纲节点（必须延续 / 不能提前揭示 / 可以推进 三行），状态「仅计划」',
          applied: null, source: '编辑按本书构思与方向起草（候选已采纳，仍属计划）' }
      ];
      var pidP = nextPropId();
      WB.S.discussProps[pidP] = { id: pidP, at: WB.now(), by: empId, round: 1, kind: 'plan',
        target: t, targetLabel: '本书走向 · ' + b.title,
        basis: '只依据你写下的构思' + (dirP ? '与已采用的方向「' + dirP.name + '」' : '') + '；不引入其他作品的人物或设定。',
        items: normItems(itemsP) };
      return { supported: true, took: took, propId: pidP,
        reply: '我把走向拆成 ' + itemsP.length + ' 项：一条主线、一条支线、第 1 章段纲三点。' +
          '它们都是「仅计划」——计划不是已发生的事实，写进正文之后才算数。',
        next: '逐项采纳；也可以直接跳过规划去准备第一章候选——跳过不等于缺失。' };
    }

    /* 说明类：只解释，不动任何对象 */
    if (intent === 'explain') {
      var cur0 = readTarget(t);
      return { supported: true, took: took, propId: null,
        reply: '说明一下这个对象的现状与依据：' + (cur0 ? '当前值是「' + String(cur0).slice(0, 60) + '」。' : '当前还没有值。') +
          '依据来自本书的' + (own.chars.length ? '人物（' + own.chars.slice(0, 3).join('、') + '）' : '（本书还没有人物）') +
          (own.worlds.length ? '与世界条目（' + own.worlds.slice(0, 3).join('、') + '）' : '') +
          (own.plan ? '，以及全书计划：' + own.plan : '') + '。这一步不产生改动。',
        next: '如果确认要改，直接说改哪里（例如：把这一段再短一点）。' };
    }

    /* 场景结构化意图：把本书已有对象接上（这是真改动） */
    if (t.kind === 'scene' && (intent === 'cast' || intent === 'ref')) {
      var sc = byId((c.scenes[t.ck] || []), t.id);
      if (!sc) return { supported: false, took: took, reply: '找不到这个场景（可能已被删除）。', next: '回到场景准备重新发起。' };
      var items = [];
      if (intent === 'cast') {
        if (!own.chars.length) return { supported: false, took: took,
          reply: '本书还没有人物档案，我不能替你编人物名字——先在创作内核·人物里建角色，我才能把出场人物接上。',
          next: '去创作内核 · 人物新增角色。' };
        own.chars.forEach(function (nm) {
          if ((sc.cast || []).indexOf(nm) < 0) items.push({ id: 'I' + (items.length + 1), label: '出场人物补上 ' + nm,
            before: '出场人物：' + ((sc.cast || []).join('、') || '（空）'), after: ((sc.cast || []).concat([nm])).join('、'),
            applied: null, op: 'castAdd', value: nm });
        });
        if (!items.length) return { supported: true, took: took, propId: null,
          reply: '这个场景的出场人物已经覆盖了本书全部 ' + own.chars.length + ' 个角色，没有可补的。',
          next: '如果你想换人，请直接在场景编辑器里改。' };
      } else {
        if (!own.worlds.length && !(c.world || []).length) return { supported: false, took: took,
          reply: '本书还没有世界条目（规则 / 地点 / 势力），没有可引用的资料。', next: '先去创作内核 · 世界新增条目。' };
        (c.world || []).forEach(function (w) {
          if ((sc.refs || []).indexOf(w.id) < 0) items.push({ id: 'I' + (items.length + 1), label: '引用资料加上 ' + w.name + '（' + w.id + '）',
            before: '引用资料：' + ((sc.refs || []).join('、') || '（空）'), after: ((sc.refs || []).concat([w.id])).join('、'),
            applied: null, op: 'refAdd', value: w.id });
        });
        if (!items.length) return { supported: true, took: took, propId: null,
          reply: '这个场景已经引用了本书全部 ' + (c.world || []).length + ' 条世界资料。', next: '无需改动。' };
      }
      var pid = nextPropId();
      WB.S.discussProps[pid] = { id: pid, at: WB.now(), by: empId, round: (opts.continueOf ? 2 : 1),
        target: t, targetLabel: targetLabelOfKind(t),
        basis: '只使用本书已建立的' + (intent === 'cast' ? '人物' : '世界条目') + '；不新增他书内容。',
        items: normItems(items) };
      return { supported: true, took: took, propId: pid,
        reply: '我把这个场景的' + (intent === 'cast' ? '出场人物' : '引用资料') + '和本书已建的' +
          (intent === 'cast' ? own.chars.length + ' 个角色' : (c.world || []).length + ' 条世界条目') +
          '对了一遍，有 ' + items.length + ' 项可以接上。逐项决定就行。',
        next: '采纳后场景的写作依据会同步显示这些对象（同一条数据，不是复制）。' };
    }

    /* 文本类目标：删减 / 删修饰词 / 展开 */
    var cur = readTarget(t);
    if (t.kind === 'chapter') {
      /* 以章为范围时，落到该章第一段可寻址的段落（明确告知落到哪一段） */
      var msC = WB.msOf(t.ck);
      if (msC && msC.paragraphs.length) { t = { kind: 'para', bookId: t.bookId, ck: t.ck, para: 1 }; cur = msC.paragraphs[0]; }
    }
    if (t.kind !== 'book' && t.kind !== 'cand' && (cur == null || cur === '')) {
      return { supported: false, took: took, reply: '这个对象现在还没有内容（' + targetLabelOfKind(t) + ' 是空的）。',
        next: '先写一点内容，或直接手写——我没有素材时不会凭空编。' };
    }
    if (!intent) {
      return { supported: false, took: took,
        reply: '演示未模拟这类要求。本轮讨论只模拟能真做的动作：再短一点 / 删掉重复与修饰词 / 展开一版（标注需你改写）/ 补出场人物 / 补引用资料 / 让它解释依据。你的原话已保留。',
        next: '换一个上面列出的说法，或直接在对象里手改。' };
    }
    if (t.kind === 'book' || t.kind === 'cand') {
      return { supported: false, took: took, reply: '这个入口是给人看整体状态的；要改具体内容，请从正文段落或创作对象发起讨论。',
        next: '从具体对象（段落 / 场景 / 人物 / 定位字段）发起。' };
    }

    var after = null, why = '', op = 'text', value = null;
    if (intent === 'shorten') { after = shortenOnce(cur); why = '删掉最后一个分句 / 压缩冗余表述，保留主干。'; }
    else if (intent === 'dedupe') { after = dedupeOnce(cur); why = '删掉空泛修饰词并把标点统一为全角。'; }
    else if (intent === 'expand') {
      var planBit = own.plan ? '承接全书计划：' + own.plan : null;
      var castBit = own.chars.length ? '出场只用本书已建人物：' + own.chars.slice(0, 3).join('、') : null;
      var hint = [planBit, castBit].filter(Boolean).join('；');
      if (!hint) return { supported: false, took: took,
        reply: '本书还没有人物或全书计划，我没有可依据的东西来展开——不替你编情节。',
        next: '先建人物或写一句全书计划，再来展开。' };
      after = String(cur) + '\n【编辑起草（演示，需你改写）：' + hint + '。】';
      why = '按本书自有计划与人物给一版展开草案，明确标注为演示，需作者改写为正文语言。';
    }
    if (!after || after === cur) {
      return { supported: false, took: took,
        reply: '按这个要求改不出实质差别（原文已经很短或没有可删的重复项）。返回未改动，不会给你一个假的改动。',
        next: '换一种要求（例如指定要删的句子），或直接在正文里手改。' };
    }
    var pid2 = nextPropId();
    var items2 = [{ id: 'I1', label: label(t.field || (t.kind === 'para' ? 'text' : 'purpose')) + ' · ' + targetLabelOfKind(t),
      before: String(cur), after: after, applied: null, op: op, value: value }];
    if (opts.continueOf && WB.S.discussProps[opts.continueOf]) {
      var prev = WB.S.discussProps[opts.continueOf];
      var decided = prev.items.filter(function (x) { return x.applied != null; });
      /* 已裁定的部分不再重复改动：新提案只覆盖未裁定范围 */
      var openItems = prev.items.filter(function (x) { return x.applied == null; });
      if (openItems.length) {
        items2 = openItems.map(function (x, i) {
          return { id: 'C' + (i + 1), label: x.label, before: x.before,
            after: (intent === 'shorten' ? shortenOnce(x.after) : (intent === 'dedupe' ? dedupeOnce(x.after) : x.after)) || x.after,
            applied: null, op: x.op, value: x.value };
        });
      } else {
        items2 = [{ id: 'C1', label: label(t.field || 'text') + ' · ' + targetLabelOfKind(t), before: String(cur),
          after: after, applied: null, op: op, value: value }];
      }
      WB.S.discussProps[pid2] = { id: pid2, at: WB.now(), by: empId, round: prev.round + 1,
        target: t, targetLabel: targetLabelOfKind(t),
        basis: why + '；已裁定的 ' + decided.length + ' 项不再重复改动。', items: normItems(items2) };
      var same = items2.every(function (x) { return x.after === x.before; });
      if (same) {
        delete WB.S.discussProps[pid2];
        return { supported: false, took: took,
          reply: '剩下的 ' + items2.length + ' 项按这个要求已经改不出实质差别了——不会返回假改动。',
          next: '换一个要求，或直接手改。' };
      }
      return { supported: true, took: took, propId: pid2,
        reply: '第 ' + (prev.round + 1) + ' 轮：只动剩下未裁定的 ' + items2.length + ' 项，已裁定的 ' + decided.length + ' 项保持不动。',
        next: '逐项决定；都定了就到正文里确认正式稿（确认 ≠ 发布）。' };
    }
    WB.S.discussProps[pid2] = { id: pid2, at: WB.now(), by: empId, round: 1, target: t,
      targetLabel: targetLabelOfKind(t), basis: why, items: normItems(items2) };
    return { supported: true, took: took, propId: pid2,
      reply: '按你的要求改了 ' + targetLabelOfKind(t) + '。这是具体提案，你可以逐项采纳、拒绝，或改完再采纳。',
      next: '采纳只写到这里（正文写进草稿）；正式稿与线上稿要另行确认。' };
  };

  /* 把提案落到显式对象。返回 false = 未写入（调用方不得报成功） */
  WB.discussApply = function (p, it, overrideText) {
    var t = p.target;
    var c = WB.craftOf(t.bookId);
    /* 采纳方向：把作者选定的方向真正写进本书 —— 故事前提 / 主要冲突 / 视角 / 创作选择。
       标签只补空缺：作者已手选的维度不被静默替换（与「采用这组」同一条规则）。 */
    if (it.op === 'dirAdopt') {
      var dd = (WB.startDirections ? WB.startDirections() : []).filter(function (x) { return x.id === it.value; })[0];
      if (!dd) return false;
      if (!c.arc) c.arc = {};
      c.arc.premise = overrideText != null && String(overrideText).trim() ? String(overrideText).trim() : dd.premise;
      c.arc.mainConflict = dd.conflict;
      var dpos = c.positioning;
      if (!dpos.coreOriginal) dpos.coreOriginal = dd.premise;
      dpos.perspective = dd.viewpoint;
      dpos.dirId = dd.id; dpos.dirName = dd.name;
      if (dpos.fields) dpos.fields.perspective = 'confirmed';
      dpos.updatedAt = WB.now();
      var dtags = WB.tagsOf(c);
      Object.keys(dd.tags || {}).forEach(function (id) {
        var def = WB.tagDef(id); if (!def) return;
        var cur = dtags[id] || {};
        if (flattenSel(def, cur).length || cur.custom) return;   /* 保留作者自己的选择 */
        dtags[id] = { sel: dd.tags[id].slice(), note: '', req: autoReq(def, { sel: dd.tags[id].slice() }) };
      });
      syncPositioningFromTags(c);
      var oo = WB.onbOf ? WB.onbOf(t.bookId) : null;
      if (oo) { oo.dirId = dd.id; oo.updatedAt = WB.now(); }
      syncPositioningToBook(t.bookId);
      return true;
    }
    /* 补设定 / 补主支线 / 补章节段纲：都是往「本书自己的创作内核」里新增对象，
       不复制他作内容；状态一律 PLANNED（仅计划），要成为正文事实仍需作者写进正文。 */
    if (it.op === 'objAdd') {
      var ak = it.addKind, data = it.data || {};
      var src = it.source || '编辑按本书构思与方向起草（候选已采纳，仍属计划）';
      if (ak === 'world') {
        if (!Array.isArray(c.world)) c.world = [];
        if (c.world.some(function (w) { return w.name === data.name; })) return false;
        c.world.push({ id: 'WD-' + twoDigit(c.world.length + 1), kind: data.kind || '规则', name: data.name,
          cond: data.cond || '', cost: data.cost || '', limit: data.limit || '', exception: data.exception || '',
          state: 'PLANNED', source: src, evidence: null, refs: [] });
        return true;
      }
      if (ak === 'character') {
        if (!Array.isArray(c.characters)) c.characters = [];
        if (c.characters.some(function (x) { return x.name === data.name; })) return false;
        c.characters.push({ id: 'CH-' + twoDigit(c.characters.length + 1), name: data.name, role: data.role || '',
          goal: data.goal || '', motivation: data.motivation || '', weakness: data.weakness || '',
          voice: data.voice || '', arc: '', state: 'PLANNED', source: src, evidence: null });
        return true;
      }
      if (!c.arc) c.arc = {};
      if (ak === 'mainLine') {
        if (!Array.isArray(c.arc.mainLines)) c.arc.mainLines = [];
        if (c.arc.mainLines.some(function (l) { return l.text === data.text; })) return false;
        c.arc.mainLines.push({ id: 'ML-' + twoDigit(c.arc.mainLines.length + 1), text: data.text, from: null, state: 'PLANNED' });
        return true;
      }
      if (ak === 'subLine') {
        if (!Array.isArray(c.arc.subLines)) c.arc.subLines = [];
        if (c.arc.subLines.some(function (l) { return l.text === data.text; })) return false;
        c.arc.subLines.push({ id: 'SL-' + twoDigit(c.arc.subLines.length + 1), text: data.text, from: null, state: 'PLANNED' });
        return true;
      }
      if (ak === 'outline') {
        if (!Array.isArray(c.outline)) c.outline = [];
        if (c.outline.some(function (n) { return n.title === data.title; })) return false;
        var bk = c.outline.filter(function (n) { return n.level === 'book'; })[0];
        if (!bk) {
          bk = { id: 'O-B', level: 'book', parent: null, chapterKey: null, chapterNo: null, title: '全书总纲',
            purpose: '', events: '', emotion: '', origin: 'ai_draft', version: 'v1' };
          c.outline.unshift(bk);
        }
        c.outline.push({ id: 'O-' + (c.outline.length + 1), level: data.level || 'chapter', parent: data.parent || bk.id,
          chapterKey: data.chapterKey || null, chapterNo: data.chapterNo != null ? data.chapterNo : null,
          title: data.title, purpose: data.purpose || '', events: data.events || '', emotion: '',
          origin: 'ai_draft', version: 'v1' });
        return true;
      }
      return false;
    }
    if (it.op === 'castAdd') {
      var sc = byId((c.scenes[t.ck] || []), t.id);
      if (!sc) return false;
      if (!Array.isArray(sc.cast)) sc.cast = [];
      if (sc.cast.indexOf(it.value) >= 0) return false;
      sc.cast.push(it.value);
      return true;
    }
    if (it.op === 'refAdd') {
      var sc2 = byId((c.scenes[t.ck] || []), t.id);
      if (!sc2) return false;
      if (!Array.isArray(sc2.refs)) sc2.refs = [];
      if (sc2.refs.indexOf(it.value) >= 0) return false;
      sc2.refs.push(it.value);
      return true;
    }
    var current=readTarget(t);
    if(['para','scene','char','world','outline','pos'].indexOf(t.kind)>=0 && String(current==null?'':current)!==String(it.before==null?'':it.before)){
      WB.toast('这项内容在讨论后已有修改，未覆盖。请基于最新内容重新讨论。','warn');return false;
    }
    c.discussionHistory=c.discussionHistory||[];
    c.discussionHistory.push({at:WB.now(),target:WB.clone(t),before:current,after:overrideText!=null?overrideText:it.after,proposal:p.id});
    var v = overrideText != null ? overrideText : it.after;
    if (t.kind === 'para') {
      var ms = WB.msOf(t.ck);
      var i = t.para - 1;
      if (!ms || i < 0 || i >= ms.paragraphs.length) return false;
      ms.paragraphs[i] = v;
      ms.updatedAt = WB.now();
      pushDraftVersion(ms, '讨论采纳（第 ' + t.para + ' 段）：' + (p.basis || '').slice(0, 40));
      return true;
    }
    if (t.kind === 'scene') { var s = byId((c.scenes[t.ck] || []), t.id); if (!s) return false; s[t.field] = v; return true; }
    if (t.kind === 'char') { var x = byId(c.characters, t.id); if (!x) return false; x[t.field] = v; return true; }
    if (t.kind === 'world') { var w = byId(c.world, t.id); if (!w) return false; w[t.field] = v; return true; }
    if (t.kind === 'outline') { var n = byId(c.outline, t.id); if (!n) return false; n[t.field] = v; return true; }
    if (t.kind === 'pos') { c.positioning[t.field] = v; c.positioning.updatedAt = WB.now(); syncPositioningToBook(t.bookId, t.field); return true; }
    return false;
  };

  /* 定位 → 作品（书名 / 摘要）同步：同一事实只有一个来源，作品库读的是它（R7） */
  function syncPositioningToBook(bookId, field) {
    var b = WB.book(bookId), c = WB.craftOf(bookId);
    if (!b) return;
    var pos = c.positioning;
    if (!field || field === 'workingTitle') {
      var wt = pos.workingTitle;
      if (wt && String(wt).trim()) b.title = String(wt).trim();
    }
    if (!field || field === 'coreOriginal') {
      if (pos.coreOriginal) b.positioning = pos.coreOriginal;
    }
    b.summary = pos.coreOriginal || b.positioning || null;
  }
  WB.syncPositioningToBook = syncPositioningToBook;

  /* ================= 候选（Discussion → Candidate → 确认写入） ================= */
  function openProposals(bookId, kind, targetId) {
    return (WB.S.craftProposals || []).filter(function (p) {
      return p.bookId === bookId && p.state === 'open' && (!kind || p.kind === kind) &&
        (!targetId || p.targetId === targetId);
    });
  }
  function newProposalId() { return 'CP-' + ((WB.S.craftProposals || []).length + 1); }
  function addProposal(bookId, kind, targetId, field, before, after, rationale, extra) {
    var p = { id: newProposalId(), bookId: bookId, kind: kind, targetId: targetId, field: field,
      fieldLabel: label(field), before: before, after: after, rationale: rationale, at: WB.now(),
      state: 'open', by: 'E-01' };
    if (extra) for (var k in extra) if (Object.prototype.hasOwnProperty.call(extra, k)) p[k] = extra[k];
    WB.S.craftProposals.push(p);
    return p;
  }
  function proposalCard(p) {
    return '<div class="note choice" style="margin-top:8px">' +
      '<b>候选 ' + WB.esc(p.id) + ' · ' + WB.esc(p.fieldLabel || label(p.field)) + '</b> ' + WB.stBadge('待作者确认', 'choice') +
      '<div class="sm t3" style="margin-top:4px">应用于：' + WB.esc(p.targetLabel || p.targetId) + '</div>' +
      '<div class="diff-txt" style="margin-top:6px">' +
      (p.before ? '<div class="before">' + WB.esc(p.before) + '</div><div class="mid"></div>' : '') +
      '<div class="after">' + WB.esc(p.after) + '</div></div>' +
      '<div class="sm t3" style="margin-top:4px">依据：' + WB.esc(p.rationale) + '</div>' +
      '<div class="btnrow" style="margin-top:6px">' +
      '<button class="btn sm primary" data-action="act.c" data-fn="craftApplyProposal" data-a1="' + p.id + '">确认应用</button>' +
      '<button class="btn sm" data-action="act.c" data-fn="craftDropProposal" data-a1="' + p.id + '">放弃</button>' +
      '<button class="btn sm ghost" data-action="act.c" data-fn="craftEditProposal" data-a1="' + p.id + '">编辑候选</button>' +
      '<button class="btn sm ghost" data-action="act.c" data-fn="craftDiscussProposal" data-a1="' + p.id + '">与编辑讨论</button>' +
      '</div></div>';
  }

  /* 起草器（非讨论）：只使用本书自有素材生成具体草案。
     本书没有可用素材时明确返回 empty=true，由调用方显示「演示未模拟」——
     绝不把另一本书的人物 / 设定搬过来（反例：《夜行灯》的记忆代价不得出现在新书里）。 */
  function mockGenerate(c, kind, id, field) {
    var cur = readField(c, kind, id, field);
    var curS = cur == null ? '' : (Array.isArray(cur) ? cur.join('、') : String(cur));
    var own = ownMaterial(c);
    var empty = { after: curS, why: '本书还没有可用素材：演示不替你编他书内容。先在本书建立人物 / 背景 / 主支线，或直接手写。', empty: true };
    var who = own.chars[0] || null;

    if (kind === 'positioning') {
      if (field === 'coreOriginal') {
        if (own.premise) return { after: '核心：' + own.premise, why: '按本书已有的故事前提收敛成一句「原创核心」，不引入本书没有的设定。' };
        /* 新书没有 arc.premise，但作者已经写下了构思：用作者自己的原话收敛，不编内容 */
        if (own.seed) return { after: '核心：' + own.seed,
          why: '按你写下的构思（你的原话）收敛成一句「原创核心」——这是你自己给出的素材，不是替他作内容。' +
            '若要更具体（主要冲突、视角、基调），先采用一个方向候选，方向会一并写进本书前提。' };
        /* 作者只做了创作选择、还没写一句话故事：把作者已选的方向拼成一句，
           并明确标出还缺人物与代价 —— 仍然只用作者自己选的东西，不掺他作内容。 */
        var pickOf = function (id) { var def = WB.tagDef(id); return def ? flattenSel(def, WB.tagsOf(c)[id] || {}) : []; };
        var g3 = pickOf('L03'), g10 = pickOf('L10'), g7 = pickOf('L07'), g15 = pickOf('L15');
        if (g3.length || g10.length || g7.length) {
          var bits = [];
          if (g3.length) bits.push('题材：' + g3.join('、'));
          if (g10.length) bits.push('主题：' + g10.join('、'));
          if (g7.length) bits.push('驱动力：' + g7.join('、'));
          if (g15.length) bits.push('基调：' + g15.join('、'));
          return { after: '核心（按你已选的方向拼出，还缺一句人物与代价）：' + bits.join('；') + '。',
            why: '你已经在本书里选了这些创作方向，编辑把它们收敛成一句「原创核心」；' +
              '主角是谁、要付出什么代价，仍要你来写——这两项不能由编辑替你决定。' };
        }
        return empty;
      }
      if (field === 'readerPromise') {
        if (!own.plan) return empty;
        return { after: '每 2–3 章兑现一次本书计划中的推进（' + String(own.plan).slice(0, 18) + '…）；不做无代价的推进。',
          why: '把读者承诺写成可检验的连载契约，依据是本书自己的全书计划。' };
      }
      if (field === 'perspective') {
        if (!who) return empty;
        return { after: '第三人称限知（跟随' + who + '，仅在章末允许短暂切换）。',
          why: '视角跟随本书已建的第一位主要人物；限定视角可约束信息泄露。' };
      }
      if (field === 'style') {
        return { after: '冷硬克制；短句为主；判断藏在动作里，不用解释性旁白。',
          why: '通用建议（不含他书专有设定）：可改可拒。' };
      }
      if (!curS) return empty;
      return { after: curS, why: '该字段需要作者给出本书自己的表述，演示不代写。', empty: true };
    }
    if (kind === 'world') {
      var w = byId(c.world, id);
      if (!w) return empty;
      if (field === 'exception' && w.cond) {
        return { after: '例外：只在' + String(w.cond).slice(0, 16) + '成立的前提下，且需付出可见代价，方可不受限制。',
          why: '把「例外」从待探索写成可写规则，条件直接取自本书该条目的 cond。' };
      }
      if (field === 'cost' && w.cond) {
        return { after: '代价：每次行使都要付出一次可被读者看见的损失。',
          why: '规则型条目需要代价；此处只给结构槽位，具体损失由作者填。', empty: false };
      }
      return { after: curS, why: '该字段需要作者给出本书自己的表述，演示不代写。', empty: true };
    }
    if (kind === 'character') {
      var ch = byId(c.characters, id);
      if (!ch) return empty;
      if (field === 'arc' && (ch.goal || ch.weakness)) {
        return { after: (ch.arc ? ch.arc + '；' : '') + '中段增加一次与「' + (ch.weakness || ch.goal) + '」直接冲突的选择，作为转折点。',
          why: '弧线的转折必须咬合本书该人物已有的弱点 / 目标，才有代价。' };
      }
      if (field === 'voice') {
        return { after: '短句为主；答非所问时用一个动作收尾，不解释动机。',
          why: '声纹写成可对照的规则，便于审校时与本书该人物的既有对白核对。' };
      }
      return { after: curS, why: '该字段需要作者给出本书自己的表述，演示不代写。', empty: true };
    }
    if (kind === 'arc') {
      if (field === 'climax' && c.arc.mainConflict) {
        return { after: '高潮：正面冲击本书主要冲突——' + String(c.arc.mainConflict).slice(0, 26) + '（不另起一个冲突）。',
          why: '高潮必须冲击本书已有的主要冲突。' };
      }
      return { after: curS, why: '该字段需要作者给出本书自己的表述，演示不代写。', empty: true };
    }
    if (kind === 'outline') {
      if (!own.plan && !own.chars.length) return empty;
      return { after: '必须延续：上一章结尾的异常；不能提前揭示：本章计划要保留的信息；可以推进：' +
        (own.plan ? String(own.plan).slice(0, 20) + '…' : (own.chars[0] || '主线') + '所在的线') + '。',
        why: '按「必须延续 / 不能提前揭示 / 可以推进」三行拆章纲，依据是本书自己的全书计划。' };
    }
    if (kind === 'scene') {
      var planRef = own.plan ? String(own.plan).slice(0, 18) : null;
      if (!planRef && !own.chars.length) return empty;
      return { after: '目的：' + (planRef || '推动本章计划') + '；结束状态：本场结束时，' + (own.chars[0] || '主角') + '手上多出一件可验证的物证。',
        why: '场景要有可验收的结束状态；人物取自本书已建角色。' };
    }
    return { after: curS, why: '演示未覆盖该对象的起草；请直接手写。', empty: true };
  }

  /* ================= 行动：模式路由 ================= */
  WB.on['book.craftMode'] = function (el, d) { WB.go('book', 'craft', { bookId: d.book, mode: d.mode }); };
  WB.on['book.sceneChap'] = function (el, d) { WB.go('book', 'craft', { bookId: d.book, mode: 'scenes', chapter: d.chapter }); };
  WB.on['book.reviewKind'] = function (el, d) { WB.go('book', 'review', { bookId: d.book, kind: d.kind, chapter: d.chapter }); };
  WB.on['book.reviewChap'] = function (el, d) { WB.go('book', 'review', { bookId: d.book, kind: d.kind, chapter: d.chapter }); };

  /* ================= 行动：打开编辑器 ================= */
  function openEditor(title, hint, value, isList, footer) {
    var body = '<div class="fld" style="margin-bottom:8px"><label>' + title + '</label>' +
      (isList
        ? '<input class="inp" id="cfVal" value="' + WB.esc(asList(value).join('、')) + '" placeholder="多项用「、」分隔" />'
        : '<textarea class="ta" id="cfVal" rows="4">' + WB.esc(value == null ? '' : value) + '</textarea>') +
      '</div>' + (hint ? ui.note('bound', hint) : '');
    WB.modal({ title: title, body: body, footer: footer });
  }
  WB.on['craft.edit'] = function (el, d) {
    var b = curBook(), c = WB.craftOf(b.id);
    var cur = readField(c, d.kind, d.id, d.field, { chapter: d.chapter });
    var isList = Array.isArray(cur);
    /* chapter 是场景等对象的归属键：必须一路带到写入，否则写入会指向不存在的 bucket
       （已复现缺陷：保存后 toast 成功但场景没变）。 */
    var chap = d.chapter || '';
    openEditor('编辑 · ' + label(d.field),
      '直接写入由作者决定；也可以先存为候选，确认后再写入。计划不是已发生事实，改动会记录影响范围。',
      cur, isList,
      '<button class="btn" data-action="close-modal">取消</button>' +
      '<button class="btn primary" data-action="act.c" data-fn="craftSaveDirect" data-a1="' + b.id + '" data-a2="' + d.kind + '" data-a3="' + WB.esc(d.id || '') + '" data-a4="' + d.field + '" data-a5="' + WB.esc(chap) + '">直接写入（作者决定）</button>' +
      '<button class="btn" data-action="act.c" data-fn="craftSaveAsProposal" data-a1="' + b.id + '" data-a2="' + d.kind + '" data-a3="' + WB.esc(d.id || '') + '" data-a4="' + d.field + '" data-a5="' + WB.esc(chap) + '">作为候选（需确认）</button>');
  };
  /* 起草（非讨论）：打开时可改，保存前会显示本书是否有可用素材 */
  WB.on['craft.draft'] = function (el, d) {
    var b = curBook(), c = WB.craftOf(b.id);
    var g = mockGenerate(c, d.kind, d.id, d.field);
    if (g.empty) {
      WB.modal({ title: '演示未模拟 · ' + label(d.field),
        body: '<div class="note choice"><b>本书还没有可用素材</b>' + WB.esc(g.why) + '</div>' +
          '<div class="sm t3">演示不会把其他作品的人物或设定搬过来填空。</div>',
        footer: '<button class="btn primary" data-action="close-modal">知道了，我直接手写</button>' });
      return;
    }
    var cur = readField(c, d.kind, d.id, d.field, { chapter: d.chapter });
    openEditor('编辑起草的草案 · ' + label(d.field),
      '这是编辑按本书自有素材起草的具体草案（演示生成）。可继续编辑，再选择「作为候选」或「直接写入」。',
      g.after, false,
      '<button class="btn" data-action="close-modal">取消</button>' +
      '<div class="spacer"></div>' +
      '<button class="btn" data-action="act.c" data-fn="craftSaveAsProposalFrom" data-a1="' + b.id + '" data-a2="' + d.kind + '" data-a3="' + WB.esc(d.id || '') + '" data-a4="' + d.field + '" data-a5="' + WB.esc(cur == null ? '' : (Array.isArray(cur) ? cur.join('、') : cur)) + '" data-a6="' + WB.esc(g.why) + '" data-a7="' + WB.esc(d.chapter || '') + '">存为候选</button>' +
      '<button class="btn primary" data-action="act.c" data-fn="craftSaveDirect" data-a1="' + b.id + '" data-a2="' + d.kind + '" data-a3="' + WB.esc(d.id || '') + '" data-a4="' + d.field + '" data-a5="' + WB.esc(d.chapter || '') + '">直接写入</button>');
  };
  /* 真实讨论：作者提要求 → 员工接管范围 → 具体回复与可编辑提案（输入框为空） */
  WB.on['craft.discuss'] = function (el, d) {
    var b = curBook();
    var spec = d.spec;
    if (!spec) {
      if (d.kind === 'scene') spec = 'scene:' + b.id + ':' + d.chapter + ':' + d.id;
      else if (d.kind === 'positioning') spec = 'pos:' + b.id + ':' + d.field;
      else if (d.kind === 'world') spec = 'world:' + b.id + ':' + d.id + ':' + d.field;
      else if (d.kind === 'character') spec = 'char:' + b.id + ':' + d.id + ':' + d.field;
      else if (d.kind === 'outline') spec = 'outline:' + b.id + ':' + d.id + ':' + d.field;
      else if (d.kind === 'arc') spec = 'book:' + b.id;
      else spec = 'book:' + b.id;
    }
    var lab = d.label || (label(d.field) + ' · ' + targetLabelOfKind(parseObj(spec)));
    WB.openConv('E-01', spec, lab);
  };
  /* 追加对象（世界 / 人物 / 大纲 / 场景 / 结局） */
  var FACT_STATE_OPTS = [['TO_EXPLORE', '待探索'], ['PLANNED', '仅计划'], ['MANUSCRIPT_FACT', '正文已发生'],
    ['CONFIRMED_CANON', '已确认设定'], ['AI_INFERRED', '推断待确认'], ['CONFLICTED', '存在冲突']];
  var LEVEL_OPTS = [['book', '全书'], ['volume', '卷'], ['chapter', '章']];
  function addFields(kind) {
    return ({
      world: [['name', 'text'], ['kind', 'text'], ['cond', 'text'], ['cost', 'text'], ['limit', 'text'], ['exception', 'text'], ['source', 'text']],
      character: [['name', 'text'], ['role', 'text'], ['goal', 'text'], ['motivation', 'text'], ['weakness', 'text'], ['voice', 'text']],
      outline: [['title', 'text'], ['level', 'select', LEVEL_OPTS], ['chapterKey', 'chapterpick'], ['purpose', 'text'], ['events', 'text']],
      scene: [['purpose', 'text'], ['pov', 'text'], ['place', 'text'], ['conflict', 'text'], ['reveal', 'text'],
        ['notReveal', 'text'], ['endState', 'text'], ['emotion', 'text'], ['length', 'text'], ['cast', 'cast'], ['refs', 'refs']],
      ending: [['text', 'text']]
    })[kind] || [['name', 'text']];
  }
  function fieldWidget(f, bookId, value) {
    var n = f[0], type = f[1], opts = f[2];
    var id = 'ad_' + n;
    if (type === 'select') {
      return '<select class="sel" id="' + id + '">' + (opts || []).map(function (o) {
        return '<option value="' + o[0] + '"' + (value === o[0] ? ' selected' : '') + '>' + WB.esc(o[1]) + '</option>';
      }).join('') + '</select>';
    }
    if (type === 'chapterpick') {
      var chs = bookChapters(bookId);
      return '<select class="sel" id="' + id + '"><option value="">（不绑定章节：纯计划）</option>' +
        chs.map(function (k) {
          var ch = WB.S.chapters[k];
          return '<option value="' + k + '"' + (value === k ? ' selected' : '') + '>第 ' + ch.no + ' 章 · ' + WB.esc(ch.title) + '</option>';
        }).join('') + '</select>' +
        '<div class="t3 xs" style="margin-top:3px">按稳定章节键绑定，改名或换号不会断开关联。</div>';
    }
    if (type === 'cast') {
      var c = WB.craftOf(bookId);
      if (!c.characters.length) return '<div class="sm t3">本书还没有人物：先到「人物」新增角色。</div>';
      return '<div class="grid g2">' + c.characters.map(function (x) {
        return '<label class="sm" style="display:flex;gap:6px;align-items:center">' +
          '<input type="checkbox" data-multi="' + n + '" value="' + WB.esc(x.name) + '"' +
          ((value || []).indexOf(x.name) >= 0 ? ' checked' : '') + ' />' + WB.esc(x.name) + '</label>';
      }).join('') + '</div>';
    }
    if (type === 'refs') {
      var c2 = WB.craftOf(bookId);
      if (!c2.world.length) return '<div class="sm t3">本书还没有世界条目：先到「世界」新增。</div>';
      return '<div>' + c2.world.map(function (w) {
        return '<label class="sm" style="display:flex;gap:6px;align-items:center;margin-bottom:2px">' +
          '<input type="checkbox" data-multi="' + n + '" value="' + WB.esc(w.id) + '"' +
          ((value || []).indexOf(w.id) >= 0 ? ' checked' : '') + ' />' + WB.esc(w.name) + '（' + w.id + '）</label>';
      }).join('') + '</div>';
    }
    if (type === 'factstate') {
      return '<select class="sel" id="' + id + '">' + FACT_STATE_OPTS.map(function (o) {
        return '<option value="' + o[0] + '"' + (value === o[0] ? ' selected' : '') + '>' + WB.esc(o[1]) + '</option>';
      }).join('') + '</select>';
    }
    return '<input class="inp" id="' + id + '" value="' + WB.esc(value == null ? '' : value) + '" />';
  }
  WB.on['craft.add'] = function (el, d) {
    var b = curBook();
    var kind = d.kind;
    var names = { world: '新增世界条目', character: '新增人物', outline: '新增大纲节点', scene: '新增场景', ending: '新增结局候选' };
    var fields = addFields(kind);
    var body = fields.map(function (f) {
      return '<div class="fld" style="margin-bottom:8px"><label>' + label(f[0]) + '</label>' +
        fieldWidget(f, b.id, f[0] === 'level' ? (d.parent ? 'volume' : 'book') : '') + '</div>';
    }).join('');
    WB.modal({ title: names[kind] || '新增',
      body: body + ui.note('bound', '新增后为「待探索 / 计划」状态，不会自动进入 Canon；确认后才作为事实使用。' +
        (kind === 'outline' ? ' 父节点：' + WB.esc(d.parent || '（顶层）') : '')),
      footer: '<button class="btn" data-action="close-modal">取消</button>' +
        '<button class="btn primary" data-action="act.c" data-fn="craftAddDo" data-a1="' + b.id + '" data-a2="' + kind + '" data-a3="' + WB.esc(d.parent || '') + '" data-a4="' + WB.esc(d.chapter || '') + '">创建</button>' });
  };
  /* 完整对象编辑器（R3）：场景 / 人物 / 世界 / 大纲的所有字段都可维护，
     场景的出场人物与引用资料从本书对象中勾选（下游写作依据读同一对象）。 */
  var OBJ_FIELDS = {
    world: [['name', 'text'], ['kind', 'text'], ['cond', 'text'], ['cost', 'text'], ['limit', 'text'],
      ['exception', 'text'], ['source', 'text'], ['state', 'factstate']],
    character: [['name', 'text'], ['role', 'text'], ['goal', 'text'], ['motivation', 'text'], ['weakness', 'text'],
      ['abilityLimit', 'text'], ['arc', 'text'], ['voice', 'text'], ['first', 'text'], ['status', 'text']],
    scene: [['purpose', 'text'], ['pov', 'text'], ['place', 'text'], ['conflict', 'text'], ['reveal', 'text'],
      ['notReveal', 'text'], ['endState', 'text'], ['emotion', 'text'], ['length', 'text'], ['cast', 'cast'], ['refs', 'refs']],
    outline: [['title', 'text'], ['level', 'select', LEVEL_OPTS], ['chapterKey', 'chapterpick'],
      ['purpose', 'text'], ['events', 'text'], ['emotion', 'text'], ['origin', 'text'], ['version', 'text']]
  };
  WB.on['craft.objEdit'] = function (el, d) {
    var b = curBook(), c = WB.craftOf(b.id);
    var fields = OBJ_FIELDS[d.kind];
    if (!fields) return;
    var o = objectOf(c, d.kind, d.id, { chapter: d.chapter });
    if (!o) { WB.toast('找不到该对象（可能已被删除）', 'warn'); return; }
    var body = fields.map(function (f) {
      return '<div class="fld" style="margin-bottom:8px"><label>' + label(f[0]) + '</label>' +
        fieldWidget(f, b.id, o[f[0]]) + '</div>';
    }).join('');
    WB.modal({ title: '编辑 · ' + targetLabelOf(c, d.kind, d.id) + (d.chapter ? '（第 ' + (WB.S.chapters[d.chapter] || {}).no + ' 章）' : ''),
      body: body + ui.note('bound', '改动会列入影响清单；计划不是已发生事实，已写正文与已发布版本不会被静默改写。'),
      footer: '<button class="btn" data-action="close-modal">取消</button>' +
        '<button class="btn primary" data-action="act.c" data-fn="craftObjSave" data-a1="' + b.id + '" data-a2="' + d.kind + '" data-a3="' + WB.esc(d.id) + '" data-a4="' + WB.esc(d.chapter || '') + '">保存</button>' });
  };
  WB.act.craftObjSave = function (bookId, kind, id, chapter) {
    var c = WB.craftOf(bookId);
    var fields = OBJ_FIELDS[kind];
    if (!fields) { WB.toast('未知对象类型', 'err'); return; }
    var ex = { chapter: chapter };
    var o = objectOf(c, kind, id, ex);
    if (!o) { WB.toast('未保存：目标对象已不存在', 'warn'); return; }
    var bad = [];
    fields.forEach(function (f) {
      var n = f[0];
      if (f[1] === 'cast' || f[1] === 'refs') {
        o[n] = Array.prototype.slice.call(document.querySelectorAll('[data-multi="' + n + '"]:checked'))
          .map(function (x) { return x.value; });
      } else {
        var e = document.getElementById('ad_' + n);
        if (!e) return;
        var v = String(e.value || '').trim();
        if (n === 'chapterKey') {
          o.chapterKey = v || null;
          o.chapterNo = v && WB.S.chapters[v] ? WB.S.chapters[v].no : null;
        } else if (n === 'name' && !v) { bad.push(label(n)); }
        else if (n === 'level') { o.level = (['book', 'volume', 'chapter'].indexOf(v) >= 0) ? v : 'book'; }
        else o[n] = v || null;
      }
    });
    if (bad.length) { WB.toast('未保存：' + bad.join('、') + ' 不能为空', 'warn'); return; }
    var imp = impactFor(c, kind, id, '（整对象）', null);
    if (imp) c.impactLog.push({ id: 'IM-' + (c.impactLog.length + 1), at: WB.now(),
      change: '编辑 ' + targetLabelOf(c, kind, id), affected: imp.affected,
      unchanged: '已发布正文与历史版本不改', decidedBy: '作者', state: 'applied' });
    WB.closeModal(); WB.rerender();
    WB.toast('已保存 ' + targetLabelOf(c, kind, id) + '；写作依据会读取同一对象', 'ok');
  };
  /* 关系新增（R3：此前没有常规入口） */
  WB.on['craft.relAdd'] = function () {
    var b = curBook(), c = WB.craftOf(b.id);
    if (!c.characters.length) { WB.toast('本书还没有人物：先新增角色再建关系', 'warn'); return; }
    var opts = c.characters.map(function (x) { return '<option value="' + WB.esc(x.name) + '">' + WB.esc(x.name) + '</option>'; }).join('');
    WB.modal({ title: '新增关系',
      body: '<div class="grid g2">' +
        '<div class="fld"><label>一方</label><select class="sel" id="relA">' + opts + '</select></div>' +
        '<div class="fld"><label>另一方</label><select class="sel" id="relB">' + opts + '</select></div></div>' +
        '<div class="grid g2" style="margin-top:8px">' +
        '<div class="fld"><label>关系</label><input class="inp" id="relType" placeholder="例如：合作 / 互相隐瞒" /></div>' +
        '<div class="fld"><label>始于</label><input class="inp" id="relSince" placeholder="例如：ch11" /></div></div>' +
        ui.note('bound', '关系带方向与起始点；未记录的关系不会被凭空补全。'),
      footer: '<button class="btn" data-action="close-modal">取消</button>' +
        '<button class="btn primary" data-action="act.c" data-fn="craftRelDo" data-a1="' + b.id + '">创建</button>' });
  };
  WB.act.craftRelDo = function (bookId) {
    var A = (document.getElementById('relA') || {}).value, B = (document.getElementById('relB') || {}).value;
    var type = String((document.getElementById('relType') || {}).value || '').trim();
    var since = String((document.getElementById('relSince') || {}).value || '').trim();
    if (!A || !B) { WB.toast('请选择关系双方', 'warn'); return; }
    if (A === B) { WB.toast('关系双方不能是同一人', 'warn'); return; }
    if (!type) { WB.toast('请填写关系类型', 'warn'); return; }
    if (!WB.S.storyState[bookId]) WB.S.storyState[bookId] = { characters: [], relations: [], canon: [], threads: [], timeline: [] };
    var rels = WB.S.storyState[bookId].relations || (WB.S.storyState[bookId].relations = []);
    var dup = rels.filter(function (r) { return r.a === A && r.b === B && r.type === type; })[0];
    if (dup) { WB.toast('该关系已存在，未重复添加', 'warn'); return; }
    rels.push({ a: A, b: B, type: type, since: since || '未记录' });
    WB.closeModal(); WB.rerender();
    WB.toast('已新增关系 ' + A + ' — ' + B + '（' + type + '）', 'ok');
  };
  WB.on['craft.know'] = function (el, d) {
    var b = curBook(), c = WB.craftOf(b.id), ch = byId(c.characters, d.id);
    if (!ch) return;
    var dom = d.domain;
    WB.modal({ title: '补充「' + WB.esc(ch.name) + '」的' + WB.esc(d.label) + '知情',
      body: '<div class="fld" style="margin-bottom:8px"><label>内容</label><input class="inp" id="knVal" placeholder="例如：顾晚其实救过林砚" /></div>' +
        ui.note('bound', '角色已知 / 作者已知 / 读者已知 / 尚未揭示必须分开；写作时只引用「该场景当下的知情状态」。'),
      footer: '<button class="btn" data-action="close-modal">取消</button>' +
        '<button class="btn primary" data-action="act.c" data-fn="charKnowAdd" data-a1="' + b.id + '" data-a2="' + d.id + '" data-a3="' + dom + '">加入</button>' });
  };

  /* ================= 行动：写入（带 chapter 归属 + 回读校验） ================= */
  WB.act.craftSaveDirect = function (bookId, kind, id, field, chapter) {
    var c = WB.craftOf(bookId), v = (document.getElementById('cfVal') || {}).value;
    if (v == null) { WB.toast('没有可保存的内容', 'warn'); return; }
    var ex = { chapter: chapter };
    var cur = readField(c, kind, id, field, ex);
    var val = Array.isArray(cur) ? asList(v) : String(v).trim();
    var wrote = writeField(c, kind, id, field, val, ex);
    var back = readFieldRaw(c, kind, id, field, ex);
    if (!wrote || JSON.stringify(back) !== JSON.stringify(val)) {
      WB.toast('未写入：找不到目标对象（' + kind + ' ' + (id || '') +
        (chapter ? ' · 第 ' + (WB.S.chapters[chapter] || {}).no + ' 章' : '') + '）——改动没有生效', 'warn');
      logStep('写入失败（对象不存在）：' + kind + ' ' + id + ' field=' + field + ' chapter=' + (chapter || '—'));
      return;
    }
    var imp = impactFor(c, kind, id, field, val);
    if (imp && kind !== 'manuscript') {
      c.impactLog.push({ id: 'IM-' + (c.impactLog.length + 1), at: WB.now(),
        change: '作者直接修改 · ' + targetLabelOf(c, kind, id) + ' · ' + label(field),
        affected: imp.affected, unchanged: '已发布正文与历史版本不改', decidedBy: '作者', state: 'applied' });
    }
    WB.toast('已直接写入（作者决定）' + (imp ? '；' + imp.note : ''), 'ok');
    WB.closeModal(); WB.rerender();
  };
  WB.act.craftSaveAsProposal = function (bookId, kind, id, field, chapter) {
    var c = WB.craftOf(bookId), v = (document.getElementById('cfVal') || {}).value;
    var ex = { chapter: chapter };
    var cur = readField(c, kind, id, field, ex);
    var before = cur == null ? '' : (Array.isArray(cur) ? cur.join('、') : String(cur));
    var after = Array.isArray(cur) ? asList(v).join('、') : String(v || '').trim();
    addProposal(bookId, kind, id, field, before, after, '作者与编辑讨论后形成的候选；确认后写入目标对象。',
      { targetLabel: targetLabelOf(c, kind, id), chapter: chapter || null });
    WB.toast('已存为候选，等待确认后写入', 'ok');
    WB.closeModal(); WB.rerender();
  };
  WB.act.craftSaveAsProposalFrom = function (bookId, kind, id, field, before, why, chapter) {
    var v = (document.getElementById('cfVal') || {}).value;
    var c = WB.craftOf(bookId);
    addProposal(bookId, kind, id, field, before, String(v || '').trim(), why || '编辑起草',
      { targetLabel: targetLabelOf(c, kind, id), chapter: chapter || null });
    WB.toast('已存为候选，等待确认后写入', 'ok');
    WB.closeModal(); WB.rerender();
  };
  WB.act.craftApplyProposal = function (pid) {
    var p = byId(WB.S.craftProposals, pid);
    if (!p) return;
    var c = WB.craftOf(p.bookId);
    var wrote;
    if (p.kind === 'manuscript') {
      var current=WB.msOf(p.targetId);
      if (!current || (p.before && current.paragraphs[(p.para||1)-1] !== p.before) || (WB.S.__msDraft && WB.S.__msDraft[p.targetId]!=null)) { WB.toast('正文已变化或有未保存修改，请重新对照候选；未覆盖草稿。','warn'); return; }
      wrote = writeField(c, 'manuscript', p.targetId, 'paragraphs', p.after, { para: p.para });
    } else {
      var ex = { chapter: p.chapter || '' };
      var cur = readField(c, p.kind, p.targetId, p.field, ex);
      wrote = writeField(c, p.kind, p.targetId, p.field, Array.isArray(cur) ? asList(p.after) : p.after, ex);
    }
    if (!wrote) {
      WB.toast('未应用：目标对象已不存在（' + p.kind + ' ' + p.targetId + '）——候选仍保留，未写入', 'warn');
      logStep('候选应用失败：' + pid + ' 目标不存在');
      return;
    }
    p.state = 'applied'; p.appliedAt = WB.now();
    var imp2 = impactFor(c, p.kind, p.targetId, p.field, p.after);
    WB.toast('候选已应用并写入目标对象' + (imp2 ? '；' + imp2.note : ''), 'ok');
    WB.rerender();
  };
  WB.act.craftDropProposal = function (pid) {
    var p = byId(WB.S.craftProposals, pid);
    if (p) { p.state = 'rejected'; p.droppedAt = WB.now(); }
    WB.toast('已放弃该候选；目标对象保持不变', '');
    WB.rerender();
  };
  WB.act.craftEditProposal = function (pid) {
    var p = byId(WB.S.craftProposals, pid);
    if (!p) return;
    openEditor('编辑候选 · ' + p.fieldLabel, '候选仍需确认后才会写入目标对象。', p.after, false,
      '<button class="btn" data-action="close-modal">取消</button>' +
      '<button class="btn primary" data-action="act.c" data-fn="craftUpdateProposal" data-a1="' + p.id + '">保存候选</button>');
  };
  WB.act.craftUpdateProposal = function (pid) {
    var p = byId(WB.S.craftProposals, pid), v = (document.getElementById('cfVal') || {}).value;
    p.after = String(v || '').trim(); p.editedAt = WB.now();
    WB.toast('候选已更新，仍未写入', 'ok'); WB.closeModal(); WB.rerender();
  };
  WB.act.craftDiscussProposal = function (pid) {
    var p = byId(WB.S.craftProposals, pid);
    WB.closeModal();
    WB.openConv('E-01', p.bookId + '|' + p.targetId, '候选 ' + p.id + ' · ' + p.fieldLabel);
  };
  WB.act.craftAddDo = function (bookId, kind, parent, chapter) {
    var c = WB.craftOf(bookId);
    function g(n) { var e = document.getElementById('ad_' + n); return e ? String(e.value || '').trim() : ''; }
    function gm(n) {
      return Array.prototype.slice.call(document.querySelectorAll('[data-multi="' + n + '"]:checked'))
        .map(function (x) { return x.value; });
    }
    function validLevel(v) { return ['book', 'volume', 'chapter'].indexOf(v) >= 0 ? v : null; }
    if (kind === 'world') {
      var id = 'WD-' + (c.world.length + 1 + 10);
      c.world.push({ id: id, kind: g('kind') || '待定', name: g('name') || '未命名条目', cond: g('cond'), cost: g('cost'),
        limit: g('limit'), exception: g('exception'), state: 'TO_EXPLORE', source: g('source') || '作者新增', evidence: null, refs: [] });
      WB.toast('已新增世界条目 ' + id + '（待探索）', 'ok');
    } else if (kind === 'character') {
      var cid = 'CH-' + (c.characters.length + 1 + 20);
      c.characters.push({ id: cid, name: g('name') || '未命名角色', role: g('role'), goal: g('goal'),
        motivation: g('motivation'), weakness: g('weakness'), abilityLimit: null, arc: null, voice: g('voice'),
        first: '待定', status: '待定', knows: { character: [], author: [], reader: [], unrevealed: [] } });
      WB.toast('已新增人物 ' + cid + '；动机 / 弧线可继续补', 'ok');
    } else if (kind === 'outline') {
      var oid = 'O-' + (c.outline.length + 1 + 20);
      var lvl = validLevel(g('level')) || (parent ? 'volume' : 'book');
      var ck = g('chapterKey');
      c.outline.push({ id: oid, level: lvl, parent: parent || null, chapterKey: ck || null,
        chapterNo: ck && WB.S.chapters[ck] ? WB.S.chapters[ck].no : null,
        title: g('title') || '未命名节点', purpose: g('purpose'), events: g('events'), emotion: null,
        origin: 'author', version: 'v1' });
      WB.toast('已新增大纲节点 ' + oid + '（作者纲' +
        (ck && WB.S.chapters[ck] ? ' · 已绑定第 ' + WB.S.chapters[ck].no + ' 章' : ' · 未绑定章节（纯计划）') + '）', 'ok');
    } else if (kind === 'scene') {
      var key = chapter;
      if (!key || !WB.S.chapters[key]) { WB.toast('未指定章节：场景必须归属某一章', 'warn'); return; }
      if (!c.scenes[key]) c.scenes[key] = [];
      var sid = 'SC-' + String((WB.S.chapters[key] || {}).no || 0) + '-' + (c.scenes[key].length + 1);
      c.scenes[key].push({ id: sid, order: c.scenes[key].length + 1, purpose: g('purpose'), pov: g('pov'),
        cast: gm('cast'), place: g('place'), conflict: g('conflict'), reveal: g('reveal'), notReveal: g('notReveal'),
        emotion: g('emotion'), endState: g('endState'), length: g('length'), refs: gm('refs') });
      WB.toast('已新增场景 ' + sid + '（第 ' + WB.S.chapters[key].no + ' 章 · 出场 ' + gm('cast').length + ' 人）', 'ok');
    } else if (kind === 'ending') {
      var eid = 'EN-' + (c.arc.endings.length + 1 + 10);
      c.arc.endings.push({ id: eid, text: g('text') || '未命名结局', state: 'candidate' });
      WB.toast('已新增结局候选 ' + eid, 'ok');
    }
    WB.closeModal(); WB.rerender();
  };
  WB.act.charKnowAdd = function (bookId, cid, domain) {
    var c = WB.craftOf(bookId), ch = byId(c.characters, cid);
    var v = (document.getElementById('knVal') || {}).value;
    if (!v || !v.trim()) { WB.toast('请填写内容', 'warn'); return; }
    if (!ch.knows) ch.knows = { character: [], author: [], reader: [], unrevealed: [] };
    if (!ch.knows[domain]) ch.knows[domain] = [];
    ch.knows[domain].push(v.trim());
    WB.toast('已补充知情（' + domain + '）；写作时按当下知情引用', 'ok');
    WB.closeModal(); WB.rerender();
  };
  WB.on['craft.knowRemove'] = function (el, d) {
    var c = curCraft(), ch = byId(c.characters, d.id);
    if (ch && ch.knows && ch.knows[d.domain]) ch.knows[d.domain].splice(Number(d.idx), 1);
    WB.toast('已移除该条知情'); WB.rerender();
  };
  WB.on['craft.endingPick'] = function (el, d) {
    var c = curCraft();
    c.arc.endings.forEach(function (e) { if (e.id !== d.id) e.state = 'candidate'; });
    var e2 = byId(c.arc.endings, d.id); if (e2) { e2.state = 'confirmed'; e2.confirmedAt = WB.now(); }
    WB.toast('已将该结局定为当前方向（其余保留为候选）', 'ok');
    c.impactLog.push({ id: 'IM-' + (c.impactLog.length + 1), at: WB.now(), change: '确认结局方向 ' + d.id,
      affected: ['卷三章纲与高潮设计'], unchanged: '已写正文不改', decidedBy: '作者', state: 'applied' });
    WB.rerender();
  };
  WB.on['craft.impactList'] = function (el, d) {
    var c = curCraft();
    WB.openDrawer({ title: '影响清单 · ' + WB.esc(d.what || '本次变更'),
      sub: '计划变更不静默覆盖已写正文',
      body: '<div class="tl">' + (c.impactLog.length ? c.impactLog.map(function (i) {
        return '<div class="tl-i ok"><div class="tl-t">' + WB.esc(i.change) + ' <span class="t3 xs">' + WB.esc(i.at) + '</span></div>' +
          '<div class="tl-s">受影响：' + WB.esc((i.affected || []).join('、') || '—') + '<br>不变：' + WB.esc(i.unchanged || '—') +
          '<br>决定：' + WB.esc(i.decidedBy || '—') + '</div></div>';
      }).join('') : '<div class="empty"><b>暂无变更记录</b>改动人物 / 设定 / 大纲后会在此列出影响范围。</div>') + '</div>' +
        ui.note('bound', '这里的每一条都是「影响清单」，不是「已全书改写」。作者可分批修订，历史正文与已发布版本保留。') });
  };
  function targetLabelOf(c, kind, id) {
    if (kind === 'positioning') return '本书定位';
    if (kind === 'world') { var w = byId(c.world, id); return w ? '世界 · ' + w.name : '世界条目'; }
    if (kind === 'character') { var ch = byId(c.characters, id); return ch ? '人物 · ' + ch.name : '人物'; }
    if (kind === 'outline') { var o = byId(c.outline, id); return o ? '大纲 · ' + o.title : '大纲节点'; }
    if (kind === 'arc') return '主支线与结局';
    if (kind === 'scene') return '场景计划 ' + id;
    if (kind === 'manuscript') return '正文段落';
    if (kind === 'ending') return '结局候选 ' + id;
    return id;
  }
  /* 变更影响：返回 { affected:[受影响范围], note:提示语 }。
     affected 必须是「受影响范围清单」（字符串数组），不得塞一句提示语——数据层与影响清单都依赖它可枚举。 */
  function impactFor(c, kind, id, field, val) {
    var o = id ? byId((c && c[kind === 'world' ? 'world' : kind === 'character' ? 'characters' : kind === 'outline' ? 'outline' : 'arc']) || [], id) : null;
    var refs = (o && o.refs) ? o.refs : [];
    if (kind === 'positioning') return { affected: ['后续章目标与创作方向引用'], note: '已在定位中记录；后续章目标可按需引用新版本' };
    if (kind === 'world') return {
      affected: ['背景 ' + (id || '') + (o && o.name ? '（' + o.name + '）' : '')].concat(
        refs.length ? refs.map(function (r) { return '引用 ' + r + ' 的相关章'; }) : ['引用该规则的相关章（尚未登记引用）']),
      note: '已记入影响清单：引用该规则的相关章需复核' };
    if (kind === 'character') return {
      affected: ['人物 ' + (id || '') + (o && o.name ? '（' + o.name + '）' : '')].concat(
        refs.length ? refs.map(function (r) { return '引用 ' + r + ' 的相关章'; }) : ['涉及该人物知情/弧线的章']),
      note: '已记入影响清单：涉及该人物知情/弧线的章需复核' };
    if (kind === 'outline') return {
      affected: ['大纲节点 ' + (id || '') + '（' + label(field) + '）', '计划变更：不影响已写正文'],
      note: '仅改动计划，不影响已写正文' };
    if (kind === 'manuscript') return { affected: ['本章正文段落'], note: '正文段落已更新（历史版本仍在版本历史中）' };
    return { affected: ['与 ' + (id || kind) + ' 相关的后续写作'], note: '' };
  }

  /* ================= 创作内核视图 ================= */
  function modeNav(current, bookId) {
    return '<div class="chiprow">' + CRAFT_MODES.map(function (m) {
      return '<button class="chip' + (m[0] === current ? ' on' : '') + '" data-action="book.craftMode" data-book="' + bookId + '" data-mode="' + m[0] + '">' + WB.esc(m[1]) + '</button>';
    }).join('') + '</div>';
  }
  WB.craftPanel=function(mode,ctx){var b=curBook(),c=curCraft();
    if(mode==='world')return worldPanel(b,c);if(mode==='characters')return charPanel(b,c);
    if(mode==='arc')return arcPanel(b,c);if(mode==='outline')return outlinePanel(b,c);
    if(mode==='scenes')return scenesPanel(b,c,ctx||{params:{}});return positioningPanel(b,c);
  };
  WB.register('book.craft', {
    render: function (ctx) {
      var b = curBook(), c = curCraft();
      var mode = (ctx.params && ctx.params.mode) || 'positioning';
      var head = ui.hdr('构思与规划 · ' + WB.esc(b.title),
        '逐步完善你的故事；编辑建议由你决定。',
        '<button class="btn" data-action="craft.impactList" data-what="' + WB.esc(b.title) + '">影响清单</button>' +
        '<button class="btn primary" data-action="nav.view" data-area="book" data-view="manuscript">去写正文</button>',
        '<span>作品 ' + WB.esc(b.id) + '</span><span class="t4">|</span><span>6 类创作对象</span><span class="t4">|</span><span>计划 ≠ 已发生事实</span>');
      var body;
      if (mode === 'world') body = worldPanel(b, c);
      else if (mode === 'characters') body = charPanel(b, c);
      else if (mode === 'arc') body = arcPanel(b, c);
      else if (mode === 'outline') body = outlinePanel(b, c);
      else if (mode === 'scenes') body = scenesPanel(b, c, ctx);
      else body = positioningPanel(b, c);
      return head + modeNav(mode, b.id) + body;
    },
    aside: function (ctx) {
      var b = curBook(), c = curCraft();
      var props = openProposals(b.id);
      return WB.asBlock('责任人', WB.ownerHtml('E-05') +
          '<div class="sm t3" style="margin-top:6px">责任编辑承担创作；独立审校编辑给出检查意见，作者裁决。</div>') +
        WB.asBlock('待确认候选（' + props.length + '）',
          props.length ? props.slice(0, 3).map(function (p) {
            return '<div class="as-w clickable" data-action="book.craftMode" data-book="' + b.id + '" data-mode="' + modeOfKind(p.kind) + '">' +
              '<div class="wt">' + WB.esc(p.fieldLabel) + '</div><div class="ws">' + WB.esc(p.targetLabel || p.targetId) + '</div></div>';
          }).join('') : '<div class="sm t3">暂无待确认候选。</div>') +
        WB.asBlock('本书来源',
          '<div class="sm t2">· 来源：作者决定 / 正文事实 / 计划 / 推断<br>· 变更 → 影响清单，不静默全书覆盖<br>· 空书显示真实空状态与创建入口</div>');
    }
  });
  function modeOfKind(kind) {
    return ({ positioning: 'positioning', world: 'world', character: 'characters', outline: 'outline',
      arc: 'arc', scene: 'scenes', ending: 'arc', manuscript: 'scenes' })[kind] || 'positioning';
  }

  /* ==========================================================================
     创作选择 L01–L24：摘要 / 选择器 / 写作要求
     依据：CURIS_WRITING_FULL_PRODUCT_INTERACTION_DESIGN_CANDIDATE.md §16.2、§17.2(D06)、§17.3
     规则（硬约束）：
       · 构思不是空文本框：默认主页只给「当前故事＋定位摘要＋少量关键已选项＋调整入口」。
       · 跨组标签用有界选择弹框（搜索/分组/已选摘要/可编辑写作要求/确认作用范围/保存）；
         少量单选用下拉；章级有限参数用右 Utility；完整构思留 Main。
       · 选择必须能转成「可编辑的写作要求」——只存标签不进入任务视为失败。
       · 关弹框回原编辑草稿；取消不生效；确认不立即生成；已手选项不被推荐静默替换。
       · 不自动新增人物、不改正文；视角/基调的「矛盾」只解释，不用标签词面禁止创作。
     ========================================================================== */
  function flattenSel(def, e) {
    if (!def) return [];
    var sel = [];
    if (Array.isArray(e.sel)) sel = sel.concat(e.sel);
    (def.optGroups || []).forEach(function (g, gi) {
      var a = e[WB.tagSubKey(def.id, gi)];
      if (Array.isArray(a)) sel = sel.concat(a);
    });
    return sel.filter(function (x) { return x && x !== '（待定）'; });
  }
  /* 已选 → 自动整理的自然语言要求（作者可直接改写；改写后的文本保存在 e.req） */
  function autoReq(def, e) {
    var sel = flattenSel(def, e);
    var parts = [];
    if (sel.length) parts.push(sel.join('、'));
    if (e.custom) parts.push('自定义：' + e.custom);
    if (e.note) parts.push(e.note);
    if (!parts.length) return '';
    return '【' + def.name + '】' + parts.join('；') + '。（本次写作要遵守；可直接改写这句。）';
  }
  /* 标签 → 定位字段：让既有下游（章目标/场景/正文依据）读到同一份选择，不建第二套真源 */
  function syncPositioningFromTags(c) {
    var pos = c.positioning, tags = WB.tagsOf(c), out = [];
    function get(id) { var d = WB.tagDef(id); return d ? flattenSel(d, tags[id] || {}) : []; }
    var v;
    v = get('L02'); if (v.length) { pos.readerPartition = v.join('、'); pos.fields.readerPartition = 'confirmed'; out.push('读者分区'); }
    v = get('L03');
    var cu = (tags.L03 || {}).custom;
    if (v.length || cu) { pos.genres = v.concat(cu ? [cu] : []); pos.fields.genres = 'confirmed'; out.push('题材'); }
    v = get('L12');
    if (v.length) { var k13 = get('L13'); pos.perspective = v.join('、') + (k13.length ? '（' + k13.join('、') + '）' : '');
      pos.fields.perspective = 'confirmed'; out.push('叙事视角'); }
    v = get('L16');
    if (v.length) { var k15 = get('L15'); pos.style = v.join('、') + (k15.length ? '；基调 ' + k15.join('、') : '');
      pos.fields.style = 'confirmed'; out.push('风格'); }
    v = get('L21'); if (v.length) { pos.taboos = v.slice(); pos.fields.taboos = 'confirmed'; out.push('作者禁区'); }
    v = get('L22');
    var e22 = tags.L22 || {};
    if (v.length || e22.targetChars) {
      var bits = v.slice();
      if (e22.targetChars) bits.push('目标 ' + e22.targetChars);
      if (e22.chapterChars) bits.push('章长 ' + e22.chapterChars);
      if (bits.length) { pos.lengthPlan = bits.join('；'); pos.fields.lengthPlan = 'confirmed'; out.push('篇幅意向'); }
    }
    return out;
  }

  /* ---- 选择器弹框（有界：搜索 / 分组 / 已选摘要 / 确认作用范围 / 保存） ---- */
  function pickState() { return WB.S.__pick; }
  function tagPickerOpen(bookId, scope, chapter) {
    var b = WB.book(bookId || WB.S.__scope.bookId) || WB.scopeBook();
    var c = WB.craftOf(b.id);
    var tags = WB.tagsOf(c);
    var dims = {};
    WB.writingTags().forEach(function (t) { dims[t.id] = WB.clone(tags[t.id] || {}); });
    var gs = WB.tagGroups();
    WB.S.__pick = { bookId: b.id, scope: scope === 'chapter' ? 'chapter' : 'book',
      chapter: chapter || null, group: (gs[0] || {}).id, q: '', dims: dims, dirty: false };
    tagPickerRender();
  }
  function pickHas(p, id) {
    var t = WB.tagDef(id); if (!t) return false;
    var e = p.dims[id] || {};
    return flattenSel(t, e).length > 0 || !!(e.custom && String(e.custom).trim()) || !!e.undecided;
  }
  function pickCount(p, gid) {
    var n = 0;
    WB.writingTags().forEach(function (t) { if ((!gid || t.group === gid) && pickHas(p, t.id)) n++; });
    return n;
  }
  function searchHit(t, q) {
    var s = q.toLowerCase();
    if (t.name.toLowerCase().indexOf(s) >= 0 || t.id.toLowerCase().indexOf(s) >= 0) return true;
    var opts = (t.opts || []).slice();
    (t.optGroups || []).forEach(function (g) { opts = opts.concat(g.opts); });
    return opts.some(function (o) { return o.toLowerCase().indexOf(s) >= 0; });
  }
  function chips(t, e, gi, list) {
    var key = gi == null ? 'sel' : WB.tagSubKey(t.id, gi);
    var cur = Array.isArray(e[key]) ? e[key] : [];
    return list.map(function (o) {
      var on = cur.indexOf(o) >= 0;
      return '<button class="tagopt' + (on ? ' on' : '') + '" data-action="pick.opt" data-tag="' + t.id +
        '" data-g="' + (gi == null ? '' : gi) + '" data-opt="' + WB.esc(o) + '">' + WB.esc(o) + '</button>';
    }).join('');
  }
  function dimBlock(p, t) {
    var e = p.dims[t.id] || (p.dims[t.id] = {});
    var modeTxt = t.mode === 'single' ? '单选' : (t.mode === 'multi' ? '多选 · 可标主次' : '组合 · 基础＋说明');
    var body = t.optGroups
      ? t.optGroups.map(function (g, gi) {
          return '<div class="tagsub">' + WB.esc(g.name) + '</div><div class="tagchips">' + chips(t, e, gi, g.opts) + '</div>';
        }).join('')
      : '<div class="tagchips">' + chips(t, e, null, t.opts) + '</div>';
    var extra = '<div class="tagchips" style="margin-top:6px">' +
      '<button class="tagopt' + (e.undecided ? ' on' : '') + '" data-action="pick.undecided" data-tag="' + t.id + '">待定</button>' +
      (t.optional ? '<span class="sm t3" style="align-self:center">（可不选）</span>' : '') +
      '</div>';
    if (t.mode === 'combo' || t.allowCustom || t.freeText) {
      extra += '<input class="tagp-search" style="margin-top:6px" data-input="pick.custom" data-id="' + t.id +
        '" placeholder="自定义（你自己的想法，会作为额外选项记录）" value="' + WB.esc(e.custom || '') + '">' +
        '<textarea style="min-height:38px;margin-top:6px;width:100%;border:1px solid var(--line);border-radius:7px;padding:5px 7px;font-size:11.5px;background:var(--surface);font-family:inherit" ' +
        'data-input="pick.note" data-id="' + t.id + '" placeholder="组合说明 / 例外（可选）">' + WB.esc(e.note || '') + '</textarea>';
    }
    return '<div class="tagdim" id="dim-' + t.id + '"><div class="tagdim-h">' + WB.esc(t.id + ' ' + t.name) +
      '<span class="mode">' + modeTxt + '</span><span class="mode">' + WB.esc(t.scope) + '</span></div>' +
      '<div class="tagdim-why">' + WB.esc(t.why) + '</div>' + body + extra + '</div>';
  }
  function pickedItem(t, e) {
    var sel = flattenSel(t, e);
    if (!sel.length && !e.custom && !e.undecided) return '';
    return '<div class="tagp-item"><div class="ti-h">' + WB.esc(t.name) +
      (e.undecided ? '<span class="mode">待定</span>' : '') + '</div>' +
      (sel.length ? '<div class="ti-sel">' + WB.esc(sel.join('、')) + '</div>' : '') +
      (e.custom ? '<div class="ti-sel">自定义：' + WB.esc(e.custom) + '</div>' : '') +
      (e.note ? '<div class="ti-sel">说明：' + WB.esc(e.note) + '</div>' : '') +
      '<div class="ti-req"><textarea data-input="pick.req" data-id="' + t.id +
      '" placeholder="转成这次要遵守的写作要求">' + WB.esc(e.req || autoReq(t, e)) + '</textarea></div>' +
      '<div class="btnrow" style="margin-top:4px"><button class="btn sm ghost" data-action="pick.clear" data-tag="' + t.id + '">清除这一项</button></div></div>';
  }
  function tagPickerRender(focusSearch) {
    var p = pickState(); if (!p) return;
    var gs = WB.tagGroups();
    var q = (p.q || '').trim();
    var groupsHtml = gs.map(function (g) {
      var cnt = pickCount(p, g.id);
      return '<button class="tagp-group' + (g.id === p.group && !q ? ' on' : '') + '" data-action="pick.group" data-g="' + g.id + '">' +
        '<span>' + WB.esc(g.name) + '</span><span class="gc">' + (cnt ? cnt + ' 已选' : '—') + '</span></button>';
    }).join('');
    var dims = WB.writingTags().filter(function (t) { return q ? searchHit(t, q) : t.group === p.group; });
    var optsHtml = dims.length
      ? dims.map(function (t) { return dimBlock(p, t); }).join('')
      : '<div class="sm t3">没有匹配「' + WB.esc(q) + '」的标签。可以写进上面的「自定义」，或换一个词再搜。</div>';
    var picked = WB.writingTags().map(function (t) { return pickedItem(t, p.dims[t.id] || {}); }).filter(Boolean);
    var chapters = Object.keys(WB.S.chapters).filter(function (k) { return WB.S.chapters[k].bookId === p.bookId; })
      .sort(function (x, y) { return WB.S.chapters[x].no - WB.S.chapters[y].no; });
    var scopeHtml = '<div class="tagp-top"><input class="tagp-search" id="tagpSearch" data-input="pick.search" ' +
      'placeholder="搜索标签（如 悬疑 / 冷峻 / 第一人称 / 伏笔）" value="' + WB.esc(p.q || '') + '">' +
      '<span class="tagp-scope">作用于：<select data-change="pick.scope">' +
      '<option value="book"' + (p.scope === 'book' ? ' selected' : '') + '>本书定位与写作偏好</option>' +
      '<option value="chapter"' + (p.scope === 'chapter' ? ' selected' : '') + '>本章临时要求（不改成全书）</option>' +
      '</select>' +
      (p.scope === 'chapter'
        ? '<select data-change="pick.chapter">' + chapters.map(function (k) {
            return '<option value="' + k + '"' + (p.chapter === k ? ' selected' : '') + '>' + WB.esc(WB.S.chapters[k].title || k) + '</option>';
          }).join('') + '</select>'
        : '') + '</span></div>';
    var warn = (p.scope === 'chapter')
      ? '<div class="tagp-warn">本章临时覆盖只改这一章；保存后会与全书定位并置显示，随时可恢复为继承全书。</div>'
      : '<div class="tagp-warn">保存只改变「选择与写作要求」，不会立即生成正文，也不改任何进行中 Work 的已固定输入。需要重做时由你明确发起新候选。</div>';
    WB.modal({
      title: '创作方向 · L01–L24 完整选择',
      body: '<div class="tagp">' + scopeHtml +
        '<div class="tagp-body">' +
        '<div class="tagp-groups">' + groupsHtml + '</div>' +
        '<div class="tagp-opts">' + optsHtml + '</div>' +
        '<div class="tagp-picked"><div class="sm t3" style="margin-bottom:6px">已选摘要（' + picked.length +
        ' 组）· 每项都可改写成你的要求</div>' + (picked.length ? picked.join('') :
          '<div class="sm t3">还没有选择。左侧按组浏览，或直接搜索；也可以先用「和编辑一起想」。</div>') + '</div>' +
        '</div>' + warn + '</div>',
      footer: '<button class="btn" data-action="pick.cancel">取消（不生效）</button>' +
        '<button class="btn" data-action="craft.suggest" data-book="' + p.bookId + '">和编辑一起想</button>' +
        '<button class="btn primary" data-action="pick.save">保存到' + (p.scope === 'chapter' ? '本章' : '本书') + '</button>'
    });
    if (focusSearch) { var s = document.getElementById('tagpSearch'); if (s) { s.focus(); try { s.setSelectionRange(s.value.length, s.value.length); } catch (e) {} } }
  }
  WB.on['pick.group'] = function (elm, d) { var p = pickState(); if (!p) return; p.group = d.g; p.q = ''; tagPickerRender(); };
  WB.on['pick.search'] = function (elm, d) { var p = pickState(); if (!p) return; p.q = d.value; tagPickerRender(true); };
  WB.on['pick.scope'] = function (elm, d) {
    var p = pickState(); if (!p) return;
    p.scope = d.value === 'chapter' ? 'chapter' : 'book';
    if (p.scope === 'chapter' && !p.chapter) {
      var ks = Object.keys(WB.S.chapters).filter(function (k) { return WB.S.chapters[k].bookId === p.bookId; });
      ks.sort(function (x, y) { return WB.S.chapters[x].no - WB.S.chapters[y].no; });
      p.chapter = ks[0] || null;
    }
    tagPickerRender();
  };
  WB.on['pick.chapter'] = function (elm, d) { var p = pickState(); if (!p) return; p.chapter = d.value; tagPickerRender(); };
  WB.on['pick.opt'] = function (elm, d) {
    var p = pickState(); if (!p) return;
    var t = WB.tagDef(d.tag); if (!t) return;
    var e = p.dims[t.id] || (p.dims[t.id] = {});
    var key = (d.g === '' || d.g == null) ? 'sel' : WB.tagSubKey(t.id, Number(d.g));
    var arr = Array.isArray(e[key]) ? e[key].slice() : [];
    var i = arr.indexOf(d.opt);
    if (i >= 0) arr.splice(i, 1);
    else if (t.mode === 'single' && key === 'sel') arr = [d.opt];
    else arr.push(d.opt);
    e[key] = arr;
    e.undecided = false;
    p.dirty = true;
    tagPickerRender();
  };
  WB.on['pick.undecided'] = function (elm, d) {
    var p = pickState(); if (!p) return;
    var e = p.dims[d.tag] || (p.dims[d.tag] = {});
    e.undecided = !e.undecided; p.dirty = true; tagPickerRender();
  };
  WB.on['pick.custom'] = function (elm, d) {
    var p = pickState(); if (!p) return;
    var e = p.dims[d.id] || (p.dims[d.id] = {}); e.custom = d.value; p.dirty = true;
  };
  WB.on['pick.note'] = function (elm, d) {
    var p = pickState(); if (!p) return;
    var e = p.dims[d.id] || (p.dims[d.id] = {}); e.note = d.value; p.dirty = true;
  };
  WB.on['pick.req'] = function (elm, d) {
    var p = pickState(); if (!p) return;
    var e = p.dims[d.id] || (p.dims[d.id] = {}); e.req = d.value; p.dirty = true;
  };
  WB.on['pick.clear'] = function (elm, d) {
    var p = pickState(); if (!p) return;
    p.dims[d.tag] = {}; p.dirty = true; tagPickerRender();
    WB.toast('已清除 ' + d.tag + '（还在草稿里，保存后才生效）');
  };
  WB.on['pick.cancel'] = function () {
    var p = pickState();
    WB.S.__pick = null; WB.closeModal();
    WB.toast(p && p.dirty ? '已放弃本次修改：定位与写作偏好保持原样' : '未修改任何内容');
  };
  WB.on['pick.save'] = function () {
    var p = pickState(); if (!p) return;
    var all = WB.writingTags();
    if (p.scope === 'chapter' && p.chapter) {
      var ch = WB.S.chapters[p.chapter];
      if (!ch) { WB.toast('找不到本章，无法保存章级要求', 'warn'); return; }
      ch.tagOverride = ch.tagOverride || {};
      ch.tagOverride._on = true;
      all.forEach(function (t) { ch.tagOverride[t.id] = WB.clone(p.dims[t.id] || {}); });
      WB.S.__pick = null; WB.closeModal(); WB.save(); WB.render();
      WB.toast('本章临时要求已保存到「' + (ch.title || p.chapter) + '」。全书定位未被改写，可随时恢复继承。', 'ok');
      return;
    }
    var c = WB.craftOf(p.bookId);
    var tags = WB.tagsOf(c);
    var changed = [];
    all.forEach(function (t) {
      var before = JSON.stringify(tags[t.id] || {});
      var work = WB.clone(p.dims[t.id] || {});
      if (!work.req) work.req = autoReq(t, work);
      tags[t.id] = work;
      if (JSON.stringify(work) !== before) changed.push(t.name);
    });
    var synced = syncPositioningFromTags(c);
    c.positioning.tagUpdatedAt = WB.now();
    WB.S.__pick = null; WB.closeModal(); WB.save(); WB.render();
    WB.toast('创作选择已保存到本书' + (changed.length ? '（改动 ' + changed.length + ' 组：' + changed.slice(0, 4).join('、') + (changed.length > 4 ? '…' : '') + '）' : '（无改动）') +
      (synced.length ? '；同步定位字段：' + synced.join('、') : '') + '。不会立即生成正文。', 'ok');
  };

  /* ----「不确定，和编辑一起想」：2–3 组带理由的 Mock 建议；选择后真更新候选与定位 ---- */
  function suggestOpen(bookId) {
    var b = WB.book(bookId || WB.S.__scope.bookId);
    var sugs = WB.tagSuggestions() || [];
    WB.modal({ title: '和编辑一起想 · 编辑给的方向（不是替你决定）',
      body: '<div class="sm t2" style="margin-bottom:10px">编辑给出 2–3 组带理由与代价的方向。采用只会补上你还没选的维度；' +
        '你已经手选过的维度不会被静默替换。采用后仍可继续手改。</div>' +
        sugs.map(function (s) {
          var chips = Object.keys(s.tags).map(function (id) {
            var t = WB.tagDef(id); if (!t) return '';
            return '<div class="ts-w"><b>' + WB.esc(t.name) + '</b>：' + WB.esc(s.tags[id].join('、')) + '</div>';
          }).join('');
          return '<div class="tag-suggest"><div class="ts-h">' + WB.esc(s.name) +
            '<span class="st st-badge st-choice">来自 ' + WB.esc(s.by) + '</span></div>' +
            '<div class="ts-w"><b>为什么：</b>' + WB.esc(s.why) + '</div>' + chips +
            '<div class="ts-t"><b>代价 / 取舍：</b>' + WB.esc(s.tradeoff) + '</div>' +
            '<div class="btnrow" style="margin-top:8px">' +
            '<button class="btn sm primary" data-action="craft.applySuggest" data-id="' + s.id + '">采用这组（只补空缺）</button>' +
            '</div></div>';
        }).join(''),
      footer: '<button class="btn" data-action="close-modal">先不用，我自己选</button>' });
  }
  WB.on['craft.suggest'] = function (elm, d) { suggestOpen(d.book); };
  WB.on['craft.applySuggest'] = function (elm, d) {
    var sug = (WB.tagSuggestions() || []).filter(function (s) { return s.id === d.id; })[0];
    if (!sug) return;
    var b = WB.scopeBook(); var c = WB.craftOf(b.id); var tags = WB.tagsOf(c);
    var kept = [], applied = [];
    Object.keys(sug.tags).forEach(function (id) {
      var t = WB.tagDef(id); if (!t) return;
      var cur = flattenSel(t, tags[id] || {});
      if (cur.length || (tags[id] && tags[id].custom)) { kept.push(t.name + '（保留你的选择）'); return; }
      tags[id] = { sel: sug.tags[id].slice(), note: '', req: autoReq(t, { sel: sug.tags[id].slice() }) };
      applied.push(t.name);
    });
    syncPositioningFromTags(c);
    c.positioning.tagUpdatedAt = WB.now();
    WB.closeModal(); WB.save(); WB.render();
    WB.toast('已采用「' + sug.name + '」：写入 ' + (applied.length ? applied.join('、') : '（无空缺可补）') +
      (kept.length ? '；' + kept.join('、') + ' 未被覆盖' : '') + '。可继续手改，或直接开始写。', 'ok');
  };
  /* ---- L01–L24 覆盖清单（交付清点，也是「记录全 / 展示少」的落点） ---- */
  WB.on['craft.coverage'] = function (elm, d) {
    var b = WB.book(d.book || WB.S.__scope.bookId);
    var c = WB.craftOf(b.id); var tags = WB.tagsOf(c);
    var rows = WB.writingTags().map(function (t) {
      var e = tags[t.id] || {}, sel = flattenSel(t, e);
      var state = sel.length ? '已选' : (e.undecided ? '待定' : '未选');
      var cls = sel.length ? 'st-published' : (e.undecided ? 'st-choice' : 'st-unknown');
      var g = (WB.tagGroups() || []).filter(function (x) { return x.id === t.group; })[0];
      return '<tr><td><b>' + t.id + '</b></td><td>' + WB.esc(t.name) + '</td><td>' + WB.esc((g || {}).name || '') +
        '</td><td>' + WB.esc(sel.join('、') || (e.undecided ? '（待定）' : '—')) +
        '</td><td>' + WB.stBadge(state, sel.length ? 'published' : (e.undecided ? 'choice' : 'unknown')) +
        '</td><td><button class="btn sm ghost" data-action="craft.gotoDim" data-tag="' + t.id + '">打开</button></td></tr>';
    }).join('');
    var done = WB.writingTags().filter(function (t) { return pickHas({ dims: tags }, t.id); }).length;
    WB.modal({ title: 'L01–L24 覆盖清单 · ' + b.title,
      body: '<div class="sm t2" style="margin-bottom:8px">已记录 <b>' + done + ' / 24</b> 组。' +
        '“已选/待定/未选”表示当前状态，不代表必须填满——未选不会阻止写作。</div>' +
        '<table class="tbl"><thead><tr><th>编号</th><th>维度</th><th>分组</th><th>当前选择</th><th>状态</th><th></th></tr></thead><tbody>' +
        rows + '</tbody></table>',
      footer: '<button class="btn" data-action="close-modal">关闭</button>' +
        '<button class="btn primary" data-action="craft.picker" data-book="' + b.id + '" data-scope="book">打开选择器</button>' });
  };
  WB.on['craft.gotoDim'] = function (elm, d) {
    var t = WB.tagDef(d.tag); if (!t) return;
    WB.closeModal(); tagPickerOpen(WB.S.__scope.bookId, 'book', null);
    var p = pickState(); if (p) { p.group = t.group; tagPickerRender(); }
    setTimeout(function () {
      var n = document.getElementById('dim-' + t.id);
      if (n && n.scrollIntoView) n.scrollIntoView({ block: 'center' });
    }, 30);
  };
  WB.on['craft.picker'] = function (elm, d) { tagPickerOpen(d.book, d.scope, d.chapter || null); };

  function positioningPanel(b, c) {
    var pos = c.positioning;
    var tags = WB.tagsOf(c);
    var props = openProposals(b.id, 'positioning');
    var all = WB.writingTags();
    var covered = all.filter(function (t) { return WB.tagTouched(tags, t.id); }).length;
    var story = pos.coreOriginal || '';
    var KEY = ['L02', 'L03', 'L04', 'L12', 'L15', 'L16', 'L20'];
    var keyHtml = KEY.map(function (id) {
      var t = WB.tagDef(id); if (!t) return '';
      var p = WB.tagPicked(tags, id);
      if (!p.sel.length) return '';
      return '<span class="keytag"><b>' + WB.esc(t.name) + '</b> ' + WB.esc(p.sel.join('、')) + '</span>';
    }).join('');
    var rows = POS_FIELDS.map(function (f) {
      var key = f[0], isList = f[2] === 'list';
      var val = pos[key];
      var valHtml = (isList ? (val || []).join('、') : val);
      var shown = valHtml ? WB.esc(valHtml) : WB.unknown('待填写');
      return '<div class="row"><div class="row-main"><div class="row-t">' + WB.esc(f[1]) + ' ' +
        WB.factBadge((pos.fields || {})[key] || 'empty') + '</div>' +
        '<div class="row-s">' + shown + '</div>' +
        '<div class="row-meta"><button class="btn sm" data-action="craft.edit" data-kind="positioning" data-field="' + key + '">编辑</button>' +
        '<button class="btn sm ghost" data-action="craft.discuss" data-kind="positioning" data-field="' + key + '" data-label="定位 · ' + WB.esc(f[1]) + '">讨论</button></div></div></div>';
    }).join('');
    return ui.panel({ title: '本书构思与定位',
        sub: '当前故事 · 定位摘要 · 调整入口。24 组创作选择已记录，按需展开，不铺成勾选表。',
        actions: '<button class="btn sm primary" data-action="craft.picker" data-book="' + b.id + '" data-scope="book">调整创作方向</button>' +
          '<button class="btn sm" data-action="craft.suggest" data-book="' + b.id + '">和编辑一起想</button>',
        body:
          '<div class="fld"><label>一句话故事</label><div>' + (story ? WB.esc(story) : WB.unknown('还没有一句话故事——可以先手写一句，稍后再补')) + '</div>' +
          '<div class="btnrow" style="margin-top:6px">' +
          '<button class="btn sm" data-action="craft.edit" data-kind="positioning" data-field="coreOriginal">手改</button>' +
          '<button class="btn sm ghost" data-action="craft.discuss" data-kind="positioning" data-field="coreOriginal" data-label="定位 · 一句话故事">和编辑讨论</button>' +
          '</div></div>' +
          '<div class="hr"></div>' +
          '<div class="sm t3" style="margin-bottom:6px">关键已选项 · 已记录 ' + covered + ' / ' + all.length + ' 组（其余按需展开，不铺成勾选表）</div>' +
          (keyHtml ? '<div class="keystrip">' + keyHtml + '</div>'
            : '<div class="sm t3">还没有选择创作方向。可以从「调整创作方向」开始，也可以直接手写，稍后再补——未选不阻止写作。</div>') +
          '<div class="btnrow" style="margin-top:10px">' +
          '<button class="btn sm" data-action="craft.coverage" data-book="' + b.id + '">查看 L01–L24 覆盖清单</button>' +
          '<button class="btn sm ghost" data-action="craft.draft" data-kind="positioning" data-field="coreOriginal">让编辑起草核心</button>' +
          '</div>' }) +
      '<details class="flow-details"><summary>完整定位字段（可后补）</summary>'+ui.panel({ title: '完整定位字段（可后补）', sub: '标签会同步到这里的字段；两者是同一份事实，不是两套真源。',
        body: '<div class="rows">' + rows + '</div>' +
          ui.note('choice', '<b>读者分区与题材是两个维度：</b>读者分区（男频 / 女频 / 不限）是运营分区，不等于题材；题材（都市 / 玄幻 / 科幻 …）可组合、暂定或自定义。不用男频决定只能写男主，也不把女频等同言情。') +
          ui.note('bound', '定位未必要一次填完。缺事实才询问；书名与计划可先建议。定位被接受后会用于本书规划与章目标，并记录来源（' + WB.esc(pos.origin === 'direction' ? '来自方向 ' + (pos.originRef || '') : pos.origin === 'imported' ? '接入既有作品' : '作者建立') + '）。') })+'</details>' +
      (props.length ? ui.panel({ title: '待确认候选', body: props.map(proposalCard).join('') }) : '') +
      ui.panel({ title: '定位 → 下游', body:
        '<div class="grid g3">' +
        '<div class="fld"><label>用于本书规划</label><div class="sm t2">章目标与场景准备会引用定位版本 ' + WB.esc(pos.updatedAt || '（待更新）') + '</div></div>' +
        '<div class="fld"><label>用于本次写作</label><div class="sm t2">标签已转成可编辑的写作要求；本次写作依据会说明用了哪些。生成后应能对照实际文本，而不是「模型收到标签」就算达成。</div></div>' +
        '<div class="fld"><label>不自动做什么</label><div class="sm t2">不自动新增人物、不改已写正文、不把本章临时要求改成全书；<b>生成 ≠ 定稿 ≠ 发布</b>。</div></div>' +
        '</div>' });
  }

  function worldPanel(b, c) {
    var props = openProposals(b.id, 'world');
    var rows = c.world.length ? c.world.map(function (w) {
      return '<div class="pnl" style="margin-bottom:10px"><div class="pnl-h"><div class="pnl-t">' +
        WB.esc(w.name) + ' <span class="sub">' + WB.esc(w.kind) + '</span></div><div class="pnl-a">' + WB.factBadge(w.state) + '</div></div>' +
        '<div class="pnl-body"><div class="grid g2">' +
        '<div class="fld"><label>条件 / 表现</label><div class="sm">' + (w.cond ? WB.esc(w.cond) : WB.unknown('待探索')) + '</div></div>' +
        '<div class="fld"><label>代价</label><div class="sm">' + (w.cost ? WB.esc(w.cost) : '—') + '</div></div>' +
        '<div class="fld"><label>限制</label><div class="sm">' + (w.limit ? WB.esc(w.limit) : '—') + '</div></div>' +
        '<div class="fld"><label>例外</label><div class="sm">' + (w.exception && w.exception !== '—' && w.exception !== '未知。' ? WB.esc(w.exception) : WB.unknown(w.exception || '未知')) + '</div></div>' +
        '</div>' +
        '<div class="sm t3" style="margin-top:6px">来源：' + WB.esc(w.source || '—') + (w.evidence ? ' · 证据：' + WB.esc(w.evidence) : '') + '</div>' +
        '<div class="btnrow" style="margin-top:8px">' +
        '<button class="btn sm" data-action="craft.objEdit" data-kind="world" data-id="' + w.id + '">编辑条目</button>' +
        '<button class="btn sm ghost" data-action="craft.discuss" data-kind="world" data-id="' + w.id + '" data-field="cond" data-label="世界 · ' + WB.esc(w.name) + '">讨论</button>' +
        '</div></div></div>';
    }).join('') : ui.empty('本书暂无世界条目', '可以新增时代 / 地点 / 势力 / 规则。没有需要世界规则的作品不强迫创建。');

    var worldProps = props.filter(function (p) { return p.kind === 'world'; });
    return ui.panel({ title: '背景与世界', sub: '规则 / 地点 / 势力：条件·代价·限制·例外',
      actions: '<button class="btn sm" data-action="craft.add" data-kind="world">新增世界条目</button>',
      body: rows + (worldProps.length ? '<div class="hr"></div>' + worldProps.map(proposalCard).join('') : '') ,
      footer: '<span>变更会列出受影响计划与已写正文；确认前不改变任何事实状态。</span>' });
  }

  function charPanel(b, c) {
    var props = openProposals(b.id, 'character');
    var DOMS = [['character', '角色已知'], ['author', '作者已知'], ['reader', '读者已知'], ['unrevealed', '尚未揭示']];
    if (!c.characters.length) {
      return ui.panel({ title: '人物与关系', actions: '<button class="btn sm" data-action="craft.add" data-kind="character">新增人物</button>',
        body: ui.empty('本书暂无人物', '可新增角色定位、目标、动机、弱点、能力限制、成长弧线、说话方式与四类知情。') });
    }
    var cards = c.characters.map(function (ch) {
      var knows = ch.knows || {};
      var kGrid = '<div class="grid g4" style="margin-top:8px">' + DOMS.map(function (dm) {
        var list = knows[dm[0]] || [];
        return '<div class="fld"><label>' + dm[1] + '（' + list.length + '）</label>' +
          (list.length ? list.map(function (t, i) {
            return '<div class="sm" style="margin-bottom:2px">· ' + WB.esc(t) +
              ' <button class="chip static" style="padding:0 4px" data-action="craft.knowRemove" data-id="' + ch.id + '" data-domain="' + dm[0] + '" data-idx="' + i + '" title="移除">×</button></div>';
          }).join('') : '<div class="sm t3">' + WB.unknown('未记录') + '</div>') +
          '<button class="btn sm ghost" style="margin-top:4px" data-action="craft.know" data-id="' + ch.id + '" data-domain="' + dm[0] + '" data-label="' + dm[1] + '">＋ 补充</button></div>';
      }).join('') + '</div>';
      var chProps = props.filter(function (p) { return p.targetId === ch.id; });
      var card=ui.panel({ title: WB.esc(ch.name) + ' <span class="sub">' + WB.esc(ch.role || '未定') + '</span>',
        actions: WB.factBadge('confirmed'),
        body: '<div class="grid g2">' +
          '<div class="fld"><label>目标</label><button class="btn sm ghost" data-action="craft.discuss" data-kind="character" data-id="' + ch.id + '" data-field="goal" data-label="人物 · ' + WB.esc(ch.name) + ' · 目标">讨论此项</button><div class="sm">' + (ch.goal ? WB.esc(ch.goal) : WB.unknown('待填写')) + '</div></div>' +
          '<div class="fld"><label>动机</label><button class="btn sm ghost" data-action="craft.discuss" data-kind="character" data-id="' + ch.id + '" data-field="motivation" data-label="人物 · ' + WB.esc(ch.name) + ' · 动机">讨论此项</button><div class="sm">' + (ch.motivation ? WB.esc(ch.motivation) : WB.unknown('待填写')) + '</div></div>' +
          '<div class="fld"><label>弱点</label><button class="btn sm ghost" data-action="craft.discuss" data-kind="character" data-id="' + ch.id + '" data-field="weakness" data-label="人物 · ' + WB.esc(ch.name) + ' · 弱点">讨论此项</button><div class="sm">' + (ch.weakness ? WB.esc(ch.weakness) : WB.unknown('待填写')) + '</div></div>' +
          '<div class="fld"><label>能力限制</label><button class="btn sm ghost" data-action="craft.discuss" data-kind="character" data-id="' + ch.id + '" data-field="abilityLimit" data-label="人物 · ' + WB.esc(ch.name) + ' · 能力限制">讨论此项</button><div class="sm">' + (ch.abilityLimit && ch.abilityLimit !== '—' ? WB.esc(ch.abilityLimit) : '—') + '</div></div>' +
          '<div class="fld"><label>成长弧线</label><button class="btn sm ghost" data-action="craft.discuss" data-kind="character" data-id="' + ch.id + '" data-field="arc" data-label="人物 · ' + WB.esc(ch.name) + ' · 成长弧线">讨论此项</button><div class="sm">' + (ch.arc ? WB.esc(ch.arc) : WB.unknown('待填写')) + '</div></div>' +
          '<div class="fld"><label>说话方式（声纹）</label><button class="btn sm ghost" data-action="craft.discuss" data-kind="character" data-id="' + ch.id + '" data-field="voice" data-label="人物 · ' + WB.esc(ch.name) + ' · 说话方式（声纹）">讨论此项</button><div class="sm">' + (ch.voice ? WB.esc(ch.voice) : WB.unknown('待填写')) + '</div></div>' +
          '</div>' +
          '<div class="sm t3" style="margin-top:6px">首次出现：' + WB.esc(ch.first || '未定') + ' · 状态：' + WB.esc(ch.status || '—') + '</div>' +
          '<div class="hr" style="margin:8px 0"></div><div class="sm t2"><b>认知域</b>：角色 / 作者 / 读者 / 尚未揭示必须分开；写作时只引用该场景当下的知情状态。</div>' +
          kGrid +
          '<div class="btnrow" style="margin-top:8px">' +
          '<button class="btn sm" data-action="craft.objEdit" data-kind="character" data-id="' + ch.id + '">编辑档案</button>' +
          '<button class="btn sm" data-action="craft.edit" data-kind="character" data-id="' + ch.id + '" data-field="arc">编辑弧线</button>' +
          '<button class="btn sm" data-action="craft.draft" data-kind="character" data-id="' + ch.id + '" data-field="arc">起草弧线</button>' +
          '<button class="btn sm ghost" data-action="craft.discuss" data-kind="character" data-id="' + ch.id + '" data-field="arc" data-label="人物 · ' + WB.esc(ch.name) + ' 弧线">讨论</button>' +
          '</div>' + (chProps.length ? chProps.map(proposalCard).join('') : '') });
      return WB.S.__route.view==='craft'?card:'<details class="flow-details"><summary>'+WB.esc(ch.name)+' · '+WB.esc(ch.role||'未定')+'</summary>'+card+'</details>';
    }).join('');
    var relations = '<div class="grid g2">' +
      ui.panel({ title: '关系（带方向与阶段）', tight: true,
        actions: '<button class="btn sm" data-action="craft.relAdd">新增关系</button>',
        body: ((WB.S.storyState[b.id] || {}).relations || []).length
          ? ui.tbl(['一方', '另一方', '关系', '始于'],
            ((WB.S.storyState[b.id] || {}).relations || []).map(function (r) { return { cells: [WB.esc(r.a), WB.esc(r.b), WB.esc(r.type), WB.esc(r.since)] }; }))
          : ui.empty('本书暂无关系记录', '关系带方向与阶段；未记录的不会凭空生成。') }) +
      ui.panel({ title: '非 Canon 演练', body: '<div class="sm t2">角色模拟（酒馆）属非 Canon 演练：对白需作者选入并复查前后文，聊天结束不会自动更新人物事实。</div>' }) +
      '</div>';
    return ui.panel({ title: '人物与关系', actions: '<button class="btn sm" data-action="craft.add" data-kind="character">新增人物</button>',
      body: cards, footer: '<span>角色 / 读者 / 作者已知分开；不强制所有作品都是男女双主角。</span>' }) + relations;
  }

  function arcPanel(b, c) {
    var a = c.arc, props = openProposals(b.id, 'arc');
    function lineList(title, arr, kind) {
      return '<div class="fld"><label>' + title + '</label>' + (arr.length ? arr.map(function (l) {
        return '<div class="sm" style="margin-bottom:3px">' + WB.esc(l.id) + ' ' + WB.esc(l.text) + ' ' + WB.factBadge(l.state) +
          ' <span class="t3 xs">' + WB.esc(l.from || '') + '</span></div>';
      }).join('') : '<div class="sm t3">' + WB.unknown('未填写') + '</div>') + '</div>';
    }
    var endings = a.endings.length ? a.endings.map(function (e) {
      return '<div class="row"><div class="row-main"><div class="row-t">' + WB.esc(e.id) + ' ' +
        (e.state === 'confirmed' ? WB.stBadge('当前方向', 'published') : WB.stBadge('候选', 'choice')) + '</div>' +
        '<div class="row-s">' + WB.esc(e.text) + '</div>' +
        '<div class="row-meta"><button class="btn sm" data-action="craft.endingPick" data-id="' + e.id + '">定为当前方向</button>' +
        '<button class="btn sm ghost" data-action="craft.edit" data-kind="ending" data-id="' + e.id + '" data-field="text">编辑</button></div></div></div>';
    }).join('') : ui.empty('尚无结局候选', '可以保留多个结局方向；确认前它们是候选，不是已发生事实。');
    return ui.panel({ title: '故事主线与结局', sub: '前提 → 冲突 → 主线/支线 → 转折 → 高潮',
        body: '<div class="grid g2">' +
          '<div class="fld"><label>故事前提</label><div class="sm">' + (a.premise ? WB.esc(a.premise) : WB.unknown('待填写')) + '</div>' +
          '<div class="btnrow" style="margin-top:4px"><button class="btn sm" data-action="craft.edit" data-kind="arc" data-field="premise">编辑</button>' +
          '<button class="btn sm ghost" data-action="craft.discuss" data-kind="arc" data-field="premise" data-label="主支线与结局 · 故事前提">讨论</button></div></div>' +
          '<div class="fld"><label>主要冲突</label><div class="sm">' + (a.mainConflict ? WB.esc(a.mainConflict) : WB.unknown('待填写')) + '</div>' +
          '<div class="btnrow" style="margin-top:4px"><button class="btn sm" data-action="craft.edit" data-kind="arc" data-field="mainConflict">编辑</button></div></div>' +
          lineList('主线', a.mainLines) + lineList('支线', a.subLines) +
          '</div>' +
          '<div class="hr"></div>' +
          '<div class="fld"><label>关键转折</label>' + (a.turns.length ? a.turns.map(function (t) {
            return '<div class="sm" style="margin-bottom:3px">' + WB.esc(t.id) + ' ' + WB.esc(t.at || '') + ' ' + WB.esc(t.text) + ' ' + WB.factBadge(t.state) + '</div>';
          }).join('') : '<div class="sm t3">' + WB.unknown('未填写') + '</div>') + '</div>' +
          '<div class="fld" style="margin-top:8px"><label>高潮</label><div class="sm">' + (a.climax ? WB.esc(a.climax) : WB.unknown('待填写')) + '</div>' +
          '<div class="btnrow" style="margin-top:4px"><button class="btn sm" data-action="craft.edit" data-kind="arc" data-field="climax">编辑</button>' +
          '<button class="btn sm ghost" data-action="craft.discuss" data-kind="arc" data-field="climax" data-label="主支线与结局 · 高潮">讨论</button></div></div>' +
          '<div class="fld" style="margin-top:8px"><label>未兑现的承诺</label>' + (a.promises.length ? a.promises.map(function (p) {
            return '<div class="sm" style="margin-bottom:3px">' + WB.esc(p.id) + ' ' + WB.esc(p.text) + ' ' + WB.factBadge(p.state) + '</div>';
          }).join('') : '<div class="sm t3">' + WB.unknown('无') + '</div>') + '</div>',
        actions: '<button class="btn sm ghost" data-action="craft.impactList" data-what="结局与主线">影响清单</button>' }) +
      ui.panel({ title: '结局候选', sub: '可保留多个方向', actions: '<button class="btn sm" data-action="craft.add" data-kind="ending">新增结局候选</button>',
        body: endings, footer: '<span>结局计划不是已发生事实；确认后影响卷章与高潮设计，但不改写已写正文。</span>' }) +
      (props.length ? ui.panel({ title: '待确认候选', body: props.map(proposalCard).join('') }) : '');
  }

  function outlinePanel(b, c) {
    var props = openProposals(b.id, 'outline');
    function nodeHtml(n, depth) {
      var chKey = chapterForOutline(c, b.id, n);
      var kids = outlineChildren(c, n.id);
      var isAi = n.origin === 'ai';
      var link = chKey
        ? '对应章节：第 ' + WB.S.chapters[chKey].no + ' 章 · ' + WB.esc(WB.S.chapters[chKey].title) + '（已显式绑定）'
        : (n.level === 'chapter' ? '未绑定章节：纯计划，可到章节建好后绑定' : '');
      return '<div class="as-w" style="margin-left:' + (depth * 14) + 'px">' +
        '<div class="wt">' + WB.esc(n.title) + ' ' + (isAi ? WB.stBadge('AI 建议', 'choice') : WB.stBadge('作者纲', 'published')) +
        ' <span class="t3 xs">' + WB.esc(n.version || '') + '</span></div>' +
        '<div class="ws">目的：' + WB.esc(n.purpose || '—') + '</div>' +
        (n.events ? '<div class="ws">关键事件：' + WB.esc(n.events) + '</div>' : '') +
        '<div class="ws">情绪推进：' + WB.esc(n.emotion || '—') + (link ? ' · ' + link : '') + '</div>' +
        '<div class="btnrow" style="margin-top:4px">' +
        '<button class="btn sm" data-action="craft.objEdit" data-kind="outline" data-id="' + n.id + '">编辑</button>' +
        '<button class="btn sm ghost" data-action="craft.discuss" data-kind="outline" data-id="' + n.id + '" data-field="purpose" data-label="大纲 · ' + WB.esc(n.title) + '">讨论</button>' +
        (n.level === 'chapter' && chKey ? '<button class="btn sm ghost" data-action="book.sceneChap" data-book="' + b.id + '" data-chapter="' + chKey + '">去场景准备</button>' : '') +
        '<button class="btn sm ghost" data-action="craft.add" data-kind="outline" data-parent="' + n.id + '">细化子节点</button>' +
        '</div>' +
        kids.map(function (k) { return nodeHtml(k, depth + 1); }).join('') +
        '</div>';
    }
    var roots = c.outline.filter(function (n) { return !n.parent; });
    var tree = roots.length ? roots.map(function (r) { return nodeHtml(r, 0); }).join('')
      : ui.empty('本书尚无大纲', '可以从一句意图开始，直接写正文，再回头提取大纲——不强制先填完整表单。');
    return ui.panel({ title: '多级大纲', sub: '全书 → 卷 → 章（按作品需要，不强制四层）',
        actions: '<button class="btn sm" data-action="craft.add" data-kind="outline">新增节点</button>' +
          '<button class="btn sm ghost" data-action="craft.extract">从正文提取章纲</button>',
        body: tree,
        footer: '<span>作者纲与 AI 建议分开保存；章级节点按稳定章节键绑定，改名不改关联，也不改写已写正文。</span>' }) +
      ui.panel({ title: '计划与事实的边界', body:
        '<div class="grid g2"><div class="sm t2">· 大纲节点默认「仅计划」，未在正文发生</div>' +
        '<div class="sm t2">· 从正文提取的章纲标记为「AI 建议」，需作者确认</div></div>' }) +
      (props.length ? ui.panel({ title: '待确认候选', body: props.map(proposalCard).join('') }) : '');
  }
  WB.on['craft.extract'] = function () {
    var b = curBook(), c = WB.craftOf(b.id);
    var chs = bookChapters(b.id).filter(function (k) { return (WB.S.manuscripts[k] || {}).paragraphs; });
    if (!chs.length) { WB.toast('本书还没有可提取的正文；先写一段再来提取', 'warn'); return; }
    var key = chs[chs.length - 1], ch = WB.S.chapters[key];
    var first = (WB.S.manuscripts[key].paragraphs[0] || '').slice(0, 18);
    addProposal(b.id, 'outline', 'O-NEW-' + key, 'purpose', '', '正文提取：第 ' + ch.no + ' 章以「' + first + '…」开篇；建议章纲——目的：承接上一章；不能提前揭示：关键身份；可以推进：物证线。',
      '从已写正文反向提取章纲（候选）；确认后才成为章纲。',
      { targetLabel: '新章纲（第 ' + ch.no + ' 章）' });
    WB.toast('已从正文提取章纲候选，等待你确认', 'ok');
    WB.rerender();
  };

  function scenesPanel(b, c, ctx) {
    ensureOutlineLinks(b, c);
    var chs = bookChapters(b.id);
    if (!chs.length) {
      return ui.panel({ title: '章节与场景准备', body: ui.empty('本书还没有章节', '先在正文写作中开出第一章，再回来准备场景。') });
    }
    var ck = (ctx.params && ctx.params.chapter) || WB.S.__sel.sceneChap || chs[chs.length - 1];
    if (!WB.S.chapters[ck] || WB.S.chapters[ck].bookId !== b.id) ck = chs[chs.length - 1];
    WB.S.__sel.sceneChap = ck;
    var ch = WB.S.chapters[ck];
    var list = (c.scenes[ck] || []);
    var scenesHtml = list.length ? list.map(function (s) {
      return '<div class="pnl" style="margin-bottom:8px"><div class="pnl-h"><div class="pnl-t">场景 ' + WB.esc(s.id) +
        ' <span class="sub">顺序 ' + (s.order || '—') + '</span></div>' +
        '<div class="pnl-a">' + WB.stBadge('计划', 'wait') + '</div></div><div class="pnl-body"><div class="grid g3">' +
        '<div class="fld"><label>目的</label><div class="sm">' + WB.esc(s.purpose || '—') + '</div></div>' +
        '<div class="fld"><label>视角 / 地点</label><div class="sm">' + WB.esc(s.pov || '—') + ' · ' + WB.esc(s.place || '—') + '</div></div>' +
        '<div class="fld"><label>出场人物</label><div class="sm">' + (WB.esc((s.cast || []).join('、') || '') || WB.unknown('待补（从本书人物中选）')) + '</div></div>' +
        '<div class="fld"><label>冲突</label><div class="sm">' + WB.esc(s.conflict || '—') + '</div></div>' +
        '<div class="fld"><label>要揭示</label><div class="sm">' + WB.esc(s.reveal || '—') + '</div></div>' +
        '<div class="fld"><label>不能揭示</label><div class="sm">' + WB.esc(s.notReveal || '—') + '</div></div>' +
        '<div class="fld"><label>情绪 / 结束状态</label><div class="sm">' + WB.esc(s.emotion || '—') + ' · ' + WB.esc(s.endState || '—') + '</div></div>' +
        '<div class="fld"><label>长度意向</label><div class="sm">' + WB.esc(s.length || '—') + '</div></div>' +
        '<div class="fld"><label>引用资料</label><div class="sm">' + (WB.esc((s.refs || []).join('、') || '') || WB.unknown('待补（从本书世界条目中选）')) + '</div></div>' +
        '</div><div class="btnrow" style="margin-top:6px">' +
        '<button class="btn sm" data-action="craft.objEdit" data-kind="scene" data-id="' + s.id + '" data-chapter="' + ck + '">编辑场景</button>' +
        '<button class="btn sm ghost" data-action="craft.discuss" data-kind="scene" data-id="' + s.id + '" data-chapter="' + ck + '" data-field="purpose" data-label="场景 ' + s.id + ' · 第 ' + ch.no + ' 章">讨论</button>' +
        '</div></div></div>';
    }).join('') : ui.empty('本章尚无场景计划', '可拆分场景，明确目的 / 视角 / 出场人物 / 要揭示 / 不能揭示 / 情绪 / 结束状态。');

    var chipRow = '<div class="chiprow">' + chs.map(function (k) {
      return '<button class="chip' + (k === ck ? ' on' : '') + '" data-action="book.sceneChap" data-book="' + b.id + '" data-chapter="' + k + '">第 ' + WB.S.chapters[k].no + ' 章</button>';
    }).join('') + '</div>';

    return ui.panel({ title: '章节与场景准备 · ' + WB.esc(b.title), sub: '选章 → 拆场景 → 检查写作依据',
        actions: '<button class="btn sm" data-action="craft.add" data-kind="scene" data-chapter="' + ck + '">新增场景</button>' +
          '<button class="btn sm primary" data-action="nav.view" data-area="book" data-view="manuscript">从此章进入写作</button>',
        body: chipRow + scenesHtml,
        footer: '<span>场景计划是计划，不是已发生事实。</span>' }) +
      basisPanel(b, c, ck) +
      ui.panel({ title: '计划不强制线性', body:
        '<div class="sm t2">作者可以从一句意图直接写，也可以先规划；两种顺序都合法。计划可暂定、后补。</div>' });
  }

  /* 写作依据：写作前可查（按需展开，不常驻技术区域）
     opts.compact = true → 只留一行摘要 + 按需展开（供正文写作面使用，避免满依据占等宽位） */
  function basisPanel(b, c, ck, opts) {
    ensureOutlineLinks(b, c);
    var ch = WB.S.chapters[ck] || {};
    var chs = bookChapters(b.id);
    var idx = chs.indexOf(ck);
    var prev = idx > 0 ? WB.S.chapters[chs[idx - 1]] : null;
    var list = (c.scenes[ck] || []);
    var castNames = [];
    list.forEach(function (s) { (s.cast || []).forEach(function (n) { if (castNames.indexOf(n) < 0) castNames.push(n); }); });
    var cast = c.characters.filter(function (x) { return castNames.indexOf(x.name) >= 0; });
    var threads = ((WB.S.storyState[b.id] || {}).threads || []);
    var refs = [];
    list.forEach(function (s) { (s.refs || []).forEach(function (r) { if (refs.indexOf(r) < 0) refs.push(r); }); });
    var worldRefs = c.world.filter(function (w) { return refs.indexOf(w.id) >= 0; });
    var learnings = (WB.S.learningUsage || []).filter(function (u) { return u.where === ck; });
    if (opts && opts.compact) {
      var missing = [];
      if (!c.positioning.coreOriginal) missing.push('定位');
      if (!list.length) missing.push('场景');
      if (!cast.length) missing.push('出场人物');
      return ui.panel({ title: '写作依据｜第 ' + (ch.no || '—') + ' 章', sub: '按需展开，不常驻',
        body: '<div class="sm t2">定位 ' + (c.positioning.coreOriginal ? '已设定' : WB.unknown('未设定')) +
          ' · 场景 ' + list.length + ' 个 · 出场人物 ' + cast.length + ' 人 · 世界引用 ' + worldRefs.length + ' · 伏笔 ' + threads.length + ' · 引用经验 ' + learnings.length + ' 条</div>' +
          (missing.length ? '<div class="t3 xs" style="margin-top:2px">缺口：' + WB.esc(missing.join('、')) + '（缺口不代表不能写）</div>' : ''),
        footer: '<button class="btn sm ghost" data-action="craft.basisDetail" data-chapter="' + ck + '">展开完整依据</button>' });
    }
    return ui.panel({ title: '本次写作依据｜第 ' + (ch.no || '—') + ' 章', sub: '写作前可查；模拟内容标 Mock',
      actions: '<button class="btn sm ghost" data-action="craft.basisDetail" data-chapter="' + ck + '">展开全部依据</button>',
      body:
        '<div class="grid g2">' +
        '<div class="fld"><label>定位核心</label><div class="sm">' + (c.positioning.coreOriginal ? WB.esc(c.positioning.coreOriginal) : WB.unknown('未设定')) + '</div></div>' +
        '<div class="fld"><label>本章章纲目的</label><div class="sm">' + WB.esc((c.outline.filter(function (n) { return chapterForOutline(c, b.id, n) === ck; })[0] || {}).purpose || '（暂无章纲）') + '</div></div>' +
        '<div class="fld"><label>前章结束状态</label><div class="sm">' + (prev ? WB.esc('第 ' + prev.no + ' 章：' + (prev.title || '')) : WB.unknown('本书第一章')) + '</div></div>' +
        '<div class="fld"><label>出场人物（声纹 / 知情）</label><div class="sm">' + (cast.length ? cast.map(function (x) { return WB.esc(x.name) + '（' + WB.esc(x.voice || '声纹待填') + '）'; }).join('；') : WB.unknown('未指定')) + '</div></div>' +
        '<div class="fld"><label>世界约束（引用）</label><div class="sm">' + (worldRefs.length ? worldRefs.map(function (w) { return WB.esc(w.name); }).join('、') : WB.unknown('无')) + '</div></div>' +
        '<div class="fld"><label>伏笔 / 承诺</label><div class="sm">' + (threads.length ? threads.map(function (t) { return WB.esc(t.id) + ' ' + WB.esc(t.state); }).join('；') : WB.unknown('无')) + '</div></div>' +
        '<div class="fld"><label>选用经验 / 参考</label><div class="sm">' + (learnings.length ? learnings.map(function (u) { return WB.esc(u.learningId) + '（准备调整：' + WB.esc(u.adaptation || u.reason || '未记录') + '）'; }).join('；') : WB.unknown('无')) + '</div></div>' +
        '<div class="fld"><label>场景顺序</label><div class="sm">' + (list.length ? list.map(function (s) { return WB.esc(s.id); }).join(' → ') : WB.unknown('未拆场景')) + '</div></div>' +
        '</div>',
      footer: '<span>该检查按需展开；不把整本书与全部聊天都发送。模拟内容标 Mock。</span>' });
  }
  /* 供正文写作面复用：写作依据面板（compact = 只留一行摘要，完整依据走按需展开） */
  WB.craftBasisHtml = function (bookId, ck, opts) {
    var b = WB.book(bookId);
    if (!b) return '';
    return basisPanel(b, WB.craftOf(bookId), ck, opts);
  };

  WB.on['craft.basisDetail'] = function (el, d) {
    var b = curBook(), c = WB.craftOf(b.id), ck = d.chapter;
    var ch = WB.S.chapters[ck] || {};
    WB.openDrawer({ title: '本次写作依据（完整）· 第 ' + (ch.no || '—') + ' 章', sub: '来源 / 版本 / 正式·候选·计划分类',
      wide: true,
      body: '<div class="sm t2">按需展开的检查面：实际使用来源、版本、正式 / 候选 / 计划分类。</div>' +
        '<div class="hr"></div>' +
        '<div class="tl">' +
        (c.outline.filter(function (n) { return chapterForOutline(c, b.id, n) === ck; }).map(function (n) {
          return '<div class="tl-i ok"><div class="tl-t">章纲 · ' + WB.esc(n.title) + '</div><div class="tl-s">' + WB.esc(n.purpose || '') + '<br>' + WB.esc(n.events || '') + '</div></div>';
        }).join('') || '<div class="tl-i"><div class="tl-t">章纲</div><div class="tl-s">尚未提取或填写</div></div>') +
        (c.world.filter(function (w) { return (w.refs || []).length; }).map(function (w) {
          return '<div class="tl-i"><div class="tl-t">世界 · ' + WB.esc(w.name) + '</div><div class="tl-s">' + WB.esc(w.cond || '') + '<br>来源：' + WB.esc(w.source || '') + '</div></div>';
        }).join('')) +
        '</div>' +
        ui.note('bound', '未取得的内容标为缺口，不假装已发送模型；Provider 与用量不在此处冒充。') });
  };
  WB.on['book.storyImpact'] = function (el, d) {
    var c = curCraft();
    var ch = byId(c.characters, d.id);
    WB.openDrawer({ title: '影响检查 · ' + WB.esc(ch ? ch.name : d.id),
      sub: '改人物知情 / 设定后列出受影响项',
      body: '<div class="sm t2">若修改该人物的知情或设定，以下位置需要复核（不是一键全书改写）：</div>' +
        '<div class="tl">' +
        '<div class="tl-i choice"><div class="tl-t">正文引用</div><div class="tl-s">凡出场并依赖该人物知情的章：' +
          WB.esc(bookChapters(curBook().id).filter(function (k) { return (WB.S.manuscripts[k] || {}).paragraphs; }).slice(0, 4).map(function (k) { return '第 ' + WB.S.chapters[k].no + ' 章'; }).join('、') || '（暂无正文）') + '</div></div>' +
        '<div class="tl-i choice"><div class="tl-t">计划与场景</div><div class="tl-s">相关章纲与场景的 reveal / notReveal 需要重新核对</div></div>' +
        '<div class="tl-i"><div class="tl-t">保持不变</div><div class="tl-s">已发布版本与历史正文不改；作者可分批修订</div></div>' +
        '</div>' +
        '<div class="btnrow" style="margin-top:8px"><button class="btn" data-action="nav.view" data-area="book" data-view="review">去审校与质量复查</button>' +
        '<button class="btn ghost" data-action="craft.impactList" data-what="' + WB.esc(ch ? ch.name : '') + '">记录到影响清单</button></div>' });
  };

  /* ================= 审校与质量 ================= */
  function analyze(bookId, chapterKey, kind) {
    var S = WB.S, c = WB.craftOf(bookId), ch = S.chapters[chapterKey] || null;
    var ms = WB.msOf(chapterKey);
    var paras = ms ? ms.paragraphs.slice() : [];
    if (!paras.length && ch) {
      var candOpening = (ch.candidate && S.candidates[ch.candidate] && S.candidates[ch.candidate].opening) || ch.opening;
      if (candOpening) paras = candOpening.slice();
    }
    var joined = paras.join('');
    var F = [], idx = 0;
    function add(o) { idx++; o.id = kind.slice(0, 1).toUpperCase() + idx; F.push(o); }
    if (kind === 'proof') {
      paras.forEach(function (p, i) {
        var n = i + 1;
        var m1 = p.match(/[，。！？；：]{2,}/);
        if (m1) add({ para: n, pos: '第 ' + n + ' 段', quote: m1[0], title: '连续标点', basis: '中文正文中不应出现连续标点',
          impact: '阅读时出现明显停顿，易被当作排版错误', suggestion: '合并为一个标点「' + m1[0].charAt(0) + '」',
          fix: { type: 'text', find: m1[0], repl: m1[0].charAt(0) } });
        var m2 = p.match(/[\u4e00-\u9fa5][,;:!?]/);
        if (m2) { var map = { ',': '，', ';': '；', ':': '：', '!': '！', '?': '？' };
          add({ para: n, pos: '第 ' + n + ' 段', quote: m2[0], title: '半角标点混用', basis: '中文段落内混用半角标点',
            impact: '全篇标点风格不统一', suggestion: '改为全角标点', fix: { type: 'text', find: m2[0], repl: m2[0].charAt(0) + map[m2[0].charAt(1)] } }); }
        var m3 = p.match(/[\u4e00-\u9fa5]\./);
        if (m3) add({ para: n, pos: '第 ' + n + ' 段', quote: m3[0], title: '句号写成半角', basis: '中文句子结尾使用半角句点',
          impact: '标点不统一', suggestion: '改为「。」', fix: { type: 'text', find: m3[0], repl: m3[0].charAt(0) + '。' } });
      });
      if (/三点四十/.test(joined) && /3[:：]40/.test(joined)) add({ pos: '全章', quote: '三点四十 / 3:40', title: '时间写法不一致',
        basis: '同一时间点出现中文与数字两种写法', impact: '同一事实两种表达，读者易混', suggestion: '统一为中文写法「三点四十」', fix: null });
    }
    if (kind === 'style') {
      var headCount = {}; var lastHead = {}, headPara = {};
      paras.forEach(function (p, i) { var h = p.slice(0, 1); headCount[h] = (headCount[h] || 0) + 1; headPara[h] = headPara[h] || i + 1; });
      Object.keys(headCount).forEach(function (h) {
        if (headCount[h] >= 3) add({ para: headPara[h], pos: '全章', quote: '共 ' + headCount[h] + ' 个段落以「' + h + '」开头',
          title: '段落起句重复', basis: '超过 3 个段落以同一字符开头', impact: '段落节奏单一，读起来像列表',
          suggestion: '在连续对白之间插入动作或环境句，打散起句', fix: null });
      });
      ['其实', '非常', '十分', '似乎', '仿佛', '有点', '一些'].forEach(function (w) {
        var cnt = (joined.match(new RegExp(w, 'g')) || []).length;
        if (cnt >= 2) {
          var at = 1; paras.forEach(function (p, i) { if (at === 1 && p.indexOf(w) >= 0) at = i + 1; });
          add({ para: at, pos: '全章', quote: w + ' × ' + cnt, title: '空泛修饰词重复', basis: '同一弱化修饰词在本章多次出现',
            impact: '削弱叙述的确定性', suggestion: '至少删除一处，或替换为具体动作', fix: null });
        }
      });
      var dialogues = paras.filter(function (p) { return /^「/.test(p); });
      if (dialogues.length >= 4) {
        var lens = dialogues.map(function (p) { return p.replace(/[「」]/g, '').length; });
        var avg = lens.reduce(function (a, b) { return a + b; }, 0) / lens.length;
        var spread = Math.max.apply(null, lens) - Math.min.apply(null, lens);
        if (spread <= Math.max(4, avg * 0.5)) add({ pos: '全章', quote: dialogues.length + ' 句对白，长度差异仅 ' + spread + ' 字',
          title: '人物声纹趋同（待核对）', basis: '多角色对白长度高度接近，缺少个体节奏差', impact: '读者可能觉得「大家说话一个样」',
          suggestion: '对照各角色声纹设定，给主要角色增加个体句式', fix: null });
      }
    }
    if (kind === 'review') {
      if (ch && ch.conflict) add({ pos: '全章', quote: ch.conflict.slice(0, 42) + '…', title: '与 Canon 冲突',
        basis: '本章候选与既有 Canon 条目矛盾', impact: '若不处理，连续性会被破坏', suggestion: '改候选，或由作者修订 Canon 并列出受影响章',
        fix: { type: 'link', area: 'book', view: 'story' } });
      var scenes = (c.scenes || {})[chapterKey] || [];
      scenes.forEach(function (sc) {
        if (sc.reveal) { var kw = String(sc.reveal).replace(/[「」]/g, '').slice(0, 4);
          if (kw && paras.length && joined.indexOf(kw) < 0) add({ pos: '全章', quote: '计划揭示：' + sc.reveal, title: '计划要揭示的内容未出现',
            basis: '场景 ' + sc.id + ' 的 reveal 在正文中找不到对应文字', impact: '本章未完成既定信息推进', suggestion: '补写该揭示，或把它移到后续章', fix: null }); }
        if (sc.notReveal) { var kw2 = String(sc.notReveal).replace(/[「」]/g, '').slice(0, 3);
          if (kw2 && joined.indexOf(kw2) >= 0) { var at2 = 1; paras.forEach(function (p, i) { if (at2 === 1 && p.indexOf(kw2) >= 0) at2 = i + 1; });
            add({ para: at2, pos: '第 ' + at2 + ' 段', quote: kw2, title: '提前揭示了本章不应揭示的内容',
              basis: '场景 ' + sc.id + ' 标记 notReveal，但正文出现', impact: '悬念被提前消耗', suggestion: '改为暗示，或删除该处', fix: null }); } }
      });
      var threads = ((S.storyState[bookId] || {}).threads) || [];
      threads.forEach(function (t) {
        if (t.plan && ch && String(t.plan).indexOf('ch' + ch.no) >= 0) {
          var kw3 = String(t.text || '').slice(0, 4);
          if (kw3 && paras.length && joined.indexOf(kw3) < 0) add({ pos: '全章', quote: '伏笔 ' + t.id + ' · ' + t.text, title: '计划兑现的伏笔未落到正文',
            basis: t.id + ' 计划在 ' + t.plan + ' 兑现，但本章未见对应文字', impact: '伏笔兑现窗口被错过', suggestion: '在本章埋设兑现点，或调整计划', fix: null });
        }
      });
    }
    if(kind==='style') WB.reviewRules(bookId).items.filter(function(r){return r.active;}).forEach(function(r){
      if(r.phrase) paras.forEach(function(p,i){if(p.indexOf(r.phrase)>=0)add({para:i+1,pos:'第 '+(i+1)+' 段',quote:r.phrase,title:'本书规则命中：'+r.text,basis:r.type+' · '+r.source,impact:'需作者结合语境判断；不代表平台违规',suggestion:'对照规则与原段落讨论后修改',fix:{type:'link',area:'book',view:'manuscript'}});});
      else add({pos:'全章',title:'待人工／模型核对：'+r.text,basis:r.type+' · '+r.source,impact:'本地演示不能判断这条语义规则是否满足',suggestion:'由作者核对并留理由，或交给审校编辑讨论',fix:{type:'link',area:'book',view:'manuscript'}});
    });
    return F;
  }

  /* 检查对象是「当前草稿」；报告必须记录它检查的是哪个版本（不得用章节 ID 当修订号） */
  function inputVersionOf(chapterKey) {
    var ms = WB.msOf(chapterKey), ch = WB.S.chapters[chapterKey] || {};
    if (!ms) return '（无正文）';
    var r = ms.versions.filter(function (x) { return x.kind === 'draft'; }).length;
    return '草稿 r' + Math.max(r, 1) + (ms.formalVersion ? '｜正式 ' + ms.formalVersion : '｜无正式稿') +
      (ch.published ? '｜线上 ' + ch.published : '｜未发布');
  }
  WB.inputVersionOf = inputVersionOf;
  WB.act.reviewRun = function (bookId, chapterKey, kind, batchId) {
    if(!batchId)return WB.on['review.start'](null,{book:bookId,chapter:chapterKey});
    if((WB.S.__msDraft&&WB.S.__msDraft[chapterKey]!=null)||!(WB.msOf(chapterKey)||{paragraphs:[]}).paragraphs.join('').trim()){WB.toast('先保存非空正文，再检查当前草稿。','warn');return;}
    var findings = analyze(bookId, chapterKey, kind);
    var run = { id: 'RR-' + ((WB.S.reviewRuns || []).length + 1), bookId: bookId, chapter: chapterKey, kind: kind,
      at: WB.now(), batchId:batchId, by: 'E-05', ruleSnapshot: WB.reviewRuleSnapshot(bookId), inputText: (WB.msOf(chapterKey) || {paragraphs:[]}).paragraphs.join('\n'), findings: findings, superseded: null, recheckOf: null,
      inputVersion: inputVersionOf(chapterKey),
      scopeLabel: ({ review: '审稿', proof: '校对', style: '表达质量' })[kind] };
    if (!WB.S.reviewRuns) WB.S.reviewRuns = [];
    WB.S.reviewRuns.unshift(run);
    WB.S.__sel.reviewRun = run.id;
    WB.save();
    return run;
  };
  /* 局部修复：一律只写草稿（工作副本）。正式稿与线上稿是快照，绝不原地覆盖。 */
  WB.act.reviewPatch = function (runId, fid) {
    var run = byId(WB.S.reviewRuns, runId), f = byId(run.findings, fid);
    if (!f) return;
    var ms = WB.msOf(run.chapter), pi = (f.para || 1) - 1;
    if (f.fix && f.fix.type === 'text') {
      if (!ms || ms.paragraphs[pi] == null) { WB.toast('未改动：第 ' + (pi + 1) + ' 段不存在', 'warn'); return; }
      var src = ms.paragraphs[pi];
      if (src.indexOf(f.fix.find) < 0) {
        WB.toast('未改动：该段已不含「' + f.fix.find + '」（可能已被改过）——不假装成功', 'warn');
        return;
      }
      ms.paragraphs[pi] = src.replace(f.fix.find, f.fix.repl);
      ms.updatedAt = WB.now();
      pushDraftVersion(ms, '校对局部修复（第 ' + (pi + 1) + ' 段）');
      f.state = 'patched'; f.patchedAt = WB.now(); f.patchedIn = 'draft';
      WB.toast('已按建议改到草稿（第 ' + (pi + 1) + ' 段）；正式稿 ' +
        (ms.formalVersion || '无') + ' 与线上稿未被覆盖', 'ok');
      WB.rerender(); return;
    }
    if (f.fix && f.fix.type === 'link') {
      WB.go(f.fix.area, f.fix.view, { bookId: run.bookId, chapter:run.chapter, stage:'write' });
      WB.toast('已带到处理入口；具体修改仍需你确认'); return;
    }
    /* 无机械修法：给具体局部改稿候选。文字必须来自本段 + 本条建议，
       不得注入固定句子或他书人物名。 */
    var before = ms && ms.paragraphs[pi] != null ? ms.paragraphs[pi] : '';
    var after;
    if (!before) after = '（编辑起草（演示，需你改写）：' + (f.suggestion || '') + '）';
    else if (/修饰词/.test(f.title)) after = dedupeOnce(before) || null;
    else if (/重复|起句/.test(f.title)) after = shortenOnce(before);
    if (!after) {
      after = before + '\n【编辑起草（演示，需你改写）：' + (f.suggestion || '') + '】';
    }
    addProposal(run.bookId, 'manuscript', run.chapter, 'paragraphs', before, after,
      '针对「' + f.title + '」的局部改稿候选：' + (f.suggestion || ''), { para: f.para || 1, targetLabel: '第 ' + (f.para || 1) + ' 段' });
    f.state = 'proposed'; f.proposedIn = 'draft';
    WB.toast('已生成局部改稿候选（具体文字，来自本段）；确认后只写进草稿', 'ok');
    WB.rerender();
  };
  WB.on['review.ignoreOpen'] = function (el, d) {
    WB.modal({ title: '忽略该问题并留理由',
      body: '<div class="fld"><label>理由（会被记录）</label><textarea class="ta" id="rvReason" rows="3" placeholder="例如：此处重复是有意的复沓；或本轮不改，留待下一版"></textarea></div>' +
        ui.note('bound', '忽略是作者的选择，不是异常；理由会保留在检查记录里，便于复查时对照。'),
      footer: '<button class="btn" data-action="close-modal">取消</button>' +
        '<button class="btn dark" data-action="act.c" data-fn="reviewIgnore" data-a1="' + WB.esc(d.run) + '" data-a2="' + WB.esc(d.fid) + '">忽略并记录</button>' });
  };
  WB.act.reviewIgnore = function (runId, fid) {
    var run = byId(WB.S.reviewRuns, runId), f = byId(run.findings, fid);
    if (f) { f.state = 'ignored'; f.reason = (document.getElementById('rvReason') || {}).value || '（未填写）'; }
    WB.toast('已忽略并记录理由', ''); WB.closeModal(); WB.rerender();
  };
  WB.act.reviewRecheck = function(runId){var run=byId(WB.S.reviewRuns,runId);if(run)WB.on['review.start'](null,{book:run.bookId,chapter:run.chapter});};

  function reviewChips(b, kind, ck) {
    return '<div class="chiprow">' + REVIEW_KINDS.map(function (k) {
      return '<button class="chip' + (k[0] === kind ? ' on' : '') + '" data-action="book.reviewKind" data-book="' + b.id + '" data-kind="' + k[0] + '" data-chapter="' + (ck || '') + '">' + WB.esc(k[1]) + '</button>';
    }).join('') + '</div>';
  }
  WB.register('book.review', {
    render: function (ctx) {
      var b = curBook(), c = curCraft();
      var chs = bookChapters(b.id);
      var kind = (ctx.params && ctx.params.kind) || 'review';
      if (!chs.length) {
        return ui.hdr('审校与质量 · ' + WB.esc(b.title), '审稿 / 校对 / 表达质量分别可触发，问题带位置与证据。',
            '<button class="btn" data-action="nav.view" data-area="book" data-view="manuscript">去写正文</button>', '') +
          ui.panel({ title: '审校与质量', body: ui.empty('本书还没有正文', '先在正文写作中写出内容，再发起审稿 / 校对 / 表达质量检查。') });
      }
      var ck = (ctx.params && ctx.params.chapter) || WB.S.__sel.reviewChap || chs[0];
      if (!WB.S.chapters[ck] || WB.S.chapters[ck].bookId !== b.id) ck = chs[0];
      WB.S.__sel.reviewChap = ck;
      var ch = WB.S.chapters[ck];
      var chipRow = '<div class="chiprow">' + chs.map(function (k) {
        return '<button class="chip' + (k === ck ? ' on' : '') + '" data-action="book.reviewChap" data-book="' + b.id + '" data-kind="' + kind + '" data-chapter="' + k + '">第 ' + WB.S.chapters[k].no + ' 章</button>';
      }).join('') + '</div>';
      var runs = (WB.S.reviewRuns || []).filter(function (r) { return r.bookId === b.id && r.chapter === ck && r.kind === kind; });
      if(ctx.params.batchId)runs=runs.filter(function(r){return r.batchId===ctx.params.batchId;});
      var cur = runs.filter(function (r) { return byId(WB.S.reviewRuns, WB.S.__sel.reviewRun) === r; })[0] || runs[0];
      var kindHint = { review: '审稿：情节推进、冲突与人物动机、结构节奏、承诺兑现、连续性、世界规则与信息泄露。',
        proof: '校对：错别字、标点、称谓、数字与时间、前后一致。默认不改变作者表达，可逐项接受或忽略。',
        style: '表达与风格：重复句式、解释性旁白、机械转折、人物声纹趋同、空泛修饰。不提供检测规避，也不虚构「去AI率」。' }[kind];

      var findingsHtml = '';
      if (cur) {
        if (!cur.findings.length) {
          findingsHtml = ui.note('info', '本次<b>未发现带证据的问题</b>。无问题不强制改稿；这也是正常结果。');
        } else {
          findingsHtml = cur.findings.map(function (f) {
            var st = ({ open: ['待处理', 'choice'], patched: ['已修改待复查', 'wait'], proposed: ['已生成候选待确认', 'choice'],
              ignored: ['作者保留', 'unknown'], rechecked: ['已复查（不再出现）', 'published'], still: ['复查后仍存在', 'rejected'] })[f.state] || ['待处理', 'choice'];
            return '<div class="pnl" style="margin-bottom:8px"><div class="pnl-h"><div class="pnl-t">' + WB.esc(f.pos) + ' · ' + WB.esc(f.title) + '</div>' +
              '<div class="pnl-a">' + WB.stBadge(st[0], st[1]) + '</div></div><div class="pnl-body">' +
              (f.quote ? '<div class="cl-q" style="margin-bottom:6px">' + WB.esc(f.quote) + '</div>' : '') +
              '<div class="grid g2"><div class="fld"><label>依据</label><div class="sm">' + WB.esc(f.basis) + '</div></div>' +
              '<div class="fld"><label>影响</label><div class="sm">' + WB.esc(f.impact) + '</div></div></div>' +
              '<div class="sm t2" style="margin-top:4px">建议：' + WB.esc(f.suggestion) + '</div>' +
              (f.reason ? '<div class="sm t3">忽略理由：' + WB.esc(f.reason) + '</div>' : '') +
              '<div class="btnrow" style="margin-top:6px">' +
              (f.state === 'ignored' ? '' :
                '<button class="btn sm primary" data-action="act.c" data-fn="reviewPatch" data-a1="' + cur.id + '" data-a2="' + f.id + '">' +
                  (f.fix && f.fix.type === 'link' ? '去处理入口' : f.fix && f.fix.type === 'text' ? '按建议修改' : '生成局部改稿候选') + '</button>' +
                '<button class="btn sm" data-action="review.ignoreOpen" data-run="' + cur.id + '" data-fid="' + f.id + '">忽略并留理由</button>') +
              (ctx.params.linear ? '' : '<button class="btn sm ghost" data-action="act.c" data-fn="reviewRecheck" data-a1="' + cur.id + '">重新审稿</button>') +
              '</div></div></div>';
          }).join('');
        }
      } else {
        findingsHtml = ui.empty('尚未发起本次检查', '选择章节与检查类型后点击「发起检查」；结果会带位置与证据，且可复查。');
      }
      var hist = runs.length > 1 ? ui.panel({ title: '检查历史', sub: runs.length + ' 次',
        body: '<div class="tl">' + runs.slice(0, 6).map(function (r) {
          return '<div class="tl-i ' + (r.id === (cur && cur.id) ? 'ok' : '') + '"><div class="tl-t">' + WB.esc(r.scopeLabel) + ' · ' + WB.esc(r.at) +
            (r.recheckOf ? ' ' + WB.stBadge('复查', 'wait') : '') + (r.superseded ? ' ' + WB.stBadge('已被新版本取代', 'unknown') : '') + '</div>' +
            '<div class="tl-s">' + r.findings.length + ' 处问题 · 输入版本：' + WB.esc(r.inputVersion || inputVersionOf(r.chapter)) + '</div></div>';
        }).join('') + '</div>' }) : '';

      return (ctx.params.linear ? '' : '<div class="review-toolbar">' + reviewChips(b, kind, ck) +
        '<button class="btn" data-action="act.c" data-fn="reviewRun" data-a1="' + b.id + '" data-a2="' + ck + '" data-a3="' + kind + '">' + (cur ? '重新检查' : '检查这一项') + '</button></div>') +
        '<p class="review-hint">' + WB.esc(kindHint) + '</p>' +
        (cur && (cur.ruleSnapshot !== WB.reviewRuleSnapshot(b.id) || cur.inputText !== (WB.msOf(ck) || {paragraphs:[]}).paragraphs.join('\n')) ? ui.note('choice', '正文或规则已改变，或旧报告缺少版本依据，请重新检查当前草稿。') : '') +
        (cur ? '<p class="quiet-copy">检查人：'+WB.esc((WB.emp(cur.by)||{}).name||cur.by)+' · 输入：'+WB.esc(cur.inputVersion||'旧记录')+'</p><details><summary>本次规则依据</summary><pre style="white-space:pre-wrap">'+WB.esc(cur.ruleSnapshot?(JSON.parse(cur.ruleSnapshot).standards||[]).concat(JSON.parse(cur.ruleSnapshot).items).map(function(x){return x.text+' · '+x.type+' · '+x.source;}).join('\n')||'无自定义规则':'旧记录未保存规则依据')+'</pre></details>' : '') + '<div class="review-results">' + findingsHtml + openProposals(b.id, 'manuscript', ck).map(proposalCard).join('') + '</div>' +
        (hist ? '<details class="flow-details"><summary>历史检查</summary>' + hist + '</details>' : '');
    },
    aside: function () {
      var b = curBook();
      var runs = (WB.S.reviewRuns || []).filter(function (r) { return r.bookId === b.id; });
      return WB.asBlock('责任人', WB.ownerHtml('E-05') +
          '<div class="sm t3" style="margin-top:6px">许清禾独立审校；沈知远负责创作与修改，作者确认定稿。</div>') +
        WB.asBlock('本书检查记录（' + runs.length + '）',
          runs.length ? runs.slice(0, 4).map(function (r) {
            return '<div class="as-w"><div class="wt">' + WB.esc(r.scopeLabel) + '</div><div class="ws">' + WB.esc(r.chapter) + ' · ' + r.findings.length + ' 处</div></div>';
          }).join('') : '<div class="sm t3">尚无检查记录。</div>') +
        WB.asBlock('边界', '<div class="sm t2">· 审校 Result ≠ 作者决定<br>· 无证据不自动改稿<br>· 不做规避检测 / 不虚构去 AI 率</div>');
    }
  });

  /* ================= 旧稿接续 ================= */
  var IMP_KINDS = [['manuscript', '正文'], ['outline', '大纲'], ['setting', '设定'], ['reference', '参考'], ['ignore', '忽略']];
  WB.on['imp.example'] = function () { WB.act.impLoad(true); };
  WB.on['imp.classify'] = function (el, d) {
    /* 框架的 change 派发只给 {value, id}（来自 data-id），没有 row —— 必须按 id 取行，
       否则下拉改了但分类不动（真实浏览器测出的缺陷）。 */
    var row = byId(WB.S.__sel.impRows || [], d.id || d.row);
    if (!row) return;
    row.kind = d.value;
    row.kindEditedBy = 'author';   /* 作者手工修正过的分类，导入记录里可区分 */
    WB.save(); WB.render();
  };
  WB.act.impLoad = function (useExample) {
    var b = curBook();
    var text = useExample
      ? '第一章 潮信\n夜深了，渡口的灯一盏盏灭下去。\n\n第二章 归舟\n第二年春天，信才寄到。\n\n大纲：全书双线，每卷收束一条线。\n\n设定：渡口在一九三七年冬被炸毁。'
      : ((document.getElementById('impText') || {}).value || '');
    if (!text.trim()) { WB.toast('请粘贴自有测试文本，或点「载入示例文本」', 'warn'); return; }
    /* 真实解析：按「第N章」切分正文，其余行按关键词粗分类（理由 + 置信度可见、可改） */
    var lines = text.split(/\n+/).map(function (s) { return s.trim(); }).filter(Boolean);
    var rows = [], cur = null, body = [];
    function flush() { if (cur) { cur.preview = body.slice(0, 2).join(' '); cur.words = body.join('').length; rows.push(cur); } cur = null; body = []; }
    lines.forEach(function (ln) {
      var m = /^第\s*([0-9一二三四五六七八九十]+)\s*章\s*(.*)$/.exec(ln);
      if (m) { flush(); cur = { id: 'IR-' + (rows.length + 1), title: ln.slice(0, 24), no: m[1], kind: 'manuscript', conf: 0.94, reason: '以「第N章」开头 → 正文' }; return; }
      if (/^(大纲|总纲|卷纲)/.test(ln)) { flush(); rows.push({ id: 'IR-' + (rows.length + 1), title: ln.slice(0, 24), kind: 'outline', conf: 0.62, reason: '含大纲关键词 → 大纲（待确认）' }); return; }
      if (/^(设定|规则|人物|地点)/.test(ln)) { flush(); rows.push({ id: 'IR-' + (rows.length + 1), title: ln.slice(0, 24), kind: 'setting', conf: 0.5, reason: '含设定关键词 → 设定（待确认）' }); return; }
      if (cur) body.push(ln); else rows.push({ id: 'IR-' + (rows.length + 1), title: ln.slice(0, 24), kind: 'ignore', conf: 0.3, reason: '未识别 → 忽略（可改）' });
    });
    flush();
    WB.S.__sel.impRows = rows;
    WB.S.__sel.impSource = useExample ? '示例文本（自有测试稿，虚构）' : '粘贴文本';
    WB.save();
    WB.toast('已解析 ' + rows.length + ' 段：分类理由与置信度可见、可修改', 'ok');
    WB.render();
  };
  WB.act.impConfirm = function () {
    var b = curBook(), rows = WB.S.__sel.impRows || [];
    if (!rows.length) { WB.toast('先解析文本', 'warn'); return; }
    var c = WB.craftOf(b.id);
    var ms = rows.filter(function (r) { return r.kind === 'manuscript'; });
    var created = 0;
    ms.forEach(function (r) {
      var no = Number(String(r.no).replace(/[^0-9]/g, '')) || 0;
      if (!no) no = Object.keys(WB.S.chapters).filter(function (k) { return WB.S.chapters[k].bookId === b.id; }).length + 1;
      var key = 'ch-' + b.id + '-' + no;
      if (!WB.S.chapters[key]) {
        if (!WB.S.volumes[b.id]) WB.S.volumes[b.id] = [{ id: 'V-01', name: '卷一 · 导入', chapters: ['ch1', 'ch1'], open: true }];
        WB.S.chapters[key] = { bookId: b.id, vol: WB.S.volumes[b.id][0].id, no: no, title: r.title.replace(/^第\s*[0-9一二三四五六七八九十]+\s*章\s*/, '') || '导入章',
          formal: null, published: null, candidate: null, state: 'draft', createdAt: WB.now(), authoredBy: 'author', imported: true };
        WB.S.manuscripts[key] = { bookId: b.id, no: no, title: r.title, versions: [{ v: 'v1', at: WB.now(), note: '由旧稿导入（草稿，未确认）' }],
          formalVersion: null, paragraphs: [r.preview || '（导入正文）'] };
        created++;
      }
    });
    b.publishedCount = b.publishedCount || 0;
    b.volumeCount = (WB.S.volumes[b.id] || []).length;
    c.importRecords.push({ id: 'IMP-' + (c.importRecords.length + 1), at: WB.now(), fileName: WB.S.__sel.impSource || '粘贴文本',
      chars: rows.reduce(function (a, r) { return a + (r.words || 0); }, 0), classes: IMP_KINDS.map(function (k) {
        return { kind: k[1], count: rows.filter(function (r) { return r.kind === k[0]; }).length };
      }).filter(function (x) { return x.count; }), state: 'confirmed',
      note: '导入只登记已分类内容；未确认分类不进入正式正文或 Canon。' });
    WB.S.__sel.impRows = null;
    WB.save();
    WB.toast('已写入：新建 ' + created + ' 章草稿（导入，未确认）；其余分类已登记', 'ok');
    WB.render();
  };
  WB.act.impExtract = function () {
    var b = curBook(), c = WB.craftOf(b.id);
    var names = c.characters.map(function (x) { return x.name; });
    var cands = [];
    var allText = Object.keys(WB.S.manuscripts).filter(function (k) { return WB.S.manuscripts[k].bookId === b.id; })
      .map(function (k) { return WB.S.manuscripts[k].paragraphs.join(''); }).join('');
    ['沈砚秋', '陆沉', '林砚', '顾晚', '老周', '闻笙'].forEach(function (n) {
      if (allText.indexOf(n) >= 0 && names.indexOf(n) < 0) cands.push({ kind: 'character', text: '人物 · ' + n, after: n, field: 'name' });
    });
    if (!cands.length) { WB.toast('未从已导入正文中抽取到新设定候选（不凭空生成）', ''); return; }
    cands.forEach(function (x) {
      addProposal(b.id, 'character', 'NEW-' + x.after, x.field, '', x.after,
        '导入时从正文实体抽取（AI 推断，待作者确认）；未确认不得进入 Canon。', { targetLabel: x.text });
    });
    WB.toast('已抽取 ' + cands.length + ' 条设定候选，等待确认（未确认为推断）', 'ok');
    WB.render();
  };
  WB.register('book.import', {
    render: function () {
      var b = curBook(), c = curCraft();
      var rows = WB.S.__sel.impRows;
      var stepPanel;
      if (!rows) {
        stepPanel = ui.panel({ title: '第 1 步 · 选择文本', sub: '自有或获授权的测试稿',
          body: '<div class="fld" style="margin-bottom:8px"><label>粘贴自有测试文本（不会外发）</label>' +
            '<textarea class="ta" id="impText" rows="6" placeholder="例如：&#10;第一章 潮信&#10;夜深了，渡口的灯一盏盏灭下去。"></textarea></div>' +
            ui.note('bound', '只导入自有或获授权全文；不绕付费与 DRM，不默认整本下载。未确认分类不进入正式正文或 Canon。') +
            '<div class="btnrow" style="margin-top:8px"><button class="btn" data-action="imp.example">载入示例文本</button>' +
            '<button class="btn primary" data-action="act.c" data-fn="impLoad" data-a1="false">解析文本</button></div>' });
      } else {
        var tableRows = rows.map(function (r) {
          var opts = IMP_KINDS.map(function (k) {
            return '<option value="' + k[0] + '"' + (r.kind === k[0] ? ' selected' : '') + '>' + k[1] + '</option>';
          }).join('');
          return { attrs: ' data-id="' + r.id + '"', cells: [
            WB.esc(r.title),
            '<select class="sel" data-change="imp.classify" data-id="' + r.id + '">' + opts + '</select>',
            '<span class="sm">' + Math.round((r.conf || 0) * 100) + '%</span>',
            '<span class="sm t3">' + WB.esc(r.reason) + '</span>' ] };
        });
        stepPanel = ui.panel({ title: '第 2 步 · 预览分类与卷章归属', sub: rows.length + ' 段',
          body: '<div class="sm t2" style="margin-bottom:6px">分类理由与置信度可见，可逐行修正；重复导入会区分新增/替换/保留。</div>' +
            ui.tbl(['识别到的段落', '分类（可改）', '置信度', '分类理由'], tableRows),
          actions: '<button class="btn sm primary" data-action="act.c" data-fn="impConfirm">确认写入</button>' +
            '<button class="btn sm ghost" data-action="act.c" data-fn="impLoad" data-a1="false">重新解析</button>',
          footer: '<span>确认后：正文以「草稿」写入（不是正式稿）；设定/大纲记为候选。</span>' }) +
          ui.panel({ title: '第 3 步 · 抽取设定候选', body:
            '<div class="sm t2">从已导入正文抽取人物 / 设定候选，标记为「AI 推断，待确认」，不自动写入 Canon。</div>' +
            '<div class="btnrow" style="margin-top:8px"><button class="btn" data-action="act.c" data-fn="impExtract">抽取设定候选</button>' +
            '<button class="btn ghost" data-action="nav.view" data-area="book" data-view="manuscript">去正文接续</button></div>' });
      }
      var histRows = c.importRecords.length ? c.importRecords.map(function (r) {
        return { cells: [WB.esc(r.id), WB.esc(r.fileName), String(r.chars || 0) + ' 字',
          (r.classes || []).map(function (x) { return WB.esc(x.kind) + '×' + x.count; }).join('、'), WB.stBadge('已确认', 'published')] };
      }) : [{ cells: ['—', WB.unknown('尚无导入记录'), '—', '—', '—'] }];
      return ui.hdr('旧稿接续 · ' + WB.esc(b.title),
        '导入自有文本 → 预览分类与卷章 → 确认写入（草稿）→ 抽取设定候选（推断待确认）→ 继续同书同章。',
        '<button class="btn" data-action="nav.view" data-area="book" data-view="manuscript">去正文</button>',
        '<span>作品 ' + WB.esc(b.id) + '</span><span class="t4">|</span><span>未确认分类不进正文 / Canon</span>') +
        stepPanel +
        ui.panel({ title: '导入历史', tight: true, body: ui.tbl(['记录', '来源文件', '规模', '分类', '状态'], histRows),
          footer: '<span>重复导入时区分新增 / 替换 / 保留；失败可重试且不重复覆盖。</span>' });
    },
    aside: function () {
      var b = curBook();
      return WB.asBlock('导入边界', '<div class="sm t2">· 只导入自有 / 获授权全文<br>· 链接与元数据只作分析引用<br>· 不按书名自动匹配既有书<br>· 原文件与导入结果建立证据映射</div>') +
        WB.asBlock('责任人', WB.ownerHtml('E-05'));
    }
  });

  /* ============================================================================
     新书起步（D05 / 作者动线）
     开书不是「建一张空卡」：起步是一段能继续、能中断、能回来的创作过程。
     任何一步都能跳过；「下一步」从本书真实资料推导（WB.onbState），不存死状态，
     所以中断后回来会自然接着做，也不会反复新建书。
     本书编辑（R3）嵌在起步区本身，走的是与共享工作区完全相同的链路，不是页尾聊天。
     ========================================================================== */
  function onbDirProps(bookId) {
    var props = WB.S.discussProps || {};
    return Object.keys(props).map(function (k) { return props[k]; }).filter(function (p) {
      return p && p.kind === 'dir' && p.target && p.target.bookId === bookId;
    });
  }
  function onbOpenDirCount(bookId) {
    return onbDirProps(bookId).filter(function (p) {
      return (p.items || []).some(function (x) { return x.applied == null; });
    }).length;
  }
  function onbChip(text, cls) {
    return '<span class="onb-chip' + (cls ? ' ' + cls : '') + '">' + WB.esc(text) + '</span>';
  }
  function onbEditorLine(step, extra) {
    return '<div class="onb-who">' + WB.ownerHtml('E-01') +
      '<span class="sm t3">本书编辑 · 负责本书定位 / 方向 / 大纲 / 草稿与候选</span></div>' +
      '<div class="sm t2" style="margin-top:4px">' + WB.esc(step.hint || '') + '</div>' +
      (extra ? '<div class="sm t3" style="margin-top:4px">' + extra + '</div>' : '');
  }

  /* 起步区：面板本体（由 book.overview 首屏调用） */
  WB.onbPanel = function (b, c) {
    var st = WB.onbState(b.id);
    var steps = WB.onbSteps() || [];
    var o = WB.onbOf(b.id) || {};
    /* 既有作品（不是本次开出来的书）不显示起步块：避免给成熟作品堆无关摘要。
       只有「开书时真的走过起步」的书才保留这个入口 —— 因为起步可以中断、可以回来补。 */
    if (st.done && !o.created) return '';
    if (st.done) {
      /* 起步已完成：不占版面，只留「到哪一步」+ 随时可回来补的入口（跳过 ≠ 缺失） */
      return ui.panel({ title: '起步已完成 · 随时可以回来补', sub: '任意一步都能回头做；下面的入口与当时起步区是同一套链路',
        body: '<div class="sm t2">' + onbChip('方向：' + (c.positioning.dirName || '未选（可以随时补）')) +
          onbChip('设定 ' + ((c.world || []).length + (c.characters || []).length) + ' 条') +
          onbChip('大纲 ' + ((c.outline || []).length) + ' 节点') +
          onbChip('在册 ' + st.chapters + ' 章') + '</div>' +
          '<div class="btnrow" style="margin-top:8px">' +
          '<button class="btn sm primary" data-action="book.continue" data-id="' + b.id + '">继续当前章</button>' +
          '<button class="btn sm" data-action="book.onbDir" data-book="' + b.id + '">再谈一次方向</button>' +
          '<button class="btn sm" data-action="book.onbBase" data-book="' + b.id + '">让编辑补一条设定</button>' +
          '<button class="btn sm" data-action="book.onbPlan" data-book="' + b.id + '">让编辑给走向</button>' +
          '<button class="btn sm ghost" data-action="book.onbOpenConv" data-book="' + b.id + '">打开与编辑的共享工作区</button>' +
          '</div>' });
    }
    var step = st.step || steps[0];
    var seedRaw = c.positioning.seedRaw || '';
    var seed = c.positioning.seed || '';
    var dirProps = onbDirProps(b.id);
    var openDirs = onbOpenDirCount(b.id);
    var dirCount = (WB.startDirections() || []).length;

    var ladder = '<div class="onb-ladder">' + steps.map(function (s, i) {
      var cls = i < st.idx ? 'done' : (i === st.idx ? 'cur' : 'todo');
      return '<span class="onb-step ' + cls + '">' + (i < st.idx ? '✓ ' : (i === st.idx ? '▸ ' : '')) + WB.esc(s.name) + '</span>';
    }).join('<span class="onb-arrow">→</span>') + '</div>' +
      '<div class="sm t3" style="margin-top:4px">顺序是建议不是门禁：任何一步都能跳过，未填不会阻止你写正文。</div>';

    var seedBlock = seedRaw
      ? '<div class="fld"><label>你的原话（已存进本书，编辑据此提方向）</label>' +
        '<div class="onb-quote">' + WB.esc(seedRaw) + '</div></div>'
      : '';

    var actBody = '';
    if (step.id === 'idea') {
      actBody =
        '<div class="fld"><label>写下一两句你的想法</label>' +
        '<textarea class="ta" id="onbSeed" rows="3" placeholder="例如：一个档案员每天收到印着明天日期的报纸。">' +
        WB.esc(seedRaw || seed) + '</textarea></div>' +
        '<div class="btnrow">' +
        '<button class="btn primary" data-action="book.onbSeed" data-book="' + b.id + '">发给编辑，请它给方向</button>' +
        '<button class="btn" data-action="book.onbSkipIdea" data-book="' + b.id + '">先不写想法，直接手写第一章</button>' +
        '</div>' +
        '<div class="sm t3" style="margin-top:6px">编辑会从你的原话里给 2–3 条方向，每条含<b>具体故事前提 / 主要冲突 / 视角 / 为什么贴你的构思 / 代价</b>。' +
        '选不选都行：不用先定读者、题材、平台，也不用先填完整套设定。</div>';
    } else if (step.id === 'dir') {
      actBody =
        '<div class="sm t2">' + (openDirs
          ? '编辑已经按你的构思给出方向候选，正在共享工作区等你逐条决定（用这个方向 / 不用这个 / 改后再采纳）。'
          : '你的构思已经存进本书。现在让编辑按它给方向候选。') + '</div>' +
        '<div class="btnrow" style="margin-top:8px">' +
        '<button class="btn primary" data-action="book.onbDir" data-book="' + b.id + '">' +
        (openDirs ? '去看编辑给的方向候选' : '让编辑给方向候选') + '</button>' +
        (openDirs ? '<button class="btn" data-action="book.onbJumpConv">跳到共享工作区</button>' : '') +
        '<button class="btn ghost" data-action="book.craftGo" data-book="' + b.id + '" data-mode="positioning">我自己写一句话故事</button>' +
        '</div>' +
        '<div class="sm t3" style="margin-top:6px">候选有 ' + dirCount + ' 条模板，编辑按你的原话挑最贴的 ' + Math.min(2, dirCount) + ' 条；' +
        '一条都贴不上时会全部列出并说明——不会硬凑。</div>';
    } else if (step.id === 'base') {
      actBody =
        '<div class="sm t2">只补这一章真的会用到的：一条背景规则（含代价与限制）、一个人物档案、一条主线。其余留到写作中探索。</div>' +
        '<div class="btnrow" style="margin-top:8px">' +
        '<button class="btn primary" data-action="book.onbBase" data-book="' + b.id + '">让编辑补这几项（先给候选）</button>' +
        '<button class="btn" data-action="book.craftGo" data-book="' + b.id + '" data-mode="characters">我自己建人物</button>' +
        '<button class="btn" data-action="book.craftGo" data-book="' + b.id + '" data-mode="world">我自己写背景规则</button>' +
        '</div>';
    } else if (step.id === 'plan') {
      actBody =
        '<div class="sm t2">可以从主支线起步，也可以跳过规划直接准备第一章——跳过不等于缺失。</div>' +
        '<div class="btnrow" style="margin-top:8px">' +
        '<button class="btn primary" data-action="book.onbPlan" data-book="' + b.id + '">让编辑给主支线与第 1 章段纲</button>' +
        '<button class="btn" data-action="book.onbSkipPlan" data-book="' + b.id + '">跳过规划，直接准备第一章</button>' +
        '</div>';
    } else {
      actBody =
        '<div class="sm t2">先试一个开头：结果会进草稿与候选，你要逐项采纳；<b>生成 ≠ 定稿 ≠ 发布</b>。</div>' +
        '<div class="btnrow" style="margin-top:8px">' +
        '<button class="btn primary" data-action="book.onbFirst" data-book="' + b.id + '">让编辑准备第 1 章候选</button>' +
        '<button class="btn" data-action="act.b" data-fn="newChapter" data-a1="' + b.id + '">我自己手写第一章</button>' +
        '</div>';
    }

    var stateBits = [];
    if (c.world.length || c.characters.length || c.outline.length) {
      stateBits.push(onbChip('世界 ' + c.world.length));
      stateBits.push(onbChip('人物 ' + c.characters.length));
      stateBits.push(onbChip('大纲 ' + c.outline.length));
      stateBits.push(onbChip('主支线 ' + (((c.arc || {}).mainLines || []).length)));
    }
    if (dirProps.length) stateBits.push(onbChip('方向候选 ' + dirProps.length + ' 组', openDirs ? 'wait' : 'ok'));
    if (o.planSkipped) stateBits.push(onbChip('规划已跳过（可回来补）'));

    return ui.panel({ title: '这本书还在起步 · 下一步：' + WB.esc(step.name),
      sub: '开书是一段可继续的过程，不是一张空卡：可以中断、可以回来，也可以整段跳过。',
      body: ladder +
        '<div class="hr"></div>' +
        '<div class="onb-card">' + onbEditorLine(step,
          (o.path ? '起步方式：' + ({ idea: '从一句想法开始', import: '导入旧稿', write: '先手写' }[o.path] || o.path) : '')) +
          '<div style="margin-top:10px">' + actBody + '</div>' +
        '</div>' +
        (seedBlock ? '<div class="hr"></div>' + seedBlock : '') +
        (stateBits.length ? '<div class="hr"></div><div class="sm t2">' + stateBits.join('') + '</div>' : '') +
        '<div class="btnrow" style="margin-top:10px">' +
        '<button class="btn sm ghost" data-action="book.onbOpenConv" data-book="' + b.id + '">打开与编辑的共享工作区</button>' +
        '<button class="btn sm ghost" data-action="book.onbSkipIdea" data-book="' + b.id + '">先不看这些，直接手写第一章</button>' +
        '</div>' });
  };

  /* ---- 起步区行动：全部走 WB.convAsk（同一条员工链路，不另造聊天） ---- */
  WB.on['book.onbSeed'] = function (elm, d) {
    var b = WB.book(d.book) || WB.scopeBook();
    var inp = document.getElementById('onbSeed');
    var txt = inp && inp.value ? inp.value.trim() : '';
    if (!txt) {
      WB.toast('先写一两句你的想法；如果已经知道要写什么，也可以直接手写第一章', 'warn');
      if (inp && inp.focus) inp.focus();
      return;
    }
    WB.convAsk('E-01', b.id, txt, { objLabel: '本书构思与方向 · ' + b.title, force: 'direction', rerender: true });
  };
  WB.on['book.onbDir'] = function (elm, d) {
    var b = WB.book(d.book) || WB.scopeBook();
    var c = WB.craftOf(b.id);
    var seeds = c.positioning.seedRaw || c.positioning.seed;
    if (!seeds) { WB.toast('还没有你的构思，编辑没有可依据的东西——先写一句想法', 'warn'); return; }
    if (onbOpenDirCount(b.id)) {
      /* 已有待决定的方向候选：直接打开，不重复问一遍（避免堆提案） */
      WB.openConv('E-01', b.id, '本书构思与方向 · ' + b.title);
      WB.toast('编辑给的方向候选还在共享工作区里等你逐条决定', 'ok');
      return;
    }
    WB.convAsk('E-01', b.id, seeds, { objLabel: '本书构思与方向 · ' + b.title, force: 'direction', rerender: true });
  };
  WB.on['book.onbBase'] = function (elm, d) {
    var b = WB.book(d.book) || WB.scopeBook();
    WB.convAsk('E-01', b.id, '这本书会用到哪些设定？只补我这一章真的要用的。',
      { objLabel: '本书要用的少量设定 · ' + b.title, force: 'base', rerender: true });
  };
  WB.on['book.onbPlan'] = function (elm, d) {
    var b = WB.book(d.book) || WB.scopeBook();
    WB.convAsk('E-01', b.id, '这本书的走向怎么定？给我主支线和第 1 章的段纲。',
      { objLabel: '本书走向 · ' + b.title, force: 'plan', rerender: true });
  };
  WB.on['book.onbSkipPlan'] = function (elm, d) {
    var b = WB.book(d.book) || WB.scopeBook();
    var o = WB.onbOf(b.id);
    if (o) { o.planSkipped = true; o.updatedAt = WB.now(); }
    WB.save(); WB.render();
    WB.toast('已跳过规划：跳过不等于缺失，随时可以回来补主支线或大纲', 'ok');
  };
  WB.on['book.onbSkipIdea'] = function (elm, d) {
    var b = WB.book(d.book) || WB.scopeBook();
    var o = WB.onbOf(b.id); if (o) o.updatedAt = WB.now();
    WB.toast('跳过构思：直接开第 1 章手写。定位与方向随时可以回来补', 'ok');
    WB.act.newChapter(b.id);
  };
  WB.on['book.onbOpenConv'] = function (elm, d) {
    var b = WB.book(d.book) || WB.scopeBook();
    WB.openConv('E-01', b.id, '本书构思与方向 · ' + b.title);
  };
  WB.on['book.onbJumpConv'] = function () {
    var n = document.getElementById('sharedArea');
    if (n && n.scrollIntoView) n.scrollIntoView({ block: 'start', behavior: 'smooth' });
  };

  /* 起点 · 拿到第一章候选：建第 1 章（草稿）→ 按本书构思与方向生成候选段落。
     候选只用于逐项裁决；采纳后仍需作者确认才成为正式稿，发布再走一次流程。 */
  WB.on['book.onbFirst'] = function (elm, d) {
    var S = WB.S;
    var b = WB.book(d.book) || WB.scopeBook();
    var c = WB.craftOf(b.id);
    var own = ownMaterial(c);
    var premise = own.premise || own.seed;
    if (!premise) { WB.toast('先写一句构思或采用一个方向，我才有依据准备第一章（不凭空编）', 'warn'); return; }
    var chs = Object.keys(S.chapters).filter(function (k) { return S.chapters[k].bookId === b.id; })
      .sort(function (x, y) { return (S.chapters[x].no || 0) - (S.chapters[y].no || 0); });
    var ck = chs.length ? chs[0] : null;
    if (!ck) { WB.act.newChapter(b.id); chs = Object.keys(S.chapters).filter(function (k) { return S.chapters[k].bookId === b.id; })
      .sort(function (x, y) { return (S.chapters[x].no || 0) - (S.chapters[y].no || 0); }); ck = chs[0]; }
    var ch = S.chapters[ck];
    var ms = WB.msOf(ck) || WB.msEnsure(ck, b.id, '第 ' + ch.no + ' 章' + (ch.title ? ' · ' + ch.title : ''));
    var dir = (WB.startDirections() || []).filter(function (x) { return x.id === c.positioning.dirId; })[0] || null;
    var cast = (c.characters || []).map(function (x) { return x.name; }).join('、') || '（本书还没建人物）';
    var skel = [
      '（候选 · 编辑起草，需你改写成正文语言）开场：把故事前提摆成一个具体动作 —— ' + String(premise).slice(0, 40),
      '（候选 · 编辑起草，需你改写）第一次显形：让代价或冲突在读者面前发生一次。' +
        (c.arc && c.arc.mainConflict ? '本书主要冲突：' + String(c.arc.mainConflict).slice(0, 40) : '（主要冲突待你确定）'),
      '（候选 · 编辑起草，需你改写）章末：留一个必须翻页的问题；本段只推进一件事，不要提前揭示。' +
        '出场只用本书已建人物：' + cast + '。'
    ];
    var changes = skel.map(function (txt, i) {
      return { id: 'F' + (i + 1), label: '第 1 章第 ' + (i + 1) + ' 段 · 段骨架', why: '依据本书构思' +
          (dir ? '与已采用的方向「' + dir.name + '」' : '') + '；只给结构，不给成稿文字。',
        before: null, after: txt, applied: null, para: i + 1 };
    });
    var cid = 'C-' + ch.no + 'F';
    S.candidates[cid] = { id: cid, bookId: b.id, chapter: ck, baseVersion: ms.formalVersion,
      kind: '第 1 章候选（按本书构思与方向）', title: '第 ' + ch.no + ' 章 · 首章候选', createdAt: WB.now(), by: 'E-01',
      rationale: '按本书构思' + (dir ? '与方向「' + dir.name + '」' : '') + '生成 ' + changes.length + ' 段骨架（演示）；逐项可采纳 / 拒绝，确认后写入正文。',
      refs: dir ? [dir.id] : [], changes: changes };
    ch.candidate = cid;
    if (!ch.state || ch.state === 'outline') ch.state = 'candidate';
    var o = WB.onbOf(b.id); if (o) o.updatedAt = WB.now();
    WB.save();
    WB.toast('已生成第 ' + ch.no + ' 章候选（' + changes.length + ' 段骨架，绑定本书）：请逐项采纳或拒绝', 'ok');
    WB.go('book', 'manuscript', { bookId: b.id, chapter: ck });
  };
})();
