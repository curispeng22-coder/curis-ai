"use client";
import { useCallback, useEffect, useLayoutEffect, useRef, useState } from "react";
import Link from "next/link";
import { createAssignedWork, getAssignedAgentWorkflow, publishAssignedAgentWorkflow } from "../../lib/v1FrontendApi.js";
import EmployeeConversation from "../v1/EmployeeConversation.js";
import { useRouter, useSearchParams } from "next/navigation";
import WorkspacePaneShell from "../workspace/WorkspacePaneShell.js";
import ContentGrowthMain from "./ContentGrowthMain.js";
import ContentGrowthMaterials from "./ContentGrowthMaterials.js";
import ContentGrowthLearning from "./ContentGrowthLearning.js";
import ContentGrowthAccounts from "./ContentGrowthAccounts.js";
import ContentGrowthVerify, { verifySourceContent } from "./ContentGrowthVerify.js";
import ContentGrowthObserve from "./ContentGrowthObserve.js";
import { contentGrowthApi as api } from "../../lib/contentGrowthApi.js";
import { cgEntry, contentHref, isContentGrowthPackage, stableRequest, cgSelectionFromEntry, CG_FORMATS, selectionFor } from "../../lib/contentGrowthState.mjs";
import ContentGrowthOperating from "./ContentGrowthOperating.js";
import ContentGrowthMarket from "./ContentGrowthMarket.js";
import ContentGrowthAnalysis from "./ContentGrowthAnalysis.js";
import styles from "./ContentGrowth.module.css";

function PublicationPackage({ value }) {
  return <section><h3>{value.title}</h3><p style={{ whiteSpace: "pre-wrap" }}>{value.body}</p>
    <p>标签 · {value.tags.join("、")}</p><p>封面文案 · {value.cover_copy}</p>
    <p>发布建议 · {value.publishing_advice}</p></section>;
}

