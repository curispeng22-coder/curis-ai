const fs = require('fs');
const path = require('path');
const PROTO = '/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype';
const FILES = ['workspace-portal.html','ceo-desk.html','founding-flow.html','workspace-studio.html','business.html','operating.html','ai-organization.html'];

const globalClasses = new Set();
const globalLucide = new Set();
const perFile = {};
let twBlocks = [];

for (const f of FILES) {
  const p = path.join(PROTO, f);
  if (!fs.existsSync(p)) { perFile[f] = { missing: true }; continue; }
  const html = fs.readFileSync(p, 'utf8');
  const classes = new Set();
  const lucide = new Set();
  // class="..."
  const classRe = /class="([^"]*)"/g;
  let m;
  while ((m = classRe.exec(html))) {
    m[1].split(/\s+/).forEach(c => { if (c) { classes.add(c); globalClasses.add(c); } });
  }
  // data-lucide="..."
  const lucRe = /data-lucide="([^"]*)"/g;
  while ((m = lucRe.exec(html))) { lucide.add(m[1]); globalLucide.add(m[1]); }
  // <style type="text/tailwindcss">...</style>
  const twRe = /<style type="text\/tailwindcss">([\s\S]*?)<\/style>/g;
  while ((m = twRe.exec(html))) { twBlocks.push({ file: f, len: m[1].length, hasApply: /@apply/.test(m[1]), hasArbitrary: /\[[^\]]+\]/.test(m[1]), sample: m[1].slice(0, 300) }); }
  perFile[f] = { classes: classes.size, lucide: [...lucide] };
}

// Categorize global classes by Tailwind utility prefix
const prefixes = {};
for (const c of globalClasses) {
  const base = c.split('-')[0].split(':').pop();
  prefixes[base] = (prefixes[base] || 0) + 1;
}
const sortedPrefixes = Object.entries(prefixes).sort((a,b)=>b[1]-a[1]);

console.log('=== Per-file ===');
for (const f of FILES) console.log(f, perFile[f].missing ? '(MISSING)' : `classes=${perFile[f].classes} lucideIcons=${perFile[f].lucide.length}`);
console.log('\n=== Global distinct class count ===', globalClasses.size);
console.log('=== Global distinct lucide icons ===', globalLucide.size, [...globalLucide].join(', '));
console.log('\n=== Top class prefixes (utility families) ===');
sortedPrefixes.slice(0, 40).forEach(([k,v]) => console.log(`  ${k}: ${v}`));
console.log('\n=== text/tailwindcss blocks ===');
twBlocks.forEach(b => console.log(`  ${b.file}: len=${b.len} @apply=${b.hasApply} arbitraryVal=${b.hasArbitrary}`));
console.log('\n=== Sample text/tailwindcss block (first file) ===');
if (twBlocks[0]) console.log(twBlocks[0].sample);
