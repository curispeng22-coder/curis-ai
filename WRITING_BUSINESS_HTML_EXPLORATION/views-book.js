/* ============================================================================
   views-book.js — 作品（作品库 / 作品概览 / 正文写作 / 故事状态）
   创作内核的另一半（定位 / 世界 / 人物 / 主支线与结局 / 大纲 / 场景）在 views-craft.js。
   硬约束：
     · 创作对象一律绑定本书；缺本书资料 → 真实空状态 + 创建入口，绝不回退他作样例。
     · 卷章只按真实归属显示；不重复列全书章节。
     · 正文可实际写 / 改 / 保存；候选不覆盖正式稿；正式稿 ≠ 线上稿。
   ========================================================================== */
(function () {
  var ui = WB.ui;

  /* 卷内章节：优先用章自身的 vol 归属，其次按卷的章号区间；不重复列全书章节 */
  function chaptersInVolume(bookId, v) {
    var all = Object.keys(WB.S.chapters).filter(function (k) { return WB.S.chapters[k].bookId === bookId; })
      .sort(function (x, y) { return WB.S.chapters[x].no - WB.S.chapters[y].no; });
    var byVol = all.filter(function (k) { return WB.S.chapters[k].vol === v.id; });
    if (byVol.length) return byVol;
    var from = parseInt(String((v.chapters || [])[0] || '').replace(/\D/g, ''), 10) || 0;
    var to = parseInt(String((v.chapters || [])[1] || '').replace(/\D/g, ''), 10) || 9999;
    return all.filter(function (k) { var n = WB.S.chapters[k].no; return n >= from && n <= to; });
  }
  function bookChapters(bookId) {
    return Object.keys(WB.S.chapters).filter(function (k) { return WB.S.chapters[k].bookId === bookId; })
      .sort(function (x, y) { return WB.S.chapters[x].no - WB.S.chapters[y].no; });
  }
  function resolveChapter(ctx, b) {
    var S = WB.S, chs = bookChapters(b.id);
    var ck = ctx.params && ctx.params.chapter;
    if (!ck || !S.chapters[ck] || S.chapters[ck].bookId !== b.id) ck = chs.length ? (S.__route.view === 'manuscript' ? chs[chs.length - 1] : chs[0]) : null;
    return ck;
  }
  /* 作品展示状态：由真实章节 / 草稿 / 正式稿 / 线上稿派生，不使用写死的 status 文案。
     「空书」只用于真的没有章节的作品；有草稿但无正式稿的作品不得标为空书。 */
  function bookDisplay(b) {
    var S = WB.S, chs = bookChapters(b.id);
    var drafted = chs.filter(function (k) {
      var ms = S.manuscripts[k];
      return ms && Array.isArray(ms.paragraphs) && ms.paragraphs.length;
    }).length;
    var formal = chs.filter(function (k) { return S.chapters[k].formal; }).length;
    var published = chs.filter(function (k) { return S.chapters[k].published; }).length;
    return { chs: chs, drafted: drafted, formal: formal, published: published,
      status: published ? '连载中' : (chs.length ? '创作中 · 尚未上线' : '待开写'),
      none: !chs.length };
  }
  /* 定位以创作内核为唯一来源；Book 上的旧定位字段只作读取兜底，不构成第二套真相。
     这里只读不写，避免渲染期产生副作用（同步发生在作者显式动作里）。 */
  function posOf(b) {
    var c = WB.S.craft && WB.S.craft[b.id];
    var p = c && c.positioning && c.positioning.coreOriginal;
    return p || b.positioning || null;
  }

  /* ---------------- 行动 ---------------- */
  WB.on['book.chap'] = function (el, d) { WB.S.__sel.para = null; WB.go('book', 'manuscript', { chapter: d.id }); };
  WB.on['book.para'] = function (el, d) {
    var same = WB.S.__sel.para === Number(d.id);
    WB.S.__sel.para = same ? null : Number(d.id);
    WB.save(); WB.render();
  };
  WB.on['book.discuss'] = function (el, d) {
    var S = WB.S, ch = WB.chapter(d.chapter);
    var obj = d.para ? d.chapter + '#p' + d.para : d.chapter;
    /* 对话带对象 + 版本状态：他接管的是哪个对象、哪个版本，必须看得见 */
    WB.openConv('E-01', obj, '第 ' + ch.no + ' 章 · ' +
      (WB.inputVersionOf ? WB.inputVersionOf(d.chapter) : (d.version || ch.formal || '候选')) +
      (d.para ? ' · 第 ' + d.para + ' 段' : ' 全章'));
  };
  /* 版本历史：草稿（工作副本）/ 正式稿快照 / 线上稿快照 三态并置，各自带可读正文快照。
     历史只追加不删除；「取回为草稿」只改工作副本，正式稿与线上稿都快照不动。 */
  WB.on['book.versions'] = function (el, d) {
    var S = WB.S, ck = d.chapter, ch = WB.chapter(ck);
    var ms = WB.msOf(ck);
    if (!ms) {
      WB.openDrawer({ title: '版本历史 · 第 ' + ch.no + ' 章', sub: '本章尚无正文',
        body: ui.empty('本章还没有正文，因此没有版本可比',
          '可以直接手写第一章；保存只产生草稿，确认后才生成正式稿，发布是另一条流程。') });
      return;
    }
    function snapBlock(title, tone, ver, at, paras, extra) {
      var list = paras || [];
      return '<div class="tl-i ' + (tone || '') + '">' +
        '<div class="tl-t">' + title + (ver ? '<span class="vtag formal">' + WB.esc(ver) + '</span>' : '') +
        '<span class="t3 xs">' + (list.length ? list.length + ' 段' : '无正文快照') + ' · ' + WB.esc(at || '时间未知') + '</span></div>' +
        (list.length
          ? '<div class="tl-s">' + list.slice(0, 2).map(function (p) { return WB.esc(String(p).slice(0, 56)); }).join('<br>') +
            (list.length > 2 ? '<br><span class="t3">…… 其余 ' + (list.length - 2) + ' 段</span>' : '') + '</div>'
          : '<div class="tl-s t3">早期版本没有保存可读快照，不能用于比对或回退。</div>') +
        (extra || '') + '</div>';
    }
    var div = WB.draftDiverged(ck);
    var rn = Math.max(ms.versions.filter(function (v) { return v.kind === 'draft'; }).length, 1);
    var draftB = snapBlock('草稿（工作副本）', div ? 'choice' : '',
      '草稿 r' + rn, ms.updatedAt, ms.paragraphs,
      '<div class="sm t3" style="margin-top:4px">' +
        (ms.formal
          ? (div ? '与正式稿 ' + WB.esc(ms.formalVersion) + ' <b>有新修改</b>：正式稿不会随草稿自动变化。'
                 : '与正式稿 ' + WB.esc(ms.formalVersion) + ' 内容一致。')
          : '尚无正式稿：手写内容目前只是草稿。') + '</div>');
    var formalB = ms.formal
      ? snapBlock('正式稿快照', 'ok', ms.formal.version, ms.formal.acceptedAt, ms.formal.paragraphs,
        '<div class="sm t3" style="margin-top:4px">' + WB.esc(ms.formal.note || '') + ' 作者已确认；<b>正式稿 ≠ 已发布</b>。</div>')
      : '<div class="tl-i"><div class="tl-t">正式稿' + WB.stBadge('尚无', 'wait') + '</div>' +
        '<div class="tl-s t3">还没有正式稿：草稿需由作者确认后才生成正式稿快照。</div></div>';
    var pubB = ms.published
      ? snapBlock('线上稿快照', 'ok', ms.published.version, ms.published.at, ms.published.paragraphs,
        '<div class="sm t3" style="margin-top:4px">' + WB.esc(ms.published.note || '') + ' 平台核验版本；只有发布流程会改动它。</div>')
      : '<div class="tl-i"><div class="tl-t">线上稿' + WB.stBadge('未发布', 'wait') + '</div>' +
        '<div class="tl-s t3">本章尚未发布；确认正式稿不会自动上线。</div></div>';
    var hist = ms.versions.map(function (v, i) { return { v: v, i: i }; }).reverse().map(function (o) {
      var v = o.v;
      var kd = v.kind === 'formal' ? ['正式', 'working'] : v.kind === 'published' ? ['线上', 'published'] : ['草稿', 'wait'];
      /* 只有**真带正文**的快照才可读、可回退；空快照取回等于清空草稿，不给入口 */
      var readable = Array.isArray(v.paragraphs) && v.paragraphs.length > 0;
      return '<div class="tl-i' + (v.kind === 'formal' ? ' ok' : '') + '"><div class="tl-t">' + WB.esc(v.v) +
        ' ' + WB.stBadge(kd[0], kd[1]) + ' <span class="t3 xs">' + WB.esc(v.at || '时间未知') + '</span></div>' +
        '<div class="tl-s">' + WB.esc(v.note || '') + '<br><span class="t3 xs">' +
        (readable ? '含 ' + v.paragraphs.length + ' 段可读快照' : '无可读快照：不提供取回（取回会清空草稿）') + '</span></div>' +
        (readable ? '<div class="btnrow" style="margin-top:4px"><button class="btn sm ghost" data-action="act.c" ' +
          'data-fn="msRestore" data-a1="' + ck + '" data-a2="' + o.i + '">取回为草稿</button></div>' : '') +
        '</div>';
    }).join('');
    WB.openDrawer({ title: '版本历史 · 第 ' + ch.no + ' 章',
      sub: '草稿 / 正式稿 / 线上稿分开保存；历史不删，只能取回为草稿',
      body: '<div class="sm t2" style="margin-bottom:8px">当前状态：' + WB.esc(WB.chapState(ch)[0]) +
        ' · 线上 ' + WB.esc(ch.published || '未发布') + '</div>' +
        '<div class="tl">' + draftB + formalB + pubB + '</div>' +
        '<div class="hr"></div>' +
        '<div class="sm t3" style="margin-bottom:6px">历史记录（新 → 旧）：取回只改草稿，正式稿与线上稿不动。</div>' +
        '<div class="tl">' + hist + '</div>' +
        ui.note('bound', '「保存」与「确认正式稿」是两件事：保存只写草稿，确认才生成正式稿快照；确认正式 ≠ 发布。' +
          '版本号只描述本地稿，不拿章节 ID 当修订号。') });
  };
  WB.on['book.apply'] = function (el, d) { WB.mergeCandidateDraft(d.id); };
  WB.on['book.rejectAll'] = function (el, d) {
    WB.modal({ title: '整份拒绝候选',
      body: '<p>将保留原正式稿不变，并把候选与理由留档（不是删除）。</p>' +
        '<div class="note">拒绝是正常选择，不是异常；编辑的建议与理由会继续留在候选记录里。</div>',
      footer: '<button class="btn" data-action="close-modal">取消</button>' +
        '<button class="btn dark" data-action="act.c" data-fn="rejectCandidate" data-a1="' + d.id + '">整份拒绝</button>' });
  };
  WB.on['book.receipt'] = function (el, d) {
    var ch = WB.chapter(d.chapter);
    var map = (WB.S.mappings || []).filter(function (m) { return m.bookId === ch.bookId && m.status === 'verified'; })[0];
    WB.openDrawer({ title: '发布事实 · 第 ' + ch.no + ' 章', sub: '正式稿与线上版本的关系',
      body: ui.kv([['正式版本', ch.formal || '—'], ['已发布版本', ch.published || '未发布'], ['上线时间', ch.publishedAt || '—'],
        ['平台映射', map ? WB.esc(map.externalId) : WB.unknown('未建立映射')]]) +
        ui.note('bound', '线上版本与本地正式版本必须可回查；改稿前后保留不同发布版本与暴露时段。'),
      footer: '<button class="btn" data-action="nav.view" data-area="publish" data-view="receipts">查看回执详情</button>' });
  };
  WB.on['book.anchor'] = function (el, d) {
    var S = WB.S, c = WB.byId(S.comments.clusters, d.id);
    WB.openDrawer({ title: '反馈锚点 · ' + c.topic, sub: '样本 ' + c.size + ' 条 / ' + c.coverage,
      body: '<div class="cl"><div class="cl-h">' + WB.esc(c.topic) +
        (c.anchor.conf === 'confirmed' ? WB.stBadge('定位已确认', 'published') : WB.stBadge('定位为推断', 'unknown')) + '</div>' +
        '<div class="cl-q">' + WB.esc(c.quote) + '<div class="who">— 平台评论（作者本人后台可见）</div></div>' +
        '<div class="sm t2">反例：' + WB.esc(c.counter) + '</div>' +
        (c.anchor.note ? '<div class="sm t3">' + WB.esc(c.anchor.note) + '</div>' : '') + '</div>' +
        ui.note('bound', '热评与样本偏差不能代表全体读者；点赞不是独立读者票数。'),
      footer: '<button class="btn" data-action="nav.view" data-area="audience" data-view="comments">去评论洞察</button>' +
        '<button class="btn" data-action="act.k" data-fn="commentToEditor" data-a1="' + c.id + '">交给编辑</button>' });
  };
  WB.on['book.storyChange'] = function (el, d) {
    var b = WB.scopeBook(), c = WB.craftOf(b.id);
    WB.modal({ title: '提出故事状态变更',
      body: '<div class="fld"><label>要变更的内容</label><select class="sel" id="scKind"><option>人物状态 / 知情</option><option>关系</option><option>Canon 条目</option><option>伏笔计划</option><option>世界规则</option></select></div>' +
        '<div class="fld" style="margin-top:8px"><label>说明</label><textarea class="ta" id="scText" placeholder="例如：把 ch46 的兑现计划提前到 ch44"></textarea></div>' +
        '<div class="note bound">变更会生成提案并列出受影响章（影响清单）；<b>不直接覆盖已发布稿件</b>，也不静默改写历史章。</div>' +
        '<div class="sm t3">结构性编辑（人物档案 / 世界规则 / 大纲）请到「创作内核」对应工作面撰写。</div>',
      footer: '<button class="btn" data-action="close-modal">取消</button>' +
        '<button class="btn" data-action="book.storyChangeDo">生成变更提案</button>' });
  };
  WB.on['book.storyChangeDo'] = function () {
    var b = WB.scopeBook(), c = WB.craftOf(b.id);
    var t = (document.getElementById('scText') || {}).value || '（未填写说明）';
    var k = (document.getElementById('scKind') || {}).value || 'Canon 条目';
    c.impactLog.push({ id: 'IM-' + (c.impactLog.length + 1), at: WB.now(), change: '变更提案 · ' + k + '：' + t.slice(0, 24),
      affected: '需人工确认受影响章与后续计划', unchanged: '已发布正文与历史版本不改', decidedBy: '作者（待确认）', state: 'proposed' });
    WB.S.works.unshift({ id: 'W-6' + (10 + WB.S.works.length), title: '故事状态变更提案 · ' + k, owner: 'E-01', status: 'working',
      at: WB.now(), artifact: t.slice(0, 40), next: '作者确认后生成新版本；受影响章列出后再改', area: 'book', obj: b.id });
    WB.closeModal(); WB.save();
    WB.toast('已生成变更提案并记入影响清单：等待作者确认；历史章不受影响', 'ok'); WB.render();
  };
  WB.on['book.continue'] = function (el, d) {
    var chs = bookChapters(d.id);
    WB.go('book', 'manuscript', { chapter: chs.length ? chs[chs.length - 1] : null });
  };
  /* 正文写作：编辑 / 保存 / 取消 */
  WB.on['book.msEdit'] = function (el, d) {
    var S = WB.S, ck = d.chapter, ch = S.chapters[ck];
    WB.msEnsure(ck, ch.bookId, '第 ' + ch.no + ' 章' + (ch.title ? ' · ' + ch.title : ''));
    S.__sel.msEdit = ck; WB.save(); WB.render();
  };
  WB.on['book.msCancelEdit'] = function () {
    var ck = WB.S.__sel.msEdit;
    if (ck && WB.S.__msDraft) delete WB.S.__msDraft[ck];   /* 取消 = 明确放弃本次未保存改动 */
    WB.S.__sel.msEdit = null; WB.save(); WB.render();
  };
  /* 未保存的手写缓冲：一旦打字就记进状态，切章 / 切书 / 收左右栏 / 重渲染都不丢。
     只有「保存草稿」或「取消」才清掉——不能在 UI 整理时把作者正在写的东西弄没。 */
  WB.on['ms.draft'] = function (elm, d) {
    var S = WB.S;
    S.__msDraft = S.__msDraft || {};
    S.__msDraft[d.id || (S.__route.params || {}).chapter] = d.value;
  };
  /* 保存 = 只写草稿（工作副本）。正式稿是快照，绝不被保存动作原地覆盖；线上稿只由发布流程改变。 */
  WB.act.msSave = function (bookId, chapterKey) {
    var ta = document.getElementById('msEditor');
    if (!ta) { WB.toast('编辑器未打开', 'warn'); return; }
    var S = WB.S, ch = S.chapters[chapterKey];
    if (!ch) { WB.toast('找不到该章节，未保存', 'err'); return; }
    var paras = ta.value.split(/\n\s*\n/).map(function (s) { return s.trim(); }).filter(Boolean);
    if (!paras.length) { WB.toast('正文为空：未保存（不把草稿清空）。可继续写，或点取消', 'warn'); return; }
    var ms = WB.msOf(chapterKey) || WB.msEnsure(chapterKey, bookId, '第 ' + ch.no + ' 章' + (ch.title ? ' · ' + ch.title : ''));
    ms.paragraphs = paras;
    ms.updatedAt = WB.now();
    var rn = ms.versions.filter(function (v) { return v.kind === 'draft'; }).length + 1;
    ms.versions.push({ v: '草稿 r' + rn, at: WB.now(), kind: 'draft',
      note: '作者手写保存（' + paras.length + ' 段）' + (ms.formal ? '；正式稿 ' + ms.formalVersion + ' 不变' : '；尚无正式稿'),
      paragraphs: paras.slice() });
    if (!ch.formal && !ch.candidate && ['outline', 'empty', undefined, '', null].indexOf(ch.state) >= 0) ch.state = 'draft';
    if (S.__msDraft) delete S.__msDraft[chapterKey];   /* 已落库：清掉缓冲，避免下次进来显示过期文本 */
    S.__sel.msEdit = null;
    WB.save();
    WB.toast('已保存为草稿 r' + rn + '（' + paras.length + ' 段）。草稿 ≠ 正式稿，也 ≠ 已发布；成为正式稿需你确认', 'ok');
    WB.render();
  };
  WB.act.msGenerate = function (bookId, chapterKey) {
    var S = WB.S, c = WB.craftOf(bookId), ch = S.chapters[chapterKey];
    var scenes = (c.scenes[chapterKey] || []);
    /* 先判定依据是否齐备：没有场景计划时不建空正文容器、不产生「成功」的假象 */
    if (!scenes.length) { WB.toast('本章还没有场景计划：请先到「创作内核 · 场景准备」拆场景，或直接手写', 'warn'); return; }
    var ms = WB.msOf(chapterKey) || WB.msEnsure(chapterKey, bookId, '第 ' + ch.no + ' 章' + (ch.title ? ' · ' + ch.title : ''));
    var changes = scenes.map(function (s, i) {
      var text = '（候选 · 场景 ' + s.id + '）' +
        (s.purpose ? s.purpose + '。' : '') +
        (s.cast && s.cast.length ? s.cast.join('与') + '在' + (s.place || '（待定地点）') + '。' : '') +
        (s.conflict ? '冲突：' + s.conflict + '。' : '') +
        (s.endState ? '结束状态：' + s.endState + '。' : '');
      return { id: 'G' + (i + 1), label: '场景 ' + s.id + ' 起草', why: '依据场景计划：' + (s.purpose || ''),
        before: null, after: text, applied: null, para: ms.paragraphs.length + i + 1 };
    });
    var cid = 'C-' + bookId + '-' + chapterKey + '-G-' + (Object.keys(S.candidates).length+1);
    if (!S.candidates[cid]) {
      S.candidates[cid] = { id: cid, bookId: bookId, chapter: chapterKey, baseVersion: ms.formalVersion, kind: '章节候选（由场景计划生成）',
        title: '第 ' + ch.no + ' 章 · 由场景计划生成', createdAt: WB.now(), by: 'E-01',
        ruleSnapshot:WB.reviewRuleSnapshot(ch.bookId),
        writingTarget:ch.writingTarget || (c.positioning.writingPlan||{}).chapter || null,
        rationale: '目标 '+(ch.writingTarget || (c.positioning.writingPlan||{}).chapter || '未设置')+' 字；当前只生成结构演示，未达到目标篇幅。按本章 ' + scenes.length + ' 个场景计划生成候选段落（Mock，但绑定本书本章）；逐项可采纳 / 拒绝，确认后写入正文。',
        refs: scenes.reduce(function (a, s) { return a.concat(s.refs || []); }, []), changes: changes };
    } else {
      S.candidates[cid].changes = changes;
    }
    ch.candidate = cid;
    if (ch.state === 'outline' || !ch.state) ch.state = 'candidate';
    WB.save();
    WB.toast('已按场景计划生成 ' + changes.length + ' 段候选（绑定本章）；请逐项裁决', 'ok');
    WB.render();
  };
  /* 选区改写：只做确定性改写（压缩 / 去重复），绝不注入固定人物或跨作品文本。
     没有可执行改写时如实标「演示未模拟」，并把入口改为与编辑讨论，而不是假装生成了候选。 */
  WB.on['book.selRewrite'] = function (el, d) {
    var S = WB.S, ck = d.chapter, n = Number(d.para);
    var ms = WB.msOf(ck);
    var before = ms && ms.paragraphs[n - 1] != null ? ms.paragraphs[n - 1] : '';
    if (!before) { WB.toast('该段没有正文：无法生成改写候选（不假装已生成）', 'warn'); return; }
    var sug = WB.selRewriteOf ? WB.selRewriteOf(before) : null;
    S.__sel.selSug = { ck: ck, n: n, before: before, after: sug ? sug.after : before, ok: !!sug };
    var verLine = WB.inputVersionOf ? WB.inputVersionOf(ck) : '—';
    WB.modal({ title: '选区改写候选 · 第 ' + n + ' 段' + (sug ? '' : '（演示未模拟）'),
      body: '<div class="sm t2">对第 ' + n + ' 段生成具体改稿候选，只影响这一段（草稿）。' +
        (sug ? '' : ' <b>这一项为演示请求，本轮未模拟。</b>') + '</div>' +
        '<div class="sm t3" style="margin-top:4px">依据：' + WB.esc(sug ? sug.why : '本轮没有可执行的确定性改写（不虚构人物与情节）') +
        ' · 输入版本：' + WB.esc(verLine) + '</div>' +
        '<div class="diff-txt" style="margin-top:8px"><div class="lbl">改前</div><div class="before">' + WB.esc(before) + '</div>' +
        '<div class="mid"></div><div class="lbl">改后</div><div class="after">' + WB.esc(sug ? sug.after : before) + '</div></div>' +
        '<div class="note bound">采纳只写入草稿；正式稿与线上稿不变，历史版本保留。' +
        (sug ? '' : ' 本轮没有可执行改动，采纳等于保留原样。') + '</div>',
      footer: '<button class="btn" data-action="close-modal">取消</button>' +
        (sug
          ? '<button class="btn primary" data-action="act.b" data-fn="msApplySelSug" data-a1="' + ck + '" data-a2="' + n + '">采纳并写入本段（草稿）</button>'
          : '<button class="btn" data-action="book.selRewriteConv" data-chapter="' + ck + '" data-para="' + n + '">改为与编辑讨论</button>') });
  };
  WB.on['book.selRewriteConv'] = function (el, d) {
    WB.closeModal();
    WB.on['book.discuss'](el, { chapter: d.chapter, para: d.para, version: '草稿' });
  };
  WB.act.msApplySelSug = function (ck, n) {
    var ms = WB.msOf(ck), sug = WB.S.__sel.selSug;
    if (!ms || ms.paragraphs[n - 1] == null) { WB.toast('该段已不存在（章节可能已变化）：未写入', 'warn'); return; }
    if (!sug || sug.ck !== ck || sug.n !== n) { WB.toast('候选已失效：请重新生成', 'warn'); return; }
    ms.paragraphs[n - 1] = sug.after;
    ms.updatedAt = WB.now();
    var rn = ms.versions.filter(function (v) { return v.kind === 'draft'; }).length + 1;
    ms.versions.push({ v: '草稿 r' + rn, at: WB.now(), kind: 'draft',
      note: '采纳选区改写候选（第 ' + n + ' 段）' + (ms.formal ? '；正式稿 ' + ms.formalVersion + ' 不变' : '；尚无正式稿'),
      paragraphs: ms.paragraphs.slice() });
    if (ms.paragraphs[n - 1] !== sug.after) { WB.toast('写入后回读不一致：改动未生效', 'err'); return; }
    WB.S.__sel.para = null; WB.S.__sel.selSug = null; WB.closeModal(); WB.save();
    WB.toast('已写入草稿第 ' + n + ' 段（草稿 r' + rn + '）；正式稿与线上稿未变，历史版本保留', 'ok');
    WB.render();
  };
  WB.on['book.reviewThis'] = function (el, d) { WB.go('book', 'review', { bookId: d.book, kind: 'review', chapter: d.chapter }); };
  WB.on['book.craftGo'] = function (el, d) { WB.go('book', 'craft', { bookId: d.book, mode: d.mode }); };
  /* 章节改名：章节有稳定内部键，改名按键关联，不靠标题正则匹配 */
  WB.on['book.rename'] = function (el, d) {
    var ch = WB.chapter(d.chapter);
    WB.modal({ title: '章节改名 · 第 ' + ch.no + ' 章',
      body: '<div class="fld"><label>章标题</label><input class="inp" id="chTitleInp" value="' + WB.esc(ch.title) + '"></div>' +
        '<div class="note bound">章节内部键：' + WB.esc(d.chapter) +
        '。改名不会断开大纲节点、场景计划与候选的关联（关联按内部键，不按标题）。</div>',
      footer: '<button class="btn" data-action="close-modal">取消</button>' +
        '<button class="btn primary" data-action="act.b" data-fn="chapRename" data-a1="' + d.chapter + '">保存标题</button>' });
  };

  /* ---------------- 作品库 ---------------- */
  WB.register('book.library', {
    render: function (ctx) { return WB.bookShelf(ctx); },
    aside: function () {
      var S = WB.S;
      return WB.asBlock('当前范围', '<div class="as-w"><div class="wt">' + WB.esc((WB.scopeBook() || {}).title || '—') + '</div>' +
          '<div class="ws">切换作品会同时切换正文、大纲、人物、候选与对话范围。</div></div>') +
        WB.asBlock('相关 Work', S.works.filter(function (w) { return w.area === 'book'; }).slice(0, 3).map(function (w) { return WB.workHtml(w); }).join('')) +
        WB.asBlock('责任', WB.ownerHtml('E-01'));
    }
  });
  /* 打开作品：作者显式动作，顺带把创作内核的定位同步到 Book（不在渲染期做写操作） */
  WB.on['book.open'] = function (el, d) {
    WB.S.__scope.bookId = d.id;
    WB.craftOf(d.id);
    if (WB.syncPositioningToBook) WB.syncPositioningToBook(d.id);
    WB.save();
    WB.go('book', 'overview', { bookId: d.id });
  };

  /* ---------------- 作品概览 ---------------- */
  WB.register('book.overview', {
    render: function (ctx) { return WB.bookHome(ctx); },
    aside: function (ctx) {
      var S = WB.S, b = WB.book(ctx.params.bookId || S.__scope.bookId) || WB.scopeBook();
      var c = WB.craftOf(b.id);
      var chs = bookChapters(b.id);
      var conflicts = chs.filter(function (k) { return S.chapters[k].conflict; });
      var props = (S.craftProposals || []).filter(function (p) { return p.bookId === b.id && p.state === 'open'; });
      var onbA = WB.onbState ? WB.onbState(b.id) : { done: true, step: null };
      return (onbA.done ? '' :
          WB.asBlock('这本书现在到哪一步',
            '<div class="as-w"><div class="wt">下一步：' + WB.esc((onbA.step || {}).name || '—') + '</div>' +
            '<div class="ws">' + WB.esc((onbA.step || {}).hint || '') + '</div></div>' +
            '<div class="sm t3">起步可以中断：回来时按本书真实资料接着做，不用重新建书。</div>')) +
        WB.asBlock('当前负责人', WB.ownerHtml('E-01') + '<div class="sm t3" style="margin-top:6px">编辑是长期责任；发布与分析是另外的责任人。</div>') +
        WB.asBlock('创作进度',
          '<div class="sm t2">· 世界条目 ' + c.world.length + ' · 人物 ' + c.characters.length + '<br>' +
          '· 大纲节点 ' + c.outline.length + ' · 场景计划 ' + Object.keys(c.scenes).reduce(function (a, k) { return a + c.scenes[k].length; }, 0) + '<br>' +
          '· 待确认候选 ' + props.length + '</div>') +
        WB.asBlock('待处理', (conflicts.length ? '<div class="as-w"><div class="wt">故事状态冲突 ' + conflicts.length + ' 处</div><div class="ws">' +
          WB.esc(S.chapters[conflicts[0]].conflict || '') + '</div></div>' : '') +
          S.works.filter(function (w) { return w.area === 'book' && w.status !== 'done'; }).slice(0, 2).map(function (w) { return WB.workHtml(w); }).join('')) +
        WB.asBlock('相关视角', '<div class="as-w clickable" data-action="nav.view" data-area="operate" data-view="home"><div class="wt">经营首页</div><div class="ws">作品组合与目标偏差</div></div>' +
          '<div class="as-w clickable" data-action="nav.view" data-area="audience" data-view="comments"><div class="wt">评论洞察</div><div class="ws">读者反馈簇与锚点</div></div>');
    }
  });

  /* ---------------- 正文写作 ---------------- */
  WB.register('book.manuscript', {
    render: function (ctx) {
      var S = WB.S;
      var b = WB.book(ctx.params.bookId || S.__scope.bookId);
      S.__scope.bookId = b.id;
      var chs = bookChapters(b.id);
      var ck = resolveChapter(ctx, b);
      var c = WB.craftOf(b.id);

      /* 空书：真实空状态 + 创建入口，不借用他作章节 */
      if (!ck) {
        return ui.hdr('正文写作 · ' + WB.esc(b.title),
          '这本作品还没有章节。可以直接手写第一章——不必先有市场数据，也不借用其他作品的稿件。',
          '<button class="btn" data-action="book.craftGo" data-book="' + b.id + '" data-mode="positioning">先定定位</button>' +
          '<button class="btn" data-action="nav.view" data-area="market" data-view="direction">看创作方向</button>',
          '<span>当前章：—</span><span class="t4">|</span><span>' + WB.stBadge('空书 · 尚无章节', 'wait') + '</span>') +
          '<div class="grid ms-grid">' +
          '<div>' + ui.panel({ title: '开写第一章', body:
            ui.empty('这本作品还没有正文', '新建的第一章是「草稿」——既不是候选，也不是正式稿；成为正式稿需要你确认，发布又要再走一次发布流程。') +
            '<div class="note bound" style="margin-top:10px">空书可以直接手写，不必先有市场数据；市场观察与方向只是可选依据。也可以先构思背景、人物与主支线。</div>' +
            '<div class="btnrow" style="margin-top:12px"><button class="btn primary" data-action="act.bk" data-fn="newChapter" data-a1="' + b.id + '">新建第 1 章（草稿）</button>' +
            '<button class="btn" data-action="book.craftGo" data-book="' + b.id + '" data-mode="outline">先写大纲</button></div>' }) +
          '</div>' +
          '<div>' + ui.panel({ title: '作品范围', body: ui.kv([
            ['作品', WB.esc(b.title) + '（' + WB.esc(b.id) + '）'],
            ['定位', WB.esc(c.positioning.coreOriginal || b.positioning || '—')],
            ['平台', WB.esc(b.platform || '—')],
            ['章节', '0 章在册'],
            ['来源', WB.esc(b.origin === 'direction' ? '由已接受方向创建' : b.origin === 'import' ? '接入已有平台作品' : '手动新建')]
          ]), footer: '<span>切换作品不会串稿：本书的正文、候选、大纲、人物与对话独立保存。</span>' }) +
          '</div></div>';
      }

      var ch = WB.chapter(ck);
      var ms = WB.msOf(ck);
      var cand = ch.candidate ? WB.candidate(ch.candidate) : null;
      var cst = cand ? WB.candidateState(cand.id) : null;
      var paraSel = S.__sel.para || null;
      var editing = S.__sel.msEdit === ck;
      /* 三态实况：草稿段数 / 草稿是否已与正式稿分叉 / 下一版正式稿号 */
      var draftN = ms ? ms.paragraphs.length : 0;
      var diverged = WB.draftDiverged(ck);
      var nextV = 'v' + ((parseInt(String(ms && ms.formalVersion || ch.formal || 'v0').replace(/\D/g, ''), 10) || 0) + 1);
      var draftRn = ms ? Math.max(ms.versions.filter(function (v) { return v.kind === 'draft'; }).length, 1) : 0;
      /* 可确认为正式稿：有草稿，且（尚无正式稿 或 草稿有新修改） */
      var canConfirm = !!draftN && (!ms.formal || diverged);

      /* 章节切换栏（卷内归属，不重复） */
      var chListHtml = (S.volumes[b.id] || []).map(function (v) {
        var list = chaptersInVolume(b.id, v);
        if (!list.length) return '';
        return '<div class="vol-h"><span>' + WB.esc(v.name) + '</span><span class="t3">' + (v.open ? '进行中' : '') + '</span></div>' +
          list.map(function (k) {
            var cc = S.chapters[k];
            return '<div class="chap' + (k === ck ? ' on' : '') + '" data-action="book.chap" data-id="' + k + '"><span class="cn">' + cc.no + '</span>' +
              '<span class="ct">' + WB.esc(cc.title) + '</span><span class="cm">' +
              (cc.formal ? '<span class="vtag formal">' + WB.esc(cc.formal) + '</span>' : '') +
              (cc.candidate ? '<span class="vtag cand">候选</span>' : '') + '</span></div>';
          }).join('');
      }).join('');

      /* 正文区 */
      var bodyHtml;
      if (editing) {
        /* 优先显示未保存缓冲（打字即记录），避免重渲染把正在写的字冲掉 */
        var buffered = WB.S.__msDraft ? WB.S.__msDraft[ck] : null;
        var text = (buffered != null) ? buffered : (ms ? ms.paragraphs.join('\n\n') : '');
        var dirtyDraft = (buffered != null) && buffered !== (ms ? ms.paragraphs.join('\n\n') : '');
        bodyHtml = '<div style="padding:0 0 8px"><div class="sm t3" style="margin-bottom:6px">空行分段；保存为草稿（不是正式稿）。' +
          (dirtyDraft ? ' <b class="ms-dirty">有未保存的改动（切章 / 收栏不会丢）</b>' : '') + '</div>' +
          '<textarea class="ms-edit" id="msEditor" data-input="ms.draft" data-id="' + ck + '">' + WB.esc(text) + '</textarea></div>';
      } else if (ms && ms.paragraphs.length) {
        var anchor = S.comments.clusters.filter(function (x) { return x.anchor.chapter === ck; });
        bodyHtml = ms.paragraphs.map(function (p, i) {
          var n = i + 1;
          var a = anchor.filter(function (x) { return x.anchor.from && n >= x.anchor.from && n <= x.anchor.to; })[0];
          var inCand = cand && cand.changes.some(function (x) { return x.para === n; });
          return '<p class="' + (paraSel === n ? 'hl' : '') + '" data-action="book.para" data-id="' + n + '" style="cursor:pointer">' +
            '<span class="ms-pn">' + (n < 10 ? '0' + n : n) + '</span>' + WB.esc(p) +
            (a ? ' <button class="chip static" data-action="book.anchor" data-id="' + a.id + '">反馈锚点 ' + a.id + '</button>' : '') +
            (inCand ? ' <button class="chip" data-action="book.diffJump" data-id="' + n + '">候选涉及本段</button>' : '') +
            '</p>';
        }).join('');
      } else if (ch.state === 'outline') {
        bodyHtml = '<div class="empty"><b>本章只有大纲</b>' + WB.esc(ch.outline || '未填写大纲') +
          '<br><span class="t3">大纲不是正文；写与不写由作者决定。可以手写，也可以按场景计划生成候选。</span></div>';
      } else if (ch.state === 'draft') {
        bodyHtml = '<div class="empty"><b>起草中</b>尚无正文。<br><span class="t3">作者可直接手写；不强制先有 AI 候选。</span></div>';
      } else if (cand && cand.opening) {
        bodyHtml = '<div class="empty"><b>候选稿（未接受）</b>以下为候选开头，接受前不属于正式稿。</div>' +
          cand.opening.map(function (p, i) {
            return '<p><span class="ms-pn">' + (i + 1 < 10 ? '0' + (i + 1) : i + 1) + '</span>' + WB.esc(p) + '</p>';
          }).join('');
      } else {
        bodyHtml = '<div class="empty"><b>本章尚无正文</b>点「手写」开始，或在场景准备后生成候选。</div>';
      }

      var selBar = (paraSel && !editing) ? '<div class="ms-tools" style="border-top:0;border-bottom:1px solid var(--line-2)">' +
        '<span class="sm t2">已选第 ' + paraSel + ' 段</span>' +
        '<button class="btn sm" data-action="book.selRewrite" data-chapter="' + ck + '" data-para="' + paraSel + '">改写这一段</button>' +
        '<button class="btn sm" data-action="book.discuss" data-chapter="' + ck + '" data-para="' + paraSel + '" data-version="' + WB.esc(ms && ms.formalVersion ? ms.formalVersion : '草稿') + '">对这一段讨论</button>' +
        '<button class="btn sm ghost" data-action="book.para" data-id="' + paraSel + '">取消选择</button>' +
        '<span class="sm t3">改动只落到草稿；正式稿与线上稿是快照</span></div>' : '';

      /* 标题可点改名：章节有稳定内部键，改名不断开大纲 / 场景 / 候选的关联 */
      var msBlock = '<div class="ms-wrap">' +
        '<div class="ms-bar"><span class="ms-title clickable" data-action="book.rename" data-chapter="' + ck + '" title="点击改名（关联按稳定章节键保持）">第 ' + ch.no + ' 章 · ' + WB.esc(ch.title) + '</span>' +
        '<span class="vtag' + (diverged ? ' cand' : '') + '">' + (draftN ? '草稿 r' + draftRn : '无草稿') + (diverged ? ' · 有新修改' : '') + '</span>' +
        (ms && ms.formal ? '<span class="vtag formal">正式 ' + WB.esc(ms.formalVersion) + '</span>' : '<span class="vtag">无正式稿</span>') +
        (ch.published ? '<span class="vtag pub">线上 ' + WB.esc(ch.published) + '</span>' : '<span class="vtag">未发布</span>') +
        (ch.candidate ? '<span class="vtag cand">候选 ' + WB.esc(ch.candidate) + '</span>' : '') +
        '<span class="spacer"></span>' +
        (editing
          ? '<button class="btn sm primary" data-action="act.b" data-fn="msSave" data-a1="' + b.id + '" data-a2="' + ck + '">保存草稿</button>' +
            '<button class="btn sm" data-action="book.msCancelEdit">取消</button>'
          : '<button class="btn sm" data-action="book.msEdit" data-chapter="' + ck + '">' + (draftN ? '手写编辑' : '手写正文') + '</button>' +
            '<button class="btn sm" data-action="book.versions" data-chapter="' + ck + '">版本历史</button>') +
        (ch.published ? '<button class="btn sm" data-action="book.receipt" data-chapter="' + ck + '">发布事实</button>' : '') +
        '</div>' + selBar +
        (diverged ? '<div style="padding:10px 14px 0">' + ui.note('choice',
          '<b>草稿已改动 ' + draftN + ' 段，正式稿 ' + WB.esc(ms.formalVersion) + ' 未变。</b>' +
          '<div class="btnrow" style="margin-top:6px">' +
          (canConfirm ? '<button class="btn sm primary" data-action="flow.stage" data-stage="review" data-chapter="' + ck + '">检查本次修改</button>' : '') +
          '<button class="btn sm" data-action="book.versions" data-chapter="' + ck + '">比对版本</button>' +
          '<button class="btn sm ghost" data-action="book.discuss" data-chapter="' + ck + '" data-version="' + WB.esc('草稿 r' + draftRn) + '">与编辑讨论草稿</button>' +
          '</div>') + '</div>' : '') +
        (ch.conflict ? '<div style="padding:10px 14px 0">' + ui.note('choice', '<b>Canon 冲突：</b>' + WB.esc(ch.conflict) +
          '<div class="btnrow" style="margin-top:6px"><button class="btn sm" data-action="nav.view" data-area="book" data-view="story">去故事状态处理</button>' +
          '<button class="btn sm" data-action="book.reviewThis" data-book="' + b.id + '" data-chapter="' + ck + '">交给审稿</button></div>') + '</div>' : '') +
        '<div class="ms-body">' + bodyHtml + '</div>' +
        '<div class="ms-tools">' +
        /* 常用动作靠近对象：确认正式稿（手写稿也能确认，R5）/ 加入发布队列 / 讨论 */
        (canConfirm && !diverged ? '<button class="btn sm primary" data-action="flow.stage" data-stage="review" data-chapter="' + ck + '">写完了，开始审校</button>' : '') +
        (ms && ms.formal && !ch.published ? '<button class="btn sm primary" data-action="act.q" data-fn="queueAdd" data-a1="' + ck + '">加入发布队列</button>' : '') +
        (ch.published && cand && cst && cst.applied ? '<button class="btn sm" data-action="act.q" data-fn="queueAdd" data-a1="' + ck + '">发布本次修订</button>' : '') +
        (!cand ? '<button class="btn sm" data-action="act.c" data-fn="msGenerate" data-a1="' + b.id + '" data-a2="' + ck + '">按场景计划生成候选</button>' : '') +
        '<button class="btn sm ghost" data-action="book.discuss" data-chapter="' + ck + '" data-version="' + WB.esc('草稿 r' + Math.max(draftRn, 1)) + '">与编辑讨论</button>' +
        '<span class="sm t3">保存草稿后，继续本章审校。</span>' +
        '</div><details class="flow-details"><summary>本章采用的写作要求</summary>' + basisStrip(b, c, ck) + '</details></div>';

      /* 候选栏 */
      var candCol;
      if (cand) {
        var items = cand.changes.map(function (x) {
          var cls = x.applied === true ? ' adopted' : x.applied === false ? ' rejected' : '';
          return '<div class="diff-i' + cls + '"><div class="diff-h"><span class="idx">' + WB.esc(x.id) + '</span>' +
            '<span class="diff-why">' + WB.esc(x.why) + '</span>' +
            '<span class="diff-acts">' +
            '<button class="btn sm' + (x.applied === true ? ' primary' : '') + '" data-action="act.c" data-fn="decideChange" data-a1="' + cand.id + '" data-a2="' + x.id + '" data-a3="true">采纳</button>' +
            '<button class="btn sm' + (x.applied === false ? ' dark' : '') + '" data-action="act.c" data-fn="decideChange" data-a1="' + cand.id + '" data-a2="' + x.id + '" data-a3="false">拒绝</button>' +
            '</span></div>' +
            '<div class="diff-txt"><div class="lbl">' + WB.esc(x.label) + '</div>' +
            (x.before ? '<div class="before">' + WB.esc(x.before) + '</div><div class="mid"></div>' : '') +
            '<div class="after">' + WB.esc(x.after) + '</div></div></div>';
        }).join('');

        candCol = '<section class="pnl"><div class="pnl-h"><div class="pnl-t">候选 ' + WB.esc(cand.id) +
          ' <span class="sub">' + WB.esc(cand.kind) + ' · 基于 ' + WB.esc(cand.baseVersion || '无正式稿') + '</span></div>' +
          '<div class="pnl-a">' + WB.stBadge('采纳 ' + cst.adopted + ' / 拒绝 ' + cst.rejected + ' / 未定 ' + cst.open, cst.open ? 'choice' : 'published') + '</div></div>' +
          '<div class="pnl-body">' +
          '<div class="sm t2">' + WB.esc(cand.rationale) + '</div>' +
          '<div class="sm t3" style="margin-top:4px">引用依据：' + WB.esc((cand.refs || []).join('、') || '—') + '</div>' +
          '<div class="hr"></div><div class="diff">' + items + '</div>' +
          (cand.conflict ? '<div class="note choice" style="margin-top:10px"><b>与 Canon 冲突</b><br>' + WB.esc(cand.conflict) + '</div>' : '') +
          '</div>' +
          '<div class="pnl-f"><div class="btnrow">' +
          (cst.applied
            ? '<span class="st st-published">已合入草稿 ' + WB.esc(ch.formal || '') + '</span>' +
              '<button class="btn sm" data-action="book.versions" data-chapter="' + ck + '">看版本</button>'
            : '<button class="btn sm primary" data-action="book.apply" data-id="' + cand.id + '">合入草稿，进入审校</button>' +
              '<button class="btn sm" data-action="book.rejectAll" data-id="' + cand.id + '">整份拒绝</button>') +
          '<button class="btn sm ghost" data-action="book.discuss" data-chapter="' + ck + '" data-version="' + WB.esc(cand.id) + '">讨论候选</button>' +
          '</div></div></section>' +
          (!cst.applied && cst.adopted > 0 ? ui.note('info', '确认后将生成 <b>正式 ' + WB.esc('v' + ((parseInt(String(ch.formal || 'v0').replace(/\D/g, ''), 10) || 0) + 1)) + '</b>：<br>' +
            '· 正式稿更新，旧版本保留<br>· 故事状态需重新对齐（受影响：后续候选、伏笔计划）<br>' +
            '· <b>线上仍是 ' + WB.esc(ch.published || '未发布') + '，不会自动改变</b>；要发布修订需另走发布流程') : '');
      } else {
        /* 无候选：不常驻等宽空卡。生成入口已在正文工具条（靠近对象），这里只留一句状态。 */
        candCol = ui.panel({ title: '候选', sub: '本章暂无',
          body: '<div class="sm t3">本章还没有候选：可以与编辑讨论后生成，或在场景准备后按场景计划生成；作者也可直接手写正文。</div>' });
      }

      var chapListPanel = chs.length
        ? ui.panel({
            title: '章节', sub: '点击切换',
            actions: WB.stBadge('当前 第 ' + ch.no + ' 章', 'working'),
            body: '<div class="chap-list" style="max-height:264px">' + chListHtml + '</div>',
            footer: '<span>切换章节不改变作品范围；候选与选区按章节各自保留。</span>'
          })
        : ui.panel({ title: '章节', body: ui.empty('本章节为空书', '可以直接手写正文，不必先有市场数据。') });

      return WB.chapterFrame(b, ck, msBlock, candCol, ctx);
    },
    aside: function (ctx) {
      var S = WB.S;
      var b = WB.book(ctx.params.bookId || S.__scope.bookId);
      var chs = bookChapters(b.id);
      var ck = resolveChapter(ctx, b);
      if (!ck) {
        return WB.asBlock('责任人', WB.ownerHtml('E-01') +
          '<div class="sm t3" style="margin-top:6px">编辑是长期责任；本书尚无正文，责任仍挂在同一员工身上。</div>') +
          WB.asBlock('本书范围', '<div class="sm t2">· 作品 ' + WB.esc(b.id) + '<br>· 0 章在册<br>· 正文与候选独立保存，不与其他作品串台</div>');
      }
      var ch = WB.chapter(ck);
      var st = S.storyState[b.id] || { threads: [], canon: [] };
      var cand = ch.candidate ? WB.candidate(ch.candidate) : null;
      var cst = cand ? WB.candidateState(cand.id) : null;
      var c = WB.craftOf(b.id);
      var scenes = (c.scenes[ck] || []);
      return WB.asBlock('本章写作要求（继承 → 临时）', chapterReqInner(b, c, ck)) +
        WB.asBlock('故事状态影响', '<div class="sm t2">' +
          (cst && cst.adopted > 0 && !cst.applied ? '确认正式版本后：<br>· 受影响章：后续候选需重对齐<br>· 伏笔计划保持不变' :
            '当前无待确认的正式版本变更。') + '</div>' +
          '<div class="hr" style="margin:8px 0"></div>' +
          ((st.threads || []).slice(0, 3).map(function (t) {
            return '<div class="sm" style="margin-bottom:4px">' + WB.esc(t.id) + ' ' + WB.esc(t.text) +
              ' <span class="t3">（' + WB.esc(t.state) + ' · ' + WB.esc(t.plan) + '）</span></div>';
          }).join('') || '<div class="sm t3">本书尚无伏笔记录。</div>')) +
        WB.asBlock('本章场景（' + scenes.length + '）',
          scenes.length ? scenes.map(function (s) {
            return '<div class="as-w"><div class="wt">' + WB.esc(s.id) + '</div><div class="ws">' + WB.esc(s.purpose || '') + '</div></div>';
          }).join('') + '<div class="btnrow" style="margin-top:6px"><button class="btn sm" data-action="book.craftGo" data-book="' + b.id + '" data-mode="scenes">去场景准备</button></div>'
            : '<div class="sm t3">本章尚未拆场景。</div><div class="btnrow" style="margin-top:6px"><button class="btn sm" data-action="book.craftGo" data-book="' + b.id + '" data-mode="scenes">去场景准备</button></div>') +
        WB.asBlock('责任人', WB.ownerHtml('E-01') +
          '<div class="btnrow" style="margin-top:8px"><button class="btn sm" data-action="book.discuss" data-chapter="' + ck + '" data-version="' + WB.esc(ch.formal || '草稿') + '">与编辑讨论</button></div>' +
          '<div class="sm t3" style="margin-top:6px">编辑是长期责任，责任与当前工作、产物相连。</div>') +
        WB.asBlock('本章 Work', S.works.filter(function (w) { return w.obj === ch.candidate || w.obj === ck; }).map(function (w) { return WB.workHtml(w); }).join('') || '<div class="sm t3">本章暂无独立 Work。</div>');
    }
  });
  WB.on['book.diffJump'] = function (el, d) {
    var ck = WB.S.__route.params.chapter;
    var ch = ck ? WB.chapter(ck) : null;
    WB.toast('该段被候选 ' + ((ch && ch.candidate) || '') + ' 涉及，右侧显示改动前后');
  };

  /* 本章写作要求：继承全书定位 + 本章临时覆盖；两者分别显示，切章/切书/收栏都不丢。 */
  function subSel(id, e) {
    var t = WB.tagDef(id); if (!t || !e) return [];
    var out = Array.isArray(e.sel) ? e.sel.slice() : [];
    (t.optGroups || []).forEach(function (g, gi) {
      var a = e[WB.tagSubKey(id, gi)];
      if (Array.isArray(a)) out = out.concat(a);
    });
    return out.filter(function (x) { return x && x !== '（待定）'; });
  }
  /* 本次写作依据：把标签选择转成的写作要求摊开，作者能读、能改（只存标签不进入任务视为失败） */
  function basisStrip(b, c, ck) {
    var tags = WB.tagsOf(c);
    var ch = WB.S.chapters[ck] || {};
    var ov = (ch.tagOverride && ch.tagOverride._on) ? ch.tagOverride : null;
    var ids = ['L12', 'L15', 'L16', 'L17', 'L19'];
    var chips = ids.map(function (id) {
      var t = WB.tagDef(id); if (!t) return '';
      var oSel = ov ? subSel(id, ov[id]) : [];
      var base = WB.tagPicked(tags, id).sel;
      var shown = oSel.length ? oSel : base;
      if (!shown.length) return '';
      var src = oSel.length ? '本章临时' : '继承全书';
      return '<span class="keytag" title="' + WB.esc(src) + '"><b>' + WB.esc(t.name) + '</b> ' + WB.esc(shown.join('、')) +
        ' <span class="t3">· ' + WB.esc(src) + '</span></span>';
    }).join('');
    return '<div class="ms-basis"><div class="sm t3" style="margin-bottom:4px">本次写作依据（来自创作选择；本章可临时覆盖，不改成全书）</div>' +
      '<div class="keystrip">' + (chips || '<span class="sm t3">未设置写作要求——不影响写作，可稍后再补。</span>') +
      '<button class="btn sm ghost" data-action="craft.picker" data-book="' + b.id + '" data-scope="chapter" data-chapter="' + ck + '">本章要求</button>' +
      '</div></div>';
  }
  function chapterReqInner(b, c, ck) {
    var ch = WB.S.chapters[ck] || {};
    var ov = (ch.tagOverride && ch.tagOverride._on) ? ch.tagOverride : null;
    var ids = ['L12', 'L13', 'L15', 'L16', 'L17', 'L19', 'L21', 'L23'];
    var rows = ids.map(function (id) {
      var t = WB.tagDef(id); if (!t) return '';
      var base = WB.tagPicked(WB.tagsOf(c), id).sel;
      var oSel = ov ? subSel(id, ov[id]) : [];
      var shown = oSel.length ? oSel : base;
      var src = oSel.length ? '本章临时' : (base.length ? '继承全书' : '未设置');
      return '<div class="as-w" style="border:0;padding:3px 0;background:none"><div class="ws">' +
        '<b>' + WB.esc(t.name) + '</b> ' + WB.stBadge(src, oSel.length ? 'choice' : (shown.length ? 'published' : 'unknown')) + '</div>' +
        '<div class="ws">' + (shown.length ? WB.esc(shown.join('、')) : '<span class="t3">—</span>') + '</div></div>';
    }).join('');
    return '<div class="sm t2">本章实际采用：<b>临时覆盖优先，其次继承全书</b>；两者分别显示，不互相顶掉。</div>' +
      '<div style="margin-top:6px">' + rows + '</div>' +
      '<div class="btnrow" style="margin-top:8px">' +
      '<button class="btn sm" data-action="craft.picker" data-book="' + b.id + '" data-scope="chapter" data-chapter="' + ck + '">设置本章临时要求</button>' +
      (ov ? '<button class="btn sm ghost" data-action="book.clearChapterReq" data-chapter="' + ck + '">恢复继承全书</button>' : '') +
      '</div>' +
      '<div class="sm t3" style="margin-top:6px">章级临时要求只改这一章，不会把本章偏好自动改成全书；未设置不阻止写作。</div>';
  }
  WB.on['book.clearChapterReq'] = function (elm, d) {
    var ch = WB.S.chapters[d.chapter];
    if (!ch || !ch.tagOverride) { WB.toast('本章本来就没有临时要求'); return; }
    ch.tagOverride = null;
    WB.save(); WB.render();
    WB.toast('已恢复为继承全书定位（本书定位未改变）', 'ok');
  };

  /* ---------------- 故事状态 ---------------- */
  WB.register('book.story', {
    render: function (ctx) {
      var S = WB.S, b = WB.book(ctx.params.bookId || S.__scope.bookId) || WB.scopeBook();
      S.__scope.bookId = b.id;
      /* 本书故事状态：缺本书资料 → 空结构（绝不回退其他作品的样例） */
      var st = S.storyState[b.id] || { characters: [], relations: [], canon: [], threads: [], timeline: [] };
      var c = WB.craftOf(b.id);
      var chs = bookChapters(b.id).filter(function (k) { return S.chapters[k].conflict; });
      var hasAny = (st.canon || []).length || (st.threads || []).length || (st.relations || []).length || (st.timeline || []).length || c.characters.length;

      var conflictPanel = chs.length ? ui.panel({ title: '冲突检查', sub: chs.length + ' 处', body:
        chs.map(function (k) {
          return '<div class="note choice"><b>第 ' + S.chapters[k].no + ' 章候选与 Canon 冲突</b><br>' + WB.esc(S.chapters[k].conflict) +
            '<div class="btnrow" style="margin-top:6px">' +
            '<button class="btn sm" data-action="book.res" data-id="' + k + '">修订候选</button>' +
            '<button class="btn sm" data-action="book.storyChange">修订 Canon（需作者决定）</button>' +
            '<button class="btn sm ghost" data-action="book.reviewThis" data-book="' + b.id + '" data-chapter="' + k + '">交给审稿</button></div></div>';
        }).join(''),
        footer: '<span>冲突不自动解决：改候选或改 Canon 都需要作者确认，历史章不受影响。</span>' }) : '';

      var charPanel = ui.panel({ title: '人物与认知域', sub: '角色 / 作者 / 读者 / 尚未揭示',
        actions: '<button class="btn sm" data-action="book.craftGo" data-book="' + b.id + '" data-mode="characters">在创作内核编辑</button>',
        body: c.characters.length ? ui.tbl(['人物', '角色', '目标 / 动机', '声纹', '认知域（角色已知 / 尚未揭示）'],
          c.characters.map(function (x) {
            var k = x.knows || {};
            return { cells: ['<b>' + WB.esc(x.name) + '</b>',
              WB.esc(x.role || '—'),
              WB.esc((x.goal || '—') + ' / ' + (x.motivation ? x.motivation.slice(0, 18) + '…' : '—')),
              WB.esc(x.voice || '—'),
              WB.esc(((k.character || []).join('；') || '—') + ' / ' + ((k.unrevealed || []).join('；') || '—'))] };
          })) : ui.empty('本书暂无人物', '到创作内核新增人物与认知域。') });

      var relationPanel = ui.panel({ title: '关系', tight: true, body: (st.relations || []).length
        ? ui.tbl(['一方', '另一方', '关系', '始于'], st.relations.map(function (r) { return { cells: [WB.esc(r.a), WB.esc(r.b), WB.esc(r.type), WB.esc(r.since)] }; }))
        : ui.empty('本书暂无关系记录', '关系带方向与阶段；未记录的不会凭空生成。') });

      var canonPanel = ui.panel({ title: 'Canon 条目', sub: '来源与可变更性', tight: true, body: (st.canon || []).length
        ? ui.tbl(['条目', '来源', '可变更'], st.canon.map(function (x) { return { cells: ['<b>' + WB.esc(x.id) + '</b> ' + WB.esc(x.text), WB.esc(x.source), WB.esc(x.changeable)] }; }))
        : ui.empty('本书暂无 Canon 条目', '从正文抽取或由作者确认后才成为 Canon；AI 推断不自动写入。') });

      var threadPanel = ui.panel({ title: '伏笔', sub: '兑现计划 / 状态 / 关联的本书对象', tight: true,
        actions: '<button class="btn sm" data-action="book.threadNew" data-book="' + b.id + '">新增伏笔</button>',
        body: (st.threads || []).length
        ? ui.tbl(['伏笔', '埋设', '计划', '状态', '关联本书对象', ''], st.threads.map(function (t) {
          var nm = WB.esc(t.text);
          return { cells: ['<b>' + WB.esc(t.id) + '</b> ' + nm, WB.esc(t.planted), WB.esc(t.plan),
            t.state === '待兑现' ? WB.stBadge(t.state, 'wait') : WB.stBadge(t.state, 'choice'),
            WB.esc(linkLabel(t.refs)),
            '<button class="btn sm" data-action="book.threadEdit" data-book="' + b.id + '" data-id="' + WB.esc(t.id) + '">编辑</button>'] };
        })) : ui.empty('本书暂无伏笔', '可以在这里新增一条伏笔，并把它关联到本书已有的章或人物；状态是计划台账，写进正文之后才算兑现。') });

      var worldPanel = ui.panel({ title: '世界与设定', tight: true, body: c.world.length
        ? ui.tbl(['设定', '类别', '条件 / 限制', '状态'], c.world.map(function (w) {
          return { cells: ['<b>' + WB.esc(w.name) + '</b>', WB.esc(w.kind), WB.esc((w.cond || '—') + ' / ' + (w.limit || '—')), WB.factBadge(w.state)] };
        })) : ui.empty('本书暂无世界设定', '到创作内核新增规则 / 地点 / 势力。') });

      var timelinePanel = ui.panel({ title: '时序', sub: '事件时间与前后依赖',
        actions: '<button class="btn sm" data-action="book.timelineNew" data-book="' + b.id + '">新增时序</button>',
        body: (st.timeline || []).length ? '<div class="tl">' + st.timeline.map(function (t) {
          return '<div class="tl-i ok"><div class="tl-t">' + WB.esc(t.at) + '</div><div class="tl-s">' + WB.esc(t.note) +
            (t.refs && t.refs.length ? ' <span class="sm t3">· 关联：' + WB.esc(linkLabel(t.refs)) + '</span>' : '') + '</div></div>';
        }).join('') + '</div>' : ui.empty('本书暂无时序记录', '可以在这里新增一条时序并关联到本书已有的章；关联只指向已有对象，不复制内容。') });

      return ui.hdr('故事状态 · ' + WB.esc(b.title),
        'Outline、人物、认知域、Canon、时序与伏笔及其来源。经营变化不破坏故事连续性：变更先提案，再列影响，不静默覆盖。',
        '<button class="btn" data-action="book.craftGo" data-book="' + b.id + '" data-mode="characters">编辑人物</button>' +
        '<button class="btn" data-action="craft.impactList" data-what="' + WB.esc(b.title) + '">影响清单</button>' +
        '<button class="btn primary" data-action="book.storyChange">提出变更</button>',
        '<span>来源标注：正文 / 计划 / 作者决定 / 推断</span><span class="t4">|</span><span>不直接覆盖已发布稿件</span>') +

        (hasAny ? '' : ui.panel({ title: '本书尚无故事状态', body:
          ui.empty('这本作品还没有故事状态', '可以到创作内核建立人物、世界与大纲；也可以直接手写正文，之后再从正文抽取候选。') +
          '<div class="btnrow" style="margin-top:10px"><button class="btn primary" data-action="book.craftGo" data-book="' + b.id + '" data-mode="characters">去建立人物</button>' +
          '<button class="btn" data-action="book.craftGo" data-book="' + b.id + '" data-mode="positioning">先去定位</button>' +
          '<button class="btn" data-action="nav.view" data-area="book" data-view="import">导入旧稿</button></div>' })) +

        conflictPanel +
        '<div class="grid g2">' + charPanel + relationPanel + '</div>' +
        '<div class="grid g2">' + canonPanel + threadPanel + '</div>' +
        '<div class="grid g2">' + worldPanel + timelinePanel + '</div>';
    },
    aside: function (ctx) {
      var S = WB.S, b = WB.book(ctx.params.bookId || S.__scope.bookId) || WB.scopeBook();
      var c = WB.craftOf(b.id);
      return WB.asBlock('结构约定', '<div class="sm t2">· 卷 / 章有稳定内部身份，标题与序号可变<br>· Scene / Passage 是正文版本内锚点<br>· 不新建 Company OS 层级</div>') +
        WB.asBlock('来源', '<div class="sm t2">Canon、伏笔、世界与人物都带来源：正文段、计划、作者决定或推断。经营与数据变化不会自动改写它们。</div>') +
        WB.asBlock('影响清单（' + c.impactLog.length + '）',
          c.impactLog.length ? c.impactLog.slice(-3).map(function (i) {
            return '<div class="as-w"><div class="wt">' + WB.esc(i.change.slice(0, 20)) + '</div><div class="ws">' +
              WB.esc(Array.isArray(i.affected) ? i.affected.join('、') : (i.affected || '—')) + '</div></div>';
          }).join('') : '<div class="sm t3">暂无变更。</div>') +
        WB.asBlock('相关 Work', S.works.filter(function (w) { return w.area === 'book'; }).slice(0, 3).map(function (w) { return WB.workHtml(w); }).join(''));
    }
  });
  /* ---------------- D10 最小编辑/联动：伏笔 与 时序 ----------------
     故事状态原先只有台账展示（只读）。起步流程简化之后创作深度不能跟着丢：
     这里补最小的写入口 —— 新增 / 编辑一条伏笔（含状态），并可把它关联到本书
     已有对象（在册章 / 已建人物）；时序同理。全部写进既有的 S.storyState[b.id]，
     不新建对象体系，也不复制他作内容。 */
  function storyStateOf(bookId) {
    var S = WB.S;
    if (!S.storyState[bookId]) S.storyState[bookId] = { characters: [], relations: [], canon: [], threads: [], timeline: [] };
    var st = S.storyState[bookId];
    if (!Array.isArray(st.threads)) st.threads = [];
    if (!Array.isArray(st.timeline)) st.timeline = [];
    return st;
  }
  /* 只列本书自己的可关联对象：在册章 + 已建人物（不跨作品、不凭空造对象） */
  function linkTargets(b, c) {
    var S = WB.S, out = [];
    Object.keys(S.chapters || {}).forEach(function (k) {
      var ch = S.chapters[k];
      if (!ch || ch.bookId !== b.id) return;
      out.push({ kind: 'chapter', id: k, label: '第 ' + ch.no + ' 章' + (ch.title ? ' · ' + ch.title : '') });
    });
    (((c || {}).characters) || []).forEach(function (x) { out.push({ kind: 'char', id: x.name, label: '人物 · ' + x.name }); });
    return out;
  }
  function linkLabel(refs) {
    if (!refs || !refs.length) return '—';
    return refs.map(function (r) { return r.label || r.id; }).join('、');
  }
  function collectRefs() {
    return Array.prototype.slice.call(document.querySelectorAll('.linkRef:checked')).map(function (el) {
      return { kind: el.getAttribute('data-kind'), id: el.value, label: el.getAttribute('data-label') };
    });
  }
  function linkBox(b, c, refs) {
    var cur = (refs || []).map(function (r) { return r.id; });
    var opts = linkTargets(b, c).map(function (o) {
      return '<label class="th-ref"><input type="checkbox" class="linkRef" value="' + WB.esc(o.id) + '" data-kind="' + WB.esc(o.kind) +
        '" data-label="' + WB.esc(o.label) + '"' + (cur.indexOf(o.id) >= 0 ? ' checked' : '') + '> ' + WB.esc(o.label) + '</label>';
    }).join('');
    return '<div class="fld" style="margin-top:8px"><label>关联本书已有对象（可多选；只列本书自己的章与人物）</label>' +
      (opts || '<div class="sm t3">这本书还没有可关联的章或人物——先手写第一章，或到创作内核建立人物。</div>') + '</div>';
  }
  function fieldVal(id) { var e = document.getElementById(id); return e ? String(e.value || '').trim() : ''; }
  function inputFld(label, id, val, ph) {
    return '<div class="fld' + (ph === null ? '' : '') + '" style="margin-top:8px"><label>' + label + '</label><input class="inp" id="' + id +
      '" value="' + WB.esc(val || '') + '" placeholder="' + WB.esc(ph || '') + '" /></div>';
  }
  function stateFld(id, cur) {
    return '<div class="fld" style="margin-top:8px"><label>状态</label><select class="sel" id="' + id + '">' +
      ['待兑现', '已兑现', '未决', '放弃'].map(function (s) {
        return '<option' + (s === cur ? ' selected' : '') + '>' + s + '</option>'; }).join('') + '</select></div>';
  }
  WB.on['book.threadNew'] = function (el, d) {
    var b = WB.book(d.book) || WB.scopeBook(), c = WB.craftOf(b.id);
    WB.modal({ title: '新增伏笔 · ' + b.title,
      body: '<div class="fld"><label>伏笔内容（用你自己的话）</label><input class="inp" id="thText" value="" placeholder="例如：旧钟停在 3:40" /></div>' +
        inputFld('埋设位置', 'thPlanted', '', '例如：ch07 / 第 7 章') +
        inputFld('计划兑现', 'thPlan', '', '例如：ch44 兑现 / 未计划') +
        stateFld('thState', '待兑现') +
        linkBox(b, c, []) +
        '<div class="note bound">伏笔状态是计划台账：<b>写进正文之后才算兑现</b>，不是正文事实。关联只指向已有对象，不复制内容。</div>',
      footer: '<button class="btn" data-action="close-modal">取消</button>' +
        '<button class="btn primary" data-action="book.threadSave" data-book="' + b.id + '" data-id="">保存伏笔</button>' });
  };
  WB.on['book.threadEdit'] = function (el, d) {
    var b = WB.book(d.book) || WB.scopeBook(), c = WB.craftOf(b.id);
    var t = WB.byId(storyStateOf(b.id).threads, d.id);
    if (!t) { WB.toast('这条伏笔已不存在（可能已被删除）', 'warn'); return; }
    WB.modal({ title: '编辑伏笔 · ' + t.id,
      body: '<div class="fld"><label>伏笔内容</label><input class="inp" id="thText" value="' + WB.esc(t.text || '') + '" /></div>' +
        inputFld('埋设位置', 'thPlanted', t.planted, '') +
        inputFld('计划兑现', 'thPlan', t.plan, '') +
        stateFld('thState', t.state) +
        linkBox(b, c, t.refs) +
        '<div class="note bound">只改这一条台账记录；<b>已写正文与已发布章节不会被改写</b>。</div>',
      footer: '<button class="btn" data-action="close-modal">取消</button>' +
        '<button class="btn primary" data-action="book.threadSave" data-book="' + b.id + '" data-id="' + WB.esc(t.id) + '">保存伏笔</button>' });
  };
  WB.on['book.threadSave'] = function (el, d) {
    var b = WB.book(d.book) || WB.scopeBook(), c = WB.craftOf(b.id);
    var st = storyStateOf(b.id);
    var text = fieldVal('thText');
    if (!text) { WB.toast('伏笔内容不能为空——先写一句你自己的话', 'warn'); return; }
    var refs = collectRefs();
    var t = d.id ? WB.byId(st.threads, d.id) : null;
    if (t) {
      t.text = text; t.planted = fieldVal('thPlanted') || '未指定'; t.plan = fieldVal('thPlan') || '未计划';
      t.state = fieldVal('thState') || t.state; t.refs = refs;
    } else {
      var n = 0;
      st.threads.forEach(function (x) { var m = /^F-(\d+)$/.exec(x.id || ''); if (m) n = Math.max(n, Number(m[1])); });
      var nid = 'F-' + (n + 1 < 10 ? '0' + (n + 1) : String(n + 1));
      st.threads.push({ id: nid, text: text, planted: fieldVal('thPlanted') || '未指定',
        plan: fieldVal('thPlan') || '未计划', state: fieldVal('thState') || '待兑现', refs: refs });
    }
    WB.closeModal(); WB.save(); WB.render();
    WB.toast(t ? '已更新伏笔与关联（正文与已发布章节不受影响）' : '已新增伏笔；状态是计划台账，写进正文才算兑现', 'ok');
  };
  WB.on['book.timelineNew'] = function (el, d) {
    var b = WB.book(d.book) || WB.scopeBook(), c = WB.craftOf(b.id);
    WB.modal({ title: '新增时序 · ' + b.title,
      body: '<div class="fld"><label>时间点</label><input class="inp" id="tlAt" value="" placeholder="例如：ch37– 或 第 3 天夜" /></div>' +
        inputFld('事件说明', 'tlNote', '', '例如：卷三：灯的来源逐步逼近') +
        linkBox(b, c, []) +
        '<div class="note bound">时序用于核对前后依赖；关联只指向本书已有对象。</div>',
      footer: '<button class="btn" data-action="close-modal">取消</button>' +
        '<button class="btn primary" data-action="book.timelineSave" data-book="' + b.id + '">保存时序</button>' });
  };
  WB.on['book.timelineSave'] = function (el, d) {
    var b = WB.book(d.book) || WB.scopeBook(), c = WB.craftOf(b.id);
    var at = fieldVal('tlAt'), note = fieldVal('tlNote');
    if (!at || !note) { WB.toast('时间点和事件说明都要填', 'warn'); return; }
    storyStateOf(b.id).timeline.push({ at: at, note: note, refs: collectRefs() });
    WB.closeModal(); WB.save(); WB.render();
    WB.toast('已新增时序记录，并关联到本书已有对象', 'ok');
  };
  WB.on['book.res'] = function (el, d) { WB.go('book', 'manuscript', { chapter: d.id }); };
})();
