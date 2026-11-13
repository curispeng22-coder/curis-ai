const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const fs = require('fs');
const path = require('path');
const DIR = '/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype';
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

const files = fs.readdirSync(DIR).filter(f => f.endsWith('.html') && !fs.statSync(path.join(DIR,f)).isDirectory());

(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless:'new', defaultViewport:{width:1440,height:900},
    args:['--no-proxy-server','--no-sandbox','--disable-setuid-sandbox','--disable-dev-shm-usage','--allow-file-access-from-files'] });

  const report = [];
  for (const f of files) {
    const page = await browser.newPage();
    await page.setRequestInterception(true);
    page.on('request', r => { const u=r.url(); if (u.startsWith('http')) r.abort().catch(()=>{}); else r.continue().catch(()=>{}); });
    try {
      await page.goto('file://'+path.join(DIR,f), {waitUntil:'domcontentloaded', timeout:30000});
    } catch(e) {}
    await new Promise(r=>setTimeout(r,350));
    const res = await page.evaluate(() => {
      function lum(rgb) {
        const [r,g,b] = rgb.map(v => { v/=255; return v<=0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055,2.4); });
        return 0.2126*r + 0.7152*g + 0.0722*b;
      }
      function parseColor(s) {
        s = (s||'').trim();
        if (s.startsWith('rgb')) { const m = s.match(/rgba?\(([^)]+)\)/); const p = m[1].split(',').map(x=>parseFloat(x)); return [p[0],p[1],p[2], p[3]===undefined?1:p[3]]; }
        return null;
      }
      function contrast(fg, bg) { const L1=lum(fg),L2=lum(bg); const hi=Math.max(L1,L2),lo=Math.min(L1,L2); return (hi+0.05)/(lo+0.05); }
      function parseColor(s) {
        s = (s||'').trim();
        if (s.startsWith('rgb')) { const m = s.match(/rgba?\(([^)]+)\)/); const p = m[1].split(',').map(x=>parseFloat(x)); return [p[0],p[1],p[2], p[3]===undefined?1:p[3]]; }
        return null;
      }
      // Composite translucent backgrounds over ancestors → true painted color behind text.
      function compositedBg(el) {
        const layers = [];
        let n = el;
        while (n && n !== document.documentElement) {
          const cs = getComputedStyle(n);
          const bg = parseColor(cs.backgroundColor);
          if (bg && bg[3] > 0) layers.push(bg);
          n = n.parentElement;
        }
        const bodyBg = parseColor(getComputedStyle(document.body).backgroundColor);
        if (bodyBg && bodyBg[3] > 0) layers.push(bodyBg);
        if (layers.length === 0) return [255,255,255];
        // Paint order: outermost first, inner on top. layers[0]=innermost.
        let acc = null;
        for (let i = layers.length - 1; i >= 0; i--) {
          const [r,g,b,a] = layers[i];
          if (!acc) { acc = [r,g,b]; continue; }
          acc = [ r*a + acc[0]*(1-a), g*a + acc[1]*(1-a), b*a + acc[2]*(1-a) ];
        }
        return acc || [255,255,255];
      }
      const out = { checked:0, fails:0, samples:[] };
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
      let node;
      while ((node = walker.nextNode())) {
        const txt = node.textContent || '';
        if (!txt.trim()) continue;
        const el = node.parentElement;
        if (!el) continue;
        const cs = getComputedStyle(el);
        if (cs.visibility === 'hidden' || cs.display === 'none') continue;
        const rect = el.getBoundingClientRect();
        if (rect.width === 0 && rect.height === 0) continue;
        const fg = parseColor(cs.color);
        const bg = compositedBg(el);
        if (!fg || fg[3] < 0.5) continue;
        out.checked++;
        const ratio = contrast(fg.slice(0,3), bg.slice(0,3));
        const px = parseFloat(cs.fontSize);
        const bold = parseInt(cs.fontWeight) >= 700;
        const large = px >= 24 || (px >= 18.66 && bold);
        const threshold = large ? 3 : 4.5;
        if (ratio < threshold) {
          out.fails++;
          if (out.samples.length < 4) out.samples.push({ txt: txt.trim().slice(0,24), fg: cs.color, bg: 'rgb('+bg.map(Math.round).join(',')+')', ratio:+ratio.toFixed(2), px:+px.toFixed(1), bold, threshold });
        }
      }
      return out;
    });
    await page.close();
    report.push({ file: f, ...res });
  }
  await browser.close();

  let totalChecked = 0, totalFails = 0;
  console.log('=== WCAG Contrast Audit (per-element, effective bg) ===');
  for (const r of report) {
    totalChecked += r.checked; totalFails += r.fails;
    const flag = r.fails > 0 ? '⚠' : '✓';
    console.log(`${flag} ${r.file.padEnd(26)} checked=${String(r.checked).padStart(4)} fails=${String(r.fails).padStart(3)}`);
    for (const s of r.samples) console.log(`     └ "${s.txt}"  ${s.fg} on ${s.bg}  ratio=${s.ratio} (${s.px}px ${s.bold?'bold':'reg'}, need ${s.threshold})`);
  }
  console.log(`\nTOTAL  checked=${totalChecked}  fails=${totalFails}  (${(totalFails/totalChecked*100).toFixed(1)}% of nodes)`);
})().catch(e=>{console.error('FATAL',e);process.exit(1);});
