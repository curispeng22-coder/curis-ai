#!/usr/bin/env python3
"""Build R&D Workspace design pages from skeleton HTML."""
import re
from pathlib import Path

WORK = Path('/Users/yy/Documents/Curis AI Workspace/.design/rd-workspace-default-office/pages')

LAYOUT_CSS = '''<style id="rd-layout">
  .rd-shell {
    display: grid;
    grid-template-columns: 220px 256px minmax(0, 1fr);
    grid-template-rows: 100vh;
    height: 100vh;
    overflow: hidden;
    background: var(--ui-bg);
  }
  .rd-shell--collapsed { grid-template-columns: 220px 0 minmax(0, 1fr); }
  .rd-shell--utility { grid-template-columns: 220px minmax(0, 1fr) 380px; }
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
  .rd-context {
    display: flex;
    flex-direction: column;
    gap: var(--spacer-16);
    padding: var(--spacer-16);
    border-right: 1px solid var(--ui-line);
    background: var(--ui-surface);
    overflow-y: auto;
    min-width: 0;
  }
  .rd-context__section { display: flex; flex-direction: column; gap: var(--spacer-8); }
  .rd-context__title {
    font-size: var(--body-xs-font-size);
    line-height: var(--body-xs-line-height);
    font-weight: var(--font-weight-medium);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--ui-text-3);
  }
  .rd-context__value {
    font-size: var(--body-sm-font-size);
    line-height: var(--body-sm-line-height);
    color: var(--ui-text);
    font-weight: var(--font-weight-medium);
  }
  .rd-context__sub {
    font-size: var(--body-xs-font-size);
    line-height: var(--body-xs-line-height);
    color: var(--ui-text-2);
  }
  .rd-context__list { display: flex; flex-direction: column; gap: var(--spacer-6); }
  .rd-context__row {
    display: flex;
    align-items: center;
    gap: var(--spacer-8);
    font-size: var(--body-sm-font-size);
    color: var(--ui-text-2);
  }
  .rd-context__row:hover { color: var(--ui-text); }
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
  .rd-workspace { overflow-y: auto; padding: var(--spacer-24); }
  .rd-pagehead {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: var(--spacer-16);
    margin-bottom: var(--spacer-24);
  }
  .rd-pagehead__title {
    font-size: var(--heading-md-font-size);
    line-height: var(--heading-md-line-height);
    font-weight: var(--font-weight-strong);
    color: var(--ui-text);
  }
  .rd-pagehead__subtitle {
    font-size: var(--body-sm-font-size);
    line-height: var(--body-sm-line-height);
    color: var(--ui-text-2);
    margin-top: var(--spacer-4);
  }
  .rd-pagehead__actions { display: flex; align-items: center; gap: var(--spacer-8); flex-shrink: 0; }
  .rd-workstation {
    border: 1px solid var(--ui-line);
    border-radius: var(--radius-6);
    background: var(--ui-surface);
    overflow: hidden;
  }
  .rd-workstation + .rd-workstation { margin-top: var(--spacer-12); }
  .rd-workstation__head {
    display: flex;
    align-items: center;
    gap: var(--spacer-12);
    padding: var(--spacer-12) var(--spacer-16);
    cursor: pointer;
  }
  .rd-workstation__head:hover { background: var(--bg-overlay-l2); }
  .rd-workstation__avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: var(--body-sm-font-size);
    font-weight: var(--font-weight-strong);
    flex-shrink: 0;
  }
  .rd-workstation__avatar--pm { background: var(--status-primary-surface-l1); color: var(--status-primary-default); }
  .rd-workstation__avatar--arch { background: var(--bg-overlay-l3); color: var(--ui-text); }
  .rd-workstation__avatar--dev { background: var(--bg-brand-popup); color: var(--text-brand); }
  .rd-workstation__avatar--qa { background: var(--status-warning-surface-l1); color: var(--status-warning-default); }
  .rd-workstation__meta { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
  .rd-workstation__name { font-size: var(--body-base-font-size); line-height: var(--body-base-line-height); color: var(--ui-text); font-weight: var(--font-weight-medium); }
  .rd-workstation__role { font-size: var(--body-xs-font-size); color: var(--ui-text-2); }
  .rd-workstation__summary { font-size: var(--body-sm-font-size); color: var(--ui-text-2); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .rd-workstation__toggle { margin-left: auto; color: var(--ui-text-3); }
  .rd-workstation__body { border-top: 1px solid var(--ui-line); padding: var(--spacer-16); }
  .rd-conversation { display: flex; flex-direction: column; gap: var(--spacer-16); }
  .rd-message { display: flex; gap: var(--spacer-12); }
  .rd-message__avatar { flex-shrink: 0; }
  .rd-message__content { display: flex; flex-direction: column; gap: var(--spacer-4); min-width: 0; }
  .rd-message__bubble {
    max-width: 720px;
    padding: var(--spacer-12) var(--spacer-14);
    border-radius: var(--radius-8);
    background: var(--bg-overlay-l2);
    border: 1px solid var(--border-neutral-l2);
    color: var(--ui-text);
    font-size: var(--body-base-font-size);
    line-height: var(--body-base-line-height);
  }
  .rd-message__bubble--user { background: var(--bg-overlay-l3); border-color: var(--border-neutral-l3); }
  .rd-message__meta { font-size: var(--body-xs-font-size); color: var(--ui-text-3); }
  .rd-message__action { color: var(--text-brand); cursor: pointer; text-decoration: none; }
  .rd-message__action:hover { text-decoration: underline; }
  .rd-utility {
    display: flex;
    flex-direction: column;
    border-left: 1px solid var(--ui-line);
    background: var(--ui-surface);
    overflow: hidden;
  }
  .rd-utility__head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--spacer-12);
    height: 40px;
    padding: 0 var(--spacer-12);
    border-bottom: 1px solid var(--ui-line);
  }
  .rd-utility__title { font-size: var(--body-sm-font-size); font-weight: var(--font-weight-medium); color: var(--ui-text); }
  .rd-utility__owner { font-size: var(--body-xs-font-size); color: var(--ui-text-2); }
  .rd-utility__body { flex: 1; overflow: auto; padding: var(--spacer-16); font-family: var(--code-editor-font-family); font-size: var(--code-editor-font-size); line-height: var(--code-editor-line-height); }
  .rd-diff__file { margin-bottom: var(--spacer-16); }
  .rd-diff__path { font-size: var(--body-sm-font-size); color: var(--ui-text); margin-bottom: var(--spacer-8); }
  .rd-diff__line { display: flex; gap: var(--spacer-8); padding: 1px 0; color: var(--ui-text-2); }
  .rd-diff__num { width: 32px; text-align: right; color: var(--ui-text-3); user-select: none; }
  .rd-diff__add { color: var(--status-success-default); }
  .rd-diff__del { color: var(--status-error-default); }
  .rd-diff__mark { background: var(--bg-overlay-l3); color: var(--ui-text); }
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
    <button class="rd-iconbtn" aria-label="搜索"><i data-lucide="search" style="width:16px;height:16px;"></i></button>
    <button class="rd-iconbtn" aria-label="通知"><i data-lucide="bell" style="width:16px;height:16px;"></i></button>
    <button class="rd-iconbtn" aria-label="CEO Assistant"><i data-lucide="message-square" style="width:16px;height:16px;"></i></button>
    <span class="ds-avatar ds-avatar--sm" style="margin-left:var(--spacer-8);">C</span>
  </div>
</header>'''

