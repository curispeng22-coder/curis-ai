import fs from 'node:fs';
import path from 'node:path';

const PAGES_DIR = '/Users/yy/Documents/Curis AI Workspace/.design/curis-entry-lifecycle-task-a/pages';

const SHELL_PAGES = [
  'company-created.html',
  'ceo-assistant-no-model.html',
  'ceo-assistant-ready.html',
  'ceo-assistant-model-menu.html',
  'model-config.html',
  'model-config-list.html',
  'model-config-add.html',
  'model-config-advanced.html',
  'empty-ceo-desk.html',
  'empty-business-space.html',
  'empty-company.html',
  'create-business-entry.html',
];

const MAIN_NAV_ITEMS = [
  { id: 'nav-ceo-desk', href: './empty-company.html', icon: 'layout-grid', label: 'CEO 工作台', key: 'ceo-desk' },
  { id: 'nav-business-space', href: './empty-business-space.html', icon: 'briefcase-business', label: '业务空间', key: 'business-space' },
  { id: 'nav-organization', href: '#', icon: 'network', label: '组织中心', key: 'organization' },
  { id: 'nav-talent', href: '#', icon: 'users', label: '人才与能力', key: 'talent' },
  { id: 'nav-insights', href: '#', icon: 'bar-chart-3', label: '经营洞察', key: 'insights' },
  { id: 'nav-library', href: '#', icon: 'folder-open', label: '资料库', key: 'library' },
  { id: 'nav-meetings', href: '#', icon: 'video', label: '会议', key: 'meetings' },
];

const CEO_AVATAR_SVG = `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="w-full h-full"><circle cx="12" cy="12" r="12" fill="var(--ui-accent-soft)"/><circle cx="12" cy="9" r="3.5" fill="var(--ui-accent)"/><path d="M6 18.5c0-3.5 2.5-5.5 6-5.5s6 2 6 5.5" stroke="var(--ui-accent)" stroke-width="2" stroke-linecap="round"/></svg>`;

function navBlock(activeKey, assistantStatus = 'muted') {
  const items = MAIN_NAV_ITEMS.map(item => {
    const isActive = item.key === activeKey;
    const activeAttr = isActive ? ' class="nav-item is-active" aria-current="page"' : ' class="nav-item"';
    return `          <li><a id="${item.id}" href="${item.href}"${activeAttr}><i data-lucide="${item.icon}" class="nav-icon"></i><span>${item.label}</span></a></li>`;
  }).join('\n');

  const assistantStatusColor = assistantStatus === 'success' ? 'var(--ui-success)' : assistantStatus === 'warning' ? 'var(--ui-warning)' : 'var(--ui-text-3)';
  const assistantLabel = assistantStatus === 'success' ? 'CEO Assistant，AI 已启用' : 'CEO Assistant，AI 尚未启用';
  const assistantActive = activeKey === 'ceo-assistant' ? ' class="nav-item is-active" aria-current="page"' : ' class="nav-item"';

  return `<nav id="main-nav" class="main-nav" aria-label="主导航">
      <div class="nav-logo">
        <div class="nav-logo-mark">C</div>
        <span class="nav-logo-text">Curis</span>
      </div>
      <div class="flex-1 overflow-y-auto">
        <ul class="nav-section" style="list-style:none;margin:0;">
${items}
        </ul>
      </div>
      <div class="nav-section-divider"></div>
      <div class="nav-section">
        <button type="button" class="nav-item"><i data-lucide="search" class="nav-icon"></i><span>搜索</span></button>
        <button type="button" class="nav-item"><i data-lucide="settings" class="nav-icon"></i><span>设置</span></button>
        <button type="button" class="nav-item"><i data-lucide="sun-moon" class="nav-icon"></i><span>主题切换</span></button>
        <button type="button" id="nav-ceo-assistant"${assistantActive} aria-label="${assistantLabel}"><i data-lucide="sparkles" class="nav-icon"></i><span>CEO Assistant</span><span class="nav-status-dot" style="background:${assistantStatusColor};"></span></button>
      </div>
      <div class="nav-section-divider"></div>
      <div class="p-3">
        <button type="button" id="ceo-avatar-menu" class="ceo-avatar w-full" aria-haspopup="true" aria-expanded="false">
          <div class="ceo-avatar-image overflow-hidden">${CEO_AVATAR_SVG}</div>
          <span id="ceo-avatar-name" class="ceo-avatar-name truncate flex-1">小敏</span>
          <i data-lucide="chevron-up" class="w-3.5 h-3.5 text-[var(--ui-text-3)]"></i>
        </button>
        <div class="popover-menu hidden" id="ceo-menu-popover" role="menu">
          <div class="px-3 py-2 border-b border-[var(--ui-line)]">
            <p class="text-[var(--ui-fs-1)] text-[var(--ui-text-3)]">CEO Display Name</p>
            <p id="menu-ceo-name" class="text-[var(--ui-fs-2)] font-medium text-[var(--ui-text)] truncate">小敏</p>
          </div>
          <a href="./model-config-list.html" class="popover-menu-item" role="menuitem"><i data-lucide="cpu" class="w-4 h-4"></i><span>模型配置 / AI 能力设置</span></a>
          <button type="button" class="popover-menu-item" role="menuitem"><i data-lucide="user" class="w-4 h-4"></i><span>账户设置</span></button>
          <div class="popover-menu-divider"></div>
          <button type="button" class="popover-menu-item" role="menuitem"><i data-lucide="log-out" class="w-4 h-4"></i><span>退出</span></button>
        </div>
      </div>
    </nav>`;
}

