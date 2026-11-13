import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

const read = (path) => readFileSync(new URL(`../${path}`, import.meta.url), "utf8");

test("Employee uses the shared composer, owner API and explicit result reader", () => {
  const source = read("components/v1/EmployeeConversation.js");
  assert.match(source, /ConversationComposer/);
  assert.match(source, /referenceControl=/);
  assert.match(source, /getEmployeeConversation/);
  assert.match(source, /ResultReferenceView/);
  assert.match(source, /resultSelection\(reference.workspace_id, reference.reference_id\)/);
  assert.match(source, /message.sender.kind === "CEO"/);
  assert.match(source, /message.message_id/);
  assert.doesNotMatch(source, /postAssistantMessage|createWork|createTask/);
});

test("Owner is shared across entry points; retry retains the message key", () => {
  const source = read("components/v1/EmployeeConversation.js");
  assert.match(source, /request_id: original.idempotency_key/);
  assert.match(source, /retry_no: 1/);
  assert.match(source, /UNVERIFIED/);
  assert.match(read("app/ceo-office/organization/employees/[id]/page.js"), /<EmployeeConversation key=/);
  assert.match(read("components/workspace/SharedEmployeeWorkArea.js"), /#employee-conversation/);
  assert.match(read("components/v1/GeneralWorkspaceOperating.js"), /encodeURIComponent\(item.company_employee_ref\).*#employee-conversation/);
  assert.match(read("lib/v1FrontendApi.js"), /employees\/\$\{encodeURIComponent\(employee\)\}\/conversation/);
});

test("Company text preflight uses the selected scope and expiry, and retry keeps the original references", async () => {
  const { createRequire } = await import("node:module"), vm = await import("node:vm");
  const require = createRequire(import.meta.url), swc = require("next/dist/build/swc");
  await swc.loadBindings();
  const source = read("components/v1/EmployeeConversation.js");
  const { code } = await swc.transform(source, { filename: "EmployeeConversation.js", isModule: true,
    jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } },
    module: { type: "commonjs" } });
  const loaded = { exports: {} };
  vm.runInNewContext(code, { module: loaded, exports: loaded.exports, require: () => ({}) });
  const check = loaded.exports.companyTextPermission;
  const expires_at = "2026-11-08T08:00:00+08:00", expiry = Date.parse(expires_at);
  const snapshot = { company_id: "A", policy: { enabled: true, expires_at, workspace_ids: ["W"], models: [{ model_key: "M" }] } };
  assert.equal(check(snapshot, "A", "W", "M", expiry - 10 * 60_000).message, "");
  assert.match(check(snapshot, "A", "W", "M", expiry - 1).message, /5 分钟内到期/);
  assert.equal(check(snapshot, "A", "W", "M", expiry - 1).blocked, false);
  assert.match(check(snapshot, "A", "W", "M", expiry).message, /已过期.*输入已保留/);
  for (const args of [[snapshot, "B", "W", "M"], [snapshot, "A", "W", "other"], [snapshot, "A", "other", "M"],
    [{ ...snapshot, continuity: { needs_reconfirmation: true } }, "A", "W", "M"]]) {
    assert.equal(check(...args, expiry - 1).blocked, true);
  }
  assert.match(source, /getCompanyTextPolicy\(companyId\).*?[\s\S]*?if \(permit\.blocked\)[\s\S]*?return;[\s\S]*?request\.current = nextRequest;/);
  assert.match(source, /references: original\.references\.map\(requestReference\)/);
  assert.match(source, /latest\.recovery_basis === "NO_EXECUTOR_LAUNCH"/);
});

