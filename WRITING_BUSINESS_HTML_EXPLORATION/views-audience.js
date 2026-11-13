/* ============================================================================
   views-audience.js — 读者与收益（表现总览 / 数据补录 / 评论洞察 / 内容归因 / 收益明细）
   底线：数据关联实际发布版本与时间窗；不同平台指标不硬合并；Unknown 不填 0；
        不编造章节/段落收益；归因分 Observation/Evidence/Hypothesis/Learning/Recommendation。
   ========================================================================== */
(function () {
  var ui = WB.ui;

  /* ---------------- 极简折线图（内联 SVG，无外部依赖） ---------------- */
  function lineChart(cfg) {
    var w = 660, h = 176, pl = 46, pr = 14, pt = 16, pb = 28;
    var all = [];
    cfg.series.forEach(function (s) { all = all.concat(s.data); });
    var min = Math.min.apply(null, all), max = Math.max.apply(null, all);
    if (max === min) { max = min + 1; }
    var pad = (max - min) * 0.18; min = min - pad; max = max + pad;
    function X(i) { return pl + (w - pl - pr) * (cfg.labels.length <= 1 ? 0 : i / (cfg.labels.length - 1)); }
    function Y(v) { return pt + (h - pt - pb) * (1 - (v - min) / (max - min)); }
    var grid = '';
    for (var g = 0; g <= 3; g++) {
      var yv = min + (max - min) * g / 3;
      var y = Y(yv);
      grid += '<line x1="' + pl + '" y1="' + y.toFixed(1) + '" x2="' + (w - pr) + '" y2="' + y.toFixed(1) + '" stroke="#E4E3DC" stroke-width="1"/>' +
        '<text x="' + (pl - 6) + '" y="' + (y + 3.5).toFixed(1) + '" text-anchor="end" font-size="9.5" fill="#8B929F">' +
        (Math.abs(max) > 1000 ? Math.round(yv / 100) / 10 + 'k' : Math.round(yv)) + '</text>';
    }
    var paths = cfg.series.map(function (s) {
      var pts = s.data.map(function (v, i) { return X(i).toFixed(1) + ',' + Y(v).toFixed(1); }).join(' ');
      var dots = s.data.map(function (v, i) {
        return '<circle cx="' + X(i).toFixed(1) + '" cy="' + Y(v).toFixed(1) + '" r="2.6" fill="' + s.color + '"/>';
      }).join('');
      return '<polyline points="' + pts + '" fill="none" stroke="' + s.color + '" stroke-width="2" stroke-linejoin="round"/>' + dots;
    }).join('');
    /* 时间轴标签：兼容 "2026-09-15" 与 "09-15" 两种写法，只去掉年份前缀 */
    var xl = cfg.labels.map(function (l, i) {
      var lab = String(l).replace(/^\d{4}-/, '');
      return (i % (cfg.step || 1) === 0 || i === cfg.labels.length - 1)
        ? '<text x="' + X(i).toFixed(1) + '" y="' + (h - 8) + '" text-anchor="middle" font-size="9.5" fill="#8B929F">' + WB.esc(lab) + '</text>' : '';
    }).join('');
    var legend = '<div class="legend">' + cfg.series.map(function (s) {
      return '<span><i style="background:' + s.color + '"></i>' + WB.esc(s.name) + (s.unit ? '（' + WB.esc(s.unit) + '）' : '') + '</span>';
    }).join('') + '</div>';
    return '<div class="chart"><svg viewBox="0 0 ' + w + ' ' + h + '" role="img" aria-label="' + WB.esc(cfg.title || '趋势') + '">' +
      grid + paths + xl + '</svg></div>' + legend;
  }

  WB.lineChart=lineChart;
  /* ---------------- 行动 ---------------- */
  WB.on['aud.metric'] = function (el, d) {
    WB.S.__sel.metric = d.key;
    WB.save(); WB.render();
  };
  WB.on['aud.age'] = function (el, d) {
    WB.S.__sel.age = d.key; WB.save(); WB.render();
    WB.toast(d.key === 'age7d' ? '已切换到「发布后 7 日」观察年龄' : '已切换到「固定日期」趋势');
  };
  WB.on['aud.point'] = function (el, d) {
    var a = WB.S.analyses.filter(function (x) { return x.bookId === WB.S.__scope.bookId && x.chapter === (d.id || 'ch43'); })[0];
    if (!a) { WB.toast('该章节尚无归因分析；保留数据缺口', 'warn'); return; }
    WB.go('audience', 'attribution', { id: a.id });
    WB.toast('已定位到' + a.chapter + '的归因详情（保留原筛选）');
  };
  WB.on['aud.publishedText'] = function (el, d) {
    var a = WB.analysis(d.id), ms = a && a.chapter && WB.S.manuscripts[a.chapter];
    var snap = ms && ms.published && ms.published.version === a.publishedVersion ? ms.published : null;
    WB.openDrawer({ title: '分析对应的线上正文 · ' + d.id, sub: a.chapter + ' · ' + (a.publishedVersion || '版本未知'), wide: true,
      body: snap && snap.paragraphs && snap.paragraphs.length
        ? '<div class="sm t3">线上快照：' + WB.esc(snap.at || a.publishedAt) + '；只读，不以当前草稿替代。</div>' + snap.paragraphs.map(function (p, i) { return '<p class="sm"><span class="t3">' + (i + 1) + '.</span> ' + WB.esc(p) + '</p>'; }).join('')
        : ui.note('bound', '本机没有与分析版本一致的线上正文快照。保留章节与版本关系，不借当前草稿补造原文。'),
      footer: '<button class="btn" data-action="close-drawer">返回归因</button>' });
  };
  WB.on['aud.commentEvidence'] = function (el, d) {
    var a = WB.analysis(d.id);
    WB.openDrawer({ title: '读者原话与反例 · ' + d.id, sub: a.window + ' · 演示评论样本', wide: true,
      body: (a.linkedComments || []).map(function (id) {
        var c = WB.byId(WB.S.comments.clusters, id);
        return c ? ui.kv([['反馈簇', WB.esc(c.topic + ' · ' + c.coverage)], ['代表原话', WB.esc(c.quote)], ['相反意见', WB.esc(c.counter)],
          ['章节 / 段落', WB.esc(c.anchor.chapter + (c.anchor.from ? ' · ' + c.anchor.from + '–' + c.anchor.to + ' 段' : ' · 未定位段落'))],
          ['定位可信度', c.anchor.conf === 'confirmed' ? '已核对' : 'AI 推断，待确认']]) : '';
      }).join('') + ui.note('bound', '评论锚点和读者意图不能由聚类自动确认为因果证据。'),
      footer: '<button class="btn" data-action="close-drawer">返回归因</button>' });
  };
  WB.on['aud.entrySave'] = function () {
    var S = WB.S;
    var plat = document.getElementById('enPlat').value;
    var field = document.getElementById('enField').value;
    var val = document.getElementById('enVal').value;
    var at = document.getElementById('enAt').value || WB.now();
    if (!val) { WB.toast('请填写数值；平台没有的字段不要强填', 'warn'); return; }
    S.dataEntries.unshift({ id: 'DE-' + (100 + S.dataEntries.length), kind: 'manual', platform: plat, at: WB.now(),
      field: field, value: val, when: at, note: '手录：只填平台真实可得的数据', status: 'done' });
    WB.save(); WB.render();
    WB.toast('已保存手录观测（含平台、字段、时点、来源），进入正式对比', 'ok');
  };
  WB.on['aud.entryCorrect'] = function (el, d) {
    var S = WB.S, e = WB.byId(S.dataEntries, d.id);
    WB.modal({ title: '订正观测',
      body: ui.kv([['字段', WB.esc(e.field)], ['原值', String(e.before)], ['订正值', WB.esc(String(e.after))], ['来源', WB.esc(e.reason)]]) +
        ui.note('bound', '订正保留原记录与订正来源；累计快照修订会使差值异常，需要在图上标注。'),
      footer: '<button class="btn" data-action="close-modal">关闭</button>' +
        '<button class="btn primary" data-action="act.e" data-fn="entryCorrect" data-a1="' + e.id + '">确认订正生效</button>' });
  };

  /* ---------------- 表现总览与对比 ---------------- */
  WB.register('audience.performance', {
    render: function () {
      var S = WB.S, b = WB.scopeBook(), pf = S.performance[b.id];
      var metric = S.__sel.metric || pf.bookLevel[0].key;
      var m = pf.bookLevel.filter(function (x) { return x.key === metric; })[0] || pf.bookLevel[0];
      var age = S.__sel.age || 'fixed';
      var other = pf.bookLevel.filter(function (x) { return x.key !== m.key; }).slice(0, 2);

      var chart = lineChart({
        title: m.key + ' 趋势', labels: m.ages, step: 1,
        series: [{ name: b.platform + ' · ' + m.key, data: m.series, color: b.id === 'B-01' ? '#6E9438' : '#B87922', unit: m.unit }]
      });

      var metricChips = ui.chips(pf.bookLevel.map(function (x) { return [x.key, x.key]; }), m.key, 'aud.metric');

      var chRows = pf.chapterLevel.map(function (c) {
        return { attrs: c.chapter === 'ch43' ? ' class="clickable" data-action="aud.point" data-id="ch43"' : '',
          cells: ['<b>' + WB.esc(c.chapter) + '</b>', WB.esc(c.key),
            c.value == null ? WB.unknown('无此字段') : '<span class="mono">' + c.value + WB.esc(c.unit) + '</span>',
            c.denom === 'unknown' ? WB.unknown('无分母 / 无样本') : '—',
            '<span class="sm t2">' + WB.esc(c.note) + '</span>'] };
      });

      return ui.hdr('表现总览与对比 · ' + WB.esc(b.title),
        '明确日期、观察年龄、数据覆盖与更新时间；从数字回到具体内容，而不是只看 KPI。',
        '<button class="btn" data-action="nav.view" data-area="audience" data-view="entry">数据补录</button>' +
        '<button class="btn" data-action="nav.view" data-area="audience" data-view="attribution">内容归因</button>',
        '<span>数据覆盖：' + WB.esc(pf.coverage) + '</span><span class="t4">|</span><span>更新 ' + WB.esc(pf.updatedAt) + '</span>' +
        '<span class="t4">|</span><span>' + WB.esc(pf.source) + '</span>') +

        '<div class="scopebar"><div class="sb-row">' +
        '<span class="sl-lb">指标</span>' + metricChips +
        '<span class="sl-lb" style="margin-left:12px">观察年龄</span>' +
        ui.chips([['fixed', '固定日期趋势'], ['age7d', '发布后 7 日'], ['age24h', '发布后 24 小时']], age, 'aud.age') +
        '<span class="sb-me">平台 <b>' + WB.esc(pf.platform) + '</b> · ' + WB.esc(pf.model) + '</span>' +
        '</div></div>' +

        '<div class="grid" style="grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:12px;align-items:start">' +
        '<div>' +
        (b.id === 'B-01' ? ui.panel({ title: '需要解释的变化 · 第 43 章',
          body: '<div class="sm">发布后 7 日，本书新增收藏 245；同观察年龄的前三章分别为 198 / 205 / 212。第 43 章读完率显示 71%，分母未知。</div>' +
            '<div class="sm t3">关联线上稿 v2 · 评论样本 K-01 · 仍可能受推荐曝光和时段影响。</div>',
          footer: '<button class="btn sm primary" data-action="aud.point">打开第 43 章内容归因</button>' }) : '') +
        ui.panel({ title: m.key + ' 趋势', sub: m.unit + ' · ' + WB.esc(m.note),
          body: chart +
            '<div class="chart-foot">口径：' + WB.esc(pf.platform) + ' 后台读数；区间与累计不混用。点击下方章级表可跳到归因。</div>',
          footer: '<button class="btn sm" data-action="aud.point">定位最近异常点 → 归因</button>' +
            '<span class="sm t3">不与其他平台合并显示</span>' }) +

        ui.panel({ title: '章级数据（含缺口）', sub: '缺粒度就显示缺口，不下钻伪造', tight: true,
          body: ui.tbl(['章', '指标', '值', '分母 / 样本', '说明'], chRows),
          footer: '<span>率只在分子分母可加且口径兼容时加权；不平均章节百分比。</span>' }) +
        '</div>' +

        '<div>' +
        ui.panel({ title: '其他指标', body: other.map(function (o) {
          var last = o.series[o.series.length - 1], first = o.series[0];
          return '<div style="margin-bottom:10px"><div class="sm strong">' + WB.esc(o.key) + '</div>' +
            '<div class="figs" style="gap:12px"><div class="fig"><span class="n sm">' + last + '</span><span class="l">最新值（' + WB.esc(o.unit) + '）</span></div>' +
            '<div class="fig"><span class="n sm">' + (last - first >= 0 ? '+' : '') + (last - first) + '</span><span class="l">7 日变化</span></div></div>' +
            '<div class="sm t3">' + WB.esc(o.note) + '</div></div>';
        }).join('') }) +

        ui.panel({ title: '观察窗对比', body:
          (function () {
            var w = S.observationsWindow.filter(function (x) { return x.chapter === 'ch43'; })[0];
            return ui.kv([['章节', WB.esc(w.chapter)], ['上线', WB.esc(w.publishedAt)],
              ['发布后 24h', '在读 ' + w.age24h['在读'] + ' · 新增收藏 ' + w.age24h['新增收藏']],
              ['发布后 7d', '在读 ' + w.age7d['在读'] + ' · 新增收藏 ' + w.age7d['新增收藏']]]) +
              ui.note('bound', '固定日期趋势与「发布后观察年龄」分开记录；跨章比较只在观察年龄一致时进行。');
          })() }) +

        ui.panel({ title: '不合并平台', body:
          '<div class="sm t2">《夜行灯》为免费阅读（广告与礼物），《白鹭洲纪事》为付费订阅。' +
          '两者的指标口径、单位与分母都不同 → <b>分平台显示，不做换算与合并</b>。</div>' +
          '<div class="btnrow" style="margin-top:8px"><button class="btn sm" data-action="act.bk" data-fn="bookScope" data-a1="B-02">切换查看《白鹭洲纪事》</button></div>' }) +
        '</div></div>';
    },
    aside: function () {
      var S = WB.S, b = WB.scopeBook(), pf = S.performance[b.id];
      var metric = S.__sel.metric || pf.bookLevel[0].key;
      var m = pf.bookLevel.filter(function (x) { return x.key === metric; })[0] || pf.bookLevel[0];
      /* 右栏只放「为完成当前工作还需看/改什么」：来源、口径、订正历史、单条补录。
         趋势 / 时间窗 / 指标切换 / 比较 / 明细仍在 Main，不退回概览卡墙。 */
      var corr = (S.dataEntries || []).filter(function (e) {
        return e.bookId === b.id || e.book === b.id || e.target === b.id;
      }).slice(0, 3);
      return WB.asBlock('数据来源与口径',
          '<div class="sm t2">· 来源：' + WB.esc(pf.source || '—') + '<br>' +
          '· 平台：' + WB.esc(pf.platform || '—') + ' · 口径模型：' + WB.esc(pf.model || '—') + '<br>' +
          '· 覆盖：' + WB.esc(pf.coverage || '—') + '<br>' +
          '· 更新：' + WB.esc(pf.updatedAt || '—') + '<br>' +
          '· 当前指标：<b>' + WB.esc(m.key) + '</b>（' + WB.esc(m.unit) + '）</div>' +
          '<div class="btnrow" style="margin-top:6px"><button class="btn sm" data-action="nav.view" data-area="audience" data-view="entry">单条补录</button></div>') +
        WB.asBlock('订正历史（' + corr.length + '）',
          corr.length ? corr.map(function (e) {
            return '<div class="as-w"><div class="wt">' + WB.esc(e.at || e.id || '') + ' · ' + WB.esc(e.kind || '') + '</div>' +
              '<div class="ws">' + WB.esc(e.field || '') + (e.before != null ? '：' + e.before + ' → ' + e.after : '') + '</div>' +
              '<div class="ws">' + WB.esc(e.reason || e.conflictNote || e.note || '') + '</div></div>';
          }).join('') + '<div class="sm t3" style="margin-top:4px">订正不改写历史读数；口径变化单独标注。</div>'
            : '<div class="sm t3">本书暂无订正记录。平台字段缺失时保留 Unknown，不填 0。</div>') +
        WB.asBlock('数据缺口', '<div class="sm t2">· 番茄：章节收益无字段<br>· 起点：章级订阅无明细<br>· 两平台：推荐曝光不可得<br>· Unknown 不换算、不合并</div>') +
        WB.asBlock('责任人', WB.ownerHtml('E-04') + '<div class="sm t3" style="margin-top:6px">分析责任：结论必须回原数据与对应正文。</div>') +
        WB.asBlock('相关 Work', S.works.filter(function (w) { return w.area === 'audience'; }).slice(0, 3).map(function (w) { return WB.workHtml(w); }).join(''));
    }
  });

  /* ---------------- 数据补录与订正 ---------------- */
  WB.register('audience.entry', {
    render: function () {
      var S = WB.S, imp = S.dataEntries.filter(function (d) { return d.kind === 'import'; })[0];
      return ui.hdr('数据补录与订正',
        '没有 API 也能反馈：导入预览列映射、手录真实可得的字段、订正保留原记录。未确认的数据不进入正式对比。',
        '<button class="btn" data-action="nav.view" data-area="audience" data-view="performance">回表现总览</button>',
        '<span>平台只写真实可得字段</span><span class="t4">|</span><span>Unknown 合法</span>') +

        (imp ? ui.panel({ title: '导入预览 · ' + WB.esc(imp.platform), sub: '待确认 · ' + imp.rows + ' 行',
          body: '<div class="grid g2"><div>' +
            ui.tbl(['原始列', '映射到'], imp.fields.map(function (f) { return { cells: [WB.esc(f[0]), '<span class="pill mono">' + WB.esc(f[1]) + '</span>'] }; })) +
            '</div><div>' + ui.kv([['行数', imp.rows + ' 行'], ['已映射', imp.mapped + ' 行'], ['冲突', imp.conflicts + ' 行'],
              ['导入时间', WB.esc(imp.at)]]) +
            '<div class="note choice" style="margin-top:8px">' + WB.esc(imp.conflictNote) + '</div>' +
            '<div class="btnrow" style="margin-top:8px">' +
            '<button class="btn primary" data-action="act.e" data-fn="entryResolve" data-a1="' + imp.id + '">确认映射并采纳</button>' +
            '<button class="btn" data-action="nav.view" data-area="audience" data-view="entry">保持待确认</button></div>' +
            '<div class="sm t3" style="margin-top:6px">未确认的行不进入正式图表。</div>' +
            '</div></div>' }) : '') +

        '<div class="grid g2">' +
        ui.panel({ title: '手动录入（真实写入演示状态）', body:
          '<div class="grid g2">' +
          '<div class="fld"><label>平台</label><select class="sel" id="enPlat"><option>番茄</option><option>起点 / 阅文</option></select></div>' +
          '<div class="fld"><label>字段</label><select class="sel" id="enField"><option>在读</option><option>新增收藏</option><option>广告收益（预估）</option><option>订阅</option><option>打赏</option></select></div>' +
          '<div class="fld"><label>数值</label><input class="inp" id="enVal" placeholder="只填平台真实可得的数值" /></div>' +
          '<div class="fld"><label>时点</label><input class="inp" id="enAt" value="' + WB.esc(S.meta.today) + '" /></div>' +
          '</div>' +
          '<div class="btnrow" style="margin-top:10px"><button class="btn primary" data-action="aud.entrySave">保存观测</button>' +
          '<span class="sm t3">没有的字段留空 → 记 Unknown，不填 0</span></div>' }) +
        ui.panel({ title: '录入规则', body:
          '<div class="sm t2">每条观测至少保存：平台/站点/账号、Book 与可得 Chapter、原指标名/定义/单位、累计或区间、时间窗/时区、采集时点、值或缺口原因、来源、原记录与订正。</div>' +
          ui.note('bound', '截图/OCR 必须确认数字与对象；导入先预览列映射、重复与时间冲突。') }) +
        '</div>' +

        ui.panel({ title: '录入与订正记录', tight: true, body: ui.tbl(['类型', '平台', '字段 / 内容', '值', '时点', '说明', '状态'],
          S.dataEntries.map(function (e) {
            var kind = { import: ['导入', 'wait'], correction: ['订正', 'choice'], manual: ['手录', 'published'] }[e.kind];
            return { cells: [
              WB.stBadge(kind[0], kind[1]), WB.esc(e.platform),
              e.kind === 'correction' ? '<b>' + WB.esc(e.field) + '</b>' : (e.kind === 'import' ? e.rows + ' 行待映射' : WB.esc(e.field)),
              e.kind === 'correction' ? '<span class="mono">' + e.before + '</span> → <span class="mono">' + e.after + '</span>' : (e.value != null ? '<span class="mono">' + WB.esc(String(e.value)) + '</span>' : '—'),
              WB.esc(e.at), '<span class="sm t2">' + WB.esc(e.reason || e.note || e.conflictNote || '') + '</span>',
              e.status === 'pending' ? WB.stBadge('待确认', 'choice') : WB.stBadge('已生效', 'published')
            ] };
          })) ,
          footer: '<span>订正保留原值；累计快照修订会让差值异常，需标注来源。</span>' });
    },
    aside: function () {
      return WB.asBlock('责任人', WB.ownerHtml('E-04') + WB.ownerHtml(null, { gapText: '财务责任人：缺' })) +
        WB.asBlock('待办缺口', '<div class="sm t2">· 起点导出 1 行时间窗冲突待确认<br>· 8 月账期差异待核对（缺财务责任人）</div>') +
        WB.asBlock('四模式', '<div class="sm t2">API_SYNC / COMPUTER_USE / IMPORT / MANUAL_ENTRY 均保来源。本原型的导入与手录为本地 Mock。</div>');
    }
  });

  /* ---------------- 评论洞察 ---------------- */
  WB.register('audience.comments', {
    render: function () {
      var S = WB.S;
      return ui.hdr('评论洞察',
        '听懂人物、剧情与节奏反馈：按主题聚类，展示样本量、代表原文、反例与定位置信；读者猜测不是 Canon。',
        '<button class="btn" data-action="nav.view" data-area="audience" data-view="attribution">去内容归因</button>',
        '<span>样本：' + WB.esc(S.comments.sample) + '</span>') +

        ui.panel({ title: '反馈簇', sub: S.comments.clusters.length + ' 簇', body:
          S.comments.clusters.filter(function(c){var ch=WB.S.chapters[c.anchor.chapter];return ch&&ch.bookId===WB.S.__scope.bookId;}).map(function (c) {
            return '<div class="cl"><div class="cl-h">' + WB.esc(c.topic) +
              WB.stBadge('样本 ' + c.size + ' / ' + c.coverage, 'wait') +
              (c.anchor.conf === 'confirmed' ? WB.stBadge('定位已确认', 'published') : WB.stBadge('定位为推断', 'unknown')) + '</div>' +
              '<div class="cl-q">' + WB.esc(c.quote) + '<div class="who">— 平台评论（作者本人在平台可见）</div></div>' +
              '<div class="sm t2">反例：' + WB.esc(c.counter) + '</div>' +
              '<div class="sm t3">定位：' + WB.esc(c.anchor.chapter) + (c.anchor.from ? ' 第 ' + c.anchor.from + '–' + c.anchor.to + ' 段' : '') +
              (c.anchor.note ? ' · ' + WB.esc(c.anchor.note) : '') + '</div>' +
              '<div class="btnrow" style="margin-top:8px">' +
              '<button class="btn sm" data-action="book.anchor" data-id="' + c.id + '">展开证据</button>' +
              '<button class="btn sm" data-action="nav.view" data-area="book" data-view="manuscript">在正文中查看</button>' +
              '<button class="btn sm" data-action="act.k" data-fn="confirmAnchor" data-a1="' + c.id + '">确认定位</button>' +
              '<button class="btn sm primary" data-action="act.k" data-fn="commentToEditor" data-a1="' + c.id + '">交给编辑</button>' +
              '</div></div>';
          }).join(''),
          footer: '<span>' + WB.esc(S.comments.actions.replyNote) + '</span>' }) +

        ui.panel({ title: '采样与偏差说明', body:
          '<div class="grid g2"><div class="sm t2">· 不同平台、作者删评/审核、热评偏置不能当全体读者意见<br>' +
          '· 点赞不是独立读者票数，情绪不能替代主题理解<br>· 聚类需给样本量与反例</div>' +
          '<div class="sm t2">· AI 提议的 Scene/Character 关联需用户或编辑确认<br>· 无直接锚点时标「推断」<br>· 旧版段落无法匹配时保旧版引用</div></div>' }) +

        ui.panel({ title: '平台质量类反馈（AI 味 / 声纹趋同 / 剧情机械）', body:
          '<div class="sm t2">处理路径：保存原反馈 → 定位实际正文版本 → 与作者自有 Accepted Manuscript 及可比高表现章节对照 → 找具体重复、措辞与冲突机械证据 → 局部修改候选 → 作者 Review → 正式保存 → 必要时另发修订 → 观察与负向 Learning。</div>' +
          ui.note('bound', '<b>本产品不提供</b>降 AI 率、绕检测、规避声明按钮或伪造人类创作记录。平台检测结论只是该平台反馈，不作为作者行为或质量的确定证明。') });
    },
    aside: function () {
      return WB.asBlock('责任人', WB.ownerHtml('E-04') + ' / ' + WB.ownerHtml('E-01')) +
        WB.asBlock('关联对象', '<div class="sm t2">评论锚点挂在已发布版本上；改版后旧评论仍留在旧版锚点，不移动到新句。</div>') +
        WB.asBlock('相关 Work', WB.S.works.filter(function (w) { return w.area === 'audience' && w.obj && String(w.obj).indexOf('K-') === 0; }).map(function (w) { return WB.workHtml(w); }).join('') || '<div class="sm t3">尚无由评论产生的 Work。</div>');
    }
  });

  /* ---------------- 内容归因详情 ---------------- */
  WB.register('audience.attribution', {
    render: function (ctx) {
      var S = WB.S;
      var id = ctx.params.id || 'A-01';
      var a = WB.analysis(id) || S.analyses[0];
      var ch = a.chapter ? WB.chapter(a.chapter) : null;
      var ms = a.chapter ? S.manuscripts[a.chapter] : null;

      var layers = [
        ['1 观察 Observation', a.layers.observation, 'l1'],
        ['2 证据 Evidence', '<ul>' + a.layers.evidence.map(function (e) { return '<li>' + WB.esc(e) + '</li>'; }).join('') + '</ul>' +
          (a.evidenceGap ? '<div class="sm t3" style="margin-top:6px">证据缺口：' + WB.esc(a.evidenceGap) + '</div>' : '') +
          '<div class="btnrow" style="margin-top:8px"><button class="btn sm" data-action="aud.evidence" data-id="' + WB.esc(a.id) + '">查看完整证据（不离开当前上下文）</button></div>', 'l2'],
        ['3 假设 Hypothesis', WB.esc(a.layers.hypothesis) +
          '<div class="sm t2" style="margin-top:6px">替代解释：</div><ul>' + a.layers.alternatives.map(function (x) { return '<li>' + WB.esc(x) + '</li>'; }).join('') + '</ul>' +
          '<div class="note danger" style="margin-top:8px"><b>反证：</b>' + WB.esc(a.layers.counter) + '</div>', 'l3'],
        ['4 经验候选 Learning', a.layers.learningDraft
          ? '<div class="sm"><b>' + WB.esc(a.layers.learningDraft.text) + '</b></div>' +
            '<div class="sm t2">范围：' + WB.esc(a.layers.learningDraft.scope) + '</div>' +
            '<div class="sm t2">尚未排除：' + WB.esc(a.layers.learningDraft.exclude) + '</div>'
          : '<div class="sm t2">本条只有书级数据 → 不生成章节经验。</div>', 'l4'],
        ['5 建议 Recommendation', WB.esc(a.layers.recommendation) + '<div class="sm t3">决定人：' + WB.esc(a.layers.owner) + '</div>', 'l5']
      ];

      return ui.hdr('内容归因详情 · ' + WB.esc(a.id),
        '不止报告数字，也不假装因果。每条分析必须能回到原数据、对应正文与当时线上版本。',
        '<button class="btn" data-action="nav.view" data-area="audience" data-view="performance">回趋势</button>',
        '<span>Book ' + WB.esc(a.bookId) + '</span><span class="t4">|</span>' +
        (a.chapter ? '<span>章节 ' + WB.esc(a.chapter) + ' · 线上版本 <span class="vtag pub">' + WB.esc(a.publishedVersion || '—') + '</span></span>'
          : '<span>' + WB.stBadge('仅书级数据', 'unknown') + '</span>') +
        '<span class="t4">|</span><span>窗口 ' + WB.esc(a.window) + '</span>') +

        '<div class="scopebar"><div class="sb-row"><span class="sl-lb">选择分析</span>' +
        ui.chips(S.analyses.map(function (x) { return [x.id, x.chapter ? x.id + '（ch43）' : x.id + '（书级）']; }), a.id, 'aud.analysisPick') +
        '<span class="sb-me">分析人 <b>何茵</b> · ' + WB.esc(a.createdAt) + '</span></div></div>' +

        '<div class="grid" style="grid-template-columns:minmax(0,1.45fr) minmax(0,1fr);gap:12px;align-items:start">' +
        '<div>' +
        layers.map(function (l) {
          return '<div class="lay ' + l[2] + '"><div class="lay-h"><span class="lay-n">' + l[0].slice(0, 1) + '</span>' + WB.esc(l[0].slice(2)) + '</div>' +
            (typeof l[1] === 'string' ? l[1] : '') + '</div>';
        }).join('') +
        ui.note('choice', '<b>表述边界：</b>' + WB.esc(a.limitation)) +
        '</div>' +

        '<div>' +
        ui.panel({ title: '关联事实', body: ui.kv([
          ['对应正文', a.chapter && ms ? '第 ' + ch.no + ' 章 · ' + WB.esc(ch.title) : '—（仅书级）'],
          ['正文版本', a.publishedVersion ? '<span class="vtag pub">线上 ' + WB.esc(a.publishedVersion) + '</span>' : WB.unknown('无')],
          ['发布日期', WB.esc(a.publishedAt || '—')],
          ['对照章节', a.linkedRefs.map(function (r) { var x = WB.byId(S.references, r); return WB.esc(x ? x.title : r); }).join('、')],
          ['关联评论', a.linkedComments.join('、') || '—'],
          ['经验', a.learningId && WB.learning(a.learningId) ? WB.esc(a.learningId) + '（' + WB.esc(WB.learning(a.learningId).text) + '）' : WB.unknown('尚未生成')]
        ]) + (a.chapter ? '<div class="btnrow"><button class="btn sm" data-action="aud.publishedText" data-id="' + a.id + '">查看当时线上正文</button>' +
          '<button class="btn sm" data-action="aud.commentEvidence" data-id="' + a.id + '">查看评论原话与反例</button></div>' : '') }) +
        ui.panel({ title: '下一步', body:
          '<div class="btnrow" style="flex-direction:column;align-items:stretch">' +
          '<button class="btn" data-action="act.a" data-fn="analysisToObservation" data-a1="' + a.id + '">建立后续观察计划（ch45）</button>' +
          (a.layers.learningDraft ? '<button class="btn primary" data-action="act.a" data-fn="analysisToLearning" data-a1="' + a.id + '">生成经验候选（限定范围）</button>' : '') +
          '<button class="btn" data-action="act.a" data-fn="analysisToLeader" data-a1="' + a.id + '">送 Leader 作为经营决定依据</button>' +
          '<button class="btn" data-action="nav.view" data-area="book" data-view="manuscript">回到正文（保留版本）</button>' +
          '</div>',
          footer: '<span>不因单次数据自动改稿或调频；建议需作者判断。</span>' }) +
        ui.panel({ title: '能证明 / 不能证明', body:
          '<div class="sm t2"><b>能：</b>该窗口内本书指标变化、评论样本指向、正文版本与发布时间对应关系。<br>' +
          '<b>不能：</b>不能证明该段对白导致收入增长；不能排除推荐曝光与时段；读者看过哪个版本未知时不能当随机实验。</div>' }) +
        '</div></div>';
    },
    aside: function () {
      var S = WB.S;
      return WB.asBlock('责任人', WB.ownerHtml('E-04') + ' / ' + WB.ownerHtml('E-01')) +
        WB.asBlock('可返回的原始位置', '<div class="sm t2">· 表现总览（保留原筛选与指标）<br>· 发布项 Q-04（线上 v2）<br>· 评论簇 K-01<br>· 经验库</div>') +
        WB.asBlock('分析纪律', '<div class="sm t2">已发章等反馈期间，后续章节可继续创作；研究与他书可并行。缺章级数据时只保留书级观察。</div>');
    }
  });
  WB.on['aud.analysisPick'] = function (el, d) { WB.go('audience', 'attribution', { id: d.key }, { replace: true }); };

  /* 完整证据审阅：以抽屉最大化使用，不丢失原筛选 / 选区 / 版本（Utility 路径） */
  WB.on['aud.evidence'] = function (el, d) {
    var a = WB.analysis(d.id) || WB.S.analyses[0];
    var ev = (a.layers.evidence || []).map(function (e) { return '<li>' + WB.esc(e) + '</li>'; }).join('');
    WB.act.openEvidence('完整证据 · ' + a.id,
      '<div class="sm t2">来源均为平台已展示的读数或已落盘的本地事实；不引入外部抓取。</div>' +
      '<ul style="padding-left:18px;line-height:1.8;margin-top:8px">' + ev + '</ul>' +
      '<div class="note danger" style="margin-top:10px"><b>证据缺口：</b>' + WB.esc(a.evidenceGap || '—') + '</div>' +
      '<div class="note bound" style="margin-top:8px"><b>表述边界：</b>' + WB.esc(a.limitation || '—') + '</div>' +
      '<div class="sm t3" style="margin-top:8px">样本：' + WB.esc(a.window || '—') + '；收集人：' + WB.ownerHtml(a.by) + '</div>', true);
  };

  /* ---------------- 收益明细 ---------------- */
  WB.register('audience.revenue', {
    render: function () {
      var S = WB.S;
      function blk(bid) {
        var b = WB.book(bid), r = S.revenue[bid];
        return ui.panel({ title: b.title + ' · ' + WB.esc(r.platform), sub: WB.esc(b.model) + ' · 币种 ' + WB.esc(r.currency) + ' · 更新 ' + WB.esc(r.updatedAt),
          tight: true, body: ui.tbl(['收入类别', '阶段', '窗口', '金额', '说明'],
            r.items.map(function (i) {
              return { cells: ['<b>' + WB.esc(i.kind) + '</b>',
                i.stage === '预估' ? WB.stBadge(i.stage, 'wait') : i.stage === '结算中' ? WB.stBadge(i.stage, 'choice') : i.stage === '已到账' ? WB.stBadge(i.stage, 'published') : i.stage === '已结算' ? WB.stBadge(i.stage, 'published') : WB.unknown('无字段'),
                WB.esc(i.window),
                i.amount == null ? WB.unknown('未提供') : '<span class="mono">' + WB.money(i.amount) + '</span>',
                '<span class="sm t2">' + WB.esc(i.note) + '</span>'] };
            })),
          footer: '<span>' + (bid === 'B-01' ? '预估 / 已结算 / 已到账 分开；不摊造章节收益。' : '账期：次月 15 日；与订阅合并出账。') + '</span>' });
      }
      return ui.hdr('收益明细',
        '收益和流量分开判断：按平台、账期、收入类别，区分预估 / 结算 / 到账，并保留来源。',
        '<button class="btn" data-action="nav.view" data-area="audience" data-view="performance">回表现总览</button>',
        '<span>币种 CNY</span><span class="t4">|</span><span>提现与税务操作留在平台</span>') +

        '<div class="grid g2">' + blk('B-01') + blk('B-02') + '</div>' +

        ui.panel({ title: '书级总额不能下钻为章节收益', body:
          ui.tbl(['想看的粒度', '平台是否提供', '本原型处理'],
            [['章级收益', '番茄未提供', WB.unknown('显示缺口，不摊分')],
             ['章级订阅', '起点未取得明细', WB.unknown('显示缺口，不推导')],
             ['卷级表现', '两平台均未确认原生报表', '可用同口径章明细聚合并标「Curis 推导」；缺数据不造全卷表现']].map(function (r) {
              return { cells: [r[0], '<span class="sm">' + r[1] + '</span>', r[2]] };
            })) ,
          footer: '<span>不编造章节/段落收益；不同平台不硬合并。</span>' }) +

        ui.panel({ title: '差异与待办', body:
          '<div class="sm t2">8 月账期存在 ¥12.40 差异；本原型<b>缺财务责任人</b> → 只登记待办，不自动对账。</div>' +
          '<div class="btnrow" style="margin-top:8px">' +
          '<button class="btn" data-action="act.rt" data-fn="revenueNote" data-a1="B-01">登记差异待办</button>' +
          '<button class="btn" data-action="nav.view" data-area="audience" data-view="entry">去数据补录</button></div>' +
          ui.note('bound', '提现、税务与账务操作留在平台与作者本人；Curis 只保存核对结果与差异 Work。') });
    },
    aside: function () {
      return WB.asBlock('责任人', WB.ownerHtml(null, { gapText: '财务责任：缺（可指派）' })) +
        WB.asBlock('相关 Work', WB.S.works.filter(function (w) { return w.obj === 'REV-DIFF'; }).map(function (w) { return WB.workHtml(w); }).join('')) +
        WB.asBlock('口径提醒', '<div class="sm t2">平台总额不得摊造章节收益；预估不等于到账。</div>');
    }
  });
})();
