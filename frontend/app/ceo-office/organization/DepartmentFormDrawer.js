"use client";

import { useEffect, useState } from "react";
import {
  TerraButton,
  TerraDrawer,
  TerraInput,
} from "../../../components/terra/TerraPrimitives.js";
import { createDepartment, updateDepartment } from "../../../lib/api.js";

const EMPTY = { name: "", mission: "", template_id: "", status: "active" };

export default function DepartmentFormDrawer({
  open,
  department,
  companyId,
  templates = [],
  existingDepts = [],
  onClose,
  onSuccess,
}) {
  const [form, setForm] = useState(EMPTY);
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!open) return;
    setForm(department ? {
      name: department.name || "",
      mission: department.mission || "",
      template_id: department.template_id || "",
      status: department.status || "active",
    } : { ...EMPTY, template_id: templates[0]?.id || "" });
    setErrors({});
  }, [open, department, templates]);

  async function submit(event) {
    event.preventDefault();
    const nextErrors = {};
    const name = form.name.trim();
    if (!name) nextErrors.name = "请输入业务部门名称";
    if (existingDepts.some((item) => item.id !== department?.id && item.name === name)) {
      nextErrors.name = "已存在同名业务部门";
    }
    if (!department && !form.template_id) nextErrors.template_id = "当前没有可用业务部门模板";
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length) return;

    setSubmitting(true);
    try {
      const saved = department
        ? await updateDepartment(department.id, {
            name,
            mission: form.mission.trim(),
            status: form.status,
          })
        : await createDepartment({
            company_id: companyId,
            template_id: form.template_id,
            name,
            mission: form.mission.trim(),
            status: form.status,
          });
      onSuccess?.(saved);
    } catch (error) {
      setErrors({ submit: error?.message || "业务部门保存失败" });
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <TerraDrawer
      open={open}
      title={department ? "编辑业务部门" : "创建业务部门"}
      description="业务部门是 CEO 直接管理的价值创造单元，例如小红书业务部、电商业务部或 AI 咨询业务部。"
      onClose={onClose}
    >
      <form onSubmit={submit} className="space-y-4">
        <TerraInput
          label="业务部门名称"
          required
          value={form.name}
          onChange={(event) => setForm((current) => ({ ...current, name: event.target.value }))}
          error={errors.name}
          placeholder="例如：小红书业务部"
          autoFocus
        />
        <div>
          <label htmlFor="department-mission" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            价值目标
          </label>
          <textarea
            id="department-mission"
            rows={4}
            value={form.mission}
            onChange={(event) => setForm((current) => ({ ...current, mission: event.target.value }))}
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none resize-y focus:ring-2 focus:ring-ui-primary/30"
            placeholder="描述该业务部门创造的价值与目标"
          />
        </div>
        {!department && (
          <div>
            <label htmlFor="department-template" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
              业务部门模板
            </label>
            <select
              id="department-template"
              value={form.template_id}
              onChange={(event) => setForm((current) => ({ ...current, template_id: event.target.value }))}
              className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
            >
              {templates.length === 0 && <option value="">暂无可用模板</option>}
              {templates.map((template) => (
                <option key={template.id} value={template.id}>{template.name}</option>
              ))}
            </select>
            {errors.template_id && <p className="text-xs text-ui-red mt-1">{errors.template_id}</p>}
          </div>
        )}
        <div>
          <label htmlFor="department-status" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            状态
          </label>
          <select
            id="department-status"
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
        {errors.submit && <p className="text-xs text-ui-red">{errors.submit}</p>}
        <div className="flex justify-end gap-3 pt-2">
          <TerraButton type="button" variant="ghost" onClick={onClose}>取消</TerraButton>
          <TerraButton type="submit" disabled={submitting || !companyId}>
            {submitting ? "保存中…" : "保存业务部门"}
          </TerraButton>
        </div>
      </form>
    </TerraDrawer>
  );
}
