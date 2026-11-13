import { workspaceFetch } from "./api.js";

export function getMemoryEntries({ query = "", scope = "all", projectId = "", employeeId = "" } = {}) {
  const params = new URLSearchParams();
  if (query.trim()) params.set("q", query.trim());
  if (scope && scope !== "all") params.set("scope", scope);
  if (projectId) params.set("project_id", projectId);
  if (employeeId) params.set("employee_id", employeeId);
  const suffix = params.toString();
  return workspaceFetch(`/api/workspace/memory${suffix ? `?${suffix}` : ""}`);
}

export const createMemoryEntry = (values) =>
  workspaceFetch("/api/workspace/memory", {
    method: "POST",
    body: JSON.stringify(values),
  });

export const updateMemoryEntry = (id, values) =>
  workspaceFetch(`/api/workspace/memory/${encodeURIComponent(id)}`, {
    method: "PATCH",
    body: JSON.stringify(values),
  });

export const getContextPackage = (id) =>
  workspaceFetch(`/api/workspace/context/${encodeURIComponent(id)}`);

export const getTaskContextPackage = (taskId) =>
  workspaceFetch(`/api/workspace/context/task/${encodeURIComponent(taskId)}`);
