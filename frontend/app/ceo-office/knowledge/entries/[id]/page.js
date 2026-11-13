"use client";

import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";
import { useParams, useSearchParams } from "next/navigation";

import TerraShell, { TerraPaneContent } from "../../../../../components/terra/TerraShell.js";
import { TerraButton, TerraCard, TerraCardHeader, TerraPageHead, TerraTag } from "../../../../../components/terra/TerraPrimitives.js";
import { TerraErrorState, TerraLoadingSkeleton } from "../../../../../components/terra/TerraState.js";
import {
  archiveKnowledgeEntry,
  getKnowledgeEntry,
  getKnowledgeResults,
  getKnowledgeUsedBy,
} from "../../../../../lib/knowledge.js";

import { useRuntime } from "../../../../../components/runtime/RuntimeProvider.js";

const SOURCE = { local_file: "本地文件", manual: "手工内容" };
const RESULT = { RESULT: "结果", ARTIFACT: "成果", EVIDENCE: "证据" };

function safeReturn(value) {
  return value?.startsWith("/ceo-office/knowledge") ? value : "/ceo-office/knowledge";
}

function readableStatus(value) {
  const labels = {
    ACTIVE: "可引用",
    ARCHIVED: "已归档",
    PLANNED: "待开始",
    ACTIVE_WORK: "进行中",
    RUNNING: "进行中",
    WAITING: "等待输入",
    COMPLETED: "已完成",
    FAILED: "处理失败",
  };
  return labels[value] || "状态未知";
}

