import assert from "node:assert/strict";
import test from "node:test";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import vm from "node:vm";

import {
  assignSkill,
  unassignSkill,
  removeSkill,
  productStateFor,
  resolveTalentReturnPath,
} from "../lib/talentMarket.js";


test("product states do not promote catalog entries into usable resources", () => {
  assert.equal(productStateFor({ market_kind: "company_employee" }, "experts"), "已加入公司");
  assert.equal(productStateFor({ recruitable: true }, "experts"), "可招聘");
  assert.equal(productStateFor({ recruitable: false }, "experts"), "正在准备");
  assert.equal(productStateFor({ source: "tenant_private" }, "skills"), "已安装");
  assert.equal(productStateFor({ status: "active", skill_type: "analysis" }, "skills"), "可安装");
  assert.equal(productStateFor({ status: "active", skill_type: "development" }, "skills"), "暂不可用");
  assert.equal(
    productStateFor({ authorization_status: "not_authorized", health_status: "unknown" }, "connectors"),
    "未连接",
  );
  assert.equal(
    productStateFor({ authorization_status: "authorized", health_status: "healthy" }, "connectors"),
    "已连接",
  );
});

const require = createRequire(import.meta.url), React = require("react"), swc = require("next/dist/build/swc");
await swc.loadBindings();
const paths = {
  route: "app/ceo-office/capabilities/page.js", model: "components/v1/ModelManagement.js",
  agent: "app/ceo-office/capabilities/PrivateAgentDrawer.js",
  employee: "app/ceo-office/organization/employees/[id]/page.js",
  edit: "app/ceo-office/organization/employees/[id]/EmployeeEditDrawer.js",
  talent: "app/ceo-office/talent-market/page.js",
  usage: "app/platform/UsageDashboardPanel.js",
  detail: "app/ceo-office/capabilities/[type]/[id]/page.js",
};
const compiled = {};
for (const [key, path] of Object.entries(paths)) compiled[key] = (await swc.transform(readFileSync(new URL(`../${path}`, import.meta.url), "utf8"), {
  filename: path, isModule: true, jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } }, module: { type: "commonjs" },
})).code;
const walk = tree => tree == null || typeof tree !== "object" ? [] : Array.isArray(tree) ? tree.flatMap(walk) : [tree, ...walk(tree.props?.children)];
const textOf = tree => tree == null ? "" : typeof tree !== "object" ? String(tree) : Array.isArray(tree) ? tree.map(textOf).join("") : textOf(tree.props?.children);
const button = (tree, label) => { const result = walk(tree).find(n => ["button", "TerraButton"].includes(n.type) && textOf(n) === label); assert.ok(result, label); return result; };
const tick = () => new Promise(resolve => setImmediate(resolve));

test("local discovery adds once and binds an existing employee with uncertain-write readback", async () => {
  const local = { name: "Synthetic Codex", discovery_ref: "a".repeat(64), capability_id: "agent.local.codex.fixture",
    installation_path: "/synthetic/codex", bindable: true, limitation: "仅发现安装，实际执行待核验。" };
  const retained = { id: "original", capability_source: "official", capability_type: "model", capability_id: "original-model", enabled: true, priority: 1 };
  let bindings = [retained], creates = 0, writes = 0, finished;
  const api = {
    discoverLocalAgents: async () => ({ agents: [local] }),
    createPrivateCapability: async value => { creates++; assert.deepEqual(Object.keys(value.metadata), ["local_agent_ref"]); return { ...value, status: "active" }; },
    getAgentAllowanceCompanies: async () => ({ companies: [{ company_id: "co", name: "Company" }] }),
    getLocalAgentEmployees: async () => ({ employees: [{ id: "employee", company_id: "co", name: "Writer", enabled: true }, { id: "foreign", company_id: "other", name: "Foreign" }] }),
    getEmployeeCapabilities: async id => { assert.equal(id, "employee"); return { employee_id: id, bindings }; },
    setEmployeeCapabilities: async () => { throw Error("full-list replacement is forbidden"); },
    addEmployeeAgentBinding: async (id, company, capability) => {
      writes++; assert.equal(id, "employee"); assert.equal(company, "co"); assert.equal(capability, local.capability_id);
      bindings = [...bindings, { capability_source: "tenant_private", capability_type: "agent", capability_id: capability, enabled: true }];
      throw Error("response lost");
    },
  };
  const h = scene("agent", api), render = () => h.render({ open: true, onSuccess: value => { finished = value; } });
  render(); let tree = render();
  await button(tree, "发现本机 Agent").props.onClick(); tree = render();
  button(tree, "Synthetic Codex · 选择添加").props.onClick(); tree = render();
  assert.equal(walk(tree).find(node => node.type === "TerraInput" && node.props.label === "Agent 标识").props.readOnly, true);
  await walk(tree).find(node => node.type === "form").props.onSubmit({ preventDefault() {} }); tree = render();
  assert.equal(creates, 1); assert.equal(finished, undefined);
  const company = walk(tree).find(node => node.type === "select" && node.props["aria-label"] === "绑定公司");
  company.props.onChange({ target: { value: "co" } }); tree = render();
  const employee = walk(tree).find(node => node.type === "select" && node.props["aria-label"] === "绑定员工");
  assert.doesNotMatch(textOf(employee), /Foreign/);
  employee.props.onChange({ target: { value: "employee" } }); tree = render();
  await button(tree, "绑定所选员工").props.onClick(); tree = render();
  assert.equal(writes, 1); assert.equal(bindings[0], retained);
  assert.equal(button(tree, "绑定所选员工").props.disabled, true);
  assert.match(textOf(tree), /不会自动重复提交/);
  await button(tree, "读取绑定结果").props.onClick(); tree = render();
  assert.equal(writes, 1); assert.match(textOf(tree), /员工绑定已读回确认/);
  button(tree, "完成登记").props.onClick(); assert.equal(finished.capability_id, local.capability_id);
});

test("disabled local Agent binding is never silently re-enabled", async () => {
  const local = { name: "Local", discovery_ref: "a".repeat(64), capability_id: "agent.local.fixture", bindable: true };
  let writes = 0;
  const h = scene("agent", {
    discoverLocalAgents: async () => ({ agents: [local] }),
    createPrivateCapability: async value => ({ ...value, status: "active" }),
    getAgentAllowanceCompanies: async () => ({ companies: [{ company_id: "co", name: "Company" }] }),
    getLocalAgentEmployees: async () => ({ employees: [{ id: "employee", company_id: "co", enabled: true }] }),
    getEmployeeCapabilities: async () => ({ employee_id: "employee", bindings: [{ capability_source: "tenant_private", capability_type: "agent", capability_id: local.capability_id, enabled: false }] }),
    addEmployeeAgentBinding: async () => { writes++; },
    setEmployeeCapabilities: async () => { writes++; },
  });
  const render = () => h.render({ open: true }); render(); let tree = render();
  await button(tree, "发现本机 Agent").props.onClick(); tree = render();
  button(tree, "Local · 选择添加").props.onClick(); tree = render();
  await walk(tree).find(node => node.type === "form").props.onSubmit({ preventDefault() {} }); tree = render();
  walk(tree).find(node => node.props?.["aria-label"] === "绑定公司").props.onChange({ target: { value: "co" } }); tree = render();
  walk(tree).find(node => node.props?.["aria-label"] === "绑定员工").props.onChange({ target: { value: "employee" } }); tree = render();
  await button(tree, "绑定所选员工").props.onClick(); tree = render();
  assert.equal(writes, 0); assert.match(textOf(tree), /不会自动重新启用/);
});

