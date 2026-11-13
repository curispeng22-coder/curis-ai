"use client";
import EmployeeConversation from "../v1/EmployeeConversation.js";
import { ConversationComposer } from "../v1/SharedConversation.js";
import { useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { getAssignedAgentWorkflow, publishAssignedAgentWorkflow } from "../../lib/v1FrontendApi.js";
import { EmployeeAvatar } from "../v1/EmployeeAvatar.js";
import { contentGrowthApi as api, cgRepairHref } from "../../lib/contentGrowthApi.js";
import { contentHref, selectionFor, selectionCurrent, cgInputKey, cgInputContext, cgInputSnapshot, restoreCgInput, saveCgInput, cgFeedbackKey, restoreCgFeedback, saveCgFeedback, clearCgFeedback, cgFeedbackSourceCurrent, cgFeedbackMatches, cgPreferenceStatus, clearCreatedCgInput, cgDraftOf, CG_FORMATS, shotSelectionFor, cgSelectionFromEntry, cgScriptProjection, cgChecksMatch, cgReferenceLabels, stableRequest } from "../../lib/contentGrowthState.mjs";
import styles from "./ContentGrowth.module.css";
const shotCopy = (shot) => `标题：${shot.title}\n画面与动作：${shot.description}\n镜头要求：${shot.camera}\n字幕：${shot.caption}\n声音：${shot.sound}\n时长：${shot.duration} 秒`;
export default function ContentGrowthMain({ company, workspaceId, entry, row, collection, request, busy, locked, perform, reload, onInspect, initialFormat = "graphic", onFormatChange, initialSources = [] }) {
  const fourForm = collection.entry.definition.version === "0.2.0";
  const draftOf = (value) => ({ ...cgDraftOf(value, fourForm, initialSources), ...(!value && fourForm ? { format: CG_FORMATS[initialFormat] ? initialFormat : "graphic" } : {}) });
  const [shotId, setShotId] = useState("");
  const oldSourceBasis = !row && initialSources.length ? JSON.stringify(initialSources) : "";
  const sourceBasis = !row ? fourForm ? JSON.stringify({ format: initialFormat, sources: initialSources }) : oldSourceBasis : "";
  const storage = cgInputKey(company, workspaceId, row?.content.entity_id, sourceBasis);
  const context = { ...cgInputContext(company, workspaceId, row?.content.entity_id, collection.entry), ...(sourceBasis ? { creationSource: sourceBasis } : {}) }, contextKey = JSON.stringify(context);
  const [hydrated, setHydrated] = useState("");
  const [draft, setDraft] = useState(() => draftOf(row)), [savedBase, setSavedBase] = useState(row?.version.entity_id || "");
  const [selection, setSelection] = useState(() => {
    try { return cgSelectionFromEntry(row, entry); } catch { return null; }
  }), [discussion, setDiscussion] = useState(false);
  const [tool, setTool] = useState(""), [toolRequest, setToolRequest] = useState(0);
  const openTool = (kind) => { setTool(kind); setToolRequest((value) => value + 1); };
  const [assignment, setAssignment] = useState(""), [model, setModel] = useState(""), [message, setMessage] = useState("");
  const [candidateBody, setCandidateBody] = useState(""), [manual, setManual] = useState(false), [candidateRef, setCandidateRef] = useState(entry.candidate || "");
  useEffect(() => { setCandidateRef(entry.candidate || ""); }, [row?.content.entity_id, entry.candidate]);
  const [feedbackChoice, setFeedbackChoice] = useState({ action: "", reason: "", confirmed: false, pending: null, busy: false, error: "", notice: "" });
  const [reviewedCandidate, setReviewedCandidate] = useState("");
  const [checks, setChecks] = useState({ content: false, references: false, account: false }), [notice, setNotice] = useState("");
  const [original, setOriginal] = useState(request || null), [localBusy, setLocalBusy] = useState(false);
  const scriptUtility = useRef(null), shotNodes = useRef(new Map());
  const cacheWritable = useRef(""), editor = useRef(null), sourceView = useRef(null), originalView = useRef(null), mounted = useRef(true);
  useEffect(() => {
    setWholeVersion(true);
    mounted.current = true;
    let cached = null, raw = null;
    try { raw = localStorage.getItem(storage) || sessionStorage.getItem(storage); cached = restoreCgInput(raw, context); } catch {}
    if (!raw && fourForm && !row) {
      try {
        const oldContext = { ...cgInputContext(company, workspaceId, null, collection.entry), ...(oldSourceBasis ? { creationSource: oldSourceBasis } : {}) };
        const previous = restoreCgInput(localStorage.getItem(cgInputKey(company, workspaceId, null, oldSourceBasis)) || sessionStorage.getItem(cgInputKey(company, workspaceId, null, oldSourceBasis)), oldContext);
        if (previous?.draft.format === initialFormat) cached = cgInputSnapshot(context, previous);
      } catch {}
    }
    cacheWritable.current = raw && !cached ? "" : contextKey;
    if (raw && !cached) setNotice("旧输入的身份或范围无法确认，未恢复或覆盖；重新编辑正文后才保存新输入。");
    if (cached) {
      setDraft({ ...draftOf(row), ...cached.draft }); setSavedBase(cached.base); setSelection(entry.version && (entry.shot || entry.start !== null && entry.start !== undefined) ? cgSelectionFromEntry(row, entry) : cached.selection); setMessage(cached.message); setDiscussion(cached.discussion); setAssignment(cached.assignment); setModel(cached.model);
    } else {
      setDraft(draftOf(row)); setSavedBase(row?.version.entity_id || ""); setMessage(""); setDiscussion(false); setAssignment(row?.version.data.work?.assignment_ref || ""); setModel(row?.version.data.work?.model_key || "");
      let originalSelection = null;
      try { originalSelection = cgSelectionFromEntry(row, entry); } catch {}
      setSelection(originalSelection);
    }
    setHydrated(contextKey);
    return () => { mounted.current = false; };
  }, [storage, contextKey]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    if (hydrated !== contextKey || cacheWritable.current !== contextKey) return;
    try { saveCgInput(sessionStorage, storage, cgInputSnapshot(context, { draft, base: savedBase, selection, message, discussion, assignment, model })); }
    catch { setNotice("内容暂存不可用或已满；本次页面输入仍保留。"); }
  }, [storage, contextKey, hydrated, draft, savedBase, selection, message, discussion, assignment, model]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { if (request) { setOriginal(request); setDiscussion(true); requestAnimationFrame(() => originalView.current?.focus()); } }, [request]);
  const dirty = !row || JSON.stringify(draft) !== JSON.stringify(draftOf(row)) || savedBase !== row.version.entity_id;
  const validSelection = row && selectionCurrent(selection, row.version, draft.body) && !dirty;
  const [wholeVersion, setWholeVersion] = useState(true);
  const savedSelection = row && !dirty && row.version.data.body.trim()
    ? selectionFor(row.version, row.version.data.body, 0, row.version.data.body.length) : null;
  const requestSelection = wholeVersion ? savedSelection : validSelection ? selection : null;
  const holders = collection.entry.assignments.filter(a => a.tenant_id === collection.entry.scope.tenant_id && a.enabled !== false && a.enabled !== 0 && a.scope_type === "WORKSPACE" && a.scope_ref === workspaceId && a.company_id === company && a.workspace_id === workspaceId && a.assignment_ref && a.company_employee_ref);
  const currentHolder = holders.length === 1 ? holders[0] : null;
  useEffect(() => {
    if (hydrated !== contextKey || locked) return;
    if (!assignment && currentHolder) setAssignment(currentHolder.assignment_ref);
    if (!model && collection.entry.model_preference?.model_key) setModel(collection.entry.model_preference.model_key);
  }, [hydrated, contextKey, locked, assignment, model, currentHolder, collection.entry.model_preference]);
  const { employee: selectedAssignment, modelCurrent, stale: stalePreference } = cgPreferenceStatus(holders, assignment, model);
  const savedBasisMatches = !fourForm || Boolean(selectedAssignment && modelCurrent
    && row?.version.data.work?.assignment_ref === assignment
    && row?.version.data.work?.recipient_ref === selectedAssignment.company_employee_ref
    && row?.version.data.work?.model_key === model);
  const savedAgentBasisMatches = !fourForm || Boolean(currentHolder
    && row?.version.data.work?.assignment_ref === currentHolder.assignment_ref
    && row?.version.data.work?.recipient_ref === currentHolder.company_employee_ref);
  const executionModel = selectedAssignment?.models?.find((choice) => choice.model_key === model);
  const executionAuthorized = executionModel?.execution_authorized === true;
  const executionNotice = executionModel?.execution_notice || collection.execution_notice || "请核对当前模型的公司文字使用许可。";
  const repairTarget = contentHref(workspaceId, { content: row?.content.entity_id, version: selection?.version_ref || row?.version.entity_id, start: selection?.start, end: selection?.end, shot: selection?.locator === "shot" ? selection.shot_id : undefined, binding: entry.binding, attempt: entry.attempt });
  const repairHref = (path) => { try { return cgRepairHref(path, repairTarget); } catch { return null; } };
  const employeeHref = (ref) => {
    if (typeof ref !== "string" || !ref.trim() || ref !== ref.trim() || ref === "." || ref === "..") return null;
    try { return repairHref(`/ceo-office/organization/employees/${encodeURIComponent(ref)}`); } catch { return null; }
  };
  const identityHref = (() => {
    const ref = currentHolder?.company_employee_ref, name = currentHolder?.name;
    return row && typeof name === "string" && name.trim() ? employeeHref(ref) : null;
  })();
  const selectedEmployeeHref = employeeHref(selectedAssignment?.company_employee_ref);
  const capabilityHref = repairHref("/ceo-office/capabilities");
  const selectedCandidate = row?.candidates.find((c) => c.version.entity_id === candidateRef);
  const candidate = selectedCandidate || null;
  const basisRef = candidate?.version.data.basis_version_ref;
  const basisMatches = basisRef ? row.versions.filter((version) => version.entity_id === basisRef) : [];
  const basis = basisMatches.length === 1 ? basisMatches[0] : null;
  const candidateBasis = basis && collection.entry.scope.tenant_id && basis.entity_type === "CONTENT_VERSION"
    && basis.parent_id === row.content.entity_id && basis.tenant_id === collection.entry.scope.tenant_id
    && basis.company_id === company && basis.workspace_id === workspaceId ? basis : null;
  const feedbackContext = [company, workspaceId, row?.content.entity_id, candidate?.version.entity_id,
    candidate?.feedback_version, candidate?.version.data.basis_version_ref, collection.entry.actor, collection.entry.scope.tenant_id];
  const feedbackStorage = candidate ? cgFeedbackKey(company, workspaceId, row.content.entity_id,
    candidate.version.entity_id, candidate.feedback_version, collection.entry.actor, collection.entry.scope.tenant_id) : "";
  const feedbackIdentity = useRef("");
  feedbackIdentity.current = JSON.stringify(feedbackContext);
  useEffect(() => {
    if (!feedbackStorage) return;
    let saved = null, raw = null, storageError = false;
    try { raw = sessionStorage.getItem(feedbackStorage); saved = restoreCgFeedback(raw, feedbackContext); }
    catch { storageError = true; }
    setFeedbackChoice(saved ? { action: saved.action, reason: saved.reason, confirmed: false, pending: saved.pending || null,
      busy: false, error: "", notice: "原候选输入已恢复；请重新确认。" }
      : { action: "", reason: "", confirmed: false, pending: null, busy: false, error: "", storageBlocked: Boolean(raw),
        notice: raw ? "原候选暂存请求无法核验；已停止新提交，请回原候选核对。" : storageError ? "暂存空间不可用；本次输入仍保留在页面。" : "" });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [feedbackStorage]);
  useEffect(() => {
    if (!feedbackStorage || !feedbackChoice.action && !feedbackChoice.reason && !feedbackChoice.pending) return;
    try { saveCgFeedback(sessionStorage, feedbackStorage, { context: feedbackContext, at: Date.now(),
      action: feedbackChoice.action, reason: feedbackChoice.reason,
      request_id: feedbackChoice.pending?.request_id || "", pending: feedbackChoice.pending }); }
    catch { setFeedbackChoice((value) => ({ ...value, notice: "暂存空间不可用；请保留当前页面和输入。" })); }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [feedbackStorage, feedbackChoice.action, feedbackChoice.reason, feedbackChoice.pending]);
  const submitFeedback = async () => {
    if (!candidate || !candidateBasis || candidateRef !== candidate.version.entity_id || candidate.feedback
      || candidate.version.data.source_class !== "MANUAL_CANDIDATE" || !candidate.eligible || dirty || busy || feedbackChoice.busy
      || feedbackChoice.storageBlocked || !feedbackChoice.confirmed || !feedbackChoice.action || !feedbackChoice.reason.trim()
      || new TextEncoder().encode(feedbackChoice.reason.trim()).length > 2000) return;
    const pending = feedbackChoice.pending || { request_id: crypto.randomUUID(), action: feedbackChoice.action, reason: feedbackChoice.reason.trim() };
    if (pending.action !== feedbackChoice.action || pending.reason !== feedbackChoice.reason.trim()) return;
    const identity = feedbackIdentity.current;
    const current = () => mounted.current && feedbackIdentity.current === identity;
    const expected = { tenant_id: collection.entry.scope.tenant_id, company_id: company, workspace_id: workspaceId,
      actor: collection.entry.actor, content_ref: row.content.entity_id, candidate_ref: candidate.version.entity_id,
      candidate_version: candidate.feedback_version, basis_version_ref: candidate.version.data.basis_version_ref };
    const finish = async (fresh, notice) => {
      if (!current()) return;
      try { clearCgFeedback(sessionStorage, feedbackStorage); } catch { /* Canonical receipt remains saved. */ }
      await reload();
      if (current()) setFeedbackChoice({ action: "", reason: "", confirmed: false, pending: null, busy: false, error: "", notice });
    };
    setFeedbackChoice((old) => ({ ...old, pending, busy: true, error: "", notice: "" }));
    const payload = { candidate_ref: candidate.version.entity_id, candidate_version: candidate.feedback_version,
      basis_version_ref: candidate.version.data.basis_version_ref, action: pending.action, reason: pending.reason, request_id: pending.request_id };
    try {
      const before = await api.content(company, workspaceId, row.content.entity_id);
      if (!current()) return;
      if (cgFeedbackMatches(before, pending, expected)) { await finish(before, "已核实原反馈保存成功。"); return; }
      if (!cgFeedbackSourceCurrent(before, expected) || before.candidates.find((item) => item.version.entity_id === expected.candidate_ref)?.feedback)
        throw new Error("原候选状态或来源已变化，请保留输入并重新核对。");
      await api.feedback(company, workspaceId, row.content.entity_id, payload);
      if (!current()) return;
      const fresh = await api.content(company, workspaceId, row.content.entity_id);
      if (!cgFeedbackMatches(fresh, pending, expected)) throw new Error("原反馈尚未核实，请保留请求并核对。");
      await finish(fresh, "候选评价已保存；没有采用或交给员工。");
    } catch (cause) {
      if (!current()) return;
      try {
        const fresh = await api.content(company, workspaceId, row.content.entity_id);
        if (cgFeedbackMatches(fresh, pending, expected)) { await finish(fresh, "已核实原反馈保存成功。"); return; }
      } catch { /* Unknown effect retains the exact request. */ }
      if (!current()) return;
      setFeedbackChoice((old) => ({ ...old, busy: false, confirmed: false,
        error: `${cause.message}；原输入与请求已保留，请先核对再重试。` }));
    }
  };
  const field = (key, value) => { cacheWritable.current = contextKey; setDraft((current) => ({ ...current, [key]: value })); };
  const workField = (key, value) => field("work", { ...draft.work, [key]: value });
  const chooseEmployee = (value) => {
    setAssignment(value); setModel("");
    if (fourForm) { const found = collection.entry.assignments.find((a) => a.assignment_ref === value); field("work", { ...draft.work, assignment_ref: value, recipient_ref: found?.company_employee_ref || "", model_key: "" }); }
  };
  const chooseModel = (value) => { setModel(value); if (fourForm) workField("model_key", value); };
  const operate = async (action, data, options) => { setNotice(""); try { return await perform(action, data, options); } catch (reason) { if (mounted.current) setNotice(reason.message); return null; } };
  const save = async () => {
    const emptyBasis = fourForm && ["assignment_ref", "recipient_ref", "model_key"].every((key) => draft.work?.[key] === "");
    const canSaveAgentBasis = !model && currentHolder && currentHolder.assignment_ref === assignment;
    const submitted = emptyBasis && selectedAssignment && (modelCurrent || canSaveAgentBasis)
      ? { ...draft, work: { ...draft.work, assignment_ref: assignment, recipient_ref: selectedAssignment.company_employee_ref, model_key: modelCurrent ? model : "" } }
      : draft;
    const result = await operate(row ? "save" : "create", submitted, { base: savedBase });
    if (!row && result) { try { clearCreatedCgInput(sessionStorage, storage, context, draft, result); } catch {} }
    if (result && mounted.current && row) { const next = draftOf(result); setDraft(next); setSavedBase(result.version.entity_id); setNotice("已保存为新版本；发送建议前请重新选择片段。"); }
  };
  const restoreSelection = () => {
    if (!validSelection) { setNotice("选段来自原版本，只能查看原依据；请重新选择。"); if (sourceView.current) { sourceView.current.open = true; sourceView.current.focus(); } return; }
    if (selection.locator === "shot") {
      openTool("shot");
      if (scriptUtility.current) scriptUtility.current.open = true;
      setShotId(selection.shot_id);
      requestAnimationFrame(() => { const node = shotNodes.current.get(selection.shot_id); if (node) { node.open = true; node.focus(); node.scrollIntoView({ block: "center" }); } });
      return;
    }
    editor.current?.focus(); editor.current?.setSelectionRange(selection.start, selection.end);
  };
  const query = async () => {
    const pending = collection.pending_requests.find((a) => a.content_ref === row.content.entity_id);
    const binding = entry.binding || original?.binding.binding_ref || pending?.binding_ref;
    const attempt = entry.attempt || original?.attempt?.attempt_id || pending?.attempt_id;
    if (!binding || !attempt) return;
    setLocalBusy(true); try { const result = await api.query(company, workspaceId, row.content.entity_id, binding, attempt); if (mounted.current) { setOriginal(result); setDiscussion(true); await reload(); originalView.current?.focus(); } }
    catch (reason) { if (mounted.current) setNotice(reason.message); } finally { if (mounted.current) setLocalBusy(false); }
  };
  const [workReview, setWorkReview] = useState(null);
  const send = async () => {
    if (busy || localBusy || locked || hydrated !== contextKey || !requestSelection || !modelCurrent || !selectedAssignment || !executionAuthorized || !savedBasisMatches) return;
    const review = await getAssignedAgentWorkflow(assignment, company, workspaceId).catch((reason) => { setNotice(reason.message); return null; });
    if (!review) return;
    if (review.state !== "READY") { setWorkReview({ ...review, assignment }); setNotice(review.reason || "请先核对原责任流程。"); return; }
    const previousBinding = original?.binding;
    const binding = previousBinding?.context?.assignment_ref === assignment && previousBinding?.discussion_scope?.object_ref === row.content.entity_id ? previousBinding : await operate("bind", { assignment_ref: assignment });
    if (!binding || !mounted.current) return;
    const created = await operate("create-work", { assignment_ref: assignment, payload: { problem: message, expected_result: "当前明确范围的文字候选，须明确采用", model_key: model, source: { kind: "content-growth", content_ref: row.content.entity_id, expected_version_ref: row.version.entity_id, selection: requestSelection, references: draft.references } } });
    if (!created?.work?.entity_id || !mounted.current) return;
    const output = await operate("send", { work_ref: created.work.entity_id, binding_ref: binding.binding_ref, body: message, model_key: model, selection: requestSelection, references: draft.references });
    if (output && mounted.current) { const result = await api.query(company, workspaceId, row.content.entity_id, binding.binding_ref, output.attempt.attempt_id); if (mounted.current) setOriginal(result); }
  };
  const scriptHistory = (version) => {
    const view = cgScriptProjection(version.data);
    if (!view) return null;
    return <details><summary>原脚本与镜头依据 · 只读</summary><p>目标：{view.goal}</p><p>输出意图：{view.intent} · 规格：{view.spec}</p><p>录制要求：{view.recording}</p><p>原责任员工：{view.employee} · 原模型：{view.model}</p>{view.sources.map((source, index) => {
      const ref = version.data.work.source_refs[index];
      const parent = ref.kind === "CONTENT_ITEM" ? ref.reference_id : ref.kind === "CONTENT_VERSION" ? collection.contents.find((item) => item.versions.some((v) => v.entity_id === ref.reference_id))?.content.entity_id : null;
      return <p key={index}>原来源：{parent ? <Link href={contentHref(workspaceId, { content: parent, version: ref.version_ref })}>{source.title}</Link> : source.title} · 已保留原版本依据</p>;
    })}{view.shots.map((shot, index) => <p className={styles.originalBasis} key={index}>{shotCopy(shot)}</p>)}</details>;
  };
  const originalVersion = row?.versions.find((v) => v.entity_id === selection?.version_ref);
  const returnVersion = entry.version && row?.versions.find((v) => v.entity_id === entry.version);
  const referenceLabels = cgReferenceLabels([...(collection.reference_options || []), ...draft.references, ...(draft.work?.source_refs || [])], collection.contents || [], collection.entry?.scope);
  const referenceText = (ref) => referenceLabels.get(ref.reference_id) || "来源需核对";
  const labels = { metadata: "内容信息", references: "引用依据", basis: "制作依据", shot: "镜头详情", versions: "正文版本", responsibility: "员工与能力" };
  const toolContent = useMemo(() => !tool ? null : <div className={`${styles.main} ${styles.utility}`}><header className={styles.row}><h2>{labels[tool]}</h2><button className={styles.formDismiss} onClick={() => setTool("")}>返回创作</button></header>{tool === "responsibility" && row && <section><h3>当前责任员工</h3><select aria-label="内容责任员工" disabled={locked || busy} value={assignment} onChange={(e) => chooseEmployee(e.target.value)}><option value="">请选择当前合法员工</option>{assignment && !selectedAssignment && <option value={assignment}>原员工（请重新核对）</option>}{collection.entry.assignments.map((a) => <option key={a.assignment_ref} value={a.assignment_ref}>{a.name}</option>)}</select>{selectedAssignment && (selectedEmployeeHref ? <Link href={selectedEmployeeHref}>核对员工能力</Link> : <span className={styles.sub}>员工入口暂不可用，请核对原选段与责任员工。</span>)}<h3>讨论能力</h3><p className={styles.sub}>{selectedAssignment ? "发送前仍需核对当前模型、选段与执行授权。" : "请选择本次讨论的合法员工；未选择时不发送建议。"}</p>{stalePreference && <p className={styles.notice}>原员工或模型资格已变化，输入仍保留；请选择当前有效选项。</p>}{capabilityHref ? <Link href={capabilityHref}>核对模型与能力</Link> : <span className={styles.sub}>原选段入口暂不可用，请核对或重新选择。</span>}</section>}{tool === "metadata" && <div className={styles.fields}>{[ ["title", "标题", 240], ["topic", "主题", 1000], ["audience", "受众", 1000] ].map(([key, label, max]) => <label key={key}>{label}<input maxLength={max} value={draft[key]} onChange={(event) => field(key, event.target.value)} /></label>)}</div>}{tool === "references" && <>{row && <details open className={styles.references}><summary>引用依据 · {draft.references.length ? `${draft.references.length} 项` : "尚未连接"}</summary><p className={styles.sub}>仅显示当前范围真实来源；保存时绑定它的实际版本。来源改变会阻止旧候选采用。</p>{collection.reference_options.filter((r) => r.reference_id !== row.content.entity_id && !row.versions.some((v) => v.entity_id === r.reference_id)).map((ref) => { const chosen = draft.references.find((r) => r.reference_id === ref.reference_id); return <div key={ref.reference_id} className={styles.reference}><label><input type="checkbox" checked={Boolean(chosen)} disabled={draft.references.length >= 8 && !chosen} onChange={(e) => field("references", e.target.checked ? [...draft.references, ref] : draft.references.filter((r) => r.reference_id !== ref.reference_id))} />{referenceText(ref)}</label>{chosen && <select aria-label={`引用用途 · ${referenceText(ref)}`} value={chosen.purpose} onChange={(e) => field("references", draft.references.map((r) => r.reference_id === ref.reference_id ? { ...r, purpose: e.target.value } : r))}>{(fourForm ? [["ORIGINAL", "原文"], ["PATTERN", "结构范例"], ["EVIDENCE", "事实依据"], ["DIRECTION", "方向参考"], ["CONTEXT", "工作背景"]] : [["BACKGROUND", "背景"], ["FACT", "事实依据"], ["STYLE", "风格参考"], ["CONSTRAINT", "约束"]]).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select>}</div>; })}{draft.references.filter((r) => !collection.reference_options.some((n) => n.reference_id === r.reference_id)).map((ref) => <p key={ref.reference_id}>原来源当前不可用：{referenceText(ref)}<button onClick={() => field("references", draft.references.filter((r) => r.reference_id !== ref.reference_id))}>移除引用</button></p>)}</details>}</>}{["basis", "shot"].includes(tool) && <>{fourForm && <details open ref={scriptUtility} className={styles.scriptUtility}><summary>脚本依据与镜头 · 按需编辑</summary>
      <label>本次目标<textarea aria-label="本次内容目标" maxLength={1000} value={draft.work.goal} onChange={(e) => workField("goal", e.target.value)} /></label>
      <label>输出意图<select aria-label="本次输出意图" value={draft.work.output_intent} onChange={(e) => workField("output_intent", e.target.value)}><option value="UNCONFIRMED">尚未确认</option><option value="AUDIO">本次制作音频</option><option value="VIDEO">本次制作视频</option></select></label>
      <label>输出规格<input aria-label="本次输出规格" maxLength={1000} value={draft.work.output_spec} onChange={(e) => workField("output_spec", e.target.value)} /></label>
      <label>录制要求<textarea aria-label="录制要求" maxLength={2000} value={draft.work.recording_requirements} onChange={(e) => workField("recording_requirements", e.target.value)} /></label>
      <p className={styles.notice}>本机媒体请在实际预览后单独确认采用；脚本采用不代表媒体已完成，商业权利仍未核验。发布核验、人工经营记录与内容经验分别保留原依据，不代表平台已发布或效果已验证。</p>
      <details><summary>原计划来源 · 仅真实范围与版本</summary>{collection.reference_options.filter((ref) => ref.reference_id !== row?.content.entity_id && !row?.versions.some((v) => v.entity_id === ref.reference_id)).map((ref) => { const chosen = draft.work.source_refs.some((s) => s.reference_id === ref.reference_id); return <label key={ref.reference_id}><input type="checkbox" checked={chosen} disabled={!chosen && draft.work.source_refs.length >= 8} onChange={(e) => workField("source_refs", e.target.checked ? [...draft.work.source_refs, { ...ref, purpose: "CONTEXT" }] : draft.work.source_refs.filter((s) => s.reference_id !== ref.reference_id))} />{referenceText(ref)}</label>; })}{draft.work.source_refs.filter((ref) => !collection.reference_options.some((s) => s.reference_id === ref.reference_id)).map((ref) => <p key={ref.reference_id}>原来源需重新核对：{referenceText(ref)}<button onClick={() => workField("source_refs", draft.work.source_refs.filter((s) => s.reference_id !== ref.reference_id))}>移除原来源</button></p>)}</details>
      {draft.format !== "graphic" && <><div className={styles.row}><h3>镜头脚本</h3><button disabled={draft.work.shots.length >= 40} onClick={() => { const id = crypto.randomUUID(); workField("shots", [...draft.work.shots, { id, title: "", description: "", camera: "", caption: "", sound: "", duration: 0 }]); setShotId(id); }}>添加镜头</button></div>
      {draft.work.shots.map((shot, index) => <details key={shot.id} tabIndex={-1} ref={(node) => { if (node) shotNodes.current.set(shot.id, node); else shotNodes.current.delete(shot.id); }} open={shotId === shot.id} className={styles.shot}><summary onClick={(e) => { e.preventDefault(); setShotId(shotId === shot.id ? "" : shot.id); }}>镜头 {index + 1} · {shot.title || "待填写"}</summary>{[["title", "镜头标题", 240], ["description", "画面与动作", 2000], ["camera", "镜头要求", 1000], ["caption", "字幕", 1000], ["sound", "声音", 1000]].map(([key, label, max]) => <label key={key}>{label}<textarea aria-label={label} maxLength={max} value={shot[key]} onChange={(e) => workField("shots", draft.work.shots.map((s) => s.id === shot.id ? { ...s, [key]: e.target.value } : s))} /></label>)}<label>时长（秒）<input aria-label="镜头时长" type="number" min="0" max="600" value={shot.duration} onChange={(e) => workField("shots", draft.work.shots.map((s) => s.id === shot.id ? { ...s, duration: Number(e.target.value) } : s))} /></label><button disabled={!row || dirty || ![shot.title, shot.description, shot.caption].some((text) => text.trim())} onClick={() => { try { setSelection(shotSelectionFor(row.version, shot.id)); } catch (reason) { setNotice(reason.message); } }}>选择此保存镜头</button></details>)}</>}
    </details>}</>}{tool === "versions" && row && <><details open className={styles.versions}><summary>正文版本记录 · {row.versions.filter((v) => v.data.kind !== "candidate").length} 个</summary>{row.versions.filter((v) => v.data.kind !== "candidate").map((v, i) => <details key={v.entity_id}><summary>保存版本 {i + 1}{v.entity_id === row.version.entity_id ? " · 当前" : " · 原依据"}</summary>{v.data.body ? <p className={styles.bodyCopy}>{v.data.body}</p> : v.data.learning_ref ? <p className={styles.sub}>正文为空；该版本保存经验依据。</p> : <p className={styles.bodyCopy}>{v.data.body}</p>}{v.data.learning_ref && <section><h3>经验依据稿 · {v.entity_id === row.version.entity_id ? "当前正文" : "未替换当前正文"}</h3><p className={styles.sub}>已引用的内容经验（引用时快照）</p><dl className={styles.definition}>{[["引用时经验原文", v.data.learning_body], ["引用时适用范围", v.data.learning_applicability], ["引用时反例/限制", v.data.learning_counterexample]].map(([label, value]) => <div key={label}><dt>{label}</dt><dd>{value || "引用时未填写"}</dd></div>)}</dl><details><summary>查看经验标识</summary><p className={styles.originalBasis}>{v.data.learning_ref}</p></details></section>}{scriptHistory(v)}</details>)}</details></>}</div>, [tool, draft, row, collection, shotId, assignment, selectedAssignment, stalePreference, locked, busy, repairTarget]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { onInspect?.(toolContent ? { id: JSON.stringify([company, workspaceId, contextKey, tool]), title: labels[tool], content: toolContent, request: toolRequest } : null); }, [onInspect, toolContent, toolRequest, contextKey, company, workspaceId, tool]); // eslint-disable-line react-hooks/exhaustive-deps
  return <>
    <header className={`${styles.row} ${styles.objectHeader}`}><div className={styles.objectIdentity}><h1>{row ? draft.title : "新建内容"}</h1><span className={styles.sub}>{fourForm ? CG_FORMATS[draft.format] : "图文"} · 本地正文</span></div>{row && <Link href={contentHref(workspaceId, { view: "production" })}>← 制作目录</Link>}</header>
    {returnVersion && returnVersion.entity_id !== row.version.entity_id && <details open className={styles.notice}><summary>从旧正文版本返回，以下仅供核对</summary><p className={styles.bodyCopy}>{returnVersion.data.body}</p><p>当前正文已更新；原选段不会迁移到新正文。</p></details>}
    {fourForm && !row && <label className={styles.formatChoice}>创作方式<select aria-label="内容形态" value={draft.format} onChange={(e) => onFormatChange ? onFormatChange(e.target.value) : field("format", e.target.value)}>{Object.entries(CG_FORMATS).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label>}
    {!row && <div className={styles.fields}>{[ ["title", "标题", 240], ["topic", "主题", 1000], ["audience", "受众", 1000] ].map(([key, label, max]) => <label key={key}>{label}<input maxLength={max} value={draft[key]} onChange={(event) => field(key, event.target.value)} /></label>)}</div>}
    {row && <div className={styles.employee}><span>责任</span>{identityHref ? <Link href={identityHref} className="inline-flex items-center gap-2" aria-label={`查看${currentHolder.name}的员工详情`}><EmployeeAvatar employee={{ id: currentHolder.company_employee_ref, name: currentHolder.name }} className="h-7 w-7" /><strong>{currentHolder.name}</strong></Link> : <strong>{currentHolder?.name || (holders.length > 1 ? "责任有多项安排" : "当前责任不可用或尚未安排")}</strong>}<button disabled={locked || busy} onClick={() => openTool("responsibility")}>查看与配置</button><button onClick={() => setDiscussion(!discussion)}>{discussion ? "收起讨论" : "展开讨论"}</button></div>}
    {row && <section hidden={!discussion} className={styles.conversation} aria-label="内容讨论">
      {!savedAgentBasisMatches && <p role="status">当前保存版本的责任与所选员工不一致，请核对责任并保存正文，再重新选择片段。</p>}
      {currentHolder?.employee_ref && <EmployeeConversation key={`${company}:${workspaceId}:${row.content.entity_id}:${currentHolder.employee_ref}`} companyId={company} employee={{ ...currentHolder, id: currentHolder.company_employee_ref }} active={discussion} blocked={Boolean(locked || busy || localBusy)} embedded={{ workspaceId, contextKey: `content:${row.content.entity_id}`, objectRef: row.content.entity_id, assignmentRef: currentHolder.assignment_ref, onAgentCandidate: reload, receiveReady: !dirty, agentSourceReady: Boolean(validSelection && savedAgentBasisMatches), agentSource: { kind: "content-growth", content_ref: row.content.entity_id, expected_version_ref: row.version.entity_id, selection, references: draft.references }, title: `讨论《${row.version.data.title}》` }} businessReturn={{ href: contentHref(workspaceId, { ...entry, content: row.content.entity_id }), kind: "content-growth" }} />}
      <section aria-label="交办当前内容"><h3>交办当前保存正文</h3>
      <ConversationComposer className={styles.discussionComposer} value={message} onChange={setMessage} inputAriaLabel="内容讨论输入" maxLength={2000} onSubmit={(event) => { event.preventDefault(); return send(); }} submitLabel={wholeVersion ? "交办当前保存完整正文" : "仅交办所选片段"} placeholder="说明希望员工怎样改进当前保存正文" busy={busy || localBusy} disabled={locked || hydrated !== contextKey || !requestSelection || !selectedAssignment || !modelCurrent || !executionAuthorized || !savedBasisMatches} controls={<><label>本次处理范围<select aria-label="内容交办范围" value={wholeVersion ? "whole" : "selection"} disabled={locked || busy || localBusy} onChange={event => setWholeVersion(event.target.value === "whole")}><option value="whole">当前已保存完整正文</option><option value="selection">仅所选片段或镜头</option></select></label><select aria-label="内容建议模型" value={model} disabled={locked || busy} onChange={(e) => chooseModel(e.target.value)}><option value="">选择可用模型</option>{model && !modelCurrent && <option value={model}>原模型（请重新核对）</option>}{selectedAssignment?.models.map((m) => <option key={m.model_key} value={m.model_key}>{m.display_name || m.model_name}</option>)}</select>{capabilityHref && <Link href={capabilityHref}>核对模型</Link>}</>} referenceControl={<span>{wholeVersion ? "将发送当前已保存完整正文；未保存修改不会发送" : validSelection ? "原选段已定位" : "请选择已保存正文的范围"}</span>} notice={locked ? "原请求仍在处理或等待核验；员工、模型和发送保持锁定。" : !executionAuthorized ? executionNotice : !savedBasisMatches ? (wholeVersion ? "当前员工或模型与保存依据不一致；请核对并保存正文。" : "当前员工或模型与保存依据不一致；请明确选择、保存正文后重新选择片段。") : !requestSelection ? (wholeVersion ? "先保存非空正文，再核对当前员工和模型。" : "先保存正文并选择片段，再核对当前员工和模型。") : "按上方明确范围交办；超出原有输入上限会拒绝，不会截断。"} />
      <button disabled={localBusy || !(original || collection.pending_requests.some((r) => r.content_ref === row.content.entity_id))} onClick={query}>查看原请求</button>
      {original && <div className={styles.result} tabIndex={-1} ref={originalView}><h3>原请求</h3><p>{(original.attempt || original.attempts?.[0])?.status === "COMPLETED" ? <span className={styles.statusDone}>建议已返回并核验</span> : (original.attempt || original.attempts?.[0])?.status === "RUNNING" ? <span className={styles.statusPending}>处理中</span> : <span className={styles.statusWarn}>结果待核验；不会重复发送</span>}</p>{original.messages?.map((m) => <article key={m.message_id}><strong>{m.sender.kind === "CEO" ? "你" : currentHolder?.name || "员工"}</strong><p className={styles.bodyCopy}>{m.sender.kind === "CEO" ? m.body.split("\n保存的内容与脚本依据：")[0] : m.body}</p></article>)}{original.attempt?.status === "COMPLETED" && <button disabled={busy} onClick={() => operate("materialize", { binding_ref: original.binding.binding_ref, attempt_id: original.attempt.attempt_id })}>将已核验建议存为候选</button>}</div>}
    </section></section>}
    {row?.operating_context && <section className={styles.notice}><h3>原方向与创作依据</h3><p>{row.operating_context.payload.title} · 已明确引用，不改写正文</p><Link href={contentHref(workspaceId,{view:"market",object:row.operating_context.payload.direction_ref||undefined})}>查看原方向与来源 →</Link></section>}
    <nav className={styles.localStages} aria-label="本地制作步骤"><span>意图与方向</span><span>正文 / 脚本与分镜</span><span>本机素材与预览</span><span>人工审阅与采用</span><Link href={contentHref(workspaceId,{view:"verify",object:row?.content.entity_id})}>逐账号本地核验 →</Link></nav>
    <div className={styles.toolbar}><button onClick={() => openTool("metadata")}>内容信息</button><button onClick={() => openTool("references")} disabled={!row}>引用依据</button>{fourForm && <button onClick={() => openTool("basis")}>制作依据</button>}{row && <button onClick={() => openTool("versions")}>版本记录</button>}</div>
    <div className={styles.scriptGrid}><section className={styles.editor}><header><strong>正文</strong><span className={dirty ? styles.stateDirty : styles.stateSaved}>{dirty ? "有未保存改动" : "已保存"}</span></header><textarea ref={editor} aria-label="内容正文与脚本" maxLength={20000} value={draft.body} onChange={(e) => field("body", e.target.value)} onSelect={(e) => { if (!row || e.target.selectionStart === e.target.selectionEnd) return; try { setSelection(selectionFor(row.version, draft.body, e.target.selectionStart, e.target.selectionEnd)); setNotice(""); } catch (reason) { setNotice(reason.message); } }} /></section>{fourForm && draft.format !== "graphic" && <section className={styles.shotList}><header className={styles.row}><h2>分镜与表达</h2><button disabled={draft.work.shots.length >= 40} onClick={() => { const id = crypto.randomUUID(); workField("shots", [...draft.work.shots, { id, title: "", description: "", camera: "", caption: "", sound: "", duration: 0 }]); setShotId(id); openTool("shot"); }}>添加镜头</button></header>{draft.work.shots.map((shot, index) => <button key={shot.id} className={styles.shotTile} onClick={() => { setShotId(shot.id); openTool("shot"); }}><strong>镜头 {index + 1} · {shot.title || "待填写"}</strong><span>{shot.description || "补充画面与表达要求"}</span><small>{shot.duration > 0 ? `${shot.duration} 秒` : "时长待填写"} · {shot.camera || "镜头要求待填写"}</small></button>)}{!draft.work.shots.length && <p className={styles.emptyRow}>从第一段画面与表达开始。没有真实媒体时，保留脚本和镜头要求。</p>}</section>}</div>
    {row && <LocalGrowthMedia company={company} workspaceId={workspaceId} row={row} dirty={dirty} locked={locked} onInspect={onInspect} initialAsset={entry.media || ""} />}
    <div className={styles.actions}><button disabled={busy || !draft.title.trim() || !draft.topic.trim() || !draft.audience.trim()} className={styles.primary} onClick={save}>{busy ? "处理中…" : row ? "保存正文" : "创建本地草稿"}</button><span className={styles.sub}>保存不会发布到账号。</span></div>
    {!wholeVersion && selection && <div className={styles.selection}><div><strong className={validSelection ? styles.selectionTitle : styles.selectionReadonly}>{validSelection ? "当前选段" : "原版本选段 · 只读依据"}</strong><p>“{selection.locator === "shot" ? selection.shot_snapshot.title || selection.shot_snapshot.description : selection.excerpt}”</p></div><button onClick={restoreSelection}>{validSelection ? "回到选段" : "查看原依据"}</button>{!validSelection && <details ref={sourceView} tabIndex={-1}><summary>原保存正文</summary><p className={styles.bodyCopy}>{selection.locator === "shot" ? shotCopy(selection.shot_snapshot) : originalVersion?.data.body || "原正文尚未读取"}</p><button onClick={() => { setSelection(null); editor.current?.focus(); }}>重新选择</button></details>}</div>}

    {row && <section className={styles.result}><div className={styles.row}><h2>候选与人工采用</h2><button disabled={busy || dirty || !validSelection} onClick={() => setManual(!manual)}>准备人工候选</button></div>{manual && <div className={styles.block}><p>这是人工准备的候选，不是员工执行结果。</p><textarea aria-label="人工候选正文" maxLength={20000} value={candidateBody} onChange={(e) => setCandidateBody(e.target.value)} /><button disabled={busy || dirty || !validSelection || !candidateBody.trim()} onClick={async () => { const result = await operate("candidate", { ...draft, body: candidateBody, selection }); if (result && mounted.current) { setManual(false); setCandidateBody(""); } }}>保存候选</button></div>}
      {row.candidates.length > 0 && <><select aria-label="查看内容候选" value={candidate?.version.entity_id || ""} onChange={(e) => { const chosen = row.candidates.find((item) => item.version.entity_id === e.target.value); setCandidateRef(e.target.value); setChecks({ content: false, references: false, account: false }); if (chosen) window.history.replaceState(null, "", contentHref(workspaceId, { content: row.content.entity_id, version: chosen.version.data.basis_version_ref, candidate: chosen.version.entity_id })); }}><option value="">请选择一份候选</option>{row.candidates.map((c, i) => <option key={c.version.entity_id} value={c.version.entity_id}>候选 {i + 1} · {c.version.data.source_class === "CONVERSATION_REPLY" ? "普通对话原回复" : c.version.data.source_class === "MANUAL_CANDIDATE" ? "人工准备" : "已核验建议"}</option>)}</select>{candidate && <>{candidate.eligible ? <p className={styles.sub}>正文和来源依据仍匹配；请逐项核对。</p> : <ul className={styles.sub}>{candidate.reasons.map((reason, index) => <li key={index}>{reason}</li>)}</ul>}{candidate.version.data.source_class === "CONVERSATION_REPLY" && <p>原对话 Task 与用量来源保留；此处是接收时的版本，不表示生成时已读取该版本。</p>}<p>采用后，候选将成为完整的新正文版本；原正文版本会保留，不会发布。</p><div className={styles.compareGrid}><article><h3>候选原保存版本</h3>{candidateBasis ? <p>{candidateBasis.data.body || "原版本正文为空"}</p> : <p className={styles.sub}>候选原版本暂不可读取</p>}</article><article><h3>当前候选</h3><p>{candidate.version.data.body}</p></article></div>
      {candidate.version.data.source_class === "MANUAL_CANDIDATE" && <section className={styles.feedback}><h3>评价这份人工候选</h3><p className={styles.sub}>作者是 CEO。认可或不认可只记录评价；修改意图仍由当前作者手动处理，尚未交给员工。采用正文需另行完成下方三项检查。</p>{candidate.feedback ? <p role="status">已记录：{{ ACCEPT: "认可", REVISE: "需要人工修改", REJECT: "不认可" }[candidate.feedback.action]} · {candidate.feedback.reason}</p> : <><div className={styles.row}>{[["ACCEPT", "认可"], ["REVISE", "需要人工修改"], ["REJECT", "不认可"]].map(([action, label]) => <label key={action}><input type="radio" name={`cg-feedback-${candidate.version.entity_id}`} checked={feedbackChoice.action === action} disabled={Boolean(feedbackChoice.pending) || feedbackChoice.busy || feedbackChoice.storageBlocked} onChange={() => setFeedbackChoice((old) => ({ ...old, action, confirmed: false }))} />{label}</label>)}</div><label>评价理由<textarea value={feedbackChoice.reason} disabled={Boolean(feedbackChoice.pending) || feedbackChoice.busy || feedbackChoice.storageBlocked} onChange={(event) => setFeedbackChoice((old) => ({ ...old, reason: event.target.value, confirmed: false }))} /></label><label><input type="checkbox" checked={feedbackChoice.confirmed} disabled={feedbackChoice.busy || feedbackChoice.storageBlocked} onChange={(event) => setFeedbackChoice((old) => ({ ...old, confirmed: event.target.checked }))} />我已核对原候选、版本、理由和仅记录评价的效果</label><button disabled={busy || dirty || !candidate.eligible || !candidateBasis || candidateRef !== candidate.version.entity_id || feedbackChoice.busy || feedbackChoice.storageBlocked || !feedbackChoice.confirmed || !feedbackChoice.action || !feedbackChoice.reason.trim() || new TextEncoder().encode(feedbackChoice.reason.trim()).length > 2000} onClick={submitFeedback}>保存候选评价</button>{feedbackChoice.error && <p role="alert">{feedbackChoice.error}</p>}{feedbackChoice.notice && <p role="status">{feedbackChoice.notice}</p>}</>}{candidate.feedback?.action === "REVISE" && <p>可回到同一内容，手动准备新的候选。</p>}<Link href={contentHref(workspaceId, { content: row.content.entity_id, version: candidate.version.data.basis_version_ref, candidate: candidate.version.entity_id })}>此候选的固定入口</Link></section>}
      <div className={styles.checks}>{[["content", "我已核对内容并决定采用"], ["references", "我已核对引用与原版本依据"], ["account", "我理解尚未连接目标账号，本次只保存本地正文"]].map(([key, label]) => <label key={key}><input type="checkbox" checked={reviewedCandidate === candidate.version.entity_id && checks[key]} onChange={(e) => { setChecks((current) => ({ ...(reviewedCandidate === candidate.version.entity_id ? current : { content: false, references: false, account: false }), [key]: e.target.checked })); setReviewedCandidate(candidate.version.entity_id); }} />{label}</label>)}</div><button disabled={busy || dirty || !candidate.eligible || !cgChecksMatch(candidate.version.entity_id, reviewedCandidate, checks)} onClick={async () => { if (!cgChecksMatch(candidate.version.entity_id, reviewedCandidate, checks)) return; const result = await operate("adopt", { candidate_ref: candidate.version.entity_id, checks }); if (result && mounted.current) { setDraft(draftOf(result)); setSavedBase(result.version.entity_id); setChecks({ content: false, references: false, account: false }); setNotice("已明确采用并保存为新版本；没有发布。"); } }}>明确采用为新正文版本</button></>}</>}

    </section>}
    {notice && <p role="status" className={styles.notice}>{notice}</p>}
  </>;
}

export function LocalGrowthMedia({ company, workspaceId, row, dirty, locked, onInspect, initialAsset = "" }) {
  const content=row.content.entity_id,version=row.version.entity_id,key=`${company}:${workspaceId}:${content}:${version}`;
  const current=useRef(key);useLayoutEffect(()=>{current.current=key;return()=>{current.current="";};},[key]);
  const [data,setData]=useState(null),[selected,setSelected]=useState(""),[url,setUrl]=useState(""),[ready,setReady]=useState(false),[error,setError]=useState(""),[notice,setNotice]=useState(""),[busy,setBusy]=useState(false),[use,setUse]=useState("OUTPUT"),[confirmed,setConfirmed]=useState(false);
  const pending=useRef(false),request=useRef(null),adoption=useRef(null);
  const [fileName,setFileName]=useState("");
  const load=async()=>{const own=key,value=await api.mediaCollection(company,workspaceId,content);if(value.entry.scope.company_id!==company||value.entry.scope.workspace_id!==workspaceId)throw new Error("媒体范围不匹配。");if(current.current===own)setData(value);};
  useEffect(()=>{setData(null);setSelected(initialAsset);setReady(false);setFileName("");setError("");setNotice("");load().catch(e=>{if(current.current===key)setError(e.message);});},[key]); // eslint-disable-line react-hooks/exhaustive-deps
  const assets=data?.records.filter(v=>v.kind==="Asset")||[],candidates=data?.records.filter(v=>v.kind==="Candidate")||[];
  const asset=assets.find(v=>v.ref===selected),candidate=candidates.find(v=>v.payload.asset_ref===selected);
  useEffect(()=>{let active=true,objectUrl="";setUrl("");setReady(false);setConfirmed(false);if(asset)api.media(company,workspaceId,content,asset.ref).then(async blob=>{const raw=await blob.arrayBuffer();const hash=Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",raw)),v=>v.toString(16).padStart(2,"0")).join("");if(hash!==asset.payload.media.sha256||raw.byteLength!==asset.payload.media.size)throw new Error("媒体字节与原资产不一致。");if(active){objectUrl=URL.createObjectURL(new Blob([raw],{type:asset.payload.media.mime}));setUrl(objectUrl);}}).catch(e=>{if(active)setError(e.message);});return()=>{active=false;if(objectUrl)URL.revokeObjectURL(objectUrl);};},[company,workspaceId,content,asset]);
  const upload=async event=>{const file=event.target.files?.[0];event.target.value="";if(!file||pending.current||dirty||locked)return;setFileName(file.name);const limits={"image/png":20*1024*1024,"image/jpeg":20*1024*1024,"audio/wav":16000000,"video/mp4":128*1024*1024};const mime=file.type==="audio/x-wav"?"audio/wav":file.type;if(!limits[mime]||file.size<=0||file.size>limits[mime]){setError("请选择范围内的PNG/JPEG、PCM WAV或MP4；总媒体额最多128MiB。");return;}pending.current=true;setBusy(true);setError("");const own=key;
    try{const raw=await file.arrayBuffer(),sha=Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",raw)),v=>v.toString(16).padStart(2,"0")).join("");if(current.current!==own)throw new Error("内容已切换，没有导入文件。");const value={title:file.name.slice(0,240),size:raw.byteLength,sha256:sha,mime,use};const storage=`curis.cg.media-import.${company}:${workspaceId}:${content}`;try{request.current=JSON.parse(sessionStorage.getItem(storage)||"null");}catch{}request.current=stableRequest(request.current,"import-media",version,value,()=>crypto.randomUUID());localStorage.setItem(storage,JSON.stringify(request.current));const output=await api.importMedia(company,workspaceId,content,{request_id:request.current.request_id,expected_version_ref:version,data:value},raw);if(current.current!==own)return;await load();if(current.current!==own)return;setSelected(output.asset.ref);setNotice("已保存本机原文件；请实际预览后决定是否采用。未发布，商业权利未核验。");sessionStorage.removeItem(storage);request.current=null;}catch(e){if(current.current===own)setError(e.message+" 原文件/请求保留，重选同文件可查询同请求，不会自动改用新依据。");}finally{pending.current=false;setBusy(false);event.target.value="";}};
  const adopt=async()=>{if(!candidate||!ready||!confirmed||pending.current||dirty||locked)return;const own=key;pending.current=true;setBusy(true);setError("");try{const payload={candidate_ref:candidate.ref,confirmed:true,rights_confirmed:true};adoption.current=stableRequest(adoption.current,"adopt-media",candidate.ref,payload,()=>crypto.randomUUID());await api.adoptMedia(company,workspaceId,content,{request_id:adoption.current.request_id,expected_ref:"",data:payload});if(current.current!==own)return;await load();if(current.current!==own)return;setNotice("已明确采用这份本地媒体候选；脚本与成片分别保留，没有发布。");}catch(e){if(current.current===own)setError(e.message);}finally{pending.current=false;if(current.current)setBusy(false);}};
  return <section className={styles.localMedia}><header className={styles.sectionHeader}><h2>{row.content.data.format==="graphic"?"图文素材与实际预览":"本机媒体与候选预览"}</h2><span>脚本采用与媒体采用分别记录</span></header><p className={styles.sub}>用户本机文件 · 仅本地使用 · 商业权利未验证；没有生成、转码或外部上传。</p>{error&&<p role="alert" className={styles.error}>{error}</p>}{notice&&<p role="status">{notice}</p>}
    <div className={styles.actions}><label>本次用途<select value={use} onChange={e=>setUse(e.target.value)}><option value="OUTPUT">作为当前形态候选</option><option value="REFERENCE">仅作参考素材</option></select></label><label className={styles.filePicker}><span>选择本机文件</span><input className={styles.fileInput} aria-label="导入本机内容媒体" type="file" accept="image/png,image/jpeg,audio/wav,video/mp4" disabled={busy||dirty||locked||!data?.configured} onChange={upload}/></label><span className={styles.fileName} role="status">{fileName ? `上次选择：${fileName}` : "尚未选择文件"}</span>{!data?.configured&&<p>当前媒体存储尚未配置，脚本编辑仍可继续。</p>}</div>
    <div className={styles.mediaItems}>{assets.map(value=><button key={value.ref} aria-pressed={selected===value.ref} onClick={()=>{setSelected(value.ref);window.history.replaceState(null,"",contentHref(workspaceId,{content,version,media:value.ref}));}}><strong>{value.payload.title}</strong><small>{value.payload.media.mime} · {value.payload.media.size.toLocaleString()} bytes · {value.payload.use==="OUTPUT"?"候选":"参考"}</small></button>)}</div>
    {data&&selected&&!asset&&<p role="alert">原媒体不存在于当前内容，保留原定位；请明确重新选择。</p>}{asset&&<div className={styles.mediaPreview}><h3>{asset.payload.title}</h3>{url&&(asset.payload.media.mime.startsWith("image/")?<img src={url} alt={asset.payload.title} onLoad={event=>setReady(event.target.naturalWidth>0)} onError={()=>{setReady(false);setError("图片未能解码，不能确认采用。");}}/>:asset.payload.media.mime.startsWith("audio/")?<audio src={url} controls onCanPlay={()=>setReady(true)} onError={()=>{setReady(false);setError("音频未能播放，不能确认采用。");}}/>:<video src={url} controls onCanPlay={()=>setReady(true)} onError={()=>{setReady(false);setError("此MP4编码未能在当前设备播放；文件保留，不能确认采用。");}}/>)}<p>{ready?"当前设备已解码，可实际核对预览":"等待实际解码，尚未具备预览证据"}</p><button onClick={()=>onInspect?.({id:`media:${asset.ref}`,title:asset.payload.title,request:asset.ref,content:<section className={`${styles.main} ${styles.utility}`}><h2>{asset.payload.title}</h2><p>固定原文件摘要 {asset.payload.media.sha256}</p><p>仅本地使用 · 权利未验证</p><Link href={contentHref(workspaceId,{content,version:asset.payload.version_ref,media:asset.ref})}>回到原内容版本与媒体</Link></section>})}>查看原资产依据</button>{candidate&&<><p>{candidate.eligible?"原正文与方向仍匹配":"原正文或方向已变化；原候选保留，不能按新依据采用"}</p><label><input type="checkbox" checked={confirmed} onChange={e=>setConfirmed(e.target.checked)}/>我已实际预览、核对原脚本和本地用途，明确采用这份候选</label><button className={styles.primary} disabled={!candidate.eligible||!confirmed||!ready||busy||dirty||locked} onClick={adopt}>明确采用本地媒体版本</button></>}</div>}
    {data?.records.filter(v=>v.kind==="Adoption").map(v=><p key={v.ref}>已保存人工媒体采用记录 · 原候选 {v.payload.candidate_ref} · 未发布</p>)}
  </section>;
}
