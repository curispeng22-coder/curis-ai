import assert from "node:assert/strict";
import test from "node:test";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import vm from "node:vm";
const require = createRequire(import.meta.url), React = require("react"), swc = require("next/dist/build/swc");
const projection = await import("../lib/organizationProjection.js"), d1State = await import("../lib/d1State.mjs"), runtimeApi = await import("../lib/runtimeApi.js");
globalThis.fetch = () => { throw new Error("Network forbidden in focused consumer tests"); };
await swc.loadBindings();
const paths={ceo:"components/delivery/d1/CeoMatterView.js",d1:"components/delivery/d1/D1Surface.js",org:"app/ceo-office/organization/OrganizationCenter.js",meeting:"app/ceo-office/meeting/page.js",decisions:"app/ceo-office/decisions/page.js",result:"components/delivery/d1/ResultView.js",work:"components/delivery/d1/WorkView.js",general:"components/v1/GeneralWorkspaceOperating.js"};
const compiled={};
for(const [name,path] of Object.entries(paths)) {
 let source=readFileSync(new URL(`../${path}`,import.meta.url),'utf8');
 if(name==='org') source+='\nexport {CompanyMap, EmployeeDirectory, BusinessFocus};';
 if(name==='meeting') source+='\nexport {MeetingDetail, MeetingSurface};';
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
const fixture=(company='A')=>({company:{company_id:company,name:`真实公司${company}`},departments:[{id:'d',company_id:company,name:'实际部门'}],employees:[{id:'e',company_id:company,name:'保留的用户姓名',enabled:true,department_id:'d'}],businesses:['b1','b2'].map((id,i)=>({company_id:company,business_id:id,department_id:'d',name:`同型业务${i+1}`,goal:'原目标',lifecycle_status:'DRAFT',workspaces:[{workspace_id:'w'+id,name:`原空间${i+1}`}],team:[{entity_id:'a'+id,lifecycle_status:'ACTIVE',data:{companyEmployeeRef:'e',roleRef:'role'+id,scopeType:'BUSINESS',scopeRef:id,roleName:'业务负责人',isLeader:true}},{entity_id:'author'+id,lifecycle_status:'ACTIVE',data:{companyEmployeeRef:'e',roleRef:'author-role'+id,scopeType:'WORKSPACE',scopeRef:'w'+id,roleName:'创作职责'}}]}))});
const runtime=(company='A')=>({status:'ready',companyId:company,snapshot:{company:{company_id:company,name:`真实公司${company}`}}});
const d1Api=(extra={})=>({attention:async()=>({company:{company_id:'A'},items:[],state:'QUIET'}),businesses:async()=>({businesses:fixture().businesses}),getOrganizationProjection:async()=>fixture(),work:async()=>({work_ref:'work',problem:'原问题'}),...extra});
test('compiled CEO joins same-type business facts only through exact workspaces and current enabled leader',()=>{
 const f=fixture(),p=projection.buildOrganizationProjection(f),h=scene('ceo',{}),attention={items:[{source_type:'RESULT',source_ref:'r',workspace_id:'wb2',summary:'仅业务二的结果',status:'COMPLETED'}]};
 h.render(h.exports.default,{company:f.company,businesses:[...f.businesses,{company_id:'foreign',business_id:'x',name:'foreign'}],organization:p,attention});
 const rows=nodes(h.tree,n=>n.type==='article');assert.equal(rows.length,2);assert.doesNotMatch(text(rows[0]),/仅业务二/);assert.match(text(rows[1]),/仅业务二/);assert.doesNotMatch(text(h.tree),/foreign|经营平稳|增长百分比/);
 assert.ok(nodes(rows[1],n=>n.type==='a').some(n=>n.props.href.includes('business_id=b2')));
 f.employees[0].enabled=false;h.render(h.exports.default,{company:f.company,businesses:f.businesses,organization:projection.buildOrganizationProjection(f),attention});assert.match(text(nodes(h.tree,n=>n.type==='article')[0]),/负责人尚未确认/);
});
test('compiled D1 discards late foreign company read and preserves independent organization failure',async()=>{
 const late=deferred(),rt=runtime(),api=d1Api({attention:()=>late.promise,getOrganizationProjection:async()=>{throw Error('unavailable');}}),h=scene('d1',api,rt);
 h.render(h.exports.default);rt.companyId='B';rt.snapshot.company={company_id:'B'};api.attention=async()=>({company:{company_id:'B'},items:[]});api.businesses=async()=>({businesses:fixture('B').businesses});h.render(h.exports.default);await tick();late.resolve({company:{company_id:'A'},items:[{summary:'old-secret'}]});await tick();h.render(h.exports.default);
 const ceo=component(h.tree,'Primitive');assert.doesNotMatch(JSON.stringify(ceo?.props),/old-secret/);
 const target=nodes(h.tree,n=>n.props?.organizationError)[0];assert.equal(target.props.company.company_id,'B');assert.equal(target.props.organization,null);assert.match(target.props.organizationError,/暂不可读取/);h.unmount();
});
test('compiled D1 validates original Meeting return; restoration remains explicit false',async()=>{
 const valid='/ceo-office/meeting?meeting=m1&company_id=A',invalid=['https://evil.test/ceo-office/meeting?meeting=m','//evil.test/ceo-office/meeting?meeting=m','/ceo-office/meeting?meeting=','/ceo-office/meeting?meeting=m&meeting=x','/ceo-office/meeting?meeting=m&x=1','/ceo-office/meeting?meeting=m#x','/ceo-office/meeting?meeting=m&company_id=B','/ceo-office/meeting?meeting=m%5Cx','/ceo-office/meeting?meeting=m%0Ax','/ceo-office/business?meeting=m'];
 for(const raw of [valid,...invalid]) {
  const query='?view=result&workspace_id=w&result_ref=r&return_to='+encodeURIComponent(raw),h=scene('d1',d1Api(),runtime(),query);h.render(h.exports.default);await tick();h.render(h.exports.default);
  assert.equal(nodes(h.tree,n=>n.type==='a'&&text(n)==='返回原会议 →').length,raw===valid?1:0);
  const view=nodes(h.tree,n=>n.props.selection?.view==='result')[0];assert.equal(view.props.selection.explicit,false);h.unmount();
 }
 const h=scene('d1',d1Api(),runtime(),'?view=result&workspace_id=w&result_ref=r&return_to='+encodeURIComponent(valid)+'&return_to='+encodeURIComponent(valid));h.render(h.exports.default);await tick();h.render(h.exports.default);assert.equal(nodes(h.tree,n=>text(n)==='返回原会议 →').length,0);h.unmount();
});
test('actual Org selection keeps one employee across two duties, reopens only on click, and rejects stale company',()=>{
 const f=fixture(),p=projection.buildOrganizationProjection({...f,businesses:[f.businesses[0]]}),rt=runtime(),h=scene('org',{},rt);const props={projection:p,query:'',setQuery(){}};h.render(h.exports.EmployeeDirectory,props);
 assert.equal(nodes(h.tree,n=>n.type==='article').length,1);nodes(h.tree,n=>n.type==='button')[0].props.onClick();h.render(h.exports.EmployeeDirectory,props);let host=component(h.tree,'TerraPaneContent');assert.equal(host.props.utilityRequestKey,1);assert.match(text(host.props.utilityTabs[0].content),/保留的用户姓名.*业务负责人/);h.render(h.exports.EmployeeDirectory,props);assert.equal(component(h.tree,'TerraPaneContent').props.utilityRequestKey,1);
 h.render(h.exports.BusinessFocus,{business:p.businesses[0],projection:p});assert.match(text(h.tree),/岗位职责2 项员工1 名/);
 rt.companyId='B';h.render(h.exports.EmployeeDirectory,props);assert.doesNotMatch(text(h.tree),/保留的用户姓名/);h.unmount();
});
const meeting={company_id:'A',meeting_id:'m',workspace_id:'w',title:'真实会议',status:'open',operating_state:'DISCUSSING',participants_detail:[],timeline:[],context_refs:[],works:[{entity_id:'work',data:{contract:{problem:'原工作'}}}],results:[{reference_id:'r',summary:'原结果',kind:'RESULT'}]};
test('actual Meeting auxiliary carries exact work/result source and safe return; pane registration never mutates',()=>{
 let mutations=0;const api={syncMeeting:async()=>{mutations++;},addMeetingMessage:async()=>{mutations++;}},h=scene('meeting',api);h.render(h.exports.MeetingDetail,{meeting,onBack(){},onReload(){}});const host=component(h.tree,'TerraPaneContent');assert.equal(host.props.initialUtilityOpen,undefined);const aux=host.props.utilityTabs[0].content;
 assert.ok(nodes(aux,n=>n.props.href?.includes('workspace_id=w')).length);const result=nodes(aux,n=>n.props.href?.includes('result_ref=r'))[0];const url=new URL(result.props.href,'http://local');assert.equal(url.searchParams.get('return_to'),'/ceo-office/meeting?meeting=m');assert.equal(url.searchParams.get('workspace_id'),'w');assert.equal(mutations,0);
 const shared=nodes(h.tree,n=>n.props.placeholder==='继续讨论，或补充你掌握的事实…')[0];shared.props.onChange('未发送的真实说明');h.render(h.exports.MeetingDetail,{meeting:{...meeting,timeline:[]},onBack(){},onReload(){}});assert.equal(nodes(h.tree,n=>n.props.placeholder==='继续讨论，或补充你掌握的事实…')[0].props.value,'未发送的真实说明');assert.equal(mutations,0);h.unmount();
});
test('actual Meeting collection discards obsolete scope read and filters foreign participants',async()=>{
 const late=deferred(),rt=runtime(),api={getMeetings:()=>late.promise,getEmployees:async()=>({employees:[]}),getCanonicalBusinesses:async()=>({businesses:[]}),getKnowledgeEntries:async()=>({entries:[]})},h=scene('meeting',api,rt);h.render(h.exports.MeetingSurface);rt.companyId='B';api.getMeetings=async()=>({active:[],history:[]});api.getEmployees=async()=>({employees:[{id:'foreign',company_id:'A'},{id:'local',company_id:'B'}]});h.render(h.exports.MeetingSurface);await tick();late.resolve({active:[{meeting_id:'old',title:'old-secret'}],history:[]});await tick();h.render(h.exports.MeetingSurface);assert.doesNotMatch(text(h.tree),/old-secret/);const overlay=component(h.tree,'MeetingOverlay');assert.deepEqual(overlay.props.employees.map(x=>x.id),['local']);h.unmount();
});
test('actual decisions uses current canonical pending packets without fake approval and preserves read errors',async()=>{
 const rt=runtime(),api={getCompanyAttention:async()=>({company:{company_id:'A'},items:[{source_type:'DECISION_PACKET',source_ref:'d',status:'WAITING_CEO',summary:'真实等待决定',workspace_id:'w'},{source_type:'RESULT',source_ref:'r',status:'WAITING_CEO',summary:'not-decision'}]})},h=scene('decisions',api,rt);h.render(h.exports.default);await tick();h.render(h.exports.default);assert.match(text(h.tree),/真实等待决定/);assert.doesNotMatch(text(h.tree),/not-decision|通过|退回|拒绝/);assert.equal(nodes(h.tree,n=>n.type==='button').length,0);assert.ok(nodes(h.tree,n=>n.type==='a'&&n.props.href?.includes('workspace_id=w')).length);h.unmount();
 const bad=scene('decisions',{getCompanyAttention:async()=>{throw Error('failed');}},runtime());bad.render(bad.exports.default);await tick();bad.render(bad.exports.default);assert.ok(nodes(bad.tree,n=>n.props.message?.includes('暂不可读取')).length);assert.doesNotMatch(text(bad.tree),/没有已返回/);bad.unmount();
});
test('actual Result explicit readable fixed-version receipt remains separate from restoration and unavailable choice',async()=>{
 for(const explicit of [false,true]){let writes=0;const api={result:async()=>({reference_id:'r',result_version:'v1',kind:'RESULT',body:'真实原文',content:'真实原文',text:'真实原文',title:'原结果'}),viewed:async()=>{writes++;}},h=scene('result',{});const props={companyId:'A',selection:{workspaceId:'w',resultRef:'r',explicit},api,onBack(){},onWork(){}};h.render(h.exports.default,props);await tick();h.render(h.exports.default,props);await tick();h.render(h.exports.default,props);assert.equal(writes,explicit?1:0);for(const label of ['接受此结果','要求修改','拒绝此结果'])assert.equal(button(h.tree,label).props.disabled,true);h.unmount();}
});
test('actual Result empty, artifact and mismatched ref never create a viewing receipt',async()=>{
 for(const result of [{reference_id:'r',kind:'RESULT',result_version:'v1'},{reference_id:'r',kind:'ARTIFACT',result_version:'v1',content:'原材料'},{reference_id:'foreign',kind:'RESULT',result_version:'v1',content:'foreign-secret'}]){let writes=0;const h=scene('result',{}),props={companyId:'A',selection:{workspaceId:'w',resultRef:'r',explicit:true},api:{result:async()=>result,viewed:async()=>{writes++;}},onBack(){},onWork(){}};h.render(h.exports.default,props);await tick();h.render(h.exports.default,props);await tick();assert.equal(writes,0);assert.doesNotMatch(text(h.tree),/foreign-secret/);h.unmount();}
});
test('compiled Company Map exposes dense real hierarchy with independent duties and no coverage ratio',()=>{
 const f=fixture(),p=projection.buildOrganizationProjection(f),h=scene('org',{},runtime());h.render(h.exports.CompanyMap,{projection:p,query:'',setQuery(){}});assert.match(text(h.tree),/实际部门.*同型业务1.*2 项职责 · 1 名员工/);assert.doesNotMatch(text(h.tree),/1\/2|2\/2|已配置/);assert.ok(nodes(h.tree,n=>n.props.href==='/ceo-office/workspace?workspace_id=wb1').length);h.unmount();
});
test('compiled Work keeps its real control and draft when opening employee details',async()=>{
 let controls=0;const h=scene('work',{}),props={companyId:'A',work:{work_ref:'work',workspaceId:'w',problem:'原问题',expected_result:'原交付',status:'ACTIVE',lifecycle_status:'ACTIVE',result_refs:[],responsibility_holder_ref:'e',responsibility_holder_name:'用户姓名'},api:{controlWork:async(c,w,action,reason)=>{assert.equal(action,'pause');assert.equal(reason,'真实暂停原因');controls++;}},onRefresh:async()=>{},onEmployeeDetail(){},onDiscuss(){}};
 h.render(h.exports.default,props);button(h.tree,'暂停工作').props.onClick();h.render(h.exports.default,props);nodes(h.tree,n=>n.type==='textarea')[0].props.onChange({target:{value:'真实暂停原因'}});h.render(h.exports.default,props);nodes(h.tree,n=>n.props['aria-label']==='查看负责人详情')[0].props.onClick();h.render(h.exports.default,props);assert.equal(nodes(h.tree,n=>n.type==='textarea')[0].props.value,'真实暂停原因');await nodes(h.tree,n=>n.type==='form')[0].props.onSubmit({preventDefault(){}});assert.equal(controls,1);assert.ok(nodes(h.tree,n=>n.type==='a'&&n.props.href==='/ceo-office/workspace?workspace_id=w').length);h.unmount();
});
test('compiled General current Work caller uses the existing D1 typed route without team or execution writes',async()=>{
 let writes=0;const data={company:{company_id:'A'},workspace:{workspace_id:'w',name:'实际工作空间'},business:{positioning:'当前业务'},goal:'原目标',operating_readiness:{status:'READY_FOR_WORK',reason:'当前责任',next_action:'核对工作'},team:{employees:[{employee_ref:'e',name:'真实员工'}]},results:[],current_work:[{work_ref:'work',problem:'原问题',status:'ACTIVE',lifecycle_status:'ACTIVE',result_refs:[],evidence_refs:[],artifact_refs:[],handoffs:[]}]};
 const h=scene('general',{getGeneralWorkspace:async()=>data,materializeGeneralWorkspaceTeam:async()=>{writes++;},executeGeneralWorkspaceWork:async()=>{writes++;}},runtime());const props={companyId:'A',workspaceId:'w',parentPath:{company:{name:'A'},department:{name:'部门'},business:{name:'业务'}}};h.render(h.exports.default,props);await tick();h.render(h.exports.default,props);const link=nodes(h.tree,n=>text(n)==='查看工作详情'&&n.props.href)[0];assert.equal(link.props.href,'/ceo-office?view=work&work_ref=work&workspace_id=w');assert.equal(writes,0);h.unmount();
});
