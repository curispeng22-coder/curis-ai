import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import vm from 'node:vm';
import {pathToFileURL} from 'node:url';
const frontendRoot=process.env.CURIS_WRITING_TEST_FRONTEND_ROOT ? pathToFileURL(process.env.CURIS_WRITING_TEST_FRONTEND_ROOT.replace(/\/$/,'')+'/') : new URL('../',import.meta.url);
const bookState=await import(new URL('lib/writingBookState.mjs',frontendRoot));
const writingState=await import(new URL('lib/writingState.mjs',frontendRoot));
const require=createRequire(new URL('package.json',frontendRoot)),React=require('react'),swc=require('next/dist/build/swc');await swc.loadBindings();
const {code}=await swc.transform(readFileSync(process.env.CURIS_TEST_BOOK_MAIN_PREIMAGE||new URL('components/writing/WritingBookMain.js',frontendRoot),'utf8'),{filename:'WritingBookMain.js',isModule:true,jsc:{parser:{syntax:'ecmascript',jsx:true},transform:{react:{runtime:'automatic'}}},module:{type:'commonjs'}});
function scene(api,props){const slots=[],effects=[],storage=new Map();let cursor=0,tree;const same=(a,b)=>a&&b&&a.length===b.length&&a.every((x,i)=>Object.is(x,b[i]));const hooks={useState(initial){const i=cursor++;if(!(i in slots))slots[i]={value:typeof initial==='function'?initial():initial};return [slots[i].value,v=>slots[i].value=typeof v==='function'?v(slots[i].value):v];},useRef(initial){const i=cursor++;return slots[i]||=( {current:initial});},useEffect(fn,deps){const i=cursor++;if(!slots[i]||!same(slots[i].deps,deps)){const old=slots[i];slots[i]={deps};effects.push(()=>{old?.cleanup?.();slots[i].cleanup=fn();});}}};hooks.useLayoutEffect=hooks.useEffect;const m={exports:{}};vm.runInNewContext(code,{module:m,exports:m.exports,crypto:globalThis.crypto,URLSearchParams,sessionStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v),removeItem:k=>storage.delete(k)},require:name=>name==='react'?{...React,...hooks}:name==='react/jsx-runtime'?require(name):name==='next/link'?{__esModule:true,default:p=>React.createElement('a',p,p.children)}:name.endsWith('writingBookState.mjs')?bookState:name.endsWith('writingState.mjs')?writingState:name.endsWith('writingApi.js')?{writingApi:api}:name.endsWith('.module.css')?{__esModule:true,default:new Proxy({},{get:(_,k)=>k})}:{} });const render=()=>{cursor=0;return tree=m.exports.default(props);};return {render,storage,async flush(){render();for(const fn of effects.splice(0))fn();await new Promise(r=>setImmediate(r));return render();},find(predicate){return nodes(render(),predicate)[0];}};}
function nodes(node,p){if(!node||typeof node!=='object')return [];if(Array.isArray(node))return node.flatMap(v=>nodes(v,p));return [...(p(node)?[node]:[]),...nodes(node.props?.children,p)];}
const text=n=>!n?'':typeof n==='string'?n:Array.isArray(n)?n.map(text).join(''):typeof n==='object'?text(n.props?.children):String(n);
function fixture(items=[]){let state={scope:{company_id:'co',workspace_id:'w',book_ref:'b'},context:{setup:{reader:'',genre:'',premise:'',style:'',conflict:''},items},record:null,head_ref:'',chapters:[{ref:'c',title:'第一章'}],read_only:false};const saves=[];const api={bookContext:async()=>state,directions:async()=>({records:[]}),saveBookContext:async(c,w,b,p)=>{saves.push(p);state={...state,context:p.data.context,head_ref:'revision'+saves.length,record:{ref:'revision'+saves.length,revision:saves.length,context:p.data.context}};return state.record;}};return {api,saves,props:{company:'co',workspaceId:'w',book:{ref:'b',title:'原书'},locator:{section:'outline'},onCreateChapter(){},onInspect(){}}};}

