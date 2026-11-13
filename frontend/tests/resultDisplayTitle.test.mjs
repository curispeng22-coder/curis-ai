import assert from 'node:assert/strict';
import test from 'node:test';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import vm from 'node:vm';
const d1Helpers=await import('../lib/d1State.mjs');
const require=createRequire(import.meta.url),swc=require('next/dist/build/swc');await swc.loadBindings();
const code={},files={Reader:'components/v1/ResultReferenceView.js',Utility:'components/workspace/SharedEmployeeWorkArea.js',General:'components/v1/GeneralWorkspaceOperating.js',D1:'components/delivery/d1/ResultView.js'};
for(const k of ['Reader','Utility','General','D1'])code[k]=(await swc.transform(readFileSync(new URL(`../${files[k]}`,import.meta.url),'utf8'),{filename:k+'.js',jsc:{parser:{syntax:'ecmascript',jsx:true},transform:{react:{runtime:'classic'}}},module:{type:'commonjs'}})).code;
const text=n=>n==null||typeof n==='boolean'?'':Array.isArray(n)?n.map(text).join(''):typeof n==='object'?text(n.props?.children):String(n);
const nodes=(n,p)=>!n||typeof n!=='object'?[]:Array.isArray(n)?n.flatMap(x=>nodes(x,p)):[...(p(n)?[n]:[]),...nodes(n.props?.children,p)];
const selection=()=>({workspaceId:'W',referenceId:'ART',explicit:false});
const data=()=>({company:{company_id:'C'},workspace:{workspace_id:'W'},current_work:[{work_ref:'WORK',problem:'整理公开进展',result_refs:['task:TASK'],artifact_refs:['ART'],result_summaries:[{reference_id:'ART',kind:'ARTIFACT',task_ref:'TASK'},{reference_id:'task:TASK',kind:'RESULT',source_work_ref:'WORK'}]}]});
const detail=()=>({tenant_id:'T',company_id:'C',workspace_id:'W',reference_id:'ART',kind:'ARTIFACT',task_ref:'TASK',title:'SYNTHETIC_INTERNAL_HEADING',content:'合成正文：一、整理；二、核对；三、交付。',status:'COMPLETED',verification_status:'UNKNOWN',result_version:'V',viewed:false});
const context=()=>({companyId:'C',workspaceId:'W',referenceId:'ART',source:{workRef:'WORK',kind:'ARTIFACT',taskRef:'TASK',goal:'整理公开进展'}});
function scene(options={}){
 const slots=[],effects=[];let index=0,tree,props;const calls={read:0,viewed:0,businessReturns:[]};
 const react={createElement(type,props,...children){return{type,props:{...props,children}}},useState(initial){const i=index++;if(!(i in slots))slots[i]=typeof initial==='function'?initial():initial;return[slots[i],v=>{slots[i]=typeof v==='function'?v(slots[i]):v}]},useRef(initial){const i=index++;return slots[i]||={current:initial}},useEffect(fn,deps){const i=index++,old=slots[i];if(!old||deps.some((v,j)=>!Object.is(v,old.deps[j]))){slots[i]={deps};effects.push(()=>{old?.cleanup?.();slots[i].cleanup=fn()})}},useMemo(fn){index++;return fn()},useCallback(fn){index++;return fn}};
 const api={getResultDetail:async()=>{calls.read++;return options.result||detail()},markResultViewed:async()=>{calls.viewed++;if(options.receiptError)throw Error('fixture')}};
 const modules={};function load(k){if(modules[k])return modules[k].exports;const m=modules[k]={exports:{}};vm.runInNewContext(code[k],{module:m,exports:m.exports,React:react,URL,URLSearchParams,fetch:()=>{throw Error('Network forbidden')},require:p=>{if(p==='react')return react;if(p.endsWith('/api.js'))return{TENANT_ID:'T'};if(p.endsWith('v1FrontendApi.js'))return api;if(p.endsWith('runtimeApi.js'))return{workspaceEntryHref:w=>'/workspace?workspace_id='+w};if(p.endsWith('businessReturnApi.js'))return{validateBusinessReturn:async(kind,href,scope)=>{calls.businessReturns.push({kind,href,scope});if(!options.validateReturn)throw Error('no authorized return fixture');return options.validateReturn(kind,href,scope)}};if(p.endsWith('d1State.mjs'))return d1Helpers;if(p.endsWith('d1Api.js'))return{d1Error:e=>e.message};if(p.endsWith('SharedEmployeeWorkArea.js'))return load('Utility');return{};}});return m.exports}
 function deep(n){if(!n||typeof n!=='object')return n;if(Array.isArray(n))return n.map(deep);if(typeof n.type==='function')return deep(n.type(n.props));return{...n,props:{...n.props,children:deep(n.props?.children)}}}
 const reader=load('Reader');return{reader,utility:load('Utility'),d1:load('D1'),calls,setProps(p){props=p},render(){index=0;tree=deep((options.root==='D1'?load('D1').default:reader.default)(props));effects.splice(0).forEach(f=>f());return tree},async settle(){for(let i=0;i<5;i++){this.render();await new Promise(r=>setImmediate(r))}return this.render()},get tree(){return tree},unmount(){slots.forEach(x=>x?.cleanup?.())}};
}
function helpers(){const h=scene();assert.equal(typeof h.reader.generalResultTitleContext,'function');assert.equal(typeof h.reader.generalResultDisplayTitle,'function');return h.reader}
test('General passes public projection context and keeps selection identity',()=>{assert.match(readFileSync(new URL("../components/v1/GeneralWorkspaceOperating.js",import.meta.url),'utf8'),/generalTitleContext=\{generalResultTitleContext\(companyId, workspaceId, data, selectedResult\)\}/);assert.deepEqual({...scene().reader.resultSelection('W','ART')},{workspaceId:'W',referenceId:'ART',explicit:true});});
test('exact artifact title uses public goal without mutating data',()=>{const h=helpers(),d=data(),r=detail(),before=JSON.stringify([d,r]);assert.equal(h.generalResultDisplayTitle(r,h.generalResultTitleContext('C','W',d,selection()),'C',selection()),'工作成果 · 整理公开进展');assert.equal(JSON.stringify([d,r]),before)});
test('RESULT preserves type and matches original work',()=>{const h=helpers(),s={...selection(),referenceId:'task:TASK'},r={...detail(),reference_id:'task:TASK',kind:'RESULT',source_work_ref:'WORK'},c=h.generalResultTitleContext('C','W',data(),s);assert.equal(h.generalResultDisplayTitle(r,c,'C',s),'工作结果 · 整理公开进展');assert.equal(h.generalResultDisplayTitle({...r,source_work_ref:'OTHER'},c,'C',s),'工作结果')});
for(const f of ['tenant_id','company_id','workspace_id','reference_id','task_ref','kind'])test('detail mismatch '+f,()=>{const h=helpers(),r={...detail(),[f]:f==='kind'?'EVIDENCE':'OTHER'};assert.equal(h.generalResultDisplayTitle(r,context(),'C',selection()),f==='kind'?'证据':'工作成果')});
for(const v of ['company','workspace','selection','duplicate-work','duplicate-summary','typed-ref','task','goal'])test('projection mismatch '+v,()=>{const h=helpers(),d=data(),s=selection();if(v==='company')d.company.company_id='OTHER';if(v==='workspace')d.workspace.workspace_id='OTHER';if(v==='selection')s.workspaceId='OTHER';if(v==='duplicate-work')d.current_work.push({...d.current_work[0]});if(v==='duplicate-summary')d.current_work[0].result_summaries.push({...d.current_work[0].result_summaries[0]});if(v==='typed-ref')d.current_work[0].artifact_refs=[];if(v==='task')d.current_work[0].result_summaries[0].task_ref='OTHER';if(v==='goal')d.current_work[0].problem=' ';assert.equal(h.generalResultDisplayTitle(detail(),h.generalResultTitleContext('C','W',d,s),'C',s),'工作成果')});
for(const [kind,label] of [['EVIDENCE','证据'],['OUTCOME','业务结果'],['UNKNOWN','工作记录']])test(kind+' is not renamed as an artifact',()=>{assert.equal(helpers().generalResultDisplayTitle({...detail(),kind},context(),'C',selection()),label)});
test('actual reader uses neutral heading for restored missing context with no viewed receipt',async()=>{const h=scene();h.setProps({companyId:'C',selection:selection(),generalTitleContext:{companyId:'C',workspaceId:'W',referenceId:'ART',source:null}});await h.settle();assert.equal(text(nodes(h.tree,n=>n.type==='h2')[0]),'工作成果');assert.equal(h.calls.viewed,0);assert.doesNotMatch(text(h.tree),/SYNTHETIC_INTERNAL_HEADING/);h.unmount()});
test('actual reader and details retain exact body, verification and original immutable object',async()=>{const r=Object.freeze({...detail(),artifacts:[Object.freeze({artifact_id:'RELATED',title:'SYNTHETIC_NESTED_TITLE',content_sha256:'fixture'})]}),before=JSON.stringify(r),h=scene({result:r});h.setProps({companyId:'C',selection:selection(),generalTitleContext:context()});await h.settle();assert.equal(text(nodes(h.tree,n=>n.type==='h2')[0]),'工作成果 · 整理公开进展');assert.ok(nodes(h.tree,n=>n.type==='p').some(n=>text(n)===r.content));assert.match(text(h.tree),/尚未验证/);assert.doesNotMatch(text(h.tree),/SYNTHETIC_INTERNAL_HEADING|SYNTHETIC_NESTED_TITLE/);assert.equal(JSON.stringify(r),before);const shown=JSON.parse(text(nodes(h.tree,n=>n.type==='pre')[0]));assert.equal(shown.verification_status,r.verification_status);assert.equal(shown.content,r.content);assert.equal(shown.result_version,r.result_version);h.unmount()});
test('explicit click keeps one receipt and failure message',async()=>{const h=scene({receiptError:true});h.setProps({companyId:'C',selection:{...selection(),explicit:true},generalTitleContext:context()});await h.settle();assert.equal(h.calls.viewed,1);assert.match(text(h.tree),/查看记录尚未保存/);assert.equal(text(nodes(h.tree,n=>n.type==='h2')[0]),'工作成果 · 整理公开进展');h.unmount()});
test('non-General caller keeps existing public title and VERIFIED status',()=>{const h=scene(),r={...detail(),title:'公开来源名',verification_status:'VERIFIED'},t=h.utility.SharedResultUtility({result:r});assert.equal(text(nodes(t,n=>n.type==='h2')[0]),'公开来源名');assert.match(text(t),/已有验证记录/)});
test('old context cannot label a new company or reference',()=>{const h=helpers();assert.equal(h.generalResultDisplayTitle(detail(),context(),'OTHER',selection()),'工作成果');assert.equal(h.generalResultDisplayTitle(detail(),context(),'C',{...selection(),referenceId:'OTHER'}),'工作成果')});

