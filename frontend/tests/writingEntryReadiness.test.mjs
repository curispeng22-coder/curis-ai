import test from "node:test";
import assert from "node:assert/strict";
import { confirmationSnapshot, writingRequestLocked, writingRepairHref, writingReturnTarget, validateWritingReturn, createWritingApi } from "../lib/writingApi.js";
import { chapterHref, writingEntry } from "../lib/writingState.mjs";

test("confirmation retains the original scalar proposal when editable values change", () => {
  const values = { business_name: "原确认", goal: "原目标", department_id: "d", proposal_sha256: "h" };
  const snapshot = confirmationSnapshot(values); values.goal = "另一个目标";
  assert.equal(snapshot.goal, "原目标"); assert.throws(() => { snapshot.goal = "改写"; });
  assert.throws(() => confirmationSnapshot({ nested: {} }));
});
test("pending and unknown require original-result query before replacement", () => {
  for (const status of ["RUNNING", "UNKNOWN", "UNVERIFIED"]) assert.equal(writingRequestLocked(status), true);
  for (const status of ["FAILED", "COMPLETED", ""]) assert.equal(writingRequestLocked(status), false);
});
test("model and responsibility repairs retain exact installed chapter return context", () => {
  const entry = { mode: "chapter", book: "book/1", chapter: "chapter/2", draft: "draft", anchor: "draft:0:4" };
  const href = chapterHref("workspace", entry);
  const repaired = new URL(writingRepairHref("/ceo-office/capabilities", href), "http://localhost");
  assert.equal(repaired.searchParams.get("return_to"), href);
  assert.deepEqual(writingEntry(new URL(href, "http://localhost").searchParams), { ...entry, view: "", formal: "", package: "" });
  assert.throws(() => writingRepairHref("https://other.invalid", href));
});
test("strict configuration facade retains server scope, model and assignment revision", async () => {
  const calls = []; const api = createWritingApi(async (...args) => { calls.push(args); });
  await api.assign("co/1", "w/1", { employee_id: "employee", expected_revision: 2 });
  await api.selectModel("co/1", "w/1", "model.selected");
  assert.equal(calls[0][0], "/api/workspace/v1/companies/co%2F1/writing/w%2F1/responsibility");
  assert.deepEqual(JSON.parse(calls[0][1].body), { employee_id: "employee", expected_revision: 2 });
  assert.deepEqual(JSON.parse(calls[1][1].body), { model_key: "model.selected" });
});

test("repair return rejects external, traversal, duplicate and invented scope URLs", () => {
  for (const value of ["https://evil.invalid/ceo-office/workspace/installed/w", "//evil.invalid/w", "javascript:alert(1)",
    "/ceo-office/workspace/installed/../w", "/ceo-office/workspace/installed/%2e%2e", "/ceo-office/workspace/installed/%252e%252e",
    "/ceo-office/workspace/installed/w\\x", "/ceo-office/workspace/installed/w?company_id=foreign",
    "/ceo-office/workspace/installed/w?writing_mode=chapter&book_ref=b&chapter_ref=c&book_ref=other",
    "/ceo-office/workspace/installed/w?writing_mode=chapter&book_ref=b", "/ceo-office/workspace/installed/w?book_ref=b",
    "/ceo-office/workspace/installed/w?writing_mode=chapter&book_ref=%252e%252e&chapter_ref=c",
    "/ceo-office/workspace/installed/w?writing_mode=unknown", "/ceo-office/workspace/installed/w#invented"]) {
    assert.throws(() => writingReturnTarget(value), value);
  }
  assert.throws(() => writingRepairHref("/ceo-office/settings", "/ceo-office/workspace/installed/w"));
});

test("return uses authorized real collection and exact chapter scope; workspace label stays truthful", async () => {
  const { WRITING_PACKAGE } = await import("../lib/writingState.mjs");
  const scope = { tenant_id: "selfuse", company_id: "co", workspace_id: "w", instance_id: "i", package_id: WRITING_PACKAGE.id,
    package_version: WRITING_PACKAGE.version, package_digest: WRITING_PACKAGE.digest };
  const entry = { mode: "chapter", book: "b", chapter: "c", anchor: "draft:0:4", draft: "draft" };
  const collection = { scope, books: [{ ref: "b" }], chapters: [{ ref: "c", bookRef: "b" }] };
  const state = { scope: { ...scope, book_ref: "b", chapter_ref: "c" } };
  const calls = [];
  const request = async (path) => { calls.push(path); return path.includes("/chapters/") ? state : collection; };
  assert.equal((await validateWritingReturn(chapterHref("w", entry), "co", request)).label, "返回当前写作章节");
  assert.equal(calls.length, 2);
  assert.equal((await validateWritingReturn("/ceo-office/workspace/installed/w", "co", request)).label, "返回写作工作台");
  for (const invalid of [
    { ...collection, scope: { ...scope, company_id: "foreign" } },
    { ...collection, scope: { ...scope, workspace_id: "foreign" } },
    { ...collection, scope: { ...scope, package_digest: "foreign" } },
    { ...collection, chapters: [{ ref: "c", bookRef: "foreign" }] },
    { ...collection, books: [] },
  ]) await assert.rejects(validateWritingReturn(chapterHref("w", entry), "co", async () => invalid));
  await assert.rejects(validateWritingReturn(chapterHref("w", entry), "co", async (path) => path.includes("/chapters/") ? { scope: { ...state.scope, chapter_ref: "foreign" } } : collection));
  await assert.rejects(validateWritingReturn(chapterHref("w", entry), "co", async () => { throw new Error("403 fixture"); }));
  await assert.rejects(validateWritingReturn(chapterHref("w", entry), "", request));
});

