import assert from "node:assert/strict";
import test from "node:test";
import { d1Reducer, initialD1State, interactionKey, readDraft, saveDraft, messageRequest, pendingRequest, rememberRequest, isMatchingCompletion, receiptEligible, lifecycleActions, remainingDraft, readableResult, executionLabel, accessLabel, currentResponsibilities } from "../lib/d1State.mjs";

test("A Result round trip restores the same Work and scroll anchor without a new view receipt", () => {
  const work = { view: "work", workRef: "original", workspaceId: "w", employeeRef: "e" };
  let state = initialD1State(work);
  state = d1Reducer(state, { type: "navigate", entry: { ...work, view: "result", resultRef: "r", explicit: true }, anchor: "result-r" });
  state = d1Reducer(state, { type: "back" });
  assert.equal(state.entry.workRef, "original");
  assert.equal(state.entry.employeeRef, "e");
  assert.equal(state.entry.anchor, "result-r");
  assert.equal(state.entry.explicit, false);
});

test("Unsent drafts and retry commands stay isolated across companies, scopes and topics", () => {
  const entry = { view: "conversation", employeeRef: "e", conversationId: "topic-one", scopeType: "COMPANY", scopeRef: "c" };
  const key = interactionKey("c", entry);
  saveDraft(key, "未发草稿"); rememberRequest(key, { request_id: "original" });
  for (const other of [interactionKey("other", entry), interactionKey("c", { ...entry, conversationId: "topic-two" }), interactionKey("c", { ...entry, scopeType: "BUSINESS", scopeRef: "b" })]) {
    assert.equal(readDraft(other), ""); assert.equal(pendingRequest(other), null);
  }
  assert.equal(readDraft(key), "未发草稿"); assert.equal(pendingRequest(key).request_id, "original");
  saveDraft(key, ""); rememberRequest(key, null);
});

test("Network retries reuse the message key, while deliberately changed input gets a new key", () => {
  let ids = 0;
  const newId = () => `request-${++ids}`;
  const first = messageRequest(null, { body: "  first  ", assignment_ref: "a" }, newId);
  assert.strictEqual(messageRequest(first, { body: "first", assignment_ref: "a" }, newId), first);
  assert.notEqual(messageRequest(first, { body: "first", assignment_ref: "other" }, newId).request_id, first.request_id);
  assert.notEqual(messageRequest(first, { body: "edited", assignment_ref: "a" }, newId).request_id, first.request_id);
});

test("Another completed message cannot clear this unsent or uncertain input", () => {
  const view = { messages: [{ message_id: "m", idempotency_key: "request-a" }], attempts: [{ message_id: "m", status: "COMPLETED" }] };
  assert.equal(isMatchingCompletion(view, { request_id: "request-b" }), false);
  assert.equal(isMatchingCompletion(view, { request_id: "request-a" }), true);
  assert.equal(isMatchingCompletion({ ...view, attempts: [{ message_id: "m", status: "UNVERIFIED" }] }, { request_id: "request-a" }), false);
});

test("Only explicitly opened supported current Result identity can create a Viewed receipt", () => {
  const result = { kind: "RESULT", reference_id: "r", result_version: "v", content: "实际正文" };
  assert.equal(receiptEligible({ explicit: true, resultRef: "r", workspaceId: "w" }, result), true);
  assert.equal(receiptEligible({ explicit: false, resultRef: "r", workspaceId: "w" }, result), false);
  assert.equal(receiptEligible({ explicit: true, resultRef: "other", workspaceId: "w" }, result), false);
  assert.equal(receiptEligible({ explicit: true, resultRef: "r" }, result), false);
  assert.equal(receiptEligible({ explicit: true, resultRef: "r", workspaceId: "w" }, { ...result, kind: "ARTIFACT" }), false);
});

test("A pending completion clears only the actual unchanged draft, including bounded retry", () => {
  const sent = messageRequest(null, { body: "原消息", assignment_ref: "a" }, () => "same-request");
  assert.equal(remainingDraft("新草稿必须保留", sent.body), "新草稿必须保留");
  assert.equal(remainingDraft(" 原消息 ", sent.body, " 原消息 "), "");
  assert.equal(remainingDraft("原消息 ", sent.body, "原消息"), "原消息 ");
  const retry = { body: "失败的旧消息", request_id: "original", retry_no: 1 };
  assert.equal(remainingDraft("正在编辑的新内容", retry.body), "正在编辑的新内容");
  assert.equal(remainingDraft("", retry.body), "");
});

test("Viewed requires actual rendered material, excluding blank, metadata and unsupported objects", () => {
  const selection = { explicit: true, resultRef: "r", workspaceId: "w" };
  const base = { kind: "RESULT", reference_id: "r", result_version: "v" };
  for (const content of [null, "", "  \n ", 5, { title: "仅标题", reference_id: "r" }, { unsupported: "隐藏内容" }]) {
    const result = { ...base, content, artifacts: [{ title: "材料索引", artifact_id: "a" }] };
    assert.deepEqual(readableResult(result), []);
    assert.equal(receiptEligible(selection, result), false);
  }
  const structured = { ...base, data: { sections: [{ title: "证据", text: "实际材料正文" }] } };
  assert.deepEqual(readableResult(structured), [{ title: "证据", text: "实际材料正文" }]);
  assert.equal(receiptEligible(selection, structured), true);
  const artifact = { ...base, artifacts: [{ title: "附件全文", content: "确实已读取的材料" }] };
  assert.equal(readableResult(artifact)[0].text, "确实已读取的材料");
  assert.equal(receiptEligible(selection, artifact), true);
  assert.equal(receiptEligible({ ...selection, explicit: false }, artifact), false);
});

