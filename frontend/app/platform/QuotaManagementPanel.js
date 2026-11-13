"use client";

import { useCallback, useEffect, useState } from "react";

// Phase-8 Billing MVP (issue P8) · P8-2 Quota 配置 + 实时计数面板。
// 为租户配置 token / employee_seat / capability / workflow 的 limit_value + period；
// current_usage 由读时聚合派生（源：usage_event / employee_instances / workflow_runs）。
// 仅计量不阻断；employee_seat / workflow 来自 Phase-4/6 数据源，标注「Admin 只读观测」。

const QUOTA_TYPES = ["token", "employee_seat", "capability", "workflow"];
const PERIODS = ["monthly", "annual", "custom"];
// 这些 quota_type 的 current_usage 来自 Phase-4/6 数据源，Admin 仅观测、不干预。
const READONLY_OBSERVATION = {
  employee_seat: "Admin 只读观测（源自 employee_instances，权威计量待 Phase-4）",
  workflow: "Admin 只读观测（源自 workflow_runs，权威计量待 Phase-6）",
};
const STATUS_COLORS = {
  active: "bg-teal-50 text-teal-800",
  exceeded: "bg-amber-50 text-amber-800",
  paused: "bg-zinc-100 text-zinc-500",
};

const EMPTY_FORM = {
  tenant_id: "default",
  plan_id: "plan_free",
  quota_type: "token",
  limit_value: 0,
  period: "monthly",
  period_start: "",
  period_end: "",
  source_scope: "",
};

function Field({ label, children }) {
  return (
    <label className="block text-sm font-bold text-zinc-700">
      {label}
      <div className="mt-1">{children}</div>
    </label>
  );
}