test("actual CreateBusiness consumer previews saved contract and reads current holder rather than receipt", async () => {
  const { readFileSync } = await import("node:fs"), { createRequire } = await import("node:module"), vm = await import("node:vm");
  const require = createRequire(import.meta.url), React = require("react"), swc = require("next/dist/build/swc"); await swc.loadBindings();
  const { buildOrganizationProjection } = await import("../lib/organizationProjection.js");
  const states = [], refs = [], effects = []; let si = 0, ri = 0, ei = 0, calls = [];
  const definition = { package_id: "com.curis.local.writing-authoring", name: "本地写作工作空间", initial_team_contract: { displayName: "章节作者", responsibility: "创作、自检、交付、复盘" } };
  const proposal = { intent: "写书", package_id: definition.package_id, proposal_sha256: "original-proposal", business_name: "写作业务", goal: "写书", workspace_name: "写作空间", department_id: "D", snapshot: { definition } };
  const founding = { entity_id: "run", data: { v1Proposal: proposal } };
  const employee = { id: "current-holder", company_id: "A", name: "当前名字", enabled: 1 };
  const payload = { company: { company_id: "A" }, employees: [employee], businesses: [{ company_id: "A", business_id: "B", team: [{ entity_id: "author", data: { companyEmployeeRef: employee.id, roleRef: "role", roleName: "章节作者" } }] }] };
  const api = { getBusinessDefinitions: async () => ({ available: true, definitions: [definition], departments: [{ id: "D", name: "合法部门" }] }), saveBusinessDraft: async () => founding,
    createBusinessFromFoundingRun: async (company, run, value) => { calls.push(value); return { founding_run: founding, activation: { status: "COMPLETED" }, creation_result: { business_id: "B", workspace_id: "W", initial_team: { employeeRef: "original-holder", contractVersion: "1" } } }; } };
  const source = readFileSync(new URL("../components/v1/CeoDeskOperating.js", import.meta.url), "utf8");
  const { code } = await swc.transform(source, { filename: "CeoDeskOperating.js", isModule: true, jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } }, module: { type: "commonjs" } });
  const loaded = { exports: {} };
  vm.runInNewContext(code, { module: loaded, exports: loaded.exports, URLSearchParams, crypto: { randomUUID: () => "request" }, crypto: { randomUUID: () => "isolated-intent" }, sessionStorage: { getItem: () => null, setItem: () => {} }, window: { location: { search: "", pathname: "/ceo-office/business" }, history: { replaceState: (_state, _title, href) => { search = href.split("?")[1] || ""; } } }, require: (name) => {
    if (name === "react") return { ...React, useState: (initial) => { const n = si++; if (!(n in states)) states[n] = initial; return [states[n], (value) => { states[n] = typeof value === "function" ? value(states[n]) : value; }]; }, useRef: (initial) => refs[ri++] ||= { current: initial }, useEffect: (effect, deps) => { const i = ei++, old = effects[i]; if (!old || deps.some((v, n) => !Object.is(v, old.deps[n]))) effects[i] = { effect, deps, pending: true, cleanup: old?.cleanup }; } };
    if (name === "react/jsx-runtime") return require(name);
    if (name.endsWith("v1FrontendApi.js")) return api;
    if (name.endsWith("runtimeApi.js")) return { createFoundingRun: async () => founding, transitionRuntimeEntity: async () => ({ entity_id: founding.entity_id, lifecycle_status: "CEO_CONFIRMED" }), getOrganizationProjection: async () => payload, workspaceOfficeHref: () => "/workspaces/W" };
    if (name.endsWith("api.js")) return { CEO_ID: "CEO" };
    if (name.endsWith("writingApi.js")) return { confirmationSnapshot, writingRequestLocked, createWritingApi: () => ({ entry: async () => ({ scope: { company_id: "A", workspace_id: "W" }, execution: { status: "UNAVAILABLE" } }) }) };
    if (name.endsWith("organizationProjection.js")) return { buildOrganizationProjection };
    if (name.endsWith("BusinessCatalogSurface.js")) return { businessCatalogHref: () => "/ceo-office/business?company_id=A&business_id=B", BUSINESS_DIRECTIONS: [{ id: "writing", packageId: definition.package_id, name: "写作" }] };
    if (name.endsWith("musicState.mjs")) return { MUSIC_PACKAGE: { id: "music", version: "0.2.0" } };
    return { __esModule: true, default: (props) => React.createElement("div", props) };
  } });
  const render = (company = "A") => { si = 0; ri = 0; ei = 0; const node = loaded.exports.CreateBusiness({ company: { company_id: company } }); return node.type === loaded.exports.LocalBusinessProposal ? loaded.exports.LocalBusinessProposal(node.props) : node; };
  const flushEffects = () => { for (const e of effects) if (e.pending) { e.cleanup?.(); e.pending = false; e.cleanup = e.effect(); } };
  const find = (node, match) => !node ? null : Array.isArray(node) ? node.map((v) => find(v, match)).find(Boolean) : match(node) ? node : find(node.props?.children, match);
  let tree = render(); flushEffects(); await Promise.resolve();
  tree = render(); find(tree, (n) => n.props?.["aria-label"] === "业务工作空间类型").props.onChange({ target: { value: definition.package_id } });
  tree = render(); find(tree, (n) => n.props?.["aria-label"] === "业务所属部门").props.onChange({ target: { value: "D" } });
  find(tree, (n) => n.props?.["aria-label"] === "业务目标").props.onChange({ target: { value: "写书" } }); tree = render(); await find(tree, (n) => n.type === "form").props.onSubmit({ preventDefault() {} });
  tree = render(); assert.ok(JSON.stringify(tree).includes("章节作者"));
  find(tree, (n) => n.props?.type === "checkbox").props.onChange({ target: { checked: true } });
  tree = render(); await find(tree, (n) => n.props?.children === "确认创建业务").props.onClick();
  tree = render(); flushEffects(); await new Promise((resolve) => setTimeout(resolve, 0));
  tree = render(); const text = JSON.stringify(tree);
  assert.ok(text.includes("当前名字")); assert.ok(text.includes("初始团队创建记录已保留")); assert.equal(text.includes("original-holder"), false); assert.ok(text.includes("员工执行当前不可用"));
  assert.ok(find(tree, (n) => n.props?.href?.includes("current-holder?company_id=A&business_id=B#employee-conversation")));
  assert.equal(calls.length, 1); assert.equal(calls[0].proposal_sha256, "original-proposal");
  const other = render("other"); assert.equal(JSON.stringify(other).includes("当前名字"), false);
});

