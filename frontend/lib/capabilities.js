// Workspace Capability Registry。
// 统一经 workspaceFetch（自动注入 X-Tenant-Id / X-Ceo-Id），不使用 Platform Admin。

import {
  workspaceFetch,
  getEmployeeCapabilities,
  setEmployeeCapabilities,
  getCompanies,
  getEmployees,
} from "./api.js";

export const getAgentAllowanceCompanies = getCompanies;
export const getLocalAgentEmployees = getEmployees;
export const addEmployeeAgentBinding = (employeeId, companyId, capabilityId) => workspaceFetch(
  `/api/workspace/employees/${encodeURIComponent(employeeId)}/agent-bindings`,
  { method: "POST", body: JSON.stringify({ company_id: companyId, capability_id: capabilityId }) });
export const discoverLocalAgents = (installationPath = "") => workspaceFetch(`/api/workspace/ai-capabilities/local?metadata_only=true${installationPath ? `&installation_path=${encodeURIComponent(installationPath)}` : ""}`);
export const createAgentAuthorization = (company, payload) => workspaceFetch(
  "/api/workspace/v1/companies/" + encodeURIComponent(company) + "/agent-authorizations",
  { method: "POST", body: JSON.stringify(payload) });
export const getAgentAllowance = (company) => workspaceFetch(`/api/workspace/v1/companies/${encodeURIComponent(company)}/agent-allowance`);
export const saveAgentAllowance = (company, payload) => workspaceFetch(`/api/workspace/v1/companies/${encodeURIComponent(company)}/agent-allowance`, { method: "PUT", body: JSON.stringify(payload) });
export const revokeAgentAllowance = (company, payload) => workspaceFetch(`/api/workspace/v1/companies/${encodeURIComponent(company)}/agent-allowance/revoke`, { method: "POST", body: JSON.stringify(payload) });

/**
 * 只读能力目录（selector）：GET /api/workspace/capabilities/selector
 * 用于能力中心与「绑定」picker。返回结构按后端实际响应动态渲染，不虚构类别。
 * @returns {Promise<any>}
 */
export function getCapabilitySelector() {
  return workspaceFetch("/api/workspace/capabilities/selector");
}

export function getCapabilities({ type = "", includeInactive = true } = {}) {
  const query = new URLSearchParams();
  if (type) query.set("type", type);
  query.set("include_inactive", String(includeInactive));
  return workspaceFetch(`/api/workspace/capabilities/registry?${query}`);
}

export function getCapability(key) {
  return workspaceFetch(`/api/workspace/capabilities/registry/${encodeURIComponent(key)}`);
}

export function createCapability(values) {
  return workspaceFetch("/api/workspace/capabilities/registry", {
    method: "POST",
    body: JSON.stringify(values),
  });
}

export function updateCapabilityStatus(key, action) {
  return workspaceFetch(`/api/workspace/capabilities/registry/${encodeURIComponent(key)}`, {
    method: "PUT",
    body: JSON.stringify({ action }),
  });
}

export function migrateHistoricalSkills() {
  return workspaceFetch("/api/workspace/capabilities/registry/migrate-skills", {
    method: "POST",
  });
}

export function getModelGatewaySummary() {
  return workspaceFetch("/api/workspace/model-gateway");
}

/**
 * 连接器运行模式（mock / real）。
 * 读：GET /api/connectors/mode → { mode, source, persisted, env }
 * 写：PUT /api/connectors/mode，mode 传空字符串表示清除设置、回落环境变量。
 */
export function getConnectorMode() {
  return workspaceFetch("/api/connectors/mode");
}

export function setConnectorMode(mode) {
  return workspaceFetch("/api/connectors/mode", {
    method: "PUT",
    body: JSON.stringify({ mode }),
  });
}

// ── 用户自定义（租户私有）模型 / 能力接入 ──
// 走 workspaceFetch（自动注入 X-Tenant-Id / X-Ceo-Id），与平台 Admin 端点隔离。
// 第一版桌面应用是单人自用（无 user/admin 拆分），未来商业化时同一套接口即供终端
// 用户自助接入自己的模型 / Agent，不依赖平台管理员令牌。

