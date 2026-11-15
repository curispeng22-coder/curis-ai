"use client";
import { useCallback, useEffect, useLayoutEffect, useRef, useState } from "react";
import Link from "next/link";
import { createAssignedWork } from "../../lib/v1FrontendApi.js";
import EmployeeConversation, { MusicResearchResult } from "../v1/EmployeeConversation.js";
import { useRouter, useSearchParams } from "next/navigation";
import WorkspacePaneShell from "../workspace/WorkspacePaneShell.js";
import MusicMain from "./MusicMain.js";
import { musicApi as api, validateMusicReturn } from "../../lib/musicApi.js";
import { musicEntry, songHref, isMusicPackage, songBasis, stableRequest, musicOperatingEntry, operatingHref, OPERATING_VIEWS, OPERATING_KIND_VIEWS, operatingDraftKey, manualNumber, observationComparison, musicScopedRead, releaseRecordLabel } from "../../lib/musicState.mjs";
import styles from "./Music.module.css";

export default function MusicWorkspace({ detail, workspaceId }) {
  const company = detail.instance.company_id, router = useRouter(), params = useSearchParams(), entry = musicEntry(params), operating = musicOperatingEntry(params), canOperate = detail.package?.version === "0.2.0";
  const researchConversation = params.getAll("research_conversation");
  const researchWork = params.getAll("research_work");
  const research = researchConversation.length === 1 && researchWork.length === 1 && researchConversation[0] && researchWork[0]
    ? { conversation_ref: researchConversation[0], research_work_ref: researchWork[0] } : null;
  const researchQuery = research ? new URLSearchParams({ research_conversation: research.conversation_ref, research_work: research.research_work_ref }) : null;
  const operatingEntry = { ...operating, view: operating.view === "songs" ? "" : operating.view || (!entry.song && canOperate ? "operating" : "") };
  const identity = JSON.stringify([company, workspaceId, entry, operatingEntry]), active = useRef(identity), epoch = useRef(0), pending = useRef(false);
  useLayoutEffect(() => { active.current = identity; }, [identity]);
  const [savedOperatingCollection, setOperatingCollection] = useState(null), [loadedIdentity, setLoadedIdentity] = useState("");
  const [savedCollection, setCollection] = useState(null), [savedRow, setRow] = useState(null), [savedRequest, setRequest] = useState(null);
  const collection = loadedIdentity === identity ? savedCollection : null, row = loadedIdentity === identity ? savedRow : null, operatingCollection = loadedIdentity === identity ? savedOperatingCollection : null, request = loadedIdentity === identity ? savedRequest : null;
  const [error, setError] = useState(""), [busy, setBusy] = useState(false), [creating, setCreating] = useState(false);
  const [inspectRef, setInspectRef] = useState(""), [inspector, setInspector] = useState(null), [utilityKey, setUtilityKey] = useState(0);
  const load = useCallback(async () => {
    const generation = ++epoch.current, key = identity;
    try {
      if (!isMusicPackage(detail) || entry.error || operating.error) throw new Error(entry.error || operating.error || "歌曲组件依据不一致。");
      const next = musicScopedRead(await api.collection(company, workspaceId), company, workspaceId, detail.package);
      if (next.entry.scope.company_id !== company || next.entry.scope.workspace_id !== workspaceId) throw new Error("歌曲范围不一致。");
      if (entry.song) await validateMusicReturn(songHref(workspaceId, entry), company);
      const current = entry.song ? await api.content(company, workspaceId, entry.song) : null;
      const operatingData = canOperate ? musicScopedRead(await api.operating(company, workspaceId), company, workspaceId, detail.package) : null;
      if (operatingEntry.object && !operatingData?.records.some(r => r.entity_id === operatingEntry.object && operatingViewsForKind[r.data.kind] === operatingEntry.view)) throw new Error("原经营对象或版本不可用，没有替换为其他对象。");
      const original = entry.attempt ? await api.query(company, workspaceId, entry.song, entry.binding, entry.attempt) : null;
      if (generation !== epoch.current || active.current !== key) return;
      setCollection(next); setOperatingCollection(operatingData); setRow(current); setRequest(original); setLoadedIdentity(key); setError("");
    } catch (reason) { if (generation === epoch.current && active.current === key) { setError(reason.message); setRow(null); setCollection(null); setOperatingCollection(null); setRequest(null); } }
  }, [company, workspaceId, identity, detail]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { setCollection(null); setRow(null); setRequest(null); setCreating(false); setInspectRef(""); setInspector(null); load(); return () => { epoch.current += 1; }; }, [load]);
  const inspect = useCallback((ref, refresh = false) => {
    if (typeof ref === "string") { setInspectRef(ref); setInspector(null); }
    else { setInspectRef(""); setInspector({ ...ref, scope: identity }); }
    if (!refresh) setUtilityKey(v => v + 1);
  }, [identity]);
  const perform = async (action, data, expected = songBasis(row), rawAudio = null) => {
    if (pending.current) throw new Error("请等待当前操作完成。");
    const key = identity; pending.current = true; setBusy(true);
    const storage = ["create-work", "send"].includes(action) ? `curis.music.model-work.${JSON.stringify([collection?.entry.scope.tenant_id, collection?.entry.actor, company, workspaceId, entry.song, action])}` : `curis.music.request.${JSON.stringify([company, workspaceId, entry.song || "new", action])}`;
    const requestStorage = ["create-work", "send"].includes(action) ? localStorage : sessionStorage;
    let previous = null; try { previous = JSON.parse(requestStorage.getItem(storage) || "null"); } catch {}
    const id = stableRequest(previous, action, expected, data, () => crypto.randomUUID());
    try {
      if (action === "import-audio") {
        // An uncertain upload owns its request until queried. Never replace it
        // with a different file/basis or silently submit a second Candidate.
        if (previous?.pending) {
          const status = await api.importStatus(company, workspaceId, entry.song, previous.request_id);
          if (key !== active.current) throw new Error("歌曲已切换，请回原歌曲查看导入记录。");
          if (status.status === "APPLIED") {
            requestStorage.setItem(storage, JSON.stringify({ ...previous, pending: false }));
            if (previous.signature === id.signature) { await load(); return status; }
          } else if (status.status !== "NOT_APPLIED" || (previous.signature !== id.signature && !["lyrics_ref", "production_ref", "master_ref"].some(field => previous.expected && status.basis && previous.expected[field] !== status.basis[field]))) throw new Error("原导入结果尚未确认，请先重新选择同一文件、保留原依据再查询重试。");
        }
        requestStorage.setItem(storage, JSON.stringify({ ...id, expected, pending: true }));
        let result;
        try { result = await api.importAudio(company, workspaceId, entry.song, { request_id: id.request_id, expected, data }, rawAudio); }
        catch (reason) {
          // A fresh typed refusal completed without a receipt. A refusal while
          // retrying UNKNOWN does not cancel the original possibly delayed POST.
          if (!previous?.pending && [400, 401, 403, 404, 409, 413, 422].includes(reason.status)) requestStorage.setItem(storage, JSON.stringify({ ...id, pending: false }));
          throw reason;
        }
        requestStorage.setItem(storage, JSON.stringify({ ...id, pending: false }));
        if (key !== active.current) throw new Error("歌曲已切换，请回原歌曲查看导入记录。");
        await load(); return result;
      }
      requestStorage.setItem(storage, JSON.stringify(id));
      const payload = { request_id: id.request_id, expected, data };
      const output = action === "create-work" ? await createAssignedWork(data.assignment_ref, { ...data.payload, request_id: id.request_id })
        : action === "create" ? await api.create(company, workspaceId, { ...payload, expected: {} })
        : action === "bind" ? await api.bind(company, workspaceId, entry.song, { request_id: id.request_id, expected, assignment_ref: data.assignment_ref })
        : action === "send" ? await api.send(company, workspaceId, entry.song, { ...data, request_id: id.request_id, expected })
        : action === "materialize" ? await api.candidate(company, workspaceId, entry.song, { ...data, request_id: id.request_id })
        : await api.command(company, workspaceId, entry.song, action, payload);
      if (key !== active.current) throw new Error("歌曲已切换，请回原歌曲查看记录。");
      if (action === "create") router.push(songHref(workspaceId, { song: output.song.entity_id }));
      else await load();
      return output;
    } catch (reason) { if (key === active.current) setError(reason.message); throw reason; }
    finally { pending.current = false; setBusy(false); }
  };
  const view = operating.view || (entry.song ? "work" : canOperate ? "operating" : "songs");
  const context = <div className={styles.context}><h2>音乐</h2><nav aria-label="音乐经营与创作">{Object.entries(OPERATING_VIEWS).filter(([key]) => !["reference", "report"].includes(key) && (canOperate || ["songs", "release"].includes(key))).map(([key,label]) => <Link aria-current={view === key ? "page" : undefined} key={key} href={operatingHref(workspaceId,{view:key,...(["operating","performance","release"].includes(key) ? {period:operatingEntry.period,song:entry.song} : {})})}>{label}</Link>)}</nav>{row && <><h3>当前歌曲</h3><Link href={songHref(workspaceId, { song: row.song.entity_id })}>{row.song.data.title}</Link><p className={styles.sub}>{row.song.data.intention}</p><h3>歌曲内导航</h3>{[["lyrics","歌词与结构"],["candidates","试听与比较"],["history","版本历史"]].map(([mode,label]) => <Link key={mode} href={songHref(workspaceId,{...entry,mode,release:""})}>{label}</Link>)}</>}</div>;
  const fixed = (ref, kind) => {
    const matches = row?.versions.filter(v => v.entity_id === ref && (!kind || v.data.kind === kind) && v.tenant_id === collection?.entry.scope.tenant_id && v.company_id === company && v.workspace_id === workspaceId && v.parent_id === row.song.entity_id) || [];
    return matches.length === 1 ? matches[0] : null;
  };
  const item = fixed(inspectRef), lyrics = item && fixed(item.data.kind === "LyricsVersion" ? item.entity_id : item.data.lyrics_ref, "LyricsVersion"), production = item && fixed(item.data.kind === "ProductionVersion" ? item.entity_id : item.data.production_ref, "ProductionVersion");
  const itemLabel = item && ["LyricsVersion", "ProductionVersion"].includes(item.data.kind) ? `${item.data.kind === "LyricsVersion" ? "歌词" : "制作"} v${row.versions.filter(v => v.data.kind === item.data.kind).findIndex(v => v.entity_id === item.entity_id) + 1}` : "版本与原依据";
  const versionUtility = inspectRef ? <div className={styles.context}><h2>{item?.data.title || itemLabel}</h2>{item ? <><p className={styles.sub}>固定原保存版本 · 查看不会替换当前稿</p><h3>原歌词</h3><pre>{lyrics ? lyrics.data.text || "原歌词为空" : item.data.kind === "ProductionVersion" ? "不适用：这版只保存制作依据" : "原歌词暂不可读取"}</pre><h3>原制作依据</h3><pre>{production ? production.data.brief || "原制作依据为空" : item.data.kind === "LyricsVersion" ? "不适用：这版只保存歌词" : "原制作依据暂不可读取"}</pre>{item.data.suggestion && <pre>{item.data.suggestion}</pre>}{item.data.rights && <p>用途：仅本地使用，商业权利未核验，不代表发行许可</p>}<button onClick={() => setInspectRef("")}>结束查看</button></> : <p>原版本暂不可读取，没有替换为最新版本。</p>}</div> : null;
  const utilityId = inspector?.scope === identity ? `music:${encodeURIComponent(inspector.id)}` : inspectRef ? `music-version:${encodeURIComponent(inspectRef)}` : "";
  const currentUtility = loadedIdentity === identity && utilityId ? { id: utilityId, title: inspector?.scope === identity ? inspector.title : itemLabel, content: inspector?.scope === identity ? inspector.content : versionUtility } : null;
  const locked = Boolean(collection?.pending_requests.length);
  const discussionHolders = (collection?.entry?.assignments || []).filter((item) => item.employee_ref && item.assignment_ref && item.company_id === company && item.workspace_id === workspaceId && item.scope_type === "WORKSPACE" && item.scope_ref === workspaceId && item.tenant_id === collection.entry.scope.tenant_id);
  const discussionHolder = discussionHolders.length === 1 ? discussionHolders[0] : null;
  return <WorkspacePaneShell workspaceId={workspaceId} surfaceId="music-song" breadcrumb="音乐 · 经营与创作" contextAvailable initialContextOpen contextLabel="经营与作品" contextPane={context} utilityAvailable={Boolean(currentUtility)} utilityLabel="辅助内容" utilityTabs={currentUtility ? [currentUtility] : []} utilityRequestKey={utilityKey} utilityRequestTabId={currentUtility?.id || ""}>
    <div className={styles.main}>{error && <p role="alert" className={styles.error}>{error}</p>}{!collection && !error && <p role="status">正在读取歌曲与版本…</p>}
      {collection && (!row || Boolean(operatingEntry.view)) && discussionHolder && <EmployeeConversation key={`${company}:${workspaceId}:workspace:${discussionHolder.employee_ref}`} companyId={company} employee={{ ...discussionHolder, id: discussionHolder.company_employee_ref }} blocked={Boolean(locked || busy)} embedded={{ workspaceId, contextKey: "workspace", assignmentRef: discussionHolder.assignment_ref, title: "音乐工作空间讨论", showBar: true }} businessReturn={{ href: operatingHref(workspaceId, operatingEntry), kind: "music" }} />}
      {collection && canOperate && operatingEntry.view && operatingEntry.view !== "release" && <MusicOperatingMain key={JSON.stringify([operatingEntry.view,operatingEntry.object,operatingEntry.period])} company={company} workspaceId={workspaceId} songs={collection.songs} entry={{...operatingEntry,song:entry.song}} collection={operatingCollection} load={load} locked={locked} research={research} researchQuery={researchQuery} />}
      {collection && operatingEntry.view === "release" && <MusicReleaseMain workspaceId={workspaceId} songs={collection.songs} entry={entry} />}
      {collection && !row && !operatingEntry.view && <MusicSongDirectory workspaceId={workspaceId} collection={collection} creating={creating} setCreating={setCreating} busy={busy} locked={locked} createMain={creating ? <MusicMain key="new" company={company} workspaceId={workspaceId} row={null} entry={{}} collection={collection} busy={busy} locked={locked} perform={perform} inspect={inspect} /> : null} />}
      {row && collection && !operatingEntry.view && <MusicMain key={row.song.entity_id} company={company} workspaceId={workspaceId} row={row} entry={{...entry,period:operating.period}} request={request} collection={collection} busy={busy} locked={locked} perform={perform} inspect={inspect} reload={load} />}
    </div>
  </WorkspacePaneShell>;
}

