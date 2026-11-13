import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";

const composer = fs.readFileSync(
  new URL("../components/rd/RdRealExecutionComposer.js", import.meta.url),
  "utf8",
);
const professionalWorkspace = fs.readFileSync(
  new URL("../components/rd/RdWorkspacePhaseTwo.js", import.meta.url),
  "utf8",
);
const shell = fs.readFileSync(new URL("../components/workspace/WorkspacePaneShell.js", import.meta.url), "utf8");

test("RD composer creates an automatic bounded execution context", () => {
  assert.match(composer, /getProjects\(workspace\.company_id\)/);
  assert.match(composer, /project_ref:/);
  assert.match(composer, /resource_refs:/);
  assert.match(composer, /test_command:/);
  assert.match(composer, /requested_access_intent: "AUTO_WITHIN_BOUNDARY"/);
  assert.doesNotMatch(composer, /workflow_run:/);
  assert.match(composer, /要解决的问题/);
  assert.match(composer, /执行详情（通常无需修改）/);
  assert.doesNotMatch(composer, />建立研发 Cycle</);
});

test("RD professional Workspace reads real responsibility and result facts", () => {
  for (const contract of [
    "getRuntimeWorkspace",
    "getProject",
    "getTask",
    "responsibilityEmployeeRef",
    "currentExecutorRef",
    "executionStatus",
    "code_change",
    "artifactRefs",
    "evidenceRefs",
    "computerAccess",
    "sessionRef",
  ]) assert.match(professionalWorkspace, new RegExp(contract));
  assert.match(professionalWorkspace, /cycles\.some\(\(item\) => item\.data\?\.executionStatus === "RUNNING"\)/);
  assert.match(professionalWorkspace, /window\.setInterval\(\(\) => load\(true\), 800\)/);
  assert.match(professionalWorkspace, /查看代码变化与测试结果/);
  assert.match(professionalWorkspace, /查看技术状态与内部 ID/);
  assert.match(professionalWorkspace, /当前无法由服务方确认/);
  assert.match(professionalWorkspace, /当前无人执行/);
  assert.doesNotMatch(professionalWorkspace, /Calendar|ContentItem|Note|fixture|mock/i);
});

test("RD Result Reference can open the shared resizable Utility without changing XHS defaults", () => {
  assert.match(professionalWorkspace, /utilityRequestKey/);
  assert.match(professionalWorkspace, /contextLabel="研发上下文"/);
  assert.match(professionalWorkspace, /utilityLabel=/);
  assert.match(shell, /utilityRequestKey > 0/);
  assert.match(shell, /contextLabel = "选题库 · 信号"/);
  assert.match(shell, /utilityLabel = "图文预览"/);
  assert.match(shell, /contextWidth/);
  assert.match(shell, /utilityWidth/);
});
