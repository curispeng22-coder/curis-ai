"use client";

import { useEffect, useState } from "react";
import {
  TerraButton,
  TerraDrawer,
  TerraInput,
} from "../../../components/terra/TerraPrimitives.js";
import { createCompany, updateCompany } from "../../../lib/api.js";

const EMPTY = { name: "", description: "", status: "active" };

export default function CompanyFormDrawer({ open, company, onClose, onSuccess }) {
  const [form, setForm] = useState(EMPTY);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!open) return;
    setForm(company ? {
      name: company.name || "",
      description: company.description || "",
      status: company.status || "active",
    } : EMPTY);
    setError("");
  }, [open, company]);

  async function submit(event) {
    event.preventDefault();
    if (!form.name.trim()) {
      setError("请输入公司名称");
      return;
    }
    setSubmitting(true);
    setError("");
    try {
      const values = { ...form, name: form.name.trim(), description: form.description.trim() };
      const saved = company
        ? await updateCompany(company.company_id, values)
        : await createCompany(values);
      onSuccess?.(saved);
    } catch (err) {
      setError(err?.message || "公司保存失败");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <TerraDrawer
      open={open}
      title={company ? "编辑公司" : "创建公司"}
      description="公司是 Workspace 中最大的业务对象。"
      onClose={onClose}
    >
      <form onSubmit={submit} className="space-y-4">
        <TerraInput
          label="公司名称"
          required
          value={form.name}
          onChange={(event) => setForm((current) => ({ ...current, name: event.target.value }))}
          error={error && !form.name.trim() ? error : ""}
          placeholder="例如：云帆智能"
          autoFocus
        />
        <div>
          <label htmlFor="company-description" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            公司描述
          </label>
          <textarea
            id="company-description"
            rows={4}
            value={form.description}
            onChange={(event) => setForm((current) => ({ ...current, description: event.target.value }))}
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none resize-y focus:ring-2 focus:ring-ui-primary/30"
            placeholder="描述公司的业务方向与目标"
          />
        </div>
        <div>
          <label htmlFor="company-status" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            状态
          </label>
          <select
            id="company-status"
            value={form.status}
            onChange={(event) => setForm((current) => ({ ...current, status: event.target.value }))}
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
          >
            <option value="active">运行中</option>
            <option value="draft">草稿</option>
            <option value="disabled">已暂停</option>
            <option value="archived">已归档</option>
          </select>
        </div>
        {error && form.name.trim() && <p className="text-xs text-ui-red">{error}</p>}
        <div className="flex justify-end gap-3 pt-2">
          <TerraButton type="button" variant="ghost" onClick={onClose}>取消</TerraButton>
          <TerraButton type="submit" disabled={submitting}>
            {submitting ? "保存中…" : "保存公司"}
          </TerraButton>
        </div>
      </form>
    </TerraDrawer>
  );
}
