import test from 'node:test';
import assert from 'node:assert/strict';
import { pathToFileURL } from 'node:url';
const frontendRoot = process.env.CURIS_CG_TEST_FRONTEND_ROOT ? pathToFileURL(process.env.CURIS_CG_TEST_FRONTEND_ROOT.replace(/\/$/, '') + '/') : new URL('../', import.meta.url);
const { cgEntry, contentHref } = await import(new URL('lib/contentGrowthState.mjs', frontendRoot));
const { createContentGrowthApi } = await import(new URL('lib/contentGrowthApi.js', frontendRoot));

test('cg_view=verify is whitelisted and encoded; unknown views still fail closed', () => {
  const params = (q) => new URLSearchParams(q);
  assert.equal(cgEntry(params('cg_view=verify')).view, 'verify');
  assert.ok(cgEntry(params('cg_view=Verify')).error, 'case-sensitive whitelist');
  assert.ok(cgEntry(params('cg_view=publish')).error, 'no publish wording in routes');
  const href = contentHref('workspace', { view: 'verify' });
  assert.ok(href.includes('cg_view=verify'), href);
  assert.equal(cgEntry(new URL(href, 'https://x.invalid').searchParams).view, 'verify');
  assert.equal(cgEntry(params('cg_view=verify&cg_version=v')).error !== undefined, true);
});

test('verification api wrappers: routes, methods, payloads and blob export', async () => {
  const calls = [];
  const request = async (url, options) => { calls.push({ url, options }); return { ok: true }; };
  const api = createContentGrowthApi(request);
  await api.verificationTemplate('c1', 'w1', 'xhs');
  await api.verifications('c1', 'w1');
  await api.verification('c1', 'w1', 'cg-verify-a');
  const checks = [{ key: 'cover', checked: true }, { key: 'title_keywords', checked: false, note: '再改标题' }];
  await api.verificationCreate('c1', 'w1', 'req-1', { content_ref: 'content-1', account_ref: 'cg-account-a', checks });
  await api.verificationExport('c1', 'w1', 'cg-verify-a');
  const base = '/api/workspace/v1/companies/c1/content-growth/w1';
  assert.deepEqual(calls.map((c) => c.url), [
    `${base}/verification-template/xhs`, `${base}/verifications`, `${base}/verifications/cg-verify-a`,
    `${base}/verifications`, `${base}/verifications/cg-verify-a/export`,
  ]);
  assert.deepEqual(calls.map((c) => c.options?.method || 'GET'), ['GET', 'GET', 'GET', 'POST', 'GET']);
  const created = JSON.parse(calls[3].options.body);
  assert.equal(created.request_id, 'req-1');
  assert.equal(created.data.content_ref, 'content-1');
  assert.equal(created.data.account_ref, 'cg-account-a');
  assert.deepEqual(created.data.checks, checks);
  // Labels are deliberately not sent: the server owns checklist labels.
  assert.equal(created.data.checks[0].label, undefined);
  // Export fetches a blob (browser turns Content-Disposition attachment into a file save).
  assert.equal(calls[4].options.responseType, 'blob');
});

test('verification route ids are percent-encoded', async () => {
  const calls = [];
  const api = createContentGrowthApi(async (url, options) => { calls.push(url); return {}; });
  await api.verification('c', 'w', 'cg-verify/..');
  await api.verificationExport('c', 'w', 'cg-verify/..');
  assert.equal(calls[0], '/api/workspace/v1/companies/c/content-growth/w/verifications/cg-verify%2F..');
  assert.equal(calls[1], '/api/workspace/v1/companies/c/content-growth/w/verifications/cg-verify%2F../export');
});

test('verification view does not gain send or scheduled-publication locators', () => {
  for (const view of ['send', 'schedule', 'platform-publish']) assert.ok(cgEntry(new URLSearchParams({cg_view:view})).error);
});

