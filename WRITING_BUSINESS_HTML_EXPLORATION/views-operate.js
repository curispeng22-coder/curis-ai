/* ============================================================================
   views-operate.js — 经营（业务首页 / 经营计划与决定详情）
   同时定义全站共用的轻量 UI 件 WB.ui，供其余视图文件复用。
   ========================================================================== */
(function () {

  /* ---------------- 共用 UI 件 ---------------- */
  var ui = {
    hdr: function (title, sub, actions, note) {
      return '<div class="ph"><div class="ph-top"><div><div class="ph-title">' + title + '</div>' +
        (sub ? '<div class="ph-sub">' + sub + '</div>' : '') + '</div>' +
        (actions ? '<div class="ph-actions">' + actions + '</div>' : '') + '</div>' +
        (note ? '<div class="ph-note">' + note + '</div>' : '') + '</div>';
    },
    panel: function (o) {
      return '<section class="pnl' + (o.plain ? ' plain' : '') + '">' +
        (o.title ? '<div class="pnl-h"><div class="pnl-t">' + o.title + (o.sub ? ' <span class="sub">' + o.sub + '</span>' : '') + '</div>' +
          (o.actions ? '<div class="pnl-a">' + o.actions + '</div>' : '') + '</div>' : '') +
        '<div class="pnl-body' + (o.tight ? ' tight' : '') + '">' + o.body + '</div>' +
        (o.footer ? '<div class="pnl-f">' + o.footer + '</div>' : '') + '</section>';
    },
    tbl: function (heads, rows, cls) {
      return '<table class="tbl' + (cls ? ' ' + cls : '') + '"><thead><tr>' +
        heads.map(function (h) { return '<th>' + h + '</th>'; }).join('') + '</tr></thead><tbody>' +
        rows.map(function (r) { return '<tr' + (r.attrs || '') + '>' + r.cells.map(function (c) { return '<td>' + c + '</td>'; }).join('') + '</tr>'; }).join('') +
        '</tbody></table>';
    },
    chips: function (list, current, action, extra) {
      return list.map(function (c) {
        var on = c[0] === current;
        return '<button class="chip' + (on ? ' on' : '') + '" data-action="' + action + '" data-key="' + c[0] + '"' + (extra || '') + '>' + WB.esc(c[1]) + '</button>';
      }).join('');
    },
    kv: function (pairs) {
      return '<div class="stack">' + pairs.map(function (p) {
        return '<div class="inline" style="align-items:flex-start"><span class="t3 sm" style="min-width:74px">' + p[0] + '</span><span class="sm" style="flex:1">' + p[1] + '</span></div>';
      }).join('') + '</div>';
    },
    src: function (s) { return '<div class="src"><span class="k">来源</span><span>' + s + '</span></div>'; },
    note: function (kind, html) { return '<div class="note ' + kind + '">' + html + '</div>'; },
    empty: function (title, body) { return '<div class="empty"><b>' + title + '</b>' + body + '</div>'; },
    worksList: function (list) {
      return '<div class="rows">' + list.map(function (w) {
        var stMap = { done: ['已回原对象', 'published'], working: ['进行中', 'working'], wait: ['等待中', 'wait'], choice: ['待决定', 'choice'], blocked: ['受阻', 'blocked'] };
        var s = stMap[w.status] || ['—', 'wait'];
        return '<div class="row clickable" data-action="work.open" data-id="' + w.id + '">' +
          '<div class="row-main"><div class="row-t">' + WB.esc(w.title) + WB.stBadge(s[0], s[1]) + '</div>' +
          '<div class="row-s">产物：' + WB.esc(w.artifact) + '<br>下一步：' + WB.esc(w.next) + '</div>' +
          '<div class="row-meta">' + WB.ownerHtml(w.owner, { gapText: '缺责任人（可指派）' }) + '<span>·</span><span>' + WB.esc(w.at) + '</span></div></div>' +
          '</div>';
      }).join('') + '</div>';
    }
  };
  WB.ui = ui;

  /* 通用：打开 Work 详情 */
  WB.on['work.open'] = function (el, d) {
    var w = WB.byId(WB.S.works, d.id);
    if (!w) return;
    WB.openDrawer({
      title: w.title, sub: 'Work · ' + w.id + ' · 责任人 ' + (w.owner ? WB.emp(w.owner).name : '缺责任人'),
      body: ui.kv([['状态', (function () { var m = { done: '已回原对象', working: '进行中', wait: '等待中', choice: '待决定' }; return m[w.status] || w.status; })()],
        ['产物', WB.esc(w.artifact)], ['下一步', WB.esc(w.next)], ['出现位置', WB.navName(w.area) + ' · ' + WB.esc(w.obj || '')],
        ['开始', WB.esc(w.at)]]) +
        ui.note('bound', 'Work 的专业内容优先；执行参数与日志不作为默认主体。结果回原对象，不在对话里另存一份。') +
        (w.owner ? '<div class="hr"></div><div class="btnrow"><button class="btn" data-action="conv.open" data-emp="' + w.owner + '" data-obj="' + WB.esc(w.obj || '') + '" data-label="' + WB.esc(w.title) + '">与责任人讨论</button>' +
          '<button class="btn" data-action="work.goto" data-id="' + w.id + '">前往相关工作面</button></div>'
          : '<div class="hr"></div>' + ui.note('choice', '该 Work 缺责任人：可指派，但不会自动发明在岗员工。') +
            '<div class="btnrow"><button class="btn" data-action="act.assign" data-fn="assignOwner" data-a1="' + w.id + '" data-a2="E-01">指派给沈知远</button>' +
            '<button class="btn" data-action="act.assign" data-fn="assignOwner" data-a1="' + w.id + '" data-a2="E-04">指派给何茵</button></div>')
    });
  };
  WB.on['work.goto'] = function (el, d) {
    var w = WB.byId(WB.S.works, d.id);
    if (w.area === 'audience' && String(w.obj).indexOf('A-') === 0) { WB.closeDrawer(); WB.go('audience', 'attribution', { id: w.obj }); return; }
    if (w.area === 'market') { WB.closeDrawer(); WB.go('market', 'watches', {}); return; }
    if (w.area === 'publish') { WB.closeDrawer(); WB.go('publish', 'queue', {}); return; }
    if (w.area === 'book') { WB.closeDrawer(); WB.go('book', 'manuscript', { chapter: 'ch44' }); return; }
    WB.closeDrawer();
  };
  WB.on['conv.open'] = function (el, d) { WB.openConv(d.emp, d.obj, d.label || d.obj); };
  WB.on['act.assign'] = null; // 由 act.assignOwner 处理
  WB.on['conv.send'] = function (el, d) { WB.convSend(d.emp, d.obj); };
  WB.on['conv.work'] = function (el, d) { WB.convWork(d.emp, d.obj); };

  /* ---------------- 经营 · 业务首页 ---------------- */
  WB.register('operate.home', {
    render: function () {
      var S = WB.S, books = WB.allBooks();
      var pending = S.decisions.filter(function (d) { return d.status === 'pending'; });
      var recent = S.works.slice(0, 5);

      var rows = books.map(function (b) {
        var st = WB.stockOf(b.id);
        var stMap = { '连载中': ['连载中', 'working'], '连载中（导入既有作品）': ['连载中', 'working'], '新建 · 未开写': ['未开写', 'wait'], '空书 · 可手写': ['空书', 'wait'] };
        var s = stMap[b.status] || ['—', 'wait'];
        var deviation = b.id === 'B-01' ? '<span class="st st-choice">目标偏差：库存 0，周更 3 章难以维持</span>'
          : (b.publishedCount ? '<span class="st st-working">计划内</span>' : '<span class="st st-wait">待开始</span>');
        return { attrs: ' class="clickable" data-action="book.goto" data-id="' + b.id + '"',
          cells: [
            '<span class="t-title">' + WB.esc(b.title) + '</span><div class="t3 xs">' + WB.esc(b.genre) + ' · ' + WB.esc(b.platform) + '</div>',
            WB.stBadge(s[0], s[1]),
            '<div class="stock"><i class="' + (st.publishable ? '' : 'draft') + '" title="可发布正式章 ' + st.publishable + '"></i><span class="sm">' + st.publishable + ' 章可发布</span></div>' +
              '<div class="t3 xs">排期 ' + st.planned + ' · 起草 ' + st.draft + '</div>',
            '<span class="sm">' + WB.esc(b.id === 'B-01' ? 'ch43 已上线 · 下一步 ch44' : (b.publishedCount ? 'ch18 已上线 · 第 19 章已排期' : '尚无正文')) + '</span>',
            deviation
          ] };
      });

      var body =
        ui.hdr('经营 · 业务首页',
          '作品组合、目标偏差、库存与排期、真实待决、最近团队行动与下一检查。这里回答：继续什么、介入什么。',
          '<button class="btn" data-action="nav.view" data-area="market" data-view="direction">看方向提案</button>' +
          '<button class="btn primary" data-action="act.book" data-fn="createBook">开一本新书</button>') +

        ui.panel({ title: '作品组合', sub: books.length + ' 部作品 · 同一 Business',
          tight: true, body: rows.length ? ui.tbl(['作品', '状态', '库存与排期', '最近位置', '目标偏差'], rows) :
            ui.empty('还没有作品', '可以从方向提案开始，或直接创建一本空书手写正文。') ,
          footer: '<span>无作品时：先定方向或直接开写；不因缺市场数据阻塞创作。</span>' }) +

        ui.panel({ title: '真实待决', sub: pending.length + ' 项需要作者输入',
          body: pending.length ? '<div class="rows">' + pending.map(function (d) {
            var kindMap = { Operating: ['经营决定', 'choice'], Choice: ['作者选择', 'wait'], Gate: ['权限 / 外部动作', 'blocked'] };
            var k = kindMap[d.kind];
            return '<div class="row clickable" data-action="nav.view" data-area="operate" data-view="plan">' +
              '<div class="row-main"><div class="row-t">' + WB.esc(d.title) + WB.stBadge(k[0], k[1]) + '</div>' +
              '<div class="row-s">' + WB.esc(d.question) + '</div></div>' +
              '<div class="row-side"><span class="sm t3">' + WB.esc(d.by === 'E-01' ? '沈知远提出' : '发布责任人提出') + '</span>' +
              '<span class="t3 xs">' + WB.esc(d.raisedAt) + '</span></div></div>';
          }).join('') + '</div>' : ui.empty('当前没有待决', '待决不假装执行；研究与他书工作可以继续。'),
          footer: '<span>Choice / Gate / Operating 三种目的分别表达，不把它做成异常告警。</span>' }) +

        ui.panel({ title: '最近团队行动', sub: '按相关性分组，不重复计数', body: ui.worksList(recent),
          footer: '<span>Provider 执行不算员工；同一 Work 只在此处出现一次。</span>' }) +

        ui.panel({ title: '下一检查', sub: S.nextCheck.at,
          body: '<div class="tl">' + S.nextCheck.items.map(function (i, x) {
            return '<div class="tl-i ' + (x === 0 ? 'ok' : 'wait') + '"><div class="tl-t">' + WB.esc(i.k) + '</div><div class="tl-s">' + WB.esc(i.v) + '</div></div>';
          }).join('') + '</div>',
          footer: '<span>监测与整理可持续进行；重大方向、作品终止与发布权限仍由作者决定。</span>' });

      return body;
    },
    aside: function () {
      var S = WB.S, b = WB.scopeBook();
      var mine = S.works.filter(function (w) { return w.area === 'operate' || w.status !== 'done'; }).slice(0, 3);
      return WB.asBlock('当前范围', '<div class="as-w"><div class="wt">' + WB.esc(b ? b.title : '—') + '</div>' +
          '<div class="ws">' + WB.esc(b ? b.platform + ' · ' + b.status : '') + '</div>' +
          '<div class="ws">' + WB.esc(b && b.goal ? b.goal : '') + '</div></div>') +
        WB.asBlock('责任与缺口', S.responsibilities.map(function (r) {
          return '<div class="as-w"><div class="wt">' + WB.esc(r.name) + '</div><div class="ws">' +
            (r.owner ? WB.ownerHtml(r.owner) : '<span class="own none">缺责任人</span>') +
            (r.note ? '<br><span class="t3">' + WB.esc(r.note) + '</span>' : '') + '</div></div>';
        }).join('')) +
        WB.asBlock('相关工作', mine.map(function (w) { return WB.workHtml(w); }).join('')) +
        WB.asBlock('演示状态', '<div class="sm t2">改动保存在本机浏览器；' +
          '<button class="btn link" data-action="act.book" data-fn="resetDemo">重置演示数据</button></div>' +
          '<div class="sm t3" style="margin-top:6px">最近 ' + WB.esc((S.__runtime.log.slice(-1)[0] || {}).t || '—') + '</div>');
    }
  });

  WB.on['book.goto'] = function (el, d) { WB.S.__scope.bookId = d.id; WB.go('book', 'overview', { bookId: d.id }); };

  /* ---------------- 经营 · 计划与决定详情 ---------------- */
  WB.register('operate.plan', {
    render: function (ctx) {
      var S = WB.S;
      var d1 = WB.decision('DEC-01'), d2 = WB.decision('DEC-02'), d3 = WB.decision('DEC-03');
      var done = S.decisions.filter(function (d) { return d.status === 'applied'; });

      function optRows(d) {
        return d.options.map(function (o) {
          var chosen = d.decision === o.key;
          return { attrs: ' class="clickable" data-action="act.dec" data-fn="decision" data-a1="' + d.id + '" data-a2="' + o.key + '"',
            cells: [
              '<span class="strong">' + WB.esc(o.label) + '</span>' + (chosen ? WB.stBadge('已选', 'published') : ''),
              '<span class="sm">' + WB.esc(o.impact) + '</span>',
              '<span class="sm t2">' + WB.esc(o.risk) + '</span>'
            ] };
        });
      }

      var decideBlock = d1.status === 'pending' ? ui.tbl(['选项', '影响', '风险'], optRows(d1)) +
          '<div class="btnrow" style="margin-top:10px">' +
          '<button class="btn primary" data-action="act.dec" data-fn="decision" data-a1="DEC-01" data-a2="slow">确认：调为周更 2 章</button>' +
          '<button class="btn" data-action="act.dec" data-fn="decision" data-a1="DEC-01" data-a2="keep">确认：保持周更 3 章</button>' +
          '<button class="btn ghost" data-action="act.dec" data-fn="decision" data-a1="DEC-01" data-a2="defer">暂缓一周</button></div>'
        : '<div class="note info"><b>该决定已处理</b><br>选择：' + WB.esc(d1.decision === 'slow' ? '调为周更 2 章' : d1.decision === 'keep' ? '保持周更 3 章' : '暂缓') +
          ' · ' + WB.esc(d1.decidedAt) + '<br>范围：只改后续计划；已发布章节与历史数据不动。</div>' +
          '<div class="btnrow" style="margin-top:8px"><button class="btn sm" data-action="act.dec" data-fn="decision" data-a1="DEC-01" data-a2="defer">改为暂缓并重议</button></div>';

      return ui.hdr('经营计划与决定详情',
        '对比继续 / 调向 / 调频 / 暂停 / 完结 / 开新书的影响。决定呈现依据、影响范围、选项与不确定性；不由数据波动自动砍书。',
        '<button class="btn" data-action="nav.view" data-area="audience" data-view="attribution">查看归因依据</button>') +

        ui.panel({ title: '待决一 · ' + WB.esc(d1.title), sub: d1.kind + ' · ' + WB.esc(d1.by === 'E-01' ? '沈知远（代行 Leader）' : '') + ' 提出 · ' + WB.esc(d1.raisedAt),
          body: '<div class="note choice">' + WB.esc(d1.question) + '</div>' +
            '<div class="hr"></div><div class="sm strong" style="margin-bottom:6px">依据</div>' +
            '<ul style="padding-left:18px;margin:0 0 10px" class="sm">' + d1.evidence.map(function (e) { return '<li>' + WB.esc(e) + '</li>'; }).join('') + '</ul>' +
            decideBlock +
            '<div class="hr"></div>' + ui.note('bound', '<b>应用边界：</b>' + WB.esc(d1.boundary)),
          footer: '<span>普通进度不是 Decision；这里只出现需要人判断的事。</span>' }) +

        ui.panel({ title: '待决二 · ' + WB.esc(d2.title), sub: 'Choice（作者选择，中性展示）',
          body: '<div class="sm">' + WB.esc(d2.question) + '</div><div class="hr"></div>' +
            '<div class="btnrow"><button class="btn primary" data-action="nav.view" data-area="book" data-view="manuscript">去正文工作面逐项处理</button>' +
            '<span class="sm t3">采纳 / 部分采纳 / 拒绝都合法；确认前线上仍是 v2。</span></div>' }) +

        ui.panel({ title: '待决三 · ' + WB.esc(d3.title), sub: 'Gate（有外部副作用）',
          body: '<div class="sm">' + WB.esc(d3.question) + '</div>' +
            ui.note('bound', '批准 ≠ 执行成功：授权后仍需提交并等待回执；参数实质改变需重新判断。') +
            '<div class="btnrow" style="margin-top:8px">' +
            (d3.status === 'pending'
              ? '<button class="btn primary" data-action="act.dec" data-fn="decision" data-a1="DEC-03" data-a2="approve">授权重新提交</button>' +
                '<button class="btn" data-action="nav.view" data-area="publish" data-view="queue">先看发布队列</button>'
              : '<span class="st st-published">已授权</span> <button class="btn sm" data-action="nav.view" data-area="publish" data-view="queue">去队列</button>') + '</div>' }) +

        ui.panel({ title: '已应用的决定', sub: done.length + ' 项',
          body: done.map(function (d) {
            return '<div class="stack" style="margin-bottom:10px"><div class="row-t">' + WB.esc(d.title) + WB.stBadge('已应用', 'published') + '</div>' +
              '<div class="sm t2">' + WB.esc(d.question) + '</div>' +
              '<div class="sm">' + WB.esc(d.appliedNote || '') + '</div>' +
              '<div class="t3 xs">接受 ' + WB.esc(d.decidedAt) + ' · 应用 ' + WB.esc(d.appliedAt || '') + '</div></div>';
          }).join('') +
          '<div class="note bound">Accepted ≠ Applied ≠ Published：接受是一个动作，应用到计划是第二个动作，平台上线是外部事实。</div>' });
    },
    aside: function () {
      var S = WB.S;
      return WB.asBlock('决定相关对象', WB.workHtml(S.works.filter(function (w) { return w.area === 'book' || w.area === 'audience'; })[0] || S.works[0])) +
        WB.asBlock('责任', WB.ownerHtml('E-01') + '<div class="sm t3" style="margin-top:6px">经营计划由编辑兼任；重大方向、作品终止与发布权限由作者决定。</div>') +
        WB.asBlock('不会自动发生', '<div class="sm t2">· 不因单章数据差自动停书<br>· 不自动采纳所有 AI 稿<br>· 不同步改写历史 Canon</div>');
    }
  });
})();
