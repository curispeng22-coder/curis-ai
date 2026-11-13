import { workspaceFetch } from "./api.js";
import { sameChapter, writingEntry, WRITING_PACKAGE } from "./writingState.mjs";
const id = (v) => { if (typeof v !== "string" || !v.trim()) throw new Error("缺少明确的写作对象标识。"); return encodeURIComponent(v); };
export function createWritingApi(request = workspaceFetch) {
  const root = (company, workspace) => `/api/workspace/v1/companies/${id(company)}/writing/${id(workspace)}`;
  const chapter = (company, workspace, entry) => `${root(company, workspace)}/books/${id(entry.book)}/chapters/${id(entry.chapter)}`;
  return {
    direct: (c, w) => request(`${root(c, w)}/direct`, { method: "POST" }),
    collection: (c, w) => request(root(c, w)),
    bookContext: (c, w, book, ref = "") => request(`${root(c, w)}/books/${id(book)}/context${ref ? `?ref=${id(ref)}` : ""}`),
    saveBookContext: (c, w, book, payload) => request(`${root(c, w)}/books/${id(book)}/context`, { method: "POST", body: JSON.stringify(payload) }),
    entry: (c, w) => request(`${root(c, w)}/entry`),
    assign: (c, w, payload) => request(`${root(c, w)}/responsibility`, { method: "POST", body: JSON.stringify(payload) }),
    selectModel: (c, w, modelKey) => request(`${root(c, w)}/model`, { method: "POST", body: JSON.stringify({ model_key: modelKey }) }),
    chapter: (c, w, e) => request(chapter(c, w, e)),
    command: (c, w, e, action, payload) => request(`${chapter(c, w, e)}/commands/${id(action)}`, { method: "POST", body: JSON.stringify(payload) }),
    discussion: (c, w, e, binding) => request(`${chapter(c, w, e)}/discussion/${id(binding)}`),
    bind: (c, w, e, payload) => request(`${chapter(c, w, e)}/discussion`, { method: "POST", body: JSON.stringify(payload) }),
    send: (c, w, e, payload) => request(`${chapter(c, w, e)}/messages`, { method: "POST", body: JSON.stringify(payload) }),
    download: (c, w, e, ref) => request(`${chapter(c, w, e)}/packages/${id(ref)}/download`, { responseType: "blob" }),
    directions: (c, w) => request(`${root(c, w)}/operating/directions`),
    direction: (c, w, ref) => request(`${root(c, w)}/operating/directions/${id(ref)}`),
    directionCommand: (c, w, action, payload) => request(`${root(c, w)}/operating/directions/commands/${id(action)}`, { method: "POST", body: JSON.stringify(payload) }),
    learnings: (c, w) => request(`${root(c, w)}/operating/learnings`),
    learning: (c, w, ref) => request(`${root(c, w)}/operating/learnings/${id(ref)}`),
    learningCommand: (c, w, action, payload) => request(`${root(c, w)}/operating/learnings/commands/${id(action)}`, { method: "POST", body: JSON.stringify(payload) }),
    snapshots: (c, w) => request(`${root(c, w)}/operating/snapshots`),
    snapshot: (c, w, ref) => request(`${root(c, w)}/operating/snapshots/${id(ref)}`),
    snapshotCommand: (c, w, action, payload) => request(`${root(c, w)}/operating/snapshots/commands/${id(action)}`, { method: "POST", body: JSON.stringify(payload) }),
    observations: (c, w) => request(`${root(c, w)}/operating/observations`),
    observation: (c, w, ref) => request(`${root(c, w)}/operating/observations/${id(ref)}`),
    observationCommand: (c, w, action, payload) => request(`${root(c, w)}/operating/observations/commands/${id(action)}`, { method: "POST", body: JSON.stringify(payload) }),
    overview: (c, w) => request(`${root(c, w)}/operating/overview`),
  };
}
export const writingApi = createWritingApi();

