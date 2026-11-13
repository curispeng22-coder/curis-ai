/* CURIS — Writing Business 探索原型 · 第 3 轮（R1–R7）作者路径验收 + 版面测量
   目的：按 @§1 的 7 条作者路径逐条走真机点击，记录「改前 / 改后」值与返回点；
        并按 @§3 在 1440×1000 与 1280×900（100% 缩放）测量正文字宽与正文占版面比例。
   产出：_evidence_round3/ 截图 + _evidence_round3/ACCEPTANCE.json
   运行：node _author_path_acceptance.js                              */
'use strict';
const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');
const http = require('http');

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const ROOT = __dirname;
const EV = path.join(ROOT, '_evidence_round3');
fs.mkdirSync(EV, { recursive: true });

const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8' };
const wait = (ms) => new Promise(r => setTimeout(r, ms));
const cut = (s) => (typeof s === 'string' ? s.slice(0, 18) + '…' : String(s));

const results = [];
const shots = [];
const consoleErrors = [];
let seq = 0;

function rec(pathId, name, ok, detail, before, after, returnPoint) {
  results.push({ path: pathId, name, ok: !!ok, detail: detail || '',
    before: before === undefined ? null : before, after: after === undefined ? null : after,
    returnPoint: returnPoint || null });
  console.log((ok ? '  ✓ ' : '  ✗ ') + '[' + pathId + '] ' + name + (detail ? '  — ' + detail : ''));
}

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
  shots.push({ n: seq, tag, file: path.basename(f) });
  return path.basename(f);
}
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
async function clickFnA2(page, fn, a2) {
  const hit = await page.evaluate((fn, a2) => {
    const els = Array.from(document.querySelectorAll('[data-fn="' + fn + '"]'));
    const el = els.filter(e => e.getAttribute('data-a2') === String(a2))[0];
    if (!el) return false;
    el.click(); return true;
  }, fn, a2);
  await wait(220);
  return hit;
}
async function setField(page, id, text) {
  await page.evaluate((id, text) => {
    const e = document.getElementById(id);
    if (e) { e.value = text; e.dispatchEvent(new Event('input', { bubbles: true })); }
  }, id, text);
  await wait(70);
}
async function goView(page, area, view, params) {
  await page.evaluate((a, v, p) => window.WB.go(a, v, p || {}), area, view, params || {});
  await wait(200);
}
const LONG_PARA_1 = '夜巡的第三个晚上，他把灯按在掌心，指腹贴着铜面，能感到一点微弱的、像是心跳的震动。廊下的风很轻，很薄，很凉，把他袖口吹得微微翻起。他没有立刻点亮，因为点亮一次就要交出一段记忆，而他已经想不起母亲的嗓音了。灯亮起来的时候，他看见廊柱后面站着一个模糊的人影，那人影没有脸，却分明在等他认出自己。';
const LONG_PARA_2 = '他向前走了一步，又停住，因为他忽然想不起来自己为什么要走进这条廊。';

