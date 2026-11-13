import { readFileSync, writeFileSync } from 'fs';
const p = '/Users/yy/Library/Application Support/TRAE SOLO CN/ModularData/ai-agent/work-mode-projects/6a647ad4366e497d35ebfdc7/curis-ceo-office/pages/capability-center.html';
let c = readFileSync(p, 'utf-8');

// Remove the accidental data-href from Model card
c = c.replace(` data-href="capability-model-list.html"`, '');

// Place markers around each module card's opening div so we can identify them
c = c.replace(
  `accent-green">\n        <div class="module-card-top">\n          <div class="module-card-icon">`,
  `MARKER_MODEL_CARD`
);
c = c.replace(
  `accent-primary">\n        <div class="module-card-top">\n          <div class="module-card-icon">`,
  `MARKER_SKILL_CARD`
);
c = c.replace(
  `accent-amber">\n        <div class="module-card-top">\n          <div class="module-card-icon">`,
  `MARKER_TOOL_CARD`
);
c = c.replace(
  `accent-purple">\n        <div class="module-card-top">\n          <div class="module-card-icon">`,
  `MARKER_WORKFLOW_CARD`
);

// Now replace href="#" in order (each module card has one href="#")
c = c.replace('href="#"', 'href="capability-model-list.html"');
c = c.replace('href="#"', 'href="capability-skill-list.html"');
c = c.replace('href="#"', 'href="capability-tool-list.html"');
c = c.replace('href="#"', 'href="capability-workflow-list.html"');

// Restore markers
c = c.replace('MARKER_MODEL_CARD', `accent-green">\n        <div class="module-card-top">\n          <div class="module-card-icon">`);
c = c.replace('MARKER_SKILL_CARD', `accent-primary">\n        <div class="module-card-top">\n          <div class="module-card-icon">`);
c = c.replace('MARKER_TOOL_CARD', `accent-amber">\n        <div class="module-card-top">\n          <div class="module-card-icon">`);
c = c.replace('MARKER_WORKFLOW_CARD', `accent-purple">\n        <div class="module-card-top">\n          <div class="module-card-icon">`);

writeFileSync(p, c, 'utf-8');

const remaining = (c.match(/href="#"/g) || []).length;
console.log(`Remaining href="#" in capability-center.html: ${remaining}`);
