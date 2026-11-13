/* 定位档外字号的具体节点与来源 */
const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const fs = require('fs'); const path = require('path');
const DIR = path.resolve(__dirname, '../..');
const OK = [12, 13, 14, 16, 20, 24, 28];
const files = fs.readdirSync(DIR).filter(f => f.endsWith('.html')).sort();

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new', defaultViewport: { width: 1440, height: 900 },
    args: ['--no-proxy-server', '--no-sandbox', '--disable-setuid-sandbox', '--allow-file-access-from-files']
  });
  const agg = {};
  for (const f of files) {
    const page = await browser.newPage();
    await page.setRequestInterception(true);
    page.on('request', r => { r.url().startsWith('http') ? r.abort().catch(()=>{}) : r.continue().catch(()=>{}); });
    try { await page.goto('file://' + path.join(DIR, f), { waitUntil: 'domcontentloaded', timeout: 30000 }); } catch (e) {}
    await new Promise(r => setTimeout(r, 500));
    const out = await page.evaluate((OK) => {
      const res = [];
      const vis = el => { const s = getComputedStyle(el); if (s.display==='none'||s.visibility==='hidden') return false;
        const r = el.getBoundingClientRect(); return r.width>0 && r.height>0; };
      document.querySelectorAll('*').forEach(el => {
        const hasText = [...el.childNodes].some(n => n.nodeType===3 && n.textContent.trim());
        if (!hasText || !vis(el)) return;
        const px = Math.round(parseFloat(getComputedStyle(el).fontSize)*10)/10;
        if (OK.includes(px)) return;
        res.push({ px, tag: el.tagName.toLowerCase(),
          cls: (el.className && el.className.baseVal !== undefined ? el.className.baseVal : el.className || '').toString().slice(0,50),
          inline: (el.getAttribute('style')||'').slice(0,70),
          txt: (el.textContent||'').trim().slice(0,26) });
      });
      return res;
    }, OK);
    out.forEach(o => {
      const k = o.px + '|' + o.tag + '|' + o.cls;
      agg[k] = agg[k] || { ...o, n: 0, pages: new Set() };
      agg[k].n++; agg[k].pages.add(f);
    });
    await page.close();
  }
  await browser.close();
  Object.values(agg).sort((a,b)=>b.n-a.n).forEach(v =>
    console.log(`${String(v.px).padStart(5)}px ×${String(v.n).padStart(3)}  <${v.tag}> .${v.cls}  | ${v.pages.size}页 | style="${v.inline}" | "${v.txt}"`));
})();
