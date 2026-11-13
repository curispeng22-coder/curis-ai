import test from 'node:test';
import assert from 'node:assert/strict';
import { CG_PACKAGE, isContentGrowthPackage, selectionFor, selectionCurrent, stableRequest, cgReturnTarget, contentHref, cgEntry, requestLocked, cgInputKey, cgInputContext, cgInputSnapshot, restoreCgInput, cgPreferenceStatus, clearCreatedCgInput } from '../lib/contentGrowthState.mjs';
const version={entity_id:'v1',data:{body:'雨后😀，信仍未打开。'}};
test('UTF-16 saved selection and split surrogate rejection',()=>{
 const s=selectionFor(version,version.data.body,2,4);assert.equal(s.excerpt,'😀');assert.equal(selectionCurrent(s,version,version.data.body),true);
 assert.throws(()=>selectionFor(version,version.data.body,2,3));assert.throws(()=>selectionFor(version,'未保存',0,2));assert.equal(selectionCurrent(s,{...version,entity_id:'v2'},version.data.body),false);
});
test('unknown locks and identical request identity reused',()=>{
 assert.equal(requestLocked('UNKNOWN'),true);assert.equal(requestLocked('RUNNING'),true);assert.equal(requestLocked('COMPLETED'),false);
 const r=stableRequest(null,'save','v1',{body:'正文',references:[]},()=> 'original');assert.equal(stableRequest(r,'save','v1',{references:[],body:'正文'},()=> 'new').request_id,'original');assert.equal(stableRequest(r,'save','v2',{body:'正文',references:[]},()=> 'new').request_id,'new');
});
test('bounded exact repair content version and original request locator',()=>{
 const href=contentHref('workspace',{content:'content',version:'v1',binding:'binding',attempt:'attempt',start:2,end:4});const target=cgReturnTarget(href);assert.equal(target.entry.content,'content');assert.equal(target.entry.start,2);assert.equal(target.href,href);
 for(const invalid of ['https://evil.invalid','//evil.invalid','/ceo-office/workspace/installed/%2e%2e','/ceo-office/workspace/installed/w?cg_content=c&cg_content=d','/ceo-office/workspace/installed/w?cg_version=v','/ceo-office/workspace/installed/w?writing_mode=books','/ceo-office/workspace/installed/w?cg_content=c&cg_start=1&cg_end=2','/ceo-office/workspace/installed/w?cg_content=c&cg_binding=b'])assert.throws(()=>cgReturnTarget(invalid),invalid);
});
test('cg_view whitelist: materials/learning allowed, unknown fail closed',()=>{
 const params=(q)=>new URLSearchParams(q);
 assert.equal(cgEntry(params('')).view,'');
 assert.equal(cgEntry(params('cg_view=materials')).view,'materials');
 assert.equal(cgEntry(params('cg_view=learning')).view,'learning');
 for(const bad of ['cg_view=admin','cg_view=materials%27','cg_view=../x'])assert.ok(cgEntry(params(bad)).error,bad);
 // view must not combine with content-scoped locators into ambiguity; content params still validate independently.
 assert.equal(cgEntry(params('cg_view=materials&cg_version=v')).error!==undefined,true);
 const href=contentHref('workspace',{view:'learning'});assert.ok(href.includes('cg_view=learning'));
});
test('cg_sources: parsed, serialized, >8 fail-closed',()=>{
 const params=(q)=>new URLSearchParams(q);
 assert.deepEqual(cgEntry(params('cg_sources=ref-a,ref-b')).sources,['ref-a','ref-b']);
 assert.deepEqual(cgEntry(params('')).sources,[]);
 assert.deepEqual(cgEntry(params('cg_sources=')).sources,[]);
 assert.ok(cgEntry(params('cg_sources=a,b,c,d,e,f,g,h,i')).error,'>8 sources must fail closed');
 const href=contentHref('w',{sources:['ref-a','ref-b']});assert.ok(href.includes('cg_sources=ref-a%2Cref-b'));
});
test('exact package definition and instance required',()=>{
 const d={package:{package_id:CG_PACKAGE.id,version:CG_PACKAGE.version,digest:CG_PACKAGE.digest,schema_version:'curis.workspace-package/v1'},instance:{package_id:CG_PACKAGE.id,package_version:CG_PACKAGE.version,package_digest:CG_PACKAGE.digest},schemas:{ContentGraphic:{schemaVersion:CG_PACKAGE.version}}};assert.equal(isContentGrowthPackage(d),true);assert.equal(isContentGrowthPackage({...d,instance:{...d.instance,package_digest:'old'}}),false);
});

