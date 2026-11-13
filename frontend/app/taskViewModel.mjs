export const TASK_ENTRY_STARTERS = [
  {
    id: "plan-next-slice",
    label: "规划下一切片",
    description: "基于当前项目证据，准备边界清晰的实现计划。",
    prefill:
      "规划下一个已批准的 Curis 工作台实现切片。\n\n关注点：\n- 阅读当前 Issue 和已接受的边界证据。\n- 识别最小实现路径。\n- 列出验证命令和范围风险检查。\n- 如果工作会越过已批准的关口，请停止并说明。",
  },
  {
    id: "review-execution",
    label: "复盘执行结果",
    description: "检查已有任务运行，并总结可供评审的证据。",
    prefill:
      "复盘最新任务执行证据。\n\n关注点：\n- 总结状态、结果、工作流、工具追踪、学习记录和演进决策证据。\n- 识别阻塞项或缺失验证。\n- 建议必须保持在当前 AI 任务执行器 MVP 边界内。",
  },
  {
    id: "verify-boundary",
    label: "验证边界",
    description: "用已接受范围检查实现证据。",
    prefill:
      "根据已接受的 Issue 边界验证当前实现。\n\n关注点：\n- 确认变更文件符合允许范围。\n- 确认任务 API 载荷仍是普通任务内容。\n- 运行可用测试和范围漂移扫描。\n- 记录已知缺口和下一席位交接。",
  },
];

export function buildTaskEntryDraft(starterId) {
  const starter = TASK_ENTRY_STARTERS.find((item) => item.id === starterId);
  return {
    content: starter?.prefill || "",
  };
}

export function buildTaskPayload(content, capability = null, employeeId = "") {
  const payload = { content };
  if (capability?.capabilitySource && capability?.capabilityType && capability?.capabilityId) {
    payload.capability_source = capability.capabilitySource;
    payload.capability_type = capability.capabilityType;
    payload.capability_id = capability.capabilityId;
  }
  if (employeeId) {
    payload.employee_id = employeeId;
  }
  return payload;
}

export function buildModelPreferencePayload(modelKey) {
  return { model_key: modelKey };
}

export function buildDepartmentActivationPayload(departmentTypeKeys) {
  return { department_type_keys: departmentTypeKeys };
}

export function buildPrivateModelPayload(form = {}) {
  assertReferencePlaceholder(form.credential_ref, "credential_ref");
  return {
    name: clean(form.name),
    provider_type: clean(form.provider_type),
    base_url: clean(form.base_url),
    model_name: clean(form.model_name),
    credential_ref: clean(form.credential_ref),
    enabled: Boolean(form.enabled),
  };
}

export function buildPrivateToolPayload(form = {}) {
  assertReferencePlaceholder(form.config_ref, "config_ref");
  return {
    name: clean(form.name),
    type: clean(form.type),
    description: clean(form.description),
    config_ref: clean(form.config_ref),
    enabled: Boolean(form.enabled),
  };
}

export function buildPrivateConnectorPayload(form = {}) {
  assertReferencePlaceholder(form.config_ref, "config_ref");
  return {
    name: clean(form.name),
    connector_type: clean(form.connector_type),
    config_ref: clean(form.config_ref),
    enabled: Boolean(form.enabled),
  };
}

export function buildPrivateCapabilitiesViewModel({ models = {}, tools = {}, connectors = {} } = {}) {
  const safeModels = models || {};
  const safeTools = tools || {};
  const safeConnectors = connectors || {};

  return {
    models: (safeModels.models || []).filter(isTenantPrivate).map((item) => ({
      name: item.name,
      detail: `${item.provider_type || "provider"} / ${item.model_name || "model"}`,
      reference: item.credential_ref || "未设置引用",
      enabled: Boolean(item.enabled),
      statusLabel: item.enabled ? "已启用" : "已停用",
      sourceLabel: "tenant_private",
    })),
    tools: (safeTools.tools || []).filter(isTenantPrivate).map((item) => ({
      name: item.name,
      detail: `${item.type || "tool"} / ${item.description || "无描述"}`,
      reference: item.config_ref || "未设置引用",
      enabled: Boolean(item.enabled),
      statusLabel: item.enabled ? "已启用" : "已停用",
      sourceLabel: "tenant_private",
    })),
    connectors: (safeConnectors.connectors || []).filter(isTenantPrivate).map((item) => ({
      name: item.name,
      detail: item.connector_type || "connector",
      reference: item.config_ref || "未设置引用",
      enabled: Boolean(item.enabled),
      statusLabel: item.enabled ? "已启用" : "已停用",
      sourceLabel: "tenant_private",
    })),
  };
}

