import assert from "node:assert/strict";
import test from "node:test";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { d1Href, parseD1Entry, d1Reducer, initialD1State, validResultBridge, resultResponseKey, restoreResultResponse, resultReceiptMatches, saveResultResponse } from "../lib/d1State.mjs";
import * as computerAccess from "../lib/computerAccess.mjs";

test("Existing topic and Employee links retain identities without creating a Work", () => {
  const entry = parseD1Entry("?conversation_id=topic%3A1&employee_ref=employee%2F1", "conversation");
  assert.equal(entry.view, "conversation"); assert.equal(entry.conversationId, "topic:1"); assert.equal(entry.employeeRef, "employee/1"); assert.equal(entry.workRef, "");
});

test("Shared Composer optional adaptation preserves default consumer controls and editable input", async () => {
  const require = createRequire(import.meta.url);
  const React = require("react");
  const { renderToStaticMarkup } = require("react-dom/server");
  const { transform, loadBindings } = require("next/dist/build/swc");
  await loadBindings();
  const source = readFileSync(new URL("../components/v1/SharedConversation.js", import.meta.url), "utf8");
  const { code } = await transform(source, { filename: "SharedConversation.js", jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "classic" } } }, module: { type: "commonjs" } });
  const mod = { exports: {} };
  const localRequire = (name) => name === "react" ? React : name === "next/link" ? { default: (props) => React.createElement("a", props) } : name.endsWith("computerAccess.mjs") ? computerAccess : {};
  new Function("require", "module", "exports", "React", code)(localRequire, mod, mod.exports, React);
  const Composer = mod.exports.ConversationComposer;
  const baseline = renderToStaticMarkup(React.createElement(Composer, { value: "原内容", placeholder: "输入消息" }));
  assert.match(baseline, /语音/); assert.match(baseline, /参考资料未接入/); assert.match(baseline, /border-t border-ui-line p-3/);
  assert.match(baseline, /aria-label="输入消息"/);
  const adapted = renderToStaticMarkup(React.createElement(Composer, { value: "新草稿", busy: true, showVoice: false, className: "d1-composer", inputAriaLabel: "讨论消息", maxLength: 8000, controls: React.createElement("p", null, "权限尚未确认"), referenceControl: React.createElement("button", { type: "button", disabled: true }, "添加资料暂不可用") }));
  assert.doesNotMatch(adapted, /语音/); assert.match(adapted, /maxlength="8000"/i); assert.match(adapted, /权限尚未确认/); assert.match(adapted, /添加资料暂不可用/);
  const textarea = adapted.match(/<textarea[\s\S]*?<\/textarea>/)[0];
  assert.doesNotMatch(textarea, /disabled|readonly/); assert.match(textarea, /新草稿/); assert.match(adapted, /type="submit" disabled/);
});

test("Legacy Result query restores a read selection, never an explicit view action", () => {
  const entry = parseD1Entry("?result_workspace=w&result_ref=task%3A1");
  assert.equal(entry.view, "result"); assert.equal(entry.workspaceId, "w"); assert.equal(entry.resultRef, "task:1"); assert.equal(entry.explicit, false);
});

test("Utility bridge pins Company Work Result and version without arbitrary return URL", () => {
  const fixed = { view: "result", resultOrigin: "utility", originCompany: "A", workspaceId: "w", workRef: "work-a", resultRef: "task:t", resultVersion: "a".repeat(64) };
  const href = d1Href(fixed), restored = parseD1Entry(new URL(href, "https://local.invalid").search);
  assert.equal(restored.resultOrigin, "utility"); assert.equal(restored.resultVersion, fixed.resultVersion);
  const eligible = { tenant_id: "t", company_id: "A", workspace_id: "w", reference_id: "task:t", result_version: fixed.resultVersion, source_work_ref: "work-a", content: "真实结果正文" };
  assert.equal(validResultBridge(restored, "A", eligible), true);
  assert.equal(validResultBridge(restored, "B", eligible), false);
  assert.equal(validResultBridge(restored, "A", { ...eligible, result_version: "b".repeat(64) }), false);
  assert.equal(validResultBridge(restored, "A", { ...eligible, content: "" }), false);
  const context = ["A", "w", "task:t", fixed.resultVersion, "work-a", "ceo"];
  const saved = { context, at: 1000, action: "REVISE", reason: "请修改", request_id: "id" };
  assert.equal(restoreResultResponse(JSON.stringify(saved), context, 1001).reason, "请修改");
  assert.equal(restoreResultResponse(JSON.stringify(saved), [...context.slice(0, 5), "other"], 1001), null);
  assert.equal(restoreResultResponse(JSON.stringify(saved), context, 1000 + 31 * 60 * 1000), null);
  assert.notEqual(resultResponseKey("A", "w", { reference_id: "task:t", result_version: fixed.resultVersion, source_work_ref: "work-a" }, "ceo"), resultResponseKey("A", "w", { reference_id: "task:t", result_version: "b".repeat(64), source_work_ref: "work-a" }, "ceo"));
});

