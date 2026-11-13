import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import vm from 'node:vm';
import {pathToFileURL} from 'node:url';
const frontendRoot=process.env.CURIS_CG_TEST_FRONTEND?pathToFileURL(process.env.CURIS_CG_TEST_FRONTEND+'/'):new URL('../',import.meta.url);
const state=await import(process.env.CURIS_CG_BASELINE==='1'?new URL('lib/contentGrowthState.mjs',frontendRoot):new URL('../lib/contentGrowthState.mjs',import.meta.url));
const require=createRequire(new URL('package.json',frontendRoot)),React=require('react'),swc=require('next/dist/build/swc');await swc.loadBindings();
const compiled={};
for(const [name,file]of Object.entries({market:'ContentGrowthMarket.js',analysis:'ContentGrowthAnalysis.js',observe:'ContentGrowthObserve.js',learning:'ContentGrowthLearning.js'})){
  compiled[name]=(await swc.transform(readFileSync(name==='learning'&&process.env.CURIS_CG_BASELINE!=='1'?new URL('../components/content-growth/'+file,import.meta.url):new URL('components/content-growth/'+file,frontendRoot),'utf8'),{filename:file,isModule:true,jsc:{parser:{syntax:'ecmascript',jsx:true},transform:{react:{runtime:'automatic'}}},module:{type:'commonjs'}})).code;
}
function scene(api,props,name='market'){
  const slots=[],effects=[],storage=new Map();let cursor=0;
  const same=(a,b)=>a&&b&&a.length===b.length&&a.every((x,i)=>Object.is(x,b[i]));
  const hooks={
    useState(initial){const i=cursor++;if(!(i in slots))slots[i]={value:typeof initial==='function'?initial():initial};return [slots[i].value,v=>slots[i].value=typeof v==='function'?v(slots[i].value):v];},
    useRef(initial){const i=cursor++;return slots[i]||={current:initial};},
    useMemo(fn,deps){const i=cursor++;if(!slots[i]||!same(slots[i].deps,deps))slots[i]={deps,value:fn()};return slots[i].value;},
    useCallback(fn,deps){return hooks.useMemo(()=>fn,deps);},
    useEffect(fn,deps){const i=cursor++;if(!slots[i]||!same(slots[i].deps,deps)){const old=slots[i];slots[i]={deps};effects.push(()=>{old?.cleanup?.();slots[i].cleanup=fn();});}},
  };hooks.useLayoutEffect=hooks.useEffect;
  const m={exports:{}};
  vm.runInNewContext(compiled[name],{module:m,exports:m.exports,crypto:globalThis.crypto,URLSearchParams,sessionStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v),removeItem:k=>storage.delete(k)},require:request=>{
    if(request==='react')return {...React,...hooks};if(request==='react/jsx-runtime')return require(request);
    if(request==='next/link')return {__esModule:true,default:p=>React.createElement('a',p,p.children)};
    if(request.endsWith('contentGrowthState.mjs'))return state;if(request.endsWith('contentGrowthApi.js'))return {contentGrowthApi:api};
    if(request.endsWith('ContentGrowthMarket.js'))return {GrowthRecordPanel:'growth-record-panel'};
    if(request.endsWith('ContentGrowthObserve.js'))return {__esModule:true,default:'observation-consumer'};
    if(request.endsWith('.module.css'))return {__esModule:true,default:new Proxy({},{get:(_,k)=>k})};return {};
  }});
  const render=()=>{cursor=0;return (name==='market'?m.exports.GrowthRecordPanel:m.exports.default)(props);};
  return {render,storage,async flush(){render();for(const fn of effects.splice(0))fn();await new Promise(r=>setImmediate(r));return render();},find:p=>nodes(render(),p)[0],unmount(){slots.forEach(slot=>slot?.cleanup?.());}};
}
function nodes(node,p){if(!node||typeof node!=='object')return [];if(Array.isArray(node))return node.flatMap(v=>nodes(v,p));return [...(p(node)?[node]:[]),...nodes(node.props?.children,p)];}
const text=n=>!n?'':typeof n==='string'?n:Array.isArray(n)?n.map(text).join(''):typeof n==='object'?text(n.props?.children):String(n);
const entry={scope:{tenant_id:'selfuse',company_id:'co',workspace_id:'w'},definition:{package_id:state.CG_PACKAGE_V02.id,version:state.CG_PACKAGE_V02.version,digest:state.CG_PACKAGE_V02.digest}};
function fixture(records=[]){let rows=records;const calls=[];return {calls,api:{operatingContext:async()=>({entry,records:rows}),accounts:async()=>({entry,accounts:[]}),observations:async()=>({entry,observations:[]}),saveOperatingContext:async(c,w,kind,p)=>{calls.push({kind,p});const r={ref:'new',payload:p.data,kind,revision:1,basis:[]};rows=[...rows,r];return r;}},props:{company:'co',workspaceId:'w',kinds:['Scope'],onInspect(){}}};}
test('real compiled manual scope saves actual user fields without model; cancel retains text',async()=>{const f=fixture(),h=scene(f.api,f.props);await h.flush();h.find(n=>n.type==='button'&&text(n)==='新增观察范围').props.onClick();const inputs=()=>nodes(h.render(),n=>n.type==='input');inputs()[0].props.onChange({target:{value:'我的阅读范围'}});inputs()[1].props.onChange({target:{value:'阅读'}});inputs()[2].props.onChange({target:{value:'十月'}});h.find(n=>n.type==='button'&&text(n)==='取消，保留输入').props.onClick();h.find(n=>n.type==='button'&&text(n)==='继续编辑保留的输入').props.onClick();assert.equal(inputs()[0].props.value,'我的阅读范围');await h.find(n=>n.type==='form').props.onSubmit({preventDefault(){}});assert.equal(f.calls.length,1);assert.equal(f.calls[0].p.data.keywords,'阅读');assert.ok(!('model' in f.calls[0].p.data));});
test('real compiled failed save retains form and exact request identity for unchanged retry',async()=>{const f=fixture();let attempts=[];f.api.saveOperatingContext=async(c,w,k,p)=>{attempts.push(p);throw new Error('409 original scope changed');};const h=scene(f.api,f.props);await h.flush();h.find(n=>n.type==='button'&&text(n)==='新增观察范围').props.onClick();nodes(h.render(),n=>n.type==='input')[0].props.onChange({target:{value:'保留输入'}});await h.find(n=>n.type==='form').props.onSubmit({preventDefault(){}});assert.match(text(h.render()),/409 original scope changed/);await h.find(n=>n.type==='form').props.onSubmit({preventDefault(){}});assert.equal(attempts[0].request_id,attempts[1].request_id);assert.equal(nodes(h.render(),n=>n.type==='input')[0].props.value,'保留输入');});
test('context source return keeps exact manual record and malformed duplicate locators refuse',()=>{const href=state.contentHref('w',{view:'analysis',object:'old-report',account:'account1',period:'十月'});const parsed=state.cgReturnTarget(href);assert.equal(parsed.entry.object,'old-report');assert.equal(parsed.entry.period,'十月');assert.throws(()=>state.cgReturnTarget(href+'&cg_object=other'));});

