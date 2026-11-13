import test from "node:test";
import assert from "node:assert/strict";
import { WRITING_PACKAGE, isWritingPackage, writingEntry, chapterHref, sameChapter, selectionFor, currentInspection, writingSessionKey, writingRequest, packageForEntry } from "../lib/writingState.mjs";
import { createWritingApi, writingRepairHref } from "../lib/writingApi.js";

const detail = { package: { package_id: WRITING_PACKAGE.id, version: WRITING_PACKAGE.version, digest: WRITING_PACKAGE.digest }, instance: { package_id: WRITING_PACKAGE.id, package_version: WRITING_PACKAGE.version, package_digest: WRITING_PACKAGE.digest }, schemas: { WritingBook: { schemaVersion: "writing.book/v1" }, WritingChapter: { schemaVersion: "writing.chapter/v1" } } };
test("Writing dispatch requires exact carrier; no guessed names or generic first object", () => {
  assert.equal(isWritingPackage(detail), true);
  assert.equal(isWritingPackage({ ...detail, package: { ...detail.package, digest: "other" } }), false);
  assert.equal(isWritingPackage({ ...detail, instance: { ...detail.instance, package_version: "0.2.0" } }), false);
});
test("entry roundtrip retains exact object, version and anchor; incomplete links fail", () => {
  const entry = { mode: "package", book: "b/1", chapter: "c/2", draft: "d", formal: "f", package: "p", anchor: "d:5:9" };
  assert.deepEqual(writingEntry(new URL(chapterHref("w", entry), "http://localhost").searchParams), { ...entry, view: "" });
  assert.ok(writingEntry(new URLSearchParams("writing_mode=chapter")).error);
  assert.ok(writingEntry(new URLSearchParams("writing_mode=unknown")).error);
});
test("UTF16 duplicate paragraph selection and dirty source rejection", () => {
  const draft = { ref: "d", text: "旧句😀\n旧句😀", sha256: "hash", knowledge: [] };
  assert.deepEqual(selectionFor(draft, draft.text, 0, 1).excerpt, "旧");
  assert.deepEqual(selectionFor(draft, draft.text, 5, 9), { draft_ref: "d", sha256: "hash", start: 5, end: 9, excerpt: "旧句😀", anchor: "d:5:9", knowledge: [] });
  assert.throws(() => selectionFor(draft, draft.text, 0, 0), { message: "请先选中一段正文。" });
  assert.throws(() => selectionFor(draft, "dirty", 0, 0), { message: "请保存当前正文后重新选择文字。" });
  assert.throws(() => selectionFor(draft, draft.text, -1, 1), { message: "选段范围无效，请重新选择正文。" });
  assert.throws(() => selectionFor(draft, draft.text, 3, 2), { message: "选段范围无效，请重新选择正文。" });
  assert.throws(() => selectionFor(draft, draft.text, 0, draft.text.length + 1), { message: "选段范围无效，请重新选择正文。" });
  assert.throws(() => selectionFor(draft, draft.text, 0.5, 1), { message: "选段范围无效，请重新选择正文。" });
  assert.throws(() => selectionFor(draft, draft.text, 2, 3), { message: "选择不能拆分字符。" });
});
test("inspection and session scope never reuse stale version or neighboring chapter", () => {
  const scope = { tenant_id: "t", company_id: "co", workspace_id: "w", instance_id: "i", book_ref: "b", chapter_ref: "c", package_id: WRITING_PACKAGE.id, package_version: WRITING_PACKAGE.version, package_digest: WRITING_PACKAGE.digest };
  assert.equal(sameChapter(scope, "co", "w", { book: "b", chapter: "other" }), false);
  assert.notEqual(writingSessionKey(scope), writingSessionKey({ ...scope, tenant_id: "other" }));
  assert.equal(currentInspection({ draft: { ref: "new", sha256: "h" }, events: [{ action: "inspection.recorded", draft_ref: "old", draft_sha256: "h" }] }), null);
});
test("commands and downloads preserve explicit scope and caller request identity", async () => {
  const calls = []; const api = createWritingApi(async (...args) => { calls.push(args); return {}; });
  const entry = { book: "b/1", chapter: "c/2" };
  const payload = { request_id: "same", expected_draft_ref: "d", data: { text: "原文", knowledge: [] } };
  await api.command("company", "w", entry, "draft.saved", payload); await api.download("company", "w", entry, "p");
  assert.ok(calls[0][0].includes("b%2F1/chapters/c%2F2/commands/draft.saved"));
  assert.deepEqual(JSON.parse(calls[0][1].body), payload);
  assert.equal(calls[1][1].responseType, "blob");
});
test("uncertain command retries retain request ID, while changed basis or payload gets a new ID", async () => {
  const original = await writingRequest(null, "draft.saved", "d", { text: "正文", knowledge: [] }, () => "first");
  assert.deepEqual(await writingRequest(original, "draft.saved", "d", { knowledge: [], text: "正文" }, () => "wrong"), original);
  assert.equal((await writingRequest(original, "draft.saved", "new", { text: "正文", knowledge: [] }, () => "next")).request_id, "next");
  assert.equal((await writingRequest(original, "draft.saved", "d", { text: "修改", knowledge: [] }, () => "changed")).request_id, "changed");
});
test("an old Package is unavailable alongside a different explicit Formal version", () => {
  const item = { action: "package.prepared", ref: "p", formal_ref: "old" };
  assert.equal(packageForEntry([item], { package: "p", formal: "new" }), null);
  assert.equal(packageForEntry([item], { package: "missing", formal: "old" }), null);
  assert.equal(packageForEntry([item], { package: "p", formal: "old" }), item);
});

async function writingComponent(path, props, api = {}) {
  const { readFileSync } = await import('node:fs'); const { createRequire } = await import('node:module'); const vm = await import('node:vm');
  const require = createRequire(import.meta.url), React = require('react'), swc = require('next/dist/build/swc'); await swc.loadBindings();
  const states = [], refs = [], effects = []; let si=0, ri=0, ei=0; const storage = api.__storage || new Map(), routes = [], writes = [];
  const hooks = { ...React, useState: initial => { const n=si++; if (!(n in states)) states[n]=initial; return [states[n], value => { states[n]=typeof value==='function' ? value(states[n]) : value; }]; }, useRef: initial => refs[ri++] ||= {current:initial}, useCallback: fn => fn, useMemo: fn => fn(), useEffect: (fn,deps) => { const n=ei++, old=effects[n]; if (!old || !deps || deps.some((v,i)=>!Object.is(v,old.deps[i]))) effects[n]={fn,deps,pending:true,cleanup:old?.cleanup}; } }; hooks.useLayoutEffect=hooks.useEffect;
  const originalApi = await import('../lib/writingApi.js'), originalState = await import('../lib/writingState.mjs'), originalBookState = await import('../lib/writingBookState.mjs'), scopeHelpers = await import('../components/writing/useWritingSurface.js');
  const source = readFileSync(new URL('../components/writing/'+path,import.meta.url),'utf8'); const {code}=await swc.transform(source,{filename:path,isModule:true,jsc:{parser:{syntax:'ecmascript',jsx:true},transform:{react:{runtime:'automatic'}}},module:{type:'commonjs'}});
  let query=''; const inert={__esModule:true,default:props=>React.createElement('div',props)}; const loaded={exports:{}};
  vm.runInNewContext(code,{module:loaded,exports:loaded.exports,URLSearchParams,crypto:globalThis.crypto,localStorage:{getItem:key=>storage.get(key)||null,setItem:(key,value)=>storage.set(key,value)},sessionStorage:{getItem:key=>storage.get(key)||null,setItem:(key,value)=>storage.set(key,value)},document:{querySelector:()=>null},require:name=>{
    if(name==='react')return hooks;if(name==='react/jsx-runtime')return require(name);
    if(name==='next/navigation')return {useRouter:()=>({push:href=>routes.push(href)}),useSearchParams:()=>new URLSearchParams(query)};
    if(name.endsWith('v1FrontendApi.js'))return api.__workApi || {};
    if(name.endsWith('writingBookState.mjs'))return originalBookState;
    if(name.endsWith('writingApi.js'))return {...originalApi,writingApi:api};if(name.endsWith('writingState.mjs'))return originalState;if(name.endsWith('useWritingSurface.js'))return {__esModule:true,...scopeHelpers};
    if(name.endsWith('api.js'))return {CEO_ID:'ceo'};if(name.endsWith('workspacePackageApi.js'))return {createInstalledWorkspaceObject:async(...args)=>{writes.push(args);if(api.createObject)return api.createObject(...args);return {object_id:args[2].object_type==='WritingBook'?'new-book':'new-chapter'};}};
    if(name.endsWith('SharedConversation.js'))return {ConversationComposer:'composer',useConversationModel:()=>api.__model || ({models:[],selected:null})};
    if(name.endsWith('EmployeeAvatar.js'))return {EmployeeAvatar:'avatar'};if(name.endsWith('.module.css'))return {__esModule:true,default:new Proxy({},{get:(_target,key)=>String(key)})};return inert;
  }});
  const render=()=>{si=0;ri=0;ei=0;return loaded.exports.default(props);}; const flush=async()=>{render();for(const e of effects)if(e.pending){e.cleanup?.();e.pending=false;e.cleanup=e.fn();}await new Promise(resolve=>setTimeout(resolve,0));return render();};
  const find=(n,pred)=>!n?null:Array.isArray(n)?n.map(v=>find(v,pred)).find(Boolean):pred(n)?n:find(n.props?.children,pred);
  return {render,flush,find:pred=>find(render(),pred),setQuery:value=>{query=value;},routes,writes,storage};
}

