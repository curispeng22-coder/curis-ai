const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const fs = require('fs'); const path = require('path');
const DIR = path.resolve(__dirname, '../..');
(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new', defaultViewport: { width: 1440, height: 900 },
    args: ['--no-proxy-server','--no-sandbox','--disable-setuid-sandbox','--allow-file-access-from-files']
  });
  for (const f of ['workspace-runtime-software.html','workspace-runtime-shortvideo.html','workspace-runtime-department.html','workspace-runtime-xhs.html','business.html','operating.html']) {
    const page = await browser.newPage();
    await page.setRequestInterception(true);
    page.on('request', r => { r.url().startsWith('http') ? r.abort().catch(()=>{}) : r.continue().catch(()=>{}); });
    await page.goto('file://' + path.join(DIR, f), { waitUntil:'domcontentloaded' });
    await new Promise(r=>setTimeout(r,400));
    const res = await page.evaluate(() => {
      const vh = window.innerHeight;
      let first = 0, totalVis = 0, cards = 0;
      document.querySelectorAll('body *').forEach(el => {
        const s = getComputedStyle(el);
        if (s.display==='none'||s.visibility==='hidden'||s.opacity==='0') return;
        const r = el.getBoundingClientRect();
        if (r.width<=0||r.height<=0) return;
        totalVis++;
        if (r.top < vh && r.bottom > 0) first++;
        if (/card|tile|item|chip|pill|tag|row|cell|node|block/i.test(el.className.baseVal!==undefined?el.className.baseVal:el.className||'')) cards++;
      });
      return { first, totalVis, cards };
    });
    console.log(`${f.padEnd(34)} 首屏可见元素=${String(res.first).padStart(4)}  全页可见=${res.totalVis}  类含(card等)=${res.cards}`);
    await page.close();
  }
  await browser.close();
})();
