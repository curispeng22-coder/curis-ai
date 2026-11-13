import assert from 'node:assert/strict';
import test from 'node:test';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import vm from 'node:vm';
const require=createRequire(import.meta.url),React=require('react'),swc=require('next/dist/build/swc');
const projection=await import('../lib/organizationProjection.js'),d1State=await import('../lib/d1State.mjs'),runtimeApi=await import('../lib/runtimeApi.js');
globalThis.fetch=()=>{throw Error('Network forbidden in copy/status tests');};await swc.loadBindings();const compiled={};
for(const [name,path] of Object.entries({shared:'components/v1/SharedConversation.js',meeting:'app/ceo-office/meeting/page.js'})){
 let s=readFileSync(new URL('../'+path,import.meta.url),'utf8');if(name==='meeting')s+='\nexport {Badge, MeetingDetail, MeetingSurface};';
 compiled[name]=(await swc.transform(s,{filename:path,isModule:true,jsc:{parser:{syntax:'ecmascript',jsx:true},transform:{react:{runtime:'automatic'}}},module:{type:'commonjs'}})).code;
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


const component=(tree,name)=>nodes(tree,n=>typeof n.type==='function'&&n.type.name===name)[0];
const manualNotice='当前可提交人工内容；自动回复与后续执行仍需各自满足条件。';
const modelNotice='尚未连接可用模型。输入会保留；请到人才与能力连接模型后重试。业务草稿仍可整理。';
function api(){return {getEnabledModels:async()=>({models:[]}),getModelPreference:async()=>({preference:null,available_models:[]}),recoverAIProvider:async()=>{throw Error('No recovery should run without a selected provider');}};}
test('actual Shared manual mode fits all three callers and submits unchanged event/null model without model requirement copy',async()=>{
 for(const [scopeKey,submitLabel] of [['meeting','发送'],['general','交给负责员工'],['business','整理业务提案']]){
  let calls=0;const h=scene('shared',api()),props={scopeKey,employee:{name:'真实员工'},allowWithoutModel:true,value:'真实手工说明',submitLabel,onSubmit:(event,model)=>{assert.equal(event.kind,'user');assert.equal(model,null);calls++;}};h.render(h.exports.default,props);await tick();h.render(h.exports.default,props);const composer=component(h.tree,'ConversationComposer');assert.equal(composer.props.disabled,false);assert.equal(composer.props.notice,manualNotice);assert.doesNotMatch(composer.props.notice,/连接模型后重试/);assert.equal(composer.props.submitLabel,submitLabel);assert.ok(nodes(h.tree,n=>n.props.href==='/ceo-office/capabilities'&&text(n)==='配置自动回复模型 →').length);composer.props.onSubmit({kind:'user'});assert.equal(calls,1);h.unmount();
 }
});
test('actual default false mode preserves original notice, link and disabled/busy/empty Composer gates',async()=>{
 for(const allowWithoutModel of [false,true]){
  const h=scene('shared',api()),props={allowWithoutModel,value:'说明',busy:true};h.render(h.exports.default,props);await tick();h.render(h.exports.default,props);let composer=component(h.tree,'ConversationComposer');assert.equal(composer.props.disabled,!allowWithoutModel);assert.equal(composer.props.notice,allowWithoutModel?manualNotice:modelNotice);if(!allowWithoutModel)assert.ok(nodes(h.tree,n=>n.props.href==='/ceo-office/capabilities'&&text(n)==='检查模型连接 →').length);
  h.render(h.exports.ConversationComposer,composer.props);assert.equal(nodes(h.tree,n=>n.type==='button'&&n.props.type==='submit')[0].props.disabled,true);h.render(h.exports.ConversationComposer,{...composer.props,busy:false,value:''});assert.equal(nodes(h.tree,n=>n.type==='button'&&n.props.type==='submit')[0].props.disabled,true);h.unmount();
 }
});
test('actual Meeting badges separate active lifecycle and blocked/stopped automation while preserving waiting/archived truth',()=>{
 const h=scene('meeting',{});
 for(const automatic of ['BLOCKED','STOPPED']){h.render(h.exports.Badge,{state:'DISCUSSING',meeting:{status:'active',orchestration:{status:automatic},background_continuation:{state:automatic}}});assert.match(text(h.tree),/会议进行中/);assert.match(text(h.tree),automatic==='BLOCKED'?/自动讨论暂不可用/:/自动讨论已停止/);}
 for(const [state,label] of [['WAITING_CEO','等待你决定'],['WAITING_RESULT','等待结果'],['ARCHIVED','已结束']]){h.render(h.exports.Badge,{state,meeting:{status:state==='ARCHIVED'?'closed':'active',orchestration:{status:'BLOCKED'}}});assert.match(text(h.tree),new RegExp(label));if(state==='ARCHIVED')assert.doesNotMatch(text(h.tree),/自动讨论/);}
 h.render(h.exports.Badge,{state:'DISCUSSING',meeting:{status:'active',orchestration:{status:'RUNNING'}}});assert.doesNotMatch(text(h.tree),/暂不可用|已停止/);h.unmount();
});
const meeting={meeting_id:'real-meeting',company_id:'A',workspace_id:'w',title:'真实人工会议',status:'active',operating_state:'DISCUSSING',participants_detail:[],timeline:[],context_refs:[],works:[],results:[],orchestration:{status:'BLOCKED',pendingEvents:[{type:'CEO_MESSAGE'}]},background_continuation:{status:'UNAVAILABLE',state:'BLOCKED'}};
test('actual header and list pass current DTO to status, with no mutation or held-state reset',async()=>{
 let writes=0;const api={getMeetings:async()=>({active:[meeting],history:[]}),getEmployees:async()=>({employees:[]}),getCanonicalBusinesses:async()=>({businesses:[]}),getKnowledgeEntries:async()=>({entries:[]}),syncMeeting:async()=>{writes++;}};const h=scene('meeting',api,{status:'ready',companyId:'A'});h.render(h.exports.MeetingSurface);await tick();h.render(h.exports.MeetingSurface);assert.equal(component(h.tree,'Badge').props.meeting,meeting);const detail=scene('meeting',api,{status:'ready',companyId:'A'});detail.render(detail.exports.MeetingDetail,{meeting,draft:{text:"",proposal:{summary:"",optionA:"",optionB:""}},onBack(){},onReload(){}});assert.equal(component(detail.tree,'Badge').props.meeting,meeting);detail.unmount();assert.equal(writes,0);assert.equal(meeting.orchestration.pendingEvents.length,1);assert.equal(meeting.orchestration.status,'BLOCKED');h.unmount();
});

test('actual Meeting refresh refusal clears busy, preserves draft and ignores stale completion',async()=>{
 const input={text:'未发送的会议输入',proposal:{summary:'未确认提案',optionA:'甲',optionB:'乙'}};let reloads=0;const gate=deferred();
 const h=scene('meeting',{syncMeeting:()=>gate.promise}),props={meeting,draft:input,onBack(){},onReload(){reloads++;}};const render=()=>h.render(h.exports.MeetingDetail,props);render();const work=button(h.tree,'刷新进展').props.onClick();render();assert.equal(button(h.tree,'刷新进展').props.disabled,true);gate.resolve(Promise.reject(Error('refresh refused')));await work;render();assert.equal(button(h.tree,'刷新进展').props.disabled,false);assert.match(text(h.tree),/refresh refused/);assert.equal(input.text,'未发送的会议输入');assert.equal(reloads,0);h.unmount();
 const late=deferred(),h2=scene('meeting',{syncMeeting:()=>late.promise}),render2=()=>h2.render(h2.exports.MeetingDetail,props);render2();const pending=button(h2.tree,'刷新进展').props.onClick();h2.unmount();late.resolve();await pending;assert.equal(reloads,0);
});
