"use client";
import { useEffect, useLayoutEffect, useRef, useState } from "react";
import Link from "next/link";
import { writingApi } from "../../lib/writingApi.js";
import { writingRequest, chapterHref } from "../../lib/writingState.mjs";
import { BOOK_SECTIONS, BOOK_KINDS, writingBookHref, bookItemDepth, orderedBookItems } from "../../lib/writingBookState.mjs";
import styles from "./Writing.module.css";

const blankItem = kind => ({ id: crypto.randomUUID(), kind, title: "", body: "", goal: "", order: 0, parent: "", status: "未开始", chapter_ref: "", category: "", role: "", knowledge: "", from_character: "", to_character: "", handoff: "", character_refs: [], world_refs: [], direction_refs: [] });
export default function WritingBookMain({ company, workspaceId, book, locator, onInspect, onCreateChapter, requestLocked, readOnly }) {
  const key = `${company}:${workspaceId}:${book.ref}`, draftKey = `curis.book-context.${key}`;
  const viewKey = `${key}:${locator?.context || "current"}`;
  const live = useRef(viewKey), view = useRef(null), generation=useRef(0); useLayoutEffect(()=>{live.current=viewKey;generation.current++;return()=>{live.current="";};},[viewKey]);
  const [state, setState] = useState(null), [context, setContext] = useState(null), [base, setBase] = useState("");
  const [editing, setEditing] = useState(null), [item, setItem] = useState(null), [tab, setTab] = useState("all"), [chapterTitle, setChapterTitle] = useState("");
  const [collapsed, setCollapsed] = useState(new Set()), [directions, setDirections] = useState([]);
  const [error, setError] = useState(""), [notice, setNotice] = useState(""), [busy, setBusy] = useState(false), [dirty, setDirty] = useState(false), [inspectedId, setInspectedId] = useState("");
  const pending = useRef(false), request = useRef(null), openedLocator = useRef("");
  useLayoutEffect(()=>{pending.current=false;request.current=null;setBusy(false);},[viewKey]);
  const section = locator?.section || "outline", selectedId = locator?.item || "";
  useLayoutEffect(()=>{openedLocator.current="";setInspectedId(selectedId);},[selectedId,viewKey]);
  useLayoutEffect(()=>{view.current={key:viewKey,context,recordRef:state?.record?.ref||"",locked:busy||requestLocked||readOnly||state?.read_only||Boolean(locator?.context)||state?.viewKey!==viewKey};},[viewKey,context,state,busy,requestLocked,readOnly,locator?.context]);
  useEffect(() => {
    let active = true; setState(null); setContext(null);
    Promise.all([writingApi.bookContext(company, workspaceId, book.ref, locator?.context || ""), writingApi.directions(company, workspaceId)]).then(([value, directionData]) => {
      if (!active || live.current !== viewKey) return;
      if (value.scope.company_id !== company || value.scope.workspace_id !== workspaceId || value.scope.book_ref !== book.ref) throw new Error("作品结构范围不匹配。");
      setDirections(directionData.records || []);
      setState({...value,viewKey});
      let retained; try { retained = JSON.parse(sessionStorage.getItem(draftKey) || "null"); } catch {}
            if (locator?.context) {
        setContext(value.context); setBase(value.record?.ref || ""); setDirty(false); setItem(null); setEditing(null);
      } else {
        setContext(retained?.context || value.context); setBase(retained?.base ?? value.record?.ref ?? ""); setDirty(Boolean(retained));
        setItem(retained?.item || null); setEditing(retained?.editing ?? null);
      }
    }).catch(reason => { if (active) setError(reason.message); });
    return () => { active = false; };
  }, [company, workspaceId, book.ref, locator?.context, key, draftKey, viewKey]);
  useEffect(() => { if (state?.viewKey===viewKey && context && dirty && !locator?.context) try { sessionStorage.setItem(draftKey, JSON.stringify({ context, base, item, editing })); } catch {} }, [state, context, base, item, editing, dirty, draftKey, locator?.context, viewKey]);
  const change = next => { if (busy || requestLocked || readOnly || state?.read_only || locator?.context) return; setContext(next); setDirty(true); setNotice(""); };
  const save = async (nextContext = context) => {
    if (pending.current || requestLocked || readOnly || state?.read_only || locator?.context) return;
    const ownGeneration=generation.current;
    pending.current = true; setBusy(true); setError("");
    try {
      request.current = await writingRequest(request.current, "book-context.save", base, nextContext, () => crypto.randomUUID());
      const result = await writingApi.saveBookContext(company, workspaceId, book.ref, { request_id: request.current.request_id, expected_ref: base, data: { context: nextContext } });
      if (live.current !== viewKey || generation.current!==ownGeneration) return;
      view.current={...view.current,context:result.context,recordRef:result.ref};
      setBase(result.ref); setContext(result.context); setState(v => ({ ...v, record: result, head_ref: result.ref, context: result.context })); setDirty(false); request.current = null;
      sessionStorage.removeItem(draftKey); setItem(null); setEditing(null); setNotice("作品结构已保存为独立新版本，正文和旧正式稿保持原样。");
    } catch (reason) { if (live.current === viewKey && generation.current===ownGeneration) {
      setError(`${reason.message} 输入已保留，可核对最新版本后重试。`);
      if(reason.status===409) try {const latest=await writingApi.bookContext(company,workspaceId,book.ref);if(live.current===viewKey&&generation.current===ownGeneration&&latest.scope.company_id===company&&latest.scope.workspace_id===workspaceId&&latest.scope.book_ref===book.ref)setState(value=>({...value,head_ref:latest.head_ref}));} catch {}
    } }
    finally { if(live.current===viewKey&&generation.current===ownGeneration){pending.current = false; setBusy(false);} }
  };
  const edit = row => { const active=view.current;if(active?.key!==viewKey)return;if(pending.current||active.locked||active.context!==context||active.recordRef!==(state.record?.ref||"")){setError("这条详情已更新或正在保存，请从当前详情重新编辑；未回填旧内容。");return;} setItem({ ...blankItem(row.kind), ...row }); setEditing(row.id); setDirty(true); };
  const publish = (row, open = false) => onInspect?.({ company, workspaceId, ref: row.id, title: row.title, content: <div className={styles.recordDetail}><h3>{row.title}</h3><p>{BOOK_KINDS[row.kind]} · {row.status || "状态待填写"}</p><p>{row.goal || "叙事目的尚未填写"}</p><p className={styles.recordBody}>{row.body || "详细说明尚未填写"}</p>{row.knowledge && <><h4>当前知情 / 边界</h4><p>{row.knowledge}</p></>}{row.kind === "relationship" && <p>{context.items.find(v=>v.id===row.from_character)?.title} → {context.items.find(v=>v.id===row.to_character)?.title}</p>}<p>{row.category || row.role}</p>{row.handoff && <><h4>上一章交接 · 作者说明</h4><p>{row.handoff}</p></>}{[...(row.character_refs||[]),...(row.world_refs||[]),...(row.kind==="node"?[...(context.items.find(v=>v.id===row.parent)?.character_refs||[]),...(context.items.find(v=>v.id===row.parent)?.world_refs||[])]:[])].filter((v,i,a)=>a.indexOf(v)===i).map(ref=>{const linked=context.items.find(v=>v.id===ref);return linked?<section key={ref}><h4>{linked.title}</h4><p>{linked.body}</p>{linked.knowledge&&<p>当前知情：{linked.knowledge}</p>}<button onClick={()=>inspect(linked)}>查看完整原条目</button></section>:<p key={ref}>原关联条目缺失，未改用其他条目。</p>;})}{(row.direction_refs||[]).map(ref=>{const value=directions.find(v=>v.entity_id===ref);return <section key={ref}><h4>{value?.data.title||"原方向无法核对"}</h4><p>{value?.data.body}</p><p>原版本 {value?.data.revision}</p></section>;})}{selectedId&&selectedId!==row.id&&context.items.some(value=>value.id===selectedId)&&<button onClick={()=>inspect(context.items.find(value=>value.id===selectedId))}>返回原定位条目</button>}<button disabled={busy || requestLocked || readOnly || state.read_only || Boolean(locator?.context)} onClick={() => { edit(row); }}>编辑这条记录</button>{row.kind === "chapter" && <Link href={chapterHref(workspaceId, { book: book.ref, chapter: row.chapter_ref })}>进入本章正文 →</Link>}{row.kind === "node" && context.items.find(v => v.id === row.parent)?.chapter_ref && <Link href={chapterHref(workspaceId, { book: book.ref, chapter: context.items.find(v => v.id === row.parent).chapter_ref })}>进入所属章节正文 →</Link>}{state.record?.context.items.some(v=>v.id===row.id) ? <Link href={writingBookHref(workspaceId, book.ref, { section:row.kind==="world"?"world":["character","relationship"].includes(row.kind)?"characters":"outline", item: row.id, context: state.record.ref })}>此条目的原版本入口</Link> : <p>这条输入尚未保存，还没有可返回的原版本入口。</p>}</div> }, { open });
  const inspect = row => {if(state?.viewKey!==viewKey||live.current!==viewKey||view.current?.key!==viewKey||view.current.context!==context||view.current.recordRef!==(state.record?.ref||""))return;setInspectedId(row.id);publish(row, true);};
  useEffect(() => {
    if(!context||state?.viewKey!==viewKey)return;
    const id=inspectedId;if(!id)return;
    const row=context.items.find(value=>value.id===id);
    const position=JSON.stringify([viewKey,selectedId]);
    const open=Boolean(selectedId&&id===selectedId&&openedLocator.current!==position);
    if(open)openedLocator.current=position;
    if(row)publish(row,open);
    else {const message="原版本中找不到这个条目；已保留原位置，没有替换为其他条目。";setError(message);onInspect?.({company,workspaceId,ref:id,title:"原条目无法核对",content:<div className={styles.recordDetail}><p role="status">{message}</p><p>原条目标识：{id}</p><Link href={writingBookHref(workspaceId,book.ref,{section,item:id,context:locator?.context||state.record?.ref||""})}>返回该原位置</Link></div>},{open});}
  }, [selectedId,inspectedId,viewKey,context,state?.record?.ref,state?.viewKey,busy,requestLocked,readOnly]); // eslint-disable-line react-hooks/exhaustive-deps
  if (!context || !state || state.viewKey!==viewKey) return <section><p role="status">正在读取本书结构…</p>{error && <p role="alert">{error}</p>}</section>;
  const locked = busy || requestLocked || readOnly || state.read_only || Boolean(locator?.context);
  const items = context.items;
  const rows = items.filter(v => section === "world" ? v.kind === "world" : section === "characters" ? ["character", "relationship"].includes(v.kind) : ["outline", "volume", "chapter", "node"].includes(v.kind));
  const visible = section === "outline" ? orderedBookItems(rows, tab, collapsed) : rows.sort((a,b)=>a.order-b.order||a.id.localeCompare(b.id));
  const planned = new Set(items.filter(v => v.kind === "chapter").map(v => v.chapter_ref));
  const start = kind => { if (item && dirty) { setError("尚有条目输入，请先恢复保存或明确放弃，再添加新条目。"); return; } const next = blankItem(kind); next.order = Math.max(-1, ...items.filter(v => v.kind === kind && !v.parent).map(v => v.order)) + 1; setItem(next); setEditing(""); setDirty(true); };
  const field = (key, value) => { if (locked) return; setItem(v => ({ ...v, [key]: value })); setDirty(true); };
  const submitItem = async event => { event.preventDefault(); if (locked || !item.title.trim()) return;
    const common = ["id","kind","title","body","goal","status","order"];
    const extra = { outline:["character_refs","world_refs","direction_refs"],volume:["parent","character_refs","world_refs","direction_refs"],chapter:["parent","chapter_ref","handoff","character_refs","world_refs","direction_refs"],node:["parent","character_refs","world_refs","direction_refs"],world:["category"],character:["role","knowledge"],relationship:["from_character","to_character"] };
    const typed = Object.fromEntries([...common,...extra[item.kind]].map(key=>[key,item[key]]));
    const next = { ...context, items: editing ? items.map(v => v.id === editing ? typed : v) : [...items, typed] };
    change(next); await save(next); };
  return <section className={styles.bookMain}>
    <header className={styles.sectionHeading}><div><h2>{BOOK_SECTIONS[section]}</h2><p>方向、结构与设定服务于这本书；也可以先写正文，随后补充。</p></div><button className={styles.primary} disabled={locked || !dirty || Boolean(item)} onClick={()=>save()}>{busy ? "正在保存…" : "保存作品计划"}</button></header>
    <nav className={styles.bookSections} aria-label="作品工作步骤">{Object.entries(BOOK_SECTIONS).map(([key,label]) => <Link aria-current={section === key ? "page" : undefined} key={key} href={writingBookHref(workspaceId, book.ref, { section:key })}>{label}</Link>)}</nav>
    <div className={styles.workMeta}><span>{state.record ? `结构版本 ${state.record.revision}` : "尚未初始化 · 正文可继续"}</span><span>{state.chapters.length} 个真实章节</span><span>{dirty ? "计划有未保存输入" : "当前保存版本"}</span></div>
    {locator?.context && <p className={styles.notice}>正在查看固定原版本，编辑草稿单独保留。<Link href={writingBookHref(workspaceId,book.ref,{section})}>返回本书编辑与保留输入</Link></p>}
    {item && editing === null && <div className={styles.notice}><p>已保留尚未保存的条目输入。</p><button onClick={()=>setEditing(items.some(v=>v.id===item.id)?item.id:"")}>恢复编辑</button><button onClick={()=>{setItem(null);setDirty(JSON.stringify(context)!==JSON.stringify(state.context));}}>明确放弃这次条目输入</button></div>}
    {error && <p role="alert" className={styles.error}>{error}</p>}{notice && <p role="status">{notice}</p>}{state.head_ref !== base && <p role="status">当前输入基于原版本；请保留输入，先核对新版本。<Link href={writingBookHref(workspaceId, book.ref, { section, context:state.head_ref })}>查看最新保存版</Link>{!locator?.context && <button disabled={locked} onClick={()=>{setBase(state.head_ref);setDirty(true);setNotice("已明确以核对的新版本为基础，当前输入仍待保存，旧版本保持不变。");}}>已核对新版本，保留输入继续保存</button>}</p>}
    {section === "setup" && <p><Link href={`/ceo-office/workspace/installed/${encodeURIComponent(workspaceId)}?writing_mode=books&book_ref=${encodeURIComponent(book.ref)}&wr_view=directions`}>核对或明确确认作品方向 →</Link> · 可以跳过初始化，先创建章节写作。</p>}
    {section === "setup" ? <div className={styles.setupGrid}>{[["reader","目标读者"],["genre","题材与类型"],["premise","故事意图"],["style","叙事与风格"],["conflict","主线冲突"]].map(([key,label]) => <label key={key}>{label}<textarea disabled={locked} maxLength={2000} value={context.setup[key]} onChange={e => change({ ...context, setup:{...context.setup,[key]:e.target.value} })} /></label>)}</div> : <>
      {section === "outline" && <nav className={styles.tabs} aria-label="大纲层级">{[["all","全书大纲"],["volume","分卷"],["chapter","章节"],["node","故事节点"]].map(([key,label]) => <button key={key} aria-current={tab===key?"page":undefined} onClick={()=>setTab(key)}>{label}</button>)}</nav>}
      <div className={styles.tableScroll}><table className={styles.outlineTable}><thead><tr><th>标题与层级</th><th>戏剧目的 / 说明</th><th>关联人物</th><th>状态</th><th>动作</th></tr></thead><tbody>{visible.map(row => <tr key={row.id} aria-selected={row.id === inspectedId}><td><div className={styles.outlineTitle} style={{ paddingLeft: `${bookItemDepth(row, items)*16}px` }}><span className={styles.outlineExpander}>{items.some(v=>v.parent===row.id) && <button aria-label={`${collapsed.has(row.id)?"展开":"收起"}${row.title}`} onClick={()=>setCollapsed(value=>{const next=new Set(value);next.has(row.id)?next.delete(row.id):next.add(row.id);return next;})}>{collapsed.has(row.id)?"▸":"▾"}</button>}</span><button onClick={()=>inspect(row)}>{BOOK_KINDS[row.kind]} · {row.title}</button></div></td><td>{row.goal || row.body || "尚未填写"}</td><td>{row.kind === "relationship" ? [row.from_character,row.to_character].map(ref=>items.find(v=>v.id===ref&&v.kind==="character")?.title || "原人物缺失").join(" → ") : row.character_refs?.map(ref=>items.find(v=>v.id===ref)?.title).filter(Boolean).join("、") || "未关联"}</td><td>{row.status || "未开始"}</td><td><button disabled={locked} onClick={()=>edit(row)}>编辑</button><button disabled={locked} onClick={()=>change({...context,items:items.filter(v=>v.id!==row.id)})}>移除</button></td></tr>)}</tbody></table></div>
      {!visible.length && <p className={styles.notice}>本书尚无这些条目。保存自己的计划后，才能明确引用到章节。</p>}
      <div className={styles.headerActions}>{(section === "outline" ? ["outline","volume","chapter","node"] : section === "world" ? ["world"] : ["character","relationship"]).map(kind=><button key={kind} disabled={locked} onClick={()=>start(kind)}>＋ 添加{BOOK_KINDS[kind]}</button>)}</div>
    </>}
    {editing !== null && item && <form className={styles.bookItemForm} onSubmit={submitItem}><fieldset disabled={locked} className={styles.itemFields}><h3>{editing ? "编辑" : "添加"}{BOOK_KINDS[item.kind]}</h3><label>标题<input required maxLength={160} value={item.title} onChange={e=>field("title",e.target.value)} /></label><label>戏剧目的 / 说明<textarea maxLength={2000} value={item.goal} onChange={e=>field("goal",e.target.value)} /></label><label>详细内容<textarea maxLength={20000} value={item.body} onChange={e=>field("body",e.target.value)} /></label>
      {["volume","chapter","node"].includes(item.kind) && <label>所属层级<select value={item.parent} onChange={e=>{field("parent",e.target.value);field("order",Math.max(-1,...items.filter(v=>v.kind===item.kind&&v.parent===e.target.value&&v.id!==item.id).map(v=>v.order))+1);}}><option value="">尚未归卷 / 顶层</option>{items.filter(v=>v.id!==item.id&&(item.kind==="node"?v.kind==="chapter":item.kind==="volume"?v.kind==="outline":["outline","volume"].includes(v.kind))).map(v=><option key={v.id} value={v.id}>{v.title}</option>)}</select></label>}
      {item.kind === "chapter" && <label>真实章节<select required value={item.chapter_ref} onChange={e=>field("chapter_ref",e.target.value)}><option value="">选择已创建章节</option>{state.chapters.map(v=><option key={v.ref} value={v.ref}>{v.title}</option>)}</select></label>}
      {item.kind === "chapter" && <label>上一章交接（作者说明）<textarea value={item.handoff} maxLength={2000} onChange={e=>field("handoff",e.target.value)} /></label>}
      {item.kind === "world" && <label>设定类别<input value={item.category} onChange={e=>field("category",e.target.value)} placeholder="地点、时代、规则或物品" /></label>}
      {item.kind === "character" && <><label>人物角色<input value={item.role} onChange={e=>field("role",e.target.value)} /></label><label>当前知情 / 行为边界<textarea value={item.knowledge} maxLength={20000} onChange={e=>field("knowledge",e.target.value)} /></label></>}
      {item.kind === "relationship" && ["from_character","to_character"].map((key,index)=><label key={key}>{index?"关系指向人物":"起点人物"}<select required value={item[key]} onChange={e=>field(key,e.target.value)}><option value="">选择本书人物</option>{items.filter(v=>v.kind==="character").map(v=><option key={v.id} value={v.id}>{v.title}</option>)}</select></label>)}
      {["outline","volume","chapter","node"].includes(item.kind) && ["character_refs","world_refs"].map(key=><fieldset key={key}><legend>{key==="character_refs"?"关联人物":"世界依据"}</legend>{items.filter(v=>v.kind===(key==="character_refs"?"character":"world")&&v.id!==item.id).map(v=><label className={styles.check} key={v.id}><input type="checkbox" checked={item[key].includes(v.id)} onChange={e=>field(key,e.target.checked?[...item[key],v.id]:item[key].filter(r=>r!==v.id))} />{v.title}</label>)}</fieldset>)}
      {["outline","volume","chapter","node"].includes(item.kind) && <fieldset><legend>已确认作品方向</legend>{directions.filter(v=>v.data.confirmed_by&&(!v.data.scope_ref||v.data.scope_ref===book.ref)).map(v=><label className={styles.check} key={v.entity_id}><input type="checkbox" checked={item.direction_refs.includes(v.entity_id)} onChange={e=>field("direction_refs",e.target.checked?[...item.direction_refs,v.entity_id]:item.direction_refs.filter(r=>r!==v.entity_id))} />{v.data.title} · 原版本 {v.data.revision}</label>)}</fieldset>}
      <label>同层顺序<input type="number" min="0" max="100000" value={item.order} onChange={e=>field("order",Number(e.target.value))} /></label><label>状态<select value={item.status} onChange={e=>field("status",e.target.value)}>{["未开始","进行中","已完成","已归档"].map(v=><option key={v}>{v}</option>)}</select></label><div className={styles.headerActions}><button className={styles.primary} disabled={locked}>保存这条记录</button><button type="button" onClick={()=>setEditing(null)}>取消，保留输入</button></div><p>保存这条记录会同时保存本次作品计划。移除仍被引用的条目会被拒绝，须先明确调整关联。</p></fieldset></form>}
    <section className={styles.unfiled}><h3>章节与正文</h3>{state.chapters.map(row=><div className={styles.row} key={row.ref}><Link href={chapterHref(workspaceId,{book:book.ref,chapter:row.ref})}>{row.title} → 正文</Link><span>{planned.has(row.ref)?"已有章节计划":"未归卷 · 可继续写作"}</span></div>)}<form className={styles.create} onSubmit={e=>{e.preventDefault();if(!locked&&chapterTitle.trim())onCreateChapter(chapterTitle);}}><label>新章节标题<input required maxLength={160} value={chapterTitle} onChange={e=>setChapterTitle(e.target.value)} /></label><button disabled={locked}>创建真实章节并写作</button></form><p>创建章节与归卷分别保存；归卷失败保留真实章节，仅重试归卷。</p></section>
  </section>;
}
