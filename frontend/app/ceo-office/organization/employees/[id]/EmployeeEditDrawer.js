"use client";

import { useEffect, useRef, useState } from "react";
import {
  TerraButton,
  TerraDrawer,
  TerraInput,
} from "../../../../../components/terra/TerraPrimitives.js";
import {
  getEmployee,
  getEmployeeCapabilities,
  setEmployeeCapabilities,
  updateEmployee,
} from "../../../../../lib/api.js";

// Phase-10 岗位授权：绑定被岗位白名单拒绝时给友好中文提示。
function friendlyBindingError(error) {
  const message = error?.message || "";
  if (message.includes("not authorized")) {
    return "部分能力超出该岗位授权范围（岗位只能绑定允许类型的能力），请调整岗位授权或选择其他能力。";
  }
  return message;
}

function capabilityKey(item) {
  return `${item.source}:${item.capability_type}:${item.capability_id}`;
}

function bindingKey(item) {
  return `${item.capability_source}:${item.capability_type}:${item.capability_id}`;
}

export default function EmployeeEditDrawer({
  open,
  employee,
  roleLabel,
  capabilities = [],
  bindings = [],
  executionPermission = null,
  onClose,
  onSuccess,
}) {
  const [form, setForm] = useState({
    name: "",
    instructions_override: "",
    status: "idle",
    capabilityKeys: [],
  });
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [execEnabled, setExecEnabled] = useState(false);
  const [unknown, setUnknown] = useState(false);
  const inFlight = useRef(false);
  const epoch = useRef(0);
  const canManage = executionPermission?.manageable === true
    && executionPermission.employee_id === employee?.id
    && executionPermission.company_id === employee?.company_id;

  useEffect(() => {
    epoch.current++;
    if (!open || !employee) return;
    setForm({
      name: employee.name || "",
      instructions_override: employee.instructions_override || "",
      status: employee.status || "idle",
      capabilityKeys: bindings.map(bindingKey),
    });
    setErrors({});
    setSubmitting(false);
    setUnknown(false);
    setExecEnabled(executionPermission?.enabled === true);
    return () => { epoch.current++; };
  }, [bindings, employee, open, executionPermission]);

  function toggleCapability(key) {
    setForm((current) => ({
      ...current,
      capabilityKeys: current.capabilityKeys.includes(key)
        ? current.capabilityKeys.filter((item) => item !== key)
        : [...current.capabilityKeys, key],
    }));
  }

  function verifyReadback(saved, profile) {
    if (saved?.id !== employee.id || saved?.company_id !== employee.company_id
      || profile?.employee_id !== employee.id
      || (profile.execution_permission && profile.execution_permission.company_id !== employee.company_id)) {
      throw new Error("员工配置回读范围不一致，请重新进入当前公司员工。");
    }
  }

  async function readback() {
    if (inFlight.current) return;
    inFlight.current = true;
    setSubmitting(true);
    const token = epoch.current;
    try {
      const [saved, profile] = await Promise.all([getEmployee(employee.id), getEmployeeCapabilities(employee.id)]);
      if (token !== epoch.current) return;
      verifyReadback(saved, profile);
      onSuccess?.(saved, profile, { readback: true });
    } catch (error) {
      if (token === epoch.current) setErrors({ submit: error?.message || "当前配置读取失败，请再次读取。" });
    } finally {
      inFlight.current = false;
      if (token === epoch.current) setSubmitting(false);
    }
  }

  async function submit(event) {
    event.preventDefault();
    if (inFlight.current || unknown) return;
    const nextErrors = {};
    if (!form.name.trim()) nextErrors.name = "请输入员工名称";
    const permissionChanged = canManage && execEnabled !== executionPermission.enabled;
    const originalKeys = new Set(bindings.map(bindingKey));
    const selectedKeys = new Set(form.capabilityKeys);
    const added = capabilities.filter((item) => selectedKeys.has(capabilityKey(item)) && !originalKeys.has(capabilityKey(item)));
    if (canManage && !execEnabled && added.some(item => ["agent", "connector"].includes(item.capability_type))) {
      nextErrors.submit = "请先明确允许此员工使用执行类能力，再保存所选 Agent。";
    }
    if (permissionChanged && !execEnabled && !executionPermission.can_revoke) {
      nextErrors.submit = "岗位模板仍授予执行许可，当前无法在员工层撤销。";
    }
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length) return;

    inFlight.current = true;
    setSubmitting(true);
    const token = epoch.current;
    try {
      const changes = {};
      if (form.name !== (employee.name || "")) changes.name = form.name.trim();
      if (form.instructions_override !== (employee.instructions_override || "")) {
        changes.instructions_override = form.instructions_override.trim();
      }
      if (form.status !== (employee.status || "idle")) changes.status = form.status;
      const capabilitiesChanged = originalKeys.size !== selectedKeys.size
        || [...originalKeys].some((key) => !selectedKeys.has(key));
      let profile = { employee_id: employee.id, bindings, execution_permission: executionPermission };
      if (capabilitiesChanged || permissionChanged) {
        const retained = bindings.filter((item) => selectedKeys.has(bindingKey(item)));
        const priority = Math.max(0, ...bindings.map((item) => item.priority || 0));
        profile = await setEmployeeCapabilities(
          employee.id,
          [...retained.map((item) => ({ capability_source: item.capability_source, capability_type: item.capability_type,
            capability_id: item.capability_id, priority: item.priority, enabled: item.enabled !== false && item.enabled !== 0 })),
          ...added.map((item, index) => ({
            capability_source: item.source, capability_type: item.capability_type,
            capability_id: item.capability_id, priority: priority + (index + 1) * 10, enabled: true,
          }))],
          canManage ? { company_id: employee.company_id, expected_revision: executionPermission.revision, enabled: execEnabled } : undefined,
        );
        if (token !== epoch.current) return;
        verifyReadback(employee, profile);
      }
      // Metadata is separate; a failure after the atomic profile save requires readback, not replay.
      const saved = Object.keys(changes).length ? await updateEmployee(employee.id, changes) : employee;
      if (token !== epoch.current) return;
      verifyReadback(saved, profile);
      onSuccess?.(saved, profile);
    } catch (error) {
      if (token === epoch.current) {
        setUnknown(true);
        setErrors({ submit: (friendlyBindingError(error) || "员工保存未能确认") + " 请读取当前配置核对结果，不要重复提交。" });
      }
    } finally {
      inFlight.current = false;
      if (token === epoch.current) setSubmitting(false);
    }
  }

  return (
    <TerraDrawer
      open={open}
      title="编辑 AI 员工"
      description="更新员工名称、自定义工作说明、状态和默认能力配置档案。"
      onClose={() => { if (!inFlight.current) onClose?.({ unknown }); }}
    >
      <form onSubmit={submit} className="space-y-4">
        <TerraInput
          label="员工名称"
          required
          value={form.name}
          onChange={(event) => setForm((current) => ({ ...current, name: event.target.value }))}
          error={errors.name}
        />

        <div className="rounded-ui-sm bg-ui-surface-2 px-3 py-2">
          <p className="text-ui-1 text-ui-txt-3">岗位模板</p>
          <p className="text-sm font-semibold text-ui-txt mt-0.5">{roleLabel || employee?.role}</p>
        </div>

        <div>
          <label htmlFor="employee-edit-responsibility" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            自定义工作说明（可选）
          </label>
          <textarea
            id="employee-edit-responsibility"
            rows={4}
            value={form.instructions_override}
            onChange={(event) => setForm((current) => ({
              ...current,
              instructions_override: event.target.value,
            }))}
            className={`w-full px-3 py-2 rounded-ui-sm border text-sm text-ui-txt bg-ui-surface outline-none resize-y focus:ring-2 focus:ring-ui-primary/30 ${
              errors.instructions_override ? "border-ui-red" : "border-ui-line"
            }`}
          />
          <p className="text-ui-1 text-ui-txt-3 mt-1">补充个人工作说明；实际岗位职责以当前责任安排为准。</p>
          {errors.instructions_override && (
            <p className="text-ui-1 text-ui-red mt-1">{errors.instructions_override}</p>
          )}
        </div>

        <div>
          <label htmlFor="employee-edit-status" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            当前状态
          </label>
          <select
            id="employee-edit-status"
            value={form.status}
            onChange={(event) => setForm((current) => ({ ...current, status: event.target.value }))}
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
          >
            <option value="idle">空闲</option>
            <option value="assigned">工作中</option>
            <option value="disabled">已暂停</option>
          </select>
        </div>

        {executionPermission && (
          <fieldset className="rounded-ui-sm border border-ui-line p-3">
            <legend className="text-xs font-bold text-ui-txt-2">员工执行许可</legend>
            <p className="text-xs text-ui-txt-2">
              当前：{executionPermission.enabled ? "已允许使用执行类能力" : "尚未允许使用执行类能力"}
            </p>
            {canManage ? (
              <label className="flex items-start gap-2.5 mt-2 text-xs text-ui-txt">
                <input type="checkbox" aria-label="允许此员工使用执行类能力"
                  checked={execEnabled} disabled={submitting || unknown}
                  onChange={(event) => setExecEnabled(event.target.checked)} />
                <span>允许此员工使用执行类能力，包括 Agent 及其他执行类工具或连接器。</span>
              </label>
            ) : <p className="text-xs text-ui-txt-3 mt-2">当前身份或岗位安排不支持在此修改执行许可。</p>}
            <p className="text-xs text-ui-txt-3 mt-2">此许可不授予资料、站点、发布或费用权限，实际工作仍需满足各项授权。</p>
            {canManage && executionPermission.enabled && !execEnabled && (
              <p className="text-xs text-ui-txt-2 mt-2">保存撤销后会移除已绑定的执行类能力；其他能力保持不变。在途外部效果仍需核对。</p>
            )}
          </fieldset>
        )}

        <fieldset>
          <legend className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            Capability Profile
          </legend>
          {capabilities.length === 0 ? (
            <p className="text-xs text-ui-txt-3 bg-ui-surface-2 rounded-ui-sm p-3">
              当前没有可用能力。
            </p>
          ) : (
            <div className="max-h-52 overflow-y-auto rounded-ui-sm border border-ui-line divide-y divide-ui-line">
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
        {unknown && <TerraButton type="button" disabled={submitting} onClick={readback}>读取当前员工配置</TerraButton>}
        <div className="flex justify-end gap-3 pt-2">
          <TerraButton type="button" variant="ghost" disabled={submitting}
            onClick={() => { if (!inFlight.current) onClose?.({ unknown }); }}>
            {unknown ? "关闭并稍后核对" : "取消"}
          </TerraButton>
          <TerraButton type="submit" disabled={submitting || unknown}>
            {submitting ? "保存中…" : "保存员工"}
          </TerraButton>
        </div>
      </form>
    </TerraDrawer>
  );
}
