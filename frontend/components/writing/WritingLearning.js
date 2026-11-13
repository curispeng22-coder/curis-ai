"use client";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { writingApi as api } from "../../lib/writingApi.js";
import { writingViewHref } from "../../lib/writingState.mjs";
import useWritingSurface, { validateWritingSurfacePayload, validateWritingSurfaceRecord } from "./useWritingSurface.js";
import styles from "./Writing.module.css";

const EMPTY_FORM = { title: "", body: "", applicability: "", counterexample: "", accepted: false, basis_refs: [], expected_ref: "" };

export default function WritingLearning({ company, workspaceId, selectedBook = null, onInspect, onNavigate }) {
  const [records, setRecords] = useState(null);
  const [collection, setCollection] = useState(null);
  const [operatingSources, setOperatingSources] = useState([]);
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
  const [newTitle, setNewTitle] = useState("");
  const [historical, setHistorical] = useState(false);
  const [applyConsent, setApplyConsent] = useState(false);

  const load = useCallback(async () => {
    const token = beginRead();
    setError("");
    try {
      const [list, coll, snapshots, directions, observations] = await Promise.all([
        api.learnings(company, workspaceId),
        api.collection(company, workspaceId),
        api.snapshots(company, workspaceId), api.directions(company, workspaceId), api.observations(company, workspaceId),
      ]);
      if (!live(token)) return;
      const payloads = [list, coll, snapshots, directions, observations];
      const scope = validateWritingSurfacePayload(coll, company, workspaceId);
      for (const payload of payloads) validateWritingSurfacePayload(payload, company, workspaceId, scope.instance_id);
      setReadyKey(surface.key);
      setRecords(list.records || []);
      setCollection(coll);
      setOperatingSources([...(snapshots.records || []).map(record => ({ ...record, sourceLabel: "市场记录" })), ...(directions.records || []).map(record => ({ ...record, sourceLabel: "作品方向" })), ...(observations.records || []).map(record => ({ ...record, sourceLabel: "人工观察" }))]);
    } catch (reason) {
      if (live(token)) setError(reason.message);
    }
  }, [company, workspaceId, beginRead, live, surface.key, setError]);

  useEffect(() => { setRecords(null); setCollection(null); setOperatingSources([]); setSelected(null); setMode("list"); setForm({ ...EMPTY_FORM }); setBusy(false); setApplyBook(""); setNewTitle(""); setHistorical(false); setApplyConsent(false); setError(""); setReadyKey(""); setQuery(""); drafts.current.clear(); formKey.current = "new"; }, [surface.key, setError]);
  useEffect(() => { load(); }, [load]);

  const books = useMemo(() => collection?.books || [], [collection]);
  const chapters = useMemo(() => collection?.chapters || [], [collection]);
  const basisChoices = useMemo(() => [
    ...operatingSources.map(record => ({ ref: record.entity_id, label: `${record.sourceLabel} · ${record.data.title} · 原版本 ${record.data.revision}（未验证）` })),
    ...books.map((b) => ({ ref: b.ref, label: `作品 · ${b.title}` })),
    ...chapters.map((c) => {
      const book = books.find((b) => b.ref === c.bookRef);
      return { ref: c.ref, label: `章节 · ${c.title}（${book?.title || "未命名作品"}）` };
    }),
  ], [books, chapters, operatingSources]);

  const toggleBasis = (ref) => {
    setForm((prev) => {
      const refs = new Set(prev.basis_refs);
      if (refs.has(ref)) refs.delete(ref);
      else if (refs.size < 8) refs.add(ref);
      return { ...prev, basis_refs: Array.from(refs) };
    });
  };

  const editForm = (key, initial = EMPTY_FORM) => {
    formKey.current = key; setForm(drafts.current.get(key) || { ...initial }); setMode("create");
  };
  const cancelForm = () => { if (mode === "create") drafts.current.set(formKey.current, { ...form }); setMode("list"); setError(""); };
  const save = async () => {
    if (readyKey !== surface.key || busy || collection?.read_only) return;
    const token = surface.capture();
    if (!form.title.trim() || !form.body.trim()) { setError("经验标题与正文不能为空。"); return; }
    setBusy(true); setError("");
    try {
      const data = {
          title: form.title.trim(),
          body: form.body.trim(),
          basis_refs: form.basis_refs,
          applicability: form.applicability.trim(),
          counterexample: form.counterexample.trim(),
          accepted: Boolean(form.accepted),
        };
      const identity = await surface.request("save-learning", form.expected_ref, data);
      if (!live(token)) return;
      const result = await api.learningCommand(company, workspaceId, "save-learning", {
        request_id: identity.request_id,
        expected_ref: form.expected_ref,
        data,
      });
      if (!live(token)) return;
      validateWritingSurfaceRecord(result.record, company, workspaceId);
      surface.complete("save-learning", token);
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
    if (!applyBook || !newTitle.trim()) { setError("请选择作品并填写新章节标题。"); return; }
    setBusy(true); setError("");
    try {
      const data = {
          learning_ref: selected.entity_id,
          book_ref: applyBook,
          title: newTitle.trim(),
          confirmed: true,
          historical: Boolean(historical),
        };
      const identity = await surface.request("use-learning", selected.entity_id, data);
      if (!live(token)) return;
      const result = await api.learningCommand(company, workspaceId, "use-learning", {
        request_id: identity.request_id,
        data,
      });
      if (!live(token)) return;
      if (result.book_ref !== applyBook || result.learning_ref !== selected.entity_id || !result.chapter_ref) throw new Error("新章节来源无法确认，请重新读取原作品。");
      surface.complete("use-learning", token);
      setMode("list"); setApplyBook(""); setNewTitle(""); setHistorical(false); setApplyConsent(false);
      onNavigate?.({ mode: "chapter", book: result.book_ref, chapter: result.chapter_ref });
    } catch (reason) {
      if (live(token)) setError(reason.message);
    } finally {
      if (live(token)) setBusy(false);
    }
  };

  const inspectRecord = (record) => {
    setSelected(record);
    if (!onInspect) { setMode("detail"); return; }
    onInspect({ company, workspaceId, ref: record.entity_id, title: "经验依据", content: <div className={styles.recordDetail}><h3>{record.data.title}</h3><p className={styles.opMeta}>版本 {record.data.revision} · {record.created_at}</p><span className={styles.badge}>{record.data.confirmed_by ? "已确认" : record.data.accepted_by ? "已接受 · 未验证" : "人工记录 · 未验证"}</span><p className={styles.recordBody}>{record.data.body}</p>{record.data.source_note && <section><h4>来源</h4><p>{record.data.source_note}</p></section>}{record.data.applicability && <section><h4>适用范围</h4><p>{record.data.applicability}</p><h4>反例与限制</h4><p>{record.data.counterexample || "未提供"}</p></section>}{record.data.basis_refs?.length > 0 && <section><h4>原引用依据</h4><ul>{record.data.basis_refs.map((ref) => <li key={ref}>{basisChoices.find((item) => item.ref === ref)?.label || "历史来源需核对"}</li>)}</ul></section>}<details><summary>追溯来源与版本</summary><p>{record.entity_id}</p><p>创建于 {record.created_at}</p><p>上一版本：{record.data.previous_ref || "初始版本"}</p></details></div> });
  };
  const visibleRecords = (records || []).filter((record) => `${record.data.title} ${record.data.source_note || ""}`.toLowerCase().includes(query.trim().toLowerCase()));
  if (readyKey !== surface.key) return <div className={styles.opView}><p className={styles.opHint}>正在读取当前工作空间…</p>{error && <p className={styles.error} role="alert">{error}</p>}</div>;
  return (
    <div className={styles.opView}>
      <div className={styles.opHead}>
        <div>
          <p className={styles.eyebrow}>写作工作空间</p>
          <h2>经验学习面</h2>
          <p className={styles.opHint}>人工写作经验 · 全部「未验证」 · 应用生成新章节，不改写现有章节</p>
        </div>
        <div className={styles.opActions}>
          {mode !== "list" && <button disabled={busy} onClick={cancelForm}>返回列表</button>}
          <Link href={writingViewHref(workspaceId, "")}>← 作品库</Link>
        </div>
      </div>
      {error && <p className={styles.error} role="alert">{error}</p>}
      {records === null && !error && <p className={styles.opHint}>正在读取经验…</p>}

      <div className={styles.surfaceToolbar}>{mode !== "list" && <button disabled={busy} onClick={cancelForm}>返回集合，保留输入</button>}<span className={styles.opBadge}>当前工作空间 · 本地记录</span></div>
      {records !== null && mode === "list" && (
        <>
          <div className={styles.operatingHero}><div><span className={styles.badge}>写作经验</span><h2>把已有依据，积累成下次创作的方法</h2><p>{selectedBook ? `当前作品：${selectedBook.title}` : "记录来源、用途与版本，明确选择后再应用。"}</p></div><div className={styles.heroFact}><strong>{records.length}</strong><span>条已保存经验记录</span></div></div>
          <div className={styles.collectionTools}><input aria-label="搜索经验" type="search" placeholder="搜索标题或来源" value={query} onChange={(event) => setQuery(event.target.value)} /><span>{visibleRecords.length} 条</span></div>
          <div className={styles.opActions}>
            <button disabled={busy || collection?.read_only} className={styles.primary} onClick={() => { editForm("new", { ...EMPTY_FORM }); }}>记录经验</button>
          </div>
          {!records.length && <p className={styles.notice}>还没有写作经验。点击「记录经验」沉淀本工作区的写作经验。</p>}
          <div className={styles.opList}>
            {visibleRecords.map((rec) => (
              <div key={rec.entity_id} className={`${styles.opCard} ${selected?.entity_id === rec.entity_id ? styles.selectedRecord : ""}`}>
                <div className={styles.opRow}>
                  <button disabled={busy} onClick={() => inspectRecord(rec)}>查看依据</button>
                  <button disabled={busy || collection?.read_only || !rec.data.accepted_by} onClick={() => {
                    setSelected(rec); setApplyBook(""); setNewTitle(""); setHistorical(false); setApplyConsent(false); setMode("apply");
                  }}>应用到新章节</button>
                  <button disabled={busy || collection?.read_only} onClick={() => editForm("edit:" + rec.entity_id, { title: rec.data.title, body: rec.data.body, applicability: rec.data.applicability, counterexample: rec.data.counterexample, accepted: Boolean(rec.data.accepted_by), basis_refs: rec.data.basis_refs, expected_ref: rec.entity_id })}>修订版本</button>
                  <strong className={styles.recordTitle}>{rec.data.title || "未命名经验"}</strong>
                </div>
                <p className={styles.opMeta}>
                  <span className={styles.opBadge}>未验证</span>
                  {rec.data.accepted_by ? "已接受" : "待接受"} · 版本 {rec.data.revision}
                </p>
              </div>
            ))}
          </div>
        </>
      )}

      {mode === "create" && (
        <fieldset className={styles.recordEditor} disabled={busy || collection?.read_only}>
          <h3>{form.expected_ref ? "修订经验（产生新版本）" : "记录经验"}</h3>
          <div className={styles.opFields}>
            <label>标题<input value={form.title} maxLength={200} onChange={(e) => setForm((p) => ({ ...p, title: e.target.value }))} /></label>
            <label>经验正文<textarea rows={8} value={form.body} onChange={(e) => setForm((p) => ({ ...p, body: e.target.value }))} /></label>
            <label>适用范围<input value={form.applicability} onChange={(e) => setForm((p) => ({ ...p, applicability: e.target.value }))} /></label>
            <label>反例与限制<textarea rows={4} value={form.counterexample} onChange={(e) => setForm((p) => ({ ...p, counterexample: e.target.value }))} /></label>
          </div>
          <h4>原依据（可选，最多 8 项）</h4>
          <div className={styles.opList}>
            {basisChoices.map((item) => (
              <label key={item.ref} className={styles.opPick}>
                <input type="checkbox" checked={form.basis_refs.includes(item.ref)}
                  disabled={!form.basis_refs.includes(item.ref) && form.basis_refs.length >= 8}
                  onChange={() => toggleBasis(item.ref)} />
                {item.label}
              </label>
            ))}
          </div>
          <label className={styles.opPick}><input type="checkbox" checked={form.accepted} onChange={(e) => setForm((p) => ({ ...p, accepted: e.target.checked }))} />我已明确接受此经验的用途</label>
          <div className={styles.opActions}>
            <button disabled={busy} onClick={save}>{form.expected_ref ? "保存新版本" : "保存经验"}</button>
            <button disabled={busy} onClick={cancelForm}>取消</button>
          </div>
        </fieldset>
      )}

      {mode === "detail" && selected && (
        <>
          <h3>{selected.data.title || "未命名经验"}</h3>
          <p className={styles.opMeta}><span className={styles.opBadge}>未验证</span>{selected.data.accepted_by ? "已接受" : "待接受"} · 版本 {selected.data.revision}</p>
          <div className={styles.opFields}>
            <label>经验正文<textarea rows={10} readOnly value={selected.data.body} /></label>
            <label>适用范围<input readOnly value={selected.data.applicability} /></label>
            <label>反例与限制<textarea rows={4} readOnly value={selected.data.counterexample} /></label>
          </div>
          {selected.data.basis_refs?.length > 0 && (
            <>
              <h4>原依据</h4>
              <ul className={styles.opRefs}>{selected.data.basis_refs.map((ref) => (
                <li key={ref}>{basisChoices.find((x) => x.ref === ref)?.label || ref}</li>
              ))}</ul>
            </>
          )}
          <div className={styles.opActions}>
            <button disabled={busy || collection?.read_only} onClick={() => {
              setForm({ title: selected.data.title, body: selected.data.body, applicability: selected.data.applicability,
                counterexample: selected.data.counterexample, accepted: Boolean(selected.data.accepted_by),
                basis_refs: selected.data.basis_refs, expected_ref: selected.entity_id });
              setMode("create");
            }}>修订为新版本</button>
          </div>
        </>
      )}

      {mode === "apply" && selected && (
        <>
          <h3>应用经验到新章节</h3>
          <p className={styles.opHint}>将在所选作品下新建章节并写入首版草稿（含原经验/适用范围/反例），不触碰任何现有章节。</p>
          <div className={styles.opFields}>
            <label>目标作品
              <select value={applyBook} onChange={(e) => setApplyBook(e.target.value)}>
                <option value="">请选择作品</option>
                {books.map((b) => <option key={b.ref} value={b.ref}>{b.title}</option>)}
              </select>
            </label>
            <label>新章节标题<input value={newTitle} maxLength={160} onChange={(e) => setNewTitle(e.target.value)} /></label>
          </div>
          <label className={styles.opPick}><input type="checkbox" checked={historical} onChange={(e) => setHistorical(e.target.checked)} />我明确知道引用的是历史版本经验</label>
          <label className={styles.opPick}><input type="checkbox" checked={applyConsent} onChange={(event) => setApplyConsent(event.target.checked)} />我确认创建一个新章节，不替换任何已有章节</label>
          <div className={styles.opActions}>
            <button disabled={busy || !applyConsent} onClick={apply}>创建新章节并跳转</button>
          </div>
        </>
      )}
    </div>
  );
}
