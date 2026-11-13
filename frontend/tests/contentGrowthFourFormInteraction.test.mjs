import test from "node:test";
import assert from "node:assert/strict";
import { CG_PACKAGE, CG_PACKAGE_V02, CG_FORMATS, isContentGrowthPackage, cgDraftOf, defaultCgWork, shotSelectionFor, selectionCurrent, cgInputKey, cgInputSnapshot, restoreCgInput, clearCreatedCgInput, contentHref, cgReturnTarget, cgSelectionFromEntry, cgScriptProjection, cgChecksMatch, cgReferenceLabel, cgReferenceLabels } from "../lib/contentGrowthState.mjs";
import { validateContentGrowthReturn } from "../lib/contentGrowthApi.js";
import { validateBusinessReturn } from "../lib/businessReturnApi.js";
const workspace = "four-workspace";
function detail(p) { return { instance: { company_id: "A", instance_id: "installed-four", workspace_id: workspace, status: "ACTIVE", package_id: p.id, package_version: p.version, package_digest: p.digest }, package: { package_id: p.id, version: p.version, digest: p.digest, schema_version: "curis.workspace-package/v1", status: "ACTIVE" }, schemas: { [p.version === "0.1.0" ? "ContentGraphic" : "ContentWork"]: { schemaVersion: p.version } }, read_only: false }; }
function row() { return { content: { entity_id: "one", company_id: "A", workspace_id: workspace }, version: { entity_id: "v1", data: { title: "输入", topic: "主题", audience: "受众", body: "雨后😀", format: "speech", references: [], work: { ...defaultCgWork(), shots: [{ id: "shot1", title: "开场", description: "实际脚本", caption: "", camera: "", sound: "", duration: 12 }] } } } }; }
const entry = (p = CG_PACKAGE_V02) => ({ entry: { actor: "owner", scope: { tenant_id: "selfuse", company_id: "A", workspace_id: workspace, scope_type: "WORKSPACE", scope_ref: workspace }, definition: { package_id: p.id, version: p.version, digest: p.digest } } });
test("exact candidate plus old package accepted without digest substitution", () => {
  assert.ok(isContentGrowthPackage(detail(CG_PACKAGE))); assert.ok(isContentGrowthPackage(detail(CG_PACKAGE_V02)));
  const bad = detail(CG_PACKAGE_V02); bad.instance.package_digest = CG_PACKAGE.digest; assert.equal(isContentGrowthPackage(bad), false);
});
test("explicit four-form new draft has empty body and unconfirmed media intent", () => {
  assert.deepEqual(Object.keys(CG_FORMATS), ["graphic", "short_video", "long_video", "speech"]);
  const input = cgDraftOf(null, true); assert.equal(input.body, ""); assert.equal(input.work.output_intent, "UNCONFIRMED"); assert.deepEqual(input.work.source_refs, []);
  assert.equal(cgDraftOf(null).work, undefined);
});
test("actual source continuation keeps source/version and never fills body", () => {
  const sources = [{ reference_id: "real-source", version_ref: "actual-v1", purpose: "CONTEXT" }];
  const input = cgDraftOf(null, true, sources); assert.equal(input.body, ""); assert.deepEqual(input.work.source_refs, sources); assert.equal(input.work.model_key, "");
});
test("shot original snapshot is immutable and old version cannot become current", () => {
  const original = row().version, selected = shotSelectionFor(original, "shot1");
  const current = structuredClone(original); current.entity_id = "v2"; current.data.work.shots[0].caption = "new";
  assert.equal(selected.shot_snapshot.caption, ""); assert.ok(selectionCurrent(selected, original, original.data.body)); assert.equal(selectionCurrent(selected, current, current.data.body), false);
  assert.throws(() => shotSelectionFor(original, "foreign"));
});
test("source-continuation cache is independent from ordinary new work", () => {
  const creationSource = JSON.stringify([{ reference_id: "source", version_ref: "v1" }]);
  const context = { company: "A", workspace, content: "new", actor: "owner", tenant: "selfuse", creationSource };
  const key = cgInputKey("A", workspace, null, creationSource); assert.notEqual(key, cgInputKey("A", workspace, null));
  const draft = cgDraftOf(null, true), saved = JSON.stringify(cgInputSnapshot(context, { draft }));
  assert.ok(restoreCgInput(saved, context)); assert.equal(restoreCgInput(saved, { ...context, creationSource: "other" }), null);
  const map = new Map([[key, saved]]), storage = { getItem: (k) => map.get(k), removeItem: (k) => map.delete(k) };
  assert.ok(clearCreatedCgInput(storage, key, context, draft, { content: { entity_id: "created", company_id: "A", workspace_id: workspace } })); assert.equal(map.size, 0);
});
test("CG return validates exact v02 definition via original authenticated seam", async () => {
  const value = `/ceo-office/workspace/installed/${workspace}`;
  assert.equal((await validateContentGrowthReturn(value, "A", { collection: async () => entry() })).company, "A");
  await assert.rejects(validateContentGrowthReturn(value, "A", { collection: async () => ({ ...entry(), entry: { ...entry().entry, definition: { ...entry().entry.definition, digest: CG_PACKAGE.digest } } }) }));
});
test("cross-company return v02 still authorizes through existing request without identity override", async () => {
  const value = `/ceo-office/workspace/installed/${workspace}`, calls = [];
  const result = await validateBusinessReturn("cg", value, { request: async (path, options) => { calls.push({ path, options }); return path.includes("/content-growth/") ? entry() : detail(CG_PACKAGE_V02); } });
  assert.equal(result.company, "A"); assert.equal(calls.length, 2); assert.ok(calls.every((c) => c.options === undefined));
  await assert.rejects(validateBusinessReturn("cg", value, { employeeCompany: "foreign", request: async () => detail(CG_PACKAGE_V02) }));
});