test('actual works Main selects a real book, creates into its scope, and requests lawful auxiliary tabs', async()=>{
  const collection={scope:{company_id:'co',workspace_id:'w'},books:[{ref:'book',title:'真实作品',status:'DRAFT'}],chapters:[{ref:'chapter',bookRef:'book',title:'真实第一章',status:'DRAFT'}],read_only:false,responsibility:{employee_name:'真实作者',reason:'执行未启用'}};
  const detail={package:{package_id:WRITING_PACKAGE.id,version:WRITING_PACKAGE.version,digest:WRITING_PACKAGE.digest},instance:{company_id:'co',package_id:WRITING_PACKAGE.id,package_version:WRITING_PACKAGE.version,package_digest:WRITING_PACKAGE.digest},schemas:{WritingBook:{schemaVersion:'writing.book/v1'},WritingChapter:{schemaVersion:'writing.chapter/v1'}}};
  const h=await writingComponent('WritingWorkspace.js',{detail,workspaceId:'w'},{collection:async()=>collection,entry:async()=>({scope:collection.scope,employee_name:'真实作者',company_employee_ref:'employee',pending:[],employees:[],execution:{status:'UNAVAILABLE'}})});
  await h.flush(); let tree=h.render(); assert.equal(tree.props.initialContextOpen,true);assert.equal(tree.props.initialUtilityOpen,false);
  assert.ok(h.find(n=>n.props?.href?.includes('writing_mode=books&book_ref=book')));assert.equal(JSON.stringify(tree).includes('雾色灯塔'),false);
  h.setQuery('writing_mode=books&book_ref=book'); await h.flush();await h.flush();
  assert.ok(JSON.stringify(h.render().props.contextPane).includes('writing_mode=chapter&book_ref=book&chapter_ref=chapter'));
  const bookMain=h.find(n=>typeof n.props?.onCreateChapter==='function');assert.ok(bookMain);bookMain.props.onInspect({company:'co',workspaceId:'w',ref:'node',title:'条目',content:'原内容'});
  await bookMain.props.onCreateChapter('新第二章');
  assert.equal(h.writes[0][2].data.bookRef,'book');await h.flush();assert.ok(h.routes[0].includes('chapter_ref=new-chapter'));
  h.setQuery('writing_mode=books&book_ref=foreign');await h.flush();await h.flush();assert.ok(JSON.stringify(h.render()).includes('当前作品不存在'));assert.equal(h.writes.length,1);
});

test('actual chapter keeps discussion hidden until requested and uses explicit save without fake availability',async()=>{
  const commands=[];const scope={tenant_id:'selfuse',company_id:'co',workspace_id:'w',instance_id:'i',book_ref:'book',chapter_ref:'chapter'};
  const state={scope,draft:{ref:'d',sha256:'sha',text:'真实原文',knowledge:[]},events:[],responsibility:{employee_name:'真实作者',status:'UNAVAILABLE',reason:'未配置可用模型'},read_only:false};
  const h=await writingComponent('WritingChapterMain.js',{state,entry:{mode:'chapter'},workspaceId:'w',company:'co',entryMetadata:{company_employee_ref:'employee',employee_name:'真实作者',models:[]},command:async(action,data)=>{commands.push({action,data});return {draft:{...state.draft,ref:'new',text:data.text}};},onNavigate(){},onRefresh(){},onExecutionLock(){},onDetails(){}});
  await h.flush();assert.equal(h.find(n=>n.props?.["aria-label"]==='章节讨论').props.hidden,true);
  h.find(n=>n.props?.children==='展开章节讨论').props.onClick();assert.equal(h.find(n=>n.type==='composer').props.disabled,true);assert.equal(JSON.stringify(h.find(n=>n.type==='composer').props.controls).includes('会话模型'),false);assert.ok(h.find(n=>n.type==='composer').props.className.includes('discussionComposer'));
  h.find(n=>n.type==='composer').props.onChange('保留讨论输入');h.find(n=>n.props?.children==='收起章节讨论').props.onClick();assert.equal(h.find(n=>n.props?.["aria-label"]==='章节讨论').props.hidden,true);
  h.find(n=>n.props?.['aria-label']==='章节正文').props.onChange({target:{value:'真实修改'}});await h.find(n=>n.props?.children==='保存草稿').props.onClick();
  assert.deepEqual(JSON.parse(JSON.stringify(commands)),[{action:'draft.saved',data:{text:'真实修改',knowledge:[]}}]);
  h.find(n=>n.props?.children==='展开章节讨论').props.onClick();assert.equal(h.find(n=>n.type==='composer').props.value,'保留讨论输入');assert.equal(commands.length,1);
});
test('actual chapter Employee Bar links only current scoped metadata and preserves exact return',async()=>{
  const scope={tenant_id:'selfuse',company_id:'co',workspace_id:'w',instance_id:'i',book_ref:'book',chapter_ref:'chapter',package_id:WRITING_PACKAGE.id,package_version:WRITING_PACKAGE.version,package_digest:WRITING_PACKAGE.digest};
  const state={scope,draft:{ref:'d',sha256:'sha',text:'原正文',knowledge:[]},events:[],responsibility:{employee_name:'旧显示名',status:'UNAVAILABLE',reason:'无模型'},read_only:false};
  const entry={mode:'chapter',book:'book',chapter:'chapter',draft:'d',anchor:'d:0:2'};
  const metadata={scope:{tenant_id:'selfuse',company_id:'co',workspace_id:'w'},company_employee_ref:'employee',employee_name:'真实作者',models:[]};
  const props={state,entry,workspaceId:'w',company:'co',entryMetadata:metadata,command:async()=>{},onNavigate(){},onRefresh(){},onExecutionLock(){},onDetails(){}};
  const h=await writingComponent('WritingChapterMain.js',props);
  const link=()=>h.find(n=>n?.props?.['aria-label']==='查看真实作者的员工详情' && typeof n.props.href==='string');
  assert.equal(link()?.props.href,writingRepairHref('/ceo-office/organization/employees/employee',chapterHref('w',entry)));
  assert.equal(h.find(n=>n?.props?.employee?.id==='employee')?.props.employee.name,'真实作者');
  props.entryMetadata={...metadata,company_employee_ref:'employee space'};
  assert.equal(link()?.props.href,writingRepairHref('/ceo-office/organization/employees/employee%20space',chapterHref('w',entry)));
  for(const changed of [
    {...metadata,company_employee_ref:''}, {...metadata,company_employee_ref:'.'}, {...metadata,company_employee_ref:'..'}, {...metadata,employee_name:''},
    {...metadata,scope:{...metadata.scope,tenant_id:'foreign'}},
    {...metadata,scope:{...metadata.scope,company_id:'foreign'}},
    {...metadata,scope:{...metadata.scope,workspace_id:'foreign'}},
    {...metadata,company_employee_ref:'\ud800'},
  ]){props.entryMetadata=changed;assert.ok(!link());}
  props.entryMetadata=metadata;props.entry={...entry,chapter:'other'};assert.ok(!link());
  props.entry=entry;assert.equal(link()?.props.href,writingRepairHref('/ceo-office/organization/employees/employee',chapterHref('w',entry)));
});

