"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import TerraShell, { TerraPaneContent } from "../../../components/terra/TerraShell.js";
import { useRuntime } from "../../../components/runtime/RuntimeProvider.js";
import {
  getOperatingIntelligence,
  runtimeErrorMessage,
  submitOperatingReportDecision,
} from "../../../lib/runtimeApi.js";

const TABS = [
  ["business", "业务结果"], ["execution", "运行与执行"], ["cost", "使用与成本"],
  ["quality", "质量与反馈"], ["organization", "组织与员工"], ["models", "模型与能力"], ["reports", "分析报告"],
];
const DIMENSION_METRICS = { execution: ["latency_p50", "failure_rate"], cost: ["provider_cost"], quality: ["acceptance_rate"] };

const STATE_COPY = {
  FACT: "事实",
  POLICY: "规则",
  EVIDENCE: "证据",
  EST: "员工估算",
  UNK: "未知",
  VERIFIED: "已核实",
  ESTIMATED: "估算",
  UNKNOWN: "未知",
  COMPARABLE: "可比较",
  NOT_COMPARABLE: "暂不可比较",
  WAITING_CEO: "等待 CEO 决定",
};

const SOURCE_COPY = {
  "Company OS": "公司经营记录",
  "Result / Acceptance": "结果与验收",
  "AI Usage Ledger": "AI 使用记录",
  "Acceptance Runtime": "结果验收记录",
};

const formatValue = (metric) => {
  if (metric?.value === null || metric?.value === undefined) return "—";
  if (metric.unit === "CURRENCY") {
    const symbol = { CNY: "¥", USD: "$", EUR: "€" }[metric.currency] || `${metric.currency || ""} `;
    return `${symbol}${Number(metric.value).toFixed(2)}`;
  }
  if (metric.unit === "%") return `${metric.value}%`;
  if (metric.unit === "ms") return `${metric.value} ms`;
  return String(metric.value);
};

function StatePill({ value }) {
  const caution = ["UNKNOWN", "ESTIMATED", "NOT_COMPARABLE"].includes(value);
  return (
    <span className={`rounded-full px-2.5 py-1 text-ui-1 font-semibold ${caution ? "bg-ui-amber-soft text-ui-amber" : "bg-ui-green-soft text-ui-green"}`}>
      {STATE_COPY[value] || value}
    </span>
  );
}

function Empty({ title, detail }) {
  return (
    <div className="rounded-2xl border border-dashed border-ui-line bg-ui-surface-2 px-6 py-12 text-center">
      <h3 className="text-base font-semibold">{title}</h3>
      <p className="mx-auto mt-2 max-w-xl text-sm leading-6 text-ui-txt-3">{detail}</p>
    </div>
  );
}

function Metric({ metric, onInspect }) {
  return (
    <button type="button" onClick={() => onInspect(metric)} className="min-w-0 rounded-ui-md border border-ui-line bg-ui-surface p-4 text-left transition hover:border-ui-primary">
      <div className="flex items-center justify-between gap-2">
        <span className="text-xs text-ui-txt-3">{metric.label}</span>
        <StatePill value={metric.verification} />
      </div>
      <strong className="mt-3 block text-2xl font-semibold tracking-[-0.03em]">{formatValue(metric)}</strong>
      <p className="mt-2 text-xs text-ui-txt-3">
        {metric.comparison == null ? "上期口径不足" : `较上期 ${metric.comparison > 0 ? "+" : ""}${metric.comparison}${metric.unit === "CURRENCY" ? "" : metric.unit}`}
      </p>
    </button>
  );
}

