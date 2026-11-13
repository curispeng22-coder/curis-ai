import test from "node:test";
import assert from "node:assert/strict";
import { businessReturnInput, validateBusinessReturn } from "../lib/businessReturnApi.js";
import { TENANT_ID } from "../lib/api.js";
import { CG_PACKAGE, contentHref } from "../lib/contentGrowthState.mjs";
import { cgRepairHref } from "../lib/contentGrowthApi.js";
import { MUSIC_PACKAGE, MUSIC_PACKAGES, songHref, operatingHref } from "../lib/musicState.mjs";
import { musicRepairHref } from "../lib/musicApi.js";
import { WRITING_PACKAGE, chapterHref } from "../lib/writingState.mjs";
import { writingRepairHref } from "../lib/writingApi.js";

function fixture(kind, { company = "B", definition = kind === "cg" ? CG_PACKAGE : kind === "music" ? MUSIC_PACKAGE : WRITING_PACKAGE } = {}) {
  const scope = { tenant_id: TENANT_ID, company_id: company, workspace_id: "w", scope_type: "WORKSPACE", scope_ref: "w" };
  const instance = { instance_id: "i", company_id: company, workspace_id: "w", package_id: definition.id,
    package_version: definition.version, package_digest: definition.digest, status: "ACTIVE" };
  const detail = { instance, read_only: false, package: { package_id: definition.id, version: definition.version, digest: definition.digest, status: "ACTIVE", schema_version: "curis.workspace-package/v1" },
    schemas: { ContentGraphic: { schemaVersion: definition.version }, MusicSong: { schemaVersion: definition.version }, WritingBook: { schemaVersion: "writing.book/v1" }, WritingChapter: { schemaVersion: "writing.chapter/v1" } } };
  const collection = kind === "writing"
    ? { scope: { ...scope, ...instance, package_version: definition.version, package_digest: definition.digest }, books: [{ ref: "book" }], chapters: [{ ref: "chapter", bookRef: "book" }] }
    : { entry: { scope, actor: "verified-ceo", definition: { package_id: definition.id, version: definition.version, digest: definition.digest } } };
  const holder = { tenant_id: TENANT_ID, company_id: company, workspace_id: "w" };
  const content = { content: { ...holder, entity_id: "content" }, versions: [{ entity_id: "version" }] };
  const song = { song: { ...holder, entity_id: "song" }, versions: [{ ...holder, entity_id: "lyrics", parent_id: "song", data: { kind: "LyricsVersion", text: "原歌词😀" } }], candidates: [], assets: [] };
  const chapter = { scope: { ...collection.scope, book_ref: "book", chapter_ref: "chapter" } };
  const record = { record: { ...holder, entity_id: "music-report-original", data: { kind: "Report" } } };
  const calls = [];
  const state = { detail, collection, content, song, chapter, record, forbidden: false };
  const request = async (path, options) => {
    calls.push({ path, options });
    assert.equal(options, undefined, "no identity headers or execution override");
    if (path === "/api/workspace/packages/workspaces/w") return structuredClone(state.detail);
    assert.ok(path.startsWith(`/api/workspace/v1/companies/${company}/`), path);
    if (state.forbidden) { const error = new Error("real request rejected fixture"); error.status = state.forbidden; throw error; }
    if (path.includes("/discussion/")) return { request: { verified_by_existing_backend: true } };
    if (path.includes("/contents/")) return structuredClone(state.content);
    if (path.includes("/songs/")) return structuredClone(state.song);
    if (path.includes("/chapters/")) return structuredClone(state.chapter);
    if (path.includes("/operating/")) return structuredClone(state.record);
    return structuredClone(state.collection);
  };
  const href = kind === "cg" ? contentHref("w", { content: "content", version: "version" })
    : kind === "music" ? songHref("w", { song: "song", lyrics: "lyrics" })
      : chapterHref("w", { mode: "chapter", book: "book", chapter: "chapter" });
  return { state, calls, request, href };
}

