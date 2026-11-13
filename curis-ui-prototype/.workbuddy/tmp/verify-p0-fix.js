const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PROTO = '/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype';
const FILES = ['finance.html', 'ceo-desk.html', 'operating.html', 'decision-room.html'];

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: 'new',
    defaultViewport: { width: 1440, height: 900 },
    args: ['--no-proxy-server', '--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--allow-file-access-from-files']
  });
  const results = {};
  for (const f of FILES) {
    const page = await browser.newPage();
    const errs = [];
    page.on('pageerror', e => errs.push('PAGEERR: ' + e.message));
    page.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE: ' + m.text()); });
    await page.setRequestInterception(true);
    page.on('request', r => { const u = r.url(); if (u.startsWith('http')) r.abort().catch(() => {}); else r.continue().catch(() => {}); });
    const t0 = Date.now();
    await page.goto('file://' + PROTO + '/' + f, { waitUntil: 'domcontentloaded', timeout: 15000 });
    // give JS time to settle; if stuck in a loop this will not resolve quickly
    await new Promise(r => setTimeout(r, 600));
    const wall = Date.now() - t0;
    // probe responsiveness: can we still evaluate after the settlement window?
    let probe;
    try {
      probe = await page.evaluate(() => {
        const out = { responsive: true };
        const root = document.querySelector('[data-finance-page]');
        if (root) {
          const strong = root.querySelector('.summary .metric strong');
          out.financeMetric = strong ? strong.textContent : '(no metric node)';
          const rows = root.querySelectorAll('.table .row').length;
          out.financeRows = rows;
        }
        // count how many iterations update() ran by checking a sentinel we can mutate?
        // Instead: ensure page is not frozen by measuring a trivial eval roundtrip.
        out.title = document.title;
        return out;
      });
    } catch (e) {
      probe = { responsive: false, error: e.message };
    }
    results[f] = { wallMs: wall, errors: errs.slice(0, 5), probe };
    await page.close();
  }
  await browser.close();

  // check tokens.css for @import
  const fs = require('fs');
  const css = fs.readFileSync(PROTO + '/_system/tokens.css', 'utf8');
  const hasImport = /@import\s+url\(/i.test(css);

  console.log(JSON.stringify({ hasFontImport: hasImport, pages: results }, null, 2));
})().catch(e => { console.error('FATAL', e); process.exit(1); });
