"use client";

import { useEffect, useState } from "react";
import {
  TASK_ENTRY_STARTERS,
  buildCapabilitySelectorViewModel,
  buildCompanyFoundationViewModel,
  buildDepartmentInstancePayload,
  buildDepartmentActivationPayload,
  buildDepartmentActivationViewModel,
  buildDepartmentCatalogSummaryViewModel,
  buildEmployeeCapabilityBindingPayload,
  buildEmployeeInstancePayload,
  buildEmployeeSystemViewModel,
  buildTaskEntryDraft,
  buildPrivateCapabilitiesViewModel,
  buildPrivateConnectorPayload,
  buildPrivateModelPayload,
  buildPrivateToolPayload,
  buildConsoleTaskState,
  buildEvolutionDecisionSummary,
  buildExecutionSummary,
  buildFallbackEvents,
  buildMetaDevelopmentSummary,
  buildModelPreferencePayload,
  buildModelPreferenceViewModel,
  buildOperatingLabels,
  buildTaskPayload,
  buildReviewSignals,
  buildWorkflowRunViewModel,
  buildWorkflowTimeline,
} from "./taskViewModel.mjs";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";
const WORKSPACE_TENANT_ID = process.env.NEXT_PUBLIC_CURIS_TENANT_ID || "selfuse";
const WORKSPACE_CEO_ID = process.env.NEXT_PUBLIC_CURIS_CEO_ID || "local-demo-ceo";
const EMPTY_PRIVATE_MODEL = {
  name: "",
  provider_type: "newapi-compatible",
  base_url: "",
  model_name: "",
  credential_ref: "",
  enabled: true,
};
const EMPTY_PRIVATE_TOOL = {
  name: "",
  type: "llm_tool",
  description: "",
  config_ref: "",
  enabled: true,
};
const EMPTY_PRIVATE_CONNECTOR = {
  name: "",
  connector_type: "",
  config_ref: "",
  enabled: true,
};
const EMPTY_DEPARTMENT_FORM = {
  template_id: "official.department.software_rnd",
  name: "研发部",
  company_id: "local-demo-company",
  enabled_employee_template_ids: [],
  enabled: true,
};
const EMPTY_EMPLOYEE_FORM = {
  department_id: "",
  template_id: "official.employee.tech_lead",
  name: "",
  company_id: "local-demo-company",
  instructions_override: "",
  status: "idle",
  enabled: true,
};
const EMPTY_BINDING_FORM = {
  employee_id: "",
  capability_value: "",
  priority: 100,
  enabled: true,
};
const EMPTY_WORKFLOW_FORM = {
  workflow_template_id: "official.workflow.software_rnd_sop",
  department_id: "",
  name: "",
  content: "",
};

