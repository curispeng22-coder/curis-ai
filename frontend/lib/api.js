// 共享 API 层（T3）：统一注入 API_BASE + X-Tenant-Id（+ X-Ceo-Id）。
// 替代各页面重复拼接头；封装 companies / departments / employees / projects /
// affiliations（ADR-0017 红线项）/ capabilities 的 CRUD。
// 纯 fetch，不引入新依赖。

import { safeReturnPath } from "./auth.mjs";
import { normalizeAssistantIdentity } from "./assistantState.mjs";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";
const TENANT_ID = process.env.NEXT_PUBLIC_CURIS_TENANT_ID || "selfuse";
const CEO_ID = process.env.NEXT_PUBLIC_CEO_ID || "selfuse-ceo";

/**
 * 统一的 Workspace fetch：自动注入租户头，非 2xx 抛 Error（message 取自 payload.detail）。
 * @param {string} path 相对路径（以 / 开头）或完整 URL。
 * @param {RequestInit} [options]
 * @returns {Promise<any>}
 */
async function workspaceFetch(path, options = {}) {
  const { responseType, ...requestOptions } = options;
  const url = path.startsWith("http") ? path : `${API_BASE}${path}`;
  const headers = {
    "X-Tenant-Id": TENANT_ID,
    "X-Ceo-Id": CEO_ID,
    ...(requestOptions.headers || {}),
  };
  if (requestOptions.body && !headers["Content-Type"]) headers["Content-Type"] = "application/json";
  const response = await fetch(url, {
    ...requestOptions,
    headers,
    cache: "no-store",
    credentials: "include",
  });
  if (response.status === 401 && typeof window !== "undefined") {
    const current = `${window.location.pathname}${window.location.search}${window.location.hash}`;
    const returnTo = safeReturnPath(current, window.location.origin);
    window.location.replace(`/login?next=${encodeURIComponent(returnTo)}`);
  }
  if (!response.ok) {
    let detail = "";
    let stage = null;
    const credentialWrite = (path === "/api/workspace/credentials" && requestOptions.method === "POST") ||
      (/^\/api\/workspace\/credentials\/cred-[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}$/.test(path) && requestOptions.method === "PUT");
    try {
      const data = await response.json();
      if (!credentialWrite) detail = data && (data.detail || data.message) ? data.detail || data.message : "";
      const fixed = [
        ["CREDENTIAL_WRITE_NOT_STARTED", "validation", "not_started"],
        ["CREDENTIAL_WRITE_NOT_STARTED", "preflight", "not_started"],
        ["CREDENTIAL_NATIVE_WRITE_UNCONFIRMED", "native_store", "unknown"],
        ["CREDENTIAL_METADATA_UNCONFIRMED", "metadata", "native_returned_success"],
        ["CREDENTIAL_METADATA_UNCONFIRMED", "metadata", "not_started"],
        ["CREDENTIAL_AUDIT_FAILED", "audit", "metadata_returned_success"],
      ];
      if (credentialWrite && fixed.some(([code, phase, certainty]) => data?.code === code && data?.stage === phase && data?.certainty === certainty)) {
        stage = { code: data.code, phase: data.stage, certainty: data.certainty };
        if (Number.isInteger(data.os_status) && data.os_status >= -(2 ** 31) && data.os_status < 2 ** 31) stage.osStatus = data.os_status;
      }
    } catch (_err) {
      detail = "";
    }
    const error = new Error(credentialWrite ? "Credential save did not complete." : detail || response.statusText || `请求失败 (${response.status})`);
    error.status = response.status;
    if (stage) Object.assign(error, stage);
    throw error;
  }
  if (response.status === 204) return null;
  if (responseType === "blob") return response.blob();
  return response.json().catch(() => null);
}

/* ── Companies / Home ── */
export const getCompanies = () => workspaceFetch("/api/workspace/companies");
export const createCompany = (values) =>
  workspaceFetch("/api/workspace/companies", { method: "POST", body: JSON.stringify(values) });