test('book locator rejects prototype keys and preserves exact original item/revision',()=>{for(const section of ['__proto__','constructor','toString','missing'])assert.throws(()=>bookState.bookLocator(new URLSearchParams({book_section:section})));const url=bookState.writingBookHref('w','b',{section:'world',item:'world1',context:'original'});assert.match(url,/context_ref=original/);assert.equal(writingState.writingEntry(new URLSearchParams(url.split('?')[1])).bookPosition.item,'world1');});
test('outline order is parent-first, stable with overlapping sibling order; collapse/filter preserve ancestry',()=>{const items=[{id:'node',kind:'node',parent:'chapter',order:0},{id:'chapter',kind:'chapter',parent:'volume',order:0},{id:'outline',kind:'outline',order:0},{id:'volume',kind:'volume',parent:'outline',order:0}];assert.deepEqual(bookState.orderedBookItems(items).map(v=>v.id),['outline','volume','chapter','node']);assert.deepEqual(bookState.orderedBookItems(items,'all',new Set(['volume'])).map(v=>v.id),['outline','volume']);assert.deepEqual(bookState.orderedBookItems(items,'node',new Set(['volume'])).map(v=>v.id),['outline','volume','chapter','node']);});
test('real compiled new-entry form cannot report old context saved; cancellation has explicit restore',async()=>{const f=fixture(),h=scene(f.api,f.props);await h.flush();h.find(n=>n.type==='button'&&text(n)==='＋ 添加世界设定');const add=h.find(n=>n.type==='button'&&text(n)==='＋ 添加全书大纲');add.props.onClick();h.find(n=>n.type==='input'&&n.props.maxLength===160).props.onChange({target:{value:'真实全书'}});assert.equal(h.find(n=>n.type==='button'&&text(n)==='保存作品计划').props.disabled,true);h.find(n=>n.type==='button'&&text(n)==='取消，保留输入').props.onClick();assert.ok(h.find(n=>n.type==='button'&&text(n)==='恢复编辑'));h.find(n=>n.type==='button'&&text(n)==='恢复编辑').props.onClick();assert.equal(h.find(n=>n.type==='input'&&n.props.maxLength===160).props.value,'真实全书');await h.find(n=>n.type==='form'&&n.props.className==='bookItemForm').props.onSubmit({preventDefault(){}});assert.equal(f.saves.length,1);assert.equal(f.saves[0].data.context.items[0].title,'真实全书');assert.equal(f.saves[0].data.context.items[0].kind,'outline');assert.ok(!('chapter_ref' in f.saves[0].data.context.items[0]));});
test('old book shows actual unfiled chapter and setup can be skipped without lazy writes',async()=>{const f=fixture(),h=scene(f.api,f.props);await h.flush();assert.match(text(h.render()),/未归卷 · 可继续写作/);assert.equal(f.saves.length,0);assert.ok(nodes(h.render(),n=>n.props?.href?.includes('chapter_ref=c')).length);});

test('fixed old context ignores retained edits, is read only, and returning restores exact unsaved editor',async()=>{const f=fixture(),original=f.api.bookContext;f.api.bookContext=async(c,w,b,ref)=>ref?{...(await original()),context:{setup:{reader:'历史读者',genre:'',premise:'',style:'',conflict:''},items:[]},record:{ref:'old',revision:1},read_only:true}:original();f.props.locator={section:'setup'};const h=scene(f.api,f.props);await h.flush();nodes(h.render(),n=>n.type==='textarea')[0].props.onChange({target:{value:'未保存新读者'}});await h.flush();const cache=[...h.storage.values()][0];assert.match(cache,/未保存新读者/);f.props.locator={section:'setup',context:'old'};await h.flush();await h.flush();assert.equal(nodes(h.render(),n=>n.type==='textarea')[0].props.value,'历史读者');assert.equal(nodes(h.render(),n=>n.type==='textarea')[0].props.disabled,true);assert.equal([...h.storage.values()][0],cache);assert.equal(f.saves.length,0);f.props.locator={section:'setup'};await h.flush();await h.flush();assert.equal(nodes(h.render(),n=>n.type==='textarea')[0].props.value,'未保存新读者');assert.equal(f.saves.length,0);});