test("unverified local app registration never exposes an executable binding", async () => {
  const local = { name: "Synthetic WorkBuddy", discovery_ref: "b".repeat(64), capability_id: "agent.local.workbuddy.fixture", installation_path: "/synthetic/WorkBuddy.app", bindable: false, limitation: "机器接口尚未验证。" };
  let listed = 0;
  const h = scene("agent", {
    discoverLocalAgents: async () => ({ agents: [local] }),
    createPrivateCapability: async value => ({ ...value, status: "inactive" }),
    getLocalAgentEmployees: async () => { listed++; throw Error("must not list employees"); },
  });
  const render = () => h.render({ open: true }); render(); let tree = render();
  await button(tree, "发现本机 Agent").props.onClick(); tree = render();
  button(tree, "Synthetic WorkBuddy · 选择添加").props.onClick(); tree = render();
  await walk(tree).find(node => node.type === "form").props.onSubmit({ preventDefault() {} }); tree = render();
  assert.match(textOf(tree), /暂不能绑定执行/); assert.equal(listed, 0);
  assert.ok(!walk(tree).some(node => node.type === "select" && node.props["aria-label"] === "绑定员工"));
});

test("manual unknown app submits selected path and remains inactive", async () => {
  const local = { manual_selection: true, name: "Synthetic WorkBuddy", discovery_ref: "b".repeat(64), capability_id: "agent.local.workbuddy.fixture", installation_path: "/synthetic/WorkBuddy.app", bindable: false, limitation: "机器接口尚未验证。" };
  let listed = 0;
  const h = scene("agent", {
    discoverLocalAgents: async path => { assert.equal(path, local.installation_path); return { agents: [local] }; },
    createPrivateCapability: async value => { assert.equal(value.metadata.local_installation_path, local.installation_path); return { ...value, status: "inactive" }; },
    getLocalAgentEmployees: async () => { listed++; throw Error("must not list employees"); },
  });
  const render = () => h.render({ open: true }); render(); let tree = render();
  walk(tree).find(node => node.props?.["aria-label"] === "其他应用路径").props.onChange({ target: { value: local.installation_path } }); tree = render();
  await button(tree, "读取所选应用安装").props.onClick(); tree = render();
  button(tree, "Synthetic WorkBuddy · 选择添加").props.onClick(); tree = render();
  await walk(tree).find(node => node.type === "form").props.onSubmit({ preventDefault() {} }); tree = render();
  assert.match(textOf(tree), /暂不能绑定执行/); assert.equal(listed, 0);
  assert.ok(!walk(tree).some(node => node.type === "select" && node.props["aria-label"] === "绑定员工"));
});

test("late local registration response cannot complete a closed and reopened drawer", async () => {
  let release, finished = 0;
  const local = { name: "Local", discovery_ref: "c".repeat(64), capability_id: "agent.local.fixture", limitation: "待核验" };
  const h = scene("agent", {
    discoverLocalAgents: async () => ({ agents: [local] }),
    createPrivateCapability: value => new Promise(resolve => { release = () => resolve({ ...value, status: "inactive" }); }),
  });
  const render = open => h.render({ open, onSuccess: () => { finished++; } });
  render(true); let tree = render(true);
  await button(tree, "发现本机 Agent").props.onClick(); tree = render(true);
  button(tree, "Local · 选择添加").props.onClick(); tree = render(true);
  const saving = walk(tree).find(node => node.type === "form").props.onSubmit({ preventDefault() {} });
  render(false); render(true); release(); await saving; tree = render(true);
  assert.equal(finished, 0); assert.doesNotMatch(textOf(tree), /已登记/);
  assert.equal(button(tree, "发现本机 Agent").props.disabled, false);
});

function scene(key, api = {}, runtime = { status: "ready", companyId: "co" }) {
  const slots = [], effects = []; let cursor = 0, uuid = 0;
  const same = (a, b) => a && b && a.length === b.length && a.every((v, i) => Object.is(v, b[i]));
  const hooks = {
    ...React,
    useState(initial) { const i = cursor++; if (!(i in slots)) slots[i] = { value: typeof initial === "function" ? initial() : initial }; return [slots[i].value, value => { slots[i].value = typeof value === "function" ? value(slots[i].value) : value; }]; },
    useRef(initial) { const i = cursor++; return slots[i] ||= { current: initial }; },
    useMemo(fn, deps) { const i = cursor++; if (!slots[i] || !same(slots[i].deps, deps)) slots[i] = { deps, value: fn() }; return slots[i].value; },
    useCallback(fn, deps) { return hooks.useMemo(() => fn, deps); },
    useEffect(fn, deps) { const i = cursor++; if (!slots[i] || !same(slots[i].deps, deps)) { const old = slots[i]; slots[i] = { deps }; effects.push(() => { old?.cleanup?.(); slots[i].cleanup = fn(); }); } },
  };
  hooks.useLayoutEffect = hooks.useEffect;
  const module = { exports: {} };
  vm.runInNewContext(compiled[key], { module, exports: module.exports, console, URLSearchParams, JSON,
    crypto: { randomUUID: () => `request-${++uuid}` },
    require(name) {
      if (name === "react") return hooks;
      if (name === "react/jsx-runtime") return require(name);
      if (name === "next/navigation") return { useParams: () => ({ id: "employee-1" }), useSearchParams: () => new URLSearchParams() };
      if (name === "next/link") return { __esModule: true, default: "a" };
      if (name.includes("RuntimeProvider")) return { useRuntime: () => runtime };
      if (name.includes("lib/")) return { businessReturnInput: () => null, roleLabel: value => value, getSkillAssignments: async () => [], ...api };
      return new Proxy({ __esModule: true, default: name.split("/").pop().replace(".js", "") }, { get: (object, prop) => prop in object ? object[prop] : prop });
    },
  });
  return {
    render(props = {}, exported = "default") {
      cursor = 0; let tree = module.exports[exported](props);
      while (typeof tree?.type === "function" || tree?.type === React.Suspense) tree = tree.type === React.Suspense ? tree.props.children : tree.type(tree.props);
      while (effects.length) effects.shift()(); return tree;
    },
    unmount() { slots.forEach(slot => slot?.cleanup?.()); },
  };
}

