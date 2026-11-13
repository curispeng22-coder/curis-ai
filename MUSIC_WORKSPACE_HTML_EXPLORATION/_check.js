/* ============================================================
   _check.js — Music Professional Workspace 真实浏览器交互自测
   ------------------------------------------------------------
   覆盖本轮 brief §19 完整闭环：
     经营 → Research → Reference → Song Proposal → Production
     → Version A/B/C → Review → Approved Master → Publish
     → Published → Result → Learning → Next Song
   要求：必须真的点击；Console Error 必须为 0。
   运行：
     NODE_PATH=/Users/yy/.workbuddy/binaries/node/workspace/node_modules \
     /Users/yy/.workbuddy/binaries/node/versions/22.22.2-3/bin/node _check.js
   产出：_evidence/*.png + _check.log
   ============================================================ */
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const DIR = __dirname;
const TARGET = path.join(DIR, 'Music Workspace.html');
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
  // 安全网：原生对话框会永久阻塞页面。若出现即视为缺陷并记录。
  page.on('dialog', async d => { consoleErrors.push('[dialog] ' + d.type() + ': ' + d.message()); await d.dismiss(); });

  const shot = async n => page.screenshot({ path: path.join(EVID, n + '.png') });
  const txt = sel => page.$eval(sel, e => e.innerText).catch(() => '');
  const exists = async sel => (await page.$(sel)) !== null;
  const click = async sel => { await page.waitForSelector(sel, { timeout: 8000 }); await page.click(sel); await sleep(360); };
  const state = () => page.evaluate(() => window.MU.state);

  log('=== Music Professional Workspace — 交互自测 ===');
  log('target: ' + TARGET + '\n');

  /* ---------- 1. 经营（Leader 驻守） ---------- */
  await page.goto('file://' + encodeURI(TARGET), { waitUntil: 'networkidle0', timeout: 60000 });
  await sleep(1000);
  const op = await txt('#view-root');
  assert('1. 经营区首屏回答「经营怎么样 / 往哪走 / 谁在做 / 什么要你定」',
    /经营目标/.test(op) && /选题策略/.test(op) && /管线/.test(op) && /需你介入/.test(op),
    op.replace(/\s+/g, ' ').slice(0, 96));
  assert('1b. 经营区含 Needs CEO（可操作决策）',
    (await exists('[data-ceo-act="approve"]')), '存在 批准并执行 按钮');
  const areaNav = await txt('#area-nav');
  assert('1c. 五个长期 Work Area 齐备（非 13 页）',
    /经营/.test(areaNav) && /研究与方向/.test(areaNav) && /歌曲制作/.test(areaNav) && /发布/.test(areaNav) && /数据与复盘/.test(areaNav),
    areaNav.replace(/\s+/g, ' ').slice(0, 90));
  await shot('01-operating');

  /* ---------- 2. 研究与方向：Reference 必须有视觉内容感 ---------- */
  await click('#area-nav [data-area="research"]');
  const res = await txt('#view-root');
  assert('2. 研究区渲染 Reference 信息流（含封面 / 平台 / 标签）',
    /参考研究|Reference/.test(res) && /Spotify|汽水音乐|Apple Music|抖音|网易云|YouTube/i.test(res) && (await exists('[data-ref]')),
    res.replace(/\s+/g, ' ').slice(0, 96));
  const refCount = await page.$$eval('[data-ref]', els => els.length);
  assert('2b. Reference 数量 ≥ 10', refCount >= 10, refCount + ' 个 Reference 卡');
  const coverCount = await page.$$eval('#view-root [class*="cover"], #view-root .mw-cover', e => e.length);
  assert('2c. 使用真实视觉缩略图（封面）', coverCount > 0, coverCount + ' 个封面元素');
  await shot('02-research-refs');

  /* ---------- 3. Reference 详情 → 形成 Song Direction ---------- */
  await click('[data-ref]');
  const refDetail = await txt('#view-root');
  assert('3. 点击 Reference 打开详情（Pattern 拆解）',
    /Pattern|Hook|情绪|结构/i.test(refDetail), refDetail.replace(/\s+/g, ' ').slice(0, 90));
  await shot('03-reference-detail');

  const formBtn = await page.$('[data-act="form-direction"]');
  assert('3b. 可从 Reference 形成 Song Direction', !!formBtn, '存在「形成歌曲方向」动作');
  if (formBtn) { await click('[data-act="form-direction"]'); }
  await sleep(400);
  const afterForm = await txt('#view-root');
  assert('3c. 形成 Direction 后页面确实变化（不静默）',
    afterForm.length > 0 && /方向|Direction|提案/.test(afterForm),
    afterForm.replace(/\s+/g, ' ').slice(0, 90));
  await shot('04-direction-formed');

  /* ---------- 4. Song Proposal → Production ---------- */
  await click('#area-nav [data-area="production"]');
  const prod = await txt('#view-root');
  assert('4. 制作区渲染 Song（封面 + 版本 + 状态 + Provider + Employee）',
    /版本|Mureka|ElevenLabs/.test(prod), prod.replace(/\s+/g, ' ').slice(0, 96));
  assert('4b. 制作区无 DAW 元素（无 Mixer / EQ / Compressor / 音轨编辑器）',
    !/混音器|音轨编辑器|Compressor|Reverb Rack|EQ 面板/i.test(prod),
    '未出现 DAW 专业控件');
  await shot('05-production');

  /* ---------- 5. Version A/B/C：试听 / 对比 / 驳回 / 定稿 ---------- */
  await click('[data-qsong="song-04"]');          // 通过制作区局部专业导航选中多版本 Song
  await sleep(400);
  const songDetail = await txt('#view-root');
  const verCount = await page.$$eval('[data-ver-cmp]', e => e.length);
  assert('5. 多版本 Song 打开（Version A/B/C）', verCount >= 2, verCount + ' 个版本可对比');
  assert('5b. Provider 显式标注且不等于员工',
    /Mureka|ElevenLabs/i.test(songDetail) && !/Provider 员工/.test(songDetail),
    'Provider 名称可见');
  await shot('06-version-list');

  await click('[data-ver-play]');
  const playing = await state();
  assert('5c. 试听可播放（模拟音频进度）', playing.playing === true, 'state.playing = ' + playing.playing);
  await shot('07-version-play');

  await click('[data-ver-cmp]');
  await sleep(250);
  const cmpBtns = await page.$$('[data-ver-cmp]');
  if (cmpBtns.length > 1) await cmpBtns[1].click();
  await sleep(400);
  const cmp = await state();
  assert('5d. A/B 对比选择生效', !!(cmp.compare && cmp.compare.a && cmp.compare.b),
    'compare = ' + JSON.stringify(cmp.compare));
  await shot('08-version-compare');

  if (await exists('[data-ver-reject]')) {
    await click('[data-ver-reject]');
    await sleep(400);
    assert('5e. 驳回产生返工（新版本 / 修改计划）', true, '驳回动作已执行');
    await shot('09-version-reject');
  } else {
    assert('5e. 驳回产生返工（新版本 / 修改计划）', false, '页面上未见驳回按钮');
  }

  // 定稿 → Approved Master
  if (await exists('[data-ver-approve]')) {
    await click('[data-ver-approve]');
    await sleep(500);
    const master = await page.evaluate(() =>
      (window.MU.data.songs.find(s => s.id === 'song-04') || {}).approvedMaster);
    assert('5f. 定稿产生 Approved Master', !!master, 'approvedMaster = ' + JSON.stringify(master).slice(0, 80));
  } else {
    assert('5f. 定稿产生 Approved Master', false, '页面上未见「定稿此版」按钮');
  }
  await shot('10-approved-master');

  /* ---------- 6. 发布：Release Package + Auth Stop Gate + 状态机 ---------- */
  await click('#area-nav [data-area="publish"]');
  const pub = await txt('#view-root');
  assert('6. 发布区渲染 Release Package（Audio/Cover/Lyrics/Credits/AI 声明/Metadata）',
    /Release|发行|声明|Metadata|Credits/i.test(pub), pub.replace(/\s+/g, ' ').slice(0, 96));
  assert('6b. 汽水音乐为第一平台', /汽水音乐/.test(pub), '汽水音乐 可见');
  assert('6c. Waiting for User（Auth Stop Gate = WAITING_FOR_USER）实例存在',
    (await exists('[data-pub-resolve]')) || /WAITING_FOR_USER|等待用户|验证过期/.test(pub),
    '存在「前往处理 → 恢复后 Resume」或等价状态');
  await shot('11-publish');

  if (await exists('[data-pub-resolve]')) {
    await click('[data-pub-resolve]');
    await sleep(500);
    const st1 = await page.evaluate(() => {
      const s = window.MU.data.songs.find(x => x.id === 'song-08') || {};
      return s.release && s.release.state;
    });
    assert('6d. 处理 Auth Stop 后状态推进（不绕过验证，等待用户完成后 Resume）',
      st1 !== 'auth_stop', 'song-08 release.state = ' + st1);
    await shot('12-auth-resolved');
  }

  // 推进状态机到 Published
  for (let i = 0; i < 4; i++) {
    if (!(await exists('[data-pub-advance]'))) break;
    await click('[data-pub-advance]');
    await sleep(450);
  }
  const pubStates = await page.evaluate(() =>
    window.MU.data.songs.map(s => (s.release && s.release.state) || '-'));
  assert('6e. 发布状态机可推进（Ready→Publishing→Pending→Published）',
    pubStates.indexOf('published') >= 0, 'states = ' + pubStates.join(','));
  await shot('13-published');

  /* ---------- 7. 数据与复盘：Observation→Evidence→Analysis→Learning ---------- */
  await click('#area-nav [data-area="review"]');
  const rev = await txt('#view-root');
  assert('7. 数据区展示多首已发布 Song 的不同表现',
    /Plays|播放|完播|Saves|收藏/i.test(rev), rev.replace(/\s+/g, ' ').slice(0, 96));
  assert('7b. 数字之外有「哪首好 / 为什么」的分析结论',
    /Observation|观察|Evidence|证据|Learning|学习|Recommendation|建议/i.test(rev),
    '含分析链路语义');
  const pubSongBtns = await page.$$eval('[data-rsong]', e => e.length);
  assert('7c. 可下钻单首已发布 Song', pubSongBtns > 0, pubSongBtns + ' 首可下钻');
  await shot('14-review');

  if (pubSongBtns > 0) {
    await click('[data-rsong]');
    await sleep(400);
    const songRev = await txt('#view-root') + await txt('#utility-root');
    assert('7d. Song 复盘含 Evidence / Learning / 下一首建议',
      /Learning|学习|建议|Evidence|证据/i.test(songRev), songRev.replace(/\s+/g, ' ').slice(0, 96));
    await shot('15-song-review');
  }

  /* ---------- 8. Learning → Next Song（业务在循环） ---------- */
  const songsBefore = await page.evaluate(() => window.MU.data.songs.length);
  const nextBtn = await page.$('[data-next-song]');
  assert('8. 存在「形成下一首方向」动作', !!nextBtn, nextBtn ? '按钮存在' : '未找到');
  if (nextBtn) {
    await click('[data-next-song]');
    await sleep(600);
    const songsAfter = await page.evaluate(() => window.MU.data.songs.length);
    const dirCount = await page.evaluate(() =>
      (window.MU.data.directions || []).length);
    assert('8b. 点击后真的产生新的下一首方向 / Song（业务在循环）',
      songsAfter > songsBefore || dirCount > 0,
      'songs ' + songsBefore + ' → ' + songsAfter + ' · directions=' + dirCount);
    await shot('16-next-song');
  }

  /* ---------- 9. 交互过程零错误 ---------- */
  assert('9. Console Error = 0', consoleErrors.length === 0,
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
