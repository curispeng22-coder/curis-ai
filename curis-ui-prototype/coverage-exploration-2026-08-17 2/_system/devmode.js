/* ============================================================
   Curis Dev Mode — 为 Frozen 交付提供开发可读标注层
   ------------------------------------------------------------
   使用方式：
     · 在 URL 后加 ?dev=1
     · 页面内按 Shift + D 开启 / Shift + Esc 关闭
     · 鼠标悬停任意元素，显示：尺寸、间距、字号档位、颜色令牌、
       圆角令牌、data-spec 组件规格
   标注层 z-index = var(--ui-z-devmode)（9000），永远在其他 UI 之上。
   ============================================================ */
(function () {
  'use strict';

  // 避免重复初始化
  if (window.__curisDevMode) return;
  window.__curisDevMode = true;

  var enabled = location.search.indexOf('dev=1') !== -1;
  var root = document.documentElement;
  var sheetUrl = new URL('_system/tokens.css', location.href).href;
  var tokenMap = null;   // color/space/radius/font -> tokenName
  var els = {};

  /* ---------- 令牌解析：从 tokens.css 建立反向索引 ---------- */
  function parseTokens(css) {
    var map = { color: {}, space: {}, radius: {}, font: {} };
    var re = /(--ui-([a-z0-9-]+)):\s*([^;]+);/g;
    var m;
    while ((m = re.exec(css))) {
      var full = m[1], name = m[2], raw = m[3].trim();
      var val = raw;
      // 跳过 var() 引用，只记录最终字面量
      if (/^var\(/.test(val)) continue;

      // 颜色
      if (/^#([0-9a-fA-F]{3,8})|^rgba?\(|^hsla?\(/.test(val)) {
        var key = normalizeColor(val);
        if (key && !map.color[key]) map.color[key] = full;
      }
      // 字号
      else if (name.indexOf('fs-') === 0) {
        var fpx = px(val);
        if (fpx) map.font[fpx] = full;
      }
      // 圆角
      else if (name.indexOf('r-') === 0 || name === 'radius' || name === 'radius-sm') {
        var rpx = px(val);
        if (rpx) map.radius[rpx] = full;
      }
      // 间距
      else if (name.indexOf('sp-') === 0) {
        var spx = px(val);
        if (spx) map.space[spx] = full;
      }
    }
    return map;
  }

  function normalizeColor(v) {
    // 把任意颜色表达归一化为 rgb(r,g,b)，用于反查最接近的令牌
    v = v.replace(/\s+/g, '').toLowerCase();
    var r, g, b;
    if (v.startsWith('rgba(') || v.startsWith('rgb(')) {
      var nums = v.match(/\d+(\.\d+)?/g);
      if (!nums || nums.length < 3) return null;
      r = +nums[0]; g = +nums[1]; b = +nums[2];
    } else if (v.startsWith('#')) {
      var hex = v.slice(1);
      if (hex.length === 3) hex = hex.split('').map(function (c) { return c + c; }).join('');
      if (hex.length !== 6 && hex.length !== 8) return null;
      r = parseInt(hex.slice(0, 2), 16);
      g = parseInt(hex.slice(2, 4), 16);
      b = parseInt(hex.slice(4, 6), 16);
    } else {
      return v;
    }
    return 'rgb(' + r + ',' + g + ',' + b + ')';
  }

  function px(v) {
    var n = parseFloat(v);
    return isNaN(n) ? null : Math.round(n);
  }

  function nearestToken(map, value, round) {
    if (!value) return '—';
    var n = typeof value === 'number' ? value : px(value);
    if (!n) return '—';
    if (map[n]) return map[n];
    var keys = Object.keys(map).map(Number).filter(Boolean);
    if (!keys.length) return n + 'px';
    var closest = keys.reduce(function (a, b) { return Math.abs(b - n) < Math.abs(a - n) ? b : a; }, keys[0]);
    // 圆角/字号必须精确匹配；颜色允许小误差
    if (round && Math.abs(closest - n) > 0.5) return n + 'px';
    return map[closest] + ' ≈' + n + 'px';
  }

  function nearestColorToken(map, rgbStr) {
    // rgb(r,g,b) 字符串
    var nums = rgbStr.match(/\d+(\.\d+)?/g);
    if (!nums || nums.length < 3) return null;
    var target = [+nums[0], +nums[1], +nums[2]];
    var best = null, bestDist = Infinity;
    Object.keys(map).forEach(function (k) {
      var kn = k.match(/\d+(\.\d+)?/g);
      if (!kn || kn.length < 3) return;
      var d = Math.sqrt(
        Math.pow(target[0] - kn[0], 2) +
        Math.pow(target[1] - kn[1], 2) +
        Math.pow(target[2] - kn[2], 2)
      );
      if (d < bestDist) { bestDist = d; best = map[k]; }
    });
    return best;
  }

  /* ---------- DOM：标注层元素 ---------- */
  function buildDOM() {
    els.wrap = document.createElement('div');
    els.wrap.id = 'curisDevMode';
    els.wrap.className = 'curis-devmode';
    els.wrap.hidden = true;
    els.wrap.setAttribute('aria-hidden', 'true');

    els.highlight = document.createElement('div');
    els.highlight.className = 'curis-devmode__highlight';

    els.tooltip = document.createElement('div');
    els.tooltip.className = 'curis-devmode__tooltip';

    els.wrap.appendChild(els.highlight);
    els.wrap.appendChild(els.tooltip);
    document.body.appendChild(els.wrap);
  }

  function injectStyles() {
    if (document.getElementById('curisDevModeStyle')) return;
    var style = document.createElement('style');
    style.id = 'curisDevModeStyle';
    style.textContent = [
      '.curis-devmode { position: fixed; inset: 0; pointer-events: none; z-index: var(--ui-z-devmode, 9000); }',
      '.curis-devmode[hidden] { display: none !important; }',
      '.curis-devmode__highlight { position: absolute; border: 1px dashed var(--ui-accent, #32f08c); background: color-mix(in srgb, var(--ui-accent, #32f08c) 8%, transparent); box-shadow: 0 0 0 1px rgba(0,0,0,0.3); border-radius: var(--ui-r-xs, 4px); transition: top 40ms, left 40ms, width 40ms, height 40ms; }',
      '.curis-devmode__tooltip { position: absolute; min-width: 220px; max-width: 360px; padding: var(--ui-sp-3, 12px); background: var(--ui-surface-2, #2b2f34); border: 1px solid var(--ui-line, #343940); border-radius: var(--ui-r-sm, 8px); color: var(--ui-text, #f3f4f6); font-size: var(--ui-fs-1, 12px); line-height: 1.45; box-shadow: var(--ui-shadow-3, 0 12px 32px rgba(0,0,0,0.44)); pointer-events: none; }',
      '.curis-devmode__tooltip code { font-family: var(--ui-mono, monospace); font-size: var(--ui-fs-1, 12px); padding: 1px var(--ui-sp-1); border-radius: var(--ui-r-xs, 4px); background: var(--ui-surface, #222529); color: var(--ui-accent, #32f08c); }',
      '.curis-devmode__tooltip .row { display: flex; justify-content: space-between; gap: var(--ui-sp-3); margin: 2px 0; }',
      '.curis-devmode__tooltip .row span:first-child { color: var(--ui-text-2, #a7adb6); }',
      '.curis-devmode__tooltip .row span:last-child { text-align: right; }',
      '.curis-devmode__tooltip .spec { margin-top: 8px; padding-top: 8px; border-top: 1px solid var(--ui-line, #343940); }',
      '.curis-devmode__tooltip .spec-title { color: var(--ui-accent, #32f08c); margin-bottom: 4px; }',
      '.curis-devmode__tooltip .note { color: var(--ui-text-3, #a3aab4); margin-top: 4px; font-style: italic; }'
    ].join('\n');
    document.head.appendChild(style);
  }

  /* ---------- 核心逻辑 ---------- */
  // class → 组件规格（class-based specs），覆盖无需逐个写 data-spec 的场景
  var CLASS_SPECS = {
    'topbar': { name: 'Global Topbar', size: '100% × 52px', states: 'default|scrolled', tokens: '--ui-topbar-h --ui-surface --ui-line', note: '全局顶栏：左侧面包屑/标题，右侧工具区。固定高度 52px。' },
    'sidebar': { name: 'Global Sidebar', size: '220px × 100vh', states: 'expanded|collapsed（P2）', tokens: '--ui-sidebar-w --ui-surface --ui-line', note: '全局侧栏：品牌、主导航分组、底部设置/帮助。220px 宽。' },
    'nav-item': { name: 'Navigation Item', size: '100% × min 32px', states: 'default|hover|active|focus', tokens: '--ui-sp-2 --ui-r-sm --ui-text-2', note: '主导航项：8px 圆角，左侧图标 + 标签，min-height 32px。' },
    'card': { name: 'Card', size: 'auto × auto', states: 'default|hover', tokens: '--ui-r-md --ui-sp-5 --ui-surface-2 --ui-line', note: '信息卡片：12px 圆角，20px 内边距，用于数据面板与列表。' },
    'btn btn-primary': { name: 'Primary Button', size: 'auto × 40px', states: 'default|hover|active|focus|disabled|loading', tokens: '--ui-ctl-h-lg --ui-r-sm --ui-action-primary-bg', note: '主按钮：绿底白字，用于创建/保存/提交。' },
    'btn btn-secondary': { name: 'Secondary Button', size: 'auto × 36px', states: 'default|hover|active|focus', tokens: '--ui-ctl-h --ui-r-sm --ui-surface-2', note: '次按钮：描边或灰底，用于次要操作。' },
    'btn btn-ghost': { name: 'Ghost Button', size: 'auto × 36px', states: 'default|hover|active|focus', tokens: '--ui-ctl-h --ui-text-2', note: '幽灵按钮：透明背景，用于抽屉内取消/低强调操作。' },
    'drawer': { name: 'Side Drawer', size: '390px × 100vh', states: 'open|closed', tokens: '--ui-r-lg --ui-z-drawer --ui-surface-2', note: '右侧抽屉：390px 宽，z-index 300，带遮罩。' },
    'metric': { name: 'Metric Card', size: 'auto × auto', states: 'default', tokens: '--ui-r-sm --ui-sp-4', note: '指标卡：展示关键数字 + 标签，用于 CEO 工作台与经营页。' }
  };

  function getSpec(el) {
    var raw = el.getAttribute('data-spec');
    if (raw) { try { return JSON.parse(raw); } catch (_) { return { note: raw }; } }
    // 没有 data-spec 时，按 class 命中 CLASS_SPECS
    var cls = (el.className && typeof el.className === 'string') ? el.className.trim() : '';
    if (!cls) return null;
    var classes = cls.split(/\s+/).filter(Boolean);
    for (var i = 0; i < classes.length; i++) {
      for (var key in CLASS_SPECS) {
        var need = key.split(' ');
        var hit = need.every(function (c) { return classes.indexOf(c) !== -1; });
        if (hit) return CLASS_SPECS[key];
      }
      if (CLASS_SPECS[classes[i]]) return CLASS_SPECS[classes[i]];
    }
    return null;
  }

  function describe(el) {
    var cs = getComputedStyle(el);
    var rect = el.getBoundingClientRect();
    var color = nearestColorToken(tokenMap.color, cs.color) || cs.color;
    var bg = cs.backgroundColor === 'rgba(0, 0, 0, 0)' ? 'transparent' : (nearestColorToken(tokenMap.color, cs.backgroundColor) || cs.backgroundColor);
    var br = nearestToken(tokenMap.radius, cs.borderTopLeftRadius, true);
    var fs = nearestToken(tokenMap.font, cs.fontSize, true);

    return {
      tag: el.tagName.toLowerCase(),
      cls: (el.className && typeof el.className === 'string') ? el.className.split(/\s+/).slice(0, 3).join('.') : '',
      w: Math.round(rect.width),
      h: Math.round(rect.height),
      padding: [px(cs.paddingTop), px(cs.paddingRight), px(cs.paddingBottom), px(cs.paddingLeft)],
      margin: [px(cs.marginTop), px(cs.marginRight), px(cs.marginBottom), px(cs.marginLeft)],
      color: color,
      bg: bg,
      br: br,
      fs: fs,
      spec: getSpec(el)
    };
  }

  function renderTooltip(info, x, y) {
    var p = info.padding;
    var m = info.margin;
    var padText = (p[0] === p[2] && p[1] === p[3]) ? (p[0] + ' ' + p[1]) : (p.join(' / '));
    var marText = (m[0] === 0 && m[1] === 0 && m[2] === 0 && m[3] === 0) ? '0' : ((m[0] === m[2] && m[1] === m[3]) ? (m[0] + ' ' + m[1]) : m.join(' / '));

    var html = [
      '<div class="row"><span>类型</span><span><code>' + escapeHtml(info.tag + (info.cls ? '.' + info.cls : '')) + '</code></span></div>',
      '<div class="row"><span>尺寸</span><span>' + info.w + ' × ' + info.h + '</span></div>',
      '<div class="row"><span>字号</span><span><code>' + escapeHtml(info.fs) + '</code></span></div>',
      '<div class="row"><span>圆角</span><span><code>' + escapeHtml(info.br) + '</code></span></div>',
      '<div class="row"><span>文字色</span><span><code>' + escapeHtml(info.color) + '</code></span></div>',
      '<div class="row"><span>背景色</span><span><code>' + escapeHtml(info.bg) + '</code></span></div>',
      '<div class="row"><span>padding</span><span>' + escapeHtml(padText) + '</span></div>',
      '<div class="row"><span>margin</span><span>' + escapeHtml(marText) + '</span></div>'
    ];

    if (info.spec) {
      html.push('<div class="spec">');
      html.push('<div class="spec-title">组件规格</div>');
      if (info.spec.name) html.push('<div class="row"><span>名称</span><span>' + escapeHtml(info.spec.name) + '</span></div>');
      if (info.spec.size) html.push('<div class="row"><span>尺寸</span><span><code>' + escapeHtml(info.spec.size) + '</code></span></div>');
      if (info.spec.states) html.push('<div class="row"><span>状态</span><span>' + escapeHtml(info.spec.states) + '</span></div>');
      if (info.spec.tokens) html.push('<div class="row"><span>令牌</span><span><code>' + escapeHtml(info.spec.tokens) + '</code></span></div>');
      if (info.spec.note) html.push('<div class="note">' + escapeHtml(info.spec.note) + '</div>');
      if (info.spec.interaction) html.push('<div class="note">交互：' + escapeHtml(info.spec.interaction) + '</div>');
      html.push('</div>');
    }

    els.tooltip.innerHTML = html.join('');

    var tw = els.tooltip.offsetWidth;
    var th = els.tooltip.offsetHeight;
    var vw = window.innerWidth;
    var vh = window.innerHeight;
    var left = x + 18;
    var top = y + 18;
    if (left + tw > vw) left = x - tw - 12;
    if (top + th > vh) top = y - th - 12;
    els.tooltip.style.left = Math.max(4, left) + 'px';
    els.tooltip.style.top = Math.max(4, top) + 'px';
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"]/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]; });
  }

  var lastEl = null;
  function onMove(e) {
    if (!enabled) return;
    var el = document.elementFromPoint(e.clientX, e.clientY);
    if (!el || el === document.body || el === document.documentElement) {
      els.highlight.style.display = 'none';
      els.tooltip.style.display = 'none';
      lastEl = null;
      return;
    }
    if (el === lastEl && el !== els.wrap && !els.wrap.contains(el)) return;
    lastEl = el;

    var rect = el.getBoundingClientRect();
    els.highlight.style.display = 'block';
    els.highlight.style.left = rect.left + 'px';
    els.highlight.style.top = rect.top + 'px';
    els.highlight.style.width = rect.width + 'px';
    els.highlight.style.height = rect.height + 'px';

    els.tooltip.style.display = 'block';
    var info = describe(el);
    renderTooltip(info, e.clientX, e.clientY);
  }

  /* ---------- 生命周期 ---------- */
  function setEnabled(v) {
    enabled = v;
    if (enabled) {
      els.wrap.hidden = false;
      if (!tokenMap) loadTokens();
    } else {
      els.wrap.hidden = true;
      lastEl = null;
    }
  }

  function loadTokens() {
    fetch(sheetUrl)
      .then(function (r) { return r.text(); })
      .then(function (css) { tokenMap = parseTokens(css); })
      .catch(function () {
        // 兜底：用内置映射，确保即使离线也能工作
        tokenMap = {
          color: {}, space: {}, radius: {}, font: {}
        };
      });
  }

  function init() {
    injectStyles();
    buildDOM();
    document.addEventListener('mousemove', throttle(onMove, 40));
    document.addEventListener('keydown', function (e) {
      if (e.shiftKey && e.key === 'D') { e.preventDefault(); setEnabled(!enabled); }
      if (e.shiftKey && e.key === 'Escape') { e.preventDefault(); setEnabled(false); }
    });
    if (enabled) {
      els.wrap.hidden = false;
      loadTokens();
    }
  }

  function throttle(fn, wait) {
    var last = 0, timer = null;
    return function (e) {
      var now = Date.now();
      if (now - last >= wait) { last = now; fn(e); }
      else {
        clearTimeout(timer);
        timer = setTimeout(function () { last = Date.now(); fn(e); }, wait);
      }
    };
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
