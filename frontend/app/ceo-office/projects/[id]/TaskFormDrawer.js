"use client";

import { useEffect, useMemo, useState } from "react";
import {
  TerraButton,
  TerraDrawer,
} from "../../../../components/terra/TerraPrimitives.js";
import { createProjectTask } from "../../../../lib/api.js";
import {
  getEmployeeCapabilities,
  getModelGatewaySummary,
} from "../../../../lib/capabilities.js";

export default function TaskFormDrawer({
  open,
  project,
  employees = [],
  onClose,
  onSuccess,
}) {
  const availableEmployees = useMemo(
    () => employees.filter(
      (item) => item.enabled
        && item.status !== "disabled"
        && item.company_id === project?.company_id
    ),
    [employees, project?.company_id]
  );
  const [content, setContent] = useState("");
  const [employeeId, setEmployeeId] = useState("");
  const [models, setModels] = useState([]);
  const [modelKey, setModelKey] = useState("");
  const [loadingModels, setLoadingModels] = useState(false);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!open) return;
    setContent("");
    setEmployeeId(availableEmployees[0]?.id || "");
    setModels([]);
    setModelKey("");
    setError("");
    setSubmitting(false);
  }, [availableEmployees, open]);

  useEffect(() => {
    if (!open || !employeeId) return undefined;
    let active = true;
    setLoadingModels(true);
    getEmployeeCapabilities(employeeId).then(async (profile) => {
      const gateway = await getModelGatewaySummary();
      if (!active) return;
      const boundKeys = new Set(
        (profile?.bindings || [])
          .filter((item) => item.enabled && item.capability_source === "official" && item.capability_type === "model")
          .map((item) => item.capability_id)
      );
      const available = (gateway?.models || []).filter((item) => boundKeys.has(item.model_key));
      setModels(available);
      setModelKey("");
    }).catch((err) => {
      if (active) setError(err?.message || "员工模型能力读取失败");
    }).finally(() => {
      if (active) setLoadingModels(false);
    });
    return () => { active = false; };
  }, [employeeId, open]);

  async function submit(event) {
    event.preventDefault();
    if (!content.trim()) return setError("请输入任务目标");
    if (!employeeId) return setError("请选择执行员工");
    setSubmitting(true);
    setError("");
    try {
      const task = await createProjectTask(project.project_id, {
        content: content.trim(),
        employee_id: employeeId,
        ...(modelKey ? {
          capability_source: "official",
          capability_type: "model",
          capability_id: modelKey,
        } : {}),
      });
      onSuccess?.(task);
    } catch (err) {
      setError(err?.message || "任务创建失败");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <TerraDrawer
      open={open}
      title="创建任务"
      description="任务属于当前项目，并交由已启用的 AI 员工执行。"
      onClose={onClose}
    >
      <form onSubmit={submit} className="space-y-4">
        <div>
          <label htmlFor="task-content" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            任务目标 *
          </label>
          <textarea
            id="task-content"
            rows={6}
            value={content}
            onChange={(event) => setContent(event.target.value)}
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none resize-y focus:ring-2 focus:ring-ui-primary/30"
            placeholder="说明这项任务需要完成的真实结果"
            autoFocus
          />
        </div>

        <div>
          <label htmlFor="task-employee" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            执行员工 *
          </label>
          <select
            id="task-employee"
            value={employeeId}
            onChange={(event) => setEmployeeId(event.target.value)}
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
          >
            {availableEmployees.length === 0 && <option value="">暂无可用员工</option>}
            {availableEmployees.map((item) => (
              <option key={item.id} value={item.id}>{item.name} · {item.role}</option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="task-model" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            执行模型
          </label>
          <select
            id="task-model"
            value={modelKey}
            onChange={(event) => setModelKey(event.target.value)}
            disabled={loadingModels}
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30 disabled:opacity-60"
          >
            <option value="">{loadingModels ? "正在读取…" : "使用员工默认模型"}</option>
            {models.map((item) => (
              <option key={item.model_key} value={item.model_key}>
                {item.display_name} · {item.model_name}
              </option>
            ))}
          </select>
          {!loadingModels && models.length === 0 && (
            <p className="text-ui-1 text-ui-txt-3 mt-1">
              该员工尚未绑定可用模型；可先在员工 Capability Profile 中绑定。
            </p>
          )}
        </div>

        {error && <p className="text-xs text-ui-red">{error}</p>}
        <div className="flex justify-end gap-3 pt-2">
          <TerraButton type="button" variant="ghost" onClick={onClose}>取消</TerraButton>
          <TerraButton type="submit" disabled={submitting || availableEmployees.length === 0}>
            {submitting ? "创建中…" : "创建任务"}
          </TerraButton>
        </div>
      </form>
    </TerraDrawer>
  );
}
