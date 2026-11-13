/*
 * Curis Runtime Capability Switcher — 运行现场「当前能力」切换器（全站唯一实现）
 * ---------------------------------------------------------------------------
 * 规范来源：Curis_Product_Blueprint.html §14 UI 蓝图 / §16 v1 单机本地自用范围
 *   能力闭环三段：AI 团队页「添加 + 绑定」→ 运行现场「切换」→ 执行时生效。
 *   本模块只负责第三段的「切换」入口，数据真源在 AI 团队页写入的 localStorage。
 *
 * 数据契约（与 ai-organization.html 严格一致，改一处必须同步改另一处）：
 *   localStorage['curis-capabilities']
 *     → [{ id, name, type, effect, resource }]
 *   localStorage['curis-capability-binds']
 *     → { [capabilityId]: [employeeKey, ...] }
 *   localStorage['curis-runtime-cap:<page>']
 *     → 本页最近一次选中的 capabilityId（按页记忆，互不干扰）
 *
 * 设计约束：
 *   1. 零依赖、幂等（dataset.curisCapBound 保证只绑定一次监听）。
 *   2. 不使用 innerHTML 注入用户输入 —— option 一律走 document.createElement +
 *      textContent，从结构上杜绝 XSS，无需手写转义。
 *   3. 空态不留死控件：没有任何已配置能力时，把 select 隐藏并换成
 *      「＋ 配置能力」链接直达 AI 团队页，保证操作路径永远闭环。
 *   4. 跨标签页同步：监听 storage 事件，在 AI 团队页新增能力后，
 *      已打开的运行现场无需刷新即可看到新能力。
 *   5. 全部视觉走冻结令牌 --ui-*，不引入任何私有色值。
 *
 * 无障碍：select 自带原生键盘操作与语义；选中变化通过 aria-live 区域播报，
 *         链接与控件均满足 WCAG AA 的可聚焦与可辨识焦点要求。
 */
