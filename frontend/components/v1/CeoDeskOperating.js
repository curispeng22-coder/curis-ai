"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";

import { CEO_ID, getAssistantIdentity } from "../../lib/api.js";
import { createFoundingRun, getCanonicalBusinesses, getFoundingRun, getOrganizationProjection, transitionRuntimeEntity, workspaceEntryHref, workspaceOfficeHref } from "../../lib/runtimeApi.js";
import { createBusinessFromFoundingRun, getBusinessDraft, getCEOAssistantConversation, getCompanyAttention, getV1Presentation, saveBusinessDraft, sendCEOAssistantMessage, getBusinessDefinitions, getBusinessCreationResult } from "../../lib/v1FrontendApi.js";
import { useRuntime } from "../runtime/RuntimeProvider.js";
import TerraShell, { TerraPaneContent } from "../terra/TerraShell.js";
import SharedConversation from "./SharedConversation.js";
import ResultReferenceView, { resultSelection, rememberResultSelection, restoreResultSelection } from "./ResultReferenceView.js";
import { confirmationSnapshot, writingRequestLocked, createWritingApi } from "../../lib/writingApi.js";
import { buildOrganizationProjection } from "../../lib/organizationProjection.js";
import { businessCatalogHref, BUSINESS_DIRECTIONS, creationDirectionDefinition } from "./BusinessCatalogSurface.js";
import { conversationError } from "../../lib/v1FrontendApi.js";

import { MUSIC_PACKAGE } from "../../lib/musicState.mjs";

const KIND_COPY = { DECISION_PACKET: "等待决定", HANDOFF: "责任交接", RESULT: "新结果", OUTCOME: "业务结果", EVIDENCE: "证据", ACCEPTANCE: "等待验收", CYCLE: "经营进度", RESPONSIBILITY_ASSIGNMENT: "工作责任" };
const STATUS_COPY = { WAITING_CEO: "等待你决定", FAILED: "需要恢复", BLOCKED: "暂时受阻", IN_REVIEW: "等待确认", PENDING: "等待处理", ACTIVE: "进行中" };

export function LocalBusinessProposal({ children, messages, value, onChange, onSubmit, busy, disabled, submitLabel }) {
  return <section aria-label="整理业务提案" className="overflow-hidden rounded-2xl border border-ui-line bg-ui-surface">
    <header className="border-b border-ui-line px-5 py-4"><h2 className="text-sm font-semibold">整理业务提案</h2><p className="text-xs text-ui-txt-2">根据你填写的目标和字段准备提案</p></header>
    <div className="space-y-4 px-5 py-5">{messages.map((message, index) => <p key={index} className="text-sm text-ui-txt-2">{message.text}</p>)}{children}</div>
    <form onSubmit={onSubmit} className="border-t border-ui-line p-3">
      <label className="block text-sm">业务目标<textarea aria-label="业务目标" value={value} disabled={busy || disabled} onChange={(event) => onChange(event.target.value)} rows={2} className="mt-2 w-full resize-none bg-transparent px-2 py-1 text-sm outline-none" /></label>
      <button type="submit" disabled={busy || disabled || !value?.trim()} className="mt-2 rounded-lg bg-ui-primary px-4 py-2 text-xs font-semibold text-ui-primary-fg disabled:opacity-40">{busy ? "处理中…" : submitLabel}</button>
    </form>
  </section>;
}

