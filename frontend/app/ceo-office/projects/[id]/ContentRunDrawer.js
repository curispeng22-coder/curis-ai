"use client";

import { useEffect, useMemo, useState } from "react";
import { TerraButton, TerraDrawer } from "../../../../components/terra/TerraPrimitives.js";
import { runContentWorkflow } from "../../../../lib/content.js";

const PLATFORM_OPTIONS = [
  { value: "xhs", label: "小红书" },
  { value: "douyin", label: "抖音" },
  { value: "toutiao", label: "头条" },
];

export default function ContentRunDrawer({ open, project, tasks = [], onClose }) {
  const availableTasks = useMemo(
    () => tasks.filter(
      (item) => ["INIT", "FAILED"].includes(item.status)
        && item.requested_capability_type === "model"
        && item.requested_capability_id
    ),
    [tasks]
  );
  const [taskId, setTaskId] = useState("");
  const [trendSource, setTrendSource] = useState("");
  const [trendSummary, setTrendSummary] = useState("");
  const [brandVoiceRef, setBrandVoiceRef] = useState("");
  const [platforms, setPlatforms] = useState(["xhs", "douyin", "toutiao"]);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!open) return;
    setTaskId(availableTasks[0]?.task_id || "");
    setTrendSource("");
    setTrendSummary("");
    setBrandVoiceRef("");
    setPlatforms(["xhs", "douyin", "toutiao"]);
    setError("");
    setSubmitting(false);
  }, [availableTasks, open]);

  function togglePlatform(value) {
    setPlatforms((current) => (
      current.includes(value)
        ? current.filter((item) => item !== value)
        : [...current, value]
    ));
  }

  async function submit(event) {
    event.preventDefault();
    if (!taskId) return setError("请选择已绑定模型的待执行任务");
    if (!trendSource.trim()) return setError("请填写可追溯的热点来源");
    if (!trendSummary.trim()) return setError("请填写热点摘要");
    if (!platforms.length) return setError("请至少选择一个目标平台");
    setSubmitting(true);
    setError("");
    try {
      await runContentWorkflow({
        project_id: project.project_id,
        task_id: taskId,
        trend_source: trendSource.trim(),
        trend_summary: trendSummary.trim(),
        platforms,
        brand_voice_ref: brandVoiceRef.trim(),
      });
      window.location.assign(`/ceo-office/execution/tasks/${taskId}`);
    } catch (err) {
      setError(err?.message || "内容工作流执行失败");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <TerraDrawer
      open={open}
      title="启动内容工作流"
      description="基于你提供的热点依据，生成选题、平台文案、SVG 图片资产与复盘计划。"
      onClose={onClose}
    >
      <form onSubmit={submit} className="space-y-4">
        <div>
          <label htmlFor="content-task" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            内容任务 *
          </label>
          <select
            id="content-task"
            value={taskId}
            onChange={(event) => setTaskId(event.target.value)}
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
          >
            {availableTasks.length === 0 && <option value="">暂无可执行内容任务</option>}
            {availableTasks.map((item) => (
              <option key={item.task_id} value={item.task_id}>{item.content}</option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="trend-source" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            热点来源 *
          </label>
          <input
            id="trend-source"
            value={trendSource}
            onChange={(event) => setTrendSource(event.target.value)}
            placeholder="报告 URL、文章标题或内部资料编号"
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
          />
        </div>

        <div>
          <label htmlFor="trend-summary" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            热点摘要 *
          </label>
          <textarea
            id="trend-summary"
            rows={4}
            value={trendSummary}
            onChange={(event) => setTrendSummary(event.target.value)}
            placeholder="摘录可核验事实，不要填写凭证或隐私信息"
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none resize-y focus:ring-2 focus:ring-ui-primary/30"
          />
        </div>

        <fieldset>
          <legend className="block text-xs font-bold text-ui-txt-2 mb-1.5">目标平台 *</legend>
          <div className="flex flex-wrap gap-3">
            {PLATFORM_OPTIONS.map((item) => (
              <label key={item.value} className="inline-flex items-center gap-2 text-sm text-ui-txt-2">
                <input
                  type="checkbox"
                  checked={platforms.includes(item.value)}
                  onChange={() => togglePlatform(item.value)}
                />
                {item.label}
              </label>
            ))}
          </div>
        </fieldset>

        <div>
          <label htmlFor="brand-voice" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            品牌语气引用
          </label>
          <input
            id="brand-voice"
            value={brandVoiceRef}
            onChange={(event) => setBrandVoiceRef(event.target.value)}
            placeholder="未配置可留空"
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
          />
        </div>

        <p className="text-ui-1 text-ui-txt-3">
          本次只生成内容预览；外部发布未执行。
        </p>
        {error && <p className="text-xs text-ui-red">{error}</p>}
        <div className="flex justify-end gap-3 pt-2">
          <TerraButton type="button" variant="ghost" onClick={onClose}>取消</TerraButton>
          <TerraButton type="submit" disabled={submitting || availableTasks.length === 0}>
            {submitting ? "生成中…" : "生成内容成果"}
          </TerraButton>
        </div>
      </form>
    </TerraDrawer>
  );
}
