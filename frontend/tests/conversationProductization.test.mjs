import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { createRequire } from "node:module";
import vm from "node:vm";
import { createHash, webcrypto } from "node:crypto";
import { computerAccessView } from "../lib/computerAccess.mjs";

const read = (path) => readFileSync(new URL(`../${path}`, import.meta.url), "utf8");
test("quick access reads bounded canonical summaries, not local history", () => {
  const source = read("components/v1/ConversationQuickAccess.js");
  assert.match(source, /getRecentConversations/);
  assert.match(source, /row.conversation_id/);
  assert.match(source, /row.activity_at/);
  assert.match(source, /dismissConversation/);
  assert.match(source, /request.current !== token/);
  assert.match(source, /recentRows\(visible.rows, expanded\)/);
  assert.doesNotMatch(source, /localStorage|sessionStorage|messages|createConversation/);
  assert.match(read("components/v1/V1Sidebar.js"), /<ConversationQuickAccess/);
});
test("topic surface reuses shared Employee holder and composer", () => {
  const page = read("app/ceo-office/conversation/page.js");
  assert.match(page, /joinConversation/);
  assert.match(page, /request.current/);
  assert.match(page, /conversationId=\{id\}/);
  const component = read("components/v1/EmployeeConversation.js");
  assert.match(component, /ConversationComposer/);
  assert.match(component, /sendConversation\(companyId, conversationId/);
  assert.match(component, /return_to=/);
  assert.match(component, /ResultReferenceView/);
  assert.doesNotMatch(component, /createWork|createProject/);
});
test("legacy assistant stops consuming simulation and local read cursor truth", () => {
  const source = read("components/assistant/GlobalAssistant.js");
  assert.match(source, /getCompanyAttention/);
  assert.doesNotMatch(source, /runtime.simulations|lastSeenEventId|localStorage|postAssistantMessage/);
  assert.match(source, /canonicalAssistantIdentity/);
  assert.match(read("components/terra/TerraShell.js"), /target.startsWith\("\/ceo-office\/conversation\?conversation_id="\)/);
});

const require = createRequire(import.meta.url);
const React = require("react"), { renderToStaticMarkup } = require("react-dom/server");
const postcss = require("postcss"), swc = require("next/dist/build/swc");
await swc.loadBindings();
const { code } = await swc.transform(read("components/v1/SharedConversation.js"), {
  filename: "SharedConversation.js", isModule: true,
  jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } },
  module: { type: "commonjs" },
});
const loaded = { exports: {} };
vm.runInNewContext(code, {
  module: loaded, exports: loaded.exports,
  require: (name) => {
    if (name === "react" || name === "react/jsx-runtime") return require(name);
    if (name.endsWith("computerAccess.mjs")) return { computerAccessView };
    if (["next/link", "../../lib/v1FrontendApi.js", "./EmployeeAvatar.js", "./ResultReferenceView.js"].includes(name)) return {};
    throw new Error(`Unexpected composer import: ${name}`);
  },
});
const { ConversationComposer } = loaded.exports;
test("Agent input reuses composer without a second submit action", () => {
  const markup = renderToStaticMarkup(React.createElement(ConversationComposer, {
    value: "synthetic work", onSubmit: () => {}, showSubmit: false, showVoice: false,
    notice: "核对后在正式工作中执行",
  }));
  assert.match(markup, /synthetic work/);
  assert.doesNotMatch(markup, /type="submit"/);
  const discussion = renderToStaticMarkup(React.createElement(ConversationComposer, { value: "synthetic discussion" }));
  assert.match(discussion, /type="submit"/);
});
function agentHarness(api, storage = new Map(), resultModule = {}) {
  const slots = [], effects = []; let cursor = 0;
  const hooks = {
    useState(initial) { const index = cursor++; if (!(index in slots)) slots[index] = typeof initial === "function" ? initial() : initial;
      return [slots[index], (value) => { slots[index] = typeof value === "function" ? value(slots[index]) : value; }]; },
    useRef(initial) { const index = cursor++; return slots[index] ||= { current: initial }; },
    useEffect(effect, deps) { const index = cursor++, old = slots[index];
      if (!old || !deps.every((value, i) => Object.is(value, old.deps[i]))) {
        effects.push(() => { old?.cleanup?.(); slots[index] = { deps, cleanup: effect() }; });
      } },
  };
  const module = { exports: {} };
  vm.runInNewContext(code, { module, exports: module.exports, JSON, TextEncoder, crypto: { randomUUID: () => "explicit-request", subtle: webcrypto.subtle },
    localStorage: { getItem: (key) => storage.has(key) ? storage.get(key) : null, setItem: (key, value) => storage.set(key, value), removeItem: (key) => storage.delete(key) },
    setInterval: () => 1, clearInterval() {},
    require(name) { if (name === "react") return hooks; if (name === "react/jsx-runtime") return require(name);
      if (name === "../../lib/v1FrontendApi.js") return {
        getAssignedAgentWorkflow: async () => ({ tenant_id: "tenant-a", company_id: "company-a", workspace_id: "workspace-a", assignment_ref: "assignment-a", state: "READY" }),
        ...api,
      }; if (name.endsWith("computerAccess.mjs")) return { computerAccessView };
      if (name === "./ResultReferenceView.js") return resultModule;
      if (["next/link", "./EmployeeAvatar.js"].includes(name)) return {};
      throw new Error("Unexpected Agent test import: " + name); },
  });
  return { render(props, flush = true) { cursor = 0; const tree = module.exports.AgentWorkControl(props); if (flush) while (effects.length) effects.shift()(); return tree; },
    flush() { while (effects.length) effects.shift()(); } };
}
function agentNodes(tree) {
  if (tree == null || typeof tree !== "object") return [];
  if (Array.isArray(tree)) return tree.flatMap(agentNodes);
  return [tree, ...agentNodes(tree.props?.children)];
}
const agentProps = { companyId: "company-a", workspaceId: "workspace-a", tenantId: "tenant-a",
  assignmentRef: "assignment-a", agents: [{ binding_id: "binding-a", display_name: "Test Agent" }],
  readiness: { state: "AVAILABLE" }, body: "处理原选段", contextKey: "content:content-a",
  source: { kind: "content-growth", content_ref: "content-a", expected_version_ref: "version-a", selection: { excerpt: "原文字" }, references: [] } };

