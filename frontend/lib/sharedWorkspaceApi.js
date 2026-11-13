import { workspaceFetch } from "./api.js";

const PREFIX = "/api/workspace/runtime/foundation/companies";
const scope = (companyId, workspaceId) =>
  `${PREFIX}/${encodeURIComponent(companyId)}/workspaces/${encodeURIComponent(workspaceId)}/shared`;

export const getSharedWorkspace = (companyId, workspaceId, request = workspaceFetch) =>
  request(scope(companyId, workspaceId));

export const getSharedEmployee = (companyId, workspaceId, employeeId, request = workspaceFetch) =>
  request(`${scope(companyId, workspaceId)}/employees/${encodeURIComponent(employeeId)}`);

export const getSharedResult = (companyId, workspaceId, referenceId, request = workspaceFetch) =>
  request(`${scope(companyId, workspaceId)}/results/${encodeURIComponent(referenceId)}`);
