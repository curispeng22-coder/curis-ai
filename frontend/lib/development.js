import { workspaceFetch } from "./api.js";

export const runDevelopmentWorkflow = (values) =>
  workspaceFetch("/api/workspace/rd-workflow/run", {
    method: "POST",
    body: JSON.stringify(values),
  });

export const getWorkflowRun = (id) =>
  workspaceFetch(`/api/workspace/workflows/${id}`);
