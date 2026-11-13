"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import { useAssistantPageContext } from "../../../components/assistant/GlobalAssistant.js";

import {
  assignmentFacts,
  buildStructuredTask,
  costFact,
  parseStructuredTask,
  primaryAction,
  progressValue,
  resultExplanation,
  resultFacts,
  statusLabel,
} from "./projectRuntimeViewModel.mjs";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";

const STATUS_TONE = {
  planned: "border-ui-line bg-ui-surface-2 text-ui-text-2",
  active: "border-ui-accent bg-ui-surface-2 text-ui-accent",
  blocked: "border-ui-danger bg-ui-surface-2 text-ui-danger",
  completed: "border-ui-success bg-ui-surface-2 text-ui-success",
  archived: "border-ui-line bg-ui-surface-2 text-ui-text-2",
  pending: "border-ui-warning bg-ui-surface-2 text-ui-warning",
  queued: "border-ui-accent bg-ui-surface-2 text-ui-accent",
  running: "border-ui-accent bg-ui-surface-2 text-ui-accent",
  review: "border-ui-warning bg-ui-surface-2 text-ui-warning",
  approved: "border-ui-success bg-ui-surface-2 text-ui-success",
  done: "border-ui-success bg-ui-surface-2 text-ui-success",
  rejected: "border-ui-danger bg-ui-surface-2 text-ui-danger",
  failed: "border-ui-danger bg-ui-surface-2 text-ui-danger",
  unknown: "border-ui-line bg-ui-surface-2 text-ui-text-2",
};

function StatusBadge({ status }) {
  return (
    <span className={`inline-flex rounded-md border px-2.5 py-1 text-xs font-bold ${STATUS_TONE[status] || STATUS_TONE.unknown}`}>
      {statusLabel(status)}
    </span>
  );
}

function LoadingState() {
  return (
    <main className="min-h-[100dvh] bg-ui-bg px-5 py-10 text-ui-txt">
      <div className="mx-auto max-w-[1320px] animate-pulse motion-reduce:animate-none">
        <div className="h-5 w-44 rounded-lg bg-ui-surface-2" />
        <div className="mt-8 h-20 max-w-2xl rounded-xl bg-ui-surface-2" />
        <div className="mt-8 grid gap-4 lg:grid-cols-[1.45fr_0.75fr]">
          <div className="h-72 rounded-xl bg-ui-surface" />
          <div className="h-72 rounded-xl bg-ui-surface" />
        </div>
      </div>
    </main>
  );
}

function Section({ title, description, children, id }) {
  return (
    <section id={id} className="rounded-xl border border-ui-line bg-ui-surface p-5 shadow-ui sm:p-6">
      <div className="mb-5">
        <h2 className="text-lg font-black tracking-tight text-ui-text">{title}</h2>
        {description ? <p className="mt-1 max-w-[68ch] text-sm leading-6 text-ui-txt-2">{description}</p> : null}
      </div>
      {children}
    </section>
  );
}

