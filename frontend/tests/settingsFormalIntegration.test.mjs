import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { SETTINGS_CATEGORIES, settingsCategory, settingsReturn, captureSettingsHref, settingsModelHref, settingsEntryIdentity,
  presentationSubmission, savedPresentationDraft, settingsDraftKey, readSettingsDraft, readSettingsModels, themeValue, applySettingsTheme, THEME_CHANGED } from "../lib/settingsEntryState.mjs";
import { validateBusinessReturn } from "../lib/businessReturnApi.js";
import { TENANT_ID } from "../lib/api.js";
import { CG_PACKAGE, contentHref } from "../lib/contentGrowthState.mjs";
import { MUSIC_PACKAGE, songHref } from "../lib/musicState.mjs";
import { WRITING_PACKAGE, chapterHref } from "../lib/writingState.mjs";

// Every request in these tests uses an injected local DTO source. No HTTP or Backend.
globalThis.fetch = () => { throw new Error("Network forbidden in Settings focused tests"); };

test("real Settings recovery callback refreshes mounted consumers only after RESTORED", async () => {
  const require = createRequire(import.meta.url);
  const parser = require("next/dist/compiled/babel/parser");
  const source = readFileSync(new URL("../app/ceo-office/settings/page.js", import.meta.url), "utf8");
  const tree = parser.parse(source, { sourceType: "module", plugins: ["jsx"] });
  const find = (node) => {
    if (!node || typeof node !== "object") return null;
    if (node.type === "VariableDeclarator" && node.id?.name === "runRecovery") return node.init;
    for (const value of Object.values(node)) {
      for (const child of Array.isArray(value) ? value : [value]) {
        const found = find(child);
        if (found) return found;
      }
    }
    return null;
  };
  const callback = find(tree);
  assert.equal(callback?.type, "ArrowFunctionExpression");
  const make = (result, runtimeStatus) => {
    const effects = { refresh: 0, profile: 0, sidebar: 0, busy: [], receipt: null, draft: "尚未保存" };
    const deps = {
      recovery: { status: "PREFLIGHT_OK", confirmationId: "a".repeat(64) }, recoveryBusy: false,
      runtime: { status: runtimeStatus, refresh: async () => { effects.refresh += 1; } },
      setRecoveryBusy: (value) => effects.busy.push(value), setRestoreConfirmed: () => {},
      nativeRecovery: async () => result, setRecovery: (value) => { effects.receipt = value; },
      profileGeneration: { current: 0 }, setReload: (change) => { effects.profile = change(effects.profile); },
      window: { dispatchEvent: (event) => { if (event.type === "presentation.changed") effects.sidebar += 1; } },
      Event, PRESENTATION_CHANGED: "presentation.changed",
    };
    const run = Function(...Object.keys(deps), `return (${source.slice(callback.start, callback.end)})`)(...Object.values(deps));
    return { run, effects };
  };
  const restored = make({ status: "RESTORED", identity: [{ company_id: "company-1" }] }, "error");
  await restored.run("commit_curis_restore");
  assert.deepEqual([restored.effects.refresh, restored.effects.profile, restored.effects.sidebar], [1, 1, 1]);
  assert.deepEqual(restored.effects.busy, [true, false]);
  assert.equal(restored.effects.receipt.status, "RESTORED");
  assert.equal(restored.effects.draft, "尚未保存");
  for (const status of ["RECOVERY_HOLD", "FAILED"]) {
    const blocked = make({ status }, "ready");
    await blocked.run("commit_curis_restore");
    assert.deepEqual([blocked.effects.refresh, blocked.effects.profile, blocked.effects.sidebar], [0, 0, 0]);
    assert.equal(blocked.effects.receipt.status, status);
  }
});

