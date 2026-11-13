"use client";

import Link from "next/link";
import { useCallback, useEffect, useMemo, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";

import { useAssistantPageContext } from "../assistant/GlobalAssistant.js";
import { CEO_ID } from "../../lib/api.js";
import {
  acceptRuntimeContentIdea,
  createRuntimeContentItem,
  createRuntimeContentVersion,
  decideRuntimeContentReview,
  getRuntimeWorkspace,
  runtimeErrorMessage,
} from "../../lib/runtimeApi.js";
import { useRuntime } from "../runtime/RuntimeProvider.js";
import TeamOperatingDefinitionEditor from "../workspace/TeamOperatingDefinitionEditor.js";
import WorkspacePaneShell from "../workspace/WorkspacePaneShell.js";

const WEEKDAYS = ["一", "二", "三", "四", "五", "六", "日"];
const CONTENT_LABEL = { IDEA: "想法", DRAFT: "草稿", IN_REVIEW: "审核中", APPROVED: "已通过", SCHEDULED: "已排期", PUBLISHED: "已发布", AWAITING_FEEDBACK: "等待反馈", REVIEWED: "已复盘" };

function dateKey(date) {
  return [date.getFullYear(), String(date.getMonth() + 1).padStart(2, "0"), String(date.getDate()).padStart(2, "0")].join("-");
}

function dateCells(month) {
  const first = new Date(month.getFullYear(), month.getMonth(), 1);
  const offset = (first.getDay() + 6) % 7;
  const start = new Date(month.getFullYear(), month.getMonth(), 1 - offset);
  return Array.from({ length: 42 }, (_, index) => {
    const day = new Date(start);
    day.setDate(start.getDate() + index);
    return day;
  });
}

function versionFor(note, versions) {
  return versions.find((version) => version.entity_id === note.current_version_id) || null;
}

function noteTitle(note, version) {
  return version?.data?.title || note.data?.intentRef || "未命名 Note";
}

function notePriority(note, selectedId) {
  if (note.lifecycle_status === "IN_REVIEW") return 0;
  if (note.entity_id === selectedId) return 1;
  if (note.lifecycle_status === "DRAFT") return 2;
  return 3;
}

function WorkContext({ note }) {
  const context = note.work_context;
  if (!context) return <section className="mt-4 rounded-ui-sm bg-ui-surface-2 p-3"><p className="text-ui-2 font-medium">当前还没有经过确认的员工责任</p><p className="mt-1 text-ui-1 leading-relaxed text-ui-txt-2">这条 Note 仍可编辑；安排员工后，系统才会显示真实负责人和执行者。</p></section>;
  const responsibility = context.current_responsibility;
  const executor = context.current_executor;
  const activity = context.system_activity;
  return <section className="mt-4 grid gap-3 rounded-ui-sm bg-ui-surface-2 p-3">
    <div><p className="text-ui-1 text-ui-txt-3">对象归属</p><p className="text-ui-2 font-medium">{context.object_owner.label}</p></div>
    {activity ? <div><p className="text-ui-1 text-ui-txt-3">系统活动</p><p className="text-ui-2 font-medium">{activity.label || activity.kind} · {activity.status}</p><p className="mt-1 text-ui-1 text-ui-txt-2">当前没有执行员工。</p></div> : responsibility?.employee ? <div><p className="text-ui-1 text-ui-txt-3">当前负责</p><p className="text-ui-2 font-medium">{responsibility.employee.data?.name || responsibility.employee.entity_id} · {responsibility.activity || "正在处理"}</p><p className="mt-1 text-ui-1 text-ui-txt-2">当前执行者：{executor?.employee?.data?.name || "暂无"} · {responsibility.status}</p></div> : <div><p className="text-ui-1 text-ui-txt-3">当前负责</p><p className="text-ui-2 text-ui-txt-2">暂无可用员工引用；不会以历史操作人或系统活动替代。</p></div>}
  </section>;
}

function HandoffEvent({ note, handoffs }) {
  const event = handoffs.find((item) => item.parent_id === note.entity_id);
  if (!event) return null;
  return <p className="mt-3 text-ui-1 text-ui-txt-2">交接已记录：{event.data?.fromEmployeeRef || "前一位员工"} → {event.data?.toEmployeeRef || "下一位员工"} · {event.lifecycle_status}</p>;
}

function PublishAndAnalyticsState({ note }) {
  const publication = note.publication;
  const analytics = note.analytics;
  if (!publication && !analytics) return null;
  return <section className="mt-4 grid gap-2 rounded-ui-sm bg-ui-surface-2 p-3">
    <div><p className="text-ui-1 text-ui-txt-3">发布</p><p className="text-ui-2 font-medium">{publication?.label || "尚未到发布阶段"}</p>{publication?.status === "WAITING_FOR_CAPABILITY" && <p className="mt-1 text-ui-1 text-ui-txt-2">当前没有已验证的发布能力；不会代替你发布，也不会生成平台回执。</p>}</div>
    <div><p className="text-ui-1 text-ui-txt-3">数据回流</p><p className="text-ui-2 font-medium">{analytics?.label || "暂无数据"}</p><p className="mt-1 text-ui-1 text-ui-txt-2">没有已验证的数据来源时，不显示浏览、点赞或互动趋势。</p></div>
  </section>;
}

function SourceMark({ value }) {
  return <span className="ml-1 text-ui-1 text-ui-txt-3">({value || "UNK"})</span>;
}

function DecisionGate({ workspace, note, decisions, onChanged }) {
  const decision = decisions.find((item) => item.parent_id === note.entity_id && item.lifecycle_status === "WAITING_CEO");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [showPackage, setShowPackage] = useState(false);
  if (note.lifecycle_status !== "IN_REVIEW" || !decision) return null;
  const plainPackage = decision.data?.plainPackage;
  const conversation = decision.data?.conversation;
  const reviewer = note.work_context?.current_responsibility?.employee?.data?.name || "当前审核员工";
  async function decide(choice) {
    setSaving(true);
    setError("");
    try {
      await decideRuntimeContentReview(workspace.workspace_id, note.entity_id, { ceo_id: CEO_ID, choice, reason: "CEO 已在当前 Note 的审核决策中作出选择" });
      onChanged();
    } catch (requestError) {
      setError(runtimeErrorMessage(requestError));
    } finally {
      setSaving(false);
    }
  }
  return <section className="mt-4 grid gap-3">
    <section className="rounded-ui-sm bg-ui-surface-2 p-3">
      <p className="text-ui-1 text-ui-txt-3">{reviewer} 的汇报</p>
      <p className="mt-1 text-ui-2 leading-relaxed text-ui-txt">{conversation?.message || "这篇内容正在等待你的判断。"}</p>
      <button type="button" onClick={() => setShowPackage(true)} className="mt-2 text-ui-1 font-semibold text-ui-accent">⚠ 等待你的决定 · 查看决策方案 ▸</button>
    </section>
    <section className="rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3">
      <p className="text-ui-2 font-semibold">需要 CEO 决策</p><p className="mt-1 text-ui-1 leading-relaxed text-ui-txt-2">审核已完成。你的选择会由 Runtime 自动继续处理，不会把 CEO 变成流程的下一步执行者。</p>
      {plainPackage ? <div className="mt-3 flex flex-wrap gap-2"><button type="button" disabled={saving} onClick={() => decide("APPROVE")} className="rounded-ui-sm bg-ui-action-primary-bg px-3 py-2 text-ui-2 font-semibold text-ui-action-primary-fg disabled:opacity-50">按建议处理</button><button type="button" disabled={saving} onClick={() => setShowPackage(true)} className="rounded-ui-sm border border-ui-line px-3 py-2 text-ui-2 font-semibold text-ui-txt disabled:opacity-50">其他方案</button><button type="button" disabled={saving} onClick={() => decide("DEFER")} className="rounded-ui-sm border border-ui-line px-3 py-2 text-ui-2 font-semibold text-ui-txt disabled:opacity-50">暂缓</button></div> : <button type="button" onClick={() => setShowPackage(true)} className="mt-3 rounded-ui-sm border border-ui-line px-3 py-2 text-ui-2 font-semibold text-ui-txt">查看方案</button>}
      {showPackage && (plainPackage ? <div className="mt-4 grid gap-3 border-t border-ui-line pt-3">
        <div className="grid gap-1"><p className="text-ui-1 text-ui-txt-3">发生了什么</p><p className="text-ui-2">{plainPackage.happened?.text}<SourceMark value={plainPackage.happened?.source} /></p><p className="text-ui-2 text-ui-txt-2">{plainPackage.cannotAutoDecide?.text}<SourceMark value={plainPackage.cannotAutoDecide?.source} /></p></div>
        <div className="grid gap-2">{(plainPackage.options || []).map((option) => <div key={option.key} className="rounded-ui-sm border border-ui-line bg-ui-bg p-3"><div className="flex flex-wrap items-center justify-between gap-2"><p className="text-ui-2 font-semibold">{option.label}</p><button type="button" disabled={saving} onClick={() => decide(option.key)} className="rounded-ui-sm border border-ui-line px-2 py-1 text-ui-1 font-semibold text-ui-txt disabled:opacity-50">选择</button></div><p className="mt-2 text-ui-1 text-ui-txt-2">影响：{option.impact?.text}<SourceMark value={option.impact?.source} /></p><p className="mt-1 text-ui-1 text-ui-txt-2">风险：{option.risk?.text}<SourceMark value={option.risk?.source} /></p><p className="mt-1 text-ui-1 text-ui-txt-2">代价：{option.cost?.text}<SourceMark value={option.cost?.source} /></p><p className="mt-1 text-ui-1 text-ui-txt-2">选择后：{option.continuation?.text}<SourceMark value={option.continuation?.source} /></p></div>)}</div>
        <p className="text-ui-2">员工建议：{plainPackage.recommendation?.text}<SourceMark value={plainPackage.recommendation?.source} /></p><p className="text-ui-1 text-ui-txt-2">建议理由：{plainPackage.recommendationReason?.text}<SourceMark value={plainPackage.recommendationReason?.source} /></p>
      </div> : <p className="mt-4 border-t border-ui-line pt-3 text-ui-2 text-ui-txt-2">这是一条旧的决策记录，尚未保存可读方案；不会补写或猜测影响、风险与建议。</p>)}
    </section>
    {error && <p role="alert" className="mt-3 text-ui-2 text-ui-red">{error}</p>}
  </section>;
}

function Calendar({ notes, versions, month, selectedId, onSelect, onChangeMonth }) {
  const byDate = useMemo(() => notes.reduce((groups, note) => {
    const scheduledFor = versionFor(note, versions)?.data?.scheduledFor;
    if (!scheduledFor) return groups;
    groups[scheduledFor] = [...(groups[scheduledFor] || []), note].sort((left, right) => notePriority(left, selectedId) - notePriority(right, selectedId));
    return groups;
  }, {}), [notes, selectedId, versions]);
  const today = dateKey(new Date());

  return <section className="rounded-ui-md border border-ui-line bg-ui-surface">
    <header className="flex flex-wrap items-center justify-between gap-3 border-b border-ui-line px-4 py-3">
      <div><p className="text-ui-1 font-medium text-ui-txt-3">Publishing Calendar</p><h1 className="mt-1 text-ui-5 font-semibold">{month.getFullYear()} 年 {month.getMonth() + 1} 月</h1></div>
      <div className="flex gap-2"><button type="button" onClick={() => onChangeMonth(-1)} className="rounded-ui-sm border border-ui-line px-3 py-2 text-ui-2">上月</button><button type="button" onClick={() => onChangeMonth(1)} className="rounded-ui-sm border border-ui-line px-3 py-2 text-ui-2">下月</button></div>
    </header>
    <div className="grid grid-cols-7 border-b border-ui-line bg-ui-surface-2">{WEEKDAYS.map((label) => <div key={label} className="px-2 py-2 text-center text-ui-1 font-semibold text-ui-txt-3">周{label}</div>)}</div>
    <div className="grid grid-cols-7">{dateCells(month).map((day) => {
      const key = dateKey(day);
      const items = byDate[key] || [];
      return <div key={key} className={`min-h-28 border-b border-r border-ui-line p-2 ${day.getMonth() === month.getMonth() ? "bg-ui-surface" : "bg-ui-surface-2 text-ui-txt-3"}`}>
        <p className={`text-ui-1 ${key === today ? "font-semibold text-ui-accent" : ""}`}>{day.getDate()}</p>
        <div className="mt-2 grid gap-1">{items.slice(0, 3).map((note) => {
          const version = versionFor(note, versions);
          const selected = note.entity_id === selectedId;
          return <button key={note.entity_id} type="button" onClick={() => onSelect(note.entity_id)} className={`truncate rounded-ui-sm px-2 py-1 text-left text-ui-1 ${selected ? "bg-ui-primary-soft text-ui-primary" : "bg-ui-surface-2 text-ui-txt hover:bg-ui-primary-soft"}`} title={noteTitle(note, version)}>{noteTitle(note, version)}</button>;
        })}</div>
        {items.length > 3 && <button type="button" onClick={() => onSelect(items[0].entity_id)} className="mt-1 text-ui-1 font-medium text-ui-accent">+{items.length - 3} 篇</button>}
      </div>;
    })}</div>
  </section>;
}

function NoteComposer({ workspace, onCreated }) {
  const [title, setTitle] = useState("");
  const [scheduledFor, setScheduledFor] = useState(dateKey(new Date()));
  const [body, setBody] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  async function submit(event) {
    event.preventDefault();
    if (!title.trim() || !scheduledFor) return;
    setSaving(true);
    setError("");
    try {
      const created = await createRuntimeContentItem(workspace.workspace_id, {
        ceo_id: CEO_ID, owner_ref: workspace.workspace_id, outcome_ref: title.trim(), intent_ref: title.trim(), blueprint_version: workspace.blueprint_version,
        platform: "XHS", platform_variant: "图文", payload_ref: "CEO 手动创建的 Note 草稿", author: "CEO", constraints_check: "尚未审核",
        title: title.trim(), body: body.trim(), scheduled_for: scheduledFor,
      });
      setTitle("");
      setBody("");
      onCreated(created.content_item.entity_id);
    } catch (requestError) {
      setError(runtimeErrorMessage(requestError));
    } finally {
      setSaving(false);
    }
  }

  return <section className="rounded-ui-md border border-ui-line bg-ui-surface p-4">
    <h2 className="text-ui-3 font-semibold">新建一条 Note</h2><p className="mt-1 text-ui-2 text-ui-txt-2">先保存真实内容意图与排期；不会创建固定任务、员工、发布回执或数据结果。</p>
    <form onSubmit={submit} className="mt-4 grid gap-3 md:grid-cols-[1fr_180px_auto]">
      <label className="grid gap-1 text-ui-1 font-medium text-ui-txt-2">标题<input required value={title} onChange={(event) => setTitle(event.target.value)} className="rounded-ui-sm border border-ui-line bg-ui-bg px-3 py-2 text-ui-2 text-ui-txt" placeholder="这条内容想表达什么" /></label>
      <label className="grid gap-1 text-ui-1 font-medium text-ui-txt-2">排期<input required type="date" value={scheduledFor} onChange={(event) => setScheduledFor(event.target.value)} className="rounded-ui-sm border border-ui-line bg-ui-bg px-3 py-2 text-ui-2 text-ui-txt" /></label>
      <button disabled={saving} className="self-end rounded-ui-sm bg-ui-action-primary-bg px-4 py-2 text-ui-2 font-semibold text-ui-action-primary-fg disabled:opacity-50">{saving ? "正在保存…" : "保存 Note"}</button>
      <label className="grid gap-1 md:col-span-3 text-ui-1 font-medium text-ui-txt-2">草稿说明（可选）<textarea value={body} onChange={(event) => setBody(event.target.value)} rows={2} className="resize-y rounded-ui-sm border border-ui-line bg-ui-bg px-3 py-2 text-ui-2 text-ui-txt" placeholder="保存为当前 Note 的初始版本，不会代替审核或发布。" /></label>
    </form>
    {error && <p role="alert" className="mt-3 text-ui-2 text-ui-red">{error}</p>}
  </section>;
}

function NoteSplit({ workspace, note, version, handoffs, decisions, onChanged }) {
  const [title, setTitle] = useState(version?.data?.title || "");
  const [body, setBody] = useState(version?.data?.body || "");
  const [tags, setTags] = useState((version?.data?.tags || []).join("，"));
  const [scheduledFor, setScheduledFor] = useState(version?.data?.scheduledFor || "");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const editable = note.lifecycle_status === "DRAFT";

  useEffect(() => {
    setTitle(version?.data?.title || "");
    setBody(version?.data?.body || "");
    setTags((version?.data?.tags || []).join("，"));
    setScheduledFor(version?.data?.scheduledFor || "");
  }, [version]);

  async function acceptIdea() {
    setSaving(true);
    setError("");
    try {
      await acceptRuntimeContentIdea(workspace.workspace_id, note.entity_id, { ceo_id: CEO_ID });
      onChanged();
    } catch (requestError) {
      setError(runtimeErrorMessage(requestError));
    } finally {
      setSaving(false);
    }
  }

  async function saveVersion(event) {
    event.preventDefault();
    setSaving(true);
    setError("");
    try {
      await createRuntimeContentVersion(workspace.workspace_id, note.entity_id, {
        ceo_id: CEO_ID, platform_variant: version?.data?.platformVariant || "图文", payload_ref: "CEO 手动编辑的 Note 草稿", author: "CEO", constraints_check: "尚未审核",
        title: title.trim(), body: body.trim(), tags: tags.split(/[，,]/).map((item) => item.trim()).filter(Boolean), cover_ref: version?.data?.coverRef || "", scheduled_for: scheduledFor || null,
      });
      onChanged();
    } catch (requestError) {
      setError(runtimeErrorMessage(requestError));
    } finally {
      setSaving(false);
    }
  }

  return <section className="rounded-ui-md border border-ui-line bg-ui-surface p-4">
    <div className="flex flex-wrap items-start justify-between gap-3"><div><p className="text-ui-1 text-ui-txt-3">Calendar → Note</p><h2 className="mt-1 text-ui-4 font-semibold">{noteTitle(note, version)}</h2></div><span className="rounded-ui-sm bg-ui-surface-2 px-2 py-1 text-ui-1 font-medium text-ui-txt-2">{CONTENT_LABEL[note.lifecycle_status] || note.lifecycle_status}</span></div>
    <WorkContext note={note} />
    <HandoffEvent note={note} handoffs={handoffs} />
    <DecisionGate workspace={workspace} note={note} decisions={decisions} onChanged={onChanged} />
    <PublishAndAnalyticsState note={note} />
    {note.lifecycle_status === "IDEA" && <div className="mt-4 rounded-ui-sm bg-ui-surface-2 p-3"><p className="text-ui-2 leading-relaxed text-ui-txt-2">这条内容意图已保存，尚未开始编辑。确认后才会进入草稿状态；不会自动提交审核或发布。</p><button type="button" disabled={saving} onClick={acceptIdea} className="mt-3 rounded-ui-sm bg-ui-action-primary-bg px-3 py-2 text-ui-2 font-semibold text-ui-action-primary-fg disabled:opacity-50">开始起草</button></div>}
    {editable && <form onSubmit={saveVersion} className="mt-4 grid gap-3"><label className="grid gap-1 text-ui-1 font-medium text-ui-txt-2">标题<input required value={title} onChange={(event) => setTitle(event.target.value)} className="rounded-ui-sm border border-ui-line bg-ui-bg px-3 py-2 text-ui-2 text-ui-txt" /></label><label className="grid gap-1 text-ui-1 font-medium text-ui-txt-2">正文<textarea value={body} onChange={(event) => setBody(event.target.value)} rows={8} className="resize-y rounded-ui-sm border border-ui-line bg-ui-bg px-3 py-2 text-ui-2 text-ui-txt" /></label><div className="grid gap-3 sm:grid-cols-2"><label className="grid gap-1 text-ui-1 font-medium text-ui-txt-2">标签<input value={tags} onChange={(event) => setTags(event.target.value)} className="rounded-ui-sm border border-ui-line bg-ui-bg px-3 py-2 text-ui-2 text-ui-txt" placeholder="以逗号分隔" /></label><label className="grid gap-1 text-ui-1 font-medium text-ui-txt-2">排期<input type="date" value={scheduledFor} onChange={(event) => setScheduledFor(event.target.value)} className="rounded-ui-sm border border-ui-line bg-ui-bg px-3 py-2 text-ui-2 text-ui-txt" /></label></div><button disabled={saving || !title.trim()} className="justify-self-start rounded-ui-sm border border-ui-line px-3 py-2 text-ui-2 font-semibold text-ui-txt disabled:opacity-50">{saving ? "正在保存版本…" : "保存新版本"}</button></form>}
    {!editable && note.lifecycle_status !== "IDEA" && <p className="mt-4 text-ui-2 leading-relaxed text-ui-txt-2">当前阶段不允许改写这条 Note。审核、CEO 决策、发布和数据反馈会在后续 Runtime 阶段接入。</p>}
    {error && <p role="alert" className="mt-3 text-ui-2 text-ui-red">{error}</p>}
  </section>;
}

function Preview({ note, version }) {
  return <div className="grid gap-3"><div><p className="text-ui-1 text-ui-txt-3">当前预览</p><h2 className="mt-1 text-ui-3 font-semibold">{noteTitle(note, version)}</h2></div><p className="whitespace-pre-wrap text-ui-2 leading-relaxed text-ui-txt-2">{version?.data?.body || "这条 Note 尚未填写正文。"}</p>{(version?.data?.tags || []).length > 0 && <p className="text-ui-1 text-ui-txt-3">{version.data.tags.map((tag) => `#${tag}`).join(" ")}</p>}<p className="text-ui-1 leading-relaxed text-ui-txt-3">预览只读取当前保存版本；不会生成封面、发布回执或平台数据。</p></div>;
}

function SignalContext({ note }) {
  return <div className="grid gap-3"><div><p className="text-ui-1 text-ui-txt-3">当前 Note</p><p className="mt-1 text-ui-2 font-semibold">{note.data?.intentRef || "尚未填写内容意图"}</p></div><div><p className="text-ui-1 text-ui-txt-3">选题信号</p><p className="mt-1 text-ui-2 leading-relaxed text-ui-txt-2">尚未连接可验证的信号来源；这里不会显示示例趋势或伪造选题。</p></div><p className="text-ui-1 leading-relaxed text-ui-txt-3">连接资料或数据能力后，信号会作为当前 Note 的上下文出现。</p></div>;
}

export default function XhsWorkspacePhaseOne() {
  const runtime = useRuntime();
  const router = useRouter();
  const searchParams = useSearchParams();
  const requestedId = searchParams.get("workspace_id") || "";
  const selectedNoteId = searchParams.get("note_id") || "";
  const [detail, setDetail] = useState(null);
  const [detailStatus, setDetailStatus] = useState("idle");
  const [detailError, setDetailError] = useState("");
  const [month, setMonth] = useState(() => new Date(new Date().getFullYear(), new Date().getMonth(), 1));
  const knownWorkspaces = runtime.snapshot?.workspaces || [];
  const workspaceId = requestedId || "";
  const knownWorkspace = knownWorkspaces.find((item) => item.workspace_id === workspaceId);
  const workspace = detail?.workspace?.business_type === "XHS" ? detail.workspace : null;
  const isForbidden = Boolean(workspaceId && runtime.status === "ready" && !knownWorkspace);
  const isWrongType = Boolean(detail?.workspace && detail.workspace.business_type !== "XHS");

  const load = useCallback(async () => {
    if (!workspaceId || !runtime.companyId) return;
    setDetailStatus("loading");
    setDetailError("");
    try {
      setDetail(await getRuntimeWorkspace(runtime.companyId, workspaceId));
      setDetailStatus("ready");
    } catch (error) {
      setDetail(null);
      setDetailStatus("error");
      setDetailError(runtimeErrorMessage(error));
    }
  }, [runtime.companyId, workspaceId]);

  useEffect(() => { load(); }, [load]);
  useAssistantPageContext({ page: "workspace", company_id: runtime.companyId, workspace_id: workspaceId, business_type: "XHS", cycle_id: "", content_id: selectedNoteId });

  const notes = detail?.content_items || [];
  const versions = detail?.content_versions || [];
  const selectedNote = notes.find((item) => item.entity_id === selectedNoteId) || null;
  const selectedVersion = selectedNote ? versionFor(selectedNote, versions) : null;
  const handoffs = detail?.handoffs || [];
  const decisions = detail?.decisions || [];
  const chooseNote = (noteId) => router.push(`/ceo-office/workspace/xhs?workspace_id=${encodeURIComponent(workspaceId)}&note_id=${encodeURIComponent(noteId)}`);
  const refreshDetail = async () => { await load(); runtime.refresh(); };

  let main;
  if (runtime.status === "idle" || runtime.status === "loading") main = <p className="text-ui-2 text-ui-txt-2">正在读取小红书运营办公室…</p>;
  else if (runtime.status === "error") main = <section className="max-w-2xl rounded-ui-md border border-ui-line bg-ui-surface p-5"><h1 className="text-ui-5 font-semibold">暂时无法读取运营办公室</h1><p className="mt-2 text-ui-2 text-ui-txt-2">{runtime.error}</p><button type="button" onClick={runtime.refresh} className="mt-4 rounded-ui-sm bg-ui-action-primary-bg px-3 py-2 text-ui-2 font-semibold text-ui-action-primary-fg">重新读取</button></section>;
  else if (!runtime.snapshot?.company) main = <section className="max-w-2xl rounded-ui-md border border-ui-line bg-ui-surface p-5"><h1 className="text-ui-5 font-semibold">先建立公司，再搭建运营办公室</h1><p className="mt-2 text-ui-2 leading-relaxed text-ui-txt-2">小红书 Workspace 只会属于已建立的公司；这里不会创建示例办公室。</p><Link href="/onboarding" className="mt-4 inline-flex min-h-8 items-center rounded-ui-sm bg-ui-action-primary-bg px-3 py-2 text-ui-2 font-semibold text-ui-action-primary-fg no-underline">继续创建公司</Link></section>;
  else if (isForbidden) main = <section className="max-w-2xl rounded-ui-md border border-ui-line bg-ui-surface p-5"><h1 className="text-ui-5 font-semibold">当前公司没有这个运营办公室</h1><p className="mt-2 text-ui-2 leading-relaxed text-ui-txt-2">没有读取或创建其他公司的数据。请从工作空间入口选择正确的办公室。</p><Link href="/ceo-office/workspace" className="mt-4 inline-flex min-h-8 items-center rounded-ui-sm border border-ui-line px-3 py-2 text-ui-2 font-semibold text-ui-txt no-underline">返回工作空间</Link></section>;
  else if (detailStatus === "loading" || detailStatus === "idle") main = <p className="text-ui-2 text-ui-txt-2">正在读取这个运营办公室…</p>;
  else if (detailStatus === "error") main = <section className="max-w-2xl rounded-ui-md border border-ui-line bg-ui-surface p-5"><h1 className="text-ui-5 font-semibold">暂时无法读取这个运营办公室</h1><p className="mt-2 text-ui-2 text-ui-txt-2">{detailError}</p><button type="button" onClick={load} className="mt-4 rounded-ui-sm bg-ui-action-primary-bg px-3 py-2 text-ui-2 font-semibold text-ui-action-primary-fg">重新读取</button></section>;
  else if (isWrongType) main = <section className="max-w-2xl rounded-ui-md border border-ui-line bg-ui-surface p-5"><h1 className="text-ui-5 font-semibold">这不是小红书运营办公室</h1><p className="mt-2 text-ui-2 leading-relaxed text-ui-txt-2">没有将其他业务的对象解释为小红书 Note。请从工作空间入口选择正确的办公室。</p><Link href="/ceo-office/workspace" className="mt-4 inline-flex min-h-8 items-center rounded-ui-sm border border-ui-line px-3 py-2 text-ui-2 font-semibold text-ui-txt no-underline">返回工作空间</Link></section>;
  else if (!workspace) main = <section className="max-w-2xl rounded-ui-md border border-ui-line bg-ui-surface p-5"><h1 className="text-ui-5 font-semibold">还没有小红书运营办公室</h1><p className="mt-2 text-ui-2 leading-relaxed text-ui-txt-2">可以先从工作空间入口选择模板并搭建业务目标；能力缺口不会伪装成已在运行。</p><Link href="/ceo-office/workspace" className="mt-4 inline-flex min-h-8 items-center rounded-ui-sm border border-ui-line px-3 py-2 text-ui-2 font-semibold text-ui-txt no-underline">打开工作空间</Link></section>;
  else main = <div className="grid gap-5"><TeamOperatingDefinitionEditor companyId={runtime.companyId} workspaceId={workspaceId} /><Calendar notes={notes} versions={versions} month={month} selectedId={selectedNoteId} onSelect={chooseNote} onChangeMonth={(step) => setMonth((current) => new Date(current.getFullYear(), current.getMonth() + step, 1))} /><NoteComposer workspace={workspace} onCreated={async (noteId) => { await refreshDetail(); chooseNote(noteId); }} />{selectedNote ? <NoteSplit workspace={workspace} note={selectedNote} version={selectedVersion} handoffs={handoffs} decisions={decisions} onChanged={refreshDetail} /> : <section className="rounded-ui-md border border-ui-line bg-ui-surface p-4"><h2 className="text-ui-3 font-semibold">选择一条 Note 开始工作</h2><p className="mt-1 text-ui-2 text-ui-txt-2">日历只显示已保存的排期内容；没有内容时不会填充示例卡片。</p></section>}</div>;

  return <WorkspacePaneShell workspaceId={workspaceId} breadcrumb="业务空间 / 小红书运营办公室" contextAvailable={Boolean(selectedNote)} contextPane={selectedNote ? <SignalContext note={selectedNote} /> : null} utilityAvailable={Boolean(selectedNote && selectedVersion)} utilityPane={selectedNote ? <Preview note={selectedNote} version={selectedVersion} /> : null}>{main}</WorkspacePaneShell>;
}
