'use strict';
const puppeteer=require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const DIR='/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype';
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const files=fs.readdirSync(DIR).filter(function(f){return f.endsWith('.html');});
(async function(){
  const browser=await puppeteer.launch({executablePath:CHROME,headless:'new',
    defaultViewport:{width:1440,height:900},
    args:['--no-proxy-server','--no-sandbox','--disable-setuid-sandbox','--disable-dev-shm-usage','--allow-file-access-from-files']});
  const rows=[];
  for(const f of files){
    const page=await browser.newPage();
    await page.setRequestInterception(true);
    page.on('request',function(r){var u=r.url(); if(u.startsWith('http')) r.abort().catch(function(){}); else r.continue().catch(function(){});});
    try{ await page.goto('file://'+path.join(DIR,f),{waitUntil:'domcontentloaded',timeout:30000}); }catch(e){}
    await new Promise(function(r){setTimeout(r,700);});
    const info=await page.evaluate(function(){
      var sb=document.querySelector('aside.sidebar')||document.querySelector('.sidebar');
      if(!sb) return {none:true};
      var tag=sb.tagName.toLowerCase();
      var canonical=sb.dataset.curisCanonicalNav==='true';
      var groups=[].slice.call(sb.querySelectorAll('.curis-nav-section')).map(function(s){
        var lbl=s.querySelector('.nav-label');
        var label=lbl?lbl.textContent.trim():'';
        var items=[].slice.call(s.querySelectorAll('a.nav-item')).map(function(a){
          var t=a.querySelector('span:not(.nav-icon):not(.nav-badge)');
          return ((t?t.textContent:a.textContent)||'').trim()+'|'+a.getAttribute('href');
        });
        return label+'::'+items.join(',');
      });
      var footer=[].slice.call(sb.querySelectorAll('.curis-canonical-footer a.nav-item')).map(function(a){return a.textContent.trim();});
      var allItems=[].slice.call(sb.querySelectorAll('a.nav-item')).map(function(a){return a.getAttribute('href');});
      return {tag:tag,canonical:canonical,groups:groups,footer:footer,count:allItems.length};
    });
    if(info.none){ rows.push({f:f,sig:'NO-SIDEBAR',count:0,canonical:false,groups:[],tag:'-'}); }
    else {
      var sig=crypto.createHash('sha1').update(JSON.stringify(info.groups)+'|'+JSON.stringify(info.footer)).digest('hex').slice(0,10);
      rows.push({f:f,sig:sig,count:info.count,canonical:info.canonical,tag:info.tag,groups:info.groups});
    }
    await page.close();
  }
  await browser.close();
  var bySig={};
  rows.forEach(function(r){(bySig[r.sig]=bySig[r.sig]||[]).push(r);});
  console.log('=== NAV SIGNATURE GROUPS ===');
  Object.entries(bySig).sort(function(a,b){return b[1].length-a[1].length;}).forEach(function(pair){
    var sig=pair[0],list=pair[1];
    console.log('\n['+sig+'] x'+list.length+'  items='+list[0].count+' canonical='+list[0].canonical+' tag='+list[0].tag);
    list.forEach(function(r){console.log('   '+r.f);});
    if(list[0].groups&&list[0].groups.length) list[0].groups.forEach(function(g){console.log('     - '+g);});
  });
  console.log('\nTOTAL distinct signatures = '+Object.keys(bySig).length);
  fs.writeFileSync(path.join(DIR,'.workbuddy','tmp','nav-sig.json'),JSON.stringify(rows,null,2));
})().catch(function(e){console.error('ERR',e.message);process.exit(1);});
