import assert from 'node:assert/strict';
import test from 'node:test';
import {displayScene as scene,nodes,text} from './uxComponentHarness.mjs';
test('Talent real search receives explicit label through actual TerraSearch and retains filtering input',async()=>{
 const s=scene();s.setRoot(s.load('talent').TalentMarketSurface,{companyId:'A'});await s.settle();let input=s.input('搜索专家或能力关键词');assert.ok(input);input.props.onChange({target:{value:'测试'}});s.render();assert.equal(s.input('搜索专家或能力关键词').props.value,'测试');
 const skills=nodes(s.tree,n=>n.type==='button'&&text(n).trim().startsWith('技能'))[0];assert.ok(skills);skills.props.onClick();s.render();assert.ok(s.input('搜索技能或能力关键词'));assert.equal(s.input('搜索技能或能力关键词').props.value,'');
});
test('optional TerraSearch label leaves unconfigured consumers and controlled/uncontrolled behavior intact',()=>{
 const s=scene(),changes=[];s.setRoot(s.load('terra').TerraSearch,{placeholder:'原搜索',onChange:v=>changes.push(v)});s.render();let input=nodes(s.tree,n=>n.type==='input')[0];assert.equal(input.props['aria-label'],undefined);input.props.onChange({target:{value:'内容'}});s.render();assert.equal(nodes(s.tree,n=>n.type==='input')[0].props.value,'内容');assert.equal(changes[0],'内容');
});
test('Meeting search has explicit name and updates query without starting a meeting',async()=>{
 const s=scene();s.setRoot(s.load('meeting').MeetingSurface,{});await s.settle();const input=s.input('搜索会议议题');assert.ok(input);input.props.onChange({target:{value:'议题'}});s.render();assert.equal(s.input('搜索会议议题').props.value,'议题');assert.match(text(s.tree),/当前没有进行中的会议/);assert.equal(s.counts.objects,0);
});
