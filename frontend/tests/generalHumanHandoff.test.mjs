import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import test from "node:test";
import * as workHelpers from "../lib/d1State.mjs";

const require = createRequire(import.meta.url);
const React = require("react");
const { renderToStaticMarkup } = require("react-dom/server");
const { transform, loadBindings } = require("next/dist/build/swc");
const read = (path) => readFileSync(new URL(`../${path}`, import.meta.url), "utf8");

async function compile(path, imports) {
  await loadBindings();
  const { code } = await transform(read(path), {
    filename: path, jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "classic" } } },
    module: { type: "commonjs" },
  });
  const mod = { exports: {} };
  new Function("require", "module", "exports", "React", code)((name) => imports[name] ?? imports.default ?? {}, mod, mod.exports, React);
  return mod.exports;
}

function hookHarness() {
  const slots = [];
  let index = 0;
  return {
    React: {
      createElement(type, props, ...children) { return { type, props: { ...props, children } }; },
      useState(initial) {
        const at = index++;
        if (!(at in slots)) slots[at] = initial;
        return [slots[at], (value) => { slots[at] = value; }];
      },
      useRef(initial) {
        const at = index++;
        if (!(at in slots)) slots[at] = { current: initial };
        return slots[at];
      },
    },
    reset() { index = 0; },
  };
}

function visit(node, predicate, found = []) {
  if (Array.isArray(node)) { for (const child of node) visit(child, predicate, found); return found; }
  if (!node || typeof node !== "object") return found;
  if (predicate(node)) found.push(node);
  visit(node.props?.children, predicate, found);
  return found;
}

function nodeText(node) {
  if (Array.isArray(node)) return node.map(nodeText).join("");
  if (node == null || typeof node === "boolean") return "";
  if (typeof node !== "object") return String(node);
  return nodeText(node.props?.children);
}

async function compiledInteractiveWorkView(harness) {
  const styles = new Proxy({}, { get: (_, key) => key });
  const mod = await compile("components/delivery/d1/WorkView.js", {
    react: harness.React,
    "../../../lib/d1Api.js": { d1Error: () => "请重新读取" },
    "../../../lib/d1State.mjs": { ...workHelpers, lifecycleActions: () => [] },
    "./CeoMatterView.js": { workState: (value) => value },
    "./D1.module.css": { __esModule: true, default: styles },
    "../../../lib/runtimeApi.js": { workspaceEntryHref: (value) => `/workspace/${value}` },
  });
  return mod.default;
}

test("scoped Human Input API sends revision and original Work without a Task key", async () => {
  const calls = [];
  const request = async (path, options) => { calls.push([path, options]); return { ok: true }; };
  const api = await compile("lib/runtimeApi.js", { "./api.js": { workspaceFetch: request } });
  await api.reportGeneralHumanInput("c", "w", "work:1", "human:1", { revision: 1, submission_id: "s1", kind: "LOCAL_INFORMATION", local_text: "事实" }, request);
  await api.reviewGeneralHumanInput("c", "w", "work:1", "human:1", 2, request);
  await api.continueGeneralHumanInput("work:1", "human:1", 3, "s1", request);
  assert.equal(calls.length, 3);
  assert.match(calls[0][0], /work%3A1\/human-input\/human%3A1\/report$/);
  assert.deepEqual(JSON.parse(calls[1][1].body), { revision: 2 });
  assert.deepEqual(JSON.parse(calls[2][1].body), { revision: 3, submission_id: "s1" });
  assert.doesNotMatch(calls[2][0], /task-runs|execution_key/);
});

test("compiled Work detail displays six facts, keeps external report unknown, and offers local continuation", async () => {
  const styles = new Proxy({}, { get: (_, key) => key });
  const mod = await compile("components/delivery/d1/WorkView.js", {
    react: React,
    "../../../lib/d1Api.js": { d1Error: () => "请重新读取" },
    "../../../lib/d1State.mjs": { ...workHelpers, lifecycleActions: () => [] },
    "./CeoMatterView.js": { workState: (value) => value },
    "./D1.module.css": { __esModule: true, default: styles },
    "../../../lib/runtimeApi.js": { workspaceEntryHref: (value) => `/workspace/${value}` },
  });
  const base = { work_ref: "work-1", workspaceId: "w", problem: "原问题", status: "WAITING", result_refs: [],
    human_input: { requestId: "human-1", revision: 1, state: "WAITING_INPUT", kind: "LOCAL_INFORMATION",
      aiCompleted: "已梳理资料", whyUser: "缺少反馈", userAction: "提供摘要", destination: "原工作",
      doneCriterion: "摘要可读", resumePlan: "继续分析" } };
  const props = { work: base, api: {}, companyId: "c", onResult: () => {}, onDiscuss: () => {}, onRefresh: () => {}, onEmployeeDetail: () => {} };
  const local = renderToStaticMarkup(React.createElement(mod.default, props));
  for (const fact of ["已梳理资料", "缺少反馈", "提供摘要", "原工作", "摘要可读", "继续分析"]) assert.match(local, new RegExp(fact));
  assert.match(local, /提交到原工作/);
  assert.doesNotMatch(local, /续接原工作一次/);
  const external = renderToStaticMarkup(React.createElement(mod.default, { ...props, work: { ...base,
    human_input: { ...base.human_input, kind: "EXTERNAL_ACTION_REPORT", state: "EXTERNAL_REPORTED_UNKNOWN",
      report: { text: "用户自述已提交" } } } }));
  assert.match(external, /外部事实未知/);
  assert.doesNotMatch(external, /续接原工作一次/);
  const ready = renderToStaticMarkup(React.createElement(mod.default, { ...props, work: { ...base,
    human_input: { ...base.human_input, state: "READY", report: { text: "本地摘要", submissionId: "s1" } } } }));
  assert.match(ready, /续接原工作一次/);
});

