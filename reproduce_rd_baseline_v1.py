#!/usr/bin/env python3
"""Reproduce Figma RD Workspace Visual Baseline v1 with three corrections:
1. Left nav uses current UI Blueprint six-area navigation.
2. Inline full Diff in Conversation becomes lightweight "查看差异" reference.
3. Employee header permanent professional tool buttons removed/reduced.
Only Default state is produced."""
from pathlib import Path
import re

ROOT = Path('/Users/yy/Documents/Curis AI Workspace/.design/rd-workspace-default-office')
PAGE = ROOT / 'pages' / 'rd-workspace-default.html'

html = PAGE.read_text(encoding='utf-8')
html = re.sub(r'<style id="rd-layout-v2">.*?</style>\n?', '', html, flags=re.DOTALL)

body_match = re.search(r'(<body[^>]*>)', html)
assert body_match, 'missing body tag'
body_start = body_match.end()

head_part = html[:body_start]
tail_part = '</body>\n</html>'

BASELINE_CSS = '''<style id="rd-baseline-v1">
  :root {
    --rd-nav-w: 220px;
    --rd-topbar-h: 52px;
    --rd-main-pad-x: 32px;
    --rd-main-pad-y: 24px;
  }
  .rd-shell {
    display: grid;
    grid-template-columns: var(--rd-nav-w) minmax(0, 1fr);
    grid-template-rows: 100vh;
    height: 100vh;
    overflow: hidden;
    background: var(--ui-bg);
    color: var(--ui-text);
  }

  /* ── Primary Navigation ── */
  .rd-nav {
    display: flex;
    flex-direction: column;
    gap: var(--spacer-8);
    padding: var(--spacer-14) var(--spacer-12);
    border-right: 1px solid var(--ui-line);
    background: var(--ui-bg);
    overflow-y: auto;
  }
  .rd-nav__brand {
    display: flex;
    align-items: center;
    gap: var(--spacer-8);
    height: 32px;
    padding: 0 var(--spacer-8);
    margin-bottom: var(--spacer-8);
    font-size: var(--heading-sm-font-size);
    font-weight: var(--font-weight-strong);
    color: var(--ui-text);
  }
  .rd-nav__beta {
    font-size: 10px;
    line-height: 1;
    font-weight: var(--font-weight-medium);
    color: var(--ui-text-3);
    padding: 2px 5px;
    border: 1px solid var(--ui-line);
    border-radius: var(--radius-4);
  }
  .rd-nav__group { display: flex; flex-direction: column; gap: 2px; }
  .rd-nav__item {
    display: flex;
    align-items: center;
    gap: var(--spacer-10);
    padding: var(--spacer-8) var(--spacer-10);
    border-radius: var(--radius-6);
    font-size: var(--body-sm-font-size);
    line-height: var(--body-sm-line-height);
    font-weight: var(--font-weight-medium);
    color: var(--ui-text-2);
    text-decoration: none;
    cursor: pointer;
    position: relative;
  }
  .rd-nav__item:hover { background: var(--bg-overlay-l2); color: var(--ui-text); }
  .rd-nav__item.is-active {
    background: var(--bg-overlay-l3);
    color: var(--ui-text);
  }
  .rd-nav__item.is-active::before {
    content: "";
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 3px;
    height: 18px;
    border-radius: 0 2px 2px 0;
    background: var(--ui-action-primary-bg);
  }
  .rd-nav__sub {
    display: flex;
    flex-direction: column;
    margin-left: var(--spacer-28);
    margin-top: 2px;
    gap: 2px;
  }
  .rd-nav__subitem {
    padding: var(--spacer-6) var(--spacer-10);
    border-radius: var(--radius-6);
    font-size: var(--body-xs-font-size);
    line-height: var(--body-xs-line-height);
    color: var(--ui-text-2);
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: var(--spacer-8);
  }
  .rd-nav__subitem:hover { background: var(--bg-overlay-l2); color: var(--ui-text); }
  .rd-nav__subitem.is-active { color: var(--ui-action-primary-fg); background: var(--ui-action-primary-bg); }
  .rd-nav__subitem-badge {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--ui-action-primary-bg);
  }
  .rd-nav__spacer { flex: 1; }
  .rd-nav__footer {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .rd-nav__profile {
    display: flex;
    align-items: center;
    gap: var(--spacer-8);
    padding: var(--spacer-8);
    border-radius: var(--radius-6);
    cursor: pointer;
  }
  .rd-nav__profile:hover { background: var(--bg-overlay-l2); }
  .rd-nav__profile-meta { display: flex; flex-direction: column; }
  .rd-nav__profile-name { font-size: var(--body-xs-font-size); color: var(--ui-text); }
  .rd-nav__profile-role { font-size: 10px; color: var(--ui-text-3); }

  /* ── Main Workspace ── */
  .rd-main {
    display: grid;
    grid-template-rows: var(--rd-topbar-h) minmax(0, 1fr);
    min-width: 0;
    overflow: hidden;
  }
  .rd-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--spacer-16);
    height: var(--rd-topbar-h);
    padding: 0 var(--rd-main-pad-x);
    border-bottom: 1px solid var(--ui-line);
    background: var(--ui-bg);
  }
  .rd-topbar__left { display: flex; align-items: center; gap: var(--spacer-16); min-width: 0; }
  .rd-breadcrumb {
    display: flex;
    align-items: center;
    gap: var(--spacer-6);
    font-size: var(--body-sm-font-size);
    color: var(--ui-text-2);
    flex-shrink: 0;
  }
  .rd-breadcrumb strong { color: var(--ui-text); font-weight: var(--font-weight-medium); }
  .rd-topbar__task {
    display: flex;
    align-items: center;
    gap: var(--spacer-8);
    font-size: var(--body-sm-font-size);
    color: var(--ui-text);
  }
  .rd-topbar__badge {
    font-size: var(--body-xs-font-size);
    font-weight: var(--font-weight-medium);
    color: var(--status-warning-default);
    background: var(--status-warning-surface-l1);
    padding: 2px var(--spacer-6);
    border-radius: var(--radius-4);
  }
  .rd-topbar__right { display: flex; align-items: center; gap: var(--spacer-8); flex-shrink: 0; }
  .rd-btn {
    display: inline-flex;
    align-items: center;
    gap: var(--spacer-4);
    height: 28px;
    padding: 0 var(--spacer-10);
    border-radius: var(--radius-6);
    border: 1px solid var(--ui-line);
    background: var(--ui-surface);
    color: var(--ui-text);
    font-size: var(--body-xs-font-size);
    font-weight: var(--font-weight-medium);
    cursor: pointer;
  }
  .rd-btn:hover { background: var(--bg-overlay-l2); }
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
    padding: var(--rd-main-pad-y) var(--rd-main-pad-x);
  }
  .rd-workspace-header {
    margin-bottom: var(--spacer-16);
  }
  .rd-workspace-title {
    font-size: var(--heading-md-font-size);
    line-height: var(--heading-md-line-height);
    font-weight: var(--font-weight-strong);
    color: var(--ui-text);
    margin-bottom: var(--spacer-6);
  }
  .rd-workspace-meta {
    display: flex;
    align-items: center;
    gap: var(--spacer-10);
    font-size: var(--body-sm-font-size);
    color: var(--ui-text-2);
  }
  .rd-workspace-meta__dot { color: var(--ui-text-3); }
  .rd-workspace-meta__alert { color: var(--status-warning-default); }

  .rd-statusbar {
    display: flex;
    align-items: center;
    gap: var(--spacer-8);
    padding: var(--spacer-10) 0;
    margin-bottom: var(--spacer-16);
    font-size: var(--body-sm-font-size);
    color: var(--status-success-default);
  }

  /* ── Workstations ── */
  .rd-workstations {
    display: flex;
    flex-direction: column;
    gap: var(--spacer-12);
  }
  .rd-workstation {
    border: 1px solid var(--ui-line);
    border-radius: var(--radius-8);
    background: var(--ui-surface);
    overflow: hidden;
  }
  .rd-workstation__head {
    display: flex;
    align-items: center;
    gap: var(--spacer-12);
    padding: var(--spacer-12) var(--spacer-16);
    cursor: pointer;
  }
  .rd-workstation__head:hover { background: var(--bg-overlay-l1); }
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
  .rd-workstation__avatar--dev { background: var(--bg-brand-popup); color: var(--text-brand); }
  .rd-workstation__avatar--arch { background: var(--bg-overlay-l3); color: var(--ui-text); }
  .rd-workstation__avatar--qa { background: var(--status-warning-surface-l1); color: var(--status-warning-default); }
  .rd-workstation__identity { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
  .rd-workstation__name { font-size: var(--body-base-font-size); line-height: var(--body-base-line-height); color: var(--ui-text); font-weight: var(--font-weight-medium); }
  .rd-workstation__role { font-size: var(--body-xs-font-size); line-height: var(--body-xs-line-height); color: var(--ui-text-3); }
  .rd-workstation__tags { display: flex; align-items: center; gap: var(--spacer-6); margin-left: auto; flex-shrink: 0; }
  .rd-tag {
    display: inline-flex;
    align-items: center;
    gap: var(--spacer-4);
    height: 22px;
    padding: 0 var(--spacer-8);
    border-radius: var(--radius-4);
    font-size: var(--body-xs-font-size);
    font-weight: var(--font-weight-medium);
  }
  .rd-tag--brand { color: var(--text-brand); background: var(--bg-brand-popup); }
  .rd-tag--neutral { color: var(--ui-text-2); background: var(--bg-overlay-l2); }
  .rd-tag--warning { color: var(--status-warning-default); background: var(--status-warning-surface-l1); }
  .rd-tag--danger { color: var(--status-error-default); background: var(--status-error-surface-l1); }
  .rd-tag__dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: currentColor;
  }
  .rd-workstation__chevron { color: var(--ui-text-3); flex-shrink: 0; width: 16px; height: 16px; }

  .rd-workstation__body {
    border-top: 1px solid var(--ui-line);
    padding: var(--spacer-16);
  }
  .rd-conversation {
    display: flex;
    flex-direction: column;
    gap: var(--spacer-20);
    max-width: 760px;
  }
  .rd-handoff {
    display: flex;
    align-items: center;
    gap: var(--spacer-8);
    font-size: var(--body-sm-font-size);
    color: var(--ui-text-2);
    padding-left: var(--spacer-40);
  }
  .rd-handoff__actor { color: var(--ui-text); font-weight: var(--font-weight-medium); }
  .rd-turn {
    display: flex;
    flex-direction: column;
    gap: var(--spacer-8);
  }
  .rd-turn__header {
    display: flex;
    align-items: center;
    gap: var(--spacer-10);
  }
  .rd-turn__avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: var(--body-xs-font-size);
    font-weight: var(--font-weight-strong);
  }
  .rd-turn__meta { display: flex; flex-direction: column; }
  .rd-turn__name { font-size: var(--body-sm-font-size); line-height: var(--body-sm-line-height); color: var(--ui-text); font-weight: var(--font-weight-medium); }
  .rd-turn__time { font-size: var(--body-xs-font-size); line-height: var(--body-xs-line-height); color: var(--ui-text-3); }
  .rd-turn__content {
    margin-left: var(--spacer-40);
    font-size: var(--body-base-font-size);
    line-height: var(--body-base-line-height);
    color: var(--ui-text);
  }
  .rd-turn__content p + p { margin-top: var(--spacer-12); }
  .rd-turn__content code {
    font-family: var(--code-editor-font-family);
    font-size: var(--code-editor-font-size);
    color: var(--ui-text-2);
    background: var(--bg-overlay-l2);
    padding: 1px 4px;
    border-radius: var(--radius-4);
  }

  /* Lightweight diff reference inside conversation */
  .rd-ref {
    display: inline-flex;
    align-items: center;
    gap: var(--spacer-8);
    margin-top: var(--spacer-10);
    padding: var(--spacer-8) var(--spacer-12);
    border: 1px solid var(--ui-line);
    border-radius: var(--radius-6);
    background: var(--bg-overlay-l1);
    color: var(--ui-text-2);
    font-size: var(--body-sm-font-size);
    cursor: pointer;
  }
  .rd-ref:hover { border-color: var(--ui-text-3); color: var(--ui-text); }
  .rd-ref__action { color: var(--text-brand); font-weight: var(--font-weight-medium); }

  /* ── Composer ── */
  .rd-composer {
    margin-top: var(--spacer-20);
    border: 1px solid var(--ui-line);
    border-radius: var(--radius-8);
    background: var(--ui-surface);
  }
  .rd-composer__input {
    width: 100%;
    padding: var(--spacer-14);
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
    padding: var(--spacer-10) var(--spacer-12);
    border-top: 1px solid var(--ui-line);
  }
  .rd-composer__left, .rd-composer__right { display: flex; align-items: center; gap: var(--spacer-4); }
  .rd-composer__btn {
    display: inline-flex;
    align-items: center;
    gap: var(--spacer-4);
    height: 26px;
    padding: 0 var(--spacer-8);
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
  <div class="rd-nav__brand">Curis <span class="rd-nav__beta">BETA</span></div>
  <nav class="rd-nav__group">
    <a class="rd-nav__item"><i data-lucide="home" style="width:16px;height:16px;"></i><span>首页 / CEO 工作台</span></a>
    <a class="rd-nav__item is-active"><i data-lucide="briefcase" style="width:16px;height:16px;"></i><span>业务空间</span></a>
    <div class="rd-nav__sub">
      <div class="rd-nav__subitem is-active"><span class="rd-nav__subitem-badge"></span><span>研发·默认办公室</span></div>
    </div>
    <a class="rd-nav__item"><i data-lucide="users" style="width:16px;height:16px;"></i><span>组织中心</span></a>
    <a class="rd-nav__item"><i data-lucide="sparkles" style="width:16px;height:16px;"></i><span>人才市场</span></a>
    <a class="rd-nav__item"><i data-lucide="folder-open" style="width:16px;height:16px;"></i><span>资料库</span></a>
    <a class="rd-nav__item"><i data-lucide="calendar" style="width:16px;height:16px;"></i><span>会议</span></a>
  </nav>
  <div class="rd-nav__spacer"></div>
  <nav class="rd-nav__footer">
    <a class="rd-nav__item"><i data-lucide="clock" style="width:16px;height:16px;"></i><span>最近工作</span></a>
    <a class="rd-nav__item"><i data-lucide="settings" style="width:16px;height:16px;"></i><span>设置</span></a>
    <a class="rd-nav__item"><i data-lucide="help-circle" style="width:16px;height:16px;"></i><span>帮助</span></a>
    <div class="rd-nav__profile">
      <span class="ds-avatar ds-avatar--sm">张</span>
      <div class="rd-nav__profile-meta">
        <span class="rd-nav__profile-name">张总</span>
        <span class="rd-nav__profile-role">CEO</span>
      </div>
    </div>
  </nav>
</aside>'''