test('D1 safe presentation copy covers artifact headline and associated material titles without changing body or original',()=>{const h=scene(),r=Object.freeze({...detail(),artifacts:[Object.freeze({artifact_id:'A',title:'SYNTHETIC_NESTED_TITLE',content:'关联正文'})]}),before=JSON.stringify(r),v=h.d1.resultDisplayCopy(r);assert.equal(v.title,'工作成果');assert.equal(v.artifacts[0].title,'关联成果');assert.equal(v.artifacts[0].content,'关联正文');assert.equal(v.content,r.content);assert.equal(v.verification_status,r.verification_status);assert.equal(JSON.stringify(r),before);});

test('actual D1 visible header, related material and source details never render internal artifact titles',async()=>{const r=Object.freeze({...detail(),artifacts:[{artifact_id:'RELATED',title:'SYNTHETIC_NESTED_TITLE',content:'关联正文'}]}),h=scene({root:'D1'});h.setProps({companyId:'C',selection:{workspaceId:'W',resultRef:'ART',explicit:false},api:{result:async()=>r}});await h.settle();assert.equal(text(nodes(h.tree,n=>n.type==='h1')[0]),'工作成果');assert.doesNotMatch(text(h.tree),/SYNTHETIC_INTERNAL_HEADING|SYNTHETIC_NESTED_TITLE/);assert.match(text(h.tree),/合成正文/);assert.match(text(h.tree),/UNKNOWN/);h.unmount();});

