import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import {
  TASK_ENTRY_STARTERS,
  buildCompanyFoundationViewModel,
  buildCapabilitySelectorViewModel,
  buildDepartmentInstancePayload,
  buildDepartmentActivationPayload,
  buildDepartmentActivationViewModel,
  buildDepartmentCatalogSummaryViewModel,
  buildEmployeeCapabilityBindingPayload,
  buildEmployeeInstancePayload,
  buildEmployeeSystemViewModel,
  buildPrivateConnectorPayload,
  buildPrivateModelPayload,
  buildPrivateToolPayload,
  buildPrivateCapabilitiesViewModel,
  buildTaskEntryDraft,
  buildConsoleTaskState,
  buildExecutionSummary,
  buildFallbackEvents,
  buildMetaDevelopmentSummary,
  buildModelPreferencePayload,
  buildModelPreferenceViewModel,
  buildOperatingLabels,
  buildTaskPayload,
  buildReviewSignals,
  buildEvolutionDecisionSummary,
  buildWorkflowRunViewModel,
  buildWorkflowTimeline,
} from "./taskViewModel.mjs";

test("buildOperatingLabels derives labels from persisted task, workflow, meta, and evolution records", () => {
  const labels = buildOperatingLabels({
    task: { status: "COMPLETED", output: "Done" },
    workflow: { status: "COMPLETED" },
    metaDevelopment: { report_id: 4 },
    evolutionDecision: { decision: "postpone_evolution" },
  });

  assert.deepEqual(labels, ["已完成", "结果已生成", "工作流已记录", "学习记录已生成", "演进已评估"]);
});

test("buildWorkflowTimeline preserves generated workflow order and derives step status", () => {
  const timeline = buildWorkflowTimeline({
    workflow_plan: [
      { step: 1, action: "analyze", purpose: "Understand", tool_required: "gpt_tool", expected_output: "Summary" },
      { step: 2, action: "validate", purpose: "Check", tool_required: "gpt_tool", expected_output: "Validation" },
    ],
    completed_steps: [1],
    failed_steps: [2],
    current_step: 2,
  });

  assert.deepEqual(timeline, [
    {
      step: 1,
      action: "analyze",
      purpose: "Understand",
      requiredTool: "gpt_tool",
      expectedOutput: "Summary",
      status: "已完成",
    },
    {
      step: 2,
      action: "validate",
      purpose: "Check",
      requiredTool: "gpt_tool",
      expectedOutput: "Validation",
      status: "失败",
    },
  ]);
});

test("buildFallbackEvents reports failed tool attempts followed by successful fallback", () => {
  const events = buildFallbackEvents([
    { step_index: 1, tool_name: "codex_tool", error: "primary failed" },
    { step_index: 1, tool_name: "gpt_tool", error: null },
    { step_index: 2, tool_name: "gpt_tool", error: null },
  ]);

  assert.deepEqual(events, [
    {
      step: 1,
      fromTool: "codex_tool",
      toTool: "gpt_tool",
      error: "primary failed",
    },
  ]);
});

test("buildExecutionSummary tells a CEO-readable task story from persisted execution state", () => {
  const summary = buildExecutionSummary({
    task: { status: "COMPLETED", selected_tool: "gpt_tool", state_flow: ["INIT", "PARSED", "RUNNING", "COMPLETED"], output: "Done" },
    workflow: { workflow_plan: [{ step: 1 }, { step: 2 }], completed_steps: [1, 2] },
    trace: [{ step_index: 1, tool_name: "gpt_tool" }, { step_index: 2, tool_name: "codex_tool" }],
    metaDevelopment: { report_id: 1 },
    evolutionDecision: { decision: "do_not_evolve" },
  });

  assert.deepEqual(summary, {
    statusLine: "已完成，结果已生成",
    workflowLine: "已记录 2 个工作流步骤，已完成 2 个",
    toolLine: "最近选择工具：gpt_tool；2 条工具追踪记录",
    learningLine: "学习报告已记录",
    evolutionLine: "演进决策：不演进",
  });
});