export const updateCompany = (id, values) =>
  workspaceFetch(`/api/workspace/companies/${id}`, { method: "PATCH", body: JSON.stringify(values) });
export const getHomeSummary = () => workspaceFetch("/api/workspace/home/summary");

/* ── Departments ── */
export const getDepartments = () => workspaceFetch("/api/workspace/departments");
export const getDepartment = (id) => workspaceFetch(`/api/workspace/departments/${id}`);
export const createDepartment = (values) =>
  workspaceFetch("/api/workspace/departments", { method: "POST", body: JSON.stringify(values) });
export const updateDepartment = (id, values) =>
  workspaceFetch(`/api/workspace/departments/${id}`, { method: "PATCH", body: JSON.stringify(values) });
export const deleteDepartment = (id) =>
  workspaceFetch(`/api/workspace/departments/${id}`, { method: "DELETE" });

/* ── Employees ── */
export const getEmployees = () => workspaceFetch("/api/workspace/employees");
export const getEmployee = async (id) => {
  const payload = await getEmployees();
  const employee = (payload?.employees || []).find((item) => item.id === id);
  if (!employee) {
    const error = new Error("员工不存在或已移除");
    error.status = 404;
    throw error;
  }
  return employee;
};
export const getEmployeeAvatarBlob = (employeeId) =>
  workspaceFetch(`/api/workspace/employees/${encodeURIComponent(employeeId)}/avatar/content`, {
    responseType: "blob",
  });
export const getEmployeeTemplates = () => workspaceFetch("/api/workspace/employee-templates");
export const getEmployeeSkills = (employeeId) =>
  workspaceFetch(`/api/workspace/employees/${encodeURIComponent(employeeId)}/skills`);
export const getEmployeeTools = (employeeId) =>
  workspaceFetch(`/api/workspace/employees/${encodeURIComponent(employeeId)}/tools`);
export const getDepartmentTemplates = () => workspaceFetch("/api/workspace/department-templates");
export const createEmployee = (values) =>
  workspaceFetch("/api/workspace/employees", { method: "POST", body: JSON.stringify(values) });
export const updateEmployee = (id, values) =>
  workspaceFetch(`/api/workspace/employees/${id}`, { method: "PATCH", body: JSON.stringify(values) });
export const deleteEmployee = (id) =>
  workspaceFetch(`/api/workspace/employees/${id}`, { method: "DELETE" });

/* ── Projects ── */
export const getProjects = (companyId) =>
  workspaceFetch(
    companyId
      ? `/api/workspace/projects?company_id=${encodeURIComponent(companyId)}`
      : "/api/workspace/projects"
  );
export const getProject = (id) => workspaceFetch(`/api/workspace/projects/${id}`);
export const getProjectArtifacts = (id) =>
  workspaceFetch(`/api/workspace/projects/${id}/artifacts`);
export const createProject = (values) =>
  workspaceFetch("/api/workspace/projects", { method: "POST", body: JSON.stringify(values) });
export const updateProject = (id, values) =>
  workspaceFetch(`/api/workspace/projects/${id}`, { method: "PATCH", body: JSON.stringify(values) });
export const deleteProject = (id) =>
  workspaceFetch(`/api/workspace/projects/${id}`, { method: "DELETE" });
export const getTasks = () => workspaceFetch("/api/tasks");
export const createTask = (values) =>
  workspaceFetch("/api/task", { method: "POST", body: JSON.stringify(values) });
export const runTask = (taskId) =>
  workspaceFetch(`/api/task/${taskId}/run`, { method: "POST" });
export const getTask = (id) => workspaceFetch(`/api/task/${id}`);
export const getStrategyMeetings = () =>
  workspaceFetch("/api/workspace/strategy-meetings");
export const createStrategyMeeting = (values) =>
  workspaceFetch("/api/workspace/strategy-meetings", {
    method: "POST",
    body: JSON.stringify(values),
  });
