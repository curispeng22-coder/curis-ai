const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const DIR='/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype';
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
(async()=>{
  const b=await puppeteer.launch({executablePath:CHROME,headless:'new',defaultViewport:{width:1440,height:900},args:['--no-proxy-server','--no-sandbox','--disable-setuid-sandbox','--disable-dev-shm-usage','--allow-file-access-from-files']});
  const p=await b.newPage(); await p.setRequestInterception(true);
  p.on('request',r=>{const u=r.url(); if(u.startsWith('http'))r.abort().catch(()=>{});else r.continue().catch(()=>{});});
  await p.goto('file://'+DIR+'/ai-organization.html',{waitUntil:'domcontentloaded',timeout:30000});
  await new Promise(r=>setTimeout(r,400));
  const res=await p.evaluate(()=>{
    const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,null); let n,out=[];
    while((n=w.nextNode())){ if(n.textContent.trim()==='+'){ const e=n.parentElement; const cs=getComputedStyle(e);
      out.push({tag:e.tagName,cls:e.className,color:cs.color,bg:cs.backgroundColor,chain:(function(){let a=[],x=e;while(x&&x!==document.body){a.push(x.tagName+'.'+(typeof x.className==='string'?x.className.split(' ').join('.'):''));x=x.parentElement;}return a.slice(0,5);})()}); } }
    return out;
  });
  console.log(JSON.stringify(res,null,2)); await b.close();
})().catch(e=>{console.error('FATAL',e);process.exit(1);});