export function buildCapabilitySelectorViewModel(payload = {}) {
  const safePayload = payload || {};
  const options = (safePayload.capabilities || [])
    .filter((item) => item?.enabled !== false && (item?.source === "official" || item?.source === "tenant_private"))
    .map((item) => ({
      value: `${item.source}|${item.capability_type}|${item.capability_id}`,
      label: item.label || item.capability_id,
      detail: `${item.source} / ${item.capability_type} / ${item.capability_id}`,
      capabilitySource: item.source,
      capabilityType: item.capability_type,
      capabilityId: item.capability_id,
    }));
  return {
    options,
    empty: options.length === 0,
  };
}

export function buildEmployeeSystemViewModel({
  employeeTemplates = {},
  departmentTemplates = {},
  departments = {},
  employees = {},
  capabilitySelector = {},
} = {}) {
  const safeEmployeeTemplates = employeeTemplates || {};
  const safeDepartmentTemplates = departmentTemplates || {};
  const safeDepartments = departments || {};
  const safeEmployees = employees || {};
  const availableEmployeeTemplates = (safeEmployeeTemplates.employee_templates || [])
    .filter((item) => item?.enabled !== false && item?.department_type === "software_rnd")
    .map((item) => ({
      id: item.id,
      name: item.name,
      role: item.role,
      source: item.source,
      responsibility: item.responsibility || item.description || "",
      label: `${item.name} · ${item.role}`,
    }));
  const availableDepartmentTemplates = (safeDepartmentTemplates.department_templates || [])
    .filter((item) => item?.enabled !== false && item?.department_type === "software_rnd")
    .map((item) => ({
      id: item.id,
      name: item.name,
      departmentType: item.department_type,
      source: item.source,
      defaultEmployeeCount: (item.default_employee_templates || []).length,
    }));
  const departmentItems = (safeDepartments.departments || [])
    .filter((item) => item?.source === "tenant_private")
    .map((item) => ({
      id: item.id,
      name: item.name,
      departmentType: item.department_type,
      enabled: Boolean(item.enabled),
      source: item.source,
    }));
  const employeeItems = (safeEmployees.employees || [])
    .filter((item) => item?.source === "tenant_private")
    .map((item) => ({
      id: item.id,
      name: item.name,
      role: item.role,
      departmentId: item.department_id,
      enabled: Boolean(item.enabled),
      status: item.status || "idle",
      source: item.source,
      label: `${item.name} · ${item.role}`,
    }));
  const employeeOptions = employeeItems
    .filter((item) => item.enabled)
    .map((item) => ({
      value: item.id,
      label: item.label,
      detail: `${item.source} / ${item.status}`,
    }));
  return {
    employeeTemplates: availableEmployeeTemplates,
    departmentTemplates: availableDepartmentTemplates,
    departments: departmentItems,
    employees: employeeItems,
    employeeOptions,
    capabilityOptions: buildCapabilitySelectorViewModel(capabilitySelector).options,
    summaryLine: `研发部模板 ${availableEmployeeTemplates.length} 个，员工实例 ${employeeItems.length} 个`,
  };
}

export function buildDepartmentInstancePayload(form = {}) {
  return {
    template_id: clean(form.template_id),
    name: clean(form.name),
    company_id: clean(form.company_id || "local-demo-company"),
    enabled_employee_template_ids: form.enabled_employee_template_ids || [],
    enabled: Boolean(form.enabled ?? true),
  };
}

