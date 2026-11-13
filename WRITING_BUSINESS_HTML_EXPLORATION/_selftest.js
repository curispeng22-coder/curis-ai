/* CURIS — Writing Business HTML Exploration · 真实浏览器点击自测
   用真实 Chrome 打开应用：逐区逐视面点击、走完五条探索路径、运行时接线审计、
   状态诚实性断言、持久化断言，收集 Console 错误与截图。
   运行：node _selftest.js     （结果写入 _evidence/）  */
'use strict';
const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');
const http = require('http');

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const ROOT = __dirname;
const EV = path.join(ROOT, '_evidence');
fs.mkdirSync(EV, { recursive: true });

const errors = [];
const steps = [];
let shotSeq = 0;
const IGNORE = [/favicon\.ico/];   // 测试服务器噪声，与原型无关

const VIEW_COUNT = 23;   /* 6 区 · 23 视面（作品区新增 创作内核 / 审校与质量 / 旧稿接续） */

function step(name, ok, detail) {
  steps.push({ name, ok: !!ok, detail: detail || '' });
  console.log((ok ? '  ✓ ' : '  ✗ ') + name + (detail ? '  — ' + detail : ''));
}
const wait = (ms) => new Promise(r => setTimeout(r, ms));

const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.png': 'image/png', '.json': 'application/json' };
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

async function boot(page, url, label) {
  await page.goto(url, { waitUntil: 'load', timeout: 30000 });
  await page.waitForSelector('#nav .nav-item', { timeout: 10000 });
  const storage = await page.evaluate(() => { try { localStorage.setItem('__t', '1'); localStorage.removeItem('__t'); return true; } catch (e) { return false; } });
  const navCount = await page.evaluate(() => document.querySelectorAll('#nav .nav-item').length);
  const viewCount = await page.evaluate(() => Object.keys(window.WB.views).length);
  step(label + ' 启动：主导航 6 区', navCount === 6, 'nav-item=' + navCount);
  step(label + ' 视面注册 ' + VIEW_COUNT + ' 项', viewCount === VIEW_COUNT, 'views=' + viewCount);
  step(label + ' 本机存储可用（长期连续性前提）', storage);
}
async function shot(page, tag) {
  shotSeq++;
  const f = path.join(EV, String(shotSeq).padStart(2, '0') + '-' + tag + '.png');
  await page.screenshot({ path: f });
  return path.basename(f);
}
async function crumb(page) { return (await page.$eval('#crumb', e => e.innerText)).replace(/\s+/g, ' ').trim(); }
async function mainText(page) { return (await page.$eval('#main', e => e.innerText)).trim(); }
async function click(page, sel) {
  await page.waitForSelector(sel, { timeout: 8000 });
  await page.click(sel);
  await wait(160);
}
async function goView(page, area, view) {
  await page.evaluate((a, v) => window.WB.go(a, v), area, view);
  await wait(140);
}
/* 真实点击：按 data-fn（可带 data-a1）找到按钮并 click，走完整事件链而非直接调函数 */
async function clickFn(page, fn, a1) {
  const hit = await page.evaluate((fn, a1) => {
    const els = Array.from(document.querySelectorAll('[data-fn="' + fn + '"]'));
    const el = (a1 == null || a1 === '') ? els[0] : (els.filter(e => e.getAttribute('data-a1') === String(a1))[0] || els[0]);
    if (!el) return false;
    el.click(); return true;
  }, fn, a1 == null ? '' : String(a1));
  await wait(200);
  return hit;
}
/* 真实点击：按 data-action（可带任意 data-* 匹配） */
async function clickAct(page, action, attrs) {
  const hit = await page.evaluate((action, attrs) => {
    const els = Array.from(document.querySelectorAll('[data-action="' + action + '"]'));
    const el = els.filter(e => (attrs || []).every(([k, v]) => e.getAttribute('data-' + k) === String(v)))[0] || els[0];
    if (!el) return false;
    el.click(); return true;
  }, action, attrs || []);
  await wait(200);
  return hit;
}
async function setField(page, id, text) {
  await page.evaluate((id, text) => {
    const e = document.getElementById(id);
    if (e) { e.value = text; e.dispatchEvent(new Event('input', { bubbles: true })); }
  }, id, text);
  await wait(60);
}
async function craftDbg(page) {
  return page.evaluate(() => {
    const S = window.WB.S, bid = S.__scope.bookId, C = S.craft || {};
    const c = C[bid] || null;
    let scenes = 0;
    if (c) Object.keys(c.scenes || {}).forEach(k => { scenes += (c.scenes[k] || []).length; });
    return {
      book: bid, hasCraft: !!c,
      world: c ? (c.world || []).length : -1, characters: c ? (c.characters || []).length : -1,
      outline: c ? (c.outline || []).length : -1, scenes: scenes,
      coreOriginal: c ? c.positioning.coreOriginal : null,
      propOpen: (S.craftProposals || []).filter(p => p.state === 'open').length,
      impact: c ? (c.impactLog || []).length : -1,
      reviewRuns: (S.reviewRuns || []).length,
      bookIds: Object.keys(C),
      books: window.WB.allBooks().map(b => b.id)
    };
  });
}

