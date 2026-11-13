import assert from 'node:assert/strict';
import test from 'node:test';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { webcrypto } from 'node:crypto';
import vm from 'node:vm';
const require = createRequire(import.meta.url), React = require('react'), swc = require('next/dist/build/swc');
const api = await import('../lib/api.js'), v1 = await import('../lib/v1FrontendApi.js');
// Resolve the local compiler before loadBindings; tests never download dependencies.
const swcRequire = createRequire(require.resolve('next/dist/build/swc'));
const localSwc = Object.keys(require('next/package.json').optionalDependencies || {})
  .filter(name => name.startsWith(`@next/swc-${process.platform}-${process.arch}`))
  .some(name => { try { swcRequire.resolve(name); return true; } catch { return false; } });
assert.ok(localSwc, 'Install the local native SWC dependency before running these offline tests');
globalThis.fetch=async()=>{throw Error('REAL_NETWORK_FORBIDDEN');};
await swc.loadBindings();
const compiled = (await swc.transform(readFileSync(new URL('../components/v1/ModelManagement.js', import.meta.url), 'utf8'), { filename:'ModelManagement.js',isModule:true,jsc:{parser:{syntax:'ecmascript',jsx:true},transform:{react:{runtime:'automatic'}}},module:{type:'commonjs'} })).code + '\nexports.Content = ModelManagementContent;';
const SECRET = 'synthetic-component-recovery-key', ID = 'cred-00000000-0000-0000-0000-000000000001';
const metadata = {tenant_id:api.TENANT_ID,credential_id:ID,credential_ref:`vault://tenant/${api.TENANT_ID}/credential/${ID}`,provider:'deepseek',storage:'macos_keychain',status:'active'};
const providers = {providers:[{provider_id:'deepseek',name:'DeepSeek',base_url:'https://api.deepseek.com',auth:'bearer',protocol:'openai_chat',discovery_mode:'models',configured:false},{provider_id:'ollama',name:'Ollama',base_url:'http://127.0.0.1:9',auth:'none',configured:false}]};
const tick=()=>new Promise(r=>setImmediate(r));
const deferred=()=>{let resolve;const promise=new Promise(r=>resolve=r);return {promise,resolve};};
function nodes(tree, predicate) {const result=[];function visit(n){if(!n||typeof n!=='object')return;if(Array.isArray(n))return n.forEach(visit);if(predicate(n))result.push(n);visit(n.props?.children);}visit(tree);return result;}
function text(n){if(n==null||typeof n==='boolean')return '';if(typeof n!=='object')return String(n);return Array.isArray(n)?n.map(text).join(''):text(n.props?.children);}
const button=(h)=>nodes(h.tree,n=>n.type==='button'&&/测试连接并发现模型|正在测试/.test(text(n)))[0];
const password=(h)=>nodes(h.tree,n=>n.type==='input'&&n.props.type==='password')[0];
function fixture(options={}) {
  const calls=[];let rows=options.rows||[], connected=false, preference=options.preference||null, preferenceReads=0, providerReads=0;
  globalThis.fetch=async(url,request={})=>{
    const path=new URL(url).pathname, method=request.method||'GET';calls.push({path,method,body:request.body?JSON.parse(request.body):undefined});
    const reply=(payload,status=200)=>({ok:status>=200&&status<300,status,statusText:'Technical response',json:async()=>payload});
    if(path==='/api/workspace/ai-capabilities/providers') { providerReads++; if(providerReads===1&&options.waitFirstProviders) { await options.waitFirstProviders.promise; if(options.failFirstProviders) throw Error('OLD_COMPANY_PROVIDER_METADATA_FAILURE'); } return reply({providers:providers.providers.map(p=>({...p,configured:p.provider_id==='deepseek'&&(connected||Boolean(options.restored))}))}); }
    if(path==='/api/workspace/private-models')return reply({models:options.models || ((connected || options.restored) ? savedModels : [])});
    if(path==='/api/workspace/model-preference') { let first=false; if(method==='GET') { preferenceReads++;first=preferenceReads===(options.waitPreferenceReadNumber||1); if(first&&options.waitFirstPreference)await options.waitFirstPreference.promise; } if(method==='PUT') { if(options.waitPreference) await options.waitPreference.promise; if(options.rejectPreference) return reply({detail:'Model no longer eligible'},422); preference={model_key:JSON.parse(request.body).model_key}; } return reply({preference,available_models:(connected || options.restored) ? (first&&options.firstAvailable ? options.firstAvailable : options.available || eligibleModels) : []}); }
    if(path==='/api/workspace/credentials'&&method==='GET')return reply({credentials:rows});
    if(path.startsWith('/api/workspace/credentials')&&method!=='GET') {
      if(options.waitStore)await options.waitStore.promise;
      if(options.loss)throw Error('Technical transport response lost');
      if(options.detail)return reply({detail:options.detail,...(options.code?{code:options.code,stage:options.stage,certainty:options.certainty,os_status:options.osStatus}:{})},options.status||422);
      if(options.malformed)return reply(null);
      rows=[metadata];return reply(options.badMetadata || metadata,method==='POST'?201:200);
    }
    if(path.endsWith('/connect')||path.endsWith('/recover')) {
      if(options.waitProvider)await options.waitProvider.promise;
      if(options.providerFail)return reply({detail:'Technical provider unavailable'},422);
      connected=true;return reply({health:'healthy',models:options.emptyDiscovery ? [] : discoveredModels});
    }
    throw Error('Unexpected fake request: '+path);
  };
  return {calls,storeCalls:()=>calls.filter(c=>c.path.startsWith('/api/workspace/credentials')&&c.method!=='GET'),providerCalls:()=>calls.filter(c=>(c.path.endsWith('/connect')||c.path.endsWith('/recover')))};
}
function scene(storage=new Map(),runtime={status:'ready',companyId:'company-A'}) {
  const slots=[],pending=[];let cursor=0,tree,runtimeValue=runtime;
  const same=(a,b)=>a&&b&&a.length===b.length&&a.every((v,i)=>Object.is(v,b[i]));
  const hooks={useCallback(fn,deps){return hooks.useMemo(()=>fn,deps);},useState(initial){const i=cursor++;if(!(i in slots))slots[i]={value:typeof initial==='function'?initial():initial};return [slots[i].value,v=>{slots[i].value=typeof v==='function'?v(slots[i].value):v;}];},useRef(initial){const i=cursor++;return slots[i]||=( {current:initial});},useMemo(fn,deps){const i=cursor++;if(!slots[i]||!same(slots[i].deps,deps))slots[i]={deps,value:fn()};return slots[i].value;},useLayoutEffect(fn,deps){return hooks.useEffect(fn,deps);},useEffect(fn,deps){const i=cursor++;if(!slots[i]||!same(slots[i].deps,deps)){const old=slots[i];slots[i]={deps};pending.push(()=>{old?.cleanup?.();slots[i].cleanup=fn();});}}};
  const compiledModule={exports:{}};
  vm.runInNewContext(compiled,{module:compiledModule,exports:compiledModule.exports,URLSearchParams,URL,TextEncoder,Uint8Array,crypto:webcrypto,console,sessionStorage:{getItem:k=>storage.has(k)?storage.get(k):null,setItem:(k,v)=>storage.set(k,v),removeItem:k=>storage.delete(k)},require:path=>{
    if(path==='react')return {...React,...hooks};
    if(path==='react/jsx-runtime')return require(path);
    if(path==='next/navigation')return {useSearchParams:()=>new URLSearchParams()};
    if(path.includes('RuntimeProvider'))return {useRuntime:()=>runtimeValue};
    if(path.endsWith('/lib/api.js'))return api;
    if(path.endsWith('/lib/v1FrontendApi.js'))return v1;
    if(path.includes('businessReturnApi'))return {businessReturnInput:()=>null};
    if(path.includes('settingsEntryState'))return {settingsModelHref:()=>null};
    return {__esModule:true,default:({children})=>React.createElement('main',null,children)};
  }});
  const h={get runtime(){return runtimeValue;},setRuntime(value){runtimeValue=value;},storage,get tree(){return tree;},render(){cursor=0;tree=compiledModule.exports.Content();while(pending.length)pending.shift()();},async settle(){for(let i=0;i<20;i++){h.render();await tick();}h.render();},unmount(){slots.forEach(s=>s.cleanup?.());},enter(){password(h).props.onChange({target:{value:SECRET}});h.render();}};
  return h;
}
function noSecret(h){assert.equal(password(h).props.value,'');assert.ok(![...h.storage.values()].join('').includes(SECRET));assert.ok(!text(h.tree).includes(SECRET));}

