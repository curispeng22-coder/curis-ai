// Phase-9A Console MVP — 纯函数聚合层单元测试。
// 运行：node --test frontend/app/platform/commercial/
import { test } from "node:test";
import assert from "node:assert";
import {
  buildConsoleOverview,
  FORBIDDEN_ZONES,
  getEmployeeSeatPolicyDesignOnly,
} from "./commercialConsole.mjs";

test("Console overview 结构完整可加载", () => {
  const overview = buildConsoleOverview({});
  assert.ok(overview);
  assert.ok(Array.isArray(overview.plans));
  assert.ok(Array.isArray(overview.pricingRules));
  assert.ok(Array.isArray(overview.quotaRules));
  assert.ok(Array.isArray(overview.capabilityPackages));
  assert.ok(overview.employeeSeatPolicy);
  assert.ok(overview.usageMeter);
  assert.ok(Array.isArray(overview.forbiddenZones));
  assert.ok(overview.boundary);
  assert.strictEqual(overview.usageMeter.dimensions.connector.placeholder, true);
  assert.strictEqual(overview.boundary.workspaceRoutesBlocked, true);
});

test("Plan 聚合展示 plan_id/name/tier/status", () => {
  const overview = buildConsoleOverview({
    plans: { plans: [{ plan_id: "p1", name: "Free", tier: "free", status: "active" }] },
  });
  assert.strictEqual(overview.plans.length, 1);
  assert.strictEqual(overview.plans[0].plan_id, "p1");
  assert.strictEqual(overview.plans[0].name, "Free");
  assert.strictEqual(overview.plans[0].tier, "free");
  assert.strictEqual(overview.plans[0].status, "active");
});

test("PricingRule 聚合展示 subject_type/pricing_type/amount/currency/billing_cycle/status", () => {
  const overview = buildConsoleOverview({
    pricingRules: [
      {
        subject_type: "plan",
        pricing_type: "subscription",
        amount: 99,
        currency: "USD",
        billing_cycle: "monthly",
        status: "active",
      },
    ],
  });
  assert.strictEqual(overview.pricingRules.length, 1);
  const r = overview.pricingRules[0];
  assert.strictEqual(r.subject_type, "plan");
  assert.strictEqual(r.pricing_type, "subscription");
  assert.strictEqual(r.amount, 99);
  assert.strictEqual(r.currency, "USD");
  assert.strictEqual(r.billing_cycle, "monthly");
  assert.strictEqual(r.status, "active");
});

test("QuotaRule 聚合展示 quota_type/limit_value/period/enforcement_mode/status", () => {
  const overview = buildConsoleOverview({
    quotaRules: [
      {
        quota_type: "token",
        limit_value: 1000,
        period: "monthly",
        enforcement_mode: "hard",
        status: "active",
      },
    ],
  });
  assert.strictEqual(overview.quotaRules.length, 1);
  const q = overview.quotaRules[0];
  assert.strictEqual(q.quota_type, "token");
  assert.strictEqual(q.limit_value, 1000);
  assert.strictEqual(q.period, "monthly");
  assert.strictEqual(q.enforcement_mode, "hard");
  assert.strictEqual(q.status, "active");
});

test("CapabilityPackage 聚合含四类 included 列表", () => {
  const overview = buildConsoleOverview({
    capabilityPackages: [
      {
        package_id: "pkg1",
        name: "Starter",
        capability_ids: '["c1","c2"]',
        connector_ids: ["k1"],
        workflow_template_ids: '["w1"]',
        employee_template_ids: null,
        status: "active",
      },
    ],
  });
  assert.strictEqual(overview.capabilityPackages.length, 1);
  const pkg = overview.capabilityPackages[0];
  assert.deepStrictEqual(pkg.includedCapabilities, ["c1", "c2"]);
  assert.deepStrictEqual(pkg.includedConnectors, ["k1"]);
  assert.deepStrictEqual(pkg.includedWorkflows, ["w1"]);
  assert.deepStrictEqual(pkg.includedEmployeeTemplates, []);
  assert.strictEqual(pkg.status, "active");
});

