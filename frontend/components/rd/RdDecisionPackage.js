"use client";

import { useState } from "react";

function Provenance({ fact }) {
  return <span>{fact?.value || "(UNK) 尚未验证"} <small className="text-ui-txt-3">({fact?.provenance || "UNK"})</small></span>;
}

export default function RdDecisionPackage({ decision, busy, onReview, onChoose }) {
  const [expanded, setExpanded] = useState(Boolean(decision?.data?.layer1ReviewedAt));
  if (!decision || decision.lifecycle_status !== "WAITING_CEO") return null;
  const data = decision.data || {};

  const view = async () => {
    if (await onReview()) setExpanded(true);
  };

  return <section className="rounded-ui-md border border-ui-warning bg-ui-warning/10 p-4" aria-label="需要 CEO 决策">
    <p className="text-ui-1 font-semibold text-ui-warning">需要 CEO 决策</p>
    <h2 className="mt-1 text-ui-3 font-semibold text-ui-txt">{data.event}</h2>
    {!expanded ? <div className="mt-3 flex gap-2">
      <button type="button" disabled={busy} onClick={view} className="rounded-ui-sm bg-ui-action-primary-bg px-3 py-2 text-ui-1 font-semibold text-ui-action-primary-fg disabled:opacity-50">查看方案</button>
      <button type="button" disabled={busy} onClick={() => onChoose("DEFER")} className="rounded-ui-sm border border-ui-line px-3 py-2 text-ui-1 font-semibold text-ui-txt disabled:opacity-50">暂缓</button>
    </div> : <div className="mt-4 grid gap-4">
      <p className="text-ui-1 text-ui-txt-2">AI 不能自行决定：{data.cannotDecideReason}</p>
      <div className="grid gap-3 md:grid-cols-2">
        {(data.options || []).map((option) => <article key={option.optionId} className="rounded-ui-sm border border-ui-line bg-ui-surface p-3">
          <h3 className="text-ui-2 font-semibold text-ui-txt">{option.label}</h3>
          <p className="mt-2 text-ui-1 text-ui-txt-2">影响：<Provenance fact={option.impact} /></p>
          <p className="mt-1 text-ui-1 text-ui-txt-2">风险：<Provenance fact={option.risk} /></p>
          <p className="mt-1 text-ui-1 text-ui-txt-2">代价：<Provenance fact={option.cost} /></p>
          <button type="button" disabled={busy} onClick={() => onChoose(option.optionId)} className="mt-3 rounded-ui-sm border border-ui-line px-3 py-2 text-ui-1 font-semibold text-ui-txt disabled:opacity-50">选择此方案</button>
        </article>)}
      </div>
      <p className="text-ui-1 text-ui-txt-2">员工建议：{data.recommendation?.optionId} ({data.recommendation?.provenance})</p>
      <p className="text-ui-1 text-ui-txt-2">理由：<Provenance fact={data.recommendationReason} /></p>
      <p className="text-ui-1 text-ui-txt-3">选择后：{data.continuationPlan}</p>
    </div>}
  </section>;
}
