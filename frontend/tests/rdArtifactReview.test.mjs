import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";

const workspace = fs.readFileSync(
  new URL("../components/rd/RdWorkspacePhaseTwo.js", import.meta.url),
  "utf8",
);
const review = fs.readFileSync(
  new URL("../components/rd/RdArtifactReview.js", import.meta.url),
  "utf8",
);
const api = fs.readFileSync(new URL("../lib/runtimeApi.js", import.meta.url), "utf8");

test("RD Artifact Review uses the persisted Cycle request and real reviewer Employee", () => {
  assert.match(workspace, /createArtifactReview/);
  assert.match(workspace, /executeArtifactReview/);
  assert.match(workspace, /artifactReview\.reviewTaskRef/);
  assert.match(workspace, /artifactReview\?\.status === "REVIEWING"/);
  assert.match(review, /reviewerEmployeeRef/);
  assert.match(review, /item\.entity_id !== holderRef/);
  assert.match(review, /当前无人执行/);
  assert.match(review, /原研发负责人继续持有这项责任/);
  assert.doesNotMatch(review, /HANDOFF|DECISION_PACKET|批准方案|CEO Decision/);
});

test("RD review Result Reference opens Utility evidence without fabricating output", () => {
  assert.match(workspace, /artifact_type === "artifact_review"/);
  assert.match(workspace, /审核结果尚未形成；这里不会根据请求状态补造结论/);
  assert.match(workspace, /Review Request/);
  assert.match(workspace, /Reviewer Task/);
  assert.match(workspace, /Codex Session/);
  assert.match(review, /查看审核结果/);
});

test("Runtime API keeps request creation separate from asynchronous reviewer execution", () => {
  assert.match(api, /createArtifactReview/);
  assert.match(api, /artifact-review`/);
  assert.match(api, /executeArtifactReview/);
  assert.match(api, /artifact-review\/execute/);
});