// Complete, recognized envelopes are a summary display only; identity and receipts stay original.
const generalEnvelope = (summary = "合成建议一。\n合成建议二。\n合成建议三。") => ({ status: "ACCEPTED", resultType: "general-business-result", summary, problem: "SYNTHETIC_PROBLEM_NOT_READING", humanInput: { whyUser: "SYNTHETIC_ENVELOPE_NOT_READING" } });
const readingResult = (envelope = generalEnvelope()) => ({ ...detail(), kind: "RESULT", reference_id: "task:TASK", source_work_ref: "WORK", content: JSON.stringify(envelope), summary: "不同的DTO摘要", response_eligibility: { status: "INELIGIBLE", reason: "合成不可选择原因" } });
const normalized = value => JSON.parse(JSON.stringify(value));
test('D1 known complete envelope preserves exact summary whitespace and the immutable DTO', () => {
 const r=Object.freeze(readingResult(generalEnvelope("  合成摘要一。\n合成摘要二。  "))),before=JSON.stringify(r),p=scene().d1.resultReadingProjection(r);
 assert.equal(p.isSummary,true);assert.equal(p.material[0].text,"  合成摘要一。\n合成摘要二。  ");assert.equal(JSON.stringify(r),before);
 assert.equal(r.result_version,'V');assert.equal(r.verification_status,'UNKNOWN');assert.equal(r.response_eligibility.status,'INELIGIBLE');
});
for(const summary of [undefined,null,'','  ',42,[],{}])test('D1 unsupported summary '+JSON.stringify(summary)+' retains original reader without guessing',()=>{
 const envelope=generalEnvelope();if(summary===undefined)delete envelope.summary;else envelope.summary=summary;
 const r=readingResult(envelope),p=scene().d1.resultReadingProjection(r);assert.equal(p.isSummary,false);assert.deepEqual(normalized(p.material),normalized(d1Helpers.readableResult(r)));
});
for(const content of ['普通合成正文','{"resultType":"general-business-result","summary":"不完整','{"resultType":"unknown","summary":"不能冒认"}','[{"resultType":"general-business-result","summary":"数组不是该合同"}]','null','42','{"summary":"没有明确类型"}'])test('D1 unknown or malformed input '+content.slice(0,25)+' is not reconstructed',()=>{
 const r={...readingResult(),content},p=scene().d1.resultReadingProjection(r);assert.equal(p.isSummary,false);assert.deepEqual(normalized(p.material),normalized(d1Helpers.readableResult(r)));
});
for(const kind of ['ARTIFACT','OUTCOME','EVIDENCE'])test('D1 '+kind+' never adopts the General RESULT envelope projection',()=>{const r={...readingResult(),kind},p=scene().d1.resultReadingProjection(r);assert.equal(p.isSummary,false);assert.deepEqual(normalized(p.material),normalized(d1Helpers.readableResult(r)));});
test('actual D1 reads summary, labels it honestly, and does not infer CEO acceptance from envelope ACCEPTED',async()=>{
 const r=Object.freeze(readingResult()),before=JSON.stringify(r),h=scene({root:'D1'});h.setProps({companyId:'C',selection:{workspaceId:'W',resultRef:r.reference_id,explicit:false},api:{result:async()=>r,respond:async()=>assert.fail('no response on read')}});await h.settle();
 const section=nodes(h.tree,n=>n.type==='section'&&nodes(n,x=>x.type==='h2'&&text(x)==='结果摘要').length)[0];assert.ok(section);assert.match(text(section),/合成建议一/);assert.doesNotMatch(text(section),/resultType|SYNTHETIC_PROBLEM|SYNTHETIC_ENVELOPE/);
 assert.match(text(h.tree),/UNKNOWN|合成不可选择原因/);assert.doesNotMatch(text(h.tree),/已保存：认可结果/);assert.equal(JSON.stringify(r),before);h.unmount();
});
test('D1 exact-version viewed receipt still receives the original object and serialized content once',async()=>{
 const r=readingResult(),h=scene({root:'D1'}),seen=[];h.setProps({companyId:'C',selection:{workspaceId:'W',resultRef:r.reference_id,explicit:true},api:{result:async()=>r,viewed:async(c,w,value)=>seen.push({c,w,value})}});await h.settle();assert.equal(seen.length,1);assert.equal(seen[0].value,r);assert.equal(seen[0].value.content,r.content);assert.equal(seen[0].value.result_version,'V');h.unmount();
});
test('D1 saved human choice and verification remain independent of envelope status',async()=>{
 const r={...readingResult(),verification_status:'FAILED',user_response:{action:'REVISE',reason:'合成已保存修改意见'}},h=scene({root:'D1'});h.setProps({companyId:'C',selection:{workspaceId:'W',resultRef:r.reference_id,explicit:false},api:{result:async()=>r}});await h.settle();assert.match(text(h.tree),/核验未通过/);assert.match(text(h.tree),/已保存：要求修改/);assert.match(text(h.tree),/合成已保存修改意见/);h.unmount();
});
test('D1 stale utility version remains blocked before summary reading',async()=>{
 const r=readingResult(),h=scene({root:'D1'});h.setProps({companyId:'C',selection:{workspaceId:'W',resultRef:r.reference_id,resultOrigin:'utility',originCompany:'C',workRef:'WORK',resultVersion:'OTHER',explicit:false},api:{result:async()=>r}});await h.settle();assert.match(text(h.tree),/固定结果版本已变化/);assert.doesNotMatch(text(h.tree),/合成建议一/);h.unmount();
});
test('D1 foreign company remains rejected by the original identity guard',async()=>{
 const r={...readingResult(),company_id:'OTHER'},h=scene({root:'D1'});h.setProps({companyId:'C',selection:{workspaceId:'W',resultRef:r.reference_id,explicit:false},api:{result:async()=>r}});await h.settle();assert.match(text(h.tree),/结果来源不一致/);assert.doesNotMatch(text(h.tree),/合成建议一/);h.unmount();
});
test('General current-work header keeps title flexible and status badge unbroken without layout replacement',()=>{
 const source=readFileSync(new URL('../components/v1/GeneralWorkspaceOperating.js',import.meta.url),'utf8');
 assert.match(source,/<div className="min-w-0 flex-1"><p className="text-ui-1 font-bold text-ui-primary">当前工作/);
 assert.match(source,/<TerraTag color=\{color\} className="shrink-0 whitespace-nowrap">\{label\}<\/TerraTag>/);
});


