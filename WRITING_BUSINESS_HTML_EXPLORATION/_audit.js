/* CURIS — Writing Business 原型 · 静态接线审计（引用集合 − 定义集合 差集）
   目的：找出「HTML 里挂得出的行动」但「JS 里没有对应处理器」的死按钮。
   运行：node _audit.js                                          */
'use strict';
const fs = require('fs');

const FILES = ['index.html', 'app.js', 'views-operate.js', 'views-market.js', 'views-craft.js', 'views-book.js',
  'views-publish.js', 'views-audience.js', 'views-learning.js'];

const SPECIAL = ['close-drawer', 'close-modal', 'nav.area', 'nav.view', 'back'];

function read(f) { return fs.readFileSync(f, 'utf8'); }
function uniq(a) { return [...new Set(a)].sort(); }

/* ---- 定义集合 ---- */
const onHandlers = new Set();   // on[<name>] / WB.on[<name>] =
const actFns = new Set();       // act 对象里的方法名
const dataFns = new Set();      // HTML 中出现的 data-fn 值

FILES.forEach((f) => {
  const t = read(f);
  let m;
  const reOn = /\b(?:WB\.)?on\[\s*'([^']+)'\s*\]\s*=/g;
  while ((m = reOn.exec(t))) onHandlers.add(m[1]);
  const reOn2 = /\b(?:WB\.)?on\[\s*"([^"]+)"\s*\]\s*=/g;
  while ((m = reOn2.exec(t))) onHandlers.add(m[1]);
  const reFn = /data-fn=\\?["']([^"'\\]+)\\?["']/g;
  while ((m = reFn.exec(t))) dataFns.add(m[1]);
});

/* act 对象：取 app.js 中 `act = {` 到匹配收尾之间的 `name: function` */
(function () {
  const t = read('app.js');
  const i = t.indexOf('var act = {');
  if (i < 0) return;
  // 逐字符找到配对的大括号
  let j = t.indexOf('{', i), depth = 0, end = -1;
  for (let k = j; k < t.length; k++) {
    if (t[k] === '{') depth++;
    else if (t[k] === '}') { depth--; if (depth === 0) { end = k; break; } }
  }
  const body = t.slice(j, end);
  const re = /^\s{4}([A-Za-z_$][\w$]*)\s*:\s*function/gm;
  let m; while ((m = re.exec(body))) actFns.add(m[1]);
  const re2 = /^\s{4}([A-Za-z_$][\w$]*)\s*:\s*-\>/gm; // 防御：箭头函数写法
  while ((m = re2.exec(body))) actFns.add(m[1]);
})();

/* 视图文件里的 act 方法：`WB.act.name = function` */
FILES.forEach((f) => {
  const t = read(f);
  const re = /\b(?:WB\.)?act\.([A-Za-z_$][\w$]*)\s*=\s*function/g;
  let m; while ((m = re.exec(t))) actFns.add(m[1]);
});

/* ---- 引用集合：所有 data-action 值（含 HTML 属性与 JS 模板串）---- */
const refs = [];  // {value, file}
FILES.forEach((f) => {
  const t = read(f);
  const re = /data-action=\\?["']([^"'\\]+)\\?["']/g;
  let m;
  while ((m = re.exec(t))) refs.push({ value: m[1], file: f });
});

const used = uniq(refs.map(r => r.value));
const dyn = used.filter(v => v.indexOf('+') >= 0 || v.indexOf('$') >= 0);

/* ---- 差集判定 ---- */
const dead = [];
used.forEach((v) => {
  if (dyn.indexOf(v) >= 0) return;                       // 动态拼接，静态不可判
  if (SPECIAL.indexOf(v) >= 0) return;                   // 内置分支
  if (v.indexOf('act.') === 0) return;                   // 经 act[fn] 分发，另由 data-fn 校验
  if (!onHandlers.has(v)) dead.push(v);
});

/* ---- data-fn → act 方法存在性 ---- */
const missingFns = [...dataFns].filter(f => !actFns.has(f));

/* ---- 可达性：data-fn 之外，还要算 on[] 处理器里直接调用 act.X(...) ---- */
const calledDirectly = new Set();
FILES.forEach((f) => {
  const t = read(f);
  const re = /\b(?:WB\.)?act\.([A-Za-z_$][\w$]*)\s*\(/g;
  let m; while ((m = re.exec(t))) calledDirectly.add(m[1]);
});
const unusedFns = [...actFns].filter(f => !dataFns.has(f) && !calledDirectly.has(f));

console.log('=== Writing Business 原型 · 接线审计 ===');
console.log('data-action 去重值：' + used.length + '（其中动态拼接 ' + dyn.length + '）');
console.log('已注册 on[] 处理器：' + onHandlers.size);
console.log('act 方法：' + actFns.size + '（其中被 on[] 处理器直接调用 ' + calledDirectly.size + '）');
console.log('data-fn 引用：' + dataFns.size);
console.log('');
if (dyn.length) console.log('动态拼接（须运行时校验）：' + dyn.join(' | ') + '\n');
console.log('✗ 无处理器的 data-action：' + dead.length);
dead.forEach(d => console.log('   ' + d));
console.log('');
console.log('✗ data-fn 指向不存在的 act 方法：' + missingFns.length);
missingFns.forEach(d => console.log('   ' + d));
console.log('');
console.log('⚠ 既无 data-fn 入口、也未被任何处理器调用的 act 方法（' + unusedFns.length + '）：');
console.log('   ' + (unusedFns.join(', ') || '（无）'));
process.exit(dead.length || missingFns.length ? 1 : 0);