const operatingKindNames = { OperatingScope: "观察范围", MarketSnapshot: "原始观察", ReferenceAnalysis: "参考分析", Direction: "创作方向", Observation: "作品观察", Report: "分析报告", Learning: "经验" };
const operatingViewsForKind = OPERATING_KIND_VIEWS;
const operatingActions = { OperatingScope: "save-scope", MarketSnapshot: "save-snapshot", ReferenceAnalysis: "save-reference", Direction: "save-direction", Observation: "save-observation", Report: "create-report", Learning: "save-learning" };
const operatingObjectNames = { market: "市场依据", reference: "参考分析", direction: "创作方向", performance: "作品观察", report: "分析报告", learning: "创作经验" };
const visibleValue = v => v === null || v === undefined ? "未提供" : String(v);

export function MusicOperatingMain({ company, workspaceId, songs, entry, collection, load, locked, research, researchQuery }) {
  const router = useRouter(), pending = useRef(false), mounted = useRef(true);
  useEffect(() => { mounted.current = true; return () => { mounted.current = false; }; }, []);
  const records = collection?.records || [], selected = records.find(r => r.entity_id === entry.object);
  const defaultKind = ({ operating: "OperatingScope", market: "OperatingScope", reference: "ReferenceAnalysis", direction: "Direction", performance: "Observation", report: "Report", learning: "Learning" })[entry.view || "operating"];
  const [editing, setEditing] = useState(false), [query, setQuery] = useState("");
  const [kind, setKind] = useState(selected?.data.kind || defaultKind), [form, setForm] = useState({}), [error, setError] = useState(""), [busy, setBusy] = useState(false);
  const actor = collection?.entry.actor || "", draft = operatingDraftKey(company, workspaceId, actor, kind, selected?.entity_id);
  const initialForm = useCallback(() => {
    const d = selected?.data || {}, period = d.period || {}, source = d.source || {}, metric = d.metrics?.[0] || d;
    return { creation_revision: crypto.randomUUID(), creation_confirmed: false, title: d.title || "", body: d.body || "", scope_ref: d.scope_ref || "", platform: d.platform || "", keywords: d.keywords || "", start: period.start || metric.period?.start || "", end: period.end || metric.period?.end || "", timezone: period.timezone || metric.period?.timezone || Intl.DateTimeFormat().resolvedOptions().timeZone,
      source_label: source.label || "", source_locator: source.locator || "", source_note: source.note || "", captured_at: source.captured_at || new Date().toISOString(), metric: metric.metric || "", definition: metric.definition || "", unit: metric.unit || "", value: metric.value === null || metric.value === undefined ? "" : String(metric.value), account: metric.account || "", currency: metric.currency || "", coverage: metric.coverage || "", method: metric.method || "", snapshot_ref: d.snapshot_ref || "", purpose: d.purpose || "PATTERN", locator: d.locator || "", material_available: d.material_available || false,
      reference_ref: d.reference_refs?.[0] || "", learning_ref: d.learning_ref || "", confirmed: false, historical: false, song_ref: d.song_ref || d.selection?.song_ref || entry.song || "", master_ref: d.master_ref || "", release_ref: d.release_ref || "", report_ref: d.report_ref || "", counterexample: d.counterexample || "", applicability: d.applicability || "", accepted: false, new_song_title: "", new_song_intention: "", lyrics: "", production: "" };
  }, [selected,entry.song]);
  useEffect(() => { let cached; try { cached = JSON.parse(sessionStorage.getItem(draft) || "null"); } catch {} setForm(cached || initialForm()); setError(""); }, [draft, initialForm]);
  const field = (name, value) => setForm(previous => { const next = { ...previous, [name]: value }; if (name === "scope_ref") Object.assign(next, { snapshot_ref: "", reference_ref: "", learning_ref: "" }); if (name === "song_ref") Object.assign(next, { master_ref: "", release_ref: "" }); if (name === "master_ref") next.release_ref = ""; try { sessionStorage.setItem(draft, JSON.stringify(next)); } catch {} return next; });
  const input = (name, label, options = {}) => <label className={styles.operatingField} key={name}><span>{label}</span><input aria-label={label} value={form[name] || ""} onChange={e => field(name, e.target.value)} {...options} /></label>;
  const textarea = (name, label, required = false) => <label className={styles.operatingField}><span>{label}</span><textarea aria-label={label} value={form[name] || ""} onChange={e => field(name, e.target.value)} required={required} rows={3} /></label>;
  const check = (name, label) => <label className={styles.operatingCheck}><input type="checkbox" checked={Boolean(form[name])} onChange={e => field(name, e.target.checked)} />{label}</label>;
  const select = (name, label, options, required = true) => <label className={styles.operatingField}><span>{label}</span><select aria-label={label} value={form[name] || ""} onChange={e => field(name, e.target.value)} required={required}><option value="">请选择明确对象与版本</option>{options.map(r => <option key={r.entity_id} value={r.entity_id}>{r.data.title || operatingKindNames[r.data.kind]} · {r.data.revision ? `v${r.data.revision}` : "固定保存版"}</option>)}</select></label>;
  const scopeOptions = records.filter(r => r.data.kind === "OperatingScope"), snapshotOptions = records.filter(r => r.data.kind === "MarketSnapshot" && r.data.scope_ref === form.scope_ref), referenceOptions = records.filter(r => r.data.kind === "ReferenceAnalysis" && r.data.scope_ref === form.scope_ref), reports = records.filter(r => r.data.kind === "Report" && r.data.scope_ref === form.scope_ref && r.data.confirmed_by);
  const song = songs.find(r => r.song.entity_id === form.song_ref), masters = (song?.versions.filter(v => v.data.kind === "MasterRevision") || []).map((r, index) => ({ ...r, data: { ...r.data, title: `${song.song.data.title} · 本地成品 ${index + 1}` } })), releases = (song?.releases.filter(r => r.data.master_ref === form.master_ref) || []).map((r, index) => ({ ...r, data: { ...r.data, title: `${r.data.title} · 准备包 ${index + 1}` } }));
  const observationRows = records.filter(r => r.data.kind === "Observation" && (!entry.song || r.data.song_ref === entry.song) && (entry.period === "all" || !entry.period || observationPeriod(r.data) === entry.period));
  const periods = [...new Set(records.filter(r => r.data.kind === "Observation").map(r => observationPeriod(r.data)))];
  const sourceFields = <fieldset className={styles.operatingGroup}><legend>原来源说明 · 人工保存，未联网核验</legend>{input("source_label", "来源名称", { required: true })}{input("source_locator", "来源位置或原文件说明", { required: true })}{textarea("source_note", "来源与核验限制", true)}{input("captured_at", "来源记录时间", { required: true })}</fieldset>;
  const periodFields = <fieldset className={styles.operatingGroup}><legend>原观察期间</legend><div className={styles.operatingColumns}>{input("start", "期间开始", { type: "date", required: true })}{input("end", "期间结束", { type: "date", required: true })}{input("timezone", "时区", { required: true })}</div></fieldset>;
  const metricFields = <fieldset className={styles.operatingGroup}><legend>观察口径 · 未知数值留空</legend><div className={styles.operatingColumns}>{input("metric", "指标名称", { required: true })}{input("unit", "单位", { required: true })}{input("value", "观察值", { inputMode: "decimal", placeholder: "未提供" })}</div>{input("definition", "指标定义", { required: true })}{input("account", "平台账号（未提供可留空）")}{input("currency", "币种（非金额可留空）")}{input("coverage", "样本覆盖范围", { required: true })}{input("method", "记录方法", { required: true })}{periodFields}</fieldset>;
  const payload = () => {
    const common = { title: form.title, body: form.body }, period = { start: form.start, end: form.end, timezone: form.timezone }, source = { label: form.source_label, locator: form.source_locator, note: form.source_note, captured_at: form.captured_at };
    const metric = { metric: form.metric, definition: form.definition, unit: form.unit, value: manualNumber(form.value), account: form.account || null, currency: form.currency || null, coverage: form.coverage, method: form.method, period };
    if (kind === "OperatingScope") return { ...common, platform: form.platform, keywords: form.keywords, period };
    if (kind === "MarketSnapshot") return { ...common, scope_ref: form.scope_ref, source, metrics: [metric] };
    if (kind === "ReferenceAnalysis") return { ...common, scope_ref: form.scope_ref, snapshot_ref: form.snapshot_ref, purpose: form.purpose, locator: form.locator, material_available: form.material_available };
    if (kind === "Direction") return { ...common, scope_ref: form.scope_ref, reference_refs: selected?.data.reference_refs?.[0] === form.reference_ref ? selected.data.reference_refs : [form.reference_ref], learning_ref: form.learning_ref || "", confirmed: form.confirmed };
    if (kind === "Observation") return { ...common, scope_ref: form.scope_ref, song_ref: form.song_ref, master_ref: form.master_ref, release_ref: form.release_ref, platform: form.platform, ...metric, source };
    if (kind === "Report") return { ...common, selection: { scope_ref: form.scope_ref, song_ref: form.song_ref || "", period: entry.period || selected?.data.selection?.period || "all" } };
    return { ...common, scope_ref: form.scope_ref, report_ref: form.report_ref, counterexample: form.counterexample, applicability: form.applicability, accepted: form.accepted };
  };
  const submit = async (action, data, expected = selected?.entity_id || "") => {
    if (pending.current || locked) return; pending.current = true; setBusy(true); setError("");
    const before = JSON.stringify(form), key = `${draft}.request.${action}`; let previous; try { previous = JSON.parse(sessionStorage.getItem(key) || "null"); } catch {}
    const request = stableRequest(previous, action, { expected_ref: expected }, data, () => crypto.randomUUID());
    try {
      sessionStorage.setItem(key, JSON.stringify(request));
      const output = await api.operatingCommand(company, workspaceId, action, { request_id: request.request_id, expected_ref: expected, data });
      if (!mounted.current) return output;
      if (sessionStorage.getItem(draft) === before) sessionStorage.removeItem(draft);
      await load();
      if (output.song) router.push(songHref(workspaceId, { song: output.song.entity_id }));
      else router.push(directionHref({ view: operatingViewsForKind[output.record.data.kind], object: output.record.entity_id, period: entry.period, song:entry.song }));
      return output;
    } catch (reason) { if (mounted.current) setError(reason.message); }
    finally { pending.current = false; if (mounted.current) setBusy(false); }
  };
  if (!collection) return <p role="status">正在读取经营依据…</p>;
  if (entry.object && !selected) return <p role="alert">原对象或版本不可用。没有替换为其他作品；请返回原列表核对。</p>;
  const current = !selected || !records.some(r => r.data.identity_ref === selected.data.identity_ref && r.data.revision > selected.data.revision);
  const directionHref = (values) => {
    const href = operatingHref(workspaceId, values);
    return researchQuery && values.view === "direction" ? `${href}${href.includes("?") ? "&" : "?"}${researchQuery}` : href;
  };
  const recordLink = ref => { const r = records.find(v => v.entity_id === ref); return r ? <Link href={directionHref({ view: operatingViewsForKind[r.data.kind], object: ref, period: entry.period, song:entry.song })}>{r.data.title} · v{r.data.revision}</Link> : <span>原来源不可用</span>; };
  const report = selected?.data.kind === "Report" ? selected.data : null;
  const masterLabel = data => {
    const item = songs.find(r => r.song.entity_id === data.song_ref), versions = item?.versions.filter(v => v.data.kind === "MasterRevision") || [], index = versions.findIndex(v => v.entity_id === data.master_ref);
    return index >= 0 ? `${item.song.data.title} · 本地成品 ${index + 1}` : "原成品不可用";
  };
  const comparison = observationComparison(observationRows.at(-2), observationRows.at(-1));
  return <div className={styles.operatingMain}>
    <header className={styles.row}><div><h1>{OPERATING_VIEWS[entry.view || "operating"]}</h1><p className={styles.sub}>手动记录来源、创作判断与下一步</p></div><Link href={songHref(workspaceId,entry.song?{song:entry.song,period:entry.period}: {})}>{entry.song?"返回原歌曲与期间":"歌曲创作"}</Link></header>
    {locked && <p role="status" className={styles.notice}>原建议请求尚待核验，当前保存与新创作已锁定。历史依据可继续查看。</p>}
    {error && <p role="alert" className={styles.error}>{error}</p>}
    <details className={styles.details}><summary>来源与可用范围</summary><p>来源与判断由你手动记录，尚未联网核验。音频生成、商业权利、平台发行及真实收益尚未接入。经验用途需要明确确认。</p></details>
    {entry.view === "operating" && <><div className={styles.operatingSummary}><section><h2>逐作品结果</h2><p>逐歌曲查看成品与期间的人工观察。</p><strong>{observationRows.length ? "已有人工观察" : "尚无原观察"}</strong></section><section><h2>可比变化</h2><p>{comparison.eligible ? `原值变化 ${comparison.difference}；${comparison.percent === null ? "原基数为 0，增长比例未提供。" : `同口径变化 ${comparison.percent.toFixed(1)}%。`}` : comparison.reason}</p></section><section><h2>来源与限制</h2><p>歌曲、成品、账号与指标分别查看；未知值保留空缺。</p></section></div><h2>判断与下一步</h2><p>从原观察追溯来源，确认创作方向后再进入歌曲。</p></>}
    {entry.view === "operating" && <section className={styles.panel}><header className={styles.row}><h2>当前歌曲与下一步</h2><Link href={songHref(workspaceId)}>全部歌曲</Link></header><div className={styles.workRows}>{songs.map(item => <Link key={item.song.entity_id} href={songHref(workspaceId,{song:item.song.entity_id})}><span className={styles.songMark} aria-hidden="true">♪</span><div><strong>{item.song.data.title}</strong><p>{item.song.data.intention || "创作意图待完善"}</p></div><span>{item.master ? "本地成品已确认" : item.choice ? "已选候选 · 待确认成品" : `${item.candidates.length} 个候选 · 待人工选版`}</span><b>继续制作 →</b></Link>)}{!songs.length && <p className={styles.empty}>还没有歌曲，从明确创作意图开始。</p>}</div></section>}
    {["operating", "performance"].includes(entry.view) && <><label className={styles.periodFilter}>观察周期<select aria-label="观察周期" value={entry.period || "all"} onChange={e => router.push(operatingHref(workspaceId, { ...entry, period: e.target.value }))}><option value="all">全部已保存周期</option>{periods.map(period => <option key={period} value={period}>{period.replaceAll("|", " · ")}</option>)}</select></label><table className={styles.table}><thead><tr><th>观察</th><th>指标与原值</th><th>来源</th><th>结果与制作</th></tr></thead><tbody>{observationRows.filter(r => !query || `${r.data.title} ${r.data.metric} ${r.data.account || ""}`.includes(query)).map(r => <tr key={r.entity_id}><td>{r.data.title} · v{r.data.revision}<br />{masterLabel(r.data)}<br />{observationPeriod(r.data).replaceAll("|", " · ")}</td><td>{r.data.metric} · {visibleValue(r.data.value)} {r.data.unit}<br />账号：{visibleValue(r.data.account)}</td><td>{r.data.source.label}<br />人工保存，未联网核验</td><td><Link href={operatingHref(workspaceId, { view: "performance", object: r.entity_id, period: entry.period || "all", song:entry.song })}>查看原观察</Link><br /><Link href={songHref(workspaceId, { song: r.data.song_ref })}>进入该作品创作</Link></td></tr>)}</tbody></table>{!observationRows.length && <p>该周期尚无观察，未提供表现、收入或归因结论。</p>}</>}
    {entry.view !== "operating" && <><div className={styles.collectionToolbar}><label>查找{operatingObjectNames[entry.view]}<input aria-label="查找音乐依据" value={query} onChange={e => setQuery(e.target.value)} placeholder="标题或说明" /></label><button disabled={busy || locked || selected && !current} onClick={() => setEditing(true)}>{selected ? "修订这版依据" : `新增${operatingKindNames[defaultKind]}`}</button>{entry.view === "market" && <Link href={operatingHref(workspaceId,{view:"reference"})}>参考分析</Link>}{entry.view === "performance" && <Link href={operatingHref(workspaceId,{view:"report",song:entry.song,period:entry.period})}>分析报告与实际用量</Link>}</div>{!["performance"].includes(entry.view) && <div className={styles.objectList}>{records.filter(r => operatingViewsForKind[r.data.kind] === entry.view && (!query || `${r.data.title} ${r.data.body || ""}`.includes(query))).map(r => <Link aria-current={r.entity_id === entry.object ? "page" : undefined} key={r.entity_id} href={directionHref({view:entry.view,object:r.entity_id,period:entry.period,song:entry.song})}><strong>{r.data.title}</strong><span>v{r.data.revision} · {operatingKindNames[r.data.kind]}</span><small>{r.data.kind === "Learning" ? r.data.accepted_by ? "用途已接受 · 效果待验证" : "待明确接受用途" : r.data.confirmed_by ? "已明确确认" : "原保存依据"}</small></Link>)}{!records.some(r => operatingViewsForKind[r.data.kind] === entry.view) && <p className={styles.empty}>尚无已保存的{operatingObjectNames[entry.view]}。</p>}</div>}</>}
    {selected && <section className={styles.panel}><header className={styles.row}><h2>{selected.data.title} · v{selected.data.revision}</h2><Link href={directionHref({ view: entry.view, period: entry.period, song:entry.song })}>返回原列表与周期</Link></header><p>{operatingKindNames[selected.data.kind]} · {current ? "当前保存版" : "原保存版，只读引用保留"}</p><pre>{selected.data.body || "尚无文字说明"}</pre>{selected.data.scope_ref && <p>原观察范围：{recordLink(selected.data.scope_ref)}</p>}{selected.data.snapshot_ref && <p>原始观察：{recordLink(selected.data.snapshot_ref)}</p>}{selected.data.report_ref && <p>原报告：{recordLink(selected.data.report_ref)}</p>}{selected.data.learning_ref && <p>采用的原经验：{recordLink(selected.data.learning_ref)}</p>}{selected.data.reference_refs?.map(ref => <p key={ref}>原参考：{recordLink(ref)}</p>)}{selected.data.source && <p>来源：{selected.data.source.label} · {selected.data.source.locator}<br />{selected.data.source.note}</p>}{selected.data.kind === "Learning" && <><p>适用范围：{selected.data.applicability}</p><p>反例与限制：{selected.data.counterexample}</p><p>{selected.data.accepted_by ? "用途已明确接受；效果仍待验证。" : "尚未明确接受用途。"}</p></>}
      {report && <><h3>固定原观察</h3><table className={styles.table}><thead><tr><th>原观察</th><th>成品与周期</th><th>原值</th></tr></thead><tbody>{report.rows.map(r => <tr key={r.entity_id}><td>{recordLink(r.entity_id)}</td><td>{masterLabel(r.data)}<br />{observationPeriod(r.data).replaceAll("|", " · ")}</td><td>{r.data.metric} · {visibleValue(r.data.value)} {r.data.unit}<br />{r.data.platform} · 账号：{visibleValue(r.data.account)}<br />{r.data.definition} · {r.data.coverage} · {r.data.method}<br />原来源：{r.data.source.label}（人工、未核验）</td></tr>)}</tbody></table><h3>所选歌曲累计创作调用用量</h3><p>这是关联歌曲的实际创作调用累计，不是观察期间、某版成品或平台表现成本；未分摊，不推算现金收益。</p>{report.usage.length ? report.usage.map(u => <p key={u.usage_record_id}>{u.model_name} · 输入 {visibleValue(u.input_tokens)} / 输出 {visibleValue(u.output_tokens)} Token · 金额 {visibleValue(u.cost_amount)} {u.currency}（原用量记录）</p>) : <p>未提供关联的实际任务用量；不是零费用。没有现金收益、结算或 ROI 依据。</p>}<p>{collection.report_current[selected.entity_id] ? "原报告与当前观察依据一致。" : "当前观察依据已变化；本报告保持原行，确认与沉淀当前候选已停止。"}</p><button disabled={busy || locked || !current || !collection.report_current[selected.entity_id]} onClick={() => submit("confirm-report", { report_ref: selected.entity_id, confirmed: true })}>明确确认原报告事实</button></>}
    </section>}
    {entry.view !== "operating" && editing && <form className={styles.panel} onSubmit={e => { e.preventDefault(); try { submit(operatingActions[kind], payload()); } catch (reason) { setError(reason.message); } }}>
      <header className={styles.row}><h2>{selected ? "保存新的明确版本" : `保存${operatingKindNames[kind]}`}</h2><button type="button" onClick={() => setEditing(false)}>取消编辑</button></header>
      {entry.view === "market" && !selected && <div className={styles.row}><button type="button" onClick={() => setKind("OperatingScope")}>配置观察范围</button><button type="button" onClick={() => setKind("MarketSnapshot")}>保存一次原始观察</button></div>}
      {input("title", "标题", { required: true })}{textarea("body", "说明与判断", ["Direction", "Learning", "ReferenceAnalysis"].includes(kind))}
      {kind !== "OperatingScope" && select("scope_ref", "原观察范围与版本", scopeOptions)}
      {kind === "OperatingScope" && <>{input("platform", "观察平台", { required: true })}{input("keywords", "关键词与观察边界", { required: true })}{periodFields}</>}
      {kind === "MarketSnapshot" && <>{sourceFields}{metricFields}</>}
      {kind === "ReferenceAnalysis" && <>{select("snapshot_ref", "原始观察与版本", snapshotOptions)}<label className={styles.operatingField}>引用用途<select aria-label="引用用途" value={form.purpose || "PATTERN"} onChange={e => field("purpose", e.target.value)}>{[["PATTERN", "有来源的模式判断"], ["EVIDENCE", "证据"], ["CONTEXT", "创作背景"], ["REFERENCE", "原素材参考"], ["STRUCTURE", "结构参考"]].map(([value,label]) => <option key={value} value={value}>{label}</option>)}</select></label>{input("locator", "原材料范围或具体位置", { required: true })}{check("material_available", "已明确提供可查看的原素材（仍未联网核验）")}</>}
      {kind === "Direction" && <>{select("reference_ref", "采用的原参考与版本", referenceOptions)}{check("confirmed", "明确确认这版创作方向")}</>}
      {kind === "Observation" && <>{select("song_ref", "具体作品", songs.map(r => r.song))}{select("master_ref", "明确确认的成品版本", masters)}{select("release_ref", "固定该成品的本地准备包", releases)}<p>本地准备包未发布；人工提供表现描述不升级为发布成功。</p>{input("platform", "观察平台", { required: true })}{sourceFields}{metricFields}</>}
      {kind === "Report" && <><label className={styles.operatingField}>报告周期<select aria-label="报告周期" value={entry.period || selected?.data.selection?.period || "all"} onChange={e => router.push(operatingHref(workspaceId,{...entry,period:e.target.value}))}><option value="all">全部已保存周期</option>{periods.map(period => <option key={period} value={period}>{period.replaceAll("|"," · ")}</option>)}</select></label><p>固定所选范围与当前周期的原观察；说明由你提供，不冒充分析员工或因果验证。</p>{select("song_ref", "仅此作品（留空保留逐作品观察）", songs.map(r=>r.song), false)}</>}
      {kind === "Learning" && <>{select("report_ref", "已明确确认的原报告", reports)}{textarea("applicability", "适用范围", true)}{textarea("counterexample", "反例与限制", true)}{check("accepted", "明确接受这版经验的用途；效果仍待验证")}</>}
      <button disabled={busy || locked || selected && !current} type="submit">{busy ? "正在保存…" : selected ? "保存新版本" : "明确保存"}</button>
    </form>}
    {research && entry.view === "direction" && <ResearchPlanning
      key={JSON.stringify([company, workspaceId, selected?.entity_id, research])} company={company}
      workspaceId={workspaceId} research={research} direction={selected?.data.kind === "Direction" ? selected : null}
      canConfirm={Boolean(current && selected?.data.confirmed_by)} assignments={collection.entry.assignments || []} locked={locked} />}
    {selected?.data.kind === "Direction" && <details className={styles.details}><summary>基于原方向开始或引用到歌曲</summary><section className={styles.panel}><h2>基于这版方向开始创作</h2>{input("new_song_title", "新歌曲名称", { required: true })}{textarea("new_song_intention", "本次明确创作意图", true)}{check("historical", "明确选择原版本及其适用范围，不替换为新版")}{check("creation_confirmed", "明确开始本次新歌曲创作")}
      <button disabled={busy || locked || !selected.data.confirmed_by || !form.creation_confirmed || !form.new_song_title || !form.new_song_intention} onClick={() => submit("create-song", { direction_ref: selected.entity_id, confirmed: form.creation_confirmed, historical: form.historical, title: form.new_song_title, intention: form.new_song_intention, lyrics: "", production: "", draft_revision: form.creation_revision }, "")}>保存并进入新歌曲</button>
      {select("song_ref", "引用到已有作品", songs.map(r=>r.song), false)}<button disabled={busy || locked || !selected.data.confirmed_by || !form.song_ref || !form.creation_confirmed} onClick={() => submit("apply-direction", { direction_ref: selected.entity_id, song_ref: form.song_ref, confirmed: form.creation_confirmed, historical: form.historical }, "")}>明确引用到原作品，保留原创作依据</button>
    </section></details>}
    {selected?.data.kind === "Learning" && <details className={styles.details}><summary>带着原经验进入下一方向</summary><section className={styles.panel}><h2>带着原经验进入下一方向</h2>{input("new_song_title", "下一方向名称")}{textarea("new_song_intention", "引用经验的明确用途", true)}{check("historical", "明确采用所选历史经验及原范围、反例和待验证状态")}{check("confirmed", "明确确认本次引用用途")}
      <button disabled={busy || locked || !selected.data.accepted_by || !form.confirmed || !form.new_song_title || !form.new_song_intention} onClick={() => submit("use-learning", { learning_ref: selected.entity_id, title: form.new_song_title, body: form.new_song_intention, confirmed: form.confirmed, historical: form.historical }, "")}>保存下一方向，不自动执行</button>
    </section></details>}
  </div>;
}
function ResearchPlanning({ company, workspaceId, research, direction, canConfirm, assignments, locked }) {
  const [view, setView] = useState(null), [error, setError] = useState("");
  const [evidence, setEvidence] = useState(""), [assignment, setAssignment] = useState("");
  const [busy, setBusy] = useState(false), [refresh, reread] = useState(0);
  const pending = useRef(false), mounted = useRef(true);
  const { conversation_ref, research_work_ref } = research;
  useEffect(() => { mounted.current = true; return () => { mounted.current = false; }; }, []);
  useEffect(() => {
    let active = true;
    api.researchDelivery(company, workspaceId, conversation_ref, research_work_ref).then(data => {
      if (!active) return;
      if (data.conversation_ref !== conversation_ref || data.research_work_ref !== research_work_ref) {
        setError("原研究交付范围不一致。"); return;
      }
      setView(data);
    }).catch(reason => { if (active) setError(reason.message || "暂时无法读取原研究交付。"); });
    return () => { active = false; };
  }, [company, workspaceId, conversation_ref, research_work_ref, refresh]);
  const saved = view?.planning_receipts.find(item => item.direction_identity_ref === direction?.data.identity_ref);
  const deliveryVersion = item => JSON.stringify([item.evidence_ref, item.evidence_version, item.summary_result_ref, item.summary_result_version]);
  const chosen = view?.deliveries.find(item => deliveryVersion(item) === evidence);
  const author = assignments.find(item => item.assignment_ref === assignment);
  async function confirm() {
    if (pending.current || locked || !canConfirm || saved || !chosen || !author) return;
    pending.current = true;
    setBusy(true); setError("");
    try {
      await api.confirmResearchPlanning(company, workspaceId, { ...research, child_work_ref: chosen.child_work_ref,
        evidence_ref: chosen.evidence_ref, evidence_version: chosen.evidence_version,
        summary_result_ref: chosen.summary_result_ref, summary_result_version: chosen.summary_result_version,
        direction_ref: direction.entity_id, assignment_ref: author.assignment_ref });
    } catch (reason) {
      if (mounted.current) setError(reason.message || "策划工作尚未确认。请核对原记录。");
    } finally {
      pending.current = false;
      if (mounted.current) { setView(null); reread(value => value + 1); setBusy(false); }
    }
  }
  return <section className={styles.panel} aria-label="基于研究交付确认歌曲策划">
    <h2>歌曲策划工作</h2>
    {error && <p role="alert">{error}</p>}
    {view?.planning_receipts.map(item => <p role="status" key={item.work_ref}>
      已创建歌曲策划工作。工作编号：{item.work_ref}
    </p>)}
    {view && !view.deliveries.length && <p role="status">原工作尚无已验收的研究交付。</p>}
    {view && (!canConfirm || saved) && view.deliveries.map(item => <MusicResearchResult key={item.evidence_ref} item={item} />)}
    {view?.deliveries.length > 0 && !saved && (canConfirm ? <>
      <label>原研究证据<select value={evidence} onChange={event => setEvidence(event.target.value)}>
        <option value="">请选择原研究证据</option>
        {view.deliveries.map(item => <option key={item.evidence_ref} value={deliveryVersion(item)}>{item.evidence_summary || item.evidence_ref}</option>)}
      </select></label>
      {chosen && <MusicResearchResult item={chosen} />}
      <label>歌曲创作责任<select value={assignment} onChange={event => setAssignment(event.target.value)}>
        <option value="">请选择歌曲创作责任</option>
        {assignments.map(item => <option key={item.assignment_ref} value={item.assignment_ref}>{item.name || item.responsibility}</option>)}
      </select></label>
      <button type="button" disabled={busy || locked || !chosen || !author} onClick={confirm}>确认并创建歌曲策划工作</button>
    </> : <p>请选择当前已确认的创作方向，再创建歌曲策划工作。</p>)}
    <button type="button" disabled={busy} onClick={() => { setView(null); setError(""); reread(value => value + 1); }}>重新读取原研究交付</button>
  </section>;
}