TOPBAR = '''<header class="rd-topbar">
  <div class="rd-topbar__left">
    <div class="rd-breadcrumb">
      <span>工作空间</span><i data-lucide="chevron-right" style="width:14px;height:14px;"></i>
      <span>研发</span><i data-lucide="chevron-right" style="width:14px;height:14px;"></i>
      <strong>默认办公室</strong>
    </div>
    <div class="rd-topbar__task">
      <span>getUserData API 性能优化</span>
      <span class="rd-topbar__badge">1项需要决策</span>
    </div>
  </div>
  <div class="rd-topbar__right">
    <button class="rd-btn"><i data-lucide="plus" style="width:12px;height:12px;"></i><span>分配新工作</span></button>
    <button class="rd-iconbtn" aria-label="搜索"><i data-lucide="search" style="width:16px;height:16px;"></i></button>
    <button class="rd-iconbtn" aria-label="通知"><i data-lucide="bell" style="width:16px;height:16px;"></i></button>
    <button class="rd-iconbtn" aria-label="CEO Assistant"><i data-lucide="message-square" style="width:16px;height:16px;"></i></button>
    <span class="ds-avatar ds-avatar--sm">张</span>
  </div>
</header>'''

COMPOSER = '''<div class="rd-composer">
  <textarea class="rd-composer__input" placeholder="描述下一步工作，或向同事提出问题…" rows="2"></textarea>
  <div class="rd-composer__bar">
    <div class="rd-composer__left">
      <button class="rd-composer__btn"><i data-lucide="plus" style="width:12px;height:12px;"></i><span>添加</span></button>
      <button class="rd-composer__btn"><i data-lucide="zap" style="width:12px;height:12px;"></i><span>执行</span></button>
      <button class="rd-composer__btn"><span>Q3</span></button>
    </div>
    <div class="rd-composer__right">
      <button class="rd-composer__btn"><span>默认审批</span></button>
      <button class="rd-composer__send" aria-label="发送"><i data-lucide="send" style="width:14px;height:14px;"></i></button>
    </div>
  </div>
</div>'''

