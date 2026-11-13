const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PROTO = '/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype';
const FILES = ['workspace-portal.html','ceo-desk.html','founding-flow.html','workspace-studio.html','business.html','operating.html','ai-organization.html'];

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: 'new',
    defaultViewport: { width: 1440, height: 900 },
    args: ['--no-proxy-server', '--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--allow-file-access-from-files']
  });
  const out = {};
  for (const f of FILES) {
    const page = await browser.newPage();
    let cdnReq = 0;
    const errs = [];
    page.on('request', r => { if (/cdn\.jsdelivr|unpkg\.com|@tailwindcss/.test(r.url())) cdnReq++; });
    page.on('pageerror', e => errs.push('PAGEERR: ' + e.message));
    page.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE: ' + m.text()); });
    await page.setRequestInterception(true);
    page.on('request', (r) => { const u = r.url(); if (u.startsWith('http')) r.abort().catch(() => {}); else r.continue().catch(() => {}); });
    const t0 = Date.now();
    await page.goto('file://' + PROTO + '/' + f, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await new Promise(r => setTimeout(r, 500));
    const probe = await page.evaluate(() => {
      const nav = document.querySelector('.nav-list') || document.querySelector('aside.sidebar .nav-item');
      const navCount = document.querySelectorAll('.nav-item, .nav-list .nav-item, aside.sidebar .nav-item').length;
      const cards = document.querySelectorAll('.card').length;
      const main = document.querySelector('.content, main, .main-area .content');
      const mainH = main ? Math.round(main.getBoundingClientRect().height) : 0;
      const card0 = document.querySelector('.card');
      const cardBg = card0 ? getComputedStyle(card0).backgroundColor : null;
      const bodyBg = getComputedStyle(document.body).backgroundColor;
      return { navCount, cards, mainH, cardBg, bodyBg, title: document.title };
    });
    out[f] = { wallMs: Date.now() - t0, cdnRequests: cdnReq, errors: errs.slice(0,4), probe };
    await page.close();
  }
  await browser.close();
  console.log(JSON.stringify(out, null, 2));
})().catch(e => { console.error('FATAL', e); process.exit(1); });