function scopedPending(props, payload) {
  const source = props.source.kind === "content-growth" ? { kind: props.source.kind, content_ref: props.source.content_ref }
    : props.source.kind === "writing" ? { kind: props.source.kind, book_ref: props.source.book_ref, chapter_ref: props.source.chapter_ref }
    : { kind: props.source.kind, song_ref: props.source.song_ref };
  return { scope: { version: 1, binding: { tenantId: props.tenantId, companyId: props.companyId,
    workspaceId: props.workspaceId, assignmentRef: props.assignmentRef, contextKey: props.contextKey, source } }, payload };
}
function businessSource(kind) {
  return kind === "writing" ? { kind, book_ref: "book", chapter_ref: "chapter" }
    : kind === "music" ? { kind, song_ref: "song" } : agentProps.source;
}
function contextFor(source) { return source.kind === "writing" ? `chapter:${source.book_ref}:${source.chapter_ref}` : source.kind === "music" ? `song:${source.song_ref}` : `content:${source.content_ref}`; }
function provenWork(work, props) {
  return { ...work, data: { responsibilityAssignmentRef: props.assignmentRef,
    followupContract: { agentSource: { input: props.source } } } };
}
function provenOrigin(props) {
  return { status: "VERIFIED", assignment_ref: props.assignmentRef, source: scopedPending(props).scope.binding.source };
}
function priorTextApi(props, workRef, taskRef) {
  const text = "前次合成结果😀";
  return {
    getResultDetail: async () => ({ tenant_id: props.tenantId, company_id: props.companyId, workspace_id: props.workspaceId,
      reference_id: `task:${taskRef}`, kind: "RESULT", source_work_ref: workRef, artifacts: [] }),
    getAgentCandidateSource: async () => ({ tenant_id: props.tenantId, company_id: props.companyId, workspace_id: props.workspaceId,
      work_ref: workRef, task_ref: taskRef, text, text_sha256: createHash("sha256").update(text).digest("hex"),
      task_output_sha256: "3".repeat(64), content_verification: "UNVERIFIED" }),
  };
}
async function choosePrior(h, props, taskRef) {
  let tree = h.render(props);
  const button = agentNodes(tree).find((node) => node.type === "button" && node.key === "candidate-" + taskRef);
  assert.ok(button); await button.props.onClick(); tree = h.render(props);
  workflowButton(tree, "选择全文").props.onClick(); tree = h.render(props);
  await workflowButton(tree, "使用所选文字作为续作依据").props.onClick();
  return h.render(props);
}
test("pending scope blocks execution before hydration and after context changes", async () => {
  let calls = 0;
  const h = agentHarness({ createAssignedWork: async () => { calls++; } });
  let tree = h.render(agentProps, false);
  let button = workflowButton(tree, "交给 Agent 执行"); assert.equal(button.props.disabled, true);
  await button.props.onClick(); assert.equal(calls, 0);
  h.flush(); tree = h.render(agentProps);
  agentNodes(tree).find((n) => n.type === "select").props.onChange({ target: { value: "binding-a" } });
  tree = h.render(agentProps); button = workflowButton(tree, "交给 Agent 执行"); assert.equal(button.props.disabled, false);
  const other = { ...agentProps, contextKey: "content:content-b", source: { ...agentProps.source, content_ref: "content-b" } };
  const changed = h.render(other, false); assert.equal(workflowButton(changed, "交给 Agent 执行").props.disabled, true);
  await button.props.onClick(); assert.equal(calls, 0);
});
test("pending scope rejects foreign payload and preserves legacy bytes", async () => {
  for (const kind of ["content-growth", "writing", "music"]) {
    const source = kind === "content-growth" ? agentProps.source : kind === "writing"
      ? { kind, book_ref: "book", chapter_ref: "chapter" } : { kind, song_ref: "song" };
    const props = { ...agentProps, source, contextKey: contextFor(source) }, key = JSON.stringify(["curis.agent-work", props.tenantId, props.companyId, props.workspaceId, props.assignmentRef, props.contextKey]);
    const payload = { request_id: "old-request", agent_binding_ref: "binding-a", source };
    const foreign = { ...source, ...(kind === "content-growth" ? { content_ref: "other" } : kind === "writing" ? { chapter_ref: "other" } : { song_ref: "other" }) };
    for (const data of [JSON.stringify({ payload }), JSON.stringify({ ...scopedPending(props, payload), payload: { ...payload, source: foreign } }), "{bad", "null", "false", "0", ""]) {
      const storage = new Map([[key, data]]); let calls = 0;
      const h = agentHarness({ createAssignedWork: async () => { calls++; } }, storage);
      h.render(props); const tree = h.render(props);
      const button = workflowButton(tree, "核对并继续原创建请求"); assert.equal(button.props.disabled, true);
      await button.props.onClick(); assert.equal(calls, 0); assert.equal(storage.get(key), data);
      assert.match(JSON.stringify(tree), /核验|负责人/);
    }
  }
});
test("pending scope requires server source proof for a saved Work and recovers provable legacy successor", async () => {
  const key = JSON.stringify(["curis.agent-work", agentProps.tenantId, agentProps.companyId, agentProps.workspaceId, agentProps.assignmentRef, agentProps.contextKey]);
  const bytes = JSON.stringify({ work_ref: "work-root" });
  for (const verified of [false, true]) {
    const storage = new Map([[key, bytes]]), work = { entity_id: "work-child", company_id: agentProps.companyId, workspace_id: agentProps.workspaceId };
    const h = agentHarness({ getOriginalAgentWork: async () => ({ tenant_id: agentProps.tenantId, root_work_ref: "work-root",
      work: verified ? provenWork(work, agentProps) : work, origin: verified ? provenOrigin(agentProps) : { status: "UNKNOWN" },
      tasks: [{ task_id: "task", status: "COMPLETED", result_ref: "task:task" }] }) }, storage);
    h.render(agentProps); await Promise.resolve(); const tree = h.render(agentProps);
    assert.equal(workflowButton(tree, "核对并回填原对象候选").props.disabled, !verified);
    assert.equal(storage.get(key), bytes);
    if (!verified) assert.match(JSON.stringify(tree), /来源无法完整核验/);
  }
});
test("pending scope rereads latest Work before saving or sending follow-up", async () => {
  const key = JSON.stringify(["curis.agent-work", agentProps.tenantId, agentProps.companyId, agentProps.workspaceId, agentProps.assignmentRef, agentProps.contextKey]);
  const bytes = JSON.stringify({ ...scopedPending(agentProps), work_ref: "work-root" });
  const work = { entity_id: "work-root", company_id: agentProps.companyId, workspace_id: agentProps.workspaceId };
  const initial = { tenant_id: agentProps.tenantId, root_work_ref: "work-root", work, origin: provenOrigin(agentProps),
    tasks: [{ task_id: "task-original", status: "COMPLETED", result_ref: "task:task-original" }] };
  for (const changed of [
    { ...initial, origin: { status: "UNKNOWN" } },
    { ...initial, origin: { ...provenOrigin(agentProps), source: { kind: "content-growth", content_ref: "foreign" } } },
    { ...initial, work: { ...work, entity_id: "other-work" } },
    { ...initial, root_work_ref: "foreign-root" },
    { ...initial, tasks: [{ task_id: "other-task", status: "COMPLETED" }] },
    { ...initial, tasks: [{ task_id: "task-original", status: "FAILED", reason_code: "outcome_unknown" }] },
  ]) {
    let reads = 0, continuations = 0, executions = 0;
    const storage = new Map([[key, bytes]]), h = agentHarness({
      getOriginalAgentWork: async () => ++reads === 1 ? initial : changed,
      continueOriginalAgentWork: async () => { continuations++; }, executeOriginalAgentWork: async () => { executions++; },
      ...priorTextApi(agentProps, "work-root", "task-original"),
    }, storage);
    h.render(agentProps); await Promise.resolve(); let tree = await choosePrior(h, agentProps, "task-original");
    const button = workflowButton(tree, "认可所选成果并沿原工作继续"); assert.equal(button.props.disabled, false);
    await button.props.onClick(); tree = h.render(agentProps);
    assert.deepEqual([reads, continuations, executions], [2, 0, 0]); assert.equal(storage.get(key), bytes);
    assert.match(JSON.stringify(tree), /已变化或尚未核验/);
  }
});
test("pending scope rejects a late workflow response before new-context effects", async () => {
  let release;
  const h = agentHarness({ getAssignedAgentWorkflow: () => new Promise((resolve) => { release = resolve; }) });
  h.render(agentProps); let tree = h.render(agentProps);
  const pending = workflowButton(tree, "核对责任流程").props.onClick();
  const next = { ...agentProps, contextKey: "content:content-b", source: { ...agentProps.source, content_ref: "content-b" } };
  h.render(next, false); release(workflowBasis("NEEDS_PUBLICATION")); await pending; h.flush(); tree = h.render(next);
  assert.equal(agentNodes(tree).some((item) => item.type === "button" && item.props.children === "确认发布当前责任流程"), false);
});
test("pending scope preserves a local change while workflow lookup is in flight", async () => {
  let release, created = 0;
  const storage = new Map(), h = agentHarness({ getAssignedAgentWorkflow: () => new Promise((resolve) => { release = resolve; }),
    createAssignedWork: async () => { created++; } }, storage);
  h.render(agentProps); let tree = h.render(agentProps);
  agentNodes(tree).find((node) => node.type === "select").props.onChange({ target: { value: "binding-a" } });
  tree = h.render(agentProps); const pending = workflowButton(tree, "交给 Agent 执行").props.onClick();
  const key = JSON.stringify(["curis.agent-work", agentProps.tenantId, agentProps.companyId, agentProps.workspaceId, agentProps.assignmentRef, agentProps.contextKey]);
  storage.set(key, "foreign bytes"); release(workflowBasis("READY")); await pending;
  assert.equal(created, 0); assert.equal(storage.get(key), "foreign bytes");
});
test("pending scope accepts bound original version and blocks changed local bytes", async () => {
  const oldSource = { ...agentProps.source, expected_version_ref: "old-version" };
  const payload = { request_id: "old", agent_binding_ref: "binding-a", source: oldSource };
  const key = JSON.stringify(["curis.agent-work", agentProps.tenantId, agentProps.companyId, agentProps.workspaceId, agentProps.assignmentRef, agentProps.contextKey]);
  const saved = JSON.stringify(scopedPending(agentProps, payload)), storage = new Map([[key, saved]]); let calls = 0;
  const h = agentHarness({ createAssignedWork: async () => { calls++; } }, storage);
  h.render(agentProps); let tree = h.render(agentProps); let button = workflowButton(tree, "核对并继续原创建请求");
  assert.equal(button.props.disabled, true);
  await button.props.onClick(); assert.equal(calls, 0); assert.equal(storage.get(key), saved);
});

