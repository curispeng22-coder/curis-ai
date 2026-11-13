import assert from "node:assert/strict";
import test from "node:test";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import vm from "node:vm";
import { pathToFileURL } from "node:url";

const frontendRoot = process.env.CURIS_MUSIC_TEST_FRONTEND_ROOT ? pathToFileURL(process.env.CURIS_MUSIC_TEST_FRONTEND_ROOT.replace(/\/$/, "") + "/") : new URL("../", import.meta.url);
const require = createRequire(new URL("package.json", frontendRoot)), React = require("react");
const musicState = await import(process.env.CURIS_MUSIC_RELEASE_NEGATIVE_ROOT ? new URL("lib/musicState.mjs", pathToFileURL(process.env.CURIS_MUSIC_RELEASE_NEGATIVE_ROOT + "/")) : new URL("../lib/musicState.mjs", import.meta.url));
const { validateMusicReturn, prepareLocalWav, verifiedAudioBlob } = await import(new URL("lib/musicApi.js", frontendRoot));
const swc = require("next/dist/build/swc");
await swc.loadBindings();
const sources = { workspace: "components/music/MusicWorkspace.js", main: "components/music/MusicMain.js", host: "components/workspace/WorkspacePaneShell.js" };
const compiled = {};
for (const [name, path] of Object.entries(sources)) {
  const root = name === "host" ? frontendRoot : process.env.CURIS_MUSIC_RELEASE_NEGATIVE_ROOT ? pathToFileURL(process.env.CURIS_MUSIC_RELEASE_NEGATIVE_ROOT + "/") : new URL("../", import.meta.url);
  compiled[name] = (await swc.transform(readFileSync(new URL(path, root), "utf8"), {
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
    sessionStorage: storageAPI, localStorage: storageAPI,
    requestAnimationFrame: (fn) => fn(), scrollTo() {},
    window: { history:{replaceState(_a,_b,href){api.comparisonHref=href;}}, location: { search: query, origin: "http://127.0.0.1:3010" }, sessionStorage: storageAPI, localStorage: storageAPI, requestAnimationFrame: (fn) => fn(), addEventListener() {}, removeEventListener() {} },
    ResizeObserver: class { observe() {} disconnect() {} },
    document: { activeElement: { focus() {} } },
    require: (path) => {
      if (path === "react") return { ...React, ...hooks };
      if (path === "react/jsx-runtime") return require(path);
      if (path === "next/link") return { __esModule: true, default: primitive("a") };
      if (path === "next/navigation") return { useSearchParams: () => new URLSearchParams(api.query || query), useRouter: () => ({ push: (href) => { api.pushed = href; } }), useParams: () => ({ id: "doc" }), usePathname: () => "/ceo-office/knowledge" };
      if (path.includes("v1FrontendApi")) return { getAssignedAgentWorkflow: api.getAssignedAgentWorkflow || (async () => ({ state: "READY" })), publishAssignedAgentWorkflow: api.publishAssignedAgentWorkflow || (async () => ({})), createAssignedWork: api.createAssignedWork };
      if (path.includes("RuntimeProvider")) return { useRuntime: () => runtime };
      if (path.includes("WorkspacePaneShell") && api.hostComponent) return { __esModule: true, default: api.hostComponent };
      if (path.includes("TerraShell")) return { __esModule: true, default: primitive("main"), TerraPaneContent };
      if (path.includes("GlobalAssistant")) return { useAssistantPageContext() {} };
      if (path.includes("theme.js")) return { roleLabel: (value) => value };
      if (path.includes("EmployeeAvatar")) return { EmployeeAvatar: primitive("span"), EMPLOYEE_AVATAR_PRESETS: [] };
      if (path.includes("musicState")) return musicState;
      if (path.includes("musicApi")) return { musicApi: api, prepareLocalWav, verifiedAudioBlob, validateMusicReturn: (href, company) => validateMusicReturn(href, company, api), musicRepairHref: (path, href) => `${path}?return_to=${encodeURIComponent(href)}` };
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




const scope = {tenant_id:"t",company_id:"A",workspace_id:"w",business_id:"b"};
const definition = {package_id:musicState.MUSIC_PACKAGE.id,version:musicState.MUSIC_PACKAGE.version,digest:musicState.MUSIC_PACKAGE.digest};
const entry = {scope,definition,actor:"ceo",assignments:[]};
const detail = {package:{...definition,schema_version:"curis.workspace-package/v1"},instance:{company_id:"A",workspace_id:"w",instance_id:"i",package_id:definition.package_id,package_version:definition.version,package_digest:definition.digest},schemas:{MusicSong:{schemaVersion:"0.2.0"}}};
const version = (id,kind,data={}) => ({...scope,entity_id:id,parent_id:"music-song-A",data:{kind,...data}});
function songRow() {
 const lyrics=version("lyrics-new","LyricsVersion",{text:"当前歌词",draft_revision:"2"}),production=version("prod-new","ProductionVersion",{brief:"当前制作"});
 const oldLyrics=version("lyrics-old","LyricsVersion",{text:"候选固定原歌词",draft_revision:"1"}),oldProduction=version("prod-old","ProductionVersion",{brief:"候选固定原制作"});
 const candidate=version("candidate-old","Candidate",{title:"本地候选A",lyrics_ref:oldLyrics.entity_id,production_ref:oldProduction.entity_id,suggestion:"独立文字建议"});
 return {song:{...scope,entity_id:"music-song-A",data:{title:"真实歌曲",intention:"本次创作意图",lyrics_ref:lyrics.entity_id,production_ref:production.entity_id,master_ref:"",schemaVersion:"0.2.0"}},lyrics,production,versions:[lyrics,production,oldLyrics,oldProduction,candidate],candidates:[candidate],assets:[],releases:[],choice:null,master:null};
}
const collection = row => ({entry,songs:row ? [row] : [],pending_requests:[],media_configured:false});
const operating = records => ({entry,records,report_current:{}});
const apiFor = row => ({collection:async()=>collection(row),content:async()=>row,operating:async()=>operating([])});
const propsFor = row => ({company:"A",workspaceId:"w",row,entry:{},collection:collection(row),perform:async()=>{},inspect(){},busy:false,locked:false});
const visibleText = tree => {
 if (tree == null || typeof tree === "boolean") return ""; if (typeof tree !== "object") return String(tree); if (Array.isArray(tree)) return tree.map(visibleText).join(""); if (tree.props?.hidden) return "";return visibleText(tree.props?.children);
};

test("Music B3 actual Main preserves fixed candidate basis, hides discussion and separates Choice/Master",()=>{
 const row=songRow(),h=scene("main",{}),props=propsFor(row);let panel;props.inspect=value=>{panel=value;};
 const render=()=>h.render(h.exports.default,props);render();render();
 assert.doesNotMatch(visibleText(h.tree),/讨论当前歌曲|给员工的留言/);assert.match(visibleText(h.tree),/当前歌曲责任不可用或尚未安排/);
 assert.equal(nodes(h.tree,n=>n.type==="select" && text(n).includes("选择当前责任员工")).length,0);
 assert.match(visibleText(h.tree),/候选固定原歌词/);assert.match(visibleText(h.tree),/候选固定原制作/);
 button(h.tree,"责任与能力").props.onClick();render();assert.equal(panel.id,"employee-selection");assert.match(text(panel.content),/当前没有合法歌曲责任员工/);
 button(h.tree,"与员工讨论").props.onClick();render();const input=nodes(h.tree,n=>n.type==="textarea"&&n.props.maxLength===2000&&n.props.value==="")[0];input.props.onChange({target:{value:"保留这次留言"}});render();button(h.tree,"收起讨论").props.onClick();render();assert.doesNotMatch(visibleText(h.tree),/保留这次留言/);button(h.tree,"与员工讨论").props.onClick();render();assert.ok(nodes(h.tree,n=>n.type==="textarea"&&n.props.value==="保留这次留言").length);
 assert.equal(button(h.tree,"选择此候选"),undefined);assert.match(visibleText(h.tree),/文字建议，无音频/);assert.match(visibleText(h.tree),/先实际试听，再选择候选/);
 props.row={...row,versions:row.versions.filter(v=>v.entity_id!=="lyrics-old")};render();assert.match(visibleText(h.tree),/候选原歌词暂不可读取/);assert.doesNotMatch(text(nodes(h.tree,n=>n.props.className==="comparison")[0]),/当前歌词/);h.unmount();
});

test("Music B3 actual operating collections open explicit forms, cancel retains scoped draft and fixed learning",()=>{
 const ref={...scope,entity_id:"music-learning-original",data:{kind:"Learning",identity_ref:"learning-i",revision:1,title:"原经验",body:"固定学习内容",applicability:"仅本场景",counterexample:"反例边界",accepted_by:"ceo",report_ref:"music-report-original"}};
 const newer={...ref,entity_id:"music-learning-new",data:{...ref.data,revision:2,title:"更新经验",body:"后续经验"}};
 const h=scene("workspace",{}),props={company:"A",workspaceId:"w",songs:[],entry:{view:"learning",object:ref.entity_id},collection:operating([ref,newer]),load:async()=>{},locked:false};
 const render=()=>h.render(h.exports.MusicOperatingMain,props);render();render();assert.match(text(h.tree),/固定学习内容|仅本场景|反例边界/);assert.equal(nodes(h.tree,n=>n.type==="form").length,0);
 assert.equal(button(h.tree,"修订这版依据").props.disabled,true);
 props.entry={view:"learning",object:newer.entity_id};h.unmount();const h2=scene("workspace",{});const r=()=>h2.render(h2.exports.MusicOperatingMain,props);r();r();button(h2.tree,"修订这版依据").props.onClick();r();const title=nodes(h2.tree,n=>n.type==="input"&&n.props["aria-label"]==="标题")[0];title.props.onChange({target:{value:"尚未提交的新标题"}});r();button(h2.tree,"取消编辑").props.onClick();r();assert.equal(nodes(h2.tree,n=>n.type==="form").length,0);button(h2.tree,"修订这版依据").props.onClick();r();assert.equal(nodes(h2.tree,n=>n.type==="input"&&n.props["aria-label"]==="标题")[0].props.value,"尚未提交的新标题");h2.unmount();
});

test("Music B3 actual workspace scopes late data and selects Utility in real host then closes/reopens",async()=>{
 const row=songRow(),api={...apiFor(row),query:"music_song=music-song-A"},parent=scene("workspace",api),host=scene("host",{});api.hostComponent=host.exports.default;
 const paint=()=>{parent.render(parent.exports.default,{detail,workspaceId:"w"});host.render(host.exports.default,parent.tree.props);host.render(host.exports.default,parent.tree.props);};paint();await tick();paint();await tick();paint();
 assert.equal(parent.tree.props.utilityAvailable,false);const child=nodes(parent.tree,n=>n.type.name==="MusicMain")[0];assert.ok(child);
 child.props.inspect("candidate-old");paint();let panel=nodes(host.tree,n=>n.props.role==="tabpanel")[0];assert.equal(panel.props.hidden,false);assert.match(text(panel),/候选固定原歌词/);assert.equal(parent.tree.props.utilityRequestTabId,"music-version:candidate-old");nodes(host.tree,n=>n.props.label==="收起辅助内容")[0].props.onClick();paint();assert.equal(nodes(host.tree,n=>n.type==="section"&&n.props["aria-label"]==="辅助内容")[0].props.hidden,true);child.props.inspect("candidate-old");paint();assert.equal(nodes(host.tree,n=>n.props.role==="tabpanel")[0].props.hidden,false);parent.unmount();host.unmount();
 const old=deferred(),foreign={...collection(row),entry:{...entry,scope:{...scope,company_id:"foreign"}}},h=scene("workspace",{collection:()=>old.promise});h.render(h.exports.default,{detail,workspaceId:"w"});h.unmount();old.resolve(foreign);await tick();h.render(h.exports.default,{detail,workspaceId:"w"});assert.doesNotMatch(text(h.tree),/真实歌曲/);assert.equal(h.tree.props.utilityAvailable,false);
});

test("Music B3 actual directory and release preserve song/pack identities without fabricated publication",()=>{
 const row=songRow(),master=version("master-old","MasterRevision",{lyrics_ref:"lyrics-old",production_ref:"prod-old"}),pack=version("pack-old","ReleasePackage",{title:"本地原包",master_ref:master.entity_id,credits:"原署名与用途"});row.versions.push(master,pack);row.releases=[pack];
 const h=scene("workspace",{});h.render(h.exports.MusicReleaseMain,{workspaceId:"w",songs:[row],entry:{song:row.song.entity_id,release:pack.entity_id}});assert.match(text(h.tree),/原署名与用途/);assert.match(text(h.tree),/仅准备 · 未发布/);assert.match(text(h.tree),/本地准备包未发布/);assert.doesNotMatch(text(h.tree),/真实收益/);
 const href=nodes(h.tree,n=>n.type==="function"||n.props?.href).map(n=>n.props.href).find(x=>x?.includes("music_release"));assert.equal(musicState.musicReturnTarget(href).entry.release,pack.entity_id);
 const d=scene("workspace",{});const props={workspaceId:"w",collection:collection(row),creating:false,setCreating(){},busy:false,locked:false};d.render(d.exports.MusicSongDirectory,props);assert.match(text(d.tree),/真实歌曲/);nodes(d.tree,n=>n.type==="input")[0].props.onChange({target:{value:"不匹配"}});d.render(d.exports.MusicSongDirectory,props);assert.match(text(d.tree),/没有匹配的歌曲/);assert.doesNotMatch(text(d.tree),/继续制作 →/);d.unmount();
});

test("Music B3 actual playable candidate requires playback and independent Choice before Master",()=>{
 const row=songRow(),asset=version("asset-current","AudioAssetVersion",{sha256:"a".repeat(64),duration:32}),candidate=version("candidate-current","Candidate",{title:"准确候选",lyrics_ref:row.lyrics.entity_id,production_ref:row.production.entity_id,asset_ref:asset.entity_id});row.versions.push(asset,candidate);row.candidates=[candidate];row.assets=[asset];
 const h=scene("main",{}),props=propsFor(row),render=()=>h.render(h.exports.default,props);render();render();assert.equal(button(h.tree,"选择此候选").props.disabled,true);assert.equal(button(h.tree,"明确确认成品版本").props.disabled,true);
 const player=nodes(h.tree,n=>n.type.name==="AudioPlayer")[0];player.props.onState({ready:true,position:4,duration:32,paused:true});render();assert.equal(button(h.tree,"选择此候选").props.disabled,true);player.props.onState({ready:true,played:true,position:4,duration:32,paused:true});render();assert.equal(button(h.tree,"选择此候选").props.disabled,false);assert.equal(button(h.tree,"明确确认成品版本").props.disabled,true);
 props.row={...row,choice:version("choice-current","HumanChoice",{candidate_ref:candidate.entity_id})};render();assert.equal(button(h.tree,"明确确认成品版本").props.disabled,false);props.row={...props.row,choice:version("choice-other","HumanChoice",{candidate_ref:"other"})};render();assert.equal(button(h.tree,"明确确认成品版本").props.disabled,true);h.unmount();
});

const savedQASong03 = {"song": {"entity_id": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299", "tenant_id": "selfuse", "company_id": "company-096d260b-e474-4eb7-b419-e617dfd1db05", "workspace_id": "workspace-package-cc7d2a23-e130-44ba-9d27-236b1a2795e2", "parent_id": "workspace-package-cc7d2a23-e130-44ba-9d27-236b1a2795e2", "data": {"title": "QA Music 无音频文本保存一", "intention": "仅验证歌词与制作描述保存、固定原版本、片段选择和返回；不生成音频、不宣称试听或发布。", "lyrics_ref": "music-14170392-ef1a-41da-81e6-41cdc2103414", "production_ref": "music-a5977d9d-bae8-4235-a759-2e093b092843", "choice_ref": "", "master_ref": "", "direction_ref": "", "learning_ref": "", "packageId": "com.curis.local.music", "packageVersion": "0.2.0", "schemaVersion": "0.2.0", "objectType": "MusicSong", "kind": "Song", "payload_sha256": "11e47b3caa6bfc286c7450cd27b3719f1af08ed1a664812b3810bd4a090f7f39"}}, "lyrics": {"entity_id": "music-14170392-ef1a-41da-81e6-41cdc2103414", "tenant_id": "selfuse", "company_id": "company-096d260b-e474-4eb7-b419-e617dfd1db05", "workspace_id": "workspace-package-cc7d2a23-e130-44ba-9d27-236b1a2795e2", "parent_id": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299", "data": {"text": "窗沿留着夜里的风\n我把清晨写成一封信\n慢慢走向有光的地方\n把未说的话留给下一行", "previous_ref": "music-92ce68e9-7fff-40c0-8e1f-aa331fa1f57e", "draft_revision": "0305df5c-9b52-4982-a210-406f7a2b7b1e", "packageId": "com.curis.local.music", "packageVersion": "0.2.0", "schemaVersion": "0.2.0", "objectType": "MusicSong", "kind": "LyricsVersion", "payload_sha256": "4c3453e333123f94cd4964bf0965a36a31b0013fd1367ea6d0e78e4d6a2cd8fe", "song_ref": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299"}}, "production": {"entity_id": "music-a5977d9d-bae8-4235-a759-2e093b092843", "tenant_id": "selfuse", "company_id": "company-096d260b-e474-4eb7-b419-e617dfd1db05", "workspace_id": "workspace-package-cc7d2a23-e130-44ba-9d27-236b1a2795e2", "parent_id": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299", "data": {"brief": "本地文本审阅：主歌四行，末行作为后续创作留白；制作方向保留克制器乐。本轮无音频、未试听、未选版，歌词演唱匹配和商用许可均未验证。", "previous_ref": "music-0e54e4b1-4ba2-450e-bafa-eaae8290d00f", "draft_revision": "cad3b133-f286-4e43-903f-5af8c405edd0", "packageId": "com.curis.local.music", "packageVersion": "0.2.0", "schemaVersion": "0.2.0", "objectType": "MusicSong", "kind": "ProductionVersion", "payload_sha256": "5686f2b408e54879f426699d749a1fbeb6681915b7e090cb3f9f89d25b2441d1", "song_ref": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299"}}, "choice": null, "master": null, "versions": [{"entity_id": "music-92ce68e9-7fff-40c0-8e1f-aa331fa1f57e", "tenant_id": "selfuse", "company_id": "company-096d260b-e474-4eb7-b419-e617dfd1db05", "workspace_id": "workspace-package-cc7d2a23-e130-44ba-9d27-236b1a2795e2", "parent_id": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299", "data": {"text": "窗沿留着夜里的风\n我把清晨写成一封信\n慢慢走向有光的地方", "previous_ref": "", "draft_revision": "06604f25-25f5-449a-ba8a-93e32e1cb0a5", "packageId": "com.curis.local.music", "packageVersion": "0.2.0", "schemaVersion": "0.2.0", "objectType": "MusicSong", "kind": "LyricsVersion", "payload_sha256": "54faeb3d6cb97b6ab7df6a5fad1349826eec5c6ad8e82aa9611464f49815c120", "song_ref": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299"}}, {"entity_id": "music-0e54e4b1-4ba2-450e-bafa-eaae8290d00f", "tenant_id": "selfuse", "company_id": "company-096d260b-e474-4eb7-b419-e617dfd1db05", "workspace_id": "workspace-package-cc7d2a23-e130-44ba-9d27-236b1a2795e2", "parent_id": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299", "data": {"brief": "本地文本审阅：结构为主歌三行，克制的器乐方向；本轮无音频、不声称歌词演唱匹配或商用许可。", "previous_ref": "", "draft_revision": "06604f25-25f5-449a-ba8a-93e32e1cb0a5", "packageId": "com.curis.local.music", "packageVersion": "0.2.0", "schemaVersion": "0.2.0", "objectType": "MusicSong", "kind": "ProductionVersion", "payload_sha256": "e2a82418edc879020cae71cb03f3a837f80cc50bd5554b6f6bf53f324c31a667", "song_ref": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299"}}, {"entity_id": "music-14170392-ef1a-41da-81e6-41cdc2103414", "tenant_id": "selfuse", "company_id": "company-096d260b-e474-4eb7-b419-e617dfd1db05", "workspace_id": "workspace-package-cc7d2a23-e130-44ba-9d27-236b1a2795e2", "parent_id": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299", "data": {"text": "窗沿留着夜里的风\n我把清晨写成一封信\n慢慢走向有光的地方\n把未说的话留给下一行", "previous_ref": "music-92ce68e9-7fff-40c0-8e1f-aa331fa1f57e", "draft_revision": "0305df5c-9b52-4982-a210-406f7a2b7b1e", "packageId": "com.curis.local.music", "packageVersion": "0.2.0", "schemaVersion": "0.2.0", "objectType": "MusicSong", "kind": "LyricsVersion", "payload_sha256": "4c3453e333123f94cd4964bf0965a36a31b0013fd1367ea6d0e78e4d6a2cd8fe", "song_ref": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299"}}, {"entity_id": "music-a5977d9d-bae8-4235-a759-2e093b092843", "tenant_id": "selfuse", "company_id": "company-096d260b-e474-4eb7-b419-e617dfd1db05", "workspace_id": "workspace-package-cc7d2a23-e130-44ba-9d27-236b1a2795e2", "parent_id": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299", "data": {"brief": "本地文本审阅：主歌四行，末行作为后续创作留白；制作方向保留克制器乐。本轮无音频、未试听、未选版，歌词演唱匹配和商用许可均未验证。", "previous_ref": "music-0e54e4b1-4ba2-450e-bafa-eaae8290d00f", "draft_revision": "cad3b133-f286-4e43-903f-5af8c405edd0", "packageId": "com.curis.local.music", "packageVersion": "0.2.0", "schemaVersion": "0.2.0", "objectType": "MusicSong", "kind": "ProductionVersion", "payload_sha256": "5686f2b408e54879f426699d749a1fbeb6681915b7e090cb3f9f89d25b2441d1", "song_ref": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299"}}], "candidates": [], "assets": [], "releases": []};
const savedQACollection03 = {"entry": {"scope": {"tenant_id": "selfuse", "company_id": "company-096d260b-e474-4eb7-b419-e617dfd1db05", "department_id": "dept-925e9f8e-af77-49d2-99a6-b1a02afa53b1", "business_id": "business-music-review-b7767c0a-8b84-4080-ae2e-149e970dc034", "workspace_id": "workspace-package-cc7d2a23-e130-44ba-9d27-236b1a2795e2", "scope_type": "WORKSPACE", "scope_ref": "workspace-package-cc7d2a23-e130-44ba-9d27-236b1a2795e2"}, "actor": "selfuse-ceo", "definition": {"package_id": "com.curis.local.music", "version": "0.2.0", "digest": "cb05fd21e4237d046e20f0b96a81f6894e71caee95c2b0c6559b91ecf56ec802", "name": "音乐创作工作空间", "published": false, "initial_team_contract": {"version": "1", "decisionSourceSHA256": "74225e91d143f877f708bd5b209bbffd989f2fe07f0f211fa7b926d12c445ce6", "packageId": "com.curis.local.music", "packageVersion": "0.2.0", "packageDigest": "cb05fd21e4237d046e20f0b96a81f6894e71caee95c2b0c6559b91ecf56ec802", "templateId": "official.employee.music.author", "departmentType": "music", "displayName": "歌曲创作负责人", "authorKey": "MUSIC_SONG_AUTHOR", "responsibility": "按歌曲与合法材料创作讨论、版本与约束自检、候选与来源事实交付、方案与后续创作复盘；不授予音频生成或发行能力", "leaderKey": "BUSINESS_LEADER", "leaderResponsibility": "接收业务目标、统筹责任与证据交付、向CEO沟通进展风险与下一步；权限成本和外部效果门交CEO决定", "coverage": ["CREATION", "SELF_CHECK", "DELIVERY", "RETROSPECTIVE"], "sha256": "3d1e3059b34bd65344630502110cc267a07db6f990d1f3d552f641583c17f6b4"}, "scope": "MANUAL_SOURCE_OPERATING_CHAIN_AND_LOCAL_SONG", "notice": "人工保存的经营依据与本地歌曲创作；真实采集、音频生成、商业权利和发行尚未验收。"}, "blueprint_version": "0.2.0", "assignments": [], "publication_status": "INTERNAL_CANDIDATE_NO_PUBLICATION"}, "songs": [{"song": {"entity_id": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299", "tenant_id": "selfuse", "company_id": "company-096d260b-e474-4eb7-b419-e617dfd1db05", "workspace_id": "workspace-package-cc7d2a23-e130-44ba-9d27-236b1a2795e2", "parent_id": "workspace-package-cc7d2a23-e130-44ba-9d27-236b1a2795e2", "data": {"title": "QA Music 无音频文本保存一", "intention": "仅验证歌词与制作描述保存、固定原版本、片段选择和返回；不生成音频、不宣称试听或发布。", "lyrics_ref": "music-14170392-ef1a-41da-81e6-41cdc2103414", "production_ref": "music-a5977d9d-bae8-4235-a759-2e093b092843", "choice_ref": "", "master_ref": "", "direction_ref": "", "learning_ref": "", "packageId": "com.curis.local.music", "packageVersion": "0.2.0", "schemaVersion": "0.2.0", "objectType": "MusicSong", "kind": "Song", "payload_sha256": "11e47b3caa6bfc286c7450cd27b3719f1af08ed1a664812b3810bd4a090f7f39"}}, "lyrics": {"entity_id": "music-14170392-ef1a-41da-81e6-41cdc2103414", "tenant_id": "selfuse", "company_id": "company-096d260b-e474-4eb7-b419-e617dfd1db05", "workspace_id": "workspace-package-cc7d2a23-e130-44ba-9d27-236b1a2795e2", "parent_id": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299", "data": {"text": "窗沿留着夜里的风\n我把清晨写成一封信\n慢慢走向有光的地方\n把未说的话留给下一行", "previous_ref": "music-92ce68e9-7fff-40c0-8e1f-aa331fa1f57e", "draft_revision": "0305df5c-9b52-4982-a210-406f7a2b7b1e", "packageId": "com.curis.local.music", "packageVersion": "0.2.0", "schemaVersion": "0.2.0", "objectType": "MusicSong", "kind": "LyricsVersion", "payload_sha256": "4c3453e333123f94cd4964bf0965a36a31b0013fd1367ea6d0e78e4d6a2cd8fe", "song_ref": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299"}}, "production": {"entity_id": "music-a5977d9d-bae8-4235-a759-2e093b092843", "tenant_id": "selfuse", "company_id": "company-096d260b-e474-4eb7-b419-e617dfd1db05", "workspace_id": "workspace-package-cc7d2a23-e130-44ba-9d27-236b1a2795e2", "parent_id": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299", "data": {"brief": "本地文本审阅：主歌四行，末行作为后续创作留白；制作方向保留克制器乐。本轮无音频、未试听、未选版，歌词演唱匹配和商用许可均未验证。", "previous_ref": "music-0e54e4b1-4ba2-450e-bafa-eaae8290d00f", "draft_revision": "cad3b133-f286-4e43-903f-5af8c405edd0", "packageId": "com.curis.local.music", "packageVersion": "0.2.0", "schemaVersion": "0.2.0", "objectType": "MusicSong", "kind": "ProductionVersion", "payload_sha256": "5686f2b408e54879f426699d749a1fbeb6681915b7e090cb3f9f89d25b2441d1", "song_ref": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299"}}, "choice": null, "master": null, "versions": [{"entity_id": "music-92ce68e9-7fff-40c0-8e1f-aa331fa1f57e", "tenant_id": "selfuse", "company_id": "company-096d260b-e474-4eb7-b419-e617dfd1db05", "workspace_id": "workspace-package-cc7d2a23-e130-44ba-9d27-236b1a2795e2", "parent_id": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299", "data": {"text": "窗沿留着夜里的风\n我把清晨写成一封信\n慢慢走向有光的地方", "previous_ref": "", "draft_revision": "06604f25-25f5-449a-ba8a-93e32e1cb0a5", "packageId": "com.curis.local.music", "packageVersion": "0.2.0", "schemaVersion": "0.2.0", "objectType": "MusicSong", "kind": "LyricsVersion", "payload_sha256": "54faeb3d6cb97b6ab7df6a5fad1349826eec5c6ad8e82aa9611464f49815c120", "song_ref": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299"}}, {"entity_id": "music-0e54e4b1-4ba2-450e-bafa-eaae8290d00f", "tenant_id": "selfuse", "company_id": "company-096d260b-e474-4eb7-b419-e617dfd1db05", "workspace_id": "workspace-package-cc7d2a23-e130-44ba-9d27-236b1a2795e2", "parent_id": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299", "data": {"brief": "本地文本审阅：结构为主歌三行，克制的器乐方向；本轮无音频、不声称歌词演唱匹配或商用许可。", "previous_ref": "", "draft_revision": "06604f25-25f5-449a-ba8a-93e32e1cb0a5", "packageId": "com.curis.local.music", "packageVersion": "0.2.0", "schemaVersion": "0.2.0", "objectType": "MusicSong", "kind": "ProductionVersion", "payload_sha256": "e2a82418edc879020cae71cb03f3a837f80cc50bd5554b6f6bf53f324c31a667", "song_ref": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299"}}, {"entity_id": "music-14170392-ef1a-41da-81e6-41cdc2103414", "tenant_id": "selfuse", "company_id": "company-096d260b-e474-4eb7-b419-e617dfd1db05", "workspace_id": "workspace-package-cc7d2a23-e130-44ba-9d27-236b1a2795e2", "parent_id": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299", "data": {"text": "窗沿留着夜里的风\n我把清晨写成一封信\n慢慢走向有光的地方\n把未说的话留给下一行", "previous_ref": "music-92ce68e9-7fff-40c0-8e1f-aa331fa1f57e", "draft_revision": "0305df5c-9b52-4982-a210-406f7a2b7b1e", "packageId": "com.curis.local.music", "packageVersion": "0.2.0", "schemaVersion": "0.2.0", "objectType": "MusicSong", "kind": "LyricsVersion", "payload_sha256": "4c3453e333123f94cd4964bf0965a36a31b0013fd1367ea6d0e78e4d6a2cd8fe", "song_ref": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299"}}, {"entity_id": "music-a5977d9d-bae8-4235-a759-2e093b092843", "tenant_id": "selfuse", "company_id": "company-096d260b-e474-4eb7-b419-e617dfd1db05", "workspace_id": "workspace-package-cc7d2a23-e130-44ba-9d27-236b1a2795e2", "parent_id": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299", "data": {"brief": "本地文本审阅：主歌四行，末行作为后续创作留白；制作方向保留克制器乐。本轮无音频、未试听、未选版，歌词演唱匹配和商用许可均未验证。", "previous_ref": "music-0e54e4b1-4ba2-450e-bafa-eaae8290d00f", "draft_revision": "cad3b133-f286-4e43-903f-5af8c405edd0", "packageId": "com.curis.local.music", "packageVersion": "0.2.0", "schemaVersion": "0.2.0", "objectType": "MusicSong", "kind": "ProductionVersion", "payload_sha256": "5686f2b408e54879f426699d749a1fbeb6681915b7e090cb3f9f89d25b2441d1", "song_ref": "music-ddd72b2b-02b1-4e97-9403-c7a27eb38299"}}], "candidates": [], "assets": [], "releases": []}], "pending_requests": [], "media_configured": false};

test("Music B3 correction populated connected directory-song-history-directory return cannot render stale anchors",async()=>{
 const row=savedQASong03,col=savedQACollection03,w=row.song.workspace_id,c=row.song.company_id,api={collection:async()=>col,content:async()=>row,operating:async()=>({entry:col.entry,records:[],report_current:{}}),query:`music_song=${row.song.entity_id}`};
 const props={workspaceId:w,detail:{package:{...col.entry.definition,schema_version:"curis.workspace-package/v1"},instance:{company_id:c,workspace_id:w,instance_id:"actual-instance",package_id:col.entry.definition.package_id,package_version:col.entry.definition.version,package_digest:col.entry.definition.digest},schemas:{MusicSong:{schemaVersion:"0.2.0"}}}};
 const parent=scene("workspace",api),render=()=>parent.render(parent.exports.default,props);render();await tick();render();await tick();render();
 let main=nodes(parent.tree,n=>n.type.name==="MusicMain")[0];assert.equal(main.props.row.versions.length,4);main.props.inspect(row.versions[0].entity_id);render();let panel=parent.tree.props.utilityTabs[0].content;assert.match(text(panel),/窗沿留着夜里的风/);assert.match(text(panel),/不适用：这版只保存歌词/);assert.doesNotMatch(text(panel),/原制作依据暂不可读取/);assert.doesNotMatch(text(panel),/把未说的话留给下一行/);button(panel,"结束查看").props.onClick();render();assert.equal(parent.tree.props.utilityAvailable,false);
 api.query="music_view=songs";assert.doesNotThrow(render);await tick();render();assert.ok(nodes(parent.tree,n=>n.type.name==="MusicSongDirectory")[0]);assert.equal(nodes(parent.tree,n=>n.type.name==="MusicMain").length,0);
 api.query=`music_song=${row.song.entity_id}&music_mode=history`;assert.doesNotThrow(render);await tick();render();await tick();render();main=nodes(parent.tree,n=>n.type.name==="MusicMain")[0];assert.equal(main.props.entry.mode,"history");main.props.inspect(row.versions[1].entity_id);render();assert.match(text(parent.tree.props.utilityTabs[0].content),/原制作/);api.query="music_view=songs";assert.doesNotThrow(render);await tick();render();assert.ok(nodes(parent.tree,n=>n.type.name==="MusicSongDirectory")[0]);parent.unmount();
});

test("Music B3 correction actual saved history distinguishes production versions and creation replaces directory scaffold",()=>{
 const row=savedQASong03,col=savedQACollection03,h=scene("main",{}),props={...propsFor(row),company:row.song.company_id,workspaceId:row.song.workspace_id,collection:col,entry:{mode:"history"}};h.render(h.exports.default,props);h.render(h.exports.default,props);assert.ok(button(h.tree,"制作 v1"));assert.ok(button(h.tree,"制作 v2"));assert.ok(button(h.tree,"歌词 v1"));assert.ok(button(h.tree,"歌词 v2"));h.unmount();
 const d=scene("workspace",{});d.render(d.exports.MusicSongDirectory,{workspaceId:row.song.workspace_id,collection:col,creating:true,setCreating(){},busy:false,locked:false,createMain:React.createElement("form",{},"实际新歌编辑区")});assert.doesNotMatch(text(d.tree),/查找歌曲|作品状态|首歌曲|新建歌曲/);assert.equal(nodes(d.tree,n=>n.props.className==="panel").length,0);assert.match(text(d.tree),/返回歌曲目录|实际新歌编辑区/);d.unmount();
});

test("normal Music input is visible only for configured user media and manual Candidate stays nonaudio",()=>{
 const row=songRow(),h=scene('main',{}),props=propsFor(row);props.collection={...props.collection,user_media_configured:true};h.render(h.exports.default,props);h.render(h.exports.default,props);assert.equal(nodes(h.tree,n=>n.type==='input'&&n.props.type==='file').length,1);assert.match(text(h.tree),/导入本机 WAV/);assert.match(text(h.tree),/商业权利与演唱匹配未核验/);assert.match(text(h.tree),/保存人工文字候选/);assert.equal(button(h.tree,'保存文字候选').props.disabled,true);h.unmount();
});

test('delayed POST unseen by GET cannot be replaced with a different file; applied receipt releases it',async()=>{
 const row=songRow();let posts=0,status='UNKNOWN';const requests=[];const api={...apiFor(row),query:'music_song=music-song-A',importAudio:async(c,w,r,p)=>{posts++;requests.push(p);throw Error('response lost before server received POST');},importStatus:async()=>({status,basis:musicState.songBasis(row),...row})};
 const h=scene('workspace',api),render=()=>h.render(h.exports.default,{detail,workspaceId:'w'});render();await tick();render();await tick();render();const main=()=>nodes(h.tree,n=>n.type.name==='MusicMain')[0];
 const data={title:'原音频',sha256:'a'.repeat(64),size:4},base=musicState.songBasis(row),bytes=new Uint8Array([1,2,3,4]);await assert.rejects(main().props.perform('import-audio',data,base,bytes),/response lost/);render();
 await assert.rejects(main().props.perform('import-audio',data,base,bytes),/尚未确认/);assert.equal(posts,1);render();
 status='NOT_APPLIED';const changed={...data,title:'另一文件',sha256:'b'.repeat(64)};await assert.rejects(main().props.perform('import-audio',changed,base,bytes),/尚未确认/);assert.equal(posts,1);render();
 // Original POST may now arrive and commit. Querying APPLIED must not POST again.
 status='APPLIED';await main().props.perform('import-audio',data,base,bytes);render();assert.equal(posts,1);assert.equal(main().props.busy,false);h.unmount();
});
test('confirmed stale immutable basis permits new input; fresh typed refusal does not leave an unknown lock',async()=>{
 const row=songRow();let posts=0,basis=musicState.songBasis(row);const api={...apiFor(row),query:'music_song=music-song-A',importAudio:async()=>{posts++;if(posts===1)throw Error('unknown');return row;},importStatus:async()=>({status:'NOT_APPLIED',basis})};const h=scene('workspace',api),render=()=>h.render(h.exports.default,{detail,workspaceId:'w'});render();await tick();render();await tick();render();const main=()=>nodes(h.tree,n=>n.type.name==='MusicMain')[0];const bytes=new Uint8Array([1]),data={title:'原文件',sha256:'a'.repeat(64),size:1};await assert.rejects(main().props.perform('import-audio',data,basis,bytes));render();basis={...basis,lyrics_ref:'new-immutable-version'};await main().props.perform('import-audio',{...data,title:'新文件'},basis,bytes);assert.equal(posts,2);h.unmount();
});
test('actual upload completion after navigation releases busy and cannot navigate/write old view',async()=>{
 const row=songRow(),gate=deferred();const api={...apiFor(row),query:'music_song=music-song-A',importAudio:()=>gate.promise};const h=scene('workspace',api),render=()=>h.render(h.exports.default,{detail,workspaceId:'w'});render();await tick();render();await tick();render();const main=nodes(h.tree,n=>n.type.name==='MusicMain')[0];
 const pending=main.props.perform('import-audio',{title:'原音频',sha256:'a'.repeat(64),size:4},musicState.songBasis(row),new Uint8Array([1,2,3,4]));const outcome=pending.catch(e=>e);render();assert.equal(nodes(h.tree,n=>n.type.name==='MusicMain')[0].props.busy,true);
 api.query='music_view=songs';render();await tick();render();gate.resolve(row);assert.match((await outcome).message,/歌曲已切换/);render();const directory=nodes(h.tree,n=>n.type.name==='MusicSongDirectory')[0];assert.equal(directory.props.busy,false);assert.equal(api.pushed,undefined);h.unmount();
});


function audioRangeScene(duration, explicit = {}) {
 const row=songRow(),asset=version('range-asset','AudioAssetVersion',{sha256:'a'.repeat(64),duration}),candidate=version('range-candidate','Candidate',{title:'范围候选',lyrics_ref:row.lyrics.entity_id,production_ref:row.production.entity_id,asset_ref:asset.entity_id});
 row.versions.push(asset,candidate);row.candidates=[candidate];row.assets=[asset];const storage=new Map(),h=scene('main',{storage}),props={...propsFor(row),entry:{mode:'candidates',...explicit}};
 const render=()=>h.render(h.exports.default,props);render();render();
 const input=label=>nodes(nodes(h.tree,n=>n.type==='label'&&text(n).startsWith(label))[0],n=>n.type==='input')[0];
 const decoded=()=>{nodes(h.tree,n=>n.type.name==='AudioPlayer')[0].props.onState({ready:true,position:0,duration,paused:true});render();};
 const selection=()=>JSON.parse(storage.get(musicState.draftKey('A','w',row.song.entity_id))).selection;
 return {h,row,asset,candidate,props,render,input,decoded,selection};
}
test('untouched audio range quotes actual short and long asset duration with exact original identities',()=>{
 for(const duration of [8,32]){
  const s=audioRangeScene(duration);assert.equal(s.input('终点（秒）').props.value,duration);s.decoded();assert.equal(button(s.h.tree,'选择此候选').props.disabled,true);
  button(s.h.tree,'引用时间范围').props.onClick();s.render();const quote=s.selection();assert.equal(quote.start,0);assert.equal(quote.end,duration);assert.equal(quote.duration,duration);assert.equal(quote.candidate_ref,s.candidate.entity_id);assert.equal(quote.asset_ref,s.asset.entity_id);assert.equal(quote.sha256,s.asset.data.sha256);assert.equal(s.row.choice,null);assert.equal(s.row.master,null);s.h.unmount();
 }
});
test('edited audio range survives data rerender and empty input remains explicit until corrected',()=>{
 const s=audioRangeScene(8);s.input('终点（秒）').props.onChange({target:{value:'3.5'}});s.render();s.props.row={...s.row,assets:[{...s.asset,data:{...s.asset.data}}]};s.render();assert.equal(s.input('终点（秒）').props.value,'3.5');s.decoded();button(s.h.tree,'引用时间范围').props.onClick();s.render();const original=s.selection();assert.equal(original.end,3.5);
 s.input('终点（秒）').props.onChange({target:{value:''}});s.render();assert.equal(s.input('终点（秒）').props.value,'');button(s.h.tree,'引用时间范围').props.onClick();s.render();assert.match(text(s.h.tree),/请填写引用范围/);assert.deepEqual(s.selection(),original);assert.equal(s.input('终点（秒）').props.value,'');s.h.unmount();
});
test('explicit out-of-bounds old audio range stays visible and rejected without clamping or retargeting',()=>{
 const s=audioRangeScene(8,{candidate:'range-candidate',asset:'range-asset',hash:'a'.repeat(64),start:1,end:16});s.decoded();assert.equal(s.input('起点（秒）').props.value,1);assert.equal(s.input('终点（秒）').props.value,16);button(s.h.tree,'引用时间范围').props.onClick();s.render();assert.match(text(s.h.tree),/音频范围必须位于准确候选的实际长度内/);assert.equal(s.selection(),null);assert.equal(s.input('终点（秒）').props.value,16);
 s.input('终点（秒）').props.onChange({target:{value:'6'}});s.render();button(s.h.tree,'引用时间范围').props.onClick();s.render();assert.equal(s.selection().start,1);assert.equal(s.selection().end,6);assert.equal(s.selection().candidate_ref,'range-candidate');assert.equal(s.selection().asset_ref,'range-asset');assert.equal(s.selection().sha256,'a'.repeat(64));s.h.unmount();
});

test('actual compiled A/B comparison excludes resolved A and never promotes B when original A is missing',()=>{const row=songRow(),b=version('candidate-B','Candidate',{title:'本地候选B',lyrics_ref:row.lyrics.entity_id,production_ref:row.production.entity_id});row.candidates.push(b);row.versions.push(b);let h=scene('main',{}),props={...propsFor(row),entry:{mode:'candidates'}};h.render(h.exports.default,props);h.render(h.exports.default,props);let select=nodes(h.tree,n=>n.props?.['aria-label']==='音乐比较候选B')[0];assert.deepEqual(nodes(select,n=>n.type==='option').map(n=>n.props.value),['','candidate-old']);select.props.onChange({target:{value:'candidate-old'}});h.render(h.exports.default,props);let comparison=nodes(h.tree,n=>n.props?.className==='compareColumns')[0];assert.match(text(comparison),/A · 本地候选B/);assert.match(text(comparison),/B · 本地候选A/);assert.match(text(comparison),/候选固定原歌词/);h.unmount();h=scene('main',{});props={...propsFor(row),entry:{mode:'candidates',candidate:'missing-original',compare:'candidate-B'}};h.render(h.exports.default,props);h.render(h.exports.default,props);comparison=nodes(h.tree,n=>n.props?.className==='compareColumns')[0];assert.match(text(comparison),/A · 原候选不存在/);assert.match(text(comparison),/B · 本地候选B/);assert.ok(!text(comparison).includes('A · 本地候选B'));h.unmount();});


test("Music save success is neutral and honest about absent or existing Master; failures retain exact alerts", async () => {
 for (const master of [null, version("master-original", "Master", { lyrics_ref: "lyrics-old" })]) {
  const row = { ...songRow(), master }, h = scene("main", {}), props = propsFor(row), calls = [];
  let reject = false;
  props.perform = async (action, data, expected) => { calls.push({ action, data, expected }); if (reject) throw new Error("原版本冲突；输入保留。"); return { ...row, song: { ...row.song, data: { ...row.song.data, lyrics_ref: "lyrics-saved", production_ref: "prod-saved" } } }; };
  const render = () => h.render(h.exports.default, props); render(); render();
  nodes(h.tree, n => n.type === "textarea" && n.props["aria-label"] === "当前歌词")[0].props.onChange({ target: { value: "新的歌词原稿" } }); render();
  await button(h.tree, "保存歌词版本").props.onClick(); render();
  const success = nodes(h.tree, n => n.type === "p" && n.props.role === "status" && text(n).startsWith("已保存新的版本"))[0];
  assert.equal(success.props.className, "notice"); assert.equal(text(success), master ? "已保存新的版本；原版本与已确认成品保留。" : "已保存新的版本；原版本保留，尚未确认成品。");
  assert.equal(calls[0].action, "save-lyrics"); assert.equal(calls[0].data.text, "新的歌词原稿"); assert.equal(calls[0].expected.lyrics_ref, "lyrics-new");
  reject = true; const production = nodes(h.tree, n => n.type === "textarea" && n.props.value === "当前制作")[0]; production.props.onChange({ target: { value: "新的制作依据" } }); render();
  await button(h.tree, "保存制作依据").props.onClick(); render();
  const error = nodes(h.tree, n => n.type === "p" && n.props.role === "alert")[0]; assert.equal(error.props.className, "error"); assert.equal(text(error), "原版本冲突；输入保留。");
  assert.ok(nodes(h.tree, n => n.type === "textarea" && n.props.value === "新的制作依据").length); assert.equal(calls[1].expected.production_ref, "prod-new"); h.unmount();
 }
});

test("Music Chinese WAV chooser retains native focus target and every existing disabled guard", () => {
 const row = songRow(), h = scene("main", {}), props = propsFor(row); props.collection = { ...props.collection, user_media_configured: true };
 const render = () => h.render(h.exports.default, props), input = () => nodes(h.tree, n => n.type === "input" && n.props.type === "file")[0]; render(); render();
 assert.match(text(h.tree), /尚未选择文件/); assert.equal(input().props["aria-label"], "导入本机 WAV"); assert.equal(input().props.accept, ".wav,audio/wav"); assert.equal(input().props.className, "fileInput"); assert.equal(input().props.hidden, undefined); assert.notEqual(input().props.tabIndex, -1); assert.equal(typeof input().props.onChange, "function"); assert.equal(input().props.onKeyDown, undefined); assert.equal(input().props.disabled, false);
 const label = nodes(h.tree, n => n.type === "label" && n.props.className === "filePicker")[0]; assert.match(text(label), /导入本机 WAV/);
 props.busy = true; render(); assert.equal(input().props.disabled, true); props.busy = false; props.locked = true; render(); assert.equal(input().props.disabled, true); props.locked = false;
 nodes(h.tree, n => n.type === "textarea" && n.props["aria-label"] === "当前歌词")[0].props.onChange({ target: { value: "未保存歌词" } }); render(); assert.equal(input().props.disabled, true); h.unmount();
 const unconfigured = scene("main", {}); unconfigured.render(unconfigured.exports.default, propsFor(row)); unconfigured.render(unconfigured.exports.default, propsFor(row)); assert.equal(nodes(unconfigured.tree, n => n.type === "input" && n.props.type === "file").length, 0); unconfigured.unmount();
});

test("Music saved request success is neutral status and local send/query failures remain exact alerts", async () => {
 for (const fail of [false, true]) {
  const row=songRow(),assignment={...scope,assignment_ref:"assignment-original",company_employee_ref:"employee-original",scope_type:"WORKSPACE",scope_ref:"w",enabled:true,name:"原责任员工",models:[{model_key:"local-fixture-model"}]};
  const draft={title:row.song.data.title,intention:row.song.data.intention,lyrics:row.lyrics.data.text,production:row.production.data.brief};
  const selection=musicState.lyricsSelection(row.lyrics,draft.lyrics,0,2),storage=new Map([[musicState.draftKey("A","w",row.song.entity_id),JSON.stringify({draft,saved:musicState.songBasis(row),selection,discussion:true,message:"核对原选段",assignment:assignment.assignment_ref,model:"local-fixture-model"})]]),calls=[];
  const api={storage,query:async()=>{throw new Error("原请求查询暂不可用");}},h=scene("main",api),props=propsFor(row);props.collection={...props.collection,entry:{...entry,assignments:[assignment]}};
  props.perform=async(action,data,expected)=>{calls.push({action,data,expected});if(action==="bind")return {binding_ref:"binding-original",context:{assignment_ref:assignment.assignment_ref}};if(action==="create-work")return {work:{entity_id:"formal-work"}};assert.equal(action,"send");if(fail)throw new Error("原请求保存失败，输入保留");return {attempt:{attempt_id:"attempt-original",status:"QUEUED"}};};
  const render=()=>h.render(h.exports.default,props);render();render();let send=nodes(h.tree,n=>n.props?.inputAriaLabel==="给员工的留言")[0];nodes(send.props.controls,n=>n.props?.["aria-label"]==="音乐交办范围")[0].props.onChange({target:{value:"selection"}});render();send=nodes(h.tree,n=>n.props?.submitLabel==="仅交办所选范围")[0];assert.equal(send.props.disabled,false);await send.props.onSubmit({preventDefault(){}});render();
  assert.deepEqual(calls.map(c=>c.action),["bind","create-work","send"]);assert.equal(calls[2].data.binding_ref,"binding-original");assert.equal(calls[2].data.model_key,"local-fixture-model");assert.deepEqual(JSON.parse(JSON.stringify(calls[2].data.selection)),selection);assert.equal(calls[2].expected.lyrics_ref,row.lyrics.entity_id);
  const notice=nodes(h.tree,n=>n.type==="p"&&text(n)===(fail?"原请求保存失败，输入保留":"原请求已保存，请查询实际结果。"))[0];assert.ok(notice);assert.equal(notice.props.className,fail?"error":"notice");assert.equal(notice.props.role,fail?"alert":"status");
  assert.ok(nodes(h.tree,n=>n.props?.inputAriaLabel==="给员工的留言"&&n.props.value==="核对原选段").length);
  if(!fail){await button(h.tree,"查询原请求").props.onClick();render();const alert=nodes(h.tree,n=>n.type==="p"&&n.props.role==="alert"&&text(n)==="原请求查询暂不可用")[0];assert.equal(alert.props.className,"error");}
  h.unmount();
 }
});

function releaseLabelRow(times) {
 const row=songRow();
 for(const [i,id] of ['music-pack-shared-prefix-A-shared-suffix','music-pack-shared-prefix-B-shared-suffix'].entries()){
  const master=version('music-master-'+i,'MasterRevision',{lyrics_ref:i?'lyrics-new':'lyrics-old',production_ref:i?'prod-new':'prod-old'});
  const pack=version(id,'ReleasePackage',{title:'同名本地准备',master_ref:master.entity_id,credits:'原署名-'+id});
  if(times[i]!==undefined)pack.created_at=times[i];
  row.versions.push(master,pack);row.releases.push(pack);row.master=master;
 }
 return row;
}
const releaseLinks=tree=>nodes(tree,n=>typeof n.props?.href==='string'&&n.props.href.includes('music_release='));
const accessibleLinkText=node=>node.props['aria-label']||text(node);
for(const times of [
 ['2026-10-21T10:00:00Z','2026-10-21T11:00:00Z'],
 ['2026-10-21T10:00:00Z','2026-10-21T10:00:00Z'],
 [undefined,undefined],
 ['not-a-time','not-a-time'],
]) for(const location of ['main','workspace']) test('compiled release record labels are distinct and exact: '+location+' '+JSON.stringify(times),()=>{
 const row=releaseLabelRow(times),original=JSON.stringify(row),h=scene(location,{});
 const paint=()=>location==='main'?h.render(h.exports.default,{...propsFor(row),entry:{mode:'release'}}):h.render(h.exports.MusicReleaseMain,{workspaceId:'w',songs:[row],entry:{song:row.song.entity_id,release:row.releases[1].entity_id}});
 paint();paint();let links=releaseLinks(h.tree);assert.equal(links.length,2);
 assert.equal(new Set(links.map(text)).size,2,'visible choice labels must distinguish same-title records');
 assert.equal(new Set(links.map(accessibleLinkText)).size,2,'accessible choice labels must distinguish same-title records');
 const labels=new Map();
 for(const pack of row.releases){
  const expected=musicState.operatingHref('w',{view:'release',song:row.song.entity_id,release:pack.entity_id});
  const link=links.find(n=>n.props.href===expected);assert.ok(link,'full song/release href preserved');
  assert.ok(text(link).includes(pack.entity_id),'full identifier disambiguates even colliding prefixes/suffixes');
  assert.ok(accessibleLinkText(link).includes(pack.entity_id));labels.set(pack.entity_id,text(link));
  const time=Date.parse(pack.created_at);
  assert.ok(text(link).includes(Number.isFinite(time)?new Date(time).toISOString():'时间未提供或不可核对'));
 }
 if(location==='workspace'){
  for(const pack of row.releases){
   h.render(h.exports.MusicReleaseMain,{workspaceId:'w',songs:[row],entry:{song:row.song.entity_id,release:pack.entity_id}});
   const selected=releaseLinks(h.tree).filter(n=>n.props['aria-current']==='page');assert.equal(selected.length,1);
   assert.ok(selected[0].props.href.includes('music_release='+pack.entity_id));
   const panel=nodes(h.tree,n=>n.type==='section'&&n.props.className==='panel')[0];
   assert.ok(text(panel).includes(pack.entity_id));assert.ok(text(panel).includes(pack.data.master_ref));assert.ok(text(panel).includes(pack.data.credits));
   assert.ok(!text(panel).includes(row.releases.find(p=>p!==pack).data.credits));
  }
 }
 assert.equal(JSON.stringify(row),original,'labels never mutate immutable version metadata');
 row.releases.reverse();paint();
 for(const link of releaseLinks(h.tree)){const ref=musicState.musicReturnTarget(link.props.href).entry.release;assert.equal(text(link),labels.get(ref),'reordering cannot rename a record');}
 h.unmount();
});

test('compiled release labels cannot surface foreign rows through the actual scoped workspace',async()=>{
 for(const field of ['tenant_id','company_id','workspace_id','parent_id']){
  const row=releaseLabelRow([undefined,undefined]);row.releases[0][field]='foreign';
  const api={...apiFor(row),query:'music_view=release'},h=scene('workspace',api);
  const paint=()=>h.render(h.exports.default,{detail,workspaceId:'w'});
  paint();await tick();paint();await tick();paint();
  assert.match(text(h.tree),/原音乐对象不属于当前范围/);
  assert.equal(releaseLinks(h.tree).length,0);assert.ok(!text(h.tree).includes('同名本地准备'));
  assert.equal(nodes(h.tree,n=>n.type===h.exports.MusicReleaseMain).length,0);
  h.unmount();
 }
});

test('compiled release records with unprovable identifiers have no selectable link',()=>{
 for(const location of ['main','workspace']) for(const id of [undefined,'','   ']){
  const row=releaseLabelRow([undefined,undefined]);row.releases=[{...row.releases[0],entity_id:id}];
  const h=scene(location,{});
  if(location==='main') {const props={...propsFor(row),entry:{mode:'release'}};h.render(h.exports.default,props);h.render(h.exports.default,props);}
  else h.render(h.exports.MusicReleaseMain,{workspaceId:'w',songs:[row],entry:{song:row.song.entity_id}});
  assert.equal(releaseLinks(h.tree).length,0);assert.match(visibleText(h.tree),/原准备记录标识不可核对/);h.unmount();
 }
});

test('compiled release labels never invent dates or a timezone for malformed metadata',()=>{
 for(const stamp of ['1','2026-02-30T10:00:00Z','2026-10-21T10:00:00',42]) for(const location of ['main','workspace']){
  const row=releaseLabelRow([stamp,stamp]),h=scene(location,{});
  if(location==='main'){const props={...propsFor(row),entry:{mode:'release'}};h.render(h.exports.default,props);h.render(h.exports.default,props);}
  else h.render(h.exports.MusicReleaseMain,{workspaceId:'w',songs:[row],entry:{song:row.song.entity_id}});
  assert.equal(releaseLinks(h.tree).length,2);
  for(const link of releaseLinks(h.tree)){assert.match(text(link),/时间未提供或不可核对/);assert.doesNotMatch(text(link),/保存于/);}
  h.unmount();
 }
});

test('formal Music Work creation persists original identity across cold remount without auto send', async () => {
 const row=songRow(),storage=new Map(),calls=[],api={...apiFor(row),storage,query:'music_song=music-song-A',createAssignedWork:async(assignment,value)=>{calls.push(structuredClone(value));if(calls.length===1)throw Error('creation unknown');return {work:{entity_id:'same-work'}};}};
 const payload={assignment_ref:'author',payload:{problem:'明确修改',expected_result:'文字结果',model_key:'model',source:{kind:'music',song_ref:row.song.entity_id}}};
 const mount=async()=>{const h=scene('workspace',api),render=()=>h.render(h.exports.default,{detail,workspaceId:'w'});render();await tick();render();await tick();render();return {h,main:nodes(h.tree,n=>n.type.name==='MusicMain')[0]};};
 let current=await mount();assert.ok(current.main);assert.equal(calls.length,0);
 await assert.rejects(current.main.props.perform('create-work',payload),/creation unknown/);current.h.unmount();
 current=await mount();assert.equal(calls.length,1,'cold read does not replay');const result=await current.main.props.perform('create-work',payload);
 assert.equal(result.work.entity_id,'same-work');assert.deepEqual(calls[0],calls[1]);current.h.unmount();
});

test('accepted text Work remains distinct from audio Choice and Master after readback', () => {
 const row=songRow(),candidate=row.candidates[0];candidate.data={...candidate.data,lyrics_ref:row.lyrics.entity_id,production_ref:row.production.entity_id,asset_ref:'',provenance:{execution_selection:{work_ref:'formal-text-work'}}};
 row.text_work_results={[candidate.entity_id]:{work_ref:'formal-text-work',status:'COMPLETED',acceptance_refs:['accepted']}};
 const h=scene('main',{}),props={...propsFor(row),entry:{candidate:candidate.entity_id,mode:'candidates'}};h.render(h.exports.default,props);h.render(h.exports.default,props);
 assert.equal(button(h.tree,'本次文字工作结果已接受').props.disabled,true);assert.match(text(h.tree),/不代表已试听音频、确认成品或发行/);assert.equal(row.choice,null);assert.equal(row.master,null);h.unmount();
});

function wholeSongScene({dirty=false,scopeMode='whole',empty=false}={}){
 const row=songRow();row.lyrics.data.text=empty?'  ':'第一句🌙\n第二句';
 const assignment={...scope,assignment_ref:'author',employee_ref:'runtime-author',company_employee_ref:'employee',scope_type:'WORKSPACE',scope_ref:'w',enabled:true,name:'作者',models:[{model_key:'flash'}]};
 const draft={title:row.song.data.title,intention:row.song.data.intention,lyrics:dirty?'未保存歌词':row.lyrics.data.text,production:row.production.data.brief};
 const storage=new Map([[musicState.draftKey('A','w',row.song.entity_id),JSON.stringify({draft,saved:musicState.songBasis(row),discussion:true,message:'按当前版本提出修改',assignment:'author',model:'flash'})]]),calls=[],h=scene('main',{storage}),props={...propsFor(row),collection:{...collection(row),entry:{...entry,assignments:[assignment]}}};
 props.perform=async(action,data,expected)=>{calls.push({action,data:structuredClone(data),expected});return action==='bind'?{binding_ref:'bound',context:{assignment_ref:'author'},discussion_scope:{object_ref:row.song.entity_id}}:action==='create-work'?{work:{entity_id:'work-whole'}}:{attempt:{attempt_id:'attempt',status:'COMPLETED'}};};
 const render=()=>h.render(h.exports.default,props),composer=()=>nodes(h.tree,n=>n.props?.inputAriaLabel==='给员工的留言')[0];render();render();
 nodes(composer().props.controls,n=>n.props?.['aria-label']==='音乐交办范围')[0].props.onChange({target:{value:scopeMode}});render();
 return {h,row,props,calls,render,composer,send:()=>composer().props.onSubmit({preventDefault(){}})};
}

test('Music whole saved lyrics creates and sends one pinned Work without selection or DOM focus',async()=>{
 const f=wholeSongScene();assert.equal(f.composer().props.submitLabel,'交办当前保存完整歌词');assert.equal(f.composer().props.disabled,false);assert.equal(f.calls.length,0);
 assert.equal(nodes(f.h.tree,n=>n.type==='summary'&&text(n).includes('针对原歌词')).length,0);
 await f.send();assert.deepEqual(f.calls.map(c=>c.action),['bind','create-work','send']);
 const source=f.calls[1].data.payload.source,request=f.calls[2].data;assert.deepEqual(source.selection,request.selection);assert.deepEqual(source.expected,JSON.parse(JSON.stringify(musicState.songBasis(f.row))));
 assert.deepEqual(request.selection,{kind:'lyrics',version_ref:f.row.lyrics.entity_id,draft_revision:f.row.lyrics.data.draft_revision,start:0,end:f.row.lyrics.data.text.length,excerpt:f.row.lyrics.data.text,locator:'lyrics'});assert.equal(f.row.choice,null);assert.equal(f.row.master,null);f.h.unmount();
});

for(const problem of ['dirty','empty','selection-without-range','locked'])test(`Music whole version preserves ${problem} gate`,async()=>{
 const f=wholeSongScene({dirty:problem==='dirty',empty:problem==='empty',scopeMode:problem==='selection-without-range'?'selection':'whole'});
 if(problem==='locked'){f.props.locked=true;f.render();}
 assert.equal(f.composer().props.disabled,true);await f.send();assert.equal(f.calls.length,0);f.h.unmount();
});