// Compose the real page and real Creator, including dependency effects and unmount cleanup.
async function completedBusinessComposition(initialStatus = "COMPLETED", normalRecordEntry = false, resultCompany = null, routeDTO = null, proposalMode = null) {
  const { readFileSync } = await import("node:fs"), { createRequire } = await import("node:module"), vm = await import("node:vm");
  const require = createRequire(import.meta.url), React = require("react"), swc = require("next/dist/build/swc"); await swc.loadBindings();
  const { buildOrganizationProjection } = await import("../lib/organizationProjection.js");
  let context, child = null, childKey = null, mounts = 0, listReads = 0, resultReads = 0, confirms = 0;
  const requests = [], parent = { states: [], refs: [], effects: [] };
  let company = routeDTO?.founding_get.company_id || "A", search = normalRecordEntry ? `business_id=${routeDTO?.founding_get.first_business.business_id || "business-A"}` : "new=1";
  const hooks = { ...React, useState: (initial) => { const c = context, index = c.si++; if (!(index in c.states)) c.states[index] = initial; return [c.states[index], (value) => { c.states[index] = typeof value === "function" ? value(c.states[index]) : value; }]; },
    useRef: (initial) => context.refs[context.ri++] ||= { current: initial }, useMemo: (fn) => fn(), useCallback: (fn) => fn,
    useEffect: (fn, deps) => { const c = context, i = c.ei++, old = c.effects[i]; if (!old || !deps || deps.some((v, n) => !Object.is(v, old.deps[n]))) c.effects[i] = { fn, deps, pending: true, cleanup: old?.cleanup }; } };
  const proposal = (proposalMode ? routeDTO?.pending_draft.proposal : routeDTO?.draft_get.proposal) || { intent: "原写作目标", package_id: "com.curis.local.writing-authoring", proposal_sha256: "original", snapshot: { company_id: company }, business_name: "原业务", goal: "原目标", workspace_name: "原空间", department_id: "D" };
  const run = () => routeDTO?.business_result.founding_run || ({ entity_id: `run-${company}`, company_id: company, owner_ref: "CEO", lifecycle_status: "COMPANY_CREATED", data: { v1Proposal: proposal, ...(normalRecordEntry ? { firstBusiness: { business_id: `business-${company}`, workspace_id: `workspace-${company}`, department_id: "D" } } : {}) } });
  const business = () => routeDTO?.organization.businesses[0] || ({ company_id: company, business_id: `business-${company}`, name: "原业务", workspaces: [{ workspace_id: `workspace-${company}` }], creation_record: normalRecordEntry ? { company_id: company, business_id: `business-${company}`, workspace_id: `workspace-${company}`, founding_run_id: `run-${company}` } : null });
  const organization = () => (proposalMode === "directoryPending" ? routeDTO.pending_organization : routeDTO?.organization) || ({ company: { company_id: company }, departments: [], employees: [], businesses: [{ ...business(), team: [] }], departmentAssignments: [] });
  if (proposalMode === "directoryPending") search = "";
  else if (proposalMode && proposalMode !== "new") search = `new=1&founding_run_id=${routeDTO.pending_get.entity_id}${proposalMode === "duplicate" ? "&founding_run_id=other" : ""}`;
  let newRuns = 0, saves = 0;
  const runtimeApi = { getOrganizationProjection: async () => organization(), getCanonicalBusinesses: () => { listReads++; return new Promise((resolve) => requests.push(() => resolve({ businesses: [business()] }))); }, getFoundingRun: async () => proposalMode ? { ...routeDTO.pending_get, ...(proposalMode === "foreign" ? { owner_ref: "foreign" } : proposalMode === "unknown" ? { lifecycle_status: "UNRECOGNIZED" } : {}) } : routeDTO?.founding_get || { entity_id: run().entity_id, company_id: company, owner_ref: "CEO", lifecycle_status: run().lifecycle_status, first_business: run().data.firstBusiness }, workspaceOfficeHref: () => "/existing-workspace", createFoundingRun: async () => { newRuns++; if (proposalMode === "new") return routeDTO.new_run; throw new Error("must not create another Run"); }, transitionRuntimeEntity: async (_id, values) => routeDTO[values.target === "CEO_CONFIRMED" ? "confirmed_transition" : "transition_" + values.target] };
  const v1 = { getBusinessDefinitions: async () => proposalMode ? routeDTO.definitions : ({ definitions: [], departments: [] }), saveBusinessDraft: async () => { saves++; return routeDTO.saved_pending; }, getBusinessDraft: async () => (proposalMode ? routeDTO.pending_draft : routeDTO?.draft_get) || ({ founding_run_id: run().entity_id, lifecycle_status: run().lifecycle_status, proposal }), getBusinessCreationResult: async () => {
    resultReads++; if (routeDTO) return routeDTO.business_result; const status = resultReads === 1 ? initialStatus : "COMPLETED";
    return { founding_run: run(), activation: { status }, ...(status === "COMPLETED" ? { creation_result: { company_id: resultCompany || company, business_id: `business-${company}`, workspace_id: `workspace-${company}` } } : {}) };
  }, createBusinessFromFoundingRun: async (_company, id, values) => { confirms++; if (proposalMode && ["new", "pending", "directoryPending"].includes(proposalMode)) { assert.equal(id, routeDTO.pending_get.entity_id); assert.equal(values.proposal_sha256, routeDTO.saved_pending.data.v1Proposal.proposal_sha256); return routeDTO.new_created; } throw new Error("must not confirm again"); } };
  const catalog = { businessCatalogHref: (id, selection = {}) => `/ceo-office/business?${new URLSearchParams({ company_id: id, ...(selection.create ? { new: "1" } : selection.businessId ? { business_id: selection.businessId } : {}) })}`, businessCatalogSelection: () => search.includes("business_id=") ? ({ kind: "business", business: business() }) : ({ kind: "create" }) };
  const inert = { __esModule: true, default: (props) => React.createElement("div", props) };
  let CreateBusiness, LocalBusinessProposal, Catalog;
  async function load(path, isParent) {
    let source = readFileSync(isParent && process.env.CURIS_TEST_BEFORE_PAGE ? process.env.CURIS_TEST_BEFORE_PAGE : new URL("../" + path, import.meta.url), "utf8");
    if (path.endsWith("BusinessCatalogSurface.js") && process.env.CURIS_TEST_BEFORE_CATALOG) source = readFileSync(process.env.CURIS_TEST_BEFORE_CATALOG, "utf8");
    if (isParent) source = source.replace("function BusinessSurface()", "export function BusinessSurface()"); // test export only
    const { code } = await swc.transform(source, { filename: path, isModule: true, jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } }, module: { type: "commonjs" } });
    const loaded = { exports: {} };
    vm.runInNewContext(code, { module: loaded, exports: loaded.exports, URLSearchParams, crypto: { randomUUID: () => "isolated-intent" }, sessionStorage: { getItem: () => null, setItem: () => {} }, window: { location: { get search() { return normalRecordEntry || proposalMode ? "?" + search : "?new=1&founding_run_id=" + run().entity_id; }, pathname: "/ceo-office/business" }, history: { replaceState: (_state, _title, href) => { search = href.split("?")[1] || ""; } } }, require: (name) => {
      if (name === "react") return hooks; if (name === "react/jsx-runtime") return require(name);
      if (name === "next/navigation") return { useSearchParams: () => new URLSearchParams(search) };
      if (name.endsWith("RuntimeProvider.js")) return { useRuntime: () => ({ companyId: company, status: "ready", snapshot: { company: { company_id: company, name: company } } }) };
      if (name.endsWith("CeoDeskOperating.js")) return { CreateBusiness };
      if (name.endsWith("runtimeApi.js")) return runtimeApi;
      if (name.endsWith("v1FrontendApi.js")) return v1;
      if (name.endsWith("writingApi.js")) return { confirmationSnapshot, writingRequestLocked, createWritingApi: () => ({ entry: async () => routeDTO?.writing_entry || ({ scope: { company_id: company, workspace_id: `workspace-${company}` }, execution: { status: "UNAVAILABLE" } }) }) };
      if (name.endsWith("organizationProjection.js")) return { buildOrganizationProjection };
      if (name.endsWith("BusinessCatalogSurface.js")) return { __esModule: true, ...Catalog, ...(proposalMode === "directoryPending" ? {} : catalog), BusinessCatalogPaneContent: inert.default };
      if (name.endsWith("musicState.mjs")) return { MUSIC_PACKAGE: { id: "music" } };
      if (name.endsWith("api.js")) return { CEO_ID: routeDTO?.founding_get.owner_ref || "CEO" };
      return inert;
    } }); return loaded.exports;
  }
  Catalog = await load("components/v1/BusinessCatalogSurface.js", false);
  ({ CreateBusiness, LocalBusinessProposal } = await load("components/v1/CeoDeskOperating.js", false));
  const Page = (await load("app/ceo-office/business/page.js", true)).BusinessSurface;
  const render = (c, fn, props) => { context = c; c.si = 0; c.ri = 0; c.ei = 0; return fn(props); };
  const effects = (c) => { for (const e of c.effects) if (e.pending) { e.cleanup?.(); e.pending = false; e.cleanup = e.fn(); } };
  const find = (n, match) => !n ? null : Array.isArray(n) ? n.map((v) => find(v, match)).find(Boolean) : match(n) ? n : find(n.props?.children, match);
  let last, lastPage;
  async function step() {
    render(parent, Page); effects(parent);
    const pageTree = render(parent, Page), node = find(pageTree, (n) => n.type === CreateBusiness); lastPage = pageTree;
    if (!node || childKey !== node.key) { if (child) for (const e of child.effects) e.cleanup?.(); child = null; childKey = null; }
    if (node) { if (!child) { child = { states: [], refs: [], effects: [] }; childKey = node.key; mounts++; } last = render(child, CreateBusiness, node.props); if (last.type === LocalBusinessProposal) last = LocalBusinessProposal(last.props); effects(child); }
    while (requests.length) requests.shift()();
    await new Promise((resolve) => setTimeout(resolve, 0));
  }
  return { step, tree: () => last, pendingLinks: () => {
    const node = find(lastPage, n => n.type === Catalog.default);
    if (!node) return [];
    const tree = render({ states: [], refs: [], effects: [] }, Catalog.default, node.props);
    const links = [];
    const walk = n => { if (!n) return; if (Array.isArray(n)) return n.forEach(walk); if (n.props?.href?.includes("founding_run_id=")) links.push(n.props.href); walk(n.props?.children); };
    walk(tree); return links;
  }, openNormalPending: () => {
    const node = find(lastPage, n => n.type === Catalog.default); assert.ok(node, "cold normal page renders actual catalog");
    const tree = render({ states: [], refs: [], effects: [] }, Catalog.default, node.props);
    const link = find(tree, n => n.props?.href?.includes("founding_run_id=")); assert.ok(link, "actual pending organization must generate a normal continue link");
    const url = new URL(link.props.href, "http://localhost");
    assert.equal(url.searchParams.get("founding_run_id"), routeDTO.pending_get.entity_id);
    assert.equal(url.searchParams.has("creation_record"), false); search = url.search.slice(1);
  }, openNormalRecord: () => { const link = find(lastPage, (n) => n.props?.children === "查看创建记录"); assert.ok(link, "normal Business must provide its actual creation link"); search = new URL(link.props.href, "http://localhost").search.slice(1); }, counts: () => ({ mounts, listReads, resultReads, confirms, newRuns, saves }), node: (match) => find(last, match), switchCompany: () => { company = "B"; }, queryHandler: () => find(last, (n) => n.props?.children === "查询原确认结果")?.props.onClick };
}

