"use client";

import { useEffect, useState } from "react";
import { getHomeSummary } from "../../lib/api.js";

/**
 * CEO 工作台首屏 first-run 引导（消费后端 home/summary 的 ai_readiness）。
 * 第一次打开 app、尚未接入任何私有模型时，顶部显示「先去绑定模型」引导，
 * 让「整个 app 靠模型驱动」这件事在首屏就讲清楚。已接入模型则完全不渲染。
 */

export default function FirstRunGate() {
  const [ready, setReady] = useState(null);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const summary = await getHomeSummary();
        if (alive) setReady(summary?.ai_readiness || null);
      } catch {
        if (alive) setReady(null);
      }
    })();
    return () => {
      alive = false;
    };
  }, []);

  if (ready?.has_private_model) return null;

  return (
    <div className="mb-5 rounded-ui-sm border border-ui-primary/30 bg-ui-primary-light px-4 py-3">
      <div className="flex flex-wrap items-center gap-3">
        <div className="min-w-0 flex-1">
          <div className="text-sm font-bold text-ui-txt">接入 AI 能力，整个 app 才动起来</div>
          <p className="mt-0.5 text-xs leading-relaxed text-ui-txt-2">
            这是 AI 全自动应用。第一次打开，先去「能力中心」添加你的模型（OpenAI 兼容 / DeepSeek / 自建网关均可），工作台里的「启动任务」才会可用。
          </p>
        </div>
        <a
          href="/ceo-office/capabilities"
          className="inline-flex h-9 flex-shrink-0 items-center rounded-ui-sm bg-ui-primary px-4 text-xs font-bold text-white no-underline hover:opacity-90"
        >
          去添加模型
        </a>
      </div>
    </div>
  );
}
