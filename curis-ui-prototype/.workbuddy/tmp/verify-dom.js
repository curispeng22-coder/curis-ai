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
  const r = await page.evaluate(()=>{
    const item = document.querySelector('.dr-item');
    const head = item.querySelector('.dr-item-head');
    const opt = item.querySelector('.dr-option');
    // simulate head expand
    head.setAttribute('aria-expanded','true');
    item.querySelector('.dr-detail').hidden = false;
    const res = {
      itemClass: item.className,
      itemDataId: item.dataset.id,
      optInbox: !!opt.closest('#inbox'),
      optClosestItem: opt.closest('.dr-item') === item,
      optClosestHead: !!opt.closest('.dr-item-head'),
      optClosestOpt: !!opt.closest('.dr-option'),
      // manually run the handler logic
      manual: (function(){
        var e = { target: opt };
        var head = e.target.closest('.dr-item-head');
        var o = e.target.closest('.dr-option');
        return { headNull: !head, oFound: !!o };
      })(),
      inboxListenerProbe: (function(){
        // add a probe listener to confirm bubbling
        var got = false;
        document.getElementById('inbox').addEventListener('click', function(){ got = true; }, { once:true });
        opt.dispatchEvent(new MouseEvent('click', { bubbles:true }));
        return got;
      })(),
      optSelectedAfterProbe: opt.classList.contains('selected')
    };
    return res;
  });
  console.log(JSON.stringify(r,null,2));
  await browser.close();
})().catch(e=>{console.error('FATAL',e);process.exit(1);});
