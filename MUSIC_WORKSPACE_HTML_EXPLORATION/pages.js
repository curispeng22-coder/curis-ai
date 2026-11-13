/* ============================================================
   pages.js — Curis · AI 音乐经营 工作区（视觉探索）
   五区 Work Area 视图 + 交互（经营/研究/制作/发布/数据复盘）。
   全部数据来自 MU.data；交互真实改变 state 与 MU.data，驱动闭环。
   依赖 app.js（MU.state / MU.* 工具）。
   ============================================================ */
window.MU = window.MU || {};
MU.pages = MU.pages || {};
(function () {
  "use strict";

  var D = MU.data;
  var S = MU.state;
  function esc(s) { return MU.esc(s); }
  function fmt(n) { return MU.fmt(n); }
  function cover(seed, size, label) { return MU.coverHTML(seed, size, label); }
  /* 兼容两种调用序：
       $(sel, root)  —— 绝对多数调用方使用
       $(root, sel)  —— 少数旧调用
     两者都返回匹配到的第一个元素；root 缺省时为 document。 */
  function $(a, b) {
    if (typeof a === "string") {
      var scope = (b && typeof b.querySelector === "function") ? b : document;
      return scope.querySelector(a);
    }
    if (a && typeof a.querySelector === "function" && typeof b === "string") {
      return a.querySelector(b);
    }
    return null;
  }
  function $all(a, b) {
    var sel = typeof a === "string" ? a : b;
    var scope = typeof a === "string"
      ? ((b && typeof b.querySelectorAll === "function") ? b : document)
      : a;
    if (!scope || typeof scope.querySelectorAll !== "function") return [];
    return Array.prototype.slice.call(scope.querySelectorAll(sel));
  }

  /* 通用：Song 行（封面 + 标题 + 元数据 + 状态） */
  function songRow(song, extra) {
    var st = MU.songStatus(song);
    var prov = song.approvedMaster ? "" :
      (song.versions && song.versions.length ? '<span class="mw-tag">版本 ' + song.versions.length + '</span>' : "");
    return '<div class="mw-row" data-song="' + song.id + '">' +
      cover(song.cover, "c44", song.name.slice(0, 1)) +
      '<div class="r-main"><div class="r-title">' + esc(song.name) +
        ' <span class="mw-status ' + st.cls + '">' + st.label + '</span></div>' +
        '<div class="r-meta">' + esc(song.style) + ' · ' + esc(song.mood) + ' · ' + esc(song.targetPlatform) +
        (song.employee ? ' · ' + esc(D.getEmp(song.employee).name) : '') + '</div>' +
        (prov ? '<div>' + prov + '</div>' : '') + '</div>' +
      '<div class="r-side">' +
        (song.bpm ? '<span class="mw-tag">' + song.bpm + ' BPM</span>' : '') +
        (extra || "") + '</div></div>';
  }

  /* 通用：跳转 Song（按状态路由到对应区） */
  MU.gotoSong = function (song) {
    if (song.status === "published") { S.area = "review"; S.selectedSong = song.id; S.selectedSongName = song.name; }
    else if (song.status === "research" || song.status === "proposal") { S.area = "research"; S.sub = "directions"; }
    else { S.area = "production"; S.selectedSong = song.id; S.selectedSongName = song.name; }
    MU.render();
  };

  /* ============================================================
     ① 经营 Operating
     ============================================================ */
  MU.pages.operating = function (root, util) {
    var inProd = D.songs.filter(function (s) { return ["research", "proposal", "production", "ready"].indexOf(s.status) >= 0; }).length;
    var published = D.songs.filter(function (s) { return s.status === "published"; });
    var openCeo = D.ceoDecisions.filter(function (c) { return c.status === "open"; }).length;
    var waiting = D.songs.filter(function (s) { return s.release && s.release.state === "auth_stop"; }).length;

    var lanes = [
      { label: "研究中 / 提案", cls: "neutral", list: D.songs.filter(function (s) { return s.status === "research" || s.status === "proposal"; }) },
      { label: "制作中", cls: "attention", list: D.songs.filter(function (s) { return s.status === "production"; }) },
      { label: "待发布", cls: "warning", list: D.songs.filter(function (s) { return s.status === "ready"; }) },
      { label: "已发布", cls: "published", list: published }
    ];

    var board = lanes.map(function (ln) {
      var items = ln.list.length ? ln.list.map(function (s) { return songRow(s); }).join("")
        : '<div class="mw-empty" style="padding:var(--ui-sp-4)">暂无</div>';
      return '<div style="margin-bottom:var(--ui-sp-4)"><div class="mw-eyebrow"><span class="mw-status ' + ln.cls + '">' +
        ln.label + '</span> · ' + ln.list.length + ' 首</div>' + items + '</div>';
    }).join("");

    var team = D.areas; // not used
    var empCards = Object.keys(D.employees).map(function (k) {
      var e = D.employees[k];
      var dot = e.status === "working" ? "ontrack" : e.status === "waiting" ? "warning" : "neutral";
      return '<div class="mw-card tight" style="display:grid;grid-template-columns:auto 1fr;gap:var(--ui-sp-3);align-items:center">' +
        '<div class="mw-ws-avatar" style="background:hsl(' + e.avatarHue + ' 55% 45%)">' + esc(e.name.slice(0, 1)) + '</div>' +
        '<div><div style="display:flex;align-items:center;gap:var(--ui-sp-2)"><b style="font-size:var(--ui-fs-2)">' + esc(e.name) + '</b>' +
        '<span class="mw-status ' + dot + '">' + (e.status === "working" ? "在岗" : e.status === "waiting" ? "等待中" : "空闲") + '</span></div>' +
        '<div class="mw-helper">' + esc(e.role) + ' · ' + esc(e.now) + '</div></div></div>';
    }).join("");

    var ceoBanners = D.ceoDecisions.filter(function (c) { return c.status === "open"; }).map(function (c) {
      return '<div class="mw-decision" data-ceo="' + c.id + '">' +
        '<div class="d-head"><span class="d-flag">⚠ 需要 CEO 决策</span><span class="d-title">' + esc(c.title) + '</span></div>' +
        '<div class="d-grid"><div><b>级别</b> ' + esc(c.level) + '</div><div><b>建议时限</b> ' + esc(c.time) + '</div>' +
        '<div style="grid-column:1/3"><b>原因</b> ' + esc(c.why) + '</div>' +
        '<div style="grid-column:1/3"><b>影响</b> ' + esc(c.impact) + '</div>' +
        '<div style="grid-column:1/3"><b>风险</b> ' + esc(c.risk) + '</div>' +
        '<div style="grid-column:1/3"><b>建议</b> ' + esc(c.advice) + '</div></div>' +
        '<div class="d-actions">' +
        '<button class="mw-btn primary sm" data-ceo-act="approve" data-id="' + c.id + '">批准并执行</button>' +
        '<button class="mw-btn sm" data-ceo-act="reject" data-id="' + c.id + '">拒绝</button>' +
        '<button class="mw-btn ghost sm" data-ceo-act="note" data-id="' + c.id + '">提供指示</button>' +
        '</div></div>';
    }).join("") || '<div class="mw-callout">暂无需 CEO 拍板的重大事项。</div>';

    root.innerHTML =
      '<div class="mw-page-head"><h1 class="mw-page-title">经营</h1>' +
      '<p class="mw-page-sub">音乐经营中枢：最近怎么样、往哪走、谁在做、什么要你定。</p></div>' +

      '<div class="mw-metrics">' +
        metric("在制歌曲", inProd, "研究中+制作+待发布", "") +
        metric("已发布", published.length, "汽水音乐", "本周期目标 6 首") +
        metric("待处理", openCeo + waiting, "CEO 决策 " + openCeo + " · 等待用户 " + waiting, "需你介入") +
        metric("本期目标达成", "3 / 6", "已发布 / 目标", "↑ 持续推进") +
      '</div>' +

      '<div class="mw-section"><div class="mw-section-title">经营目标与策略</div>' +
        '<div class="mw-grid" style="grid-template-columns:1fr 1fr">' +
          '<div class="mw-card"><div class="mw-eyebrow">经营目标（Leader 设定）</div><div style="font-size:var(--ui-fs-2);line-height:1.6">' + esc(D.operating.goal) + '</div></div>' +
          '<div class="mw-card"><div class="mw-eyebrow">选题策略</div><div style="font-size:var(--ui-fs-2);line-height:1.6">' + esc(D.operating.strategy) + '</div>' +
          '<div class="mw-eyebrow" style="margin-top:var(--ui-sp-2)">红线（不做什么）</div><div class="mw-helper">' + esc(D.operating.forbidden) + '</div></div>' +
        '</div></div>' +

      '<div class="mw-section"><div class="mw-section-title">Song 管线 · 持续经营总览</div>' + board + '</div>' +

      '<div class="mw-section"><div class="mw-section-title">团队与责任（Employee ≠ Provider）</div>' +
        '<div class="mw-grid" style="grid-template-columns:1fr 1fr">' + empCards + '</div></div>' +

      '<div class="mw-section"><div class="mw-section-title">需要 CEO 决定</div>' + ceoBanners + '</div>' +

      '<div class="mw-section"><div class="mw-callout"><b>下一首为什么做：</b>' + esc(D.operating.nextCycle) +
        ' <a href="#" data-go-research style="color:var(--ui-accent)">查看研究区方向 →</a></div></div>';

    // 绑定
    $all(root, "[data-song]").forEach(function (el) {
      el.addEventListener("click", function () {
        var s = D.getSong(el.getAttribute("data-song")); if (s) MU.gotoSong(s);
      });
    });
    var gr = $("[data-go-research]"); if (gr) gr.addEventListener("click", function (e) { e.preventDefault(); S.area = "research"; S.sub = "directions"; MU.render(); });
    $all(root, "[data-ceo-act]").forEach(function (b) {
      b.addEventListener("click", function () {
        var id = b.getAttribute("data-id"); var c = D.ceoDecisions.filter(function (x) { return x.id === id; })[0];
        if (!c) return;
        var act = b.getAttribute("data-ceo-act");
        if (act === "approve") c.status = "resolved";
        else if (act === "reject") c.status = "rejected";
        else { MU.toast("（Mock）已记录你的指示，将回填到经营对话。"); return; }
        MU.render();
      });
    });

    /* 右侧专业导航：持续经营看板（按经营区实需命名） */
    var health = [
      ["在制阶段分布", "研究 2 · 制作 2 · 待发布 1"],
      ["发布→回收周期", "约 9 天（8-30 发布 → 9-08 首采）"],
      ["Learning 转化", "4 条 Learning，3 条已被下一首采纳"],
      ["Provider 健康", "Mureka 98% · ElevenLabs 100%"],
      ["Computer Use 触发", "本周 3 次，Auth Stop 1 次"]
    ].map(function (r) { return '<div class="mw-util-row"><span>' + r[0] + '</span><b>' + esc(r[1]) + '</b></div>'; }).join("");
    util.innerHTML = '<p class="mw-util-title">持续经营看板</p>' +
      '<div class="mw-util-card"><h4>经营健康度</h4>' + health + '</div>' +
      '<div class="mw-util-card"><h4>九问速览</h4>' +
        utilRow("已自主完成", "3 首发布 + 4 条 Learning") +
        utilRow("正在做", "Song-04/05 制作中") +
        utilRow("等 Provider", "Song-05 首版生成中") +
        utilRow("等试听", "Song-04 A/B 待评审") +
        utilRow("等发布", "Song-08 卡登录验证") +
        utilRow("待 CEO", openCeo + " 项决策") + '</div>' +
      '<div class="mw-util-card"><h4>下一步</h4><p class="mw-helper">基于 Song-01 Learning，下一首强化「前置留白 Hook」。</p></div>';

    // 选中歌联动右侧
    $all(util, "a").forEach(function () {});
  };

  function metric(label, value, delta, caliber) {
    return '<div class="mw-metric"><div class="m-label">' + esc(label) + '</div>' +
      '<div class="m-value">' + esc(value) + '</div>' +
      (delta ? '<div class="m-delta">' + esc(delta) + '</div>' : '') +
      (caliber ? '<div class="m-caliber">' + esc(caliber) + '</div>' : '') + '</div>';
  }
  function utilRow(k, v) { return '<div class="mw-util-row"><span>' + esc(k) + '</span><b>' + esc(v) + '</b></div>'; }

  /* ============================================================
     ② 研究与方向 Research & Direction
     局部专业导航：趋势 / Reference / 歌曲方向（右侧）
     ============================================================ */
  MU.pages.research = function (root, util) {
    if (!S.sub) S.sub = "refs";
    var e = D.getEmp("e2");

    // 趋势视图
    function trendsView() {
      var rows = D.trends.map(function (t) {
        var p = D.platforms.filter(function (x) { return x.id === t.platform; })[0];
        return '<div class="mw-row" data-trend="' + t.id + '">' +
          '<div class="mw-ws-avatar" style="background:hsl(' + hashc(t.platform) + ' 50% 42%);width:36px;height:36px">' + esc((p ? p.name : "").slice(0, 1)) + '</div>' +
          '<div class="r-main"><div class="r-title">' + esc(t.signal) + ' <span class="mw-tag">' + esc(t.tag) + '</span>' +
            (t.recommend ? '<span class="mw-status ontrack">值得跟</span>' : '') + '</div>' +
            '<div class="r-meta">' + esc(p ? p.name : t.platform) + ' · 热度 ' + esc(t.heat) + ' · ' + esc(t.fresh) + '</div>' +
            '<div class="mw-helper" style="margin-top:3px">' + esc(t.note) + '</div></div>' +
          '<div class="r-side"><span class="mw-tag" style="color:var(--ui-success)">' + esc(t.growth) + '</span></div></div>';
      }).join("");
      return '<div class="mw-section"><div class="mw-section-title">趋势与榜单（资产化）</div>' + rows + '</div>';
    }

    // Reference 网格
    function refsView() {
      var cards = D.references.map(function (r) {
        var p = D.platforms.filter(function (x) { return x.id === r.platform; })[0];
        return '<div class="mw-row" data-ref="' + r.id + '">' +
          cover(r.cover, "c56", r.title.slice(0, 1)) +
          '<div class="r-main"><div class="r-title">' + esc(r.title) + ' <span class="mw-tag">' + esc(r.style) + '</span></div>' +
          '<div class="r-meta">' + esc(r.artist) + ' · ' + esc(p ? p.name : r.platform) + ' · ' + esc(r.heat) + '</div>' +
          '<div class="mw-helper" style="margin-top:3px">' + esc(r.mood) + ' · ' + r.bpm + ' BPM · Hook：' + esc(r.hook) + '</div></div>' +
          '<div class="r-side"><span class="mw-tag">参考</span></div></div>';
      }).join("");
      return '<div class="mw-section"><div class="mw-section-title">参考研究 · Pattern 提取（' + D.references.length + '）</div>' + cards + '</div>';
    }

    // 参考详情
    function refDetail(r) {
      var p = D.platforms.filter(function (x) { return x.id === r.platform; })[0];
      var pt = r.pattern;
      var patRows = [["主题", pt.theme], ["情绪", pt.emotion], ["结构", pt.structure], ["Vocal", pt.vocal], ["编曲", pt.arrangement], ["受众", pt.audience]]
        .map(function (kv) { return '<div class="mw-util-row"><span>' + kv[0] + '</span><b>' + esc(kv[1]) + '</b></div>'; }).join("");
      return '<div class="mw-section"><div class="mw-btn-row" style="margin-bottom:var(--ui-sp-3)"><button class="mw-btn ghost sm" data-back-refs>← 返回参考库</button></div>' +
        '<div style="display:grid;grid-template-columns:120px 1fr;gap:var(--ui-sp-4);align-items:start">' +
          cover(r.cover, "c120", r.title.slice(0, 1)) +
          '<div><div class="mw-page-title" style="font-size:var(--ui-fs-5)">' + esc(r.title) + '</div>' +
          '<div class="mw-helper">' + esc(r.artist) + ' · ' + esc(p ? p.name : r.platform) + ' · ' + esc(r.heat) + ' · ' + r.bpm + ' BPM</div>' +
          '<div style="margin-top:var(--ui-sp-2)"><span class="mw-tag">' + esc(r.style) + '</span><span class="mw-tag">' + esc(r.mood) + '</span></div>' +
          '<div class="mw-card" style="margin-top:var(--ui-sp-3)"><div class="mw-eyebrow">Hook</div><div style="font-size:var(--ui-fs-2);line-height:1.6">' + esc(r.hook) + '</div></div>' +
          '<div class="mw-btn-row" style="margin-top:var(--ui-sp-3)">' +
            '<button class="mw-btn primary" data-act="form-direction" data-ref="' + r.id + '">形成歌曲方向 →</button>' +
            '<button class="mw-btn" data-act="ask-ref">问研究 Employee：为什么火？</button></div>' +
          '<div id="ref-detail-msg"></div>' +
          '</div></div></div>';
    }

    // 歌曲方向列表
    function dirsView() {
      var cards = D.directions.map(function (d) {
        var refs = d.fromRefs.map(function (rid) { var r = D.getRef(rid); return r ? '<span class="mw-tag">' + esc(r.title) + '</span>' : ''; }).join("");
        var st = d.status === "in_production" ? '<span class="mw-status ontrack">已进入制作</span>' : (d.approved ? '<span class="mw-status ontrack">已批准</span>' : '<span class="mw-status warning">待审批</span>');
        return '<div class="mw-card" data-dir="' + d.id + '">' +
          '<div class="r-title" style="font-size:var(--ui-fs-3);font-weight:600">' + esc(d.name) + ' ' + st + '</div>' +
          '<div class="mw-helper" style="margin-top:4px">受众 ' + esc(d.audience) + ' · 创建 ' + esc(d.createdAt) + '</div>' +
          '<div style="margin-top:var(--ui-sp-2)">' + refs + '</div>' +
          '<div class="mw-helper" style="margin-top:var(--ui-sp-2)"><b>依据：</b>' + esc(d.basis) + '</div>' +
          '<div class="mw-helper"><b>约束：</b>' + esc(d.constraint) + '</div>' +
          (d.status === "in_research" && !d.approved ? '<div class="mw-btn-row" style="margin-top:var(--ui-sp-2)"><button class="mw-btn primary sm" data-act="approve-dir" data-id="' + d.id + '">批准并进入制作 →</button></div>' : '') +
          '</div>';
      }).join("");
      return '<div class="mw-section"><div class="mw-section-title">歌曲方向（原创重组，禁抄旋律）</div>' + cards + '</div>';
    }

    // 研究 Employee 工作台
    function wsView() {
      return '<div class="mw-section"><div class="mw-section-title">研究 Employee 工作台</div>' +
        '<div class="mw-ws"><div class="mw-ws-head"><div class="mw-ws-avatar" style="background:hsl(' + e.avatarHue + ' 55% 45%)">' + esc(e.name.slice(0, 1)) + '</div>' +
        '<div class="mw-ws-who"><div class="w-name">' + esc(e.name) + ' · ' + esc(e.role) + '</div><div class="w-role"><span class="mw-status ontrack">在岗</span> 当前 Provider：无（趋势来自平台 API）</div></div></div>' +
        '<div class="mw-ws-now">' + esc(e.now) + '</div>' +
        '<div class="mw-conv" id="research-conv">' +
          convMsg("emp", "苏晚", "我已把 City Pop 回潮、抖音夜场景、Tidal Letter 复古结构三条信号标为值得跟，母体 Pattern 准备落到《霓虹慢车》方向卡。") +
        '</div>' +
        bindComposer("research-conv", function (txt) {
          return "好问题。这首火在三件事：① 副歌切分贝斯 groove 对味；② 84–112 BPM 的慢板都市夜情绪；③ TikTok/抖音的副歌切片传播。建议你方向卡沿用母题、不要抄旋律。";
        }) +
        '</div></div>';
    }

    // 主内容路由
    var main = "";
    if (S.selectedRef) {
      var r = D.getRef(S.selectedRef);
      main = refDetail(r); S.selectedRefTitle = r ? r.title : "";
    } else if (S.sub === "trends") main = trendsView();
    else if (S.sub === "directions") main = dirsView();
    else main = refsView();

    root.innerHTML =
      '<div class="mw-page-head"><h1 class="mw-page-title">研究与方向</h1>' +
      '<p class="mw-page-sub">趋势 / 榜单资产化 → Reference Pattern 提取 → 原创 Song Direction。点击参考可看 Pattern 并「形成歌曲方向」。</p></div>' +
      main + wsView();

    // 绑定
    var back = $("[data-back-refs]"); if (back) back.addEventListener("click", function () { S.selectedRef = null; renderSafe(); });
    $all(root, "[data-ref]").forEach(function (el) { el.addEventListener("click", function () { S.selectedRef = el.getAttribute("data-ref"); renderSafe(); }); });
    $all(root, "[data-act='form-direction']").forEach(function (b) { b.addEventListener("click", function () { MU.formDirection(b.getAttribute("data-ref")); }); });
    $all(root, "[data-act='ask-ref']").forEach(function (b) { b.addEventListener("click", function () { askRefDetail(); }); });
    $all(root, "[data-act='approve-dir']").forEach(function (b) { b.addEventListener("click", function () { MU.approveDirection(b.getAttribute("data-id")); }); });

    /* 右侧专业导航 */
    util.innerHTML = '<p class="mw-util-title">研究 · 专业导航</p>' +
      '<div class="mw-util-nav">' +
        utilNavItem("trends", "趋势 / 榜单", D.trends.length) +
        utilNavItem("refs", "Reference", D.references.length) +
        utilNavItem("directions", "歌曲方向", D.directions.length) +
      '</div>' +
      (S.selectedRef ? '<div class="mw-util-card"><h4>Pattern 画像</h4>' + (function () { var rr = D.getRef(S.selectedRef); if (!rr) return ""; var pt = rr.pattern; return [["主题", pt.theme], ["情绪", pt.emotion], ["结构", pt.structure], ["Vocal", pt.vocal], ["编曲", pt.arrangement]].map(function (kv) { return utilRow(kv[0], kv[1]); }).join(""); })() + '</div>' : '') +
      '<div class="mw-util-card"><h4>红线</h4><p class="mw-helper">仅提取 Pattern（风格/结构/Hook），不存受版权歌词/旋律；送交 Provider 的参考须自有/授权。</p></div>';
    $all(util, "[data-sub]").forEach(function (b) { b.addEventListener("click", function () { S.sub = b.getAttribute("data-sub"); S.selectedRef = null; renderSafe(); }); });
  };

  function hashc(s) { var h = 0; for (var i = 0; i < String(s).length; i++) h = (h * 31 + s.charCodeAt(i)) % 360; return h; }
  function utilNavItem(sub, label, count) {
    return '<a class="mw-util-nav-item' + (S.sub === sub && !S.selectedRef ? " active" : "") + '" data-sub="' + sub + '"><span>' + esc(label) + '</span>' +
      (count != null ? '<span class="u-count">' + count + '</span>' : '') + '</a>';
  }
  function convMsg(who, name, text) {
    return '<div class="mw-msg ' + who + '"><div class="m-bubble"><div class="m-meta">' + esc(name) + '</div>' + esc(text) + '</div></div>';
  }

  // 通用对话 Composer（返回 HTML 片段，绑定在 bindConv 中完成）
  function bindComposer(convId, empReply) {
    return '<div class="mw-composer"><textarea placeholder="对研究 Employee 说点什么…" rows="1"></textarea>' +
      '<button class="mw-btn primary" data-send="' + convId + '">发送</button></div>';
  }

  function askRefDetail() {
    var box = document.getElementById("ref-detail-msg");
    if (!box) return;
    box.innerHTML = convMsg("emp", "苏晚", "这首最近火在：① 副歌切分贝斯 groove 对味；② 84–112 BPM 慢板都市夜情绪契合推荐池；③ 抖音副歌切片传播强。结构、情绪、Hook 可直接拆进我们的方向，但旋律必须原创。");
  }

  function renderSafe() { MU.render(); }

  /* 形成歌曲方向（Reference → 新方向） */
  MU.formDirection = function (refId) {
    var ref = D.getRef(refId); if (!ref) return;
    var dir = {
      id: "dir-" + Date.now(), name: ref.title + "（方向）", fromRefs: [refId], status: "in_research",
      audience: ref.pattern.audience, constraint: "基于《" + ref.title + "》母题原创重组，不抄具体旋律/Hook 表达。",
      basis: "来自参考《" + ref.title + "》Pattern 提取（" + ref.pattern.theme + "）。", employee: "e2", approved: false, createdAt: "今天", fresh: true
    };
    D.directions.unshift(dir);
    S.selectedRef = null; S.sub = "directions"; S.area = "research";
    MU.render();
  };

  /* 批准方向 → 进入制作（创建 Song） */
  MU.approveDirection = function (dirId) {
    var dir = D.directions.filter(function (x) { return x.id === dirId; })[0]; if (!dir) return;
    dir.approved = true; dir.status = "in_production";
    // 关闭研究区待 CEO 决策（如有）
    D.ceoDecisions.forEach(function (c) { if (c.area === "research" && c.status === "open") c.status = "resolved"; });
    var song = {
      id: "song-" + Date.now(), name: dir.name.replace("（方向）", ""), direction: dir.basis, style: "待定", mood: "待定",
      bpm: 100, targetPlatform: "汽水音乐", employee: "e3", provider: "Mureka", status: "proposal",
      cover: "rv" + (D.references.length + D.directions.length), hook: "（待制作 Employee 生成）",
      versions: [], approvedMaster: null, release: null, performance: null,
      proposalNote: "方向已批准，待制作 Employee 生成首版。"
    };
    D.songs.unshift(song);
    S.area = "production"; S.selectedSong = song.id; S.selectedSongName = song.name;
    MU.render();
  };

  /* ============================================================
     ③ 歌曲制作 Song Production（最核心）
     局部专业导航：Song 队列 / 当前 Song / Versions
     ============================================================ */
  MU.pages.production = function (root, util) {
    var e = D.getEmp("e3");
    var queue = D.songs.filter(function (s) { return s.status === "production" || s.status === "ready" || s.status === "proposal"; });

    if (!S.selectedSong && queue.length) S.selectedSong = queue[0].id;
    var song = S.selectedSong ? D.getSong(S.selectedSong) : null;

    // 播放器（模拟试听）
    function playerHTML() {
      return '<div class="mw-player"><button class="mw-play-btn" data-play>▶</button>' +
        '<div class="p-bar" data-bar><div class="p-fill" data-fill></div><div class="p-head" data-head></div></div>' +
        '<span class="p-time" data-time>0:00 / 0:30</span></div>';
    }

    function versionCard(v) {
      var scores = v.scores ? Object.keys(v.scores).map(function (k) {
        return '<div class="mw-score"><span>' + esc(scoreName(k)) + '</span><div class="s-track"><div class="s-fill" style="width:' + v.scores[k] + '%"></div></div><span class="s-num">' + v.scores[k] + '</span></div>';
      }).join("") : '<div class="mw-helper">生成中（轮询 preparing）…</div>';
      var selCls = (S.compare.a === v.id || S.compare.b === v.id) ? " sel" : "";
      var st = v.status === "approved" ? '<span class="mw-status published">已定稿</span>'
        : v.status === "review" ? '<span class="mw-status review">待评审</span>'
        : v.status === "rejected" ? '<span class="mw-status rejected">已驳回</span>'
        : '<span class="mw-status generating">生成中</span>';
      return '<div class="mw-ver-card' + selCls + '" data-ver="' + v.id + '">' +
        '<div class="v-head"><span class="ver-label' + (v.status === "approved" ? " approved" : "") + '">' + v.label + '</span>' +
          '<div><div style="font-weight:600;font-size:var(--ui-fs-2)">版本 ' + v.label + '</div><div class="mw-helper">' + esc(v.provider) + ' · ' + esc(v.model) + '</div></div>' +
          '<div style="margin-left:auto">' + st + '</div></div>' +
        '<div class="mw-helper">' + esc(v.note) + '</div>' +
        (v.scores ? '<div class="mw-score-list">' + scores + '</div>' : '') +
        '<div class="mw-btn-row" style="margin-top:var(--ui-sp-2)">' +
          (v.scores ? '<button class="mw-btn ghost sm" data-ver-play="' + v.id + '">试听</button>' : '') +
          '<button class="mw-btn ghost sm" data-ver-cmp="' + v.id + '">对比</button>' +
          (v.status === "review" ? '<button class="mw-btn primary sm" data-ver-approve="' + v.id + '">定稿此版</button>' : '') +
          (v.status === "review" ? '<button class="mw-btn sm" data-ver-reject="' + v.id + '">驳回</button>' : '') +
        '</div></div>';
    }

    function comparePanel() {
      if (!S.compare.a || !S.compare.b) {
        return '<div class="mw-callout">选择两个版本点击「对比」，即可并排比较评分维度（能量/结构/响度/情绪/商业潜力）。</div>';
      }
      var va = song.versions.filter(function (x) { return x.id === S.compare.a; })[0];
      var vb = song.versions.filter(function (x) { return x.id === S.compare.b; })[0];
      if (!va || !vb) return "";
      var keys = ["energy", "structure", "loudness", "emotion", "commercial"];
      var rows = keys.map(function (k) {
        var a = va.scores ? va.scores[k] : 0, b = vb.scores ? vb.scores[k] : 0;
        var lead = a > b ? "a" : (b > a ? "b" : "");
        return '<tr><td>' + esc(scoreName(k)) + '</td><td style="text-align:right;font-weight:600;color:' + (lead === "a" ? "var(--ui-success)" : "var(--ui-text)") + '">' + a + '</td>' +
          '<td style="text-align:right;font-weight:600;color:' + (lead === "b" ? "var(--ui-success)" : "var(--ui-text)") + '">' + b + '</td></tr>';
      }).join("");
      return '<div class="mw-card"><div class="mw-section-title" style="font-size:var(--ui-fs-3)">A/B 比较 · ' + va.label + ' vs ' + vb.label + '</div>' +
        '<table class="mw-table"><thead><tr><th>维度</th><th style="text-align:right">版本 ' + va.label + '</th><th style="text-align:right">版本 ' + vb.label + '</th></tr></thead><tbody>' + rows + '</tbody></table>' +
        '<div class="mw-callout" style="margin-top:var(--ui-sp-2)"><b>Employee 初判：</b>版本 ' + (va.scores && vb.scores ? (va.scores.commercial >= vb.scores.commercial ? va.label : vb.label) : "") + ' 商业潜力更高，建议以其为母版基准。</div>' +
        '<div class="mw-btn-row" style="margin-top:var(--ui-sp-2)"><button class="mw-btn sm" data-cmp-clear>清除比较</button></div></div>';
    }

    // 制作 Employee 工作台（选中 Song 时含版本对话）
    function wsView() {
      var body = song
        ? '<div class="mw-ws-now">' + esc(e.now) + '</div>' +
          '<div class="mw-conv" id="prod-conv">' + convMsg("emp", "陈默", "Song-04《霓虹慢车》A/B 已生成完毕，在等你试听评审。C 版本（ElevenLabs 声线）正在生成。" + (S.selectedSong === "song-04" ? "" : "")) + '</div>' +
          bindComposer("prod-conv", function (txt) {
            if (/改|返工|重/.test(txt)) return "收到。我会据你的意见调整 Brief（人声后撤 / 升调），重新发起一个版本。";
            return "明白。我会继续推进《" + (song ? song.name : "") + "》的版本评审，并把结果同步给你。";
          })
        : '<div class="mw-ws-now">当前没有选中的 Song，请先在队列中选择。</div>';
      return '<div class="mw-section"><div class="mw-section-title">制作 Employee 工作台</div>' +
        '<div class="mw-ws"><div class="mw-ws-head"><div class="mw-ws-avatar" style="background:hsl(' + e.avatarHue + ' 55% 45%)">' + esc(e.name.slice(0, 1)) + '</div>' +
        '<div class="mw-ws-who"><div class="w-name">' + esc(e.name) + ' · ' + esc(e.role) + '</div><div class="w-role"><span class="mw-status ontrack">在岗</span> 当前 Provider：' + (song ? esc(song.provider) : "—") + ' / ElevenLabs Music</div></div></div>' +
        body + '</div></div>';
    }

    // 主内容
    var main = "";
    if (!song) {
      main = '<div class="mw-empty">队列中暂无制作中的 Song。可在研究区「形成歌曲方向 → 批准进入制作」。</div>';
    } else {
      var verGrid = song.versions.length ? '<div class="mw-ver-grid">' + song.versions.map(versionCard).join("") + '</div>'
        : '<div class="mw-empty">尚无版本。点击下方「发起首版生成」。</div>';
      main =
        '<div class="mw-page-head"><h1 class="mw-page-title">歌曲制作</h1>' +
        '<p class="mw-page-sub">核心链：方向 → Brief → Provider 生成 → 版本 A/B/C → 试听·比较·评审 → 定稿 Approved Master。</p></div>' +
        '<div style="display:grid;grid-template-columns:120px 1fr;gap:var(--ui-sp-4);align-items:start;margin-bottom:var(--ui-sp-4)">' +
          cover(song.cover, "c120", song.name.slice(0, 1)) +
          '<div><div class="mw-page-title" style="font-size:var(--ui-fs-5)">' + esc(song.name) + '</div>' +
          '<div class="mw-helper">' + esc(song.style) + ' · ' + esc(song.mood) + ' · ' + song.bpm + ' BPM · 目标 ' + esc(song.targetPlatform) + ' · ' + esc(D.getEmp(song.employee).name) + '</div>' +
          '<div style="margin-top:var(--ui-sp-2)"><span class="mw-tag">' + esc(song.direction) + '</span></div>' +
          (song.status === "proposal" ? '<div class="mw-callout" style="margin-top:var(--ui-sp-2)">' + esc(song.proposalNote || "") + '</div>' : '') +
          '</div></div>' +
        (song.status !== "proposal" ? playerHTML() : '') +
        '<div class="mw-section"><div class="mw-section-title">版本工作室（Version Studio）</div>' +
          (song.status === "proposal" ? '<div class="mw-btn-row" style="margin-bottom:var(--ui-sp-3)"><button class="mw-btn primary" data-gen="' + song.id + '">发起首版生成（Mureka）</button></div>' : '') +
          verGrid + '</div>' +
        '<div class="mw-section"><div class="mw-section-title">A/B 比较</div>' + comparePanel() + '</div>' +
        (song.approvedMaster ? '<div class="mw-callout" style="border-color:rgba(63,207,134,.4);background:rgba(63,207,134,.08)"><b>Approved Master 已锁定：</b>版本 ' + masterLabel(song) + '。可在「发布」区组装 Release Package。</div>' : '');
    }

    root.innerHTML = main + wsView();

    // 绑定
    var gen = $("[data-gen]"); if (gen) gen.addEventListener("click", function () { MU.genVersion(gen.getAttribute("data-gen")); });
    $all(root, "[data-ver-approve]").forEach(function (b) { b.addEventListener("click", function () { MU.approveVersion(song.id, b.getAttribute("data-ver-approve")); }); });
    $all(root, "[data-ver-reject]").forEach(function (b) { b.addEventListener("click", function () { MU.rejectVersion(song.id, b.getAttribute("data-ver-reject")); }); });
    $all(root, "[data-ver-cmp]").forEach(function (b) { b.addEventListener("click", function () { toggleCompare(b.getAttribute("data-ver-cmp")); }); });
    $all(root, "[data-ver-play]").forEach(function (b) { b.addEventListener("click", function () { playVersion(b.getAttribute("data-ver-play")); }); });
    var cmpClear = $("[data-cmp-clear]"); if (cmpClear) cmpClear.addEventListener("click", function () { S.compare = { a: null, b: null }; renderSafe(); });
    bindPlay(root);

    /* 右侧专业导航：Song 队列 / 当前 Song / Versions */
    var queueHTML = queue.map(function (s) {
      var st = MU.songStatus(s);
      return '<a class="mw-util-nav-item' + (s.id === S.selectedSong ? " active" : "") + '" data-qsong="' + s.id + '">' +
        '<span>' + esc(s.name) + '</span><span class="u-count">' + st.label + '</span></a>';
    }).join("") || '<div class="mw-helper">队列为空</div>';
    var verList = song && song.versions.length ? song.versions.map(function (v) {
      return '<div class="mw-util-row"><span>版本 ' + v.label + ' · ' + esc(v.provider) + '</span><b>' + (v.status === "approved" ? "定稿" : v.status === "review" ? "待审" : v.status === "generating" ? "生成中" : v.status) + '</b></div>';
    }).join("") : '<div class="mw-helper">—</div>';
    util.innerHTML = '<p class="mw-util-title">制作 · 专业导航</p>' +
      '<div class="mw-util-card"><h4>Song 队列</h4><div class="mw-util-nav">' + queueHTML + '</div></div>' +
      (song ? '<div class="mw-util-card"><h4>当前 Song</h4>' + utilRow("名称", song.name) + utilRow("方向", song.direction) + utilRow("风格", song.style) + utilRow("BPM", song.bpm) + utilRow("Provider", song.provider) + '</div>' : '') +
      '<div class="mw-util-card"><h4>Versions</h4>' + verList + '</div>' +
      '<div class="mw-util-card"><h4>不做什么</h4><p class="mw-helper">不造 DAW / 音轨编辑器 / 混音器；Provider 仅作为版本元数据中的一条调用记录。</p></div>';
    $all(util, "[data-qsong]").forEach(function (b) { b.addEventListener("click", function () { S.selectedSong = b.getAttribute("data-qsong"); S.selectedSongName = D.getSong(S.selectedSong).name; renderSafe(); }); });
  };

  function scoreName(k) {
    return { energy: "能量", structure: "结构", loudness: "响度", emotion: "情绪", commercial: "商业潜力" }[k] || k;
  }
  function masterLabel(song) {
    var v = song.versions.filter(function (x) { return x.id === song.approvedMaster; })[0];
    return v ? v.label : "—";
  }
  function toggleCompare(verId) {
    if (S.compare.a === verId) { S.compare.a = null; }
    else if (S.compare.b === verId) { S.compare.b = null; }
    else if (!S.compare.a) S.compare.a = verId;
    else if (!S.compare.b) S.compare.b = verId;
    else { S.compare.a = S.compare.b; S.compare.b = verId; }
    renderSafe();
  }
  function bindComposerBind(root, convId, empReply) {
    var btn = $("[data-send='" + convId + "']", root);
    if (!btn) return;
    btn.addEventListener("click", function () {
      var ta = btn.previousElementSibling;
      var txt = ta ? ta.value.trim() : "";
      if (!txt) return;
      var conv = document.getElementById(convId);
      if (!conv) return;
      conv.innerHTML += convMsg("user", "你", txt);
      var reply = empReply ? empReply(txt) : "收到。";
      conv.innerHTML += convMsg("emp", "陈默", reply);
      if (ta) ta.value = "";
    });
  }
  function bindPlay(root) {
    var btn = $("[data-play]", root);
    if (!btn) return;
    btn.addEventListener("click", function () {
      if (S.playing) { stopPlay(); return; }
      S.playing = true; btn.textContent = "⏸";
      S.playProgress = 0;
      var fill = $("[data-fill]", root), head = $("[data-head]", root), bar = $("[data-bar]", root), time = $("[data-time]", root);
      S.playTimer = setInterval(function () {
        S.playProgress += 1;
        var pct = Math.min(100, S.playProgress / 30 * 100);
        if (fill) fill.style.width = pct + "%";
        if (head) head.style.left = pct + "%";
        if (time) time.textContent = Math.floor(S.playProgress / 2) + ":00 / 0:30";
        if (S.playProgress >= 30) stopPlay();
      }, 100);
    });
  }
  function stopPlay() {
    S.playing = false;
    if (S.playTimer) { clearInterval(S.playTimer); S.playTimer = null; }
    var btn = document.querySelector("[data-play]"); if (btn) btn.textContent = "▶";
  }
  /* ── 版本试听：内置 Mock 播放器 ──────────────────────────────────────
     单实例语义：任何时刻只有一个版本在播，切换版本自动停止上一个。
     进度条与计时落在该版本卡片内部；不弹浏览器对话框、不加载音频引擎
     （Curis 不造音频引擎，这里只表达「正在试听」的产品语义）。 */
  function resetVersionPlayUI() {
    $all(document, "[data-ver-play]").forEach(function (b) { b.textContent = "试听"; });
    $all(document, "[data-ver-playbar]").forEach(function (n) { if (n.parentNode) n.parentNode.removeChild(n); });
  }
  function haltPlay() {
    if (S.playTimer) { clearInterval(S.playTimer); S.playTimer = null; }
    S.playing = false; S.playVerId = null;
  }
  function playVersion(verId) {
    // 再点同一版本 = 暂停
    if (S.playing && S.playVerId === verId) { haltPlay(); S.playProgress = 0; resetVersionPlayUI(); return; }
    haltPlay(); resetVersionPlayUI();
    if (typeof stopPlay === "function") stopPlay();

    var card = document.querySelector('[data-ver="' + verId + '"]');
    if (!card) return;
    var btn = card.querySelector('[data-ver-play="' + verId + '"]');

    S.playing = true; S.playVerId = verId; S.playProgress = 0;
    if (btn) btn.textContent = "⏸ 暂停";

    var row = document.createElement("div");
    row.className = "mw-player";
    row.setAttribute("data-ver-playbar", verId);
    row.style.marginTop = "var(--ui-sp-2)";
    row.innerHTML =
      '<button class="mw-play-btn" type="button">⏸</button>' +
      '<div class="p-bar"><div class="p-fill"></div></div>' +
      '<span class="p-time">0:00 / 0:30 · 播放中</span>';
    var anchor = card.querySelector(".mw-btn-row");
    if (anchor) card.insertBefore(row, anchor); else card.appendChild(row);

    var fill = row.querySelector(".p-fill");
    var time = row.querySelector(".p-time");
    S.playTimer = setInterval(function () {
      S.playProgress += 1;
      var pct = Math.min(100, S.playProgress / 30 * 100);
      if (fill) fill.style.width = pct + "%";
      if (time) time.textContent = Math.floor(S.playProgress / 2) + ":00 / 0:30 · 播放中";
      if (S.playProgress >= 30) {
        if (time) time.textContent = "0:30 / 0:30 · 播放完毕";
        haltPlay();
        $all(document, "[data-ver-play]").forEach(function (b) { b.textContent = "试听"; });
      }
    }, 100);
  }

  /* 制作区交互 */
  MU.genVersion = function (songId) {
    var song = D.getSong(songId); if (!song) return;
    var label = String.fromCharCode(65 + song.versions.length);
    var provider = (song.versions.length % 2 === 0) ? "Mureka" : "ElevenLabs Music";
    var v = { id: "v-" + songId + "-" + label.toLowerCase() + Date.now(), label: label, provider: provider, model: provider === "Mureka" ? "mureka-1" : "el-music-1", status: "generating", scores: null, note: "陈默发起生成（轮询 preparing）。", createdAt: "进行中", fresh: true };
    song.versions.push(v);
    if (song.status === "proposal") song.status = "production";
    renderSafe();
  };
  MU.refreshVersion = function (songId, verId) {
    var v = D.getSong(songId).versions.filter(function (x) { return x.id === verId; })[0]; if (!v) return;
    v.status = "review";
    v.scores = { energy: 70 + Math.floor(Math.random() * 20), structure: 70 + Math.floor(Math.random() * 20), loudness: 70 + Math.floor(Math.random() * 20), emotion: 70 + Math.floor(Math.random() * 20), commercial: 70 + Math.floor(Math.random() * 20) };
    v.note = "生成完成，待试听评审。"; v.createdAt = "今天";
    renderSafe();
  };
  MU.approveVersion = function (songId, verId) {
    var song = D.getSong(songId); if (!song) return;
    song.versions.forEach(function (v) { if (v.id === verId) { v.status = "approved"; } else if (v.status !== "rejected") { v.status = "review"; } });
    song.approvedMaster = verId; song.status = "ready";
    D.ceoDecisions.forEach(function (c) { if (c.area === "publish" && c.status === "open" && /ElevenLabs/.test(c.title)) c.status = "resolved"; });
    renderSafe();
  };
  MU.rejectVersion = function (songId, verId) {
    var song = D.getSong(songId); if (!song) return;
    var v = song.versions.filter(function (x) { return x.id === verId; })[0]; if (v) { v.status = "rejected"; v.note = "已驳回，等待调整指令后重新生成。"; }
    renderSafe();
  };

  /* ============================================================
     ④ 发布 Publishing
     局部专业导航：Release 状态机 / 当前 Release Package
     ============================================================ */
  MU.pages.publish = function (root, util) {
    var e = D.getEmp("e4");
    var list = D.songs.filter(function (s) {
      return s.status === "ready" || (s.release && ["ready", "publishing", "auth_stop", "pending"].indexOf(s.release.state) >= 0);
    });

    function releaseCard(song) {
      var r = song.release || { state: "ready" };
      var st = MU.pubState(r.state);
      var flow = ["ready", "publishing", "auth_stop", "pending", "published"];
      var curIdx = flow.indexOf(r.state);
      var flowHTML = flow.map(function (f, idx) {
        var fs = MU.pubState(f);
        var cls = idx === curIdx ? " current" : (curIdx > 0 && idx < curIdx ? " done" : "");
        return '<span class="mw-state-node' + cls + '">' + fs.label + '</span>';
      }).join('<span class="mw-state-arrow">→</span>');

      var action = "";
      if (r.state === "ready") action = '<button class="mw-btn primary" data-pub-advance="' + song.id + '">经 Computer Use 发布 →</button>';
      else if (r.state === "publishing") action = '<button class="mw-btn primary" data-pub-advance="' + song.id + '">继续（Computer Use 填写/上传）</button>';
      else if (r.state === "auth_stop") action = '<button class="mw-btn" data-pub-resolve="' + song.id + '">前往处理 → 恢复后 Resume</button>';
      else if (r.state === "pending") action = '<button class="mw-btn primary" data-pub-advance="' + song.id + '">平台已审核，标记已上线</button>';
      else action = '<span class="mw-status published">已发布：' + esc(r.platform) + (r.url ? ' · ' + esc(r.url) : '') + (r.date ? ' · ' + esc(r.date) : '') + '</span>';

      var pkg = releasePackageHTML(song);

      return '<div class="mw-card" data-psong="' + song.id + '" style="margin-bottom:var(--ui-sp-4)">' +
        '<div style="display:flex;align-items:center;gap:var(--ui-sp-3);margin-bottom:var(--ui-sp-3)">' +
          cover(song.cover, "c56", song.name.slice(0, 1)) +
          '<div><div class="mw-page-title" style="font-size:var(--ui-fs-4)">' + esc(song.name) + '</div>' +
          '<div class="mw-helper">母版版本 ' + masterLabel(song) + ' · 目标 ' + esc(song.targetPlatform) + '</div></div>' +
          '<div style="margin-left:auto"><span class="mw-status ' + st.cls + '">' + st.label + '</span></div></div>' +
        '<div class="mw-state-flow" style="margin-bottom:var(--ui-sp-3)">' + flowHTML + '</div>' +
        (r.state === "auth_stop" ? '<div class="mw-decision" style="margin-bottom:var(--ui-sp-3)"><div class="d-head"><span class="d-flag">⛔ Authentication Stop Gate</span><span class="d-title">= WAITING_FOR_USER</span></div>' +
          '<div class="mw-helper">' + esc(r.reason || "登录 / 验证 / 风控命中，已停止自动点击，等待你处理。绝不绕过 CAPTCHA/MFA。") + '</div></div>' : '') +
        pkg +
        '<div class="mw-btn-row" style="margin-top:var(--ui-sp-3)">' + action + '</div>' +
        '</div>';
    }

    function releasePackageHTML(song) {
      var fields = [
        ["Song Name", song.name, true], ["Audio（母带）", song.approvedMaster ? "版本 " + masterLabel(song) + " ✓" : "缺失", !!song.approvedMaster],
        ["Cover", "3000×3000 ✓", true], ["Lyrics", "原创 TXT ✓", true], ["Artist", "Curis 虚拟艺人 ✓", true],
        ["Credits / AI 声明", "已勾选 AI 生成 ✓", true], ["ISRC", "已生成 ✓", true], ["授权状态", "Mureka 商用授权 ✓", true]
      ];
      var rows = fields.map(function (f) { return utilRow(f[0], f[1]); }).join("");
      return '<div class="mw-util-card" style="background:var(--ui-surface-2)"><h4>Release Package</h4>' + rows + '</div>';
    }

    root.innerHTML =
      '<div class="mw-page-head"><h1 class="mw-page-title">发布</h1>' +
      '<p class="mw-page-sub">汽水音乐第一实例：Release Package 组装 → 经 Computer Use 发布 → 遇验证即 Authentication Stop Gate（=WAITING_FOR_USER）→ 平台审核 → Published。</p></div>' +
      (list.length ? list.map(releaseCard).join("") : '<div class="mw-empty">队列中暂无待发布项。在「歌曲制作」定稿 Approved Master 后会出现在这里。</div>');

    $all(root, "[data-pub-advance]").forEach(function (b) { b.addEventListener("click", function () { MU.publishAdvance(b.getAttribute("data-pub-advance")); }); });
    $all(root, "[data-pub-resolve]").forEach(function (b) { b.addEventListener("click", function () { MU.resolveAuth(b.getAttribute("data-pub-resolve")); }); });

    /* 右侧专业导航 */
    util.innerHTML = '<p class="mw-util-title">发布 · 专业导航</p>' +
      '<div class="mw-util-card"><h4>Release 状态机</h4>' +
        utilRow("Ready", "包齐 + 三要素核验") + utilRow("Publishing", "Computer Use 填写/上传") +
        utilRow("Waiting for User", "Auth Stop Gate") + utilRow("Pending Review", "平台审核中") +
        utilRow("Published", "已上线") + '</div>' +
      '<div class="mw-util-card"><h4>Auth Stop Gate</h4><p class="mw-helper">命中登录/验证/风控即 STOP → 保存位置 → Human Gate → 通知。绝不绕过 CAPTCHA/MFA/风控。内部即既有 WAITING_FOR_USER。</p></div>' +
      '<div class="mw-util-card"><h4>Provider 实例</h4>' + utilRow("分发", "汽水音乐（Computer Use）") + utilRow("未来", "B2B Distributor API（M2 关闭主路径）") + '</div>';
  };

  function slug(s) { return String(s).replace(/[^\w一-龥]/g, "").slice(0, 8); }
  function seedPerf() {
    return { plays: 0, completion: 0, saves: 0, shares: 0, likes: 0, followers: 0, revenue: 0, source: "COMPUTER_USE", fresh: "待观察期后采集" };
  }
  MU.publishAdvance = function (songId) {
    var s = D.getSong(songId); if (!s) return;
    if (!s.release) s.release = { state: "ready", platform: s.targetPlatform, version: masterLabel(s) };
    var r = s.release;
    if (r.state === "ready") { r.state = "publishing"; r.gated = false; }
    else if (r.state === "publishing" && !r.gated) { r.state = "auth_stop"; r.gated = true; r.reason = "汽水后台要求登录验证，需你重新登录后再继续（Authentication Stop Gate = WAITING_FOR_USER，绝不绕过）。"; }
    else if (r.state === "auth_stop") { r.state = "publishing"; }
    else if (r.state === "publishing" && r.gated) { r.state = "pending"; }
    else if (r.state === "pending") { r.state = "published"; r.date = "今天"; r.url = "qishui.app/s/" + slug(s.name); s.status = "published"; s.performance = seedPerf(); }
    renderSafe();
  };
  MU.resolveAuth = function (songId) {
    var s = D.getSong(songId); if (!s || !s.release) return;
    if (s.release.state === "auth_stop") s.release.state = "publishing";
    renderSafe();
  };

  /* ============================================================
     ⑤ 数据与复盘 Data & Review
     局部专业导航：已发布 Song / 四模式 Result Intake
     ============================================================ */
  MU.pages.review = function (root, util) {
    var e = D.getEmp("e5");
    var published = D.songs.filter(function (s) { return s.status === "published"; });
    if (!S.selectedSong && published.length) S.selectedSong = published[0].id;
    var song = S.selectedSong ? D.getSong(S.selectedSong) : null;

    function metricsHTML(p) {
      var items = [
        ["Plays 播放", p.plays, "规模信号"], ["Completion 完播率", (p.completion * 100).toFixed(0) + "%", "质量信号·强驱动"],
        ["Saves 收藏", p.saves, "强意图"], ["Shares 分享", p.shares, "传播"], ["Likes 喜欢", p.likes, "弱意图"],
        ["Followers 粉丝", p.followers, "长期资产"], ["Revenue 收益", "¥" + fmt(p.revenue), "滞后·不夸大"]
      ].map(function (m) { return metric(m[0], typeof m[1] === "number" ? fmt(m[1]) : m[1], m[2], ""); }).join("");
      return '<div class="mw-metrics" style="grid-template-columns:repeat(4,1fr)">' + items + '</div>';
    }

    function analysisHTML(song) {
      var learningsFor = D.learnings.filter(function (l) { return l.fromSong === song.id; });
      var obs = "《" + song.name + "》在汽水音乐上线后，完播率与收藏显著高于我们其他歌，尤其副歌前置留白 Hook 的留存更好。";
      var ev = "Plays " + fmt(song.performance.plays) + " · Completion " + (song.performance.completion * 100).toFixed(0) + "% · Saves " + fmt(song.performance.saves) + "（数据经 Computer Use 回收，来源 " + esc(song.performance.source) + "）。";
      var analysis = "情绪向（" + esc(song.mood) + "）在都市夜场景有效；" + (song.performance.completion > 0.6 ? "高完播说明结构留白成功" : "完播偏弱，结构需优化") + "；" + (song.performance.saves > 50000 ? "高收藏说明主题有复用价值" : "收藏偏弱");
      var learn = learningsFor.length ? learningsFor.map(function (l) { return "<li><b>" + esc(l.type) + "（" + esc(l.confidence) + "）：</b>" + esc(l.text) + " <span class='mw-helper'>证据：" + esc(l.evidence) + "；应用：" + esc(l.apply) + "</span></li>"; }).join("") : "<li>暂无专项 Learning。</li>";
      var rec = "下一首继续用「前置留白 Hook」；优先 80–100 BPM 都市情绪向；制作 Brief 强制切片 Hook + 至少一层床音。";
      return '<div class="mw-section"><div class="mw-section-title">分析与学习</div>' +
        '<div class="mw-grid" style="grid-template-columns:1fr 1fr">' +
          '<div class="mw-card"><div class="mw-eyebrow">Observation 观察</div><div style="font-size:var(--ui-fs-2);line-height:1.6">' + obs + '</div>' +
            '<div class="mw-eyebrow" style="margin-top:var(--ui-sp-2)">Evidence 证据</div><div class="mw-helper">' + ev + '</div></div>' +
          '<div class="mw-card"><div class="mw-eyebrow">Analysis 分析</div><div style="font-size:var(--ui-fs-2);line-height:1.6">' + analysis + '</div>' +
            '<div class="mw-eyebrow" style="margin-top:var(--ui-sp-2)">Recommendation 建议</div><div class="mw-helper">' + rec + '</div></div>' +
        '</div>' +
        '<div class="mw-card" style="margin-top:var(--ui-sp-3)"><div class="mw-eyebrow">Learning 沉淀</div><ul style="margin:var(--ui-sp-2) 0;padding-left:var(--ui-sp-4);color:var(--ui-text-2);font-size:var(--ui-fs-2);line-height:1.6">' + learn + '</ul>' +
          '<div class="mw-btn-row" style="margin-top:var(--ui-sp-2)"><button class="mw-btn primary" data-next-song="' + song.id + '">形成下一首方向 →</button></div></div>' +
        '</div>';
    }

    var main = "";
    if (!song) {
      main = '<div class="mw-empty">暂无已发布 Song。发布并回收数据后在此复盘。</div>';
    } else {
      var p = song.performance || seedPerf();
      main =
        '<div class="mw-page-head"><h1 class="mw-page-title">数据与复盘</h1>' +
        '<p class="mw-page-sub">四模式回收（API_SYNC / COMPUTER_USE / IMPORT / MANUAL_ENTRY）→ 分析 → Learning → 流入下一首。</p></div>' +
        '<div style="display:grid;grid-template-columns:120px 1fr;gap:var(--ui-sp-4);align-items:start;margin-bottom:var(--ui-sp-4)">' +
          cover(song.cover, "c120", song.name.slice(0, 1)) +
          '<div><div class="mw-page-title" style="font-size:var(--ui-fs-5)">' + esc(song.name) + '</div>' +
          '<div class="mw-helper">' + esc(song.style) + ' · ' + esc(song.mood) + ' · ' + esc(song.release ? song.release.platform : song.targetPlatform) + (song.release ? ' · ' + esc(song.release.date) : '') + '</div>' +
          '<div class="mw-helper" style="margin-top:4px">数据来源：' + esc(p.source) + ' · ' + esc(p.fresh) + '</div></div></div>' +
        (p.plays > 0 ? metricsHTML(p) : '<div class="mw-callout">该 Song 数据仍在观察期（发布后 7–14 天）待 Computer Use 采集；最小指标集：Plays/Completion/Saves/Shares/Likes。</div>') +
        (p.plays > 0 ? analysisHTML(song) : '');
    }

    root.innerHTML = main;

    $all(root, "[data-next-song]").forEach(function (b) { b.addEventListener("click", function () { MU.makeNextSong(b.getAttribute("data-next-song")); }); });

    /* 右侧专业导航 */
    var pubHTML = published.map(function (s) {
      return '<a class="mw-util-nav-item' + (s.id === S.selectedSong ? " active" : "") + '" data-rsong="' + s.id + '"><span>' + esc(s.name) + '</span><span class="u-count">' + (s.performance && s.performance.plays > 0 ? fmt(s.performance.plays) + " 播" : "待采") + '</span></a>';
    }).join("") || '<div class="mw-helper">暂无</div>';
    util.innerHTML = '<p class="mw-util-title">数据 · 专业导航</p>' +
      '<div class="mw-util-card"><h4>已发布 Song</h4><div class="mw-util-nav">' + pubHTML + '</div></div>' +
      '<div class="mw-util-card"><h4>四模式 Result Intake</h4>' +
        utilRow("API_SYNC", "Apple/YT（未来）") + utilRow("COMPUTER_USE", "汽水后台读（主路径）") +
        utilRow("IMPORT", "平台导出") + utilRow("MANUAL_ENTRY", "人工录入兜底") + '</div>' +
      '<div class="mw-util-card"><h4>最小指标集</h4><p class="mw-helper">Plays / Completion / Saves / Shares / Likes 必录；Comments/Follower/Revenue 按需。</p></div>' +
      '<div class="mw-util-card"><h4>分析 Employee</h4><div class="mw-helper">' + esc(e.name) + ' · ' + esc(e.now) + '</div></div>';
    $all(util, "[data-rsong]").forEach(function (b) { b.addEventListener("click", function () { S.selectedSong = b.getAttribute("data-rsong"); S.selectedSongName = D.getSong(S.selectedSong).name; renderSafe(); }); });
  };

  MU.makeNextSong = function (songId) {
    var s = D.getSong(songId); if (!s) return;
    var dir = {
      id: "dir-" + Date.now(), name: s.name + "Ⅱ（方向）", fromRefs: [], status: "in_research",
      audience: "24–32 都市夜猫", constraint: "基于《" + s.name + "》Learning：强化前置留白 Hook，沿用母题。",
      basis: "来自《" + s.name + "》市场反馈的 Learning 沉淀。", employee: "e2", approved: false, createdAt: "今天", fresh: true, fromLearning: true
    };
    D.directions.unshift(dir);
    S.area = "research"; S.sub = "directions"; S.selectedRef = null; S.selectedSong = null;
    MU.render();
  };

  /* 通用对话 Composer 绑定（研究/制作） */
  // 重新定义 bindComposer：返回空（HTML 中已含），真正绑定放在各页末尾
  // 这里提供统一绑定入口
  function bindConv(root) {
    $all(root, "[data-send]").forEach(function (btn) {
      var convId = btn.getAttribute("data-send");
      var ta = btn.parentElement.querySelector("textarea");
      btn.addEventListener("click", function () {
        var txt = ta ? ta.value.trim() : "";
        if (!txt) return;
        var conv = document.getElementById(convId);
        if (!conv) return;
        conv.innerHTML += convMsg("user", "你", txt);
        var reply = "收到，我记下了。";
        // 简单按上下文给回复
        if (/改|返工|重|调/.test(txt)) reply = "明白，我会据你的意见调整 Brief 并重新发起版本。";
        else if (/火|为什么|热门|趋势/.test(txt)) reply = "这首火在三件事：① groove 对味；② 慢板都市夜情绪契合推荐池；③ 副歌切片在短视频传播强。";
        else if (/方向|下一首|学/.test(txt)) reply = "我已把上首 Learning 落到新方向卡，建议你批准进入制作验证。";
        conv.innerHTML += convMsg("emp", convId.indexOf("prod") >= 0 ? "陈默" : "苏晚", reply);
        if (ta) ta.value = "";
      });
    });
  }
  // 在渲染后统一绑定对话
  var _origRender = MU.render;
  MU.render = function () {
    _origRender();
    var root = document.getElementById("view-root");
    if (root) bindConv(root);
  };
})();