test("shot repair round trip reads canonical saved snapshot and old version stays readonly", async () => {
  const record = row(); record.versions = [record.version];
  const href = contentHref(workspace, { content: "one", version: "v1", shot: "shot1" });
  const target = cgReturnTarget(href); assert.equal(target.entry.shot, "shot1");
  const selected = cgSelectionFromEntry(record, target.entry); assert.deepEqual(selected.shot_snapshot, record.version.data.work.shots[0]);
  const current = structuredClone(record.version); current.entity_id = "v2"; current.data.work.shots[0].description = "changed";
  assert.equal(selectionCurrent(selected, current, current.data.body), false);
  assert.equal(selected.shot_snapshot.description, "实际脚本");
  await validateContentGrowthReturn(href, "A", { collection: async () => entry(), content: async () => record });
  record.content.tenant_id = "selfuse";
  const fromEmployeeOrModel = await validateBusinessReturn("cg", href, { request: async (path) => path.includes("/contents/") ? record : path.includes("/content-growth/") ? entry() : detail(CG_PACKAGE_V02) });
  assert.equal(fromEmployeeOrModel.entry.shot, "shot1");
  await assert.rejects(validateContentGrowthReturn(contentHref(workspace, { content: "one", version: "v1", shot: "foreign" }), "A", { collection: async () => entry(), content: async () => record }));
  assert.throws(() => cgReturnTarget(`${href}&cg_start=0&cg_end=2`));
  assert.throws(() => cgReturnTarget(contentHref(workspace, { content: "one", shot: "shot1" })));
  assert.throws(() => cgReturnTarget(`${href}&cg_shot=other`));
});
test("readonly script projection contains ordinary labels and no raw identity/source IDs", () => {
  const data = row().version.data;
  data.work.assignment_ref = "SECRET_ASSIGNMENT_ID"; data.work.model_key = "SECRET_MODEL_KEY";
  data.work.source_refs = [{ title: "已保存原来源", reference_id: "SECRET_SOURCE_ID", version_ref: "SECRET_VERSION_ID" }];
  data.qualification = { assignment: { context: { name: "脚本作者" } }, model: { model: { display_name: "已选模型" } } };
  const projection = cgScriptProjection(data), text = JSON.stringify(projection);
  assert.equal(projection.employee, "脚本作者"); assert.equal(projection.model, "已选模型"); assert.equal(projection.intent, "尚未确认");
  for (const token of ["SECRET_ASSIGNMENT_ID", "SECRET_MODEL_KEY", "SECRET_SOURCE_ID", "SECRET_VERSION_ID", "shot1"]) assert.equal(text.includes(token), false);
});

test("human checks for an earlier candidate cannot approve a new candidate", () => {
  const checked = { content: true, references: true, account: true };
  assert.ok(cgChecksMatch("old", "old", checked)); assert.equal(cgChecksMatch("new", "old", checked), false);
  assert.equal(cgChecksMatch("new", "new", { ...checked, references: false }), false);
});

