export const CG_PACKAGE = Object.freeze({ id: "com.curis.local.content-growth", version: "0.1.0", digest: "aec85f973ca864f581c8fe6f800b68a1b9c23dc25ad5e194ca4e61e9edddcc0d" });
export const CG_PACKAGE_V02 = Object.freeze({ id: CG_PACKAGE.id, version: "0.2.0", digest: "90cc938b70d64a4888385ec40a6844879881409511e9544dec354ef91882a0a6" });
export const CG_VIEWS = Object.freeze(["operating", "market", "production", "analysis", "materials", "learning", "accounts", "verify", "observe"]);
export const CG_FORMATS = Object.freeze({ graphic: "图文", short_video: "短视频", long_video: "长视频", speech: "口播" });
export const cgDefinition = (version) => [CG_PACKAGE, CG_PACKAGE_V02].find((p) => p.version === version);
export function cgScopedRead(payload, company, workspace) {
  const scope = payload?.entry?.scope, definition = payload?.entry?.definition;
  const expected = cgDefinition(definition?.version);
  if (!scope?.tenant_id || scope.company_id !== company || scope.workspace_id !== workspace
    || !expected || definition.package_id !== expected.id || definition.digest !== expected.digest) throw new Error("内容范围或版本已变化，请从原工作区重新进入。");
  return payload;
}
export const defaultCgWork = (sources = []) => ({ goal: "", shots: [], recording_requirements: "", output_intent: "UNCONFIRMED", output_spec: "", source_refs: sources, assignment_ref: "", recipient_ref: "", model_key: "" });
export function cgDraftOf(row, fourForm = false, sources = []) {
  const data = row?.version.data;
  const draft = { title: data?.title || "", topic: data?.topic || "", audience: data?.audience || "", body: data?.body || "", target_account_refs: [], references: data?.references || (!row && !fourForm ? sources.map((source) => ({ ...source, purpose: "BACKGROUND" })) : []) };
  return fourForm ? { ...draft, format: data?.format || "graphic", work: data?.work || defaultCgWork(sources) } : draft;
}
export function shotSelectionFor(version, shotId) {
  const shot = version.data.work?.shots.find((s) => s.id === shotId);
  if (!shot || ![shot.title, shot.description, shot.caption].some((text) => text.trim())) throw new Error("先保存有效镜头，再选择原版本依据。");
  return { version_ref: version.entity_id, locator: "shot", shot_id: shotId, shot_snapshot: JSON.parse(JSON.stringify(shot)) };
}
export const requestLocked = (status) => ["RUNNING", "UNKNOWN", "UNVERIFIED"].includes(status);
export function isContentGrowthPackage(detail) {
  const p = detail?.package, i = detail?.instance;
  const definition = cgDefinition(p?.version);
  return Boolean(p && i && definition && p.package_id === definition.id && p.digest === definition.digest
    && i.package_id === p.package_id && i.package_version === p.version && i.package_digest === p.digest
    && p.schema_version === "curis.workspace-package/v1" && detail.schemas?.[p.version === CG_PACKAGE.version ? "ContentGraphic" : "ContentWork"]?.schemaVersion === p.version);
}
export function cgEntry(params) {
  const content = params.get("cg_content") || "", version = params.get("cg_version") || "";
  const candidate = params.get("cg_candidate") || "";
  const binding = params.get("cg_binding") || "", attempt = params.get("cg_attempt") || "";
  const start = params.get("cg_start"), end = params.get("cg_end"), shot = params.get("cg_shot") || "";
  const view = params.get("cg_view") || "";
  const sourcesRaw = params.get("cg_sources") || "";
  const sources = sourcesRaw ? sourcesRaw.split(",").filter((s) => s.trim()) : [];
  if (view && !CG_VIEWS.includes(view)) return { error: "请从当前内容入口重新进入。" };
  if (sources.length > 8) return { error: "引用素材超出边界。" };
  if ((!content && (version || candidate || binding || attempt || shot || start !== null || end !== null))
    || params.getAll("cg_candidate").length > 1 || candidate && (!version || !/^[A-Za-z0-9._:-]{1,256}$/.test(candidate) || [".", ".."].includes(candidate))
    || params.has("cg_shot") && (!shot || params.getAll("cg_shot").length !== 1)
    || shot && (!version || start !== null || end !== null || !/^[A-Za-z0-9._:-]{1,128}$/.test(shot) || [".", ".."].includes(shot)) || Boolean(binding) !== Boolean(attempt)
    || (start !== null || end !== null) && (!version || !/^\d+$/.test(start || "") || !/^\d+$/.test(end || "") || Number(end) <= Number(start))) return { error: "请从当前内容入口重新进入。" };
  const object=params.get("cg_object")||"", account=params.get("cg_account")||"", period=params.get("cg_period")||"", media=params.get("cg_media")||"";
  if ([object,account,period,media].some(v=>v.length>256||/[\\\u0000-\u001f]/.test(v)) || ["cg_object","cg_account","cg_period","cg_media"].some(k=>params.getAll(k).length>1)) return {error:"原经营位置无效。"};
  return { object, account, period, media, content, version, candidate, binding, attempt, shot, start: start === null ? null : Number(start), end: end === null ? null : Number(end), view, sources };
}
export function contentHref(workspace, entry = {}) {
  const p = new URLSearchParams();
  for (const [key, value] of Object.entries({ cg_object:entry.object,cg_account:entry.account,cg_period:entry.period,cg_media:entry.media,cg_content: entry.content, cg_version: entry.version, cg_candidate: entry.candidate, cg_binding: entry.binding, cg_attempt: entry.attempt, cg_start: entry.start, cg_end: entry.end, cg_shot: entry.shot, cg_view: entry.view, cg_sources: entry.sources?.length ? entry.sources.join(",") : undefined })) if (value !== undefined && value !== null && value !== "") p.set(key, String(value));
  return `/ceo-office/workspace/installed/${encodeURIComponent(workspace)}${p.size ? `?${p}` : ""}`;
}
export function selectionFor(version, text, start, end) {
  if (text !== version.data.body || !Number.isInteger(start) || !Number.isInteger(end) || start < 0 || end <= start || end > text.length) throw new Error("先保存正文，再重新选择片段。");
  for (const n of [start, end]) if (n > 0 && /[\uD800-\uDBFF]/u.test(text[n - 1]) && /[\uDC00-\uDFFF]/u.test(text[n] || "")) throw new Error("选段不能拆开字符。");
  return { version_ref: version.entity_id, start, end, excerpt: text.slice(start, end), locator: "body" };
}
export function selectionCurrent(selection, version, text) {
  if (selection?.locator === "shot") {
    const shot = version.data.work?.shots.find((s) => s.id === selection.shot_id);
    return Boolean(selection.version_ref === version.entity_id && shot && JSON.stringify(shot) === JSON.stringify(selection.shot_snapshot));
  }
  return Boolean(selection && selection.version_ref === version.entity_id && text === version.data.body
    && text.slice(selection.start, selection.end) === selection.excerpt);
}
export function stableRequest(previous, action, base, data, id) {
  const sorted = (v) => Array.isArray(v) ? v.map(sorted) : v && typeof v === "object" ? Object.fromEntries(Object.keys(v).sort().map((key) => [key, sorted(v[key])])) : v;
  const signature = JSON.stringify(sorted({ action, base, data }));
  return previous?.signature === signature ? previous : { signature, request_id: id() };
}
export function cgReturnTarget(value) {
  const invalid = () => { throw new Error("请从当前图文工作台重新进入。"); };
  if (typeof value !== "string" || /[\\\u0000-\u0020#]/.test(value)) invalid();
  const match = /^\/ceo-office\/workspace\/installed\/([^/?]+)(?:\?[^#]*)?$/.exec(value);
  if (!match) invalid();
  let workspace; try { workspace = decodeURIComponent(match[1]); } catch { invalid(); }
  if (!workspace || /[%/\\]/.test(workspace) || [".", ".."].includes(workspace)) invalid();
  const url = new URL(value, "https://cg-return.invalid"), allowed = new Set(["cg_content", "cg_version", "cg_candidate", "cg_binding", "cg_attempt", "cg_start", "cg_end", "cg_shot", "cg_view","cg_object","cg_account","cg_period","cg_media"]);
  for (const [key, ref] of url.searchParams) if (!allowed.has(key) || url.searchParams.getAll(key).length !== 1 || /[%\\\u0000-\u001f]/.test(ref) || [".", ".."].includes(ref)) invalid();
  const entry = cgEntry(url.searchParams); if (entry.error) invalid();
  return { href: url.pathname + url.search, workspace, entry };
}

// Session input is a preference, never a saved version, grant or execution result.
export const cgInputKey = (company, workspace, content, sourceBasis = "") => `curis.cg.input.${company}:${workspace}:${content || "new"}${sourceBasis ? `:${encodeURIComponent(sourceBasis)}` : ""}`;
export const cgFeedbackKey = (company, workspace, content, candidate, version, actor, tenant = "") =>
  `curis.cg.feedback.${encodeURIComponent(JSON.stringify([tenant, company, workspace, content, candidate, version, actor]))}`;
export function saveCgFeedback(storage, key, snapshot) {
  const raw = JSON.stringify(snapshot), indexKey = "curis.cg.feedback.index";
  if (new TextEncoder().encode(raw).length > 16384) throw new Error("候选评价输入超过暂存上限。");
  const index = JSON.parse(storage.getItem(indexKey) || "[]");
  if (!Array.isArray(index) || index.length > 32 || index.some((item) => typeof item !== "string" || !item.startsWith("curis.cg.feedback.")))
    throw new Error("候选评价暂存索引无法核验。");
  if (!index.includes(key) && index.length === 32) throw new Error("候选评价暂存数量已满。");
  storage.setItem(indexKey, JSON.stringify(index.includes(key) ? index : [...index, key]));
  storage.setItem(key, raw);
}
export function clearCgFeedback(storage, key) {
  storage.removeItem(key);
  const indexKey = "curis.cg.feedback.index";
  const raw = storage.getItem(indexKey);
  if (raw) { const index = JSON.parse(raw); if (Array.isArray(index)) storage.setItem(indexKey, JSON.stringify(index.filter((item) => item !== key))); }
}
export function restoreCgFeedback(raw, context, now = Date.now()) {
  try {
    if (typeof raw !== "string" || raw.length > 16384) return null;
    const saved = JSON.parse(raw || "null");
    return saved && JSON.stringify(saved.context) === JSON.stringify(context) && Number.isFinite(saved.at)
      && saved.at <= now && now - saved.at <= 30 * 60 * 1000
      && ["", "ACCEPT", "REVISE", "REJECT"].includes(saved.action)
      && typeof saved.reason === "string" && new TextEncoder().encode(saved.reason).length <= 2000
      && typeof saved.request_id === "string"
      && (saved.pending === null || saved.pending === undefined || (
        typeof saved.pending === "object" && !Array.isArray(saved.pending)
        && /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(saved.pending.request_id)
        && saved.pending.request_id === saved.request_id
        && ["ACCEPT", "REVISE", "REJECT"].includes(saved.pending.action)
        && saved.pending.action === saved.action && saved.pending.reason === saved.reason.trim()
      )) ? saved : null;
  } catch { return null; }
}

export function cgFeedbackSourceCurrent(fresh, expected) {
  const content = fresh?.content;
  const candidate = fresh?.candidates?.find((item) => item?.version?.entity_id === expected?.candidate_ref);
  return Boolean(content && candidate && expected?.tenant_id && expected?.actor
    && content.tenant_id === expected.tenant_id && content.company_id === expected.company_id
    && content.workspace_id === expected.workspace_id && content.entity_id === expected.content_ref
    && candidate.version.tenant_id === expected.tenant_id
    && candidate.version.company_id === expected.company_id
    && candidate.version.workspace_id === expected.workspace_id
    && candidate.version.parent_id === expected.content_ref
    && candidate.version.data?.source_class === "MANUAL_CANDIDATE"
    && candidate.version.data?.manual_actor === expected.actor && candidate.version.owner_ref === expected.actor
    && candidate.version.data?.basis_version_ref === expected.basis_version_ref
    && candidate.feedback_version === expected.candidate_version && candidate.eligible === true);
}

export function cgFeedbackMatches(fresh, pending, expected) {
  if (!cgFeedbackSourceCurrent(fresh, expected) || !pending) return false;
  const candidate = fresh.candidates.find((item) => item.version.entity_id === expected.candidate_ref);
  const receipt = candidate.feedback;
  return Boolean(receipt && receipt.tenant_id === expected.tenant_id
    && receipt.company_id === expected.company_id && receipt.workspace_id === expected.workspace_id
    && receipt.content_ref === expected.content_ref && receipt.candidate_ref === expected.candidate_ref
    && receipt.candidate_version === expected.candidate_version
    && receipt.basis_version_ref === expected.basis_version_ref && receipt.ceo_id === expected.actor
    && receipt.request_id === pending.request_id && receipt.action === pending.action
    && receipt.reason === pending.reason);
}
export const cgInputContext = (company, workspace, content, entry) => ({ company, workspace, content: content || "new", tenant: entry.scope.tenant_id, actor: entry.actor });
export function cgInputSnapshot(context, input) {
  return { context, at: Date.now(), draft: input.draft, base: input.base, selection: input.selection || null, message: typeof input.message === "string" ? input.message : "", discussion: input.discussion === true, assignment: typeof input.assignment === "string" ? input.assignment : "", model: typeof input.model === "string" ? input.model : "" };
}
export function restoreCgInput(raw, context, now = Date.now()) {
  try {
    if (typeof raw !== "string" || new TextEncoder().encode(raw).length > 131072) return null;
    const saved = JSON.parse(raw || "null");
    if (!saved?.draft || !context.actor || !context.tenant || !saved.context
      || !Number.isFinite(saved.at) || saved.at > now || now - saved.at > 30 * 60 * 1000
      || Object.keys(context).some((k) => saved.context[k] !== context[k])) return null;
    return cgInputSnapshot(context, saved);
  } catch { return null; }
}
export function saveCgInput(storage, key, snapshot) {
  const raw = JSON.stringify(snapshot), indexKey = "curis.cg.input.index";
  if (new TextEncoder().encode(raw).length > 131072) throw new Error("内容输入超过暂存上限。");
  const index = JSON.parse(storage.getItem(indexKey) || "[]");
  if (!Array.isArray(index) || index.length > 32 || index.some((item) => typeof item !== "string" || !item.startsWith("curis.cg.input.")))
    throw new Error("内容暂存索引无法核验。");
  if (!index.includes(key) && index.length === 32) throw new Error("内容暂存数量已满。");
  storage.setItem(indexKey, JSON.stringify(index.includes(key) ? index : [...index, key]));
  storage.setItem(key, raw);
}
export function cgPreferenceStatus(assignments, assignment, model) {
  const employee = assignments.find((a) => a.assignment_ref === assignment);
  const modelCurrent = Boolean(employee?.models?.some((m) => m.model_key === model));
  return { employee, modelCurrent, stale: Boolean(assignment && !employee || model && !modelCurrent) };
}
export function clearCreatedCgInput(storage, key, context, submitted, result) {
  if (context.content !== "new" || key !== cgInputKey(context.company, context.workspace, null, context.creationSource || "") || !result?.content?.entity_id || result.content.company_id !== context.company || result.content.workspace_id !== context.workspace) return false;
  const cached = restoreCgInput(storage.getItem(key), context);
  // A late or repeated response cannot erase inputs entered after its request.
  if (!cached || JSON.stringify(cached.draft) !== JSON.stringify(submitted)) return false;
  storage.removeItem(key);
  const indexKey = "curis.cg.input.index";
  try { const rawIndex = storage.getItem(indexKey);
    if (rawIndex) { const index = JSON.parse(rawIndex);
      if (Array.isArray(index)) storage.setItem(indexKey, JSON.stringify(index.filter((item) => item !== key))); }
  } catch { /* Preserve the input deletion result; malformed index is not authority. */ }
  return true;
}

export function cgSelectionFromEntry(row, entry) {
  if (!entry.version) return null;
  const version = row?.versions.find((v) => v.entity_id === entry.version);
  if (!version) throw new Error("原保存版本不存在。");
  if (entry.shot) return shotSelectionFor(version, entry.shot);
  if (entry.start !== null && entry.start !== undefined && entry.end !== null && entry.end !== undefined) return selectionFor(version, version.data.body, entry.start, entry.end);
  return null;
}
export function cgScriptProjection(data) {
  const work = data.work;
  if (!work) return null;
  return { goal: work.goal || "未填写", intent: { UNCONFIRMED: "尚未确认", AUDIO: "本次制作音频", VIDEO: "本次制作视频" }[work.output_intent], spec: work.output_spec || "未填写", recording: work.recording_requirements || "未填写", employee: data.qualification?.assignment?.context?.name || "未选择", model: data.qualification?.model?.model?.display_name || "未选择", sources: work.source_refs.map((s) => ({ title: s.title })), shots: work.shots.map(({ title, description, camera, caption, sound, duration }) => ({ title, description, camera, caption, sound, duration })) };
}

export const cgChecksMatch = (candidateRef, reviewedRef, checks) => Boolean(candidateRef && candidateRef === reviewedRef && ["content", "references", "account"].every((key) => checks[key] === true));

// P1 reference-label helper (2026-10-06, CURIS-V1-CG-FOUR-FORM-INTERACTION-001).
// Display-only ordinary labels for canonical reference DTOs. It never mutates
// references, never invents titles for missing/stale/foreign records, and is not
// an authorization resolver: service qualification stays authoritative.
const CG_REF_KIND_LABELS = Object.freeze({ WORK: "工作", DECISION_PACKET: "决策包", KNOWLEDGE: "资料", RESULT: "结果", ARTIFACT: "产物", EVIDENCE: "证据", PACKAGE_DOMAIN_OBJECT: "歌曲" });
const CG_REF_NEEDS_REVIEW = "来源需核对";

function cgManualSourceParts(record, scope) {
  if (!record || record.schemaVersion !== "cg.operating-context/v1"
      || !["tenant_id", "company_id", "workspace_id"].every((key) => typeof scope?.[key] === "string" && scope[key] && record.scope?.[key] === scope[key])
      || !["Reference", "Report"].includes(record.kind) || record.kind === "Report" && record.payload?.confirmed !== true
      || typeof record.ref !== "string" || !/^[A-Za-z0-9._:-]{1,256}$/.test(record.ref) || [".", ".."].includes(record.ref)
      || !Number.isSafeInteger(record.revision) || record.revision < 1
      || typeof record.payload?.title !== "string" || !record.payload.title.trim() || record.payload.title.length > 240) return null;
  return { label: `${record.kind === "Report" ? "人工报告" : "原参考"} · ${record.payload.title} · v${record.revision}`, baseText: record.payload.title };
}

export function cgManualLearningSources(response, scope) {
  cgScopedRead(response, scope?.company_id, scope?.workspace_id);
  if (response.entry.scope.tenant_id !== scope?.tenant_id || response.schema_version !== "cg.operating-context/v1" || !Array.isArray(response.records))
    throw new Error("人工依据范围或版本已变化，请从原工作区重新进入。");
  return response.records.filter((record) => cgManualSourceParts(record, scope)).map((record) => ({
    reference_id: record.ref, kind: "MANUAL_CONTEXT", title: record.payload.title,
    version_ref: record.ref, purpose: "CONTEXT", locator: "", manual_record: record,
  }));
}

function cgRecordInScope(record, scope) {
  if (!record || typeof record !== "object" || !scope) return true;
  if (record.tenant_id !== undefined && scope.tenant_id !== undefined && record.tenant_id !== scope.tenant_id) return false;
  if (record.company_id !== undefined && scope.company_id !== undefined && record.company_id !== scope.company_id) return false;
  if (record.workspace_id !== undefined && scope.workspace_id !== undefined && record.workspace_id !== scope.workspace_id) return false;
  return true;
}

function cgReferenceParts(reference, contents, scope) {
  const fallback = { label: CG_REF_NEEDS_REVIEW };
  if (!reference || typeof reference !== "object" || !Array.isArray(contents)) return fallback;
  if (reference.kind === "MANUAL_CONTEXT") {
    const record = reference.manual_record;
    if (reference.reference_id !== record?.ref || reference.version_ref !== record?.ref) return fallback;
    return cgManualSourceParts(record, scope) || fallback;
  }
  if (reference.kind === "WORK" || reference.kind === "DECISION_PACKET" || reference.kind === "KNOWLEDGE"
      || reference.kind === "RESULT" || reference.kind === "ARTIFACT" || reference.kind === "EVIDENCE"
      || reference.kind === "PACKAGE_DOMAIN_OBJECT") {
    const kindLabel = CG_REF_KIND_LABELS[reference.kind];
    return { label: `${kindLabel} · ${reference.title || "未命名来源"}` };
  }
  if (reference.kind !== "CONTENT_ITEM" && reference.kind !== "CONTENT_VERSION") return fallback;
  const matcher = reference.kind === "CONTENT_ITEM"
    ? (item) => item?.content?.entity_id === reference.reference_id
    : (item) => item.versions.some((version) => version.entity_id === reference.reference_id);
  const item = contents.find(matcher);
  if (!item || !cgRecordInScope(item.content, scope)) return fallback;
  const formatLabel = CG_FORMATS[item.content.data?.format] || "内容";
  const headId = item.content.current_version_id || item.version?.entity_id;
  let version = null;
  let state = "";
  if (reference.kind === "CONTENT_ITEM") {
    if (reference.version_ref) {
      version = item.versions.find((candidate) => candidate.entity_id === reference.version_ref) || null;
      if (!version) return { label: CG_REF_NEEDS_REVIEW, contentId: item.content.entity_id, formatLabel, baseText: "" };
      state = reference.version_ref === headId ? "当前内容" : "原版本需核对";
    } else {
      version = item.version || item.versions.find((candidate) => candidate.entity_id === headId) || null;
      if (!version) return { label: CG_REF_NEEDS_REVIEW, contentId: item.content.entity_id, formatLabel, baseText: "" };
      state = "当前内容";
    }
  } else {
    version = item.versions.find((candidate) => candidate.entity_id === reference.reference_id) || null;
    if (!version) return { label: CG_REF_NEEDS_REVIEW, contentId: item.content.entity_id, formatLabel, baseText: "" };
    state = version.data?.kind === "candidate" ? "候选" : version.entity_id === headId ? "固定版本" : "历史版本";
  }
  const baseText = version.data?.title || "未命名内容";
  return { label: `${formatLabel} · ${state} · ${baseText}`, contentId: item.content.entity_id, formatLabel, baseText };
}

export function cgReferenceLabel(reference, contents = [], scope = null) {
  return cgReferenceParts(reference, contents, scope).label;
}
export function cgReferenceTitle(reference, contents = [], scope = null) {
  const parts = cgReferenceParts(reference, contents, scope);
  if (["CONTENT_ITEM", "CONTENT_VERSION", "MANUAL_CONTEXT"].includes(reference?.kind)) return parts.baseText || "来源标题暂不可读取";
  return reference?.title && !["查看来源", "查看原依据"].includes(reference.title) ? reference.title : "来源标题暂不可读取";
}

// Batch labels with view-local 来源n disambiguation for same-title distinct
// contents. Ordinals follow the authorized collection presentation order and
// are never persisted or treated as canonical version identity.
export function cgReferenceLabels(references, contents = [], scope = null) {
  const parts = (Array.isArray(references) ? references : []).map((reference) => ({ reference, ...cgReferenceParts(reference, contents, scope) }));
  const ambiguous = new Map();
  for (const part of parts) {
    if (!part.contentId || !part.baseText) continue;
    const key = `${part.formatLabel}|${part.baseText}`;
    const group = ambiguous.get(key) || new Set();
    group.add(part.contentId);
    ambiguous.set(key, group);
  }
  // Dense rank inside each ambiguous group, following collection order: 来源1/来源2,
  // never the content's global position in the collection.
  const ranksByKey = new Map();
  for (const [key, group] of ambiguous) {
    if (group.size <= 1) continue;
    const ranks = new Map();
    let ordinal = 0;
    for (const item of contents) {
      const contentId = item?.content?.entity_id;
      if (contentId && group.has(contentId)) ranks.set(contentId, ++ordinal);
    }
    ranksByKey.set(key, ranks);
  }
  const result = new Map();
  for (const part of parts) {
    let { label } = part;
    if (part.contentId && part.baseText) {
      const ordinal = ranksByKey.get(`${part.formatLabel}|${part.baseText}`)?.get(part.contentId);
      if (ordinal) label = `${label}（来源${ordinal}）`;
    }
    result.set(part.reference.reference_id, label);
  }
  return result;
}
