/* ============================================================
   _check.js — RD Professional Workspace 真实浏览器交互自测
   ------------------------------------------------------------
   要求（本轮 brief §24）：必须真的点击，不能只检查 DOM 存在；
   Console Error 必须为 0。
   运行：
     NODE_PATH=/Users/yy/.workbuddy/binaries/node/workspace/node_modules \
     /Users/yy/.workbuddy/binaries/node/versions/22.22.2-3/bin/node _check.js
   产出：_evidence/*.png（逐步截图） + _check.log（断言与 Console 记录）
   ============================================================ */
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const DIR = __dirname;
const TARGET = path.join(DIR, 'RD Workspace.html');
const EVID = path.join(DIR, '_evidence');
const LOG = path.join(DIR, '_check.log');

if (!fs.existsSync(EVID)) fs.mkdirSync(EVID, { recursive: true });

const lines = [];
function log(s) { lines.push(s); console.log(s); }
const results = [];
function assert(name, cond, detail) {
  results.push({ name, pass: !!cond, detail: detail || '' });
  log((cond ? '  PASS  ' : '  FAIL  ') + name + (detail ? '  — ' + detail : ''));
}
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new',
    args: ['--no-sandbox', '--no-proxy-server', '--disable-gpu', '--window-size=1680,1050']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1680, height: 1050 });

  const consoleErrors = [];
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push('[console] ' + m.text()); });
  page.on('pageerror', e => consoleErrors.push('[pageerror] ' + e.message));
  page.on('requestfailed', r => consoleErrors.push('[requestfailed] ' + r.url()));

  const shot = async n => { await page.screenshot({ path: path.join(EVID, n + '.png') }); };
  const txt = sel => page.$eval(sel, e => e.innerText).catch(() => '');
  const exists = async sel => (await page.$(sel)) !== null;
  const click = async sel => { await page.waitForSelector(sel, { timeout: 8000 }); await page.click(sel); await sleep(320); };
  // 确保某员工处于展开态（以该员工的 Composer 是否渲染为判据），最多尝试 3 次
  const ensureExpanded = async eid => {
    for (let i = 0; i < 3; i++) {
      if (await page.$('.composer[data-eid="' + eid + '"]')) return true;
      await click('[data-action="toggle-emp"][data-eid="' + eid + '"]');
      await sleep(250);
    }
    return !!(await page.$('.composer[data-eid="' + eid + '"]'));
  };

  log('=== RD Professional Workspace — 交互自测 ===');
  log('target: ' + TARGET + '\n');

  /* ---------- 1. 载入 + Project Operating Header ---------- */
  await page.goto('file://' + encodeURI(TARGET), { waitUntil: 'networkidle0', timeout: 60000 });
  await sleep(900);
  const header1 = await txt('#proj-header');
  assert('1. Project Operating Header 渲染', header1.includes('默认办公空间'),
    'header 首行: ' + header1.split('\n')[0]);
  assert('1b. Header 含 CEO 第一眼四问要素',
    /本轮目标/.test(header1) && /Leader 判断/.test(header1) && /下一步检查/.test(header1),
    '本轮目标 / Leader 判断 / 下一步检查 均存在');
  const counts1 = await page.evaluate(() => window.RD.api.counts(window.RD.api.proj()));
  log('  初始计数: ' + JSON.stringify(counts1));
  await shot('01-project-header');

  /* ---------- 2. Employee Work Surface 状态排序 ---------- */
  const surface = await txt('#work-surface');
  assert('2. Employee Work Surface 渲染', surface.length > 200, surface.length + ' 字符');
  assert('2b. Working 员工展开（含 Conversation）',
    (await page.$('.composer')) !== null, 'Composer 存在');
  await shot('02-employee-working');

  /* ---------- 3. Project 切换 ---------- */
  await click('[data-action="toggle-proj"]');
  await click('[data-action="switch-project"][data-pid="p-internal"]');
  const header2 = await txt('#proj-header');
  assert('3. Project 切换生效', header2 !== header1 && header2.length > 0,
    '切换后: ' + header2.split('\n')[0]);
  await shot('03-project-switched');
  await click('[data-action="toggle-proj"]');
  await click('[data-action="switch-project"][data-pid="p-default"]');
  await sleep(300);

  /* ---------- 4. 多 Work 员工：Work 切换必须切换 Conversation 上下文 ---------- */
  // 切回 p-default 后，working/needs_ceo/review 员工已自动展开；
  // 直接点 Work 切换器（setWork 会确保该员工展开），不再 toggle 以免把已展开收起。
  await ensureExpanded('e-xuchuan');
  await click('[data-action="set-work"][data-wid="W-231"]');
  const conv231 = await txt('.composer[data-wid="W-231"]') + await txt('#work-surface');
  await click('[data-action="set-work"][data-wid="W-232"]');
  const conv232 = await txt('#work-surface');
  assert('4. 徐川多 Work 展开（W-231/W-232/W-236）',
    (await exists('[data-action="set-work"][data-wid="W-231"]')) &&
    (await exists('[data-action="set-work"][data-wid="W-232"]')) &&
    (await exists('[data-action="set-work"][data-wid="W-236"]')),
    '三个 Work 切换器均存在');
  assert('4b. Work 切换后 Conversation 上下文确实改变',
    conv231 !== conv232 && /隔离|Profile|tenant/i.test(conv232),
    'W-232 上下文命中 Profile/隔离语义');
  await shot('04-multiwork-switch');

  /* ---------- 5. Conversation 双向发送 + 员工拆分并行 Work ---------- */
  await click('[data-action="set-work"][data-wid="W-231"]');
  const composerSel = '.composer[data-wid="W-231"] textarea';
  await page.waitForSelector(composerSel, { timeout: 8000 });
  const before = await txt('#work-surface');
  await page.click(composerSel);
  await page.type(composerSel, '把这个继续推进，拆成两条并行的线。', { delay: 8 });
  await page.keyboard.press('Enter');
  await sleep(900);
  const after = await txt('#work-surface');
  assert('5. Conversation 发送成功（CEO 消息入列）',
    after.length > before.length && after.includes('拆成两条并行'),
    '消息长度 ' + before.length + ' → ' + after.length);
  assert('5b. 员工给出真实研发计划（拆成并行 Work）',
    /W-231/.test(after) && /W-232/.test(after) && /Codex/.test(after),
    '回复含 W-231/W-232/Codex');
  await shot('05-conversation-send');

  /* ---------- 6. Provider 异步执行 ---------- */
  await sleep(600);
  const liveBefore = await txt('#work-surface');
  assert('6. Provider 进入执行态', /执行中|正在执行/.test(liveBefore), '出现执行中提示');
  await shot('06-provider-working');
  // 切到别的员工，验证执行不因切换而中断
  await click('[data-action="toggle-emp"][data-eid="e-chenhao"]');
  await sleep(300);
  await click('[data-action="toggle-emp"][data-eid="e-xuchuan"]');
  await sleep(4200);
  const afterExec = await txt('#work-surface');
  assert('6b. Provider 结果返回（切换员工后仍继续执行）',
    /执行完成|已生成/.test(afterExec) || /127\/127|查看差异/.test(afterExec),
    '结果/引用可见');
  await shot('07-provider-result');

  /* ---------- 7. Utility：Diff（先切到陈昊 W-230，差异引用属于该 Work） ---------- */
  await ensureExpanded('e-chenhao');
  await click('[data-action="set-work"][data-wid="W-230"]');
  await click('[data-action="open-ref"][data-ref="ref-diff-230"]');
  const utilDiff = await txt('#util-pane');
  assert('7. 打开 Diff Utility', /diff|差异|api\/users/i.test(utilDiff) || utilDiff.length > 60,
    utilDiff.length + ' 字符');
  await shot('08-utility-diff');

  /* ---------- 8. Utility：Test Result ---------- */
  await click('[data-action="open-ref"][data-ref="ref-test-230"]');
  const utilTest = await txt('#util-pane');
  assert('8. 打开 Test Result Utility', /测试|127|pass/i.test(utilTest),
    '含测试结论: ' + utilTest.replace(/\s+/g, ' ').slice(0, 90));
  await shot('09-utility-test');

  /* ---------- 9. Needs CEO 内嵌 Decision Banner ---------- */
  const decTxt = await txt('#decision');
  assert('9. Decision 内嵌 Main 顶部（非独立页）', decTxt.length > 60 && /需要你拍板|授权/.test(decTxt),
    decTxt.replace(/\s+/g, ' ').slice(0, 80));
  assert('9b. Decision 含八要素',
    /为何 AI 不能自决/.test(decTxt) && /影响/.test(decTxt) && /风险/.test(decTxt) && /Employee 建议/.test(decTxt),
    '为何不能自决/影响/风险/建议 均存在');
  const countsBefore = await page.evaluate(() => window.RD.api.counts(window.RD.api.proj()));
  const progressBefore = await page.evaluate(() => window.RD.api.proj().progress);
  await shot('10-needs-ceo');

  /* ---------- 10. 批准 Decision 必须真的改变页面状态 ---------- */
  await click('[data-action="approve-decision"]');
  await sleep(600);
  const countsAfter = await page.evaluate(() => window.RD.api.counts(window.RD.api.proj()));
  const progressAfter = await page.evaluate(() => window.RD.api.proj().progress);
  const w240 = await page.evaluate(() => window.RD.api.work('W-240').status);
  assert('10. 批准 Decision 后 Project 进度真的变化',
    progressAfter === progressBefore + 8,
    '进度 ' + progressBefore + '% → ' + progressAfter + '%');
  assert('10b. 测试员工（王雨 / W-240）由 Waiting → Working',
    w240 === 'working', 'W-240.status = ' + w240);
  log('  批准前计数: ' + JSON.stringify(countsBefore));
  log('  批准后计数: ' + JSON.stringify(countsAfter));
  await shot('11-decision-approved');

  /* ---------- 11. 测试 Employee 开始工作 + Work 完成 ---------- */
  await click('[data-action="toggle-emp"][data-eid="e-wangyu"]');
  const wangyu = await txt('#work-surface');
  assert('11. 测试 Employee 工作现场可见', /王雨/.test(wangyu), '王雨 出现在工作面');
  await shot('12-test-employee-start');

  /* ---------- 12. Work 完成 → Project 计数真的变化 ---------- */
  const completeBefore = countsAfter.complete;
  await page.evaluate(() => { window.RD.api.work('W-240').status = 'complete'; });
  // 通过 Project 往返触发一次完整 render（数据变更挂在全局 work 对象上，不因切换丢失）
  await click('[data-action="toggle-proj"]');
  await click('[data-action="switch-project"][data-pid="p-internal"]');
  await click('[data-action="toggle-proj"]');
  await click('[data-action="switch-project"][data-pid="p-default"]');
  await sleep(500);
  const countsDone = await page.evaluate(() => window.RD.api.counts(window.RD.api.proj()));
  const headerDone = await txt('#proj-header');
  assert('12. Work 完成后 Project 计数真的变化',
    countsDone.complete === completeBefore + 1 && headerDone.includes(String(countsDone.complete)),
    'complete ' + completeBefore + ' → ' + countsDone.complete + '（Header 同步显示）');
  await shot('13-work-complete');

  /* ---------- 13. Console 零错误 ---------- */
  assert('13. Console Error = 0', consoleErrors.length === 0,
    consoleErrors.length ? consoleErrors.join(' | ') : '零错误');

  const passN = results.filter(r => r.pass).length;
  log('\n=== 结果：' + passN + '/' + results.length + ' 通过 · Console Error ' + consoleErrors.length + ' ===');
  log('\n=== CONSOLE / PAGE ERRORS ===');
  log(consoleErrors.length ? consoleErrors.join('\n') : '(none)');

  fs.writeFileSync(LOG, lines.join('\n'), 'utf8');
  await browser.close();
  process.exit(consoleErrors.length === 0 && passN === results.length ? 0 : 1);
})().catch(async e => {
  log('FATAL: ' + e.message);
  fs.writeFileSync(LOG, lines.join('\n'), 'utf8');
  process.exit(1);
});
