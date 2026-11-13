import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

const read = (path) => readFileSync(new URL(`../${path}`, import.meta.url), "utf8");

test("objectSearchState maps nine object types with labels and icons", async () => {
  const { OBJECT_GROUPS, groupMeta } = await import("../lib/objectSearchState.mjs");
  const types = OBJECT_GROUPS.map((g) => g.type);
  assert.deepEqual(types, [
    "business", "workspace", "employee", "business_object",
    "knowledge", "meeting", "decision", "task", "result",
  ]);
  for (const g of OBJECT_GROUPS) {
    assert.ok(g.label, `${g.type} has a label`);
    assert.ok(g.icon, `${g.type} has an icon`);
  }
  assert.equal(groupMeta("employee").label, "员工");
  assert.equal(groupMeta("unknown").label, "unknown");
});

test("objectHref routes each type to a verified existing page", async () => {
  const { objectHref } = await import("../lib/objectSearchState.mjs");
  assert.equal(objectHref({ type: "business", id: "b1" }), "/ceo-office/business");
  assert.equal(objectHref({ type: "workspace", id: "w1" }), "/ceo-office/workspace/installed/w1");
  assert.equal(objectHref({ type: "employee", id: "e1" }), "/ceo-office/organization/employees/e1");
  assert.equal(objectHref({ type: "knowledge", id: "k1" }), "/ceo-office/knowledge/entries/k1");
  assert.equal(objectHref({ type: "meeting", id: "m1" }), "/ceo-office/meeting?meeting=m1");
  assert.equal(objectHref({ type: "decision", id: "d1" }), "/ceo-office/decisions");
  assert.equal(objectHref({ type: "task", id: "t1" }), "/ceo-office/execution/tasks/t1");
  assert.equal(
    objectHref({ type: "result", id: "a1", workspace_id: "ws1" }),
    "/ceo-office/workspace?workspace_id=ws1&result_workspace=ws1&result_ref=a1",
  );
  assert.equal(
    objectHref({ type: "business_object", id: "o1", workspace_id: "ws1" }),
    "/ceo-office/workspace/installed/ws1",
  );
  assert.equal(objectHref({ type: "business_object", id: "o1" }), "/ceo-office/workspace");
  assert.equal(objectHref({ type: "unknown", id: "x" }), "/ceo-office");
});

test("WorkspacePaneShell consumes the real search surface (not disabled copy)", () => {
  const source = read("components/workspace/WorkspacePaneShell.js");
  assert.match(source, /searchCompanyObjects/);
  assert.match(source, /objectSearchState/);
  assert.match(source, /onSearchKeyDown/);
  assert.doesNotMatch(source, /全公司搜索尚未接入/);
});

test("object-search API method targets the company-scoped endpoint", () => {
  const api = read("lib/v1FrontendApi.js");
  assert.match(api, /\/api\/workspace\/companies\/\$\{encodeURIComponent\(companyId\)\}\/object-search\?q=/);
});
