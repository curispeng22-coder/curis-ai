import {
  getCompanies,
  getDepartments,
  getEmployeeCapabilities,
  getEmployeeSkills,
  getEmployees,
  getEmployeeTemplates,
  workspaceFetch,
} from "./api.js";
import { safeReturnPath } from "./auth.mjs";

const CURIS_FIRST_BATCH = new Set([
  "et_product_manager",
  "et_architect",
  "et_frontend_engineer",
  "et_backend_engineer",
  "et_qa_engineer",
]);

const INSTALLABLE_SKILL_TYPES = new Set([
  "planning",
  "analysis",
  "architecture",
  "frontend",
  "backend",
  "qa",
  "tool_operation",
]);

export async function getTalentMarketData() {
  const [templates, productionLine, skills, connectors, companies, departments, employees] = await Promise.all([
    getEmployeeTemplates(),
    workspaceFetch("/api/workspace/talent-market/production-line"),
    workspaceFetch("/api/workspace/skills/templates"),
    workspaceFetch("/api/connectors"),
    getCompanies(),
    getDepartments(),
    getEmployees(),
  ]);
  const curisExperts = (templates?.employee_templates || []).filter((item) => CURIS_FIRST_BATCH.has(item.id)).map((item) => ({
    ...item,
    market_kind: "curis_ready",
    maturity: "CURIS_READY",
    source: item.source || "curis",
    source_label: "Curis-ready",
    recruitable: true,
    category: item.department_type === "software_rnd" ? "研发" : "其他",
    composition: {
      status: "validated",
      skills: item.default_skill ? [item.default_skill] : [],
      tools: item.default_tool ? [item.default_tool] : [],
      mcp: [],
      knowledge_requirements: [],
      connector_requirements: [],
      model_requirements: item.default_capability_types || [],
    },
  }));
  const externalCandidates = (productionLine?.resources || []).filter((item) => item.resource_type === "agent");
  const companyById = new Map((companies?.companies || []).map((item) => [item.company_id, item]));
  const departmentById = new Map((departments?.departments || []).map((item) => [item.id, item]));
  const companyEmployees = (employees?.employees || []).map((item) => ({
    ...item,
    market_kind: "company_employee",
    company_name: companyById.get(item.company_id)?.name || "公司未记录",
    department_name: item.department_id
      ? departmentById.get(item.department_id)?.name || "部门未记录"
      : "暂未归属部门",
    category: item.role || "其他",
  }));
  return {
    experts: [...curisExperts, ...externalCandidates],
    companyEmployees,
    skills: skills?.skills || [],
    connectors: connectors?.connectors || [],
    connectorMode: connectors?.mode || "mock",
    companies: companies?.companies || [],
    departments: departments?.departments || [],
    employees: employees?.employees || [],
    productionLine,
    expertCategories: [...new Set([...curisExperts, ...externalCandidates].map((item) => item.category).filter(Boolean))].sort(),
  };
}

export function productStateFor(item, kind) {
  if (kind === "experts") {
    if (item.market_kind === "company_employee") return "已加入公司";
    if (item.recruitable) return "可招聘";
    return "正在准备";
  }
  if (kind === "skills") {
    if (item.source === "tenant_private") return item.dependency_status?.ready === false ? "已安装·待准备" : "已安装";
    return item.status === "active" && INSTALLABLE_SKILL_TYPES.has(item.skill_type)
      ? "可安装"
      : "暂不可用";
  }
  if (item.authorization_status !== "authorized") return "未连接";
  if (item.health_status === "healthy") return "已连接";
  if (item.health_status === "unhealthy") return "连接异常";
  return "待验证";
}

export async function getEmployeeAbilitySummary(employeeId) {
  const [skills, capabilities] = await Promise.allSettled([
    getEmployeeSkills(employeeId),
    getEmployeeCapabilities(employeeId),
  ]);
  return {
    skills: skills.status === "fulfilled" ? skills.value?.bindings || [] : [],
    capabilities: capabilities.status === "fulfilled" ? capabilities.value?.bindings || [] : [],
    complete: skills.status === "fulfilled" && capabilities.status === "fulfilled",
  };
}

export function resolveTalentReturnPath({ returnTo = "", source = "", origin = "http://localhost" } = {}) {
  if (!returnTo) return source === "organization" ? "/ceo-office/organization" : "";
  const candidate = String(returnTo).trim();
  if (!candidate.startsWith("/") || candidate.startsWith("//")) return "";
  const resolved = safeReturnPath(candidate, origin);
  return resolved === "/ceo-office" || resolved.startsWith("/ceo-office/") ? resolved : "";
}

export function recruitExpert(payload) {
  return workspaceFetch("/api/workspace/talent-market/recruit", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function uploadEmployeeAvatar(employeeId, file) {
  return workspaceFetch(`/api/workspace/employees/${encodeURIComponent(employeeId)}/avatar`, {
    method: "PUT",
    headers: { "Content-Type": file.type },
    body: file,
  });
}

export function installSkill(skillId) {
  return workspaceFetch(`/api/workspace/skills/templates/${encodeURIComponent(skillId)}/install`, {
    method: "POST",
  });
}

export function previewSkillPackage(source) {
  return workspaceFetch("/api/workspace/skills/packages/preview", { method: "POST", body: JSON.stringify(source) });
}

export function installSkillPackage(source) {
  return workspaceFetch("/api/workspace/skills/packages/install", { method: "POST", body: JSON.stringify(source) });
}

export function assignSkill(employeeId, skillTemplateId) {
  return workspaceFetch(`/api/workspace/employees/${encodeURIComponent(employeeId)}/skills/${encodeURIComponent(skillTemplateId)}`, { method: "POST" });
}

export async function getSkillAssignments(employees, skillTemplateId) {
  const rows = await Promise.all(employees.map(async employee => {
    const result = await getEmployeeSkills(employee.id);
    return (result?.bindings || []).some(item => item.skill_template_id === skillTemplateId) ? employee : null;
  }));
  return rows.filter(Boolean);
}

export function unassignSkill(employeeId, skillTemplateId) {
  return workspaceFetch(`/api/workspace/employees/${encodeURIComponent(employeeId)}/skills/${encodeURIComponent(skillTemplateId)}`, { method: "DELETE" });
}

export function removeSkill(skillTemplateId, companyId = "") {
  const scope = companyId ? `?company_id=${encodeURIComponent(companyId)}` : "";
  return workspaceFetch(`/api/workspace/skills/templates/${encodeURIComponent(skillTemplateId)}${scope}`, { method: "DELETE" });
}
