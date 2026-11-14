import assert from "node:assert/strict";
import test from "node:test";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import vm from "node:vm";

const require = createRequire(import.meta.url), React = require("react");
const cgState = await import("../lib/contentGrowthState.mjs");
const swc = require("next/dist/build/swc");
await swc.loadBindings();
const sources = {
  workspace: "components/content-growth/ContentGrowthWorkspace.js",
  main: "components/content-growth/ContentGrowthMain.js",
  accounts: "components/content-growth/ContentGrowthAccounts.js",
  verify: "components/content-growth/ContentGrowthVerify.js",
  observe: "components/content-growth/ContentGrowthObserve.js",
  learning: "components/content-growth/ContentGrowthLearning.js",
  materials: "components/content-growth/ContentGrowthMaterials.js",
  host: "components/workspace/WorkspacePaneShell.js",
  analysis: "components/content-growth/ContentGrowthAnalysis.js",
};
const compiled = {};
for (const [name, path] of Object.entries(sources)) {
  compiled[name] = (await swc.transform(readFileSync(new URL(`../${path}`, import.meta.url), "utf8"), {
    filename: path, isModule: true, jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } }, module: { type: "commonjs" },
  })).code;
}

// Drive the actual compiled consumers with deterministic hooks and deferred API reads; no App or DB.
function scene(name, api, runtime = { status: "ready", companyId: "a", snapshot: { company: { name: "A" } } }, query = "") {
  const slots = [], pending = []; let cursor = 0, tree;
  const same = (a, b) => a && b && a.length === b.length && a.every((item, i) => Object.is(item, b[i]));
  const hooks = {
    useState(initial) { const i = cursor++; if (!(i in slots)) slots[i] = { value: typeof initial === "function" ? initial() : initial }; return [slots[i].value, (value) => { slots[i].value = typeof value === "function" ? value(slots[i].value) : value; }]; },
    useRef(initial) { const i = cursor++; return slots[i] ||= { current: initial }; },
    useMemo(fn, deps) { const i = cursor++; if (!slots[i] || !same(slots[i].deps, deps)) slots[i] = { deps, value: fn() }; return slots[i].value; },
    useCallback(fn, deps) { return hooks.useMemo(() => fn, deps); },
    useLayoutEffect(fn, deps) { return hooks.useEffect(fn, deps); },
    useId() { return "fixture-pane"; },
    useContext() { return api.paneSetter; },
    useEffect(fn, deps) { const i = cursor++; if (!slots[i] || !same(slots[i].deps, deps)) { const previous = slots[i]; slots[i] = { deps }; pending.push(() => { previous?.cleanup?.(); slots[i].cleanup = fn(); }); } },
  };
  function TerraPaneContent(props) { return React.createElement("utility", props); }
  const primitive = (tag) => function Primitive({ children, ...props }) { return React.createElement(tag, props, children); };
  const primitives = new Proxy({}, { get: (_, key) => key === "__esModule" ? true : primitive("div") });
  const loaded = { exports: {} }, storage = api.storage || new Map();
  const storageAPI = { getItem: (key) => storage.get(key) || null, setItem: (key, value) => storage.set(key, value), removeItem: (key) => storage.delete(key) };
  vm.runInNewContext(compiled[name], {
    module: loaded, exports: loaded.exports, URLSearchParams, URL, Blob, console, crypto: globalThis.crypto, TextEncoder, location: { pathname: "/ceo-office/knowledge", search: "", assign: (value) => { api.returned = value; } }, scrollY: 0,
    sessionStorage: storageAPI, localStorage: storageAPI,
    requestAnimationFrame: (fn) => fn(), scrollTo() {},
    window: { location: { search: query, origin: "http://127.0.0.1:3010" }, sessionStorage: storageAPI, localStorage: storageAPI, requestAnimationFrame: (fn) => fn(), addEventListener() {}, removeEventListener() {} },
    ResizeObserver: class { observe() {} disconnect() {} },
    document: { activeElement: { focus() {} } },
    require: (path) => {
      if (path === "react") return { ...React, ...hooks };
      if (path === "react/jsx-runtime") return require(path);
      if (path === "next/link") return { __esModule: true, default: primitive("a") };
      if (path === "next/navigation") return { useSearchParams: () => new URLSearchParams(api.query || query), useRouter: () => ({ push: (href) => { api.pushed = href; } }), useParams: () => ({ id: "doc" }), usePathname: () => "/ceo-office/knowledge" };
      if (path.includes("v1FrontendApi")) return { getAssignedAgentWorkflow: api.getAssignedAgentWorkflow || (async () => ({ state: "READY" })), publishAssignedAgentWorkflow: api.publishAssignedAgentWorkflow || (async () => ({})), createAssignedWork: api.createAssignedWork };
      if (path.includes("RuntimeProvider")) return { useRuntime: () => runtime };
      if (path.includes("WorkspacePaneShell") && api.hostComponent) return { __esModule: true, default: api.hostComponent };
      if (path.includes("TerraShell")) return { __esModule: true, default: primitive("main"), TerraPaneContent };
      if (path.includes("GlobalAssistant")) return { useAssistantPageContext() {} };
      if (path.includes("theme.js")) return { roleLabel: (value) => value };
      if (path.includes("EmployeeAvatar")) return { EmployeeAvatar: primitive("span"), EMPLOYEE_AVATAR_PRESETS: [] };
      if (path.endsWith("/api.js")) return { TENANT_ID: scope.tenant_id };
      if (path.includes("contentGrowthState")) return cgState;
      if (path.includes("contentGrowthApi")) return { contentGrowthApi: api, cgRepairHref: (path, href) => `${path}?return_to=${encodeURIComponent(href)}` };
      if (path.endsWith(".module.css")) return { __esModule: true, default: new Proxy({}, { get: (_, key) => String(key) }) };
      if (path.endsWith("ContentGrowthMarket.js")) return { GrowthRecordPanel: primitive("div") };
      if (path.endsWith("ContentGrowthVerify.js")) { const Component = primitive("div"); Object.defineProperty(Component, "name", { value: "ContentGrowthVerify" }); return { __esModule: true, default: Component, verifySourceContent: scene("verify", api, runtime).exports.verifySourceContent }; }
      if (/ContentGrowth[A-Za-z]+\.js$/.test(path)) { const name = path.split("/").at(-1).replace(".js", ""); const Component = primitive("div"); Object.defineProperty(Component, "name", { value: name }); return { __esModule: true, default: Component }; }
      if (path.includes("lib/")) return api;
      return primitives;
    },
  });
  return {
    exports: loaded.exports,
    render(component, props = {}) { cursor = 0; tree = component(props); while (pending.length) pending.shift()(); return tree; },
    unmount() { slots.forEach((slot) => slot.cleanup?.()); },
    get tree() { return tree; },
  };
}
const tick = () => new Promise((resolve) => setImmediate(resolve));
const deferred = () => { let resolve; const promise = new Promise((r) => { resolve = r; }); return { promise, resolve }; };
function nodes(tree, predicate) {
  const found = [];
  function visit(node) {
    if (!node || typeof node !== "object") return;
    if (Array.isArray(node)) return node.forEach(visit);
    if (predicate(node)) found.push(node);
    visit(node.props?.children);
  }
  visit(tree); return found;
}
const text = (tree) => {
  if (tree == null || typeof tree === "boolean") return "";
  if (typeof tree !== "object") return String(tree);
  if (Array.isArray(tree)) return tree.map(text).join("");
  return text(tree.props?.children);
};
const button = (tree, label) => nodes(tree, (node) => node.type === "button" && text(node) === label)[0];




const scope = { tenant_id: "t", company_id: "A", workspace_id: "w", business_id: "biz" };
const entry = { scope, actor: "ceo", definition: { package_id: cgState.CG_PACKAGE_V02.id, version: cgState.CG_PACKAGE_V02.version, digest: cgState.CG_PACKAGE_V02.digest }, assignments: [], publication_status: "INTERNAL_CANDIDATE_NO_PUBLICATION" };
const collection = () => ({ entry, contents: [], reference_options: [], pending_requests: [], execution_authorized: false, execution_notice: "需准确授权" });
const detail = { instance: { company_id: "A", workspace_id: "w", instance_id: "i", package_id: entry.definition.package_id, package_version: entry.definition.version, package_digest: entry.definition.digest }, package: { package_id: entry.definition.package_id, version: entry.definition.version, digest: entry.definition.digest, schema_version: "curis.workspace-package/v1" }, schemas: { ContentWork: { schemaVersion: "0.2.0" } } };
const account = (id, platform = "xhs") => ({ entity_id: id, company_id: "A", workspace_id: "other-workspace", data: { business_ref: "biz", platform_ref: platform, name: id, growth_stage: "cold_start", status: "active" } });
const accountsPayload = () => ({ entry, catalog: [{ platform: "xhs", name: "小红书" }, { platform: "douyin", name: "抖音" }], accounts: [account("one"), account("two", "douyin")] });
const sourceAPI = () => ({ collection: async () => collection(), accounts: async () => accountsPayload(), account: async (_, __, id) => account(id), verifications: async () => ({ entry, verifications: [] }), observations: async () => ({ entry, observations: [] }) });
const runtime = { status: "ready", companyId: "A", snapshot: { company: { name: "A" } } };
const labelInput = (tree, label) => { const node = nodes(tree, (node) => node.type === "label" && text(node).startsWith(label))[0]; return nodes(node, (child) => child.type === "input")[0]; };