export function buildEmployeeInstancePayload(form = {}) {
  return {
    department_id: clean(form.department_id),
    template_id: clean(form.template_id),
    name: clean(form.name),
    company_id: clean(form.company_id || "local-demo-company"),
    instructions_override: clean(form.instructions_override),
    status: clean(form.status || "idle"),
    enabled: Boolean(form.enabled ?? true),
  };
}

export function buildEmployeeCapabilityBindingPayload(form = {}, selectedCapability = null) {
  if (!selectedCapability?.capabilitySource || !selectedCapability?.capabilityType || !selectedCapability?.capabilityId) {
    return { bindings: [] };
  }
  return {
    bindings: [
      {
        capability_source: selectedCapability.capabilitySource,
        capability_type: selectedCapability.capabilityType,
        capability_id: selectedCapability.capabilityId,
        priority: Number(form.priority || 100),
        enabled: Boolean(form.enabled ?? true),
      },
    ],
  };
}

export function buildWorkflowRunViewModel(workflow = {}) {
  const steps = (workflow?.steps || [])
    .slice()
    .sort((a, b) => Number(a.step_order || 0) - Number(b.step_order || 0))
    .map((step) => ({
      id: step.workflow_step_id || step.id,
      order: Number(step.step_order || 0),
      name: step.step_name || step.name || "未命名步骤",
      role: step.employee_role || "unknown",
      employeeId: step.employee_id || "",
      ownerLine: `${step.employee_role || "unknown"} · ${step.employee_id || "未分配"}`,
      status: step.status || "pending",
      statusLabel: translateWorkflowStatus(step.status || "pending"),
      output: step.output || "",
      error: step.error || "",
    }));
  const completed = steps.filter((step) => step.status === "succeeded").length;
  const status = workflow?.status || "pending";
  return {
    workflowRunId: workflow?.workflow_run_id || "",
    status,
    statusLabel: translateWorkflowStatus(status),
    summaryLine: `${steps.length} 个步骤，${completed} 个已完成`,
    canRunNextStep: ["pending", "running"].includes(status),
    finalReport: workflow?.final_report || "",
    steps,
  };
}

export function buildModelPreferenceViewModel(payload = {}) {
  const officialModels = (payload.available_models || []).filter((model) => model?.source === "official" && model?.status === "active");
  const selectedModelKey = payload.preference?.model_key || "";
  const selectedModel = officialModels.find((model) => model.model_key === selectedModelKey) || payload.preference || null;
  return {
    currentLabel: selectedModel ? modelDisplayName(selectedModel) : "未设置默认模型",
    currentDetail: selectedModel ? modelDetail(selectedModel) : "将使用系统当前默认模型",
    selectedModelKey,
    options: officialModels.map((model) => ({
      modelKey: model.model_key,
      label: modelDisplayName(model),
      detail: modelDetail(model),
    })),
  };
}

export function buildCompanyFoundationViewModel({ tasks = [], modelPreference = {} } = {}) {
  const modelView = buildModelPreferenceViewModel(modelPreference || {});
  const completedTasks = tasks.filter((task) => task?.status === "COMPLETED").length;
  return {
    companyName: "Curis 本地演示公司",
    workspaceLine: "本地演示 · 默认工作区",
    releaseLine: "模型网关本地首版已收口",
    modelLine: `默认模型：${modelView.currentLabel}`,
    taskLine: `任务台：${tasks.length} 个任务，${completedTasks} 个已完成`,
    sourceLinks: [
      { label: "公司基础边界", href: "/docs/decisions/ADR-0031-workspace-company-foundation-boundaries.md" },
      { label: "项目记忆", href: "/knowledge/PROJECT_MEMORY.md" },
      { label: "首版收口记录", href: "/docs/release/model-gateway-local-demo-first-version-release-record.md" },
    ],
    signals: ["本地演示", "任务台", "模型偏好", "项目记忆"],
  };
}

