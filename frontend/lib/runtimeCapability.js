"use client";

/*
 * Runtime Capability — 运行现场「当前能力」的数据契约层（全站唯一实现）
 * ---------------------------------------------------------------------------
 * 规范来源：Curis UI Frozen Spec §3.7「运行时能力切换器」
 *   能力闭环三段：能力中心「注册 + 绑定」→ 运行现场「切换」→ 执行时生效。
 *   本模块只负责第三段「切换」的状态管理；能力目录真源在后端
 *   GET /api/workspace/capabilities/registry，不在前端造数据。
 *
 * 与原型（curis-ui-prototype/_system/runtime-capability.js）的差异：
 *   原型用 localStorage['curis-capabilities'] 承载 mock 目录；真实前端改读后端
 *   registry。**唯一保留在 localStorage 的是「本页最近一次选择」**，因为它是
 *   纯客户端的操作偏好，不属于业务数据，也不该占用后端写接口。
 *
 * 存储契约：
 *   localStorage['curis-runtime-cap:<pathname>'] → capability_key（字符串）
 *   按 pathname 分桶，保证「项目 A 的运行现场」与「任务 B 的执行页」互不干扰。
 *
 * 同步契约：
 *   同标签页 → window 派发 CustomEvent('curis:runtime-capability')
 *   跨标签页 → 监听原生 storage 事件
 *   两条通道汇总到同一个 subscribe，组件只订阅一次。
 *
 * SSR 安全：所有 localStorage 访问都包了 typeof window 判断 + try/catch
 *   （Safari 隐私模式下 localStorage.setItem 会抛异常，此时静默降级为
 *   「仅本次会话有效」，绝不阻断交互）。
 */

import { useCallback, useEffect, useMemo, useState } from "react";
import { usePathname } from "next/navigation";
import { getCapabilities } from "./capabilities.js";

export const RUNTIME_CAP_EVENT = "curis:runtime-capability";
const KEY_PREFIX = "curis-runtime-cap:";

/** 能力类型 → 中文分组名。与能力中心 TABS 保持一致，改一处必须同步改另一处。 */
export const CAPABILITY_TYPE_LABEL = {
  model: "模型",
  agent: "AI 员工",
  skill: "技能",
  tool: "工具",
  workflow: "工作流",
  connector: "连接器",
  cli: "CLI",
  api: "HTTP API",
  webhook: "Webhook",
  mcp: "MCP",
};

/** 分组展示顺序：高频在前，降低长列表的选择成本。 */
const TYPE_ORDER = [
  "model",
  "agent",
  "skill",
  "tool",
  "workflow",
  "connector",
  "cli",
  "api",
  "webhook",
  "mcp",
];

export function runtimeCapStorageKey(pathname) {
  return KEY_PREFIX + (pathname || "/");
}

export function readRuntimeCapability(pathname) {
  if (typeof window === "undefined") return "";
  try {
    return window.localStorage.getItem(runtimeCapStorageKey(pathname)) || "";
  } catch {
    return "";
  }
}

export function writeRuntimeCapability(pathname, capabilityKey) {
  if (typeof window === "undefined") return;
  const storageKey = runtimeCapStorageKey(pathname);
  try {
    if (capabilityKey) window.localStorage.setItem(storageKey, capabilityKey);
    else window.localStorage.removeItem(storageKey);
  } catch {
    // 隐私模式 / 配额耗尽：静默降级，选择仅在本次会话内存中有效。
  }
  // 同标签页广播：storage 事件不会在写入方触发，必须自己发一次。
  window.dispatchEvent(
    new CustomEvent(RUNTIME_CAP_EVENT, { detail: { pathname, capabilityKey } })
  );
}

/**
 * 订阅当前页的能力选择变化（同标签页 + 跨标签页两条通道）。
 * @returns {() => void} 取消订阅
 */
export function subscribeRuntimeCapability(pathname, onChange) {
  if (typeof window === "undefined") return () => {};
  const storageKey = runtimeCapStorageKey(pathname);

  const onCustom = (event) => {
    if (event?.detail?.pathname === pathname) onChange(event.detail.capabilityKey || "");
  };
  const onStorage = (event) => {
    if (event.key === storageKey) onChange(event.newValue || "");
  };

  window.addEventListener(RUNTIME_CAP_EVENT, onCustom);
  window.addEventListener("storage", onStorage);
  return () => {
    window.removeEventListener(RUNTIME_CAP_EVENT, onCustom);
    window.removeEventListener("storage", onStorage);
  };
}

/**
 * 运行现场读取 / 设置「当前能力」。
 *
 * 用法（页面侧）：
 *   const { capabilityKey, setCapabilityKey } = useRuntimeCapability();
 *   // 发起执行时把 capabilityKey 一并提交给后端
 *
 * 注意：首帧一定返回空字符串，localStorage 在 useEffect 里补读，
 *       避免 SSR / CSR 首帧不一致导致的 hydration 报错。
 */
export function useRuntimeCapability() {
  const pathname = usePathname();
  const [capabilityKey, setState] = useState("");

  useEffect(() => {
    setState(readRuntimeCapability(pathname));
    return subscribeRuntimeCapability(pathname, setState);
  }, [pathname]);

  const setCapabilityKey = useCallback(
    (next) => {
      setState(next || "");
      writeRuntimeCapability(pathname, next || "");
    },
    [pathname]
  );

  return { capabilityKey, setCapabilityKey, pathname };
}

/**
 * 拉取可切换的能力目录（只取已启用项），并按类型分组。
 *
 * 失败不抛：运行现场的顶栏不能因为能力目录读不到就整页崩，
 * 降级为 error 文案 + 重试入口，页面主流程照常可用。
 */
export function useCapabilityOptions() {
  const [capabilities, setCapabilities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const reload = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const payload = await getCapabilities({ includeInactive: false });
      const list = Array.isArray(payload?.capabilities) ? payload.capabilities : [];
      setCapabilities(list.filter((item) => item && item.capability_key));
    } catch (err) {
      setCapabilities([]);
      setError(err?.message || "能力目录读取失败");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    reload();
  }, [reload]);

  const groups = useMemo(() => {
    const bucket = new Map();
    capabilities.forEach((item) => {
      const type = item.type || "other";
      if (!bucket.has(type)) bucket.set(type, []);
      bucket.get(type).push(item);
    });
    const known = TYPE_ORDER.filter((type) => bucket.has(type));
    const unknown = [...bucket.keys()].filter((type) => !TYPE_ORDER.includes(type)).sort();
    return [...known, ...unknown].map((type) => ({
      type,
      label: CAPABILITY_TYPE_LABEL[type] || type,
      items: bucket.get(type),
    }));
  }, [capabilities]);

  return { capabilities, groups, loading, error, reload };
}