test("Route serialization keeps the original Work, topic and four-scope references", () => {
  const entry = { view: "result", resultRef: "task:r", workRef: "work:w", workspaceId: "w", employeeRef: "e", conversationId: "t", scopeType: "WORKSPACE", scopeRef: "w", explicit: true };
  const restored = parseD1Entry(new URL(d1Href(entry), "https://local.invalid").search);
  for (const key of ["workRef", "resultRef", "workspaceId", "conversationId", "employeeRef", "scopeType", "scopeRef"]) assert.equal(restored[key], entry[key]);
  assert.equal(restored.explicit, false);
});

test("Browser history restoration discards stale return stacks and explicit action intent", () => {
  let state = d1Reducer(initialD1State({ view: "work", workRef: "a" }), { type: "navigate", entry: { view: "result", resultRef: "r", explicit: true } });
  state = d1Reducer(state, { type: "restore", entry: parseD1Entry("?work_ref=b&workspace_id=w") });
  assert.equal(state.entry.workRef, "b"); assert.equal(state.returns.length, 0); assert.equal(state.entry.explicit, false);
});

test("Employee Utility renders current activities separately from role duties and confines Work highlighting to its entry Workspace", async () => {
  const require = createRequire(import.meta.url), React = require("react");
  const { renderToStaticMarkup } = require("react-dom/server"), { transform, loadBindings } = require("next/dist/build/swc");
  const helpers = await import("../lib/d1State.mjs");
  await loadBindings();
  const source = readFileSync(new URL("../components/delivery/d1/D1Surface.js", import.meta.url), "utf8");
  const { code } = await transform(source, { filename: "D1Surface.js", jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "classic" } } }, module: { type: "commonjs" } });
  const entry = { view: "work", workRef: "current", workspaceId: "w" };
  const employee = { employee_ref: "e", company_employee_ref: "company-e", responsibility: "长期岗位职责", organization_record: { name: "员工", role: "岗位" }, current_responsibilities: [{ object_ref: "current", object_type: "WORK", responsibility_holder_ref: "e", object_owner_ref: "e", activity: "责任已分配，尚未开始执行。" }] };
  let utility, captured, updates = [], reads = [], stateIndex;
  const hookReact = { ...React, useState: () => {
    const index = stateIndex++;
    return [[true, {}, { loading: false, value: { companyId: "c", workspaceId: "w", work_ref: "current" } }, 0, null, false, utility][index], (value) => { if (index === 6) updates.push(value); }];
  }, useReducer: () => [{ entry, returns: [] }, () => {}], useEffect: () => {}, useRef: () => ({ current: null }), useCallback: (fn) => fn };
  const styles = new Proxy({}, { get: (_, name) => name });
  const localRequire = (name) => {
    if (name === "react") return hookReact;
    if (name === "next/navigation") return { useSearchParams: () => new URLSearchParams() };
    if (name.endsWith("RuntimeProvider.js")) return { useRuntime: () => ({ companyId: "c", status: "ready", snapshot: {} }) };
    if (name.endsWith("d1State.mjs")) return helpers;
    if (name.endsWith("d1Api.js")) return { d1Api: { employeeDetail: async (...args) => { reads.push(args); return employee; } } };
    if (name.endsWith("theme.js")) return { roleLabel: (value) => value };
    if (name.endsWith(".css")) return { __esModule: true, default: styles };
    if (name.endsWith("WorkView.js")) return { __esModule: true, default: (props) => { captured = props; return null; } };
    // Business-body SSR fixture only; actual Shell controls are verified separately.
    if (name.endsWith("WorkspacePaneShell.js")) return { __esModule: true, default: (props) => React.createElement(React.Fragment, null, props.contextPane, props.children, props.utilityPane) };
    return { __esModule: true, default: () => null };
  };
  const mod = { exports: {} };
  new Function("require", "module", "exports", "React", code)(localRequire, mod, mod.exports, hookReact);
  const render = (value) => { utility = value; stateIndex = 0; return renderToStaticMarkup(mod.exports.default({})); };
  const markup = render({ employee, responsibilities: helpers.currentResponsibilities(employee, "current") });
  assert.match(markup, /当前查看的工作/); assert.match(markup, /责任已分配，尚未开始执行。/); assert.match(markup, /岗位职责<\/dt><dd>长期岗位职责/);
  for (const [current_responsibilities, text] of [[[], "当前工作空间暂无已记录的当前责任"], [undefined, "当前责任未记录"]]) {
    const value = { ...employee, current_responsibilities };
    assert.match(render({ employee: value, responsibilities: helpers.currentResponsibilities(value) }), new RegExp(text));
  }
  render(null);
  const oldDocument = globalThis.document;
  globalThis.document = { activeElement: null };
  try {
    await captured.onEmployeeDetail("e", "w");
    assert.equal(updates.at(-1).responsibilities.items[0].current, true);
    await captured.onEmployeeDetail("e", "other-w");
    assert.equal(updates.at(-1).responsibilities.items[0].current, false);
    assert.deepEqual(reads, [["c", "e", "w"], ["c", "e", "other-w"]]);
  } finally { if (oldDocument === undefined) delete globalThis.document; else globalThis.document = oldDocument; }
});

