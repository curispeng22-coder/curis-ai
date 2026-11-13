import test from "node:test";
import assert from "node:assert/strict";
import { writingEntry, writingViewHref } from "../lib/writingState.mjs";
import { writingReturnTarget } from "../lib/writingApi.js";

const params = (q) => new URLSearchParams(q);

test("wr_view whitelist: empty/directions/learning/market/performance/overview, unknown fails closed", () => {
  assert.equal(writingEntry(params("")).view, "");
  assert.equal(writingEntry(params("wr_view=directions")).view, "directions");
  assert.equal(writingEntry(params("wr_view=learning")).view, "learning");
  assert.equal(writingEntry(params("wr_view=market")).view, "market");
  assert.equal(writingEntry(params("wr_view=performance")).view, "performance");
  assert.equal(writingEntry(params("wr_view=overview")).view, "overview");
  for (const bad of ["wr_view=admin", "wr_view=op", "wr_view=DIRECTIONS", "wr_view=../x", "wr_view=snapshots", "wr_view=dashboard"]) {
    assert.ok(writingEntry(params(bad)).error, bad);
  }
});

test("operating views only enter from workspace books level", () => {
  const ok = writingEntry(params("writing_mode=books&wr_view=directions"));
  assert.equal(ok.error, undefined);
  assert.equal(ok.mode, "books");
  assert.equal(ok.view, "directions");
  const blocked = writingEntry(params("writing_mode=chapter&book_ref=b&chapter_ref=c&wr_view=learning"));
  assert.ok(blocked.error);
  const overviewBlocked = writingEntry(params("writing_mode=chapter&book_ref=b&chapter_ref=c&wr_view=overview"));
  assert.ok(overviewBlocked.error);
});

test("writingViewHref serialization rejects unknown views", () => {
  assert.equal(writingViewHref("w", ""), "/ceo-office/workspace/installed/w");
  assert.equal(writingViewHref("w", "directions"), "/ceo-office/workspace/installed/w?wr_view=directions");
  assert.equal(writingViewHref("w", "market"), "/ceo-office/workspace/installed/w?wr_view=market");
  assert.equal(writingViewHref("w", "performance"), "/ceo-office/workspace/installed/w?wr_view=performance");
  assert.equal(writingViewHref("w", "overview"), "/ceo-office/workspace/installed/w?wr_view=overview");
  assert.throws(() => writingViewHref("w", "observations"));
});

test("repair return accepts wr_view but still rejects invented params", () => {
  const target = writingReturnTarget("/ceo-office/workspace/installed/w?wr_view=learning");
  assert.equal(target.entry.view, "learning");
  assert.equal(writingReturnTarget("/ceo-office/workspace/installed/w?wr_view=performance").entry.view, "performance");
  assert.equal(writingReturnTarget("/ceo-office/workspace/installed/w?wr_view=overview").entry.view, "overview");
  assert.throws(() => writingReturnTarget("/ceo-office/workspace/installed/w?wr_view=learning&evil=1"));
});