(function () {
  'use strict';

  var CAP_STORE = 'curis-capabilities';
  var BIND_STORE = 'curis-capability-binds';
  var TEAM_PAGE = 'ai-organization.html';

  var EFFECT_SHORT = { '只读': '只读', '检索': '检索', '写入': '写入', '执行': '执行' };
  /* 与 ai-organization.html 的 CAP_TYPE_LABEL 保持一致：存英文标识、显中文 */
  var TYPE_LABEL = { '模型': '模型', 'Agent': 'AI 员工', 'Skill': '技能', 'Tool': '工具', 'MCP': '连接器' };

  function pageKey() {
    var p = (location.pathname.split('/').pop() || 'index').replace(/\.html$/, '');
    return 'curis-runtime-cap:' + p;
  }

  function readJSON(key, fallback) {
    try {
      var v = JSON.parse(localStorage.getItem(key));
      return v == null ? fallback : v;
    } catch (e) {
      return fallback;
    }
  }

  function loadCaps() {
    var list = readJSON(CAP_STORE, []);
    return Object.prototype.toString.call(list) === '[object Array]' ? list : [];
  }

  function boundCount(capId) {
    var binds = readJSON(BIND_STORE, {});
    var arr = binds && binds[capId];
    return arr && arr.length ? arr.length : 0;
  }

  /* 空态链接的样式只注入一次（cssText 写不了 :hover / :focus-visible） */
  function ensureStyle() {
    if (document.getElementById('curisCapEmptyStyle')) return;
    var s = document.createElement('style');
    s.id = 'curisCapEmptyStyle';
    s.textContent =
      '.cap-empty-link{font-size:var(--ui-fs-1);color:var(--ui-text-2);' +
      'text-decoration:none;border:1px dashed var(--ui-line);border-radius:var(--ui-radius-sm);' +
      'padding:var(--ui-sp-1) var(--ui-sp-2);line-height:1.2;white-space:nowrap;' +
      'transition:color .15s ease,border-color .15s ease;}' +
      '.cap-empty-link:hover{color:var(--ui-accent);border-color:var(--ui-accent);}' +
      '.cap-empty-link:focus-visible{outline:2px solid var(--ui-accent);outline-offset:2px;}';
    document.head.appendChild(s);
  }

  /* 空态：把死下拉换成一条通往 AI 团队页的实链接，操作路径不断头 */
  function renderEmpty(label, select) {
    if (!select) return;
    ensureStyle();
    select.hidden = true;
    var wrap = select.parentNode;
    if (!wrap) return;
    var link = wrap.querySelector('[data-cap-empty-link]');
    if (!link) {
      link = document.createElement('a');
      link.setAttribute('data-cap-empty-link', '');
      /* data-cta：语义等同按钮，吃 tokens.css 的 32px 触达下限 */
      link.setAttribute('data-cta', '');
      link.setAttribute('data-spec', JSON.stringify({
        name: 'Capability Empty CTA',
        size: 'auto × 32px',
        states: 'default|hover|focus',
        tokens: '--ui-ctl-h-sm --ui-r-sm --ui-accent',
        note: '无已配置能力时显示，跳转到 AI 团队页继续操作，避免死胡同。'
      }));
      link.className = 'cap-empty-link';
      link.href = TEAM_PAGE;
      link.textContent = '＋ 配置能力';
      link.title = '前往 AI 团队页添加模型 / AI 员工 / 技能 / 工具 / 连接器';
      wrap.appendChild(link);
    }
    link.hidden = false;
    if (label) label.textContent = '当前能力';
  }

  function clearEmpty(select) {
    if (!select || !select.parentNode) return;
    var link = select.parentNode.querySelector('[data-cap-empty-link]');
    if (link) link.hidden = true;
    select.hidden = false;
  }

  function announce(text) {
    var live = document.getElementById('runtimeCapLive');
    if (!live) {
      live = document.createElement('span');
      live.id = 'runtimeCapLive';
      live.setAttribute('aria-live', 'polite');
      live.style.cssText =
        'position:absolute;width:1px;height:1px;overflow:hidden;' +
        'clip:rect(0 0 0 0);white-space:nowrap;';
      document.body.appendChild(live);
    }
    live.textContent = text;
  }

  function render() {
    var select = document.getElementById('runtimeCapSelect');
    if (!select) return;
    var label = select.parentNode ? select.parentNode.querySelector('span') : null;

    var caps = loadCaps();
    if (!caps.length) {
      select.innerHTML = '';
      renderEmpty(label, select);
      return;
    }
    clearEmpty(select);

    var remembered = null;
    try { remembered = localStorage.getItem(pageKey()); } catch (e) { remembered = null; }

    /* 按类型分组，降低长列表的选择成本 */
    var order = [];
    var groups = {};
    caps.forEach(function (c) {
      if (!c || !c.id) return;
      var t = c.type || '其他';
      if (!groups[t]) { groups[t] = []; order.push(t); }
      groups[t].push(c);
    });

    select.innerHTML = '';
    var hint = document.createElement('option');
    hint.value = '';
    hint.textContent = '未选择';
    select.appendChild(hint);

    var matched = false;
    order.forEach(function (t) {
      var og = document.createElement('optgroup');
      og.label = TYPE_LABEL[t] || t;
      groups[t].forEach(function (c) {
        var o = document.createElement('option');
        o.value = c.id;
        var eff = EFFECT_SHORT[c.effect] || c.effect || '';
        var n = boundCount(c.id);
        /* textContent 赋值 —— 用户输入不参与 HTML 解析 */
        o.textContent = c.name + (eff ? '（' + eff + '）' : '') + (n ? ' · 已绑定 ' + n + ' 人' : '');
        if (remembered && remembered === c.id) { o.selected = true; matched = true; }
        og.appendChild(o);
      });
      select.appendChild(og);
    });
    if (!matched) select.value = '';
  }

  function bind() {
    var select = document.getElementById('runtimeCapSelect');
    if (!select || select.dataset.curisCapBound === '1') return;
    select.dataset.curisCapBound = '1';
    select.addEventListener('change', function () {
      try {
        if (select.value) localStorage.setItem(pageKey(), select.value);
        else localStorage.removeItem(pageKey());
      } catch (e) { /* 隐私模式下静默降级，不阻断交互 */ }
      var txt = select.options[select.selectedIndex]
        ? select.options[select.selectedIndex].textContent
        : '未选择';
      announce('当前能力已切换为 ' + txt);
    });
  }

  function init() {
    render();
    bind();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  /* AI 团队页新增 / 删除 / 绑定能力后，已打开的运行现场自动跟随 */
  window.addEventListener('storage', function (e) {
    if (e.key === CAP_STORE || e.key === BIND_STORE) render();
  });

  /* 同标签页内手动刷新入口（供未来页面内添加能力时调用） */
  window.curisRefreshRuntimeCapabilities = render;
})();