test('actual author-check mode retains check input and cannot confirm without a current server inspection',async()=>{
  const commands=[];const state={scope:{tenant_id:'selfuse',company_id:'co',workspace_id:'w',instance_id:'i',book_ref:'book',chapter_ref:'chapter'},draft:{ref:'d',sha256:'sha',text:'已保存正文',knowledge:[]},events:[],responsibility:{status:'UNAVAILABLE',reason:'未连接模型'},read_only:false};
  const props={state,entry:{mode:'review'},workspaceId:'w',company:'co',command:async(action,data)=>{commands.push({action,data});return {};},onNavigate(){},onRefresh(){},onExecutionLock(){}};
  const h=await writingComponent('WritingChapterMain.js',props);await h.flush();
  assert.equal(h.find(n=>n.props?.['aria-label']==='章节正文'),undefined);
  for(const title of ['情节与人物连贯性','语言、错字与格式','署名、引用与权利声明'])h.find(n=>n.type==='label'&&Array.isArray(n.props.children)&&n.props.children.includes(title)).props.children[0].props.onChange({target:{checked:true}});
  h.find(n=>n.props?.['aria-label']==='检查备注').props.onChange({target:{value:'作者检查输入'}});await h.flush();
  const reopened=await writingComponent('WritingChapterMain.js',props,{__storage:h.storage});await reopened.flush();
  assert.equal(reopened.find(n=>n.props?.['aria-label']==='检查备注').props.value,'作者检查输入');
  assert.equal(reopened.find(n=>n.props?.children==='记录当前版本作者检查').props.disabled,false);
  assert.equal(reopened.find(n=>n.props?.children==='明确确认当前版本为正式稿').props.disabled,true);
  await reopened.find(n=>n.props?.children==='记录当前版本作者检查').props.onClick();
  assert.equal(commands[0].action,'inspection.recorded');assert.equal(commands[0].data.mode,'AUTHOR_MANUAL');assert.equal(commands[0].data.note,'作者检查输入');
  assert.equal(reopened.find(n=>n.props?.children==='明确确认当前版本为正式稿').props.disabled,true,'local checks do not fabricate current server inspection');
});

test('author Formal confirmation requires both current server inspection and a separate explicit author choice',async()=>{
  const calls=[],routes=[];const state={scope:{tenant_id:'selfuse',company_id:'co',workspace_id:'w',instance_id:'i',book_ref:'book',chapter_ref:'chapter'},draft:{ref:'draft',sha256:'sha',text:'保存版本正文',knowledge:[]},events:[{action:'inspection.recorded',ref:'inspection',draft_ref:'draft',draft_sha256:'sha'}],responsibility:{status:'UNAVAILABLE',reason:'无模型'},read_only:false};
  const h=await writingComponent('WritingChapterMain.js',{state,entry:{mode:'review'},workspaceId:'w',company:'co',command:async(action,data)=>{calls.push({action,data});return {ref:'formal'};},onNavigate:value=>routes.push(value),onRefresh(){},onExecutionLock(){}});await h.flush();
  assert.equal(h.find(n=>n.props?.children==='明确确认当前版本为正式稿').props.disabled,true);
  h.find(n=>n.type==='label'&&Array.isArray(n.props.children)&&n.props.children.includes('我已检查当前保存版本，同意确认为正式稿（尚未发布）')).props.children[0].props.onChange({target:{checked:true}});
  await h.find(n=>n.props?.children==='明确确认当前版本为正式稿').props.onClick();assert.equal(calls[0].action,'formal.confirmed');assert.equal(calls[0].data.inspection_ref,'inspection');assert.equal(calls[0].data.confirmed,true);assert.equal(routes[0].mode,'package');assert.equal(routes[0].formal,'formal');
});

test('operating surface identity owns headline and breadcrumb while Book remains scope and Context has no conflicting workbench active',async()=>{
  const detail={package:{package_id:WRITING_PACKAGE.id,version:WRITING_PACKAGE.version,digest:WRITING_PACKAGE.digest},instance:{company_id:'co',package_id:WRITING_PACKAGE.id,package_version:WRITING_PACKAGE.version,package_digest:WRITING_PACKAGE.digest},schemas:{WritingBook:{schemaVersion:'writing.book/v1'},WritingChapter:{schemaVersion:'writing.chapter/v1'}}};
  const collection={scope:{company_id:'co',workspace_id:'w'},books:[{ref:'book',title:'实际作品',status:'DRAFT'}],chapters:[],read_only:false,responsibility:{reason:'无模型'}};
  const h=await writingComponent('WritingWorkspace.js',{detail,workspaceId:'w'},{collection:async()=>collection,entry:async()=>({scope:collection.scope,pending:[],employees:[],execution:{status:'UNAVAILABLE'}})});
  const find=(node,p)=>!node?null:Array.isArray(node)?node.map(x=>find(x,p)).find(Boolean):p(node)?node:find(node.props?.children,p);
  for(const [view,title] of [['overview','经营'],['market','市场与方向'],['directions','作品方向'],['performance','读者与收益'],['learning','写作经验']]){
    h.setQuery('writing_mode=books&book_ref=book&wr_view='+view);await h.flush();await h.flush();
    assert.equal(h.find(n=>n.type==='h1').props.children,title);
    assert.ok(JSON.stringify(h.render().props.breadcrumb).includes(title));
    assert.ok(h.find(n=>n.props?.className==='scopeChip'&&JSON.stringify(n.props.children).includes('实际作品')));
    const workbench=find(h.render().props.contextPane,n=>n.props?.children==='作品工作台');assert.equal(workbench.props['aria-current'],undefined);
  }
});

