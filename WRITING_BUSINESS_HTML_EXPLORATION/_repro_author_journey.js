/* CURIS — Writing Business HTML Exploration · 本轮 P0 基线复现（作者主路径与员工协作）
   目的：在实施任何修订之前，用真实 Chrome 复现 CEO/Codex 反馈的三项缺陷，
         并把「修前」状态留成基线证据。
   运行：node _repro_author_journey.js
   产出：_evidence_author_journey/_baseline_repro/（截图 + BASELINE_REPRO.md）
   ========================================================================== */
'use strict';
const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');
const os = require('os');
const http = require('http');

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const ROOT = __dirname;
const EV = path.join(ROOT, '_evidence_author_journey', '_baseline_repro');
fs.mkdirSync(EV, { recursive: true });

const errors = [];
const findings = [];
let seq = 0;

function note(id, title, detail) {
  findings.push({ id, title, detail: detail == null ? '' : String(detail) });
  console.log('\n### ' + id + ' ' + title + (detail ? '\n    ' + String(detail).replace(/\n/g, '\n    ') : ''));
}
const wait = (ms) => new Promise(r => setTimeout(r, ms));

const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.png': 'image/png' };
function serve() {
  return new Promise((resolve) => {
    const s = http.createServer((req, res) => {
      const p = decodeURIComponent(req.url.split('?')[0]);
      if (p === '/favicon.ico') { res.writeHead(204); return res.end(); }
      const f = path.join(ROOT, p === '/' ? 'index.html' : p);
      if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end('404'); }
      res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' });
      fs.createReadStream(f).pipe(res);
    });
    s.listen(0, '127.0.0.1', () => resolve(s));
  });
}
async function shot(page, tag) {
  seq++;
  const f = path.join(EV, String(seq).padStart(2, '0') + '-' + tag + '.png');
  await page.screenshot({ path: f });
  return path.basename(f);
}
async function mainText(page) { return (await page.$eval('#main', e => e.innerText)).trim(); }
async function count(page, sel) { return page.evaluate(s => document.querySelectorAll(s).length, sel); }
async function clickFn(page, fn, attrs) {
  const hit = await page.evaluate((fn, attrs) => {
    const els = Array.from(document.querySelectorAll('[data-fn="' + fn + '"]'));
    const el = els.filter(e => (attrs || []).every(([k, v]) => e.getAttribute('data-' + k) === String(v)))[0] || els[0];
    if (!el) return null;
    el.click();
    return (el.innerText || el.textContent || '').trim();
  }, fn, attrs || []);
  await wait(260);
  return hit;
}
async function clickAct(page, action, attrs) {
  return page.evaluate((action, attrs) => {
    const els = Array.from(document.querySelectorAll('[data-action="' + action + '"]'));
    const el = els.filter(e => (attrs || []).every(([k, v]) => e.getAttribute('data-' + k) === String(v)))[0] || els[0];
    if (!el) return null;
    el.click();
    return (el.innerText || el.textContent || '').trim();
  }, action, attrs || []).then(async (r) => { await wait(280); return r; });
}
async function setInput(page, sel, text) {
  await page.evaluate((s, t) => {
    const e = document.querySelector(s);
    if (e) { e.value = t; e.dispatchEvent(new Event('input', { bubbles: true })); }
  }, sel, text);
  await wait(100);
}

const SEED = '我想写一部近未来悬疑小说，档案员收到明天的报纸。请先与我讨论两种故事方向，不要写正文。';

