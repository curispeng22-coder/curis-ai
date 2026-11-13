// Actual components; all external APIs are fixture-only. No App or database.
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
import vm from 'node:vm';
import path from 'node:path';
const business = await (async () => {
const require=createRequire(import.meta.url),React=require('react'),swc=require('next/dist/build/swc');
const root=fileURLToPath(new URL("../..", import.meta.url)); await swc.loadBindings();
const files={catalog:'components/v1/BusinessCatalogSurface.js',creator:'components/v1/CeoDeskOperating.js',shared:'components/v1/SharedConversation.js',page:'app/ceo-office/business/page.js',writing:'components/writing/WritingWorkspace.js',writingApi:'lib/writingApi.js',writingState:'lib/writingState.mjs',bookState:'lib/writingBookState.mjs',musicState:'lib/musicState.mjs'};
const code={};for(const [k,p] of Object.entries(files)){let s=readFileSync(path.join(root,'frontend',p),'utf8');if(k==='page')s=s.replace('function BusinessSurface()','export function BusinessSurface()');code[k]=(await swc.transform(s,{filename:p,isModule:true,jsc:{parser:{syntax:'ecmascript',jsx:true},transform:{react:{runtime:'automatic'}}},module:{type:'commonjs'}})).code;}
const tick=()=>new Promise(r=>setImmediate(r));
const writingId='com.curis.local.writing-authoring';
const def=(id=writingId)=>({package_id:id,name:'本地写作工作空间',version:'v1',digest:'digest',initial_team_contract:{sha256:'contract',packageId:id,packageVersion:'v1',packageDigest:'digest',displayName:'章节作者'}});
const text=n=>n==null||typeof n==='boolean'?'':typeof n!=='object'?String(n):Array.isArray(n)?n.map(text).join(''):text(n.props?.children);
function nodes(n,p){if(!n||typeof n!=='object')return[];if(Array.isArray(n))return n.flatMap(x=>nodes(x,p));return[...(p(n)?[n]:[]),...nodes(n.props?.children,p)];}
function scene(options={}){
 let current,pending=[],frameId=0,query=options.query||'',company='A',lastRaw,lastTree;const frames=new Map(),modules={},storage=new Map(Object.entries(options.storage||{}));
 const counts={models:0,recover:0,runs:0,saves:0,confirms:0,objects:0};let saved,run={entity_id:'R',owner_ref:'CEO',company_id:'A',lifecycle_status:'PROPOSED'};
 const definition=options.definition||def();const definitions=options.definitions||{definitions:[definition],departments:[{id:'D',name:'业务部'}]};
 const same=(a,b)=>a&&b&&a.length===b.length&&a.every((x,i)=>Object.is(x,b[i]));
 const hooks={...React,useState(initial){const f=current,i=f.i++;if(!(i in f.slots))f.slots[i]={value:typeof initial==='function'?initial():initial};return[f.slots[i].value,v=>{f.slots[i].value=typeof v==='function'?v(f.slots[i].value):v;}];},useRef(initial){const f=current,i=f.i++;return f.slots[i]||=( {current:initial});},useEffect(fn,deps){const f=current,i=f.i++,old=f.slots[i];if(!old||!same(old.deps,deps)){f.slots[i]={deps};pending.push(()=>{old?.cleanup?.();f.slots[i].cleanup=fn();});}},useMemo(fn,deps){const f=current,i=f.i++;if(!f.slots[i]||!same(f.slots[i].deps,deps))f.slots[i]={deps,value:fn()};return f.slots[i].value;},useCallback(fn,deps){return hooks.useMemo(()=>fn,deps);},useLayoutEffect(fn,deps){hooks.useEffect(fn,deps);},useContext(){return()=>{};},useId(){return'fixture';}};
 const api={CEO_ID:'CEO',getBusinessDefinitions:async(companyId)=>options.definitionByCompany ? await options.definitionByCompany(companyId) : options.definitionPromise?await options.definitionPromise:definitions,getCanonicalBusinesses:async()=>({businesses:[]}),getOrganizationProjection:async()=>({company:{company_id:company},businesses:[],departmentAssignments:[],employees:[],departments:[]}),createFoundingRun:async()=>{counts.runs++;return run;},transitionRuntimeEntity:async(_id,v)=>{run={...run,lifecycle_status:v.target};return run;},saveBusinessDraft:async(_id,v)=>{counts.saves++;saved={...v,proposal_sha256:'sha',snapshot:{company_id:company,definition}};run={...run,data:{v1Proposal:saved}};return run;},createBusinessFromFoundingRun:async()=>{counts.confirms++;if(options.createError)throw Object.assign(new Error("明确失败"),{status:409});if(options.createPromise)return await options.createPromise;return result();},getFoundingRun:async()=>options.restoredRun||run,getBusinessDraft:async()=>({founding_run_id:'R',proposal:options.restoredProposal||saved}),getBusinessCreationResult:async()=>options.resultStatus==='UNKNOWN'?{founding_run:options.restoredRun||run,activation:{status:'UNKNOWN'}}:result(),workspaceOfficeHref:()=>'/existing-workspace',workspaceEntryHref:()=>'/existing-workspace',getEnabledModels:async()=>{counts.models++;return{models:[]};},getModelPreference:async()=>({preference:null,available_models:[]}),recoverAIProvider:async()=>{counts.recover++;throw Error('provider recovery forbidden');},computerAccessView:()=>({title:'无电脑操作',label:'不可用'}),getAssistantIdentity:async()=>({}),conversationError:e=>e.message,createInstalledWorkspaceObject:async()=>{counts.objects++;throw Error('no object writes in validation test');}};
 function result(){return{founding_run:options.restoredRun||run,activation:{status:'COMPLETED'},creation_result:{company_id:'A',business_id:'B',workspace_id:'W'}};}
 const primitive=tag=>function Primitive({children,...props}){return React.createElement(tag,props,children);};
 const inert={__esModule:true,default:primitive('inert')};
 function load(k){if(modules[k])return modules[k].exports;const m=modules[k]={exports:{}};
 vm.runInNewContext(code[k],{module:m,exports:m.exports,URL,URLSearchParams,console,crypto:{randomUUID:()=>String(++frameId)},fetch:()=>{throw Error('Network forbidden');},sessionStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v)},window:{location:{unmount(){for(const frame of frames.values())for(const slot of frame.slots)slot?.cleanup?.();},get search(){return query;},pathname:'/ceo-office/business',assign(){}},history:{replaceState(_a,_b,url){query=new URL(url,'http://local').search;}},sessionStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v)}},document:{querySelector:()=>({focus(){}})},require:p=>{
 if(p==='react')return hooks;if(p==='react/jsx-runtime')return require(p);
 if(p==='next/link')return{__esModule:true,default:primitive('a')};if(p==='next/image')return{__esModule:true,default:primitive('img')};
 if(p==='next/navigation')return{useSearchParams:()=>new URLSearchParams(query),useRouter:()=>({push(){}})};
 if(p.endsWith('BusinessCatalogSurface.js'))return load('catalog');if(p.endsWith('CeoDeskOperating.js'))return load('creator');if(p.endsWith('SharedConversation.js'))return load('shared');if(p.endsWith('writingState.mjs'))return load('writingState');if(p.endsWith('writingBookState.mjs'))return load('bookState');if(p.endsWith('writingApi.js'))return {...load('writingApi'),writingApi:{collection:async()=>({scope:{company_id:company,workspace_id:'W'},books:[],chapters:[],responsibility:{reason:'本地编辑可继续'}}),entry:async()=>({scope:{company_id:company,workspace_id:'W'},pending:[],employees:[]})},createWritingApi:()=>({entry:async()=>({scope:{company_id:'A',workspace_id:'W'},execution:{status:'UNAVAILABLE'}})})};
 if(p.includes('RuntimeProvider'))return{useRuntime:()=>({status:'ready',companyId:company,snapshot:{company:{company_id:company,name:'测试公司'}}})};
 if(p.includes('TerraShell'))return{...inert,TerraPaneContent:props=>React.createElement('panes',props)};
 if(p.includes('organizationProjection'))return{buildOrganizationProjection:()=>({businessById:new Map([['B',{staffingCount:0,roleCount:0,assignments:[]}]]),departmentById:new Map(),employees:[]})};
 if(p.includes('EmployeeAvatar'))return{EmployeeAvatar:primitive('avatar')};if(p.includes('TerraIcons'))return{TerraIcon:primitive('icon')};
 if(p.includes('musicState'))return load('musicState');
 if(p.endsWith('.css'))return{__esModule:true,default:new Proxy({},{get:(_,k)=>k})};if(p.endsWith('.png'))return{__esModule:true,default:'fixture.png'};
 if(p.includes('/lib/'))return api;return inert;
 }});return m.exports;}
 function invoke(fn,props,key){let f=frames.get(key);if(!f||f.fn!==fn){f={fn,slots:[],i:0};frames.set(key,f);}current=f;f.i=0;return fn(props);}
 function deep(n,key='tree'){if(!n||typeof n!=='object')return n;if(Array.isArray(n))return n.map((x,i)=>deep(x,key+':'+i));if(typeof n.type==='function')return deep(invoke(n.type,n.props,key),key+':child');return{...n,props:{...n.props,children:deep(n.props?.children,key+':children')}};}
 let Root=load('creator').CreateBusiness,props={company:{company_id:'A'},sourceDefinition:options.origin||''};
 return{counts,load,storage,api,render(){lastRaw=invoke(Root,props,'root');lastTree=deep(lastRaw);const q=pending;pending=[];q.forEach(f=>f());return lastTree;},async settle(){for(let i=0;i<5;i++){this.render();await tick();}return this.render();},unmount(){for(const frame of frames.values())for(const slot of frame.slots)slot?.cleanup?.();},get search(){return query;},get tree(){return lastTree;},get raw(){return lastRaw;},setRoot(fn,p){Root=fn;props=p;frames.clear();pending=[];},button(label){return nodes(lastTree,n=>n.type==='button'&&text(n)===label)[0];},input(label){return nodes(lastTree,n=>n.props?.['aria-label']===label)[0];},setCompany(v){company=v;props={...props,company:{company_id:v}};},setQuery(v){query=v;}};
}

