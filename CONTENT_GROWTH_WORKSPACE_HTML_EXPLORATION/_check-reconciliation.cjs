// Run: node _check-reconciliation.cjs. State-contract check; browser evidence is separate.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const values={};const document={addEventListener(){},querySelectorAll(){return []},querySelector(){return null},getElementById(id){return {value:values[id]||'',classList:{add(){},remove(){}},style:{},innerHTML:''}}};
const ctx={console,document,setTimeout(){},clearTimeout(){},setInterval(){},clearInterval(){},URL,Date,structuredClone,TextEncoder,Blob,localStorage:{getItem(){return null},setItem(){}},navigator:{},requestAnimationFrame(){}};ctx.window=ctx;ctx.addEventListener=()=>{};vm.createContext(ctx);
for(const file of ['data.js','data-wf.js','data-r5.js','visuals.js','app.js','pages.js','pages2.js','analytics-r5.js','workspace-r7.js','workspace-r8.js','production-work.js','workspace-integration.js'])vm.runInContext(fs.readFileSync(__dirname+'/'+file,'utf8'),ctx,{filename:file});
const C=ctx.CG;C.render=()=>{};C.toast=()=>{};C.closeModal=()=>{};C.openModal=x=>C.lastModal=x;C.go=r=>{C.S.route=r};
let checks=0;const ok=(v,m)=>{assert(v,m);checks++};const action=(a,p,checked)=>C.H['pw-'+a]({dataset:{action:'pw-'+a,p},checked});
for(const [method,acc] of [['dh-oral','dy-founder'],['image-post','xhs-brand'],['article','wx-brand'],['mixcut','dy-brand']]){
const id='CHECK-'+method,defs=C.METHODS[method].steps;const w={id,method,format:method==='article'?'article':method==='image-post'?'image':'video',area:'production',owner:'e-zhou',target:acc,title:'合同检查',status:'working',spec:{ratio:method==='article'?'文章':'9:16'},delivReview:'人工确认'};C.WORKS.push(w);C.WF[id]={method,cur:'brief',steps:Object.fromEntries(defs.map((d,i)=>[d.k,{st:i?'wait':'working',by:C.RESP_EMP[d.resp],artV:'—',art:d.n}]))};C.PW.init(w);
const page=C.productionWorkPage(w);ok(!!page.main,'renders '+method);if(method==='article'||method==='image-post')ok(!page.main.includes('数字人口播 ·'),'no digital steps '+method);
if(method==='dh-oral'){const v=C.PW.revise(w,'script','修改开头');ok(v==='v1','first revision');C.PW.accept(w,'script');}
for(let n=0;n<15&&w.pw.selected!=='qa';n++){const k=w.pw.selected;ok(C.PW.ready(w,k),'ready '+method+' '+k);action('finish',id+'|'+k);}
ok(C.WF[id].cur==='qa','queue current step stays synchronized '+method);ok(C.PW.qaReady(w),'QA dependency readiness '+method);C.PW.check(w);
if(method==='dh-oral'){ok(w.pw.qa==='REWORK','finding grounded in mock claim');C.PW.revise(w,'script','修改限定条件');ok(C.wfOf(w).steps.dh.st==='done','independent asset preserved');C.PW.accept(w,'script');for(let n=0;n<12&&w.pw.selected!=='qa';n++)action('finish',id+'|'+w.pw.selected);C.PW.check(w);}
ok(w.pw.qa==='NEEDS_REVIEW','human gate '+method);action('pass',id);ok(w.pw.qa!=='PASS','no automatic human approval');action('human',id,true);action('pass',id);ok(w.pw.qa==='PASS','QA PASS '+method);C.handoffPublication(w);C.handoffPublication(w);const ps=C.PUBS.filter(p=>p.workId===id);ok(ps.length===1,'idempotent publication');ok(ps[0].accountId===acc,'account preserved');ok(ps[0].mode===(method==='article'?'human':'auto'),'publishing requirement');
}
const old=C.work('W-202'),oldState=C.wfOf(old).steps.script.st;C.PW.init(old);ok(C.wfOf(old).steps.script.st===oldState,'opening preserves existing script review state');ok(C.wfOf(old).steps.script.versions.length>=3,'old version metadata preserved');
console.log('PASS '+checks+' contract assertions across four methods. Browser click evidence required separately.');
