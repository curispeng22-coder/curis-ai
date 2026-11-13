import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";

const workspace = fs.readFileSync(new URL("../components/rd/RdWorkspacePhaseTwo.js", import.meta.url), "utf8");
const handoff = fs.readFileSync(new URL("../components/rd/RdResponsibilityHandoff.js", import.meta.url), "utf8");
const api = fs.readFileSync(new URL("../lib/runtimeApi.js", import.meta.url), "utf8");

test("RD keeps Artifact Review separate from a true Responsibility Handoff", () => {
  assert.match(workspace, /createResponsibilityHandoff/);
  assert.match(workspace, /sendResponsibilityHandoff/);
  assert.match(handoff, /artifactReview\?\.status !== "APPROVED"/);
  assert.match(handoff, /代码送审不会转移责任/);
  assert.match(handoff, /Current Executor 仍为 none/);
  assert.match(workspace, /detail\?\.role_slots/);
  assert.doesNotMatch(handoff, /DECISION_PACKET|CEO Decision|自动执行/);
});

test("RD Handoff UI sends one bounded transfer and never impersonates the target response", () => {
  assert.match(api, /createResponsibilityHandoff/);
  assert.match(api, /sendResponsibilityHandoff/);
  assert.match(api, /responsibility-handoff\/send/);
  assert.doesNotMatch(workspace, /respondResponsibilityHandoff/);
  assert.doesNotMatch(handoff, /onRespond|respondResponsibilityHandoff/);
});
