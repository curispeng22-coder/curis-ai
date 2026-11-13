import assert from "node:assert/strict";
import test from "node:test";
import { createD1Api, d1Error } from "../lib/d1Api.js";

test("Work read resolves the exact workspace and reference, never substitutes another Work", async () => {
  const calls = [];
  const api = createD1Api(async (path) => { calls.push(path); return { company: { company_id: "c" }, workspace: { workspace_id: "w" }, current_work: [{ work_ref: "a", problem: "A" }, { work_ref: "b", problem: "B" }] }; });
  assert.equal((await api.work("c", "w", "b")).problem, "B");
  await assert.rejects(api.work("c", "w", "missing"), (error) => error.status === 404);
  await assert.rejects(api.work("c", "", "b"), (error) => error.code === "WORK_READ_SCOPE_GAP");
  assert.equal(calls.length, 2);
  const wrong = createD1Api(async () => ({ company: { company_id: "foreign" }, workspace: { workspace_id: "w" }, current_work: [{ work_ref: "b" }] }));
  await assert.rejects(wrong.work("c", "w", "b"), /范围不一致/);
});

test("Topic sends preserve message id, Assignment and strict supported DTO on retries", async () => {
  const calls = [];
  const api = createD1Api(async (path, options) => { calls.push({ path, options }); return {}; });
  const payload = { body: "same message", request_id: "same-request", assignment_ref: "assignment", signature: "internal", inputAtSend: "  same message  " };
  await api.send("company/1", { conversationId: "topic:1" }, payload);
  await api.send("company/1", { conversationId: "topic:1" }, payload);
  assert.equal(calls[0].path, "/api/workspace/v1/companies/company%2F1/conversations/topic%3A1/messages");
  assert.deepEqual(JSON.parse(calls[0].options.body), { body: "same message", request_id: "same-request", assignment_ref: "assignment", references: [] });
  assert.equal(calls[0].options.body, calls[1].options.body);
  assert.equal(calls.length, 2);
});

test("Stable Employee entry opens its canonical holder; it does not create a topic or Work", async () => {
  const paths = [];
  const api = createD1Api(async (path) => { paths.push(path); return {}; });
  await api.send("c", { employeeRef: "e" }, { body: "question", request_id: "r", assignment_ref: "a" });
  assert.deepEqual(paths, ["/api/workspace/v1/companies/c/employees/e/conversation/open", "/api/workspace/v1/companies/c/employees/e/conversation/messages"]);
});

test("Viewed records exactly the returned version and cannot accept or transition a Result", async () => {
  const calls = [];
  const api = createD1Api(async (path, options) => { calls.push({ path, options }); return {}; });
  await api.result("c", "w", "task:result");
  assert.equal(calls[0].options, undefined);
  await api.viewed("c", "w", { kind: "RESULT", reference_id: "task:result", result_version: "source-hash" });
  assert.deepEqual(JSON.parse(calls[1].options.body), { workspace_id: "w", result_ref: "task:result", result_version: "source-hash" });
  assert.equal(calls[1].path, "/api/workspace/v1/companies/c/result-viewed");
  assert.throws(() => api.viewed("c", "w", { kind: "ARTIFACT", reference_id: "a" }), /版本/);
  assert.throws(() => api.result("c", "", "r"), (error) => error.code === "RESULT_READ_SCOPE_GAP");
});

test("Only supported lifecycle commands can reach the existing scoped endpoint", async () => {
  const calls = [];
  const api = createD1Api(async (path, options) => calls.push({ path, options }));
  await api.controlWork("c", { workspaceId: "w", work_ref: "work" }, "pause", "核对来源");
  assert.equal(calls[0].path, "/api/workspace/runtime/foundation/companies/c/workspaces/w/shared/general/works/work/lifecycle/pause");
  assert.throws(() => api.controlWork("c", { workspaceId: "w", work_ref: "work" }, "accept", ""), /不支持/);
  assert.throws(() => api.controlWork("c", { work_ref: "work" }, "resume", ""), /未接入/);
});

test("Errors never expose Provider or database diagnostic text", () => {
  assert.ok(!d1Error({ message: "private provider sql trace" }).includes("private"));
  assert.match(d1Error({ status: 403 }), /身份/);
  assert.match(d1Error({ status: 409 }), /输入已保留/);
});

test("Employee detail resolves explicit same-Company mapping before read-only binding lookup", async () => {
  const paths = [];
  const projection = { company: { company_id: "c" }, workspace: { workspace_id: "w" }, team: { employees: [{ employee_ref: "runtime-e", company_employee_ref: "company-e", identity_status: "VERIFIED_EXPLICIT_BRIDGE", identity_bridge: { status: "VERIFIED", companyEmployeeRef: "company-e" }, organization_record: { identity_status: "VERIFIED_EXPLICIT_BRIDGE", name: "真实员工名" } }] } };
  const api = createD1Api(async (path) => { paths.push(path); return path.endsWith("/capabilities") ? { employee_id: "company-e", bindings: [{ capability_type: "agent", enabled: true }] } : projection; });
  const value = await api.employeeDetail("c", "runtime-e", "w");
  assert.equal(value.organization_record.name, "真实员工名");
  assert.equal(paths[1], "/api/workspace/employees/company-e/capabilities");
  assert.ok(paths.every((path) => !path.includes("recover")));
  await assert.rejects(api.employeeDetail("c", "runtime-e", ""));
  projection.team.employees[0].identity_status = "EXACT_ID_FALLBACK";
  const before = paths.length;
  await assert.rejects(api.employeeDetail("c", "runtime-e", "w"));
  assert.equal(paths.length, before + 1);
  projection.team.employees[0].identity_status = "VERIFIED_EXPLICIT_BRIDGE";
  projection.team.employees[0].identity_bridge.companyEmployeeRef = "foreign-e";
  await assert.rejects(api.employeeDetail("c", "runtime-e", "w"));
  projection.company.company_id = "foreign-company";
  await assert.rejects(api.employeeDetail("c", "runtime-e", "w"));
});


test("Work Usage is a scoped read and cannot accept foreign rows or invent totals", async () => {
  const work = {companyId:"c", workspaceId:"w", work_ref:"original"};
  const records = [{usage_record_id:"one",company_id:"c",workspace_id:"w",work_ref:"original",cost_amount:null,total_tokens:null},
    {usage_record_id:"two",company_id:"c",workspace_id:"w",work_ref:"original",cost_amount:null,total_tokens:null}];
  const calls=[];
  const api=createD1Api(async (path,options)=>{calls.push([path,options]);return {company_id:"c",workspace_id:"w",work_ref:"original",records};});
  assert.deepEqual(await api.usage("c",work),records);
  assert.equal(calls[0][1],undefined);
  assert.match(calls[0][0],/companies\/c\/workspaces\/w\/shared\/general\/works\/original\/usage$/);
  records[0].workspace_id="foreign";
  await assert.rejects(api.usage("c",work),/范围不一致/);
  await assert.rejects(api.usage("other",work));
});
