import assert from "node:assert/strict";
import test from "node:test";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import * as helpers from "../lib/d1State.mjs";

const require = createRequire(import.meta.url);
const { transform, loadBindings } = require("next/dist/build/swc");
function hooks() {
  const slots = [], effects = [];
  let index = 0;
  const react = {
    createElement(type, props, ...children) { return { type, props: { ...props, children } }; },
    useState(initial) {
      const at = index++;
      if (!(at in slots)) slots[at] = typeof initial === "function" ? initial() : initial;
      return [slots[at], (value) => { slots[at] = typeof value === "function" ? value(slots[at]) : value; }];
    },
    useRef(initial) { const at = index++; return slots[at] ||= { current: initial }; },
    useReducer(reducer, value, init) {
      const [state, set] = react.useState(() => init ? init(value) : value);
      return [state, (action) => set((current) => reducer(current, action))];
    },
    useCallback(fn, deps) {
      const at = index++, old = slots[at];
      if (!old || deps.some((x, i) => x !== old.deps[i])) slots[at] = { value: fn, deps };
      return slots[at].value;
    },
    useEffect(fn, deps) {
      const at = index++, old = slots[at];
      if (!old || deps.some((x, i) => x !== old.deps[i])) effects.push(() => {
        old?.cleanup?.(); slots[at] = { deps, cleanup: fn() };
      });
    },
  };
  return { react, render(fn, props) { index = 0; return fn(props); }, flush() { effects.splice(0).forEach((fn) => fn()); } };
}
async function compile(path, h, imports) {
  await loadBindings();
  const { code } = await transform(readFileSync(new URL(`../${path}`, import.meta.url), "utf8"), {
    filename: path, jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "classic" } } }, module: { type: "commonjs" },
  });
  const mod = { exports: {} };
  new Function("require", "module", "exports", "React", code)((name) => name === "react" ? h.react : imports[name] || {}, mod, mod.exports, h.react);
  return mod.exports.default;
}
function find(node, predicate, result = []) {
  if (Array.isArray(node)) { node.forEach((x) => find(x, predicate, result)); return result; }
  if (!node || typeof node !== "object") return result;
  if (predicate(node)) result.push(node);
  find(node.props?.children, predicate, result); return result;
}
function text(node) {
  if (Array.isArray(node)) return node.map(text).join("");
  if (node == null || typeof node === "boolean") return "";
  return typeof node === "object" ? text(node.props?.children) : String(node);
}
const button = (tree, label) => find(tree, (x) => x.type === "button" && text(x) === label)[0];
const deferred = () => { let resolve, reject; const promise = new Promise((a, b) => { resolve = a; reject = b; }); return { promise, resolve, reject }; };
const styles = { __esModule: true, default: new Proxy({}, { get: (_, key) => key }) };
async function workView(h) {
  return compile("components/delivery/d1/WorkView.js", h, {
    "../../../lib/d1Api.js": { d1Error: () => "读取未确认" }, "../../../lib/d1State.mjs": helpers,
    "./CeoMatterView.js": { workState: (x) => x }, "./D1.module.css": styles,
    "../../../lib/runtimeApi.js": { workspaceEntryHref: (x) => `/workspace/${x}` },
  });
}

test("control success plus failed GET preserves draft and pending across new objects/remount until exact readback", async () => {
  let posts = 0;
  const work = { companyId: "c-control", workspaceId: "w", work_ref: "original", lifecycle_status: "ACTIVE", status: "ACTIVE" };
  helpers.saveWorkControl(helpers.workControlKey(work.companyId, work), null);
  const h = hooks(), Component = await workView(h);
  const props = { work, companyId: work.companyId, api: { controlWork: async () => { posts++; } }, onRefresh: async () => { throw new Error("GET down"); } };
  const render = () => h.render(Component, props);
  let tree = render(); button(tree, "暂停工作").props.onClick(); tree = render();
  find(tree, (x) => x.type === "textarea")[0].props.onChange({ target: { value: "保留原理由" } }); tree = render();
  await find(tree, (x) => x.type === "form")[0].props.onSubmit({ preventDefault() {} }); tree = render();
  assert.equal(posts, 1); assert.equal(find(tree, (x) => x.type === "textarea")[0].props.value, "保留原理由");
  props.work = { ...work }; tree = render();
  await find(tree, (x) => x.type === "form")[0].props.onSubmit({ preventDefault() {} }); assert.equal(posts, 1);
  const remount = hooks(), Remounted = await workView(remount);
  tree = remount.render(Remounted, props);
  assert.equal(button(tree, "确认暂停工作").props.disabled, true);
  props.onRefresh = async () => ({ ...work, companyId: "foreign", lifecycle_status: "PAUSED" });
  tree = remount.render(Remounted, props); await button(tree, "重新读取原工作").props.onClick(); tree = remount.render(Remounted, props);
  assert.equal(button(tree, "确认暂停工作").props.disabled, true);
  props.onRefresh = async () => ({ ...work, lifecycle_status: "ACTIVE" });
  tree = remount.render(Remounted, props); await button(tree, "重新读取原工作").props.onClick(); tree = remount.render(Remounted, props);
  assert.equal(button(tree, "确认暂停工作").props.disabled, true);
  props.onRefresh = async () => ({ ...work, lifecycle_status: "PAUSED" });
  tree = remount.render(Remounted, props); await button(tree, "重新读取原工作").props.onClick(); tree = remount.render(Remounted, props);
  assert.equal(find(tree, (x) => x.type === "form").length, 0);
  assert.equal(helpers.readWorkControl(helpers.workControlKey(work.companyId, work)), null);
});