test("compiled unknown report keeps draft and submission key locked until a fresh original Work read", async () => {
  const harness = hookHarness();
  const WorkView = await compiledInteractiveWorkView(harness);
  const human = { requestId: "human-1", revision: 1, state: "WAITING_INPUT", kind: "LOCAL_INFORMATION",
    targetRef: "work-1", aiCompleted: "已看资料", whyUser: "缺摘要", userAction: "提供摘要",
    destination: "原工作", doneCriterion: "摘要可读", resumePlan: "继续分析" };
  const originalWork = { work_ref: "work-1", workspaceId: "w", problem: "原问题", status: "WAITING",
    lifecycle_status: "ACTIVE", result_refs: [], human_input: human };
  const sent = [];
  let refreshes = 0;
  let first = true;
  const props = { work: originalWork, companyId: "c", api: { reportHumanInput: async (_company, _work, body) => {
    sent.push(body.submission_id);
    if (first) { first = false; throw new Error("unknown network outcome"); }
  } }, onRefresh: async () => { refreshes++; }, onResult() {}, onDiscuss() {}, onEmployeeDetail() {} };
  const render = () => { harness.reset(); return WorkView(props); };
  let tree = render();
  visit(tree, (node) => node.type === "textarea")[0].props.onChange({ target: { value: "保留摘要" } });
  tree = render();
  const report = (view) => visit(view, (node) => node.type === "form" && nodeText(node).includes("补充本地信息"))[0];
  await report(tree).props.onSubmit({ preventDefault() {} });
  tree = render();
  assert.equal(refreshes, 1);
  assert.equal(visit(tree, (node) => node.type === "textarea")[0].props.value, "保留摘要");
  assert.equal(visit(tree, (node) => node.type === "button" && nodeText(node).includes("提交到原工作"))[0].props.disabled, true);
  await report(tree).props.onSubmit({ preventDefault() {} });
  assert.equal(sent.length, 1, "unknown result must not be blindly retried");
  props.work = { ...originalWork };
  tree = render();
  await report(tree).props.onSubmit({ preventDefault() {} });
  assert.equal(sent.length, 1, "a new object reference is not a successful readback");
  props.onRefresh = async () => ({ ...originalWork, companyId: "c" });
  tree = render();
  await visit(tree, (node) => node.type === "button" && nodeText(node).includes("重新读取原工作"))[0].props.onClick();
  tree = render();
  await report(tree).props.onSubmit({ preventDefault() {} });
  assert.equal(sent.length, 1, "unchanged revision/state is still an unknown effect");
  const reported = { ...originalWork, companyId: "c", human_input: { ...human, revision: 2, state: "LOCAL_REPORTED",
    report: { submissionId: sent[0], text: "保留摘要", referenceRefs: [] } } };
  props.onRefresh = async () => reported;
  tree = render();
  await visit(tree, (node) => node.type === "button" && nodeText(node).includes("重新读取原工作"))[0].props.onClick();
  props.work = reported;
  tree = render();
  assert.equal(visit(tree, (node) => node.type === "button" && nodeText(node) === "核对本地补充")[0].props.disabled, false);
  assert.equal(sent.length, 1, "confirmed report never replays the original POST");
});

test("compiled invalid revision cannot report and expired continuation stays disabled", async () => {
  const harness = hookHarness();
  const WorkView = await compiledInteractiveWorkView(harness);
  const human = { requestId: "human-1", revision: 1, state: "WAITING_INPUT", kind: "LOCAL_INFORMATION",
    targetRef: "work-1", aiCompleted: "已看资料", whyUser: "缺摘要", userAction: "提供摘要",
    destination: "原工作", doneCriterion: "摘要可读", resumePlan: "继续分析" };
  let reports = 0;
  const props = { work: { work_ref: "work-1", workspaceId: "w", status: "WAITING", result_refs: [],
    human_input: { ...human, revision: 0 } },
    companyId: "c", api: { reportHumanInput: async () => { reports++; } },
    onRefresh() {}, onResult() {}, onDiscuss() {}, onEmployeeDetail() {} };
  harness.reset();
  const invalid = WorkView(props);
  const reportForm = visit(invalid, (node) => node.type === "form" && nodeText(node).includes("补充本地信息"))[0];
  await reportForm.props.onSubmit({ preventDefault() {} });
  assert.equal(reports, 0, "invalid current revision cannot submit");
  props.work = { ...props.work, human_input: { ...human, state: "READY", expiresAt: "2020-01-01T00:00:00Z",
    report: { submissionId: "s1", text: "摘要" } } };
  harness.reset();
  const expired = WorkView(props);
  const continuation = visit(expired, (node) => node.type === "button" && nodeText(node).includes("续接原工作一次"))[0];
  assert.equal(continuation.props.disabled, true);
  assert.match(nodeText(expired), /员工报告的进展/);
  assert.match(nodeText(expired), /已过期或范围发生变化/);
});

test("all affected JSX consumers compile with the installed offline compiler", async () => {
  await loadBindings();
  for (const path of ["components/v1/GeneralWorkspaceOperating.js", "app/ceo-office/execution/tasks/[id]/page.js"] ) {
    const { code } = await transform(read(path), { filename: path, jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "classic" } } }, module: { type: "commonjs" } });
    assert.ok(code.length > 100);
  }
});
