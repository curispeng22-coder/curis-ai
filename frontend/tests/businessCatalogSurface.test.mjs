import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import vm from "node:vm";

const require = createRequire(import.meta.url);
const React = require("react");
const { renderToStaticMarkup } = require("react-dom/server");
const swc = require("next/dist/build/swc");
await swc.loadBindings();
const source = readFileSync(new URL("../components/v1/BusinessCatalogSurface.js", import.meta.url), "utf8");
const { code } = await swc.transform(source, { filename: "BusinessCatalogSurface.js", isModule: true,
  jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } }, module: { type: "commonjs" } });
const loaded = { exports: {} };
vm.runInNewContext(code, { module: loaded, exports: loaded.exports, URLSearchParams,
  require: (name) => {
    if (["react", "react/jsx-runtime"].includes(name)) return require(name);
    if (name.includes("runtimeApi")) return { workspaceOfficeHref: (w) => `/ceo-office/workspace/installed/${encodeURIComponent(w.workspace_id)}` };
    if (name === "next/link") return { __esModule: true, default: (props) => React.createElement("a", props) };
    if (name === "next/image") return { __esModule: true, default: ({ src, ...props }) => React.createElement("img", { ...props, src: src.src }) };
    if (name.endsWith(".png")) return { __esModule: true, default: { src: "/approved-reference.png" } };
    if (name.endsWith(".module.css")) return { __esModule: true, default: new Proxy({}, { get: (_, key) => key }) };
    if (name.endsWith("TerraShell.js")) return { TerraPaneContent: (props) => React.createElement("section", { "data-real-panes": true }, props.contextPane, props.utilityTabs?.map((tab) => React.createElement("article", { key: tab.id }, tab.content))) };
    return { TerraIcon: () => React.createElement("span", { "aria-hidden": true }) };
  } });
const { BUSINESS_DIRECTIONS, businessCatalogProjection: project, businessCatalogSelection: select, businessCatalogHref: href, default: Catalog } = loaded.exports;
const company = { company_id: "A", name: "真实测试公司" };
const businesses = [{ business_id: "one", company_id: "A", name: "第一项写作", workspaces: [] }, { business_id: "two", company_id: "A", name: "第二项写作", workspaces: [] }];
const props = { company, businesses: [], organization: null, definitions: null };

