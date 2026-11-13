"use client";
import { useCallback, useEffect, useLayoutEffect, useRef, useState } from "react";
import Link from "next/link";
import EmployeeConversation from "../v1/EmployeeConversation.js";
import { useRouter, useSearchParams } from "next/navigation";
import { CEO_ID } from "../../lib/api.js";
import { createInstalledWorkspaceObject } from "../../lib/workspacePackageApi.js";
import { writingRepairHref, writingApi } from "../../lib/writingApi.js";
import { chapterHref, isWritingPackage, sameChapter, writingEntry, writingRequest, writingSessionKey } from "../../lib/writingState.mjs";
import WorkspacePaneShell from "../workspace/WorkspacePaneShell.js";
import WritingBookMain from "./WritingBookMain.js";
import { writingBookHref, BOOK_SECTIONS, BOOK_KINDS } from "../../lib/writingBookState.mjs";
import WritingChapterMain from "./WritingChapterMain.js";
import WritingPublishingMain from "./WritingPublishingMain.js";
import WritingDirection from "./WritingDirection.js";
import WritingLearning from "./WritingLearning.js";
import WritingMarket from "./WritingMarket.js";
import WritingPerformance from "./WritingPerformance.js";
import WritingOverview from "./WritingOverview.js";
import { writingViewHref } from "../../lib/writingState.mjs";
import { validateWritingSurfaceRecord } from "./useWritingSurface.js";
import styles from "./Writing.module.css";

const bookHref = (workspace, book) => `${writingViewHref(workspace, "")}?${new URLSearchParams({ writing_mode: "books", book_ref: book })}`;
const bookStatus = (status) => ({ DRAFT: "草稿", ARCHIVED: "已归档" })[status] || "状态未提供";

const WRITING_SURFACES = {
  overview: { title: "经营", description: "查看当前作品、依据与待确认方向，安排下一步。" },
  market: { title: "市场与方向", description: "记录人工来源与观察，保留尚未核验的市场依据。" },
  directions: { title: "作品方向", description: "选择适用范围与引用依据，明确确认后再应用到章节。" },
  performance: { title: "读者与收益", description: "查看人工反馈记录；平台读者与收益数据尚未连接。" },
  learning: { title: "写作经验", description: "保存用途、原依据与限制，明确选择后应用到新章节。" },
};

