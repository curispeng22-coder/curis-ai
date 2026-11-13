const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const FILE = '/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype/decision-room.html';
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless:'new', defaultViewport:{width:1440,height:900},
    args:['--no-proxy-server','--no-sandbox','--disable-setuid-sandbox','--disable-dev-shm-usage','--allow-file-access-from-files'] });
  const page = await browser.newPage();
  await page.setRequestInterception(true);
  page.on('request', r=>{ const u=r.url(); if(u.startsWith('http')) r.abort().catch(()=>{}); else r.continue().catch(()=>{}); });
  await page.goto('file://'+FILE,{waitUntil:'domcontentloaded',timeout:30000});
  await new Promise(r=>setTimeout(r,500));
  const r = await page.evaluate(async ()=>{
    const out={};
    document.querySelector('.dr-item-head').click();
    await new Promise(x=>setTimeout(x,60));
    // option select
    const opt=document.querySelector('.dr-item .dr-option');
    opt.click();
    await new Promise(x=>setTimeout(x,40));
    out.optionSelected = opt.classList.contains('selected');
    // sim tab
    const tabs=document.querySelectorAll('.dr-item .dr-sim-tab');
    if(tabs[1]){ tabs[1].click(); await new Promise(x=>setTimeout(x,40)); out.simSwitched = tabs[1].classList.contains('active'); }
    // decide
    const btn=document.querySelector('.dr-item [data-decide="approve"]');
    btn.click();
    await new Promise(x=>setTimeout(x,60));
    out.afterActive = !!document.querySelector('.dr-item .dr-after.active');
    out.traceLen = (document.querySelector('.dr-item .trace')||{innerHTML:''}).innerHTML.length;
    // does #inbox have a click listener? indirectly test by checking if option click worked (proves delegation)
    return out;
  });
  console.log(JSON.stringify(r,null,2));
  await browser.close();
})().catch(e=>{console.error('FATAL',e);process.exit(1);});
