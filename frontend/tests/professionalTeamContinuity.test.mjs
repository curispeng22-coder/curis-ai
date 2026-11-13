import assert from "node:assert/strict";
import test from "node:test";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import vm from "node:vm";

const require = createRequire(import.meta.url), React = require("react");
const musicState = await import("../lib/musicState.mjs");
const cgState = await import("../lib/contentGrowthState.mjs");
const writingState = await import("../lib/writingState.mjs");
const { validateMusicReturn, musicRepairHref } = await import("../lib/musicApi.js");
const { cgRepairHref } = await import("../lib/contentGrowthApi.js");
const swc = require("next/dist/build/swc");
await swc.loadBindings();
const sources = {music:"components/music/MusicMain.js",cg:"components/content-growth/ContentGrowthMain.js",business:"app/ceo-office/business/page.js"};
const compiled = {};
for (const [name, path] of Object.entries(sources)) {
  compiled[name] = (await swc.transform(readFileSync(new URL(`../${path}`, import.meta.url), "utf8"), {
    filename: path, isModule: true, jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } }, module: { type: "commonjs" },
  })).code;
}

// Drive the actual compiled consumers with deterministic hooks and deferred API reads; no App or DB.
function scene(name, api, runtime = { status: "ready", companyId: "a", snapshot: { company: { name: "A" } } }, query = "") {
  const slots = [], pending = []; let cursor = 0, tree;
  const same = (a, b) => a && b && a.length === b.length && a.every((item, i) => Object.is(item, b[i]));
  const hooks = {
    useState(initial) { const i = cursor++; if (!(i in slots)) slots[i] = { value: typeof initial === "function" ? initial() : initial }; return [slots[i].value, (value) => { slots[i].value = typeof value === "function" ? value(slots[i].value) : value; }]; },
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
    window: { location: { search: query, origin: "http://127.0.0.1:3010" }, sessionStorage: storageAPI, localStorage: storageAPI, requestAnimationFrame: (fn) => fn(), addEventListener() {}, removeEventListener() {} },
    ResizeObserver: class { observe() {} disconnect() {} },
    document: { activeElement: { focus() {} } },
    require: (path) => {
      if (path === "react") return { ...React, ...hooks };
      if (path === "react/jsx-runtime") return require(path);
      if (path === "next/link") return { __esModule: true, default: primitive("a") };
      if (path === "next/navigation") return { useSearchParams: () => new URLSearchParams(api.query || query), useRouter: () => ({ push: (href) => { api.pushed = href; } }), useParams: () => ({ id: "doc" }), usePathname: () => "/ceo-office/knowledge" };
      if (path.includes("RuntimeProvider")) return { useRuntime: () => runtime };
      if (path.includes("WorkspacePaneShell") && api.hostComponent) return { __esModule: true, default: api.hostComponent };
      if (path.includes("TerraShell")) return { __esModule: true, default: primitive("main"), TerraPaneContent };
      if (path.includes("GlobalAssistant")) return { useAssistantPageContext() {} };
      if (path.includes("theme.js")) return { roleLabel: (value) => value };
      if (path.includes("EmployeeAvatar")) return { EmployeeAvatar: primitive("span"), EMPLOYEE_AVATAR_PRESETS: [] };
      if (path.includes("contentGrowthState")) return cgState;
      if (path.includes("writingState")) return writingState;
      if (path.includes("contentGrowthApi")) return {contentGrowthApi:api,cgRepairHref:api.cgRepairHref || cgRepairHref};
      if (path.includes("workspacePackageApi")) return api;
      if (path.endsWith("/api.js")) return {CEO_ID:"ceo"};
      if (path.includes("musicState")) return musicState;
      if (path.includes("musicApi")) return { musicApi: api, validateMusicReturn: (href, company) => validateMusicReturn(href, company, api), musicRepairHref: api.musicRepairHref || musicRepairHref };
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
const identityLinks = (tree) => nodes(tree, (node) => typeof node.props?.["aria-label"] === "string" && node.props["aria-label"].startsWith("查看") && node.props.href?.includes("/organization/employees/"));




const holder={tenant_id:"t",assignment_ref:"author-assignment",company_employee_ref:"employee",name:"用户真实姓名",company_id:"A",workspace_id:"w",scope_type:"WORKSPACE",scope_ref:"w",models:[]};
const scope={tenant_id:"t",company_id:"A",workspace_id:"w",business_id:"b"};
const col={entry:{scope,assignments:[holder],definition:{package_id:musicState.MUSIC_PACKAGE.id,version:musicState.MUSIC_PACKAGE.version,digest:musicState.MUSIC_PACKAGE.digest}},pending_requests:[],media_configured:false};
const lyrics={...scope,entity_id:"lyrics",parent_id:"song",data:{kind:"LyricsVersion",text:"已保存歌词",draft_revision:"1"}},production={...scope,entity_id:"production",parent_id:"song",data:{kind:"ProductionVersion",brief:"原制作"}};
const row={song:{...scope,entity_id:"song",data:{title:"真实歌曲",intention:"创作",lyrics_ref:"lyrics",production_ref:"production"}},lyrics,production,versions:[lyrics,production],candidates:[],assets:[],releases:[]};
test("actual Music current holder is independent of empty recipient and execution",()=>{
 const storage=new Map([[musicState.draftKey("A","w","song"),JSON.stringify({assignment:"stale-recipient"})]]);const h=scene("music",{storage}),props={company:"A",workspaceId:"w",row,entry:{},collection:col,perform:async()=>{},inspect(){}};h.render(h.exports.default,props);h.render(h.exports.default,props);assert.match(text(h.tree),/用户真实姓名/);assert.doesNotMatch(text(h.tree),/歌曲责任待落实/);
 const link=identityLinks(h.tree)[0];assert.equal(identityLinks(h.tree).length,1);assert.equal(link.props.href,musicRepairHref("/ceo-office/organization/employees/employee",musicState.songHref("w",{song:"song",mode:"lyrics",lyrics:"lyrics",production:"production"})));assert.equal(nodes(link,n=>n.props?.employee?.id==="employee").length,1);
 props.collection={...col,entry:{...col.entry,assignments:[{...holder,company_employee_ref:"employee space"}]}};h.render(h.exports.default,props);assert.equal(identityLinks(h.tree)[0].props.href,musicRepairHref("/ceo-office/organization/employees/employee%20space",musicState.songHref("w",{song:"song",mode:"lyrics",lyrics:"lyrics",production:"production"})));props.collection=col;h.render(h.exports.default,props);
 button(h.tree,"与员工讨论").props.onClick();h.render(h.exports.default,props);assert.equal(button(h.tree,"请求文字建议").props.disabled,true);
 for(const assignments of [[],[holder,holder],[{...holder,company_id:"foreign"}],[{...holder,tenant_id:"foreign"}],[{...holder,workspace_id:"foreign"}],[{...holder,enabled:false}],[{...holder,company_employee_ref:""}],[{...holder,company_employee_ref:"."}],[{...holder,company_employee_ref:".."}],[{...holder,company_employee_ref:"\ud800"}],[{...holder,name:""}]]){props.collection={...col,entry:{...col.entry,assignments}};h.render(h.exports.default,props);assert.equal(identityLinks(h.tree).length,0);}
 props.collection=col;h.render(h.exports.default,props);assert.equal(identityLinks(h.tree).length,1);
 h.unmount();
});
test("actual CG current holder never selects a recipient or grants execution",()=>{
 const version={...scope,entity_id:"v",data:{title:"真实内容",topic:"主题",audience:"受众",body:"正文",format:"graphic",references:[],work:{...cgState.defaultCgWork(),assignment_ref:"stale-recipient"}}},content={...scope,entity_id:"content"};const h=scene("cg",{}),props={company:"A",workspaceId:"w",row:{content,version,versions:[version],candidates:[]},entry:{},collection:{entry:{...col.entry,definition:{package_id:cgState.CG_PACKAGE_V02.id,version:cgState.CG_PACKAGE_V02.version,digest:cgState.CG_PACKAGE_V02.digest}},reference_options:[],pending_requests:[],execution_authorized:false,execution_notice:"未授权"},perform:async()=>{},inspect(){},onInspect(){}};h.render(h.exports.default,props);h.render(h.exports.default,props);assert.match(text(h.tree),/用户真实姓名/);
 const link=identityLinks(h.tree)[0];assert.equal(identityLinks(h.tree).length,1);assert.equal(link.props.href,cgRepairHref("/ceo-office/organization/employees/employee",cgState.contentHref("w",{content:"content",version:"v"})));assert.equal(nodes(link,n=>n.props?.employee?.id==="employee").length,1);
 props.collection={...props.collection,entry:{...props.collection.entry,assignments:[{...holder,company_employee_ref:"employee space"}]}};h.render(h.exports.default,props);assert.equal(identityLinks(h.tree)[0].props.href,cgRepairHref("/ceo-office/organization/employees/employee%20space",cgState.contentHref("w",{content:"content",version:"v"})));props.collection={...props.collection,entry:{...props.collection.entry,assignments:[holder]}};h.render(h.exports.default,props);
 button(h.tree,"展开讨论").props.onClick();h.render(h.exports.default,props);assert.equal(button(h.tree,"发送一次建议请求").props.disabled,true);
 for(const assignments of [[],[holder,holder],[{...holder,company_id:"foreign"}],[{...holder,tenant_id:"foreign"}],[{...holder,workspace_id:"foreign"}],[{...holder,enabled:false}],[{...holder,company_employee_ref:""}],[{...holder,company_employee_ref:"."}],[{...holder,company_employee_ref:".."}],[{...holder,company_employee_ref:"\ud800"}],[{...holder,name:""}]]){props.collection={...props.collection,entry:{...props.collection.entry,assignments}};h.render(h.exports.default,props);assert.equal(identityLinks(h.tree).length,0);}
 h.unmount();
});
test("malformed original return stays a plain Employee Bar without hiding Main or enabling execution",()=>{
 const badRepair=()=>{throw Error("original return rejected")};const music=scene("music",{musicRepairHref:badRepair}),musicProps={company:"A",workspaceId:"w",row,entry:{},collection:col,perform:async()=>{},inspect(){}};music.render(music.exports.default,musicProps);assert.equal(identityLinks(music.tree).length,0);assert.match(text(music.tree),/用户真实姓名/);assert.match(text(music.tree),/歌词/);music.unmount();
 const version={...scope,entity_id:"v",data:{title:"真实内容",topic:"主题",audience:"受众",body:"正文",format:"graphic",references:[],work:{...cgState.defaultCgWork(),assignment_ref:"author-assignment"}}},content={...scope,entity_id:"content"};let utility;const cg=scene("cg",{}),props={company:"A",workspaceId:"w",row:{content,version,versions:[version],candidates:[]},entry:{binding:"orphan"},collection:{entry:{...col.entry,definition:{package_id:cgState.CG_PACKAGE_V02.id,version:cgState.CG_PACKAGE_V02.version,digest:cgState.CG_PACKAGE_V02.digest}},reference_options:[],pending_requests:[],execution_authorized:false,execution_notice:"未授权"},perform:async()=>{},onInspect(value){utility=value;}};cg.render(cg.exports.default,props);cg.render(cg.exports.default,props);assert.equal(identityLinks(cg.tree).length,0);assert.match(text(cg.tree),/用户真实姓名/);assert.match(text(cg.tree),/正文/);
 button(cg.tree,"展开讨论").props.onClick();cg.render(cg.exports.default,props);assert.equal(nodes(cg.tree,n=>n.props?.href?.includes("/ceo-office/capabilities")).length,0);assert.equal(button(cg.tree,"发送一次建议请求").props.disabled,true);
 button(cg.tree,"查看与配置").props.onClick();cg.render(cg.exports.default,props);assert.equal(nodes(utility?.content,n=>n.props?.href?.includes("/organization/employees/") || n.props?.href?.includes("/ceo-office/capabilities")).length,0);cg.unmount();
});
test("dot employee refs leave actual Music and CG Bar and selected Utility plain",()=>{
 for(const ref of [".",".."]){
  const dot={...holder,company_employee_ref:ref},musicCollection={...col,entry:{...col.entry,assignments:[dot]}};
  const storage=new Map([[musicState.draftKey("A","w","song"),JSON.stringify({assignment:dot.assignment_ref})]]);
  let musicUtility;const music=scene("music",{storage}),props={company:"A",workspaceId:"w",row,entry:{},collection:musicCollection,perform:async()=>{},inspect(value){musicUtility=value;}};
  music.render(music.exports.default,props);music.render(music.exports.default,props);assert.equal(identityLinks(music.tree).length,0);
  button(music.tree,"责任与能力").props.onClick();music.render(music.exports.default,props);
  assert.equal(nodes(musicUtility?.content,n=>n.props?.href?.includes("/organization/employees/")).length,0);assert.match(text(musicUtility?.content),/员工入口暂不可用/);music.unmount();
  const version={...scope,entity_id:"v",data:{title:"真实内容",topic:"主题",audience:"受众",body:"正文",format:"graphic",references:[],work:{...cgState.defaultCgWork(),assignment_ref:dot.assignment_ref}}},content={...scope,entity_id:"content"};
  let cgUtility;const cg=scene("cg",{}),cgProps={company:"A",workspaceId:"w",row:{content,version,versions:[version],candidates:[]},entry:{},collection:{entry:{...musicCollection.entry,definition:{package_id:cgState.CG_PACKAGE_V02.id,version:cgState.CG_PACKAGE_V02.version,digest:cgState.CG_PACKAGE_V02.digest}},reference_options:[],pending_requests:[],execution_authorized:false,execution_notice:"未授权"},perform:async()=>{},onInspect(value){cgUtility=value;}};
  cg.render(cg.exports.default,cgProps);cg.render(cg.exports.default,cgProps);assert.equal(identityLinks(cg.tree).length,0);
  button(cg.tree,"查看与配置").props.onClick();cg.render(cg.exports.default,cgProps);
  assert.equal(nodes(cgUtility?.content,n=>n.props?.href?.includes("/organization/employees/")).length,0);assert.match(text(cgUtility?.content),/员工入口暂不可用/);cg.unmount();
 }
});
test("valid Music and CG Utility retain the selected recipient separately from current Holder",()=>{
 const recipient={...holder,assignment_ref:"selected-assignment",company_employee_ref:"selected-employee",enabled:false};
 const assignments=[holder,recipient],musicCollection={...col,entry:{...col.entry,assignments}},storage=new Map([[musicState.draftKey("A","w","song"),JSON.stringify({assignment:recipient.assignment_ref})]]);
 let musicUtility;const music=scene("music",{storage}),musicProps={company:"A",workspaceId:"w",row,entry:{},collection:musicCollection,perform:async()=>{},inspect(value){musicUtility=value;}};
 music.render(music.exports.default,musicProps);music.render(music.exports.default,musicProps);
 assert.match(identityLinks(music.tree)[0].props.href,/\/employees\/employee\?/);
 button(music.tree,"责任与能力").props.onClick();music.render(music.exports.default,musicProps);
 const musicLink=nodes(musicUtility?.content,n=>n.props?.href?.includes("/organization/employees/"))[0];
 assert.equal(musicLink.props.href,musicRepairHref("/ceo-office/organization/employees/selected-employee",musicState.songHref("w",{song:"song",mode:"lyrics",lyrics:"lyrics",production:"production"})));music.unmount();
 const version={...scope,entity_id:"v",data:{title:"真实内容",topic:"主题",audience:"受众",body:"正文",format:"graphic",references:[],work:{...cgState.defaultCgWork(),assignment_ref:recipient.assignment_ref}}},content={...scope,entity_id:"content"};
 let cgUtility;const cg=scene("cg",{}),cgProps={company:"A",workspaceId:"w",row:{content,version,versions:[version],candidates:[]},entry:{},collection:{entry:{...musicCollection.entry,definition:{package_id:cgState.CG_PACKAGE_V02.id,version:cgState.CG_PACKAGE_V02.version,digest:cgState.CG_PACKAGE_V02.digest}},reference_options:[],pending_requests:[],execution_authorized:false,execution_notice:"未授权"},perform:async()=>{},onInspect(value){cgUtility=value;}};
 cg.render(cg.exports.default,cgProps);cg.render(cg.exports.default,cgProps);assert.match(identityLinks(cg.tree)[0].props.href,/\/employees\/employee\?/);
 button(cg.tree,"查看与配置").props.onClick();cg.render(cg.exports.default,cgProps);
 const cgLink=nodes(cgUtility?.content,n=>n.props?.href?.includes("/organization/employees/"))[0];
 assert.equal(cgLink.props.href,cgRepairHref("/ceo-office/organization/employees/selected-employee",cgState.contentHref("w",{content:"content",version:"v"})));cg.unmount();
});
test("restored invalid Music lyrics range keeps Main and input while repair links stay plain",()=>{
 const key=musicState.draftKey("A","w","song"),selection={kind:"lyrics",version_ref:"lyrics",draft_revision:"1",start:4,end:2,excerpt:"",locator:"lyrics"};
 const storage=new Map([[key,JSON.stringify({selection,message:"保留原留言",discussion:true,assignment:"author-assignment"})]]);
 let utility;const h=scene("music",{storage}),props={company:"A",workspaceId:"w",row,entry:{},collection:col,perform:async()=>{},inspect(value){utility=value;}};
 h.render(h.exports.default,props);h.render(h.exports.default,props);
 assert.match(text(h.tree),/真实歌曲/);assert.equal(identityLinks(h.tree).length,0);
 assert.equal(nodes(h.tree,n=>n.props?.href?.includes("/ceo-office/capabilities")).length,0);
 assert.equal(nodes(h.tree,n=>n.type==="textarea" && n.props?.value==="保留原留言").length,1);
 assert.equal(button(h.tree,"请求文字建议").props.disabled,true);
 button(h.tree,"责任与能力").props.onClick();h.render(h.exports.default,props);
 assert.equal(nodes(utility?.content,n=>n.props?.href?.includes("/organization/employees/")).length,0);
 assert.equal(JSON.parse(storage.get(key)).selection.start,4);
 h.unmount();
});
test("actual explicit completion retains UNKNOWN request and only reads current roster",async()=>{
 const p=musicState.MUSIC_PACKAGE,detail={package:{package_id:p.id,version:p.version,digest:p.digest,schema_version:"curis.workspace-package/v1"},instance:{company_id:"A",workspace_id:"w",package_id:p.id,package_version:p.version,package_digest:p.digest,status:"ACTIVE"},schemas:{MusicSong:{schemaVersion:p.version}},read_only:false};let calls=0,reads=0;const storage=new Map(),api={storage,getInstalledWorkspace:async()=>detail,completeInstalledWorkspaceInitialTeam:async()=>{calls++;throw Error("response lost");}};const h=scene("business",api),props={companyId:"A",business:{business_id:"b",workspaces:[{workspace_id:"w"}]},onChanged(){reads++;}};const render=()=>h.render(h.exports.InitialTeamCompletion,props);render();await tick();render();nodes(h.tree,n=>n.type==="input")[0].props.onChange({target:{checked:true}});render();await button(h.tree,"确认补齐初始团队").props.onClick();render();assert.equal(calls,1);assert.equal(button(h.tree,"确认补齐初始团队").props.disabled,true);button(h.tree,"只读查询当前团队").props.onClick();render();assert.equal(reads,1);assert.equal(calls,1);h.unmount();const restored=scene("business",api);restored.render(restored.exports.InitialTeamCompletion,props);await tick();restored.render(restored.exports.InitialTeamCompletion,props);assert.equal(button(restored.tree,"确认补齐初始团队").props.disabled,true);assert.equal(calls,1);restored.unmount();
});

test("actual completion consumer drops late foreign detail after unmount",async()=>{
 const read=deferred(),h=scene("business",{getInstalledWorkspace:()=>read.promise});let changed=0;const props={companyId:"A",business:{business_id:"b",workspaces:[{workspace_id:"w"}]},onChanged(){changed++;}};h.render(h.exports.InitialTeamCompletion,props);h.unmount();read.resolve({instance:{company_id:"foreign",workspace_id:"w"}});await tick();h.render(h.exports.InitialTeamCompletion,props);assert.equal(button(h.tree,"确认补齐初始团队"),undefined);assert.equal(changed,0);
});
