import Link from "next/link";

import { TerraButton, TerraCard } from "../terra/TerraPrimitives.js";


export function RuntimeLoading({ label = "正在读取公司运行状态…" }) {
  return (
    <div role="status" aria-live="polite" className="space-y-3">
      <p className="text-ui-2 text-ui-txt-2">{label}</p>
      <div className="h-24 animate-pulse rounded-ui-md bg-ui-surface-2" />
      <div className="h-40 animate-pulse rounded-ui-md bg-ui-surface-2" />
    </div>
  );
}

export function RuntimeError({ message, onRetry, forbidden = false }) {
  return (
    <TerraCard className="max-w-2xl">
      <h2 className="font-ui-sans text-ui-5 font-semibold text-ui-txt">
        {forbidden ? "无权访问" : "运行状态读取失败"}
      </h2>
      <p role="alert" className="mt-2 max-w-[68ch] text-ui-2 leading-relaxed text-ui-txt-2">
        {message || "当前无法读取运行状态。"}
      </p>
      <div className="mt-4 flex flex-wrap gap-2">
        {onRetry && <TerraButton onClick={onRetry}>重新加载</TerraButton>}
        <Link href="/ceo-office" className="inline-flex min-h-8 items-center px-3 text-ui-1 font-bold text-ui-txt-2 no-underline">
          返回 CEO 工作台
        </Link>
      </div>
    </TerraCard>
  );
}

export function RuntimeEmpty({ title, description, action }) {
  return (
    <TerraCard className="max-w-2xl">
      <h2 className="font-ui-sans text-ui-5 font-semibold text-ui-txt">{title}</h2>
      <p className="mt-2 max-w-[68ch] text-ui-2 leading-relaxed text-ui-txt-2">{description}</p>
      {action && <div className="mt-4">{action}</div>}
    </TerraCard>
  );
}