test("Next query restoration preserves internal Result intent and returns, but restores external destinations and popstate", async () => {
  const require = createRequire(import.meta.url), React = require("react");
  const { transform, loadBindings } = require("next/dist/build/swc");
  const helpers = await import("../lib/d1State.mjs");
  await loadBindings();
  const source = readFileSync(new URL("../components/delivery/d1/D1Surface.js", import.meta.url), "utf8");
  const { code } = await transform(source, { filename: "D1Surface.js", jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "classic" } } }, module: { type: "commonjs" } });
  let query = "?view=work&work_ref=work-a&workspace_id=w", state, stateIndex, refIndex, effectIndex;
  const values = [], refs = [], effects = [], pendingEffects = [], listeners = new Map(), actions = [];
  const hookReact = { ...React,
    useReducer: (_reducer, initial, initialize) => {
      state ??= initialize(initial);
      return [state, (action) => { actions.push(action); state = helpers.d1Reducer(state, action); }];
    },
    useState: (initial) => {
      const index = stateIndex++;
      if (!(index in values)) values[index] = index === 2 ? { loading: false, value: { companyId: "c", workspaceId: "w", work_ref: "work-a" } } : initial;
      return [values[index], (value) => { values[index] = typeof value === "function" ? value(values[index]) : value; }];
    },
    useRef: (initial) => { const index = refIndex++; refs[index] ??= { current: initial }; return refs[index]; },
    useCallback: (callback) => callback,
    useEffect: (callback, dependencies) => {
      const index = effectIndex++, previous = effects[index];
      // Execute the company-context and two real entry-adapter effects; business fetch effects are
      // outside this deterministic hook harness and verified in Browser.
      if (index < 3 && (!previous || dependencies.some((value, i) => !Object.is(value, previous.dependencies[i])))) pendingEffects.push(() => {
        previous?.cleanup?.(); effects[index] = { dependencies, cleanup: callback() };
      });
    },
  };
  const Work = () => null, Matter = () => null, Result = () => null, Shell = () => null;
  const localRequire = (name) => {
    if (name === "react") return hookReact;
    if (name === "next/navigation") return { useSearchParams: () => new URLSearchParams(query) };
    if (name.endsWith("RuntimeProvider.js")) return { useRuntime: () => ({ companyId: "c", status: "ready", snapshot: {} }) };
    if (name.endsWith("d1State.mjs")) return helpers;
    if (name.endsWith("d1Api.js")) return { d1Api: {} };
    if (name.endsWith(".css")) return { __esModule: true, default: new Proxy({}, { get: (_, key) => key }) };
    if (name.endsWith("WorkView.js")) return { __esModule: true, default: Work };
    if (name.endsWith("CeoMatterView.js")) return { __esModule: true, default: Matter };
    if (name.endsWith("ResultView.js")) return { __esModule: true, default: Result };
    if (name.endsWith("WorkspacePaneShell.js")) return { __esModule: true, default: Shell };
    return { __esModule: true, default: () => null };
  };
  const mod = { exports: {} };
  new Function("require", "module", "exports", "React", code)(localRequire, mod, mod.exports, hookReact);
  const priorWindow = globalThis.window;
  globalThis.window = { location: { pathname: "/ceo-office", search: query },
    history: {
      pushState: (_data, _title, href) => { window.location.search = new URL(href, "https://local.invalid").search; },
      replaceState: (_data, _title, href) => { window.location.search = new URL(href, "https://local.invalid").search; },
    },
    requestAnimationFrame: () => {}, // Real DOM focus is checked in Browser.
    addEventListener: (name, callback) => listeners.set(name, callback),
    removeEventListener: (name, callback) => { if (listeners.get(name) === callback) listeners.delete(name); },
  };
  const render = () => {
    stateIndex = refIndex = effectIndex = 0;
    const tree = mod.exports.default({});
    while (pendingEffects.length) pendingEffects.shift()();
    return tree;
  };
  const findWork = (node) => {
    if (!React.isValidElement(node)) return null;
    if (node.type === Work) return node;
    for (const child of React.Children.toArray(node.props.children)) { const found = findWork(child); if (found) return found; }
    return null;
  };
  const findResult = (node) => {
    if (!React.isValidElement(node)) return null;
    if (node.type === Result) return node;
    for (const child of React.Children.toArray(node.props.children)) { const found = findResult(child); if (found) return found; }
    return null;
  };
  try {
    render(); const tree = render();
    assert.equal(state.entry.workRef, "work-a"); assert.equal(state.entry.explicit, false);
    findWork(tree).props.onResult("task:r", "w");
    const restoresBeforeInternal = actions.filter((action) => action.type === "restore").length;
    render(); // Reducer may commit before Next's native-history query update.
    assert.equal(state.entry.explicit, true); assert.equal(state.returns.length, 1);
    assert.equal(findResult(render()).props.backLabel, "返回原对象");
    query = window.location.search; render();
    assert.equal(state.entry.resultRef, "task:r"); assert.equal(state.entry.explicit, true);
    assert.equal(state.returns[0].workRef, "work-a");
    assert.equal(actions.filter((action) => action.type === "restore").length, restoresBeforeInternal);
    findResult(render()).props.onWork("work-a", "w");
    query = window.location.search;
    const returnedWork = render();
    assert.equal(state.entry.view, "work"); assert.equal(state.entry.workRef, "work-a"); assert.equal(state.entry.workspaceId, "w");
    const contextBack = (tree) => React.Children.toArray(tree.props.contextPane.props.children).find((node) => node.type === "button");
    assert.equal(React.Children.toArray(returnedWork.props.contextPane.props.children).filter((node) => node.type === "button" && node.props.disabled).length, 0);
    contextBack(returnedWork).props.onClick();
    query = window.location.search;
    const returnedResult = render();
    assert.equal(state.entry.view, "result"); assert.equal(state.entry.resultRef, "task:r"); assert.equal(state.entry.explicit, false);
    assert.equal(React.Children.toArray(returnedResult.props.contextPane.props.children).filter((node) => node.type === "button" && node.props.disabled).length, 0);
    contextBack(returnedResult).props.onClick();
    assert.equal(state.entry.view, "work"); assert.equal(state.entry.workRef, "work-a");
    query = window.location.search = ""; render(); render();
    assert.equal(state.entry.view, "home"); assert.equal(state.entry.workRef, "");
    assert.equal(state.entry.resultRef, ""); assert.equal(state.entry.explicit, false); assert.equal(state.returns.length, 0);
    query = window.location.search = "?view=work&work_ref=work-b&workspace_id=other-w"; render(); render();
    assert.equal(state.entry.workRef, "work-b"); assert.equal(state.entry.workspaceId, "other-w");
    state = helpers.d1Reducer(state, { type: "navigate", entry: { ...state.entry, view: "result", resultRef: "task:b", explicit: true } });
    window.location.search = "?view=result&result_ref=task:b&workspace_id=other-w";
    listeners.get("popstate")();
    assert.equal(state.entry.resultRef, "task:b"); assert.equal(state.entry.explicit, false); assert.equal(state.returns.length, 0);
    assert.equal(findResult(render()).props.backLabel, "返回 CEO 工作台");
    query = window.location.search = ""; render(); render();
    values[1] = { loading: false, attention: null, businesses: [] };
    const findNode = (node, predicate) => {
      if (!React.isValidElement(node)) return null;
      if (predicate(node)) return node;
      for (const child of React.Children.toArray(node.props.children)) { const found = findNode(child, predicate); if (found) return found; }
      return null;
    };
    findNode(render(), (node) => node.type === Matter).props.onMatter({ source_ref: "task:anchor", source_type: "RESULT", workspace_id: "w" });
    query = window.location.search;
    const matterTree = render();
    assert.equal(state.returns[0].anchor, "matter-task:anchor");
    const isMainReturn = (node) => node.type === "button" && node.props.children === "← 返回原对象";
    const matterReturn = findNode(matterTree, isMainReturn);
    assert.ok(matterReturn, "Matter retains its existing Main return control");
    matterReturn.props.onClick();
    assert.equal(state.entry.view, "home"); assert.equal(state.returns.length, 0);
    for (const view of ["work", "result"]) {
      state = helpers.d1Reducer(helpers.initialD1State({ view: "home" }), { type: "navigate", entry: { view, workRef: "work-a", workspaceId: "w", resultRef: view === "result" ? "task:r" : "", explicit: true } });
      query = window.location.search = new URL(helpers.d1Href(state.entry), "https://local.invalid").search;
      const focusedTree = render();
      assert.equal(findNode(focusedTree, isMainReturn), null, "Other focused Main types do not gain that control");
      assert.ok(findNode(findNode(focusedTree, (node) => node.type === Shell).props.contextPane,
        (node) => node.type === "button" && React.Children.toArray(node.props.children).join("") === "← 返回原对象"));
    }
    state = helpers.d1Reducer(state, { type: "restore", entry: helpers.parseD1Entry("?view=work&work_ref=work-a&workspace_id=w") });
    query = window.location.search = "?view=work&work_ref=work-a&workspace_id=w";
    const restoredWork = render();
    assert.ok(findNode(findNode(restoredWork, (node) => node.type === Shell).props.contextPane,
      (node) => node.type === "button" && React.Children.toArray(node.props.children).join("") === "← 返回 CEO 工作台"));
  } finally { if (priorWindow === undefined) delete globalThis.window; else globalThis.window = priorWindow; }
});

