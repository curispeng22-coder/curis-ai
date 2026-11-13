/* 剩余 8 项（P0-3/P0-4/P1-2/P1-4/P2-1/P2-2/P2-5/P3）真实 Chrome 基线探针 */
const puppeteer = require('/Users/yy/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '../..');
const PAGES = fs.readdirSync(ROOT).filter(f => f.endsWith('.html')).sort();

// 违禁词：产品术语必须本地化（用户可见文案中不得出现）
const BANNED = ['Agent', 'ROI', 'KPI', 'Workspace', 'Runtime', 'Studio', 'Blueprint',
  'Outcome', 'Evidence', 'Owner', 'Canvas', 'Dashboard', 'Pipeline', 'Token'];

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new',
    defaultViewport: { width: 1440, height: 900 },
    args: ['--no-proxy-server', '--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--allow-file-access-from-files']
  });

  const report = {};
  const allFontSizes = {};
  const allBanned = {};

  for (const p of PAGES) {
    const page = await browser.newPage();
    const external = [];
    await page.setRequestInterception(true);
    page.on('request', r => {
      const u = r.url();
      if (/^https?:/i.test(u)) { external.push(u); return r.abort().catch(() => {}); }
      r.continue().catch(() => {});
    });
    try {
      await page.goto('file://' + path.join(ROOT, p), { waitUntil: 'domcontentloaded', timeout: 30000 });
    } catch (e) {}
    await new Promise(r => setTimeout(r, 600));

    const data = await page.evaluate((BANNED) => {
      const vis = el => {
        const s = getComputedStyle(el);
        if (s.display === 'none' || s.visibility === 'hidden' || +s.opacity === 0) return false;
        const r = el.getBoundingClientRect();
        return r.width > 0 && r.height > 0;
      };

      // --- P0-4 dialog / aria-modal ---
      const ariaModal = document.querySelectorAll('[aria-modal]').length;
      const roleDialog = document.querySelectorAll('[role="dialog"]').length;

      // --- P1-2 字阶 ---
      const sizes = {};
      let tiny = 0;
      document.querySelectorAll('*').forEach(el => {
        if (!el.textContent || !el.textContent.trim()) return;
        // 仅统计直接含文本的叶子节点
        const hasText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
        if (!hasText || !vis(el)) return;
        const fs2 = Math.round(parseFloat(getComputedStyle(el).fontSize) * 10) / 10;
        sizes[fs2] = (sizes[fs2] || 0) + 1;
        if (fs2 < 12) tiny++;
      });

      // --- P1-4 违禁词（可见文本） ---
      const hits = {};
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      let n;
      while ((n = walker.nextNode())) {
        const t = n.textContent.trim();
        if (!t) continue;
        const el = n.parentElement;
        if (!el || !vis(el)) continue;
        BANNED.forEach(w => {
          const re = new RegExp('\\b' + w + '\\b', 'i');
          if (re.test(t)) {
            hits[w] = hits[w] || [];
            if (hits[w].length < 3) hits[w].push(t.slice(0, 60));
          }
        });
      }

      // --- P2-1 内容区出口（非导航区的可跳转链接） ---
      const main = document.querySelector('main, .main, .content, .page-content') || document.body;
      const outlets = [...main.querySelectorAll('a[href]')].filter(a => {
        if (a.closest('.sidebar, nav, .curis-nav-section, .topbar')) return false;
        const h = a.getAttribute('href') || '';
        return h && h !== '#' && !h.startsWith('javascript:') && vis(a);
      }).length;

      // --- P2-2 导航常驻项 ---
      const navSections = [...document.querySelectorAll('.curis-nav-section')];
      const navItems = document.querySelectorAll('.curis-nav-section a').length;
      const navGroups = navSections.map(s => {
        const label = (s.querySelector('.nav-section-label, .curis-nav-label') || {}).textContent || '';
        return { label: label.trim(), items: s.querySelectorAll('a').length };
      });

      // --- P2-5 死按钮（可见 button 无 onclick/无 data-action/无 form/无 href） ---
      const dead = [];
      document.querySelectorAll('button, [role="button"]').forEach(b => {
        if (!vis(b)) return;
        const hasHandler = b.onclick || b.getAttribute('onclick') ||
          b.dataset.action || b.dataset.nav || b.dataset.target || b.dataset.tab ||
          b.getAttribute('type') === 'submit' || b.closest('a[href]') ||
          b.id || b.className.match(/tab|toggle|close|nav|filter|menu|expand|collapse/i);
        if (!hasHandler) dead.push((b.textContent || '').trim().slice(0, 30) || '[空]');
      });

      // --- P3 首屏密度 ---
      const firstScreen = [...document.querySelectorAll('body *')].filter(el => {
        if (!vis(el)) return false;
        const r = el.getBoundingClientRect();
        return r.top < 900 && r.bottom > 0 && r.left < 1440;
      }).length;

      return { ariaModal, roleDialog, sizes, tiny, hits, outlets, navItems, navGroups, dead, firstScreen };
    }, BANNED);

    report[p] = { external: external.length, externalUrls: external.slice(0, 5), ...data };
    Object.entries(data.sizes).forEach(([k, v]) => { allFontSizes[k] = (allFontSizes[k] || 0) + v; });
    Object.entries(data.hits).forEach(([k, v]) => {
      allBanned[k] = allBanned[k] || { pages: [], samples: [] };
      allBanned[k].pages.push(p);
      if (allBanned[k].samples.length < 3) allBanned[k].samples.push(...v.slice(0, 1));
    });
    await page.close();
  }

  await browser.close();

  console.log('=== P0-3 外部请求 ===');
  const extTotal = Object.values(report).reduce((a, r) => a + r.external, 0);
  console.log('总计:', extTotal, extTotal === 0 ? '✅' : '❌');
  Object.entries(report).filter(([, r]) => r.external).forEach(([p, r]) => console.log(' ', p, r.external, r.externalUrls.join(',')));

  console.log('\n=== P0-4 aria-modal / role=dialog ===');
  Object.entries(report).filter(([, r]) => r.ariaModal || r.roleDialog)
    .forEach(([p, r]) => console.log(' ', p, 'aria-modal=' + r.ariaModal, 'role=dialog=' + r.roleDialog));
  const amTotal = Object.values(report).reduce((a, r) => a + r.ariaModal, 0);
  console.log('aria-modal 总计:', amTotal, amTotal === 0 ? '✅' : '❌');

  console.log('\n=== P1-2 字阶 ===');
  const sorted = Object.entries(allFontSizes).sort((a, b) => +a[0] - +b[0]);
  console.log('档位数:', sorted.length, sorted.length <= 7 ? '✅' : '❌');
  console.log(sorted.map(([k, v]) => `${k}px×${v}`).join('  '));
  const tinyTotal = Object.values(report).reduce((a, r) => a + r.tiny, 0);
  console.log('<12px 节点:', tinyTotal, tinyTotal === 0 ? '✅' : '❌');
  Object.entries(report).filter(([, r]) => r.tiny).forEach(([p, r]) => console.log('  ', p, r.tiny));

  console.log('\n=== P1-4 违禁术语 ===');
  const bkeys = Object.keys(allBanned);
  console.log('命中词种类:', bkeys.length, bkeys.length === 0 ? '✅' : '❌');
  bkeys.forEach(k => console.log(' ', k, '→', allBanned[k].pages.length + '页', '|', allBanned[k].samples.join(' / ')));

  console.log('\n=== P2-1 内容区出口 ===');
  const zero = Object.entries(report).filter(([, r]) => r.outlets === 0);
  console.log('0 出口页:', zero.length, zero.length === 0 ? '✅' : '❌');
  Object.entries(report).forEach(([p, r]) => console.log(' ', p.padEnd(36), r.outlets));

  console.log('\n=== P2-2 导航结构 ===');
  const sample = Object.entries(report)[0];
  console.log('导航项总数:', sample[1].navItems);
  console.log('分组:', JSON.stringify(sample[1].navGroups));

  console.log('\n=== P2-5 死按钮 ===');
  const deadTotal = Object.values(report).reduce((a, r) => a + r.dead.length, 0);
  console.log('总计:', deadTotal, deadTotal === 0 ? '✅' : '❌');
  Object.entries(report).filter(([, r]) => r.dead.length).forEach(([p, r]) => console.log(' ', p, r.dead.join(' | ')));

  console.log('\n=== P3 首屏密度 ===');
  Object.entries(report).sort((a, b) => b[1].firstScreen - a[1].firstScreen)
    .forEach(([p, r]) => console.log(' ', p.padEnd(36), r.firstScreen, (r.firstScreen >= 150 && r.firstScreen <= 220) ? '✅' : '❌'));

  fs.writeFileSync(path.join(__dirname, 'baseline-remaining.json'), JSON.stringify(report, null, 2));
})();
