import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

const root = new URL("../", import.meta.url);
const page = readFileSync(new URL("app/ceo-office/meeting/page.js", root), "utf8");
const api = readFileSync(new URL("lib/api.js", root), "utf8");

test("Meeting Room uses the accepted overview, overlay, conversation, decision and result continuity", () => {
  for (const text of [
    "当前会议", "最近历史会议", "召开会议", "推进负责人", "参与员工", "你的参与方式",
    "会议会持续存在", "形成下一项决定", "等待你的决定", "工作与结果", "结果已返回",
    "团队讨论中", "等待工作结果", "讨论暂时没有新的进展", "团队讨论已暂停",
    "员工返回的内容还不能作为会议结果",
  ]) assert.ok(page.includes(text), text);
  assert.ok(page.includes("SharedConversation"));
  assert.ok(page.includes("EmployeeAvatar"));
  assert.ok(page.includes("UNKNOWN") || page.includes("UNK"));
  assert.ok(!page.includes("localStorage"));
  assert.ok(!page.includes("SAMPLE_MEETING"));
  assert.ok(!page.includes("`：${continuation.reason}`"));
});

test("Meeting Room client keeps one canonical company-scoped API path", () => {
  for (const action of [
    "getMeetings", "createMeeting", "addMeetingMessage", "requestMeetingDecision",
    "reviewMeetingDecision", "chooseMeetingDecision", "syncMeeting", "closeMeeting",
  ]) assert.ok(api.includes(`export const ${action}`), action);
  assert.ok(api.includes("/api/workspace/runtime/foundation/companies/"));
  assert.ok(api.includes("/decision/choose"));
});
