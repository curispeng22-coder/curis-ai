const VIEWS = new Set(["home", "matter", "work", "result", "conversation"]);
const SCOPES = new Set(["COMPANY", "DEPARTMENT", "BUSINESS", "WORKSPACE"]);

export function parseD1Entry(search = "", initialView = "home") {
  const params = new URLSearchParams(search);
  const view = params.get("view");
  const bridgeKeys = ["result_origin", "result_version", "origin_company", "result_bridge_invalid"];
  const bridgePresent = bridgeKeys.some((key) => params.has(key));
  const bridgeValid = bridgePresent && !params.has("result_bridge_invalid")
    && params.getAll("result_origin").length === 1 && params.get("result_origin") === "utility"
    && params.getAll("result_version").length === 1 && /^[0-9a-f]{64}$/.test(params.get("result_version") || "")
    && params.getAll("origin_company").length === 1 && Boolean(params.get("origin_company"))
    && params.getAll("result_ref").length === 1 && Boolean(params.get("result_ref"))
    && params.getAll("result_workspace").length === 1 && Boolean(params.get("result_workspace"))
    && params.getAll("work_ref").length === 1 && Boolean(params.get("work_ref"))
    && (!params.has("workspace_id") || params.getAll("workspace_id").length === 1 && params.get("workspace_id") === params.get("result_workspace"));
  return {
    view: VIEWS.has(view) ? view : params.has("result_ref") ? "result" : params.has("work_ref") ? "work" : initialView,
    sourceRef: params.get("source_ref") || "",
    sourceType: params.get("source_type") || "",
    workRef: params.get("work_ref") || "",
    workspaceId: params.get("result_workspace") || params.get("workspace_id") || "",
    resultRef: params.get("result_ref") || "",
    resultOrigin: bridgeValid ? "utility" : "",
    resultVersion: bridgeValid ? params.get("result_version") : "",
    originCompany: bridgeValid ? params.get("origin_company") : "",
    resultBridgeInvalid: bridgePresent && !bridgeValid,
    employeeRef: params.get("employee_ref") || "",
    conversationId: params.get("conversation_id") || "",
    scopeType: SCOPES.has(params.get("scope_type")) ? params.get("scope_type") : "",
    scopeRef: params.get("scope_ref") || "",
    explicit: false,
  };
}

export function d1Href(entry, pathname = "/ceo-office") {
  const params = new URLSearchParams();
  const fields = { view: entry.view, source_ref: entry.sourceRef, source_type: entry.sourceType,
    work_ref: entry.workRef, workspace_id: entry.workspaceId, result_ref: entry.resultRef,
    result_origin: entry.resultOrigin, result_version: entry.resultVersion, origin_company: entry.originCompany,
    employee_ref: entry.employeeRef, conversation_id: entry.conversationId,
    scope_type: entry.scopeType, scope_ref: entry.scopeRef };
  for (const [key, value] of Object.entries(fields)) if (value) params.set(key, value);
  if (entry.resultBridgeInvalid) params.set("result_bridge_invalid", "1");
  if (entry.resultRef && entry.workspaceId) params.set("result_workspace", entry.workspaceId);
  return `${pathname}?${params}`;
}

export function interactionKey(companyId, entry) {
  return JSON.stringify([companyId, entry.scopeType || "", entry.scopeRef || "", entry.workspaceId || "",
    entry.employeeRef || "", entry.conversationId || "", entry.workRef || "", entry.sourceRef || ""]);
}

export function initialD1State(entry) {
  return { entry, returns: [] };
}

export function d1Reducer(state, action) {
  if (action.type === "navigate") return { ...state, entry: action.entry, returns: [...state.returns, { ...state.entry, anchor: action.anchor || "" }].slice(-20) };
  if (action.type === "restore") return { ...state, entry: { ...action.entry, explicit: false }, returns: [] };
  if (action.type === "back") {
    if (!state.returns.length) return { ...state, entry: { view: "home", explicit: false } };
    return { ...state, entry: { ...state.returns.at(-1), explicit: false }, returns: state.returns.slice(0, -1) };
  }
  return state;
}

