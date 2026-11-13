"use client";

/**
 * 任务图（DAG）可视化 + 状态字典。
 *
 * 数据来自 GET /api/pipeline/{graph_id}/graph（后端 issue_pipeline_api._graph_to_public）：
 *   { graph_id, available, progress, is_complete, has_escalation, escalations, nodes[] }
 * 节点见 backend/app/task_graph.py TaskNode.to_dict()。
 *
 * 布局用「依赖层级分列」而不是力导向：节点数在个位到十位数，分层已经足够表达
 * 依赖关系，且零新依赖、SSR 安全。层级 = max(依赖层级)+1，环则回落到插入序。
 */

import { TerraIcon } from "./TerraIcons";
import { TerraTag, TerraEmpty } from "./TerraPrimitives";

/** 任务级状态（PipelineTask.status）。 */
export const PIPELINE_TASK_STATUS = {
  pending: { label: "待规划", color: "grey", dot: "bg-ui-line-2" },
  queued: { label: "排队中", color: "amber", dot: "bg-ui-amber" },
  running: { label: "执行中", color: "primary", dot: "bg-ui-primary" },
  review: { label: "待验收", color: "cyan", dot: "bg-ui-cyan" },
  approved: { label: "已通过", color: "green", dot: "bg-ui-green" },
  rejected: { label: "已驳回", color: "red", dot: "bg-ui-red" },
  failed: { label: "已失败", color: "red", dot: "bg-ui-red" },
};

/** 节点级状态（TaskNode.status）。 */
export const PIPELINE_NODE_STATUS = {
  pending: { label: "待触发", color: "grey" },
  ready: { label: "就绪", color: "amber" },
  running: { label: "执行中", color: "primary" },
  review: { label: "待验收", color: "cyan" },
  approved: { label: "已通过", color: "green" },
  done: { label: "已完成", color: "green" },
  failed: { label: "已失败", color: "red" },
  unknown: { label: "未知", color: "grey" },
};

export function taskStatusMeta(status) {
  return PIPELINE_TASK_STATUS[status] || { label: status || "未记录", color: "grey", dot: "bg-ui-line-2" };
}

export function nodeStatusMeta(status) {
  return PIPELINE_NODE_STATUS[status] || PIPELINE_NODE_STATUS.unknown;
}

/**
 * 计算每个节点的依赖层级。环或缺失依赖时该节点回落到 0 层，保证一定能画出来。
 * @param {Array} nodes
 * @returns {Array<Array>} 按层分组的节点二维数组
 */
export function layerNodes(nodes) {
  const byId = new Map(nodes.map((node) => [node.id, node]));
  const level = new Map();
  const visiting = new Set();

  function resolve(id) {
    if (level.has(id)) return level.get(id);
    if (visiting.has(id)) return 0; // 环：断在这里
    visiting.add(id);
    const node = byId.get(id);
    const deps = (node?.deps || []).filter((dep) => byId.has(dep));
    const value = deps.length === 0 ? 0 : Math.max(...deps.map(resolve)) + 1;
    visiting.delete(id);
    level.set(id, value);
    return value;
  }

  nodes.forEach((node) => resolve(node.id));
  const maxLevel = nodes.length ? Math.max(...nodes.map((node) => level.get(node.id) || 0)) : 0;
  const layers = Array.from({ length: maxLevel + 1 }, () => []);
  nodes.forEach((node) => layers[level.get(node.id) || 0].push(node));
  return layers;
}

