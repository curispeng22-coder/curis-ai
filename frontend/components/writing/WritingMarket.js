"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { writingApi as api } from "../../lib/writingApi.js";
import { writingViewHref } from "../../lib/writingState.mjs";
import useWritingSurface, { validateWritingSurfacePayload, validateWritingSurfaceRecord } from "./useWritingSurface.js";
import styles from "./Writing.module.css";

const EMPTY_FORM = { title: "", body: "", period: "", source_note: "" };

export default function WritingMarket({ company, workspaceId, selectedBook = null, onInspect }) {
  const [records, setRecords] = useState(null);
  const [collection, setCollection] = useState(null);
  const surface = useWritingSurface(company, workspaceId, selectedBook?.ref || "");
  const { beginRead, live } = surface;
  const [readyKey, setReadyKey] = useState("");
  const drafts = useRef(new Map());
  const formKey = useRef("new");
  const [query, setQuery] = useState("");
  const [errorRead, setErrorRead] = useState({ key: "", message: "" });
  const error = errorRead.key === surface.key ? errorRead.message : "";
  const setError = useCallback((message) => setErrorRead({ key: surface.key, message }), [surface.key]);
  const [busy, setBusy] = useState(false);
  const [mode, setMode] = useState("list"); // list | create | detail
  const [selected, setSelected] = useState(null);
  const [form, setForm] = useState({ ...EMPTY_FORM });

  const load = useCallback(async () => {
    const token = beginRead();
    setError("");
    try {
      const [list, coll] = await Promise.all([
        api.snapshots(company, workspaceId),
        api.collection(company, workspaceId),
      ]);
      if (!live(token)) return;
      const payloads = [list, coll];
      const scope = validateWritingSurfacePayload(coll, company, workspaceId);
      for (const payload of payloads) validateWritingSurfacePayload(payload, company, workspaceId, scope.instance_id);
      setReadyKey(surface.key);
      setRecords(list.records || []);
      setCollection(coll);
    } catch (reason) {
      if (live(token)) setError(reason.message);
    }
  }, [company, workspaceId, beginRead, live, surface.key, setError]);

  useEffect(() => { setRecords(null); setCollection(null); setSelected(null); setMode("list"); setForm({ ...EMPTY_FORM }); setBusy(false); setError(""); setReadyKey(""); setQuery(""); drafts.current.clear(); formKey.current = "new"; }, [surface.key, setError]);
  useEffect(() => { load(); }, [load]);

  const editForm = (key, initial = EMPTY_FORM) => {
    formKey.current = key; setForm(drafts.current.get(key) || { ...initial }); setMode("create");
  };
  const cancelForm = () => { if (mode === "create") drafts.current.set(formKey.current, { ...form }); setMode("list"); setError(""); };
  const save = async () => {
    if (readyKey !== surface.key || busy || collection?.read_only) return;
    const token = surface.capture();
    if (!form.title.trim() || !form.body.trim() || !form.source_note.trim()) {
      setError("快照标题、正文与人工来源说明不能为空。");
      return;
    }
    setBusy(true); setError("");
    try {
      const data = {
          title: form.title.trim(),
          body: form.body.trim(),
          period: form.period.trim(),
          source_note: form.source_note.trim(),
        };
      const identity = await surface.request("save-snapshot", "", data);
      if (!live(token)) return;
      const result = await api.snapshotCommand(company, workspaceId, "save-snapshot", {
        request_id: identity.request_id,
        expected_ref: "",
        data,
      });
      if (!live(token)) return;
      validateWritingSurfaceRecord(result.record, company, workspaceId);
      surface.complete("save-snapshot", token);
      drafts.current.delete(formKey.current);
      setForm({ ...EMPTY_FORM });
      setMode("list");
      await load();
    } catch (reason) {
      if (live(token)) setError(reason.message);
    } finally {
      if (live(token)) setBusy(false);
    }
  };

  const inspectRecord = (record) => {
    setSelected(record);
    if (!onInspect) { setMode("detail"); return; }
    onInspect({ company, workspaceId, ref: record.entity_id, title: "快照依据", content: <div className={styles.recordDetail}><h3>{record.data.title}</h3><p className={styles.opMeta}>版本 {record.data.revision} · {record.created_at}</p><span className={styles.badge}>{record.data.confirmed_by ? "已确认" : record.data.accepted_by ? "已接受 · 未验证" : "人工记录 · 未验证"}</span><p className={styles.recordBody}>{record.data.body}</p>{record.data.source_note && <section><h4>来源</h4><p>{record.data.source_note}</p></section>}{record.data.applicability && <section><h4>适用范围</h4><p>{record.data.applicability}</p><h4>反例与限制</h4><p>{record.data.counterexample || "未提供"}</p></section>}<details><summary>追溯来源与版本</summary><p>{record.entity_id}</p><p>创建于 {record.created_at}</p></details></div> });
  };
  const visibleRecords = (records || []).filter((record) => `${record.data.title} ${record.data.source_note || ""}`.toLowerCase().includes(query.trim().toLowerCase()));
  if (readyKey !== surface.key) return <div className={styles.opView}><p className={styles.opHint}>正在读取当前工作空间…</p>{error && <p className={styles.error} role="alert">{error}</p>}</div>;
  return (
    <div className={styles.opView}>
      <div className={styles.opHead}>
        <div>
          <p className={styles.eyebrow}>写作工作空间</p>
          <h2>人工市场快照</h2>
          <p className={styles.opHint}>人工录入的选题/平台/读者信号 · 无平台自动采集 · 人工来源未核验 · 原记录不改写</p>
        </div>
        <div className={styles.opActions}>
          {mode !== "list" && <button disabled={busy} onClick={cancelForm}>返回列表</button>}
          <Link href={writingViewHref(workspaceId, "")}>← 作品库</Link>
        </div>
      </div>
      {error && <p className={styles.error} role="alert">{error}</p>}
      {records === null && !error && <p className={styles.opHint}>正在读取市场快照…</p>}

      <div className={styles.surfaceToolbar}>{mode !== "list" && <button disabled={busy} onClick={cancelForm}>返回集合，保留输入</button>}<span className={styles.opBadge}>当前工作空间 · 本地记录</span></div>
      {records !== null && mode === "list" && (
        <>
          <div className={styles.operatingHero}><div><span className={styles.badge}>市场证据</span><h2>从有来源的记录，发现可写的方向</h2><p>{selectedBook ? `当前作品：${selectedBook.title}` : "记录来源、用途与版本，明确选择后再应用。"}</p></div><div className={styles.heroFact}><strong>{records.length}</strong><span>条已保存快照记录</span></div></div>
          <div className={styles.collectionTools}><input aria-label="搜索快照" type="search" placeholder="搜索标题或来源" value={query} onChange={(event) => setQuery(event.target.value)} /><span>{visibleRecords.length} 条</span></div>
          <div className={styles.opActions}>
            <button disabled={busy || collection?.read_only} className={styles.primary} onClick={() => { editForm("new", { ...EMPTY_FORM }); }}>录入新快照</button>
          </div>
          {!records.length && <p className={styles.notice}>还没有市场快照。所有信号均由你人工录入，系统不连接平台、不自动采集。</p>}
          <div className={styles.opList}>
            {visibleRecords.map((rec) => (
              <div key={rec.entity_id} className={`${styles.opCard} ${selected?.entity_id === rec.entity_id ? styles.selectedRecord : ""}`}>
                <div className={styles.opRow}>
                  <button disabled={busy} onClick={() => inspectRecord(rec)}>查看依据</button>
                  <strong className={styles.recordTitle}>{rec.data.title || "未命名快照"}</strong>
                </div>
                <p className={styles.opMeta}>
                  <span className={styles.opBadge}>人工录入 · 未验证</span>
                  {rec.data.period || "未填周期"}
                </p>
              </div>
            ))}
          </div>
        </>
      )}

      {mode === "create" && (
        <fieldset className={styles.recordEditor} disabled={busy || collection?.read_only}>
          <h3>录入市场快照</h3>
          <div className={styles.opFields}>
            <label>标题<input value={form.title} maxLength={200} onChange={(e) => setForm((p) => ({ ...p, title: e.target.value }))} /></label>
            <label>正文<textarea rows={8} value={form.body} onChange={(e) => setForm((p) => ({ ...p, body: e.target.value }))} /></label>
            <label>观察周期<input placeholder="如 2026-10 / 2026-W40" value={form.period} maxLength={200} onChange={(e) => setForm((p) => ({ ...p, period: e.target.value }))} /></label>
            <label>人工来源说明（必填）<input placeholder="人工观察 / 编辑沟通 / 公开榜单阅读" value={form.source_note} maxLength={500} onChange={(e) => setForm((p) => ({ ...p, source_note: e.target.value }))} /></label>
          </div>
          <p className={styles.opHint}>保存后保留这次人工记录与来源说明，尚未核验；后续变化请另录新记录。</p>
          <div className={styles.opActions}>
            <button disabled={busy} onClick={save}>保存快照</button>
            <button disabled={busy} onClick={cancelForm}>取消</button>
          </div>
        </fieldset>
      )}

      {mode === "detail" && selected && (
        <>
          <h3>{selected.data.title || "未命名快照"}</h3>
          <p className={styles.opMeta}><span className={styles.opBadge}>人工录入 · 未验证</span>{selected.data.period || "未填周期"}</p>
          <div className={styles.opFields}>
            <label>正文<textarea rows={10} readOnly value={selected.data.body} /></label>
            <label>人工来源说明<input readOnly value={selected.data.source_note} /></label>
          </div>
          <p className={styles.opHint}>记录人：{selected.owner_ref || "—"}</p>
        </>
      )}
    </div>
  );
}