test("normal and empty entry are directory, never first business or creation", () => {
  assert.equal(select(new URLSearchParams(), "A", businesses).kind, "directory");
  assert.equal(select(new URLSearchParams(), "A", []).kind, "directory");
  assert.equal(select(new URLSearchParams("new=1"), "A", []).kind, "create");
});
test("multiple same-direction businesses retain exact canonical identity", () => {
  const choice = select(new URLSearchParams("company_id=A&business_id=two"), "A", businesses);
  assert.equal(choice.business, businesses[1]);
  const url = href("A", { businessId: "two" });
  assert.equal(select(new URL(url, "http://local").searchParams, "A", businesses).business.business_id, "two");
});
test("foreign, duplicate, unknown and mixed selection fail closed", () => {
  for (const query of ["company_id=B&business_id=one", "business_id=foreign", "definition=external", "definition=writing&definition=music", "business_id=one&definition=writing", "company_id=A&company_id=B"]) assert.equal(select(new URLSearchParams(query), "A", businesses).kind, "invalid");
  assert.equal(select(new URLSearchParams("business_id=foreign"), "A", [{ business_id: "foreign", company_id: "B" }]).kind, "invalid");
});
test("all three references remain readable without availability or team fabrication", () => {
  assert.equal(BUSINESS_DIRECTIONS.length, 3);
  const view = project("A", [], null, null);
  assert.ok(view.directions.every((item) => item.definition === null && !item.availabilityKnown));
  const unavailable = project("A", [], null, { available: false, definitions: [{ package_id: "com.curis.local.content-growth", published: false }] });
  assert.equal(unavailable.directions[0].definition, null);
  assert.ok(unavailable.directions.every((item) => item.availabilityKnown));
});
test("support department needs actual scoped responsibility; template labels cannot create it", () => {
  const organization = { company, departments: [{ id: "support", company_id: "A", name: "实际支持部门" }, { id: "other", company_id: "B", name: "外公司" }, { id: "empty", company_id: "A", name: "未绑定部门" }], departmentAssignments: [{ company_id: "A", data: { responsibilityKey: "space.engineering.leadership", scopeRef: "support" } }, { company_id: "B", data: { responsibilityKey: "data.analytics.company_analysis", scopeRef: "other" } }] };
  assert.equal(project("A", businesses, organization).departments.length, 1);
  assert.equal(project("A", businesses, organization).departments[0].name, "实际支持部门");
  assert.equal(project("A", businesses, { ...organization, company: { company_id: "B" } }).departments.length, 0);
});
test("empty catalog renders three reading entries and no form, employee count or invented identity", () => {
  const html = renderToStaticMarkup(React.createElement(Catalog, props));
  for (const title of ["公司支持部门", "当前业务", "内容增长 · 写作 · 音乐", "内容增长", "写作", "音乐", "还没有经营中的业务"]) assert.ok(html.includes(title));
  assert.equal(html.includes("<form"), false);
  assert.equal(html.includes("名员工"), false);
  assert.equal(html.includes("business_id="), false);
});
test("compact directory keeps direction names and doors prominent without hiding real empty or unavailable state", () => {
  const html = renderToStaticMarkup(React.createElement(Catalog, props));
  for (const name of ["内容增长", "写作", "音乐"]) assert.ok(html.indexOf(`<h3>${name}</h3>`) < html.indexOf(`alt="${name}工作参考"`));
  assert.equal((html.match(/了解能力与边界/g) || []).length, 3);
  assert.ok(html.includes("还没有经营中的业务")); assert.ok(html.includes("未提供可用定义"));
  const css = readFileSync(new URL("../components/v1/BusinessCatalogSurface.module.css", import.meta.url), "utf8");
  assert.match(css, /minmax\(min\(100%, 240px\)/); assert.match(css, /minmax\(min\(100%, 178px\)/);
  assert.equal(/\.department\s*\{[^}]*border:/.test(css), false);
});
test("definition detail has a scoped return and disabled activation even when local definition reads", () => {
  const html = renderToStaticMarkup(React.createElement(Catalog, { ...props, definitionId: "writing", definitions: { definitions: [{ package_id: "com.curis.local.writing-authoring", name: "本地写作工作空间" }] } }));
  assert.ok(html.includes("本地写作工作空间"));
  assert.ok(html.includes("company_id=A"));
  const paneHtml = renderToStaticMarkup(React.createElement(loaded.exports.BusinessCatalogPaneContent, { ...props, definitions: { definitions: [{ package_id: "com.curis.local.writing-authoring", name: "本地写作工作空间" }] }, definitionStatus: "ready", selection: { kind: "definition", definitionId: "writing" } }));
  assert.ok(paneHtml.includes("disabled"));
  assert.ok(paneHtml.includes("当前未提供可创建的业务定义或初始团队合同"));
  assert.equal(html.includes("<aside"), false);
  assert.equal(html.includes("<form"), false);
});

function deferred() {
  let resolve, reject;
  const promise = new Promise((yes, no) => { resolve = yes; reject = no; });
  return { promise, resolve, reject };
}
const flushReads = () => new Promise((resolve) => setImmediate(resolve));

async function pageReadHarness(readBusinesses, readDefinitions, { readOrganization = (id) => Promise.resolve({ company: { company_id: id }, departmentAssignments: [] }), createWork = () => Promise.reject(new Error("not released")), query = "" } = {}) {
  const pageSource = readFileSync(new URL("../app/ceo-office/business/page.js", import.meta.url), "utf8");
  const { code: pageCode } = await swc.transform(pageSource, { filename: "page.js", isModule: true,
    jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } }, module: { type: "commonjs" } });
  const states = [], refs = [], effects = [];
  let index = 0, refIndex = 0, cleanups = [], runtime;
  const pageModule = { exports: {} };
  vm.runInNewContext(pageCode, { module: pageModule, exports: pageModule.exports, URLSearchParams, crypto: { randomUUID: () => "request-1" },
    require: (name) => {
      if (name === "react") return { ...React, useState: (initial) => {
        const key = index++;
        if (!(key in states)) states[key] = initial;
        return [states[key], (next) => { states[key] = typeof next === "function" ? next(states[key]) : next; }];
      }, useRef: (initial) => { const key = refIndex++; refs[key] ??= { current: initial }; return refs[key]; }, useEffect: (effect) => effects.push(effect) };
      if (name === "react/jsx-runtime") return require(name);
      if (name === "next/navigation") return { useSearchParams: () => new URLSearchParams(query) };
      if (name.endsWith("RuntimeProvider.js")) return { useRuntime: () => runtime };
      if (name.endsWith("BusinessCatalogSurface.js")) return loaded.exports;
      if (name.endsWith("runtimeApi.js")) return { getCanonicalBusinesses: readBusinesses,
        getOrganizationProjection: readOrganization, runtimeErrorMessage: () => "读取失败" };
      if (name.endsWith("v1FrontendApi.js")) return { getBusinessDefinitions: readDefinitions, createAssignedWork: createWork };
      return {};
    } });
  const root = pageModule.exports.default();
  const Surface = root.props.children.props.children.type;
  return {
    mount: (companyId) => {
      for (const cleanup of cleanups) cleanup?.();
      runtime = { companyId, status: "ready", snapshot: { company: { company_id: companyId } } };
      index = refIndex = 0; effects.length = 0; Surface();
      cleanups = effects.map((effect) => effect());
    },
    view: () => states.find((state) => state && "businesses" in state),
    definitionRead: () => states.find((state) => state && "payload" in state),
    delegation: () => states.find((state) => state && "pending" in state && "goal" in state),
    render: () => { index = refIndex = 0; return Surface(); },
  };
}

