import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";

const workspace = fs.readFileSync(new URL("../components/rd/RdWorkspacePhaseTwo.js", import.meta.url), "utf8");
const decision = fs.readFileSync(new URL("../components/rd/RdDecisionPackage.js", import.meta.url), "utf8");
const api = fs.readFileSync(new URL("../lib/runtimeApi.js", import.meta.url), "utf8");

test("high-risk RD Layer 0 cannot directly approve", () => {
  assert.match(decision, /查看方案/);
  assert.match(decision, /暂缓/);
  assert.doesNotMatch(decision, /按建议处理|立即批准|直接执行/);
  assert.match(decision, /layer1ReviewedAt/);
});

test("RD P7 shows provenance and applies a choice through the same Cycle", () => {
  for (const value of ["impact", "risk", "cost", "provenance", "recommendationReason", "continuationPlan"]) {
    assert.match(decision, new RegExp(value));
  }
  assert.match(workspace, /selectedCycle\?\.data\?\.rdDecisionPacketRef/);
  assert.match(workspace, /reviewRDDecision/);
  assert.match(workspace, /chooseRDDecision/);
  assert.match(api, /rd-decision\/review/);
  assert.match(api, /rd-decision\/choose/);
  assert.doesNotMatch(decision, /Handoff|responsibility-handoff/);
});