WORKSTATION_LI_MING = '''<article class="rd-workstation" data-state="needs_ceo">
  <div class="rd-workstation__head">
    <span class="rd-workstation__avatar rd-workstation__avatar--arch">李</span>
    <div class="rd-workstation__identity">
      <span class="rd-workstation__name">李明</span>
      <span class="rd-workstation__role">系统架构师</span>
    </div>
    <div class="rd-workstation__tags">
      <span class="rd-tag rd-tag--warning"><span>等待授权</span></span>
      <span class="rd-tag rd-tag--danger"><span class="rd-tag__dot"></span><span>需要 CEO</span></span>
    </div>
    <i data-lucide="chevron-down" class="rd-workstation__chevron"></i>
  </div>
</article>'''

WORKSTATION_WANG_SHUO = '''<article class="rd-workstation" data-state="waiting">
  <div class="rd-workstation__head">
    <span class="rd-workstation__avatar rd-workstation__avatar--qa">王</span>
    <div class="rd-workstation__identity">
      <span class="rd-workstation__name">王硕</span>
      <span class="rd-workstation__role">质量保障工程师</span>
    </div>
    <div class="rd-workstation__tags">
      <span class="rd-tag rd-tag--neutral"><span>等待中</span></span>
    </div>
    <i data-lucide="chevron-down" class="rd-workstation__chevron"></i>
  </div>
</article>'''