test("real page+Creator completed original Run restores once and stays mounted", async () => {
  const h = await completedBusinessComposition();
  for (let i = 0; i < 8; i++) await h.step();
  assert.equal(h.counts().mounts, 1, "completed restore must not notify parent into a loading/remount cycle");
  assert.equal(h.counts().listReads, 1); assert.equal(h.counts().confirms, 0);
  assert.ok(JSON.stringify(h.tree()).includes("业务已创建"));
  h.switchCompany(); for (let i = 0; i < 4; i++) await h.step();
  assert.equal(h.counts().listReads, 2); assert.equal(h.counts().mounts, 2, "Company switch legitimately replaces scoped Creator");
});

test("original pending Run query completion refreshes parent once without remount or reconfirmation", async () => {
  const h = await completedBusinessComposition("RUNNING");
  for (let i = 0; i < 3; i++) await h.step();
  const query = h.queryHandler(); assert.equal(typeof query, "function"); await query();
  for (let i = 0; i < 5; i++) await h.step();
  assert.equal(h.counts().mounts, 1); assert.equal(h.counts().listReads, 2); assert.equal(h.counts().confirms, 0);
  await query(); for (let i = 0; i < 3; i++) await h.step();
  assert.equal(h.counts().listReads, 2, "repeated completed original-result query must not notify twice");
  assert.ok(JSON.stringify(h.tree()).includes("业务已创建"));
});

