// T-016: front-end display of "价格待核实" (price_status=VERIFICATION_REQUIRED).
// Field names/values come from backend CompanyExecutionPolicy.options()/read():
//   price_status "CURRENT" | "VERIFICATION_REQUIRED", price_notice, per_request_ceiling_cny (string | null),
//   policy.execution_state "AWAITING_PRICE_VERIFICATION".
// All rendering is done with the REAL components compiled by swc and fixture-only APIs (no network / backend).
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import vm from "node:vm";

const require = createRequire(import.meta.url);
const swc = require("next/dist/build/swc");
await swc.loadBindings();
const read = (p) => readFileSync(new URL(`../${p}`, import.meta.url), "utf8");

async function compile(file, filename) {
  const { code } = await swc.transform(read(file), {
    filename, isModule: true,
    jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } },
    module: { type: "commonjs" },
  });
  return code;
}

const settingsCode = await compile("app/ceo-office/settings/page.js", "settings.js");
const employeeCode = await compile("components/v1/EmployeeConversation.js", "employee.js");

const text = (n) => typeof n === "string" ? n : Array.isArray(n) ? n.map(text).join("")
  : n?.props ? text(n.props.children) : "";
const nodes = (root, predicate) => {
  const result = [];
  const walk = (n) => {
    if (!n || typeof n !== "object") return;
    if (Array.isArray(n)) { n.forEach(walk); return; }
    if (predicate(n)) result.push(n);
    walk(n.props?.children);
  };
  walk(root);
  return result;
};
const same = (a, b) => a && b && a.length === b.length && a.every((v, i) => Object.is(v, b[i]));

// ---- Fixtures: the real `read()` view shape ---------------------------------
const FUTURE = () => new Date(Date.now() + 60 * 60_000).toISOString();
const PRICE_NOTICE = "价格待核实：许可范围和预算已保存，但尚不能进行付费模型执行；" +
  "请由维护者更新经核验的价格依据后，重新核对并确认公司许可。原输入会保留，不会自动调用或计费。";

const baseView = () => ({
  company_id: "A", policy: null, preview_token: "preview",
  totals: { reserved_micro_cny: 0, estimated_micro_cny: 0 },
  workspaces: [{ workspace_id: "W", name: "写作工作空间" }],
  models: [{ model_key: "m", display_name: "DeepSeek", destination: "https://api.deepseek.com" }],
  price: { checked_at: "2026-11-05T11:52:26+00:00", valid_until: "2027-11-12T11:52:26+00:00",
    input_cny_per_million: 2, output_cny_per_million: 8,
    source_cny: "https://api-docs.deepseek.com/zh-cn/quick_start/pricing/" },
  max_input_bytes: 16384, max_output_tokens: 2048,
});
const currentView = () => ({ ...baseView(), price_status: "CURRENT", price_notice: "", per_request_ceiling_cny: "0.049664" });
// VERIFICATION_REQUIRED uses the shipped, expired price evidence (T-014): valid_until in the past.
const pendingView = () => ({ ...baseView(),
  price: { ...baseView().price, checked_at: "2026-11-05T11:52:26+00:00", valid_until: "2026-11-12T11:52:26+00:00" },
  price_status: "VERIFICATION_REQUIRED", price_notice: PRICE_NOTICE, per_request_ceiling_cny: null });
// A saved pending license (enabled=true, execution_state=AWAITING_PRICE_VERIFICATION) is the
// real T-014 state the execution entry consumes; CompanyTextConsent only needs the top-level fields.
const pendingExecutionView = () => ({ ...pendingView(),
  policy: { enabled: true, expires_at: FUTURE(), execution_state: "AWAITING_PRICE_VERIFICATION",
    workspace_ids: ["W"], models: [{ model_key: "m" }] } });

// ---- Settings page (CompanyTextConsent) real render ------------------------
function consentScene(view) {
  let cursor = 0, tree; const slots = [], effects = [];
  const hooks = {
    useState(initial) { const i = cursor++; if (!(i in slots)) slots[i] = { value: typeof initial === "function" ? initial() : initial }; return [slots[i].value, (v) => { slots[i].value = typeof v === "function" ? v(slots[i].value) : v; }]; },
    useRef(initial) { const i = cursor++; return slots[i] ||= { current: initial }; },
    useEffect(fn, deps) { const i = cursor++, old = slots[i]; if (!old || !same(old.deps, deps)) { slots[i] = { deps }; effects.push(() => { old?.cleanup?.(); slots[i].cleanup = fn(); }); } },
    useLayoutEffect(fn, deps) { hooks.useEffect(fn, deps); },
  };
  const api = { getCompanyTextPolicy: async () => structuredClone(view), saveCompanyTextPolicy: async () => ({ policy: {} }) };
  const module = { exports: {} };
  vm.runInNewContext(settingsCode, {
    module, exports: module.exports, URLSearchParams, crypto: { randomUUID: () => "req" },
    setTimeout: () => 0, clearTimeout() {},
    require: (name) => name === "react" ? hooks : name === "react/jsx-runtime" ? require(name)
      : name.includes("v1FrontendApi") ? api : name.endsWith(".css") ? { __esModule: true, default: {} } : {},
  });
  const render = () => { cursor = 0; tree = module.exports.CompanyTextConsent({ companyId: "A" }); while (effects.length) effects.shift()(); return tree; };
  const flush = async () => { for (let i = 0; i < 6; i++) { render(); await new Promise((r) => setImmediate(r)); } return render(); };
  return { flush, nodes, text, get tree() { return tree; } };
}

