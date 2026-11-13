"use client";

/*
 * RuntimeCapabilitySwitcher — 运行现场顶栏「当前能力」切换器
 * ---------------------------------------------------------------------------
 * 规范来源：Curis UI Frozen Spec §3.7
 *   放在 TerraShell 的 topbarExtra 槽位，只在「运行现场」类页面出现
 *   （项目工作台 / 执行运行 / 任务执行 / 公司运行 / 运行追踪）。
 *
 * 四态齐全，任何一态都不留死控件：
 *   loading → 占位下拉（disabled，宽度稳定，不抖版）
 *   error   → 文案 + 重试按钮（不阻断页面主流程）
 *   empty   → 虚线 CTA 直达能力中心，操作路径不断头
 *   ready   → 按类型分组的原生 select
 *
 * 无障碍：
 *   - 原生 <select> 自带键盘操作与语义，不自造下拉
 *   - <label> 显式关联，窄屏时标签仅视觉隐藏（sr-only），语义仍在
 *   - 切换结果经 aria-live="polite" 播报
 *   - 控件高度取 --ui-ctl-h-sm（32px），满足触达下限
 *   - 焦点样式由 globals.css 的全局 :focus-visible 规则统一提供
 *
 * 安全：React 默认转义文本节点，能力名称不参与 HTML 解析，结构上无 XSS 面。
 */

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import {
  useCapabilityOptions,
  useRuntimeCapability,
} from "../../lib/runtimeCapability.js";

const CAPABILITY_CENTER = "/ceo-office/capabilities";

const SELECT_CLASS =
  "h-[var(--ui-ctl-h-sm)] max-w-[220px] rounded-ui-sm border border-ui-line " +
  "bg-ui-surface-2 px-2 text-ui-2 text-ui-txt " +
  "hover:border-ui-primary disabled:opacity-60 disabled:cursor-not-allowed " +
  "transition-colors";

export default function RuntimeCapabilitySwitcher({ className = "" }) {
  const { capabilityKey, setCapabilityKey } = useRuntimeCapability();
  const { capabilities, groups, loading, error, reload } = useCapabilityOptions();
  const [announcement, setAnnouncement] = useState("");
  const mounted = useRef(false);

  // 记住的能力若已被停用 / 删除，静默回落到「未选择」，避免提交幽灵 key。
  useEffect(() => {
    if (loading || !capabilityKey) return;
    const stillValid = capabilities.some((item) => item.capability_key === capabilityKey);
    if (!stillValid) setCapabilityKey("");
  }, [loading, capabilityKey, capabilities, setCapabilityKey]);

  // 首帧不播报，只在用户真正切换后播报。
  useEffect(() => {
    if (!mounted.current) {
      mounted.current = true;
      return;
    }
    const current = capabilities.find((item) => item.capability_key === capabilityKey);
    setAnnouncement(
      current ? `当前能力已切换为 ${current.name || current.capability_key}` : "当前能力已清空"
    );
  }, [capabilityKey, capabilities]);

  const wrapClass = `inline-flex items-center gap-2 ${className}`;

  if (loading) {
    return (
      <div className={wrapClass}>
        <span className="hidden text-ui-1 text-ui-txt-3 sm:inline">当前能力</span>
        <span
          className={`${SELECT_CLASS} inline-flex items-center text-ui-txt-3`}
          aria-busy="true"
        >
          载入中…
        </span>
      </div>
    );
  }

  if (error) {
    return (
      <div className={wrapClass}>
        <span className="text-ui-1 text-ui-red">能力目录读取失败</span>
        <button
          type="button"
          onClick={reload}
          className="h-[var(--ui-ctl-h-sm)] rounded-ui-sm border border-ui-line px-2 text-ui-1 text-ui-txt-2 hover:border-ui-primary hover:text-ui-primary transition-colors"
        >
          重试
        </button>
      </div>
    );
  }

  if (!capabilities.length) {
    return (
      <div className={wrapClass}>
        <span className="hidden text-ui-1 text-ui-txt-3 sm:inline">当前能力</span>
        <Link
          href={CAPABILITY_CENTER}
          title="前往能力中心注册模型 / AI 员工 / 技能 / 工具 / 连接器"
          className="inline-flex h-[var(--ui-ctl-h-sm)] items-center rounded-ui-sm border border-dashed border-ui-line px-2 text-ui-1 text-ui-txt-2 hover:border-ui-primary hover:text-ui-primary transition-colors"
        >
          ＋ 配置能力
        </Link>
      </div>
    );
  }

  return (
    <div className={wrapClass}>
      <label htmlFor="runtimeCapSelect" className="text-ui-1 text-ui-txt-3 max-sm:sr-only">
        当前能力
      </label>
      <select
        id="runtimeCapSelect"
        className={SELECT_CLASS}
        value={capabilityKey}
        onChange={(event) => setCapabilityKey(event.target.value)}
      >
        <option value="">未选择</option>
        {groups.map((group) => (
          <optgroup key={group.type} label={group.label}>
            {group.items.map((item) => (
              <option key={item.capability_key} value={item.capability_key}>
                {item.name || item.capability_key}
              </option>
            ))}
          </optgroup>
        ))}
      </select>
      <span aria-live="polite" className="sr-only">
        {announcement}
      </span>
    </div>
  );
}