const outline=()=>({id:'outline1',kind:'outline',title:'旧标题',body:'旧正文',goal:'全书目的',order:0,status:'未开始',character_refs:[],world_refs:[],direction_refs:[]});
const editButton=descriptor=>nodes(descriptor.content,n=>n.type==='button'&&text(n)==='编辑这条记录')[0];
test('row Utility follows saved revision and rejects an old callback before a current second save',async()=>{const f=fixture([outline()]),descriptors=[];f.props.onInspect=d=>descriptors.push(d);const h=scene(f.api,f.props);await h.flush();await h.flush();h.find(n=>n.type==='button'&&text(n)==='全书大纲 · 旧标题').props.onClick();await h.flush();const oldEdit=editButton(descriptors.at(-1)).props.onClick;oldEdit();await h.flush();h.find(n=>n.type==='input'&&n.props.maxLength===160).props.onChange({target:{value:'新标题'}});await h.find(n=>n.type==='form'&&n.props.className==='bookItemForm').props.onSubmit({preventDefault(){}});oldEdit();await h.flush();await h.flush();assert.match(text(descriptors.at(-1).content),/新标题/);assert.ok(!h.find(n=>n.type==='form'&&n.props.className==='bookItemForm'),'old callback cannot repopulate a stale row');assert.equal(f.saves.length,1);editButton(descriptors.at(-1)).props.onClick();await h.flush();assert.equal(h.find(n=>n.type==='input'&&n.props.maxLength===160).props.value,'新标题');await h.find(n=>n.type==='form'&&n.props.className==='bookItemForm').props.onSubmit({preventDefault(){}});assert.equal(f.saves[1].expected_ref,'revision1');assert.equal(f.saves[1].data.context.items[0].title,'新标题');});
test('fixed history preserves retained current item input and missing original selection has no latest fallback',async()=>{const f=fixture([outline()]),original=f.api.bookContext,descriptors=[];f.props.onInspect=d=>descriptors.push(d);f.api.bookContext=async(c,w,b,ref)=>ref?{...(await original()),context:{setup:{reader:'历史读者',genre:'',premise:'',style:'',conflict:''},items:[{...outline(),title:'历史原标题'}]},record:{ref:'historic',revision:1,context:{items:[outline()]}},read_only:true}:original();const h=scene(f.api,f.props);await h.flush();await h.flush();h.find(n=>n.type==='button'&&text(n)==='全书大纲 · 旧标题').props.onClick();await h.flush();const stale=editButton(descriptors.at(-1)).props.onClick;stale();await h.flush();h.find(n=>n.type==='input'&&n.props.maxLength===160).props.onChange({target:{value:'未保存当前输入'}});await h.flush();const cache=[...h.storage.values()][0];f.props.locator={section:'outline',item:'outline1',context:'historic'};await h.flush();await h.flush();stale();await h.flush();assert.match(text(descriptors.at(-1).content),/历史原标题/);assert.equal(editButton(descriptors.at(-1)).props.disabled,true);assert.equal([...h.storage.values()][0],cache);assert.equal(f.saves.length,0);f.props.locator={section:'outline',item:'missing-original',context:'historic'};await h.flush();await h.flush();assert.match(text(descriptors.at(-1).content),/原版本中找不到/);assert.equal(editButton(descriptors.at(-1)),undefined);assert.ok(nodes(descriptors.at(-1).content,n=>n.props?.href?.includes('book_item=missing-original')&&n.props.href.includes('context_ref=historic')).length);f.props.locator={section:'outline'};await h.flush();await h.flush();assert.equal(h.find(n=>n.type==='input'&&n.props.maxLength===160).props.value,'未保存当前输入');assert.equal(f.saves.length,0);});
test('old Book edit callback and late save cannot enter another Book with the same item ID',async()=>{const f=fixture([outline()]),original=f.api.bookContext,descriptors=[];f.props.onInspect=d=>descriptors.push(d);f.api.bookContext=async(c,w,b)=>b==='other'?{...(await original()),scope:{company_id:'co',workspace_id:'w',book_ref:'other'},context:{setup:{reader:'',genre:'',premise:'',style:'',conflict:''},items:[{...outline(),title:'另一本书'}]}}:original();const h=scene(f.api,f.props);await h.flush();await h.flush();h.find(n=>n.type==='button'&&text(n)==='全书大纲 · 旧标题').props.onClick();await h.flush();const stale=editButton(descriptors.at(-1)).props.onClick;stale();await h.flush();h.find(n=>n.type==='input'&&n.props.maxLength===160).props.onChange({target:{value:'保存中的本书输入'}});let resolve;f.api.saveBookContext=()=>new Promise(r=>resolve=r);const pending=h.find(n=>n.type==='form'&&n.props.className==='bookItemForm').props.onSubmit({preventDefault(){}});f.props.book={ref:'other',title:'另一本'};await h.flush();await h.flush();stale();resolve({ref:'late-old',context:{setup:{reader:'',genre:'',premise:'',style:'',conflict:''},items:[{...outline(),title:'错误旧返回'}]}});await pending;await h.flush();assert.match(text(h.render()),/另一本书/);assert.ok(!text(h.render()).includes('错误旧返回'));assert.ok(!h.find(n=>n.type==='form'&&n.props.className==='bookItemForm'));});