test('existing workspaceFetch delivers safe detail and status once',async()=>{
 let calls=0;globalThis.fetch=async()=>{calls++;return {ok:false,status:404,statusText:'Technical',json:async()=>({detail:'macOS Keychain store cancelled (OSStatus -128)'})};};
 await assert.rejects(api.workspaceFetch('/api/workspace/credentials'),e=>e.status===404&&e.message.includes('OSStatus -128'));assert.equal(calls,1);
});
test('workspaceFetch preserves only the recognized credential outcome code',async()=>{
 globalThis.fetch=async()=>({ok:false,status:422,statusText:'Technical',json:async()=>({detail:'SENTINEL_SECRET',code:'CREDENTIAL_WRITE_NOT_STARTED',stage:'preflight',certainty:'not_started',os_status:-25307})});
 await assert.rejects(api.workspaceFetch('/api/workspace/credentials',{method:'POST'}),e=>e.status===422&&e.code==='CREDENTIAL_WRITE_NOT_STARTED'&&e.phase==='preflight'&&e.certainty==='not_started'&&e.osStatus===-25307&&!e.message.includes('SENTINEL_SECRET'));
 await assert.rejects(api.workspaceFetch('/api/workspace/credentials'),e=>e.status===422&&!e.code);
 globalThis.fetch=async()=>({ok:false,status:422,statusText:'Technical',json:async()=>({detail:'unknown outcome',code:'UNTRUSTED_CODE'})});
 await assert.rejects(api.workspaceFetch('/api/workspace/credentials',{method:'POST'}),e=>e.status===422&&!e.code);
 globalThis.fetch=async()=>({ok:false,status:422,statusText:'Technical',json:async()=>({detail:'SENTINEL_SECRET',code:'CREDENTIAL_NATIVE_WRITE_UNCONFIRMED',stage:'metadata',certainty:'unknown'})});
 await assert.rejects(api.workspaceFetch('/api/workspace/credentials',{method:'POST'}),e=>e.status===422&&!e.code&&!e.message.includes('SENTINEL_SECRET'));
});
for(const [label,options] of [['preflight',{detail:'SENTINEL_SECRET',code:'CREDENTIAL_WRITE_NOT_STARTED',stage:'preflight',certainty:'not_started',osStatus:-25307}],['native',{detail:'SENTINEL_SECRET',code:'CREDENTIAL_NATIVE_WRITE_UNCONFIRMED',stage:'native_store',certainty:'unknown',osStatus:-128}],['metadata',{detail:'SENTINEL_SECRET',code:'CREDENTIAL_METADATA_UNCONFIRMED',stage:'metadata',certainty:'native_returned_success',status:500}],['audit',{detail:'SENTINEL_SECRET',code:'CREDENTIAL_AUDIT_FAILED',stage:'audit',certainty:'metadata_returned_success',status:500}],['cancel',{detail:'macOS Keychain store cancelled (OSStatus -128)'}],['loss',{loss:true}],['malformed',{malformed:true}]])test('actual component holds '+label+' across remount without a second write',async()=>{
 const f=fixture(options),storage=new Map(),h=scene(storage);await h.settle();h.enter();await button(h).props.onClick();await h.settle();assert.equal(f.storeCalls().length,1);assert.equal(f.providerCalls().length,0);noSecret(h);assert.equal(Boolean(button(h).props.disabled),true);assert.match(text(h.tree),({preflight:/写入未开始/,native:/写入阶段返回错误/,metadata:/资料登记失败/,audit:/完成记录失败/})[label]||/尚未确认/);assert.ok(!text(h.tree).includes('SENTINEL_SECRET'));h.unmount();
 const restored=scene(storage);await restored.settle();await button(restored).props.onClick();assert.equal(f.storeCalls().length,1);assert.equal(Boolean(button(restored).props.disabled),true);restored.unmount();
});
test('saved receipt clears secret before provider reply and reuses metadata-confirmed ref after failure/remount',async()=>{
 const wait=deferred(),f=fixture({waitProvider:wait,providerFail:true}),storage=new Map(),h=scene(storage);await h.settle();h.enter();const request=button(h).props.onClick();await h.settle();assert.equal(f.storeCalls().length,1);assert.equal(f.providerCalls().length,1);noSecret(h);wait.resolve();await request;await h.settle();assert.match(text(h.tree),/凭据已保存/);h.unmount();
 const restored=scene(storage);await restored.settle();await button(restored).props.onClick();await restored.settle();assert.equal(f.storeCalls().length,1);assert.equal(f.providerCalls().length,2);assert.ok(f.providerCalls().every(c=>c.body.credential_ref===metadata.credential_ref));noSecret(restored);restored.unmount();
});
test('valid save response with failed local receipt is held without provider call or repeat',async()=>{
 const f=fixture(),storage=new Map(),originalSet=storage.set;
 storage.set=function(key,value){if(typeof value==='string'&&value.includes('"state":"KNOWN"'))throw Error('synthetic local receipt failure');return originalSet.call(this,key,value);};
 const h=scene(storage);await h.settle();h.enter();await button(h).props.onClick();await h.settle();
 assert.equal(f.storeCalls().length,1);assert.equal(f.providerCalls().length,0);assert.equal(Boolean(button(h).props.disabled),true);
 assert.match(text(h.tree),/服务端已返回有效保存结果，但本地保护回执失败/);noSecret(h);
 await button(h).props.onClick();assert.equal(f.storeCalls().length,1);h.unmount();
});
test('same tick reentry and pending Company switch cannot create or connect under another scope',async()=>{
 const wait=deferred(),f=fixture({waitStore:wait}),storage=new Map(),runtime={status:'ready',companyId:'company-A'},h=scene(storage,runtime);await h.settle();h.enter();const click=button(h).props.onClick;const first=click();await click();assert.equal(f.storeCalls().length,1);runtime.companyId='company-B';await h.settle();await button(h).props.onClick();assert.equal(f.storeCalls().length,1);wait.resolve();await first;await h.settle();assert.equal(f.providerCalls().length,0);h.unmount();
 const restored=scene(storage,runtime);await restored.settle();await button(restored).props.onClick();assert.equal(f.storeCalls().length,1);assert.equal(f.providerCalls().length,0);restored.unmount();
});
test('PUT404 storage failure holds the existing reference rather than fallback create',async()=>{
 const f=fixture({models:[{provider_type:'deepseek',credential_ref:metadata.credential_ref}],rows:[metadata],detail:'macOS Keychain store cancelled (OSStatus -128)',status:404}),h=scene();await h.settle();h.enter();await button(h).props.onClick();await h.settle();assert.equal(f.storeCalls().length,1);assert.equal(f.storeCalls()[0].method,'PUT');assert.equal(f.providerCalls().length,0);assert.equal(Boolean(button(h).props.disabled),true);noSecret(h);h.unmount();
});
test('known receipt with missing metadata cannot create or use another ref',async()=>{
 const f=fixture({providerFail:true}),storage=new Map(),h=scene(storage);await h.settle();h.enter();await button(h).props.onClick();h.unmount();fixture({rows:[]});const restored=scene(storage);await restored.settle();await button(restored).props.onClick();assert.equal(Boolean(button(restored).props.disabled),true);assert.equal(f.storeCalls().length,1);restored.unmount();
});
test('successful ordinary connect keeps default selection and never persists the key or endpoint',async()=>{
 const f=fixture(),h=scene();await h.settle();h.enter();await button(h).props.onClick();await h.settle();assert.equal(f.storeCalls().length,1);assert.equal(f.providerCalls().length,1);assert.match(text(h.tree),/设为默认/);noSecret(h);assert.ok(![...h.storage.values()].join('').includes('https://api.deepseek.com'));h.unmount();
});
test('corrupt marker is held without a write',async()=>{
 const f=fixture(),storage=new Map([[`curis.modelCredentialAttempt:${JSON.stringify([api.TENANT_ID,'deepseek'])}`,'{bad json']]),h=scene(storage);await h.settle();await button(h).props.onClick();assert.equal(f.storeCalls().length,0);assert.equal(f.providerCalls().length,0);h.unmount();
});

