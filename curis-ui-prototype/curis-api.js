/*
 * Curis —— 前端接入真实后端的 API 客户端（第 3 步）。
 *
 * 对应后端 A5 统一响应契约：所有 /api/ceo-day/* 返回
 *   { code, message, data, trace_id, timestamp }
 * code === 0 为成功；非 0 抛错（message 可读）。
 *
 * 用法（无需打包，原生 <script> 即可）：
 *   <script src="curis-api.js"></script>
 *   const api = new CurisAPI("http://localhost:8000");
 *   const dir = await api.createDirection({ name, template_type, ... });
 *
 * 注意：本客户端只调用真实接口，不做静默 mock —— 接不上后端会明确报错，
 * 避免"假装有能力"。原型里原有的硬编码数据请逐步替换为真实调用。
 */
(function (global) {
  "use strict";

  class CurisAPI {
    constructor(baseUrl) {
      this.base = (baseUrl || "http://localhost:8000").replace(/\/+$/, "");
    }

    async _call(path, method, body) {
      const opts = { method: method, headers: {} };
      if (body !== undefined) {
        opts.headers["Content-Type"] = "application/json";
        opts.body = JSON.stringify(body);
      }
      const resp = await fetch(this.base + path, opts);
      const json = await resp.json().catch(() => ({}));
      if (json && typeof json.code === "number" && json.code !== 0) {
        throw new Error(json.message || ("请求失败 " + resp.status));
      }
      return json && json.data !== undefined ? json.data : json;
    }

    get(path) { return this._call(path, "GET"); }
    post(path, body) { return this._call(path, "POST", body || {}); }

    // ---- BusinessDirection ----
    createDirection(p) { return this.post("/api/ceo-day/business-directions", p); }
    submitBrief(did) { return this.post(`/api/ceo-day/business-directions/${did}/submit-brief`); }
    approveDirection(did, authorized) {
      return this.post(`/api/ceo-day/business-directions/${did}/approve`, { authorized: !!authorized });
    }
    scaleDirection(did) { return this.post(`/api/ceo-day/business-directions/${did}/scale`); }
    setVerification(did, grade) {
      return this.post(`/api/ceo-day/business-directions/${did}/verification`, { grade });
    }

    // ---- Commitment ----
    createCommitment(p) { return this.post("/api/ceo-day/commitments", p); }
    firstResult(cid) { return this.post(`/api/ceo-day/commitments/${cid}/first-result`); }
    fulfillCommitment(cid, verificationStatus) {
      return this.post(`/api/ceo-day/commitments/${cid}/fulfill`, { verification_status: verificationStatus });
    }

    // ---- Workspace ----
    createWorkspace(p) { return this.post("/api/ceo-day/workspaces", p); }
    startBlueprint(wid) { return this.post(`/api/ceo-day/workspaces/${wid}/start-blueprint`); }
    passSimulation(wid) { return this.post(`/api/ceo-day/workspaces/${wid}/pass-simulation`); }
    submitWorkspaceApproval(wid, issuesResolved, externalAgentReviewed) {
      return this.post(`/api/ceo-day/workspaces/${wid}/submit-approval`, {
        issues_resolved: !!issuesResolved, external_agent_reviewed: !!externalAgentReviewed,
      });
    }
    approveLaunch(wid) { return this.post(`/api/ceo-day/workspaces/${wid}/approve-launch`); }

    // ---- Cadence / Run ----
    createCadence(p) { return this.post("/api/ceo-day/cadences", p); }
    enableCadence(cid, nextFireAt) {
      return this.post(`/api/ceo-day/cadences/${cid}/enable`, { next_fire_at: nextFireAt || null });
    }
    fire() { return this.post("/api/ceo-day/fire"); }
    openRun(runId) { return this.post(`/api/ceo-day/runs/${runId}/open`); }
    resolveRun(runId, reason) {
      return this.post(`/api/ceo-day/runs/${runId}/resolve`, { reason: reason || "" });
    }

    // ---- Outcome ----
    createOutcome(p) { return this.post("/api/ceo-day/outcomes", p); }
    confirmAttribution(oid) { return this.post(`/api/ceo-day/outcomes/${oid}/confirm-attribution`); }
  }

  global.CurisAPI = CurisAPI;
})(window);
