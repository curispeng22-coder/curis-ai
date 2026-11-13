import { workspaceFetch } from "./api.js";

export const runContentWorkflow = (values) =>
  workspaceFetch("/api/workspace/content-workflow/run", {
    method: "POST",
    body: JSON.stringify(values),
  });
