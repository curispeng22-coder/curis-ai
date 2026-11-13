"use client";

import { useParams } from "next/navigation";

import InstalledWorkspaceRuntime from "../../../../../components/workspace/InstalledWorkspaceRuntime.js";


export default function InstalledWorkspacePage() {
  const params = useParams();
  return <InstalledWorkspaceRuntime workspaceId={String(params?.workspaceId || "")} />;
}