test("buildMetaDevelopmentSummary makes report evidence readable before raw details", () => {
  const summary = buildMetaDevelopmentSummary({
    gap_analysis: {
      task_signature: "ui_api",
      status: "ready_for_review",
      detected_gaps: ["workflow_length", "codex_overuse"],
    },
    planned_issues: [{ title: "Review generated execution output" }],
    verification_plan: ["Frontend lint", "Scope drift scan"],
  });

  assert.deepEqual(summary, [
    "任务模式：ui_api",
    "评审状态：准备评审",
    "发现缺口：工作流长度、Codex 过度使用",
    "计划跟进项：1",
    "验证项：2",
  ]);
});

test("buildEvolutionDecisionSummary explains policy, decision, risk, and proposal record", () => {
  const summary = buildEvolutionDecisionSummary({
    decision: "postpone_evolution",
    policy: ["STABILITY", "OPTIMIZATION", "EVOLUTION"],
    proposal: { target_module: "workflow_optimizer", requires_approval: true },
    risk_analysis: {
      stability_risk: { level: "low" },
      locked_module_risk: { blocked: true },
      rollback_risk: { level: "controlled" },
    },
  });

  assert.deepEqual(summary, [
    "决策：暂缓演进",
    "策略：稳定性 > 优化 > 演进",
    "提案记录：workflow_optimizer；需要审批",
    "风险：稳定性 低；锁定模块 被阻止；回滚 受控",
    "不会自动应用代码变更。",
  ]);
});

test("buildReviewSignals derives review signals only from existing execution records", () => {
  const signals = buildReviewSignals({
    task: { status: "FAILED", error: "tool failed", output: "partial result" },
    workflow: { failed_steps: [2] },
    metaDevelopment: { report_id: 3 },
    evolutionDecision: {
      decision: "postpone_evolution",
      proposal: { requires_approval: true },
    },
  });

  assert.deepEqual(signals, ["需要复核", "结果已生成", "学习记录已生成", "演进已评估", "需要用户决策"]);
});

test("buildConsoleTaskState keeps selected-task run control derived from task state", () => {
  const state = buildConsoleTaskState({
    task: { task_id: "task-1", status: "COMPLETED", output: "Done" },
    selectedTaskId: "task-1",
  });

  assert.deepEqual(state, {
    isSelected: true,
    canRun: true,
    runLabel: "再次运行",
    reviewSignals: ["结果已生成"],
  });
});

test("buildReviewSignals does not show running once a task completed", () => {
  const signals = buildReviewSignals({
    task: { status: "COMPLETED", output: "Done" },
    workflow: { current_step: 1, completed_steps: [1] },
  });

  assert.deepEqual(signals, ["结果已生成"]);
});

test("task entry starters are bounded to ordinary task content", () => {
  assert.equal(TASK_ENTRY_STARTERS.length, 3);

  for (const starter of TASK_ENTRY_STARTERS) {
    assert.deepEqual(Object.keys(starter).sort(), ["description", "id", "label", "prefill"].sort());
    assert.equal(typeof starter.prefill, "string");
    assert.doesNotMatch(starter.prefill, /task_type|role_id|entry_kind/i);
  }
});

test("buildTaskEntryDraft returns local composer content only", () => {
  const draft = buildTaskEntryDraft("review-execution");

  assert.deepEqual(Object.keys(draft), ["content"]);
  assert.match(draft.content, /复盘最新任务执行证据/);
  assert.doesNotMatch(JSON.stringify(draft), /task_type|role_id|entry_kind/i);
});

test("buildTaskPayload preserves existing Task API shape", () => {
  assert.deepEqual(buildTaskPayload("Summarize current execution evidence"), {
    content: "Summarize current execution evidence",
  });
});