// P1 reference-label helper (CURIS-V1-CG-FOUR-FORM-INTERACTION-001, 2026-10-06)
function labeledVersion(entityId, data, scopeRef = {}) {
  return { entity_id: entityId, tenant_id: "selfuse", company_id: "A", workspace_id: workspace, ...scopeRef, data };
}
function labeledItem(id, format, versions, currentId, scopeRef = {}) {
  const content = { entity_id: id, tenant_id: "selfuse", company_id: "A", workspace_id: workspace, current_version_id: currentId, data: { format }, ...scopeRef };
  return { content, version: versions.find((version) => version.entity_id === currentId), versions };
}
const labelScope = { tenant_id: "selfuse", company_id: "A", workspace_id: workspace };

test("reference labels distinguish current item and fixed/history/candidate versions", () => {
  const v1 = labeledVersion("c1-v1", { kind: "draft", title: "周一穿搭", body: "旧正文" });
  const v2 = labeledVersion("c1-v2", { kind: "draft", title: "周一穿搭改版", body: "新正文" });
  const candidate = labeledVersion("c1-ca", { kind: "candidate", title: "候选标题" });
  const contents = [labeledItem("c1", "graphic", [v1, v2, candidate], "c1-v2")];
  assert.equal(cgReferenceLabel({ reference_id: "c1", kind: "CONTENT_ITEM", version_ref: "c1-v2" }, contents, labelScope), "图文 · 当前内容 · 周一穿搭改版");
  assert.equal(cgReferenceLabel({ reference_id: "c1", kind: "CONTENT_ITEM" }, contents, labelScope), "图文 · 当前内容 · 周一穿搭改版");
  assert.equal(cgReferenceLabel({ reference_id: "c1-v2", kind: "CONTENT_VERSION", version_ref: "c1-v2" }, contents, labelScope), "图文 · 固定版本 · 周一穿搭改版");
  assert.equal(cgReferenceLabel({ reference_id: "c1-v1", kind: "CONTENT_VERSION", version_ref: "c1-v1" }, contents, labelScope), "图文 · 历史版本 · 周一穿搭");
  assert.equal(cgReferenceLabel({ reference_id: "c1-ca", kind: "CONTENT_VERSION", version_ref: "c1-ca" }, contents, labelScope), "图文 · 候选 · 候选标题");
});

test("stale pinned item reference keeps old title after head advance and never takes new head", () => {
  const v1 = labeledVersion("c2-v1", { kind: "draft", title: "原选题", body: "原正文" });
  const v2 = labeledVersion("c2-v2", { kind: "draft", title: "新选题", body: "新正文" });
  const contents = [labeledItem("c2", "speech", [v1, v2], "c2-v2")];
  const stale = { reference_id: "c2", kind: "CONTENT_ITEM", title: "原选题", version_ref: "c2-v1", purpose: "CONTEXT", locator: "" };
  const label = cgReferenceLabel(stale, contents, labelScope);
  assert.ok(label.includes("原版本需核对")); assert.ok(label.includes("原选题")); assert.equal(label.includes("新选题"), false);
  const missingPinned = { reference_id: "c2", kind: "CONTENT_ITEM", version_ref: "c2-gone" };
  assert.equal(cgReferenceLabel(missingPinned, contents, labelScope), "来源需核对");
});

test("same-title distinct contents get view-local ordinals in presentation order", () => {
  const a1 = labeledVersion("a-v", { kind: "draft", title: "同款标题" });
  const b1 = labeledVersion("b-v", { kind: "draft", title: "同款标题" });
  const itemA = labeledItem("a", "long_video", [a1], "a-v");
  const itemB = labeledItem("b", "long_video", [b1], "b-v");
  const refs = [{ reference_id: "b", kind: "CONTENT_ITEM", version_ref: "b-v" }, { reference_id: "a", kind: "CONTENT_ITEM", version_ref: "a-v" }];
  const labels = cgReferenceLabels(refs, [itemA, itemB], labelScope);
  assert.equal(labels.get("a"), "长视频 · 当前内容 · 同款标题（来源1）");
  assert.equal(labels.get("b"), "长视频 · 当前内容 · 同款标题（来源2）");
  // Same content referenced twice is not ambiguous.
  const single = cgReferenceLabels([{ reference_id: "a", kind: "CONTENT_ITEM", version_ref: "a-v" }, { reference_id: "a", kind: "CONTENT_ITEM", version_ref: "a-v" }], [itemA, itemB], labelScope);
  assert.equal(single.get("a"), "长视频 · 当前内容 · 同款标题");
});