test("settled real businesses remain readable when definition request never settles", async () => {
  const definitions = deferred();
  const page = await pageReadHarness(() => Promise.resolve({ businesses }), () => definitions.promise);
  page.mount("A"); await flushReads();
  assert.equal(page.view().status, "ready");
  assert.equal(page.view().businesses.length, 2);
});

test("creation cannot override a mixed business or definition selector", () => {
  for (const query of ["new=1&business_id=foreign", "new=1&business_id=one", "new=1&definition=writing", "new=1&definition=foreign", "new=1&business_id=", "new=1&definition=writing&business_id=one"]) {
    assert.equal(select(new URLSearchParams(query), "A", businesses).kind, "invalid", query);
  }
});

test("definition failure stays distinct from empty or unpublished while businesses remain ready", async () => {
  const page = await pageReadHarness(() => Promise.resolve({ businesses }), () => Promise.reject(new Error("controlled definition failure")));
  page.mount("A"); await flushReads();
  assert.equal(page.view().status, "ready");
  assert.equal(page.definitionRead().status, "error");
  assert.equal(page.definitionRead().payload, null);
  const loading = renderToStaticMarkup(React.createElement(Catalog, { ...props, definitionId: "writing", definitionStatus: "loading" }));
  const failed = renderToStaticMarkup(React.createElement(Catalog, { ...props, definitionId: "writing", definitionStatus: "error" }));
  assert.ok(loading.includes("正在读取可用范围"));
  assert.ok(failed.includes("可用范围暂时无法读取"));
  assert.equal(failed.includes("当前尚不可启用"), false);
});

test("late old-company definition success or failure cannot replace current scope", async () => {
  for (const fail of [false, true]) {
    const old = deferred();
    const current = { definitions: [{ package_id: "com.curis.local.writing-authoring", name: "当前公司定义" }] };
    const page = await pageReadHarness((id) => Promise.resolve({ businesses: businesses.map((item) => ({ ...item, company_id: id })) }), (id) => id === "A" ? old.promise : Promise.resolve(current));
    page.mount("A"); await flushReads(); page.mount("B"); await flushReads();
    if (fail) old.reject(new Error("late old read")); else old.resolve({ definitions: [{ name: "旧公司定义" }] });
    await flushReads();
    assert.equal(page.view().companyId, "B");
    assert.equal(page.definitionRead().companyId, "B");
    assert.equal(page.definitionRead().status, "ready");
    assert.equal(page.definitionRead().payload, current);
  }
});

test("catalog consumer provides real empty navigation and company/definition tabs, no page-local fourth pane", () => {
  const html = renderToStaticMarkup(React.createElement(loaded.exports.BusinessCatalogPaneContent, { ...props, definitionStatus: "loading", selection: { kind: "directory" } }));
  assert.ok(html.includes("业务导航")); assert.ok(html.includes("还没有经营中的业务"));
  assert.ok(html.includes("当前公司") || html.includes(company.name));
  assert.ok(html.includes("正在读取可用范围"));
  assert.notEqual(loaded.exports.businessPaneId("A", "definition", "writing"), loaded.exports.businessPaneId("B", "definition", "writing"));
  assert.notEqual(loaded.exports.businessPaneId("A", "business", "one"), loaded.exports.businessPaneId("A", "business", "two"));
});

