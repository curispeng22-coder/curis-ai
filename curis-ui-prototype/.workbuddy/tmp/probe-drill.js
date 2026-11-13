const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const fs = require('fs'); const path = require('path');
const DIR = path.resolve(__dirname, '../..');
(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new', defaultViewport: { width: 1440, height: 900 },
    args: ['--no-proxy-server','--no-sandbox','--disable-setuid-sandbox','--allow-file-access-from-files']
  });
  for (const f of fs.readdirSync(DIR).filter(x=>x.endsWith('.html')).sort()) {
    const page = await browser.newPage();
    await page.setRequestInterception(true);
    page.on('request', r => { r.url().startsWith('http') ? r.abort().catch(()=>{}) : r.continue().catch(()=>{}); });
    await page.goto('file://' + path.join(DIR, f), { waitUntil:'domcontentloaded' });
    await new Promise(r=>setTimeout(r,400));
    const res = await page.evaluate(() => {
      // 内容区 = main / .main / .content / .curis-content，排除侧栏
      const isNav = el => el.closest('aside, .sidebar, .curis-canonical-sidebar-main, .nav, nav, .curis-nav-section, .nav-footer');
      const contentHosts = document.querySelectorAll('main, .main, .content, .curis-content, article, .page');
      let internal = 0, sample = [];
      document.querySelectorAll('a[href]').forEach(a => {
        const h = a.getAttribute('href') || '';
        if (/^[^#?].*\.html(#.*)?$/.test(h) && h.indexOf('http')!==0) {
          if (!isNav(a)) { internal++; if(sample.length<4) sample.push(h); }
        }
      });
      return { internal, sample };
    });
    const flag = res.internal ? '✓' : '✗';
    console.log(`${flag} ${f.padEnd(34)} 内容区内链=${String(res.internal).padStart(2)}  ${res.sample.join(', ')}`);
    await page.close();
  }
  await browser.close();
})();
