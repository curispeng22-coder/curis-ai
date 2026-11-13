const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const fs = require('fs'); const path = require('path');
const DIR = path.resolve(__dirname, '../..');
(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new', defaultViewport: { width: 1440, height: 900 },
    args: ['--no-proxy-server','--no-sandbox','--disable-setuid-sandbox','--allow-file-access-from-files']
  });
  for (const f of ['workspace-shell-reference.html','ai-organization.html','workspace-studio.html']) {
    const page = await browser.newPage();
    await page.setRequestInterception(true);
    page.on('request', r => { r.url().startsWith('http') ? r.abort().catch(()=>{}) : r.continue().catch(()=>{}); });
    await page.goto('file://' + path.join(DIR, f), { waitUntil:'domcontentloaded' });
    await new Promise(r=>setTimeout(r,400));
    const res = await page.evaluate(() => {
      const beforeX = window.scrollX;
      window.scrollTo(500, 0);           // 尝试横向滚动
      const afterX = window.scrollX;
      const canHScroll = afterX > beforeX + 1;
      window.scrollTo(0,0);
      return { docScrollW: document.documentElement.scrollWidth, clientW: document.documentElement.clientWidth, scrollXattempt: afterX, canHScroll, bodyOverflowX: getComputedStyle(document.body).overflowX, htmlOverflowX: getComputedStyle(document.documentElement).overflowX };
    });
    console.log(`${f}: docScrollW=${res.docScrollW} clientW=${res.clientW} 尝试横向scrollX=${res.scrollXattempt} 可横向滚动=${res.canHScroll} (bodyX=${res.bodyOverflowX}, htmlX=${res.htmlOverflowX})`);
    await page.close();
  }
  await browser.close();
})();