CONTEXT = '''<aside class="rd-context" role="complementary" aria-label="上下文侧栏">
  <section class="rd-context__section">
    <div class="rd-context__title">当前 Workspace</div>
    <div class="rd-context__value">Curis Desktop / R&D 办公室</div>
    <div class="rd-context__sub">目标：完成 Desktop Shell 交互评审</div>
  </section>
  <section class="rd-context__section">
    <div class="rd-context__title">当前责任</div>
    <div class="rd-context__value">Shell 适配与主题修复</div>
    <div class="rd-context__sub">负责员工：开发工程师 · Codex</div>
  </section>
  <section class="rd-context__section">
    <div class="rd-context__title">相关文件 / 目录</div>
    <div class="ds-filetree" style="width:100%;background:var(--ui-bg);">
      <div class="ds-filetree__row"><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23a7adb6' stroke-width='2'%3E%3Cpath d='M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z'/%3E%3C/svg%3E" class="icon ds-filetree__chevron" alt=""><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23a7adb6' stroke-width='2'%3E%3Cpath d='M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z'/%3E%3C/svg%3E" class="icon" alt=""><span class="ds-filetree__label">frontend</span></div>
      <div class="ds-filetree__row" data-depth="1"><span class="ds-filetree__chevron ds-filetree__chevron--leaf"></span><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23a7adb6' stroke-width='2'%3E%3Cpath d='M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z'/%3E%3Cpolyline points='14 2 14 8 20 8'/%3E%3C/svg%3E" class="icon" alt=""><span class="ds-filetree__label">app/layout.js</span></div>
      <div class="ds-filetree__row is-active" data-depth="1"><span class="ds-filetree__chevron ds-filetree__chevron--leaf"></span><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23a7adb6' stroke-width='2'%3E%3Cpath d='M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z'/%3E%3Cpolyline points='14 2 14 8 20 8'/%3E%3C/svg%3E" class="icon" alt=""><span class="ds-filetree__label">app/theme.js</span></div>
      <div class="ds-filetree__row" data-depth="1"><span class="ds-filetree__chevron ds-filetree__chevron--leaf"></span><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23a7adb6' stroke-width='2'%3E%3Cpath d='M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z'/%3E%3C/svg%3E" class="icon" alt=""><span class="ds-filetree__label">components/shell</span></div>
    </div>
  </section>
  <section class="rd-context__section">
    <div class="rd-context__title">最近对象</div>
    <div class="rd-context__list">
      <div class="rd-context__row"><i data-lucide="file-text" style="width:14px;height:14px;"></i><span>PRD v1.2 · 已批准</span></div>
      <div class="rd-context__row"><i data-lucide="file-text" style="width:14px;height:14px;"></i><span>Tech Spec · 已批准</span></div>
      <div class="rd-context__row"><i data-lucide="scroll-text" style="width:14px;height:14px;"></i><span>Adapter Draft · 修改中</span></div>
    </div>
  </section>
</aside>'''