test("real profile effect keeps the scoped unsaved draft through cold recovery rebind", async () => {
  const require = createRequire(import.meta.url);
  const parser = require("next/dist/compiled/babel/parser");
  const source = readFileSync(new URL("../app/ceo-office/settings/page.js", import.meta.url), "utf8");
  const tree = parser.parse(source, { sourceType: "module", plugins: ["jsx"] });
  const find = (node) => {
    if (!node || typeof node !== "object") return null;
    if (node.type === "CallExpression" && node.callee?.name === "useEffect" && node.arguments?.[0]?.type === "ArrowFunctionExpression") {
      const text = source.slice(node.arguments[0].start, node.arguments[0].end);
      if (text.includes("getV1Presentation().then") && text.includes("readSettingsDraft")) return node.arguments[0];
    }
    for (const value of Object.values(node)) for (const child of Array.isArray(value) ? value : [value]) {
      const found = find(child); if (found) return found;
    }
    return null;
  };
  const callback = find(tree);
  assert.equal(callback?.type, "ArrowFunctionExpression");
  const key = settingsDraftKey(TENANT_ID, "selfuse-ceo", "company-1", "work-return");
  const pending = { display_name: "尚未保存的姓名", avatar_ref: "preset:iris" };
  const saved = { display_name: "资料库旧姓名", avatar_ref: "preset:mint", welcome_dismissed: true };
  const state = { draft: pending, profile: null, reads: 0 };
  const deps = {
    identityReady: false, profileGeneration: { current: 0 }, saveGeneration: { current: 0 }, saving: { current: false },
    setProfile: (value) => { state.profile = value; }, setDraft: (value) => { state.draft = value; },
    EMPTY: { display_name: "", avatar_ref: "" }, setProfileError: () => {}, setSaveStatus: () => {},
    getV1Presentation: async () => { state.reads += 1; return saved; }, alive: { current: true },
    scopeRef: { current: key }, scopeKey: key, presentationSubmission, readSettingsDraft,
    window: { sessionStorage: { getItem: (name) => name === key ? JSON.stringify(pending) : null } },
  };
  const effect = () => Function(...Object.keys(deps), `return (${source.slice(callback.start, callback.end)})`)(...Object.values(deps));
  effect()();
  assert.equal(state.draft.display_name, pending.display_name);
  assert.equal(state.reads, 0, "cold error must not refetch or clear the mounted draft");
  deps.identityReady = true;
  effect()();
  await Promise.resolve(); await Promise.resolve();
  assert.equal(state.reads, 1);
  assert.equal(state.profile.status, "ready");
  assert.deepEqual(state.draft, pending, "saved backend profile must not overwrite scoped unsaved input");
});

