export const MUSIC_PACKAGE = Object.freeze({ id: "com.curis.local.music", version: "0.2.0", digest: "cb05fd21e4237d046e20f0b96a81f6894e71caee95c2b0c6559b91ecf56ec802" });
export const MUSIC_PACKAGES = Object.freeze([MUSIC_PACKAGE, Object.freeze({ id: MUSIC_PACKAGE.id, version: "0.1.0", digest: "5d9f36c36c2461f4540ad59277b56447a1a67cb2953759f43c52afbe5ed2cf76" })]);
export function exactMusicDefinition(d) { return MUSIC_PACKAGES.some(p => d?.package_id === p.id && d.version === p.version && d.digest === p.digest); }
export function isMusicPackage(detail) {
  const p = detail?.package, i = detail?.instance;
  return Boolean(p && i && exactMusicDefinition(p) && i.package_id === p.package_id && i.package_version === p.version && i.package_digest === p.digest && p.schema_version === "curis.workspace-package/v1" && detail.schemas?.MusicSong?.schemaVersion === p.version);
}
const names = ["song", "lyrics", "production", "candidate", "asset", "hash", "start", "end", "binding", "attempt", "release", "mode", "compare"];
export function musicEntry(params) {
  const entry = Object.fromEntries(names.map((k) => [k, params.get(`music_${k}`) || ""]));
  const bad = () => ({ error: "请从当前歌曲工作台重新进入。" });
  for (const key of names) if (params.getAll(`music_${key}`).length > 1 || entry[key].length > 256) return bad();
  if (!entry.song && names.some((k) => k !== "song" && entry[k])) return bad();
  if (entry.mode && !["lyrics", "candidates", "history", "release", "analysis"].includes(entry.mode)) return bad();
  if (entry.release && (!entry.song || entry.mode && entry.mode !== "release")) return bad();
  if (Boolean(entry.binding) !== Boolean(entry.attempt) || entry.asset && !entry.candidate || Boolean(entry.start) !== Boolean(entry.end)) return bad();
  if (entry.asset && !/^[0-9a-f]{64}$/.test(entry.hash) || entry.hash && !entry.asset) return bad();
  if (entry.start) {
    if ((!entry.asset && !entry.lyrics) || !/^\d+(?:\.\d+)?$/.test(entry.start) || !/^\d+(?:\.\d+)?$/.test(entry.end) || !Number.isFinite(Number(entry.end)) || Number(entry.end) <= Number(entry.start) || !entry.asset && (!Number.isInteger(Number(entry.start)) || !Number.isInteger(Number(entry.end)))) return bad();
    entry.start = Number(entry.start); entry.end = Number(entry.end);
  } else { entry.start = null; entry.end = null; }
  return entry;
}
export function songHref(workspace, entry = {}) {
  const params = new URLSearchParams();
  if (!entry.song) params.set("music_view", "songs");
  for (const key of names) if (entry[key] !== undefined && entry[key] !== null && entry[key] !== "") params.set(`music_${key}`, String(entry[key]));
  if (entry.period) params.set("music_period",entry.period);
  const result = `/ceo-office/workspace/installed/${encodeURIComponent(workspace)}${params.size ? `?${params}` : ""}`;
  if (musicEntry(params).error) throw new Error("返回歌曲的定位不完整。");
  return result;
}
export function musicReturnTarget(value) {
  const invalid = () => { throw new Error("无法确认原歌曲入口。"); };
  if (typeof value !== "string" || /[\\\u0000-\u0020#]/.test(value)) invalid();
  const match = /^\/ceo-office\/workspace\/installed\/([^/?]+)(?:\?[^#]*)?$/.exec(value);
  if (!match) invalid();
  let workspace; try { workspace = decodeURIComponent(match[1]); } catch { invalid(); }
  if (!workspace || /[%/\\]/.test(workspace) || [".", ".."].includes(workspace)) invalid();
  const url = new URL(value, "https://music-return.invalid");
  for (const [key, ref] of url.searchParams) if (!([...names, "view", "object", "period"].includes(key.replace(/^music_/, ""))) || !key.startsWith("music_") || url.searchParams.getAll(key).length !== 1 || /[%\\\u0000-\u001f]/.test(ref) || [".", ".."].includes(ref)) invalid();
  const entry = musicEntry(url.searchParams), operating = musicOperatingEntry(url.searchParams); if (entry.error || operating.error) invalid();
  return { href: url.pathname + url.search, workspace, entry, operating };
}
export const songBasis = (row) => Object.fromEntries(["lyrics_ref", "production_ref", "master_ref"].map((k) => [k, row?.song?.data[k] || ""]));
export function lyricsSelection(version, draft, start, end) {
  if (draft !== version?.data.text || !Number.isInteger(start) || !Number.isInteger(end) || !(0 <= start && start < end && end <= draft.length)) throw new Error("先保存歌词，再选择原版本的完整字符。");
  for (const n of [start, end]) if (n > 0 && /[\uD800-\uDBFF]/u.test(draft[n - 1]) && /[\uDC00-\uDFFF]/u.test(draft[n] || "")) throw new Error("不能切开完整字符。");
  return { kind: "lyrics", version_ref: version.entity_id, draft_revision: version.data.draft_revision, start, end, excerpt: draft.slice(start, end), locator: "lyrics" };
}
export function audioSelection(row, candidate, asset, start, end) {
  if (!candidate || !asset || candidate.data.asset_ref !== asset.entity_id || asset.parent_id !== row.song.entity_id || !Number.isFinite(start) || !Number.isFinite(end) || !(0 <= start && start < end && end <= asset.data.duration)) throw new Error("音频范围必须位于准确候选的实际长度内。");
  return { kind: "audio", song_ref: row.song.entity_id, candidate_ref: candidate.entity_id, candidate_version_ref: candidate.entity_id, asset_ref: asset.entity_id, sha256: asset.data.sha256, start, end, duration: asset.data.duration, anchor: "candidate-audio" };
}
export function selectionCurrent(selection, row, draft, production, candidate) {
  if (!selection || draft !== row.lyrics.data.text || production !== row.production.data.brief) return false;
  if (selection.kind === "lyrics") return selection.version_ref === row.lyrics.entity_id && selection.draft_revision === row.lyrics.data.draft_revision && draft.slice(selection.start, selection.end) === selection.excerpt;
  return selection.song_ref === row.song.entity_id && selection.candidate_ref === candidate?.entity_id && candidate?.data.asset_ref === selection.asset_ref && candidate.data.lyrics_ref === row.lyrics.entity_id && candidate.data.production_ref === row.production.entity_id;
}
export const requestLocked = (status) => ["RUNNING", "UNKNOWN", "UNVERIFIED"].includes(status);
export function stableRequest(previous, action, base, data, makeId) {
  const sorted = (v) => Array.isArray(v) ? v.map(sorted) : v && typeof v === "object" ? Object.fromEntries(Object.keys(v).sort().map((k) => [k, sorted(v[k])])) : v;
  const signature = JSON.stringify(sorted({ action, base, data }));
  return previous?.signature === signature ? previous : { signature, request_id: makeId() };
}
export const draftKey = (company, workspace, song) => "curis.music.draft." + JSON.stringify([company, workspace, song || "new"]);
export function restoredPlayer(saved, duration) {
  const position = Number.isFinite(saved?.position) && saved.position >= 0 && saved.position <= duration ? saved.position : 0;
  return { position, paused: saved?.paused !== false };
}

export const OPERATING_KIND_VIEWS = Object.freeze({ OperatingScope: "market", MarketSnapshot: "market", ReferenceAnalysis: "reference", Direction: "direction", Observation: "performance", Report: "report", Learning: "learning" });
export const OPERATING_VIEWS = Object.freeze({ operating: "经营", songs: "歌曲创作", market: "市场依据", reference: "参考分析", direction: "创作方向", release: "发行与发布", performance: "作品表现", report: "分析报告", learning: "经验与下一首" });
export function musicOperatingEntry(params) {
  const entry = Object.fromEntries(["view", "object", "period"].map(k => [k, params.get(`music_${k}`) || ""]));
  if (Object.keys(entry).some(k => params.getAll(`music_${k}`).length > 1 || entry[k].length > 256) || entry.view && !Object.hasOwn(OPERATING_VIEWS, entry.view) || entry.object && (!entry.view || !/^music-[A-Za-z0-9-]+$/.test(entry.object)) || /[\\\u0000-\u001f]/.test(entry.object)) return { error: "原经营对象入口无法确认。" };
  return entry;
}
export function operatingHref(workspace, entry = {}) {
  const params = new URLSearchParams();
  for (const k of ["view", "object", "period"]) if (entry[k]) params.set(`music_${k}`, entry[k]);
  if (entry.song) params.set("music_song", entry.song);
  if (entry.release) params.set("music_release", entry.release);
  if (musicEntry(params).error || musicOperatingEntry(params).error) throw new Error("经营对象定位不完整。");
  return `/ceo-office/workspace/installed/${encodeURIComponent(workspace)}${params.size ? `?${params}` : ""}`;
}
export function manualNumber(value) {
  if (value === "") return null;
  if (typeof value !== "string" || !/^\d+(?:\.\d+)?$/.test(value) || !Number.isFinite(Number(value))) throw new Error("观察值应为非负数；未知请留空。");
  return Number(value);
}
export const operatingDraftKey = (company, workspace, actor, view, ref) => "curis.music.operating.draft." + JSON.stringify([company, workspace, actor, view, ref || "new"]);
export function observationComparison(before, after) {
  if (!before || !after) return { eligible: false, reason: "需要两次完整观察。" };
  const a = before.data || before, b = after.data || after;
  const identity = ["song_ref", "master_ref", "platform", "account", "metric", "definition", "unit", "currency", "coverage", "method"];
  if (identity.some(k => k !== "currency" && !a[k] || a[k] !== b[k]) || a.value === null || b.value === null) return { eligible: false, reason: "对象、成品、账号、口径或观察值不完整或不同。" };
  const startA = Date.parse(a.period?.start), endA = Date.parse(a.period?.end), startB = Date.parse(b.period?.start), endB = Date.parse(b.period?.end);
  if (![startA, endA, startB, endB].every(Number.isFinite) || a.period.timezone !== b.period.timezone || endA - startA !== endB - startB || endA > startB || startA >= endA || startB >= endB) return { eligible: false, reason: "期间、时区或覆盖不具有可比条件。" };
  return { eligible: true, difference: b.value - a.value, percent: a.value === 0 ? null : (b.value - a.value) / a.value * 100 };
}

export function musicScopedRead(value, company, workspace, definition) {
  const scope = value?.entry?.scope, actual = value?.entry?.definition;
  if (!scope?.tenant_id || scope.company_id !== company || scope.workspace_id !== workspace || !exactMusicDefinition(actual) || definition && (actual.package_id !== definition.package_id || actual.version !== definition.version || actual.digest !== definition.digest)) throw new Error("音乐范围或版本依据不一致。");
  const check = (row, parent) => {
    if (!row || row.tenant_id !== scope.tenant_id || row.company_id !== company || row.workspace_id !== workspace || parent && row.parent_id !== parent) throw new Error("原音乐对象不属于当前范围。");
  };
  const records = value.records || [];
  if (new Set(records.map(r => r.entity_id)).size !== records.length) throw new Error("原音乐对象标识不唯一。");
  for (const row of records) check(row);
  for (const row of value.songs || []) {
    check(row.song);
    if (new Set((row.versions || []).map(v => v.entity_id)).size !== (row.versions || []).length) throw new Error("原歌曲版本标识不唯一。");
    for (const version of [...(row.versions || []), ...(row.candidates || []), ...(row.assets || []), ...(row.releases || []), ...[row.lyrics,row.production,row.choice,row.master].filter(Boolean)]) check(version, row.song.entity_id);
  }
  return value;
}

// The full immutable ref remains distinct when timestamps or shortened refs collide.
export function releaseRecordLabel(pack) {
  if (pack?.data?.kind !== "ReleasePackage" || typeof pack.entity_id !== "string" || !pack.entity_id.trim() || pack.entity_id.length > 256) return null;
  const stamp = typeof pack.created_at === "string" ? pack.created_at : "";
  const explicitTime = /^\d{4}-\d{2}-\d{2}T(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/.test(stamp);
  const date = explicitTime ? new Date(stamp.slice(0, 10) + "T00:00:00Z") : null;
  const validDate = date && Number.isFinite(date.getTime()) && date.toISOString().startsWith(stamp.slice(0, 10));
  const time = validDate ? Date.parse(stamp) : NaN;
  return `${Number.isFinite(time) ? "保存于 " + new Date(time).toISOString() : "时间未提供或不可核对"} · 记录 ${pack.entity_id}`;
}
