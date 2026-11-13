import assert from "node:assert/strict";
import test from "node:test";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import vm from "node:vm";

const require = createRequire(import.meta.url), React = require("react");
const swc = require("next/dist/build/swc");
await swc.loadBindings();
const sources = {
  knowledge: "app/ceo-office/knowledge/page.js",
  reader: "app/ceo-office/knowledge/entries/[id]/page.js",
  talent: "app/ceo-office/talent-market/page.js",
  insights: "app/ceo-office/analytics/OperatingIntelligence.js",
  shell: "components/terra/TerraShell.js",
  host: "components/workspace/WorkspacePaneShell.js",
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
    module: loaded, exports: loaded.exports, URLSearchParams, URL, console, location: { pathname: "/ceo-office/knowledge", search: "", assign: (value) => { api.returned = value; } }, scrollY: 0,
    sessionStorage: storageAPI,
    requestAnimationFrame: (fn) => fn(), scrollTo() {},
    window: { location: { search: query, origin: "http://127.0.0.1:3010" }, sessionStorage: storageAPI, localStorage: storageAPI, requestAnimationFrame: (fn) => fn(), addEventListener() {}, removeEventListener() {} },
    ResizeObserver: class { observe() {} disconnect() {} },
    document: { activeElement: { focus() {} } },
    require: (path) => {
      if (path === "react") return { ...React, ...hooks };
      if (path === "react/jsx-runtime") return require(path);
      if (path === "next/link") return { __esModule: true, default: primitive("a") };
      if (path === "next/navigation") return { useSearchParams: () => new URLSearchParams(query), useParams: () => ({ id: "doc" }), usePathname: () => "/ceo-office/knowledge" };
      if (path.includes("RuntimeProvider")) return { useRuntime: () => runtime };
      if (path.includes("WorkspacePaneShell") && api.hostComponent) return { __esModule: true, default: api.hostComponent };
      if (path.includes("TerraShell")) return { __esModule: true, default: primitive("main"), TerraPaneContent };
      if (path.includes("GlobalAssistant")) return { useAssistantPageContext() {} };
      if (path.includes("theme.js")) return { roleLabel: (value) => value };
      if (path.includes("EmployeeAvatar")) return { EmployeeAvatar: primitive("span"), EMPLOYEE_AVATAR_PRESETS: [] };
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
const pane = (tree) => nodes(tree, (node) => typeof node.type === "function" && node.type.name === "TerraPaneContent")[0];

test("actual Talent composition has no automatic detail; selects, changes type and filters current company", async () => {
  const api = { getTalentMarketData: async () => ({ experts: [{ id: "expert", name: "专家", recruitable: true }], skills: [], connectors: [], companies: [{ company_id: "a" }, { company_id: "b" }], departments: [], employees: [{ id: "ea", company_id: "a" }, { id: "eb", company_id: "b" }], companyEmployees: [{ id: "ea", company_id: "a", name: "A员工", market_kind: "company_employee" }, { id: "eb", company_id: "b", name: "B员工", market_kind: "company_employee" }], expertCategories: [] }), resolveTalentReturnPath: () => "", productStateFor: () => "可招聘", getEmployeeAbilitySummary: async () => ({ skills: [], capabilities: [] }) };
  const h = scene("talent", api), render = () => h.render(h.exports.TalentMarketSurface, { companyId: "a" }); render(); await tick(); render();
  assert.equal(pane(h.tree).props.utilityPane, null);
  const card = nodes(h.tree, (node) => node.type === h.exports.SearchResultCard)[0];
  card.props.onSelect({ kind: "experts", item: card.props.item }); render();
  assert.ok(pane(h.tree).props.utilityPane); assert.equal(pane(h.tree).props.utilityRequestKey, 1);
  const tabs = nodes(h.tree, (node) => node.type === "button" && text(node).startsWith("技能")); tabs[0].props.onClick(); render();
  assert.equal(pane(h.tree).props.utilityPane, null);
  nodes(h.tree, (node) => node.type === "button" && text(node).startsWith("专家"))[0].props.onClick(); render();
  nodes(h.tree, (node) => node.type === "button" && text(node).startsWith("公司员工"))[0].props.onClick(); render();
  const employeeCards = nodes(h.tree, (node) => node.type === h.exports.SearchResultCard);
  assert.deepEqual(employeeCards.map((node) => node.props.item.id), ["ea"]);
  h.unmount();
});

test("actual closed RecruitPanel retains cancelled name when reopened without recruitment", () => {
  const h = scene("talent", {}), props = { expert: { id: "expert", name: "专家", recruitable: true }, data: { companies: [{ company_id: "a" }], departments: [] }, onClose() {}, onSuccess() {} };
  h.render(h.exports.RecruitPanel, props);
  nodes(h.tree, (node) => node.type === "input" && node.props.required)[0].props.onChange({ target: { value: "我的分析师" } });
  assert.equal(h.render(h.exports.RecruitPanel, { ...props, open: false }), null);
  h.render(h.exports.RecruitPanel, props);
  assert.equal(nodes(h.tree, (node) => node.type === "input" && node.props.required)[0].props.value, "我的分析师");
  h.unmount();
});

const insightData = (company) => ({ company: { company_id: company }, scope: { ref: company, name: company }, scopes: [], time_range: { days: 30 }, metrics: [], benchmark: { metrics: [] }, reports: [], summary: { headline: "原事实", fact: "事实", analysis: "解读", recommendation: "建议" }, trust: { canonical_sources: [], manual_count: 0, external_outcome: { label: "待连接" } } });
test("actual Insights consumer rejects wrong scope and discards a late old-company read", async () => {
  const old = deferred(), current = deferred();
  const api = { getOperatingIntelligence: (company) => company === "a" ? old.promise : current.promise, runtimeErrorMessage: (error) => error.message };
  const a = scene("insights", api), b = scene("insights", api);
  a.render(a.exports.InsightsSurface, { companyId: "a" }); a.unmount();
  b.render(b.exports.InsightsSurface, { companyId: "b" });
  current.resolve(insightData("foreign")); old.resolve(insightData("a")); await tick();
  b.render(b.exports.InsightsSurface, { companyId: "b" });
  assert.match(text(b.tree), /范围已变化/); assert.doesNotMatch(text(b.tree), /原事实/);
  assert.equal(pane(b.tree).props.utilityPane, null); b.unmount();
});

test("actual Insights selection enters one Utility, scope change removes the old evidence immediately", async () => {
  const data = insightData("a"); data.metrics = [{ key: "provider_cost", label: "执行成本", value: null, unit: "CURRENCY", comparison: null, verification: "UNKNOWN", source: "AI Usage Ledger", source_refs: ["source"], sample_size: 0 }];
  const api = { getOperatingIntelligence: async () => data, runtimeErrorMessage: (error) => error.message };
  const h = scene("insights", api), render = () => h.render(h.exports.InsightsSurface, { companyId: "a" }); render(); await tick(); render();
  assert.equal(pane(h.tree).props.utilityPane, null);
  const overview = nodes(h.tree, (node) => node.type.name === "Overview")[0]; overview.props.onInspect(data.metrics[0]); render();
  assert.ok(pane(h.tree).props.utilityPane); assert.equal(pane(h.tree).props.utilityRequestKey, 1);
  button(h.tree, "7 天").props.onClick(); render();
  assert.equal(pane(h.tree).props.utilityPane, null); h.unmount();
});

test("actual Knowledge collection and original work picker return use real handlers", async () => {
  const api = { getKnowledgeEntries: async () => ({ entries: [], total: 0 }), getLocalKnowledgeRoots: async () => ({ roots: [] }), getCanonicalBusinesses: async () => ({ businesses: [] }), getWorkKnowledgeReferences: async () => ({ references: [], work: { problem: "原工作" } }), addWorkKnowledgeReferences: async (work, selected) => { assert.equal(work, "work"); assert.deepEqual([...selected], ["doc"]); }, runtimeErrorMessage: (error) => error.message };
  const h = scene("knowledge", api, undefined, "pick_for=work&return_to=%2Fceo-office%2Fworkspace%3Fworkspace_id%3Dw");
  const render = () => h.render(h.exports.KnowledgeSurface); render(); await tick(); render();
  const browse = nodes(h.tree, (node) => node.type.name === "Browse")[0]; assert.equal(browse.props.pickerContext.problem, "原工作");
  browse.props.onSelect(["doc"]); render();
  const head = nodes(h.tree, (node) => node.props.title === "为当前工作选择资料")[0]; await head.props.actions.props.onClick();
  assert.equal(api.returned, "/ceo-office/workspace?workspace_id=w"); h.unmount();
});

test("actual KnowledgeReader discards unmounted reads and rejects a foreign company before showing body", async () => {
  const response = deferred(); const api = { getKnowledgeEntry: () => response.promise, getKnowledgeUsedBy: async () => ({ works: [] }), getKnowledgeResults: async () => ({ results: [] }) };
  const h = scene("reader", api); h.render(h.exports.KnowledgeReader, { companyId: "a" });
  response.resolve({ company_id: "b", body: "FOREIGN BODY" }); await tick(); h.render(h.exports.KnowledgeReader, { companyId: "a" });
  assert.doesNotMatch(text(h.tree), /FOREIGN BODY/);
  assert.ok(nodes(h.tree, (node) => node.props.message?.includes("不属于当前公司")).length); h.unmount();
});

test("actual Knowledge manual drawer retains cancelled input without creating a record", async () => {
  let writes = 0;
  const api = { getKnowledgeEntries: async () => ({ entries: [], total: 0 }), getLocalKnowledgeRoots: async () => ({ roots: [] }), getCanonicalBusinesses: async () => ({ businesses: [] }), createKnowledgeEntry: async () => { writes += 1; }, runtimeErrorMessage: (error) => error.message };
  const h = scene("knowledge", api), render = () => h.render(h.exports.KnowledgeSurface);
  const open = () => nodes(h.tree, (node) => node.props.title === "资料库")[0].props.actions.props.children.at(-1).props.onClick();
  render(); await tick(); render(); open(); render();
  let drawer = nodes(h.tree, (node) => node.props.title === "新建资料")[0];
  drawer.props.children.props.setForm((form) => ({ ...form, title: "保留的标题", body: "保留的原文" })); render();
  drawer = nodes(h.tree, (node) => node.props.title === "新建资料")[0]; drawer.props.onClose(); render(); open(); render();
  drawer = nodes(h.tree, (node) => node.props.title === "新建资料")[0];
  assert.equal(drawer.props.children.props.form.title, "保留的标题"); assert.equal(drawer.props.children.props.form.body, "保留的原文"); assert.equal(writes, 0); h.unmount();
});

test("actual unmounted Talent consumer ignores a late catalogue response", async () => {
  const read = deferred(), h = scene("talent", { getTalentMarketData: () => read.promise, resolveTalentReturnPath: () => "" });
  h.render(h.exports.TalentMarketSurface, { companyId: "a" }); h.unmount();
  read.resolve({ experts: [{ id: "old", name: "OLD COMPANY" }] }); await tick();
  h.render(h.exports.TalentMarketSurface, { companyId: "a" });
  assert.equal(nodes(h.tree, (node) => node.type === h.exports.SearchResultCard).length, 0);
});

test("actual Reader shows original text once and labels independently authored summary", async () => {
  for (const [body, summary, independent] of [["原文  第一段", "原文 第一段", false], ["原文 第一段，后文", "原文 第一段", false], ["完整原文", "独立摘要", true]]) {
    const api = { getKnowledgeEntry: async () => ({ id: "doc", company_id: "a", source_status: "AVAILABLE", lifecycle_status: "ACTIVE", body, summary, title: "资料" }), getKnowledgeUsedBy: async () => ({ works: [] }), getKnowledgeResults: async () => ({ results: [] }) };
    const h = scene("reader", api); h.render(h.exports.KnowledgeReader, { companyId: "a" }); await tick(); h.render(h.exports.KnowledgeReader, { companyId: "a" });
    const bodyNode = nodes(h.tree, (node) => node.type === "div" && node.props.children === body);
    assert.equal(bodyNode.length, 1); assert.equal(nodes(h.tree, (node) => node.type === "h2" && text(node) === "摘要").length, independent ? 1 : 0);
    if (!independent) assert.equal(nodes(h.tree, (node) => node.type === "p" && node.props.children === summary).length, 0);
    h.unmount();
  }
});

test("real TerraShell adapter and WorkspacePaneShell select late content, close/reopen and reset current scope", () => {
  const runtime = { companyId: "a" }, storage = new Map();
  const host = scene("host", { storage }, runtime);
  const shell = scene("shell", { hostComponent: host.exports.default, storage }, runtime);
  const paint = () => {
    shell.render(shell.exports.default, { topCrumb: "资料库" });
    const child = shell.tree.props.children;
    assert.equal(child.type, host.exports.default);
    host.render(child.type, child.props); host.render(child.type, child.props);
  };
  paint();
  const adapter = scene("shell", { paneSetter: shell.tree.props.value }, runtime);
  const content = React.createElement("p", null, "A当前来源");
  const register = (key, value, target = "current") => {
    adapter.render(adapter.exports.TerraPaneContent, { utilityPane: value, utilityLabel: "资料来源", utilityRequestKey: key, utilityRequestTabId: target }); paint();
  };
  register(0, content);
  assert.equal(nodes(host.tree, (node) => node.props.role === "tabpanel").length, 0);
  register(1, content);
  let panel = nodes(host.tree, (node) => node.props.role === "tabpanel")[0];
  assert.equal(panel.props.hidden, false); assert.equal(text(panel), "A当前来源");
  assert.equal(nodes(host.tree, (node) => node.type === "section" && node.props["aria-label"] === "资料来源")[0].props.hidden, false);
  nodes(host.tree, (node) => node.props.label === "收起资料来源")[0].props.onClick(); paint();
  assert.equal(nodes(host.tree, (node) => node.type === "section" && node.props["aria-label"] === "资料来源")[0].props.hidden, true);
  register(2, content);
  button(host.tree, "×").props.onClick(); paint();
  assert.equal(nodes(host.tree, (node) => node.props.role === "tabpanel").length, 0);
  register(3, content);
  assert.equal(text(nodes(host.tree, (node) => node.props.role === "tabpanel")[0]), "A当前来源");
  runtime.companyId = "b"; register(0, null);
  assert.doesNotMatch(text(host.tree), /A当前来源/);
  register(1, React.createElement("p", null, "B当前来源"));
  panel = nodes(host.tree, (node) => node.props.role === "tabpanel")[0]; assert.equal(panel.props.hidden, false); assert.equal(text(panel), "B当前来源");
  adapter.unmount(); shell.unmount(); host.unmount();
});

test("all four production opening actions select their actual descriptor through the real adapter and host", async () => {
  const runtime = { status: "ready", companyId: "a", snapshot: { company: { name: "A" } } };
  const kApi = { getKnowledgeEntries: async () => ({ entries: [], total: 0 }), getLocalKnowledgeRoots: async () => ({ roots: [] }), getCanonicalBusinesses: async () => ({ businesses: [] }), runtimeErrorMessage: (error) => error.message };
  const library = scene("knowledge", kApi, runtime); library.render(library.exports.KnowledgeSurface); await tick(); library.render(library.exports.KnowledgeSurface);
  nodes(library.tree, (node) => node.props.title === "资料库")[0].props.actions.props.children[0].props.onClick(); library.render(library.exports.KnowledgeSurface);
  const reader = scene("reader", { getKnowledgeEntry: async () => ({ id: "doc", company_id: "a", source_label: "真实资料来源", source_status: "AVAILABLE", body: "正文", title: "资料" }), getKnowledgeUsedBy: async () => ({ works: [] }), getKnowledgeResults: async () => ({ results: [] }) }, runtime);
  reader.render(reader.exports.KnowledgeReader, { companyId: "a" }); await tick(); reader.render(reader.exports.KnowledgeReader, { companyId: "a" });
  nodes(reader.tree, (node) => node.props.title === "资料")[0].props.actions.props.children[0].props.onClick(); reader.render(reader.exports.KnowledgeReader, { companyId: "a" });
  const talent = scene("talent", { getTalentMarketData: async () => ({ experts: [{ id: "expert", name: "实际专家", recruitable: true }], skills: [], connectors: [], companies: [], departments: [], employees: [], companyEmployees: [], expertCategories: [] }), resolveTalentReturnPath: () => "" }, runtime);
  talent.render(talent.exports.TalentMarketSurface, { companyId: "a" }); await tick(); talent.render(talent.exports.TalentMarketSurface, { companyId: "a" });
  const card = nodes(talent.tree, (node) => node.type === talent.exports.SearchResultCard)[0]; card.props.onSelect({ kind: "experts", item: card.props.item }); talent.render(talent.exports.TalentMarketSurface, { companyId: "a" });
  const data = insightData("a"); data.metrics = [{ key: "provider_cost", label: "执行成本", value: null, comparison: null, unit: "CURRENCY", source: "AI Usage Ledger", verification: "UNKNOWN", sample_size: 0, source_refs: [] }];
  const insights = scene("insights", { getOperatingIntelligence: async () => data, runtimeErrorMessage: (error) => error.message }, runtime);
  insights.render(insights.exports.InsightsSurface, { companyId: "a" }); await tick(); insights.render(insights.exports.InsightsSurface, { companyId: "a" }); nodes(insights.tree, (node) => node.type.name === "Overview")[0].props.onInspect(data.metrics[0]); insights.render(insights.exports.InsightsSurface, { companyId: "a" });
  for (const consumer of [library, reader, talent, insights]) {
    const actualProps = pane(consumer.tree).props;
    assert.equal(actualProps.utilityRequestTabId, "current"); assert.ok(actualProps.utilityRequestKey > 0);
    const host = scene("host", {}, runtime), shell = scene("shell", { hostComponent: host.exports.default }, runtime);
    const paint = () => { shell.render(shell.exports.default); const child = shell.tree.props.children; host.render(child.type, child.props); host.render(child.type, child.props); };
    paint(); assert.equal(nodes(host.tree, (node) => node.props.role === "tabpanel").length, 0);
    const adapter = scene("shell", { paneSetter: shell.tree.props.value }, runtime);
    adapter.render(adapter.exports.TerraPaneContent, actualProps); paint();
    const panel = nodes(host.tree, (node) => node.props.role === "tabpanel")[0];
    assert.equal(panel.props.hidden, false); assert.equal(panel.props.children, actualProps.utilityPane);
    assert.equal(nodes(host.tree, (node) => node.type === "section" && node.props["aria-label"] === actualProps.utilityLabel)[0].props.hidden, false);
    adapter.unmount(); paint(); assert.equal(nodes(host.tree, (node) => node.props.role === "tabpanel").length, 0);
    shell.unmount(); host.unmount(); consumer.unmount();
  }
});