test("CG view locators extend only existing routes and keep original content/version identity", () => {
  for (const view of ["operating", "market", "production", "analysis", "accounts", "verify", "observe", "learning", "materials"]) {
    const href = cgState.contentHref("w", { view }); assert.equal(cgState.cgReturnTarget(href).entry.view, view);
  }
  assert.throws(() => cgState.cgReturnTarget("/ceo-office/workspace/installed/w?cg_view=fake-publish"));
  const original = cgState.cgReturnTarget(cgState.contentHref("w", { content: "c", version: "v", start: 0, end: 1 }));
  assert.equal(original.entry.content, "c"); assert.equal(original.entry.version, "v"); assert.equal(original.entry.start, 0);
  assert.equal(cgState.cgScopedRead({ entry }, "A", "w").entry, entry);
  assert.throws(() => cgState.cgScopedRead({ entry: { ...entry, scope: { ...scope, company_id: "B" } } }, "A", "w"));
});

test("manual candidate locator and draft stay on exact author, content, basis and candidate", () => {
  const href = cgState.contentHref("w", { content: "content-1", version: "basis-1", candidate: "candidate-1" });
  const parsed = cgState.cgReturnTarget(href);
  assert.equal(parsed.entry.candidate, "candidate-1"); assert.equal(parsed.entry.version, "basis-1");
  assert.throws(() => cgState.cgReturnTarget("/ceo-office/workspace/installed/w?cg_content=c&cg_candidate=x"));
  assert.throws(() => cgState.cgReturnTarget(href + "&cg_candidate=other"));
  const context = ["A", "w", "content-1", "candidate-1", "a".repeat(64), "basis-1", "ceo"];
  const draft = { context, at: 1000, action: "ACCEPT", reason: "同意", request_id: "id" };
  assert.equal(cgState.restoreCgFeedback(JSON.stringify(draft), context, 1001).reason, "同意");
  assert.equal(cgState.restoreCgFeedback(JSON.stringify(draft), [...context.slice(0, 3), "other", ...context.slice(4)], 1001), null);
  assert.equal(cgState.restoreCgFeedback(JSON.stringify(draft), context, 1000 + 31 * 60 * 1000), null);
  assert.notEqual(cgState.cgFeedbackKey("A", "w", "content-1", "candidate-1", "a".repeat(64), "ceo"), cgState.cgFeedbackKey("A", "w", "content-1", "candidate-2", "a".repeat(64), "ceo"));
});

test("compiled manual candidate Main confirms, sends and reads back the exact candidate receipt", async () => {
  const data = { ...cgState.cgDraftOf(null, true), title: "正文", topic: "主题", audience: "受众", body: "原文" };
  const basis = { entity_id: "basis", entity_type: "CONTENT_VERSION", parent_id: "content", tenant_id: "t", company_id: "A", workspace_id: "w", data };
  const version = { ...basis, entity_id: "candidate", owner_ref: "ceo", data: { ...data, body: "人工候选", kind: "candidate", source_class: "MANUAL_CANDIDATE", manual_actor: "ceo", basis_version_ref: "basis" } };
  const candidate = { version, eligible: true, reasons: [], feedback_version: "a".repeat(64), feedback: null };
  const row = { content: { entity_id: "content", tenant_id: "t", company_id: "A", workspace_id: "w" }, version: basis, versions: [basis, version], candidates: [candidate] };
  let sent, reloaded = 0, reads = 0;
  const api = { content: async () => { reads += 1; return sent && reads > 1 ? { ...row, candidates: [{ ...candidate, feedback: { ...sent, tenant_id: "t", company_id: "A", workspace_id: "w", content_ref: "content", ceo_id: "ceo", receipt_ref: 1 } }] } : row; },
    feedback: async (_c, _w, _r, payload) => { sent = payload; return { ...payload, receipt_ref: 1 }; } };
  const h = scene("main", api, runtime), props = { company: "A", workspaceId: "w", entry: { candidate: "candidate", version: "basis" }, row,
    collection: collection(), busy: false, locked: false, onInspect() {}, perform() {}, reload: async () => { reloaded += 1; } };
  const render = () => h.render(h.exports.default, props);
  render(); render();
  const choice = nodes(h.tree, (node) => node.type === "input" && node.props.type === "radio" && node.props.name === "cg-feedback-candidate" && node.props.checked === false)[0];
  choice.props.onChange(); render();
  const reason = nodes(h.tree, (node) => node.type === "textarea" && node.props.value === "" && node.props["aria-label"] !== "内容正文与脚本")[0];
  reason.props.onChange({ target: { value: "已核对人工候选" } }); render();
  const confirmation = nodes(h.tree, (node) => node.type === "input" && node.props.type === "checkbox" && text(node) === "")[0];
  // The confirmation checkbox follows the feedback reason, before adoption checks.
  const checks = nodes(h.tree, (node) => node.type === "input" && node.props.type === "checkbox");
  assert.ok(confirmation); checks[0].props.onChange({ target: { checked: true } }); render();
  const save = button(h.tree, "保存候选评价"); assert.equal(save.props.disabled, false);
  await save.props.onClick();
  assert.equal(sent.candidate_ref, "candidate"); assert.equal(sent.basis_version_ref, "basis"); assert.equal(sent.candidate_version, "a".repeat(64));
  assert.equal(sent.action, "ACCEPT"); assert.equal(sent.reason, "已核对人工候选"); assert.equal(reloaded, 1);

  sent = null; reads = 0;
  let posts = [];
  api.content = async () => {
    reads++;
    if (reads === 2 || reads === 3) throw new Error("recovery unavailable");
    return sent ? { ...row, candidates: [{ ...candidate, feedback: { ...sent, tenant_id: "t", company_id: "A", workspace_id: "w", content_ref: "content", ceo_id: "ceo", receipt_ref: 2 } }] } : row;
  };
  api.feedback = async (_c, _w, _r, payload) => {
    posts.push(payload.request_id);
    if (posts.length === 1) throw new Error("unknown");
    sent = payload;
  };
  render();
  nodes(h.tree, (node) => node.type === "input" && node.props.type === "radio" && node.props.name === "cg-feedback-candidate")[0].props.onChange(); render();
  nodes(h.tree, (node) => node.type === "textarea" && node.props.value === "" && node.props["aria-label"] !== "内容正文与脚本")[0].props.onChange({ target: { value: "第二次核对" } }); render();
  nodes(h.tree, (node) => node.type === "input" && node.props.type === "checkbox")[0].props.onChange({ target: { checked: true } }); render();
  await button(h.tree, "保存候选评价").props.onClick();
  assert.equal(posts.length, 1);
  const id = posts[0];
  render();
  nodes(h.tree, (node) => node.type === "input" && node.props.type === "checkbox")[0].props.onChange({ target: { checked: true } }); render();
  await button(h.tree, "保存候选评价").props.onClick();
  assert.equal(posts.length, 1, "failed recovery GET must prevent another POST");
  render();
  nodes(h.tree, (node) => node.type === "input" && node.props.type === "checkbox")[0].props.onChange({ target: { checked: true } }); render();
  await button(h.tree, "保存候选评价").props.onClick();
  assert.deepEqual(posts, [id, id]);
  h.unmount();
});

test("compiled candidate feedback ignores late old-object and unmounted reads", async () => {
  const makeRow = (id) => {
    const data = { ...cgState.cgDraftOf(null, true), title: "正文", topic: "主题", audience: "受众", body: "原文" };
    const basis = { entity_id: `basis-${id}`, entity_type: "CONTENT_VERSION", parent_id: `content-${id}`, tenant_id: "t", company_id: "A", workspace_id: "w", data };
    const version = { ...basis, entity_id: `candidate-${id}`, owner_ref: "ceo", data: { ...data, body: "人工候选", kind: "candidate", source_class: "MANUAL_CANDIDATE", manual_actor: "ceo", basis_version_ref: basis.entity_id } };
    const candidate = { version, eligible: true, reasons: [], feedback_version: "a".repeat(64), feedback: null };
    return { content: { entity_id: `content-${id}`, tenant_id: "t", company_id: "A", workspace_id: "w" }, version: basis, versions: [basis, version], candidates: [candidate] };
  };
  const storage = new Map(), oldRead = deferred(), unmountedRead = deferred();
  let posts = 0, reloads = 0, row = makeRow("old");
  const api = { storage, content: () => row.content.entity_id === "content-old" ? oldRead.promise : unmountedRead.promise,
    feedback: async () => { posts++; } };
  const h = scene("main", api, runtime);
  const props = () => ({ company: "A", workspaceId: "w", entry: { candidate: row.candidates[0].version.entity_id, version: row.version.entity_id }, row,
    collection: collection(), busy: false, locked: false, onInspect() {}, perform() {}, reload: async () => { reloads++; } });
  const render = () => h.render(h.exports.default, props());
  const choose = () => {
    render(); render();
    nodes(h.tree, (node) => node.type === "input" && node.props.type === "radio" && node.props.name === `cg-feedback-${row.candidates[0].version.entity_id}`)[0].props.onChange(); render();
    nodes(h.tree, (node) => node.type === "textarea" && node.props.value === "" && node.props["aria-label"] !== "内容正文与脚本")[0].props.onChange({ target: { value: "待核对理由" } }); render();
    nodes(h.tree, (node) => node.type === "input" && node.props.type === "checkbox")[0].props.onChange({ target: { checked: true } }); render();
    return button(h.tree, "保存候选评价").props.onClick();
  };
  const oldSubmit = choose();
  row = makeRow("new"); render(); render();
  const newKey = cgState.cgFeedbackKey("A", "w", row.content.entity_id, row.candidates[0].version.entity_id,
    row.candidates[0].feedback_version, "ceo", "t");
  storage.set(newKey, "新候选草稿");
  oldRead.resolve(makeRow("old")); await oldSubmit;
  assert.equal(posts, 0); assert.equal(reloads, 0); assert.equal(storage.get(newKey), "新候选草稿");
  storage.delete(newKey);
  const unmountedSubmit = choose();
  storage.set(newKey, "保留未确认请求");
  h.unmount(); unmountedRead.resolve(row); await unmountedSubmit;
  assert.equal(posts, 0); assert.equal(reloads, 0); assert.equal(storage.get(newKey), "保留未确认请求");
});

