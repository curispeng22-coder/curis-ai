import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

const sidebar = readFileSync(new URL("../components/v1/V1Sidebar.js", import.meta.url), "utf8");

test("Workspace routes retain the Business Space navigation selection", () => {
  const expression = sidebar.match(/const active = (.*);/)[1];
  const active = new Function("pathname", "href", `return ${expression};`);
  for (const route of ["/ceo-office/workspace", "/ceo-office/workspace/software", "/ceo-office/workspace/xhs", "/ceo-office/workspace/installed/example"]) {
    assert.equal(active(route, "/ceo-office/business"), true);
    assert.equal(active(route, "/ceo-office"), false);
  }
  assert.equal(active("/ceo-office/workspaces-other", "/ceo-office/business"), false);
  assert.equal(active("/ceo-office/organization", "/ceo-office/business"), false);
  assert.match(sidebar, /aria-current=\{active \? "page" : undefined\}/);
});

test("unavailable global search cannot navigate to a missing route", () => {
  assert.doesNotMatch(sidebar, /href="\/ceo-office\/search"/);
  assert.match(sidebar, /button type="button" disabled title="全局搜索暂未开放/);
  assert.match(sidebar, /<ConversationQuickAccess/);
});

test("employee role display reuses shared translations across areas", () => {
  for (const path of ["app/ceo-office/talent-market/page.js", "app/ceo-office/organization/OrganizationCenter.js"]) {
    const source = readFileSync(new URL(`../${path}`, import.meta.url), "utf8");
    assert.match(source, /import \{ roleLabel \} from/);
    assert.match(source, /roleLabel\(employee.role\)/);
    assert.doesNotMatch(source, /Business scope|canonical relation|可证明的 Business/);
  }
  const talent = readFileSync(new URL("../app/ceo-office/talent-market/page.js", import.meta.url), "utf8");
  assert.match(talent, /event.key === "Escape" && !busy/);
});

test("result summary is readable while original evidence is retained", () => {
  const source = readFileSync(new URL("../components/workspace/SharedEmployeeWorkArea.js", import.meta.url), "utf8");
  const body = source.split("function readableResult(result) {")[1].split("\n}\n")[0];
  const readable = new Function("result", body);
  assert.equal(readable({content: '{"summary":"测试通过","execution_ref":"private"}'}), "测试通过");
  assert.equal(readable({content: "原始文本"}), "原始文本");
  assert.equal(readable({content: '{"execution_ref":"private"}', summary: "已返回结果"}), "已返回结果");
  assert.match(source, /JSON.stringify\(result, null, 2\)/);
});

test("meeting provenance and shared avatar keep ordinary readable identity", () => {
  const meeting = readFileSync(new URL("../app/ceo-office/meeting/page.js", import.meta.url), "utf8");
  assert.match(meeting, /roleLabel\(item.role\)/);
  assert.match(meeting, /EST: "员工估计", UNK: "未知"/);
  assert.match(meeting, /PROVENANCE\[fact\?\.provenance\]/);
  const conversation = readFileSync(new URL("../components/v1/SharedConversation.js", import.meta.url), "utf8");
  assert.match(conversation, /EmployeeAvatar employee=\{\{ \.\.\.employee, name: employee\?\.name \|\| "CEO 助理" \}\}/);
});

test("pending execution does not lock work controls and rejects duplicate submit", async () => {
  const source = readFileSync(new URL("../components/v1/GeneralWorkspaceOperating.js", import.meta.url), "utf8");
  const body = source.split("async function execute(workRef) {")[1].split("\n  async function assignEmployee")[0].replace(/\n  }\s*$/, "");
  let finish;
  const pending = new Promise((resolve) => { finish = resolve; });
  let calls = 0;
  let selected = "";
  const ref = { current: false };
  const run = new Function("executionPending", "setExecutingWork", "setActionError", "executeGeneralWorkspaceWork", "refresh", "conversationError", `return async (workRef) => {${body}}`)(ref, (value) => { selected = value; }, () => {}, () => { calls += 1; return pending; }, async () => {}, () => "暂时不可用");
  const first = run("work-a");
  await run("work-a");
  assert.equal(calls, 1);
  assert.equal(selected, "work-a");
  assert.doesNotMatch(body, /setBusy\(true\)/);
  assert.match(source, /window.setInterval\(read, 1500\)/);
  finish(); await first;
  assert.equal(ref.current, false);
  assert.equal(selected, "");
});