PAGEHEAD = '''<div class="rd-pagehead">
  <div>
    <div class="rd-pagehead__title">R&D 办公室 · Desktop Shell 交互评审</div>
    <div class="rd-pagehead__subtitle">当前目标：完成 Desktop Shell 适配并提交 QA</div>
  </div>
  <div class="rd-pagehead__actions">
    <button class="ds-btn ds-btn--secondary"><i data-lucide="users" style="width:14px;height:14px;"></i><span>团队</span></button>
    <button class="ds-btn ds-btn--ghost" aria-label="更多"><i data-lucide="more-horizontal" style="width:14px;height:14px;"></i></button>
  </div>
</div>'''

COMPOSER = '''<div class="ds-composer" style="max-width:none;margin-top:var(--spacer-16);">
  <textarea class="ds-composer__input" placeholder="继续当前工作…" rows="2"></textarea>
  <div class="ds-composer__toolbar">
    <div class="ds-composer__tools">
      <button class="ds-composer__icon-btn" aria-label="添加上下文"><i data-lucide="plus" style="width:16px;height:16px;color:var(--ui-text-2);"></i></button>
      <button class="ds-composer__model"><i data-lucide="zap" style="width:12px;height:12px;"></i><span>运行</span><i data-lucide="chevron-down" style="width:12px;height:12px;"></i></button>
      <button class="ds-composer__model"><span>Codex</span><i data-lucide="chevron-down" style="width:12px;height:12px;"></i></button>
    </div>
    <div class="ds-composer__actions">
      <button class="ds-composer__icon-btn" aria-label="停止"><i data-lucide="square" style="width:16px;height:16px;color:var(--ui-text-2);"></i></button>
      <button class="ds-composer__send" aria-label="发送"><i data-lucide="send" style="width:16px;height:16px;color:var(--ui-action-primary-fg);"></i></button>
    </div>
  </div>
</div>'''

WORKSTATION_PM = '''<article class="rd-workstation" data-state="completed">
  <div class="rd-workstation__head">
    <span class="rd-workstation__avatar rd-workstation__avatar--pm">P</span>
    <div class="rd-workstation__meta">
      <div class="rd-workstation__name">产品经理 · ChatGPT</div>
      <div class="rd-workstation__role">产品规划</div>
    </div>
    <div class="rd-workstation__summary">PRD 已锁定，已交接给架构师</div>
    <span class="ds-tag ds-tag--success">已完成</span>
    <span class="rd-workstation__toggle"><i data-lucide="chevron-down" style="width:16px;height:16px;"></i></span>
  </div>
</article>'''

WORKSTATION_ARCH = '''<article class="rd-workstation" data-state="completed">
  <div class="rd-workstation__head">
    <span class="rd-workstation__avatar rd-workstation__avatar--arch">A</span>
    <div class="rd-workstation__meta">
      <div class="rd-workstation__name">架构师 · Claude</div>
      <div class="rd-workstation__role">技术设计</div>
    </div>
    <div class="rd-workstation__summary">技术方案已批准，已交接给开发工程师</div>
    <span class="ds-tag ds-tag--success">已完成</span>
    <span class="rd-workstation__toggle"><i data-lucide="chevron-down" style="width:16px;height:16px;"></i></span>
  </div>
</article>'''