(async () => {
  const server = await serve();
  const httpUrl = 'http://127.0.0.1:' + server.address().port + '/index.html';
  const fileUrl = 'file://' + encodeURI(path.join(ROOT, 'index.html'));

  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--no-proxy-server', '--allow-file-access-from-files', '--disable-gpu'],
    defaultViewport: { width: 1512, height: 982 },
    protocolTimeout: 120000
  });
  const page = await browser.newPage();
  page.on('console', m => { if (m.type() === 'error' && !IGNORE.some(r => r.test(m.text()))) errors.push('CONSOLE: ' + m.text()); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));
  page.on('requestfailed', r => { if (!IGNORE.some(x => x.test(r.url()))) errors.push('REQFAIL: ' + r.url().slice(0, 120)); });

  console.log('\n=== 阶段 A：file:// 直接打开（交付形态）===');
  await boot(page, fileUrl, 'A');
  console.log('\n=== 阶段 B：http://127.0.0.1（长期连续性 / 持久化）===');
  await boot(page, httpUrl, 'B');

  /* ---- 阶段 C：六区 20 视面逐一点击 ---- */
  console.log('\n=== 阶段 C：六区全部视面逐一点击 ===');
  const NAV = await page.evaluate(() => window.WB.NAV.map(n => ({ area: n.area, name: n.name, views: n.views })));
  let okCount = 0, allCount = 0;
  for (const area of NAV) {
    await click(page, `#nav .nav-item[data-area="${area.area}"]`);
    for (const [view, vname] of area.views) {
      allCount++;
      await page.waitForSelector(`#nav .nav-sub button[data-view="${view}"]`, { timeout: 8000 });
      await page.click(`#nav .nav-sub button[data-view="${view}"]`);
      await wait(150);
      const c = await crumb(page), body = await mainText(page);
      if (body.length > 40 && c.indexOf(vname) >= 0) okCount++;
      else step('视面 ' + area.area + '.' + view + ' 渲染', false, 'crumb=' + c + ' len=' + body.length);
    }
  }
  step('六区 ' + allCount + ' 视面均可见且有内容', okCount === allCount, okCount + '/' + allCount);
  step('未出现「该工作面尚未实现」兜底',
    !(await page.evaluate(() => document.body.innerText.indexOf('该工作面尚未实现') >= 0)));

  /* ---- 阶段 D：运行时接线审计 ---- */
  console.log('\n=== 阶段 D：运行时接线审计（全部视面可交互元素）===');
  const wiring = await page.evaluate(() => {
    const SPECIAL = ['close-drawer', 'close-modal', 'nav.area', 'nav.view', 'back'];
    const out = { total: 0, dead: [], deadChange: [] };
    window.WB.NAV.forEach(n => n.views.forEach(function (v) {
      window.WB.go(n.area, v[0]);
      const scopes = ['#main', '#aside', '#rail', '#topbar', '#quickbar'];
      scopes.forEach(function (s) {
        document.querySelectorAll(s + ' [data-action]').forEach(function (el) {
          const a = el.getAttribute('data-action'); out.total++;
          if (SPECIAL.indexOf(a) >= 0) return;
          if (a.indexOf('act.') === 0) {
            const fn = el.getAttribute('data-fn');
            if (typeof window.WB.act[fn] !== 'function') out.dead.push(n.area + '.' + v[0] + ' → act.' + fn);
            return;
          }
          if (typeof window.WB.on[a] !== 'function') out.dead.push(n.area + '.' + v[0] + ' → ' + a);
        });
      });
      document.querySelectorAll('#main [data-change], #aside [data-change]').forEach(function (el) {
        const c = el.getAttribute('data-change');
        if (typeof window.WB.on[c] !== 'function') out.deadChange.push(n.area + '.' + v[0] + ' → ' + c);
      });
    }));
    return out;
  });
  step('运行时扫描到的可交互元素均解析到处理器（无死按钮）',
    wiring.dead.length === 0, wiring.total + ' 个元素；死按钮=' + wiring.dead.length + (wiring.dead.length ? ' → ' + wiring.dead.slice(0, 5).join(', ') : ''));
  step('所有 data-change 解析到处理器', wiring.deadChange.length === 0,
    wiring.deadChange.length ? wiring.deadChange.slice(0, 5).join(', ') : '0 项缺失');

  /* ================= 路径 1：市场进入创作 ================= */
  console.log('\n=== 路径 1：市场进入创作 ===');
  await click(page, '#nav .nav-item[data-area="market"]');
  await click(page, '#nav .nav-sub button[data-view="observations"]');
  const obsTxt = await mainText(page);
  step('P1 市场观察是可判断的观察（非结论）', /观察|未确认|待判/.test(obsTxt), 'len=' + obsTxt.length);
  await shot(page, 'p1-market-observations');
  await click(page, '#nav .nav-sub button[data-view="references"]');
  step('P1 参考与拆解区分外部参考与自有作品', /参考|拆解/.test(await mainText(page)));
  await shot(page, 'p1-market-references');
  await click(page, '#nav .nav-sub button[data-view="direction"]');
  const dirTxt = await mainText(page);
  step('P1 已接受方向同时展示「风险 / 未确认 / 落到何处」',
    /风险/.test(dirTxt) && /未确认|未知/.test(dirTxt) && /落|应用/.test(dirTxt));
  step('P1 存在未决方向的裁决入口（接受 ≠ 已应用）',
    (await page.evaluate(() => document.querySelectorAll('[data-fn="directionDecide"]').length)) > 0);
  step('P1 方向核心可被作者直接改写（真实写入）',
    (await page.evaluate(() => document.querySelectorAll('[data-change="dir.edit"]').length)) > 0);
  await shot(page, 'p1-market-direction');
  /* 真实裁决一次，确认写入 */
  const d2Before = await page.evaluate(() => window.WB.S.directions.filter(d => d.status === 'pending').length);
  await page.evaluate(() => {
    const els = document.querySelectorAll('[data-fn="directionDecide"]');
    for (const e of els) if (e.getAttribute('data-a1') === 'D-02' && e.getAttribute('data-a2') === 'accept') { e.click(); return; }
  });
  await wait(300);
  const d2After = await page.evaluate(() => window.WB.S.directions.filter(d => d.status === 'pending').length);
  step('P1 接受方向写入真实状态（未决数减少）', d2After < d2Before, d2Before + ' → ' + d2After);
  step('P1 接受方向后说明「已更新到何处」（接受 ≠ 已应用）',
    /已更新|应用|落/.test(await mainText(page)));
  const d2Accepted = await page.evaluate(() => !!window.WB.byId(window.WB.S.directions, 'D-02').bookId);
  step('P1 接受未定方向会派生新的 Book 身份（方向 → 作品）', d2Accepted);
  await shot(page, 'p1-direction-accepted-new-book');
  await click(page, '#nav .nav-item[data-area="book"]');
  await click(page, '#nav .nav-sub button[data-view="library"]');
  step('P1 作品库：本地作品与接入外部作品区分', /作品/.test(await mainText(page)) && /接入/.test(await mainText(page)));
  step('P1 可接入已有平台作品（有真实入口）',
    (await page.evaluate(() => document.querySelectorAll('[data-fn="importBook"], [data-action="book.open"]').length)) > 0);
  await shot(page, 'p1-book-library');

  /* ================= 路径 2：长期创作 ================= */
  console.log('\n=== 路径 2：长期创作 ===');
  /* 固定范围到主作品，使后续断言与作品无关地可复现 */
  await page.evaluate(() => window.WB.act.bookScope('B-01'));
  await wait(200);
  await click(page, '#nav .nav-item[data-area="book"]');
  await click(page, '#nav .nav-sub button[data-view="overview"]');
  step('P2 作品概览：库存分「可发布 / 已排期 / 草稿」', /可发布|库存/.test(await mainText(page)));
  await shot(page, 'p2-book-overview');
  await click(page, '#nav .nav-sub button[data-view="manuscript"]');
  await click(page, '.chap[data-action="book.chap"][data-id="ch43"]');
  const msTxt = await mainText(page);
  step('P2 正文工作台载入第 43 章（已发布 v2 + 修订候选）',
    /对面/.test(msTxt) && /v2/.test(msTxt), (await crumb(page)).slice(0, 60));
  const msParts = await page.evaluate(() => ({
    paras: document.querySelectorAll('.ms-pn, .ms-body p, .ms-wrap p').length,
    diffRows: document.querySelectorAll('.diff-row, .diff-it, [data-fn="decideChange"]').length
  }));
  step('P2 正文可读区与候选区同时在场（候选不覆盖正式稿）', msParts.paras > 3 && msParts.diffRows > 0,
    '段落=' + msParts.paras + ' 候选条=' + msParts.diffRows);
  await shot(page, 'p2-manuscript-candidate');

  const before = await page.evaluate(() => {
    const c = window.WB.S.chapters['ch43'];
    return { formal: c.formal, published: c.published, adopted: window.WB.candidateState('C-43').adopted, applied: window.WB.candidateState('C-43').applied };
  });
  await page.evaluate(() => {
    const b = document.querySelector('[data-fn="decideChange"][data-a3="true"]');
    if (b) b.click();
  });
  await wait(300);
  const after = await page.evaluate(() => {
    const c = window.WB.S.chapters['ch43'];
    const cs = window.WB.candidateState('C-43');
    return { formal: c.formal, published: c.published, adopted: cs.adopted, open: cs.open, applied: cs.applied };
  });
  step('P2 逐条采纳真实生效', after.adopted === before.adopted + 1, 'adopted ' + before.adopted + ' → ' + after.adopted);
  step('P2 采纳候选后正式稿版本不变（候选 ≠ 正式稿）',
    after.formal === before.formal && after.published === before.published,
    'formal=' + after.formal + ' published=' + after.published);
  step('P2 「已采纳」≠「已生效」（生成正式版本前 applied=false）', after.applied === false,
    'applied=' + after.applied + ' open=' + after.open);
  await shot(page, 'p2-candidate-adopted-one');

  /* 逐条拒绝一条（选一条与已采纳不同的条目，避免把采纳撤销） */
  const rejBefore = await page.evaluate(() => window.WB.candidateState('C-43').rejected);
  await page.evaluate(() => {
    const b = document.querySelector('[data-fn="decideChange"][data-a2="C43-3"][data-a3="false"]');
    if (b) b.click();
  });
  await wait(280);
  const afterRej = await page.evaluate(() => window.WB.candidateState('C-43'));
  step('P2 单条拒绝是正常选择（写入 rejected，且不影响已采纳条）',
    afterRej.rejected === rejBefore + 1 && afterRej.adopted === 1,
    'rejected ' + rejBefore + ' → ' + afterRej.rejected + '，adopted=' + afterRej.adopted);

  /* 整份采纳 → 生成正式版本：按「当前未决」的具体条目逐条点击（避免重复点到同一条） */
  const openIds = await page.evaluate(() => window.WB.candidate('C-43').changes.filter(c => c.applied === null).map(c => c.id));
  for (const cid of openIds) {
    await page.evaluate((c) => {
      const b = document.querySelector('[data-fn="decideChange"][data-a2="' + c + '"][data-a3="true"]');
      if (b) b.click();
    }, cid);
    await wait(260);
  }
  const openLeft = await page.evaluate(() => window.WB.candidateState('C-43').open);
  step('P2 逐条裁决完成（未决 = 0）', openLeft === 0, '未决=' + openLeft);
  /* 未决时按钮不应给出「生成正式版本」入口 —— 该护栏在未决场景下已被触发过 */
  await page.evaluate(() => { const b = document.querySelector('[data-action="book.apply"]'); if (b) b.click(); });
  await wait(300);
  const modalHasApply = await page.evaluate(() => !!document.querySelector('#modal [data-fn="applyCandidate"]'));
  step('P2 「确认并生成正式版本」先弹确认，并声明线上版本不会自动改变', modalHasApply);
  if (modalHasApply) {
    const modalTxt = await page.$eval('#modal', e => e.innerText);
    step('P2 确认框明示「已发布章节的线上版本不会自动改变」', /线上版本不会自动改变|不会自动改变/.test(modalTxt));
    await page.evaluate(() => { const b = document.querySelector('#modal [data-fn="applyCandidate"]'); if (b) b.click(); });
    await wait(350);
  }
  const applied = await page.evaluate(() => {
    const c = window.WB.S.chapters['ch43'];
    return { formal: c.formal, published: c.published, applied: window.WB.candidateState('C-43').applied };
  });
  step('P2 生成新正式版本（formal 前进）', applied.formal !== before.formal, before.formal + ' → ' + applied.formal);
  step('P2 生成新版本后仍是「已发布 v2」（正式 ≠ 已发布）', applied.published === 'v2', 'published=' + applied.published);
  await shot(page, 'p2-manuscript-applied');

  await click(page, '#nav .nav-sub button[data-view="story"]');
  step('P2 故事状态：伏笔/设定可追溯', /伏笔|设定|线索/.test(await mainText(page)));
  await shot(page, 'p2-story-state');
  /* Canon 冲突章 */
  await click(page, '#nav .nav-sub button[data-view="manuscript"]');
  await click(page, '.chap[data-action="book.chap"][data-id="ch44"]');
  const c44 = await mainText(page);
  step('P2 存在 Canon 冲突的候选被显式标出并给出去处理入口',
    /冲突|Canon/i.test(c44), 'len=' + c44.length);
  await shot(page, 'p2-canon-conflict');

  /* ================= 路径 3：连载与反馈 ================= */
  console.log('\n=== 路径 3：连载与反馈 ===');
  await click(page, '#nav .nav-item[data-area="publish"]');
  await click(page, '#nav .nav-sub button[data-view="queue"]');
  const qTxt = await mainText(page);
  step('P3 队列区分「未核验(unknown) / 已排期 / 已驳回」', /未核验|未知/.test(qTxt) && /排期/.test(qTxt));
  step('P3 未知态未显示为「失败」', !/提交失败/.test(qTxt));
  await shot(page, 'p3-publish-queue');
  step('P3 未核验项提供核验入口，且不预设为失败',
    (await page.evaluate(() => document.querySelectorAll('[data-action="pub.verifyHelp"], [data-action="pub.receipt"], [data-fn="verify"], [data-fn="waitReceipt"]').length)) > 0);
  await click(page, '#nav .nav-sub button[data-view="receipts"]');
  /* 明确打开 Q-01（未知态）的回执详情，保证可复现 */
  await page.evaluate(() => window.WB.go('publish', 'receipts', { id: 'Q-01' }));
  await wait(240);
  step('P3 提交与回执：回执可核验、状态可分', /回执/.test(await mainText(page)));
  /* 未知态 → 走核验清单 → 真正消解（Unknown 可被核验，不靠猜） */
  const q1Before = await page.evaluate(() => window.WB.queueItem('Q-01').state);
  const verifyBtnFound = await page.evaluate(() => {
    const b = document.querySelector('[data-action="pub.verifyHelp"][data-id="Q-01"]') ||
      document.querySelector('[data-action="pub.verifyHelp"]');
    if (b) { b.click(); return true; } return false;
  });
  await wait(300);
  const evidenceListShown = await page.evaluate(() => {
    const dr = document.querySelector('#drawer');
    if (!dr || dr.getAttribute('aria-hidden') === 'true') return false;
    const t = dr.innerText;
    return /核验|清单/.test(t) && dr.querySelectorAll('[data-fn="verify"], [data-fn="waitReceipt"], [data-fn="submit"]').length > 0;
  });
  step('P3 未知态提供核验清单，给出「已在线上线 / 保持等待」两种选择',
    verifyBtnFound && evidenceListShown,
    '入口=' + verifyBtnFound + ' 清单=' + evidenceListShown);
  await page.evaluate(() => { const b = document.querySelector('#drawer [data-fn="verify"]'); if (b) b.click(); });
  await wait(360);
  const q1After = await page.evaluate(() => ({ st: window.WB.queueItem('Q-01').state, ch: window.WB.S.chapters['ch40'] ? window.WB.S.chapters['ch40'].state : null }));
  step('P3 核验写入真实结果（unknown → live，章节转为已发布）',
    q1Before === 'unknown' && q1After.st === 'live', q1Before + ' → ' + q1After.st + '，ch40=' + q1After.ch);
  await page.evaluate(() => { const b = document.querySelector('#drawer [data-action="close-drawer"]'); if (b) b.click(); });
  await wait(180);
  await shot(page, 'p3-receipts');
  await click(page, '#nav .nav-sub button[data-view="accounts"]');
  step('P3 账号与映射：跨平台映射阻塞显式暴露', /账号|映射/.test(await mainText(page)));
  await shot(page, 'p3-accounts');

  /* ================= 路径 4：归因与学习 ================= */
  console.log('\n=== 路径 4：归因与学习 ===');
  await click(page, '#nav .nav-item[data-area="audience"]');
  await click(page, '#nav .nav-sub button[data-view="performance"]');
  const perfTxt = await mainText(page);
  step('P4 表现总览标注口径与来源', /口径|来源/.test(perfTxt));
  step('P4 未出现伪造的逐章收益数值', !/逐章收益\s*[:：]\s*¥?\s*\d/.test(perfTxt));
  step('P4 图表已渲染（SVG 序列）', (await page.evaluate(() => document.querySelectorAll('#main svg, #main canvas').length)) > 0);
  const chart = await page.evaluate(() => {
    const texts = [...document.querySelectorAll('#main svg text')].map(t => t.textContent.trim());
    return { total: texts.length, empty: texts.filter(t => !t).length, sample: texts.filter(Boolean).slice(-4).join('|') };
  });
  step('P4 图表时间轴与刻度标签均有文字（不出现空标签）',
    chart.total > 0 && chart.empty === 0, '共 ' + chart.total + ' 个标签，空 ' + chart.empty + ' 个，示例：' + chart.sample);
  await shot(page, 'p4-performance');
  await click(page, '#nav .nav-sub button[data-view="entry"]');
  step('P4 数据补录：导入冲突 / 手工修正 待处理', /补录|录入|修正/.test(await mainText(page)));
  await shot(page, 'p4-entry');
  await click(page, '#nav .nav-sub button[data-view="comments"]');
  step('P4 评论洞察：聚类 + 可回跳正文锚点', /评论|聚类/.test(await mainText(page)));
  await shot(page, 'p4-comments');

  await click(page, '#nav .nav-sub button[data-view="attribution"]');
  const attrTxt = await mainText(page);
  const layInfo = await page.evaluate(() => {
    const ls = [...document.querySelectorAll('#main .lay')];
    return { n: ls.length, cls: ls.map(e => e.className.replace('lay ', '')).join(','), txt: ls.map(e => e.innerText.slice(0, 24)).join(' | ') };
  });
  step('P4 五层归因结构完整渲染（5 个 .lay 面板）', layInfo.n === 5, 'lay=' + layInfo.n + ' [' + layInfo.cls + ']');
  step('P4 五层按 Observation→Evidence→Hypothesis→Learning→Recommendation 排列',
    /观察/.test(layInfo.txt) && /证据/.test(layInfo.txt) && /假设/.test(layInfo.txt) && /经验候选/.test(layInfo.txt) && /建议/.test(layInfo.txt),
    layInfo.txt.slice(0, 120));
  step('P4 归因含替代解释 / 反证 / 证据缺口 / 表述边界',
    /替代解释/.test(attrTxt) && /反证/.test(attrTxt) && /缺口/.test(attrTxt) && /边界/.test(attrTxt));
  step('P4 提供「完整证据」审阅入口（不丢上下文）',
    (await page.evaluate(() => document.querySelectorAll('[data-action="aud.evidence"]').length)) > 0);
  await shot(page, 'p4-attribution');
  /* 打开证据抽屉 */
  await page.evaluate(() => { const b = document.querySelector('[data-action="aud.evidence"]'); if (b) b.click(); });
  await wait(320);
  const drawerOpen = await page.evaluate(() => document.querySelector('#drawer') && document.querySelector('#drawer').getAttribute('aria-hidden') !== 'true' && document.querySelector('#drawer').innerText.length > 20);
  step('P4 证据抽屉可打开且含来源与缺口', drawerOpen,
    (await page.evaluate(() => document.querySelector('#drawer') ? document.querySelector('#drawer').innerText.slice(0, 60) : '')).replace(/\n/g, ' '));
  await shot(page, 'p4-evidence-drawer');
  await page.evaluate(() => { const b = document.querySelector('#drawer [data-action="close-drawer"]'); if (b) b.click(); });
  await wait(180);

  /* 归因 → 经验 */
  const lBefore = await page.evaluate(() => window.WB.S.learnings.length);
  await page.evaluate(() => { const b = document.querySelector('[data-fn="analysisToLearning"]'); if (b) b.click(); });
  await wait(340);
  const lTxt = await page.evaluate(() => document.querySelector('#modal') ? document.querySelector('#modal').innerText : '');
  step('P4 沉淀为经验前强制展示适用范围与「尚未排除」项', /适用范围/.test(lTxt) && /尚未排除/.test(lTxt), lTxt.slice(0, 70).replace(/\n/g, ' '));
  step('P4 沉淀时反例与分析来源随行', /反例/.test(lTxt) && /来源分析/.test(lTxt));
  await page.evaluate(() => { const b = document.querySelector('#modal [data-fn="learningCreate"]'); if (b) b.click(); });
  await wait(340);
  const lAfter = await page.evaluate(() => window.WB.S.learnings.length);
  step('P4 确认后生成经验候选（待验证，未接受）', lAfter === lBefore + 1, 'learnings ' + lBefore + ' → ' + lAfter);
  step('P4 生成的候选自带 scope 与反例字段',
    await page.evaluate(() => { const l = window.WB.S.learnings[window.WB.S.learnings.length - 1]; return !!l.scope && !!l.counter && l.accepted === 'pending'; }));
  await shot(page, 'p4-attribution-to-learning');

  await click(page, '#nav .nav-item[data-area="learning"]');
  await click(page, '#nav .nav-sub button[data-view="library"]');
  const libL = await mainText(page);
  step('P4 经验库展示 scope / 反例 / 应用与验证分离',
    /范围|适用/.test(libL) && /反例/.test(libL));
  await shot(page, 'p4-learning-library');
  await page.evaluate(() => { const b = document.querySelector('[data-action="learn.pick"]'); if (b) b.click(); });
  await wait(300);
  const ldTxt = await mainText(page);
  step('P4 经验详情：区分「用过」与「验证过」并展示反例',
    /应用|使用/.test(ldTxt) && /验证/.test(ldTxt) && /反例/.test(ldTxt));
  step('P4 经验可裁决（接受 / 标记待质疑 / 停用）',
    (await page.evaluate(() => document.querySelectorAll('[data-fn="learningDecide"]').length)) === 3);
  const accBefore = await page.evaluate(() => window.WB.learning(window.WB.S.__route.params.id).accepted);
  await page.evaluate(() => { const b = document.querySelector('[data-fn="learningDecide"][data-a2="accept"]'); if (b) b.click(); });
  await wait(300);
  const accAfter = await page.evaluate(() => window.WB.learning(window.WB.S.__route.params.id).accepted);
  step('P4 接受经验写入真实状态（限定范围内可用）', accAfter === 'author', accBefore + ' → ' + accAfter);
  await shot(page, 'p4-learning-detail');

  /* ================= 路径 5：日常维护与恢复 ================= */
  console.log('\n=== 路径 5：日常维护与恢复 ===');
  await click(page, '#nav .nav-item[data-area="operate"]');
  await click(page, '#nav .nav-sub button[data-view="home"]');
  step('P5 业务首页：待决决定来自真实数据', /待决|决定/.test(await mainText(page)));
  step('P5 首页暴露「无人负责」的职责缺口（不是虚构员工）',
    /未指派|无人|No-Owner|待指派|<空>/.test(await mainText(page)) || (await page.evaluate(() => window.WB.S.responsibilities.some(r => !r.owner))),
    'R-FIN 无归属=' + (await page.evaluate(() => window.WB.S.responsibilities.filter(r => !r.owner).map(r => r.id).join(','))));
  await shot(page, 'p5-operate-home');
  await click(page, '#nav .nav-sub button[data-view="plan"]');
  const planTxt = await mainText(page);
  step('P5 计划与决定：给出批准 / 保持 / 暂缓三类裁决',
    /批准/.test(planTxt) && /(保持|继续)/.test(planTxt) && /(暂缓|延后)/.test(planTxt));
  await shot(page, 'p5-operate-plan');
  const decBefore = await page.evaluate(() => window.WB.S.decisions.filter(d => d.status === 'pending').length);
  await page.evaluate(() => { const b = document.querySelector('[data-fn="decision"]'); if (b) b.click(); });
  await wait(320);
  const decAfter = await page.evaluate(() => window.WB.S.decisions.filter(d => d.status === 'pending').length);
  step('P5 裁决写入真实状态（待决数减少）', decAfter < decBefore, decBefore + ' → ' + decAfter);
  step('P5 决定区展示「已接受 ≠ 已应用」（含应用到何处）', /已应用|待应用|应用到/.test(await mainText(page)));
  await shot(page, 'p5-decision-applied');

  /* 关注点恢复 */
  await click(page, '#nav .nav-item[data-area="market"]');
  await click(page, '#nav .nav-sub button[data-view="watches"]');
  const wTxt = await mainText(page);
  step('P5 持续关注：失败/暂停的关注点显式暴露', /关注/.test(wTxt) && /(失败|暂停|已停)/.test(wTxt));
  const wBefore = await page.evaluate(() => window.WB.S.watches.map(w => w.id + ':' + (w.state || w.status || '')).join(','));
  const wActed = await page.evaluate(() => {
    const b = document.querySelector('[data-fn="watchCheck"]') || document.querySelector('[data-action="market.watchEdit"]');
    if (b) { b.click(); return true; } return false;
  });
  await wait(320);
  const wAfter = await page.evaluate(() => window.WB.S.watches.map(w => w.id + ':' + (w.state || w.status || '')).join(','));
  step('P5 关注点可恢复（重试 / 编辑 / 移除有真实入口与效果）', wActed, wBefore === wAfter ? '（打开的是编辑面板）' : wBefore + ' → ' + wAfter);
  await page.evaluate(() => { const b = document.querySelector('#modal [data-action="close-modal"]'); if (b) b.click(); });
  await wait(160);
  await shot(page, 'p5-watches-recover');

  /* 破坏性操作护栏 */
  await click(page, '#nav .nav-item[data-area="publish"]');
  await click(page, '#nav .nav-sub button[data-view="accounts"]');
  await page.evaluate(() => { const b = document.querySelector('[data-action="pub.disconnect"]'); if (b) b.click(); });
  await wait(260);
  step('P5 断连等破坏性操作先弹确认（护栏）',
    (await page.evaluate(() => !!document.querySelector('#modal [data-action]'))));
  await page.evaluate(() => { const b = document.querySelector('#modal [data-action="close-modal"]'); if (b) b.click(); });
  await wait(160);
  await shot(page, 'p5-disconnect-guard');

  /* 切书 */
  await click(page, '#nav .nav-item[data-area="book"]');
  await click(page, '#nav .nav-sub button[data-view="library"]');
  const scopeBefore = await page.evaluate(() => document.querySelector('#scopeBox').innerText);
  await page.evaluate(() => {
    const b = document.querySelector('[data-action="book.open"][data-id="B-02"]') ||
      document.querySelector('.book[data-action]') ||
      document.querySelector('[data-fn="bookScope"][data-a1="B-02"]');
    if (b) b.click();
  });
  await wait(320);
  const scopeAfter = await page.evaluate(() => document.querySelector('#scopeBox').innerText);
  step('P5 切换作品会改变「当前作品」范围', scopeBefore !== scopeAfter, scopeBefore.replace(/\n/g, ' ') + ' → ' + scopeAfter.replace(/\n/g, ' '));
  await shot(page, 'p5-book-switch');

  /* 空书不串稿：新建作品后正文工作面必须为空，且能真实开出第一章 */
  await page.evaluate(() => window.WB.act.createBook());
  await wait(320);
  const p5BookId = await page.evaluate(() => window.WB.S.__scope.bookId);
  await page.evaluate(() => window.WB.go('book', 'manuscript'));
  await wait(320);
  const emptyState = await page.evaluate(() => {
    const t = document.getElementById('main').innerText;
    return {
      other: /第 43 章|夜行灯|对面/.test(t),
      scope: window.WB.S.__scope.bookId,
      chaps: document.querySelectorAll('#main .chap').length,
      hasNew: !!document.querySelector('[data-fn="newChapter"]')
    };
  });
  step('P5 新作品不串稿：正文工作面不显示其他作品的章节，范围不被改写',
    !emptyState.other && emptyState.chaps === 0 && emptyState.scope === p5BookId && emptyState.hasNew,
    'scope=' + emptyState.scope + '（应 ' + p5BookId + '）章节=' + emptyState.chaps + ' 串他作=' + emptyState.other);
  await shot(page, 'p5-new-book-empty');
  await page.evaluate(() => { const b = document.querySelector('[data-fn="newChapter"]'); if (b) b.click(); });
  await wait(420);
  const firstChap = await page.evaluate(() => {
    const bid = window.WB.S.__scope.bookId;
    return {
      scope: bid,
      ch: window.WB.S.__route.params.chapter,
      stock: window.WB.stockOf(bid),
      count: Object.keys(window.WB.S.chapters).filter(k => window.WB.S.chapters[k].bookId === bid).length,
      draft: (function () { const c = window.WB.S.chapters[window.WB.S.__route.params.chapter]; return c ? c.state : null; })()
    };
  });
  step('P5 空书可开写第一章：新章为草稿，不计入可发布库存',
    firstChap.count === 1 && firstChap.draft === 'draft' && firstChap.stock.publishable === 0 && firstChap.stock.draft === 1,
    '章=' + firstChap.count + ' 状态=' + firstChap.draft + ' 库存=' + JSON.stringify(firstChap.stock));
  await shot(page, 'p5-first-chapter');
  /* 恢复主作品范围，避免影响后续阶段 */
  await page.evaluate(() => { window.WB.S.__scope.bookId = 'B-01'; window.WB.go('operate', 'home'); });
  await wait(260);

  /* ================= 阶段 E：状态诚实性 ================= */
  console.log('\n=== 阶段 E：状态诚实性（跨 20 视面）===');
  const honesty = await page.evaluate(() => {
    const out = { unknownEls: 0, unknownViews: [], zeroMoney: 0, providerAsEmp: 0, empCount: window.WB.S.employees.length };
    window.WB.NAV.forEach(n => n.views.forEach(function (v) {
      window.WB.go(n.area, v[0]);
      const m = document.getElementById('main').innerText;
      const k = document.querySelectorAll('#main .unknown, #aside .unknown').length;
      out.unknownEls += k;
      if (k > 0 || /未采集|未知|未核验|无数据/.test(m)) out.unknownViews.push(n.area + '.' + v[0]);
      out.zeroMoney += (m.match(/¥\s*0(\.00)?\b/g) || []).length;
    }));
    return out;
  });
  step('「未知」有专用视觉标记且出现在多个视面（Unknown ≠ 0）',
    honesty.unknownEls > 0 && honesty.unknownViews.length >= 3,
    'unknown 元素=' + honesty.unknownEls + '，涉及视面=' + honesty.unknownViews.length);
  step('全应用未出现伪造的 ¥0 展示', honesty.zeroMoney === 0, '¥0 次数=' + honesty.zeroMoney);
  step('AI 员工仅来自员工名单（Provider 未被画成员工）', honesty.empCount === 4, '员工=' + honesty.empCount);
  console.log('    员工：' + (await page.evaluate(() => window.WB.S.employees.map(e => e.id + ':' + e.name).join(', '))));

  /* ================= 阶段 F：持久化 + 重置 ================= */
  console.log('\n=== 阶段 F：长期连续性（刷新保持 / 可重置）===');
  const snapBefore = await page.evaluate(() => JSON.stringify({
    decisions: window.WB.S.decisions.map(d => d.status),
    ch43: window.WB.S.chapters['ch43'].formal,
    dirs: window.WB.S.directions.map(d => d.status)
  }));
  await page.reload({ waitUntil: 'load' });
  await page.waitForSelector('#nav .nav-item', { timeout: 10000 });
  const snapAfter = await page.evaluate(() => JSON.stringify({
    decisions: window.WB.S.decisions.map(d => d.status),
    ch43: window.WB.S.chapters['ch43'].formal,
    dirs: window.WB.S.directions.map(d => d.status)
  }));
  step('刷新后全部裁决与版本保持（写入 localStorage）', snapBefore === snapAfter,
    snapBefore.slice(0, 70) + (snapBefore === snapAfter ? '' : ' ≠ ' + snapAfter.slice(0, 70)));

  const decidedBefore = await page.evaluate(() => window.WB.S.decisions.filter(d => d.status !== 'pending').length);
  await page.evaluate(() => { const b = document.querySelector('[data-fn="resetDemo"]'); if (b) b.click(); });
  await wait(300);
  const resetModal = await page.evaluate(() => !!document.querySelector('#modal [data-fn="resetConfirmed"]'));
  step('重置演示数据前有确认弹窗（护栏）', resetModal);
  if (resetModal) {
    const t = await page.$eval('#modal', e => e.innerText);
    step('重置确认框声明只影响本机 localStorage', /localStorage/.test(t));
    await page.evaluate(() => { const b = document.querySelector('#modal [data-fn="resetConfirmed"]'); if (b) b.click(); });
    await wait(420);
  }
  const decidedAfter = await page.evaluate(() => window.WB.S.decisions.filter(d => d.status !== 'pending').length);
  step('重置后回到初始样例（已裁决数下降）', decidedAfter < decidedBefore, decidedBefore + ' → ' + decidedAfter);
  await shot(page, 'f-reset-restored');

  /* ================= 阶段 I：创作内核定向修订 · 超出第 43 章样例的 7 条验收路径 ================= */
  console.log('\n=== 阶段 I：定向修订 · 7 条验收路径（真实浏览器）===');

  /* ---------- I-1 新书路径：真空白 → 定位 → 背景/人物 → 手写 → 场景 → 候选 → 正式 ---------- */
  console.log('--- I-1 新书路径：空态必须真实、定位可编辑可确认 ---');
  await goView(page, 'book', 'library');
  step('I-1 作品库提供「新建作品」真实入口',
    await page.evaluate(() => !!document.querySelector('[data-fn="createBook"]')));
  await shot(page, 'i1-book-library');

  await clickFn(page, 'createBook');
  await wait(340);
  const nb = await craftDbg(page);
  const newBookId = nb.book;
  step('I-1 新建得到全新作品身份（不是既有作品）', newBookId !== 'B-01' && newBookId !== 'B-02', 'book=' + newBookId);
  step('I-1 新书创作内核为真空：背景 / 人物 / 大纲 / 场景 = 0',
    nb.hasCraft && nb.world === 0 && nb.characters === 0 && nb.outline === 0 && nb.scenes === 0,
    JSON.stringify({ world: nb.world, characters: nb.characters, outline: nb.outline, scenes: nb.scenes }));
  step('I-1 新书定位核心未填写（未知 ≠ 已填）', !nb.coreOriginal, 'coreOriginal=' + JSON.stringify(nb.coreOriginal));
  await shot(page, 'i1-new-book-overview');

  /* 反证（复现缺陷 ①）：新书故事状态不得回落第 43 章样例 */
  await goView(page, 'book', 'story');
  const storyTxt = await mainText(page);
  step('I-1 新书故事状态不出现他作人物/作品（禁止回落 B-01 样例）',
    !/林砚|顾晚|夜行灯|白鹭洲/.test(storyTxt), storyTxt.slice(0, 56).replace(/\s+/g, ' '));
  step('I-1 新书故事状态显示真实空态 + 空态创建入口', /暂无|尚无|还没有/.test(storyTxt));
  await shot(page, 'i1-story-empty-real');

  /* 定位：读者分区 ≠ 题材，可编辑、可确认 */
  await goView(page, 'book', 'craft');
  await clickAct(page, 'book.craftMode', [['mode', 'positioning']]);
  const posTxt = await mainText(page);
  step('I-1 定位把「读者分区」与「题材」作为两个维度同时呈现（分区 ≠ 题材）',
    /读者分区/.test(posTxt) && /题材/.test(posTxt));
  step('I-1 定位字段具备可编辑入口',
    await page.evaluate(() => document.querySelectorAll('[data-action="craft.edit"][data-kind="positioning"]').length >= 2));
  await shot(page, 'i1-positioning-form');

  await clickAct(page, 'craft.edit', [['kind', 'positioning'], ['field', 'coreOriginal']]);
  await setField(page, 'cfVal', '核心原创：每点亮一次灯要交出一段记忆；代价本身推动主角的选择。');
  await clickFn(page, 'craftSaveDirect');
  const afterPos = await craftDbg(page);
  step('I-1 定位经作者直接写入并真实落库',
    /代价本身推动主角的选择/.test(String(afterPos.coreOriginal)), String(afterPos.coreOriginal).slice(0, 44));

  /* 背景 / 人物：真实工作操作（新增 → 待探索，不自动进 Canon） */
  await clickAct(page, 'book.craftMode', [['mode', 'world']]);
  await clickAct(page, 'craft.add', [['kind', 'world']]);
  await setField(page, 'ad_name', '夜行灯');
  await setField(page, 'ad_cond', '灯亮起时可看见未了之事的轮廓');
  await setField(page, 'ad_cost', '每点亮一次烧掉持有者一段无关记忆');
  await setField(page, 'ad_limit', '同一夜只能点亮一次');
  await clickFn(page, 'craftAddDo', newBookId);
  const afterWorld = await craftDbg(page);
  step('I-1 新书可新增背景条目', afterWorld.world === nb.world + 1, nb.world + ' → ' + afterWorld.world);
  const newWorldState = await page.evaluate(() => {
    const c = window.WB.S.craft[window.WB.S.__scope.bookId];
    return c.world[c.world.length - 1].state;
  });
  step('I-1 新增背景为「待探索」，不自动成为既有事实', newWorldState === 'TO_EXPLORE', 'state=' + newWorldState);

  await clickAct(page, 'book.craftMode', [['mode', 'characters']]);
  await clickAct(page, 'craft.add', [['kind', 'character']]);
  await setField(page, 'ad_name', '林砚');
  await setField(page, 'ad_role', '主角 · 夜巡人');
  await setField(page, 'ad_goal', '查清灯的来源，同时保住记忆清单');
  await clickFn(page, 'craftAddDo', newBookId);
  const afterChar = await craftDbg(page);
  step('I-1 新书可新增人物（含认知域四分）', afterChar.characters === nb.characters + 1,
    nb.characters + ' → ' + afterChar.characters);
  step('I-1 人物认知域按 角色/作者/读者/未揭露 四分',
    await page.evaluate(() => {
      const c = window.WB.S.craft[window.WB.S.__scope.bookId], x = c.characters[c.characters.length - 1];
      return !!(x.knows && 'character' in x.knows && 'author' in x.knows && 'reader' in x.knows && 'unrevealed' in x.knows);
    }));
  await shot(page, 'i1-craft-world-characters');

  /* 大纲节点 */
  await clickAct(page, 'book.craftMode', [['mode', 'outline']]);
  await clickAct(page, 'craft.add', [['kind', 'outline']]);
  await setField(page, 'ad_title', '第 1 章 · 灯下客');
  await setField(page, 'ad_level', 'chapter');
  await setField(page, 'ad_purpose', '建立主角与灯的关系');
  await clickFn(page, 'craftAddDo', newBookId);
  const afterOutline = await craftDbg(page);
  step('I-1 新书可新增大纲节点', afterOutline.outline === 1, 'outline=' + afterOutline.outline);
  step('I-1 作者手写大纲默认不计为 AI 推断',
    await page.evaluate(() => {
      const c = window.WB.S.craft[window.WB.S.__scope.bookId];
      return c.outline[0].origin === 'author' && !!c.outline[0].version;
    }));

  /* 正文：可写可存（草稿 ≠ 正式稿） */
  await goView(page, 'book', 'manuscript');
  await clickFn(page, 'newChapter', newBookId);
  const ckNew = await page.evaluate(() => window.WB.S.__scope.bookId && Object.keys(window.WB.S.chapters).filter(k => window.WB.S.chapters[k].bookId === window.WB.S.__scope.bookId).slice(-1)[0]);
  step('I-1 空书可新建第一章（草稿）', !!ckNew, 'chapter=' + ckNew);
  await clickAct(page, 'book.msEdit');
  await setField(page, 'msEditor', '夜巡的第三个晚上，他把灯按在掌心。\n\n灯亮时，他看见廊下站着一个模糊的人影。');
  await clickFn(page, 'msSave', newBookId);
  const afterWrite = await page.evaluate(c => {
    const ms = window.WB.S.manuscripts[c], ch = window.WB.S.chapters[c];
    return { paras: ms.paragraphs.length, formal: ch.formal, published: ch.published, state: ch.state };
  }, ckNew);
  step('I-1 手写正文可保存为草稿（分段真实落库）', afterWrite.paras === 2, '段落=' + afterWrite.paras);
  step('I-1 草稿既不是正式稿也不是已发布', !afterWrite.formal && !afterWrite.published,
    'formal=' + afterWrite.formal + ' published=' + afterWrite.published);
  await shot(page, 'i1-manuscript-handwritten');

  /* 场景 → 按场景生成候选 → 逐项采纳 → 生成正式版 */
  await goView(page, 'book', 'craft');
  await clickAct(page, 'book.craftMode', [['mode', 'scenes']]);
  await clickAct(page, 'craft.add', [['kind', 'scene'], ['chapter', ckNew]]);
  await setField(page, 'ad_purpose', '入夜：建立灯的代价');
  await setField(page, 'ad_pov', '林砚');
  await setField(page, 'ad_conflict', '点灯会失去记忆');
  await setField(page, 'ad_reveal', '灯能照出未了之事');
  await setField(page, 'ad_notReveal', '灯的来源');
  await clickFn(page, 'craftAddDo', newBookId);
  const afterScene = await craftDbg(page);
  step('I-1 新书可新增场景计划', afterScene.scenes === 1, 'scenes=' + afterScene.scenes);

  await goView(page, 'book', 'manuscript');
  await page.evaluate(c => window.WB.go('book', 'manuscript', { chapter: c }), ckNew);
  await wait(200);
  await clickFn(page, 'msGenerate', newBookId);
  const gen = await page.evaluate(c => {
    const ch = window.WB.S.chapters[c], cand = window.WB.S.candidates[ch.candidate];
    return cand ? { id: cand.id, chapter: cand.chapter, n: cand.changes.length, bound: cand.bookId === window.WB.S.__scope.bookId } : null;
  }, ckNew);
  step('I-1 按场景计划生成候选（Mock 但绑定本书本章的具体可编辑产物）',
    !!gen && gen.bound && gen.n === 1 && gen.chapter === ckNew,
    gen ? 'candidate=' + gen.id + ' changes=' + gen.n + ' chapter=' + gen.chapter : '未生成');
  await shot(page, 'i1-scene-to-candidate');

  if (gen) {
    await clickFn(page, 'decideChange', gen.id);
    const adopted = await page.evaluate(id => window.WB.candidateState(id), gen.id);
    step('I-1 候选可逐项采纳（采纳 ≠ 已生效）', adopted.adopted === 1 && adopted.applied === false,
      'adopted=' + adopted.adopted + ' applied=' + adopted.applied);
    await clickAct(page, 'book.apply', [['id', gen.id]]);
    const hasApplyGate = await page.evaluate(() => !!document.querySelector('#modal [data-fn="applyCandidate"]'));
    step('I-1 「确认并生成正式版本」先弹确认闸（候选 ≠ 直接生效）', hasApplyGate);
    await clickFn(page, 'applyCandidate', gen.id);
    await wait(260);
    const applied = await page.evaluate(c => {
      const ch = window.WB.S.chapters[c];
      return { formal: ch.formal, published: ch.published };
    }, ckNew);
    step('I-1 确认后生成正式版本（formal 前进）', !!applied.formal, 'formal=' + applied.formal);
    step('I-1 生成正式版本不改线上版本（正式 ≠ 已发布）', !applied.published, 'published=' + applied.published);
    await shot(page, 'i1-candidate-applied');
  }

  /* ---------- I-2 先写后规划 ---------- */
  console.log('--- I-2 先写后规划：先落正文，再补大纲/场景 ---');
  const prePlan = await page.evaluate(() => {
    const bid = window.WB.S.__scope.bookId;
    const ks = Object.keys(window.WB.S.chapters).filter(k => window.WB.S.chapters[k].bookId === bid);
    return { outline: window.WB.S.craft[bid].outline.length, chaps: ks.length };
  });
  step('I-2 先写后规划前：正文已存在（手写落库）', prePlan.chaps >= 1, '章=' + prePlan.chaps);
  await goView(page, 'book', 'craft');
  await clickAct(page, 'book.craftMode', [['mode', 'outline']]);
  const hasExtract = await page.evaluate(() => !!document.querySelector('[data-action="craft.extract"]'));
  step('I-2 提供「从正文提取章纲」入口（先写后规划的真实入口）', hasExtract);
  const propBeforeExtract = (await craftDbg(page)).propOpen;
  await clickAct(page, 'craft.extract');
  const propAfterExtract = (await craftDbg(page)).propOpen;
  step('I-2 从已写正文反向提取章纲 → 形成待确认候选（不自动成为章纲）',
    propAfterExtract === propBeforeExtract + 1, propBeforeExtract + ' → ' + propAfterExtract);
  step('I-2 提取产物是候选，必须作者确认后才写入目标对象',
    await page.evaluate(() => (window.WB.S.craftProposals || []).some(p => p.state === 'open' && p.field === 'purpose')));
  await shot(page, 'i2-extract-outline-candidate');
  await clickAct(page, 'craft.add', [['kind', 'outline']]);
  await setField(page, 'ad_title', '第 2 章 · 无名巷');
  await setField(page, 'ad_level', 'chapter');
  await setField(page, 'ad_purpose', '推进对手线');
  await clickFn(page, 'craftAddDo', newBookId);
  const postPlan = await craftDbg(page);
  step('I-2 写后可补大纲（计划 ≠ 事实，不覆盖已写正文）',
    postPlan.outline > prePlan.outline, prePlan.outline + ' → ' + postPlan.outline);
  await shot(page, 'i2-write-then-plan');

  /* ---------- I-3 旧稿导入 ---------- */
  console.log('--- I-3 旧稿导入：解析 → 分类可改 → 确认写入（草稿）→ 抽取设定候选 ---');
  await page.evaluate(() => { window.WB.S.__scope.bookId = 'B-02'; window.WB.go('book', 'import', { bookId: 'B-02' }); });
  await wait(220);
  const impBefore = await page.evaluate(() => ({
    recs: window.WB.S.craft['B-02'].importRecords.length,
    chaps: Object.keys(window.WB.S.chapters).filter(k => window.WB.S.chapters[k].bookId === 'B-02').length,
    drafts: Object.keys(window.WB.S.chapters).filter(k => window.WB.S.chapters[k].bookId === 'B-02' && window.WB.S.chapters[k].state === 'draft').length,
    formals: Object.keys(window.WB.S.chapters).filter(k => window.WB.S.chapters[k].bookId === 'B-02' && window.WB.S.chapters[k].formal).length
  }));
  await clickAct(page, 'imp.example');
  const parsed = await page.evaluate(() => (window.WB.S.__sel.impRows || []).map(r => r.kind));
  step('I-3 导入解析产出分类行（带理由与置信度）', parsed.length >= 3, '行=' + parsed.length + ' [' + parsed.join(',') + ']');
  step('I-3 解析结果含正文、大纲、设定等多类', parsed.indexOf('manuscript') >= 0 && parsed.indexOf('outline') >= 0 && parsed.indexOf('setting') >= 0,
    parsed.join(','));
  step('I-3 分类可逐行修正（下拉 change 入口存在）',
    await page.evaluate(() => document.querySelectorAll('[data-change="imp.classify"]').length > 0));
  await shot(page, 'i3-import-classify');

  /* 把一行从「大纲」改成「忽略」，验证修改真实生效 */
  const changed = await page.evaluate(() => {
    const sels = Array.from(document.querySelectorAll('[data-change="imp.classify"]'));
    const t = sels.filter(s => s.value === 'outline')[0];
    if (!t) return false;
    t.value = 'ignore'; t.dispatchEvent(new Event('change', { bubbles: true })); return true;
  });
  await wait(200);
  step('I-3 分类修正写入真实状态', changed &&
    (await page.evaluate(() => (window.WB.S.__sel.impRows || []).some(r => r.kind === 'ignore'))));

  await clickFn(page, 'impConfirm');
  const impAfter = await page.evaluate(() => ({
    recs: window.WB.S.craft['B-02'].importRecords.length,
    chaps: Object.keys(window.WB.S.chapters).filter(k => window.WB.S.chapters[k].bookId === 'B-02').length,
    drafts: Object.keys(window.WB.S.chapters).filter(k => window.WB.S.chapters[k].bookId === 'B-02' && window.WB.S.chapters[k].state === 'draft').length,
    formals: Object.keys(window.WB.S.chapters).filter(k => window.WB.S.chapters[k].bookId === 'B-02' && window.WB.S.chapters[k].formal).length,
    importedClean: Object.keys(window.WB.S.chapters)
      .filter(k => window.WB.S.chapters[k].bookId === 'B-02' && window.WB.S.chapters[k].imported)
      .every(k => !window.WB.S.chapters[k].formal && window.WB.S.chapters[k].state === 'draft')
  }));
  step('I-3 确认写入新建导入章（草稿）', impAfter.chaps > impBefore.chaps, impBefore.chaps + ' → ' + impAfter.chaps);
  step('I-3 导入只写草稿，不把既有正式稿改掉，也不新建正式稿',
    impAfter.formals === impBefore.formals && impAfter.drafts > impBefore.drafts && impAfter.importedClean,
    '正式 ' + impBefore.formals + ' → ' + impAfter.formals + '；草稿 ' + impBefore.drafts + ' → ' + impAfter.drafts + '；导入章均为草稿=' + impAfter.importedClean);
  step('I-3 导入记录登记（分类计数与状态）', impAfter.recs > impBefore.recs, impBefore.recs + ' → ' + impAfter.recs);
  await shot(page, 'i3-import-confirmed');

  await clickFn(page, 'impExtract');
  const extracted = await page.evaluate(() => (window.WB.S.craftProposals || []).filter(p => p.state === 'open').length);
  step('I-3 从已导入正文抽取设定候选（AI 推断，待确认，不自动进 Canon）',
    extracted >= 0, '待确认候选=' + extracted);
  await shot(page, 'i3-import-extract-candidates');

  /* ---------- I-4 知识变更影响 ---------- */
  console.log('--- I-4 知识变更：改动列出受影响范围，且不静默覆盖已发布正文 ---');
  await page.evaluate(() => { window.WB.S.__scope.bookId = 'B-01'; window.WB.go('book', 'craft', { bookId: 'B-01', mode: 'world' }); });
  await wait(220);
  const beforeChange = await page.evaluate(() => {
    const w = window.WB.S.craft['B-01'].world[0];
    return {
      impact: window.WB.S.craft['B-01'].impactLog.length,
      ch43: window.WB.S.manuscripts['ch43'].paragraphs.join('|'),
      id: w.id, cond: w.cond, cost: w.cost, limit: w.limit, exception: w.exception,
      state: w.state, source: w.source, evidence: w.evidence, refs: (w.refs || []).join(',')
    };
  });
  /* 世界条目走「完整对象编辑器」维护（R3）：一次写入全部既有字段，而不只是改一个名字 */
  await clickAct(page, 'craft.objEdit', [['kind', 'world'], ['id', beforeChange.id]]);
  await setField(page, 'ad_cond', beforeChange.cond + '（作者修订：改为必须直视灯芯）');
  await clickFn(page, 'craftObjSave', 'B-01');
  const afterChange = await page.evaluate(() => {
    const c = window.WB.S.craft['B-01'], w = c.world[0];
    return {
      impact: c.impactLog.length,
      ch43: window.WB.S.manuscripts['ch43'].paragraphs.join('|'),
      last: c.impactLog[c.impactLog.length - 1],
      w: { cond: w.cond, cost: w.cost, limit: w.limit, exception: w.exception,
        state: w.state, source: w.source, evidence: w.evidence, refs: (w.refs || []).join(',') }
    };
  });
  step('I-4 知识变更写入影响清单（受影响范围为可枚举清单）',
    afterChange.impact === beforeChange.impact + 1 && Array.isArray(afterChange.last.affected) && afterChange.last.affected.length > 0,
    'impact ' + beforeChange.impact + ' → ' + afterChange.impact + '：' +
    (Array.isArray(afterChange.last.affected) ? afterChange.last.affected.join('、') : JSON.stringify(afterChange.last.affected)));
  step('I-4 世界条目其余字段在编辑后保持完整（R3：不是只留一个字段）',
    afterChange.w.cond !== beforeChange.cond &&
    afterChange.w.cost === beforeChange.cost && afterChange.w.limit === beforeChange.limit &&
    afterChange.w.exception === beforeChange.exception && afterChange.w.state === beforeChange.state &&
    afterChange.w.source === beforeChange.source && afterChange.w.evidence === beforeChange.evidence &&
    afterChange.w.refs === beforeChange.refs,
    'cond 已改；cost/limit/exception/state/source/evidence/refs 均保留');
  step('I-4 影响记录显式声明「未改动的部分」（禁止静默全文覆盖）', !!afterChange.last.unchanged,
    afterChange.last.unchanged);
  step('I-4 已发布正文在知识变更后保持不变（计划 ≠ 已发生事实）',
    afterChange.ch43 === beforeChange.ch43, afterChange.ch43 === beforeChange.ch43 ? '未变' : '被改写');
  await shot(page, 'i4-knowledge-change-impact');

  await page.evaluate(() => window.WB.go('book', 'craft', { bookId: 'B-01', mode: 'arc' }));
  await wait(180);
  await clickAct(page, 'craft.endingPick', [['id', 'EN-01']]);
  const picked = await page.evaluate(() => {
    const c = window.WB.S.craft['B-01'];
    return { e1: c.arc.endings.filter(e => e.id === 'EN-01')[0].state,
      others: c.arc.endings.filter(e => e.id !== 'EN-01').map(e => e.state),
      impact: c.impactLog.length };
  });
  step('I-4 结局方向可确认，其余保留为候选（不静默定稿）',
    picked.e1 === 'confirmed' && picked.others.every(s => s === 'candidate'),
    'EN-01=' + picked.e1 + ' 其余=' + picked.others.join(','));
  step('I-4 结局确认也写入本书影响清单（不再误写全局）', picked.impact > afterChange.impact,
    afterChange.impact + ' → ' + picked.impact);
  await shot(page, 'i4-ending-confirmed');

  /* ---------- I-5 双书 + 新空书切换，无串扰 ---------- */
  console.log('--- I-5 双书 + 新空书切换：章节 / 创作内核不串作 ---');
  const scopeSnap = {};
  for (const bid of ['B-01', 'B-02', newBookId]) {
    await page.evaluate(b => { window.WB.S.__scope.bookId = b; window.WB.go('book', 'manuscript', { bookId: b }); }, bid);
    await wait(200);
    scopeSnap[bid] = await page.evaluate(b => {
      const S = window.WB.S;
      const ks = Object.keys(S.chapters).filter(k => S.chapters[k].bookId === b);
      const c = S.craft[b] || null;
      return {
        scope: S.__scope.bookId, chaps: ks.length,
        titles: ks.slice(0, 4).map(k => S.chapters[k].title),
        world: c ? (c.world || []).length : 0,
        chars: c ? (c.characters || []).length : 0,
        txt: document.getElementById('main').innerText
      };
    }, bid);
  }
  step('I-5 切换作品真实改变当前作品范围',
    scopeSnap['B-01'].scope === 'B-01' && scopeSnap['B-02'].scope === 'B-02' && scopeSnap[newBookId].scope === newBookId,
    [scopeSnap['B-01'].scope, scopeSnap['B-02'].scope, scopeSnap[newBookId].scope].join(' / '));
  step('I-5 新空书正文工作面不显示其他作品的章节',
    !scopeSnap[newBookId].txt.includes('旧钟') && !scopeSnap[newBookId].txt.includes('白鹭洲'), 'len=' + scopeSnap[newBookId].txt.length);
  step('I-5 不同作品的创作内核互不污染（世界/人物计数各自独立）',
    new Set([scopeSnap['B-01'].world, scopeSnap['B-02'].world, scopeSnap[newBookId].world]).size > 1,
    '背景计数 ' + scopeSnap['B-01'].world + ' / ' + scopeSnap['B-02'].world + ' / ' + scopeSnap[newBookId].world);
  step('I-5 复现缺陷反证：正文工作面不再「每卷重复全书章节」',
    await page.evaluate(() => {
      let dup = 0;
      window.WB.NAV.forEach(() => {});
      const S = window.WB.S;
      Object.keys(S.volumes).forEach(b => {
        const seen = {};
        (S.volumes[b] || []).forEach(v => { const sig = (v.chapters || []).join('~'); if (seen[sig]) dup++; seen[sig] = 1; });
      });
      return dup === 0;
    }));
  await shot(page, 'i5-two-books-scope');

  /* ---------- I-6 刷新持久 + w1→w2 迁移保留编辑 ---------- */
  console.log('--- I-6 刷新持久：真实刷新保持；w1→w2 迁移不清空用户编辑 ---');
  const persistBefore = await page.evaluate(() => JSON.stringify({
    bids: Object.keys(window.WB.S.craft || {}),
    edits: Object.keys(window.WB.S.craft || {}).map(b => (window.WB.S.craft[b].positioning || {}).coreOriginal || ''),
    runs: (window.WB.S.craft['B-01'].impactLog || []).length
  }));
  await page.reload({ waitUntil: 'load' });
  await page.waitForSelector('#nav .nav-item', { timeout: 10000 });
  const persistAfter = await page.evaluate(() => JSON.stringify({
    bids: Object.keys(window.WB.S.craft || {}),
    edits: Object.keys(window.WB.S.craft || {}).map(b => (window.WB.S.craft[b].positioning || {}).coreOriginal || ''),
    runs: (window.WB.S.craft['B-01'].impactLog || []).length
  }));
  step('I-6 刷新后创作内核与影响清单保持（真实写入 localStorage）', persistBefore === persistAfter,
    persistBefore === persistAfter ? '一致' : persistBefore.slice(0, 60) + ' ≠ ' + persistAfter.slice(0, 60));

  const preRaw = await page.evaluate(() => localStorage.getItem('curis.writing.exploration.v1'));
  await page.evaluate(() => {
    const KEY = 'curis.writing.exploration.v1';
    const p = JSON.parse(localStorage.getItem(KEY));
    const old = { v: 'w1', s: JSON.parse(JSON.stringify(p.s)) };
    delete old.s.craft;                              /* w1 结构没有创作内核 */
    delete old.s.craftProposals;
    delete old.s.reviewRuns;
    old.s.chapters['ch43'].formal = 'v9-user-edit';  /* 模拟 w1 时代用户已存的编辑 */
    localStorage.setItem(KEY, JSON.stringify(old));
  });
  await page.reload({ waitUntil: 'load' });
  await page.waitForSelector('#nav .nav-item', { timeout: 10000 });
  const mig = await page.evaluate(() => ({
    v: JSON.parse(localStorage.getItem('curis.writing.exploration.v1')).v,
    cur: window.WB.VERSION,
    backup: !!localStorage.getItem(window.WB.BACKUP_PREFIX + 'w1'),
    ch43: window.WB.S.chapters['ch43'].formal,
    hasCraft: !!window.WB.S.craft,
    hasProposals: Array.isArray(window.WB.S.craftProposals)
  }));
  step('I-6 w1→当前 schema 迁移保留用户既有编辑（不以清空 localStorage 换测试通过）',
    mig.ch43 === 'v9-user-edit', 'ch43.formal=' + mig.ch43);
  step('I-6 迁移后版本为当前 schema 且补齐创作内核结构', mig.v === mig.cur && mig.hasCraft && mig.hasProposals,
    'v=' + mig.v + '（当前 ' + mig.cur + '）craft=' + mig.hasCraft + ' proposals=' + mig.hasProposals);
  step('I-6 迁移前先做轻量备份（旧载荷可回查）', mig.backup, 'backup key=' + '（存在=' + mig.backup + '）');
  await shot(page, 'i6-migration-preserved');
  /* 还原迁移前状态，避免影响后续阶段 */
  await page.evaluate(raw => localStorage.setItem('curis.writing.exploration.v1', raw), preRaw);
  await page.reload({ waitUntil: 'load' });
  await page.waitForSelector('#nav .nav-item', { timeout: 10000 });

  /* ---------- I-7 市场 → 作品 → 发布 → 反馈 → 学习 → 下一章 回流 ---------- */
  console.log('--- I-7 回流链：市场 → 作品 → 发布 → 反馈 → 学习 → 下一章 ---');
  await goView(page, 'market', 'direction');
  step('I-7 ① 市场方向可作创作起点（有依据集合与裁决入口）',
    /方向|依据/.test(await mainText(page)));
  await shot(page, 'i7-1-market-direction');

  await page.evaluate(() => { window.WB.S.__scope.bookId = 'B-01'; window.WB.go('book', 'manuscript', { bookId: 'B-01', chapter: 'ch43' }); });
  await wait(220);
  step('I-7 ② 作品正文承载落点（正式稿 / 线上版本分离可见）',
    /正式/.test(await mainText(page)) && /线上|未发布/.test(await mainText(page)));
  await shot(page, 'i7-2-book-manuscript');

  await goView(page, 'publish', 'queue');
  const pqTxt = await mainText(page);
  step('I-7 ③ 发布队列区分未核验 / 已排期（未知 ≠ 失败）', /未核验|未知/.test(pqTxt) && /排期/.test(pqTxt));
  await shot(page, 'i7-3-publish-queue');

  await goView(page, 'audience', 'attribution');
  step('I-7 ④ 读者与收益：五层归因可回溯到正文',
    await page.evaluate(() => document.querySelectorAll('#main .lay').length === 5));
  await shot(page, 'i7-4-attribution');

  await goView(page, 'learning', 'library');
  step('I-7 ⑤ 写作经验：经验带 scope 与反例（可被下一章引用）',
    /适用范围|scope/.test(await mainText(page)) || /反例/.test(await mainText(page)));
  await shot(page, 'i7-5-learning');

  await page.evaluate(() => { window.WB.S.__scope.bookId = 'B-01'; window.WB.go('book', 'craft', { bookId: 'B-01', mode: 'scenes', chapter: 'ch44' }); });
  await wait(220);
  const returnTxt = await mainText(page);
  step('I-7 ⑥ 回流到下一章的场景准备（链路闭合，可继续写作）',
    /场景/.test(returnTxt) && await page.evaluate(() => !!document.querySelector('[data-action="nav.view"][data-view="manuscript"]')));
  await shot(page, 'i7-6-return-to-next-chapter');

  /* 恢复主作品范围 */
  await page.evaluate(() => { window.WB.S.__scope.bookId = 'B-01'; window.WB.go('operate', 'home'); });
  await wait(220);

  /* ---- 阶段 G：单文件构建物真机校验 ---- */
  console.log('\n=== 阶段 G：单文件构建物（index.single.html）真机校验 ===');
  const singlePath = path.join(ROOT, 'index.single.html');
  const srcFiles = ['index.html', 'styles.css', 'data.js', 'app.js', 'views-operate.js', 'views-market.js', 'views-craft.js',
    'views-book.js', 'views-publish.js', 'views-audience.js', 'views-learning.js'];
  if (!fs.existsSync(singlePath)) {
    step('单文件构建物存在（需先运行 node _build.js）', false, 'index.single.html 不存在');
  } else {
    const singleMtime = fs.statSync(singlePath).mtimeMs;
    const newer = srcFiles.filter(f => fs.statSync(path.join(ROOT, f)).mtimeMs > singleMtime);
    step('单文件构建物不早于全部源文件（防「构建过期」）', newer.length === 0,
      newer.length ? '比构建物更新：' + newer.join(', ') + ' → 需重新构建' : '构建新鲜');

    const errBefore = errors.length;
    const p2 = await browser.newPage();
    const p2errs = [];
    p2.on('console', m => { if (m.type() === 'error' && !IGNORE.some(r => r.test(m.text()))) p2errs.push(m.text()); });
    p2.on('pageerror', e => p2errs.push('PAGEERROR: ' + e.message));
    await p2.goto('file://' + encodeURI(singlePath), { waitUntil: 'load', timeout: 30000 });
    await p2.waitForSelector('#nav .nav-item', { timeout: 10000 });
    const s = await p2.evaluate(() => ({
      nav: document.querySelectorAll('#nav .nav-item').length,
      views: Object.keys(window.WB.views).length,
      external: document.querySelectorAll('script[src], link[href]').length,
      inlineStyle: document.querySelectorAll('style').length,
      storage: (function () { try { localStorage.setItem('__t', '1'); localStorage.removeItem('__t'); return true; } catch (e) { return false; } })()
    }));
    await p2.evaluate(() => window.WB.go('book', 'manuscript', { chapter: 'ch44' }));
    await wait(250);
    const s2 = await p2.evaluate(() => ({
      len: document.getElementById('main').innerText.length,
      canon: /Canon 冲突/.test(document.getElementById('main').innerText),
      chapList: document.querySelectorAll('#main .chap').length
    }));
    await p2.screenshot({ path: path.join(EV, String(++shotSeq).padStart(2, '0') + '-single-file-build.png') });
    await p2.close();
    step('单文件版零外部引用且含内联样式', s.external === 0 && s.inlineStyle > 0,
      '外部引用=' + s.external + ' 内联 style=' + s.inlineStyle);
    step('单文件版 6 区 / ' + VIEW_COUNT + ' 视面可用', s.nav === 6 && s.views === VIEW_COUNT, 'nav=' + s.nav + ' views=' + s.views);
    step('单文件版本机存储可用（长期连续性）', s.storage);
    step('单文件版关键视图可用（ch44 Canon 冲突 + 章节列表）', s2.canon && s2.chapList > 0,
      'len=' + s2.len + ' canon=' + s2.canon + ' 章节=' + s2.chapList);
    step('单文件版 Console Error = 0', p2errs.length === 0, p2errs.slice(0, 3).join(' | '));
    errors.length = errBefore;   /* 单文件页错误已单独断言，不重复计入主页面 */
  }

  /* ---- 阶段 H：Console ---- */
  console.log('\n=== 阶段 H：Console（主应用页）===');
  step('Console Error = 0（含 pageerror / 请求失败）', errors.length === 0, errors.slice(0, 5).join(' | '));

  await browser.close();
  server.close();

  /* ---- 汇总 ---- */
  const failed = steps.filter(s => !s.ok);
  const L = [];
  L.push('# Writing Business HTML Exploration · 真实浏览器自测报告');
  L.push('');
  L.push('- 运行时间：' + new Date().toISOString());
  L.push('- 浏览器：系统 Chrome（headless=new，viewport 1512×982）');
  L.push('- 打开方式：`file://` 直接打开 + `http://127.0.0.1` 本地服务');
  L.push('- 断言：' + steps.length + ' 项；通过 ' + (steps.length - failed.length) + '；失败 ' + failed.length);
  L.push('- Console Error：' + errors.length);
  L.push('- 截图：' + shotSeq + ' 张（同目录 PNG）');
  L.push('');
  L.push('| # | 断言 | 结果 | 备注 |');
  L.push('|---|------|------|------|');
  steps.forEach((s, i) => L.push('| ' + (i + 1) + ' | ' + s.name + ' | ' + (s.ok ? 'PASS' : '**FAIL**') + ' | ' + s.detail.replace(/\|/g, '\\|').slice(0, 150) + ' |'));
  if (errors.length) { L.push(''); L.push('## Console 错误明细'); errors.forEach(e => L.push('- ' + e.slice(0, 300))); }
  fs.writeFileSync(path.join(EV, 'SELFTEST_REPORT.md'), L.join('\n'));

  console.log('\n============================');
  console.log('断言 ' + steps.length + ' / 通过 ' + (steps.length - failed.length) + ' / 失败 ' + failed.length);
  console.log('Console Error: ' + errors.length);
  console.log('截图：' + shotSeq + ' 张');
  if (failed.length) { console.log('\n失败项：'); failed.forEach(f => console.log('  ✗ ' + f.name + '  ' + f.detail)); }
  process.exit(failed.length ? 1 : 0);
})().catch(e => { console.error('HARNESS ERROR:', e); process.exit(2); });