test("compiled Work consumer keeps result scope, lifecycle controls and original return", async () => {
  const require = createRequire(import.meta.url), React = require("react");
  const { renderToStaticMarkup } = require("react-dom/server"), { transform, loadBindings } = require("next/dist/build/swc");
  const helpers = await import("../lib/d1State.mjs");
  await loadBindings();
  const source = readFileSync(new URL("../components/delivery/d1/WorkView.js", import.meta.url), "utf8");
  const { code } = await transform(source, { filename: "WorkView.js", jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "classic" } } }, module: { type: "commonjs" } });
  const values = ["", "", false, ""], lock = { current: false };
  let index = 0, work = { work_ref: "work-a", workspaceId: "w", problem: "当前问题", expected_result: "预期交付", reason: "当前进展", status: "READY", lifecycle_status: "READY", execution_status: "NONE", responsibility_holder_ref: "employee-a", responsibility_holder_name: "员工甲", result_refs: ["result-a", "result-b"], result_summaries: [{ reference_id: "result-a", title: "第一份结果" }] };
  const hookReact = { ...React, useState: (initial) => { const position = index++; return [values[position] ?? initial, (next) => { values[position] = typeof next === "function" ? next(values[position]) : next; }]; }, useRef: () => lock };
  const mod = { exports: {} };
  new Function("require", "module", "exports", "React", code)((name) => {
    if (name === "react") return hookReact;
    if (name.endsWith("d1State.mjs")) return helpers;
    if (name.endsWith("d1Api.js")) return { d1Error: (error) => error.message };
    if (name.endsWith("CeoMatterView.js")) return { workState: (status) => status };
    if (name.endsWith("runtimeApi.js")) return { workspaceEntryHref: (workspace) => `/workspace/${workspace}` };
    if (name.endsWith(".css")) return { __esModule: true, default: new Proxy({}, { get: (_, key) => key }) };
    return {};
  }, mod, mod.exports, hookReact);
  const results = [], employees = [], discussions = [], controls = [];
  let refreshed = 0, rejectControl = false;
  const api = { controlWork: async (...args) => { controls.push(args); if (rejectControl) throw new Error("控制失败"); } };
  const render = () => { index = 0; return mod.exports.default({ work, api, companyId: "company-a", onResult: (...args) => results.push(args), onDiscuss: (...args) => discussions.push(args), onRefresh: async () => { refreshed++; return { ...work, companyId: "company-a", lifecycle_status: helpers.controlTarget(work, controls.at(-1)[2]) }; }, onEmployeeDetail: (...args) => employees.push(args) }); };
  const findAll = (node, predicate) => {
    if (!React.isValidElement(node)) return [];
    return [...(predicate(node) ? [node] : []), ...React.Children.toArray(node.props.children).flatMap((child) => findAll(child, predicate))];
  };
  const textOf = (node) => React.Children.toArray(node.props.children).map((child) => typeof child === "string" ? child : React.isValidElement(child) ? textOf(child) : "").join("");
  const button = (tree, label) => findAll(tree, (node) => node.type === "button" && textOf(node) === label)[0];
  let tree = render(), markup = renderToStaticMarkup(tree);
  assert.equal(markup.split("预期交付").length - 1, 1);
  assert.match(markup, /当前进展/); assert.match(markup, /关联结果/);
  const rows = findAll(tree, (node) => node.type === "button" && node.props.className === "matterRow");
  assert.equal(rows.length, 2);
  rows[0].props.onClick(); rows[1].props.onClick();
  assert.deepEqual(results, [["result-a", "w"], ["result-b", "w"]]);
  assert.match(markup, /第一份结果/); assert.match(markup, /工作结果名称未记录/);
  assert.match(markup, /href="\/workspace\/w"/);
  findAll(tree, (node) => node.type === "button" && node.props["aria-label"] === "查看负责人详情")[0].props.onClick();
  button(tree, "一起讨论 ⌄").props.onClick();
  assert.deepEqual(employees, [["employee-a", "w"]]); assert.deepEqual(discussions, [["employee-a", "w"]]);
  button(tree, "暂停工作").props.onClick();
  tree = render();
  findAll(tree, (node) => node.type === "textarea")[0].props.onChange({ target: { value: "需要核对" } });
  tree = render();
  await findAll(tree, (node) => node.type === "form")[0].props.onSubmit({ preventDefault() {} });
  assert.deepEqual(controls[0], ["company-a", work, "pause", "需要核对"]);
  assert.equal(refreshed, 1); assert.equal(values[0], ""); assert.equal(values[1], "");
  button(render(), "停止工作").props.onClick();
  button(render(), "取消").props.onClick();
  assert.equal(findAll(render(), (node) => node.type === "form").length, 0);
  work = { ...work, lifecycle_status: "PAUSED", result_refs: [] };
  tree = render(); markup = renderToStaticMarkup(tree);
  assert.match(markup, /尚未返回结果/); assert.ok(button(tree, "恢复原工作")); assert.equal(button(tree, "暂停工作"), undefined);
  button(tree, "恢复原工作").props.onClick();
  findAll(render(), (node) => node.type === "textarea")[0].props.onChange({ target: { value: "恢复理由" } });
  rejectControl = true;
  await findAll(render(), (node) => node.type === "form")[0].props.onSubmit({ preventDefault() {} });
  assert.match(renderToStaticMarkup(render()), /控制失败/);
  work = { ...work, lifecycle_status: "COMPLETED" };
  tree = render();
  assert.equal(button(tree, "恢复原工作"), undefined); assert.equal(button(tree, "停止工作"), undefined);
});

