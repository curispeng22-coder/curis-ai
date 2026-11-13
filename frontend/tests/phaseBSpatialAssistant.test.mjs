import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const source = (path) => readFileSync(new URL(`../${path}`, import.meta.url), "utf8");

test("floating host uses existing durable Assistant conversation and shared composer", () => {
  const host = source("components/assistant/GlobalAssistant.js");
  assert.match(host, /getCEOAssistantConversation\(runtime.companyId\)/);
  assert.match(host, /sendCEOAssistantMessage\(company/);
  assert.match(host, /<SharedConversation/);
  assert.match(host, /setPointerCapture/);
  assert.match(host, /onPointerMove=\{moveDrag\}/);
  assert.match(host, /assistant.minimizeAssistant/);
  assert.match(host, /clampAssistantPosition/);
  assert.match(host, /data-d0-assistant-anchor/);
  assert.match(source("app/layout.js"), /<GlobalAssistantProvider>\{children\}<\/GlobalAssistantProvider>/);
  assert.doesNotMatch(host, /localStorage|lastSeenEventId|simulation/);
});

test("shared spatial shell reuses pane controls and leaves runtime independent", () => {
  const shell = source("components/terra/TerraShell.js");
  assert.match(shell, /<WorkspacePaneShell/);
  assert.match(shell, /contextAvailable=\{Boolean\(paneContent.contextPane \|\| readingDirectory\)\}/);
  assert.match(shell, /utilityAvailable=\{Boolean\(paneContent.utilityPane\)\}/);
  assert.doesNotMatch(shell, /pauseWork|cancelWork|dismissResult/);
  assert.match(source("components/v1/GeneralWorkspaceOperating.js"), /TerraPaneContent/);
});