test('409 keeps input, reads the same Book new head, and late historical/other Book conflicts cannot alter current view',async()=>{for(const navigation of ['stay','history','other']){const f=fixture([outline()]),original=f.api.bookContext;let reads=0,resolve;f.api.bookContext=async(c,w,b,ref)=>{reads++;if(reads===2)return new Promise(r=>resolve=r);const value=await original();return {...value,scope:{...value.scope,book_ref:b},read_only:Boolean(ref)};};f.api.saveBookContext=async()=>{throw Object.assign(new Error('conflict'),{status:409});};const h=scene(f.api,f.props);await h.flush();await h.flush();h.find(n=>n.type==='button'&&text(n)==='编辑').props.onClick();h.find(n=>n.type==='input'&&n.props.maxLength===160).props.onChange({target:{value:'冲突输入保留'}});const pending=h.find(n=>n.type==='form'&&n.props.className==='bookItemForm').props.onSubmit({preventDefault(){}});await new Promise(r=>setImmediate(r));if(navigation==='history')f.props.locator={section:'outline',context:'historic'};if(navigation==='other')f.props.book={ref:'other',title:'另一本'};if(navigation!=='stay'){await h.flush();await h.flush();}resolve({scope:{company_id:'co',workspace_id:'w',book_ref:'b'},head_ref:'new-head'});await pending;await h.flush();await h.flush();const links=nodes(h.render(),n=>n.props?.href?.includes('context_ref=new-head'));if(navigation==='stay'){assert.equal(h.find(n=>n.type==='input'&&n.props.maxLength===160).props.value,'冲突输入保留');assert.equal(links.length,1);assert.equal(f.saves.length,0);}else assert.equal(links.length,0);}});
test('fixed node URL initializes selection once, linked world/person stay in same original revision and return to original node',async()=>{const world={id:'world1',kind:'world',title:'原世界',body:'原规则',order:0},person={id:'person1',kind:'character',title:'原人物',body:'原档案',knowledge:'原知情',order:0},chapter={id:'chapter1',kind:'chapter',title:'原章节',chapter_ref:'c',order:0,world_refs:['world1'],character_refs:['person1']},node={id:'node1',kind:'node',title:'原节点',parent:'chapter1',order:0};const f=fixture([world,person,chapter,node]),original=f.api.bookContext,descriptors=[];f.props.onInspect=d=>descriptors.push(d);f.api.bookContext=async(c,w,b,ref)=>({...await original(),record:{ref:ref||'current',revision:1,context:{items:[world,person,chapter,node]}},read_only:Boolean(ref)});const h=scene(f.api,f.props);await h.flush();await h.flush();h.find(n=>n.type==='button'&&text(n)==='故事节点 · 原节点').props.onClick();await h.flush();const staleLinked=nodes(descriptors.at(-1).content,n=>n.type==='button'&&text(n)==='查看完整原条目')[0].props.onClick;f.props.locator={section:'outline',item:'node1',context:'original-fixed'};await h.flush();await h.flush();const count=descriptors.length;staleLinked();await h.flush();assert.equal(descriptors.length,count);assert.equal(descriptors.at(-1).ref,'node1');for(const target of ['person1','world1']){const current=descriptors.at(-1);const section=nodes(current.content,n=>n.type==='section'&&text(n).includes(target==='world1'?'原世界':'原人物'))[0];nodes(section,n=>n.type==='button'&&text(n)==='查看完整原条目')[0].props.onClick();await h.flush();await h.flush();assert.equal(descriptors.at(-1).ref,target);assert.equal(editButton(descriptors.at(-1)).props.disabled,true);assert.ok(nodes(descriptors.at(-1).content,n=>n.props?.href?.includes('context_ref=original-fixed')&&n.props.href.includes('book_section='+(target==='world1'?'world':'characters'))).length);nodes(descriptors.at(-1).content,n=>n.type==='button'&&text(n)==='返回原定位条目')[0].props.onClick();await h.flush();await h.flush();assert.equal(descriptors.at(-1).ref,'node1');}assert.equal(f.saves.length,0);});
test('foreign Book response is refused without publishing or saving its rows',async()=>{const f=fixture([outline()]),original=f.api.bookContext,descriptors=[];f.props.onInspect=d=>descriptors.push(d);f.api.bookContext=async()=>({...await original(),scope:{company_id:'co',workspace_id:'w',book_ref:'foreign'}});const h=scene(f.api,f.props);await h.flush();await h.flush();assert.match(text(h.render()),/作品结构范围不匹配/);assert.equal(descriptors.length,0);assert.equal(f.saves.length,0);assert.ok(!h.find(n=>n.type==='form'&&n.props.className==='bookItemForm'));});


