"use client";

import { useCallback, useEffect, useState } from "react";

// ADR-0028 Phase-2 (issue 070/071): 统一官方能力目录标签页（Admin 写）。
// 覆盖 model / tool / connector 三类能力：按 type 分组展示；统一新增表单
// （type 下拉、capability_key / name / provider_id / display_name、gateway_ref
// 仅 model 显示下拉自 /api/platform/gateways、auth_type 仅形状占位、status 默认
// active）；启用 / 停用开关（无物理删除）。Admin 绝不执行模型 / 工具 / 连接器调用。
const CAPABILITY_TYPES = ["model", "tool", "connector"];
const TYPE_LABELS = { model: "模型", tool: "工具", connector: "连接器" };

export default function CapabilityCatalogPanel({ apiFetch, onMessage }) {
  const [capabilities, setCapabilities] = useState([]);
  const [gateways, setGateways] = useState([]);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    capability_key: "",
    type: "model",
    name: "",
    provider_id: "",
    display_name: "",
    gateway_ref: "newapi",
    auth_type: "none",
    status: "active",
  });

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [capRes, gatewayRes] = await Promise.all([
        apiFetch("/api/platform/capabilities?include_inactive=true"),
        apiFetch("/api/platform/gateways"),
      ]);
      setCapabilities(capRes.capabilities || []);
      setGateways(gatewayRes.gateways || []);
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  }, [apiFetch, onMessage]);

  useEffect(() => {
    load().catch(() => null);
  }, [load]);

  const createCapability = async (event) => {
    event.preventDefault();
    setLoading(true);
    try {
      await apiFetch("/api/platform/capabilities", {
        method: "POST",
        body: JSON.stringify({
          capability_key: form.capability_key,
          type: form.type,
          name: form.name,
          provider_id: form.provider_id,
          display_name: form.display_name,
          gateway_ref: form.type === "model" ? form.gateway_ref : "",
          auth_type: form.auth_type,
          status: form.status,
        }),
      });
      onMessage(`能力 ${form.capability_key}（${form.type}）已创建`);
      setForm({
        capability_key: "",
        type: "model",
        name: "",
        provider_id: "",
        display_name: "",
        gateway_ref: "newapi",
        auth_type: "none",
        status: "active",
      });
      await load();
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  const toggleStatus = async (capabilityKey, enable) => {
    setLoading(true);
    try {
      await apiFetch(
        `/api/platform/capabilities/${encodeURIComponent(capabilityKey)}`,
        {
          method: "PUT",
          body: JSON.stringify({ action: enable ? "enable" : "disable" }),
        },
      );
      onMessage(`能力 ${capabilityKey} 已${enable ? "启用" : "停用"}`);
      await load();
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  const grouped = CAPABILITY_TYPES.map((type) => ({
    type,
    items: capabilities.filter((c) => c.type === type),
  }));

  return (
    <div className="grid gap-5 lg:grid-cols-[minmax(0,1fr)_420px]">
      <section className="admin-card">
        <h2 className="admin-card-title">官方能力目录</h2>
        <div className="admin-note mt-4">
          Admin 仅定义能力元数据，不执行模型 / 工具 / 连接器调用（绝不发起出站请求）。
        </div>
        {loading && capabilities.length === 0 ? (
          <div className="admin-meta mt-4">加载中…</div>
        ) : (
          <div className="mt-4 space-y-5">
            {grouped.map((group) => (
              <div key={group.type}>
                <div className="admin-meta flex items-center gap-2 font-bold">
                  <span>{TYPE_LABELS[group.type] || group.type}</span>
                  <span className="admin-count">{group.items.length}</span>
                </div>
                <div className="mt-3 space-y-2">
                  {group.items.length ? (
                    group.items.map((item) => (
                      <article key={item.capability_key} className="admin-item">
                        <div className="flex flex-wrap items-center justify-between gap-3">
                          <div>
                            <div className="text-sm font-bold">
                              {item.display_name || item.name || item.capability_key}
                            </div>
                            <div className="admin-meta mt-1">
                              {item.capability_key} · 提供方={item.provider_id || "—"} · 网关={item.gateway_ref || "—"} · 鉴权={item.auth_type}
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
                              onClick={() => toggleStatus(item.capability_key, false)}
                            >
                              停用
                            </button>
                          ) : (
                            <button
                              type="button"
                              className="admin-btn admin-btn-primary"
                              onClick={() => toggleStatus(item.capability_key, true)}
                            >
                              启用
                            </button>
                          )}
                        </div>
                      </article>
                    ))
                  ) : (
                    <div className="admin-empty">暂无 {TYPE_LABELS[group.type] || group.type} 能力</div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="admin-card">
        <h2 className="admin-card-title">新增官方能力</h2>
        <form className="mt-4 grid gap-4" onSubmit={createCapability}>
          <Field label="类型">
            <select
              className="admin-input"
              value={form.type}
              onChange={(e) => setForm({ ...form, type: e.target.value })}
            >
              <option value="model">模型</option>
              <option value="tool">工具</option>
              <option value="connector">连接器</option>
            </select>
          </Field>
          <Field label="能力键（全局唯一）">
            <input
              className="admin-input mono"
              required
              placeholder="如 gpt-4o / web_search / slack"
              value={form.capability_key}
              onChange={(e) => setForm({ ...form, capability_key: e.target.value })}
            />
          </Field>
          <Field label="名称">
            <input
              className="admin-input"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
            />
          </Field>
          <Field label="提供方 ID">
            <input
              className="admin-input"
              placeholder="openai / internal / slack"
              value={form.provider_id}
              onChange={(e) => setForm({ ...form, provider_id: e.target.value })}
            />
          </Field>
          <Field label="展示名称">
            <input
              className="admin-input"
              required
              value={form.display_name}
              onChange={(e) => setForm({ ...form, display_name: e.target.value })}
            />
          </Field>
          {form.type === "model" ? (
            <Field label="关联网关（仅模型）">
              <select
                className="admin-input"
                value={form.gateway_ref}
                onChange={(e) => setForm({ ...form, gateway_ref: e.target.value })}
              >
                {gateways.length ? (
                  gateways.map((g) => (
                    <option key={g.gateway_id} value={g.gateway_id}>
                      {g.gateway_id}（{g.name || g.gateway_id}）
                    </option>
                  ))
                ) : (
                  <option value="newapi">newapi（默认）</option>
                )}
              </select>
            </Field>
          ) : null}
          <Field label="鉴权类型">
            <select
              className="admin-input"
              value={form.auth_type}
              onChange={(e) => setForm({ ...form, auth_type: e.target.value })}
            >
              <option value="none">无</option>
              <option value="oauth">OAuth 授权</option>
              <option value="apikey">API 密钥</option>
            </select>
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
            创建能力
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