export function buildDepartmentCatalogSummaryViewModel(payload = {}, { loading = false, error = "" } = {}) {
  if (loading) {
    return {
      statusLine: "正在加载部门目录",
      categoryLine: "类别：加载中",
      items: [],
      empty: false,
      loading: true,
      errorMessage: "",
    };
  }

  if (error) {
    return {
      statusLine: "部门目录加载失败",
      categoryLine: "类别：暂不可用",
      items: [],
      empty: false,
      loading: false,
      errorMessage: error,
    };
  }

  const activeOfficialTypes = (payload?.department_types || [])
    .filter((type) => type?.source === "official" && Number(type?.enabled ?? 1) === 1)
    .map((type) => ({
      typeKey: type.type_key,
      label: type.display_name || type.type_key || "未命名部门类型",
      category: departmentCategoryLabel(type.category),
    }));
  const categoryCounts = activeOfficialTypes.reduce((counts, type) => {
    counts.set(type.category, (counts.get(type.category) || 0) + 1);
    return counts;
  }, new Map());
  const categoryLine = activeOfficialTypes.length
    ? `类别：${Array.from(categoryCounts.entries()).map(([category, count]) => `${category} ${count} 个`).join("，")}`
    : "类别：暂无";

  return {
    statusLine: activeOfficialTypes.length ? `已启用 ${activeOfficialTypes.length} 个官方部门类型` : "暂无启用的官方部门类型",
    categoryLine,
    items: activeOfficialTypes,
    empty: activeOfficialTypes.length === 0,
    loading: false,
    errorMessage: "",
  };
}

export function buildDepartmentActivationViewModel(payload = {}, { loading = false, saving = false, error = "" } = {}) {
  if (loading) {
    return {
      statusLine: "正在加载已启用部门",
      activeLine: "请稍候",
      selectedKeys: [],
      options: [],
      empty: false,
      loading: true,
      saving: false,
      errorMessage: "",
    };
  }

  if (saving) {
    return {
      statusLine: "正在保存部门启用状态",
      activeLine: "请稍候",
      selectedKeys: [],
      options: [],
      empty: false,
      loading: false,
      saving: true,
      errorMessage: "",
    };
  }

  if (error) {
    return {
      statusLine: "部门启用状态加载失败",
      activeLine: "已启用部门暂不可用",
      selectedKeys: [],
      options: [],
      empty: false,
      loading: false,
      saving: false,
      errorMessage: error,
    };
  }

  const selectedKeys = (payload?.active_department_type_keys || []).filter(Boolean);
  const selectedSet = new Set(selectedKeys);
  const options = (payload?.department_types || [])
    .filter((type) => type?.source === "official")
    .map((type) => ({
      typeKey: type.type_key,
      label: type.display_name || type.type_key || "未命名部门类型",
      category: departmentCategoryLabel(type.category),
      checked: selectedSet.has(type.type_key),
    }));
  const activeLabels = options.filter((item) => selectedSet.has(item.typeKey)).map((item) => item.label);

  return {
    statusLine: selectedKeys.length ? `已启用 ${selectedKeys.length} 个公司部门` : "尚未启用公司部门",
    activeLine: activeLabels.length ? `已启用：${activeLabels.join("、")}` : "可从官方部门类型中选择",
    selectedKeys,
    options,
    empty: options.length === 0,
    loading: false,
    saving: false,
    errorMessage: "",
  };
}

export function buildOperatingLabels({ task, workflow, metaDevelopment, evolutionDecision } = {}) {
  const labels = [];
  const status = task?.status;
  if (status === "COMPLETED") labels.push("已完成");
  if (status === "RUNNING") labels.push("运行中");
  if (status === "FAILED") labels.push("失败");
  if (task?.output) labels.push("结果已生成");
  if (workflow?.status || workflow?.workflow_plan?.length || workflow?.generated_steps?.length) labels.push("工作流已记录");
  if (metaDevelopment?.report_id) labels.push("学习记录已生成");
  if (evolutionDecision?.decision) labels.push("演进已评估");
  if (workflow?.failed_steps?.length || task?.error) labels.push("存在阻塞");
  return labels;
}

