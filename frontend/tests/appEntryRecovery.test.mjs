import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import vm from "node:vm";
const require=createRequire(import.meta.url),React=require('react'),swc=require('next/dist/build/swc');
await swc.loadBindings();
const {code}=await swc.transform(readFileSync(new URL('../components/v1/AppEntry.js',import.meta.url),'utf8')+'\nexport {Setup};',{filename:'AppEntry.js',isModule:true,jsc:{parser:{syntax:'ecmascript',jsx:true},transform:{react:{runtime:'automatic'}}},module:{type:'commonjs'}});
function load(api={}) {
 const slots=[],effects=[],cleanups=[];let cursor=0;const hooks={useState(v){const i=cursor++;slots[i]??={value:typeof v==='function'?v():v};return[slots[i].value,x=>slots[i].value=typeof x==='function'?x(slots[i].value):x];},useRef(v){const i=cursor++;return slots[i]??={current:v};},useEffect(fn,deps){const i=cursor++;if(!slots[i]||deps.some((x,j)=>x!==slots[i][j])){slots[i]=deps;effects.push(()=>{const cleanup=fn();if(typeof cleanup==='function')cleanups.push(cleanup);});}}};
 const ShellStub=()=>null;
 const module={exports:{}},store=api.storage || new Map();
 vm.runInNewContext(code,{module,exports:module.exports,crypto:globalThis.crypto,sessionStorage:{getItem:k=>store.get(k)||null,setItem:(k,v)=>store.set(k,v),removeItem:k=>store.delete(k)},FileReader:api.FileReader,window:{location:{replace(){}}},require:p=>p==='react'?{...React,...hooks}:p==='react/jsx-runtime'?require(p):p.endsWith('/api.js')?{CEO_ID:'selfuse-ceo'}:p.includes('RuntimeProvider')?{useRuntime:()=>api.runtime||({status:'ready',snapshot:null,refresh:async()=>{}})}:p.includes('v1FrontendApi')?{getV1Presentation:async()=>({}),...api}:p.includes('runtimeApi')?api:p.endsWith('/TerraShell.js')?{default:ShellStub,__esModule:true}:{default:()=>null,__esModule:true}});
 return {exports:module.exports,store,shell:ShellStub,render(component=module.exports.default,props={}){cursor=0;const tree=component(props);while(effects.length)effects.shift()();return tree;},unmount(){cleanups.forEach(fn=>fn());}};
}
const complete=load().exports.completeCompanySetup;
function fixture() {
 let state='ARRIVED',runCalls=0,companies=0,drop='';const moves=[];
 const api={saveV1Presentation:async()=>{},createFoundingRun:async()=>{runCalls++;if(drop==='create'){drop='';throw Error('lost run response');}return{entity_id:'run'};},getFoundingRun:async()=>({entity_id:'run',owner_ref:'selfuse-ceo',lifecycle_status:state,company_id:state==='COMPANY_CREATED'?'company-stable':null}),transitionRuntimeEntity:async(id,p)=>{moves.push(p.target);state=p.target;if(drop===p.target){drop='';throw Error('lost transition response');}},materializeFoundingCompany:async(id,p)=>{assert.equal(id,'run');assert.equal(p.company_id,'company-stable');assert.equal(p.name,'原公司');state='COMPANY_CREATED';companies++;if(drop==='materialize'){drop='';throw Error('lost company response');}return{company:p};},getRuntimeCompany:async()=>({company:{company_id:'company-stable',name:'原公司'}})};
 return {api,operation:{companyId:'company-stable',runId:'',values:{display_name:'CEO',avatar_ref:'',company_name:'原公司'}},drop(x){drop=x;},stats:()=>({runCalls,companies,moves})};
}
for(const failure of ['CLARIFYING','materialize'])test(`lost ${failure} queries same run and stable Company without duplicates`,async()=>{
 const f=fixture();let saved;f.drop(failure);await assert.rejects(complete(f.operation,x=>saved=JSON.parse(JSON.stringify(x)),f.api));assert.equal(saved.runId,'run');
 await complete(saved,()=>{},f.api);assert.equal(f.stats().runCalls,1);assert.equal(f.stats().companies,1);assert.equal(new Set(f.stats().moves).size,4);
});
test('lost initial run permits empty-run retry but one Company, no invented request field',async()=>{
 const f=fixture();f.drop('create');await assert.rejects(complete(f.operation,()=>{},f.api));assert.equal(f.operation.runId,'');await complete(f.operation,()=>{},f.api);assert.equal(f.stats().runCalls,2);assert.equal(f.stats().companies,1);
});
test('unreadable same run prevents another transition or Company',async()=>{
 const f=fixture();f.operation.runId='run';f.api.getFoundingRun=async()=>{throw Error('offline');};await assert.rejects(complete(f.operation,()=>{},f.api));assert.equal(f.stats().moves.length,0);assert.equal(f.stats().companies,0);
});
test('skip refusal releases actual synchronous gate and shows error',async()=>{
 let writes=0;const h=load({saveV1Presentation:async()=>{writes++;throw Error('save refused');}});h.render();await new Promise(setImmediate);let tree=h.render();await tree.props.onSkip();tree=h.render();assert.equal(tree.props.busy,false);assert.match(tree.props.error,/save refused/);await tree.props.onSkip();assert.equal(writes,2);
});

