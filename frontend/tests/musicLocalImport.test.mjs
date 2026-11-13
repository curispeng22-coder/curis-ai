import test from 'node:test';
import assert from 'node:assert/strict';
import {createMusicApi,prepareLocalWav,verifiedAudioBlob} from '../lib/musicApi.js';
globalThis.fetch=()=>{throw Error('network forbidden');};
const file=(bytes=new Uint8Array([82,73,70,70]))=>({name:'用户音频.wav',size:bytes.length,arrayBuffer:async()=>bytes.buffer});
test('file cancel is empty; oversize rejected before reading; stale selection rejects before upload',async()=>{
 assert.equal(await prepareLocalWav(null),null);assert.equal(await prepareLocalWav(file(),()=>false),null);
 await assert.rejects(prepareLocalWav({name:'large.wav',size:16000001,arrayBuffer:()=>{throw Error('must not read');}}),/16MB/);
 let current=true;const f=file();f.arrayBuffer=async()=>{current=false;return new Uint8Array([82,73,70,70]).buffer;};await assert.rejects(prepareLocalWav(f,()=>current),/已改变/);
});
test('bounded bytes and Unicode metadata use existing authenticated transport and exact scope',async()=>{
 const p=await prepareLocalWav(file());assert.equal(p.data.size,4);assert.match(p.data.sha256,/^[a-f0-9]{64}$/);
 const calls=[];const api=createMusicApi(async(path,options)=>{calls.push([path,options]);return{};});const payload={request_id:'same',expected:{lyrics_ref:'l',production_ref:'p',master_ref:''},data:p.data};await api.importAudio('公司','workspace','song',payload,p.bytes);await api.importStatus('公司','workspace','song','same');
 assert.match(calls[0][0],/%E5%85%AC%E5%8F%B8/);assert.deepEqual(JSON.parse(decodeURIComponent(calls[0][1].headers['X-Music-Import'])),payload);assert.equal(calls[0][1].headers['Content-Type'],'audio/wav');assert.equal(calls[0][1].body,p.bytes);assert.match(calls[1][0],/imports\/same$/);
});
test('verified audio accepts only exact local provenance pair and byte hash',async()=>{
 const f=await prepareLocalWav(file()),blob=new Blob([f.bytes],{type:'audio/wav'}),base={size:f.data.size,sha256:f.data.sha256};
 for(const [rights,purpose] of [['LOCAL_DESIGN_ONLY','NONCOMMERCIAL_ISOLATED_TEST'],['LOCAL_USER_PROVIDED_UNVERIFIED','LOCAL_USE_ONLY']])assert.equal(await verifiedAudioBlob(blob,{data:{...base,rights,purpose}}),blob);
 await assert.rejects(verifiedAudioBlob(blob,{data:{...base,rights:'LOCAL_DESIGN_ONLY',purpose:'LOCAL_USE_ONLY'}}));await assert.rejects(verifiedAudioBlob(blob,{data:{...base,sha256:'0'.repeat(64),rights:'LOCAL_USER_PROVIDED_UNVERIFIED',purpose:'LOCAL_USE_ONLY'}}));
});