for (const kind of ["cg", "music", "writing"]) {
  test(`${kind}: source B survives default A without changing or authorizing default Company`, async () => {
    const f = fixture(kind), runtime = Object.freeze({ companyId: "A", status: "ready" });
    for (const options of [{}, { employeeCompany: "B" }]) {
      const result = await validateBusinessReturn(kind, f.href, { ...options, request: f.request });
      assert.equal(result.company, "B"); assert.equal(result.href, f.href); assert.equal(runtime.companyId, "A");
    }
    assert.ok(f.calls.some(c => c.path.startsWith("/api/workspace/v1/companies/B/")));
    assert.ok(!f.calls.some(c => c.path.includes("/companies/A/")));
  });
  test(`${kind}: metadata alone and same-tenant foreign Company never authorize a return`, async () => {
    for (const status of [403, 404]) {
      const f = fixture(kind); f.state.forbidden = status;
      await assert.rejects(validateBusinessReturn(kind, f.href, { request: f.request }));
      assert.equal(f.calls.length, 2);
    }
    const f = fixture(kind);
    await assert.rejects(validateBusinessReturn(kind, f.href, { employeeCompany: "A", request: f.request }));
    assert.equal(f.calls.length, 1);
    await assert.rejects(validateBusinessReturn(kind, f.href, { employeeCompany: "", request: f.request }));
  });
  test(`${kind}: original scope, active instance and exact package must agree`, async () => {
    for (const mutate of [
      s => { s.detail.instance.workspace_id = "foreign"; },
      s => { s.detail.instance.instance_id = ""; },
      s => { s.detail.instance.status = "DISABLED"; },
      s => { s.detail.package.status = "DISABLED"; },
      s => { delete s.detail.read_only; },
      s => { s.detail.instance.package_digest = "wrong"; },
      s => { (s.collection.scope || s.collection.entry.scope).tenant_id = "foreign"; },
      s => { (s.collection.scope || s.collection.entry.scope).company_id = "A"; },
      s => { (s.collection.scope || s.collection.entry.scope).workspace_id = "foreign"; },
    ]) {
      const f = fixture(kind); mutate(f.state);
      await assert.rejects(validateBusinessReturn(kind, f.href, { request: f.request }));
    }
  });
}

test("outer return is finite; legacy writing and employee conversation branch remain", () => {
  const href = fixture("writing").href;
  assert.deepEqual(businessReturnInput(new URLSearchParams({ return_to: href })), { kind: "writing", value: href });
  assert.equal(businessReturnInput(new URLSearchParams()), null);
  assert.equal(businessReturnInput(new URLSearchParams({ return_to: "/ceo-office/conversation?conversation_id=original" }), { allowConversation: true }), null);
  for (const params of [
    new URLSearchParams(`return_to=${encodeURIComponent(href)}&return_to=${encodeURIComponent(href)}`),
    new URLSearchParams({ return_to: href, return_kind: "unknown" }),
    new URLSearchParams({ return_to: href, return_kind: "__proto__" }),
    new URLSearchParams({ return_kind: "cg" }),
    new URLSearchParams({ return_to: href, company_id: "B" }),
    new URLSearchParams(`return_to=${encodeURIComponent(href)}&return_kind=writing&return_kind=music`),
    new URLSearchParams({ return_to: href, return_kind: "music" }),
  ]) assert.throws(() => businessReturnInput(params));
});

test("no arbitrary URL Company, external origin or cross-business target is an authorization input", async () => {
  for (const kind of ["cg", "music", "writing"]) {
    for (const value of ["https://foreign.invalid/", "//foreign.invalid/", "/ceo-office/workspace/installed/%2e%2e", "/ceo-office/workspace/installed/w?company_id=B"]) {
      const f = fixture(kind); await assert.rejects(validateBusinessReturn(kind, value, { request: f.request })); assert.equal(f.calls.length, 0);
    }
  }
  const f = fixture("music"); f.state.detail = fixture("cg").state.detail;
  await assert.rejects(validateBusinessReturn("music", f.href, { request: f.request }));
});

test("CG original version/attempt and tenant stay bound; historical version is not retargeted", async () => {
  const f = fixture("cg");
  assert.equal((await validateBusinessReturn("cg", f.href, { request: f.request })).entry.version, "version");
  f.state.content.versions = []; await assert.rejects(validateBusinessReturn("cg", f.href, { request: f.request }));
  f.state.content.versions = [{ entity_id: "version" }]; f.state.content.content.tenant_id = "foreign";
  await assert.rejects(validateBusinessReturn("cg", f.href, { request: f.request }));
  const a = fixture("cg"), href = contentHref("w", { content: "content", binding: "binding", attempt: "attempt" });
  const failAttempt = async (path, options) => { if (path.includes("/discussion/")) throw new Error("original attempt rejected"); return a.request(path, options); };
  await assert.rejects(validateBusinessReturn("cg", href, { request: failAttempt }));
});

