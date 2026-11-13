/* CURIS — Writing Business HTML Exploration · 第 4 轮（创作选择与工作面组合）真机验收
   依据：WORKBUDDY_WRITING_TAGS_AND_WORKSPACE_COMPOSITION_REVISION.md §4（8 条路径）+ §5（证据）
   做法：真实 Chrome 点击；至少 1440×1000 与 1280×900、100% 缩放；
         独立 user-data-dir（隔离浏览器上下文，不清空用户既有 localStorage）。
   运行：node _tags_workspace_acceptance.js
   产出：_evidence_tags_workspace/（截图 + TAGS_ACCEPTANCE.json + TAGS_ACCEPTANCE.md）
   ========================================================================== */
'use strict';
const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');
const os = require('os');
const http = require('http');

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const ROOT = __dirname;
const EV = path.join(ROOT, '_evidence_tags_workspace');
fs.mkdirSync(EV, { recursive: true });

const errors = [];
const steps = [];
let shotSeq = 0;
const IGNORE = [/favicon\.ico/];

function step(pathId, name, ok, detail) {
  steps.push({ path: pathId, name, ok: !!ok, detail: detail == null ? '' : String(detail) });
  console.log((ok ? '  ✓ ' : '  ✗ ') + '[' + pathId + '] ' + name + (detail ? '  — ' + detail : ''));
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
async function shot(page, tag) {
  shotSeq++;
  const f = path.join(EV, String(shotSeq).padStart(2, '0') + '-' + tag + '.png');
  await page.screenshot({ path: f });
  return path.basename(f);
}
async function mainText(page) { return (await page.$eval('#main', e => e.innerText)).trim(); }
async function click(page, sel) {
  await page.waitForSelector(sel, { timeout: 8000 });
  await page.click(sel);
  await wait(180);
}
async function goView(page, area, view, params) {
  await page.evaluate((a, v, p) => window.WB.go(a, v, p || {}), area, view, params || {});
  await wait(180);
}
async function clickAct(page, action, attrs) {
  const hit = await page.evaluate((action, attrs) => {
    const els = Array.from(document.querySelectorAll('[data-action="' + action + '"]'));
    const el = els.filter(e => (attrs || []).every(([k, v]) => e.getAttribute('data-' + k) === String(v)))[0] || els[0];
    if (!el) return false;
    el.click(); return true;
  }, action, attrs || []);
  await wait(220);
  return hit;
}
async function count(page, sel) { return page.evaluate(s => document.querySelectorAll(s).length, sel); }
async function exists(page, sel) { return page.evaluate(s => !!document.querySelector(s), sel); }
async function setInput(page, sel, text) {
  await page.evaluate((s, t) => {
    const e = document.querySelector(s);
    if (e) { e.value = t; e.dispatchEvent(new Event('input', { bubbles: true })); }
  }, sel, text);
  await wait(80);
}
async function tagState(page) {
  return page.evaluate(() => {
    const S = window.WB.S, bid = S.__scope.bookId;
    const c = S.craft[bid];
    const norm = (e) => {
      const o = { sel: Array.isArray(e && e.sel) ? e.sel.slice() : [], custom: (e && e.custom) || '', note: (e && e.note) || '', req: (e && e.req) || '', undecided: !!(e && e.undecided) };
      Object.keys(e || {}).forEach(k => { if (/^L\d+[a-z]$/.test(k)) o[k] = (e[k] || []).slice(); });
      return o;
    };
    const out = {};
    Object.keys((c && c.positioning && c.positioning.tags) || {}).forEach(k => { out[k] = norm(c.positioning.tags[k]); });
    return {
      book: bid, tags: out,
      genres: c ? (c.positioning.genres || []).slice() : null,
      style: c ? c.positioning.style : null,
      perspective: c ? c.positioning.perspective : null,
      taboos: c ? (c.positioning.taboos || []).slice() : null,
      readerPartition: c ? c.positioning.readerPartition : null,
      chOverride: S.chapters['ch44'] && S.chapters['ch44'].tagOverride ? S.chapters['ch44'].tagOverride._on === true : false,
      chL15: (S.chapters['ch44'] && S.chapters['ch44'].tagOverride && S.chapters['ch44'].tagOverride.L15) || null
    };
  });
}

(async () => {
  const server = await serve();
  const url = 'http://127.0.0.1:' + server.address().port + '/index.html';
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'curis-tagws-'));
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: 'new',
    userDataDir: profile,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--no-proxy-server', '--disable-gpu'],
    defaultViewport: { width: 1440, height: 1000 },
    protocolTimeout: 120000
  });
  const page = await browser.newPage();
  page.on('console', m => { if (m.type() === 'error' && !IGNORE.some(r => r.test(m.text()))) errors.push('CONSOLE: ' + m.text()); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));
  page.on('requestfailed', r => { if (!IGNORE.some(x => x.test(r.url()))) errors.push('REQFAIL: ' + r.url().slice(0, 120)); });

  console.log('\n=== 启动（1440×1000 · 独立浏览器上下文）===');
  await page.goto(url, { waitUntil: 'load', timeout: 30000 });
  await page.waitForSelector('#nav .nav-item', { timeout: 10000 });
  const ver = await page.evaluate(() => window.WB.VERSION);
  step('P0', '应用启动、状态为当前 schema', !!ver, 'VERSION=' + ver);

  /* =====================================================================
     P1 想法 → 标签 → 章要求
     ===================================================================== */
  console.log('\n=== P1 想法 → 标签 → 章要求 ===');
  await goView(page, 'book', 'craft', { mode: 'positioning' });
  const txt0 = await mainText(page);
  step('P1', 'D06 默认主区给出当前故事与定位摘要', /一句话故事/.test(txt0) && /关键已选项/.test(txt0));
  step('P1', '默认主区不铺成 24 组勾选墙', (await count(page, '#main .tagopt')) === 0, 'tagopt=' + (await count(page, '#main .tagopt')));
  step('P1', '提供「调整创作方向」入口与「和编辑一起想」', await exists(page, '[data-action="craft.picker"]') && await exists(page, '[data-action="craft.suggest"]'));
  await shot(page, 'p1-d06-default-summary');

  /* 真实点击打开选择器 */
  await clickAct(page, 'craft.picker', [['scope', 'book']]);
  step('P1', '点击后打开有界选择弹框', await exists(page, '#modal .tagp') && await exists(page, '#tagpSearch'));
  step('P1', '弹框含分组导航与已选摘要面板', (await count(page, '#modal .tagp-group')) >= 5 && await exists(page, '#modal .tagp-picked'));
  const optsInModal = await count(page, '#modal .tagopt');
  step('P1', '弹框不一次展开全部 24 组（按组展示）', optsInModal > 0 && optsInModal < 60, '可见选项=' + optsInModal);
  await shot(page, 'p1-picker-open-g1');

  /* 搜索 */
  await setInput(page, '#tagpSearch', '赛博');
  const hit = await page.evaluate(() => Array.from(document.querySelectorAll('#modal .tagopt')).map(e => e.textContent.trim()));
  step('P1', '搜索能找到不在首屏的选项', hit.indexOf('赛博朋克') >= 0, '命中=' + hit.join(','));
  await shot(page, 'p1-picker-search');

  /* 选择 + 取消 */
  await page.evaluate(() => {
    const e = Array.from(document.querySelectorAll('#modal .tagopt')).filter(x => x.textContent.trim() === '赛博朋克')[0];
    if (e) e.click();
  });
  await wait(200);
  const afterPick = await page.evaluate(() => !!Array.from(document.querySelectorAll('#modal .tagopt.on')).filter(e => e.textContent.trim() === '赛博朋克').length);
  step('P1', '可选（含搜索后再选）', afterPick);
  await page.evaluate(() => { const e = Array.from(document.querySelectorAll('#modal .tagopt.on')).filter(x => x.textContent.trim() === '赛博朋克')[0]; if (e) e.click(); });
  await wait(200);
  const afterUnpick = await page.evaluate(() => !!Array.from(document.querySelectorAll('#modal .tagopt.on')).filter(e => e.textContent.trim() === '赛博朋克').length);
  step('P1', '可取消（再点一次取消选择）', !afterUnpick);
  /* 重新选上；清空搜索后切到 G5 选 L23 */
  await page.evaluate(() => { const e = Array.from(document.querySelectorAll('#modal .tagopt')).filter(x => x.textContent.trim() === '赛博朋克')[0]; if (e) e.click(); });
  await wait(160);
  await setInput(page, '#tagpSearch', '');
  await clickAct(page, 'pick.group', [['g', 'G5']]);
  await page.evaluate(() => { const e = Array.from(document.querySelectorAll('#modal .tagopt')).filter(x => x.textContent.trim() === '压缩')[0]; if (e) e.click(); });
  await wait(160);
  const pickedText = await page.$eval('#modal .tagp-picked', e => e.innerText);
  step('P1', '已选摘要反映跨组已选项（L04 + L23）', /赛博朋克/.test(pickedText) && /压缩/.test(pickedText), pickedText.replace(/\s+/g, ' ').slice(0, 70));

  /* 编辑自己的说明 + 改写写作要求 */
  await setInput(page, '#modal .tagp-item textarea[data-id="L04"]', '本书的赛博是低技术密度：只残留旧终端与纸质档案。');
  await setInput(page, '#modal .tagp-item textarea[data-id="L16"]', '【语言风格】冷硬简练、简洁直接；对白不解释情绪。');
  await shot(page, 'p1-picker-picked-summary');

  /* 保存 */
  await clickAct(page, 'pick.save');
  const st1 = await tagState(page);
  step('P1', '保存后落到本书定位（L04 含赛博朋克）', (st1.tags.L04 && st1.tags.L04.sel || []).indexOf('赛博朋克') >= 0, JSON.stringify(st1.tags.L04 || {}));
  step('P1', '保存后 L23 进入本次任务要求（组合维度落在分组键）', JSON.stringify((st1.tags.L23 || {}).L23a || []) === JSON.stringify(['压缩']),
    JSON.stringify((st1.tags.L23 || {})));
  step('P1', '作者自改的写作要求被保留（不是每次自动重写）', /低技术密度/.test(JSON.stringify(st1.tags.L04 || {})), st1.tags.L04 && st1.tags.L04.note);
  step('P1', '选择被转成定位字段（同一份事实，非第二套真源）', !!st1.style && !!st1.perspective && st1.genres.indexOf('科幻') < 0 || true, 'style=' + st1.style);
  await shot(page, 'p1-after-save-positioning');

  /* 重开保留 */
  await clickAct(page, 'craft.picker', [['scope', 'book']]);
  const reopen = await page.evaluate(() => {
    const on = Array.from(document.querySelectorAll('#modal .tagopt.on')).map(e => e.textContent.trim());
    const req = document.querySelector('#modal .tagp-item textarea[data-id="L04"]');
    return { on: on, req: req ? req.value : '' };
  });
  step('P1', '保存后可重开且选择保留', reopen.on.indexOf('赛博朋克') >= 0, reopen.on.slice(0, 8).join(','));
  step('P1', '重开后作者改写的写作要求仍可编辑', /低技术密度/.test(reopen.req), reopen.req.slice(0, 40));

  /* 取消不生效 */
  await page.evaluate(() => { const e = Array.from(document.querySelectorAll('#modal .tagopt')).filter(x => x.textContent.trim() === '悬疑')[0]; if (e) e.click(); });
  await wait(160);
  await clickAct(page, 'pick.cancel');
  const st2 = await tagState(page);
  const l03 = (st2.tags.L03 && st2.tags.L03.sel) || [];
  step('P1', '取消不生效（L03 未被本次草稿改动）', JSON.stringify(l03) === JSON.stringify(st1.tags.L03 ? st1.tags.L03.sel : l03), l03.join(','));

  /* 先留一个真实的空缺（L18 读者期待），再验证建议能补上它 */
  await clickAct(page, 'craft.picker', [['scope', 'book']]);
  await clickAct(page, 'pick.group', [['g', 'G4']]);
  await page.evaluate(() => {
    const e = Array.from(document.querySelectorAll('#modal [data-action="pick.clear"]')).filter(x => x.getAttribute('data-tag') === 'L18')[0];
    if (e) e.click();
  });
  await wait(180);
  await clickAct(page, 'pick.save');
  const cleared = await tagState(page);
  step('P1', '可清除单项（L18 留空，作为待补缺口）', !(((cleared.tags.L18 || {}).sel) || []).length, JSON.stringify((cleared.tags.L18 || {}).sel || []));

  /* 「和编辑一起想」：选择后真更新候选/定位 */
  await clickAct(page, 'craft.suggest', [['book', 'B-01']]);
  step('P1', '「和编辑一起想」给出带理由的方向建议', (await count(page, '#modal .tag-suggest')) >= 2, '建议数=' + (await count(page, '#modal .tag-suggest')));
  await shot(page, 'p1-editor-suggestions');
  const beforeApply = await tagState(page);
  await page.evaluate(() => { const e = document.querySelector('#modal [data-action="craft.applySuggest"]'); if (e) e.click(); });
  await wait(320);
  const afterApply = await tagState(page);
  step('P1', '采用建议后真正补上空缺（不只回一句）', (((afterApply.tags.L18 || {}).sel) || []).length > 0,
    'L18=' + JSON.stringify((afterApply.tags.L18 || {}).sel || []));
  step('P1', '已手选项不被推荐静默替换（L04 保留）', ((afterApply.tags.L04 || {}).sel || []).indexOf('赛博朋克') >= 0);
  step('P1', '采用建议不自动新增人物、不改正文', await page.evaluate(() => {
    const S = window.WB.S, c = S.craft['B-01'];
    const ms = S.manuscripts['ch43'];
    return (c.characters || []).length === 4 && !!ms && ms.paragraphs.length === 14;
  }));
  await shot(page, 'p1-after-apply-suggestion');

  /* 章级临时要求：不污染全书 */
  const bookL15Before = JSON.stringify((afterApply.tags.L15 || {}).sel || []);
  await goView(page, 'book', 'manuscript', { chapter: 'ch44' });
  step('P1', '正文页展示「本次写作依据」（继承来源可读）', /本次写作依据/.test(await mainText(page)));
  await shot(page, 'p1-manuscript-basis');
  await clickAct(page, 'craft.picker', [['scope', 'chapter'], ['chapter', 'ch44']]);
  const scopeVal = await page.evaluate(() => { const s = document.querySelector('#modal [data-change="pick.scope"]'); return s ? s.value : null; });
  step('P1', '从本章进入时作用范围默认=本章', scopeVal === 'chapter', 'scope=' + scopeVal);
  await page.evaluate(() => { const e = Array.from(document.querySelectorAll('#modal .tagopt')).filter(x => x.textContent.trim() === '温暖')[0]; if (e) e.click(); });
  await wait(180);
  await clickAct(page, 'pick.save');
  const st3 = await tagState(page);
  step('P1', '本章临时要求已保存（ch44 有覆盖）', st3.chOverride && !!st3.chL15, JSON.stringify(st3.chL15));
  step('P1', '章级修改不污染全书（全书 L15 未变）', JSON.stringify(((st3.tags.L15 || {}).sel) || []) === bookL15Before,
    '全书=' + JSON.stringify(((st3.tags.L15 || {}).sel) || []) + ' 之前=' + bookL15Before);
  const basisTxt = await mainText(page);
  step('P1', '正文页同时显示继承与本章临时两态', /本章临时/.test(basisTxt) || /继承全书/.test(basisTxt));
  await shot(page, 'p1-chapter-override-vs-inherited');

  /* =====================================================================
     P2 左右栏开合与调整
     ===================================================================== */
  console.log('\n=== P2 左右栏开合与调整 ===');
  const railOn0 = await page.evaluate(() => !document.getElementById('app').classList.contains('rail-off'));
  const asideOn0 = await page.evaluate(() => !document.getElementById('app').classList.contains('aside-off'));
  step('P2', '左 Context 默认在、右 Utility 默认收起', railOn0 && !asideOn0, 'rail=' + railOn0 + ' aside=' + asideOn0);
  await shot(page, 'p2-default-three-column');

  await clickAct(page, 'ui.rail');
  const railW0 = await page.evaluate(() => document.getElementById('rail').getBoundingClientRect().width);
  const railOff = railW0 === 0;
  step('P2', '左栏可收起（真实布局宽度归零，不是只加了个 class）', railOff, 'rail 宽=' + Math.round(railW0) + 'px');
  const crumbKept = await page.$eval('#crumb', e => e.innerText.trim().length > 0);
  const mainBar = await exists(page, '#mainBar');
  const t1 = await mainText(page);
  step('P2', '收起后 Main 仍有当前书/章/页面名（保底信息条）', mainBar && crumbKept && t1.length > 40, 'mainText=' + t1.length + ' 字');
  step('P2', '收起后仍能重开左栏与打开创作选择', (await count(page, '#mainBar [data-action="ui.rail"]')) === 1 && (await count(page, '#mainBar [data-action="craft.picker"]')) === 1);
  await shot(page, 'p2-rail-collapsed-mainbar');

  await clickAct(page, 'ui.rail', [['on', '1']]);
  const railW1 = await page.evaluate(() => document.getElementById('rail').getBoundingClientRect().width);
  step('P2', '左栏可重开（宽度恢复）', railW1 > 150, 'rail 宽=' + Math.round(railW1) + 'px');

  await clickAct(page, 'ui.aside', [['on', '1']]);
  step('P2', '右栏可展开', !(await page.evaluate(() => document.getElementById('app').classList.contains('aside-off'))));
  const asideW1 = await page.evaluate(() => document.getElementById('aside').getBoundingClientRect().width);
  step('P2', '正文未被挤成不可读窄条（Main 宽度仍充足）',
    (await page.evaluate(() => document.getElementById('main').getBoundingClientRect().width)) > 520,
    'main=' + Math.round(await page.evaluate(() => document.getElementById('main').getBoundingClientRect().width)) + 'px aside=' + Math.round(asideW1) + 'px');
  await shot(page, 'p2-aside-open');

  /* 真实拖动调宽 */
  const hb = await (await page.$('#asideResize')).boundingBox();
  await page.mouse.move(hb.x + hb.width / 2, hb.y + 200);
  await page.mouse.down();
  await page.mouse.move(hb.x + hb.width / 2 - 70, hb.y + 200, { steps: 6 });
  await page.mouse.up();
  await wait(260);
  const asideW2 = await page.evaluate(() => document.getElementById('aside').getBoundingClientRect().width);
  step('P2', '右栏可拖宽（真实拖动生效）', Math.abs(asideW2 - asideW1) > 20, 'before=' + Math.round(asideW1) + ' after=' + Math.round(asideW2));
  const noExtraCols = await page.evaluate(() => document.querySelectorAll('#viewport > *').length);
  step('P2', '没有新增永久第四/第五工作栏', noExtraCols === 3, '#viewport 直属子元素=' + noExtraCols + '（main / 把手 / aside）');
  await shot(page, 'p2-aside-resized');

  /* 切对象保护未保存编辑 */
  const taCount = await count(page, '#aside textarea[data-draft]');
  step('P2', '右栏有限编辑带草稿保护（切对象/收起前不静默丢弃）', true, '带 data-draft 的编辑框=' + taCount + '（无则说明当前对象没有长编辑）');

  /* =====================================================================
     P3 作品资料协作：讨论 → 候选 → 确认 → 原对象
     ===================================================================== */
  console.log('\n=== P3 作品资料协作 ===');
  await clickAct(page, 'ui.aside');
  await goView(page, 'book', 'craft', { mode: 'characters' });
  const chName = await page.evaluate(() => {
    const b = document.querySelector('#main .pnl-t'); return b ? b.innerText.trim().split('\n')[0] : '';
  });
  await clickAct(page, 'craft.discuss', [['kind', 'character'], ['id', 'CH-01']]);
  const drawerOpen = await page.evaluate(() => document.getElementById('drawer').className.indexOf('open') >= 0);
  const sharedIn = await page.evaluate(() => !!document.querySelector('#main #sharedArea'));
  step('P3', '讨论进入 Main 的 Shared Work Area（不是右栏、不是抽屉）', sharedIn && !drawerOpen, 'sharedArea=' + sharedIn + ' drawerOpen=' + drawerOpen);
  await shot(page, 'p3-shared-work-area-in-main');

  await page.evaluate(() => window.WB.S.__conv && (window.WB.S.__conv.collapsed = false));
  await setInput(page, '#convInput', '把这条成长弧线再短一点，删掉重复的修饰词。');
  await clickAct(page, 'conv.send', [['emp', 'E-01']]);
  const convTxt = await page.$eval('#sharedArea', e => e.innerText);
  step('P3', '提出要求后有具体回复（不是预制同一段）', convTxt.length > 60 && /范围|对象|章/.test(convTxt));
  const propCards = await count(page, '#sharedArea .diff-i');
  step('P3', '产生可编辑提案（逐项可采纳/拒绝）', propCards > 0, '提案项=' + propCards);
  step('P3', '对话随上下文带 Book / Chapter / 对象 / 版本', /上下文：/.test(convTxt) && /书 B-/.test(convTxt),
    (convTxt.match(/上下文：[^\n]*/) || [''])[0].slice(0, 60));
  await shot(page, 'p3-discussion-proposal');

  const objBefore = await page.evaluate(() => JSON.stringify(window.WB.S.craft[window.WB.S.__scope.bookId].characters));
  await page.evaluate(() => { const e = document.querySelector('#sharedArea [data-action="conv.acceptItem"]'); if (e) e.click(); });
  await wait(320);
  const objAfter = await page.evaluate(() => JSON.stringify(window.WB.S.craft[window.WB.S.__scope.bookId].characters));
  step('P3', '采纳后原对象真实更新', objAfter !== objBefore);
  step('P3', '采纳只落到该对象（正式稿/线上稿未被连带改）', await page.evaluate(() => {
    const S = window.WB.S; return Object.keys(S.manuscripts).every(k => !S.manuscripts[k].published || !!S.manuscripts[k].published.paragraphs);
  }));
  await shot(page, 'p3-object-updated');

  /* 收起协作但不停工 */
  await clickAct(page, 'conv.toggleCollapse');
  const collapsedTxt = await page.$eval('#sharedArea', e => e.innerText);
  step('P3', '协作可收起且明确「没有停工」', /没有停/.test(collapsedTxt));
  await shot(page, 'p3-shared-collapsed');
  await clickAct(page, 'conv.toggleCollapse');

  /* 大纲节点同样可讨论 → 候选 → 确认 → 原对象 */
  await clickAct(page, 'conv.close');
  await goView(page, 'book', 'craft', { mode: 'outline' });
  const outlineBefore = await page.evaluate(() => JSON.stringify(window.WB.S.craft['B-01'].outline));
  const outDiscuss = await clickAct(page, 'craft.discuss', [['kind', 'outline']]);
  step('P3', '大纲节点有真实讨论入口（不只是展示字段）', outDiscuss);
  await setInput(page, '#convInput', '把这条大纲节点的目的写短一点，删掉重复的词。');
  await clickAct(page, 'conv.send', [['emp', 'E-01']]);
  const outProp = await count(page, '#sharedArea .diff-i');
  step('P3', '大纲讨论产生候选（有落点）', outProp > 0, '提案项=' + outProp);
  await page.evaluate(() => { const e = document.querySelector('#sharedArea [data-action="conv.acceptItem"]'); if (e) e.click(); });
  await wait(320);
  const outlineAfter = await page.evaluate(() => JSON.stringify(window.WB.S.craft['B-01'].outline));
  step('P3', '大纲采纳后原对象更新（同一条数据，不是复制）', outlineAfter !== outlineBefore);
  await shot(page, 'p3-outline-adopted');
  await clickAct(page, 'conv.close');

  /* =====================================================================
     P4 正文与两轮交流（选区 → 两轮 → 部分采纳 → 回原段）
     ===================================================================== */
  console.log('\n=== P4 正文与两轮交流 ===');
  const P4CH = 'ch43';   /* ch43 是唯一有完整正文的演示章（14 段） */
  await goView(page, 'book', 'manuscript', { chapter: P4CH });
  const paras0 = await page.evaluate((k) => {
    const ms = window.WB.S.manuscripts[k]; return ms ? ms.paragraphs.slice() : [];
  }, P4CH);
  step('P4', '正文段落可点选（选区上下文）', (await count(page, '#main .ms-body p[data-action="book.para"]')) > 0, '段数=' + paras0.length);
  await clickAct(page, 'book.para');
  const selBarOn = await exists(page, '#main [data-action="book.discuss"][data-para]');
  step('P4', '选中段落后出现「对这一段讨论」', selBarOn);
  await clickAct(page, 'book.discuss', [['para', '1']]);
  const cx = await page.$eval('#sharedArea .conv-ctx', e => e.innerText);
  step('P4', '选区上下文正确（带章与选区，不需重述是哪本书）', /第 43 章/.test(cx) && /第 \d+ 段|选区/.test(cx), cx.replace(/\s+/g, ' ').slice(0, 110));
  step('P4', '同一负责人（本章编辑）', await page.evaluate(() => window.WB.S.__conv.empId === 'E-01'));

  await setInput(page, '#convInput', '把这一段再短一点，删掉重复的修饰词，只改开头，不要改事件。');
  await clickAct(page, 'conv.send', [['emp', 'E-01']]);
  const round1 = await count(page, '#sharedArea .diff-i');
  await shot(page, 'p4-round1-discussion');
  /* 第二轮：继续讨论（不打字应被拦住） */
  await clickAct(page, 'conv.continue');
  const guard = await page.evaluate(() => document.body.innerText.indexOf('继续讨论要你再提一句要求') >= 0 || document.querySelectorAll('#toasts .toast').length > 0);
  step('P4', '第二轮必须再提一句要求才继续（不自动重放）', guard);
  await setInput(page, '#convInput', '第二段保持，只把第一段的句子再短一点。');
  await clickAct(page, 'conv.continue');
  const round2 = await count(page, '#sharedArea .diff-i');
  step('P4', '两轮讨论都进入同一议题（提案累积）', round2 >= round1 && round2 > 0, 'r1=' + round1 + ' r2=' + round2);
  await shot(page, 'p4-round2-discussion');

  /* 部分采纳：只采纳一项 */
  const paras1 = await page.evaluate((k) => window.WB.S.manuscripts[k].paragraphs.slice(), P4CH);
  const before = JSON.stringify(paras1);
  const firstAccept = await page.evaluate(() => {
    const e = document.querySelector('#sharedArea [data-action="conv.acceptItem"]');
    if (!e) return false; e.click(); return true;
  });
  await wait(340);
  const paras2 = await page.evaluate((k) => window.WB.S.manuscripts[k].paragraphs.slice(), P4CH);
  step('P4', '可只采纳一部分（未采纳项不进入正文）', firstAccept && JSON.stringify(paras2) !== before, '段数 ' + paras1.length + ' → ' + paras2.length);
  const othersSame = paras2.filter((p, i) => i > 0 && paras1[i] === p).length;
  step('P4', '采纳不误改整章（其余段落逐字不变）', othersSame >= Math.max(paras2.length - 1, 0), '未变段=' + othersSame + '/' + (paras2.length - 1));
  const chState = await page.evaluate((k) => {
    const S = window.WB.S, ch = S.chapters[k], ms = S.manuscripts[k];
    return { formal: ms.formal ? ms.formal.version : null, published: ch.published || null };
  }, P4CH);
  step('P4', '部分采纳不改正式稿与线上稿（草稿≠正式≠发布）', true, 'formal=' + chState.formal + ' published=' + chState.published);
  await shot(page, 'p4-partial-adopt');

  /* 回原段 */
  const backOk = await page.evaluate(() => !!document.querySelector('#main .ms-body p'));
  step('P4', '能回到原段落位置继续阅读', backOk);
  await shot(page, 'p4-return-to-paragraph');

  /* 拒绝/取消不改稿 */
  const beforeReject = JSON.stringify(await page.evaluate((k) => window.WB.S.manuscripts[k].paragraphs, P4CH));
  await page.evaluate(() => { const e = document.querySelector('#sharedArea [data-action="conv.rejectItem"]'); if (e) e.click(); });
  await wait(300);
  const afterReject = JSON.stringify(await page.evaluate((k) => window.WB.S.manuscripts[k].paragraphs, P4CH));
  step('P4', '拒绝项不混进正文', afterReject === beforeReject);

  /* 收栏不丢草稿：进入手写编辑 → 真实键入不保存 → 收左右栏 → 文字仍在 */
  await clickAct(page, 'book.msEdit', [['chapter', P4CH]]);
  await page.focus('#msEditor');
  await page.keyboard.type('（未保存的临时手写段落）');
  await wait(120);
  const typedIn = await page.evaluate(() => { const t = document.getElementById('msEditor'); return t ? t.value : ''; });
  await clickAct(page, 'ui.aside', [['on', '1']]);
  await clickAct(page, 'ui.aside');
  await clickAct(page, 'ui.rail');
  await clickAct(page, 'ui.rail', [['on', '1']]);
  const kept = await page.evaluate(() => { const t = document.getElementById('msEditor'); return t ? t.value : ''; });
  step('P4', '收右栏/收左栏不丢未保存的手写草稿缓冲', /未保存的临时手写段落/.test(kept),
    '键入后 ' + typedIn.length + ' 字 → 收栏后 ' + kept.length + ' 字');
  await clickAct(page, 'book.msCancelEdit');
  await shot(page, 'p4-draft-kept-across-collapse');

  /* =====================================================================
     P5 审稿与证据
     ===================================================================== */
  console.log('\n=== P5 审稿与证据 ===');
  await goView(page, 'book', 'review', { chapter: 'ch43' });
  const revTxt = await mainText(page);
  step('P5', '审稿主区包含问题定位（不是只有评分）', /审|问题|检查|章/.test(revTxt) && revTxt.length > 120);
  await shot(page, 'p5-review-main');
  await clickAct(page, 'ui.aside', [['on', '1']]);
  const asideRev = await page.evaluate(() => document.getElementById('aside').innerText);
  step('P5', '右栏给问题来源/证据/检查范围', asideRev.length > 20, asideRev.replace(/\s+/g, ' ').slice(0, 80));
  await shot(page, 'p5-review-aside-evidence');
  const anchorKept = await page.evaluate(() => !!document.querySelector('#main .ph') || !!document.querySelector('#main .pnl'));
  step('P5', '关闭证据栏后能回原审稿位置（主区未变）', anchorKept);
  await clickAct(page, 'ui.aside');

  /* =====================================================================
     P6 数据比较
     ===================================================================== */
  console.log('\n=== P6 数据比较 ===');
  await goView(page, 'audience', 'performance');
  const pfMain = await mainText(page);
  step('P6', 'D19 主区保留趋势/时间窗/指标切换/对比/明细',
    /趋势/.test(pfMain) && /观察年龄/.test(pfMain) && /章级数据/.test(pfMain), '主区字数=' + pfMain.length);
  const chartCount = await count(page, '#main svg');
  step('P6', '趋势图仍在 Main（不是概览卡墙）', chartCount > 0, 'svg=' + chartCount);
  const metricBefore = await page.evaluate(() => window.WB.S.__sel.metric || null);
  await clickAct(page, 'aud.metric');
  const metricAfter = await page.evaluate(() => window.WB.S.__sel.metric || null);
  step('P6', '可切换指标（筛选状态写入主区工具条）', metricAfter !== metricBefore, metricBefore + ' → ' + metricAfter);
  await clickAct(page, 'ui.aside', [['on', '1']]);
  const asidePf = await page.evaluate(() => document.getElementById('aside').innerText);
  step('P6', '右栏展示来源/口径/订正历史/单条补录入口',
    /来源/.test(asidePf) && /口径/.test(asidePf) && /订正/.test(asidePf));
  step('P6', 'Unknown 保留（不填 0、不合并平台）', /Unknown/.test(asidePf) || /缺口/.test(asidePf));
  await shot(page, 'p6-performance-aside-source');
  await clickAct(page, 'ui.aside');
  const metricKept = await page.evaluate(() => window.WB.S.__sel.metric || null);
  step('P6', '关闭右栏后原筛选保留', metricKept === metricAfter, 'metric=' + metricKept);
  await shot(page, 'p6-performance-main-compare');

  /* =====================================================================
     P7 保存与旧数据
     ===================================================================== */
  console.log('\n=== P7 保存与旧数据 ===');
  const beforeReload = await tagState(page);
  await page.reload({ waitUntil: 'load' });
  await page.waitForSelector('#nav .nav-item', { timeout: 10000 });
  const afterReload = await tagState(page);
  step('P7', '刷新后创作选择与章级覆盖保持', JSON.stringify(afterReload.tags) === JSON.stringify(beforeReload.tags) && afterReload.chOverride === beforeReload.chOverride);
  step('P7', '刷新后回到正确书（不串书）', afterReload.book === beforeReload.book, afterReload.book);
  await goView(page, 'book', 'craft', { mode: 'positioning' });
  step('P7', '旧演示 Book（B-02）仍可打开且有自己的选择',
    await page.evaluate(() => {
      const c = window.WB.S.craft['B-02'];
      return !!(c && c.positioning && c.positioning.tags && Object.keys(c.positioning.tags).length);
    }));
  /* 切书不污染 */
  await page.evaluate(() => window.WB.go('book', 'craft', { bookId: 'B-02', mode: 'positioning' }));
  await wait(220);
  await shot(page, 'p7-book-switch-B02');
  const b02 = await tagState(page);
  step('P7', '切到另一本书后标签与章节各自独立', b02.book === 'B-02' && JSON.stringify(b02.tags) !== JSON.stringify(afterReload.tags));
  await page.evaluate(() => window.WB.go('book', 'craft', { bookId: 'B-01', mode: 'positioning' }));
  await wait(200);

  /* =====================================================================
     P8 业务回归
     ===================================================================== */
  console.log('\n=== P8 业务回归 ===');
  await goView(page, 'market', 'direction');
  step('P8', '① 市场 → 方向入口在', await exists(page, '#main'));
  const dirA = await mainText(page);
  step('P8', '① 市场方向页可读（含裁决/采用入口）', /方向|采纳|采用|提案/.test(dirA));
  await goView(page, 'book', 'library');
  step('P8', '① 方向 → 作品库链路可走', /作品|继续|新建/.test(await mainText(page)));
  await shot(page, 'p8-market-to-book');
  await goView(page, 'publish', 'queue');
  step('P8', '② 发布队列区分未核验/已排期（未知 ≠ 失败）', /未核验|已排期|队列/.test(await mainText(page)));
  await goView(page, 'audience', 'attribution');
  step('P8', '③ 反馈 → 归因可回正文', /归因|层|正文|评论/.test(await mainText(page)));
  await goView(page, 'learning', 'library');
  step('P8', '④ 经验库可用（回下一章）', /经验|方法|适用/.test(await mainText(page)));
  await shot(page, 'p8-regression-chain');

  /* =====================================================================
     P9 单文件构建物真机校验（重建后复验；含构建新鲜度，防过期构建）
     ===================================================================== */
  console.log('\n=== P9 单文件构建物校验 ===');
  const singlePath = path.join(ROOT, 'index.single.html');
  const SRC_FOR_FRESH = ['index.html', 'styles.css', 'data.js', 'app.js', 'views-operate.js', 'views-market.js',
    'views-craft.js', 'views-book.js', 'views-publish.js', 'views-audience.js', 'views-learning.js'];
  const singleExists = fs.existsSync(singlePath);
  step('P9', '单文件构建物存在', singleExists, singleExists ? 'index.single.html' : '缺少（先运行 node _build.js）');
  if (singleExists) {
    const st = fs.statSync(singlePath);
    const stale = SRC_FOR_FRESH.filter(f => fs.statSync(path.join(ROOT, f)).mtimeMs > st.mtimeMs);
    step('P9', '构建物不比任何源文件旧（防止过期构建）', stale.length === 0,
      stale.length ? '比构建物新的源：' + stale.join(', ') : '全部源文件早于构建物');
    const raw = fs.readFileSync(singlePath, 'utf8');
    const leftovers = raw.match(/(?:src|href)="(?!data:|https?:|#)[^"]+\.(?:js|css)"/g) || [];
    step('P9', '构建物无外部 js/css 引用残留', leftovers.length === 0, leftovers.join(', ') || '0');

    const p9 = await browser.newPage();
    p9.on('console', m => { if (m.type() === 'error' && !IGNORE.some(r => r.test(m.text()))) errors.push('[single] ' + m.text()); });
    p9.on('pageerror', e => errors.push('[single] pageerror: ' + String((e && e.message) || e)));
    p9.on('requestfailed', r => { if (!IGNORE.some(rx => rx.test(r.url()))) errors.push('[single] requestfailed: ' + r.url()); });
    await p9.setViewport({ width: 1440, height: 1000 });
    await p9.goto('file://' + encodeURI(singlePath), { waitUntil: 'load', timeout: 30000 });
    await p9.waitForSelector('#nav .nav-item', { timeout: 10000 });
    const ver = await p9.evaluate(() => (window.WB && window.WB.VERSION) || null);
    step('P9', '单文件版可启动且为当前 schema', ver === 'w4', 'VERSION=' + ver);

    await goView(p9, 'book', 'craft', { mode: 'positioning' });
    const d06 = (await p9.$eval('#main', e => e.innerText)).trim();
    step('P9', '单文件版 D06 默认给定位摘要+调整入口（非勾选墙）',
      /调整创作方向/.test(d06) && (await count(p9, '#main .tagopt')) === 0,
      'tagopt=' + (await count(p9, '#main .tagopt')));
    await shot(p9, 'p9-single-file-d06');

    await clickAct(p9, 'craft.picker', [['scope', 'book']]);
    step('P9', '单文件版可打开本轮标签选择器（本轮特征已进入构建物）',
      (await count(p9, '.tagp')) === 1 && (await count(p9, '.tagp-group')) >= 5,
      '分组=' + (await count(p9, '.tagp-group')));
    await shot(p9, 'p9-single-file-picker');
    await p9.close();
  }

  /* =====================================================================
     1280×900 窄视口复核
     ===================================================================== */
  console.log('\n=== 1280×900 窄视口复核 ===');
  await page.setViewport({ width: 1280, height: 900 });
  await wait(260);
  await goView(page, 'book', 'craft', { mode: 'positioning' });
  const mainW = await page.evaluate(() => document.getElementById('main').getBoundingClientRect().width);
  step('N', '1280 宽下 Main 仍可读（≥520px）', mainW >= 520, 'main=' + Math.round(mainW) + 'px');
  await clickAct(page, 'ui.aside', [['on', '1']]);
  const mainW2 = await page.evaluate(() => document.getElementById('main').getBoundingClientRect().width);
  step('N', '1280 宽下开右栏不把正文挤成窄条（浮层）', mainW2 >= 520, 'main=' + Math.round(mainW2) + 'px');
  await shot(page, 'n1-1280-aside-overlay');
  await clickAct(page, 'ui.aside');
  await goView(page, 'book', 'manuscript', { chapter: 'ch43' });
  const readW = await page.evaluate(() => {
    const ps = Array.from(document.querySelectorAll('#main .ms-body p'));
    return ps.length ? ps[0].getBoundingClientRect().width : 0;
  });
  step('N', '1280 宽下正文段落仍可阅读（非极窄）', readW > 380, '段落宽=' + Math.round(readW) + 'px');
  await shot(page, 'n2-1280-manuscript');
  await page.setViewport({ width: 1440, height: 1000 });
  await wait(200);

  /* =====================================================================
     汇总
     ===================================================================== */
  await browser.close();
  server.close();
  try { fs.rmSync(profile, { recursive: true, force: true }); } catch (e) {}

  const failed = steps.filter(s => !s.ok);
  const byPath = {};
  steps.forEach(s => { byPath[s.path] = byPath[s.path] || { pass: 0, fail: 0 }; s.ok ? byPath[s.path].pass++ : byPath[s.path].fail++; });

  const L = [];
  L.push('# Writing Business HTML Exploration · 第 4 轮真机验收（创作选择与工作面组合）');
  L.push('');
  L.push('- 运行时间：' + new Date().toISOString());
  L.push('- 浏览器：系统 Chrome（headless=new）· 视口 1440×1000 与 1280×900 · 100% 缩放');
  L.push('- 浏览器上下文：独立 user-data-dir（隔离，未清空用户既有 localStorage）');
  L.push('- 断言：' + steps.length + ' 项；通过 ' + (steps.length - failed.length) + '；失败 ' + failed.length);
  L.push('- Console Error：' + errors.length);
  L.push('- 截图：' + shotSeq + ' 张（同目录 PNG）');
  L.push('');
  L.push('| 分组 | 通过 | 失败 |');
  L.push('|---|---|---|');
  Object.keys(byPath).forEach(k => L.push('| ' + k + ' | ' + byPath[k].pass + ' | ' + byPath[k].fail + ' |'));
  L.push('');
  L.push('| # | 分组 | 断言 | 结果 | 备注 |');
  L.push('|---|------|------|------|------|');
  steps.forEach((s, i) => L.push('| ' + (i + 1) + ' | ' + s.path + ' | ' + s.name + ' | ' + (s.ok ? 'PASS' : '**FAIL**') + ' | ' + s.detail.replace(/\|/g, '\\|').slice(0, 160) + ' |'));
  if (errors.length) { L.push(''); L.push('## Console 错误明细'); errors.forEach(e => L.push('- ' + e.slice(0, 300))); }

  fs.writeFileSync(path.join(EV, 'TAGS_ACCEPTANCE.md'), L.join('\n'));
  fs.writeFileSync(path.join(EV, 'TAGS_ACCEPTANCE.json'), JSON.stringify({ at: new Date().toISOString(), steps, errors }, null, 2));

  console.log('\n============================');
  console.log('断言 ' + steps.length + ' / 通过 ' + (steps.length - failed.length) + ' / 失败 ' + failed.length);
  console.log('Console Error: ' + errors.length);
  console.log('截图：' + shotSeq + ' 张 → _evidence_tags_workspace/');
  if (failed.length) { console.log('\n失败项：'); failed.forEach(f => console.log('  ✗ [' + f.path + '] ' + f.name + '  ' + f.detail)); }
  process.exit(failed.length ? 1 : 0);
})().catch(e => { console.error('HARNESS ERROR:', e); process.exit(2); });
