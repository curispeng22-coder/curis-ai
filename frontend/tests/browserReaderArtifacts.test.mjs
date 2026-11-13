import assert from "node:assert/strict";
import test from "node:test";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { webcrypto, createHash } from "node:crypto";
import vm from "node:vm";

const require = createRequire(import.meta.url);
const swc = require("next/dist/build/swc");
await swc.loadBindings();
const source = readFileSync(new URL("../components/v1/ResultReferenceView.js", import.meta.url), "utf8");
const { code } = await swc.transform(source, { filename: "ResultReferenceView.js", isModule: true,
  jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } },
  module: { type: "commonjs" } });

function harness(filePromise, direct=false) {
  const slots = [], effects = [], revoked = []; let index = 0, next = 0;
  const result = {reference_id:"task:t", result_version:"v1", tenant_id:"tenant", company_id:"company",
    workspace_id:"workspace", source_work_ref:"work", artifacts:[{artifact_id:"a", artifact_type:"agent_file_receipt",
    title:"capture.png", content_sha256:"a".repeat(64)}]};
  if (direct) Object.assign(result, {reference_id:"a", kind:"ARTIFACT", artifact_type:"agent_file_receipt",
    task_ref:"t", content_sha256:"a".repeat(64), title:"capture.png",
    content:JSON.stringify({tenant_id:"tenant",company_id:"company",work_ref:"work",task_id:"t"})});
  const hooks = {
    useState(initial) { let i=index++; if (!(i in slots)) slots[i]=typeof initial === "function" ? initial() : initial;
      return [slots[i], v => { slots[i]=typeof v === "function" ? v(slots[i]) : v; }]; },
    useRef(initial) { let i=index++; return slots[i] ||= {current:initial}; },
    useEffect(fn,deps) { let i=index++, old=slots[i];
      if (!old || deps.length !== old.deps.length || !deps.every((v,j)=>Object.is(v,old.deps[j])))
        effects.push(()=>{ old?.cleanup?.(); slots[i]={deps,cleanup:fn()}; }); },
  };
  const jsx = (type,props) => ({type,props:props || {}});
  const url = { createObjectURL:()=> "blob:"+(++next), revokeObjectURL:v=>revoked.push(v) };
  const loaded={exports:{}};
  vm.runInNewContext(code,{module:loaded,exports:loaded.exports,JSON,Uint8Array,Blob,URL:url,crypto:webcrypto,
    atob:v=>Buffer.from(v,"base64").toString("binary"),setTimeout,
    createImageBitmap:async blob=>{ const data=Buffer.from(await blob.arrayBuffer());
      const expected=Buffer.from("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGP4z8DwHwAFAAH/iZk9HQAAAABJRU5ErkJggg==","base64");
      if(!data.equals(expected)) throw Error("image decode rejected");
      return {width:1,height:1,close(){}}; },
    require:name=>{
      if(name==="react") return hooks;
      if(name==="react/jsx-runtime") return {jsx,jsxs:jsx};
      if(name.endsWith("/api.js")) return {TENANT_ID:"tenant"};
      if(name.endsWith("/v1FrontendApi.js")) return {getResultDetail:async()=>result,markResultViewed:async()=>{},getOriginalAgentFile:()=>filePromise};
      if(name.endsWith("/runtimeApi.js")) return {workspaceEntryHref:()=>"/workspace"};
      if(name.endsWith("/d1State.mjs")) return {d1Href:()=>"/",readableResult:()=>[]};
      if(name.endsWith("/SharedEmployeeWorkArea.js")) return {SharedResultUtility:()=>null};
      throw Error(name);
    }});
  let props={companyId:"company",selection:{workspaceId:"workspace",referenceId:direct ? "a" : "task:t",explicit:false}};
  function render(){ index=0; const tree=loaded.exports.default(props); while(effects.length)effects.shift()(); return tree; }
  function find(node, pred, out=[]) {
    if (!node || typeof node !== "object") return out;
    if (pred(node)) out.push(node);
    for (const child of [node.props?.children].flat(Infinity)) find(child,pred,out);
    return out;
  }
  return {render,find,revoked,result,change:()=>{props={...props,selection:{...props.selection,referenceId:"task:other"}};}};
}
const bytes=Uint8Array.from(Buffer.from("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGP4z8DwHwAFAAH/iZk9HQAAAABJRU5ErkJggg==","base64"));
const hash=createHash("sha256").update(bytes).digest("hex");
const payload={tenant_id:"tenant",company_id:"company",workspace_id:"workspace",work_ref:"work",task_id:"t",
  artifact_ref:"a",artifact_content_sha256:"a".repeat(64),mime_type:"image/png",sha256:hash,bytes:bytes.length,
  content_base64:Buffer.from(bytes).toString("base64"),browser_capture:{tenant_id:"tenant",company_id:"company",
  work_ref:"work",task_id:"t",sha256:hash,bytes:bytes.length,mime_type:"image/png",
  session_id:"session",tab_id:"tab",url:"https://example.com/public"}};
async function ready(h) { h.render(); await Promise.resolve(); return h.render(); }
test("explicit preview verifies identity and cleans blob on result switch",async()=>{
  const h=harness(Promise.resolve(payload)); let tree=await ready(h);
  const button=h.find(tree,n=>n.type==="button" && n.props.children==="核验并预览截图")[0];
  assert.ok(button); await button.props.onClick(); tree=h.render();
  assert.equal(h.find(tree,n=>n.type==="img")[0].props.src,"blob:1");
  h.change(); tree=h.render(); assert.equal(h.find(tree,n=>n.type==="img").length,0);
  assert.deepEqual(h.revoked,["blob:1"]);
});
test("foreign receipt and late response cannot produce a preview",async()=>{
  let resolve; const delayed=new Promise(r=>{resolve=r}); const h=harness(delayed); let tree=await ready(h);
  const request=h.find(tree,n=>n.type==="button" && n.props.children==="核验并预览截图")[0].props.onClick();
  h.change(); h.render(); resolve({...payload,company_id:"other"}); await request;
  assert.equal(h.find(h.render(),n=>n.type==="img").length,0);
});

for (const [label, bad] of [
  ["foreign company", {...payload, company_id:"other"}],
  ["foreign task", {...payload, task_id:"other"}],
  ["receipt version", {...payload, artifact_content_sha256:"b".repeat(64)}],
  ["file hash", {...payload, sha256:"b".repeat(64)}],
  ["not png", {...payload, content_base64:Buffer.alloc(bytes.length).toString("base64")}],
]) {
  test("preview rejects " + label, async () => {
    const h=harness(Promise.resolve(bad)); const tree=await ready(h);
    await h.find(tree,n=>n.type==="button" && n.props.children==="核验并预览截图")[0].props.onClick();
    assert.equal(h.find(h.render(),n=>n.type==="img").length,0);
  });
}

test("direct ARTIFACT uses content as locator and verifies protected file identity",async()=>{
  const h=harness(Promise.resolve(payload),true); const tree=await ready(h);
  await h.find(tree,n=>n.type==="button" && n.props.children==="核验并预览截图")[0].props.onClick();
  assert.equal(h.find(h.render(),n=>n.type==="img")[0].props.src,"blob:1");
});
test("direct ARTIFACT refuses a mismatched protected receipt",async()=>{
  const h=harness(Promise.resolve({...payload,task_id:"foreign"}),true); const tree=await ready(h);
  await h.find(tree,n=>n.type==="button" && n.props.children==="核验并预览截图")[0].props.onClick();
  assert.equal(h.find(h.render(),n=>n.type==="img").length,0);
});