function observationPeriod(data) { return [data.period.start, data.period.end, data.period.timezone].join("|"); }

export function MusicSongDirectory({ workspaceId, collection, creating, setCreating, busy, locked, createMain }) {
  const [query, setQuery] = useState(""), [status, setStatus] = useState("all");
  const songs = collection.songs.filter(r => (!query || `${r.song.data.title} ${r.song.data.intention}`.includes(query)) && (status === "all" || status === "master" && r.master || status === "draft" && !r.master));
  if (creating) return <div className={styles.creation}><button className={styles.backAction} onClick={() => setCreating(false)}>← 返回歌曲目录</button>{createMain}</div>;
  return <><header className={styles.row}><div><h1>歌曲制作</h1><p className={styles.sub}>意图、歌词、候选、人工选版与成品各自保存</p></div><button className={styles.primary} disabled={busy || locked} onClick={() => setCreating(true)}>新建歌曲</button></header><div className={styles.collectionToolbar}><label>查找歌曲<input aria-label="查找歌曲" placeholder="歌名或创作意图" value={query} onChange={e => setQuery(e.target.value)} /></label><label>作品状态<select value={status} onChange={e => setStatus(e.target.value)}><option value="all">全部歌曲</option><option value="draft">成品待确认</option><option value="master">已有本地成品</option></select></label><span>{songs.length} 首歌曲</span></div>{collection.pending_requests.map(p => <p key={p.attempt_id} className={styles.notice}>原建议{p.status === "RUNNING" ? "处理中" : "待核验"} · <Link href={songHref(workspaceId,{song:p.execution_selection.song_ref,...(p.binding_ref ? {binding:p.binding_ref,attempt:p.attempt_id} : {})})}>查看原请求</Link></p>)}<div className={styles.workRows}>{songs.map(item => <Link key={item.song.entity_id} href={songHref(workspaceId,{song:item.song.entity_id})}><span className={styles.songMark} aria-hidden="true">♪</span><div><strong>{item.song.data.title}</strong><p>{item.song.data.intention || "创作意图待完善"}</p></div><span>{item.candidates.length} 个候选<br />{item.master ? "成品已确认 · 仅本地" : item.choice ? "已选版 · 成品未确认" : "待试听与人工选版"}</span><b>继续制作 →</b></Link>)}</div>{!songs.length && <div className={styles.empty}><h2>{collection.songs.length ? "没有匹配的歌曲" : "开始第一首歌"}</h2><p>先保存自己的创作意图与歌词，再比较实际候选。尚未生成或导入音频。</p></div>}</>;
}