import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import vm from 'node:vm';
const state = await import(new URL('lib/contentGrowthState.mjs', frontendRoot));
const native = await import('../lib/nativeContentGrowthExport.js');
const require = createRequire(new URL('package.json', frontendRoot));
const React = require('react'), swc = require('next/dist/build/swc');
await swc.loadBindings();
const { code } = await swc.transform(readFileSync(new URL('../components/content-growth/ContentGrowthVerify.js', import.meta.url), 'utf8'), {filename:'ContentGrowthVerify.js',isModule:true,jsc:{parser:{syntax:'ecmascript',jsx:true},transform:{react:{runtime:'automatic'}}},module:{type:'commonjs'}});
const nodes=(n,p)=>!n||typeof n!=='object'?[]:Array.isArray(n)?n.flatMap(x=>nodes(x,p)):[...(p(n)?[n]:[]),...nodes(n.props?.children,p)];
const text=n=>n==null?'':typeof n==='string'?n:Array.isArray(n)?n.map(text).join(''):typeof n==='object'?text(n.props?.children):String(n);
function mounted({browser=false,fetchBlob,invoke}={}) {
 const record={entity_id:'cg-verify-one',company_id:'c',data:{objectType:'PublishVerification',business_ref:'b',content_title:'原标题',content_body:'原正文',content_format:'graphic',account_ref:'cg-account-one',account_name:'账号',platform_ref:'xhs',platform_name:'小红书',checks:[{key:'cover',label:'封面',checked:false,note:''}],connection_status:'NOT_CONNECTED',verification:'UNVERIFIED',source:'CEO_MANUAL'}};
 const entry={scope:{tenant_id:'t',company_id:'c',workspace_id:'w',business_id:'b'},definition:{package_id:state.CG_PACKAGE.id,version:state.CG_PACKAGE.version,digest:state.CG_PACKAGE.digest}};
 const payload={...native.cgExportSelection(record,'c','b'),package_type:'curis.cg.local-verification-export/1',exported_at:'2026-10-23T00:00:00Z',notice:'本地核验导出，不构成发布；平台连接不存在。'};
 const bytes=new Blob([JSON.stringify(payload)]), calls={fetch:0,invoke:0,url:0};
 const bridge={invoke:async(...args)=>{calls.invoke++;return invoke?invoke(...args):{status:'SAVED',verified:true,bytes:bytes.size,path:'/synthetic/export/test.json'};}};
 const api={verifications:async()=>({entry,verifications:[record]}),collection:async()=>({entry,contents:[]}),accounts:async()=>({entry,accounts:[]}),verification:async()=>record,receipts:async()=>({entry,receipts:[]}),verificationExport:async()=>{calls.fetch++;return fetchBlob?fetchBlob(bytes):bytes;}};
 const slots=[],effects=[];let cursor=0,pane=null,tree;const same=(a,b)=>a&&b&&a.length===b.length&&a.every((v,i)=>Object.is(v,b[i]));
 const hooks={useState(initial){const i=cursor++;if(!(i in slots))slots[i]={value:typeof initial==='function'?initial():initial};return [slots[i].value,v=>{slots[i].value=typeof v==='function'?v(slots[i].value):v;}];},useRef(value){const i=cursor++;return slots[i]||=( {current:value});},useMemo(fn,deps){const i=cursor++;if(!slots[i]||!same(slots[i].deps,deps))slots[i]={deps,value:fn()};return slots[i].value;},useCallback(fn,deps){return hooks.useMemo(()=>fn,deps);},useEffect(fn,deps){const i=cursor++;if(!slots[i]||!same(slots[i].deps,deps)){const old=slots[i];slots[i]={deps};effects.push(()=>{old?.cleanup?.();slots[i].cleanup=fn();});}}};
 const module={exports:{}};const scopedNative={...native,saveNativeContentGrowthExport:(blob,selection,unused,current)=>native.saveNativeContentGrowthExport(blob,selection,bridge,current)};
 vm.runInNewContext(code,{module,exports:module.exports,window:browser?{}:{__TAURI_INTERNALS__:bridge},crypto:globalThis.crypto,structuredClone,URL:{createObjectURL(){calls.url++;return 'blob:synthetic';},revokeObjectURL(){}},require:name=>name==='react'?{...React,...hooks}:name==='react/jsx-runtime'?require(name):name==='next/link'?{__esModule:true,default:props=>React.createElement('a',props,props.children)}:name.endsWith('contentGrowthApi.js')?{contentGrowthApi:api}:name.endsWith('contentGrowthState.mjs')?state:name.endsWith('nativeContentGrowthExport.js')?scopedNative:name.endsWith('.module.css')?{__esModule:true,default:new Proxy({},{get:(_,k)=>k})}:{}});
 const props={company:'c',workspaceId:'w',onInspect:d=>{pane=d?.content||null;}};
 const render=()=>{cursor=0;return tree=module.exports.default(props);};
 const h={props,calls,render,async flush(){render();for(const fn of effects.splice(0))fn();await new Promise(resolve=>setImmediate(resolve));render();for(const fn of effects.splice(0))fn();},find(label){return nodes([tree,pane],n=>n.type==='button'&&text(n)===label)[0];},all(){return [tree,pane];},unmount(){for(const s of slots)s.cleanup?.();}};
 return h;
}
async function ready(h){await h.flush();await h.flush();await h.find('查看').props.onClick();await h.flush();}
test('compiled native UI blocks duplicate save and only reports verified readback',async()=>{
 let release;const h=mounted({fetchBlob:bytes=>new Promise(resolve=>release=()=>resolve(bytes))});await ready(h);
 const click=h.find('导出本地文件').props.onClick;const pending=click();await click();await h.flush();assert.equal(h.calls.fetch,1);assert.equal(h.find('导出本地文件').props.disabled,true);
 release();await pending;await h.flush();assert.equal(h.calls.invoke,1);assert.equal(h.calls.url,0);assert.match(text(h.all()),/本地文件已保存并读回核验/);
 assert.equal(nodes(h.all(),n=>n.type==='a'&&n.props.download).length,0);
});
test('compiled UI keeps browser anchor and does not claim browser file completion',async()=>{
 const h=mounted({browser:true});await ready(h);await h.find('导出本地文件').props.onClick();await h.flush();assert.equal(h.calls.invoke,0);assert.equal(h.calls.url,1);assert.equal(nodes(h.all(),n=>n.type==='a'&&n.props.download).length,1);assert.doesNotMatch(text(h.all()),/已保存并读回/);
});
test('compiled UI cancel and invalid result never say saved',async()=>{
 for(const value of [{status:'CANCELLED',verified:false,path:null,bytes:0},{status:'SAVED',verified:false,path:'/synthetic',bytes:1}]){
 const h=mounted({invoke:async()=>value});await ready(h);await h.find('导出本地文件').props.onClick();await h.flush();assert.doesNotMatch(text(h.all()),/已保存并读回/);assert.match(text(h.all()),value.status==='CANCELLED'?/已取消保存/:/尚未核验/);
 }
});
test('compiled UI discards old fetch after prop scope change or unmount before effects',async()=>{
 for(const unmount of [false,true]){let release;const h=mounted({fetchBlob:bytes=>new Promise(resolve=>release=()=>resolve(bytes))});await ready(h);const pending=h.find('导出本地文件').props.onClick();
 if(unmount)h.unmount();else {h.props.company='other';h.render();}
 release();await pending;assert.equal(h.calls.invoke,0);assert.equal(h.calls.url,0);}
});

test('old compiled pane callback cannot fetch after scope changes before effects',async()=>{
 const h=mounted();await ready(h);const staleClick=h.find('导出本地文件').props.onClick;
 h.props.company='other';h.render();await staleClick();
 assert.equal(h.calls.fetch,0);assert.equal(h.calls.invoke,0);assert.equal(h.calls.url,0);
});
