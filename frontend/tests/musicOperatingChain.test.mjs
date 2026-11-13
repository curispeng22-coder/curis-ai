import test from 'node:test';
import assert from 'node:assert/strict';
import {manualNumber,observationComparison,musicScopedRead,operatingHref,musicReturnTarget,musicOperatingEntry,operatingDraftKey,MUSIC_PACKAGES,isMusicPackage,stableRequest,songHref} from '../lib/musicState.mjs';
import {validateMusicReturn} from '../lib/musicApi.js';
const observed = (value, start='2026-10-01',end='2026-10-02', changes={}) => ({song_ref:'song-A',master_ref:'master-A',platform:'platform-A',account:'account-A',metric:'plays',definition:'specified plays',unit:'次',currency:null,coverage:'same sample',method:'manual',value,period:{start,end,timezone:'Asia/Shanghai'},...changes});
test('song directory has an explicit route distinct from the operating landing, old song links stay exact',()=>{
 assert.equal(musicReturnTarget(songHref('workspace-1')).operating.view,'songs');
 assert.equal(songHref('workspace-1',{song:'song-1'}),'/ceo-office/workspace/installed/workspace-1?music_song=song-1');
 assert.notEqual(songHref('workspace-1'),operatingHref('workspace-1',{view:'operating'}));
});
test('unknown differs from actual zero and no guessed growth',()=>{
 assert.equal(manualNumber(''),null);assert.equal(manualNumber('0'),0);assert.throws(()=>manualNumber(' '));assert.throws(()=>manualNumber('-1'));
 const comparison=observationComparison(observed(0),observed(100,'2026-10-02','2026-10-03'));assert.equal(comparison.eligible,true);assert.equal(comparison.difference,100);assert.equal(comparison.percent,null);
 for(const changes of [{value:null},{account:null},{master_ref:'other'},{song_ref:'other'},{unit:'人'},{definition:'other'},{coverage:'other'}])assert.equal(observationComparison(observed(0),observed(100,'2026-10-02','2026-10-03',changes)).eligible,false);
 assert.equal(observationComparison(observed(0),observed(100)).eligible,false);
});
test('Music B3 original object/version/period and song scene return exact, foreign object blocked',async()=>{
 const href=operatingHref('workspace-1',{view:'performance',object:'music-obs-B',period:'2026-10-01|2026-10-02|Asia/Shanghai',song:'music-song-B'});
 const parsed=musicReturnTarget(href);assert.equal(parsed.operating.object,'music-obs-B');assert.equal(parsed.entry.song,'music-song-B');assert.equal(parsed.operating.period,'2026-10-01|2026-10-02|Asia/Shanghai');
 assert.ok(musicOperatingEntry(new URLSearchParams('music_view=learning&music_view=market')).error);
 assert.throws(()=>operatingHref('workspace-1',{view:'learning',object:'../fake'}));
 const p=MUSIC_PACKAGES[0],record={tenant_id:'tenant-1',entity_id:'music-obs-B',company_id:'company-1',workspace_id:'workspace-1',data:{kind:'Observation'}};
 const api={collection:async()=>({entry:{scope:{tenant_id:'tenant-1',company_id:'company-1',workspace_id:'workspace-1'},definition:{package_id:p.id,version:p.version,digest:p.digest}}}),operatingContent:async()=>({record}),content:async()=>({song:{tenant_id:'tenant-1',entity_id:'music-song-B',company_id:'company-1',workspace_id:'workspace-1'},versions:[]})};
 assert.equal((await validateMusicReturn(href,'company-1',api)).href,href);
 await assert.rejects(validateMusicReturn(href,'company-1',{...api,operatingContent:async()=>({record:{...record,company_id:'foreign'}})}));
 await assert.rejects(validateMusicReturn(href,'company-1',{...api,operatingContent:async()=>({record:{...record,data:{kind:'Learning'}}})}));
});
test('finite exact old and new package identity, actor/version draft isolation',()=>{
 for(const p of MUSIC_PACKAGES){const d={package:{package_id:p.id,version:p.version,digest:p.digest,schema_version:'curis.workspace-package/v1'},instance:{package_id:p.id,package_version:p.version,package_digest:p.digest},schemas:{MusicSong:{schemaVersion:p.version}}};assert.ok(isMusicPackage(d));assert.equal(isMusicPackage({...d,package:{...d.package,digest:'foreign'}}),false);}
 assert.notEqual(operatingDraftKey('c','w','actor1','Learning','version1'),operatingDraftKey('c','w','actor1','Learning','version2'));
 assert.notEqual(operatingDraftKey('c','w','actor1','Learning','version1'),operatingDraftKey('c','w','actor2','Learning','version1'));
});
test('same creation intent stays stable, second explicit intent differs',()=>{
 let n=0;const data={title:'first',draft_revision:'original-intent'},a=stableRequest(null,'create-song',{},data,()=>String(++n));
 assert.equal(stableRequest(a,'create-song',{},data,()=>String(++n)).request_id,a.request_id);
 assert.notEqual(stableRequest(a,'create-song',{}, {...data,title:'second',draft_revision:'second-intent'},()=>String(++n)).request_id,a.request_id);
});

test('Music B3 scoped reads preserve exact legacy definition and reject foreign rows or changed digest',()=>{
 for(const p of MUSIC_PACKAGES){const d={package_id:p.id,version:p.version,digest:p.digest},entry={scope:{tenant_id:'t',company_id:'c',workspace_id:'w'},definition:d};const payload={entry,records:[{tenant_id:'t',company_id:'c',workspace_id:'w'}]};assert.equal(musicScopedRead(payload,'c','w',d),payload);assert.throws(()=>musicScopedRead({...payload,records:[{tenant_id:'foreign',company_id:'c',workspace_id:'w'}]},'c','w',d));assert.throws(()=>musicScopedRead({...payload,entry:{...entry,definition:{...d,digest:'foreign'}}},'c','w',d));}
 const href=operatingHref('w',{view:'release',song:'song-A',release:'pack-A'});assert.equal(musicReturnTarget(href).entry.release,'pack-A');assert.equal(musicReturnTarget(href).operating.view,'release');
});


test('two-candidate return preserves original song, candidates and operating period',()=>{
 const href=songHref('workspace-1',{song:'song-A',candidate:'candidate-A',compare:'candidate-B',mode:'candidates',period:'2026-10-01|2026-10-02|Asia/Shanghai'});
 const target=musicReturnTarget(href);assert.equal(target.entry.candidate,'candidate-A');assert.equal(target.entry.compare,'candidate-B');assert.equal(target.operating.period,'2026-10-01|2026-10-02|Asia/Shanghai');
 assert.throws(()=>musicReturnTarget(href+'&music_compare=foreign'));
});
