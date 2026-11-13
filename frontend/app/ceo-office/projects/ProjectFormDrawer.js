"use client";

import { useEffect, useMemo, useState } from "react";
import {
  TerraButton,
  TerraDrawer,
  TerraInput,
} from "../../../components/terra/TerraPrimitives.js";
import { createProject } from "../../../lib/api.js";

const EMPTY = {
  name: "",
  goal: "",
  description: "",
  department_id: "",
  owner_employee_id: "",
};

export default function ProjectFormDrawer({
  open,
  departments = [],
  employees = [],
  onClose,
  onSuccess,
}) {
  const [form, setForm] = useState(EMPTY);
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  const availableDepartments = useMemo(
    () => departments.filter((item) => item.enabled && item.status === "active"),
    [departments]
  );
  const compatibleEmployees = useMemo(
    () => employees.filter(
      (item) => item.enabled
        && item.status !== "disabled"
        && item.department_id === form.department_id
    ),
    [employees, form.department_id]
  );

  useEffect(() => {
    if (!open) return;
    const department = availableDepartments[0];
    const owner = employees.find(
      (item) => item.enabled
        && item.status !== "disabled"
        && item.department_id === department?.id
    );
    setForm({
      ...EMPTY,
      department_id: department?.id || "",
      owner_employee_id: owner?.id || "",
    });
    setErrors({});
    setSubmitting(false);
  }, [availableDepartments, employees, open]);

  function selectDepartment(departmentId) {
    const owner = employees.find(
      (item) => item.enabled
        && item.status !== "disabled"
        && item.department_id === departmentId
    );
    setForm((current) => ({
      ...current,
      department_id: departmentId,
      owner_employee_id: owner?.id || "",
    }));
  }

  async function submit(event) {
    event.preventDefault();
    const nextErrors = {};
    const companyId = availableDepartments.find(
      (item) => item.id === form.department_id
    )?.company_id;
    if (!companyId) nextErrors.submit = "当前业务部门所属 Workspace 不可用";
    if (!form.name.trim()) nextErrors.name = "请输入项目名称";
    if (!form.goal.trim()) nextErrors.goal = "请输入项目目标";
    if (!form.department_id) nextErrors.department_id = "请先创建并选择业务部门";
    if (!form.owner_employee_id) nextErrors.owner_employee_id = "请先为该业务部门创建并选择项目负责人";
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length) return;

    setSubmitting(true);
    try {
      const project = await createProject({
        company_id: companyId,
        name: form.name.trim(),
        goal: form.goal.trim(),
        description: form.description.trim(),
        department_id: form.department_id,
        owner_employee_id: form.owner_employee_id,
        status: "planned",
      });
      onSuccess?.(project);
    } catch (error) {
      setErrors({ submit: error?.message || "项目创建失败" });
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <TerraDrawer
      open={open}
      title="创建项目"
      description="项目直接归属于业务部门；负责人必须是该业务部门的员工。"
      onClose={onClose}
    >
      <form onSubmit={submit} className="space-y-4">
        <TerraInput
          label="项目名称"
          required
          value={form.name}
          onChange={(event) => setForm((current) => ({ ...current, name: event.target.value }))}
          error={errors.name}
          placeholder="例如：Curis MVP 交付"
          autoFocus
        />

        <div>
          <label htmlFor="project-goal" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            项目目标 *
          </label>
          <textarea
            id="project-goal"
            rows={4}
            value={form.goal}
            onChange={(event) => setForm((current) => ({ ...current, goal: event.target.value }))}
            className={`w-full px-3 py-2 rounded-ui-sm border text-sm text-ui-txt bg-ui-surface outline-none resize-y focus:ring-2 focus:ring-ui-primary/30 ${
              errors.goal ? "border-ui-red" : "border-ui-line"
            }`}
            placeholder="说明项目需要完成的真实业务目标"
          />
          {errors.goal && <p className="text-ui-1 text-ui-red mt-1">{errors.goal}</p>}
        </div>

        <div>
          <label htmlFor="project-description" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            项目说明
          </label>
          <textarea
            id="project-description"
            rows={3}
            value={form.description}
            onChange={(event) => setForm((current) => ({ ...current, description: event.target.value }))}
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none resize-y focus:ring-2 focus:ring-ui-primary/30"
            placeholder="补充范围、约束或预期成果"
          />
        </div>

        <div>
          <label htmlFor="project-department" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            所属业务部门 *
          </label>
          <select
            id="project-department"
            value={form.department_id}
            onChange={(event) => selectDepartment(event.target.value)}
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
          >
            {availableDepartments.length === 0 && <option value="">暂无可用业务部门</option>}
            {availableDepartments.map((item) => (
              <option key={item.id} value={item.id}>{item.name}</option>
            ))}
          </select>
          {errors.department_id && <p className="text-ui-1 text-ui-red mt-1">{errors.department_id}</p>}
        </div>

        <div>
          <label htmlFor="project-owner" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            项目负责人 *
          </label>
          <select
            id="project-owner"
            value={form.owner_employee_id}
            onChange={(event) => setForm((current) => ({
              ...current,
              owner_employee_id: event.target.value,
            }))}
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
          >
            {compatibleEmployees.length === 0 && <option value="">当前业务部门暂无可用员工</option>}
            {compatibleEmployees.map((item) => (
              <option key={item.id} value={item.id}>{item.name}</option>
            ))}
          </select>
          {errors.owner_employee_id && (
            <p className="text-ui-1 text-ui-red mt-1">{errors.owner_employee_id}</p>
          )}
        </div>

        <p className="text-xs text-ui-txt-3 bg-ui-surface-2 rounded-ui-sm p-3">
          创建后进入项目工作台，可继续创建任务并查看任务成果。
        </p>
        {errors.submit && <p className="text-xs text-ui-red">{errors.submit}</p>}

        <div className="flex justify-end gap-3 pt-2">
          <TerraButton type="button" variant="ghost" onClick={onClose}>取消</TerraButton>
          <TerraButton type="submit" disabled={submitting}>
            {submitting ? "创建中…" : "创建项目"}
          </TerraButton>
        </div>
      </form>
    </TerraDrawer>
  );
}