test("unknown POST never retries and an in-flight GET keeps input locked", async () => {
  const h = hooks(), Component = await workView(h), read = deferred();
  let posts = 0, reads = 0;
  const work = { companyId: "c-unknown", workspaceId: "w", work_ref: "x", lifecycle_status: "ACTIVE", status: "ACTIVE" };
  const props = { work, companyId: work.companyId, api: { controlWork: async () => { posts++; throw new Error("POST response lost"); } }, onRefresh: () => { reads++; return read.promise; } };
  const render = () => h.render(Component, props);
  let tree = render(); button(tree, "停止工作").props.onClick(); tree = render();
  find(tree, (x) => x.type === "textarea")[0].props.onChange({ target: { value: "不要重发" } }); tree = render();
  await find(tree, (x) => x.type === "form")[0].props.onSubmit({ preventDefault() {} }); tree = render();
  assert.equal(reads, 0); assert.equal(posts, 1);
  const promise = button(tree, "重新读取原工作").props.onClick(); tree = render();
  assert.equal(button(tree, "正在确认…").props.disabled, true);
  assert.equal(find(tree, (x) => x.type === "textarea")[0].props.value, "不要重发");
  read.resolve({ ...work, lifecycle_status: "CANCELLED" }); await promise;
  assert.equal(posts, 1);
});

test("Usage empty and unknown are honest; separate attempts remain separate", async () => {
  const h = hooks(), Component = await workView(h);
  let rows = [];
  const props = { work: { companyId: "c-usage", workspaceId: "w", work_ref: "x" }, companyId: "c-usage", api: { usage: async () => rows } };
  const render = () => h.render(Component, props);
  let tree = render(); await button(tree, "查看使用记录").props.onClick(); tree = render();
  assert.match(text(tree), /不能据此判断费用/);
  rows = [1, 2].map((attempt_no) => ({ usage_record_id: `row-${attempt_no}`, attempt_no, logical_call_id: "same", metering_status: "unknown", total_tokens: null, cost_amount: null }));
  await button(tree, "查看使用记录").props.onClick(); tree = render();
  assert.equal(find(tree, (x) => x.type === "dl" && text(x).includes("原执行 / Task / 尝试")).length, 2);
  assert.doesNotMatch(text(tree), /0 USD|Token0/);
});

test("D1Surface refresh retains the same WorkView element until real GET, rejecting stale reads", async () => {
  const h = hooks(), Work = () => {}, reads = [], original = { companyId: "c-surface", workspaceId: "w", work_ref: "x", lifecycle_status: "ACTIVE" };
  const api = { attention: async () => ({ company: { company_id: "c-surface" }, items: [] }), businesses: async () => ({ businesses: [] }),
    work: () => { const row = deferred(); reads.push(row); return row.promise; } };
  globalThis.window = { location: { search: "?view=work&workspace_id=w&work_ref=x", pathname: "/ceo-office" }, addEventListener() {}, removeEventListener() {} };
  const Component = await compile("components/delivery/d1/D1Surface.js", h, {
    "next/navigation": { useSearchParams: () => new URLSearchParams(window.location.search) },
    "../../runtime/RuntimeProvider.js": { useRuntime: () => ({ companyId: "c-surface", status: "ready", snapshot: { company: { company_id: "c-surface" } } }) },
    "../../../lib/d1Api.js": { d1Api: api, d1Error: () => "GET failed" }, "../../../lib/d1State.mjs": helpers,
    "./WorkView.js": { __esModule: true, default: Work }, "./D1.module.css": styles,
    "../../../lib/runtimeApi.js": { getOrganizationProjection: async () => ({ company: { company_id: "c-surface" } }) },
    "../../../lib/organizationProjection.js": { buildOrganizationProjection: (x) => x },
    "../../../lib/theme.js": { roleLabel: (x) => x },
  });
  const render = () => h.render(Component, {});
  render(); h.flush(); render(); h.flush();
  assert.equal(reads.length, 1); reads[0].resolve(original); await new Promise(setImmediate);
  let tree = render(), element = find(tree, (x) => x.type === Work)[0]; assert.ok(element);
  const key = element.props.key, pending = element.props.onRefresh();
  tree = render(); element = find(tree, (x) => x.type === Work)[0]; assert.equal(element.props.key, key);
  reads[1].reject(new Error("GET failure")); await assert.rejects(pending); tree = render();
  assert.ok(find(tree, (x) => x.type === Work)[0], "GET failure must not unmount the editor");
  element = find(tree, (x) => x.type === Work)[0];
  const older = element.props.onRefresh(), newest = element.props.onRefresh();
  reads[3].resolve({ ...original, lifecycle_status: "PAUSED" }); await newest;
  reads[2].resolve(original); await assert.rejects(older);
  tree = render(); assert.equal(find(tree, (x) => x.type === Work)[0].props.work.lifecycle_status, "PAUSED");
  delete globalThis.window;
});

