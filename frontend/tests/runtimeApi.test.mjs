import assert from "node:assert/strict";
import test from "node:test";

import {
  createRuntimeContentItem,
  createRuntimeCycle,
  createRuntimeSimulation,
  createRuntimeWorkspace,
  decideStaffing,
  closeOperatingCycle,
  executeOperatingCycle,
  executeRuntimeSimulation,
  getCapabilitySupplyReview,
  getStaffingApproval,
  getRuntimeBootstrap,
  reviewCapabilitySupply,
  resumeOperatingCycle,
  reviewOperatingCycle,
  reviewRuntimeSimulation,
  rollbackStaffing,
  runtimeErrorMessage,
  startRuntimeSimulation,
  startOperatingCycle,
  transitionRuntimeEntity,
  workspaceEntryHref,
} from "../lib/runtimeApi.js";


test("empty bootstrap returns no invented company facts", async () => {
  const calls = [];
  const result = await getRuntimeBootstrap(async (path) => {
    calls.push(path);
    return { companies: [] };
  });

  assert.deepEqual(result, { companyId: "", snapshot: null, simulations: [] });
  assert.deepEqual(calls, ["/api/workspace/runtime/foundation/companies"]);
});

test("bootstrap discovers id once then reads company, workspace and simulations from Runtime", async () => {
  const calls = [];
  const request = async (path) => {
    calls.push(path);
    if (path === "/api/workspace/runtime/foundation/companies") return { companies: [{ company_id: "company/a", is_default: true }] };
    if (path.endsWith("/companies/company%2Fa")) {
      return { company: { company_id: "company/a" }, workspaces: [{ workspace_id: "ws/一" }, { workspace_id: "ws-2" }] };
    }
    return { simulations: [{ simulation_run_id: path }] };
  };

  const result = await getRuntimeBootstrap(request);

  assert.equal(result.companyId, "company/a");
  assert.equal(result.simulations.length, 2);
  assert.deepEqual(calls, [
    "/api/workspace/runtime/foundation/companies",
    "/api/workspace/runtime/foundation/companies/company%2Fa",
    "/api/workspace/runtime/foundation/companies/company%2Fa/workspaces/ws%2F%E4%B8%80/simulations",
    "/api/workspace/runtime/foundation/companies/company%2Fa/workspaces/ws-2/simulations",
  ]);
  assert.equal(calls.some((path) => /projects|tasks|home\/summary/.test(path)), false);
});

test("Runtime transition keeps actor and state command in the persisted API", async () => {
  let captured;
  await transitionRuntimeEntity("founding/1", { target: "CLARIFYING", actor: "CEO", trigger: "request_clarification" }, async (path, options) => {
    captured = { path, options };
    return { lifecycle_status: "CLARIFYING" };
  });

  assert.equal(captured.path, "/api/workspace/runtime/foundation/entities/founding%2F1/transition");
  assert.equal(captured.options.method, "POST");
  assert.deepEqual(JSON.parse(captured.options.body), { target: "CLARIFYING", actor: "CEO", trigger: "request_clarification" });
});

test("Workspace Studio creates a Runtime Workspace instead of a legacy Project", async () => {
  let captured;
  await createRuntimeWorkspace("company/a", {
    ceo_id: "selfuse-ceo",
    business_ref: "business-rd",
    business_type: "RD",
    name: "研发工作台",
    blueprint_version: "v1",
    blueprint: { businessType: "RD", stages: ["INTAKE"] },
  }, async (path, options) => {
    captured = { path, options };
    return { workspace: { workspace_id: "workspace/rd", business_type: "RD" } };
  });

  assert.equal(captured.path, "/api/workspace/runtime/foundation/companies/company%2Fa/workspaces");
  assert.equal(captured.options.method, "POST");
  assert.equal(JSON.parse(captured.options.body).business_type, "RD");
});