test("T-016 设置页 有效态(price_status=CURRENT)：照常显示单次准入上限，不出现「价格待核实」", async () => {
  const scene = consentScene(currentView());
  const tree = await scene.flush();
  const body = scene.text(tree);
  assert.match(body, /单次准入上限 ¥0\.049664/);
  assert.doesNotMatch(body, /价格待核实/);
  assert.doesNotMatch(body, /¥null/);
});

test("T-016 设置页 待核实态(price_status=VERIFICATION_REQUIRED)：显示「价格待核实」与 price_notice；null 上限不崩、不显示为 0 元", async () => {
  const scene = consentScene(pendingView());
  const tree = await scene.flush();
  const body = scene.text(tree);
  assert.ok(tree, "component renders without throwing when per_request_ceiling_cny is null");
  assert.match(body, /价格待核实/);
  assert.match(body, /尚不能进行付费模型执行/);
  assert.match(body, /原输入会保留/);
  assert.doesNotMatch(body, /¥null/, "null ceiling is not rendered as ¥null");
  const ceilingPara = scene.nodes(tree, (n) => n.type === "p" && scene.text(n).includes("每次完整文字输入最多"))[0];
  assert.ok(ceilingPara);
  const ceilingText = scene.text(ceilingPara);
  assert.match(ceilingText, /暂无经核验的单次准入上限/);
  assert.doesNotMatch(ceilingText, /0 元|¥0/, "null ceiling is not shown as 0 元 / ¥0");
});

// ---- Execution entry (companyTextPermission + real component) --------------
function loadCheck() {
  const module = { exports: {} };
  vm.runInNewContext(employeeCode, { module, exports: module.exports, require: () => ({}) });
  return module.exports.companyTextPermission;
}
const check = loadCheck();

test("T-016 执行入口 待核实态：companyTextPermission 拦截付费执行并给出明确说明、承诺保留输入", () => {
  const snapshot = { company_id: "A", price_status: "VERIFICATION_REQUIRED", price_notice: PRICE_NOTICE,
    per_request_ceiling_cny: null,
    policy: { enabled: true, expires_at: FUTURE(), execution_state: "AWAITING_PRICE_VERIFICATION",
      workspace_ids: ["W"], models: [{ model_key: "m" }] } };
  const permit = check(snapshot, "A", "W", "m", Date.now());
  assert.equal(permit.blocked, true, "paid execution must be blocked while price is unverified");
  assert.equal(permit.pricePending, true);
  assert.match(permit.message, /价格待核实/);
  assert.match(permit.message, /尚不能进行付费模型执行/);
  assert.match(permit.message, /原输入会保留|输入已保留/);
});

test("T-016 执行入口 待核实许可(execution_state=AWAITING_PRICE_VERIFICATION)：同样拦截", () => {
  const snapshot = { company_id: "A", price_notice: PRICE_NOTICE,
    policy: { enabled: true, expires_at: FUTURE(), execution_state: "AWAITING_PRICE_VERIFICATION",
      workspace_ids: ["W"], models: [{ model_key: "m" }] } };
  const permit = check(snapshot, "A", "W", "m", Date.now());
  assert.equal(permit.blocked, true);
  assert.match(permit.message, /价格待核实/);
});

test("T-016 执行入口 有效态(price_status=CURRENT)：companyTextPermission 照常放行", () => {
  const snapshot = { company_id: "A", price_status: "CURRENT", price_notice: "", per_request_ceiling_cny: "0.049664",
    policy: { enabled: true, expires_at: FUTURE(), workspace_ids: ["W"], models: [{ model_key: "m" }] } };
  const permit = check(snapshot, "A", "W", "m", Date.now());
  assert.equal(permit.blocked, false);
  assert.notEqual(permit.pricePending, true);
  assert.equal(permit.message, "");
});

