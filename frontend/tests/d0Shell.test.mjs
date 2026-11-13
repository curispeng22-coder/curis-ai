import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import vm from "node:vm";

const require = createRequire(import.meta.url);
const swc = require("next/dist/build/swc");
await swc.loadBindings();
async function load(path, overrides = {}, globals = {}) {
  const source = readFileSync(new URL("../" + path, import.meta.url), "utf8");
  const { code } = await swc.transform(source, { filename: path, isModule: true,
    jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } },
    module: { type: "commonjs" } });
  const loaded = { exports: {} };
  vm.runInNewContext(code, { module: loaded, exports: loaded.exports, URLSearchParams, require: (name) => overrides[name] || (name === "react" || name === "react/jsx-runtime" ? require(name) : {}), console, ...globals });
  return loaded.exports;
}

async function utilityEffectHarness(descriptors = [{ id: "A:one", title: "one", content: "real one" }, { id: "A:two", title: "two", content: "real two" }]) {
  const React = require("react"), states = [], refs = [], effects = [], layouts = [], storage = new Map();
  let stateIndex = 0, refIndex = 0;
  const source = readFileSync(new URL("../components/workspace/WorkspacePaneShell.js", import.meta.url), "utf8");
  const { code } = await swc.transform(source, { filename: "WorkspacePaneShell.js", isModule: true,
    jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } }, module: { type: "commonjs" } });
  const loaded = { exports: {} };
  const window = { sessionStorage: { getItem: (key) => storage.get(key) ?? null, setItem: (key, value) => storage.set(key, value) }, localStorage: { getItem: () => null }, requestAnimationFrame: (fn) => fn() };
  vm.runInNewContext(code, { module: loaded, exports: loaded.exports, window, console, require: (name) => {
    if (name === "react") return { ...React, useId: () => "test", useState: (initial) => {
      const key = stateIndex++; if (!(key in states)) states[key] = initial;
      return [states[key], (next) => { states[key] = typeof next === "function" ? next(states[key]) : next; }];
    }, useRef: (initial) => { const key = refIndex++; return refs[key] ||= { current: initial }; }, useLayoutEffect: (effect) => layouts.push(effect), useEffect: (effect) => effects.push(effect) };
    if (name === "react/jsx-runtime") return require(name);
    if (name === "next/navigation") return { usePathname: () => "/ceo-office/business" };
    if (name.endsWith("RuntimeProvider.js")) return { useRuntime: () => ({ companyId: "A" }) };
    return {};
  } });
  const scope = loaded.exports.paneScopeKey("A", "directory", "business");
  const render = (key, target) => {
    stateIndex = 0; refIndex = 0; effects.length = 0; layouts.length = 0;
    const tree = loaded.exports.default({ workspaceId: "directory", surfaceId: "business", utilityAvailable: true,
      utilityTabs: descriptors, utilityRequestKey: key, utilityRequestTabId: target });
    while (layouts.length) layouts.shift()();
    effects.find((effect) => effect.toString().includes("requestSeen.current"))();
    return tree;
  };
  function find(node, label) {
    if (!node) return null;
    if (Array.isArray(node)) return node.map((item) => find(item, label)).find(Boolean);
    if (node.props?.label === label || node.props?.["aria-label"] === label || node.props?.role === "tab" && node.props.children === label) return node;
    return find(node.props?.children, label);
  }
  return { render, saved: () => JSON.parse(storage.get(scope)), close: (tree) => find(tree, "收起详情").props.onClick(), click: (tree, label) => find(tree, label).props.onClick(), tabs: () => JSON.parse(storage.get(scope + ".tabs") || "null"), scroll: (tree, strip) => { find(tree, "已打开的辅助内容").props.ref.current = strip; effects.find((effect) => effect.toString().includes("tabListRef.current"))(); } };
}

async function catalogEventHarness() {
  const React = require("react"), states = [], pending = [], effectDeps = [];
  let stateIndex = 0, effectIndex = 0;
  const component = await load("components/v1/BusinessCatalogSurface.js", {
    react: { ...React, useState: (initial) => {
      const key = stateIndex++; if (!(key in states)) states[key] = initial;
      return [states[key], (next) => { states[key] = typeof next === "function" ? next(states[key]) : next; }];
    }, useMemo: (fn) => fn(), useEffect: (effect, deps) => {
      const key = effectIndex++; if (!effectDeps[key] || deps.some((v, i) => v !== effectDeps[key][i])) { effectDeps[key] = deps; pending.push(effect); }
    } },
  });
  const render = (selection) => {
    stateIndex = 0; effectIndex = 0;
    return component.BusinessCatalogPaneContent({ company: { company_id: "A", name: "Actual A" }, businesses: [], organization: null, definitions: null, definitionStatus: "loading", selection }).props;
  };
  function link(node, name) {
    if (!node) return null;
    if (Array.isArray(node)) return node.map((v) => link(v, name)).find(Boolean);
    if (node.props?.href && node.props.children === name) return node;
    return link(node.props?.children, name);
  }
  return { render, flush: () => { for (const effect of pending.splice(0)) effect(); }, link, id: component.businessPaneId };
}
const shell = await load("components/workspace/WorkspacePaneShell.js");
const recent = await load("components/v1/ConversationQuickAccess.js");
const assistant = await load("components/assistant/GlobalAssistant.js");
const terra = await load("components/terra/TerraShell.js");

