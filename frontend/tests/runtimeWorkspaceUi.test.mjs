import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

import {
  getCanonicalBusinesses,
  getRuntimeWorkspace,
  getRuntimeWorkspaceDetails,
  getWorkspaceParentPath,
  isLegacyOfficeType,
  workspaceOfficeHref,
} from "../lib/runtimeApi.js";


const read = (path) => readFile(new URL(path, import.meta.url), "utf8");

test("Workspace detail reads only tenant-scoped Runtime API paths", async () => {
  const calls = [];
  const request = async (path) => {
    calls.push(path);
    return { workspace: { workspace_id: path } };
  };

  await getRuntimeWorkspace("company/一", "workspace/一", request);
  await getRuntimeWorkspaceDetails("company/一", [{ workspace_id: "rd" }, { workspace_id: "xhs" }], request);

  assert.deepEqual(calls, [
    "/api/workspace/runtime/foundation/companies/company%2F%E4%B8%80/workspaces/workspace%2F%E4%B8%80",
    "/api/workspace/runtime/foundation/companies/company%2F%E4%B8%80/workspaces/rd",
    "/api/workspace/runtime/foundation/companies/company%2F%E4%B8%80/workspaces/xhs",
  ]);
});

test("Package workspaces open the installed office while legacy RD/XHS/TTK never deep-link", () => {
  // Current V1 model: only PACKAGE workspaces have a dedicated office.
  assert.equal(
    workspaceOfficeHref({ workspace_id: "pkg/1", business_type: "PACKAGE" }),
    "/ceo-office/workspace/installed/pkg%2F1",
  );
  // Frozen legacy business types (out of V1 scope) must never resolve to their old
  // software / xhs / shortvideo pages; they fall back to the generic workspace entry.
  for (const type of ["RD", "XHS", "TTK", "rd", "xhs", "ttk"]) {
    const href = workspaceOfficeHref({ workspace_id: "legacy/1", business_type: type });
    assert.equal(href, "/ceo-office/workspace?workspace_id=legacy%2F1");
    assert.doesNotMatch(href, /software|xhs|shortvideo/);
  }
  // Unknown / empty types keep the generic fallback unchanged.
  assert.equal(workspaceOfficeHref({ workspace_id: "g/1", business_type: "" }), "/ceo-office/workspace?workspace_id=g%2F1");
});

test("isLegacyOfficeType recognises only frozen RD/XHS/TTK business types", () => {
  for (const type of ["RD", "XHS", "TTK", "rd", "xhs", "ttk"]) {
    assert.equal(isLegacyOfficeType(type), true);
  }
  for (const type of ["PACKAGE", "GENERIC", "", null, undefined]) {
    assert.equal(isLegacyOfficeType(type), false);
  }
});

test("Frozen legacy office pages are preserved but carry an out-of-V1 notice", async () => {
  const [software, xhs, shortvideo, notice, portal] = await Promise.all([
    read("../app/ceo-office/workspace/software/page.js"),
    read("../app/ceo-office/workspace/xhs/page.js"),
    read("../app/ceo-office/workspace/shortvideo/page.js"),
    read("../components/workspace/LegacyOfficeScopeNotice.js"),
    read("../app/ceo-office/workspace/page.js"),
  ]);
  // Pages and their legacy components are preserved (history not deleted) ...
  assert.match(software, /RdWorkspacePhaseTwo/);
  assert.match(xhs, /XhsWorkspacePhaseOne/);
  assert.match(shortvideo, /WorkspaceRuntimeView businessType="TTK"/);
  // ... but each renders the shared out-of-scope marker for direct-URL visitors.
  for (const source of [software, xhs, shortvideo]) {
    assert.match(source, /LegacyOfficeScopeNotice/);
  }
  assert.match(notice, /data-legacy-office-notice/);
  assert.match(notice, /V1/);
  // The workspace entry page uses the legacy predicate instead of a self-looping office link.
  assert.match(portal, /isLegacyOfficeType/);
});