const ctx=cgInputContext('company','workspace','content',{scope:{tenant_id:'tenant'},actor:'ceo'});
const input={draft:{title:'标题',topic:'主题',audience:'受众',body:version.data.body,references:[]},base:'v1',selection:selectionFor(version,version.data.body,2,4),message:'尚未发送',discussion:true,assignment:'employee',model:'model'};
const store=()=>{const map=new Map();return {getItem:k=>map.get(k)||null,setItem:(k,v)=>map.set(k,v),removeItem:k=>map.delete(k)};};
test('same scoped input survives employee/model return, collapse and reload without authority',()=>{
 const s=store(),key=cgInputKey('company','workspace','content');
 s.setItem(key,JSON.stringify(cgInputSnapshot(ctx,{...input,grant:true,execution_authorized:true,pending_requests:[],task:'fake',usage:'fake'})));
 const restored=restoreCgInput(s.getItem(key),ctx);assert.deepEqual(restored,cgInputSnapshot(ctx,input));assert.equal(restored.message,'尚未发送');assert.equal(restored.assignment,'employee');assert.equal(restored.model,'model');assert.deepEqual(restored.selection,input.selection);
 for(const extra of ['grant','execution_authorized','pending_requests','task','usage'])assert.equal(extra in restored,false);
 s.setItem(key,JSON.stringify(cgInputSnapshot(ctx,{...restored,discussion:false})));assert.equal(restoreCgInput(s.getItem(key),ctx).discussion,false);assert.equal(restoreCgInput(s.getItem(key),ctx).message,input.message);
});
test('input scope isolates company, workspace, content, tenant and legal actor',()=>{
 const raw=JSON.stringify(cgInputSnapshot(ctx,input));for(const field of Object.keys(ctx))assert.equal(restoreCgInput(raw,{...ctx,[field]:'another'}),null,field);
 assert.notEqual(cgInputKey('a','w','c'),cgInputKey('b','w','c'));assert.notEqual(cgInputKey('a','w','c'),cgInputKey('a','w','d'));assert.notEqual(cgInputKey('a','w',null),cgInputKey('a','w','c'));
 assert.equal(restoreCgInput('broken',ctx),null);assert.equal(restoreCgInput(JSON.stringify(input),ctx),null);assert.equal(restoreCgInput(JSON.stringify(input),{...ctx,actor:''}),null);
});
test('explicit preferences retained but stale employee/model cannot qualify; pending outranks preference',()=>{
 const assignments=[{assignment_ref:'employee',models:[{model_key:'model'}]}];const restored=restoreCgInput(JSON.stringify(cgInputSnapshot(ctx,input)),ctx);
 assert.equal(cgPreferenceStatus(assignments,restored.assignment,restored.model).modelCurrent,true);
 assert.equal(cgPreferenceStatus([],restored.assignment,restored.model).stale,true);assert.equal(cgPreferenceStatus([],restored.assignment,restored.model).modelCurrent,false);
 assert.equal(cgPreferenceStatus([{assignment_ref:'employee',models:[]}],restored.assignment,restored.model).modelCurrent,false);
 assert.equal(cgPreferenceStatus(assignments,'','').modelCurrent,false);
 for(const status of ['RUNNING','UNKNOWN','UNVERIFIED'])assert.equal(requestLocked(status),true);
 assert.equal(selectionCurrent(restored.selection,{...version,entity_id:'v2'},version.data.body),false);
});
test('canonical create clears only exact new input; failed, uncertain, unsent, mismatched and repeated results retain it',()=>{
 const context={...ctx,content:'new'},key=cgInputKey('company','workspace',null),s=store();
 const cache=()=>s.setItem(key,JSON.stringify(cgInputSnapshot(context,input)));cache();s.setItem(cgInputKey('company','workspace','other'),'unrelated');
 const result={content:{entity_id:'new-canonical',company_id:'company',workspace_id:'workspace'}};
 for(const bad of [null,{}, {content:{entity_id:''}}, {...result,content:{...result.content,company_id:'another'}}, {...result,content:{...result.content,workspace_id:'another'}}]){assert.equal(clearCreatedCgInput(s,key,context,input.draft,bad),false);assert.ok(s.getItem(key));}
 assert.equal(clearCreatedCgInput(s,key,context,input.draft,result),true);assert.equal(s.getItem(key),null);assert.equal(s.getItem(cgInputKey('company','workspace','other')),'unrelated');
 assert.equal(clearCreatedCgInput(s,key,context,input.draft,result),false);
 const newer={...input.draft,body:'后来尚未发送的新输入'};s.setItem(key,JSON.stringify(cgInputSnapshot(context,{...input,draft:newer})));assert.equal(clearCreatedCgInput(s,key,context,input.draft,result),false);assert.equal(restoreCgInput(s.getItem(key),context).draft.body,newer.body);
});

test("operating views use the same bounded original-return whitelist", () => {
  for (const view of ["operating", "market", "production", "analysis"]) assert.equal(cgReturnTarget(contentHref("w", { view })).entry.view, view);
  assert.throws(() => cgReturnTarget("/ceo-office/workspace/installed/w?cg_view=analysis&cg_view=operating"));
});
