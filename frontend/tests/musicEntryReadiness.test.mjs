import test from "node:test";
import assert from "node:assert/strict";
import { MUSIC_PACKAGE, musicEntry, songHref, musicReturnTarget, lyricsSelection, audioSelection, selectionCurrent, stableRequest, draftKey, restoredPlayer, isMusicPackage } from "../lib/musicState.mjs";
import { createMusicApi, validateMusicReturn, verifiedAudioBlob } from "../lib/musicApi.js";
const objectScope={tenant_id:'tenant-1',company_id:'company-1',workspace_id:'workspace-1'};
const lyrics={...objectScope,entity_id:'lyrics-1',parent_id:'song-1',data:{kind:'LyricsVersion',text:'你的名字😀，留在雨中。',draft_revision:'r1'}};
const production={...objectScope,entity_id:'production-1',parent_id:'song-1',data:{kind:'ProductionVersion',brief:'轻快节奏'}};
const candidate={...objectScope,entity_id:'candidate-1',parent_id:'song-1',data:{kind:'Candidate',asset_ref:'asset-1',lyrics_ref:'lyrics-1',production_ref:'production-1'}};
const asset={...objectScope,entity_id:'asset-1',parent_id:'song-1',data:{kind:'AudioAssetVersion',sha256:'a'.repeat(64),duration:32}};
const row={song:{...objectScope,entity_id:'song-1',company_id:'company-1',workspace_id:'workspace-1'},lyrics,production,candidates:[candidate],assets:[asset],versions:[lyrics,production,candidate,asset]};