test("actual workspace has four production choices and opens the chosen empty format without upgrading legacy", async () => {
  const api = { ...sourceAPI(), query: "cg_view=production" }, h = scene("workspace", api, runtime);
  const render = () => h.render(h.exports.default, { detail, workspaceId: "w" }); render(); await tick(); render();
  const choices = nodes(h.tree, (node) => node.type === "button" && node.props.className === "method"); assert.equal(choices.length, 4);
  choices[1].props.onClick(); render();
  const creator = nodes(h.tree, (node) => node.type.name === "ContentGrowthMain")[0]; assert.equal(creator.props.initialFormat, "long_video"); assert.equal(creator.props.row, null);
  assert.equal(nodes(h.tree, (node) => node.type === "button" && text(node) === "返回制作目录").length, 1); h.unmount();
  const old = cgState.CG_PACKAGE;
  assert.equal(cgState.isContentGrowthPackage({ instance: { package_id: old.id, package_version: old.version, package_digest: old.digest }, package: { package_id: old.id, version: old.version, digest: old.digest, schema_version: "curis.workspace-package/v1" }, schemas: { ContentGraphic: { schemaVersion: old.version } } }), true);
});

test("actual Main preserves separate cancelled four-format drafts and no sample body or confirmed media intent", () => {
  const storage = new Map(), props = { company: "A", workspaceId: "w", entry: {}, row: null, collection: collection(), busy: false, locked: false, onInspect() {}, perform: async () => { throw new Error("no write expected"); } };
  for (const format of Object.keys(cgState.CG_FORMATS)) {
    const h = scene("main", { storage }, runtime); h.render(h.exports.default, { ...props, initialFormat: format }); h.render(h.exports.default, { ...props, initialFormat: format });
    const editor = nodes(h.tree, (node) => node.type === "textarea" && node.props["aria-label"] === "内容正文与脚本")[0]; assert.equal(editor.props.value, ""); editor.props.onChange({ target: { value: `${format}保留原稿` } }); h.render(h.exports.default, { ...props, initialFormat: format }); h.unmount();
  }
  for (const format of Object.keys(cgState.CG_FORMATS)) {
    const h = scene("main", { storage }, runtime); h.render(h.exports.default, { ...props, initialFormat: format }); h.render(h.exports.default, { ...props, initialFormat: format });
    assert.equal(nodes(h.tree, (node) => node.type === "textarea" && node.props["aria-label"] === "内容正文与脚本")[0].props.value, `${format}保留原稿`); h.unmount();
  }
  for (const [key, raw] of storage) { if (key === "curis.cg.input.index") continue; const saved = JSON.parse(raw); assert.equal(saved.draft.work.output_intent, "UNCONFIRMED"); assert.equal(saved.draft.work.shots.length, 0); }
});

test("actual account utility accepts same-business other-workspace record and retains cancelled create draft", async () => {
  let panel; const api = sourceAPI(), h = scene("accounts", api, runtime), props = { company: "A", workspaceId: "w", onInspect: (value) => { panel = value; } };
  const render = () => h.render(h.exports.default, props); render(); await tick(); render();
  const view = nodes(h.tree, (node) => node.type === "button" && text(node) === "查看")[0]; view.props.onClick(); await tick(); render();
  assert.ok(panel); assert.match(text(panel.content), /one/); assert.doesNotMatch(text(h.tree), /账号范围已变化/);
  button(h.tree, "登记本地账号").props.onClick(); render();
  labelInput(panel.content, "账号名").props.onChange({ target: { value: "保留账号草稿" } }); render(); button(panel.content, "取消").props.onClick(); render();
  button(h.tree, "登记本地账号").props.onClick(); render(); assert.equal(labelInput(panel.content, "账号名").props.value, "保留账号草稿"); h.unmount();
});

test("actual per-account template ignores late old account result and retains current original template", async () => {
  const one = deferred(), two = deferred(); let panel;
  const api = { ...sourceAPI(), verificationTemplate: (_, __, platform) => platform === "xhs" ? one.promise : two.promise }, h = scene("verify", api, runtime), props = { company: "A", workspaceId: "w", onInspect: (value) => { panel = value; } };
  const render = () => h.render(h.exports.default, props); render(); await tick(); render(); button(h.tree, "新建核验").props.onClick(); render();
  let select = nodes(panel.content, (node) => node.type === "select")[1]; select.props.onChange({ target: { value: "one" } }); render(); select = nodes(panel.content, (node) => node.type === "select")[1]; select.props.onChange({ target: { value: "two" } }); render();
  two.resolve({ entry, platform: "douyin", checks: [{ key: "two", label: "当前抖音模板" }] }); await tick(); render();
  one.resolve({ entry, platform: "xhs", checks: [{ key: "one", label: "过期小红书模板" }] }); await tick(); render();
  assert.match(text(panel.content), /当前抖音模板/); assert.doesNotMatch(text(panel.content), /过期小红书模板/); h.unmount();
});

test("actual current workspace consumer emits selected Utility into real host, closes and explicitly reopens", async () => {
  const api = { ...sourceAPI(), query: "cg_view=accounts" }, parent = scene("workspace", api, runtime), parentProps = { detail, workspaceId: "w" };
  const host = scene("host", {}, runtime); api.hostComponent = host.exports.default;
  const paint = () => { parent.render(parent.exports.default, parentProps); host.render(host.exports.default, parent.tree.props); host.render(host.exports.default, parent.tree.props); };
  paint(); await tick(); paint();
  const child = nodes(parent.tree, (node) => node.type.name === "ContentGrowthAccounts")[0], consumer = scene("accounts", sourceAPI(), runtime);
  const renderChild = () => consumer.render(consumer.exports.default, child.props); renderChild(); await tick(); renderChild(); paint();
  assert.equal(nodes(host.tree, (node) => node.props.role === "tabpanel").length, 0);
  nodes(consumer.tree, (node) => node.type === "button" && text(node) === "查看")[0].props.onClick(); await tick(); renderChild(); paint();
  let panel = nodes(host.tree, (node) => node.props.role === "tabpanel")[0]; assert.equal(panel.props.hidden, false); assert.ok(text(panel).includes("one"));
  nodes(host.tree, (node) => node.props.label === "收起辅助内容")[0].props.onClick(); paint(); assert.equal(nodes(host.tree, (node) => node.type === "section" && node.props["aria-label"] === "辅助内容")[0].props.hidden, true);
  nodes(consumer.tree, (node) => node.type === "button" && text(node) === "查看")[0].props.onClick(); await tick(); renderChild(); paint();
  panel = nodes(host.tree, (node) => node.props.role === "tabpanel")[0]; assert.equal(panel.props.hidden, false); assert.equal(nodes(host.tree, (node) => node.type === "section" && node.props["aria-label"] === "辅助内容")[0].props.hidden, false);
  consumer.unmount(); parent.unmount(); host.unmount();
});

test("actual scope consumer drops unmounted collection and cannot reveal late foreign account data", async () => {
  const read = deferred(), h = scene("accounts", { accounts: () => read.promise }, runtime), props = { company: "A", workspaceId: "w", onInspect() {} };
  h.render(h.exports.default, props); h.unmount(); read.resolve({ entry, accounts: [account("FOREIGN OLD ROW")], catalog: [] }); await tick(); h.render(h.exports.default, props);
  assert.doesNotMatch(text(h.tree), /FOREIGN OLD ROW/);
});

test("actual manual observation retries the same normalized uncertain request, then uses a new identity after confirmed save", async () => {
  let panel; const calls = []; let first = true;
  const api = { ...sourceAPI(), observationCreate: async (_, __, id, data) => { calls.push({ id, data }); if (first) { first = false; throw new Error("结果待核验"); } return { entity_id: `saved-${calls.length}` }; } }, h = scene("observe", api, runtime), props = { company: "A", workspaceId: "w", onInspect: (value) => { panel = value; } };
  const render = () => h.render(h.exports.default, props); render(); await tick(); render();
  const fill = () => {
    nodes(panel.content, (node) => node.type === "select")[0].props.onChange({ target: { value: "one" } }); render();
    labelInput(panel.content, "观察标题").props.onChange({ target: { value: " 原观察 " } }); render();
    labelInput(panel.content, "观察周期").props.onChange({ target: { value: " 本周 " } }); render();
    nodes(panel.content, (node) => node.type === "textarea")[0].props.onChange({ target: { value: " 原人工事实 " } }); render();
  };
  button(h.tree, "新建观察").props.onClick(); render(); fill(); await button(panel.content, "保存观察记录").props.onClick(); render();
  await button(panel.content, "保存观察记录").props.onClick(); render();
  assert.equal(calls[0].id, calls[1].id); assert.equal(calls[1].data.title, "原观察");
  button(h.tree, "新建观察").props.onClick(); render(); assert.equal(labelInput(panel.content, "观察标题").props.value, ""); fill(); await button(panel.content, "保存观察记录").props.onClick(); render();
  assert.notEqual(calls[1].id, calls[2].id); h.unmount();
});