export default function ProjectRuntimePage() {
  const params = useParams();
  const projectId = String(params?.project_id || "");
  useAssistantPageContext({ page: "project", project_id: projectId });
  const [payload, setPayload] = useState(null);
  const [goal, setGoal] = useState("");
  const [chatGoal, setChatGoal] = useState("");
  const [acceptanceCriteria, setAcceptanceCriteria] = useState("");
  const [constraintsRisk, setConstraintsRisk] = useState("");
  const [inputMode, setInputMode] = useState("chat");
  const [confirmation, setConfirmation] = useState(null);
  const [reviewNote, setReviewNote] = useState("");
  const [loading, setLoading] = useState(true);
  const [acting, setActing] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const load = useCallback(async () => {
    if (!projectId) return;
    setError("");
    try {
      const next = await api(`/api/pipeline/project/${encodeURIComponent(projectId)}`);
      setPayload(next);
      const structured = parseStructuredTask(next.runtime?.task?.natural_language);
      const nextGoal = structured.goal || next.project?.goal || "";
      setGoal((current) => current || nextGoal);
      setChatGoal((current) => current || nextGoal);
      setAcceptanceCriteria((current) => current || structured.acceptanceCriteria);
      setConstraintsRisk((current) => current || structured.constraintsRisk);
    } catch (err) {
      setError(err.message || "项目运行状态读取失败");
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  useEffect(() => {
    load();
  }, [load]);

  const taskStatus = payload?.runtime?.task?.status;
  useEffect(() => {
    if (!['queued', 'running'].includes(taskStatus)) return undefined;
    const timer = window.setInterval(load, 2000);
    return () => window.clearInterval(timer);
  }, [load, taskStatus]);

  const runtime = payload?.runtime;
  const project = payload?.project;
  const task = runtime?.task;
  const graph = runtime?.graph;
  const action = useMemo(() => primaryAction(runtime), [runtime]);
  const progress = progressValue(graph);
  const facts = resultFacts(task);
  const explanation = resultExplanation(task);
  const canEditGoal = explanation.canCreateNextRun;
  const assignments = assignmentFacts(graph);
  const recordedCost = costFact(task);
  const recordedStructure = parseStructuredTask(task?.natural_language);

  const perform = async (work, successMessage) => {
    setActing(true);
    setError("");
    setNotice("");
    try {
      await work();
      setNotice(successMessage);
      await load();
      return true;
    } catch (err) {
      setError(err.message || "操作失败，请重试");
      return false;
    } finally {
      setActing(false);
    }
  };

  const prepareConfirmation = () => {
    const nextGoal = (inputMode === "chat" ? chatGoal : goal).trim();
    if (!nextGoal) {
      setError(inputMode === "chat" ? "请先说说这次想继续完成什么" : "请先填写任务目标");
      return;
    }
    setError("");
    setConfirmation({
      goal: nextGoal,
      acceptanceCriteria: inputMode === "structured" ? acceptanceCriteria.trim() : "",
      constraintsRisk: inputMode === "structured" ? constraintsRisk.trim() : "",
    });
  };

  const submitGoal = async () => {
    const structuredText = buildStructuredTask(confirmation || {});
    if (!structuredText) {
      setError("确认单中的目标、验收标准和约束 / 风险都需要填写");
      return;
    }
    const nextGoal = confirmation.goal.trim();
    const submitted = await perform(async () => {
      await api(`/api/workspace/projects/${encodeURIComponent(projectId)}`, {
        method: "PATCH",
        body: JSON.stringify({ goal: nextGoal }),
      });
      await api("/api/pipeline/submit", {
        method: "POST",
        body: JSON.stringify({ natural_language: structuredText, project_id: projectId }),
      });
    }, task ? "新目标已保存，下一次计划已生成" : "目标已提交，计划已生成");
    if (!submitted) return;
    setGoal(nextGoal);
    setChatGoal(nextGoal);
    setAcceptanceCriteria(confirmation.acceptanceCriteria.trim());
    setConstraintsRisk(confirmation.constraintsRisk.trim());
    setConfirmation(null);
  };

  const startRun = () => {
    if (!task) return;
    if ((action.kind === "auto_run" || action.kind === "retry") && graph?.graph_id) {
      perform(
        () => api(`/api/pipeline/${encodeURIComponent(graph.graph_id)}/auto-run`, { method: "POST" }),
        "运行已启动",
      );
    } else if (action.kind === "dispatch") {
      perform(
        () => api(`/api/pipeline/${encodeURIComponent(task.id)}/dispatch`, { method: "POST" }),
        "返工运行已继续",
      );
    }
  };

  const decide = (kind) => {
    if (!task) return;
    const note = reviewNote.trim();
    if ((kind === "reject" || kind === "rework") && !note) {
      setError("拒绝或返工时请填写原因");
      return;
    }
    const options = { method: "POST" };
    if (kind === "reject" || kind === "rework") {
      options.body = JSON.stringify({ note });
    }
    perform(
      () => api(`/api/pipeline/${encodeURIComponent(task.id)}/${kind}`, options),
      kind === "approve" ? "成果已批准" : kind === "reject" ? "成果已拒绝" : "已进入返工队列",
    );
  };

  if (loading) return <LoadingState />;
  if (error && !payload) {
    return (
      <main className="min-h-[100dvh] bg-ui-bg px-5 py-16 text-ui-txt">
        <div className="mx-auto max-w-2xl rounded-xl border border-ui-danger bg-ui-surface p-8">
          <p className="text-sm font-bold text-ui-danger">项目读取失败</p>
          <h1 className="mt-3 text-3xl font-black tracking-tight">无法打开 Project Runtime</h1>
          <p className="mt-4 text-sm leading-6 text-ui-txt-2">{error}</p>
          <a href={`/login?next=${encodeURIComponent(`/projects/${projectId}`)}`} className="mt-6 inline-flex rounded-lg bg-ui-success px-4 py-2.5 text-sm font-bold text-white no-underline">进入本地 Workspace</a>
          <button type="button" onClick={load} className="mt-6 rounded-lg bg-ui-bg px-4 py-2.5 text-sm font-bold text-white active:translate-y-px">
            重新读取
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-[100dvh] bg-ui-bg text-ui-txt">
      <header className="border-b border-ui-line bg-ui-surface">
        <div className="mx-auto flex min-h-16 max-w-[1320px] items-center justify-between gap-4 px-5 py-3 sm:px-8">
          <div className="flex min-w-0 items-center gap-3 text-sm">
            <a href="/ceo-office" className="font-black tracking-tight text-ui-text no-underline">CURIS</a>
            <span className="text-ui-text-3">/</span>
            <span className="truncate font-semibold text-ui-txt-2">项目负责人工作台</span>
          </div>
          <span className="hidden max-w-[320px] truncate font-mono text-ui-1 text-ui-txt-3 sm:block">{projectId}</span>
        </div>
      </header>

      <div className="mx-auto max-w-[1320px] px-5 py-8 sm:px-8 sm:py-10">
        <section className="grid gap-7 border-b border-ui-line pb-8 lg:grid-cols-[1.5fr_0.7fr] lg:items-end">
          <div>
            <div className="mb-4 flex flex-wrap items-center gap-3">
              <StatusBadge status={task?.status || project?.status} />
              <span className="text-xs font-semibold text-ui-txt-3">{project?.company_id}</span>
            </div>
            <h1 className="max-w-4xl text-3xl font-black tracking-[-0.035em] text-ui-text sm:text-5xl">{project?.name || "未命名项目"}</h1>
            <p className="mt-4 max-w-3xl text-base leading-7 text-ui-txt-2">{project?.description || "从目标开始，计划、运行、决策和成果都在这里恢复。"}</p>
          </div>
          <div className="lg:text-right">
            {action.kind === "view_result" ? (
              <a href="#results" className="inline-flex rounded-lg bg-ui-success px-5 py-3 text-sm font-black text-white no-underline hover:bg-ui-success active:translate-y-px">{action.label}</a>
            ) : action.kind === "approve" ? (
              <button type="button" disabled={acting} onClick={() => decide("approve")} className="rounded-lg bg-ui-success px-5 py-3 text-sm font-black text-white hover:bg-ui-success disabled:cursor-not-allowed disabled:opacity-50 active:translate-y-px">{acting ? "处理中" : action.label}</button>
            ) : action.kind === "auto_run" || action.kind === "retry" || action.kind === "dispatch" ? (
              <button type="button" disabled={acting} onClick={startRun} className="rounded-lg bg-ui-success px-5 py-3 text-sm font-black text-white hover:bg-ui-success disabled:cursor-not-allowed disabled:opacity-50 active:translate-y-px">{acting ? "处理中" : action.label}</button>
            ) : (
              <div className="rounded-lg border border-ui-line bg-ui-surface px-4 py-3 text-sm font-semibold text-ui-txt-3">{action.kind === "submit" ? "从下方提交目标" : action.label}</div>
            )}
          </div>
        </section>

        {notice ? <p className="mt-5 rounded-lg border border-ui-success bg-ui-surface-2 px-4 py-3 text-sm font-bold text-ui-success">{notice}</p> : null}
        {error ? <p className="mt-5 rounded-lg border border-ui-danger bg-ui-surface-2 px-4 py-3 text-sm font-bold text-ui-danger">{error}</p> : null}

        <div className="mt-6 grid gap-6 lg:grid-cols-[1.45fr_0.75fr]">
          <div className="grid gap-6">
            <Section
              id="goal"
              title="这次要完成什么"
              description={
                canEditGoal
                  ? task
                    ? "提出下一步目标或填写结构化任务，确认后创建下一次运行；当前结果会继续保留。"
                    : "两种入口都会先整理成同一份任务确认单，再生成本项目计划。"
                  : "目标已进入当前运行，完成前不会创建第二条运行。"
              }
            >
              {canEditGoal ? (
                <>
                  <div className="inline-flex rounded-lg border border-ui-line bg-ui-surface-2 p-1" aria-label="目标输入方式">
                    <button
                      type="button"
                      onClick={() => {
                        setInputMode("chat");
                        setConfirmation(null);
                      }}
                      className={`rounded-md px-4 py-2 text-sm font-black ${inputMode === "chat" ? "bg-ui-surface text-ui-text shadow-sm" : "text-ui-txt-2"}`}
                    >
                      聊聊下一步
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setInputMode("structured");
                        setConfirmation(null);
                      }}
                      className={`rounded-md px-4 py-2 text-sm font-black ${inputMode === "structured" ? "bg-ui-surface text-ui-text shadow-sm" : "text-ui-txt-2"}`}
                    >
                      结构化任务
                    </button>
                  </div>

                  {inputMode === "chat" ? (
                    <div className="mt-5">
                      <label className="block text-sm font-bold text-ui-text" htmlFor="project-chat-goal">我想让项目继续做</label>
                      <textarea
                        id="project-chat-goal"
                        value={chatGoal}
                        disabled={acting}
                        onChange={(event) => {
                          setChatGoal(event.target.value);
                          setConfirmation(null);
                        }}
                        rows={4}
                        className="mt-2 w-full resize-y rounded-lg border border-ui-line bg-ui-surface px-4 py-3 text-sm leading-6 text-ui-text outline-none transition focus:border-ui-success focus:ring-2 focus:ring-ui-accent disabled:bg-ui-surface-2"
                        placeholder="例如：继续完善项目负责人工作台，让结果更容易判断"
                      />
                    </div>
                  ) : (
                    <div className="mt-5 grid gap-4">
                      <TaskField id="structured-goal" label="目标" value={goal} onChange={(value) => {
                        setGoal(value);
                        setConfirmation(null);
                      }} placeholder="这次要完成什么" />
                      <TaskField id="acceptance-criteria" label="验收标准" value={acceptanceCriteria} onChange={(value) => {
                        setAcceptanceCriteria(value);
                        setConfirmation(null);
                      }} placeholder="怎样算完成、需要看到什么结果" />
                      <TaskField id="constraints-risk" label="约束 / 风险" value={constraintsRisk} onChange={(value) => {
                        setConstraintsRisk(value);
                        setConfirmation(null);
                      }} placeholder="不能做什么、需要特别留意什么" />
                    </div>
                  )}

                  {!confirmation ? (
                    <button type="button" disabled={acting} onClick={prepareConfirmation} className="mt-4 rounded-lg bg-ui-success px-5 py-3 text-sm font-black text-white hover:bg-ui-success disabled:opacity-50 active:translate-y-px">
                      整理为任务确认单
                    </button>
                  ) : (
                    <div className="mt-5 rounded-xl border-2 border-ui-success bg-ui-surface-2/60 p-5">
                      <div className="flex flex-wrap items-center justify-between gap-3">
                        <div>
                          <p className="text-xs font-black uppercase tracking-[0.16em] text-ui-success">提交前确认</p>
                          <h3 className="mt-1 text-lg font-black text-ui-text">结构化任务确认单</h3>
                        </div>
                        <span className="rounded-md border border-ui-success bg-ui-surface px-2.5 py-1 text-xs font-bold text-ui-success">
                          {task ? "创建下一次项目运行" : "创建首次项目运行"}
                        </span>
                      </div>
                      <div className="mt-5 grid gap-4">
                        <TaskField id="confirm-goal" label="目标" value={confirmation.goal} onChange={(value) => setConfirmation((current) => ({ ...current, goal: value }))} />
                        <TaskField id="confirm-acceptance" label="验收标准" value={confirmation.acceptanceCriteria} onChange={(value) => setConfirmation((current) => ({ ...current, acceptanceCriteria: value }))} placeholder="补充可判断的完成标准" />
                        <TaskField id="confirm-risk" label="约束 / 风险" value={confirmation.constraintsRisk} onChange={(value) => setConfirmation((current) => ({ ...current, constraintsRisk: value }))} placeholder="补充本次运行必须遵守的边界" />
                      </div>
                      <div className="mt-5 flex flex-wrap gap-3">
                        <button type="button" disabled={acting} onClick={submitGoal} className="rounded-lg bg-ui-success px-5 py-3 text-sm font-black text-white hover:bg-ui-success disabled:opacity-50 active:translate-y-px">
                          {acting ? "正在生成" : "确认并生成计划"}
                        </button>
                        <button type="button" disabled={acting} onClick={() => setConfirmation(null)} className="rounded-lg border border-ui-line bg-ui-surface px-5 py-3 text-sm font-black text-ui-text disabled:opacity-50">
                          返回修改
                        </button>
                      </div>
                    </div>
                  )}
                </>
              ) : (
                <div className="grid gap-3 sm:grid-cols-3">
                  <Fact label="目标" value={recordedStructure.goal || project?.goal || "未记录"} />
                  <Fact label="验收标准" value={recordedStructure.acceptanceCriteria || "未记录"} />
                  <Fact label="约束 / 风险" value={recordedStructure.constraintsRisk || "未记录"} />
                </div>
              )}
            </Section>

            <Section title="AI 公司执行计划" description="先看准备怎么做；Task 与 Graph 标识只保留在运行证据中。">
              {!graph?.nodes?.length ? (
                <div className="rounded-lg border border-dashed border-ui-line px-5 py-8 text-center text-sm text-ui-txt-3">提交目标后显示计划。</div>
              ) : (
                <div className="space-y-3">
                  {graph.available === false ? (
                    <p className="rounded-lg border border-ui-warning bg-ui-surface-2 px-4 py-3 text-sm text-ui-warning">服务已重启，计划快照仍在，但节点运行态无法恢复。不会显示推测进度。</p>
                  ) : null}
                  {graph.nodes.map((node, index) => (
                    <article key={node.id} className="grid gap-3 rounded-lg border border-ui-line bg-ui-surface-2/70 p-4 sm:grid-cols-[44px_1fr_auto] sm:items-center">
                      <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-ui-bg font-mono text-xs font-black text-white">{index + 1}</div>
                      <div>
                        <h3 className="text-sm font-black text-ui-text">{node.status === "failed" ? "启动失败 / 未执行" : (node.goal || "未命名节点")}</h3>
                        <p className="mt-1 text-xs text-ui-txt-3">依赖：{node.deps?.length ? node.deps.join(", ") : "无"}</p>
                      </div>
                      <StatusBadge status={node.status} />
                    </article>
                  ))}
                </div>
              )}
            </Section>

            <Section title="员工分工" description="只展示当前计划真实记录的员工与能力；未分配时明确标记待调度。">
              {!assignments.length ? (
                <div className="rounded-lg border border-dashed border-ui-line px-5 py-8 text-center text-sm text-ui-txt-3">生成计划后显示员工与能力分工。</div>
              ) : (
                <div className="grid gap-3 sm:grid-cols-2">
                  {assignments.map((item) => (
                    <article key={item.id} className="rounded-lg border border-ui-line bg-ui-surface-2 p-4">
                      <div className="flex items-start justify-between gap-3">
                        <h3 className="text-sm font-black text-ui-text">{item.goal}</h3>
                        <StatusBadge status={item.status} />
                      </div>
                      <p className="mt-3 text-xs font-bold text-ui-txt-3">负责人</p>
                      <p className="mt-1 text-sm font-semibold text-ui-text">{item.employee}</p>
                      <p className="mt-3 text-xs font-bold text-ui-txt-3">能力</p>
                      <p className="mt-1 text-sm font-semibold text-ui-text">{item.capability}</p>
                    </article>
                  ))}
                </div>
              )}
            </Section>

            <Section id="results" title="成果" description="先说明这次发生了什么，再保留测试、文件和 trace 证据。">
              {!task ? (
                <div className="rounded-lg border border-dashed border-ui-line px-5 py-8 text-center text-sm text-ui-txt-3">当前还没有成果记录。</div>
              ) : (
                <div className="space-y-5">
                  <ResultExplanation explanation={explanation} />
                  {task.executor_result || facts.rework.length ? (
                    <div className="grid gap-3 sm:grid-cols-3">
                      <Fact label="测试退出码" value={facts.testExitCode ?? "未记录"} />
                      <Fact label="执行轮次" value={facts.rounds ?? "未记录"} />
                      <Fact label="涉及文件" value={facts.files.length || "未记录"} />
                    </div>
                  ) : null}
                  {facts.diff ? (
                    <div>
                      <h3 className="mb-2 text-sm font-black">代码差异</h3>
                      <pre className="max-h-[420px] overflow-auto rounded-lg border border-ui-line bg-ui-bg p-4 text-xs leading-6 text-ui-text">{facts.diff}</pre>
                    </div>
                  ) : null}
                  {facts.artifact ? (
                    <div>
                      <h3 className="mb-2 text-sm font-black">运行成果</h3>
                      <pre className="max-h-[420px] overflow-auto rounded-lg border border-ui-line bg-ui-bg p-4 text-xs leading-6 text-ui-text">{facts.artifact}</pre>
                    </div>
                  ) : null}
                  {facts.rework.length ? (
                    <div>
                      <h3 className="mb-2 text-sm font-black">返工记录</h3>
                      <ul className="space-y-2 text-sm text-ui-text-2">
                        {facts.rework.map((item, index) => <li key={`${index}-${item}`} className="rounded-lg bg-ui-surface-2 px-4 py-3">{item}</li>)}
                      </ul>
                    </div>
                  ) : null}
                </div>
              )}
            </Section>
          </div>

          <aside className="grid content-start gap-6">
            <Section title="运行状态">
              <div className="grid grid-cols-2 gap-3">
                <Fact label="总体进度" value={progress === null ? "不可恢复" : `${progress}%`} />
                <Fact label="节点数" value={graph?.nodes?.length ?? 0} />
                <Fact label="返工次数" value={task?.rework_count ?? 0} />
                <Fact label="运行存储" value={runtime?.persistence === "process_only" ? "进程态" : "未知"} />
              </div>
              {runtime?.blocked_reason ? (
                <p className="mt-4 rounded-lg border border-ui-warning bg-ui-surface-2 px-4 py-3 text-sm leading-6 text-ui-warning">当前运行进程已不可用。请保留现有证据，不会自动重建或重放。</p>
              ) : null}
            </Section>

            <Section title="成本与风险">
              <div className="grid gap-3">
                <Fact label="本次记录成本" value={recordedCost} />
                <Fact label="约束 / 风险" value={recordedStructure.constraintsRisk || constraintsRisk || "未记录"} />
              </div>
              {recordedCost === "未记录" ? (
                <p className="mt-3 text-xs leading-5 text-ui-txt-3">现有 Project Runtime 返回中没有成本字段，因此不会把未知成本显示为 0。</p>
              ) : null}
            </Section>

            {task?.status === "review" ? (
              <Section title="待决策" description="批准是主动作；拒绝和返工必须填写原因。">
                <label className="block text-sm font-bold text-ui-text" htmlFor="review-note">决策说明</label>
                <textarea id="review-note" value={reviewNote} onChange={(event) => setReviewNote(event.target.value)} rows={3} className="mt-2 w-full rounded-lg border border-ui-line px-3 py-2.5 text-sm outline-none focus:border-ui-success focus:ring-2 focus:ring-ui-accent" placeholder="拒绝或返工时必填" />
                <div className="mt-4 grid grid-cols-2 gap-3">
                  <button type="button" disabled={acting} onClick={() => decide("reject")} className="rounded-lg border border-ui-danger bg-ui-surface px-3 py-2.5 text-sm font-bold text-ui-danger disabled:opacity-50 active:translate-y-px">拒绝</button>
                  <button type="button" disabled={acting} onClick={() => decide("rework")} className="rounded-lg border border-ui-line bg-ui-surface px-3 py-2.5 text-sm font-bold text-ui-text disabled:opacity-50 active:translate-y-px">要求返工</button>
                </div>
              </Section>
            ) : null}

            <Section title="运行证据" description="Task、能力路由和 trace 仅在这里展开。">
              {!task ? (
                <p className="text-sm leading-6 text-ui-txt-3">生成计划后显示证据。</p>
              ) : (
                <div className="space-y-3">
                  <details className="rounded-lg border border-ui-line bg-ui-surface-2 p-4">
                    <summary className="cursor-pointer text-sm font-black">Task 与 Graph 标识</summary>
                    <dl className="mt-3 grid gap-2 font-mono text-ui-1 text-ui-txt-2">
                      <div><dt className="font-sans font-bold text-ui-text">Task</dt><dd className="break-all">{task.id}</dd></div>
                      <div><dt className="font-sans font-bold text-ui-text">Graph</dt><dd className="break-all">{graph?.graph_id || "未记录"}</dd></div>
                    </dl>
                  </details>
                  <details className="rounded-lg border border-ui-line bg-ui-surface-2 p-4">
                    <summary className="cursor-pointer text-sm font-black">能力降级与 Trace</summary>
                    {!runtime?.trace?.length ? <p className="mt-3 text-sm text-ui-txt-3">暂无 trace 记录。</p> : (
                      <ul className="mt-3 space-y-3">
                        {runtime.trace.map((item, index) => (
                          <li key={`${index}-${item.at || item.step}`} className="text-xs leading-5 text-ui-text-2">
                            <strong>{item.tool || "未记录能力"}</strong><br />
                            <span>{item.status || (item.error ? "失败" : "完成")}</span>
                          </li>
                        ))}
                      </ul>
                    )}
                  </details>
                </div>
              )}
            </Section>
          </aside>
        </div>
      </div>
    </main>
  );
}

function TaskField({ id, label, value, onChange, placeholder = "" }) {
  return (
    <label className="block text-sm font-bold text-ui-text" htmlFor={id}>
      {label}
      <textarea
        id={id}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        rows={3}
        className="mt-2 w-full resize-y rounded-lg border border-ui-line bg-ui-surface px-4 py-3 text-sm font-normal leading-6 text-ui-text outline-none transition focus:border-ui-success focus:ring-2 focus:ring-ui-accent"
        placeholder={placeholder}
      />
    </label>
  );
}

function Fact({ label, value }) {
  return (
    <div className="rounded-lg border border-ui-line bg-ui-surface-2 px-4 py-3">
      <div className="text-ui-1 font-bold text-ui-txt-3">{label}</div>
      <div className="mt-1 break-words text-sm font-black text-ui-text">{value}</div>
    </div>
  );
}

function ResultExplanation({ explanation }) {
  const tones = {
    failure: "border-ui-danger bg-ui-surface-2 text-ui-danger",
    success: "border-ui-success bg-ui-surface-2 text-ui-success",
    progress: "border-ui-accent bg-ui-surface-2 text-ui-accent",
    neutral: "border-ui-line bg-ui-surface-2 text-ui-text",
  };
  return (
    <div className={`rounded-lg border px-4 py-4 ${tones[explanation.tone] || tones.neutral}`}>
      <h3 className="text-sm font-black">{explanation.title}</h3>
      <p className="mt-1 max-w-[68ch] text-sm leading-6">{explanation.body}</p>
      {explanation.canCreateNextRun ? (
        <a href="#goal" className="mt-3 inline-flex text-sm font-black text-ui-success underline decoration-ui-success underline-offset-4">
          修改目标并继续
        </a>
      ) : null}
    </div>
  );
}

async function api(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    cache: "no-store",
    credentials: "include",
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(typeof body.detail === "string" ? body.detail : "请求失败");
  }
  return body;
}
