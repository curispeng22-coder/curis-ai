import test from "node:test";
import assert from "node:assert/strict";
import { WRITING_PACKAGE, candidateOutcome, formalVersions, writingCandidates, continuationSources, continuationSource, continuationWorkPayload } from "../lib/writingState.mjs";

// Same component harness as writingChapter.test.mjs: real component source is
// transformed with SWC and rendered against fixture-only APIs. Nothing touches
// the network, a database or the backend.
async function writingComponent(path, props, api = {}) {
  const { readFileSync } = await import("node:fs"); const { createRequire } = await import("node:module"); const vm = await import("node:vm");
  const require = createRequire(import.meta.url), React = require("react"), swc = require("next/dist/build/swc"); await swc.loadBindings();
  const states = [], refs = [], effects = []; let si = 0, ri = 0, ei = 0;
  const storage = api.__storage || new Map(), routes = [], writes = [];
  const hooks = { ...React, useState: initial => { const n = si++; if (!(n in states)) states[n] = initial; return [states[n], value => { states[n] = typeof value === "function" ? value(states[n]) : value; }]; }, useRef: initial => refs[ri++] ||= { current: initial }, useCallback: fn => fn, useMemo: fn => fn(), useEffect: (fn, deps) => { const n = ei++, old = effects[n]; if (!old || !deps || deps.some((v, i) => !Object.is(v, old.deps[i]))) effects[n] = { fn, deps, pending: true, cleanup: old?.cleanup }; } };
  hooks.useLayoutEffect = hooks.useEffect;
  const originalApi = await import("../lib/writingApi.js"), originalState = await import("../lib/writingState.mjs"), originalBookState = await import("../lib/writingBookState.mjs"), scopeHelpers = await import("../components/writing/useWritingSurface.js");
  const source = readFileSync(new URL("../components/writing/" + path, import.meta.url), "utf8");
  const { code } = await swc.transform(source, { filename: path, isModule: true, jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } }, module: { type: "commonjs" } });
  let query = ""; const inert = { __esModule: true, default: props => React.createElement("div", props) }; const loaded = { exports: {} };
  vm.runInNewContext(code, { module: loaded, exports: loaded.exports, URLSearchParams, crypto: globalThis.crypto, localStorage: { getItem: key => storage.get(key) || null, setItem: (key, value) => storage.set(key, value) }, sessionStorage: { getItem: key => storage.get(key) || null, setItem: (key, value) => storage.set(key, value) }, document: { querySelector: () => null }, require: name => {
    if (name === "react") return hooks; if (name === "react/jsx-runtime") return require(name);
    if (name === "next/navigation") return { useRouter: () => ({ push: href => routes.push(href) }), useSearchParams: () => new URLSearchParams(query) };
    if (name.endsWith("v1FrontendApi.js")) return api.__workApi || {};
    if (name.endsWith("writingBookState.mjs")) return originalBookState;
    if (name.endsWith("writingApi.js")) return { ...originalApi, writingApi: api };
    if (name.endsWith("writingState.mjs")) return originalState;
    if (name.endsWith("useWritingSurface.js")) return { __esModule: true, ...scopeHelpers };
    if (name.endsWith("api.js")) return { CEO_ID: "ceo" };
    if (name.endsWith("workspacePackageApi.js")) return { createInstalledWorkspaceObject: async (...args) => { writes.push(args); return { object_id: "new" }; } };
    if (name.endsWith("SharedConversation.js")) return { ConversationComposer: "composer", useConversationModel: () => api.__model || ({ models: [], selected: null }) };
    if (name.endsWith("EmployeeAvatar.js")) return { EmployeeAvatar: "avatar" };
    if (name.endsWith(".module.css")) return { __esModule: true, default: new Proxy({}, { get: (_target, key) => String(key) }) };
    return inert;
  } });
  const render = () => { si = 0; ri = 0; ei = 0; return loaded.exports.default(props); };
  const flush = async () => { render(); for (const e of effects) if (e.pending) { e.cleanup?.(); e.pending = false; e.cleanup = e.fn(); } await new Promise(resolve => setTimeout(resolve, 0)); return render(); };
  const find = (n, pred) => !n ? null : Array.isArray(n) ? n.map(v => find(v, pred)).find(Boolean) : pred(n) ? n : find(n.props?.children, pred);
  const all = (n, pred) => !n || typeof n !== "object" ? [] : Array.isArray(n) ? n.flatMap(v => all(v, pred)) : [...(pred(n) ? [n] : []), ...all(n.props?.children, pred)];
  const text = n => n == null ? "" : Array.isArray(n) ? n.map(text).join("") : typeof n === "object" ? text(n.props?.children) : String(n);
  return { render, flush, find: pred => find(render(), pred), all: pred => all(render(), pred), text: n => text(n), setQuery: value => { query = value; }, routes, writes, storage };
}