test("directory grid contract fits three readable cards in the observed narrow Main without window breakpoints", () => {
  const css = readFileSync(new URL("../components/v1/BusinessCatalogSurface.module.css", import.meta.url), "utf8");
  const grid = css.match(/\.directionGrid\s*\{([^}]+)\}/)[1];
  const minimum = Number(grid.match(/minmax\(min\(100%, (\d+)px\), 1fr\)/)[1]);
  const gap = Number(grid.match(/gap: (\d+)px/)[1]);
  const columns = (width) => Math.min(3, Math.floor((width + gap) / (Math.min(width, minimum) + gap)));
  assert.equal(columns(586), 3);
  assert.equal(columns(560), 3);
  assert.equal(columns(557), 2, "below readable threshold wraps rather than squeezing text");
  assert.equal(columns(140), 1);
  assert.equal((css.match(/\.directionGrid\s*\{/g) || []).length, 1, "no window rule overrides intrinsic Main sizing");
  assert.match(css, /\.directionTitle h3\s*\{ font-size: 18px;/);
  assert.match(css, /\.page p\s*\{[^}]*font-size: 14px;/);
  assert.match(css, /\.primary, \.action\s*\{[^}]*font-size: 14px;/);
  assert.match(css, /\.photo\s*\{[^}]*height: 104px;/);
  assert.equal(/(?:display:\s*none|visibility:\s*hidden|line-clamp|text-overflow)/.test(grid), false);
});

test("only server-available matching Writing team contract offers ordinary creation", () => {
  const definition = { package_id: "com.curis.local.writing-authoring", version: "0.1.0", digest: "approved", name: "本地写作工作空间",
    initial_team_contract: { packageId: "com.curis.local.writing-authoring", packageVersion: "0.1.0", packageDigest: "approved", sha256: "contract", displayName: "章节作者" } };
  const direction = { id: "writing", packageId: definition.package_id, definition };
  assert.equal(loaded.exports.directionCreationReady(direction, "ready"), true);
  assert.equal(loaded.exports.directionCreationReady(direction, "loading"), false);
  assert.equal(loaded.exports.directionCreationReady({ ...direction, id: "music" }, "ready"), false);
  assert.equal(loaded.exports.directionCreationReady({ ...direction, definition: { ...definition, digest: "changed" } }, "ready"), false);
  const html = renderToStaticMarkup(React.createElement(Catalog, { ...props, definitionId: "writing", definitions: { definitions: [definition] }, definitionStatus: "ready" }));
  assert.ok(html.includes("创建时将配备章节作者")); assert.ok(html.includes("自检不等于独立审核"));
  assert.ok(html.includes("new=1")); assert.equal(html.includes("已连接"), false);
});

test('saved PROPOSED proposals use actual Company-scoped normal continue links and exclude duplicate references', () => {
  const item = { company_id: 'A', founding_run_id: 'actual-pending', business_name: '保存的第二写作', lifecycle_status: 'PROPOSED' };
  const organization = { company, pending_business_proposals: [item, { ...item, company_id: 'B', founding_run_id: 'foreign' }, { ...item, lifecycle_status: 'UNKNOWN', founding_run_id: 'unknown' }] };
  const html = renderToStaticMarkup(React.createElement(Catalog, { ...props, organization }));
  assert.ok(html.includes('继续创建')); assert.ok(html.includes('保存的第二写作'));
  const match = html.match(/href="([^"]*founding_run_id[^"]*)"/); assert.ok(match);
  const query = new URL(match[1].replaceAll('&amp;', '&'), 'http://local').searchParams;
  assert.equal(query.get('company_id'), 'A'); assert.equal(query.get('new'), '1'); assert.equal(query.get('founding_run_id'), item.founding_run_id);
  assert.equal(query.has('creation_record'), false); assert.equal(html.includes('foreign'), false); assert.equal(html.includes('unknown'), false);
  const stale = renderToStaticMarkup(React.createElement(Catalog, { ...props, organization: { ...organization, company: { company_id: 'B' } } }));
  assert.equal(stale.includes('继续创建'), false);
  assert.equal(project('A', [], { company, pending_business_proposals: [item, { ...item }] }).pendingProposals.length, 0);
});

function findElement(node, predicate) {
  if (Array.isArray(node)) return node.map((item) => findElement(item, predicate)).find(Boolean) || null;
  if (!React.isValidElement(node)) return null;
  if (predicate(node)) return node;
  return findElement(node.props.children, predicate);
}

test("Music direction resolves to a real sprite symbol", async () => {
  const iconSource = readFileSync(new URL("../components/terra/TerraIcons.js", import.meta.url), "utf8");
  const { code: iconCode } = await swc.transform(iconSource, { filename: "TerraIcons.js", isModule: true,
    jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "classic" } } }, module: { type: "commonjs" } });
  const icons = { exports: {} };
  new Function("require", "module", "exports", "React", iconCode)(() => ({}), icons, icons.exports, React);
  const sprite = renderToStaticMarkup(React.createElement(icons.exports.TerraIconSprite));
  assert.equal(BUSINESS_DIRECTIONS.find((item) => item.id === "music").icon, "i-music_note");
  assert.match(sprite, /<symbol id="i-music_note" viewBox="0 0 24 24"><path d="[^"]+"><\/path><\/symbol>/);
});