test('corrupt stored operation fails closed instead of offering another Company',async()=>{
 const storage=new Map([['curis.company-setup.v1','{broken']]);const h=load({storage});h.render();const tree=h.render();const flatten=v=>v==null?'':typeof v==='object'?(Array.isArray(v)?v.map(flatten).join(''):flatten(v.props?.children)):String(v);assert.match(flatten(tree),/原建公司记录暂不可读取/);assert.equal(tree.props.onCreate,undefined);
});
test('actual skip synchronous gate rejects a second click before React rerenders',async()=>{
 let finish,calls=0;const gate=new Promise(resolve=>finish=resolve),h=load({saveV1Presentation:()=>{calls++;return gate;}});h.render();await new Promise(setImmediate);const tree=h.render(),first=tree.props.onSkip(),second=tree.props.onSkip();assert.equal(calls,1);finish();await Promise.all([first,second]);assert.equal(h.render().props.onSkip,undefined);
});

const flatten=v=>v==null?'':typeof v==='object'?(Array.isArray(v)?v.map(flatten).join(''):flatten(v.props?.children)):String(v);
function nodes(tree,predicate){const result=[];function visit(v){if(!v||typeof v!=='object')return;if(Array.isArray(v))return v.forEach(visit);if(predicate(v))result.push(v);visit(v.props?.children);}visit(tree);return result;}
function uiApi(){
 let state='ARRIVED',company=null;const calls={profiles:[],runs:0,companies:[],refuse:false,unknown:false};
 const api={saveV1Presentation:async value=>{calls.profiles.push(value);if(calls.refuse){calls.refuse=false;throw Object.assign(Error('known profile validation refused'),{status:422});}},createFoundingRun:async()=>{calls.runs++;if(calls.unknown){calls.unknown=false;throw Error('run response unknown');}return{entity_id:'ui-run'};},getFoundingRun:async()=>({entity_id:'ui-run',owner_ref:'selfuse-ceo',lifecycle_status:state,company_id:company?.company_id}),transitionRuntimeEntity:async(id,p)=>{state=p.target;},materializeFoundingCompany:async(id,p)=>{calls.companies.push(p);company={company_id:p.company_id,name:p.name};state='COMPANY_CREATED';return{company};},getRuntimeCompany:async()=>({company})};
 return{api,calls};
}
async function setupParent(api,avatar='preset:iris'){
 const h=load(api);h.render();await new Promise(setImmediate);h.render().props.onCreate();let tree=h.render();tree.props.setValue({display_name:'CEO',company_name:'原公司',avatar_ref:avatar});h.render();return h;
}
function readerClass(){
 const readers=[];
 class Reader{constructor(){readers.push(this);}readAsDataURL(file){this.file=file;}abort(){this.aborted=true;}async finish(result){this.result=result??`data:${this.file.type};base64,${Buffer.from(await this.file.arrayBuffer()).toString('base64')}`;this.onload?.();}}
 return{Reader,readers};
}
// Valid 1x1 PNG plus a legal ancillary tEXt chunk reproduces the real 203188-byte boundary.
function pngOfSize(size){
 const base=Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Wl6n1kAAAAASUVORK5CYII=','base64');
 const data=Buffer.alloc(size-base.length-12,120);data.write('Note\0');const type=Buffer.from('tEXt');let crc=0xffffffff;for(const b of Buffer.concat([type,data])){crc^=b;for(let j=0;j<8;j++)crc=(crc>>>1)^((crc&1)?0xedb88320:0);}const chunk=Buffer.alloc(data.length+12);chunk.writeUInt32BE(data.length);type.copy(chunk,4);data.copy(chunk,8);chunk.writeUInt32BE((crc^0xffffffff)>>>0,chunk.length-4);return Buffer.concat([base.subarray(0,-12),chunk,base.subarray(-12)]);
}
test('actual Setup rejects valid 203188-byte PNG visibly before checkpoint, preserves avatar and allows replacement',async()=>{
 const {api,calls}=uiApi(),parent=await setupParent(api),{Reader,readers}=readerClass(),child=load({FileReader:Reader});
 let props=parent.render().props,tree=child.render(child.exports.Setup,props);const file=new File([pngOfSize(203188)],'valid-large.png',{type:'image/png'});assert.equal(file.size,203188);
 nodes(tree,n=>n.type==='input'&&n.props.type==='file')[0].props.onChange({target:{files:[file],value:'selected'}});tree=child.render(child.exports.Setup,props);assert.match(flatten(tree),/194KB/);assert.equal(readers.length,0);assert.equal(calls.profiles.length,0);assert.equal(parent.store.size,0);assert.equal(parent.render().props.value.avatar_ref,'preset:iris');
 nodes(tree,n=>n.type==='button'&&flatten(n)==='移除头像')[0].props.onClick();assert.equal(parent.render().props.value.avatar_ref,'');
 await parent.render().props.onSubmit({preventDefault(){}});assert.equal(calls.companies.length,1);assert.equal(calls.profiles[0].avatar_ref,'');parent.unmount();child.unmount();
});
test('actual FileReader checks encoded length, keeps old avatar, then accepts a small PNG',async()=>{
 const {api,calls}=uiApi(),parent=await setupParent(api),{Reader,readers}=readerClass(),child=load({FileReader:Reader});let props=parent.render().props;const render=()=>child.render(child.exports.Setup,props);
 const small=new File([pngOfSize(1024)],'small.png',{type:'image/png'});nodes(render(),n=>n.type==='input'&&n.props.type==='file')[0].props.onChange({target:{files:[small],value:'small'}});assert.equal(nodes(render(),n=>typeof n.type==='function'&&n.type.name==='PrimaryButton')[0].props.disabled,true);
 await readers[0].finish('data:image/png;base64,'+'A'.repeat(270920));assert.match(flatten(render()),/头像过大/);assert.equal(parent.render().props.value.avatar_ref,'preset:iris');
 nodes(render(),n=>n.type==='input'&&n.props.type==='file')[0].props.onChange({target:{files:[small],value:'small'}});await readers[1].finish();props=parent.render().props;render();assert.ok(props.value.avatar_ref.startsWith('data:image/png;base64,'));assert.ok(props.value.avatar_ref.length<260000);
 await props.onSubmit({preventDefault(){}});assert.equal(calls.companies.length,1);assert.ok(calls.profiles[0].avatar_ref.startsWith('data:image/png;base64,'));parent.unmount();child.unmount();
});
test('actual parent validates name before snapshot and releases known pre-run422 without dropping avatar',async()=>{
 const {api,calls}=uiApi(),parent=await setupParent(api);let props=parent.render().props;props.setValue({...props.value,display_name:'CEO\ninvalid'});await parent.render().props.onSubmit({preventDefault(){}});props=parent.render().props;assert.equal(props.recovering,false);assert.equal(calls.profiles.length,0);assert.equal(parent.store.size,0);assert.match(props.error,/称呼/);
 props.setValue({...props.value,display_name:'合法称呼'});calls.refuse=true;await parent.render().props.onSubmit({preventDefault(){}});props=parent.render().props;assert.equal(props.recovering,false);assert.equal(calls.runs,0);assert.equal(parent.store.size,0);assert.equal(props.value.avatar_ref,'preset:iris');
 props.setValue({...props.value,avatar_ref:'preset:mint'});await parent.render().props.onSubmit({preventDefault(){}});assert.equal(calls.companies.length,1);assert.equal(calls.profiles.at(-1).avatar_ref,'preset:mint');parent.unmount();
});
test('actual parent keeps stable snapshot and Company ID after genuinely unknown run response',async()=>{
 const {api,calls}=uiApi(),parent=await setupParent(api);calls.unknown=true;await parent.render().props.onSubmit({preventDefault(){}});let props=parent.render().props;assert.equal(props.recovering,true);const original=JSON.parse(parent.store.get('curis.company-setup.v1'));assert.equal(original.runRequested,true);
 props.setValue({...props.value,company_name:'不应改写',avatar_ref:'preset:amber'});props=parent.render().props;assert.equal(props.value.company_name,'原公司');assert.equal(props.value.avatar_ref,'preset:iris');await props.onSubmit({preventDefault(){}});assert.equal(calls.companies.length,1);assert.equal(calls.companies[0].company_id,original.companyId);assert.equal(calls.companies[0].name,'原公司');parent.unmount();
});
test('late FileReader cannot replace a preset or submitted snapshot even before the child rerenders',async()=>{
 const {api,calls}=uiApi(),parent=await setupParent(api),{Reader,readers}=readerClass(),child=load({FileReader:Reader});let props=parent.render().props;const tree=child.render(child.exports.Setup,props),file=new File([pngOfSize(1024)],'late.png',{type:'image/png'});
 nodes(tree,n=>n.type==='input'&&n.props.type==='file')[0].props.onChange({target:{files:[file],value:'late'}});nodes(tree,n=>n.type==='button'&&n.props['aria-label']==='选择头像 mint')[0].props.onClick();props=parent.render().props;
 const submitting=props.onSubmit({preventDefault(){}});await readers[0].finish();await submitting;assert.equal(calls.profiles[0].avatar_ref,'preset:mint');assert.equal(calls.companies.length,1);parent.unmount();child.unmount();
});

