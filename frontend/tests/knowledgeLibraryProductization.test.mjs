import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

const root = new URL("../", import.meta.url);
const page = readFileSync(new URL("app/ceo-office/knowledge/page.js", root), "utf8");
const detail = readFileSync(new URL("app/ceo-office/knowledge/entries/[id]/page.js", root), "utf8");
const client = readFileSync(new URL("lib/knowledge.js", root), "utf8");
const workspace = readFileSync(new URL("components/v1/GeneralWorkspaceOperating.js", root), "utf8");

test("knowledge surfaces expose the accepted real-data flow", () => {
  for (const text of [
    "资料集合", "清除筛选", "搜索标题、正文或标签", "加载更多",
    "为当前工作选择资料", "期望结果", "添加 ${selected.length} 条并返回",
    "被哪些工作使用", "相关结果与证据", "查看技术详情",
  ]) assert.ok(`${page}\n${detail}`.includes(text), text);

  for (const endpoint of [
    "/api/workspace/knowledge/entries", "/used-by", "/results", "/works/",
  ]) assert.ok(client.includes(endpoint), endpoint);

  assert.ok(page.includes("pick_for"));
  assert.ok(page.includes("return_to"));
  assert.ok(workspace.includes("pick_for: work.work_ref"));
  assert.ok(workspace.includes("添加参考资料"));
  assert.ok(page.includes("来源与接入"));
  assert.ok(page.includes("TerraPaneContent"));
  assert.ok(detail.includes("TerraPaneContent"));
  assert.ok(page.includes('utilityRequestTabId="current"'));
  assert.ok(detail.includes('utilityRequestTabId="current"'));
  assert.ok(!page.includes("SAMPLE_ENTRIES"));
  assert.ok(!page.includes("getProjects"));
  assert.ok(!page.includes("getDepartments"));
  assert.ok(!detail.includes("资料 ID"));
});
