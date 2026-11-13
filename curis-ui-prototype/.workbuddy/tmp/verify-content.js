const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PROTO = '/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype';
const FILES = ['workspace-portal.html','workspace-studio.html','business.html'];

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: 'new',
    defaultViewport: { width: 1440, height: 900 },
    args: ['--no-proxy-server', '--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--allow-file-access-from-files']
  });
  for (const f of FILES) {
    const page = await browser.newPage();
    await page.setRequestInterception(true);
    page.on('request', r => { const u = r.url(); if (u.startsWith('http')) r.abort().catch(() => {}); else r.continue().catch(() => {}); });
    await page.goto('file://' + PROTO + '/' + f, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await new Promise(r => setTimeout(r, 500));
    const info = await page.evaluate(() => {
      const body = document.body;
      // find the largest visible block element as a proxy for "content area"
      const all = [...document.querySelectorAll('div, section, main, article')];
      let maxH = 0, maxSel = '';
      for (const el of all) {
        const r = el.getBoundingClientRect();
        if (r.height > maxH) { maxH = Math.round(r.height); maxSel = el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).split(' ')[0] : ''); }
      }
      return {
        bodyScrollH: document.documentElement.scrollHeight,
        bodyInnerTextLen: body.innerText.trim().length,
        largestBlock: maxSel + ' = ' + maxH + 'px',
        sidebarExists: !!document.querySelector('aside.sidebar, .sidebar, .nav-list'),
        hasVisibleContent: body.innerText.trim().length > 50
      };
    });
    console.log(f, JSON.stringify(info));
    await page.close();
  }
  await browser.close();
})().catch(e => { console.error('FATAL', e); process.exit(1); });
