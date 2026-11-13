/* Minimal state-contract check; no browser, no persisted user state. */
const assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs');
let formal=0,route=null,reason='',draft={paragraphs:['原文'],formalVersion:'v1',versions:[]};
let candidate={id:'C',chapter:'ch1',baseVersion:'v1',changes:[{para:1,before:'原文',after:'改稿',applied:true}]};
const craft={};
const WB={craftOf:()=>craft,clone:x=>JSON.parse(JSON.stringify(x)),esc:String,ui:{},S:{chapters:{ch1:{bookId:'B'}},reviewRuns:[],__ui:{}},views:{'market.references':{},'book.craft':{render:()=>''}},on:{},act:{msConfirmFormal:()=>formal++},register(k,v){this.views[k]=v;},msOf:()=>draft,candidate:()=>candidate,candidateState:()=>({open:0}),toast:()=>{},now:()=> 'now',save:()=>{},go:(a,v,p)=>route=p};
vm.runInNewContext(fs.readFileSync(__dirname+'/views-flow.js','utf8'),{WB,document:{getElementById:()=>({value:reason})}});
assert.equal(WB.canFinalize('ch1'),false,'unreviewed text cannot be finalized');
WB.mergeCandidateDraft('C');assert.deepEqual(draft.paragraphs,['改稿']);assert.equal(formal,0);assert.equal(draft.formalVersion,'v1');assert.equal(route.stage,'review');
WB.mergeCandidateDraft('C');assert.equal(draft.versions.length,1,'merge is idempotent');
WB.S.reviewRuns=['review','proof','style'].map(kind=>({kind,batchId:'batch',ruleSnapshot:WB.reviewRuleSnapshot('B'),chapter:'ch1',inputText:'改稿',id:kind,findings:[]}));
WB.S.reviewBatches={ch1:{id:'batch',book:'B',state:'done',basis:WB.reviewRuleSnapshot('B'),text:'改稿'}};
assert.equal(WB.canFinalize('ch1'),true);
draft.paragraphs=['再次改稿'];assert.equal(WB.canFinalize('ch1'),false,'review invalidates after text changes');
draft.paragraphs=['改稿'];WB.S.reviewRuns[0].findings=[{state:'open'}];WB.on['flow.finalize'](null,{chapter:'ch1'});assert.equal(formal,0,'unresolved suggestions need author reason');
reason='有意保留';WB.on['flow.finalize'](null,{chapter:'ch1'});assert.equal(formal,1);assert.equal(route.stage,'publish');
candidate={id:'C2',chapter:'ch1',baseVersion:'v0',changes:[{para:1,before:'改稿',after:'不能覆盖',applied:true}]};WB.mergeCandidateDraft('C2');assert.deepEqual(draft.paragraphs,['改稿'],'outdated candidate cannot overwrite');
console.log('PASS: draft merge, idempotency, review freshness, author decision, publication handoff, outdated candidate guard');

const old=WB.reviewRuleSnapshot('B'); WB.reviewRules('B').version++;assert.equal(WB.canFinalize('ch1'),false,'rule changes invalidate review');assert.notEqual(old,WB.reviewRuleSnapshot('B'));console.log('PASS rule version invalidation');

const craftSrc=fs.readFileSync(__dirname+'/views-craft.js','utf8');
const analyzeSrc=craftSrc.slice(craftSrc.indexOf('  function analyze('),craftSrc.indexOf('  /* 检查对象'));
const analyze=vm.runInNewContext(analyzeSrc+';analyze',{WB});
WB.S.storyState={};draft.paragraphs=['灯，照着灯。'];
WB.reviewRules('B').items=[{id:'r1',active:true,text:'少用灯',type:'作者偏好',source:'作者',phrase:'灯'},{id:'r2',active:true,text:'人物行为符合动机',type:'作者偏好',source:'作者',phrase:''}];
let findings=analyze('B','ch1','style');assert(findings.some(f=>f.quote==='灯'&&f.para===1));assert(findings.some(f=>f.title.startsWith('待人工')));
WB.reviewRules('B').items.forEach(r=>r.active=false);assert(!analyze('B','ch1','style').some(f=>f.title.includes('本书规则')||f.title.startsWith('待人工')));
console.log('PASS literal rules, semantic unknown, disabled rules');