test("Generic control reads exact scope without team materialization and locks an unknown effect", async () => {
  const h = hooks(), read = deferred();
  let posts = 0, gets = 0, teamWrites = 0;
  const work = { work_ref: "generic-work", lifecycle_status: "ACTIVE", status: "ACTIVE", problem: "manual test",
    result_refs: [], evidence_refs: [], artifact_refs: [] };
  const data = { company: { company_id: "generic-c" }, workspace: { workspace_id: "w", name: "test" }, business: {},
    current_work: [work], team: { employees: [] }, results: [], operating_readiness: { status: "READY_FOR_WORK" } };
  const api = { getGeneralWorkspace: async () => { gets++; return gets === 1 ? data : read.promise; },
    controlGeneralWorkspaceWork: async () => { posts++; }, materializeGeneralWorkspaceTeam: async () => { teamWrites++; },
    getGeneralWorkspaceTeamCandidates: async () => ({ employees: [] }) };
  globalThis.window = { location: { search: "", origin: "http://curis.local" }, sessionStorage: { getItem: () => null } };
  const Component = await compile("components/v1/GeneralWorkspaceOperating.js", h, {
    "../../lib/d1State.mjs": helpers, "../../lib/runtimeApi.js": api,
    "./ResultReferenceView.js": { resultSelection() {}, restoreResultSelection() {}, generalResultTitleContext() {} },
  });
  const props = { companyId: "generic-c", workspaceId: "w", parentPath: { company: {}, department: {}, business: {} } };
  const render = () => h.render(Component, props);
  render(); h.flush(); await new Promise(setImmediate);
  let tree = render(); assert.ok(button(tree, "暂停"));
  const pending = button(tree, "暂停").props.onClick(); await Promise.resolve(); tree = render();
  assert.equal(button(tree, "暂停").props.disabled, true);
  read.resolve({ ...data, company: { company_id: "foreign" } }); await pending; tree = render();
  assert.equal(teamWrites, 0); assert.equal(posts, 1); assert.equal(gets, 2);
  assert.match(text(tree), /控制结果待核对/);
  assert.equal(button(tree, "开始处理"), undefined);
  await button(tree, "暂停").props.onClick(); assert.equal(posts, 1);
  delete globalThis.window;
});

test("Generic late control cannot write across a scope render or unlock a newer command", async () => {
  for (const finishBeforeEffects of [true, false]) {
    const h = hooks(), oldRead = deferred(), newRead = deferred();
    let oldGets = 0, newGets = 0, posts = 0;
    const makeData = (workspaceId, state = "ACTIVE") => ({ company: { company_id: "scope-c" }, workspace: { workspace_id: workspaceId, name: workspaceId },
      business: {}, team: { employees: [] }, results: [], operating_readiness: { status: "READY_FOR_WORK" },
      current_work: [{ work_ref: `work-${workspaceId}`, lifecycle_status: state, status: state, result_refs: [], evidence_refs: [], artifact_refs: [] }] });
    const api = { getGeneralWorkspace: async (_company, workspace) => {
      if (workspace === "old") return ++oldGets === 1 ? makeData("old") : oldRead.promise;
      return ++newGets === 1 ? makeData("new") : newRead.promise;
    }, controlGeneralWorkspaceWork: async () => { posts++; } };
    globalThis.window = { location: { search: "", origin: "http://curis.local" }, sessionStorage: { getItem: () => null } };
    for (const ws of ["old", "new"]) helpers.saveWorkControl(helpers.workControlKey("scope-c", { workspaceId: ws, work_ref: `work-${ws}` }), null);
    const Component = await compile("components/v1/GeneralWorkspaceOperating.js", h, { "../../lib/d1State.mjs": helpers,
      "../../lib/runtimeApi.js": api, "./ResultReferenceView.js": { restoreResultSelection() {}, generalResultTitleContext() {} } });
    const props = { companyId: "scope-c", workspaceId: "old", parentPath: { company: {}, department: {}, business: {} } };
    const render = () => h.render(Component, props);
    render(); h.flush(); await new Promise(setImmediate);
    let tree = render(); const oldPending = button(tree, "暂停").props.onClick(); await Promise.resolve();
    props.workspaceId = "new"; tree = render();
    assert.equal(button(tree, "暂停"), undefined, "old Work must disappear immediately on a different scope");
    if (finishBeforeEffects) {
      oldRead.resolve(makeData("old", "PAUSED")); await oldPending;
      tree = render(); assert.equal(button(tree, "继续工作"), undefined);
    }
    h.flush(); await new Promise(setImmediate); tree = render();
    assert.ok(button(tree, "暂停"));
    const newPending = button(tree, "暂停").props.onClick(); await Promise.resolve(); tree = render();
    assert.equal(button(tree, "暂停").props.disabled, true);
    if (!finishBeforeEffects) {
      oldRead.resolve(makeData("old", "PAUSED")); await oldPending; tree = render();
      assert.equal(button(tree, "暂停").props.disabled, true, "old finally cannot release the new command");
    }
    newRead.resolve(makeData("new", "PAUSED")); await newPending; tree = render();
    assert.ok(button(tree, "继续工作")); assert.equal(posts, 2);
    delete globalThis.window;
  }
});

