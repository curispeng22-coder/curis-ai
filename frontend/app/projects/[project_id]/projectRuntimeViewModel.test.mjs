import test from "node:test";
import assert from "node:assert/strict";

import {
  assignmentFacts,
  buildStructuredTask,
  costFact,
  parseStructuredTask,
  primaryAction,
  progressValue,
  resultExplanation,
  resultFacts,
  statusLabel,
} from "./projectRuntimeViewModel.mjs";

test("maps runtime states to one primary action", () => {
  assert.deepEqual(primaryAction({ available_actions: ["submit"] }), { kind: "submit", label: "生成计划" });
  assert.deepEqual(primaryAction({ available_actions: ["auto_run"] }), { kind: "auto_run", label: "启动运行" });
  assert.deepEqual(primaryAction({ available_actions: ["retry"] }), { kind: "retry", label: "重新运行" });
  assert.deepEqual(primaryAction({ available_actions: ["dispatch"] }), { kind: "dispatch", label: "继续运行" });
  assert.deepEqual(primaryAction({ available_actions: ["approve", "reject"] }), { kind: "approve", label: "批准成果" });
  assert.deepEqual(primaryAction({ task: { status: "running" }, available_actions: [] }), { kind: "none", label: "运行进行中" });
});

test("never invents progress for unavailable process state", () => {
  assert.equal(progressValue({ available: false, nodes: [{ status: "unknown" }] }), null);
  assert.equal(progressValue({ available: true, nodes: [{ status: "done" }, { status: "pending" }] }), 50);
});

test("exposes only recorded result facts", () => {
  assert.deepEqual(resultFacts({ executor_result: {}, rework_feedback: [] }), {
    diff: "",
    artifact: "",
    files: [],
    testExitCode: null,
    rounds: null,
    rework: [],
  });
  assert.equal(statusLabel("review"), "待决策");
});

test("explains results and opens the next run only after a terminal state", () => {
  assert.equal(resultExplanation({ status: "running" }).canCreateNextRun, false);
  assert.deepEqual(resultExplanation({ status: "review" }), {
    tone: "success",
    title: "运行成功，等待你的确认",
    body: "检查已通过并记录成果。你可以批准成果，或填写原因要求返工。",
    canCreateNextRun: false,
  });
  assert.equal(resultExplanation({ status: "failed" }).canCreateNextRun, true);
  assert.equal(resultExplanation({ status: "approved" }).canCreateNextRun, true);
  assert.equal(resultExplanation({ status: "rejected" }).canCreateNextRun, true);
});

test("builds one deterministic confirmation payload for both input paths", () => {
  const payload = {
    goal: "交付项目负责人工作台",
    acceptanceCriteria: "可启动运行并看到成果",
    constraintsRisk: "不新增后端接口",
  };
  const text = buildStructuredTask(payload);
  assert.equal(
    text,
    "目标：交付项目负责人工作台\n验收标准：可启动运行并看到成果\n约束 / 风险：不新增后端接口",
  );
  assert.deepEqual(parseStructuredTask(text), payload);
  assert.equal(
    parseStructuredTask(
      "目标：完成工作台\n保留现有结果\n验收标准：可生成计划\n可启动运行\n约束 / 风险：不新增接口",
    ).goal,
    "完成工作台\n保留现有结果",
  );
  assert.equal(buildStructuredTask({ ...payload, acceptanceCriteria: "" }), "");
});

test("keeps legacy goals readable without inventing structured fields", () => {
  assert.deepEqual(parseStructuredTask("完成现有目标"), {
    goal: "完成现有目标",
    acceptanceCriteria: "",
    constraintsRisk: "",
  });
});

test("shows only recorded employee capability and cost facts", () => {
  assert.deepEqual(
    assignmentFacts({
      nodes: [
        {
          id: "n1",
          goal: "运行检查",
          employee_id: "employee-a",
          capability_path: ["local.tool"],
          status: "done",
        },
        {
          id: "n2",
          goal: "整理结果",
          cap_requirement: { cap_type: "tool" },
          status: "pending",
        },
      ],
    }),
    [
      {
        id: "n1",
        goal: "运行检查",
        employee: "employee-a",
        capability: "local.tool",
        status: "done",
      },
      {
        id: "n2",
        goal: "整理结果",
        employee: "尚未分配具体员工",
        capability: "tool 能力待调度",
        status: "pending",
      },
    ],
  );
  assert.equal(costFact({ executor_result: { estimated_cost: 0.00125 } }), "USD 0.001250");
  assert.equal(costFact({ executor_result: {} }), "未记录");
});