test("six accepted categories and legacy/unknown tab have a safe default", () => {
  assert.equal(SETTINGS_CATEGORIES.length, 6);
  for (const [key] of SETTINGS_CATEGORIES) assert.equal(settingsCategory(key), key);
  for (const key of ["profile", "brand", "notify", null, "../models"]) assert.equal(settingsCategory(key), "personal");
});
test("backup uses the existing data category and preserves the original Work return and draft scope", () => {
  const entry = captureSettingsHref("/ceo-office/business", "?filter=active");
  const query = new URLSearchParams(entry.split("?")[1]);
  const before = settingsEntryIdentity(query);
  const draft = settingsDraftKey(TENANT_ID, "selfuse-ceo", "company-1", before);
  query.set("tab", "data");
  assert.equal(settingsCategory(query.get("tab")), "data");
  assert.equal(settingsReturn(query).href, "/ceo-office/business?filter=active");
  assert.equal(settingsDraftKey(TENANT_ID, "selfuse-ceo", "company-1", settingsEntryIdentity(query)), draft);
});
test("the existing full-PUT submission keeps the loaded welcome flag and untouched local avatar", () => {
  const loaded = { welcome_dismissed: true, display_name: "原姓名", avatar_ref: "data:image/png;base64,abc", irrelevant: "must not send" };
  assert.deepEqual(presentationSubmission(loaded, { ...loaded, display_name: " 新姓名 " }), {
    welcome_dismissed: true, display_name: "新姓名", avatar_ref: loaded.avatar_ref,
  });
  assert.equal(presentationSubmission({ ...loaded, welcome_dismissed: false }, loaded).welcome_dismissed, false);
  assert.throws(() => presentationSubmission({ avatar_ref: "" }, loaded));
  for (const name of ["x".repeat(81), "unsafe\u0001name"]) assert.throws(() => presentationSubmission(loaded, { ...loaded, display_name: name }));
  for (const avatar of ["https://example.invalid/avatar.png", "data:image/svg+xml;base64,abc", "preset:" + "x".repeat(260000)]) {
    assert.throws(() => presentationSubmission(loaded, { ...loaded, avatar_ref: avatar }));
  }
});
test("an older successful save normalizes its own submission but preserves later edits", () => {
  const submitted = { display_name: " 原名 ", avatar_ref: "preset:iris" }, saved = { display_name: "原名", avatar_ref: "preset:iris", welcome_dismissed: true };
  assert.equal(savedPresentationDraft({ ...submitted }, submitted, saved), saved);
  const later = { display_name: "继续编辑", avatar_ref: "preset:mint" };
  assert.equal(savedPresentationDraft(later, submitted, saved), later);
});
test("temporary draft keys isolate tenant, actor, Company and source work", () => {
  const original = settingsDraftKey("t", "ceo", "A", "work1");
  for (const args of [["other", "ceo", "A", "work1"], ["t", "other", "A", "work1"], ["t", "ceo", "B", "work1"], ["t", "ceo", "A", "work2"]]) assert.notEqual(settingsDraftKey(...args), original);
  const draft = { display_name: "尚未保存", avatar_ref: "preset:iris" };
  assert.deepEqual(readSettingsDraft({ getItem: (key) => key === original ? JSON.stringify({ ...draft, credential: "must not retain" }) : null }, original), draft);
  for (const raw of ["not-json", "x".repeat(270001), JSON.stringify({ display_name: "x", avatar_ref: "https://private.invalid" })]) assert.equal(readSettingsDraft({ getItem: () => raw }, original), null);
});
test("the existing theme key remains the only theme store and dispatches a shared refresh", () => {
  const calls = [], host = { document: { documentElement: { dataset: {} } }, localStorage: { setItem: (...args) => calls.push(args) }, dispatchEvent: (event) => calls.push(event.type) };
  assert.equal(themeValue("untrusted"), "system"); assert.equal(applySettingsTheme("dark", host), "dark");
  assert.equal(host.document.documentElement.dataset.theme, "dark");
  assert.deepEqual(calls, [["curis.theme", "dark"], THEME_CHANGED]);
});
test("ordinary local areas return precisely; unsupported receivers get no invented return", () => {
  const url = captureSettingsHref("/ceo-office/business", "?filter=active");
  assert.equal(settingsReturn(new URLSearchParams(url.split("?")[1])).href, "/ceo-office/business?filter=active");
  for (const path of ["/ceo-office/settings", "/ceo-office/capabilities", "/ceo-office/employees/private", "https://evil.invalid", "//evil.invalid"]) assert.equal(captureSettingsHref(path), "/ceo-office/settings");
});
test("external, duplicate, self-loop and mixed return metadata cannot become redirects", () => {
  for (const params of [new URLSearchParams({ settings_from: "https://evil.invalid" }), new URLSearchParams({ settings_from: "/ceo-office/settings" }),
    new URLSearchParams("settings_from=/ceo-office&settings_from=/ceo-office/business"), new URLSearchParams({ return_kind: "unknown", return_to: "/ceo-office" }),
    new URLSearchParams("return_to=/ceo-office&return_to=/ceo-office"), new URLSearchParams({ settings_from: "/ceo-office\\evil" })]) assert.throws(() => settingsReturn(params));
});

