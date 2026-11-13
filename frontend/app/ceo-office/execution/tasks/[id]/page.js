"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useParams } from "next/navigation";
import Image from "next/image";
import TerraShell from "../../../../../components/terra/TerraShell.js";
import RuntimeCapabilitySwitcher from "../../../../../components/terra/RuntimeCapabilitySwitcher.js";
import {
  TerraBackLink,
  TerraBoundary,
  TerraButton,
  TerraCard,
  TerraCardHeader,
  TerraDrawer,
  TerraEmpty,
  TerraPageHead,
  TerraTag,
} from "../../../../../components/terra/TerraPrimitives.js";
import { TerraErrorState, TerraLoadingSkeleton } from "../../../../../components/terra/TerraState.js";
import {
  acceptTaskHandoff,
  cancelTaskRun,
  getEmployees,
  getProjects,
  getTask,
  getTaskJob,
  getTaskRun,
  getTaskRunTimeline,
  pauseTaskForInput,
  reassignTaskHandoff,
  requestTaskHandoff,
  resumeTaskRun,
  startTaskJob,
  supplyTaskInput,
} from "../../../../../lib/api.js";
import {
  createMemoryEntry,
  getContextPackage,
} from "../../../../../lib/memory.js";
import { workspaceEntryHref } from "../../../../../lib/runtimeApi.js";

const STATUS = {
  INIT: { label: "待执行", color: "grey" },
  PENDING: { label: "排队中", color: "amber" },
  PARSED: { label: "执行中", color: "primary" },
  RUNNING: { label: "执行中", color: "primary" },
  AWAITING_INPUT: { label: "等待补充", color: "amber" },
  HUMAN_HANDOFF: { label: "人工接管", color: "red" },
  RESUMED: { label: "已恢复", color: "primary" },
  COMPLETED: { label: "已完成", color: "green" },
  FAILED: { label: "失败", color: "red" },
  CANCELLED: { label: "已取消", color: "grey" },
};

const PLATFORM_LABEL = { xhs: "小红书", douyin: "抖音", toutiao: "头条" };
const EVENT_LABEL = {
  execution_started: "开始执行",
  capability_selected: "已选择能力",
  knowledge_retrieved: "已检索上下文",
  model_called: "模型调用",
  tool_called: "工具调用",
  awaiting_input: "等待补充信息",
  input_supplied: "用户已补充信息",
  human_handoff_requested: "请求人工接管",
  human_handoff_accepted: "人工已接管",
  human_handoff_reassigned: "已转派接管人",
  execution_resumed: "恢复 AI 执行",
  execution_completed: "执行完成",
  execution_failed: "执行失败",
  execution_cancelled: "执行取消",
};
const EVENT_DOT = {
  green: "bg-ui-green",
  red: "bg-ui-red",
  amber: "bg-ui-amber",
  grey: "bg-ui-line-2",
  cyan: "bg-ui-primary",
};

function formatTime(value) {
  if (!value) return "未记录";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString("zh-CN");
}

function parseJson(value) {
  try {
    return JSON.parse(value);
  } catch (_err) {
    return null;
  }
}

function contentResultFor(task) {
  if (task?.selected_tool !== "content_workflow_runtime") return null;
  const result = parseJson(task.output);
  return result?.package?.artifacts ? result : null;
}