const scope = { tenant_id: "selfuse", company_id: "co", workspace_id: "w", instance_id: "i", book_ref: "book", chapter_ref: "chapter", package_id: WRITING_PACKAGE.id, package_version: WRITING_PACKAGE.version, package_digest: WRITING_PACKAGE.digest };
const selection = { draft_ref: "draft", sha256: "hash", start: 0, end: 2, excerpt: "已保存", anchor: "draft:0:2", knowledge: [] };
const candidate = (overrides = {}) => ({ action: "candidate.manual-recorded", ref: "candidate-1", draft_ref: "draft", source_class: "CEO_MANUAL", selection, replacement: "新正文", ...overrides });
const binding = () => ({ action: "discussion.bound", ref: "binding", draft_ref: "draft", discussion_scope: { object_ref: "chapter" }, assignment_ref: "assignment", selection });
const baseState = (events = []) => ({ scope, draft: { ref: "draft", sha256: "hash", text: "已保存正文", knowledge: [] }, events, responsibility: { status: "UNAVAILABLE", reason: "未连接模型" }, read_only: false });
const props = (state, extra = {}) => ({ state, entry: { mode: "chapter", book: "book", chapter: "chapter" }, workspaceId: "w", company: "co", command: async () => ({}), onNavigate() {}, onRefresh() {}, onExecutionLock() {}, onDetails() {}, ...extra });
const readyApi = (extra = {}) => ({ __model: { models: [{ model_key: "model.writing-entry", model_name: "写作模型" }], selected: { model_key: "model.writing-entry", model_name: "写作模型" } }, __workApi: { createAssignedWork: async () => ({ work: { entity_id: "work-1" } }), getAssignedAgentWorkflow: async () => ({ state: "READY" }), publishAssignedAgentWorkflow: async () => ({}) }, ...extra });
const html = h => JSON.stringify(h.render());

// ---------- pure state helpers ----------
test("candidateOutcome reads ADOPTED / REJECTED / PENDING from append-only events", () => {
  const events = [
    { action: "candidate.manual-recorded", ref: "c1" },
    { action: "candidate.rejected", ref: "r1", candidate_ref: "c2", reason: "不符合要求", status: "REJECTED" },
    { action: "candidate.adopted", ref: "a1", candidate_ref: "c3", formal_ref: "f1" },
    { action: "formal.confirmed", ref: "f1", snapshot: { text: "正式稿" } },
  ];
  assert.equal(candidateOutcome(events, "c1").status, "PENDING");
  assert.equal(candidateOutcome(events, "c2").status, "REJECTED");
  assert.equal(candidateOutcome(events, "c2").rejected.reason, "不符合要求");
  assert.equal(candidateOutcome(events, "c3").status, "ADOPTED");
  assert.equal(candidateOutcome(events, "c3").adopted.formal_ref, "f1");
  assert.equal(formalVersions(events).length, 1);
  assert.equal(writingCandidates(events).length, 1);
});

test("续做来源默认最新正式版本、可选历史版本；无正式版本才用候选稿并标注", () => {
  const events = [
    { action: "formal.confirmed", ref: "f1", snapshot: { text: "第一稿" }, created_at: "t1" },
    { action: "formal.confirmed", ref: "f2", snapshot: { text: "第二稿" }, created_at: "t2" },
    { action: "candidate.manual-recorded", ref: "c1", replacement: "候选正文" },
  ];
  const options = continuationSources(events);
  assert.deepEqual(options.map(o => [o.source_ref, o.source_class, o.label]), [["f2", "FORMAL", "最新正式版本"], ["f1", "FORMAL", "历史正式版本"]]);
  assert.equal(continuationSource(events, "").source_ref, "f2");
  assert.equal(continuationSource(events, "f1").text, "第一稿");
  const noFormal = continuationSources([{ action: "candidate.manual-recorded", ref: "c9", replacement: "候选正文" }]);
  assert.equal(noFormal.length, 1);
  assert.equal(noFormal[0].source_class, "CANDIDATE");
  assert.equal(noFormal[0].label, "基于候选稿");
  assert.ok(noFormal.every(o => o.label !== "正式版本"));
  assert.equal(continuationSource([], ""), null);
});