test("normal capabilities route mounts Agent setup inside the existing model shell with return links", async () => {
  const route = scene("route").render();
  assert.equal(route.type, "ModelManagement");
  assert.equal(typeof route.props.children.type, "function");
  const model = scene("model", {}, { status: "loading" }).render({ children: route.props.children });
  assert.equal(model.type, "TerraShell");
  assert.ok(walk(model).includes(route.props.children));
  let fail = true;
  const setup = scene("route", { getPrivateCapabilities: async () => { if (fail) throw Error("offline"); return { capabilities: [{ capability_id: "agent.local", display_name: "Local", metadata: { kind: "codex-cli" } }] }; } });
  setup.render({}, "AgentSetupPanel"); await tick();
  let tree = setup.render({}, "AgentSetupPanel"); assert.match(textOf(tree), /offline/);
  let disclosure = button(tree, "配置外部 Agent 与员工执行");
  assert.equal(disclosure.props["aria-expanded"], false);
  assert.equal(disclosure.props["aria-controls"], "employee-agent-panel");
  assert.equal(walk(tree).find(n => n.props.id === "employee-agent-panel").props.hidden, true);
  disclosure.props.onClick(); tree = setup.render({}, "AgentSetupPanel");
  disclosure = button(tree, "配置外部 Agent 与员工执行");
  assert.equal(disclosure.props["aria-expanded"], true);
  assert.equal(walk(tree).find(n => n.props.id === "employee-agent-panel").props.hidden, false);
  assert.ok(walk(tree).some(n => n.type === "AgentAllowancePanel"));
  disclosure.props.onClick(); tree = setup.render({}, "AgentSetupPanel");
  assert.equal(button(tree, "配置外部 Agent 与员工执行").props["aria-expanded"], false);
  assert.equal(walk(tree).find(n => n.props.id === "employee-agent-panel").props.hidden, true);
  button(tree, "配置外部 Agent 与员工执行").props.onClick(); tree = setup.render({}, "AgentSetupPanel");
  fail = false; await button(tree, "读取已登记 Agent").props.onClick(); tree = setup.render({}, "AgentSetupPanel");
  assert.match(textOf(tree), /Local.*agent.local.*本机 Codex/);
  assert.ok(walk(tree).some(n => n.type === "AgentAllowancePanel"));
  button(tree, "注册自定义 Agent").props.onClick(); tree = setup.render({}, "AgentSetupPanel");
  const drawer = walk(tree).find(n => n.type === "PrivateAgentDrawer"); assert.equal(drawer.props.open, true);
  drawer.props.onClose(); assert.equal(walk(setup.render({}, "AgentSetupPanel")).find(n => n.type === "PrivateAgentDrawer").props.open, false);
  const skillLink = walk(tree).find(n => n.type === "a" && n.props.href.includes("talent-market"));
  assert.equal(resolveTalentReturnPath({ returnTo: new URL(skillLink.props.href, "http://curis").searchParams.get("returnTo") }), "/ceo-office/capabilities#employee-agents");
  assert.ok(walk(tree).some(n => n.props.href === "/ceo-office/settings?tab=models"));
  const settings = readFileSync(new URL("../app/ceo-office/settings/page.js", import.meta.url), "utf8");
  assert.match(settings, /href="\/ceo-office\/capabilities#employee-agents"/);
  assert.doesNotMatch(settings, /外部 AI Agent 集成暂未开放/);
});

test("existing DSH edit sends only a revision-bound choice; lost response requires readback", async () => {
  const old = { capability_id: "agent.dsh", display_name: "DSH", revision: "a".repeat(64),
    metadata: { kind: "acp-stdio", agent_id: "deepseek_harness", installation_ref: "b".repeat(64), dsh_shared_account: false } };
  let calls = 0, saved, successes = 0;
  const h = scene("agent", {
    updateDshAgentAccount: async (id, value) => { calls++; assert.equal(id, old.capability_id);
      assert.deepEqual(JSON.parse(JSON.stringify(value)), { company_id: "co", expected_revision: old.revision, dsh_shared_account: true, consent: true });
      saved = { ...old, revision: "c".repeat(64), metadata: { ...old.metadata, dsh_shared_account: true } }; throw Error("response lost"); },
    getPrivateCapabilities: async () => ({ capabilities: [saved] }),
  });
  const props = { open: true, editingAgent: old, companyId: "co", onSuccess: () => successes++ };
  h.render(props); let tree = h.render(props);
  assert.equal(button(tree, "确认变更账号配置").props.disabled, true);
  walk(tree).find(n => n.type === "input" && n.props.type === "checkbox").props.onChange({ target: { checked: true } }); tree = h.render(props);
  const submit = walk(tree).find(n => n.type === "form").props.onSubmit;
  submit({ preventDefault() {} }); submit({ preventDefault() {} }); await tick(); tree = h.render(props);
  assert.equal(calls, 1); assert.equal(successes, 0); assert.equal(button(tree, "确认变更账号配置").props.disabled, true);
  await button(tree, "读取配置结果").props.onClick(); assert.equal(successes, 1); assert.equal(calls, 1);
});

test("DSH edit entry preserves the original registration and drops late results after Company change", async () => {
  const item = { capability_id: "agent.dsh", display_name: "DSH", revision: "a".repeat(64),
    metadata: { kind: "acp-stdio", agent_id: "deepseek_harness", installation_ref: "b".repeat(64) } };
  const route = scene("route", { getPrivateCapabilities: async () => ({ capabilities: [item] }) });
  route.render({}, "AgentSetupPanel"); await tick(); let tree = route.render({}, "AgentSetupPanel");
  button(tree, "编辑账号配置").props.onClick(); tree = route.render({}, "AgentSetupPanel");
  const drawer = walk(tree).find(n => n.type === "PrivateAgentDrawer"); assert.equal(drawer.props.editingAgent, item); assert.equal(drawer.props.companyId, "co");
  let release, successes = 0;
  const h = scene("agent", { updateDshAgentAccount: () => new Promise(resolve => { release = resolve; }) });
  const props = { open: true, editingAgent: item, companyId: "co", onSuccess: () => successes++ };
  h.render(props); tree = h.render(props);
  walk(tree).find(n => n.type === "input" && n.props.type === "checkbox").props.onChange({ target: { checked: true } }); tree = h.render(props);
  walk(tree).find(n => n.type === "form").props.onSubmit({ preventDefault() {} });
  h.render({ ...props, companyId: "other" });
  release({ ...item, revision: "d".repeat(64), metadata: { ...item.metadata, dsh_shared_account: true } }); await tick();
  assert.equal(successes, 0);
});

test("Codex registration submits no endpoint, and unknown save must read the registry without repeating POST", async () => {
  let posts = 0, payload, successes = 0;
  const api = { createPrivateCapability: async value => { posts++; payload = value; throw Error("response lost"); },
    getPrivateCapabilities: async () => ({ capabilities: [{ ...payload }] }) };
  const h = scene("agent", api), props = { open: true, onSuccess: () => successes++ };
  h.render(props); let tree = h.render(props);
  const change = (label, value) => { walk(tree).find(n => n.props.label === label).props.onChange({ target: { value } }); tree = h.render(props); };
  change("Agent 标识", "agent.local"); change("显示名称", "Local");
  walk(tree).find(n => n.type === "select").props.onChange({ target: { value: "codex-cli" } }); tree = h.render(props);
  assert.ok(!walk(tree).some(n => n.props.label === "接入地址 / 命令"));
  const submit = walk(tree).find(n => n.type === "form").props.onSubmit;
  await Promise.all([submit({ preventDefault() {} }), submit({ preventDefault() {} })]); tree = h.render(props);
  assert.equal(posts, 1); assert.equal(payload.metadata.kind, "codex-cli"); assert.equal(payload.metadata.endpoint, undefined); assert.equal(payload.metadata.browser_skill_path, undefined);
  assert.equal(button(tree, "保存自定义 Agent").props.disabled, true);
  await button(tree, "读取登记结果").props.onClick(); assert.equal(successes, 1); assert.equal(posts, 1);
});

