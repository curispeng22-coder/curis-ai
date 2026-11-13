import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

import { materializeFoundingCompany } from "../lib/runtimeApi.js";


test("materialization client sends only the authorized company contract", async () => {
  let captured;
  const values = { company_id: "company-1", ceo_id: "ceo-1", name: "Curis" };
  const result = await materializeFoundingCompany("founding/run-1", values, async (path, options) => {
    captured = { path, options };
    return { company: { company_id: "company-1" }, assistant: { entity_id: "assistant-1" } };
  });

  assert.equal(
    captured.path,
    "/api/workspace/runtime/foundation/founding-runs/founding%2Frun-1/materialize-company"
  );
  assert.equal(captured.options.method, "POST");
  assert.deepEqual(JSON.parse(captured.options.body), values);
  assert.equal("actor" in JSON.parse(captured.options.body), false);
  assert.equal(result.assistant.entity_id, "assistant-1");
});


test("Founding Guide confirms Runtime snapshot before CEO Desk without legacy company writes", async () => {
  const source = await readFile(new URL("../app/onboarding/page.js", import.meta.url), "utf8");

  assert.match(source, /materializeFoundingCompany\(run\.entity_id/);
  assert.match(source, /await getRuntimeCompany\(result\.company\.company_id\)/);
  assert.match(source, /await runtime\.refresh\(\)/);
  assert.match(source, /window\.location\.replace\("\/ceo-office"\)/);
  assert.match(source, />建立公司</);
  assert.doesNotMatch(source, /\bcreateCompany\s*\(/);
  assert.doesNotMatch(source, /localStorage/);
  assert.doesNotMatch(source, /createProject|createTask/);
});