export function KnowledgeReader({ companyId }) {
  const params = useParams();
  const searchParams = useSearchParams();
  const id = params?.id || "";
  const backHref = safeReturn(searchParams.get("return_to") || "");
  const [state, setState] = useState({ status: "loading", entry: null, works: [], results: [], error: "" });
  const [archiving, setArchiving] = useState(false);
  const [sourceRequest, setSourceRequest] = useState(0);
  const alive = useRef(true), generation = useRef(0);
  useEffect(() => { alive.current = true; return () => { alive.current = false; generation.current += 1; }; }, []);

  const load = useCallback(async () => {
    if (!id || !companyId) return;
    const ticket = ++generation.current;
    setState((current) => ({ ...current, status: "loading", error: "" }));
    try {
      const [entry, used, results] = await Promise.all([
        getKnowledgeEntry(id),
        getKnowledgeUsedBy(id),
        getKnowledgeResults(id),
      ]);
      if (!alive.current || ticket !== generation.current) return;
      if (entry.company_id !== companyId) throw new Error("这条资料不属于当前公司，请返回资料库重新选择。");
      setState({ status: "ready", entry, works: used?.works || [], results: results?.results || [], error: "" });
    } catch (error) {
      if (!alive.current || ticket !== generation.current) return;
      setState({ status: "error", entry: null, works: [], results: [], error: error?.message || "无法读取资料" });
    }
  }, [id, companyId]);

  useEffect(() => { load(); }, [load]);

  async function archive() {
    if (!confirm("归档后，历史工作仍可追溯这条资料，但新工作不能再选择它。确认归档？")) return;
    setArchiving(true);
    try {
      await archiveKnowledgeEntry(id);
      if (alive.current) await load();
    } catch (error) {
      if (!alive.current) return;
      setState((current) => ({ ...current, error: error?.message || "归档失败" }));
    } finally {
      if (alive.current) setArchiving(false);
    }
  }

  if (!companyId) return <TerraShell topCrumb="资料库"><TerraErrorState message="请先选择公司，再阅读资料。" /></TerraShell>;
  if (state.status === "loading") return <TerraShell topCrumb="资料库 / 阅读"><TerraLoadingSkeleton variant="page" /></TerraShell>;
  if (state.status === "error" || !state.entry) return <TerraShell topCrumb="资料库 / 阅读"><TerraErrorState message={state.error || "资料不存在"} onRetry={load} /></TerraShell>;

  const entry = state.entry;
  const sourceAvailable = entry.source_status === "AVAILABLE";
  const summary = String(entry.summary || "").replace(/\s+/g, " ").trim();
  const independentSummary = summary && !String(entry.body || "").replace(/\s+/g, " ").trim().startsWith(summary);
  return <TerraShell topCrumb="资料库 / 阅读" assistantContext={{ page: "knowledge-entry", knowledgeId: id }}>
    <Link href={backHref} className="mb-4 inline-flex text-ui-1 font-bold text-ui-primary no-underline">← 返回资料库</Link>
    <TerraPageHead
      title={entry.title}
      subtitle={`${entry.scope_name || "归属未知"} · ${SOURCE[entry.source_type] || "来源未知"}`}
      pill={{ text: readableStatus(entry.lifecycle_status), icon: "i-auto_stories" }}
      actions={<div className="flex flex-wrap gap-2"><TerraButton variant="ghost" onClick={() => setSourceRequest((value) => value + 1)}>来源与引用</TerraButton>{entry.lifecycle_status === "ACTIVE" && <TerraButton variant="ghost" disabled={archiving} onClick={archive}>{archiving ? "归档中…" : "归档资料"}</TerraButton>}</div>}
    />

    {state.error && <div className="mb-4 rounded-ui-sm border border-ui-red bg-ui-red-soft px-4 py-3 text-ui-1 text-ui-red">{state.error}</div>}
    {!sourceAvailable && <div className="mb-4 rounded-ui-sm border border-ui-amber bg-ui-amber-soft px-4 py-3 text-ui-1 text-ui-amber">原始来源当前不可访问。历史引用仍保留，但请恢复本地资料根后再核对原文。</div>}

    <TerraPaneContent utilityRequestTabId="current" utilityLabel="来源与引用" utilityRequestKey={sourceRequest} utilityPane={<div className="space-y-5 p-5">
        <TerraCard>
          <TerraCardHeader icon="i-link" iconClass="cyan" title="来源与范围" />
          <dl className="space-y-3 text-ui-2">
            <div><dt className="text-ui-1 text-ui-txt-3">来源</dt><dd className="mt-1 text-ui-txt">{entry.source_label || SOURCE[entry.source_type] || "来源未知"}</dd></div>
            {entry.source_path && <div><dt className="text-ui-1 text-ui-txt-3">相对路径</dt><dd className="mt-1 break-words text-ui-txt">{entry.source_path}</dd></div>}
            <div><dt className="text-ui-1 text-ui-txt-3">使用范围</dt><dd className="mt-1 text-ui-txt">{entry.scope_name || "归属未知"}</dd></div>
            <div><dt className="text-ui-1 text-ui-txt-3">最近更新</dt><dd className="mt-1 text-ui-txt">{entry.updated_at || "时间未知"}</dd></div>
          </dl>
        </TerraCard>

        <TerraCard>
          <TerraCardHeader icon="i-widgets" title="被哪些工作使用" />
          {state.works.length ? <ul className="divide-y divide-ui-line">{state.works.map((work) => <li key={work.work_ref} className="py-3 first:pt-0 last:pb-0"><Link href={`/ceo-office/workspace?workspace_id=${encodeURIComponent(work.workspace_id)}`} className="font-semibold text-ui-2 text-ui-txt no-underline hover:text-ui-primary">{work.title}</Link><p className="mt-1 text-ui-1 text-ui-txt-3">{work.responsibility || "责任未记录"} · {readableStatus(work.status)}</p></li>)}</ul> : <p className="text-ui-2 text-ui-txt-3">还没有工作引用这条资料。</p>}
        </TerraCard>

        <TerraCard>
          <TerraCardHeader icon="i-verified" iconClass="violet" title="相关结果与证据" />
          {state.results.length ? <ul className="space-y-2">{state.results.map((result) => <li key={`${result.kind}:${result.reference_id}`} className="rounded-ui-sm bg-ui-surface-2 px-3 py-2 text-ui-2 text-ui-txt"><strong>{RESULT[result.kind] || "引用"}</strong><span className="ml-2 text-ui-1 text-ui-txt-3">来自已引用工作</span></li>)}</ul> : <p className="text-ui-2 text-ui-txt-3">引用工作尚未产生可追溯结果。</p>}
        </TerraCard>

        <details className="rounded-ui-md border border-ui-line bg-ui-surface px-4 py-3 text-ui-1 text-ui-txt-3">
          <summary className="cursor-pointer font-bold text-ui-txt-2">查看技术详情</summary>
          <dl className="mt-3 space-y-2 break-all"><div><dt>资料标识</dt><dd>{entry.id}</dd></div><div><dt>范围状态</dt><dd>{entry.scope_status}</dd></div><div><dt>内容校验</dt><dd>{entry.content_sha256 || "未记录"}</dd></div></dl>
        </details>
</div>} />
    <div className="mx-auto max-w-[75ch]">
      <main>
        <article className="min-h-[520px] py-4">
          <p className="text-ui-1 font-bold text-ui-primary">资料正文</p>
          {independentSummary && <section className="mt-3 border-b border-ui-line pb-4"><h2 className="text-ui-1 font-semibold text-ui-txt-3">摘要</h2><p className="mt-2 text-ui-3 leading-relaxed text-ui-txt-2">{entry.summary}</p></section>}
          <div className="mt-6 whitespace-pre-wrap break-words text-ui-3 leading-8 text-ui-txt">{entry.body || "正文为空"}</div>
          {!!entry.tags?.length && <div className="mt-8 flex flex-wrap gap-2">{entry.tags.map((tag) => <TerraTag key={tag} color="violet">{tag}</TerraTag>)}</div>}
        </article>
      </main>


    </div>
  </TerraShell>;
}

export default function KnowledgeEntryPage() {
  const runtime = useRuntime(), params = useParams();
  return <KnowledgeReader key={`${runtime.companyId || "none"}:${params?.id || ""}`} companyId={runtime.companyId || ""} />;
}