test("compiled Result consumer keeps view receipt separate from decisions and returns", async () => {
  const require = createRequire(import.meta.url), React = require("react");
  const { renderToStaticMarkup } = require("react-dom/server"), { transform, loadBindings } = require("next/dist/build/swc");
  const helpers = await import("../lib/d1State.mjs");
  await loadBindings();
  const source = readFileSync(new URL("../components/delivery/d1/ResultView.js", import.meta.url), "utf8");
  const { code } = await transform(source, { filename: "ResultView.js", jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "classic" } } }, module: { type: "commonjs" } });
  const readableResult = { tenant_id: "t", company_id: "A", workspace_id: "w", reference_id: "result-a", result_version: "v1", kind: "RESULT", title: "当前结果", content: "真实结果正文", source_work_ref: "work-a", artifacts: [] };
  let result = readableResult, state = { loading: false, result, error: "" }, reload = 0, receipt = { status: "idle", error: "" };
  let choice = { action: "", reason: "", confirmed: false, pending: null, busy: false, error: "", notice: "" }, actor = "", sent = null;
  let index = 0, viewed = 0, viewedCallback = 0, backs = 0, failReceipt = false;
  const workReturns = [], attempt = { current: null }, identity = { current: "" }, mounted = { current: true };
  let refIndex = 0;
  const effects = [];
  const hookReact = { ...React, useState: () => {
    const position = index++;
    return [[state, reload, receipt, choice][position], (next) => {
      if (position === 0) state = typeof next === "function" ? next(state) : next;
      if (position === 1) reload = typeof next === "function" ? next(reload) : next;
      if (position === 2) receipt = typeof next === "function" ? next(receipt) : next;
      if (position === 3) choice = typeof next === "function" ? next(choice) : next;
    }];
  }, useRef: () => [attempt, identity, mounted][refIndex++], useEffect: (effect) => effects.push(effect) };
  const mod = { exports: {} };
  new Function("require", "module", "exports", "React", code)((name) => {
    if (name === "react") return hookReact;
    if (name.endsWith("d1State.mjs")) return helpers;
    if (name.endsWith("d1Api.js")) return { d1Error: () => "读取失败" };
    if (name.endsWith("runtimeApi.js")) return { workspaceEntryHref: () => "/workspace/w" };
    if (name.endsWith(".css")) return { __esModule: true, default: new Proxy({}, { get: (_, key) => key }) };
    return {};
  }, mod, mod.exports, hookReact);
  let selection = parseD1Entry("?view=result&result_ref=result-a&workspace_id=w");
  const api = { viewed: async () => { viewed += 1; if (failReceipt) throw new Error("回执失败"); },
    respond: async (_company, _workspace, _result, action, reason, requestId) => { sent = { action, reason, request_id: requestId }; },
    result: async () => ({ ...state.result, user_response: sent ? { ...sent, tenant_id: "t", company_id: "A", workspace_id: "w", result_ref: state.result.reference_id, result_version: state.result.result_version, source_work_ref: state.result.source_work_ref, ceo_id: "ceo" } : null }) };
  const render = (backLabel = "返回 CEO 工作台") => { index = refIndex = 0; effects.length = 0; const tree = mod.exports.default({ companyId: "A", actorId: actor, selection, api, backLabel, onBack: () => { backs++; }, onWork: (...args) => workReturns.push(args), onViewed: () => { viewedCallback++; } }); return { tree, markup: renderToStaticMarkup(tree) }; };
  const findAll = (node, predicate) => {
    if (!React.isValidElement(node)) return [];
    return [...(predicate(node) ? [node] : []), ...React.Children.toArray(node.props.children).flatMap((child) => findAll(child, predicate))];
  };
  const textOf = (node) => React.Children.toArray(node.props.children).map((child) => typeof child === "string" ? child : React.isValidElement(child) ? textOf(child) : "").join("");
  const button = (tree, label) => findAll(tree, (node) => node.type === "button" && textOf(node) === label)[0];
  const restored = render();
  effects.at(-1)();
  assert.equal(viewed, 0);
  assert.match(restored.markup, /由链接恢复 · 未自动记录查看/);
  assert.match(restored.markup, /真实结果正文/); assert.match(restored.markup, /结果版本<\/dt><dd[^>]*>v1/);
  assert.match(restored.markup, /此来源尚不能记录选择/);
  assert.doesNotMatch(restored.markup, /<button[^>]*>(?:接受此结果|要求修改|拒绝此结果)<\/button>/);
  assert.match(restored.markup, /href="\/workspace\/w"/);
  button(restored.tree, "回原工作核对").props.onClick();
  button(restored.tree, "返回 CEO 工作台").props.onClick();
  assert.deepEqual(workReturns, [["work-a", "w"]]); assert.equal(backs, 1);
  assert.match(render("返回原对象").markup, /返回原对象/);

  selection = { ...selection, explicit: true };
  effects.length = 0; render(); effects.at(-1)();
  await Promise.resolve(); await Promise.resolve();
  assert.equal(viewed, 1); assert.equal(viewedCallback, 1); assert.equal(receipt.status, "saved");
  assert.match(render().markup, /已记录此版本的查看/);

  result = { ...readableResult, content: " ", source_work_ref: "" };
  state = { loading: false, result, error: "" }; receipt = { status: "idle", error: "" }; attempt.current = null;
  const unreadable = render(); effects.at(-1)();
  assert.equal(viewed, 1); assert.match(unreadable.markup, /尚无可阅读的结果材料/);
  assert.equal(button(unreadable.tree, "回原工作核对"), undefined);
  button(unreadable.tree, "重新读取结果").props.onClick(); assert.equal(reload, 1);

  state = { loading: false, result: null, error: "读取失败" };
  const failedRead = render();
  assert.match(failedRead.markup, /读取失败/);
  button(failedRead.tree, "重新读取结果").props.onClick(); assert.equal(reload, 2);
  button(failedRead.tree, "返回 CEO 工作台").props.onClick(); assert.equal(backs, 2);

  result = readableResult; state = { loading: false, result, error: "" }; receipt = { status: "idle", error: "" }; attempt.current = null; failReceipt = true;
  render(); effects.at(-1)();
  await Promise.resolve(); await Promise.resolve();
  assert.equal(receipt.status, "error"); assert.equal(viewed, 2);
  failReceipt = false;
  await button(render().tree, "重试保存查看记录").props.onClick();
  assert.equal(viewed, 3); assert.equal(receipt.status, "saved");
  const oldStorage = globalThis.sessionStorage;
  const storage = new Map(); globalThis.sessionStorage = { getItem: (key) => storage.get(key) || null, setItem: (key, value) => storage.set(key, value), removeItem: (key) => storage.delete(key) };
  try {
    actor = ""; sent = null; choice = { action: "", reason: "", confirmed: false, pending: null, busy: false, error: "", notice: "" };
    state = { loading: false, error: "", result: { ...readableResult, response_actor_ref: "ceo", response_eligibility: { status: "ELIGIBLE" }, user_response: null } };
    const eligible = render(); assert.match(eligible.markup, /对这份交付作选择/);
    const radios = findAll(eligible.tree, (node) => node.type === "input" && node.props.type === "radio");
    radios[1].props.onChange();
    const reason = findAll(render().tree, (node) => node.type === "textarea")[0]; reason.props.onChange({ target: { value: "请员工修改" } });
    const confirm = findAll(render().tree, (node) => node.type === "input" && node.props.type === "checkbox")[0]; confirm.props.onChange({ target: { checked: true } });
    await button(render().tree, "保存此版本的人类选择").props.onClick();
    assert.equal(sent.action, "REVISE"); assert.equal(sent.reason, "请员工修改");
    assert.equal(state.result.user_response.request_id, sent.request_id);
    assert.match(render().markup, /已保存：要求修改/);

    // A network-unknown write cannot be reposted until a fresh scoped GET succeeds.
    state = { loading: false, error: "", result: { ...readableResult, response_actor_ref: "ceo", response_eligibility: { status: "ELIGIBLE" }, user_response: null } };
    choice = { action: "ACCEPT", reason: "已核对", confirmed: true, pending: null, busy: false, error: "", notice: "" };
    sent = null;
    let posts = [], reads = 0;
    api.respond = async (_company, _workspace, _result, action, reason, requestId) => {
      posts.push(requestId);
      if (posts.length === 1) throw new Error("unknown");
      sent = { action, reason, request_id: requestId };
    };
    api.result = async () => {
      reads++;
      if (reads <= 3) throw new Error("read unavailable");
      return { ...state.result, user_response: sent ? { ...sent, tenant_id: "t", company_id: "A", workspace_id: "w", result_ref: "result-a", result_version: "v1", source_work_ref: "work-a", ceo_id: "ceo" } : null };
    };
    await button(render().tree, "保存此版本的人类选择").props.onClick();
    assert.equal(posts.length, 1); assert.ok(choice.pending);
    const originalId = choice.pending.request_id;
    choice = { ...choice, confirmed: true };
    await button(render().tree, "保存此版本的人类选择").props.onClick();
    assert.equal(posts.length, 1, "failed recovery GET must prevent another POST");
    choice = { ...choice, confirmed: true };
    await button(render().tree, "保存此版本的人类选择").props.onClick();
    assert.deepEqual(posts, [originalId, originalId]);
    assert.equal(state.result.user_response.request_id, originalId);

    // A late response from the old Result must not clear a newly selected Result's draft.
    selection = { ...selection, resultRef: "result-a" };
    state = { loading: false, error: "", result: { ...readableResult, response_actor_ref: "ceo", response_eligibility: { status: "ELIGIBLE" }, user_response: null } };
    choice = { action: "ACCEPT", reason: "旧对象理由", confirmed: true, pending: null, busy: false, error: "", notice: "" };
    let releaseOld, lateReads = 0;
    api.respond = () => new Promise((resolve) => { releaseOld = resolve; });
    api.result = async () => { lateReads++; return state.result; };
    const oldSubmit = button(render().tree, "保存此版本的人类选择").props.onClick();
    selection = { ...selection, resultRef: "result-b" };
    state = { loading: false, error: "", result: { ...readableResult, reference_id: "result-b", result_version: "v2", response_actor_ref: "ceo", response_eligibility: { status: "ELIGIBLE" }, user_response: null } };
    choice = { action: "REVISE", reason: "新对象理由", confirmed: true, pending: null, busy: false, error: "", notice: "" };
    const newKey = helpers.resultResponseKey("A", "w", state.result, "ceo"); storage.set(newKey, "新对象草稿");
    render(); releaseOld(); await oldSubmit;
    assert.equal(lateReads, 0); assert.equal(storage.get(newKey), "新对象草稿"); assert.equal(choice.reason, "新对象理由");

    // Unmount invalidates the same identity before an in-flight POST resolves.
    let releaseUnmount;
    api.respond = () => new Promise((resolve) => { releaseUnmount = resolve; });
    const unmountedSubmit = button(render().tree, "保存此版本的人类选择").props.onClick();
    const pendingId = choice.pending.request_id;
    effects[0]()();
    releaseUnmount(); await unmountedSubmit;
    assert.equal(lateReads, 0); assert.equal(storage.get(newKey), "新对象草稿"); assert.equal(choice.pending.request_id, pendingId);
  } finally { if (oldStorage === undefined) delete globalThis.sessionStorage; else globalThis.sessionStorage = oldStorage; }
});