test('cancelled manual input blocks silent new-form replacement until explicit discard',async()=>{const f=fixture(),h=scene(f.api,f.props);await h.flush();h.find(n=>n.type==='button'&&text(n)==='新增观察范围').props.onClick();nodes(h.render(),n=>n.type==='input')[0].props.onChange({target:{value:'保留原输入'}});h.find(n=>n.type==='button'&&text(n)==='取消，保留输入').props.onClick();h.find(n=>n.type==='button'&&text(n)==='新增观察范围').props.onClick();assert.match(text(h.render()),/输入已保留/);h.find(n=>n.type==='button'&&text(n)==='继续编辑保留的输入').props.onClick();assert.equal(nodes(h.render(),n=>n.type==='input')[0].props.value,'保留原输入');h.find(n=>n.type==='button'&&text(n)==='取消，保留输入').props.onClick();h.find(n=>n.type==='button'&&text(n)==='明确放弃保留输入').props.onClick();h.find(n=>n.type==='button'&&text(n)==='新增观察范围').props.onClick();assert.equal(nodes(h.render(),n=>n.type==='input')[0].props.value,'');});
test('saving disables actual whole form and cancel until request settles',async()=>{const f=fixture();let resolve;f.api.saveOperatingContext=()=>new Promise(r=>{resolve=r;});const h=scene(f.api,f.props);await h.flush();h.find(n=>n.type==='button'&&text(n)==='新增观察范围').props.onClick();const pending=h.find(n=>n.type==='form').props.onSubmit({preventDefault(){}});assert.equal(h.find(n=>n.type==='fieldset').props.disabled,true);resolve({ref:'saved'});await pending;assert.equal(f.calls.length,0);assert.match(text(h.render()),/已保存原来源/);});
test('binding a reference preserves pinned direction/reports and ignores late result after scope change',async()=>{const direction={ref:'direction',kind:'Direction',payload:{title:'原方向'},revision:1,basis:[]},reference={ref:'reference',kind:'Reference',payload:{title:'原参考'},revision:1,basis:[]},prior={ref:'context',kind:'Context',payload:{content_ref:'content',version_ref:'version',reference_refs:['existing-reference'],direction_ref:'direction',report_refs:['original-report']},revision:1,basis:[]};const f=fixture([direction,reference,prior]);f.props.kinds=['Reference'];f.props.collection={contents:[{content:{entity_id:'content'},version:{entity_id:'version',data:{title:'真实原内容'}}}]};const h=scene(f.api,f.props);await h.flush();h.find(n=>n.type==='select').props.onChange({target:{value:'content'}});await h.find(n=>n.type==='button'&&text(n)==='确认引用，不改正文').props.onClick();assert.deepEqual(JSON.parse(JSON.stringify(f.calls[0].p.data)),{title:'原参考',content_ref:'content',version_ref:'version',reference_refs:['existing-reference','reference'],direction_ref:'direction',report_refs:['original-report']});let resolve;f.api.saveOperatingContext=()=>new Promise(r=>resolve=r);const pending=h.find(n=>n.type==='button'&&text(n)==='确认引用，不改正文').props.onClick();f.props.company='other';await h.flush();resolve({ref:'late'});await pending;assert.ok(!text(h.render()).includes('late'));});


