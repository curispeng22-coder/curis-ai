const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const fs = require('fs'); const path = require('path');
const DIR = path.resolve(__dirname, '../..');
(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new', defaultViewport: { width: 1440, height: 900 },
    args: ['--no-proxy-server','--no-sandbox','--disable-setuid-sandbox','--allow-file-access-from-files']
  });
  for (const f of (process.argv.slice(2).length?process.argv.slice(2):['workspace-shell-reference.html'])) {
    const page = await browser.newPage();
    await page.setRequestInterception(true);
    page.on('request', r => { r.url().startsWith('http') ? r.abort().catch(()=>{}) : r.continue().catch(()=>{}); });
    await page.goto('file://' + path.join(DIR, f), { waitUntil:'domcontentloaded' });
    await new Promise(r=>setTimeout(r,400));
    const res = await page.evaluate(() => {
      const vw = window.innerWidth;
      const out = [];
      document.querySelectorAll('*').forEach(el => {
        const s = getComputedStyle(el);
        if (s.display==='none'||s.visibility==='hidden') return;
        const r = el.getBoundingClientRect();
        if (r.right > vw + 1) out.push({ t: el.tagName.toLowerCase(), c:(el.className.baseVal!==undefined?el.className.baseVal:el.className||'').toString().slice(0,40), right: Math.round(r.right), w: Math.round(r.width) });
      });
      // 去重按 right 降序取前 12
      out.sort((a,b)=>b.right-a.right);
      return { vw, docScrollW: document.documentElement.scrollWidth, items: out.slice(0,12) };
    });
    console.log(`\n=== ${f} (vw=${res.vw}, docScrollW=${res.docScrollW}) ===`);
    res.items.forEach(i => console.log(`  <${i.t}>.${i.c}  right=${i.right} width=${i.w}`));
    await page.close();
  }
  await browser.close();
})();
