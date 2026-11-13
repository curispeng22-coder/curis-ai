import { workspaceFetch } from "./api.js";
import { getCanonicalBusinesses, getGeneralWorkspace, getRuntimeCompany, controlGeneralWorkspaceWork, reportGeneralHumanInput, reviewGeneralHumanInput, continueGeneralHumanInput } from "./runtimeApi.js";

const id = (value) => {
  if (typeof value !== "string" || !value.trim()) throw new Error("当前对象缺少合法标识，请返回来源。");
  return encodeURIComponent(value);
};
const companyPath = (company) => `/api/workspace/v1/companies/${id(company)}`;
const post = (request, path, body) => request(path, { method: "POST", ...(body === undefined ? {} : { body: JSON.stringify(body) }) });

export function d1Error(error) {
  if ([401, 403, 404].includes(error?.status)) return "当前身份无法读取这项内容，请返回原公司或工作范围确认权限。";
  if ([409, 422].includes(error?.status)) return "对象或责任状态已变化。输入已保留，请重新读取后核对。";
  return "暂时无法确认操作结果。输入已保留，请重新读取已有记录后重试。";
}

export function createD1Api(request = workspaceFetch) {
  return {
    attention: (company) => request(`${companyPath(company)}/attention`),
    company: (company) => getRuntimeCompany(company, request),
    businesses: (company) => getCanonicalBusinesses(company, request),
    employees: (company) => request(`${companyPath(company)}/conversations/employees`),
    recent: (company) => request(`${companyPath(company)}/conversations`),
    employeeDetail: async (company, employeeRef, workspace) => {
      id(company); id(employeeRef);
      if (!workspace) throw new Error("尚不能确认这位员工的档案身份，请从所在工作打开。");
      const payload = await getGeneralWorkspace(company, workspace, request);
      if (payload.company?.company_id !== company || payload.workspace?.workspace_id !== workspace) throw new Error("员工来源范围不一致。");
      const employee = payload.team?.employees?.find((item) => item.employee_ref === employeeRef);
      if (!employee || employee.identity_status !== "VERIFIED_EXPLICIT_BRIDGE" || employee.identity_bridge?.status !== "VERIFIED" || employee.identity_bridge.companyEmployeeRef !== employee.company_employee_ref || employee.organization_record?.identity_status !== "VERIFIED_EXPLICIT_BRIDGE") throw new Error("尚不能确认这位员工的档案身份，请从所在工作核对。");
      const bindings = await request(`/api/workspace/employees/${id(employee.company_employee_ref)}/capabilities`);
      if (bindings.employee_id !== employee.company_employee_ref) throw new Error("员工档案身份不一致。");
      return { ...employee, companyId: company, workspaceId: workspace, bindings: bindings.bindings || [] };
    },
    conversation: (company, entry) => request(entry.conversationId
      ? `${companyPath(company)}/conversations/${id(entry.conversationId)}`
      : `${companyPath(company)}/employees/${id(entry.employeeRef)}/conversation`),
    createTopic: (company, payload) => post(request, `${companyPath(company)}/conversations`, payload),
    joinTopic: (company, conversation, employee) => post(request, `${companyPath(company)}/conversations/${id(conversation)}/employee`, { employee_ref: employee }),
    send: async (company, entry, payload) => {
      const body = { body: payload.body, assignment_ref: payload.assignment_ref || "", request_id: payload.request_id, references: [], ...(payload.retry_no ? { retry_no: payload.retry_no } : {}) };
      if (entry.conversationId) return post(request, `${companyPath(company)}/conversations/${id(entry.conversationId)}/messages`, body);
      const path = `${companyPath(company)}/employees/${id(entry.employeeRef)}/conversation`;
      await post(request, `${path}/open`);
      return post(request, `${path}/messages`, body);
    },
    work: async (company, workspace, reference) => {
      id(company); id(reference);
      if (!workspace) throw Object.assign(new Error("此范围尚无独立 Work 详情读取接口。请返回其合法来源；不会借用其他工作空间。"), { code: "WORK_READ_SCOPE_GAP" });
      const payload = await getGeneralWorkspace(company, workspace, request);
      if (payload.company?.company_id !== company || payload.workspace?.workspace_id !== workspace) throw new Error("工作来源范围不一致。");
      const work = (payload.current_work || []).find((item) => item.work_ref === reference);
      if (!work) throw Object.assign(new Error("来源未返回这项 Work，请回到原工作空间核对。"), { status: 404 });
      return { ...work, companyId: company, workspaceId: workspace, team: payload.team || [] };
    },
    controlWork: (company, work, action, reason) => {
      if (!work.workspaceId) throw new Error("此范围尚未接入该工作命令。");
      if (!["pause", "resume", "cancel", "archive", "restore"].includes(action)) throw new Error("不支持该操作。");
      return controlGeneralWorkspaceWork(company, work.workspaceId, work.work_ref, action, { reason }, request);
    },
    usage: async (company, work) => {
      if (!work.workspaceId || work.companyId !== company) throw new Error("工作来源范围不一致。");
      const payload = await request(`/api/workspace/runtime/foundation/companies/${id(company)}/workspaces/${id(work.workspaceId)}/shared/general/works/${id(work.work_ref)}/usage`);
      if (payload?.company_id !== company || payload.workspace_id !== work.workspaceId || payload.work_ref !== work.work_ref
        || !Array.isArray(payload.records) || payload.records.some((row) => row.company_id !== company
          || row.workspace_id !== work.workspaceId || row.work_ref !== work.work_ref)) throw new Error("使用记录来源范围不一致。");
      return payload.records;
    },
    reportHumanInput: (company, work, values) => reportGeneralHumanInput(company, work.workspaceId, work.work_ref, work.human_input.requestId, values, request),
    reviewHumanInput: (company, work) => reviewGeneralHumanInput(company, work.workspaceId, work.work_ref, work.human_input.requestId, work.human_input.revision, request),
    continueHumanInput: (work) => continueGeneralHumanInput(work.work_ref, work.human_input.requestId, work.human_input.revision, work.human_input.report?.submissionId, request),
    result: (company, workspace, reference) => {
      id(reference);
      if (!workspace) throw Object.assign(new Error("此范围的结果详情入口尚未接入，请返回原来源。"), { code: "RESULT_READ_SCOPE_GAP" });
      return request(`${companyPath(company)}/result-detail?${new URLSearchParams({ workspace_id: workspace, result_ref: reference })}`);
    },
    viewed: (company, workspace, result) => {
      if (!workspace || !result.result_version || !["RESULT", "OUTCOME"].includes(result.kind)) throw new Error("此来源没有可记录的结果版本与范围。");
      return post(request, `${companyPath(company)}/result-viewed`, { workspace_id: workspace || "", result_ref: result.reference_id, result_version: result.result_version });
    },
    respond: (company, workspace, result, action, reason, requestId) => {
      if (!workspace || !result?.result_version || !result?.source_work_ref) throw new Error("结果来源与版本尚未确认。");
      return post(request, `${companyPath(company)}/result-response`, { workspace_id: workspace,
        result_ref: result.reference_id, result_version: result.result_version,
        source_work_ref: result.source_work_ref, action, reason, request_id: requestId });
    },
  };
}

export const d1Api = createD1Api();
