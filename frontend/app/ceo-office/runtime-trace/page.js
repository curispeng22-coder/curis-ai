"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import TerraShell from "../../../components/terra/TerraShell.js";
import RuntimeCapabilitySwitcher from "../../../components/terra/RuntimeCapabilitySwitcher.js";
import {
  TerraCard,
  TerraEmpty,
  TerraPageHead,
  TerraTag,
} from "../../../components/terra/TerraPrimitives.js";
import {
  TerraErrorState,
  TerraLoadingSkeleton,
} from "../../../components/terra/TerraState.js";
import { getRuntimeTrace } from "../../../lib/api.js";

const TYPE_LABEL = {
  model_call: "模型调用",
  tool_call: "工具调用",
  workflow: "工作流",
  task: "任务",
};

/**
 * Frozen B1 · Secondary（次级文字入口），32px 命中高度。
 */
const SECONDARY_LINK =
  "inline-flex items-center h-[var(--ui-ctl-h-sm)] px-2 rounded-ui-sm text-ui-2 font-bold text-ui-accent no-underline transition-colors hover:bg-ui-surface-2";

/**
 * 运行时轨迹（Runtime Trace）只读视图。
 * 展示执行管道事件（能力调用 / token / 缓存命中 / 延迟），append-only，只读不编辑。
 */
export default function RuntimeTracePage() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const payload = await getRuntimeTrace({ limit: 100 });
      setEvents(payload?.events || []);
    } catch (err) {
      setError(err?.message || "运行轨迹读取失败");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  if (loading) {
    return (
      <TerraShell topCrumb="运行轨迹">
        <TerraLoadingSkeleton variant="page" />
      </TerraShell>
    );
  }
  if (error) {
    return (
      <TerraShell topCrumb="运行轨迹">
        <TerraErrorState message={error} onRetry={load} />
      </TerraShell>
    );
  }

  return (
    <TerraShell
      topCrumb="运行轨迹"
      topbarExtra={<RuntimeCapabilitySwitcher />}
    >
      <TerraPageHead
        title="运行轨迹"
        subtitle="执行管道事件（能力调用 / 用量 / 延迟），只读记录。"
        pill={{ text: `${events.length} 条事件`, icon: "i-list" }}
      />
      {events.length === 0 ? (
        <TerraEmpty icon="i-inbox">
          尚未产生运行事件
          <Link href="/ceo-office/execution" className={`${SECONDARY_LINK} mt-2`}>去执行工作台派发任务</Link>
        </TerraEmpty>
      ) : (
        // 轨迹行密度：紧凑卡（B2 紧凑内边距 16px）+ 8px 行距，
        // 正文 text-ui-3(14px)、次要 text-ui-2(13px)，对齐原型轨迹列表层级。
        <div className="flex flex-col gap-2 mt-5">
          {events.map((event) => (
            <TerraCard key={event.id}>
              <div className="flex flex-wrap items-center gap-2">
                <TerraTag color="grey">{TYPE_LABEL[event.event_type] || event.event_type}</TerraTag>
                <span className="text-ui-3 font-semibold text-ui-txt">
                  {event.capability || event.task_ref || event.run_id}
                </span>
                <span className="ml-auto text-ui-2 text-ui-txt-3">{event.created_at}</span>
              </div>
              <div className="flex flex-wrap gap-3 mt-2 text-ui-2 text-ui-txt-2">
                {event.tokens_in != null && <span>输入 {event.tokens_in}</span>}
                {event.tokens_out != null && <span>输出 {event.tokens_out}</span>}
                {event.cache_hit != null && (
                  <span className={event.cache_hit ? "text-ui-green font-semibold" : undefined}>
                    缓存 {event.cache_hit ? "命中" : "未中"}
                  </span>
                )}
                {event.latency_ms != null && <span>延迟 {event.latency_ms}ms</span>}
              </div>
            </TerraCard>
          ))}
        </div>
      )}
    </TerraShell>
  );
}
