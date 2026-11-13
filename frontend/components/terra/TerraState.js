"use client";

import { TerraIcon } from "./TerraIcons.js";

/**
 * 数据态文案常量（handoff §6，全站统一）。
 * 所有页面必须使用这些常量，禁止硬编码占位文案。
 */
export const DATA_COPY = {
  noData: "未记录",
  unsynced: "尚未同步",
  noOwner: "未分配负责人",
  unassigned: "未分配",
  unknownCost: "未记录",       // 成本未知不得写 $0
  noRuntime: "未读取事实",      // 运行状态未读取
  sample: "示例快照 · 未接入真实数据",
};

/**
 * noRuntimeFact — 统一「运行事实未读取」文案入口（公司运行/Workflow/执行态）。
 * 与 DATA_COPY.noRuntime 同值，作为语义别名集中引用。
 * @type {string}
 */
export const noRuntimeFact = DATA_COPY.noRuntime;

/**
 * TerraSampleBadge — 示例数据标识（统一 amber 胶囊）。
 * 凡展示示例/快照数据，必须挂载此组件，避免被误读为真实运行事实。
 */
export function TerraSampleBadge({ className = "" }) {
  return (
    <span className={`inline-flex items-center gap-1.5 bg-ui-accent-light text-ui-accent rounded-full px-3 py-1 text-xs font-semibold ${className}`}>
      <TerraIcon name="i-info" className="w-3.5 h-3.5 flex-shrink-0" />
      {DATA_COPY.sample}
    </span>
  );
}

/**
 * TerraEmptyState — 空态通用组件。
 *
 * @param {Object} props
 * @param {string} props.icon - TerraIcon name
 * @param {string} props.title - 空态标题
 * @param {string} [props.description] - 空态描述/原因
 * @param {React.ReactNode} [props.action] - 主操作按钮
 */
export function TerraEmptyState({ icon, title, description, action }) {
  return (
    <div className="py-12 px-6 text-center">
      {icon && (
        <div className="mb-3 inline-flex items-center justify-center w-14 h-14 rounded-full bg-ui-surface-2">
          <TerraIcon name={icon} className="w-7 h-7 text-ui-txt-3" />
        </div>
      )}
      <h3 className="font-ui-sans font-semibold text-lg text-ui-txt mb-1.5">{title}</h3>
      {description && (
        <p className="text-sm text-ui-txt-3 max-w-md mx-auto mb-4 leading-relaxed">{description}</p>
      )}
      {action && <div className="mt-2">{action}</div>}
    </div>
  );
}

/**
 * TerraErrorState — 错误态通用组件。
 *
 * @param {Object} props
 * @param {string} props.title - 错误标题
 * @param {string} [props.message] - 可读错误原因
 * @param {Function} props.onRetry - 重试回调
 */
export function TerraErrorState({ title = "加载失败", message, onRetry }) {
  return (
    <div className="py-12 px-6 text-center">
      <div className="mb-3 inline-flex items-center justify-center w-14 h-14 rounded-full bg-ui-red-soft">
        <TerraIcon name="i-error" className="w-7 h-7 text-ui-red" />
      </div>
      <h3 className="font-ui-sans font-semibold text-lg text-ui-txt mb-1.5">{title}</h3>
      {message && (
        <p className="text-sm text-ui-txt-3 max-w-md mx-auto mb-4 leading-relaxed">{message}</p>
      )}
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="mt-2 inline-flex items-center gap-1.5 px-4 py-2.5 rounded-ui-sm bg-ui-primary text-ui-primary-fg text-xs font-bold hover:bg-ui-primary-dark transition-colors"
        >
          <TerraIcon name="i-refresh" className="w-4 h-4" /> {/* fallback if not in icons */}
          重新读取
        </button>
      )}
    </div>
  );
}

/**
 * TerraLoadingSkeleton — Loading 骨架屏。
 *
 * @param {Object} props
 * @param {"page"|"card"|"list"} [props.variant="page"] - 骨架类型
 */
export function TerraLoadingSkeleton({ variant = "page" }) {
  if (variant === "card") {
    return (
      <div className="bg-ui-surface border border-ui-line rounded-ui-lg p-4 animate-pulse">
        <div className="h-4 bg-ui-surface-2 rounded w-32 mb-3" />
        <div className="h-3 bg-ui-surface-2 rounded w-full mb-2" />
        <div className="h-3 bg-ui-surface-2 rounded w-3/4" />
      </div>
    );
  }

  if (variant === "list") {
    return (
      <div className="space-y-3 animate-pulse">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="bg-ui-surface border border-ui-line rounded-ui-md p-3">
            <div className="h-4 bg-ui-surface-2 rounded w-40 mb-2" />
            <div className="h-3 bg-ui-surface-2 rounded w-full" />
          </div>
        ))}
      </div>
    );
  }

  // page variant — full page skeleton
  return (
    <div className="animate-pulse space-y-4">
      <div className="h-8 bg-ui-surface-2 rounded w-48" />
      <div className="h-3 bg-ui-surface-2 rounded w-64" />
      <div className="grid grid-cols-3 gap-3.5 mt-4">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="bg-ui-surface border border-ui-line rounded-ui-lg p-4 h-28" />
        ))}
      </div>
    </div>
  );
}