test("engineering delegation shows only a verified same-scope child Work receipt", async () => {
  const leader = { entity_id: "assignment-a", entity_type: "RESPONSIBILITY_ASSIGNMENT", tenant_id: "tenant-a", company_id: "A", workspace_id: null, lifecycle_status: "ACTIVE", data: { responsibilityKey: "space.engineering.leadership", responsibility: "为公司建立业务空间", scopeType: "DEPARTMENT", scopeRef: "engineering", employeeRef: "runtime-employee-a", companyEmployeeRef: "company-employee-a", revision: 1, isLeader: true } };
  const reads = () => Promise.resolve({ businesses: [] });
  const payloads = [];
  const page = await pageReadHarness(reads, () => Promise.resolve({ definitions: [] }), {
    query: "new=1", readOrganization: () => Promise.resolve({ company, departmentAssignments: [leader] }),
    createWork: (assignment, payload) => {
      payloads.push({ assignment, payload });
      return Promise.resolve({
        cycle: { entity_id: "cycle-a", entity_type: "CYCLE", tenant_id: "tenant-a", company_id: "A", workspace_id: null,
          data: { kind: "GENERAL_WORK_CYCLE", scopeType: "DEPARTMENT", scopeRef: "engineering", releaseKey: payload.request_id, contract: { problem: payload.problem, expectedResult: payload.expected_result, constraints: [], references: [] } } },
        work: { entity_id: "work-a", entity_type: "WORK", tenant_id: "tenant-a", company_id: "A", workspace_id: null, parent_id: "cycle-a", owner_ref: "runtime-employee-a", lifecycle_status: "PLANNED",
          data: { kind: "CANONICAL_CHILD_WORK", cycleRef: "cycle-a", scopeType: "DEPARTMENT", scopeRef: "engineering", releaseKey: "initial", responsibilityAssignmentRef: "assignment-a", holderEmployeeRef: "runtime-employee-a", responsibilityKey: "space.engineering.leadership", responsibility: "为公司建立业务空间", assignmentRevision: 1 } },
      });
    },
  });
  page.mount("A"); await flushReads();
  const input = findElement(page.render(), (node) => node.type === "input" && node.props["aria-label"] === "委托空间工程的目标");
  assert.ok(input);
  input.props.onChange({ target: { value: "建立歌曲业务" } });
  const form = findElement(page.render(), (node) => node.type === "form" && typeof node.props.onSubmit === "function");
  assert.ok(form); await form.props.onSubmit({ preventDefault() {} });
  assert.equal(payloads.length, 1); assert.equal(payloads[0].assignment, "assignment-a");
  assert.equal(payloads[0].payload.problem, "建立歌曲业务");
  assert.equal(page.delegation().work.entity_id, "work-a");
  const receipt = findElement(page.render(), (node) => node.props.role === "status");
  assert.ok(receipt);
  const receiptText = renderToStaticMarkup(receipt);
  assert.match(receiptText, /委托已记录/); assert.match(receiptText, /建立歌曲业务/);
  assert.match(receiptText, /为公司建立业务空间/); assert.match(receiptText, /尚未执行/);
  assert.doesNotMatch(receiptText, /工作详情/);
});

