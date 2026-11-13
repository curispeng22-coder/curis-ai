/* 决定性可达性探针：对「最深的可见元素」做真实滚动测试，
   判定其是否可被用户滚动到（无论靠 window 还是内层滚动容器）。*/
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
      const vh = window.innerHeight, vw = window.innerWidth;
      const vis = el => { const s = getComputedStyle(el); if (s.display==='none'||s.visibility==='hidden'||s.opacity==='0') return false; const r = el.getBoundingClientRect(); return r.width>0 && r.height>0; };
      // 收集可见、在普通文档流中的深层元素（排除 fixed/absolute 离屏浮层）
      let cand = [];
      document.querySelectorAll('body *').forEach(el => {
        if (!vis(el)) return;
        const s = getComputedStyle(el);
        if (s.position === 'fixed' || s.position === 'absolute') {
          const r = el.getBoundingClientRect();
          if (r.top > vh || r.bottom < 0 || r.left > vw || r.right < 0) return;
        }
        cand.push(el);
      });
      cand.sort((a,b) => b.getBoundingClientRect().bottom - a.getBoundingClientRect().bottom);
      const deep = cand[0];
      if (!deep) return { ok:true, note:'empty' };
      const deepBottom = deep.getBoundingClientRect().bottom;
      // 若首屏已容纳，直接 OK
      if (deepBottom <= vh + 2) return { ok:true, deepest: Math.round(deepBottom), note:'fits' };
      // 找最近滚动祖先
      const nearestScroller = (el) => {
        let n = el.parentElement;
        while (n && n !== document.documentElement) {
          const s = getComputedStyle(n);
          if (s.overflowY === 'auto' || s.overflowY === 'scroll' || s.overflowY === 'overlay') return n;
          n = n.parentElement;
        }
        return null; // 用 window
      };
      const sc = nearestScroller(deep);
      let reachable;
      if (sc) {
        const before = sc.scrollTop;
        sc.scrollTop = sc.scrollHeight;
        reachable = (sc.scrollHeight - sc.clientHeight - sc.scrollTop) <= 2;
        sc.scrollTop = before;
      } else {
        const before = window.scrollY;
        window.scrollTo(0, deepBottom + 99999);
        reachable = window.scrollY > before + 1;
        window.scrollTo(0, 0);
      }
      return { ok: reachable, deepest: Math.round(deepBottom), scroller: sc ? (sc.tagName.toLowerCase()+'.'+(sc.className.baseVal!==undefined?sc.className.baseVal:sc.className||'').toString().slice(0,24)) : 'window' };
    });
    if (!res.ok) bad++;
    const flag = res.ok ? '✓' : '✗';
    console.log(`${flag} ${f.padEnd(34)} 最深底边=${String(res.deepest).padStart(5)} (视口900) ` + (res.scroller?`滚动容器=${res.scroller}`:'') + (res.note?` [${res.note}]`:''));
    await page.close();
  }
  await browser.close();
  console.log(`\n真正不可达页 = ${bad}`);
  process.exit(bad ? 1 : 0);
})();
