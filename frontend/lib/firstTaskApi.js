// T-017 / W03-A 前端：首启与写作任务草稿的 API 封装（复用 workspaceFetch，不新增依赖）。
// 路径与字段以后端 frontend_v1_router.py / first_launch_service.py 实际实现为准。

import { workspaceFetch } from "./api.js";

const companyWriting = (companyId, workspaceId) =>
  `/api/workspace/v1/companies/${encodeURIComponent(companyId)}/writing/${encodeURIComponent(workspaceId)}`;

// POST /api/workspace/v1/first-launch -> { company_id, teams, next_action }
export const firstLaunch = () =>
  workspaceFetch("/api/workspace/v1/first-launch", { method: "POST" });

// PUT .../writing/{workspace_id}/task-draft  body { draft_id, text, expected_revision }
export const saveWritingTaskDraft = (companyId, workspaceId, { draftId, text, expectedRevision }) =>
  workspaceFetch(`${companyWriting(companyId, workspaceId)}/task-draft`, {
    method: "PUT",
    body: JSON.stringify({ draft_id: draftId, text, expected_revision: expectedRevision }),
  });

// GET .../writing/{workspace_id}/task-drafts/{work_id}
export const readWritingTaskDraft = (companyId, workspaceId, workId) =>
  workspaceFetch(`${companyWriting(companyId, workspaceId)}/task-drafts/${encodeURIComponent(workId)}`);