async function surfaceHarness(file, initialProps, api = {}) {
  const { readFileSync } = await import('node:fs'), { createRequire } = await import('node:module'), vm = await import('node:vm');
  const require = createRequire(import.meta.url), React = require('react'), swc = require('next/dist/build/swc'); await swc.loadBindings();
  const writing = await import('../lib/writingState.mjs'), { TENANT_ID } = await import('../lib/api.js');
  const states=[],refs=[],effects=[],memos=[];let si=0,ri=0,ei=0,mi=0;let props=initialProps;
  const hooks={...React,useState:initial=>{const n=si++;if(!(n in states))states[n]=initial;return [states[n],value=>{states[n]=typeof value==='function'?value(states[n]):value;}];},useRef:initial=>refs[ri++]||={current:initial},useCallback:(fn,deps)=>{const n=mi++,old=memos[n];if(!old||deps.some((v,i)=>!Object.is(v,old.deps[i])))memos[n]={value:fn,deps};return memos[n].value;},useMemo:(fn,deps)=>{const n=mi++,old=memos[n];if(!old||deps.some((v,i)=>!Object.is(v,old.deps[i])))memos[n]={value:fn(),deps};return memos[n].value;},useEffect:(fn,deps)=>{const n=ei++,old=effects[n];if(!old||!deps||deps.some((v,i)=>!Object.is(v,old.deps[i])))effects[n]={fn,deps,pending:true,cleanup:old?.cleanup};}};hooks.useLayoutEffect=hooks.useEffect;
  const modules=new Map();async function load(name){const source=readFileSync(new URL('../components/writing/'+name,import.meta.url),'utf8');const {code}=await swc.transform(source,{filename:name,isModule:true,jsc:{parser:{syntax:'ecmascript',jsx:true},transform:{react:{runtime:'automatic'}}},module:{type:'commonjs'}});const m={exports:{}};vm.runInNewContext(code,{module:m,exports:m.exports,URLSearchParams,crypto:globalThis.crypto,require:name=>{if(name==='react')return hooks;if(name==='react/jsx-runtime')return require(name);if(name.endsWith('writingState.mjs'))return writing;if(name.endsWith('writingApi.js'))return {writingApi:api};if(name.endsWith('api.js'))return {TENANT_ID};if(name.endsWith('useWritingSurface.js'))return modules.get('useWritingSurface.js');if(name.endsWith('.module.css'))return {__esModule:true,default:new Proxy({},{get:(_t,k)=>String(k)})};return {__esModule:true,default:p=>React.createElement('div',p)};}});modules.set(name,m.exports);return m.exports;}
  const helper=await load('useWritingSurface.js');let Component;
  if(file==='hook')Component=p=>helper.default(p.company,p.workspaceId,p.object || "");else Component=(await load(file)).default;
  const render=()=>{si=0;ri=0;ei=0;mi=0;return Component(props);};
  const flush=async()=>{render();for(const effect of effects)if(effect.pending){effect.cleanup?.();effect.pending=false;effect.cleanup=effect.fn();}await new Promise(resolve=>setTimeout(resolve,0));return render();};
  const find=(n,p)=>!n?null:Array.isArray(n)?n.map(v=>find(v,p)).find(Boolean):p(n)?n:find(n.props?.children,p);
  return {render,flush,setProps:p=>{props=p;},find:p=>find(render(),p),helper};
}

const operatingScope = async (company='co') => {
  const { TENANT_ID }=await import('../lib/api.js'),{WRITING_PACKAGE}=await import('../lib/writingState.mjs');
  return {tenant_id:TENANT_ID,company_id:company,workspace_id:'w',instance_id:'i',package_id:WRITING_PACKAGE.id,package_version:WRITING_PACKAGE.version,package_digest:WRITING_PACKAGE.digest};
};

test('six-surface guard rejects foreign DTO and stale read/mutation across a render-time scope change',async()=>{
  const h=await surfaceHarness('hook',{company:'co',workspaceId:'w'});await h.flush();let guard=h.render();const read=guard.beginRead(),mutation=guard.capture();
  const scope=await operatingScope();assert.equal(h.helper.validateWritingSurfacePayload({entry:{scope},records:[]},'co','w').instance_id,'i');
  assert.throws(()=>h.helper.validateWritingSurfacePayload({entry:{scope:{...scope,company_id:'foreign'}},records:[]},'co','w'));
  assert.throws(()=>h.helper.validateWritingSurfacePayload({entry:{scope},records:[{tenant_id:scope.tenant_id,company_id:'foreign',workspace_id:'w',entity_id:'foreign'}]},'co','w'));
  h.setProps({company:'other',workspaceId:'w'});guard=h.render();assert.equal(guard.live(read),false);assert.equal(guard.live(mutation),false);await h.flush();assert.equal(h.render().live(mutation),false);
});

test('same ambiguous payload retries preserve identity; changed payload/version and successful new command do not',async()=>{
  const h=await surfaceHarness('hook',{company:'co',workspaceId:'w'});await h.flush();const guard=h.render();
  const first=await guard.request('save-direction','v1',{title:'原',confirmed:true});
  assert.equal((await guard.request('save-direction','v1',{confirmed:true,title:'原'})).request_id,first.request_id);
  assert.notEqual((await guard.request('save-direction','v2',{title:'原',confirmed:true})).request_id,first.request_id);
  const changed=await guard.request('save-direction','v1',{title:'改',confirmed:true});assert.notEqual(changed.request_id,first.request_id);
  guard.complete('save-direction',changed.token);assert.notEqual((await guard.request('save-direction','v1',{title:'改',confirmed:true})).request_id,changed.request_id);
});

