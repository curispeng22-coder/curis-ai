"use client";

// 起任务按钮（T4 / 工作台）。
// 点击调用 startWorkflow 创建 workflow 实例，仅展示返回的状态 / 实例 id（只读，不轮询不声称完成）。
// 异常经 try/catch 捕获并展示错误文案，绝不崩。

import { useState } from "react";
import { startWorkflow } from "../lib/task.js";

export default function StartTaskButton({
  empId,
  projectId,
  projectName,
  label = "开始任务",
}) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function handleClick() {
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const data = await startWorkflow({ empId, projectId, projectName });
      // 只读展示创建结果；不轮询、不声称执行完成。
      setResult(data || {});
    } catch (err) {
      setError(err && err.message ? err.message : "启动任务失败");
    } finally {
      setLoading(false);
    }
  }

  const instanceId =
    result &&
    (result.workflow_instance_id || result.id || result.instance_id);
  const status = result && (result.status || result.state);

  return (
    <span>
      <button
        type="button"
        className="ceo-secondary-action"
        style={{ minHeight: "var(--ui-ctl-h-sm)", fontSize: "var(--ui-fs-1)" }}
        onClick={handleClick}
        disabled={loading}
      >
        {loading ? "启动中…" : label}
      </button>
      {error && (
        <div
          style={{
            color: "var(--ui-danger)",
            fontSize: "var(--ui-fs-1)",
            marginTop: "var(--ui-sp-1)",
            maxWidth: 280,
          }}
        >
          ! {error}
        </div>
      )}
      {instanceId && (
        <div
          style={{
            color: "var(--ui-text-3)",
            fontSize: "var(--ui-fs-1)",
            marginTop: "var(--ui-sp-1)",
            lineHeight: 1.5,
            maxWidth: 280,
          }}
        >
          已创建实例：{instanceId}
          {status ? ` · 状态：${status}` : ""}
          <br />
          （仅展示创建状态，未轮询执行结果）
        </div>
      )}
    </span>
  );
}