const tick=()=>new Promise(resolve=>setImmediate(resolve));
const deferred=()=>{let resolve,reject;const promise=new Promise((yes,no)=>{resolve=yes;reject=no;});return {promise,resolve,reject};};
const button=(tree,label)=>nodes(tree,n=>n.type==='button'&&text(n)===label)[0];
function control(tree,label,tag){const row=nodes(tree,n=>n.type==='label'&&text(n).startsWith(label))[0];assert.ok(row,'label '+label);const input=nodes(row,n=>n.type===tag)[0];assert.ok(input,'control '+label);return input;}
const scopedEntry=(company,workspace)=>({...entry,scope:{...entry.scope,company_id:company,workspace_id:workspace,business_id:'business-'+company}});
const originalReport=()=>({ref:'report-original',kind:'Report',revision:1,basis:[],payload:{title:'原报告',account_ref:'account-one',period:'本周',observation_refs:['observation-old'],content_ref:'',version_ref:'',artifact_ref:'',fact:'保留事实',interpretation:'保留解读',unknown:'保留未知',next_decision:'保留下一步',confirmed:true}});
function liveFixture(){
  let records=[originalReport()],observations=[{entity_id:'observation-old',data:{scope_ref:'account-one',period:'本周',title:'原观察',body:'原事实',platform_ref:'xhs',account_name:'原账号'}}];
  const creates=[],saves=[];
  const api={
    operatingContext:async(c,w)=>({entry:scopedEntry(c,w),records:c==='co'?records:[]}),
    accounts:async(c,w)=>({entry:scopedEntry(c,w),accounts:[{entity_id:'account-one',data:{name:'原账号',platform_ref:'xhs'}}]}),
    observations:async(c,w)=>({entry:scopedEntry(c,w),observations:c==='co'?[...observations]:[]}),
    observationCreate:async(c,w,id,data)=>{creates.push({company:c,workspace:w,id,data});const item={entity_id:'observation-new-'+creates.length,data:{...data,account_name:'原账号',platform_ref:'xhs'}};observations=[...observations,item];return item;},
    saveOperatingContext:async(c,w,kind,payload)=>{saves.push(payload);const item={ref:'saved-report',kind,revision:2,basis:[],payload:payload.data};records=[...records,item];return item;},
  };
  return {api,creates,saves,setObservations:value=>{observations=value;}};
}
async function connected(f){
  let panel;const parentProps={company:'co',workspaceId:'w',collection:{contents:[]},entry:{object:'report-original'},onInspect:value=>{panel=value;}};
  const parent=scene(f.api,parentProps,'analysis');await parent.flush();
  const reportElement=()=>nodes(parent.render(),n=>n.type==='growth-record-panel')[0],observeElement=()=>nodes(parent.render(),n=>n.type==='observation-consumer')[0];
  const reportProps={...reportElement().props},observeProps={...observeElement().props};const report=scene(f.api,reportProps),observe=scene(f.api,observeProps,'observe');
  const sync=async()=>{await parent.flush();Object.assign(reportProps,reportElement().props);Object.assign(observeProps,observeElement().props);await report.flush();await observe.flush();};
  await sync();await sync();
  return {parent,parentProps,report,reportProps,observe,observeProps,reportElement,observeElement,sync,get panel(){return panel;},close(){observe.unmount();report.unmount();parent.unmount();}};
}
async function fillObservation(flow,title='同页新观察'){
  button(flow.observe.render(),'新建观察').props.onClick();await flow.observe.flush();
  control(flow.panel.content,'观察账号','select').props.onChange({target:{value:'account-one'}});await flow.observe.flush();
  control(flow.panel.content,'观察标题','input').props.onChange({target:{value:title}});await flow.observe.flush();
  control(flow.panel.content,'观察周期','input').props.onChange({target:{value:'本周'}});await flow.observe.flush();
  control(flow.panel.content,'观察正文','textarea').props.onChange({target:{value:'同页人工事实'}});await flow.observe.flush();
}
function observationChoices(tree){const group=nodes(tree,n=>n.type==='fieldset'&&Array.isArray(n.props.children)&&n.props.children.some(v=>v?.type==='legend'&&text(v)==='固定原观察'))[0];return nodes(group,n=>n.type==='label');}

