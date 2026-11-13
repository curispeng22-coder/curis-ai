"use client";

import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";

import { useRuntime } from "../../../components/runtime/RuntimeProvider.js";
import { RuntimeEmpty, RuntimeError, RuntimeLoading } from "../../../components/runtime/RuntimeStates.js";
import TerraShell, { TerraPaneContent } from "../../../components/terra/TerraShell.js";
import { d1Href } from "../../../lib/d1State.mjs";
import { EmployeeAvatar } from "../../../components/v1/EmployeeAvatar.js";
import SharedConversation from "../../../components/v1/SharedConversation.js";
import {
  addMeetingMessage,
  chooseMeetingDecision,
  closeMeeting,
  createMeeting,
  getEmployees,
  getMeeting,
  getMeetings,
  requestMeetingDecision,
  reviewMeetingDecision,
  syncMeeting,
} from "../../../lib/api.js";
import { roleLabel } from "../../../lib/theme.js";
import { getKnowledgeEntries } from "../../../lib/knowledge.js";
import { getCanonicalBusinesses, runtimeErrorMessage, workspaceEntryHref } from "../../../lib/runtimeApi.js";

const PROVENANCE = { FACT: "事实", POLICY: "规则", EVIDENCE: "证据", EST: "员工估计", UNK: "未知" };
const STATE = {
  DISCUSSING: ["讨论中", "bg-ui-green-soft text-ui-green"],
  WAITING_CEO: ["等待你决定", "bg-ui-amber-soft text-ui-amber"],
  WAITING_RESULT: ["等待结果", "bg-ui-cyan-soft text-ui-cyan"],
  ARCHIVED: ["已结束", "bg-ui-surface-2 text-ui-txt-3"],
};
const CEO_MODE = { DECISION_ONLY: "只在需要决定时参与", OBSERVE: "旁听并接收进展", JOIN: "参与完整讨论" };
const CONTINUATION_STATE = {
  READY: "团队已准备继续讨论",
  RUNNING: "团队讨论中",
  WAITING_CEO: "等待你决定",
  WAITING_WORK: "等待工作结果",
  SUFFICIENT: "本轮讨论已充分",
  NO_PROGRESS: "讨论暂时没有新的进展",
  BLOCKED: "团队讨论已暂停",
  STOPPED: "会议已停止自动推进",
};
function continuationReason(reason) {
  const value = String(reason || "");
  if (!value) return "";
  if (/Meeting Result contract/i.test(value)) return "员工返回的内容还不能作为会议结果，可以补充资料或更换模型后重试";
  if (/provider|model|timeout|unavailable/i.test(value)) return "当前模型服务暂时不可用，可以稍后重试或更换模型";
  return "当前执行没有形成可继续使用的结果";
}
const emptyForm = { title: "", background: "", business_id: "", workspace_id: "", leader_ref: "", participant_refs: [], ceo_participation_mode: "DECISION_ONLY", context_refs: [] };
const emptyProposal = { summary: "", optionA: "", optionB: "" };
const emptyMeetingDraft = { text: "", proposal: emptyProposal };