test("buildTaskPayload includes selected capability only when explicitly selected", () => {
  const capability = {
    capabilitySource: "tenant_private",
    capabilityType: "tool",
    capabilityId: "tenant-writer",
  };
  assert.deepEqual(buildTaskPayload("Run with tenant tool", capability), {
    content: "Run with tenant tool",
    capability_source: "tenant_private",
    capability_type: "tool",
    capability_id: "tenant-writer",
  });
  assert.deepEqual(buildTaskPayload("Run with tenant tool", capability, "emp-1"), {
    content: "Run with tenant tool",
    capability_source: "tenant_private",
    capability_type: "tool",
    capability_id: "tenant-writer",
    employee_id: "emp-1",
  });
});

test("employee system view model keeps templates, instances, and capabilities separated", () => {
  const viewModel = buildEmployeeSystemViewModel({
    employeeTemplates: {
      employee_templates: [
        {
          id: "official.employee.tech_lead",
          name: "Tech Lead",
          role: "tech_lead",
          source: "official",
          department_type: "software_rnd",
          enabled: true,
        },
      ],
    },
    departmentTemplates: {
      department_templates: [
        {
          id: "official.department.software_rnd",
          name: "研发部",
          department_type: "software_rnd",
          source: "official",
          default_employee_templates: ["official.employee.tech_lead"],
          enabled: true,
        },
      ],
    },
    departments: {
      departments: [
        { id: "dept-1", name: "研发部", department_type: "software_rnd", source: "tenant_private", enabled: true },
      ],
    },
    employees: {
      employees: [
        { id: "emp-1", name: "技术负责人", role: "tech_lead", department_id: "dept-1", source: "tenant_private", status: "idle", enabled: true },
      ],
    },
    capabilitySelector: {
      capabilities: [
        { source: "official", capability_type: "model", capability_id: "official.newapi.default", label: "默认模型", enabled: true },
      ],
    },
  });

  assert.equal(viewModel.summaryLine, "研发部模板 1 个，员工实例 1 个");
  assert.equal(viewModel.employeeOptions[0].value, "emp-1");
  assert.equal(viewModel.capabilityOptions[0].capabilitySource, "official");
});

test("employee system payload builders keep contract field shape", () => {
  assert.deepEqual(
    buildDepartmentInstancePayload({
      template_id: "official.department.software_rnd",
      name: "研发部",
      company_id: "local-demo-company",
      enabled_employee_template_ids: ["official.employee.tech_lead"],
      enabled: true,
    }),
    {
      template_id: "official.department.software_rnd",
      name: "研发部",
      company_id: "local-demo-company",
      enabled_employee_template_ids: ["official.employee.tech_lead"],
      enabled: true,
    },
  );
  assert.deepEqual(
    buildEmployeeInstancePayload({
      department_id: "dept-1",
      template_id: "official.employee.tech_lead",
      name: "技术负责人",
      instructions_override: "拆解任务",
    }),
    {
      department_id: "dept-1",
      template_id: "official.employee.tech_lead",
      name: "技术负责人",
      company_id: "local-demo-company",
      instructions_override: "拆解任务",
      status: "idle",
      enabled: true,
    },
  );
  assert.deepEqual(
    buildEmployeeCapabilityBindingPayload(
      { priority: 5, enabled: true },
      { capabilitySource: "tenant_private", capabilityType: "tool", capabilityId: "tenant-writer" },
    ),
    {
      bindings: [
        {
          capability_source: "tenant_private",
          capability_type: "tool",
          capability_id: "tenant-writer",
          priority: 5,
          enabled: true,
        },
      ],
    },
  );
});

