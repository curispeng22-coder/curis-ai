"use client";
import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { writingApi as api } from "../../lib/writingApi.js";
import { chapterHref, writingViewHref } from "../../lib/writingState.mjs";
import useWritingSurface, { validateWritingSurfacePayload, validateWritingSurfaceRecord } from "./useWritingSurface.js";
import styles from "./Writing.module.css";

export default function WritingOverview({ company, workspaceId, selectedBook = null, onInspect }) {
  const [view, setView] = useState(null);
  const surface = useWritingSurface(company, workspaceId, selectedBook?.ref || "");
  const { beginRead, live } = surface;
  const [readyKey, setReadyKey] = useState("");
  const [errorRead, setErrorRead] = useState({ key: "", message: "" });
  const error = errorRead.key === surface.key ? errorRead.message : "";
  const setError = useCallback((message) => setErrorRead({ key: surface.key, message }), [surface.key]);

  const load = useCallback(async () => {
    const token = beginRead();
    setError("");
    try {
      const payload = await api.overview(company, workspaceId);
      if (!live(token)) return;
      validateWritingSurfacePayload(payload, company, workspaceId);
      setReadyKey(surface.key); setView(payload);
    } catch (reason) {
      if (live(token)) setError(reason.message);
    }
  }, [company, workspaceId, beginRead, live, surface.key, setError]);

  useEffect(() => { setView(null); setError(""); setReadyKey(""); }, [surface.key, setError]);
  useEffect(() => { load(); }, [load]);

  const bookTitles = useMemo(() => new Map((view?.books || []).map((b) => [b.ref, b.title])), [view]);
  const chapterTitles = useMemo(() => new Map((view?.chapters || []).map((c) => [c.ref, c.title])), [view]);

  const scopeLabel = (ref) => {
    if (!ref) return "工作区级";
    if (bookTitles.has(ref)) return `作品 · ${bookTitles.get(ref)}`;
    if (chapterTitles.has(ref)) return `章节 · ${chapterTitles.get(ref)}`;
    return "来源需核对";
  };

  const inspect = async (kind, item) => {
    const token = beginRead();
    try {
      const payload = await api[kind](company, workspaceId, item.ref);
      if (!live(token)) return;
      const record = validateWritingSurfaceRecord(payload.record, company, workspaceId);
      onInspect?.({ company, workspaceId, ref: record.entity_id, title: "经营依据", content: <div className={styles.recordDetail}><h3>{record.data.title}</h3><p className={styles.opMeta}>版本 {record.data.revision} · {record.created_at}</p><p className={styles.recordBody}>{record.data.body}</p>{record.data.source_note && <p>来源：{record.data.source_note}</p>}<details><summary>追溯来源</summary><p>{record.entity_id}</p></details></div> });
    } catch (reason) { if (live(token)) setError(reason.message); }
  };
  const scopedViewHref = (view) => {
    const href = writingViewHref(workspaceId, view);
    return selectedBook ? `${href}${view ? "&" : "?"}${new URLSearchParams({ writing_mode: "books", book_ref: selectedBook.ref })}` : href;
  };
  const workHref = (book) => `${writingViewHref(workspaceId, "")}?${new URLSearchParams({ writing_mode: "books", book_ref: book })}`;
  if (readyKey !== surface.key) return <div className={styles.opView}><p className={styles.opHint}>正在读取当前工作空间…</p>{error && <p className={styles.error} role="alert">{error}</p>}</div>;
  if (error) {
  return (
      <div className={styles.opView}>
        <Header workspaceId={workspaceId} />
        <p className={styles.error} role="alert">{error}</p>
      </div>
    );
  }
  if (!view) return <div className={styles.opView}><Header workspaceId={workspaceId} /><p className={styles.opHint}>正在读取经营投影…</p></div>;

  return (
    <div className={styles.opView}>
      <Header workspaceId={workspaceId} />
      <div className={styles.operatingHero}><div><span className={styles.badge}>当前创作</span><h2>从作品与依据，安排下一步</h2><p>先继续正在写的章节，再查看方向、市场记录和经验。</p></div><span className={styles.opBadge}>平台数据未连接</span></div>
      <div className={styles.factStrip}>{[[view.books.length, "部作品"], [view.chapters.length, "个章节"], [view.chapters.filter((item) => item.has_draft).length, "章已保存草稿"], [view.directions.current.filter((item) => item.confirmed).length, "项已确认方向"]].map(([value, label]) => <div key={label}><strong>{value}</strong><span>{label}</span></div>)}</div>

      <section className={styles.opSection}>
        <h3>正在写什么（{view.books.length} 部作品 · {view.chapters.length} 个章节）</h3>
        {!view.books.length && <p className={styles.notice}>还没有作品。先在作品库创建作品与章节。</p>}
        <div className={styles.opList}>
          {view.books.map((b) => (
            <div key={b.ref} className={styles.opCard}>
              <div className={styles.opRow}><Link className={styles.recordTitle} href={workHref(b.ref)}>{b.title}</Link><Link href={workHref(b.ref)}>进入作品 →</Link></div>
              <p className={styles.opMeta}>{b.chapter_count} 个章节</p>
              {view.chapters.filter((c) => c.book_ref === b.ref).map((c) => (
                <Link key={c.ref} className={styles.overviewChapter} href={chapterHref(workspaceId, { book: b.ref, chapter: c.ref })}>
                  <span className={styles.opBadge}>{c.has_draft ? "已有草稿" : "尚无草稿"}</span>
                  {c.title}<span>继续正文 →</span>
                </Link>
              ))}
            </div>
          ))}
        </div>
      </section>

      <section className={styles.opSection}>
        <div className={styles.opBlockHead}>
          <h3>当前方向（{view.directions.current.length}）</h3>
          <Link href={scopedViewHref("directions")}>前往创作方向 →</Link>
        </div>
        {!view.directions.current.length && <p className={styles.notice}>还没有创作方向。方向保存并确认后会在此显示当前版本。</p>}
        <div className={styles.opList}>
          {view.directions.current.map((d) => (
            <div key={d.ref} className={styles.opCard}>
              <div className={styles.opRow}>
                <span className={styles.opBadge}>{d.confirmed ? "已确认" : "待确认"}</span>
                <button className={styles.recordTitle} onClick={() => inspect("direction", d)}>{d.title}</button>
              </div>
              <p className={styles.opMeta}>{scopeLabel(d.scope_ref)} · 版本 {d.revision}</p>
            </div>
          ))}
        </div>
      </section>

      <section className={styles.opSection}>
        <div className={styles.opBlockHead}>
          <h3>积累的经验（当前 {view.learnings.current.length} · 历史版本 {view.learnings.total_versions}）</h3>
          <Link href={scopedViewHref("learning")}>前往经验学习 →</Link>
        </div>
        {!view.learnings.current.length && <p className={styles.notice}>还没有写作经验。已接受的经验当前版本会在此显示。</p>}
        <div className={styles.opList}>
          {view.learnings.current.map((l) => (
            <div key={l.ref} className={styles.opCard}>
              <div className={styles.opRow}>
                <span className={styles.opBadge}>{l.accepted ? "已接受 · 未验证" : "待接受 · 未验证"}</span>
                <button className={styles.recordTitle} onClick={() => inspect("learning", l)}>{l.title}</button>
              </div>
              {l.applicability && <p className={styles.opMeta}>{l.applicability}</p>}
            </div>
          ))}
        </div>
      </section>

      <section className={styles.opSection}>
        <div className={styles.opBlockHead}>
          <h3>最新市场快照（共 {view.snapshots.total} 条，显示最近 {view.snapshots.latest.length}）</h3>
          <Link href={scopedViewHref("market")}>前往市场快照 →</Link>
        </div>
        {!view.snapshots.total && <p className={styles.notice}>还没有市场快照。市场信号全部由你人工录入，系统不自动采集。</p>}
        <div className={styles.opList}>
          {view.snapshots.latest.map((s) => (
            <div key={s.ref} className={styles.opCard}>
              <div className={styles.opRow}>
                <span className={styles.opBadge}>人工录入 · 未验证</span>
                <button className={styles.recordTitle} onClick={() => inspect("snapshot", s)}>{s.title}</button>
              </div>
              <p className={styles.opMeta}>{s.period || "未填周期"}</p>
            </div>
          ))}
        </div>
      </section>

      <section className={styles.opSection}>
        <div className={styles.opBlockHead}>
          <h3>最新表现观察（共 {view.observations.total} 条，显示最近 {view.observations.latest.length}）</h3>
          <Link href={scopedViewHref("performance")}>前往表现观察 →</Link>
        </div>
        <p className={styles.notice} role="note">外部平台读者/阅读数据：<strong>未连接</strong>（平台凭证链属后续阶段）。以下仅为人工观察。</p>
        {!view.observations.total && <p className={styles.notice}>还没有表现观察。</p>}
        <div className={styles.opList}>
          {view.observations.latest.map((o) => (
            <div key={o.ref} className={styles.opCard}>
              <div className={styles.opRow}>
                <span className={styles.opBadge}>人工录入 · 未验证</span>
                <button className={styles.recordTitle} onClick={() => inspect("observation", o)}>{o.title}</button>
              </div>
              <p className={styles.opMeta}>{scopeLabel(o.scope_ref)} · {o.period || "未填周期"}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

function Header({ workspaceId }) {
  return (
    <div className={styles.opHead}>
      <div>
        <p className={styles.eyebrow}>写作工作空间</p>
        <h2>经营</h2>
        <p className={styles.opHint}>方向是什么 / 正在写什么 / 积累了什么经验 / 最新信号</p>
      </div>
      <div className={styles.opActions}>
        <Link href={writingViewHref(workspaceId, "")}>← 作品库</Link>
      </div>
    </div>
  );
}