export function buildReviewSignals({ task, workflow, metaDevelopment, evolutionDecision } = {}) {
  const signals = [];
  const status = task?.status;
  const hasFailure = status === "FAILED" || Boolean(task?.error) || Boolean(workflow?.failed_steps?.length);
  const hasActiveWorkflowStep = Boolean(workflow?.current_step && status !== "COMPLETED" && status !== "FAILED");
  if (hasFailure || workflow?.blocker || task?.blocker) signals.push("需要复核");
  if (status === "RUNNING" || hasActiveWorkflowStep) signals.push("运行中");
  if (status === "PENDING") signals.push("等待中");
  if (task?.output) signals.push("结果已生成");
  if (metaDevelopment?.report_id) signals.push("学习记录已生成");
  if (evolutionDecision?.decision) signals.push("演进已评估");
  if (needsUserDecision(evolutionDecision, task, workflow)) signals.push("需要用户决策");
  return dedupe(signals);
}

export function buildConsoleTaskState({ task, selectedTaskId, workflow, metaDevelopment, evolutionDecision } = {}) {
  const isSelected = Boolean(task?.task_id && selectedTaskId === task.task_id);
  const isRunning = task?.status === "RUNNING";
  return {
    isSelected,
    canRun: Boolean(task?.task_id && !isRunning),
    runLabel: task?.status === "COMPLETED" ? "再次运行" : "运行任务",
    reviewSignals: buildReviewSignals({ task, workflow, metaDevelopment, evolutionDecision }),
  };
}

export function buildExecutionSummary({ task, workflow, trace, metaDevelopment, evolutionDecision } = {}) {
  const statusText = translateValue(task?.status || "unknown");
  const resultText = task?.output ? "，结果已生成" : "";
  const workflowSteps = workflow?.workflow_plan?.length || workflow?.generated_steps?.length || 0;
  const completedSteps = workflow?.completed_steps?.length || 0;
  const traceCount = trace?.length || 0;
  return {
    statusLine: `${statusText}${resultText}`,
    workflowLine: workflowSteps ? `已记录 ${workflowSteps} 个工作流步骤，已完成 ${completedSteps} 个` : "暂无工作流记录",
    toolLine: task?.selected_tool ? `最近选择工具：${task.selected_tool}；${traceCount} 条工具追踪记录` : `${traceCount} 条工具追踪记录`,
    learningLine: metaDevelopment?.report_id ? "学习报告已记录" : "暂无学习报告",
    evolutionLine: evolutionDecision?.decision ? `演进决策：${translateValue(evolutionDecision.decision)}` : "暂无演进决策",
  };
}

export function buildWorkflowTimeline(workflow = {}) {
  const completed = new Set(workflow.completed_steps || []);
  const failed = new Set(workflow.failed_steps || []);
  const current = workflow.current_step;
  return (workflow.workflow_plan || workflow.generated_steps || [])
    .slice()
    .sort((a, b) => Number(a.step || 0) - Number(b.step || 0))
    .map((step) => {
      const stepNumber = Number(step.step || 0);
      return {
        step: stepNumber,
        action: step.action || step.step_name || "执行",
        purpose: step.purpose || step.description || "",
        requiredTool: step.tool_required || "",
        expectedOutput: step.expected_output || "",
        status: stepStatus(stepNumber, { completed, failed, current }),
      };
    });
}

export function buildMetaDevelopmentSummary(report) {
  if (!report) return [];
  const gapAnalysis = report.gap_analysis || {};
  const detectedGaps = (gapAnalysis.detected_gaps || []).map(translateValue);
  return [
    `任务模式：${gapAnalysis.task_signature || "未知"}`,
    `评审状态：${translateValue(gapAnalysis.status || "unknown")}`,
    `发现缺口：${detectedGaps.length ? detectedGaps.join("、") : "无"}`,
    `计划跟进项：${(report.planned_issues || []).length}`,
    `验证项：${(report.verification_plan || []).length}`,
  ];
}

