"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";

import { useAssistantPageContext } from "../assistant/GlobalAssistant.js";
import { CEO_ID, getProjects, getTask } from "../../lib/api.js";
import {
  createArtifactReview,
  createResponsibilityHandoff,
  executeOperatingCycle,
  executeArtifactReview,
  getRuntimeWorkspace,
  chooseRDDecision,
  reviewRDDecision,
  runtimeErrorMessage,
  sendResponsibilityHandoff,
  startOperatingCycle,
} from "../../lib/runtimeApi.js";
import { useRuntime } from "../runtime/RuntimeProvider.js";
import WorkspacePaneShell from "../workspace/WorkspacePaneShell.js";
import RdArtifactReview from "./RdArtifactReview.js";
import RdDecisionPackage from "./RdDecisionPackage.js";
import RdRealExecutionComposer from "./RdRealExecutionComposer.js";
import RdResponsibilityHandoff from "./RdResponsibilityHandoff.js";

const STATUS = {
  PLANNED: ["waiting", "待准备"],
  READY: ["waiting", "可以开始"],
  RUNNING: ["working", "工作中"],
  COMPLETED: ["completed", "已完成"],
  FAILED: ["failed", "需要处理"],
};

const STATUS_CLASS = {
  working: "text-ui-success",
  waiting: "text-ui-txt-3",
  completed: "text-ui-success",
  failed: "text-ui-red",
  idle: "text-ui-txt-3",
};

function employeeByRef(detail, ref) {
  return (detail?.employees || []).find((item) => item.entity_id === ref) || null;
}

function employeePresentation(employee, detail) {
  const runtimeName = employee?.data?.name || "";
  const role = (detail?.role_slots || []).find((item) => item.entity_id === employee?.data?.roleSlotRef);
  return {
    name: runtimeName === "Engineering AI" ? "研发员工" : runtimeName || "待分配员工",
    role: role?.data?.name || "研发员工",
  };
}

function taskArtifact(task) {
  const artifact = (task?.artifacts || []).find((item) => item.artifact_type === "code_change");
  if (!artifact?.content) return null;
  try {
    return { ...artifact, payload: JSON.parse(artifact.content) };
  } catch {
    return null;
  }
}

function reviewArtifact(task) {
  return (task?.artifacts || []).find((item) => item.artifact_type === "artifact_review") || null;
}

function responsibilityState(cycle) {
  const execution = cycle?.data?.executionStatus || "PLANNED";
  return STATUS[execution] || ["idle", execution || "尚未开始"];
}

function Fact({ label, value }) {
  return <div><dt className="text-ui-1 text-ui-txt-3">{label}</dt><dd className="mt-1 break-words text-ui-2 text-ui-txt">{value || "未记录"}</dd></div>;
}

function accessCopy(access) {
  const requested = access?.requested_intent === "AUTO_WITHIN_BOUNDARY" ? "自动处理" : "按当前设置处理";
  const configured = access?.configured_state === "CONFIGURED" ? "已按允许范围配置" : "尚未完成配置";
  const effective = access?.effective_state === "UNKNOWN" ? "当前无法由服务方确认" : access?.effective_state || "当前无法确认";
  return { requested, configured, effective };
}

