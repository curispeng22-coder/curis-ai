"use client";

import { Suspense } from "react";

import XhsWorkspacePhaseOne from "../../../../components/xhs/XhsWorkspacePhaseOne.js";
import { RuntimeLoading } from "../../../../components/runtime/RuntimeStates.js";
import LegacyOfficeScopeNotice from "../../../../components/workspace/LegacyOfficeScopeNotice.js";


export default function XhsRuntimePage() {
  return (
    <>
      <LegacyOfficeScopeNotice label="小红书旧业务工作面" />
      <Suspense fallback={<RuntimeLoading label="正在打开小红书运营办公室…" />}>
        <XhsWorkspacePhaseOne />
      </Suspense>
    </>
  );
}
