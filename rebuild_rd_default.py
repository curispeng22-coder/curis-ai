#!/usr/bin/env python3
"""Rebuild Default R&D Workspace page from current skeleton, applying corrected v2 layout."""
from pathlib import Path
import re

ROOT = Path('/Users/yy/Documents/Curis AI Workspace/.design/rd-workspace-default-office')
PAGE = ROOT / 'pages' / 'rd-workspace-default.html'

# Extract existing head (tokens + components) from the current page
html = PAGE.read_text(encoding='utf-8')

# Remove old rd-layout style block
html = re.sub(r'<style id="rd-layout">.*?</style>\n?', '', html, flags=re.DOTALL)

# Find end of opening body tag
body_match = re.search(r'(<body[^>]*>)', html)
assert body_match, 'missing body tag'
body_start = body_match.end()

head_part = html[:body_start]
tail_part = '</body>\n</html>'

LAYOUT_V2_CSS = '''<style id="rd-layout-v2">
  .rd-shell {
    display: grid;
    grid-template-columns: 220px minmax(0, 1fr);
    grid-template-rows: 100vh;
    height: 100vh;
    overflow: hidden;
    background: var(--ui-bg);
    color: var(--ui-text);
  }
  .rd-shell--context {
    grid-template-columns: 220px minmax(0, 1fr) 280px;
  }
  .rd-nav {
    display: flex;
    flex-direction: column;
    gap: var(--spacer-8);
    padding: var(--spacer-12);
    border-right: 1px solid var(--ui-line);
    background: var(--ui-bg);
    overflow-y: auto;
  }
  .rd-nav__brand {
    display: flex;
    align-items: center;
    gap: var(--spacer-8);
    height: 36px;
    padding: 0 var(--spacer-8);
    font-size: var(--heading-sm-font-size);
    font-weight: var(--font-weight-strong);
    color: var(--ui-text);
  }
  .rd-nav__group { display: flex; flex-direction: column; gap: 2px; }
  .rd-nav__item {
    display: flex;
    align-items: center;
    gap: var(--spacer-8);
    padding: var(--spacer-8);
    border-radius: var(--radius-6);
    font-size: var(--body-sm-font-size);
    line-height: var(--body-sm-line-height);
    font-weight: var(--font-weight-medium);
    color: var(--ui-text-2);
    text-decoration: none;
    cursor: pointer;
  }
  .rd-nav__item:hover { background: var(--bg-overlay-l2); color: var(--ui-text); }
  .rd-nav__item.is-active { background: var(--ui-action-primary-bg); color: var(--ui-action-primary-fg); }
  .rd-nav__spacer { flex: 1; }
  .rd-main {
    display: grid;
    grid-template-rows: 52px minmax(0, 1fr);
    min-width: 0;
    overflow: hidden;
  }
  .rd-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--spacer-16);
    height: 52px;
    padding: 0 var(--spacer-16);
    border-bottom: 1px solid var(--ui-line);
    background: var(--ui-bg);
  }
  .rd-breadcrumb {
    display: flex;
    align-items: center;
    gap: var(--spacer-8);
    font-size: var(--body-sm-font-size);
    color: var(--ui-text-2);
  }
  .rd-breadcrumb strong { color: var(--ui-text); font-weight: var(--font-weight-medium); }
  .rd-topbar__actions { display: flex; align-items: center; gap: var(--spacer-8); }
  .rd-iconbtn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: var(--radius-6);
    background: transparent;
    border: none;
    color: var(--ui-text-2);
    cursor: pointer;
  }
  .rd-iconbtn:hover { background: var(--bg-overlay-l2); color: var(--ui-text); }
  .rd-workspace {
    overflow-y: auto;
    padding: var(--spacer-24) var(--spacer-32);
  }
  .rd-workspace-header {
    max-width: 840px;
    margin: 0 auto var(--spacer-24);
  }
  .rd-workspace-title {
    font-size: var(--heading-md-font-size);
    line-height: var(--heading-md-line-height);
    font-weight: var(--font-weight-strong);
    color: var(--ui-text);
  }
  .rd-workspace-subtitle {
    font-size: var(--body-sm-font-size);
    line-height: var(--body-sm-line-height);
    color: var(--ui-text-2);
    margin-top: var(--spacer-4);
  }
  .rd-workstations {
    display: flex;
    flex-direction: column;
    border-top: 1px solid var(--ui-line);
    max-width: 840px;
    margin: 0 auto;
  }
  .rd-workstation {
    border-bottom: 1px solid var(--ui-line);
  }
  .rd-workstation__head {
    display: flex;
    align-items: center;
    gap: var(--spacer-12);
    padding: var(--spacer-12) 0;
    cursor: pointer;
  }
  .rd-workstation__head:hover { background: var(--bg-overlay-l1); }
  .rd-workstation__avatar {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: var(--body-xs-font-size);
    font-weight: var(--font-weight-strong);
    flex-shrink: 0;
  }
  .rd-workstation__avatar--pm { background: var(--status-primary-surface-l1); color: var(--status-primary-default); }
  .rd-workstation__avatar--arch { background: var(--bg-overlay-l3); color: var(--ui-text); }
  .rd-workstation__avatar--dev { background: var(--bg-brand-popup); color: var(--text-brand); }
  .rd-workstation__avatar--qa { background: var(--status-warning-surface-l1); color: var(--status-warning-default); }
  .rd-workstation__meta { flex: 1; min-width: 0; display: flex; align-items: baseline; gap: var(--spacer-12); }
  .rd-workstation__name { font-size: var(--body-base-font-size); line-height: var(--body-base-line-height); color: var(--ui-text); font-weight: var(--font-weight-medium); white-space: nowrap; }
  .rd-workstation__summary { font-size: var(--body-sm-font-size); color: var(--ui-text-2); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .rd-workstation__status {
    display: inline-flex;
    align-items: center;
    gap: var(--spacer-4);
    font-size: var(--body-xs-font-size);
    line-height: var(--body-xs-line-height);
    font-weight: var(--font-weight-medium);
    flex-shrink: 0;
  }
  .rd-workstation__status--completed { color: var(--status-success-default); }
  .rd-workstation__status--working { color: var(--text-brand); }
  .rd-workstation__status--working::before {
    content: "";
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: currentColor;
  }
  .rd-workstation__status--waiting { color: var(--status-warning-default); }
  .rd-workstation__chevron { color: var(--ui-text-3); flex-shrink: 0; width: 16px; height: 16px; }
  .rd-workstation__body {
    padding-bottom: var(--spacer-24);
  }
  .rd-conversation {
    display: flex;
    flex-direction: column;
    gap: var(--spacer-24);
  }
  .rd-turn {
    display: flex;
    flex-direction: column;
    gap: var(--spacer-6);
  }
  .rd-turn__header {
    display: flex;
    align-items: center;
    gap: var(--spacer-8);
    color: var(--ui-text-2);
    font-size: var(--body-xs-font-size);
  }
  .rd-turn__content {
    color: var(--ui-text);
    font-size: var(--body-base-font-size);
    line-height: var(--body-base-line-height);
    padding-left: var(--spacer-32);
  }
  .rd-turn__content p + p { margin-top: var(--spacer-12); }
  .rd-turn__content ul { margin-top: var(--spacer-8); padding-left: var(--spacer-16); color: var(--ui-text-2); }
  .rd-turn__content li + li { margin-top: var(--spacer-4); }
  .rd-turn__content code {
    font-family: var(--code-editor-font-family);
    font-size: var(--code-editor-font-size);
    color: var(--ui-text-2);
    background: var(--bg-overlay-l2);
    padding: 1px 4px;
    border-radius: var(--radius-4);
  }
  .rd-composer {
    margin-top: var(--spacer-24);
    border: 1px solid var(--ui-line);
    border-radius: var(--radius-8);
    background: var(--ui-surface);
  }
  .rd-composer__input {
    width: 100%;
    padding: var(--spacer-12) var(--spacer-14);
    border: none;
    background: transparent;
    color: var(--ui-text);
    font-size: var(--body-base-font-size);
    line-height: var(--body-base-line-height);
    resize: none;
    outline: none;
  }
  .rd-composer__bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--spacer-8);
    padding: var(--spacer-8) var(--spacer-12);
    border-top: 1px solid var(--ui-line);
  }
  .rd-composer__left, .rd-composer__right { display: flex; align-items: center; gap: var(--spacer-4); }
  .rd-composer__btn {
    display: inline-flex;
    align-items: center;
    gap: var(--spacer-4);
    padding: var(--spacer-4) var(--spacer-8);
    border-radius: var(--radius-4);
    border: none;
    background: transparent;
    color: var(--ui-text-2);
    font-size: var(--body-xs-font-size);
    cursor: pointer;
  }
  .rd-composer__btn:hover { background: var(--bg-overlay-l2); color: var(--ui-text); }
  .rd-composer__send {
    width: 28px;
    height: 28px;
    border-radius: var(--radius-6);
    background: var(--ui-action-primary-bg);
    color: var(--ui-action-primary-fg);
    border: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }
  .rd-composer__send:hover { filter: brightness(1.1); }
</style>'''

