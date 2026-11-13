"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import GatewayPanel from "./GatewayPanel";
// ADR-0028 Phase-2 (issue 070/071): ModelCatalogPanel 已被统一官方能力目录
// 替代，保留不渲染以便回滚；新标签页使用 CapabilityCatalogPanel。
import ModelCatalogPanel from "./ModelCatalogPanel";
import CapabilityCatalogPanel from "./CapabilityCatalogPanel";
import AuditEventPanel from "./AuditEventPanel";
import UsageProjectionPanel from "./UsageProjectionPanel";
import TalentProductionPanel from "./TalentProductionPanel";

// 平台级管理后台（ADR-0017 S4 D4.platform, issue 060）。
// UI 解禁（总控决策席 gate 书面确认）：仅平台级管理后台必要 UI。
// 仅调用 /api/platform/*（须管理员令牌鉴权）。
const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";

const DEFAULT_ADMIN_TOKEN = "platform-admin-dev";

const DEFAULT_MANIFEST = JSON.stringify(
  {
    capability_set: [],
    tool_classes: [],
    quality_lines: [],
    output_channels: [],
    roi_schema: {},
    guardrail_refs: [],
    employee_role_spec: {},
  },
  null,
  2,
);

// v1 自用合法面板（L2 冻结类已剥离：多租户 / 计费 / 配额 / 商业运营相关面板
// 不在此列，不渲染、不引用）。
const TABS = [
  { id: "types", label: "部门类型目录" },
  { id: "policies", label: "跨公司策略 / 全局护栏" },
  { id: "gateways", label: "模型网关" },
  { id: "capabilities", label: "官方能力目录" },
  { id: "usage", label: "用量投影" },
  { id: "audit", label: "审计轨迹" },
  { id: "talent", label: "人才生产线" },
];

export default function PlatformConsole() {
  const [token, setToken] = useState(DEFAULT_ADMIN_TOKEN);
  const [tab, setTab] = useState("types");
  const [message, setMessage] = useState("");

  const apiFetch = async (path, options = {}) => {
    const headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      ...(options.headers || {}),
    };
    const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
    if (response.status === 401) {
      throw new Error("鉴权失败：管理员令牌无效（请在顶部填写正确令牌）");
    }
    const payload = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(payload.detail || `请求失败：${path}`);
    }
    return payload;
  };

  return (
    <main className="admin-shell px-6 py-8">
      <section className="mx-auto max-w-6xl">
        <header className="pb-5" style={{ borderBottom: "1px solid var(--admin-line)" }}>
          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold" style={{ margin: 0 }}>
                Curis 平台管理后台
              </h1>
              <p className="admin-meta mt-1" style={{ fontSize: "var(--admin-font-sm)" }}>
                部门类型 / 策略 · 网关 / 能力目录 · 用量投影 / 审计轨迹
              </p>
            </div>
            <Link
              href="/"
              className="admin-header-link"
              style={{ marginTop: 6 }}
            >
              ← 返回工作台
            </Link>
          </div>
        </header>

        <div className="admin-toolbar mt-5">
          <span className="admin-toolbar-label">管理员令牌</span>
          <div className="relative flex-1 min-w-[16rem]" style={{ position: "relative" }}>
            <input
              id="admin-token"
              className="admin-input mono"
              style={{ paddingRight: 32 }}
              value={token}
              onChange={(event) => setToken(event.target.value)}
            />
            <span
              style={{
                position: "absolute", right: 10, top: "50%", transform: "translateY(-50%)",
                color: "var(--admin-faint)", fontSize: 14, pointerEvents: "none",
              }}
              title="令牌用于 API 鉴权"
            >
              🔑
            </span>
          </div>
        </div>

        {message ? (
          <div className="admin-message mt-4" style={{ border: "1px solid var(--admin-active-soft)", background: "var(--admin-active-soft)", color: "var(--admin-active)" }}>
            {message}
          </div>
        ) : null}

        <nav className="mt-6 flex gap-1" style={{ borderBottom: "1px solid var(--admin-line)", paddingBottom: 0 }}>
          {TABS.map((item) => {
            const active = item.id === tab;
            return (
              <button
                key={item.id}
                type="button"
                className={active ? "admin-tab admin-tab-active" : "admin-tab"}
                onClick={() => setTab(item.id)}
              >
                {item.label}
              </button>
            );
          })}
        </nav>

        <div className="mt-5">
          {tab === "types" ? (
            <DepartmentTypesPanel apiFetch={apiFetch} onMessage={setMessage} />
          ) : null}
          {tab === "policies" ? (
            <PoliciesPanel apiFetch={apiFetch} onMessage={setMessage} />
          ) : null}
          {tab === "gateways" ? (
            <GatewayPanel apiFetch={apiFetch} onMessage={setMessage} />
          ) : null}
          {tab === "capabilities" ? (
            <CapabilityCatalogPanel apiFetch={apiFetch} onMessage={setMessage} />
          ) : null}
          {tab === "usage" ? (
            <UsageProjectionPanel apiFetch={apiFetch} onMessage={setMessage} />
          ) : null}
          {tab === "audit" ? (
            <AuditEventPanel apiFetch={apiFetch} onMessage={setMessage} />
          ) : null}
          {tab === "talent" ? (
            <TalentProductionPanel apiFetch={apiFetch} onMessage={setMessage} />
          ) : null}
        </div>
      </section>
    </main>
  );
}