test("private capability payload builders keep reference placeholders and reject secret-like input", () => {
  assert.deepEqual(
    buildPrivateModelPayload({
      name: "tenant-deepseek",
      provider_type: "newapi-compatible",
      base_url: "https://tenant-gateway.example.com",
      model_name: "tenant-model-a",
      credential_ref: "env:TENANT_MODEL_KEY",
      enabled: true,
    }),
    {
      name: "tenant-deepseek",
      provider_type: "newapi-compatible",
      base_url: "https://tenant-gateway.example.com",
      model_name: "tenant-model-a",
      credential_ref: "env:TENANT_MODEL_KEY",
      enabled: true,
    },
  );
  assert.deepEqual(
    buildPrivateToolPayload({
      name: "tenant-writer",
      type: "llm_tool",
      description: "Tenant writing tool",
      config_ref: "vault:TENANT_TOOL_CONFIG",
      enabled: false,
    }),
    {
      name: "tenant-writer",
      type: "llm_tool",
      description: "Tenant writing tool",
      config_ref: "vault:TENANT_TOOL_CONFIG",
      enabled: false,
    },
  );
  assert.deepEqual(
    buildPrivateConnectorPayload({
      name: "tenant-crm",
      connector_type: "crm",
      config_ref: "kms:TENANT_CRM_CONFIG",
      enabled: true,
    }),
    {
      name: "tenant-crm",
      connector_type: "crm",
      config_ref: "kms:TENANT_CRM_CONFIG",
      enabled: true,
    },
  );
  assert.throws(
    () => buildPrivateModelPayload({
      name: "bad",
      provider_type: "newapi-compatible",
      base_url: "https://tenant-gateway.example.com",
      model_name: "tenant-model-a",
      credential_ref: "sk-real-secret-value-123456",
      enabled: true,
    }),
    /scheme:reference/,
  );
});

test("buildPrivateCapabilitiesViewModel groups tenant private capability lists without official pollution", () => {
  const viewModel = buildPrivateCapabilitiesViewModel({
    models: {
      models: [
        {
          tenant_id: "tenant-a",
          name: "tenant-deepseek",
          provider_type: "newapi-compatible",
          base_url: "https://tenant-gateway.example.com",
          model_name: "tenant-model-a",
          credential_ref: "env:TENANT_MODEL_KEY",
          enabled: true,
          source: "tenant_private",
        },
      ],
    },
    tools: {
      tools: [
        {
          tenant_id: "tenant-a",
          name: "tenant-writer",
          type: "llm_tool",
          description: "Tenant writing tool",
          config_ref: "env:TENANT_TOOL_CONFIG",
          enabled: true,
          source: "tenant_private",
        },
      ],
    },
    connectors: {
      connectors: [
        {
          tenant_id: "tenant-a",
          name: "tenant-crm",
          connector_type: "crm",
          config_ref: "env:TENANT_CRM_CONFIG",
          enabled: false,
          source: "tenant_private",
        },
      ],
    },
  });

  assert.deepEqual(viewModel.models[0].sourceLabel, "tenant_private");
  assert.deepEqual(viewModel.tools[0].sourceLabel, "tenant_private");
  assert.deepEqual(viewModel.connectors[0].statusLabel, "已停用");
  assert.doesNotMatch(JSON.stringify(viewModel), /source":"official|sk-real/i);
});

test("buildPrivateCapabilitiesViewModel handles unloaded capability state", () => {
  assert.deepEqual(
    buildPrivateCapabilitiesViewModel({ models: null, tools: null, connectors: null }),
    { models: [], tools: [], connectors: [] },
  );
});

test("buildCapabilitySelectorViewModel keeps official and tenant private options clearly labeled", () => {
  const viewModel = buildCapabilitySelectorViewModel({
    capabilities: [
      {
        capability_id: "model_gateway_tool",
        capability_type: "tool",
        label: "Model Gateway execution",
        source: "official",
        enabled: true,
      },
      {
        capability_id: "tenant-writer",
        capability_type: "tool",
        label: "tenant-writer",
        source: "tenant_private",
        enabled: true,
      },
    ],
  });

  assert.deepEqual(viewModel.options, [
    {
      value: "official|tool|model_gateway_tool",
      label: "Model Gateway execution",
      detail: "official / tool / model_gateway_tool",
      capabilitySource: "official",
      capabilityType: "tool",
      capabilityId: "model_gateway_tool",
    },
    {
      value: "tenant_private|tool|tenant-writer",
      label: "tenant-writer",
      detail: "tenant_private / tool / tenant-writer",
      capabilitySource: "tenant_private",
      capabilityType: "tool",
      capabilityId: "tenant-writer",
    },
  ]);
});