export const writingRequestLocked = (status) => ["RUNNING", "UNKNOWN", "UNVERIFIED"].includes(status);
export function confirmationSnapshot(values) {
  if (Object.values(values).some((v) => typeof v !== "string" && typeof v !== "number")) throw new Error("确认需要明确且不变的字段。");
  return Object.freeze({ ...values });
}
export function writingRepairHref(path, returnHref) {
  if (!(path === "/ceo-office/capabilities" || /^\/ceo-office\/organization\/employees\/[^/?#\\]+$/.test(path))) throw new Error("修复入口需要现有模型或员工页面。");
  writingReturnTarget(returnHref);
  return `${path}?return_to=${encodeURIComponent(returnHref)}`;
}

export function writingReturnTarget(value) {
  const invalid = () => { throw new Error("请从当前写作工作台重新进入。"); };
  if (typeof value !== "string" || /[\\\u0000-\u0020#]/.test(value)) invalid();
  const match = /^\/ceo-office\/workspace\/installed\/([^/?]+)(?:\?[^#]*)?$/.exec(value);
  if (!match) invalid();
  let workspace;
  try { workspace = decodeURIComponent(match[1]); } catch { invalid(); }
  if (!workspace || /[%/\\]/.test(workspace) || [".", ".."].includes(workspace)) invalid();
  const url = new URL(value, "https://writing-return.invalid");
  const allowed = new Set(["writing_mode", "book_ref", "chapter_ref", "draft_ref", "formal_ref", "package_ref", "anchor", "wr_view", "book_section", "book_item", "context_ref"]);
  for (const [key, ref] of url.searchParams) {
    if (!allowed.has(key) || url.searchParams.getAll(key).length !== 1 || /[%\\\u0000-\u001f]/.test(ref)
      || ref.split("/").some((part) => part === "." || part === "..")) invalid();
  }
  const entry = writingEntry(url.searchParams);
  const selectedBook = url.searchParams.get("writing_mode") === "books" && entry.book && !entry.chapter;
  if (entry.error || Boolean(entry.book) !== Boolean(entry.chapter) && !selectedBook) invalid();
  if (selectedBook && (entry.draft || entry.formal || entry.package || entry.anchor)) invalid();
  if (!entry.book && (entry.draft || entry.formal || entry.package || entry.anchor)) invalid();
  return { href: url.pathname + url.search, workspace, entry };
}

export async function validateWritingReturn(value, company, request = workspaceFetch) {
  const target = writingReturnTarget(value);
  if (!company) throw new Error("请先确认当前公司。");
  const api = createWritingApi(request);
  const collection = await api.collection(company, target.workspace);
  const scope = collection?.scope;
  if (!scope?.tenant_id || !scope.instance_id || scope.company_id !== company || scope.workspace_id !== target.workspace
    || scope.package_id !== WRITING_PACKAGE.id || scope.package_version !== WRITING_PACKAGE.version || scope.package_digest !== WRITING_PACKAGE.digest) {
    throw new Error("当前工作台无法确认，请从写作入口重新进入。");
  }
  if (!target.entry.book) return { ...target, company, label: "返回写作工作台" };
  const book = collection.books?.find((item) => item.ref === target.entry.book);
  if (target.entry.mode === "books" && !target.entry.chapter) {
    if (!book) throw new Error("当前作品无法确认，请从作品库重新进入。");
    return { ...target, company, label: "返回当前作品" };
  }
  const chapter = collection.chapters?.find((item) => item.ref === target.entry.chapter && item.bookRef === target.entry.book);
  if (!book || !chapter) throw new Error("当前作品或章节无法确认，请从写作入口重新进入。");
  const state = await api.chapter(company, target.workspace, target.entry);
  if (!sameChapter(state?.scope, company, target.workspace, target.entry) || state.scope.tenant_id !== scope.tenant_id
    || state.scope.instance_id !== scope.instance_id) throw new Error("章节范围已变化，请从写作入口重新进入。");
  return { ...target, company, label: "返回当前写作章节" };
}