test('relationship list reads directed endpoints from the saved context and keeps ordinary associations', async () => {
  const people=[{id:'a',kind:'character',title:'甲',order:0},{id:'b',kind:'character',title:'乙',order:1}];
  const relation={id:'r',kind:'relationship',title:'同盟',from_character:'a',to_character:'b',order:0};
  const f=fixture([...people,relation,{...relation,id:'missing',title:'缺失关系',to_character:'absent'}, {...outline(),character_refs:['a','b']}]);
  f.props.locator={section:'characters'};
  const h=scene(f.api,f.props);await h.flush();await h.flush();
  const row=title=>nodes(h.render(),n=>n.type==='tr'&&text(n).includes(title))[0];
  assert.equal(nodes(row('同盟'),n=>n.type==='td')[2].props.children,'甲 → 乙');
  assert.equal(nodes(row('缺失关系'),n=>n.type==='td')[2].props.children,'甲 → 原人物缺失');
  h.find(n=>n.type==='button'&&text(n)==='人物关系 · 同盟').props.onClick();
  nodes(row('同盟'),n=>n.type==='button'&&text(n)==='编辑')[0].props.onClick();
  await h.find(n=>n.type==='form'&&n.props.className==='bookItemForm').props.onSubmit({preventDefault(){}});
  assert.equal(f.saves[0].data.context.items.find(v=>v.id==='r').from_character,'a');
  assert.equal(f.saves[0].data.context.items.find(v=>v.id==='r').to_character,'b');
  f.props.locator={section:'outline'};await h.flush();await h.flush();
  assert.equal(nodes(row('旧标题'),n=>n.type==='td')[2].props.children,'甲、乙');
});

test('explicit inspection opens once; saving and parent creation locks only refresh the current detail', async () => {
  const f=fixture([outline()]),events=[];f.props.onInspect=(descriptor,intent)=>events.push({descriptor,...intent});
  const h=scene(f.api,f.props);await h.flush();await h.flush();
  h.find(n=>n.type==='button'&&text(n)==='全书大纲 · 旧标题').props.onClick();await h.flush();
  assert.equal(events.filter(e=>e.open).length,1);
  // Treat the pane as closed after the first explicit request: later refreshes must not issue another open.
  editButton(events.at(-1).descriptor).props.onClick();await h.flush();
  h.find(n=>n.type==='input'&&n.props.maxLength===160).props.onChange({target:{value:'保存后的标题'}});
  await h.find(n=>n.type==='form'&&n.props.className==='bookItemForm').props.onSubmit({preventDefault(){}});
  await h.flush();await h.flush();
  assert.match(text(events.at(-1).descriptor.content),/保存后的标题/);
  assert.equal(events.filter(e=>e.open).length,1);
  f.props.requestLocked=true;await h.flush();await h.flush();
  assert.equal(editButton(events.at(-1).descriptor).props.disabled,true);
  editButton(events.at(-1).descriptor).props.onClick();await h.flush();
  assert.ok(!h.find(n=>n.type==='form'&&n.props.className==='bookItemForm'));
  f.props.requestLocked=false;await h.flush();await h.flush();
  assert.equal(events.filter(e=>e.open).length,1);
  h.find(n=>n.type==='button'&&text(n)==='全书大纲 · 保存后的标题').props.onClick();
  assert.equal(events.filter(e=>e.open).length,2);
});

