"use client";

/**
 * 流水线任务详情：任务图 + 调度 + 验收/返工闭环。
 *
 * 这是主轴后半段「执行 → 验收 → 返工 → 完成」的落点。三个终局动作：
 * - 通过（approve）：review → approved，闭环结束。
 * - 打回返工（rework）：review → pending，rework_count+1，上限 2 次，可再跑。
 * - 驳回（reject）：review → rejected，终态，不再跑。
 *
 * 任务图存在进程内存（后端 _graph_registry），后端重启会丢实时状态，此时
 * /graph 返回 404，页面降级为只显示任务本身，不假装图还在。
 */

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useParams } from "next/navigation";
import TerraShell from "../../../../../components/terra/TerraShell.js";
import {
  TerraBackLink,
  TerraButton,
  TerraCard,
  TerraCardHeader,
  TerraEmpty,
  TerraPageHead,
  TerraTag,
} from "../../../../../components/terra/TerraPrimitives.js";
import { TerraErrorState, TerraLoadingSkeleton } from "../../../../../components/terra/TerraState.js";
import { TerraIcon } from "../../../../../components/terra/TerraIcons.js";
import PipelineGraphView, {
  nodeStatusMeta,
  taskStatusMeta,
} from "../../../../../components/terra/PipelineGraphView.js";
import {
  approvePipelineTask,
  autoRunPipelineGraph,
  dispatchPipelineTask,
  getPipelineGraph,
  getPipelineTask,
  getPipelineTrace,
  pickGraphId,
  rejectPipelineTask,
  reworkPipelineTask,
} from "../../../../../lib/api.js";

const POLL_INTERVAL_MS = 2000;
const LIVE_STATUSES = ["queued", "running"];
const MAX_REWORK = 2;

function Row({ label, children }) {
  return (
    <div className="flex gap-3 py-1.5 border-b border-ui-line last:border-b-0">
      <span className="text-ui-1 text-ui-txt-3 w-24 flex-shrink-0">{label}</span>
      <span className="text-ui-2 text-ui-txt flex-1 min-w-0 break-words">{children ?? "—"}</span>
    </div>
  );
}

