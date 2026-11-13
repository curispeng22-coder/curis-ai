const fs = require('fs');
const path = require('path');

const DIR = '/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype';

// private token -> frozen --ui-* token
const MAP = {
  'bg': 'ui-bg',
  'panel': 'ui-surface',
  'panel2': 'ui-surface-2',
  'surface': 'ui-surface',
  'surface2': 'ui-surface-2',
  'text': 'ui-text',
  'muted': 'ui-text-2',
  'faint': 'ui-text-3',
  'line': 'ui-line',
  'accent': 'ui-accent',
  'accentText': 'ui-action-primary-fg',
  'primary': 'ui-action-primary-bg',
  'primaryText': 'ui-action-primary-fg',
  'primaryFg': 'ui-action-primary-fg',
  'ok': 'ui-success',
  'warn': 'ui-warning',
  'bad': 'ui-danger',
  'bg-base-default': 'ui-bg',
};

// Build replacement: replace var(--token) with var(--ui-*)
const files = [
  'finance.html',
  'assets.html',
  'workspace-runtime-software.html',
  'workspace-runtime-shortvideo.html',
  'workspace-runtime-department.html',
  'workspace-shell-reference.html',
];

const aliasDecl = new RegExp(
  '^\\s*--(' + Object.keys(MAP).join('|') + '):\\s*var\\(--(ui|color)-[a-z0-9-]+\\)\\s*;?\\s*$',
  'gm'
);

let report = [];
for (const f of files) {
  const fp = path.join(DIR, f);
  let html = fs.readFileSync(fp, 'utf8');

  // 1) replace usages var(--token) -> var(--ui-*)
  let replaced = 0;
  for (const [priv, ui] of Object.entries(MAP)) {
    const re = new RegExp('var\\(--' + priv + '\\)', 'g');
    const before = html;
    html = html.split('var(--' + priv + ')').join('var(--' + ui + ')');
    const diff = (before.match(re) || []).length;
    replaced += diff;
  }

  // 2) remove alias-only declaration lines (private token : var(--ui-*);)
  const beforeLines = html.split('\n');
  const afterLines = beforeLines.filter(l => !aliasDecl.test(l));
  const removedLines = beforeLines.length - afterLines.length;
  html = afterLines.join('\n');

  fs.writeFileSync(fp, html);
  report.push({ file: f, usagesReplaced: replaced, aliasDeclLinesRemoved: removedLines });
}

console.log(JSON.stringify(report, null, 2));

// 3) sanity: any leftover private var(--token) usages referencing the MAP keys?
const leftoverRe = new RegExp('var\\(--(' + Object.keys(MAP).join('|') + ')\\)', 'g');
let leftovers = {};
for (const f of files) {
  const fp = path.join(DIR, f);
  const html = fs.readFileSync(fp, 'utf8');
  const m = html.match(leftoverRe);
  if (m) leftovers[f] = m.length;
}
console.log('LEFTOVER private var() usages:', JSON.stringify(leftovers));