CHEN_HAO_BODY = f'''<div class="rd-workstation__body">
  <div class="rd-conversation">
    <div class="rd-handoff">
      <i data-lucide="git-commit" style="width:14px;height:14px;"></i>
      <span><span class="rd-handoff__actor">李明</span> 已完成架构方案，交接给 <span class="rd-handoff__actor">陈昊</span> 执行开发</span>
      <span>昨天 11:42</span>
    </div>
    <div class="rd-turn">
      <div class="rd-turn__header">
        <span class="rd-turn__avatar rd-workstation__avatar--dev">陈</span>
        <div class="rd-turn__meta">
          <span class="rd-turn__name">陈昊 · 全栈开发工程师</span>
          <span class="rd-turn__time">14:23</span>
        </div>
      </div>
      <div class="rd-turn__content">
        <p>我已完成 <code>getUserData()</code> 函数的重构。原先的三次独立数据库查询现已合并为单次联表查询，响应时间预计降低 68%。涉及 <code>api/users.ts</code> 与 <code>lib/db/queries.ts</code>，共 127 行修改。</p>
        <div class="rd-ref" title="在右侧 Utility Surface 查看完整差异">
          <i data-lucide="file-diff" style="width:14px;height:14px;"></i>
          <span>api/users.ts · 34-93</span>
          <span class="rd-ref__action">查看差异</span>
        </div>
      </div>
    </div>
  </div>
  {COMPOSER}
</div>'''