export function CreateBusiness({ company, onCreated, originalRecord = null, sourceDefinition = "" }) {
  const [sourceCompany, setSourceCompany] = useState(company.company_id);
  const [previousCreation, setPreviousCreation] = useState(null);
  const newDraftEpoch = useRef(0);
  useEffect(() => () => { newDraftEpoch.current += 1; }, [company.company_id, sourceDefinition]);
  const [originStatus, setOriginStatus] = useState(sourceDefinition ? "loading" : "");
  const companyScope = useRef(company.company_id);
  const [run, setRun] = useState(null); const [stage, setStage] = useState("intent");
  const [intent, setIntent] = useState("");
  const [draft, setDraft] = useState({ business_name: "", goal: "", positioning: "", workspace_name: "", department_id: "", package_id: "" });
  const [definitions, setDefinitions] = useState(null); const [confirmed, setConfirmed] = useState(null);
  const [result, setResult] = useState(null); const [status, setStatus] = useState("");
  const [teamRead, setTeamRead] = useState({ status: "idle" });
  const [teamRefresh, setTeamRefresh] = useState(0);
  const [consent, setConsent] = useState(false); const [busy, setBusy] = useState(false); const [error, setError] = useState("");
  const gate = useRef(false); const locked = busy || writingRequestLocked(status);
  const notifiedRuns = useRef(new Set());
  const storageKey = `curis.businessConfirmation.${company.company_id}`;
  const savedProposal = run?.data?.v1Proposal;
  const teamContract = savedProposal?.package_id === draft.package_id
    ? savedProposal?.snapshot?.definition?.initial_team_contract : null;
  useEffect(() => {
    if (stage !== "created" || !result?.business_id) return;
    let active = true;
    setTeamRead({ companyId: company.company_id, status: "loading" });
    Promise.all([getOrganizationProjection(company.company_id),
      confirmed?.package_id === "com.curis.local.writing-authoring" ? createWritingApi().entry(company.company_id, result.workspace_id) : Promise.resolve(null)])
      .then(([organization, entry]) => {
        if (!active) return;
        if (organization.company?.company_id !== company.company_id || entry && (entry.scope?.company_id !== company.company_id || entry.scope?.workspace_id !== result.workspace_id)) throw new Error("Current team scope changed");
        const team = buildOrganizationProjection(organization).businessById.get(result.business_id);
        if (!team) throw new Error("Current Business is unavailable");
        setTeamRead({ companyId: company.company_id, status: "ready", team, execution: entry?.execution });
      }).catch(() => { if (active) setTeamRead({ companyId: company.company_id, status: "error" }); });
    return () => { active = false; };
  }, [company.company_id, result?.business_id, result?.workspace_id, confirmed?.package_id, stage, teamRefresh]);
  const remember = (value) => { try { sessionStorage.setItem(storageKey, JSON.stringify(value)); } catch {} };
  const acceptResult = (response, notify = true) => {
    if (companyScope.current !== company.company_id) return;
    if (originalRecord && (response.founding_run?.entity_id !== originalRecord.founding_run_id
      || response.founding_run.company_id !== company.company_id
      || response.founding_run.data?.firstBusiness?.business_id !== originalRecord.business_id
      || response.founding_run.data?.firstBusiness?.workspace_id !== originalRecord.workspace_id
      || response.creation_result && (response.creation_result.company_id !== company.company_id
        || response.creation_result.business_id !== originalRecord.business_id || response.creation_result.workspace_id !== originalRecord.workspace_id))) {
      setStatus("UNKNOWN"); setError("原创建结果与当前业务不一致，请从业务详情重新进入。"); return;
    }
    setRun(response.founding_run); setStatus(response.activation?.status || (response.creation_result ? "COMPLETED" : "UNKNOWN"));
    if (response.creation_result) {
      setResult(response.creation_result); setStage("created");
      const key = `${company.company_id}:${response.founding_run.entity_id}`;
      if (notify && !notifiedRuns.current.has(key)) {
        notifiedRuns.current.add(key); onCreated?.(response);
        const created = response.creation_result;
        if (!originalRecord && created.company_id === company.company_id && typeof created.workspace_id === "string" && created.workspace_id.trim()) {
          remember({ runId: response.founding_run.entity_id });
          window.location.assign(workspaceOfficeHref(created.workspace || { workspace_id: created.workspace_id, business_type: confirmed?.package_id || draft.package_id ? "PACKAGE" : "GENERIC" }));
        }
      }
    }
    else setStage("proposal");
    remember({ runId: response.founding_run.entity_id });
  };
  useEffect(() => {
    let active = true;
    companyScope.current = company.company_id;
    setPreviousCreation(null); setSourceCompany(company.company_id); setRun(null); setStage("intent"); setIntent("");
    setDraft({ business_name: "", goal: "", positioning: "", workspace_name: "", department_id: "", package_id: "" });
    setConfirmed(null); setConsent(false); setResult(null); setStatus(""); setError(""); setDefinitions(null);
    setBusy(false); gate.current = false;
    setOriginStatus(sourceDefinition ? "loading" : "");
    const runIds = new URLSearchParams(window.location.search).getAll("founding_run_id");
    if (!originalRecord && (runIds.length > 1 || runIds.length === 1 && !runIds[0])) {
      setStatus("UNKNOWN"); setError("无法确认唯一原提案，请从业务目录重新进入。");
      return () => { active = false; };
    }
    let runId = originalRecord?.founding_run_id || runIds[0];
    if (!originalRecord) try { runId ||= JSON.parse(sessionStorage.getItem(storageKey) || "null")?.runId; } catch {}
    const definitionsRead = getBusinessDefinitions(company.company_id).then((value) => {
      if (!active) return;
      setDefinitions(value);
      if (!runId && sourceDefinition) {
        const definition = creationDirectionDefinition(sourceDefinition, value);
        setOriginStatus(definition ? "" : "unavailable");
        if (definition) setDraft((current) => ({ ...current, package_id: definition.package_id }));
      }
      return value;
    }).catch(() => {
      if (!active) return;
      setDefinitions({ available: false, departments: [], notice: "业务定义暂时不可读取，输入保留。" });
      if (sourceDefinition) setOriginStatus("unavailable");
    });
    if (!runId) return () => { active = false; };
    Promise.all([getFoundingRun(runId), getBusinessDraft(runId)]).then(async ([current, payload]) => {
      if (!active) return;
      const saved = payload.proposal;
      if (current.entity_id !== runId || current.owner_ref !== CEO_ID || payload.founding_run_id !== runId
        || current.company_id && current.company_id !== company.company_id
        || saved?.company_id && saved.company_id !== company.company_id
        || saved?.snapshot?.company_id && saved.snapshot.company_id !== company.company_id
        || saved?.package_id && saved.snapshot?.company_id !== company.company_id
        || !["PROPOSED", "CEO_CONFIRMED", "COMPANY_CREATED"].includes(current.lifecycle_status)) {
        setStatus("UNKNOWN"); setError("无法确认当前公司的原提案，请从业务目录重新进入。"); return;
      }
      if (originalRecord && (current.entity_id !== originalRecord.founding_run_id || current.company_id !== company.company_id
        || current.owner_ref !== CEO_ID || payload.founding_run_id !== current.entity_id
        || current.first_business?.business_id !== originalRecord.business_id || current.first_business?.workspace_id !== originalRecord.workspace_id
        || payload.proposal?.department_id && payload.proposal.department_id !== current.first_business.department_id
        || payload.proposal?.company_id && payload.proposal.company_id !== company.company_id
        || payload.proposal?.snapshot?.company_id && payload.proposal.snapshot.company_id !== company.company_id)) {
        setStatus("UNKNOWN"); setError("无法确认当前公司的原提案，请返回业务详情。"); return;
      }
      setRun({ ...current, data: { v1Proposal: saved } });
      if (saved) { setIntent(saved.intent); setDraft({ business_name: saved.business_name, goal: saved.goal, positioning: saved.positioning || "", workspace_name: saved.workspace_name, package_id: saved.package_id || "", department_id: saved.department_id || "" }); setStage("proposal"); }
      if (sourceDefinition && !originalRecord) {
        const available = await definitionsRead;
        if (!active) return;
        const expectedPackage = BUSINESS_DIRECTIONS.find((item) => item.id === sourceDefinition)?.packageId;
        setOriginStatus(saved?.package_id !== expectedPackage ? "mismatch" : creationDirectionDefinition(sourceDefinition, available) ? "" : "unavailable");
      }
      if (saved?.package_id && ["CEO_CONFIRMED", "COMPANY_CREATED"].includes(current.lifecycle_status)) {
        const original = confirmationSnapshot({ ceo_id: CEO_ID, business_name: saved.business_name, goal: saved.goal,
          positioning: saved.positioning || "", workspace_name: saved.workspace_name, intent_summary: saved.intent,
          package_id: saved.package_id, department_id: saved.department_id, proposal_sha256: saved.proposal_sha256 });
        setConfirmed(original); setConsent(true); setStatus("UNKNOWN");
        const response = await getBusinessCreationResult(company.company_id, runId);
        if (active) acceptResult(response, false);
      }
    }).catch(() => { if (active) { setStatus("UNKNOWN"); setError("原确认结果待核验，请重新读取原确认。"); } });
    return () => { active = false; };
  }, [company.company_id, sourceDefinition]); // eslint-disable-line react-hooks/exhaustive-deps
  const newRun = async () => {
    let current = await createFoundingRun({ owner_ref: CEO_ID, intent_ref: `business-intent-${crypto.randomUUID()}`, org_version: "org-v1", blueprint_version: "" });
    for (const [target, trigger] of [["INTENT_CAPTURED", "capture_intent"], ["CLARIFYING", "request_clarification"], ["PROPOSED", "propose_company"]]) current = await transitionRuntimeEntity(current.entity_id, { target, actor: "CEO", trigger, reason: "CEO填写业务意图并形成可确认提案", evidenceRefs: [], context: {} });
    return current;
  };
  const propose = async (event) => {
    if (originalRecord) return;
    event.preventDefault(); if (!intent.trim() || locked || confirmed || originStatus || gate.current) return;
    gate.current = true; setBusy(true); setError("");
    try {
      const current = await newRun(); const name = intent.trim().slice(0, 24);
      const next = { ...draft, intent: intent.trim(), business_name: name, goal: intent.trim(), workspace_name: draft.package_id ? ((definitions?.definitions || [definitions?.definition]).find((item) => item?.package_id === draft.package_id)?.name || "专业工作空间") : `${name}工作空间` };
      const saved = await saveBusinessDraft(current.entity_id, { ...next, company_id: company.company_id });
      if (companyScope.current !== company.company_id) return;
      setRun(saved); setDraft(next); setStage("proposal"); remember({ runId: saved.entity_id });
      window.history.replaceState(null, "", `${window.location.pathname}?new=1&founding_run_id=${encodeURIComponent(saved.entity_id)}`);
    } catch (caught) { if (companyScope.current === company.company_id) setError(caught.message || "业务提案尚未保存，输入保留。"); }
    finally { if (companyScope.current === company.company_id) { gate.current = false; setBusy(false); } }
  };
  const confirm = async (retry = false) => {
    if (originalRecord) return;
    if (locked || originStatus || gate.current || stage === "created" || (!retry && (confirmed || !consent))) return;
    gate.current = true; setBusy(true); setError("");
    let current = run; let snapshot = confirmed;
    try {
      if (!retry) {
        current ||= await newRun();
        current = await saveBusinessDraft(current.entity_id, { ...draft, intent, company_id: company.company_id });
        if (companyScope.current !== company.company_id) return;
        const proposal = current.data.v1Proposal;
        snapshot = confirmationSnapshot({ ceo_id: CEO_ID, business_name: proposal.business_name, goal: proposal.goal,
          positioning: proposal.positioning || "", workspace_name: proposal.workspace_name, intent_summary: proposal.intent,
          package_id: proposal.package_id || "", department_id: proposal.department_id || "", proposal_sha256: proposal.proposal_sha256 || "" });
        setConfirmed(snapshot); setRun(current);
        const confirmedRunId = current.entity_id;
        current = await transitionRuntimeEntity(current.entity_id, { target: "CEO_CONFIRMED", actor: "CEO", trigger: "confirm_company", reason: "CEO明确确认原业务提案", evidenceRefs: [], context: {} });
        if (companyScope.current !== company.company_id) return;
        if (current.entity_id !== confirmedRunId) throw new Error("原提案身份已变化，请核对。");
        current = { ...current, data: { ...current.data, v1Proposal: proposal } };
        setRun(current); remember({ runId: current.entity_id });
      }
      setStatus("RUNNING");
      const response = await createBusinessFromFoundingRun(company.company_id, current.entity_id, { ...snapshot, retry_no: retry ? 1 : 0 });
      if (companyScope.current !== company.company_id) return;
      if (snapshot.package_id) acceptResult(response);
      else { setStatus("COMPLETED"); onCreated?.(response); window.location.assign(workspaceEntryHref(response.creation_result.workspace_id)); }
    } catch (caught) {
      if (companyScope.current !== company.company_id) return;
      // A response error is a known refusal; a transport failure can still have committed the original confirmation.
      setStatus(caught.status ? "FAILED" : "UNKNOWN"); setError(caught.message || "原确认结果待核验。");
    } finally { if (companyScope.current === company.company_id) { gate.current = false; setBusy(false); } }
  };
  const query = async () => {
    if (!run || gate.current) return;
    gate.current = true; setBusy(true);
    try { acceptResult(await getBusinessCreationResult(company.company_id, run.entity_id)); }
    catch (caught) { if (companyScope.current === company.company_id) { setError(caught.message); setStatus("UNKNOWN"); } }
    finally { if (companyScope.current === company.company_id) { gate.current = false; setBusy(false); } }
  };
  const restoreEditing = () => { if (locked || status !== "FAILED") return; setRun(null); setConfirmed(null); setConsent(false); setStatus(""); remember(null); setStage("proposal"); };
  const field = (name, value) => { if (!locked && !confirmed) setDraft((v) => ({ ...v, [name]: value })); };
  const startNewDraft = async () => {
    if (originalRecord || locked || gate.current || stage !== "created") return;
    const requestEpoch = ++newDraftEpoch.current;
    gate.current = true; setBusy(true); setError("");
    try {
      const available = await getBusinessDefinitions(company.company_id);
      if (companyScope.current !== company.company_id || requestEpoch !== newDraftEpoch.current) return;
      const definition = sourceDefinition ? creationDirectionDefinition(sourceDefinition, available) : null;
      if (sourceDefinition && !definition) { setOriginStatus("unavailable"); return; }
      setPreviousCreation({ runId: run.entity_id, name: confirmed?.business_name || draft.business_name });
      setDefinitions(available); setIntent("");
      setDraft({ business_name: "", goal: "", positioning: "", workspace_name: "", department_id: "", package_id: definition?.package_id || "" });
      setConfirmed(null); setConsent(false); setRun(null); setStatus(""); setResult(null); setStage("intent"); setOriginStatus(""); remember(null);
      window.history.replaceState(null, "", businessCatalogHref(company.company_id, { create: true, sourceDefinition }));
    } catch { if (companyScope.current === company.company_id && requestEpoch === newDraftEpoch.current) setError("新草稿的业务定义暂不可读取，原创建结果仍保留。"); }
    finally { if (companyScope.current === company.company_id && requestEpoch === newDraftEpoch.current) { gate.current = false; setBusy(false); } }
  };
  const originalCreationHref = (id) => `${businessCatalogHref(company.company_id, { create: true })}&founding_run_id=${encodeURIComponent(id)}`;
  const newDraftLabel = `开始新的${BUSINESS_DIRECTIONS.find((item) => item.id === sourceDefinition)?.name || "业务"}草稿`;
  const inputClass = "mt-1 h-10 w-full rounded-lg border border-ui-line bg-ui-surface px-3 text-sm text-ui-txt";
  const messages = [{ role: "assistant", text: "本步骤整理你填写的目标和字段，不调用模型开展研究。核对提案并确认后，才会创建业务和工作空间。" }];
  const creationContent = stage === "created" && result && <div className="mt-4 rounded-xl border border-ui-line p-4"><h3>业务已创建</h3><p>{confirmed?.business_name || draft.business_name}</p><Link href={workspaceOfficeHref(result.workspace || { workspace_id: result.workspace_id, business_type: draft.package_id ? "PACKAGE" : "" })}>进入工作空间 →</Link><Link className="mt-3 block text-ui-primary" href={businessCatalogHref(company.company_id, { businessId: result.business_id })}>查看当前业务 →</Link>{result.initial_team && <p className="mt-3 text-xs text-ui-txt-3">初始团队创建记录已保留；这是创建回执，当前安排以下方实际读取为准。</p>}<section className="mt-3" aria-label="当前业务团队"><h4>当前团队</h4>{teamRead.companyId === company.company_id && teamRead.status === "ready" ? <><p>{teamRead.team.staffingCount} 名当前员工 · {teamRead.team.roleCount} 项责任</p><ul>{teamRead.team.assignments.map((member) => <li key={member.assignmentRef}>{member.employee ? <Link className="text-ui-primary" href={`/ceo-office/organization/employees/${encodeURIComponent(member.employeeRef)}?${new URLSearchParams({ company_id: company.company_id, business_id: result.business_id })}#employee-conversation`}>{member.employee.name} · {member.roleName}</Link> : "当前员工身份无法确认"}{!member.enabled && <p>当前责任员工或岗位不可用，请核对安排。</p>}</li>)}</ul><p role="status">{teamRead.execution?.status === "UNAVAILABLE" ? "员工执行当前不可用；尚需配置可用模型、能力与授权。本地编辑可继续。" : "责任安排不代表模型、工具或执行已可用；请在实际工作空间核对执行状态。"}</p></> : <p role="status">{teamRead.status === "error" ? "当前团队资料暂不可读取，创建回执仍保留。" : "正在读取当前团队…"}</p>}<button type="button" onClick={() => setTeamRefresh((value) => value + 1)}>重新读取当前团队</button></section><p>原确认和创建结果已保留。</p>{!originalRecord && <><Link href={originalCreationHref(run.entity_id)}>查看旧创建结果</Link><button disabled={locked} onClick={startNewDraft}>{newDraftLabel}</button></>}</div>;
  if (sourceCompany !== company.company_id) return <p role="status">正在读取当前公司的业务提案…</p>;
  if (originalRecord) return <section aria-label="原业务创建记录">{creationContent || <><p role="status">{status === "RUNNING" ? "原确认正在处理，尚未完成。" : status === "FAILED" ? "原确认未完成，记录保留。" : "原确认结果待核验，记录保留。"}</p><button type="button" disabled={busy || !run} onClick={query}>查询原确认结果</button></>}{error && <p role="alert">{error}</p>}</section>;
  return <LocalBusinessProposal messages={messages} value={intent} onChange={(v) => { if (!locked && !confirmed) setIntent(v); }} onSubmit={propose} busy={busy} disabled={locked || Boolean(confirmed) || Boolean(originStatus)} submitLabel={stage === "created" ? "业务已创建" : confirmed ? "原确认已保留" : "整理业务提案"}>
    {previousCreation && <p className="text-sm text-ui-txt-2">原业务“{previousCreation.name}”的创建结果保留。<Link href={originalCreationHref(previousCreation.runId)}>查看旧创建结果</Link></p>}
    {originStatus && <section aria-label="来源方向提示"><p role={originStatus === "loading" ? "status" : "alert"}>{originStatus === "loading" ? "正在核对来源方向的可用定义…" : originStatus === "mismatch" ? stage === "created" ? `这是先前的${BUSINESS_DIRECTIONS.find((item) => item.packageId === draft.package_id)?.name || "通用"}业务创建结果，与当前${BUSINESS_DIRECTIONS.find((item) => item.id === sourceDefinition)?.name || "来源"}方向不同。原结果已保留，请明确选择查看旧结果或开始新草稿。` : "来源方向与原提案不一致。原提案已保留，不能按此入口重新提交。" : "来源方向当前不可创建，未改为通用工作空间。请返回业务目录核对。"}</p><Link href={originStatus === "mismatch" && run ? `${businessCatalogHref(company.company_id, { create: true })}&founding_run_id=${encodeURIComponent(run.entity_id)}` : businessCatalogHref(company.company_id)}>{originStatus === "mismatch" ? stage === "created" ? "查看旧创建结果" : "返回原提案" : "返回业务目录"}</Link>{originStatus === "mismatch" && stage === "created" && result && <button disabled={locked} onClick={startNewDraft}>{newDraftLabel}</button>}</section>}
    <label className="mb-3 block text-sm">工作空间<select aria-label="业务工作空间类型" className={inputClass} disabled={locked || Boolean(confirmed) || Boolean(originStatus)} value={draft.package_id} onChange={(e) => field("package_id", e.target.value)}><option value="">通用工作空间</option>{(definitions?.definitions || (definitions?.available ? [definitions.definition] : [])).filter((item) => item.package_id !== MUSIC_PACKAGE.id || item.published === true && item.version === MUSIC_PACKAGE.version && item.digest === MUSIC_PACKAGE.digest).map((item) => <option key={item.package_id} value={item.package_id}>{item.name || "本地写作工作空间"}</option>)}</select></label>
    <p className="text-xs text-ui-txt-3">{draft.package_id ? BUSINESS_DIRECTIONS.find((item) => item.packageId === draft.package_id)?.boundary || "请核对所选工作空间的可用范围。" : "通用工作空间；具体工作以实际责任与能力为准。"}</p>
    {definitions?.available === false && definitions?.notice && <p role="status" className="text-xs text-ui-txt-3">部分业务定义暂不可用：{definitions.notice}</p>}
    {draft.package_id && <label className="mt-3 block text-sm">所属部门<select aria-label="业务所属部门" className={inputClass} disabled={locked || Boolean(confirmed)} value={draft.department_id} onChange={(e) => field("department_id", e.target.value)}><option value="">请选择现有部门</option>{definitions?.departments.map((d) => <option key={d.id} value={d.id}>{d.name}</option>)}</select></label>}
    {stage === "proposal" && <div className="mt-4 rounded-xl border border-ui-line p-4"><h3>确认业务提案</h3><div className="mt-3 grid gap-3 sm:grid-cols-2"><label>业务名称<input className={inputClass} disabled={locked || Boolean(confirmed)} value={draft.business_name} onChange={(e) => field("business_name", e.target.value)} /></label><label>第一工作空间<input className={inputClass} disabled={locked || Boolean(confirmed)} value={draft.workspace_name} onChange={(e) => field("workspace_name", e.target.value)} /></label><label className="sm:col-span-2">你的目标<textarea className={inputClass} disabled={locked || Boolean(confirmed)} value={draft.goal} onChange={(e) => field("goal", e.target.value)} /></label></div><p className="mt-3 text-xs text-ui-txt-3">{draft.package_id ? "只创建当前公司已发行的专业业务与工作空间；本地编辑可继续，员工建议另需当前责任、模型及费用授权。" : "创建通用业务和工作空间，不假装匹配专业方法。"}</p>{draft.package_id && <section className="mt-3" aria-label="本次提案的初始团队"><h4>初始团队</h4>{teamContract ? <><p>将创建{teamContract.displayName}（可改名），兼业务负责人。</p><p>{teamContract.responsibility}</p><p>自检不等于独立审核；模型、工具及员工执行另需配置与授权。</p></> : <p>当前提案未保存有效的初始团队合同；修改后确认会重新保存，请核对。</p>}</section>}<label className="mt-3 flex gap-2 text-sm"><input type="checkbox" checked={consent} disabled={locked || Boolean(confirmed)} onChange={(e) => setConsent(e.target.checked)} />我确认按这份提案创建业务与第一工作空间</label><div className="mt-4 flex flex-wrap gap-2">{!confirmed && <button disabled={locked || Boolean(originStatus) || !consent || !draft.business_name.trim() || !draft.goal.trim() || !draft.workspace_name.trim() || (Boolean(draft.package_id) && !draft.department_id)} onClick={() => confirm()} className="rounded-lg bg-ui-primary px-4 py-2 text-sm text-ui-primary-fg">确认创建业务</button>}{status === "FAILED" && <><button disabled={busy || Boolean(originStatus)} onClick={() => confirm(true)}>重试原确认</button><button disabled={busy} onClick={restoreEditing}>恢复提案编辑，重新确认</button></>}{confirmed && <button disabled={busy} onClick={query}>查询原确认结果</button>}{!confirmed && <button disabled={locked} onClick={() => setStage("intent")}>返回修改</button>}</div>{status && <p role="status" className="mt-3">{status === "RUNNING" ? "原确认正在处理，请等待或查询原结果。" : status === "UNKNOWN" ? "原确认结果待核验，已保留原提案，不会再次创建。" : status === "FAILED" ? "原确认未完成，提案保留。" : "原确认已完成。"}</p>}</div>}
    {creationContent}
    {error && <p role="alert" className="mt-3 text-ui-red">{error}</p>}
  </LocalBusinessProposal>;
}

