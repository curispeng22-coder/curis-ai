"use client";

import { useCallback, useEffect, useState } from "react";

// ADR-0028 Phase-2 (issue 065)：用量投影标签页（复用 R-04 GET /api/platform/usage）。
// 纯计量读数，不含金额 / 货币 / ROI。tenant_id 缺失 fail-closed（后端拒绝跨租户聚合）。
export default function UsageProjectionPanel({ apiFetch, onMessage }) {
  const [tenantId, setTenantId] = useState("default");
  const [capabilitySource, setCapabilitySource] = useState("");
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (tenantId) params.set("tenant_id", tenantId);
      if (capabilitySource) params.set("capability_source", capabilitySource);
      const query = params.toString() ? `?${params.toString()}` : "";
      const next = await apiFetch(`/api/platform/usage${query}`);
      setEvents(next.usage_events || []);
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  }, [apiFetch, onMessage, tenantId, capabilitySource]);

  useEffect(() => {
    load().catch(() => null);
  }, [load]);

  return (
    <section className="admin-card">
      <h2 className="admin-card-title">用量投影</h2>
      <div className="admin-note-info mt-3">
        仅计量读数，不含金额 / ROI（纯 usage.* 事件投影）。
      </div>

      <div className="mt-4 flex flex-wrap items-end gap-4">
        <label className="admin-field">
          租户 ID
          <div>
            <input
              className="admin-input mono min-w-[16rem]"
              value={tenantId}
              placeholder="如 default"
              onChange={(e) => setTenantId(e.target.value)}
            />
          </div>
        </label>
        <label className="admin-field">
          能力来源
          <div>
            <select
              className="admin-input"
              value={capabilitySource}
              onChange={(e) => setCapabilitySource(e.target.value)}
            >
              <option value="">全部</option>
              <option value="official">官方</option>
              <option value="tenant_private">租户私有</option>
              <option value="marketplace">市场</option>
            </select>
          </div>
        </label>
        <button
          type="button"
          className="admin-btn admin-btn-primary h-10"
          onClick={load}
          disabled={loading}
        >
          查询用量
        </button>
      </div>

      {loading && events.length === 0 ? (
        <div className="admin-meta mt-4">加载中…</div>
      ) : (
        <div className="mt-4 overflow-x-auto">
          {events.length ? (
            <table className="admin-table">
              <thead>
                <tr>
                  <th>事件类型</th>
                  <th>作用域类型</th>
                  <th>数量</th>
                  <th>单位</th>
                  <th>能力引用</th>
                  <th>原始计量值</th>
                  <th>创建时间</th>
                </tr>
              </thead>
              <tbody>
                {events.map((event) => {
                  const payload = event.payload || {};
                  return (
                    <tr key={event.event_id}>
                      <td className="mono">{event.event_type}</td>
                      <td>{payload.scope_type ?? "—"}</td>
                      <td>{payload.quantity ?? "—"}</td>
                      <td>{payload.unit ?? "—"}</td>
                      <td className="mono">{payload.capability_ref ?? "—"}</td>
                      <td>{payload.raw_meter_value ?? "—"}</td>
                      <td className="muted">{event.created_at}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          ) : (
            <div className="admin-empty">该租户暂无用量事件</div>
          )}
        </div>
      )}
    </section>
  );
}