function Overview({ data, onInspect, dimension }) {
  const keys = DIMENSION_METRICS[dimension];
  const metrics = keys ? data.metrics.filter((item) => keys.includes(item.key)) : dimension === "business" ? data.metrics : [];
  return <div className="space-y-7">
    <header className="border-b border-ui-line pb-4"><p className="text-ui-1 text-ui-txt-3">{data.scope.name} · 最近 {data.time_range.days} 天</p><h2 className="mt-2 text-xl font-semibold text-ui-txt">{dimension === "business" ? data.summary.headline : TABS.find(([key]) => key === dimension)?.[1]}</h2></header>
    {dimension === "business" ? <div className="grid gap-x-8 gap-y-6 md:grid-cols-2">{[["事实", data.summary.fact], ["解读", data.summary.analysis], ["仍未知", data.trust.external_outcome.label], ["建议与行动", data.summary.recommendation]].map(([label, body]) => <section key={label} className="border-t border-ui-line pt-4"><h3 className="text-sm font-semibold text-ui-primary">{label}</h3><p className="mt-2 max-w-[70ch] text-sm leading-7 text-ui-txt-2">{body}</p></section>)}</div> : null}
    {metrics.length ? <section aria-label="经营事实"><div className="mb-3 flex items-center justify-between"><h3 className="text-sm font-semibold">{dimension === "business" ? "公司投入与执行事实" : "本期记录"}</h3><span className="text-xs text-ui-txt-3">选择指标查看原始来源</span></div><div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">{metrics.map((metric) => <Metric key={metric.key} metric={metric} onInspect={onInspect} />)}</div></section> : dimension !== "business" ? <Empty title={dimension === "organization" ? "组织经营证据尚未汇集" : "模型能力经营证据尚未汇集"} detail={dimension === "organization" ? "可到组织中心查看当前岗位与员工。此期间还没有可比较的人员经营记录。" : "可到设置查看已配置的模型。没有可核验的能力经营记录时，不会生成排名或趋势。"} /> : null}
    {metrics.length > 0 && <Explore data={data} metricKeys={metrics.map((item) => item.key)} onInspect={onInspect} />}
    <footer className="border-t border-ui-line pt-4 text-xs leading-6 text-ui-txt-3">来源：{data.trust.canonical_sources.map((source) => SOURCE_COPY[source] || source).join(" · ") || "尚未读取"} · 人工记录 {data.trust.manual_count} 条</footer>
  </div>;
}

function Explore({ data, metricKeys, onInspect }) {
  const groups = data.benchmark.metrics.filter((group) => metricKeys.includes(group.metric));
  return <section className="border-t border-ui-line pt-5"><h3 className="font-semibold">各业务同口径比较</h3><p className="mt-1 text-xs leading-6 text-ui-txt-3">业务原生结果单位不同，不能相加；样本不足时不排名。</p><div className="mt-4 space-y-5">{groups.map((group) => <section key={group.metric}><div className="mb-2 flex items-center gap-3"><button type="button" onClick={() => onInspect(data.metrics.find((item) => item.key === group.metric))} className="text-sm font-semibold text-ui-primary">{data.metrics.find((item) => item.key === group.metric)?.label || "当前指标"}</button><StatePill value={group.status} /></div>{group.status === "COMPARABLE" ? <table className="w-full text-sm"><caption className="sr-only">同口径业务比较</caption><thead className="border-b border-ui-line text-left text-xs text-ui-txt-3"><tr><th className="py-2 font-medium">业务</th><th className="py-2 text-right font-medium">本期记录</th></tr></thead><tbody className="divide-y divide-ui-line">{group.rows.map((row) => <tr key={row.business_id}><td className="py-3">{row.name}</td><td className="py-3 text-right font-semibold">{formatValue(row)}</td></tr>)}</tbody></table> : <p className="border-b border-ui-line pb-3 text-sm text-ui-txt-2">{group.reason}</p>}</section>)}</div></section>;
}

function Reports({ data, onDecision, onInspect }) {
  const [selected, setSelected] = useState("");
  const report = data.reports.find((item) => item.artifact_id === selected);
  if (!report) return <section><header className="mb-5"><h2 className="text-xl font-semibold">分析报告</h2><p className="mt-2 text-sm text-ui-txt-2">从已有报告阅读事实、判断与下一步。</p></header>{data.reports.length ? <div className="divide-y divide-ui-line border-y border-ui-line">{data.reports.map((item) => <button key={item.artifact_id} type="button" onClick={() => setSelected(item.artifact_id)} className="flex w-full items-center justify-between gap-4 py-4 text-left hover:text-ui-primary"><span><strong className="block text-sm font-semibold">{item.title}</strong><span className="mt-1 block text-xs text-ui-txt-3">{new Date(item.created_at).toLocaleDateString("zh-CN")}</span></span><span className="text-sm">阅读报告 →</span></button>)}</div> : <Empty title="还没有经营分析报告" detail="先积累可复核的经营事实。已有的分析成果会出现在这里。" />}</section>;
  const content = report.content;
  return <article><button type="button" onClick={() => setSelected("")} className="mb-4 text-sm font-semibold text-ui-primary">← 返回报告列表</button><header className="flex flex-wrap items-start justify-between gap-4 border-b border-ui-line pb-5"><div><p className="text-xs text-ui-txt-3">分析报告 · {data.scope.name}</p><h2 className="mt-2 text-2xl font-semibold">{report.title}</h2></div><button type="button" onClick={() => onInspect({ kind: "report", report })} className="rounded-ui-sm border border-ui-line px-3 py-2 text-sm font-semibold">查看依据</button></header><div className="mt-6 grid gap-x-8 gap-y-6 md:grid-cols-2">{[['事实', content.facts], ['解读', content.analysis], ['仍未知', content.unknown]].map(([title, items]) => <section key={title} className="border-t border-ui-line pt-4"><h3 className="text-sm font-semibold text-ui-primary">{title}</h3><ul className="mt-3 space-y-3">{items.map((item, index) => <li key={index} className="text-sm leading-7"><StatePill value={item.provenance} /><p className="mt-2">{item.value}</p></li>)}</ul></section>)}<section className="border-t border-ui-line pt-4"><h3 className="text-sm font-semibold text-ui-primary">建议与行动</h3><p className="mt-3 text-sm leading-7">{content.recommendation.value}</p>{content.decisionCandidate ? report.decision ? <p className="mt-4 text-sm text-ui-amber">已形成 CEO 决策事项 · {STATE_COPY[report.decision.status] || "查看决策状态"}</p> : <button onClick={() => onDecision(report.artifact_id)} className="mt-4 rounded-ui-sm bg-ui-primary px-4 py-2.5 text-sm font-semibold text-ui-primary-fg">查看方案并交给 CEO 决定</button> : null}</section></div></article>;
}

function SourceDetail({ selected, data }) {
  if (selected.kind === "report") return <div className="space-y-4 p-5"><h2 className="text-lg font-semibold">{selected.report.title} · 依据</h2><p className="text-sm">作者：{selected.report.content.author?.name || "未记录"}</p><p className="text-sm text-ui-txt-2">{data.scope.name} · 最近 {data.time_range.days} 天</p><details className="border-t border-ui-line pt-4 text-sm"><summary className="cursor-pointer">查看来源标识</summary><ul className="mt-3 space-y-2 break-all text-xs text-ui-txt-2">{selected.report.content.evidenceRefs.map((ref) => <li key={ref}>{ref}</li>)}</ul></details></div>;
  return <div className="space-y-5 p-5"><header><p className="text-xs text-ui-txt-3">原始指标与来源</p><h2 className="mt-2 text-lg font-semibold">{selected.label}</h2><div className="mt-3"><StatePill value={selected.verification} /></div></header><dl className="grid grid-cols-2 gap-x-4 gap-y-3 text-sm"><dt className="text-ui-txt-3">本期</dt><dd className="text-right font-semibold">{formatValue(selected)}</dd><dt className="text-ui-txt-3">上一周期</dt><dd className="text-right">{selected.baseline == null ? "—" : formatValue({ ...selected, value: selected.baseline })}</dd><dt className="text-ui-txt-3">样本</dt><dd className="text-right">{selected.sample_size}</dd><dt className="text-ui-txt-3">来源</dt><dd className="text-right">{SOURCE_COPY[selected.source] || selected.source}</dd><dt className="text-ui-txt-3">期间</dt><dd className="text-right">最近 {data.time_range.days} 天</dd><dt className="text-ui-txt-3">最近记录</dt><dd className="text-right">{selected.updated_at ? new Date(selected.updated_at).toLocaleString("zh-CN") : "未记录"}</dd></dl><p className="text-sm leading-6 text-ui-txt-2">{selected.unknown_reason || "只比较相同定义、单位和期间的记录。"}</p><details className="border-t border-ui-line pt-4 text-sm"><summary className="cursor-pointer">查看来源标识</summary><ul className="mt-3 space-y-2 break-all text-xs">{(selected.source_refs || []).map((ref) => <li key={ref}>{ref}</li>)}</ul></details></div>;
}

export function InsightsSurface({ companyId }) {
  const [tab, setTab] = useState("business");
  const [days, setDays] = useState(30), [businessId, setBusinessId] = useState("");
  const [snapshot, setSnapshot] = useState(null), [selected, setSelected] = useState(null);
  const [detailRequest, setDetailRequest] = useState(0), [error, setError] = useState(""), [busy, setBusy] = useState(false);
  const generation = useRef(0), alive = useRef(true), deciding = useRef(false);
  const key = JSON.stringify([companyId, businessId, days]);
  const data = snapshot?.key === key ? snapshot.data : null;
  useEffect(() => { alive.current = true; return () => { alive.current = false; generation.current += 1; }; }, []);
  const load = useCallback(async () => {
    if (!companyId) return;
    const ticket = ++generation.current;
    setBusy(true); setError(""); setSelected(null);
    try {
      const next = await getOperatingIntelligence(companyId, { days, businessId });
      if (!alive.current || ticket !== generation.current) return;
      if (next.company?.company_id !== companyId || next.scope?.ref !== (businessId || companyId)) throw new Error("经营资料的范围已变化，请重新读取。");
      setSnapshot({ key, data: next });
    } catch (failure) { if (alive.current && ticket === generation.current) setError(runtimeErrorMessage(failure)); }
    finally { if (alive.current && ticket === generation.current) setBusy(false); }
  }, [businessId, days, companyId, key]);
  useEffect(() => { load(); return () => { generation.current += 1; }; }, [load]);
  const scopes = useMemo(() => data?.scopes || [], [data]);
  const createDecision = async (artifactId) => {
    if (deciding.current || !data?.reports.some((item) => item.artifact_id === artifactId)) return;
    deciding.current = true; setBusy(true); setError("");
    const ticket = generation.current;
    try { await submitOperatingReportDecision(companyId, artifactId); if (alive.current && ticket === generation.current) await load(); }
    catch (failure) { if (alive.current && ticket === generation.current) setError(runtimeErrorMessage(failure)); }
    finally { deciding.current = false; if (alive.current && ticket === generation.current) setBusy(false); }
  };
  const inspect = (item) => { if (!item) return; setSelected(item); setDetailRequest((value) => value + 1); };
  const chooseTab = useCallback((value) => { setTab(value); setSelected(null); }, []);
  const context = useMemo(() => companyId ? <nav aria-label="经营分析目录" className="grid auto-rows-max content-start gap-1 text-sm">
    {TABS.map(([value, label]) => <button key={value} type="button" onClick={() => chooseTab(value)}
      aria-current={tab === value ? "page" : undefined} className={`rounded-ui-sm px-3 py-2 text-left hover:bg-ui-surface-2 ${tab === value ? "bg-ui-primary-light font-semibold text-ui-primary" : "text-ui-txt-2"}`}>{label}{value === "reports" && data ? ` · ${data.reports.length}` : ""}</button>)}
  </nav> : null, [companyId, tab, data, chooseTab]);
  return <TerraShell topCrumb="经营洞察" assistantContext={{ page: "operating-intelligence", companyId }}>
    <TerraPaneContent contextPane={context} contextLabel="经营分析目录" initialContextOpen utilityRequestTabId="current" utilityLabel="依据与来源" utilityRequestKey={detailRequest} utilityPane={selected && data ? <SourceDetail selected={selected} data={data} /> : null} />
    <div className="mx-auto w-full max-w-[1320px] text-ui-txt"><header className="flex flex-wrap items-end justify-between gap-4 border-b border-ui-line pb-5"><div><h1 className="text-2xl font-semibold tracking-[-0.025em]">经营洞察</h1><p className="mt-2 text-sm text-ui-txt-2">从事实看变化，从依据做决定。</p></div><div className="flex flex-wrap items-center gap-2"><select aria-label="分析范围" value={businessId} onChange={(event) => { setBusinessId(event.target.value); setSelected(null); }} className="h-9 max-w-[240px] rounded-ui-sm border border-ui-line bg-ui-surface px-3 text-sm"><option value="">全公司</option>{scopes.map((item) => <option key={item.business_id} value={item.business_id}>{item.name}</option>)}</select>{[7,30].map((value) => <button key={value} onClick={() => { setDays(value); setSelected(null); }} aria-pressed={days === value} className={`h-9 rounded-ui-sm px-3 text-sm font-semibold ${days === value ? "bg-ui-primary text-ui-primary-fg" : "border border-ui-line bg-ui-surface"}`}>{value} 天</button>)}</div></header>
    <nav aria-label="经营分析维度" className="mb-6 flex flex-wrap gap-x-5 border-b border-ui-line">{TABS.map(([value, label]) => <button key={value} type="button" onClick={() => chooseTab(value)} aria-pressed={tab === value} className={`border-b-2 py-3 text-sm font-semibold ${tab === value ? "border-ui-primary text-ui-primary" : "border-transparent text-ui-txt-2 hover:text-ui-primary"}`}>{label}</button>)}</nav>
    {error && <div role="alert" className="mb-5 flex items-center justify-between gap-4 rounded-ui-sm bg-ui-red-soft px-4 py-3 text-sm text-ui-red"><span>{error}</span><button onClick={load} className="font-semibold">重试</button></div>}
    <main aria-busy={busy}>{!companyId ? <Empty title="公司尚未建立" detail="建立公司后，在这里查看经营事实与报告。" /> : !data ? <Empty title={error ? "经营资料暂时无法读取" : "正在读取经营事实"} detail={error ? "重试读取，原来的分析范围保持不变。" : "读取当前公司已保存的记录。"} /> : tab === "reports" ? <Reports key={key} data={data} onDecision={createDecision} onInspect={inspect} /> : <Overview data={data} dimension={tab} onInspect={inspect} />}</main>
  </div></TerraShell>;
}

export default function OperatingIntelligence() {
  const runtime = useRuntime();
  return <InsightsSurface key={runtime.companyId || "no-company"} companyId={runtime.companyId || ""} />;
}