test("correction Main leads with editor, keeps real gap and puts qualification selector in Utility", () => {
  const data = { ...cgState.cgDraftOf(null, true), title: "真实标题", topic: "原主题", audience: "原受众", body: "原保存正文" };
  const version = { entity_id: "v", data }, row = { content: { entity_id: "c", company_id: "A", workspace_id: "w" }, version, versions: [version], candidates: [] };
  let panel; const props = { company: "A", workspaceId: "w", entry: {}, row, collection: collection(), busy: false, locked: false, onInspect: (value) => { panel = value; }, perform() {} }, h = scene("main", {}, runtime);
  const render = () => h.render(h.exports.default, props); render(); render();
  assert.match(text(h.tree), /当前责任不可用或尚未安排/);
  const verifyLink = nodes(h.tree, (node) => node.props.href && text(node) === "逐账号本地核验 →")[0];
  const verifyEntry = cgState.cgEntry(new URL(verifyLink.props.href, "http://fixture").searchParams); assert.equal(verifyEntry.object, "c"); assert.equal(verifyEntry.view, "verify"); assert.equal(verifyEntry.content, "");
  assert.equal(nodes(h.tree, (node) => node.type === "select" && node.props["aria-label"] === "内容责任员工").length, 0);
  assert.equal(nodes(h.tree, (node) => node.type === "p" && node.props.className === "metadataSummary").length, 0);
  assert.equal(nodes(h.tree, (node) => node.props.className === "conversation")[0].props.hidden, true);
  button(h.tree, "查看与配置").props.onClick(); render(); assert.ok(panel);
  assert.equal(nodes(panel.content, (node) => node.type === "select" && node.props["aria-label"] === "内容责任员工").length, 1);
  button(h.tree, "展开讨论").props.onClick(); render();
  const blocks = Array.from(h.tree.props.children); assert.ok(blocks.findIndex((node) => node?.props?.className === "conversation") < blocks.findIndex((node) => node?.props?.className === "scriptGrid"));
  assert.equal(nodes(h.tree, (node) => node.type === "textarea" && node.props["aria-label"] === "内容正文与脚本")[0].props.value, "原保存正文"); h.unmount();
});

test("correction source title uses exact scoped pinned metadata rather than generic action or new head", () => {
  const contents = [{ content: { entity_id: "c", tenant_id: "t", company_id: "A", workspace_id: "w", data: { format: "graphic" }, current_version_id: "new" }, version: { entity_id: "new", data: { title: "后来标题" } }, versions: [{ entity_id: "old", data: { title: "原版本标题", kind: "draft" } }, { entity_id: "new", data: { title: "后来标题" } }] }];
  const ref = { kind: "CONTENT_ITEM", reference_id: "c", title: "查看来源", version_ref: "old" };
  assert.equal(cgState.cgReferenceTitle(ref, contents, scope), "原版本标题");
  assert.equal(cgState.cgReferenceTitle({ ...ref, version_ref: "missing" }, contents, scope), "来源标题暂不可读取");
  assert.equal(cgState.cgReferenceTitle(ref, contents, { ...scope, company_id: "B" }), "来源标题暂不可读取");
});

test("correction Analysis embeds actual manual observation hierarchy with one H1", async () => {
  const h = scene("analysis", {}, runtime); h.render(h.exports.default, { company: "A", workspaceId: "w", onInspect() {} });
  assert.equal(nodes(h.tree, (node) => node.type === "h1").length, 1);
  const child = nodes(h.tree, (node) => node.type.name === "ContentGrowthObserve")[0]; assert.equal(child.props.embedded, true);
  const embedded = scene("observe", sourceAPI(), runtime); embedded.render(embedded.exports.default, child.props); await tick(); embedded.render(embedded.exports.default, child.props);
  assert.equal(nodes(embedded.tree, (node) => node.type === "h1").length, 0); assert.match(text(embedded.tree), /人工观察 · 未验证/);
  embedded.unmount(); h.unmount();
});

test("provenance candidate comparison stays on exact original basis before and after adopted or later head", () => {
  const version = (id, body, kind = "draft", extra = {}) => ({ entity_id: id, entity_type: "CONTENT_VERSION", parent_id: "c", tenant_id: "t", company_id: "A", workspace_id: "w", data: { ...cgState.cgDraftOf(null, true), title: "正文", topic: "主题", audience: "受众", body, kind, ...extra } });
  const original = version("original", "固定原文"), adopted = version("adopted", "采用后正文", "adopted"), later = version("later", "后来正文");
  const cand = version("candidate", "人工候选", "candidate", { basis_version_ref: "original", selection: { version_ref: "original", locator: "body", start: 0, end: 2, excerpt: "固定" } });
  let row = { content: { entity_id: "c", tenant_id: "t", company_id: "A", workspace_id: "w" }, version: original, versions: [original, cand, adopted, later], candidates: [{ version: cand, eligible: false, reasons: ["已采用"] }] };
  const h = scene("main", {}, runtime), props = { company: "A", workspaceId: "w", entry: { candidate: "candidate" }, collection: collection(), busy: false, locked: false, onInspect() {}, perform() {} }, render = () => h.render(h.exports.default, { ...props, row });
  const left = () => nodes(h.tree, (node) => node.type === "article" && text(node).startsWith("候选原保存版本"))[0];
  render(); render(); assert.equal(text(left()), "候选原保存版本固定原文");
  assert.match(text(h.tree), /采用后，候选将成为完整的新正文版本；原正文版本会保留，不会发布。/);
  row = { ...row, version: adopted }; render(); assert.equal(text(left()), "候选原保存版本固定原文");
  row = { ...row, version: later }; render(); assert.equal(text(left()), "候选原保存版本固定原文");
  for (const invalid of [[], [original, original], [{ ...original, company_id: "B" }], [{ ...original, tenant_id: "foreign" }], [{ ...original, workspace_id: "other" }], [{ ...original, parent_id: "other" }], [{ ...original, entity_type: "CONTENT_ITEM" }]]) {
    row = { ...row, versions: [...invalid, cand, adopted, later] }; render(); assert.equal(text(left()), "候选原保存版本候选原版本暂不可读取");
  }
  row = { ...row, versions: [original, cand, adopted, later], candidates: [{ version: { ...cand, data: { ...cand.data, basis_version_ref: "later" } }, eligible: false, reasons: ["原候选"] }] }; render(); assert.equal(text(left()), "候选原保存版本后来正文");
  assert.equal(adopted.data.body, "采用后正文"); assert.equal(original.data.body, "固定原文"); h.unmount();
});

test("provenance non-head empty learning version exposes fixed snapshots without replacing current body or reading latest learning", () => {
  const base = { entity_type: "CONTENT_VERSION", parent_id: "c", tenant_id: "t", company_id: "A", workspace_id: "w" };
  const head = { ...base, entity_id: "head", data: { title: "当前", topic: "主题", audience: "受众", body: "", references: [], kind: "draft" } };
  const historical = { ...base, entity_id: "learning-draft", data: { ...head.data, learning_ref: "exact-learning", learning_body: "引用时原经验", learning_applicability: "引用时适用范围", learning_counterexample: "引用时限制" } };
  const row = { content: { entity_id: "c", tenant_id: "t", company_id: "A", workspace_id: "w" }, version: head, versions: [head, historical], candidates: [] };
  let panel; const h = scene("main", {}, runtime), oldCollection = { ...collection(), entry: { ...entry, definition: { package_id: cgState.CG_PACKAGE.id, version: cgState.CG_PACKAGE.version, digest: cgState.CG_PACKAGE.digest } } };
  const props = { company: "A", workspaceId: "w", entry: {}, row, collection: oldCollection, busy: false, locked: false, onInspect: (value) => { panel = value; }, perform() {} }, render = () => h.render(h.exports.default, props);
  render(); render(); button(h.tree, "版本记录").props.onClick(); render();
  assert.ok(panel); assert.match(text(panel.content), /经验依据稿 · 未替换当前正文/); assert.match(text(panel.content), /引用时原经验/); assert.match(text(panel.content), /引用时适用范围/); assert.match(text(panel.content), /引用时限制/); assert.match(text(panel.content), /正文为空；该版本保存经验依据/);
  assert.equal(nodes(h.tree, (node) => node.type === "textarea" && node.props["aria-label"] === "内容正文与脚本")[0].props.value, ""); assert.equal(row.version.entity_id, "head"); assert.equal(historical.data.body, ""); h.unmount();
});


test("CG feedback readback rejects foreign scope, actor and candidate basis", () => {
  const expected = { tenant_id: "t", company_id: "A", workspace_id: "w", content_ref: "content", candidate_ref: "candidate", candidate_version: "a".repeat(64), basis_version_ref: "basis", actor: "ceo" };
  const pending = { request_id: "123e4567-e89b-42d3-a456-426614174000", action: "ACCEPT", reason: "认可" };
  const version = { entity_id: "candidate", tenant_id: "t", company_id: "A", workspace_id: "w", parent_id: "content", owner_ref: "ceo", data: { source_class: "MANUAL_CANDIDATE", manual_actor: "ceo", basis_version_ref: "basis" } };
  const feedback = { ...pending, tenant_id: "t", company_id: "A", workspace_id: "w", content_ref: "content", candidate_ref: "candidate", candidate_version: expected.candidate_version, basis_version_ref: "basis", ceo_id: "ceo" };
  const fresh = { content: { entity_id: "content", tenant_id: "t", company_id: "A", workspace_id: "w" }, candidates: [{ version, eligible: true, feedback_version: expected.candidate_version, feedback }] };
  assert.equal(cgState.cgFeedbackMatches(fresh, pending, expected), true);
  assert.equal(cgState.cgFeedbackMatches({ ...fresh, candidates: [{ ...fresh.candidates[0], feedback: { ...feedback, ceo_id: "other" } }] }, pending, expected), false);
  assert.equal(cgState.cgFeedbackMatches({ ...fresh, candidates: [{ ...fresh.candidates[0], version: { ...version, parent_id: "foreign" } }] }, pending, expected), false);
});