const meetingPath = (companyId, suffix = "") =>
  `/api/workspace/runtime/foundation/companies/${encodeURIComponent(companyId)}/meetings${suffix}`;
export const getMeetings = (companyId) => workspaceFetch(meetingPath(companyId));
export const createMeeting = (companyId, values) =>
  workspaceFetch(meetingPath(companyId), { method: "POST", body: JSON.stringify(values) });
export const getMeeting = (companyId, meetingId) =>
  workspaceFetch(meetingPath(companyId, `/${encodeURIComponent(meetingId)}`));
export const addMeetingMessage = (companyId, meetingId, values) =>
  workspaceFetch(meetingPath(companyId, `/${encodeURIComponent(meetingId)}/messages`), {
    method: "POST", body: JSON.stringify(values),
  });
export const requestMeetingDecision = (companyId, meetingId, values) =>
  workspaceFetch(meetingPath(companyId, `/${encodeURIComponent(meetingId)}/decision`), {
    method: "POST", body: JSON.stringify(values),
  });
export const reviewMeetingDecision = (companyId, meetingId) =>
  workspaceFetch(meetingPath(companyId, `/${encodeURIComponent(meetingId)}/decision/review`), { method: "POST" });
export const chooseMeetingDecision = (companyId, meetingId, values) =>
  workspaceFetch(meetingPath(companyId, `/${encodeURIComponent(meetingId)}/decision/choose`), {
    method: "POST", body: JSON.stringify(values),
  });
export const syncMeeting = (companyId, meetingId) =>
  workspaceFetch(meetingPath(companyId, `/${encodeURIComponent(meetingId)}/sync`), { method: "POST" });
export const closeMeeting = (companyId, meetingId) =>
  workspaceFetch(meetingPath(companyId, `/${encodeURIComponent(meetingId)}/close`), { method: "POST" });
export const createProjectTask = (projectId, values) =>
  workspaceFetch(`/api/workspace/projects/${projectId}/tasks`, {
    method: "POST",
    body: JSON.stringify(values),
  });
export const startTaskJob = (projectId, taskId) =>
  workspaceFetch(`/api/workspace/projects/${projectId}/tasks/${taskId}/jobs`, {
    method: "POST",
  });
export const getTaskJob = (jobId) => workspaceFetch(`/api/workspace/jobs/${jobId}`);
export const getTaskRun = (taskRunId) =>
  workspaceFetch(`/api/workspace/task-runs/${taskRunId}`);
export const getTaskRunTimeline = (taskRunId) =>
  workspaceFetch(`/api/workspace/task-runs/${taskRunId}/timeline`);
export const pauseTaskForInput = (taskRunId, values) =>
  workspaceFetch(`/api/workspace/task-runs/${taskRunId}/awaiting-input`, {
    method: "POST",
    body: JSON.stringify(values),
  });
export const supplyTaskInput = (taskRunId, values) =>
  workspaceFetch(`/api/workspace/task-runs/${taskRunId}/input`, {
    method: "POST",
    body: JSON.stringify(values),
  });
export const requestTaskHandoff = (taskRunId, values) =>
  workspaceFetch(`/api/workspace/task-runs/${taskRunId}/handoff`, {
    method: "POST",
    body: JSON.stringify(values),
  });
export const acceptTaskHandoff = (taskRunId) =>
  workspaceFetch(`/api/workspace/task-runs/${taskRunId}/handoff/accept`, {
    method: "POST",
  });
export const reassignTaskHandoff = (taskRunId, assigneeId) =>
  workspaceFetch(`/api/workspace/task-runs/${taskRunId}/handoff/assignee`, {
    method: "PATCH",
    body: JSON.stringify({ assignee_id: assigneeId }),
  });
export const resumeTaskRun = (taskRunId) =>
  workspaceFetch(`/api/workspace/task-runs/${taskRunId}/resume`, {
    method: "POST",
    body: JSON.stringify({}),
  });