function domainFixture(kind) {
  const definition = kind === "cg" ? CG_PACKAGE : kind === "music" ? MUSIC_PACKAGE : WRITING_PACKAGE;
  const scope = { tenant_id: TENANT_ID, company_id: "B", workspace_id: "w", scope_type: "WORKSPACE", scope_ref: "w" };
  const instance = { instance_id: "i", company_id: "B", workspace_id: "w", package_id: definition.id, package_version: definition.version, package_digest: definition.digest, status: "ACTIVE" };
  const detail = { instance, read_only: false, package: { package_id: definition.id, version: definition.version, digest: definition.digest, status: "ACTIVE", schema_version: "curis.workspace-package/v1" },
    schemas: { ContentGraphic: { schemaVersion: definition.version }, MusicSong: { schemaVersion: definition.version }, WritingBook: { schemaVersion: "writing.book/v1" }, WritingChapter: { schemaVersion: "writing.chapter/v1" } } };
  const collection = kind === "writing" ? { scope: { ...scope, ...instance }, books: [{ ref: "book" }], chapters: [{ ref: "chapter", bookRef: "book" }] }
    : { entry: { scope, actor: "verified-ceo", definition: { package_id: definition.id, version: definition.version, digest: definition.digest } } };
  const content = { content: { ...scope, entity_id: "content" }, versions: [{ entity_id: "version" }] };
  const song = { song: { ...scope, entity_id: "song" }, versions: [{ ...scope, entity_id: "lyrics", parent_id: "song", data: { kind: "LyricsVersion", text: "原歌词" } }], candidates: [], assets: [] };
  const chapter = { scope: { ...collection.scope, book_ref: "book", chapter_ref: "chapter" } };
  const href = kind === "cg" ? contentHref("w", { content: "content", version: "version" }) : kind === "music" ? songHref("w", { song: "song", lyrics: "lyrics" }) : chapterHref("w", { mode: "chapter", book: "book", chapter: "chapter", anchor: "draft:0:4" });
  const calls = [], state = { forbidden: false, collection };
  const request = async (path, options) => {
    calls.push(path); assert.equal(options, undefined);
    if (path === "/api/workspace/packages/workspaces/w") return detail;
    assert.ok(path.startsWith("/api/workspace/v1/companies/B/"));
    if (state.forbidden) throw Object.assign(new Error("forbidden fixture"), { status: 403 });
    if (path.includes("/contents/")) return content;
    if (path.includes("/songs/")) return song;
    if (path.includes("/chapters/")) return chapter;
    return state.collection;
  };
  return { href, request, state, calls };
}
for (const kind of ["cg", "music", "writing"]) {
  test(kind + ": Sidebar→Settings→existing model page→same category preserves the exact original target", async () => {
    const f = domainFixture(kind), [path, query] = f.href.split("?");
    const entry = new URLSearchParams(captureSettingsHref(path, query).split("?")[1]);
    assert.deepEqual(settingsReturn(entry).business, { kind, value: f.href });
    const model = new URLSearchParams(settingsModelHref(entry).split("?")[1]);
    const back = new URLSearchParams(settingsModelHref(model, { returning: true }).split("?")[1]);
    assert.equal(back.get("tab"), "models"); assert.equal(back.get("return_to"), f.href);
    assert.equal(settingsEntryIdentity(entry), settingsEntryIdentity(back), "same temporary draft source across the round trip");
    const returned = settingsReturn(back).business;
    const verified = await validateBusinessReturn(returned.kind, returned.value, { request: f.request });
    assert.equal(verified.company, "B"); assert.equal(verified.href, f.href);
    assert.ok(!f.calls.some((call) => call.includes("/companies/A/")));
    f.state.forbidden = true;
    await assert.rejects(validateBusinessReturn(returned.kind, returned.value, { request: f.request }));
    entry.set("settings_from", "/ceo-office"); assert.throws(() => settingsReturn(entry));
  });
}
test("model metadata can show configured/default facts without claiming connection health", async () => {
  const value = await readSettingsModels({ readProviders: async () => ({ providers: [{ configured: true, healthy: true }, { configured: false }] }), readPreference: async () => ({ preference: { model_name: "saved-choice" } }), isCurrent: () => true });
  assert.deepEqual(value, { status: "ready", configured: 1, defaultName: "saved-choice" });
  assert.ok(!Object.hasOwn(value, "healthy"));
});
test("cancelled or superseded model reads discard both success and failure; retry is a fresh read", async () => {
  let release, current = true;
  const pending = readSettingsModels({ readProviders: () => new Promise((resolve) => { release = resolve; }), readPreference: async () => ({}), isCurrent: () => current });
  current = false; release({ providers: [] }); assert.equal(await pending, null);
  assert.equal(await readSettingsModels({ readProviders: async () => { throw new Error("read failed"); }, readPreference: async () => ({}), isCurrent: () => false }), null);
  assert.deepEqual(await readSettingsModels({ readProviders: async () => { throw new Error("read failed"); }, readPreference: async () => ({}), isCurrent: () => true }), { status: "error" });
  assert.deepEqual(await readSettingsModels({ readProviders: async () => ({ providers: [] }), readPreference: async () => ({}), isCurrent: () => true }), { status: "ready", configured: 0, defaultName: "" });
});