test('actual Analysis -> Observe save -> existing Report refresh retains fields, selected refs, expected version and uncertain request identity',async()=>{
  const f=liveFixture();f.api.saveOperatingContext=async(c,w,k,p)=>{f.saves.push(p);throw new Error('原请求结果待核对');};const flow=await connected(f);
  const initialKey=flow.reportElement().key;button(flow.report.render(),'修订为新版本').props.onClick();await flow.report.flush();
  control(flow.report.render(),'事实（人工原记录）','textarea').props.onChange({target:{value:'正在填写的事实'}});await flow.report.flush();
  let pending=flow.report.find(n=>n.type==='form').props.onSubmit({preventDefault(){}});await flow.report.flush();await pending;await flow.report.flush();
  const storageKey='curis.cg.manual.co:w:Report',before=JSON.parse(flow.report.storage.get(storageKey));assert.equal(before.expected,'report-original');assert.ok(before.identity.request_id);assert.equal(before.editing,true);
  await fillObservation(flow);await button(flow.panel.content,'保存观察记录').props.onClick();await flow.sync();await flow.sync();
  assert.equal(flow.reportElement().key,initialKey);assert.equal(flow.reportElement().props.selectedRef,'report-original');assert.equal(flow.reportProps.observationRevision,1);
  const choices=observationChoices(flow.report.render());assert.equal(choices.length,2);assert.equal(choices.find(n=>text(n).startsWith('原观察')).props.children[0].props.checked,true);assert.equal(choices.find(n=>text(n).startsWith('同页新观察')).props.children[0].props.checked,false);
  assert.deepEqual(JSON.parse(flow.report.storage.get(storageKey)),before,'refresh does not reset retained form/expected/identity/confirmation');
  for(const [label,value]of [['事实（人工原记录）','正在填写的事实'],['人工解读','保留解读'],['尚未确定','保留未知'],['建议与下一步','保留下一步']])assert.equal(control(flow.report.render(),label,'textarea').props.value,value);
  pending=flow.report.find(n=>n.type==='form').props.onSubmit({preventDefault(){}});await flow.report.flush();await pending;await flow.report.flush();
  assert.equal(f.saves[0].request_id,f.saves[1].request_id);assert.equal(f.saves[1].expected_ref,'report-original');assert.deepEqual(JSON.parse(JSON.stringify(f.saves[1].data.observation_refs)),['observation-old']);
  flow.close();
});

test('confirmed Observe save invalidates sibling even if its own list reload fails; failed save keeps identity and sends no notification',async()=>{
  const f=liveFixture(),create=f.api.observationCreate,read=f.api.observations,attempts=[];let fail=true,failRead=false;
  f.api.observationCreate=async(...args)=>{attempts.push(args);if(fail){fail=false;throw new Error('保存结果待核验');}const item=await create(...args);failRead=true;return item;};
  f.api.observations=async(...args)=>{if(failRead){failRead=false;throw new Error('仅下方列表重读失败');}return read(...args);};
  const flow=await connected(f);button(flow.report.render(),'修订为新版本').props.onClick();await flow.report.flush();await fillObservation(flow);
  await button(flow.panel.content,'保存观察记录').props.onClick();await flow.sync();assert.equal(flow.reportProps.observationRevision,0);assert.equal(f.creates.length,0);
  await button(flow.panel.content,'保存观察记录').props.onClick();await flow.sync();await flow.sync();
  assert.equal(attempts[0][2],attempts[1][2]);assert.equal(flow.reportProps.observationRevision,1);assert.equal(observationChoices(flow.report.render()).length,2);assert.match(text(flow.observe.render()),/仅下方列表重读失败/);
  await fillObservation(flow,'下一条确认观察');await button(flow.panel.content,'保存观察记录').props.onClick();await flow.sync();assert.notEqual(attempts[1][2],attempts[2][2]);flow.close();
});

