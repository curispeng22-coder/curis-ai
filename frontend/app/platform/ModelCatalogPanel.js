"use client";

import { useCallback, useEffect, useState } from "react";

// ADR-0028 Phase-2 (issue 070/071): DEPRECATED — 已统一并入官能力目录。
// 本组件被 CapabilityCatalogPanel 替代，不再被 page.js 渲染（保留以便回滚）。
// 请勿在此处继续新增功能；新增能力录入请走 CapabilityCatalogPanel。
//
// ADR-0028 Phase-2 (issue 065): 官方模型目录标签页（Admin 写）。
// 模型列表含启用/停用开关（无物理删除）；新增表单含 gateway_ref 下拉与 auth_type 形状。
export default function ModelCatalogPanel({ apiFetch, onMessage }) {
  const [models, setModels] = useState([]);
  const [gateways, setGateways] = useState([]);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    model_key: "",
    provider_id: "",
    display_name: "",
    supported_models: "",
    auth_type: "apikey",
    gateway_ref: "newapi",
    default_model: "",
    status: "active",
  });

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [modelRes, gatewayRes] = await Promise.all([
        apiFetch("/api/platform/models?include_inactive=true"),
        apiFetch("/api/platform/gateways"),
      ]);
      setModels(modelRes.models || []);
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

  const createModel = async (event) => {
    event.preventDefault();
    setLoading(true);
    try {
      const supported = form.supported_models
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean);
      await apiFetch("/api/platform/models", {
        method: "POST",
        body: JSON.stringify({
          model_key: form.model_key,
          provider_id: form.provider_id,
          display_name: form.display_name,
          supported_models: supported,
          auth_type: form.auth_type,
          gateway_ref: form.gateway_ref,
          default_model: form.default_model,
          status: form.status,
        }),
      });
      onMessage(`模型 ${form.model_key} 已创建`);
      setForm({
        model_key: "",
        provider_id: "",
        display_name: "",
        supported_models: "",
        auth_type: "apikey",
        gateway_ref: "newapi",
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

  const toggleStatus = async (modelKey, enable) => {
    setLoading(true);
    try {
      await apiFetch(`/api/platform/models/${encodeURIComponent(modelKey)}`, {
        method: "PUT",
        body: JSON.stringify({ action: enable ? "enable" : "disable" }),
      });
      onMessage(`模型 ${modelKey} 已${enable ? "启用" : "停用"}`);
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
        <h2 className="text-sm font-black uppercase text-zinc-500">官方模型目录</h2>
        {loading && models.length === 0 ? (
          <div className="mt-3 text-sm font-bold text-zinc-400">加载中…</div>
        ) : (
          <div className="mt-3 space-y-2">
            {models.length ? (
              models.map((item) => (
                <article
                  key={item.model_key}
                  className="rounded-md border border-zinc-200 p-3"
                >
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div>
                      <div className="text-sm font-black">{item.display_name || item.model_key}</div>
                      <div className="text-xs text-zinc-500">
                        {item.model_key} · provider={item.provider_id} · gateway={item.gateway_ref} · auth={item.auth_type}
                      </div>
                    </div>
                    <span
                      className={`rounded-md px-2 py-1 text-xs font-bold ${
                        item.status === "active"
                          ? "bg-teal-50 text-teal-800"
                          : "bg-zinc-100 text-zinc-500"
                      }`}
                    >
                      {item.status === "active" ? "启用" : "停用"}
                    </span>
                  </div>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {item.status === "active" ? (
                      <button
                        type="button"
                        className="rounded-md border border-zinc-300 px-3 py-1.5 text-xs font-bold text-zinc-700"
                        onClick={() => toggleStatus(item.model_key, false)}
                      >
                        停用
                      </button>
                    ) : (
                      <button
                        type="button"
                        className="rounded-md bg-teal-700 px-3 py-1.5 text-xs font-bold text-white"
                        onClick={() => toggleStatus(item.model_key, true)}
                      >
                        启用
                      </button>
                    )}
                  </div>
                </article>
              ))
            ) : (
              <div className="rounded-md border border-dashed border-zinc-300 p-4 text-sm font-bold text-zinc-400">
                暂无模型
              </div>
            )}
          </div>
        )}
      </section>

      <section className="rounded-md border border-zinc-200 bg-white p-4 shadow-sm">
        <h2 className="text-sm font-black uppercase text-zinc-500">新增官方模型</h2>
        <form className="mt-3 grid gap-3" onSubmit={createModel}>
          <Field label="model_key">
            <input
              className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm font-mono"
              required
              value={form.model_key}
              onChange={(e) => setForm({ ...form, model_key: e.target.value })}
            />
          </Field>
          <Field label="provider_id">
            <input
              className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm"
              required
              value={form.provider_id}
              onChange={(e) => setForm({ ...form, provider_id: e.target.value })}
            />
          </Field>
          <Field label="display_name">
            <input
              className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm"
              required
              value={form.display_name}
              onChange={(e) => setForm({ ...form, display_name: e.target.value })}
            />
          </Field>
          <Field label="supported_models（逗号分隔）">
            <input
              className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm font-mono"
              placeholder="gpt-4o, gpt-4o-mini"
              value={form.supported_models}
              onChange={(e) => setForm({ ...form, supported_models: e.target.value })}
            />
          </Field>
          <Field label="auth_type（仅形状占位：none / oauth / apikey）">
            <select
              className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm"
              value={form.auth_type}
              onChange={(e) => setForm({ ...form, auth_type: e.target.value })}
            >
              <option value="none">none</option>
              <option value="oauth">oauth</option>
              <option value="apikey">apikey</option>
            </select>
          </Field>
          <Field label="gateway_ref（关联模型网关）">
            <select
              className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm"
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
          <Field label="default_model（仅元数据）">
            <input
              className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm"
              placeholder="如 gpt-4o"
              value={form.default_model}
              onChange={(e) => setForm({ ...form, default_model: e.target.value })}
            />
          </Field>
          <Field label="status">
            <select
              className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm"
              value={form.status}
              onChange={(e) => setForm({ ...form, status: e.target.value })}
            >
              <option value="active">active</option>
              <option value="inactive">inactive</option>
            </select>
          </Field>
          <button
            type="submit"
            className="h-10 rounded-md bg-zinc-950 px-4 text-sm font-bold text-white disabled:opacity-50"
            disabled={loading}
          >
            创建模型
          </button>
        </form>
      </section>
    </div>
  );
}

function Field({ label, children }) {
  return (
    <label className="block text-sm font-bold text-zinc-700">
      {label}
      <div className="mt-1">{children}</div>
    </label>
  );
}
