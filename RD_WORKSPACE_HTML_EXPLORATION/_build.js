/* ============================================================
   _build.js — 零依赖 CommonJS 打包脚本
   读取 index.html + styles.css + 所有 JS，内联生成单文件 RD Workspace.html。
   运行：/Users/yy/.workbuddy/binaries/node/versions/22.22.2-3/bin/node _build.js
   输出：RD Workspace.html（所有 CSS/JS/Mock 内联，零外部引用）
   ============================================================ */
const fs = require('fs');
const path = require('path');
const dir = __dirname;

// Frozen 设计令牌必须先于业务样式（styles.css 只消费 var(--ui-*)，不自定义调色板）
const tokens = fs.readFileSync(path.join(dir, 'tokens.css'), 'utf8');
// 去掉 @import（单文件版把 tokens.css 直接内联在 <style> 顶部）
const css = tokens + '\n' + fs.readFileSync(path.join(dir, 'styles.css'), 'utf8').replace(/@import[^;]+;/g, '');

// 所有 JS（顺序敏感：data 先于 app）
const jsFiles = ['data.js', 'app.js'];
const js = jsFiles.map(f => '/* ===== ' + f + ' ===== */\n' + fs.readFileSync(path.join(dir, f), 'utf8')).join('\n\n');

// 读取 index.html，提取 <body> 内部标记（避免重复维护两份结构）
const htmlSrc = fs.readFileSync(path.join(dir, 'index.html'), 'utf8');
const bodyMatch = htmlSrc.match(/<body[^>]*>([\s\S]*)<\/body>/i);
if (!bodyMatch) { console.error('无法提取 body'); process.exit(1); }
let body = bodyMatch[1];
// 去掉外部引用（link / script src），改为内联
body = body.replace(/<link[^>]*href=["']styles\.css["'][^>]*>/gi, '');
body = body.replace(/<script[^>]*src=["'][^"']+["'][^>]*>\s*<\/script>/gi, '');

const escape = s => s.replace(/<\/script>/g, '<\\/script>');

const out = '<!DOCTYPE html>\n' +
  '<html lang="zh-CN" data-theme="dark">\n' +
  '<head>\n' +
  '  <meta charset="utf-8" />\n' +
  '  <meta name="viewport" content="width=device-width, initial-scale=1" />\n' +
  '  <title>RD Professional Workspace — 高保真交互探索（单文件版）</title>\n' +
  '  <style>\n' + css + '\n  </style>\n' +
  '</head>\n' +
  '<body>\n' + body +
  '  <script>\n' + escape(js) + '\n  </script>\n' +
  '</body>\n</html>\n';

fs.writeFileSync(path.join(dir, 'RD Workspace.html'), out, 'utf8');
console.log('built RD Workspace.html, bytes =', out.length);