NAV = '''<aside class="rd-nav" role="navigation" aria-label="一级导航">
  <div class="rd-nav__brand">Curis</div>
  <nav class="rd-nav__group">
    <a class="rd-nav__item"><i data-lucide="home" style="width:16px;height:16px;"></i><span>首页 / CEO 工作台</span></a>
    <a class="rd-nav__item is-active"><i data-lucide="layers" style="width:16px;height:16px;"></i><span>业务空间</span></a>
    <a class="rd-nav__item"><i data-lucide="users" style="width:16px;height:16px;"></i><span>组织中心</span></a>
    <a class="rd-nav__item"><i data-lucide="sparkles" style="width:16px;height:16px;"></i><span>人才市场</span></a>
    <a class="rd-nav__item"><i data-lucide="folder-open" style="width:16px;height:16px;"></i><span>资料库</span></a>
    <a class="rd-nav__item"><i data-lucide="calendar" style="width:16px;height:16px;"></i><span>会议</span></a>
  </nav>
  <div class="rd-nav__spacer"></div>
  <nav class="rd-nav__group">
    <a class="rd-nav__item"><i data-lucide="clock" style="width:16px;height:16px;"></i><span>最近工作</span></a>
    <a class="rd-nav__item"><i data-lucide="user" style="width:16px;height:16px;"></i><span>我的账户</span></a>
  </nav>
</aside>'''

