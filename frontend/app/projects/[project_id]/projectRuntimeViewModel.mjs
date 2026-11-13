const STATUS_LABELS = {
  planned: "已规划",
  active: "进行中",
  blocked: "受阻",
  completed: "已完成",
  archived: "已归档",
  pending: "待启动",
  queued: "已排队",
  running: "运行中",
  review: "待决策",
  approved: "已完成",
  rejected: "已拒绝",
  failed: "失败",
  done: "已完成",
  unknown: "状态不可恢复",
};

export function statusLabel(status) {
  return STATUS_LABELS[status] || status || "未开始";
}

export function primaryAction(runtime) {
  const actions = runtime?.available_actions || [];
  const task = runtime?.task;
  if (actions.includes("submit")) return { kind: "submit", label: "生成计划" };
  if (actions.includes("auto_run")) return { kind: "auto_run", label: "启动运行" };
  if (actions.includes("retry")) return { kind: "retry", label: "重新运行" };
  if (actions.includes("dispatch")) return { kind: "dispatch", label: "继续运行" };
  if (actions.includes("approve")) return { kind: "approve", label: "批准成果" };
  if (actions.includes("view_result")) return { kind: "view_result", label: "查看成果" };
  if (task?.status === "running" || task?.status === "queued") {
    return { kind: "none", label: "运行进行中" };
  }
  return { kind: "none", label: "当前无可执行动作" };
}

export function progressValue(graph) {
  const value = graph?.progress;
  if (typeof value === "number") return Math.max(0, Math.min(100, value));
  if (value && typeof value === "object" && typeof value.percent === "number") {
    return Math.max(0, Math.min(100, value.percent));
  }
  const nodes = graph?.nodes || [];
  if (!nodes.length || graph?.available === false) return null;
  return Math.round((nodes.filter((node) => node.status === "done").length / nodes.length) * 100);
}

export function resultFacts(task) {
  const result = task?.executor_result || {};
  return {
    diff: typeof result.diff_text === "string" ? result.diff_text : "",
    artifact: typeof result.artifact_text === "string" ? result.artifact_text : "",
    files: Array.isArray(result.files) ? result.files : [],
    testExitCode: Number.isInteger(result.test_exit_code) ? result.test_exit_code : null,
    rounds: Number.isFinite(result.rounds) ? result.rounds : null,
    rework: Array.isArray(task?.rework_feedback) ? task.rework_feedback : [],
  };
}

export function buildStructuredTask({ goal, acceptanceCriteria, constraintsRisk }) {
  const values = {
    goal: String(goal || "").trim(),
    acceptanceCriteria: String(acceptanceCriteria || "").trim(),
    constraintsRisk: String(constraintsRisk || "").trim(),
  };
  if (!values.goal || !values.acceptanceCriteria || !values.constraintsRisk) {
    return "";
  }
  return [
    `目标：${values.goal}`,
    `验收标准：${values.acceptanceCriteria}`,
    `约束 / 风险：${values.constraintsRisk}`,
  ].join("\n");
}

export function parseStructuredTask(value) {
  const text = typeof value === "string" ? value.trim() : "";
  const match = text.match(/^目标：([\s\S]+?)\n验收标准：([\s\S]+?)\n约束 \/ 风险：([\s\S]+)$/);
  if (!match) {
    return {
      goal: text,
      acceptanceCriteria: "",
      constraintsRisk: "",
    };
  }
  return {
    goal: match[1].trim(),
    acceptanceCriteria: match[2].trim(),
    constraintsRisk: match[3].trim(),
  };
}

export function assignmentFacts(graph) {
  return (graph?.nodes || []).map((node, index) => {
    const paths = Array.isArray(node.capability_path) ? node.capability_path.filter(Boolean) : [];
    const capType = node.cap_requirement?.cap_type;
    return {
      id: node.id || `node-${index + 1}`,
      goal: node.goal || `计划步骤 ${index + 1}`,
      employee: node.employee_id || "尚未分配具体员工",
      capability: paths.length ? paths.join(" → ") : capType ? `${capType} 能力待调度` : "能力待调度",
      status: node.status || "pending",
    };
  });
}

export function costFact(task) {
  const result = task?.executor_result || {};
  const value = result.estimated_cost ?? result.cost_usd;
  if (typeof value !== "number" || !Number.isFinite(value) || value < 0) {
    return "未记录";
  }
  return `USD ${value.toFixed(6)}`;
}

export function resultExplanation(task) {
  if (!task) {
    return {
      tone: "neutral",
      title: "先写下这次要完成的目标",
      body: "保存目标后会生成计划，你确认后再启动运行。",
      canCreateNextRun: true,
    };
  }
  if (task.status === "failed") {
    return {
      tone: "failure",
      title: "这次运行没有成功",
      body: "没有产生可交付成果。你可以重新运行当前目标，或修改目标后创建下一次运行。",
      canCreateNextRun: true,
    };
  }
  if (task.status === "rejected") {
    return {
      tone: "failure",
      title: "这次成果未被接受",
      body: "修改目标后可以创建下一次运行，原结果会继续保留作为证据。",
      canCreateNextRun: true,
    };
  }
  if (task.status === "approved") {
    return {
      tone: "success",
      title: "这次成果已确认",
      body: "结果已经保留。现在可以修改目标并创建下一次运行。",
      canCreateNextRun: true,
    };
  }
  if (task.status === "review") {
    return {
      tone: "success",
      title: "运行成功，等待你的确认",
      body: "检查已通过并记录成果。你可以批准成果，或填写原因要求返工。",
      canCreateNextRun: false,
    };
  }
  if (task.status === "running" || task.status === "queued") {
    return {
      tone: "progress",
      title: "正在执行这次目标",
      body: "页面会自动更新状态；完成后这里会显示结果和下一步。",
      canCreateNextRun: false,
    };
  }
  return {
    tone: "progress",
    title: "计划已经准备好",
    body: "启动运行后，结果、执行证据和下一步会回到这里。",
    canCreateNextRun: false,
  };
}
