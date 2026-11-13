import { workspaceFetch } from "./api.js";

const PREFIX = "/api/workspace/runtime/foundation";

export function runtimeErrorMessage(error) {
  if (error?.status === 401) return "登录状态已失效，正在返回登录页。";
  if (error?.status === 403 || error?.status === 404) return "无权访问该运行对象，或对象已不存在。";
  if (error?.status === 409) return "当前状态不允许执行这个操作，请刷新后重试。";
  if (error?.status === 422) return "提交内容不符合当前运行规则，请检查后重试。";
  return "运行状态暂时无法读取，请稍后重试。";
}

export function pickCurrentCompany(payload) {
  const companies = Array.isArray(payload) ? payload : payload?.companies || [];
  return companies.find((item) => item.is_default) || companies[0] || null;
}

export async function getRuntimeCompany(companyId, request = workspaceFetch) {
  return request(`${PREFIX}/companies/${encodeURIComponent(companyId)}`);
}

export async function getRuntimeCompanies(request = workspaceFetch) {
  return request(`${PREFIX}/companies`);
}

export async function getCanonicalBusinesses(companyId, request = workspaceFetch) {
  return request(`${PREFIX}/companies/${encodeURIComponent(companyId)}/businesses`);
}

export async function getOrganizationProjection(companyId, request = workspaceFetch) {
  return request(`${PREFIX}/companies/${encodeURIComponent(companyId)}/organization`);
}

export async function getOperatingIntelligence(companyId, options = {}, request = workspaceFetch) {
  const query = new URLSearchParams({ days: String(options.days || 30) });
  if (options.businessId) query.set("business_id", options.businessId);
  return request(`${PREFIX}/companies/${encodeURIComponent(companyId)}/operating-intelligence?${query}`);
}

export const submitOperatingReportDecision = (companyId, artifactId, request = workspaceFetch) =>
  request(
    `${PREFIX}/companies/${encodeURIComponent(companyId)}/operating-intelligence/reports/${encodeURIComponent(artifactId)}/decision`,
    { method: "POST" }
  );

export async function getCanonicalBusiness(companyId, businessId, request = workspaceFetch) {
  return request(
    `${PREFIX}/companies/${encodeURIComponent(companyId)}/businesses/${encodeURIComponent(businessId)}`
  );
}

