import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import vm from 'node:vm';
const require=createRequire(import.meta.url),React=require('react'),swc=require('next/dist/build/swc');
const {renderToStaticMarkup}=require('react-dom/server'),parser=require('next/dist/compiled/babel/parser');
const read=(p)=>readFileSync(new URL('../'+p,import.meta.url),'utf8');
await swc.loadBindings();
const {code}=await swc.transform(read('components/v1/BusinessCatalogSurface.js'),{filename:'catalog.js',jsc:{parser:{syntax:'ecmascript',jsx:true},transform:{react:{runtime:'automatic'}}},module:{type:'commonjs'}});
const module={exports:{}};
vm.runInNewContext(code,{module,exports:module.exports,URLSearchParams,require:(name)=>{
 if(['react','react/jsx-runtime'].includes(name))return require(name);
 if(name==='next/link')return{__esModule:true,default:(props)=>React.createElement('a',props)};
 if(name==='next/image')return{__esModule:true,default:()=>null};
 if(name.includes('runtimeApi'))return{workspaceOfficeHref:(w)=>'/installed/'+encodeURIComponent(w.workspace_id)};
 if(name.endsWith('.css'))return{__esModule:true,default:{}};
 if(name.endsWith('.png'))return{__esModule:true,default:{src:'fixture'}};
 return{TerraIcon:()=>null};
}});
const Catalog=module.exports.default,company={company_id:'A',name:'测试公司'};
const render=(businesses,definitions=null)=>renderToStaticMarkup(React.createElement(Catalog,{company,businesses,organization:null,definitions,definitionStatus:'ready',selection:{kind:'directory'}}));
const business=(id,packageId='com.curis.local.writing-authoring',version='v1')=>({business_id:id,company_id:'A',name:'自定义 '+id,workspaces:[{workspace_id:'w/'+id,name:'明确空间 '+id,business_type:'PACKAGE',package_id:packageId,package_version:version}]});
function find(source,predicate){const tree=parser.parse(source,{sourceType:'module',plugins:['jsx']});let found;function walk(node){if(!node||typeof node!=='object'||found)return;if(predicate(node)){found=node;return;}for(const value of Object.values(node))for(const child of Array.isArray(value)?value:[value])walk(child);}walk(tree);assert.ok(found);return source.slice(found.start,found.end);}

test('zero, one, many: all three directions stay above the complete instance list, exact installed versions only',()=>{
 for(const rows of [[],[business('one')],[business('one'),business('two'),business('music','com.curis.local.music'),business('cg','com.curis.local.content-growth'),business('unknown','other'),business('broken',null,42)]]){
  const html=render(rows);assert.ok(html.indexOf('内容增长 · 写作 · 音乐')<html.indexOf('当前业务'));
  for(const direction of ['写作','内容增长','音乐'])assert.ok(html.includes(direction));
  for(const row of rows)assert.ok(html.includes('/installed/w%2F'+row.business_id));
  assert.equal(html.includes('进入 自定义 unknown'),false);assert.equal(html.includes('进入 自定义 broken'),false);
  assert.equal(html.includes('new=1&amp;source_definition='),false);
 }
 const html=render([business('one'),business('two')]);assert.ok(html.includes('进入 自定义 one'));assert.ok(html.includes('进入 自定义 two'));assert.equal(html.includes('已安装 v1'),false);assert.ok(html.includes('明确空间 one'));assert.ok(html.includes('明确空间 two'));
 assert.equal(render([{...business('foreign'),company_id:'B'}]).includes('自定义 foreign'),false);
});

test('actual package redirect requires exact company, workspace and resolved business parent',()=>{
 const source=read('app/ceo-office/workspace/page.js');
 const effect=find(source,(n)=>n.type==='ArrowFunctionExpression'&&source.slice(n.start,n.end).includes('router.replace(workspaceOfficeHref(workspace))'));
 const good={status:'ready',detail:{workspace:{workspace_id:'W',company_id:'A',business_id:'B',business_type:'PACKAGE'}},parent:{status:'RESOLVED',parentPath:{company:{company_id:'A'},workspace:{workspace_id:'W'},business:{business_id:'B'}}}};
 const run=(view)=>{const calls=[];Function('view','workspaceId','runtime','router','workspaceOfficeHref',`return (${effect})`) (view,'W',{companyId:'A'},{replace:(url)=>calls.push(url)},(w)=>'/installed/'+w.workspace_id)();return calls;};
 assert.deepEqual(run(good),['/installed/W']);
 for(const mutate of [(v)=>v.status='loading',(v)=>v.detail.workspace.company_id='B',(v)=>v.parent.status='UNRESOLVED',(v)=>v.parent.parentPath.business.business_id='other',(v)=>v.detail.workspace.business_type='GENERIC',(v)=>v.detail.workspace.workspace_id='other']){const bad=structuredClone(good);mutate(bad);assert.deepEqual(run(bad),[]);}
});

test('actual creation callback enters the returned workspace once; restored result never redirects',()=>{
 const source=read('components/v1/CeoDeskOperating.js');const callback=find(source,(n)=>n.type==='VariableDeclarator'&&n.id?.name==='acceptResult');const expression=callback.slice(callback.indexOf('=')+1);
 const make=(originalRecord=null)=>{const calls=[];const deps={company:{company_id:'A'},companyScope:{current:'A'},originalRecord,setStatus(){},setError(){},setRun(){},setResult(){},setStage(){},notifiedRuns:{current:new Set()},onCreated(){},remember(){},confirmed:{package_id:'com.curis.local.writing-authoring'},draft:{},window:{location:{assign:(url)=>calls.push(url)}},workspaceOfficeHref:(w)=>'/installed/'+w.workspace_id};return{calls,accept:Function(...Object.keys(deps),`return (${expression})`)(...Object.values(deps))};};
 const result={founding_run:{entity_id:'R',company_id:'A'},activation:{status:'COMPLETED'},creation_result:{company_id:'A',business_id:'B',workspace_id:'EXACT'}};
 const current=make();current.accept(result);current.accept(result);assert.deepEqual(current.calls,['/installed/EXACT']);
 const restored=make();restored.accept(result,false);assert.deepEqual(restored.calls,[]);
 const foreign=make();foreign.accept({...result,creation_result:{...result.creation_result,company_id:'B'}});assert.deepEqual(foreign.calls,[]);
 const unknown=make();unknown.accept({...result,activation:{status:'UNKNOWN'},creation_result:null});assert.deepEqual(unknown.calls,[]);
});