test('actual market form cancellation retains same-scope input and ignores late foreign-scope reads',async()=>{
  const scope=await operatingScope();let resolveOld;const oldList=new Promise(resolve=>{resolveOld=resolve;});let calls=0;
  const api={snapshots:async company=>{calls++;return company==='co'&&calls===1?oldList:{entry:{scope:await operatingScope(company)},records:[]};},collection:async company=>({scope:await operatingScope(company),books:[],chapters:[],read_only:false})};
  const h=await surfaceHarness('WritingMarket.js',{company:'co',workspaceId:'w'},api);await h.flush();
  h.setProps({company:'other',workspaceId:'w'});assert.equal(JSON.stringify(h.render()).includes('录入新快照'),false);await h.flush();
  resolveOld({entry:{scope},records:[{tenant_id:scope.tenant_id,company_id:'co',workspace_id:'w',entity_id:'old',data:{title:'旧范围不可显示'}}]});await new Promise(resolve=>setTimeout(resolve,0));
  assert.equal(JSON.stringify(h.render()).includes('旧范围不可显示'),false);
  h.find(n=>n.props?.children==='录入新快照').props.onClick();h.find(n=>n.type==='input'&&n.props.maxLength===200).props.onChange({target:{value:'保留的标题'}});
  h.find(n=>n.props?.children==='取消').props.onClick();h.find(n=>n.props?.children==='录入新快照').props.onClick();assert.equal(h.find(n=>n.type==='input'&&n.props.maxLength===200).props.value,'保留的标题');
});

test('late market mutation success cannot clear or populate the next workspace form',async()=>{
  let finish;const writes=[];
  const api={snapshots:async company=>({entry:{scope:await operatingScope(company)},records:[]}),collection:async company=>({scope:await operatingScope(company),books:[],chapters:[],read_only:false}),snapshotCommand:async(company,workspace,action,payload)=>{writes.push({company,workspace,action,payload});return new Promise(resolve=>{finish=resolve;});}};
  const h=await surfaceHarness('WritingMarket.js',{company:'co',workspaceId:'w'},api);await h.flush();h.find(n=>n.props?.children==='录入新快照').props.onClick();
  h.find(n=>n.type==='input'&&n.props.maxLength===200).props.onChange({target:{value:'旧范围保存'}});h.find(n=>n.type==='textarea'&&n.props.rows===8).props.onChange({target:{value:'旧范围正文'}});h.find(n=>n.type==='input'&&n.props.maxLength===500).props.onChange({target:{value:'人工来源'}});
  const pending=h.find(n=>n.props?.children==='保存快照').props.onClick();await new Promise(resolve=>setTimeout(resolve,0));assert.equal(writes.length,1);
  h.setProps({company:'other',workspaceId:'w'});await h.flush();finish({record:{tenant_id:(await operatingScope()).tenant_id,company_id:'co',workspace_id:'w',entity_id:'old',data:{title:'旧范围保存'}}});await pending;
  assert.equal(JSON.stringify(h.render()).includes('旧范围保存'),false);h.find(n=>n.props?.children==='录入新快照').props.onClick();assert.equal(h.find(n=>n.type==='input'&&n.props.maxLength===200).props.value,'');
});

