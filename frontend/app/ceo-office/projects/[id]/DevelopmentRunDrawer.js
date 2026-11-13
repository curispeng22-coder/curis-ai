"use client";

import { useEffect, useMemo, useState } from "react";
import { TerraButton, TerraDrawer } from "../../../../components/terra/TerraPrimitives.js";
import { runDevelopmentWorkflow } from "../../../../lib/development.js";

export default function DevelopmentRunDrawer({ open, project, tasks = [], onClose }) {
  const availableTasks = useMemo(
    () => tasks.filter(
      (item) => ["INIT", "FAILED"].includes(item.status)
        && item.requested_capability_type === "model"
        && item.requested_capability_id
    ),
    [tasks]
  );
  const [taskId, setTaskId] = useState("");
  const [targetFiles, setTargetFiles] = useState("");
  const [testFile, setTestFile] = useState("");
  const [maxRounds, setMaxRounds] = useState("3");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!open) return;
    setTaskId(availableTasks[0]?.task_id || "");
    setTargetFiles("");
    setTestFile("");
    setMaxRounds("3");
    setError("");
    setSubmitting(false);
  }, [availableTasks, open]);

  async function submit(event) {
    event.preventDefault();
    const files = targetFiles.split(/[\n,]/).map((item) => item.trim()).filter(Boolean);
    if (!taskId) return setError("请选择已绑定模型的待执行任务");
    if (!files.length) return setError("请填写至少一个目标文件");
    if (!testFile.trim()) return setError("请填写已登记的测试文件");
    setSubmitting(true);
    setError("");
    try {
      const run = await runDevelopmentWorkflow({
        project_id: project.project_id,
        task_id: taskId,
        target_files: files,
        test_file: testFile.trim(),
        max_rounds: Number(maxRounds),
      });
      window.location.assign(`/ceo-office/execution/runs/${run.workflow_run_id}`);
    } catch (err) {
      setError(err?.message || "研发工作流执行失败");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <TerraDrawer
      open={open}
      title="启动研发工作流"
      description="使用任务已绑定的模型，在受控目录完成代码修改、测试与 Git 差异记录。"
      onClose={onClose}
    >
      <form onSubmit={submit} className="space-y-4">
        <div>
          <label htmlFor="rd-task" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            开发任务 *
          </label>
          <select
            id="rd-task"
            value={taskId}
            onChange={(event) => setTaskId(event.target.value)}
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
          >
            {availableTasks.length === 0 && <option value="">暂无可执行研发任务</option>}
            {availableTasks.map((item) => (
              <option key={item.task_id} value={item.task_id}>{item.content}</option>
            ))}
          </select>
          <p className="text-ui-1 text-ui-txt-3 mt-1">
            仅显示待执行或失败、且已人工绑定模型能力的任务。
          </p>
        </div>

        <div>
          <label htmlFor="rd-targets" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            目标文件 *
          </label>
          <textarea
            id="rd-targets"
            rows={4}
            value={targetFiles}
            onChange={(event) => setTargetFiles(event.target.value)}
            placeholder={"backend/app/example.py\n每行一个仓库内相对路径"}
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm font-mono text-ui-txt bg-ui-surface outline-none resize-y focus:ring-2 focus:ring-ui-primary/30"
          />
        </div>

        <div>
          <label htmlFor="rd-test" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            测试文件 *
          </label>
          <input
            id="rd-test"
            value={testFile}
            onChange={(event) => setTestFile(event.target.value)}
            placeholder="backend/tests/test_example.py"
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm font-mono text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
          />
        </div>

        <div>
          <label htmlFor="rd-rounds" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            最大修复轮次
          </label>
          <select
            id="rd-rounds"
            value={maxRounds}
            onChange={(event) => setMaxRounds(event.target.value)}
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
          >
            <option value="1">1 轮</option>
            <option value="2">2 轮</option>
            <option value="3">3 轮</option>
          </select>
        </div>

        {error && <p className="text-xs text-ui-red">{error}</p>}
        <div className="flex justify-end gap-3 pt-2">
          <TerraButton type="button" variant="ghost" onClick={onClose}>取消</TerraButton>
          <TerraButton type="submit" disabled={submitting || availableTasks.length === 0}>
            {submitting ? "执行中…" : "启动执行"}
          </TerraButton>
        </div>
      </form>
    </TerraDrawer>
  );
}
