import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

const read = (path) => readFileSync(path==="components/v1/AppEntry.js"&&process.env.CURIS_TEST_APP_ENTRY_PREIMAGE?process.env.CURIS_TEST_APP_ENTRY_PREIMAGE:new URL(`../${path}`, import.meta.url), "utf8");

test("App Entry keeps skip separate from Company creation", () => {
  const source = read("components/v1/AppEntry.js");
  assert.match(source, /welcome_dismissed: true/);
  assert.match(source, /materializeFoundingCompany/);
  assert.match(source, /先看看 Curis/);
  assert.doesNotMatch(source.match(/const skip[\s\S]*?const createCompany/)?.[0] || "", /materializeFoundingCompany/);
});

test("shared conversation exposes the accepted model and composer seams", () => {
  const source = read("components/v1/SharedConversation.js");
  assert.match(source, /当前对话模型/);
  assert.match(source, /参考资料/);
  assert.match(source, /尚未连接可用模型/);
  assert.match(source, /recoverAIProvider/);
  assert.match(source, /modelStillAvailable/);
  assert.match(source, /recoveredModel\.capability_id/);
});

test("packaged credentials revalidate without browser secret persistence", () => {
  const management = read("components/v1/ModelManagement.js");
  const api = read("lib/v1FrontendApi.js");
  assert.match(management, /macOS Keychain/);
  assert.match(management, /recoverDefault: true/);
  assert.match(api, /ai-capabilities\/providers\/\$\{encodeURIComponent\(providerId\)\}\/recover/);
  assert.match(management, /setModelPreference\(model\.capability_id\)/);
  assert.match(management, /\[selectedProviderId, selectedBaseUrl\]/);
  assert.doesNotMatch(management, /localStorage|indexedDB|只用于当前 Curis 进程/);
});

test("CEO Desk consumes canonical attention and business references", () => {
  const source = read("components/v1/CeoDeskOperating.js");
  const api = read("lib/v1FrontendApi.js");
  assert.match(source, /getCompanyAttention/);
  assert.match(source, /getCanonicalBusinesses/);
  assert.match(source, /createBusinessFromFoundingRun/);
  assert.match(source, /workspaceEntryHref/);
  assert.match(source, /getCEOAssistantConversation/);
  assert.match(source, /sendCEOAssistantMessage/);
  assert.match(api, /assistant\/conversation/);
});

test("accepted seven-area navigation is the only primary list", () => {
  const source = read("components/v1/V1Sidebar.js");
  for (const label of ["CEO 工作台", "业务空间", "组织中心", "人才与能力", "经营洞察", "资料库", "会议"]) assert.match(source, new RegExp(label));
  assert.doesNotMatch(source, /旧任务流水线/);
});


test("actual setup and sidebar render the same persisted preset colors across theme accents", async()=>{
  const {createRequire}=await import('node:module'),vm=await import('node:vm'),presets=await import('../lib/avatarPresets.mjs');
  const require=createRequire(import.meta.url),React=require('react'),swc=require('next/dist/build/swc');await swc.loadBindings();
  const compile=async(file,exposed)=>{const source=read(file);const {code}=await swc.transform(source,{filename:file,isModule:true,jsc:{parser:{syntax:'ecmascript',jsx:true},transform:{react:{runtime:'automatic'}}},module:{type:'commonjs'}});const m={exports:{}};vm.runInNewContext(code+';exports.exposed='+exposed+';',{module:m,exports:m.exports,require:name=>name==='react'?{...React,useState:v=>[v,()=>{}],useRef:v=>({current:v}),useEffect(){},useLayoutEffect(){}}:name==='react/jsx-runtime'?require(name):name.endsWith('avatarPresets.mjs')?presets:{}});return m.exports.exposed;};
  const Avatar=await compile('components/v1/V1Sidebar.js','Avatar');
  const Setup=await compile('components/v1/AppEntry.js','Setup');
  const nodes=(n,p)=>!n||typeof n!=='object'?[]:Array.isArray(n)?n.flatMap(v=>nodes(v,p)):[...(p(n)?[n]:[]),...nodes(n.props?.children,p)];
  for(const [id,label,bg,fg] of presets.AVATAR_PRESETS){const avatar=Avatar({presentation:{avatar_ref:'preset:'+id,display_name:'用户'}});assert.equal(avatar.props.style.backgroundColor,bg);assert.equal(avatar.props.style.color,fg);assert.equal(avatar.props.children,label);const setup=Setup({value:{avatar_ref:'preset:'+id,display_name:'用户',company_name:'公司'},setValue(){},onSubmit(){},onBack(){},busy:false});const swatch=nodes(setup,n=>n.props?.style?.background===bg)[0];assert.ok(swatch);assert.equal(swatch.props.style.color,fg);}
});

