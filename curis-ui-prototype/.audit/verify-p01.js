/* Verify P0-1 / P1-1 fix: probe 3 pages × 3 theme modes. */
const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const path = require('path');
const fs = require('fs');

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const ROOT = '/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype';
const OUT = '/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype/.audit/2026-08-04';
const PAGES = ['ceo-desk.html', 'workspace-portal.html', 'workspace-studio.html'];

async function probe(page) {
  return await page.evaluate(() => {
    const cs = getComputedStyle(document.documentElement);
    const bodyCs = getComputedStyle(document.body);
    const one = s => document.querySelector(s);
    const color = sel => { const el = one(sel); if(!el) return null; const c = getComputedStyle(el); return {bg: c.backgroundColor, color: c.color}; };
    return {
      dataTheme: document.documentElement.getAttribute('data-theme'),
      hasDarkClass: document.documentElement.classList.contains('dark'),
      uiBg: cs.getPropertyValue('--ui-bg').trim(),
      uiAccent: cs.getPropertyValue('--ui-accent').trim(),
      bgBaseDefault: cs.getPropertyValue('--bg-base-default').trim(),
      statusPrimary: cs.getPropertyValue('--status-primary').trim(),
      bodyBg: bodyCs.backgroundColor,
      bodyColor: bodyCs.color,
      cTopbar: color('.curis-topbar, .topbar'),
      cSidebar: color('.curis-sidebar, .sidebar'),
      cCard: color('.card'),
      btnPrimary: document.querySelectorAll('.btn-primary').length,
      primaryClass: document.querySelectorAll('button.primary, a.primary').length,
      fab: !!document.getElementById('assistant-fab'),
      badge: !!document.querySelector('.mock-badge[data-curis-auto]'),
      companion: !!document.getElementById('curis-companion'),
      askFab: document.querySelectorAll('.ask-fab').length,
      drawerBare: !!document.getElementById('drawer'),
    };
  });
}

async function load(page, file, theme, osScheme) {
  await page.evaluateOnNewDocument((t) => {
    try { localStorage.setItem('curis-theme', t); } catch(e) {}
  }, theme);
  await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: osScheme }]);
  await page.goto('file://' + path.join(ROOT, file), { waitUntil: 'domcontentloaded', timeout: 30000 });
  try { await page.waitForSelector('#assistant-fab', { timeout: 8000 }); } catch(e) {}
  await new Promise(r => setTimeout(r, 1500));
}

async function run() {
  const results = {};
  for (const file of PAGES) {
    results[file] = {};
    const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new',
      args: ['--no-proxy-server', '--no-sandbox', '--disable-gpu', '--force-device-scale-factor=1'] });
    try {
      const page = await browser.newPage();
      await page.setViewport({ width: 1440, height: 900 });
      await page.setRequestInterception(true);
      page.on('request', req => { if (req.url().startsWith('file://')) req.continue(); else req.abort(); });

      await load(page, file, 'dark', 'dark');
      results[file].dark = await probe(page);

      await load(page, file, 'light', 'light');
      results[file].light = await probe(page);

      await load(page, file, 'system', 'light');
      results[file].systemLight = await probe(page);

      await load(page, file, 'system', 'dark');
      results[file].systemDark = await probe(page);
    } catch (e) {
      results[file].error = String(e).slice(0, 200);
    } finally {
      await browser.close();
    }
    console.log('done', file);
  }
  fs.writeFileSync(path.join(OUT, 'verify-p01.json'), JSON.stringify(results, null, 2));
  console.log('DONE');
}
run().catch(e => { console.error('FATAL', e); process.exit(1); });