test('fixed locator requests initial detail once and every hierarchy row reserves its expander slot', async () => {
  const items=[{...outline(),id:'o',title:'全书'}, {id:'v',kind:'volume',parent:'o',title:'卷',order:0}, {id:'c',kind:'chapter',parent:'v',title:'章',order:0,chapter_ref:'c'}, {id:'n',kind:'node',parent:'c',title:'叶子',order:0}];
  const f=fixture(items),events=[];f.props.locator={section:'outline',item:'n',context:'fixed'};f.props.onInspect=(d,intent)=>events.push({d,...intent});
  const h=scene(f.api,f.props);await h.flush();await h.flush();await h.flush();
  assert.equal(events.filter(e=>e.open).length,1);
  const rows=nodes(h.render(),n=>n.type==='tr'&&typeof n.props['aria-selected']==='boolean');
  assert.deepEqual(rows.map(row=>nodes(row,n=>n.props?.className==='outlineTitle')[0].props.style.paddingLeft),['0px','16px','32px','48px']);
  assert.ok(rows.every(row=>nodes(row,n=>n.props?.className==='outlineExpander').length===1));
  assert.equal(rows[3].props['aria-selected'],true);
  h.find(n=>n.type==='button'&&text(n)==='卷 · 卷').props.onClick();await h.flush();
  assert.equal(nodes(h.render(),n=>n.type==='tr'&&n.props['aria-selected']===true).length,1);
  assert.equal(text(nodes(h.render(),n=>n.type==='tr'&&n.props['aria-selected']===true)[0]).includes('卷 · 卷'),true);
  f.props.requestLocked=true;await h.flush();await h.flush();
  assert.equal(events.filter(e=>e.open).length,2);
  f.props.locator={section:'outline',context:'fixed'};await h.flush();await h.flush();
  f.props.locator={section:'outline',item:'n',context:'fixed'};await h.flush();await h.flush();
  assert.equal(events.filter(e=>e.open).length,3,'explicitly revisiting the same locator opens its detail again');
});