(async () => {
  const server = await serve();
  const url = 'http://127.0.0.1:' + server.address().port + '/index.html';
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'curis-authorjourney-repro-'));
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: 'new', userDataDir: profile,
    protocolTimeout: 30000, args: ['--no-proxy-server', '--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  page.on('console', m => { if (m.type() === 'error' && !/favicon/.test(m.location() ? (m.location().url || '') : '')) errors.push(m.text()); });
  page.on('pageerror', e => errors.push('pageerror: ' + String((e && e.message) || e)));
  await page.setViewport({ width: 1440, height: 1000 });
  await page.goto(url, { waitUntil: 'load', timeout: 30000 });
  await page.waitForSelector('#nav .nav-item', { timeout: 10000 });

  console.log('=== 基线复现（修前）===');

  /* ---- P1：新开书退化为创建空对象 ---- */
  await page.evaluate(() => window.WB.go('operate', 'home'));
  await wait(300);
  const booksBefore = await page.evaluate(() => window.WB.S.__runtime.createdBooks.length);
  const entryLabel = await clickFn(page, 'createBook');
  booksBefore;
  await wait(400);
  const overviewTxt = await mainText(page);
  const created = await page.evaluate(() => {
    const S = window.WB.S, b = S.__runtime.createdBooks[S.__runtime.createdBooks.length - 1];
    return { id: b && b.id, title: b && b.title, status: b && b.status, scope: S.__scope.bookId,
      hasIdeaEntry: !!document.querySelector('[data-fn="startFromIdea"],[data-action="startFromIdea"]'),
      hasImportEntry: !!document.querySelector('[data-fn="importBook"],[data-action="importBook"]'),
      hasWriteEntry: !!document.querySelector('[data-fn="newChapter"],[data-action="newChapter"]') };
  });
  await shot(page, 'baseline-new-book-overview');
  note('P1', '新开书退化为创建空对象', '点击入口「' + entryLabel + '」→ 立即得到 ' + created.id + '「' + created.title + '」（' + created.status + '），'
    + '跳到作品概览。\n概览首屏是否提供起步选择：从想法=' + created.hasIdeaEntry + ' / 导入旧稿=' + created.hasImportEntry + ' / 先手写=' + created.hasWriteEntry
    + '\n概览文字片段：' + overviewTxt.slice(0, 200).replace(/\n/g, ' / '));

  /* ---- P1b：构思对话无法推进新书意图 ---- */
  const convBtn = await clickAct(page, 'conv.open');
  await wait(300);
  const dock1 = await count(page, '#sharedArea');
  await setInput(page, '#convInput', SEED);
  await clickAct(page, 'conv.send');
  await wait(600);
  const reply1 = await page.evaluate(() => {
    const ms = Array.from(document.querySelectorAll('#convMsgs .msg'));
    const last = ms[ms.length - 1];
    return last ? last.innerText.trim() : '(no message)';
  });
  await shot(page, 'baseline-discussion-unhandled');
  note('P1b', '构思对话返回「未模拟」', '点击「' + convBtn + '」→ 共享工作区元素=' + dock1
    + '\n作者输入：' + SEED + '\n编辑回复：' + reply1.slice(0, 260).replace(/\n/g, ' / '));

  /* ---- P1c：标签建议采用后，起草核心仍被空素材阻断 ---- */
  await page.evaluate(() => window.WB.go('book', 'craft', { mode: 'positioning' }));
  await wait(320);
  const sugBtn = await clickAct(page, 'craft.suggest');
  await wait(400);
  const sugCount = await count(page, '#modal .tag-suggest');
  await shot(page, 'baseline-direction-presets');
  await clickAct(page, 'craft.applySuggest', [['id', 'SUG-01']]);
  await wait(420);
  const afterApply = await page.evaluate(() => {
    const S = window.WB.S, bid = S.__scope.bookId, c = S.craft[bid];
    return { tags: Object.keys((c.positioning.tags) || {}).length,
      coreOriginal: c.positioning.coreOriginal || '',
      opener: (c.positioning.opener || ''), premise: c.positioning.premise || '' };
  });
  const draftLabel = await clickFn(page, 'craft.draft', [['kind', 'positioning'], ['field', 'coreOriginal']]);
  await wait(420);
  const draftModal = await page.evaluate(() => {
    const m = document.getElementById('modal');
    return m && m.classList.contains('on') ? m.innerText.trim().slice(0, 300) : '(no modal)';
  });
  await shot(page, 'baseline-core-blocked');
  note('P1c', '采用标签建议后起草核心仍被空素材阻断', '建议数=' + sugCount + ' · 采用 SUG-01 后标签维度=' + afterApply.tags
    + '\n一句话故事(coreOriginal)="' + afterApply.coreOriginal + '" · premise="' + afterApply.premise + '"'
    + '\n点击「' + draftLabel + '」→ ' + draftModal.replace(/\n/g, ' / '));

  /* ---- P2：员工藏在页尾 ---- */
  await clickAct(page, 'close-modal');
  await page.evaluate(() => window.WB.go('book', 'overview'));
  await wait(300);
  const layout = await page.evaluate(() => {
    const main = document.getElementById('main');
    const sa = document.querySelector('#main #sharedArea') || document.querySelector('#sharedArea');
    const r = sa ? sa.getBoundingClientRect() : null;
    const m = main.getBoundingClientRect();
    const h = document.getElementById('main').scrollHeight;
    return { mainH: Math.round(m.height), mainScrollH: Math.round(h),
      sharedTop: r ? Math.round(r.top - m.top) : null,
      sharedBottom: r ? Math.round(r.bottom - m.top) : null,
      sharedIsInsideMain: !!(sa && sa.closest('#main')) };
  });
  await shot(page, 'baseline-employee-at-page-bottom');
  note('P2', '员工协作位于长内容下方（页尾）', 'Main 可视高=' + layout.mainH + ' · 内容高=' + layout.mainScrollH
    + '\n共享工作区是否在 Main 内=' + layout.sharedIsInsideMain + ' · 距 Main 顶部=' + layout.sharedTop + 'px，底部=' + layout.sharedBottom + 'px');

  /* ---- 汇总 ---- */
  await browser.close();
  server.close();
  try { fs.rmSync(profile, { recursive: true, force: true }); } catch (e) {}

  const L = ['# 本轮基线复现（修订前）', '',
    '- 运行时间：' + new Date().toISOString(),
    '- 浏览器：系统 Chrome（headless=new）· 1440×1000 · 独立 user-data-dir',
    '- 目的：在实施前坐实三项反馈，作为修订前基线。',
    '- Console Error：' + errors.length, ''];
  findings.forEach(f => { L.push('## ' + f.id + ' ' + f.title, '', f.detail, ''); });
  if (errors.length) { L.push('## Console 错误', ''); errors.forEach(e => L.push('- ' + e.slice(0, 240))); }
  fs.writeFileSync(path.join(EV, 'BASELINE_REPRO.md'), L.join('\n'));

  console.log('\n============================');
  console.log('复现项：' + findings.length + ' · Console Error: ' + errors.length + ' · 截图：' + seq + ' 张');
  if (errors.length) errors.forEach(e => console.log('  ! ' + e.slice(0, 200)));
  process.exit(0);
})().catch(e => { console.error('HARNESS ERROR:', e); process.exit(2); });
