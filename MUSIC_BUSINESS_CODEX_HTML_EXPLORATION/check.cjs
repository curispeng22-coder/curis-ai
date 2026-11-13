const assert=require('node:assert/strict'),m=require('./model.js'),seed=require('./data.js');
const s=structuredClone(seed),song=m.song(s,'night');
assert.throws(()=>m.pack(s,'night'));m.approve(s,'night','B');m.pack(s,'night');
assert.equal(song.release.master,'B');m.release(s,'night','submit');assert.equal(song.release.status,'waiting_user');
assert.throws(()=>m.release(s,'night','publish'));m.release(s,'night','resume');m.release(s,'night','unknown');
assert.throws(()=>m.release(s,'night','submit'));m.release(s,'night','verify');assert.equal(song.release.status,'published');
const frozenLyrics=song.release.lyrics;song.lyrics='新的歌词';assert.equal(song.release.lyrics,frozenLyrics);song.lyricVersion++;assert.throws(()=>m.approve(s,'night','A'));const v=m.generate(s,'night','改副歌');m.approve(s,'night',v);
assert.equal(song.release.master,'B');assert.throws(()=>m.release(s,'night','submit'));
m.pack(s,'night');assert.equal(song.releaseHistory[0].master,'B');assert.equal(song.releaseHistory[0].status,'published');
const next=m.create(s,{intent:'下一首',learning:'learn-1'});assert.equal(s.learnings[0].applications[0].song,next.id);assert.notEqual(next.id,song.id);
console.log('PASS: Master/version guards, release handoff/unknown recovery, learning-to-next-song lineage.');

// R1–R4: scope isolation, non-expert entry, acceptance gate and immutable Song input.
const vm=require('node:vm'),fs=require('node:fs');
const draftState=structuredClone(seed),context={state:draftState,document:{addEventListener(){}},structuredClone,MusicModel:m,model:m,save(){},render(){},toast(){},navigate(){},current(){return draftState.songs[0];}};
vm.createContext(context);vm.runInContext(fs.readFileSync(__dirname+'/direction.js','utf8'),context);
context.initResearch();assert.equal(context.snapshots().length,3);draftState.watches[0].revision=2;assert.equal(context.snapshots().length,0);draftState.watches[0].revision=1;
draftState.directionInput='';draftState.creativeInput.tags=['开车','松弛'];context.proposeDirection();assert.match(draftState.directionDraft.summary,/开车/);assert.match(draftState.directionDraft.summary,/松弛/);
const count=draftState.songs.length;context.handleDirectionAction('create-song',{});assert.equal(draftState.songs.length,count);
const accepted=draftState.directionDraft;accepted.status='accepted';accepted.reason='以场景为依据';accepted.evidence={reason:'模拟变化',times:['早','晚']};context.handleDirectionAction('create-song',{});assert.equal(draftState.songs.length,count+1);accepted.evidence.reason='changed';assert.equal(draftState.songs.at(-1).directionArtifact.evidence.reason,'模拟变化');assert.equal(draftState.songs.at(-1).candidates.length,0);
console.log('PASS: research scope versions, guided-only intent, acceptance gate, immutable Direction input; no automatic production.');

vm.runInContext(fs.readFileSync(__dirname+'/business.js','utf8'),context);context.initBusiness();
assert.equal(context.styleDistribution(5).reduce((sum,x)=>sum+x[1],0),10);
const originalMetric=structuredClone(draftState.metrics[0]);draftState.metrics.push({...originalMetric,plays:99,share:9});assert.equal(context.metricRows({metricPlatform:'汽水音乐'})[0].plays,99);assert.equal(context.metricRows({metricPlatform:'汽水音乐'}).length,1);
assert.equal(context.totalKnown([{share:null}],'share',true),'未知');assert.match(context.totalKnown([{share:0},{share:null}],'share',true),/未知/);
const tide=m.song(draftState,'tide');assert.equal(context.publicationStatus(tide,'汽水音乐'),'已发布');assert.equal(context.publicationStatus(tide,'YouTube'),'待发布');tide.master='M2';assert.equal(context.publicationStatus(tide,'汽水音乐'),'待发布');assert.equal(draftState.publications[0].master,'M1');
draftState.metricPlatform='不存在的平台';assert.equal(context.metricRows().length,0);assert.equal(context.metricRows({}).length,2);
console.log('PASS: monthly latest-record dedup, unknown versus zero, platform/Master scope, independent overview totals, style sample count.');

vm.runInContext(fs.readFileSync(__dirname+'/market-intelligence.js','utf8'),context);
const watch=context.musicWatch(),marketHistory=context.musicSnapshots(watch),marketChanges=context.musicChangeRows(marketHistory[0],marketHistory[2]);
assert.equal(marketHistory.length,3);
assert.equal(marketChanges.find(x=>x.row.id==='ref-night').change[1],'up');
assert.equal(marketChanges.find(x=>x.row.id==='ref-window').change[1],'new');
assert.equal(marketChanges.find(x=>x.row.id==='ref-road').change[1],'down');
assert.equal(context.musicChangeRows(marketHistory[2],marketHistory[0]).length,0);
watch.revision++;assert.equal(context.musicSnapshots(watch).length,0);watch.revision--;
console.log('PASS: same-scope snapshot history, directional change, new discovery, and reversed-time guard.');