test("续做/要求修改 payload 用后端真实字段；缺要求/模型/选段时拒绝构造", () => {
  const args = { scope: { book_ref: "book", chapter_ref: "chapter" }, draft: { ref: "draft" }, selection: { draft_ref: "draft" }, modelKey: "model.writing-entry", source: { source_ref: "f2", source_class: "FORMAL", label: "最新正式版本" }, requirements: "请改得简洁", requestId: "req-1" };
  const payload = continuationWorkPayload(args);
  assert.equal(payload.problem, "请改得简洁");
  assert.equal(payload.model_key, "model.writing-entry");
  assert.equal(payload.source.kind, "writing");
  assert.equal(payload.source.expected_draft_ref, "draft");
  assert.equal(payload.source.book_ref, "book");
  assert.deepEqual(payload.source.continuation, { source_ref: "f2", requirements: "请改得简洁", confirmed: true });
  assert.equal(continuationWorkPayload({ ...args, requirements: "   " }), null);
  assert.equal(continuationWorkPayload({ ...args, modelKey: "" }), null);
  assert.equal(continuationWorkPayload({ ...args, selection: null }), null);
  assert.equal(continuationWorkPayload({ ...args, mode: "REVISE" }).source.continuation.mode, "REVISE");
});

// ---------- acceptance criterion 1: 采用 ----------
test("采用：一次点击提交 candidate.adopted，防重使重复点击只提交一次；已采用即显示正式版本且不再可点", async () => {
  let release; const commands = [];
  const state = baseState([candidate()]);
  const h = await writingComponent("WritingChapterMain.js", props(state, { command: async (action, data) => { commands.push({ action, data }); return new Promise(r => { release = r; }); } }));
  await h.flush();
  const adopt = () => h.find(n => n.props?.children === "确认采用这处修改");
  assert.ok(adopt());
  const first = adopt().props.onClick();
  const second = adopt().props.onClick();
  assert.equal(commands.length, 1, "按钮防重：第二次点击不会发起第二个采用命令");
  assert.equal(commands[0].action, "candidate.adopted");
  assert.equal(commands[0].data.candidate_ref, "candidate-1");
  assert.equal(commands[0].data.confirmed, true);
  release({ draft: { ref: "draft2", sha256: "h2", text: "新正文", knowledge: [] }, formal_ref: "formal-1" });
  await first; await second;
  // Simulate the server's atomic result: one adoption and exactly one formal version.
  state.events.push({ action: "candidate.adopted", ref: "adoption", candidate_ref: "candidate-1", draft: { ...state.draft, ref: "draft2", text: "新正文" }, formal_ref: "formal-1" });
  state.events.push({ action: "candidate.adopted", ref: "adoption-replay", candidate_ref: "candidate-1", draft: { ...state.draft, ref: "draft2", text: "新正文" }, formal_ref: "formal-1" });
  state.events.push({ action: "formal.confirmed", ref: "formal-1", snapshot: { text: "新正文" }, created_at: "2026-11-14" });
  assert.match(html(h), /已采用 · 正式版本/);
  assert.equal(h.find(n => n.props?.children === "确认采用这处修改"), undefined, "结果幂等：已采用后不再提供采用按钮");
  assert.match(h.text(h.render()), /共 1 份正式版本/, "重复采用不新增正式版本");
  assert.equal(formalVersions(state.events).length, 1);
  assert.match(html(h), /新正文/);
});

