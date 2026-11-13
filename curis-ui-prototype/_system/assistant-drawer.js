/* Curis Global Assistant Drawer — injects a consistent CEO Assistant
   floating trigger + right-side drawer into any page that loads it. */
(function () {
  'use strict';

  function initAssistantDrawer() {
    if (document.getElementById('assistant-drawer')) return;

    const context = (document.body.dataset.assistantContext || document.title || '当前页面')
      .replace(/Curis · /g, '')
      .replace(/ - Curis.*$/i, '')
      .trim();

    // Backdrop
    const overlay = document.createElement('div');
    overlay.id = 'assistant-overlay';
    overlay.className = 'assistant-overlay';
    overlay.setAttribute('aria-hidden', 'true');

    // Drawer
    const drawer = document.createElement('aside');
    drawer.id = 'assistant-drawer';
    drawer.className = 'assistant-drawer';
    /* P0-4 fix: the assistant drawer is a NON-modal supplementary side panel,
       not a modal dialog. role=dialog + aria-modal=true trapped screen readers
       into the drawer and hid the rest of the page. Restore the <aside>'s
       implicit complementary role and drop aria-modal. */
    drawer.setAttribute('role', 'complementary');
    drawer.setAttribute('aria-hidden', 'true');
    drawer.setAttribute('aria-label', 'CEO 助理抽屉');

    // Body content: prefer page-defined template, else default suggestions
    let bodyHtml = '';
    const tpl = document.getElementById('assistant-drawer-body');
    if (tpl) {
      bodyHtml = tpl.innerHTML;
    } else {
      bodyHtml = `
        <div class="assistant-context">
          <div class="assistant-context-label">当前上下文</div>
          <div class="assistant-context-value">${escapeHtml(context)}</div>
        </div>
        <div class="assistant-greeting">你好，我是 Curis CEO 助理。我可以帮你整理当前页面需要关注的重点，或生成下一步动作建议。</div>
        <div class="assistant-actions">
          <button class="assistant-action" type="button">
            <span class="assistant-action-marker decision"></span>
            <span>
              <p class="assistant-action-title">生成决策包</p>
              <p class="assistant-action-desc">汇总当前上下文，整理投入产出模拟、现金流影响与回滚路径。</p>
            </span>
          </button>
          <button class="assistant-action" type="button">
            <span class="assistant-action-marker attention"></span>
            <span>
              <p class="assistant-action-title">标记需关注项</p>
              <p class="assistant-action-desc">识别页面中状态异常或需要 CEO 决策的事项。</p>
            </span>
          </button>
          <button class="assistant-action" type="button">
            <span class="assistant-action-marker info"></span>
            <span>
              <p class="assistant-action-title">解释当前状态</p>
              <p class="assistant-action-desc">用一句话总结当前页面最关键的信息。</p>
            </span>
          </button>
        </div>
      `;
    }

    drawer.innerHTML = `
      <div class="assistant-drawer-header">
        <div class="assistant-drawer-title">
          <div class="assistant-drawer-avatar">C</div>
          <span>Assistant · Curis</span>
        </div>
        <button class="assistant-drawer-close" type="button" aria-label="关闭抽屉">×</button>
      </div>
      <div class="assistant-drawer-body">
        ${bodyHtml}
      </div>
    `;

    // Floating trigger
    const fab = document.createElement('button');
    fab.id = 'assistant-fab';
    fab.className = 'assistant-fab';
    fab.type = 'button';
    fab.setAttribute('aria-label', '询问 CEO 助理');
    fab.innerHTML = '<span>询问助理</span>';

    document.body.appendChild(overlay);
    document.body.appendChild(drawer);
    document.body.appendChild(fab);

    function toggle(open) {
      const shouldOpen = open === undefined ? !drawer.classList.contains('open') : Boolean(open);
      drawer.classList.toggle('open', shouldOpen);
      overlay.classList.toggle('open', shouldOpen);
      drawer.setAttribute('aria-hidden', shouldOpen ? 'false' : 'true');
      if (shouldOpen) {
        const closeBtn = drawer.querySelector('.assistant-drawer-close');
        if (closeBtn) closeBtn.focus();
      }
    }

    fab.addEventListener('click', () => toggle());
    overlay.addEventListener('click', () => toggle(false));
    drawer.querySelector('.assistant-drawer-close').addEventListener('click', () => toggle(false));

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && drawer.classList.contains('open')) {
        toggle(false);
      }
    });
  }

  function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, (m) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAssistantDrawer);
  } else {
    initAssistantDrawer();
  }
})();