test("CG scoped feedback and content draft storage have finite size, count and lifetime", () => {
  const map = new Map(), storage = { getItem: (key) => map.get(key) || null, setItem: (key, value) => map.set(key, value) };
  for (let i = 0; i < 32; i++) cgState.saveCgFeedback(storage, `curis.cg.feedback.${i}`, { at: 1000, reason: "ok" });
  assert.throws(() => cgState.saveCgFeedback(storage, "curis.cg.feedback.overflow", {}), /数量/);
  const context = { company: "A", workspace: "w", content: "new", tenant: "t", actor: "ceo" };
  const snapshot = cgState.cgInputSnapshot(context, { draft: { title: "原输入" } });
  assert.ok(cgState.restoreCgInput(JSON.stringify(snapshot), context));
  assert.equal(cgState.restoreCgInput(JSON.stringify({ ...snapshot, at: 1000 }), context, 1000 + 31 * 60 * 1000), null);
  assert.throws(() => cgState.saveCgInput(storage, "curis.cg.input.1", { ...snapshot, draft: { title: "x".repeat(140000) } }), /上限/);
});


test("CG candidate reasons remain separate verbatim rows with original punctuation and order", () => {
 const data = { ...cgState.cgDraftOf(null, true), title: "正文", body: "原文", kind: "draft" }, original = { entity_id: "original", entity_type: "CONTENT_VERSION", parent_id: "c", ...scope, data };
 const candidate = { ...original, entity_id: "candidate", data: { ...data, kind: "candidate", basis_version_ref: "original" } };
 const reasons = ["已采用，请查看采用版本。", "正文已改变，请查看原版本并重新准备候选。", "保留原文；不要改写标点！"];
 const row = { content: { entity_id: "c", ...scope }, version: original, versions: [original, candidate], candidates: [{ version: candidate, eligible: false, reasons }] };
 const h = scene("main", {}, runtime), props = { company: "A", workspaceId: "w", entry: { candidate: "candidate" }, row, collection: collection(), busy: false, locked: false, onInspect() {}, perform() {} }, render = () => h.render(h.exports.default, props); render(); render();
 const list = nodes(h.tree, n => n.type === "ul" && nodes(n, child => child.type === "li").length === reasons.length)[0]; assert.ok(list); assert.deepEqual(nodes(list, n => n.type === "li").map(text), reasons); assert.doesNotMatch(text(list), /。；/); assert.deepEqual(row.candidates[0].reasons, reasons);
 row.candidates = [{ version: candidate, eligible: true, reasons: [] }]; render(); assert.match(text(h.tree), /正文和来源依据仍匹配；请逐项核对。/); assert.equal(nodes(h.tree, n => n.type === "ul").length, 0); h.unmount();
});

test("CG Chinese media chooser retains native focus target, configuration and edit locks", async () => {
 const h = scene("main", { mediaCollection: async () => ({ entry, configured: true, records: [] }) }), props = { company: "A", workspaceId: "w", row: { content: { entity_id: "c", data: { format: "graphic" } }, version: { entity_id: "v" } }, dirty: false, locked: false };
 const render = () => h.render(h.exports.LocalGrowthMedia, props), input = () => nodes(h.tree, n => n.type === "input" && n.props.type === "file")[0]; render(); assert.equal(input().props.disabled, true); await tick(); render();
 assert.equal(input().props.disabled, false); assert.match(text(h.tree), /尚未选择文件/); assert.equal(input().props["aria-label"], "导入本机内容媒体"); assert.equal(input().props.accept, "image/png,image/jpeg,audio/wav,video/mp4"); assert.equal(input().props.className, "fileInput"); assert.equal(input().props.hidden, undefined); assert.notEqual(input().props.tabIndex, -1); assert.equal(typeof input().props.onChange, "function"); assert.equal(input().props.onKeyDown, undefined);
 const label = nodes(h.tree, n => n.type === "label" && n.props.className === "filePicker")[0]; assert.equal(text(label), "选择本机文件"); assert.notEqual(label.props.className, "primary");
 props.dirty = true; render(); assert.equal(input().props.disabled, true); props.dirty = false; props.locked = true; render(); assert.equal(input().props.disabled, true); h.unmount();
});

// L1-RC1: exercise the production media consumer with deferred local bytes/API responses.
async function l1MediaFixture() {
 const bytes = new Uint8Array([137,80,78,71]);
 const hash = Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256", bytes)), v=>v.toString(16).padStart(2,"0")).join("");
 const asset={ref:"asset",kind:"Asset",payload:{title:"本机测试图",version_ref:"v",use:"OUTPUT",media:{mime:"image/png",size:bytes.length,sha256:hash}}};
 const candidate={ref:"media-candidate",kind:"Candidate",eligible:true,payload:{asset_ref:"asset",version_ref:"v"}};
 const calls=[];
 const api={mediaCollection:async()=>({entry,configured:true,records:[asset,candidate]}),media:async()=>new Blob([bytes],{type:"image/png"}),importMedia:async(...args)=>{calls.push(args);return {asset};},adoptMedia:async()=>({})};
 const props={company:"A",workspaceId:"w",row:{content:{entity_id:"c",data:{format:"graphic"}},version:{entity_id:"v"}},dirty:false,locked:false,initialAsset:"asset"};
 const h=scene("main",api),render=()=>h.render(h.exports.LocalGrowthMedia,props),flush=async()=>{render();await tick();render();await tick();render();};
 await flush();for(let i=0;i<30&&!nodes(h.tree,n=>n.type==="img").length;i++){await tick();render();}return {api,props,h,render,flush,calls,bytes};
}
test("L1 media invalid selection clears native input and cancellation makes no import",async()=>{
 const f=await l1MediaFixture(),input=()=>nodes(f.h.tree,n=>n.type==="input"&&n.props.type==="file")[0];
 const target={value:"invalid.mp3",files:[{name:"invalid.mp3",type:"audio/mpeg",size:8}]};
 await input().props.onChange({target});f.render();assert.equal(target.value,"");assert.match(text(f.h.tree),/请选择范围内/);
 await input().props.onChange({target:{value:"",files:[]}});assert.equal(f.calls.length,0);f.h.unmount();
});
test("L1 media new version clears old upload success and error notices",async()=>{
 const f=await l1MediaFixture();
 await nodes(f.h.tree,n=>n.type==="input"&&n.props.type==="file")[0].props.onChange({target:{value:"test.png",files:[{name:"test.png",type:"image/png",size:f.bytes.length,arrayBuffer:async()=>f.bytes.buffer}]}});
 f.render();assert.match(text(f.h.tree),/已保存本机原文件/);
 await nodes(f.h.tree,n=>n.type==="input"&&n.props.type==="file")[0].props.onChange({target:{value:"bad.mp3",files:[{name:"bad.mp3",type:"audio/mpeg",size:8}]}});
 f.render();assert.match(text(f.h.tree),/请选择范围内/);
 f.props.row={...f.props.row,version:{entity_id:"v2"}};await f.flush();
 assert.doesNotMatch(text(f.h.tree),/已保存本机原文件|请选择范围内/);f.h.unmount();
});
test("L1 media adoption settling after version change releases busy without stale success",async()=>{
 const f=await l1MediaFixture(),waiting=deferred();f.api.adoptMedia=()=>waiting.promise;
 nodes(f.h.tree,n=>n.type==="img")[0].props.onLoad({target:{naturalWidth:1}});f.render();
 nodes(f.h.tree,n=>n.type==="input"&&n.props.type==="checkbox")[0].props.onChange({target:{checked:true}});f.render();
 const done=button(f.h.tree,"明确采用本地媒体版本").props.onClick();f.render();assert.equal(nodes(f.h.tree,n=>n.props?.type==="file")[0].props.disabled,true);
 f.props.row={...f.props.row,version:{entity_id:"v2"}};await f.flush();waiting.resolve({});await done;f.render();
 assert.equal(nodes(f.h.tree,n=>n.props?.type==="file")[0].props.disabled,false);
 assert.doesNotMatch(text(f.h.tree),/已明确采用这份/);f.h.unmount();
});
test("L1 production basis copy does not deny supported local media and learning",()=>{
 const data={...cgState.cgDraftOf(null,true),title:"标题",body:"正文"},version={entity_id:"v",data};let panel;
 const props={company:"A",workspaceId:"w",entry:{},row:{content:{entity_id:"c",data:{format:"graphic"}},version,versions:[version],candidates:[]},collection:collection(),busy:false,locked:false,perform(){},onInspect:value=>{panel=value;}};
 const h=scene("main",{});h.render(h.exports.default,props);h.render(h.exports.default,props);
 button(h.tree,"制作依据").props.onClick();h.render(h.exports.default,props);
 assert.doesNotMatch(text(panel.content),/尚无真实媒体文件|经营报告、已接受学习的完整接续尚不支持/);
 assert.match(text(panel.content),/实际预览/);assert.match(text(panel.content),/未核验/);h.unmount();
});

