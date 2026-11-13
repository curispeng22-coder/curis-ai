"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRuntime } from "../../../components/runtime/RuntimeProvider.js";
import ModelManagement from "../../../components/v1/ModelManagement.js";
import PrivateAgentDrawer, { AgentAllowancePanel } from "./PrivateAgentDrawer.js";
import { getPrivateCapabilities } from "../../../lib/capabilities.js";

export function AgentSetupPanel() {
  const runtime = useRuntime();
  const [editingAgent, setEditingAgent] = useState(null);
  const [open, setOpen] = useState(false), [agents, setAgents] = useState(null);
  const [expanded, setExpanded] = useState(false);
  const [busy, setBusy] = useState(false), [error, setError] = useState("");
  const request = useRef(0);
  async function read() {
    const token = ++request.current;
    setBusy(true); setError("");
    try {
      const result = await getPrivateCapabilities("agent");
      if (token === request.current) setAgents(result.capabilities || []);
    } catch (reason) {
      if (token === request.current) { setAgents(null); setError(reason.message || "已登记 Agent 暂时无法读取。"); }
    } finally { if (token === request.current) setBusy(false); }
  }
  useEffect(() => { read(); return () => { request.current++; }; }, []);
  return <section id="employee-agents" className="mb-6 rounded-2xl border border-ui-line bg-ui-surface p-4">
    <button type="button" aria-expanded={expanded} aria-controls="employee-agent-panel" onClick={() => setExpanded((value) => !value)} className="cursor-pointer font-semibold">配置外部 Agent 与员工执行</button>
    <div id="employee-agent-panel" hidden={!expanded} className="mt-4 space-y-4">
      <p>先登记 Agent，再到员工资料选择能力、到人才市场的「技能」页安装并分配完整技能，最后确认额度和独立浏览器连接。保存配置不代表连接或执行已验证。</p>
      <div className="flex flex-wrap gap-4">
        <button type="button" onClick={() => { setEditingAgent(null); setOpen(true); }}>注册自定义 Agent</button>
        <button type="button" disabled={busy} onClick={read}>{busy ? "正在读取…" : "读取已登记 Agent"}</button>
        <Link href="/ceo-office/organization">前往员工资料绑定</Link>
        <Link href="/ceo-office/talent-market?returnTo=%2Fceo-office%2Fcapabilities%23employee-agents">前往人才市场安装技能</Link>
      </div>
      {agents && <><h2 className="font-semibold">已登记 Agent</h2>{agents.length ? <ul>{agents.map((item) => <li key={item.capability_id}>{item.display_name} · {item.capability_id} · {item.metadata?.kind === "codex-cli" ? "本机 Codex" : item.metadata?.kind || "接入类型待核对"} · 连接与执行待核验{item.metadata?.kind === "acp-stdio" && item.metadata?.agent_id === "deepseek_harness" && <button type="button" disabled={runtime.status !== "ready" || !runtime.companyId} onClick={() => { setEditingAgent(item); setOpen(true); }}>编辑账号配置</button>}</li>)}</ul> : <p>尚未登记 Agent。</p>}</>}
      {error && <p role="alert">{error}</p>}
      <AgentAllowancePanel />
      <Link href="/ceo-office/settings?tab=models">返回模型设置</Link>
      <PrivateAgentDrawer open={open} editingAgent={editingAgent} companyId={runtime.companyId || ""} onClose={() => setOpen(false)} onSuccess={() => { setOpen(false); read(); }} />
    </div>
  </section>;
}

export default function CapabilitiesPage() {
  return <ModelManagement><AgentSetupPanel /></ModelManagement>;
}
