"use client";

import { useCallback, useEffect, useState } from "react";

// AuditEvent 只读投影：Admin 在后台按时间范围/事件类型/租户查看所有
// capability.* / governance.* 审计事件。仅受控命名空间，不暴露 usage.* 等
// 未授权事件类型。复用 apiFetch + Bearer token 范式，不引入 MUI/状态库。
export default function AuditEventPanel({ apiFetch, onMessage }) {
  const [tenantId, setTenantId] = useState("");
  const [eventType, setEventType] = useState("");
  const [since, setSince] = useState("");
  const [limit, setLimit] = useState("100");
  const [events, setEvents] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (tenantId) params.set("tenant_id", tenantId);
      if (eventType) params.set("event_type", eventType);
      if (since) params.set("since", since);
      params.set("limit", limit || "100");
      const qs = params.toString();
      const next = await apiFetch(`/api/platform/audit?${qs}`);
      setEvents(next.audit_events || []);
      setTotal(next.total || 0);
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  }, [apiFetch, onMessage, tenantId, eventType, since, limit]);

  useEffect(() => {
    load().catch(() => null);
  }, [load]);

  const truncate = (str, maxLen = 120) => {
    if (!str) return "—";
    try {
      const obj = JSON.parse(str);
      const s = JSON.stringify(obj);
      return s.length > maxLen ? s.slice(0, maxLen) + "…" : s;
    } catch {
      return str.length > maxLen ? str.slice(0, maxLen) + "…" : str;
    }
  };

  return (
    <section className="admin-card">
      <h2 className="admin-card-title">审计轨迹</h2>
      <div className="admin-note mt-3">
        仅受控命名空间（capability.* / governance.*）审计记录，只读投影。
      </div>

      <div className="mt-4 flex flex-wrap items-end gap-4">
        <label className="admin-field">
          租户 ID
          <div>
            <input
              className="admin-input mono min-w-[12rem]"
              value={tenantId}
              placeholder="留空 = 全局"
              onChange={(e) => setTenantId(e.target.value)}
            />
          </div>
        </label>
        <label className="admin-field">
          事件类型
          <div>
            <select
              className="admin-input min-w-[12rem]"
              value={eventType}
              onChange={(e) => setEventType(e.target.value)}
            >
              <option value="">全部</option>
              <option value="capability.%">能力类事件</option>
              <option value="governance.%">治理类事件</option>
            </select>
          </div>
        </label>
        <label className="admin-field">
          起始时间
          <div>
            <input
              className="admin-input mono min-w-[12rem]"
              value={since}
              placeholder="ISO 8601，如 2026-01-01T00:00:00"
              onChange={(e) => setSince(e.target.value)}
            />
          </div>
        </label>
        <label className="admin-field">
          返回条数
          <div>
            <input
              className="admin-input mono w-20"
              type="number"
              min="1"
              max="1000"
              value={limit}
              onChange={(e) => setLimit(e.target.value)}
            />
          </div>
        </label>
        <button
          type="button"
          className="admin-btn admin-btn-primary h-10"
          onClick={load}
          disabled={loading}
        >
          查询
        </button>
      </div>

      {total > 0 ? (
        <div className="admin-meta mt-2">共 {total} 条记录</div>
      ) : null}

      {loading && events.length === 0 ? (
        <div className="admin-meta mt-3">加载中…</div>
      ) : (
        <div className="mt-4 overflow-x-auto">
          {events.length ? (
            <table className="admin-table">
              <thead>
                <tr>
                  <th>创建时间</th>
                  <th>事件类型</th>
                  <th>租户 ID</th>
                  <th>关联 ID</th>
                  <th>负载</th>
                </tr>
              </thead>
              <tbody>
                {events.map((event) => (
                  <tr key={event.event_id}>
                    <td className="muted nowrap">{event.created_at}</td>
                    <td className="mono">{event.event_type}</td>
                    <td className="mono">{event.tenant_id || "—"}</td>
                    <td className="mono muted">
                      {event.correlation_id || "—"}
                    </td>
                    <td className="mono breakall">
                      {truncate(event.payload)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="admin-empty">暂无审计事件</div>
          )}
        </div>
      )}
    </section>
  );
}