test("Workspace runtime creates first work items through Runtime APIs", async () => {
  const calls = [];
  const request = async (path, options) => {
    calls.push({ path, options });
    return { entity_id: "runtime-1" };
  };

  await createRuntimeCycle("workspace/rd", {
    ceo_id: "selfuse-ceo",
    owner_ref: "CEO Assistant",
    outcome_ref: "完善 Curis",
    intent_ref: "完善 Curis",
    blueprint_version: "v1",
  }, request);
  await createRuntimeContentItem("workspace/xhs", {
    ceo_id: "selfuse-ceo",
    owner_ref: "CEO Assistant",
    outcome_ref: "验证内容结果",
    intent_ref: "验证内容结果",
    blueprint_version: "v1",
    platform: "XHS",
    platform_variant: "图文",
    payload_ref: "knowledge:brief-1",
    author: "内容 AI",
    constraints_check: "待 CEO 检查",
  }, request);

  assert.equal(calls[0].path, "/api/workspace/runtime/foundation/workspaces/workspace%2Frd/cycles");
  assert.equal(calls[1].path, "/api/workspace/runtime/foundation/workspaces/workspace%2Fxhs/content-items");
  assert.equal(calls.every(({ options }) => options.method === "POST"), true);
});

test("Workspace runtime starts a persisted SimulationRun through the scoped command", async () => {
  const calls = [];
  const request = async (path, options) => {
    calls.push({ path, options });
    return { simulation_run_id: "simulation/1", lifecycle_status: "RUNNING" };
  };

  await createRuntimeSimulation("workspace/rd", {
    ceo_id: "selfuse-ceo",
    subject_id: "cycle/1",
    scenario_id: "RD-001",
    blueprint_version: "v1",
    participants: ["Engineering AI"],
    input_refs: [],
  }, request);
  await startRuntimeSimulation("workspace/rd", "simulation/1", {
    ceo_id: "selfuse-ceo",
    trigger: "ceo_start",
    reason: "开始验证",
  }, request);

  assert.equal(calls[0].path, "/api/workspace/runtime/foundation/workspaces/workspace%2Frd/simulations");
  assert.equal(calls[1].path, "/api/workspace/runtime/foundation/workspaces/workspace%2Frd/simulations/simulation%2F1/transition");
  assert.equal(JSON.parse(calls[1].options.body).target, "RUNNING");
});

test("Workspace runtime keeps execution and CEO review as explicit commands", async () => {
  const calls = [];
  const request = async (path, options) => {
    calls.push({ path, options });
    return { lifecycle_status: "RUNNING" };
  };

  await executeRuntimeSimulation("workspace/rd", "simulation/1", {
    ceo_id: "selfuse-ceo", trigger: "ceo_execute",
  }, request);
  await reviewRuntimeSimulation("workspace/rd", "simulation/1", {
    ceo_id: "selfuse-ceo", decision: "PASS", evidence_refs: ["evidence/1"],
  }, request);

  assert.match(calls[0].path, /simulations\/simulation%2F1\/execute$/);
  assert.equal(JSON.parse(calls[0].options.body).target, "RUNNING");
  assert.match(calls[1].path, /simulations\/simulation%2F1\/review$/);
  assert.equal(JSON.parse(calls[1].options.body).decision, "PASS");
});

test("Capability supply review stays a scoped Resource Check command", async () => {
  const calls = [];
  const request = async (path, options) => {
    calls.push({ path, options });
    return { resourceCheckPassed: false, activationReady: false };
  };

  await getCapabilitySupplyReview("company/一", "workspace/一", request);
  await reviewCapabilitySupply("workspace/一", {
    ceo_id: "selfuse-ceo",
    selections: [{
      requirement_ref: "requirement:test-runner",
      source: "official",
      capability_type: "tool",
      capability_id: "official.test-runner",
    }],
  }, request);

  assert.equal(calls[0].path, "/api/workspace/runtime/foundation/companies/company%2F%E4%B8%80/workspaces/workspace%2F%E4%B8%80/capability-supply-review");
  assert.equal(calls[1].path, "/api/workspace/runtime/foundation/workspaces/workspace%2F%E4%B8%80/capability-supply-review");
  assert.equal(calls[1].options.method, "POST");
  assert.equal(JSON.parse(calls[1].options.body).selections[0].capability_id, "official.test-runner");
});