test('Report refresh latest read wins over late same-scope responses/errors and keeps account-period filtering',async()=>{
  for(const lateError of [false,true]){
    const f=liveFixture(),old=deferred(),read=f.api.observations;let first=true;
    f.api.observations=(...args)=>{if(first){first=false;return old.promise;}return read(...args);};
    const props={company:'co',workspaceId:'w',kinds:['Report'],observationRevision:0};const h=scene(f.api,props);await h.flush();
    f.setObservations([{entity_id:'new',data:{title:'最新有效观察',scope_ref:'account-one',period:'本周'}},{entity_id:'foreign-account',data:{title:'其他账号',scope_ref:'different',period:'本周'}},{entity_id:'foreign-period',data:{title:'其他周期',scope_ref:'account-one',period:'上周'}}]);
    props.observationRevision=1;await h.flush();await h.flush();button(h.render(),'修订为新版本').props.onClick();await h.flush();
    assert.equal(observationChoices(h.render()).length,1);assert.match(text(observationChoices(h.render())),/最新有效观察/);
    if(lateError)old.reject(new Error('迟到旧读取错误'));else old.resolve({entry,observations:[{entity_id:'stale',data:{title:'迟到旧数据',scope_ref:'account-one',period:'本周'}}]});
    await h.flush();await h.flush();assert.match(text(observationChoices(h.render())),/最新有效观察/);assert.doesNotMatch(text(h.render()),/迟到旧/);h.unmount();
  }
});

test('Observe late success/failure after scope change, ABA return or unmount cannot notify or clear a newer creation',async()=>{
  for(const navigation of ['scope','workspace','aba','unmount','failure']){
    const f=liveFixture(),wait=deferred(),create=f.api.observationCreate;let calls=0;
    f.api.observationCreate=(...args)=>{calls++;return calls===1?wait.promise:create(...args);};
    const flow=await connected(f);await fillObservation(flow,'旧请求');const oldSave=button(flow.panel.content,'保存观察记录').props.onClick;const pending=oldSave();await flow.observe.flush();
    const previousRevision=flow.reportProps.observationRevision;
    if(navigation==='unmount'){flow.observe.unmount();}
    else {if(navigation==='workspace')flow.parentProps.workspaceId='other-workspace';else flow.parentProps.company='other';await flow.sync();if(navigation==='aba'||navigation==='failure'){flow.parentProps.company='co';await flow.sync();}await fillObservation(flow,'新作用域保留输入');}
    if(navigation==='failure')wait.reject(new Error('旧作用域失败'));else wait.resolve({entity_id:'old-success'});
    await pending;await flow.parent.flush();
    assert.equal(flow.reportElement().props.observationRevision,previousRevision);
    if(navigation!=='unmount'){await flow.observe.flush();assert.equal(control(flow.panel.content,'观察标题','input').props.value,'新作用域保留输入');await oldSave();assert.equal(calls,1,'stale save callback cannot issue a new request');}
    flow.close();
  }
});

test('Analysis ignores old-scope/ABA/unmounted notification callbacks and Report ignores old-scope reads',async()=>{
  const f=liveFixture(),props={company:'co',workspaceId:'w'};const parent=scene(f.api,props,'analysis');await parent.flush();const get=()=>nodes(parent.render(),n=>n.type==='observation-consumer')[0].props.onSaved,rev=()=>nodes(parent.render(),n=>n.type==='growth-record-panel')[0].props.observationRevision;
  const old=get();old({company:'other',workspaceId:'w'});assert.equal(rev(),0);props.company='other';await parent.flush();old({company:'co',workspaceId:'w'});assert.equal(rev(),0);props.company='co';await parent.flush();old({company:'co',workspaceId:'w'});assert.equal(rev(),0);get()({company:'co',workspaceId:'w'});assert.equal(rev(),1);const live=get();parent.unmount();live({company:'co',workspaceId:'w'});assert.equal(rev(),1);
  const delayed=deferred(),api={...f.api,observations:(c,w)=>c==='co'?delayed.promise:Promise.resolve({entry:scopedEntry(c,w),observations:[]})},reportProps={company:'co',workspaceId:'w',kinds:['Report']},h=scene(api,reportProps);await h.flush();reportProps.company='other';await h.flush();delayed.resolve({entry,observations:[{entity_id:'old',data:{title:'旧公司数据'}}]});await h.flush();await h.flush();assert.doesNotMatch(text(h.render()),/旧公司数据/);h.unmount();
});