const ACTIVE_MAP = {
  'company-created.html': 'ceo-desk',
  'empty-ceo-desk.html': 'ceo-desk',
  'empty-company.html': 'ceo-desk',
  'empty-business-space.html': 'business-space',
  'ceo-assistant-no-model.html': 'ceo-assistant',
  'ceo-assistant-ready.html': 'ceo-assistant',
  'ceo-assistant-model-menu.html': 'ceo-assistant',
  'create-business-entry.html': 'ceo-assistant',
  'model-config.html': null,
  'model-config-list.html': null,
  'model-config-add.html': null,
  'model-config-advanced.html': null,
};

const ASSISTANT_STATUS_MAP = {
  'company-created.html': 'warning',
  'empty-ceo-desk.html': 'muted',
  'empty-business-space.html': 'muted',
  'empty-company.html': 'success',
  'ceo-assistant-no-model.html': 'warning',
  'ceo-assistant-ready.html': 'success',
  'ceo-assistant-model-menu.html': 'success',
  'create-business-entry.html': 'success',
  'model-config.html': 'warning',
  'model-config-list.html': 'warning',
  'model-config-add.html': 'warning',
  'model-config-advanced.html': 'warning',
};

function replaceBetween(html, startMarker, endMarker, replacement) {
  const startIdx = html.indexOf(startMarker);
  if (startIdx === -1) {
    console.warn('start marker not found');
    return html;
  }
  const endIdx = html.indexOf(endMarker, startIdx + startMarker.length);
  if (endIdx === -1) {
    console.warn('end marker not found');
    return html;
  }
  return html.slice(0, startIdx) + replacement + html.slice(endIdx + endMarker.length);
}

for (const file of SHELL_PAGES) {
  const filePath = path.join(PAGES_DIR, file);
  if (!fs.existsSync(filePath)) {
    console.warn(`skip missing ${file}`);
    continue;
  }
  let html = fs.readFileSync(filePath, 'utf8');

  const activeKey = ACTIVE_MAP[file] ?? null;
  const assistantStatus = ASSISTANT_STATUS_MAP[file] ?? 'muted';
  html = replaceBetween(html, '<nav id="main-nav" class="main-nav" aria-label="主导航">', '</nav>', navBlock(activeKey, assistantStatus));

  html = html.replace(/AI EXECUTION NOT READY/g, 'AI 尚未启用');
  html = html.replace(/AI Ready/g, 'AI 已启用');
  html = html.replace(/AI 未 Ready/g, 'AI 尚未启用');
  html = html.replace(/Capability Gap/g, '能力缺口');
  html = html.replace(/Model Enabled/g, '模型已启用');
  html = html.replace(/Default Model/g, '默认模型');
  html = html.replace(/Health/g, '连接状态');
  html = html.replace(/Health Check/g, '连接检查');

  fs.writeFileSync(filePath, html);
  console.log(`updated ${file}`);
}