export function PublicationWork({ company, workspaceId, collection, row, request, busy, locked, perform }) {
  const [brief, setBrief] = useState({ topic: "", audience: "", platform: "", goal: "" });
  const [suggestion, setSuggestion] = useState(null);
  const [instruction, setInstruction] = useState("");
  const [original, setOriginal] = useState(null);
  const [review, setReview] = useState(null);
  const [confirmed, setConfirmed] = useState("");
  const [notice, setNotice] = useState("");
  const [working, setWorking] = useState(false);
  const [canResume, setCanResume] = useState(false);
  const pending = useRef(false);
  const holder = collection.entry.assignments.length === 1 ? collection.entry.assignments[0] : null;
  const saved = row?.version.data;
  const model = saved?.work?.model_key || collection.entry.model_preference?.model_key;
  const authorized = holder?.models?.some((item) => item.model_key === model && item.execution_authorized);
  const ownPending = collection.pending_requests.find((item) => item.content_ref === row?.content.entity_id);
  const storageKey = `curis.cg.publication.${JSON.stringify([collection.entry.scope.tenant_id, company, workspaceId, row?.content.entity_id || "new"])}`;
  const readRetained = () => {
    try { return JSON.parse(localStorage.getItem(storageKey) || "null"); }
    catch { return { unreadable: true }; }
  };
  const restored = request?.attempt && { binding_ref: request.binding.binding_ref, attempt_id: request.attempt.attempt_id };
  const currentLocator = () => {
    const retained = original || readRetained();
    const current = retained?.work_payload?.payload?.source?.expected_version_ref === row?.version.entity_id
      ? retained : null;
    if (row?.publication_attempt) return { ...current, ...row.publication_attempt };
    return current || restored || (retained?.unreadable ? retained : null);
  };
  const run = async (operation) => {
    if (pending.current) return;
    pending.current = true; setWorking(true); setNotice("");
    try { await operation(); } catch (reason) { setNotice(reason.message); }
    finally { pending.current = false; setWorking(false); }
  };
  const create = () => run(async () => {
    if (!suggestion || !authorized) return;
    await api.prepareModel(company, workspaceId, { assignment_ref: holder.assignment_ref, model_key: model });
    await perform("create", {
      title: suggestion.title, topic: suggestion.topic, audience: suggestion.audience,
      body: `主题：${suggestion.title}\n受众：${suggestion.audience}\n平台：${suggestion.platform}\n目标：${suggestion.goal}`,
      format: "graphic", references: [], target_account_refs: [],
      work: { goal: suggestion.goal, recording_requirements: "", output_spec: suggestion.platform,
        output_intent: "UNCONFIRMED", assignment_ref: holder.assignment_ref,
        recipient_ref: holder.company_employee_ref, model_key: model, shots: [], source_refs: [],
        publication_brief: { platform: suggestion.platform, confirmed_topic: suggestion.title } },
    });
  });
  const query = () => run(async () => {
    const retained = currentLocator();
    const locator = ownPending ? { ...retained, ...ownPending } : retained;
    if (!locator?.binding_ref) { setNotice(locator?.unreadable ? "原交办记录无法读取，请先核对原任务。" : "当前内容还没有提交生成。"); return; }
    const result = await api.query(company, workspaceId, row.content.entity_id, locator.binding_ref, locator.attempt_id);
    const attempt = result.attempt || result.attempts?.find((item) =>
      item.execution_selection?.work_ref === locator.work_ref);
    setCanResume(!attempt && Boolean(locator.work_payload && locator.send_payload));
    if (attempt) {
      const resolved = { ...locator, status: attempt.effect_status === "UNKNOWN" ? "UNKNOWN" : attempt.status, attempt_id: attempt.attempt_id, work_ref: attempt.execution_selection?.work_ref || locator.work_ref };
      localStorage.setItem(storageKey, JSON.stringify(resolved));
      setOriginal(resolved);
    }
    if (attempt?.status === "COMPLETED" && attempt.effect_status !== "UNKNOWN") {
      await perform("materialize", { binding_ref: locator.binding_ref, attempt_id: attempt.attempt_id });
      setNotice("已回收内容包候选。");
    } else setNotice("原请求状态：" + (attempt?.effect_status === "UNKNOWN" ? "结果待核验" : attempt?.status || "等待核对"));
  });
  const generate = () => run(async () => {
    if (!row || locked || !authorized) return;
    const workflow = await getAssignedAgentWorkflow(holder.assignment_ref, company, workspaceId);
    if (workflow.state !== "READY") {
      setReview(workflow);
      setNotice(workflow.reason || "请先确认当前责任流程。");
      return;
    }
    const body = saved.publication_package ? instruction.trim() : "按已确认选题生成本期内容包。";
    if (!body) return;
    const selection = selectionFor(row.version, saved.body, 0, saved.body.length);
    const binding = await perform("bind", { assignment_ref: holder.assignment_ref });
    const locator = { binding_ref: binding.binding_ref, attempt_id: "", work_ref: "",
      work_payload: { assignment_ref: holder.assignment_ref, payload: {
        problem: body, expected_result: "标题、正文、标签、封面文案和发布建议",
        model_key: model, source: { kind: "content-growth", content_ref: row.content.entity_id,
          expected_version_ref: row.version.entity_id, selection, references: saved.references },
      } },
      send_payload: { binding_ref: binding.binding_ref, body, model_key: model, selection, references: saved.references },
    };
    localStorage.setItem(storageKey, JSON.stringify(locator));
    setOriginal(locator);
    await dispatch(locator);
  });
  const dispatch = async (locator) => {
    setCanResume(false);
    const base = locator.work_payload.payload.source.expected_version_ref;
    if (row.version.entity_id !== base) throw new Error("原内容版本已变化，请保留原交办并核对。");
    const created = locator.work_ref ? null : await perform("create-work", locator.work_payload, { base });
    const retained = { ...locator, work_ref: locator.work_ref || created.work.entity_id };
    localStorage.setItem(storageKey, JSON.stringify(retained));
    setOriginal(retained);
    const result = await perform("send", { ...retained.send_payload, work_ref: retained.work_ref }, { base });
    const finished = { ...retained, attempt_id: result.attempt.attempt_id };
    localStorage.setItem(storageKey, JSON.stringify(finished));
    setOriginal(finished);
    setNotice("已交办。可查询并回收原结果。");
  };
  if (!row) return <section className={styles.block}>
    <h2>制作内容包</h2>
    <form onSubmit={(event) => {
      event.preventDefault();
      const fields = Object.fromEntries(Object.entries(brief).map(([key, value]) => [key, value.trim()]));
      if (Object.values(fields).every(Boolean)) setSuggestion({ ...fields, title: `${fields.topic}：给${fields.audience}的实用切入点`.slice(0, 240) });
    }}>
      {Object.entries({ topic: "主题", audience: "目标受众", platform: "发布平台", goal: "内容目标" }).map(([key, label]) =>
        <label key={key}>{label}<input required maxLength={key === "platform" ? 80 : 200} value={brief[key]}
          onChange={(event) => { setSuggestion(null); setBrief({ ...brief, [key]: event.target.value }); }} /></label>)}
      <button>查看选题建议</button>
    </form>
    {suggestion && <><h3>选题策划 · 本地建议</h3><label>选题<input maxLength={240} value={suggestion.title}
      onChange={(event) => setSuggestion({ ...suggestion, title: event.target.value })} /></label>
      <button disabled={working || busy || locked || !authorized || !suggestion.title.trim()} onClick={create}>确认选题并保存</button></>}
    {!authorized && <p>请先为内容增长工作台确认所选模型的公司文字许可。</p>}
    {notice && <p role="status">{notice}</p>}
  </section>;
  const currentCandidate = row.candidates.find((item) => item.eligible && item.version.data.publication_package);
  const prior = currentLocator();
  const awaitingResult = prior && !["FAILED", "CANCELLED"].includes(prior.status) && !row.candidates.some((item) => item.version.data.attempt_id === prior.attempt_id);
  return <section className={styles.block}>
    <h1>{saved.title}</h1><p>发布平台 · {saved.work.publication_brief.platform}</p>
    {saved.publication_package && <><h2>正式内容包</h2><PublicationPackage value={saved.publication_package} /></>}
    {currentCandidate && <section><h2>审核候选内容包</h2><PublicationPackage value={currentCandidate.version.data.publication_package} />
      <label><input type="checkbox" checked={confirmed === currentCandidate.version.entity_id}
        onChange={(event) => setConfirmed(event.target.checked ? currentCandidate.version.entity_id : "")} />
        已核对正文、来源和发布建议，采用后保存在本地。</label>
      <button disabled={working || busy || locked || confirmed !== currentCandidate.version.entity_id} onClick={() => run(() => perform("adopt", {
        candidate_ref: currentCandidate.version.entity_id, checks: { content: true, references: true, account: true },
      }))}>确认采用为正式内容包</button></section>}
    {saved.publication_package && <label>下一期要求<textarea maxLength={1200} value={instruction}
      onChange={(event) => setInstruction(event.target.value)} /></label>}
    <button disabled={working || busy || locked || !authorized || awaitingResult || Boolean(currentCandidate) || (saved.publication_package && !instruction.trim())}
      onClick={generate}>{saved.publication_package ? "基于正式内容包交办下一期" : "交办生成内容包"}</button>
    {review?.state === "NEEDS_PUBLICATION" && review.publication_allowed && <button disabled={working || busy}
      onClick={() => run(async () => {
        await publishAssignedAgentWorkflow(holder.assignment_ref, { company_id: company, workspace_id: workspaceId,
          expected_revision: review.assignment_revision, review_token: review.review_token, confirm: true });
        setReview(null); setNotice("当前责任已确认，可以交办生成。");
      })}>确认当前责任流程</button>}
    {canResume && prior && <button disabled={working || busy || locked || !authorized}
      onClick={() => run(() => dispatch(prior))}>继续原交办</button>}
    <button disabled={working || busy} onClick={query}>查询并回收原结果</button>
    {notice && <p role="status">{notice}</p>}
  </section>;
}