export const cancelTaskRun = (taskRunId, reason = "") =>
  workspaceFetch(`/api/workspace/task-runs/${taskRunId}/cancel`, {
    method: "POST",
    body: JSON.stringify({ reason }),
  });

/* ── Global Assistant Runtime ── */
export const getAssistantIdentity = () =>
  workspaceFetch("/api/workspace/assistant/identity");
export const updateAssistantIdentity = (values) =>
  workspaceFetch("/api/workspace/assistant/identity", {
    method: "PUT",
    body: JSON.stringify(normalizeAssistantIdentity(values)),
  });
export const getAssistantSnapshot = () =>
  workspaceFetch("/api/workspace/assistant/snapshot");
export const getAssistantNotifications = (afterEventId = 0) =>
  workspaceFetch(
    `/api/workspace/assistant/notifications?after_event_id=${encodeURIComponent(afterEventId)}`
  );
export const submitAssistantCommand = (command, intent, context) =>
  workspaceFetch("/api/workspace/assistant/commands", {
    method: "POST",
    body: JSON.stringify({ command, intent, context }),
  });

/* ── Affiliations（ADR-0017 红线项）── */
export const setEmployeeAffiliations = (employeeId, affiliations) =>
  workspaceFetch("/api/workspace/employee-affiliations", {
    method: "POST",
    body: JSON.stringify({ employee_id: employeeId, affiliations }),
  });
export const listAffiliationsByEmployee = (employeeId) =>
  workspaceFetch(`/api/workspace/employee-affiliations?employee_id=${encodeURIComponent(employeeId)}`);
export const listAffiliationsByDepartment = (departmentId) =>
  workspaceFetch(`/api/workspace/employee-affiliations?department_id=${encodeURIComponent(departmentId)}`);
export const listAffiliationsByProject = (projectId) =>
  workspaceFetch(`/api/workspace/employee-affiliations?project_id=${encodeURIComponent(projectId)}`);
export const deleteAffiliation = (id) =>
  workspaceFetch(`/api/workspace/employee-affiliations/${id}`, { method: "DELETE" });

/* ── Capabilities（复用既有端点）── */
export const getEmployeeCapabilities = (employeeId) =>
  workspaceFetch(`/api/workspace/employees/${employeeId}/capabilities`);
export const setEmployeeCapabilities = (employeeId, bindings, executionPermission) =>
  workspaceFetch(`/api/workspace/employees/${employeeId}/capabilities`, {
    method: "PUT",
    body: JSON.stringify({ bindings, ...(executionPermission ? { execution_permission: executionPermission } : {}) }),
  });
export const getCapabilitySelector = () =>
  workspaceFetch("/api/workspace/capabilities/selector");

/* ── 业务工作台引导（Workbench Guide）── */
export const listGuides = () => workspaceFetch("/api/workspace/guides");
export const startGuideSession = (guideId) =>
  workspaceFetch("/api/workspace/guides/sessions", {
    method: "POST",
    body: JSON.stringify({ guide_id: guideId }),
  });
export const answerGuideSession = (sessionId, step, answer) =>
  workspaceFetch(`/api/workspace/guides/sessions/${sessionId}/answer`, {
    method: "POST",
    body: JSON.stringify({ step, answer }),
  });
export const confirmGuideSession = (sessionId, blueprint) =>
  workspaceFetch(`/api/workspace/guides/sessions/${sessionId}/confirm`, {
    method: "POST",
    body: JSON.stringify({ blueprint }),
  });
export const abandonGuideSession = (sessionId) =>
  workspaceFetch(`/api/workspace/guides/sessions/${sessionId}/abandon`, {
    method: "POST",
  });