for (const change of [{credential_id:'cred------------------------------------'},{tenant_id:'other-tenant'},{provider:'ollama'},{status:'disabled'}])test('malformed successful storage metadata is UNKNOWN: '+Object.keys(change)[0],async()=>{
 const f=fixture({badMetadata:{...metadata,...change}}),h=scene();await h.settle();h.enter();await button(h).props.onClick();await h.settle();assert.equal(f.storeCalls().length,1);assert.equal(f.providerCalls().length,0);assert.equal(Boolean(button(h).props.disabled),true);noSecret(h);h.unmount();
});
test('endpoint mismatch holds receipt and exact original endpoint restores metadata-confirmed ref',async()=>{
 const f=fixture({providerFail:true}),h=scene();await h.settle();h.enter();await button(h).props.onClick();await h.settle();const endpoint=()=>nodes(h.tree,n=>n.type==='input'&&!n.props.type)[0];endpoint().props.onChange({target:{value:'https://api.deepseek.com/changed'}});await h.settle();await button(h).props.onClick();assert.equal(f.storeCalls().length,1);assert.equal(f.providerCalls().length,1);assert.equal(Boolean(button(h).props.disabled),true);
 endpoint().props.onChange({target:{value:'https://api.deepseek.com'}});await h.settle();await button(h).props.onClick();assert.equal(f.storeCalls().length,1);assert.equal(f.providerCalls().length,2);noSecret(h);h.unmount();
});
test('two mounted components reread the pending marker before storage',async()=>{
 const wait=deferred(),f=fixture({waitStore:wait}),storage=new Map(),a=scene(storage),b=scene(storage);await a.settle();await b.settle();a.enter();b.enter();const one=button(a).props.onClick();await button(b).props.onClick();assert.equal(f.storeCalls().length,1);wait.resolve();await one;a.unmount();b.unmount();
});

