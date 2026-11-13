"use client";

import TerraShell from "../../../components/terra/TerraShell.js";
import { TerraPageHead, TerraEmpty } from "../../../components/terra/TerraPrimitives.js";

/** 日历占位页（T2）：原型有、v1 暂不建设，Blueprint §16 明确暂不建设项 */
export default function CalendarPage() {
  return (
    <TerraShell topCrumb="公司资源 / 日历">
      <TerraPageHead
        title="日历"
        subtitle="公司级日程与重要节点总览（规划中）"
      />
      <TerraEmpty icon="i-clock">
        日历 · 规划中 · v1 暂不建设（Blueprint §16）
      </TerraEmpty>
    </TerraShell>
  );
}
