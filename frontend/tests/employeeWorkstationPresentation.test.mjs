import assert from "node:assert/strict";
import test from "node:test";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import vm from "node:vm";
const require=createRequire(import.meta.url),React=require("react"),swc=require("next/dist/build/swc");
const projection=await import("../lib/organizationProjection.js"),runtimeApi=await import("../lib/runtimeApi.js"),d1State=await import("../lib/d1State.mjs");
globalThis.fetch=()=>{throw Error('Network forbidden in employee presentation tests');};
await swc.loadBindings();const compiled={};
for(const [name,path] of Object.entries({page:'app/ceo-office/organization/employees/[id]/page.js',conversation:'components/v1/EmployeeConversation.js'})){
 let source=readFileSync(new URL('../'+path,import.meta.url),'utf8');if(name==='page')source+='\nexport {EmployeeDetailContent};';
 compiled[name]=(await swc.transform(source,{filename:path,isModule:true,jsc:{parser:{syntax:'ecmascript',jsx:true},transform:{react:{runtime:'automatic'}}},module:{type:'commonjs'}})).code;
}
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
      if (path === "next/navigation") return { useSearchParams: () => new URLSearchParams(api.query ?? query), useRouter: () => ({ push: (href) => { api.pushed = href; } }), useParams: () => ({ id: api.id || "e" }), usePathname: () => "/ceo-office/knowledge" };
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
      if (path.includes("BusinessCatalogSurface")) return { businessCatalogHref: (company, selection) => `/ceo-office/business?company_id=${company}&business_id=${selection.businessId}` };
      if (path.includes("EmployeeConversation.js")) return { __esModule: true, default: function EmployeeConversation() {} };
      if (path.includes("SharedConversation.js")) return { ConversationComposer: primitive("composer") };
      if (path.includes("businessReturnApi")) return { businessReturnInput: () => null, validateBusinessReturn: async () => {throw Error("No business-object mock provided");} };
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


