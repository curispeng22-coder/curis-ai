import { workspaceFetch } from "./api.js";

const PREFIX = "/api/workspace/packages";

export const getInstalledWorkspaceNavigation = (companyId = "", request = workspaceFetch) =>
  request(`${PREFIX}/navigation${companyId ? `?company_id=${encodeURIComponent(companyId)}` : ""}`);

export const getInstalledWorkspace = (workspaceId, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}`);

export const createInstalledWorkspaceObject = (workspaceId, actionId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/actions/${encodeURIComponent(actionId)}`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const operateInstalledWorkspaceObject = (workspaceId, objectId, values, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/objects/${encodeURIComponent(objectId)}/company-operate`, {
    method: "POST",
    body: JSON.stringify(values),
  });

export const resolveInstalledWorkspaceCompanyIntegration = (workspaceId, objectId, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/objects/${encodeURIComponent(objectId)}/company-integration`);

export const completeInstalledWorkspaceInitialTeam = (workspaceId, payload, request = workspaceFetch) =>
  request(`${PREFIX}/workspaces/${encodeURIComponent(workspaceId)}/initial-team`, {method:"POST", body:JSON.stringify(payload)});