test('Reference purpose selector and original details use Chinese while saved protocol enums remain exact',async()=>{
  const labels={CONTEXT:'背景参考',REFERENCE:'参考借鉴',PATTERN:'模式参考',EVIDENCE:'证据参考',STRUCTURE:'结构参考'};
  for(const [purpose,label]of Object.entries(labels)){
    let inspected;const record={ref:'reference',kind:'Reference',revision:1,basis:[],payload:{title:'原参考',scope_ref:'scope',snapshot_ref:'snapshot',locator:'原位置',body:'原创作方法',purpose}};
    const f=fixture([record,{ref:'scope',kind:'Scope',payload:{title:'原范围'},revision:1,basis:[]},{ref:'snapshot',kind:'Snapshot',payload:{title:'原快照',scope_ref:'scope'},revision:1,basis:[]}]);f.props.kinds=['Reference'];f.props.onInspect=value=>{inspected=value;};const h=scene(f.api,f.props);await h.flush();button(h.render(),'查看原来源').props.onClick();assert.match(text(inspected.content),new RegExp(label));assert.ok(!text(inspected.content).includes(purpose));
    button(h.render(),'修订为新版本').props.onClick();const select=control(h.render(),'引用用途','select');const option=nodes(select,n=>n.type==='option'&&n.props.value===purpose)[0];assert.equal(text(option),label);select.props.onChange({target:{value:option.props.value}});
    await h.find(n=>n.type==='form').props.onSubmit({preventDefault(){}});assert.equal(f.calls[0].p.data.purpose,purpose);assert.equal(f.calls[0].p.expected_ref,'reference');h.unmount();
  }
});


test('background observation invalidation cannot unlock or duplicate an in-flight Report save',async()=>{
  const f=liveFixture(),pending=deferred(),calls=[];f.api.saveOperatingContext=async(c,w,k,p)=>{calls.push(p);return pending.promise;};const props={company:'co',workspaceId:'w',kinds:['Report'],observationRevision:0},h=scene(f.api,props);await h.flush();button(h.render(),'修订为新版本').props.onClick();await h.flush();
  const save=h.find(n=>n.type==='form').props.onSubmit({preventDefault(){}});await h.flush();const originalIdentity=calls[0].request_id;assert.equal(h.find(n=>n.type==='fieldset').props.disabled,true);
  props.observationRevision=1;await h.flush();await h.flush();assert.equal(h.find(n=>n.type==='fieldset').props.disabled,true);assert.equal(JSON.parse(h.storage.get('curis.cg.manual.co:w:Report')).identity.request_id,originalIdentity);
  await h.find(n=>n.type==='form').props.onSubmit({preventDefault(){}});assert.equal(calls.length,1);assert.equal(calls[0].expected_ref,'report-original');assert.deepEqual(JSON.parse(JSON.stringify(calls[0].data.observation_refs)),['observation-old']);
  pending.resolve({ref:'saved'});await save;await h.flush();assert.equal(h.find(n=>n.type==='form'),undefined);h.unmount();
});

test('latest successful Report refresh clears only the prior read failure while retaining the editor',async()=>{
  const f=liveFixture(),props={company:'co',workspaceId:'w',kinds:['Report'],selectedRef:'report-original',observationRevision:0};
  const h=scene(f.api,props);await h.flush();button(h.render(),'修订为新版本').props.onClick();await h.flush();
  control(h.render(),'事实（人工原记录）','textarea').props.onChange({target:{value:'仍在编辑的事实'}});await h.flush();
  const read=f.api.observations;f.api.observations=async()=>{throw new Error('读取原观察暂时失败');};props.observationRevision=1;await h.flush();await tick();await h.flush();assert.match(text(h.render()),/读取原观察暂时失败/);
  f.api.observations=read;props.observationRevision=2;await h.flush();await tick();await h.flush();assert.doesNotMatch(text(h.render()),/读取原观察暂时失败/);assert.equal(control(h.render(),'事实（人工原记录）','textarea').props.value,'仍在编辑的事实');assert.equal(JSON.parse(h.storage.get('curis.cg.manual.co:w:Report')).expected,'report-original');h.unmount();
});

