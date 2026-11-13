import assert from 'node:assert/strict';
import test from 'node:test';
import {displayScene as scene,nodes,text} from './uxComponentHarness.mjs';
async function library(storage={}){
 const s=scene({storage}),p=s.load('writingState').WRITING_PACKAGE;
 s.setRoot(s.load('writing').default,{workspaceId:'W',detail:{package:{package_id:p.id,version:p.version,digest:p.digest},instance:{company_id:'A',package_id:p.id,package_version:p.version,package_digest:p.digest},schemas:{WritingBook:{schemaVersion:'writing.book/v1'},WritingChapter:{schemaVersion:'writing.chapter/v1'}}}});await s.settle();return s;
}
test('DIAGNOSTIC: cancel after empty-title validation removes only local new-book error',async()=>{
 const s=await library();s.button('新建第一部作品').props.onClick();s.render();const form=nodes(s.tree,n=>n.type==='form')[0];form.props.onSubmit({preventDefault(){}});s.render();assert.match(text(s.tree),/请填写作品名称/);s.button('取消').props.onClick();s.render();assert.equal(s.input('作品名称'),undefined);assert.equal(s.counts.objects,0);assert.doesNotMatch(text(s.tree),/请填写作品名称/);
});
test('cancel must retain persisted creation UNKNOWN and refuse another object write',async()=>{
 const key='curis.writing.creation-unknown.A:W',s=await library({[key]:'pending'});s.button('新建第一部作品').props.onClick();s.render();s.input('作品名称').props.onChange({target:{value:'合法标题'}});s.render();nodes(s.tree,n=>n.type==='form')[0].props.onSubmit({preventDefault(){}});s.render();s.button('取消').props.onClick();s.render();assert.match(text(s.tree),/原创建结果待核对/);assert.equal(s.storage.get(key),'pending');assert.equal(s.counts.objects,0);
});
test('local title validation is attached to the input and clears on editing without global retry copy',async()=>{
 const s=await library();s.button('新建第一部作品').props.onClick();s.render();nodes(s.tree,n=>n.type==='form')[0].props.onSubmit({preventDefault(){}});s.render();const input=s.input('作品名称');assert.equal(input.props['aria-invalid'],true);const id=input.props['aria-describedby'];assert.ok(id);assert.equal(nodes(s.tree,n=>n.props?.id===id&&n.props.role==='alert').length,1);assert.doesNotMatch(text(s.tree),/核对来源后重试/);input.props.onChange({target:{value:'新标题'}});s.render();assert.equal(s.input('作品名称').props['aria-invalid'],false);assert.doesNotMatch(text(s.tree),/请填写作品名称/);assert.equal(s.counts.objects,0);
});
test('cancelling after a simulated remote unknown preserves the error, stored receipt and creation lock',async()=>{
 const s=await library();s.button('新建第一部作品').props.onClick();s.render();s.input('作品名称').props.onChange({target:{value:'新标题'}});s.render();nodes(s.tree,n=>n.type==='form')[0].props.onSubmit({preventDefault(){}});await s.settle();assert.equal(s.counts.objects,1);assert.match(text(s.tree),/原创建结果未确定/);s.button('取消').props.onClick();s.render();assert.match(text(s.tree),/原创建结果未确定/);assert.ok(s.storage.get('curis.writing.creation-unknown.A:W'));s.button('新建第一部作品').props.onClick();s.render();nodes(s.tree,n=>n.type==='form')[0].props.onSubmit({preventDefault(){}});await s.settle();assert.equal(s.counts.objects,1);
});

function publishing(entry={}){
 const s=scene(),events=[{action:'formal.confirmed',ref:'F2',created_at:'2026-10-26 00:00:01',snapshot:{text:'第二稿'}},{action:'formal.confirmed',ref:'F1',created_at:'2026-10-25 21:41:49',snapshot:{text:'第一稿'}},{action:'package.prepared',ref:'P1',formal_ref:'F1',created_at:'2026-10-25 22:00:00',package:{metadata:{introduction:'介绍',credits:'作者'}}}],state={scope:{company_id:'A'},events},original=JSON.stringify(state),navigation=[];
 const props={state,entry,workspaceId:'W',command:()=>{throw Error('No command permitted in display test');},busy:false,onNavigate:v=>navigation.push(v)};
 s.setRoot(s.load('publishing').default,props);s.render();return{s,events,state,original,navigation};
}
test('formal options, fallback choices and package history label known UTC without changing refs or order',()=>{
 const {s,events,state,original,navigation}=publishing();
 const options=nodes(s.tree,n=>n.type==='option'&&n.props.value);
 assert.deepEqual(options.map(n=>n.props.value),['F2','F1']);assert.match(text(options[0]),/2026-10-26 00:00:01 UTC/);assert.match(text(options[1]),/2026-10-25 21:41:49 UTC/);
 const fallback=nodes(s.tree,n=>n.type==='button'&&text(n).startsWith('选择正式稿'));assert.equal(fallback.length,2);assert.ok(fallback.every(n=>text(n).endsWith('UTC')));fallback[1].props.onClick();assert.equal(navigation[0].formal,'F1');assert.equal(navigation[0].package,'');
 const history=nodes(s.tree,n=>n.type==='button'&&text(n).startsWith('打开发布包'))[0];assert.match(text(history),/22:00:00 UTC/);history.props.onClick();assert.equal(navigation[1].package,'P1');assert.equal(navigation[1].formal,'F1');
 assert.equal(JSON.stringify(state),original);assert.equal(events[1].created_at,'2026-10-25 21:41:49');
});
test('selected formal snapshot and navigation stay anchored to the original ref',()=>{const {s,navigation,state,original}=publishing({formal:'F1'});assert.match(text(s.tree),/第一稿/);assert.doesNotMatch(text(s.tree),/第二稿/);s.input('已确认正式稿版本').props.onChange({target:{value:'F2'}});assert.equal(navigation[0].formal,'F2');assert.equal(JSON.stringify(state),original);});
test('unknown/invalid timestamp strings are preserved without inventing UTC; missing time stays explicit',()=>{
 const f=scene().load('publishing').writingEventTime;assert.equal(typeof f,'function');for(const v of ['2026-02-30 01:00:00','2026-10-26 24:01:00','unknown','2026-10-26T05:41:49+08:00','2026-10-25T21:41:49Z'])assert.equal(f(v),v);assert.equal(f('2024-02-29 00:00:00'),'2024-02-29 00:00:00 UTC');assert.equal(f(null),'时间未记录');
});
