const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const fs = require('fs'); const path = require('path');
const DIR = path.resolve(__dirname, '../..');
(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new', defaultViewport: { width: 1440, height: 900 },
    args: ['--no-proxy-server','--no-sandbox','--disable-setuid-sandbox','--allow-file-access-from-files']
  });
  const page = await browser.newPage();
  await page.setRequestInterception(true);
  page.on('request', r => { r.url().startsWith('http') ? r.abort().catch(()=>{}) : r.continue().catch(()=>{}); });
  const f = process.argv[2] || 'ai-organization.html';
  await page.goto('file://' + path.join(DIR, f), { waitUntil:'domcontentloaded' });
  await new Promise(r=>setTimeout(r,400));
  const info = await page.evaluate(() => {
    const html = document.documentElement, body = document.body;
    const sh = getComputedStyle(html), sb = getComputedStyle(body);
    // deepest visible in-flow element
    let cand=[]; document.querySelectorAll('body *').forEach(el=>{const s=getComputedStyle(el);if(s.display==='none'||s.visibility==='hidden')return;const r=el.getBoundingClientRect();if(r.height>0)cand.push({el,b:r.bottom,pos:s.position});});
    cand.sort((a,b)=>b.b-a.b);
    const deep=cand[0];
    const before=window.scrollY;
    window.scrollTo(0, 99999);
    const after=window.scrollY;
    return {
      htmlOverflow: sh.overflow+'/'+sh.overflowY, htmlHeight: sh.height,
      bodyOverflow: sb.overflow+'/'+sb.overflowY, bodyHeight: sb.height,
      docScrollH: html.scrollHeight, docClientH: html.clientHeight,
      winScrollable: html.scrollHeight - html.clientHeight,
      before, after, moved: after>before+1,
      deepestTag: deep?deep.el.tagName.toLowerCase():'?',
      deepestClass: deep?(deep.el.className.baseVal!==undefined?deep.el.className.baseVal:deep.el.className||'').toString().slice(0,40):'?',
      deepestPos: deep?deep.pos:'?', deepestBottom: deep?Math.round(deep.b):0
    };
  });
  console.log(JSON.stringify(info,null,2));
  await browser.close();
})();
