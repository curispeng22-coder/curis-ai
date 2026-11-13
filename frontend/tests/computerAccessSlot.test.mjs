import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import { computerAccessView, COMPUTER_ACCESS_MODEL_VIEW } from "../lib/computerAccess.mjs";

const read = (path) => readFileSync(new URL(`../${path}`, import.meta.url), "utf8");

test("model executors and no-bridge employees get distinct truthful read-only views", () => {
  assert.equal(
    computerAccessView({ state: "MODEL_EXECUTOR_NOT_APPLICABLE" }).label,
    "访问权限 · 模型不适用",
  );
  assert.equal(
    computerAccessView(null, { modelBacked: true }).label,
    "访问权限 · 模型不适用",
  );
  assert.equal(COMPUTER_ACCESS_MODEL_VIEW.title.includes("不提供选择"), true);
  assert.equal(
    computerAccessView({ state: "NO_EXECUTION_BRIDGE" }).label,
    "访问权限 · 无法确认",
  );
  assert.equal(computerAccessView(null).label, "访问权限 · 无法确认");
});

test("only a verified effective snapshot may claim enabled access", () => {
  const granted = computerAccessView({
    configured_state: "CONFIGURED",
    effective_state: "GRANTED",
    verification_state: "VERIFIED",
  });
  assert.equal(granted.label, "访问权限 · 已验证生效");
  const denied = computerAccessView({ effective_state: "DENIED", verification_state: "VERIFIED" });
  assert.equal(denied.label, "访问权限 · 已验证未授予");
  // Configured but unverified must not claim effectiveness (ADR-0046).
  const pending = computerAccessView({
    configured_state: "CONFIGURED",
    effective_state: "UNKNOWN",
    verification_state: "UNVERIFIED",
  });
  assert.equal(pending.label, "访问权限 · 已配置 · 待验证");
  const unverifiedGranted = computerAccessView({
    configured_state: "CONFIGURED",
    effective_state: "GRANTED",
    verification_state: "UNVERIFIED",
  });
  assert.equal(unverifiedGranted.label, "访问权限 · 已配置 · 待验证");
  // Agent present without evidence stays unconfirmed.
  assert.equal(computerAccessView(null, { agentBacked: true }).label, "访问权限 · 无法确认");
});

test("shared composer renders a read-only access slot instead of the upcoming placeholder", () => {
  const source = read("components/v1/SharedConversation.js");
  assert.match(source, /export function ComputerAccessSlot/);
  assert.match(source, /computerAccessView/);
  assert.doesNotMatch(source, /ComposerUpcomingControl label="访问权限"/);
  assert.match(source, /<button[^>]*disabled[^>]*>\{view\.label\}<\/button>/);
  assert.match(source, /access=\{\{ state: "MODEL_EXECUTOR_NOT_APPLICABLE" \}\}/);
  // The blocked controls remain explicit placeholders.
  assert.match(source, /ComposerUpcomingControl label="工作模式"/);
  assert.match(source, /ComposerUpcomingControl label="Auto"/);
});

test("conversation hosts feed server or snapshot truth into the slot", () => {
  const employee = read("components/v1/EmployeeConversation.js");
  assert.match(employee, /access=\{view\?\.computer_access/);
  const workArea = read("components/workspace/SharedEmployeeWorkArea.js");
  assert.match(workArea, /access=\{composer\.computer_access/);
  assert.match(workArea, /accessExecutor=\{\{ modelBacked/);
  assert.doesNotMatch(workArea, /· \{accessLabel\(employee\.composer/);
  const d1 = read("components/delivery/d1/EmployeeConversationView.js");
  assert.match(d1, /access=\{profile\?\.composer\?\.computer_access/);
  assert.doesNotMatch(d1, /<p>\{accessLabel\(/);
  const writing = read("components/writing/WritingChapterMain.js");
  assert.match(writing, /MODEL_EXECUTOR_NOT_APPLICABLE/);
});
