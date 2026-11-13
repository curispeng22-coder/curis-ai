const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const FILE = '/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype/decision-room.html';
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', defaultViewport:{width:1440,height:900},
    args:['--no-proxy-server','--no-sandbox','--disable-setuid-sandbox','--disable-dev-shm-usage','--allow-file-access-from-files'] });
  const page = await browser.newPage();
  const errs=[];
  page.on('pageerror', e=>errs.push('PAGEERR: '+e.message));
  page.on('console', m=>{ if(m.type()==='error') errs.push('CONSOLE: '+m.text()); });
  await page.setRequestInterception(true);
  page.on('request', r=>{ const u=r.url(); if(u.startsWith('http')) r.abort().catch(()=>{}); else r.continue().catch(()=>{}); });
  await page.goto('file://'+FILE,{waitUntil:'domcontentloaded',timeout:30000});
  await new Promise(r=>setTimeout(r,500));
  const dbg = await page.evaluate(async ()=>{
    const head = document.querySelector('.dr-item-head');
    head.click();
    await new Promise(r=>setTimeout(r,80));
    const btn = document.querySelector('.dr-item [data-decide="approve"]');
    let clickErr=null;
    try { btn.click(); } catch(e){ clickErr = e.message; }
    await new Promise(r=>setTimeout(r,120));
    const after = document.querySelector('.dr-item .dr-after');
    return {
      btnFound: !!btn,
      btnDisabled: btn? btn.disabled : null,
      clickErr,
      afterExists: !!after,
      afterClass: after? after.className : null,
      afterActive: after? after.classList.contains('active') : null,
      trace: document.querySelector('.dr-item .trace') ? document.querySelector('.dr-item .trace').innerHTML.slice(0,60) : null
    };
  });
  console.log(JSON.stringify({errs, dbg},null,2));
  await browser.close();
})().catch(e=>{console.error('FATAL',e);process.exit(1);});
