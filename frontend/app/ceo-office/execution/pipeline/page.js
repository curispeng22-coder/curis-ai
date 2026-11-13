"use client";

/**
 * 任务流水线（规划 → 任务图 → 队列 → 调度）。
 *
 * 这是主轴「目标 → 规划 → 任务图 → 队列 → 调度 → 执行 → 验收 → 返工 → 完成」的
 * 前半段入口。后端能力早就齐了（backend/app/issue_pipeline_api.py），此前前端
 * 零调用，导致产品看起来只有"单条任务直跑"，没有编排。
 *
 * 与 /ceo-office/execution 的分工：
 * - execution：扁平任务清单（/api/tasks），一条需求一次直跑。
 * - execution/pipeline：带依赖的任务图 + 自动调度 + 验收返工闭环。
 */

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import TerraShell from "../../../../components/terra/TerraShell.js";
import {
  TerraButton,
  TerraCard,
  TerraCardHeader,
  TerraEmpty,
  TerraPageHead,
  TerraSearch,
  TerraTag,
} from "../../../../components/terra/TerraPrimitives.js";
import { TerraErrorState, TerraLoadingSkeleton } from "../../../../components/terra/TerraState.js";
import { TerraIcon } from "../../../../components/terra/TerraIcons.js";
import { taskStatusMeta } from "../../../../components/terra/PipelineGraphView.js";
import {
  getProjects,
  listPipelineTasks,
  pickGraphId,
  submitPipelineTask,
} from "../../../../lib/api.js";

// 有任务在跑时才轮询，避免空转打后端。
const POLL_INTERVAL_MS = 3000;
const LIVE_STATUSES = ["queued", "running"];

function relativeTime(iso) {
  if (!iso) return "";
  const timestamp = Date.parse(iso);
  if (Number.isNaN(timestamp)) return "";
  const diff = Date.now() - timestamp;
  if (diff < 60_000) return "刚刚";
  if (diff < 3_600_000) return `${Math.floor(diff / 60_000)} 分钟前`;
  if (diff < 86_400_000) return `${Math.floor(diff / 3_600_000)} 小时前`;
  return `${Math.floor(diff / 86_400_000)} 天前`;
}

