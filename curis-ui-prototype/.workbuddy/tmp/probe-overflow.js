/* 字号提升后的溢出 / 裁切检测 */
const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const fs = require('fs'); const path = require('path');
const DIR = path.resolve(__dirname, '../..');
const files = fs.readdirSync(DIR).filter(f => f.endsWith('.html')).sort();

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new', defaultViewport: { width: 1440, height: 900 },
    args: ['--no-proxy-server', '--no-sandbox', '--disable-setuid-sandbox', '--allow-file-access-from-files']
  });
  let grand = 0;
  for (const f of files) {
    const page = await browser.newPage();
    await page.setRequestInterception(true);
    page.on('request', r => { r.url().startsWith('http') ? r.abort().catch(()=>{}) : r.continue().catch(()=>{}); });
    try { await page.goto('file://' + path.join(DIR, f), { waitUntil: 'domcontentloaded', timeout: 30000 }); } catch (e) {}
    await new Promise(r => setTimeout(r, 500));
    const res = await page.evaluate(() => {
      const out = [];
      const vis = el => { const s = getComputedStyle(el); if (s.display==='none'||s.visibility==='hidden') return false;
        const r = el.getBoundingClientRect(); return r.width>0 && r.height>0; };
      document.querySelectorAll('*').forEach(el => {
        if (!vis(el)) return;
        const s = getComputedStyle(el);
        const clips = s.overflow==='hidden'||s.overflowX==='hidden'||s.overflowY==='hidden';
        const ellipsis = s.textOverflow === 'ellipsis';
        // 被裁掉的内容（排除刻意的单行省略号）
        const overX = el.scrollWidth  - el.clientWidth;
        const overY = el.scrollHeight - el.clientHeight;
        if (clips && !ellipsis && (overX > 2 || overY > 2)) {
          out.push({ t: el.tagName.toLowerCase(),
            c: (el.className.baseVal !== undefined ? el.className.baseVal : el.className||'').toString().slice(0,40),
            overX, overY, txt: (el.textContent||'').trim().slice(0,30) });
        }
      });
      // 横向溢出视口
      const bodyOver = document.documentElement.scrollWidth - document.documentElement.clientWidth;
      return { out, bodyOver };
    });
    grand += res.out.length;
    const flag = (res.out.length || res.bodyOver > 2) ? '⚠' : '✓';
    console.log(`${flag} ${f.padEnd(36)} 裁切=${String(res.out.length).padStart(3)}  横向溢出=${res.bodyOver}px`);
    res.out.slice(0, 4).forEach(o => console.log(`     <${o.t}>.${o.c} +${o.overX}x +${o.overY}y "${o.txt}"`));
    await page.close();
  }
  await browser.close();
  console.log(`\nTOTAL 裁切节点 = ${grand}`);
})();