for (const mode of ['standard', 'trial', 'continuous']) test(`compiled Company consent ${mode} preserves unknown save identity and revocation`, async () => {
  const trialMode = mode === 'trial', continuousMode = mode === 'continuous';
  const vm = await import('node:vm'), require = createRequire(import.meta.url), swc = require('next/dist/build/swc');
  await swc.loadBindings();
  const {code} = await swc.transform(readFileSync(new URL('../app/ceo-office/settings/page.js', import.meta.url),'utf8'), {filename:'settings.js',jsc:{parser:{syntax:'ecmascript',jsx:true},transform:{react:{runtime:'automatic'}}},module:{type:'commonjs'}});
  let cursor=0, tree, fail=true, sequence=0;
  const slots=[], effects=[], calls=[];
  const same=(a,b)=>a&&b&&a.length===b.length&&a.every((v,i)=>Object.is(v,b[i]));
  const hooks={useState(initial){const i=cursor++;if(!(i in slots))slots[i]={value:initial};return[slots[i].value,(v)=>{slots[i].value=typeof v==='function'?v(slots[i].value):v;}];},useRef(initial){const i=cursor++;return slots[i]||={current:initial};},useEffect(fn,deps){const i=cursor++,old=slots[i];if(!old||!same(old.deps,deps)){slots[i]={deps};effects.push(()=>{old?.cleanup?.();slots[i].cleanup=fn();});}}};
  let view={company_id:'A',policy:null,preview_token:'verified-preview',totals:{reserved_micro_cny:0,estimated_micro_cny:0},workspaces:[{workspace_id:'W',name:'实际工作空间'}],models:[{model_key:'m',display_name:'模型',destination:'https://api.deepseek.com'}],price:{checked_at:'fixture',valid_until:'fixture',input_cny_per_million:2,output_cny_per_million:8,source_cny:'https://api-docs.deepseek.com/zh-cn/quick_start/pricing/'},max_input_bytes:4096,max_output_tokens:2048,per_request_ceiling_cny:'0.025088'};
  if (continuousMode) view.policy={revision:'old-trial',trial_authorization_ref:'server-trial',workspace_ids:['W'],models:[{model_key:'m'}],budget_micro_cny:100000,enabled:true,expires_at:'2020-01-01T00:00:00Z'};
  const api={getCompanyTextPolicy:async()=>structuredClone(view),saveCompanyTextPolicy:async(company,value)=>{calls.push({company,value:structuredClone(value)});if(fail)throw Error('unknown transport');view={...view,continuity:{status:'VALID',needs_reconfirmation:false,history_incomplete:Boolean(view.continuity?.history_incomplete),can_confirm:true,token:'state-'+calls.length},totals:{reserved_micro_cny:0,estimated_micro_cny:0},policy:{...value,...((value.authorization_mode==='synthetic_continuous'||view.policy?.test_authorization_ref)?{test_authorization_ref:'server-continuous'}:{}),...((value.authorization_mode==='synthetic_trial'||view.policy?.trial_authorization_ref)?{trial_authorization_ref:'server-trial'}:{}),revision:'r'+calls.length,expires_at:'fixture',budget_micro_cny:100000,models:[{model_key:'m'}]}};return{policy:view.policy};}};
  const module={exports:{}};
  vm.runInNewContext(code,{module,exports:module.exports,URLSearchParams,crypto:{randomUUID:()=>`save-${++sequence}`},require:(name)=>name==='react'?hooks:name==='react/jsx-runtime'?require(name):name.includes('v1FrontendApi')?api:name.endsWith('.css')?{__esModule:true,default:{}}:{}});
  const nodes=(root,predicate)=>{const result=[];function walk(n){if(!n||typeof n!=='object')return;if(Array.isArray(n)){n.forEach(walk);return;}if(predicate(n))result.push(n);walk(n.props?.children);}walk(root);return result;};
  const text=(n)=>typeof n==='string'?n:Array.isArray(n)?n.map(text).join(''):n?.props?text(n.props.children):'';
  const render=()=>{cursor=0;tree=module.exports.CompanyTextConsent({companyId:'A'});while(effects.length)effects.shift()();return tree;};
  const flush=async()=>{for(let i=0;i<4;i++){render();await new Promise(r=>setImmediate(r));}render();};
  const button=(label)=>nodes(tree,n=>n.type==='button'&&text(n)===label)[0];
  await flush();assert.equal(calls.length,0);assert.equal(button('保存文字许可').props.disabled,true);
  const trialBox=()=>nodes(tree,n=>n.props?.['aria-label']==='本轮合成验收受限授权')[0];
  assert.equal(trialBox().props.checked,continuousMode,'old trial is retained; new authorization defaults off');
  const continuousBox=()=>nodes(tree,n=>n.props?.['aria-label']==='本轮持续合成验收授权')[0];
  assert.equal(continuousBox().props.checked,false);
  if (continuousMode) {
    assert.match(text(tree), /文字许可已过期/);
    assert.doesNotMatch(text(tree), /已保存许可，有效至/);
  }
  if(continuousMode){continuousBox().props.onChange({target:{checked:true}});render();assert.ok(text(tree).includes('不会自动停止'));assert.equal(button('保存文字许可').props.disabled,true);}
  if(trialMode){trialBox().props.onChange({target:{checked:true}});render();assert.ok(text(tree).includes('实际费用未知时停止后续调用'));}
  for(const box of nodes(tree,n=>n.type==='input'&&n.props.type==='checkbox'&&!n.props.checked&&!['本轮合成验收受限授权','本轮持续合成验收授权'].includes(n.props['aria-label'])))box.props.onChange({target:{checked:true}});
  nodes(tree,n=>n.type==='input'&&n.props.type==='number')[0].props.onChange({target:{value:'0.1'}});render();
  assert.equal(button('保存文字许可').props.disabled,false);await button('保存文字许可').props.onClick();render();
  assert.equal(calls.length,1);assert.equal(button('保存文字许可').props.disabled,true);
  assert.equal(calls[0].value.authorization_mode,continuousMode?'synthetic_continuous':trialMode?'synthetic_trial':undefined);
  assert.equal(calls[0].value.budget_cny,'0.1');
  assert.equal(nodes(tree,n=>n.type==='fieldset')[0].props.disabled,true);
  fail=false;await button('重试原保存请求').props.onClick();await flush();
  assert.deepEqual(calls[0],calls[1]);assert.equal(calls[1].value.consent,true);assert.deepEqual(calls[1].value.workspace_ids,['W']);
  assert.equal(button('保存文字许可').props.disabled,true);
  await button('撤销后续文字执行').props.onClick();await flush();
  assert.equal(calls.at(-1).value.enabled,false);assert.equal(calls.at(-1).value.expected_revision,'r2');
  assert.ok(text(tree).includes('当前未授权文字执行'));assert.equal(button('撤销后续文字执行').props.disabled,true);
  if(continuousMode){assert.equal(continuousBox().props.checked,true);assert.equal(continuousBox().props.disabled,true);assert.ok(text(tree).includes('¥10 仅作参考'));return;}
  if(trialMode){
    assert.equal(trialBox().props.checked,true);assert.equal(trialBox().props.disabled,true);
    assert.ok(text(tree).includes('不能改为普通授权解除限制'));
    const before=calls.length;await button('重新读取文字许可').props.onClick();await flush();
    assert.equal(calls.length,before);assert.equal(trialBox().props.checked,true);
    return;
  }
  const beforeRestoreRead=calls.length;
  view={...view,policy:{...view.policy,enabled:true},continuity:{status:'MISMATCH',needs_reconfirmation:true,history_incomplete:true,can_confirm:true,token:'restored-state'},totals:{reserved_micro_cny:null,estimated_micro_cny:null}};
  await button('重新读取文字许可').props.onClick();await flush();
  assert.equal(calls.length,beforeRestoreRead,'metadata read does not authorize or replay');
  assert.ok(text(tree).includes('旧费用授权已失效'));
  assert.ok(text(tree).includes('历史费用不可完整核实'));
  assert.ok(!text(tree).includes('¥0.000000'),'unknown historic cost is not rendered as zero');
  assert.equal(nodes(tree,n=>n.type==='input'&&n.props.type==='number')[0].props.value,'');
  assert.equal(button('保存文字许可').props.disabled,true);
  nodes(tree,n=>n.type==='input'&&n.props.type==='number')[0].props.onChange({target:{value:'0.05'}});
  nodes(tree,n=>n.type==='input'&&n.props.type==='checkbox').at(-1).props.onChange({target:{checked:true}});render();
  await button('保存文字许可').props.onClick();await flush();
  assert.equal(calls.at(-1).value.history_acknowledged,true);
  assert.equal(calls.at(-1).value.budget_cny,'0.05');
  assert.ok(text(tree).includes('重新确认后累计估算'));
  assert.ok(text(tree).includes('不代表历史费用已结清'));
  view={...view,continuity:{status:'UNVERIFIABLE',needs_reconfirmation:true,history_incomplete:true,can_confirm:false,token:'bad-state'}};
  await button('重新读取文字许可').props.onClick();await flush();
  assert.equal(button('保存文字许可').props.disabled,true);
  assert.ok(text(tree).includes('请保留现场处理'));
});