export function MusicReleaseMain({ workspaceId, songs, entry }) {
  const items = songs.filter(s => !entry.song || s.song.entity_id === entry.song).flatMap(s => s.releases.map(pack => ({ song: s, pack })));
  const selected = entry.release ? items.find(x => x.pack.entity_id === entry.release && releaseRecordLabel(x.pack)) : null;
  const master = selected?.song.versions.find(v => v.entity_id === selected.pack.data.master_ref && v.data.kind === "MasterRevision");
  return <><header className={styles.row}><div><h1>发行与发布</h1><p className={styles.sub}>本地准备包 · 固定成品、署名与用途，尚未发布</p></div><Link href={songHref(workspaceId, entry.song ? {song:entry.song,mode:"release"} : {})}>回歌曲准备</Link>{entry.song && <Link href={songHref(workspaceId,{song:entry.song,mode:"candidates"})}>返回同歌试听与人工选版 →</Link>}</header><div className={styles.workRows}>{items.map(({song,pack}) => releaseRecordLabel(pack) ? <Link aria-current={entry.release === pack.entity_id ? "page" : undefined} key={pack.entity_id} href={operatingHref(workspaceId,{view:"release",song:song.song.entity_id,release:pack.entity_id})}><span className={styles.songMark} aria-hidden="true">♪</span><div><strong>{pack.data.title}</strong><p>{releaseRecordLabel(pack)}</p><p>原歌曲：{song.song.data.title}</p></div><span>固定本地成品<br />仅准备 · 未发布</span><b>查看原依据 →</b></Link> : <p key={pack.entity_id} role="status">原准备记录标识不可核对</p>)}</div>{!items.length && <div className={styles.empty}><h2>尚无本地准备包</h2><p>在歌曲中实际试听、明确选版并独立确认成品后，才能保存本地准备。</p></div>}{entry.release && !selected && <p role="alert">原准备包不可读取，没有替换为其它包。</p>}{selected && <section className={styles.panel}><h2>{selected.pack.data.title} · 原准备包</h2><p>{releaseRecordLabel(selected.pack)}</p><p>仅本地使用 · 无商业发行许可</p><h3>固定署名与用途</h3><pre>{selected.pack.data.credits || "原包未提供署名说明"}</pre><h3>原成品依据</h3>{master && <p>成品记录：{master.entity_id}</p>}<p>{master ? "固定原歌词、制作、音频与人工选择；后续修改不会改写原包。" : "原成品暂不可读取"}</p><Link href={songHref(workspaceId,{song:selected.song.song.entity_id,mode:"release"})}>回到该歌曲与成品</Link></section>}<p className={styles.sub}>未连接发行平台 · 本地准备包未发布</p></>;
}