return {scene,nodes,text,def,writingId,tick};

})();
const display = await (async () => {
const require=createRequire(import.meta.url),React=require('react'),swc=require('next/dist/build/swc');
const root=fileURLToPath(new URL("../..", import.meta.url)); await swc.loadBindings();
const files={writing:'components/writing/WritingWorkspace.js',publishing:'components/writing/WritingPublishingMain.js',terra:'components/terra/TerraPrimitives.js',talent:'app/ceo-office/talent-market/page.js',meeting:'app/ceo-office/meeting/page.js',writingApi:'lib/writingApi.js',writingState:'lib/writingState.mjs',bookState:'lib/writingBookState.mjs',surface:'components/writing/useWritingSurface.js'};
const code={};for(const [k,p] of Object.entries(files)){let s=readFileSync(path.join(root,'frontend',p),'utf8');if(k==='meeting')s+='\nexport { MeetingSurface };';code[k]=(await swc.transform(s,{filename:p,isModule:true,jsc:{parser:{syntax:'ecmascript',jsx:true},transform:{react:{runtime:'automatic'}}},module:{type:'commonjs'}})).code;}
const tick=()=>new Promise(r=>setImmediate(r));
const writingId='com.curis.local.writing-authoring';
const def=(id=writingId)=>({package_id:id,name:'本地写作工作空间',version:'v1',digest:'digest',initial_team_contract:{sha256:'contract',packageId:id,packageVersion:'v1',packageDigest:'digest',displayName:'章节作者'}});
const text=n=>n==null||typeof n==='boolean'?'':typeof n!=='object'?String(n):Array.isArray(n)?n.map(text).join(''):text(n.props?.children);
function nodes(n,p){if(!n||typeof n!=='object')return[];if(Array.isArray(n))return n.flatMap(x=>nodes(x,p));return[...(p(n)?[n]:[]),...nodes(n.props?.children,p)];}
function scene(options={}){
 let current,pending=[],frameId=0,query=options.query||'',company='A',lastRaw,lastTree;const frames=new Map(),modules={},storage=new Map(Object.entries(options.storage||{}));
 const counts={models:0,recover:0,runs:0,saves:0,confirms:0,objects:0};let saved,run={entity_id:'R',owner_ref:'CEO',company_id:'A',lifecycle_status:'PROPOSED'};
 const definition=options.definition||def();const definitions=options.definitions||{definitions:[definition],departments:[{id:'D',name:'业务部'}]};
 const same=(a,b)=>a&&b&&a.length===b.length&&a.every((x,i)=>Object.is(x,b[i]));
 const hooks={...React,useState(initial){const f=current,i=f.i++;if(!(i in f.slots))f.slots[i]={value:typeof initial==='function'?initial():initial};return[f.slots[i].value,v=>{f.slots[i].value=typeof v==='function'?v(f.slots[i].value):v;}];},useRef(initial){const f=current,i=f.i++;return f.slots[i]||=( {current:initial});},useEffect(fn,deps){const f=current,i=f.i++,old=f.slots[i];if(!old||!same(old.deps,deps)){f.slots[i]={deps};pending.push(()=>{old?.cleanup?.();f.slots[i].cleanup=fn();});}},useMemo(fn,deps){const f=current,i=f.i++;if(!f.slots[i]||!same(f.slots[i].deps,deps))f.slots[i]={deps,value:fn()};return f.slots[i].value;},useCallback(fn,deps){return hooks.useMemo(()=>fn,deps);},useLayoutEffect(fn,deps){hooks.useEffect(fn,deps);},useContext(){return()=>{};},useId(){return'fixture';}};
 const api={TENANT_ID:'T',CEO_ID:'CEO',getTalentMarketData:async()=>({companies:[],departments:[],employees:[],companyEmployees:[],experts:[],skills:[],connectors:[],expertCategories:[]}),resolveTalentReturnPath:()=>'',getMeetings:async()=>({active:[],history:[]}),getEmployees:async()=>({employees:[]}),getKnowledgeEntries:async()=>({entries:[]}),runtimeErrorMessage:e=>e.message,getBusinessDefinitions:async(companyId)=>options.definitionByCompany ? await options.definitionByCompany(companyId) : options.definitionPromise?await options.definitionPromise:definitions,getCanonicalBusinesses:async()=>({businesses:[]}),getOrganizationProjection:async()=>({company:{company_id:company},businesses:[],departmentAssignments:[],employees:[],departments:[]}),createFoundingRun:async()=>{counts.runs++;return run;},transitionRuntimeEntity:async(_id,v)=>{run={...run,lifecycle_status:v.target};return run;},saveBusinessDraft:async(_id,v)=>{counts.saves++;saved={...v,proposal_sha256:'sha',snapshot:{company_id:company,definition}};run={...run,data:{v1Proposal:saved}};return run;},createBusinessFromFoundingRun:async()=>{counts.confirms++;if(options.createError)throw Object.assign(new Error("明确失败"),{status:409});if(options.createPromise)return await options.createPromise;return result();},getFoundingRun:async()=>options.restoredRun||run,getBusinessDraft:async()=>({founding_run_id:'R',proposal:options.restoredProposal||saved}),getBusinessCreationResult:async()=>options.resultStatus==='UNKNOWN'?{founding_run:options.restoredRun||run,activation:{status:'UNKNOWN'}}:result(),workspaceOfficeHref:()=>'/existing-workspace',workspaceEntryHref:()=>'/existing-workspace',getEnabledModels:async()=>{counts.models++;return{models:[]};},getModelPreference:async()=>({preference:null,available_models:[]}),recoverAIProvider:async()=>{counts.recover++;throw Error('provider recovery forbidden');},computerAccessView:()=>({title:'无电脑操作',label:'不可用'}),getAssistantIdentity:async()=>({}),conversationError:e=>e.message,createInstalledWorkspaceObject:async()=>{counts.objects++;if(options.objectError)throw options.objectError;throw Error('no object writes in validation test');}};
 function result(){return{founding_run:options.restoredRun||run,activation:{status:'COMPLETED'},creation_result:{company_id:'A',business_id:'B',workspace_id:'W'}};}
 const primitive=tag=>function Primitive({children,...props}){return React.createElement(tag,props,children);};
 const inert={__esModule:true,default:primitive('inert')};
 function load(k){if(modules[k])return modules[k].exports;const m=modules[k]={exports:{}};
 vm.runInNewContext(code[k],{module:m,exports:m.exports,URL,URLSearchParams,console,crypto:{randomUUID:()=>String(++frameId)},fetch:()=>{throw Error('Network forbidden');},sessionStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v)},window:{location:{get search(){return query;},pathname:'/ceo-office/business',assign(){}},history:{replaceState(_a,_b,url){query=new URL(url,'http://local').search;}},sessionStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v)}},document:{querySelector:()=>({focus(){}})},require:p=>{
 if(p==='react')return hooks;if(p==='react/jsx-runtime')return require(p);
 if(p==='next/link')return{__esModule:true,default:primitive('a')};if(p==='next/image')return{__esModule:true,default:primitive('img')};
 if(p==='next/navigation')return{useSearchParams:()=>new URLSearchParams(query),useRouter:()=>({push(){}})};
 if(p.endsWith('BusinessCatalogSurface.js'))return load('catalog');if(p.endsWith('CeoDeskOperating.js'))return load('creator');if(p.endsWith('SharedConversation.js'))return load('shared');if(p.endsWith('writingState.mjs'))return load('writingState');if(p.endsWith('writingBookState.mjs'))return load('bookState');if(p.endsWith('writingApi.js'))return {...load('writingApi'),writingApi:{collection:async()=>({scope:{company_id:company,workspace_id:'W'},books:[],chapters:[],responsibility:{reason:'本地编辑可继续'}}),entry:async()=>({scope:{company_id:company,workspace_id:'W'},pending:[],employees:[]})},createWritingApi:()=>({entry:async()=>({scope:{company_id:'A',workspace_id:'W'},execution:{status:'UNAVAILABLE'}})})};
 if(p.includes('RuntimeProvider'))return{useRuntime:()=>({status:'ready',companyId:company,snapshot:{company:{company_id:company,name:'测试公司'}}})};
 if(p.includes('TerraShell'))return{...inert,TerraPaneContent:props=>React.createElement('panes',props)};
 if(p.includes('organizationProjection'))return{buildOrganizationProjection:()=>({businessById:new Map([['B',{staffingCount:0,roleCount:0,assignments:[]}]]),departmentById:new Map(),employees:[]})};
 if(p.includes('EmployeeAvatar'))return{EmployeeAvatar:primitive('avatar')};if(p.includes('TerraIcons'))return{TerraIcon:primitive('icon')};if(p.includes('TerraPrimitives'))return load('terra');if(p.includes('TerraState'))return{DATA_COPY:{},TerraLoadingSkeleton:primitive('loading'),TerraErrorState:primitive('error')};if(p.includes('useWritingSurface'))return load('surface');
 if(p.includes('musicState'))return load('musicState');
 if(p.endsWith('.css'))return{__esModule:true,default:new Proxy({},{get:(_,k)=>k})};if(p.endsWith('.png'))return{__esModule:true,default:'fixture.png'};
 if(p.includes('/lib/'))return api;return inert;
 }});return m.exports;}
 function invoke(fn,props,key){let f=frames.get(key);if(!f||f.fn!==fn){f={fn,slots:[],i:0};frames.set(key,f);}current=f;f.i=0;return fn(props);}
 function deep(n,key='tree'){if(!n||typeof n!=='object')return n;if(Array.isArray(n))return n.map((x,i)=>deep(x,key+':'+i));if(typeof n.type==='function')return deep(invoke(n.type,n.props,key),key+':child');return{...n,props:{...n.props,children:deep(n.props?.children,key+':children')}};}
 let Root=null,props={};
 return{counts,load,storage,api,render(){lastRaw=invoke(Root,props,'root');lastTree=deep(lastRaw);const q=pending;pending=[];q.forEach(f=>f());return lastTree;},async settle(){for(let i=0;i<5;i++){this.render();await tick();}return this.render();},get tree(){return lastTree;},get raw(){return lastRaw;},setRoot(fn,p){Root=fn;props=p;frames.clear();pending=[];},button(label){return nodes(lastTree,n=>n.type==='button'&&text(n)===label)[0];},input(label){return nodes(lastTree,n=>n.props?.['aria-label']===label)[0];},setCompany(v){company=v;props={...props,company:{company_id:v}};},setQuery(v){query=v;}};
}

return {scene,nodes,text,def,writingId,tick};

})();

export const businessScene=business.scene, displayScene=display.scene;
export const {nodes,text,def,writingId,tick}=business;