test('structured corrupt receipt stays held without copying an invalid ref into a new marker',async()=>{
 const f=fixture(),storage=new Map(),h=scene(storage);await h.settle();h.enter();await button(h).props.onClick();h.unmount();const key=[...storage.keys()][0],record=JSON.parse(storage.get(key));record.ref='untrusted-invalid-reference';const original=JSON.stringify(record);storage.set(key,original);const restored=scene(storage);await restored.settle();await button(restored).props.onClick();assert.equal(f.storeCalls().length,1);assert.equal(f.providerCalls().length,1);assert.equal(storage.get(key),original);assert.equal(Boolean(button(restored).props.disabled),true);assert.ok(!text(restored.tree).includes(record.ref));restored.unmount();
});

test('ordinary tenant model configuration does not add a Company prerequisite',async()=>{
 const f=fixture(),h=scene(new Map(),{status:'ready',companyId:null});await h.settle();h.enter();await button(h).props.onClick();await h.settle();assert.equal(f.storeCalls().length,1);assert.equal(f.providerCalls().length,1);noSecret(h);h.unmount();
});

test('denied PENDING marker write clears secret and holds before any credential or Provider request',async()=>{
 class DeniedPending extends Map {set(key,value){if(!key.includes(':probe:')&&JSON.parse(value).state==='PENDING')throw Error('Technical session marker write denied');return super.set(key,value);}}
 const f=fixture(),h=scene(new DeniedPending());await h.settle();h.enter();await button(h).props.onClick();await h.settle();noSecret(h);assert.equal(Boolean(button(h).props.disabled),true);assert.match(text(h.tree),/本次未发送凭据请求/);assert.equal(f.storeCalls().length,0);assert.equal(f.providerCalls().length,0);await button(h).props.onClick();assert.equal(f.storeCalls().length,0);assert.equal(f.providerCalls().length,0);h.unmount();
});
for(const operation of ['set','get','remove'])test('unavailable session protection blocks Key entry at '+operation,async()=>{
 class DeniedProbe extends Map {
  set(key,value){if(operation==='set'&&key.includes(':probe:'))throw Error('Technical probe denied');return super.set(key,value);}
  get(key){if(operation==='get'&&key.includes(':probe:'))throw Error('Technical probe denied');return super.get(key);}
  delete(key){if(operation==='remove'&&key.includes(':probe:'))throw Error('Technical probe denied');return super.delete(key);}
 }
 const marker=`curis.modelCredentialAttempt:${JSON.stringify([api.TENANT_ID,'deepseek'])}`,storage=new DeniedProbe([[marker,'{old unknown marker']]),f=fixture(),h=scene(storage);await h.settle();assert.equal(password(h).props.disabled,true);assert.equal(Boolean(button(h).props.disabled),true);assert.match(text(h.tree),/本地会话保护不可用/);assert.equal(f.storeCalls().length,0);assert.equal(f.providerCalls().length,0);assert.equal(storage.get(marker),'{old unknown marker');noSecret(h);h.unmount();
});
for(const status of [422,500])test('untyped '+status+' stays UNKNOWN after a credential request',async()=>{
 const f=fixture({detail:'technical rejection',status}),h=scene();await h.settle();h.enter();await button(h).props.onClick();await h.settle();assert.equal(f.storeCalls().length,1);assert.equal(f.providerCalls().length,0);assert.match(text(h.tree),/保存结果尚未确认/);assert.doesNotMatch(text(h.tree),/写入未开始/);noSecret(h);h.unmount();
});
test('failed KNOWN receipt after a successful storage response remains held',async()=>{
 class DeniedKnown extends Map {set(key,value){if(!key.includes(':probe:')&&JSON.parse(value).state==='KNOWN')throw Error('Technical known receipt denied');return super.set(key,value);}}
 const f=fixture(),h=scene(new DeniedKnown());await h.settle();h.enter();await button(h).props.onClick();await h.settle();assert.equal(f.storeCalls().length,1);assert.equal(f.providerCalls().length,0);assert.equal(Boolean(button(h).props.disabled),true);assert.match(text(h.tree),/服务端已返回有效保存结果，但本地保护回执失败/);noSecret(h);h.unmount();
});

