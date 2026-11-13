"use client";

import { TerraErrorState } from "../components/terra/TerraState.js";

export default function AppError({ error, reset }) {
  const reference = error?.digest ? `参考编号：${error.digest}` : "";

  return (
    <main className="min-h-screen bg-ui-bg px-4 py-16">
      <section className="mx-auto max-w-xl rounded-ui-lg border border-ui-line bg-ui-surface">
        <TerraErrorState
          title="页面暂时无法显示"
          message={`当前页面发生未预期错误。${reference}`}
          onRetry={reset}
        />
      </section>
    </main>
  );
}
