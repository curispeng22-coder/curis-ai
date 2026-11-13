"use client";

import { createContext, useContext, useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAssistantPageContext } from "../assistant/GlobalAssistant.js";
import WorkspacePaneShell from "../workspace/WorkspacePaneShell.js";

const PaneContentContext = createContext(null);

export function terraPaneAvailability(content = {}, readingDirectory = null) {
  return { context: Boolean(content.contextPane || readingDirectory), utility: Boolean(content.utilityPane || content.utilityTabs?.length) };
}

export function TerraPaneContent({ contextPane, utilityPane, utilityTabs, contextLabel = "当前工作", utilityLabel = "结果与证据", utilityRequestKey = 0, utilityRequestTabId = "", initialContextOpen = false, initialUtilityOpen = false }) {
  const setContent = useContext(PaneContentContext);
  useEffect(() => {
    setContent?.({ contextPane, utilityPane, utilityTabs, contextLabel, utilityLabel, utilityRequestKey, utilityRequestTabId, initialContextOpen, initialUtilityOpen });
    return () => setContent?.({});
  }, [setContent, contextPane, utilityPane, utilityTabs, contextLabel, utilityLabel, utilityRequestKey, utilityRequestTabId, initialContextOpen, initialUtilityOpen]);
  return null;
}

/**
 * TerraShell — 顶层壳组件（nav + main）。
 *
 * 响应式行为：
 * - 共享D0 host按实际可用Main宽度切换辅助栏为overlay。
 * - 本适配层保留旧消费者props和返回语义；用户主题位于头像入口。
 *
 * Props:
 * - children: 页面内容
 * - topCrumb: 顶部面包屑文字
 * - topbarExtra: 顶部栏右侧额外内容
 * - assistantContext: 当前页面提供的安全结构化上下文
 */
export default function TerraShell({
  children,
  topCrumb = "",
  topbarExtra,
  assistantContext,
}) {
  const [paneContent, setPaneContent] = useState({});
  const pathname = usePathname();
  const [returnTo, setReturnTo] = useState("");
  useEffect(() => {
    const target = new URLSearchParams(window.location.search).get("return_to") || "";
    setReturnTo(target.startsWith("/ceo-office/conversation?conversation_id=") ? target : "");
  }, [pathname]);
  useAssistantPageContext(assistantContext || { page: "workspace" });
  // The existing Reader provides this context only after its actual entry is readable.
  const readingDirectory = assistantContext?.page === "knowledge-entry" && assistantContext.knowledgeId
    ? <nav aria-label="资料目录" className="space-y-3 text-sm"><Link href="/ceo-office/knowledge" className="block text-ui-primary">公司资料</Link><span aria-current="page" className="block text-ui-txt-2">当前资料</span></nav>
    : null;
  const available = terraPaneAvailability(paneContent, readingDirectory);

  return (
    <PaneContentContext.Provider value={setPaneContent}>
      <WorkspacePaneShell workspaceId={`surface:${pathname}`} breadcrumb={topCrumb}
        {...paneContent} contextPane={paneContent.contextPane || readingDirectory}
        contextLabel={paneContent.contextLabel || (readingDirectory ? "资料目录" : "当前工作")}
        contextAvailable={available.context} utilityAvailable={available.utility}
        surfaceId={pathname} headerExtra={topbarExtra}>
          {returnTo ? <Link href={returnTo} className="mb-4 inline-block text-ui-primary">← 返回对话</Link> : null}
          {children}
      </WorkspacePaneShell>
    </PaneContentContext.Provider>
  );
}