test("Business-origin employee return validates current canonical responsibility without altering professional returns", async () => {
  const { createRequire } = await import("node:module"), vm = await import("node:vm");
  const require = createRequire(import.meta.url), swc = require("next/dist/build/swc"); await swc.loadBindings();
  const source = read("app/ceo-office/organization/employees/[id]/page.js");
  const { code } = await swc.transform(source, { filename: "employee/page.js", isModule: true, jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } }, module: { type: "commonjs" } });
  const { buildOrganizationProjection } = await import("../lib/organizationProjection.js");
  const loaded = { exports: {} }; vm.runInNewContext(code, { module: loaded, exports: loaded.exports, URLSearchParams, require: (name) => name.endsWith("organizationProjection.js") ? { buildOrganizationProjection } : name.endsWith("BusinessCatalogSurface.js") ? { businessCatalogHref: (company, selection) => `/ceo-office/business?${new URLSearchParams({ company_id: company, business_id: selection.businessId })}` } : {} });
  const employee = { id: "current", company_id: "A", name: "用户改名" };
  const organization = { company: { company_id: "A" }, employees: [employee], businesses: [{ company_id: "A", business_id: "B", team: [{ entity_id: "assignment", data: { companyEmployeeRef: "current", roleRef: "role" } }] }] };
  const query = new URLSearchParams({ company_id: "A", business_id: "B" });
  assert.equal(loaded.exports.employeeBusinessReturn(query, "A", employee, organization), "/ceo-office/business?company_id=A&business_id=B");
  for (const bad of ["company_id=A&company_id=A&business_id=B", "company_id=foreign&business_id=B", "company_id=A&business_id=foreign", "company_id=A&business_id=B&return_to=https://foreign"]) assert.throws(() => loaded.exports.employeeBusinessReturn(new URLSearchParams(bad), "A", employee, organization));
  assert.throws(() => loaded.exports.employeeBusinessReturn(query, "other", employee, organization));
  assert.equal(loaded.exports.employeeBusinessReturn(new URLSearchParams("return_to=old&return_kind=writing"), "A", employee, organization), null);
  const duties = loaded.exports.employeeCurrentDuties("A", employee, organization);
  assert.equal(duties.length, 1); assert.equal(duties[0].roleRef, "role");
  assert.throws(() => loaded.exports.employeeCurrentDuties("other", employee, organization));
  assert.equal(loaded.exports.employeeCurrentDuties("A", employee, { ...organization, businesses: [] }).length, 0);
  assert.match(source, /模板详情暂不可读取/);
  assert.equal(source.includes("职责未记录"), false);
  assert.match(read("components/v1/EmployeeConversation.js"), /executionModels.length === 0/);
  assert.match(read("components/v1/EmployeeConversation.js"), /暂无符合当前全局资格的模型/);
});

