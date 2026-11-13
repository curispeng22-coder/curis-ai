"use client";

import { Suspense } from "react";

import RdWorkspacePhaseTwo from "../../../../components/rd/RdWorkspacePhaseTwo.js";
import { RuntimeLoading } from "../../../../components/runtime/RuntimeStates.js";
import LegacyOfficeScopeNotice from "../../../../components/workspace/LegacyOfficeScopeNotice.js";


export default function SoftwareRuntimePage() {
  return (
    <>
      <LegacyOfficeScopeNotice label="研发（RD）业务" />
      <Suspense fallback={<RuntimeLoading label="正在打开研发办公室…" />}>
        <RdWorkspacePhaseTwo />
      </Suspense>
    </>
  );
}