function RdContext({ project, cycle }) {
  if (!cycle) return <p className="text-ui-2 text-ui-txt-2">选择一项研发工作后查看项目背景。</p>;
  const hasResult = Boolean((cycle.data?.resultRefs || []).length);
  return <div className="grid gap-5">
    <section>
      <p className="text-ui-1 text-ui-txt-3">项目背景</p>
      <h2 className="mt-1 text-ui-3 font-semibold">{project?.name || cycle.data?.projectRef || "项目读取中"}</h2>
      <p className="mt-2 text-ui-2 leading-relaxed text-ui-txt-2">{project?.goal || cycle.data?.outcomeRef}</p>
    </section>
    <section className="border-t border-ui-line pt-4">
      <p className="text-ui-1 text-ui-txt-3">当前工作</p>
      <p className="mt-1 text-ui-2 font-medium">{cycle.data?.workItemName}</p>
      <p className="mt-2 text-ui-1 leading-relaxed text-ui-txt-2">{cycle.data?.instruction}</p>
    </section>
    <section className="border-t border-ui-line pt-4">
      <p className="text-ui-1 text-ui-txt-3">相关文件</p>
      {(cycle.data?.resourceRefs || []).length ? <ul className="mt-2 grid gap-2">{cycle.data.resourceRefs.map((ref) => <li key={ref} className="rounded-ui-sm bg-ui-surface px-2 py-1.5 font-mono text-ui-1 text-ui-txt-2">{ref}</li>)}</ul> : <p className="mt-2 text-ui-2 text-ui-txt-2">未声明文件范围。</p>}
    </section>
    <section className="border-t border-ui-line pt-4">
      <p className="text-ui-1 text-ui-txt-3">已有结果</p>
      <p className="mt-2 text-ui-2 text-ui-txt-2">{hasResult ? "代码变化与验证证据已保存，可从右侧证据面查看。" : "这项工作还没有形成可验证结果。"}</p>
    </section>
    <details className="border-t border-ui-line pt-4 text-ui-1 text-ui-txt-2">
      <summary className="cursor-pointer font-semibold">查看技术引用</summary>
      <dl className="mt-3 grid gap-3">
        <Fact label="Cycle ID" value={cycle.entity_id} />
        <Fact label="Task ID" value={cycle.data?.taskRef} />
        <Fact label="Evidence ID" value={(cycle.data?.evidenceRefs || []).join(" · ")} />
      </dl>
    </details>
  </div>;
}

function DiffView({ diff }) {
  if (!diff) return <p className="text-ui-2 text-ui-txt-2">当前 Artifact 没有可读取的文件差异。</p>;
  return <pre className="overflow-x-auto rounded-ui-sm bg-ui-bg p-3 font-mono text-ui-1 leading-relaxed">{diff.split("\n").map((line, index) => {
    const tone = line.startsWith("+") && !line.startsWith("+++") ? "text-ui-success" : line.startsWith("-") && !line.startsWith("---") ? "text-ui-red" : "text-ui-txt-2";
    return <span key={`${index}-${line}`} className={`block whitespace-pre ${tone}`}>{line || " "}</span>;
  })}</pre>;
}