WORKSTATION_CHEN_HAO = f'''<article class="rd-workstation rd-workstation--expanded" data-state="working">
  <div class="rd-workstation__head">
    <span class="rd-workstation__avatar rd-workstation__avatar--dev">陈</span>
    <div class="rd-workstation__identity">
      <span class="rd-workstation__name">陈昊</span>
      <span class="rd-workstation__role">全栈开发工程师</span>
    </div>
    <div class="rd-workstation__tags">
      <span class="rd-tag rd-tag--brand"><span class="rd-tag__dot"></span><span>运行中</span></span>
      <span class="rd-tag rd-tag--neutral"><i data-lucide="git-branch" style="width:10px;height:10px;"></i><span>feat/api-perf-v2</span></span>
      <span class="rd-tag rd-tag--neutral"><span>ollama/qwen2.5</span></span>
    </div>
    <i data-lucide="chevron-up" class="rd-workstation__chevron"></i>
  </div>
  {CHEN_HAO_BODY}
</article>'''

BODY = f'''<div class="rd-shell">
  {NAV}
  <div class="rd-main">
    {TOPBAR}
    <div class="rd-workspace">
      <header class="rd-workspace-header">
        <h1 class="rd-workspace-title">研发·默认办公室</h1>
        <div class="rd-workspace-meta">
          <span>3名AI员工</span>
          <span class="rd-workspace-meta__dot">·</span>
          <span>getUserData API 性能优化</span>
          <span class="rd-workspace-meta__dot">·</span>
          <span class="rd-workspace-meta__alert">1项需要决策</span>
        </div>
      </header>
      <div class="rd-statusbar">
        <i data-lucide="check-circle" style="width:16px;height:16px;"></i>
        <span>已批准 — 李明正在继续执行数据库迁移</span>
      </div>
      <section class="rd-workstations" aria-label="员工工作位">
        {WORKSTATION_CHEN_HAO}
        {WORKSTATION_LI_MING}
        {WORKSTATION_WANG_SHUO}
      </section>
    </div>
  </div>
</div>'''

head_part = head_part.replace('</head>', f'{BASELINE_CSS}\n</head>')
PAGE.write_text(head_part + '\n' + BODY + '\n' + tail_part, encoding='utf-8')

print('baseline v1 reproduced')