export default function ContentGrowthWorkspace({ detail, workspaceId }) {
  const company = detail.instance.company_id, router = useRouter(), params = useSearchParams(), entry = cgEntry(params);
  const entryKey = JSON.stringify([company, workspaceId, entry]);
  const active = useRef(entryKey);
  useLayoutEffect(() => { active.current = entryKey; }, [entryKey]);
  const epoch = useRef(0), pending = useRef(false);
  const [verifiedKey, setVerifiedKey] = useState("");
  const [collection, setCollection] = useState(null), [row, setRow] = useState(null), [request, setRequest] = useState(null);
  const [creationSources, setCreationSources] = useState([]);
  const [error, setError] = useState(""), [busy, setBusy] = useState(false), [creating, setCreating] = useState(false);
  const [sourceError, setSourceError] = useState("");
  const [publication, setPublication] = useState(false);
  const [creationFormat, setCreationFormat] = useState("graphic");
  const [utility, setUtility] = useState({ scope: "", key: 0 });
  const inspect = useCallback((next) => setUtility((previous) => { if (!next) return { scope: entryKey, key: previous.key }; const id = encodeURIComponent(next.id); return { ...next, id, scope: entryKey, key: previous.key + (previous.scope !== entryKey || previous.id !== id || previous.request !== next.request ? 1 : 0) }; }), [entryKey]);
  const load = useCallback(async () => {
    const generation = ++epoch.current, key = entryKey;
    try {
      if (!isContentGrowthPackage(detail) || entry.error) throw new Error(entry.error || "内容组件依据不一致。");
      const next = await api.collection(company, workspaceId);
      if (next.entry.scope.company_id !== company || next.entry.scope.workspace_id !== workspaceId) throw new Error("当前内容范围不一致。");
      const current = entry.content ? await api.content(company, workspaceId, entry.content) : null;
      if (entry.version && !current?.versions.some((v) => v.entity_id === entry.version)) throw new Error("原正文版本不存在。");
      if (entry.version) cgSelectionFromEntry(current, entry);
      if (entry.candidate && !current?.candidates.some((item) => item.version.entity_id === entry.candidate && item.version.data.basis_version_ref === entry.version)) throw new Error("原候选或版本已变化，请返回内容目录核对。");
      const original = entry.attempt ? await api.query(company, workspaceId, entry.content, entry.binding, entry.attempt) : null;
      if (generation !== epoch.current || key !== active.current) return;
      setVerifiedKey(key); setCollection(next); setRow(current); setRequest(original); setError("");
    } catch (reason) { if (generation === epoch.current && key === active.current) { setError(reason.message); setRow(null); } }
  // The identity includes every bounded return locator and rejects late cross-content responses.
  }, [company, workspaceId, entryKey, detail]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { setCollection(null); setRow(null); setRequest(null); setCreating(false); setPublication(false); setSourceError(""); load(); return () => { epoch.current += 1; }; }, [load]);
  // Resolve cg_sources from URL into creationSources when the collection is ready.
  useEffect(() => {
    const isReady = verifiedKey === entryKey;
    if (!isReady || !collection || !entry.sources?.length || creating) return;
    const resolved = entry.sources
      .map((ref) => collection.reference_options.find((s) => s.reference_id === ref))
      .filter(Boolean)
      .map((s) => ({ ...s, purpose: "CONTEXT" }));
    if (resolved.length !== entry.sources.length) {
      setSourceError("部分素材来源不可确认，已忽略。");
    }
    if (resolved.length) { setCreationSources(resolved); setCreating(true); }
  }, [verifiedKey, entryKey, collection, entry.sources, creating]);
  const perform = async (action, data, options = {}) => {
    if (pending.current) throw new Error("请等待当前操作完成。");
    const key = entryKey; pending.current = true; setBusy(true);
    const base = options.base || row?.version.entity_id || "";
    const storage = ["create-work", "send"].includes(action) ? `curis.cg.model-work.${JSON.stringify([collection?.entry.scope.tenant_id, collection?.entry.actor, company, workspaceId, entry.content, action])}` : `curis.cg.request.${company}:${workspaceId}:${entry.content || "create"}:${action}`;
    const requestStorage = ["create-work", "send"].includes(action) ? localStorage : sessionStorage;
    let previous = null; try { previous = JSON.parse(requestStorage.getItem(storage) || "null"); } catch {}
    const identity = stableRequest(previous, action, base, data, () => crypto.randomUUID());
    try {
      requestStorage.setItem(storage, JSON.stringify(identity));
      const payload = { request_id: identity.request_id, expected_version_ref: base, data };
      const output = action === "create-work" ? await createAssignedWork(data.assignment_ref, { ...data.payload, request_id: identity.request_id })
        : action === "create" ? await api.create(company, workspaceId, payload)
        : action === "bind" ? await api.bind(company, workspaceId, entry.content, { request_id: identity.request_id, expected_version_ref: base, assignment_ref: data.assignment_ref })
        : action === "send" ? await api.send(company, workspaceId, entry.content, { ...data, request_id: identity.request_id, expected_version_ref: base })
        : action === "materialize" ? await api.candidate(company, workspaceId, entry.content, { ...data, request_id: identity.request_id })
        : await api.command(company, workspaceId, entry.content, action, payload);
      if (key !== active.current) throw new Error("内容已切换，请从原内容查看记录。");
      if (action === "create") {
        if (entry.object) {
          const payload={title:output.version.data.title,content_ref:output.content.entity_id,version_ref:output.version.entity_id,reference_refs:[],direction_ref:entry.object,report_refs:[]};
          await api.saveOperatingContext(company,workspaceId,"Context",{request_id:`${identity.request_id}-basis`,expected_ref:"",data:payload});
        }
        router.push(contentHref(workspaceId, { content: output.content.entity_id }));
      }
      else await load();
      return output;
    } catch (reason) { if (key === active.current) setError(reason.message); throw reason; }
    finally { pending.current = false; if (key === active.current) setBusy(false); }
  };
  const originalLink = (item) => contentHref(workspaceId, { content: item.content_ref, binding: item.binding_ref, attempt: item.attempt_id });
  const ready = verifiedKey === entryKey;
  const view = entry.content ? "work" : creating || entry.view === "production" ? "production" : entry.view || "operating";
  const methods = ["graphic", "long_video", "short_video", "speech"].map((format) => [format, CG_FORMATS[format]]);
  const navigation = [["operating", "经营"], ["market", "市场与方向"], ["production", "内容制作"], ["materials", "素材与灵感"], ["accounts", "平台与账号"], ["verify", "发布准备"], ["observe", "表现与归因"], ["analysis", "经营分析"], ["learning", "内容经验"]];
  const start = (format = "graphic", sources = []) => { inspect(null); setCreationFormat(format); setCreationSources(sources); setCreating(true); };
  const currentUtility = utility.scope === entryKey && utility.content ? utility : null;
  const verificationSource = verifySourceContent(collection?.contents, entry.object, collection?.entry?.scope);
  const context = <div className={styles.context}><h2>内容增长</h2><nav aria-label="内容增长工作区">{navigation.map(([key, label]) => <Link key={key} aria-current={view === key ? "page" : undefined} href={contentHref(workspaceId, { view: key })}>{label}</Link>)}</nav>{row && <section><h3>当前内容</h3><Link aria-current="page" href={contentHref(workspaceId, { content: row.content.entity_id })}>{row.version.data.title}</Link><p className={styles.sub}>{CG_FORMATS[row.version.data.format] || "图文"} · 本地正文</p></section>}<section><h3>最近内容</h3>{ready && collection?.contents.slice(0, 8).map((item) => <Link key={item.content.entity_id} href={contentHref(workspaceId, { content: item.content.entity_id })}>{item.version.data.title}</Link>)}</section></div>;
  const locked = Boolean(ready && collection?.pending_requests.length);
  const discussionHolders = (collection?.entry?.assignments || []).filter((item) => item.employee_ref && item.assignment_ref && item.company_id === company && item.workspace_id === workspaceId && item.scope_type === "WORKSPACE" && item.scope_ref === workspaceId && item.tenant_id === collection.entry.scope.tenant_id);
  const discussionHolder = discussionHolders.length === 1 ? discussionHolders[0] : null;
  return <WorkspacePaneShell workspaceId={workspaceId} surfaceId="content-growth-graphic" breadcrumb={`内容增长 / ${view === "work" ? row?.version.data.title || "内容创作" : navigation.find(([key]) => key === view)?.[1] || "内容制作"}`} contextAvailable contextPane={context} initialContextOpen contextLabel="经营与内容" utilityAvailable={Boolean(currentUtility)} utilityTabs={currentUtility ? [{ id: currentUtility.id, title: currentUtility.title, content: currentUtility.content }] : []} utilityRequestKey={currentUtility?.key || 0} utilityRequestTabId={currentUtility?.id || ""} utilityLabel="辅助内容">
    <div className={styles.main}>{error && <p className={styles.error} role="alert">{error}</p>}{sourceError && <p className={styles.error} role="alert">{sourceError}</p>}
      {(!ready || !collection) && !error && <p role="status" className={styles.sub}>正在读取内容工作区…</p>}
      {ready && collection && <>
        {collection.entry.publication_status !== "PUBLISHED" && <span className={styles.reviewBadge}>内部审阅 · 尚未正式启用</span>}
      {collection && view !== "work" && discussionHolder && <EmployeeConversation key={`${company}:${workspaceId}:workspace:${discussionHolder.employee_ref}`} companyId={company} employee={{ ...discussionHolder, id: discussionHolder.company_employee_ref }} blocked={Boolean(locked || busy)} embedded={{ workspaceId, contextKey: "workspace", assignmentRef: discussionHolder.assignment_ref, title: "内容增长工作空间讨论", showBar: true }} businessReturn={{ href: contentHref(workspaceId, { view }), kind: "content-growth" }} />}
        {view === "operating" && collection.entry.definition.version === "0.2.0" && <button
          onClick={() => { setPublication(true); setCreating(true); }}>制作内容包</button>}
        {view === "operating" && <ContentGrowthOperating key={entryKey} company={company} workspaceId={workspaceId} collection={collection} onInspect={inspect} />}
        {view === "market" && <ContentGrowthMarket key={entryKey} company={company} workspaceId={workspaceId} collection={collection} onInspect={inspect} />}
        {view === "analysis" && <ContentGrowthAnalysis key={entryKey} company={company} workspaceId={workspaceId} collection={collection} entry={entry} onInspect={inspect} />}
        {view === "materials" && <ContentGrowthMaterials key={entryKey} company={company} workspaceId={workspaceId} entry={entry} onInspect={inspect} />}
        {view === "learning" && <ContentGrowthLearning key={entryKey} company={company} workspaceId={workspaceId} entry={entry} onInspect={inspect} />}
        {view === "accounts" && <ContentGrowthAccounts key={entryKey} company={company} workspaceId={workspaceId} onInspect={inspect} sourceRef={entry.object} sourceContent={verificationSource} />}
        {view === "verify" && <ContentGrowthVerify key={entryKey} company={company} workspaceId={workspaceId} onInspect={inspect} sourceRef={entry.object} />}
        {view === "observe" && <ContentGrowthObserve key={entryKey} company={company} workspaceId={workspaceId} onInspect={inspect} />}
        {view === "production" && <>
          {entry.object && <p className={styles.notice}>本次将明确关联所选原方向；创建成功但关联未核实会保留原创建请求，仅重试关联，不另建内容。</p>}
          <header className={styles.pageHeader}><div><h1>内容制作</h1><p className={styles.sub}>选择创作方式，让内容从想法走向可核对的正文与脚本。</p></div>{creating && <button disabled={busy} onClick={() => { setCreating(false); setPublication(false); inspect(null); }}>返回制作目录</button>}</header>
          {!creating && <><div className={styles.methods}>{methods.map(([format, label], index) => {
            const available = collection.entry.definition.version === "0.2.0" || format === "graphic";
            const rows = collection.contents.filter((item) => (item.version.data.format || "graphic") === format);
            return <button key={format} className={styles.method} disabled={!available || busy} onClick={() => start(format)}><span className={styles.methodNumber}>0{index + 1}</span><strong>{label}</strong><span>{format === "graphic" ? "主题 · 正文 · 人工审阅" : format === "speech" ? "表达 · 录制要求 · 脚本" : "策划 · 脚本 · 分镜"}</span><small>{available ? `${rows.length} 条本地内容 · 新建空稿 →` : "当前图文版本不支持"}</small></button>;
          })}</div><h2 className={styles.sectionTitle}>制作工作</h2>{methods.map(([format, label]) => {
            const rows = collection.contents.filter((item) => (item.version.data.format || "graphic") === format);
            return <section key={format} className={styles.workGroup}><header className={styles.row}><h3>{label}</h3><span className={styles.sub}>{rows.length} 条</span></header>{rows.length ? <div className={styles.tableScroll}><table className={styles.collection}><thead><tr><th>主题与内容</th><th>受众 / 当前责任</th><th>当前本地工序</th><th>下一步</th></tr></thead><tbody>{rows.map((item) => {
              const pending = collection.pending_requests.find((r) => r.content_ref === item.content.entity_id);
              return <tr key={item.content.entity_id}><td><Link href={contentHref(workspaceId, { content: item.content.entity_id })}>{item.version.data.title}</Link><small>{item.version.data.topic}</small></td><td>{item.version.data.audience}<small>{collection.entry.assignments?.find(v=>v.entity_id===item.version.data.work?.assignment_ref)?.name || "责任详情按需核对"}</small></td><td>{pending ? pending.status === "RUNNING" ? "建议处理中" : "原请求待核验" : "本地保存正文"}</td><td><Link href={pending ? originalLink(pending) : contentHref(workspaceId, { content: item.content.entity_id })}>{pending ? "查看原请求" : "继续创作"}</Link>{collection.entry.definition.version === "0.2.0" && <button disabled={busy} onClick={() => { const source = collection.reference_options.find((r) => r.reference_id === item.content.entity_id); if (source) start(format, [{ ...source, purpose: "CONTEXT" }]); }}>据此新建</button>}</td></tr>;
            })}</tbody></table></div> : <p className={styles.emptyRow}>还没有{label}内容，选择上方创作方式开始。</p>}</section>;
          })}</>}
          {creating && publication && <PublicationWork company={company} workspaceId={workspaceId} collection={collection}
            row={null} busy={busy} locked={locked} perform={perform} />}
          {creating && !publication && <ContentGrowthMain key={`new:${creationFormat}:${JSON.stringify(creationSources)}`} initialFormat={creationFormat} onFormatChange={(format) => { inspect(null); setCreationFormat(format); }} initialSources={creationSources} onInspect={inspect} company={company} workspaceId={workspaceId} entry={{}} row={null} collection={collection} busy={busy} locked={locked} perform={perform} />}
        </>}
        {view === "work" && row?.version.data.work?.publication_brief && <PublicationWork key={row.content.entity_id}
          company={company} workspaceId={workspaceId} collection={collection} row={row} request={request} busy={busy} locked={locked} perform={perform} />}
        {view === "work" && row && !row.version.data.work?.publication_brief && <ContentGrowthMain key={`${row.content.entity_id}:${entry.candidate || ""}`} onInspect={inspect} company={company} workspaceId={workspaceId} entry={entry} row={row} request={request} collection={collection} busy={busy} locked={locked} perform={perform} reload={load} />}
      </>}
    </div>
  </WorkspacePaneShell>;
}