test("actual employee parent passes Agent to editor and adding it preserves other binding states", async () => {
  const original = { capability_source: "tenant_private", capability_type: "model", capability_id: "original", priority: 70, enabled: false };
  let bindings = [original], calls = 0;
  const api = {
    getEmployee: async () => ({ id: "employee-1", company_id: "co", name: "Writer", role: "writing", status: "idle" }),
    getDepartments: async () => ({}), getEmployeeTemplates: async () => ({}), getEmployeeSkills: async () => ({}), getEmployeeTools: async () => ({}),
    getCapabilitySelector: async () => ({ capabilities: [{ source: "tenant_private", capability_type: "agent", capability_id: "agent.local", label: "Local", enabled: true }] }),
    getEmployeeCapabilities: async () => ({ employee_id: "employee-1", bindings }), getOrganizationProjection: async () => ({ company: { company_id: "co" } }),
    setEmployeeCapabilities: async (id, next) => { assert.equal(id, "employee-1"); calls++; bindings = next; return { employee_id: id, bindings }; },
  };
  const parent = scene("employee", api); parent.render(); await tick(); let tree = parent.render();
  await button(tree, "编辑员工").props.onClick(); tree = parent.render();
  const props = walk(tree).find(n => n.type === "EmployeeEditDrawer").props;
  assert.equal(props.capabilities.length, 1); assert.equal(props.capabilities[0].capability_type, "agent");
  const edit = scene("edit", api); edit.render(props); tree = edit.render(props);
  walk(tree).find(n => n.type === "input" && n.props.type === "checkbox").props.onChange(); tree = edit.render(props);
  await walk(tree).find(n => n.type === "form").props.onSubmit({ preventDefault() {} });
  assert.equal(calls, 1); assert.equal(JSON.stringify(bindings[0]), JSON.stringify(original)); assert.equal(bindings[1].capability_id, "agent.local");
  const cold = scene("employee", api); cold.render(); await tick();
  const coldProps = walk(cold.render()).find(n => n.type === "EmployeeEditDrawer").props;
  assert.equal(coldProps.bindings.length, 2); assert.equal(coldProps.bindings[1].capability_type, "agent");
  const wrong = scene("employee", api, { status: "ready", companyId: "other-company" }); wrong.render(); await tick();
  assert.ok(!walk(wrong.render()).some(n => n.type === "EmployeeEditDrawer"));
});

test("allowance refresh recovers failed load, uses the same authorization and checks exact browser receipt", async () => {
  let failRead = true, saveCount = 0, browserCount = 0, saved;
  const value = { authorization_ref: "original-auth", revision: "r1", used_calls: 1, remaining_calls: 3, binding_options: [{ binding_ref: "b1", employee_name: "Writer", agent_name: "Local" }], policy: null };
  const api = { getAgentAllowanceCompanies: async () => ({ companies: [{ company_id: "co", name: "Test" }] }),
    getAgentAllowance: async () => { if (failRead) throw Error("load failed"); return value; },
    saveAgentAllowance: async (company, payload) => { assert.equal(company, "co"); saved = payload; saveCount++; throw Error("save unknown"); },
    controlAgentBrowser: async (company, binding, action) => { browserCount++; return { company_id: "wrong", binding_ref: binding, reason: "incorrect success" }; },
  };
  const h = scene("agent", api), render = () => h.render({}, "AgentAllowancePanel");
  render(); await tick(); render(); await tick(); let tree = render(); assert.match(textOf(tree), /load failed/);
  failRead = false; await button(tree, "读取当前许可").props.onClick(); tree = render();
  for (const node of walk(tree).filter(n => n.type === "input")) node.props.onChange({ target: { checked: true } }); tree = render();
  await button(tree, "确认许可").props.onClick(); tree = render();
  assert.equal(saved.authorization_ref, "original-auth"); assert.equal(saved.expected_revision, "r1"); assert.equal(JSON.stringify(saved.binding_refs), '["b1"]');
  assert.equal(button(tree, "确认许可").props.disabled, true); assert.equal(saveCount, 1);
  await button(tree, "读取当前许可").props.onClick(); tree = render();
  assert.match(textOf(tree), /已占用 1 次，剩余 3 次/); assert.equal(value.authorization_ref, "original-auth");
  await button(tree, "核对只读环境").props.onClick(); tree = render();
  assert.equal(browserCount, 1); assert.match(textOf(tree), /浏览器回执不属于当前员工/); assert.doesNotMatch(textOf(tree), /incorrect success/);
  assert.equal(button(tree, "停止准备窗口").props.disabled, false);
  assert.ok(!walk(tree).some(n => textOf(n) === "另行授权 4 次新调用"));
});

test("unlimited subscription use needs separate confirmation and keeps prior count visible", async () => {
  let sent;
  const bounded = { authorization_ref: "same-auth", revision: "r1", used_calls: 4, remaining_calls: 0,
    limit_mode: "FOUR_CALLS", binding_options: [{ binding_ref: "b1", employee_name: "Writer", agent_name: "Local" }], policy: null };
  const api = { getAgentAllowanceCompanies: async () => ({ companies: [{ company_id: "co", name: "Test" }] }),
    getAgentAllowance: async () => bounded,
    saveAgentAllowance: async (_company, payload) => { sent = payload; return { ...bounded, revision: "r2", limit_mode: "UNLIMITED", remaining_calls: null }; } };
  const h = scene("agent", api), render = () => h.render({}, "AgentAllowancePanel");
  render(); await tick(); render(); await tick(); let tree = render();
  let boxes = walk(tree).filter(n => n.type === "input" && n.props.type === "checkbox");
  boxes[0].props.onChange({ target: { checked: true } });
  boxes[1].props.onChange({ target: { checked: true } }); tree = render();
  assert.equal(button(tree, "确认许可").props.disabled, true);
  boxes = walk(tree).filter(n => n.type === "input" && n.props.type === "checkbox");
  boxes[2].props.onChange({ target: { checked: true } }); tree = render();
  assert.equal(button(tree, "确认许可").props.disabled, false);
  await button(tree, "确认许可").props.onClick(); tree = render();
  assert.equal(sent.unlimited_consent, true); assert.equal(sent.authorization_ref, "same-auth");
  assert.match(textOf(tree), /不设调用次数上限/); assert.match(textOf(tree), /已占用 4 次/);
  assert.doesNotMatch(textOf(tree), /剩余 null/);
});

test("pinned complete Skill preview requires explicit license consent before install", async () => {
  let installed, result;
  const pin = "d9a78aed47874459ae1e44523a597e42dd9acf99";
  const api = { previewSkillPackage: async source => ({ ...source, repo_url: "https://github.com/Tencent/BrowserSkill", commit: pin, subdirectory: "crates/bsk-cli/skill", package_sha256: "fixed-package", license_text: "MIT", files: [{ path: "SKILL.md", bytes: 15 }, { path: "references/help.md", bytes: 20 }] }),
    installSkillPackage: async payload => { installed = payload; return { skill_template_id: "pinned-skill" }; } };
  const h = scene("talent", api), props = { onInstalled: value => { result = value; } }, render = () => h.render(props, "RepositorySkillImport");
  let tree = render();
  walk(tree).find(n => n.props["aria-label"] === "技能链接").props.onChange({ target: { value: "https://github.com/Tencent/BrowserSkill" } }); tree = render();
  assert.equal(walk(tree).some(n => ["技能固定版本", "技能目录"].includes(n.props?.["aria-label"])), false);
  await button(tree, "识别技能").props.onClick(); tree = render();
  assert.equal(button(tree, "安装技能").props.disabled, true); assert.match(textOf(tree), /2 个完整文件/);
  walk(tree).find(n => n.type === "input" && n.props.type === "checkbox").props.onChange({ target: { checked: true } }); tree = render();
  await button(tree, "安装技能").props.onClick();
  assert.equal(installed.commit, pin); assert.equal(installed.expected_package_sha256, "fixed-package"); assert.equal(installed.license_accepted, true); assert.equal(result.skill_template_id, "pinned-skill");
});

