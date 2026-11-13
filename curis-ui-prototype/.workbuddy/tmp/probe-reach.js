/* 内容可达性 / 滚动链探针 — 断言 App Shell 正确：
   - html 无纵向溢出（scrollHeight <= innerHeight）
   - html 无横向溢出（scrollWidth <= innerWidth）
   - 存在有效滚动容器（overflowY auto/scroll 且 scrollHeight>clientHeight）=> 内容可达
*/
const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const fs = require('fs'); const path = require('path');
const DIR = path.resolve(__dirname, '../..');
const targets = process.argv.slice(2);
const files = (targets.length ? targets : fs.readdirSync(DIR).filter(f => f.endsWith('.html'))).sort();

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new', defaultViewport: { width: 1440, height: 900 },
    args: ['--no-proxy-server', '--no-sandbox', '--disable-setuid-sandbox', '--allow-file-access-from-files']
  });
  let bad = 0;
  for (const f of files) {
    const page = await browser.newPage();
    await page.setRequestInterception(true);
    page.on('request', r => { r.url().startsWith('http') ? r.abort().catch(()=>{}) : r.continue().catch(()=>{}); });
    try { await page.goto('file://' + path.join(DIR, f), { waitUntil: 'domcontentloaded', timeout: 30000 }); } catch (e) {}
    await new Promise(r => setTimeout(r, 400));
    const res = await page.evaluate(() => {
      const vw = window.innerWidth, vh = window.innerHeight;
      const de = document.documentElement;
      const bodyV = de.scrollHeight - vh;       // 纵向溢出
      const bodyH = de.scrollWidth - vw;        // 横向溢出
      // 找有效滚动容器
      let scrollers = 0, topScroller = null;
      document.querySelectorAll('*').forEach(el => {
        const s = getComputedStyle(el);
        const sy = s.overflowY, oa = (sy === 'auto' || sy === 'scroll');
        if (oa && (el.scrollHeight - el.clientHeight > 2)) {
          scrollers++;
          if (!topScroller) topScroller = { t: el.tagName.toLowerCase(), c: (el.className.baseVal!==undefined?el.className.baseVal:el.className||'').toString().slice(0,30), sh: el.scrollHeight, ch: el.clientHeight };
        }
      });
      // 最深的可见内容底边
      let deepest = 0;
      document.querySelectorAll('*').forEach(el => {
        const s = getComputedStyle(el); if (s.display==='none'||s.visibility==='hidden') return;
        const b = el.getBoundingClientRect().bottom;
        if (b > deepest) deepest = b;
      });
      return { vh, vw, bodyV, bodyH, scrollers, topScroller, deepest };
    });
    const ok = (res.bodyV <= 2 && res.bodyH <= 2 && res.scrollers > 0);
    if (!ok) bad++;
    const flag = ok ? '✓' : '✗';
    console.log(`${flag} ${f.padEnd(34)} 纵向溢出=${String(res.bodyV).padStart(4)}px 横向溢出=${String(res.bodyH).padStart(4)}px 滚动器=${res.scrollers} 最深底边=${Math.round(res.deepest)} (视口${res.vh})` + (res.topScroller?`  首滚器=<${res.topScroller.t}>.${res.topScroller.c}`:''));
    await page.close();
  }
  await browser.close();
  console.log(`\n不可达/溢出页 = ${bad}`);
  process.exit(bad ? 1 : 0);
})();