// Model selection and Runtime lifecycle regressions, using this same fake harness.
const discoveredModels=[{capability_id:'fake.pro',model_id:'deepseek-v4-pro',display_name:'deepseek-v4-pro'},{capability_id:'fake.flash',model_id:'deepseek-flash',display_name:'deepseek-flash'}];
const savedModels=discoveredModels.map(m=>({tenant_id:api.TENANT_ID,provider_type:'deepseek',model_name:m.model_id,base_url:'https://api.deepseek.com',enabled:true,source:'tenant_private',credential_ref:metadata.credential_ref}));
const eligibleModels=discoveredModels.map(m=>({source:'tenant_private',provider_id:'deepseek',model_key:m.capability_id,model_name:m.model_id,display_name:m.display_name,status:'active'}));
const chooseButton=h=>nodes(h.tree,n=>n.type==='button'&&text(n)==='设为默认')[0];
const modelSelect=h=>nodes(h.tree,n=>n.type==='select'&&nodes(n,v=>v.type==='option').some(v=>v.props.value==='fake.flash'))[0];
test('candidate uses eligible saved choices after remount without discover or credential rewrite',async()=>{
 const f=fixture(),storage=new Map(),h=scene(storage);await h.settle();h.enter();await button(h).props.onClick();await h.settle();h.unmount();const restored=scene(storage);await restored.settle();assert.ok(modelSelect(restored));assert.match(text(restored.tree),/未重新测试连接/);modelSelect(restored).props.onChange({target:{value:'fake.flash'}});await restored.settle();await chooseButton(restored).props.onClick();await restored.settle();assert.equal(f.providerCalls().length,1);assert.equal(f.storeCalls().length,1);assert.equal(f.calls.filter(c=>c.method==='PUT'&&c.path.endsWith('/model-preference')).length,1);assert.equal(f.calls.at(-1).body.model_key,'fake.flash');noSecret(restored);restored.unmount();
});
test('candidate shows explicit success and accurate available labels without another request',async()=>{
 const f=fixture(),h=scene();await h.settle();h.enter();await button(h).props.onClick();await h.settle();assert.match(text(h.tree),/连接成功，请选择模型并设为默认/);assert.doesNotMatch(text(h.tree),/等待重新验证/);assert.equal(f.providerCalls().length,1);noSecret(h);h.unmount();
});
test('candidate recovers choices from validated metadata when successful response has no in-memory choices; fixture is not root-cause proof',async()=>{
 const f=fixture({emptyDiscovery:true}),h=scene();await h.settle();h.enter();await button(h).props.onClick();await h.settle();assert.ok(chooseButton(h));assert.match(text(h.tree),/未重新测试连接/);assert.equal(f.providerCalls().length,1);h.unmount();
});
for (const [label,options] of [['ineligible',{available:[]}],['foreign provider',{available:eligibleModels.map(x=>({...x,provider_id:'ollama'}))}],['official model',{available:eligibleModels.map(x=>({...x,source:'official'}))}],['different endpoint',{models:savedModels.map(x=>({...x,base_url:'https://other.invalid'}))}],['disabled saved model',{models:savedModels.map(x=>({...x,enabled:false}))}]]) test('candidate excludes '+label+' persisted choices',async()=>{
 const f=fixture({restored:true,...options}),h=scene();await h.settle();assert.equal(chooseButton(h),undefined);assert.equal(f.providerCalls().length,0);assert.equal(f.storeCalls().length,0);h.unmount();
});
test('candidate UNKNOWN credential marker cannot enable saved choices or issue a request',async()=>{
 const storage=new Map([[`curis.modelCredentialAttempt:${JSON.stringify([api.TENANT_ID,'deepseek'])}`,'{invalid-marker']]),f=fixture({restored:true}),h=scene(storage);await h.settle();assert.equal(chooseButton(h),undefined);assert.ok(button(h).props.disabled);await button(h).props.onClick();assert.equal(f.calls.filter(x=>x.method!=='GET').length,0);h.unmount();
});

