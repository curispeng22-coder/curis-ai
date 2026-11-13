import { workspaceFetch } from "./api.js";
export const continueOriginalAgentWork = (work, payload) => workspaceFetch(
  "/api/workspace/runtime/foundation/team-operating/works/" + encodeURIComponent(work) + "/follow-up",
  { method: "POST", body: JSON.stringify(payload) });
export const getAgentCandidateSource = (work, task, artifact) => workspaceFetch("/api/workspace/runtime/foundation/team-operating/works/" + encodeURIComponent(work) + "/candidate-source/" + encodeURIComponent(task) + (artifact ? "?" + new URLSearchParams({ artifact_ref: artifact }) : ""));
export const createAgentCandidate = (work, payload) => workspaceFetch("/api/workspace/runtime/foundation/team-operating/works/" + encodeURIComponent(work) + "/candidate", { method: "POST", body: JSON.stringify(payload) });
export const getOriginalAgentFile = (work, artifact) => workspaceFetch("/api/workspace/runtime/foundation/team-operating/works/" + encodeURIComponent(work) + "/files/" + encodeURIComponent(artifact));

const conversationsPath = (company) => `/api/workspace/v1/companies/${encodeURIComponent(company)}/conversations`;
export const getAssignedAgentWorkflow = (assignment, company, workspace) => workspaceFetch(
  "/api/workspace/runtime/foundation/team-operating/assignments/" + encodeURIComponent(assignment) + "/agent-workflow?" +
  new URLSearchParams({ company_id: company, workspace_id: workspace }));
export const publishAssignedAgentWorkflow = (assignment, payload) => workspaceFetch(
  "/api/workspace/runtime/foundation/team-operating/assignments/" + encodeURIComponent(assignment) + "/agent-workflow",
  { method: "POST", body: JSON.stringify(payload) });
export const createAssignedWork = (assignment, payload) => workspaceFetch(`/api/workspace/runtime/foundation/team-operating/assignments/${encodeURIComponent(assignment)}/work`, { method: "POST", body: JSON.stringify(payload) });
export const getOriginalAgentWork = (work) => workspaceFetch(`/api/workspace/runtime/foundation/team-operating/works/${encodeURIComponent(work)}`);
export const executeOriginalAgentWork = (work) => workspaceFetch(`/api/workspace/runtime/foundation/team-operating/works/${encodeURIComponent(work)}/execute?max_executions=1`, { method: "POST" });
export const stopOriginalAgentWork = (work) => workspaceFetch(`/api/workspace/runtime/foundation/team-operating/works/${encodeURIComponent(work)}/cancel`, { method: "POST", body: JSON.stringify({ reason: "用户停止当前 Agent 工作" }) });
export const getRecentConversations = (company) => workspaceFetch(conversationsPath(company));
export const getConversationEmployees = (company) => workspaceFetch(`${conversationsPath(company)}/employees`);
export const getConversation = (company, id) => workspaceFetch(`${conversationsPath(company)}/${encodeURIComponent(id)}`);
export const createConversation = (company, value) => workspaceFetch(conversationsPath(company), { method: "POST", body: JSON.stringify(value) });
export const joinConversation = (company, id, employee_ref) => workspaceFetch(`${conversationsPath(company)}/${encodeURIComponent(id)}/employee`, { method: "POST", body: JSON.stringify({ employee_ref }) });
export const dismissConversation = (company, id) => workspaceFetch(`${conversationsPath(company)}/${encodeURIComponent(id)}/dismiss`, { method: "POST" });
export const sendConversation = (company, id, value) => workspaceFetch(`${conversationsPath(company)}/${encodeURIComponent(id)}/messages`, { method: "POST", body: JSON.stringify(value) });

export const getV1Presentation = () => workspaceFetch("/api/workspace/v1/presentation");
export const saveV1Presentation = (value) => workspaceFetch("/api/workspace/v1/presentation", {
  method: "PUT",
  body: JSON.stringify(value),
});

export const getCompanyAttention = (companyId) =>
  workspaceFetch(`/api/workspace/v1/companies/${encodeURIComponent(companyId)}/attention`);

export const getResultDetail = (companyId, workspaceId, referenceId) => workspaceFetch(
  `/api/workspace/v1/companies/${encodeURIComponent(companyId)}/result-detail?${new URLSearchParams({ workspace_id: workspaceId, result_ref: referenceId })}`
);
export const markResultViewed = (companyId, workspaceId, result) => workspaceFetch(
  `/api/workspace/v1/companies/${encodeURIComponent(companyId)}/result-viewed`,
  { method: "POST", body: JSON.stringify({ workspace_id: workspaceId, result_ref: result.reference_id, result_version: result.result_version }) }
);