export default function Home() {
  const [content, setContent] = useState("");
  const [tasks, setTasks] = useState([]);
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [message, setMessage] = useState("");
  const [selectedStarterId, setSelectedStarterId] = useState("");
  const [loading, setLoading] = useState(false);
  const [detailLoading, setDetailLoading] = useState(false);
  const [modelPreference, setModelPreference] = useState(null);
  const [modelPreferenceSelection, setModelPreferenceSelection] = useState("");
  const [modelPreferenceLoading, setModelPreferenceLoading] = useState(false);
  const [modelPreferenceSaving, setModelPreferenceSaving] = useState(false);
  const [modelPreferenceMessage, setModelPreferenceMessage] = useState("");
  const [departmentCatalog, setDepartmentCatalog] = useState(null);
  const [departmentCatalogLoading, setDepartmentCatalogLoading] = useState(false);
  const [departmentCatalogError, setDepartmentCatalogError] = useState("");
  const [departmentActivation, setDepartmentActivation] = useState(null);
  const [departmentActivationSelection, setDepartmentActivationSelection] = useState([]);
  const [departmentActivationLoading, setDepartmentActivationLoading] = useState(false);
  const [departmentActivationSaving, setDepartmentActivationSaving] = useState(false);
  const [departmentActivationError, setDepartmentActivationError] = useState("");
  const [departmentActivationMessage, setDepartmentActivationMessage] = useState("");
  const [privateModels, setPrivateModels] = useState(null);
  const [privateTools, setPrivateTools] = useState(null);
  const [privateConnectors, setPrivateConnectors] = useState(null);
  const [privateCapabilityMessage, setPrivateCapabilityMessage] = useState("");
  const [privateCapabilityLoading, setPrivateCapabilityLoading] = useState(false);
  const [privateCapabilitySaving, setPrivateCapabilitySaving] = useState("");
  const [privateModelForm, setPrivateModelForm] = useState(EMPTY_PRIVATE_MODEL);
  const [privateToolForm, setPrivateToolForm] = useState(EMPTY_PRIVATE_TOOL);
  const [privateConnectorForm, setPrivateConnectorForm] = useState(EMPTY_PRIVATE_CONNECTOR);
  const [capabilitySelector, setCapabilitySelector] = useState(null);
  const [selectedCapabilityValue, setSelectedCapabilityValue] = useState("");
  const [employeeTemplates, setEmployeeTemplates] = useState(null);
  const [departmentTemplates, setDepartmentTemplates] = useState(null);
  const [departments, setDepartments] = useState(null);
  const [employees, setEmployees] = useState(null);
  const [employeeSystemLoading, setEmployeeSystemLoading] = useState(false);
  const [employeeSystemSaving, setEmployeeSystemSaving] = useState("");
  const [employeeSystemMessage, setEmployeeSystemMessage] = useState("");
  const [departmentForm, setDepartmentForm] = useState(EMPTY_DEPARTMENT_FORM);
  const [employeeForm, setEmployeeForm] = useState(EMPTY_EMPLOYEE_FORM);
  const [bindingForm, setBindingForm] = useState(EMPTY_BINDING_FORM);
  const [selectedEmployeeId, setSelectedEmployeeId] = useState("");
  const [workflowTemplates, setWorkflowTemplates] = useState(null);
  const [workflowRuns, setWorkflowRuns] = useState(null);
  const [selectedWorkflowRun, setSelectedWorkflowRun] = useState(null);
  const [workflowForm, setWorkflowForm] = useState(EMPTY_WORKFLOW_FORM);
  const [workflowLoading, setWorkflowLoading] = useState(false);
  const [workflowSaving, setWorkflowSaving] = useState("");
  const [workflowMessage, setWorkflowMessage] = useState("");
  const selectedTaskId = selectedRecord?.task?.task_id;

  const loadTasks = async () => {
    const response = await fetch(`${API_BASE}/api/tasks`, { cache: "no-store" });
    if (!response.ok) throw new Error("任务列表加载失败");
    const nextTasks = await response.json();
    setTasks(nextTasks);
    return nextTasks;
  };

  const loadTaskRecord = async (task) => {
    if (!task?.task_id) return null;
    setDetailLoading(true);
    try {
      const [detail, workflow, trace, metaDevelopment, evolutionDecision] = await Promise.all([
        fetchJson(`/api/task/${task.task_id}`),
        fetchOptionalJson(`/api/task/${task.task_id}/workflow`),
        fetchOptionalJson(`/api/task/${task.task_id}/trace`, []),
        fetchOptionalJson(`/api/task/${task.task_id}/meta-development`),
        fetchOptionalJson(`/api/task/${task.task_id}/evolution-decisions`),
      ]);
      const record = {
        task: detail,
        workflow,
        trace: trace || [],
        metaDevelopment,
        evolutionDecision,
      };
      setSelectedRecord(record);
      return record;
    } finally {
      setDetailLoading(false);
    }
  };

  const loadModelPreference = async () => {
    setModelPreferenceLoading(true);
    try {
      const payload = await fetchJson("/api/workspace/model-preference");
      const viewModel = buildModelPreferenceViewModel(payload);
      setModelPreference(payload);
      setModelPreferenceSelection(viewModel.options.some((model) => model.modelKey === viewModel.selectedModelKey) ? viewModel.selectedModelKey : "");
      return payload;
    } finally {
      setModelPreferenceLoading(false);
    }
  };

  const loadDepartmentCatalog = async () => {
    setDepartmentCatalogLoading(true);
    setDepartmentCatalogError("");
    try {
      const payload = await fetchJson("/api/catalog/department-types");
      setDepartmentCatalog(payload);
      return payload;
    } catch (error) {
      setDepartmentCatalogError(error.message || "部门目录加载失败");
      return null;
    } finally {
      setDepartmentCatalogLoading(false);
    }
  };

  const loadDepartmentActivation = async () => {
    setDepartmentActivationLoading(true);
    setDepartmentActivationError("");
    try {
      const payload = await fetchJson("/api/workspace/departments/activation");
      setDepartmentActivation(payload);
      setDepartmentActivationSelection(payload.active_department_type_keys || []);
      return payload;
    } catch (error) {
      setDepartmentActivationError(error.message || "部门启用状态加载失败");
      return null;
    } finally {
      setDepartmentActivationLoading(false);
    }
  };

  const loadPrivateCapabilities = async () => {
    setPrivateCapabilityLoading(true);
    try {
      const [models, tools, connectors, selector] = await Promise.all([
        fetchJson("/api/workspace/private-models"),
        fetchJson("/api/workspace/private-tools"),
        fetchJson("/api/workspace/private-connectors"),
        fetchJson("/api/workspace/capabilities/selector"),
      ]);
      setPrivateModels(models);
      setPrivateTools(tools);
      setPrivateConnectors(connectors);
      setCapabilitySelector(selector);
      return { models, tools, connectors, selector };
    } finally {
      setPrivateCapabilityLoading(false);
    }
  };

  const loadEmployeeSystem = async () => {
    setEmployeeSystemLoading(true);
    try {
      const [employeeTemplatePayload, departmentTemplatePayload, departmentPayload, employeePayload] = await Promise.all([
        fetchJson("/api/workspace/employee-templates"),
        fetchJson("/api/workspace/department-templates"),
        fetchJson("/api/workspace/departments"),
        fetchJson("/api/workspace/employees"),
      ]);
      setEmployeeTemplates(employeeTemplatePayload);
      setDepartmentTemplates(departmentTemplatePayload);
      setDepartments(departmentPayload);
      setEmployees(employeePayload);
      return { employeeTemplatePayload, departmentTemplatePayload, departmentPayload, employeePayload };
    } finally {
      setEmployeeSystemLoading(false);
    }
  };

  const loadWorkflowSystem = async () => {
    setWorkflowLoading(true);
    try {
      const [templates, runs] = await Promise.all([
        fetchJson("/api/workspace/workflow-templates"),
        fetchJson("/api/workspace/workflows"),
      ]);
      setWorkflowTemplates(templates);
      setWorkflowRuns(runs);
      return { templates, runs };
    } finally {
      setWorkflowLoading(false);
    }
  };

  const loadWorkflowRun = async (workflowRunId) => {
    if (!workflowRunId) return null;
    const detail = await fetchJson(`/api/workspace/workflows/${encodeURIComponent(workflowRunId)}`);
    setSelectedWorkflowRun(detail);
    return detail;
  };

  useEffect(() => {
    loadTasks().catch((error) => setMessage(error.message));
    loadModelPreference().catch((error) => setModelPreferenceMessage(error.message || "模型偏好加载失败"));
    loadDepartmentCatalog();
    loadDepartmentActivation();
    loadPrivateCapabilities().catch((error) => setPrivateCapabilityMessage(error.message || "私有能力加载失败"));
    loadEmployeeSystem().catch((error) => setEmployeeSystemMessage(error.message || "研发部员工加载失败"));
    loadWorkflowSystem().catch((error) => setWorkflowMessage(error.message || "工作流加载失败"));
  }, []);

  const submitTask = async (event) => {
    event.preventDefault();
    setLoading(true);
    setMessage("");
    try {
      const selectedCapability = buildCapabilitySelectorViewModel(capabilitySelector || {}).options.find((item) => item.value === selectedCapabilityValue);
      const response = await fetch(`${API_BASE}/api/task`, {
        method: "POST",
        headers: apiHeaders({ "Content-Type": "application/json" }),
        body: JSON.stringify(buildTaskPayload(content, selectedCapability, selectedEmployeeId)),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "任务创建失败");
      const nextTasks = await loadTasks();
      const createdTask = nextTasks.find((task) => task.task_id === payload.task_id);
      if (createdTask) await loadTaskRecord(createdTask);
      setContent("");
      setSelectedStarterId("");
      setMessage("任务已创建");
    } catch (error) {
      setMessage(error.message);
      setDetailLoading(false);
    } finally {
      setLoading(false);
    }
  };

  const saveDepartmentInstance = async () => {
    setEmployeeSystemSaving("department");
    setEmployeeSystemMessage("");
    try {
      const response = await fetch(`${API_BASE}/api/workspace/departments`, {
        method: "POST",
        headers: apiHeaders({ "Content-Type": "application/json" }),
        body: JSON.stringify(buildDepartmentInstancePayload(departmentForm)),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "研发部创建失败");
      setDepartmentForm(EMPTY_DEPARTMENT_FORM);
      await loadEmployeeSystem();
      setEmployeeSystemMessage("研发部实例已创建");
    } catch (error) {
      setEmployeeSystemMessage(error.message || "研发部创建失败");
    } finally {
      setEmployeeSystemSaving("");
    }
  };

  const saveEmployeeInstance = async () => {
    setEmployeeSystemSaving("employee");
    setEmployeeSystemMessage("");
    try {
      const response = await fetch(`${API_BASE}/api/workspace/employees`, {
        method: "POST",
        headers: apiHeaders({ "Content-Type": "application/json" }),
        body: JSON.stringify(buildEmployeeInstancePayload(employeeForm)),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "员工创建失败");
      setEmployeeForm(EMPTY_EMPLOYEE_FORM);
      await loadEmployeeSystem();
      setEmployeeSystemMessage("员工实例已创建");
    } catch (error) {
      setEmployeeSystemMessage(error.message || "员工创建失败");
    } finally {
      setEmployeeSystemSaving("");
    }
  };

  const saveEmployeeBinding = async () => {
    setEmployeeSystemSaving("binding");
    setEmployeeSystemMessage("");
    try {
      const selectedCapability = buildCapabilitySelectorViewModel(capabilitySelector || {}).options.find((item) => item.value === bindingForm.capability_value);
      const response = await fetch(`${API_BASE}/api/workspace/employees/${encodeURIComponent(bindingForm.employee_id)}/capabilities`, {
        method: "PUT",
        headers: apiHeaders({ "Content-Type": "application/json" }),
        body: JSON.stringify(buildEmployeeCapabilityBindingPayload(bindingForm, selectedCapability)),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "员工能力绑定失败");
      setBindingForm(EMPTY_BINDING_FORM);
      setEmployeeSystemMessage("员工能力已绑定");
    } catch (error) {
      setEmployeeSystemMessage(error.message || "员工能力绑定失败");
    } finally {
      setEmployeeSystemSaving("");
    }
  };

  const runTask = async (taskId) => {
    setLoading(true);
    setMessage("");
    try {
      const response = await fetch(`${API_BASE}/api/task/${taskId}/run`, { method: "POST", headers: apiHeaders() });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "任务执行失败");
      await loadTasks();
      await loadTaskRecord(payload);
      setMessage("任务已完成");
    } catch (error) {
      setMessage(error.message);
      setDetailLoading(false);
      await loadTasks().catch(() => null);
    } finally {
      setLoading(false);
    }
  };

  const createWorkflowRun = async () => {
    setWorkflowSaving("create");
    setWorkflowMessage("");
    try {
      const response = await fetch(`${API_BASE}/api/workspace/workflows`, {
        method: "POST",
        headers: apiHeaders({ "Content-Type": "application/json" }),
        body: JSON.stringify(workflowForm),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "工作流创建失败");
      setWorkflowForm(EMPTY_WORKFLOW_FORM);
      await loadWorkflowSystem();
      setSelectedWorkflowRun(payload);
      setWorkflowMessage("研发 SOP 工作流已创建");
    } catch (error) {
      setWorkflowMessage(error.message || "工作流创建失败");
    } finally {
      setWorkflowSaving("");
    }
  };

  const runWorkflowNextStep = async (workflowRunId) => {
    setWorkflowSaving("run");
    setWorkflowMessage("");
    try {
      const response = await fetch(`${API_BASE}/api/workspace/workflows/${encodeURIComponent(workflowRunId)}/run-next-step`, {
        method: "POST",
        headers: apiHeaders(),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "工作流步骤执行失败");
      await loadWorkflowSystem();
      setSelectedWorkflowRun(payload);
      setWorkflowMessage("下一步已执行");
    } catch (error) {
      setWorkflowMessage(error.message || "工作流步骤执行失败");
    } finally {
      setWorkflowSaving("");
    }
  };

  const selectEntryStarter = (starterId) => {
    const draft = buildTaskEntryDraft(starterId);
    setContent(draft.content);
    setSelectedStarterId(starterId);
  };

  const saveModelPreference = async () => {
    if (!modelPreferenceSelection) return;
    setModelPreferenceSaving(true);
    setModelPreferenceMessage("");
    try {
      const response = await fetch(`${API_BASE}/api/workspace/model-preference`, {
        method: "PUT",
        headers: apiHeaders({ "Content-Type": "application/json" }),
        body: JSON.stringify(buildModelPreferencePayload(modelPreferenceSelection)),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "模型偏好保存失败");
      const nextPreference = await loadModelPreference();
      const current = buildModelPreferenceViewModel(nextPreference);
      setModelPreferenceMessage(`已保存默认模型：${current.currentLabel}`);
    } catch (error) {
      setModelPreferenceMessage(error.message || "模型偏好保存失败");
    } finally {
      setModelPreferenceSaving(false);
    }
  };

  const resetModelPreference = async () => {
    setModelPreferenceSaving(true);
    setModelPreferenceMessage("");
    try {
      const response = await fetch(`${API_BASE}/api/workspace/model-preference`, { method: "DELETE", headers: apiHeaders() });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "模型偏好重置失败");
      await loadModelPreference();
      setModelPreferenceMessage("已重置工作区默认模型");
    } catch (error) {
      setModelPreferenceMessage(error.message || "模型偏好重置失败");
    } finally {
      setModelPreferenceSaving(false);
    }
  };

  const toggleDepartmentActivation = (typeKey) => {
    setDepartmentActivationSelection((current) => (
      current.includes(typeKey)
        ? current.filter((item) => item !== typeKey)
        : [...current, typeKey]
    ));
  };

  const saveDepartmentActivation = async () => {
    setDepartmentActivationSaving(true);
    setDepartmentActivationError("");
    setDepartmentActivationMessage("");
    try {
      const response = await fetch(`${API_BASE}/api/workspace/departments/activation`, {
        method: "PUT",
        headers: apiHeaders({ "Content-Type": "application/json" }),
        body: JSON.stringify(buildDepartmentActivationPayload(departmentActivationSelection)),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "部门启用状态保存失败");
      const nextActivation = await loadDepartmentActivation();
      const current = buildDepartmentActivationViewModel(nextActivation);
      setDepartmentActivationMessage(current.statusLine);
    } catch (error) {
      setDepartmentActivationError(error.message || "部门启用状态保存失败");
    } finally {
      setDepartmentActivationSaving(false);
    }
  };

  const savePrivateModel = async () => {
    await savePrivateCapability({
      path: "/api/workspace/private-models",
      form: privateModelForm,
      buildPayload: buildPrivateModelPayload,
      reset: () => setPrivateModelForm(EMPTY_PRIVATE_MODEL),
      label: "私有模型",
    });
  };

  const savePrivateTool = async () => {
    await savePrivateCapability({
      path: "/api/workspace/private-tools",
      form: privateToolForm,
      buildPayload: buildPrivateToolPayload,
      reset: () => setPrivateToolForm(EMPTY_PRIVATE_TOOL),
      label: "私有工具",
    });
  };

  const savePrivateConnector = async () => {
    await savePrivateCapability({
      path: "/api/workspace/private-connectors",
      form: privateConnectorForm,
      buildPayload: buildPrivateConnectorPayload,
      reset: () => setPrivateConnectorForm(EMPTY_PRIVATE_CONNECTOR),
      label: "私有连接器",
    });
  };

  const savePrivateCapability = async ({ path, form, buildPayload, reset, label }) => {
    setPrivateCapabilitySaving(label);
    setPrivateCapabilityMessage("");
    try {
      const response = await fetch(`${API_BASE}${path}`, {
        method: "POST",
        headers: apiHeaders({ "Content-Type": "application/json" }),
        body: JSON.stringify(buildPayload(form)),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || `${label}保存失败`);
      reset();
      await loadPrivateCapabilities();
      setPrivateCapabilityMessage(`${label}已添加`);
    } catch (error) {
      setPrivateCapabilityMessage(error.message || `${label}保存失败`);
    } finally {
      setPrivateCapabilitySaving("");
    }
  };

  return (
    <main className="min-h-screen bg-ui-bg px-4 py-8 text-ui-txt">
      <section className="mx-auto max-w-6xl">
        <header className="border-b border-ui-line pb-4">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <h1 className="text-ui-6 font-black">Curis 工作台</h1>
            <a
              href="/platform"
              className="rounded-ui-sm border border-ui-line px-3 py-2 text-ui-1 font-bold text-ui-txt-2"
            >
              平台管理后台 →
            </a>
          </div>
          <p className="mt-2 max-w-4xl text-ui-3 text-ui-txt-2">
            任务 → 编排器 → 自动工作流生成器 → 执行员工 → 工具路由 → 工具执行器 → 结果 → 执行学习 → 元开发 → 演进治理器 → 存储
          </p>
        </header>

        <CompanyFoundationPanel
          tasks={tasks}
          modelPreference={modelPreference}
          departmentCatalog={departmentCatalog}
          departmentCatalogLoading={departmentCatalogLoading}
          departmentCatalogError={departmentCatalogError}
          departmentActivation={departmentActivation}
          departmentActivationSelection={departmentActivationSelection}
          departmentActivationLoading={departmentActivationLoading}
          departmentActivationSaving={departmentActivationSaving}
          departmentActivationError={departmentActivationError}
          departmentActivationMessage={departmentActivationMessage}
          onToggleDepartment={toggleDepartmentActivation}
          onSaveDepartmentActivation={saveDepartmentActivation}
        />

        <ModelPreferencePanel
          payload={modelPreference}
          selectedModelKey={modelPreferenceSelection}
          loading={modelPreferenceLoading}
          saving={modelPreferenceSaving}
          message={modelPreferenceMessage}
          onSelectModel={setModelPreferenceSelection}
          onSave={saveModelPreference}
          onReset={resetModelPreference}
        />

        <PrivateCapabilitiesPanel
          models={privateModels}
          tools={privateTools}
          connectors={privateConnectors}
          loading={privateCapabilityLoading}
          saving={privateCapabilitySaving}
          message={privateCapabilityMessage}
          modelForm={privateModelForm}
          toolForm={privateToolForm}
          connectorForm={privateConnectorForm}
          onModelFormChange={setPrivateModelForm}
          onToolFormChange={setPrivateToolForm}
          onConnectorFormChange={setPrivateConnectorForm}
          onSaveModel={savePrivateModel}
          onSaveTool={savePrivateTool}
          onSaveConnector={savePrivateConnector}
        />

        <EmployeeSystemPanel
          employeeTemplates={employeeTemplates}
          departmentTemplates={departmentTemplates}
          departments={departments}
          employees={employees}
          capabilitySelector={capabilitySelector}
          loading={employeeSystemLoading}
          saving={employeeSystemSaving}
          message={employeeSystemMessage}
          departmentForm={departmentForm}
          employeeForm={employeeForm}
          bindingForm={bindingForm}
          onDepartmentFormChange={setDepartmentForm}
          onEmployeeFormChange={setEmployeeForm}
          onBindingFormChange={setBindingForm}
          onSaveDepartment={saveDepartmentInstance}
          onSaveEmployee={saveEmployeeInstance}
          onSaveBinding={saveEmployeeBinding}
        />

        <WorkflowSystemPanel
          templates={workflowTemplates}
          runs={workflowRuns}
          selectedRun={selectedWorkflowRun}
          departments={departments}
          form={workflowForm}
          loading={workflowLoading}
          saving={workflowSaving}
          message={workflowMessage}
          onFormChange={setWorkflowForm}
          onCreate={createWorkflowRun}
          onSelectRun={loadWorkflowRun}
          onRunNextStep={runWorkflowNextStep}
        />

        <form className="mt-5 grid gap-4 rounded-ui-sm border border-ui-line bg-ui-surface p-4 shadow-sm" onSubmit={submitTask}>
          <div>
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div>
                <h2 className="text-ui-3 font-black uppercase text-ui-txt-3">任务入口</h2>
                <p className="mt-1 text-ui-3 text-ui-txt-2">选择一个入口模板，或直接在任务编辑器中输入。</p>
              </div>
              {selectedStarterId ? (
                <button type="button" className="rounded-ui-sm border border-ui-line px-3 py-2 text-ui-1 font-bold text-ui-txt-2" onClick={() => setSelectedStarterId("")}>
                  自由输入
                </button>
              ) : null}
            </div>
            <div className="mt-3 grid gap-2 md:grid-cols-3">
              {TASK_ENTRY_STARTERS.map((starter) => {
                const isSelected = starter.id === selectedStarterId;
                return (
                  <button
                    key={starter.id}
                    type="button"
                    className={`rounded-ui-sm border p-3 text-left ${isSelected ? "border-ui-primary bg-ui-primary text-ui-primary-fg" : "border-ui-line bg-ui-surface-2 text-ui-txt"}`}
                    onClick={() => selectEntryStarter(starter.id)}
                  >
                    <span className="block text-ui-3 font-black">{starter.label}</span>
                    <span className={`mt-1 block text-ui-1 ${isSelected ? "text-ui-primary-fg opacity-75" : "text-ui-txt-3"}`}>{starter.description}</span>
                  </button>
                );
              })}
            </div>
          </div>
          <label className="block text-ui-3 font-bold text-ui-txt-2">
            任务编辑器
            <textarea
              className="mt-1 min-h-24 w-full rounded-ui-sm border border-ui-line px-3 py-2 font-normal"
              required
              value={content}
              onChange={(event) => setContent(event.target.value)}
            />
          </label>
          <CapabilitySelectorField
            payload={capabilitySelector}
            value={selectedCapabilityValue}
            onChange={setSelectedCapabilityValue}
          />
          <EmployeeSelectorField
            employees={employees}
            employeeTemplates={employeeTemplates}
            departmentTemplates={departmentTemplates}
            departments={departments}
            capabilitySelector={capabilitySelector}
            value={selectedEmployeeId}
            onChange={setSelectedEmployeeId}
          />
          <button type="submit" className="h-10 w-fit rounded-ui-sm bg-ui-primary px-4 text-ui-3 font-bold text-ui-primary-fg disabled:opacity-50" disabled={loading}>
            创建任务
          </button>
        </form>

        {message ? <div className="mt-4 rounded-ui-sm bg-ui-surface p-3 text-ui-3 font-bold text-ui-txt-2 shadow-sm">{message}</div> : null}

        <section className="mt-6 grid gap-4 lg:grid-cols-[320px_minmax(0,1fr)]">
          <div>
            <h2 className="text-ui-3 font-black uppercase text-ui-txt-3">任务历史</h2>
            <div className="mt-3 space-y-2">
              {tasks.length ? (
                tasks.map((task) => (
                  <TaskHistoryItem
                    key={task.task_id}
                    task={task}
                    selectedTaskId={selectedTaskId}
                    loading={loading}
                    onSelect={() => loadTaskRecord(task)}
                    onRun={() => runTask(task.task_id)}
                  />
                ))
              ) : (
                <div className="rounded-ui-sm border border-dashed border-ui-line bg-ui-surface p-4 text-ui-3 font-bold text-ui-txt-3">尚未创建任务</div>
              )}
            </div>
          </div>

          <div className="min-w-0">
            <h2 className="text-ui-3 font-black uppercase text-ui-txt-3">选中任务详情</h2>
            {detailLoading ? (
              <div className="mt-3 rounded-ui-sm border border-ui-line bg-ui-surface p-6 text-ui-3 font-bold text-ui-txt-3 shadow-sm">正在加载任务证据</div>
            ) : selectedRecord ? (
              <TaskDetail record={selectedRecord} loading={loading} onRun={runTask} />
            ) : (
              <div className="mt-3 rounded-ui-sm border border-dashed border-ui-line bg-ui-surface p-6 text-center text-ui-3 font-bold text-ui-txt-3">尚未选择任务</div>
            )}
          </div>
        </section>
      </section>
    </main>
  );
}

function CompanyFoundationPanel({
  tasks,
  modelPreference,
  departmentCatalog,
  departmentCatalogLoading,
  departmentCatalogError,
  departmentActivation,
  departmentActivationSelection,
  departmentActivationLoading,
  departmentActivationSaving,
  departmentActivationError,
  departmentActivationMessage,
  onToggleDepartment,
  onSaveDepartmentActivation,
}) {
  const viewModel = buildCompanyFoundationViewModel({ tasks, modelPreference });
  const departmentSummary = buildDepartmentCatalogSummaryViewModel(departmentCatalog, {
    loading: departmentCatalogLoading,
    error: departmentCatalogError,
  });
  const activationPayload = departmentActivation
    ? { ...departmentActivation, active_department_type_keys: departmentActivationSelection }
    : departmentActivation;
  const activationSummary = buildDepartmentActivationViewModel(activationPayload, {
    loading: departmentActivationLoading,
    saving: departmentActivationSaving,
    error: departmentActivationError,
  });

  return (
    <section className="mt-5 rounded-ui-sm border border-ui-line bg-ui-surface p-4 shadow-sm">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h2 className="text-ui-3 font-black uppercase text-ui-txt-3">公司工作区</h2>
          <div className="mt-1 text-ui-5 font-black text-ui-txt">{viewModel.companyName}</div>
          <p className="mt-1 text-ui-3 text-ui-txt-2">{viewModel.workspaceLine}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {viewModel.signals.map((signal) => (
            <span key={signal} className="rounded-ui-sm border border-ui-line bg-ui-surface-2 px-2 py-1 text-ui-1 font-bold text-ui-txt-2">
              {signal}
            </span>
          ))}
        </div>
      </div>

      <div className="mt-4 grid gap-3 md:grid-cols-3">
        <div className="rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3">
          <div className="text-ui-1 font-bold text-ui-txt-3">本地首版</div>
          <div className="mt-1 text-ui-3 font-black text-ui-txt">{viewModel.releaseLine}</div>
        </div>
        <div className="rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3">
          <div className="text-ui-1 font-bold text-ui-txt-3">模型偏好</div>
          <div className="mt-1 text-ui-3 font-black text-ui-txt">{viewModel.modelLine}</div>
        </div>
        <div className="rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3">
          <div className="text-ui-1 font-bold text-ui-txt-3">执行入口</div>
          <div className="mt-1 text-ui-3 font-black text-ui-txt">{viewModel.taskLine}</div>
        </div>
      </div>

      <div className="mt-4 grid gap-2 md:grid-cols-3">
        {viewModel.sourceLinks.map((source) => (
          <a key={source.href} href={source.href} className="rounded-ui-sm border border-ui-line px-3 py-2 text-ui-3 font-bold text-ui-txt-2">
            {source.label}
          </a>
        ))}
      </div>

      <div className="mt-4 rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3">
        <div className="flex flex-wrap items-start justify-between gap-2">
          <div>
            <div className="text-ui-1 font-bold text-ui-txt-3">部门目录</div>
            <div className="mt-1 text-ui-3 font-black text-ui-txt">{departmentSummary.statusLine}</div>
            <div className="mt-1 text-ui-1 font-bold text-ui-txt-3">{departmentSummary.categoryLine}</div>
          </div>
          {departmentSummary.errorMessage ? <div className="text-ui-1 font-bold text-ui-red">{departmentSummary.errorMessage}</div> : null}
        </div>
        {departmentSummary.items.length ? (
          <div className="mt-3 grid gap-2 md:grid-cols-2">
            {departmentSummary.items.map((item) => (
              <div key={item.typeKey} className="rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2">
                <div className="text-ui-3 font-black text-ui-txt">{item.label}</div>
                <div className="mt-1 text-ui-1 font-bold text-ui-txt-3">
                  {item.category} · {item.typeKey}
                </div>
              </div>
            ))}
          </div>
        ) : null}
        {departmentSummary.empty ? <div className="mt-3 text-ui-3 font-bold text-ui-txt-3">尚未提供可展示的官方部门类型</div> : null}
      </div>

      <div className="mt-4 rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3">
        <div className="flex flex-wrap items-start justify-between gap-2">
          <div>
            <div className="text-ui-1 font-bold text-ui-txt-3">启用部门</div>
            <div className="mt-1 text-ui-3 font-black text-ui-txt">{activationSummary.statusLine}</div>
            <div className="mt-1 text-ui-1 font-bold text-ui-txt-3">{activationSummary.activeLine}</div>
          </div>
          <button
            type="button"
            className="rounded-ui-sm bg-ui-primary px-3 py-2 text-ui-1 font-bold text-ui-primary-fg disabled:opacity-50"
            onClick={onSaveDepartmentActivation}
            disabled={activationSummary.loading || activationSummary.saving || activationSummary.empty}
          >
            {activationSummary.saving ? "保存中" : "保存启用部门"}
          </button>
        </div>
        {activationSummary.options.length ? (
          <div className="mt-3 grid gap-2 md:grid-cols-2">
            {activationSummary.options.map((item) => (
              <label key={item.typeKey} className="flex items-start gap-2 rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-ui-3 font-bold text-ui-txt">
                <input
                  type="checkbox"
                  className="mt-1"
                  checked={departmentActivationSelection.includes(item.typeKey)}
                  onChange={() => onToggleDepartment(item.typeKey)}
                  disabled={activationSummary.loading || activationSummary.saving}
                />
                <span>
                  <span className="block text-ui-txt">{item.label}</span>
                  <span className="block text-ui-1 text-ui-txt-3">
                    {item.category} · {item.typeKey}
                  </span>
                </span>
              </label>
            ))}
          </div>
        ) : null}
        {activationSummary.empty ? <div className="mt-3 text-ui-3 font-bold text-ui-txt-3">尚未提供可启用的官方部门类型</div> : null}
        {activationSummary.errorMessage ? <div className="mt-3 text-ui-3 font-bold text-ui-red">{activationSummary.errorMessage}</div> : null}
        {departmentActivationMessage ? <div className="mt-3 text-ui-3 font-bold text-ui-txt-2">{departmentActivationMessage}</div> : null}
      </div>

    </section>
  );
}

function ModelPreferencePanel({ payload, selectedModelKey, loading, saving, message, onSelectModel, onSave, onReset }) {
  const viewModel = buildModelPreferenceViewModel(payload || {});
  const busy = loading || saving;
  const hasOptions = viewModel.options.length > 0;
  const canReset = Boolean(payload?.preference?.model_key);

  return (
    <section className="mt-5 rounded-ui-sm border border-ui-line bg-ui-surface p-4 shadow-sm">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h2 className="text-ui-3 font-black uppercase text-ui-txt-3">默认模型</h2>
          <p className="mt-1 text-ui-3 text-ui-txt-2">从已启用的官方模型中选择当前工作区默认模型。</p>
        </div>
        <div className="text-left md:text-right">
          <div className="text-ui-1 font-bold text-ui-txt-3">当前默认模型</div>
          <div className="mt-1 text-ui-3 font-black text-ui-txt">{loading ? "正在加载模型偏好" : viewModel.currentLabel}</div>
          <div className="mt-1 text-ui-1 font-bold text-ui-txt-3">{loading ? "请稍候" : viewModel.currentDetail}</div>
        </div>
      </div>

      <div className="mt-4 grid gap-3 md:grid-cols-[minmax(0,1fr)_auto_auto]">
        <label className="block text-ui-3 font-bold text-ui-txt-2">
          官方模型
          <select
            className="mt-1 h-10 w-full rounded-ui-sm border border-ui-line bg-ui-surface px-3 text-ui-3 font-normal disabled:bg-ui-bg"
            value={selectedModelKey}
            onChange={(event) => onSelectModel(event.target.value)}
            disabled={busy || !hasOptions}
          >
            <option value="" disabled>
              {hasOptions ? "请选择官方模型" : "尚未提供可选官方模型"}
            </option>
            {viewModel.options.map((model) => (
              <option key={model.modelKey} value={model.modelKey}>
                {model.label} - {model.detail}
              </option>
            ))}
          </select>
        </label>
        <button
          type="button"
          className="h-10 self-end rounded-ui-sm bg-ui-primary px-4 text-ui-3 font-bold text-ui-primary-fg disabled:opacity-50"
          onClick={onSave}
          disabled={busy || !selectedModelKey}
        >
          {saving ? "保存中" : "保存模型"}
        </button>
        <button
          type="button"
          className="h-10 self-end rounded-ui-sm border border-ui-line px-4 text-ui-3 font-bold text-ui-txt-2 disabled:opacity-50"
          onClick={onReset}
          disabled={busy || !canReset}
        >
          重置默认
        </button>
      </div>

      {message ? <div className="mt-3 rounded-ui-sm bg-ui-surface-2 px-3 py-2 text-ui-3 font-bold text-ui-txt-2">{message}</div> : null}
    </section>
  );
}

function PrivateCapabilitiesPanel({
  models,
  tools,
  connectors,
  loading,
  saving,
  message,
  modelForm,
  toolForm,
  connectorForm,
  onModelFormChange,
  onToolFormChange,
  onConnectorFormChange,
  onSaveModel,
  onSaveTool,
  onSaveConnector,
}) {
  const viewModel = buildPrivateCapabilitiesViewModel({ models, tools, connectors });
  return (
    <section className="mt-5 rounded-ui-sm border border-ui-line bg-ui-surface p-4 shadow-sm">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h2 className="text-ui-3 font-black uppercase text-ui-txt-3">私有能力</h2>
          <p className="mt-1 text-ui-3 text-ui-txt-2">为当前租户添加私有模型、工具和连接器；引用字段只填写 scheme:reference。</p>
        </div>
        <span className="rounded-ui-sm border border-ui-line bg-ui-surface-2 px-2 py-1 text-ui-1 font-bold text-ui-txt-2">
          tenant_private
        </span>
      </div>

      <div className="mt-4 grid gap-4 lg:grid-cols-3">
        <PrivateModelForm form={modelForm} saving={saving === "私有模型"} onChange={onModelFormChange} onSave={onSaveModel} />
        <PrivateToolForm form={toolForm} saving={saving === "私有工具"} onChange={onToolFormChange} onSave={onSaveTool} />
        <PrivateConnectorForm form={connectorForm} saving={saving === "私有连接器"} onChange={onConnectorFormChange} onSave={onSaveConnector} />
      </div>

      {message ? <div className="mt-3 rounded-ui-sm bg-ui-surface-2 px-3 py-2 text-ui-3 font-bold text-ui-txt-2">{message}</div> : null}

      <div className="mt-4 grid gap-3 md:grid-cols-3">
        <PrivateCapabilityList title="私有模型" loading={loading} items={viewModel.models} />
        <PrivateCapabilityList title="私有工具" loading={loading} items={viewModel.tools} />
        <PrivateCapabilityList title="私有连接器" loading={loading} items={viewModel.connectors} />
      </div>
    </section>
  );
}

function EmployeeSystemPanel({
  employeeTemplates,
  departmentTemplates,
  departments,
  employees,
  capabilitySelector,
  loading,
  saving,
  message,
  departmentForm,
  employeeForm,
  bindingForm,
  onDepartmentFormChange,
  onEmployeeFormChange,
  onBindingFormChange,
  onSaveDepartment,
  onSaveEmployee,
  onSaveBinding,
}) {
  const viewModel = buildEmployeeSystemViewModel({
    employeeTemplates,
    departmentTemplates,
    departments,
    employees,
    capabilitySelector,
  });
  return (
    <section className="mt-5 rounded-ui-sm border border-ui-line bg-ui-surface p-4 shadow-sm">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h2 className="text-ui-3 font-black uppercase text-ui-txt-3">研发部员工</h2>
          <p className="mt-1 text-ui-3 text-ui-txt-2">基于官方研发部模板创建租户内员工，并绑定 official / tenant_private 能力。</p>
        </div>
        <span className="rounded-ui-sm border border-ui-line bg-ui-surface-2 px-2 py-1 text-ui-1 font-bold text-ui-txt-2">
          {loading ? "加载中" : viewModel.summaryLine}
        </span>
      </div>

      <div className="mt-4 grid gap-4 lg:grid-cols-3">
        <div className="rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3">
          <div className="text-ui-3 font-black text-ui-txt">创建研发部</div>
          <SelectField
            label="department_template"
            value={departmentForm.template_id}
            options={viewModel.departmentTemplates.map((item) => ({ value: item.id, label: `${item.name} · ${item.source}` }))}
            onChange={(value) => onDepartmentFormChange({ ...departmentForm, template_id: value })}
          />
          <InputField label="name" value={departmentForm.name} onChange={(value) => onDepartmentFormChange({ ...departmentForm, name: value })} />
          <InputField label="company_id" value={departmentForm.company_id} onChange={(value) => onDepartmentFormChange({ ...departmentForm, company_id: value })} />
          <EnabledField checked={departmentForm.enabled} onChange={(value) => onDepartmentFormChange({ ...departmentForm, enabled: value })} />
          <SaveButton label={saving === "department" ? "保存中" : "创建研发部"} onClick={onSaveDepartment} disabled={saving === "department" || !departmentForm.template_id} />
        </div>

        <div className="rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3">
          <div className="text-ui-3 font-black text-ui-txt">创建员工</div>
          <SelectField
            label="department_id"
            value={employeeForm.department_id}
            options={viewModel.departments.map((item) => ({ value: item.id, label: `${item.name} · ${item.source}` }))}
            onChange={(value) => onEmployeeFormChange({ ...employeeForm, department_id: value })}
          />
          <SelectField
            label="template_id"
            value={employeeForm.template_id}
            options={viewModel.employeeTemplates.map((item) => ({ value: item.id, label: item.label }))}
            onChange={(value) => onEmployeeFormChange({ ...employeeForm, template_id: value })}
          />
          <InputField label="name" value={employeeForm.name} onChange={(value) => onEmployeeFormChange({ ...employeeForm, name: value })} />
          <InputField label="instructions_override" value={employeeForm.instructions_override} onChange={(value) => onEmployeeFormChange({ ...employeeForm, instructions_override: value })} />
          <EnabledField checked={employeeForm.enabled} onChange={(value) => onEmployeeFormChange({ ...employeeForm, enabled: value })} />
          <SaveButton label={saving === "employee" ? "保存中" : "创建员工"} onClick={onSaveEmployee} disabled={saving === "employee" || !employeeForm.department_id || !employeeForm.template_id} />
        </div>

        <div className="rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3">
          <div className="text-ui-3 font-black text-ui-txt">绑定能力</div>
          <SelectField
            label="employee_id"
            value={bindingForm.employee_id}
            options={viewModel.employeeOptions}
            onChange={(value) => onBindingFormChange({ ...bindingForm, employee_id: value })}
          />
          <SelectField
            label="capability"
            value={bindingForm.capability_value}
            options={viewModel.capabilityOptions.map((item) => ({ value: item.value, label: `${item.label} · ${item.detail}` }))}
            onChange={(value) => onBindingFormChange({ ...bindingForm, capability_value: value })}
          />
          <InputField label="priority" value={String(bindingForm.priority)} onChange={(value) => onBindingFormChange({ ...bindingForm, priority: value })} />
          <EnabledField checked={bindingForm.enabled} onChange={(value) => onBindingFormChange({ ...bindingForm, enabled: value })} />
          <SaveButton label={saving === "binding" ? "保存中" : "保存绑定"} onClick={onSaveBinding} disabled={saving === "binding" || !bindingForm.employee_id || !bindingForm.capability_value} />
        </div>
      </div>

      {message ? <div className="mt-3 rounded-ui-sm bg-ui-surface-2 px-3 py-2 text-ui-3 font-bold text-ui-txt-2">{message}</div> : null}

      <div className="mt-4 grid gap-3 md:grid-cols-3">
        <EmployeeList title="员工模板" items={viewModel.employeeTemplates} loading={loading} />
        <EmployeeList title="研发部实例" items={viewModel.departments} loading={loading} />
        <EmployeeList title="员工实例" items={viewModel.employees} loading={loading} />
      </div>
    </section>
  );
}

function WorkflowSystemPanel({
  templates,
  runs,
  selectedRun,
  departments,
  form,
  loading,
  saving,
  message,
  onFormChange,
  onCreate,
  onSelectRun,
  onRunNextStep,
}) {
  const workflowTemplates = (templates?.workflow_templates || []).filter((item) => item.source === "official" && item.status === "active");
  const departmentOptions = (departments?.departments || [])
    .filter((item) => item.enabled !== false)
    .map((item) => ({ value: item.id, label: `${item.name} · ${item.department_type}` }));
  const selectedView = selectedRun ? buildWorkflowRunViewModel(selectedRun) : null;

  return (
    <section className="mt-5 rounded-ui-sm border border-ui-line bg-ui-surface p-4 shadow-sm">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h2 className="text-ui-3 font-black uppercase text-ui-txt-3">研发 SOP 工作流</h2>
          <p className="mt-1 text-ui-3 text-ui-txt-2">第一版只执行 official 研发 SOP 顺序流程，不做 DAG 或流程编辑器。</p>
        </div>
        <span className="rounded-ui-sm bg-ui-bg px-2 py-1 text-ui-1 font-black text-ui-txt-2">Phase-6</span>
      </div>

      {message ? <div className="mt-3 rounded-ui-sm bg-ui-surface-2 p-2 text-ui-1 font-bold text-ui-txt-2">{message}</div> : null}

      <div className="mt-4 grid gap-3 lg:grid-cols-[minmax(0,1fr)_320px]">
        <div className="rounded-ui-sm border border-ui-line p-3">
          <div className="text-ui-1 font-black uppercase text-ui-txt-3">创建工作流运行</div>
          <div className="mt-3 grid gap-3 md:grid-cols-2">
            <SelectField
              label="workflow_template"
              value={form.workflow_template_id}
              options={workflowTemplates.map((item) => ({ value: item.id, label: item.name }))}
              onChange={(value) => onFormChange({ ...form, workflow_template_id: value })}
            />
            <SelectField
              label="department_id"
              value={form.department_id}
              options={departmentOptions}
              onChange={(value) => onFormChange({ ...form, department_id: value })}
            />
            <InputField label="name" value={form.name} onChange={(value) => onFormChange({ ...form, name: value })} />
            <label className="block text-ui-1 font-bold text-ui-txt-2 md:col-span-2">
              研发需求
              <textarea
                className="mt-1 min-h-20 w-full rounded-ui-sm border border-ui-line px-3 py-2 text-ui-3 font-normal"
                value={form.content}
                onChange={(event) => onFormChange({ ...form, content: event.target.value })}
              />
            </label>
          </div>
          <SaveButton label={saving === "create" ? "创建中" : "创建工作流"} onClick={onCreate} disabled={saving === "create" || !form.workflow_template_id || !form.department_id || !form.content} />
        </div>

        <div className="rounded-ui-sm border border-ui-line p-3">
          <div className="text-ui-1 font-black uppercase text-ui-txt-3">运行实例</div>
          <div className="mt-3 space-y-2">
            {(runs?.workflow_runs || []).length ? (
              runs.workflow_runs.map((run) => (
                <button
                  type="button"
                  key={run.workflow_run_id}
                  className="block w-full rounded-ui-sm border border-ui-line bg-ui-surface-2 p-2 text-left text-ui-1"
                  onClick={() => onSelectRun(run.workflow_run_id)}
                >
                  <span className="block font-black">{run.workflow_run_id}</span>
                  <span className="text-ui-txt-3">{run.status} · task={run.task_id}</span>
                </button>
              ))
            ) : (
              <div className="rounded-ui-sm border border-dashed border-ui-line p-3 text-ui-1 font-bold text-ui-txt-3">{loading ? "加载中" : "尚未创建运行实例"}</div>
            )}
          </div>
        </div>
      </div>

      {selectedView ? (
        <div className="mt-4 rounded-ui-sm border border-ui-line p-3">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div>
              <div className="text-ui-1 font-black text-ui-txt-3">{selectedView.workflowRunId}</div>
              <div className="mt-1 text-ui-3 font-black">{selectedView.statusLabel} · {selectedView.summaryLine}</div>
            </div>
            <SaveButton label={saving === "run" ? "执行中" : "执行下一步"} onClick={() => onRunNextStep(selectedView.workflowRunId)} disabled={saving === "run" || !selectedView.canRunNextStep} />
          </div>
          <div className="mt-3 grid gap-2 md:grid-cols-2">
            {selectedView.steps.map((step) => (
              <div key={step.id} className="rounded-ui-sm border border-ui-line p-3">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-ui-1 font-black text-ui-txt-3">#{step.order}</span>
                  <span className="rounded-ui-sm bg-ui-bg px-2 py-1 text-ui-1 font-bold text-ui-txt-2">{step.statusLabel}</span>
                </div>
                <div className="mt-2 text-ui-3 font-black">{step.name}</div>
                <div className="mt-1 text-ui-1 font-bold text-ui-txt-3">{step.ownerLine}</div>
                {step.output ? <pre className="mt-2 max-h-28 overflow-auto whitespace-pre-wrap rounded-ui-sm bg-ui-surface-2 border border-ui-line p-2 text-ui-1 text-ui-txt">{step.output}</pre> : null}
                {step.error ? <div className="mt-2 rounded-ui-sm bg-ui-surface-2 p-2 text-ui-1 font-bold text-ui-red">{step.error}</div> : null}
              </div>
            ))}
          </div>
          {selectedView.finalReport ? <pre className="mt-3 whitespace-pre-wrap rounded-ui-sm bg-ui-surface-2 border border-ui-line p-3 text-ui-3 text-ui-txt">{selectedView.finalReport}</pre> : null}
        </div>
      ) : null}
    </section>
  );
}

function EmployeeSelectorField({ employees, employeeTemplates, departmentTemplates, departments, capabilitySelector, value, onChange }) {
  const viewModel = buildEmployeeSystemViewModel({ employees, employeeTemplates, departmentTemplates, departments, capabilitySelector });
  return (
    <label className="block text-ui-3 font-bold text-ui-txt-2">
      执行员工
      <select
        className="mt-1 h-10 w-full rounded-ui-sm border border-ui-line bg-ui-surface px-3 text-ui-3 font-normal"
        value={value}
        onChange={(event) => onChange(event.target.value)}
      >
        <option value="">自动分配给 Tech Lead</option>
        {viewModel.employeeOptions.map((item) => (
          <option key={item.value} value={item.value}>
            {item.label} - {item.detail}
          </option>
        ))}
      </select>
      <span className="mt-1 block text-ui-1 font-bold text-ui-txt-3">未选择时由默认研发负责人接收。</span>
    </label>
  );
}

function EmployeeList({ title, items, loading }) {
  return (
    <div className="rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3">
      <div className="text-ui-1 font-bold text-ui-txt-3">{title}</div>
      {loading ? <div className="mt-2 text-ui-3 font-bold text-ui-txt-3">正在加载</div> : null}
      {!loading && !items.length ? <div className="mt-2 text-ui-3 font-bold text-ui-txt-3">尚未产生记录</div> : null}
      <div className="mt-2 space-y-2">
        {items.map((item) => (
          <div key={item.id} className="rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div className="text-ui-3 font-black text-ui-txt">{item.name}</div>
              <span className="rounded-ui-sm border border-ui-line bg-ui-surface-2 px-2 py-1 text-ui-1 font-bold text-ui-txt-2">{item.source}</span>
            </div>
            <div className="mt-1 text-ui-1 font-bold text-ui-txt-3">{item.role || item.departmentType || item.id}</div>
            {item.status ? <div className="mt-1 text-ui-1 font-bold text-ui-txt-2">{item.status}</div> : null}
          </div>
        ))}
      </div>
    </div>
  );
}

function PrivateModelForm({ form, saving, onChange, onSave }) {
  return (
    <div className="rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3">
      <div className="text-ui-3 font-black text-ui-txt">新增私有模型</div>
      <InputField label="name" value={form.name} onChange={(value) => onChange({ ...form, name: value })} />
      <InputField label="provider_type" value={form.provider_type} onChange={(value) => onChange({ ...form, provider_type: value })} />
      <InputField label="base_url" value={form.base_url} onChange={(value) => onChange({ ...form, base_url: value })} />
      <InputField label="model_name" value={form.model_name} onChange={(value) => onChange({ ...form, model_name: value })} />
      <InputField label="credential_ref" value={form.credential_ref} placeholder="env:TENANT_MODEL_KEY" onChange={(value) => onChange({ ...form, credential_ref: value })} />
      <EnabledField checked={form.enabled} onChange={(value) => onChange({ ...form, enabled: value })} />
      <SaveButton label={saving ? "保存中" : "添加模型"} onClick={onSave} disabled={saving} />
    </div>
  );
}

function PrivateToolForm({ form, saving, onChange, onSave }) {
  return (
    <div className="rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3">
      <div className="text-ui-3 font-black text-ui-txt">新增私有工具</div>
      <InputField label="name" value={form.name} onChange={(value) => onChange({ ...form, name: value })} />
      <InputField label="type" value={form.type} onChange={(value) => onChange({ ...form, type: value })} />
      <InputField label="description" value={form.description} onChange={(value) => onChange({ ...form, description: value })} />
      <InputField label="config_ref" value={form.config_ref} placeholder="env:TENANT_TOOL_CONFIG" onChange={(value) => onChange({ ...form, config_ref: value })} />
      <EnabledField checked={form.enabled} onChange={(value) => onChange({ ...form, enabled: value })} />
      <SaveButton label={saving ? "保存中" : "添加工具"} onClick={onSave} disabled={saving} />
    </div>
  );
}

function PrivateConnectorForm({ form, saving, onChange, onSave }) {
  return (
    <div className="rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3">
      <div className="text-ui-3 font-black text-ui-txt">新增私有连接器</div>
      <InputField label="name" value={form.name} onChange={(value) => onChange({ ...form, name: value })} />
      <InputField label="connector_type" value={form.connector_type} onChange={(value) => onChange({ ...form, connector_type: value })} />
      <InputField label="config_ref" value={form.config_ref} placeholder="env:TENANT_CONNECTOR_CONFIG" onChange={(value) => onChange({ ...form, config_ref: value })} />
      <EnabledField checked={form.enabled} onChange={(value) => onChange({ ...form, enabled: value })} />
      <SaveButton label={saving ? "保存中" : "添加连接器"} onClick={onSave} disabled={saving} />
    </div>
  );
}

function CapabilitySelectorField({ payload, value, onChange }) {
  const viewModel = buildCapabilitySelectorViewModel(payload || {});
  return (
    <label className="block text-ui-3 font-bold text-ui-txt-2">
      执行能力
      <select
        className="mt-1 h-10 w-full rounded-ui-sm border border-ui-line bg-ui-surface px-3 text-ui-3 font-normal"
        value={value}
        onChange={(event) => onChange(event.target.value)}
      >
        <option value="">自动选择能力</option>
        {viewModel.options.map((item) => (
          <option key={item.value} value={item.value}>
            {item.label} - {item.detail}
          </option>
        ))}
      </select>
      <span className="mt-1 block text-ui-1 font-bold text-ui-txt-3">清楚标记 source：official / tenant_private</span>
    </label>
  );
}

function PrivateCapabilityList({ title, loading, items }) {
  return (
    <div className="rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3">
      <div className="text-ui-1 font-bold text-ui-txt-3">{title}</div>
      {loading ? <div className="mt-2 text-ui-3 font-bold text-ui-txt-3">正在加载</div> : null}
      {!loading && !items.length ? <div className="mt-2 text-ui-3 font-bold text-ui-txt-3">尚未产生记录</div> : null}
      <div className="mt-2 space-y-2">
        {items.map((item) => (
          <div key={`${title}-${item.name}`} className="rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div className="text-ui-3 font-black text-ui-txt">{item.name}</div>
              <span className="rounded-ui-sm border border-ui-line bg-ui-surface-2 px-2 py-1 text-ui-1 font-bold text-ui-txt-2">{item.sourceLabel}</span>
            </div>
            <div className="mt-1 text-ui-1 font-bold text-ui-txt-3">{item.detail}</div>
            <div className="mt-1 text-ui-1 font-bold text-ui-txt-3">{item.reference}</div>
            <div className="mt-1 text-ui-1 font-bold text-ui-txt-2">{item.statusLabel}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function InputField({ label, value, placeholder = "", onChange }) {
  return (
    <label className="mt-3 block text-ui-1 font-bold text-ui-txt-2">
      {label}
      <input
        className="mt-1 h-9 w-full rounded-ui-sm border border-ui-line bg-ui-surface px-2 text-ui-3 font-normal text-ui-txt"
        value={value}
        placeholder={placeholder}
        onChange={(event) => onChange(event.target.value)}
      />
    </label>
  );
}

function SelectField({ label, value, options, onChange }) {
  return (
    <label className="mt-3 block text-ui-1 font-bold text-ui-txt-2">
      {label}
      <select
        className="mt-1 h-9 w-full rounded-ui-sm border border-ui-line bg-ui-surface px-2 text-ui-3 font-normal text-ui-txt"
        value={value}
        onChange={(event) => onChange(event.target.value)}
      >
        <option value="">请选择</option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </label>
  );
}

function EnabledField({ checked, onChange }) {
  return (
    <label className="mt-3 flex items-center gap-2 text-ui-1 font-bold text-ui-txt-2">
      <input type="checkbox" checked={checked} onChange={(event) => onChange(event.target.checked)} />
      enabled
    </label>
  );
}

function SaveButton({ label, onClick, disabled }) {
  return (
    <button
      type="button"
      className="mt-3 h-9 rounded-ui-sm bg-ui-primary px-3 text-ui-1 font-bold text-ui-primary-fg disabled:opacity-50"
      onClick={onClick}
      disabled={disabled}
    >
      {label}
    </button>
  );
}

function TaskHistoryItem({ task, selectedTaskId, loading, onSelect, onRun }) {
  const state = buildConsoleTaskState({ task, selectedTaskId });
  const reviewSignals = state.reviewSignals.length ? state.reviewSignals : buildReviewSignals({ task });
  const borderClass = state.isSelected ? "border-ui-primary" : "border-ui-line";

  return (
    <article className={`rounded-ui-sm border ${borderClass} bg-ui-surface p-3 shadow-sm`}>
      <button type="button" className="block w-full text-left" onClick={onSelect}>
        <div className="text-ui-3 font-black">{task.content}</div>
        <div className="mt-1 flex flex-wrap items-center gap-2">
          <span className="text-ui-1 font-bold text-ui-txt-3">{formatStatus(task.status)}</span>
          {state.isSelected ? <span className="text-ui-1 font-black text-ui-txt">已选中</span> : null}
        </div>
        {reviewSignals.length ? <SignalList signals={reviewSignals} /> : null}
      </button>
      {task.status !== "COMPLETED" ? (
        <button type="button" className="mt-3 rounded-ui-sm bg-ui-primary px-3 py-2 text-ui-2 font-bold text-ui-primary-fg disabled:opacity-50" onClick={onRun} disabled={loading || !state.canRun}>
          {state.runLabel}
        </button>
      ) : null}
    </article>
  );
}

async function fetchJson(path) {
  const response = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.detail || `加载失败：${path}`);
  return payload;
}

async function fetchOptionalJson(path, fallback = null) {
  const response = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
  if (response.status === 404) return fallback;
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.detail || `加载失败：${path}`);
  return payload;
}

function apiHeaders(extra = {}) {
  return {
    "X-Tenant-Id": WORKSPACE_TENANT_ID,
    "X-Ceo-Id": WORKSPACE_CEO_ID,
    ...extra,
  };
}

function TaskDetail({ record, loading, onRun }) {
  const { task, workflow, metaDevelopment, evolutionDecision } = record;
  const labels = buildOperatingLabels(record);
  const summary = buildExecutionSummary(record);
  const consoleState = buildConsoleTaskState({
    task,
    selectedTaskId: task.task_id,
    workflow,
    metaDevelopment,
    evolutionDecision,
  });
  const timeline = buildWorkflowTimeline(workflow || {});
  const fallbackEvents = buildFallbackEvents(record.trace || []);
  const metaSummary = buildMetaDevelopmentSummary(record.metaDevelopment);
  const evolutionSummary = buildEvolutionDecisionSummary(record.evolutionDecision);

  return (
    <article className="mt-3 space-y-3">
      <section className="rounded-ui-sm border border-ui-line bg-ui-surface p-4 shadow-sm">
        <div className="text-ui-1 font-bold text-ui-txt-3">{task.task_id}</div>
        <div className="mt-2 flex flex-wrap items-start justify-between gap-3">
          <div>
            <div className="text-ui-5 font-black">{summary.statusLine}</div>
            <div className="mt-2 flex flex-wrap items-center gap-2">
              {labels.map((label) => (
                <span key={label} className="rounded-ui-sm border border-ui-line bg-ui-surface-2 px-2 py-1 text-ui-1 font-bold text-ui-txt-2">
                  {label}
                </span>
              ))}
            </div>
          </div>
          <button type="button" className="rounded-ui-sm bg-ui-primary px-3 py-2 text-ui-2 font-bold text-ui-primary-fg disabled:opacity-50" onClick={() => onRun(task.task_id)} disabled={loading || !consoleState.canRun}>
            {consoleState.runLabel}
          </button>
        </div>
        {consoleState.reviewSignals.length ? <SignalList signals={consoleState.reviewSignals} /> : null}
        <div className="mt-3 grid gap-2 text-ui-3 text-ui-txt-2 md:grid-cols-2">
          <div>{summary.workflowLine}</div>
          <div>{summary.toolLine}</div>
          <div>{summary.learningLine}</div>
          <div>{summary.evolutionLine}</div>
        </div>
        <div className="mt-2 text-ui-1 text-ui-txt-3">{(task.state_flow || []).join(" → ")}</div>
        {task.output ? <pre className="mt-3 max-h-64 overflow-auto whitespace-pre-wrap rounded-ui-sm bg-ui-surface-2 border border-ui-line p-3 text-ui-2 text-ui-txt">{task.output}</pre> : null}
        <div className="mt-3 text-ui-1 font-bold text-ui-txt-3">成本：${Number(task.cost || 0).toFixed(6)}</div>
      </section>

      <DetailSection title="工作流时间线" empty={!timeline.length}>
        <div className="space-y-2">
          {timeline.map((step) => (
            <div key={`${step.step}-${step.action}`} className="rounded-ui-sm border border-ui-line p-3">
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-ui-1 font-black text-ui-txt-3">步骤 {step.step}</span>
                <span className="text-ui-3 font-black">{step.action}</span>
                <span className="rounded-ui-sm bg-ui-bg px-2 py-1 text-ui-1 font-bold text-ui-txt-2">{step.status}</span>
              </div>
              <div className="mt-2 text-ui-3 text-ui-txt-2">{step.purpose}</div>
              <div className="mt-2 grid gap-2 text-ui-1 text-ui-txt-3 sm:grid-cols-2">
                <div>所需工具：{step.requiredTool || "无"}</div>
                <div>预期输出：{step.expectedOutput || "无"}</div>
              </div>
            </div>
          ))}
        </div>
      </DetailSection>

      <DetailSection title="工具追踪与降级" empty={!record.trace.length && !fallbackEvents.length}>
        {fallbackEvents.length ? (
          <div className="mb-3 space-y-2">
            {fallbackEvents.map((event) => (
              <div key={`${event.step}-${event.fromTool}-${event.toTool}`} className="rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3 text-ui-3 text-ui-amber">
                步骤 {event.step}：{event.fromTool} 降级到 {event.toTool}。{event.error}
              </div>
            ))}
          </div>
        ) : null}
        <div className="space-y-2">
          {(record.trace || []).map((item, index) => (
            <div key={`${item.step_index}-${item.tool_name}-${index}`} className="rounded-ui-sm border border-ui-line p-3 text-ui-3">
              <div className="font-bold">
                步骤 {item.step_index} · {item.tool_name}
              </div>
              {item.error ? <div className="mt-1 text-ui-red">{item.error}</div> : <div className="mt-1 text-ui-txt-2">成功</div>}
            </div>
          ))}
        </div>
      </DetailSection>

      <DetailSection title="学习与元开发" empty={!metaDevelopment}>
        {metaDevelopment ? <EvidenceSummary items={metaSummary} details={metaDevelopment} /> : null}
      </DetailSection>

      <DetailSection title="演进决策" empty={!evolutionDecision}>
        {evolutionDecision ? <EvidenceSummary items={evolutionSummary} details={evolutionDecision} /> : null}
      </DetailSection>
    </article>
  );
}

function SignalList({ signals }) {
  return (
    <div className="mt-2 flex flex-wrap gap-2">
      {signals.map((signal) => (
        <span key={signal} className="rounded-ui-sm border border-ui-line bg-ui-surface-2 px-2 py-1 text-ui-1 font-bold text-ui-txt-2">
          {signal}
        </span>
      ))}
    </div>
  );
}

function DetailSection({ title, empty, children }) {
  return (
    <section className="rounded-ui-sm border border-ui-line bg-ui-surface p-4 shadow-sm">
      <h3 className="text-ui-3 font-black uppercase text-ui-txt-3">{title}</h3>
      {empty ? <div className="mt-3 text-ui-3 font-bold text-ui-txt-3">尚未产生记录</div> : <div className="mt-3">{children}</div>}
    </section>
  );
}

function JsonBlock({ value }) {
  return <pre className="max-h-72 overflow-auto whitespace-pre-wrap rounded-ui-sm bg-ui-surface-2 p-3 text-ui-1 text-ui-txt-2">{JSON.stringify(value, null, 2)}</pre>;
}

function EvidenceSummary({ items, details }) {
  return (
    <div className="space-y-3">
      <ul className="space-y-2">
        {items.map((item) => (
          <li key={item} className="rounded-ui-sm border border-ui-line bg-ui-surface-2 px-3 py-2 text-ui-3 text-ui-txt-2">
            {item}
          </li>
        ))}
      </ul>
      <details className="rounded-ui-sm border border-ui-line p-3">
        <summary className="cursor-pointer text-ui-1 font-black uppercase text-ui-txt-3">查看原始记录</summary>
        <div className="mt-3">
          <JsonBlock value={details} />
        </div>
      </details>
    </div>
  );
}

function formatStatus(status) {
  const dictionary = {
    COMPLETED: "已完成",
    RUNNING: "运行中",
    FAILED: "失败",
    PENDING: "等待中",
  };
  return dictionary[status] || status || "未知";
}
