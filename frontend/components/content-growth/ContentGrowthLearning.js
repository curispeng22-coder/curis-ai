"use client";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { contentGrowthApi as api } from "../../lib/contentGrowthApi.js";
import { contentHref, cgScopedRead, stableRequest, cgReferenceLabels, cgManualLearningSources } from "../../lib/contentGrowthState.mjs";
import styles from "./ContentGrowth.module.css";

const EMPTY_FORM = { title: "", body: "", applicability: "", counterexample: "", accepted: false };

export default function ContentGrowthLearning({ company, workspaceId, entry, onInspect }) {
  const [readingScope, setReadingScope] = useState(null);
  const [records, setRecords] = useState([]), [materials, setMaterials] = useState([]), [contents, setContents] = useState([]);
  const [panelRequest, setPanelRequest] = useState(0);
  const alive = useRef(true), readSequence = useRef(0), mutation = useRef(false), readInfo = useRef(null), commandIdentity = useRef({});
  const [loaded, setLoaded] = useState(false);
  const requestId = (action, base, data) => { const next = stableRequest(commandIdentity.current[action], action, base, data, () => crypto.randomUUID()); commandIdentity.current[action] = next; return next.request_id; };
  useEffect(() => { alive.current = true; return () => { alive.current = false; readSequence.current += 1; }; }, []);
  const [error, setError] = useState(""), [busy, setBusy] = useState(false);
  const [mode, setMode] = useState("list"); // list | create | detail | apply
  const [selected, setSelected] = useState(null);
  const [form, setForm] = useState({ ...EMPTY_FORM });
  const [basisMap, setBasisMap] = useState(new Map());

  const load = useCallback(async () => {
    const ticket = ++readSequence.current;
    setError("");
    try {
      const [learnings, mats, coll, manual] = await Promise.all([
        api.learnings(company, workspaceId),
        api.materials(company, workspaceId),
        api.collection(company, workspaceId),
        api.operatingContext(company, workspaceId),
      ]);
      [learnings, mats, coll, manual].forEach((value) => cgScopedRead(value, company, workspaceId));
      const manualMaterials = cgManualLearningSources(manual, learnings.entry.scope);
      if (!alive.current || ticket !== readSequence.current) return;
      readInfo.current = learnings.entry; setReadingScope(learnings.entry.scope); setLoaded(true);
      setRecords(learnings.records || []);
      setMaterials([...(mats.materials || []), ...manualMaterials]);
      setContents(coll.contents || []);
    } catch (reason) {
      if (!alive.current || ticket !== readSequence.current) return;
      setError(reason.message);
    }
  }, [company, workspaceId]);

  useEffect(() => { load(); }, [load]);

  const labels = useMemo(() => cgReferenceLabels(materials, contents, readingScope), [materials, contents, readingScope]);
  const basisList = useMemo(() => Array.from(basisMap.values()), [basisMap]);

  const toggleBasis = (m) => {
    setBasisMap((prev) => {
      const next = new Map(prev);
      if (next.has(m.reference_id)) next.delete(m.reference_id);
      else if (next.size < 8) next.set(m.reference_id, m);
      return next;
    });
  };

  const save = async () => {
    if (mutation.current || !alive.current || !loaded) return;
    if (!form.title.trim() || !form.body.trim()) { setError("标题与正文不能为空。"); return; }
    mutation.current = true; setBusy(true); setError("");
    try {
      const payload = {
        request_id: "",
        expected_ref: "",
        data: {
          title: form.title.trim(),
          body: form.body.trim(),
          basis_refs: basisList.map((m) => m.reference_id),
          applicability: form.applicability.trim(),
          counterexample: form.counterexample.trim(),
          accepted: Boolean(form.accepted),
        },
      };
      payload.request_id = requestId("save-learning", "", payload.data);
      await api.learningCommand(company, workspaceId, "save-learning", payload);
      if (!alive.current) return;
      commandIdentity.current["save-learning"] = null;
      setForm({ ...EMPTY_FORM });
      setBasisMap(new Map());
      if (!alive.current) return;
      setMode("list");
      await load();
    } catch (reason) {
      if (alive.current) setError(reason.message);
    } finally {
      mutation.current = false; if (alive.current) setBusy(false);
    }
  };

  const apply = async (learningRef, contentRef, historical) => {
    if (mutation.current || !alive.current || !loaded) return;
    mutation.current = true; setBusy(true); setError("");
    try {
      await api.learningCommand(company, workspaceId, "use-learning", {
        request_id: requestId("use-learning", learningRef, { learningRef, contentRef, historical: Boolean(historical) }),
        data: { learning_ref: learningRef, content_ref: contentRef, confirmed: true, historical: Boolean(historical) },
      });
      if (!alive.current) return;
      commandIdentity.current["use-learning"] = null;
      setMode("list");
      await load();
    } catch (reason) {
      if (alive.current) setError(reason.message);
    } finally {
      mutation.current = false; if (alive.current) setBusy(false);
    }
  };

  const recordLabel = (rec) => rec.data.title || "未命名经验";
  const recordMeta = (rec) => `${rec.data.accepted_by ? "已接受" : "待接受"} · 适用：${rec.data.applicability || "未指定"}`;

  const panel = useMemo(() => mode === "list" ? null : <section className={`${styles.main} ${styles.utility}`}><fieldset disabled={busy}><button disabled={busy} className={styles.formDismiss} onClick={() => setMode("list")}>← 返回列表</button>{error && <p className={styles.error} role="alert">{error}</p>}
      {mode === "create" && (
        <>
          <h2>保存新经验</h2>
          <div className={styles.fields} style={{ gridTemplateColumns: "1fr" }}>
            <label>标题<input value={form.title} onChange={(e) => setForm((p) => ({ ...p, title: e.target.value }))} /></label>
            <label>正文<textarea rows={8} value={form.body} onChange={(e) => setForm((p) => ({ ...p, body: e.target.value }))} /></label>
            <label>适用范围<input value={form.applicability} onChange={(e) => setForm((p) => ({ ...p, applicability: e.target.value }))} /></label>
            <label>反例/注意<textarea rows={4} value={form.counterexample} onChange={(e) => setForm((p) => ({ ...p, counterexample: e.target.value }))} /></label>
            <label style={{ flexDirection: "row", alignItems: "center", gap: "8px" }}>
              <input type="checkbox" checked={form.accepted} onChange={(e) => setForm((p) => ({ ...p, accepted: e.target.checked }))} />
              已明确接受此经验的用途
            </label>
          </div>
          <h3>原依据素材（可选，最多 8 项）</h3>
          <div className={styles.materialList}>
            {materials.map((m) => {
              const chosen = basisMap.has(m.reference_id);
              return (
                <div key={m.reference_id} className={styles.materialItem}>
                  <label><input type="checkbox" checked={chosen} disabled={!chosen && basisMap.size >= 8} onChange={() => toggleBasis(m)} />{labels.get(m.reference_id) || "来源需核对"}</label>
                  <p className={styles.materialMeta}>{m.kind}</p>
                </div>
              );
            })}
          </div>
          <div className={styles.actions}>
            <button className={styles.primary} disabled={busy || !loaded} onClick={save}>保存经验</button>
            <button disabled={busy} onClick={() => setMode("list")}>取消</button>
          </div>
        </>
      )}
      {mode === "detail" && selected && (
        <>
          <h2>{recordLabel(selected)}</h2>
          <p className={styles.materialMeta}>{recordMeta(selected)} · 版本 {selected.data.revision}</p>
          <div className={styles.fields} style={{ gridTemplateColumns: "1fr" }}>
            <label>正文<textarea rows={10} readOnly value={selected.data.body} /></label>
            <label>适用范围<input readOnly value={selected.data.applicability} /></label>
            <label>反例/注意<textarea rows={4} readOnly value={selected.data.counterexample} /></label>
          </div>
          {selected.data.basis_refs?.length > 0 && (
            <>
              <h3>原依据</h3>
              <div className={styles.materialList}>
                {selected.data.basis_refs.map((ref) => {
                  const m = materials.find((x) => x.reference_id === ref);
                  return <div key={ref} className={styles.materialItem}>{labels.get(ref) || m?.title || "原依据当前不可读取"}</div>;
                })}
              </div>
            </>
          )}
        </>
      )}
      {mode === "apply" && selected && (
        <>
          <h2>应用经验到草稿</h2>
          <p className={styles.sub}>选择目标内容，将经验作为新版本草稿插入（不替换当前最新版本）。</p>
          {!contents.length && <p className={styles.notice}>当前工作区没有内容。请先创建内容。</p>}
          <div className={styles.materialList}>
            {contents.map((item) => (
              <div key={item.content.entity_id} className={styles.materialItem}>
                <button disabled={busy} onClick={() => apply(selected.entity_id, item.content.entity_id, false)}>应用到「{item.version.data.title || "未命名"}」</button>
                <p className={styles.materialMeta}>{item.version.data.topic || ""}</p>
              </div>
            ))}
          </div>
          <div className={styles.actions}>
            <button disabled={busy} onClick={() => setMode("list")}>取消</button>
          </div>
        </>
      )}

  </fieldset></section>, [mode, selected, form, basisList, materials, labels, contents, busy, error, panelRequest, loaded]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { onInspect?.(panel ? { id: JSON.stringify([company, workspaceId, "ContentGrowthLearning.js", mode, selected?.entity_id || "new"]), title: mode === "create" ? "填写资料" : selected?.data.name || selected?.data.title || selected?.data.content_title || "原始资料", content: panel, request: panelRequest } : null); }, [onInspect, panel, company, workspaceId, mode, selected, panelRequest]);
  return (
    <div className={styles.main}>
      <div className={styles.row}>
        <div>
          <h1>内容经验</h1>
          <p className={styles.sub}>保留原依据、适用范围与反例，明确决定如何继续</p>
        </div>
        <div className={styles.actions}>
          {mode !== "list" && <button onClick={() => setMode("list")}>返回列表</button>}
          <Link href={contentHref(workspaceId, { view: "production" })}>← 制作目录</Link>
        </div>
      </div>
      {error && <p className={styles.error} role="alert">{error}</p>}
      {(
        <>
          <div className={styles.actions}>
            <button className={styles.primary} disabled={busy || !loaded} onClick={() => { setPanelRequest((value) => value + 1); setMode("create"); }}>保存新经验</button>
          </div>
          {loaded && !records.length && <p className={styles.notice}>还没有经验。点击「保存新经验」记录本工作区的内容制作经验。</p>}
          <div className={styles.denseRows}>
            {records.map((rec) => (
              <div key={rec.entity_id} className={styles.observationRow}>
                <div className={styles.row} style={{ justifyContent: "flex-start", gap: "12px" }}>
                  <button disabled={busy} onClick={() => { setSelected(rec); setPanelRequest((value) => value + 1); setPanelRequest((value) => value + 1); setMode("detail"); }}>查看</button>
                  <button disabled={busy} onClick={() => { setSelected(rec); setPanelRequest((value) => value + 1); setMode("apply"); }}>应用</button>
                  <span className={styles.selectionTitle}>{recordLabel(rec)}</span>
                </div>
                <p className={styles.materialMeta}>{recordMeta(rec)}</p>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