// Team collaboration: independent candidates, immutable pool versions and guarded direct creation.
vm.runInContext(fs.readFileSync(__dirname+'/team.js','utf8'),context);context.initTeam();
draftState.directionInput='旅行';context.proposeDirection();context.prepareOptions();
const opts=draftState.directionDraft.options;opts[1].audience='自驾听众';assert.notEqual(opts[0].audience,opts[1].audience);
context.poolSave(opts[1]);const poolCopy=structuredClone(draftState.directionPool[0]);opts[1].summary='修订内容';assert.equal(draftState.directionPool[0].summary,poolCopy.summary);opts[1].revision++;context.poolSave(opts[1]);assert.equal(draftState.directionPoolHistory[0].summary,poolCopy.summary);
const direct=m.create(draftState,{intent:'直接创作',title:'直接创作检查'});direct.directionPending=true;assert.throws(()=>m.generate(draftState,direct.id));direct.directionPending=false;direct.learningWork='只采用短动机技巧';const oldDirection=direct.direction;m.generate(draftState,direct.id,'制作');assert.match(direct.candidates[0].desc,/只采用短动机技巧/);assert.equal(direct.direction,oldDirection);
console.log('PASS: independent candidate positioning, persisted immutable revision history, direct-song direction gate, selective learning in work input.');

// Layout regression: chat content must not inherit the horizontal Employee identity row.
context.esc=x=>String(x??'');context.btn=(label)=>'<button>'+label+'</button>';context.badge=()=>'';
const chatHtml=context.creativeConversation();assert.equal((chatHtml.match(/id="employee-input"/g)||[]).length,1);assert.ok(!chatHtml.includes('class="thread-message agent"'));assert.ok(!chatHtml.includes('proposal-list'));
context.location={hash:'#overview'};vm.runInContext(fs.readFileSync(__dirname+'/app.js','utf8').split('\n').find(x=>x.startsWith('function navigate(')),context);context.navigate('direction');assert.equal(context.location.hash,'research');assert.equal(draftState.marketView,'direction');context.location.hash='#research';context.navigate('reference');assert.equal(context.location.hash,'#research');assert.equal(draftState.marketView,'reference');
console.log('PASS: one chat composer, isolated message styles, candidates outside chat column, flat market/reference/direction navigation.');

// Song-specific conversation must not mutate the business research draft.
context.cover=()=>'';context.tags=()=>'';context.candidate=()=>'<article>audio</article>';
draftState.workPage='song';context.current=()=>direct;direct.directionPending=true;direct.intentTags=['长途旅行','松弛'];
const marketBefore=JSON.stringify(draftState.directionDraft);
context.$=selector=>selector==='#work-message'?{value:'想用木吉他做旅行的歌'}:null;
context.handleSongAction('work-send',{});
assert.equal(direct.songProposals.length,3);assert.equal(direct.songProposals[0].status,'candidate');
assert.equal(JSON.stringify(draftState.directionDraft),marketBefore);
assert.equal((context.song().match(/id="work-message"/g)||[]).length,1);
assert.ok(!context.song().includes('id="lyrics"'));assert.ok(!context.songDetails().includes('id="work-message"'));
direct.songFocus=1;const acceptedText=direct.songProposals[1].summary;
context.$=selector=>selector==='#song-proposal-edit'?{value:acceptedText}:null;
context.handleSongAction('song-confirm',{});
assert.equal(direct.directionPending,false);assert.equal(direct.directionArtifact.status,'accepted');
assert.ok(direct.directionArtifact.tags.includes('木吉他'));assert.equal(direct.directionChoices.length,3);
const directionBefore=direct.direction,versionsBefore=direct.candidates.length;
context.$=selector=>selector==='#work-message'?{value:'把鼓点减轻'}:null;
context.handleSongAction('work-send',{});context.handleSongAction('song-run-revision',{});
assert.equal(direct.direction,directionBefore);assert.equal(direct.candidates.length,versionsBefore+1);
console.log('PASS: Song-scoped suggestions, one main composer, pre-production gate, confirmed context, additive revision.');

context.$=()=>({open:false});context.close=()=>{};
const named=context.createFromDirection({...direct.directionArtifact,title:'原方向名称'},'独立歌曲名称');
assert.equal(named.title,'独立歌曲名称');assert.equal(named.directionArtifact.title,'原方向名称');
console.log('PASS: Song title remains separate from accepted Direction identity.');
// Visible quick choices toggle without losing the Song discussion draft.
direct.directionPending=true;direct.intentTags=[];context.current=()=>direct;
context.songThread().draft='保留这句想法';
context.handleSongAction('song-quick-tag',{dataset:{value:'开车'}});
assert.deepEqual(Array.from(direct.intentTags),['开车']);
assert.equal(context.songThread().draft,'保留这句想法');
context.handleSongAction('song-quick-tag',{dataset:{value:'开车'}});
assert.equal(direct.intentTags.length,0);
const startHtml=context.song();
assert.ok(startHtml.indexOf('id="work-message"')<startHtml.indexOf('常用创作偏好'));
assert.ok(startHtml.indexOf('常用创作偏好')<startHtml.indexOf('song-discussion'));
assert.equal((startHtml.match(/id="work-message"/g)||[]).length,1);
console.log('PASS: visible guided entry, toggle round trip, retained draft, single top composer.');
