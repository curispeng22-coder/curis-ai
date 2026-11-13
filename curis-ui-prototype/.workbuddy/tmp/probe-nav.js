const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const fs = require('fs'); const path = require('path');
const DIR = path.resolve(__dirname, '../..');
(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new', defaultViewport: { width: 1440, height: 900 },
    args: ['--no-proxy-server','--no-sandbox','--disable-setuid-sandbox','--allow-file-access-from-files']
  });
  for (const f of ['operating.html','finance.html','workspace-runtime-software.html']) {
    const page = await browser.newPage();
    await page.setRequestInterception(true);
    page.on('request', r => { r.url().startsWith('http') ? r.abort().catch(()=>{}) : r.continue().catch(()=>{}); });
    await page.goto('file://' + path.join(DIR, f), { waitUntil:'domcontentloaded' });
    await new Promise(r=>setTimeout(r,500));
    const before = await page.evaluate(() => {
      const pers = document.querySelectorAll('.curis-primary-nav .nav-item').length;
      const toggle = document.querySelector('.nav-more-toggle');
      const panel = document.querySelector('.nav-more-panel');
      return { persistent: pers, toggleExists: !!toggle, expanded: toggle?toggle.getAttribute('aria-expanded'):null, panelHidden: panel?panel.hidden:null, panelItems: panel?panel.querySelectorAll('.nav-item').length:0, total: document.querySelectorAll('.sidebar .nav-item, aside .nav-item').length };
    });
    // 点击展开
    await page.evaluate(() => { const t=document.querySelector('.nav-more-toggle'); if(t) t.click(); });
    await new Promise(r=>setTimeout(r,200));
    const after = await page.evaluate(() => {
      const panel = document.querySelector('.nav-more-panel');
      return { panelHidden: panel?panel.hidden:null, panelItems: panel?panel.querySelectorAll('.nav-item').length:0, expanded: document.querySelector('.nav-more-toggle')?.getAttribute('aria-expanded') };
    });
    console.log(`${f}: 常驻=${before.persistent} 折叠默认展开=${before.expanded} 折叠项(展开后)=${after.panelItems} (total nav-item=${before.total})`);
    await page.close();
  }
  await browser.close();
})();
