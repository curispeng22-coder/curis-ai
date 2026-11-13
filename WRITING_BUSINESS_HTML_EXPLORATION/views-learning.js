/* ============================================================================
   views-learning.js — 写作经验（经验库与适用检查 / 经验详情与应用回访）
   底线：经验有适用范围、反例与使用回访；应用次数 ≠ 验证次数；
        不自动停书、不绕平台 AI 规则、不暗示真实后台持续运行。
   ========================================================================== */
(function () {
  var ui = WB.ui;

  WB.on['learn.pick'] = function (el, d) { WB.go('learning', 'detail', { id: d.key }, { replace: true }); };
  WB.on['learn.use'] = function (el, d) {
    var l = WB.learning(d.id);
    if (l.deactivated || l.accepted !== 'author') { WB.toast('只有作者接受且未停用的经验才能进入写作依据', 'warn'); return; }
    WB.modal({ title: '把经验带入下一次创作',
      body: ui.kv([['经验', WB.esc(WB.learning(d.id).text)], ['范围', WB.esc(WB.learning(d.id).scope)], ['反例', WB.esc(WB.learning(d.id).counter)]]) +
        '<div class="fld" style="margin-top:8px"><label>带到哪里</label><select class="sel" id="luWhere"><option value="ch44">第 44 章</option><option value="ch45">第 45 章</option><option value="outline:B-01">《夜行灯》后续大纲</option></select></div>' +
        '<div class="fld"><label>为什么适用、准备具体调整什么</label><textarea class="ta" id="luReason" placeholder="例如：第45章缩短支线，提前主冲突；不改变已发布章节。"></textarea></div>' +
        ui.note('bound', '作者确认后写入目标章或大纲的写作依据；不自动改正文。后续表现回到使用记录验证或质疑。跨书复用需另行授权。'),
      footer: '<button class="btn" data-action="close-modal">取消</button>' +
        '<button class="btn primary" data-action="learn.useDo" data-id="' + d.id + '">记录应用</button>' });
  };
  WB.on['learn.useDo'] = function (el, d) {
    var w = document.getElementById('luWhere').value, reason = document.getElementById('luReason').value.trim();
    if (!reason) { WB.toast('请说明为什么用于这里，以及准备改变什么', 'warn'); return; }
    WB.closeModal(); WB.act.learningUse(d.id, w, reason);
    if (w.indexOf('outline:') === 0) WB.go('book', 'craft', { bookId: w.slice(8), mode: 'outline' });
    else WB.go('book', 'manuscript', { bookId: WB.chapter(w).bookId, chapter: w, stage: 'write' });
  };
  WB.on['learn.followUp'] = function (el, d) {
    var u = WB.byId(WB.S.learningUsage, d.id);
    WB.modal({ title: '应用回访 · ' + u.target,
      body: ui.kv([['经验', WB.esc(WB.learning(u.learningId).text)], ['用于', WB.esc(u.where)], ['计划如何调整', WB.esc(u.reason || '未记录')],
        ['原始依据', WB.esc((u.source || []).join('、') || '早期记录未保存')], ['反例', WB.esc(u.counter || '早期记录未保存')], ['记录时间', WB.esc(u.at)],
        ['当前状态', u.decision === 'applied' ? '已应用' : u.decision === 'rejected' ? '被拒绝（未采用）' : '待决定'],
        ['回访结论', WB.esc(u.followUp || '尚无后续表现数据')]]) +
        ui.note('choice', '后续反馈会追加验证或反例；<b>不追溯改旧分析</b>。旧的应用记录保留。'),
      footer: '<button class="btn" data-action="learn.addVerify" data-id="' + u.id + '">追加一次验证（观察 7 日窗）</button>' +
        '<button class="btn" data-action="close-modal">关闭</button>' });
  };
  WB.on['learn.addVerify'] = function (el, d) {
    var u = WB.byId(WB.S.learningUsage, d.id), l = WB.learning(u.learningId);
    l.verified++;
    u.followUp = '已追加验证：ch39 的 7 日窗与邻章持平 → 计入反例候选。';
    WB.closeModal(); WB.save();
    WB.toast('已追加一次验证（验证次数 ' + l.verified + '／应用次数 ' + l.used + '，两者分开统计）', 'ok');
    WB.render();
  };

  /* ---------------- 经验库与适用检查 ---------------- */
  WB.register('learning.library', {
    render: function () {
      var S = WB.S;
      var rows = S.learnings.map(function (l) {
        var acc = l.deactivated ? WB.stBadge('已停用', 'wait')
          : l.accepted === 'author' ? WB.stBadge('作者已接受', 'published') : WB.stBadge('待验证', 'choice');
        return { attrs: ' class="clickable" data-action="learn.pick" data-key="' + l.id + '"',
          cells: [
            '<span class="strong">' + WB.esc(l.text) + '</span><div class="t3 xs">' + WB.esc(l.id) + ' · ' + WB.esc(l.kind) + '经验</div>',
            '<span class="sm">' + WB.esc(l.scope) + '</span><div class="t3 xs">' + WB.esc(l.platform + ' · ' + l.stage) + '</div>',
            l.evidence.map(function (e) { return '<span class="pill mono">' + WB.esc(e) + '</span>'; }).join(' ') +
              l.usedNote.length < 20 ? '' : '<div class="t3 xs">' + WB.esc(l.usedNote) + '</div>',
            '<span class="sm">应用 <b>' + l.used + '</b> · 验证 <b>' + l.verified + '</b></span>' +
              '<div class="t3 xs">' + (l.verified < l.used ? '验证落后于应用' : '验证与应用同步') + '</div>',
            acc,
            '<div class="btnrow"><button class="btn sm" data-action="learn.pick" data-key="' + l.id + '">详情</button>' +
              '<button class="btn sm" data-action="learn.use" data-id="' + l.id + '">用于下一章</button></div>'
          ] };
      });

      var usage = S.learningUsage;
      return ui.hdr('经验库与适用检查',
        '本书 / 跨章 / 授权跨作品的写作经验：正例、反例、适用范围与验证次数。避免一次成功被机械复用。',
        '<button class="btn" data-action="nav.view" data-area="learning" data-view="detail">看一条经验详情</button>',
        '<span>经验 ' + S.learnings.length + ' 条</span><span class="t4">|</span><span>使用记录 ' + usage.length + ' 条</span>' +
        '<span class="t4">|</span><span>跨作品复用需作者授权</span>') +

        ui.panel({ title: '经验条目', sub: '每条都可被质疑、修订与停用', tight: true,
          body: ui.tbl(['经验', '适用范围', '依据与反例', '应用 / 验证', '接受状态', '操作'], rows),
          footer: '<span>好经验与坏经验（负向）都沉淀；数据缺失时只保存「待验证创作经验」。</span>' }) +

        ui.panel({ title: '适用检查 · 为什么建议 / 为何不适用', body:
          '<div class="grid g2">' +
          '<div><div class="sm strong" style="margin-bottom:6px">本章可用的经验</div>' +
          S.learnings.filter(function (l) { return !l.deactivated; }).map(function (l) {
            return '<div class="as-w"><div class="wt">' + WB.esc(l.text) + '</div>' +
              '<div class="ws">为什么建议：' + WB.esc(l.evidence.join('、')) + ' 的证据支持<br>' +
              '反例提醒：' + WB.esc(l.counter) + '</div></div>';
          }).join('') + '</div>' +
          '<div><div class="sm strong" style="margin-bottom:6px">不宜直接套用</div>' +
          '<div class="as-w"><div class="wt">《雾港来信》的慢热结构</div><div class="ws">与本作节奏取向相反 → 只作对照，不作模板。</div></div>' +
          '<div class="as-w"><div class="wt">跨作品复用</div><div class="ws">尚未授权：世界设定与私稿不会自动共享；只复用被授权且抽象化的部分。</div></div>' +
          '</div></div>' }) +

        ui.panel({ title: '使用记录与回访', tight: true, body: ui.tbl(['记录', '经验', '用于', '决定', '时间', '回访'],
          usage.map(function (u) {
            var d = u.decision === 'applied' ? ['已应用', 'published'] : u.decision === 'rejected' ? ['被拒绝', 'wait'] : ['待决定', 'choice'];
            return { cells: [WB.esc(u.id), WB.esc(u.learningId), WB.esc(u.where + ' · ' + u.target) + '<div class="t3 xs">计划调整：' + WB.esc(u.reason || '未记录') + '</div>',
              WB.stBadge(d[0], d[1]), WB.esc(u.at),
              u.followUp ? '<span class="sm">' + WB.esc(u.followUp) + '</span>' : '<button class="btn sm" data-action="learn.followUp" data-id="' + u.id + '">回访</button>'] };
          })) ,
          footer: '<span>被拒绝的经验同样留档：说明了为什么不适用。</span>' });
    },
    aside: function () {
      var S = WB.S;
      return WB.asBlock('责任人', WB.ownerHtml('E-01') + ' / ' + WB.ownerHtml('E-04') + '<div class="sm t3" style="margin-top:6px">编辑引用经验；分析提供依据。</div>') +
        WB.asBlock('经验范围', '<div class="sm t2">本章 → 本书跨章 → 作者授权跨作品。<br>跨书只复用被授权且抽象化的经验。</div>') +
        WB.asBlock('不做什么', '<div class="sm t2">· 不自动停书<br>· 不绕平台 AI 规则<br>· 不暗示真实后台持续运行</div>');
    }
  });

  /* ---------------- 经验详情与应用回访 ---------------- */
  WB.register('learning.detail', {
    render: function (ctx) {
      var S = WB.S;
      var id = ctx.params.id || 'L-01';
      var l = WB.learning(id) || S.learnings[0];
      l = WB.learning(id) ? l : S.learnings[0];
      var usage = S.learningUsage.filter(function (u) { return u.learningId === l.id; });
      var fromAnalysis = S.analyses.filter(function (a) { return l.evidence.indexOf(a.id) >= 0; })[0];

      return ui.hdr('经验详情与应用回访 · ' + WB.esc(l.id),
        WB.esc(l.text),
        '<button class="btn" data-action="learn.use" data-id="' + l.id + '">用于下一章</button>' +
        '<button class="btn" data-action="nav.view" data-area="learning" data-view="library">回经验库</button>',
        '<span>' + WB.esc(l.kind) + '经验</span><span class="t4">|</span><span>范围：' + WB.esc(l.scope) + '</span>' +
        '<span class="t4">|</span>' + (l.deactivated ? WB.stBadge('已停用', 'wait') : l.accepted === 'author' ? WB.stBadge('作者已接受', 'published') : WB.stBadge('待验证', 'choice'))) +

        '<div class="scopebar"><div class="sb-row"><span class="sl-lb">选择经验</span>' +
        ui.chips(S.learnings.map(function (x) { return [x.id, x.id + ' · ' + x.kind]; }), l.id, 'learn.pick') + '</div></div>' +

        '<div class="grid" style="grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:12px;align-items:start">' +
        '<div>' +
        ui.panel({ title: '来源与依据', body: ui.kv([
          ['来源', l.evidence.map(function (e) { return '<span class="pill mono">' + WB.esc(e) + '</span>'; }).join(' ') + '（分析 / 评论 / 审校）'],
          ['平台与阶段', WB.esc(l.platform + ' · ' + l.stage)],
          ['可信理由', WB.esc(l.usedNote)],
          ['尚未排除', WB.esc(l.notExcluded)],
          ['接受时间', WB.esc(l.acceptedAt || '—') + '（' + (l.accepted === 'author' ? '作者接受' : '待作者确认') + '）']
        ]) +
          (fromAnalysis ? '<div class="btnrow" style="margin-top:8px"><button class="btn sm" data-action="nav.view" data-area="audience" data-view="attribution">回到原分析 ' + WB.esc(fromAnalysis.id) + '</button></div>' : '') }) +

        ui.panel({ title: '反证与边界', body:
          '<div class="note choice"><b>反例：</b>' + WB.esc(l.counter) + '</div>' +
          '<div class="note bound"><b>反向使用时要注意：</b>若在信息章或收束章套用，可能加重刻意感。经验不是规则。</div>' }) +

        ui.panel({ title: '应用与验证', tight: true, body: ui.tbl(['记录', '用于', '决定', '回访'],
          usage.length ? usage.map(function (u) {
            var d = u.decision === 'applied' ? ['已应用', 'published'] : u.decision === 'rejected' ? ['被拒绝', 'wait'] : ['待决定', 'choice'];
            return { cells: [WB.esc(u.id), WB.esc(u.where + ' · ' + u.target), WB.stBadge(d[0], d[1]),
              u.followUp ? '<span class="sm">' + WB.esc(u.followUp) + '</span>' : '<button class="btn sm" data-action="learn.followUp" data-id="' + u.id + '">回访</button>'] };
          }) : [{ cells: ['—', '尚未应用于任何章', '—', '—'] }]),
          footer: '<span>应用 <b>' + l.used + '</b> 次 · 验证 <b>' + l.verified + '</b> 次 —— 两者分开统计。</span>' }) +
        '</div>' +

        '<div>' +
        ui.panel({ title: '操作', body:
          '<div class="btnrow" style="flex-direction:column;align-items:stretch">' +
          '<button class="btn primary" data-action="act.l" data-fn="learningDecide" data-a1="' + l.id + '" data-a2="accept">接受（限定范围）</button>' +
          '<button class="btn" data-action="act.l" data-fn="learningDecide" data-a1="' + l.id + '" data-a2="question">标记待质疑（使用前显示反例）</button>' +
          '<button class="btn" data-action="act.l" data-fn="learningDecide" data-a1="' + l.id + '" data-a2="deactivate">停用（保留历史使用）</button>' +
          '<button class="btn" data-action="learn.use" data-id="' + l.id + '">用于下一章</button>' +
          '</div>',
          footer: '<span>停用不改旧分析、不改历史使用记录。</span>' }) +

        ui.panel({ title: '回流到创作', body:
          '<div class="sm t2">可用于：下一章目标、后续 Outline 提案、经营决定依据。<br>引用时会带上范围与反例；作者可拒绝套路化建议。</div>' +
          '<div class="btnrow" style="margin-top:8px">' +
          '<button class="btn sm" data-action="nav.view" data-area="book" data-view="manuscript">下一章上下文</button>' +
          '<button class="btn sm" data-action="nav.view" data-area="market" data-view="direction">方向提案</button>' +
          '<button class="btn sm" data-action="nav.view" data-area="operate" data-view="plan">经营决定</button></div>' }) +

        ui.panel({ title: '版本与失效', body:
          '<div class="sm t2">· 经验修订不追溯改旧分析<br>· 旧应用保留原引用<br>· 失效原因会记录，便于下次避免</div>' +
          (l.deactivated ? '<div class="note" style="margin-top:8px">该经验已停用：仍可用于回顾，但不再作为建议来源。</div>' : '') });
        '</div></div>';
    },
    aside: function (ctx) {
      var l = WB.learning(ctx.params.id || 'L-01') || WB.S.learnings[0];
      return WB.asBlock('当前对象', '<div class="as-w"><div class="wt">' + WB.esc(l.text) + '</div><div class="ws">范围：' + WB.esc(l.scope) +
          '<br>反例：' + WB.esc(l.counter) + '</div></div>') +
        WB.asBlock('责任人', WB.ownerHtml('E-01')) +
        WB.asBlock('提醒', '<div class="sm t2">一次成功不等于可复用结论；范围越小越安全。</div>');
    }
  });
})();
