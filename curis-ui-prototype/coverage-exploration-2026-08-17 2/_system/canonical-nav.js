/*
 * Curis Canonical Sidebar Navigation — 全站唯一导航真源
 * ---------------------------------------------------------------------------
 * 规范来源：docs/03_Design/Curis_Design_System.md §3.1 Navigation hierarchy
 *   公司     ：CEO 工作台、经营、业务、AI 团队、工作空间
 *   经营工具 ：会议工作台、决策室
 *   办公室   ：由已配置的业务空间生成的部门办公室入口（按状态动态生成）
 *   公司资源 ：成果库、知识库、财务、日历
 *   设置与帮助固定在底部
 *
 * 设计约束（P1-3 收敛）：
 *   1. 全站只允许这一个渲染器改写 aside.sidebar 的导航区域。
 *      历史上存在两套竞争渲染器（页面内联 fzn-nav + 静态 markup），
 *      导致同一产品出现 3 种导航签名，已在本次收敛中全部移除。
 *   2. 办公室分组的可见性只由公司运行状态决定，与「当前处在哪一页」无关。
 *      这样在同一状态下，全站任意页面的导航签名完全一致。
 *   3. 本模块零依赖（不依赖 curis-prototype.js），因此
 *      workspace-runtime-* 等未加载原型脚本的页面也能复用同一导航。
 *
 * 幂等：通过 aside.dataset.curisCanonicalNav 保证只渲染一次。
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'curis-prototype-state';

  // ── 冻结导航模型（唯一真源，禁止在页面内联副本）
  var NAV_MODEL = {
    primary: [
      ['CEO 工作台', 'ceo-desk.html', '◆'],
      ['经营', 'operating.html', '◎'],
      ['业务', 'business.html', '◇'],
      ['AI 团队', 'ai-organization.html', '□'],
      ['工作空间', 'workspace-portal.html', '▣']
    ],
    tools: [
      ['会议工作台', 'meeting.html', '◌'],
      ['决策室', 'decision-room.html', '◇'],
      ['任务流水线', 'execution-pipeline.html', '⋕']
    ],
    offices: [
      ['研发办公室', 'workspace-runtime-software.html', '◉'],
      ['小红书运营办公室', 'workspace-runtime-xhs.html', '◌'],
      ['抖音 / TikTok 运营办公室', 'workspace-runtime-shortvideo.html', '◌'],
      ['部门办公室', 'workspace-runtime-department.html', '◉']
    ],
    resources: [
      ['成果库', 'assets.html', '▤'],
      ['知识库', 'knowledge.html', '⌘'],
      ['财务', 'finance.html', '¥'],
      ['日历', 'calendar.html', '◷']
    ],
    footer: [
      ['设置', '#', '○'],
      ['帮助与反馈', '#', '?']
    ]
  };

  // ── 统一图标系统（P2-2 图标整改）：内联 SVG 线性图标，stroke=currentColor，
  //    自动跟随文字色 / 激活态 / 明暗主题，全站风格一致。viewBox 24×24，线宽 1.75。 ──
  function navSvg(paths) {
    return '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" ' +
      'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + paths + '</svg>';
  }
  var ICONS = {
    'ceo-desk.html': navSvg('<path d="M4 8l3.2 3.2L12 5l4.8 6.2L20 8v9a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V8z"/>'),
    'operating.html': navSvg('<path d="M3 12h4l2-6 4 12 2-6h6"/>'),
    'business.html': navSvg('<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>'),
    'ai-organization.html': navSvg('<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/><rect x="9.5" y="9.5" width="5" height="5" rx="1"/>'),
    'workspace-portal.html': navSvg('<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M9 4v16M15 4v16"/>'),
    'meeting.html': navSvg('<rect x="3" y="6" width="12" height="12" rx="2"/><path d="M15 10l6-3v10l-6-3"/>'),
    'decision-room.html': navSvg('<path d="M12 3v18"/><path d="M5 7h14"/><path d="M4 7l4 6H0l4-6z"/><path d="M20 7l-4 6h8l-4-6z"/><path d="M8 21h8"/>'),
    'execution-pipeline.html': navSvg('<path d="M4 7h4l2 4 4-8 2 4h4"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/><path d="M9 17h6"/>'),
    'workspace-runtime-software.html': navSvg('<path d="M9 8l-4 4 4 4"/><path d="M15 8l4 4-4 4"/><path d="M13 6l-2 12"/>'),
    'workspace-runtime-xhs.html': navSvg('<path d="M6 3h9l5 5v13a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z"/><path d="M14 3v6h6"/><path d="M9 13h7M9 17h5"/>'),
    'workspace-runtime-shortvideo.html': navSvg('<circle cx="12" cy="12" r="9"/><path d="M10 8.5l6 3.5-6 3.5v-7z"/>'),
    'workspace-runtime-department.html': navSvg('<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2"/><path d="M10 21v-3h4v3"/>'),
    'assets.html': navSvg('<rect x="3" y="4" width="18" height="5" rx="1"/><path d="M5 9v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V9"/><path d="M10 13h4"/>'),
    'knowledge.html': navSvg('<path d="M4 5a2 2 0 0 1 2-2h6v16H6a2 2 0 0 0-2 2V5z"/><path d="M20 5a2 2 0 0 0-2-2h-6v16h6a2 2 0 0 1 2 2V5z"/>'),
    'finance.html': navSvg('<path d="M7 5l5 7 5-7"/><path d="M12 12v7"/><path d="M8 14h8M8 17h8"/>'),
    'calendar.html': navSvg('<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 9h18"/><path d="M8 3v4M16 3v4"/>'),
    '__settings': navSvg('<circle cx="12" cy="12" r="3.2"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5 5l2.1 2.1M16.9 16.9L19 19M19 5l-2.1 2.1M7.1 16.9L5 19"/>'),
    '__help': navSvg('<circle cx="12" cy="12" r="9"/><path d="M9.2 9.5a2.8 2.8 0 0 1 5.4 1c0 1.8-2.6 2-2.6 3.5"/><circle cx="12" cy="17" r="0.7" fill="currentColor" stroke="none"/>'),
    '__default': navSvg('<circle cx="12" cy="12" r="3"/>')
  };

  // 归属同一 Workspace 运行入口的页面：这些页在导航里由「工作空间」一项代表，
  // 不作为与公司级栏目平级的独立分组出现。
  var RUNTIME_PAGES = [
    'workspace-runtime-software.html',
    'workspace-runtime-xhs.html',
    'workspace-runtime-shortvideo.html',
    'workspace-runtime-department.html',
    'workspace-studio.html',
    'workspace-shell-reference.html'
  ];

  function readState() {
    try {
      return JSON.parse(window.localStorage.getItem(STORAGE_KEY) || '{}') || {};
    } catch (error) {
      return {};
    }
  }

  function currentPage() {
    return window.location.pathname.split('/').pop() || 'ceo-desk.html';
  }

  // 办公室分组：只看公司状态，不看当前页面，保证全站签名一致。
  function activeOffices(state) {
    var hrefs = {};
    var events = state.calendarEvents || [];
    var firstBusiness = String(state.firstBusiness || (state.newBusinessDraft && state.newBusinessDraft.name) || '');
    var hasEvent = function (route) {
      return events.some(function (item) { return item && item.route === route; });
    };
    if (state.companyCreatedAt) {
      if (/软件|Curis|研发/.test(firstBusiness) || state.softwareAcceptance || hasEvent('workspace-runtime-software.html')) {
        hrefs['workspace-runtime-software.html'] = true;
      }
      if (/小红书/.test(firstBusiness) || state.latestXhsFeedback || hasEvent('workspace-runtime-xhs.html')) {
        hrefs['workspace-runtime-xhs.html'] = true;
      }
      if (/抖音|TikTok|短视频/.test(firstBusiness) || state.latestExternalFeedback || hasEvent('workspace-runtime-shortvideo.html')) {
        hrefs['workspace-runtime-shortvideo.html'] = true;
      }
    }
    if (state.departmentStatus === 'active') hrefs['workspace-runtime-department.html'] = true;
    return NAV_MODEL.offices.filter(function (item) { return hrefs[item[1]]; });
  }

  // 角标只反映需要 CEO 处理的事项数量，其余栏目保持安静。
  function badgeFor(label, state) {
    if (label === 'CEO 工作台') {
      var pending = (state.calendarEvents || []).filter(function (item) {
        return item && ['queued', 'waiting_ceo', 'acknowledged', 'failed'].indexOf(item.status) >= 0;
      }).length + ((state.lastConnector && state.lastConnector.status === 'pending') ? 1 : 0);
      return pending ? String(pending) : '';
    }
    if (label === '工作空间' && state.companyCreatedAt) {
      var count = activeOffices(state).filter(function (item) {
        return item[1] !== 'workspace-runtime-department.html';
      }).length;
      return count > 1 ? String(count) : '';
    }
    return '';
  }

  // 高亮分两级：
  //   exact   —— 当前页在导航中有精确入口，承担唯一的 aria-current="page"
  //   ancestor—— Workspace 运行页由「工作空间」代表，视觉同样高亮，但不重复
  //              声明 aria-current，避免一屏出现两个 current（WCAG 4.1.2）。
  function activeKind(href, page, hasExact) {
    if (href === page) return 'exact';
    if (href === 'workspace-portal.html' && RUNTIME_PAGES.indexOf(page) >= 0) {
      return hasExact ? 'ancestor' : 'exact';
    }
    return '';
  }

  function makeSection(label, items, sectionClass, page, state, hasExact, suppressHref) {
    var section = document.createElement('section');
    section.className = ('curis-nav-section ' + (sectionClass || '')).trim();
    section.style.cssText = 'display:grid;gap:var(--ui-sp-1);';
    if (label) {
      var heading = document.createElement('p');
      heading.className = 'nav-label';
      heading.textContent = label;
      heading.style.cssText = 'margin:var(--ui-sp-3) 0 var(--ui-sp-1);padding:0 var(--ui-sp-2);';
      section.appendChild(heading);
    }
    var nav = document.createElement('nav');
    nav.className = 'nav curis-canonical-nav-group';
    nav.setAttribute('aria-label', label || '主导航');
    nav.style.cssText = 'display:grid;gap:var(--ui-sp-1);';
    items.forEach(function (entry) {
      var name = entry[0], href = entry[1];
      var link = document.createElement('a');
      link.className = 'nav-item';
      link.href = href;
      link.dataset.curisCanonicalLink = 'true';
      var kind = activeKind(href, page, hasExact);
      if (href === suppressHref) kind = '';   // 当前页已在折叠区上方内联高亮，抽屉内同名项不再重复声明 current
      if (kind === 'exact') {
        link.setAttribute('aria-current', 'page');
        link.classList.add('active');
      } else if (kind === 'ancestor') {
        link.classList.add('active', 'is-ancestor');
      }
      var badge = badgeFor(name, state);
      link.innerHTML = '<span class="nav-icon icon" aria-hidden="true">' + (ICONS[href] || ICONS.__default) + '</span><span>' + name +
        '</span>' + (badge ? '<span class="nav-badge">' + badge + '</span>' : '');
      nav.appendChild(link);
    });
    section.appendChild(nav);
    return section;
  }

  function render() {
    var sidebar = document.querySelector('aside.sidebar') || document.querySelector('.sidebar');
    if (!sidebar) return false;
    if (sidebar.dataset.curisCanonicalNav === 'true') return true;
    sidebar.dataset.curisCanonicalNav = 'true';

    var page = currentPage();
    var state = readState();

    // 品牌区统一，缺失时补齐，避免各页自行拼装。
    var brand = sidebar.querySelector('.brand, .sidebar-brand');
    if (!brand) {
      brand = document.createElement('div');
      sidebar.insertBefore(brand, sidebar.firstChild);
    }
    brand.className = 'brand';
    brand.innerHTML = '<span class="brand-mark">C</span><span>Curis</span>';

    // 保留页面自带的侧栏脚注文案（各页可不同），但只保留一份。
    var footNodes = [].slice.call(sidebar.querySelectorAll('.sidebar-foot'));
    var sidebarFoot = footNodes.length ? footNodes[0].cloneNode(true) : null;

    // 清掉一切历史导航残留：静态 markup、旧分组、内联 fzn 渲染结果。
    sidebar.querySelectorAll(
      '.nav-section,.nav-list,.nav-group,.nav,.nav-footer,.sidebar-footer,.nav-label,' +
      '.sidebar-foot,.assistant-mini,.curis-nav-section,.curis-canonical-sidebar-main,' +
      '.fzn-nav,.fzn-footer,.fzn-group,.fzn-item'
    ).forEach(function (node) { node.remove(); });

    var offices = activeOffices(state);
    // 当前页是否在导航中有精确入口，决定 aria-current 落在子项还是父项。
    var hasExact = NAV_MODEL.primary.concat(NAV_MODEL.tools, offices, NAV_MODEL.resources)
      .some(function (entry) { return entry[1] === page; });

    // ── P2-2（修订）：4 常驻（公司级核心入口）+ 「更多」抽屉（7 折叠 + 动态办公室）──
    //   抽屉默认【始终收起】，不再按当前页自动整段展开；身处折叠区时，把当前页作为
    //   单个高亮项内联在常驻区下方（"当前栏目"），既满足 WCAG 2.4.3「当前位置可见」，
    //   又让默认视图稳定为 4（+1 当前）+ 更多，不再铺开整列。
    var PERSISTENT_HREFS = ['ceo-desk.html', 'operating.html', 'business.html', 'workspace-portal.html'];
    var persistent = NAV_MODEL.primary.filter(function (entry) {
      return PERSISTENT_HREFS.indexOf(entry[1]) >= 0;
    });
    // 折叠区全集（用于内联「当前栏目」判定与抽屉内容）
    var foldedAll = [['AI 团队', 'ai-organization.html']]
      .concat(NAV_MODEL.tools, NAV_MODEL.resources, offices);
    var currentFolded = foldedAll.filter(function (entry) { return entry[1] === page; })[0] || null;
    var suppressHref = currentFolded ? currentFolded[1] : null;

    var main = document.createElement('div');
    main.className = 'curis-canonical-sidebar-main';
    main.style.cssText = 'display:flex;flex-direction:column;gap:var(--ui-sp-1);flex:1;min-height:0;overflow:auto;';
    main.appendChild(makeSection('', persistent, 'curis-primary-nav', page, state, hasExact));

    // 身处折叠区页面：内联当前栏目（高亮 + aria-current），抽屉内同名项通过 suppressHref 跳过重复声明
    if (currentFolded) {
      main.appendChild(makeSection('当前栏目', [currentFolded], 'curis-here-nav', page, state, true));
    }

    var toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'nav-more-toggle';
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', '展开次要导航');
    toggle.style.cssText = 'display:flex;align-items:center;justify-content:space-between;width:100%;margin:var(--ui-sp-2) 0 var(--ui-sp-1);padding:var(--ui-sp-2);border:0;border-radius:var(--ui-r-sm);background:transparent;color:var(--ui-text-2);font:inherit;font-size:var(--ui-fs-1);cursor:pointer;';
    toggle.innerHTML = '<span>更多</span><span class="nav-more-caret" aria-hidden="true">▾</span>';
    var panel = document.createElement('div');
    panel.className = 'nav-more-panel';
    panel.style.cssText = 'display:none;gap:var(--ui-sp-1);';
    panel.hidden = true;
    panel.appendChild(makeSection('', [['AI 团队', 'ai-organization.html']], 'curis-ai-nav', page, state, hasExact, suppressHref));
    panel.appendChild(makeSection('经营工具', NAV_MODEL.tools, 'curis-tool-nav', page, state, hasExact, suppressHref));
    panel.appendChild(makeSection('公司资源', NAV_MODEL.resources, 'curis-resource-nav', page, state, hasExact, suppressHref));
    if (offices.length) panel.appendChild(makeSection('办公室', offices, 'curis-office-nav', page, state, hasExact, suppressHref));
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', open ? 'false' : 'true');
      panel.hidden = open;
      panel.style.display = open ? 'none' : 'grid';
    });
    main.appendChild(toggle);
    main.appendChild(panel);
    sidebar.appendChild(main);

    var footer = document.createElement('div');
    footer.className = 'nav-footer curis-canonical-footer';
    footer.style.cssText = 'margin-top:auto;display:grid;gap:var(--ui-sp-1);padding-top:var(--ui-sp-3);';
    // P2-5：设置 / 帮助不再是无动作的死链接（href="#"），改为打开 CEO 助理（真实可用动作）。
    NAV_MODEL.footer.forEach(function (entry) {
      var item = document.createElement('button');
      item.type = 'button';
      item.className = 'nav-item';
      item.style.cssText = 'width:100%;text-align:left;background:transparent;border:0;font:inherit;color:inherit;cursor:pointer;';
      var ficon = entry[0] === '设置' ? ICONS['__settings'] : ICONS['__help'];
      item.innerHTML = '<span class="nav-icon icon" aria-hidden="true">' + ficon + '</span><span>' + entry[0] + '</span>';
      item.addEventListener('click', function () {
        var fab = document.getElementById('assistant-fab');
        if (fab) fab.click();
      });
      footer.appendChild(item);
    });
    sidebar.appendChild(footer);

    if (sidebarFoot) sidebar.appendChild(sidebarFoot);
    return true;
  }

  window.CurisCanonicalNav = { MODEL: NAV_MODEL, render: render, readState: readState };

  /* ── 自动注入 Dev Mode 标注层（Frozen 交付物之一）
     仅当 URL 带 ?dev=1 或按 Shift+D 才激活，不激活时仅有极小监听器开销。 */
  (function loadDevMode() {
    var s = document.createElement('script');
    s.src = new URL('_system/devmode.js', location.href).pathname;
    s.async = true;
    // 避免阻塞 DOMContentLoaded；在 head 末尾追加即可
    (document.head || document.documentElement).appendChild(s);
  })();

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', render);
  } else {
    render();
  }
})();
