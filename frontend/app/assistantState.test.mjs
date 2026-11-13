import assert from "node:assert/strict";
import test from "node:test";

import {
  INITIAL_ASSISTANT_STATE,
  assistantReducer,
  normalizeAssistantContext,
  normalizeAssistantIdentity,
} from "../lib/assistantState.mjs";

test("assistant state survives page context changes", () => {
  let state = assistantReducer(INITIAL_ASSISTANT_STATE, { type: "open" });
  state = assistantReducer(state, { type: "input", value: "生成10个选题" });
  state = assistantReducer(state, {
    type: "loaded",
    snapshot: { identity: { name: "自定义助手" } },
    notifications: [{ notification_id: 8 }],
    unreadCount: 1,
  });
  state = assistantReducer(state, {
    type: "context",
    value: { page: "project", project_id: "project-1", unsafe: "ignored" },
  });

  assert.equal(state.open, true);
  assert.equal(state.input, "生成10个选题");
  assert.equal(state.unreadCount, 1);
  assert.deepEqual(state.pageContext, {
    page: "project",
    project_id: "project-1",
  });
});

test("assistant identity stays data-driven and minimize is reversible", () => {
  assert.equal(INITIAL_ASSISTANT_STATE.identity.name, "");
  let state = assistantReducer(INITIAL_ASSISTANT_STATE, {
    type: "identity",
    value: {
      name: "小助手",
      avatar: "🌿",
      role: "CEO 秘书",
      tone: "简洁",
      personality: "主动",
    },
  });
  state = assistantReducer(state, { type: "minimize" });
  assert.equal(state.open, false);
  assert.equal(state.minimized, true);
  state = assistantReducer(state, { type: "open" });
  assert.equal(state.open, true);
  assert.equal(state.minimized, false);
  assert.equal(state.identity.name, "小助手");
  assert.deepEqual(
    normalizeAssistantIdentity({
      ...state.identity,
      tenant_id: "must-not-submit",
      updated_at: "2026-07-30T00:00:00Z",
    }),
    {
      name: "小助手",
      avatar: "🌿",
      role: "CEO 秘书",
      tone: "简洁",
      personality: "主动",
    }
  );
});

test("assistant context never accepts arbitrary page data", () => {
  assert.deepEqual(
    normalizeAssistantContext({
      page: "task",
      task_id: "task-1",
      prompt: "must not cross the boundary",
      api_key: "secret",
    }),
    { page: "task", task_id: "task-1" }
  );
  assert.deepEqual(
    normalizeAssistantContext({ page: "api_key=secret" }),
    { page: "workspace" }
  );
});