test('local publishing prepares only the explicitly selected immutable Formal and keeps platform publication separate',async()=>{
  const scope={...await operatingScope(),book_ref:'book',chapter_ref:'chapter'};const calls=[],routes=[];
  const state={scope,read_only:false,draft:{ref:'draft'},events:[{action:'formal.confirmed',ref:'formal',created_at:'2026-10-09',snapshot:{text:'作者确认的正文快照'}}]};
  const h=await surfaceHarness('WritingPublishingMain.js',{state,entry:{book:'book',chapter:'chapter',formal:'formal'},workspaceId:'w',command:async(action,data)=>{calls.push({action,data});return {ref:'local-package'};},busy:false,onNavigate:next=>routes.push(next)});await h.flush();
  h.find(n=>n.props?.['aria-label']==='作品介绍').props.onChange({target:{value:'作品介绍'}});h.find(n=>n.props?.['aria-label']==='署名').props.onChange({target:{value:'作者署名'}});h.find(n=>n.type==='input'&&n.props.type==='checkbox').props.onChange({target:{checked:true}});
  await h.find(n=>n.type==='form').props.onSubmit({preventDefault(){}});
  assert.equal(calls.length,1);assert.equal(calls[0].action,'package.prepared');assert.equal(calls[0].data.formal_ref,'formal');assert.equal(calls[0].data.target,'LOCAL_DOWNLOAD');assert.equal(calls[0].data.rights_declared,true);assert.equal(routes[0].package,'local-package');assert.ok(JSON.stringify(h.render()).includes('未上线'));
});

test('direction application requires explicit consent and only relates the selected existing chapter',async()=>{
  const scope=await operatingScope(),writes=[],details=[];const record={tenant_id:scope.tenant_id,company_id:'co',workspace_id:'w',entity_id:'direction',created_at:'2026-10-09',data:{identity_ref:'direction',revision:1,title:'原方向',body:'实际方向依据',scope_ref:'book',confirmed_by:'ceo',reference_refs:[],learning_ref:''}};
  const entry={scope};const collection={scope,books:[{ref:'book',title:'作品'}],chapters:[{ref:'chapter',bookRef:'book',title:'已有章节'}],read_only:false};
  const api={directions:async()=>({entry,records:[record]}),collection:async()=>collection,learnings:async()=>({entry,records:[]}),snapshots:async()=>({entry,records:[]}),directionCommand:async(c,w,a,p)=>{writes.push({c,w,a,p});return {book_ref:'book',chapter_ref:'chapter',direction_ref:'direction'};}};
  const h=await surfaceHarness('WritingDirection.js',{company:'co',workspaceId:'w',onInspect:d=>details.push(d)},api);await h.flush();h.find(n=>n.props?.children==='查看依据').props.onClick();assert.equal(details[0].ref,'direction');assert.equal(details[0].company,'co');
  h.find(n=>n.props?.children==='应用到章节').props.onClick();assert.equal(h.find(n=>n.props?.children==='确认应用').props.disabled,true);
  h.find(n=>n.type==='select'&&JSON.stringify(n.props.children).includes('请选择章节')).props.onChange({target:{value:'chapter'}});
  h.find(n=>n.type==='label'&&Array.isArray(n.props.children)&&n.props.children.includes('我确认只关联这个方向，不改写章节正文')).props.children[0].props.onChange({target:{checked:true}});
  await h.find(n=>n.props?.children==='确认应用').props.onClick();assert.equal(writes[0].a,'apply-direction');assert.equal(writes[0].p.data.chapter_ref,'chapter');assert.equal(Object.hasOwn(writes[0].p.data,'text'),false);assert.equal(writes[0].p.data.confirmed,true);
});

test('accepted learning use explicitly creates a new chapter and returns its actual identity',async()=>{
  const scope=await operatingScope(),writes=[],routes=[];const record={tenant_id:scope.tenant_id,company_id:'co',workspace_id:'w',entity_id:'learning',created_at:'2026-10-09',data:{identity_ref:'learning',revision:1,title:'经验',body:'已有经验',accepted_by:'ceo',basis_refs:[],applicability:'适用范围',counterexample:'限制'}};
  const entry={scope};const api={learnings:async()=>({entry,records:[record]}),collection:async()=>({scope,books:[{ref:'book',title:'作品'}],chapters:[],read_only:false}),learningCommand:async(c,w,a,p)=>{writes.push({c,w,a,p});return {book_ref:'book',chapter_ref:'new-actual',learning_ref:'learning'};}};
  const h=await surfaceHarness('WritingLearning.js',{company:'co',workspaceId:'w',onNavigate:value=>routes.push(value)},api);await h.flush();h.find(n=>n.props?.children==='应用到新章节').props.onClick();h.find(n=>n.type==='select').props.onChange({target:{value:'book'}});h.find(n=>n.type==='input'&&n.props.maxLength===160).props.onChange({target:{value:'明确的新章'}});
  assert.equal(h.find(n=>n.props?.children==='创建新章节并跳转').props.disabled,true);h.find(n=>n.type==='label'&&Array.isArray(n.props.children)&&n.props.children.includes('我确认创建一个新章节，不替换任何已有章节')).props.children[0].props.onChange({target:{checked:true}});
  await h.find(n=>n.props?.children==='创建新章节并跳转').props.onClick();assert.equal(writes[0].a,'use-learning');assert.equal(writes[0].p.data.learning_ref,'learning');assert.equal(Object.hasOwn(writes[0].p.data,'chapter_ref'),false);assert.equal(routes[0].chapter,'new-actual');
});

