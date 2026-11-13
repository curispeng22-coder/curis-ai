"use client";

import { useParams } from "next/navigation";
import TerraShell from "../../../../../components/terra/TerraShell.js";
import { TerraPageHead, TerraEmpty } from "../../../../../components/terra/TerraPrimitives.js";

/** 具体部门办公室占位页（v1 暂不建设，Blueprint §16 明确暂不建设项） */
export default function DepartmentOfficeDetailPage() {
  const params = useParams();
  const id = params?.id;
  return (
    <TerraShell topCrumb="工作空间 / 部门办公室">
      <TerraPageHead
        title={id ? `部门办公室 · ${id}` : "部门办公室"}
        subtitle="业务部门共享办公与协作空间"
      />
      <TerraEmpty icon="i-apartment">
        部门办公室 · 规划中 · v1 暂不建设（Blueprint §16 · 业务启动后可激活）
      </TerraEmpty>
    </TerraShell>
  );
}