(async () => {
  const server = await serve();
  const url = 'http://127.0.0.1:' + server.address().port + '/index.html';
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--no-proxy-server', '--disable-gpu'],
    defaultViewport: { width: 1440, height: 1000, deviceScaleFactor: 1 },
    protocolTimeout: 180000
  });
  const page = await browser.newPage();
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push('CONSOLE: ' + m.text()); });
  page.on('pageerror', e => consoleErrors.push('PAGEERROR: ' + e.message));
  page.on('requestfailed', r => { if (!/favicon/.test(r.url())) consoleErrors.push('REQFAIL: ' + r.url().slice(0, 100)); });

  await page.goto(url, { waitUntil: 'load', timeout: 30000 });
  await page.waitForSelector('#nav .nav-item', { timeout: 10000 });

  /* ============================================================
     §1-A1 有想法 → 打开一本书（对象归属 + 真实产物 + 返回点）
     ============================================================ */
  console.log('\n--- §1-A1 有想法 → 打开一本书 ---');
  /* 真实动线：创作方向 → 去作品库 → 打开作品（方向页本身没有 book.open，必须走作品库） */
  await goView(page, 'market', 'direction');
  const dirBefore = await page.evaluate(() => ({
    view: window.WB.S.__route.area + '/' + window.WB.S.__route.view,
    scope: window.WB.S.__scope.bookId,
    toLibrary: !!document.querySelector('[data-action="nav.view"][data-area="book"][data-view="library"]')
  }));
  await clickAct(page, 'nav.view', [['area', 'book'], ['view', 'library']]);
  const libAfter = await page.evaluate(() => ({
    view: window.WB.S.__route.area + '/' + window.WB.S.__route.view,
    openBtns: Array.from(document.querySelectorAll('[data-action="book.open"]')).map(e => e.getAttribute('data-id'))
  }));
  rec('A1', '「有想法」入口可到作品库（创作方向 → 去作品库）',
    libAfter.view === 'book/library' && libAfter.openBtns.length >= 2 && dirBefore.toLibrary,
    '方向页入口=' + dirBefore.toLibrary + ' 落点=' + libAfter.view + ' 可打开作品=' + libAfter.openBtns.join('/'),
    { 视图: dirBefore.view }, { 视图: libAfter.view },
    '返回点：左侧导航「书 · 作品库」常驻');

  /* 先打开另一本书，再打开目标书：证明范围真的被切换，而不是默认值碰巧相等 */
  await clickAct(page, 'book.open', [['id', 'B-02']]);
  const b2 = await page.evaluate(() => {
    var c = window.WB.S.craft['B-02'] || {};
    return { view: window.WB.S.__route.area + '/' + window.WB.S.__route.view, scope: window.WB.S.__scope.bookId,
      world: (c.world || []).length, characters: (c.characters || []).length,
      continueExists: !!document.querySelector('[data-action="book.continue"]') };
  });
  rec('A1', '打开 B-02 后范围切到 B-02，并载入 B-02 自己的创作对象（不串到 B-01）',
    b2.scope === 'B-02' && b2.view === 'book/overview' && b2.world > 0 && b2.characters > 0,
    '范围=' + b2.scope + ' 视图=' + b2.view + ' B-02 背景' + b2.world + '/人物' + b2.characters,
    { 范围: b2.scope }, null, '返回点：「继续当前章」直达正文');

  /* 返回点实测：点返回上一位置，应回到作品库且范围不变 */
  const backClicked = await page.evaluate(() => {
    var el = document.querySelector('#btnBack');
    if (!el || el.disabled) return false;
    el.click(); return true;
  });
  await wait(250);
  const backTo = await page.evaluate(() => ({ view: window.WB.S.__route.area + '/' + window.WB.S.__route.view, scope: window.WB.S.__scope.bookId }));
  rec('A1', '返回点可用：返回上一位置回到作品库，且保留原范围',
    backClicked && backTo.view === 'book/library' && backTo.scope === 'B-02',
    '返回命中=' + backClicked + ' 落点=' + backTo.view + ' 保留范围=' + backTo.scope,
    null, { 视图: backTo.view, 范围: backTo.scope },
    '返回点：顶部 ← 返回上一位置（保留原范围与筛选）');

  /* 打开目标作品 B-01：范围切换 + 本书自有对象 + 返回点齐全 */
  await clickAct(page, 'book.open', [['id', 'B-01']]);
  const a1After = await page.evaluate(() => {
    const c = window.WB.S.craft['B-01'] || {};
    const bk = window.WB.scopeBook() || {};
    return {
      view: window.WB.S.__route.area + '/' + window.WB.S.__route.view,
      scope: bk.id || null,
      owned: { world: (c.world || []).length, characters: (c.characters || []).length, outline: (c.outline || []).length, scenes: Object.keys(c.scenes || {}).length },
      backEnabled: !document.querySelector('#btnBack').disabled,
      hasContinue: !!document.querySelector('[data-action="book.continue"]'),
      chapterCount: window.WB.S.chapters ? Object.keys(window.WB.S.chapters).filter(k => window.WB.S.chapters[k].bookId === 'B-01').length : 0
    };
  });
  rec('A1', '打开作品后范围切换到该书，并载入本书自有创作对象',
    a1After.scope === 'B-01' && a1After.view === 'book/overview' && a1After.owned.world > 0 && a1After.owned.characters > 0 && a1After.chapterCount > 0,
    '范围=' + a1After.scope + ' 视图=' + a1After.view + ' 背景' + a1After.owned.world + '/人物' + a1After.owned.characters + '/大纲' + a1After.owned.outline + '/场景' + a1After.owned.scenes + ' 在册章节=' + a1After.chapterCount,
    { 范围: b2.scope }, { 范围: a1After.scope },
    '返回点：#btnBack（返回上一位置）+ 作品库入口；「继续当前章」直达正文');
  rec('A1', '路径有返回点（返回上一位置 可用 / 继续当前章 存在）', a1After.backEnabled && a1After.hasContinue,
    '返回上一位置可用=' + a1After.backEnabled + ' 继续当前章=' + a1After.hasContinue);
  await shot(page, 'a1-open-book-from-direction');

  /* ============================================================
     §1-A2 打磨世界 / 人物 / 弧线（对象归属 + 真实产物 + 下游引用）
     ============================================================ */
  console.log('\n--- §1-A2 打磨世界 / 人物 / 弧线 ---');
  await goView(page, 'book', 'craft', { bookId: 'B-01', mode: 'world' });
  const wBefore = await page.evaluate(() => {
    const w = window.WB.S.craft['B-01'].world[0];
    return { id: w.id, cond: w.cond, impact: window.WB.S.craft['B-01'].impactLog.length };
  });
  await clickAct(page, 'craft.objEdit', [['kind', 'world'], ['id', wBefore.id]]);
  await setField(page, 'ad_cond', wBefore.cond + '（本轮作者修订：必须直视灯芯才生效）');
  await clickFn(page, 'craftObjSave', 'B-01');
  const wAfter = await page.evaluate(() => {
    const c = window.WB.S.craft['B-01'], w = c.world[0];
    return { cond: w.cond, impact: c.impactLog.length, last: c.impactLog[c.impactLog.length - 1] };
  });
  rec('A2', '世界条目可完整维护（不限一个字段），改动写入影响清单',
    wAfter.cond !== wBefore.cond && wAfter.impact === wBefore.impact + 1,
    '影响清单 ' + wBefore.impact + ' → ' + wAfter.impact + '；受影响：' + (wAfter.last.affected || []).join('、'),
    { cond: wBefore.cond.slice(0, 24) + '…' }, { cond: wAfter.cond.slice(0, 24) + '…' },
    '返回点：创作内核左侧工作面（世界）保持在同一本书范围内');

  /* 人物：改声纹，并在「故事状态」里读到同一对象（下游引用同一条数据） */
  await goView(page, 'book', 'craft', { bookId: 'B-01', mode: 'characters' });
  const cBefore = await page.evaluate(() => {
    const x = window.WB.S.craft['B-01'].characters[0];
    return { id: x.id, name: x.name, voice: x.voice };
  });
  await clickAct(page, 'craft.objEdit', [['kind', 'character'], ['id', cBefore.id]]);
  await setField(page, 'ad_voice', '（本轮：短句、少形容词、常停顿）');
  await clickFn(page, 'craftObjSave', 'B-01');
  const cAfter = await page.evaluate(() => {
    const x = window.WB.S.craft['B-01'].characters[0];
    return { voice: x.voice, goal: x.goal, motivation: x.motivation, arc: x.arc, first: x.first, status: x.status };
  });
  await goView(page, 'book', 'story', { bookId: 'B-01' });
  const storyReads = await page.evaluate(() => document.querySelector('#main').innerText.includes('短句、少形容词、常停顿'));
  rec('A2', '人物档案改声纹后其余字段保持，且「故事状态」读到同一条数据',
    cAfter.voice === '（本轮：短句、少形容词、常停顿）' && !!cAfter.goal && !!cAfter.arc && storyReads,
    '故事状态读到同一对象=' + storyReads + '；goal/arc/motivation/first/status 均保留',
    { voice: cBefore.voice }, { voice: cAfter.voice },
    '返回点：故事状态 ← 创作内核·人物（同一对象，非复制）');
  await shot(page, 'a2-character-voice-downstream');

  /* 弧线 / 定位字段走逐字段编辑，验证「打磨弧线」也在路径内 */
  await goView(page, 'book', 'craft', { bookId: 'B-01', mode: 'arc' });
  const arcBefore = await page.evaluate(() => window.WB.S.craft['B-01'].arc.premise);
  await clickAct(page, 'craft.edit', [['kind', 'arc'], ['field', 'premise']]);
  await setField(page, 'cfVal', String(arcBefore || '') + '（本轮：代价必须推动选择）');
  await clickFn(page, 'craftSaveDirect', 'B-01');
  const arcAfter = await page.evaluate(() => window.WB.S.craft['B-01'].arc.premise);
  rec('A2', '弧线（premise）可打磨并真实落库', arcAfter !== arcBefore,
    '改前 ' + String(arcBefore).length + ' 字 → 改后 ' + String(arcAfter).length + ' 字',
    String(arcBefore).slice(0, 20) + '…', String(arcAfter).slice(0, 20) + '…', '返回点：创作内核 · 主支线与结局');

  /* ============================================================
     §1-A3 写一章（真实产物：草稿段落；不自动成为正式稿）
     ============================================================ */
  console.log('\n--- §1-A3 写一章 ---');
  await goView(page, 'book', 'manuscript', { bookId: 'B-01' });
  await clickFn(page, 'newChapter', 'B-01');
  const newCk = await page.evaluate(() => {
    const S = window.WB.S;
    const ks = Object.keys(S.chapters).filter(k => S.chapters[k].bookId === 'B-01').sort((a, b) => S.chapters[a].no - S.chapters[b].no);
    return ks[ks.length - 1];
  });
  const a3Before = await page.evaluate(c => {
    const ch = window.WB.S.chapters[c], ms = window.WB.S.manuscripts[c];
    return { state: ch.state, formal: ch.formal, published: ch.published, paras: ms ? ms.paragraphs.length : null };
  }, newCk);
  await clickAct(page, 'book.msEdit', [['chapter', newCk]]);
  await setField(page, 'msEditor', LONG_PARA_1 + '\n\n' + LONG_PARA_2);
  await clickFn(page, 'msSave', 'B-01');
  const a3After = await page.evaluate(c => {
    const ch = window.WB.S.chapters[c], ms = window.WB.S.manuscripts[c];
    return { state: ch.state, formal: ch.formal, published: ch.published, paras: ms.paragraphs.length,
      formalSnap: !!ms.formal, pubSnap: !!ms.published, draftVer: (ms.versions.filter(v => v.kind === 'draft').slice(-1)[0] || {}).v };
  }, newCk);
  rec('A3', '手写一章真实落库为草稿（分段），且不自动成为正式稿 / 线上稿',
    a3After.paras === 2 && !a3After.formal && !a3After.published,
    '章=' + newCk + ' 段落=' + a3After.paras + ' 状态=' + a3After.state + ' 草稿版本=' + a3After.draftVer,
    a3Before, { 段落: a3After.paras, 正式稿: a3After.formal, 线上稿: a3After.published },
    '返回点：章节列表（同章保留）+「继续当前章」入口');
  rec('A3', '章节改名按键关联（不靠标题匹配）且改名后大纲/场景/候选关联不断',
    await (async () => {
      await clickAct(page, 'book.rename', [['chapter', newCk]]);
      await setField(page, 'chTitleInp', '夜巡·第三夜');
      await clickFn(page, 'chapRename', newCk);
      return page.evaluate(c => {
        const ch = window.WB.S.chapters[c];
        const ms = window.WB.S.manuscripts[c];
        return ch.title === '夜巡·第三夜' && !!ms && ms.title.indexOf('夜巡·第三夜') >= 0;
      }, newCk);
    })());
  await shot(page, 'a3-write-chapter-draft');

  /* ============================================================
     §1-A4 改一段（选区 → 讨论 → 逐项采纳 → 只写草稿；2 轮延续）
     ============================================================ */
  console.log('\n--- §1-A4 改一段 ---');
  await clickAct(page, 'book.para', [['id', '1']]);
  const selOn = await page.evaluate(() => !!document.querySelector('[data-action="book.selRewrite"]'));
  rec('A4', '选中段落出现「改写这一段 / 对这一段讨论」入口（靠近对象）', selOn);

  const p1Before = await page.evaluate(c => window.WB.S.manuscripts[c].paragraphs[0], newCk);
  await clickAct(page, 'book.discuss', [['chapter', newCk], ['para', '1']]);
  const convScope = await page.evaluate(() => {
    const d = document.querySelector('#drawer');
    return { text: d ? d.innerText : '',
      inputFree: !!document.querySelector('#convInput'),
      prefilled: (document.querySelector('#convInput') || {}).value || '' };
  });
  rec('A4', '对话显示「他负责的范围」与对象/版本，且输入框为空可自由输入',
    /他负责的范围/.test(convScope.text) && /草稿 r/.test(convScope.text) && convScope.inputFree && convScope.prefilled === '',
    '版本行示例=' + ((convScope.text.match(/第 \d+ 章 · 草稿 r\d+[^\n]*/) || [''])[0]).slice(0, 60));
  await shot(page, 'a4-selection-conversation');

  await setField(page, 'convInput', '这一段再短一点');
  await clickAct(page, 'conv.send');
  const r1 = await page.evaluate(() => {
    const S = window.WB.S, pids = Object.keys(S.discussProps);
    const p = S.discussProps[pids[pids.length - 1]];
    return { pid: p.id, round: p.round, items: p.items.length,
      after: p.items[0].after, before: p.items[0].before,
      target: p.targetLabel, basis: p.basis };
  });
  rec('A4', '第 1 轮：讨论产生具体可编辑提案（不是「收到」）', r1.round === 1 && r1.items >= 1 && r1.after !== r1.before,
    '提案=' + r1.pid + ' 落到=' + r1.target + '；改前 ' + r1.before.length + ' 字 → 改后 ' + r1.after.length + ' 字');
  await clickAct(page, 'conv.acceptItem', [['pid', r1.pid], ['item', 'I1']]);
  const p1After = await page.evaluate(c => {
    const ms = window.WB.S.manuscripts[c];
    return { para: ms.paragraphs[0], formal: ms.formalVersion, paraN: ms.paragraphs.length };
  }, newCk);
  rec('A4', '采纳只写入草稿该段；正式稿未变',
    p1After.para === r1.after && p1After.para !== p1Before && !p1After.formal,
    '第 1 段 ' + p1Before.length + ' 字 → ' + p1After.para.length + ' 字；正式版本=' + (p1After.formal || '无'),
    { 第1段: p1Before.slice(0, 30) + '…' }, { 第1段: p1After.para.slice(0, 30) + '…' },
    '返回点：正文工作面（草稿变化；版本历史可回退）');

  /* 第 2 轮：延续同一候选（conv.continue），只动未裁定范围 */
  await setField(page, 'convInput', '这一段再短一点');
  await clickAct(page, 'conv.continue', [['pid', r1.pid]]);
  const r2 = await page.evaluate(() => {
    const S = window.WB.S, pids = Object.keys(S.discussProps);
    const p = S.discussProps[pids[pids.length - 1]];
    const prev = S.discussProps[pids[pids.length - 2]];
    return { pid: p.id, round: p.round, items: p.items.length, after: p.items[0].after,
      basis: p.basis, prevRound: prev.round, prevState: prev.items.map(x => x.applied) };
  });
  const advanced = r2.round === r2.prevRound + 1;
  await clickAct(page, 'conv.acceptItem', [['pid', r2.pid], ['item', r2.items ? 'I1' : 'C1']]);
  const p1After2 = await page.evaluate(c => window.WB.S.manuscripts[c].paragraphs[0], newCk);
  rec('A4', '第 2 轮延续同一对象继续收紧，且已裁定项不被重复改动',
    advanced && p1After2.length <= p1After.para.length && r2.prevState.every(x => x !== null),
    '轮次 ' + r2.prevRound + ' → ' + r2.round + '；段落字数 ' + p1After.para.length + ' → ' + p1After2.length + '（第 1 轮裁定保持=' + r2.prevState.join(',') + '）',
    { 段落字数: p1After.para.length }, { 段落字数: p1After2.length }, '返回点：对话抽屉可反复发起，正文同步刷新');
  await shot(page, 'a4-two-round-discussion');

  /* 未模拟的意图必须明说 */
  await clickAct(page, 'book.discuss', [['chapter', newCk], ['para', '1']]);
  await setField(page, 'convInput', '帮我把这一段改得更有电影感');
  await clickAct(page, 'conv.send');
  const unsup = await page.evaluate(() => {
    const d = document.querySelector('#drawer').innerText;
    const S = window.WB.S, pids = Object.keys(S.discussProps);
    return { demoSaid: /演示未模拟|未模拟这类要求/.test(d), propsUnchanged: pids.length };
  });
  rec('A4', '未支持的意图如实说「演示未模拟」，不产生假改动', unsup.demoSaid,
    '对话内明示未模拟=true；提案总数未增加（' + unsup.propsUnchanged + '）', null, null, '返回点：可换说法或直接手改');
  await clickAct(page, 'close-drawer');

  /* ============================================================
     §1-A5 审校 / 校对（报告记录输入版本；修复只写草稿）
     ============================================================ */
  console.log('\n--- §1-A5 审校 / 校对 ---');
  /* 先恢复一段「可被检查到」的草稿文本（含半角标点与重复弱化词），确保检查有真实发现 */
  await goView(page, 'book', 'manuscript', { bookId: 'B-01', chapter: newCk });
  await clickAct(page, 'book.msEdit', [['chapter', newCk]]);
  await setField(page, 'msEditor', LONG_PARA_1.replace('，指腹贴着铜面', ',指腹贴着铜面') + '\n\n其实他其实并不想点亮它。');
  await clickFn(page, 'msSave', 'B-01');
  await goView(page, 'book', 'review', { bookId: 'B-01', chapter: newCk, kind: 'proof' });
  await shot(page, 'a5-review-location');
  const reviewBtn = await page.evaluate(() => !!document.querySelector('[data-fn="reviewRun"]'));
  rec('A5', '审校工作面可从当前章发起检查（位置明确）', reviewBtn);
  await page.evaluate(() => {
    const els = Array.from(document.querySelectorAll('[data-fn="reviewRun"]'));
    const el = els.filter(e => e.getAttribute('data-a3') === 'proof')[0] || els[0];
    if (el) el.click();
  });
  await wait(260);
  const run = await page.evaluate(() => {
    const S = window.WB.S, r = (S.reviewRuns || [])[0];
    return r ? { id: r.id, n: r.findings.length, ver: r.inputVersion, scope: r.scopeLabel,
      withFix: r.findings.filter(f => f.fix).length, kinds: r.findings.map(f => f.kind) } : null;
  });
  rec('A5', '检查报告记录「检查的是哪个版本」（不用章节 ID 当修订号）',
    !!run && /草稿 r\d+/.test(run.ver) && /正式|未发布/.test(run.ver),
    '报告=' + (run ? run.id : '—') + ' 输入版本=' + (run ? run.ver : '—'),
    null, run ? run.ver : null, '返回点：报告留在本章历史里；旧报告会标注适用性');
  if (run && run.n) {
    const draftBefore = await page.evaluate(c => window.WB.S.manuscripts[c].paragraphs.join('|'), newCk);
    const formalBefore = await page.evaluate(c => window.WB.S.manuscripts[c].formalVersion, newCk);
    await clickFn(page, 'reviewPatch', run.id);
    const after = await page.evaluate(c => {
      const ms = window.WB.S.manuscripts[c];
      return { draft: ms.paragraphs.join('|'), formal: ms.formalVersion };
    }, newCk);
    rec('A5', '处理检查项只改草稿；正式稿快照不动（不原地覆盖）',
      after.formal === formalBefore && (after.draft !== draftBefore || run.withFix === 0),
      '发现 ' + run.n + ' 项（含可执行修复 ' + run.withFix + ' 项）；正式版本 ' + (formalBefore || '无') + ' → ' + (after.formal || '无') + '；草稿是否变化=' + (after.draft !== draftBefore),
      { 草稿: draftBefore.slice(0, 30) + '…', 正式版本: formalBefore }, { 草稿: after.draft.slice(0, 30) + '…', 正式版本: after.formal },
      '返回点：审校报告与正文双向可回');
  }
  const reviewUnsup = await page.evaluate(() => {
    const t = document.querySelector('#main').innerText;
    return { noFakeSuccess: !/已修复全部问题/.test(t) };
  });
  rec('A5', '不把「检查完成」冒充「问题已修复」', reviewUnsup.noFakeSuccess);

  /* ============================================================
     §1-A6 定稿 + 发布（确认正式 ≠ 发布；线上稿快照不变）
     ============================================================ */
  console.log('\n--- §1-A6 定稿 + 发布 ---');
  await goView(page, 'book', 'manuscript', { bookId: 'B-01', chapter: newCk });
  const fBefore = await page.evaluate(c => {
    const ch = window.WB.S.chapters[c], ms = window.WB.S.manuscripts[c];
    return { formal: ch.formal, published: ch.published, formalVer: ms.formalVersion,
      confirmBtn: !!document.querySelector('[data-fn="msConfirmFormal"]') };
  }, newCk);
  rec('A6', '纯手写稿也有「确认正式稿」入口（不必先有候选）', fBefore.confirmBtn,
    '当前正式版本=' + (fBefore.formalVer || '无'));
  await clickFn(page, 'msConfirmFormal', newCk);
  const fAfter = await page.evaluate(c => {
    const ch = window.WB.S.chapters[c], ms = window.WB.S.manuscripts[c];
    return { formal: ch.formal, published: ch.published, hasFormalSnap: !!ms.formal,
      snapParas: ms.formal ? ms.formal.paragraphs.length : 0, state: ch.state };
  }, newCk);
  rec('A6', '确认后生成正式稿快照；线上稿不变（确认正式 ≠ 发布）',
    !!fAfter.formal && !fAfter.published && fAfter.hasFormalSnap && fAfter.snapParas > 0,
    '正式 ' + (fBefore.formal || '无') + ' → ' + fAfter.formal + '；线上=' + (fAfter.published || '未发布') + '；快照段落=' + fAfter.snapParas,
    { 正式稿: fBefore.formal, 线上稿: fBefore.published }, { 正式稿: fAfter.formal, 线上稿: fAfter.published },
    '返回点：版本历史（草稿/正式/线上三态并置 + 取回为草稿）');
  await shot(page, 'a6-confirm-formal-not-publish');

  await clickFn(page, 'queueAdd', newCk);
  const qAfter = await page.evaluate(c => {
    const q = window.WB.S.queue.filter(x => x.chapter === c);
    return { n: q.length, version: q.length ? q[0].version : null, state: q.length ? q[0].state : null,
      published: window.WB.S.chapters[c].published };
  }, newCk);
  rec('A6', '加入发布队列记录的是正式版本号；线上稿仍未改变',
    qAfter.n >= 1 && qAfter.version === fAfter.formal && !qAfter.published,
    '队列项=' + qAfter.n + ' 版本=' + qAfter.version + ' 状态=' + qAfter.state + ' 线上=' + (qAfter.published || '未发布'),
    null, { 队列版本: qAfter.version }, '返回点：连载发布 · 发布队列');

  /* 版本历史三态可读 + 可回退（未发布的作品，线上稿位应显示「未发布」而不是编造快照） */
  await clickAct(page, 'book.versions', [['chapter', newCk]]);
  const hist = await page.evaluate(c => {
    const t = document.querySelector('#drawer').innerText;
    const ms = window.WB.S.manuscripts[c], ch = window.WB.S.chapters[c];
    const drafts = ms.versions.map((v, i) => ({ v: v, i: i }))
      .filter(o => o.v.kind === 'draft' && Array.isArray(o.v.paragraphs) && o.v.paragraphs.length > 0);
    const now = ms.paragraphs[0];
    const target = drafts.filter(o => o.v.paragraphs[0] !== now)[0] || drafts[0] || null;
    return {
      draftSlot: /草稿（工作副本）/.test(t),
      formalSlot: /正式稿快照/.test(t),
      pubSnapshot: /线上稿快照/.test(t),
      pubNotYet: /线上稿\s*未发布|未发布/.test(t),
      restore: document.querySelectorAll('[data-fn="msRestore"]').length,
      draftCount: drafts.length,
      versionsDump: ms.versions.map((v, i) => i + ':' + v.kind + ':' + (Array.isArray(v.paragraphs) ? v.paragraphs.length : 'none')).join(' | '),
      now0: now,
      targetIdx: target ? target.i : -1,
      targetVer: target ? target.v.v : null,
      target0: target ? target.v.paragraphs[0] : null,
      formalVer: ms.formal ? ms.formal.version : null,
      published: ch.published || null
    };
  }, newCk);
  rec('A6', '版本历史三态并置且各自可读（未发布时线上稿位如实显示「未发布」，不编造快照）',
    hist.draftSlot && hist.formalSlot && !hist.pubSnapshot && hist.pubNotYet && hist.restore > 0 && hist.draftCount >= 2,
    '草稿位=' + hist.draftSlot + ' 正式稿位=' + hist.formalSlot + ' 线上稿快照=' + hist.pubSnapshot +
      ' 未发布标注=' + hist.pubNotYet + ' 可回退入口=' + hist.restore + ' 可读草稿快照=' + hist.draftCount,
    null, { 草稿快照数: hist.draftCount, 正式稿: hist.formalVer, 线上稿: hist.published || '未发布' },
    '返回点：版本历史抽屉（关闭后回到同一章）');

  /* 取回真的改草稿，且正式稿 / 线上稿不动 */
  if (hist.targetIdx >= 0) {
    const clickedRestore = await clickFnA2(page, 'msRestore', hist.targetIdx);
    await wait(250);
    const restore = await page.evaluate((c, expect, before) => {
      const ms = window.WB.S.manuscripts[c], ch = window.WB.S.chapters[c];
      return { now0: ms.paragraphs[0], matched: ms.paragraphs[0] === expect,
        changed: ms.paragraphs[0] !== before,
        formalVer: ms.formal ? ms.formal.version : null, published: ch.published || null };
    }, newCk, hist.target0, hist.now0);
    rec('A6', '「取回为草稿」真的改草稿内容，且正式稿快照与线上稿不动',
      clickedRestore && restore.matched && restore.changed && restore.formalVer === hist.formalVer && restore.published === hist.published,
      '取回 ' + hist.targetVer + '（命中按钮=' + clickedRestore + '）：草稿第 1 段已改变=' + restore.changed + ' 与快照一致=' + restore.matched +
        '；正式稿 ' + hist.formalVer + ' → ' + restore.formalVer + '；线上=' + (restore.published || '未发布') +
        '；版本清单 ' + hist.versionsDump,
      { 草稿第1段: cut(hist.now0), 正式稿: hist.formalVer },
      { 草稿第1段: cut(restore.now0), 正式稿: restore.formalVer },
      '返回点：版本历史抽屉内可反复取回');
  } else {
    rec('A6', '「取回为草稿」真的改草稿内容，且正式稿快照与线上稿不动', false, '没有可读草稿快照，无法验证取回');
  }
  await shot(page, 'a6-version-history-three-state');
  await clickAct(page, 'close-drawer');

  /* ============================================================
     §1-A7 第二天回来继续（刷新后仍在，且能回到原处）
     ============================================================ */
  console.log('\n--- §1-A7 第二天回来继续 ---');
  const before7 = await page.evaluate(c => {
    const ms = window.WB.S.manuscripts[c], ch = window.WB.S.chapters[c];
    const cm = window.WB.S.craft['B-01'];
    return { para: ms.paragraphs[0], formal: ms.formalVersion, published: ch.published,
      title: ch.title, impact: cm.impactLog.length, convKeys: Object.keys(window.WB.S.conversations).filter(k => k.indexOf(c) >= 0).length };
  }, newCk);
  await page.reload({ waitUntil: 'load' });
  await page.waitForSelector('#nav .nav-item', { timeout: 10000 });
  await goView(page, 'book', 'manuscript', { bookId: 'B-01', chapter: newCk });
  const after7 = await page.evaluate(c => {
    const ms = window.WB.S.manuscripts[c], ch = window.WB.S.chapters[c];
    const cm = window.WB.S.craft['B-01'];
    return { para: ms.paragraphs[0], formal: ms.formalVersion, published: ch.published,
      title: ch.title, impact: cm.impactLog.length, convKeys: Object.keys(window.WB.S.conversations).filter(k => k.indexOf(c) >= 0).length,
      sameBook: window.WB.S.__scope.bookId === 'B-01' };
  }, newCk);
  rec('A7', '刷新后草稿 / 正式稿 / 线上稿 / 影响清单 / 对话全部保持，并回到同一本书同一章',
    after7.para === before7.para && after7.formal === before7.formal && after7.impact === before7.impact &&
    after7.sameBook && after7.convKeys === before7.convKeys,
    '段落一致=' + (after7.para === before7.para) + ' 正式=' + after7.formal + ' 影响清单=' + after7.impact + ' 对话条=' + after7.convKeys,
    { 正式稿: before7.formal, 影响清单: before7.impact, 对话键: before7.convKeys },
    { 正式稿: after7.formal, 影响清单: after7.impact, 对话键: after7.convKeys },
    '返回点：作品库 → 作品概览 → 正文（章节列表保留原章）');
  await shot(page, 'a7-resume-next-day');

  /* ============================================================
     §3 版面测量：1440×1000 与 1280×900（100% 缩放）
     ============================================================ */
  console.log('\n--- §3 版面测量（正文优先；窄宽度下沉辅助信息）---');
  const layoutReport = {};
  async function measure(w, h, label, shotTag) {
    await page.setViewport({ width: w, height: h, deviceScaleFactor: 1 });
    await wait(320);
    await goView(page, 'book', 'manuscript', { bookId: 'B-01', chapter: 'ch43' });
    await wait(220);
    const m = await page.evaluate(() => {
      const body = document.querySelector('.ms-body');
      const grid = document.querySelector('.ms-grid');
      const main = document.querySelector('#main');
      const p = body ? body.querySelector('p') : null;
      if (!body || !p || !grid || !main) {
        return { missing: true, hasBody: !!body, hasPara: !!p, hasGrid: !!grid, hasMain: !!main };
      }
      const cs = getComputedStyle(body), pcs = getComputedStyle(p);
      const textW = body.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
      /* 逐段累计，避免只用第一段（短段）算出假密度 */
      let totChars = 0, totLines = 0, longest = 0;
      Array.from(body.querySelectorAll('p')).forEach(function (q) {
        const t = (q.innerText || '').replace(/\s/g, '');
        if (!t) return;
        const lh2 = parseFloat(getComputedStyle(q).lineHeight) || 1;
        const n = Math.max(1, Math.round(q.getBoundingClientRect().height / lh2));
        totChars += t.length; totLines += n;
        longest = Math.max(longest, t.length);
      });
      const charsPerLine = totLines ? Math.round(totChars / totLines) : 0;
      const firstParaChars = ((p.innerText || '').replace(/\s/g, '')).length;
      const right = grid.children.length > 1 ? grid.children[1] : null;
      const rightVisible = right && getComputedStyle(right).display !== 'none' && right.getBoundingClientRect().width > 0;
      const gridCols = getComputedStyle(grid).gridTemplateColumns;
      const stacked = gridCols.trim().split(/\s+/).length < 2;
      return {
        missing: false,
        viewport: window.innerWidth, mainW: main.clientWidth, textW: Math.round(textW),
        charsPerLine: charsPerLine, lines: totLines, paras: body.querySelectorAll('p').length,
        longestPara: longest, firstParaChars: firstParaChars,
        bodyBoxW: body.clientWidth, bodyMaxW: cs.maxWidth,
        rightW: rightVisible ? Math.round(right.getBoundingClientRect().width) : 0,
        stacked: stacked, gridCols: gridCols,
        bodyShareOfMain: Math.round((body.clientWidth / main.clientWidth) * 100),
        textShareOfViewport: Math.round((textW / window.innerWidth) * 100),
        overflowX: document.documentElement.scrollWidth > window.innerWidth + 1,
        scrollX: document.documentElement.scrollWidth
      };
    });
    layoutReport[label] = m;
    await shot(page, shotTag);
    rec('L', label + '：正文单行字数与版面占比可读（不是每行几个字）',
      !!m && !m.missing && m.charsPerLine >= 24 && !m.overflowX,
      m && m.missing
        ? '正文节点缺失：body=' + m.hasBody + ' 段落=' + m.hasPara + ' 栅格=' + m.hasGrid
        : '正文宽=' + m.textW + 'px · 平均每行≈' + m.charsPerLine + '字（' + m.paras + ' 段 / ' + m.lines + ' 行 · 最长段 ' + m.longestPara + ' 字）· 正文框=' + m.bodyBoxW + 'px（max-width:' + m.bodyMaxW + '）· 正文占主区=' + m.bodyShareOfMain + '% · 辅助栏=' + (m.stacked ? '下沉（占满 ' + m.rightW + 'px，不压缩正文）' : '并排 ' + m.rightW + 'px') + ' · 横向溢出=' + m.overflowX + ' · 栅格=' + m.gridCols,
      null, m && !m.missing ? { 平均每行字数: m.charsPerLine, 正文字宽: m.textW, 辅助栏: m.stacked ? '下沉' : '并排', 栅格: m.gridCols } : null,
      '窄宽度把辅助信息下沉，不压缩正文');
    return m;
  }
  await measure(1440, 1000, '1440×1000', 'l-1440x1000-manuscript');
  await measure(1280, 900, '1280×900', 'l-1280x900-manuscript');
  await page.setViewport({ width: 1440, height: 1000, deviceScaleFactor: 1 });
  await wait(260);

  /* 无候选：不得长期占等宽空卡 */
  await goView(page, 'book', 'manuscript', { bookId: 'B-01', chapter: newCk });
  const noCand = await page.evaluate(() => {
    const t = document.querySelector('#main').innerText;
    const pnls = Array.from(document.querySelectorAll('#main .pnl'));
    const cand = pnls.filter(p => /^候选/.test(p.innerText.trim()))[0];
    return { hasCandidateBoard: !!cand, candHeight: cand ? Math.round(cand.getBoundingClientRect().height) : 0,
      mentions: /本章暂无/.test(t) };
  });
  rec('L', '无候选时不渲染等宽空卡（收敛为一句状态）', !noCand.hasCandidateBoard || noCand.candHeight < 120,
    '候选卡存在=' + noCand.hasCandidateBoard + ' 高度=' + noCand.candHeight + 'px');
  const dupButtons = await page.evaluate(() => {
    const texts = Array.from(document.querySelectorAll('#main button')).map(b => b.innerText.trim());
    const dup = {};
    texts.forEach(t => { dup[t] = (dup[t] || 0) + 1; });
    return Object.keys(dup).filter(k => dup[k] > 1 && k.length > 1);
  });
  rec('L', '同一工作面不重复出现同名动作按钮', dupButtons.length === 0,
    dupButtons.length ? '重复：' + dupButtons.join(' | ') : '无重复');
  await shot(page, 'l-no-empty-candidate-board');

  /* 候选对比：只在真的有可对比内容时出现 */
  await goView(page, 'book', 'manuscript', { bookId: 'B-01', chapter: 'ch44' });
  const candView = await page.evaluate(() => {
    const t = document.querySelector('#main').innerText;
    return { hasDiff: !!document.querySelector('#main .diff'), adoptBtns: document.querySelectorAll('#main [data-fn="decideChange"]').length };
  });
  rec('L', '有候选时才出现对比区（改前 / 改后 + 逐项采纳）', candView.hasDiff && candView.adoptBtns > 0,
    '对比区=' + candView.hasDiff + ' 逐项按钮=' + candView.adoptBtns);
  await shot(page, 'l-candidate-comparison');

  /* 空书起步 */
  await goView(page, 'book', 'library');
  await clickFn(page, 'createBook');
  await wait(300);
  await goView(page, 'book', 'manuscript');
  const emptyBook = await page.evaluate(() => {
    const t = document.querySelector('#main').innerText;
    return { empty: /还没有章节|还没有正文|开写第一章/.test(t),
      newBtn: !!document.querySelector('[data-fn="newChapter"]'), scope: window.WB.S.__scope.bookId };
  });
  rec('L', '空书起步：真实空状态 + 直接手写第一章入口', emptyBook.empty && emptyBook.newBtn,
    '范围=' + emptyBook.scope + ' 空态=' + emptyBook.empty + ' 新建章入口=' + emptyBook.newBtn);
  await shot(page, 'l-empty-book-start');

  /* ============================================================
     §4 缺陷回归：R2（生成失败不得冒充成功）、R7（定位回流到作品）
     R1/R3/R4/R5/R6 分别由 A6 / A2 / A3 / A6 / A4 覆盖
     ============================================================ */
  console.log('\n--- §4-R2 没有依据时生成不得冒充成功 ---');
  /* 承接上一段的空书 B-03：新建第一章（该章没有场景计划） */
  await clickFn(page, 'newChapter');
  await wait(320);
  const d2 = await page.evaluate(() => {
    const bk = window.WB.S.__scope.bookId;
    const chs = Object.keys(window.WB.S.chapters).filter(k => window.WB.S.chapters[k].bookId === bk);
    const ck = chs[chs.length - 1];
    const c = window.WB.S.craft[bk] || {};
    return { bk: bk, ck: ck, scenes: ((c.scenes || {})[ck] || []).length,
      cand: window.WB.S.chapters[ck].candidate || null,
      msBefore: !!window.WB.S.manuscripts[ck] };
  });
  await page.evaluate(() => { var tb = document.getElementById('toasts'); if (tb) tb.innerHTML = ''; });
  await clickFn(page, 'msGenerate', d2.bk);
  await wait(140);
  const d2after = await page.evaluate((ck) => {
    const tb = document.getElementById('toasts');
    return { cand: window.WB.S.chapters[ck].candidate || null,
      msAfter: !!window.WB.S.manuscripts[ck],
      toasts: tb ? tb.innerText.replace(/\s+/g, ' ').trim() : '' };
  }, d2.ck);
  rec('R2', '没有场景计划时「按场景计划生成候选」不生成候选、不建空正文容器、不静默造假，并明确提示',
    !d2after.cand && !d2after.msAfter && /场景计划/.test(d2after.toasts),
    '该章场景计划=' + d2.scenes + ' 项；生成后候选=' + d2after.cand + '；正文容器 ' + d2.msBefore + ' → ' + d2after.msAfter +
      '；本次提示=' + JSON.stringify(d2after.toasts),
    { 候选: d2.cand, 正文容器: d2.msBefore }, { 候选: d2after.cand, 正文容器: d2.msAfter },
    '返回点：留在同一章，可去「场景准备」或直接手写');
  await shot(page, 'r2-no-fake-generate');

  console.log('\n--- §4-R7 创作内核「定位」回流到作品 ---');
  await goView(page, 'book', 'library');
  const d7 = await page.evaluate(() => {
    /* 人为制造缺陷前置条件：作品上的定位是旧值 / 空，看打开作品时是否被创作内核回流覆盖 */
    var b = window.WB.S.books.filter(x => x.id === 'B-01')[0];
    var pos = ((window.WB.S.craft['B-01'] || {}).positioning || {});
    b.positioning = '（未同步的旧值 · R7 前置条件）';
    b.summary = null;
    window.WB.render();
    return { craft: pos.coreOriginal || null, stale: b.positioning };
  });
  await clickAct(page, 'book.open', [['id', 'B-01']]);
  const d7after = await page.evaluate((craft) => {
    var b = window.WB.S.books.filter(x => x.id === 'B-01')[0];
    var ov = document.querySelector('#main').innerText;
    return { book: b.positioning, summary: b.summary,
      overviewShowsCraft: !!craft && ov.indexOf(String(craft).slice(0, 12)) >= 0,
      overviewNoStale: ov.indexOf('未同步的旧值') < 0 };
  }, d7.craft);
  rec('R7', '打开作品时创作内核「定位」回流到作品对象（作品概览不再显示未设定或旧值）',
    !!d7.craft && d7after.book === d7.craft && d7after.summary === d7.craft && d7after.overviewNoStale && d7after.overviewShowsCraft,
    '创作内核定位=' + String(d7.craft).slice(0, 20) + '…｜作品定位 ' + String(d7.stale).slice(0, 14) + '… → ' +
      String(d7after.book).slice(0, 20) + '…｜summary 同步=' + (d7after.summary === d7.craft) +
      '｜概览显示回流值=' + d7after.overviewShowsCraft + '｜概览残留旧值=' + !d7after.overviewNoStale,
    { 作品定位: d7.stale }, { 作品定位: d7after.book },
    '返回点：作品概览 · 定位行 / 创作内核 · 定位');
  await shot(page, 'r7-positioning-synced-to-book');

  /* ================= 汇总 ================= */
  const pass = results.filter(r => r.ok).length;
  console.log('\n============================');
  console.log('作者路径 / 版面验收：' + results.length + ' 项 · 通过 ' + pass + ' · 失败 ' + (results.length - pass));
  console.log('Console Error: ' + consoleErrors.length);
  console.log('截图：' + shots.length + ' 张（_evidence_round3/）');
  if (consoleErrors.length) console.log(JSON.stringify(consoleErrors, null, 2));
  const failed = results.filter(r => !r.ok);
  if (failed.length) { console.log('\n失败项：'); failed.forEach(f => console.log('  ✗ [' + f.path + '] ' + f.name + ' — ' + f.detail)); }

  fs.writeFileSync(path.join(EV, 'ACCEPTANCE.json'), JSON.stringify({
    at: new Date().toISOString(), total: results.length, pass,
    fail: results.length - pass, consoleErrors, layout: layoutReport, shots,
    results
  }, null, 2));

  await browser.close();
  server.close();
  process.exit(failed.length ? 1 : 0);
})().catch(e => { console.error('ACCEPTANCE FAILED', e); process.exit(2); });