/* ── CEO 经营日 / 运行时 trace（Phase-9 / EvoFlow A2）── */
export const getOperatingDay = (params = {}) => {
  const query = new URLSearchParams(
    Object.entries(params).filter(([, value]) => value != null && value !== "")
  ).toString();
  return workspaceFetch(`/api/workspace/ceo/operating-day${query ? `?${query}` : ""}`);
};
export const getRuntimeTrace = (params = {}) => {
  const query = new URLSearchParams(
    Object.entries(params).filter(([, value]) => value != null && value !== "")
  ).toString();
  return workspaceFetch(`/api/workspace/runtime-trace${query ? `?${query}` : ""}`);
};

/* ── Pipeline：规划 → 任务图 → 队列 → 调度 → 验收 → 返工 ──
 * 后端 backend/app/issue_pipeline_api.py（prefix /api/pipeline）。
 * 任务状态机：pending → queued → running → review → approved | rejected；
 * rework 把 review 打回 pending（上限 2 次）。
 * 注意：任务对象本身不直接返回 graph_id，需从 issue_spec.pipeline_graph_id 取，
 * 统一用 pickGraphId() 提取，避免各页面各写一份。
 */

/** 从 pipeline 任务对象里提取 graph_id（submit 直接返回的除外）。 */
export const pickGraphId = (task) =>
  task?.graph_id || task?.issue_spec?.pipeline_graph_id || null;

/** 提交自然语言需求 → 生成 issue_spec + 任务图。返回 {id, graph_id, status, questions?} */
export const submitPipelineTask = (values) =>
  workspaceFetch("/api/pipeline/submit", { method: "POST", body: JSON.stringify(values) });

/** 全部 pipeline 任务列表。 */
export const listPipelineTasks = () => workspaceFetch("/api/pipeline/list");

/** 单个任务详情（含 executor_result / rework_feedback / review_note）。 */
export const getPipelineTask = (taskId) => workspaceFetch(`/api/pipeline/${taskId}`);

/** 手动派发一个任务（pending/queued → running，后台线程执行）。 */
export const dispatchPipelineTask = (taskId) =>
  workspaceFetch(`/api/pipeline/${taskId}/dispatch`, { method: "POST" });

/** 验收通过（review → approved）。 */
export const approvePipelineTask = (taskId) =>
  workspaceFetch(`/api/pipeline/${taskId}/approve`, { method: "POST" });

/** 驳回（review → rejected，终态）。 */
export const rejectPipelineTask = (taskId, note = "") =>
  workspaceFetch(`/api/pipeline/${taskId}/reject`, {
    method: "POST",
    body: JSON.stringify({ note }),
  });

/** 返工（review → pending，rework_count+1，上限 2）。 */
export const reworkPipelineTask = (taskId, note = "手动触发返工") =>
  workspaceFetch(`/api/pipeline/${taskId}/rework`, {
    method: "POST",
    body: JSON.stringify({ note }),
  });

/** 任务图（DAG）：节点、依赖、触发、状态、进度。 */
export const getPipelineGraph = (graphId) => workspaceFetch(`/api/pipeline/${graphId}/graph`);

/** 启动常驻自动调度：按就绪态自动拉节点，跑完自动置 review。 */
export const autoRunPipelineGraph = (graphId) =>
  workspaceFetch(`/api/pipeline/${graphId}/auto-run`, { method: "POST" });

/** 执行 trace（含能力降级链）。 */
export const getPipelineTrace = (graphId) => workspaceFetch(`/api/pipeline/${graphId}/trace`);

/** 项目视角的运行时读模型（project + task + graph + trace + available_actions）。 */
export const getPipelineProjectRuntime = (projectId) =>
  workspaceFetch(`/api/pipeline/project/${projectId}`);

/** 经验沉淀查询。 */
export const getPipelineLessons = (params = {}) => {
  const query = new URLSearchParams(
    Object.entries(params).filter(([, value]) => value != null && value !== "")
  ).toString();
  return workspaceFetch(`/api/pipeline/lessons${query ? `?${query}` : ""}`);
};

export { API_BASE, TENANT_ID, CEO_ID, workspaceFetch };