test("same-title ordinals are dense inside the ambiguous group, not global positions", () => {
  const other1 = labeledVersion("o1-v", { kind: "draft", title: "无关内容一" });
  const same1 = labeledVersion("s1-v", { kind: "draft", title: "重复名字" });
  const other2 = labeledVersion("o2-v", { kind: "draft", title: "无关内容二" });
  const other3 = labeledVersion("o3-v", { kind: "draft", title: "无关内容三" });
  const same2 = labeledVersion("s2-v", { kind: "draft", title: "重复名字" });
  const contents = [
    labeledItem("o1", "graphic", [other1], "o1-v"),
    labeledItem("s1", "long_video", [same1], "s1-v"),
    labeledItem("o2", "graphic", [other2], "o2-v"),
    labeledItem("o3", "speech", [other3], "o3-v"),
    labeledItem("s2", "long_video", [same2], "s2-v"),
  ];
  const labels = cgReferenceLabels([
    { reference_id: "s1", kind: "CONTENT_ITEM", version_ref: "s1-v" },
    { reference_id: "s2", kind: "CONTENT_ITEM", version_ref: "s2-v" },
  ], contents, labelScope);
  assert.equal(labels.get("s1"), "长视频 · 当前内容 · 重复名字（来源1）");
  assert.equal(labels.get("s2"), "长视频 · 当前内容 · 重复名字（来源2）");
});

test("missing, unknown and foreign-scope references all require review", () => {
  const v1 = labeledVersion("c3-v1", { kind: "draft" });
  const local = labeledItem("c3", "graphic", [v1], "c3-v1");
  const foreignVersion = labeledVersion("f-v1", { kind: "draft", title: "别的公司内容" }, { company_id: "B" });
  const foreign = labeledItem("f", "graphic", [foreignVersion], "f-v1", { company_id: "B" });
  const contents = [local, foreign];
  assert.equal(cgReferenceLabel({ reference_id: "c3", kind: "CONTENT_ITEM", version_ref: "c3-v1" }, contents, labelScope), "图文 · 当前内容 · 未命名内容");
  assert.equal(cgReferenceLabel({ reference_id: "ghost", kind: "CONTENT_ITEM", version_ref: "g-v" }, contents, labelScope), "来源需核对");
  assert.equal(cgReferenceLabel({ reference_id: "f", kind: "CONTENT_ITEM", version_ref: "f-v1" }, contents, labelScope), "来源需核对");
  assert.equal(cgReferenceLabel({ reference_id: "x", kind: "UNSUPPORTED_KIND" }, contents, labelScope), "来源需核对");
});

test("non-content kinds keep actual ordinary titles and helper never mutates or exposes ids", () => {
  const refs = [{ reference_id: "w1", workspace_id: workspace, kind: "WORK", title: "选题会纪要", version_ref: "digest", purpose: "BACKGROUND", locator: "" },
    { reference_id: "d1", workspace_id: workspace, kind: "DECISION_PACKET", title: "" }];
  const before = structuredClone(refs);
  const labels = cgReferenceLabels(refs, [], labelScope);
  assert.equal(labels.get("w1"), "工作 · 选题会纪要");
  assert.equal(labels.get("d1"), "决策包 · 未命名来源");
  assert.deepEqual(refs, before);
  for (const label of labels.values()) {
    for (const token of ["w1", "d1", "digest"]) assert.equal(label.includes(token), false);
    assert.equal(typeof label, "string");
  }
});

test("legacy new reference draft preserves qualified source with legacy purpose and no copied body", () => {
  const source = { reference_id: "original-version", kind: "CONTENT_VERSION", version_ref: "original-version", purpose: "CONTEXT" };
  const draft = cgDraftOf(null, false, [source]);
  assert.equal(draft.body, ""); assert.equal(draft.references[0].reference_id, "original-version"); assert.equal(draft.references[0].purpose, "BACKGROUND"); assert.equal(draft.work, undefined); assert.equal(source.purpose, "CONTEXT");
});