test('actual isolated creation-source DTO feeds chapter basis and reads the fixed original learning version', {skip:!process.env.CURIS_TEST_CREATION_SOURCE_OUTPUT}, async()=>{
  const {readFileSync}=await import('node:fs');const evidence=JSON.parse(readFileSync(process.env.CURIS_TEST_CREATION_SOURCE_OUTPUT,'utf8'));const chapter=evidence.chapter,scope=chapter.scope,calls=[];
  const detail={package:{package_id:scope.package_id,version:scope.package_version,digest:scope.package_digest},instance:{company_id:scope.company_id,package_id:scope.package_id,package_version:scope.package_version,package_digest:scope.package_digest},schemas:{WritingBook:{schemaVersion:'writing.book/v1'},WritingChapter:{schemaVersion:'writing.chapter/v1'}}};
  const collection={scope,books:[{ref:scope.book_ref,title:'来源作品',status:'DRAFT'}],chapters:[{ref:scope.chapter_ref,bookRef:scope.book_ref,title:'来源章节',status:'DRAFT'}],read_only:false,responsibility:{}};
  const h=await writingComponent('WritingWorkspace.js',{detail,workspaceId:scope.workspace_id},{collection:async()=>collection,entry:async()=>({scope,pending:[],employees:[]}),chapter:async()=>chapter,learning:async(c,w,ref)=>{calls.push(ref);return {record:evidence.source_record,current_ref:'later-version-not-selected'};}});h.setQuery(new URLSearchParams({writing_mode:'chapter',book_ref:scope.book_ref,chapter_ref:scope.chapter_ref}).toString());await h.flush();await h.flush();
  const tab=h.render().props.utilityTabs.find(tab=>tab.id==='basis');assert.ok(JSON.stringify(tab.content).includes('创建来源经验'));assert.ok(JSON.stringify(tab.content).includes('原版本'));
  const find=(n,p)=>!n?null:Array.isArray(n)?n.map(v=>find(v,p)).find(Boolean):p(n)?n:find(n.props?.children,p);await find(tab.content,n=>n.props?.children==='查看原经验版本').props.onClick();
  assert.deepEqual(calls,[chapter.creation_source.learning_ref]);assert.equal(h.render().props.utilityTabs.at(-1).title,'来源经验');assert.ok(JSON.stringify(h.render().props.utilityTabs.at(-1).content).includes(evidence.source_record.data.title));
});

test('author inspection compares current body and exact basis, including same-body rebind',()=>{const basis={context_ref:'A'},draft={ref:'same-body',sha256:'same-hash',book_context_basis:basis},check={ref:'check',action:'inspection.recorded',draft_ref:draft.ref,draft_sha256:draft.sha256,book_context_basis:basis};assert.equal(currentInspection({draft,events:[check],book_context_status:{status:'CURRENT'}}).ref,'check');assert.equal(currentInspection({draft:{...draft,book_context_basis:{context_ref:'B'}},events:[check]}),null);assert.equal(currentInspection({draft,events:[{...check,book_context_basis:undefined}]}),null);assert.equal(currentInspection({draft,events:[check],book_context_status:{status:'STALE'}}),null);});
test('unknown actual chapter creation remains locked across remount without a second POST',async()=>{const collection={scope:{company_id:'co',workspace_id:'w'},books:[{ref:'book',title:'原书',status:'DRAFT'}],chapters:[],read_only:false,responsibility:{status:'UNAVAILABLE'}};const detail={package:{package_id:WRITING_PACKAGE.id,version:WRITING_PACKAGE.version,digest:WRITING_PACKAGE.digest},instance:{company_id:'co',package_id:WRITING_PACKAGE.id,package_version:WRITING_PACKAGE.version,package_digest:WRITING_PACKAGE.digest},schemas:{WritingBook:{schemaVersion:'writing.book/v1'},WritingChapter:{schemaVersion:'writing.chapter/v1'}}};const api={collection:async()=>collection,entry:async()=>({scope:collection.scope,pending:[],employees:[]}),createObject:async()=>{throw new Error('response lost');}};let h=await writingComponent('WritingWorkspace.js',{detail,workspaceId:'w'},api);h.setQuery('writing_mode=books&book_ref=book');await h.flush();await h.flush();let main=h.find(n=>typeof n.props?.onCreateChapter==='function');await main.props.onCreateChapter('原创建标题');await h.flush();assert.equal(h.writes.length,1);main=h.find(n=>typeof n.props?.onCreateChapter==='function');await main.props.onCreateChapter('原创建标题');assert.equal(h.writes.length,1);const restored=await writingComponent('WritingWorkspace.js',{detail,workspaceId:'w'},{...api,__storage:h.storage});restored.setQuery('writing_mode=books&book_ref=book');await restored.flush();await restored.flush();await restored.find(n=>typeof n.props?.onCreateChapter==='function').props.onCreateChapter('原创建标题');assert.equal(restored.writes.length,0);assert.match(JSON.stringify(restored.render()),/原创建结果待核对/);});

test('actual Workspace employee return keeps fixed Book position, operating view and chapter publication anchors',async()=>{
  const scope={tenant_id:'selfuse',company_id:'co',workspace_id:'w',instance_id:'i',book_ref:'book',chapter_ref:'chapter',package_id:WRITING_PACKAGE.id,package_version:WRITING_PACKAGE.version,package_digest:WRITING_PACKAGE.digest};
  const detail={package:{package_id:WRITING_PACKAGE.id,version:WRITING_PACKAGE.version,digest:WRITING_PACKAGE.digest},instance:{company_id:'co',package_id:WRITING_PACKAGE.id,package_version:WRITING_PACKAGE.version,package_digest:WRITING_PACKAGE.digest},schemas:{WritingBook:{schemaVersion:'writing.book/v1'},WritingChapter:{schemaVersion:'writing.chapter/v1'}}};
  const collection={scope,books:[{ref:'book',title:'原书',status:'DRAFT'}],chapters:[{ref:'chapter',bookRef:'book',title:'原章节',status:'DRAFT'}],read_only:false,responsibility:{status:'UNAVAILABLE',reason:'受控未连接'}};
  const state={scope,draft:{ref:'draft-original',sha256:'a'.repeat(64),text:'原文',knowledge:[]},events:[],responsibility:{status:'UNAVAILABLE',reason:'受控未连接'},read_only:false};
  const api={collection:async()=>collection,entry:async()=>({scope,company_employee_ref:'employee-original',employee_name:'原员工',pending:[],employees:[],execution:{status:'UNAVAILABLE'}}),chapter:async()=>state};
  const find=(n,p)=>!n?null:Array.isArray(n)?n.map(v=>find(v,p)).find(Boolean):p(n)?n:find(n.props?.children,p);
  const queries=['','writing_mode=books&book_ref=book','writing_mode=books&book_ref=book&book_section=world&book_item=world-original&context_ref=original-fixed','writing_mode=books&book_ref=book&book_section=characters&book_item=person-original&context_ref=original-fixed','writing_mode=books&book_ref=book&book_section=outline&book_item=node-original&context_ref=original-fixed','writing_mode=books&book_ref=book&wr_view=market','writing_mode=books&wr_view=overview','writing_mode=chapter&book_ref=book&chapter_ref=chapter&draft_ref=draft-original&anchor=draft-original%3A0%3A1','writing_mode=package&book_ref=book&chapter_ref=chapter&draft_ref=draft-original&formal_ref=formal-original&package_ref=package-original&anchor=draft-original%3A0%3A1'];
  for(const query of queries){const h=await writingComponent('WritingWorkspace.js',{detail,workspaceId:'w'},api);h.setQuery(query);await h.flush();await h.flush();const tab=h.render().props.utilityTabs.find(t=>t.id==='responsibility'),link=find(tab.content,n=>typeof n.props?.href==='string'&&n.props.href.startsWith('/ceo-office/organization/employees/'));assert.ok(link,'actual employee detail link exists');const href=new URL(link.props.href,'http://local');assert.equal(href.pathname,'/ceo-office/organization/employees/employee-original');const target=href.searchParams.get('return_to'),back=new URL(target,'http://local');assert.equal(back.pathname,'/ceo-office/workspace/installed/w');const parsed=(await import('../lib/writingApi.js')).writingReturnTarget(target);for(const[key,value]of new URLSearchParams(query))assert.equal(key==='writing_mode'?parsed.entry.mode:back.searchParams.get(key),value,`preserve ${key} for ${query}`);assert.equal(parsed.workspace,'w');}
  const parse=(await import('../lib/writingApi.js')).writingReturnTarget;
  const base='/ceo-office/workspace/installed/w?writing_mode=books&book_ref=book&wr_view=market';
  for(const suffix of['&wr_view=overview','&book_ref=other','&book_section=world&book_section=characters','&draft_ref=author-draft','&formal_ref=author-formal','&package_ref=author-package','&anchor=author-range'])assert.throws(()=>parse(base+suffix));
  for(const bad of['/foreign?writing_mode=books','https://foreign.invalid/ceo-office/workspace/installed/w','/ceo-office/workspace/installed/w?writing_mode=books&book_ref=book&wr_view=constructor','/ceo-office/workspace/installed/w?writing_mode=chapter&book_ref=book&chapter_ref=chapter&wr_view=market'])assert.throws(()=>parse(bad));
  for(const query of['writing_mode=books&book_ref=foreign&book_section=world&context_ref=original-fixed','writing_mode=books&book_ref=book&book_section=constructor']){const h=await writingComponent('WritingWorkspace.js',{detail,workspaceId:'w'},api);h.setQuery(query);await h.flush();await h.flush();const tab=h.render().props.utilityTabs.find(t=>t.id==='responsibility');assert.ok(!find(tab.content,n=>typeof n.props?.href==='string'&&n.props.href.startsWith('/ceo-office/organization/employees/')),'invalid or foreign source cannot emit an employee return');}
});