test("EmployeeSeatPolicy design-only 占位", () => {
  const overview = buildConsoleOverview({});
  const policy = overview.employeeSeatPolicy;
  assert.strictEqual(policy.designOnly, true);
  assert.strictEqual(policy.employeeTypes.length, 3);
  const employeeValues = policy.employeeTypes.map((e) => e.value).sort();
  assert.deepStrictEqual(employeeValues, ["enterprise", "professional", "standard"]);
  assert.strictEqual(policy.seatTypes.length, 4);
  const seatValues = policy.seatTypes.map((s) => s.value).sort();
  assert.deepStrictEqual(seatValues, ["additional", "included", "reserved", "trial"]);
  assert.ok(policy.statusEnum.includes("draft"));
  assert.ok(policy.statusEnum.includes("active"));
  assert.ok(policy.statusEnum.includes("disabled"));
  assert.ok(policy.note.includes("design-only") || policy.note.includes("尚未落地 API"));
  // getEmployeeSeatPolicyDesignOnly 独立可用。
  const direct = getEmployeeSeatPolicyDesignOnly();
  assert.strictEqual(direct.designOnly, true);
  assert.strictEqual(direct.seatTypes.length, 4);
});

test("Usage Meter 只读六维（token 正确 + connector 占位 + 无写操作）", () => {
  const usageSummary = {
    tenant_id: "t1",
    totals: {
      usage_event_count: 5,
      prompt_tokens: 10,
      completion_tokens: 20,
      total_tokens: 30,
      estimated_cost: 0.001,
    },
    by_employee: [],
    by_workflow: [],
    by_capability_source: [],
  };
  const overview = buildConsoleOverview({ usageSummary, tenantId: "t1" });
  assert.strictEqual(overview.usageMeter.tenantId, "t1");
  assert.strictEqual(overview.usageMeter.dimensions.token.totalTokens, 30);
  assert.strictEqual(overview.usageMeter.dimensions.token.usageEventCount, 5);
  assert.strictEqual(overview.usageMeter.dimensions.connector.available, false);
  assert.strictEqual(overview.usageMeter.dimensions.connector.placeholder, true);
  assert.strictEqual(overview.usageMeter.dimensions.employee.available, true);
  assert.strictEqual(overview.usageMeter.dimensions.workflow.available, true);
  assert.strictEqual(overview.usageMeter.dimensions.capability.available, true);
  // 本模块为纯函数，不触发任何网络。
  assert.strictEqual(typeof buildConsoleOverview, "function");
});

test("禁止区 5 项全部 LOCKED", () => {
  assert.strictEqual(FORBIDDEN_ZONES.length, 5);
  assert.ok(FORBIDDEN_ZONES.every((z) => z.locked === true));
  const ids = FORBIDDEN_ZONES.map((z) => z.id).sort();
  assert.deepStrictEqual(ids, [
    "invoice",
    "marketplace",
    "payment",
    "promotion_execution",
    "value_pricing",
  ]);
});

test("Admin/Workspace 边界未破坏", () => {
  const overview = buildConsoleOverview({});
  assert.strictEqual(overview.boundary.workspaceRoutesBlocked, true);
  assert.ok(overview.boundary.admin.apis.includes("/api/platform/*"));
  assert.ok(
    overview.boundary.workspace.apis.some(
      (a) => a.includes("/api/workspace") && a.includes("（禁止触碰）"),
    ),
  );
  // 边界未破坏判定：workspaceRoutesBlocked 为真且禁止区全 locked。
  assert.ok(overview.boundary.workspaceRoutesBlocked === true);
  assert.ok(FORBIDDEN_ZONES.every((z) => z.locked === true));
});