// ---------- acceptance criterion 2: 要求修改 ----------
test("要求修改：必须填写意见并确认才提交；取消不创建任何东西、不调用模型", async () => {
  const works = [], commands = [];
  const state = baseState([candidate(), binding()]);
  const api = readyApi(); api.__workApi.createAssignedWork = async (assignment, payload) => { works.push({ assignment, payload }); return { work: { entity_id: "work-revise" } }; };
  const h = await writingComponent("WritingChapterMain.js", props(state, { command: async (action, data) => { commands.push({ action, data }); return {}; } }), api);
  await h.flush();
  h.find(n => n.props?.children === "要求修改").props.onClick();
  assert.equal(h.find(n => n.props?.children === "确认提交").props.disabled, true, "空意见不能提交");
  h.find(n => n.props?.["aria-label"] === "修改意见").props.onChange({ target: { value: "请改得简洁" } });
  assert.equal(h.find(n => n.props?.children === "确认提交").props.disabled, false);
  await h.find(n => n.props?.["aria-label"] === "取消要求修改").props.onClick();
  assert.equal(works.length, 0); assert.equal(commands.length, 0, "取消不创建 Work、不发章节命令");
  assert.equal(h.find(n => n.props?.children === "确认提交"), undefined, "取消关闭表单");
  h.find(n => n.props?.children === "要求修改").props.onClick();
  h.find(n => n.props?.["aria-label"] === "修改意见").props.onChange({ target: { value: "请改得简洁" } });
  await h.find(n => n.props?.children === "确认提交").props.onClick();
  assert.equal(works.length, 1);
  assert.equal(commands.length, 0, "要求修改走 createAssignedWork，不产生章节命令或模型调用");
  const { assignment, payload } = works[0];
  assert.equal(assignment, "assignment");
  assert.equal(payload.problem, "请改得简洁");
  assert.equal(payload.model_key, "model.writing-entry");
  assert.equal(payload.source.kind, "writing");
  assert.equal(payload.source.expected_draft_ref, "draft");
  assert.deepEqual(payload.source.continuation, { source_ref: "candidate-1", requirements: "请改得简洁", confirmed: true, mode: "REVISE" });
});

// ---------- acceptance criterion 3: 拒绝 ----------
test("拒绝：确认后发 candidate.rejected，之后显示已拒绝且原稿仍可查看", async () => {
  const commands = [];
  const state = baseState([candidate()]);
  const h = await writingComponent("WritingChapterMain.js", props(state, { command: async (action, data) => { commands.push({ action, data }); return {}; } }));
  await h.flush();
  h.find(n => n.props?.children === "拒绝").props.onClick();
  h.find(n => n.props?.["aria-label"] === "拒绝理由").props.onChange({ target: { value: "不符合要求" } });
  await h.find(n => n.props?.children === "确认拒绝").props.onClick();
  assert.equal(commands.length, 1);
  assert.equal(commands[0].action, "candidate.rejected");
  assert.equal(commands[0].data.candidate_ref, "candidate-1");
  assert.equal(commands[0].data.reason, "不符合要求");
  state.events.push({ action: "candidate.rejected", ref: "reject-1", candidate_ref: "candidate-1", reason: "不符合要求", status: "REJECTED" });
  const view = html(h);
  assert.match(view, /已拒绝/);
  assert.match(view, /原选段/); assert.match(view, /将替换为/);
  assert.match(view, /已保存/, "原稿内容仍可查看");
  assert.match(view, /新正文/, "原候选内容仍保留");
  assert.equal(h.find(n => n.props?.children === "确认采用这处修改"), undefined, "已拒绝候选不能再采用");
});

// ---------- acceptance criterion 4: 续做来源 ----------
test("续做：默认最新正式版本、可选历史版本并显示来源", async () => {
  const state = baseState([
    { action: "formal.confirmed", ref: "formal-old", snapshot: { text: "第一稿" }, created_at: "2026-10-25" },
    { action: "formal.confirmed", ref: "formal-new", snapshot: { text: "第二稿" }, created_at: "2026-10-26" },
    binding(),
  ]);
  const h = await writingComponent("WritingChapterMain.js", props(state), readyApi());
  await h.flush();
  const select = () => h.find(n => n.props?.["aria-label"] === "续做来源");
  assert.ok(select());
  assert.deepEqual(select().props.children.map(o => o.props.value), ["formal-new", "formal-old"]);
  assert.equal(select().props.value, "formal-new", "默认选中最新正式版本");
  assert.match(JSON.stringify(select().props.children[0]), /最新正式版本/);
  assert.match(JSON.stringify(select().props.children[1]), /历史正式版本/);
  assert.match(html(h), /第二稿/); assert.match(html(h), /正式版本/); assert.match(html(h), /formal-new/);
  select().props.onChange({ target: { value: "formal-old" } });
  assert.equal(select().props.value, "formal-old");
  assert.match(html(h), /第一稿/); assert.match(html(h), /历史正式版本/); assert.match(html(h), /formal-old/);
});