WORKSTATION_QA = '''<article class="rd-workstation" data-state="waiting">
  <div class="rd-workstation__head">
    <span class="rd-workstation__avatar rd-workstation__avatar--qa">Q</span>
    <div class="rd-workstation__meta">
      <div class="rd-workstation__name">QA</div>
      <div class="rd-workstation__role">质量验证</div>
    </div>
    <div class="rd-workstation__summary">等待开发工程师完成 Shell 适配后接手</div>
    <span class="ds-tag ds-tag--warning">等待</span>
    <span class="rd-workstation__toggle"><i data-lucide="chevron-down" style="width:16px;height:16px;"></i></span>
  </div>
</article>'''

CODEX_BODY = '''<div class="rd-workstation__body">
  <div class="rd-conversation">
    <div class="rd-message">
      <span class="ds-avatar rd-message__avatar" style="background:var(--ui-action-primary-bg);color:var(--ui-action-primary-fg);">C</span>
      <div class="rd-message__content">
        <div class="rd-message__bubble rd-message__bubble--user">
          把 Top Bar 的 theme toggle 改成跟随系统，并确保首次加载不闪烁。
        </div>
        <div class="rd-message__meta">CEO · 10:42</div>
      </div>
    </div>
    <div class="rd-message">
      <span class="ds-avatar rd-message__avatar rd-workstation__avatar--dev">C</span>
      <div class="rd-message__content">
        <div class="rd-message__bubble">
          已定位到 <code style="font-family:var(--code-editor-font-family);">theme.js</code> 的初始化顺序。我会先读取系统偏好，再渲染首屏，避免闪烁。需要同时调整 <code style="font-family:var(--code-editor-font-family);">app/layout.js</code> 的 provider 注入位置。
          <div style="margin-top:var(--spacer-8);"><a class="rd-message__action" href="rd-utility-open.html">修改 7 个文件 · 查看 Diff</a></div>
        </div>
        <div class="rd-message__meta">开发工程师 · Codex · 10:43</div>
      </div>
    </div>
    <div class="rd-message">
      <span class="ds-avatar rd-message__avatar rd-workstation__avatar--dev">C</span>
      <div class="rd-message__content">
        <div class="rd-message__bubble">
          正在运行 <code style="font-family:var(--code-editor-font-family);">frontend/tests/shell/theme.test.js</code>，确认切换后状态正确。
        </div>
        <div class="rd-message__meta">开发工程师 · Codex · 10:45</div>
      </div>
    </div>
  </div>
  {composer}
</div>'''.format(composer=COMPOSER)

WORKSTATION_CODEX_EXPANDED = f'''<article class="rd-workstation" data-state="working">
  <div class="rd-workstation__head">
    <span class="rd-workstation__avatar rd-workstation__avatar--dev">C</span>
    <div class="rd-workstation__meta">
      <div class="rd-workstation__name">开发工程师 · Codex</div>
      <div class="rd-workstation__role">代码实现</div>
    </div>
    <div class="rd-workstation__summary">正在修改 Adapter，保留当前测试范围</div>
    <span class="ds-tag ds-tag--brand"><span style="width:6px;height:6px;border-radius:50%;background:currentColor;display:inline-block;margin-right:6px;"></span>工作中</span>
    <span class="rd-workstation__toggle"><i data-lucide="chevron-up" style="width:16px;height:16px;"></i></span>
  </div>
  {CODEX_BODY}
</article>'''

WORKSTATION_CODEX_COLLAPSED = '''<article class="rd-workstation" data-state="working">
  <div class="rd-workstation__head">
    <span class="rd-workstation__avatar rd-workstation__avatar--dev">C</span>
    <div class="rd-workstation__meta">
      <div class="rd-workstation__name">开发工程师 · Codex</div>
      <div class="rd-workstation__role">代码实现</div>
    </div>
    <div class="rd-workstation__summary">正在修改 Adapter，保留当前测试范围</div>
    <span class="ds-tag ds-tag--brand"><span style="width:6px;height:6px;border-radius:50%;background:currentColor;display:inline-block;margin-right:6px;"></span>工作中</span>
    <span class="rd-workstation__toggle"><i data-lucide="chevron-down" style="width:16px;height:16px;"></i></span>
  </div>
</article>'''