test("late allowance reads cannot replace the latest company or refresh, browser prepare and stop stay scoped", async () => {
  let releaseOld, reads = 0;
  const actions = [];
  const value = { authorization_ref: "same-auth", revision: "latest", used_calls: 2, remaining_calls: 2,
    binding_options: [{ binding_ref: "b1", employee_name: "Writer", agent_name: "Local" }], policy: null };
  const api = { getAgentAllowanceCompanies: async () => ({ companies: [{ company_id: "co", name: "Test" }, { company_id: "other", name: "Other" }] }),
    getAgentAllowance: async company => { reads++; if (reads === 1) return new Promise(resolve => { releaseOld = resolve; }); return { ...value, reason: company }; },
    controlAgentBrowser: async (company, binding, action) => { actions.push({ company, binding, action }); return { company_id: company, binding_ref: binding, state: action === "stop" ? "STOPPED" : "UNAVAILABLE", reason: action || "checked" }; } };
  const h = scene("agent", api), render = () => h.render({}, "AgentAllowancePanel");
  render(); await tick(); let tree = render();
  walk(tree).find(n => n.type === "select").props.onChange({ target: { value: "co" } }); render();
  await button(render(), "读取当前许可").props.onClick();
  releaseOld({ ...value, used_calls: 0, remaining_calls: 4, reason: "stale" }); await tick(); tree = render();
  assert.match(textOf(tree), /已占用 2 次，剩余 2 次/); assert.doesNotMatch(textOf(tree), /stale/);
  await button(tree, "准备公开网页只读").props.onClick(); tree = render();
  await button(tree, "核对只读环境").props.onClick(); tree = render();
  await button(tree, "停止准备窗口").props.onClick();
  assert.equal(JSON.stringify(actions), JSON.stringify(["prepare", "", "stop"].map(action => ({ company: "co", binding: "b1", action }))));
  tree = render(); walk(tree).find(n => n.type === "select").props.onChange({ target: { value: "other" } }); render(); await tick(); tree = render();
  assert.match(textOf(tree), /other/); assert.doesNotMatch(textOf(tree), /checked/);
});


test("return context accepts only local Curis paths", () => {
  assert.equal(
    resolveTalentReturnPath({ returnTo: "/ceo-office/workspace?workspace_id=workspace-1" }),
    "/ceo-office/workspace?workspace_id=workspace-1",
  );
  assert.equal(resolveTalentReturnPath({ source: "organization" }), "/ceo-office/organization");
  assert.equal(resolveTalentReturnPath({ returnTo: "https://example.com" }), "");
  assert.equal(resolveTalentReturnPath({ returnTo: "//example.com/ceo-office" }), "");
  assert.equal(resolveTalentReturnPath({ returnTo: "/other-product" }), "");
});


test("assigning a Skill uses one server-side item mutation", async () => {
  const original = globalThis.fetch, calls = [];
  globalThis.fetch = async (url, options = {}) => { calls.push({ url, options }); return new Response(JSON.stringify({ bindings: [{ skill_template_id: "old" }, { skill_template_id: "new" }] }), { status: 200, headers: { "Content-Type": "application/json" } }); };
  try { const result = await assignSkill("employee-1", "new"); assert.equal(calls.length, 1); assert.equal(calls[0].options.method, "POST"); assert.match(calls[0].url, /employees\/employee-1\/skills\/new$/); assert.equal(calls[0].options.body, undefined); assert.equal(result.bindings.length, 2); }
  finally { globalThis.fetch = original; }
});


test("Talent surface uses product language and keeps internal catalog terms out of the main path", async () => {
  const source = await (await import("node:fs/promises")).readFile(
    new URL("../app/ceo-office/talent-market/page.js", import.meta.url),
    "utf8",
  );
  assert.match(source, /人才与能力/);
  assert.match(source, /可招聘与准备中/);
  assert.match(source, /公司员工/);
  assert.match(source, /返回原来的工作位置/);
  assert.doesNotMatch(source, /Candidate ·/);
  assert.doesNotMatch(source, /Tool \/ MCP/);
  assert.doesNotMatch(source, /来源路径：/);
  assert.doesNotMatch(source, /Curis-ready/);
  assert.doesNotMatch(source, /Mock ·/);
  assert.match(source, /能力类型/);
  assert.match(source, /TerraPaneContent/);
  assert.match(source, /utilityRequestTabId="current"/);
  assert.match(source, /repeat\(auto-fill,minmax\(min\(100%,300px\),1fr\)\)/);
  assert.match(source, /companyEmployees: next.companyEmployees.filter/);
});

const permissionState = (enabled = false) => ({ company_id: "co", employee_id: "employee-1",
  manageable: true, enabled, can_revoke: true, effective_classes: enabled ? ["exec"] : [], revision: "a".repeat(64) });
const executionChoice = tree => walk(tree).find(n => n.props?.["aria-label"] === "允许此员工使用执行类能力");
const agentChoice = tree => walk(tree).find(n => n.type === "input" && n.props.type === "checkbox" && !n.props["aria-label"]);
const editFixture = permission => ({ open: true, employee: { id: "employee-1", company_id: "co", name: "专业员工", status: "idle" },
  bindings: [], capabilities: [{ source: "tenant_private", capability_type: "agent", capability_id: "agent.local", label: "Local Agent", enabled: true }],
  executionPermission: permission });

test("canonical parent passes permission; explicit consent and profile go to the same request", async () => {
  const permission = permissionState(), calls = [];
  const employee = editFixture(permission).employee;
  const api = {
    getEmployee: async () => employee, getDepartments: async () => ({}), getEmployeeTemplates: async () => ({}),
    getEmployeeSkills: async () => ({}), getEmployeeTools: async () => ({}),
    getCapabilitySelector: async () => ({ capabilities: editFixture(permission).capabilities }),
    getEmployeeCapabilities: async () => ({ employee_id: employee.id, bindings: [], execution_permission: permission }),
    getOrganizationProjection: async () => ({ company: { company_id: "co" } }),
    setEmployeeCapabilities: async (id, bindings, consent) => {
      calls.push({ id, bindings, consent });
      return { employee_id: id, bindings, execution_permission: { ...permission, enabled: consent.enabled } };
    },
  };
  const parent = scene("employee", api); parent.render(); await tick();
  let tree = parent.render(); await button(tree, "编辑员工").props.onClick(); tree = parent.render();
  const props = walk(tree).find(n => n.type === "EmployeeEditDrawer").props;
  assert.equal(props.executionPermission, permission);
  const edit = scene("edit", api); edit.render(props); tree = edit.render(props);
  assert.equal(executionChoice(tree).props.checked, false);
  agentChoice(tree).props.onChange(); tree = edit.render(props);
  await walk(tree).find(n => n.type === "form").props.onSubmit({ preventDefault() {} });
  assert.equal(calls.length, 0);
  tree = edit.render(props); assert.match(textOf(tree), /请先明确允许/);
  executionChoice(tree).props.onChange({ target: { checked: true } }); tree = edit.render(props);
  const submit = walk(tree).find(n => n.type === "form").props.onSubmit;
  await Promise.all([submit({ preventDefault() {} }), submit({ preventDefault() {} })]);
  assert.equal(calls.length, 1);
  assert.equal(calls[0].consent.enabled, true);
  assert.equal(calls[0].consent.company_id, "co");
  assert.equal(calls[0].consent.expected_revision, permission.revision);
  assert.equal(calls[0].bindings[0].capability_id, "agent.local");
});