test("Business and Workspace entry consume canonical spine APIs", async () => {
  const calls = [];
  const request = async (path) => { calls.push(path); return {}; };
  await getCanonicalBusinesses("company/一", request);
  await getWorkspaceParentPath("workspace/一", request);
  assert.deepEqual(calls, [
    "/api/workspace/runtime/foundation/companies/company%2F%E4%B8%80/businesses",
    "/api/workspace/runtime/foundation/workspaces/workspace%2F%E4%B8%80/parent-path",
  ]);
});

test("RD and XHS use independent professional instances while TTK is an honest compatibility entry", async () => {
  const [portal, rd, rdPhaseTwo, xhs, ttk, view, shell, phaseOne] = await Promise.all([
    read("../app/ceo-office/workspace/page.js"),
    read("../app/ceo-office/workspace/software/page.js"),
    read("../components/rd/RdWorkspacePhaseTwo.js"),
    read("../app/ceo-office/workspace/xhs/page.js"),
    read("../app/ceo-office/workspace/shortvideo/page.js"),
    read("../components/runtime/WorkspaceRuntimeView.js"),
    read("../components/workspace/WorkspacePaneShell.js"),
    read("../components/xhs/XhsWorkspacePhaseOne.js"),
  ]);

  assert.match(portal, /getCanonicalBusinesses/);
  assert.match(portal, /getWorkspaceParentPath/);
  assert.match(rd, /RdWorkspacePhaseTwo/);
  assert.match(xhs, /XhsWorkspacePhaseOne/);
  assert.match(ttk, /WorkspaceRuntimeView businessType="TTK"/);
  assert.match(view, /not-yet-accepted TTK professional instance/);
  assert.match(view, /getWorkspaceParentPath/);
  assert.doesNotMatch(view, /createRuntimeCycle|createRuntimeContentItem|createRuntimeSimulation|RdRealExecutionComposer/);
  for (const source of [portal, ttk, view]) {
    assert.doesNotMatch(source, /getProjects|getTasks|TaskLauncher|project_type|fixture|mock/i);
  }
  assert.match(rdPhaseTwo, /WorkspacePaneShell/);
  assert.match(rdPhaseTwo, /getRuntimeWorkspace/);
  assert.match(rdPhaseTwo, /getProject/);
  assert.match(rdPhaseTwo, /getTask/);
  assert.match(rdPhaseTwo, /responsibilityEmployeeRef/);
  assert.match(rdPhaseTwo, /currentExecutorRef/);
  assert.match(rdPhaseTwo, /code_change/);
  assert.match(rdPhaseTwo, /computerAccess/);
  assert.match(rdPhaseTwo, /Result Reference|查看代码变化与测试结果/);
  assert.doesNotMatch(rdPhaseTwo, /Calendar|ContentItem|Note|fixture|mock/i);
  assert.doesNotMatch(xhs, /WorkspaceRuntimeView|TerraShell|getProjects|getTasks|TaskLauncher|project_type|fixture|mock/i);
  for (const label of ["CEO 工作台", "业务空间", "组织中心", "人才市场", "资料库", "会议", "选题库 · 信号", "图文预览"]) {
    assert.match(shell, new RegExp(label));
  }
  assert.match(shell, /workspaceId/);
  assert.match(shell, /contextWidth/);
  assert.match(shell, /utilityWidth/);
  assert.match(phaseOne, /runtime\.snapshot/);
  assert.match(phaseOne, /work_context/);
  assert.match(phaseOne, /当前没有执行员工/);
  assert.match(phaseOne, /暂无可用员工引用/);
  assert.match(phaseOne, /等待你的决定 · 查看决策方案/);
  assert.match(phaseOne, /按建议处理/);
  assert.match(phaseOne, /plainPackage/);
  assert.match(phaseOne, /SourceMark/);
  assert.match(phaseOne, /尚未连接可验证的信号来源/);
  assert.match(phaseOne, /WAITING_FOR_CAPABILITY/);
  assert.match(phaseOne, /当前没有已验证的发布能力/);
  assert.match(phaseOne, /暂无数据/);
  assert.doesNotMatch(phaseOne, /["']PUBLISHING["']|["']ANALYTICS_PENDING["']|["']ANALYTICS_READY["']|fixture|mock/i);
});

