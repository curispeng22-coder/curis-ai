const fs = require('fs');
const path = require('path');
const DIR = '/Users/yy/Documents/Curis AI Workspace/curis-ui-prototype';

const files = [
  'finance.html', 'assets.html',
  'workspace-runtime-software.html', 'workspace-runtime-shortvideo.html',
  'workspace-runtime-department.html', 'workspace-shell-reference.html',
];

// A line is a "pure alias declaration line" if, after trimming, it consists
// ONLY of `--name: var(--ui-...)` or `--name: var(--ui-..., #fallback)` segments
// separated by `;` or whitespace.
const pureAliasLine = /^\s*(--[a-zA-Z0-9-]+:\s*var\(--(ui|color)-[a-zA-Z0-9-]+\)(,\s*#[0-9a-fA-F]+)?\s*;?\s*)+\s*$/;

let report = [];
for (const f of files) {
  const fp = path.join(DIR, f);
  const lines = fs.readFileSync(fp, 'utf8').split('\n');
  const before = lines.length;
  const kept = lines.filter(l => !pureAliasLine.test(l));
  const removed = before - kept.length;
  fs.writeFileSync(fp, kept.join('\n'));
  report.push({ file: f, pureAliasLinesRemoved: removed });
}
console.log(JSON.stringify(report, null, 2));
