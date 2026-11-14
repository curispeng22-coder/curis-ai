import { workspaceFetch } from "./api.js";
import { cgReturnTarget, cgDefinition, cgSelectionFromEntry } from "./contentGrowthState.mjs";
const id = (v) => { if (typeof v !== "string" || !v.trim()) throw new Error("缺少明确内容入口。"); return encodeURIComponent(v); };
export function createContentGrowthApi(request = workspaceFetch) {
  const root = (c, w) => `/api/workspace/v1/companies/${id(c)}/content-growth/${id(w)}`;
  const item = (c, w, ref) => `${root(c, w)}/contents/${id(ref)}`;
  const post = (url, payload) => request(url, { method: "POST", body: JSON.stringify(payload) });
  return {
    prepareModel: (c, w, p) => post(`${root(c, w)}/model`, p),
    collection: (c, w) => request(root(c, w)),
    operatingContext: (c,w) => request(`${root(c,w)}/operating-context`),
    saveOperatingContext: (c,w,kind,p) => post(`${root(c,w)}/operating-context/${id(kind)}`,p),
    mediaCollection: (c,w,r) => request(`${item(c,w,r)}/media`),
    importMedia: (c,w,r,p,bytes) => request(`${item(c,w,r)}/media`,{method:"POST",headers:{"Content-Type":p.data.mime,"X-CG-Import":encodeURIComponent(JSON.stringify(p))},body:bytes}),
    media: (c,w,r,asset) => request(`${item(c,w,r)}/media/${id(asset)}`,{responseType:"blob"}),
    adoptMedia: (c,w,r,p) => post(`${item(c,w,r)}/media/adopt`,p),
    materials: (c, w) => request(`${root(c, w)}/materials`),
    learnings: (c, w) => request(`${root(c, w)}/learnings`),
    learningCommand: (c, w, action, p) => post(`${root(c, w)}/learnings/commands/${id(action)}`, p),
    accounts: (c, w) => request(`${root(c, w)}/accounts`),
    account: (c, w, r) => request(`${root(c, w)}/accounts/${id(r)}`),
    accountCreate: (c, w, data) => post(`${root(c, w)}/accounts`, { data }),
    accountEdit: (c, w, r, data) => request(`${root(c, w)}/accounts/${id(r)}`, { method: "PUT", body: JSON.stringify({ data }) }),
    verificationTemplate: (c, w, platform) => request(`${root(c, w)}/verification-template/${id(platform)}`),
    verifications: (c, w) => request(`${root(c, w)}/verifications`),
    verification: (c, w, r) => request(`${root(c, w)}/verifications/${id(r)}`),
    verificationCreate: (c, w, requestId, data) => post(`${root(c, w)}/verifications`, { request_id: requestId, data }),
    verificationExport: (c, w, r) => request(`${root(c, w)}/verifications/${id(r)}/export`, { responseType: "blob" }),
    receipts: (c, w, vr) => request(`${root(c, w)}/verifications/${id(vr)}/receipts`),
    receiptCreate: (c, w, vr, requestId, data) => post(`${root(c, w)}/verifications/${id(vr)}/receipts`, { request_id: requestId, data }),
    receipt: (c, w, r) => request(`${root(c, w)}/receipts/${id(r)}`),
    observations: (c, w) => request(`${root(c, w)}/observations`),
    observationCreate: (c, w, requestId, data) => post(`${root(c, w)}/observations`, { request_id: requestId, data }),
    observation: (c, w, r) => request(`${root(c, w)}/observations/${id(r)}`),
    content: (c, w, r) => request(item(c, w, r)),
    create: (c, w, p) => post(`${root(c, w)}/contents`, p),
    command: (c, w, r, action, p) => post(`${item(c, w, r)}/commands/${id(action)}`, p),
    bind: (c, w, r, p) => post(`${item(c, w, r)}/discussion`, p),
    query: (c, w, r, binding, attempt) => request(`${item(c, w, r)}/discussion/${id(binding)}${attempt ? `?attempt_id=${id(attempt)}` : ""}`),
    send: (c, w, r, p) => post(`${item(c, w, r)}/messages`, p),
    candidate: (c, w, r, p) => post(`${item(c, w, r)}/reply-candidate`, p),
    feedback: (c, w, r, p) => post(`${item(c, w, r)}/candidate-feedback`, p),
  };
}
export const contentGrowthApi = createContentGrowthApi();
export function cgRepairHref(path, returnHref) {
  if (!(path === "/ceo-office/capabilities" || /^\/ceo-office\/organization\/employees\/[^/?#\\]+$/.test(path))) throw new Error("请使用当前模型或员工入口。");
  cgReturnTarget(returnHref); return `${path}?return_to=${encodeURIComponent(returnHref)}&return_kind=cg`;
}
export async function validateContentGrowthReturn(value, company, api = contentGrowthApi) {
  const target = cgReturnTarget(value); if (!company) throw new Error("先确认当前公司。");
  const collection = await api.collection(company, target.workspace), scope = collection?.entry?.scope, definition = collection?.entry?.definition;
  const expected = cgDefinition(definition?.version);
  if (!expected || scope?.company_id !== company || scope?.workspace_id !== target.workspace || definition?.package_id !== expected.id || definition?.digest !== expected.digest) throw new Error("原图文工作空间不属于当前公司。");
  if (target.entry.content) {
    const row = await api.content(company, target.workspace, target.entry.content);
    if (row?.content?.entity_id !== target.entry.content || row.content.company_id !== company || row.content.workspace_id !== target.workspace
      || target.entry.version && !row.versions?.some((v) => v.entity_id === target.entry.version)) throw new Error("原内容或版本无法确认。");
    cgSelectionFromEntry(row, target.entry);
    if (target.entry.candidate) {
      const candidate = row.candidates?.find((item) => item.version.entity_id === target.entry.candidate);
      if (!candidate || candidate.version.data.basis_version_ref !== target.entry.version) throw new Error("原候选或版本无法确认。");
    }
    if (target.entry.attempt) await api.query(company, target.workspace, target.entry.content, target.entry.binding, target.entry.attempt);
  }
  return { ...target, company, label: "返回当前内容工作台" };
}