test('same workspace object switch immediately invalidates the previous form/read/mutation owner',async()=>{
  const h=await surfaceHarness('hook',{company:'co',workspaceId:'w',object:'book-one'});await h.flush();const token=h.render().capture();h.setProps({company:'co',workspaceId:'w',object:'book-two'});assert.equal(h.render().live(token),false);await h.flush();assert.equal(h.render().live(token),false);
});

test('native writing bridge verifies original package bytes before invoke and never promotes cancel/unsupported to saved',async()=>{
  const {saveNativeWritingPackage}=await import('../lib/nativeWritingExport.js');const scope={...await operatingScope(),book_ref:'book',chapter_ref:'chapter'};
  const value={schema_version:'writing.local-package/v1',metadata:{target:'LOCAL_DOWNLOAD'},external_publication:'NOT_PUBLISHED',scope,package_ref:'package',formal_ref:'formal'};const bytes=new TextEncoder().encode(JSON.stringify(value));
  const sha=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),n=>n.toString(16).padStart(2,'0')).join('');const prepared={ref:'package',formal_ref:'formal',content_sha256:sha};let calls=0;
  const bridge={invoke:async(name,args)=>{calls++;assert.equal(name,'save_writing_local_package');assert.equal(args.packageRef,'package');assert.equal(args.formalRef,'formal');assert.deepEqual(new Uint8Array(args.bytes),bytes);return {status:'SAVED',path:'/authorized/export/package.json',bytes:bytes.length,verified:true};}};
  assert.equal((await saveNativeWritingPackage(new Blob([bytes]),prepared,scope,bridge)).sha256,sha);
  assert.equal((await saveNativeWritingPackage(new Blob([bytes]),prepared,scope,{})).status,'UNSUPPORTED');
  assert.equal((await saveNativeWritingPackage(new Blob([bytes]),prepared,scope,{invoke:async()=>({status:'CANCELLED'})})).status,'CANCELLED');
  await assert.rejects(saveNativeWritingPackage(new Blob([bytes]),{...prepared,content_sha256:'bad'},scope,bridge));
  await assert.rejects(saveNativeWritingPackage(new Blob([bytes]),prepared,{...scope,company_id:'foreign'},bridge));
  await assert.rejects(saveNativeWritingPackage(new Blob([bytes]),prepared,scope,bridge,()=>false));assert.equal(calls,1);
});

test('learning evidence chooser exposes real existing operating records and keeps exact selected versions',async()=>{
  const scope=await operatingScope(),entry={scope};const record=(entity_id,title)=>({tenant_id:scope.tenant_id,company_id:'co',workspace_id:'w',entity_id,created_at:'2026-10-10',data:{title,revision:2}});const writes=[];
  const api={learnings:async()=>({entry,records:[]}),collection:async()=>({scope,books:[],chapters:[],read_only:false}),snapshots:async()=>({entry,records:[record('market-v2','市场来源')]}),directions:async()=>({entry,records:[record('direction-v2','方向来源')]}),observations:async()=>({entry,records:[record('observation-v2','观察来源')]}),learningCommand:async(c,w,a,p)=>{writes.push(p);return {record:record('learning','保存经验')};}};
  const h=await surfaceHarness('WritingLearning.js',{company:'co',workspaceId:'w'},api);await h.flush();h.find(n=>n.props?.children==='记录经验').props.onClick();const tree=JSON.stringify(h.render());for(const label of ['市场记录','作品方向','人工观察','原版本 2'])assert.ok(tree.includes(label));
  h.find(n=>n.type==='input'&&n.props.maxLength===200).props.onChange({target:{value:'经验标题'}});h.find(n=>n.type==='textarea'&&n.props.rows===8).props.onChange({target:{value:'经验正文'}});
  h.find(n=>n.type==='input'&&n.props.type==='checkbox'&&n.props.checked===false&&n.props.disabled===false).props.onChange();
  await h.find(n=>n.props?.children==='保存经验').props.onClick();assert.equal(writes[0].data.basis_refs[0],'market-v2');
});