// Session-local only; no canonical messages, Work states, or Result history.
const drafts = new Map();
const pending = new Map();
export function pendingRequest(key) { return pending.get(key) || null; }
export function rememberRequest(key, request) {
  if (!request) pending.delete(key);
  else { pending.delete(key); pending.set(key, request); }
  while (pending.size > 100) pending.delete(pending.keys().next().value);
}
export function readDraft(key) { return drafts.get(key) || ""; }
export function saveDraft(key, value) {
  if (!value) drafts.delete(key);
  else { drafts.delete(key); drafts.set(key, value); }
  while (drafts.size > 100) drafts.delete(drafts.keys().next().value);
}

export function messageRequest(previous, values, newId) {
  const normalized = { body: values.body.trim(), assignment_ref: values.assignment_ref || "", references: [] };
  const signature = JSON.stringify(normalized);
  return previous?.signature === signature ? previous : { ...normalized, request_id: newId(), signature };
}

export function isMatchingCompletion(view, request) {
  if (!request) return false;
  const message = (view.messages || []).find((item) => item.idempotency_key === request.request_id);
  return Boolean(message && (view.attempts || []).some((item) => item.message_id === message.message_id && item.status === "COMPLETED"));
}

export function receiptEligible(selection, result) {
  return Boolean(selection?.explicit && selection.workspaceId && result?.result_version && result.reference_id === selection.resultRef && ["RESULT", "OUTCOME"].includes(result.kind) && readableResult(result).length);
}

