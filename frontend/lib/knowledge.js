import { workspaceFetch } from "./api.js";

export function getKnowledgeEntries({
  query = "",
  scope = "all",
  projectId = "",
  companyId = "",
  targetType = "",
  targetRef = "",
  sourceType = "",
  lifecycleStatus = "ACTIVE",
  sort = "updated",
  limit = 30,
  offset = 0,
  workRef = "",
} = {}) {
  const params = new URLSearchParams();
  if (query.trim()) params.set("q", query.trim());
  if (scope !== "all") params.set("scope", scope);
  if (projectId) params.set("project_id", projectId);
  if (companyId) params.set("company_id", companyId);
  if (targetType) params.set("target_type", targetType);
  if (targetRef) params.set("target_ref", targetRef);
  if (sourceType) params.set("source_type", sourceType);
  if (lifecycleStatus !== "ACTIVE") params.set("lifecycle_status", lifecycleStatus);
  if (sort !== "updated") params.set("sort", sort);
  params.set("limit", String(limit));
  if (offset) params.set("offset", String(offset));
  if (workRef) params.set("work_ref", workRef);
  const suffix = params.toString();
  return workspaceFetch(`/api/workspace/knowledge/entries${suffix ? `?${suffix}` : ""}`);
}

export const getKnowledgeEntry = (id) =>
  workspaceFetch(`/api/workspace/knowledge/entries/${encodeURIComponent(id)}`);

export const getKnowledgeUsedBy = (id) =>
  workspaceFetch(`/api/workspace/knowledge/entries/${encodeURIComponent(id)}/used-by`);

export const getKnowledgeResults = (id) =>
  workspaceFetch(`/api/workspace/knowledge/entries/${encodeURIComponent(id)}/results`);

export const archiveKnowledgeEntry = (id) =>
  workspaceFetch(`/api/workspace/knowledge/entries/${encodeURIComponent(id)}/archive`, {
    method: "POST",
  });

export const getWorkKnowledgeReferences = (workRef) =>
  workspaceFetch(`/api/workspace/knowledge/works/${encodeURIComponent(workRef)}/references`);

export const addWorkKnowledgeReferences = (workRef, knowledgeIds) =>
  workspaceFetch(`/api/workspace/knowledge/works/${encodeURIComponent(workRef)}/references`, {
    method: "POST",
    body: JSON.stringify({ knowledge_ids: knowledgeIds }),
  });

export const createKnowledgeEntry = (values) =>
  workspaceFetch("/api/workspace/knowledge/entries", {
    method: "POST",
    body: JSON.stringify(values),
  });

export const getLocalKnowledgeRoots = () =>
  workspaceFetch("/api/workspace/knowledge/connectors/local-files");

export const getLocalKnowledgeFiles = (rootId, query = "") => {
  const params = new URLSearchParams({ root_id: rootId });
  if (query.trim()) params.set("q", query.trim());
  return workspaceFetch(
    `/api/workspace/knowledge/connectors/local-files/files?${params}`
  );
};

export const importLocalKnowledgeFile = (values) =>
  workspaceFetch("/api/workspace/knowledge/import", {
    method: "POST",
    body: JSON.stringify(values),
  });
