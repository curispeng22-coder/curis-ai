"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import TerraShell from "../../../../../components/terra/TerraShell.js";
import RuntimeCapabilitySwitcher from "../../../../../components/terra/RuntimeCapabilitySwitcher.js";
import {
  TerraBackLink,
  TerraCard,
  TerraCardHeader,
  TerraPageHead,
  TerraTag,
} from "../../../../../components/terra/TerraPrimitives.js";
import { TerraErrorState, TerraLoadingSkeleton } from "../../../../../components/terra/TerraState.js";
import { getWorkflowRun } from "../../../../../lib/development.js";

const RUN_STATUS = {
  completed: { label: "已完成", color: "green" },
  failed: { label: "失败", color: "red" },
  running: { label: "执行中", color: "amber" },
};

function parseOutput(value) {
  try {
    const parsed = JSON.parse(value || "");
    return parsed && typeof parsed === "object" ? parsed : null;
  } catch (_error) {
    return null;
  }
}

function formatTime(value) {
  if (!value) return "未记录";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString("zh-CN");
}

function duration(startedAt, completedAt) {
  if (!startedAt || !completedAt) return "未记录";
  const seconds = Math.max(0, Math.round((new Date(completedAt) - new Date(startedAt)) / 1000));
  return Number.isFinite(seconds) ? `${seconds} 秒` : "未记录";
}