test("human report/review/continue keep unknown commands locked until their exact authoritative effect", async () => {
  for (const command of ["report", "review", "continue"]) {
    const h = hooks(), Component = await workView(h);
    let posts = 0, submission = "same-report", fresh, getFails = false;
    const revision = { report: 1, review: 2, continue: 3 }[command];
    const request = { requestId: `human-${command}`, revision, kind: "LOCAL_INFORMATION",
      state: { report: "WAITING_INPUT", review: "LOCAL_REPORTED", continue: "READY" }[command],
      companyId: `c-human-${command}`, workspaceId: "w", targetRef: "original-human-work", workRef: "original-human-work",
      assignmentRef: "assignment", holderRef: "holder", sourceTaskRef: "original-task", sourceExecutionKey: "original-execution",
      sourceOutputSha256: "original-output", inputFingerprint: "original-input", actionVersion: "original-action",
      ...(command !== "report" ? { report: { submissionId: submission, text: "draft", referenceRefs: [], source: "USER_LOCAL_INPUT", actor: "CEO", at: "2026-01-01T00:00:00Z" } } : {}),
      ...(command === "continue" ? { reviewedAt: "2026-01-01T00:00:01Z" } : {}) };
    const work = { companyId: request.companyId, workspaceId: "w", work_ref: request.targetRef,
      lifecycle_status: "ACTIVE", status: "WAITING", result_refs: [], human_input: request };
    fresh = structuredClone(work);
    const unknown = async (_company, _work, body) => { posts++; if (command === "report") submission = body.submission_id; throw Error("unknown POST"); };
    const props = { work, companyId: work.companyId, api: { reportHumanInput: unknown, reviewHumanInput: unknown, continueHumanInput: unknown },
      onRefresh: async () => { if (getFails) throw Error("unknown GET"); return fresh; } };
    const render = () => h.render(Component, props);
    const act = (tree) => command === "report" ? find(tree, (x) => x.type === "form")[0].props.onSubmit({ preventDefault() {} })
      : button(tree, command === "review" ? "核对本地补充" : "续接原工作一次").props.onClick({ preventDefault() {} });
    const disabled = (tree) => button(tree, { report: "提交到原工作", review: "核对本地补充", continue: "续接原工作一次" }[command]).props.disabled;
    let tree = render();
    if (command === "report") { find(tree, (x) => x.type === "textarea")[0].props.onChange({ target: { value: "draft" } }); tree = render(); }
    await act(tree); tree = render(); assert.equal(posts, 1); assert.equal(disabled(tree), true);
    await act(tree); assert.equal(posts, 1, `${command}: unchanged GET cannot allow another POST`);
    const accepted = { ...work, human_input: { ...request, revision: revision + 1,
      state: { report: "LOCAL_REPORTED", review: "READY", continue: "CLAIMED" }[command],
      report: request.report || { submissionId: submission, text: "draft", referenceRefs: [] },
      ...(command === "review" ? { reviewedAt: "2026-01-01T00:00:01Z" } : {}),
      ...(command === "continue" ? { continuationKey: "responsibility:original-human-work:assignment:1", claimedAt: "2026-01-01T00:00:02Z" } : {}) } };
    const wrong = [
      structuredClone(work),
      { ...accepted, human_input: { ...accepted.human_input, revision } },
      { ...accepted, human_input: { ...accepted.human_input, state: request.state } },
      { ...accepted, companyId: "foreign" }, { ...accepted, workspaceId: "foreign" }, { ...accepted, work_ref: "foreign" },
      { ...accepted, human_input: { ...accepted.human_input, companyId: "foreign" } },
      { ...accepted, human_input: { ...accepted.human_input, requestId: "another-request" } },
      { ...accepted, human_input: { ...accepted.human_input, sourceTaskRef: "another-source" } },
      { ...accepted, human_input: { ...accepted.human_input, report: { ...accepted.human_input.report, submissionId: "wrong-submission" } } },
      { ...accepted, human_input: { ...accepted.human_input, report: { ...accepted.human_input.report, text: "another-report" } } },
      { ...accepted, human_input: { ...accepted.human_input, revision: revision + 10 } },
    ];
    if (command === "continue") wrong.push(
      { ...accepted, human_input: { ...accepted.human_input, continuationKey: null } },
      { ...accepted, human_input: { ...accepted.human_input, continuationKey: "responsibility:other:assignment:1" } },
      { ...accepted, human_input: { ...accepted.human_input, claimedAt: null } });
    if (command === "review") wrong.push({ ...accepted, human_input: { ...accepted.human_input, reviewedAt: null } });
    for (const value of wrong) {
      fresh = value; tree = render(); await button(tree, "重新读取原工作").props.onClick(); tree = render();
      assert.equal(disabled(tree), true, `${command}: wrong scope/source/version/state/submission cannot confirm`);
      await act(tree); assert.equal(posts, 1);
      if (command === "report") assert.equal(find(tree, (x) => x.type === "textarea")[0].props.value, "draft");
    }
    // Even if the parent renders another current request, the old pending command must not act on it.
    props.work = { ...work, human_input: { ...request, requestId: "replacement-request" } }; tree = render();
    await act(tree); assert.equal(posts, 1); props.work = work;
    getFails = true; tree = render(); await button(tree, "重新读取原工作").props.onClick(); tree = render();
    assert.equal(disabled(tree), true); await act(tree); assert.equal(posts, 1); getFails = false;
    fresh = { ...work, lifecycle_status: "PAUSED", human_input: { ...request, revision: revision + 1,
      state: "INVALIDATED", invalidatedReason: "ORIGINAL_WORK_CANCELLED" } };
    tree = render(); await button(tree, "重新读取原工作").props.onClick(); tree = render();
    assert.match(text(tree), /原请求已失效/); assert.match(text(tree), /提交是否完成仍未确认/);
    assert.equal(disabled(tree), true);
    fresh = accepted; tree = render(); await button(tree, "重新读取原工作").props.onClick(); props.work = accepted; tree = render();
    assert.doesNotMatch(text(tree), /正在核对原工作中的提交结果/);
    if (command !== "continue") assert.equal(button(tree, command === "report" ? "核对本地补充" : "续接原工作一次").props.disabled, false);
    else assert.match(text(tree), /续接已领取/);
    assert.equal(posts, 1, `${command}: authoritative confirmation does not resend`);
  }
});