test("compiled Employee conversation distinguishes loading, failed, zero, and unselected legal scope without changing selection", async () => {
  const { createRequire } = await import("node:module"), vm = await import("node:vm");
  const require = createRequire(import.meta.url), React = require("react"), swc = require("next/dist/build/swc");
  await swc.loadBindings();
  const { code } = await swc.transform(read("components/v1/EmployeeConversation.js"), {
    filename: "EmployeeConversation.js", isModule: true,
    jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } },
    module: { type: "commonjs" },
  });
  const tick = () => new Promise((resolve) => setImmediate(resolve));
  const assignments = [
    { assignment_ref: "a1", workspace_id: "w1", responsibility: "经营责任" },
    { assignment_ref: "a2", workspace_id: "w2", responsibility: "创作责任" },
  ];
  const view = (count) => ({ owner_ref: "e", company_id: "A", tenant_id: "t", assignments: assignments.slice(0, count), messages: [], attempts: [], execution_models: [] });
  const nodes = (tree, predicate) => {
    const found = [];
    function visit(node) {
      if (!node || typeof node !== "object") return;
      if (Array.isArray(node)) return node.forEach(visit);
      if (predicate(node)) found.push(node);
      visit(node.props?.children);
    }
    visit(tree); return found;
  };
  const text = (tree) => typeof tree === "string" ? tree : tree?.props ? text(tree.props.children) : Array.isArray(tree) ? tree.map(text).join("") : "";
  const scene = (getResponse) => {
    const slots = [], pending = []; let cursor = 0, tree;
    const same = (a, b) => a && b && a.length === b.length && a.every((item, index) => Object.is(item, b[index]));
    const hooks = {
      useState(initial) { const i = cursor++; if (!(i in slots)) slots[i] = { value: typeof initial === "function" ? initial() : initial }; return [slots[i].value, (value) => { slots[i].value = typeof value === "function" ? value(slots[i].value) : value; }]; },
      useRef(initial) { const i = cursor++; return slots[i] ||= { current: initial }; },
      useCallback(fn, deps) { const i = cursor++; if (!slots[i] || !same(slots[i].deps, deps)) slots[i] = { deps, value: fn }; return slots[i].value; },
      useEffect(fn, deps) { const i = cursor++; if (!slots[i] || !same(slots[i].deps, deps)) { const old = slots[i]; slots[i] = { deps }; pending.push(() => { old?.cleanup?.(); slots[i].cleanup = fn(); }); } },
    };
    function ConversationComposer() {}
    function EmployeeAvatar() {}
    const loaded = { exports: {} };
    vm.runInNewContext(code, {
      module: loaded, exports: loaded.exports, URLSearchParams, crypto: globalThis.crypto, setInterval, clearInterval,
      require: (name) => name === "react" ? hooks : name === "react/jsx-runtime" ? require(name)
        : name.includes("SharedConversation") ? { ConversationComposer }
          : name.includes("EmployeeAvatar") ? { EmployeeAvatar }
            : name.includes("ResultReferenceView") ? { __esModule: true, default: function ResultReferenceView() {}, resultSelection: () => ({}) }
              : name.includes("v1FrontendApi") ? {
                getEmployeeConversation: getResponse, getConversation: getResponse,
                getEmployeeConversationReferences: async () => ({ references: [] }),
                openEmployeeConversation: async () => { throw Error("No send allowed"); },
                sendEmployeeConversation: async () => { throw Error("No send allowed"); },
              } : {},
    });
    return {
      render(extra = {}) { cursor = 0; tree = loaded.exports.default({ companyId: "A", employee: { id: "e", name: "员工" }, conversationId: null, ...extra }); while (pending.length) pending.shift()(); return tree; },
      get tree() { return tree; },
    };
  };
  const composer = (tree) => nodes(tree, (node) => node.type?.name === "ConversationComposer")[0].props;
  const scope = (tree) => nodes(tree, (node) => node.type === "select" && node.props["aria-label"] === "本次讨论的责任范围")[0];

  let resolvePending, reads = 0;
  const pendingScene = scene(() => {
    reads++;
    if (reads === 1) return new Promise((resolve) => { resolvePending = resolve; });
    if (reads === 2) return Promise.resolve(view(2));
    return Promise.reject(Error("read failed"));
  });
  pendingScene.render();
  assert.equal(composer(pendingScene.tree).disabled, true);
  assert.match(composer(pendingScene.tree).notice, /正在确认/);
  resolvePending(view(2)); await tick(); pendingScene.render();
  assert.equal(scope(pendingScene.tree).props.value, "");
  assert.equal(nodes(scope(pendingScene.tree), (node) => node.type === "option").length, 3);
  assert.equal(composer(pendingScene.tree).disabled, true);
  assert.equal(composer(pendingScene.tree).notice, "请选择这次讨论的责任范围；选择后再发送。");
  scope(pendingScene.tree).props.onChange({ target: { value: "a1" } }); pendingScene.render();
  assert.equal(scope(pendingScene.tree).props.value, "a1");
  assert.equal(composer(pendingScene.tree).disabled, false);
  assert.match(text(pendingScene.tree), /暂无符合当前全局资格的模型/);
  nodes(pendingScene.tree, (node) => node.type === "button" && text(node) === "重新读取")[0].props.onClick();
  pendingScene.render(); assert.equal(composer(pendingScene.tree).disabled, true);
  await tick(); pendingScene.render();
  assert.equal(scope(pendingScene.tree).props.value, "a1");
  assert.equal(composer(pendingScene.tree).disabled, false);
  nodes(pendingScene.tree, (node) => node.type === "button" && text(node) === "重新读取")[0].props.onClick();
  await tick(); pendingScene.render();
  assert.equal(scope(pendingScene.tree).props.value, "a1");
  assert.equal(composer(pendingScene.tree).disabled, true);
  assert.equal(composer(pendingScene.tree).notice, "当前责任范围暂时无法确认，请重新读取。");

  const zero = scene(async () => view(0)); zero.render(); await tick(); zero.render();
  assert.equal(composer(zero.tree).disabled, true);
  assert.equal(composer(zero.tree).notice, "当前没有可用于这次回复的责任范围；已有工作安排可在员工资料中查看。");
  const one = scene(async () => view(1)); one.render(); await tick(); one.render();
  assert.equal(scope(one.tree).props.value, "a1");
  const failed = scene(async () => { throw Error("read failed"); }); failed.render(); await tick(); failed.render();
  assert.equal(composer(failed.tree).disabled, true);
  assert.equal(composer(failed.tree).notice, "当前责任范围暂时无法确认，请重新读取。");
  assert.doesNotMatch(composer(failed.tree).notice, /没有可用于/);
  for (const kind of ["cg", "music", "writing"]) {
    const businessReturn = { kind, href: `/ceo-office/workspace/installed/w?object=exact-${kind}&version=original`, label: "返回原工作" };
    const full = scene(async (company) => { assert.equal(company, "A"); return { ...view(0), conversation_id: "original-topic" }; });
    full.render({ businessReturn }); await tick(); full.render({ businessReturn });
    const link = nodes(full.tree, (node) => node.type === "a" && text(node) === "打开完整对话")[0];
    const query = new URL(link.props.href, "http://curis.local").searchParams;
    assert.equal(query.get("conversation_id"), "original-topic");
    assert.equal(query.get("return_kind"), kind); assert.equal(query.get("return_to"), businessReturn.href);
    assert.equal(composer(full.tree).disabled, true, "unknown scope still prevents sending");
    full.render();
    assert.equal(nodes(full.tree, (node) => node.type === "a" && text(node) === "打开完整对话")[0].props.href, "/ceo-office/conversation?conversation_id=original-topic");
  }

});