test("Runtime compatibility view does not mix accepted RD or XHS domain logic", async () => {
  const view = await read("../components/runtime/WorkspaceRuntimeView.js");
  assert.match(view, /canonical Workspace identity/);
  assert.match(view, /尚未验收/);
  assert.doesNotMatch(view, /INTAKE:|ContentRuntime|RdRuntime|OperatingCycleControl|SimulationLauncher/);
});

test("Workspace pages extend the existing shared Assistant context without a third column", async () => {
  const [view, state, assistant] = await Promise.all([
    read("../components/runtime/WorkspaceRuntimeView.js"),
    read("../lib/assistantState.mjs"),
    read("../components/assistant/GlobalAssistant.js"),
  ]);

  for (const key of ["workspace_id", "business_type"]) {
    assert.match(state, new RegExp(`"${key}"`));
    assert.match(view, new RegExp(`${key}:`));
  }
  assert.match(assistant, /position|fixed/);
  assert.doesNotMatch(view, /<aside|xl:grid-cols-3/);
});

test("Workspace Studio persists a truthful Blueprint assembly draft before Runtime gates", async () => {
  const studio = await read("../app/ceo-office/workspace/studio/page.js");

  for (const stage of ["Discover", "Blueprint", "Compose", "Bind", "Staff", "Simulate", "Approve", "Operate"]) {
    assert.match(studio, new RegExp(`\\[\"${stage}\"`));
  }
  for (const field of [
    "stageContracts",
    "roleSlots",
    "capabilityBindings",
    "evidenceRule",
    "failurePolicy",
    "simulationScenarios",
    "approvalGate",
  ]) {
    assert.match(studio, new RegExp(`${field}:`));
  }
  assert.match(studio, /STUDIO_DRAFT/);
  assert.match(studio, /PLANNED_NOT_MATERIALIZED/);
  assert.match(studio, /REQUIRED_NOT_AUTHORIZED/);
  assert.match(studio, /CEO_EXPLICIT_APPROVAL_REQUIRED/);
  assert.match(studio, /保存 Draft 并形成候选岗位方案/);
  assert.match(studio, /capabilityRefs/);
  assert.match(studio, /requirement:code-repository/);
  assert.match(studio, /未模拟 · 未批准/);
  assert.match(studio, /createRuntimeWorkspace/);
  assert.doesNotMatch(studio, /getProjects|getTasks|createProject|localStorage|sessionStorage/i);
});

test("CEO Workforce and Assistant separate proposed candidates from active AI employees", async () => {
  const [entry, desk, assistant] = await Promise.all([
    read("../app/ceo-office/page.js"),
    read("../components/v1/CeoDeskOperating.js"),
    read("../components/assistant/GlobalAssistant.js"),
  ]);

  assert.match(entry, /CeoDeskOperating/);
  assert.match(desk, /只看今天需要知道、决定和推进的事情/);
  assert.match(desk, /当前没有可证明的下一责任/);
  assert.doesNotMatch(desk, /候选专业 AI · 尚未雇佣或在岗/);
  assert.match(assistant, /employee\.lifecycle_status !== "PROPOSED"/);
  assert.match(assistant, /activeEmployees\.length \+ \(snapshot\??\.assistant \? 1 : 0\)/);
  assert.match(assistant, /今日简报/);
  assert.match(assistant, /我正在关注/);
  assert.match(assistant, /候选方案待审查/);
  assert.doesNotMatch(assistant, /指令已创建 Task|查看 Task/);
});
