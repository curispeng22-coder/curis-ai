const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const fs = require('fs'); const path = require('path');
const DIR = path.resolve(__dirname, '../..');
(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new', defaultViewport: { width: 1440, height: 900 },
    args: ['--no-proxy-server','--no-sandbox','--disable-setuid-sandbox','--allow-file-access-from-files']
  });
  for (const f of ['workspace-runtime-software.html','workspace-runtime-xhs.html','workspace-studio.html','business.html']) {
    const page = await browser.newPage();
    await page.setRequestInterception(true);
    page.on('request', r => { r.url().startsWith('http') ? r.abort().catch(()=>{}) : r.continue().catch(()=>{}); });
    await page.goto('file://' + path.join(DIR, f), { waitUntil:'domcontentloaded' });
    await new Promise(r=>setTimeout(r,400));
    const res = await page.evaluate(() => {
      const content = document.querySelector('.content, .curis-content');
      const sidebar = document.querySelector('.sidebar, .curis-sidebar');
      let contentScrolls = false, sidebarStays = false;
      if (content) {
        const before = content.scrollTop;
        content.scrollTop = 400;
        contentScrolls = (content.scrollTop - before) > 50;
        content.scrollTop = 0;
      }
      if (sidebar) {
        const t0 = sidebar.getBoundingClientRect().top;
        if (content) { content.scrollTop = 400; }
        const t1 = sidebar.getBoundingClientRect().top;
        sidebarStays = Math.abs(t1 - t0) < 2;
        if (content) content.scrollTop = 0;
      }
      return { hasContent: !!content, contentScrolls, hasSidebar: !!sidebar, sidebarStays };
    });
    console.log(`${f}: 内容可滚动=${res.contentScrolls} 侧栏固定=${res.sidebarStays} (content=${res.hasContent}, sidebar=${res.hasSidebar})`);
    await page.close();
  }
  await browser.close();
})();