test('Overview detail consumes the actual singular record DTO without requiring invented entry.scope',async()=>{
  const scope=await operatingScope(),details=[];const record={tenant_id:scope.tenant_id,company_id:'co',workspace_id:'w',entity_id:'direction',created_at:'2026-10-10',data:{title:'原方向',body:'实际正文',revision:1}};
  const overview={entry:{scope},books:[],chapters:[],directions:{current:[{ref:'direction',title:'原方向',scope_ref:'',confirmed:true,revision:1}]},learnings:{current:[],total_versions:0},snapshots:{total:0,latest:[]},observations:{total:0,latest:[]}};
  const h=await surfaceHarness('WritingOverview.js',{company:'co',workspaceId:'w',onInspect:data=>details.push(data)},{overview:async()=>overview,direction:async()=>({record,current_ref:'direction'})});await h.flush();await h.find(n=>n.props?.children==='原方向').props.onClick();assert.equal(details[0].ref,'direction');assert.ok(JSON.stringify(details[0].content).includes('实际正文'));
});

test('native save diagnostics preserve rejection type/class with no private strings in output or ordinary UI',async()=>{
  const {writingSaveDiagnostic,writingSaveFailureMessage}=await import('../lib/nativeWritingExport.js');
  const acl=writingSaveDiagnostic('Command save_writing_local_package not allowed by ACL');assert.equal(acl.errorType,'string');assert.equal(acl.code,'NSV_IPC_ACL');
  for(const reason of ['secret /Users/person/private/export/file.json?token=hidden',new Error('sensitive /private/tmp/root/id.json'),{code:'NSV_DIRECTORY',stage:'DIRECTORY',message:'/private/data/secret',bytes:[1,2],scope:{company_id:'private-id'}}]){
    const diagnostic=writingSaveDiagnostic(reason);assert.equal(Object.keys(diagnostic).length,6);const json=JSON.stringify(diagnostic);assert.equal(json.includes('/'),false);assert.equal(json.includes('private-id'),false);assert.equal(json.includes('hidden'),false);const ui=writingSaveFailureMessage(reason);assert.equal(ui.includes('/'),false);assert.ok(ui.includes('支持码'));
  }
  assert.equal(writingSaveDiagnostic(new Error('invalid args `scope`')).code,'NSV_IPC_ARGUMENT');
  assert.equal(writingSaveDiagnostic({message:'unknown'}).errorType,'object');
  assert.equal(writingSaveFailureMessage({diagnostic:{code:'/private/path'}}).includes('/private'),false);
});

test('save ACL is a separate exact-origin capability and does not broaden the existing core capability',async()=>{
  const {readFileSync}=await import('node:fs');const config=JSON.parse(readFileSync(new URL('../../desktop/tauri.conf.json',import.meta.url),'utf8'));const capabilities=config.app.security.capabilities;const save=capabilities.find(c=>c.identifier==='writing-local-package-export');assert.deepEqual(save.windows,['main']);assert.deepEqual(save.webviews,['main']);assert.equal(save.local,false);assert.deepEqual(save.remote.urls,['http://127.0.0.1:3010']);assert.deepEqual(save.permissions,['allow-save-writing-local-package']);
  for(const capability of capabilities.filter(c=>c!==save))assert.equal(capability.permissions.includes('allow-save-writing-local-package'),false);
});