export default function QuotaManagementPanel({ apiFetch, onMessage }) {
  const [form, setForm] = useState({ ...EMPTY_FORM });
  const [viewTenantId, setViewTenantId] = useState("default");
  const [quotas, setQuotas] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadQuotas = useCallback(async () => {
    if (!viewTenantId) return;
    setLoading(true);
    try {
      const next = await apiFetch(
        `/api/platform/quotas/${encodeURIComponent(viewTenantId)}`,
      );
      setQuotas(next.quotas || []);
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  }, [apiFetch, onMessage, viewTenantId]);

  useEffect(() => {
    loadQuotas().catch(() => null);
  }, [loadQuotas]);

  const upsert = async (event) => {
    event.preventDefault();
    setLoading(true);
    try {
      const body = {
        tenant_id: form.tenant_id,
        plan_id: form.plan_id,
        quota_type: form.quota_type,
        limit_value: Number(form.limit_value) || 0,
        period: form.period,
        period_start: form.period_start,
        period_end: form.period_end,
        source_scope: form.source_scope
          ? form.source_scope.split(",").map((s) => s.trim()).filter(Boolean)
          : [],
      };
      await apiFetch("/api/platform/quotas", {
        method: "POST",
        body: JSON.stringify(body),
      });
      onMessage(`租户 ${form.tenant_id} 的 ${form.quota_type} 配额已配置`);
      setViewTenantId(form.tenant_id);
      await loadQuotas();
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_380px]">
      <section className="rounded-md border border-zinc-200 bg-white p-4 shadow-sm">
        <h2 className="text-sm font-black uppercase text-zinc-500">租户配额（current_usage 读时聚合）</h2>
        <div className="mt-3 flex flex-wrap items-end gap-3">
          <Field label="查看 tenant_id">
            <input
              className="min-w-[16rem] rounded-md border border-zinc-300 px-3 py-2 text-sm font-mono"
              value={viewTenantId}
              onChange={(e) => setViewTenantId(e.target.value)}
            />
          </Field>
          <button
            type="button"
            className="h-10 rounded-md bg-zinc-950 px-4 text-sm font-bold text-white"
            onClick={loadQuotas}
          >
            查询
          </button>
        </div>
        {READONLY_OBSERVATION[form.quota_type] ? (
          <div className="mt-3 rounded-md border border-sky-200 bg-sky-50 p-2 text-xs font-bold text-sky-800">
            {READONLY_OBSERVATION[form.quota_type]}
          </div>
        ) : null}
        {loading && quotas.length === 0 ? (
          <div className="mt-3 text-sm font-bold text-zinc-400">加载中…</div>
        ) : (
          <div className="mt-3 overflow-x-auto">
            <table className="w-full border-collapse text-sm">
              <thead>
                <tr className="border-b border-zinc-200 text-left text-xs text-zinc-500">
                  <th className="py-2 pr-3">quota_type</th>
                  <th className="py-2 pr-3">limit</th>
                  <th className="py-2 pr-3">current_usage</th>
                  <th className="py-2 pr-3">period</th>
                  <th className="py-2 pr-3">status</th>
                </tr>
              </thead>
              <tbody>
                {quotas.length ? (
                  quotas.map((q) => (
                    <tr key={q.quota_id} className="border-b border-zinc-100">
                      <td className="py-2 pr-3 font-mono text-xs">{q.quota_type}</td>
                      <td className="py-2 pr-3 font-mono text-xs">{q.limit_value}</td>
                      <td className="py-2 pr-3 font-mono text-xs">
                        {q.current_usage}
                        {READONLY_OBSERVATION[q.quota_type] ? (
                          <span className="ml-1 text-ui-1 text-sky-600">观测</span>
                        ) : null}
                      </td>
                      <td className="py-2 pr-3 font-mono text-xs">{q.period}</td>
                      <td className="py-2 pr-3">
                        <span
                          className={`rounded-md px-2 py-1 text-xs font-bold ${
                            STATUS_COLORS[q.status] || "bg-zinc-100 text-zinc-500"
                          }`}
                        >
                          {q.status}
                        </span>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={5} className="py-4 text-center font-bold text-zinc-400">
                      该租户暂无配额实例（可在右侧配置）
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="rounded-md border border-zinc-200 bg-white p-4 shadow-sm">
        <h2 className="text-sm font-black uppercase text-zinc-500">配置 / 派生配额</h2>
        <form className="mt-3 grid gap-3" onSubmit={upsert}>
          <Field label="tenant_id">
            <input
              className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm font-mono"
              required
              value={form.tenant_id}
              onChange={(e) => setForm({ ...form, tenant_id: e.target.value })}
            />
          </Field>
          <Field label="plan_id（配额实例按 plan 派生）">
            <input
              className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm font-mono"
              required
              value={form.plan_id}
              onChange={(e) => setForm({ ...form, plan_id: e.target.value })}
            />
          </Field>
          <div className="grid grid-cols-2 gap-3">
            <Field label="quota_type">
              <select
                className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm"
                value={form.quota_type}
                onChange={(e) => setForm({ ...form, quota_type: e.target.value })}
              >
                {QUOTA_TYPES.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
            </Field>
            <Field label="limit_value（0=不限）">
              <input
                type="number"
                className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm font-mono"
                value={form.limit_value}
                onChange={(e) => setForm({ ...form, limit_value: e.target.value })}
              />
            </Field>
          </div>
          <Field label="period">
            <select
              className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm"
              value={form.period}
              onChange={(e) => setForm({ ...form, period: e.target.value })}
            >
              {PERIODS.map((p) => (
                <option key={p} value={p}>
                  {p}
                </option>
              ))}
            </select>
          </Field>
          <div className="grid grid-cols-2 gap-3">
            <Field label="period_start">
              <input
                className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm font-mono"
                value={form.period_start}
                placeholder="可选"
                onChange={(e) => setForm({ ...form, period_start: e.target.value })}
              />
            </Field>
            <Field label="period_end">
              <input
                className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm font-mono"
                value={form.period_end}
                placeholder="可选"
                onChange={(e) => setForm({ ...form, period_end: e.target.value })}
              />
            </Field>
          </div>
          <Field label="source_scope（capability 白名单，逗号分隔）">
            <input
              className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm font-mono"
              value={form.source_scope}
              placeholder="如 official,marketplace"
              onChange={(e) => setForm({ ...form, source_scope: e.target.value })}
            />
          </Field>
          <button
            type="submit"
            className="h-10 rounded-md bg-zinc-950 px-4 text-sm font-bold text-white disabled:opacity-50"
            disabled={loading}
          >
            保存配额
          </button>
        </form>
      </section>
    </div>
  );
}