test("malformed Utility bridge stays invalid and cannot fall through to latest Result", () => {
  const base = "?view=result&result_ref=task%3At&result_workspace=w&work_ref=work-a&result_version=" + "a".repeat(64) + "&origin_company=A";
  for (const suffix of ["&result_origin=utility&result_origin=utility", "&result_origin=other", "&result_origin=utility&result_version=bad", "&result_origin=utility&origin_company=B&origin_company=A"]) {
    const entry = parseD1Entry(base + suffix);
    assert.equal(entry.resultBridgeInvalid, true);
    assert.equal(entry.resultOrigin, "");
    assert.equal(parseD1Entry(new URL(d1Href(entry), "https://local.invalid").search).resultBridgeInvalid, true);
  }
});

test("Result receipt requires full tenant and object identity, including actor", () => {
  const expected = { tenant_id: "t", company_id: "A", workspace_id: "w", reference_id: "task:t", result_version: "a".repeat(64), source_work_ref: "work-a", response_actor_ref: "ceo" };
  const pending = { request_id: "123e4567-e89b-42d3-a456-426614174000", action: "REVISE", reason: "修改" };
  const receipt = { tenant_id: "t", company_id: "A", workspace_id: "w", result_ref: "task:t", result_version: expected.result_version, source_work_ref: "work-a", ceo_id: "ceo", ...pending };
  assert.equal(resultReceiptMatches({ ...expected, user_response: receipt }, pending, expected), true);
  for (const field of ["tenant_id", "company_id", "workspace_id", "result_ref", "result_version", "source_work_ref", "ceo_id", "request_id", "action", "reason"]) {
    assert.equal(resultReceiptMatches({ ...expected, user_response: { ...receipt, [field]: "foreign" } }, pending, expected), false, field);
  }
  const context = ["t", "A", "w", "task:t", expected.result_version, "work-a", "ceo"];
  assert.equal(restoreResultResponse(JSON.stringify({ context, at: 1000, action: "REVISE", reason: "修改", request_id: pending.request_id, pending: { ...pending, request_id: "other" } }), context, 1001), null);
});


test("Result draft storage bounds serialized size and scoped count", () => {
  const map = new Map(), storage = { getItem: (key) => map.get(key) || null, setItem: (key, value) => map.set(key, value) };
  for (let i = 0; i < 32; i++) saveResultResponse(storage, `curis.result.response.${i}`, { at: 1000, reason: "ok" });
  assert.throws(() => saveResultResponse(storage, "curis.result.response.overflow", { at: 1000 }), /数量/);
  assert.throws(() => saveResultResponse(storage, "curis.result.response.1", { reason: "x".repeat(17000) }), /上限/);
});