test("lost authorization response only permits scoped readback, never repeats the mutation", async () => {
  const permission = permissionState(), props = editFixture(permission);
  let count = 0, current, accepted;
  props.onSuccess = (saved, profile, options) => { accepted = { saved, profile, options }; };
  const api = {
    setEmployeeCapabilities: async (id, bindings, consent) => {
      count++; current = { employee_id: id, bindings, execution_permission: { ...permission, enabled: consent.enabled } };
      throw Error("response lost");
    },
    getEmployee: async () => props.employee, getEmployeeCapabilities: async () => current,
  };
  const h = scene("edit", api); h.render(props); let tree = h.render(props);
  agentChoice(tree).props.onChange();
  executionChoice(tree).props.onChange({ target: { checked: true } }); tree = h.render(props);
  await walk(tree).find(n => n.type === "form").props.onSubmit({ preventDefault() {} }); tree = h.render(props);
  assert.equal(button(tree, "保存员工").props.disabled, true);
  await walk(tree).find(n => n.type === "form").props.onSubmit({ preventDefault() {} });
  assert.equal(count, 1);
  await button(tree, "读取当前员工配置").props.onClick();
  assert.equal(count, 1); assert.equal(accepted.options.readback, true);
  assert.equal(accepted.profile.execution_permission.enabled, true);
});

test("revoke is explicit, includes the current revision, and template inheritance cannot pretend to revoke", async () => {
  for (const canRevoke of [true, false]) {
    const permission = { ...permissionState(true), can_revoke: canRevoke }, props = editFixture(permission);
    props.bindings = [{ capability_source: "tenant_private", capability_type: "agent", capability_id: "agent.local", priority: 80, enabled: true }];
    let request;
    const h = scene("edit", { setEmployeeCapabilities: async (id, bindings, consent) => {
      request = consent; return { employee_id: id, bindings: [], execution_permission: { ...permission, enabled: false } };
    } });
    h.render(props); let tree = h.render(props);
    executionChoice(tree).props.onChange({ target: { checked: false } }); tree = h.render(props);
    assert.match(textOf(tree), /移除已绑定的执行类能力/);
    await walk(tree).find(n => n.type === "form").props.onSubmit({ preventDefault() {} });
    if (canRevoke) { assert.equal(request.enabled, false); assert.equal(request.expected_revision, permission.revision); }
    else { assert.equal(request, undefined); assert.match(textOf(h.render(props)), /岗位模板仍授予执行许可/); }
  }
});

test("stale employee response cannot accept a different Company or survive scope change", async () => {
  const props = editFixture(permissionState()), hCalls = [];
  let finish;
  const h = scene("edit", { setEmployeeCapabilities: (id, bindings) => new Promise(resolve => { finish = () => resolve({
    employee_id: id, bindings, execution_permission: permissionState(true) }); }) });
  props.onSuccess = () => hCalls.push("success");
  h.render(props); let tree = h.render(props);
  agentChoice(tree).props.onChange(); executionChoice(tree).props.onChange({ target: { checked: true } });
  tree = h.render(props);
  const pending = walk(tree).find(n => n.type === "form").props.onSubmit({ preventDefault() {} });
  h.render({ ...props, employee: { ...props.employee, id: "other", company_id: "other-company" } });
  finish(); await pending; assert.deepEqual(hCalls, []);
});

test("production API serializes optional explicit permission without inventing a grant", async () => {
  const source = readFileSync(new URL("../lib/api.js", import.meta.url), "utf8");
  const start = source.indexOf("export const setEmployeeCapabilities");
  const end = source.indexOf("export const getCapabilitySelector", start);
  const code = source.slice(start, end).replace("export const setEmployeeCapabilities =", "globalThis.setEmployeeCapabilities =");
  const calls = [], context = { JSON, workspaceFetch: async (...args) => calls.push(args) };
  vm.runInNewContext(code, context);
  await context.setEmployeeCapabilities("employee-1", []);
  assert.deepEqual(JSON.parse(calls[0][1].body), { bindings: [] });
  const permission = { company_id: "co", expected_revision: "a".repeat(64), enabled: false };
  await context.setEmployeeCapabilities("employee-1", [], permission);
  assert.deepEqual(JSON.parse(calls[1][1].body), { bindings: [], execution_permission: permission });
});

test("unknown save can close; reopening refreshes server truth and cannot replay the old request", async () => {
  let permission = permissionState(), bindings = [], saves = 0, reads = 0;
  const employee = editFixture(permission).employee;
  const api = {
    getEmployee: async () => employee, getDepartments: async () => ({}), getEmployeeTemplates: async () => ({}),
    getEmployeeSkills: async () => ({}), getEmployeeTools: async () => ({}),
    getCapabilitySelector: async () => ({ capabilities: editFixture(permission).capabilities }),
    getOrganizationProjection: async () => ({ company: { company_id: "co" } }),
    getEmployeeCapabilities: async () => { reads++; return { employee_id: employee.id, bindings, execution_permission: permission }; },
    setEmployeeCapabilities: async (id, next) => { saves++; bindings = next; permission = permissionState(true); throw Error("lost"); },
  };
  const parent = scene("employee", api); parent.render(); await tick();
  let tree = parent.render(); await button(tree, "编辑员工").props.onClick(); tree = parent.render();
  const props = walk(tree).find(n => n.type === "EmployeeEditDrawer").props;
  const edit = scene("edit", { ...api, getEmployeeCapabilities: async () => { throw Error("offline"); } });
  edit.render(props); tree = edit.render(props);
  agentChoice(tree).props.onChange(); executionChoice(tree).props.onChange({ target: { checked: true } });
  tree = edit.render(props);
  await walk(tree).find(n => n.type === "form").props.onSubmit({ preventDefault() {} }); tree = edit.render(props);
  await button(tree, "读取当前员工配置").props.onClick(); tree = edit.render(props);
  assert.equal(button(tree, "保存员工").props.disabled, true);
  assert.equal(button(tree, "关闭并稍后核对").props.disabled, false);
  button(tree, "关闭并稍后核对").props.onClick(); tree = parent.render();
  assert.match(textOf(tree), /保存结果尚未确认/);
  assert.equal(walk(tree).find(n => n.type === "EmployeeEditDrawer").props.open, false);
  const priorReads = reads; await button(tree, "编辑员工").props.onClick(); tree = parent.render();
  const current = walk(tree).find(n => n.type === "EmployeeEditDrawer").props;
  assert.ok(reads > priorReads); assert.equal(current.executionPermission.enabled, true);
  assert.equal(current.bindings.length, 1); assert.equal(saves, 1);
});

const skillMarketData = skills => ({
  companies: [{ company_id: "co" }], departments: [], employees: [{ id: "employee-1", company_id: "co", name: "专业员工" }],
  companyEmployees: [], experts: [], expertCategories: [], connectors: [], skills,
});
const packageSkill = () => ({ skill_template_id: "skill-fixed-package", name: "skill", source: "tenant_private",
  package: { repo_url: "https://github.com/Tencent/BrowserSkill", subdirectory: "crates/bsk-cli/skill",
    commit: "d9a78aed47874459ae1e44523a597e42dd9acf99", package_sha256: "fixed-fixture-package" } });
