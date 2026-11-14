"use client";
import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import EmployeeConversation from "../v1/EmployeeConversation.js";
import { ConversationComposer, useConversationModel } from "../v1/SharedConversation.js";
import { EmployeeAvatar } from "../v1/EmployeeAvatar.js";
import { writingApi, writingRequestLocked, writingRepairHref } from "../../lib/writingApi.js";
import { chapterHref, currentInspection, sameChapter, selectionFor, writingSessionKey, WRITING_CHECKS, writingCandidates, candidateOutcome, formalVersions, continuationSources, continuationSource, continuationWorkPayload } from "../../lib/writingState.mjs";
import { writingBookHref, BOOK_KINDS } from "../../lib/writingBookState.mjs";
import { createAssignedWork, getAssignedAgentWorkflow, publishAssignedAgentWorkflow } from "../../lib/v1FrontendApi.js";
import styles from "./Writing.module.css";

export default function WritingChapterMain({ state, entry, workspaceId, company, command, busy, onNavigate, entryMetadata, onRefresh, onDetails, onExecutionLock, requestLocked }) {
  const key = writingSessionKey(state.scope); const editor = useRef(null); const initialized = useRef(false);
  const [text, setText] = useState(state.draft.text); const [message, setMessage] = useState("");
  const [discussionOpen, setDiscussionOpen] = useState(Boolean(state.direct)); const [selection, setSelection] = useState(null);
  const [checks, setChecks] = useState([]); const [note, setNote] = useState(""); const [error, setError] = useState("");
  const [formalConsent, setFormalConsent] = useState(false);
  const [conversation, setConversation] = useState(null); const [request, setRequest] = useState(null);
  const [hydrated, setHydrated] = useState(false);
  const [fontSize, setFontSize] = useState("16");
  const [workReview, setWorkReview] = useState(null);
  const [basisOpen, setBasisOpen] = useState(false), [basisIds, setBasisIds] = useState([]);
  const [manualOpen, setManualOpen] = useState(false), [replacement, setReplacement] = useState("");
  const model = useConversationModel(key, { models: entryMetadata?.models || [], selected: entryMetadata?.selected_model, preference: entryMetadata?.model_preference,
    onChoose: async (modelKey) => { if (requestLocked || writingRequestLocked(request?.status)) throw new Error("原请求待核验，请先查询。"); const result = await writingApi.selectModel(company, workspaceId, modelKey); await onRefresh(); return result; } });
  const [editBase, setEditBase] = useState(state.draft.ref);
  const sending = useRef(false); const [sendBusy, setSendBusy] = useState(false);
  const previousHead = useRef(state.draft.ref); const savedText = useRef(state.draft.text);
  const actionPending = useRef(""); const [actionBusy, setActionBusy] = useState("");
  const [resultMessage, setResultMessage] = useState("");
  const [panel, setPanel] = useState(null); const [panelValue, setPanelValue] = useState("");
  const [continuationOpen, setContinuationOpen] = useState(false);
  const [sourceRef, setSourceRef] = useState(""); const [continuationText, setContinuationText] = useState("");
  useEffect(() => {
    if (initialized.current) return;
    try { const value = JSON.parse(localStorage.getItem(key) || sessionStorage.getItem(key) || "null"); if (value) { setText(value.text ?? state.draft.text); setMessage(value.message || ""); setEditBase(value.baseRef || state.draft.ref); setSelection(value.selection || null); setRequest(value.request || null); setDiscussionOpen(Boolean(state.direct || value.discussionOpen)); setChecks((Array.isArray(value.checks) ? value.checks : []).filter((check) => WRITING_CHECKS.includes(check))); setNote(value.note || ""); } } catch {}
    initialized.current = true;
    setHydrated(true);
  }, [key]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    // A route may mount this component briefly before its scope read finishes.
    // Never replace the retained input with first-render defaults before hydration.
    if (hydrated) { try { localStorage.setItem(key, JSON.stringify({ text, message, baseRef: editBase, selection, request, discussionOpen, checks, note })); } catch {} }
  }, [key, text, message, editBase, selection, request, discussionOpen, checks, note, hydrated]);
  useEffect(() => {
    if (state.draft.ref !== previousHead.current) {
      // A remote head never overwrites dirty input. Own successful save/adoption sets it explicitly.
      if (text === savedText.current) { setText(state.draft.text); setEditBase(state.draft.ref); }
      previousHead.current = state.draft.ref; savedText.current = state.draft.text;
      setSelection(null); setChecks([]);
      setFormalConsent(false);
    }
  }, [state.draft.ref, state.draft.text, text]);
  useEffect(() => {
    if (!entry.anchor || !editor.current) return;
    const prefix = state.draft.ref + ":";
    if (!entry.anchor.startsWith(prefix)) return;
    const [start, end] = entry.anchor.slice(prefix.length).split(":").map(Number);
    try { setSelection(selectionFor(state.draft, text, start, end)); editor.current.focus(); editor.current.setSelectionRange(start, end); } catch {}
  }, [entry.anchor, state.draft.ref]); // eslint-disable-line react-hooks/exhaustive-deps
  const dirty = text !== state.draft.text;
  const inspection = currentInspection(state);
  const reviewedAdoption = inspection && state.events.find(e => e.action === "candidate.adopted"
    && e.draft?.ref === state.draft.ref && e.work_ref && e.acceptance_ref);
  const candidates = writingCandidates(state.events);
  const binding = [...state.events].reverse().find((e) => e.action === "discussion.bound" && e.draft_ref === state.draft.ref && e.discussion_scope?.object_ref === entry.chapter);
  const run = async (action, data, base) => { try { setError(""); return await command(action, data, undefined, base); } catch (reason) { setError(reason.message); return null; } };
  const sourceOptions = continuationSources(state.events);
  const chosenSource = continuationSource(state.events, sourceRef);
  const assignmentRef = binding?.assignment_ref || entryMetadata?.assignment_ref;
  const fullSelection = () => state.draft.text
    ? selectionFor(state.draft, state.draft.text, 0, state.draft.text.length)
    : state.direct ? { draft_ref: state.draft.ref, sha256: state.draft.sha256, start: 0, end: 0,
        excerpt: "", anchor: `${state.draft.ref}:0:0`, knowledge: state.draft.knowledge } : null;
  const workSelection = (candidate) => [candidate?.selection, selection, binding?.selection]
    .find((item) => item?.draft_ref === state.draft.ref) || fullSelection();
  const createWorkAvailable = typeof createAssignedWork === "function" && Boolean(model.selected && assignmentRef && workSelection(null) && !dirty && !state.read_only && !requestLocked && !writingRequestLocked(request?.status) && request?.phase !== "WORK_READY");
  const stageContinuation = async (workPayload) => {
    const bound = binding?.selection?.anchor === workPayload.source.selection.anchor
      ? binding : await command("discussion.start", { selection: workPayload.source.selection });
    const next = {
      payload: { binding_ref: bound.ref, body: workPayload.problem, request_id: workPayload.request_id, model_key: workPayload.model_key },
      binding_ref: bound.ref, assignment_ref: assignmentRef, work_payload: workPayload, work_mode: true,
      status: "UNKNOWN", phase: "WORK_CREATE",
    };
    localStorage.setItem(key, JSON.stringify({ text, message: workPayload.problem, baseRef: editBase, selection, request: next, discussionOpen: true, checks, note }));
    setRequest(next); setMessage(workPayload.problem); setDiscussionOpen(true); onExecutionLock(true);
    const result = await createAssignedWork(assignmentRef, workPayload);
    if (!result?.work?.entity_id) throw new Error("未确认交办创建，请查询原请求。");
    const ready = { ...next, payload: { ...next.payload, work_ref: result.work.entity_id }, status: "FAILED", phase: "WORK_READY" };
    localStorage.setItem(key, JSON.stringify({ text, message: workPayload.problem, baseRef: editBase, selection, request: ready, discussionOpen: true, checks, note }));
    setRequest(ready); onExecutionLock(false);
    return result;
  };
  const submitPanel = async (candidate) => {
    if (!panel || panel.ref !== candidate.ref || actionPending.current || candidateOutcome(state.events, candidate.ref).status !== "PENDING") return;
    actionPending.current = candidate.ref; setActionBusy(candidate.ref); setError("");
    try {
      if (panel.kind === "reject") {
        const output = await run("candidate.rejected", { candidate_ref: candidate.ref, reason: panelValue });
        if (output) { setPanel(null); setPanelValue(""); setResultMessage("已拒绝；原稿与来源仍保留，可继续查看。"); }
        return;
      }
      if (!createWorkAvailable) { setError("请先配置可用模型并选择当前正文范围，再确认提交。"); return; }
      const payload = continuationWorkPayload({ scope: state.scope, draft: state.draft, selection: workSelection(candidate),
        modelKey: model.selected.model_key, source: { source_ref: candidate.ref, source_class: "CANDIDATE", label: "基于候选稿" },
        requirements: panelValue, requestId: crypto.randomUUID(), mode: "REVISE" });
      if (!payload) { setError("请填写修改意见并确认后再提交。"); return; }
      const result = await stageContinuation(payload);
      if (result?.work) { setPanel(null); setPanelValue(""); setResultMessage("已创建关联修改工作；尚未调用模型，结果仍需人工采用。"); }
      else setError("未创建工作；请核对后重试。");
    } catch (reason) { setError(reason.message); }
    finally { actionPending.current = ""; setActionBusy(""); }
  };
  const submitContinuation = async () => {
    if (actionPending.current || !chosenSource || !continuationText.trim() || !createWorkAvailable) return;
    const payload = continuationWorkPayload({ scope: state.scope, draft: state.draft, selection: workSelection(null),
      modelKey: model.selected.model_key, source: chosenSource, requirements: continuationText, requestId: crypto.randomUUID(), mode: "CONTINUE" });
    if (!payload) { setError("请填写修改要求并确认后再续做。"); return; }
    actionPending.current = "continuation"; setActionBusy("continuation");
    try {
      const result = await stageContinuation(payload);
      if (result?.work) { setContinuationOpen(false); setContinuationText(""); setSourceRef(""); setResultMessage(`已创建续做工作；来源：${chosenSource.label}，结果仍需人工采用。`); }
      else setError("未创建工作；请核对后重试。");
    } catch (reason) { setError(reason.message); }
    finally { actionPending.current = ""; setActionBusy(""); }
  };
  const continuationDisabledReason = actionBusy === "continuation" ? "正在创建，请稍候。"
    : !continuationText.trim() ? "请填写修改要求。"
    : !model.selected ? "请先配置可用模型；输入会保留。"
    : !assignmentRef || !workSelection(null) ? "请先确认当前正文和负责员工。"
    : !createWorkAvailable ? "请先保存正文或完成原交办。" : "";
  const save = async () => { const output = await run("draft.saved", { text, knowledge: state.draft.knowledge }, editBase); if (output) { savedText.current = output.draft.text; previousHead.current = output.draft.ref; setText(output.draft.text); setEditBase(output.draft.ref); setSelection(null); setChecks([]); } };
  const select = () => {
    try { const value = selectionFor(state.draft, text, editor.current.selectionStart, editor.current.selectionEnd); setSelection(value); setError(""); onNavigate({ anchor: value.anchor, draft: value.draft_ref }); }
    catch (reason) { setError(reason.message); }
  };
  const receiveDirectResult = async (current, attempt, bindingRef) => {
    if (!state.direct || attempt?.status !== "COMPLETED" || attempt.effect_status === "UNKNOWN") return;
    const reply = current.messages.find((item) => item.sender.kind === "EMPLOYEE"
      && item.provenance?.execution_selection?.work_ref
      && item.task_ref === attempt.task_ref);
    if (!reply || !reply.body || state.events.some((item) => item.action === "candidate.recorded" && item.message_ref === reply.message_id)) return;
    const original = state.events.find((item) => item.action === "discussion.bound" && item.ref === bindingRef);
    if (original && original.draft_ref !== state.draft.ref) return;
    await command("candidate.recorded", { binding_ref: bindingRef, message_ref: reply.message_id,
      reply_start: 0, reply_end: reply.body.length, reply_excerpt: reply.body }, `direct-result:${reply.message_id}`);
  };
  const readDiscussion = async () => {
    const originalBinding = request?.binding_ref || binding?.ref || (state.direct && [...state.events].reverse().find((event) => event.action === "discussion.bound")?.ref);
    if (!originalBinding) return;
    try {
      if (request?.work_payload && !request.payload.work_ref) {
        const result = await createAssignedWork(request.assignment_ref, request.work_payload);
        setRequest({ ...request, payload: { ...request.payload, work_ref: result.work.entity_id }, status: "FAILED", phase: "WORK_READY" });
        onExecutionLock(false); setError("原交办已核对。点击继续原交办才会发送，不会自动调用模型。");
        return;
      }
      const current = await writingApi.discussion(company, workspaceId, entry, originalBinding); setConversation(current);
      const originalMessage = request?.payload?.request_id ? current.messages.find((m) => m.sender.kind === "CEO" && m.idempotency_key === request.payload.request_id) : null;
      const attempt = request ? current.attempts.filter((a) => a.message_id === (request.message_id || originalMessage?.message_id) || a.attempt_id === request.attempt_id).at(-1) : current.attempts.filter((a) => a.execution_selection?.purpose === "WRITING_CHAPTER_REPLY" && a.execution_selection?.scope?.chapter_ref === entry.chapter).at(-1);
      if (attempt) {
        const status = attempt.effect_status === "UNKNOWN" ? "UNKNOWN" : attempt.status;
        setRequest((old) => ({ ...(old || {}), binding_ref: originalBinding, attempt_id: attempt.attempt_id, message_id: attempt.message_id, safeRetry: attempt.status === "FAILED" && attempt.effect_status === "SETTLED" && !attempt.task_ref, status }));
        onExecutionLock(writingRequestLocked(status));
        await receiveDirectResult(current, attempt, originalBinding);
      }
      await onRefresh();
    } catch (reason) { setError(reason.message); }
  };
  const recovered = useRef(false);
  useEffect(() => {
    if (!hydrated || recovered.current) return;
    recovered.current = true;
    if (state.direct && (!request || request.payload?.work_ref) && request?.phase !== "WORK_READY") {
      void readDiscussion();
    }
  }, [hydrated]); // eslint-disable-line react-hooks/exhaustive-deps
  const send = async (event, retry = false, workMode = false, reviewRef = null) => {
    event.preventDefault();
    if (sending.current || requestLocked || writingRequestLocked(request?.status) || dirty || state.read_only) return;
    if ((!binding && !state.direct && !retry) || state.responsibility.status !== "AVAILABLE" || !model.selected) { setError(state.responsibility.reason || "请先核对责任员工和可用模型。"); return; }
    if (retry && (request?.status !== "FAILED" || !request.payload || (request.phase !== "WORK_READY" && request.payload.work_ref && !request.safeRetry))) return;
    const payload = retry ? { ...request.payload, retry_no: request.phase === "WORK_READY" || !request.attempt_id ? 0 : 1 } : { binding_ref: binding?.ref, body: message, request_id: crypto.randomUUID(), model_key: model.selected.model_key };
    let retained = { payload, binding_ref: payload.binding_ref, status: "RUNNING", work_mode: workMode || Boolean(payload.work_ref) };
    let creationStarted = false, sendStarted = false;
    sending.current = true; setSendBusy(true); onExecutionLock(true);
    try {
      const savedModel = entryMetadata?.selected_model?.model;
      if (state.direct && !retry && (savedModel?.model_key !== payload.model_key
          || savedModel.source !== model.selected.source || savedModel.updated_at !== model.selected.updated_at)) {
        const prepared = await writingApi.selectModel(company, workspaceId, payload.model_key);
        if (prepared.execution?.status !== "AVAILABLE") {
          throw new Error(prepared.execution?.reason || "当前写作模型尚未获得执行许可。");
        }
        await onRefresh();
      }
      let activeBinding = binding;
      if (state.direct && !retry && !activeBinding) {
        activeBinding = await command("discussion.start", { selection: fullSelection() });
        payload.binding_ref = activeBinding.ref;
        retained = { ...retained, binding_ref: activeBinding.ref };
      }
      if (workMode && !retry) {
        const assignment = activeBinding.assignment_ref || entryMetadata?.assignment_ref;
        const review = await getAssignedAgentWorkflow(assignment, company, workspaceId);
        if (review.state !== "READY") {
          if (review.state === "NEEDS_PUBLICATION" && review.publication_allowed) {
            setWorkReview({ ...review, assignment }); onExecutionLock(false); return;
          }
          throw new Error(review.reason || "原责任流程尚不能创建交办。");
        }
        const workPayload = { problem: payload.body, expected_result: "原章节选文的可采用正文候选；执行不等于采用",
          request_id: payload.request_id, model_key: payload.model_key,
          source: { kind: "writing", book_ref: state.scope.book_ref, chapter_ref: state.scope.chapter_ref,
            expected_draft_ref: state.draft.ref, selection: activeBinding.selection,
            ...(reviewRef ? { review_ref: reviewRef } : {}) } };
        retained = { ...retained, assignment_ref: assignment, work_payload: workPayload, phase: "WORK_CREATE" };
        setRequest(retained);
        // Persist the original creation identity before a response can be lost.
        try { localStorage.setItem(key, JSON.stringify({ text, message, baseRef: editBase, selection, request: retained, discussionOpen: true, checks, note })); }
        catch { throw new Error("无法保存原交办标识；没有创建工作或发送模型请求。"); }
        creationStarted = true;
        const result = await createAssignedWork(assignment, workPayload);
        payload.work_ref = result.work.entity_id;
        retained = { ...retained, payload: { ...payload }, phase: "WORK_READY" };
        if (reviewRef) {
          setRequest({ ...retained, status: "FAILED" }); onExecutionLock(false);
          setError("基于复盘的新工作已创建，尚未发送；核对后点击继续原交办才会调用模型。");
          await onRefresh(); return;
        }
      }
      setRequest(retained);
      if (payload.work_ref) {
        retained = { ...retained, phase: "WORK_SUBMITTED" };
        localStorage.setItem(key, JSON.stringify({ text, message, baseRef: editBase, selection, request: retained, discussionOpen: true, checks, note }));
      }
      sendStarted = true;
      const result = await writingApi.send(company, workspaceId, entry, payload);
      setRequest({ ...retained, payload, binding_ref: payload.binding_ref, attempt_id: result.attempt.attempt_id, message_id: result.attempt.message_id, status: result.attempt.status });
      const current = await writingApi.discussion(company, workspaceId, entry, payload.binding_ref); setConversation(current);
      const attempt = current.attempts.find((a) => a.attempt_id === result.attempt.attempt_id);
      if (attempt) { const status = attempt.effect_status === "UNKNOWN" ? "UNKNOWN" : attempt.status; setRequest((old) => ({ ...old, status, safeRetry: attempt.status === "FAILED" && attempt.effect_status === "SETTLED" && !attempt.task_ref })); onExecutionLock(writingRequestLocked(status)); }
      try { await receiveDirectResult(current, attempt, payload.binding_ref); }
      catch (reason) { setError(reason.message); }
      await onRefresh();
    } catch (reason) {
      const status = (!creationStarted && !sendStarted) || (reason.status && reason.status < 500) ? "FAILED" : "UNKNOWN";
      setRequest({ ...retained, payload, binding_ref: payload.binding_ref, status }); onExecutionLock(writingRequestLocked(status)); setError(reason.message);
    } finally { sending.current = false; setSendBusy(false); }
  };
  const visibleBody = (m) => { if (m.sender.kind === "CEO") { try { return JSON.parse(m.body).author_message || m.body; } catch {} } return m.body; };
  const lock = requestLocked || writingRequestLocked(request?.status);
  const basisDisabledReason = lock ? "原请求待核验，请先查询结果。"
    : busy ? "正在处理，请稍后再绑定。"
    : state.read_only ? "当前章节只读，暂不能绑定。"
    : state.draft.ref === "ABSENT" ? "请先保存本章正文草稿；作品计划已保存不代表正文已有保存版本。"
    : dirty ? "正文有未保存修改，请先保存草稿再绑定。"
    : !state.book_context?.record ? "作品计划尚无保存版本，请先保存作品计划。"
    : !state.book_context.context.items.length ? "已保存作品计划中没有可选条目，请先补充并保存。"
    : !basisIds.length ? "请选择要绑定的作品结构条目。" : "";
  const modelControls = <>{model.models.length > 0 && <><label>会话模型<select aria-label="章节会话模型" disabled={lock || sendBusy || busy} value={model.selected?.model_key || ""} onChange={async (e) => { if (lock || sending.current) return; const chosen = model.models.find((m) => m.model_key === e.target.value); if (chosen) try { await model.choose(chosen); } catch (reason) { setError(reason.message); } }}><option value="">请选择可用模型</option>{model.models.map((m) => <option key={`${m.source}:${m.model_key}`} value={m.model_key}>{m.display_name || m.model_name}</option>)}</select></label></>}<Link href={writingRepairHref("/ceo-office/capabilities", chapterHref(workspaceId, entry))} aria-label="配置模型，保留当前章节">配置模型</Link></>;
  const employeeName = entryMetadata?.employee_name || state.responsibility.employee_name;
  const identityHref = (() => {
    const ref = entryMetadata?.company_employee_ref, name = entryMetadata?.employee_name;
    const scope = entryMetadata?.scope;
    if (typeof ref !== "string" || !ref.trim() || ref !== ref.trim() || ref === "." || ref === ".." || typeof name !== "string" || !name.trim()
      || !scope?.tenant_id || scope.tenant_id !== state.scope?.tenant_id || scope.company_id !== company || scope.workspace_id !== workspaceId
      || !sameChapter(state.scope, company, workspaceId, entry)) return null;
    try { return writingRepairHref(`/ceo-office/organization/employees/${encodeURIComponent(ref)}`, chapterHref(workspaceId, entry)); } catch { return null; }
  })();
  const characters = Array.from(text.replace(/\s/gu, "")).length;
  return <div className={styles.chapter}>
    <nav className={styles.tabs} aria-label="章节工作"><button aria-current={entry.mode === "chapter" ? "page" : undefined} onClick={() => onNavigate({ mode: "chapter" })}>章节正文</button><button aria-current={entry.mode === "review" ? "page" : undefined} onClick={() => onNavigate({ mode: "review" })}>作者检查</button><button onClick={() => onNavigate({ mode: "package", formal: "", package: "" })}>正式稿与发布包</button></nav>
    <section className={styles.chapterBasisSummary} aria-label="本章目标与交接">
      <div><h3>本章目标</h3><p>{state.draft.book_context_basis?.items.filter(v=>["chapter","node"].includes(v.kind)).map(v=>v.goal || v.title).join(" → ") || "尚未绑定本章故事目标，可先写正文。"}</p></div>
      <div><h3>上一章交接</h3><p>{state.draft.book_context_basis?.items.find(v=>v.kind==="chapter")?.handoff || "原依据尚无作者交接说明"}</p></div>
    </section>
    <section className={styles.chapterBasisStrip} aria-label="本章结构与原版本依据">
      <div><p><strong>结构路径：</strong>{state.draft.book_context_basis?.items.filter(v=>["outline","volume","chapter","node"].includes(v.kind)).map(v=>v.title).join(" / ") || "本章尚未绑定结构路径"}</p><p><strong>原版本依据：</strong>{state.book_context_status?.reason || "尚未绑定作品结构依据。"}</p></div>
      <div className={styles.chapterBasisActions}><Link href={writingBookHref(workspaceId, entry.book)}>查看作品大纲、设定与人物 →</Link><button onClick={()=>setBasisOpen(v=>!v)}>明确选择 / 重绑本章依据</button></div>
    </section>
    {basisOpen && <section className={styles.bookItemForm}><h3>选择当前作品结构条目</h3><p>只绑定已保存版本，不改正文；重新绑定后须重新检查正式稿。</p>{state.book_context?.context.items.map(item=><label className={styles.check} key={item.id}><input type="checkbox" checked={basisIds.includes(item.id)} onChange={e=>setBasisIds(e.target.checked?[...basisIds,item.id]:basisIds.filter(v=>v!==item.id))} />{item.title} · {BOOK_KINDS[item.kind] || "未知类型"}</label>)}<p id="writing-basis-disabled" role="status">{basisDisabledReason || "将绑定这些条目的已保存原版本；正文保持原样。"}</p><button aria-describedby="writing-basis-disabled" disabled={Boolean(basisDisabledReason)} onClick={async()=>{const value=await run("context.bound",{context_ref:state.book_context.record.ref,item_ids:basisIds,confirmed:true});if(value){setChecks([]);setFormalConsent(false);setBasisOpen(false);}}}>确认绑定原版本依据</button><button onClick={()=>setBasisOpen(false)}>取消，保留选择</button></section>}
    {entry.draft && entry.draft !== state.draft.ref && <p role="status">来源链接指向历史正文版本。当前编辑区显示最新草稿；历史快照保留在下方版本记录。</p>}
    <div className={styles.employeeBar} aria-label="当前章节负责员工">
      {identityHref ? <Link href={identityHref} className="inline-flex items-center gap-2" aria-label={`查看${entryMetadata.employee_name}的员工详情`}><EmployeeAvatar employee={{ id: entryMetadata.company_employee_ref, name: entryMetadata.employee_name }} className="h-7 w-7" /><strong>{entryMetadata.employee_name}</strong></Link> : <><EmployeeAvatar employee={{ id: entryMetadata?.company_employee_ref, name: employeeName || "负责员工待明确" }} className="h-7 w-7" /><strong>{employeeName || "负责员工待明确"}</strong></>}<span>本章正文与修改</span>
      <button onClick={() => onDetails?.("responsibility")}>当前责任</button>
      <button aria-expanded={discussionOpen} onClick={() => { setDiscussionOpen(!discussionOpen); if (!discussionOpen) readDiscussion(); }}>{discussionOpen ? "收起章节讨论" : "展开章节讨论"}</button>

    </div>
    {error && <p className={styles.error} role="alert">{error}</p>}
    {resultMessage && <p className={styles.notice} role="status">{resultMessage}</p>}
    {editBase !== state.draft.ref && <aside role="alert" className={styles.source}><p>正文已被其他编辑更新。保留输入仍基于旧版本，保存将拒绝覆盖。请核对最新版本后再决定。</p><button onClick={() => setEditBase(state.draft.ref)}>已核对，保留输入并以最新版本为基础</button></aside>}
    <section hidden={!discussionOpen && !state.direct} className={styles.discussion} aria-label="章节讨论">
      {!state.direct && identityHref && entryMetadata?.employee_ref && <EmployeeConversation key={`${company}:${workspaceId}:${entry.chapter}:${entryMetadata.employee_ref}`} companyId={company} employee={{ employee_ref: entryMetadata.employee_ref, id: entryMetadata.company_employee_ref, name: employeeName }} active={discussionOpen} blocked={Boolean(lock || busy)} embedded={{ workspaceId, contextKey: `chapter:${entry.book}:${entry.chapter}`, objectRef: entry.chapter, assignmentRef: entryMetadata.assignment_ref, title: "章节讨论", receiveReady: !dirty && !state.read_only, onAgentCandidate: onRefresh, onReload: onRefresh, agentSourceReady: Boolean(!dirty && !state.read_only && selection?.draft_ref === state.draft.ref && selection?.sha256 === state.draft.sha256), agentSource: { kind: "writing", book_ref: entry.book, chapter_ref: entry.chapter, expected_draft_ref: state.draft.ref, selection } }} businessReturn={{ href: chapterHref(workspaceId, entry), kind: "writing" }} />}
      <details open={state.direct || undefined}><summary>{state.direct ? "交办写作与查看结果" : "针对已保存选文请求修改建议"}</summary>
      {(selection || binding) && <div className={styles.discussionActions}>
        {selection && <button disabled={dirty || busy || state.responsibility.status !== "AVAILABLE"} onClick={async () => { const result = await run("discussion.start", { selection }); if (result) setConversation(null); }}>绑定当前选文讨论</button>}
        {binding && <button onClick={readDiscussion}>读取讨论进展</button>}
      </div>}
      <button type="button" disabled={lock || dirty || busy || sendBusy || (!binding && !state.direct) || !model.selected || !message.trim() || state.responsibility.status !== "AVAILABLE" || request?.phase === "WORK_READY"}
        onClick={e => send(e, false, true)}>{state.direct ? "交办写作" : "明确交办本次修改"}</button>
      {reviewedAdoption && <><p>可基于当前作者复盘创建下一次工作；需重新绑定当前选文，并核验当前员工、模型与授权。</p><p>已保存复盘：{inspection.note || "未填写备注"}</p>
        <button type="button" disabled={lock || dirty || busy || sendBusy || !binding || !model.selected || !message.trim() || state.responsibility.status !== "AVAILABLE" || request?.phase === "WORK_READY"}
          onClick={e => send(e, false, true, inspection.ref)}>基于当前复盘创建新工作（不发送）</button></>}
      {workReview && <section aria-label="核对本次交办责任"><p>{workReview.reason} 只发布当前章节作者责任，正文仍须您明确采用。</p>
        <button type="button" disabled={busy || sendBusy} onClick={async () => { try {
          await publishAssignedAgentWorkflow(workReview.assignment, { company_id: company, workspace_id: workspaceId,
            expected_revision: workReview.assignment_revision, review_token: workReview.review_token, confirm: true });
          setWorkReview(null); setError("责任已确认，请点击明确交办本次修改继续。尚未调用模型。");
        } catch (reason) { setError(reason.message); } }}>确认发布当前责任</button>
        <button type="button" onClick={() => setWorkReview(null)}>取消，保留输入</button></section>}
      {request?.phase === "WORK_READY" && request.status === "FAILED" && <button type="button" disabled={busy || sendBusy || lock}
        onClick={e => send(e, true, true)}>继续原交办</button>}
      {request?.payload?.work_ref && <p>原交办已保留；模型回复不等于正文已采用。</p>}
      <ConversationComposer className={styles.discussionComposer} inputClassName={styles.discussionInput} actionsClassName={styles.discussionActions} value={message} onChange={setMessage} onSubmit={(event) => send(event, false, Boolean(state.direct))} placeholder={state.direct ? "告诉作者你想写什么…" : "说说你想调整哪一段…"} inputAriaLabel="章节讨论输入" submitLabel="发送给负责员工" disabled={(!binding && !state.direct) || state.responsibility.status !== "AVAILABLE" || dirty || busy || !model.selected || request?.phase === "WORK_READY"} busy={busy || sendBusy} maxLength={8000} showVoice={false} access={{ state: "MODEL_EXECUTOR_NOT_APPLICABLE" }} controls={modelControls} referenceControl={<span className={styles.discussionReference}>{binding ? "讨论依据已绑定" : selection ? "当前选文已定位" : "尚未选择正文"}</span>} notice={request?.phase === "WORK_READY" ? "新工作尚未发送，请核对后点击继续原交办。" : !model.models.length ? "暂无可用模型；输入会保留。" : state.responsibility.status !== "AVAILABLE" ? "员工执行不可用；输入会保留。" : "仅讨论；回复不等于业务结果。"} />
    {(request || conversation?.messages.length) && <section className={styles.section} aria-label="章节讨论结果"><h2>章节讨论结果</h2>{request && <p role="status">{request.phase === "WORK_READY" ? "新工作已创建，尚未发送" : request.status === "CANCELLED" ? "原请求已取消" : request.status === "RUNNING" ? "原请求正在处理" : writingRequestLocked(request.status) ? "原请求结果待核验；不会重发或换责任员工" : request.status === "FAILED" ? "原请求未完成，输入保留" : "原请求已完成"}</p>}<button onClick={readDiscussion}>查询原请求结果</button>{request?.status === "FAILED" && request.payload && <button disabled={busy || lock || dirty || request.payload.retry_no === 1 || (Boolean(request.payload.work_ref) && !request.safeRetry) || request.phase === "WORK_READY" || state.responsibility.status !== "AVAILABLE"} onClick={(e) => send(e, true)}>明确重试原失败请求</button>}{conversation?.messages.filter((m) => m.provenance?.execution_selection?.purpose === "WRITING_CHAPTER_REPLY").map((m) => <article key={m.message_id}><b>{m.sender.kind === "CEO" ? "作者" : m.provenance?.source_class === "PROVIDER_EXECUTOR" ? "员工回复 · 已验证模型来源" : "员工回复 · 受控验证来源"}</b><p>{visibleBody(m)}</p>{m.sender.kind === "EMPLOYEE" && <><p>回复基于原选文；正文或责任已变化时，先核对来源，不能直接采用。</p><button disabled={dirty || busy || !binding} onClick={() => run("candidate.recorded", { binding_ref: request?.binding_ref || binding.ref, message_ref: m.message_id, reply_start: 0, reply_end: m.body.length, reply_excerpt: m.body })}>记录为修改建议</button><details><summary>查看原请求依据与来源</summary><pre>{JSON.stringify({ context: m.context, task_ref: m.task_ref, provenance: m.provenance }, null, 2)}</pre></details></>}</article>)}</section>}
    </details></section>
    {entry.mode !== "review" && <div className={styles.editorFrame}>
      <div className={styles.editorState}><span className={styles.badge}>当前草稿</span><span role="status">{dirty ? "有未保存修改" : state.draft.ref === "ABSENT" ? "尚未保存正文" : "当前草稿已保存"}</span><span>{characters.toLocaleString()} 字符</span><button className={styles.primary} disabled={busy || state.read_only} onClick={save}>保存草稿</button><button onClick={() => onDetails?.("versions")}>版本记录</button></div>
      <div className={styles.editorTools}><span>正文</span><label>字号<select aria-label="正文文字大小" value={fontSize} onChange={(event) => setFontSize(event.target.value)}>{["14", "16", "18", "20"].map((size) => <option key={size} value={size}>{size}px</option>)}</select></label><button disabled={dirty || busy || state.draft.ref === "ABSENT"} onClick={select}>引用选中文字</button><button onClick={() => onDetails?.("basis")}>本章依据</button><button onClick={() => onNavigate({ mode: "review" })}>作者检查</button></div>
      <label className={styles.editorLabel}><span className={styles.srOnly}>章节正文</span><textarea ref={editor} aria-label="章节正文" placeholder="从这里开始写下本章正文…" value={text} onChange={(event) => { setText(event.target.value); setSelection(null); }} readOnly={state.read_only} className={styles.editor} style={{ fontSize: `${fontSize}px` }} spellCheck={false} /></label>
      <footer className={styles.editorFooter}><span>{characters.toLocaleString()} 字符 · {dirty ? "未保存" : "当前保存版本"}</span><span>{state.events.some((event) => event.action === "formal.confirmed") ? "正式稿独立保留" : "尚未确认正式稿"}</span></footer>
    </div>}
    {selection && <aside className={styles.source}><h3>选中的正文依据</h3><blockquote>{selection.excerpt}</blockquote><p>范围 {selection.start}–{selection.end} · 当前保存版本</p></aside>}

    {entry.mode === "chapter" && <section className={styles.section}><h2>作者人工修改候选</h2><p>先保存并选择一段正文；人工候选不会冒充员工回复。</p><button disabled={busy || dirty || !selection || state.read_only} onClick={()=>setManualOpen(v=>!v)}>准备人工修改</button>{manualOpen && <><blockquote>{selection?.excerpt}</blockquote><label>候选替换文字<textarea aria-label="人工修改候选" maxLength={200000} value={replacement} onChange={e=>setReplacement(e.target.value)} /></label><button disabled={busy || dirty || !selection || !replacement.trim()} onClick={async()=>{const value=await run("candidate.manual-recorded",{selection,replacement});if(value)setManualOpen(false);}}>保存人工候选</button><button onClick={()=>setManualOpen(false)}>保留原文，收起</button></>}</section>}
    {candidates.length > 0 && <section className={styles.section}><h2>候选修改</h2><p>采用一次点击即形成正式版本；要求修改需填写意见并确认；拒绝后原稿仍可查看。</p>{candidates.map((candidate) => {
      const outcome = candidateOutcome(state.events, candidate.ref);
      const open = panel?.ref === candidate.ref;
      const canAct = !busy && !dirty && !state.read_only && !actionBusy && outcome.status === "PENDING";
      const sourceLabel = candidate.source_class === "CONVERSATION_REPLY" ? "普通对话原回复 · 接收版本不代表生成依据" : candidate.source_class === "CEO_MANUAL" ? "作者人工候选 · 未经独立审校" : candidate.source_class === "AGENT_EXECUTOR" ? "Agent 原工作成果 · 内容待核验" : `员工回复衍生建议 · ${candidate.source_class === "PROVIDER_EXECUTOR" ? "已验证模型回复" : "受控验证来源"}`;
      return <article key={candidate.ref} className={styles.candidate}>
        <p>{sourceLabel}</p>
        <p role="status" className={styles.badge}>{outcome.status === "ADOPTED" ? "已采用 · 正式版本" : outcome.status === "REJECTED" ? "已拒绝" : "待采用"}</p>
        <div>
          <section><h3>{candidate.source_class === "CONVERSATION_REPLY" ? "接收时的当前正文" : "原选段"}</h3><blockquote>{candidate.selection?.excerpt ?? state.draft.text}</blockquote></section>
          <section><h3>将替换为</h3><blockquote>{candidate.replacement}</blockquote></section>
        </div>
        {outcome.status === "ADOPTED" && <p role="status">已采用为正式版本（{outcome.adopted?.formal_ref || outcome.adopted?.ref}）。同一候选重复采用不会新增正式版本；原候选与来源仍保留。</p>}
        {outcome.status === "REJECTED" && <p role="status">已拒绝；原稿与来源仍保留在上方，可继续查看。{outcome.rejected?.reason ? ` 理由：${outcome.rejected.reason}` : ""}</p>}
        {outcome.status === "PENDING" && <div className={styles.opRow}>
          <button className={styles.primary} disabled={!canAct || candidate.draft_ref !== state.draft.ref || actionBusy === candidate.ref} onClick={async () => {
            if (actionPending.current || candidateOutcome(state.events, candidate.ref).status !== "PENDING") return;
            actionPending.current = candidate.ref; setActionBusy(candidate.ref); setError("");
            try {
              const output = await run("candidate.adopted", { candidate_ref: candidate.ref, confirmed: true });
              if (output && output.draft) { setText(output.draft.text); setEditBase(output.draft.ref); savedText.current = output.draft.text; previousHead.current = output.draft.ref; setChecks([]); setSelection(null); setResultMessage("已采用，正式版本已生成。"); }
            } finally { actionPending.current = ""; setActionBusy(""); }
          }}>确认采用这处修改</button>
          <button disabled={!canAct} onClick={() => { setPanel({ kind: "revise", ref: candidate.ref }); setPanelValue(""); }}>要求修改</button>
          <button disabled={!canAct} onClick={() => { setPanel({ kind: "reject", ref: candidate.ref }); setPanelValue(""); }}>拒绝</button>
        </div>}
        {open && <div className={styles.bookItemForm} role="group" aria-label={panel.kind === "revise" ? "要求修改表单" : "拒绝候选表单"}>
          <label>{panel.kind === "revise" ? "修改意见" : "拒绝理由（可选）"}<textarea aria-label={panel.kind === "revise" ? "修改意见" : "拒绝理由"} maxLength={panel.kind === "revise" ? 1600 : 2000} value={panelValue} onChange={(event) => setPanelValue(event.target.value)} /></label>
          <p role="status">{panel.kind === "revise" ? "填写意见并确认提交后才创建关联工作；取消不创建、不调用模型。" : "确认后候选标记为已拒绝，原稿保留；取消不创建任何内容。"}</p>
          <div className={styles.opRow}>
            <button className={styles.primary} disabled={Boolean(actionBusy) || (panel.kind === "revise" && (!panelValue.trim() || !createWorkAvailable))} onClick={() => submitPanel(candidate)}>{panel.kind === "revise" ? "确认提交" : "确认拒绝"}</button>
            <button onClick={() => { setPanel(null); setPanelValue(""); }} aria-label={panel.kind === "revise" ? "取消要求修改" : "取消拒绝"}>取消</button>
          </div>
        </div>}
      </article>;
    })}</section>}
    {formalVersions(state.events).length > 0 && <section className={styles.section} aria-label="正式版本"><h2>正式版本</h2><p role="status">共 {formalVersions(state.events).length} 份正式版本；同一候选重复采用不会新增。</p>{formalVersions(state.events).map((formal, index, all) => <article key={formal.ref} className={styles.formalSnapshot}><p><span className={styles.badge}>正式版本</span> {index === all.length - 1 ? "最新" : "历史"} · {formal.ref}</p><pre>{formal.snapshot?.text ?? ""}</pre></article>)}</section>}
    {sourceOptions.length > 0 && <section className={styles.section} aria-label="续做工作台"><h2>续做 / 二次生成</h2><p>默认基于最新正式版本，可显式选择历史正式版本；没有正式版本时只能基于候选稿，并明确标注来源。</p>
      <label>来源<select aria-label="续做来源" value={sourceRef || chosenSource?.source_ref || ""} onChange={(event) => setSourceRef(event.target.value)}>{sourceOptions.map((option, index) => <option key={option.source_ref} value={option.source_ref}>{option.label}{index === 0 ? "（默认）" : ""} · {option.source_ref}</option>)}</select></label>
      {chosenSource && <div className={styles.formalSnapshot} role="status"><p><strong>来源：</strong>{chosenSource.source_class === "CANDIDATE" ? "基于候选稿（无正式版本）" : `${chosenSource.label} · 正式版本`}</p><p>来源标识：{chosenSource.source_ref}</p><pre>{chosenSource.text}</pre></div>}
      {!continuationOpen && <button className={styles.primary} disabled={!chosenSource} onClick={() => setContinuationOpen(true)}>续做</button>}
      {continuationOpen && <div className={styles.bookItemForm}><label>修改要求<textarea aria-label="续做修改要求" maxLength={1600} value={continuationText} onChange={(event) => setContinuationText(event.target.value)} /></label><p role="status">{continuationDisabledReason || `将基于${chosenSource.label}生成候选，结果仍需人工采用。`}</p><div className={styles.opRow}><button className={styles.primary} disabled={Boolean(continuationDisabledReason) || !chosenSource} onClick={submitContinuation}>确认续做</button><button onClick={() => { setContinuationOpen(false); setContinuationText(""); setSourceRef(""); }} aria-label="取消续做">取消</button></div></div>}
    </section>}
    {entry.mode === "review" && <section className={styles.reviewPanel}><div className={styles.reviewHeading}><span className={styles.badge}>作者裁决</span><h2>检查当前保存版本</h2><p>核对正文、署名与引用，再明确确认正式稿。正式稿仍未发布。</p></div>{(dirty || state.draft.ref === "ABSENT") && <p role="status" className={styles.notice}>请先返回正文保存草稿，再检查当前版本。</p>}<p>按当前正文版本检查，不代表独立审核或平台许可。</p>{WRITING_CHECKS.map((check, index) => <label className={styles.check} key={check}><input type="checkbox" checked={checks.includes(check)} onChange={(e) => setChecks(e.target.checked ? [...checks, check] : checks.filter((v) => v !== check))} />{["情节与人物连贯性", "语言、错字与格式", "署名、引用与权利声明"][index]}</label>)}<label>检查备注<textarea aria-label="检查备注" maxLength={2000} value={note} onChange={(e) => setNote(e.target.value)} /></label><button disabled={busy || dirty || state.read_only || state.draft.ref === "ABSENT" || checks.length !== 3} onClick={() => run("inspection.recorded", { mode: "AUTHOR_MANUAL", checks: WRITING_CHECKS, note })}>记录当前版本作者检查</button>{inspection && <p>当前版本已记录作者人工检查。</p>}{reviewedAdoption && <button type="button" disabled={busy || dirty || lock} onClick={() => { setDiscussionOpen(true); onNavigate({ mode: "chapter" }); }}>返回正文，基于复盘准备下一次工作</button>}<label className={styles.authorConsent}><input type="checkbox" checked={formalConsent} onChange={(event) => setFormalConsent(event.target.checked)} />我已检查当前保存版本，同意确认为正式稿（尚未发布）</label><button className={styles.primary} disabled={busy || dirty || state.read_only || !inspection || !formalConsent} onClick={async () => { if (!formalConsent) return; const formal = await run("formal.confirmed", { inspection_ref: inspection.ref, confirmed: true }); if (formal) onNavigate({ mode: "package", formal: formal.ref, draft: state.draft.ref, package: "", anchor: "" }); }}>明确确认当前版本为正式稿</button><button onClick={() => onNavigate({ mode: "chapter" })}>返回正文，保留检查输入</button></section>}

  </div>;
}
