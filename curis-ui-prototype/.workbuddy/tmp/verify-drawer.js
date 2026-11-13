const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PROTO = '/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype';
const FILES = ['ceo-desk.html','operating.html','decision-room.html','business.html'];

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
    const res = await page.evaluate(async () => {
      const d = document.getElementById('assistant-drawer');
      if (!d) return { drawer: false };
      const before = { role: d.getAttribute('role'), ariaModal: d.getAttribute('aria-modal'), ariaHidden: d.getAttribute('aria-hidden') };
      // open it via the FAB
      const fab = document.getElementById('assistant-fab') || document.querySelector('.assistant-fab');
      let opened = null;
      if (fab) { fab.click(); await new Promise(r => setTimeout(r, 120)); }
      opened = { role: d.getAttribute('role'), ariaModal: d.getAttribute('aria-modal'), ariaHidden: d.getAttribute('aria-hidden'), hasOpenClass: d.classList.contains('open') };
      return { drawer: true, before, opened };
    });
    console.log(f, JSON.stringify(res));
    await page.close();
  }
  await browser.close();
})().catch(e => { console.error('FATAL', e); process.exit(1); });