function NodeCard({ node, onSelect, selected }) {
  const meta = nodeStatusMeta(node.status);
  const capType = node.cap_requirement?.cap_type;
  const clickable = typeof onSelect === "function";
  return (
    <div
      role={clickable ? "button" : undefined}
      tabIndex={clickable ? 0 : undefined}
      onClick={clickable ? () => onSelect(node) : undefined}
      onKeyDown={
        clickable
          ? (event) => {
              if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                onSelect(node);
              }
            }
          : undefined
      }
      className={`w-full text-left rounded-ui-md border bg-ui-surface px-3 py-2.5 transition-colors ${
        selected ? "border-ui-accent shadow-ui-2" : "border-ui-line"
      } ${clickable ? "cursor-pointer hover:border-ui-accent" : ""}`}
    >
      <div className="flex items-start gap-2">
        <span className="text-ui-1 font-mono text-ui-txt-3 mt-0.5 flex-shrink-0">{node.id}</span>
        <div className="flex-1 min-w-0">
          <div className="text-ui-2 font-semibold text-ui-txt leading-snug break-words">
            {node.goal || "（无目标描述）"}
          </div>
          <div className="text-ui-1 text-ui-txt-3 mt-1 flex flex-wrap items-center gap-x-2 gap-y-1">
            {capType && <span>能力：{capType}</span>}
            {node.deps?.length > 0 && <span>依赖：{node.deps.join(" · ")}</span>}
            {node.attempts > 0 && <span>尝试 {node.attempts} 次</span>}
            {node.rework_count > 0 && <span className="text-ui-amber">返工 {node.rework_count}</span>}
            {node.cap_switch_count > 0 && <span className="text-ui-violet">换能力 {node.cap_switch_count}</span>}
          </div>
        </div>
        <TerraTag color={meta.color}>{meta.label}</TerraTag>
      </div>
      {node.note && (
        <div className="text-ui-1 text-ui-red mt-1.5 break-words">{node.note}</div>
      )}
    </div>
  );
}

/**
 * DAG 主视图。
 * @param {object} props
 * @param {object} props.graph  /graph 端点返回体
 * @param {(node:object)=>void} [props.onSelectNode]
 * @param {string} [props.selectedNodeId]
 */
export default function PipelineGraphView({ graph, onSelectNode, selectedNodeId }) {
  const nodes = graph?.nodes || [];
  if (!graph) {
    return <TerraEmpty icon="i-polyline">尚未生成任务图。</TerraEmpty>;
  }
  if (!graph.available) {
    return (
      <TerraEmpty icon="i-polyline">
        任务图快照仅存于进程内存，后端重启后已丢失实时状态。
        {nodes.length > 0 && <span> 下方为提交时留存的计划快照（共 {nodes.length} 个节点）。</span>}
      </TerraEmpty>
    );
  }
  if (nodes.length === 0) {
    return <TerraEmpty icon="i-polyline">任务图为空。</TerraEmpty>;
  }

  const layers = layerNodes(nodes);
  const progress = graph.progress || {};
  const total = progress.total ?? nodes.length;
  const done = progress.done ?? nodes.filter((node) => node.status === "done").length;
  const percent =
    progress.percent != null ? progress.percent : total > 0 ? Math.round((done / total) * 100) : 0;

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-3">
        <div className="flex-1 h-1.5 rounded-ui-pill bg-ui-surface-3 overflow-hidden">
          <div
            className={`h-full rounded-ui-pill transition-all ${
              graph.has_escalation ? "bg-ui-red" : graph.is_complete ? "bg-ui-green" : "bg-ui-primary"
            }`}
            style={{ width: `${percent}%` }}
          />
        </div>
        <span className="text-ui-1 text-ui-txt-3 flex-shrink-0 tabular-nums">
          {done}/{total} 节点 · {percent}%
        </span>
      </div>

      {graph.has_escalation && (
        <div className="flex items-start gap-2 rounded-ui-sm border border-ui-red bg-ui-red-soft px-3 py-2 text-ui-1 text-ui-red">
          <TerraIcon name="i-warning" className="w-4 h-4 flex-shrink-0 mt-px" />
          <div>
            <div className="font-bold">已升级人工处理</div>
            {(graph.escalations || []).map((item, index) => (
              <div key={index} className="mt-0.5 break-words">
                {typeof item === "string" ? item : JSON.stringify(item)}
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="space-y-2">
        {layers.map((layer, index) => (
          <div key={index}>
            <div className="text-ui-1 text-ui-txt-3 mb-1.5 flex items-center gap-1.5">
              <span className="w-5 h-5 rounded-ui-pill bg-ui-surface-3 grid place-items-center font-bold tabular-nums">
                {index + 1}
              </span>
              第 {index + 1} 层 · {layer.length} 个节点
              {index > 0 && <span className="text-ui-txt-3">（依赖上一层完成）</span>}
            </div>
            <div className="grid gap-2 sm:grid-cols-2">
              {layer.map((node) => (
                <NodeCard
                  key={node.id}
                  node={node}
                  onSelect={onSelectNode}
                  selected={selectedNodeId === node.id}
                />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