TOPBAR = '''<header class="rd-topbar">
  <div class="rd-breadcrumb">
    <span>业务空间</span><i data-lucide="chevron-right" style="width:14px;height:14px;"></i>
    <span>Curis Desktop</span><i data-lucide="chevron-right" style="width:14px;height:14px;"></i>
    <strong>R&D 办公室</strong>
  </div>
  <div class="rd-topbar__actions">
    <button class="rd-iconbtn" aria-label="上下文" title="上下文"><i data-lucide="panel-right-open" style="width:16px;height:16px;"></i></button>
    <button class="rd-iconbtn" aria-label="通知"><i data-lucide="bell" style="width:16px;height:16px;"></i></button>
    <button class="rd-iconbtn" aria-label="CEO Assistant"><i data-lucide="message-square" style="width:16px;height:16px;"></i></button>
    <span class="ds-avatar ds-avatar--sm" style="margin-left:var(--spacer-8);">C</span>
  </div>
</header>'''

COMPOSER = '''<div class="rd-composer">
  <textarea class="rd-composer__input" placeholder="继续当前工作…" rows="2"></textarea>
  <div class="rd-composer__bar">
    <div class="rd-composer__left">
      <button class="rd-composer__btn" aria-label="添加上下文"><i data-lucide="plus" style="width:12px;height:12px;"></i></button>
      <button class="rd-composer__btn"><i data-lucide="zap" style="width:12px;height:12px;"></i><span>运行</span></button>
      <button class="rd-composer__btn"><span>Codex</span></button>
    </div>
    <div class="rd-composer__right">
      <button class="rd-composer__btn" aria-label="停止"><i data-lucide="square" style="width:12px;height:12px;"></i></button>
      <button class="rd-composer__send" aria-label="发送"><i data-lucide="send" style="width:14px;height:14px;"></i></button>
    </div>
  </div>
</div>'''

WORKSTATION_PM = '''<article class="rd-workstation" data-state="completed">
  <div class="rd-workstation__head">
    <span class="rd-workstation__avatar rd-workstation__avatar--pm">P</span>
    <div class="rd-workstation__meta">
      <span class="rd-workstation__name">产品经理 · ChatGPT</span>
      <span class="rd-workstation__summary">PRD 已锁定，已交接给架构师</span>
    </div>
    <span class="rd-workstation__status rd-workstation__status--completed">已完成</span>
    <i data-lucide="chevron-down" class="rd-workstation__chevron"></i>
  </div>
</article>'''

WORKSTATION_ARCH = '''<article class="rd-workstation" data-state="completed">
  <div class="rd-workstation__head">
    <span class="rd-workstation__avatar rd-workstation__avatar--arch">A</span>
    <div class="rd-workstation__meta">
      <span class="rd-workstation__name">架构师 · Claude</span>
      <span class="rd-workstation__summary">技术方案已批准，已交接给开发工程师</span>
    </div>
    <span class="rd-workstation__status rd-workstation__status--completed">已完成</span>
    <i data-lucide="chevron-down" class="rd-workstation__chevron"></i>
  </div>
</article>'''

