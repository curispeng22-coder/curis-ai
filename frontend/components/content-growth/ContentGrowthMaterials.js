"use client";
import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { contentGrowthApi as api } from "../../lib/contentGrowthApi.js";
import { contentHref, cgReferenceLabels, cgReferenceTitle, cgScopedRead } from "../../lib/contentGrowthState.mjs";
import { GrowthRecordPanel } from "./ContentGrowthMarket.js";
import styles from "./ContentGrowth.module.css";

const FILTERS = [
  { key: "", label: "全部" },
  { key: "WORK", label: "工作" },
  { key: "DECISION_PACKET", label: "决策包" },
  { key: "CONTENT_ITEM", label: "内容" },
  { key: "CONTENT_VERSION", label: "内容版本" },
];

export default function ContentGrowthMaterials({ company, workspaceId, entry, onInspect }) {
  const [data, setData] = useState(null), [error, setError] = useState(""), [filter, setFilter] = useState("");
  const [selected, setSelected] = useState(new Map());
  const [contents, setContents] = useState([]);
  useEffect(() => {
    let cancelled = false;
    Promise.all([api.materials(company, workspaceId), api.collection(company, workspaceId)])
      .then(([result, coll]) => { cgScopedRead(result, company, workspaceId); cgScopedRead(coll, company, workspaceId); if (!cancelled) { setData(result); setContents(coll.contents || []); } })
      .catch((reason) => { if (!cancelled) setError(reason.message); });
    return () => { cancelled = true; };
  }, [company, workspaceId]);
  const labels = useMemo(() => data ? cgReferenceLabels(data.materials, contents, data.entry.scope) : new Map(), [data, contents]);
  const filtered = useMemo(() => {
    if (!data) return [];
    if (!filter) return data.materials;
    return data.materials.filter((m) => m.kind === filter || (filter === "CONTENT_ITEM" && m.entity_type === "CONTENT_ITEM") || (filter === "CONTENT_VERSION" && m.entity_type === "CONTENT_VERSION"));
  }, [data, filter]);
  const toggle = (material) => {
    setSelected((current) => {
      const next = new Map(current);
      if (next.has(material.reference_id)) next.delete(material.reference_id);
      else if (next.size < 8) next.set(material.reference_id, material);
      return next;
    });
  };
  const referenceArray = Array.from(selected.values()).map((m) => ({ reference_id: m.reference_id, workspace_id: workspaceId, kind: m.kind, title: m.title, version_ref: m.version_ref || "", purpose: m.purpose || "CONTEXT", locator: m.locator || "" }));
  const createHref = referenceArray.length ? contentHref(workspaceId, { view: "", sources: referenceArray.map((r) => r.kind === "CONTENT_ITEM" && r.version_ref ? r.version_ref : r.reference_id) }) : contentHref(workspaceId);
  return <div className={styles.main}>
    <header className={styles.pageHeader}><div><h1>素材与灵感</h1><p className={styles.sub}>核对已有来源与版本，选择少量依据开始新稿。</p></div><Link href={contentHref(workspaceId, { view: "production" })}>← 制作目录</Link></header>
    <GrowthRecordPanel company={company} workspaceId={workspaceId} kinds={["Reference"]} collection={{contents}} selectedRef={entry.object} onInspect={onInspect} />
    {error && <p className={styles.error} role="alert">{error}</p>}
    {!data && !error && <p role="status" className={styles.sub}>正在读取素材…</p>}
    {data && <>
      <div className={styles.row} style={{ gap: "8px", flexWrap: "wrap" }}>
        {FILTERS.map((f) => <button key={f.key} className={filter === f.key ? styles.primary : styles.secondary} onClick={() => setFilter(f.key)}>{f.label}</button>)}
      </div>
      {!filtered.length && <p className={styles.notice}>当前筛选下没有素材。素材来自本工作区已授权的内容、工作与决策记录。</p>}
      <div className={styles.referenceGrid}>{filtered.map((m) => {
        const label = labels.get(m.reference_id) || "来源需核对";
        const title = cgReferenceTitle(m, contents, data.entry.scope);
        const chosen = selected.has(m.reference_id);
        return <div key={m.reference_id} className={styles.materialItem}>
          <label><input type="checkbox" checked={chosen} disabled={!chosen && selected.size >= 8} onChange={() => toggle(m)} />{title}</label>
          <p className={styles.materialMeta}>{FILTERS.find((item) => item.key === m.kind)?.label || "参考"} · {label}</p>
          <button onClick={() => {
            const parent = contents.find((item) => item.content.entity_id === m.reference_id || item.versions.some((version) => version.entity_id === m.reference_id));
            onInspect?.({ id: `source:${m.reference_id}`, title, request: Date.now(), content: <section className={`${styles.main} ${styles.utility}`}><h2>{title}</h2><p>{label}</p><p className={styles.sub}>引用会保留原版本与用途，来源变化时仍须核对。</p>{parent ? <Link href={contentHref(workspaceId, { content: parent.content.entity_id, version: m.kind === "CONTENT_VERSION" ? m.reference_id : m.version_ref })}>回原内容核对 →</Link> : <p>当前可查看来源信息，原文需要在原工作中核对。</p>}<details><summary>查看来源标识</summary><p className={styles.originalBasis}>{m.reference_id}</p></details></section> });
          }}>查看原依据</button>
        </div>;
      })}</div>
      {selected.size > 0 && <div className={styles.actions}>
        <p className={styles.sub}>已选 {selected.size} / 8 项素材</p>
        <Link className={styles.primary} href={createHref}>新建内容并引用已选素材</Link>
      </div>}
    </>}
  </div>;
}
