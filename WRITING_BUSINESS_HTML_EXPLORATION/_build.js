/* CURIS — Writing Business HTML Exploration · 单文件构建
   把 styles.css 与全部 JS 内联进一个 HTML，便于分发与评审。
   ⚠ 生成物 `index.single.html` 禁止手改；改源码后重新运行本脚本。
   运行：node _build.js                                             */
'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('node:crypto');

const ROOT = __dirname;
const OUT = path.join(ROOT, 'index.single.html');

const css = fs.readFileSync(path.join(ROOT, 'styles.css'), 'utf8');
let html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');

// Refresh only resources whose contents changed; browser cache must not hide a revision.
html=html.replace(/(src|href)="([\w-]+\.(?:js|css))(?:\?v=[^"]+)?"/g, function(_,attr,file){return attr+'="'+file+'?v='+crypto.createHash('sha256').update(fs.readFileSync(path.join(ROOT,file))).digest('hex').slice(0,10)+'"';});
fs.writeFileSync(path.join(ROOT,'index.html'),html);
const before = html.length;

/* 1) 内联样式表 */
html = html.replace(/<link rel="stylesheet" href="styles\.css(?:\?v=[^" ]+)?" \/>/,
  '<style>\n' + css + '\n</style>');

/* 2) 依原顺序内联脚本，并校验替换数量 */
const jsFiles = ['data.js', 'app.js', 'views-operate.js', 'views-market.js', 'views-craft.js', 'views-book.js',
  'views-publish.js', 'views-audience.js', 'views-learning.js', 'views-flow.js', 'views-reflection.js', 'views-journey.js'];
let inlined = 0;
jsFiles.forEach(function (f) {
  const tag = (html.match(new RegExp('<script src="'+f.replace('.', '\\.')+'(?:\\?v=[^"]+)?"></script>'))||[])[0];
  if (!tag || html.indexOf(tag) < 0) throw new Error('构建失败：未找到脚本标签 ' + tag);
  const code = fs.readFileSync(path.join(ROOT, f), 'utf8');
  html = html.replace(tag, '<script>\n/* ===== ' + f + ' ===== */\n' + code + '\n</script>');
  inlined++;
});

/* 3) 自检：不得残留任何外部引用 */
const leftovers = html.match(/(?:src|href)="(?!data:|https?:|#)[^"]+\.(?:js|css)"/g);
if (leftovers) throw new Error('构建失败：仍存在外部引用 ' + leftovers.join(', '));
if (html.indexOf('</html>') < 0) throw new Error('构建失败：HTML 结构不完整');

fs.writeFileSync(OUT, html);

console.log('=== 单文件构建 ===');
console.log('内联脚本：' + inlined + ' 个');
console.log('原始大小：' + (before / 1024).toFixed(1) + ' KB');
console.log('输出：' + path.basename(OUT) + '（' + (html.length / 1024).toFixed(1) + ' KB）');
console.log('外部引用残留：0');
