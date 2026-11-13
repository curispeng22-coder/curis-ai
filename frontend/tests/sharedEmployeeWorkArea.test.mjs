import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";

const component = fs.readFileSync(new URL("../components/workspace/SharedEmployeeWorkArea.js", import.meta.url), "utf8");
const api = fs.readFileSync(new URL("../lib/sharedWorkspaceApi.js", import.meta.url), "utf8");

test("Shared Employee Work Area preserves Employee, execution and UI-state boundaries", () => {
  assert.match(component, /item\.ui_status\?\.code === "working"/);
  assert.match(component, /employee\.current_execution \|\| employee\.current_responsibilities/);
  assert.match(component, /onOpenEmployee\?\.\(employee\.employee_ref\)/);
  assert.match(component, /aria-expanded=\{open\}/);
  assert.doesNotMatch(component, /set.*Runtime|transition|HANDOFF|DECISION_PACKET/);
});

test("Composer stays capability-backed and disabled without a real send handler", () => {
  assert.match(component, /typeof onSend === "function"/);
  assert.match(component, /item\.status === "AVAILABLE"/);
  assert.match(component, /effective_state.*UNKNOWN/);
  assert.match(component, /当前员工尚未接入可验证的指令发送/);
  assert.doesNotMatch(component, /OpenAI|Anthropic|DeepSeek|Codex/);
});

test("Employee Detail and Result Utility remain separate from Conversation", () => {
  assert.match(component, /export function SharedEmployeeDetail/);
  assert.match(component, /组织关系/);
  assert.match(component, /长期责任/);
  assert.match(component, /最近结果/);
  assert.match(component, /export function SharedResultUtility/);
  assert.match(component, /onOpenResult\?\.\(ref\)/);
});

test("Shared API exposes only scoped read routes", () => {
  assert.match(api, /\/shared`/);
  assert.match(api, /\/employees\//);
  assert.match(api, /\/results\//);
  assert.doesNotMatch(api, /method:\s*"POST"|method:\s*"PUT"|method:\s*"DELETE"/);
});