WORKSPACE_DEFAULT = f'''<div class="rd-shell">
  {NAV}
  {CONTEXT}
  <div class="rd-main">
    {TOPBAR}
    <div class="rd-workspace">
      {PAGEHEAD}
      <section aria-label="员工工作位">
        {WORKSTATION_PM}
        {WORKSTATION_ARCH}
        {WORKSTATION_CODEX_EXPANDED}
        {WORKSTATION_QA}
      </section>
    </div>
  </div>
</div>'''

WORKSPACE_COLLAPSED = f'''<div class="rd-shell rd-shell--collapsed">
  {NAV}
  <div class="rd-main">
    {TOPBAR}
    <div class="rd-workspace">
      {PAGEHEAD}
      <section aria-label="员工工作位">
        {WORKSTATION_PM}
        {WORKSTATION_ARCH}
        {WORKSTATION_CODEX_COLLAPSED}
        {WORKSTATION_QA}
      </section>
    </div>
  </div>
</div>'''

UTILITY_PANE = '''<aside class="rd-utility" role="region" aria-label="开发工具面板">
  <div class="rd-utility__head">
    <div style="display:flex;align-items:center;gap:var(--spacer-8);">
      <span class="rd-utility__title">Diff / Changes</span>
      <span class="rd-utility__owner">开发工程师 · Codex · Shell 适配</span>
    </div>
    <a href="rd-workspace-default.html" class="rd-iconbtn" aria-label="返回对话"><i data-lucide="x" style="width:16px;height:16px;"></i></a>
  </div>
  <div class="ds-editortabs" style="border-bottom:1px solid var(--ui-line);">
    <div class="ds-editortab is-active"><span>变更概览</span></div>
    <div class="ds-editortab"><span>app/theme.js</span><i data-lucide="x" style="width:12px;height:12px;"></i></div>
    <div class="ds-editortab"><span>app/layout.js</span><i data-lucide="x" style="width:12px;height:12px;"></i></div>
  </div>
  <div class="rd-utility__body">
    <div class="rd-diff__file">
      <div class="rd-diff__path">frontend/app/theme.js</div>
      <div class="rd-diff__line"><span class="rd-diff__num">12</span><span class="rd-diff__del">- const theme = loadStoredTheme();</span></div>
      <div class="rd-diff__line"><span class="rd-diff__num">13</span><span class="rd-diff__add">+ const theme = resolveInitialTheme();</span></div>
      <div class="rd-diff__line"><span class="rd-diff__num">14</span><span class="rd-diff__mark">  const systemPrefers = window.matchMedia('(prefers-color-scheme: dark)');</span></div>
      <div class="rd-diff__line"><span class="rd-diff__num">15</span><span class="rd-diff__add">+ applyTheme(theme, { avoidFlash: true });</span></div>
    </div>
    <div class="rd-diff__file">
      <div class="rd-diff__path">frontend/app/layout.js</div>
      <div class="rd-diff__line"><span class="rd-diff__num"> 8</span><span class="rd-diff__del">- &lt;ThemeProvider&gt;</span></div>
      <div class="rd-diff__line"><span class="rd-diff__num"> 9</span><span class="rd-diff__add">+ &lt;ThemeProvider initial="system"&gt;</span></div>
      <div class="rd-diff__line"><span class="rd-diff__num">10</span><span class="rd-diff__mark">  &lt;Shell&gt;{children}&lt;/Shell&gt;</span></div>
    </div>
  </div>
</aside>'''

WORKSPACE_UTILITY = f'''<div class="rd-shell rd-shell--utility">
  {NAV}
  <div class="rd-main">
    {TOPBAR}
    <div class="rd-workspace">
      {PAGEHEAD}
      <section aria-label="员工工作位">
        {WORKSTATION_PM}
        {WORKSTATION_ARCH}
        {WORKSTATION_CODEX_EXPANDED}
        {WORKSTATION_QA}
      </section>
    </div>
  </div>
  {UTILITY_PANE}
</div>'''


def build_page(name, main_html):
    skel = (WORK / name).read_text(encoding='utf-8')
    skel = skel.replace('</head>', f'{LAYOUT_CSS}\n</head>')
    skel = skel.replace('<main>\n    </main>', f'<main>\n{main_html}\n    </main>')
    (WORK / name).write_text(skel, encoding='utf-8')


build_page('rd-workspace-default.html', WORKSPACE_DEFAULT)
build_page('rd-workstation-collapsed.html', WORKSPACE_COLLAPSED)
build_page('rd-utility-open.html', WORKSPACE_UTILITY)
print('pages built')