const rootfScope={tenant_id:'selfuse',company_id:'co',workspace_id:'w',instance_id:'i',book_ref:'book',chapter_ref:'chapter',package_id:WRITING_PACKAGE.id,package_version:WRITING_PACKAGE.version,package_digest:WRITING_PACKAGE.digest};
function rootfState() {
  return {scope:rootfScope,draft:{ref:'saved-draft',sha256:'saved-hash',text:'保存正文',knowledge:[]},events:[],responsibility:{status:'UNAVAILABLE',reason:'无模型'},read_only:false,book_context:{record:{ref:'context10'},context:{items:[{id:'node',kind:'node',title:'节点',goal:'推进冲突'}]}}};
}
function rootfProps(state) {return {state,entry:{mode:'chapter',book:'book',chapter:'chapter'},workspaceId:'w',company:'co',command:async()=>({ref:'bound'}),onNavigate(){},onRefresh(){},onExecutionLock(){}};}
function rootfWorkspace(state,extra={}) {
  const detail={package:{package_id:WRITING_PACKAGE.id,version:WRITING_PACKAGE.version,digest:WRITING_PACKAGE.digest},instance:{company_id:'co',package_id:WRITING_PACKAGE.id,package_version:WRITING_PACKAGE.version,package_digest:WRITING_PACKAGE.digest},schemas:{WritingBook:{schemaVersion:'writing.book/v1'},WritingChapter:{schemaVersion:'writing.chapter/v1'}}};
  const collection={scope:rootfScope,books:[{ref:'book',title:'原作品',status:'DRAFT'}],chapters:[{ref:'chapter',bookRef:'book',title:'原章',status:'DRAFT'}],read_only:false,responsibility:{reason:'无模型'}};
  return writingComponent('WritingWorkspace.js',{detail,workspaceId:'w'},{collection:async()=>collection,chapter:async()=>state,entry:async()=>({scope:rootfScope,pending:[],employees:[]}),...extra});
}
const rootfNodes=(n,p)=>!n||typeof n!=='object'?[]:Array.isArray(n)?n.flatMap(v=>rootfNodes(v,p)):[...(p(n)?[n]:[]),...rootfNodes(n.props?.children,p)];
const rootfText=n=>n==null?'':Array.isArray(n)?n.map(rootfText).join(''):typeof n==='object'?rootfText(n.props?.children):String(n);

test('Writing dialogue reread releases only the server pending lock', async () => {
  const state = rootfState();
  let pending = [{ attempt_id: 'original', status: 'RUNNING' }];
  const metadata = () => ({ scope: rootfScope, pending, employees: [], models: [],
    employee_ref: 'employee', company_employee_ref: 'employee', employee_name: '作者' });
  const workspace = await rootfWorkspace(state, { entry: async () => metadata() });
  workspace.setQuery('writing_mode=chapter&book_ref=book&chapter_ref=chapter');
  await workspace.flush(); await workspace.flush();
  const main = () => workspace.find(n => typeof n.props?.onExecutionLock === 'function');
  assert.equal(main().props.requestLocked, true);

  const props = { ...rootfProps(state), ...main().props };
  const chapter = await writingComponent('WritingChapterMain.js', props);
  await chapter.flush();
  const conversation = () => chapter.find(n => n.props?.embedded?.objectRef === 'chapter');
  assert.equal(conversation().props.blocked, true);
  pending = [];
  await conversation().props.embedded.onReload();
  assert.equal(main().props.requestLocked, false);
  props.requestLocked = main().props.requestLocked;
  assert.equal(conversation().props.blocked, false);
  assert.equal(conversation().props.embedded.receiveReady, true);
  const editor = chapter.find(n => n.props?.['aria-label'] === '章节正文' && n.type === 'textarea');
  editor.props.onChange({ target: { value: '未保存正文' } });
  assert.equal(conversation().props.embedded.receiveReady, false);
  editor.props.onChange({ target: { value: state.draft.text } });
  props.state = { ...state, read_only: true };
  assert.equal(conversation().props.embedded.receiveReady, false);

  main().props.onExecutionLock(true);
  await main().props.onRefresh();
  assert.equal(main().props.requestLocked, true);
  assert.equal(workspace.storage.get('curis.writing.pending.co:w'), 'true');
});

test('actual Workspace refresh never issues a new Utility open during save or chapter creation',async()=>{
  let finish;const h=await rootfWorkspace(rootfState(),{createObject:()=>new Promise(resolve=>{finish=resolve;})});
  h.setQuery('writing_mode=books&book_ref=book');await h.flush();await h.flush();
  const main=()=>h.find(n=>typeof n.props?.onCreateChapter==='function');
  const d={company:'co',workspaceId:'w',ref:'relation',title:'关系',content:'旧内容'};
  main().props.onInspect(d,{open:true});const key=h.render().props.utilityRequestKey;
  // Closing a pane/tab consumes no new open request. Feed the same refreshes the real BookMain emits.
  main().props.onInspect({...d,content:'已保存的新内容'},{open:false});
  assert.equal(h.render().props.utilityRequestKey,key);
  assert.equal(h.render().props.utilityTabs.at(-1).content,'已保存的新内容');
  const pending=main().props.onCreateChapter('第二章');assert.ok(main().props.requestLocked);
  main().props.onInspect({...d,content:'创建中只读详情'},{open:false});assert.equal(h.render().props.utilityRequestKey,key);
  finish({object_id:'new-chapter'});await pending;await h.flush();
  assert.equal(h.render().props.utilityRequestKey,key);assert.equal(h.writes.length,1);
  main().props.onInspect({...d,company:'foreign'},{open:true});assert.equal(h.render().props.utilityRequestKey,key);
  main().props.onInspect(d,{open:true});assert.equal(h.render().props.utilityRequestKey,key+1);
});