test("successful human POST plus stale GET stays locked and external report confirms only its unknown state", async () => {
  const h = hooks(), Component = await workView(h);
  let posts = 0, submitted, fresh;
  const work = { companyId: "external-c", workspaceId: "w", work_ref: "external-work", status: "WAITING", lifecycle_status: "ACTIVE", result_refs: [],
    human_input: { companyId: "external-c", workspaceId: "w", targetRef: "external-work", requestId: "external-r", kind: "EXTERNAL_ACTION_REPORT", revision: 1, state: "WAITING_INPUT" } };
  fresh = work;
  const props = { work, companyId: work.companyId, onRefresh: async () => fresh, api: { reportHumanInput: async (_c, _w, body) => { posts++; submitted = body; } } };
  const render = () => h.render(Component, props);
  let tree = render(); find(tree, (x) => x.type === "textarea")[0].props.onChange({ target: { value: "manual source" } }); tree = render();
  await find(tree, (x) => x.type === "form")[0].props.onSubmit({ preventDefault() {} }); tree = render();
  assert.equal(button(tree, "提交到原工作").props.disabled, true); assert.equal(submitted.manual_source, "manual source");
  fresh = { ...work, human_input: { ...work.human_input, revision: 2, state: "EXTERNAL_REPORTED_UNKNOWN",
    report: { submissionId: submitted.submission_id, text: "manual source", referenceRefs: [] } } };
  await button(tree, "重新读取原工作").props.onClick(); props.work = fresh; tree = render();
  assert.doesNotMatch(text(tree), /正在核对原工作中的提交结果/); assert.match(text(tree), /外部事实未知/);
  assert.equal(button(tree, "续接原工作一次"), undefined); assert.equal(posts, 1);
});

test("authoritative later human states reconcile the same submission without replay or invented completion", async () => {
  for (const [command, state, nextRevision] of [["report", "READY", 3], ["report", "CLAIMED", 4], ["report", "CLOSED", 5],
    ["review", "CLAIMED", 4], ["review", "CLOSED", 5], ["continue", "CLOSED", 5]]) {
    const h = hooks(), Component = await workView(h);
    let posts = 0, submission = "retained-report";
    const human = { requestId: "later-request", companyId: "later-company", workspaceId: "w", targetRef: "later-work", assignmentRef: "assignment",
      kind: "LOCAL_INFORMATION", revision: { report: 1, review: 2, continue: 3 }[command],
      state: { report: "WAITING_INPUT", review: "LOCAL_REPORTED", continue: "READY" }[command],
      ...(command === "report" ? {} : { report: { submissionId: submission, text: "retained draft", referenceRefs: [] } }) };
    const work = { companyId: "later-company", workspaceId: "w", work_ref: "later-work", lifecycle_status: "ACTIVE", status: "WAITING", result_refs: [], human_input: human };
    let confirmed;
    const send = async (_c, _w, body) => { posts++; if (command === "report") submission = body.submission_id; throw Error("response lost"); };
    const props = { work, companyId: work.companyId, api: { reportHumanInput: send, reviewHumanInput: send, continueHumanInput: send }, onRefresh: async () => {
      confirmed = { ...work, human_input: { ...human, state, revision: nextRevision,
        report: { submissionId: submission, text: "retained draft", referenceRefs: [] }, reviewedAt: "2026-01-01T00:00:01Z",
        continuationKey: "responsibility:later-work:assignment:1", claimedAt: "2026-01-01T00:00:02Z", closedAt: "2026-01-01T00:00:03Z" } };
      return confirmed;
    } };
    const render = () => h.render(Component, props);
    let tree = render();
    if (command === "report") {
      find(tree, (x) => x.type === "textarea")[0].props.onChange({ target: { value: "retained draft" } }); tree = render();
      await find(tree, (x) => x.type === "form")[0].props.onSubmit({ preventDefault() {} });
    } else await button(tree, command === "review" ? "核对本地补充" : "续接原工作一次").props.onClick({ preventDefault() {} });
    props.work = confirmed; tree = render();
    assert.doesNotMatch(text(tree), /正在核对原工作中的提交结果/); assert.equal(posts, 1);
    if (state === "READY") assert.equal(button(tree, "续接原工作一次").props.disabled, false);
    else assert.equal(button(tree, "续接原工作一次"), undefined);
  }
});

