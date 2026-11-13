"use client";

import DevConsole from "../_devConsole.js";

/**
 * 开发者控制台（原根路由 `/` 的内容）。
 *
 * 2026-08-07 起 `/` 让位给产品入口 `/ceo-office`，这里保留原有的全功能裸表单
 * 面板作为调试与兜底通道：默认模型设置、私有能力三列表（模型/工具/连接器）、
 * 员工模板与实例、研发 SOP 工作流手动执行、任务历史与执行详情。
 *
 * 这些面板中有一部分尚未在产品页里有对等入口，因此不删除、不隐藏。
 */
export default function DevConsolePage() {
  return (
    <>
      <div className="border-b border-ui-line bg-ui-bg-2 px-6 py-2">
        <div className="mx-auto flex max-w-[1200px] flex-wrap items-center gap-3">
          <span className="rounded-ui-sm bg-ui-txt-3 px-2 py-0.5 text-[11px] font-bold uppercase tracking-wide text-white">
            Dev
          </span>
          <span className="text-xs text-ui-txt-2">
            开发者控制台 · 全功能裸表单，非产品界面
          </span>
          <a
            href="/ceo-office"
            className="ml-auto inline-flex h-8 items-center rounded-ui-sm border border-ui-line bg-white px-3 text-xs font-bold text-ui-txt no-underline hover:bg-ui-bg-2"
          >
            返回 CEO 工作台
          </a>
        </div>
      </div>
      <DevConsole />
    </>
  );
}