WORKSTATION_QA = '''<article class="rd-workstation" data-state="waiting">
  <div class="rd-workstation__head">
    <span class="rd-workstation__avatar rd-workstation__avatar--qa">Q</span>
    <div class="rd-workstation__meta">
      <span class="rd-workstation__name">QA</span>
      <span class="rd-workstation__summary">等待开发工程师完成 Shell 适配后接手</span>
    </div>
    <span class="rd-workstation__status rd-workstation__status--waiting">等待</span>
    <i data-lucide="chevron-down" class="rd-workstation__chevron"></i>
  </div>
</article>'''

CODEX_BODY = f'''<div class="rd-workstation__body">
  <div class="rd-conversation">
    <div class="rd-turn rd-turn--user">
      <div class="rd-turn__header">
        <span class="ds-avatar ds-avatar--sm" style="background:var(--ui-action-primary-bg);color:var(--ui-action-primary-fg);">CEO</span>
        <span>CEO · 10:42</span>
      </div>
      <div class="rd-turn__content">
        把 Top Bar 的 theme toggle 改成跟随系统，并确保首次加载不闪烁。
      </div>
    </div>
    <div class="rd-turn">
      <div class="rd-turn__header">
        <span class="ds-avatar ds-avatar--sm rd-workstation__avatar--dev">C</span>
        <span>开发工程师 · Codex · 10:43</span>
      </div>
      <div class="rd-turn__content">
        <p>已定位到 <code>theme.js</code> 的初始化顺序。我会先读取系统偏好，再渲染首屏，避免闪烁。需要同时调整 <code>app/layout.js</code> 的 provider 注入位置。</p>
        <p>预计修改 7 个文件，主要变更：</p>
        <ul>
          <li><code>theme.js</code>：使用 <code>resolveInitialTheme()</code> 替代 <code>loadStoredTheme()</code></li>
          <li><code>layout.js</code>：<code>ThemeProvider</code> 增加 <code>initial="system"</code></li>
          <li>Shell 组件：移除硬编码 <code>dark</code> class</li>
        </ul>
      </div>
    </div>
    <div class="rd-turn">
      <div class="rd-turn__header">
        <span class="ds-avatar ds-avatar--sm rd-workstation__avatar--dev">C</span>
        <span>开发工程师 · Codex · 10:45</span>
      </div>
      <div class="rd-turn__content">
        正在运行 <code>frontend/tests/shell/theme.test.js</code>，确认切换后状态正确。
      </div>
    </div>
  </div>
  {COMPOSER}
</div>'''

WORKSTATION_CODEX = f'''<article class="rd-workstation rd-workstation--expanded" data-state="working">
  <div class="rd-workstation__head">
    <span class="rd-workstation__avatar rd-workstation__avatar--dev">C</span>
    <div class="rd-workstation__meta">
      <span class="rd-workstation__name">开发工程师 · Codex</span>
      <span class="rd-workstation__summary">正在修改 Adapter，保留当前测试范围</span>
    </div>
    <span class="rd-workstation__status rd-workstation__status--working">工作中</span>
    <i data-lucide="chevron-up" class="rd-workstation__chevron"></i>
  </div>
  {CODEX_BODY}
</article>'''

BODY = f'''<div class="rd-shell">
  {NAV}
  <div class="rd-main">
    {TOPBAR}
    <div class="rd-workspace">
      <header class="rd-workspace-header">
        <h1 class="rd-workspace-title">R&D 办公室 · Desktop Shell 交互评审</h1>
        <p class="rd-workspace-subtitle">当前责任：Shell 适配与主题修复 · 负责员工：开发工程师 · Codex</p>
      </header>
      <section class="rd-workstations" aria-label="员工工作位">
        {WORKSTATION_PM}
        {WORKSTATION_ARCH}
        {WORKSTATION_CODEX}
        {WORKSTATION_QA}
      </section>
    </div>
  </div>
</div>'''

# Insert new layout CSS just before </head>
head_part = head_part.replace('</head>', f'{LAYOUT_V2_CSS}\n</head>')

PAGE.write_text(head_part + '\n' + BODY + '\n' + tail_part, encoding='utf-8')

# Remove other state pages
for obsolete in ['rd-workstation-collapsed.html', 'rd-utility-open.html']:
    p = ROOT / 'pages' / obsolete
    if p.exists():
        p.unlink()

print('default page rebuilt; obsolete pages removed')