test("buildModelPreferenceViewModel exposes official model choices without secret metadata", () => {
  const viewModel = buildModelPreferenceViewModel({
    preference: {
      model_key: "official:gpt-4.1-mini",
      display_name: "GPT-4.1 Mini",
      provider_id: "openai",
      gateway_ref: "newapi:gpt-4.1-mini",
      source: "official",
    },
    available_models: [
      {
        model_key: "official:gpt-4.1-mini",
        display_name: "GPT-4.1 Mini",
        provider_id: "openai",
        gateway_ref: "newapi:gpt-4.1-mini",
        model_name: "gpt-4.1-mini",
        source: "official",
        status: "active",
        credential_ref: "must-not-render",
      },
      {
        model_key: "custom:blocked",
        display_name: "Blocked",
        provider_id: "other",
        gateway_ref: "blocked",
        source: "tenant",
        status: "active",
      },
    ],
  });

  assert.deepEqual(viewModel, {
    currentLabel: "GPT-4.1 Mini",
    currentDetail: "openai / gpt-4.1-mini",
    selectedModelKey: "official:gpt-4.1-mini",
    options: [
      {
        modelKey: "official:gpt-4.1-mini",
        label: "GPT-4.1 Mini",
        detail: "openai / gpt-4.1-mini",
      },
    ],
  });
  assert.doesNotMatch(JSON.stringify(viewModel), /credential_ref|must-not-render/i);
});

test("buildModelPreferencePayload keeps the existing preference API shape", () => {
  assert.deepEqual(buildModelPreferencePayload("official:gpt-4.1-mini"), {
    model_key: "official:gpt-4.1-mini",
  });
});

test("buildCompanyFoundationViewModel frames existing local workspace state without new behavior data", () => {
  const viewModel = buildCompanyFoundationViewModel({
    tasks: [
      { task_id: "task-1", status: "COMPLETED" },
      { task_id: "task-2", status: "PENDING" },
    ],
    modelPreference: {
      preference: {
        model_key: "official.newapi.default",
        display_name: "New API Default Model",
        provider_id: "newapi",
        gateway_ref: "newapi",
        model_name: "newapi-default",
        source: "official",
        credential_ref: "must-not-render",
      },
      available_models: [
        {
          model_key: "official.newapi.default",
          display_name: "New API Default Model",
          provider_id: "newapi",
          gateway_ref: "newapi",
          model_name: "newapi-default",
          source: "official",
          status: "active",
        },
      ],
    },
  });

  assert.deepEqual(viewModel, {
    companyName: "Curis 本地演示公司",
    workspaceLine: "本地演示 · 默认工作区",
    releaseLine: "模型网关本地首版已收口",
    modelLine: "默认模型：New API Default Model",
    taskLine: "任务台：2 个任务，1 个已完成",
    sourceLinks: [
      { label: "公司基础边界", href: "/docs/decisions/ADR-0031-workspace-company-foundation-boundaries.md" },
      { label: "项目记忆", href: "/knowledge/PROJECT_MEMORY.md" },
      { label: "首版收口记录", href: "/docs/release/model-gateway-local-demo-first-version-release-record.md" },
    ],
    signals: ["本地演示", "任务台", "模型偏好", "项目记忆"],
  });
  assert.doesNotMatch(JSON.stringify(viewModel), /credential_ref|must-not-render/i);
});

test("buildCompanyFoundationViewModel handles unloaded model preference state", () => {
  const viewModel = buildCompanyFoundationViewModel({
    tasks: [],
    modelPreference: null,
  });

  assert.equal(viewModel.modelLine, "默认模型：未设置默认模型");
  assert.equal(viewModel.taskLine, "任务台：0 个任务，0 个已完成");
});