test("explicit same-request terminal invalidation retires uncertainty without claiming success or blocking lawful Work controls", async () => {
  for (const lifecycle of ["CANCELLED", "COMPLETED", "ARCHIVED"]) {
    const h = hooks(), Component = await workView(h);
    let posts = 0, fresh;
    const work = { companyId: `retired-${lifecycle}`, workspaceId: "w", work_ref: "retired-work", lifecycle_status: "ACTIVE", status: "WAITING", result_refs: [],
      human_input: { requestId: "retired-r", kind: "LOCAL_INFORMATION", revision: 1, state: "WAITING_INPUT", targetRef: "retired-work" } };
    fresh = work;
    const props = { work, companyId: work.companyId, onRefresh: async () => fresh,
      api: { reportHumanInput: async () => { posts++; throw Error("unknown submission"); } } };
    const render = () => h.render(Component, props);
    let tree = render(); find(tree, (x) => x.type === "textarea")[0].props.onChange({ target: { value: "retained uncertain draft" } }); tree = render();
    await find(tree, (x) => x.type === "form")[0].props.onSubmit({ preventDefault() {} }); tree = render();
    const invalidated = { ...work, lifecycle_status: lifecycle, human_input: { ...work.human_input,
      revision: 2, state: "INVALIDATED", invalidatedAt: "2026-01-01T00:00:01Z", invalidatedReason: "ORIGINAL_WORK_CANCELLED" } };
    for (const wrong of [{ ...invalidated, companyId: "foreign" },
      { ...invalidated, human_input: { ...invalidated.human_input, requestId: "other-request" } },
      { ...invalidated, human_input: { ...invalidated.human_input, revision: 1 } },
      { ...invalidated, lifecycle_status: "PAUSED" }]) {
      fresh = wrong; tree = render(); await button(tree, "重新读取原工作").props.onClick(); tree = render();
      assert.match(text(tree), /正在核对原工作中的提交结果/); assert.equal(button(tree, "提交到原工作").props.disabled, true);
    }
    fresh = invalidated; tree = render(); await button(tree, "重新读取原工作").props.onClick(); props.work = invalidated; tree = render();
    assert.match(text(tree), /提交是否完成仍未确认/); assert.match(text(tree), /草稿已保留/);
    const label = lifecycle === "ARCHIVED" ? "恢复查看" : "归档工作";
    assert.equal(button(tree, label).props.disabled, false); button(tree, label).props.onClick(); tree = render();
    assert.ok(find(tree, (x) => x.type === "form")[0], "lawful Work action remains available after human retirement");
    assert.match(text(tree), /该次提交是否完成仍未确认/);
    // A stale parent render cannot make the retired human request actionable again.
    props.work = work; tree = render();
    assert.equal(button(tree, "提交到原工作").props.disabled, true);
    assert.equal(find(tree, (x) => x.type === "textarea")[0].props.value, "retained uncertain draft");
    await find(tree, (x) => x.type === "form")[0].props.onSubmit({ preventDefault() {} }); assert.equal(posts, 1);
  }
});