test("engineering UNKNOWN keeps the captured payload and blocks another POST; stale and bad lineage never become receipts", async () => {
  const leader = { entity_id: "assignment-a", entity_type: "RESPONSIBILITY_ASSIGNMENT", tenant_id: "tenant-a", company_id: "A", workspace_id: null, lifecycle_status: "ACTIVE", data: { responsibilityKey: "space.engineering.leadership", responsibility: "原责任", scopeType: "DEPARTMENT", scopeRef: "engineering", employeeRef: "runtime-a", companyEmployeeRef: "company-a", revision: 1, isLeader: true } };
  for (const outcome of ["network", "bad-lineage", "late-company"]) {
    const pending = deferred(), calls = [];
    const page = await pageReadHarness(() => Promise.resolve({ businesses: [] }), () => Promise.resolve({ definitions: [] }), {
      query: "new=1", readOrganization: (id) => Promise.resolve({ company: { company_id: id }, departmentAssignments: [{ ...leader, company_id: id }] }),
      createWork: (assignment, payload) => { calls.push({ assignment, payload }); return pending.promise; },
    });
    page.mount("A"); await flushReads();
    findElement(page.render(), (node) => node.type === "input" && node.props["aria-label"] === "委托空间工程的目标").props.onChange({ target: { value: "原始目标" } });
    const submit = findElement(page.render(), (node) => node.type === "form" && typeof node.props.onSubmit === "function").props.onSubmit({ preventDefault() {} });
    assert.equal(calls.length, 1);
    if (outcome === "late-company") page.mount("B");
    if (outcome === "network") pending.reject(new Error("network unknown"));
    else pending.resolve({ cycle: { entity_id: "cycle-a", entity_type: "CYCLE", tenant_id: "tenant-a", company_id: "A", workspace_id: null,
      data: { kind: "GENERAL_WORK_CYCLE", scopeType: "DEPARTMENT", scopeRef: "engineering", releaseKey: calls[0].payload.request_id, contract: { problem: "原始目标", expectedResult: calls[0].payload.expected_result, constraints: [], references: [] } } },
      work: { entity_id: "work-a", entity_type: "WORK", tenant_id: "tenant-a", company_id: "A", workspace_id: null, parent_id: "wrong-cycle", owner_ref: "runtime-a", lifecycle_status: "PLANNED",
        data: { kind: "CANONICAL_CHILD_WORK", cycleRef: "cycle-a", scopeType: "DEPARTMENT", scopeRef: "engineering", releaseKey: "initial", responsibilityAssignmentRef: "assignment-a", holderEmployeeRef: "runtime-a", responsibilityKey: "space.engineering.leadership", responsibility: "原责任", assignmentRevision: 1 } } });
    await submit;
    if (outcome === "late-company") { assert.equal(page.delegation().companyId, "B"); assert.equal(page.delegation().work, null); continue; }
    assert.equal(page.delegation().work, null); assert.equal(page.delegation().uncertain, true);
    assert.equal(page.delegation().pending.problem, "原始目标"); assert.equal(page.delegation().pending.request_id, calls[0].payload.request_id);
    const locked = findElement(page.render(), (node) => node.type === "input" && node.props["aria-label"] === "委托空间工程的目标");
    assert.equal(locked.props.disabled, true);
    await findElement(page.render(), (node) => node.type === "form" && typeof node.props.onSubmit === "function").props.onSubmit({ preventDefault() {} });
    assert.equal(calls.length, 1);
  }
});

test("authoritative assignment rejection preserves the goal and permits a new request", async () => {
  const leader = { entity_id: "assignment-a", entity_type: "RESPONSIBILITY_ASSIGNMENT", tenant_id: "tenant-a", company_id: "A", workspace_id: null, lifecycle_status: "ACTIVE", data: { responsibilityKey: "space.engineering.leadership", scopeType: "DEPARTMENT", scopeRef: "engineering", employeeRef: "runtime-a", companyEmployeeRef: "company-a", isLeader: true } };
  const page = await pageReadHarness(() => Promise.resolve({ businesses: [] }), () => Promise.resolve({ definitions: [] }), {
    query: "new=1", readOrganization: () => Promise.resolve({ company, departmentAssignments: [leader] }),
    createWork: () => Promise.reject({ status: 422 }),
  });
  page.mount("A"); await flushReads();
  findElement(page.render(), (node) => node.type === "input" && node.props["aria-label"] === "委托空间工程的目标").props.onChange({ target: { value: "保留的目标" } });
  await findElement(page.render(), (node) => node.type === "form" && typeof node.props.onSubmit === "function").props.onSubmit({ preventDefault() {} });
  assert.equal(page.delegation().goal, "保留的目标");
  assert.equal(page.delegation().uncertain, false);
  assert.equal(page.delegation().pending, null);
  assert.equal(page.delegation().request, "");
  assert.equal(findElement(page.render(), (node) => node.type === "input" && node.props["aria-label"] === "委托空间工程的目标").props.disabled, false);
});