// Keep the mounted hook slots across navigation; passive effects deliberately wait.
const workspaceSource=process.env.CURIS_TEST_WRITING_WORKSPACE_PREIMAGE||new URL('../components/writing/WritingWorkspace.js',import.meta.url);
const {code:workspaceCode}=await swc.transform(readFileSync(workspaceSource,'utf8'),{filename:'WritingWorkspace.js',isModule:true,jsc:{parser:{syntax:'ecmascript',jsx:true},transform:{react:{runtime:'automatic'}}},module:{type:'commonjs'}});
function workspaceScene() {
  const slots=[],passive=[],layout=[],storage=new Map(),calls=[];
  let cursor=0,params=new URLSearchParams({writing_mode:'chapter',book_ref:'a',chapter_ref:'ca'});
  const pkg=writingState.WRITING_PACKAGE;
  const props={workspaceId:'w',detail:{package:{package_id:pkg.id,version:pkg.version,digest:pkg.digest},instance:{company_id:'co',package_id:pkg.id,package_version:pkg.version,package_digest:pkg.digest},schemas:{WritingBook:{schemaVersion:'writing.book/v1'},WritingChapter:{schemaVersion:'writing.chapter/v1'}}}};
  const scope=(company,workspace,book,chapter)=>({company_id:company,workspace_id:workspace,book_ref:book,chapter_ref:chapter,package_id:pkg.id,package_version:pkg.version,package_digest:pkg.digest});
  const api={
    collection:async(company,workspace)=>({scope:scope(company,workspace),books:[{ref:'a',title:'作品 A',status:'DRAFT'},{ref:'b',title:'作品 B',status:'DRAFT'}],chapters:[{ref:'ca',bookRef:'a',title:'章节 A'},{ref:'cb',bookRef:'b',title:'章节 B'}],responsibility:{reason:'本地责任'}}),
    entry:async(company,workspace)=>({scope:scope(company,workspace),pending:[],employees:[],execution:{status:'UNAVAILABLE'}}),
    chapter:async(company,workspace,entry)=>({scope:scope(company,workspace,entry.book,entry.chapter),draft:{ref:'draft-'+entry.chapter,knowledge:[],book_context_basis:{context_ref:'basis-'+entry.chapter,items:[{id:'world-'+entry.chapter,kind:'world',title:'世界-'+entry.chapter,body:'规则-'+entry.chapter}],directions:[]}},responsibility:{reason:'章节责任'},events:[{ref:'event-'+entry.chapter,action:'draft.saved',draft:{text:'正文-'+entry.chapter},created_at:'本地'}]}),
    command:async(...args)=>{calls.push(args);return {};},
  };
  const equal=(a,b)=>a&&b&&a.length===b.length&&a.every((v,i)=>Object.is(v,b[i]));
  const effect=(queue,fn,deps)=>{const i=cursor++;if(!slots[i]||!equal(slots[i].deps,deps)){const old=slots[i];slots[i]={deps};queue.push(()=>{old?.cleanup?.();slots[i].cleanup=fn();});}};
  const hooks={
    useState(initial){const i=cursor++;if(!(i in slots))slots[i]={value:typeof initial==='function'?initial():initial};return [slots[i].value,v=>{slots[i].value=typeof v==='function'?v(slots[i].value):v;}];},
    useRef(initial){const i=cursor++;return slots[i]||=( {current:initial});},
    useCallback(fn,deps){const i=cursor++;if(!slots[i]||!equal(slots[i].deps,deps))slots[i]={deps,value:fn};return slots[i].value;},
    useEffect(fn,deps){effect(passive,fn,deps);},
    useLayoutEffect(fn,deps){effect(layout,fn,deps);},
  };
  const m={exports:{}};
  vm.runInNewContext(workspaceCode,{module:m,exports:m.exports,crypto:globalThis.crypto,URLSearchParams,sessionStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v)},require:name=>{
    if(name==='react')return {...React,...hooks};
    if(name==='react/jsx-runtime')return require(name);
    if(name==='next/navigation')return {useRouter:()=>({push(){}}),useSearchParams:()=>params};
    if(name.endsWith('writingState.mjs'))return writingState;
    if(name.endsWith('writingBookState.mjs'))return bookState;
    if(name.endsWith('writingApi.js'))return {writingApi:api,writingRepairHref:href=>href};
    if(name.endsWith('.module.css'))return {__esModule:true,default:new Proxy({},{get:(_,k)=>k})};
    if(name==='next/link'||name.endsWith('.js'))return {__esModule:true,default:name==='next/link'?'a':name.split('/').at(-1).replace('.js','')};
    throw new Error('Unexpected dependency: '+name);
  }});
  const render=()=>{cursor=0;return m.exports.default(props);};
  const commitLayout=()=>{for(const fn of layout.splice(0))fn();};
  return {calls,api,props,render,commitLayout,
    navigate(query,{company='co',workspace='w'}={}){params=new URLSearchParams(query);props.workspaceId=workspace;props.detail={...props.detail,instance:{...props.detail.instance,company_id:company}};},
    async flush(){render();commitLayout();for(const fn of passive.splice(0))fn();await new Promise(resolve=>setImmediate(resolve));return render();},
  };
}
const chapterNode=tree=>nodes(tree,n=>['WritingChapterMain','WritingPublishingMain'].includes(n.type))[0];
const basisTab=tree=>tree.props.utilityTabs.find(tab=>tab.id==='basis').content;
const versionsTab=tree=>tree.props.utilityTabs.find(tab=>tab.id==='versions').content;
const basisLinks=tree=>nodes(basisTab(tree),n=>typeof n.props?.href==='string'&&n.props.href.includes('context_ref='));