test("buildDepartmentCatalogSummaryViewModel summarizes active official department types without secret metadata", () => {
  const viewModel = buildDepartmentCatalogSummaryViewModel({
    department_types: [
      {
        type_key: "business.general",
        category: "business",
        display_name: "业务部",
        source: "official",
        enabled: 1,
        credential_ref: "must-not-render",
      },
      {
        type_key: "function.hr",
        category: "function",
        display_name: "人事部",
        source: "official",
        enabled: 1,
      },
      {
        type_key: "tenant.custom",
        category: "business",
        display_name: "Custom",
        source: "tenant_private",
        enabled: 1,
      },
      {
        type_key: "function.disabled",
        category: "function",
        display_name: "Disabled",
        source: "official",
        enabled: 0,
      },
    ],
  });

  assert.deepEqual(viewModel, {
    statusLine: "已启用 2 个官方部门类型",
    categoryLine: "类别：业务型 1 个，职能型 1 个",
    items: [
      { typeKey: "business.general", label: "业务部", category: "业务型" },
      { typeKey: "function.hr", label: "人事部", category: "职能型" },
    ],
    empty: false,
    loading: false,
    errorMessage: "",
  });
  assert.doesNotMatch(JSON.stringify(viewModel), /credential_ref|must-not-render|tenant.custom|Disabled/i);
});

test("buildDepartmentCatalogSummaryViewModel reports loading, error, and empty states", () => {
  assert.deepEqual(buildDepartmentCatalogSummaryViewModel(null, { loading: true }), {
    statusLine: "正在加载部门目录",
    categoryLine: "类别：加载中",
    items: [],
    empty: false,
    loading: true,
    errorMessage: "",
  });

  assert.deepEqual(buildDepartmentCatalogSummaryViewModel(null, { error: "部门目录加载失败" }), {
    statusLine: "部门目录加载失败",
    categoryLine: "类别：暂不可用",
    items: [],
    empty: false,
    loading: false,
    errorMessage: "部门目录加载失败",
  });

  assert.deepEqual(buildDepartmentCatalogSummaryViewModel({ department_types: [] }), {
    statusLine: "暂无启用的官方部门类型",
    categoryLine: "类别：暂无",
    items: [],
    empty: true,
    loading: false,
    errorMessage: "",
  });
});

test("buildDepartmentActivationViewModel exposes active official department choices without secret metadata", () => {
  const viewModel = buildDepartmentActivationViewModel({
    active_department_type_keys: ["business.general"],
    department_types: [
      {
        type_key: "business.general",
        category: "business",
        display_name: "业务部",
        source: "official",
        enabled: true,
        credential_ref: "must-not-render",
      },
      {
        type_key: "function.hr",
        category: "function",
        display_name: "人事部",
        source: "official",
        enabled: false,
      },
      {
        type_key: "tenant.private",
        category: "business",
        display_name: "Private",
        source: "tenant_private",
        enabled: true,
      },
    ],
  });

  assert.deepEqual(viewModel, {
    statusLine: "已启用 1 个公司部门",
    activeLine: "已启用：业务部",
    selectedKeys: ["business.general"],
    options: [
      { typeKey: "business.general", label: "业务部", category: "业务型", checked: true },
      { typeKey: "function.hr", label: "人事部", category: "职能型", checked: false },
    ],
    empty: false,
    loading: false,
    saving: false,
    errorMessage: "",
  });
  assert.doesNotMatch(JSON.stringify(viewModel), /credential_ref|must-not-render|tenant.private|Private/i);
});