async function ceoHarness(attention, businessPayload = { company_id: "A", businesses: [] }) {
  const ceoSource = readFileSync(new URL("../components/v1/CeoDeskOperating.js", import.meta.url), "utf8");
  const { code: ceoCode } = await swc.transform(ceoSource, { filename: "CeoDeskOperating.js", isModule: true,
    jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } }, module: { type: "commonjs" } });
  const values = [], refs = [];
  let index = 0, refIndex = 0, load;
  const runtime = { companyId: "A", status: "ready", snapshot: { company } };
  const hookReact = { ...React,
    useState: (initial) => { const key = index++; if (!(key in values)) values[key] = initial; return [values[key], (next) => { values[key] = typeof next === "function" ? next(values[key]) : next; }]; },
    useRef: (initial) => { const key = refIndex++; refs[key] ??= { current: initial }; return refs[key]; },
    useEffect: () => {}, useCallback: (callback) => { load = callback; return callback; },
  };
  const mod = { exports: {} };
  vm.runInNewContext(ceoCode, { module: mod, exports: mod.exports, URLSearchParams,
    require: (name) => {
      if (name === "react") return hookReact;
      if (name === "react/jsx-runtime") return require(name);
      if (name.endsWith("RuntimeProvider.js")) return { useRuntime: () => runtime };
      if (name.endsWith("v1FrontendApi.js")) return { getCompanyAttention: () => attention instanceof Error ? Promise.reject(attention) : Promise.resolve(attention), getCEOAssistantConversation: () => Promise.resolve({}), getV1Presentation: () => Promise.resolve({}), conversationError: (_error, fallback) => fallback };
      if (name.endsWith("runtimeApi.js")) return { getCanonicalBusinesses: () => Promise.resolve(businessPayload) };
      if (name.endsWith("api.js")) return { getAssistantIdentity: () => Promise.resolve({}) };
      return { __esModule: true, default: () => null };
    } });
  const render = () => { index = refIndex = 0; return mod.exports.default(); };
  render();
  return { render, load: () => load(), view: () => values[0] };
}

function elementText(node) {
  if (Array.isArray(node)) return node.map(elementText).join(" ");
  if (typeof node === "string" || typeof node === "number") return String(node);
  return React.isValidElement(node) ? elementText(node.props.children) : "";
}

function countElements(node, predicate) {
  if (Array.isArray(node)) return node.reduce((sum, item) => sum + countElements(item, predicate), 0);
  return React.isValidElement(node) ? Number(predicate(node)) + countElements(node.props.children, predicate) : 0;
}

test("zero-Business CEO Main keeps real same-company attention beside the single creation entry", async () => {
  const item = { source_ref: "matter-1", source_type: "CYCLE", summary: "公司支持事项", status: "ACTIVE", workspace_id: "" };
  const active = await ceoHarness({ company, state: "PARTIAL", items: [item], workspace_count: 0 });
  await active.load();
  assert.equal(active.view().status, "ready");
  const tree = active.render();
  assert.match(elementText(tree), /公司支持事项/);
  assert.equal(countElements(tree, (node) => node.type?.name === "CreateBusiness"), 1);
  assert.equal(elementText(tree).includes("今天没有需要你处理的事项"), false);
  const quiet = await ceoHarness({ company, state: "QUIET", items: [], workspace_count: 0 });
  await quiet.load();
  assert.match(elementText(quiet.render()), /今天没有需要你处理的事项/);
  for (const payload of [{ company: { company_id: "B" }, state: "PARTIAL", items: [item], workspace_count: 0 }, { state: "QUIET", items: [], workspace_count: 0 }, { company, state: "QUIET" }, { company, state: "PARTIAL", items: [], workspace_count: 0 }, { company, state: "QUIET", items: [item], workspace_count: 0 }, new Error("attention unreadable")]) {
    const denied = await ceoHarness(payload);
    await denied.load();
    assert.equal(denied.view().status, "error");
    assert.doesNotMatch(elementText(denied.render()), /经营平稳|公司支持事项/);
  }
});

