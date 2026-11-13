"use client";

import { useCallback, useEffect, useState } from "react";

// Phase-8 Billing MVP (issue P8) · P8-3 Usage 只读聚合面板。
// 调用 /api/platform/usage/summary，按 tenant / model / capability / employee / workflow
// 分维度展示用量。仅含脱敏字段（credential_id / credential_ref_digest），不暴露明文凭证。
// tenant_id 缺失后端 fail-closed（返回 422）。

function costText(facts) {
  const rows = facts?.cost_by_currency;
  if (!rows?.length) return facts == null ? "尚未读取" : "未记录";
  return rows.map(row => {
    const known = row.known_cost;
    const label = row.currency === "UNKNOWN" ? "币种未知" : row.currency;
    const amount = known == null ? "" : `${Number(known).toFixed(4)} ${label}`;
    return row.unknown_cost_count > 0
      ? `${amount ? `已知部分 ${amount}；` : ""}${row.unknown_cost_count} 次费用未知`
      : amount || "费用未知";
  }).join("；");
}

function Field({ label, children }) {
  return (
    <label className="block text-sm font-bold text-zinc-700">
      {label}
      <div className="mt-1">{children}</div>
    </label>
  );
}

function DimensionTable({ title, columns, rows, emptyText }) {
  if (!rows || rows.length === 0) {
    return (
      <div className="mt-3">
        <h3 className="text-xs font-black uppercase text-zinc-500">{title}</h3>
        <div className="mt-1 rounded-md border border-dashed border-zinc-300 p-3 text-xs font-bold text-zinc-400">
          {emptyText}
        </div>
      </div>
    );
  }
  return (
    <div className="mt-3 overflow-x-auto">
      <h3 className="text-xs font-black uppercase text-zinc-500">{title}</h3>
      <table className="mt-1 w-full border-collapse text-sm">
        <thead>
          <tr className="border-b border-zinc-200 text-left text-xs text-zinc-500">
            {columns.map((c) => (
              <th key={c.key} className="py-2 pr-3">
                {c.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr key={idx} className="border-b border-zinc-100">
              {columns.map((c) => (
                <td key={c.key} className="py-2 pr-3 font-mono text-xs">
                  {c.key === "total_cost" ? costText(row) : row[c.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function UsageDashboardPanel({ apiFetch, onMessage }) {
  const [tenantId, setTenantId] = useState("default");
  const [periodStart, setPeriodStart] = useState("");
  const [periodEnd, setPeriodEnd] = useState("");
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);

  const load = useCallback(async () => {
    if (!tenantId) {
      onMessage("tenant_id 为必填参数（fail-closed）");
      return;
    }
    setLoading(true);
    try {
      const params = new URLSearchParams();
      params.set("tenant_id", tenantId);
      if (periodStart) params.set("period_start", periodStart);
      if (periodEnd) params.set("period_end", periodEnd);
      const next = await apiFetch(`/api/platform/usage/summary?${params.toString()}`);
      setSummary(next);
    } catch (error) {
      onMessage(error.message);
      setSummary(null);
    } finally {
      setLoading(false);
    }
  }, [apiFetch, onMessage, tenantId, periodStart, periodEnd]);

  useEffect(() => {
    load().catch(() => null);
  }, [load]);

  const totals = summary?.totals;

  return (
    <section className="rounded-md border border-zinc-200 bg-white p-4 shadow-sm">
      <h2 className="text-sm font-black uppercase text-zinc-500">用量聚合（只读 · 脱敏）</h2>
      <div className="mt-3 flex flex-wrap items-end gap-3">
        <Field label="tenant_id（必填）">
          <input
            className="min-w-[16rem] rounded-md border border-zinc-300 px-3 py-2 text-sm font-mono"
            required
            value={tenantId}
            onChange={(e) => setTenantId(e.target.value)}
          />
        </Field>
        <Field label="period_start（可选）">
          <input
            className="rounded-md border border-zinc-300 px-3 py-2 text-sm font-mono"
            value={periodStart}
            placeholder="如 2025-01-01"
            onChange={(e) => setPeriodStart(e.target.value)}
          />
        </Field>
        <Field label="period_end（可选）">
          <input
            className="rounded-md border border-zinc-300 px-3 py-2 text-sm font-mono"
            value={periodEnd}
            placeholder="如 2025-01-31"
            onChange={(e) => setPeriodEnd(e.target.value)}
          />
        </Field>
        <button
          type="button"
          className="h-10 rounded-md bg-zinc-950 px-4 text-sm font-bold text-white"
          onClick={load}
        >
          聚合
        </button>
      </div>

      <div className="mt-3 grid grid-cols-3 gap-3">
        <div className="rounded-md border border-zinc-200 p-3">
          <div className="text-xs font-bold text-zinc-500">总 token</div>
          <div className="font-mono text-lg font-black">{totals?.total_tokens ?? "尚未读取"}</div>
        </div>
        <div className="rounded-md border border-zinc-200 p-3">
          <div className="text-xs font-bold text-zinc-500">总事件数</div>
          <div className="font-mono text-lg font-black">{totals?.event_count ?? "尚未读取"}</div>
        </div>
        <div className="rounded-md border border-zinc-200 p-3">
          <div className="text-xs font-bold text-zinc-500">记录成本（非账单）</div>
          <div className="font-mono text-lg font-black">
            {costText(totals)}
          </div>
        </div>
      </div>

      {summary ? (
        <>
          <DimensionTable
            title="按模型 (by_model)"
            emptyText="无用量事件"
            columns={[
              { key: "model_name", label: "model_name" },
              { key: "total_tokens", label: "total_tokens" },
              { key: "total_cost", label: "total_cost" },
              { key: "count", label: "count" },
            ]}
            rows={summary.by_model}
          />
          <DimensionTable
            title="按能力来源 (by_capability_source)"
            emptyText="无用量事件"
            columns={[
              { key: "capability_source", label: "capability_source" },
              { key: "count", label: "count" },
              { key: "total_tokens", label: "total_tokens" },
            ]}
            rows={summary.by_capability_source}
          />
          <DimensionTable
            title="按员工 (by_employee)"
            emptyText="无用量事件"
            columns={[
              { key: "employee_id", label: "employee_id" },
              { key: "count", label: "count" },
              { key: "total_tokens", label: "total_tokens" },
            ]}
            rows={summary.by_employee}
          />
          <DimensionTable
            title="按工作流 (by_workflow)"
            emptyText="无用量事件"
            columns={[
              { key: "workflow_run_id", label: "workflow_run_id" },
              { key: "count", label: "count" },
              { key: "total_tokens", label: "total_tokens" },
            ]}
            rows={summary.by_workflow}
          />
        </>
      ) : (
        <div className="mt-3 text-sm font-bold text-zinc-400">
          {loading ? "加载中…" : "请输入 tenant_id 并点击聚合"}
        </div>
      )}
    </section>
  );
}