test("UI pane scopes distinguish Company, workspace and Surface including ambiguous punctuation", () => {
  assert.notEqual(shell.paneScopeKey("A", "one", "reading"), shell.paneScopeKey("B", "one", "reading"));
  assert.notEqual(shell.paneScopeKey("A", "one", "reading"), shell.paneScopeKey("A", "one", "working"));
  assert.notEqual(shell.paneScopeKey("a:b", "c", "d"), shell.paneScopeKey("a", "b:c", "d"));
});
test("consumer four-pane initial preference applies only without saved fold choices", () => {
  const first = shell.initialPanePreferences(null, { context: true, utility: true }, { contextWidth: 234, utilityWidth: 320 });
  assert.equal(first.context, true); assert.equal(first.utility, true);
  assert.equal(first.contextWidth, 234); assert.equal(first.utilityWidth, 320);
  const saved = shell.initialPanePreferences({ context: false, utility: false, contextWidth: 210, utilityWidth: 340 }, { context: true, utility: true });
  assert.equal(saved.context, false); assert.equal(saved.utility, false);
  const existing = shell.initialPanePreferences(null); assert.equal(existing.context, false); assert.equal(existing.utility, false);
});
test("actual utility request effect preserves user fold on clear target and rerender, opens only new legal request", async () => {
  const host = await utilityEffectHarness();
  host.render(1, "A:one");
  const opened = host.render(1, "A:one"); host.close(opened);
  assert.equal(host.saved().utility, false);
  host.render(1, ""); assert.equal(host.saved().utility, false, "return to directory must not create a new open request");
  host.render(1, "A:two"); assert.equal(host.saved().utility, false, "target change without new serial must not reopen");
  host.render(2, "A:two"); assert.equal(host.saved().utility, true);
  assert.equal(host.tabs().active, "A:two"); assert.equal(host.tabs().ids.filter((id) => id === "A:two").length, 1);
  host.render(3, "foreign"); assert.equal(host.tabs().active, "A:two");
});
test("real same-URL catalog click reopens closed Music and focuses it without rerender or modifier requests", async () => {
  const consumer = await catalogEventHarness(), music = { kind: "definition", definitionId: "music" };
  consumer.render(music); consumer.flush();
  let data = consumer.render(music);
  const writingId = consumer.id("A", "definition", "writing"), musicId = consumer.id("A", "definition", "music");
  const host = await utilityEffectHarness([{ id: writingId, title: "Writing", content: "actual writing" }, { id: musicId, title: "Music", content: "actual music" }]);
  host.render(data.utilityRequestKey, data.utilityRequestTabId);
  let tree = host.render(data.utilityRequestKey, data.utilityRequestTabId);
  host.click(tree, "Writing"); tree = host.render(data.utilityRequestKey, data.utilityRequestTabId);
  host.click(tree, "关闭标签 · Music"); assert.equal(host.tabs().active, writingId);
  const event = { button: 0, defaultPrevented: false, metaKey: false, ctrlKey: false, shiftKey: false, altKey: false };
  const callback = consumer.link(data.contextPane, "音乐").props.onClick;
  assert.equal(typeof callback, "function", "same URL actual Link needs explicit intent callback");
  callback(event); data = consumer.render(music); host.render(data.utilityRequestKey, data.utilityRequestTabId);
  assert.equal(host.tabs().active, musicId); assert.equal(host.tabs().ids.filter((id) => id === musicId).length, 1);
  callback(event); data = consumer.render(music); host.render(data.utilityRequestKey, data.utilityRequestTabId);
  assert.equal(host.tabs().ids.filter((id) => id === musicId).length, 1);
  tree = host.render(data.utilityRequestKey, data.utilityRequestTabId); host.close(tree);
  const key = data.utilityRequestKey;
  for (const extra of [{ button: 1 }, { metaKey: true }, { ctrlKey: true }, { shiftKey: true }, { altKey: true }, { defaultPrevented: true }]) callback({ ...event, ...extra });
  data = consumer.render(music); host.render(data.utilityRequestKey, data.utilityRequestTabId);
  assert.equal(data.utilityRequestKey, key); assert.equal(host.saved().utility, false);
  consumer.link(data.contextPane, "写作").props.onClick(event);
  assert.equal(consumer.render(music).utilityRequestKey, key, "different href click must wait for original route effect");
  const writing = { kind: "definition", definitionId: "writing" };
  consumer.render(writing); consumer.flush(); data = consumer.render(writing);
  assert.equal(data.utilityRequestKey, key + 1, "different target route effect emits only once");
  host.render(data.utilityRequestKey, data.utilityRequestTabId); assert.equal(host.tabs().active, writingId);
  host.close(host.render(data.utilityRequestKey, data.utilityRequestTabId));
  assert.ok(!consumer.link(data.contextPane, "foreign"));
  const directory = consumer.render({ kind: "directory" }); consumer.flush(); host.render(directory.utilityRequestKey, directory.utilityRequestTabId);
  assert.equal(directory.utilityRequestKey, 0); assert.equal(host.saved().utility, false);
});
test("existing Terra bridge recognizes real tab descriptors without requiring compatibility body", () => {
  const content = { contextPane: {}, utilityTabs: [{ id: "company-A", content: {} }] };
  assert.equal(terra.terraPaneAvailability(content).context, true);
  assert.equal(terra.terraPaneAvailability(content).utility, true);
  assert.equal(terra.terraPaneAvailability({ utilityTabs: [] }).utility, false);
  assert.equal(terra.terraPaneAvailability({}).context, false);
});
test("CEO zero-business consumer supplies scoped navigation and actual facts to one shared host", async () => {
  const React = require("react"), { renderToStaticMarkup } = require("react-dom/server");
  let registered;
  const ceo = await load("components/v1/CeoDeskOperating.js", {
    "next/link": { __esModule: true, default: (props) => React.createElement("a", props) },
    "../terra/TerraShell.js": { TerraPaneContent: (props) => { registered = props; return React.createElement("section", null, props.contextPane); } },
  });
  const html = renderToStaticMarkup(React.createElement(ceo.CeoDeskPaneContent, { company: { company_id: "A", name: "真实公司A" }, snapshot: { workspaces: [] }, view: { businesses: [], attention: { items: [] }, conversation: { assistant: { name: "实际助理" } } }, selectedResult: null, requestKey: 0 }));
  assert.ok(html.includes("还没有经营中的业务")); assert.ok(html.includes("company_id=A"));
  assert.equal(registered.initialContextOpen, true); assert.equal(registered.initialUtilityOpen, true);
  assert.equal(registered.utilityTabs.length, 1); assert.ok(registered.utilityTabs[0].id.includes('"A"'));
  assert.notEqual(ceo.ceoResultTabId("A", { workspaceId: "w", referenceId: "r" }), ceo.ceoResultTabId("B", { workspaceId: "w", referenceId: "r" }));
});
test("D1 normal home branch supplies actual home panes while preserving work directory logic", () => {
  const source = readFileSync(new URL("../components/delivery/d1/D1Surface.js", import.meta.url), "utf8");
  assert.match(source, /home\.companyId === companyId && home\.businessesKnown/);
  assert.match(source, /contextPane=\{homeDirectory \|\| directory\}/);
  assert.match(source, /utilityTabs=\{homeTabs\}/);
  assert.match(source, /initialContextOpen=\{Boolean\(homeCompany\)\}/);
  assert.match(source, /const hasWorkDirectory = \["work", "result"\]/);
});
test("stale or corrupted pane widths are bounded without opening unavailable panels", () => {
  const p = shell.sanitizePanePreferences({ context: "yes", utility: true, contextWidth: -99, utilityWidth: Infinity });
  assert.equal(p.context, false); assert.equal(p.utility, true); assert.equal(p.contextWidth, 170); assert.equal(p.utilityWidth, 340);
  assert.equal(shell.paneWidth("context", 999), 320); assert.equal(shell.paneWidth("utility", 999), 480);
});
test("adaptive desktop preserves Main; narrow or extreme combinations overlay the latest auxiliary", () => {
  assert.equal(shell.paneGeometry(1440, true, true, true, 210, 340, "utility").overlay, null);
  const narrow = shell.paneGeometry(1024, true, true, true, 210, 340, "utility");
  assert.equal(narrow.navWidth, 158); assert.equal(narrow.overlay, "utility"); assert.equal(narrow.suppress, null);
  const extreme = shell.paneGeometry(1024, true, true, true, 320, 480, "context");
  assert.equal(extreme.overlay, "context"); assert.equal(extreme.suppress, "utility");
  assert.equal(shell.paneGeometry(1440, true, false, false, 210, 340, "utility").overlay, null);
});
test("recent top3 and expanded use canonical activity order without mutating server rows", () => {
  const rows = [1, 4, 2, 3].map((n) => ({ conversation_id: "topic-" + n, activity_at: "2026-10-04T0" + n + ":00:00Z" }));
  assert.equal(recent.recentRows(rows, false).map((x) => x.conversation_id).join(","), "topic-4,topic-3,topic-2");
  assert.equal(recent.recentRows(rows, true).length, 4);
  assert.equal(rows[0].conversation_id, "topic-1");
});
test("floating Assistant dragged beyond a resized viewport stays reachable", () => {
  const p = assistant.clampAssistantPosition({ left: 1300, top: 800 }, 390, 455, 1024, 700);
  assert.equal(p.left, 626); assert.equal(p.top, 237);
  const smaller = assistant.clampAssistantPosition({ left: -20, top: -1 }, 390, 455, 300, 350);
  assert.equal(smaller.left, 8); assert.equal(smaller.top, 8);
});
test("visual-first shell keeps one Main landmark, seven navigation routes and reference-sized labels", () => {
  const read = (path) => readFileSync(new URL("../" + path, import.meta.url), "utf8");
  const layout = read("components/workspace/WorkspacePaneShell.js");
  const sidebar = read("components/v1/V1Sidebar.js");
  const css = read("components/workspace/WorkspacePaneShell.module.css");
  assert.match(layout, /href="#curis-main"/);
  assert.match(layout, /<main id="curis-main" hidden=\{maximized\} tabIndex=\{-1\}/);
  assert.match(sidebar, /className=\{styles.sidebarBrand\}>Curis/);
  assert.match(sidebar, /className=\{styles.primaryNav\}/);
  assert.match(css, /\.navLink\{[^}]*font-size:14px/);
  assert.match(css, /\.header\{[^}]*height:48px/);
  assert.equal((sidebar.match(/\["(?:CEO 工作台|业务空间|组织中心|人才与能力|经营洞察|资料库|会议)"/g) || []).length, 7);
});
test("panel frames and controls remain distinct without forcing empty columns", () => {
  const css = readFileSync(new URL("../components/workspace/WorkspacePaneShell.module.css", import.meta.url), "utf8");
  const source = readFileSync(new URL("../components/workspace/WorkspacePaneShell.js", import.meta.url), "utf8");
  assert.match(css, /\.main\{[^}]*margin:0;[^}]*border:0;[^}]*border-radius:0/);
  assert.match(css, /\.pane\{[^}]*height:100%;[^}]*border-right:1px[^}]*border-radius:0;[^}]*margin:0/);
  assert.match(source, /title=\{label\} aria-label=\{label\}/);
  assert.match(source, /contextAvailable && contextPane && \(!contextOpen \|\| geometry.suppress === "context"\)/);
  assert.match(source, /utilityAvailable && tabs.length > 0 && \(!utilityOpen \|\| geometry.suppress === "utility"\)/);
  assert.match(source, /<PanelControl side="right" label=\{"收起" \+ utilityLabel\}/);
  assert.equal(shell.paneGeometry(1360, true, true, true, 210, 340, "utility").overlay, null);
});
test("fold controls align and stable tracks animate with resize and reduced-motion exceptions", () => {
  const css = readFileSync(new URL("../components/workspace/WorkspacePaneShell.module.css", import.meta.url), "utf8");
  const source = readFileSync(new URL("../components/workspace/WorkspacePaneShell.js", import.meta.url), "utf8");
  assert.match(css, /\.navigation>\.header\{margin-top:1px/);
  assert.match(css, /transition:grid-template-columns 200ms cubic-bezier/);
  assert.match(css, /\.main\{grid-column:3;grid-row:1\}/);
  assert.match(css, /\.utility\{grid-column:4\}/);
  assert.match(css, /prefers-reduced-motion:reduce\)\{\.shell\{transition:none\}/);
  assert.match(css, /resizer:active/);
  assert.match(source, /event\.preventDefault\(\); event\.currentTarget\.focus\(\); drag\.current/);
  assert.match(source, /"0px"\]\.join\(" "\)/);
});
test("Utility UI tabs deduplicate open, preserve siblings on close and reject unknown references", () => {
  const ids = ["responsibility", "version:one"];
  let value = shell.utilityTabState({ ids: [ids[0]], active: ids[0] }, { type: "open", id: ids[1] }, ids);
  assert.equal(value.ids.join(","), ids.join(",")); assert.equal(value.active, ids[1]);
  value = shell.utilityTabState(value, { type: "open", id: ids[1] }, ids); assert.equal(value.ids.length, 2);
  value = shell.utilityTabState(value, { type: "close", id: ids[1] }, ids); assert.equal(value.active, ids[0]);
  value = shell.utilityTabState(value, { type: "open", id: "other-company" }, ids); assert.equal(value.ids.length, 1);
  value = shell.utilityTabState(value, { type: "read" }, []); assert.equal(value.ids.length, 0);
});
test("plus creates distinct blank UI tabs; choosing content replaces only the selected blank", () => {
  const available = ["responsibility", "version:one"];
  let value = { ids: [available[0]], active: available[0] };
  value = shell.utilityTabState(value, { type: "new", id: "new:10-1" }, available);
  value = shell.utilityTabState(value, { type: "new", id: "new:10-2" }, available);
  assert.equal(value.ids.join(","), "responsibility,new:10-1,new:10-2");
  assert.equal(value.active, "new:10-2");
  value = shell.utilityTabState(value, { type: "select", id: "version:one" }, available);
  assert.equal(value.ids.join(","), "responsibility,new:10-1,version:one");
  value = shell.utilityTabState(value, { type: "open", id: "new:10-1" }, available);
  assert.equal(value.active, "new:10-1");
  const before = JSON.stringify(value);
  value = shell.utilityTabState(value, { type: "select", id: "other-company" }, available);
  assert.equal(JSON.stringify(value), before);
  value = shell.utilityTabState(value, { type: "select", id: "responsibility" }, available);
  assert.equal(value.ids.join(","), "responsibility,version:one");
  assert.equal(value.active, "responsibility");
});
test("directory has no visible title and tab expansion reuses inline layout without modal", () => {
  const source = readFileSync(new URL("../components/workspace/WorkspacePaneShell.js", import.meta.url), "utf8");
  const css = readFileSync(new URL("../components/workspace/WorkspacePaneShell.module.css", import.meta.url), "utf8");
  assert.doesNotMatch(source, /<h2[^>]*>\{contextLabel\}/);
  assert.doesNotMatch(source, /showModal|utilityDialog|<dialog/);
  assert.match(source, /<main id="curis-main" hidden=\{maximized\}/);
  assert.match(source, /aria-label="新建标签页"/);
  assert.match(source, /maximized \? "0px" : "minmax\(0, 1fr\)"/);
  assert.match(css, /\.expandedUtility\{border-left:0\}/);
  assert.doesNotMatch(css, /\.maximized\{|\.maximized::backdrop/);
});

test("active utility tabs scroll only their horizontal strip across selection and close", async () => {
  const h = await utilityEffectHarness();
  h.render(1, "A:two");
  let tree = h.render(1, "A:two");
  let item = { left: 340, right: 440, width: 100 };
  const strip = { scrollLeft: 0, scrollTop: 19, clientLeft: 1, clientWidth: 200,
    scrollIntoView: () => assert.fail("ancestor scrolling is forbidden"),
    focus: () => assert.fail("focus stealing is forbidden"),
    getBoundingClientRect: () => ({ left: 99 }),
    querySelector: (selector) => {
      assert.equal(selector, '[role="tab"][aria-selected="true"]');
      return { parentElement: { getBoundingClientRect: () => item } };
    } };
  h.scroll(tree, strip);
  assert.equal(strip.scrollLeft, 140);
  h.click(tree, "one");
  tree = h.render(1, "A:two");
  assert.equal(h.tabs().active, "A:one");
  item = { left: 20, right: 120, width: 100 };
  h.scroll(tree, strip);
  assert.equal(strip.scrollLeft, 60);
  item = { left: 120, right: 220, width: 100 };
  h.scroll(tree, strip);
  assert.equal(strip.scrollLeft, 60, "visible tab does not move");
  h.click(tree, "关闭标签 · one");
  tree = h.render(1, "A:two");
  assert.equal(h.tabs().active, "A:two");
  item = { left: 110, right: 360, width: 250 };
  h.scroll(tree, strip);
  assert.equal(strip.scrollLeft, 70, "oversized label aligns its beginning");
  strip.clientWidth = 0;
  h.scroll(tree, strip);
  assert.equal(strip.scrollLeft, 70, "hidden strip does not scroll");
  strip.clientWidth = 200; strip.querySelector = () => null;
  h.scroll(tree, strip);
  assert.equal(strip.scrollLeft, 70, "missing active element does not scroll");
  assert.equal(strip.scrollTop, 19);
  assert.equal(readFileSync(new URL("../components/workspace/WorkspacePaneShell.js", import.meta.url), "utf8").includes("scrollIntoView("), false);
});

test("three current consumers register real Context and only scoped Utility content", async () => {
  const React = require("react");
  const hooks = { ...React, useState: (initial) => [initial, () => {}], useMemo: (fn) => fn(),
    useCallback: (fn) => fn, useEffect: () => {}, useRef: (initial) => ({ current: initial }) };
  const findPane = (node) => {
    if (!node) return null;
    if (Array.isArray(node)) return node.map(findPane).find(Boolean);
    if (node.props?.contextPane !== undefined && node.props?.utilityLabel) return node.props;
    return findPane(node.props?.children);
  };
  const organization = await load("app/ceo-office/organization/OrganizationCenter.js", { react: hooks });
  const business = { id: "business-1", name: "实际业务", departmentId: "department-1", roleCount: 1,
    staffingCount: 1, workspaceCount: 0, workspaces: [], assignments: [], status: "经营中" };
  const department = { id: "department-1", name: "实际部门", businessCount: 1, employeeCount: 1,
    businesses: [business], description: "已记录职责" };
  const employee = { id: "employee-1", name: "实际员工", role: "analyst", status: "进行中", assignments: [], departmentName: department.name, departmentId: department.id };
  const projection = { company: { id: "A", name: "实际公司" }, departments: [department],
    businesses: [business], businessById: new Map([[business.id, business]]), employees: [employee],
    totals: { departments: 1, businesses: 1, employees: 1, vacancies: 0 } };
  const map = findPane(organization.OrganizationReady({ projection, tab: "map", selectedBusinessId: "", selectedDepartmentId: "" }));
  assert.equal(map.initialContextOpen, true);
  assert.equal(map.initialUtilityOpen, true);
  assert.equal(map.utilityTabs.map((item) => item.title).join(","), "当前公司");
  const selected = findPane(organization.OrganizationReady({ projection, tab: "map", selectedBusinessId: business.id, selectedDepartmentId: "" }));
  assert.equal(selected.utilityTabs[1].title, business.name);
  assert.equal(selected.utilityRequestTabId, JSON.stringify(["A", "business", business.id]));
  const departmentPane = findPane(organization.OrganizationReady({ projection, tab: "map", selectedBusinessId: "", selectedDepartmentId: department.id }));
  assert.equal(departmentPane.utilityTabs[1].title, department.name);
  assert.equal(departmentPane.utilityRequestTabId, JSON.stringify(["A", "department", department.id]));
  const directoryPane = findPane(organization.OrganizationReady({ projection, tab: "employees", selectedBusinessId: "", selectedDepartmentId: "" }));
  assert.equal(directoryPane.utilityTabs.map((item) => item.title).join(","), "当前公司");
  assert.equal(directoryPane.utilityRequestTabId, "");
  const employeeOrganization = await load("app/ceo-office/organization/OrganizationCenter.js", { react: {
    ...hooks, useState: (() => { let index = 0; return (initial) => [index++ === 1 ? employee.id : initial, () => {}]; })(),
  } });
  const employeePane = findPane(employeeOrganization.OrganizationReady({ projection, tab: "employees", selectedBusinessId: "", selectedDepartmentId: "" }));
  assert.equal(employeePane.utilityTabs[1].title, employee.name);
  assert.equal(employeePane.utilityRequestTabId, JSON.stringify(["A", "employee", employee.id]));
  assert.equal(findPane(organization.OrganizationReady({ projection, tab: "map", selectedBusinessId: "other-company", selectedDepartmentId: "" })).utilityTabs.length, 1);
  const unresolved = { ...business, id: "unresolved", departmentId: "unknown" };
  const withUnresolved = { ...projection, businessById: new Map([[business.id, business], [unresolved.id, unresolved]]) };
  assert.equal(findPane(organization.OrganizationReady({ projection: withUnresolved, tab: "map", selectedBusinessId: unresolved.id, selectedDepartmentId: "" })).utilityTabs.length, 1);
  const talent = await load("app/ceo-office/talent-market/page.js", { react: {
    ...hooks, useState: (() => { let index = 0; return (initial) => [index++ === 0
      ? { experts: [], skills: [], connectors: [], companyEmployees: [], employees: [],
        companies: [], departments: [], expertCategories: [] } : initial, () => {}]; })(),
  } });
  const talentPane = findPane(talent.TalentMarketSurface({ companyId: "A" }));
  assert.equal(talentPane.initialContextOpen, true);
  assert.equal(talentPane.utilityPane, null, "no selected expert means no invented Inspector");
  assert.equal(talent.resourceTitle({ source: "official", role: "finance_analyst", name: "finance_analyst" }), "财务分析专家");
  assert.equal(talent.resourceTitle({ source: "official", role: "finance_analyst", name: "Finance Financial Analyst" }), "财务分析专家");
  assert.equal(talent.resourceTitle({ source: "official", role: "finance_analyst", display_name: "Alex", name: "Finance Financial Analyst" }), "Alex");
  assert.equal(talent.resourceTitle({ source: "marketplace", role: "finance_analyst", name: "Finance Financial Analyst" }), "Finance Financial Analyst");
  assert.equal(talent.resourceTitle({ role: "unknown_role", name: "Named candidate" }), "Named candidate");
  const expert = { id: "official.employee.finance_analyst", source: "official", role: "finance_analyst", name: "Finance Financial Analyst" };
  const selectedTalent = await load("app/ceo-office/talent-market/page.js", { react: {
    ...hooks, useState: (() => { let index = 0; return (initial) => {
      const value = index === 0 ? { experts: [expert], skills: [], connectors: [], companyEmployees: [], employees: [], companies: [], departments: [], expertCategories: [] }
        : index === 5 ? { kind: "experts", item: expert } : initial;
      index += 1; return [value, () => {}];
    }; })(),
  } });
  assert.ok(findPane(selectedTalent.TalentMarketSurface({ companyId: "A" })).utilityPane, "selected real expert registers Inspector");
  const insights = await load("app/ceo-office/analytics/OperatingIntelligence.js", { react: hooks });
  const insightPane = findPane(insights.InsightsSurface({ companyId: "A" }));
  assert.equal(insightPane.initialContextOpen, true);
  assert.equal(insightPane.utilityPane, null, "no selected metric means no invented source");
  const selectedInsights = await load("app/ceo-office/analytics/OperatingIntelligence.js", { react: {
    ...hooks, useState: (() => { let index = 0; return (initial) => {
      const value = index === 3 ? { key: JSON.stringify(["A", "", 30]), data: { reports: [], scopes: [] } }
        : index === 4 ? { label: "实际指标", kind: "metric" } : initial;
      index += 1; return [value, () => {}];
    }; })(),
  } });
  assert.ok(findPane(selectedInsights.InsightsSurface({ companyId: "A" })).utilityPane, "selected real metric registers its source");
});

test("visible production-line candidate gets a source-bound ordinary name without changing maturity", async () => {
  const candidate = { id: "resource:agent:finance-financial-analyst:0123456789ab", resource_type: "agent", role: "finance_analyst",
    name: "Finance Financial Analyst", source: "external", market_kind: "external_candidate",
    source_url: "https://github.com/jnMetaCode/agency-agents-zh",
    source_path: "finance/finance-financial-analyst.md", source_verified: false,
    maturity: "CANDIDATE", recruitable: false };
  const api = { getEmployeeTemplates: async () => ({ employee_templates: [] }),
    workspaceFetch: async (path) => path.includes("production-line") ? { resources: [candidate] }
      : path.includes("skills") ? { skills: [] } : { connectors: [] },
    getCompanies: async () => ({ companies: [] }), getDepartments: async () => ({ departments: [] }),
    getEmployees: async () => ({ employees: [] }) };
  const market = await load("lib/talentMarket.js", { "./api.js": api });
  const page = await load("app/ceo-office/talent-market/page.js");
  const data = await market.getTalentMarketData();
  assert.equal(data.experts.length, 1, "the production-line row reaches the visible catalog");
  const visible = data.experts[0];
  assert.equal(page.resourceTitle(visible), "财务分析专家");
  assert.equal(visible.source, "external");
  assert.equal(visible.market_kind, "external_candidate");
  assert.equal(market.productStateFor(visible, "experts"), "正在准备");
  assert.equal(page.resourceTitle({ ...visible, source_path: "other-source.md" }), visible.name);
  assert.equal(page.resourceTitle({ ...visible, display_name: "Chosen display name" }), "Chosen display name");
});


async function searchConsumerHarness() {
  const React = require("react"), states = [], refs = [], deps = [], cleanups = [], pending = [], layouts = [], timers = new Map(), listeners = new Map(), requests = [], focus = [];
  let companyId = "", stateIndex = 0, refIndex = 0, effectIndex = 0, timerId = 0;
  const window = { location: { href: "" }, sessionStorage: { getItem: () => null, setItem() {} }, localStorage: { getItem: () => null },
    requestAnimationFrame: (fn) => fn(), setTimeout: (fn) => { const id = ++timerId; timers.set(id, fn); return id; }, clearTimeout: (id) => timers.delete(id),
    addEventListener: (name, fn) => listeners.set(name, fn), removeEventListener: (name, fn) => { if (listeners.get(name) === fn) listeners.delete(name); } };
  const scheduleEffect = (queue, fn, next) => { const i = effectIndex++; if (!deps[i] || next.some((v, j) => v !== deps[i][j])) queue.push(() => { cleanups[i]?.(); cleanups[i] = fn(); deps[i] = next; }); };
  const loaded = await load("components/workspace/WorkspacePaneShell.js", {
    react: { ...React, useId: () => "search-test", useState: (initial) => { const i = stateIndex++; if (!(i in states)) states[i] = initial; return [states[i], (next) => { states[i] = typeof next === "function" ? next(states[i]) : next; }]; },
      useRef: (initial) => { const i = refIndex++; return refs[i] ||= { current: initial }; }, useLayoutEffect: (fn, next) => scheduleEffect(layouts, fn, next), useEffect: (fn, next) => scheduleEffect(pending, fn, next) },
    "next/navigation": { usePathname: () => "/ceo-office" }, "../runtime/RuntimeProvider.js": { useRuntime: () => ({ companyId }) },
    "../../lib/v1FrontendApi.js": { searchCompanyObjects: (id, query) => new Promise((resolve, reject) => requests.push({ id, query, resolve, reject })) },
    "../../lib/objectSearchState.mjs": { groupMeta: () => ({ label: "资料", icon: "i-home" }), objectHref: (item) => "/ceo-office/knowledge?entry=" + item.id },
  }, { window, ResizeObserver: class { observe() {} disconnect() {} } });
  function nodes(node, predicate) { if (!node || typeof node !== "object") return []; if (Array.isArray(node)) return node.flatMap((v) => nodes(v, predicate)); return [...(predicate(node) ? [node] : []), ...nodes(node.props?.children, predicate), ...nodes(node.props?.brandActions, predicate)]; }
  const render = () => { stateIndex = 0; refIndex = 0; effectIndex = 0; layouts.length = 0; pending.length = 0; return loaded.default({ workspaceId: "surface:home", surfaceId: "/ceo-office" }); };
  const layoutCommit = (id = companyId) => { companyId = id; const tree = render();
    for (const node of nodes(tree, (n) => n.props?.ref || n.props?.buttonRef)) { const ref = node.props.ref || node.props.buttonRef; if (typeof ref === "object") ref.current = { focus: () => focus.push(node.props.label || node.props["aria-label"] || "main"), querySelector: () => null, querySelectorAll: () => [], clientWidth: 0 }; }
    while (layouts.length) layouts.shift()(); return tree; };
  const flushPassive = () => { while (pending.length) pending.shift()(); };
  const commit = (id = companyId) => { let tree; for (let i = 0; i < 3; i++) { tree = layoutCommit(id); flushPassive(); } return tree; };
  const abandon = (id) => { const committed = companyId; companyId = id; render(); layouts.length = 0; pending.length = 0; companyId = committed; };
  const find = (tree, label) => nodes(tree, (n) => n.props?.label === label || n.props?.["aria-label"] === label)[0];
  return { commit, layoutCommit, flushPassive, abandon, find, nodes, requests, focus, window, searchButton: (tree) => find(tree, "搜索公司对象"),
    open: (tree) => find(tree, "搜索公司对象").props.onClick(), type: (tree, value) => find(tree, "搜索关键词").props.onChange({ target: { value } }),
    nextTimer: () => [...timers.values()][0], fireTimers: () => { for (const [id, fn] of [...timers]) { timers.delete(id); fn(); } }, escape: () => listeners.get("keydown")?.({ key: "Escape" }),
    unmount: () => { cleanups.forEach((fn) => fn?.()); } };
}

test("no Company disables expanded and collapsed search including direct activation", async () => {
  const h = await searchConsumerHarness(); let tree = h.commit("");
  for (let i = 0; i < 2; i++) {
    const trigger = h.searchButton(tree), button = trigger.type(trigger.props);
    assert.equal(button.props.disabled, true); assert.match(button.props.title, /建立公司后/); trigger.props.onClick(); tree = h.commit();
    assert.equal(h.nodes(tree, (n) => n.props?.role === "dialog").length, 0); h.fireTimers(); assert.equal(h.requests.length, 0);
    if (!i) { h.find(tree, "收起导航").props.onClick(); tree = h.commit(); }
  }
  h.unmount();
});
test("Company loss cancels queued search, rejects late responses and stale keyboard selection", async () => {
  const h = await searchConsumerHarness(); let tree = h.commit("A"); h.open(tree); tree = h.commit(); h.type(tree, "old query"); tree = h.commit();
  const queued = h.nextTimer(), oldKey = h.find(tree, "搜索关键词").props.onKeyDown; assert.equal(typeof queued, "function");
  tree = h.commit(""); queued(); assert.equal(h.requests.length, 0); oldKey({ key: "Enter", preventDefault() {} }); assert.equal(h.window.location.href, "");
  tree = h.commit("A"); h.open(tree); tree = h.commit(); h.type(tree, "pending"); tree = h.commit(); h.fireTimers(); assert.equal(h.requests.length, 1);
  tree = h.commit(""); h.requests[0].resolve({ groups: [{ type: "knowledge", items: [{ id: "old", title: "old company result" }] }] }); await new Promise(setImmediate); tree = h.commit();
  assert.equal(h.nodes(tree, (n) => n.props?.role === "dialog").length, 0); tree = h.commit("B"); h.open(tree); tree = h.commit();
  assert.equal(h.find(tree, "搜索关键词").props.value, ""); assert.equal(h.nodes(tree, (n) => n.props?.role === "option").length, 0); assert.equal(h.requests.length, 1); h.unmount();
});
test("real Company search retains query, focus, Arrow/Enter selection and visible errors", async () => {
  const h = await searchConsumerHarness(); let tree = h.commit("A"); assert.equal(h.searchButton(tree).type(h.searchButton(tree).props).props.disabled, false);
  h.open(tree); tree = h.commit(); assert.ok(h.focus.includes("搜索关键词")); h.type(tree, "chapter"); tree = h.commit(); h.fireTimers();
  assert.equal(h.requests[0].id, "A"); assert.equal(h.requests[0].query, "chapter"); h.requests[0].resolve({ groups: [{ type: "knowledge", items: [{ id: "one", title: "One" }, { id: "two", title: "Two" }] }] }); await new Promise(setImmediate); tree = h.commit();
  h.find(tree, "搜索关键词").props.onKeyDown({ key: "ArrowDown", preventDefault() {} }); tree = h.commit(); h.find(tree, "搜索关键词").props.onKeyDown({ key: "Enter", preventDefault() {} }); tree = h.commit();
  assert.equal(h.window.location.href, "/ceo-office/knowledge?entry=two"); assert.ok(h.focus.includes("搜索公司对象")); assert.equal(h.nodes(tree, (n) => n.props?.role === "dialog").length, 0);
  h.open(tree); tree = h.commit(); h.type(tree, "retry"); tree = h.commit(); h.fireTimers(); h.requests[1].reject(Error("offline")); await new Promise(setImmediate); tree = h.commit();
  const text = (v) => v == null ? "" : typeof v === "object" ? (Array.isArray(v) ? v.map(text).join("") : text(v.props?.children)) : String(v);
  assert.match(text(tree), /搜索暂时不可用/); h.escape(); tree = h.commit(); assert.equal(h.nodes(tree, (n) => n.props?.role === "dialog").length, 0); h.unmount();
});


test("abandoned Company render cannot change the still-committed search callbacks", async () => {
  const h = await searchConsumerHarness(); let tree = h.commit("A"); h.open(tree); tree = h.commit(); h.type(tree, "committed A"); tree = h.commit();
  h.abandon("B"); h.fireTimers(); assert.equal(h.requests.length, 1); assert.equal(h.requests[0].id, "A");
  h.requests[0].resolve({ groups: [{ type: "knowledge", items: [{ id: "A-one", title: "A result" }] }] }); await new Promise(setImmediate); tree = h.commit();
  const key = h.find(tree, "搜索关键词").props.onKeyDown; h.abandon("B"); key({ key: "Enter", preventDefault() {} });
  assert.equal(h.window.location.href, "/ceo-office/knowledge?entry=A-one"); h.commit(); h.unmount();
});
test("layout commit fences old search and Enter before passive cleanup runs", async () => {
  const h = await searchConsumerHarness(); let tree = h.commit("A"); h.open(tree); tree = h.commit(); h.type(tree, "original"); tree = h.commit(); h.fireTimers();
  h.requests[0].resolve({ groups: [{ type: "knowledge", items: [{ id: "old", title: "old result" }] }] }); await new Promise(setImmediate); tree = h.commit();
  const oldKey = h.find(tree, "搜索关键词").props.onKeyDown, oldOption = h.nodes(tree, (n) => n.props?.role === "option")[0];
  h.type(tree, "queued"); tree = h.commit(); const queued = h.nextTimer(); assert.equal(typeof queued, "function");
  tree = h.layoutCommit(""); assert.equal(h.nodes(tree, (n) => n.props?.role === "dialog").length, 0);
  queued(); oldKey({ key: "Enter", preventDefault() {} }); oldOption.props.onClick(); assert.equal(h.requests.length, 1); assert.equal(h.window.location.href, "");
  h.flushPassive(); h.commit(""); h.unmount();
});
