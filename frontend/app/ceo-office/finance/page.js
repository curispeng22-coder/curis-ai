"use client";

import TerraShell from "../../../components/terra/TerraShell.js";
import { TerraPageHead, TerraEmpty } from "../../../components/terra/TerraPrimitives.js";

/** 财务占位页（T2）：原型有、v1 暂不建设，Blueprint §16 明确暂不建设项 */
export default function FinancePage() {
  return (
    <TerraShell topCrumb="公司资源 / 财务">
      <TerraPageHead
        title="财务"
        subtitle="经营日成本与收支汇总（规划中）"
      />
      <TerraEmpty icon="i-pie_chart">
        财务 · 规划中 · v1 暂不建设（Blueprint §16）
      </TerraEmpty>
    </TerraShell>
  );
}