test("Agent explicit Work preserves its source and cold read cannot start a second execution", async () => {
  let executed = 0, submitted;
  const storage = new Map(), original = { tenant_id: "tenant-a", work: { entity_id: "work-a", company_id: "company-a", workspace_id: "workspace-a" } };
  const api = { createAssignedWork: async (assignment, payload) => { submitted = { assignment, payload }; return { work: original.work }; },
    getOriginalAgentWork: async () => ({ ...original, origin: provenOrigin(agentProps), tasks: executed ? [{ task_id: "task-a", status: "COMPLETED", call_reserved: true }] : [] }),
    executeOriginalAgentWork: async () => { executed++; } };
  const harness = agentHarness(api, storage);
  let tree = harness.render(agentProps); tree = harness.render(agentProps);
  agentNodes(tree).find((n) => n.type === "select").props.onChange({ target: { value: "binding-a" } });
  tree = harness.render(agentProps);
  const start = agentNodes(tree).find((n) => n.type === "button" && n.props.children === "交给 Agent 执行");
  assert.equal(start.props.disabled, false);
  await start.props.onClick();
  assert.equal(executed, 1); assert.equal(submitted.assignment, "assignment-a");
  assert.equal(JSON.stringify(submitted.payload.source), JSON.stringify(agentProps.source));
  tree = harness.render(agentProps);
  await agentNodes(tree).find((n) => n.type === "button" && n.props.children === "读取原工作").props.onClick();
  const cold = agentHarness(api, storage); cold.render(agentProps); await Promise.resolve(); cold.render(agentProps);
  assert.equal(executed, 1);
});

test("Cancelled Agent Work reports a stop request without claiming process exit", async () => {
  const key = JSON.stringify(["curis.agent-work", "tenant-a", "company-a", "workspace-a", "assignment-a", "content:content-a"]);
  const storage = new Map([[key, JSON.stringify({ work_ref: "work-a" })]]);
  const harness = agentHarness({ getOriginalAgentWork: async () => ({
    tenant_id: "tenant-a", work: { entity_id: "work-a", company_id: "company-a", workspace_id: "workspace-a" },
    tasks: [{ task_id: "task-a", status: "CANCELLED" }],
  }) }, storage);
  harness.render(agentProps);
  await Promise.resolve();
  const tree = harness.render(agentProps);
  const messages = agentNodes(tree).filter((node) => node.props?.role === "status").map((node) => node.props.children);
  assert.ok(messages.includes("已请求停止；外部进程和效果仍需核验"));
  assert.ok(!messages.includes("原工作已停止；外部效果仍需核验"));
});

test("Unknown Agent outcome remains visible and cannot be continued", async () => {
  const key = JSON.stringify(["curis.agent-work", "tenant-a", "company-a", "workspace-a", "assignment-a", "content:content-a"]);
  const storage = new Map([[key, JSON.stringify({ work_ref: "work-a" })]]);
  const harness = agentHarness({ getOriginalAgentWork: async () => ({
    tenant_id: "tenant-a", work: { entity_id: "work-b", company_id: "company-a", workspace_id: "workspace-a" },
    tasks: [{ task_id: "task-b", status: "FAILED", reason_code: "outcome_unknown", call_reserved: false }],
    history: [
      { work: { entity_id: "work-a" }, tasks: [{ task_id: "task-a", status: "COMPLETED" }] },
      { work: { entity_id: "work-b" }, tasks: [{ task_id: "task-b", status: "FAILED", reason_code: "outcome_unknown", call_reserved: false }] },
    ],
  }) }, storage);
  harness.render(agentProps);
  await Promise.resolve();
  const nodes = agentNodes(harness.render(agentProps));
  assert.ok(nodes.some((node) => node.props?.role === "status" && node.props.children === "执行状态和外部效果仍需核验，不能重复启动。"));
  assert.ok(!nodes.some((node) => node.type === "button" && node.props.children === "修复后继续原工作"));
});

for (const scenario of ["verified", "missing", "conflict", "missing_history", "empty_history", "other_work", "other_task"]) {
  test(`Agent local child status is shown only with consistent evidence: ${scenario}`, async () => {
    const key = JSON.stringify(["curis.agent-work", "tenant-a", "company-a", "workspace-a", "assignment-a", "content:content-a"]);
    const storage = new Map([[key, JSON.stringify({ work_ref: "work-a" })]]);
    const work = { entity_id: "work-a", company_id: "company-a", workspace_id: "workspace-a" };
    const task = { task_id: "task-a", status: "CANCELLED", reason_code: "outcome_unknown",
      ...(scenario === "missing" ? {} : { local_process_state: "DIRECT_CHILD_REAPED" }) };
    const history = scenario === "missing_history" ? undefined : scenario === "empty_history" ? [] : [{
      work: scenario === "other_work" ? { ...work, entity_id: "work-b" } : work,
      tasks: [{ ...task, ...(scenario === "conflict" ? { local_process_state: "UNKNOWN" } : {}),
        ...(scenario === "other_task" ? { task_id: "task-b" } : {}) }],
    }];
    const harness = agentHarness({ getOriginalAgentWork: async () => ({ tenant_id: "tenant-a", work, tasks: [task], history }) }, storage);
    harness.render(agentProps);
    await Promise.resolve();
    const nodes = agentNodes(harness.render(agentProps));
    const local = nodes.filter((node) => node.props?.role === "status" &&
      node.props.children === "受控直接子进程已退出；其他进程和外部效果仍待核验。");
    assert.equal(local.length, scenario === "verified" ? 1 : 0);
    assert.ok(nodes.some((node) => node.props?.role === "status" &&
      node.props.children === "执行状态和外部效果仍需核验，不能重复启动。"));
    assert.ok(!nodes.some((node) => node.type === "button" && node.props.children === "修复后继续原工作"));
  });
}

test("Agent rechecks original Work after an outcome becomes unknown", async () => {
  const key = JSON.stringify(["curis.agent-work", "tenant-a", "company-a", "workspace-a", "assignment-a", "content:content-a"]);
  const storage = new Map([[key, JSON.stringify({ work_ref: "work-a" })]]);
  let reads = 0, executions = 0;
  const harness = agentHarness({
    getOriginalAgentWork: async () => ({ tenant_id: "tenant-a",
      work: { entity_id: "work-a", company_id: "company-a", workspace_id: "workspace-a" },
      tasks: [{ task_id: "task-a", status: "FAILED", call_reserved: false,
        reason_code: ++reads > 1 ? "outcome_unknown" : null }] }),
    executeOriginalAgentWork: async () => { executions++; },
  }, storage);
  harness.render(agentProps);
  await Promise.resolve();
  const tree = harness.render(agentProps);
  const resume = agentNodes(tree).find((node) => node.type === "button" && node.props.children === "修复后继续原工作");
  assert.ok(resume);
  await resume.props.onClick();
  assert.equal(executions, 0);
});

test("Agent cannot execute after an original Work read crosses tenant scope", async () => {
  let executed = 0;
  const harness = agentHarness({ createAssignedWork: async () => ({ work: { entity_id: "work-a" } }),
    getOriginalAgentWork: async () => ({ tenant_id: "other-tenant", work: { company_id: "company-a", workspace_id: "workspace-a" }, tasks: [] }),
    executeOriginalAgentWork: async () => { executed++; } });
  harness.render(agentProps); let tree = harness.render(agentProps);
  agentNodes(tree).find((n) => n.type === "select").props.onChange({ target: { value: "binding-a" } });
  tree = harness.render(agentProps);
  await agentNodes(tree).find((n) => n.type === "button" && n.props.children === "交给 Agent 执行").props.onClick();
  tree = harness.render(agentProps);
  assert.equal(executed, 0);
  assert.match(agentNodes(tree).find((n) => n.props?.role === "alert").props.children, /不属于当前公司/);
});

test("Explicit Agent follow-up keeps root history and a cold reload never replays it", async () => {
  let calls = 0, childCreated = false, submitted;
  const rootWork = provenWork({ entity_id: "work-root", company_id: "company-a", workspace_id: "workspace-a" }, agentProps);
  const childWork = { ...rootWork, entity_id: "work-child" };
  const first = { task_id: "task-root", status: "COMPLETED", result_ref: "task:task-root" };
  const key = JSON.stringify(["curis.agent-work", "tenant-a", "company-a", "workspace-a", "assignment-a", "content:content-a"]);
  const storage = new Map([[key, JSON.stringify({ ...scopedPending(agentProps), work_ref: "work-root" })]]);
  const api = {
    ...priorTextApi(agentProps, "work-root", "task-root"),
    continueOriginalAgentWork: async (parent, payload) => {
      submitted = { parent, payload }; childCreated = true; return { work: childWork };
    },
    getOriginalAgentWork: async () => {
      const tasks = calls ? [{ task_id: "task-child", status: "COMPLETED", result_ref: "task:task-child" }] : [];
      return { tenant_id: "tenant-a", root_work_ref: "work-root", origin: provenOrigin(agentProps),
        work: childCreated ? childWork : rootWork, tasks: childCreated ? tasks : [first],
        history: [{ work: rootWork, tasks: [first] }, ...(childCreated ? [{ work: childWork, tasks }] : [])] };
    },
    executeOriginalAgentWork: async (work) => { assert.equal(work, "work-child"); calls++; },
  };
  const props = { ...agentProps, body: "继续补充新的建议", source: { ...agentProps.source, expected_version_ref: "version-fresh" } };
  const harness = agentHarness(api, storage); harness.render(props); await Promise.resolve();
  let tree = harness.render(props);
  assert.equal(calls, 0);
  assert.equal(workflowButton(tree, "认可所选成果并沿原工作继续").props.disabled, true);
  tree = await choosePrior(harness, props, "task-root");
  await workflowButton(tree, "认可所选成果并沿原工作继续").props.onClick();
  assert.equal(submitted.parent, "work-root");
  assert.equal(submitted.payload.accepted_task_ref, "task-root");
  assert.equal(submitted.payload.accept_result, true);
  assert.equal(submitted.payload.source.expected_version_ref, "version-fresh");
  assert.equal(submitted.payload.prior_result.mode, "result");
  assert.equal(calls, 1);
  assert.equal(JSON.parse(storage.get(key)).work_ref, "work-root");
  const cold = agentHarness(api, storage); cold.render(props); await Promise.resolve(); tree = cold.render(props);
  assert.equal(calls, 1);
  assert.equal(agentNodes(tree).filter((node) => node.type === "button" && Array.isArray(node.props.children)
    && node.props.children[0] === "查看第 ").length, 2);
});

