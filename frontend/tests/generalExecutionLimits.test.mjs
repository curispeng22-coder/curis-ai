import assert from 'node:assert/strict';import test from 'node:test';import {readFileSync} from 'node:fs';import {createRequire} from 'node:module';import vm from 'node:vm';
const require=createRequire(import.meta.url),React=require('react'),swc=require('next/dist/build/swc');const runtimeApi=await import('../lib/runtimeApi.js'),d1State=await import('../lib/d1State.mjs'),projection=await import('../lib/organizationProjection.js');globalThis.fetch=()=>{throw Error('Network forbidden');};await swc.loadBindings();const path='components/v1/GeneralWorkspaceOperating.js';const compiled={general:(await swc.transform(readFileSync(new URL('../'+path,import.meta.url),'utf8'),{filename:path,isModule:true,jsc:{parser:{syntax:'ecmascript',jsx:true},transform:{react:{runtime:'automatic'}}},module:{type:'commonjs'}})).code};
function scene(name, api, runtime = { status: "ready", companyId: "a", snapshot: { company: { name: "A" } } }, query = "") {
  const slots = [], pending = []; let cursor = 0, tree;
  const same = (a, b) => a && b && a.length === b.length && a.every((item, i) => Object.is(item, b[i]));
  const hooks = {
    useState(initial) { const i = cursor++; if (!(i in slots)) slots[i] = { value: typeof initial === "function" ? initial() : initial }; return [slots[i].value, (value) => { slots[i].value = typeof value === "function" ? value(slots[i].value) : value; }]; },
    useReducer(reducer, initial, init) { const [value, setValue] = hooks.useState(() => init ? init(initial) : initial); return [value, (action) => setValue((current) => reducer(current, action))]; },
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
    module: loaded, exports: loaded.exports, URLSearchParams, URL, console, crypto: globalThis.crypto, location: { pathname: "/ceo-office/knowledge", search: "", assign: (value) => { api.returned = value; } }, scrollY: 0,
    sessionStorage: storageAPI,
    requestAnimationFrame: (fn) => fn(), scrollTo() {},
    window: { location: { search: query, pathname: "/ceo-office", origin: "http://127.0.0.1:3010" }, history: {pushState(...args) { api.history = args[2]; },replaceState(...args) { api.history = args[2]; }}, setInterval(fn) { api.poll = fn; return 1; }, clearInterval() {}, sessionStorage: storageAPI, localStorage: storageAPI, requestAnimationFrame: (fn) => fn(), addEventListener() {}, removeEventListener() {} },
    ResizeObserver: class { observe() {} disconnect() {} },
    document: { activeElement: { focus() {} } },
    require: (path) => {
      if (path === "react") return { ...React, ...hooks };
      if (path === "react/jsx-runtime") return require(path);
      if (path === "next/link") return { __esModule: true, default: primitive("a") };
      if (path === "next/navigation") return { useSearchParams: () => new URLSearchParams(api.query ?? query), useRouter: () => ({ push: (href) => { api.pushed = href; } }), useParams: () => ({ id: "doc" }), usePathname: () => "/ceo-office/knowledge" };
      if (path.includes("RuntimeProvider")) return { useRuntime: () => runtime };
      if (path.includes("WorkspacePaneShell") && api.hostComponent) return { __esModule: true, default: api.hostComponent };
      if (path.includes("TerraShell")) return { __esModule: true, default: primitive("main"), TerraPaneContent };
      if (path.includes("GlobalAssistant")) return { useAssistantPageContext() {} };
      if (path.includes("theme.js")) return { roleLabel: (value) => value };
      if (path.includes("EmployeeAvatar")) return { EmployeeAvatar: primitive("span"), EMPLOYEE_AVATAR_PRESETS: [] };
      if (path.includes("organizationProjection")) return projection;
      if (path.includes("d1State")) return d1State;
      if (path.includes("d1Api")) return { d1Api: api, d1Error: () => "无法读取当前资料" };
      if (path.includes("runtimeApi")) return { ...runtimeApi, ...api };
      if (path.includes("ResultReferenceView")) return { __esModule: true, default: primitive("result-reference"), restoreResultSelection: () => null, rememberResultSelection() {}, resultSelection: (workspaceId, referenceId) => ({workspaceId, referenceId}) };
      if (path.includes("CeoMatterView")) return { __esModule: true, default: primitive("ceo"), workState: (value) => value };
      if (path.includes("lib/")) return api;
      if (path.endsWith(".module.css")) return { __esModule: true, default: new Proxy({}, { get: (_, key) => String(key) }) };
      if (/Music[A-Za-z]+\.js$/.test(path)) { const name = path.split("/").at(-1).replace(".js", ""); const Component = primitive("div"); Object.defineProperty(Component, "name", { value: name }); return { __esModule: true, default: Component }; }
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

const authPath = 'app/ceo-office/capabilities/PrivateAgentDrawer.js';
compiled.auth = (await swc.transform(readFileSync(new URL('../' + authPath, import.meta.url), 'utf8'), { filename: authPath, isModule: true, jsc: { parser: { syntax: 'ecmascript', jsx: true }, transform: { react: { runtime: 'automatic' } } }, module: { type: 'commonjs' } })).code;
const capabilitiesCode = (await swc.transform(readFileSync(new URL('../lib/capabilities.js', import.meta.url), 'utf8'), { filename: 'capabilities.js', isModule: true, module: { type: 'commonjs' } })).code;
function authClient(request) {
  const loaded = { exports: {} };
  vm.runInNewContext(capabilitiesCode, { module: loaded, exports: loaded.exports, require: () => ({ workspaceFetch: request }) });
  return loaded.exports;
}
const generation = 'a'.repeat(48);
const authValue = (company = 'A', state = 'DISCONNECTED') => ({ company_id: company, binding_ref: 'binding', capability_id: 'agent', state, generation: state === 'DISCONNECTED' ? null : generation });
test('Codex client rejects foreign scope, untrusted challenge and coerced field types before display', async () => {
  const calls = [], client = authClient(async (...args) => { calls.push(args); return authValue(); });
  for (const value of [null, [], { ...authValue(), company_id: 'B' }, { ...authValue(), secret: 'never-display' }, { ...authValue(), generation: [generation] },
    { ...authValue('A', 'WAITING_FOR_LOGIN'), user_code: ['ABCD-1234'], verification_url: 'https://auth.openai.com/codex/device' },
    { ...authValue('A', 'WAITING_FOR_LOGIN'), user_code: 'ABCD-1234', verification_url: 'https://evil.example' }, { ...authValue('A', 'CONNECTED'), generation: null }]) {
    assert.throws(() => client.codexConnectionState(value, 'A', 'binding'));
  }
  for (const payload of [{ request_id: ['12345678-1234-1234-1234-123456789abc'] }, { request_id: '12345678-1234-1234-1234-123456789abc', expected_generation: [generation] }, { request_id: 'x'.repeat(36) }]) {
    await assert.rejects(client.controlAgentCodexAuth('A', 'binding', 'connect', payload));
  }
  assert.equal(calls.length, 0);
  await client.controlAgentCodexAuth('A', 'binding', 'connect', { request_id: '12345678-1234-1234-1234-123456789abc' });
  assert.equal(calls[0][0], '/api/workspace/v1/companies/A/agent-auth/binding/connect');
  assert.equal(JSON.parse(calls[0][1].body).expected_generation, null);
});
const authAllowance = { binding_options: [{ binding_ref: 'binding', employee_name: '员工', agent_name: 'Codex' }], policy: { bindings: [] }, used_calls: 0, remaining_calls: 4 };
async function authScene(overrides = {}) {
  const api = { getAgentAllowanceCompanies: async () => [{ company_id: 'A', name: 'A' }, { company_id: 'B', name: 'B' }], getAgentAllowance: async () => authAllowance,
    getAgentCodexAuth: async (company) => authValue(company), ...overrides };
  const h = scene('auth', api), render = () => h.render(h.exports.AgentAllowancePanel);
  render(); await tick(); render(); nodes(h.tree, n => n.type === 'select')[0].props.onChange({ target: { value: 'A' } });
  render(); await tick(); render(); await tick(); render();
  return { h, api, render };
}
test('Codex UI displays only transient official challenge, polls GET and clears it on company change', async () => {
  let reads = 0, posts = 0;
  const challenge = { ...authValue('A', 'WAITING_FOR_LOGIN'), verification_url: 'https://auth.openai.com/codex/device', user_code: 'ABCD-1234' };
  const { h, api, render } = await authScene({ getAgentCodexAuth: async (company) => { reads++; return company === 'A' ? challenge : authValue(company); }, controlAgentCodexAuth: async () => { posts++; } });
  assert.match(text(h.tree), /ABCD-1234/);
  assert.equal(nodes(h.tree, n => n.type === 'a' && n.props.href === challenge.verification_url)[0].props.rel, 'noopener noreferrer');
  const before = reads; api.poll(); await tick(); render(); assert.equal(reads, before + 1); assert.equal(posts, 0);
  nodes(h.tree, n => n.type === 'select')[0].props.onChange({ target: { value: 'B' } }); render(); await tick(); render(); await tick(); render();
  assert.doesNotMatch(text(h.tree), /ABCD-1234/); h.unmount();
});
test('Codex UI serializes duplicate clicks and UNKNOWN requires explicit GET without POST retry', async () => {
  const wait = deferred(); let posts = 0, reads = 0;
  const { h, render } = await authScene({ getAgentCodexAuth: async (company) => { reads++; return authValue(company); }, controlAgentCodexAuth: async () => { posts++; await wait.promise; throw Error('unknown'); } });
  const click = button(h.tree, '登录 Codex').props.onClick, first = click(); await click(); assert.equal(posts, 1);
  wait.resolve(); await first; render(); assert.match(text(h.tree), /不会自动重复提交/); assert.equal(button(h.tree, '登录 Codex').props.disabled, true);
  await button(h.tree, '登录 Codex').props.onClick(); assert.equal(posts, 1);
  await button(h.tree, '读取 Codex 连接').props.onClick(); render(); assert.equal(button(h.tree, '登录 Codex').props.disabled, false); assert.equal(posts, 1); assert.equal(reads, 2); h.unmount();
});
test('late Codex login response cannot repopulate a different company', async () => {
  const wait = deferred();
  const { h, render } = await authScene({ controlAgentCodexAuth: async () => wait.promise });
  const first = button(h.tree, '登录 Codex').props.onClick();
  nodes(h.tree, n => n.type === 'select')[0].props.onChange({ target: { value: 'B' } }); render(); await tick(); render();
  wait.resolve({ ...authValue('A', 'WAITING_FOR_LOGIN'), verification_url: 'https://auth.openai.com/codex/device', user_code: 'LATE-1234' }); await first; render();
  assert.doesNotMatch(text(h.tree), /LATE-1234/); h.unmount();
});
test('unmount clears transient challenge and a remount only reads current state', async () => {
  const storage = new Map(); let posts = 0;
  const first = await authScene({ storage, getAgentCodexAuth: async () => ({ ...authValue('A', 'WAITING_FOR_LOGIN'), verification_url: 'https://auth.openai.com/codex/device', user_code: 'ABCD-1234' }) });
  assert.match(text(first.h.tree), /ABCD-1234/); first.h.unmount(); assert.equal(storage.size, 0);
  const next = await authScene({ storage, controlAgentCodexAuth: async () => { posts++; } });
  assert.doesNotMatch(text(next.h.tree), /ABCD-1234/); assert.equal(posts, 0); next.h.unmount();
});


const data={company:{company_id:'A'},workspace:{workspace_id:'w',name:'实际工作空间'},business:{positioning:'当前目标'},goal:'内部核对',operating_readiness:{status:'READY_FOR_WORK',reason:'实际责任',next_action:'核对'},team:{employees:[{employee_ref:'e',name:'实际员工'}]},results:[],current_work:[{work_ref:'one',problem:'内部交付核对',status:'ACTIVE',lifecycle_status:'ACTIVE',result_refs:[],evidence_refs:[],artifact_refs:[],handoffs:[]}]};
const props={companyId:'A',workspaceId:'w',parentPath:{company:{name:'A'},department:{name:'部门'},business:{name:'业务'}}};
test('existing wrapper no argument URL/body is unchanged; bounded request is strict and scoped',async()=>{
 let calls=[];const request=async(url,options)=>{calls.push({url,options});};await runtimeApi.executeGeneralWorkspaceWork('work/ref',request);assert.deepEqual(calls[0],{url:'/api/workspace/runtime/foundation/team-operating/works/work%2Fref/execute?max_executions=1',options:{method:'POST'}});
 await runtimeApi.executeGeneralWorkspaceWork('work/ref',request,{max_prompt_bytes:4096,max_output_tokens:2048});assert.deepEqual(JSON.parse(calls[1].options.body),{max_prompt_bytes:4096,max_output_tokens:2048});
 for(const bad of [{max_prompt_bytes:4097,max_output_tokens:2048},{max_prompt_bytes:4096,max_output_tokens:true},{max_prompt_bytes:4096,max_output_tokens:1.1},{max_prompt_bytes:4096,max_output_tokens:2049,version:2}])assert.throws(()=>runtimeApi.executeGeneralWorkspaceWork('ref',request,bad));assert.equal(calls.length,2);
});
test('actual Work-local opt-in locks UNKNOWN, survives remount and never calls a second execution',async()=>{
 let executions=[];const storage=new Map(),api={storage,conversationError:(error,fallback)=>fallback,getGeneralWorkspace:async(companyId,workspaceId)=>({...data,company:{...data.company,company_id:companyId},workspace:{...data.workspace,workspace_id:workspaceId}}),executeGeneralWorkspaceWork:async(ref,request,limits)=>{executions.push({ref,limits});throw Error('Response unknown');}};
 const h=scene('general',api);h.render(h.exports.default,props);await tick();h.render(h.exports.default,props);nodes(h.tree,n=>n.type==='input'&&n.props.type==='checkbox')[0].props.onChange({target:{checked:true}});h.render(h.exports.default,props);await button(h.tree,'开始处理').props.onClick();h.render(h.exports.default,props);assert.equal(executions.length,1);assert.deepEqual(JSON.parse(JSON.stringify(executions[0].limits)),{max_prompt_bytes:4096,max_output_tokens:2048});assert.equal(button(h.tree,'开始处理').props.disabled,true);assert.match(text(h.tree),/只重新读取/);h.unmount();
 const restored=scene('general',api);restored.render(restored.exports.default,props);await tick();restored.render(restored.exports.default,props);assert.equal(button(restored.tree,'开始处理').props.disabled,true);await button(restored.tree,'开始处理').props.onClick();assert.equal(executions.length,1);restored.unmount();
 const foreign=scene('general',api);foreign.render(foreign.exports.default,{...props,companyId:'B'});await tick();foreign.render(foreign.exports.default,{...props,companyId:'B'});assert.equal(nodes(foreign.tree,n=>n.type==='input'&&n.props.type==='checkbox')[0].props.checked,false);foreign.unmount();
});
test('actual normal existing Work caller retains ordinary behavior and pending prevents concurrent duplicate click',async()=>{
 let calls=0;const wait=deferred();const api={conversationError:(error,fallback)=>fallback,getGeneralWorkspace:async()=>data,executeGeneralWorkspaceWork:async(ref,request,limits)=>{assert.equal(limits,null);calls++;await wait.promise;}};const h=scene('general',api);h.render(h.exports.default,props);await tick();h.render(h.exports.default,props);const click=button(h.tree,'开始处理').props.onClick;const one=click();await click();assert.equal(calls,1);wait.resolve();await one;h.unmount();
});
