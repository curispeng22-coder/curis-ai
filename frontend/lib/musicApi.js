import { workspaceFetch } from "./api.js";
import { musicReturnTarget, exactMusicDefinition, OPERATING_KIND_VIEWS, musicScopedRead } from "./musicState.mjs";
const id = (v) => { if (typeof v !== "string" || !v.trim()) throw new Error("缺少明确歌曲入口。"); return encodeURIComponent(v); };
export function createMusicApi(request = workspaceFetch) {
  const root = (c, w) => `/api/workspace/v1/companies/${id(c)}/music/${id(w)}`;
  const item = (c, w, r) => `${root(c, w)}/songs/${id(r)}`;
  const post = (url, payload) => request(url, { method: "POST", body: JSON.stringify(payload) });
  return {
    researchDelivery: (c, w, conversation, work) => request(`${root(c, w)}/research-delivery?${new URLSearchParams({ conversation_ref: conversation, research_work_ref: work })}`),
    confirmResearchPlanning: (c, w, payload) => post(`${root(c, w)}/research-planning/confirm`, payload),
    importAudio: (c,w,r,p,bytes) => request(`${item(c,w,r)}/audio-import`, { method: "POST", headers: { "Content-Type": "audio/wav", "X-Music-Import": encodeURIComponent(JSON.stringify(p)) }, body: bytes }), importStatus: (c,w,r,key) => request(`${item(c,w,r)}/imports/${id(key)}`), operating: (c, w) => request(`${root(c,w)}/operating`), operatingContent: (c,w,r) => request(`${root(c,w)}/operating/${id(r)}`), operatingCommand: (c,w,a,p) => post(`${root(c,w)}/operating/commands/${id(a)}`,p), collection: (c, w) => request(root(c, w)), content: (c, w, r) => request(item(c, w, r)), create: (c, w, p) => post(`${root(c, w)}/songs`, p), command: (c, w, r, action, p) => post(`${item(c, w, r)}/commands/${id(action)}`, p), bind: (c, w, r, p) => post(`${item(c, w, r)}/discussion`, p), query: (c, w, r, b, a) => request(`${item(c, w, r)}/discussion/${id(b)}${a ? `?attempt_id=${id(a)}` : ""}`), send: (c, w, r, p) => post(`${item(c, w, r)}/messages`, p), candidate: (c, w, r, p) => post(`${item(c, w, r)}/reply-candidate`, p), media: (c, w, r, a) => request(`${item(c, w, r)}/assets/${id(a)}`, { responseType: "blob" }) };
}
export const musicApi = createMusicApi();
export function musicRepairHref(path, href) {
  if (!(path === "/ceo-office/capabilities" || /^\/ceo-office\/organization\/employees\/[^/?#\\]+$/.test(path))) throw new Error("请使用当前模型或员工入口。");
  musicReturnTarget(href); return `${path}?return_kind=music&return_to=${encodeURIComponent(href)}`;
}
export async function validateMusicReturn(value, company, api = musicApi) {
  const target = musicReturnTarget(value); if (!company) throw new Error("请先确认当前公司。");
  const collection = musicScopedRead(await api.collection(company, target.workspace), company, target.workspace), scope = collection?.entry?.scope, d = collection?.entry?.definition;
  if (scope?.company_id !== company || scope?.workspace_id !== target.workspace || !exactMusicDefinition(d)) throw new Error("原歌曲不属于当前公司组件。");
  if (target.operating?.object) {
    const original = await api.operatingContent(company, target.workspace, target.operating.object);
    if (original.record?.entity_id !== target.operating.object || original.record.tenant_id !== scope.tenant_id || original.record.company_id !== company || original.record.workspace_id !== target.workspace || OPERATING_KIND_VIEWS[original.record.data.kind] !== target.operating.view) throw new Error("原经营对象无法确认。");
  }
  if (target.entry.song) {
    const row = await api.content(company, target.workspace, target.entry.song);
    musicScopedRead({ entry: collection.entry, songs: [row] }, company, target.workspace);
    if (row?.song?.tenant_id !== scope.tenant_id || row?.song?.entity_id !== target.entry.song || row.song.company_id !== company || row.song.workspace_id !== target.workspace) throw new Error("原歌曲无法确认。");
    for (const [key, kind] of [["lyrics", "LyricsVersion"], ["production", "ProductionVersion"], ["candidate", "Candidate"], ["asset", "AudioAssetVersion"]]) if (target.entry[key] && !row.versions.some((v) => v.entity_id === target.entry[key] && v.tenant_id === scope.tenant_id && v.company_id === company && v.workspace_id === target.workspace && v.parent_id === target.entry.song && v.data.kind === kind)) throw new Error("原歌曲版本无法确认。");
    if (target.entry.release) {
      const matches = row.releases?.filter(v => v.entity_id === target.entry.release) || [];
      const pack = matches.length === 1 ? matches[0] : null;
      if (!pack || pack.tenant_id !== scope.tenant_id || pack.company_id !== company || pack.workspace_id !== target.workspace || pack.parent_id !== target.entry.song || pack.data.kind !== "ReleasePackage" || row.versions.filter(v => v.entity_id === pack.data.master_ref && v.tenant_id === scope.tenant_id && v.company_id === company && v.workspace_id === target.workspace && v.parent_id === target.entry.song && v.data.kind === "MasterRevision").length !== 1) throw new Error("原准备包与成品依据无法确认。");
    }
    if (target.entry.asset) {
      const c = row.candidates.find((v) => v.entity_id === target.entry.candidate), a = row.assets.find((v) => v.entity_id === target.entry.asset);
      if (c.data.asset_ref !== a.entity_id || a.data.sha256 !== target.entry.hash || target.entry.end !== null && target.entry.end > a.data.duration) throw new Error("原候选与音频范围无法确认。");
    } else if (target.entry.end !== null) {
      const v = row.versions.find((v) => v.entity_id === target.entry.lyrics); if (target.entry.end > v.data.text.length) throw new Error("原歌词范围无法确认。");
    }
    if (target.entry.compare && !row.candidates.some(v=>v.entity_id===target.entry.compare)) throw new Error("原比较候选不属于这首歌。");
    if (target.entry.attempt) await api.query(company, target.workspace, target.entry.song, target.entry.binding, target.entry.attempt);
  }
  return { ...target, company, label: "返回当前歌曲工作台" };
}
export async function verifiedAudioBlob(blob, asset) {
  if (!(blob instanceof Blob) || blob.size !== asset.data.size || blob.size > 16000000 || !blob.type.startsWith("audio/wav")) throw new Error("音频大小或类型不一致。");
  const hash = Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256", await blob.arrayBuffer())), (b) => b.toString(16).padStart(2, "0")).join("");
  if (hash !== asset.data.sha256 || !((asset.data.rights === "LOCAL_DESIGN_ONLY" && asset.data.purpose === "NONCOMMERCIAL_ISOLATED_TEST") || (asset.data.rights === "LOCAL_USER_PROVIDED_UNVERIFIED" && asset.data.purpose === "LOCAL_USE_ONLY"))) throw new Error("音频字节或用途不一致。");
  return blob;
}

export async function prepareLocalWav(file, isCurrent = () => true) {
  if (!file || !isCurrent()) return null;
  if (!/\.wav$/i.test(file.name) || !Number.isInteger(file.size) || file.size <= 0 || file.size > 16000000) throw new Error("请选择不超过16MB的 PCM WAV 文件。");
  const bytes = new Uint8Array(await file.arrayBuffer());
  if (bytes.byteLength !== file.size) throw new Error("文件读取不完整。");
  const sha256 = Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256", bytes)), b => b.toString(16).padStart(2, "0")).join("");
  if (!isCurrent()) throw new Error("原歌曲或草稿已改变，请保留文件并重新选择。");
  return { bytes, data: { title: file.name.replace(/\.wav$/i, "").slice(0, 240).trim() || "用户本地音频", sha256, size: bytes.byteLength } };
}
