/* Re-probe finance + targeted token-resolution check on a few pages. */
const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const fs = require('fs');
const path = require('path');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const ROOT = '/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype';
const OUT = '/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype/.audit/2026-08-04';

async function probeTokens(page){
  return await page.evaluate(() => {
    const root = document.documentElement;
    const cs = getComputedStyle(root);
    const bodyCs = getComputedStyle(document.body);
    return {
      uiBg: cs.getPropertyValue('--ui-bg').trim(),
      uiSurface: cs.getPropertyValue('--ui-surface').trim(),
      uiAccent: cs.getPropertyValue('--ui-accent').trim(),
      bgBaseDefault: cs.getPropertyValue('--bg-base-default').trim(),
      bg: cs.getPropertyValue('--bg').trim(),
      statusPrimary: cs.getPropertyValue('--status-primary').trim(),
      accent: cs.getPropertyValue('--accent').trim(),
      bodyBg: bodyCs.backgroundColor,
      dataTheme: root.getAttribute('data-theme'),
      globalLayer: !!document.getElementById('curis-global-layer'),
      frozenPatch: !!document.getElementById('curis-frozen-patch'),
      neutral: !!document.body.dataset.curisNeutral,
      btnPrimary: document.querySelectorAll('.btn-primary').length,
      primaryClass: document.querySelectorAll('button.primary, a.primary').length,
      fab: !!document.getElementById('assistant-fab'),
      badge: !!document.querySelector('.mock-badge[data-curis-auto]'),
    };
  });
}

async function runOne(file){
  const browser = await puppeteer.launch({ executablePath: CHROME, headless:'new',
    args:['--no-proxy-server','--no-sandbox','--disable-gpu','--disable-dev-shm-usage'] });
  try {
    const page = await browser.newPage();
    await page.setViewport({ width:1440, height:900 });
    await page.setRequestInterception(true);
    page.on('request', req => { if(req.url().startsWith('file://')) req.continue(); else req.abort(); });
    await page.evaluateOnNewDocument(() => { try{ localStorage.setItem('curis-theme','dark'); }catch(e){} });
    await page.emulateMediaFeatures([{ name:'prefers-color-scheme', value:'dark' }]);
    await page.goto('file://'+path.join(ROOT,file), { waitUntil:'domcontentloaded', timeout:30000 });
    try { await page.waitForSelector('#assistant-fab', { timeout:8000 }); } catch(e){}
    await new Promise(r=>setTimeout(r,1200));
    const res = await probeTokens(page);
    await page.screenshot({ path: path.join(OUT, file.replace('.html','')+'-dark.png') });
    return res;
  } finally { try{ await browser.close(); }catch(e){} }
}

(async () => {
  const out = {};
  for (const f of ['ceo-desk.html','calendar.html','workspace-studio.html','ai-organization.html','workspace-runtime-software.html']){
    out[f] = await runOne(f);
    console.log('done', f, JSON.stringify(out[f]));
  }
  fs.writeFileSync(path.join(OUT,'tokens-probe.json'), JSON.stringify(out, null, 2));
  console.log('ALL DONE');
})().catch(e=>{ console.error('FATAL',e); process.exit(1); });