const returnLink = h => nodes(h.tree,n=>n.type==='a'&&text(n)==='返回原工作空间')[0].props.href;
const chapterReturn = '/ceo-office/workspace/installed/W?writing_mode=chapter&book_ref=book&chapter_ref=chapter&draft_ref=draft&anchor=selected';
for(const kind of ['writing','cg','music'])test('result returns to validated '+kind+' object rather than workspace library',async()=>{
 const href=kind==='writing'?chapterReturn:`/ceo-office/workspace/installed/W?${kind}_mode=object`;
 const h=scene({validateReturn:async(k,value,scope)=>{assert.equal(k,kind);assert.equal(value,href);assert.equal(scope.employeeCompany,'C');return{company:'C',workspace:'W',href:value}}});
 h.setProps({companyId:'C',selection:selection(),businessReturn:{kind,href}});await h.settle();
 assert.equal(returnLink(h),href);assert.equal(h.calls.businessReturns.length,1);assert.equal(h.calls.viewed,0);h.unmount();
});
test('unvalidated result origin retains existing conversation/workspace fallback while pending',async()=>{
 let finish;const h=scene({validateReturn:()=>new Promise(resolve=>{finish=resolve})});
 const conversation='/ceo-office/conversation?conversation_id=original';
 h.setProps({companyId:'C',selection:selection(),businessReturn:{kind:'writing',href:chapterReturn},conversationReturn:conversation});await h.settle();
 assert.match(returnLink(h),/^\/workspace\?workspace_id=W&result_workspace=W&result_ref=ART/);
 assert.equal(new URL(returnLink(h),'https://fixture.invalid').searchParams.get('return_to'),conversation);
 finish({company:'C',workspace:'W',href:chapterReturn});await h.settle();assert.equal(returnLink(h),chapterReturn);h.unmount();
});
for(const failure of ['company','workspace','invalid','missing-href'])test('result origin refuses '+failure+' and retains safe fallback',async()=>{
 const h=scene({validateReturn:async()=>{if(failure==='invalid')throw Error('invalid source');return{company:failure==='company'?'OTHER':'C',workspace:failure==='workspace'?'OTHER':'W',...(failure==='missing-href'?{}:{href:chapterReturn})}}});
 h.setProps({companyId:'C',selection:selection(),businessReturn:{kind:'writing',href:failure==='invalid'?'https://untrusted.invalid/':chapterReturn}});await h.settle();
 assert.match(returnLink(h),/^\/workspace\?workspace_id=W&result_workspace=W&result_ref=ART/);assert.doesNotMatch(returnLink(h),/untrusted/);h.unmount();
});
test('unknown business kind never reaches the business return validator',async()=>{
 const h=scene({validateReturn:async()=>assert.fail('unrecognized kind must not validate')});h.setProps({companyId:'C',selection:selection(),businessReturn:{kind:'foreign',href:chapterReturn}});await h.settle();
 assert.equal(h.calls.businessReturns.length,0);assert.match(returnLink(h),/^\/workspace\?/);h.unmount();
});
test('stale origin validation cannot replace current object return',async()=>{
 const pending=[];const h=scene({validateReturn:(kind,href)=>new Promise(resolve=>pending.push({href,resolve}))});
 const props={companyId:'C',selection:selection(),businessReturn:{kind:'writing',href:chapterReturn}};
 h.setProps(props);await h.settle();assert.equal(pending.length,1);
 const next=chapterReturn.replace('chapter_ref=chapter','chapter_ref=next');h.setProps({...props,businessReturn:{kind:'writing',href:next}});await h.settle();assert.equal(pending.length,2);
 pending[0].resolve({company:'C',workspace:'W',href:chapterReturn});await h.settle();assert.match(returnLink(h),/^\/workspace\?/);
 pending[1].resolve({company:'C',workspace:'W',href:next});await h.settle();assert.equal(returnLink(h),next);h.unmount();
});
test('changed company cannot display a previous validated object link even before effects settle',async()=>{
 const h=scene({validateReturn:async()=>({company:'C',workspace:'W',href:chapterReturn})});const props={companyId:'C',selection:selection(),businessReturn:{kind:'writing',href:chapterReturn}};
 h.setProps(props);await h.settle();assert.equal(returnLink(h),chapterReturn);
 h.setProps({...props,companyId:'OTHER'});h.render();assert.match(returnLink(h),/^\/workspace\?/);await h.settle();assert.match(returnLink(h),/^\/workspace\?/);h.unmount();
});