export const ceoResultTabId = (companyId, selection) => JSON.stringify([companyId, "result", selection.workspaceId, selection.referenceId]);

export function CeoDeskPaneContent({ company, snapshot, view, selectedResult, openResult, onViewed, onClose, requestKey }) {
  const panes = useMemo(() => {
    const businesses = view.businesses.filter((item) => item.company_id === company.company_id);
    const items = view.attention?.items || [];
    const context = <nav aria-label="公司业务导航" className="space-y-4"><h2 className="text-sm font-semibold">{company.name}</h2>{businesses.length ? businesses.map((item) => <Link key={item.business_id} className="block text-sm text-ui-primary" href={`/ceo-office/business?company_id=${encodeURIComponent(company.company_id)}&business_id=${encodeURIComponent(item.business_id)}`}>{item.name || "未命名业务"}</Link>) : <p className="text-sm text-ui-txt-2">还没有经营中的业务</p>}<Link className="block text-sm text-ui-primary" href={`/ceo-office/business?company_id=${encodeURIComponent(company.company_id)}`}>查看业务目录 →</Link></nav>;
    const tabs = [{ id: JSON.stringify([company.company_id, "facts"]), title: "当前公司", content: <section><h2 className="text-lg font-semibold">{company.name}</h2><dl className="mt-4 space-y-3 text-sm"><div><dt className="text-ui-txt-2">已读取业务</dt><dd>{businesses.length}</dd></div><div><dt className="text-ui-txt-2">工作空间</dt><dd>{Array.isArray(snapshot.workspaces) ? snapshot.workspaces.length : "尚未读取"}</dd></div><div><dt className="text-ui-txt-2">CEO 助理</dt><dd>{view.conversation?.assistant?.name || view.identity?.name || "姓名尚未读取"}</dd></div></dl>{!businesses.length && <p className="mt-5 text-sm text-ui-txt-2">公司已建立，可以先了解业务方向。</p>}</section> }];
    if (items.length) tabs.push({ id: JSON.stringify([company.company_id, "attention"]), title: "责任与结果", content: <section><h2 className="text-lg font-semibold">已读取事项</h2>{items.map((item) => <div className="mt-4 text-sm" key={item.source_ref}><p>{item.summary}</p><p className="mt-1 text-ui-txt-2">{STATUS_COPY[item.status] || "查看事实"}</p>{item.source_type === "RESULT" && <button type="button" className="mt-2 text-ui-primary" onClick={() => openResult(item)}>查看结果 →</button>}{item.next_check_at && <p className="mt-1 text-ui-txt-2">下次检查：{item.next_check_at}</p>}</div>)}</section> });
    const selections = items.filter((item) => item.source_type === "RESULT" && item.workspace_id && item.source_ref).map((item) => ({ selection: resultSelection(item.workspace_id, item.source_ref), title: item.summary || "结果详情" }));
    if (selectedResult && !selections.some((item) => ceoResultTabId(company.company_id, item.selection) === ceoResultTabId(company.company_id, selectedResult))) selections.push({ selection: selectedResult, title: "原结果" });
    for (const item of selections) tabs.push({ id: ceoResultTabId(company.company_id, item.selection), title: item.title, content: <ResultReferenceView companyId={company.company_id} selection={item.selection} onViewed={onViewed} onClose={onClose} /> });
    return { context, tabs };
  }, [company, snapshot, view, selectedResult, openResult, onViewed, onClose]);
  return <TerraPaneContent contextPane={panes.context} utilityTabs={panes.tabs} contextLabel="公司业务" utilityLabel="对象信息" initialContextOpen initialUtilityOpen utilityRequestKey={requestKey} utilityRequestTabId={selectedResult ? ceoResultTabId(company.company_id, selectedResult) : ""} />;
}