test("Music legacy installed definition and immutable Operating return are both retained", async () => {
  const legacy = fixture("music", { definition: MUSIC_PACKAGES[1] });
  assert.equal((await validateBusinessReturn("music", legacy.href, { request: legacy.request })).entry.lyrics, "lyrics");
  const f = fixture("music"), href = operatingHref("w", { view: "report", object: "music-report-original", period: "original-period", song: "song" });
  const result = await validateBusinessReturn("music", href, { request: f.request });
  assert.equal(result.operating.object, "music-report-original"); assert.equal(result.operating.period, "original-period");
  f.state.record.record.company_id = "A"; await assert.rejects(validateBusinessReturn("music", href, { request: f.request }));
});

test("Writing instance/chapter and CG/Music actor/workspace scopes fail closed", async () => {
  const f = fixture("writing"); f.state.collection.scope.instance_id = "another";
  await assert.rejects(validateBusinessReturn("writing", f.href, { request: f.request }));
  const w = fixture("writing"); w.state.chapter.scope.chapter_ref = "another";
  await assert.rejects(validateBusinessReturn("writing", w.href, { request: w.request }));
  for (const kind of ["cg", "music"]) for (const mutate of [s => { s.collection.entry.actor = ""; }, s => { s.collection.entry.actor = { owner: true }; }, s => { s.collection.entry.scope.scope_type = "COMPANY"; }]) {
    const x = fixture(kind); mutate(x.state); await assert.rejects(validateBusinessReturn(kind, x.href, { request: x.request }));
  }
});
test("Employee Bar repair links retain the exact three-domain return and reject malformed ranges", async () => {
  const helpers = { cg: cgRepairHref, music: musicRepairHref, writing: writingRepairHref };
  for (const kind of ["cg", "music", "writing"]) {
    const f = fixture(kind), path = "/ceo-office/organization/employees/emp-1";
    const linked = helpers[kind](path, f.href);
    const input = businessReturnInput(new URL(linked, "http://localhost").searchParams);
    assert.deepEqual(input, { kind, value: f.href });
    const verified = await validateBusinessReturn(input.kind, input.value, { employeeCompany: "B", request: f.request });
    assert.equal(verified.href, f.href);
    const wrong = fixture(kind);
    await assert.rejects(validateBusinessReturn(input.kind, input.value, { employeeCompany: "A", request: wrong.request }));
    assert.throws(() => helpers[kind]("/ceo-office/organization/employees/../other", f.href));
  }
  assert.throws(() => cgRepairHref("/ceo-office/organization/employees/emp-1", contentHref("w", { content: "content", version: "version", start: 3, end: 2 })));
  assert.throws(() => musicRepairHref("/ceo-office/organization/employees/emp-1", "/ceo-office/workspace/installed/w?music_song=song&music_lyrics=lyrics&music_start=3&music_end=2"));
  assert.throws(() => writingRepairHref("/ceo-office/organization/employees/emp-1", "/ceo-office/workspace/installed/w?writing_mode=chapter&book_ref=book"));
});