test("normal Business link restores actual original record with empty storage and no new confirmation", async () => {
  const h = await completedBusinessComposition("COMPLETED", true);
  for (let i = 0; i < 3; i++) await h.step();
  assert.equal(h.counts().mounts, 0);
  h.openNormalRecord(); for (let i = 0; i < 7; i++) await h.step();
  assert.equal(h.counts().mounts, 1); assert.equal(h.counts().confirms, 0);
  const text = JSON.stringify(h.tree()); assert.ok(text.includes("业务已创建"));
  assert.equal(text.includes("整理业务提案"), false); assert.equal(text.includes("新建另一项业务"), false);
  assert.equal(text.includes("确认创建业务"), false);
});

test("record-only UNKNOWN query keeps normal original locator without exposing creation actions", async () => {
  const h = await completedBusinessComposition("UNKNOWN", true);
  for (let i = 0; i < 3; i++) await h.step(); h.openNormalRecord();
  for (let i = 0; i < 3; i++) await h.step();
  assert.ok(JSON.stringify(h.tree()).includes("原确认结果待核验"));
  const query = h.queryHandler(); await query(); for (let i = 0; i < 4; i++) await h.step();
  assert.equal(h.counts().confirms, 0); assert.equal(h.counts().mounts, 1);
  assert.ok(JSON.stringify(h.tree()).includes("业务已创建"));
});

