"use client";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { writingApi as api } from "../../lib/writingApi.js";
import { chapterHref, writingViewHref } from "../../lib/writingState.mjs";
import useWritingSurface, { validateWritingSurfacePayload, validateWritingSurfaceRecord } from "./useWritingSurface.js";
import styles from "./Writing.module.css";

const EMPTY_FORM = { title: "", body: "", scope_ref: "", reference_refs: [], learning_ref: "", confirmed: false, expected_ref: "" };

export default function WritingDirection({ company, workspaceId, selectedBook = null, onInspect }) {
  const [records, setRecords] = useState(null);
  const [collection, setCollection] = useState(null);
  const [learnings, setLearnings] = useState([]);
  const [marketRefs, setMarketRefs] = useState([]);
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
  const [mode, setMode] = useState("list"); // list | create | detail | apply
  const [selected, setSelected] = useState(null);
  const [form, setForm] = useState({ ...EMPTY_FORM });
  const [applyBook, setApplyBook] = useState("");
  const [applyChapter, setApplyChapter] = useState("");
  const [historical, setHistorical] = useState(false);
  const [applyConsent, setApplyConsent] = useState(false);

  const load = useCallback(async () => {
    const token = beginRead();
    setError("");
    try {
      const [dirs, coll, learningList, snapshots] = await Promise.all([
        api.directions(company, workspaceId),
        api.collection(company, workspaceId),
        api.learnings(company, workspaceId),
        api.snapshots(company, workspaceId),
      ]);
      if (!live(token)) return;
      const payloads = [dirs, coll, learningList, snapshots];
      const scope = validateWritingSurfacePayload(coll, company, workspaceId);
      for (const payload of payloads) validateWritingSurfacePayload(payload, company, workspaceId, scope.instance_id);
      setReadyKey(surface.key);
      setRecords(dirs.records || []);
      setCollection(coll);
      const latestLearning = new Map();
      for (const record of learningList.records || []) {
        const id = record.data.identity_ref || record.entity_id;
        if (!latestLearning.has(id) || record.data.revision > latestLearning.get(id).data.revision) latestLearning.set(id, record);
      }
      setLearnings([...latestLearning.values()].filter((record) => record.data.accepted_by));
      setMarketRefs(snapshots.records || []);
    } catch (reason) {
      if (live(token)) setError(reason.message);
    }
  }, [company, workspaceId, beginRead, live, surface.key, setError]);

  useEffect(() => { setRecords(null); setCollection(null); setSelected(null); setMode("list"); setForm({ ...EMPTY_FORM }); setBusy(false); setLearnings([]); setMarketRefs([]); setApplyBook(""); setApplyChapter(""); setHistorical(false); setApplyConsent(false); setError(""); setReadyKey(""); setQuery(""); drafts.current.clear(); formKey.current = "new"; }, [surface.key, setError]);
  useEffect(() => { load(); }, [load]);

  const books = useMemo(() => collection?.books || [], [collection]);
  const chapters = useMemo(() => collection?.chapters || [], [collection]);
  const bookTitle = useCallback((ref) => books.find((b) => b.ref === ref)?.title || "", [books]);
  const refChoices = useMemo(() => [
    ...marketRefs.map((record) => ({ ref: record.entity_id, label: `市场证据 · ${record.data.title}（${record.data.period || "时点未提供"}）` })),
    ...books.map((b) => ({ ref: b.ref, label: `作品 · ${b.title}` })),
    ...chapters.map((c) => ({ ref: c.ref, label: `章节 · ${c.title}（${bookTitle(c.bookRef) || "未命名作品"}）` })),
  ], [books, chapters, bookTitle, marketRefs]);

  const toggleRef = (ref) => {
    setForm((prev) => {
      const refs = new Set(prev.reference_refs);
      if (refs.has(ref)) refs.delete(ref);
      else if (refs.size < 8) refs.add(ref);
      return { ...prev, reference_refs: Array.from(refs) };
    });
  };

  const editForm = (key, initial = EMPTY_FORM) => {
    formKey.current = key; setForm(drafts.current.get(key) || { ...initial }); setMode("create");
  };
  const cancelForm = () => { if (mode === "create") drafts.current.set(formKey.current, { ...form }); setMode("list"); setError(""); };
  const save = async () => {
    if (readyKey !== surface.key || busy || collection?.read_only) return;
    const token = surface.capture();
    if (!form.title.trim() || !form.body.trim()) { setError("方向标题与正文不能为空。"); return; }
    setBusy(true); setError("");
    try {
      const data = {
          title: form.title.trim(),
          body: form.body.trim(),
          scope_ref: form.scope_ref,
          reference_refs: form.reference_refs,
          learning_ref: form.learning_ref,
          confirmed: Boolean(form.confirmed),
        };
      const identity = await surface.request("save-direction", form.expected_ref, data);
      if (!live(token)) return;
      const result = await api.directionCommand(company, workspaceId, "save-direction", {
        request_id: identity.request_id,
        expected_ref: form.expected_ref,
        data,
      });
      if (!live(token)) return;
      validateWritingSurfaceRecord(result.record, company, workspaceId);
      surface.complete("save-direction", token);
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

  const apply = async () => {
    if (readyKey !== surface.key || busy || collection?.read_only) return;
    const token = surface.capture();
    if (!applyConsent) { setError("请明确确认本次应用方式。"); return; }
    if (!applyBook || !applyChapter) { setError("请明确选择作品与章节。"); return; }
    setBusy(true); setError("");
    try {
      const data = {
          direction_ref: selected.entity_id,
          book_ref: applyBook,
          chapter_ref: applyChapter,
          confirmed: true,
          historical: Boolean(historical),
        };
      const identity = await surface.request("apply-direction", selected.entity_id, data);
      if (!live(token)) return;
      const result = await api.directionCommand(company, workspaceId, "apply-direction", {
        request_id: identity.request_id,
        data,
      });
      if (!live(token)) return;
      if (result.book_ref !== applyBook || result.chapter_ref !== applyChapter || result.direction_ref !== selected.entity_id) throw new Error("返回的章节或方向来源不一致。");
      surface.complete("apply-direction", token);
      setMode("list");
      setApplyBook(""); setApplyChapter(""); setHistorical(false); setApplyConsent(false);
      setError("");
    } catch (reason) {
      if (live(token)) setError(reason.message);
    } finally {
      if (live(token)) setBusy(false);
    }
  };

  const scopeLabel = (rec) => rec.data.scope_ref ? `作品 · ${bookTitle(rec.data.scope_ref) || "来源需核对"}` : "整个写作工作区";

  const inspectRecord = (record) => {
    setSelected(record);
    if (!onInspect) { setMode("detail"); return; }
    onInspect({ company, workspaceId, ref: record.entity_id, title: "方向依据", content: <div className={styles.recordDetail}><h3>{record.data.title}</h3><p className={styles.opMeta}>版本 {record.data.revision} · {record.created_at}</p><span className={styles.badge}>{record.data.confirmed_by ? "已确认" : record.data.accepted_by ? "已接受 · 未验证" : "人工记录 · 未验证"}</span><p className={styles.recordBody}>{record.data.body}</p>{record.data.source_note && <section><h4>来源</h4><p>{record.data.source_note}</p></section>}{record.data.applicability && <section><h4>适用范围</h4><p>{record.data.applicability}</p><h4>反例与限制</h4><p>{record.data.counterexample || "未提供"}</p></section>}{record.data.reference_refs?.length > 0 && <section><h4>原引用依据</h4><ul>{record.data.reference_refs.map((ref) => <li key={ref}>{refChoices.find((item) => item.ref === ref)?.label || "历史来源需核对"}</li>)}</ul></section>}{record.data.learning_ref && <section><h4>来源经验</h4><p>{learnings.find((item) => item.entity_id === record.data.learning_ref)?.data.title || "原版本经验 · 来源需核对"}</p></section>}<details><summary>追溯来源与版本</summary><p>{record.entity_id}</p><p>创建于 {record.created_at}</p><p>上一版本：{record.data.previous_ref || "初始版本"}</p></details></div> });
  };
  const visibleRecords = (records || []).filter((record) => `${record.data.title} ${record.data.source_note || ""}`.toLowerCase().includes(query.trim().toLowerCase())
    && (!selectedBook || !record.data.scope_ref || record.data.scope_ref === selectedBook.ref));
  if (readyKey !== surface.key) return <div className={styles.opView}><p className={styles.opHint}>正在读取当前工作空间…</p>{error && <p className={styles.error} role="alert">{error}</p>}</div>;
  return (
    <div className={styles.opView}>
      <div className={styles.opHead}>
        <div>
          <p className={styles.eyebrow}>写作工作空间</p>
          <h2>创作方向</h2>
          <p className={styles.opHint}>明确「往哪写」 · 确认后才可被章节引用 · 本地人工记录</p>
        </div>
        <div className={styles.opActions}>
          {mode !== "list" && <button disabled={busy} onClick={cancelForm}>返回列表</button>}
          <Link href={writingViewHref(workspaceId, "")}>← 作品库</Link>
        </div>
      </div>
      {error && <p className={styles.error} role="alert">{error}</p>}
      {records === null && !error && <p className={styles.opHint}>正在读取创作方向…</p>}

      <div className={styles.surfaceToolbar}>{mode !== "list" && <button disabled={busy} onClick={cancelForm}>返回集合，保留输入</button>}<span className={styles.opBadge}>当前工作空间 · 本地记录</span></div>
      {records !== null && mode === "list" && (
        <>
          <div className={styles.operatingHero}><div><span className={styles.badge}>作品方向</span><h2>明确往哪写，让每章有据可循</h2><p>{selectedBook ? `当前作品：${selectedBook.title}` : "记录来源、用途与版本，明确选择后再应用。"}</p></div><div className={styles.heroFact}><strong>{records.length}</strong><span>条已保存方向记录</span></div></div>
          <div className={styles.collectionTools}><input aria-label="搜索方向" type="search" placeholder="搜索标题或来源" value={query} onChange={(event) => setQuery(event.target.value)} /><span>{visibleRecords.length} 条</span></div>
          <div className={styles.opActions}>
            <button disabled={busy || collection?.read_only} className={styles.primary} onClick={() => { editForm("new", { ...EMPTY_FORM, scope_ref: selectedBook?.ref || "" }); }}>新建方向</button>
          </div>
          {!records.length && <p className={styles.notice}>还没有创作方向。点击「新建方向」记录本工作区的写作方向。</p>}
          <div className={styles.opList}>
            {visibleRecords.map((rec) => (
              <div key={rec.entity_id} className={`${styles.opCard} ${selected?.entity_id === rec.entity_id ? styles.selectedRecord : ""}`}>
                <div className={styles.opRow}>
                  <button disabled={busy} onClick={() => inspectRecord(rec)}>查看依据</button>
                  <button disabled={busy || collection?.read_only || !rec.data.confirmed_by} onClick={() => {
                    setSelected(rec);
                    const first = rec.data.revision === 1;
                    setApplyBook(first && rec.data.scope_ref ? rec.data.scope_ref : "");
                    setApplyChapter(""); setHistorical(false); setApplyConsent(false);
                    setMode("apply");
                  }}>应用到章节</button>
                  <button disabled={busy || collection?.read_only} onClick={() => editForm("edit:" + rec.entity_id, { title: rec.data.title, body: rec.data.body, scope_ref: rec.data.scope_ref, reference_refs: rec.data.reference_refs, learning_ref: rec.data.learning_ref, confirmed: Boolean(rec.data.confirmed_by), expected_ref: rec.entity_id })}>修订版本</button>
                  <strong className={styles.recordTitle}>{rec.data.title || "未命名方向"}</strong>
                </div>
                <p className={styles.opMeta}>
                  {rec.data.confirmed_by ? "已确认" : "待确认"} · {scopeLabel(rec)} · 版本 {rec.data.revision}
                </p>
              </div>
            ))}
          </div>
        </>
      )}

      {mode === "create" && (
        <fieldset className={styles.recordEditor} disabled={busy || collection?.read_only}>
          <h3>{form.expected_ref ? "修订方向（产生新版本）" : "新建方向"}</h3>
          <div className={styles.opFields}>
            <label>标题<input value={form.title} maxLength={200} onChange={(e) => setForm((p) => ({ ...p, title: e.target.value }))} /></label>
            <label>正文<textarea rows={7} value={form.body} onChange={(e) => setForm((p) => ({ ...p, body: e.target.value }))} /></label>
            <label>适用范围
              <select value={form.scope_ref} onChange={(e) => setForm((p) => ({ ...p, scope_ref: e.target.value }))}>
                <option value="">整个写作工作区</option>
                {books.map((b) => <option key={b.ref} value={b.ref}>作品 · {b.title}</option>)}
              </select>
            </label>
            <label>来源经验（可选）
              <select value={form.learning_ref} onChange={(e) => setForm((p) => ({ ...p, learning_ref: e.target.value }))}>
                <option value="">不引用经验</option>
                {learnings.map((l) => <option key={l.entity_id} value={l.entity_id}>{l.data.title}（v{l.data.revision}）</option>)}
              </select>
            </label>
          </div>
          <h4>参考对象（可选，最多 8 项）</h4>
          <div className={styles.opList}>
            {refChoices.map((item) => (
              <label key={item.ref} className={styles.opPick}>
                <input type="checkbox" checked={form.reference_refs.includes(item.ref)}
                  disabled={!form.reference_refs.includes(item.ref) && form.reference_refs.length >= 8}
                  onChange={() => toggleRef(item.ref)} />
                {item.label}
              </label>
            ))}
          </div>
          <label className={styles.opPick}><input type="checkbox" checked={form.confirmed} onChange={(e) => setForm((p) => ({ ...p, confirmed: e.target.checked }))} />我已明确确认此方向</label>
          <div className={styles.opActions}>
            <button disabled={busy} onClick={save}>{form.expected_ref ? "保存新版本" : "保存方向"}</button>
            <button disabled={busy} onClick={cancelForm}>取消</button>
          </div>
        </fieldset>
      )}

      {mode === "detail" && selected && (
        <>
          <h3>{selected.data.title || "未命名方向"}</h3>
          <p className={styles.opMeta}>{selected.data.confirmed_by ? `已确认 · ${selected.data.confirmed_by}` : "待确认"} · {scopeLabel(selected)} · 版本 {selected.data.revision}</p>
          <div className={styles.opFields}>
            <label>正文<textarea rows={9} readOnly value={selected.data.body} /></label>
          </div>
          {selected.data.reference_refs?.length > 0 && (
            <>
              <h4>参考对象</h4>
              <ul className={styles.opRefs}>{selected.data.reference_refs.map((ref) => (
                <li key={ref}>{refChoices.find((x) => x.ref === ref)?.label || ref}</li>
              ))}</ul>
            </>
          )}
          {selected.data.learning_ref && <p className={styles.opMeta}>来源经验：{selected.data.learning_ref}</p>}
          <div className={styles.opActions}>
            <button disabled={busy || collection?.read_only} onClick={() => {
              setForm({ title: selected.data.title, body: selected.data.body, scope_ref: selected.data.scope_ref,
                reference_refs: selected.data.reference_refs, learning_ref: selected.data.learning_ref,
                confirmed: Boolean(selected.data.confirmed_by), expected_ref: selected.entity_id });
              setMode("create");
            }}>修订为新版本</button>
          </div>
        </>
      )}

      {mode === "apply" && selected && (
        <>
          <h3>将方向应用到章节</h3>
          <p className={styles.opHint}>「{selected.data.title}」 · 应用仅建立章节与方向的显式引用，不改正文。</p>
          <div className={styles.opFields}>
            <label>作品
              <select value={applyBook} onChange={(e) => { setApplyBook(e.target.value); setApplyChapter(""); }}>
                <option value="">请选择作品</option>
                {books.map((b) => <option key={b.ref} value={b.ref}>{b.title}</option>)}
              </select>
            </label>
            <label>章节
              <select value={applyChapter} onChange={(e) => setApplyChapter(e.target.value)} disabled={!applyBook}>
                <option value="">请选择章节</option>
                {chapters.filter((c) => c.bookRef === applyBook).map((c) => <option key={c.ref} value={c.ref}>{c.title}</option>)}
              </select>
            </label>
          </div>
          <label className={styles.opPick}><input type="checkbox" checked={historical} onChange={(e) => setHistorical(e.target.checked)} />我明确知道引用的是历史版本方向</label>
          <label className={styles.opPick}><input type="checkbox" checked={applyConsent} onChange={(event) => setApplyConsent(event.target.checked)} />我确认只关联这个方向，不改写章节正文</label>
          <div className={styles.opActions}>
            <button disabled={busy || !applyConsent} onClick={apply}>确认应用</button>
            {applyChapter && <Link href={chapterHref(workspaceId, { mode: "chapter", book: applyBook, chapter: applyChapter })}>打开该章节</Link>}
          </div>
        </>
      )}
    </div>
  );
}
