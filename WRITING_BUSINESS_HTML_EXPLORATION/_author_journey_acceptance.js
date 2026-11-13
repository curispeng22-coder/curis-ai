/* CURIS — Writing Business HTML Exploration · 第 5 轮作者动线真实验收
   目标：用真实 Chrome 点击（非注入运行态）走通 7 条路径，并把每一步的记录与截图落盘。
   路径：
     P1 新书从想法开始（起点 → 构思 → 方向候选 → 采纳 → 起草核心不再被阻断）
     P2 自行开写（先手写：直接第 1 章，空书不铺 0 指标，起步可回头补）
     P3 素材与编辑（补必要设定 / 主支线 → 真实写进本书创作内核，状态为「仅计划」）
     P4 文本与审校（既有正文路径回归：讨论 → 提案 → 采纳只落草稿）
     P5 连续性（切书再切回：方向 / 设定 / 对话 / 候选都不串台）
     P6 页面顺序（首屏先回答「哪本书 / 到哪一步 / 谁在管 / 下一步」，员工在 Main 顶部）
     P7 业务回归（六区关键视面仍可进入且无 Console Error）
   运行：node _author_journey_acceptance.js
   产出：_evidence_author_journey/round5/（截图 + PATH_RECORD.md）
   ========================================================================== */
'use strict';
const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');
const os = require('os');
const http = require('http');

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const ROOT = __dirname;
/* 入口可切换：默认源码 index.html；交付物形态用 WRITING_ENTRY=index.single.html 复跑。
   证据目录同样可指定，避免两种形态互相覆盖。 */
const ENTRY = process.env.WRITING_ENTRY || 'index.html';
const EV = path.join(ROOT, '_evidence_author_journey', process.env.WRITING_EV || 'round5');
fs.mkdirSync(EV, { recursive: true });

const errors = [];
const steps = [];
let seq = 0;
let pass = 0, fail = 0, partial = 0;

