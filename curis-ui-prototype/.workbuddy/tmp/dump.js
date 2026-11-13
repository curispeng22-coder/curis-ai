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
  await new Promise(r=>setTimeout(r,400));
  const html = await page.evaluate(()=>{
    const item=document.querySelector('.dr-item');
    // build parent chain of first .dr-option
    const opt=item.querySelector('.dr-option');
    const chain=[]; let n=opt; while(n && n!==item){ chain.push(n.tagName+'.'+(n.className||'')); n=n.parentElement; }
    return { chain, headOuter: item.querySelector('.dr-item-head').outerHTML.slice(0,400) };
  });
  console.log(JSON.stringify(html,null,2));
  await browser.close();
})().catch(e=>{console.error('FATAL',e);process.exit(1);});