test('embedded real composer preserves drafts across collapse, object switch and cold mount; normal reply needs no Selection', async () => {
  const {createRequire}=await import('node:module'),vm=await import('node:vm');
  const require=createRequire(import.meta.url),swc=require('next/dist/build/swc');await swc.loadBindings();
  const {code}=await swc.transform(read('components/v1/EmployeeConversation.js'),{filename:'employee.js',jsc:{parser:{syntax:'ecmascript',jsx:true},transform:{react:{runtime:'automatic'}}},module:{type:'commonjs'}});
  const storage=new Map(),creates=[],sends=[];let id=0,topic=null,createUnknown=false,sendUnknown=false,agentAvailable=false;
  let companyText = false, expiresAt;
  const base=()=>({tenant_id:'T',company_id:'A',owner_ref:'e',employee:{id:'e'},conversation_id:'',assignments:[{assignment_ref:'a',workspace_id:'W',responsibility:'章节创作'}],execution_models:[{source:'official',model_key:'m'}],model_preference:{model_key:'m'},execution_readiness:[{assignment_ref:'a',status:'AVAILABLE',company_text:companyText}],messages:[],attempts:[]});
  const api={getEmployeeConversation:async()=>({...base(),discussion_topics:topic?[{conversation_id:topic.conversation_id,...topic.discussion_scope,assignment_ref:'a'}]:[]}),getConversation:async()=>structuredClone(topic),getEmployeeConversationReferences:async()=>({references:[]}),createConversation:async(company,payload)=>{creates.push(payload);if(createUnknown){createUnknown=false;throw Error('lost creation response');}topic||={...base(),conversation_id:'topic',discussion_scope:{workspace_id:'W',object_ref:'o1'}};return structuredClone(topic);},sendConversation:async(company,topicId,payload)=>{sends.push(payload);topic={...topic,messages:[{message_id:'msg',idempotency_key:payload.request_id,sender:{kind:'CEO'},body:payload.body,context:{workspace_id:'W'},references:[]},{message_id:'reply',sender:{kind:'EMPLOYEE'},body:'真实受控回复',task_ref:'task',context:{workspace_id:'W'},references:[]}],attempts:[{attempt_id:'attempt',message_id:'msg',status:sendUnknown?'UNKNOWN':'COMPLETED',effect_status:sendUnknown?'UNKNOWN':'SETTLED'}]};if(sendUnknown)throw Error('lost message response');return structuredClone(topic);}};
  const nodes=(root,predicate)=>{const result=[];function walk(n){if(!n||typeof n!=='object')return;if(Array.isArray(n)){n.forEach(walk);return;}if(predicate(n))result.push(n);walk(n.props?.children);}walk(root);return result;};
  const text=(n)=>typeof n==='string'?n:Array.isArray(n)?n.map(text).join(''):n?.props?text(n.props.children):'';
  const originalRead=api.getEmployeeConversation;api.getEmployeeConversation=async(...args)=>({...await originalRead(...args),execution_agents:agentAvailable?[{binding_id:'agent-binding',display_name:'已绑定 Agent'}]:[]});
  api.getCompanyTextPolicy = async () => ({ company_id: 'A', policy: { enabled: true, expires_at: expiresAt,
    workspace_ids: ['W'], models: [{ model_key: 'm' }] } });
  function scene(){let cursor=0,tree;const slots=[],effects=[];const same=(a,b)=>a&&b&&a.length===b.length&&a.every((v,i)=>Object.is(v,b[i]));
    const hooks={useState(initial){const i=cursor++;if(!(i in slots))slots[i]={value:initial};return[slots[i].value,v=>{slots[i].value=typeof v==='function'?v(slots[i].value):v;}];},useRef(initial){const i=cursor++;return slots[i]||={current:initial};},useCallback(fn,deps){const i=cursor++;if(!slots[i]||!same(slots[i].deps,deps))slots[i]={deps,value:fn};return slots[i].value;},useEffect(fn,deps){const i=cursor++,old=slots[i];if(!old||!same(old.deps,deps)){slots[i]={deps};effects.push(()=>{old?.cleanup?.();slots[i].cleanup=fn();});}}};
    function ConversationComposer(){}function AgentWorkControl(){}function EmployeeAvatar(){}function ResultReferenceView(){}
    const module={exports:{}};vm.runInNewContext(code,{module,exports:module.exports,URLSearchParams,crypto:{randomUUID:()=>`request-${++id}`},localStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v)},window:{addEventListener(){},removeEventListener(){}},setInterval:()=>0,clearInterval(){},require:name=>name==='react'?hooks:name==='react/jsx-runtime'?require(name):name.includes('SharedConversation')?{ConversationComposer,AgentWorkControl}:name.includes('EmployeeAvatar')?{EmployeeAvatar}:name.includes('ResultReferenceView')?{__esModule:true,default:ResultReferenceView,resultSelection:(workspaceId,referenceId)=>({workspaceId,referenceId})}:name.includes('v1FrontendApi')?api:{}});
    let props={companyId:'A',employee:{id:'e',name:'真实负责员工'},active:true,embedded:{workspaceId:'W',contextKey:'o1',objectRef:'o1',assignmentRef:'a',title:'当前章节'},businessReturn:{kind:'writing',href:'/exact-original-chapter'}};
    const render=()=>{cursor=0;tree=module.exports.default(props);while(effects.length)effects.shift()();return tree;};
    return{async flush(){for(let i=0;i<6;i++){render();await new Promise(r=>setImmediate(r));}render();},change(value){props={...props,...value};},get tree(){return tree;},get composer(){return nodes(tree,n=>n.type===ConversationComposer)[0].props;},button(label){return nodes(tree,n=>n.type==='button'&&text(n)===label)[0];}};
  }
  const first=scene();await first.flush();
  assert.match(read('components/v1/SharedConversation.js'),/conversationReturn=\{returnHref\} businessReturn=\{businessReturn\}/);
  first.composer.onChange('尚未发送的正文讨论');await first.flush();
  first.change({active:false});await first.flush();assert.equal(first.composer.value,'尚未发送的正文讨论');assert.equal(sends.length,0);
  first.change({active:true,embedded:{workspaceId:'W',contextKey:'o2',objectRef:'o2',assignmentRef:'a'}});await first.flush();assert.equal(first.composer.value,'');
  const cold=scene();await cold.flush();assert.equal(cold.composer.value,'尚未发送的正文讨论');assert.equal(cold.composer.disabled,false);
  await cold.composer.onSubmit({preventDefault(){}});await cold.flush();assert.equal(sends.length,1);assert.equal(sends[0].references.length,0);assert.equal('_phase' in sends[0],false);assert.equal(sends[0].execution_selection.purpose,'CONVERSATION_REPLY');assert.equal(cold.composer.value,'');const replyLink=nodes(cold.tree,n=>n.type==='a'&&text(n)==='打开这次回复')[0];assert.ok(replyLink.props.href.includes('return_to=%2Fexact-original-chapter'));assert.ok(replyLink.props.href.endsWith('#reply'));
  storage.clear();const historyCold=scene();await historyCold.flush();assert.ok(text(historyCold.tree).includes('真实受控回复'));assert.equal(sends.length,1);
  storage.clear();topic=null;creates.length=0;sends.length=0;createUnknown=true;
  const interrupted=scene();await interrupted.flush();interrupted.composer.onChange('创建入口时断开');await interrupted.flush();await interrupted.composer.onSubmit({preventDefault(){}});await interrupted.flush();assert.equal(sends.length,0);assert.equal(interrupted.composer.disabled,true);
  const recovered=scene();await recovered.flush();await recovered.button('恢复原讨论入口').props.onClick();await recovered.flush();assert.equal(creates.length,2);assert.equal(creates[0].request_id,creates[1].request_id);assert.equal(sends.length,0);assert.equal(recovered.composer.value,'创建入口时断开');
  sendUnknown=true;await recovered.composer.onSubmit({preventDefault(){}});await recovered.flush();assert.equal(sends.length,1);
  const unknownCold=scene();await unknownCold.flush();assert.equal(unknownCold.composer.disabled,true);assert.equal(unknownCold.composer.value,'创建入口时断开');assert.equal(sends.length,1);
  storage.clear();topic=null;sendUnknown=false;agentAvailable=true;sends.length=0;creates.length=0;
  for (const embedded of [
    {workspaceId:'W',contextKey:'workspace',objectRef:null,assignmentRef:'a',title:'作品库讨论'},
    {workspaceId:'W',contextKey:'book:book',objectRef:'book',assignmentRef:'a',title:'作品讨论'},
  ]) {
    const workspace=scene();workspace.change({embedded});await workspace.flush();
    const agentControl=nodes(workspace.tree,n=>n.type?.name==='AgentWorkControl')[0];
    assert.equal(agentControl.props.businessReturn.href,'/exact-original-chapter');
    assert.equal(agentControl.props.businessReturn.kind,'writing');
    const choice=nodes(workspace.tree,n=>n.type==='select'&&n.props['aria-label']==='本次与员工协作方式')[0];
    assert.equal(nodes(choice,n=>n.type==='option'&&n.props.value==='agent')[0].props.disabled,true);
    assert.match(text(workspace.tree),/当前入口用于讨论，无需选择文字范围/);
    assert.doesNotMatch(text(workspace.tree),/请保存当前对象并选择有效范围|重新选择有效文字范围/);
    choice.props.onChange({target:{value:'agent'}});await workspace.flush();
    assert.equal(workspace.composer.showSubmit,true,'missing source cannot enter formal execution, including stale callbacks');
    assert.equal(workspace.composer.disabled,false,'ordinary discussion needs no selection');
    assert.equal(nodes(workspace.tree,n=>n.type?.name==='AgentWorkControl')[0].props.disabled,true);
    assert.equal(sends.length,0);assert.equal(creates.length,0);
  }
  const writingSource={workspaceId:'W',contextKey:'chapter:book:chapter',objectRef:'chapter',assignmentRef:'a',title:'章节讨论',agentSourceReady:false,agentSource:{kind:'writing',book_ref:'book',chapter_ref:'chapter'}};
  const modes=scene();modes.change({embedded:writingSource});await modes.flush();modes.composer.onChange('保留的员工工作指令');await modes.flush();
  const modeChoice=()=>nodes(modes.tree,n=>n.type==='select'&&n.props['aria-label']==='本次与员工协作方式')[0];
  const workControl=()=>nodes(modes.tree,n=>n.type?.name==='AgentWorkControl')[0];
  assert.equal(modeChoice().props.value,'discussion');assert.equal(workControl().props.disabled,true);
  const oldSubmit=modes.composer.onSubmit;
  modeChoice().props.onChange({target:{value:'agent'}});await modes.flush();
  assert.equal(modes.composer.value,'保留的员工工作指令');assert.equal(modes.composer.showSubmit,false);
  let prevented=0;await oldSubmit({preventDefault(){prevented++;}});await modes.composer.onSubmit({preventDefault(){prevented++;}});
  assert.equal(prevented,2);assert.equal(sends.length,0);assert.equal(creates.length,0);
  assert.equal(workControl().props.body,'保留的员工工作指令');assert.equal(workControl().props.disabled,true,'unsaved source still blocks Agent');
  assert.match(text(modes.tree),/章节保存版本和正文选段/);
  modes.change({active:false});await modes.flush();modes.change({active:true});await modes.flush();assert.equal(modeChoice().props.value,'agent');
  modes.change({embedded:{...writingSource,agentSource:undefined,agentSourceReady:undefined}});await modes.flush();
  assert.equal(modeChoice().props.value,'discussion');assert.equal(modes.composer.showSubmit,true);
  assert.equal(workControl().props.disabled,true);assert.equal(modes.composer.value,'保留的员工工作指令');
  modes.change({embedded:writingSource});await modes.flush();
  modeChoice().props.onChange({target:{value:'discussion'}});await modes.flush();
  assert.equal(modes.composer.value,'保留的员工工作指令');assert.equal(modes.composer.showSubmit,true);assert.equal(sends.length,0);
  modeChoice().props.onChange({target:{value:'agent'}});await modes.flush();
  agentAvailable=false;await modes.button('重新读取').props.onClick();await modes.flush();
  assert.equal(modeChoice(),undefined);assert.equal(modes.composer.showSubmit,true);
  assert.equal(modes.composer.value,'保留的员工工作指令');assert.equal(sends.length,0);
  await modes.composer.onSubmit({preventDefault(){}});await modes.flush();
  assert.equal(sends.length,1);assert.equal(sends[0].body,'保留的员工工作指令');
  storage.clear();topic=null;agentAvailable=true;sends.length=0;creates.length=0;
  for (const [kind,contextKey,source,label,notice] of [
    ['writing','chapter:book:chapter',{book_ref:'book',chapter_ref:'chapter'},'章节正文选段',/章节保存版本和正文选段/],
    ['content-growth','content:content',{content_ref:'content'},'内容正文片段或镜头范围',/当前保存版本、员工责任及正文片段或镜头范围/],
    ['music','song:song',{song_ref:'song'},'歌词片段',/此处不支持按音频范围正式执行/],
  ]) {
    const embedded={workspaceId:'W',contextKey,objectRef:kind,assignmentRef:'a',agentSourceReady:false,agentSource:{kind,...source}};
    const domain=scene();domain.change({embedded});await domain.flush();domain.composer.onChange('只准备，不执行');await domain.flush();
    const choice=()=>nodes(domain.tree,n=>n.type==='select'&&n.props['aria-label']==='本次与员工协作方式')[0];
    const work=()=>nodes(domain.tree,n=>n.type?.name==='AgentWorkControl')[0];
    assert.equal(domain.composer.disabled,false);assert.doesNotMatch(text(domain.tree),notice);
    choice().props.onChange({target:{value:'agent'}});await domain.flush();
    assert.match(text(domain.tree),notice);assert.equal(work().props.disabled,true);
    domain.change({embedded:{...embedded,agentSourceReady:true}});await domain.flush();
    assert.match(text(domain.tree),new RegExp('已准备'+label+'；执行能力与许可仍需核对'));
    assert.equal(work().props.disabled,false);assert.equal(domain.composer.value,'只准备，不执行');
    domain.change({blocked:true});await domain.flush();assert.equal(work().props.disabled,true,'source readiness never overrides other guards');
    assert.equal(sends.length,0);assert.equal(creates.length,0,'mode/source changes never dispatch a request');
  }
  storage.clear(); topic = null; agentAvailable = false; companyText = true;
  expiresAt = new Date(Date.now() - 1000).toISOString();
  const expired = scene(); await expired.flush();
  expired.composer.onChange('续期后保留这条输入'); await expired.flush();
  await expired.composer.onSubmit({ preventDefault() {} }); await expired.flush();
  assert.match(text(expired.tree), /公司文字许可已过期/);
  const settings = nodes(expired.tree, (node) => node.type === 'a' && text(node) === '核对公司文字许可')[0];
  assert.equal(new URL(settings.props.href, 'https://curis.invalid').searchParams.get('return_to'), '/exact-original-chapter');
  assert.deepEqual([creates.length, sends.length], [0, 0]);
  const renewed = scene(); expiresAt = new Date(Date.now() + 60 * 60_000).toISOString(); await renewed.flush();
  assert.equal(renewed.composer.value, '续期后保留这条输入');
  assert.deepEqual([creates.length, sends.length], [0, 0]);
  await renewed.composer.onSubmit({ preventDefault() {} }); await renewed.flush();
  assert.equal(sends[0].body, '续期后保留这条输入');
  assert.deepEqual([creates.length, sends.length], [1, 1]);
});