test('committed Setup busy/recovering invalidates asynchronous avatar reads and resumes safely',async()=>{
 const {createRequire}=await import('node:module'),vm=await import('node:vm'),presets=await import('../lib/avatarPresets.mjs');const require=createRequire(import.meta.url),React=require('react'),swc=require('next/dist/build/swc');await swc.loadBindings();
 const {code}=await swc.transform(read('components/v1/AppEntry.js'),{filename:'AppEntry.js',isModule:true,jsc:{parser:{syntax:'ecmascript',jsx:true},transform:{react:{runtime:'automatic'}}},module:{type:'commonjs'}});
 const slots=[],effects=[],readers=[];let cursor=0;const same=(a,b)=>a&&b&&a.length===b.length&&a.every((v,i)=>Object.is(v,b[i]));const hooks={useState(initial){const i=cursor++;slots[i]||={value:initial};return[slots[i].value,v=>slots[i].value=typeof v==='function'?v(slots[i].value):v];},useRef(initial){const i=cursor++;return slots[i]||={current:initial};},useEffect(fn,deps){const i=cursor++;if(!slots[i]||!same(slots[i].deps,deps)){const old=slots[i];slots[i]={deps};effects.push(()=>{old?.cleanup?.();slots[i].cleanup=fn();});}}};hooks.useLayoutEffect=hooks.useEffect;
 class Reader{constructor(){readers.push(this);this.result='data:image/png;base64,YQ==';this.aborted=false;}abort(){this.aborted=true;}readAsDataURL(){}}
 const m={exports:{}};vm.runInNewContext(code+';exports.Setup=Setup;',{module:m,exports:m.exports,FileReader:Reader,require:name=>name==='react'?{...React,...hooks}:name==='react/jsx-runtime'?require(name):name.endsWith('avatarPresets.mjs')?presets:{}});
 let value={display_name:'用户',company_name:'公司',avatar_ref:'preset:green'},writes=0;const props={value,setValue(next){writes++;value=typeof next==='function'?next(value):next;props.value=value;},onSubmit(){},onBack(){},busy:false,recovering:false};const render=()=>{cursor=0;return m.exports.Setup(props);};const commit=()=>{render();for(const effect of effects.splice(0))effect();return render();};const nodes=(n,p)=>!n||typeof n!=='object'?[]:Array.isArray(n)?n.flatMap(v=>nodes(v,p)):[...(p(n)?[n]:[]),...nodes(n.props?.children,p)];const input=()=>nodes(render(),n=>n.type==='input'&&n.props.type==='file')[0];commit();const oldChoose=input().props.onChange;oldChoose({target:{files:[{name:'a.png',type:'image/png',size:1}],value:'file'}});assert.equal(readers.length,1);
 props.busy=true;render();readers[0].onload();assert.equal(writes,1,'uncommitted render must not publish a new lock'); // This value is then replaced by the committed lock before another read.
 props.busy=false;commit();oldChoose({target:{files:[{name:'b.png',type:'image/png',size:1}],value:'file'}});const before=writes;props.busy=true;commit();const stale=readers.at(-1);assert.equal(stale.aborted,true);stale.onload();assert.equal(writes,before);oldChoose({target:{files:[{type:'image/png',size:1}],value:'file'}});assert.equal(readers.length,2);
 props.busy=false;commit();oldChoose({target:{files:[{type:'image/png',size:1}],value:'file'}});const recoveringRead=readers.at(-1);props.recovering=true;commit();assert.equal(recoveringRead.aborted,true);recoveringRead.onload();assert.equal(writes,before);props.recovering=false;commit();stale.onload();recoveringRead.onload();assert.equal(writes,before,'unlock never revives an invalidated read');oldChoose({target:{files:[{type:'image/png',size:1}],value:'file'}});assert.equal(readers.length,4);readers.at(-1).onload();assert.equal(writes,before+1);commit();for(const slot of slots)slot?.cleanup?.();readers.at(-1).onload();assert.equal(writes,before+1,'unmounted completion is ignored');
});
