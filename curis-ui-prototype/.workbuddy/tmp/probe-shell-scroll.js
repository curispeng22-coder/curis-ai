/* 诊断 runtime 页 App Shell 的滚动链路 */
const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const path = require('path');
const DIR = path.resolve(__dirname, '../..');
const PAGES = ['workspace-runtime-software.html', 'workspace-studio.html'];

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new', defaultViewport: { width: 1440, height: 900 },
    args: ['--no-proxy-server', '--no-sandbox', '--disable-setuid-sandbox', '--allow-file-access-from-files']
  });
  for (const f of PAGES) {
    for (const shrink of [false, true]) {
      const page = await browser.newPage();
      await page.setRequestInterception(true);
      page.on('request', r => { r.url().startsWith('http') ? r.abort().catch(()=>{}) : r.continue().catch(()=>{}); });
      try { await page.goto('file://' + path.join(DIR, f), { waitUntil: 'domcontentloaded', timeout: 30000 }); } catch (e) {}
      if (shrink) {
        // 把字阶还原到收敛前的旧值，判断溢出是否由本轮字号提升引入
        await page.addStyleTag({ content: ':root{--ui-fs-1:10px;--ui-fs-2:11px;--ui-fs-3:13px;--ui-fs-4:15px;--ui-fs-5:18px;--ui-fs-6:22px;--ui-fs-7:28px}' });
      }
      await new Promise(r => setTimeout(r, 500));
      const res = await page.evaluate(() => {
        const b = document.body;
        const chain = [];
        [...b.children].forEach(el => {
          const s = getComputedStyle(el);
          chain.push({ t: el.tagName.toLowerCase(), c: (el.className||'').toString().slice(0,28),
            h: Math.round(el.getBoundingClientRect().height), sh: el.scrollHeight, ch: el.clientHeight,
            ov: s.overflowY, hgt: s.height });
        });
        return { bodyOver: b.scrollHeight - b.clientHeight, bodyClient: b.clientHeight, chain };
      });
      await page.close();
      console.log(`\n${f}  [${shrink ? '旧字阶' : '新字阶'}]  body 溢出=${res.bodyOver}px  (可视 ${res.bodyClient}px)`);
      res.chain.forEach(c => console.log(`   <${c.t}>.${c.c.padEnd(28)} h=${String(c.h).padStart(5)} scrollH=${String(c.sh).padStart(5)} clientH=${String(c.ch).padStart(5)} overflowY=${c.ov} css-height=${c.hgt}`));
    }
  }
  await browser.close();
})();