export default function ExecutionTaskPage() {
  const params = useParams();
  const id = params?.id || "";
  const [task, setTask] = useState(null);
  const [project, setProject] = useState(null);
  const [employee, setEmployee] = useState(null);
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState(false);
  const [error, setError] = useState("");
  const [contextPackage, setContextPackage] = useState(null);
  const [executionControl, setExecutionControl] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [controlMode, setControlMode] = useState("");
  const [controlStep, setControlStep] = useState("");
  const [controlQuestion, setControlQuestion] = useState("");
  const [controlSummary, setControlSummary] = useState("");
  const [controlAssignee, setControlAssignee] = useState("");
  const [controlError, setControlError] = useState("");
  const [savingControl, setSavingControl] = useState(false);
  const [memoryOpen, setMemoryOpen] = useState(false);
  const [memoryType, setMemoryType] = useState("project");
  const [memoryTitle, setMemoryTitle] = useState("");
  const [memoryContent, setMemoryContent] = useState("");
  const [memoryTags, setMemoryTags] = useState("");
  const [memoryError, setMemoryError] = useState("");
  const [savingMemory, setSavingMemory] = useState(false);
  const [savedMemory, setSavedMemory] = useState(null);
  const loadVersion = useRef(0);

  const load = useCallback(async () => {
    if (!id) return;
    const version = ++loadVersion.current;
    setLoading(true);
    setError("");
    try {
      const taskPayload = await getTask(id);
      const [projectResult, employeeResult, jobResult, controlResult, timelineResult] = await Promise.allSettled([
        getProjects(),
        getEmployees(),
        getTaskJob(id),
        getTaskRun(id),
        getTaskRunTimeline(id),
      ]);
      const projectPayload = projectResult.status === "fulfilled" ? projectResult.value : {};
      const employeePayload = employeeResult.status === "fulfilled" ? employeeResult.value : {};
      const jobPayload = jobResult.status === "fulfilled" ? jobResult.value : {};
      const controlPayload = controlResult.status === "fulfilled" ? controlResult.value : null;
      const timelinePayload = timelineResult.status === "fulfilled" ? timelineResult.value : {};
      const nextTask = {
        ...taskPayload,
        ...jobPayload,
        status: jobPayload.task_status || taskPayload.status,
      };
      if (version !== loadVersion.current) return;
      setTask(nextTask);
      setExecutionControl(controlPayload);
      setTimeline(timelinePayload?.events || []);
      if (nextTask.context_package_id) {
        try {
          setContextPackage(await getContextPackage(nextTask.context_package_id));
        } catch (_err) {
          setContextPackage(null);
          setError("任务已读取，Context Package 暂时无法读取，可重新读取");
        }
      } else {
        setContextPackage(null);
      }
      setProject(
        (projectPayload?.projects || []).find(
          (item) => item.project_id === taskPayload.project_id
        ) || null
      );
      setEmployee(
        (employeePayload?.employees || []).find(
          (item) => item.id === taskPayload.employee_id
        ) || null
      );
      if ([projectResult, employeeResult, jobResult, controlResult, timelineResult].some((result) => result.status === "rejected")) {
        setError("任务已读取，部分执行事实暂时无法读取，可重新读取");
      }
    } catch (err) {
      if (version === loadVersion.current) {
        setError(err?.message || "任务读取失败");
      }
    } finally {
      if (version === loadVersion.current) setLoading(false);
    }
  }, [id]);

  useEffect(() => { load(); }, [load]);

  const taskStatus = task?.status;
  useEffect(() => {
    if (!["PENDING", "PARSED", "RUNNING", "RESUMED"].includes(taskStatus)) return undefined;
    const timer = setInterval(async () => {
      try {
        const [job, control, timelinePayload] = await Promise.all([
          getTaskJob(id),
          getTaskRun(id),
          getTaskRunTimeline(id),
        ]);
        setExecutionControl(control);
        setTimeline(timelinePayload?.events || []);
        if (["completed", "failed"].includes(job.status)) {
          const refreshed = await getTask(id);
          setTask({ ...refreshed, ...job, status: job.task_status });
        } else {
          setTask((current) => ({ ...current, ...job, status: job.task_status }));
        }
        if (
          job.context_package_id
          && job.context_package_id !== contextPackage?.id
        ) {
          setContextPackage(await getContextPackage(job.context_package_id));
        }
      } catch (err) {
        setError(err?.message || "执行状态读取失败");
      }
    }, 750);
    return () => clearInterval(timer);
  }, [contextPackage?.id, id, taskStatus]);

  async function run() {
    setStarting(true);
    setError("");
    try {
      const job = await startTaskJob(task.project_id, task.task_id);
      setTask((current) => ({ ...current, ...job, status: job.task_status }));
    } catch (err) {
      setError(err?.message || "任务执行失败");
    } finally {
      setStarting(false);
    }
  }

  function openControl(mode) {
    setControlMode(mode);
    setControlStep(executionControl?.current_step || "当前步骤");
    setControlQuestion(executionControl?.pending_question || "");
    setControlSummary(mode === "input" ? "" : executionControl?.context_summary || "");
    setControlAssignee(executionControl?.handoff_assignee_id || "");
    setControlError("");
  }

  async function submitControl(event) {
    event.preventDefault();
    setSavingControl(true);
    setControlError("");
    try {
      if (controlMode === "awaiting") {
        await pauseTaskForInput(task.task_id, {
          current_step: controlStep,
          question: controlQuestion,
          context_summary: controlSummary,
          responsible_id: controlAssignee,
          resume_parameters: {},
        });
      } else if (controlMode === "handoff") {
        await requestTaskHandoff(task.task_id, {
          current_step: controlStep,
          question: controlQuestion,
          context_summary: controlSummary,
          assignee_id: controlAssignee,
          resume_parameters: {},
        });
      } else if (controlMode === "input") {
        await supplyTaskInput(task.task_id, {
          input_summary: controlSummary,
          resume_parameters: {},
        });
      } else if (controlMode === "reassign") {
        await reassignTaskHandoff(task.task_id, controlAssignee);
      }
      setControlMode("");
      await load();
    } catch (err) {
      setControlError(err?.message || "执行控制操作失败");
    } finally {
      setSavingControl(false);
    }
  }

  async function acceptHandoff() {
    setStarting(true);
    setError("");
    try {
      await acceptTaskHandoff(task.task_id);
      await load();
    } catch (err) {
      setError(err?.message || "接管失败");
    } finally {
      setStarting(false);
    }
  }

  async function resumeExecution() {
    setStarting(true);
    setError("");
    try {
      await resumeTaskRun(task.task_id);
      await load();
    } catch (err) {
      setError(err?.message || "恢复执行失败");
    } finally {
      setStarting(false);
    }
  }

  async function cancelExecution() {
    if (!window.confirm("确认取消本次执行？取消后不可恢复。")) return;
    setStarting(true);
    setError("");
    try {
      await cancelTaskRun(task.task_id, "用户在 Task 详情取消执行");
      await load();
    } catch (err) {
      setError(err?.message || "取消执行失败");
    } finally {
      setStarting(false);
    }
  }

  function openMemory() {
    setMemoryType(task.project_id ? "project" : task.employee_id ? "employee" : "user");
    setMemoryTitle("");
    setMemoryContent("");
    setMemoryTags("");
    setMemoryError("");
    setMemoryOpen(true);
  }

  async function saveMemory(event) {
    event.preventDefault();
    setMemoryError("");
    if (!memoryTitle.trim() || !memoryContent.trim()) {
      setMemoryError("请填写 Memory 标题和内容");
      return;
    }
    setSavingMemory(true);
    try {
      const memory = await createMemoryEntry({
        memory_type: memoryType,
        title: memoryTitle.trim(),
        content: memoryContent.trim(),
        tags: memoryTags.split(/[,，]/).map((item) => item.trim()).filter(Boolean),
        project_id: memoryType === "project" ? task.project_id : null,
        employee_id: memoryType === "employee" ? task.employee_id : null,
        source_task_id: task.task_id,
        confidence: 1,
      });
      setSavedMemory(memory);
      setMemoryOpen(false);
    } catch (err) {
      setMemoryError(err?.message || "Memory 保存失败");
    } finally {
      setSavingMemory(false);
    }
  }

  if (loading) {
    return (
      <TerraShell
        topCrumb="执行工作台 / 任务详情"
        assistantContext={{ page: "task", task_id: id }}
      >
        <TerraLoadingSkeleton variant="page" />
      </TerraShell>
    );
  }
  if (error && !task) {
    return (
      <TerraShell
        topCrumb="执行工作台 / 任务详情"
        assistantContext={{ page: "task", task_id: id }}
      >
        <TerraErrorState message={error} onRetry={load} />
      </TerraShell>
    );
  }

  const status = STATUS[task?.status] || { label: task?.status || "未记录", color: "grey" };
  const executions = task?.executions || [];
  const modelUsage = task?.model_usage;
  const canRun = ["INIT", "FAILED"].includes(task?.status);
  const canCaptureMemory = ["COMPLETED", "FAILED"].includes(task?.status);
  const isActive = ["PENDING", "PARSED", "RUNNING", "RESUMED"].includes(task?.status);
  const isAwaiting = task?.status === "AWAITING_INPUT";
  const isHandoff = task?.status === "HUMAN_HANDOFF";
  const canRequestHandoff = isActive || task?.status === "FAILED";
  const canCancel = isActive || isAwaiting || isHandoff;
  const contentResult = contentResultFor(task);
  const artifacts = task?.artifacts || [];
  const contentArtifacts = contentResult?.package?.artifacts || [];
  const topicArtifact = contentArtifacts.find((item) => item.metadata?.stage === "topic");
  const topic = parseJson(topicArtifact?.body);
  const retrospectiveArtifact = contentArtifacts.find(
    (item) => item.metadata?.stage === "retrospective"
  );
  const retrospective = parseJson(retrospectiveArtifact?.body);
  const contentPlatforms = contentResult?.package?.platforms_targeted || [];
  const originalGeneralWork = executionControl?.original_general_work;
  const boundWorkUnverified = Boolean(task?.work_ref && !executionControl);

  return (
    <TerraShell
      topCrumb="执行工作台 / 任务详情"
      topbarExtra={<RuntimeCapabilitySwitcher />}
      assistantContext={{ page: "task", task_id: id }}
    >
      <TerraBackLink href="/ceo-office/execution">返回执行工作台</TerraBackLink>
      <TerraPageHead
        title={task.content}
        subtitle={`任务 ID：${task.task_id}`}
        pill={{ text: status.label, icon: "i-checklist" }}
        facts={[
          { value: project?.name || "未分配", label: "项目" },
          { value: employee?.name || task.employee_name || "未分配", label: "执行员工" },
          { value: artifacts.length, label: "成果" },
        ]}
        actions={originalGeneralWork ? <a href={`${workspaceEntryHref(originalGeneralWork.workspace_id)}#work-${encodeURIComponent(originalGeneralWork.work_ref)}`} className="text-sm font-bold text-ui-primary">返回原工作处理</a> : boundWorkUnverified ? null : canRun || canCaptureMemory || canCancel ? (
          <div className="flex flex-wrap gap-2">
            {canCaptureMemory && (
              <TerraButton variant="ghost" onClick={openMemory}>沉淀经验</TerraButton>
            )}
            {canRun && (
              <TerraButton onClick={run} disabled={starting}>
                {starting ? "启动中…" : task.status === "FAILED" ? "重新执行" : "执行任务"}
              </TerraButton>
            )}
            {isActive && (
              <>
                <TerraButton variant="ghost" onClick={() => openControl("awaiting")}>
                  等待补充
                </TerraButton>
              </>
            )}
            {canRequestHandoff && (
              <TerraButton variant="ghost" onClick={() => openControl("handoff")}>
                人工接管
              </TerraButton>
            )}
            {isAwaiting && (
              <>
                <TerraButton variant="ghost" onClick={() => openControl("input")}>
                  补充信息
                </TerraButton>
                <TerraButton variant="ghost" onClick={() => openControl("handoff")}>
                  转人工接管
                </TerraButton>
                <TerraButton onClick={resumeExecution} disabled={starting}>
                  恢复 AI 执行
                </TerraButton>
              </>
            )}
            {isHandoff && (
              <>
                <TerraButton variant="ghost" onClick={acceptHandoff} disabled={starting}>
                  接受接管
                </TerraButton>
                <TerraButton variant="ghost" onClick={() => openControl("reassign")}>
                  转派接管人
                </TerraButton>
                <TerraButton onClick={resumeExecution} disabled={starting}>
                  恢复 AI 执行
                </TerraButton>
              </>
            )}
            {canCancel && (
              <TerraButton variant="danger" onClick={cancelExecution} disabled={starting}>
                取消执行
              </TerraButton>
            )}
          </div>
        ) : null}
      />

      {originalGeneralWork && <TerraBoundary className="mb-4">此 Task 属于原 General Work。补充、续接和停止请在原工作处理；Task 结果仅作来源记录。</TerraBoundary>}
      {boundWorkUnverified && <TerraBoundary className="mb-4">原工作范围暂时无法核实，请先重新读取任务状态再操作。</TerraBoundary>}

      {error && <p className="text-xs text-ui-red mb-3">{error}</p>}
      {savedMemory && (
        <TerraBoundary className="mb-4">
          Memory 已确认沉淀：{savedMemory.title}（{savedMemory.memory_level}）
        </TerraBoundary>
      )}

      <div className="grid grid-cols-12 gap-3.5">
        <TerraCard className="col-span-12 lg:col-span-8">
          <TerraCardHeader icon="i-checklist" iconClass="amber" title="任务目标" />
          <p className="text-sm text-ui-txt-2 leading-relaxed">{task.content}</p>

          <div className="mt-5">
            <h3 className="text-xs font-bold text-ui-txt-2 mb-2">状态流</h3>
            <div className="flex flex-wrap gap-2">
              {(task.state_flow || []).map((item, index) => {
                const itemStatus = STATUS[item] || { label: item, color: "grey" };
                return (
                  <TerraTag key={`${item}-${index}`} color={itemStatus.color}>
                    {index + 1}. {itemStatus.label}
                  </TerraTag>
                );
              })}
            </div>
          </div>
        </TerraCard>

        <TerraCard className="col-span-12 lg:col-span-4 min-w-0">
          <TerraCardHeader icon="i-info" iconClass="primary" title="执行事实" />
          <dl className="space-y-2">
            {[
              { label: "所属项目", value: project?.name || "未分配" },
              { label: "执行员工", value: employee?.name || task.employee_name || "未分配" },
              { label: "执行能力", value: task.selected_tool || task.requested_capability_id || "未记录" },
              { label: "最终模型", value: modelUsage?.model_name || "未记录" },
              { label: "Token", value: modelUsage ? modelUsage.total_tokens : "未记录" },
              {
                label: "执行成本",
                value: modelUsage?.estimated_cost > 0
                  ? `$${Number(modelUsage.estimated_cost).toFixed(4)} ${modelUsage.currency}`
                  : Number(task.cost || 0) > 0
                    ? `$${Number(task.cost).toFixed(4)}`
                    : "未记录",
              },
              {
                label: "模型回退",
                value: modelUsage
                  ? modelUsage.fallback_used
                    ? `${modelUsage.fallback_from_model} → ${modelUsage.model_name}`
                    : "未触发"
                  : "未记录",
              },
              { label: "当前状态", value: status.label },
            ].map((row) => (
              <div key={row.label} className="grid grid-cols-[auto_minmax(0,1fr)] gap-3 bg-ui-surface-2 rounded-ui-sm px-3 py-2">
                <dt className="text-xs text-ui-txt-3">{row.label}</dt>
                <dd className="min-w-0 text-xs text-ui-txt font-medium text-right break-all">{row.value}</dd>
              </div>
            ))}
          </dl>
        </TerraCard>

        <TerraCard className="col-span-12">
          <TerraCardHeader icon="i-timeline" iconClass="cyan" title="执行时间线" />
          {(isAwaiting || isHandoff) && (
            <TerraBoundary className="mb-4">
              <strong>{isAwaiting ? "等待补充信息" : "人工接管中"}</strong>
              <span className="ml-2">
                {executionControl?.pending_question || executionControl?.context_summary || "执行已安全暂停"}
              </span>
              {executionControl?.handoff_assignee_id && (
                <span className="ml-2">责任人：{executionControl.handoff_assignee_id}</span>
              )}
            </TerraBoundary>
          )}
          {timeline.length ? (
            <ol className="space-y-2">
              {timeline.map((event) => {
                const color = event.event_type === "execution_completed"
                  ? "green"
                  : ["execution_failed", "human_handoff_requested"].includes(event.event_type)
                    ? "red"
                    : ["awaiting_input", "input_supplied"].includes(event.event_type)
                      ? "amber"
                      : event.event_type === "execution_cancelled"
                        ? "grey"
                        : "cyan";
                const detail = event.usage_record_id
                  ? `${event.provider_id || "provider"} / ${event.model_name || "model"} · Usage ${event.usage_record_id}`
                  : event.tool_name
                    ? event.tool_name
                    : event.question || event.context_summary || event.assignee_id || event.execution_status || "已记录";
                return (
                  <li
                    key={event.event_id}
                    className="grid grid-cols-[auto_minmax(0,1fr)] gap-3 rounded-ui-sm border border-ui-line bg-ui-surface-2 px-3 py-2.5"
                  >
                    <span className={`mt-1.5 h-2 w-2 rounded-full ${EVENT_DOT[color]}`} />
                    <div className="min-w-0">
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <span className="text-xs font-bold text-ui-txt">
                          {EVENT_LABEL[event.event_type] || event.event_type}
                        </span>
                        <time className="text-ui-1 text-ui-txt-3">
                          {formatTime(event.timestamp)}
                        </time>
                      </div>
                      <p className="mt-1 break-words text-xs text-ui-txt-2">{detail}</p>
                    </div>
                  </li>
                );
              })}
            </ol>
          ) : (
            <TerraEmpty icon="i-timeline">尚无结构化执行事件。</TerraEmpty>
          )}
        </TerraCard>

        <TerraCard className="col-span-12">
          <TerraCardHeader icon="i-memory" iconClass="violet" title="Context Package" />
          {contextPackage ? (
            <>
              <dl className="grid grid-cols-1 gap-2 sm:grid-cols-3">
                {[
                  { label: "Package ID", value: contextPackage.id },
                  { label: "状态", value: contextPackage.status === "ready" ? "已检索相关上下文" : "最小上下文" },
                  { label: "内容摘要", value: contextPackage.package_sha256 },
                ].map((row) => (
                  <div key={row.label} className="min-w-0 rounded-ui-sm bg-ui-surface-2 px-3 py-2">
                    <dt className="text-ui-1 text-ui-txt-3">{row.label}</dt>
                    <dd className="mt-1 break-all text-xs font-medium text-ui-txt">{row.value || "未记录"}</dd>
                  </div>
                ))}
              </dl>
              <div className="mt-4 grid grid-cols-1 gap-3 lg:grid-cols-2">
                <div>
                  <h3 className="mb-2 text-xs font-bold text-ui-txt-2">相关 Memory</h3>
                  {contextPackage.relevant_memory?.length ? (
                    <div className="space-y-2">
                      {contextPackage.relevant_memory.map((item) => (
                        <div key={item.id} className="rounded-ui-sm bg-ui-surface-2 px-3 py-2">
                          <div className="flex flex-wrap items-center gap-2">
                            <span className="text-xs font-bold text-ui-txt">{item.title}</span>
                            <TerraTag color="violet">{item.memory_level}</TerraTag>
                          </div>
                          <p className="mt-1 text-xs leading-relaxed text-ui-txt-2">{item.content}</p>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <TerraEmpty>未检索到相关 Memory。</TerraEmpty>
                  )}
                </div>
                <div>
                  <h3 className="mb-2 text-xs font-bold text-ui-txt-2">相关 Knowledge</h3>
                  {contextPackage.relevant_knowledge?.length ? (
                    <div className="space-y-2">
                      {contextPackage.relevant_knowledge.map((item) => (
                        <div key={item.id} className="rounded-ui-sm bg-ui-surface-2 px-3 py-2">
                          <div className="flex flex-wrap items-center gap-2">
                            <span className="text-xs font-bold text-ui-txt">{item.title}</span>
                            <TerraTag color="green">{item.scope_name}</TerraTag>
                          </div>
                          <p className="mt-1 text-xs leading-relaxed text-ui-txt-2">{item.summary}</p>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <TerraEmpty>未检索到相关 Knowledge。</TerraEmpty>
                  )}
                </div>
              </div>
              <div className="mt-4 flex flex-wrap gap-2">
                {(contextPackage.required_tools || []).map((item) => (
                  <TerraTag key={item} color="cyan">{item}</TerraTag>
                ))}
                {(contextPackage.constraints || []).map((item) => (
                  <TerraTag key={item} color="grey">{item}</TerraTag>
                ))}
              </div>
              <p className="mt-3 text-xs text-ui-txt-3">
                输出要求：{contextPackage.output_requirement || "未记录"}
              </p>
            </>
          ) : (
            <TerraEmpty icon="i-memory">
              尚未生成 Context Package；执行任务前会自动构建。
            </TerraEmpty>
          )}
        </TerraCard>

        {contentResult ? (
          <>
            <TerraCard className="col-span-12">
              <TerraCardHeader icon="i-trending_up" iconClass="amber" title="热点依据与选题" />
              <dl className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div className="bg-ui-surface-2 rounded-ui-sm px-3 py-2">
                  <dt className="text-ui-1 text-ui-txt-3">热点来源</dt>
                  <dd className="text-sm text-ui-txt break-all mt-1">
                    {topic?.trend_source || "未记录"}
                  </dd>
                </div>
                <div className="bg-ui-surface-2 rounded-ui-sm px-3 py-2">
                  <dt className="text-ui-1 text-ui-txt-3">选题角度</dt>
                  <dd className="text-sm text-ui-txt mt-1">{topic?.topic?.angle || "未记录"}</dd>
                </div>
              </dl>
              <h3 className="font-ui-sans font-bold text-xl text-ui-txt mt-4">
                {topic?.topic?.title || topicArtifact?.title || "未记录"}
              </h3>
              <p className="text-sm text-ui-txt-2 leading-relaxed mt-2">
                {topic?.trend_analysis || "未记录"}
              </p>
            </TerraCard>

            {contentPlatforms.map((platform) => {
              const copy = contentArtifacts.find(
                (item) => item.platform === platform && ["copywriting", "script"].includes(item.type)
              );
              const image = contentArtifacts.find(
                (item) => item.platform === platform && item.type === "media_asset"
              );
              return (
                <TerraCard key={platform} className="col-span-12 lg:col-span-4 min-w-0">
                  <TerraCardHeader
                    icon="i-campaign"
                    iconClass="primary"
                    title={PLATFORM_LABEL[platform] || platform}
                  />
                  <h3 className="text-sm font-bold text-ui-txt">{copy?.title || "未记录"}</h3>
                  <p className="text-sm text-ui-txt-2 whitespace-pre-wrap leading-relaxed mt-2">
                    {copy?.body || "未记录"}
                  </p>
                  {image?.body ? (
                    <Image
                      src={`data:image/svg+xml;charset=utf-8,${encodeURIComponent(image.body)}`}
                      alt={`${PLATFORM_LABEL[platform] || platform} 内容封面`}
                      width={1080}
                      height={1440}
                      unoptimized
                      className="w-full aspect-[3/4] object-cover rounded-ui-sm border border-ui-line mt-4"
                    />
                  ) : (
                    <TerraEmpty>图片资产未记录</TerraEmpty>
                  )}
                </TerraCard>
              );
            })}

            <TerraCard className="col-span-12">
              <TerraCardHeader icon="i-monitoring" iconClass="green" title="复盘计划" />
              <p className="text-sm text-ui-txt-2">{retrospective?.hypothesis || "未记录"}</p>
              <div className="flex flex-wrap gap-2 mt-3">
                {(retrospective?.metrics || []).map((metric) => (
                  <TerraTag key={metric} color="cyan">{metric}</TerraTag>
                ))}
              </div>
              <p className="text-xs text-ui-txt-3 mt-3">
                {retrospective?.next_review || "未记录"}
              </p>
              <p className="text-xs font-semibold text-ui-amber mt-3">外部发布未执行</p>
            </TerraCard>
          </>
        ) : (
          <TerraCard className="col-span-12">
            <TerraCardHeader
              icon={task.status === "FAILED" ? "i-error" : "i-inventory_2"}
              iconClass={task.status === "FAILED" ? "red" : "green"}
              title={task.status === "FAILED" ? "失败原因" : "任务成果"}
            />
            {task.error ? (
              <p className="text-sm text-ui-red whitespace-pre-wrap break-words">{task.error}</p>
            ) : artifacts.length && task.output ? (
              <pre className="text-sm text-ui-txt-2 whitespace-pre-wrap break-words font-sans">
                {task.output}
              </pre>
            ) : (
              <TerraEmpty icon="i-inventory_2">尚未登记任务成果。</TerraEmpty>
            )}
          </TerraCard>
        )}
      </div>

      <TerraBoundary className="mt-4">
        本页只展示结构化执行事件和安全摘要，不展示模型隐藏思维链或底层调试日志。
      </TerraBoundary>

      <TerraDrawer
        open={Boolean(controlMode)}
        title={{
          awaiting: "等待补充信息",
          handoff: "请求人工接管",
          input: "补充执行信息",
          reassign: "转派接管人",
        }[controlMode] || "执行控制"}
        description="操作将持久化到原 Task Run；刷新或重启后状态不会丢失。"
        onClose={() => setControlMode("")}
      >
        <form onSubmit={submitControl} className="space-y-4">
          {["awaiting", "handoff"].includes(controlMode) && (
            <>
              <div>
                <label htmlFor="control-step" className="mb-1.5 block text-xs font-bold text-ui-txt-2">
                  当前执行步骤 *
                </label>
                <input
                  id="control-step"
                  required
                  value={controlStep}
                  onChange={(event) => setControlStep(event.target.value)}
                  className="w-full rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-sm text-ui-txt outline-none"
                />
              </div>
              <div>
                <label htmlFor="control-question" className="mb-1.5 block text-xs font-bold text-ui-txt-2">
                  待解决问题 *
                </label>
                <textarea
                  id="control-question"
                  required
                  rows={3}
                  value={controlQuestion}
                  onChange={(event) => setControlQuestion(event.target.value)}
                  className="w-full resize-y rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-sm text-ui-txt outline-none"
                />
              </div>
            </>
          )}
          {controlMode !== "reassign" && (
            <div>
              <label htmlFor="control-summary" className="mb-1.5 block text-xs font-bold text-ui-txt-2">
                {controlMode === "input" ? "补充信息" : "已有上下文安全摘要"} *
              </label>
              <textarea
                id="control-summary"
                required
                rows={5}
                value={controlSummary}
                onChange={(event) => setControlSummary(event.target.value)}
                placeholder={controlMode === "input" ? "填写恢复执行所需的信息" : "只填写安全摘要，不粘贴密钥或凭证"}
                className="w-full resize-y rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-sm text-ui-txt outline-none"
              />
            </div>
          )}
          {["awaiting", "handoff", "reassign"].includes(controlMode) && (
            <div>
              <label htmlFor="control-assignee" className="mb-1.5 block text-xs font-bold text-ui-txt-2">
                接管人或责任人 {controlMode === "reassign" ? "*" : ""}
              </label>
              <input
                id="control-assignee"
                required={controlMode === "reassign"}
                value={controlAssignee}
                onChange={(event) => setControlAssignee(event.target.value)}
                placeholder="留空则使用当前 Owner"
                className="w-full rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-sm text-ui-txt outline-none"
              />
            </div>
          )}
          {controlError && <p className="text-xs text-ui-red">{controlError}</p>}
          <div className="flex justify-end gap-3 pt-2">
            <TerraButton type="button" variant="ghost" onClick={() => setControlMode("")}>
              取消
            </TerraButton>
            <TerraButton type="submit" disabled={savingControl}>
              {savingControl ? "保存中…" : "确认"}
            </TerraButton>
          </div>
        </form>
      </TerraDrawer>

      <TerraDrawer
        open={memoryOpen}
        title="沉淀经验"
        description="由你确认长期有效的经验；系统不会自动把执行日志写入 Memory。"
        onClose={() => setMemoryOpen(false)}
      >
        <form onSubmit={saveMemory} className="space-y-4">
          <div>
            <label htmlFor="task-memory-type" className="mb-1.5 block text-xs font-bold text-ui-txt-2">
              Memory 类型 *
            </label>
            <select
              id="task-memory-type"
              value={memoryType}
              onChange={(event) => setMemoryType(event.target.value)}
              className="w-full rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-sm text-ui-txt outline-none"
            >
              <option value="user">用户 Memory</option>
              {task.project_id && <option value="project">项目 Memory</option>}
              {task.employee_id && <option value="employee">员工 Memory</option>}
            </select>
          </div>
          <div>
            <label htmlFor="task-memory-title" className="mb-1.5 block text-xs font-bold text-ui-txt-2">
              标题 *
            </label>
            <input
              id="task-memory-title"
              value={memoryTitle}
              onChange={(event) => setMemoryTitle(event.target.value)}
              placeholder="例如：发布验收原则"
              className="w-full rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-sm text-ui-txt outline-none"
            />
          </div>
          <div>
            <label htmlFor="task-memory-content" className="mb-1.5 block text-xs font-bold text-ui-txt-2">
              经验内容 *
            </label>
            <textarea
              id="task-memory-content"
              rows={7}
              value={memoryContent}
              onChange={(event) => setMemoryContent(event.target.value)}
              placeholder="提炼未来仍有价值的方法、规则或问题解决经验"
              className="w-full resize-y rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-sm text-ui-txt outline-none"
            />
          </div>
          <div>
            <label htmlFor="task-memory-tags" className="mb-1.5 block text-xs font-bold text-ui-txt-2">
              标签
            </label>
            <input
              id="task-memory-tags"
              value={memoryTags}
              onChange={(event) => setMemoryTags(event.target.value)}
              placeholder="用逗号分隔，最多 10 个"
              className="w-full rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-sm text-ui-txt outline-none"
            />
          </div>
          {memoryError && <p className="text-xs text-ui-red">{memoryError}</p>}
          <div className="flex justify-end gap-3 pt-2">
            <TerraButton type="button" variant="ghost" onClick={() => setMemoryOpen(false)}>
              取消
            </TerraButton>
            <TerraButton type="submit" disabled={savingMemory}>
              {savingMemory ? "保存中…" : "确认沉淀"}
            </TerraButton>
          </div>
        </form>
      </TerraDrawer>
    </TerraShell>
  );
}