export function resultResponseKey(company, workspace, result, actor = "") {
  return `curis.result.response.${encodeURIComponent(JSON.stringify([result?.tenant_id, company, workspace, result?.reference_id, result?.result_version, result?.source_work_ref, actor]))}`;
}
export function saveResultResponse(storage, key, snapshot) {
  const raw = JSON.stringify(snapshot), indexKey = "curis.result.response.index";
  if (new TextEncoder().encode(raw).length > 16384) throw new Error("结果输入超过暂存上限。");
  const index = JSON.parse(storage.getItem(indexKey) || "[]");
  if (!Array.isArray(index) || index.length > 32 || index.some((item) => typeof item !== "string" || !item.startsWith("curis.result.response.")))
    throw new Error("结果暂存索引无法核验。");
  if (!index.includes(key) && index.length === 32) throw new Error("结果暂存数量已满。");
  storage.setItem(indexKey, JSON.stringify(index.includes(key) ? index : [...index, key]));
  storage.setItem(key, raw);
}
export function clearResultResponse(storage, key) {
  storage.removeItem(key);
  const indexKey = "curis.result.response.index";
  const raw = storage.getItem(indexKey);
  if (raw) { const index = JSON.parse(raw); if (Array.isArray(index)) storage.setItem(indexKey, JSON.stringify(index.filter((item) => item !== key))); }
}
export function restoreResultResponse(raw, context, now = Date.now()) {
  try {
    if (typeof raw !== "string" || raw.length > 16384) return null;
    const saved = JSON.parse(raw || "null");
    return saved && JSON.stringify(saved.context) === JSON.stringify(context)
      && Number.isFinite(saved.at) && saved.at <= now && now - saved.at <= 30 * 60 * 1000
      && ["ACCEPT", "REVISE", "REJECT", ""].includes(saved.action) && typeof saved.reason === "string"
      && new TextEncoder().encode(saved.reason).length <= 2000
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
export function validResultBridge(entry, company, result) {
  return !entry?.resultBridgeInvalid && entry?.resultOrigin === "utility" && entry.originCompany === company
    && entry.workspaceId && entry.workRef && entry.resultRef && entry.resultVersion
    && result?.tenant_id && result.company_id === company && result.workspace_id === entry.workspaceId
    && result?.reference_id === entry.resultRef && result.result_version === entry.resultVersion
    && result.source_work_ref === entry.workRef && readableResult(result).length > 0;
}

export function resultReceiptMatches(fresh, pending, expected) {
  const saved = fresh?.user_response;
  return Boolean(fresh && saved && pending && expected
    && expected.tenant_id && expected.company_id && expected.workspace_id && expected.reference_id
    && expected.result_version && expected.source_work_ref && expected.response_actor_ref
    && fresh.tenant_id === expected.tenant_id && fresh.company_id === expected.company_id
    && fresh.workspace_id === expected.workspace_id && fresh.reference_id === expected.reference_id
    && fresh.result_version === expected.result_version && fresh.source_work_ref === expected.source_work_ref
    && fresh.response_actor_ref === expected.response_actor_ref
    && saved.tenant_id === expected.tenant_id && saved.company_id === expected.company_id
    && saved.workspace_id === expected.workspace_id && saved.result_ref === expected.reference_id
    && saved.result_version === expected.result_version && saved.source_work_ref === expected.source_work_ref
    && saved.ceo_id === expected.response_actor_ref && saved.request_id === pending.request_id
    && saved.action === pending.action && saved.reason === pending.reason);
}

// Only material supported by the Result surface counts as a successful read.
// Metadata, identifiers, unsupported objects and UI placeholders are not material.
export function readableResult(result) {
  function material(value, depth = 0) {
    if (depth > 5) return [];
    if (typeof value === "string") return value.trim() ? [{ text: value }] : [];
    if (Array.isArray(value)) return value.flatMap((item) => material(item, depth + 1));
    if (!value || typeof value !== "object") return [];
    const parts = material(value.content ?? value.text ?? value.body ?? value.summary ?? value.sections, depth + 1);
    const title = typeof value.title === "string" ? value.title : "";
    return parts.map((part, index) => ({ ...part, title: index === 0 ? title || part.title : part.title }));
  }
  for (const value of [result?.content, result?.data?.content, result?.data?.sections, result?.data?.summary, result?.summary]) {
    const parts = material(value);
    if (parts.length) return parts;
  }
  return (result?.artifacts || []).flatMap((item) => material({ title: item.title, content: item.content }));
}

export function remainingDraft(current, sentBody, inputAtSend = sentBody) {
  return current === inputAtSend && current.trim() === sentBody ? "" : current;
}

export function executionLabel(bindings = []) {
  const active = bindings.filter((item) => item.enabled && ["model", "agent"].includes(item.capability_type));
  if (active.length !== 1) return "执行方式待确认";
  const binding = active[0];
  return `${binding.capability_type === "model" ? "模型" : "Agent"}绑定 · ${binding.display_name || binding.name || "名称未记录"}`;
}

export function accessLabel(access) {
  return { GRANTED: "当前已授予访问权限", DENIED: "当前未授予访问权限", REVOKED: "访问权限已撤回", NONE: "当前无访问权限" }[access?.effective_state] || "权限尚未确认";
}

export function currentResponsibilities(employee, currentWorkRef = "") {
  const source = employee?.current_responsibilities;
  if (!Array.isArray(source) || !employee?.employee_ref) return { items: [], message: "当前责任未记录" };
  if (!source.length) return { items: [], message: "当前工作空间暂无已记录的当前责任" };
  const items = source.filter((item) => item && item.responsibility_holder_ref === employee.employee_ref
    && (!item.object_owner_ref || item.object_owner_ref === employee.employee_ref)).map((item) => ({
    current: Boolean(currentWorkRef && item.object_type === "WORK" && item.object_ref === currentWorkRef),
    work: item.object_type === "WORK",
    activity: typeof item.activity === "string" && item.activity.trim() ? item.activity : "当前活动未记录",
  }));
  return { items: [...items.filter((item) => item.current), ...items.filter((item) => !item.current)], message: items.length ? "" : "当前责任未记录" };
}

export function lifecycleActions(work) {
  if (!work?.workspaceId || !work?.work_ref) return [];
  const state = work.lifecycle_status;
  if (state === "ARCHIVED") return ["restore"];
  if (["CANCELLED", "COMPLETED"].includes(state)) return ["archive"];
  if (state === "PAUSED") return ["resume", "cancel"];
  if (["PLANNED", "READY", "ACTIVE", "WAITING", "BLOCKED"].includes(state)) return ["pause", "cancel"];
  return [];
}

const workControls = new Map();
export function workControlKey(company, work) { return JSON.stringify([company, work.workspaceId, work.work_ref]); }
export function readWorkControl(key) { return workControls.get(key) || null; }
export function saveWorkControl(key, value) {
  if (value) workControls.set(key, value); else workControls.delete(key);
}
export function controlTarget(work, action) {
  return { pause: "PAUSED", cancel: "CANCELLED", archive: "ARCHIVED",
    resume: work.resume_to || "ACTIVE", restore: work.restore_to || "COMPLETED" }[action];
}
export function controlReadbackMatches(company, original, fresh, pending) {
  return Boolean(pending?.target && fresh?.companyId === company && fresh.workspaceId === original.workspaceId
    && fresh.work_ref === original.work_ref && fresh.lifecycle_status === pending.target);
}