function RdUtility({ cycle, task, reviewTask, mode, onMode }) {
  const artifact = taskArtifact(task);
  const reviewResult = reviewArtifact(reviewTask);
  const payload = artifact?.payload;
  const access = accessCopy(cycle?.data?.computerAccess);
  if (!cycle?.data?.taskRef) return <p className="text-ui-2 text-ui-txt-2">研发员工完成或尝试执行后，代码变化与验证证据会出现在这里。</p>;
  return <div className="grid gap-4">
    <div className="flex flex-wrap gap-2" role="tablist" aria-label="研发结果模式">
      {[["diff", "代码变化"], ["test", "测试结果"], ...(cycle.data?.artifactReview ? [["review", "审核结果"]] : []), ["meta", "执行详情"]].map(([value, label]) => <button key={value} type="button" role="tab" aria-selected={mode === value} onClick={() => onMode(value)} className={`rounded-ui-sm px-2.5 py-1.5 text-ui-1 font-semibold ${mode === value ? "bg-ui-action-primary-bg text-ui-action-primary-fg" : "border border-ui-line text-ui-txt-2"}`}>{label}</button>)}
    </div>
    {mode === "diff" && <section><p className="mb-2 text-ui-1 text-ui-txt-3">{(payload?.changedFiles || cycle.data?.changedFiles || []).join(" · ") || "尚无文件变化"}</p><DiffView diff={payload?.diff} /></section>}
    {mode === "test" && <section className="grid gap-3"><Fact label="验证结果" value={(payload?.testResult?.exitCode ?? cycle.data?.testResult?.exitCode) === 0 ? "测试通过" : (payload?.testResult?.exitCode ?? cycle.data?.testResult?.exitCode) == null ? "尚未运行" : "测试未通过"} /><details className="text-ui-1 text-ui-txt-2"><summary className="cursor-pointer font-semibold">查看测试详情</summary><dl className="mt-3 grid gap-3"><Fact label="验证命令" value={(payload?.testResult?.command || cycle.data?.testResult?.command || []).join(" ")} /><Fact label="退出码" value={String(payload?.testResult?.exitCode ?? cycle.data?.testResult?.exitCode ?? "未运行")} /></dl>{payload?.testResult?.stdout && <pre className="mt-3 overflow-x-auto rounded-ui-sm bg-ui-bg p-3 font-mono text-ui-1 text-ui-txt-2">{payload.testResult.stdout}</pre>}{payload?.testResult?.stderr && <pre className="mt-3 overflow-x-auto rounded-ui-sm bg-ui-bg p-3 font-mono text-ui-1 text-ui-red">{payload.testResult.stderr}</pre>}</details></section>}
    {mode === "review" && <section className="grid gap-3"><Fact label="审核状态" value={cycle.data?.artifactReview?.status} /><p className="whitespace-pre-wrap rounded-ui-sm bg-ui-bg p-3 text-ui-1 leading-relaxed text-ui-txt-2">{reviewResult?.content || cycle.data?.artifactReview?.summary || "审核结果尚未形成；这里不会根据请求状态补造结论。"}</p><details className="text-ui-1 text-ui-txt-2"><summary className="cursor-pointer font-semibold">查看审核执行详情</summary><dl className="mt-3 grid gap-3"><Fact label="Review Request" value={cycle.data?.artifactReview?.requestRef} /><Fact label="Reviewer Task" value={cycle.data?.artifactReview?.reviewTaskRef} /><Fact label="Codex Session" value={cycle.data?.artifactReview?.sessionRef} /><Fact label="实际权限" value={accessCopy(cycle.data?.artifactReview?.computerAccess).effective} /></dl></details></section>}
    {mode === "meta" && <section className="grid gap-4"><dl className="grid gap-3"><Fact label="执行能力" value="Codex（研发员工的代码执行能力）" /><Fact label="访问方式" value={access.requested} /><Fact label="当前状态" value={access.configured} /><Fact label="实际权限" value={access.effective} /></dl><details className="border-t border-ui-line pt-4 text-ui-1 text-ui-txt-2"><summary className="cursor-pointer font-semibold">查看技术状态与内部 ID</summary><dl className="mt-3 grid gap-3"><Fact label="Task ID" value={cycle.data.taskRef} /><Fact label="Artifact ID" value={artifact?.artifact_id} /><Fact label="Codex Session ID" value={cycle.data?.sessionRef} /><Fact label="Provider" value={payload?.provider || "未记录"} /><Fact label="Requested" value={cycle.data?.computerAccess?.requested_intent} /><Fact label="Configured" value={cycle.data?.computerAccess?.configured_state} /><Fact label="Effective" value={cycle.data?.computerAccess?.effective_state || "UNKNOWN"} /><Fact label="Verification" value={cycle.data?.computerAccess?.verification_state || "UNVERIFIED"} /></dl></details></section>}
    {!artifact && <p className="rounded-ui-sm border border-ui-line bg-ui-surface p-3 text-ui-1 text-ui-txt-2">执行记录已保存，但代码结果尚不可读取；这里不会根据员工汇报补造代码变化或测试结果。</p>}
  </div>;
}