test("续做：无正式版本时明确标注基于候选稿并据此创建续做工作；取消不创建", async () => {
  const works = [];
  const state = baseState([candidate(), binding()]);
  const api = readyApi(); api.__workApi.createAssignedWork = async (assignment, payload) => { works.push({ assignment, payload }); return { work: { entity_id: "work-cont" } }; };
  const h = await writingComponent("WritingChapterMain.js", props(state), api);
  await h.flush();
  const select = () => h.find(n => n.props?.["aria-label"] === "续做来源");
  assert.equal(select().props.children.length, 1);
  assert.equal(select().props.children[0].props.value, "candidate-1");
  assert.match(JSON.stringify(select().props.children[0]), /基于候选稿/);
  assert.match(html(h), /基于候选稿（无正式版本）/);
  assert.ok(!JSON.stringify(select().props.children).includes("最新正式版本"), "没有正式版本时不提供最新正式版本选项");
  // Cancel creates nothing.
  h.find(n => n.props?.children === "续做").props.onClick();
  h.find(n => n.props?.["aria-label"] === "续做修改要求").props.onChange({ target: { value: "不会提交" } });
  await h.find(n => n.props?.["aria-label"] === "取消续做").props.onClick();
  assert.equal(works.length, 0);
  // Confirm builds a continuation based on the explicitly labelled candidate.
  h.find(n => n.props?.children === "续做").props.onClick();
  h.find(n => n.props?.["aria-label"] === "续做修改要求").props.onChange({ target: { value: "继续往下写" } });
  assert.equal(h.find(n => n.props?.children === "确认续做").props.disabled, false);
  await h.find(n => n.props?.children === "确认续做").props.onClick();
  assert.equal(works.length, 1);
  const payload = works[0].payload;
  assert.equal(payload.problem, "继续往下写");
  assert.equal(payload.source.continuation.source_ref, "candidate-1");
  assert.equal(payload.source.continuation.confirmed, true);
  assert.notEqual(payload.source.continuation.mode, "REVISE", "续做用后端默认 CONTINUE 模式");
  assert.equal(continuationSources(state.events)[0].source_class, "CANDIDATE");
});

test("a confirmed continuation survives remount and sends the same Work and request", async () => {
  const works = [], sends = [], storage = new Map();
  const state = { ...baseState([
    binding(),
    { action: "formal.confirmed", ref: "formal-1", snapshot: { text: "已采用正文" } },
  ]), responsibility: { status: "AVAILABLE" } };
  const api = readyApi({ __storage: storage });
  api.__workApi.createAssignedWork = async (_assignment, payload) => {
    works.push(payload);
    return { work: { entity_id: "work-next" } };
  };
  const attempt = { attempt_id: "attempt-next", message_id: "message-next", status: "COMPLETED", effect_status: "SETTLED" };
  api.send = async (_company, _workspace, _entry, payload) => { sends.push(payload); return { attempt }; };
  api.discussion = async () => ({ attempts: [attempt], messages: [] });
  let view = await writingComponent("WritingChapterMain.js", props(state), api);
  await view.flush();
  view.find(node => node.props?.children === "续做").props.onClick();
  view.find(node => node.props?.["aria-label"] === "续做修改要求").props.onChange({ target: { value: "改写结尾" } });
  await view.find(node => node.props?.children === "确认续做").props.onClick();
  assert.equal(works[0].source.continuation.source_ref, "formal-1");
  assert.equal(sends.length, 0);

  view = await writingComponent("WritingChapterMain.js", props(state), api);
  await view.flush();
  await view.find(node => node.props?.children === "继续原交办").props.onClick({ preventDefault() {} });
  assert.equal(works.length, 1);
  assert.equal(sends.length, 1);
  assert.equal(sends[0].request_id, works[0].request_id);
  assert.equal(sends[0].work_ref, "work-next");
  assert.equal(sends[0].body, "改写结尾");
  assert.equal(sends[0].retry_no, 0);
});