const verificationContent = (ref='source',version='v1') => ({content:{...scope,entity_id:ref},version:{...scope,entity_id:version,data:{title:'来源正文',body:'保存正文'}},versions:[],candidates:[]});
async function verificationScene({sourceRef='source',rows=[verificationContent()],storage=new Map(),fail=false}={}){
 let panel;const writes=[],api={...sourceAPI(),storage,collection:async()=>({...collection(),contents:rows}),accounts:async()=>{if(fail)throw Error('读取失败');return{...accountsPayload(),accounts:[]}},verificationCreate:async(...args)=>{writes.push(args);throw Error('unexpected write')}};
 const h=scene('verify',api,runtime),props={company:'A',workspaceId:'w',sourceRef,onInspect:p=>{panel=p}};
 const render=()=>h.render(h.exports.default,props);render();await tick();render();await tick();render();
 return{h,api,props,render,writes,get panel(){return panel},open(){button(h.tree,'新建核验').props.onClick();render()},contentSelect(){return nodes(panel.content,n=>n.type==='select')[0]}};
}
test('UX CG source hint is visible but never selected before explicit action; zero accounts has a local route',async()=>{
 const f=await verificationScene();assert.match(text(f.h.tree),/来源正文/);f.open();assert.equal(f.contentSelect().props.value,'');button(f.panel.content,'使用这篇内容').props.onClick();f.render();assert.equal(f.contentSelect().props.value,'source');const link=nodes(f.panel.content,n=>text(n)==='先登记本地账号'&&n.props.href)[0];assert.equal(cgState.cgEntry(new URL(link.props.href,'http://fixture').searchParams).object,'source');assert.equal(f.writes.length,0);f.h.unmount();
});
for(const variant of ['missing','duplicate','foreign-company','foreign-workspace','foreign-tenant'])test('UX CG '+variant+' source cannot preselect or offer source-use action',async()=>{
 const rows=[verificationContent()];if(variant==='missing')rows[0].content.entity_id='other';if(variant==='duplicate')rows.push(verificationContent());if(variant==='foreign-company')rows[0].content.company_id='B';if(variant==='foreign-workspace')rows[0].version.workspace_id='other';if(variant==='foreign-tenant')rows[0].content.tenant_id='other';
 const f=await verificationScene({rows});f.open();assert.equal(f.contentSelect().props.value,'');assert.equal(button(f.panel.content,'使用这篇内容'),undefined);assert.match(text(f.panel.content),/无法唯一确认/);assert.equal(f.writes.length,0);f.h.unmount();
});
test('UX CG read failure is not treated as zero accounts',async()=>{const f=await verificationScene({fail:true});assert.match(text(f.h.tree),/读取失败/);assert.equal(nodes(f.h.tree,n=>n.props.href&&text(n)==='先登记本地账号').length,0);assert.equal(button(f.h.tree,'新建核验').props.disabled,true);f.h.unmount()});
test('UX CG local account round trip retains explicit same-version content and never creates verification',async()=>{
 const storage=new Map(),f=await verificationScene({storage});f.open();button(f.panel.content,'使用这篇内容').props.onClick();f.render();const link=nodes(f.panel.content,n=>n.props.href&&text(n)==='先登记本地账号')[0];let blocked=false;link.props.onClick({preventDefault(){blocked=true}});assert.equal(blocked,false);assert.equal(storage.size,1);f.h.unmount();
 const e=cgState.cgEntry(new URL(link.props.href,'http://fixture').searchParams),parentApi={...sourceAPI(),collection:async()=>({...collection(),contents:[verificationContent()]})},parent=scene('workspace',parentApi,runtime,new URL(link.props.href,'http://fixture').search);parent.render(parent.exports.default,{detail,workspaceId:'w'});await tick();parent.render(parent.exports.default,{detail,workspaceId:'w'});const child=nodes(parent.tree,n=>n.type.name==='ContentGrowthAccounts')[0];assert.equal(child.props.sourceRef,e.object);assert.equal(child.props.sourceContent.content.entity_id,'source');const accounts=scene('accounts',parentApi,runtime);accounts.render(accounts.exports.default,child.props);await tick();accounts.render(accounts.exports.default,child.props);const back=nodes(accounts.tree,n=>n.props.href&&text(n)==='返回发布核验')[0],backEntry=cgState.cgEntry(new URL(back.props.href,'http://fixture').searchParams);assert.equal(backEntry.view,'verify');assert.equal(backEntry.object,'source');
 const returned=await verificationScene({storage,sourceRef:backEntry.object});assert.equal(returned.contentSelect().props.value,'source');assert.match(text(returned.h.tree),/已保留你明确选择的内容/);assert.equal(returned.writes.length,0);returned.h.unmount();parent.unmount();accounts.unmount();
});
test('UX CG changed content version on return requires new explicit choice',async()=>{
 const storage=new Map(),f=await verificationScene({storage});f.open();button(f.panel.content,'使用这篇内容').props.onClick();f.render();nodes(f.panel.content,n=>n.props.href&&text(n)==='先登记本地账号')[0].props.onClick({preventDefault(){assert.fail('should retain choice')}});f.h.unmount();const returned=await verificationScene({storage,rows:[verificationContent('source','v2')]});assert.match(text(returned.h.tree),/版本已变化/);returned.open();assert.equal(returned.contentSelect().props.value,'');assert.equal(returned.writes.length,0);returned.h.unmount();
});
test('UX CG ordinary entry does not imply a source or select first content',async()=>{const f=await verificationScene({sourceRef:''});f.open();assert.equal(f.contentSelect().props.value,'');assert.equal(button(f.panel.content,'使用这篇内容'),undefined);f.h.unmount()});

for (const versionRef of [undefined, '', ' ']) test(`UX CG malformed return version ${JSON.stringify(versionRef)} cannot restore or offer source`, async () => {
 const row=verificationContent();row.version.entity_id=versionRef;
 const key=`curis.cg.verifyReturn:${JSON.stringify(['t','A','w','source'])}`;
 const storage=new Map([[key,JSON.stringify({tenant:'t',company:'A',workspace:'w',contentRef:'source',versionRef,explicit:true})]]);
 const returned=await verificationScene({storage,rows:[row]});
 assert.doesNotMatch(text(returned.h.tree),/已保留你明确选择的内容/);returned.open();
 assert.equal(returned.contentSelect().props.value,'');assert.equal(button(returned.panel.content,'使用这篇内容'),undefined);
 assert.equal(returned.writes.length,0);returned.h.unmount();
});
test('UX CG return storage removal failure preserves no restored choice and makes no write', async () => {
 const key=`curis.cg.verifyReturn:${JSON.stringify(['t','A','w','source'])}`;
 const storage=new Map([[key,JSON.stringify({tenant:'t',company:'A',workspace:'w',contentRef:'source',versionRef:'v1',explicit:true})]]);
 storage.delete=()=>{throw Error('storage removal unavailable')};
 const returned=await verificationScene({storage});assert.match(text(returned.h.tree),/未能恢复原选择/);
 assert.doesNotMatch(text(returned.h.tree),/已保留你明确选择的内容/);returned.open();assert.equal(returned.contentSelect().props.value,'');
 assert.equal(storage.size,1);assert.equal(returned.writes.length,0);returned.h.unmount();
});

async function savedReturnNoticeScene(outcome) {
 let panel,saved=false,unknownReject;const writes=[],key=`curis.cg.verifyReturn:${JSON.stringify(['t','A','w','source'])}`;
 const storage=new Map([[key,JSON.stringify({tenant:'t',company:'A',workspace:'w',contentRef:'source',versionRef:'v1',explicit:true})]]);
 const record=Object.freeze({entity_id:'verification-fixture',company_id:'A',data:Object.freeze({content_title:'合成核验内容',account_ref:'one',account_name:'one',platform_name:'合成平台',checks:Object.freeze([1,2,3,4].map(i=>Object.freeze({key:'check'+i,checked:false,note:''})))}),created_at:'2026-01-01T00:00:00Z'});
 const recordBefore=JSON.stringify(record),api={...sourceAPI(),storage,collection:async()=>({...collection(),contents:[verificationContent()]}),verifications:async()=>({entry,verifications:saved?[record]:[]}),verificationTemplate:async()=>({entry,platform:'xhs',checks:[1,2,3,4].map(i=>({key:'check'+i,label:'合成检查'+i}))}),verificationCreate:async(...args)=>{writes.push(args);if(outcome==='failure')throw Error('合成保存失败');if(outcome==='unknown')return new Promise((_resolve,reject)=>{unknownReject=reject});saved=true;return record;}};
 const h=scene('verify',api,runtime),props={company:'A',workspaceId:'w',sourceRef:'source',onInspect:value=>{panel=value}};const render=()=>h.render(h.exports.default,props);render();await tick();render();await tick();render();assert.match(text(h.tree),/尚未保存核验/);assert.equal(storage.size,0);
 await nodes(panel.content,n=>n.type==='select')[1].props.onChange({target:{value:'one'}});render();await tick();render();
 return{h,render,storage,writes,record,recordBefore,get panel(){return panel},get rejectUnknown(){return unknownReject},save(){return button(panel.content,'保存核验记录').props.onClick()}};
}
test('CG successful zero-of-four verification clears only stale return notice and preserves saved record',async()=>{
 const f=await savedReturnNoticeScene('success');assert.equal(nodes(f.panel.content,n=>n.type==='input'&&n.props.type==='checkbox').filter(n=>n.props.checked).length,0);await f.save();f.render();await tick();f.render();
 assert.doesNotMatch(text(f.h.tree),/尚未保存核验/);assert.match(text(f.h.tree),/核对通过 0\/4/);assert.equal(f.writes.length,1);assert.deepEqual(f.writes[0][3].checks.map(c=>c.checked),[false,false,false,false]);assert.equal(JSON.stringify(f.record),f.recordBefore);assert.equal(f.storage.size,0);f.h.unmount();
});
for(const outcome of ['failure','unknown'])test('CG '+outcome+' write keeps notice and explicit input without restoring or rewriting the consumed pointer',async()=>{
 const f=await savedReturnNoticeScene(outcome);nodes(f.panel.content,n=>n.type==='input'&&n.props.placeholder==='核对备注（可选）')[0].props.onChange({target:{value:'合成保留备注'}});f.render();const pending=f.save();f.render();
 if(outcome==='unknown'){assert.match(text(f.h.tree),/尚未保存核验/);assert.equal(nodes(f.panel.content,n=>n.type==='select')[0].props.value,'source');f.rejectUnknown(Error('合成结果未知'));}
 await pending;f.render();assert.match(text(f.h.tree),/尚未保存核验/);assert.equal(nodes(f.panel.content,n=>n.type==='select')[0].props.value,'source');assert.equal(nodes(f.panel.content,n=>n.type==='select')[1].props.value,'one');assert.equal(nodes(f.panel.content,n=>n.type==='input'&&n.props.placeholder==='核对备注（可选）')[0].props.value,'合成保留备注');assert.equal(f.writes.length,1);assert.equal(f.storage.size,0);assert.equal(JSON.stringify(f.record),f.recordBefore);f.h.unmount();
});