test("record-only result cannot claim creation when response Company differs from validated locator", async () => {
  const h = await completedBusinessComposition("COMPLETED", true, "foreign");
  for (let i = 0; i < 3; i++) await h.step(); h.openNormalRecord();
  for (let i = 0; i < 5; i++) await h.step();
  const text = JSON.stringify(h.tree()); assert.equal(text.includes("业务已创建"), false);
  assert.ok(text.includes("原创建结果与当前业务不一致")); assert.equal(h.counts().confirms, 0);
});

test("actual isolated TestClient route DTO feeds normal original-record page and Creator", { skip: !process.env.CURIS_TEST_ROUTE_DTO_PATH && "requires exact isolated TestClient response artifact" }, async () => {
  const { readFileSync } = await import("node:fs");
  const evidence = JSON.parse(readFileSync(process.env.CURIS_TEST_ROUTE_DTO_PATH, "utf8"));
  const dto = evidence.responses;
  assert.equal(Object.hasOwn(dto.founding_get, "data"), false);
  assert.equal(dto.founding_get.first_business.business_id, dto.business_result.creation_result.business_id);
  assert.equal(dto.draft_get.proposal.snapshot.company_id, dto.founding_get.company_id);
  assert.ok(dto.business_result.founding_run.data.firstBusiness);
  const h = await completedBusinessComposition("COMPLETED", true, null, dto);
  for (let i = 0; i < 3; i++) await h.step(); h.openNormalRecord();
  for (let i = 0; i < 7; i++) await h.step();
  assert.ok(JSON.stringify(h.tree()).includes("业务已创建"), "real projection DTO must restore completed original result");
  assert.equal(h.counts().confirms, 0); assert.equal(h.counts().mounts, 1);
});


