"use client";

import { useCallback, useEffect, useState } from "react";

// Phase-8 Billing MVP (issue P8) · P8-4 Billing Event 查询 + calculate 面板。
// 展示状态机 draft → calculated → issued（issued 仅占位、无资金动作）。
// amount 为非权威估算（usage_event × quota_rules.overage），绝不触发支付 / 发票 / 扣款。

const STATUS_COLORS = {
  draft: "bg-zinc-100 text-zinc-500",
  calculated: "bg-sky-50 text-sky-800",
  issued: "bg-teal-50 text-teal-800",
};
const STATUS_FLOW = ["draft", "calculated", "issued"];

function Field({ label, children }) {
  return (
    <label className="block text-sm font-bold text-zinc-700">
      {label}
      <div className="mt-1">{children}</div>
    </label>
  );
}

function StatusBadge({ status }) {
  return (
    <span
      className={`rounded-md px-2 py-1 text-xs font-bold ${
        STATUS_COLORS[status] || "bg-zinc-100 text-zinc-500"
      }`}
    >
      {status}
    </span>
  );
}

export default function BillingEventPanel({ apiFetch, onMessage }) {
  const [tenantId, setTenantId] = useState("default");
  const [status, setStatus] = useState("");
  const [periodStart, setPeriodStart] = useState("");
  const [periodEnd, setPeriodEnd] = useState("");
  const [asCalculated, setAsCalculated] = useState(true);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (tenantId) params.set("tenant_id", tenantId);
      if (status) params.set("status", status);
      const next = await apiFetch(`/api/platform/billing-events?${params.toString()}`);
      setEvents(next.billing_events || []);
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  }, [apiFetch, onMessage, tenantId, status]);

  useEffect(() => {
    load().catch(() => null);
  }, [load]);

  const calculate = async (event) => {
    event.preventDefault();
    setLoading(true);
    try {
      const body = {
        tenant_id: tenantId,
        period_start: periodStart,
        period_end: periodEnd,
        as_calculated: asCalculated,
      };
      const next = await apiFetch("/api/platform/billing-events/calculate", {
        method: "POST",
        body: JSON.stringify(body),
      });
      const created = next.billing_events || [];
      onMessage(`已生成 ${created.length} 条 billing_event（状态=${created[0]?.status || "n/a"}）`);
      await load();
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_360px]">
      <section className="rounded-md border border-zinc-200 bg-white p-4 shadow-sm">
        <h2 className="text-sm font-black uppercase text-zinc-500">Billing Event 列表</h2>
        <div className="mt-3 flex flex-wrap items-end gap-3">
          <Field label="tenant_id">
            <input
              className="min-w-[16rem] rounded-md border border-zinc-300 px-3 py-2 text-sm font-mono"
              value={tenantId}
              onChange={(e) => setTenantId(e.target.value)}
            />
          </Field>
          <Field label="status 过滤">
            <select
              className="rounded-md border border-zinc-300 px-3 py-2 text-sm"
              value={status}
              onChange={(e) => setStatus(e.target.value)}
            >
              <option value="">全部</option>
              {STATUS_FLOW.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </Field>
          <button
            type="button"
            className="h-10 rounded-md bg-zinc-950 px-4 text-sm font-bold text-white"
            onClick={load}
          >
            查询
          </button>
        </div>

        <div className="mt-3 rounded-md border border-amber-200 bg-amber-50 p-2 text-xs font-bold text-amber-800">
          状态机：{STATUS_FLOW.join(" → ")}。issued 仅占位，无支付 / 发票 / 扣款副作用。
          amount 为非权威估算（usage × overage 单价）。
        </div>

        {loading && events.length === 0 ? (
          <div className="mt-3 text-sm font-bold text-zinc-400">加载中…</div>
        ) : (
          <div className="mt-3 overflow-x-auto">
            <table className="w-full border-collapse text-sm">
              <thead>
                <tr className="border-b border-zinc-200 text-left text-xs text-zinc-500">
                  <th className="py-2 pr-3">subject_type</th>
                  <th className="py-2 pr-3">subject_id</th>
                  <th className="py-2 pr-3">amount</th>
                  <th className="py-2 pr-3">currency</th>
                  <th className="py-2 pr-3">status</th>
                </tr>
              </thead>
              <tbody>
                {events.length ? (
                  events.map((ev) => (
                    <tr key={ev.billing_event_id} className="border-b border-zinc-100">
                      <td className="py-2 pr-3 font-mono text-xs">{ev.subject_type}</td>
                      <td className="py-2 pr-3 font-mono text-xs">{ev.subject_id}</td>
                      <td className="py-2 pr-3 font-mono text-xs">{ev.amount}</td>
                      <td className="py-2 pr-3 font-mono text-xs">{ev.currency}</td>
                      <td className="py-2 pr-3">
                        <StatusBadge status={ev.status} />
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={5} className="py-4 text-center font-bold text-zinc-400">
                      暂无 billing_event（可在右侧 calculate）
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="rounded-md border border-zinc-200 bg-white p-4 shadow-sm">
        <h2 className="text-sm font-black uppercase text-zinc-500">Calculate Billing Event</h2>
        <form className="mt-3 grid gap-3" onSubmit={calculate}>
          <Field label="tenant_id">
            <input
              className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm font-mono"
              required
              value={tenantId}
              onChange={(e) => setTenantId(e.target.value)}
            />
          </Field>
          <div className="grid grid-cols-2 gap-3">
            <Field label="period_start">
              <input
                className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm font-mono"
                value={periodStart}
                placeholder="如 2025-01-01"
                onChange={(e) => setPeriodStart(e.target.value)}
              />
            </Field>
            <Field label="period_end">
              <input
                className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm font-mono"
                value={periodEnd}
                placeholder="如 2025-01-31"
                onChange={(e) => setPeriodEnd(e.target.value)}
              />
            </Field>
          </div>
          <label className="flex items-center gap-2 text-sm font-bold text-zinc-700">
            <input
              type="checkbox"
              checked={asCalculated}
              onChange={(e) => setAsCalculated(e.target.checked)}
            />
            as_calculated（true→calculated，false→draft）
          </label>
          <button
            type="submit"
            className="h-10 rounded-md bg-zinc-950 px-4 text-sm font-bold text-white disabled:opacity-50"
            disabled={loading}
          >
            计算并生成
          </button>
        </form>
      </section>
    </div>
  );
}
