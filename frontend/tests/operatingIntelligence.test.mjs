import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import {
  getOperatingIntelligence,
  submitOperatingReportDecision,
} from "../lib/runtimeApi.js";

const read = (path) => readFileSync(new URL(`../${path}`, import.meta.url), "utf8");

test("Operating Intelligence uses one canonical scoped read endpoint", async () => {
  const calls = [];
  await getOperatingIntelligence("company/一", { days: 7, businessId: "business/一" }, async (path, options) => {
    calls.push({ path, options });
    return {};
  });
  assert.equal(calls[0].path, "/api/workspace/runtime/foundation/companies/company%2F%E4%B8%80/operating-intelligence?days=7&business_id=business%2F%E4%B8%80");
});

test("Report decision reuses the existing decision command", async () => {
  let call;
  await submitOperatingReportDecision("company/a", "artifact/a", async (path, options) => {
    call = { path, options };
    return { entity_type: "DECISION_PACKET" };
  });
  assert.equal(call.path, "/api/workspace/runtime/foundation/companies/company%2Fa/operating-intelligence/reports/artifact%2Fa/decision");
  assert.equal(call.options.method, "POST");
});

test("Current page delegates to the accepted operating surface and keeps unknown honest", () => {
  const page = read("app/ceo-office/analytics/page.js");
  const surface = read("app/ceo-office/analytics/OperatingIntelligence.js");
  assert.match(page, /return <OperatingIntelligence \/>/);
  assert.match(surface, /未知不会显示成零/);
  assert.match(surface, /先积累可复核的经营事实/);
  assert.match(surface, /查看方案并交给 CEO 决定/);
  assert.doesNotMatch(surface, /健康分|综合评分|模拟报告/);
  assert.match(surface, /经营分析维度/);
  assert.match(surface, /TerraPaneContent/);
  assert.match(surface, /utilityRequestTabId="current"/);
  assert.doesNotMatch(surface, /真实分析 Artifact/);
  assert.match(surface, /next.scope\?\.ref/);
});
