import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

const read = (path) => readFileSync(new URL(`../${path}`, import.meta.url), "utf8");

test("historical running snapshot without an executor does not claim live employee activity", () => {
  const source = read("components/v1/GeneralWorkspaceOperating.js");
  const expression = source.match(/\{(work\.current_executor_ref \?[^{}]+)\}<\/dd>/)?.[1];
  assert.ok(expression);
  const progress = new Function("work", `return (${expression});`);
  assert.equal(progress({ execution_status: "RUNNING", current_executor_ref: null }), "当前没有员工执行");
  assert.equal(progress({ execution_status: "RUNNING", current_executor_ref: "employee-a" }), "员工正在处理");
  assert.equal(progress({ execution_status: "WAITING", current_executor_ref: "employee-a" }), "员工已接手");
  assert.match(source, /EXECUTING: \["正在处理"/);
});

test("global assistant uses the canonical runtime identity without fake local answers", () => {
  const source = read("components/assistant/GlobalAssistant.js");
  assert.match(source, /canonicalAssistantIdentity\(snapshot\)/);
  assert.match(source, /snapshot\?\.assistant/);
  assert.doesNotMatch(source, /getAssistantIdentity|updateAssistantIdentity/);
  assert.doesNotMatch(source, /pathname === "\/ceo-office".*dispatch\(\{ type: "open"/s);
  assert.doesNotMatch(source, /已基于 .* Runtime 快照回答/);
});

test("general workspace consumes canonical work and execution APIs", () => {
  const component = read("components/v1/GeneralWorkspaceOperating.js");
  const page = read("app/ceo-office/workspace/page.js");
  const api = read("lib/runtimeApi.js");
  assert.match(page, /business_type.*GENERIC/s);
  assert.match(page, /GeneralWorkspaceOperating/);
  assert.match(component, /getGeneralWorkspace/);
  assert.match(component, /createGeneralWorkspaceWork/);
  assert.match(component, /executeGeneralWorkspaceWork/);
  assert.match(component, /responsibility_holder_name/);
  assert.match(component, /current_executor_ref/);
  assert.match(component, /ResultReferenceView/);
  assert.match(read("components/v1/ResultReferenceView.js"), /SharedResultUtility/);
  assert.match(component, /materializeGeneralWorkspaceTeam/);
  assert.match(component, /getGeneralWorkspaceTeamCandidates/);
  assert.match(component, /assignGeneralWorkspaceEmployee/);
  assert.match(component, /加入业务团队/);
  assert.doesNotMatch(component, /重新处理/);
  assert.match(component, /lifecycleActions\(scopedWork\)/);
  assert.match(component, /reviewGeneralWorkspaceDecision/);
  assert.match(component, /chooseGeneralWorkspaceDecision/);
  assert.match(component, /已转交给/);
  assert.match(component, /需要你的决定/);
  assert.match(api, /shared\/general\/works/);
  assert.match(api, /decision\/review/);
  assert.match(api, /shared\/results/);
  assert.match(api, /team-operating\/works/);
  assert.match(api, /shared\/general\/team\/assign/);
  assert.doesNotMatch(component, /fake|mock|模拟完成/i);
});

test("general workspace exposes durable lifecycle controls in user language", () => {
  const component = read("components/v1/GeneralWorkspaceOperating.js");
  const api = read("lib/runtimeApi.js");
  assert.match(api, /lifecycle/);
  assert.match(component, /controlGeneralWorkspaceWork/);
  assert.match(component, /暂停/);
  assert.match(component, /继续工作/);
  assert.match(component, /归档/);
  assert.doesNotMatch(component, /runtime_entities/);
});
