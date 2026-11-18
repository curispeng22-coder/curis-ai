import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";

import { getTeamOperatingDefinition, publishTeamOperatingDefinition } from "../lib/runtimeApi.js";


test("Team Operating API reads a scoped definition without exposing Runtime storage", async () => {
  let path = "";
  await getTeamOperatingDefinition({
    companyId: "company/一", workspaceId: "workspace/一", scopeType: "WORKSPACE",
    scopeRef: "workspace/一", workflowKey: "content-growth",
  }, async (value) => { path = value; return { published: null }; });

  assert.match(path, /team-operating\/definition\?/);
  assert.match(path, /company_id=company%2F%E4%B8%80/);
  assert.match(path, /scope_type=WORKSPACE/);
  assert.equal(/runtime_entities|data_json/.test(path), false);
});

test("Team Operating publish carries UI order and bounded role edits", async () => {
  let captured;
  await publishTeamOperatingDefinition({
    company_id: "company-1", workspace_id: "workspace-1", scope_type: "WORKSPACE",
    scope_ref: "workspace-1", workflow_key: "content-growth",
    default_flow: ["topic", "research"],
    roles: [{
      responsibility_key: "topic", role_name: "选题", employee_ref: "employee-topic",
      responsibility: "负责选题", input_contract: { description: "目标" },
      output_contract: { description: "选题结果", requiresResult: true }, is_leader: false,
    }],
  }, async (path, options) => { captured = { path, options }; return { published: { version: 2 } }; });

  assert.equal(captured.path, "/api/workspace/runtime/foundation/team-operating/definitions/publish");
  assert.equal(captured.options.method, "POST");
  const body = JSON.parse(captured.options.body);
  assert.deepEqual(body.default_flow, ["topic", "research"]);
  assert.equal(body.roles[0].employee_ref, "employee-topic");
  assert.equal(body.roles[0].output_contract.requiresResult, true);
});

test("XHS uses the lightweight product-language editor and reorder controls", () => {
  const editor = fs.readFileSync(new URL("../components/workspace/TeamOperatingDefinitionEditor.js", import.meta.url), "utf8");
  const xhs = fs.readFileSync(new URL("../components/xhs/XhsWorkspacePhaseOne.js", import.meta.url), "utf8");

  assert.match(editor, /团队运转/);
  assert.match(editor, /默认流程/);
  assert.match(editor, /data-role-key=/);
  assert.match(editor, /draggable=/);
  assert.match(editor, /onDragOver=/);
  assert.match(editor, /上移/);
  assert.match(editor, /保存新版本/);
  assert.doesNotMatch(editor, /DAG|State Machine|Runtime Graph/);
  assert.match(xhs, /TeamOperatingDefinitionEditor/);
});

test("only the reviewed Music Business can build a first research publication request", async () => {
  const { createRequire } = await import("node:module");
  const { default: vm } = await import("node:vm");
  const require = createRequire(import.meta.url);
  const swc = require("next/dist/build/swc");
  await swc.loadBindings();
  const text = fs.readFileSync(new URL("../components/workspace/TeamOperatingDefinitionEditor.js", import.meta.url), "utf8");
  const { code } = await swc.transform(text, { filename: "TeamOperatingDefinitionEditor.js", isModule: true,
    jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } },
    module: { type: "commonjs" } });
  const module = { exports: {} };
  vm.runInNewContext(code, { module, exports: module.exports, require: id => id.includes("runtimeApi") ? {} : require(id) });
  const request = module.exports.musicResearchPublishRequest;
  const leader = { assignmentRef: "leader-assignment", roleRef: "leader-role", assignmentRevision: 5,
    employeeRef: "leader", isLeader: true, responsibilityKey: "BUSINESS_LEADER", roleName: "业务负责人", responsibility: "统筹" };
  const review = { company_id: "company", scope: { type: "BUSINESS", ref: "music", workspace_id: null },
    workflow_key: "music-market-research", published: null, can_publish: true, leader,
    available_employees: [{ employee_ref: "researcher" }] };
  let captured;
  await publishTeamOperatingDefinition(request("company", "music", review, "researcher"),
    async (path, options) => { captured = { path, body: JSON.parse(options.body) }; return { published: { version: 1 } }; });
  assert.equal(captured.path, "/api/workspace/runtime/foundation/team-operating/definitions/publish");
  assert.equal(captured.body.scope_type, "BUSINESS");
  assert.equal("workspace_id" in captured.body, false);
  assert.deepEqual(captured.body.music_research, { leader_revision: 5, confirm: true });
  assert.equal(captured.body.roles[0].assignment_ref, "leader-assignment");
  assert.equal(captured.body.roles[1].employee_ref, "researcher");
  for (const invalid of [
    { company_id: "elsewhere" }, { published: { version: 1 } }, { can_publish: false },
    { scope: { ...review.scope, workspace_id: "fake-workspace" } }, { scope: { ...review.scope, ref: "old" } },
  ]) assert.throws(() => request("company", "music", { ...review, ...invalid }, "researcher"), /重新核对/);
  assert.throws(() => request("company", "music", review, "leader"), /重新核对/);
});
