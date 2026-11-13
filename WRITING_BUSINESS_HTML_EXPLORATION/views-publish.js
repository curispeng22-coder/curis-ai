/* ============================================================================
   views-publish.js — 连载发布（发布队列与日历 / 提交与回执详情 / 平台账号与作品映射）
   底线：草稿保存 ≠ 提交；提交 ≠ 上线；平台预审 ≠ 作者接受；
        未知外部效果先核验、不重发；本地暂停排期不等于平台撤销。
   ========================================================================== */
(function () {
  var ui = WB.ui;

  var stateMap = {
    live: ['已上线', 'published'], scheduled: ['已排期', 'wait'], waiting: ['已提交 · 等待回执', 'wait'],
    draft: ['待排期', 'wait'], rejected: ['平台退回', 'rejected'], unknown: ['外部状态未知', 'unknown']
  };

  /* ---------------- 行动 ---------------- */
  WB.on['pub.pkg'] = function (el, d) {
    var S = WB.S, q = WB.queueItem(d.id), ch = WB.chapter(q.chapter);
    var checks = [
      ['章序', '第 ' + ch.no + ' 章，紧接已上线章节（无跳号）', true],
      ['稿件版本', '正式 ' + q.version + (ch.published ? '（线上为 ' + ch.published + '，本次为修订）' : ''), true],
      ['库存', '本批 1 章；发布后库存 ' + Math.max(0, WB.stockOf(q.bookId).publishable - 1), true],
      ['格式', '章节正文纯文本，无外链', true],
      ['声明 / 合同', '按 ' + q.target + ' 当前适用规则核验；<b>完整 AI 条款本轮未确认</b>', false],
      ['必要权限', '账号 ' + q.account + ' 已核对；平台侧定时任务能力未确认', false]
    ];
    WB.openDrawer({ title: '发布包预览 · ' + q.title, sub: WB.esc(q.target + ' · ' + q.account + ' · 版本 ' + q.version),
      body: '<div class="note bound">导出与预览只完成<b>准备</b>，不等于发布。</div><div class="hr"></div>' +
        ui.tbl(['检查项', '内容', '结论'], checks.map(function (c) {
          return { cells: [c[0], '<span class="sm">' + c[1] + '</span>', c[2] ? WB.stBadge('通过', 'published') : WB.stBadge('待核验', 'unknown')] };
        })) +
        ui.note('choice', '两项未确认：平台声明/合同条款与定时发布能力。未确认前按人工路径提交，并把未确认项留在台账上。'),
      footer: '<button class="btn" data-action="pub.export" data-id="' + q.id + '">导出发布包（Mock）</button>' +
        '<button class="btn primary" data-action="act.q" data-fn="submit" data-a1="' + q.id + '">登记人工提交</button>' });
  };
  WB.on['pub.export'] = function (el, d) {
    var S = WB.S, q = WB.queueItem(d.id);
    S.queue.forEach(function (x) { if (x.id === d.id) x.exportedAt = WB.now(); });
    WB.save();
    WB.toast('已导出发布包（Mock，本地生成）：导出完成不等于发布，仍需人工提交', 'warn');
    WB.render();
  };
  WB.on['pub.receipt'] = function (el, d) { WB.go('publish', 'receipts', { id: d.id }); };
  WB.on['pub.verifyHelp'] = function (el, d) {
    WB.openDrawer({ title: '外部状态核验清单 · ' + d.id, sub: '未知先核验，不重复提交',
      body: '<div class="tl">' +
        ['打开平台作品管理，确认目标账号为 ACC-01',
         '查找第 40 章是否存在：<b>存在</b> → 比对线上版本与本地 v1，登记回执',
         '不存在 → 确认平台侧无草稿或待审残留，再决定是否补发',
         '两种情况都要登记证据（截图/时间），未核验前保持「未知」'].map(function (t, i) {
          return '<div class="tl-i unknown"><div class="tl-t">第 ' + (i + 1) + ' 步</div><div class="tl-s">' + t + '</div></div>';
        }).join('') + '</div>' +
        ui.note('bound', '效果未知先核验；<b>不默认重发</b>。若已上线又重发，会造成重复章节。'),
      footer: '<button class="btn primary" data-action="act.q" data-fn="verify" data-a1="' + d.id + '">核验完成：已在线上线</button>' +
        '<button class="btn" data-action="act.q" data-fn="submit" data-a1="' + d.id + '">核验为未上线 → 重新提交</button>' });
  };
  WB.on['pub.disconnect'] = function (el, d) {
    var inFlight = WB.S.queue.filter(function (q) { return q.account === d.id && ['scheduled', 'waiting', 'unknown'].indexOf(q.state) >= 0; });
    WB.modal({ title: '断开映射影响确认',
      body: '<p>断开 <b>' + WB.esc(d.name) + '</b> 前，以下在途事项受影响：</p>' +
        (inFlight.length ? '<ul class="sm" style="padding-left:18px">' + inFlight.map(function (q) {
          return '<li>' + WB.esc(q.title) + '（' + stateMap[q.state][0] + '）</li>';
        }).join('') + '</ul>' : '<div class="sm t2">当前无在途提交。</div>') +
        ui.note('bound', '断开<b>不删除历史</b>：已产生的发布记录、回执与观测保留；重新打开会恢复当前对象与待决。') +
        '<div class="sm t2">断开后：该平台不再出现在可发布目标里；已提交平台定时任务需另行在平台核验。</div>',
      footer: '<button class="btn" data-action="close-modal">取消</button>' +
        '<button class="btn dark" data-action="pub.disconnectDo" data-id="' + d.id + '">确认断开</button>' });
  };
  WB.on['pub.disconnectDo'] = function (el, d) {
    var m = WB.byId(WB.S.mappings, d.id);
    m.status = 'disconnected';
    WB.closeModal(); WB.save();
    WB.toast('已断开映射；历史记录保留，在途事项仍需在平台核验', 'warn'); WB.render();
  };
  WB.on['pub.verifyMapping'] = function (el, d) {
    var m = WB.byId(WB.S.mappings, d.id);
    if (m.status === 'blocked') { WB.toast('该映射受授权范围限制：未确认独家/授权前不提交，仅保留目标建议', 'warn'); return; }
    m.verifiedAt = WB.now(); m.status = 'verified';
    WB.save(); WB.toast('映射已核对：外部 ID 与内部章号一致', 'ok'); WB.render();
  };
  WB.on['pub.addAccount'] = function (el, d) {
    WB.modal({ title: '添加平台账号（示例）',
      body: '<div class="note bound">原型不执行真实登录、验证码与账号绑定。登录与验证码要交回作者本人处理。</div>' +
        '<div class="grid g2" style="margin-top:10px"><div class="fld"><label>平台</label><input class="inp" value="待选择" /></div>' +
        '<div class="fld"><label>站点</label><input class="inp" value="主站" /></div></div>' +
        '<div class="fld" style="margin-top:8px"><label>合同 / 授权范围</label><input class="inp" placeholder="例如：独家 / 非独家 / 待确认" /></div>',
      footer: '<button class="btn" data-action="close-modal">取消</button>' +
        '<button class="btn primary" data-action="close-modal">保存（示例：不产生真实连接）</button>' });
  };
  WB.on['pub.resched'] = function (el, d) {
    WB.modal({ title: '重新排期 · ' + d.id,
      body: '<div class="fld"><label>计划时间</label><select class="sel" id="rsWhen"><option>2026-09-23 20:00</option><option>2026-09-24 20:00</option><option>2026-09-25 21:00</option></select></div>' +
        ui.note('bound', '若平台侧已有定时任务，本地改期不会撤销它 —— 需要另行在平台核验。'),
      footer: '<button class="btn" data-action="close-modal">取消</button>' +
        '<button class="btn primary" data-action="pub.reschedDo" data-id="' + d.id + '">确认改期</button>' });
  };
  WB.on['pub.reschedDo'] = function (el, d) {
    var when = document.getElementById('rsWhen').value;
    WB.act.schedule(d.id, when); WB.closeModal();
  };

  /* ---------------- 发布队列与日历 ---------------- */
  WB.register('publish.queue', {
    render: function () {
      var S = WB.S;
      var rows = S.queue.map(function (q) {
        var m = stateMap[q.state], ch = WB.chapter(q.chapter);
        var acts = '<div class="btnrow">';
        if (q.state === 'draft') acts += '<button class="btn sm" data-action="pub.resched" data-id="' + q.id + '">排期</button>';
        if (q.state === 'scheduled') acts += '<button class="btn sm" data-action="pub.pkg" data-id="' + q.id + '">预览发布包</button>' +
          '<button class="btn sm" data-action="act.q" data-fn="submit" data-a1="' + q.id + '">提交</button>' +
          '<button class="btn sm ghost" data-action="act.q" data-fn="pauseSchedule" data-a1="' + q.id + '">暂停排期</button>';
        if (q.state === 'waiting') acts += '<button class="btn sm" data-action="act.q" data-fn="verify" data-a1="' + q.id + '">核验回执</button>';
        if (q.state === 'unknown') acts += '<button class="btn sm" data-action="pub.verifyHelp" data-id="' + q.id + '">核验外部状态</button>';
        if (q.state === 'rejected') acts += '<button class="btn sm" data-action="nav.view" data-area="book" data-view="manuscript">看修改稿</button>' +
          '<button class="btn sm" data-action="nav.view" data-area="operate" data-view="plan">申请重新提交</button>';
        if (q.state === 'live') acts += '<button class="btn sm" data-action="nav.view" data-area="audience" data-view="performance">看表现</button>';
        acts += '<button class="btn sm ghost" data-action="pub.receipt" data-id="' + q.id + '">回执</button></div>';
        return { cells: [
          '<span class="strong">' + WB.esc(q.title) + '</span><div class="t3 xs">' + WB.esc(q.target) + ' · ' + WB.esc(q.account) + '</div>',
          WB.stBadge(m[0], m[1]),
          '<span class="vtag formal">' + WB.esc(q.version) + '</span>' + (ch && ch.published && ch.published !== q.version ? '<div class="t3 xs">线上 ' + WB.esc(ch.published) + '</div>' : ''),
          '<span class="sm">' + WB.esc(q.plannedAt || '未排期') + '</span>' + (q.submittedAt ? '<div class="t3 xs">提交 ' + WB.esc(q.submittedAt) + '</div>' : ''),
          '<span class="sm">' + WB.esc(q.evidence || '—') + '</span>' +
            (q.rejectReason ? '<div class="t3 xs">原因：' + WB.esc(q.rejectReason) + '</div>' : ''),
          acts
        ] };
      });

      var b01 = WB.stockOf('B-01'), b02 = WB.stockOf('B-02');
      return ui.hdr('发布队列与日历',
        '把库存变成有序连载：平台、Book、章节顺序、稿件版本、计划时间与等待/失败状态。',
        '<button class="btn" data-action="nav.view" data-area="publish" data-view="accounts">账号与映射</button>',
        '<span>队列 ' + S.queue.length + ' 项</span><span class="t4">|</span><span>等待回执 ' +
        S.queue.filter(function (q) { return q.state === 'waiting'; }).length + '</span><span class="t4">|</span><span>外部未知 ' +
        S.queue.filter(function (q) { return q.state === 'unknown'; }).length + '</span>') +

        ui.panel({ title: '发布队列', tight: true, body: ui.tbl(['章节', '状态', '稿件版本', '计划 / 提交', '证据 / 说明', '操作'], rows),
          footer: '<span>状态文案与颜色共同表达；未知与失败不用同一种语气。</span>' }) +

        ui.panel({ title: '库存与节奏', body:
          '<div class="grid g2">' +
          '<div><div class="sm strong">《夜行灯》</div><div class="figs" style="margin-top:6px">' +
          '<div class="fig"><span class="n sm">' + b01.publishable + '</span><span class="l">可发布正式章</span></div>' +
          '<div class="fig"><span class="n sm">' + b01.planned + '</span><span class="l">已排期</span></div>' +
          '<div class="fig"><span class="n sm">' + b01.draft + '</span><span class="l">候选 / 大纲</span></div></div>' +
          '<div class="sm t2" style="margin-top:6px">库存 0：ch44 候选未采纳，未采纳候选不计库存 → 直接影响节奏决定（DEC-01）。</div></div>' +
          '<div><div class="sm strong">《白鹭洲纪事》</div><div class="figs" style="margin-top:6px">' +
          '<div class="fig"><span class="n sm">' + b02.publishable + '</span><span class="l">可发布正式章</span></div>' +
          '<div class="fig"><span class="n sm">' + b02.planned + '</span><span class="l">已排期</span></div>' +
          '<div class="fig"><span class="n sm">' + b02.draft + '</span><span class="l">起草中</span></div></div>' +
          '<div class="sm t2" style="margin-top:6px">第 19 章正式稿已接受并排期 09-22 21:00（本地计划）。</div></div>' +
          '</div>' +
          ui.note('bound', '更新节奏是作品计划，不把平台全勤/合同要求混成统一日更数。'), footer:
          '<button class="btn sm" data-action="nav.view" data-area="operate" data-view="plan">去节奏决定</button>' }) +

        ui.panel({ title: '提交方式与边界', body:
          '<div class="grid g3">' + S.submitModes.map(function (m) {
            return '<div class="fld"><label>' + WB.esc(m.label) + '</label><div class="sm t2">' + WB.esc(m.note) + '</div></div>';
          }).join('') + '</div>' +
          ui.note('bound', '草稿保存 ≠ 提交；提交 ≠ 上线；平台预审 ≠ 作者接受。<b>本地暂停排期不等于平台已撤销定时任务。</b>') });
    },
    aside: function () {
      var S = WB.S;
      return WB.asBlock('责任人', WB.ownerHtml('E-03') + '<div class="sm t3" style="margin-top:6px">发布责任：有界提交与回执登记；不做平台能力承诺。</div>') +
        WB.asBlock('外部未知', (function () {
          var u = S.queue.filter(function (q) { return q.state === 'unknown'; });
          return u.length ? u.map(function (q) {
            return '<div class="as-w"><div class="wt">' + WB.esc(q.title) + '</div><div class="ws">' + WB.stBadge('待核验', 'unknown') +
              '<br>' + WB.esc(q.stateNote || '') + '</div></div>';
          }).join('') : '<div class="sm t3">当前没有外部未知项。</div>';
        })()) +
        WB.asBlock('相关 Work', S.works.filter(function (w) { return w.area === 'publish'; }).map(function (w) { return WB.workHtml(w); }).join(''));
    }
  });

  /* ---------------- 提交 / 回执详情 ---------------- */
  WB.register('publish.receipts', {
    render: function (ctx) {
      var S = WB.S;
      var id = ctx.params.id || 'Q-04';
      var q = WB.queueItem(id) || S.queue[3];
      var ch = WB.chapter(q.chapter);
      var r = S.receipts[q.id] || {};
      var m = stateMap[q.state];

      var steps = [
        { t: '排期', s: q.plannedAt || '未排期', k: q.plannedAt ? 'ok' : 'wait' },
        { t: '提交', s: q.submittedAt || '尚未提交' + (q.exportedAt ? '（已导出发布包 ' + q.exportedAt + '，仅完成准备）' : ''), k: q.submittedAt ? 'ok' : 'wait' },
        { t: '等待 / 回执', s: r.kind === 'verified' ? '平台回执已核验（' + (r.onlineVersion || '') + '）'
            : r.kind === 'rejected' ? '平台退回：' + (r.reason || '') : r.kind === 'none' ? '无回执 — 外部效果未知' : (r.note || '等待平台回执'), k: r.kind === 'verified' ? 'ok' : r.kind === 'rejected' ? 'choice' : 'unknown' },
        { t: '核验线上版本', s: q.verifiedAt ? '已核验于 ' + q.verifiedAt + '，线上版本 = ' + (q.publishedVersion || q.version) : '未核验', k: q.verifiedAt ? 'ok' : 'unknown' },
        { t: '观察', s: q.state === 'live' ? '观察窗已建立（发布后 24h / 7d）' : '未建立（尚未确认上线）', k: q.state === 'live' ? 'ok' : 'wait' }
      ];

      var picker = '<div class="scopebar"><div class="sb-row"><span class="sl-lb">选择队列项</span>' +
        ui.chips(S.queue.map(function (x) { return [x.id, x.title.replace('第 ', '').replace(' 章', '')]; }), q.id, 'pub.pickRow') + '</div></div>';

      return ui.hdr('提交与回执详情 · ' + WB.esc(q.title),
        '原稿与实际发布版、目标账号、声明、回执、线上链接与审查原因分开记录。这里回答：到底上线了没有、是哪一个版本。',
        '<button class="btn" data-action="nav.view" data-area="publish" data-view="queue">回队列</button>',
        '<span>当前：' + WB.esc(m[0]) + '</span><span class="t4">|</span><span>账号 ' + WB.esc(q.account) + '</span>') +
        picker +

        '<div class="grid" style="grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:12px;align-items:start">' +
        '<div>' +
        ui.panel({ title: '事实对照', body: ui.kv([
          ['内部章节', '第 ' + ch.no + ' 章 · ' + WB.esc(ch.title) + '（' + WB.esc(q.chapter) + '）'],
          ['提交版本', '<span class="vtag formal">' + WB.esc(q.version) + '</span>'],
          ['实际线上版本', q.publishedVersion ? '<span class="vtag pub">' + WB.esc(q.publishedVersion) + '</span>' : (q.state === 'unknown' ? WB.unknown('未知（无回执）') : WB.unknown('尚未确认'))],
          ['目标账号', WB.esc(q.target + ' · ' + q.account)],
          ['声明 / 合同', '按适用站点与作品形态核验；<b>完整 AI 与签约条款本轮未确认</b>'],
          ['回执证据', WB.esc((r.screens || []).join('、') || r.note || '—')],
          ['线上链接', q.state === 'live' ? '已登记（原型不打开外部页面）' : '—'],
          ['审查原因', WB.esc(q.rejectReason || '—')]
        ]) }) +
        ui.panel({ title: '发布时间线', body: '<div class="tl">' + steps.map(function (s2) {
          return '<div class="tl-i ' + s2.k + '"><div class="tl-t">' + WB.esc(s2.t) + '</div><div class="tl-s">' + s2.s + '</div></div>';
        }).join('') + '</div>' }) +
        '</div>' +

        '<div>' +
        (q.state === 'unknown' ? ui.panel({ title: '未知路径（不重发）', body:
          '<div class="note bound"><b>提交后网络中断，平台侧是否已上线未知。</b><br>' + WB.esc(q.stateNote || '') + '</div>' +
          '<div class="btnrow" style="margin-top:8px">' +
          '<button class="btn primary" data-action="pub.verifyHelp" data-id="' + q.id + '">打开核验清单</button>' +
          '<button class="btn" data-action="act.q" data-fn="waitReceipt" data-a1="' + q.id + '">保持等待</button></div>' +
          '<div class="sm t3" style="margin-top:8px">效果未知先核验；不重复发章，避免线上出现两个第 40 章。</div>' }) : '') +
        (q.state === 'rejected' ? ui.panel({ title: '退回处理', body:
          '<div class="note choice"><b>平台退回：</b>' + WB.esc(q.rejectReason || '') + '</div>' +
          '<div class="sm" style="margin-top:8px">修改稿 <b>R-42</b> 已准备（机构名脱敏）。重新提交会产生外部副作用，需作者授权。</div>' +
          '<div class="btnrow" style="margin-top:8px">' +
          '<button class="btn" data-action="nav.view" data-area="book" data-view="manuscript">查看修改稿</button>' +
          '<button class="btn primary" data-action="nav.view" data-area="operate" data-view="plan">申请重新提交（Gate）</button></div>' }) : '') +
        (q.state === 'live' ? ui.panel({ title: '已上线后的动作', body:
          '<div class="sm t2">线上版本与本地正式版本一致。可建立/延续观察窗，并在「读者与收益」把表现关联到该发布版本与时间窗。</div>' +
          '<div class="btnrow" style="margin-top:8px">' +
          '<button class="btn" data-action="nav.view" data-area="audience" data-view="performance">去表现总览</button>' +
          '<button class="btn" data-action="nav.view" data-area="audience" data-view="attribution">看内容归因</button></div>' }) : '') +
        (q.state === 'scheduled' ? ui.panel({ title: '排期待执行', body:
          '<div class="note"><b>本地排期 ≠ 平台定时任务。</b>本原型不执行外部提交；到期后走人工路径提交并登记回执。</div>' +
          '<div class="btnrow" style="margin-top:8px">' +
          '<button class="btn primary" data-action="pub.pkg" data-id="' + q.id + '">预览发布包</button>' +
          '<button class="btn" data-action="act.q" data-fn="submit" data-a1="' + q.id + '">登记人工提交</button></div>' }) : '') +
        (q.state === 'waiting' ? ui.panel({ title: '等待回执', body:
          '<div class="note"><b>等待 ≠ 失败。</b>已登记提交事实，回执未到；到点核验，不重发。</div>' +
          '<div class="btnrow" style="margin-top:8px">' +
          '<button class="btn primary" data-action="act.q" data-fn="verify" data-a1="' + q.id + '">核验完成：已上线</button>' +
          '<button class="btn" data-action="act.q" data-fn="waitReceipt" data-a1="' + q.id + '">继续等待</button></div>' }) : '') +
        (q.state === 'draft' ? ui.panel({ title: '待排期', body:
          '<div class="sm t2">先排期或直接提交。稿件版本 ' + WB.esc(q.version) + ' 已确认。</div>' +
          '<div class="btnrow" style="margin-top:8px"><button class="btn primary" data-action="pub.resched" data-id="' + q.id + '">排期</button>' +
          '<button class="btn" data-action="act.q" data-fn="submit" data-a1="' + q.id + '">直接提交</button></div>' }) : '') +
        ui.panel({ title: '发布版快照', body:
          '<div class="sm t2">本地改到 v3 不把已发布 v2 的数据归给 v3。读者是否看过旧版未知时，不能当作随机 A/B 实验。</div>' +
          '<div class="btnrow" style="margin-top:8px"><button class="btn sm" data-action="book.versions" data-chapter="' + q.chapter + '">查看版本历史</button></div>' }) +
        '</div></div>';
    },
    aside: function (ctx) {
      var S = WB.S, q = WB.queueItem(ctx.params.id || 'Q-04') || S.queue[3];
      return WB.asBlock('当前对象', '<div class="as-w"><div class="wt">' + WB.esc(q.title) + '</div><div class="ws">' +
          WB.esc(q.target) + ' · 版本 ' + WB.esc(q.version) + '</div><div class="ws">' + WB.stBadge(stateMap[q.state][0], stateMap[q.state][1]) + '</div></div>') +
        WB.asBlock('责任人', WB.ownerHtml('E-03')) +
        WB.asBlock('返回位置', '<div class="sm t2">返回后会保留队列的筛选与滚动位置；发布项、观测与经验都能回到原处。</div>');
    }
  });
  WB.on['pub.pickRow'] = function (el, d) { WB.go('publish', 'receipts', { id: d.key }, { replace: true }); };

  /* ---------------- 平台账号与作品映射 ---------------- */
  WB.register('publish.accounts', {
    render: function () {
      var S = WB.S;
      return ui.hdr('平台账号与作品映射',
        '连接真实平台，但不创造第二本书：账号、站点、合同范围、Book/章外部 ID、能力与权限缺口、规则来源都在这里。',
        '<button class="btn primary" data-action="pub.addAccount">添加账号</button>',
        '<span>账号 ' + S.accounts.length + ' 个</span><span class="t4">|</span><span>映射 ' + S.mappings.length + ' 条</span>') +

        ui.panel({ title: '账号与合同范围', tight: true, body: ui.tbl(['账号', '平台 / 站点', '合同 / 授权范围', '已确认能力', '缺口（本原型未做）', '规则来源'],
          S.accounts.map(function (a) {
            return { cells: [
              '<b>' + WB.esc(a.id) + '</b><div class="t3 xs">' + WB.esc(a.holder) + '</div>',
              WB.esc(a.platform) + '<div class="t3 xs">' + WB.esc(a.site) + '</div>',
              '<span class="sm">' + WB.esc(a.scope) + '</span>',
              a.capability.map(function (c) { return '<span class="pill">' + WB.esc(c) + '</span>'; }).join(' '),
              a.gap.map(function (c) { return WB.unknown(c); }).join(' '),
              '<span class="sm t2">' + WB.esc(a.rules) + '</span><div class="t3 xs">' + WB.esc(a.verified) + '</div>'
            ] };
          })) ,
          footer: '<span>「平台支持某能力」不等于「Curis 有可用接口」；未确认的字段保留为未知。</span>' }) +

        ui.panel({ title: 'Book / 章 外部映射', tight: true, body: ui.tbl(['映射', 'Book', '外部作品 ID', '范围', '章映射', '状态', '操作'],
          S.mappings.map(function (m) {
            var st = m.status === 'verified' ? ['已核验', 'published'] : m.status === 'blocked' ? ['受限 · 待授权', 'blocked'] : ['已断开', 'wait'];
            return { cells: [
              '<b>' + WB.esc(m.id) + '</b>',
              WB.esc(m.bookTitle) + '<div class="t3 xs">' + WB.esc(m.bookId) + '</div>',
              WB.esc(m.externalId) + '<div class="t3 xs">' + WB.esc(m.accountId) + '</div>',
              '<span class="sm">' + WB.esc(m.scope) + '</span>',
              '<span class="sm">' + WB.esc(m.chapterMap) + '</span>',
              WB.stBadge(st[0], st[1]) + (m.note ? '<div class="t3 xs">' + WB.esc(m.note) + '</div>' : ''),
              '<div class="btnrow">' +
                '<button class="btn sm" data-action="pub.verifyMapping" data-id="' + m.id + '">核验</button>' +
                (m.status === 'blocked' ? '<button class="btn sm" data-action="pub.disconnect" data-id="' + m.id + '">处理授权</button>'
                  : '<button class="btn sm ghost" data-action="pub.disconnect" data-id="' + m.id + '">断开</button>') +
              '</div>'
            ] };
          })) ,
          footer: '<span>断开不删历史；重新打开会恢复当前对象、正式稿、待决与外部未知。</span>' }) +

        '<div class="grid g2">' +
        ui.panel({ title: '映射纪律', body:
          '<div class="sm t2">· 章拆分/合并/调序需显式映射内部章与平台章<br>· 不能只靠标题相同自动匹配<br>' +
          '· 既有作品可导入平台目录并逐条确认，不重新创建所有身份<br>· 跨平台发布须先核实独家/授权范围，不默认一稿多发</div>' }) +
        ui.panel({ title: '本原型不执行', body:
          '<div class="sm t2">· 真实登录 / 验证码 / 支付<br>· 真实账号绑定<br>· 外部提交与平台定时任务<br>· 任何外部网络请求</div>' +
            ui.note('bound', '登录与验证码交回作者本人；恢复后重新核验目标账号与稿件。') }) +
        '</div>';
    },
    aside: function () {
      var S = WB.S;
      return WB.asBlock('责任人', WB.ownerHtml('E-03')) +
        WB.asBlock('受限期事项', (function () {
          var bl = S.mappings.filter(function (m) { return m.status === 'blocked'; });
          return bl.length ? bl.map(function (m) {
            return '<div class="as-w"><div class="wt">' + WB.esc(m.id + ' · ' + m.bookTitle + ' → ' + m.accountId) + '</div>' +
              '<div class="ws">' + WB.stBadge('受限 · 待授权', 'blocked') + '<br>' + WB.esc(m.note || '') + '</div></div>';
          }).join('') : '<div class="sm t3">无。</div>';
        })()) +
        WB.asBlock('相关 Work', S.works.filter(function (w) { return w.area === 'publish'; }).map(function (w) { return WB.workHtml(w); }).join(''));
    }
  });
})();
