// Commercial Operation Console — 纯函数聚合层（Phase-9A Console MVP）。
//
// 设计约束（红线）：
// - 纯 ESM 模块：零 import、零 fetch、零 React、零副作用。
// - 可被 `node --test` 直接 import，作为前端聚合的单一事实来源。
// - 仅消费既有 GET /api/platform/* 响应，绝不做 mutation、绝不触碰 /api/workspace/*。
// - EmployeeSeatPolicy 与 Connector 计量维度为 design-only 占位，不调用任何不存在的接口。

/**
 * 禁止区：本阶段锁定的 5 个商业化执行模块。
 * 这些模块涉及 Payment / Invoice / Marketplace / Promotion 执行 / Value Pricing，
 * 不在 Admin 只读聚合范围内，且本阶段不实现任何用户购买或自动扣款。
 * @type {ReadonlyArray<{ id: string, label: string, locked: boolean }>}
 */
export const FORBIDDEN_ZONES = [
  { id: "payment", label: "Payment", locked: true },
  { id: "invoice", label: "Invoice", locked: true },
  { id: "marketplace", label: "Marketplace", locked: true },
  { id: "promotion_execution", label: "Promotion Execution", locked: true },
  { id: "value_pricing", label: "Value Pricing", locked: true },
];

/**
 * 将可能为数组 / JSON 字符串 / null 的值统一转换为数组（容错）。
 * - 已是数组：原样返回。
 * - 字符串：尝试 JSON.parse，失败兜底 []。
 * - 其余（null / undefined / 对象）：兜底 []。
 * @param {unknown} value
 * @returns {Array<unknown>}
 */
function asArray(value) {
  if (Array.isArray(value)) return value;
  if (typeof value === "string") {
    try {
      const parsed = JSON.parse(value);
      return Array.isArray(parsed) ? parsed : [];
    } catch {
      return [];
    }
  }
  return [];
}

/**
 * EmployeeSeatPolicy 设计态元信息（design-only）。
 * 契约已定义但尚未落地数据库表与 API，本阶段仅展示契约元信息，
 * 不调用任何不存在的接口、不触计费。
 * @returns {{
 *   designOnly: boolean,
 *   employeeTypes: Array<{ value: string, label: string }>,
 *   seatTypes: Array<{ value: string, label: string, quotaCost: number | string }>,
 *   statusEnum: string[],
 *   quotaCostNote: string,
 *   note: string,
 * }}
 */
export function getEmployeeSeatPolicyDesignOnly() {
  return {
    designOnly: true,
    employeeTypes: [
      { value: "standard", label: "Standard AI Employee" },
      { value: "professional", label: "Professional AI Employee" },
      { value: "enterprise", label: "Enterprise AI Employee" },
    ],
    seatTypes: [
      { value: "included", label: "套餐内含", quotaCost: 0 },
      { value: "additional", label: "增购", quotaCost: 1 },
      { value: "trial", label: "试用", quotaCost: 0 },
      { value: "reserved", label: "预留", quotaCost: "N" },
    ],
    statusEnum: ["draft", "active", "disabled"],
    quotaCostNote:
      "quota_cost 为配置数值 {seat_quota_cost, token_quota_cost}，仅建模套餐配额消耗，不触计费；pricing_reference → plan_id → pricing_rules(subscription) 为价格权威（本阶段仅说明，不拉取）。",
    note: "EmployeeSeatPolicy 为 design-only：契约已定义但尚未落地表与 API，本阶段仅展示契约元信息，不调用任何不存在的接口。",
  };
}

/**
 * 将 usage summary 映射为只读六维计量结构。
 * Connector 维度尚未接入（design-only 占位），现有 usage summary 无独立 connector 维度。
 * @param {object|null} summary GET /api/platform/usage/summary 响应
 * @param {string|undefined} tenantId 当前聚合 tenant_id
 * @returns {{
 *   tenantId: string|null,
 *   dimensions: {
 *     tenant: { id: string|null, available: boolean, note: string },
 *     employee: { available: boolean, byEmployee: Array<unknown>, note: string },
 *     workflow: { available: boolean, byWorkflow: Array<unknown>, note: string },
 *     capability: { available: boolean, byCapabilitySource: Array<unknown>, byCapabilityType: Array<unknown>, note: string },
 *     connector: { available: boolean, placeholder: boolean, note: string },
 *     token: { available: boolean, usageEventCount: number, promptTokens: number, completionTokens: number, totalTokens: number, estimatedCost: number, note: string },
 *   },
 * }}
 */
