'use strict';
const puppeteer=require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const path=require('path'),fs=require('fs');
const DIR='/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype';
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const out=path.join(DIR,'.workbuddy','tmp','verify-shots');
fs.mkdirSync(out,{recursive:true});
const pages=['business','calendar','finance','knowledge','meeting','founding-flow'];
(async()=>{
  const browser=await puppeteer.launch({executablePath:CHROME,headless:'new',
    defaultViewport:{width:1440,height:900},
    args:['--no-proxy-server','--no-sandbox','--disable-setuid-sandbox','--disable-dev-shm-usage','--allow-file-access-from-files']});
  for(const name of pages){
    const page=await browser.newPage();
    await page.setRequestInterception(true);
    page.on('request',r=>{const u=r.url(); if(u.startsWith('http')) r.abort().catch(()=>{}); else r.continue().catch(()=>{});});
    try{ await page.goto('file://'+path.join(DIR,name+'.html'),{waitUntil:'domcontentloaded',timeout:30000}); }catch(e){}
    await new Promise(r=>setTimeout(r,500));
    const probe=await page.evaluate(()=>{
      const cs=getComputedStyle(document.body), rs=getComputedStyle(document.documentElement);
      const g=n=>rs.getPropertyValue(n).trim();
      return {bodyBg:cs.backgroundColor,bodyColor:cs.color,uiBg:g('--ui-bg'),
        bgAlias:g('--bg-base-default')||g('--bg'),primary:g('--primary')||g('--accent')};
    });
    console.log(name.padEnd(16),JSON.stringify(probe));
    await page.screenshot({path:path.join(out,name+'.png')});
    await page.close();
  }
  await browser.close();
  console.log('shots ->',out);
})().catch(e=>{console.error('ERR',e.message);process.exit(1);});
