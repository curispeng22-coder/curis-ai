/* One invocation, sequential passes, immutable review scope. No persisted browser state. */
const assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs');
const timers=[],calls=[],craft={positioning:{genre:'悬疑'}},ms={paragraphs:['原稿']};
const WB={esc:String,ui:{},clone:x=>JSON.parse(JSON.stringify(x)),S:{chapters:{ch1:{bookId:'B'}},storyState:{},reviewRuns:[],__ui:{}},views:{'market.references':{},'book.craft':{render:()=>''}},on:{},act:{},register(k,v){this.views[k]=v;},craftOf:()=>craft,msOf:()=>ms,toast:()=>{},now:()=> 'now',save:()=>{},go:()=>{},render:()=>{}};
vm.runInNewContext(fs.readFileSync(__dirname+'/views-flow.js','utf8'),{WB,setTimeout:fn=>timers.push(fn)});
WB.act.reviewRun=(id,ck,kind,batchId)=>{calls.push(kind);let r={id:'r'+calls.length,batchId,chapter:ck,kind,inputText:ms.paragraphs.join('\n'),ruleSnapshot:WB.reviewRuleSnapshot(id),findings:[]};WB.S.reviewRuns.unshift(r);return r;};
WB.on['review.start'](null,{chapter:'ch1'});WB.on['review.start'](null,{chapter:'ch1'});
assert.equal(timers.length,1,'duplicate start ignored');assert.equal(WB.canFinalize('ch1'),false);
while(timers.length)timers.shift()();
assert.deepEqual(calls,['proof','review','style']);assert.equal(WB.S.reviewBatches.ch1.state,'done');assert.equal(WB.S.reviewBatches.ch1.reportIds.length,3);assert.equal(WB.canFinalize('ch1'),true);
craft.positioning.genre='科幻';assert.equal(WB.canFinalize('ch1'),false,'changed book context invalidates report');
WB.on['review.start'](null,{chapter:'ch1'});timers.shift()();ms.paragraphs=['中途改稿'];timers.shift()();assert.equal(WB.S.reviewBatches.ch1.state,'error');assert.equal(calls.length,4,'no mixed-version report');assert.equal(WB.canFinalize('ch1'),false);
assert.equal(WB.S.reviewBatchHistory.length,1,'prior session retained');assert.equal(JSON.parse(WB.reviewRuleSnapshot('B')).standards.length,3,'employee standards included even without user rules');
console.log('PASS: one start / three passes, duplicate protection, complete-only acceptance, context invalidation, interrupted input, history, professional standards');