test("Execution and permission labels reflect returned evidence, never endpoint inference", () => {
  assert.equal(executionLabel(), "执行方式待确认");
  assert.equal(executionLabel([{ capability_type: "agent", enabled: true }]), "Agent绑定 · 名称未记录");
  assert.equal(executionLabel([{ capability_type: "model", enabled: true, display_name: "已记录名称" }]), "模型绑定 · 已记录名称");
  assert.equal(executionLabel([{ capability_type: "agent", enabled: false }]), "执行方式待确认");
  assert.equal(executionLabel([{ capability_type: "model", enabled: true }, { capability_type: "agent", enabled: true }]), "执行方式待确认");
  assert.equal(accessLabel({ configured_state: "GRANTED", effective_state: "UNKNOWN" }), "权限尚未确认");
  assert.equal(accessLabel({ effective_state: "GRANTED" }), "当前已授予访问权限");
});

test("Terminal and unknown scope Work does not offer pause or resume", () => {
  assert.deepEqual(lifecycleActions({ work_ref: "x", lifecycle_status: "ACTIVE" }), []);
  assert.deepEqual(lifecycleActions({ workspaceId: "w", work_ref: "x", lifecycle_status: "COMPLETED" }), ["archive"]);
  assert.deepEqual(lifecycleActions({ workspaceId: "w", work_ref: "x", lifecycle_status: "PAUSED" }), ["resume", "cancel"]);
});


test("Current Work responsibility uses supplied activity, prioritizes exact context and keeps all lawful entries", () => {
  const first = { object_type: "WORK", object_ref: "other", responsibility_holder_ref: "e", object_owner_ref: "e", activity: "等待核对资料。", work_status: "waiting" };
  const current = { ...first, object_ref: "current", activity: "责任已分配，尚未开始执行。", work_status: "idle", current_executor_ref: null };
  const employee = { employee_ref: "e", responsibility: "长期岗位职责", current_responsibilities: [first, current, { ...first, object_ref: "another", activity: "整理现有材料。" }] };
  const snapshot = structuredClone(employee);
  assert.deepEqual(currentResponsibilities(employee, "current"), { items: [{ current: true, work: true, activity: current.activity }, { current: false, work: true, activity: first.activity }, { current: false, work: true, activity: "整理现有材料。" }], message: "" });
  assert.deepEqual(employee, snapshot);
  assert.equal(currentResponsibilities(employee).items.filter((item) => item.current).length, 0);
  assert.equal(currentResponsibilities(employee, "not-provided").items.length, 3);
});

test("Current responsibilities reject foreign holders/owners and never infer ownership from executor, name or role", () => {
  const valid = { object_type: "WORK", object_ref: "current", responsibility_holder_ref: "e", object_owner_ref: "e", activity: "已分配" };
  const employee = { employee_ref: "e", name: "same name", role: "same role", current_responsibilities: [
    { ...valid, responsibility_holder_ref: "foreign" }, { ...valid, object_owner_ref: "foreign" },
    { ...valid, responsibility_holder_ref: null, current_executor_ref: "e" }, { ...valid, responsibility_holder_ref: undefined, object_owner_ref: "e" }, null, valid,
  ] };
  assert.equal(currentResponsibilities(employee, "current").items.length, 1);
  assert.equal(currentResponsibilities({ ...employee, employee_ref: "" }).message, "当前责任未记录");
  assert.equal(currentResponsibilities({ ...employee, current_responsibilities: employee.current_responsibilities.slice(0, -1) }).message, "当前责任未记录");
});

test("Empty, absent and incomplete current responsibilities stay distinct from static role responsibility", () => {
  assert.deepEqual(currentResponsibilities({ employee_ref: "e", responsibility: "长期职责", current_responsibilities: [] }), { items: [], message: "当前工作空间暂无已记录的当前责任" });
  for (const current_responsibilities of [undefined, null, {}, "unknown"]) assert.deepEqual(currentResponsibilities({ employee_ref: "e", responsibility: "静态职责", current_responsibilities }), { items: [], message: "当前责任未记录" });
  for (const activity of [undefined, null, " ", {}]) assert.deepEqual(currentResponsibilities({ employee_ref: "e", current_responsibilities: [{ responsibility_holder_ref: "e", activity }] }, "missing"), { items: [{ current: false, work: false, activity: "当前活动未记录" }], message: "" });
});


test("Work controls use canonical lifecycle and never offer failed execution retry", () => {
  for (const lifecycle_status of ["PLANNED", "READY", "ACTIVE", "WAITING", "BLOCKED"]) assert.deepEqual(lifecycleActions({ workspaceId:"w", work_ref:"x", lifecycle_status }), ["pause","cancel"]);
  for (const lifecycle_status of ["FAILED", "UNKNOWN"]) assert.deepEqual(lifecycleActions({ workspaceId:"w", work_ref:"x", lifecycle_status }), []);
  assert.deepEqual(lifecycleActions({workspaceId:"w",work_ref:"x",lifecycle_status:"ARCHIVED"}), ["restore"]);
});