function Workstation({ cycle, detail, task, selected, onSelect, onStart, onExecute, onSubmitReview, onSubmitHandoff, onOpenResult, busy }) {
  const [kind, label] = responsibilityState(cycle);
  const [expanded, setExpanded] = useState(["working", "failed"].includes(kind));
  const holderRef = cycle.data?.workContext?.responsibilityEmployeeRef;
  const executorRef = cycle.data?.workContext?.currentExecutorRef;
  const holder = employeeByRef(detail, holderRef);
  const executor = employeeByRef(detail, executorRef);
  const holderView = employeePresentation(holder, detail);
  const executorView = employeePresentation(executor, detail);
  const canStart = cycle.lifecycle_status === "PLANNED";
  const canExecute = cycle.lifecycle_status === "RUNNING" && cycle.data?.executionStatus === "READY";
  const resultReady = Boolean(cycle.data?.taskRef && (cycle.data?.artifactRefs || []).length);

  useEffect(() => {
    if (["working", "failed"].includes(kind)) setExpanded(true);
  }, [kind]);

  return <article className={`rounded-ui-md border bg-ui-surface ${selected ? "border-ui-accent" : "border-ui-line"}`}>
    <button type="button" onClick={() => { onSelect(); setExpanded((value) => !value); }} className="flex w-full items-center gap-3 p-3 text-left">
      <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-ui-surface-2 text-ui-1 font-bold text-ui-txt-2">{holderView.name.slice(0, 1)}</span>
      <span className="min-w-0 flex-1"><span className="block truncate text-ui-2 font-semibold">{holderView.name} · {holderView.role}</span><span className="mt-0.5 block truncate text-ui-1 text-ui-txt-3">正在负责：{cycle.data?.workItemName || "未命名研发工作"}</span></span>
      <span className={`text-ui-1 font-semibold ${STATUS_CLASS[kind]}`}>{label}</span>
      <span aria-hidden="true" className="text-ui-txt-3">{expanded ? "⌃" : "⌄"}</span>
    </button>
    {expanded && <div className="border-t border-ui-line p-4">
      <dl className="grid gap-3 sm:grid-cols-3">
        <Fact label="当前工作" value={cycle.data?.workItemName} />
        <Fact label="负责人" value={`${holderView.name} · ${holderView.role}`} />
        <Fact label="现在由谁执行" value={executorRef ? `${executorView.name} 正在处理` : "当前无人执行"} />
      </dl>
      <section className="mt-4 rounded-ui-sm bg-ui-surface-2 p-3">
        <p className="text-ui-1 text-ui-txt-3">{holderView.name} 的工作进展</p>
        <p className="mt-1 text-ui-2 leading-relaxed text-ui-txt">{cycle.data?.conversation?.summary || (kind === "working" ? "正在允许范围内处理这项工作；形成可验证结果前不会显示完成。" : kind === "failed" ? "这次执行没有通过验证，代码变化和失败证据已经保留。" : "这项工作已建立，等待研发员工开始处理。")}</p>
        {resultReady && <button type="button" onClick={() => onOpenResult("diff")} className="mt-2 text-ui-1 font-semibold text-ui-accent">📎 查看代码变化与测试结果 ▸</button>}
      </section>
      <RdArtifactReview cycle={cycle} employees={detail?.employees || []} busy={busy} onSubmit={onSubmitReview} onOpenResult={onOpenResult} />
      <RdResponsibilityHandoff cycle={cycle} employees={detail?.employees || []} busy={busy} onSubmit={onSubmitHandoff} />
      <div className="mt-4 flex flex-wrap gap-2">
        {canStart && <button type="button" disabled={busy} onClick={onStart} className="rounded-ui-sm bg-ui-action-primary-bg px-3 py-2 text-ui-2 font-semibold text-ui-action-primary-fg disabled:opacity-50">{busy ? "准备中…" : "准备开始"}</button>}
        {canExecute && <button type="button" disabled={busy} onClick={onExecute} className="rounded-ui-sm bg-ui-action-primary-bg px-3 py-2 text-ui-2 font-semibold text-ui-action-primary-fg disabled:opacity-50">{busy ? "正在交给员工…" : "交给研发员工"}</button>}
        {kind === "failed" && <p className="text-ui-1 leading-relaxed text-ui-red">这项工作需要处理失败原因后才能继续；当前不会自动重试。</p>}
        {cycle.data?.taskRef && <Link href={`/ceo-office/execution/tasks/${encodeURIComponent(cycle.data.taskRef)}`} className="inline-flex items-center rounded-ui-sm border border-ui-line px-3 py-2 text-ui-1 font-semibold text-ui-txt-2 no-underline">查看完整执行记录</Link>}
      </div>
      <details className="mt-4 border-t border-ui-line pt-3 text-ui-1 text-ui-txt-2"><summary className="cursor-pointer font-semibold">查看责任与执行 ID</summary><dl className="mt-3 grid gap-3 sm:grid-cols-2"><Fact label="对象归属" value={cycle.owner_ref} /><Fact label="Responsibility Holder" value={holderRef} /><Fact label="Current Executor" value={executorRef || "none"} /><Fact label="Task ID" value={cycle.data?.taskRef} /></dl></details>
    </div>}
  </article>;
}