function DepartmentTypesPanel({ apiFetch, onMessage }) {
  const [types, setTypes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    type_key: "",
    category: "custom",
    display_name: "",
    description: "",
    manifest: DEFAULT_MANIFEST,
    approved_by: "",
  });

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const next = await apiFetch("/api/platform/department-types");
      setTypes(next);
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  }, [apiFetch, onMessage]);

  useEffect(() => {
    load().catch(() => null);
  }, [load]);

  const createType = async (event) => {
    event.preventDefault();
    setLoading(true);
    try {
      let manifest;
      try {
        manifest = JSON.parse(form.manifest);
      } catch {
        throw new Error("manifest 不是合法 JSON");
      }
      await apiFetch("/api/platform/department-types", {
        method: "POST",
        body: JSON.stringify({
          type_key: form.type_key,
          category: form.category,
          display_name: form.display_name,
          description: form.description,
          manifest,
          approved_by: form.approved_by,
        }),
      });
      onMessage(`部门类型 ${form.type_key} 已创建（需人工审批已提供）`);
      setForm({
        type_key: "",
        category: "custom",
        display_name: "",
        description: "",
        manifest: DEFAULT_MANIFEST,
        approved_by: "",
      });
      await load();
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  const toggleEnabled = async (typeKey, enable) => {
    setLoading(true);
    try {
      await apiFetch(`/api/platform/department-types/${encodeURIComponent(typeKey)}`, {
        method: "PUT",
        body: JSON.stringify({ action: enable ? "enable" : "disable" }),
      });
      onMessage(`部门类型 ${typeKey} 已${enable ? "启用" : "停用"}`);
      await load();
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  const removeType = async (typeKey) => {
    const approvedBy = window.prompt(
      `移除部门类型 ${typeKey} 须经人工审批门控。请输入审批人身份：`,
    );
    if (approvedBy === null) return;
    setLoading(true);
    try {
      await apiFetch(`/api/platform/department-types/${encodeURIComponent(typeKey)}`, {
        method: "DELETE",
        body: JSON.stringify({ approved_by: approvedBy }),
      });
      onMessage(`部门类型 ${typeKey} 已移除`);
      await load();
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_360px]">
      <section className="admin-card">
        <h2 className="admin-card-title">部门类型目录</h2>
        {loading && types.length === 0 ? (
          <div className="admin-meta mt-4">加载中…</div>
        ) : (
          <div className="mt-4 space-y-3">
            {types.length ? (
              types.map((item) => (
                <article key={item.type_key} className="admin-item">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div>
                      <div className="text-sm font-bold">{item.display_name || item.type_key}</div>
                      <div className="admin-meta mt-1">
                        {item.type_key} · {item.category}
                      </div>
                    </div>
                    <span
                      className={`admin-badge ${
                        item.enabled ? "admin-badge-active" : "admin-badge-muted"
                      }`}
                    >
                      {item.enabled ? "启用" : "停用"}
                    </span>
                  </div>
                  {item.description ? (
                    <div className="admin-meta mt-2">{item.description}</div>
                  ) : null}
                  <div className="mt-3 flex flex-wrap gap-2">
                    {item.enabled ? (
                      <button
                        type="button"
                        className="admin-btn"
                        onClick={() => toggleEnabled(item.type_key, false)}
                      >
                        停用
                      </button>
                    ) : (
                      <button
                        type="button"
                        className="admin-btn admin-btn-primary"
                        onClick={() => toggleEnabled(item.type_key, true)}
                      >
                        启用
                      </button>
                    )}
                    <button
                      type="button"
                      className="admin-btn admin-btn-danger"
                      onClick={() => removeType(item.type_key)}
                    >
                      移除
                    </button>
                  </div>
                </article>
              ))
            ) : (
              <div className="admin-empty">暂无部门类型</div>
            )}
          </div>
        )}
      </section>

      <section className="admin-card">
        <h2 className="admin-card-title">新增部门类型</h2>
        <form className="mt-4 grid gap-4" onSubmit={createType}>
          <Field label="类型键">
            <input
              className="admin-input"
              required
              value={form.type_key}
              onChange={(e) => setForm({ ...form, type_key: e.target.value })}
            />
          </Field>
          <Field label="分类">
            <input
              className="admin-input"
              value={form.category}
              onChange={(e) => setForm({ ...form, category: e.target.value })}
            />
          </Field>
          <Field label="展示名称">
            <input
              className="admin-input"
              value={form.display_name}
              onChange={(e) => setForm({ ...form, display_name: e.target.value })}
            />
          </Field>
          <Field label="描述">
            <input
              className="admin-input"
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
            />
          </Field>
          <Field label="清单（JSON，7 键契约）">
            <textarea
              className="admin-input mono min-h-40"
              value={form.manifest}
              onChange={(e) => setForm({ ...form, manifest: e.target.value })}
            />
          </Field>
          <Field label="审批人（人工批准门控）">
            <input
              className="admin-input"
              placeholder="须提供人工批准者身份"
              value={form.approved_by}
              onChange={(e) => setForm({ ...form, approved_by: e.target.value })}
            />
          </Field>
          <button
            type="submit"
            className="admin-btn admin-btn-primary h-10"
            disabled={loading}
          >
            创建类型
          </button>
        </form>
      </section>
    </div>
  );
}

function PoliciesPanel({ apiFetch, onMessage }) {
  const [policies, setPolicies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    policy_key: "",
    value: "{}",
    tenant_scope: "all",
  });

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const next = await apiFetch("/api/platform/policies");
      setPolicies(next);
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  }, [apiFetch, onMessage]);

  useEffect(() => {
    load().catch(() => null);
  }, [load]);

  const setPolicy = async (event) => {
    event.preventDefault();
    setLoading(true);
    try {
      let value;
      try {
        value = JSON.parse(form.value);
      } catch {
        throw new Error("value 不是合法 JSON");
      }
      await apiFetch("/api/platform/policies", {
        method: "POST",
        body: JSON.stringify({
          policy_key: form.policy_key,
          value,
          tenant_scope: form.tenant_scope,
        }),
      });
      onMessage(`策略 ${form.policy_key} 已设置（作用域=${form.tenant_scope}）`);
      setForm({ policy_key: "", value: "{}", tenant_scope: "all" });
      await load();
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  const togglePolicy = async (policyKey, enable) => {
    setLoading(true);
    try {
      await apiFetch(`/api/platform/policies`, {
        method: "POST",
        body: JSON.stringify({
          policy_key: policyKey,
          action: enable ? "enable" : "disable",
        }),
      });
      onMessage(`策略 ${policyKey} 已${enable ? "启用" : "停用"}`);
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
        <h2 className="admin-card-title">跨公司策略 / 全局护栏</h2>
        {loading && policies.length === 0 ? (
          <div className="admin-meta mt-4">加载中…</div>
        ) : (
          <div className="mt-4 space-y-3">
            {policies.length ? (
              policies.map((item) => (
                <article key={item.policy_key} className="admin-item">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div>
                      <div className="text-sm font-bold">{item.policy_key}</div>
                      <div className="admin-meta mt-1">作用域 = {item.tenant_scope}</div>
                    </div>
                    <span
                      className={`admin-badge ${
                        item.enabled ? "admin-badge-active" : "admin-badge-muted"
                      }`}
                    >
                      {item.enabled ? "启用" : "停用"}
                    </span>
                  </div>
                  <pre className="admin-pre mt-2 max-h-40">{item.policy_value}</pre>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {item.enabled ? (
                      <button
                        type="button"
                        className="admin-btn"
                        onClick={() => togglePolicy(item.policy_key, false)}
                      >
                        停用
                      </button>
                    ) : (
                      <button
                        type="button"
                        className="admin-btn admin-btn-primary"
                        onClick={() => togglePolicy(item.policy_key, true)}
                      >
                        启用
                      </button>
                    )}
                  </div>
                </article>
              ))
            ) : (
              <div className="admin-empty">暂无策略</div>
            )}
          </div>
        )}
      </section>

      <section className="admin-card">
        <h2 className="admin-card-title">设置策略</h2>
        <form className="mt-4 grid gap-4" onSubmit={setPolicy}>
          <Field label="策略键">
            <input
              className="admin-input"
              required
              value={form.policy_key}
              onChange={(e) => setForm({ ...form, policy_key: e.target.value })}
            />
          </Field>
          <Field label="策略值（JSON）">
            <textarea
              className="admin-input mono min-h-28"
              value={form.value}
              onChange={(e) => setForm({ ...form, value: e.target.value })}
            />
          </Field>
          <Field label="作用域（all = 全局）">
            <input
              className="admin-input"
              value={form.tenant_scope}
              onChange={(e) => setForm({ ...form, tenant_scope: e.target.value })}
            />
          </Field>
          <button
            type="submit"
            className="admin-btn admin-btn-primary h-10"
            disabled={loading}
          >
            设置策略
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
