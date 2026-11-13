import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

import { getRuntimeBootstrap, getRuntimeCompanies } from "../lib/runtimeApi.js";


test("fresh First Arrival reads the side-effect-free Runtime collection", async () => {
  const calls = [];
  const result = await getRuntimeBootstrap(async (path, options) => {
    calls.push({ path, options });
    return { tenant_id: "selfuse", companies: [] };
  });

  assert.deepEqual(result, { companyId: "", snapshot: null, simulations: [] });
  assert.deepEqual(calls, [
    { path: "/api/workspace/runtime/foundation/companies", options: undefined },
  ]);
});


test("Runtime collection client is GET-only and bootstrap never calls the legacy directory", async () => {
  let captured;
  await getRuntimeCompanies(async (path, options) => {
    captured = { path, options };
    return { companies: [] };
  });
  const source = await readFile(new URL("../lib/runtimeApi.js", import.meta.url), "utf8");

  assert.deepEqual(captured, {
    path: "/api/workspace/runtime/foundation/companies",
    options: undefined,
  });
  assert.doesNotMatch(source, /request\("\/api\/workspace\/companies"\)/);
});