for (const scenario of ["authorized", "denied", "missing", "string-true", "locked", "stale-selection"]) {
  test(`CG selected composer uses exact model policy projection: ${scenario}`, async () => {
    const selectedKey = scenario === "denied" ? "other-model" : "current-model";
    const current = { model_key: "current-model", display_name: "当前模型", execution_authorized: true, execution_notice: "当前许可已核对" };
    if (scenario === "missing") delete current.execution_authorized;
    if (scenario === "string-true") current.execution_authorized = "true";
    const other = { model_key: "other-model", display_name: "其他模型", execution_authorized: false, execution_notice: "当前模型不在公司许可内；输入保留。" };
    const assignment = { ...scope, assignment_ref: "author", employee_ref: "runtime-author", company_employee_ref: "employee", name: "负责员工", scope_type: "WORKSPACE", scope_ref: "w", models: [current, other] };
    const data = { ...cgState.cgDraftOf(null, true), title: "保存正文", body: "原保存正文" };
    data.work = { ...data.work, assignment_ref: "author", recipient_ref: "employee", model_key: selectedKey };
    const version = { entity_id: "v", data }, old = { entity_id: "old", data: { ...data, body: "旧保存正文" } };
    const row = { content: { entity_id: "c", company_id: "A", workspace_id: "w" }, version, versions: [version, old], candidates: [] };
    const writes = [], bound = { binding_ref: "bound", context: { assignment_ref: "author" }, discussion_scope: { object_ref: "c" } };
    const api = { query: async () => ({ binding: bound, messages: [], attempt: { attempt_id: "attempt", status: "COMPLETED" } }) };
    const h = scene("main", api, runtime), props = { company: "A", workspaceId: "w", row,
      entry: { version: scenario === "stale-selection" ? "old" : "v", start: 0, end: 2 },
      collection: { ...collection(), entry: { ...entry, assignments: [assignment] }, execution_authorized: scenario !== "authorized" },
      busy: false, locked: scenario === "locked", onInspect() {}, reload: async () => {},
      perform: async (action, payload) => { writes.push({ action, payload }); return action === "bind" ? bound : action === "create-work" ? { work: { entity_id: "formal-work" } } : { attempt: { attempt_id: "attempt" } }; } };
    const render = () => h.render(h.exports.default, props);
    const composer = () => nodes(h.tree, node => node.props?.inputAriaLabel === "内容讨论输入")[0];
    render(); render(); render();
    nodes(composer().props.controls, n => n.props?.["aria-label"] === "内容交办范围")[0].props.onChange({ target: { value: "selection" } }); render();
    composer().props.onChange("请修改原选段，保留我的输入。"); render();
    assert.equal(Boolean(composer().props.disabled), scenario !== "authorized");
    if (scenario === "denied") assert.equal(composer().props.notice, other.execution_notice);
    await composer().props.onSubmit({ preventDefault() {} }); render();
    assert.equal(composer().props.value, "请修改原选段，保留我的输入。");
    if (scenario === "authorized") {
      assert.deepEqual(writes.map(value => value.action), ["bind", "create-work", "send"]);
      assert.equal(writes[2].payload.model_key, selectedKey);
      assert.equal(writes[2].payload.selection.version_ref, "v");
      assert.equal(writes[2].payload.selection.excerpt, "原保");
    } else assert.deepEqual(writes, [], "Calling submit directly must also respect the unchanged selection/pending and exact model guards");
    h.unmount();
  });
}

function savedBasisScene({ work = {}, changeEmployee, preference = "current-model", failSave = false, scopeMode = "selection", includeSelection = true, body = "原保存正文" } = {}) {
  const current = { model_key: "current-model", display_name: "当前模型", execution_authorized: true };
  const employee = { ...scope, assignment_ref: "author", employee_ref: "runtime-author", company_employee_ref: "employee", name: "负责员工", scope_type: "WORKSPACE", scope_ref: "w", models: [current, { model_key: "previous-model", execution_authorized: true }] };
  const assignments = changeEmployee ? changeEmployee(employee) : [employee];
  const data = { ...cgState.cgDraftOf(null, true), title: "保存正文", topic: "主题", audience: "读者", body };
  data.work = { ...data.work, ...work };
  const version = { entity_id: "basis-v1", data }, row = { content: { entity_id: "basis-content", company_id: "A", workspace_id: "w" }, version, versions: [version], candidates: [] };
  const writes = [], storage = new Map(), bound = { binding_ref: "bound", context: { assignment_ref: "author" }, discussion_scope: { object_ref: row.content.entity_id } };
  const api = { storage, query: async () => ({ binding: bound, messages: [], attempt: { attempt_id: "attempt", status: "COMPLETED" } }) };
  const h = scene("main", api, runtime), props = { company: "A", workspaceId: "w", row, entry: includeSelection ? { version: version.entity_id, start: 0, end: 2 } : {},
    collection: { ...collection(), entry: { ...entry, assignments, model_preference: { model_key: preference } } }, busy: false, locked: false, onInspect(value) { api.panel = value; }, reload: async () => {},
    perform: async (action, payload, options) => {
      writes.push({ action, payload: structuredClone(payload), options });
      if (action === "save" || action === "create") {
        if (failSave) throw Error("保存冲突，原输入保留");
        const next = { entity_id: "basis-v2", data: structuredClone(payload) };
        props.row = { ...row, version: next, versions: [...row.versions, next] }; return props.row;
      }
      return action === "bind" ? bound : action === "create-work" ? { work: { entity_id: "formal-work" } } : { attempt: { attempt_id: "attempt" } };
    } };
  const render = () => h.render(h.exports.default, props), composer = () => nodes(h.tree, n => n.props?.inputAriaLabel === "内容讨论输入")[0];
  render(); render(); render(); nodes(composer().props.controls, n => n.props?.["aria-label"] === "内容交办范围")[0].props.onChange({ target: { value: scopeMode } }); render(); composer().props.onChange("请修改原选段"); render();
  return { h, props, writes, storage, api, original: structuredClone(data), render, composer,
    save: () => button(h.tree, "保存正文").props.onClick(), send: () => composer().props.onSubmit({ preventDefault() {} }),
    select: () => { nodes(h.tree, n => n.props?.["aria-label"] === "内容正文与脚本")[0].props.onSelect({ target: { selectionStart: 0, selectionEnd: 2 } }); render(); } };
}

test("CG empty saved basis requires explicit Save, then a new selection before compiled send", async () => {
  const f = savedBasisScene();
  assert.equal(f.writes.length, 0); assert.equal(f.composer().props.disabled, true); assert.match(f.composer().props.notice, /保存正文后重新选择/);
  await f.send(); assert.equal(f.writes.length, 0);
  await f.save(); f.render();
  assert.deepEqual(f.writes[0].payload.work, { ...f.original.work, assignment_ref: "author", recipient_ref: "employee", model_key: "current-model" });
  assert.equal(f.writes[0].options.base, "basis-v1"); assert.equal(f.props.row.version.entity_id, "basis-v2");
  assert.equal(f.original.work.assignment_ref, "", "Save must not mutate the original version");
  assert.equal(f.composer().props.disabled, true, "Saving must not silently rebase the old selection");
  await f.send(); assert.deepEqual(f.writes.map(x => x.action), ["save"]);
  f.select(); assert.equal(f.composer().props.disabled, false); await f.send();
  assert.deepEqual(f.writes.map(x => x.action), ["save", "bind", "create-work", "send"]);
  assert.equal(f.writes[3].payload.selection.version_ref, "basis-v2"); assert.equal(f.writes[3].payload.selection.excerpt, "原保"); f.h.unmount();
});

test("CG saves the unique Agent responsibility without inventing a text model", async () => {
  const f = savedBasisScene({ preference: "", changeEmployee: e => [{ ...e, models: [] }] });
  const agent = () => nodes(f.h.tree, n => n.props?.embedded?.contextKey === "content:basis-content")[0];
  assert.equal(agent().props.embedded.agentSourceReady, false);
  assert.match(text(f.h.tree), /当前保存版本的责任与所选员工不一致/);
  await f.save(); f.render();
  assert.deepEqual(f.writes[0].payload.work, { ...f.original.work, assignment_ref: "author", recipient_ref: "employee", model_key: "" });
  assert.equal(f.original.work.assignment_ref, "", "The prior version remains unchanged");
  assert.equal(agent().props.embedded.agentSourceReady, false, "The old selection is not rebased");
  f.select(); assert.equal(agent().props.embedded.agentSourceReady, true);
  assert.equal(f.composer().props.disabled, true, "Ordinary model discussion still requires a model");
  f.h.unmount();
});

test("CG does not choose an Agent responsibility when several are available", async () => {
  const f = savedBasisScene({ preference: "", changeEmployee: e => [{ ...e, models: [] },
    { ...e, assignment_ref: "second", employee_ref: "other", company_employee_ref: "other", models: [] }] });
  await f.save(); f.render();
  assert.deepEqual(f.writes[0].payload.work, f.original.work);
  assert.equal(nodes(f.h.tree, n => n.props?.embedded?.contextKey === "content:basis-content").length, 0);
  f.h.unmount();
});

for (const [name, options] of [
  ["missing employee", { changeEmployee: () => [] }],
  ...["tenant_id", "company_id", "workspace_id", "scope_ref"].map(key => [`foreign ${key}`, { changeEmployee: e => [{ ...e, [key]: "foreign" }] }]),
  ["disabled employee", { changeEmployee: e => [{ ...e, enabled: false }] }],
  ["missing models", { changeEmployee: e => [{ ...e, models: [] }] }],
  ["stale model", { preference: "unavailable-model" }],
  ["unknown saved basis", { work: { assignment_ref: "old-author", recipient_ref: "old-employee", model_key: "unknown-model" } }],
  ["partial saved basis", { work: { assignment_ref: "author", recipient_ref: "employee" } }],
]) test(`CG explicit local save preserves basis without guessing: ${name}`, async () => {
  const f = savedBasisScene(options); assert.equal(Boolean(button(f.h.tree, "保存正文").props.disabled), false);
  await f.send(); assert.equal(f.writes.length, 0); await f.save(); f.render();
  assert.deepEqual(f.writes[0].payload.work, f.original.work); assert.equal(f.composer().props.disabled, true); f.h.unmount();
});

