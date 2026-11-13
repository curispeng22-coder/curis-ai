"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useParams } from "next/navigation";
import TerraShell from "../../../../components/terra/TerraShell.js";
import RuntimeCapabilitySwitcher from "../../../../components/terra/RuntimeCapabilitySwitcher.js";
import {
  TerraBackLink,
  TerraBoundary,
  TerraButton,
  TerraCard,
  TerraCardHeader,
  TerraEmpty,
  TerraPageHead,
  TerraTag,
} from "../../../../components/terra/TerraPrimitives.js";
import { TerraErrorState, TerraLoadingSkeleton } from "../../../../components/terra/TerraState.js";
import {
  getDepartments,
  getEmployees,
  getProject,
  getProjectArtifacts,
  getTaskJob,
  getTasks,
  startTaskJob,
} from "../../../../lib/api.js";
import TaskFormDrawer from "./TaskFormDrawer.js";
import DevelopmentRunDrawer from "./DevelopmentRunDrawer.js";
import ContentRunDrawer from "./ContentRunDrawer.js";

const TABS = [
  { key: "overview", label: "概览" },
  { key: "tasks", label: "任务" },
  { key: "knowledge", label: "资料" },
  { key: "artifacts", label: "成果" },
  { key: "metrics", label: "数据" },
];

const STATUS = {
  planned: { label: "规划中", color: "grey" },
  active: { label: "执行中", color: "green" },
  blocked: { label: "阻塞", color: "red" },
  completed: { label: "已完成", color: "cyan" },
  archived: { label: "已归档", color: "amber" },
};

const TASK_STATUS = {
  INIT: { label: "待执行", color: "grey" },
  PENDING: { label: "排队中", color: "amber" },
  PARSED: { label: "执行中", color: "primary" },
  RUNNING: { label: "执行中", color: "primary" },
  COMPLETED: { label: "已完成", color: "green" },
  FAILED: { label: "失败", color: "red" },
};