test('actual basis gives each disabled reason, Chinese types and an unchanged explicit saved-draft binding',async()=>{
  const cases=[['unsaved',s=>s.draft.ref='ABSENT',/先保存本章正文草稿/],['readonly',s=>s.read_only=true,/只读/],['missing record',s=>s.book_context.record=null,/先保存作品计划/],['empty saved plan',s=>s.book_context.context.items=[],/没有可选条目/],['no selection',()=>{},/请选择要绑定/]];
  for(const [name,change,reason] of cases){const state=rootfState();change(state);const h=await writingComponent('WritingChapterMain.js',rootfProps(state));await h.flush();h.find(n=>n.props?.children==='明确选择 / 重绑本章依据').props.onClick();const button=h.find(n=>n.props?.children==='确认绑定原版本依据');assert.equal(button.props.disabled,true,name);assert.match(rootfText(h.find(n=>n.props?.id==='writing-basis-disabled')),reason,name);}
  for(const flag of ['busy','requestLocked']){const props={...rootfProps(rootfState()),[flag]:true};const h=await writingComponent('WritingChapterMain.js',props);await h.flush();h.find(n=>n.props?.children==='明确选择 / 重绑本章依据').props.onClick();assert.match(rootfText(h.find(n=>n.props?.id==='writing-basis-disabled')),flag==='busy'?/正在处理/:/原请求待核验/);assert.equal(h.find(n=>n.props?.children==='确认绑定原版本依据').props.disabled,true);}
  const state=rootfState(),commands=[],props={...rootfProps(state),command:async(action,data)=>{commands.push({action,data});return {ref:'binding'};}};
  const h=await writingComponent('WritingChapterMain.js',props);await h.flush();h.find(n=>n.props?.children==='明确选择 / 重绑本章依据').props.onClick();
  assert.match(rootfText(h.find(n=>n.type==='label'&&rootfText(n).includes('节点'))),/节点 · 故事节点/);
  h.find(n=>n.type==='input'&&n.props.type==='checkbox').props.onChange({target:{checked:true}});
  assert.equal(h.find(n=>n.props?.children==='确认绑定原版本依据').props.disabled,false);
  h.find(n=>n.props?.['aria-label']==='章节正文').props.onChange({target:{value:'未保存正文'}});
  assert.equal(h.find(n=>n.props?.children==='确认绑定原版本依据').props.disabled,true);assert.match(rootfText(h.find(n=>n.props?.id==='writing-basis-disabled')),/未保存修改/);
  h.find(n=>n.props?.['aria-label']==='章节正文').props.onChange({target:{value:state.draft.text}});
  await h.find(n=>n.props?.children==='确认绑定原版本依据').props.onClick();
  assert.deepEqual(JSON.parse(JSON.stringify(commands)),[{action:'context.bound',data:{context_ref:'context10',item_ids:['node'],confirmed:true}}]);
  assert.equal(state.draft.ref,'saved-draft');assert.equal(state.draft.text,'保存正文');assert.ok(!h.find(n=>n.props?.children==='确认绑定原版本依据'));
});

test('actual Workspace context binding remains anchored to saved draft and current immutable context',async()=>{
  const state=rootfState(),calls=[];const h=await rootfWorkspace(state,{command:async(...args)=>{calls.push(args);return {ref:'bound'};}});
  h.setQuery('writing_mode=chapter&book_ref=book&chapter_ref=chapter');await h.flush();await h.flush();
  const chapter=h.find(n=>typeof n.props?.command==='function'&&n.props?.state===state);
  await chapter.props.command('context.bound',{context_ref:'context10',item_ids:['node'],confirmed:true});
  assert.equal(calls.length,1);assert.equal(calls[0][3],'context.bound');assert.equal(calls[0][4].expected_draft_ref,'saved-draft');assert.equal(calls[0][4].data.context_ref,'context10');
});

test('actual goal/handoff pair keeps path/version/actions in its separate strip without denying a saved plan',async()=>{
  const state=rootfState();state.draft.book_context_basis={context_ref:'fixed',items:[{id:'v',kind:'volume',title:'原卷'},{id:'c',kind:'chapter',title:'原章',goal:'原目标',handoff:'上一章交接'.repeat(80)}]};state.book_context_status={status:'CURRENT',reason:'固定原版本依据'};
  const h=await writingComponent('WritingChapterMain.js',rootfProps(state));await h.flush();
  const cards=h.find(n=>n.props?.className==='chapterBasisSummary'),strip=h.find(n=>n.props?.className==='chapterBasisStrip');
  assert.equal(rootfNodes(cards,n=>n.type==='div').length,2);assert.match(rootfText(cards),/原目标/);assert.match(rootfText(cards),/上一章交接/);assert.ok(!rootfText(cards).includes('固定原版本依据'));assert.equal(rootfNodes(cards,n=>n.type==='button').length,0);
  assert.match(rootfText(strip),/原卷 \/ 原章/);assert.match(rootfText(strip),/固定原版本依据/);assert.equal(rootfNodes(strip,n=>n.type==='button').length,1);
  state.draft.book_context_basis=null;assert.match(rootfText(h.render()),/尚未绑定结构路径/);assert.ok(!rootfText(h.render()).includes('本章尚未归卷'));
});

test('agent candidate labels original range and replacement before explicit adoption',async()=>{
  const state=rootfState(),calls=[];
  state.events=[{action:'candidate.agent-recorded',ref:'candidate-1',draft_ref:state.draft.ref,source_class:'AGENT_EXECUTOR',selection:{excerpt:'原有选段'},replacement:'新正文'}];
  const props={...rootfProps(state),command:async(action,data)=>{calls.push({action,data});return null;}};
  const h=await writingComponent('WritingChapterMain.js',props);await h.flush();
  assert.ok(h.find(n=>n.type==='h3'&&n.props.children==='原选段'));
  assert.ok(h.find(n=>n.type==='h3'&&n.props.children==='将替换为'));
  assert.equal(calls.length,0);
});

test('actual basis groups only pinned fields and retains concurrent character data, directed endpoints and fixed links',async()=>{
  const state=rootfState();state.draft.book_context_basis={context_ref:'fixed10',items:[{id:'n',kind:'node',title:'原节点',goal:'原目的',body:'原节点正文'}, {id:'a',kind:'character',title:'原甲',role:'原角色',knowledge:'原知情',body:'原人物正文'}, {id:'b',kind:'character',title:'原乙',body:'乙档案'}, {id:'r',kind:'relationship',title:'原关系',from_character:'a',to_character:'b',body:'原关系状态'}, {id:'missing',kind:'relationship',title:'缺端点',from_character:'a',to_character:'latest-only'}, {id:'world',kind:'world',title:'原世界',category:'原类别',body:'原规则'}],directions:[{ref:'direction10',title:'原方向',revision:10,body:'原方向正文'}]};
  state.book_context.context.items=[{id:'a',kind:'character',title:'最新甲',role:'最新角色',knowledge:'最新知情'}, {id:'latest-only',kind:'character',title:'不应补用最新人物'}];
  const h=await rootfWorkspace(state);h.setQuery('writing_mode=chapter&book_ref=book&chapter_ref=chapter');await h.flush();await h.flush();
  const content=h.render().props.utilityTabs.find(t=>t.id==='basis').content;
  const groups=rootfNodes(content,n=>n.type==='section'&&n.props?.className==='basisGroup');
  assert.deepEqual(groups.map(n=>rootfText(n.props.children[0])),['结构与故事节点','人物','人物关系','世界设定']);
  const text=rootfText(content);for(const value of ['原目的','原角色','原知情','原人物正文','原甲 → 原乙','原关系状态','原类别','原规则','原方向正文','原快照缺少该端点人物'])assert.ok(text.includes(value),value);
  for(const value of ['最新甲','最新角色','最新知情','不应补用最新人物'])assert.ok(!text.includes(value),value);
  const links=rootfNodes(content,n=>typeof n.props?.href==='string'&&n.props.href.includes('book_item='));assert.equal(links.length,6);assert.ok(links.every(n=>n.props.href.includes('context_ref=fixed10')));
  assert.ok(rootfNodes(content,n=>n.type==='img').length===0);
});

test('same-body rebind clears author checks/consent and does not restore an obsolete inspection',async()=>{
  const state=rootfState(),basis={context_ref:'old',items:[],directions:[]};state.draft.book_context_basis=basis;state.events=[{action:'inspection.recorded',ref:'old-check',draft_ref:state.draft.ref,draft_sha256:state.draft.sha256,book_context_basis:basis}];
  const props=rootfProps(state);props.entry.mode='review';props.command=async()=>{state.draft.book_context_basis={context_ref:'context10',items:[],directions:[]};return {ref:'rebound'};};
  const h=await writingComponent('WritingChapterMain.js',props);await h.flush();
  h.find(n=>n.props?.className==='authorConsent').props.children[0].props.onChange({target:{checked:true}});
  assert.equal(h.find(n=>n.props?.children==='明确确认当前版本为正式稿').props.disabled,false);
  h.find(n=>n.props?.children==='明确选择 / 重绑本章依据').props.onClick();h.find(n=>n.type==='input'&&n.props.type==='checkbox').props.onChange({target:{checked:true}});
  await h.find(n=>n.props?.children==='确认绑定原版本依据').props.onClick();
  assert.equal(h.find(n=>n.props?.className==='authorConsent').props.children[0].props.checked,false);
  assert.equal(h.find(n=>n.props?.children==='明确确认当前版本为正式稿').props.disabled,true);
  assert.equal(state.draft.ref,'saved-draft');assert.equal(state.draft.text,'保存正文');
});


