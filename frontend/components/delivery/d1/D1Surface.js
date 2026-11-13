"use client";

import { useCallback, useEffect, useReducer, useRef, useState } from "react";
import { useSearchParams } from "next/navigation";
import { useRuntime } from "../../runtime/RuntimeProvider.js";
import { businessReturnInput, validateBusinessReturn } from "../../../lib/businessReturnApi.js";
import { d1Api, d1Error } from "../../../lib/d1Api.js";
import { d1Reducer, d1Href, initialD1State, interactionKey, parseD1Entry, currentResponsibilities } from "../../../lib/d1State.mjs";
import CeoMatterView from "./CeoMatterView.js";
import EmployeeConversationView from "./EmployeeConversationView.js";
import WorkView from "./WorkView.js";
import ResultView from "./ResultView.js";
import styles from "./D1.module.css";
import WorkspacePaneShell from "../../workspace/WorkspacePaneShell.js";
import { roleLabel } from "../../../lib/theme.js";
import { getOrganizationProjection } from "../../../lib/runtimeApi.js";
import { buildOrganizationProjection } from "../../../lib/organizationProjection.js";


export function BusinessConversationReturn({ search, companyId }) {
  const [verified, setVerified] = useState(null);
  useEffect(() => {
    let active = true;
    setVerified(null);
    let input;
    try { input = businessReturnInput(new URLSearchParams(search)); } catch { return; }
    if (!input) return;
    validateBusinessReturn(input.kind, input.value)
      .then((target) => { if (active) setVerified({ search, companyId, target }); })
      .catch(() => { if (active) setVerified(null); });
    return () => { active = false; };
  }, [search, companyId]);
  if (!verified || verified.search !== search || verified.companyId !== companyId) return null;
  return <a className={styles.back} href={verified.target.href}>{verified.target.label} →</a>;
}