test('candidate provider and endpoint switches cannot select a saved model from a different scope',async()=>{
 const f=fixture({restored:true}),h=scene();await h.settle();assert.ok(chooseButton(h));const endpoint=()=>nodes(h.tree,n=>n.type==='input'&&!n.props.type)[0];endpoint().props.onChange({target:{value:'https://other.invalid'}});await h.settle();assert.equal(chooseButton(h),undefined);endpoint().props.onChange({target:{value:'https://api.deepseek.com'}});await h.settle();assert.ok(chooseButton(h));nodes(h.tree,n=>n.type==='button'&&text(n).includes('Ollama'))[0].props.onClick();await h.settle();assert.equal(chooseButton(h),undefined);assert.equal(f.calls.filter(c=>c.method!=='GET').length,0);h.unmount();
});
test('candidate Company switch drops old metadata choices, return preserves original eligible scope',async()=>{
 const f=fixture({restored:true}),runtime={status:'ready',companyId:'company-A'},h=scene(new Map(),runtime);await h.settle();assert.ok(chooseButton(h));runtime.companyId='company-B';h.render();assert.equal(chooseButton(h),undefined);await h.settle();assert.ok(chooseButton(h));assert.equal(f.calls.filter(c=>c.path.endsWith('/model-preference')).length,2);runtime.companyId='company-A';await h.settle();assert.ok(chooseButton(h));assert.equal(f.calls.filter(c=>c.method!=='GET').length,0);h.unmount();
});
test('candidate rejects saved models from another tenant',async()=>{
 const f=fixture({restored:true,models:savedModels.map(x=>({...x,tenant_id:'other-tenant'}))}),h=scene();await h.settle();assert.equal(chooseButton(h),undefined);assert.equal(f.calls.filter(c=>c.method!=='GET').length,0);h.unmount();
});
test('candidate server rejection of expired model does not persist conversation selection or rediscover',async()=>{
 const f=fixture({restored:true,rejectPreference:true}),h=scene();await h.settle();modelSelect(h).props.onChange({target:{value:'fake.flash'}});await h.settle();await chooseButton(h).props.onClick();await h.settle();assert.match(text(h.tree),/默认模型选择尚未确认/);assert.equal(h.storage.has('curis.v1.conversationModel'),false);assert.equal(f.providerCalls().length,0);assert.equal(f.storeCalls().length,0);assert.equal(f.calls.filter(c=>c.method==='PUT').length,1);h.unmount();
});
test('candidate preference in flight is single-submit and late reply cannot populate a different Company view',async()=>{
 const wait=deferred(),f=fixture({restored:true,waitPreference:wait}),runtime={status:'ready',companyId:'company-A'},h=scene(new Map(),runtime);await h.settle();modelSelect(h).props.onChange({target:{value:'fake.flash'}});await h.settle();const click=chooseButton(h).props.onClick,request=click();await click();runtime.companyId='company-B';await h.settle();wait.resolve();await request;await h.settle();assert.equal(h.storage.has('curis.v1.conversationModel'),false);assert.ok(chooseButton(h));assert.doesNotMatch(text(h.tree),/当前租户默认/);assert.equal(f.calls.filter(c=>c.method==='PUT').length,1);assert.equal(f.providerCalls().length,0);h.unmount();
});