test("compiled Shared return chain validates source independently of denied conversation and discards stale results", async () => {
  const { readFileSync } = await import("node:fs");
  const { createRequire } = await import("node:module"), vm = await import("node:vm");
  const require = createRequire(import.meta.url), React = require("react"), swc = require("next/dist/build/swc");
  await swc.loadBindings();
  const compile = async (path) => (await swc.transform(readFileSync(new URL(`../${path}`, import.meta.url), "utf8"), {
    filename: path, isModule: true, jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } }, module: { type: "commonjs" },
  })).code;
  const pageCode = await compile("app/ceo-office/organization/employees/[id]/page.js");
  const page = { exports: {} };
  vm.runInNewContext(pageCode, { module: page, exports: page.exports, URLSearchParams, require: (name) => name.endsWith("businessReturnApi.js") ? { businessReturnInput } : {} });
  const returnCode = await compile("components/delivery/d1/D1Surface.js");
  const tick = () => new Promise((resolve) => setImmediate(resolve));
  const scene = (request) => {
    const slots = [], effects = []; let cursor = 0;
    const hooks = {
      useState(initial) { const i = cursor++; slots[i] ||= { value: initial }; return [slots[i].value, value => { slots[i].value = value; }]; },
      useEffect(fn, deps) { const i = cursor++; if (!slots[i] || deps.some((v, j) => v !== slots[i].deps[j])) { const previous = slots[i]; slots[i] = { deps }; effects.push(() => { previous?.cleanup?.(); slots[i].cleanup = fn(); }); } },
    };
    const loaded = { exports: {} };
    vm.runInNewContext(returnCode, { module: loaded, exports: loaded.exports, URLSearchParams,
      require: name => name === "react" ? hooks : name === "react/jsx-runtime" ? require(name)
        : name.endsWith("businessReturnApi.js") ? { businessReturnInput, validateBusinessReturn: (kind, href) => validateBusinessReturn(kind, href, { request }) }
          : name.endsWith(".css") ? { __esModule: true, default: {} } : {} });
    return (search, companyId = "A") => { cursor = 0; const tree = loaded.exports.BusinessConversationReturn({ search, companyId }); while (effects.length) effects.shift()(); return tree; };
  };
  for (const kind of ["cg", "music", "writing"]) {
    const f = fixture(kind), verified = await validateBusinessReturn(kind, f.href, { employeeCompany: "B", request: f.request });
    const query = new URLSearchParams({ return_kind: kind, return_to: f.href }).toString();
    const employee = { id: "employee-B", company_id: "B" };
    const target = page.exports.employeeConversationReturn(query, query, "ready", employee, employee.id, { [kind]: verified });
    assert.equal(target.href, f.href); assert.equal(target.kind, kind);
    for (const args of [
      [query, "stale", "ready", employee, employee.id, { [kind]: verified }],
      [query, query, "loading", employee, employee.id, { [kind]: verified }],
      [query, query, "ready", { ...employee, company_id: "foreign" }, employee.id, { [kind]: verified }],
      [query, query, "ready", employee, "other-employee", { [kind]: verified }],
      [query, query, "ready", employee, employee.id, { [kind]: { ...verified, href: "/another" } }],
    ]) assert.equal(page.exports.employeeConversationReturn(...args), null);
    const render = scene(f.request);
    assert.equal(render(query), null); await tick();
    const link = render(query); assert.equal(link.type, "a"); assert.equal(link.props.href, f.href);
    assert.ok(f.calls.every(call => !call.path.includes("/conversations") && !call.path.includes("/companies/A/")), "return validation cannot read, authorize or execute the denied conversation in default Company A");
    assert.equal(render(query, "changed-default"), null, "company change immediately suppresses old validated link");
  }
  for (const change of [f => { f.state.forbidden = 403; }, f => { f.state.content.content.company_id = "foreign"; }]) {
    const f = fixture("cg"); change(f); const query = new URLSearchParams({ return_kind: "cg", return_to: f.href }).toString(), render = scene(f.request);
    render(query); await tick(); assert.equal(render(query), null);
  }
  for (const query of [
    "", "return_to=https%3A%2F%2Fforeign.invalid&return_kind=cg",
    `return_kind=cg&return_to=${encodeURIComponent(fixture("cg").href)}&return_to=other`,
    `return_kind=music&return_to=${encodeURIComponent(fixture("cg").href)}`,
    "return_to=%2Fceo-office%2Fmeeting%3Fmeeting%3Dm",
  ]) {
    const f = fixture("cg"), render = scene(f.request); render(query); await tick(); assert.equal(render(query), null);
  }
  const f = fixture("cg"); let release;
  const delayed = async (path, options) => { if (path === "/api/workspace/packages/workspaces/w") await new Promise(resolve => { release = resolve; }); return f.request(path, options); };
  const render = scene(delayed), query = new URLSearchParams({ return_kind: "cg", return_to: f.href }).toString();
  render(query); render(""); release(); await tick(); assert.equal(render(""), null, "obsolete verified request cannot restore a link");
  const surface = readFileSync(new URL("../components/delivery/d1/D1Surface.js", import.meta.url), "utf8");
  assert.match(surface, /entry.view === "conversation" && <BusinessConversationReturn/);
  assert.match(surface, /meetingReturn && <a[^>]+href=\{meetingReturn\}/);
});