export function buildEvolutionDecisionSummary(decision) {
  if (!decision) return [];
  const risk = decision.risk_analysis || {};
  const proposal = decision.proposal;
  const proposalText = proposal
    ? `提案记录：${proposal.target_module || "未知目标"}；${proposal.requires_approval ? "需要审批" : "未标记审批"}`
    : "提案记录：无";
  return [
    `决策：${translateValue(decision.decision || "unknown")}`,
    `策略：${(decision.policy || []).map(translatePolicy).join(" > ") || "未记录"}`,
    proposalText,
    `风险：稳定性 ${translateValue(risk.stability_risk?.level || "unknown")}；锁定模块 ${risk.locked_module_risk?.blocked ? "被阻止" : "正常"}；回滚 ${translateValue(risk.rollback_risk?.level || "unknown")}`,
    "不会自动应用代码变更。",
  ];
}

export function buildFallbackEvents(trace = []) {
  const events = [];
  for (let index = 0; index < trace.length; index += 1) {
    const item = trace[index];
    if (!item?.error) continue;
    const nextSuccess = trace
      .slice(index + 1)
      .find((next) => next.step_index === item.step_index && !next.error);
    if (!nextSuccess) continue;
    events.push({
      step: item.step_index,
      fromTool: item.tool_name,
      toTool: nextSuccess.tool_name,
      error: item.error,
    });
  }
  return events;
}

function stepStatus(step, { completed, failed, current }) {
  if (failed.has(step)) return "失败";
  if (completed.has(step)) return "已完成";
  if (current === step) return "运行中";
  return "等待中";
}

function needsUserDecision(evolutionDecision, task, workflow) {
  if (task?.requires_user_decision || workflow?.requires_user_decision) return true;
  if (!evolutionDecision) return false;
  if (evolutionDecision.decision === "postpone_evolution" || evolutionDecision.decision === "rollback_previous_evolution") return true;
  if (evolutionDecision.proposal?.requires_approval) return true;
  return Boolean(evolutionDecision.rollback_record || evolutionDecision.rollbackRecord);
}

function dedupe(items) {
  return Array.from(new Set(items));
}

function clean(value) {
  return String(value || "").trim();
}

function isTenantPrivate(item) {
  return item?.source === "tenant_private";
}

function assertReferencePlaceholder(value, fieldName) {
  const text = clean(value);
  if (!/^(env|kms|vault):[A-Za-z0-9_.:/-]+$/.test(text)) {
    throw new Error(`${fieldName} 仅允许 scheme:reference 占位`);
  }
}

function modelDisplayName(model = {}) {
  return model.display_name || model.model_name || model.model_key || "未命名模型";
}

function modelDetail(model = {}) {
  const provider = model.provider_id || "官方模型";
  const name = model.model_name || gatewayModelName(model.gateway_ref) || model.model_key || "未记录模型名";
  return `${provider} / ${name}`;
}

function gatewayModelName(gatewayRef = "") {
  const parts = String(gatewayRef || "").split(":");
  return parts.length > 1 ? parts.slice(1).join(":") : gatewayRef;
}

function departmentCategoryLabel(category) {
  const labels = {
    business: "业务型",
    function: "职能型",
  };
  return labels[category] || category || "未分类";
}

function humanize(value) {
  return String(value)
    .toLowerCase()
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function translateValue(value) {
  const normalized = String(value || "unknown").toLowerCase();
  const dictionary = {
    completed: "已完成",
    running: "运行中",
    failed: "失败",
    pending: "等待中",
    unknown: "未知",
    do_not_evolve: "不演进",
    postpone_evolution: "暂缓演进",
    rollback_previous_evolution: "回滚上次演进",
    ready_for_review: "准备评审",
    workflow_length: "工作流长度",
    codex_overuse: "Codex 过度使用",
    low: "低",
    medium: "中",
    high: "高",
    controlled: "受控",
  };
  return dictionary[normalized] || humanize(value).toLowerCase();
}

function translateWorkflowStatus(value) {
  const labels = {
    pending: "待执行",
    running: "运行中",
    succeeded: "已完成",
    failed: "失败",
    skipped: "已跳过",
    cancelled: "已取消",
    active: "已启用",
  };
  return labels[value] || translateValue(value || "unknown");
}

function translatePolicy(value) {
  const dictionary = {
    STABILITY: "稳定性",
    OPTIMIZATION: "优化",
    EVOLUTION: "演进",
  };
  return dictionary[value] || value;
}
