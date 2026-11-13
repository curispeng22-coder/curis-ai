import { bookLocator } from "./writingBookState.mjs";
export const WRITING_PACKAGE = Object.freeze({ id: "com.curis.local.writing-authoring", version: "0.1.0", digest: "2f4c37d6b579d8db31f88f7626acec44b9f630164ba8c9909e217a5f41e2d66e" });
export const WRITING_CHECKS = ["continuity", "language", "rights"];

export function isWritingPackage(detail) {
  const p = detail?.package; const i = detail?.instance;
  return Boolean(p && i && p.package_id === WRITING_PACKAGE.id && p.version === WRITING_PACKAGE.version && p.digest === WRITING_PACKAGE.digest
    && i.package_id === p.package_id && i.package_version === p.version && i.package_digest === p.digest
    && detail.schemas?.WritingBook?.schemaVersion === "writing.book/v1" && detail.schemas?.WritingChapter?.schemaVersion === "writing.chapter/v1");
}

export const WRITING_VIEWS = new Set(["", "directions", "learning", "market", "performance", "overview"]);

export function writingEntry(params) {
  let bookPosition; try { bookPosition = bookLocator(params); } catch (reason) { return { error: reason.message }; }
  const mode = params.get("writing_mode") || "books";
  const book = params.get("book_ref") || ""; const chapter = params.get("chapter_ref") || "";
  if (!["books", "chapter", "review", "package"].includes(mode)) return { error: "写作入口无效。" };
  if (mode !== "books" && (!book || !chapter)) return { error: "请从真实作品和章节进入。" };
  const view = params.get("wr_view") || "";
  if (!WRITING_VIEWS.has(view)) return { error: "写作经营面入口无效。" };
  if (view && mode !== "books") return { error: "经营面请从作品库入口进入。" };
  return { mode, book, chapter, view, ...( ["book_section","book_item","context_ref"].some(k=>params.has(k)) ? {bookPosition} : {}), draft: params.get("draft_ref") || "", formal: params.get("formal_ref") || "", package: params.get("package_ref") || "", anchor: params.get("anchor") || "" };
}

export function writingViewHref(workspace, view) {
  if (!WRITING_VIEWS.has(view)) throw new Error("写作经营面入口无效。");
  const params = new URLSearchParams();
  if (view) params.set("wr_view", view);
  const query = params.toString();
  return `/ceo-office/workspace/installed/${encodeURIComponent(workspace)}${query ? `?${query}` : ""}`;
}

export function chapterHref(workspace, entry) {
  const params = new URLSearchParams({ writing_mode: entry.mode || "chapter", book_ref: entry.book, chapter_ref: entry.chapter });
  for (const [key, value] of [["draft_ref", entry.draft], ["formal_ref", entry.formal], ["package_ref", entry.package], ["anchor", entry.anchor]]) if (value) params.set(key, value);
  return `/ceo-office/workspace/installed/${encodeURIComponent(workspace)}?${params}`;
}

export function sameChapter(scope, company, workspace, entry) {
  return Boolean(scope && scope.company_id === company && scope.workspace_id === workspace && scope.book_ref === entry.book && scope.chapter_ref === entry.chapter
    && scope.package_id === WRITING_PACKAGE.id && scope.package_version === WRITING_PACKAGE.version && scope.package_digest === WRITING_PACKAGE.digest);
}

export function eventByRef(events, action, ref) { return events.find((e) => e.action === action && e.ref === ref) || null; }
export function packageForEntry(events, entry) {
  const item = eventByRef(events, "package.prepared", entry.package);
  return item && (!entry.formal || item.formal_ref === entry.formal) ? item : null;
}
export function newestEvent(events, action) { return [...events].reverse().find((e) => e.action === action) || null; }
export function currentInspection(state) {
  return [...state.events].reverse().find((e) => e.action === "inspection.recorded" && e.draft_ref === state.draft.ref && e.draft_sha256 === state.draft.sha256 && JSON.stringify(e.book_context_basis || null) === JSON.stringify(state.draft.book_context_basis || null) && state.book_context_status?.status !== "STALE") || null;
}
export function selectionFor(draft, text, start, end) {
  if (text !== draft.text) throw new Error("请保存当前正文后重新选择文字。");
  if (!Number.isInteger(start) || !Number.isInteger(end) || start < 0 || end < start || end > text.length) throw new Error("选段范围无效，请重新选择正文。");
  if (end === start) throw new Error("请先选中一段正文。");
  for (const boundary of [start, end]) if (boundary > 0 && /[\uD800-\uDBFF]/u.test(text[boundary - 1]) && /[\uDC00-\uDFFF]/u.test(text[boundary] || "")) throw new Error("选择不能拆分字符。");
  return { draft_ref: draft.ref, sha256: draft.sha256, start, end, excerpt: text.slice(start, end), anchor: `${draft.ref}:${start}:${end}`, knowledge: draft.knowledge };
}
export function writingSessionKey(scope) { return `curis.writing.input.${JSON.stringify([scope.tenant_id, scope.company_id, scope.workspace_id, scope.instance_id, scope.book_ref, scope.chapter_ref])}`; }
export async function writingRequest(previous, action, base, data, newId) {
  const sorted = (value) => Array.isArray(value) ? value.map(sorted) : value && typeof value === "object" ? Object.fromEntries(Object.keys(value).sort().map((k) => [k, sorted(value[k])])) : value;
  const bytes = new TextEncoder().encode(JSON.stringify(sorted({ action, base, data })));
  const signature = Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256", bytes)), (v) => v.toString(16).padStart(2, "0")).join("");
  return previous?.signature === signature ? previous : { signature, request_id: newId() };
}
