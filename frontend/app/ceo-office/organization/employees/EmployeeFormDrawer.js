"use client";

import { useEffect, useMemo, useState } from "react";
import {
  TerraButton,
  TerraDrawer,
  TerraInput,
} from "../../../../components/terra/TerraPrimitives.js";
import {
  createEmployee,
  deleteEmployee,
  setEmployeeCapabilities,
} from "../../../../lib/api.js";

// Phase-10 岗位授权：绑定被岗位白名单拒绝时给友好中文提示（避免裸露英文 detail）。
function friendlyBindingError(error) {
  const message = error?.message || "";
  if (message.includes("not authorized")) {
    return "部分能力超出该岗位授权范围（岗位只能绑定允许类型的能力），请调整岗位授权或选择其他能力。";
  }
  return message;
}

const EMPTY = {
  name: "",
  department_id: "",
  template_id: "",
  instructions_override: "",
  capabilityKeys: [],
};

function capabilityKey(item) {
  return `${item.source}:${item.capability_type}:${item.capability_id}`;
}

function toBinding(item, priority) {
  return {
    capability_source: item.source,
    capability_type: item.capability_type,
    capability_id: item.capability_id,
    priority,
    enabled: true,
  };
}

export default function EmployeeFormDrawer({
  open,
  departments = [],
  templates = [],
  capabilities = [],
  onClose,
  onSuccess,
}) {
  const [form, setForm] = useState(EMPTY);
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  const department = departments.find((item) => item.id === form.department_id);
  const compatibleTemplates = useMemo(
    () => templates.filter(
      (item) => !department || item.department_type === department.department_type
    ),
    [department, templates]
  );
  const selectedTemplate = compatibleTemplates.find((item) => item.id === form.template_id);

  useEffect(() => {
    if (!open) return;
    const firstDepartment = departments.find((item) => item.status === "active" && item.enabled)
      || departments[0];
    const firstTemplate = templates.find(
      (item) => item.department_type === firstDepartment?.department_type
    );
    setForm({
      ...EMPTY,
      department_id: firstDepartment?.id || "",
      template_id: firstTemplate?.id || "",
    });
    setErrors({});
    setSubmitting(false);
  }, [open, departments, templates]);

  function selectDepartment(departmentId) {
    const nextDepartment = departments.find((item) => item.id === departmentId);
    const nextTemplate = templates.find(
      (item) => item.department_type === nextDepartment?.department_type
    );
    setForm((current) => ({
      ...current,
      department_id: departmentId,
      template_id: nextTemplate?.id || "",
    }));
  }

  function toggleCapability(key) {
    setForm((current) => ({
      ...current,
      capabilityKeys: current.capabilityKeys.includes(key)
        ? current.capabilityKeys.filter((item) => item !== key)
        : [...current.capabilityKeys, key],
    }));
  }

  async function submit(event) {
    event.preventDefault();
    const nextErrors = {};
    if (!form.name.trim()) nextErrors.name = "请输入员工名称";
    if (!form.department_id) nextErrors.department_id = "请先创建并选择业务部门";
    if (!form.template_id) nextErrors.template_id = "当前业务部门没有可用员工模板";
    if (!form.instructions_override.trim()) {
      nextErrors.instructions_override = "请填写员工职责";
    }
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length) return;

    setSubmitting(true);
    let created = null;
    try {
      created = await createEmployee({
        department_id: form.department_id,
        template_id: form.template_id,
        name: form.name.trim(),
        instructions_override: form.instructions_override.trim(),
        status: "idle",
        enabled: true,
      });
      const selected = capabilities.filter(
        (item) => form.capabilityKeys.includes(capabilityKey(item))
      );
      const profile = selected.length
        ? await setEmployeeCapabilities(
            created.id,
            selected.map((item, index) => toBinding(item, (index + 1) * 10))
          )
        : { bindings: [] };
      onSuccess?.(created, profile);
    } catch (error) {
      if (created?.id) await deleteEmployee(created.id).catch(() => null);
      setErrors({ submit: friendlyBindingError(error) || "员工创建失败" });
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <TerraDrawer
      open={open}
      title="创建 AI 员工"
      description="员工是责任主体；角色来自模板，能力通过配置档案组合。"
      onClose={onClose}
    >
      <form onSubmit={submit} className="space-y-4">
        <TerraInput
          label="员工名称"
          required
          value={form.name}
          onChange={(event) => setForm((current) => ({ ...current, name: event.target.value }))}
          error={errors.name}
          placeholder="例如：研发负责人"
          autoFocus
        />

        <div>
          <label htmlFor="employee-department" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            所属业务部门 *
          </label>
          <select
            id="employee-department"
            value={form.department_id}
            onChange={(event) => selectDepartment(event.target.value)}
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
          >
            {departments.length === 0 && <option value="">暂无业务部门</option>}
            {departments.map((item) => (
              <option key={item.id} value={item.id} disabled={!item.enabled}>
                {item.name}{!item.enabled ? "（已暂停）" : ""}
              </option>
            ))}
          </select>
          {errors.department_id && <p className="text-ui-1 text-ui-red mt-1">{errors.department_id}</p>}
        </div>

        <div>
          <label htmlFor="employee-template" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            角色模板 *
          </label>
          <select
            id="employee-template"
            value={form.template_id}
            onChange={(event) => setForm((current) => ({ ...current, template_id: event.target.value }))}
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
          >
            {compatibleTemplates.length === 0 && <option value="">暂无兼容模板</option>}
            {compatibleTemplates.map((item) => (
              <option key={item.id} value={item.id}>{item.name}</option>
            ))}
          </select>
          {selectedTemplate && (
            <p className="text-ui-1 text-ui-txt-3 mt-1">
              岗位：{selectedTemplate.role} · {selectedTemplate.description || "未记录模板说明"}
            </p>
          )}
          {errors.template_id && <p className="text-ui-1 text-ui-red mt-1">{errors.template_id}</p>}
        </div>

        <div>
          <label htmlFor="employee-responsibility" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            职责 *
          </label>
          <textarea
            id="employee-responsibility"
            rows={4}
            value={form.instructions_override}
            onChange={(event) => setForm((current) => ({
              ...current,
              instructions_override: event.target.value,
            }))}
            className={`w-full px-3 py-2 rounded-ui-sm border text-sm text-ui-txt bg-ui-surface outline-none resize-y focus:ring-2 focus:ring-ui-primary/30 ${
              errors.instructions_override ? "border-ui-red" : "border-ui-line"
            }`}
            placeholder="例如：负责技术方案、任务拆解与代码质量"
          />
          {errors.instructions_override && (
            <p className="text-ui-1 text-ui-red mt-1">{errors.instructions_override}</p>
          )}
        </div>

        <fieldset>
          <legend className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            Capability Profile（可选）
          </legend>
          {capabilities.length === 0 ? (
            <p className="text-xs text-ui-txt-3 bg-ui-surface-2 rounded-ui-sm p-3">
              当前没有可用能力，可稍后在员工详情配置。
            </p>
          ) : (
            <div className="max-h-48 overflow-y-auto rounded-ui-sm border border-ui-line divide-y divide-ui-line">
              {capabilities.map((item) => {
                const key = capabilityKey(item);
                return (
                  <label key={key} className="flex items-start gap-2.5 px-3 py-2.5 hover:bg-ui-surface-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={form.capabilityKeys.includes(key)}
                      onChange={() => toggleCapability(key)}
                      className="mt-0.5 accent-ui-primary"
                    />
                    <span className="min-w-0">
                      <span className="block text-xs font-semibold text-ui-txt truncate">{item.label}</span>
                      <span className="block text-ui-1 text-ui-txt-3">
                        {item.capability_type} · {item.source}
                      </span>
                    </span>
                  </label>
                );
              })}
            </div>
          )}
        </fieldset>

        {errors.submit && <p className="text-xs text-ui-red">{errors.submit}</p>}
        <div className="flex justify-end gap-3 pt-2">
          <TerraButton type="button" variant="ghost" onClick={onClose}>取消</TerraButton>
          <TerraButton type="submit" disabled={submitting}>
            {submitting ? "创建中…" : "创建员工"}
          </TerraButton>
        </div>
      </form>
    </TerraDrawer>
  );
}
