"use client";

// T-017 / W03-A：首次执行任务入口。
// 本分支（基于 t-011）尚无 W04-A 首屏「任务输入」入口，故新增这一最小执行入口页面，
// 把 FirstTaskModelSetup 挂到真实 RuntimeProvider 数据上；不改既有首页/对话组件，避免回归。

import { useRuntime } from "../../../components/runtime/RuntimeProvider.js";
import FirstTaskModelSetup from "../../../components/v1/FirstTaskModelSetup.js";

export default function FirstTaskPage() {
  const runtime = useRuntime();
  const teams = Array.isArray(runtime.teams) ? runtime.teams : [];
  const writing = teams.find((team) => team && team.kind === "writing");
  return <FirstTaskModelSetup
    runtimeStatus={runtime.status}
    teams={teams}
    companyId={runtime.companyId || ""}
    writingWorkspaceId={writing?.workspace_id || ""}
  />;
}