test("CEO requires a real same-company business array before claiming zero businesses", async () => {
  const attention = { company, state: "QUIET", items: [], workspace_count: 0 };
  const empty = await ceoHarness(attention, { company_id: "A", businesses: [] });
  await empty.load();
  assert.equal(empty.view().status, "ready");
  assert.equal(countElements(empty.render(), (node) => node.type?.name === "CreateBusiness"), 1);
  const filled = await ceoHarness(attention, { company_id: "A", businesses: [{ business_id: "business-1", company_id: "A", name: "真实业务" }] });
  await filled.load();
  assert.equal(filled.view().status, "ready");
  assert.equal(filled.view().businesses[0].business_id, "business-1");
  for (const malformed of [{}, null, { company_id: "A" }, { company_id: "A", businesses: null }, { company_id: "A", businesses: {} }, { company_id: "A", businesses: "not an array" }, { company_id: "B", businesses: [] }, { company_id: "A", businesses: [null] }, { company_id: "A", businesses: [{ business_id: "foreign", company_id: "B", name: "别家公司" }] }, { company_id: "A", businesses: [{ business_id: "", company_id: "A" }] }]) {
    const denied = await ceoHarness(attention, malformed);
    await denied.load();
    assert.equal(denied.view().status, "error", JSON.stringify(malformed));
    assert.doesNotThrow(() => denied.render());
    assert.equal(countElements(denied.render(), (node) => node.type?.name === "CreateBusiness"), 0);
  }
});

test("CEO rejects malformed attention rows before Main or context rendering", async () => {
  const valid = { source_ref: "company-matter", source_type: "CYCLE", summary: "公司部门事项", status: "ACTIVE" };
  const companyMatter = await ceoHarness({ company, state: "PARTIAL", items: [valid], workspace_count: 0 });
  await companyMatter.load();
  assert.equal(companyMatter.view().status, "ready");
  assert.match(elementText(companyMatter.render()), /公司部门事项/);
  for (const bad of [null, 7, {}, { ...valid, source_ref: 7 }, { ...valid, source_type: ["RESULT"] }, { ...valid, source_type: { toString: () => "RESULT" } }, { ...valid, source_type: [] }, { ...valid, summary: { text: "bad" } }, { ...valid, status: null }, { ...valid, workspace_id: {} }, { ...valid, next_check_at: {} }, { ...valid, responsibility_ref: {} }]) {
    const denied = await ceoHarness({ company, state: "PARTIAL", items: [bad], workspace_count: 0 });
    await denied.load();
    assert.equal(denied.view().status, "error", JSON.stringify(bad));
    assert.doesNotThrow(() => denied.render());
  }
});

test("normal Business entry no longer routes new Workspace to legacy Studio", () => {
  const page = readFileSync(new URL("../app/ceo-office/business/page.js", import.meta.url), "utf8");
  assert.doesNotMatch(page, /href=\{`\/ceo-office\/workspace\/studio/);
  assert.match(page, /首个工作空间随业务建立/);
  for (const file of ["content_growth_v02", "music"]) {
    const release = JSON.parse(readFileSync(new URL(`../../backend/app/bundled_workspace_packages/${file}_release.json`, import.meta.url), "utf8"));
    assert.equal(release.published, true); assert.equal(release.publicRelease, false); assert.equal(release.providerFeeGrant, false);
    assert.equal(release.decision.scope, "LOCAL_BETA_DEFINITION_ONLY");
  }
});


test("long names and many workspaces retain every exact target and readable workspace label without package versions", () => {
  const rows = BUSINESS_DIRECTIONS.map((direction, index) => ({
    business_id: `long-business-${index}`, company_id: "A", name: "连续经营业务名称".repeat(24),
    workspaces: Array.from({ length: 8 }, (_, n) => ({ workspace_id: `exact-${index}/${n}`,
      name: `具体工作空间${n}-` + "UnbrokenWorkspaceName".repeat(12), business_type: "PACKAGE",
      package_id: direction.packageId, package_version: "internal-version-do-not-display" })),
  }));
  const before = JSON.stringify(rows);
  const html = renderToStaticMarkup(React.createElement(Catalog, { ...props, businesses: rows }));
  assert.ok(html.includes("内容增长 · 写作 · 音乐"));
  assert.equal(html.includes("internal-version-do-not-display"), false);
  for (const [i, direction] of BUSINESS_DIRECTIONS.entries()) {
    const list = html.match(new RegExp(String.raw`<div class="directionWorkspaces" aria-label="${direction.name}已有工作空间">([\s\S]*?)<\/div>`))?.[1];
    assert.ok(list, direction.name);
    assert.equal((list.match(/<a /g) || []).length, 8);
    for (const workspace of rows[i].workspaces) {
      assert.ok(list.includes(`href="/ceo-office/workspace/installed/${encodeURIComponent(workspace.workspace_id)}"`));
      assert.ok(list.includes(`<span class="workspaceName">${workspace.name} →</span>`));
      assert.ok(list.includes(`title="${rows[i].name} · ${workspace.name}"`));
    }
  }
  assert.equal(JSON.stringify(rows), before, "presentation cannot rewrite identities, versions, or names");
});