test('lyrics UTF16 keeps whole emoji and immediately expires on edit or version change',()=>{
  const sel=lyricsSelection(lyrics,lyrics.data.text,4,6);assert.equal(sel.excerpt,'😀');
  assert.throws(()=>lyricsSelection(lyrics,lyrics.data.text,4,5));
  assert.equal(selectionCurrent(sel,row,lyrics.data.text,production.data.brief,candidate),true);
  assert.equal(selectionCurrent(sel,row,'你的回忆😀，留在雨中。',production.data.brief,candidate),false);
  assert.equal(selectionCurrent(sel,{...row,lyrics:{...lyrics,entity_id:'lyrics-2'}},lyrics.data.text,production.data.brief,candidate),false);
});
test('audio time locator binds original candidate and asset and does not retarget on switch',()=>{
  const sel=audioSelection(row,candidate,asset,8,16);
  assert.throws(()=>audioSelection(row,candidate,asset,8,40));assert.throws(()=>audioSelection(row,candidate,asset,NaN,16));
  assert.equal(selectionCurrent(sel,row,lyrics.data.text,production.data.brief,candidate),true);
  assert.equal(selectionCurrent(sel,row,lyrics.data.text,production.data.brief,{...candidate,entity_id:'candidate-2'}),false);
  assert.equal(sel.asset_ref,'asset-1');assert.equal(sel.candidate_version_ref,'candidate-1');
});
test('same Song version/asset/range and attempt survive finite return path',()=>{
  const href=songHref('workspace-1',{song:'song-1',lyrics:'lyrics-1',production:'production-1',candidate:'candidate-1',asset:'asset-1',hash:'a'.repeat(64),start:8,end:16,binding:'binding-1',attempt:'attempt-1'});
  const parsed=musicReturnTarget(href);assert.equal(parsed.entry.start,8);assert.equal(parsed.entry.asset,'asset-1');assert.equal(parsed.entry.attempt,'attempt-1');
  assert.equal(musicEntry(new URLSearchParams('music_song=song-1&music_lyrics=lyrics-1&music_start=0&music_end=4')).start,0);
});
test('return rejects external, duplicate, ambiguous, traversal and partial asset anchors',()=>{
  for (const path of ['https://evil.test','//evil.test/','/ceo-office/workspace/installed/%2e%2e','/ceo-office/workspace/installed/a?music_song=x&music_song=y','/ceo-office/workspace/installed/a?music_song=x&music_asset=a','/ceo-office/workspace/installed/a?music_song=x&music_attempt=a','/ceo-office/workspace/installed/a?music_song=x&music_lyrics=y&music_start=0.5&music_end=4','/ceo-office/workspace/installed/a?unknown=x']) assert.throws(()=>musicReturnTarget(path),path);
});
test('Music B3 current company/holder and immutable asset hash are verified before repair return',async()=>{
  const api={collection:async()=>({entry:{scope:{tenant_id:'tenant-1',company_id:'company-1',workspace_id:'workspace-1'},definition:{package_id:MUSIC_PACKAGE.id,version:MUSIC_PACKAGE.version,digest:MUSIC_PACKAGE.digest}}}),content:async()=>row};
  const href=songHref('workspace-1',{song:'song-1',candidate:'candidate-1',asset:'asset-1',hash:'a'.repeat(64),start:8,end:16});
  assert.equal((await validateMusicReturn(href,'company-1',api)).entry.song,'song-1');
  await assert.rejects(()=>validateMusicReturn(href,'foreign-company',api));
  await assert.rejects(()=>validateMusicReturn(href.replace('music_end=16','music_end=40'),'company-1',api));
});
test('request identity reuses uncertain write; changed basis requires a different original request',()=>{
  const a=stableRequest(null,'save',{'lyrics_ref':'v1'},{text:'x'},()=> 'one');
  assert.equal(stableRequest(a,'save',{'lyrics_ref':'v1'},{text:'x'},()=> 'two'),a);
  assert.equal(stableRequest(a,'save',{'lyrics_ref':'v2'},{text:'x'},()=> 'two').request_id,'two');
  assert.notEqual(draftKey('company','workspace','song-1'),draftKey('company','workspace','song-2'));
});
test('API query is read only and media uses scoped opaque asset route plus auth fetch',async()=>{
  const requests=[],api=createMusicApi(async(...args)=>{requests.push(args);return {};});
  await api.query('company','workspace','song','binding','attempt');await api.media('company','workspace','song','asset');
  assert.equal(requests[0][1],undefined);assert.ok(requests[0][0].endsWith('?attempt_id=attempt'));assert.equal(requests[1][1].responseType,'blob');assert.ok(requests[1][0].endsWith('/songs/song/assets/asset'));
});
test('player position and paused state are independent and bounded for each asset',()=>{
  const memories={'asset-a':{position:12.5,paused:false},'asset-b':{position:8,paused:true}};
  assert.deepEqual(restoredPlayer(memories['asset-a'],32),{position:12.5,paused:false});assert.deepEqual(restoredPlayer(memories['asset-b'],32),{position:8,paused:true});assert.equal(restoredPlayer({position:40,paused:true},32).position,0);
});
test('exact package dispatch refuses drifting digest or schema',()=>{
  const detail={package:{package_id:MUSIC_PACKAGE.id,version:MUSIC_PACKAGE.version,digest:MUSIC_PACKAGE.digest,schema_version:'curis.workspace-package/v1'},instance:{package_id:MUSIC_PACKAGE.id,package_version:MUSIC_PACKAGE.version,package_digest:MUSIC_PACKAGE.digest},schemas:{MusicSong:{schemaVersion:MUSIC_PACKAGE.version}}};
  assert.ok(isMusicPackage(detail));assert.equal(isMusicPackage({...detail,instance:{...detail.instance,package_digest:'foreign'}}),false);
});
test('browser media bytes reject mismatched hash and unqualified rights',async()=>{
  const blob=new Blob(['audio'],{type:'audio/wav'}), hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',await blob.arrayBuffer())),b=>b.toString(16).padStart(2,'0')).join('');
  const a={data:{size:blob.size,sha256:hash,rights:'LOCAL_DESIGN_ONLY',purpose:'NONCOMMERCIAL_ISOLATED_TEST'}};assert.equal(await verifiedAudioBlob(blob,a),blob);
  await assert.rejects(()=>verifiedAudioBlob(blob,{data:{...a.data,sha256:'0'.repeat(64)}}));await assert.rejects(()=>verifiedAudioBlob(blob,{data:{...a.data,rights:'COMMERCIAL'}}));
});

test('Music B3 fixed release and candidate mode return refuses missing foreign or wrong master',async()=>{
 const master={...objectScope,entity_id:'master-old',parent_id:'song-1',data:{kind:'MasterRevision'}};
 const pack={...objectScope,entity_id:'pack-old',parent_id:'song-1',data:{kind:'ReleasePackage',master_ref:master.entity_id}};
 const selected={...row,versions:[...row.versions,master,pack],releases:[pack]};
 const api={collection:async()=>({entry:{scope:objectScope,definition:{package_id:MUSIC_PACKAGE.id,version:MUSIC_PACKAGE.version,digest:MUSIC_PACKAGE.digest}}}),content:async()=>selected};
 const href=songHref('workspace-1',{song:'song-1',release:pack.entity_id,mode:'release'});
 assert.equal((await validateMusicReturn(href,'company-1',api)).entry.release,pack.entity_id);
 for(const changed of [{...selected,releases:[]},{...selected,releases:[{...pack,tenant_id:'foreign'}]},{...selected,versions:selected.versions.filter(v=>v.entity_id!==master.entity_id)}]) await assert.rejects(validateMusicReturn(href,'company-1',{...api,content:async()=>changed}));
 assert.equal(musicReturnTarget(songHref('workspace-1',{song:'song-1',candidate:'candidate-1',mode:'candidates'})).entry.candidate,'candidate-1');
 assert.throws(()=>songHref('workspace-1',{song:'song-1',mode:'unknown'}));
});
