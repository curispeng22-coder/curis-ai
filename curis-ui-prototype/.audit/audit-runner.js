/* Curis UI runtime audit — one browser per page, incremental save. */
const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const fs = require('fs');
const path = require('path');

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const ROOT = '/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype';
const OUT = '/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype/.audit/2026-08-04';
fs.mkdirSync(OUT, { recursive: true });

const PAGES = [
  'ceo-desk.html','operating.html','business.html','ai-organization.html',
  'workspace-portal.html','workspace-studio.html','founding-flow.html','decision-room.html',
  'meeting.html','finance.html','knowledge.html','calendar.html','assets.html',
  'workspace-runtime-software.html','workspace-runtime-xhs.html','workspace-runtime-shortvideo.html',
  'workspace-runtime-department.html'
];

async function probe(page){
  return await page.evaluate(() => {
    const q = s => document.querySelectorAll(s);
    const one = s => document.querySelector(s);
    const color = (sel) => { const el = one(sel); if(!el) return null; const cs=getComputedStyle(el); return {bg: cs.backgroundColor, color: cs.color}; };
    const shell = one('.curis-shell, .shell, .app-shell, .app, .curis-app, [class*="shell"]');
    let shellInfo = null;
    if (shell) {
      const r = shell.getBoundingClientRect(); const cs = getComputedStyle(shell);
      shellInfo = { cls: shell.className.toString().slice(0,40), display: cs.display, cols: cs.gridTemplateColumns, w: Math.round(r.width), h: Math.round(r.height), childCount: shell.children.length };
      const sidebar = shell.querySelector('.curis-sidebar, .sidebar');
      const main = shell.querySelector('.curis-main, .main');
      if (sidebar) shellInfo.sidebarW = Math.round(sidebar.getBoundingClientRect().width);
      if (main) { const mr = main.getBoundingClientRect(); shellInfo.mainX = Math.round(mr.x); shellInfo.mainW = Math.round(mr.width); shellInfo.mainY = Math.round(mr.y); }
      shellInfo.scrollW = document.documentElement.scrollWidth;
    }
    return {
      btnPrimary: q('.btn-primary').length,
      primaryClass: q('button.primary, a.primary').length,
      fab: !!one('#assistant-fab'),
      companion: !!one('#curis-companion'),
      askFab: q('.ask-fab').length,
      drawerBare: !!one('#drawer'),
      assistantDrawer: !!one('#assistant-drawer'),
      badge: !!one('.mock-badge[data-curis-auto]'),
      shell: shellInfo,
      cBody: color('body'),
      cTopbar: color('.curis-topbar, .topbar'),
      cSidebar: color('.curis-sidebar, .sidebar'),
      cCard: color('.card'),
      theme: document.documentElement.getAttribute('data-theme') || '(none)'
    };
  });
}

async function load(page, file, theme, osScheme){
  await page.evaluateOnNewDocument((t) => { try{ localStorage.setItem('curis-theme', t); }catch(e){} }, theme);
  await page.emulateMediaFeatures([{ name:'prefers-color-scheme', value: osScheme }]);
  const url = 'file://' + path.join(ROOT, file);
  await page.goto(url, { waitUntil:'domcontentloaded', timeout:30000 });
  try { await page.waitForSelector('#assistant-fab', { timeout:8000 }); } catch(e){}
  await new Promise(r=>setTimeout(r, 1200));
}

async function run(){
  console.log('AUDIT START', PAGES.length, 'pages');
  const results = {};
  for (const file of PAGES){
    results[file] = {};
    const browser = await puppeteer.launch({ executablePath: CHROME, headless:'new',
      args:['--no-proxy-server','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--force-device-scale-factor=1'] });
    try {
      const page = await browser.newPage();
      await page.setViewport({ width:1440, height:900, deviceScaleFactor:1 });
      await page.setRequestInterception(true);
      page.on('request', req => { if(req.url().startsWith('file://')) req.continue(); else req.abort(); });
      const consoleErr = [];
      page.on('console', m => { if(m.type()==='error') consoleErr.push(m.text().slice(0,160)); });
      page.on('pageerror', e => consoleErr.push('PAGEERR: '+String(e).slice(0,160)));

      await load(page, file, 'dark', 'dark');
      results[file].dark = await probe(page);
      await page.screenshot({ path: path.join(OUT, file.replace('.html','')+'-dark.png') });

      await load(page, file, 'light', 'light');
      results[file].light = await probe(page);
      await page.screenshot({ path: path.join(OUT, file.replace('.html','')+'-light.png') });

      if (['ceo-desk.html','workspace-portal.html','founding-flow.html','calendar.html','workspace-studio.html'].includes(file)){
        await load(page, file, 'system', 'light');
        results[file].systemLight = await probe(page);
        await load(page, file, 'system', 'dark');
        results[file].systemDark = await probe(page);
      }
      results[file].consoleErr = consoleErr.slice(0,6);
    } catch(e){
      results[file].error = String(e).slice(0,200);
    } finally {
      try { await browser.close(); } catch(e){}
    }
    fs.writeFileSync(path.join(OUT,'results.json'), JSON.stringify(results, null, 2));
    console.log('done', file);
  }
  console.log('ALL DONE');
}
run().catch(e=>{ console.error('FATAL', e); process.exit(1); });
