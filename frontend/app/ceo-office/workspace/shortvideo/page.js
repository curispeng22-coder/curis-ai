"use client";

import { Suspense } from "react";

import WorkspaceRuntimeView from "../../../../components/runtime/WorkspaceRuntimeView.js";
import { RuntimeLoading } from "../../../../components/runtime/RuntimeStates.js";
import LegacyOfficeScopeNotice from "../../../../components/workspace/LegacyOfficeScopeNotice.js";


export default function ShortVideoRuntimePage() {
  return (
    <>
      <LegacyOfficeScopeNotice label="抖音 / TikTok（电商）业务" />
      <Suspense fallback={<RuntimeLoading label="正在打开抖音 / TikTok 运营办公室…" />}>
        <WorkspaceRuntimeView businessType="TTK" />
      </Suspense>
    </>
  );
}
