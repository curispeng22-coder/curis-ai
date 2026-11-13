import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import vm from 'node:vm';
const require=createRequire(import.meta.url),React=require('react'),{renderToStaticMarkup}=require('react-dom/server'),swc=require('next/dist/build/swc');await swc.loadBindings();
test('actual Chinese help provides local steps, backup/audio limits and a back action',async()=>{
 const {code}=await swc.transform(readFileSync(new URL('../app/ceo-office/help/page.js',import.meta.url),'utf8'),{filename:'help.js',isModule:true,jsc:{parser:{syntax:'ecmascript',jsx:true},transform:{react:{runtime:'automatic'}}},module:{type:'commonjs'}});let backs=0;const m={exports:{}};
 vm.runInNewContext(code,{module:m,exports:m.exports,require:p=>p==='react/jsx-runtime'?require(p):p==='next/navigation'?{useRouter:()=>({back:()=>backs++})}:p==='next/link'?{__esModule:true,default:props=>React.createElement('a',props)}:p.includes('TerraShell')?{__esModule:true,default:({children})=>React.createElement('main',null,children)}:{TerraPageHead:()=>null}});
 const tree=m.exports.default(),html=renderToStaticMarkup(tree);for(const label of ['不需要先连接模型','16 MB','64个文件','备份不会释放','商业权利','备份','恢复'])assert.ok(html.includes(label),label);assert.ok(html.includes('href="/ceo-office/settings"'));assert.ok(html.includes('href="/ceo-office/business"'));tree.props.children[1].props.onClick();assert.equal(backs,1);
 const nav=readFileSync(new URL('../components/v1/V1Sidebar.js',import.meta.url),'utf8');assert.match(nav,/href="\/ceo-office\/help"/);assert.doesNotMatch(nav,/帮助入口尚未接入/);
});
