import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

const read = (path) => readFileSync(new URL(`../${path}`, import.meta.url), "utf8");

test("Result opening uses an explicit durable command; restoration is read-only", () => {
  const source = read("components/v1/ResultReferenceView.js");
  assert.match(source, /selection\.explicit/);
  assert.match(source, /state\.key !== key/);
  assert.match(source, /resultSelection\(params\.get\("result_workspace"\), params\.get\("result_ref"\), false\)/);
  assert.match(source, /getResultDetail/);
  assert.match(source, /markResultViewed/);
  assert.doesNotMatch(source, /localStorage|sessionStorage|Acceptance|transitionRuntime/);
  const api = read("lib/v1FrontendApi.js");
  assert.match(api, /result_version: result\.result_version/);
  assert.match(api, /result-viewed/);
});

test("CEO and Work result links share the reader and canonical references", () => {
  for (const file of ["CeoDeskOperating", "GeneralWorkspaceOperating"]) {
    const source = read(`components/v1/${file}.js`);
    assert.match(source, /ResultReferenceView/);
    assert.match(source, /restoreResultSelection/);
    assert.match(source, /rememberResultSelection/);
  }
  assert.match(read("components/v1/CeoDeskOperating.js"), /onViewed=\{load\}/);
  assert.match(read("components/v1/GeneralWorkspaceOperating.js"), /#work-\$\{work\.work_ref\}/);
});

test("Composer is shared, preserves failed input and keeps unimplemented tools disabled", () => {
  const source = read("components/v1/SharedConversation.js");
  const employee = read("components/workspace/SharedEmployeeWorkArea.js");
  assert.match(employee, /ConversationComposer/);
  assert.match(employee, /await onSend/);
  assert.match(employee, /输入已保留/);
  assert.match(source, /employee\?\.assistant_id/);
  assert.match(source, /message\.message_id/);
  assert.match(source, /referenceHref \?/);
  assert.match(source, /语音输入尚未连接/);
  assert.match(source, /scopeKey/);
});