for (const sample of [
  { id: "real names", name: "原员工名", holderName: "原负责人", team: "原员工名", holder: "原负责人" },
  { id: "verified placeholder", team: "组织员工名", holder: "组织员工名" },
  { id: "whitespace names", name: " \t", holderName: " \n", team: "组织员工名", holder: "组织员工名" },
  { id: "missing names", name: undefined, holderName: undefined, team: "组织员工名", holder: "组织员工名" },
  { id: "wrong bridge", bridge: "foreign", team: "未命名员工", holder: "未命名员工" },
  { id: "unverified bridge", bridgeStatus: "UNKNOWN", team: "未命名员工", holder: "未命名员工" },
  { id: "unverified employee", identity: "EXACT_ID_FALLBACK", team: "未命名员工", holder: "未命名员工" },
  { id: "unverified organization", organizationIdentity: "EXACT_ID_MATCH", team: "未命名员工", holder: "未命名员工" },
  { id: "absent organization", noOrganization: true, team: "未命名员工", holder: "未命名员工" },
  { id: "blank organization", organizationName: "  ", team: "未命名员工", holder: "未命名员工" },
  { id: "foreign holder", holderRef: "foreign", team: "组织员工名", holder: "未命名员工" },
  { id: "missing holder", holderRef: null, holderName: undefined, team: "组织员工名", holder: "尚未明确" },
  { id: "duplicate holder", duplicate: true, team: "组织员工名", holder: "未命名员工" },
  { id: "unverified team name is not a holder fallback", identity: "EXACT_ID_FALLBACK", name: "现有团队名", holderName: undefined, team: "现有团队名", holder: "尚未明确" },
]) {
  test(`General verified display names: ${sample.id}`, async () => {
    const h = hooks(); let gets = 0, teamWrites = 0;
    const value = (key, fallback) => Object.hasOwn(sample, key) ? sample[key] : fallback;
    const employee = { employee_ref: "runtime-e", company_employee_ref: "company-e",
      name: value("name", "未命名员工"), identity_status: value("identity", "VERIFIED_EXPLICIT_BRIDGE"),
      identity_bridge: { status: value("bridgeStatus", "VERIFIED"), companyEmployeeRef: value("bridge", "company-e") },
      organization_record: sample.noOrganization ? null : { identity_status: value("organizationIdentity", "VERIFIED_EXPLICIT_BRIDGE"), name: value("organizationName", "组织员工名") },
      responsibility: "原职责" };
    const work = { work_ref: "work-e", lifecycle_status: "WAITING", status: "WAITING", execution_status: "FAILED", problem: "公开任务",
      responsibility_holder_ref: value("holderRef", "runtime-e"), responsibility_holder_name: value("holderName", "未命名员工"),
      current_executor_ref: null, result_refs: [], evidence_refs: [], artifact_refs: [] };
    const data = { company: { company_id: "c" }, workspace: { workspace_id: "w", name: "公开空间" }, business: {},
      current_work: [work], team: { employees: sample.duplicate ? [employee, { ...employee }] : [employee] }, results: [],
      operating_readiness: { status: "READY_FOR_WORK" } };
    const snapshot = JSON.stringify(data);
    const api = { getGeneralWorkspace: async () => { gets++; return data; },
      getGeneralWorkspaceTeamCandidates: async () => ({ employees: [] }),
      materializeGeneralWorkspaceTeam: async () => { teamWrites++; throw Error("No team mutation"); } };
    globalThis.window = { location: { search: "", origin: "http://curis.local" }, sessionStorage: { getItem: () => null } };
    try {
      const Component = await compile("components/v1/GeneralWorkspaceOperating.js", h, {
        "next/link": { __esModule: true, default: "a" }, "../../lib/d1State.mjs": helpers,
        "../../lib/runtimeApi.js": api, "./ResultReferenceView.js": { resultSelection() {}, restoreResultSelection() {}, generalResultTitleContext() {} },
      });
      const props = { companyId: "c", workspaceId: "w", parentPath: { company: {}, department: {}, business: {} } };
      const render = () => h.render(Component, props);
      render(); h.flush(); await new Promise(setImmediate); const tree = render();
      const rows = find(tree, (x) => x.type === "li" && x.props.key === "runtime-e");
      assert.equal(rows.length, sample.duplicate ? 2 : 1);
      for (const row of rows) {
        const linked = employee.identity_status === "VERIFIED_EXPLICIT_BRIDGE";
        assert.equal(text(row.props.children[0]), sample.team + (linked ? " · 对话" : ""));
        assert.equal(text(row.props.children[1]), "原职责");
        const links = find(row, (x) => x.type === "a");
        assert.equal(links.length, linked ? 1 : 0);
        if (linked) assert.equal(links[0].props.href, "/ceo-office/organization/employees/company-e#employee-conversation");
      }
      const holder = find(tree, (x) => x.type === "div" && Array.isArray(x.props.children)
        && x.props.children[0]?.type === "dt" && text(x.props.children[0]) === "负责人");
      assert.equal(holder.length, 1); assert.equal(text(holder[0].props.children[1]), sample.holder);
      assert.match(text(tree), /当前没有员工执行/);
      assert.equal(button(tree, "开始处理"), undefined);
      assert.equal(JSON.stringify(data), snapshot);
      assert.equal(gets, 1); assert.equal(teamWrites, 0);
    } finally { delete globalThis.window; }
  });
}


