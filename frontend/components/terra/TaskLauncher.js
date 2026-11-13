"use client";

import { useEffect, useState } from "react";
import { getHomeSummary, createTask, runTask } from "../../lib/api.js";
import { TerraButton, TerraCard, TerraCardHeader, TerraTag } from "./TerraPrimitives.js";

/**
 * 业务空间运行现场的「启动任务」入口（共享组件，software / xhs / shortvideo 复用）。
 *
 * 三态门禁，全部基于后端 home/summary 的 ai_readiness（唯一真源）：
 *  1. 未接入私有模型 → 引导去能力中心添加模型；
 *  2. 已添加模型但未绑定到员工 → 引导去组织绑定；
 *  3. 两者就绪 → 显示 composer，提交后调 POST /api/task + /api/task/{id}/run。
 *
 * 数据纪律：无模型 / 无绑定时绝不伪造执行结果；提交后若模型凭据未配，
 * 真实报错原样展示，不静默。
 */

const BUSINESS_LABEL = {
  software: "研发办公室",
  xhs: "小红书运营办公室",
  shortvideo: "抖音 / TikTok 运营办公室",
};

export default function TaskLauncher({ business, title, defaultContent = "" }) {
  const [readiness, setReadiness] = useState(null);
  const [loading, setLoading] = useState(true);
  const [content, setContent] = useState(defaultContent || "");
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const summary = await getHomeSummary();
        if (!alive) return;
        setReadiness(
          summary?.ai_readiness || { has_private_model: false, has_bound_employee: false }
        );
      } catch {
        if (alive) setReadiness({ has_private_model: false, has_bound_employee: false });
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, []);

  const launch = async () => {
    if (!content.trim() || submitting) return;
    setSubmitting(true);
    setError("");
    setResult(null);
    try {
      const created = await createTask({ content: content.trim(), capability_type: "model" });
      const taskId = created?.task_id;
      if (!taskId) throw new Error("后端未返回任务标识");
      const runResult = await runTask(taskId);
      setResult(runResult || { task_id: taskId, status: "submitted" });
      setContent("");
    } catch (err) {
      setError(err?.message || "任务启动失败（请确认模型凭据已在能力中心正确配置）");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="mb-5 rounded-ui-sm border border-ui-line bg-ui-surface-2 px-3 py-2 text-xs text-ui-txt-3">
        正在检查 AI 能力就绪状态…
      </div>
    );
  }

  if (!readiness?.has_private_model) {
    return (
      <TerraCard className="mb-5">
        <TerraCardHeader icon="i-verified" iconClass="primary" title="先接入 AI 能力，工作台才能启动任务" />
        <p className="mb-3 text-xs leading-relaxed text-ui-txt-2">
          这是 AI 全自动应用。第一次打开，先去「能力中心」添加你的模型（OpenAI 兼容 / DeepSeek / 自建网关均可），整个 app 才有执行力。
        </p>
        <a
          href="/ceo-office/capabilities"
          className="inline-flex h-9 items-center rounded-ui-sm bg-ui-primary px-4 text-xs font-bold text-white no-underline hover:opacity-90"
        >
          去能力中心添加模型
        </a>
      </TerraCard>
    );
  }

  if (!readiness?.has_bound_employee) {
    return (
      <TerraCard className="mb-5">
        <TerraCardHeader icon="i-lightbulb" iconClass="amber" title="模型已添加，还需绑定到 AI 员工" />
        <p className="mb-3 text-xs leading-relaxed text-ui-txt-2">
          已添加模型。下一步把模型绑定到 AI 员工（组织 → 员工 → 能力），任务才能真正派发给模型执行。
        </p>
        <a
          href="/ceo-office/organization/employees"
          className="inline-flex h-9 items-center rounded-ui-sm bg-ui-primary px-4 text-xs font-bold text-white no-underline hover:opacity-90"
        >
          去绑定 AI 员工
        </a>
      </TerraCard>
    );
  }

  return (
    <TerraCard className="mb-5">
      <TerraCardHeader
        icon="i-verified"
        iconClass="primary"
        title={title || `在「${BUSINESS_LABEL[business] || "本业务"}」启动一个任务`}
      />
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="用自然语言描述任务，例如：为本周迭代生成回归测试计划，覆盖登录与支付链路"
        rows={3}
        className="mt-2 w-full resize-none rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-xs text-ui-txt placeholder:text-ui-txt-3 focus:border-ui-primary focus:outline-none"
      />
      <div className="mt-2 flex items-center gap-2">
        <TerraButton variant="primary" disabled={!content.trim() || submitting} onClick={launch}>
          {submitting ? "执行中…" : "启动任务"}
        </TerraButton>
        {result && <TerraTag color="green">已创建 · {result.task_id || "已提交"}</TerraTag>}
      </div>
      {error && <p className="mt-2 text-xs leading-relaxed text-ui-red">{error}</p>}
      {result && (
        <pre className="mt-2 max-h-48 overflow-auto rounded-ui-sm border border-ui-line bg-ui-surface-2 p-2 text-xs text-ui-txt-2">
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </TerraCard>
  );
}