function Badge({ state, meeting }) {
  const [label, style] = STATE[state] || ["状态未知", STATE.ARCHIVED[1]];
  const automatic = meeting?.orchestration?.status || meeting?.background_continuation?.state;
  const paused = meeting?.status !== "closed" && state !== "ARCHIVED" && ["BLOCKED", "STOPPED"].includes(automatic);
  return <span className="inline-flex flex-wrap items-center gap-2"><span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${style}`}>{state === "DISCUSSING" && meeting?.status === "active" ? "会议进行中" : label}</span>{paused && <span className="rounded-full bg-ui-amber-soft px-2.5 py-1 text-xs font-semibold text-ui-amber">{automatic === "STOPPED" ? "自动讨论已停止" : "自动讨论暂不可用"}</span>}</span>;
}

function MeetingOverlay({ open, onClose, onCreate, businesses, employees, knowledge, busy, error }) {
  const [form, setForm] = useState(emptyForm);
  const workspaces = useMemo(() => businesses.flatMap((business) =>
    (business.workspaces || []).map((workspace) => ({ ...workspace, business_id: business.business_id, business_name: business.name }))), [businesses]);
  useEffect(() => {
    if (!open) return;
    const workspace = workspaces[0];
    const leader = employees[0];
    setForm({ ...emptyForm, business_id: workspace?.business_id || businesses[0]?.business_id || "", workspace_id: workspace?.workspace_id || "", leader_ref: leader?.id || "", participant_refs: leader ? [leader.id] : [] });
  }, [businesses, employees, open, workspaces]);
  if (!open) return null;
  const chooseWorkspace = (workspaceId) => {
    const workspace = workspaces.find((item) => item.workspace_id === workspaceId);
    setForm((current) => ({ ...current, workspace_id: workspaceId, business_id: workspace?.business_id || "" }));
  };
  const toggleParticipant = (employeeId) => setForm((current) => ({
    ...current,
    participant_refs: current.participant_refs.includes(employeeId)
      ? current.participant_refs.filter((item) => item !== employeeId)
      : [...current.participant_refs, employeeId],
  }));
  const toggleContext = (id) => setForm((current) => ({
    ...current,
    context_refs: current.context_refs.some((item) => item.ref === id)
      ? current.context_refs.filter((item) => item.ref !== id)
      : [...current.context_refs, { type: "KNOWLEDGE", ref: id }],
  }));
  const valid = form.title.trim() && form.workspace_id && form.leader_ref && form.participant_refs.includes(form.leader_ref);
  return <div className="fixed inset-0 z-[80] grid place-items-center bg-black/30 px-4 py-8 backdrop-blur-[2px]" role="dialog" aria-modal="true" aria-label="召开会议">
    <form onSubmit={(event) => { event.preventDefault(); if (valid) onCreate(form); }} className="max-h-full w-full max-w-[760px] overflow-y-auto rounded-2xl border border-ui-line bg-ui-surface p-6 shadow-ui-3">
      <div className="flex items-start justify-between gap-4"><div><p className="text-xs font-semibold text-ui-primary">召开会议</p><h2 className="mt-1 text-xl font-semibold text-ui-txt">把一个真实经营问题交给团队</h2><p className="mt-1 text-xs text-ui-txt-3">会议会持续存在；离开页面不会结束讨论。</p></div><button type="button" onClick={onClose} className="rounded-lg px-2 py-1 text-sm text-ui-txt-3 hover:bg-ui-surface-2">关闭</button></div>
      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <label className="md:col-span-2 text-xs font-medium text-ui-txt-2">议题<input autoFocus value={form.title} onChange={(event) => setForm({ ...form, title: event.target.value })} placeholder="例如：下一阶段应该优先解决哪个客户问题？" className="mt-2 h-11 w-full rounded-xl border border-ui-line bg-ui-surface px-3 text-sm outline-none focus:border-ui-primary" /></label>
        <label className="md:col-span-2 text-xs font-medium text-ui-txt-2">背景<textarea value={form.background} onChange={(event) => setForm({ ...form, background: event.target.value })} rows={3} placeholder="补充已有事实、约束或为什么现在需要讨论" className="mt-2 w-full resize-none rounded-xl border border-ui-line bg-ui-surface p-3 text-sm outline-none focus:border-ui-primary" /></label>
        <label className="text-xs font-medium text-ui-txt-2">相关工作空间<select value={form.workspace_id} onChange={(event) => chooseWorkspace(event.target.value)} className="mt-2 h-11 w-full rounded-xl border border-ui-line bg-ui-surface px-3 text-sm"><option value="">请选择</option>{workspaces.map((item) => <option key={item.workspace_id} value={item.workspace_id}>{item.business_name} · {item.name}</option>)}</select></label>
        <label className="text-xs font-medium text-ui-txt-2">推进负责人<select value={form.leader_ref} onChange={(event) => { const id = event.target.value; setForm({ ...form, leader_ref: id, participant_refs: form.participant_refs.includes(id) ? form.participant_refs : [...form.participant_refs, id] }); }} className="mt-2 h-11 w-full rounded-xl border border-ui-line bg-ui-surface px-3 text-sm"><option value="">请选择</option>{employees.map((item) => <option key={item.id} value={item.id}>{item.name} · {roleLabel(item.role)}</option>)}</select></label>
      </div>
      <fieldset className="mt-5"><legend className="text-xs font-medium text-ui-txt-2">参与员工</legend><div className="mt-2 grid gap-2 sm:grid-cols-2">{employees.length ? employees.map((item) => <label key={item.id} className={`flex cursor-pointer items-center gap-3 rounded-xl border p-3 ${form.participant_refs.includes(item.id) ? "border-ui-primary bg-ui-primary-soft" : "border-ui-line"}`}><input type="checkbox" checked={form.participant_refs.includes(item.id)} onChange={() => toggleParticipant(item.id)} /><EmployeeAvatar employee={item} className="h-8 w-8" /><span className="min-w-0"><strong className="block truncate text-xs text-ui-txt">{item.name}</strong><span className="text-xs text-ui-txt-3">{roleLabel(item.role)}</span></span></label>) : <p className="text-xs text-ui-amber">当前公司还没有可加入会议的员工。</p>}</div></fieldset>
      <fieldset className="mt-5"><legend className="text-xs font-medium text-ui-txt-2">相关资料（可选）</legend><div className="mt-2 flex flex-wrap gap-2">{knowledge.length ? knowledge.slice(0, 8).map((item) => <button type="button" key={item.id} onClick={() => toggleContext(item.id)} className={`rounded-lg border px-3 py-2 text-xs ${form.context_refs.some((ref) => ref.ref === item.id) ? "border-ui-primary bg-ui-primary-soft text-ui-primary" : "border-ui-line text-ui-txt-2"}`}>{item.title}</button>) : <span className="text-xs text-ui-txt-3">暂无可引用资料，可以先开会。</span>}</div></fieldset>
      <fieldset className="mt-5"><legend className="text-xs font-medium text-ui-txt-2">你的参与方式</legend><div className="mt-2 grid gap-2 md:grid-cols-3">{Object.entries(CEO_MODE).map(([value, label]) => <label key={value} className={`cursor-pointer rounded-xl border p-3 text-xs ${form.ceo_participation_mode === value ? "border-ui-primary bg-ui-primary-soft text-ui-primary" : "border-ui-line text-ui-txt-2"}`}><input className="mr-2" type="radio" name="ceo-mode" value={value} checked={form.ceo_participation_mode === value} onChange={() => setForm({ ...form, ceo_participation_mode: value })} />{label}</label>)}</div></fieldset>
      {error ? <p role="alert" className="mt-4 rounded-lg bg-ui-red-soft px-3 py-2 text-xs text-ui-red">{error}</p> : null}
      <div className="mt-6 flex justify-end gap-2"><button type="button" onClick={onClose} className="rounded-lg border border-ui-line px-4 py-2 text-xs font-semibold text-ui-txt-2">取消</button><button disabled={!valid || busy} className="rounded-lg bg-ui-primary px-5 py-2 text-xs font-semibold text-ui-primary-fg disabled:opacity-40">{busy ? "正在召开…" : "开始会议"}</button></div>
    </form>
  </div>;
}

function DecisionPanel({ meeting, onRefresh }) {
  const decision = meeting.decision;
  const [open, setOpen] = useState(Boolean(decision?.data?.layer1ReviewedAt));
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  if (!decision) return null;
  const data = decision.data || {};
  const waiting = decision.lifecycle_status === "WAITING_CEO";
  const highRisk = data.complexity === "HIGH_RISK";
  const recommendation = data.recommendation?.optionId;
  const reveal = async () => {
    setBusy(true); setError("");
    try { if (waiting) await reviewMeetingDecision(meeting.company_id, meeting.meeting_id); setOpen(true); await onRefresh(); }
    catch (cause) { setError(cause.message); } finally { setBusy(false); }
  };
  const choose = async (choice) => {
    setBusy(true); setError("");
    try { await chooseMeetingDecision(meeting.company_id, meeting.meeting_id, { choice, reason: "CEO已在会议中确认该方案" }); await onRefresh(); }
    catch (cause) { setError(cause.message); } finally { setBusy(false); }
  };
  return <section className="rounded-2xl border border-ui-line bg-ui-amber-soft p-4">
    <div className="flex flex-wrap items-start justify-between gap-3"><div><span className="text-xs font-semibold text-ui-amber">{waiting ? "等待你的决定" : "决定已应用"}</span><h3 className="mt-1 text-sm font-semibold text-ui-txt">{data.event}</h3><p className="mt-1 text-xs leading-5 text-ui-txt-2">{data.cannotDecideReason}</p></div>{waiting ? <div className="flex gap-2">{!highRisk && !open ? <button disabled={busy} onClick={() => choose(recommendation)} className="rounded-lg bg-ui-primary px-3 py-2 text-xs font-semibold text-ui-primary-fg">按建议处理</button> : null}<button disabled={busy} onClick={reveal} className="rounded-lg border border-ui-line bg-ui-surface px-3 py-2 text-xs font-semibold text-ui-amber">查看方案</button><button disabled={busy} onClick={() => choose("DEFER")} className="rounded-lg px-3 py-2 text-xs text-ui-amber">暂缓</button></div> : null}</div>
    {open ? <div className="mt-4 border-t border-ui-line pt-4"><div className="grid gap-3 md:grid-cols-2">{(data.options || []).map((option) => <article key={option.optionId} className="rounded-xl border border-ui-line bg-ui-surface p-3"><div className="flex items-start justify-between gap-2"><strong className="text-xs text-ui-txt">{option.label}</strong>{option.optionId === recommendation ? <span className="text-xs font-semibold text-ui-primary">员工建议</span> : null}</div>{[["影响", option.impact], ["风险", option.risk], ["代价", option.cost]].map(([label, fact]) => <p key={label} className="mt-2 text-xs leading-5 text-ui-txt-2"><span className="font-semibold text-ui-txt-2">{label}</span> · {fact?.value || "未知"} <span className="text-ui-txt-3">[{PROVENANCE[fact?.provenance] || "未知"}]</span></p>)}{waiting ? <button disabled={busy} onClick={() => choose(option.optionId)} className="mt-3 w-full rounded-lg border border-ui-line px-3 py-2 text-xs font-semibold text-ui-primary hover:border-ui-primary">选择这个方案</button> : null}</article>)}</div><p className="mt-3 text-xs text-ui-txt-2">建议理由：{data.recommendationReason?.value || "未知"} [{PROVENANCE[data.recommendationReason?.provenance] || "未知"}]</p></div> : null}
    {error ? <p role="alert" className="mt-3 text-xs text-ui-red">{error}</p> : null}
  </section>;
}

function TimelineItem({ item, people }) {
  if (item.kind === "SYSTEM") return <p className="text-center text-xs text-ui-txt-3">{item.text}</p>;
  const employee = people.get(item.actorRef);
  const ceo = item.actorType === "CEO";
  if (["DECISION_REQUEST", "DECISION_RESULT", "RESULT_RETURNED"].includes(item.kind)) return <div className="rounded-xl border border-ui-line bg-ui-surface-2 p-3 text-xs text-ui-txt-2"><strong className="block text-ui-txt">{item.kind === "DECISION_REQUEST" ? "决策请求" : item.kind === "RESULT_RETURNED" ? "结果已返回" : "决定已记录"}</strong><p className="mt-1">{item.text}</p>{item.gap ? <p className="mt-2 text-ui-amber">{item.gap}</p> : null}</div>;
  return <div className={`flex gap-2 ${ceo ? "justify-end" : ""}`}>{!ceo ? <EmployeeAvatar employee={employee || { name: "员工" }} className="h-8 w-8" /> : null}<div className={`max-w-[78%] ${ceo ? "rounded-2xl rounded-br-md bg-ui-primary-soft px-4 py-3 text-ui-primary" : "pt-1"}`}><p className="text-xs text-ui-txt-3">{ceo ? "CEO" : employee?.name || "员工"}</p><p className="mt-1 text-sm leading-6">{item.text}</p></div></div>;
}

function MeetingDetail({ meeting, onBack, onReload, contextPane, draft, onDraftChange, onDraftSubmitted }) {
  const { text, proposal } = draft;
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const people = useMemo(() => new Map((meeting.participants_detail || []).map((item) => [item.id, item])), [meeting.participants_detail]);
  const refreshIdentity = `${meeting.company_id}:${meeting.meeting_id}`, currentRefresh = useRef(refreshIdentity), refreshing = useRef(false);
  useLayoutEffect(() => { currentRefresh.current = refreshIdentity; return () => { currentRefresh.current = ""; }; }, [refreshIdentity]);
  const refresh = useCallback(async () => {
    if (refreshing.current) return; refreshing.current = true; const identity = refreshIdentity; setBusy(true); setError("");
    try { await syncMeeting(meeting.company_id, meeting.meeting_id); if (currentRefresh.current === identity) await onReload(); }
    catch (cause) { if (currentRefresh.current === identity) setError(cause.message || "会议暂时无法刷新，原输入已保留。"); }
    finally { refreshing.current = false; if (currentRefresh.current === identity) setBusy(false); }
  }, [refreshIdentity, meeting.company_id, meeting.meeting_id, onReload]);
  const send = async (event) => {
    event.preventDefault(); if (!text.trim()) return;
    setBusy(true); setError("");
    try { await addMeetingMessage(meeting.company_id, meeting.meeting_id, { actor_type: "CEO", actor_ref: "ceo", text: text.trim() }); onDraftSubmitted("text", text); await onReload(); }
    catch (cause) { setError(cause.message); } finally { setBusy(false); }
  };
  const formDecision = async () => {
    if (![proposal.summary, proposal.optionA, proposal.optionB].every((item) => item.trim())) return;
    setBusy(true); setError("");
    const unknown = { value: "当前会议没有可靠数据", provenance: "UNK" };
    try {
      await requestMeetingDecision(meeting.company_id, meeting.meeting_id, {
        decisionKey: `meeting-${meeting.meeting_id}-${Date.now()}`,
        complexity: "LOW_RISK",
        event: proposal.summary.trim(),
        cannotDecideReason: "两个方案存在业务取舍，需要CEO确认。",
        options: [proposal.optionA, proposal.optionB].map((label, index) => ({ optionId: `OPTION_${index + 1}`, label: label.trim(), impact: unknown, risk: unknown, cost: unknown })),
        recommendation: { optionId: "OPTION_1", provenance: "EST" },
        recommendationReason: { value: "推进负责人基于当前会议讨论提出，仍需CEO判断。", provenance: "EST" },
        ceoChoicePrompt: "请选择下一步方案",
        continuationPlan: proposal.optionA.trim(),
        evidenceRefs: meeting.context_refs.filter((item) => item.type === "EVIDENCE").map((item) => item.ref),
        workContract: { problem: proposal.summary.trim(), expectedResult: proposal.optionA.trim(), constraints: ["只使用会议已引用的事实"], references: meeting.context_refs.map((item) => item.ref) },
      });
      onDraftSubmitted("proposal", proposal); await onReload();
    } catch (cause) { setError(cause.message); } finally { setBusy(false); }
  };
  const endMeeting = async () => { setBusy(true); try { await closeMeeting(meeting.company_id, meeting.meeting_id); await onReload(); } catch (cause) { setError(cause.message); } finally { setBusy(false); } };
  const auxiliary = useMemo(() => {
    const continuation = meeting.background_continuation || {};
    return [{ id: JSON.stringify([meeting.company_id, meeting.meeting_id, "evidence"]), title: "依据与后续", content: <div className="space-y-4" aria-label="会议依据与后续责任"><section className="rounded-2xl border border-ui-line bg-ui-surface p-4"><h2 className="text-xs font-semibold text-ui-txt">会议上下文</h2><dl className="mt-3 space-y-3 text-xs"><div><dt className="text-ui-txt-3">CEO参与</dt><dd className="mt-1 text-ui-txt-2">{CEO_MODE[meeting.ceo_participation_mode]}</dd></div><div><dt className="text-ui-txt-3">工作空间</dt><dd className="mt-1"><Link className="text-ui-primary" href={workspaceEntryHref(meeting.workspace_id)}>查看相关工作空间</Link></dd></div><div><dt className="text-ui-txt-3">引用资料</dt><dd className="mt-1 text-ui-txt-2">{meeting.context_refs.length ? `${meeting.context_refs.length} 项真实引用` : "暂无引用"}</dd></div></dl></section>
      <section className="rounded-2xl border border-ui-line bg-ui-surface p-4"><h2 className="text-xs font-semibold text-ui-txt">工作与结果</h2><div className="mt-3 space-y-2">{meeting.works.length ? meeting.works.map((work) => <div key={work.entity_id} className="rounded-xl bg-ui-surface-2 p-3 text-xs"><Link className="font-semibold text-ui-primary" href={d1Href({ view: "work", workRef: work.entity_id, workspaceId: meeting.workspace_id }) + `&return_to=${encodeURIComponent(`/ceo-office/meeting?meeting=${encodeURIComponent(meeting.meeting_id)}`)}`}>{work.data?.contract?.problem || "会议决定形成的工作"}</Link><p className="mt-1 text-ui-txt-3">{(work.data?.responsibilityRouting || {}).status === "COMPLETED" ? "已完成" : "已交给负责员工"}</p></div>) : <p className="text-xs text-ui-txt-3">尚未形成工作。</p>}{meeting.results.map((result) => <div key={result.reference_id} className="rounded-xl border border-ui-line bg-ui-green-soft p-3 text-xs"><Link className="font-semibold text-ui-primary" href={d1Href({ view: "result", resultRef: result.reference_id, workspaceId: meeting.workspace_id }) + `&return_to=${encodeURIComponent(`/ceo-office/meeting?meeting=${encodeURIComponent(meeting.meeting_id)}`)}`}>{result.summary || "结果已返回"}</Link><p className="mt-1 text-ui-green">{result.kind || "RESULT"}</p></div>)}</div>{continuation.status === "AVAILABLE" ? <p className="mt-3 rounded-lg bg-ui-primary-soft px-3 py-2 text-xs leading-4 text-ui-primary">{CONTINUATION_STATE[continuation.state] || "团队状态暂时未知"}{continuation.reason ? `：${continuationReason(continuation.reason)}` : ""}</p> : <p className="mt-3 rounded-lg bg-ui-amber-soft px-3 py-2 text-xs leading-4 text-ui-amber">当前没有会议后台自动对话能力。已经形成的工作仍由负责员工推进。</p>}</section></div> }];
  }, [meeting]);
  return <><TerraPaneContent contextPane={contextPane} contextLabel="会议目录" initialContextOpen utilityTabs={auxiliary} utilityLabel="会议依据与责任" initialUtilityOpen /><div className="mx-auto max-w-[1100px]"><div className="flex flex-wrap items-start justify-between gap-4 border-b border-ui-line pb-4"><div><button onClick={onBack} className="text-xs font-semibold text-ui-primary">← 返回会议</button><div className="mt-3 flex items-center gap-3"><h1 className="text-2xl font-semibold tracking-[-.02em] text-ui-txt">{meeting.title}</h1><Badge state={meeting.operating_state} meeting={meeting} /></div><p className="mt-2 max-w-3xl text-xs leading-5 text-ui-txt-3">{meeting.background || "未补充会议背景"}</p></div><div className="flex gap-2"><button onClick={refresh} disabled={busy} className="rounded-lg border border-ui-line px-3 py-2 text-xs text-ui-txt-2">刷新进展</button>{meeting.status !== "closed" ? <button onClick={endMeeting} disabled={busy} className="rounded-lg border border-ui-line px-3 py-2 text-xs text-ui-txt-2">结束会议</button> : null}</div></div>
    <div className="mt-5 min-w-0"><main className="min-w-0 space-y-4"><div className="flex flex-wrap items-center gap-2">{meeting.participants_detail.map((item) => <span key={item.id} className="inline-flex items-center gap-2 rounded-full border border-ui-line bg-ui-surface py-1 pl-1 pr-3 text-xs text-ui-txt-2"><EmployeeAvatar employee={item} className="h-7 w-7" />{item.name} · {roleLabel(item.role)}{item.id === meeting.leader_employee_id ? " · 推进" : ""}</span>)}</div>
      {meeting.decision ? <DecisionPanel meeting={meeting} onRefresh={onReload} /> : null}
      <div className="[&>section>header]:hidden"><SharedConversation employee={meeting.leader} value={text} onChange={(value) => onDraftChange("text", value)} onSubmit={send} allowWithoutModel busy={busy} placeholder="继续讨论，或补充你掌握的事实…"><div className="space-y-4">{meeting.timeline.map((item) => <TimelineItem key={item.messageId} item={item} people={people} />)}</div></SharedConversation></div>
      {meeting.status !== "closed" && (!meeting.decision || meeting.decision.lifecycle_status === "APPLIED") ? <section className="rounded-2xl border border-ui-line bg-ui-surface p-4"><div><h2 className="text-sm font-semibold text-ui-txt">形成下一项决定</h2><p className="mt-1 text-xs text-ui-txt-3">把讨论收敛为两个真实选项。未知的影响、风险和代价会明确标记为未知。</p></div><input value={proposal.summary} onChange={(event) => onDraftChange("proposal", { ...proposal, summary: event.target.value })} placeholder="发生了什么，需要CEO决定什么？" className="mt-4 h-10 w-full rounded-lg border border-ui-line bg-ui-surface px-3 text-xs" /><div className="mt-2 grid gap-2 md:grid-cols-2"><input value={proposal.optionA} onChange={(event) => onDraftChange("proposal", { ...proposal, optionA: event.target.value })} placeholder="方案一（推进员工建议）" className="h-10 rounded-lg border border-ui-line bg-ui-surface px-3 text-xs" /><input value={proposal.optionB} onChange={(event) => onDraftChange("proposal", { ...proposal, optionB: event.target.value })} placeholder="方案二" className="h-10 rounded-lg border border-ui-line bg-ui-surface px-3 text-xs" /></div><button disabled={busy || !proposal.summary.trim() || !proposal.optionA.trim() || !proposal.optionB.trim()} onClick={formDecision} className="mt-3 rounded-lg bg-ui-primary px-4 py-2 text-xs font-semibold text-ui-primary-fg disabled:opacity-40">提交CEO决定</button></section> : null}
      {error ? <p role="alert" className="rounded-lg bg-ui-red-soft px-3 py-2 text-xs text-ui-red">{error}</p> : null}</main>
      </div>
  </div></>;
}

function MeetingSurface() {
  const runtime = useRuntime();
  const [state, setState] = useState({ companyId: "", status: "idle", meetings: { active: [], history: [] }, employees: [], businesses: [], knowledge: [], error: "" });
  const [selected, setSelected] = useState(null);
  const [overlay, setOverlay] = useState(false);
  const [query, setQuery] = useState("");
  const [busy, setBusy] = useState(false);
  const [formError, setFormError] = useState("");
  const [targetSection, setTargetSection] = useState("");
  const [drafts, setDrafts] = useState({});
  const readGeneration = useRef(0);
  const activeMeetingRef = useRef(selected);
  const activeCompanyRef = useRef(runtime.companyId);
  activeCompanyRef.current = runtime.companyId;
  const load = useCallback(async (meetingId) => {
    if (!runtime.companyId) return;
    const generation = ++readGeneration.current;
    setState((current) => ({ ...current, status: "loading", error: "" }));
    try {
      const meetings = await getMeetings(runtime.companyId);
      const employees = await getEmployees();
      const businesses = await getCanonicalBusinesses(runtime.companyId);
      const knowledge = await getKnowledgeEntries({ companyId: runtime.companyId, limit: 8 });
      const id = meetingId !== undefined
        ? meetingId
        : selected?.meeting_id || new URLSearchParams(window.location.search).get("meeting") || "";
      const detail = id ? await getMeeting(runtime.companyId, id) : null;
      if (generation !== readGeneration.current) return;
      if (detail && detail.company_id !== runtime.companyId) throw new Error("会议公司来源不一致");
      activeMeetingRef.current = detail;
      setSelected(detail);
      setState({ companyId: runtime.companyId, status: "ready", meetings, employees: (employees.employees || []).filter((employee) => employee.company_id === runtime.companyId), businesses: businesses.businesses || [], knowledge: knowledge.entries || [], error: "" });
    } catch (cause) { if (generation === readGeneration.current) setState((current) => ({ ...current, companyId: runtime.companyId, status: "error", error: runtimeErrorMessage(cause) })); }
  }, [runtime.companyId, selected?.meeting_id]);
  useEffect(() => { if (runtime.status === "ready") load(); return () => { readGeneration.current += 1; }; }, [runtime.status, runtime.companyId]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    if (!selected || selected.status === "closed") return undefined;
    const timer = window.setInterval(() => {
      if (activeCompanyRef.current === selected.company_id && activeMeetingRef.current?.company_id === selected.company_id && activeMeetingRef.current?.meeting_id === selected.meeting_id) load(selected.meeting_id);
    }, 5000);
    return () => window.clearInterval(timer);
  }, [selected?.meeting_id, selected?.status]); // eslint-disable-line react-hooks/exhaustive-deps
  const openMeeting = async (id) => { activeMeetingRef.current = { company_id: runtime.companyId, meeting_id: id }; window.history.replaceState(null, "", `?meeting=${encodeURIComponent(id)}`); await load(id); };
  const back = () => { activeMeetingRef.current = null; window.history.replaceState(null, "", window.location.pathname); setSelected(null); load(""); };
  useEffect(() => {
    if (!selected && targetSection) {
      document.getElementById(targetSection)?.scrollIntoView({ block: "start" });
      setTargetSection("");
    }
  }, [selected, targetSection]);
  const goToCollection = (section) => { setTargetSection(section); if (selected) back(); };
  const create = async (form) => {
    setBusy(true); setFormError("");
    try { const meeting = await createMeeting(runtime.companyId, form); setOverlay(false); activeMeetingRef.current = { company_id: runtime.companyId, meeting_id: meeting.meeting_id }; window.history.replaceState(null, "", `?meeting=${encodeURIComponent(meeting.meeting_id)}`); await load(meeting.meeting_id); }
    catch (cause) { setFormError(cause.message); } finally { setBusy(false); }
  };
  if (runtime.status === "loading" || state.status === "idle") return <RuntimeLoading label="正在读取会议…" />;
  if (runtime.status === "error" || runtime.status === "forbidden") return <RuntimeError message={runtime.error} onRetry={runtime.refresh} forbidden={runtime.status === "forbidden"} />;
  if (!runtime.companyId) return <RuntimeEmpty title="先建立公司" description="会议属于公司经营空间。建立公司后再召开会议。" />;
  if (state.status === "error") return <RuntimeError message={state.error} onRetry={() => load()} />;
  if (state.companyId !== runtime.companyId) return <RuntimeLoading label="正在读取当前公司的会议…" />;
  const context = <nav aria-label="会议目录" className="grid auto-rows-max content-start gap-2 text-sm">
    {[["active", "当前会议", "meeting-current"], ["history", "历史会议", "meeting-history"]].map(([kind, label, section]) => <section key={kind} className="grid auto-rows-max content-start gap-1">
      <button type="button" onClick={() => goToCollection(section)} className="rounded-ui-sm px-3 py-2 text-left font-semibold text-ui-txt hover:bg-ui-surface-2">{label} · {state.meetings[kind].length}</button>
      {state.meetings[kind].map((item) => <button key={item.meeting_id} type="button" onClick={() => openMeeting(item.meeting_id)}
        aria-current={selected?.meeting_id === item.meeting_id ? "page" : undefined}
        className={`truncate rounded-ui-sm px-4 py-2 text-left hover:bg-ui-surface-2 ${selected?.meeting_id === item.meeting_id ? "bg-ui-primary-light font-semibold text-ui-primary" : "text-ui-txt-2"}`}>{item.title}</button>)}
    </section>)}
  </nav>;
  if (selected) {
    const draftKey = JSON.stringify([selected.company_id, selected.meeting_id, "ceo"]);
    const draft = drafts[draftKey] || emptyMeetingDraft;
    const onDraftChange = (field, value) => setDrafts((current) => ({ ...current, [draftKey]: { ...emptyMeetingDraft, ...current[draftKey], [field]: value } }));
    const onDraftSubmitted = (field, submitted) => setDrafts((current) => {
      const saved = current[draftKey];
      if (!saved || (field === "text" ? saved.text !== submitted : Object.keys(emptyProposal).some((key) => saved.proposal[key] !== submitted[key]))) return current;
      const updated = { ...saved, [field]: field === "text" ? "" : emptyProposal };
      const next = { ...current };
      if (!updated.text && !Object.values(updated.proposal).some(Boolean)) delete next[draftKey];
      else next[draftKey] = updated;
      return next;
    });
    const reloadIfCurrent = () => activeCompanyRef.current === selected.company_id && activeMeetingRef.current?.company_id === selected.company_id && activeMeetingRef.current?.meeting_id === selected.meeting_id ? load(selected.meeting_id) : Promise.resolve();
    return <MeetingDetail key={JSON.stringify([selected.company_id, selected.meeting_id])} meeting={selected} onBack={back} onReload={reloadIfCurrent} contextPane={context} draft={draft} onDraftChange={onDraftChange} onDraftSubmitted={onDraftSubmitted} />;
  }
  const filter = (items) => items.filter((item) => !query.trim() || `${item.title} ${item.background}`.toLowerCase().includes(query.trim().toLowerCase()));
  return <><TerraPaneContent contextPane={context} contextLabel="会议目录" initialContextOpen /><div className="mx-auto max-w-[1180px]"><header className="flex flex-wrap items-end justify-between gap-4 border-b border-ui-line pb-4"><div><h1 className="text-2xl font-semibold tracking-[-.02em] text-ui-txt">会议</h1><p className="mt-2 text-xs text-ui-txt-3">团队讨论、CEO决定和工作结果在同一个会议中持续衔接。</p></div><button onClick={() => setOverlay(true)} className="rounded-lg bg-ui-primary px-4 py-2.5 text-xs font-semibold text-ui-primary-fg">召开会议</button></header>
    <div id="meeting-current" className="mt-5 flex items-center justify-between gap-3"><h2 className="text-sm font-semibold text-ui-txt">当前会议</h2><input aria-label="搜索会议议题" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="搜索议题" className="h-9 w-56 rounded-lg border border-ui-line bg-ui-surface px-3 text-xs outline-none focus:border-ui-primary" /></div>
    <div className="mt-3 divide-y divide-ui-line overflow-hidden rounded-2xl border border-ui-line bg-ui-surface">{filter(state.meetings.active).length ? filter(state.meetings.active).map((item) => <button key={item.meeting_id} onClick={() => openMeeting(item.meeting_id)} className="grid w-full items-center gap-3 px-5 py-4 text-left hover:bg-ui-surface-2 md:grid-cols-[minmax(0,1fr)_auto_auto]"><span className="min-w-0"><strong className="block truncate text-sm text-ui-txt">{item.title}</strong><span className="mt-1 block truncate text-xs text-ui-txt-3">{item.background || "暂无背景"} · {item.participants_detail.length} 位员工</span></span><Badge state={item.operating_state} meeting={item} /><span className="text-xs font-semibold text-ui-primary">进入会议 →</span></button>) : <div className="px-5 py-12 text-center"><h3 className="text-sm font-semibold text-ui-txt">当前没有进行中的会议</h3><p className="mt-2 text-xs text-ui-txt-3">遇到需要多人讨论或CEO判断的问题时，可以召开一次会议。</p></div>}</div>
    <section id="meeting-history" className="mt-8"><h2 className="text-sm font-semibold text-ui-txt">最近历史会议</h2><div className="mt-3 divide-y divide-ui-line border-y border-ui-line">{filter(state.meetings.history).length ? filter(state.meetings.history).map((item) => <button key={item.meeting_id} onClick={() => openMeeting(item.meeting_id)} className="grid w-full items-center gap-3 py-3 text-left md:grid-cols-[minmax(0,1fr)_160px_120px]"><span><strong className="block text-xs text-ui-txt-2">{item.title}</strong><span className="mt-1 block text-xs text-ui-txt-3">{item.results.length ? `${item.results.length} 项结果` : "暂无结果"}</span></span><span className="text-xs text-ui-txt-3">{item.participants_detail.map((person) => person.name).join("、")}</span><span className="text-right text-xs text-ui-txt-3">{item.closed_at ? new Date(item.closed_at).toLocaleDateString("zh-CN") : "时间未知"}</span></button>) : <p className="py-8 text-center text-xs text-ui-txt-3">暂无历史会议。</p>}</div></section>
    <MeetingOverlay open={overlay} onClose={() => { setOverlay(false); setFormError(""); }} onCreate={create} businesses={state.businesses} employees={state.employees} knowledge={state.knowledge} busy={busy} error={formError} />
  </div></>;
}

export default function MeetingPage() {
  return <TerraShell topCrumb="经营工具 / 会议"><MeetingSurface /></TerraShell>;
}
