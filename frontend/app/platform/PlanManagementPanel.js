"use client";

import { useCallback, useEffect, useState } from "react";

// Phase-8 Billing MVP (issue P8) · P8-1 Plan 管理面板。
// 创建 / 查看 / 修改 / 启用·停用 Free / Pro / Enterprise。
// 仅调用 /api/platform/plans*（须管理员令牌）。不实现任何支付 / 扣费 / 折扣字段。

const TIERS = ["free", "pro", "enterprise"];
const STATUSES = ["draft", "active", "deprecated", "archived"];
const INTERVALS = ["monthly", "annual", "custom"];
const STATUS_COLORS = {
  active: "bg-teal-50 text-teal-800",
  draft: "bg-zinc-100 text-zinc-500",
  deprecated: "bg-amber-50 text-amber-800",
  archived: "bg-zinc-200 text-zinc-600",
};

const EMPTY_FORM = {
  plan_code: "",
  name: "",
  tier: "free",
  status: "draft",
  billing_interval: "monthly",
  features: "[]",
  quota_rules: "{}",
};

function Field({ label, children }) {
  return (
    <label className="block text-sm font-bold text-zinc-700">
      {label}
      <div className="mt-1">{children}</div>
    </label>
  );
}

export default function PlanManagementPanel({ apiFetch, onMessage }) {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [form, setForm] = useState({ ...EMPTY_FORM });

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const next = await apiFetch("/api/platform/plans");
      setPlans(next.plans || []);
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  }, [apiFetch, onMessage]);

  useEffect(() => {
    load().catch(() => null);
  }, [load]);

  const startCreate = () => {
    setEditingId(null);
    setForm({ ...EMPTY_FORM });
  };

  const startEdit = (plan) => {
    setEditingId(plan.plan_id);
    setForm({
      plan_code: plan.plan_code,
      name: plan.name,
      tier: plan.tier,
      status: plan.status,
      billing_interval: plan.billing_interval,
      features: JSON.stringify(plan.features || [], null, 2),
      quota_rules: JSON.stringify(plan.quota_rules || {}, null, 2),
    });
  };

  const submit = async (event) => {
    event.preventDefault();
    setLoading(true);
    try {
      let features;
      let quotaRules;
      try {
        features = JSON.parse(form.features);
        quotaRules = JSON.parse(form.quota_rules);
      } catch {
        throw new Error("features / quota_rules 必须是合法 JSON");
      }
      const body = {
        plan_code: form.plan_code,
        name: form.name,
        tier: form.tier,
        status: form.status,
        billing_interval: form.billing_interval,
        features,
        quota_rules: quotaRules,
      };
      if (editingId) {
        await apiFetch(`/api/platform/plans/${encodeURIComponent(editingId)}`, {
          method: "PUT",
          body: JSON.stringify(body),
        });
        onMessage(`Plan ${editingId} 已更新`);
      } else {
        await apiFetch("/api/platform/plans", {
          method: "POST",
          body: JSON.stringify(body),
        });
        onMessage(`Plan ${form.plan_code} 已创建`);
      }
      setEditingId(null);
      setForm({ ...EMPTY_FORM });
      await load();
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  const toggle = async (plan, enable) => {
    setLoading(true);
    try {
      await apiFetch(`/api/platform/plans/${encodeURIComponent(plan.plan_id)}/toggle`, {
        method: "POST",
        body: JSON.stringify({ action: enable ? "enable" : "disable" }),
      });
      onMessage(`Plan ${plan.plan_code} 已${enable ? "启用" : "停用"}`);
      await load();
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_380px]">
      <section className="rounded-md border border-zinc-200 bg-white p-4 shadow-sm">
        <h2 className="text-sm font-black uppercase text-zinc-500">Plan 列表</h2>
        {loading && plans.length === 0 ? (
          <div className="mt-3 text-sm font-bold text-zinc-400">加载中…</div>
        ) : (
          <div className="mt-3 space-y-2">
            {plans.length ? (
              plans.map((plan) => (
                <article key={plan.plan_id} className="rounded-md border border-zinc-200 p-3">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div>
                      <div className="text-sm font-black">
                        {plan.name}{" "}
                        <span className="font-mono text-xs text-zinc-400">{plan.plan_code}</span>
                      </div>
                      <div className="text-xs text-zinc-500">
                        {plan.tier} · {plan.billing_interval} · v{plan.version}
                      </div>
                    </div>
                    <span
                      className={`rounded-md px-2 py-1 text-xs font-bold ${
                        STATUS_COLORS[plan.status] || "bg-zinc-100 text-zinc-500"
                      }`}
                    >
                      {plan.status}
                    </span>
                  </div>
                  {plan.quota_rules ? (
                    <pre className="mt-2 max-h-32 overflow-auto rounded-md bg-zinc-50 p-2 text-ui-1 text-zinc-600">
                      {JSON.stringify(plan.quota_rules, null, 2)}
                    </pre>
                  ) : null}
                  <div className="mt-3 flex flex-wrap gap-2">
                    <button
                      type="button"
                      className="rounded-md border border-zinc-300 px-3 py-1.5 text-xs font-bold text-zinc-700"
                      onClick={() => startEdit(plan)}
                    >
                      编辑
                    </button>
                    {plan.status === "active" ? (
                      <button
                        type="button"
                        className="rounded-md border border-amber-300 px-3 py-1.5 text-xs font-bold text-amber-700"
                        onClick={() => toggle(plan, false)}
                      >
                        停用
                      </button>
                    ) : (
                      <button
                        type="button"
                        className="rounded-md bg-teal-700 px-3 py-1.5 text-xs font-bold text-white"
                        onClick={() => toggle(plan, true)}
                      >
                        启用
                      </button>
                    )}
                  </div>
                </article>
              ))
            ) : (
              <div className="rounded-md border border-dashed border-zinc-300 p-4 text-sm font-bold text-zinc-400">
                暂无 Plan
              </div>
            )}
          </div>
        )}
      </section>

      <section className="rounded-md border border-zinc-200 bg-white p-4 shadow-sm">
        <h2 className="text-sm font-black uppercase text-zinc-500">
          {editingId ? "编辑 Plan" : "新增 Plan"}
        </h2>
        <form className="mt-3 grid gap-3" onSubmit={submit}>
          <Field label="plan_code（与 plan_tier 1:1）">
            <input
              className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm font-mono"
              required
              disabled={!!editingId}
              value={form.plan_code}
              onChange={(e) => setForm({ ...form, plan_code: e.target.value })}
            />
          </Field>
          <Field label="name">
            <input
              className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm"
              required
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
            />
          </Field>
          <div className="grid grid-cols-3 gap-3">
            <Field label="tier">
              <select
                className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm"
                value={form.tier}
                onChange={(e) => setForm({ ...form, tier: e.target.value })}
              >
                {TIERS.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
            </Field>
            <Field label="status">
              <select
                className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm"
                value={form.status}
                onChange={(e) => setForm({ ...form, status: e.target.value })}
              >
                {STATUSES.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
            </Field>
            <Field label="billing_interval">
              <select
                className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm"
                value={form.billing_interval}
                onChange={(e) => setForm({ ...form, billing_interval: e.target.value })}
              >
                {INTERVALS.map((i) => (
                  <option key={i} value={i}>
                    {i}
                  </option>
                ))}
              </select>
            </Field>
          </div>
          <Field label="features (JSON 数组)">
            <textarea
              className="min-h-20 w-full rounded-md border border-zinc-300 px-3 py-2 font-mono text-xs"
              value={form.features}
              onChange={(e) => setForm({ ...form, features: e.target.value })}
            />
          </Field>
          <Field label="quota_rules (JSON 对象，含 limit + overage 单价)">
            <textarea
              className="min-h-28 w-full rounded-md border border-zinc-300 px-3 py-2 font-mono text-xs"
              value={form.quota_rules}
              onChange={(e) => setForm({ ...form, quota_rules: e.target.value })}
            />
          </Field>
          <div className="flex flex-wrap gap-2">
            <button
              type="submit"
              className="h-10 flex-1 rounded-md bg-zinc-950 px-4 text-sm font-bold text-white disabled:opacity-50"
              disabled={loading}
            >
              {editingId ? "保存修改" : "创建 Plan"}
            </button>
            {editingId ? (
              <button
                type="button"
                className="h-10 rounded-md border border-zinc-300 px-4 text-sm font-bold text-zinc-700"
                onClick={startCreate}
              >
                取消
              </button>
            ) : null}
          </div>
        </form>
      </section>
    </div>
  );
}