const component=(tree,name)=>nodes(tree,n=>typeof n.type==='function'&&n.type.name===name)[0];
const employee={id:'e',company_id:'A',name:'用户命名',role:'当前岗位',enabled:true,status:'idle',department_id:'d',template_id:'template',created_at:'2026-10-11'};
const organization={company:{company_id:'A',name:'当前公司'},departments:[{id:'d',company_id:'A',name:'当前部门'}],employees:[employee],businesses:[{company_id:'A',business_id:'b',department_id:'d',name:'真实业务',team:[{entity_id:'a1',lifecycle_status:'ACTIVE',data:{companyEmployeeRef:'e',roleRef:'leader',roleName:'业务负责人',scopeType:'BUSINESS',scopeRef:'b'}},{entity_id:'a2',lifecycle_status:'ACTIVE',data:{companyEmployeeRef:'e',roleRef:'author',roleName:'创作责任',scopeType:'WORKSPACE',scopeRef:'w'}}]}]};
function apiFor(extra={}) {return {id:'e',getEmployee:async()=>employee,getDepartments:async()=>({departments:organization.departments}),getEmployeeTemplates:async()=>({employee_templates:[{id:'template',name:'真实模板',responsibility:'模板说明不是当前职责'}]}),getCapabilitySelector:async()=>({capabilities:[]}),getEmployeeCapabilities:async()=>({bindings:[]}),getEmployeeSkills:async()=>({bindings:[]}),getEmployeeTools:async()=>({bindings:[]}),getOrganizationProjection:async()=>organization,...extra};}
const rt=()=>({status:'ready',companyId:'A',snapshot:{company:{company_id:'A'}}});
async function loaded(extra={},query=''){const api=apiFor(extra),runtime=rt(),h=scene('page',api,runtime,query);h.render(h.exports.EmployeeDetailContent);await tick();await tick();h.render(h.exports.EmployeeDetailContent);return {h,api,runtime};}
test('actual loaded employee Main is one compact identity and genuine duties before unchanged full conversation',async()=>{
 const {h}=await loaded();const headers=nodes(h.tree,n=>n.type==='header');assert.match(text(headers[0]),/用户命名.*当前岗位.*当前部门/);assert.equal(nodes(h.tree,n=>n.type==='h1').length,1);assert.equal(nodes(h.tree,n=>n.props.facts).length,0);assert.doesNotMatch(text(h.tree),/关联项目|未分配|模板说明不是当前职责/);
 const duties=nodes(h.tree,n=>n.props['aria-labelledby']==='employee-duty-title')[0];assert.match(text(duties),/业务负责人.*创作责任/);const convo=component(h.tree,'EmployeeConversation');assert.ok(convo);assert.equal(convo.key,'A:e:null');assert.equal(convo.props.companyId,'A');assert.equal(convo.props.employee.name,'用户命名');assert.equal(convo.props.conversationId,null);assert.ok(!convo.props.hidden);h.unmount();
});
test('official Content Growth duty is explained in Chinese in Main and Utility while custom duty and source stay exact',async()=>{
 const official='目标与合法账号上下文中的创作、事实与规格自检、Publishing交付准备与真实回执、Analytics口径与缺失事实复盘；自检不是独立审核';
 const custom='用户自定 Publishing 与 Analytics 工作范围';
 const expected='目标与合法账号上下文中的创作、事实与规格自检、发布交付准备与真实回执、数据分析口径与缺失事实复盘；自检不是独立审核';
 const current=structuredClone(organization);
 current.businesses[0].team[0].data.responsibility=custom;
 current.businesses[0].team[1].data.responsibility=official;
 const {h}=await loaded({getOrganizationProjection:async()=>current});
 const duties=nodes(h.tree,n=>n.props['aria-labelledby']==='employee-duty-title')[0];
 assert.match(text(duties),new RegExp(expected));assert.match(text(duties),new RegExp(custom));assert.doesNotMatch(text(duties),/Publishing交付准备/);
 nodes(h.tree,n=>n.type==='button'&&n.props['aria-label']==='打开用户命名的档案')[0].props.onClick();h.render(h.exports.EmployeeDetailContent);
 const utility=text(component(h.tree,'TerraPaneContent').props.utilityTabs[0].content);
 assert.match(utility,new RegExp(expected));assert.match(utility,new RegExp(custom));assert.doesNotMatch(utility,/Publishing交付准备/);
 assert.equal(current.businesses[0].team[0].data.responsibility,custom);assert.equal(current.businesses[0].team[1].data.responsibility,official);
 h.unmount();
});
test('actual avatar/name Utility intent keeps full Conversation identity, real detail, and edit open/cancel with zero writes',async()=>{
 let writes=0;const {h}=await loaded({sendEmployeeMessage:async()=>{writes++;}});const first=component(h.tree,'EmployeeConversation');const avatar=nodes(h.tree,n=>n.type==='button'&&n.props['aria-label']==='打开用户命名的档案')[0];avatar.props.onClick();h.render(h.exports.EmployeeDetailContent);const host=component(h.tree,'TerraPaneContent');assert.equal(host.props.utilityRequestKey,1);assert.match(text(host.props.utilityTabs[0].content),/用户命名.*模板说明不是当前职责/);assert.equal(component(h.tree,'EmployeeConversation').key,first.key);assert.equal(component(h.tree,'EmployeeConversation').type,first.type);assert.equal(component(h.tree,'EmployeeConversation').props.employee,first.props.employee);
 // Shared host closes its own tab; an ordinary parent rerender carries no new open serial.
 h.render(h.exports.EmployeeDetailContent);assert.equal(component(h.tree,'TerraPaneContent').props.utilityRequestKey,1);nodes(h.tree,n=>n.type==='button'&&n.props['aria-label']==='打开用户命名的档案')[1].props.onClick();h.render(h.exports.EmployeeDetailContent);assert.equal(component(h.tree,'TerraPaneContent').props.utilityRequestKey,2);
 const edit=nodes(h.tree,n=>n.props.icon==='i-checklist')[0];edit.props.onClick();h.render(h.exports.EmployeeDetailContent);let drawer=nodes(h.tree,n=>n.props.roleLabel&&n.props.onSuccess)[0];assert.equal(drawer.props.open,true);drawer.props.onClose();h.render(h.exports.EmployeeDetailContent);drawer=nodes(h.tree,n=>n.props.roleLabel&&n.props.onSuccess)[0];assert.equal(drawer.props.open,false);assert.equal(component(h.tree,'EmployeeConversation').key,first.key);assert.equal(writes,0);h.unmount();
});
test('actual unchanged child conversation draft survives parent Utility and edit state rerenders',async()=>{
 const {h}=await loaded();const element=component(h.tree,'EmployeeConversation');let writes=0;const api={getEmployeeConversation:async()=>({employee,assignments:[{assignment_ref:'a1',workspace_id:'w'}],messages:[],attempts:[],execution_models:[]}),getEmployeeConversationReferences:async()=>({references:[]}),sendEmployeeMessage:async()=>{writes++;}};const child=scene('conversation',api);child.render(child.exports.default,element.props);await tick();child.render(child.exports.default,element.props);await tick();child.render(child.exports.default,element.props);let composer=nodes(child.tree,n=>n.props.placeholder==='想和用户命名讨论什么？')[0];composer.props.onChange('未发送的输入');child.render(child.exports.default,element.props);
 nodes(h.tree,n=>n.type==='button'&&n.props['aria-label']==='打开用户命名的档案')[0].props.onClick();h.render(h.exports.EmployeeDetailContent);const same=component(h.tree,'EmployeeConversation');assert.equal(same.key,element.key);assert.equal(same.type,element.type);child.render(child.exports.default,same.props);composer=nodes(child.tree,n=>n.props.placeholder==='想和用户命名讨论什么？')[0];assert.equal(composer.props.value,'未发送的输入');assert.match(text(child.tree),/尚未配置可用的显式模型桥接/);assert.equal(writes,0);h.unmount();child.unmount();
});
test('actual same-name role is not duplicated in header; empty and disabled facts remain honest',async()=>{
 const disabled={...employee,name:'当前岗位',enabled:false,status:'disabled'};const {h}=await loaded({getEmployee:async()=>disabled,getOrganizationProjection:async()=>({...organization,employees:[disabled],businesses:[]})});const header=nodes(h.tree,n=>n.type==='header')[0];assert.equal(text(header).split('当前岗位').length-1,1);assert.match(text(header),/已暂停/);assert.match(text(h.tree),/当前尚未安排工作职责/);assert.doesNotMatch(text(h.tree),/可执行|正在执行|已联网/);h.unmount();
});
test('actual source scope guard rejects foreign employee and original malformed Business return without new truth',async()=>{
 for(const [extra,query] of [[{getEmployee:async()=>({...employee,company_id:'foreign'})},''],[{},'?company_id=foreign&business_id=b']]){
  const {h}=await loaded(extra,query);assert.equal(component(h.tree,'EmployeeConversation'),undefined);assert.ok(nodes(h.tree,n=>n.props.message).length);h.unmount();
 }
 const {h}=await loaded({},'?company_id=A&business_id=b');assert.ok(nodes(h.tree,n=>n.props.href==='/ceo-office/business?company_id=A&business_id=b').length);h.unmount();
});
test('installed CSS parser verifies local Main container descendant rules and intact focus/readability',()=>{
 const nextRequire=createRequire(require.resolve('next/package.json')),postcss=nextRequire('postcss'),css=postcss.parse(readFileSync(new URL('../app/ceo-office/organization/employees/[id]/EmployeeWorkstation.module.css',import.meta.url),'utf8'));let containers=0;css.walkAtRules('container',rule=>{containers++;rule.walkRules(child=>assert.notEqual(child.selector,'.page'));rule.walkDecls(d=>assert.ok(!['order','position'].includes(d.prop)));});assert.equal(containers,2);assert.ok(css.nodes.some(rule=>rule.selector==='.page'&&rule.nodes.some(d=>d.prop==='container-type'&&d.value==='inline-size')));assert.ok(css.nodes.some(rule=>rule.selector?.includes(':focus-visible')));
});