export default function ExecutionRunPage() {
  const params = useParams();
  const id = params?.id || "";
  const [run, setRun] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    if (!id) return;
    setLoading(true);
    setError("");
    try {
      setRun(await getWorkflowRun(id));
    } catch (err) {
      setError(err?.message || "研发运行读取失败");
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => { load(); }, [load]);

  const developmentResult = useMemo(() => {
    for (const step of run?.steps || []) {
      const parsed = parseOutput(step.output);
      if (parsed?.mode === "real_rd") return parsed;
    }
    return null;
  }, [run?.steps]);

  if (loading) {
    return (
      <TerraShell topCrumb="执行工作台 / 研发运行">
        <TerraLoadingSkeleton variant="page" />
      </TerraShell>
    );
  }
  if (error || !run) {
    return (
      <TerraShell topCrumb="执行工作台 / 研发运行">
        <TerraErrorState message={error || "运行不存在"} onRetry={load} />
      </TerraShell>
    );
  }

  const status = RUN_STATUS[run.status] || { label: run.status || "未记录", color: "grey" };
  return (
    <TerraShell
      topCrumb="执行工作台 / 研发运行 / 运行详情"
      topbarExtra={<RuntimeCapabilitySwitcher />}
    >
      <TerraBackLink href={run.project_id ? `/ceo-office/projects/${run.project_id}` : "/ceo-office/execution"}>
        返回项目工作台
      </TerraBackLink>
      <TerraPageHead
        title="研发工作流运行"
        subtitle={`运行 ID：${run.workflow_run_id} · 模板：${run.workflow_template_id || "未记录"}`}
        pill={{ text: status.label, icon: "i-account_tree" }}
        facts={[
          { value: run.project_id || "未记录", label: "项目" },
          { value: formatTime(run.started_at), label: "开始时间" },
          { value: duration(run.started_at, run.completed_at), label: "耗时" },
        ]}
      />

      <div className="grid grid-cols-12 gap-3.5">
        <TerraCard className="col-span-12 lg:col-span-8">
          <TerraCardHeader icon="i-terminal" iconClass="cyan" title="真实运行步骤" />
          <div className="space-y-2 mt-1">
            {(run.steps || []).map((step) => {
              const parsed = parseOutput(step.output);
              const stepStatus = step.status === "completed"
                ? { label: "已完成", color: "green" }
                : step.status === "failed"
                  ? { label: "失败", color: "red" }
                  : { label: step.status || "未记录", color: "amber" };
              return (
                <div
                  key={step.workflow_step_id}
                  className="flex items-start gap-3 px-3 py-2.5 rounded-ui-md bg-ui-surface border border-ui-line"
                >
                  <span className={`w-2 h-2 rounded-full mt-1.5 flex-shrink-0 ${
                    step.status === "completed" ? "bg-ui-green" : step.status === "failed" ? "bg-ui-red" : "bg-ui-amber"
                  }`} />
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-semibold text-ui-txt">
                      {step.step_order}. {step.step_name}
                    </div>
                    <p className="text-ui-1 text-ui-txt-3 mt-0.5 break-words">
                      {parsed?.fact || (parsed?.mode === "real_rd"
                        ? `代码执行 ${parsed.status} · 测试退出码 ${parsed.test_exit_code ?? "未记录"}`
                        : step.error || step.output || "未记录")}
                    </p>
                  </div>
                  <TerraTag color={stepStatus.color} size="sm">{stepStatus.label}</TerraTag>
                </div>
              );
            })}
          </div>
        </TerraCard>

        <TerraCard className="col-span-12 lg:col-span-4">
          <TerraCardHeader icon="i-info" iconClass="primary" title="运行事实" />
          <dl className="space-y-2 mt-1">
            {[
              { label: "运行状态", value: status.label },
              { label: "Task", value: run.task_id || "未记录" },
              { label: "执行模型", value: developmentResult?.model_name || "未记录" },
              { label: "Token", value: developmentResult?.total_tokens ?? "未记录" },
              {
                label: "成本",
                value: developmentResult?.estimated_cost == null
                  ? "未记录"
                  : `$${Number(developmentResult.estimated_cost).toFixed(6)} USD`,
              },
              { label: "修复轮次", value: developmentResult?.rounds ?? "未记录" },
            ].map((row) => (
              <div key={row.label} className="flex justify-between gap-3 bg-ui-surface-2 rounded-ui-sm px-3 py-2">
                <dt className="text-xs text-ui-txt-3 flex-shrink-0">{row.label}</dt>
                <dd className="text-xs text-ui-txt font-medium text-right break-all">{row.value}</dd>
              </div>
            ))}
          </dl>
        </TerraCard>

        <TerraCard className="col-span-12">
          <TerraCardHeader icon="i-difference" iconClass="green" title="代码成果与 Git 差异" />
          {developmentResult ? (
            <div className="space-y-3">
              <dl className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                <div className="bg-ui-surface-2 rounded-ui-sm px-3 py-2">
                  <dt className="text-ui-1 text-ui-txt-3">变更文件</dt>
                  <dd className="text-sm text-ui-txt font-semibold mt-0.5">
                    {developmentResult.files?.length ?? 0}
                  </dd>
                </div>
                <div className="bg-ui-surface-2 rounded-ui-sm px-3 py-2">
                  <dt className="text-ui-1 text-ui-txt-3">测试退出码</dt>
                  <dd className="text-sm text-ui-txt font-semibold mt-0.5">
                    {developmentResult.test_exit_code ?? "未记录"}
                  </dd>
                </div>
                <div className="bg-ui-surface-2 rounded-ui-sm px-3 py-2">
                  <dt className="text-ui-1 text-ui-txt-3">Diff SHA-256</dt>
                  <dd className="text-xs text-ui-txt font-mono mt-0.5 break-all">
                    {developmentResult.diff_sha256 || "未记录"}
                  </dd>
                </div>
              </dl>
              <div>
                <div className="text-ui-1 font-bold text-ui-txt-2 mb-1.5">变更路径</div>
                <div className="flex flex-wrap gap-1.5">
                  {(developmentResult.files || []).map((file) => (
                    <TerraTag key={file.path} color="cyan">{file.path}</TerraTag>
                  ))}
                </div>
              </div>
              <pre className="max-h-[32rem] overflow-auto rounded-ui-sm bg-ui-surface-2 p-4 text-xs leading-relaxed text-ui-txt whitespace-pre">
                {developmentResult.diff_text || "未记录"}
              </pre>
              <p className="text-ui-1 text-ui-txt-3">
                本页展示同次运行生成的真实 Git diff；远程提交、分支与 PR 未执行。
              </p>
            </div>
          ) : (
            <p className="text-sm text-ui-txt-3">
              本次运行没有成功代码成果。失败原因：{run.final_report || "未记录"}
            </p>
          )}
        </TerraCard>
      </div>
    </TerraShell>
  );
}