export function getPrivateModels() {
  return workspaceFetch("/api/workspace/private-models");
}

export function createPrivateModel(values) {
  return workspaceFetch("/api/workspace/private-models", {
    method: "POST",
    body: JSON.stringify(values),
  });
}

export function getPrivateCapabilities(type) {
  const query = type ? `?capability_type=${encodeURIComponent(type)}` : "";
  return workspaceFetch(`/api/workspace/capabilities/private${query}`);
}

export function createPrivateCapability(values) {
  return workspaceFetch("/api/workspace/capabilities/private", {
    method: "POST",
    body: JSON.stringify(values),
  });
}

export function updateDshAgentAccount(capabilityId, values) {
  return workspaceFetch(`/api/workspace/capabilities/private/agent/${encodeURIComponent(capabilityId)}/dsh-account`, {
    method: "PATCH", body: JSON.stringify(values),
  });
}

// 员工能力绑定：复用 lib/api.js 既有封装（GET / PUT /api/workspace/employees/:id/capabilities）。
export { getEmployeeCapabilities, setEmployeeCapabilities };

export function controlAgentBrowser(companyId, bindingRef, action = "") {
  const url = "/api/workspace/v1/companies/" + encodeURIComponent(companyId) + "/agent-browser/" + encodeURIComponent(bindingRef);
  return workspaceFetch(url + (action ? "/" + action : ""), action ? { method: "POST" } : undefined);
}

export function codexConnectionState(value, companyId, bindingRef) {
  const states = ["DISCONNECTED", "CONNECTED", "STARTING", "WAITING_FOR_LOGIN", "DISCONNECTING", "IN_USE", "HELD", "UNAVAILABLE"];
  const fields = ["company_id", "binding_ref", "capability_id", "state", "generation", "verification_url", "user_code"];
  if (!value || typeof value !== "object" || Array.isArray(value) || value.company_id !== companyId || value.binding_ref !== bindingRef || !states.includes(value.state)
      || Object.keys(value).some((key) => !fields.includes(key))
      || (value.generation != null && (typeof value.generation !== "string" || !/^[a-f0-9]{48}$/.test(value.generation)))
      || (["CONNECTED", "WAITING_FOR_LOGIN"].includes(value.state) && value.generation == null)) throw new Error("Codex 连接回执不属于当前公司或尚未核验。");
  const safe = { company_id: companyId, binding_ref: bindingRef, state: value.state, generation: value.generation ?? null };
  if (value.state === "WAITING_FOR_LOGIN") {
    if (value.verification_url !== "https://auth.openai.com/codex/device" || typeof value.user_code !== "string" || !/^[A-Z0-9]{4}-[A-Z0-9]{4}$/.test(value.user_code)) throw new Error("官方登录地址或临时代码无法核验。");
    safe.verification_url = value.verification_url;
    safe.user_code = value.user_code;
  }
  return safe;
}

export async function getAgentCodexAuth(companyId, bindingRef) {
  const value = await workspaceFetch("/api/workspace/v1/companies/" + encodeURIComponent(companyId) + "/agent-auth/" + encodeURIComponent(bindingRef));
  return codexConnectionState(value, companyId, bindingRef);
}

export async function controlAgentCodexAuth(companyId, bindingRef, action, payload) {
  if (!["connect", "disconnect"].includes(action) || !payload || Array.isArray(payload) || typeof payload.request_id !== "string" || !/^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/.test(payload.request_id)
      || Object.keys(payload).some((key) => !["request_id", "expected_generation"].includes(key))
      || (payload.expected_generation != null && (typeof payload.expected_generation !== "string" || !/^[a-f0-9]{48}$/.test(payload.expected_generation)))) throw new Error("Codex 连接请求无法核验。");
  const value = await workspaceFetch("/api/workspace/v1/companies/" + encodeURIComponent(companyId) + "/agent-auth/" + encodeURIComponent(bindingRef) + "/" + action,
    { method: "POST", body: JSON.stringify({ request_id: payload.request_id, expected_generation: payload.expected_generation ?? null }) });
  return codexConnectionState(value, companyId, bindingRef);
}