export default function PipelinePage() {
  const [tasks, setTasks] = useState([]);
  const [projects, setProjects] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [goal, setGoal] = useState("");
  const [projectId, setProjectId] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState("");
  const [questions, setQuestions] = useState([]);

  const loadVersion = useRef(0);

  const load = useCallback(async ({ silent = false } = {}) => {
    const version = ++loadVersion.current;
    if (!silent) setLoading(true);
    try {
      const [taskPayload, projectPayload] = await Promise.all([
        listPipelineTasks(),
        getProjects().catch(() => null),
      ]);
      if (version !== loadVersion.current) return;
      setTasks(Array.isArray(taskPayload) ? taskPayload : []);
      setProjects(projectPayload?.projects || []);
      setError("");
    } catch (err) {
      if (version === loadVersion.current && !silent) {
        setError(err?.message || "流水线读取失败");
      }
    } finally {
      if (version === loadVersion.current && !silent) setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const hasLive = useMemo(
    () => tasks.some((task) => LIVE_STATUSES.includes(task.status)),
    [tasks]
  );

  useEffect(() => {
    if (!hasLive) return undefined;
    const timer = setInterval(() => load({ silent: true }), POLL_INTERVAL_MS);
    return () => clearInterval(timer);
  }, [hasLive, load]);

  async function handleSubmit(event) {
    event.preventDefault();
    const text = goal.trim();
    if (!text || submitting) return;
    setSubmitting(true);
    setSubmitError("");
    setQuestions([]);
    try {
      const payload = await submitPipelineTask({
        natural_language: text,
        ...(projectId ? { project_id: projectId } : {}),
      });
      if (Array.isArray(payload?.questions) && payload.questions.length > 0) {
        // 信息不足：后端把任务留在 pending 并回问题，不自动开跑。
        setQuestions(payload.questions);
      } else {
        setGoal("");
      }
      await load({ silent: true });
    } catch (err) {
      setSubmitError(err?.message || "提交失败");
    } finally {
      setSubmitting(false);
    }
  }

  const projectNames = useMemo(
    () => Object.fromEntries(projects.map((item) => [item.project_id, item.name])),
    [projects]
  );

  const filtered = useMemo(() => {
    const query = searchQuery.trim().toLowerCase();
    if (!query) return tasks;
    return tasks.filter((task) =>
      [task.natural_language, task.id, task.status, task.issue_spec?.title]
        .some((value) => String(value || "").toLowerCase().includes(query))
    );
  }, [tasks, searchQuery]);

  const counts = useMemo(
    () => ({
      total: tasks.length,
      running: tasks.filter((task) => LIVE_STATUSES.includes(task.status)).length,
      review: tasks.filter((task) => task.status === "review").length,
      approved: tasks.filter((task) => task.status === "approved").length,
    }),
    [tasks]
  );

  if (loading) {
    return (
      <TerraShell topCrumb="任务流水线">
        <TerraLoadingSkeleton variant="page" />
      </TerraShell>
    );
  }
  if (error) {
    return (
      <TerraShell topCrumb="任务流水线">
        <TerraErrorState message={error} onRetry={load} />
      </TerraShell>
    );
  }

  return (
    <TerraShell
      topCrumb="任务流水线"
      topbarExtra={
        <TerraSearch
          placeholder="搜索需求或任务 ID…"
          value={searchQuery}
          onChange={setSearchQuery}
        />
      }
    >
      <TerraPageHead
        title="任务流水线"
        subtitle="一句话需求 → 自动拆成任务图 → 排队调度执行 → 你来验收或打回返工"
        pill={{ text: "Pipeline", icon: "i-polyline" }}
        facts={[
          { value: counts.total, label: "总任务" },
          { value: counts.running, label: "执行中" },
          { value: counts.review, label: "待验收" },
          { value: counts.approved, label: "已通过" },
        ]}
      />

      <TerraCard className="mb-4">
        <TerraCardHeader icon="i-target" iconClass="primary" title="下达新需求" />
        <form onSubmit={handleSubmit} className="space-y-3">
          <div>
            <label
              htmlFor="pipeline-goal"
              className="block text-ui-1 font-bold text-ui-txt-2 mb-1.5 tracking-wide"
            >
              用一句话说清你要什么 *
            </label>
            <textarea
              id="pipeline-goal"
              value={goal}
              onChange={(event) => setGoal(event.target.value)}
              rows={3}
              required
              placeholder="例如：给官网加一个联系表单，提交后写入数据库并发邮件通知我"
              className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-ui-3 text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-accent resize-y"
            />
            <p className="text-ui-1 text-ui-txt-3 mt-1">
              系统会先解析成结构化 issue，再拆成带依赖的任务图。信息不够时会回问你，而不是瞎跑。
            </p>
          </div>

          <div className="flex flex-wrap items-end gap-3">
            <div className="min-w-[220px]">
              <label
                htmlFor="pipeline-project"
                className="block text-ui-1 font-bold text-ui-txt-2 mb-1.5 tracking-wide"
              >
                归属项目（可选）
              </label>
              <select
                id="pipeline-project"
                value={projectId}
                onChange={(event) => setProjectId(event.target.value)}
                className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-ui-3 text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-accent"
              >
                <option value="">不绑定项目</option>
                {projects.map((project) => (
                  <option key={project.project_id} value={project.project_id}>
                    {project.name}
                  </option>
                ))}
              </select>
            </div>
            <TerraButton type="submit" icon="i-bolt" disabled={submitting || !goal.trim()}>
              {submitting ? "解析中…" : "提交并生成任务图"}
            </TerraButton>
          </div>

          {submitError && (
            <div className="flex items-start gap-2 rounded-ui-sm border border-ui-red bg-ui-red-soft px-3 py-2 text-ui-1 text-ui-red">
              <TerraIcon name="i-error" className="w-4 h-4 flex-shrink-0 mt-px" />
              <span>{submitError}</span>
            </div>
          )}

          {questions.length > 0 && (
            <div className="rounded-ui-sm border border-ui-amber bg-ui-amber-soft px-3 py-2 text-ui-1 text-ui-amber">
              <div className="font-bold flex items-center gap-1.5">
                <TerraIcon name="i-info" className="w-4 h-4" />
                信息不足，任务已排在待规划，先回答这些再开跑：
              </div>
              <ul className="list-disc pl-5 mt-1 space-y-0.5">
                {questions.map((question, index) => (
                  <li key={index}>{typeof question === "string" ? question : JSON.stringify(question)}</li>
                ))}
              </ul>
            </div>
          )}
        </form>
      </TerraCard>

      <TerraCard>
        <div className="flex items-center justify-between mb-3">
          <TerraCardHeader icon="i-polyline" iconClass="cyan" title="任务图队列" />
          <button
            type="button"
            onClick={() => load({ silent: true })}
            className="inline-flex items-center gap-1 text-ui-1 text-ui-txt-3 hover:text-ui-accent transition-colors"
          >
            <TerraIcon name="i-refresh" className="w-4 h-4" />
            刷新
            {hasLive && <span className="text-ui-primary">· 自动</span>}
          </button>
        </div>

        {filtered.length === 0 ? (
          <TerraEmpty icon="i-checklist">
            {tasks.length === 0
              ? "还没有流水线任务。在上面下达第一条需求，系统会自动拆成任务图。"
              : "没有匹配的任务。"}
          </TerraEmpty>
        ) : (
          <div className="space-y-2">
            {filtered.map((task) => {
              const meta = taskStatusMeta(task.status);
              const graphId = pickGraphId(task);
              return (
                <a
                  key={task.id}
                  href={`/ceo-office/execution/pipeline/${task.id}`}
                  className="block no-underline"
                >
                  <div className="flex items-center gap-3 px-3 py-2.5 rounded-ui-md bg-ui-surface border border-ui-line hover:border-ui-accent transition-colors">
                    <span className={`w-2 h-2 rounded-ui-pill flex-shrink-0 ${meta.dot}`} />
                    <div className="flex-1 min-w-0">
                      <div className="font-semibold text-ui-2 text-ui-txt truncate">
                        {task.issue_spec?.title || task.natural_language || task.id}
                      </div>
                      <div className="text-ui-1 text-ui-txt-3 mt-0.5 flex flex-wrap items-center gap-x-2">
                        <span className="font-mono">{task.id.slice(0, 8)}</span>
                        {task.issue_spec?.project_id && (
                          <span>· {projectNames[task.issue_spec.project_id] || task.issue_spec.project_id}</span>
                        )}
                        {graphId && <span>· 任务图 {String(graphId).slice(0, 8)}</span>}
                        {task.created_at && <span>· {relativeTime(task.created_at)}</span>}
                      </div>
                    </div>
                    {task.rework_count > 0 && (
                      <TerraTag color="amber">返工 {task.rework_count}/2</TerraTag>
                    )}
                    <TerraTag color={meta.color}>{meta.label}</TerraTag>
                  </div>
                </a>
              );
            })}
          </div>
        )}
      </TerraCard>
    </TerraShell>
  );
}