test('manual candidate keeps saved UTF16 selection and requires a separate adoption command',async()=>{
  const state=rootfState(),calls=[],routes=[];state.draft.text='甲😀乙';
  const props={...rootfProps(state),onNavigate:value=>routes.push(value),command:async(action,data)=>{calls.push({action,data});return {ref:'manual-candidate'};}};
  const h=await writingComponent('WritingChapterMain.js',props);await h.flush();
  h.find(n=>n.props?.['aria-label']==='章节正文').props.ref.current={selectionStart:1,selectionEnd:3};
  h.find(n=>n.props?.children==='引用选中文字').props.onClick();
  assert.equal(routes[0].anchor,'saved-draft:1:3');assert.equal(h.find(n=>n.props?.children==='准备人工修改').props.disabled,false);
  h.find(n=>n.props?.children==='准备人工修改').props.onClick();h.find(n=>n.props?.['aria-label']==='人工修改候选').props.onChange({target:{value:'明确替换'}});
  await h.find(n=>n.props?.children==='保存人工候选').props.onClick();
  assert.equal(calls.length,1);assert.equal(calls[0].action,'candidate.manual-recorded');assert.equal(calls[0].data.selection.excerpt,'😀');assert.equal(calls[0].data.selection.draft_ref,'saved-draft');assert.equal(calls[0].data.selection.start,1);assert.equal(calls[0].data.selection.end,3);assert.equal(calls[0].data.replacement,'明确替换');assert.equal(state.draft.text,'甲😀乙');
  state.events=[{...calls[0].data,ref:'manual-candidate',action:'candidate.manual-recorded',draft_ref:state.draft.ref,source_class:'CEO_MANUAL'}];
  assert.equal(h.find(n=>n.props?.children==='确认采用这处修改').props.disabled,false);
  h.find(n=>n.props?.['aria-label']==='章节正文').props.onChange({target:{value:'另有未保存正文'}});assert.equal(h.find(n=>n.props?.children==='确认采用这处修改').props.disabled,true);assert.equal(calls.length,1);
});


function densityItems() {
  const common=(id,kind,title)=>({id,kind,title,goal:title+'目的',body:title+'完整说明',status:title+'状态',order:0});
  return [{...common('o','outline','原大纲')},{...common('v','volume','原卷'),parent:'o'},
    {...common('c','chapter','原章'),parent:'v',chapter_ref:'chapter',handoff:'原章交接'},
    {...common('n','node','原节点'),parent:'c'},
    {...common('a','character','原甲'),role:'原甲角色',knowledge:'原甲知情'},
    {...common('b','character','原乙'),role:'原乙角色',knowledge:'原乙知情'},
    {...common('r','relationship','原关系'),from_character:'a',to_character:'b'},
    {...common('w','world','原世界'),category:'原世界类别'}];
}
async function densityContent(items) {
  const state=rootfState();state.draft.book_context_basis={context_ref:'fixed-context10',items,directions:[]};
  state.book_context.context.items=items.map(v=>({...v,title:'禁止使用最新'+v.title,goal:'禁止使用最新目的',body:'禁止使用最新正文'}));
  const h=await rootfWorkspace(state);h.setQuery('writing_mode=chapter&book_ref=book&chapter_ref=chapter');await h.flush();await h.flush();
  return h.render().props.utilityTabs.find(t=>t.id==='basis').content;
}

test('eight full pinned items compact three ancestors, expose only the real leaf purpose and preserve all eight original read-only records',async()=>{
  const items=densityItems(),content=await densityContent(items);
  const ancestors=rootfNodes(content,n=>n.props?.className==='basisAncestors');assert.equal(ancestors.length,1);
  assert.equal(rootfNodes(ancestors,n=>typeof n.props?.href==='string').length,3);
  const primary=rootfNodes(content,n=>n.props?.['data-basis-primary']===true);assert.equal(primary.length,1);assert.match(rootfText(primary),/原节点目的/);
  assert.equal(rootfNodes(content,n=>n.props?.className==='basisItem').length,5,'ancestors are compact links, not four full cards');
  assert.ok(!rootfText(ancestors).includes('原大纲完整说明'));assert.ok(!rootfText(ancestors).includes('原卷目的'));
  const visibleText=rootfText(content);for(const value of ['原甲角色','原甲知情','原甲完整说明','原乙角色','原乙知情','原乙完整说明','原甲 → 原乙','原关系完整说明','原世界类别','原世界完整说明'])assert.ok(visibleText.includes(value),value);
  assert.ok(!visibleText.includes('禁止使用最新'));
  const links=rootfNodes(content,n=>typeof n.props?.href==='string'&&n.props.href.includes('book_item='));assert.equal(links.length,8);
  assert.deepEqual(new Set(links.map(n=>new URL(n.props.href,'http://local').searchParams.get('book_item'))),new Set(items.map(v=>v.id)));
  for(const link of links){
    const params=new URL(link.props.href,'http://local').searchParams;assert.equal(params.get('context_ref'),'fixed-context10');const id=params.get('book_item'),item=items.find(v=>v.id===id),descriptors=[],reads=[];
    const context={setup:{reader:'',genre:'',premise:'',style:'',conflict:''},items};
    const h=await writingComponent('WritingBookMain.js',{company:'co',workspaceId:'w',book:{ref:'book',title:'原作品'},locator:{section:params.get('book_section'),item:id,context:params.get('context_ref')},onInspect:d=>descriptors.push(d),onCreateChapter(){}},{bookContext:async(co,w,b,ref)=>{reads.push(ref);return {scope:rootfScope,context,record:{ref:'fixed-context10',revision:10,context},chapters:[{ref:'chapter',title:'原章'}],read_only:true};},directions:async()=>({records:[]})});
    await h.flush();await h.flush();await h.flush();const original=descriptors.at(-1);assert.equal(original.ref,id);assert.equal(reads.at(-1),'fixed-context10');
    const text=rootfText(original.content);for(const field of ['goal','body','status','role','knowledge','category','handoff'])if(item[field])assert.ok(text.includes(item[field]),id+' '+field);
    assert.equal(rootfNodes(original.content,n=>n.type==='button'&&rootfText(n)==='编辑这条记录')[0].props.disabled,true);
  }
});

test('multi-branch pinned structure retains every leaf purpose instead of inventing a single current node',async()=>{
  const items=densityItems();items.push({id:'c2',kind:'chapter',title:'另一章',goal:'另一章目的',parent:'v',chapter_ref:'other-chapter',order:1},{id:'n2',kind:'node',title:'并列节点',goal:'并列节点目的',parent:'c',order:1});
  const content=await densityContent(items),primary=rootfNodes(content,n=>n.props?.['data-basis-primary']===true);
  assert.equal(primary.length,3);for(const value of ['原节点目的','另一章目的','并列节点目的'])assert.ok(rootfText(primary).includes(value),value);
  assert.ok(!rootfText(primary).includes('原章目的'));assert.ok(!rootfText(content).includes('当前节点'));
  assert.equal(rootfNodes(content,n=>typeof n.props?.href==='string'&&n.props.href.includes('book_item=')).length,10);
});