test("Staffing approval and rollback remain explicit CEO Runtime commands", async () => {
  const calls = [];
  const request = async (path, options) => {
    calls.push({ path, options });
    return { workspaceStatus: "DRAFT", activationReady: true };
  };

  await getStaffingApproval("company/一", "workspace/一", request);
  await decideStaffing("workspace/一", {
    ceo_id: "selfuse-ceo", choice: "APPROVE", reason: "approve current runtime",
  }, request);
  await rollbackStaffing("workspace/一", {
    ceo_id: "selfuse-ceo", reason: "rollback current activation",
  }, request);

  assert.equal(calls[0].path, "/api/workspace/runtime/foundation/companies/company%2F%E4%B8%80/workspaces/workspace%2F%E4%B8%80/staffing-approval");
  assert.match(calls[1].path, /staffing-decision$/);
  assert.equal(JSON.parse(calls[1].options.body).choice, "APPROVE");
  assert.match(calls[2].path, /staffing-rollback$/);
  assert.equal(JSON.parse(calls[2].options.body).reason, "rollback current activation");
});

test("Operating Cycle keeps start execution acceptance recovery and close as scoped commands", async () => {
  const calls = [];
  const request = async (path, options) => {
    calls.push({ path, options });
    return { entity_id: "cycle/一", lifecycle_status: "RUNNING" };
  };
  const workspaceId = "workspace/一";
  const cycleId = "cycle/一";

  await startOperatingCycle(workspaceId, cycleId, { ceo_id: "selfuse-ceo", reason: "start" }, request);
  await executeOperatingCycle(workspaceId, cycleId, { ceo_id: "selfuse-ceo", reason: "execute" }, request);
  await resumeOperatingCycle(workspaceId, cycleId, { ceo_id: "selfuse-ceo", reason: "resume" }, request);
  await reviewOperatingCycle(workspaceId, cycleId, {
    ceo_id: "selfuse-ceo", decision: "ACCEPT", evidence_refs: ["evidence/1"], reason: "accept",
  }, request);
  await closeOperatingCycle(workspaceId, cycleId, {
    ceo_id: "selfuse-ceo", choice: "CONTINUE", reason: "continue",
  }, request);

  assert.deepEqual(calls.map(({ path }) => path), [
    "/api/workspace/runtime/foundation/workspaces/workspace%2F%E4%B8%80/cycles/cycle%2F%E4%B8%80/start",
    "/api/workspace/runtime/foundation/workspaces/workspace%2F%E4%B8%80/cycles/cycle%2F%E4%B8%80/execute",
    "/api/workspace/runtime/foundation/workspaces/workspace%2F%E4%B8%80/cycles/cycle%2F%E4%B8%80/resume",
    "/api/workspace/runtime/foundation/workspaces/workspace%2F%E4%B8%80/cycles/cycle%2F%E4%B8%80/review",
    "/api/workspace/runtime/foundation/workspaces/workspace%2F%E4%B8%80/cycles/cycle%2F%E4%B8%80/close",
  ]);
  assert.equal(JSON.parse(calls[3].options.body).decision, "ACCEPT");
  assert.equal(JSON.parse(calls[4].options.body).choice, "CONTINUE");
});

test("workspace links are dynamic and Runtime errors are safe Chinese projections", () => {
  assert.equal(workspaceEntryHref("workspace/一"), "/ceo-office/workspace?workspace_id=workspace%2F%E4%B8%80");
  assert.equal(runtimeErrorMessage({ status: 403 }), "无权访问该运行对象，或对象已不存在。");
  assert.equal(runtimeErrorMessage({ status: 404 }), "无权访问该运行对象，或对象已不存在。");
  assert.equal(runtimeErrorMessage({ status: 500, message: "secret database error" }), "运行状态暂时无法读取，请稍后重试。");
});