for (const savedTabs of [
  { name: "empty tabs", ids: [], active: "" },
  { name: "blank active tab", ids: ["new:0-1"], active: "new:0-1" },
  { name: "closed current tab", ids: [], active: "current" },
]) {
  test(`General result click selects visible current pane from ${savedTabs.name}`, async () => {
    const previousWindow = globalThis.window, previousObserver = globalThis.ResizeObserver;
    const storage = new Map();
    const scope = 'curis.d0.panes.["result-c","surface:/result-test","/result-test"]';
    storage.set(scope + ".tabs", JSON.stringify(savedTabs));
    const sessionStorage = { getItem: (key) => storage.get(key) ?? null, setItem: (key, value) => storage.set(key, value) };
    globalThis.window = { location: { search: "", origin: "http://curis.local" }, sessionStorage,
      localStorage: { getItem: () => null }, addEventListener() {}, removeEventListener() {}, requestAnimationFrame(fn) { fn(); } };
    globalThis.ResizeObserver = class { observe() {} disconnect() {} };
    let reads = 0, writes = 0;
    const remembered = [];
    const data = { company: { company_id: "result-c" }, workspace: { workspace_id: "result-w", name: "公开测试空间" },
      business: {}, team: { employees: [] }, results: [], operating_readiness: { status: "READY_FOR_WORK" },
      current_work: [{ work_ref: "public-work", lifecycle_status: "COMPLETED", status: "COMPLETED", problem: "公开测试任务",
        result_refs: ["public-result"], evidence_refs: ["public-evidence"], artifact_refs: ["public-artifact"],
        result_summaries: [{ reference_id: "public-result", kind: "RESULT" }, { reference_id: "public-evidence", kind: "EVIDENCE" }, { reference_id: "public-artifact", kind: "ARTIFACT" }] }] };
    const before = JSON.stringify(data);
    const denyWrite = () => { writes++; throw new Error("Result selection must not mutate or execute work"); };
    try {
      const general = hooks(), shell = hooks();
      shell.react.useLayoutEffect = shell.react.useEffect;
      shell.react.useId = () => shell.react.useRef("result-tab-test-").current;
      const General = await compile("components/v1/GeneralWorkspaceOperating.js", general, {
        "next/link": { __esModule: true, default: "a" }, "../../lib/d1State.mjs": helpers,
        "../terra/TerraShell.js": { TerraPaneContent: "pane-content" },
        "./ResultReferenceView.js": { __esModule: true, default: "result-detail",
          resultSelection: (workspaceId, referenceId) => ({ workspaceId, referenceId, explicit: true }),
          generalResultTitleContext: () => null, restoreResultSelection: () => null, rememberResultSelection: (selection) => remembered.push(selection) },
        "../../lib/runtimeApi.js": { getGeneralWorkspace: async () => { reads++; return data; },
          createGeneralWorkspaceWork: denyWrite, executeGeneralWorkspaceWork: denyWrite,
          controlGeneralWorkspaceWork: denyWrite, materializeGeneralWorkspaceTeam: denyWrite },
      });
      const Shell = await compile("components/workspace/WorkspacePaneShell.js", shell, {
        "next/navigation": { usePathname: () => "/result-test" },
        "../runtime/RuntimeProvider.js": { useRuntime: () => ({ companyId: "result-c" }) },
        "../../lib/objectSearchState.mjs": { OBJECT_GROUPS: [] }, "./WorkspacePaneShell.module.css": styles,
      });
      const props = { companyId: "result-c", workspaceId: "result-w", parentPath: { company: {}, department: {}, business: {} } };
      const renderGeneral = () => general.render(General, props);
      renderGeneral(); general.flush(); await new Promise(setImmediate);
      let page = renderGeneral();
      // Exercise the real shared shell with General's descriptors, as TerraShell forwards them.
      const renderShell = () => {
        const descriptor = find(page, (node) => node.type === "pane-content")[0].props;
        const shellProps = { workspaceId: "surface:/result-test", surfaceId: "/result-test", ...descriptor,
          utilityLabel: "结果与证据", utilityAvailable: Boolean(descriptor.utilityPane) };
        shell.render(Shell, shellProps); shell.flush(); return shell.render(Shell, shellProps);
      };
      renderShell();
      for (const [label, referenceId] of [["查看结果 ▸", "public-result"], ["查看证据 ▸", "public-evidence"], ["查看成果 ▸", "public-artifact"]]) {
        button(page, label).props.onClick(); page = renderGeneral();
        let pane = renderShell();
        const visible = find(pane, (node) => node.props?.role === "tabpanel" && !node.props.hidden);
        assert.equal(visible.length, 1, "explicit result click must open and select a content tab");
        const detail = find(visible[0], (node) => node.type === "result-detail")[0];
        assert.ok(detail, "selected tab must contain the requested result, not the blank tab picker");
        assert.deepEqual(detail.props.selection, { workspaceId: "result-w", referenceId, explicit: true });
        assert.equal(detail.props.companyId, "result-c");
        assert.equal(find(pane, (node) => node.type === "section" && node.props["aria-label"] === "结果与证据")[0].props.hidden, false);
        assert.deepEqual(JSON.parse(storage.get(scope + ".tabs")), { ids: ["current"], active: "current" });
        assert.equal(find(pane, (node) => node.props?.role === "tab" && node.props["aria-selected"] === true).length, 1);
        find(pane, (node) => node.type === "button" && node.props["aria-label"] === "关闭标签 · 结果与证据")[0].props.onClick();
        page = renderGeneral(); pane = renderShell();
        assert.equal(find(pane, (node) => node.props?.role === "tabpanel").length, 0, "ordinary rerender must respect user closing the tab");
        button(page, label).props.onClick(); page = renderGeneral(); pane = renderShell();
        assert.equal(find(pane, (node) => node.props?.role === "tabpanel" && !node.props.hidden).length, 1, "a fresh click reopens the same result");
      }
      assert.equal(remembered.length, 6); assert.equal(reads, 1); assert.equal(writes, 0);
      assert.equal(JSON.stringify(data), before);
    } finally {
      if (previousWindow === undefined) delete globalThis.window; else globalThis.window = previousWindow;
      if (previousObserver === undefined) delete globalThis.ResizeObserver; else globalThis.ResizeObserver = previousObserver;
    }
  });
}
