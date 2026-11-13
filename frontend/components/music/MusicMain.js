"use client";
import EmployeeConversation from "../v1/EmployeeConversation.js";
import { ConversationComposer } from "../v1/SharedConversation.js";
import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { getAssignedAgentWorkflow, publishAssignedAgentWorkflow } from "../../lib/v1FrontendApi.js";
import { EmployeeAvatar } from "../v1/EmployeeAvatar.js";
import { musicApi as api, musicRepairHref, verifiedAudioBlob, prepareLocalWav } from "../../lib/musicApi.js";
import { draftKey, lyricsSelection, audioSelection, selectionCurrent, songBasis, songHref, operatingHref, restoredPlayer, releaseRecordLabel } from "../../lib/musicState.mjs";
import styles from "./Music.module.css";

function AudioPlayer({ company, workspaceId, song, asset, restoreState, onState, returnStart, rangeRequest }) {
  const played = useRef(false);
  const audio = useRef(null), latest = useRef(onState), [url, setUrl] = useState(""), [error, setError] = useState(""), [state, setState] = useState({ ready: false, position: 0, paused: true, duration: 0 });
  const [seek, setSeek] = useState(String(returnStart ?? 0));
  const savedState = useRef(null), rangeIntent = useRef(null), appliedRange = useRef(""), seekInput = useRef(null);
  useEffect(() => { latest.current = onState; }, [onState]);
  useEffect(() => { savedState.current = restoreState; }, [restoreState]);
  const applyRange = useCallback((element) => {
    const intent = rangeIntent.current;
    if (!intent || appliedRange.current === intent.nonce || !Number.isFinite(element.duration)) return;
    if (!Number.isFinite(intent.start) || intent.start < 0 || intent.start >= element.duration) { setError("原范围起点超出实际音频，原锚点保留。"); appliedRange.current = intent.nonce; return; }
    if (!Array.from({ length: element.seekable.length }, (_, i) => [element.seekable.start(i), element.seekable.end(i)]).some(([start, end]) => start <= intent.start && intent.start <= end)) return;
    try { element.currentTime = intent.start; setSeek(String(intent.start)); appliedRange.current = intent.nonce; seekInput.current?.focus(); }
    catch { setError("原音频范围暂时无法定位，请重试原范围。"); }
  }, []);
  const project = useCallback(() => {
    const element = audio.current; if (!element) return;
    applyRange(element);
    if (!element.paused && element.currentTime > 0 && element.readyState >= 2) played.current = true;
    const next = { played: played.current, ready: element.readyState >= 2 && element.duration === asset.data.duration && (!rangeIntent.current || appliedRange.current === rangeIntent.current.nonce), position: element.currentTime, duration: element.duration, paused: element.paused };
    setState(next); latest.current(next);
  }, [applyRange, asset.data.duration]);
  useEffect(() => {
    rangeIntent.current = rangeRequest || (returnStart !== null && returnStart !== undefined ? { start: returnStart, nonce: `entry:${asset.entity_id}:${returnStart}` } : null);
    if (audio.current?.readyState >= 1) project();
  }, [rangeRequest, returnStart, asset.entity_id, project]);
  useEffect(() => {
    let current = true, objectUrl = "";
    played.current = false; setUrl(""); setError(""); setState({ ready: false, position: 0, paused: true, duration: 0 });
    api.media(company, workspaceId, song, asset.entity_id).then((blob) => verifiedAudioBlob(blob, asset)).then((blob) => {
      if (current) { objectUrl = URL.createObjectURL(blob); setUrl(objectUrl); }
    }).catch((reason) => { if (current) { setError(reason.message); latest.current({ ready: false, position: 0, duration: 0, paused: true }); } });
    const element = audio.current;
    return () => {
      current = false;
      if (element) element.pause();
      if (objectUrl) URL.revokeObjectURL(objectUrl);
    };
  // Stable asset identity retains this player across save, selection and fold.
  }, [company, workspaceId, song, asset.entity_id]); // eslint-disable-line react-hooks/exhaustive-deps
  const loaded = () => {
    const element = audio.current;
    if (!element || element.duration !== asset.data.duration) { setError("浏览器解码长度与原资产不一致。"); return; }
    const saved = restoredPlayer(savedState.current, element.duration);
    if (!rangeIntent.current) {
      element.currentTime = saved.position;
      if (!saved.paused) element.play().catch(() => { setError("请点击播放以继续试听。"); project(); });
    }
    project();
  };
  const locate = () => {
    const position = Number(seek), element = audio.current;
    if (!element || !state.ready || !Number.isFinite(position) || position < 0 || position > element.duration) { setError("定位必须位于音频的实际长度内。"); return; }
    element.currentTime = position; setError(""); project();
  };
  return <div className={styles.player}><h3>本地试听</h3><audio ref={audio} src={url || undefined} preload="auto" onLoadedMetadata={loaded} onLoadedData={project} onCanPlay={project} onTimeUpdate={project} onPlay={project} onPause={project} onEnded={project} onError={() => { played.current = false; setError("音频缺失或解码失败，选择与确认已禁用。"); setState((v) => ({ ...v, ready: false })); latest.current({ ready: false, position: 0, duration: 0, paused: true }); }} />
    <div className={styles.actions}><button disabled={!state.ready || Boolean(error)} onClick={() => audio.current?.play().catch((reason) => setError(reason.message))}>播放</button><button disabled={!state.ready || state.paused} onClick={() => audio.current?.pause()}>暂停</button><label>定位（秒）<input ref={seekInput} type="number" min="0" max={asset.data.duration} step="0.1" value={seek} onChange={(e) => setSeek(e.target.value)} /></label><button disabled={!state.ready} onClick={locate}>定位</button></div>
    <output aria-live="off">{state.ready ? `${state.paused ? "暂停" : "播放中"} · ${state.position.toFixed(1)} / ${state.duration} 秒` : "正在读取并核对音频…"}</output>{error && <p className={styles.error} role="alert">{error}</p>}
  </div>;
}