const skillTab = tree => walk(tree).find(n => n.type === "button" && textOf(n).startsWith("技能"));
const repositoryForm = tree => walk(tree).find(n => typeof n.type === "function" && n.type.name === "RepositorySkillImport");
const skillCards = tree => walk(tree).filter(n => typeof n.type === "function" && n.type.name === "SearchResultCard");
const talentPane = tree => walk(tree).find(n => n.type === "TerraPaneContent");

test("repository Skill remains canonical but displays/searches source and installation opens the assignment Inspector", async () => {
  const installed = packageSkill(), original = JSON.stringify(installed), assignments = [];
  let skills = [];
  const api = { productStateFor, resolveTalentReturnPath, getTalentMarketData: async () => skillMarketData(skills),
    assignSkill: async (...args) => assignments.push(args) };
  const h = scene("talent", api), props = { companyId: "co" };
  h.render(props, "TalentMarketSurface"); await tick(); let tree = h.render(props, "TalentMarketSurface");
  skillTab(tree).props.onClick(); tree = h.render(props, "TalentMarketSurface");
  walk(tree).find(n => n.type === "TerraSearch").props.onChange("unrelated-filter"); tree = h.render(props, "TalentMarketSurface");
  assert.equal(skillCards(tree).length, 0);
  const priorRequest = talentPane(tree).props.utilityRequestKey;
  skills = [installed];
  await repositoryForm(tree).props.onInstalled({ ...installed }); tree = h.render(props, "TalentMarketSurface");
  assert.equal(walk(tree).find(n => n.type === "TerraSearch").props.value, "");
  assert.equal(skillCards(tree).length, 1);
  const pane = talentPane(tree);
  assert.ok(pane.props.utilityRequestKey > priorRequest);
  const inspector = pane.props.utilityPane.props.children;
  assert.equal(inspector.props.selected.item, installed);
  const detail = inspector.type(inspector.props);
  assert.match(textOf(detail), /BrowserSkill/);
  await walk(detail).find(n => n.props.id === "talent-skill-employee").props.onChange({ target: { value: "employee-1" } });
  assert.deepEqual(assignments, [["employee-1", installed.skill_template_id]]);
  for (const query of ["Browser", "crates/bsk-cli/skill"]) {
    walk(tree).find(n => n.type === "TerraSearch").props.onChange(query); tree = h.render(props, "TalentMarketSurface");
    assert.equal(skillCards(tree).length, 1);
    const card = skillCards(tree)[0];
    assert.match(textOf(card.type(card.props)), /BrowserSkill/);
  }
  assert.equal(JSON.stringify(installed), original); // No rename or manifest mutation.
});

test("installed Skill requires a unique refreshed canonical identity and matching package readback", async () => {
  for (const variant of ["missing", "duplicate", "changed"]) {
    const installed = packageSkill();
    let skills = [];
    const h = scene("talent", { productStateFor, resolveTalentReturnPath,
      getTalentMarketData: async () => skillMarketData(skills) });
    const props = { companyId: "co" };
    h.render(props, "TalentMarketSurface"); await tick(); let tree = h.render(props, "TalentMarketSurface");
    skillTab(tree).props.onClick(); tree = h.render(props, "TalentMarketSurface");
    skills = variant === "missing" ? [] : variant === "duplicate" ? [installed, { ...installed }]
      : [{ ...installed, package: { ...installed.package, package_sha256: "other" } }];
    await repositoryForm(tree).props.onInstalled(installed); tree = h.render(props, "TalentMarketSurface");
    assert.equal(talentPane(tree).props.utilityPane, null);
    assert.match(textOf(tree), /不要重复安装/);
  }
});

test("late installed Skill refresh cannot select or open Inspector in a new Company", async () => {
  const installed = packageSkill(); let reads = 0, finish;
  const h = scene("talent", { productStateFor, resolveTalentReturnPath, getTalentMarketData: async () => {
    reads++; if (reads === 2) return new Promise(resolve => { finish = resolve; });
    return skillMarketData([]);
  } });
  const props = { companyId: "co" };
  h.render(props, "TalentMarketSurface"); await tick(); let tree = h.render(props, "TalentMarketSurface");
  skillTab(tree).props.onClick(); tree = h.render(props, "TalentMarketSurface");
  const pending = repositoryForm(tree).props.onInstalled(installed);
  h.render({ companyId: "other" }, "TalentMarketSurface"); await tick();
  finish(skillMarketData([installed])); await pending;
  tree = h.render({ companyId: "other" }, "TalentMarketSurface");
  assert.equal(talentPane(tree).props.utilityPane, null);
  assert.equal(talentPane(tree).props.utilityRequestKey, 0);
});

test("unverified legacy browser state is never shown as ready", async () => {
  const value = { authorization_ref:"auth", revision:"r", used_calls:1, remaining_calls:3,
    binding_options:[{binding_ref:"b1",employee_name:"Writer",agent_name:"Local"}], policy:null };
  const api = {getAgentAllowanceCompanies:async()=>({companies:[{company_id:"co",name:"Test"}]}),
    getAgentAllowance:async()=>value,
    controlAgentBrowser:async()=>({company_id:"co",binding_ref:"b1",state:"CONNECTED",reason:"old browser ready"})};
  const h=scene("agent",api), render=()=>h.render({},"AgentAllowancePanel");
  render(); await tick(); let tree=render();
  walk(tree).find(n=>n.type==="select").props.onChange({target:{value:"co"}}); render();
  await button(render(),"读取当前许可").props.onClick(); tree=render();
  await button(tree,"核对只读环境").props.onClick(); tree=render();
  assert.match(textOf(tree), /尚未核验/); assert.doesNotMatch(textOf(tree), /old browser ready/);
});


test("ACP allowance uses an explicit separate grant and never calls Codex auth", async () => {
  const codex = { agent_kind: "codex-cli", agent_id: "codex" };
  const acp = { agent_kind: "acp-stdio", agent_id: "deepseek_harness", installation_ref: "a".repeat(64) };
  let creates = 0, authReads = 0;
  let value = { authorization_ref: "old-codex", authorization_subject: codex, revision: "r1", used_calls: 2, remaining_calls: 2,
    binding_options: [{ binding_ref: "dsh", employee_name: "Writer", agent_name: "DSH", agent_kind: "acp-stdio", authorization_subject: acp }], policy: null };
  const h = scene("agent", {
    getAgentAllowanceCompanies: async () => ({ companies: [{ company_id: "co", name: "Company" }] }),
    getAgentAllowance: async () => value,
    getAgentCodexAuth: async () => { authReads++; throw Error("wrong auth"); },
    saveAgentAllowance: async () => { throw Error("must not reuse old grant"); },
    createAgentAuthorization: async (_company, payload) => {
      creates++; assert.equal(payload.previous_authorization_ref, "old-codex"); assert.equal(payload.consent, true);
      assert.equal(JSON.stringify(payload.binding_refs), '["dsh"]');
      value = { ...value, authorization_ref: "new-acp", authorization_subject: acp, revision: "r2", used_calls: 0, remaining_calls: 4,
        policy: { enabled: true, bindings: [{ binding_ref: "dsh" }] } };
      throw Error("response lost");
    },
  });
  const render = () => h.render({}, "AgentAllowancePanel");
  render(); await tick(); render(); await tick(); let tree = render();
  assert.equal(authReads, 0); assert.doesNotMatch(textOf(tree), /读取 Codex 连接|登录 Codex|准备公开网页只读/);
  walk(tree).find(node => node.type === "input" && node.props.type === "checkbox").props.onChange({ target: { checked: true } }); tree = render();
  const consent = walk(tree).find(node => node.type === "label" && textOf(node).includes("我确认以上范围"));
  walk(consent).find(node => node.type === "input").props.onChange({ target: { checked: true } }); tree = render();
  assert.equal(button(tree, "确认许可").props.disabled, true);
  assert.match(textOf(tree), /旧授权与用量保留/);
  await button(tree, "另行授权 4 次新调用").props.onClick(); tree = render();
  assert.equal(creates, 1); assert.equal(button(tree, "另行授权 4 次新调用").props.disabled, true);
  await button(tree, "读取当前许可").props.onClick(); tree = render();
  assert.equal(creates, 1); assert.match(textOf(tree), /已占用 0 次，剩余 4 次/); assert.equal(authReads, 0);
});


