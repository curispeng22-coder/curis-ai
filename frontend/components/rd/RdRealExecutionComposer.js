"use client";

import { useEffect, useState } from "react";

import { CEO_ID, getProjects } from "../../lib/api.js";
import { createRuntimeCycle, runtimeErrorMessage } from "../../lib/runtimeApi.js";
import { TerraButton, TerraCard, TerraInput, TerraTag } from "../terra/TerraPrimitives.js";


export default function RdRealExecutionComposer({ workspace, onCreated }) {
  const [projects, setProjects] = useState([]);
  const [values, setValues] = useState({
    projectRef: "",
    title: "",
    outcome: "",
    instruction: "",
    resourceRefs: "",
    testCommand: "python3 -m pytest -q",
  });
  const [saving, setSaving] = useState(false);
  const [advancedOpen, setAdvancedOpen] = useState(false);
  const [error, setError] = useState("");
  const change = (key) => (event) => setValues((current) => ({ ...current, [key]: event.target.value }));

  useEffect(() => {
    getProjects(workspace.company_id)
      .then((payload) => {
        const rows = (payload?.projects || payload || []).filter((item) => item.status === "active");
        setProjects(rows);
        setValues((current) => ({ ...current, projectRef: current.projectRef || rows[0]?.project_id || "" }));
      })
      .catch(() => setProjects([]));
  }, [workspace.company_id]);

  async function submit(event) {
    event.preventDefault();
    if (!values.projectRef.trim() || !values.title.trim() || !values.outcome.trim()) {
      setError("请选择项目，并告诉研发员工要解决的问题和期望结果。");
      return;
    }
    if (!values.resourceRefs.trim() || !values.testCommand.trim()) {
      setAdvancedOpen(true);
      setError("当前项目还没有默认执行范围，请在执行详情中确认相关文件和验证方式。");
      return;
    }
    setSaving(true);
    setError("");
    try {
      await createRuntimeCycle(workspace.workspace_id, {
        ceo_id: CEO_ID,
        owner_ref: "CEO Assistant",
        outcome_ref: values.outcome.trim(),
        intent_ref: values.instruction.trim() || values.title.trim(),
        blueprint_version: workspace.blueprint_version,
        project_ref: values.projectRef,
        work_item_title: values.title.trim(),
        instruction: values.instruction.trim() || `${values.title.trim()}。期望结果：${values.outcome.trim()}。`,
        resource_refs: values.resourceRefs.split(/[,\n]/).map((item) => item.trim()).filter(Boolean),
        test_command: values.testCommand.trim().split(/\s+/),
        requested_access_intent: "AUTO_WITHIN_BOUNDARY",
      });
      setValues((current) => ({ ...current, title: "", outcome: "", instruction: "", resourceRefs: "" }));
      setAdvancedOpen(false);
      onCreated();
    } catch (requestError) {
      setError(requestError?.message || runtimeErrorMessage(requestError));
    } finally {
      setSaving(false);
    }
  }

  return (
    <TerraCard className="mb-4">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h2 className="font-ui-sans text-ui-4 font-semibold text-ui-txt">开始一项研发工作</h2>
          <p className="mt-1 text-ui-1 text-ui-txt-3">告诉研发员工要解决的问题。代码执行范围和验证方式只在需要时确认。</p>
        </div>
        <TerraTag color="amber">受控执行</TerraTag>
      </div>
      <form onSubmit={submit} className="mt-4 grid gap-3">
        <label className="text-ui-1 font-bold text-ui-txt-2">
          研发项目
          <select value={values.projectRef} onChange={change("projectRef")} className="mt-1.5 min-h-10 w-full rounded-ui-sm border border-ui-line bg-ui-surface px-3 text-ui-2 text-ui-txt" required>
            <option value="">选择已有项目</option>
            {projects.map((project) => <option key={project.project_id} value={project.project_id}>{project.name}</option>)}
          </select>
        </label>
        <div className="grid gap-3 sm:grid-cols-2">
          <TerraInput label="要解决的问题" placeholder="例如：修复计算函数错误" value={values.title} onChange={change("title")} required />
          <TerraInput label="期望结果" placeholder="例如：加法测试恢复通过" value={values.outcome} onChange={change("outcome")} required />
        </div>
        <details open={advancedOpen} onToggle={(event) => setAdvancedOpen(event.currentTarget.open)} className="rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3">
          <summary className="cursor-pointer text-ui-1 font-semibold text-ui-txt-2">执行详情（通常无需修改）</summary>
          <div className="mt-3 grid gap-3">
            <label className="text-ui-1 font-bold text-ui-txt-2">
              给研发员工的补充说明
              <textarea rows={3} value={values.instruction} onChange={change("instruction")} placeholder="不填写时，将直接使用上面的工作与期望结果。" className="mt-1.5 w-full resize-y rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-ui-2 text-ui-txt" />
            </label>
            <div className="grid gap-3 sm:grid-cols-2">
              <TerraInput label="本次相关文件" placeholder="src/calc.py, tests/test_calc.py" value={values.resourceRefs} onChange={change("resourceRefs")} required />
              <TerraInput label="验证方式" value={values.testCommand} onChange={change("testCommand")} required />
            </div>
            <p className="text-ui-1 leading-relaxed text-ui-txt-3">当前项目尚未提供默认文件范围，因此首次执行需要确认。这里不会扩大员工的文件访问范围。</p>
          </div>
        </details>
        {!projects.length && <p className="text-ui-1 text-ui-warning">当前公司还没有可用研发项目；请先在项目页建立真实项目。</p>}
        {error && <p role="alert" className="rounded-ui-sm border border-ui-red bg-ui-red/10 px-3 py-2 text-ui-1 text-ui-red">{error}</p>}
        <div><TerraButton type="submit" variant="primary" disabled={saving || !projects.length}>{saving ? "正在交给员工…" : "交给研发员工"}</TerraButton></div>
      </form>
    </TerraCard>
  );
}