test('successful refresh after concurrent save failure preserves operation error and exact retry request',async()=>{
  const f=liveFixture(),readGate=deferred(),saveGate=deferred(),attempts=[],props={company:'co',workspaceId:'w',kinds:['Report'],selectedRef:'report-original',observationRevision:0};
  f.api.saveOperatingContext=async(c,w,k,p)=>{attempts.push(p);return saveGate.promise;};
  const h=scene(f.api,props);await h.flush();button(h.render(),'修订为新版本').props.onClick();await h.flush();control(h.render(),'事实（人工原记录）','textarea').props.onChange({target:{value:'结果未知仍保留原事实'}});await h.flush();
  const saving=h.find(n=>n.type==='form').props.onSubmit({preventDefault(){}});f.api.observations=()=>readGate.promise;props.observationRevision=1;await h.flush();
  saveGate.reject(new Error('409 原请求结果未知'));await saving;await h.flush();const before=JSON.parse(h.storage.get('curis.cg.manual.co:w:Report'));assert.match(text(h.render()),/409 原请求结果未知 输入已保留，请核对原请求后重试。/);
  readGate.resolve({entry:scopedEntry('co','w'),observations:[{entity_id:'observation-old',data:{scope_ref:'account-one',period:'本周',title:'原观察'}}]});await tick();await h.flush();
  assert.match(text(h.render()),/409 原请求结果未知 输入已保留，请核对原请求后重试。/);assert.equal(control(h.render(),'事实（人工原记录）','textarea').props.value,'结果未知仍保留原事实');const after=JSON.parse(h.storage.get('curis.cg.manual.co:w:Report'));assert.deepEqual(after.identity,before.identity);assert.equal(after.expected,'report-original');assert.deepEqual(after.form.observation_refs,['observation-old']);
  await h.find(n=>n.type==='form').props.onSubmit({preventDefault(){}});assert.equal(attempts.length,2);assert.equal(attempts[0].request_id,attempts[1].request_id);h.unmount();
});