test('candidate return after selecting a default reads metadata only, without automatic recovery Provider calls',async()=>{
 const f=fixture(),storage=new Map(),h=scene(storage);await h.settle();h.enter();await button(h).props.onClick();await h.settle();modelSelect(h).props.onChange({target:{value:'fake.flash'}});await h.settle();await chooseButton(h).props.onClick();await h.settle();h.unmount();const restored=scene(storage);await restored.settle();assert.ok(chooseButton(restored));assert.match(text(restored.tree),/未重新测试连接/);assert.equal(f.providerCalls().length,1);assert.equal(f.calls.filter(c=>c.path.endsWith('/recover')).length,0);assert.equal(f.storeCalls().length,1);restored.unmount();
});

test('candidate rereads changed credential marker before default PUT rather than trusting stale rendered choices',async()=>{
 const f=fixture(),h=scene();await h.settle();h.enter();await button(h).props.onClick();await h.settle();modelSelect(h).props.onChange({target:{value:'fake.flash'}});await h.settle();const key=`curis.modelCredentialAttempt:${JSON.stringify([api.TENANT_ID,'deepseek'])}`,record=JSON.parse(h.storage.get(key));h.storage.set(key,JSON.stringify({...record,state:'PENDING'}));await chooseButton(h).props.onClick();await h.settle();assert.equal(chooseButton(h),undefined);assert.equal(f.calls.filter(c=>c.method==='PUT'&&c.path.endsWith('/model-preference')).length,0);assert.equal(f.providerCalls().length,1);h.unmount();
});

test('QA regression: immutable idle to loading to ready loads eligible choices once ready, with no connect',async()=>{
 const f=fixture({restored:true}),h=scene(new Map(),{status:'idle',companyId:''});await h.settle();assert.equal(f.calls.length,0);h.setRuntime({status:'loading',companyId:''});await h.settle();assert.equal(f.calls.length,0);h.setRuntime({status:'ready',companyId:'company-A'});await h.settle();assert.ok(chooseButton(h));assert.ok(modelSelect(h));assert.equal(f.calls.filter(c=>c.path.endsWith('/model-preference')).length,1);assert.equal(f.calls.filter(c=>c.method!=='GET').length,0);h.unmount();
});
test('QA regression: late old-company preference response cannot erase new-company choices',async()=>{
 const wait=deferred(),f=fixture({restored:true,waitFirstPreference:wait,firstAvailable:[]}),h=scene(new Map(),{status:'ready',companyId:'company-A'});await h.settle();assert.equal(chooseButton(h),undefined);h.setRuntime({status:'ready',companyId:'company-B'});await h.settle();assert.ok(chooseButton(h));wait.resolve();await h.settle();assert.ok(chooseButton(h));assert.ok(modelSelect(h));assert.equal(f.calls.filter(c=>c.method!=='GET').length,0);h.unmount();
});
test('QA regression: same-company loading round invalidates earlier metadata generation',async()=>{
 const wait=deferred(),f=fixture({restored:true,waitFirstPreference:wait,firstAvailable:[]}),h=scene(new Map(),{status:'ready',companyId:'company-A'});await h.settle();h.setRuntime({status:'loading',companyId:'company-A'});await h.settle();assert.equal(chooseButton(h),undefined);h.setRuntime({status:'ready',companyId:'company-A'});await h.settle();assert.ok(chooseButton(h));wait.resolve();await h.settle();assert.ok(chooseButton(h));assert.equal(f.calls.filter(c=>c.method!=='GET').length,0);h.unmount();
});
test('QA regression: late old-company provider failure cannot overwrite current-company success',async()=>{
 const wait=deferred(),f=fixture({restored:true,waitFirstProviders:wait,failFirstProviders:true}),h=scene(new Map(),{status:'ready',companyId:'company-A'});await h.settle();h.setRuntime({status:'ready',companyId:'company-B'});await h.settle();assert.ok(chooseButton(h));wait.resolve();await h.settle();assert.ok(chooseButton(h));assert.doesNotMatch(text(h.tree),/OLD_COMPANY_PROVIDER_METADATA_FAILURE/);assert.equal(f.calls.filter(c=>c.method!=='GET').length,0);h.unmount();
});