test('legacy oversized saved pre-run snapshot becomes editable without changing an uncertain run',async()=>{
 const {api,calls}=uiApi();const saved={companyId:'old-local-id',runId:'',values:{display_name:'CEO',company_name:'原公司',avatar_ref:'data:image/png;base64,'+'A'.repeat(270920)}};const storage=new Map([['curis.company-setup.v1',JSON.stringify(saved)]]);const parent=load({...api,storage});parent.render();let props=parent.render().props;assert.equal(props.recovering,true);await props.onSubmit({preventDefault(){}});props=parent.render().props;assert.equal(props.recovering,false);assert.equal(calls.runs,0);assert.equal(calls.profiles.length,0);assert.equal(parent.store.size,0);assert.equal(props.value.avatar_ref,saved.values.avatar_ref);props.setValue({...props.value,avatar_ref:'preset:iris'});await parent.render().props.onSubmit({preventDefault(){}});assert.equal(calls.companies.length,1);parent.unmount();
});

test('actual avatar chooser rejects empty or unsupported files without changing previous choice',async()=>{
 const {api,calls}=uiApi(),parent=await setupParent(api),{Reader,readers}=readerClass(),child=load({FileReader:Reader});const props=parent.render().props;for(const file of [new File([],'empty.png',{type:'image/png'}),new File(['text'],'wrong.txt',{type:'text/plain'})]){const tree=child.render(child.exports.Setup,props);nodes(tree,n=>n.type==='input'&&n.props.type==='file')[0].props.onChange({target:{files:[file],value:'selected'}});assert.match(flatten(child.render(child.exports.Setup,props)),/PNG、JPEG/);assert.equal(parent.render().props.value.avatar_ref,'preset:iris');}assert.equal(readers.length,0);assert.equal(calls.profiles.length,0);parent.unmount();child.unmount();
});

