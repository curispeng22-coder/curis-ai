"use client";

// 成果展示中心（Self-use v1 · Wave 2 F2）
// 统一查看：内容发布包 / 代码（研发工作流）/ 视频与数据报告（内容工作流运行）。
// 复用 /api/results/* 与 /api/content-workflow/run（W1 闭环）。

import { useCallback, useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";
const TENANT_ID = process.env.NEXT_PUBLIC_CURIS_TENANT_ID || "selfuse";

export default function ResultsCenterPage() {
  const [summary, setSummary] = useState(null);
  const [packages, setPackages] = useState([]);
  const [runs, setRuns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [trigger, setTrigger] = useState({ prompt: "春季护肤：3 个被忽略的误区", platforms: "xhs,douyin" });
  const [busy, setBusy] = useState(false);
  const [toast, setToast] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const [s, p, r] = await Promise.all([
        fetch(`${API_BASE}/api/results/summary`, { headers: { "X-Tenant-Id": TENANT_ID }, cache: "no-store" }).then((x) => x.json()),
        fetch(`${API_BASE}/api/results/publish-packages?limit=50`, { headers: { "X-Tenant-Id": TENANT_ID }, cache: "no-store" }).then((x) => x.json()),
        fetch(`${API_BASE}/api/results/content-workflow-runs?limit=50`, { headers: { "X-Tenant-Id": TENANT_ID }, cache: "no-store" }).then((x) => x.json()),
      ]);
      setSummary(s);
      setPackages(p.publish_packages || []);
      setRuns(r.runs || []);
    } catch (err) {
      setError(err.message || "读取失败");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const onRun = async (e) => {
    e.preventDefault();
    setBusy(true);
    setError("");
    setToast("");
    try {
      const res = await fetch(`${API_BASE}/api/content-workflow/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-Tenant-Id": TENANT_ID },
        body: JSON.stringify({
          prompt: trigger.prompt,
          platforms: trigger.platforms.split(",").map((s) => s.trim()).filter(Boolean),
        }),
      });
      const payload = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(payload.detail || "运行失败");
      const published = (payload.published_platforms || []).join(", ") || "无";
      setToast(`闭环完成：${payload.status} · 发布包 ${payload.package?.package_id} · 已发布 ${published}`);
      await load();
    } catch (err) {
      setError(err.message || "运行失败");
    } finally {
      setBusy(false);
    }
  };

  return (
    <main style={{ maxWidth: 1080, margin: "0 auto", padding: "48px 24px", color: "#0f172a" }}>
      <h1 style={{ fontSize: 28, marginBottom: 4 }}>成果展示中心</h1>
      <p style={{ color: "#64748b", marginBottom: 24 }}>
        内容发布包 / 代码 / 视频 / 数据报告统一查看。研发工作流跑通内容由「研发部真实引擎」产生，
        内容闭环由 W1 生成→发布包→发布链路产出。
      </p>

      {toast ? (
        <div style={{ background: "#ecfdf5", color: "#065f46", padding: "10px 14px", borderRadius: 8, marginBottom: 16 }}>{toast}</div>
      ) : null}
      {error ? (
        <div style={{ background: "#fef2f2", color: "#991b1b", padding: "10px 14px", borderRadius: 8, marginBottom: 16 }}>{error}</div>
      ) : null}

      <section style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))", gap: 16, marginBottom: 32 }}>
        <Card label="内容发布包" value={summary?.publish_packages?.total ?? "—"} sub={`已发布 ${summary?.publish_packages?.published ?? 0}`} />
        <Card label="内容闭环运行" value={summary?.content_workflow_runs?.total ?? "—"} sub={`完成 ${summary?.content_workflow_runs?.completed ?? 0}`} />
        <Card label="研发工作流" value={summary?.rd_workflow_runs ?? "—"} sub="wl_ai_rd_*" />
        <Card label="代码产物" value={summary?.code_artifacts ?? "—"} sub="step_results" />
      </section>

      <section style={{ border: "1px solid #e2e8f0", borderRadius: 12, padding: 20, marginBottom: 32, background: "#fff" }}>
        <h2 style={{ fontSize: 18, marginBottom: 14 }}>触发内容闭环（mock 无需 docker）</h2>
        <form onSubmit={onRun} style={{ display: "grid", gap: 12 }}>
          <input
            value={trigger.prompt}
            onChange={(e) => setTrigger((t) => ({ ...t, prompt: e.target.value }))}
            placeholder="选题 / 提示"
            style={{ padding: 10, borderRadius: 8, border: "1px solid #cbd5e1" }}
          />
          <input
            value={trigger.platforms}
            onChange={(e) => setTrigger((t) => ({ ...t, platforms: e.target.value }))}
            placeholder="平台，逗号分隔：xhs,douyin"
            style={{ padding: 10, borderRadius: 8, border: "1px solid #cbd5e1" }}
          />
          <button type="submit" disabled={busy} style={{ justifySelf: "start", padding: "10px 20px", borderRadius: 8, border: "none", background: "#0f172a", color: "#fff", cursor: "pointer" }}>
            {busy ? "运行中…" : "运行生成→发布"}
          </button>
        </form>
      </section>

      <section style={{ marginBottom: 32 }}>
        <h2 style={{ fontSize: 18, marginBottom: 12 }}>内容发布包</h2>
        {loading ? <p style={{ color: "#64748b" }}>读取中…</p> : packages.length === 0 ? (
          <p style={{ color: "#64748b" }}>暂无发布包。运行上方闭环即可生成。</p>
        ) : (
          <Table
            headers={["发布包", "来源工作流", "平台", "状态", "时间"]}
            rows={packages.map((p) => [
              p.package_id,
              p.source_workflow,
              (p.platforms_targeted || []).join(", "),
              p.status,
              (p.created_at || "").slice(0, 19).replace("T", " "),
            ])}
          />
        )}
      </section>

      <section>
        <h2 style={{ fontSize: 18, marginBottom: 12 }}>内容工作流运行</h2>
        {loading ? <p style={{ color: "#64748b" }}>读取中…</p> : runs.length === 0 ? (
          <p style={{ color: "#64748b" }}>暂无运行记录。</p>
        ) : (
          <Table
            headers={["运行 ID", "来源工作流", "状态", "步骤", "时间"]}
            rows={runs.map((r) => [
              r.run_id,
              r.workflow_content_id,
              r.status,
              `${r.steps_done}/${r.steps_total}`,
              (r.created_at || "").slice(0, 19).replace("T", " "),
            ])}
          />
        )}
      </section>
    </main>
  );
}

function Card({ label, value, sub }) {
  return (
    <div style={{ border: "1px solid #e2e8f0", borderRadius: 12, padding: 18, background: "#fff" }}>
      <div style={{ fontSize: 12, color: "#64748b" }}>{label}</div>
      <div style={{ fontSize: 28, fontWeight: 600, margin: "6px 0" }}>{value}</div>
      <div style={{ fontSize: 12, color: "#94a3b8" }}>{sub}</div>
    </div>
  );
}

function Table({ headers, rows }) {
  return (
    <table style={{ width: "100%", borderCollapse: "collapse", background: "#fff", borderRadius: 12, overflow: "hidden" }}>
      <thead>
        <tr style={{ background: "#f8fafc", textAlign: "left" }}>
          {headers.map((h) => (
            <th key={h} style={{ padding: "10px 12px", fontSize: 13, color: "#475569" }}>{h}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((row, i) => (
          <tr key={i} style={{ borderTop: "1px solid #f1f5f9" }}>
            {row.map((cell, j) => (
              <td key={j} style={{ padding: "10px 12px", fontSize: 13 }}>{cell}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
