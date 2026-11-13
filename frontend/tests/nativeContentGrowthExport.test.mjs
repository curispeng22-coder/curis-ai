import test from 'node:test';
import assert from 'node:assert/strict';
import { cgExportSelection, saveNativeContentGrowthExport } from '../lib/nativeContentGrowthExport.js';
const record=()=>({entity_id:'cg-verify-one',company_id:'c',data:{objectType:'PublishVerification',business_ref:'b',content_title:'标题',content_body:'正文',content_format:'text',account_ref:'cg-account-one',account_name:'账号',platform_ref:'xhs',platform_name:'小红书',checks:[{key:'cover',label:'封面',checked:false,note:''}],connection_status:'NOT_CONNECTED',verification:'UNVERIFIED',source:'CEO_MANUAL'}});
const selection=()=>cgExportSelection(record(),'c','b');
const payload=()=>({...selection(),package_type:'curis.cg.local-verification-export/1',exported_at:'2026-10-23T00:00:00+00:00',notice:'本地核验导出，不构成发布；平台连接不存在。'});
const blob=value=>new Blob([JSON.stringify(value)]);
test('selected scoped record, dedicated command, exact bytes and verified result',async()=>{
 const input=blob(payload()),calls=[];
 const result=await saveNativeContentGrowthExport(input,selection(),{invoke:async(command,args)=>{calls.push({command,args});return {status:'SAVED',verified:true,bytes:input.size,path:'/synthetic/export/test.json'};}});
 assert.equal(result.status,'SAVED');assert.equal(calls[0].command,'save_cg_local_verification');
 assert.deepEqual(Buffer.from(calls[0].args.bytes),Buffer.from(await input.arrayBuffer()));
 assert.equal(calls[0].args.selection.verification_ref,'cg-verify-one');assert.equal('company_id' in JSON.parse(Buffer.from(calls[0].args.bytes)),false);
});
test('foreign selected company/business, wrong kind/truth are rejected',()=>{
 for(const change of [r=>r.company_id='other',r=>r.data.business_ref='other',r=>r.data.objectType='Other',r=>r.data.verification='VERIFIED',r=>r.data.source='AUTO',r=>r.data.connection_status='CONNECTED']){const r=record();change(r);assert.throws(()=>cgExportSelection(r,'c','b'));}
});
test('wrong ref/account/platform/body/checks/truth/type/extra field/bytes never invoke',async()=>{
 let calls=0;const bridge={invoke:async()=>{calls++;}};
 for(const change of [p=>p.verification_ref='cg-verify-other',p=>p.account.ref='cg-account-other',p=>p.platform.ref='douyin',p=>p.body='changed',p=>p.checks[0].checked=true,p=>p.verification='VERIFIED',p=>p.source='AUTO',p=>p.connection_status='CONNECTED',p=>p.package_type='other',p=>p.company_id='invented',p=>p.exported_at=null]){const p=payload();change(p);await assert.rejects(saveNativeContentGrowthExport(blob(p),selection(),bridge));}
 for(const input of [new Blob([]),new Blob(['x'.repeat(2*1024*1024+1)]),new Blob(['not-json']),new Blob([new Uint8Array([255])])])await assert.rejects(saveNativeContentGrowthExport(input,selection(),bridge));
 assert.equal(calls,0);
});
test('selection stale before call or after byte wait cannot open panel',async()=>{
 let current=false,calls=0;const bridge={invoke:async()=>{calls++;}};
 await assert.rejects(saveNativeContentGrowthExport(blob(payload()),selection(),bridge,()=>current));
 current=true;let release;const input={arrayBuffer:()=>new Promise(resolve=>release=resolve)};
 const pending=saveNativeContentGrowthExport(input,selection(),bridge,()=>current);current=false;release(await blob(payload()).arrayBuffer());await assert.rejects(pending);assert.equal(calls,0);
});
test('selection stale while native returns never binds success to new record',async()=>{
 let current=true,release;const input=blob(payload());const pending=saveNativeContentGrowthExport(input,selection(),{invoke:()=>new Promise(resolve=>release=resolve)},()=>current);
 await new Promise(resolve=>setImmediate(resolve));current=false;release({status:'SAVED',verified:true,bytes:input.size,path:'/synthetic/old.json'});await assert.rejects(pending,/原记录/);
});
test('cancel is explicit and malformed/partial/no-file results are never successful',async()=>{
 const input=blob(payload());const cancelled={status:'CANCELLED',verified:false,bytes:0,path:null};
 assert.deepEqual(await saveNativeContentGrowthExport(input,selection(),{invoke:async()=>cancelled}),cancelled);
 for(const value of [null,{status:'SAVED'}, {status:'SAVED',verified:false,bytes:input.size,path:'/x'}, {status:'SAVED',verified:true,bytes:0,path:'/x'}, {status:'SAVED',verified:true,bytes:input.size,path:''},{status:'CANCELLED',verified:true,bytes:0,path:null}])await assert.rejects(saveNativeContentGrowthExport(input,selection(),{invoke:async()=>value}));
});
test('native failure cannot leak raw paths or package content',async()=>{
 for(const reason of ['/private/sensitive/token',new Error('/private/sensitive/token'),{code:'NSV_WRITE',path:'/private/sensitive/token',errorClass:'SECRET'}]){
 await assert.rejects(saveNativeContentGrowthExport(blob(payload()),selection(),{invoke:async()=>{throw reason;}}),error=>!error.message.includes('sensitive')&&!error.message.includes('SECRET')&&error.message.includes('支持码'));
 }
});