test('QA regression: same-company older metadata cannot overwrite newer post-connect choices',async()=>{
 const wait=deferred(),f=fixture({restored:true,rows:[metadata],waitFirstPreference:wait,waitPreferenceReadNumber:2,firstAvailable:[]}),h=scene(new Map(),{status:'ready',companyId:'company-A'});await h.settle();assert.ok(chooseButton(h));h.setRuntime({status:'loading',companyId:'company-A'});await h.settle();h.setRuntime({status:'ready',companyId:'company-A'});await h.settle();assert.equal(chooseButton(h),undefined);await button(h).props.onClick();await h.settle();assert.equal(f.providerCalls().length,1,JSON.stringify(f.calls.map(c=>[c.path,c.method])));assert.ok(chooseButton(h));assert.ok(modelSelect(h));assert.equal(f.providerCalls().length,1);wait.resolve();await h.settle();assert.ok(chooseButton(h));assert.ok(modelSelect(h));assert.equal(f.providerCalls().length,1);noSecret(h);h.unmount();
});

test('UX revisit selects exact saved default instead of the first eligible model with no write',async()=>{
 const f=fixture({restored:true,preference:{model_key:'fake.flash',model_name:'deepseek-flash'}}),h=scene();await h.settle();assert.equal(modelSelect(h).props.value,'fake.flash');assert.match(text(h.tree),/已保存配置 · 本次未验证/);assert.doesNotMatch(text(h.tree),/先为 Curis|本次连接验证通过/);assert.equal(f.calls.filter(x=>x.method!=='GET').length,0);h.unmount();
});
for(const [name,preference,available] of [['missing',null,undefined],['foreign',{model_key:'other.flash',model_name:'deepseek-flash'},undefined],['duplicate',{model_key:'fake.flash'},[...eligibleModels,...eligibleModels.filter(x=>x.model_key==='fake.flash')]]])test('UX '+name+' default requires explicit choice without guessing',async()=>{
 const f=fixture({restored:true,preference,available}),h=scene();await h.settle();assert.equal(modelSelect(h).props.value,'');assert.equal(chooseButton(h).props.disabled,true);await chooseButton(h).props.onClick();assert.equal(f.calls.filter(x=>x.method!=='GET').length,0);h.unmount();
});
test('UX user choice wins over saved default and only explicit default action writes',async()=>{
 const f=fixture({restored:true,preference:{model_key:'fake.flash',model_name:'deepseek-flash'}}),h=scene();await h.settle();modelSelect(h).props.onChange({target:{value:'fake.pro'}});await h.settle();assert.equal(modelSelect(h).props.value,'fake.pro');assert.equal(f.calls.filter(x=>x.method!=='GET').length,0);await chooseButton(h).props.onClick();await h.settle();assert.equal(f.calls.filter(x=>x.method==='PUT').length,1);assert.equal(f.calls.find(x=>x.method==='PUT').body.model_key,'fake.pro');assert.equal(f.providerCalls().length,0);h.unmount();
});
test('UX first connection never mistakes programmatic first result for an explicit selection',async()=>{
 const f=fixture(),h=scene();await h.settle();h.enter();await button(h).props.onClick();await h.settle();assert.equal(modelSelect(h).props.value,'');assert.ok(chooseButton(h).props.disabled);assert.equal(f.providerCalls().length,1);assert.equal(f.calls.filter(x=>x.path.endsWith('/model-preference')&&x.method==='PUT').length,0);h.unmount();
});
test('UX genuine failed validation keeps failure visible, never a successful badge',async()=>{
 const f=fixture({restored:true,rows:[metadata],providerFail:true}),h=scene();await h.settle();await button(h).props.onClick();await h.settle();assert.match(text(h.tree),/本次连接验证未通过/);assert.match(text(h.tree),/模型尚未验证/);assert.doesNotMatch(text(h.tree),/本次连接验证通过/);assert.equal(f.providerCalls().length,1);h.unmount();
});
