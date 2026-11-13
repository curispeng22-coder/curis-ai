/* ============================================================
   _build.js — 把 CSS + JS 全部内联进单个 HTML 文件。
   读取 index.html 的 <body> 骨架（不重复书写），剥离外部引用，
   注入 tokens.css + styles.css + data.js + app.js + pages.js。
   零外部引用（无 CDN / 无 web 字体 / 无远程图片）。
   ============================================================ */
const fs = require("fs");
const path = require("path");
const dir = __dirname;

// 读取 index.html，抽取 <body> 骨架
const raw = fs.readFileSync(path.join(dir, "index.html"), "utf8");
const bodyMatch = raw.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
let body = bodyMatch ? bodyMatch[1] : "";

// 剥离外部引用（保留骨架 DOM）
body = body.replace(/<link[^>]*href="styles\.css"[^>]*>/gi, "");
body = body.replace(/<script[^>]*src="(?:data|app|pages)\.js"[^>]*>\s*<\/script>/gi, "");
body = body.replace(/<script>\s*if \(window\.MU && MU\.init\) MU\.init\(\);\s*<\/script>/i, "");

// 组装 CSS（tokens 在前，styles 在后；去掉 @import）
const tokens = fs.readFileSync(path.join(dir, "tokens.css"), "utf8");
let css = fs.readFileSync(path.join(dir, "styles.css"), "utf8").replace(/@import[^;]+;/g, "");
const cssAll = tokens + "\n/* ===== styles.css ===== */\n" + css;

// 组装 JS（escape 内部 </script>）
const jsFiles = ["data.js", "app.js", "pages.js"];
const js = jsFiles
  .map(function (f) { return "/* ===== " + f + " ===== */\n" + fs.readFileSync(path.join(dir, f), "utf8"); })
  .join("\n\n");
const escape = function (s) { return s.replace(/<\/script>/g, "<\\/script>"); };

const html =
  '<!doctype html>\n' +
  '<html lang="zh-CN" data-theme="dark">\n' +
  "<head>\n" +
  '<meta charset="utf-8" />\n' +
  '<meta name="viewport" content="width=device-width, initial-scale=1" />\n' +
  "<title>Curis · AI 音乐经营工作区（视觉探索）</title>\n" +
  "<style>\n" + cssAll + "\n</style>\n" +
  "</head>\n" +
  "<body>" + body + "\n" +
  "<script>\n" + escape(js) + "\n</script>\n" +
  "<script>if(window.MU&&MU.init)MU.init();<\/script>\n" +
  "</body>\n</html>\n";

fs.writeFileSync(path.join(dir, "Music Workspace.html"), html, "utf8");
console.log("✓ Built Music Workspace.html  (" + (html.length / 1024).toFixed(1) + " KB, " + html.length + " bytes)");
