"use client";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { writingApi as api } from "../../lib/writingApi.js";
import { writingViewHref } from "../../lib/writingState.mjs";
import useWritingSurface, { validateWritingSurfacePayload, validateWritingSurfaceRecord } from "./useWritingSurface.js";
import styles from "./Writing.module.css";

const EMPTY_FORM = { title: "", body: "", scope_ref: "", period: "" };

export default function WritingPerformance({ company, workspaceId, selectedBook = null, onInspect }) {
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
        api.observations(company, workspaceId),
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

  const books = useMemo(() => collection?.books || [], [collection]);
  const chapters = useMemo(() => collection?.chapters || [], [collection]);
  const scopeOptions = useMemo(() => [
    ...books.map((b) => ({ ref: b.ref, label: `作品 · ${b.title}`, kind: "book" })),
    ...chapters.map((ch) => {
      const book = books.find((b) => b.ref === ch.bookRef);
      return { ref: ch.ref, label: `章节 · ${ch.title}（${book?.title || "未命名作品"}）`, kind: "chapter" };
    }),
  ], [books, chapters]);

  const scopeLabel = (ref) => scopeOptions.find((item) => item.ref === ref)?.label || "来源需核对";

  const editForm = (key, initial = EMPTY_FORM) => {
    formKey.current = key; setForm(drafts.current.get(key) || { ...initial }); setMode("create");
  };
  const cancelForm = () => { if (mode === "create") drafts.current.set(formKey.current, { ...form }); setMode("list"); setError(""); };
  const save = async () => {
    if (readyKey !== surface.key || busy || collection?.read_only) return;
    const token = surface.capture();
    if (!form.title.trim() || !form.body.trim()) { setError("观察标题与正文不能为空。"); return; }
    if (!form.scope_ref) { setError("请明确选择观察对象（作品或章节）。"); return; }
    setBusy(true); setError("");
    try {
      const data = {
          title: form.title.trim(),
          body: form.body.trim(),
          scope_ref: form.scope_ref,
          period: form.period.trim(),
        };
      const identity = await surface.request("save-observation", "", data);
      if (!live(token)) return;
      const result = await api.observationCommand(company, workspaceId, "save-observation", {
        request_id: identity.request_id,
        expected_ref: "",
        data,
      });
      if (!live(token)) return;
      validateWritingSurfaceRecord(result.record, company, workspaceId);
      surface.complete("save-observation", token);
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
    onInspect({ company, workspaceId, ref: record.entity_id, title: "观察依据", content: <div className={styles.recordDetail}><h3>{record.data.title}</h3><p className={styles.opMeta}>版本 {record.data.revision} · {record.created_at}</p><span className={styles.badge}>{record.data.confirmed_by ? "已确认" : record.data.accepted_by ? "已接受 · 未验证" : "人工记录 · 未验证"}</span><p className={styles.recordBody}>{record.data.body}</p>{record.data.source_note && <section><h4>来源</h4><p>{record.data.source_note}</p></section>}{record.data.applicability && <section><h4>适用范围</h4><p>{record.data.applicability}</p><h4>反例与限制</h4><p>{record.data.counterexample || "未提供"}</p></section>}<details><summary>追溯来源与版本</summary><p>{record.entity_id}</p><p>创建于 {record.created_at}</p></details></div> });
  };
  const visibleRecords = (records || []).filter((record) => `${record.data.title} ${record.data.source_note || ""}`.toLowerCase().includes(query.trim().toLowerCase()));
  if (readyKey !== surface.key) return <div className={styles.opView}><p className={styles.opHint}>正在读取当前工作空间…</p>{error && <p className={styles.error} role="alert">{error}</p>}</div>;
  return (
    <div className={styles.opView}>
      <div className={styles.opHead}>
        <div>
          <p className={styles.eyebrow}>写作工作空间</p>
          <h2>人工表现观察</h2>
          <p className={styles.opHint}>对作品/章节表现的人工记录 · 全部「未验证」 · 人工观察未核验 · 原记录不改写</p>
        </div>
        <div className={styles.opActions}>
          {mode !== "list" && <button disabled={busy} onClick={cancelForm}>返回列表</button>}
          <Link href={writingViewHref(workspaceId, "")}>← 作品库</Link>
        </div>
      </div>
      {error && <p className={styles.error} role="alert">{error}</p>}

      <p className={styles.connectionNote} role="note">平台读者与收益未连接；以下为人工观察，不代表平台数据。</p>

      {records === null && !error && <p className={styles.opHint}>正在读取表现观察…</p>}

      <div className={styles.surfaceToolbar}>{mode !== "list" && <button disabled={busy} onClick={cancelForm}>返回集合，保留输入</button>}<span className={styles.opBadge}>当前工作空间 · 本地记录</span></div>
      {records !== null && mode === "list" && (
        <>
          <div className={styles.operatingHero}><div><span className={styles.badge}>读者与收益</span><h2>记录作品反馈，再判断下一步</h2><p>{selectedBook ? `当前作品：${selectedBook.title}` : "记录来源、用途与版本，明确选择后再应用。"}</p></div><div className={styles.heroFact}><strong>{records.length}</strong><span>条已保存观察记录</span></div></div>
          <div className={styles.collectionTools}><input aria-label="搜索观察" type="search" placeholder="搜索标题或来源" value={query} onChange={(event) => setQuery(event.target.value)} /><span>{visibleRecords.length} 条</span></div>
          <div className={styles.opActions}>
            <button disabled={busy || collection?.read_only} className={styles.primary} onClick={() => { editForm("new", { ...EMPTY_FORM }); }}>录入新观察</button>
          </div>
          {!records.length && <p className={styles.notice}>还没有表现观察。请基于人工沟通与自查如实记录，不推测平台数据。</p>}
          <div className={styles.opList}>
            {visibleRecords.map((rec) => (
              <div key={rec.entity_id} className={`${styles.opCard} ${selected?.entity_id === rec.entity_id ? styles.selectedRecord : ""}`}>
                <div className={styles.opRow}>
                  <button disabled={busy} onClick={() => inspectRecord(rec)}>查看依据</button>
                  <strong className={styles.recordTitle}>{rec.data.title || "未命名观察"}</strong>
                </div>
                <p className={styles.opMeta}>
                  <span className={styles.opBadge}>人工录入 · 未验证</span>
                  {scopeLabel(rec.data.scope_ref)} · {rec.data.period || "未填周期"}
                </p>
              </div>
            ))}
          </div>
        </>
      )}

      {mode === "create" && (
        <fieldset className={styles.recordEditor} disabled={busy || collection?.read_only}>
          <h3>录入表现观察</h3>
          <div className={styles.opFields}>
            <label>标题<input value={form.title} maxLength={200} onChange={(e) => setForm((p) => ({ ...p, title: e.target.value }))} /></label>
            <label>正文<textarea rows={8} value={form.body} onChange={(e) => setForm((p) => ({ ...p, body: e.target.value }))} /></label>
            <label>观察对象（作品或章节）
              <select value={form.scope_ref} onChange={(e) => setForm((p) => ({ ...p, scope_ref: e.target.value }))}>
                <option value="">请选择作品或章节</option>
                {books.map((b) => <option key={b.ref} value={b.ref}>作品 · {b.title}</option>)}
                {chapters.map((ch) => {
                  const book = books.find((b) => b.ref === ch.bookRef);
                  return <option key={ch.ref} value={ch.ref}>章节 · {ch.title}（{book?.title || "未命名作品"}）</option>;
                })}
              </select>
            </label>
            <label>观察周期<input placeholder="如 2026-W40 / 2026-10" value={form.period} maxLength={200} onChange={(e) => setForm((p) => ({ ...p, period: e.target.value }))} /></label>
          </div>
          <p className={styles.opHint}>保存后保留这次人工观察，尚未核验；后续变化请另录新观察。</p>
          <div className={styles.opActions}>
            <button disabled={busy} onClick={save}>保存观察</button>
            <button disabled={busy} onClick={cancelForm}>取消</button>
          </div>
        </fieldset>
      )}

      {mode === "detail" && selected && (
        <>
          <h3>{selected.data.title || "未命名观察"}</h3>
          <p className={styles.opMeta}>
            <span className={styles.opBadge}>人工录入 · 未验证</span>
            {scopeLabel(selected.data.scope_ref)} · {selected.data.period || "未填周期"}
          </p>
          <div className={styles.opFields}>
            <label>正文<textarea rows={10} readOnly value={selected.data.body} /></label>
          </div>
          <p className={styles.opHint}>记录人：{selected.owner_ref || "—"} · 外部平台数据：未连接</p>
        </>
      )}
    </div>
  );
}