const initialDraft = (row) => ({ title: row?.song.data.title || "", intention: row?.song.data.intention || "", lyrics: row?.lyrics.data.text || "", production: row?.production.data.brief || "" });
export default function MusicMain({ company, workspaceId, row, entry, request, collection, busy: workspaceBusy, locked, perform, inspect, reload }) {
  const [importing, setImporting] = useState(false), importPending = useRef(false), importBasis = useRef("");
  const [manualCandidate, setManualCandidate] = useState({ title: "", suggestion: "" });
  const busy = workspaceBusy || importing;
  const storage = draftKey(company, workspaceId, row?.song.entity_id), mounted = useRef(true), editor = useRef(null), originalView = useRef(null), dialog = useRef(null);
  const [draft, setDraft] = useState(() => initialDraft(row)), [saved, setSaved] = useState(() => songBasis(row)), [revision, setRevision] = useState("initial"), [hydrated, setHydrated] = useState(false);
  const [selection, setSelection] = useState(null), [discussion, setDiscussion] = useState(false), [message, setMessage] = useState(""), [notice, setNoticeState] = useState({ text: "", error: false });
  const setNotice = (text, error = true) => setNoticeState({ text, error });
  const [fileName, setFileName] = useState("");
  const [assignment, setAssignment] = useState(""), [model, setModel] = useState(""), [binding, setBinding] = useState(null), [original, setOriginal] = useState(request || null);
  const [candidateRef, setCandidateRef] = useState(entry.candidate || ""), [range, setRange] = useState({ start: entry.start ?? 0, end: entry.end ?? null });
  const [compareRef, setCompareRef] = useState(entry.compare || "");
  const [rangeRequest, setRangeRequest] = useState(null);
  const [playback, setPlayback] = useState({ asset: "", ready: false, position: 0, duration: 0 }), [players, setPlayers] = useState({}), [tab, setTab] = useState(entry.mode || (entry.candidate ? "candidates" : "lyrics"));
  const [checks, setChecks] = useState({ basis: false, local_only: false }), [credits, setCredits] = useState("");
  const [masterBasis, setMasterBasis] = useState(null), [employeeUtility, setEmployeeUtility] = useState(false);
  useEffect(() => {
    setWholeVersion(true);
    mounted.current = true; setFileName("");
    try {
      const cached = JSON.parse(localStorage.getItem(storage) || sessionStorage.getItem(storage) || "null");
      if (cached) {
        setDraft(cached.draft || initialDraft(row)); setSaved(cached.saved || songBasis(row)); setRevision(cached.revision || "restored"); setSelection(cached.selection || null); setMessage(cached.message || ""); setDiscussion(cached.discussion === true); setAssignment(cached.assignment || ""); setModel(cached.model || ""); setBinding(cached.binding || null); setCandidateRef(entry.candidate || cached.candidateRef || ""); setPlayers(cached.players || {});
      }
      if (row && entry.lyrics && entry.start !== null && !entry.asset) {
        const version = row.versions.find((v) => v.entity_id === entry.lyrics);
        setSelection(lyricsSelection(version, version.data.text, entry.start, entry.end));
      }
    } catch { setNotice("旧输入无法恢复；请核对保存版本。"); }
    setHydrated(true);
    return () => { mounted.current = false; };
  }, [storage]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    if (hydrated) try { localStorage.setItem(storage, JSON.stringify({ draft, saved, revision, selection, message, discussion, assignment, model, binding, candidateRef, players })); } catch {}
  }, [storage, hydrated, draft, saved, revision, selection, message, discussion, assignment, model, binding, candidateRef, playback, players]);
  useEffect(() => { if (request) { setOriginal(request); setDiscussion(true); requestAnimationFrame(() => originalView.current?.focus()); } }, [request]);
  const candidate = candidateRef ? row?.candidates.find((v) => v.entity_id === candidateRef) : row?.candidates.at(-1), asset = row?.assets.find((v) => v.entity_id === candidate?.data.asset_ref);
  const rangeEnd = range.end ?? asset?.data.duration ?? "";
  const holders = collection.entry.assignments.filter(a => a.tenant_id === collection.entry.scope.tenant_id && a.enabled !== false && a.enabled !== 0 && a.scope_type === "WORKSPACE" && a.scope_ref === workspaceId && a.company_id === company && a.workspace_id === workspaceId && a.assignment_ref && a.company_employee_ref);
  const currentHolder = holders.length === 1 ? holders[0] : null;
  useEffect(() => {
    if (!hydrated || locked) return;
    if (!assignment && currentHolder) setAssignment(currentHolder.assignment_ref);
    if (!model && collection.entry.model_preference?.model_key) setModel(collection.entry.model_preference.model_key);
  }, [hydrated, locked, assignment, model, currentHolder, collection.entry.model_preference]);
  const author = collection.entry.assignments.find((a) => a.assignment_ref === assignment);
  const modelCurrent = Boolean(author?.models?.some((m) => m.model_key === model));
  const lyricsDirty = !row || draft.lyrics !== row.lyrics.data.text || saved.lyrics_ref !== row.lyrics.entity_id;
  const productionDirty = !row || draft.production !== row.production.data.brief || saved.production_ref !== row.production.entity_id;
  const detailsDirty = !row || draft.title !== row.song.data.title || draft.intention !== row.song.data.intention;
  const dirty = lyricsDirty || productionDirty || detailsDirty, validSelection = row && selectionCurrent(selection, row, draft.lyrics, draft.production, candidate) && !dirty;
  const [wholeVersion, setWholeVersion] = useState(true);
  const savedSelection = row && !dirty && row.lyrics.data.text.trim()
    ? lyricsSelection(row.lyrics, row.lyrics.data.text, 0, row.lyrics.data.text.length) : null;
  const requestSelection = wholeVersion ? savedSelection : validSelection ? selection : null;
  const currentCandidate = candidate?.data.lyrics_ref === row?.lyrics.entity_id && candidate?.data.production_ref === row?.production.entity_id;
  importBasis.current = JSON.stringify([songBasis(row), draft, revision]);
  const importFile = async event => {
    const file = event.target.files?.[0]; event.target.value = "";
    if (!file || importPending.current || busy || locked || dirty) return;
    importPending.current = true; setImporting(true); setFileName(file.name); setNotice(""); const basis = importBasis.current;
    try {
      const prepared = await prepareLocalWav(file, () => mounted.current && importBasis.current === basis);
      if (prepared) await perform("import-audio", prepared.data, songBasis(row), prepared.bytes);
    } catch (reason) { if (mounted.current) setNotice(`${reason.message} 原文件不会自动重发；可重新选择同一文件查询重试。`); }
    finally { importPending.current = false; if (mounted.current) setImporting(false); }
  };
  const auditionReady = !dirty && currentCandidate && asset && playback.asset === asset.entity_id && playback.ready && playback.played === true && playback.position > 0;
  const pendingOriginal = collection.pending_requests.find((p) => p.execution_selection.song_ref === row?.song.entity_id);
  const field = (key, value) => { setDraft((d) => ({ ...d, [key]: value })); setRevision(crypto.randomUUID()); };
  const operate = async (action, data, expected) => {
    setNotice(""); try { return await perform(action, data, expected); } catch (reason) { if (mounted.current) setNotice(reason.message); return null; }
  };
  const adoptDialogueLyrics = async () => {
    const output = await operate("adopt-dialogue-lyrics", { candidate_ref: candidate.entity_id, confirmed: true }, songBasis(row));
    if (!output || !mounted.current) return;
    setDraft(current => ({ ...current, lyrics: output.lyrics.data.text }));
    setSaved(current => ({ ...current, lyrics_ref: output.lyrics.entity_id }));
    setRevision(output.lyrics.data.draft_revision);
    setSelection(null);
    setTab("lyrics");
    setNotice("已采用为新歌词版本，原版本保留。", false);
  };
  const save = async (part) => {
    if (!row) {
      const output = await operate("create", { ...draft, draft_revision: revision }, {}); if (output) { localStorage.removeItem(storage); sessionStorage.removeItem(storage); } return;
    }
    if (part === "details") { await operate("save-details", { title: draft.title, intention: draft.intention }, { title: row.song.data.title, intention: row.song.data.intention }); return; }
    const lyric = part === "lyrics", key = lyric ? "lyrics_ref" : "production_ref";
    const output = await operate(lyric ? "save-lyrics" : "save-production", { [lyric ? "text" : "brief"]: draft[part], draft_revision: revision }, { [key]: saved[key] });
    if (output && mounted.current) { setSaved((v) => ({ ...v, [key]: output.song.data[key] })); setNotice(output.master ? "已保存新的版本；原版本与已确认成品保留。" : "已保存新的版本；原版本保留，尚未确认成品。", false); }
  };
  const selectText = () => {
    try { const e = editor.current; setSelection(lyricsSelection(row.lyrics, draft.lyrics, e.selectionStart, e.selectionEnd)); setDiscussion(true); setNotice(""); } catch (reason) { setNotice(reason.message); }
  };
  const selectAudio = () => {
    try { if (!playback.ready || playback.asset !== asset?.entity_id) throw new Error("先读取准确资产并确认解码长度。"); if (range.start === "" || rangeEnd === "") throw new Error("请填写引用范围的起点与终点。"); setSelection(audioSelection(row, candidate, asset, Number(range.start), Number(rangeEnd))); setDiscussion(true); setNotice(""); } catch (reason) { setNotice(reason.message); }
  };
  const anchor = row ? { song: row.song.entity_id, mode: tab, ...(candidate ? {candidate:candidate.entity_id} : {}), lyrics: selection?.kind === "lyrics" ? selection.version_ref : row.lyrics.entity_id, production: row.production.entity_id, ...(selection?.kind === "audio" ? { candidate: selection.candidate_ref, asset: selection.asset_ref, hash: selection.sha256, start: selection.start, end: selection.end } : selection ? { start: selection.start, end: selection.end } : {}), ...(original?.binding && original?.attempt?.attempt_id ? { binding: original.binding.binding_ref, attempt: original.attempt.attempt_id } : {}) } : {};
  const repairTarget = (() => { try { return songHref(workspaceId, anchor); } catch { return null; } })();
  const repairHref = (path) => { if (!repairTarget) return null; try { return musicRepairHref(path, repairTarget); } catch { return null; } };
  const employeeHref = (ref) => {
    if (typeof ref !== "string" || !ref.trim() || ref !== ref.trim() || ref === "." || ref === "..") return null;
    try { return repairHref(`/ceo-office/organization/employees/${encodeURIComponent(ref)}`); } catch { return null; }
  };
  const identityHref = (() => {
    const ref = currentHolder?.company_employee_ref, name = currentHolder?.name;
    return row && typeof name === "string" && name.trim() ? employeeHref(ref) : null;
  })();
  const query = async () => {
    const b = original?.binding?.binding_ref || binding?.binding_ref || pendingOriginal?.binding_ref;
    if (!b || !row) return;
    try { const result = await api.query(company, workspaceId, row.song.entity_id, b, original?.attempt?.attempt_id || pendingOriginal?.attempt_id); if (mounted.current) { setOriginal({ ...result, attempt: result.attempt || result.attempts?.at(-1) }); setDiscussion(true); } await reload?.(); } catch (reason) { if (mounted.current) setNotice(reason.message); }
  };
  const [workReview, setWorkReview] = useState(null);
  const send = async () => {
    if (!requestSelection || busy || locked || !author || !modelCurrent) return;
    const review = await getAssignedAgentWorkflow(assignment, company, workspaceId).catch((reason) => { setNotice(reason.message); return null; });
    if (!review) return;
    if (review.state !== "READY") { setWorkReview({ ...review, assignment }); setNotice(review.reason || "请先核对原责任流程。"); return; }
    let bound = binding;
    if (!bound || bound.context.assignment_ref !== assignment || bound.discussion_scope?.object_ref !== row.song.entity_id) bound = await operate("bind", { assignment_ref: assignment }, songBasis(row));
    if (!bound || !mounted.current) return;
    setBinding(bound);
    const created = await operate("create-work", { assignment_ref: assignment, payload: { problem: message, expected_result: "当前明确歌词范围的文字建议，须明确接受；不生成音频或发行", model_key: model, source: { kind: "music", song_ref: row.song.entity_id, expected: songBasis(row), selection: requestSelection, references: [] } } });
    if (!created?.work?.entity_id || !mounted.current) return;
    const result = await operate("send", { work_ref: created.work.entity_id, binding_ref: bound.binding_ref, body: message, model_key: model, selection: requestSelection, references: [] }, songBasis(row));
    if (result && mounted.current) { setOriginal({ binding: bound, attempt: result.attempt, messages: [] }); setNotice("原请求已保存，请查询实际结果。", false); }
  };
  const choose = () => operate("choose", { candidate_ref: candidate.entity_id, audition: { asset_ref: asset.entity_id, sha256: asset.data.sha256, position: playback.position, duration: playback.duration, source: "USER_REPORTED_PLAYBACK" } }, songBasis(row));
  const basisVersion = (ref, kind) => {
    const versions = row?.versions.filter(v => v.entity_id === ref && v.data.kind === kind && v.parent_id === row.song.entity_id && v.tenant_id === collection.entry.scope.tenant_id && v.company_id === company && v.workspace_id === workspaceId) || [];
    return versions.length === 1 ? versions[0] : null;
  };
  const candidateLyrics = candidate && basisVersion(candidate.data.lyrics_ref, "LyricsVersion"), candidateProduction = candidate && basisVersion(candidate.data.production_ref, "ProductionVersion");
  const authorHref = employeeHref(author?.company_employee_ref);
  const capabilityHref = repairHref("/ceo-office/capabilities");
  const employeeDetails = { id: "employee-selection", title: "歌曲责任与能力", content: <div className={styles.context}><h2>歌曲责任与能力</h2><p>只列当前歌曲范围中实际可用的责任员工；选择不扩大执行授权。</p><label>责任员工<select disabled={locked || busy} value={assignment} onChange={e => { setAssignment(e.target.value); setModel(""); }}><option value="">选择当前责任员工</option>{collection.entry.assignments.map(a => <option key={a.assignment_ref} value={a.assignment_ref}>{a.name}</option>)}</select></label>{author && (authorHref ? <Link href={authorHref}>查看员工与能力</Link> : <span className={styles.sub}>员工入口暂不可用，请核对原选段与责任员工。</span>)}{!collection.entry.assignments.length && <p>当前没有合法歌曲责任员工，不能请求员工建议。</p>}</div> };
  useEffect(() => { if (employeeUtility) inspect(employeeDetails, true); }, [employeeUtility, assignment, busy, locked, collection.entry.assignments, repairTarget, inspect]); // eslint-disable-line react-hooks/exhaustive-deps
  const confirmMaster = async (event) => {
    event.preventDefault(); if (!checks.basis || !checks.local_only || !masterBasis) return;
    const result = await operate("confirm-master", { choice_ref: masterBasis.choice_ref, credits, confirmation: checks }, masterBasis.expected);
    if (result) dialog.current?.close();
  };
  const versionLabel = (ref) => { const versions = row?.versions.filter((v) => v.data.kind === "LyricsVersion") || []; const i = versions.findIndex((v) => v.entity_id === ref); return i < 0 ? "原歌词版本" : `歌词 v${i + 1}`; };
  const productionLabel = ref => {
    const versions = row?.versions.filter(v => v.data.kind === "ProductionVersion") || [], index = versions.findIndex(v => v.entity_id === ref);
    return index < 0 ? "制作原版本" : `制作 v${index + 1}`;
  };
  return <>
    <header className={styles.row}><div><h1>{row ? `歌曲《${row.song.data.title}》` : "新建歌曲"}</h1><p className={styles.sub}>{row?.song.data.intention || "从创作意图开始，保存歌词与制作方向。"}{dirty && row ? " · 有未保存修改" : ""}</p></div>{row && <button onClick={() => inspect(row.lyrics.entity_id)}>版本与依据</button>}</header>
    {row?.song.data.direction_ref && <p className={styles.sub}>创作原方向：<Link href={operatingHref(workspaceId,{view:"direction",object:row.song.data.direction_ref,song:row.song.entity_id,period:entry.period})}>查看固定原方向</Link>{row.song.data.learning_ref && <> · <Link href={operatingHref(workspaceId,{view:"learning",object:row.song.data.learning_ref,song:row.song.entity_id,period:entry.period})}>查看采用的原经验</Link></>}</p>}
    <details className={row ? styles.details : styles.newSongIdentity} open={!row}><summary>歌名与创作意图</summary><div className={styles.fields}><label>歌名<input maxLength={240} value={draft.title} onChange={(e) => field("title", e.target.value)} /></label><label>创作意图<input maxLength={2000} value={draft.intention} onChange={(e) => field("intention", e.target.value)} /></label></div>{row && <button disabled={busy || !detailsDirty} onClick={() => save("details")}>保存歌名与意图</button>}</details>
    {row && <><div className={styles.employee}>{identityHref ? <Link href={identityHref} className="inline-flex items-center gap-2" aria-label={`查看${currentHolder.name}的员工详情`}><EmployeeAvatar employee={{ id: currentHolder.company_employee_ref, name: currentHolder.name }} className="h-7 w-7" /><strong>{currentHolder.name}</strong></Link> : <><span className={styles.employeeMark} aria-hidden="true">{currentHolder?.name?.slice(0, 1) || "♪"}</span><strong>{currentHolder?.name || (holders.length > 1 ? "歌曲责任有多项安排" : "当前歌曲责任不可用或尚未安排")}</strong></>}<span className={styles.sub}> · 歌词与制作依据</span><div className={styles.actions}><button onClick={() => { setEmployeeUtility(true); inspect(employeeDetails); }}>责任与能力</button><button aria-expanded={discussion} onClick={() => setDiscussion((v) => !v)}>{discussion ? "收起讨论" : "与员工讨论"}</button></div></div>
      {((assignment && !author) || (model && !modelCurrent)) && <p className={styles.notice}>原员工或模型的资格已改变，输入保留；请重新核对当前合法选项。</p>}
      {locked && <p className={styles.notice}>工作空间有原请求{pendingOriginal?.status === "RUNNING" ? "正在处理" : "待核验"}；暂不能换歌曲、员工或模型再次请求。{pendingOriginal && <button onClick={query}>查看原请求</button>}</p>}
      {<section hidden={!discussion} className={styles.discussion} aria-label="歌曲讨论">
        {currentHolder?.employee_ref && <EmployeeConversation key={`${company}:${workspaceId}:${row.song.entity_id}:${currentHolder.employee_ref}`} companyId={company} employee={{ ...currentHolder, id: currentHolder.company_employee_ref }} active={discussion} blocked={Boolean(locked || busy)} embedded={{ workspaceId, contextKey: `song:${row.song.entity_id}`, objectRef: row.song.entity_id, assignmentRef: currentHolder.assignment_ref, onAgentCandidate: reload, receiveReady: !dirty, agentSourceReady: Boolean(validSelection && selection?.kind === "lyrics"), agentSource: { kind: "music", song_ref: row.song.entity_id, expected: songBasis(row), selection, references: [] }, title: `讨论《${row.song.data.title}》` }} businessReturn={{ href: songHref(workspaceId, entry), kind: "music" }} />}
        <section aria-label="交办当前歌曲"><h3>交办当前保存歌词</h3><div className={styles.row}><h2>讨论当前歌曲</h2>{capabilityHref ? <Link href={capabilityHref}>核对模型</Link> : <span className={styles.sub}>原选段入口暂不可用，请核对或重新选择。</span>}</div>{!wholeVersion && selection ? <div className={styles.selection}><span>{selection.kind === "lyrics" ? `${versionLabel(selection.version_ref)} · ${selection.start}–${selection.end} 字符` : `音频原版本 · ${selection.start}–${selection.end} 秒`} · {validSelection ? "原依据可用" : "原依据已过期，只读"}</span><button onClick={() => { inspect(selection.kind === "lyrics" ? selection.version_ref : selection.candidate_ref); if (selection.kind === "audio") { setCandidateRef(selection.candidate_ref); setRange({ start: selection.start, end: selection.end }); setRangeRequest({ asset: selection.asset_ref, start: selection.start, nonce: crypto.randomUUID() }); setTab("candidates"); } }}>查看原选段</button><button onClick={() => setSelection(null)}>移除选段</button>{selection.kind === "lyrics" && <pre>{selection.excerpt}</pre>}</div> : <p className={styles.sub}>先选择保存歌词或准确音频范围。讨论结果是文字建议。</p>}
        {workReview && <section aria-label="核对本次文字工作责任"><p>{workReview.reason} 发布流程不会发送模型请求。</p>{workReview.state === "NEEDS_PUBLICATION" && workReview.publication_allowed && <button disabled={busy || workReview.assignment !== assignment} onClick={async () => { try { await publishAssignedAgentWorkflow(assignment, { company_id: company, workspace_id: workspaceId, expected_revision: workReview.assignment_revision, review_token: workReview.review_token, confirm: true }); setWorkReview(null); setNotice("原责任流程已确认，请明确交办本次文字工作。"); } catch (reason) { setNotice(reason.message); } }}>明确确认原责任流程</button>}</section>}<ConversationComposer value={message} onChange={setMessage} inputAriaLabel="给员工的留言" maxLength={2000} onSubmit={(event) => { event.preventDefault(); return send(); }} submitLabel={wholeVersion ? "交办当前保存完整歌词" : "仅交办所选范围"} busy={busy} disabled={locked || !requestSelection || !author || !modelCurrent} controls={<><label>本次处理范围<select aria-label="音乐交办范围" value={wholeVersion ? "whole" : "selection"} disabled={locked || busy} onChange={event => setWholeVersion(event.target.value === "whole")}><option value="whole">当前已保存完整歌词</option><option value="selection">仅所选范围</option></select></label><label>本次模型<select disabled={locked || busy} value={model} onChange={(e) => setModel(e.target.value)}><option value="">选择合法模型</option>{author?.models?.map((m) => <option key={m.model_key} value={m.model_key}>{m.display_name || m.model_name || m.model_key}</option>)}</select></label></>} referenceControl={<span>{wholeVersion ? "将发送当前已保存完整歌词；不生成音频" : validSelection ? "原选段已定位" : "请选择原歌词或音频范围"}</span>} notice={wholeVersion ? "明确交办当前保存完整歌词；仍受原有输入上限约束，超限拒绝、不截断。结果须另存候选并由你明确接受。" : "仅按所选范围请求文字建议；结果须另存候选并由你决定是否接受。"} />{(binding || original || pendingOriginal) && <button disabled={busy} onClick={query}>查询原请求</button>}      {original && <section ref={originalView} tabIndex={-1} className={styles.panel}><header className={styles.row}><h2>原请求与结果</h2><button onClick={query}>只读查询</button></header><p>{original.attempt?.status === "COMPLETED" ? "文字建议已完成" : original.attempt?.status === "FAILED" ? "原请求未完成" : "处理中或结果待核验；不会重放"}</p>{original.messages?.map((m) => <article key={m.message_id}><strong>{m.sender.kind === "CEO" ? "你" : currentHolder?.name || "员工"}</strong><pre>{m.sender.kind === "CEO" ? m.body.split("\n歌曲的原保存依据（仅文字建议，不生成音频）：")[0] : m.body}</pre></article>)}{original.attempt?.status === "COMPLETED" && <button disabled={busy} onClick={() => operate("materialize", { binding_ref: original.binding.binding_ref, attempt_id: original.attempt.attempt_id })}>保存为独立文字候选</button>}</section>}</section></section>}
      <nav className={styles.tabs} aria-label="歌曲创作阶段">{[["lyrics", "歌词与结构"], ["candidates", "制作与候选"], ["history", "版本历史"], ["release", "发行依据"], ["analysis", "结果与下一首"]].map(([key, label]) => <button key={key} aria-current={tab === key ? "page" : undefined} onClick={() => setTab(key)}>{label}</button>)}</nav></>}
    {row && tab === "lyrics" && <section className={styles.lyricReadback}><h2>已保存歌词结构</h2><div className={styles.lyricSections}>{row.lyrics.data.text.split(/\n\s*\n/).filter(Boolean).map((part,index)=><article key={index}><h3>{part.split("\n")[0].match(/^\[.*\]$/)?part.split("\n")[0]:`段落 ${index+1}`}</h3><pre>{part}</pre></article>)}</div><p>原保存版本；下方编辑区的修改须独立保存。</p></section>}
    <div hidden={row && tab !== "lyrics"} className={styles.split}><section className={styles.panel}><header className={styles.row}><h2>歌词</h2><div className={styles.actions}>{row && <span className={styles.sub}>{versionLabel(row.lyrics.entity_id)}</span>}<button className={styles.primary} disabled={busy || !lyricsDirty || !draft.title.trim()} onClick={() => save("lyrics")}>{row ? "保存歌词版本" : "创建歌曲"}</button></div></header><textarea ref={editor} className={styles.lyrics} aria-label="当前歌词" maxLength={20000} readOnly={busy} value={draft.lyrics} onChange={(e) => field("lyrics", e.target.value)} />{row && <><button disabled={lyricsDirty || busy} onClick={selectText}>引用所选文字</button><p className={styles.sub}>选中文字后引用，保留原版本、字符范围与原文。</p></>}</section><section className={styles.panel}><header className={styles.row}><h2>结构与制作方向</h2>{row && <button disabled={busy || !productionDirty} onClick={() => save("production")}>保存制作依据</button>}</header><label>制作意图<textarea rows={8} maxLength={2000} value={draft.production} onChange={(e) => field("production", e.target.value)} /></label><p className={styles.notice}>记录结构、声音和制作意图；不会自动生成音频。</p></section></div>
    {row && <><section hidden={!['lyrics','candidates'].includes(tab)} className={styles.panel}><header className={styles.row}><h2>制作与试听比较</h2><div className={styles.actions}>{collection.user_media_configured && <><label className={styles.filePicker}><span>导入本机 WAV</span><input className={styles.fileInput} aria-label="导入本机 WAV" type="file" accept=".wav,audio/wav" disabled={busy || locked || dirty} onChange={importFile} /></label><span className={styles.fileName} role="status">{fileName ? `上次选择：${fileName}` : "尚未选择文件"}</span></>}{collection.legacy_media_configured && ["a", "b"].map((letter) => <button key={letter} disabled={busy || dirty} onClick={() => operate("local-sample", { sample: `demo-${letter}.wav`, title: `本地器乐 ${letter.toUpperCase()}` }, songBasis(row))}>接入本地试听 {letter.toUpperCase()}</button>)}</div></header>
      <p className={styles.sub}>用户提供音频仅限本地使用，商业权利与演唱匹配未核验；实际试听后才可人工选版。最多16MB、10分钟 PCM WAV。{!collection.user_media_configured && "当前安装的普通本机音频存储未配置，不能导入。"}</p>
      <details><summary>保存人工文字候选（无音频）</summary><label>候选名称<input disabled={busy || locked} value={manualCandidate.title} maxLength={240} onChange={e => setManualCandidate(v => ({ ...v, title: e.target.value }))} /></label><label>文字建议<textarea disabled={busy || locked} value={manualCandidate.suggestion} maxLength={20000} onChange={e => setManualCandidate(v => ({ ...v, suggestion: e.target.value }))} /></label><button disabled={busy || locked || dirty || !manualCandidate.title.trim()} onClick={() => operate("candidate", manualCandidate, songBasis(row))}>保存文字候选</button></details>
      {!row.candidates.length ? <p className={styles.notice}>尚无候选。保存歌词与制作意图后，在这里比较；没有音频时不能试听或选版。</p> : <div className={styles.candidates}>{row.candidates.map((c) => <article key={c.entity_id} className={candidate?.entity_id === c.entity_id ? styles.selected : styles.candidate}><button aria-pressed={candidate?.entity_id === c.entity_id} onClick={() => { setCandidateRef(c.entity_id); setRangeRequest(null); inspect(c.entity_id); }}>{c.data.title}</button><p className={styles.sub}>{versionLabel(c.data.lyrics_ref)} · 原制作版本 · {c.data.asset_ref ? "本地音频" : "文字建议，无音频"}</p>{c.data.suggestion && <pre>{c.data.suggestion}</pre>}{c.data.lyrics_ref !== row.lyrics.entity_id || c.data.production_ref !== row.production.entity_id ? <p className={styles.notice}>原依据已过期，保留原版本供查看。</p> : null}</article>)}</div>}
      {row.candidates.length > 1 && <section className={styles.candidateCompare}><header className={styles.row}><h3>两份原候选试听比较</h3><label>比较另一候选<select aria-label="音乐比较候选B" value={compareRef} onChange={e=>{setCompareRef(e.target.value);window.history.replaceState(null,"",songHref(workspaceId,{...entry,song:row.song.entity_id,mode:"candidates",candidate:candidate?.entity_id || candidateRef,compare:e.target.value}));}}><option value="">选择候选 B</option>{row.candidates.filter(v=>v.entity_id!==candidate?.entity_id).map(v=><option key={v.entity_id} value={v.entity_id}>{v.data.title}</option>)}</select></label></header><div className={styles.compareColumns}>{[candidate,row.candidates.find(v=>v.entity_id===compareRef&&v.entity_id!==candidate?.entity_id)].map((value,index)=>{if(!value)return <article key={index}><h4>{index?"B":"A"} · {index&&!compareRef?"请选择另一份原候选":"原候选不存在或不能与自身比较"}</h4></article>;const originalAsset=row.assets.find(a=>a.entity_id===value.data.asset_ref),lyrics=row.versions.find(v=>v.entity_id===value.data.lyrics_ref),production=row.versions.find(v=>v.entity_id===value.data.production_ref);return <article key={value.entity_id}><h4>{index?"B":"A"} · {value.data.title}</h4><p>固定原歌词与制作依据，不自动选版</p><pre>{lyrics?.data.text||"原歌词未提供"}</pre><p>{production?.data.brief||"原制作未提供"}</p>{originalAsset?<AudioPlayer company={company} workspaceId={workspaceId} song={row.song.entity_id} asset={originalAsset} restoreState={players[originalAsset.entity_id]} onState={state=>setPlayers(previous=>JSON.stringify(previous[originalAsset.entity_id])===JSON.stringify(state)?previous:{...previous,[originalAsset.entity_id]:state})}/>:<p>未关联实际音频，不能试听或确认为成品。</p>}<button onClick={()=>{setCandidateRef(value.entity_id);setTab("candidates");}}>回此候选与原范围</button></article>;})}</div></section>}
      {candidate?.data?.provenance?.dialogue_source && !candidate.data.asset_ref && <section className={styles.panel}><p>普通对话原回复；接收版本不代表生成依据。采用会替换当前歌词，原版本保留。</p><button disabled={busy || dirty || candidate.data.lyrics_ref !== row.lyrics.entity_id || candidate.data.production_ref !== row.production.entity_id} onClick={adoptDialogueLyrics}>确认以这条回复替换歌词</button></section>}
      {candidate?.data?.provenance?.execution_selection?.work_ref && !candidate.data.asset_ref && <section className={styles.panel}><p>此项仅接受本次文字 Work 的结果，不代表已试听音频、确认成品或发行。</p><button disabled={busy || dirty || row.text_work_results?.[candidate.entity_id]?.status === "COMPLETED" || candidate.data.lyrics_ref !== row.lyrics.entity_id || candidate.data.production_ref !== row.production.entity_id} onClick={() => operate("accept-text-result", { candidate_ref: candidate.entity_id, confirmed: true }, songBasis(row))}>{row.text_work_results?.[candidate.entity_id]?.status === "COMPLETED" ? "本次文字工作结果已接受" : "明确接受本次文字工作结果"}</button></section>}
      {candidate && <div className={styles.comparison}><section><h3>候选原歌词</h3><pre>{candidateLyrics ? candidateLyrics.data.text || "原歌词为空" : "候选原歌词暂不可读取"}</pre></section><section><h3>候选原制作依据</h3><pre>{candidateProduction ? candidateProduction.data.brief || "原制作依据为空" : "候选原制作依据暂不可读取"}</pre></section></div>}
      {candidateRef && !candidate && <p role="status">原候选暂不可读取，没有替换为其它候选。</p>}
      {asset && <><AudioPlayer key={asset.entity_id} company={company} workspaceId={workspaceId} song={row.song.entity_id} asset={asset} restoreState={players[asset.entity_id]} returnStart={entry.asset === asset.entity_id ? entry.start : null} rangeRequest={rangeRequest?.asset === asset.entity_id ? rangeRequest : null} onState={(state) => { setPlayers((all) => ({ ...all, [asset.entity_id]: { position: state.position, paused: state.paused } })); setPlayback({ ...state, asset: asset.entity_id }); }} /><div className={styles.actions}><label>起点（秒）<input type="number" min="0" max={asset.data.duration} step="0.1" value={range.start} onChange={(e) => setRange((v) => ({ ...v, start: e.target.value }))} /></label><label>终点（秒）<input type="number" min="0" max={asset.data.duration} step="0.1" value={rangeEnd} onChange={(e) => setRange((v) => ({ ...v, end: e.target.value }))} /></label><button disabled={!playback.ready || dirty} onClick={selectAudio}>引用时间范围</button><button disabled={busy || !auditionReady} onClick={choose}>选择此候选</button><button disabled={busy || dirty || !currentCandidate || !playback.ready || playback.asset !== asset.entity_id || !row.choice || row.choice.data.candidate_ref !== candidate.entity_id} onClick={() => { setChecks({ basis: false, local_only: false }); setMasterBasis({ choice_ref: row.choice.entity_id, expected: songBasis(row) }); dialog.current?.showModal(); }}>明确确认成品版本</button></div></>}
      <details className={styles.details}><summary>音频用途与选版说明</summary><p>本地音频仅供本机试听与选版。歌词演唱匹配、商业权利尚未核验；试听后选择候选，再独立确认成品版本。</p></details></section>
      <section hidden={!["lyrics", "candidates", "release"].includes(tab)} className={styles.panel}><header className={styles.row}><h2>人工选择与成品版本</h2>{row.master && <button onClick={() => inspect(row.master.entity_id)}>查看成品原依据</button>}</header><p>{row.choice ? `已选择 ${row.candidates.find((c) => c.entity_id === row.choice.data.candidate_ref)?.data.title || "原候选"}；${row.master ? "另有明确确认的本地成品" : "尚未确认成品版本"}。` : "先实际试听，再选择候选，最后独立确认成品版本。"}</p>{row.master && <p className={styles.notice}>成品版本固定 {versionLabel(row.master.data.lyrics_ref)} 与原制作、音频、署名及用途；后续编辑不会改写这些依据。仅限本地用途，用户提供音频的商业权利未核验，不可据此发行。</p>}</section>
      {tab === "release" && <section className={styles.panel}><header className={styles.row}><h2>发行原依据</h2><button disabled={busy || !row.master} onClick={() => operate("prepare-release", { master_ref: row.master.entity_id }, songBasis(row))}>建立本地发行准备包</button></header>{row.releases.map((pack) => <p key={pack.entity_id}>{releaseRecordLabel(pack) ? <Link href={operatingHref(workspaceId, { view: "release", song: row.song.entity_id, release: pack.entity_id })}>《{pack.data.title}》 · {releaseRecordLabel(pack)} · 固定成品原版本 · 仅准备，未发布</Link> : "原准备记录标识不可核对"}</p>)}<p className={styles.notice}>本地准备记录不代表平台发布；发行账号与商业许可尚未核验。</p><button disabled>发布到平台</button></section>}
      {tab === "analysis" && <section className={styles.panel}><h2>结果、投入与下一首</h2><p>没有已核验的平台表现、收入或因果结论。{row.song.data.schemaVersion === "0.2.0" && <><Link href={operatingHref(workspaceId,{view:"performance",song:row.song.entity_id})}>保存或查看此作品的原观察</Link> · <Link href={operatingHref(workspaceId,{view:"report",song:row.song.entity_id})}>查看原报告与累计创作用量</Link></>}</p><p className={styles.notice}>从这首歌的原观察继续复盘，再明确下一首的方向。</p></section>}

      <details className={styles.details} open={tab === "history"}><summary>保存版本与原依据</summary>{row.versions.filter((v) => ["LyricsVersion", "ProductionVersion", "MasterRevision"].includes(v.data.kind)).map((v) => <button key={v.entity_id} onClick={() => inspect(v.entity_id)}>{v.data.kind === "LyricsVersion" ? versionLabel(v.entity_id) : v.data.kind === "MasterRevision" ? "成品原版本" : productionLabel(v.entity_id)}</button>)}</details>
      <dialog ref={dialog} className={styles.confirm} aria-labelledby="music-master-title"><form onSubmit={confirmMaster}><header className={styles.row}><h2 id="music-master-title">明确确认本地成品</h2><button type="button" onClick={() => dialog.current.close()}>取消</button></header><p>固定原 Choice、歌词、制作和音频版本。本地文件与确认不代表商业发行许可。</p><label className={styles.check}><input type="checkbox" checked={checks.basis} onChange={(e) => setChecks((v) => ({ ...v, basis: e.target.checked }))} />我已核对并明确确认此选择的原依据。</label><label className={styles.check}><input type="checkbox" checked={checks.local_only} onChange={(e) => setChecks((v) => ({ ...v, local_only: e.target.checked }))} />我确认仅限本地使用，无商业发行许可或歌词演唱匹配结论。</label><label>署名与用途说明<textarea maxLength={2000} value={credits} onChange={(e) => setCredits(e.target.value)} /></label><button className={styles.primary} disabled={busy || !checks.basis || !checks.local_only} type="submit">确认并固定 成品原依据</button></form></dialog>
    </>}{notice.text && <p className={notice.error ? styles.error : styles.notice} role={notice.error ? "alert" : "status"}>{notice.text}</p>}
  </>;
}
