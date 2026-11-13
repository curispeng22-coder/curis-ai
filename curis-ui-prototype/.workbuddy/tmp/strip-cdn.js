const fs = require('fs');
const path = require('path');
const PROTO = '/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype';
const FILES = ['workspace-portal.html','ceo-desk.html','founding-flow.html','workspace-studio.html','business.html','operating.html','ai-organization.html'];

const REPLACEMENT = `    <style id="legacy-base">
      body { background: var(--background); color: var(--foreground); }
      td, th { overflow-wrap: break-word; word-break: break-all; word-break: auto-phrase; }
      th { white-space: nowrap; }
    </style>`;

let allOk = true;
for (const f of FILES) {
  const p = path.join(PROTO, f);
  if (!fs.existsSync(p)) { console.log(`SKIP ${f} (missing)`); continue; }
  let html = fs.readFileSync(p, 'utf8');

  // 1) remove the two CDN <script> tags (tailwind browser + lucide), incl. surrounding whitespace/newline
  const twRe = /\s*<script src="https:\/\/cdn\.jsdelivr\.net\/npm\/@tailwindcss\/browser@4\.3\.1[^"]*"><\/script>\s*\n/;
  const luRe = /\s*<script src="https:\/\/unpkg\.com\/lucide@1\.8\.0[^"]*"><\/script>\s*\n/;
  const twHit = twRe.test(html);
  const luHit = luRe.test(html);
  html = html.replace(twRe, '').replace(luRe, '');
  if (!twHit) { console.log(`WARN ${f}: tailwind CDN script not found`); allOk = false; }
  if (!luHit) { console.log(`WARN ${f}: lucide CDN script not found`); allOk = false; }

  // 2) replace the <style type="text/tailwindcss"> block (any inner content) with plain CSS equivalent
  const twBlockRe = /<style type="text\/tailwindcss">[\s\S]*?<\/style>/;
  if (!twBlockRe.test(html)) { console.log(`WARN ${f}: text/tailwindcss block not found`); allOk = false; }
  html = html.replace(twBlockRe, REPLACEMENT);

  // 3) sanity: no remaining cdn/unpkg/@tailwindcss/text-tailwindcss references
  const residual = /cdn\.jsdelivr|unpkg\.com|@tailwindcss|text\/tailwindcss/.test(html);
  if (residual) { console.log(`WARN ${f}: residual CDN reference remains`); allOk = false; }

  fs.writeFileSync(p, html);
  console.log(`OK ${f} (tw=${twHit} lucide=${luHit})`);
}
console.log(allOk ? '\nALL FILES PROCESSED CLEAN' : '\nSOME WARNINGS — see above');
