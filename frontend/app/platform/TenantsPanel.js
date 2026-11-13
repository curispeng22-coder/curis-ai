"use client";

import { useCallback, useEffect, useState } from "react";

const STATUS_OPTIONS = ["active", "inactive", "suspended"];
const STATUS_LABELS = { active: "活跃", inactive: "停用", suspended: "暂停" };
const STATUS_COLORS = {
  active: "bg-teal-50 text-teal-800",
  inactive: "bg-zinc-100 text-zinc-500",
  suspended: "bg-amber-50 text-amber-800",
};

const EMPTY_FORM = {
  tenant_id: "",
  name: "",
  plan_tier: "free",
  contact_email: "",
  description: "",
};

export default function TenantsPanel({ apiFetch, onMessage }) {
  const [tenants, setTenants] = useState([]);
  const [loading, setLoading] = useState(false);
  const [createForm, setCreateForm] = useState({ ...EMPTY_FORM });
  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState({});

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const data = await apiFetch("/api/platform/tenants");
      setTenants(data.tenants || []);
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  }, [apiFetch, onMessage]);

  useEffect(() => {
    load().catch(() => null);
  }, [load]);

  const handleCreate = async (event) => {
    event.preventDefault();
    if (!createForm.tenant_id.trim() || !createForm.name.trim()) {
      onMessage("tenant_id 和 name 为必填项");
      return;
    }
    setLoading(true);
    try {
      await apiFetch("/api/platform/tenants", {
        method: "POST",
        body: JSON.stringify(createForm),
      });
      onMessage(`租户 ${createForm.tenant_id} 已创建`);
      setCreateForm({ ...EMPTY_FORM });
      await load();
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  const startEdit = (item) => {
    setEditingId(item.tenant_id);
    setEditForm({
      name: item.name || "",
      plan_tier: item.plan_tier || "free",
      contact_email: item.contact_email || "",
      description: item.description || "",
    });
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditForm({});
  };

  const handleEdit = async (tenantId) => {
    setLoading(true);
    try {
      const payload = {};
      if (editForm.name !== undefined) payload.name = editForm.name;
      if (editForm.plan_tier !== undefined) payload.plan_tier = editForm.plan_tier;
      if (editForm.contact_email !== undefined) payload.contact_email = editForm.contact_email;
      if (editForm.description !== undefined) payload.description = editForm.description;
      await apiFetch(`/api/platform/tenants/${encodeURIComponent(tenantId)}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      });
      onMessage(`租户 ${tenantId} 已更新`);
      setEditingId(null);
      setEditForm({});
      await load();
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = async (tenantId, newStatus) => {
    setLoading(true);
    try {
      await apiFetch(`/api/platform/tenants/${encodeURIComponent(tenantId)}`, {
        method: "PUT",
        body: JSON.stringify({ status: newStatus }),
      });
      onMessage(`租户 ${tenantId} 状态已切换为 ${STATUS_LABELS[newStatus]}`);
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
        <h2 className="text-sm font-black uppercase text-zinc-500">
          租户列表（{tenants.length}）
        </h2>
        {loading && tenants.length === 0 ? (
          <div className="mt-3 text-sm font-bold text-zinc-400">加载中…</div>
        ) : (
          <div className="mt-3 space-y-2">
            {tenants.length ? (
              tenants.map((item) => (
                <article
                  key={item.tenant_id}
                  className="rounded-md border border-zinc-200 p-3"
                >
                  {editingId === item.tenant_id ? (
                    /* ── 编辑态 ── */
                    <div className="grid gap-2">
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-black text-zinc-700">
                          {item.tenant_id}
                        </span>
                      </div>
                      <div className="grid grid-cols-2 gap-2">
                        <label className="text-xs font-bold text-zinc-500">
                          名称
                          <input
                            className="mt-1 w-full rounded-md border border-zinc-300 px-2 py-1.5 text-xs"
                            value={editForm.name}
                            onChange={(e) =>
                              setEditForm({ ...editForm, name: e.target.value })
                            }
                          />
                        </label>
                        <label className="text-xs font-bold text-zinc-500">
                          plan_tier
                          <input
                            className="mt-1 w-full rounded-md border border-zinc-300 px-2 py-1.5 text-xs"
                            value={editForm.plan_tier}
                            onChange={(e) =>
                              setEditForm({ ...editForm, plan_tier: e.target.value })
                            }
                          />
                        </label>
                      </div>
                      <label className="text-xs font-bold text-zinc-500">
                        联系邮箱
                        <input
                          className="mt-1 w-full rounded-md border border-zinc-300 px-2 py-1.5 text-xs"
                          value={editForm.contact_email}
                          onChange={(e) =>
                            setEditForm({ ...editForm, contact_email: e.target.value })
                          }
                        />
                      </label>
                      <label className="text-xs font-bold text-zinc-500">
                        描述
                        <textarea
                          className="mt-1 w-full rounded-md border border-zinc-300 px-2 py-1.5 text-xs"
                          rows={2}
                          value={editForm.description}
                          onChange={(e) =>
                            setEditForm({ ...editForm, description: e.target.value })
                          }
                        />
                      </label>
                      <div className="flex gap-2">
                        <button
                          type="button"
                          className="rounded-md bg-zinc-950 px-3 py-1.5 text-xs font-bold text-white"
                          onClick={() => handleEdit(item.tenant_id)}
                        >
                          保存
                        </button>
                        <button
                          type="button"
                          className="rounded-md border border-zinc-300 px-3 py-1.5 text-xs font-bold text-zinc-700"
                          onClick={cancelEdit}
                        >
                          取消
                        </button>
                      </div>
                    </div>
                  ) : (
                    /* ── 展示态 ── */
                    <>
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <div>
                          <div className="text-sm font-black">
                            {item.tenant_id}
                          </div>
                          <div className="text-xs text-zinc-500">{item.name}</div>
                        </div>
                        <div className="flex items-center gap-2">
                          <span
                            className={`rounded-md px-2 py-1 text-xs font-bold ${
                              STATUS_COLORS[item.status] || "bg-zinc-100 text-zinc-500"
                            }`}
                          >
                            {STATUS_LABELS[item.status] || item.status}
                          </span>
                          <select
                            className="rounded-md border border-zinc-300 px-2 py-1 text-xs font-bold"
                            value={item.status}
                            onChange={(e) =>
                              handleStatusChange(item.tenant_id, e.target.value)
                            }
                          >
                            {STATUS_OPTIONS.map((s) => (
                              <option key={s} value={s}>
                                {STATUS_LABELS[s]}
                              </option>
                            ))}
                          </select>
                        </div>
                      </div>
                      <div className="mt-2 grid grid-cols-2 gap-1 text-xs text-zinc-500">
                        <div>
                          <span className="font-bold">等级：</span>
                          {item.plan_tier || "free"}
                        </div>
                        <div>
                          <span className="font-bold">邮箱：</span>
                          {item.contact_email || "—"}
                        </div>
                      </div>
                      {item.description ? (
                        <div className="mt-1 text-xs text-zinc-600">
                          {item.description}
                        </div>
                      ) : null}
                      <div className="mt-2">
                        <button
                          type="button"
                          className="rounded-md border border-zinc-300 px-3 py-1 text-xs font-bold text-zinc-700"
                          onClick={() => startEdit(item)}
                        >
                          编辑
                        </button>
                      </div>
                    </>
                  )}
                </article>
              ))
            ) : (
              <div className="rounded-md border border-dashed border-zinc-300 p-4 text-sm font-bold text-zinc-400">
                暂无租户
              </div>
            )}
          </div>
        )}
      </section>

      <section className="rounded-md border border-zinc-200 bg-white p-4 shadow-sm">
        <h2 className="text-sm font-black uppercase text-zinc-500">新增租户</h2>
        <form className="mt-3 grid gap-3" onSubmit={handleCreate}>
          <label className="block text-sm font-bold text-zinc-700">
            tenant_id
            <input
              className="mt-1 w-full rounded-md border border-zinc-300 px-3 py-2 text-sm"
              required
              value={createForm.tenant_id}
              onChange={(e) =>
                setCreateForm({ ...createForm, tenant_id: e.target.value })
              }
            />
          </label>
          <label className="block text-sm font-bold text-zinc-700">
            名称
            <input
              className="mt-1 w-full rounded-md border border-zinc-300 px-3 py-2 text-sm"
              required
              value={createForm.name}
              onChange={(e) =>
                setCreateForm({ ...createForm, name: e.target.value })
              }
            />
          </label>
          <label className="block text-sm font-bold text-zinc-700">
            plan_tier
            <input
              className="mt-1 w-full rounded-md border border-zinc-300 px-3 py-2 text-sm"
              value={createForm.plan_tier}
              onChange={(e) =>
                setCreateForm({ ...createForm, plan_tier: e.target.value })
              }
            />
          </label>
          <label className="block text-sm font-bold text-zinc-700">
            联系邮箱
            <input
              className="mt-1 w-full rounded-md border border-zinc-300 px-3 py-2 text-sm"
              value={createForm.contact_email}
              onChange={(e) =>
                setCreateForm({ ...createForm, contact_email: e.target.value })
              }
            />
          </label>
          <label className="block text-sm font-bold text-zinc-700">
            描述
            <textarea
              className="mt-1 w-full rounded-md border border-zinc-300 px-3 py-2 text-sm"
              rows={3}
              value={createForm.description}
              onChange={(e) =>
                setCreateForm({ ...createForm, description: e.target.value })
              }
            />
          </label>
          <button
            type="submit"
            className="h-10 rounded-md bg-zinc-950 px-4 text-sm font-bold text-white disabled:opacity-50"
            disabled={loading}
          >
            创建租户
          </button>
        </form>
      </section>
    </div>
  );
}