test("actual HTTP DTO normal new -> save proposal -> explicit confirm -> result survives parent URL update", { skip: !process.env.CURIS_TEST_ROUTE_DTO_PATH }, async () => {
  const { readFileSync } = await import("node:fs");
  const dto = JSON.parse(readFileSync(process.env.CURIS_TEST_ROUTE_DTO_PATH, "utf8")).responses;
  const h = await completedBusinessComposition("COMPLETED", false, null, dto, "new");
  for (let i = 0; i < 3; i++) await h.step();
  h.node(n => n.props?.["aria-label"] === "业务工作空间类型").props.onChange({ target: { value: dto.pending_draft.proposal.package_id } }); await h.step();
  h.node(n => n.props?.["aria-label"] === "业务所属部门").props.onChange({ target: { value: dto.pending_draft.proposal.department_id } });
  h.node(n => n.props?.["aria-label"] === "业务目标").props.onChange({ target: { value: dto.pending_draft.proposal.intent } }); await h.step();
  await h.node(n => n.type === "form").props.onSubmit({ preventDefault() {} });
  for (let i = 0; i < 3; i++) await h.step();
  assert.ok(JSON.stringify(h.tree()).includes("确认业务提案"));
  assert.equal(h.counts().mounts, 1); assert.equal(h.counts().newRuns, 1); assert.equal(h.counts().confirms, 0);
  h.node(n => n.props?.type === "checkbox").props.onChange({ target: { checked: true } }); await h.step();
  await h.node(n => n.props?.children === "确认创建业务").props.onClick();
  for (let i = 0; i < 5; i++) await h.step();
  assert.ok(JSON.stringify(h.tree()).includes("业务已创建"));
  assert.equal(h.counts().newRuns, 1); assert.equal(h.counts().confirms, 1); assert.equal(h.counts().mounts, 1);
});

test("actual projected pending Run with empty storage restores saved proposal without existing Business or automatic confirmation", { skip: !process.env.CURIS_TEST_ROUTE_DTO_PATH }, async () => {
  const { readFileSync } = await import("node:fs");
  const dto = JSON.parse(readFileSync(process.env.CURIS_TEST_ROUTE_DTO_PATH, "utf8")).responses;
  assert.equal(dto.pending_get.lifecycle_status, "PROPOSED"); assert.equal(Boolean(dto.pending_get.first_business), false);
  const h = await completedBusinessComposition("COMPLETED", false, null, dto, "pending");
  for (let i = 0; i < 6; i++) await h.step();
  assert.ok(JSON.stringify(h.tree()).includes("确认业务提案")); assert.ok(JSON.stringify(h.tree()).includes("章节作者"));
  assert.equal(h.counts().newRuns, 0); assert.equal(h.counts().confirms, 0);
  h.node(n => n.props?.type === "checkbox").props.onChange({ target: { checked: true } }); await h.step();
  await h.node(n => n.props?.children === "确认创建业务").props.onClick();
  for (let i = 0; i < 4; i++) await h.step();
  assert.ok(JSON.stringify(h.tree()).includes("业务已创建")); assert.equal(h.counts().newRuns, 0); assert.equal(h.counts().confirms, 1);
});

test("pending restore rejects foreign owner, duplicate Run and unknown state without writes", { skip: !process.env.CURIS_TEST_ROUTE_DTO_PATH }, async () => {
  const { readFileSync } = await import("node:fs");
  const dto = JSON.parse(readFileSync(process.env.CURIS_TEST_ROUTE_DTO_PATH, "utf8")).responses;
  for (const mode of ["foreign", "duplicate", "unknown"]) {
    const h = await completedBusinessComposition("COMPLETED", false, null, dto, mode);
    for (let i = 0; i < 5; i++) await h.step();
    assert.equal(JSON.stringify(h.tree()).includes("确认创建业务"), false, mode);
    assert.ok(JSON.stringify(h.tree()).includes("无法确认"), mode);
    assert.equal(h.counts().confirms, 0); assert.equal(h.counts().newRuns, 0); assert.equal(h.counts().saves, 0);
  }
});


