"use client";

// DEPRECATED: 商业运营面板，L2 冻结，v1 自用不渲染

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { buildConsoleOverview, FORBIDDEN_ZONES } from "./commercialConsole.mjs";

/**
 * Commercial Operation Console 只读聚合面板（Phase-9A Console MVP）。
 *
 * 红线：仅 GET /api/platform/*，绝不 mutation（POST/PUT/DELETE），绝不 fetch /api/workspace/*。
 * props 与既有 Panel 一致：{ apiFetch, onMessage }。
 */
export default function CommercialConsolePanel({ apiFetch, onMessage }) {
  const [overview, setOverview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [tenantId, setTenantId] = useState("");

  const loadAll = useCallback(async () => {
    setLoading(true);
    try {
      const results = await Promise.allSettled([
        apiFetch("/api/platform/plans"),
        apiFetch("/api/platform/pricing-rules"),
        apiFetch("/api/platform/quota-rules"),
        apiFetch("/api/platform/capability-packages"),
        apiFetch(
          `/api/platform/usage/summary${
            tenantId ? `?tenant_id=${encodeURIComponent(tenantId)}` : ""
          }`,
        ),
      ]);
      const [plansR, pricingR, quotaR, capR, usageR] = results;
      const plans = plansR.status === "fulfilled" ? plansR.value : null;
      const pricingRules = pricingR.status === "fulfilled" ? pricingR.value : null;
      const quotaRules = quotaR.status === "fulfilled" ? quotaR.value : null;
      const capabilityPackages = capR.status === "fulfilled" ? capR.value : null;
      const usageSummary = usageR.status === "fulfilled" ? usageR.value : null;
      const next = buildConsoleOverview({
        plans,
        pricingRules,
        quotaRules,
        capabilityPackages,
        usageSummary,
        tenantId:
          tenantId || (usageR.status === "fulfilled" ? usageR.value?.tenant_id : null),
      });
      setOverview(next);
      const failed = results.filter((r) => r.status === "rejected").length;
      if (failed) {
        onMessage(`部分聚合失败（${failed} 项），其余已展示`);
      }
    } catch (e) {
      onMessage(e.message);
    } finally {
      setLoading(false);
    }
  }, [apiFetch, onMessage, tenantId]);

  useEffect(() => {
    loadAll().catch(() => null);
  }, [loadAll]);

  return (
    <div className="space-y-5">
      <header className="rounded-md border border-zinc-200 bg-white p-4 shadow-sm">
        <h2 className="text-lg font-black text-zinc-900">
          Commercial Operation Console（商业运营控制中心 · 只读聚合）
        </h2>
        <p className="mt-1 text-xs text-zinc-500">
          仅 GET /api/platform/*，绝不 mutation，绝不触碰 /api/workspace/*。本控制台聚合 Plan /
          Pricing / Quota / CapabilityPackage / EmployeeSeatPolicy（design-only）/ Usage 只读观测。
        </p>
        <div className="mt-3 flex flex-wrap items-end gap-3">
          <label className="text-xs font-bold text-zinc-500" htmlFor="cc-tenant">
            tenant_id（可选）
          </label>
          <input
            id="cc-tenant"
            className="min-w-[16rem] flex-1 rounded-md border border-zinc-300 px-3 py-2 text-sm"
            placeholder="留空则获取平台级聚合"
            value={tenantId}
            onChange={(event) => setTenantId(event.target.value)}
          />
          <button
            type="button"
            className="h-9 rounded-md bg-zinc-950 px-4 text-sm font-bold text-white disabled:opacity-50"
            onClick={() => loadAll().catch(() => null)}
            disabled={loading}
          >
            聚合
          </button>
        </div>
      </header>

      {loading ? (
        <div className="rounded-md border border-dashed border-zinc-300 bg-white p-6 text-sm font-bold text-zinc-400">
          加载中…
        </div>
      ) : overview === null ? (
        <div className="rounded-md border border-dashed border-zinc-300 bg-white p-6 text-sm font-bold text-zinc-400">
          尚未加载聚合数据。
        </div>
      ) : (
        <>
          <SectionCard title="Plans 套餐" hint={`${overview.plans.length} 项`}>
            {overview.plans.length ? (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="text-zinc-500">
                    <tr>
                      <th className="px-2 py-1">plan_id</th>
                      <th className="px-2 py-1">name</th>
                      <th className="px-2 py-1">tier</th>
                      <th className="px-2 py-1">status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {overview.plans.map((p) => (
                      <tr key={p.plan_id} className="border-t border-zinc-100">
                        <td className="px-2 py-1 font-mono">{p.plan_id}</td>
                        <td className="px-2 py-1 font-bold">{p.name}</td>
                        <td className="px-2 py-1">{p.tier}</td>
                        <td className="px-2 py-1">
                          <StatusBadge status={p.status} />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="text-xs text-zinc-400">暂无 Plan 数据</div>
            )}
          </SectionCard>

          <SectionCard title="Pricing Rules 定价规则" hint={`${overview.pricingRules.length} 项`}>
            {overview.pricingRules.length ? (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="text-zinc-500">
                    <tr>
                      <th className="px-2 py-1">subject_type</th>
                      <th className="px-2 py-1">pricing_type</th>
                      <th className="px-2 py-1">amount</th>
                      <th className="px-2 py-1">currency</th>
                      <th className="px-2 py-1">billing_cycle</th>
                      <th className="px-2 py-1">status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {overview.pricingRules.map((r, i) => (
                      <tr key={i} className="border-t border-zinc-100">
                        <td className="px-2 py-1 font-mono">{r.subject_type}</td>
                        <td className="px-2 py-1">{r.pricing_type}</td>
                        <td className="px-2 py-1">{String(r.amount)}</td>
                        <td className="px-2 py-1">{r.currency}</td>
                        <td className="px-2 py-1">{r.billing_cycle}</td>
                        <td className="px-2 py-1">
                          <StatusBadge status={r.status} />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="text-xs text-zinc-400">暂无 PricingRule 数据</div>
            )}
          </SectionCard>

          <SectionCard title="Quota Rules 配额规则" hint={`${overview.quotaRules.length} 项`}>
            {overview.quotaRules.length ? (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="text-zinc-500">
                    <tr>
                      <th className="px-2 py-1">quota_type</th>
                      <th className="px-2 py-1">limit_value</th>
                      <th className="px-2 py-1">period</th>
                      <th className="px-2 py-1">enforcement_mode</th>
                      <th className="px-2 py-1">status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {overview.quotaRules.map((q, i) => (
                      <tr key={i} className="border-t border-zinc-100">
                        <td className="px-2 py-1 font-mono">{q.quota_type}</td>
                        <td className="px-2 py-1">{String(q.limit_value)}</td>
                        <td className="px-2 py-1">{q.period}</td>
                        <td className="px-2 py-1">{q.enforcement_mode}</td>
                        <td className="px-2 py-1">
                          <StatusBadge status={q.status} />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="text-xs text-zinc-400">暂无 QuotaRule 数据</div>
            )}
          </SectionCard>

          <SectionCard
            title="Capability Packages 能力包"
            hint={`${overview.capabilityPackages.length} 项`}
          >
            {overview.capabilityPackages.length ? (
              <div className="space-y-2">
                {overview.capabilityPackages.map((pkg) => (
                  <article key={pkg.package_id} className="rounded-md border border-zinc-200 p-3">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <div>
                        <div className="text-sm font-black">{pkg.name}</div>
                        <div className="text-xs text-zinc-500">{pkg.package_id}</div>
                      </div>
                      <StatusBadge status={pkg.status} />
                    </div>
                    <div className="mt-2 grid gap-2 sm:grid-cols-2">
                      <IncludedList label="Capabilities" items={pkg.includedCapabilities} />
                      <IncludedList label="Connectors" items={pkg.includedConnectors} />
                      <IncludedList label="Workflows" items={pkg.includedWorkflows} />
                      <IncludedList label="Employee Templates" items={pkg.includedEmployeeTemplates} />
                    </div>
                  </article>
                ))}
              </div>
            ) : (
              <div className="text-xs text-zinc-400">暂无 CapabilityPackage 数据</div>
            )}
          </SectionCard>

          <SectionCard title="Employee Seat Policy 员工席位策略" hint="design-only">
            {(() => {
              const policy = overview.employeeSeatPolicy;
              return (
                <div className="space-y-3">
                  <span className="inline-block rounded-md bg-amber-50 px-2 py-1 text-xs font-bold text-amber-800">
                    design-only · 尚未落地 API
                  </span>
                  <div className="grid gap-3 sm:grid-cols-2">
                    <div>
                      <div className="text-xs font-bold text-zinc-500">Employee Types（3）</div>
                      <ul className="mt-1 space-y-1">
                        {policy.employeeTypes.map((e) => (
                          <li key={e.value} className="text-sm">
                            {e.label}{" "}
                            <span className="text-xs text-zinc-400">({e.value})</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <div className="text-xs font-bold text-zinc-500">Seat Types（4）</div>
                      <ul className="mt-1 space-y-1">
                        {policy.seatTypes.map((s) => (
                          <li key={s.value} className="text-sm">
                            {s.label}{" "}
                            <span className="text-xs text-zinc-400">
                              ({s.value}, quotaCost={String(s.quotaCost)})
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                  <div>
                    <div className="text-xs font-bold text-zinc-500">statusEnum</div>
                    <div className="mt-1 flex flex-wrap gap-1">
                      {policy.statusEnum.map((s) => (
                        <span
                          key={s}
                          className="rounded bg-zinc-100 px-2 py-0.5 text-xs font-mono text-zinc-600"
                        >
                          {s}
                        </span>
                      ))}
                    </div>
                  </div>
                  <p className="text-xs text-zinc-600">{policy.quotaCostNote}</p>
                  <p className="text-xs text-zinc-600">{policy.note}</p>
                </div>
              );
            })()}
          </SectionCard>

          <SectionCard title="Usage Meter 用量计量（只读六维）">
            {(() => {
              const d = overview.usageMeter.dimensions;
              return (
                <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                  <MeterCard title="Tenant" available={d.tenant.available} note={d.tenant.note}>
                    id: {d.tenant.id ?? "-"}
                  </MeterCard>
                  <MeterCard
                    title="Employee"
                    available={d.employee.available}
                    note={d.employee.note}
                  >
                    {d.employee.byEmployee.length} 条
                  </MeterCard>
                  <MeterCard
                    title="Workflow"
                    available={d.workflow.available}
                    note={d.workflow.note}
                  >
                    {d.workflow.byWorkflow.length} 条
                  </MeterCard>
                  <MeterCard
                    title="Capability"
                    available={d.capability.available}
                    note={d.capability.note}
                  >
                    source {d.capability.byCapabilitySource.length} / type{" "}
                    {d.capability.byCapabilityType.length}
                  </MeterCard>
                  <MeterCard
                    title="Connector"
                    available={d.connector.available}
                    placeholder={d.connector.placeholder}
                    note={d.connector.note}
                  >
                    占位（未接入）
                  </MeterCard>
                  <MeterCard title="Token" available={d.token.available} note={d.token.note}>
                    <div className="mt-1 space-y-0.5 text-xs">
                      <div>events: {d.token.usageEventCount}</div>
                      <div>prompt: {d.token.promptTokens}</div>
                      <div>completion: {d.token.completionTokens}</div>
                      <div>total: {d.token.totalTokens}</div>
                      <div>est. cost: {d.token.estimatedCost}</div>
                    </div>
                  </MeterCard>
                </div>
              );
            })()}
          </SectionCard>

          <SectionCard title="禁止区 · Forbidden Zones（本阶段锁定）">
            <div className="flex flex-wrap gap-2">
              {overview.forbiddenZones.map((z) => (
                <div
                  key={z.id}
                  className="flex items-center gap-2 rounded-md border border-red-300 px-3 py-2 text-sm font-bold text-red-700"
                >
                  <span>🔒</span>
                  <span>{z.label}</span>
                  <span className="text-xs">本阶段锁定（LOCKED）</span>
                </div>
              ))}
            </div>
          </SectionCard>

          <SectionCard title="Admin / Workspace 边界（职责隔离 · 路由锁定）">
            <div className="grid gap-3 sm:grid-cols-2">
              <div className="rounded-md border border-zinc-200 p-3">
                <div className="text-xs font-black uppercase text-zinc-600">Admin（本控制台）</div>
                <p className="mt-1 text-xs text-zinc-600">{overview.boundary.admin.owns}</p>
                <div className="mt-2 flex flex-wrap gap-1">
                  {overview.boundary.admin.apis.map((a) => (
                    <span
                      key={a}
                      className="rounded bg-teal-50 px-2 py-0.5 text-xs font-mono text-teal-800"
                    >
                      {a}
                    </span>
                  ))}
                </div>
              </div>
              <div className="rounded-md border border-red-300 p-3">
                <div className="text-xs font-black uppercase text-red-700">
                  Workspace（禁止触碰）
                </div>
                <p className="mt-1 text-xs text-zinc-600">{overview.boundary.workspace.owns}</p>
                <div className="mt-2 flex flex-wrap gap-1">
                  {overview.boundary.workspace.apis.map((a) => (
                    <span
                      key={a}
                      className="rounded bg-red-50 px-2 py-0.5 text-xs font-mono text-red-700"
                    >
                      {a}
                    </span>
                  ))}
                </div>
              </div>
            </div>
            <p className="mt-3 text-xs text-zinc-500">{overview.boundary.note}</p>
            <p className="mt-1 text-xs font-bold text-red-700">
              {overview.boundary.workspaceRoutesBlocked
                ? "Workspace 路由已锁定（workspaceRoutesBlocked）"
                : "Workspace 路由未锁定"}
            </p>
          </SectionCard>

          <SectionCard title="配置面托管入口">
            <div className="flex flex-wrap gap-2">
              <Link
                href="/platform"
                className="rounded-md border border-zinc-300 px-3 py-2 text-xs font-bold text-zinc-700"
              >
                Plan 管理 → /platform
              </Link>
              <span className="rounded-md border border-zinc-200 px-3 py-2 text-xs font-bold text-zinc-500">
                PricingRule / QuotaRule / CapabilityPackage → 在 /platform 对应 TAB
              </span>
              <span className="rounded-md border border-amber-300 px-3 py-2 text-xs font-bold text-amber-800">
                EmployeeSeatPolicy（design-only，禁用跳转）
              </span>
            </div>
          </SectionCard>
        </>
      )}
    </div>
  );
}

/** 状态徽标：active 用 teal-50 激活态，其余用 zinc 灰阶。 */
function StatusBadge({ status }) {
  const active = status === "active";
  return (
    <span
      className={`rounded-md px-2 py-1 text-xs font-bold ${
        active ? "bg-teal-50 text-teal-800" : "bg-zinc-100 text-zinc-500"
      }`}
    >
      {status ?? "-"}
    </span>
  );
}

/** 卡片容器。 */
function SectionCard({ title, hint, children }) {
  return (
    <section className="rounded-md border border-zinc-200 bg-white p-4 shadow-sm">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h3 className="text-sm font-black uppercase text-zinc-500">{title}</h3>
        {hint ? <span className="text-xs text-zinc-400">{hint}</span> : null}
      </div>
      <div className="mt-3">{children}</div>
    </section>
  );
}

/** 能力包四类 included 列表渲染。 */
function IncludedList({ label, items }) {
  return (
    <div className="rounded-md bg-zinc-50 p-2">
      <div className="text-xs font-bold text-zinc-500">{label}</div>
      {items.length ? (
        <ul className="mt-1 flex flex-wrap gap-1">
          {items.map((it, i) => (
            <li
              key={i}
              className="rounded bg-zinc-200 px-2 py-0.5 text-xs font-mono text-zinc-700"
            >
              {String(it)}
            </li>
          ))}
        </ul>
      ) : (
        <div className="mt-1 text-xs text-zinc-400">无</div>
      )}
    </div>
  );
}

/** 计量维度卡片：available 显示 teal 态，placeholder 显示 red 态。 */
function MeterCard({ title, available, placeholder, note, children }) {
  return (
    <div
      className={`rounded-md border p-3 ${
        available ? "border-zinc-200 bg-white" : "border-dashed border-red-300 bg-red-50/30"
      }`}
    >
      <div className="flex items-center justify-between">
        <span className="text-xs font-black uppercase text-zinc-600">{title}</span>
        {available ? (
          <span className="rounded bg-teal-50 px-1.5 py-0.5 text-ui-1 font-bold text-teal-800">
            available
          </span>
        ) : (
          <span className="rounded bg-red-100 px-1.5 py-0.5 text-ui-1 font-bold text-red-700">
            placeholder
          </span>
        )}
      </div>
      <div className="mt-2 text-sm">{children}</div>
      {note ? <div className="mt-2 text-ui-1 text-zinc-400">{note}</div> : null}
    </div>
  );
}
