const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');

const FILE = '/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype/decision-room.html';
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    defaultViewport: { width: 1440, height: 900 },
    args: ['--no-proxy-server', '--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--allow-file-access-from-files']
  });
  const page = await browser.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));

  await page.setRequestInterception(true);
  page.on('request', r => {
    const u = r.url();
    if (u.startsWith('http')) r.abort().catch(() => {});
    else r.continue().catch(() => {});
  });

  const t0 = Date.now();
  await page.goto('file://' + FILE, { waitUntil: 'domcontentloaded', timeout: 30000 });
  // give scripts a tick
  await new Promise(r => setTimeout(r, 600));
  const wall = Date.now() - t0;

  const checks = await page.evaluate(() => {
    const out = {};
    out.inboxCount = document.querySelectorAll('.dr-item').length;
    out.workspaceStudioLinks = document.querySelectorAll('a[href*="workspace-studio"]').length;
    out.modalBackdrop = document.querySelectorAll('.modal-backdrop').length;
    out.ariaModal = document.querySelectorAll('[aria-modal="true"]').length;
    out.roleDialog = document.querySelectorAll('[role="dialog"]').length;
    out.cdnScripts = [...document.querySelectorAll('script[src]')].filter(s => /cdn|unpkg|jsdelivr/.test(s.src)).length;
    out.themeVarsStyle = !!document.getElementById('theme-vars');
    out.inlineShadcn = !!document.querySelector('style#theme-vars, style#semantic-token-fallback');
    // forbidden visible English terms (case-insensitive) anywhere in body text
    const bodyText = document.body.innerText || '';
    const forbidden = ['ROI', 'KPI', 'Agent', 'Runtime', 'Studio', 'Truth', 'Blueprint', 'Outcome', 'Evidence', 'Workspace'];
    out.forbiddenHits = forbidden.filter(w => new RegExp('\\b' + w + '\\b', 'i').test(bodyText));
    // back button present
    out.backBtn = !!document.getElementById('backBtn');
    out.breadcrumb = (document.querySelector('.crumbs') ? document.querySelector('.crumbs').innerText.replace(/\s+/g, ' ').trim() : '');
    out.pendingBadge = (document.getElementById('pendingBadge') || {}).textContent || '';
    return out;
  });

  // Interaction: expand first item, then make a decision
  const interaction = await page.evaluate(async () => {
    const head = document.querySelector('.dr-item-head');
    if (!head) return { ok: false, reason: 'no item head' };
    head.click();
    await new Promise(r => setTimeout(r, 100));
    const detail = document.querySelector('.dr-item .dr-detail');
    const expanded = head.getAttribute('aria-expanded') === 'true' && detail && !detail.hidden;

    const decideBtn = document.querySelector('.dr-item [data-decide="approve"]');
    if (!decideBtn) return { ok: true, expanded };
    decideBtn.click();
    await new Promise(r => setTimeout(r, 100));
    const after = document.querySelector('.dr-item .dr-after');
    const decided = after && after.classList.contains('active');
    const pill = document.querySelector('.dr-item .dr-pill');
    return { ok: true, expanded, decided, pillText: pill ? pill.textContent : '' };
  });

  console.log(JSON.stringify({ wall, errors, checks, interaction }, null, 2));
  await browser.close();
})().catch(e => { console.error('FATAL', e); process.exit(1); });