test('absent optional fields add no template rows while missing primary purpose and endpoint remain explicit',async()=>{
  const items=[{id:'c',kind:'chapter',title:'仅有章标题',goal:'',body:'',status:''}, {id:'a',kind:'character',title:'仅有角色',role:'叙事角色',knowledge:'',body:'',goal:'',status:''}, {id:'w',kind:'world',title:'规则',body:'唯一规则',category:'',goal:'',status:''}, {id:'r',kind:'relationship',title:'关系',from_character:'a',to_character:'absent',body:'真实关系说明',goal:'',status:''}];
  const content=await densityContent(items);assert.equal(rootfNodes(content,n=>n.props?.className==='basisSecondary').length,0);
  assert.equal(rootfNodes(content,n=>n.type==='dt').length,0);assert.ok(!rootfText(content).includes('原快照未提供人物说明'));assert.ok(!rootfText(content).includes('原快照未提供世界规则'));assert.match(rootfText(content),/原快照未提供叙事目的/);assert.match(rootfText(content),/原快照缺少该端点人物/);
  assert.equal(rootfNodes(content,n=>n.type==='p'&&rootfText(n).includes('叙事角色')).length,1);assert.equal(rootfNodes(content,n=>n.type==='p'&&rootfText(n).includes('唯一规则')).length,1);
});


async function explicitWritingScene(workApi, reviewed = false) {
  const state=rootfState();state.responsibility={status:'AVAILABLE',employee_name:'章节作者'};
  const selected={model_key:'fixture-model',model_name:'fixture-model',source:'official'};
  state.events=[{action:'discussion.bound',ref:'binding',draft_ref:state.draft.ref,discussion_scope:{object_ref:'chapter'},
    assignment_ref:'assignment',selection:selectionFor(state.draft,state.draft.text,0,2)}];
  if (reviewed) state.events.push(
    {action:'candidate.adopted',ref:'adoption',draft:{...state.draft},work_ref:'prior-work',acceptance_ref:'prior-acceptance'},
    {action:'inspection.recorded',ref:'review',draft_ref:state.draft.ref,draft_sha256:state.draft.sha256,
      book_context_basis:state.draft.book_context_basis,note:'作者复盘'});
  const sent=[];const attempt={attempt_id:'attempt',message_id:'message',status:'COMPLETED'};
  const api={__model:{models:[selected],selected},__workApi:workApi,
    send:async(...args)=>{sent.push(args[3]);return {attempt};},
    discussion:async()=>({messages:[],attempts:[attempt]})};
  const h=await writingComponent('WritingChapterMain.js',rootfProps(state),api);await h.flush();
  h.find(n=>n.props?.children==='展开章节讨论').props.onClick();await h.flush();
  h.find(n=>n.type==='composer').props.onChange('只修改原选文');
  return {h,sent};
}

test('ordinary Writing discussion has no Work; explicit delegation sends its original Work reference',async()=>{
  const created=[];
  const {h,sent}=await explicitWritingScene({getAssignedAgentWorkflow:async()=>({state:'READY'}),
    createAssignedWork:async(assignment,payload)=>{created.push({assignment,payload});return {work:{entity_id:'work-original'}};}});
  await h.find(n=>n.type==='composer').props.onSubmit({preventDefault(){}});
  assert.equal(created.length,0);assert.equal(sent.length,1);assert.equal(sent[0].work_ref,undefined);
  await h.find(n=>n.props?.children==='明确交办本次修改').props.onClick({preventDefault(){}});
  assert.equal(created.length,1);assert.equal(sent.length,2);assert.equal(sent[1].work_ref,'work-original');
  assert.equal(created[0].payload.request_id,sent[1].request_id);
  assert.equal(created[0].payload.source.chapter_ref,'chapter');
});

test('Writing responsibility publication requires explicit confirmation before creating Work',async()=>{
  let created=0,published=0;
  const {h,sent}=await explicitWritingScene({getAssignedAgentWorkflow:async()=>({state:'NEEDS_PUBLICATION',publication_allowed:true,
    assignment_revision:2,review_token:'a'.repeat(64),reason:'核对当前责任'}),
    createAssignedWork:async()=>{created++;},publishAssignedAgentWorkflow:async()=>{published++;}});
  await h.find(n=>n.props?.children==='明确交办本次修改').props.onClick({preventDefault(){}});
  assert.equal(created,0);assert.equal(sent.length,0);assert.equal(published,0);
  await h.find(n=>n.props?.children==='确认发布当前责任').props.onClick();
  assert.equal(published,1);assert.equal(created,0);assert.equal(sent.length,0);
  assert.equal(h.find(n=>n.type==='composer').props.value,'只修改原选文');
});

test('unknown Writing Work creation reads back the same identity and never automatically sends',async()=>{
  const identities=[];let count=0;
  const {h,sent}=await explicitWritingScene({getAssignedAgentWorkflow:async()=>({state:'READY'}),
    createAssignedWork:async(_assignment,payload)=>{identities.push(payload.request_id);if(++count===1)throw Error('lost response');return {work:{entity_id:'work-original'}};}});
  await h.find(n=>n.props?.children==='明确交办本次修改').props.onClick({preventDefault(){}});
  assert.equal(sent.length,0);
  await h.find(n=>n.props?.children==='查询原请求结果').props.onClick();
  assert.equal(sent.length,0);assert.equal(identities.length,2);assert.equal(identities[0],identities[1]);
  await h.find(n=>n.props?.children==='继续原交办').props.onClick({preventDefault(){}});
  assert.equal(sent.length,1);assert.equal(sent[0].work_ref,'work-original');assert.equal(sent[0].request_id,identities[0]);
});


test('Writing review creates a distinct prepared Work and sends only after a second explicit action',async()=>{
  const created=[];
  const {h,sent}=await explicitWritingScene({getAssignedAgentWorkflow:async()=>({state:'READY'}),
    createAssignedWork:async(assignment,payload)=>{created.push(payload);return{work:{entity_id:'review-new-work'}};}},true);
  const button=h.find(n=>n.props?.children==='基于当前复盘创建新工作（不发送）');
  assert.equal(button.props.disabled,false);
  await button.props.onClick({preventDefault(){}});await h.flush();
  assert.equal(created.length,1);assert.equal(created[0].source.review_ref,'review');
  assert.equal(sent.length,0,'Work creation cannot call the model');
  assert.equal(h.find(n=>n.type==='composer').props.disabled,true);
  assert.equal(h.find(n=>n.props?.children==='明确交办本次修改').props.disabled,true);
  assert.equal(h.find(n=>n.props?.children==='基于当前复盘创建新工作（不发送）').props.disabled,true);
  await h.find(n=>n.props?.children==='继续原交办').props.onClick({preventDefault(){}});await h.flush();
  assert.equal(sent.length,1);assert.equal(sent[0].work_ref,'review-new-work');
  assert.notEqual(sent[0].work_ref,'prior-work');assert.equal(created.length,1);
});

test('Writing review unknown creation queries the same identity and never auto-dispatches',async()=>{
  const created=[];
  const {h,sent}=await explicitWritingScene({getAssignedAgentWorkflow:async()=>({state:'READY'}),
    createAssignedWork:async(assignment,payload)=>{created.push(structuredClone(payload));
      if(created.length===1)throw Error('synthetic lost creation response');return{work:{entity_id:'review-retained'}};}},true);
  await h.find(n=>n.props?.children==='基于当前复盘创建新工作（不发送）').props.onClick({preventDefault(){}});await h.flush();
  assert.equal(sent.length,0);
  await h.find(n=>n.props?.children==='查询原请求结果').props.onClick();await h.flush();
  assert.deepEqual(created[0],created[1]);assert.equal(created[1].source.review_ref,'review');
  assert.equal(sent.length,0);
  await h.find(n=>n.props?.children==='继续原交办').props.onClick({preventDefault(){}});await h.flush();
  assert.equal(sent.length,1);assert.equal(sent[0].work_ref,'review-retained');
});