export default function ProjectWorkspacePage() {
  const params = useParams();
  const id = params?.id || "";
  const [project, setProject] = useState(null);
  const [departments, setDepartments] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [artifacts, setArtifacts] = useState([]);
  const [tab, setTab] = useState("overview");
  const [taskDrawerOpen, setTaskDrawerOpen] = useState(false);
  const [developmentDrawerOpen, setDevelopmentDrawerOpen] = useState(false);
  const [contentDrawerOpen, setContentDrawerOpen] = useState(false);
  const [jobStatus, setJobStatus] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [taskError, setTaskError] = useState("");
  const loadVersion = useRef(0);

  const loadAll = useCallback(async () => {
    if (!id) return;
    const version = ++loadVersion.current;
    setLoading(true);
    setError("");
    try {
      const projectPayload = await getProject(id);
      const [departmentResult, employeeResult, taskResult, artifactResult] = await Promise.allSettled([
        getDepartments(),
        getEmployees(),
        getTasks(),
        getProjectArtifacts(id),
      ]);
      if (taskResult.status === "rejected") throw taskResult.reason;
      if (version !== loadVersion.current) return;
      setProject(projectPayload);
      setDepartments(
        departmentResult.status === "fulfilled"
          ? departmentResult.value?.departments || []
          : []
      );
      setEmployees(
        employeeResult.status === "fulfilled"
          ? employeeResult.value?.employees || []
          : []
      );
      setTasks((Array.isArray(taskResult.value) ? taskResult.value : []).filter(
        (item) => item.project_id === id
      ));
      setArtifacts(
        artifactResult.status === "fulfilled"
          ? artifactResult.value?.artifacts || []
          : []
      );
    } catch (err) {
      if (version === loadVersion.current) {
        setError(err?.message || "项目工作台读取失败");
      }
    } finally {
      if (version === loadVersion.current) setLoading(false);
    }
  }, [id]);

  useEffect(() => { loadAll(); }, [loadAll]);

  async function runTask(task) {
    setTaskError("");
    setJobStatus((current) => ({ ...current, [task.task_id]: "queued" }));
    try {
      const job = await startTaskJob(id, task.task_id);
      setJobStatus((current) => ({ ...current, [task.task_id]: job.status }));
      for (let attempt = 0; attempt < 120; attempt += 1) {
        await new Promise((resolve) => setTimeout(resolve, 500));
        const currentJob = await getTaskJob(job.job_id);
        setJobStatus((current) => ({ ...current, [task.task_id]: currentJob.status }));
        if (!["queued", "running"].includes(currentJob.status)) break;
      }
      await loadAll();
    } catch (err) {
      setTaskError(err?.message || "任务执行失败");
      setJobStatus((current) => ({ ...current, [task.task_id]: "failed" }));
    }
  }

  const department = useMemo(
    () => departments.find((item) => item.id === project?.department_id),
    [departments, project?.department_id]
  );
  const owner = useMemo(
    () => employees.find((item) => item.id === project?.owner_employee_id),
    [employees, project?.owner_employee_id]
  );
  const status = STATUS[project?.status] || { label: project?.status || "未记录", color: "grey" };
  const outputCount = tasks.filter((item) => item.output).length;

  if (loading) {
    return (
      <TerraShell
        topCrumb="项目中心 / 项目工作台"
        assistantContext={{ page: "project", project_id: id }}
      >
        <TerraLoadingSkeleton variant="page" />
      </TerraShell>
    );
  }
  if (error || !project) {
    return (
      <TerraShell
        topCrumb="项目中心 / 项目工作台"
        assistantContext={{ page: "project", project_id: id }}
      >
        <TerraErrorState message={error || "项目不存在"} onRetry={loadAll} />
      </TerraShell>
    );
  }

  return (
    <TerraShell
      topCrumb="项目中心 / 项目工作台"
      topbarExtra={<RuntimeCapabilitySwitcher />}
      assistantContext={{ page: "project", project_id: id }}
    >
      <TerraBackLink href="/ceo-office/projects">返回项目中心</TerraBackLink>
      <TerraPageHead
        title={project.name}
        subtitle={`项目 ID：${project.project_id}`}
        pill={{ text: status.label, icon: "i-folder_open" }}
        facts={[
          { value: tasks.length, label: "任务" },
          { value: outputCount, label: "已有输出" },
        ]}
      />

      <nav className="flex flex-wrap gap-1.5 mb-4" aria-label="项目工作台视图">
        {TABS.map((item) => (
          <button
            key={item.key}
            type="button"
            onClick={() => setTab(item.key)}
            className={`px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${
              tab === item.key
                ? "bg-ui-primary text-ui-primary-fg"
                : "bg-ui-surface-2 text-ui-txt-2 hover:bg-ui-surface-3"
            }`}
          >
            {item.label}
          </button>
        ))}
      </nav>

      {tab === "overview" && (
        <div className="grid grid-cols-12 gap-3.5">
          <TerraCard className="col-span-12 lg:col-span-8">
            <TerraCardHeader icon="i-flag" iconClass="primary" title="项目目标" />
            <p className="text-sm text-ui-txt-2 leading-relaxed">{project.goal}</p>
            <div className="mt-4">
              <div className="text-ui-1 text-ui-txt-3 mb-1">项目说明</div>
              <p className="text-sm text-ui-txt-2 leading-relaxed">
                {project.description || "未记录"}
              </p>
            </div>
          </TerraCard>

          <TerraCard className="col-span-12 lg:col-span-4">
            <TerraCardHeader icon="i-groups" iconClass="cyan" title="项目团队" />
            {owner ? (
              <div className="flex items-center gap-3 rounded-ui-sm border border-ui-line p-3">
                <span className="w-9 h-9 rounded-full bg-ui-primary text-ui-primary-fg grid place-items-center font-bold">
                  {owner.name?.slice(0, 1) || "?"}
                </span>
                <div className="min-w-0 flex-1">
                  <div className="text-sm font-semibold text-ui-txt truncate">{owner.name}</div>
                  <div className="text-ui-1 text-ui-txt-3">项目负责人 · {owner.role}</div>
                </div>
                <TerraTag color="green">负责人</TerraTag>
              </div>
            ) : (
              <TerraEmpty>未分配项目负责人</TerraEmpty>
            )}
          </TerraCard>

          <TerraCard className="col-span-12">
            <TerraCardHeader icon="i-info" iconClass="surface" title="项目基础信息" />
            <dl className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
              {[
                { label: "所属业务部门", value: department?.name || "未分配" },
                { label: "项目负责人", value: owner?.name || "未分配" },
                {
                  label: "业务类型",
                  value: department?.department_type === "content.growth"
                    ? department.department_type
                    : project.project_type || "未记录",
                },
                { label: "当前阶段", value: "未记录" },
              ].map((item) => (
                <div key={item.label} className="bg-ui-surface-2 rounded-ui-sm px-3 py-2">
                  <dt className="text-ui-1 text-ui-txt-3">{item.label}</dt>
                  <dd className="text-sm text-ui-txt font-medium mt-0.5">{item.value}</dd>
                </div>
              ))}
            </dl>
          </TerraCard>
        </div>
      )}

      {tab === "tasks" && (
        <TerraCard>
          <div className="flex items-start justify-between gap-3">
            <TerraCardHeader icon="i-checklist" iconClass="primary" title="项目任务" />
            <div className="flex flex-wrap justify-end gap-2">
              {department?.department_type === "software_rnd" && (
                <TerraButton
                  size="sm"
                  variant="ghost"
                  icon="i-terminal"
                  onClick={() => setDevelopmentDrawerOpen(true)}
                >
                  启动研发工作流
                </TerraButton>
              )}
              {department?.department_type === "content.growth" && (
                <TerraButton
                  size="sm"
                  variant="ghost"
                  icon="i-auto_awesome"
                  onClick={() => setContentDrawerOpen(true)}
                >
                  启动内容工作流
                </TerraButton>
              )}
              <TerraButton size="sm" icon="i-add" onClick={() => setTaskDrawerOpen(true)}>
                创建任务
              </TerraButton>
            </div>
          </div>
          {taskError && <p className="text-xs text-ui-red mb-3">{taskError}</p>}
          {tasks.length === 0 ? (
            <TerraEmpty icon="i-checklist">
              当前项目暂无任务。创建后可交由 AI 员工异步执行。
            </TerraEmpty>
          ) : (
            <div className="space-y-2">
              {tasks.map((task) => {
                const statusKey = jobStatus[task.task_id] === "queued"
                  ? "PENDING"
                  : jobStatus[task.task_id] === "running"
                    ? "RUNNING"
                    : task.status;
                const taskStatus = TASK_STATUS[statusKey] || { label: statusKey || "未记录", color: "grey" };
                const isRunning = ["queued", "running"].includes(jobStatus[task.task_id])
                  || ["PENDING", "PARSED", "RUNNING"].includes(task.status);
                return (
                  <div
                    key={task.task_id}
                    className="rounded-ui-sm border border-ui-line px-3 py-2.5 hover:border-ui-primary-light"
                  >
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0">
                      <a
                        href={`/ceo-office/execution/tasks/${task.task_id}`}
                        className="text-sm font-semibold text-ui-txt no-underline hover:text-ui-primary"
                      >
                        {task.content}
                      </a>
                      <p className="text-ui-1 text-ui-txt-3 mt-1">
                        执行者：{task.employee_name || "未分配"}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <TerraTag color={taskStatus.color}>{taskStatus.label}</TerraTag>
                      {["INIT", "FAILED"].includes(task.status) && (
                        <TerraButton
                          size="sm"
                          variant="ghost"
                          disabled={isRunning}
                          onClick={() => runTask(task)}
                        >
                          {task.status === "FAILED" ? "重试" : "执行"}
                        </TerraButton>
                      )}
                    </div>
                  </div>
                  {task.error && <p className="text-ui-1 text-ui-red mt-2">{task.error}</p>}
                </div>
                );
              })}
            </div>
          )}
        </TerraCard>
      )}

      {tab === "knowledge" && (
        <TerraCard>
          <TerraCardHeader icon="i-description" iconClass="cyan" title="项目资料" />
          <TerraEmpty icon="i-description">
            暂无项目资料。独立 Knowledge 对象将在资料 Sprint 接入，本页不生成本地草稿。
          </TerraEmpty>
        </TerraCard>
      )}

      {tab === "artifacts" && (
        <TerraCard>
          <TerraCardHeader icon="i-inventory_2" iconClass="green" title="项目成果" />
          {artifacts.length === 0 ? (
            <TerraEmpty icon="i-inventory_2">
              暂无项目成果。任务成功执行并登记成果后会显示在这里。
            </TerraEmpty>
          ) : (
            <div className="space-y-2">
              {artifacts.map((artifact) => (
                <a
                  key={artifact.artifact_id}
                  href={`/ceo-office/execution/tasks/${artifact.task_id}`}
                  className="block rounded-ui-sm border border-ui-line px-3 py-2.5 no-underline hover:border-ui-primary-light"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <div className="text-sm font-semibold text-ui-txt">{artifact.title}</div>
                      <div className="mt-1 text-ui-1 text-ui-txt-3">
                        任务成果 · {artifact.artifact_type}
                      </div>
                    </div>
                    <TerraTag color="green">{artifact.status}</TerraTag>
                  </div>
                </a>
              ))}
            </div>
          )}
        </TerraCard>
      )}

      {tab === "metrics" && (
        <TerraCard>
          <TerraCardHeader icon="i-bar_chart" iconClass="violet" title="项目数据" />
          <dl className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {[
              { label: "任务总数", value: tasks.length },
              { label: "已有输出", value: outputCount },
              { label: "经营指标", value: "未记录" },
            ].map((item) => (
              <div key={item.label} className="bg-ui-surface-2 rounded-ui-sm px-3 py-3">
                <dt className="text-ui-1 text-ui-txt-3">{item.label}</dt>
                <dd className="font-ui-sans font-bold text-xl text-ui-primary mt-1">{item.value}</dd>
              </div>
            ))}
          </dl>
        </TerraCard>
      )}

      <TerraBoundary className="mt-4">
        工作台只展示当前 Project、Task 与其真实成果；未接入的资料和经营数据保持空状态。
      </TerraBoundary>

      <TaskFormDrawer
        open={taskDrawerOpen}
        project={project}
        employees={employees}
        onClose={() => setTaskDrawerOpen(false)}
        onSuccess={async () => {
          setTaskDrawerOpen(false);
          await loadAll();
        }}
      />
      <DevelopmentRunDrawer
        open={developmentDrawerOpen}
        project={project}
        tasks={tasks}
        onClose={() => setDevelopmentDrawerOpen(false)}
      />
      <ContentRunDrawer
        open={contentDrawerOpen}
        project={project}
        tasks={tasks}
        onClose={() => setContentDrawerOpen(false)}
      />
    </TerraShell>
  );
}