function renderedSubmit(props = {}) {
  const html = renderToStaticMarkup(React.createElement(ConversationComposer, { value: "讨论正文", ...props }));
  const matches = [...html.matchAll(/<button([^>]*type="submit"[^>]*)>([^<]*)<\/button>/g)];
  assert.equal(matches.length, 1);
  const [, attributes, label] = matches[0];
  const style = attributes.match(/style="([^"]*)"/)?.[1];
  assert.ok(style, "send colors must outrank normal business button resets");
  const colors = Object.fromEntries(postcss.parse(`button { ${style} }`).first.nodes.map(({ prop, value }) => [prop, value]));
  assert.equal(colors.background, "var(--ui-action-primary-bg)");
  assert.equal(colors.color, "var(--ui-action-primary-fg)");
  assert.match(attributes, /disabled:opacity-40/);
  return { attributes, label, colors };
}

for (const submitLabel of ["发送", "发送给负责员工", "发送一次建议请求", "请求文字建议"]) {
  for (const [state, props, disabled] of [
    ["ready", {}, false], ["unavailable", { disabled: true }, true],
    ["busy", { busy: true }, true], ["blank", { value: "  \n " }, true],
  ]) test(`shared ${submitLabel} renders primary colors and truthful ${state} state`, () => {
    const button = renderedSubmit({ submitLabel, ...props });
    assert.equal(/\sdisabled=""/.test(button.attributes), disabled);
    assert.equal(button.label, props.busy ? "处理中…" : submitLabel);
  });
}

// Inspect emitted inline colors and actual CSS declarations; this is not a browser cascade simulation.
for (const [business, path, selector] of [
  ["content growth", "components/content-growth/ContentGrowth.module.css", ".main button"],
  ["writing", "components/writing/Writing.module.css", ".workspace button"],
  ["music", "components/music/Music.module.css", ".main button"],
]) test(`${business} parent button colors remain normal-priority beneath composer inline colors`, () => {
  const resets = [];
  postcss.parse(read(path)).walkRules((rule) => {
    if (rule.selectors.includes(selector)) rule.walkDecls(/^(background|background-color|color)$/, (decl) => resets.push(decl));
  });
  assert.ok(resets.some(({ prop }) => prop === "background"));
  assert.ok(resets.every(({ important }) => !important));
  renderedSubmit();
});

