"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import TerraShell from "../../../components/terra/TerraShell.js";
import {
  TerraCard,
  TerraEmpty,
  TerraPageHead,
  TerraSearch,
  TerraTag,
} from "../../../components/terra/TerraPrimitives.js";
import { TerraErrorState, TerraLoadingSkeleton } from "../../../components/terra/TerraState.js";
import { TerraIcon } from "../../../components/terra/TerraIcons.js";
import { getEmployees, getProjects, getTasks } from "../../../lib/api.js";

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

export default function ExecutionPage() {
  const [tasks, setTasks] = useState([]);
  const [projects, setProjects] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const loadVersion = useRef(0);

  async function loadAll() {
    const version = ++loadVersion.current;
    setLoading(true);
    setError("");
    try {
      const taskPayload = await getTasks();
      const projectPayload = await getProjects();
      const employeePayload = await getEmployees();
      if (version !== loadVersion.current) return;
      setTasks(Array.isArray(taskPayload) ? taskPayload : []);
      setProjects(projectPayload?.projects || []);
      setEmployees(employeePayload?.employees || []);
    } catch (err) {
      if (version === loadVersion.current) {
        setError(err?.message || "执行工作台读取失败");
      }
    } finally {
      if (version === loadVersion.current) setLoading(false);
    }
  }

  useEffect(() => { loadAll(); }, []);

  const projectNames = useMemo(
    () => Object.fromEntries(projects.map((item) => [item.project_id, item.name])),
    [projects]
  );
  const employeeNames = useMemo(
    () => Object.fromEntries(employees.map((item) => [item.id, item.name])),
    [employees]
  );
  const filtered = tasks.filter((task) => {
    const query = searchQuery.trim().toLowerCase();
    if (!query) return true;
    return [
      task.content,
      task.employee_name,
      employeeNames[task.employee_id],
      projectNames[task.project_id],
    ].some((value) => value?.toLowerCase().includes(query));
  });

  if (loading) {
    return (
      <TerraShell topCrumb="执行工作台">
        <TerraLoadingSkeleton variant="page" />
      </TerraShell>
    );
  }
  if (error) {
    return (
      <TerraShell topCrumb="执行工作台">
        <TerraErrorState message={error} onRetry={loadAll} />
      </TerraShell>
    );
  }

  return (
    <TerraShell
      topCrumb="执行工作台"
      topbarExtra={(
        <TerraSearch
          placeholder="搜索任务、项目或员工…"
          value={searchQuery}
          onChange={setSearchQuery}
        />
      )}
    >
      <TerraPageHead
        title="执行工作台"
        subtitle="聚合真实项目任务与执行状态"
        pill={{ text: "Task 执行", icon: "i-terminal" }}
        facts={[
          { value: tasks.length, label: "任务" },
          { value: tasks.filter((item) => item.status === "COMPLETED").length, label: "已完成" },
        ]}
      />

      {/* 主轴入口：本页是「一条需求直跑」的扁平清单；带依赖编排 + 验收返工的完整
          闭环在 /execution/pipeline。后端能力早已具备，此前前端没有入口。 */}
      <a href="/ceo-office/execution/pipeline" className="block no-underline mb-4">
        <TerraCard hover>
          <div className="flex items-center gap-3">
            <span className="w-[34px] h-[34px] rounded-ui-sm grid place-items-center flex-shrink-0 bg-ui-cyan-soft text-ui-cyan">
              <TerraIcon name="i-polyline" className="w-5 h-5" />
            </span>
            <div className="flex-1 min-w-0">
              <div className="font-semibold text-ui-3 text-ui-txt">任务流水线</div>
              <div className="text-ui-1 text-ui-txt-3 mt-0.5">
                一句话需求 → 自动拆成任务图 → 排队调度执行 → 验收通过或打回返工
              </div>
            </div>
            <TerraTag color="cyan">完整闭环</TerraTag>
          </div>
        </TerraCard>
      </a>

      <TerraCard>
        {filtered.length === 0 ? (
          <TerraEmpty icon="i-checklist">
            {tasks.length === 0 ? "暂无任务，请先进入项目工作台创建。" : "没有匹配的任务。"}
          </TerraEmpty>
        ) : (
          <div className="space-y-2">
            {filtered.map((task) => {
              const status = STATUS[task.status] || { label: task.status || "未记录", color: "grey" };
              return (
                <a
                  key={task.task_id}
                  href={`/ceo-office/execution/tasks/${task.task_id}`}
                  className="block no-underline"
                >
                  <div className="flex items-center gap-3 px-3 py-2.5 rounded-ui-md bg-ui-surface border border-ui-line hover:border-ui-primary-light transition-colors">
                    <span className={`w-2 h-2 rounded-full flex-shrink-0 ${
                      task.status === "COMPLETED"
                        ? "bg-ui-green"
                        : task.status === "FAILED"
                          ? "bg-ui-red"
                          : ["PENDING", "PARSED", "RUNNING", "RESUMED", "AWAITING_INPUT"].includes(task.status)
                            ? "bg-ui-amber"
                            : "bg-ui-line-2"
                    }`} />
                    <div className="flex-1 min-w-0">
                      <div className="font-semibold text-sm text-ui-txt truncate">{task.content}</div>
                      <div className="text-ui-1 text-ui-txt-3 mt-0.5">
                        {projectNames[task.project_id] || "未分配项目"} · {employeeNames[task.employee_id] || task.employee_name || "未分配"}
                      </div>
                    </div>
                    <TerraTag color={status.color}>{status.label}</TerraTag>
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
