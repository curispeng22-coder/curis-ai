/* ============================================================================
   views-market.js — 市场与方向（市场观察 / 持续关注 / 参考与拆解 / 创作方向）
   ========================================================================== */
(function () {
  var ui = WB.ui;

  function growthRows() {
    var snaps = WB.S.marketSnapshots.filter(function (x) { return x.watchId === 'W-01'; }).slice().sort(function (a, b) { return a.at.localeCompare(b.at); });
    if (snaps.length < 2) return [];
    var first = snaps[0], last = snaps[snaps.length - 1];
    if (first.platform !== last.platform || first.source !== last.source || first.scope !== last.scope || first.metric !== last.metric || first.unit !== last.unit) return [];
    return last.entries.map(function (end) {
      var start = first.entries.filter(function (x) { return x.id === end.id; })[0];
      if (!start || typeof start.value !== 'number' || typeof end.value !== 'number' || start.value <= 0) return null;
      return { item: end, first: start, a: first, b: last, delta: end.value - start.value,
        pct: Math.round((end.value - start.value) / start.value * 1000) / 10, rank: start.rank - end.rank };
    }).filter(Boolean).sort(function (a, b) { return b.pct - a.pct; });
  }

  /* ---------------- 行动 ---------------- */
  WB.on['market.openSource'] = function (el, d) {
    WB.modal({ title: '公开来源：' + d.name,
      body: '<p>本原型的来源指认为公开页面。为保持离线可运行，原型<b>不执行任何外部跳转或联网读取</b>。</p>' +
        WB.ui.kv([['来源类型', WB.esc(d.kind || '公开页面')], ['范围', WB.esc(d.scope || '—')], ['采集方式', WB.esc(d.method || '正常授权浏览器浏览公开页面')]]) +
        '<div class="note bound">未登录作者后台、未发布、未读取真实稿费；公开页面内容不构成平台能力证明。</div>',
      footer: '<button class="btn" data-action="close-modal">关闭</button>' });
  };
  WB.on['market.refDetail'] = function (el, d) {
    var r = WB.byId(WB.S.references, d.id);
    WB.openDrawer({ title: r.title, sub: WB.esc(r.platform + ' · ' + r.genre + (r.sample ? ' · 虚构样例条目' : r.own ? ' · 自有作品' : '')),
      wide: true,
      body: ui.kv([['来源', WB.esc(r.source)], ['原文范围', WB.esc(r.scope)], ['主题', WB.esc(r.theme)], ['冲突', WB.esc(r.conflict)],
        ['角色', WB.esc(r.character)], ['结构', WB.esc(r.structure)], ['节奏', WB.esc(r.rhythm)], ['文风', WB.esc(r.style)]]) +
        ui.note('choice', '<b>局限：</b>' + WB.esc(r.limit)) +
        ui.note('bound', '参考不是本书的 Canon：它只能进入定位与章目标，不改变世界设定。'),
      footer: '<button class="btn" data-action="act.ref" data-fn="refSave" data-a1="' + r.id + '">' + (r.saved ? '取消保存' : '保存参考') + '</button>' +
        '<button class="btn primary" data-action="act.ref" data-fn="refToDirection" data-a1="' + r.id + '">用于创作方向</button>' });
  };
  WB.on['market.refSave'] = function (el, d) { WB.act.refSave(d.id); WB.render(); };
  WB.on['market.research'] = function (el, d) {
    WB.S.__sel.research = d.id;
    WB.go('market', 'direction', { from: d.id });
    WB.toast('已把 ' + d.id + ' 带进方向提案：来源、日期、范围与未知项随行', 'ok');
  };
  WB.on['market.obsSaveRef'] = function (el, d) {
    var o = WB.byId(WB.S.marketObservations, d.id);
    if (WB.S.references.filter(function (r) { return r.fromObs === o.id; }).length) { WB.toast('该观察已生成参考条目'); return; }
    WB.S.references.push({ id: 'R-0' + (WB.S.references.length + 1), title: '《' + (o.scope.split('·')[0] || '观察').trim() + '》（虚构样例）',
      platform: o.platform, genre: '待归类', source: o.scope + '（' + o.at + ' 快照）', scope: '公开榜单元数据；未导入正文',
      theme: '待补充', conflict: '待补充', character: '待补充', structure: '待补充', rhythm: '待补充', style: '待补充',
      limit: o.limit, sample: true, saved: true, fromObs: o.id });
    WB.save(); WB.toast('已保存为参考（带来源与局限）；可在「参考与拆解」补充拆解', 'ok'); WB.render();
  };
  WB.on['market.watchEdit'] = function (el, d) {
    var w = WB.watch(d.id);
    WB.modal({ title: '编辑关注 · ' + w.name,
      body: '<div class="fld"><label>名称</label><input class="inp" id="wName" value="' + WB.esc(w.name) + '"></div>' +
        '<div class="fld"><label>平台与来源</label><input class="inp" id="wSource" value="' + WB.esc(w.source) + '"></div>' +
        '<div class="fld"><label>榜单 / 分类 / 研究范围</label><input class="inp" id="wScope" value="' + WB.esc(w.scope || '') + '"></div>' +
        '<div class="fld"><label>题材 / 关键词 / 新书或指定作品</label><input class="inp" id="wFocus" value="' + WB.esc(w.focus || '') + '"></div>' +
        '<div class="fld"><label>观察窗口</label><input class="inp" id="wWindow" value="' + WB.esc(w.window || '') + '"></div>' +
        '<div class="fld"><label>关注指标（实际可得才录入）</label><input class="inp" id="wMetrics" value="' + WB.esc(w.metrics || '') + '"></div>' +
        '<div class="fld"><label>检查频率</label><select class="sel" id="wCad">' +
        ['每日 09:00', '每 2 日 09:00', '每周一 09:00', '暂停（仅保留历史）'].map(function (c) {
          return '<option' + (c === w.cadence ? ' selected' : '') + '>' + c + '</option>';
        }).join('') + '</select></div>' +
        ui.kv([['执行方式', WB.esc(w.method)], ['预算', WB.esc(w.budget || '未设置')], ['下次检查', WB.esc(w.next || '未安排')]]) +
        '<div class="note bound">此处维护研究范围；实际检查仍为 Mock，不默认实时全网。</div>',
      footer: '<button class="btn" data-action="close-modal">取消</button><button class="btn primary" data-action="market.watchEditSave" data-id="' + w.id + '">保存</button>' });
  };
  WB.on['market.watchEditSave'] = function (el, d) {
    var v = document.getElementById('wCad').value;
    var w = WB.watch(d.id);
    var name = document.getElementById('wName').value.trim(), source = document.getElementById('wSource').value.trim(), scope = document.getElementById('wScope').value.trim();
    if (!name || !source || !scope) { WB.toast('请填写名称、来源和观察范围', 'warn'); return; }
    w.name = name; w.source = source; w.scope = scope;
    w.focus = document.getElementById('wFocus').value.trim();
    w.window = document.getElementById('wWindow').value.trim();
    w.metrics = document.getElementById('wMetrics').value.trim();
    if (v.indexOf('暂停') === 0) { w.state = 'paused'; w.next = null; w.cadence = w.cadence; w.pausedBy = '作者'; }
    else { w.cadence = v; w.state = w.state === 'failed' ? 'failed' : 'active'; if (w.state === 'active' && !w.next) w.next = '等待下次计划检查'; }
    WB.closeModal(); WB.save(); WB.toast('关注配置已更新（真实写入本机演示状态）', 'ok'); WB.render();
  };
  WB.on['market.snapshotDetail'] = function (el, d) {
    var x = WB.byId(WB.S.marketSnapshots, d.id);
    WB.openDrawer({ title: '观察快照 · ' + x.at, sub: x.platform + ' · ' + x.scope + ' · Mock',
      body: ui.kv([['榜单来源', WB.esc(x.source)], ['指标与单位', WB.esc(x.metric + '（' + x.unit + '）')], ['证据', WB.esc(x.evidence)]]) +
        ui.tbl(['作品', '原始榜位', '该次读数'], x.entries.map(function (e) { return { cells: [WB.esc(e.title), String(e.rank), e.value == null ? WB.unknown('Unknown') : String(e.value) + ' ' + WB.esc(x.unit)] }; })) +
        ui.note('bound', '所有数值是虚构演示快照；真实平台字段、口径和可获取性尚未核验。'),
      footer: '<button class="btn" data-action="close-drawer">返回市场观察</button>' });
  };
  WB.on['market.growthRef'] = function (el, d) {
    var row = growthRows().filter(function (x) { return x.item.id === d.id; })[0];
    if (!row) { WB.toast('缺少同口径历史，无法形成增长参考', 'warn'); return; }
    var ref = WB.S.references.filter(function (x) { return x.marketItemId === row.item.id; })[0];
    if (!ref) {
      ref = { id: 'R-M' + Date.now(), marketItemId: row.item.id, title: row.item.title, platform: row.b.platform, genre: row.item.genre,
        source: row.a.id + ' → ' + row.b.id + ' · ' + row.b.source, scope: row.b.scope + '；仅榜单元数据与 Mock 观察值',
        theme: '待研究', conflict: '待研究', character: '待研究', structure: '待研究', rhythm: '待研究', style: '待研究',
        limit: '增长相关性不解释原因；需阅读合法可见文本并检查反例，再形成 Pattern。', sample: true, saved: true };
      WB.S.references.push(ref); WB.save();
    }
    WB.closeDrawer();
    WB.go('market', 'references');
    WB.on['market.refDetail'](null, { id: ref.id });
  };

  /* ---------------- 市场观察 ---------------- */
  WB.register('market.observations', {
    render: function () {
      var S = WB.S;
      var rows = S.marketObservations.map(function (o) {
        var w = o.watchId ? WB.watch(o.watchId) : null;
        return { attrs: ' class="clickable" data-action="market.obsDetail" data-id="' + o.id + '"',
          cells: [
            '<span class="strong">' + WB.esc(o.at) + '</span><div class="t3 xs">' + WB.esc(o.platform) + '</div>',
            '<span class="sm">' + WB.esc(o.scope) + '</span>',
            '<span class="sm">' + WB.esc(o.change) + '</span>',
            '<span class="sm t2">' + WB.esc(o.limit) + '</span>',
            o.partial ? WB.stBadge('仅标题/摘要可读', 'unknown') : WB.stBadge('公开页面可读', 'published')
          ] };
      });
      var growth = growthRows();
      var snaps = S.marketSnapshots.slice().sort(function (a, b) { return b.at.localeCompare(a.at); });
      var genre = {};
      growth.forEach(function (r) { (genre[r.item.genre] || (genre[r.item.genre] = [])).push(r); });
      return ui.hdr('市场观察',
        '平台、题材、榜单与来源的时间快照：找机会，而不是凭热度数字猜。每次快照都带来源、日期、范围与局限。',
        '<button class="btn" data-action="nav.view" data-area="market" data-view="watches">持续关注管理</button>' +
        '<button class="btn primary" data-action="nav.view" data-area="market" data-view="direction">形成方向提案</button>',
        '<span>覆盖范围：番茄公开榜单 · 起点公开分类入口 · 番茄公告目录（部分仅标题可读）</span>' +
        '<span class="t4">|</span><span>更新：' + WB.esc(S.watches[0].last) + '</span>' +
        '<span class="t4">|</span><span>不默认实时全网</span>') +

        ui.panel({ title: '近期增长 · 同范围历史对比', sub: 'Mock · ' + (snaps.length ? snaps[snaps.length - 1].at + ' → ' + snaps[0].at : '缺历史'), tight: true,
          body: growth.length ? ui.tbl(['作品 / 阶段', '观察值变化', '增幅', '榜位变化', '下一步'], growth.map(function (r) { return { cells: [
            '<b>' + WB.esc(r.item.title) + '</b><div class="t3 xs">' + WB.esc(r.item.stage + ' · ' + r.item.genre) + '</div>',
            r.first.value + ' → ' + r.item.value + '（' + (r.delta >= 0 ? '+' : '') + r.delta + ' ' + WB.esc(r.b.unit) + '）',
            (r.pct >= 0 ? '+' : '') + r.pct + '%',
            r.first.rank + ' → ' + r.item.rank + '（' + (r.rank >= 0 ? '↑' : '↓') + Math.abs(r.rank) + '）',
            '<button class="btn sm" data-action="market.growthRef" data-id="' + r.item.id + '">加入参考并拆解</button>'
          ] }; })) : WB.unknown('缺少可比较的快照'),
          footer: '只比较同平台、来源、范围、指标、单位和同一作品。按相对增幅排列；新书加速是研究线索，不是平台推荐结论。全部读数为 Mock。' }) +
        ui.panel({ title: '题材升温线索', tight: true,
          body: Object.keys(genre).map(function (g) { return '<div class="sm" style="margin:8px 0"><b>' + WB.esc(g) + '</b> · 样本 ' + genre[g].length + ' 本；其中新书 ' + genre[g].filter(function (r) { return r.item.stage === '新书'; }).length + ' 本。' +
            ' 观察窗 ' + WB.esc(genre[g][0].a.at + ' → ' + genre[g][0].b.at) + '；证据 ' + WB.esc(genre[g][0].a.id + ' / ' + genre[g][0].b.id) + '</div>'; }).join('') +
            ui.note('bound', '仅当前榜单 3 本虚构样例，不足以推断整个市场或题材偏好变化。先加入参考，拆解具体作品。') }) +
        ui.panel({ title: '同一观察范围的快照历史', tight: true,
          body: ui.tbl(['时间', '来源与范围', '作品数', '证据', '查看'], snaps.map(function (x) { return { cells: [WB.esc(x.at), WB.esc(x.platform + ' · ' + x.scope), String(x.entries.length), WB.esc(x.evidence), '<button class="btn sm" data-action="market.snapshotDetail" data-id="' + x.id + '">原始榜位</button>'] }; })),
          footer: 'T1 / T2 / T3 原样保留；缺失指标保持 Unknown，不从名次推算收入。' }) +
        ui.panel({ title: '观察快照', sub: S.marketObservations.length + ' 条 · 均可追溯到来源',
          tight: true, body: ui.tbl(['日期 / 平台', '范围', '变化', '不能据此得出什么', '可读程度'], rows),
          footer: '<span>' + WB.esc(WB.S.meta.caseNote) + '</span>' }) +

        ui.panel({ title: '覆盖范围与缺口', body:
          '<div class="grid g2">' +
          '<div><div class="sm strong" style="margin-bottom:6px">已知可读</div><ul class="sm t2" style="padding-left:18px;margin:0">' +
          '<li>番茄公开榜单：排名、在读、完结与更新信息</li><li>起点公开分类/推荐入口</li><li>公告目录（标题）</li></ul></div>' +
          '<div><div class="sm strong" style="margin-bottom:6px">本轮未确认</div><ul class="sm t2" style="padding-left:18px;margin:0">' +
          '<li>起点榜单页面正文为空 → 不报告字段</li><li>公告正文跳转失败 → 不推测规则</li>' +
          '<li>内部推荐权重与真实收入（不可得）</li></ul></div></div>' +
          ui.note('bound', '没有公开证据不等于没有能力；但也不能把「平台支持某数据」当作「Curis 可用」。') })
      ;
    },
    aside: function () {
      var S = WB.S;
      return WB.asBlock('来源维护', S.watches.map(function (w) {
        var m = { active: ['正常', 'working'], paused: ['已暂停（作者）', 'wait'], failed: ['读取失败', 'unknown'] };
        return '<div class="as-w clickable" data-action="nav.view" data-area="market" data-view="watches">' +
          '<div class="wt">' + WB.esc(w.name) + '</div><div class="ws">' + WB.st(m[w.state][0], m[w.state][1]) +
          '<br>最近 ' + WB.esc(w.last || '—') + ' · 下次 ' + WB.esc(w.next || '未计划') +
          (w.fail ? '<br><span class="t3">失败：' + WB.esc(w.fail) + '</span>' : '') + '</div></div>';
      }).join('')) +
      WB.asBlock('责任人', WB.ownerHtml('E-02') + '<div class="sm t3" style="margin-top:6px">研究责任：把来源变成可用依据；不代替作者判断方向。</div>') +
      WB.asBlock('近期待办', '<div class="sm t2">公告目录正文读取失败 → 保持失败与原因，等待渠道可读（下次 09-23）。</div>');
    }
  });

  WB.on['market.obsDetail'] = function (el, d) {
    var o = WB.byId(WB.S.marketObservations, d.id);
    WB.openDrawer({ title: '市场快照 · ' + o.at, sub: WB.esc(o.platform + ' · ' + o.scope),
      body: ui.kv([['变化', WB.esc(o.change)], ['局限', WB.esc(o.limit)], ['来源方式', '正常授权浏览器浏览公开页面'], ['采集时点', WB.esc(o.at)]]) +
        ui.note('bound', '单次排名不能说明趋势，也不能转化为营收预测。'),
      footer: '<button class="btn" data-action="market.openSource" data-name="' + WB.esc(o.scope) + '" data-kind="观察快照" data-scope="' + WB.esc(o.scope) + '">打开原站（说明）</button>' +
        '<button class="btn" data-action="market.obsSaveRef" data-id="' + o.id + '">保存为参考</button>' +
        '<button class="btn primary" data-action="market.research" data-id="' + o.id + '">研究此方向</button>' });
  };

  /* ---------------- 持续关注管理 ---------------- */
  WB.register('market.watches', {
    render: function () {
      var S = WB.S;
      var rows = S.watches.map(function (w) {
        var m = { active: ['正常', 'working'], paused: ['已暂停', 'wait'], failed: ['读取失败', 'unknown'] };
        return { cells: [
          '<span class="strong">' + WB.esc(w.name) + '</span><div class="t3 xs">' + WB.esc(w.kind) + ' · ' + WB.esc(w.source) + '<br>范围：' + WB.esc(w.scope || '待设置') + '<br>重点：' + WB.esc(w.focus || '待设置') + '</div>',
          '<span class="sm">' + WB.esc(w.method) + '</span><div class="t3 xs">预算：' + WB.esc(w.budget || '未设置') + '</div>',
          '<span class="sm">' + WB.esc(w.cadence) + '</span><div class="t3 xs">窗口：' + WB.esc(w.window || '待设置') + '<br>指标：' + WB.esc(w.metrics || '待设置') + '</div>',
          '<span class="sm">' + WB.esc(w.last || '尚未运行') + '</span><div class="t3 xs">下次：' + WB.esc(w.next || '—') + '</div>',
          WB.st(m[w.state][0], m[w.state][1]) + (w.fail ? '<div class="t3 xs">' + WB.esc(w.fail) + '</div>' : '') +
            (w.pausedBy ? '<div class="t3 xs">暂停人：' + WB.esc(w.pausedBy) + '</div>' : ''),
          '<div class="btnrow">' +
            (w.state === 'paused'
              ? '<button class="btn sm" data-action="act.w" data-fn="watchToggle" data-a1="' + w.id + '">恢复</button>'
              : '<button class="btn sm" data-action="act.w" data-fn="watchToggle" data-a1="' + w.id + '">暂停</button>') +
            '<button class="btn sm" data-action="act.w" data-fn="watchCheck" data-a1="' + w.id + '">立即检查</button>' +
            '<button class="btn sm" data-action="market.watchEdit" data-id="' + w.id + '">编辑</button>' +
            '<button class="btn sm ghost" data-action="act.w" data-fn="watchRemove" data-a1="' + w.id + '">移除</button>' +
          '</div>'
        ] };
      });
      return ui.hdr('持续关注管理',
        '关注的是「可维护的扫描」，不是假自动：每条关注都显示状态、方式、频率、最近与下次、失败原因。',
        '<button class="btn primary" data-action="act.w" data-fn="watchAdd">添加关注</button>',
        '<span>改动会真实写入本机演示状态</span><span class="t4">|</span><span>平台执行可以 Mock，关注配置不可假</span>') +

        ui.panel({ title: '关注列表', sub: S.watches.length + ' 条', tight: true,
          body: ui.tbl(['关注', '扫描方式', '频率', '最近 / 下次', '状态', '操作'], rows),
          footer: '<span>失败保留原状；暂停保留历史快照；移除不回滚已产生的观察。</span>' }) +

        ui.panel({ title: '失败与等待说明', body:
          '<div class="note bound"><b>W-03 番茄 · 创作者公告目录</b><br>本轮公告正文页跳转失败。失败原因已记录，下一次检查 09-23。' +
          '不代替阅读，也不推测规则内容 —— 未知就保持未知。</div>' +
          '<div class="note"><b>为什么不做「实时全网」</b><br>扫描频率由授权预算、来源限制与任务需要决定；浏览器只在正常允许访问时操作。</div>' });
    },
    aside: function () {
      return WB.asBlock('责任人', WB.ownerHtml('E-02')) +
        WB.asBlock('相关 Work', WB.S.works.filter(function (w) { return w.area === 'market'; }).map(function (w) { return WB.workHtml(w); }).join('')) +
        WB.asBlock('可用方式', '<div class="sm t2">合法 API（若真实有权可用）→ 正常授权浏览器 → 人工贴链接/截图/文件。<br>本轮均为公开页面的正常浏览。</div>');
    }
  });

  /* ---------------- 参考与拆解 ---------------- */
  WB.register('market.references', {
    render: function () {
      var S = WB.S;
      return ui.hdr('参考与拆解',
        '把「我读过什么」变成可用依据：来源、原文范围、六维拆解与局限一起保存；参考不成为本书的 Canon。',
        '<button class="btn" data-action="nav.view" data-area="market" data-view="observations">回到市场观察</button>') +

        '<div class="grid g2">' + S.references.map(function (r) {
          return '<section class="pnl" style="margin-bottom:12px"><div class="pnl-h"><div class="pnl-t">' + WB.esc(r.title) +
            (r.sample ? ' <span class="chip static">虚构样例</span>' : r.own ? ' <span class="chip static">自有作品</span>' : '') +
            '</div><div class="pnl-a">' + (r.saved ? WB.stBadge('已保存', 'published') : WB.stBadge('未保存', 'wait')) + '</div></div>' +
            '<div class="pnl-body">' +
            '<div class="sm"><b>' + WB.esc(r.conflict) + '</b></div>' +
            '<div class="sm t2" style="margin-top:4px">主题：' + WB.esc(r.theme) + ' · 节奏：' + WB.esc(r.rhythm) + '</div>' +
            ui.src(WB.esc(r.source) + ' · 范围：' + WB.esc(r.scope)) +
            '<div class="note bound" style="margin-top:8px">' + WB.esc(r.limit) + '</div>' +
            '</div><div class="pnl-f"><div class="btnrow">' +
            '<button class="btn sm" data-action="market.refDetail" data-id="' + r.id + '">查看完整拆解</button>' +
            '<button class="btn sm" data-action="market.refSave" data-id="' + r.id + '">' + (r.saved ? '取消保存' : '保存参考') + '</button>' +
            '<button class="btn sm primary" data-action="market.research" data-id="' + r.id + '">用于方向</button>' +
            '</div></div></section>';
        }).join('') + '</div>' +

        ui.panel({ title: 'Pattern 候选', sub: '从参考中提炼、可被拒绝的候选，不是规则',
          body: S.patterns.map(function (p) {
            return '<div class="stack" style="margin-bottom:12px">' +
              '<div class="row-t">' + WB.esc(p.text) + WB.stBadge(p.state, 'choice') + '</div>' +
              '<div class="sm t2">适用：' + WB.esc(p.scope) + '</div>' +
              '<div class="sm">反例：' + WB.esc(p.counter) + '</div>' +
              '<div class="sm t2">使用限制：' + WB.esc(p.caution) + '</div>' +
              '<div class="t3 xs">来自：' + WB.esc(p.from.join('、')) + '</div></div>';
          }).join(''),
          footer: '<span>Pattern 进入方向与章目标；不写入 Canon，也不自动应用。</span>' });
    },
    aside: function () {
      return WB.asBlock('参考使用规则', '<div class="sm t2">· 热门作品默认只导入链接、元数据与合法片段<br>· 不绕付费/DRM，不默认整本下载或训练模型<br>· 「风格蒸馏」限定为叙事特征总结与作者自身偏好对照，不声称已训练专属模型</div>') +
        WB.asBlock('责任', WB.ownerHtml('E-02') + ' / ' + WB.ownerHtml('E-01')) +
        WB.asBlock('相关 Work', WB.workHtml(WB.S.works.filter(function (w) { return w.area === 'market'; })[0]));
    }
  });

  /* ---------------- 创作方向提案 ---------------- */
  WB.register('market.direction', {
    render: function (ctx) {
      var S = WB.S, from = ctx.params.from;
      var d1 = WB.byId(S.directions, 'D-01'), d2 = WB.byId(S.directions, 'D-02');

      function card(d) {
        var decided = d.status === 'accepted' || d.status === 'rejected';
        return '<section class="pnl"><div class="pnl-h"><div class="pnl-t">' + WB.esc(d.title) +
          ' ' + (d.status === 'accepted' ? WB.stBadge('已接受', 'published') : d.status === 'rejected' ? WB.stBadge('已拒绝', 'wait') : WB.stBadge('待决定', 'choice')) +
          '</div><div class="pnl-a"><span class="t3 xs">' + WB.esc(d.id) + '</span></div></div>' +
          '<div class="pnl-body">' +
          '<div class="grid g2" style="gap:10px">' +
          '<div class="fld"><label>平台 / 读者</label><div class="sm">' + WB.esc(d.platform) + ' · ' + WB.esc(d.reader) + '</div></div>' +
          '<div class="fld"><label>题材 / 形式</label><div class="sm">' + WB.esc(d.genre) + '</div></div>' +
          '<div class="fld"><label>原创核心</label><div class="sm">' + WB.esc(d.core) + '</div></div>' +
          '<div class="fld"><label>作者希望保留</label><div class="sm">' + WB.esc(d.keep) + '</div></div>' +
          '<div class="fld"><label>目标</label><div class="sm">' + WB.esc(d.goal) + '</div></div>' +
          '<div class="fld"><label>与参考的差异</label><div class="sm">' + WB.esc(d.diff) + '</div></div>' +
          '</div>' +
          '<div class="hr"></div>' +
          '<div class="sm"><b>风险：</b>' + WB.esc(d.risk) + '</div>' +
          '<div class="sm t2"><b>未知：</b>' + WB.esc(d.unknown) + '</div>' +
          '<div class="sm t3" style="margin-top:4px">引用：' + WB.esc(d.refs.join('、')) + '</div>' +
          (d.appliedTo ? '<div class="note info" style="margin-top:8px">接受后应用：' + WB.esc(d.appliedTo) + ' · ' + WB.esc(d.acceptedAt || '') + '</div>' : '') +
          (!decided ? '<div class="hr"></div><div class="fld"><label>作者补充 / 修改（会真实保存）</label>' +
            '<textarea class="ta" data-change="dir.edit" data-id="' + d.id + '" data-field="core">' + WB.esc(d.core) + '</textarea></div>' : '') +
          '</div>' +
          '<div class="pnl-f"><div class="btnrow">' +
          (decided
            ? '<button class="btn sm" data-action="act.d" data-fn="directionDecide" data-a1="' + d.id + '" data-a2="accept">重新确认接受</button>' +
              '<button class="btn sm ghost" data-action="nav.view" data-area="book" data-view="library">去作品库</button>'
            : '<button class="btn sm primary" data-action="act.d" data-fn="directionDecide" data-a1="' + d.id + '" data-a2="accept">接受方向</button>' +
              '<button class="btn sm" data-action="act.d" data-fn="directionDecide" data-a1="' + d.id + '" data-a2="reject">拒绝</button>' +
              '<button class="btn sm ghost" data-action="nav.view" data-area="market" data-view="references">再看参考</button>') +
          '</div></div></section>';
      }

      return ui.hdr('创作方向提案',
        '热门适配作者，不复制爆款。方向包含平台、读者、原创核心、作者表达、目标、参考差异与风险；缺事实才询问，书名与计划可以先建议。',
        '<button class="btn" data-action="nav.view" data-area="market" data-view="references">参考与拆解</button>',
        from ? '<span class="chip soft">已带入 ' + WB.esc(from) + ' 的来源、日期与范围</span>' : '') +

        ui.panel({ title: '两个方向的比较', plain: true, body:
          ui.tbl(['维度', 'D-01 卷三方向', 'D-02 新书方向'], [
            { cells: ['平台 / 读者', '番茄 · 都市奇谈读者', '起点 · 民国悬疑读者'] },
            { cells: ['结构主张', '每单元独立成立，同时推进长线', '双线交替，每卷收束一条线'] },
            { cells: ['与参考关系', '取自 R-01 的对峙前置；不复制设定', '取自 R-02 的双线结构；节奏取向相反'] },
            { cells: ['作者表达', '保持克制、不解释', '保留对年代细节的把握'] },
            { cells: ['主要风险', '单元同质化', '与既有作品题材接近、产能分散'] },
            { cells: ['状态', '已接受并应用（09-18）', '待作者决定'] }
          ]) }) +

        card(d1) + card(d2) +

        ui.panel({ title: '方向 → 作品 的交接内容', body:
          '<div class="sm">接受方向后进入作品时，必须携带：作者确认的定位版本、目标读者、平台、原创差异、参考来源与范围、明确未知。</div>' +
          ui.note('bound', '已有书改变方向时，先显示后续 Outline、人物弧光与连载承诺的影响，不能静默改历史章。') });
    },
    aside: function () {
      var u = WB.S.learningUsage.slice(0, 2);
      return WB.asBlock('可用经验（限定范围）', u.map(function (x) {
        var l = WB.learning(x.learningId);
        return '<div class="as-w clickable" data-action="nav.view" data-area="learning" data-view="detail">' +
          '<div class="wt">' + WB.esc(l.text) + '</div><div class="ws">范围：' + WB.esc(l.scope) +
          '<br>反例：' + WB.esc(l.counter) + '</div></div>';
      }).join('')) +
        WB.asBlock('责任', WB.ownerHtml('E-01') + ' + ' + WB.ownerHtml('E-02')) +
        WB.asBlock('不会发生', '<div class="sm t2">· 参考不会写成本书 Canon<br>· 方向不会静默覆盖历史章节<br>· 不会用实时热度自动生成趋势</div>');
    }
  });

  WB.on['dir.edit'] = function (el, d) {
    var dir = WB.byId(WB.S.directions, d.id);
    dir[d.id === 'D-02' ? 'core' : 'core'] = el.value;
    WB.save();
    WB.toast('已保存你的修改（真实写入本机演示状态）', 'ok');
  };
})();