function mapUsageMeter(summary, tenantId) {
  return {
    tenantId: tenantId ?? (summary?.tenant_id ?? null),
    dimensions: {
      tenant: {
        id: tenantId ?? (summary?.tenant_id ?? null),
        available: true,
        note: "按租户只读聚合（仅观测）",
      },
      employee: {
        available: true,
        byEmployee: summary?.by_employee ?? [],
        note: "员工用量（by_employee）",
      },
      workflow: {
        available: true,
        byWorkflow: summary?.by_workflow ?? [],
        note: "工作流用量（by_workflow）",
      },
      capability: {
        available: true,
        byCapabilitySource: summary?.by_capability_source ?? [],
        byCapabilityType: summary?.by_capability_type ?? [],
        note: "能力用量（by_capability_source / by_capability_type）",
      },
      connector: {
        available: false,
        placeholder: true,
        note: "Connector 计量维度尚未接入（design-only 占位）：现有 usage summary 无独立 connector 维度，本阶段不改动后端。",
      },
      token: {
        available: true,
        usageEventCount: summary?.totals?.usage_event_count ?? 0,
        promptTokens: summary?.totals?.prompt_tokens ?? 0,
        completionTokens: summary?.totals?.completion_tokens ?? 0,
        totalTokens: summary?.totals?.total_tokens ?? 0,
        estimatedCost: summary?.totals?.estimated_cost ?? 0,
        note: "token 用量来自 usage summary totals",
      },
    },
  };
}

/**
 * 构建商业运营控制台的只读聚合视图模型。
 *
 * @param {object} [input]
 * @param {object|Array<object>} [input.plans] 兼容 {plans:[...]} 或 [...]（来自 GET /api/platform/plans）
 * @param {Array<object>} [input.pricingRules] 来自 GET /api/platform/pricing-rules
 * @param {Array<object>} [input.quotaRules] 来自 GET /api/platform/quota-rules
 * @param {Array<object>} [input.capabilityPackages] 来自 GET /api/platform/capability-packages
 * @param {object|null} [input.usageSummary] 来自 GET /api/platform/usage/summary
 * @param {string} [input.tenantId]
 * @returns {{
 *   plans: Array<{ plan_id: string, name: string, tier: string, status: string }>,
 *   pricingRules: Array<{ subject_type: string, pricing_type: string, amount: number, currency: string, billing_cycle: string, status: string }>,
 *   quotaRules: Array<{ quota_type: string, limit_value: number, period: string, enforcement_mode: string, status: string }>,
 *   capabilityPackages: Array<{ package_id: string, name: string, includedCapabilities: Array<unknown>, includedConnectors: Array<unknown>, includedWorkflows: Array<unknown>, includedEmployeeTemplates: Array<unknown>, status: string }>,
 *   employeeSeatPolicy: ReturnType<typeof getEmployeeSeatPolicyDesignOnly>,
 *   usageMeter: ReturnType<typeof mapUsageMeter>,
 *   forbiddenZones: ReadonlyArray<{ id: string, label: string, locked: boolean }>,
 *   boundary: { admin: object, workspace: object, note: string, workspaceRoutesBlocked: boolean },
 * }}
 */
export function buildConsoleOverview(input = {}) {
  const safeInput = input || {};
  const plansRaw = safeInput.plans?.plans || safeInput.plans || [];
  const plans = Array.isArray(plansRaw) ? plansRaw : [];
  const pricingRules = Array.isArray(safeInput.pricingRules) ? safeInput.pricingRules : [];
  const quotaRules = Array.isArray(safeInput.quotaRules) ? safeInput.quotaRules : [];
  const capabilityPackages = Array.isArray(safeInput.capabilityPackages)
    ? safeInput.capabilityPackages
    : [];
  const usageSummary = safeInput.usageSummary ?? null;

  return {
    plans: plans.map((p) => ({
      plan_id: p.plan_id,
      name: p.name,
      tier: p.tier,
      status: p.status,
    })),
    pricingRules: pricingRules.map((r) => ({
      subject_type: r.subject_type,
      pricing_type: r.pricing_type,
      amount: r.amount,
      currency: r.currency,
      billing_cycle: r.billing_cycle,
      status: r.status,
    })),
    quotaRules: quotaRules.map((q) => ({
      quota_type: q.quota_type,
      limit_value: q.limit_value,
      period: q.period,
      enforcement_mode: q.enforcement_mode,
      status: q.status,
    })),
    capabilityPackages: capabilityPackages.map((pkg) => ({
      package_id: pkg.package_id,
      name: pkg.name,
      includedCapabilities: asArray(pkg.capability_ids),
      includedConnectors: asArray(pkg.connector_ids),
      includedWorkflows: asArray(pkg.workflow_template_ids),
      includedEmployeeTemplates: asArray(pkg.employee_template_ids),
      status: pkg.status,
    })),
    employeeSeatPolicy: getEmployeeSeatPolicyDesignOnly(),
    usageMeter: mapUsageMeter(usageSummary, safeInput.tenantId),
    forbiddenZones: FORBIDDEN_ZONES,
    boundary: {
      admin: {
        owns: "Plan / Pricing / Quota / CapabilityPackage / EmployeeSeatPolicy / 商业配置 / Usage 只读观测",
        apis: ["/api/platform/*"],
      },
      workspace: {
        owns: "EmployeeInstance / WorkflowRun / Capability 执行 / Credential resolver / Usage Event / Value Event",
        apis: ["/api/workspace/*（禁止触碰）"],
      },
      note: "Admin 不修改 Workspace Runtime、不接管 EmployeeInstance、不修改 WorkflowRun、不读 tenant_private 明文密钥；Workspace 不判断价格、不生成 BillingEvent。",
      workspaceRoutesBlocked: true,
    },
  };
}