function executionScene(policyView) {
  const storage = new Map(), opens = [], sends = [];
  let cursor = 0, tree; const slots = [], effects = [];
  const conversationView = {
    tenant_id: "T", company_id: "A", owner_ref: "e", employee: { id: "e" },
    conversation_id: "c", discussion_scope: { workspace_id: "W", object_ref: null, assignment_ref: "a" },
    assignments: [{ assignment_ref: "a", workspace_id: "W", responsibility: "章节创作" }],
    execution_models: [{ source: "official", model_key: "m", binding_id: "b", display_name: "DeepSeek" }],
    model_preference: { model_key: "m" },
    execution_readiness: [{ assignment_ref: "a", status: "AVAILABLE", company_text: true }],
    messages: [], attempts: [],
  };
  const api = {
    getEmployeeConversation: async () => structuredClone(conversationView),
    getConversation: async () => structuredClone(conversationView),
    getEmployeeConversationReferences: async () => ({ references: [] }),
    getCompanyTextPolicy: async () => structuredClone(policyView),
    openEmployeeConversation: async () => { opens.push(1); },
    sendEmployeeConversation: async () => { sends.push(1); return structuredClone(conversationView); },
    sendConversation: async () => { sends.push(1); return structuredClone(conversationView); },
    receiveConversationResult: async () => ({}),
  };
  function ConversationComposer() {} function AgentWorkControl() {} function EmployeeAvatar() {} function ResultReferenceView() {}
  const hooks = {
    useState(initial) { const i = cursor++; if (!(i in slots)) slots[i] = { value: typeof initial === "function" ? initial() : initial }; return [slots[i].value, (v) => { slots[i].value = typeof v === "function" ? v(slots[i].value) : v; }]; },
    useRef(initial) { const i = cursor++; return slots[i] ||= { current: initial }; },
    useCallback(fn, deps) { const i = cursor++; if (!slots[i] || !same(slots[i].deps, deps)) slots[i] = { deps, value: fn }; return slots[i].value; },
    useEffect(fn, deps) { const i = cursor++, old = slots[i]; if (!old || !same(old.deps, deps)) { slots[i] = { deps }; effects.push(() => { old?.cleanup?.(); slots[i].cleanup = fn(); }); } },
    useLayoutEffect(fn, deps) { hooks.useEffect(fn, deps); },
  };
  const module = { exports: {} };
  vm.runInNewContext(employeeCode, {
    module, exports: module.exports, URLSearchParams, crypto: { randomUUID: () => "req" },
    window: { addEventListener() {}, removeEventListener() {} }, setInterval: () => 0, clearInterval() {},
    localStorage: { getItem: (k) => storage.get(k) || null, setItem: (k, v) => storage.set(k, v) },
    sessionStorage: { getItem: () => null, setItem() {}, removeItem() {} },
    require: (name) => name === "react" ? hooks : name === "react/jsx-runtime" ? require(name)
      : name.includes("SharedConversation") ? { ConversationComposer, AgentWorkControl }
        : name.includes("EmployeeAvatar") ? { EmployeeAvatar }
          : name.includes("ResultReferenceView") ? { __esModule: true, default: ResultReferenceView, resultSelection: () => ({}) }
            : name.includes("v1FrontendApi") ? api : {},
  });
  const props = { companyId: "A", employee: { id: "e", name: "员工" }, conversationId: null, active: true };
  const render = () => { cursor = 0; tree = module.exports.default(props); while (effects.length) effects.shift()(); return tree; };
  const flush = async () => { for (let i = 0; i < 10; i++) { render(); await new Promise((r) => setImmediate(r)); } return render(); };
  const composer = () => nodes(tree, (n) => n.type === ConversationComposer)[0];
  return {
    flush, text,
    get tree() { return tree; },
    get composerValue() { return composer()?.props.value; },
    setInput(v) { composer().props.onChange(v); render(); },
    async submit() { await composer().props.onSubmit({ preventDefault() {} }); },
    get opens() { return opens.length; },
    get sends() { return sends.length; },
  };
}

test("T-016 执行入口 组件渲染(待核实)：显示「价格待核实」，付费执行被拦且用户输入不丢失", async () => {
  const scene = executionScene(pendingExecutionView());
  await scene.flush();
  assert.match(scene.text(scene.tree), /价格待核实/, "execution entry shows the pending-price status");
  scene.setInput("用户已经写好的正文，不能丢");
  await scene.flush();
  await scene.submit();
  await scene.flush();
  assert.equal(scene.opens, 0, "no conversation/execution request is dispatched");
  assert.equal(scene.sends, 0, "paid execution is blocked before any send");
  assert.equal(scene.composerValue, "用户已经写好的正文，不能丢", "the typed input is retained");
  assert.match(scene.text(scene.tree), /价格待核实/, "block reason stays visible after the blocked attempt");
});