export async function getWorkspaceParentPath(workspaceId, request = workspaceFetch) {
  return request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/parent-path`);
}

export async function getWorkspaceSimulations(companyId, workspaceId, request = workspaceFetch) {
  return request(
    `${PREFIX}/companies/${encodeURIComponent(companyId)}/workspaces/${encodeURIComponent(workspaceId)}/simulations`
  );
}

export const createRuntimeSimulation = (workspaceId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/simulations`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const startRuntimeSimulation = (workspaceId, simulationId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/simulations/${encodeURIComponent(simulationId)}/transition`, {
    method: "POST",
    body: JSON.stringify({ ...values, target: "RUNNING" }),
  });

export const executeRuntimeSimulation = (workspaceId, simulationId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/simulations/${encodeURIComponent(simulationId)}/execute`, {
    method: "POST",
    body: JSON.stringify({ ...values, target: "RUNNING" }),
  });

export const reviewRuntimeSimulation = (workspaceId, simulationId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/simulations/${encodeURIComponent(simulationId)}/review`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const getCapabilitySupplyReview = (companyId, workspaceId, request = workspaceFetch) =>
  request(
    `${PREFIX}/companies/${encodeURIComponent(companyId)}/workspaces/${encodeURIComponent(workspaceId)}/capability-supply-review`
  );

export const reviewCapabilitySupply = (workspaceId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/capability-supply-review`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const getStaffingApproval = (companyId, workspaceId, request = workspaceFetch) =>
  request(
    `${PREFIX}/companies/${encodeURIComponent(companyId)}/workspaces/${encodeURIComponent(workspaceId)}/staffing-approval`
  );

export const decideStaffing = (workspaceId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/staffing-decision`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const rollbackStaffing = (workspaceId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/staffing-rollback`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export async function getRuntimeWorkspace(companyId, workspaceId, request = workspaceFetch) {
  return request(
    `${PREFIX}/companies/${encodeURIComponent(companyId)}/workspaces/${encodeURIComponent(workspaceId)}`
  );
}

export const getGeneralWorkspace = (companyId, workspaceId, request = workspaceFetch) =>
  request(
    `${PREFIX}/companies/${encodeURIComponent(companyId)}/workspaces/${encodeURIComponent(workspaceId)}/shared/general`
  );

export const createGeneralWorkspaceWork = (companyId, workspaceId, values, request = workspaceFetch) =>
  request(
    `${PREFIX}/companies/${encodeURIComponent(companyId)}/workspaces/${encodeURIComponent(workspaceId)}/shared/general/works`,
    { method: "POST", body: JSON.stringify(values) }
  );

export const materializeGeneralWorkspaceTeam = (companyId, workspaceId, request = workspaceFetch) =>
  request(
    `${PREFIX}/companies/${encodeURIComponent(companyId)}/workspaces/${encodeURIComponent(workspaceId)}/shared/general/team/materialize`,
    { method: "POST" }
  );

export const getGeneralWorkspaceTeamCandidates = (companyId, workspaceId, request = workspaceFetch) =>
  request(
    `${PREFIX}/companies/${encodeURIComponent(companyId)}/workspaces/${encodeURIComponent(workspaceId)}/shared/general/team/candidates`
  );

export const assignGeneralWorkspaceEmployee = (companyId, workspaceId, values, request = workspaceFetch) =>
  request(
    `${PREFIX}/companies/${encodeURIComponent(companyId)}/workspaces/${encodeURIComponent(workspaceId)}/shared/general/team/assign`,
    { method: "POST", body: JSON.stringify(values) }
  );

export const reviewGeneralWorkspaceDecision = (companyId, workspaceId, workRef, request = workspaceFetch) =>
  request(
    `${PREFIX}/companies/${encodeURIComponent(companyId)}/workspaces/${encodeURIComponent(workspaceId)}/shared/general/works/${encodeURIComponent(workRef)}/decision/review`,
    { method: "POST" }
  );

export const chooseGeneralWorkspaceDecision = (companyId, workspaceId, workRef, values, request = workspaceFetch) =>
  request(
    `${PREFIX}/companies/${encodeURIComponent(companyId)}/workspaces/${encodeURIComponent(workspaceId)}/shared/general/works/${encodeURIComponent(workRef)}/decision/choose`,
    { method: "POST", body: JSON.stringify(values) }
  );

export const getGeneralWorkspaceResult = (companyId, workspaceId, referenceId, request = workspaceFetch) =>
  request(
    `${PREFIX}/companies/${encodeURIComponent(companyId)}/workspaces/${encodeURIComponent(workspaceId)}/shared/results/${encodeURIComponent(referenceId)}`
  );

export const executeGeneralWorkspaceWork = (workRef, request = workspaceFetch, limits = null) => {
  if (limits !== null && (Object.keys(limits).sort().join(",") !== "max_output_tokens,max_prompt_bytes"
    || !Number.isInteger(limits.max_output_tokens) || limits.max_output_tokens < 1 || limits.max_output_tokens > 2048
    || !Number.isInteger(limits.max_prompt_bytes) || limits.max_prompt_bytes < 1 || limits.max_prompt_bytes > 4096)) throw new Error("执行限制不符合当前范围。");
  return request(`${PREFIX}/team-operating/works/${encodeURIComponent(workRef)}/execute?max_executions=1`, {
    method: "POST", ...(limits === null ? {} : { body: JSON.stringify(limits) }),
  });
};

export const controlGeneralWorkspaceWork = (companyId, workspaceId, workRef, action, values = {}, request = workspaceFetch) =>
  request(
    `${PREFIX}/companies/${encodeURIComponent(companyId)}/workspaces/${encodeURIComponent(workspaceId)}/shared/general/works/${encodeURIComponent(workRef)}/lifecycle/${encodeURIComponent(action)}`,
    { method: "POST", body: JSON.stringify(values) }
  );

export const reportGeneralHumanInput = (companyId, workspaceId, workRef, requestId, values, request = workspaceFetch) =>
  request(`${PREFIX}/companies/${encodeURIComponent(companyId)}/workspaces/${encodeURIComponent(workspaceId)}/shared/general/works/${encodeURIComponent(workRef)}/human-input/${encodeURIComponent(requestId)}/report`, {
    method: "POST", body: JSON.stringify(values),
  });

export const reviewGeneralHumanInput = (companyId, workspaceId, workRef, requestId, revision, request = workspaceFetch) =>
  request(`${PREFIX}/companies/${encodeURIComponent(companyId)}/workspaces/${encodeURIComponent(workspaceId)}/shared/general/works/${encodeURIComponent(workRef)}/human-input/${encodeURIComponent(requestId)}/review`, {
    method: "POST", body: JSON.stringify({ revision }),
  });

export const continueGeneralHumanInput = (workRef, requestId, revision, submissionId, request = workspaceFetch) =>
  request(`${PREFIX}/team-operating/works/${encodeURIComponent(workRef)}/human-input/${encodeURIComponent(requestId)}/continue`, {
    method: "POST", body: JSON.stringify({ revision, submission_id: submissionId }),
  });

export const createRuntimeWorkspace = (companyId, values, request = workspaceFetch) =>
  request(`${PREFIX}/companies/${encodeURIComponent(companyId)}/workspaces`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const createRuntimeCycle = (workspaceId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/cycles`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const startOperatingCycle = (workspaceId, cycleId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/cycles/${encodeURIComponent(cycleId)}/start`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const executeOperatingCycle = (workspaceId, cycleId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/cycles/${encodeURIComponent(cycleId)}/execute`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const createArtifactReview = (workspaceId, cycleId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/cycles/${encodeURIComponent(cycleId)}/artifact-review`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const executeArtifactReview = (workspaceId, cycleId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/cycles/${encodeURIComponent(cycleId)}/artifact-review/execute`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const createResponsibilityHandoff = (workspaceId, cycleId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/cycles/${encodeURIComponent(cycleId)}/responsibility-handoff`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const sendResponsibilityHandoff = (workspaceId, cycleId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/cycles/${encodeURIComponent(cycleId)}/responsibility-handoff/send`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const reviewRDDecision = (workspaceId, cycleId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/cycles/${encodeURIComponent(cycleId)}/rd-decision/review`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const chooseRDDecision = (workspaceId, cycleId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/cycles/${encodeURIComponent(cycleId)}/rd-decision/choose`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const resumeOperatingCycle = (workspaceId, cycleId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/cycles/${encodeURIComponent(cycleId)}/resume`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const reviewOperatingCycle = (workspaceId, cycleId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/cycles/${encodeURIComponent(cycleId)}/review`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const closeOperatingCycle = (workspaceId, cycleId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/cycles/${encodeURIComponent(cycleId)}/close`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const getTeamOperatingDefinition = (values, request = workspaceFetch) => {
  const query = new URLSearchParams({
    company_id: values.companyId,
    scope_type: values.scopeType,
    scope_ref: values.scopeRef,
    workflow_key: values.workflowKey,
  });
  if (values.workspaceId) query.set("workspace_id", values.workspaceId);
  return request(`${PREFIX}/team-operating/definition?${query.toString()}`);
};

export const publishTeamOperatingDefinition = (values, request = workspaceFetch) =>
  request(`${PREFIX}/team-operating/definitions/publish`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const createRuntimeContentItem = (workspaceId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/content-items`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const acceptRuntimeContentIdea = (workspaceId, contentId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/content-items/${encodeURIComponent(contentId)}/accept-idea`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const setRuntimeContentWorkContext = (workspaceId, contentId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/content-items/${encodeURIComponent(contentId)}/work-context`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const decideRuntimeContentReview = (workspaceId, contentId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/content-items/${encodeURIComponent(contentId)}/decision`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const executeRuntimeContentStage = (workspaceId, contentId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/content-items/${encodeURIComponent(contentId)}/execute`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const createRuntimeContentVersion = (workspaceId, contentId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/content-items/${encodeURIComponent(contentId)}/versions`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export function getRuntimeWorkspaceDetails(companyId, workspaces, request = workspaceFetch) {
  return Promise.all(
    (workspaces || []).map((workspace) =>
      getRuntimeWorkspace(companyId, workspace.workspace_id, request)
    )
  );
}

export async function getRuntimeBootstrap(request = workspaceFetch) {
  const directory = await getRuntimeCompanies(request);
  const current = pickCurrentCompany(directory);
  const companyId = current?.company_id || current?.id || "";
  if (!companyId) return { companyId: "", snapshot: null, simulations: [] };

  const snapshot = await getRuntimeCompany(companyId, request);
  const groups = [];
  for (const workspace of snapshot?.workspaces || []) {
    groups.push(await getWorkspaceSimulations(companyId, workspace.workspace_id, request));
  }
  return {
    companyId,
    snapshot,
    simulations: groups.flatMap((group) => group?.simulations || []),
  };
}

export const createFoundingRun = (values, request = workspaceFetch) =>
  request(`${PREFIX}/founding-runs`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const getFoundingRun = (foundingRunId, request = workspaceFetch) =>
  request(`${PREFIX}/founding-runs/${encodeURIComponent(foundingRunId)}`);

export const materializeFoundingCompany = (foundingRunId, values, request = workspaceFetch) =>
  request(`${PREFIX}/founding-runs/${encodeURIComponent(foundingRunId)}/materialize-company`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const transitionRuntimeEntity = (entityId, values, request = workspaceFetch) =>
  request(`${PREFIX}/entities/${encodeURIComponent(entityId)}/transition`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export function workspaceEntryHref(workspaceId) {
  return `/ceo-office/workspace?workspace_id=${encodeURIComponent(workspaceId)}`;
}

// Legacy pre-package business types (RD / 小红书 XHS / 抖音 TTK) are frozen out of V1
// scope (CURIS-V1-LEGACY-RD-XHS-TTK-FREEZE-20261007, CEO decision 2026-10-07). Their
// dedicated office pages remain readable by direct URL but must never be linked from V1
// entry surfaces; XHS lives on as a *platform* inside the Content Growth package chain.
export const LEGACY_OFFICE_TYPES = ["RD", "XHS", "TTK"];

export function isLegacyOfficeType(businessType) {
  return LEGACY_OFFICE_TYPES.includes(String(businessType || "").toUpperCase());
}

export function workspaceOfficeHref(workspace) {
  const type = String(workspace?.business_type || "").toUpperCase();
  if (type === "PACKAGE") {
    return `/ceo-office/workspace/installed/${encodeURIComponent(workspace?.workspace_id || "")}`;
  }
  // Legacy RD/XHS/TTK offices are frozen out of V1; never deep-link to their dedicated
  // pages. Historical workspaces fall back to the generic read-only workspace entry.
  return workspaceEntryHref(workspace?.workspace_id || "");
}
