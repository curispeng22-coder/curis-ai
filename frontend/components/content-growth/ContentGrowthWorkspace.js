"use client";
import { useCallback, useEffect, useLayoutEffect, useRef, useState } from "react";
import Link from "next/link";
import { createAssignedWork } from "../../lib/v1FrontendApi.js";
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
import { cgEntry, contentHref, isContentGrowthPackage, stableRequest, cgSelectionFromEntry, CG_FORMATS } from "../../lib/contentGrowthState.mjs";
import ContentGrowthOperating from "./ContentGrowthOperating.js";
import ContentGrowthMarket from "./ContentGrowthMarket.js";
import ContentGrowthAnalysis from "./ContentGrowthAnalysis.js";
import styles from "./ContentGrowth.module.css";

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
  useEffect(() => { setCollection(null); setRow(null); setRequest(null); setCreating(false); setSourceError(""); load(); return () => { epoch.current += 1; }; }, [load]);
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
          <header className={styles.pageHeader}><div><h1>内容制作</h1><p className={styles.sub}>选择创作方式，让内容从想法走向可核对的正文与脚本。</p></div>{creating && <button disabled={busy} onClick={() => { setCreating(false); inspect(null); }}>返回制作目录</button>}</header>
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
          {creating && <ContentGrowthMain key={`new:${creationFormat}:${JSON.stringify(creationSources)}`} initialFormat={creationFormat} onFormatChange={(format) => { inspect(null); setCreationFormat(format); }} initialSources={creationSources} onInspect={inspect} company={company} workspaceId={workspaceId} entry={{}} row={null} collection={collection} busy={busy} locked={locked} perform={perform} />}
        </>}
        {view === "work" && row && <ContentGrowthMain key={`${row.content.entity_id}:${entry.candidate || ""}`} onInspect={inspect} company={company} workspaceId={workspaceId} entry={entry} row={row} request={request} collection={collection} busy={busy} locked={locked} perform={perform} reload={load} />}
      </>}
    </div>
  </WorkspacePaneShell>;
}
