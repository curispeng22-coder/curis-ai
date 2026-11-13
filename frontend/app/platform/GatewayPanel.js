"use client";

import { useCallback, useEffect, useState } from "react";

// ADR-0028 Phase-2 (issue 065): 模型网关标签页（Admin 写）。
// 仅定义网关元数据：credential_ref 是外部密钥托管引用占位（scheme:reference），
// 不含任何 token / key 明文控件；Admin 绝不发起出站调用。
export default function GatewayPanel({ apiFetch, onMessage }) {
  const [gateways, setGateways] = useState([]);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    gateway_id: "",
    name: "",
    type: "newapi",
    base_url: "",
    credential_ref: "",
    default_model: "",
    status: "active",
  });

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const next = await apiFetch("/api/platform/gateways");
      setGateways(next.gateways || []);
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  }, [apiFetch, onMessage]);

  useEffect(() => {
    load().catch(() => null);
  }, [load]);

  const createGateway = async (event) => {
    event.preventDefault();
    setLoading(true);
    try {
      await apiFetch("/api/platform/gateways", {
        method: "POST",
        body: JSON.stringify(form),
      });
      onMessage(`网关 ${form.gateway_id} 已创建`);
      setForm({
        gateway_id: "",
        name: "",
        type: "newapi",
        base_url: "",
        credential_ref: "",
        default_model: "",
        status: "active",
      });
      await load();
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  const toggleStatus = async (gatewayId, enable) => {
    setLoading(true);
    try {
      await apiFetch(`/api/platform/gateways/${encodeURIComponent(gatewayId)}`, {
        method: "PUT",
        body: JSON.stringify({ action: enable ? "enable" : "disable" }),
      });
      onMessage(`网关 ${gatewayId} 已${enable ? "启用" : "停用"}`);
      await load();
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid gap-5 lg:grid-cols-[minmax(0,1fr)_380px]">
      <section className="admin-card">
        <h2 className="admin-card-title">模型网关</h2>
        <div className="admin-note mt-4">
          Admin 仅定义网关元数据，不执行模型调用（绝不向 New API 发起出站请求）。
        </div>
        {loading && gateways.length === 0 ? (
          <div className="admin-meta mt-4">加载中…</div>
        ) : (
          <div className="mt-4 space-y-3">
            {gateways.length ? (
              gateways.map((item) => (
                <article key={item.gateway_id} className="admin-item">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div>
                      <div className="text-sm font-bold">{item.name || item.gateway_id}</div>
                      <div className="admin-meta mt-1">
                        {item.gateway_id} · {item.type} · {item.base_url || "（未配置）"}
                      </div>
                    </div>
                    <span
                      className={`admin-badge ${
                        item.status === "active" ? "admin-badge-active" : "admin-badge-muted"
                      }`}
                    >
                      {item.status === "active" ? "启用" : "停用"}
                    </span>
                  </div>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {item.status === "active" ? (
                      <button
                        type="button"
                        className="admin-btn"
                        onClick={() => toggleStatus(item.gateway_id, false)}
                      >
                        停用
                      </button>
                    ) : (
                      <button
                        type="button"
                        className="admin-btn admin-btn-primary"
                        onClick={() => toggleStatus(item.gateway_id, true)}
                      >
                        启用
                      </button>
                    )}
                  </div>
                </article>
              ))
            ) : (
              <div className="admin-empty">暂无网关配置</div>
            )}
          </div>
        )}
      </section>

      <section className="admin-card">
        <h2 className="admin-card-title">新增网关</h2>
        <form className="mt-4 grid gap-4" onSubmit={createGateway}>
          <Field label="网关 ID">
            <input
              className="admin-input"
              required
              value={form.gateway_id}
              onChange={(e) => setForm({ ...form, gateway_id: e.target.value })}
            />
          </Field>
          <Field label="名称">
            <input
              className="admin-input"
              required
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
            />
          </Field>
          <Field label="类型（仅 newapi）">
            <input
              className="admin-input mono"
              value={form.type}
              onChange={(e) => setForm({ ...form, type: e.target.value })}
            />
          </Field>
          <Field label="网关基础地址（非凭证）">
            <input
              className="admin-input mono"
              placeholder="https://your-gateway.example.com"
              value={form.base_url}
              onChange={(e) => setForm({ ...form, base_url: e.target.value })}
            />
          </Field>
          <Field label="密钥引用（待审批门控）">
            <input
              className="admin-input mono"
              placeholder="env:CURIS_MODEL_GATEWAY_API_KEY"
              value={form.credential_ref}
              onChange={(e) => setForm({ ...form, credential_ref: e.target.value })}
            />
            <p className="admin-field-hint">
              仅存不透明引用串（scheme:reference），绝不持久化密钥值。
            </p>
          </Field>
          <Field label="默认模型（仅元数据）">
            <input
              className="admin-input"
              placeholder="如 gpt-4o"
              value={form.default_model}
              onChange={(e) => setForm({ ...form, default_model: e.target.value })}
            />
          </Field>
          <Field label="状态">
            <select
              className="admin-input"
              value={form.status}
              onChange={(e) => setForm({ ...form, status: e.target.value })}
            >
              <option value="active">启用</option>
              <option value="inactive">停用</option>
            </select>
          </Field>
          <button
            type="submit"
            className="admin-btn admin-btn-primary h-10"
            disabled={loading}
          >
            创建网关
          </button>
        </form>
      </section>
    </div>
  );
}

function Field({ label, children }) {
  return (
    <label className="admin-field">
      {label}
      <div>{children}</div>
    </label>
  );
}