test('empty Company after Skip or saved dismissal uses the shared shell and keeps manual setup entry',async()=>{
 for(const dismissed of [false,true]){
  const {api,calls}=uiApi(),h=load({...api,runtime:{status:'empty',companyId:'',snapshot:null,refresh:async()=>{}},getV1Presentation:async()=>({welcome_dismissed:dismissed})});
  h.render();await new Promise(setImmediate);
  if(!dismissed)await h.render().props.onSkip();
  const empty=h.render(),shell=empty.type(empty.props);
  assert.equal(shell.type,h.shell);assert.equal(shell.props.topCrumb,'CEO 工作台');assert.equal(shell.props.assistantContext.page,'ceo-office');assert.equal(shell.props.assistantContext.company_id,undefined);
  assert.match(flatten(shell),/这里还没有公司/);assert.equal(nodes(shell,n=>n.type==='main').length,0);
  const create=nodes(shell,n=>typeof n.type==='function'&&n.type.name==='PrimaryButton'&&flatten(n)==='创建我的 AI 公司')[0];assert.ok(create);create.props.onClick();
  const setup=h.render();assert.equal(setup.type.name,'Setup');assert.equal(setup.props.recovering,false);assert.equal(calls.runs,0);assert.equal(calls.companies.length,0);assert.equal(calls.profiles.length,dismissed?0:1);assert.equal(h.store.size,0);h.unmount();
 }
});