for (const theme of ["light", "dark"]) test(`composer colors resolve through existing ${theme} action tokens`, () => {
  const rule = postcss.parse(read("app/globals.css")).nodes.find((node) => node.type === "rule" && node.selectors.includes(`[data-theme="${theme}"]`));
  assert.ok(rule);
  const tokens = Object.fromEntries(rule.nodes.filter((node) => node.type === "decl").map(({ prop, value }) => [prop, value]));
  const { colors } = renderedSubmit();
  const background = tokens[colors.background.slice(4, -1)], foreground = tokens[colors.color.slice(4, -1)];
  assert.match(background, /^#[\da-f]{6}$/i);
  assert.match(foreground, /^#[\da-f]{6}$/i);
  assert.notEqual(background, foreground);
  assert.notEqual(background, tokens["--ui-surface"]);
});

test("composer keeps submit delegation and input updates unchanged", () => {
  const submit = () => { throw new Error("render must not send"); };
  let changed;
  const form = ConversationComposer({ value: "原文", onSubmit: submit, onChange: (value) => { changed = value; } });
  assert.equal(form.props.onSubmit, submit);
  const textarea = React.Children.toArray(form.props.children).find((child) => child.type === "textarea");
  textarea.props.onChange({ target: { value: "修改后的讨论" } });
  assert.equal(changed, "修改后的讨论");
});


function workflowBasis(state = "NEEDS_PUBLICATION", extra = {}) {
  return { tenant_id: "tenant-a", company_id: "company-a", workspace_id: "workspace-a", assignment_ref: "assignment-a",
    assignment_revision: 3, review_token: "a".repeat(64), employee_name: "原员工", role_name: "原责任",
    responsibility: "处理原选段", scope_type: "WORKSPACE", scope_ref: "workspace-a", workspace_name: "原业务",
    matching_count: state === "READY" ? 1 : state === "AMBIGUOUS" ? 2 : 0, state,
    reason: state === "READY" ? "已读取唯一流程，请单独继续" : state === "AMBIGUOUS" ? "存在多个流程" : "请确认发布",
    publication_allowed: state === "NEEDS_PUBLICATION", ...extra };
}
function workflowButton(tree, label) {
  const node = agentNodes(tree).find((item) => item.type === "button" && item.props.children === label);
  assert.ok(node, label); return node;
}
function originalPending(props = agentProps) {
  const key = JSON.stringify(["curis.agent-work", props.tenantId, props.companyId, props.workspaceId, props.assignmentRef, props.contextKey]);
  const payload = { request_id: "retained-original-uuid", problem: "原请求正文", expected_result: "原期望成果",
    agent_binding_ref: "binding-a", browser_hosts: [], source: props.source };
  return { key, payload, storage: new Map([[key, JSON.stringify(scopedPending(props, payload))]]) };
}
for (const kind of ["content-growth", "writing", "music"]) {
  test(kind + " publication preserves a same-session request and cold unknown is not replayed", async () => {
    const props = { ...agentProps, source: businessSource(kind), contextKey: contextFor(businessSource(kind)) };
    const key = JSON.stringify(["curis.agent-work", props.tenantId, props.companyId, props.workspaceId, props.assignmentRef, props.contextKey]);
    const storage = new Map(); let reads = 0, publications = 0, created = 0, executed = 0, ready = false;
    const original = { tenant_id: props.tenantId, work: { entity_id: "work-a", company_id: props.companyId, workspace_id: props.workspaceId } };
    const api = {
      getAssignedAgentWorkflow: async () => { reads++; return workflowBasis(ready ? "READY" : "NEEDS_PUBLICATION"); },
      publishAssignedAgentWorkflow: async () => { publications++; ready = true; return workflowBasis("READY"); },
      createAssignedWork: async () => { created++; return original; },
      getOriginalAgentWork: async () => ({ ...original, origin: provenOrigin(props), tasks: executed ? [{ status: "COMPLETED", call_reserved: true }] : [] }),
      executeOriginalAgentWork: async () => { executed++; },
    };
    const harness = agentHarness(api, storage); harness.render(props); let tree = harness.render(props);
    agentNodes(tree).find((item) => item.type === "select").props.onChange({ target: { value: "binding-a" } });
    tree = harness.render(props); await workflowButton(tree, "交给 Agent 执行").props.onClick(); tree = harness.render(props);
    const before = storage.get(key); assert.ok(before); assert.deepEqual([created, executed], [0, 0]);
    await workflowButton(tree, "核对责任流程").props.onClick(); tree = harness.render(props);
    agentNodes(tree).find((item) => item.type === "input" && item.props.type === "checkbox").props.onChange({ target: { checked: true } });
    tree = harness.render(props); await workflowButton(tree, "确认发布当前责任流程").props.onClick(); tree = harness.render(props);
    assert.deepEqual([publications, created, executed], [1, 0, 0]); assert.equal(storage.get(key), before);
    const cold = agentHarness(api, storage); cold.render(props); const coldTree = cold.render(props);
    assert.equal(workflowButton(coldTree, "核对并继续原创建请求").props.disabled, true);
    await workflowButton(coldTree, "核对并继续原创建请求").props.onClick();
    assert.deepEqual([publications, created, executed], [1, 0, 0]); assert.equal(storage.get(key), before);
    await workflowButton(tree, "核对并继续原创建请求").props.onClick();
    assert.deepEqual([publications, created, executed], [1, 1, 1]);
  });
}
test("ambiguous or stale workflow cannot create Work or offer publication", async () => {
  for (const state of ["AMBIGUOUS", "STALE"]) {
    const { key, storage } = originalPending(), before = storage.get(key); let created = 0;
    const harness = agentHarness({ getAssignedAgentWorkflow: async () => workflowBasis(state),
      createAssignedWork: async () => { created++; } }, storage);
    harness.render(agentProps); let tree = harness.render(agentProps);
    await workflowButton(tree, "核对并继续原创建请求").props.onClick(); tree = harness.render(agentProps);
    assert.equal(created, 0); assert.equal(storage.get(key), before);
    assert.equal(agentNodes(tree).some((item) => item.type === "button" && item.props.children === "确认发布当前责任流程"), false);
  }
});
test("lost publication response permits readback and never replays original creation", async () => {
  const storage = new Map(); let published = false, writes = 0, created = 0;
  const harness = agentHarness({ getAssignedAgentWorkflow: async () => workflowBasis(published ? "READY" : "NEEDS_PUBLICATION"),
    publishAssignedAgentWorkflow: async () => { writes++; published = true; throw new Error("响应丢失"); },
    createAssignedWork: async () => { created++; } }, storage);
  harness.render(agentProps); let tree = harness.render(agentProps);
  await workflowButton(tree, "核对责任流程").props.onClick(); tree = harness.render(agentProps);
  agentNodes(tree).find((item) => item.type === "input" && item.props.type === "checkbox").props.onChange({ target: { checked: true } });
  tree = harness.render(agentProps); await workflowButton(tree, "确认发布当前责任流程").props.onClick(); tree = harness.render(agentProps);
  assert.equal(agentNodes(tree).some((item) => item.type === "button" && item.props.children === "确认发布当前责任流程"), false);
  await workflowButton(tree, "核对责任流程").props.onClick(); harness.render(agentProps);
  assert.deepEqual([writes, created], [1, 0]); assert.equal(storage.size, 0);
});
test("late workflow response cannot cross workspace and a mismatched tenant cannot authorize publication", async () => {
  let release;
  const harness = agentHarness({ getAssignedAgentWorkflow: () => new Promise((resolve) => { release = resolve; }) });
  harness.render(agentProps); let tree = harness.render(agentProps);
  const pending = workflowButton(tree, "核对责任流程").props.onClick();
  const other = { ...agentProps, workspaceId: "workspace-b", assignmentRef: "assignment-b", contextKey: "content:content-b" };
  harness.render(other); release(workflowBasis()); await pending; tree = harness.render(other);
  assert.equal(agentNodes(tree).some((item) => item.type === "button" && item.props.children === "确认发布当前责任流程"), false);
  const wrong = agentHarness({ getAssignedAgentWorkflow: async () => workflowBasis("NEEDS_PUBLICATION", { tenant_id: "foreign" }) });
  wrong.render(agentProps); tree = wrong.render(agentProps);
  await workflowButton(tree, "核对责任流程").props.onClick(); tree = wrong.render(agentProps);
  assert.match(agentNodes(tree).find((item) => item.props?.role === "alert").props.children, /不属于/);
  assert.equal(agentNodes(tree).some((item) => item.type === "button" && item.props.children === "确认发布当前责任流程"), false);
});
test("unverified local pending data cannot be overwritten by a new request", async () => {
  const { key, storage } = originalPending(); storage.set(key, "{broken");
  let created = 0;
  const harness = agentHarness({ createAssignedWork: async () => { created++; } }, storage);
  harness.render(agentProps); let tree = harness.render(agentProps);
  await workflowButton(tree, "核对并继续原创建请求").props.onClick();
  assert.equal(created, 0); assert.equal(storage.get(key), "{broken");
});


test("cold pending details show cached Agent, expectation and source even when current bindings changed", async () => {
  const source = { kind: "writing", book_ref: "book-original", chapter_ref: "chapter-original",
    expected_draft_ref: "draft-original", selection: { draft_ref: "draft-original", sha256: "f".repeat(64), start: 0, end: 144, excerpt: "原选段" } };
  for (const agents of [[], [{ binding_id: "different-binding", display_name: "另一个 Agent" }]]) {
    const props = { ...agentProps, source, contextKey: contextFor(source), agents };
    const { key, storage } = originalPending(props); const before = storage.get(key);
    let created = 0, reads = 0;
    const harness = agentHarness({ createAssignedWork: async () => { created++; },
      getAssignedAgentWorkflow: async () => { reads++; return workflowBasis("READY"); } }, storage);
    harness.render(props); let tree = harness.render(props);
    const text = JSON.stringify(tree);
    for (const expected of ["binding-a", "原期望成果", "book-original", "chapter-original", "draft-original",
      "0–144", "f".repeat(64), "当前绑定列表无法核验名称", "原业务包版本", "原请求未提供"]) assert.ok(text.includes(expected), expected);
    assert.equal(agentNodes(tree).find((item) => item.type === "select").props.value, "binding-a");
    const button = workflowButton(tree, "核对并继续原创建请求");
    assert.equal(button.props.disabled, true);
    await button.props.onClick();
    assert.deepEqual([created, reads], [0, 0]); assert.equal(storage.get(key), before);
    tree = harness.render(props); assert.ok(JSON.stringify(tree).includes("retained-original-uuid"));
  }
});

const fileHash = (text) => createHash("sha256").update(text).digest("hex");
const fileBody = "章😀节正文", fileNotes = "核对说明，不是章节正文";
const candidateFiles = [
  { artifact_id: "notes-file", artifact_type: "agent_file_receipt", title: "revision-notes.md", content_sha256: "1".repeat(64) },
  { artifact_id: "body-file", artifact_type: "agent_file_receipt", title: "chapter-candidate.md", content_sha256: "2".repeat(64) },
];
function candidateDetail(props, files = candidateFiles) {
  return { tenant_id: props.tenantId, company_id: props.companyId, workspace_id: props.workspaceId,
    reference_id: "task:task-original", kind: "RESULT", source_work_ref: "work-original", artifacts: files,
    summary: "已经完成，请查收。", result_version: "result-version-original" };
}
function candidateProof(props, artifact) {
  const file = candidateFiles.find((item) => item.artifact_id === artifact);
  const text = file ? artifact === "body-file" ? fileBody : fileNotes : "无文件的完整文字成果";
  return { tenant_id: props.tenantId, company_id: props.companyId, workspace_id: props.workspaceId,
    work_ref: "work-original", task_ref: "task-original", source_kind: props.source.kind,
    content_verification: "UNVERIFIED", text, text_sha256: fileHash(text), task_output_sha256: "3".repeat(64),
    ...(file ? { artifact_ref: artifact, artifact_content_sha256: file.content_sha256,
      file_sha256: fileHash(text), file_bytes: Buffer.byteLength(text), filename: file.title,
      task_output_sha256: "3".repeat(64) } : {}) };
}
async function candidateHarness(props = agentProps, overrides = {}, files = candidateFiles) {
  const key = JSON.stringify(["curis.agent-work", props.tenantId, props.companyId, props.workspaceId, props.assignmentRef, props.contextKey]);
  const storage = new Map([[key, JSON.stringify({ ...scopedPending(props), work_ref: "work-original" })]]);
  const original = storage.get(key), calls = { executions: 0, creations: 0, previews: [], saved: [] };
  const api = {
    getOriginalAgentWork: async () => ({ tenant_id: props.tenantId, origin: provenOrigin(props),
      work: provenWork({ entity_id: "work-original", company_id: props.companyId, workspace_id: props.workspaceId }, props),
      tasks: [{ task_id: "task-original", status: "COMPLETED", call_reserved: true, result_ref: "task:task-original" }] }),
    getResultDetail: async (company, workspace, reference) => {
      assert.deepEqual([company, workspace, reference], [props.companyId, props.workspaceId, "task:task-original"]);
      return candidateDetail(props, files);
    },
    getAgentCandidateSource: async (work, task, artifact) => {
      calls.previews.push([work, task, artifact]);
      assert.deepEqual([work, task], ["work-original", "task-original"]);
      return candidateProof(props, artifact);
    },
    createAgentCandidate: async (work, payload) => { calls.saved.push([work, JSON.parse(JSON.stringify(payload))]); },
    executeOriginalAgentWork: async () => { calls.executions++; },
    createAssignedWork: async () => { calls.creations++; },
    ...overrides,
  };
  const harness = agentHarness(api, storage); harness.render(props); await Promise.resolve();
  let tree = harness.render(props);
  await workflowButton(tree, "核对并回填原对象候选").props.onClick();
  return { harness, calls, storage, key, original, props, render: () => harness.render(props) };
}
const filePicker = (tree) => agentNodes(tree).find((node) => node.props?.["aria-label"] === "选择要回填的原成果文件");
const fileTextarea = (tree) => agentNodes(tree).find((node) => node.props?.["aria-label"] === "原成果正文，可选择回填范围");

test("candidate range requires explicit confirmation and survives collapsed selection until cleared", async () => {
  const run = await candidateHarness(); let tree = run.render();
  await filePicker(tree).props.onChange({ target: { value: "body-file" } }); tree = run.render();
  assert.equal(workflowButton(tree, "保存为原对象候选").props.disabled, true);
  assert.equal(workflowButton(tree, "使用所选文字作为续作依据").props.disabled, true);
  fileTextarea(tree).props.onSelect({ target: { selectionStart: 1, selectionEnd: 3 } }); tree = run.render();
  assert.equal(workflowButton(tree, "保存为原对象候选").props.disabled, true);
  workflowButton(tree, "确认所选片段").props.onClick(); tree = run.render();
  assert.match(JSON.stringify(tree), /😀/);
  fileTextarea(tree).props.onSelect({ target: { selectionStart: 3, selectionEnd: 3 } }); tree = run.render();
  assert.equal(workflowButton(tree, "保存为原对象候选").props.disabled, false);
  workflowButton(tree, "清除选择").props.onClick(); tree = run.render();
  assert.equal(workflowButton(tree, "保存为原对象候选").props.disabled, true);
  assert.equal(run.calls.saved.length, 0);
});

test("collapsed draft cannot confirm old full text and a new range confirms exactly", async () => {
  const run = await candidateHarness(); let tree = run.render();
  await filePicker(tree).props.onChange({ target: { value: "body-file" } }); tree = run.render();
  fileTextarea(tree).props.onSelect({ target: { selectionStart: 0, selectionEnd: fileBody.length } }); tree = run.render();
  const staleConfirm = workflowButton(tree, "确认所选片段");
  assert.equal(staleConfirm.props.disabled, false);
  fileTextarea(tree).props.onSelect({ target: { selectionStart: 0, selectionEnd: 0 } }); tree = run.render();
  assert.equal(workflowButton(tree, "确认所选片段").props.disabled, true);
  staleConfirm.props.onClick(); tree = run.render();
  assert.equal(workflowButton(tree, "保存为原对象候选").props.disabled, true);
  fileTextarea(tree).props.onSelect({ target: { selectionStart: 1, selectionEnd: 3 } }); tree = run.render();
  workflowButton(tree, "确认所选片段").props.onClick(); tree = run.render();
  await workflowButton(tree, "保存为原对象候选").props.onClick();
  assert.deepEqual([run.calls.saved[0][1].start, run.calls.saved[0][1].end, run.calls.saved[0][1].excerpt], [1, 3, "😀"]);
});

test("explicit full file selection saves exact text without filtering", async () => {
  const run = await candidateHarness(); let tree = run.render();
  await filePicker(tree).props.onChange({ target: { value: "notes-file" } }); tree = run.render();
  assert.equal(workflowButton(tree, "保存为原对象候选").props.disabled, true);
  workflowButton(tree, "选择全文").props.onClick(); tree = run.render();
  assert.ok(JSON.stringify(tree).includes(fileNotes));
  await workflowButton(tree, "保存为原对象候选").props.onClick();
  assert.equal(run.calls.saved[0][1].excerpt, fileNotes);
  assert.deepEqual([run.calls.saved[0][1].start, run.calls.saved[0][1].end], [0, fileNotes.length]);
});

test("existing different candidate conflict keeps original and directs user to check it", async () => {
  const run = await candidateHarness(agentProps, { createAgentCandidate: async () => {
    throw new Error("原结果已生成另一份候选，请先核对原候选。");
  } });
  let tree = run.render(); await filePicker(tree).props.onChange({ target: { value: "body-file" } }); tree = run.render();
  workflowButton(tree, "选择全文").props.onClick(); tree = run.render();
  await workflowButton(tree, "保存为原对象候选").props.onClick(); tree = run.render();
  assert.match(JSON.stringify(tree), /请读取原候选核对；不会重新执行 Agent/);
  assert.deepEqual([run.calls.executions, run.calls.creations], [0, 0]);
  assert.equal(run.storage.get(run.key), run.original);
});

test("changed source version invalidates a previously confirmed selection", async () => {
  const run = await candidateHarness(); let tree = run.render();
  await filePicker(tree).props.onChange({ target: { value: "body-file" } }); tree = run.render();
  workflowButton(tree, "选择全文").props.onClick(); tree = run.render();
  const oldSave = workflowButton(tree, "保存为原对象候选");
  const changed = { ...run.props, source: { ...run.props.source, expected_version_ref: "changed-version" } };
  run.harness.render(changed);
  await oldSave.props.onClick();
  assert.equal(run.calls.saved.length, 0);
  assert.equal(fileTextarea(run.harness.render(changed)), undefined);
});

test("late candidate save does not refresh or show success after source version changes", async () => {
  let release, refreshes = 0;
  const calls = [];
  const props = { ...agentProps, onCandidate: () => { refreshes++; } };
  const run = await candidateHarness(props, { createAgentCandidate: (work, payload) => {
    calls.push([work, payload]); return new Promise((resolve) => { release = resolve; });
  } });
  let tree = run.render(); await filePicker(tree).props.onChange({ target: { value: "body-file" } }); tree = run.render();
  workflowButton(tree, "选择全文").props.onClick(); tree = run.render();
  const saving = workflowButton(tree, "保存为原对象候选").props.onClick();
  const changed = { ...props, source: { ...props.source, expected_version_ref: "changed-version" } };
  run.harness.render(changed); release(); await saving; tree = run.harness.render(changed);
  assert.equal(calls.length, 1); assert.equal(refreshes, 0);
  assert.doesNotMatch(JSON.stringify(tree), /已记录到原对象的候选列表/);
});

test("oversize full selection cannot be saved or used for follow-up", async () => {
  const longText = "甲".repeat(11000);
  const run = await candidateHarness(agentProps, { getAgentCandidateSource: async () => ({
    ...candidateProof(agentProps), text: longText, text_sha256: fileHash(longText),
  }) }, []);
  let tree = run.render(); workflowButton(tree, "选择全文").props.onClick(); tree = run.render();
  assert.equal(workflowButton(tree, "保存为原对象候选").props.disabled, true);
  assert.equal(workflowButton(tree, "使用所选文字作为续作依据").props.disabled, true);
  assert.match(JSON.stringify(tree), /32768/); assert.equal(run.calls.saved.length, 0);
});

test("follow-up requires explicit prior file and selected text, retaining uncertain request without replay", async () => {
  let sent = null, calls = 0;
  const run = await candidateHarness(agentProps, { continueOriginalAgentWork: async (parent, payload) => {
    calls++; sent = { parent, payload }; throw new Error("响应未知");
  } });
  let tree = run.render();
  assert.equal(workflowButton(tree, "认可所选成果并沿原工作继续").props.disabled, true);
  await filePicker(tree).props.onChange({ target: { value: "body-file" } }); tree = run.render();
  fileTextarea(tree).props.onSelect({ target: { selectionStart: 1, selectionEnd: 3 } }); tree = run.render();
  workflowButton(tree, "确认所选片段").props.onClick(); tree = run.render();
  workflowButton(tree, "使用所选文字作为续作依据").props.onClick(); tree = run.render();
  assert.match(JSON.stringify(tree), /已选续作依据/);
  await workflowButton(tree, "认可所选成果并沿原工作继续").props.onClick(); tree = run.render();
  assert.equal(calls, 1); assert.equal(sent.parent, "work-original");
  assert.equal(sent.payload.prior_result.mode, "file"); assert.equal(sent.payload.prior_result.artifact_ref, "body-file");
  assert.deepEqual([sent.payload.prior_result.start, sent.payload.prior_result.end], [1, 3]);
  assert.equal(JSON.stringify(sent.payload.prior_result).includes(fileBody), false);
  assert.equal(workflowButton(tree, "认可所选成果并沿原工作继续").props.disabled, true);
  await workflowButton(tree, "认可所选成果并沿原工作继续").props.onClick(); assert.equal(calls, 1);
});
test("follow-up allows explicit result text only when no file was offered", async () => {
  let sent;
  const run = await candidateHarness(agentProps, { continueOriginalAgentWork: async (_parent, payload) => {
    sent = payload; throw new Error("响应未知");
  } }, []);
  let tree = run.render(); assert.equal(filePicker(tree), undefined);
  workflowButton(tree, "选择全文").props.onClick(); tree = run.render();
  workflowButton(tree, "使用所选文字作为续作依据").props.onClick(); tree = run.render();
  await workflowButton(tree, "认可所选成果并沿原工作继续").props.onClick();
  assert.equal(sent.prior_result.mode, "result"); assert.equal(sent.prior_result.artifact_ref, undefined);
});

test("three businesses explicitly select original file and persist UTF16 selection with distinct hashes", async () => {
  for (const kind of ["writing", "content-growth", "music"]) {
    const run = await candidateHarness({ ...agentProps, source: businessSource(kind), contextKey: contextFor(businessSource(kind)) });
    let tree = run.render();
    assert.equal(filePicker(tree).props.value, "");
    assert.equal(fileTextarea(tree), undefined);
    assert.equal(workflowButton(tree, "保存为原对象候选").props.disabled, true);
    assert.equal(run.calls.previews.length, 0);
    await filePicker(tree).props.onChange({ target: { value: "body-file" } }); tree = run.render();
    assert.equal(fileTextarea(tree).props.value, fileBody);
    assert.notEqual(fileTextarea(tree).props.value, fileNotes);
    fileTextarea(tree).props.onSelect({ target: { selectionStart: 1, selectionEnd: 3 } });
    tree = run.render(); workflowButton(tree, "确认所选片段").props.onClick();
    tree = run.render(); await workflowButton(tree, "保存为原对象候选").props.onClick();
    assert.deepEqual(run.calls.saved, [["work-original", { task_ref: "task-original", start: 1, end: 3,
      excerpt: "😀", text_sha256: fileHash(fileBody), artifact_ref: "body-file",
      artifact_content_sha256: "2".repeat(64), file_sha256: fileHash(fileBody), task_output_sha256: "3".repeat(64) }]]);
    assert.notEqual(run.calls.saved[0][1].artifact_content_sha256, run.calls.saved[0][1].file_sha256);
    assert.deepEqual([run.calls.executions, run.calls.creations], [0, 0]);
    assert.equal(run.storage.get(run.key), run.original);
  }
});
test("no-file text compatibility keeps original four text fields and no implicit execution", async () => {
  const run = await candidateHarness(agentProps, {}, []);
  let tree = run.render(); assert.equal(filePicker(tree), undefined);
  assert.equal(fileTextarea(tree).props.value, "无文件的完整文字成果");
  assert.equal(workflowButton(tree, "保存为原对象候选").props.disabled, true);
  workflowButton(tree, "选择全文").props.onClick(); tree = run.render();
  await workflowButton(tree, "保存为原对象候选").props.onClick();
  assert.deepEqual(Object.keys(run.calls.saved[0][1]).sort(), ["end", "excerpt", "start", "task_ref", "text_sha256"]);
  assert.deepEqual([run.calls.executions, run.calls.creations], [0, 0]);
});
test("original file preview rejects foreign identity receipt hash bytes and text hash without enabling save", async () => {
  const changes = [
    { tenant_id: "foreign" }, { company_id: "foreign" }, { workspace_id: "foreign" }, { work_ref: "foreign" },
    { task_ref: "foreign" }, { artifact_ref: "notes-file" }, { artifact_content_sha256: "0".repeat(64) },
    { file_sha256: "0".repeat(64) }, { text_sha256: "0".repeat(64) }, { file_bytes: 1 },
    { task_output_sha256: "invalid" }, { content_verification: "VERIFIED" },
  ];
  for (const change of changes) {
    const run = await candidateHarness(agentProps, { getAgentCandidateSource: async () => ({ ...candidateProof(agentProps, "body-file"), ...change }) });
    let tree = run.render(); await filePicker(tree).props.onChange({ target: { value: "body-file" } }); tree = run.render();
    assert.equal(fileTextarea(tree), undefined);
    assert.equal(workflowButton(tree, "保存为原对象候选").props.disabled, true);
    assert.ok(agentNodes(tree).some((node) => node.props?.role === "alert"));
    assert.equal(run.calls.saved.length, 0);
  }
});
test("late file response and old save handler cannot replace or save a new explicit selection", async () => {
  const pending = new Map();
  const run = await candidateHarness(agentProps, { getAgentCandidateSource: (work, task, artifact) => new Promise((resolve) => pending.set(artifact, resolve)) });
  let tree = run.render();
  const notesRead = filePicker(tree).props.onChange({ target: { value: "notes-file" } });
  tree = run.render(); const bodyRead = filePicker(tree).props.onChange({ target: { value: "body-file" } });
  pending.get("body-file")(candidateProof(agentProps, "body-file")); await bodyRead; tree = run.render();
  const oldSave = workflowButton(tree, "保存为原对象候选");
  pending.get("notes-file")(candidateProof(agentProps, "notes-file")); await notesRead; tree = run.render();
  assert.equal(fileTextarea(tree).props.value, fileBody);
  const nextRead = filePicker(tree).props.onChange({ target: { value: "notes-file" } });
  await oldSave.props.onClick(); assert.equal(run.calls.saved.length, 0);
  pending.get("notes-file")(candidateProof(agentProps, "notes-file")); await nextRead;
  assert.equal(fileTextarea(run.render()).props.value, fileNotes);
});
test("late candidate file cannot cross workspace or resurrect after clearing selection", async () => {
  for (const changeScope of [false, true]) {
    let release;
    const run = await candidateHarness(agentProps, { getAgentCandidateSource: () => new Promise((resolve) => { release = resolve; }) });
    let tree = run.render(); const pending = filePicker(tree).props.onChange({ target: { value: "body-file" } });
    const other = { ...agentProps, workspaceId: "workspace-other", contextKey: "other-source" };
    if (changeScope) run.harness.render(other);
    else { tree = run.render(); await filePicker(tree).props.onChange({ target: { value: "" } }); }
    release(candidateProof(agentProps, "body-file")); await pending;
    tree = changeScope ? run.harness.render(other) : run.render();
    assert.equal(fileTextarea(tree), undefined); assert.equal(run.calls.saved.length, 0);
    assert.deepEqual([run.calls.executions, run.calls.creations], [0, 0]);
  }
});
test("late candidate file cannot return after source version changes", async () => {
  let release;
  const run = await candidateHarness(agentProps, { getAgentCandidateSource: () => new Promise((resolve) => { release = resolve; }) });
  let tree = run.render(); const waiting = filePicker(tree).props.onChange({ target: { value: "body-file" } });
  const changed = { ...run.props, source: { ...run.props.source, expected_version_ref: "new-version" } };
  run.harness.render(changed); release(candidateProof(agentProps, "body-file")); await waiting;
  assert.equal(fileTextarea(run.harness.render(changed)), undefined);
  assert.equal(run.calls.saved.length, 0);
});
test("foreign or duplicate result file list is refused before file preview", async () => {
  for (const change of [{ source_work_ref: "foreign" }, { reference_id: "task:foreign" }, { workspace_id: "foreign" },
    { artifacts: [candidateFiles[0], candidateFiles[0]] }]) {
    const run = await candidateHarness(agentProps, { getResultDetail: async () => ({ ...candidateDetail(agentProps), ...change }) });
    assert.equal(filePicker(run.render()), undefined); assert.equal(run.calls.previews.length, 0);
  }
});

test("Codex hold is shown only for a trusted scoped reason and cannot be continued", async () => {
  async function renderReason(reason_code) {
    const key = JSON.stringify(["curis.agent-work", "tenant-a", "company-a", "workspace-a", "assignment-a", "content:content-a"]);
    const storage = new Map([[key, JSON.stringify({ work_ref: "work-a" })]]);
    const harness = agentHarness({ getOriginalAgentWork: async () => ({
      tenant_id: "tenant-a", work: { entity_id: "work-a", company_id: "company-a", workspace_id: "workspace-a" },
      tasks: [{ task_id: "task-a", status: "FAILED", call_reserved: false, reason_code }],
    }) }, storage);
    harness.render(agentProps); await Promise.resolve();
    return agentNodes(harness.render(agentProps));
  }
  const held = await renderReason("codex_execution_held");
  assert.ok(held.some((n) => n.props?.role === "status" && n.props.children === "真实 Agent 执行暂不可用：停止安全机制尚未验证。"));
  assert.ok(!held.some((n) => n.type === "button" && n.props.children === "修复后继续原工作"));
  const ordinary = await renderReason(null);
  assert.ok(ordinary.some((n) => n.props?.role === "status" && n.props.children === "原执行未完成"));
  assert.ok(ordinary.some((n) => n.type === "button" && n.props.children === "修复后继续原工作"));
});


test("current Agent work opens the pinned Package17 result component", async () => {
  const stage = new URL("../../artifacts/tasks/CURIS-V1-EMPLOYEE-EXECUTION-CAPABILITIES-20261029/native-build-01/source/frontend/components/v1/ResultReferenceView.js", import.meta.url);
  const stagedSource = readFileSync(stage, "utf8");
  assert.equal(createHash("sha256").update(stagedSource).digest("hex"), "3371d6c7f55336cf7fc34459f299ff5b191d2e8fe38322326273ff2fa8b33636");
  const compiled = await swc.transform(stagedSource, { filename: "ResultReferenceView.js", isModule: true,
    jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } },
    module: { type: "commonjs" } });
  const slots = [], effects = []; let cursor = 0, reads = 0, downloads = 0, clicked = false;
  const hooks = {
    useState(initial) { const i = cursor++; if (!(i in slots)) slots[i] = typeof initial === "function" ? initial() : initial;
      return [slots[i], (v) => { slots[i] = typeof v === "function" ? v(slots[i]) : v; }]; },
    useRef(initial) { const i = cursor++; return slots[i] ||= { current: initial }; },
    useEffect(effect, deps) { const i = cursor++, old = slots[i];
      if (!old || !deps.every((v, j) => Object.is(v, old.deps[j]))) effects.push(() => { old?.cleanup?.(); slots[i] = { deps, cleanup: effect() }; }); },
  };
  const body = "ordinary fixture file", digest = createHash("sha256").update(body).digest("hex");
  const result = { tenant_id: "tenant-a", company_id: "company-a", workspace_id: "workspace-a",
    reference_id: "result-a", source_work_ref: "work-a", viewed: true,
    artifacts: [{ artifact_id: "artifact-a", artifact_type: "agent_file_receipt", title: "file.txt" }] };
  const resultModule = { exports: {} };
  vm.runInNewContext(compiled.code, { module: resultModule, exports: resultModule.exports, Uint8Array,
    atob, Blob, crypto: { subtle: webcrypto.subtle }, URL: { createObjectURL: () => "blob:fixture", revokeObjectURL() {} },
    document: { createElement: () => ({ click() { clicked = true; } }) }, setTimeout() {},
    require(name) {
      if (name === "react") return hooks;
      if (name === "react/jsx-runtime") return require(name);
      if (name === "../../lib/api.js") return { TENANT_ID: "tenant-a" };
      if (name === "../../lib/v1FrontendApi.js") return {
        getResultDetail: async (company, workspace, ref) => { reads++; assert.equal(company, "company-a"); assert.equal(workspace, "workspace-a"); assert.equal(ref, "result-a"); return result; },
        getOriginalAgentFile: async (work, artifact) => { downloads++; assert.equal(work, "work-a"); assert.equal(artifact, "artifact-a"); return { tenant_id: "tenant-a", company_id: "company-a", work_ref: work, artifact_ref: artifact, bytes: body.length, sha256: digest, content_base64: Buffer.from(body).toString("base64"), filename: "file.txt" }; },
      };
      if (name === "../../lib/runtimeApi.js") return { workspaceEntryHref: () => "/workspace" };
      if (name === "../../lib/d1State.mjs") return { d1Href: () => "/result", readableResult: () => [] };
      if (name === "../workspace/SharedEmployeeWorkArea.js") return { SharedResultUtility: () => null };
      throw new Error("Unexpected staged result import: " + name);
    },
  });
  const key = JSON.stringify(["curis.agent-work", "tenant-a", "company-a", "workspace-a", "assignment-a", "content:content-a"]);
  const storage = new Map([[key, JSON.stringify({ work_ref: "work-a" })]]);
  const agent = agentHarness({ getOriginalAgentWork: async () => ({ tenant_id: "tenant-a",
    work: { entity_id: "work-a", company_id: "company-a", workspace_id: "workspace-a" },
    tasks: [{ task_id: "task-a", status: "COMPLETED", result_ref: "result-a" }] }) }, storage, resultModule.exports);
  agent.render(agentProps); await Promise.resolve();
  let tree = agent.render(agentProps);
  agentNodes(tree).find((n) => n.type === "button" && Array.isArray(n.props.children) && n.props.children.includes("查看第 ")).props.onClick();
  tree = agent.render(agentProps);
  const view = agentNodes(tree).find((n) => n.type === resultModule.exports.default);
  assert.ok(view); assert.equal(view.props.companyId, "company-a"); assert.equal(view.props.selection.referenceId, "result-a");
  function renderResult() { cursor = 0; const rendered = view.type(view.props); while (effects.length) effects.shift()(); return rendered; }
  renderResult(); await Promise.resolve();
  const resultTree = renderResult(); assert.equal(reads, 1);
  const button = agentNodes(resultTree).find((n) => n.type === "button" && Array.isArray(n.props.children) && n.props.children.includes("下载原成果："));
  assert.ok(button); await button.props.onClick(); assert.equal(downloads, 1); assert.equal(clicked, true);
  view.props.onClose(); assert.ok(!agentNodes(agent.render(agentProps)).some((n) => n.type === resultModule.exports.default));
});