test("Skill link choices use pinned server source and preserve readable selection", async () => {
  let chosen;
  const pin = "a".repeat(40);
  const api = { previewSkillPackage: async input => {
    chosen = input;
    return input.subdirectory ? { repo_url: "https://github.com/a/b", commit: pin, subdirectory: input.subdirectory, files: [], license_text: "MIT", package_sha256: "hash" }
      : { selection_required: true, repo_url: "https://github.com/a/b", commit: pin, choices: [{ name: "Research", directory: "skills/research" }] };
  } };
  const h = scene("talent", api), props = { onInstalled: () => {} }, render = () => h.render(props, "RepositorySkillImport");
  let tree = render(); walk(tree).find(n => n.props["aria-label"] === "技能链接").props.onChange({ target: { value: "https://github.com/a/b" } });
  await button(render(), "识别技能").props.onClick(); await button(render(), "Research").props.onClick();
  assert.deepEqual(JSON.parse(JSON.stringify(chosen)), { repo_url: "https://github.com/a/b", commit: pin, subdirectory: "skills/research" });
});

test("Skill unbind and library removal are separate item endpoints", async () => {
  const original = globalThis.fetch, calls = [];
  globalThis.fetch = async (url, options = {}) => { calls.push({ url, options }); return new Response("{}", { status: 200, headers: { "Content-Type": "application/json" } }); };
  try {
    await unassignSkill("employee-1", "new"); assert.equal(calls.length, 1); assert.equal(calls[0].options.method, "DELETE"); assert.equal(calls[0].options.body, undefined); assert.match(calls[0].url, /employees\/employee-1\/skills\/new$/);
    await removeSkill("new", "company"); assert.equal(calls[1].options.method, "DELETE"); assert.match(calls[1].url, /skills\/templates\/new\?company_id=company$/);
  } finally { globalThis.fetch = original; }
});


test("installed Skill Inspector shows pending dependencies and explicit unbind/removal", async () => {
  const actions = [], item = { ...packageSkill(), dependency_status: { ready: false, preparation: "existing_browser_connection", message: "官方连接尚未准备" } };
  const h = scene("talent", { productStateFor }), props = { selected: { kind: "skills", item }, data: { employees: [{ id: "employee-1", name: "Alice" }] }, assignments: [{ id: "employee-1", name: "Alice" }],
    onUnassign: id => actions.push(id), onRemove: () => actions.push("remove"), onAssign: () => {}, busy: false };
  const tree = h.render(props, "Inspector");
  assert.match(textOf(tree), /官方连接尚未准备/);
  button(tree, "解除与Alice的绑定").props.onClick(); button(tree, "从公司移除技能").props.onClick();
  assert.deepEqual(actions, ["employee-1", "remove"]);
  assert.ok(walk(tree).some(n => n.type === "a" && n.props.href === "/ceo-office/capabilities#employee-agents"));
});

test("binding mutations never GET or PUT a stale full list", async () => {
  const original = globalThis.fetch, methods = [];
  globalThis.fetch = async (_, options = {}) => { methods.push(options.method); assert.ok(["POST", "DELETE"].includes(options.method)); return new Response("{}", { status: 200, headers: { "Content-Type": "application/json" } }); };
  try { await assignSkill("employee", "new"); await unassignSkill("employee", "old"); assert.deepEqual(methods, ["POST", "DELETE"]); }
  finally { globalThis.fetch = original; }
});


for (const [name, rows, expected, forbidden] of [
  ["unknown", [{ currency: "USD", known_cost: null, unknown_cost_count: 1 }], /1 次费用未知/, /0\.0000/],
  ["zero", [{ currency: "USD", known_cost: 0, unknown_cost_count: 0 }], /0\.0000 USD/, /费用未知/],
  ["partial", [{ currency: "USD", known_cost: 1.25, unknown_cost_count: 2 }], /已知部分 1\.2500 USD；2 次费用未知/, /3\.2500/],
  ["currencies", [{ currency: "EUR", known_cost: 2, unknown_cost_count: 0 }, { currency: "USD", known_cost: 1, unknown_cost_count: 0 }], /2\.0000 EUR；1\.0000 USD/, /3\.0000/],
  ["empty", [], /未记录/, /0\.0000/],
]) {
  test(`actual usage and capability consumers preserve ${name} money facts`, async () => {
    const facts = { total_tokens: 2, total_cost: null, estimated_cost: null,
      event_count: rows.length ? 2 : 0, usage_event_count: rows.length ? 2 : 0, cost_by_currency: rows };
    const summary = { totals: facts, by_model: [{ model_name: "fixture", ...facts }],
      by_capability_source: [], by_employee: [], by_workflow: [] };
    const dashboard = scene("usage");
    const props = { apiFetch: async () => summary, onMessage() {} };
    assert.match(textOf(dashboard.render(props)), /尚未读取/);
    await tick();
    const tree = dashboard.render(props);
    assert.match(textOf(tree), expected); assert.doesNotMatch(textOf(tree), forbidden);
    const tableNode = walk(tree).find(node => typeof node.type === "function" && node.type.name === "DimensionTable" && node.props.title.includes("by_model"));
    assert.ok(tableNode);
    const tableText = textOf(tableNode.type(tableNode.props));
    assert.match(tableText, expected); assert.doesNotMatch(tableText, forbidden);
    const detail = scene("detail", {
      getCapability: async () => ({ type: "model", capability_key: "fixture", name: "Fixture", gateway_ref: "gw", model_name: "fixture", status: "active" }),
      getModelGatewaySummary: async () => ({ providers: [], usage: { by_model: [{ ...facts, model_gateway_id: "gw", model_name: "fixture" }] } }),
    });
    detail.render(); await tick();
    const detailText = textOf(detail.render());
    assert.match(detailText, expected);
    // The explanatory copy mentions unknown costs; inspect the actual cost value only.
    const label = walk(detail.render()).find(node => node.type === "dt" && textOf(node) === "成本");
    assert.ok(label);
    // Each render produces new React elements; find the matching container by its label.
    const container = walk(detail.render()).find(node => node.type === "div" && Array.isArray(node.props.children)
      && node.props.children.some(child => child?.type === "dt" && textOf(child) === "成本"));
    assert.ok(container);
    assert.doesNotMatch(textOf(container), forbidden);
  });
}