export default function D1Surface({ initialView = "home", legacyEntry, navigationSlot, utilitySlot }) {
  const runtime = useRuntime();
  const companyId = runtime.companyId;
  const [state, dispatch] = useReducer(d1Reducer, { view: initialView, explicit: false }, initialD1State);
  const [ready, setReady] = useState(false);
  const [home, setHome] = useState({ companyId: "", loading: true, attention: null, businesses: [], error: "", businessesKnown: false });
  const [work, setWork] = useState({ loading: true, value: null, error: "" });
  const [reload, setReload] = useState(0);
  const [discussion, setDiscussion] = useState(null);
  const [discussionOpen, setDiscussionOpen] = useState(false);
  const [utility, setUtility] = useState(null);
  const utilityRequest = useRef(null);
  const utilityTrigger = useRef(null);
  const [utilityRequestKey, setUtilityRequestKey] = useState(0);
  const requestEmployeeDetail = (employeeRef, workspaceId) => {
    setUtilityRequestKey((value) => value + 1);
    return openEmployeeDetail(employeeRef, workspaceId);
  };
  const entry = state.entry;

  const search = useSearchParams().toString();
  const currentEntry = useRef(entry);
  const currentCompany = useRef(companyId);
  useEffect(() => { currentCompany.current = companyId; }, [companyId]);
  const workGeneration = useRef(0);
  const restoredEntry = useRef(false);
  useEffect(() => { currentEntry.current = entry; }, [entry]);
  useEffect(() => {
    const restore = () => { dispatch({ type: "restore", entry: parseD1Entry(window.location.search, initialView) }); setDiscussion(null); setDiscussionOpen(false); utilityRequest.current = null; setUtility(null); };
    const next = parseD1Entry(search, initialView);
    // Internal history updates already dispatched their entry and must retain
    // return anchors and explicit Result intent. External destinations restore.
    if (!restoredEntry.current || Object.entries(next).some(([key, value]) => key !== "explicit" && (currentEntry.current[key] || "") !== (value || ""))) restore();
    restoredEntry.current = true;
    setReady(true);
    window.addEventListener("popstate", restore);
    return () => window.removeEventListener("popstate", restore);
  }, [search, initialView]);

  useEffect(() => { utilityRequest.current = null; setUtility(null); }, [companyId]);

  useEffect(() => {
    let active = true;
    setHome({ companyId, loading: true, attention: null, businesses: [], error: "", businessesKnown: false });
    if (!companyId) return () => { active = false; };
    Promise.allSettled([d1Api.attention(companyId).then((payload) => {
      if (payload?.company?.company_id && payload.company.company_id !== companyId) throw new Error("公司事项来源不一致");
      return payload;
    }), d1Api.businesses(companyId), getOrganizationProjection(companyId).then((payload) => {
      if (payload?.company?.company_id !== companyId) throw new Error("公司组织来源不一致");
      return buildOrganizationProjection(payload);
    })]).then(([attention, businesses, organization]) => {
      if (!active) return;
      setHome({ companyId, loading: false, attention: attention.status === "fulfilled" ? attention.value : null,
        businesses: businesses.status === "fulfilled" ? (businesses.value.businesses || []).filter((item) => item.company_id === companyId) : [],
        businessesKnown: businesses.status === "fulfilled",
        organization: organization.status === "fulfilled" ? organization.value : null,
        organizationError: organization.status === "rejected" ? "组织资料暂不可读取；负责人信息尚未确认。" : "",
        error: attention.status === "rejected" ? d1Error(attention.reason) : businesses.status === "rejected" ? "业务目录尚未读取；已读取的事项仍保留。" : "" });
    });
    return () => { active = false; };
  }, [companyId, reload]);

  const refreshWork = useCallback(async () => {
    const scope = JSON.stringify([companyId, entry.workspaceId, entry.workRef]);
    const ticket = ++workGeneration.current;
    const isCurrent = () => ticket === workGeneration.current && currentCompany.current === companyId
      && currentEntry.current.view === "work"
      && JSON.stringify([companyId, currentEntry.current.workspaceId, currentEntry.current.workRef]) === scope;
    setWork((previous) => ({ ...previous, loading: true, error: "" }));
    try {
      const value = await d1Api.work(companyId, entry.workspaceId, entry.workRef);
      if (!isCurrent()) throw new Error("原工作范围已变化，请返回原来源重新读取。");
      setWork({ loading: false, value, error: "" });
      return value;
    } catch (cause) {
      if (isCurrent()) setWork((previous) => ({ ...previous, loading: false,
        error: cause.code === "WORK_READ_SCOPE_GAP" ? "这项工作缺少可用的读取入口。请返回原来源核对。" : d1Error(cause) }));
      throw cause;
    }
  }, [companyId, entry.workspaceId, entry.workRef]);
  useEffect(() => {
    setWork({ loading: true, value: null, error: "" });
    if (companyId && entry.view === "work") refreshWork().catch(() => {});
    return () => { workGeneration.current += 1; };
  }, [companyId, entry.view, refreshWork]);

  function navigate(next, anchor = "") {
    setDiscussion(null); setDiscussionOpen(false); utilityRequest.current = null; setUtility(null);
    dispatch({ type: "navigate", entry: next, anchor });
    window.history.pushState(null, "", d1Href(next, window.location.pathname) + (meetingReturn ? `&return_to=${encodeURIComponent(meetingReturn)}` : ""));
  }
  function back() {
    setDiscussion(null); setDiscussionOpen(false); utilityRequest.current = null; setUtility(null);
    const previous = state.returns.at(-1) || { view: initialView, explicit: false };
    dispatch({ type: "back" });
    window.history.replaceState(null, "", d1Href(previous, window.location.pathname) + (meetingReturn ? `&return_to=${encodeURIComponent(meetingReturn)}` : ""));
    if (previous.anchor) window.requestAnimationFrame(() => document.getElementById(previous.anchor)?.focus());
  }
  function openWork(reference, workspaceId) { navigate({ ...entry, view: "work", workRef: reference, workspaceId: workspaceId || "", resultRef: "", resultOrigin: "", resultVersion: "", originCompany: "", resultBridgeInvalid: false, explicit: false }); }
  function openResult(reference, workspaceId) { navigate({ ...entry, view: "result", resultRef: reference, workspaceId: workspaceId || "", resultOrigin: "", resultVersion: "", originCompany: "", resultBridgeInvalid: false, explicit: true }); }
  function discuss(employeeRef, workspaceId) {
    const next = { ...entry, view: "conversation", employeeRef: employeeRef || "", conversationId: "", workspaceId: workspaceId || "", explicit: false };
    if (discussion && interactionKey(companyId, discussion) === interactionKey(companyId, next)) setDiscussionOpen((value) => !value);
    else { setDiscussion(next); setDiscussionOpen(true); }
  }
  async function openEmployeeDetail(employeeRef, workspaceId) {
    const token = {}; utilityRequest.current = token; utilityTrigger.current = document.activeElement;
    const currentWorkRef = workspaceId === entry.workspaceId ? entry.workRef || "" : "";
    setUtility({ loading: true, employee: null, error: "" });
    try {
      const value = await d1Api.employeeDetail(companyId, employeeRef, workspaceId);
      if (utilityRequest.current === token) setUtility({ loading: false, employee: value, responsibilities: currentResponsibilities(value, currentWorkRef), error: "" });
    } catch (_cause) {
      if (utilityRequest.current === token) setUtility({ loading: false, employee: null, error: "尚不能确认这位员工的档案身份或读取权限。请回到原工作空间核对。" });
    }
  }
  function closeEmployeeDetail() {
    utilityRequest.current = null; setUtility(null); utilityTrigger.current?.focus();
  }
  const refresh = useCallback(async () => { setReload((value) => value + 1); }, []);
  const company = runtime.snapshot?.company;
  if (!ready || runtime.status === "idle" || runtime.status === "loading") return <div className={styles.root}><p className={styles.loading} role="status">正在读取公司与工作范围…</p></div>;
  if (["error", "forbidden"].includes(runtime.status)) return <div className={styles.root}><section className={styles.empty} role="alert"><h1>公司当前无法读取</h1><p>{runtime.error || "请确认登录与公司权限。"}</p><button onClick={runtime.refresh}>重新读取公司</button></section></div>;
  if (!companyId) return legacyEntry || <div className={styles.root}><section className={styles.empty}><h1>先建立公司</h1><a href="/welcome">返回公司建立入口</a></section></div>;
  if (entry.view === "home" && home.companyId === companyId && home.businessesKnown && home.businesses.length === 0 && legacyEntry) return legacyEntry;
  let meetingReturn = "";
  const returns = new URLSearchParams(search).getAll("return_to");
  if (returns.length === 1) {
    const raw = returns[0];
    try {
      const url = new URL(raw, "http://curis.local");
      const ids = url.searchParams.getAll("meeting"), companies = url.searchParams.getAll("company_id");
      if (raw.startsWith("/ceo-office/meeting?") && raw.length <= 2048 && !/[\\\x00-\x20\x7f#]/.test(raw)
        && url.origin === "http://curis.local" && url.pathname === "/ceo-office/meeting" && !url.hash
        && ids.length === 1 && ids[0].trim() && !/[\\\x00-\x20\x7f#]/.test(ids[0])
        && companies.length <= 1 && (!companies.length || companies[0] === companyId)
        && [...url.searchParams.keys()].every((key) => ["meeting", "company_id"].includes(key))) meetingReturn = url.pathname + url.search;
    } catch { /* An invalid source never becomes a return target. */ }
  }
  const focused = ["work", "result", "matter"].includes(entry.view);
  const backLabel = state.returns.length ? "返回原对象" : "返回 CEO 工作台";
  const hasWorkDirectory = ["work", "result"].includes(entry.view) && Boolean(entry.workRef && entry.workspaceId);
  const discussionView = discussionOpen && discussion ? <div id="d1-work-discussion" className={styles.discussionSlot}><EmployeeConversationView key={interactionKey(companyId, discussion)} companyId={companyId} entry={discussion} api={d1Api} compact onFull={() => navigate(discussion)} onEntry={navigate} onResult={openResult} onEmployeeDetail={requestEmployeeDetail} /></div> : null;
  const directory = hasWorkDirectory ? (<section className={[styles.root, styles.embeddedRoot, styles.context, styles.embeddedDirectory, styles.workResultDirectory].join(" ")}><p>{entry.view === "work" ? work.value?.problem || "工作名称未记录" : "保留原工作与来源"}</p><button onClick={back}>← {backLabel}</button>{entry.workRef && entry.view !== "work" && <button onClick={() => openWork(entry.workRef, entry.workspaceId)}>工作详情</button>}<p className={styles.limit}>来源与责任保持原范围。</p></section>) : null;
  const employeeDetail = utility ? (<section className={[styles.root, styles.embeddedRoot, styles.employeeUtility, styles.embeddedUtility].join(" ")} aria-label="员工档案">{utility.loading ? <p role="status">正在读取员工档案…</p> : utility.error ? <p role="alert">{utility.error}</p> : <><h3>{utility.employee.organization_record.name || "员工姓名未记录"}</h3><dl className={styles.meta}><dt>岗位</dt><dd>{roleLabel(utility.employee.organization_record.role) || "岗位名称未记录"}</dd><dt>部门</dt><dd>{utility.employee.organization_record.primary_department?.name || "未记录"}</dd><dt>当前责任</dt><dd>{utility.responsibilities.items.length ? <ul>{utility.responsibilities.items.map((item, index) => <li key={index}><strong>{item.current ? "当前查看的工作" : item.work ? "当前工作" : "当前职责"}</strong><p>{item.activity}</p></li>)}</ul> : utility.responsibilities.message}</dd><dt>岗位职责</dt><dd>{typeof utility.employee.responsibility === "string" && utility.employee.responsibility.trim() ? utility.employee.responsibility : "岗位职责未记录"}</dd><dt>当前情况</dt><dd>{utility.employee.ui_status?.label || "未记录"}</dd></dl><p className={styles.limit}>档案来自当前公司，查看不会改变员工的工作或讨论。</p><details className={styles.sourceDetails}><summary>查看员工来源详情</summary><dl className={styles.meta}><dt>公司标识</dt><dd>{companyId}</dd><dt>员工标识</dt><dd>{utility.employee.employee_ref}</dd><dt>档案标识</dt><dd>{utility.employee.company_employee_ref}</dd></dl></details></>}</section>) : utilitySlot;
  const homeCompany = entry.view === "home" && runtime.snapshot?.company?.company_id === companyId ? runtime.snapshot.company : null;
  const scopedHomeBusinesses = home.companyId === companyId ? home.businesses : [];
  const homeDirectory = homeCompany ? <nav aria-label="公司业务导航" className="space-y-4"><h2 className="text-sm font-semibold">{homeCompany.name}</h2>{home.companyId !== companyId || home.loading ? <p role="status">正在读取业务导航…</p> : scopedHomeBusinesses.length ? scopedHomeBusinesses.map((item) => <a key={item.business_id} className="block text-sm text-ui-primary" href={`/ceo-office/business?company_id=${encodeURIComponent(companyId)}&business_id=${encodeURIComponent(item.business_id)}`}>{item.name || "未命名业务"}</a>) : <p className="text-sm text-ui-txt-2">{home.businessesKnown ? "还没有经营中的业务" : "业务导航暂时无法读取"}</p>}<a className="block text-sm text-ui-primary" href={`/ceo-office/business?company_id=${encodeURIComponent(companyId)}`}>查看业务目录 →</a></nav> : null;
  const homeTabs = homeCompany ? [{ id: JSON.stringify([companyId, "facts"]), title: "当前公司", content: <section><h2 className="text-lg font-semibold">{homeCompany.name}</h2><dl className="mt-4 space-y-3 text-sm"><div><dt className="text-ui-txt-2">工作空间</dt><dd>{Array.isArray(runtime.snapshot.workspaces) ? runtime.snapshot.workspaces.length : "尚未读取"}</dd></div><div><dt className="text-ui-txt-2">已读取业务</dt><dd>{home.companyId === companyId && home.businessesKnown ? scopedHomeBusinesses.length : "尚未读取"}</dd></div></dl></section> }, ...scopedHomeBusinesses.map((item) => ({ id: JSON.stringify([companyId, "business", item.business_id]), title: item.name || "业务信息", content: <section><h2 className="text-lg font-semibold">{item.name || "未命名业务"}</h2><p className="mt-3 text-sm text-ui-txt-2">{item.definition?.goal || "经营目标尚未读取"}</p><a className="mt-4 block text-ui-primary" href={`/ceo-office/business?company_id=${encodeURIComponent(companyId)}&business_id=${encodeURIComponent(item.business_id)}`}>进入业务现场 →</a></section> }))] : undefined;
  return <WorkspacePaneShell workspaceId={entry.workspaceId || ""} surfaceId={"d1:" + initialView + ":" + entry.view}
    breadcrumb={entry.view === "conversation" ? "员工对话" : entry.view === "result" ? "阅读结果" : entry.view === "work" ? "当前工作" : "CEO 工作台"}
    navigationSlot={navigationSlot} contextAvailable={Boolean(homeDirectory || directory)} contextPane={homeDirectory || directory} contextLabel={homeCompany ? "公司业务" : "当前工作"}
    utilityAvailable={Boolean(homeTabs?.length || employeeDetail)} utilityPane={homeCompany ? undefined : employeeDetail} utilityTabs={homeTabs} utilityLabel={homeCompany ? "对象信息" : "员工详情"} utilityRequestKey={utilityRequestKey}
    initialContextOpen={Boolean(homeCompany)} initialUtilityOpen={Boolean(homeCompany)}
    onUtilityClose={utility ? closeEmployeeDetail : undefined}>
    <div className={[styles.root, styles.embeddedRoot].join(" ")} data-d1-batch="SUPPORTED_PATHS"><div className={[styles.main, styles.embeddedMain].join(" ")} id="d1-main">
      {entry.view === "conversation" && <BusinessConversationReturn search={search} companyId={companyId} />}
      {meetingReturn && <a className={styles.back} href={meetingReturn}>返回原会议 →</a>}
      {state.returns.length > 0 && (!focused || entry.view === "matter") && <button className={styles.back} onClick={back}>← 返回原对象</button>}
      {entry.view === "home" || entry.view === "matter" ? <>
        {home.loading ? <p role="status" className={styles.loading}>正在读取公司事项…</p> : <CeoMatterView company={company} attention={home.companyId === companyId ? home.attention : null} businesses={scopedHomeBusinesses} businessesKnown={home.companyId === companyId && home.businessesKnown} organization={home.companyId === companyId ? home.organization : null} organizationError={home.companyId === companyId ? home.organizationError : ""} selected={entry.view === "matter" ? entry : null}
          onMatter={(item) => navigate({ view: "matter", sourceRef: item.source_ref, sourceType: item.source_type, workspaceId: item.workspace_id || "", explicit: false }, `matter-${item.source_ref}`)} onWork={openWork} onResult={openResult} onDiscuss={discuss} />}
        {home.error && <div className={styles.error} role="alert"><p>{home.error}</p><button onClick={refresh}>重新读取公司事项</button></div>}
      </> : null}
      {entry.view === "work" && (work.value?.companyId === companyId && work.value?.workspaceId === entry.workspaceId && work.value?.work_ref === entry.workRef ? <>
        <WorkView key={JSON.stringify([companyId, entry.workspaceId, entry.workRef])} work={work.value} companyId={companyId} api={d1Api} onResult={openResult} onDiscuss={discuss} onRefresh={refreshWork} onEmployeeDetail={requestEmployeeDetail} discussionOpen={discussionOpen} discussionSlot={discussionView} />
        {work.loading && <p role="status">正在重新读取原工作，输入仍保留…</p>}
        {work.error && <p role="alert">{work.error}</p>}
      </> : work.loading ? <p className={styles.loading} role="status">正在读取原工作…</p> : <section className={styles.panel} role="alert"><h1>这项工作暂时无法打开</h1><p>{work.error}</p><div className={styles.actions}><button onClick={() => refreshWork().catch(() => {})}>重新读取工作</button><button onClick={back}>{backLabel}</button>{entry.workspaceId && <a href={`/ceo-office/workspace/installed/${encodeURIComponent(entry.workspaceId)}`}>返回原工作空间</a>}</div></section>)}
      {entry.view === "result" && <ResultView key={JSON.stringify([companyId, entry.workspaceId, entry.resultRef])} companyId={companyId} selection={entry} api={d1Api} onBack={back} backLabel={backLabel} onWork={openWork} onViewed={refresh} />}
      {entry.view === "conversation" && <EmployeeConversationView key={interactionKey(companyId, entry)} companyId={companyId} entry={entry} api={d1Api} onEntry={navigate} onResult={openResult} onEmployeeDetail={requestEmployeeDetail} />}
      {entry.view !== "work" && discussionView}
    </div></div>
  </WorkspacePaneShell>;
}