test("cold real Company catalog -> actual pending organization link -> original saved proposal -> explicit confirm", { skip: !process.env.CURIS_TEST_ROUTE_DTO_PATH }, async () => {
  const { readFileSync } = await import("node:fs");
  const dto = JSON.parse(readFileSync(process.env.CURIS_TEST_ROUTE_DTO_PATH, "utf8")).responses;
  assert.equal(dto.pending_organization.pending_business_proposals.length, 1);
  assert.equal(dto.pending_organization.pending_business_proposals[0].founding_run_id, dto.pending_get.entity_id);
  const h = await completedBusinessComposition("COMPLETED", false, null, dto, "directoryPending");
  for (let i=0;i<4;i++) await h.step();
  assert.equal(h.counts().mounts, 0); assert.equal(h.pendingLinks().length, 1);
  h.openNormalPending(); for (let i=0;i<5;i++) await h.step();
  assert.ok(JSON.stringify(h.tree()).includes("确认业务提案"));
  assert.equal(h.counts().newRuns, 0); assert.equal(h.counts().saves, 0); assert.equal(h.counts().confirms, 0);
  h.node(n=>n.props?.type==="checkbox").props.onChange({target:{checked:true}}); await h.step();
  await h.node(n=>n.props?.children==="确认创建业务").props.onClick();
  for (let i=0;i<4;i++) await h.step();
  assert.ok(JSON.stringify(h.tree()).includes("业务已创建"));
  assert.equal(h.counts().newRuns, 0); assert.equal(h.counts().confirms, 1);
  const stale=await completedBusinessComposition("COMPLETED", false, null, dto, "directoryPending");
  for (let i=0;i<4;i++) await stale.step(); stale.switchCompany();
  for (let i=0;i<4;i++) await stale.step(); assert.equal(stale.pendingLinks().length, 0);
});

test('explicit selected-work return validates the real scoped collection without inventing a chapter', async () => {
  const { writingReturnTarget, validateWritingReturn, WRITING_PACKAGE } = await import('../lib/writingApi.js').then(async api => ({ ...api, ...(await import('../lib/writingState.mjs')) }));
  const { validateBusinessReturn } = await import('../lib/businessReturnApi.js');
  const { TENANT_ID } = await import('../lib/api.js');
  const href = '/ceo-office/workspace/installed/w?writing_mode=books&book_ref=book';
  const instance = { instance_id: 'i', company_id: 'co', workspace_id: 'w', package_id: WRITING_PACKAGE.id, package_version: WRITING_PACKAGE.version, package_digest: WRITING_PACKAGE.digest, status: 'ACTIVE' };
  const collection = { scope: { ...instance, tenant_id: TENANT_ID }, books: [{ ref: 'book', title: '实际作品' }], chapters: [] };
  const detail = { instance, read_only: false, package: { package_id: WRITING_PACKAGE.id, version: WRITING_PACKAGE.version, digest: WRITING_PACKAGE.digest, status: 'ACTIVE' }, schemas: { WritingBook: { schemaVersion: 'writing.book/v1' }, WritingChapter: { schemaVersion: 'writing.chapter/v1' } } };
  const calls = [];
  const request = async (path, options) => { assert.equal(options, undefined); calls.push(path); return path === '/api/workspace/packages/workspaces/w' ? detail : collection; };
  assert.equal((await validateWritingReturn(href, 'co', request)).label, '返回当前作品');
  assert.equal((await validateBusinessReturn('writing', href, { employeeCompany: 'co', request })).entry.book, 'book');
  assert.equal(calls.some(path => path.includes('/chapters/')), false);
  await assert.rejects(validateWritingReturn(href.replace('book_ref=book', 'book_ref=missing'), 'co', request));
  await assert.rejects(validateBusinessReturn('writing', href, { employeeCompany: 'foreign', request }));
  await assert.rejects(validateBusinessReturn('writing', href, { request: async path => path.includes('/packages/') ? detail : { ...collection, scope: { ...collection.scope, tenant_id: 'foreign' } } }));
  const operatingHref=href+'&wr_view=market';
  const operating=await validateWritingReturn(operatingHref,'co',request);assert.equal(operating.entry.book,'book');assert.equal(operating.entry.view,'market');
  assert.equal((await validateBusinessReturn('writing',operatingHref,{employeeCompany:'co',request})).entry.view,'market');
  assert.equal(calls.some(path=>path.includes('/chapters/')),false);
  for (const bad of ['?book_ref=book', '?writing_mode=chapter&book_ref=book', '?writing_mode=books&book_ref=book&draft_ref=d', '?writing_mode=books&book_ref=book&anchor=d:0:1', '?writing_mode=books&book_ref=book&book_ref=foreign']) assert.throws(() => writingReturnTarget('/ceo-office/workspace/installed/w'+bad));
});