const manualSource=(kind='Report',revision=1,ref=`report-v${revision}`)=>({ref,kind,revision,schemaVersion:'cg.operating-context/v1',scope:{...entry.scope},payload:{title:'同名经营报告',confirmed:true}});
const manualResponse=records=>({entry,schema_version:'cg.operating-context/v1',records});
test('Learning manual sources preserve exact same-title report versions and Reference identity without changing inputs',()=>{
  const records=[manualSource(),manualSource('Report',2),manualSource('Reference',3,'reference-v3')];const before=JSON.stringify(records);
  const sources=state.cgManualLearningSources(manualResponse(records),entry.scope);assert.deepEqual(sources.map(s=>s.reference_id),['report-v1','report-v2','reference-v3']);
  const labels=state.cgReferenceLabels(sources,[],entry.scope);assert.equal(labels.get('report-v1'),'人工报告 · 同名经营报告 · v1');assert.equal(labels.get('report-v2'),'人工报告 · 同名经营报告 · v2');assert.equal(labels.get('reference-v3'),'原参考 · 同名经营报告 · v3');
  assert.ok(sources.every(s=>s.version_ref===s.reference_id));assert.equal(JSON.stringify(records),before);
});
test('Learning manual source qualification rejects unknown unconfirmed foreign missing and malformed records without title fallback',()=>{
  const valid=manualSource(),bad=[null,{}, {...valid,kind:'Direction'}, {...valid,schemaVersion:'unknown'}, {...valid,scope:null}];
  for(const key of ['tenant_id','company_id','workspace_id']){bad.push({...valid,scope:{...entry.scope,[key]:'FOREIGN'}});const scope={...entry.scope};delete scope[key];bad.push({...valid,scope});}
  for(const confirmed of [false,'true',1,undefined])bad.push({...valid,payload:{...valid.payload,confirmed}});
  for(const revision of [0,-1,1.5,'2',NaN,Infinity,Number.MAX_SAFE_INTEGER+1,undefined])bad.push({...valid,revision});
  for(const title of ['', ' ', 3, null, 'x'.repeat(241)])bad.push({...valid,payload:{...valid.payload,title}});
  for(const ref of ['',null,'a b','..', 'x'.repeat(257)])bad.push({...valid,ref});
  assert.deepEqual(state.cgManualLearningSources(manualResponse(bad),entry.scope),[]);
  for(const record of bad){const material={kind:'MANUAL_CONTEXT',reference_id:record?.ref,version_ref:record?.ref,title:'SECRET_TITLE',manual_record:record};assert.equal(state.cgReferenceLabel(material,[],entry.scope),'来源需核对');assert.equal(state.cgReferenceTitle(material,[],entry.scope),'来源标题暂不可读取');}
  const source=state.cgManualLearningSources(manualResponse([valid]),entry.scope)[0];for(const key of ['reference_id','version_ref'])assert.equal(state.cgReferenceLabel({...source,[key]:'wrong'},[],entry.scope),'来源需核对');
  assert.equal(state.cgReferenceLabel(source,[],null),'来源需核对');
});
test('Learning manual envelope validates tenant company workspace package schema and records shape',()=>{
  for(const key of ['tenant_id','company_id','workspace_id'])assert.throws(()=>state.cgManualLearningSources({...manualResponse([manualSource()]),entry:{...entry,scope:{...entry.scope,[key]:'FOREIGN'}}},entry.scope));
  for(const response of [null,{}, {...manualResponse([]),records:null}, {...manualResponse([]),schema_version:'unknown'}, {...manualResponse([]),entry:{...entry,definition:{...entry.definition,digest:'wrong'}}}])assert.throws(()=>state.cgManualLearningSources(response,entry.scope));
});
function learningFixture(response=manualResponse([manualSource(),manualSource('Report',2),manualSource('Reference',3,'reference-v3')])){
 let panel;const calls=[];const api={learnings:async()=>({entry,records:[]}),materials:async()=>({entry,materials:[]}),collection:async()=>({entry,contents:[]}),operatingContext:async()=>response,learningCommand:async(c,w,action,payload)=>{calls.push({c,w,action,payload});return {};}};
 const props={company:'co',workspaceId:'w',onInspect:v=>{panel=v;}};const h=scene(api,props,'learning');return {api,props,h,calls,get panel(){return panel;}};
}
test('compiled Learning selects report v2 by visible exact label and sends only its canonical basis ref',async()=>{
 const f=learningFixture();await f.h.flush();await f.h.flush();button(f.h.render(),'保存新经验').props.onClick();await f.h.flush();
 const labels=nodes(f.panel.content,n=>n.type==='label');const pick=labels.find(n=>text(n)==='人工报告 · 同名经营报告 · v2');assert.ok(pick);assert.ok(labels.some(n=>text(n)==='人工报告 · 同名经营报告 · v1'));nodes(pick,n=>n.type==='input')[0].props.onChange();await f.h.flush();
 control(f.panel.content,'标题','input').props.onChange({target:{value:'基于第二版的经验'}});control(f.panel.content,'正文','textarea').props.onChange({target:{value:'保留原报告版本'}});await f.h.flush();await button(f.panel.content,'保存经验').props.onClick();await f.h.flush();
 assert.equal(f.calls.length,1);assert.equal(f.calls[0].action,'save-learning');assert.deepEqual(Array.from(f.calls[0].payload.data.basis_refs),['report-v2']);assert.ok(!('basis_hashes' in f.calls[0].payload.data));f.h.unmount();
});
test('compiled Learning rejects foreign manual envelope before enabling new experience or exposing titles',async()=>{
 for(const key of ['tenant_id','company_id','workspace_id']){
  const f=learningFixture({...manualResponse([manualSource()]),entry:{...entry,scope:{...entry.scope,[key]:'FOREIGN'}}});await f.h.flush();await f.h.flush();assert.equal(button(f.h.render(),'保存新经验').props.disabled,true);assert.ok(!text(f.h.render()).includes('同名经营报告'));assert.equal(f.calls.length,0);f.h.unmount();
 }
});
test('compiled Learning ignores late manual response after a newer scope read and after unmount',async()=>{
 const f=learningFixture();let resolve;f.api.operatingContext=()=>new Promise(r=>{resolve=r;});await f.h.flush();const oldResolve=resolve;
 const otherEntry={...entry,scope:{...entry.scope,company_id:'other'}};f.props.company='other';f.api.learnings=async()=>({entry:otherEntry,records:[]});f.api.materials=async()=>({entry:otherEntry,materials:[]});f.api.collection=async()=>({entry:otherEntry,contents:[]});f.api.operatingContext=async()=>({entry:otherEntry,schema_version:'cg.operating-context/v1',records:[]});await f.h.flush();await f.h.flush();
 oldResolve(manualResponse([manualSource()]));await f.h.flush();button(f.h.render(),'保存新经验').props.onClick();await f.h.flush();assert.ok(!text(f.panel.content).includes('同名经营报告'));assert.equal(f.calls.length,0);f.h.unmount();
 const g=learningFixture();g.api.operatingContext=()=>new Promise(r=>{resolve=r;});await g.h.flush();g.h.unmount();resolve(manualResponse([manualSource()]));await new Promise(r=>setImmediate(r));assert.equal(g.calls.length,0);assert.equal(g.panel,null);
});
