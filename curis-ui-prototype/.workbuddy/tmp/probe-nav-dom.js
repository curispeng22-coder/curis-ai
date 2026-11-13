'use strict';
const puppeteer=require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const path=require('path');
const DIR='/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype';
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const targets=['business.html','workspace-portal.html','ai-organization.html','ceo-desk.html'];
(async function(){
  const browser=await puppeteer.launch({executablePath:CHROME,headless:'new',
    defaultViewport:{width:1440,height:900},
    args:['--no-proxy-server','--no-sandbox','--disable-setuid-sandbox','--disable-dev-shm-usage','--allow-file-access-from-files']});
  for(const f of targets){
    const page=await browser.newPage();
    var errs=[];
    page.on('pageerror',function(e){errs.push(e.message);});
    page.on('console',function(m){ if(m.type()==='error') errs.push('console: '+m.text()); });
    await page.setRequestInterception(true);
    page.on('request',function(r){var u=r.url(); if(u.startsWith('http')) r.abort().catch(function(){}); else r.continue().catch(function(){});});
    try{ await page.goto('file://'+path.join(DIR,f),{waitUntil:'domcontentloaded',timeout:30000}); }catch(e){}
    await new Promise(function(r){setTimeout(r,900);});
    const info=await page.evaluate(function(){
      var asideSb=document.querySelector('aside.sidebar');
      var anySb=document.querySelector('.sidebar');
      var sb=asideSb||anySb;
      return {
        hasAsideSidebar: !!asideSb,
        sidebarTag: sb?sb.tagName.toLowerCase():null,
        sidebarClass: sb?sb.className:null,
        canonicalFlag: sb?sb.dataset.curisCanonicalNav:null,
        childTags: sb?[].slice.call(sb.children).map(function(c){return c.tagName.toLowerCase()+'.'+(c.className||'').split(' ')[0];}):[],
        navItemCount: sb?sb.querySelectorAll('a.nav-item').length:0,
        sectionCount: sb?sb.querySelectorAll('.curis-nav-section').length:0,
        visibleWidth: sb?sb.getBoundingClientRect().width:0,
        innerLen: sb?sb.innerHTML.length:0,
        firstText: sb?(sb.textContent||'').replace(/\s+/g,' ').trim().slice(0,120):''
      };
    });
    console.log('\n=== '+f+' ===');
    console.log(JSON.stringify(info,null,2));
    if(errs.length) console.log('PAGE ERRORS:',errs.slice(0,5));
    await page.close();
  }
  await browser.close();
})().catch(function(e){console.error('ERR',e.message);process.exit(1);});