export default function RdWorkspacePhaseTwo() {
  const runtime = useRuntime();
  const router = useRouter();
  const params = useSearchParams();
  const workspaceId = params.get("workspace_id") || "";
  const requestedCycle = params.get("cycle_id") || "";
  const [detail, setDetail] = useState(null);
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");
  const [busyCycle, setBusyCycle] = useState("");
  const [task, setTask] = useState(null);
  const [reviewTask, setReviewTask] = useState(null);
  const [project, setProject] = useState(null);
  const [utilityMode, setUtilityMode] = useState("diff");
  const [utilityRequestKey, setUtilityRequestKey] = useState(0);
  const knownWorkspace = (runtime.snapshot?.workspaces || []).find((item) => item.workspace_id === workspaceId);
  const workspace = detail?.workspace?.business_type === "RD" ? detail.workspace : null;
  const cycles = detail?.cycles || [];
  const selectedCycle = cycles.find((item) => item.entity_id === requestedCycle) || cycles[0] || null;
  const pendingDecision = (detail?.decisions || []).find((item) => item.entity_id === selectedCycle?.data?.rdDecisionPacketRef) || null;

  const load = useCallback(async (quiet = false) => {
    if (!runtime.companyId || !workspaceId) return;
    if (!quiet) setStatus("loading");
    try {
      setDetail(await getRuntimeWorkspace(runtime.companyId, workspaceId));
      setError("");
      setStatus("ready");
    } catch (requestError) {
      setError(runtimeErrorMessage(requestError));
      if (!quiet) setStatus("error");
    }
  }, [runtime.companyId, workspaceId]);

  useEffect(() => { load(); }, [load]);
  useEffect(() => {
    const primaryRunning = cycles.some((item) => item.data?.executionStatus === "RUNNING");
    const reviewRunning = cycles.some((item) => item.data?.artifactReview?.status === "REVIEWING");
    if (!primaryRunning && !reviewRunning) return undefined;
    const poll = window.setInterval(() => load(true), 800);
    return () => window.clearInterval(poll);
  }, [cycles, load]);
  useEffect(() => {
    let active = true;
    setTask(null);
    setReviewTask(null);
    setProject(null);
    if (!selectedCycle) return () => { active = false; };
    if (selectedCycle.data?.taskRef) getTask(selectedCycle.data.taskRef).then((value) => { if (active) setTask(value); }).catch(() => {});
    if (selectedCycle.data?.artifactReview?.reviewTaskRef) getTask(selectedCycle.data.artifactReview.reviewTaskRef).then((value) => { if (active) setReviewTask(value); }).catch(() => {});
    if (selectedCycle.data?.projectRef) getProjects(runtime.companyId).then((value) => {
      if (active) setProject((value?.projects || []).find((item) => item.project_id === selectedCycle.data.projectRef) || null);
    }).catch(() => {});
    return () => { active = false; };
  }, [runtime.companyId, selectedCycle?.entity_id, selectedCycle?.data?.projectRef, selectedCycle?.data?.taskRef, selectedCycle?.data?.artifactReview?.reviewTaskRef]);

  useAssistantPageContext({ page: "workspace", company_id: runtime.companyId, workspace_id: workspaceId, business_type: "RD", cycle_id: selectedCycle?.entity_id || "" });

  const chooseCycle = (cycleId) => router.replace(`/ceo-office/workspace/software?workspace_id=${encodeURIComponent(workspaceId)}&cycle_id=${encodeURIComponent(cycleId)}`);
  const operate = async (cycle, action) => {
    setBusyCycle(cycle.entity_id);
    setError("");
    try {
      if (action === "start") {
        await startOperatingCycle(workspaceId, cycle.entity_id, { ceo_id: CEO_ID, reason: "CEO 准备当前真实研发责任" });
      } else {
        await executeOperatingCycle(workspaceId, cycle.entity_id, { ceo_id: CEO_ID, reason: "CEO 请求研发员工执行当前真实 Task" });
      }
      await load(true);
    } catch (requestError) {
      setError(runtimeErrorMessage(requestError));
      await load(true);
    } finally {
      setBusyCycle("");
    }
  };
  const submitReview = async (cycle, reviewerEmployeeRef) => {
    setBusyCycle(cycle.entity_id);
    setError("");
    try {
      await createArtifactReview(workspaceId, cycle.entity_id, { ceo_id: CEO_ID, reviewer_employee_ref: reviewerEmployeeRef });
      await executeArtifactReview(workspaceId, cycle.entity_id, { ceo_id: CEO_ID, reason: "审核员工检查当前代码 Artifact" });
      await load(true);
    } catch (requestError) {
      setError(runtimeErrorMessage(requestError));
      await load(true);
    } finally {
      setBusyCycle("");
    }
  };
  const submitHandoff = async (cycle, targetEmployeeRef) => {
    setBusyCycle(cycle.entity_id);
    setError("");
    try {
      await createResponsibilityHandoff(workspaceId, cycle.entity_id, {
        ceo_id: CEO_ID,
        target_employee_ref: targetEmployeeRef,
        responsibility_summary: "接管已审核结果的后续研发责任",
        reason: "当前实现与审核已完成，转入下一项明确责任",
      });
      await sendResponsibilityHandoff(workspaceId, cycle.entity_id, { ceo_id: CEO_ID, reason: "发送最小责任上下文" });
      await load(true);
    } catch (requestError) {
      setError(runtimeErrorMessage(requestError));
      await load(true);
    } finally {
      setBusyCycle("");
    }
  };
  const reviewDecision = async () => {
    if (!selectedCycle) return;
    setBusyCycle(selectedCycle.entity_id);
    setError("");
    try {
      await reviewRDDecision(workspaceId, selectedCycle.entity_id, { ceo_id: CEO_ID, reason: "CEO 查看完整高风险方案" });
      await load(true);
      return true;
    } catch (requestError) {
      setError(runtimeErrorMessage(requestError));
      return false;
    } finally {
      setBusyCycle("");
    }
  };
  const chooseDecision = async (choice) => {
    if (!selectedCycle) return;
    setBusyCycle(selectedCycle.entity_id);
    setError("");
    try {
      await chooseRDDecision(workspaceId, selectedCycle.entity_id, {
        ceo_id: CEO_ID,
        choice,
        reason: choice === "DEFER" ? "CEO 暂缓，等待更合适的业务窗口" : "CEO 已查看方案并作出选择",
      });
      await load(true);
    } catch (requestError) {
      setError(runtimeErrorMessage(requestError));
      await load(true);
    } finally {
      setBusyCycle("");
    }
  };
  const openResult = (mode) => { setUtilityMode(mode); setUtilityRequestKey((value) => value + 1); };

  const summary = useMemo(() => {
    const working = cycles.filter((item) => item.data?.executionStatus === "RUNNING").length;
    const failed = cycles.filter((item) => item.data?.executionStatus === "FAILED").length;
    const completed = cycles.filter((item) => item.data?.executionStatus === "COMPLETED").length;
    return `${(detail?.employees || []).length} 名研发员工 · ${cycles.length} 项工作 · ${working} 项进行中 · ${completed} 项已完成${failed ? ` · ${failed} 项需要处理` : ""}`;
  }, [cycles, detail?.employees]);

  let main;
  if (runtime.status === "loading" || status === "loading" || status === "idle") main = <p className="text-ui-2 text-ui-txt-2">正在读取研发办公室…</p>;
  else if (!runtime.snapshot?.company) main = <section className="rounded-ui-md border border-ui-line bg-ui-surface p-5"><h1 className="text-ui-5 font-semibold">先建立公司，再进入研发办公室</h1><Link href="/onboarding" className="mt-4 inline-flex text-ui-accent">继续创建公司</Link></section>;
  else if (!knownWorkspace || status === "error") main = <section className="rounded-ui-md border border-ui-line bg-ui-surface p-5"><h1 className="text-ui-5 font-semibold">暂时无法读取这个研发办公室</h1><p className="mt-2 text-ui-2 text-ui-txt-2">{error || "当前公司没有这个 Workspace。"}</p><button type="button" onClick={() => load()} className="mt-4 rounded-ui-sm border border-ui-line px-3 py-2 text-ui-2 font-semibold">重新读取</button></section>;
  else if (!workspace) main = <section className="rounded-ui-md border border-ui-line bg-ui-surface p-5"><h1 className="text-ui-5 font-semibold">这不是研发 Workspace</h1><p className="mt-2 text-ui-2 text-ui-txt-2">不会把其他业务对象解释成研发 Project 或 Task。</p></section>;
  else main = <div className="grid gap-4">
    <header className="rounded-ui-md border border-ui-line bg-ui-surface p-4">
      <p className="text-ui-1 text-ui-txt-3">研发办公室</p>
      <h1 className="mt-1 text-ui-5 font-semibold">{workspace.name}</h1>
      <p className="mt-2 text-ui-2 text-ui-txt-2">{summary}</p>
      <p className="mt-2 text-ui-1 text-ui-txt-3">选择一项工作，就能看到负责人、当前进展和可验证结果。</p>
    </header>
    <RdDecisionPackage decision={pendingDecision} busy={busyCycle === selectedCycle?.entity_id} onReview={reviewDecision} onChoose={chooseDecision} />
    {error && <p role="alert" className="rounded-ui-sm border border-ui-red bg-ui-red/10 p-3 text-ui-1 text-ui-red">{error}</p>}
    <section className="grid gap-3" aria-label="研发员工工作位">
      {cycles.map((cycle) => <Workstation key={cycle.entity_id} cycle={cycle} detail={detail} task={selectedCycle?.entity_id === cycle.entity_id ? task : null} selected={selectedCycle?.entity_id === cycle.entity_id} onSelect={() => chooseCycle(cycle.entity_id)} onStart={() => operate(cycle, "start")} onExecute={() => operate(cycle, "execute")} onSubmitReview={(reviewerRef) => submitReview(cycle, reviewerRef)} onSubmitHandoff={(targetRef) => submitHandoff(cycle, targetRef)} onOpenResult={openResult} busy={busyCycle === cycle.entity_id} />)}
      {!cycles.length && <section className="rounded-ui-md border border-ui-line bg-ui-surface p-4"><h2 className="text-ui-3 font-semibold">还没有研发工作</h2><p className="mt-1 text-ui-2 text-ui-txt-2">选择一个现有项目，告诉研发员工要解决的问题和期望结果。</p></section>}
    </section>
    <RdRealExecutionComposer workspace={workspace} onCreated={() => load(true)} />
  </div>;

  return <WorkspacePaneShell
    workspaceId={workspaceId}
    breadcrumb={`业务空间 / ${workspace?.name || "研发办公室"}${selectedCycle ? ` / ${selectedCycle.data?.workItemName || "当前责任"}` : ""}`}
    contextAvailable={Boolean(selectedCycle)}
    contextLabel="研发上下文"
    contextPane={<RdContext project={project} cycle={selectedCycle} />}
    utilityAvailable={Boolean(selectedCycle?.data?.taskRef)}
    utilityLabel={`研发证据${selectedCycle?.data?.workItemName ? ` · ${selectedCycle.data.workItemName}` : ""}`}
    utilityPane={<RdUtility cycle={selectedCycle} task={task} reviewTask={reviewTask} mode={utilityMode} onMode={setUtilityMode} />}
    utilityRequestKey={utilityRequestKey}
  >{main}</WorkspacePaneShell>;
}