export function conversationError(error, fallback = "暂时无法完成操作。输入已保留，请稍后重试。") {
  const status = error?.status || error?.statusCode;
  if ([401, 403, 404].includes(status)) return "当前身份无法读取这项内容，请返回原工作空间确认访问权限。";
  if (status === 409) return "这项内容的状态已变化，请重新读取后继续。";
  return fallback; // Raw SQL/provider/IPC errors never become conversation copy.
}

export const getCEOAssistantConversation = (companyId) =>
  workspaceFetch(`/api/workspace/v1/companies/${encodeURIComponent(companyId)}/assistant/conversation`);

export const sendCEOAssistantMessage = (companyId, values) =>
  workspaceFetch(`/api/workspace/v1/companies/${encodeURIComponent(companyId)}/assistant/conversation`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const getAIProviders = () => workspaceFetch("/api/workspace/ai-capabilities/providers");
export const getEnabledModels = () => workspaceFetch("/api/workspace/private-models");
export const getModelPreference = () => workspaceFetch("/api/workspace/model-preference");
export const setModelPreference = (modelKey) => workspaceFetch("/api/workspace/model-preference", {
  method: "PUT",
  body: JSON.stringify({ model_key: modelKey }),
});
export const createSessionCredential = (provider, secret) => workspaceFetch("/api/workspace/credentials", {
  method: "POST",
  body: JSON.stringify({
    name: `${provider} 当前会话凭证`,
    provider,
    credential_type: "api_key",
    secret,
  }),
});
export const updateCredential = (credentialId, provider, secret) => workspaceFetch(
  `/api/workspace/credentials/${encodeURIComponent(credentialId)}`,
  {
    method: "PUT",
    body: JSON.stringify({ provider, credential_type: "api_key", secret }),
  }
);
export const connectAIProvider = (providerId, values) =>
  workspaceFetch(`/api/workspace/ai-capabilities/providers/${encodeURIComponent(providerId)}/connect`, {
    method: "POST",
    body: JSON.stringify(values),
  });
export const recoverAIProvider = (providerId) =>
  workspaceFetch(`/api/workspace/ai-capabilities/providers/${encodeURIComponent(providerId)}/recover`, {
    method: "POST",
  });

export const createBusinessFromFoundingRun = (companyId, foundingRunId, values) =>
  workspaceFetch(
    `/api/workspace/v1/companies/${encodeURIComponent(companyId)}/founding-runs/${encodeURIComponent(foundingRunId)}/business`,
    { method: "POST", body: JSON.stringify(values) }
  );

export const saveBusinessDraft = (foundingRunId, values) =>
  workspaceFetch(`/api/workspace/v1/founding-runs/${encodeURIComponent(foundingRunId)}/business-draft`, {
    method: "PUT",
    body: JSON.stringify(values),
  });

export const getBusinessDraft = (foundingRunId) =>
  workspaceFetch(`/api/workspace/v1/founding-runs/${encodeURIComponent(foundingRunId)}/business-draft`);

const employeeConversationPath = (company, employee) => `/api/workspace/v1/companies/${encodeURIComponent(company)}/employees/${encodeURIComponent(employee)}/conversation`;
export const getEmployeeConversation = (company, employee) => workspaceFetch(employeeConversationPath(company, employee));
export const getEmployeeConversationReferences = (company, employee, assignment) => workspaceFetch(employeeConversationPath(company, employee) + "/references?assignment_ref=" + encodeURIComponent(assignment));
export const openEmployeeConversation = (company, employee) => workspaceFetch(employeeConversationPath(company, employee) + "/open", { method: "POST" });
export const sendEmployeeConversation = (company, employee, payload) => workspaceFetch(employeeConversationPath(company, employee) + "/messages", { method: "POST", body: JSON.stringify(payload) });

export const getBusinessDefinitions = (companyId) => workspaceFetch(`/api/workspace/v1/companies/${encodeURIComponent(companyId)}/business-definitions`);
export const getBusinessCreationResult = (companyId, runId) => workspaceFetch(`/api/workspace/v1/companies/${encodeURIComponent(companyId)}/founding-runs/${encodeURIComponent(runId)}/business-result`);

export const searchCompanyObjects = (companyId, query) =>
  workspaceFetch(`/api/workspace/companies/${encodeURIComponent(companyId)}/object-search?q=${encodeURIComponent(query || "")}`);

export const getCompanyTextPolicy = (company) => workspaceFetch(`/api/workspace/v1/companies/${encodeURIComponent(company)}/text-execution-policy`);
export const saveCompanyTextPolicy = (company, value) => workspaceFetch(`/api/workspace/v1/companies/${encodeURIComponent(company)}/text-execution-policy`, { method: "PUT", body: JSON.stringify(value) });

export const receiveConversationResult = (company, id, value) => workspaceFetch(`${conversationsPath(company)}/${encodeURIComponent(id)}/receive-result`, { method: "POST", body: JSON.stringify(value) });
