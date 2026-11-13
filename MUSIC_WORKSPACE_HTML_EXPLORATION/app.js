/* ============================================================
   app.js — Curis · AI 音乐经营 工作区（视觉探索）
   核心命名空间 MU：状态、外壳渲染、七区导航、主题、路由、共享工具。
   页面渲染与交互在 pages.js（MU.pages.*）。
   ============================================================ */
window.MU = window.MU || {};
(function () {
  "use strict";

  /* ── 全局七区导航（verbatim，Frozen 语言） ─────────────────────────── */
  var ZONES = [
    { id: "ceo",        name: "CEO 工作台", ico: "◆" },
    { id: "biz",        name: "业务空间",   ico: "◇", active: true }, /* 音乐工作区所在 */
    { id: "org",        name: "组织中心",   ico: "□" },
    { id: "talent",     name: "人才与能力", ico: "⌘" },
    { id: "insight",    name: "经营洞察",   ico: "◎" },
    { id: "library",    name: "资料库",     ico: "▤" },
    { id: "meeting",    name: "会议",       ico: "◌" }
  ];

  var STORAGE_KEY = "curis-music-theme";

  var state = {
    area: "operating",     // 当前 Work Area
    zone: "biz",           // 当前七区
    selectedSong: null,    // 制作区/数据区选中的 Song
    selectedRef: null,     // 研究区选中的 Reference
    compare: { a: null, b: null }, // 版本 A/B 比较选择
    playing: false,
    playTimer: null,
    playProgress: 0
  };
  MU.state = state;

  /* ── 共享工具 ──────────────────────────────────────────────────────── */
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
  MU.esc = esc;

  function fmt(n) {
    if (n == null) return "—";
    return Number(n).toLocaleString("en-US");
  }
  MU.fmt = fmt;

  /* ── 轻量提示（替代浏览器原生 alert：原生对话框会阻塞页面且不符合
        高保真原型的成熟度要求） ─────────────────────────────────────── */
  var _toastHost = null;
  function toast(msg, kind) {
    if (!_toastHost) {
      _toastHost = document.createElement("div");
      _toastHost.className = "mw-toasts";
      document.body.appendChild(_toastHost);
    }
    var el = document.createElement("div");
    el.className = "mw-toast" + (kind ? " " + kind : "");
    el.textContent = msg;
    _toastHost.appendChild(el);
    setTimeout(function () { el.classList.add("leaving"); }, 2200);
    setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 2700);
  }
  MU.toast = toast;

  function hashHue(str) {
    var h = 0;
    for (var i = 0; i < String(str).length; i++) h = (h * 31 + str.charCodeAt(i)) % 360;
    return h;
  }

  // 确定性伪随机（用于封面波形）
  function seeded(seed) {
    var s = 0;
    for (var i = 0; i < String(seed).length; i++) s = (s * 131 + str_char(seed, i)) % 9973;
    return function () { s = (s * 1103515245 + 12345) % 2147483648; return (s % 1000) / 1000; };
  }
  function str_char(s, i) { return s.charCodeAt(i) || 7; }

  // 封面：CSS 渐变 + inline SVG 抽象波形/同心（无远程资源）
  MU.coverHTML = function (seed, sizeClass, label) {
    var hue = hashHue(seed);
    var c1 = "hsl(" + hue + " 60% 46%)";
    var c2 = "hsl(" + ((hue + 40) % 360) + " 55% 26%)";
    var rnd = seeded(seed);
    var bars = "";
    for (var i = 0; i < 11; i++) {
      var hgt = 12 + Math.round(rnd() * 60);
      var x = 8 + i * 8;
      bars += '<rect x="' + x + '" y="' + (50 - hgt / 2) + '" width="4" height="' + hgt +
              '" rx="2" fill="rgba(255,255,255,0.30)"/>';
    }
    var svg = '<svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">' + bars + '</svg>';
    var txt = esc(label || String(seed).slice(0, 2));
    return '<div class="mw-cover ' + sizeClass + '" style="background:linear-gradient(135deg,' + c1 + ',' + c2 + ')">' +
           svg + '<span class="cov-seed">' + txt + '</span></div>';
  };

  // 状态 → 显示文案 + 样式类
  var SONG_STATUS = {
    research:  { label: "研究中", cls: "neutral" },
    proposal:  { label: "提案待审", cls: "warning" },
    production:{ label: "制作中", cls: "attention" },
    ready:     { label: "待发布", cls: "warning" },
    published: { label: "已发布", cls: "published" }
  };
  MU.songStatus = function (s) { return SONG_STATUS[s.status] || { label: s.status, cls: "neutral" }; };

  var PUB_STATE = {
    ready:      { label: "Ready", cls: "ready" },
    publishing: { label: "Publishing", cls: "attention" },
    auth_stop:  { label: "Waiting for User", cls: "blocked" },
    pending:    { label: "Pending Review", cls: "review" },
    published:  { label: "Published", cls: "published" },
    rejected:   { label: "Rejected", cls: "rejected" }
  };
  MU.pubState = function (st) { return PUB_STATE[st] || { label: st, cls: "neutral" }; };

  MU.areaName = function (id) {
    var a = MU.data.areas.filter(function (x) { return x.id === id; })[0];
    return a ? a.name : id;
  };

  /* ── 主题切换（dark 默认） ─────────────────────────────────────────── */
  function applyTheme(t) {
    if (t !== "light" && t !== "dark") t = "dark";
    document.documentElement.setAttribute("data-theme", t);
    var btns = document.querySelectorAll("[data-theme-btn]");
    for (var i = 0; i < btns.length; i++) {
      var b = btns[i];
      b.classList.toggle("active", b.getAttribute("data-theme-btn") === t);
    }
  }
  MU.toggleTheme = function (t) {
    try { localStorage.setItem(STORAGE_KEY, t); } catch (e) {}
    applyTheme(t);
  };
  function initTheme() {
    var t = "dark";
    try { var s = localStorage.getItem(STORAGE_KEY); if (s === "light" || s === "dark") t = s; } catch (e) {}
    applyTheme(t);
    var host = document.getElementById("theme-switch");
    if (host) {
      [["dark", "深色"], ["light", "浅色"]].forEach(function (p) {
        var b = document.createElement("button");
        b.className = "mw-theme-btn";
        b.setAttribute("data-theme-btn", p[0]);
        b.textContent = p[1];
        b.addEventListener("click", function () { MU.toggleTheme(p[0]); });
        host.appendChild(b);
      });
    }
  }

  /* ── 左导航：七区 + 音乐工作区局部专业导航 ─────────────────────────── */
  function renderSidebar() {
    var zoneNav = document.getElementById("zone-nav");
    var areaNav = document.getElementById("area-nav");
    var foot = document.getElementById("side-foot");
    if (!zoneNav) return;

    // 七区全局导航
    zoneNav.innerHTML = '<p class="mw-nav-label">全局</p>';
    ZONES.forEach(function (z) {
      var a = document.createElement("a");
      a.className = "mw-zone-item" + (z.id === state.zone ? " active" : "");
      a.href = "#";
      a.setAttribute("data-zone", z.id);
      a.innerHTML = '<span class="z-ico">' + z.ico + '</span><span>' + z.name + '</span>';
      a.addEventListener("click", function (e) {
        e.preventDefault();
        state.zone = z.id;
        if (z.id === "biz") { state.area = "operating"; renderSidebar(); render(); }
        else { renderSidebar(); renderZonePlaceholder(z.name); }
      });
      zoneNav.appendChild(a);
    });

    // 音乐工作区局部专业导航（按 Work Area 实需命名，非「上下文」）
    areaNav.innerHTML = '<p class="mw-nav-label">AI 音乐经营 · 工作区</p>';
    MU.data.areas.forEach(function (area) {
      var a = document.createElement("a");
      a.className = "mw-area-item" + (area.id === state.area ? " active" : "");
      a.href = "#";
      a.setAttribute("data-area", area.id);
      var count = areaCount(area.id);
      a.innerHTML = '<span class="a-ico">' + area.icon + '</span><span>' + area.name +
        '</span>' + (count != null ? '<span class="a-count">' + count + '</span>' : '');
      a.addEventListener("click", function (e) {
        e.preventDefault();
        state.zone = "biz";
        setArea(area.id);
      });
      areaNav.appendChild(a);
    });

    if (foot) {
      foot.innerHTML = '事实先于观点。<br/>共识必须回到责任与结果。';
    }
  }

  // 局部导航上的计数（真实反映状态）
  function areaCount(areaId) {
    var d = MU.data;
    if (areaId === "production") return d.songs.filter(function (s) { return s.status === "production"; }).length;
    if (areaId === "publish") {
      return d.songs.filter(function (s) {
        return s.status === "ready" || (s.release && ["ready", "publishing", "auth_stop", "pending"].indexOf(s.release.state) >= 0);
      }).length;
    }
    if (areaId === "research") return d.references.length;
    if (areaId === "review") return d.songs.filter(function (s) { return s.status === "published"; }).length;
    if (areaId === "operating") return d.ceoDecisions.filter(function (c) { return c.status === "open"; }).length;
    return null;
  }
  MU.areaCount = areaCount;

  /* ── 顶栏：面包屑 + Needs CEO 徽标 ───────────────────────────────── */
  function renderTopbar() {
    var crumb = document.getElementById("breadcrumb");
    var badge = document.getElementById("needs-ceo-badge");
    if (crumb) {
      var sub = state.selectedSong && state.area === "production" ? " · " + esc(state.selectedSongName || "")
              : state.selectedRef && state.area === "research" ? " · " + esc(state.selectedRefTitle || "")
              : "";
      crumb.innerHTML = '<span>Curis</span><span>/</span><span>业务空间</span><span>/</span>' +
        '<b>AI 音乐经营</b><span>/</span><b>' + esc(MU.areaName(state.area)) + '</b>' + sub;
    }
    if (badge) {
      var open = MU.data.ceoDecisions.filter(function (c) { return c.status === "open"; }).length;
      // 发布区 Auth Stop Gate 也计为需要用户处理
      var waiting = MU.data.songs.filter(function (s) { return s.release && s.release.state === "auth_stop"; }).length;
      var total = open + waiting;
      if (total > 0) { badge.classList.add("show"); badge.textContent = "待处理：" + total; }
      else { badge.classList.remove("show"); }
    }
  }

  /* ── 路由：切换 Work Area ─────────────────────────────────────────── */
  function setArea(id) {
    state.area = id;
    state.selectedSong = null; state.selectedRef = null;
    state.compare = { a: null, b: null };
    renderSidebar(); render();
  }
  MU.setArea = setArea;

  function renderZonePlaceholder(zoneName) {
    var root = document.getElementById("view-root");
    var util = document.getElementById("utility-root");
    if (root) {
      root.innerHTML =
        '<div class="mw-page-head"><h1 class="mw-page-title">' + esc(zoneName) + '</h1>' +
        '<p class="mw-page-sub">本视觉探索聚焦于「AI 音乐经营」工作区；其他七区为 Curis 全局导航占位，不在本次探索范围。</p></div>' +
        '<div class="mw-empty">（该区为占位 · 当前仅 AI 音乐经营工作区可交互）</div>';
    }
    if (util) util.innerHTML = '<p class="mw-util-title">专业导航</p><div class="mw-util-card"><h4>说明</h4><p class="mw-helper">进入「业务空间 → AI 音乐经营」查看五区闭环。</p></div>';
    renderTopbar();
  }

  /* ── 主渲染 ──────────────────────────────────────────────────────── */
  function render() {
    renderTopbar();
    var root = document.getElementById("view-root");
    var util = document.getElementById("utility-root");
    if (!root) return;
    root.scrollTop = 0;

    var area = state.area;
    if (!MU.pages || !MU.pages[area]) {
      renderZonePlaceholder(MU.areaName(area));
      return;
    }
    MU.pages[area](root, util); // 页面自行渲染 Main + 右侧专业导航 + 绑定事件
  }
  MU.render = render;

  /* ── 启动 ────────────────────────────────────────────────────────── */
  MU.init = function () {
    initTheme();
    renderSidebar();
    render();
  };
})();