test("buildDepartmentActivationViewModel reports loading, saving, error, and empty states", () => {
  assert.deepEqual(buildDepartmentActivationViewModel(null, { loading: true }), {
    statusLine: "正在加载已启用部门",
    activeLine: "请稍候",
    selectedKeys: [],
    options: [],
    empty: false,
    loading: true,
    saving: false,
    errorMessage: "",
  });

  assert.deepEqual(buildDepartmentActivationViewModel(null, { saving: true }), {
    statusLine: "正在保存部门启用状态",
    activeLine: "请稍候",
    selectedKeys: [],
    options: [],
    empty: false,
    loading: false,
    saving: true,
    errorMessage: "",
  });

  assert.deepEqual(buildDepartmentActivationViewModel(null, { error: "部门启用状态加载失败" }), {
    statusLine: "部门启用状态加载失败",
    activeLine: "已启用部门暂不可用",
    selectedKeys: [],
    options: [],
    empty: false,
    loading: false,
    saving: false,
    errorMessage: "部门启用状态加载失败",
  });

  assert.deepEqual(buildDepartmentActivationViewModel({ active_department_type_keys: [], department_types: [] }), {
    statusLine: "尚未启用公司部门",
    activeLine: "可从官方部门类型中选择",
    selectedKeys: [],
    options: [],
    empty: true,
    loading: false,
    saving: false,
    errorMessage: "",
  });
});

test("buildDepartmentActivationPayload keeps the existing activation API shape", () => {
  assert.deepEqual(buildDepartmentActivationPayload(["business.general", "function.hr"]), {
    department_type_keys: ["business.general", "function.hr"],
  });
});

test("workspace page wires the department activation selector to existing APIs", () => {
  const pageSource = readFileSync(new URL("./page.js", import.meta.url), "utf8");

  assert.match(pageSource, /buildDepartmentActivationPayload/);
  assert.match(pageSource, /buildDepartmentActivationViewModel/);
  assert.match(pageSource, /\/api\/workspace\/departments\/activation/);
  assert.match(pageSource, /启用部门/);
  assert.doesNotMatch(pageSource, /task_type|role_id|entry_kind/i);
});

test("workspace page wires private capability UI without platform API calls", () => {
  const pageSource = readFileSync(new URL("./page.js", import.meta.url), "utf8");

  assert.match(pageSource, /\/api\/workspace\/private-models/);
  assert.match(pageSource, /\/api\/workspace\/private-tools/);
  assert.match(pageSource, /\/api\/workspace\/private-connectors/);
  assert.match(pageSource, /\/api\/workspace\/capabilities\/selector/);
  assert.match(pageSource, /私有能力/);
  assert.match(pageSource, /X-Ceo-Id/);
  assert.match(pageSource, /X-Tenant-Id/);
  assert.match(pageSource, /apiHeaders\(\)/);
  assert.doesNotMatch(pageSource, /\/api\/platform\//);
});

test("workflow run view model summarizes sequential SOP steps", () => {
  const viewModel = buildWorkflowRunViewModel({
    workflow_run_id: "wr-1",
    status: "running",
    final_report: "",
    steps: [
      {
        workflow_step_id: "ws-1",
        step_order: 1,
        step_name: "Tech Lead 拆解",
        employee_role: "tech_lead",
        employee_id: "emp-1",
        status: "succeeded",
        output: "拆解完成",
      },
      {
        workflow_step_id: "ws-2",
        step_order: 2,
        step_name: "Product Manager 补充需求",
        employee_role: "product_manager",
        employee_id: "emp-2",
        status: "pending",
        output: "",
      },
    ],
  });

  assert.equal(viewModel.statusLabel, "运行中");
  assert.equal(viewModel.summaryLine, "2 个步骤，1 个已完成");
  assert.equal(viewModel.canRunNextStep, true);
  assert.deepEqual(viewModel.steps.map((step) => step.ownerLine), [
    "tech_lead · emp-1",
    "product_manager · emp-2",
  ]);
});

test("workspace page wires workflow MVP APIs without platform runtime calls", () => {
  const pageSource = readFileSync(new URL("./page.js", import.meta.url), "utf8");

  assert.match(pageSource, /\/api\/workspace\/workflow-templates/);
  assert.match(pageSource, /\/api\/workspace\/workflows/);
  assert.match(pageSource, /run-next-step/);
  assert.doesNotMatch(pageSource, /\/api\/platform\//);
});