export default function CeoDeskOperating() {
  const runtime = useRuntime();
  const [view, setView] = useState({ companyId: "", status: "loading", attention: null, businesses: [], identity: null, conversation: null, presentation: null, error: "" });
  const readGeneration = useRef(0);
  const resultCompany = useRef(runtime.companyId);
  const [resultRequest, setResultRequest] = useState(0);
  const [selectedResult, setSelectedResult] = useState(null);
  useEffect(() => { setSelectedResult(restoreResultSelection()); }, []);
  const openResult = (item) => { const selected = resultSelection(item.workspace_id, item.source_ref); setSelectedResult(selected); rememberResultSelection(selected); setResultRequest((value) => value + 1); };
  const [assistantInput, setAssistantInput] = useState("");
  const [assistantBusy, setAssistantBusy] = useState(false);
  const [assistantError, setAssistantError] = useState("");
  const assistantRequest = useRef(0);
  useEffect(() => { assistantRequest.current += 1; setAssistantInput(""); setAssistantBusy(false); setAssistantError(""); }, [runtime.companyId]);
  const load = useCallback(async () => {
    if (!runtime.companyId) return;
    const companyId = runtime.companyId;
    const generation = ++readGeneration.current;
    try {
      const attention = await getCompanyAttention(companyId);
      if (attention?.company?.company_id !== companyId || !Array.isArray(attention.items)
        || attention.state !== (attention.items.length ? "PARTIAL" : "QUIET")
        || !Number.isInteger(attention.workspace_count) || attention.workspace_count < 0
        || attention.items.some((item) => !item || typeof item !== "object" || Array.isArray(item)
          || typeof item.source_ref !== "string" || !item.source_ref.trim()
          || typeof item.source_type !== "string" || !Object.hasOwn(KIND_COPY, item.source_type)
          || typeof item.summary !== "string" || !item.summary.trim()
          || typeof item.status !== "string" || !item.status.trim()
          || item.workspace_id != null && typeof item.workspace_id !== "string"
          || item.next_check_at != null && typeof item.next_check_at !== "string"
          || item.responsibility_ref != null && typeof item.responsibility_ref !== "string")) throw new Error("公司事项来源无法确认");
      const businessPayload = await getCanonicalBusinesses(companyId);
      if (businessPayload?.company_id !== companyId || !Array.isArray(businessPayload.businesses)
        || businessPayload.businesses.some((item) => !item || typeof item !== "object" || Array.isArray(item)
          || item.company_id !== companyId || typeof item.business_id !== "string" || !item.business_id.trim()
          || item.name != null && typeof item.name !== "string")) throw new Error("当前业务来源无法确认");
      const [identityResult, conversationResult, presentationResult] = await Promise.allSettled([
        getAssistantIdentity(), getCEOAssistantConversation(companyId), getV1Presentation(),
      ]);
      if (generation !== readGeneration.current) return;
      setView({
        companyId,
        status: "ready",
        attention,
        businesses: businessPayload.businesses,
        identity: identityResult.status === "fulfilled" ? identityResult.value : null,
        conversation: conversationResult.status === "fulfilled" ? conversationResult.value : null,
        presentation: presentationResult.status === "fulfilled" ? presentationResult.value : null,
        error: "",
      });
    } catch (caught) { if (generation === readGeneration.current) setView((current) => ({ ...current, companyId: runtime.companyId, status: "error", error: conversationError(caught, "经营信息暂时无法读取，请重新读取。") })); }
  }, [runtime.companyId]);
  const sendAssistant = async (event, selectedModel) => {
    event.preventDefault();
    if (!assistantInput.trim()) return;
    const request = ++assistantRequest.current;
    setAssistantBusy(true); setAssistantError("");
    try {
      const response = await sendCEOAssistantMessage(runtime.companyId, {
        message: assistantInput.trim(),
        model_key: selectedModel?.capability_id || selectedModel?.model_key || "",
        references: selectedResult ? [{ reference_id: selectedResult.referenceId, workspace_id: selectedResult.workspaceId }] : [],
      });
      if (request !== assistantRequest.current) return;
      setAssistantInput("");
      setView((current) => ({ ...current, conversation: { ...current.conversation, messages: response.messages } }));
    } catch (caught) {
      if (request === assistantRequest.current) setAssistantError(conversationError(caught, "CEO 助理暂时无法回复，输入已保留。请检查模型连接后重试。"));
    } finally { if (request === assistantRequest.current) setAssistantBusy(false); }
  };
  useEffect(() => {
    readGeneration.current += 1;
    if (resultCompany.current !== runtime.companyId) { resultCompany.current = runtime.companyId; setSelectedResult(null); setResultRequest(0); }
    if (runtime.status === "ready") load();
  }, [load, runtime.status, runtime.companyId]);
  useEffect(() => { const refresh = () => { if (document.visibilityState === "visible") load(); }; window.addEventListener("focus", refresh); document.addEventListener("visibilitychange", refresh); return () => { window.removeEventListener("focus", refresh); document.removeEventListener("visibilitychange", refresh); }; }, [load]);
  useEffect(() => { if (runtime.status === "empty") window.location.replace("/welcome"); }, [runtime.status]);
  if (runtime.status === "empty") return <main className="grid min-h-screen place-items-center bg-ui-bg text-sm text-ui-txt-3">正在返回 Curis 入口…</main>;
  if (["idle", "loading"].includes(runtime.status) || runtime.status === "ready" && (view.status === "loading" || view.companyId !== runtime.companyId)) return <main className="grid min-h-screen place-items-center bg-ui-bg text-sm text-ui-txt-3">正在准备今天的经营信息…</main>;
  if (["error", "forbidden"].includes(runtime.status) || view.status === "error") return <main className="grid min-h-screen place-items-center bg-ui-bg px-6"><section className="rounded-2xl bg-ui-surface p-7"><h1 className="text-xl font-semibold">暂时无法读取 CEO 工作台</h1><p className="mt-2 text-sm text-ui-txt-2">{runtime.error || view.error}</p><button onClick={() => { runtime.refresh(); load(); }} className="mt-4 text-sm font-semibold text-ui-primary">重新读取</button></section></main>;
  const items = view.attention?.items || []; const primary = items[0]; const watching = items.slice(1, 4); const important = items.find((item) => ["RESULT", "OUTCOME", "ACCEPTANCE"].includes(item.source_type)); const next = items.find((item) => item.responsibility_ref || item.next_check_at);
  const company = runtime.snapshot.company; const assistantName = view.conversation?.assistant?.name || view.identity?.name || "CEO 助理";
  const attentionMain = <div className="grid gap-4 "><div className="space-y-4"><section className="rounded-2xl border border-ui-line bg-ui-surface p-6"><span className="text-xs font-semibold text-ui-primary">今天最重要</span>{primary ? <><div className="mt-3 flex items-start justify-between gap-3"><div><h2 className="text-xl font-semibold">{primary.summary}</h2><p className="mt-2 text-sm text-ui-txt-2">{"来自原工作责任"} · {STATUS_COPY[primary.status] || "查看事实"}</p></div><span className="rounded-full bg-ui-amber-soft px-2.5 py-1 text-xs font-semibold text-ui-amber">{KIND_COPY[primary.source_type] || "经营事项"}</span></div>{primary.source_type === "RESULT" ? <button type="button" onClick={() => openResult(primary)} className="mt-5 mr-4 text-sm font-semibold text-ui-primary">查看结果 ▸</button> : null}<a href={primary.workspace_id ? workspaceEntryHref(primary.workspace_id) : "/ceo-office/decisions"} className="mt-5 inline-flex text-sm font-semibold text-ui-primary">回到业务现场 →</a></> : <><h2 className="mt-3 text-xl font-semibold">今天没有需要你处理的事项</h2><p className="mt-2 text-sm text-ui-txt-3">这是根据当前可读取的 经营记录得出的安静状态。</p></>}</section><section className="rounded-2xl border border-ui-line bg-ui-surface p-5"><div className="flex items-center justify-between"><h2 className="text-sm font-semibold">持续关注</h2><Link href="/ceo-office/business" className="text-xs text-ui-primary">查看业务</Link></div>{watching.length ? <ul className="mt-3 divide-y divide-ui-line">{watching.map((item) => <li key={item.source_ref} className="py-3"><p className="text-sm font-medium">{item.summary}</p><p className="mt-1 text-xs text-ui-txt-3">{STATUS_COPY[item.status] || "查看工作进度"}</p>{item.source_type === "RESULT" ? <button type="button" onClick={() => openResult(item)} className="mt-2 text-xs text-ui-primary">查看结果 ▸</button> : <a href={item.workspace_id ? workspaceEntryHref(item.workspace_id) : "/ceo-office/decisions"} className="mt-2 block text-xs text-ui-primary">返回原事项 ▸</a>}</li>)}</ul> : <p className="mt-3 text-sm text-ui-txt-3">暂无其他已确认的关注事项。</p>}</section></div></div>;
  return <TerraShell topCrumb={company.name} assistantContext={{ page: "ceo-desk", companyId: company.company_id }}><CeoDeskPaneContent company={company} snapshot={runtime.snapshot} view={view} selectedResult={selectedResult} openResult={openResult} onViewed={load} onClose={() => { setSelectedResult(null); rememberResultSelection(null); }} requestKey={resultRequest} /><div className="mx-auto max-w-[1180px] text-ui-txt"><header className="mb-5 flex flex-wrap items-end justify-between gap-4"><div><p className="text-xs font-semibold text-ui-primary">CEO 工作台</p><h1 className="mt-1 text-3xl font-semibold tracking-[-0.03em]">早上好，{view.presentation?.display_name || "CEO"}</h1><p className="mt-2 text-sm text-ui-txt-3">只看今天需要知道、决定和推进的事情。</p></div><Link href="/ceo-office/business" className="rounded-xl border border-ui-line bg-ui-surface px-4 py-2 text-sm font-semibold text-ui-txt-2 no-underline">进入业务空间</Link></header><section className="mb-4 flex flex-wrap items-center gap-x-6 gap-y-2 rounded-2xl border border-ui-line bg-ui-surface px-5 py-4 text-sm"><strong>{company.name}</strong><span className="text-ui-txt-3">{view.attention?.workspace_count || 0} 个工作空间</span><span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${items.length ? "bg-ui-amber-soft text-ui-amber" : "bg-ui-green-soft text-ui-green"}`}>{items.length ? `${items.length} 项需要关注` : "经营平稳"}</span><span className="ml-auto text-xs text-ui-txt-3">公司事实 · {view.attention?.state === "QUIET" ? "安静" : "部分可用"}</span></section>{!view.businesses.length ? <>{attentionMain}<div className="mt-4"><CreateBusiness company={company} onCreated={load} /></div></> : <>{attentionMain}<div className="mt-4"><SharedConversation scopeKey={`${company.company_id}:${view.conversation?.assistant?.assistant_id || ""}`} employee={{ ...view.conversation?.assistant, name: assistantName, role: "公司级协调与经营跟进" }} messages={view.conversation?.messages?.length ? view.conversation.messages : [{ role: "assistant", text: `我会持续关注 ${view.businesses.length} 项业务。需要你决定的事项会出现在上方，并保留原始业务入口。` }]} value={assistantInput} onChange={setAssistantInput} onSubmit={sendAssistant} busy={assistantBusy} placeholder="向 CEO 助理询问公司经营情况…">{assistantError ? <p role="alert" className="rounded-lg bg-ui-red-soft px-3 py-2 text-sm text-ui-red">{assistantError}</p> : null}</SharedConversation></div></>}</div></TerraShell>;
}