export default function WritingWorkspace({ detail, workspaceId }) {
  const router = useRouter(); const params = useSearchParams(); const entry = writingEntry(params);
  const company = detail.instance?.company_id; const epoch = useRef(0);
  const [collectionState, setCollection] = useState(null); const [chapterState, setChapter] = useState(null);
  const collection = collectionState?.scope?.company_id === company && collectionState?.scope?.workspace_id === workspaceId ? collectionState : null;
  // Navigation renders before the load effect clears the previous chapter.
  const chapter = !entry.error && entry.mode !== "books" && sameChapter(chapterState?.scope, company, workspaceId, entry) ? chapterState : null;
  const [error, setError] = useState(""); const [busy, setBusy] = useState(false);
  const [metadataRead, setEntryMetadata] = useState(null); const [picker, setPicker] = useState(false); const [holder, setHolder] = useState("");
  const entryMetadata = metadataRead?.scope?.company_id === company && metadataRead?.scope?.workspace_id === workspaceId ? metadataRead : null;
  const executionLock = useRef(false); const [localRequestLocked, setLocalRequestLocked] = useState(false);
  const lockedRequest = localRequestLocked || Boolean(entryMetadata?.pending.length);
  const lockKey = `curis.writing.pending.${company}:${workspaceId}`;
  const setExecutionLock = (value) => { executionLock.current = value; setLocalRequestLocked(value); try { sessionStorage.setItem(lockKey, JSON.stringify(value)); } catch {} };
  useEffect(() => { try { const value = JSON.parse(sessionStorage.getItem(lockKey) || "false"); executionLock.current = value; setLocalRequestLocked(value); } catch {} }, [lockKey]);
  const [bookTitle, setBookTitle] = useState(""); const [bookTitleError, setBookTitleError] = useState(""); const [chapterTitles, setChapterTitles] = useState({});
  const [query, setQuery] = useState(""); const [statusFilter, setStatusFilter] = useState("");
  const [newBookOpen, setNewBookOpen] = useState(false);
  const creationKey=`curis.writing.creation-unknown.${company}:${workspaceId}`;
  const [creationUnknown,setCreationUnknown]=useState(false);
  useEffect(()=>{try{setCreationUnknown(Boolean(sessionStorage.getItem(creationKey)));}catch{}},[creationKey]);
  const [recordPanel, setRecordPanel] = useState(null);
  const [detailRequest, setDetailRequest] = useState({ key: 0, tab: "responsibility" });
  const openDetail = (tab) => setDetailRequest((current) => ({ key: current.key + 1, tab }));
  useEffect(() => {
    setQuery(""); setStatusFilter(""); setNewBookOpen(false); setBookTitle(""); setBookTitleError(""); setChapterTitles({}); setPicker(false); setRecordPanel(null);
  }, [company, workspaceId]);
  const entryKey = JSON.stringify([company, workspaceId, entry.mode, entry.book, entry.chapter]);
  const activeKey = useRef(entryKey); const pendingKey = useRef("");
  useLayoutEffect(() => { activeKey.current = entryKey; if (pendingKey.current !== entryKey) { pendingKey.current = ""; setBusy(false); } }, [entryKey]);
  const load = useCallback(async () => {
    const generation = ++epoch.current; const key = entryKey;
    try {
      if (!isWritingPackage(detail) || !company || entry.error) throw new Error(entry.error || "写作工作空间来源不可验证。");
      const [next, metadata] = await Promise.all([writingApi.collection(company, workspaceId), writingApi.entry(company, workspaceId)]);
      if (next.scope.company_id !== company || next.scope.workspace_id !== workspaceId) throw new Error("作品库来源不匹配。");
      if (metadata.scope?.company_id !== company || metadata.scope?.workspace_id !== workspaceId) throw new Error("当前责任来源不匹配。");
      if (entry.book && !next.books.some((book) => book.ref === entry.book)) throw new Error("当前作品不存在于这个工作空间，请返回作品库。");
      let state = null;
      if (entry.mode !== "books") {
        state = await writingApi.chapter(company, workspaceId, entry);
        if (!sameChapter(state.scope, company, workspaceId, entry)) throw new Error("章节来源不匹配。");
        if (entry.draft && state.draft.ref !== entry.draft && !state.events.some((e) => e.draft?.ref === entry.draft)) throw new Error("来源正文版本不存在。");
      }
      if (generation !== epoch.current || key !== activeKey.current) return;
      setCollection(next); setChapter(state); setEntryMetadata(metadata); setError("");
    } catch (reason) { if (generation === epoch.current && key === activeKey.current) { setError(reason.message); setChapter(null); } }
  // Stable identities guard late reads when navigating between books/chapters.
  }, [company, workspaceId, entryKey, detail]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { setCollection(null); setChapter(null); load(); return () => { epoch.current += 1; }; }, [load]);
  const command = async (action, data, requestId, expectedDraftRef) => {
    if (!chapter || pendingKey.current === entryKey) throw new Error("请等待当前章节读取完成。");
    const key = entryKey; pendingKey.current = key; setBusy(true);
    try {
      const storageKey = writingSessionKey(chapter.scope) + ".request." + action;
      let previous = null;
      try { previous = JSON.parse(sessionStorage.getItem(storageKey) || "null"); } catch {}
      const request = await writingRequest(previous, action, expectedDraftRef || chapter.draft.ref, data, () => requestId || crypto.randomUUID());
      if (key !== activeKey.current) throw new Error("章节已切换；没有发送原章节操作。");
      try { sessionStorage.setItem(storageKey, JSON.stringify(request)); } catch {}
      const payload = { request_id: request.request_id, expected_draft_ref: expectedDraftRef || chapter.draft.ref, data };
      const output = action === "discussion.start" ? await writingApi.bind(company, workspaceId, entry, payload) : await writingApi.command(company, workspaceId, entry, action, payload);
      if (key !== activeKey.current) throw new Error("章节已切换；请从原章节读取操作记录。");
      await load(); return output;
    } catch (reason) { if (key === activeKey.current) setError(reason.message); throw reason; } finally { if (key === activeKey.current) { pendingKey.current = ""; setBusy(false); } }
  };
  const create = async (kind, title, book) => {
    if (pendingKey.current === entryKey) return;
    if (creationUnknown || sessionStorage.getItem(creationKey)) { setError("原创建结果未知，不能再次创建。请读取作品与章节清单，核对原结果。"); return; }
    if (!title.trim()) { if (kind === "WritingBook") setBookTitleError("请填写作品名称。"); else setError("请填写章节标题。"); document.querySelector(kind === "WritingBook" ? "[aria-label=作品名称]" : `[data-chapter-input="${book}"]`)?.focus(); return; }
    if (kind === "WritingBook") setBookTitleError("");
    const key = entryKey; pendingKey.current = key; setBusy(true);
    try {
      if (kind === "WritingChapter" && !collection.books.some((b) => b.ref === book)) throw new Error("请先选择当前作品。");
      const created = await createInstalledWorkspaceObject(workspaceId, "core.domain-object.create", { ceo_id: CEO_ID, object_type: kind, data: { title, status: "DRAFT", ...(book ? { bookRef: book } : {}) } });
      if (!created?.object_id) throw new Error("创建响应缺少明确对象，结果未知。");
      if (key === activeKey.current) {
        setError("");
        if (kind === "WritingBook") { setBookTitle(""); setNewBookOpen(false); router.push(writingBookHref(workspaceId, created.object_id, { section: "setup" })); }
        else { setChapterTitles((current) => ({ ...current, [book]: "" })); router.push(chapterHref(workspaceId, { book, chapter: created.object_id })); }
      }
    } catch (reason) { if ([400,401,403,404,409,422].includes(reason.status)) {if(key===activeKey.current)setError(reason.message);return;} try {sessionStorage.setItem(creationKey,JSON.stringify({kind,title,book:book||""}));}catch{} if (key === activeKey.current) {setCreationUnknown(true);setError(reason.message+" 原创建结果未确定，请读取清单核对；不会重复发送创建。");} } finally { if (key === activeKey.current) { pendingKey.current = ""; setBusy(false); } }
  };
  const assign = async () => {
    if (executionLock.current || entryMetadata?.pending.length || busy) return;
    if (!holder) { setError("请选择当前公司的责任员工。"); return; }
    setBusy(true);
    try { await writingApi.assign(company, workspaceId, { employee_id: holder, expected_revision: entryMetadata.assignment_revision }); setPicker(false); await load(); }
    catch (reason) { setError(reason.message); } finally { setBusy(false); }
  };
  const book = collection?.books.find((b) => b.ref === entry.book);
  const selected = collection?.chapters.find((c) => c.ref === entry.chapter && c.bookRef === entry.book);
  const inspectRecord = useCallback((descriptor, { open = true } = {}) => {
    const active = JSON.parse(activeKey.current);
    if (descriptor.company !== company || descriptor.workspaceId !== workspaceId || active[0] !== company || active[1] !== workspaceId || active[3] !== entry.book) return;
    setRecordPanel({ ...descriptor, objectKey: entry.book }); if (open) setDetailRequest((current) => ({ key: current.key + 1, tab: "operating:" + descriptor.ref }));
  }, [company, workspaceId, entry.book, setRecordPanel, setDetailRequest]);
  const readOriginalLearning = async () => {
    const source = chapter?.creation_source;
    if (source?.status !== "AVAILABLE") return;
    const key = entryKey;
    try {
      const payload = await writingApi.learning(company, workspaceId, source.learning_ref);
      if (key !== activeKey.current) return;
      const record = validateWritingSurfaceRecord(payload.record, company, workspaceId);
      if (record.entity_id !== source.learning_ref || record.data.revision !== source.revision || record.data.payload_sha256 !== source.payload_sha256) throw new Error("原经验版本已无法核对。");
      inspectRecord({ company, workspaceId, ref: record.entity_id, title: "来源经验", content: <div className={styles.recordDetail}><h3>{record.data.title}</h3><p>原版本 {record.data.revision} · 未验证</p><p className={styles.recordBody}>{record.data.body}</p><h4>适用范围与限制</h4><p>{record.data.applicability}</p><p>{record.data.counterexample}</p><details><summary>来源标识</summary><p>{record.entity_id}</p><p>{record.data.payload_sha256}</p></details></div> });
    } catch (reason) { if (key === activeKey.current) setError(reason.message); }
  };
  const surfaceHref = (view) => {
    const href = writingViewHref(workspaceId, view);
    return entry.book ? `${href}${view ? "&" : "?"}${new URLSearchParams({ writing_mode: "books", book_ref: entry.book })}` : href;
  };
  const operatingSurface = WRITING_SURFACES[entry.view];
  const authorSurface = entry.mode === "review" ? { title: "作者检查", description: "检查当前保存版本，再独立明确确认正式稿。" } : entry.mode === "package" ? { title: "正式稿与本地交付", description: "选择作者确认的正文快照，准备未上线的本地包。" } : null;
  const currentSurface = operatingSurface || authorSurface;
  const pageTitle = currentSurface?.title || selected?.title || book?.title || "作品";
  const pageDescription = currentSurface?.description || (book ? "围绕这部作品组织章节，继续正文创作。" : "管理作品与章节，继续你的创作。");
  const bookChapters = collection?.chapters.filter((item) => item.bookRef === book?.ref) || [];
  const visibleBooks = collection?.books.filter((item) => item.title.toLowerCase().includes(query.trim().toLowerCase())
    && (!statusFilter || item.status === statusFilter)) || [];
  const employeeReturn = entry.mode === "books" ? entry.view ? surfaceHref(entry.view) : book ? writingBookHref(workspaceId, book.ref, entry.bookPosition) : writingViewHref(workspaceId, "") : chapterHref(workspaceId, entry);
  const context = <div className={styles.context}>
    <p className={styles.contextTitle}>写作</p>
    <nav className={styles.opNav} aria-label="写作经营面">
      {[["overview", "经营"], ["market", "市场与方向"], ["", "作品"], ["performance", "读者与收益"], ["learning", "写作经验"]].map(([view, label]) => <Link key={view} href={surfaceHref(view)} aria-current={entry.view === view ? "page" : undefined}>{label}</Link>)}
    </nav>
    {selected && <Link href={chapterHref(workspaceId, { ...entry, mode: "package" })}>正式稿与本地交付</Link>}
    {book ? <><div className={styles.selectedBook}><div><h3>{book.title}</h3><span className={styles.badge}>{bookStatus(book.status)}</span><p>{bookChapters.length} 个章节</p></div></div>
      <Link href={bookHref(workspaceId, book.ref)} aria-current={!entry.view && entry.mode === "books" ? "page" : undefined}>作品工作台</Link>
      <Link href={surfaceHref("directions")} aria-current={entry.view === "directions" ? "page" : undefined}>作品方向</Link>
      {Object.entries(BOOK_SECTIONS).map(([section,title]) => <Link key={section} href={writingBookHref(workspaceId, book.ref, { section })} aria-current={!entry.view && entry.mode === "books" && entry.bookPosition?.section === section ? "page" : undefined}>{title}</Link>)}
      <section className={styles.chapterTree}><h3>章节目录 <span>{bookChapters.length}</span></h3>{bookChapters.map((item, index) => <Link key={item.ref} href={chapterHref(workspaceId, { book: book.ref, chapter: item.ref })} aria-current={entry.chapter === item.ref ? "page" : undefined}><span>{index + 1}</span>{item.title}</Link>)}{!bookChapters.length && <p>还没有章节。在作品工作台添加第一章。</p>}</section>
    </> : <section><h3>作品目录</h3>{collection?.books.map((item) => <Link key={item.ref} href={bookHref(workspaceId, item.ref)}>{item.title}</Link>)}{collection?.books.length === 0 && <p>新作品会出现在这里。</p>}</section>}
  </div>;
  const pinnedBasis = chapter?.draft.book_context_basis;
  const basisGroups = [["结构与故事节点", ["outline","volume","chapter","node"]], ["人物", ["character"]], ["人物关系", ["relationship"]], ["世界设定", ["world"]]];
  const utilityTabs = [
    { id: "responsibility", title: "当前责任", content: <div className={styles.context}>
      <h3>{entryMetadata?.employee_name || "章节作者待明确"}</h3><p>章节创作责任；本地编辑可以继续。</p><p>{chapter?.responsibility.reason || collection?.responsibility.reason}</p>
      {entryMetadata?.company_employee_ref && <Link href={writingRepairHref(`/ceo-office/organization/employees/${encodeURIComponent(entryMetadata.company_employee_ref)}`, employeeReturn)}>查看员工详情</Link>}
      {entryMetadata && <><button disabled={busy || lockedRequest || Boolean(entryMetadata.pending.length) || collection?.read_only} onClick={() => { if (!executionLock.current) { setPicker(!picker); setHolder(""); } }}>{picker ? "收起选择" : "更换责任员工"}</button>
      {picker && <fieldset disabled={busy || lockedRequest}><legend>选择当前公司的员工</legend>{entryMetadata.employees.map((employee) => <label className={styles.check} key={employee.id}><input type="radio" name="writing-holder" value={employee.id} checked={holder === employee.id} onChange={() => { if (!executionLock.current) setHolder(employee.id); }} />{employee.name} · {employee.role}</label>)}{!entryMetadata.employees.length && <p>暂无可承担责任的员工。</p>}<button disabled={!holder} onClick={assign}>确认责任员工</button><button onClick={() => setPicker(false)}>取消，保留当前责任</button></fieldset>}</>}
      {lockedRequest && <p role="status">原请求待核验，请先从原章节查询结果。</p>}
    </div> },
    { id: "basis", title: "本章依据", content: <div className={styles.context}><h3>{selected?.title || book?.title || "当前作品"}</h3>{chapter ? <><p>正文依据：{chapter.draft.ref === "ABSENT" ? "尚未保存正文" : "当前保存版本"}</p>{chapter.draft.book_context_basis && <><h4>作品结构原版本依据</h4><p>{chapter.book_context_status?.reason}</p>{basisGroups.map(([title,kinds]) => {
        const items = pinnedBasis.items.filter(item=>kinds.includes(item.kind));
        const structural = kinds.includes("node");
        const parents = new Set(items.map(item=>item.parent).filter(Boolean));
        const primary = structural ? items.filter(item=>["chapter","node"].includes(item.kind)&&!parents.has(item.id)) : items;
        const ancestors = structural ? items.filter(item=>!primary.includes(item)) : [];
        const originalHref = item => writingBookHref(workspaceId, book.ref, {section:item.kind === "world" ? "world" : ["character","relationship"].includes(item.kind) ? "characters" : "outline", item:item.id, context:pinnedBasis.context_ref});
        return items.length ? <section key={title} className={styles.basisGroup}><h4>{title}</h4>
          {ancestors.length > 0 && <nav className={styles.basisAncestors} aria-label="原版本结构条目">{ancestors.map(item=><Link key={item.id} href={originalHref(item)}>{BOOK_KINDS[item.kind]} · {item.title} →</Link>)}</nav>}
          {primary.map(item => {
            const core = (structural ? [["叙事目的",item.goal || "原快照未提供叙事目的"]]
              : item.kind === "character" ? [["角色",item.role],["当前知情 / 边界",item.knowledge],["人物说明",item.body]]
              : item.kind === "world" ? [["类别",item.category],["世界规则",item.body]]
              : [["关系说明",item.body]]).filter(([,value])=>value);
            const secondary = [...(!structural ? [["戏剧目的",item.goal]] : [["详细内容",item.body]]),
              ...(item.kind === "chapter" ? [["上一章交接",item.handoff]] : []), ["状态",item.status]].filter(([,value])=>value);
            return <article key={item.id} className={styles.basisItem} data-basis-primary={structural || undefined}><h5><Link href={originalHref(item)}>{BOOK_KINDS[item.kind]} · {item.title} →</Link></h5>
              {item.kind === "relationship" && <p>关系方向：{[item.from_character,item.to_character].map(ref=>pinnedBasis.items.find(value=>value.id===ref&&value.kind==="character")?.title || "原快照缺少该端点人物").join(" → ")}</p>}
              {core.map(([label,value])=><p key={label}><strong>{label}：</strong>{value}</p>)}
              {!core.length && <p>原快照未提供{item.kind === "character" ? "人物说明" : item.kind === "world" ? "世界规则" : "关系说明"}。</p>}
              {secondary.length > 0 && <details className={styles.basisSecondary}><summary>更多原版本字段</summary><dl>{secondary.map(([label,value])=><div key={label}><dt>{label}</dt><dd>{value}</dd></div>)}</dl></details>}
            </article>;
          })}</section> : null;
      })}{chapter.draft.book_context_basis.directions.map(direction=><section key={direction.ref}><h4>{direction.title} · 原方向版本 {direction.revision}</h4><p>{direction.body}</p></section>)}<Link href={chapterHref(workspaceId,entry)}>返回本章与原选段</Link></>}{chapter.draft.knowledge.length ? chapter.draft.knowledge.map((item, index) => <section key={item.ref || index}><h4>{item.title || item.name || `引用资料 ${index + 1}`}</h4><p>{item.excerpt || item.description || "已记录在当前正文依据中。"}</p><details><summary>来源标识</summary><p>{item.ref || item.reference_id || "来源未提供"}</p></details></section>) : <p>当前正文尚未引用资料。</p>}{chapter.creation_source?.status === "AVAILABLE" && <section><h4>创建来源经验</h4><p>{chapter.creation_source.title} · 原版本 {chapter.creation_source.revision}</p><p>人工经验 · 未验证；后续修订不会替换这个来源。</p><button onClick={readOriginalLearning}>查看原经验版本</button></section>}{["MISSING", "AMBIGUOUS"].includes(chapter.creation_source?.status) && <p role="status">创建来源暂无法唯一核对，请保留原章节。</p>}<p>作者检查针对当前保存版本；独立审核尚未提供。</p></> : <p>选择真实章节后，查看它的正文与引用依据。</p>}</div> },
    { id: "versions", title: "版本记录", content: <div className={styles.context}><h3>章节版本记录</h3>{chapter?.events.length ? [...chapter.events].reverse().map((event) => <details key={event.ref}><summary>{({ "draft.saved": "保存草稿", "inspection.recorded": "作者人工检查", "formal.confirmed": "作者确认正式稿", "package.prepared": "准备本地发布包", "candidate.recorded": "记录修改建议", "candidate.adopted": "采用修改建议", "discussion.bound": "绑定章节讨论" })[event.action] || "章节工作记录"} · {event.created_at}</summary>{event.draft && <pre>{event.draft.text}</pre>}{event.snapshot && <p>正式稿快照独立保留。</p>}<p className={styles.trace}>{event.ref}</p></details>) : <p>当前章节还没有保存的版本记录。</p>}<p>草稿、作者确认的正式稿与发布包分别保存。本地发布包未发布到平台。</p></div> },
  ];
  const scopedPanel = recordPanel?.company === company && recordPanel?.workspaceId === workspaceId && recordPanel?.objectKey === entry.book ? recordPanel : null;
  if (scopedPanel) utilityTabs.push({ id: "operating:" + scopedPanel.ref, title: scopedPanel.title, content: scopedPanel.content });
  const orderedTabs = chapter ? [utilityTabs[1], utilityTabs[2], utilityTabs[0], ...utilityTabs.slice(3)] : utilityTabs;
  return <WorkspacePaneShell workspaceId={workspaceId} surfaceId="writing" breadcrumb={<span>写作 / {currentSurface?.title || (book ? "作品工作台" : "作品库")}{book ? ` / ${book.title}` : ""}{selected ? ` / ${selected.title}` : ""}</span>} contextPane={context} utilityTabs={orderedTabs} utilityRequestKey={detailRequest.key} utilityRequestTabId={detailRequest.tab} contextAvailable utilityAvailable initialContextOpen initialUtilityOpen={false} contextLabel="作品与章节" utilityLabel="辅助内容">
    <div className={styles.workspace} data-writing-workspace={workspaceId}>
      <header className={styles.header}><div><h1>{pageTitle}</h1>{(!selected || currentSurface) && <p className={styles.subtitle}>{pageDescription}</p>}{currentSurface && book && <Link className={styles.scopeChip} href={bookHref(workspaceId, book.ref)}>当前作品 · {book.title}{selected ? ` / ${selected.title}` : ""}</Link>}</div><div className={styles.headerActions}>{(book || entry.view) && <Link href={writingViewHref(workspaceId, "")}>返回作品库</Link>}<button onClick={load} disabled={busy}>重新读取</button>{!entry.view && !book && collection && <button className={styles.primary} onClick={() => setNewBookOpen(!newBookOpen)} disabled={busy || collection.read_only}>＋ 新建作品</button>}</div></header>
      {entryMetadata?.employee_ref && entryMetadata?.employee_name && (!chapter || entry.mode === "package") && <EmployeeConversation key={`${company}:${workspaceId}:${book?.ref || "workspace"}:${entryMetadata.employee_ref}`} companyId={company} employee={{ employee_ref: entryMetadata.employee_ref, id: entryMetadata.company_employee_ref, name: entryMetadata.employee_name }} blocked={Boolean(busy || lockedRequest)} embedded={{ workspaceId, contextKey: book?.ref ? `book:${book.ref}` : "workspace", assignmentRef: entryMetadata.assignment_ref, objectRef: book?.ref || null, title: book?.title ? `讨论《${book.title}》` : "写作工作空间讨论", showBar: true }} businessReturn={{ href: book ? bookHref(workspaceId, book.ref) : writingViewHref(workspaceId, ""), kind: "writing" }} />}

      {creationUnknown&&<p role="status" className={styles.notice}>原创建结果待核对。<button onClick={()=>load()}>读取已保存作品与章节</button>请从清单打开原对象；创建保持锁定。</p>}
      {error && <p role="alert" className={styles.error}>{error} 输入已保留，请核对来源后重试。</p>}
      {!collection && !error && <p className={styles.notice}>正在读取作品与章节…</p>}
      {collection && entry.mode === "books" && !entry.view && !book && <>
        {newBookOpen && <form className={styles.create} onSubmit={(event) => { event.preventDefault(); create("WritingBook", bookTitle); }}><label>作品名称<input autoFocus aria-label="作品名称" aria-invalid={Boolean(bookTitleError)} aria-describedby={bookTitleError ? "writing-book-title-error" : undefined} value={bookTitle} maxLength={160} onChange={(event) => { setBookTitle(event.target.value); setBookTitleError(""); }} /></label>{bookTitleError && <p id="writing-book-title-error" role="alert" className={styles.error}>{bookTitleError}</p>}<button className={styles.primary} disabled={busy || creationUnknown || collection.read_only}>创建作品</button><button type="button" onClick={() => { setNewBookOpen(false); setBookTitleError(""); }}>取消</button></form>}
        <div className={styles.collectionTools}><input type="search" aria-label="搜索作品" placeholder="搜索作品名称" value={query} onChange={(event) => setQuery(event.target.value)} /><select aria-label="作品状态" value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)}><option value="">全部状态</option><option value="DRAFT">草稿</option><option value="ARCHIVED">已归档</option></select><span>{visibleBooks.length} 部作品</span></div>
        <div className={styles.books}>{visibleBooks.map((item) => { const chapters = collection.chapters.filter((chapter) => chapter.bookRef === item.ref); return <article key={item.ref} className={styles.bookCard}><div className={styles.bookCover} aria-label={`作品封面占位 · ${item.title}`}><small>写作作品</small><strong>{item.title}</strong><span>CURIS</span></div><div className={styles.bookCardBody}><h2>{item.title}</h2><span className={styles.badge}>{bookStatus(item.status)}</span><dl><div><dt>章节</dt><dd>{chapters.length} 个</dd></div><div><dt>当前工作</dt><dd>{chapters.length ? "继续章节正文" : "准备第一章"}</dd></div><div><dt>平台发布</dt><dd>未连接</dd></div></dl><Link className={styles.bookDoor} href={bookHref(workspaceId, item.ref)}>进入作品 →</Link></div></article>; })}</div>
        {!visibleBooks.length && <section className={styles.libraryEmpty}><div className={styles.emptyBook} aria-hidden="true">你的<br />下一部作品</div><div><h2>{collection.books.length ? "没有符合筛选的作品" : "从一个故事开始"}</h2><p>{collection.books.length ? "调整名称或状态，查看已保存的作品。" : "建立作品，再为它添加章节。正文会保存在当前工作空间中。"}</p>{!collection.books.length && <button className={styles.primary} disabled={collection.read_only} onClick={() => setNewBookOpen(true)}>新建第一部作品</button>}</div></section>}
      </>}
      {collection && book && entry.mode === "books" && !entry.view && <WritingBookMain key={`${company}:${workspaceId}:${book.ref}`} company={company} workspaceId={workspaceId} book={book} locator={entry.bookPosition} onInspect={inspectRecord} onCreateChapter={title=>create("WritingChapter",title,book.ref)} requestLocked={lockedRequest||creationUnknown||busy} readOnly={collection.read_only} />}
      {collection && entry.mode === "books" && entry.view === "directions" && <WritingDirection key={`${company}:${workspaceId}:${entry.view}:${entry.book}`} company={company} workspaceId={workspaceId} selectedBook={book || null} onInspect={inspectRecord} />}
      {collection && entry.mode === "books" && entry.view === "learning" && <WritingLearning key={`${company}:${workspaceId}:${entry.view}:${entry.book}`} company={company} workspaceId={workspaceId} selectedBook={book || null} onInspect={inspectRecord} onNavigate={(next) => router.push(chapterHref(workspaceId, next))} />}
      {collection && entry.mode === "books" && entry.view === "market" && <WritingMarket key={`${company}:${workspaceId}:${entry.view}:${entry.book}`} company={company} workspaceId={workspaceId} selectedBook={book || null} onInspect={inspectRecord} />}
      {collection && entry.mode === "books" && entry.view === "performance" && <WritingPerformance key={`${company}:${workspaceId}:${entry.view}:${entry.book}`} company={company} workspaceId={workspaceId} selectedBook={book || null} onInspect={inspectRecord} />}
      {collection && entry.mode === "books" && entry.view === "overview" && <WritingOverview key={`${company}:${workspaceId}:${entry.view}:${entry.book}`} company={company} workspaceId={workspaceId} selectedBook={book || null} onInspect={inspectRecord} />}
      {chapter && book && selected && (entry.mode === "package" ? <WritingPublishingMain key={`${company}:${workspaceId}:${entry.chapter}`} state={chapter} entry={entry} workspaceId={workspaceId} command={command} busy={busy} onNavigate={(next) => router.push(chapterHref(workspaceId, { ...entry, ...next }))} /> : <WritingChapterMain key={`${company}:${workspaceId}:${entry.chapter}`} state={chapter} entry={entry} workspaceId={workspaceId} company={company} command={command} busy={busy} entryMetadata={entryMetadata} onRefresh={load} onDetails={openDetail} onExecutionLock={setExecutionLock} requestLocked={lockedRequest} onNavigate={(next) => router.push(chapterHref(workspaceId, { ...entry, ...next }))} />)}
    </div>
  </WorkspacePaneShell>;
}