test("ordinary reply returns only its identity and receiving version, with explicit receipt and no replay", async () => {
  const { code: employeeCode } = await swc.transform(read("components/v1/EmployeeConversation.js"), {
    filename: "EmployeeConversation.js", isModule: true,
    jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } }, module: { type: "commonjs" },
  });
  const slots = [], effects = []; let cursor = 0;
  const same = (a, b) => a && b && a.length === b.length && a.every((x, i) => Object.is(x, b[i]));
  const hooks = {
    useState(initial) { const i = cursor++; if (!(i in slots)) slots[i] = typeof initial === "function" ? initial() : initial;
      return [slots[i], value => { slots[i] = typeof value === "function" ? value(slots[i]) : value; }]; },
    useRef(initial) { const i = cursor++; return slots[i] ||= { current: initial }; },
    useCallback(fn, deps) { const i = cursor++; if (!same(slots[i]?.deps, deps)) slots[i] = { fn, deps }; return slots[i].fn; },
    useEffect(fn, deps) { const i = cursor++; if (!same(slots[i], deps)) { slots[i] = deps; effects.push(fn); } },
  };
  const view = { tenant_id: "tenant", company_id: "company", owner_ref: "employee", conversation_id: "conversation",
    assignments: [{ assignment_ref: "assignment", workspace_id: "workspace" }], execution_models: [], attempts: [],
    discussion_scope: { workspace_id: "workspace", object_ref: "object", assignment_ref: "assignment" },
    discussion_topics: [{ conversation_id: "conversation", workspace_id: "workspace", object_ref: "object", assignment_ref: "assignment" }],
    messages: [{ message_id: "reply", task_ref: "task", sender: { kind: "EMPLOYEE" }, body: "原回复",
      provenance: { execution_selection: { purpose: "CONVERSATION_REPLY" } } }] };
  const calls = []; let refreshed = 0, reread = 0;
  const module = { exports: {} };
  vm.runInNewContext(employeeCode, { module, exports: module.exports, URLSearchParams, setInterval: () => 1, clearInterval() {},
    localStorage: { getItem: () => null, setItem() {} },
    require(name) { if (name === "react") return hooks; if (name === "react/jsx-runtime") return require(name);
      if (name.includes("v1FrontendApi")) return { getConversation: async () => view, getEmployeeConversation: async () => view,
        getEmployeeConversationReferences: async () => ({ references: [] }), receiveConversationResult: async (...args) => { calls.push(args); return { candidate_ref: "candidate" }; } };
      return {}; },
  });
  const props = { companyId: "company", employee: { employee_ref: "employee" }, conversationId: "conversation",
    embedded: { workspaceId: "workspace", contextKey: "content:object", objectRef: "object", assignmentRef: "assignment", receiveReady: true,
      onAgentCandidate: () => { refreshed++; }, onReload: () => { reread++; }, agentSource: { kind: "content-growth", content_ref: "object", expected_version_ref: "version",
        selection: null, references: [] } } };
  const render = extra => { cursor = 0; const tree = module.exports.default({ ...props, ...extra }); while (effects.length) effects.shift()(); return tree; };
  render(); await new Promise(resolve => setImmediate(resolve));
  const receipt = tree => agentNodes(tree).find(n => n.type === "button" && ["送回当前工作候选", "已送回业务候选"].includes(n.props.children));
  let tree = render(); assert.equal(receipt(tree).props.disabled, undefined);
  await Promise.all([receipt(tree).props.onClick(), receipt(tree).props.onClick()]);
  assert.equal(calls.length, 1); assert.equal(refreshed, 1);
  assert.deepEqual(JSON.parse(JSON.stringify(calls[0])), ["company", "conversation", { workspace_id: "workspace", message_ref: "reply",
    source: { kind: "content-growth", content_ref: "object", expected_version_ref: "version" } }]);
  tree = render(); assert.ok(agentNodes(tree).some(n => n.type === "button" && n.props.children === "已送回业务候选" && n.props.disabled));
  assert.ok(receipt(render({ embedded: { ...props.embedded, receiveReady: false } })).props.disabled);
  const button = (tree, label) => agentNodes(tree).find(n => n.type === "button" && n.props.children === label);
  for (const [credential_wait, label] of [
    ["WAITING", "正在核对模型凭据，等待系统返回。"],
    ["LONG_WAIT", "模型凭据核对已等待较久，原请求结果仍待确认。可重新读取状态，请勿重复发送。"],
    [undefined, "已接收原请求，正在处理并等待回复。"],
  ]) {
    view.attempts = [{ attempt_id: "original", status: "RUNNING", credential_wait }];
    await button(render(), "重新读取").props.onClick();
    tree = render();
    assert.ok(agentNodes(tree).some(n => n.props.role === "status" && n.props.children === label));
    assert.equal(button(tree, "修复后重试原消息"), undefined);
  }
  assert.equal(reread, 3);
  assert.equal(calls.length, 1);
});