test("CG explicit save needs no execution grant, but still cannot send without it", async () => {
  const f = savedBasisScene({ changeEmployee: e => [{ ...e, models: e.models.map(m => ({ ...m, execution_authorized: false })) }] });
  await f.save(); f.render(); f.select(); assert.equal(f.writes[0].payload.work.model_key, "current-model");
  await f.send(); assert.deepEqual(f.writes.map(x => x.action), ["save"]); f.h.unmount();
});

test("CG existing valid saved basis wins over inherited preference; explicit new choice needs Save", async () => {
  const f = savedBasisScene({ work: { assignment_ref: "author", recipient_ref: "employee", model_key: "previous-model" } });
  await f.save(); f.render(); assert.deepEqual(f.writes[0].payload.work, f.original.work);
  const choose = nodes(f.composer().props.controls, n => n.props?.["aria-label"] === "内容建议模型")[0];
  choose.props.onChange({ target: { value: "current-model" } }); f.render(); await f.send(); assert.equal(f.writes.length, 1);
  await f.save(); f.render(); assert.equal(f.writes[1].payload.work.model_key, "current-model"); f.h.unmount();
});

test("CG explicit employee/model replacement repairs unknown basis only on Save", async () => {
  const f = savedBasisScene({ work: { assignment_ref: "old-author", recipient_ref: "old-employee", model_key: "old-model" } });
  button(f.h.tree, "查看与配置").props.onClick(); f.render();
  nodes(f.api.panel.content, n => n.props?.["aria-label"] === "内容责任员工")[0].props.onChange({ target: { value: "author" } }); f.render();
  nodes(f.composer().props.controls, n => n.props?.["aria-label"] === "内容建议模型")[0].props.onChange({ target: { value: "current-model" } }); f.render();
  assert.equal(f.writes.length, 0); await f.save(); f.render();
  assert.deepEqual(f.writes[0].payload.work, { ...f.original.work, assignment_ref: "author", recipient_ref: "employee", model_key: "current-model" }); f.h.unmount();
});

test("CG failed save keeps original empty basis and cannot enable old selection", async () => {
  const f = savedBasisScene({ failSave: true }); await f.save(); f.render();
  assert.equal(f.props.row.version.entity_id, "basis-v1"); assert.match(text(f.h.tree), /保存冲突/);
  await f.send(); assert.deepEqual(f.writes.map(x => x.action), ["save"]); f.h.unmount();
});

test("CG new local draft explicitly saves inherited basis and clears only its submitted input cache", async () => {
  const employee = { ...scope, assignment_ref: "author", employee_ref: "runtime-author", company_employee_ref: "employee", name: "负责员工", scope_type: "WORKSPACE", scope_ref: "w", models: [{ model_key: "current-model", execution_authorized: false }] };
  const storage = new Map(), writes = [], h = scene("main", { storage }, runtime);
  const props = { company: "A", workspaceId: "w", row: null, entry: {}, collection: { ...collection(), entry: { ...entry, assignments: [employee], model_preference: { model_key: "current-model" } } },
    busy: false, locked: false, onInspect() {}, reload: async () => {}, perform: async (action, payload) => {
      writes.push({ action, payload }); return { content: { entity_id: "new-content", company_id: "A", workspace_id: "w" }, version: { entity_id: "new-version", data: payload } };
    } };
  const render = () => h.render(h.exports.default, props); render(); render(); render();
  for (const label of nodes(h.tree, n => n.type === "label" && ["标题", "主题", "受众"].some(v => text(n).startsWith(v)))) {
    nodes(label, n => n.type === "input")[0].props.onChange({ target: { value: "明确填写" } });
  }
  render(); const cached = [...storage.keys()].filter(k => k !== "curis.cg.input.index"); assert.equal(cached.length, 1);
  assert.equal(button(h.tree, "创建本地草稿").props.disabled, false); await button(h.tree, "创建本地草稿").props.onClick();
  assert.equal(writes[0].action, "create"); assert.equal(writes[0].payload.work.assignment_ref, "author");
  assert.equal(writes[0].payload.work.recipient_ref, "employee"); assert.equal(writes[0].payload.work.model_key, "current-model");
  assert.equal(storage.has(cached[0]), false); h.unmount();
});

test('formal CG Work creation persists original identity across cold remount without auto send', async () => {
 const row={content:{entity_id:'cold-content',company_id:'A',workspace_id:'w'},version:{entity_id:'cold-v',data:{title:'正文'}},versions:[],candidates:[]};row.versions=[row.version];
 const storage=new Map(),calls=[],api={...sourceAPI(),storage,query:'cg_content=cold-content',content:async()=>row,createAssignedWork:async(assignment,value)=>{calls.push(structuredClone(value));if(calls.length===1)throw Error('creation unknown');return {work:{entity_id:'same-work'}};}};
 const payload={assignment_ref:'author',payload:{problem:'明确修改',expected_result:'文字结果',model_key:'model',source:{kind:'content-growth',content_ref:'cold-content'}}};
 const mount=async()=>{const h=scene('workspace',api,runtime),render=()=>h.render(h.exports.default,{detail,workspaceId:'w'});render();await tick();render();await tick();render();return {h,main:nodes(h.tree,n=>n.type.name==='ContentGrowthMain')[0]};};
 let current=await mount();assert.ok(current.main);assert.equal(calls.length,0);
 await assert.rejects(current.main.props.perform('create-work',payload),/creation unknown/);current.h.unmount();
 current=await mount();assert.equal(calls.length,1,'cold read does not replay');const result=await current.main.props.perform('create-work',payload);
 assert.equal(result.work.entity_id,'same-work');assert.deepEqual(calls[0],calls[1]);current.h.unmount();
});

test('CG whole saved version needs no text selection and pins the same full basis in Work and send', async () => {
 const body='第一行🌙\n第二行，保留全部。',f=savedBasisScene({work:{assignment_ref:'author',recipient_ref:'employee',model_key:'current-model'},scopeMode:'whole',includeSelection:false,body});
 assert.equal(f.writes.length,0);assert.equal(f.composer().props.submitLabel,'交办当前保存完整正文');assert.equal(f.composer().props.disabled,false);
 assert.equal(nodes(f.h.tree,n=>n.type==='summary'&&text(n).includes('针对已保存选段')).length,0);
 await f.send();assert.deepEqual(f.writes.map(x=>x.action),['bind','create-work','send']);
 const source=f.writes[1].payload.payload.source,request=f.writes[2].payload;
 assert.deepEqual(source.selection,request.selection);assert.equal(source.expected_version_ref,'basis-v1');
 assert.deepEqual(request.selection,{version_ref:'basis-v1',start:0,end:body.length,excerpt:body,locator:'body'});f.h.unmount();
});

test('CG selected mode without a range blocks instead of silently falling back to whole version', async () => {
 const f=savedBasisScene({work:{assignment_ref:'author',recipient_ref:'employee',model_key:'current-model'},scopeMode:'selection',includeSelection:false});
 assert.equal(f.composer().props.disabled,true);await f.send();assert.equal(f.writes.length,0);
 nodes(f.composer().props.controls,n=>n.props?.['aria-label']==='内容交办范围')[0].props.onChange({target:{value:'whole'}});f.render();
 assert.equal(f.composer().props.disabled,false);assert.equal(f.writes.length,0);f.h.unmount();
});

for (const problem of ['dirty','empty','denied','locked']) test(`CG whole saved version preserves ${problem} gate`,async()=>{
 const f=savedBasisScene({work:{assignment_ref:'author',recipient_ref:'employee',model_key:'current-model'},scopeMode:'whole',includeSelection:false,body:problem==='empty'?'   ':'保存正文',changeEmployee:problem==='denied'?e=>[{...e,models:e.models.map(m=>({...m,execution_authorized:false}))}]:undefined});
 if(problem==='dirty')nodes(f.h.tree,n=>n.props?.['aria-label']==='内容正文与脚本')[0].props.onChange({target:{value:'未保存正文'}});
 if(problem==='locked')f.props.locked=true;
 f.render();assert.equal(f.composer().props.disabled,true);await f.send();assert.equal(f.writes.length,0);f.h.unmount();
});


test("completed package work recovers its candidate without local storage or a duplicate send", async () => {
  const calls = [];
  const api = { query: async (...args) => {
    calls.push(["query", ...args]);
    return { attempt: { attempt_id: "original-attempt", status: "COMPLETED" } };
  } };
  const h = scene("workspace", api, runtime);
  const props = { company: "A", workspaceId: "w", busy: false, locked: false, collection: { ...collection(), pending_requests: [
      { content_ref: "content", binding_ref: "other-version-binding", attempt_id: "original-attempt" },
    ] },
    row: { content: { entity_id: "content" }, candidates: [],
      version: { entity_id: "draft", data: { title: "选题", work: { publication_brief: { platform: "小红书" } } } },
      publication_attempt: { binding_ref: "original-binding", attempt_id: "original-attempt", work_ref: "original-work", status: "COMPLETED" } },
    perform: async (action, payload) => { calls.push([action, payload.attempt_id]); },
  };
  h.render(h.exports.PublicationWork, props);
  assert.equal(button(h.tree, "交办生成内容包").props.disabled, true);
  await button(h.tree, "查询并回收原结果").props.onClick();
  assert.deepEqual(calls, [["query", "A", "w", "content", "original-binding", "original-attempt"], ["materialize", "original-attempt"]]);
});