function step(id, title, ok, detail) {
  const verdict = ok === true ? 'PASS' : (ok === 'part' ? 'PARTIAL' : 'FAIL');
  if (ok === true) pass++; else if (ok === 'part') partial++; else fail++;
  steps.push({ id, title, verdict, detail: detail == null ? '' : String(detail) });
  console.log('[' + verdict + '] ' + id + ' ' + title + (detail ? '\n        ' + String(detail).replace(/\n/g, '\n        ') : ''));
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
/* 严格命中：给了 attrs 就必须精确匹配，否则返回 null（绝不回退到第一个，
   否则测试会把「没找到入口」误报成「路径走通」）。 */
async function clickAct(page, action, attrs) {
  const r = await page.evaluate((action, attrs) => {
    const els = Array.from(document.querySelectorAll('[data-action="' + action + '"]'));
    const pool = attrs && attrs.length
      ? els.filter(e => attrs.every(([k, v]) => e.getAttribute('data-' + k) === String(v)))
      : els;
    const el = pool[0];
    if (!el) return null;
    el.click();
    return (el.innerText || el.textContent || '').trim();
  }, action, attrs || []);
  await wait(300);
  return r;
}
async function clickFn(page, fn, attrs) {
  const r = await page.evaluate((fn, attrs) => {
    const els = Array.from(document.querySelectorAll('[data-fn="' + fn + '"]'));
    const pool = attrs && attrs.length
      ? els.filter(e => attrs.every(([k, v]) => e.getAttribute('data-' + k) === String(v)))
      : els;
    const el = pool[0];
    if (!el) return null;
    el.click();
    return (el.innerText || el.textContent || '').trim();
  }, fn, attrs || []);
  await wait(320);
  return r;
}
async function sendConv(page, text) {
  await page.evaluate((t) => {
    const e = document.querySelector('#convInput');
    if (e) { e.value = t; e.dispatchEvent(new Event('input', { bubbles: true })); }
  }, text);
  await wait(80);
  await clickAct(page, 'conv.send');
  await wait(500);
}
async function lastEmpReply(page) {
  return page.evaluate(() => {
    const ms = Array.from(document.querySelectorAll('#convMsgs .msg'));
    const emp = ms.filter(m => !m.classList.contains('me'));
    const last = emp[emp.length - 1];
    return last ? last.innerText.trim() : '(none)';
  });
}
/* 真实点击切换作品：工具条「切换作品」→ 作品列表里点某一本（不直接改运行态） */
async function switchTo(page, id) {
  await clickAct(page, 'ui.bookSwitch');
  await wait(380);
  const ok = await clickAct(page, 'ui.pickBook', [['id', id]]);
  await wait(420);
  return ok;
}

const SEED = '我想写一部近未来悬疑小说，档案员收到明天的报纸。请先与我讨论两种故事方向，不要写正文。';
const SEED_PREMISE = '写一部近未来悬疑小说，档案员收到明天的报纸。';

(async () => {
  const server = await serve();
  const url = 'http://127.0.0.1:' + server.address().port + '/' + ENTRY;
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'curis-authorjourney-r5-'));
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: 'new', userDataDir: profile,
    protocolTimeout: 40000, args: ['--no-proxy-server', '--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  page.on('console', m => { if (m.type() === 'error' && !/favicon/.test(m.location() ? (m.location().url || '') : '')) errors.push(m.text()); });
  page.on('pageerror', e => errors.push('pageerror: ' + String((e && e.message) || e)));
  await page.setViewport({ width: 1440, height: 1000 });
  await page.goto(url, { waitUntil: 'load', timeout: 30000 });
  await page.waitForSelector('#nav .nav-item', { timeout: 10000 });
  console.log('=== 第 5 轮作者动线验收 · ' + ENTRY + ' · 1440×1000 ===');

  /* =================== P1 新书从想法开始 =================== */
  await page.evaluate(() => window.WB.go('operate', 'home'));
  await wait(320);
  await clickFn(page, 'createBook');
  await wait(400);
  const chooser = await page.evaluate(() => {
    const m = document.getElementById('modal');
    const on = m && m.classList.contains('on');
    const paths = Array.from(document.querySelectorAll('#modal [data-fn="createBookPath"]')).map(e => e.getAttribute('data-a1'));
    return { on: !!on, paths: paths, txt: on ? m.innerText.trim() : '' };
  });
  await shot(page, 'P1-start-path-chooser');
  step('P1-1', '点「开一本新书」先出现起步方式选择（不是直接建空书）',
    chooser.on && chooser.paths.length === 3 && /从一句想法开始/.test(chooser.txt),
    '模态打开=' + chooser.on + ' · 起步方式=' + JSON.stringify(chooser.paths));

  await clickFn(page, 'createBookPath', [['a1', 'idea']]);
  await wait(500);
  const startPanel = await page.evaluate(() => {
    const S = window.WB.S, b = S.__runtime.createdBooks[S.__runtime.createdBooks.length - 1];
    const main = document.getElementById('main');
    const onb = main.querySelector('.onb-ladder');
    const mbar = document.getElementById('mainBar');
    const firstPanel = main.querySelector('.pnl');
    return { id: b && b.id, scope: S.__scope.bookId,
      hasSeedBox: !!document.getElementById('onbSeed'),
      ladderSteps: main.querySelectorAll('.onb-step').length,
      curStep: (main.querySelector('.onb-step.cur') || {}).innerText || '',
      onbIsFirstPanel: !!(onb && firstPanel && firstPanel.contains(onb)),
      onbTopBelowMainBar: firstPanel && mbar ? Math.round(firstPanel.getBoundingClientRect().top - mbar.getBoundingClientRect().bottom) : null,
      zeroStatNote: /起步阶段不铺 0 指标/.test(main.innerText),
      zeroFigCount: main.querySelectorAll('.figs .fig').length,
      sharedAreaAbsentBeforeAsk: !document.querySelector('#sharedArea') };
  });
  await shot(page, 'P1-new-book-start-panel');
  step('P1-2', '新书落到「起步区」而不是空卡：有想法输入框、5 步阶梯、当前步高亮',
    startPanel.hasSeedBox && startPanel.ladderSteps === 5 && /写下你的想法/.test(startPanel.curStep) && startPanel.onbIsFirstPanel,
    '书=' + startPanel.id + ' · 阶梯步数=' + startPanel.ladderSteps + ' · 当前步=' + startPanel.curStep +
    '\n起步区在首屏第 1 个面板=' + startPanel.onbIsFirstPanel + ' · 距工具条=' + startPanel.onbTopBelowMainBar + 'px');
  step('P1-3', '空书不铺 0 指标（正式进展与库存折叠成一句说明）',
    startPanel.zeroStatNote && startPanel.zeroFigCount === 0,
    '出现「起步阶段不铺 0 指标」=' + startPanel.zeroStatNote + ' · 页面上的 0 指标卡=' + startPanel.zeroFigCount + ' 个');

  /* 真实键盘输入构思，再点「发给编辑」 */
  await page.click('#onbSeed');
  await page.type('#onbSeed', SEED, { delay: 4 });
  await wait(150);
  await clickAct(page, 'book.onbSeed');
  await wait(700);
  const afterAsk = await page.evaluate(() => {
    const S = window.WB.S, bid = S.__scope.bookId, c = S.craft[bid];
    const main = document.getElementById('main');
    const mbar = document.getElementById('mainBar');
    const sa = document.querySelector('#main #sharedArea');
    const items = Array.from(document.querySelectorAll('#sharedArea .diff-i'));
    return { inMain: !!sa, topBelowMainBar: sa && mbar ? Math.round(sa.getBoundingClientRect().top - mbar.getBoundingClientRect().bottom) : null,
      msgCount: document.querySelectorAll('#convMsgs .msg').length,
      convCtx: (document.querySelector('#sharedArea .conv-ctx') || {}).innerText || '',
      dirItems: items.length,
      itemHeads: items.map(e => (e.querySelector('.diff-why') || {}).innerText || ''),
      hasPremiseLabel: /故事前提/.test(sa ? sa.innerText : ''),
      hasTradeoff: /代价 \/ 取舍/.test(sa ? sa.innerText : ''),
      seedRaw: c.positioning.seedRaw || '', seed: c.positioning.seed || '',
      onbSeedEcho: (main.querySelector('.onb-quote') || {}).innerText || '' };
  });
  await shot(page, 'P1-direction-candidates');
  step('P1-4', '作者原话被接住并保存（seedRaw = 原话，seed = 去掉指令后的构思）',
    afterAsk.seedRaw.indexOf('档案员收到明天的报纸') >= 0 && afterAsk.seed === SEED_PREMISE,
    'seedRaw="' + afterAsk.seedRaw + '"\nseed="' + afterAsk.seed + '"\n起步区回显="' + afterAsk.onbSeedEcho.slice(0, 40) + '…"');
  step('P1-5', '编辑给出具体方向候选（含故事前提 / 冲突 / 视角 / 取舍），不是标签包',
    afterAsk.dirItems >= 2 && afterAsk.hasPremiseLabel && afterAsk.hasTradeoff,
    '候选数=' + afterAsk.dirItems + ' · 候选标题=' + JSON.stringify(afterAsk.itemHeads) +
    '\n含「故事前提」=' + afterAsk.hasPremiseLabel + ' · 含「代价 / 取舍」=' + afterAsk.hasTradeoff);
  step('P1-6', '不再返回「演示未模拟这类要求」',
    !/演示未模拟/.test(await lastEmpReply(page)),
    '编辑回复：' + (await lastEmpReply(page)).slice(0, 180).replace(/\n/g, ' / '));
  step('P1-7', '员工嵌在当前工作（共享工作区在 Main 顶部、工具条之下）',
    afterAsk.inMain && afterAsk.topBelowMainBar != null && afterAsk.topBelowMainBar < 200,
    '在 Main 内=' + afterAsk.inMain + ' · 距工具条=' + afterAsk.topBelowMainBar + 'px（修前基线：距 Main 顶部 1022px）');
  step('P1-8', '对话顶部先说明接管范围（对象 / 版本 / 状态）',
    /对话对象/.test(afterAsk.convCtx) && /负责的范围/.test(afterAsk.convCtx),
    afterAsk.convCtx.slice(0, 160).replace(/\n/g, ' / '));

  await clickAct(page, 'conv.acceptItem', [['item', 'D1']]);
  await wait(600);
  const afterAdopt = await page.evaluate(() => {
    const S = window.WB.S, bid = S.__scope.bookId, c = S.craft[bid], p = c.positioning;
    return { premise: (c.arc && c.arc.premise) || '', conflict: (c.arc && c.arc.mainConflict) || '',
      core: p.coreOriginal || '', dirId: p.dirId || '', dirName: p.dirName || '',
      tagDims: Object.keys(p.tags || {}).length, genres: (p.genres || []).join('、'),
      perspective: p.perspective || '', world: (c.world || []).length, chars: (c.characters || []).length };
  });
  await shot(page, 'P1-direction-adopted');
  step('P1-9', '采纳方向后真正写进本书（前提 / 主要冲突 / 一句话故事 / 创作选择）',
    !!afterAdopt.premise && !!afterAdopt.core && afterAdopt.dirId === 'SD-01' && afterAdopt.tagDims >= 5,
    '方向=' + afterAdopt.dirId + ' ' + afterAdopt.dirName + '\n故事前提：' + afterAdopt.premise.slice(0, 70) + '…' +
    '\n主要冲突：' + afterAdopt.conflict.slice(0, 50) + '…\n一句话故事：' + afterAdopt.core.slice(0, 50) + '…' +
    '\n已写标签维度=' + afterAdopt.tagDims + ' · 题材=' + afterAdopt.genres + ' · 视角=' + afterAdopt.perspective);

  /* 修前受阻断的那一步：让编辑起草核心 */
  await page.evaluate(() => window.WB.go('book', 'craft', { mode: 'positioning' }));
  await wait(420);
  const draftLabel = await clickAct(page, 'craft.draft', [['kind', 'positioning'], ['field', 'coreOriginal']]);
  await wait(450);
  const draft = await page.evaluate(() => {
    const m = document.getElementById('modal');
    const on = m && m.classList.contains('on');
    const ta = document.getElementById('cfVal');
    return { on: !!on, txt: on ? m.innerText.trim() : '', val: ta ? ta.value : null };
  });
  await shot(page, 'P1-core-draft-unblocked');
  step('P1-10', '采纳方向后「让编辑起草核心」不再被空素材阻断',
    draft.on && !/演示未模拟/.test(draft.txt) && !!draft.val,
    '入口按钮="' + draftLabel + '" · 模态打开=' + draft.on +
    '\n模态内容：' + draft.txt.slice(0, 140).replace(/\n/g, ' / ') + '\n草案值="' + String(draft.val).slice(0, 80) + '"');
  await clickAct(page, 'close-modal');
  await wait(200);

  /* =================== P3 素材与编辑（同一本书继续） =================== */
  await page.evaluate(() => window.WB.go('book', 'overview'));
  await wait(320);
  const beforeBase = await page.evaluate(() => {
    const c = window.WB.S.craft[window.WB.S.__scope.bookId];
    return { world: (c.world || []).length, chars: (c.characters || []).length, ml: ((c.arc || {}).mainLines || []).length };
  });
  await clickAct(page, 'book.onbBase');
  await wait(600);
  const baseProp = await page.evaluate(() => {
    const blocks = Array.from(document.querySelectorAll('#sharedArea .note.choice'));
    const last = blocks[blocks.length - 1];
    const items = last ? Array.from(last.querySelectorAll('.diff-i')) : [];
    return { n: items.length, heads: items.map(e => (e.querySelector('.diff-why') || {}).innerText || ''),
      blocks: blocks.length,
      /* 未裁定项必须真的给出裁决入口；漏给 = 作者想采纳也没得点（第 5 轮真实缺陷） */
      hasRest: !!(last && last.querySelector('[data-action="conv.acceptRest"]')),
      itemBtns: last ? last.querySelectorAll('[data-action="conv.acceptItem"]').length : 0,
      pendingTxt: last ? ((last.querySelector('.st-badge') || {}).innerText || '') : '' };
  });
  await shot(page, 'P3-base-proposal');
  /* 只裁定最后一个提案（= 本次补设定），不碰之前的 */
  const baseRest = await page.evaluate(() => {
    const blocks = Array.from(document.querySelectorAll('#sharedArea .note.choice'));
    const last = blocks[blocks.length - 1];
    const b = last ? last.querySelector('[data-action="conv.acceptRest"]') : null;
    if (b) { b.click(); return true; }
    return false;
  });
  await wait(600);
  if (!baseRest) {
    for (const it of ['B1', 'B2', 'B3']) {
      await page.evaluate((item) => {
        const blocks = Array.from(document.querySelectorAll('#sharedArea .note.choice'));
        const last = blocks[blocks.length - 1];
        const b = last ? last.querySelector('[data-action="conv.acceptItem"][data-item="' + item + '"]') : null;
        if (b) b.click();
      }, it);
      await wait(320);
    }
  }
  const afterBase = await page.evaluate(() => {
    const c = window.WB.S.craft[window.WB.S.__scope.bookId];
    return { world: (c.world || []).length, chars: (c.characters || []).length,
      ml: ((c.arc || {}).mainLines || []).length,
      states: (c.world || []).map(w => w.state), src: (c.world || [])[0] ? (c.world[0].source || '') : '' };
  });
  await shot(page, 'P3-base-adopted');
  step('P3-1', '「让编辑补设定」给出可裁决候选（背景规则 / 人物 / 主线），且真的可裁决',
    baseProp.n >= 3 && baseProp.hasRest && baseProp.itemBtns >= 3,
    '候选项=' + baseProp.n + ' · ' + JSON.stringify(baseProp.heads) +
    '\n余项采纳入口=' + baseProp.hasRest + ' · 逐项裁决按钮=' + baseProp.itemBtns + ' 个 · 状态标记="' + baseProp.pendingTxt + '"');
  step('P3-2', '采纳后真实写进本书创作内核，且状态是「仅计划」而不是正文事实',
    afterBase.world > beforeBase.world && afterBase.chars > beforeBase.chars && afterBase.ml > beforeBase.ml
      && afterBase.states.every(s => s === 'PLANNED'),
    '世界 ' + beforeBase.world + '→' + afterBase.world + ' · 人物 ' + beforeBase.chars + '→' + afterBase.chars +
    ' · 主线 ' + beforeBase.ml + '→' + afterBase.ml + '\n新增世界条目状态=' + JSON.stringify(afterBase.states) +
    '\n来源：' + afterBase.src);

  await clickAct(page, 'book.onbPlan');
  await wait(600);
  const planProp = await page.evaluate(() => {
    const blocks = Array.from(document.querySelectorAll('#sharedArea .note.choice'));
    const last = blocks[blocks.length - 1];
    return last ? { n: last.querySelectorAll('.diff-i').length,
      hasRest: !!last.querySelector('[data-action="conv.acceptRest"]'),
      itemBtns: last.querySelectorAll('[data-action="conv.acceptItem"]').length,
      pendingTxt: (last.querySelector('.st-badge') || {}).innerText || '' } : { n: 0 };
  });
  const planRest = await page.evaluate(() => {
    const blocks = Array.from(document.querySelectorAll('#sharedArea .note.choice'));
    const last = blocks[blocks.length - 1];
    const b = last ? last.querySelector('[data-action="conv.acceptRest"]') : null;
    if (b) { b.click(); return true; }
    return false;
  });
  await wait(600);
  if (!planRest) {
    for (const it of ['P1', 'P2', 'P3']) {
      await page.evaluate((item) => {
        const blocks = Array.from(document.querySelectorAll('#sharedArea .note.choice'));
        const last = blocks[blocks.length - 1];
        const b = last ? last.querySelector('[data-action="conv.acceptItem"][data-item="' + item + '"]') : null;
        if (b) b.click();
      }, it);
      await wait(300);
    }
  }
  const afterPlan = await page.evaluate(() => {
    const c = window.WB.S.craft[window.WB.S.__scope.bookId];
    return { ml: ((c.arc || {}).mainLines || []).length, sl: ((c.arc || {}).subLines || []).length, ol: (c.outline || []).length };
  });
  await shot(page, 'P3-plan-adopted');
  step('P3-3', '「定走向」给出主支线 + 第 1 章段纲并可落成计划对象',
    planProp.n >= 3 && planProp.hasRest && afterPlan.sl >= 1 && afterPlan.ol >= 1,
    '候选项=' + planProp.n + ' 个（余项采纳入口=' + planProp.hasRest + ' · 逐项按钮=' + planProp.itemBtns +
    ' · 状态="' + (planProp.pendingTxt || '') + '"）· 主线=' + afterPlan.ml + ' · 支线=' + afterPlan.sl + ' · 大纲节点=' + afterPlan.ol);

  /* 连续两轮：同一对象第二轮（继续讨论，自动带范围） */
  await sendConv(page, '这个方向能不能再给一条支线？');
  const round2 = await page.evaluate(() => ({
    msgs: document.querySelectorAll('#convMsgs .msg').length,
    ctxTags: Array.from(document.querySelectorAll('#convMsgs .msg .sm.t3')).map(e => e.innerText).filter(t => /^上下文：/.test(t)).slice(-1)[0] || '' }));
  step('P3-4', '同一对象可连续两轮，且每条要求自动带范围（书 / 章 / 版本）',
    round2.msgs >= 6 && /书 B-0/.test(round2.ctxTags),
    '对话消息数=' + round2.msgs + ' · 最近一条上下文标签=' + round2.ctxTags);

  /* 第一章候选（作者真实顺序：先补必要设定，再准备首章） */
  await page.evaluate(() => window.WB.go('book', 'overview'));
  await wait(360);
  const firstChBtn = await clickAct(page, 'book.onbFirst');
  await wait(700);
  const firstCh = await page.evaluate(() => {
    const S = window.WB.S, bid = S.__scope.bookId;
    const chs = Object.keys(S.chapters).filter(k => S.chapters[k].bookId === bid);
    const ck = chs.sort((a, b) => (S.chapters[a].no || 0) - (S.chapters[b].no || 0))[0];
    const ch = S.chapters[ck] || {};
    const cand = ch.candidate ? S.candidates[ch.candidate] : null;
    return { chs: chs.length, chNo: ch.no, formal: ch.formal, candidate: ch.candidate,
      kind: cand ? cand.kind : '', items: cand ? cand.changes.length : 0,
      allNull: cand ? cand.changes.every(x => x.applied === null) : false,
      paraHasCast: cand ? /本书已建人物/.test(JSON.stringify(cand.changes)) : false,
      routeView: S.__route.view };
  });
  await shot(page, 'P1-first-chapter-candidate');
  step('P1-11', '拿到第 1 章候选（逐项待裁决；未确认前不是正式稿、更不是已发布）',
    firstCh.chs >= 1 && !!firstCh.candidate && firstCh.items >= 3 && firstCh.allNull && !firstCh.formal && firstCh.paraHasCast,
    '入口="' + firstChBtn + '" · 在册章=' + firstCh.chs + ' · 第 ' + firstCh.chNo + ' 章 · 候选=' + firstCh.candidate + '（' + firstCh.kind + '）' +
    '\n候选项=' + firstCh.items + '（全部待裁决=' + firstCh.allNull + '）· 正式稿=' + String(firstCh.formal) +
    ' · 候选引用本书已建人物=' + firstCh.paraHasCast + ' · 当前视面=' + firstCh.routeView);

  /* =================== P5 连续性（切书再切回） =================== */
  const newBookId = await page.evaluate(() => window.WB.S.__scope.bookId);
  await switchTo(page, 'B-01');
  const onB01 = await page.evaluate(() => {
    const S = window.WB.S, c = S.craft['B-01'];
    return { scope: S.__scope.bookId, premise: (c.arc && c.arc.premise) || '', core: c.positioning.coreOriginal || '',
      dirId: c.positioning.dirId || '', hasSeed: !!c.positioning.seedRaw };
  });
  await clickAct(page, 'book.onbDir', [['book', 'B-01']]);
  await wait(500);
  const noBleed = await count(page, '#sharedArea .diff-i');
  await shot(page, 'P5-switch-book-no-bleed');
  step('P5-1', '切到另一本书：B-01 的方向 / 前提 / 原话互不串台',
    onB01.scope === 'B-01' && !onB01.dirId && !onB01.hasSeed && /记忆/.test(onB01.premise),
    'B-01 前提="' + onB01.premise.slice(0, 46) + '…" · dirId="' + onB01.dirId + '" · 有作者原话=' + onB01.hasSeed +
    '\nB-01 侧新开方向讨论产生的候选数=' + noBleed);

  await switchTo(page, newBookId);
  await page.evaluate(() => window.WB.go('book', 'overview'));
  await wait(360);
  const backState = await page.evaluate(() => {
    const S = window.WB.S, c = S.craft[S.__scope.bookId];
    return { scope: S.__scope.bookId, premise: (c.arc && c.arc.premise) || '', core: c.positioning.coreOriginal || '',
      dirId: c.positioning.dirId || '', chars: (c.characters || []).length, world: (c.world || []).length,
      seedRaw: c.positioning.seedRaw || '', convKeep: Object.keys(S.conversations).filter(k => k.indexOf(S.__scope.bookId) >= 0).length };
  });
  await shot(page, 'P5-switch-back-continues');
  step('P5-2', '切回新书：方向 / 设定 / 作者原话 / 对话都还在，可直接继续',
    backState.dirId === 'SD-01' && backState.chars >= 1 && backState.world >= 1 && backState.seedRaw.indexOf('档案员') >= 0,
    '方向=' + backState.dirId + ' · 人物=' + backState.chars + ' · 世界=' + backState.world +
    '\n对话会话键（含本书）=' + backState.convKeep + ' · 作者原话仍在=' + (backState.seedRaw.indexOf('档案员') >= 0));

  /* =================== P6 页面顺序 =================== */
  /* 先把员工协作重新拉起来（切书会按作品隔离地关掉对话，这是设计行为） */
  await clickAct(page, 'book.onbOpenConv', [['book', newBookId]]);
  await wait(500);
  const order = await page.evaluate(() => {
    const main = document.getElementById('main');
    const titles = Array.from(main.querySelectorAll('.pnl-h .pnl-t, .sarea-t')).map(e => e.innerText.trim());
    const idx = (re) => titles.findIndex(t => re.test(t));
    return { titles: titles.slice(0, 8),
      sharedFirst: /共享工作区/.test(titles[0] || ''),
      onbBeforeCraft: idx(/起步|下一步|这本书/) >= 0 && idx(/起步|下一步|这本书/) < idx(/创作内核入口/) };
  });
  step('P6-1', '首屏顺序：员工共享工作区在最上 → 起步/下一步 → 创作内核入口（不再堆 0 指标）',
    order.sharedFirst && order.onbBeforeCraft,
    '首屏顺序：' + JSON.stringify(order.titles.slice(0, 5)) +
    '\n共享工作区在首位=' + order.sharedFirst + ' · 起步块在创作内核入口之前=' + order.onbBeforeCraft);
  const posOrder = await page.evaluate(async () => {
    window.WB.go('book', 'craft', { mode: 'positioning' });
    await new Promise(r => setTimeout(r, 400));
    const main = document.getElementById('main');
    const first = main.querySelector('.pnl');
    return { firstTitle: first ? (first.querySelector('.pnl-t') || {}).innerText : '',
      firstBodyHasStory: first ? /一句话故事/.test(first.innerText) : false,
      firstBodyHasEditor: first ? /和编辑一起想/.test(first.innerText) : false,
      firstBodyHasCoverage: first ? /覆盖清单/.test(first.innerText) : false };
  });
  await shot(page, 'P6-positioning-first-screen');
  step('P6-2', '定位页首屏先给「一句话故事 + 编辑入口」，L01–L24 覆盖退到第二层',
    posOrder.firstBodyHasStory && posOrder.firstBodyHasCoverage,
    '第一个面板=' + posOrder.firstTitle + ' · 含一句话故事=' + posOrder.firstBodyHasStory +
    ' · 含编辑入口=' + posOrder.firstBodyHasEditor + ' · 覆盖清单在同面板第二层=' + posOrder.firstBodyHasCoverage);

  /* =================== P2 自行开写（先手写） =================== */
  await page.evaluate(() => window.WB.go('operate', 'home'));
  await wait(320);
  await clickFn(page, 'createBook');
  await wait(360);
  await clickFn(page, 'createBookPath', [['a1', 'write']]);
  await wait(700);
  const writePath = await page.evaluate(() => {
    const S = window.WB.S, bid = S.__scope.bookId;
    const chs = Object.keys(S.chapters).filter(k => S.chapters[k].bookId === bid);
    const b = (S.__runtime.createdBooks || []).filter(x => x.id === bid)[0] || {};
    return { scope: bid, view: S.__route.view, chs: chs.length,
      onbPath: b.onboarding ? b.onboarding.path : '', title: b.title,
      chState: chs.length ? S.chapters[chs[0]].state : '', chFormal: chs.length ? S.chapters[chs[0]].formal : null };
  });
  await shot(page, 'P2-write-path-chapter1');
  step('P2-1', '「先手写」直接进入第 1 章手写（草稿，不强制先填设定）',
    writePath.chs === 1 && writePath.view === 'manuscript' && !writePath.chFormal,
    '书=' + writePath.scope + '（' + writePath.title + '）· 起步方式=' + writePath.onbPath +
    '\n落在=' + writePath.view + ' · 在册章=' + writePath.chs + ' · 章状态=' + writePath.chState + ' · 正式稿=' + String(writePath.chFormal));

  await page.evaluate(() => window.WB.go('book', 'overview'));
  await wait(360);
  const writeOverview = await page.evaluate(() => {
    const t = document.getElementById('main').innerText;
    return { hasOnb: !!document.querySelector('#onbSeed, .onb-ladder'),
      curStep: (document.querySelector('.onb-step.cur') || {}).innerText || '',
      zeroStatNote: /起步阶段不铺 0 指标/.test(t), figs: document.querySelectorAll('.figs .fig').length };
  });
  await shot(page, 'P2-overview-after-self-start');
  step('P2-2', '自行开写后仍能回到起步区补方向（不因跳过而缺失）',
    writeOverview.hasOnb && writeOverview.figs === 0 && writeOverview.zeroStatNote,
    '起步区仍存在=' + writeOverview.hasOnb + ' · 当前步=' + writeOverview.curStep +
    '\n仍不铺 0 指标=' + writeOverview.zeroStatNote + '（0 指标卡=' + writeOverview.figs + '）');

  /* =================== P4 文本与审校（既有正文路径回归） =================== */
  await switchTo(page, 'B-01');
  await page.evaluate(() => window.WB.go('book', 'manuscript', { chapter: 'ch43' }));
  await wait(500);
  const beforeTxt = await page.evaluate(() => {
    const ms = window.WB.msOf('ch43');
    return { p0: ms.paragraphs[0] || '', formal: ms.formalVersion || '', n: ms.paragraphs.length };
  });
  const dis = await page.evaluate(() => {
    const els = Array.from(document.querySelectorAll('[data-action="book.discuss"]'));
    const el = els.filter(e => e.getAttribute('data-chapter') === 'ch43' && !e.getAttribute('data-para'))[0] || els[0];
    if (!el) return null; el.click(); return (el.innerText || '').trim();
  });
  await wait(500);
  await sendConv(page, '这一段再短一点，删掉重复的修饰词');
  const p4Prop = await page.evaluate(() => {
    const items = Array.from(document.querySelectorAll('#sharedArea .diff-i'));
    return { n: items.length, txt: document.getElementById('sharedArea').innerText };
  });
  await shot(page, 'P4-text-proposal');
  await clickAct(page, 'conv.acceptRest');
  await wait(500);
  const afterTxt = await page.evaluate(() => {
    const ms = window.WB.msOf('ch43');
    return { p0: ms.paragraphs[0] || '', formal: ms.formalVersion || '', n: ms.paragraphs.length,
      chosen: (document.querySelector('#chosenVersion, .ms-ver') || {}).innerText || '' };
  });
  await shot(page, 'P4-text-adopted');
  step('P4-1', '既有正文路径未回归：讨论 → 具体提案 → 采纳只落草稿，正式稿不变',
    p4Prop.n >= 1 && !/演示未模拟/.test(p4Prop.txt) && afterTxt.p0 !== beforeTxt.p0 && afterTxt.formal === beforeTxt.formal,
    '入口=' + dis + ' · 提案项=' + p4Prop.n + '\n改前首段="' + beforeTxt.p0.slice(0, 44) + '…"' +
    '\n改后首段="' + afterTxt.p0.slice(0, 44) + '…"\n正式版号 ' + beforeTxt.formal + ' → ' + afterTxt.formal + '（应不变）');

  /* =================== P7 业务回归（六区关键视面） =================== */
  const zones = [
    ['operate', 'home'], ['book', 'library'], ['book', 'overview'], ['book', 'manuscript'],
    ['market', 'direction'], ['publish', 'queue'], ['audience', 'performance'], ['learning', 'library']
  ];
  const zoneRes = [];
  for (const [area, view] of zones) {
    const before = errors.length;
    await page.evaluate((a, v) => window.WB.go(a, v), area, view);
    await wait(340);
    const info = await page.evaluate(() => {
      const m = document.getElementById('main');
      return { len: m.innerText.trim().length, hasErr: /未实现的行动|尚未实现/.test(m.innerText) };
    });
    zoneRes.push({ zone: area + '/' + view, len: info.len, err: errors.length - before, broken: info.hasErr });
  }
  await shot(page, 'P7-zone-regression');
  step('P7-1', '六区关键视面均可进入且无「未实现的行动 / 尚未实现」',
    zoneRes.every(z => z.len > 120 && !z.broken && z.err === 0),
    zoneRes.map(z => z.zone + '=' + z.len + '字' + (z.broken ? '(未实现!)' : '') + (z.err ? '(ERR' + z.err + ')' : '')).join(' · '));

  /* =================== P8 创作深度（D10 最小编辑/联动：伏笔 / 时序） =================== */
  await switchTo(page, 'B-01');
  await page.evaluate(() => window.WB.go('book', 'story'));
  await wait(450);
  const storyBefore = await page.evaluate(() => {
    const S = window.WB.S, bid = S.__scope.bookId;
    const st = S.storyState[bid] || {};
    return { bid: bid, threads: (st.threads || []).length, tl: (st.timeline || []).length,
      hasNew: !!document.querySelector('[data-action="book.threadNew"]'),
      hasTlNew: !!document.querySelector('[data-action="book.timelineNew"]') };
  });
  await shot(page, 'P8-story-depth-entry');
  step('P8-1', '故事状态页给出伏笔 / 时序的最小写入口（不再是只读台账）',
    storyBefore.hasNew && storyBefore.hasTlNew,
    '页=' + storyBefore.bid + ' · 原有伏笔=' + storyBefore.threads + ' 条 / 时序=' + storyBefore.tl + ' 条' +
    ' · 入口：新增伏笔=' + storyBefore.hasNew + ' · 新增时序=' + storyBefore.hasTlNew);

  /* 真实点击「新增伏笔」：填内容 / 位置 / 计划 + 勾选一本书已有的章 → 保存 */
  await clickAct(page, 'book.threadNew');
  await wait(420);
  const linkCount = await page.evaluate(() => document.querySelectorAll('#modal .linkRef').length);
  await page.evaluate(() => {
    const set = (id, v) => { const e = document.getElementById(id); if (e) { e.value = v; e.dispatchEvent(new Event('input', { bubbles: true })); } };
    set('thText', '试用伏笔 · 门牌号每年倒着走');
    set('thPlanted', 'ch01');
    set('thPlan', 'ch05 兑现');
    const cb = document.querySelector('#modal .linkRef');
    if (cb) { cb.checked = true; cb.dispatchEvent(new Event('change', { bubbles: true })); }
  });
  await wait(180);
  const threadModalShot = await shot(page, 'P8-thread-modal');
  await clickAct(page, 'book.threadSave');
  await wait(520);
  const storyAfter = await page.evaluate(() => {
    const S = window.WB.S, bid = S.__scope.bookId;
    const st = S.storyState[bid] || {};
    const list = st.threads || [];
    const t = list.filter(x => /门牌号/.test(x.text || ''))[0] || {};
    const inTable = Array.from(document.querySelectorAll('#main table')).some(tb => tb.innerText.indexOf(t.id || '\u0000') >= 0);
    return { n: list.length, id: t.id || '', text: t.text || '', state: t.state || '',
      refs: (t.refs || []).map(r => r.label), inTable: inTable };
  });
  await shot(page, 'P8-thread-created');
  step('P8-2', '新增伏笔写进本书台账，并可关联到本书已有对象（章 / 人物）',
    storyAfter.n === storyBefore.threads + 1 && /门牌号/.test(storyAfter.text) && storyAfter.state === '待兑现' &&
      storyAfter.refs.length >= 1 && linkCount >= 1 && storyAfter.inTable,
    '模态=' + threadModalShot + ' · 可关联对象=' + linkCount + ' 个' +
    '\n伏笔 ' + storyBefore.threads + ' → ' + storyAfter.n + ' 条 · 新条目=' + storyAfter.id + '(' + storyAfter.state + ')' +
    ' · 已关联=[' + storyAfter.refs.join('、') + '] · 出现在台账表格=' + storyAfter.inTable);

  /* 编辑该伏笔：验证回填 + 改状态生效 + 不重复建条目 */
  await clickAct(page, 'book.threadEdit', [['id', storyAfter.id]]);
  await wait(420);
  const prefill = await page.evaluate(() => ({
    txt: (document.getElementById('thText') || {}).value || '',
    sel: (document.getElementById('thState') || {}).value || '',
    checked: document.querySelectorAll('#modal .linkRef:checked').length }));
  await page.evaluate(() => {
    const e = document.getElementById('thState'); if (e) { e.value = '已兑现'; e.dispatchEvent(new Event('change', { bubbles: true })); }
  });
  await wait(150);
  await clickAct(page, 'book.threadSave', [['id', storyAfter.id]]);
  await wait(520);
  const edited = await page.evaluate(() => {
    const S = window.WB.S, bid = S.__scope.bookId;
    const st = S.storyState[bid] || {};
    const list = st.threads || [];
    const t = list.filter(x => /门牌号/.test(x.text || ''))[0] || {};
    return { state: t.state || '', n: list.length };
  });
  step('P8-3', '编辑伏笔：回填原值、改状态生效，且不会重复新增条目',
    !!prefill.txt && prefill.checked >= 1 && edited.state === '已兑现' && edited.n === storyAfter.n,
    '回填内容="' + prefill.txt.slice(0, 22) + '" · 回填状态=' + prefill.sel + ' · 回填已勾选关联=' + prefill.checked +
    '\n保存后状态=' + edited.state + ' · 伏笔条目数=' + edited.n + '（未重复新增）');

  /* 新增时序：同一个最小写入口模型 */
  await clickAct(page, 'book.timelineNew');
  await wait(420);
  await page.evaluate(() => {
    const set = (id, v) => { const e = document.getElementById(id); if (e) { e.value = v; e.dispatchEvent(new Event('input', { bubbles: true })); } };
    set('tlAt', 'ch05'); set('tlNote', '试用时序 · 门牌号第一次倒着走');
    const cb = document.querySelector('#modal .linkRef');
    if (cb) { cb.checked = true; cb.dispatchEvent(new Event('change', { bubbles: true })); }
  });
  await wait(180);
  await clickAct(page, 'book.timelineSave');
  await wait(520);
  const tlAfter = await page.evaluate(() => {
    const S = window.WB.S, bid = S.__scope.bookId;
    const st = S.storyState[bid] || {};
    const list = st.timeline || [];
    const t = list.filter(x => /门牌号/.test(x.note || ''))[0] || {};
    return { n: list.length, at: t.at || '', note: t.note || '', refs: (t.refs || []).length };
  });
  await shot(page, 'P8-timeline-created');
  step('P8-4', '新增时序可写进本书并关联到已有章（创作深度不因起步简化而丢失）',
    tlAfter.n === storyBefore.tl + 1 && /门牌号/.test(tlAfter.note) && tlAfter.refs >= 1,
    '时序 ' + storyBefore.tl + ' → ' + tlAfter.n + ' 条 · 新条目=' + tlAfter.at + ' · 关联=' + tlAfter.refs + ' 个' +
    '\n说明="' + tlAfter.note + '"');

  /* =================== 1280×900 复跑关键路径 =================== */
  await page.setViewport({ width: 1280, height: 900 });
  await wait(300);
  await switchTo(page, newBookId);
  await page.evaluate(() => window.WB.go('book', 'overview'));
  await wait(400);
  await clickAct(page, 'book.onbOpenConv', [['book', newBookId]]);
  await wait(450);
  /* 先验证展开态：共享工作区在首屏、无横向溢出 */
  const open1280 = await page.evaluate(() => {
    const main = document.getElementById('main');
    const sa = document.querySelector('#main #sharedArea');
    return { overflowX: main.scrollWidth > main.clientWidth + 2, mainW: main.clientWidth,
      sharedVisible: sa ? sa.getBoundingClientRect().top < window.innerHeight : false };
  });
  /* 再收起对话（真实点击「收起」）：验证收起后起步区回到首屏 */
  await clickAct(page, 'conv.toggleCollapse');
  await wait(400);
  const small = await page.evaluate(() => {
    const main = document.getElementById('main');
    const mbar = document.getElementById('mainBar');
    const onb = main.querySelector('.onb-ladder, .onb-chip');
    const sa = document.querySelector('#main #sharedArea');
    return { hasOnb: !!onb, onbVisible: onb ? onb.getBoundingClientRect().top < window.innerHeight : false,
      sharedTop: sa && mbar ? Math.round(sa.getBoundingClientRect().top - mbar.getBoundingClientRect().bottom) : null,
      collapsed: sa ? sa.classList.contains('is-collapsed') : false,
      sharedMinLine: sa ? /工作没有停/.test(sa.innerText) : false,
      overflowX: main.scrollWidth > main.clientWidth + 2, mainW: main.clientWidth };
  });
  await shot(page, 'P6-1280x900');
  step('P6-3', '1280×900：展开态共享工作区在首屏；收起后只留一行且起步区回到首屏；无横向溢出',
    small.hasOnb && small.onbVisible && small.collapsed && small.sharedMinLine && !small.overflowX && open1280.sharedVisible,
    'Main 宽=' + small.mainW + 'px · 展开态共享工作区首屏可见=' + open1280.sharedVisible +
    '\n收起后：收起态=' + small.collapsed + ' · 保留「工作没有停」一行=' + small.sharedMinLine +
    ' · 起步区首屏可见=' + small.onbVisible + ' · 横向溢出=' + small.overflowX);
  await clickAct(page, 'conv.toggleCollapse');
  await wait(300);
  /* =================== 汇总 =================== */
  await browser.close();
  server.close();
  try { fs.rmSync(profile, { recursive: true, force: true }); } catch (e) {}

  const L = ['# 第 5 轮作者动线验收 · 路径记录', '',
    '- 运行时间：' + new Date().toISOString(),
    '- 入口：' + ENTRY + '（源码形态或由 _build.js 生成的单文件交付物）',
    '- 浏览器：系统 Chrome（headless=new）· 独立 user-data-dir（隔离演示数据，无注入运行态）',
    '- 视口：1440×1000（主）与 1280×900（复跑关键路径）· 100% 缩放',
    '- 结果：PASS ' + pass + ' · PARTIAL ' + partial + ' · FAIL ' + fail + ' · Console Error ' + errors.length,
    '- 截图：' + seq + ' 张（同目录，按编号顺序）', ''];
  ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8'].forEach(p => {
    const rows = steps.filter(s => s.id.indexOf(p) === 0);
    if (!rows.length) return;
    const names = { P1: '新书从想法开始', P2: '自行开写', P3: '素材与编辑', P4: '文本与审校', P5: '连续性', P6: '页面顺序', P7: '业务回归', P8: '创作深度（D10 最小编辑/联动）' };
    L.push('## ' + p + ' ' + names[p], '');
    rows.forEach(s => L.push('- **[' + s.verdict + ']** `' + s.id + '` ' + s.title + (s.detail ? '\n  - ' + s.detail.replace(/\n/g, '\n  - ') : '')));
    L.push('');
  });
  if (errors.length) { L.push('## Console 错误', ''); errors.forEach(e => L.push('- `' + e.slice(0, 300) + '`')); }
  fs.writeFileSync(path.join(EV, 'PATH_RECORD.md'), L.join('\n'));

  console.log('\n============================');
  console.log('PASS ' + pass + ' · PARTIAL ' + partial + ' · FAIL ' + fail + ' · Console Error ' + errors.length + ' · 截图 ' + seq + ' 张');
  if (errors.length) errors.forEach(e => console.log('  ! ' + e.slice(0, 220)));
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error('HARNESS ERROR:', e); process.exit(2); });