for(const transition of [
  {name:'library',query:{}},
  {name:'another book',query:{writing_mode:'books',book_ref:'b'}},
  {name:'another book chapter',query:{writing_mode:'chapter',book_ref:'b',chapter_ref:'cb'}},
  {name:'company mismatch',query:{writing_mode:'chapter',book_ref:'a',chapter_ref:'ca'},scope:{company:'other'}},
  {name:'workspace mismatch',query:{writing_mode:'chapter',book_ref:'a',chapter_ref:'ca'},scope:{workspace:'other'}},
]) test('compiled mounted workspace isolates retained chapter before effects: '+transition.name,async()=>{
  const h=workspaceScene();await h.flush();await h.flush();
  let tree=h.render();const oldChapter=chapterNode(tree);assert.ok(oldChapter);
  assert.equal(basisLinks(tree).length,1);assert.match(basisLinks(tree)[0].props.href,/book_ref=a.*context_ref=basis-ca/);
  oldChapter.props.onDetails('versions');tree=h.render();assert.equal(tree.props.utilityRequestTabId,'versions');
  h.navigate(transition.query,transition.scope);
  // Render without flushing either effect queue: old chapter and collection are still mounted.
  tree=h.render();
  assert.equal(chapterNode(tree),undefined,'old chapter cannot become the new route command target');
  assert.equal(basisLinks(tree).length,0,'old basis cannot be relinked to the destination');
  assert.ok(!text(versionsTab(tree)).includes('正文-ca'),'old version content is hidden');
  h.commitLayout();
  await assert.rejects(oldChapter.props.command('draft.save',{text:'不得发出'},'stale-request'),/章节已切换/);
  assert.equal(h.calls.length,0,'retained command never sends to a different route');
  await h.flush();await h.flush();tree=h.render();
  if(transition.query.writing_mode==='chapter'){
    const current=chapterNode(tree);assert.ok(current);
    assert.equal(current.props.state.scope.company_id,transition.scope?.company||'co');
    assert.equal(current.props.state.scope.workspace_id,transition.scope?.workspace||'w');
    assert.equal(current.props.state.scope.book_ref,transition.query.book_ref);
    assert.equal(current.props.state.scope.chapter_ref,transition.query.chapter_ref);
    const href=basisLinks(tree)[0].props.href;
    assert.ok(href.includes('book_ref='+transition.query.book_ref));
    assert.ok(href.includes('context_ref=basis-'+transition.query.chapter_ref));
    assert.ok(!href.includes('undefined'));
  }else assert.equal(chapterNode(tree),undefined);
});

test('compiled mounted workspace retains exact chapter basis across same-scope review/package and current commands',async()=>{
  const h=workspaceScene();await h.flush();await h.flush();
  for(const mode of ['review','package','chapter']){
    h.navigate({writing_mode:mode,book_ref:'a',chapter_ref:'ca'});
    const tree=h.render(),child=chapterNode(tree);assert.ok(child);
    assert.equal(child.props.state.scope.chapter_ref,'ca');
    assert.match(basisLinks(tree)[0].props.href,/book_ref=a.*context_ref=basis-ca/);
    assert.match(text(versionsTab(tree)),/正文-ca/);
    await h.flush();await h.flush();
  }
  const tree=h.render();await chapterNode(tree).props.command('draft.save',{text:'当前章节'},'current-request');
  assert.equal(h.calls.length,1);assert.equal(h.calls[0][0],'co');assert.equal(h.calls[0][1],'w');
  assert.equal(h.calls[0][2].book,'a');assert.equal(h.calls[0][2].chapter,'ca');
  assert.equal(h.calls[0][4].expected_draft_ref,'draft-ca');
});

for(const scope of [{company:'other'},{workspace:'other'}]) test('compiled mounted workspace hides foreign library before effects: '+Object.keys(scope)[0],async()=>{
  const h=workspaceScene();await h.flush();await h.flush();
  assert.match(text(h.render().props.contextPane),/作品 A/);
  h.navigate({},scope);
  const tree=h.render();
  for(const region of [tree,tree.props.contextPane]){
    assert.ok(!/作品 A|作品 B|章节 A|章节 B/.test(text(region)),'foreign library titles are hidden before effect cleanup');
    assert.equal(nodes(region,n=>typeof n.props?.href==='string'&&/[?&](book_ref|chapter_ref)=/.test(n.props.href)).length,0,'foreign object links are hidden');
  }
  assert.equal(chapterNode(tree),undefined);assert.equal(basisLinks(tree).length,0);
  assert.equal(nodes(tree,n=>n.type==='button'&&text(n)==='＋ 新建作品').length,0,'old collection cannot enable creation in the new scope');
  await h.flush();await h.flush();
  const loaded=h.render();assert.match(text(loaded),/作品 A/);
  assert.equal(nodes(loaded,n=>n.type==='button'&&text(n)==='＋ 新建作品').length,1);
  assert.equal(h.calls.length,0);
});
