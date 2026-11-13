import { useCallback, useEffect, useState } from "react";

const MATURITY_LABEL = {
  DISCOVERED: "已发现",
  CANDIDATE: "候选",
  COMPOSED: "已组合",
  VALIDATED: "已验证",
  CURIS_READY: "Curis-ready",
  BLOCKED: "已阻塞",
};

export default function TalentProductionPanel({ apiFetch, onMessage }) {
  const [payload, setPayload] = useState(null);
  const [loading, setLoading] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      setPayload(await apiFetch("/api/platform/talent-market/production-line"));
    } catch (error) {
      onMessage(error.message);
    } finally {
      setLoading(false);
    }
  }, [apiFetch, onMessage]);

  useEffect(() => { load().catch(() => null); }, [load]);

  if (!payload) return <p className="admin-meta">{loading ? "正在扫描公开快照…" : "暂无扫描结果"}</p>;
  const counts = payload.counts || {};
  const agents = (payload.resources || []).filter((item) => item.resource_type === "agent");
  return (
    <section>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-xl font-bold">人才生产线</h2>
          <p className="admin-meta mt-1">只读 Candidate Queue；扫描不会直接创建员工或安装资源。</p>
        </div>
        <button type="button" className="admin-button" onClick={() => load()} disabled={loading}>{loading ? "扫描中…" : "重新扫描"}</button>
      </div>
      <div className="mt-4 grid gap-2 sm:grid-cols-4">
        {["discovered", "deduped", "candidate", "blocked"].map((key) => <div key={key} className="admin-card"><div className="admin-meta">{key}</div><div className="mt-1 text-2xl font-bold">{counts[key] || 0}</div></div>)}
      </div>
      <div className="mt-5 overflow-x-auto">
        <table className="admin-table w-full">
          <thead><tr><th>资源</th><th>分类</th><th>成熟度</th><th>来源 / 许可证</th><th>安全</th></tr></thead>
          <tbody>{agents.map((item) => <tr key={item.id}><td><div className="font-semibold">{item.name}</div><div className="admin-meta">{item.source_path}</div></td><td>{item.category}</td><td>{MATURITY_LABEL[item.maturity] || item.maturity}</td><td><div>{item.source_label}</div><div className="admin-meta">{item.license}</div></td><td>{item.security_status === "pass" ? "通过" : "阻塞"}</td></tr>)}</tbody>
        </table>
      </div>
    </section>
  );
}