export default function PipelineTaskDetailPage() {
  const params = useParams();
  const taskId = String(params?.taskId || "");

  const [task, setTask] = useState(null);
  const [graph, setGraph] = useState(null);
  const [trace, setTrace] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [actionError, setActionError] = useState("");
  const [actionBusy, setActionBusy] = useState("");
  const [note, setNote] = useState("");
  const [selectedNodeId, setSelectedNodeId] = useState("");

  const loadVersion = useRef(0);

  const load = useCallback(
    async ({ silent = false } = {}) => {
      if (!taskId) return;
      const version = ++loadVersion.current;
      if (!silent) setLoading(true);
      try {
        const taskPayload = await getPipelineTask(taskId);
        if (version !== loadVersion.current) return;
        setTask(taskPayload);
        setError("");

        const graphId = pickGraphId(taskPayload);
        if (graphId) {
          // 图存进程内存，后端重启后 404 属正常降级，不当成页面错误。
          const [graphPayload, tracePayload] = await Promise.all([
            getPipelineGraph(graphId).catch(() => null),
            getPipelineTrace(graphId).catch(() => null),
          ]);
          if (version !== loadVersion.current) return;
          setGraph(graphPayload);
          setTrace(tracePayload);
        } else {
          setGraph(null);
          setTrace(null);
        }
      } catch (err) {
        if (version === loadVersion.current && !silent) {
          setError(err?.message || "任务读取失败");
        }
      } finally {
        if (version === loadVersion.current && !silent) setLoading(false);
      }
    },
    [taskId]
  );

  useEffect(() => {
    load();
  }, [load]);

  const isLive = task ? LIVE_STATUSES.includes(task.status) : false;
  useEffect(() => {
    if (!isLive) return undefined;
    const timer = setInterval(() => load({ silent: true }), POLL_INTERVAL_MS);
    return () => clearInterval(timer);
  }, [isLive, load]);

  const graphId = task ? pickGraphId(task) : null;
  const meta = taskStatusMeta(task?.status);
  const reworkCount = task?.rework_count || 0;
  const canRework = task?.status === "review" && reworkCount < MAX_REWORK;
  const canReview = task?.status === "review";
  const canRun = ["pending", "queued", "failed"].includes(task?.status);

  const selectedNode = useMemo(
    () => (graph?.nodes || []).find((node) => node.id === selectedNodeId) || null,
    [graph, selectedNodeId]
  );

  async function runAction(key, fn, { requireNote = false } = {}) {
    if (actionBusy) return;
    if (requireNote && !note.trim()) {
      setActionError("请先写清楚哪里不合格，返工/驳回都会把这段话带给执行方。");
      return;
    }
    setActionBusy(key);
    setActionError("");
    try {
      await fn();
      setNote("");
      await load({ silent: true });
    } catch (err) {
      setActionError(err?.message || "操作失败");
    } finally {
      setActionBusy("");
    }
  }

  if (loading) {
    return (
      <TerraShell topCrumb="任务流水线 / 详情">
        <TerraLoadingSkeleton variant="page" />
      </TerraShell>
    );
  }
  if (error || !task) {
    return (
      <TerraShell topCrumb="任务流水线 / 详情">
        <TerraBackLink href="/ceo-office/execution/pipeline">返回任务流水线</TerraBackLink>
        <TerraErrorState message={error || "任务不存在"} onRetry={load} />
      </TerraShell>
    );
  }

  const result = task.executor_result || null;

  return (
    <TerraShell topCrumb="任务流水线 / 详情">
      <TerraBackLink href="/ceo-office/execution/pipeline">返回任务流水线</TerraBackLink>

      <TerraPageHead
        title={task.issue_spec?.title || task.natural_language || task.id}
        subtitle={`任务 ${task.id}${graphId ? ` · 任务图 ${graphId}` : ""}`}
        pill={{ text: meta.label, icon: "i-polyline" }}
        facts={[
          { value: graph?.progress?.total ?? "—", label: "节点" },
          { value: graph?.progress?.done ?? "—", label: "已完成" },
          { value: `${reworkCount}/${MAX_REWORK}`, label: "返工" },
        ]}
      />

      {/* ── 操作条 ── */}
      <TerraCard className="mb-4">
        <div className="flex flex-wrap items-center gap-2">
          <TerraTag color={meta.color}>{meta.label}</TerraTag>
          {isLive && (
            <span className="text-ui-1 text-ui-txt-3 inline-flex items-center gap-1">
              <TerraIcon name="i-refresh" className="w-3.5 h-3.5" />
              每 2 秒自动刷新
            </span>
          )}
          <div className="flex-1" />

          {canRun && graphId && (
            <TerraButton
              icon="i-bolt"
              disabled={Boolean(actionBusy)}
              onClick={() => runAction("auto", () => autoRunPipelineGraph(graphId))}
            >
              {actionBusy === "auto" ? "启动中…" : "自动调度执行"}
            </TerraButton>
          )}
          {canRun && (
            <TerraButton
              variant="ghost"
              icon="i-terminal"
              disabled={Boolean(actionBusy)}
              onClick={() => runAction("dispatch", () => dispatchPipelineTask(task.id))}
            >
              {actionBusy === "dispatch" ? "派发中…" : "单次派发"}
            </TerraButton>
          )}
          {canReview && (
            <>
              <TerraButton
                icon="i-verified"
                disabled={Boolean(actionBusy)}
                onClick={() => runAction("approve", () => approvePipelineTask(task.id))}
              >
                {actionBusy === "approve" ? "提交中…" : "验收通过"}
              </TerraButton>
              <TerraButton
                variant="ghost"
                icon="i-refresh"
                disabled={Boolean(actionBusy) || !canRework}
                title={canRework ? "" : `返工已达上限 ${MAX_REWORK} 次`}
                onClick={() =>
                  runAction("rework", () => reworkPipelineTask(task.id, note.trim() || "手动触发返工"), {
                    requireNote: true,
                  })
                }
              >
                {actionBusy === "rework" ? "打回中…" : `打回返工${canRework ? "" : "（已达上限）"}`}
              </TerraButton>
              <TerraButton
                variant="danger"
                icon="i-block"
                disabled={Boolean(actionBusy)}
                onClick={() =>
                  runAction("reject", () => rejectPipelineTask(task.id, note.trim()), {
                    requireNote: true,
                  })
                }
              >
                {actionBusy === "reject" ? "驳回中…" : "驳回"}
              </TerraButton>
            </>
          )}
        </div>

        {canReview && (
          <div className="mt-3">
            <label
              htmlFor="pipeline-note"
              className="block text-ui-1 font-bold text-ui-txt-2 mb-1.5 tracking-wide"
            >
              验收意见（打回返工 / 驳回时必填）
            </label>
            <textarea
              id="pipeline-note"
              rows={2}
              value={note}
              onChange={(event) => setNote(event.target.value)}
              placeholder="例如：表单校验没做，邮箱格式非法也能提交；另外提交后没有成功提示。"
              className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-ui-3 text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-accent resize-y"
            />
          </div>
        )}

        {actionError && (
          <div className="mt-3 flex items-start gap-2 rounded-ui-sm border border-ui-red bg-ui-red-soft px-3 py-2 text-ui-1 text-ui-red">
            <TerraIcon name="i-error" className="w-4 h-4 flex-shrink-0 mt-px" />
            <span>{actionError}</span>
          </div>
        )}

        {task.status === "approved" && (
          <div className="mt-3 flex items-center gap-2 rounded-ui-sm border border-ui-green bg-ui-green-soft px-3 py-2 text-ui-1 text-ui-green">
            <TerraIcon name="i-verified" className="w-4 h-4" />
            已验收通过，闭环结束。
          </div>
        )}
        {task.status === "rejected" && (
          <div className="mt-3 rounded-ui-sm border border-ui-red bg-ui-red-soft px-3 py-2 text-ui-1 text-ui-red">
            <div className="font-bold">已驳回（终态）</div>
            {task.review_note && <div className="mt-0.5">{task.review_note}</div>}
          </div>
        )}
        {task.status === "failed" && (
          <div className="mt-3 rounded-ui-sm border border-ui-red bg-ui-red-soft px-3 py-2 text-ui-1 text-ui-red">
            <div className="font-bold">执行失败并已升级</div>
            <div className="mt-0.5">可修正需求后重新触发自动调度，或直接驳回。</div>
          </div>
        )}
      </TerraCard>

      <div className="grid gap-4 lg:grid-cols-[minmax(0,1.6fr)_minmax(0,1fr)]">
        <div className="space-y-4">
          <TerraCard>
            <TerraCardHeader icon="i-polyline" iconClass="cyan" title="任务图" />
            <PipelineGraphView
              graph={graph}
              onSelectNode={(node) => setSelectedNodeId(node.id === selectedNodeId ? "" : node.id)}
              selectedNodeId={selectedNodeId}
            />
          </TerraCard>

          {selectedNode && (
            <TerraCard>
              <TerraCardHeader icon="i-info" iconClass="primary" title={`节点 ${selectedNode.id}`} />
              <div className="space-y-0">
                <Row label="目标">{selectedNode.goal}</Row>
                <Row label="状态">
                  <TerraTag color={nodeStatusMeta(selectedNode.status).color}>
                    {nodeStatusMeta(selectedNode.status).label}
                  </TerraTag>
                </Row>
                <Row label="依赖">{selectedNode.deps?.length ? selectedNode.deps.join(" · ") : "无"}</Row>
                <Row label="触发">
                  {selectedNode.trigger?.mode || "condition"}
                  {selectedNode.trigger?.at ? ` @ ${selectedNode.trigger.at}` : ""}
                  {selectedNode.trigger?.on_event ? ` on ${selectedNode.trigger.on_event}` : ""}
                </Row>
                <Row label="能力需求">{selectedNode.cap_requirement?.cap_type || "—"}</Row>
                <Row label="能力链">
                  {selectedNode.capability_path?.length
                    ? selectedNode.capability_path.join(" → ")
                    : "尚未执行"}
                </Row>
                <Row label="尝试">{`${selectedNode.attempts || 0} 次 · 返工 ${selectedNode.rework_count || 0} · 换能力 ${selectedNode.cap_switch_count || 0}`}</Row>
              </div>
              {selectedNode.result && (
                <pre className="mt-3 max-h-64 overflow-auto rounded-ui-sm bg-ui-surface-2 border border-ui-line p-3 text-ui-1 text-ui-txt-2 whitespace-pre-wrap break-words">
                  {typeof selectedNode.result === "string"
                    ? selectedNode.result
                    : JSON.stringify(selectedNode.result, null, 2)}
                </pre>
              )}
            </TerraCard>
          )}

          <TerraCard>
            <TerraCardHeader icon="i-description" iconClass="surface" title="执行产出" />
            {!result ? (
              <TerraEmpty icon="i-description">尚无产出，任务跑完后在这里看结果。</TerraEmpty>
            ) : (
              <div className="space-y-3">
                <div className="flex flex-wrap gap-2">
                  <TerraTag color={result.status === "success" ? "green" : "red"}>
                    {result.status === "success" ? "执行成功" : "执行失败"}
                  </TerraTag>
                  {result.rounds != null && <TerraTag color="grey">共 {result.rounds} 轮</TerraTag>}
                  {result.files?.length > 0 && (
                    <TerraTag color="cyan">{result.files.length} 个文件</TerraTag>
                  )}
                </div>
                {result.files?.length > 0 && (
                  <ul className="text-ui-1 text-ui-txt-2 font-mono space-y-0.5">
                    {result.files.map((file) => (
                      <li key={file} className="break-all">
                        {file}
                      </li>
                    ))}
                  </ul>
                )}
                {result.artifact_text && (
                  <pre className="max-h-80 overflow-auto rounded-ui-sm bg-ui-surface-2 border border-ui-line p-3 text-ui-1 text-ui-txt-2 whitespace-pre-wrap break-words">
                    {result.artifact_text}
                  </pre>
                )}
                {result.diff_text && (
                  <pre className="max-h-80 overflow-auto rounded-ui-sm bg-ui-surface-2 border border-ui-line p-3 text-ui-1 text-ui-txt-2 whitespace-pre">
                    {result.diff_text}
                  </pre>
                )}
              </div>
            )}
          </TerraCard>
        </div>

        <div className="space-y-4">
          <TerraCard>
            <TerraCardHeader icon="i-checklist" iconClass="surface" title="任务信息" />
            <div className="space-y-0">
              <Row label="原始需求">{task.natural_language}</Row>
              <Row label="状态">
                <TerraTag color={meta.color}>{meta.label}</TerraTag>
              </Row>
              <Row label="创建">{task.created_at}</Row>
              <Row label="入队">{task.queued_at}</Row>
              <Row label="开始">{task.started_at}</Row>
              <Row label="完成">{task.completed_at}</Row>
              <Row label="验收结论">{task.review_decision}</Row>
              <Row label="验收备注">{task.review_note}</Row>
            </div>
          </TerraCard>

          {reworkCount > 0 && (
            <TerraCard>
              <TerraCardHeader icon="i-refresh" iconClass="amber" title={`返工记录 ${reworkCount}/${MAX_REWORK}`} />
              {task.rework_feedback ? (
                <div className="text-ui-2 text-ui-txt whitespace-pre-wrap break-words">
                  {typeof task.rework_feedback === "string"
                    ? task.rework_feedback
                    : JSON.stringify(task.rework_feedback, null, 2)}
                </div>
              ) : (
                <TerraEmpty icon="i-refresh">无返工说明。</TerraEmpty>
              )}
            </TerraCard>
          )}

          {task.issue_spec && (
            <TerraCard>
              <TerraCardHeader icon="i-dataset" iconClass="violet" title="结构化 Issue" />
              <pre className="max-h-72 overflow-auto rounded-ui-sm bg-ui-surface-2 border border-ui-line p-3 text-ui-1 text-ui-txt-2 whitespace-pre-wrap break-words">
                {JSON.stringify(task.issue_spec, null, 2)}
              </pre>
            </TerraCard>
          )}

          <TerraCard>
            <TerraCardHeader icon="i-monitoring" iconClass="surface" title="执行轨迹" />
            {!trace?.trace?.length ? (
              <TerraEmpty icon="i-monitoring">暂无轨迹事件。</TerraEmpty>
            ) : (
              <ol className="space-y-2">
                {trace.trace.map((event, index) => (
                  <li key={index} className="flex gap-2">
                    <span className="w-1.5 h-1.5 rounded-ui-pill bg-ui-line-2 mt-1.5 flex-shrink-0" />
                    <div className="min-w-0 flex-1">
                      <div className="text-ui-1 text-ui-txt break-words">
                        {event.event || event.type || "event"}
                        {event.node_id ? ` · ${event.node_id}` : ""}
                      </div>
                      <div className="text-ui-1 text-ui-txt-3 break-words">
                        {[event.capability, event.reason, event.detail, event.message]
                          .filter(Boolean)
                          .join(" · ") || JSON.stringify(event)}
                      </div>
                    </div>
                  </li>
                ))}
              </ol>
            )}
          </TerraCard>
        </div>
      </div>
    </TerraShell>
  );
}
