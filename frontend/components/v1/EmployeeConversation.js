"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { AgentWorkControl, ConversationComposer } from "./SharedConversation.js";
import { EmployeeAvatar } from "./EmployeeAvatar.js";
import { confirmConversationResearchWork, receiveConversationResult, createConversation, executeOriginalAgentWork, getConversation, sendConversation, getCompanyTextPolicy, getEmployeeConversation, getEmployeeConversationReferences, openEmployeeConversation, sendEmployeeConversation } from "../../lib/v1FrontendApi.js";
import { musicApi } from "../../lib/musicApi.js";
import { getCanonicalBusinesses } from "../../lib/runtimeApi.js";
import { operatingHref, stableRequest } from "../../lib/musicState.mjs";
import ResultReferenceView, { resultSelection } from "./ResultReferenceView.js";

function requestReference({ reference_id, workspace_id, kind, version_ref, purpose, locator }) {
  return { reference_id, workspace_id, kind, ...(version_ref ? { version_ref, purpose, locator } : {}) };
}

export function companyTextPermission(snapshot, company, workspace, model, now) {
  if (snapshot?.company_id !== company) return { blocked: true, message: "暂时无法核对当前公司文字许可。输入已保留。" };
  const { policy, continuity } = snapshot;
  if (!policy?.enabled || continuity?.needs_reconfirmation || continuity?.can_confirm === false) {
    return { blocked: true, message: "当前没有可用的公司文字许可。输入已保留。" };
  }
  const expiry = Date.parse(policy.expires_at);
  if (!Number.isFinite(expiry)) return { blocked: true, message: "无法确认公司文字许可的有效期。输入已保留。" };
  if (now >= expiry) return { blocked: true, message: "公司文字许可已过期。续期后可继续，输入已保留。" };
  if (!policy.workspace_ids?.includes(workspace) || !policy.models?.some((item) => item.model_key === model)) {
    return { blocked: true, message: "当前工作空间或模型不在公司文字许可范围内。输入已保留。" };
  }
  return { blocked: false, message: expiry - now <= 5 * 60 * 1000 ? "公司文字许可将在 5 分钟内到期，可提前续期。" : "" };
}

function renewalDraftKey({ tenant_id, company_id, conversation_id, owner_ref }) {
  return `curis.employee.discussion.renewal.${JSON.stringify([tenant_id, company_id, conversation_id, owner_ref])}`;
}

export function MusicResearchResult({ item }) {
  const recommendation = item.recommendation;
  return <div>
    {item.evidence_summary && <p>研究证据：{item.evidence_summary}</p>}
    <p><a href={item.source.url} target="_blank" rel="noreferrer">查看原公开来源</a> · <time dateTime={item.source.captured_at}>{item.source.captured_at}</time></p>
    <p className="break-all">快照校验值：{item.source.snapshot_sha256}</p>
    <p className="break-all">证据版本：{item.evidence_version}</p>
    {item.metrics?.map((metric, index) => <div key={index}>
      <p>{metric.label} · {metric.value} {metric.unit} · {metric.period} · {metric.population}</p>
      <blockquote className="whitespace-pre-wrap">{metric.source_quote}</blockquote>
    </div>)}
    {item.limitations && <p className="whitespace-pre-wrap">证据适用限制：{item.limitations}</p>}
    <p className="whitespace-pre-wrap">负责人建议：{item.opportunity_summary}</p>
    {recommendation && <>
      <p>短视频：{recommendation.short_video.suitability}。假设：{recommendation.short_video.hypothesis}</p>
      <p>流媒体试听：{recommendation.streaming_preview.suitability}。假设：{recommendation.streaming_preview.hypothesis}</p>
      <p>建议先测试{recommendation.preferred_channel === "short_video" ? "短视频" : "流媒体试听"}。{recommendation.rationale}</p>
      <p>七天测试步骤</p>
      <ol className="list-decimal pl-5">{recommendation.seven_day_test.steps.map(step => <li key={step}>{step}</li>)}</ol>
      <p>观察指标：{recommendation.seven_day_test.metrics.join("、")}</p>
      <p>判定规则：{recommendation.seven_day_test.decision_rule}</p>
      <p>建议适用限制：{recommendation.limitations}</p>
    </>}
  </div>;
}

const marketMetricFields = [
  ["label", "指标", 200], ["value", "数值", 100], ["unit", "单位", 100],
  ["period", "时期", 200], ["population", "样本与口径", 500], ["source_quote", "原文引句", 1000],
];

function snapshotText(value) {
  if (typeof value === "string") return value;
  return value && typeof value === "object" ? Object.values(value).map(snapshotText).filter(Boolean).join("\n\n") : "";
}

function MarketSourceReview({ source, blocked, onAccepted }) {
  const [count, setCount] = useState(1);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const pending = useRef(false), request = useRef(null);
  const text = snapshotText(source.snapshot?.result);
  async function accept(event) {
    event.preventDefault();
    if (blocked || pending.current || !text) return;
    const form = new FormData(event.currentTarget);
    if (!form.has("reviewed")) return;
    const metrics = Array.from({ length: count }, (_, index) => Object.fromEntries(
      marketMetricFields.map(([key]) => [key, String(form.get(`${key}-${index}`) || "").trim()]),
    ));
    const limitations = String(form.get("limitations") || "").trim();
    if (!limitations || metrics.some(metric => Object.values(metric).some(value => !value))) {
      setError("请填写每项指标、原文引句和适用限制。");
      return;
    }
    const { work_ref, task_ref, artifact_ref, result_version, snapshot_sha256 } = source;
    const payload = { task_ref, artifact_ref, result_version, snapshot_sha256, reviewed: true, metrics, limitations };
    request.current = stableRequest(request.current, "accept-market-evidence", work_ref, payload, () => crypto.randomUUID());
    pending.current = true;
    setSaving(true);
    setError("");
    try {
      const saved = await musicApi.acceptResearchSource(work_ref, { ...payload, request_id: request.current.request_id });
      if (saved?.work_ref !== work_ref || !saved.evidence_ref || !/^[a-f0-9]{64}$/.test(saved.evidence_version)) {
        throw new Error("证据接受回执待核对，请重新读取原研究交付。");
      }
      onAccepted();
    } catch (reason) {
      setError(reason.message || "暂时无法确认原市场证据。");
    } finally {
      pending.current = false;
      setSaving(false);
    }
  }
  return <form onSubmit={accept}>
    <p>待核对的原快照 · {source.source_url}</p>
    <p className="break-all"><time dateTime={source.captured_at}>{source.captured_at}</time> · {source.snapshot_sha256}</p>
    <pre className="max-h-64 overflow-auto whitespace-pre-wrap">{text || "原快照没有可核对的文字。"}</pre>
    {Array.from({ length: count }, (_, index) => <fieldset key={index} disabled={blocked || saving}>
      <legend>指标 {index + 1}</legend>
      {marketMetricFields.map(([key, label, limit]) => <label key={key} className="block">
        {label} <input required name={`${key}-${index}`} maxLength={limit} className="w-full text-ui-1" />
      </label>)}
    </fieldset>)}
    <button type="button" disabled={blocked || saving || count >= 12} onClick={() => setCount(count + 1)}>添加指标</button>
    {count > 1 && <button type="button" disabled={blocked || saving} onClick={() => setCount(count - 1)}>移除最后一项</button>}
    <label className="block">适用限制 <textarea required name="limitations" maxLength={2000} disabled={blocked || saving} /></label>
    <label className="block"><input required type="checkbox" name="reviewed" disabled={blocked || saving} /> 我已核对原文、指标口径和适用限制</label>
    <button type="submit" className="text-ui-primary" disabled={blocked || saving || !text}>接受原市场证据</button>
    {error && <p role="alert">{error}</p>}
  </form>;
}

function MusicResearchDelivery({ company, receipt, workspace, blocked }) {
  const [delivery, setDelivery] = useState(null);
  const [source, setSource] = useState(null);
  const [readiness, setReadiness] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const pending = useRef(false);
  const mounted = useRef(true);
  useEffect(() => { mounted.current = true; return () => { mounted.current = false; }; }, []);
  async function readDelivery(execute = false, hosts = null) {
    if (pending.current) return;
    if (execute && (blocked || !(delivery?.can_continue_research || (delivery?.can_start_research && readiness?.ready === true)))) return;
    if (hosts && (blocked || !delivery?.can_start_research || !readiness?.can_set_browser_scope)) return;
    pending.current = true;
    setLoading(true);
    setError("");
    try {
      if (execute) {
        const result = await executeOriginalAgentWork(receipt.work_ref);
        if (result?.work?.entity_id !== receipt.work_ref) throw new Error("研究执行回执与原对话不一致。");
        if (mounted.current && result.execution_blocked) setError(result.execution_blocked);
      }
      if (hosts) await musicApi.setResearchBrowserScope(receipt.work_ref, hosts);
      const data = await musicApi.researchDelivery(company, workspace, receipt.conversation_ref, receipt.work_ref);
      if (data.conversation_ref !== receipt.conversation_ref || data.research_work_ref !== receipt.work_ref) {
        throw new Error("研究回执与原对话不一致。");
      }
      const status = data.can_start_research ? await musicApi.researchReadiness(receipt.work_ref) : null;
      if (status && status.work_ref !== receipt.work_ref) throw new Error("研究准备状态与原工作不一致。");
      if (mounted.current) { setDelivery(data); setReadiness(status); }
    } catch (reason) {
      if (mounted.current) {
        if (!hosts) { setDelivery(null); setReadiness(null); }
        setError(reason.message || "暂时无法读取研究交付。");
      }
    } finally {
      pending.current = false;
      if (mounted.current) setLoading(false);
    }
  }
  async function openSource(candidate) {
    if (pending.current || blocked) return;
    pending.current = true;
    setLoading(true);
    setSource(null);
    setError("");
    try {
      const preview = await musicApi.researchSource(candidate);
      if (preview?.root_work_ref !== receipt.work_ref || preview.work_ref !== candidate.work_ref
          || preview.task_ref !== candidate.task_ref || preview.artifact_ref !== candidate.artifact_ref
          || preview.content_verification !== "UNVERIFIED") {
        throw new Error("来源快照与原研究回执不一致。");
      }
      if (mounted.current) setSource(preview);
    } catch (reason) {
      if (mounted.current) setError(reason.message || "暂时无法读取原研究快照。");
    } finally {
      pending.current = false;
      if (mounted.current) setLoading(false);
    }
  }
  const candidates = delivery?.market_review_sources || [];
  const reviewSource = source && candidates.some(item => item.work_ref === source.work_ref
    && item.task_ref === source.task_ref && item.artifact_ref === source.artifact_ref) ? source : null;
  return <div>
    <button type="button" className="text-ui-primary" disabled={loading} onClick={() => readDelivery()}>读取研究交付</button>
    {readiness?.can_set_browser_scope && <form onSubmit={event => {
      event.preventDefault();
      const value = new FormData(event.currentTarget).get("hosts");
      const hosts = Array.from(new Set(String(value || "").split(/[\s,]+/).filter(Boolean)));
      if (hosts.length) readDelivery(false, hosts);
    }}>
      <label className="block">允许研究员工访问的公开域名（每行一个，最多八个）
        <textarea name="hosts" key={JSON.stringify(readiness.hosts)} defaultValue={(readiness.hosts || []).join("\n")}
          required disabled={loading || blocked} />
      </label>
      <button type="submit" className="text-ui-primary" disabled={loading || blocked}>保存研究范围</button>
    </form>}
    {readiness?.blockers?.map((reason, index) => <p role="status" key={`${reason.code}:${index}`}>{reason.message}</p>)}
    {delivery?.can_start_research && <button type="button" className="ml-2 text-ui-primary"
      disabled={loading || blocked || readiness?.ready !== true} onClick={() => readDelivery(true)}>启动原研究工作</button>}
    {delivery?.market_review_required && <p role="status">请核对并接受原研究的市场证据。</p>}
    {candidates.map(item => <button key={item.artifact_ref} type="button" className="text-ui-primary"
      disabled={loading || blocked} onClick={() => openSource(item)}>读取原快照</button>)}
    {reviewSource && <MarketSourceReview key={`${reviewSource.artifact_ref}:${reviewSource.result_version}`}
      source={reviewSource} blocked={blocked || loading} onAccepted={() => { setSource(null); readDelivery(); }} />}
    {delivery?.can_continue_research && <button type="button" className="ml-2 text-ui-primary"
      disabled={loading || blocked} onClick={() => readDelivery(true)}>请负责人汇总已接受的证据</button>}
    {error && <p role="alert">{error}</p>}
    {delivery && !delivery.can_start_research && !delivery.market_review_required && !delivery.can_continue_research && !delivery.deliveries.length
      && <p role="status">尚未收到引用正式市场证据的负责人建议。</p>}
    {delivery?.deliveries.map(item => <MusicResearchResult key={item.evidence_ref} item={item} />)}
    {delivery?.planning_receipts?.map(item => <p role="status" key={item.work_ref}>已创建歌曲策划工作。工作编号：{item.work_ref}</p>)}
    {(delivery?.deliveries.length > 0 || delivery?.planning_receipts.length > 0) && <a className="text-ui-primary"
      href={`${operatingHref(workspace, { view: "direction" })}&${new URLSearchParams({
        research_conversation: receipt.conversation_ref, research_work: receipt.work_ref,
      })}`}>进入音乐工作台查看策划</a>}
  </div>;
}

export default function EmployeeConversation({ companyId, employee, conversationId, businessReturn, embedded = null, active = true, blocked = false }) {
  const [view, setView] = useState(null);
  const [musicCatalog, setMusicCatalog] = useState(null);
  const hasResearchReceipts = Boolean(!embedded && view?.research_work_receipts?.length);
  useEffect(() => {
    if (!hasResearchReceipts || !companyId) return;
    let active = true;
    getCanonicalBusinesses(companyId).then(data => {
      if (active && data.company_id === companyId) setMusicCatalog(data);
    }).catch(() => { if (active) setMusicCatalog(null); });
    return () => { active = false; };
  }, [companyId, hasResearchReceipts]);
  const [error, setError] = useState("");
  const [received, setReceived] = useState({});
  const receiving = useRef(false);
  const confirmingResearch = useRef(false);
  const receiveContext = useRef("");
  const [readState, setReadState] = useState("loading");
  const [input, setInput] = useState("");
  const [assignment, setAssignment] = useState("");
  const [busy, setBusy] = useState(false);
  const [options, setOptions] = useState([]);
  const [selected, setSelected] = useState([]);
  const [workMode, setWorkMode] = useState("discussion");
  const modeRef = useRef("discussion");
  const [result, setResult] = useState(null);
  const request = useRef(null), epoch = useRef(0), sending = useRef(false), cache = useRef(null);
  const restoredAssignment = useRef("");
  const [topic, setTopic] = useState(conversationId || ""), [hydrated, setHydrated] = useState(false);
  const [uncertain, setUncertain] = useState(false), [expanded, setExpanded] = useState(false);
  const [permission, setPermission] = useState(null), [permissionClock, setPermissionClock] = useState(Date.now);
  const workspaceId = embedded?.workspaceId, contextKey = embedded?.contextKey;
  const receiptContext = JSON.stringify([companyId, workspaceId, contextKey, embedded?.objectRef]);
  receiveContext.current = receiptContext;
  const isActive = active && (!embedded?.showBar || expanded);
  const modelKey = (item) => embedded ? `${item.source}:${item.model_key}` : item.binding_id || `${item.source}:${item.model_key}`;
  const employeeRef = employee?.employee_ref || employee?.id;
  const employeeName = employee?.name || "员工";
  const [modelBinding, setModelBinding] = useState("");
  const [modelStale, setModelStale] = useState(false);
  const executionModels = view?.execution_models || [];
  const hasAgent = Boolean(employeeRef && view?.execution_agents?.length);
  const missingAgentSource = Boolean(embedded && !embedded.agentSource);
  const agentMode = hasAgent && !missingAgentSource && workMode === "agent";
  modeRef.current = agentMode ? "agent" : "discussion";
  const chooseModel = useCallback((bindingId) => { setModelBinding(bindingId); setModelStale(false); }, []);
  useEffect(() => { setModelBinding(""); setModelStale(false); }, [employeeRef]);
  useEffect(() => {
    if (!employeeRef || !modelBinding) { setModelStale(false); return; }
    if (!executionModels.some((item) => modelKey(item) === modelBinding)) {
      setModelStale(true);
      setModelBinding("");
    } else { setModelStale(false); }
  }, [employeeRef, modelBinding, executionModels]);
  const selectionFor = useCallback((assignmentRef) => {
    if (!employeeRef || !modelBinding) return undefined;
    const model = executionModels.find((item) => modelKey(item) === modelBinding);
    const workspaceId = (view?.assignments || []).find((item) => item.assignment_ref === assignmentRef)?.workspace_id;
    if (!model || !workspaceId) return null;
    return { purpose: "CONVERSATION_REPLY", binding_id: model.binding_id,
      scope: { company_id: companyId, workspace_id: workspaceId },
      model: { source: model.source, model_key: model.model_key } };
  }, [employeeRef, modelBinding, executionModels, view?.assignments, companyId]);
  const conversationHref = view?.conversation_id ? `/ceo-office/conversation?conversation_id=${encodeURIComponent(view.conversation_id)}` : "";
  const fullConversationHref = conversationHref && businessReturn
    ? `${conversationHref}&${new URLSearchParams({ return_to: businessReturn.href, return_kind: businessReturn.kind })}`
    : conversationHref;
  const receiveResult = async (message) => {
    if (receiveContext.current !== receiptContext || receiving.current || blocked || !embedded?.receiveReady || !view?.conversation_id) return;
    const original = embedded.agentSource;
    const fields = original?.kind === "writing" ? ["kind", "book_ref", "chapter_ref", "expected_draft_ref"]
      : original?.kind === "content-growth" ? ["kind", "content_ref", "expected_version_ref"] : ["kind", "song_ref", "expected"];
    const source = Object.fromEntries(fields.map(key => [key, original?.[key]]));
    receiving.current = true; setBusy(true); setError("");
    try {
      await receiveConversationResult(companyId, view.conversation_id, { workspace_id: workspaceId, message_ref: message.message_id, source });
      if (receiveContext.current !== receiptContext) return;
      setReceived(value => ({ ...value, [message.message_id]: true }));
      await embedded.onAgentCandidate?.();
    } catch (reason) { if (receiveContext.current === receiptContext) setError(reason.message || "送回未确认；请重新读取原对象，勿重复生成回复。"); }
    finally { receiving.current = false; setBusy(false); }
  };
  const load = useCallback(async () => {
    const generation = epoch.current;
    setReadState("loading");
    try {
      let value = conversationId ? await getConversation(companyId, conversationId) : await getEmployeeConversation(companyId, employeeRef);
      if (generation !== epoch.current) return;
      if (employeeRef && ![value.owner_ref, value.employee?.id].includes(employeeRef)) throw new Error("Employee mismatch");
      if (embedded) {
        if (value.company_id !== companyId || !value.tenant_id) throw new Error("Conversation scope missing");
        const storageKey = `curis.employee.discussion.${JSON.stringify([value.tenant_id, companyId, workspaceId, contextKey, employeeRef])}`;
        let saved = null;
        if (cache.current !== storageKey) {
          try { saved = JSON.parse(localStorage.getItem(storageKey) || "null"); } catch {}
          cache.current = storageKey;
          setInput(typeof saved?.input === "string" ? saved.input : "");
          setSelected(Array.isArray(saved?.selected) ? saved.selected : []);
          setModelBinding(saved?.model || ""); request.current = saved?.request || null;
          setUncertain(Boolean(saved?.request)); setTopic(saved?.topic || "");
        }
        const matchingTopics = (value.discussion_topics || []).filter((item) => item.workspace_id === workspaceId
          && (item.object_ref || null) === (embedded.objectRef || null)
          && (!embedded.assignmentRef || item.assignment_ref === embedded.assignmentRef));
        if (matchingTopics.length > 1) throw new Error("Ambiguous scoped discussion");
        const topicId = saved?.topic || topic || matchingTopics[0]?.conversation_id;
        if (topicId && topicId !== topic) setTopic(topicId);
        if (topicId) {
          value = await getConversation(companyId, topicId);
          if (generation !== epoch.current) return;
          if (value.company_id !== companyId || value.owner_ref !== employeeRef
            || value.discussion_scope?.workspace_id !== workspaceId || (value.discussion_scope?.object_ref || null) !== (embedded.objectRef || null)
            || value.messages.some((m) => m.context?.workspace_id && m.context.workspace_id !== workspaceId)) throw new Error("Topic scope mismatch");
          if (request.current?._phase === "CREATING") {
            request.current = { ...request.current, _phase: "READY" }; setUncertain(false);
          }
        } else value = { ...value, conversation_id: "", messages: [], attempts: [] };
        value = { ...value, assignments: (value.assignments || []).filter((item) => item.workspace_id === workspaceId
          && (!embedded.assignmentRef || item.assignment_ref === embedded.assignmentRef)) };
      } else if (!cache.current && value.tenant_id && value.company_id === companyId && value.owner_ref === employeeRef
        && value.execution_readiness?.some((item) => item.company_text)) {
        cache.current = renewalDraftKey(value);
        try {
          const draft = JSON.parse(sessionStorage.getItem(cache.current) || "null");
          if (typeof draft?.input === "string" && value.assignments.some((item) => item.assignment_ref === draft.assignment)) {
            sessionStorage.removeItem(cache.current);
            restoredAssignment.current = draft.assignment;
            setInput(draft.input); setSelected(Array.isArray(draft.selected) ? draft.selected : []);
            setModelBinding(draft.model || ""); setAssignment(draft.assignment);
          }
        } catch {}
      }
      if (generation !== epoch.current) return;
      setView(value); setError("");
      setAssignment((current) => value.assignments.some((item) => item.assignment_ref === current) ? current : value.assignments.length === 1 ? value.assignments[0].assignment_ref : "");
      const originalMessage = value.messages?.find((m) => m.idempotency_key === request.current?.request_id);
      const attempt = value.attempts?.findLast((a) => a.message_id === originalMessage?.message_id);
      if (attempt && ["COMPLETED", "FAILED"].includes(attempt.status) && attempt.effect_status !== "UNKNOWN") setUncertain(false);
      if (attempt?.status === "COMPLETED" && attempt.effect_status !== "UNKNOWN" && request.current) {
        const sent = request.current.body; request.current = null;
        setInput((current) => current.trim() === sent ? "" : current);
      }
      setHydrated(true);
      setReadState("ready");
    } catch { if (generation !== epoch.current) return; setReadState("error"); setError("暂时无法读取这位员工的对话，请重新读取。已有记录不会被删除。"); }
  }, [companyId, employeeRef, conversationId, workspaceId, contextKey, embedded?.assignmentRef, embedded?.objectRef, topic]);
  async function confirmResearch(message) {
    if (confirmingResearch.current || sending.current || busy || running || blocked || embedded
      || readState !== "ready" || !view?.conversation_id) return;
    const generation = epoch.current;
    confirmingResearch.current = true;
    setBusy(true);
    setError("");
    try {
      await confirmConversationResearchWork(companyId, { employeeRef, conversationId }, {
        message_ref: message.message_id, proposal_version: message.research_proposal.version,
      });
      if (generation === epoch.current) await load();
    } catch {
      if (generation === epoch.current) {
        setReadState("error");
        setError("研究工作尚未确认创建。请重新读取原对话，核对是否已有工作回执。");
      }
    } finally {
      if (generation === epoch.current) {
        confirmingResearch.current = false;
        setBusy(false);
      }
    }
  }
  useEffect(() => {
    epoch.current += 1; cache.current = null; request.current = null; sending.current = false; restoredAssignment.current = "";
    confirmingResearch.current = false; setBusy(false);
    setView(null); setInput(""); setSelected([]); setTopic(conversationId || ""); setHydrated(false); setUncertain(false);
    modeRef.current = "discussion"; setWorkMode("discussion");
    return () => { epoch.current += 1; };
  }, [companyId, employeeRef, conversationId, workspaceId, contextKey]);
  useEffect(() => { if (isActive && !blocked) load(); }, [load, isActive, blocked]);
  useEffect(() => {
    if (!embedded || !hydrated || !cache.current) return;
    try { localStorage.setItem(cache.current, JSON.stringify({ input, selected, model: modelBinding, topic, request: request.current })); } catch {}
  }, [embedded, hydrated, input, selected, modelBinding, topic, busy, uncertain]);
  useEffect(() => {
    if (!embedded || modelBinding || modelStale) return;
    const preferred = executionModels.find((m) => m.model_key === view?.model_preference?.model_key);
    if (preferred) setModelBinding(modelKey(preferred));
  }, [embedded, executionModels, view?.model_preference, modelBinding, modelStale]);
  useEffect(() => {
    let active = true;
    if (!embedded && !restoredAssignment.current) setSelected([]);
    if (restoredAssignment.current === assignment) restoredAssignment.current = "";
    setOptions([]);
    if (assignment) getEmployeeConversationReferences(companyId, employeeRef, assignment)
      .then((value) => { if (active) setOptions(value.references || []); })
      .catch(() => { if (active) setError("当前来源暂时无法读取，可以不加引用继续讨论。"); });
    return () => { active = false; };
  }, [assignment, companyId, employeeRef]);
  const runningAttempt = view?.attempts?.find((item) => item.status === "RUNNING");
  const readiness = view?.execution_readiness?.find((item) => item.assignment_ref === assignment);
  const companyText = !agentMode && Boolean(readiness?.company_text);
  const assignmentWorkspace = view?.assignments?.find((item) => item.assignment_ref === assignment)?.workspace_id;
  const permissionModel = selectionFor(assignment)?.model.model_key || view?.model_preference?.model_key;
  const permissionNotice = companyText && permission && assignmentWorkspace && permissionModel
    ? companyTextPermission(permission, companyId, assignmentWorkspace, permissionModel, permissionClock) : null;
  useEffect(() => {
    if (!companyText || !isActive || blocked) return;
    let cancelled = false;
    const refresh = () => getCompanyTextPolicy(companyId).then((snapshot) => {
      if (!cancelled) { setPermission(snapshot); setPermissionClock(Date.now()); }
    }).catch(() => { if (!cancelled) setPermission(null); });
    refresh();
    window.addEventListener("focus", refresh);
    const timer = setInterval(() => setPermissionClock(Date.now()), 30_000);
    return () => { cancelled = true; clearInterval(timer); window.removeEventListener("focus", refresh); };
  }, [companyText, companyId, isActive, blocked]);
  const running = Boolean(runningAttempt);
  const runningNotice = runningAttempt?.credential_wait === "LONG_WAIT"
    ? "模型凭据核对已等待较久，原请求结果仍待确认。可重新读取状态，请勿重复发送。"
    : runningAttempt?.credential_wait === "WAITING"
      ? "正在核对模型凭据，等待系统返回。"
      : "已接收原请求，正在处理并等待回复。";
  useEffect(() => {
    if (!running || !isActive) return undefined;
    const timer = setInterval(load, 2000);
    return () => clearInterval(timer);
  }, [running, load, isActive]);
  async function recoverTopic() {
    if (!embedded || topic || request.current?._phase !== "CREATING" || sending.current) return;
    const generation = epoch.current, original = request.current;
    sending.current = true; setBusy(true);
    try {
      const created = await createConversation(companyId, { request_id: `topic:${original.request_id}`,
        title: (embedded.title || "当前工作讨论").slice(0, 120), employee_ref: employeeRef,
        discussion_scope: { workspace_id: workspaceId, object_ref: embedded.objectRef || null, assignment_ref: original.assignment_ref } });
      if (generation !== epoch.current) return;
      request.current = { ...original, _phase: "READY" };
      localStorage.setItem(cache.current, JSON.stringify({ input, selected, model: modelBinding, topic: created.conversation_id, request: request.current }));
      setTopic(created.conversation_id); setUncertain(false); setError("讨论入口已恢复。原输入保留，请明确发送后继续。");
    } catch { if (generation === epoch.current) setError("讨论入口仍未确认。原请求保留，没有重新发送文字。"); }
    finally { if (generation === epoch.current) { sending.current = false; setBusy(false); } }
  }
  async function send(event, retry = false) {
    event.preventDefault();
    if ((!retry && !input.trim()) || sending.current || confirmingResearch.current || busy || running || uncertain || blocked || unresolved || (employeeRef && !assignment)) return;
    const generation = epoch.current;
    const body = input.trim();
    const references = selected.map(requestReference);
    let nextRequest = request.current;
    let selection = retry ? undefined : selectionFor(assignment);
    if (employeeRef && selection === null) {
      setError("之前选择的模型已不可用（可能已停用）。请重新选择模型后再发送；输入已保留。");
      return;
    }
    if (retry) {
      const original = view.messages.find((message) => message.message_id === latest.message_id);
      if (!original) return;
      const prior = latest.execution_selection;
      if (prior) {
        if (!executionModels.some((item) => item.binding_id === prior.binding_id
          && item.source === prior.model?.source && item.model_key === prior.model?.model_key)) {
          setError("上次使用的模型已不可用。请先重新选择模型，再重试原消息。");
          return;
        }
        selection = { purpose: "CONVERSATION_REPLY", binding_id: prior.binding_id,
          scope: { company_id: companyId, workspace_id: prior.scope?.workspace_id },
          model: { source: prior.model.source, model_key: prior.model.model_key } };
      }
      nextRequest = { body: original.body, assignment_ref: original.context.assignment_ref,
        references: original.references.map(requestReference),
        request_id: original.idempotency_key, retry_no: 1, ...(selection ? { execution_selection: selection } : {}) };
    } else if (!request.current || request.current.body !== body || request.current.assignment_ref !== assignment
      || JSON.stringify(request.current.references) !== JSON.stringify(references)
      || JSON.stringify(request.current.execution_selection || null) !== JSON.stringify(selection || null)) {
      nextRequest = { body, assignment_ref: assignment, references, request_id: crypto.randomUUID(),
        ...(selection ? { execution_selection: selection } : {}) };
    }
    sending.current = true; setBusy(true); setError("");
    if (companyText) {
      const snapshot = await getCompanyTextPolicy(companyId).catch(() => null);
      if (generation !== epoch.current) return;
      setPermission(snapshot); setPermissionClock(Date.now());
      const permit = companyTextPermission(snapshot, companyId, selection?.scope.workspace_id || assignmentWorkspace,
        selection?.model.model_key || permissionModel, Date.now());
      if (permit.blocked) {
        sending.current = false; setBusy(false); setError(permit.message);
        return;
      }
    }
    request.current = nextRequest;
    if (embedded && cache.current) {
      request.current = { ...request.current, _phase: topic ? "SENDING" : "CREATING" };
      try { localStorage.setItem(cache.current, JSON.stringify({ input, selected, model: modelBinding, topic, request: request.current })); }
      catch { sending.current = false; setBusy(false); setError("无法保存原请求，请恢复本地存储后再发送。输入仍保留。"); return; }
    }
    try {
      let value;
      if (embedded) {
        let topicId = topic;
        if (!topicId) {
          const created = await createConversation(companyId, { request_id: `topic:${request.current.request_id}`, title: (embedded.title || "当前工作讨论").slice(0, 120), employee_ref: employeeRef, discussion_scope: { workspace_id: workspaceId, object_ref: embedded.objectRef || null, assignment_ref: assignment } });
          if (generation !== epoch.current) return;
          topicId = created.conversation_id; setTopic(topicId);
          request.current = { ...request.current, _phase: "SENDING" };
          localStorage.setItem(cache.current, JSON.stringify({ input, selected, model: modelBinding, topic: topicId, request: request.current }));
        }
        const { _phase, ...payload } = request.current;
        value = await sendConversation(companyId, topicId, payload);
        value = { ...value, assignments: (value.assignments || []).filter((a) => a.workspace_id === workspaceId) };
      } else if (conversationId) value = await sendConversation(companyId, conversationId, request.current);
      else { await openEmployeeConversation(companyId, employeeRef); value = await sendEmployeeConversation(companyId, employeeRef, request.current); }
      if (generation !== epoch.current) return;
      setView(value);
      if (!employeeRef) { setInput(""); request.current = null; }
      // Retain input until a real successful Employee reply is observed.
    } catch (sendError) {
      if (generation !== epoch.current) return;
      setUncertain(!sendError?.status || sendError.status >= 500);
      setError(sendError?.status === 409
        ? "当前责任、模型或公司文字许可已变化。请重新读取状态并核对；输入已保留，不会重复发送。"
        : sendError?.status === 404
          ? "当前责任或员工绑定不可用。请检查这位员工的工作范围、当前模型与公司文字许可；输入已保留。"
          : "消息暂未确认接手。输入已保留，请先重新读取状态，避免重复发送。");
    }
    finally { if (generation === epoch.current) { sending.current = false; setBusy(false); } }
  }
  const latest = view?.attempts?.at(-1);
  const unresolved = Boolean(latest && (["UNVERIFIED", "UNKNOWN"].includes(latest.status) || latest.effect_status === "UNKNOWN"));
  const readyReason = readiness?.status === "UNAVAILABLE" ? readiness.reason : "";
  const permissionHref = `/ceo-office/settings?${new URLSearchParams({ tab: "company", ...(businessReturn ? { return_to: businessReturn.href, return_kind: businessReturn.kind } : {}) })}`;
  function keepDraftForRenewal(event) {
    if (embedded || !cache.current || !input.trim() || request.current?.body === input.trim()) return;
    try { sessionStorage.setItem(cache.current, JSON.stringify({ input, selected, model: modelBinding, assignment })); }
    catch { event.preventDefault(); setError("无法保存输入。请保留当前页面，再从设置续期。"); }
  }
  const canRetry = latest?.status === "FAILED" && !latest.retry_no && !unresolved
    && (!latest.execution_selection?.grant?.policy_revision || latest.recovery_basis === "NO_EXECUTOR_LAUNCH");
  const sourceLabel = { writing: "章节正文选段", "content-growth": "内容正文片段或镜头范围", music: "歌词片段" }[embedded?.agentSource?.kind] || "对象执行依据";
  const sourceNotice = {
    writing: "交给 Agent 前，请核对章节保存版本和正文选段；只读或过期依据不能执行。",
    "content-growth": "交给 Agent 前，请核对当前保存版本、员工责任及正文片段或镜头范围。",
    music: "交给 Agent 前，请保存歌曲当前修改并选择有效歌词片段；此处不支持按音频范围正式执行。",
  }[embedded?.agentSource?.kind] || "当前执行来源尚未核验，请返回原对象核对保存版本与有效范围。";
  const assignmentNotice = readState === "loading" ? "正在确认这次可用的责任范围…"
    : readState === "error" ? "当前责任范围暂时无法确认，请重新读取。"
      : !view?.assignments?.length ? "当前没有可用于这次回复的责任范围；已有工作安排可在员工资料中查看。"
        : !assignment ? "请选择这次讨论的责任范围；选择后再发送。"
          : "可直接讨论当前工作；引用资料和针对选段修改均为可选操作。";
  useEffect(() => {
    const original = view?.messages?.find((m) => m.idempotency_key === request.current?.request_id);
    if (latest?.status === "COMPLETED" && latest.effect_status !== "UNKNOWN" && request.current && latest.message_id === original?.message_id) {
      const completedBody = request.current.body;
      setInput((value) => value.trim() === completedBody ? "" : value);
      request.current = null; setUncertain(false);
    }
  }, [latest?.attempt_id, latest?.status]);
  return <>{embedded?.showBar && <div className="flex flex-wrap items-center gap-3 border-b border-ui-line py-3" aria-label="工作空间负责员工"><EmployeeAvatar employee={employee} /><strong>{employeeName}</strong><button type="button" aria-expanded={expanded} onClick={() => setExpanded((value) => !value)}>{expanded ? "收起讨论" : "与员工讨论"}</button></div>}<section hidden={!isActive} id={embedded ? undefined : "employee-conversation"} className="rounded-ui-md border border-ui-line bg-ui-surface" aria-label="员工对话" data-conversation-id={view?.conversation_id || ""}>
    <header className="flex flex-wrap items-center gap-3 border-b border-ui-line p-4">{employee ? <EmployeeAvatar employee={employee} /> : null}<div className="flex-1"><h2 className="font-semibold">{employeeRef ? `与${employeeName}对话` : "先记录想讨论的事情"}</h2><p className="text-ui-1 text-ui-txt-2">每次回复只使用当前授权的工作背景。</p></div>{!embedded && employeeRef ? <a className="text-ui-primary" href={`/ceo-office/conversation?employee_ref=${encodeURIComponent(view?.owner_ref || employeeRef)}`}>新话题</a> : null}{employeeRef && conversationHref ? <a className="text-ui-primary" href={`/ceo-office/organization/employees/${encodeURIComponent(employee.id || employeeRef)}?return_to=${encodeURIComponent(conversationHref)}`}>查看员工</a> : null}{!conversationId && conversationHref ? <a className="text-ui-primary" href={fullConversationHref}>打开完整对话</a> : null}</header>
    <div className="space-y-3 p-4" aria-live="polite">
      {!view && !error ? <p className="text-ui-2 text-ui-txt-2">正在读取对话…</p> : null}
      {view?.messages?.length === 0 ? <p className="text-ui-2 text-ui-txt-2">{employeeRef ? "可以直接与这位员工讨论，不需要先创建工作。" : "先记录问题，选择员工后再继续讨论。"}</p> : null}
      {view?.messages?.map((message) => {
        const proposal = !embedded && message.sender.kind === "EMPLOYEE" && message.context?.scope_type === "BUSINESS" && message.research_proposal;
        const receipt = proposal && view.research_work_receipts?.find((item) => item.conversation_ref === view.conversation_id
          && item.proposal_message_ref === message.message_id && item.proposal_version === proposal.version && item.work_ref);
        const business = receipt && musicCatalog?.company_id === companyId
          ? musicCatalog.businesses?.find(item => item.business_id === receipt.business_ref && item.company_id === companyId) : null;
        const musicWorkspaces = (business?.workspaces || []).filter(item =>
          item.business_type === "PACKAGE" && item.package_id === "com.curis.local.music"
          && item.package_version === "0.2.0" && item.workspace_id);
        return <article key={message.message_id} id={message.message_id} className="text-ui-2"><p className="font-medium">{message.sender.kind === "CEO" ? "你" : employeeName}</p><p className="whitespace-pre-wrap">{message.display_body || message.body}</p>
        {receipt ? <><p role="status">已创建研究工作。工作编号：{receipt.work_ref}</p>
          {musicWorkspaces.length === 1 && <MusicResearchDelivery key={`${receipt.work_ref}:${musicWorkspaces[0].workspace_id}`}
            company={companyId} receipt={receipt} workspace={musicWorkspaces[0].workspace_id}
            blocked={busy || running || blocked || readState !== "ready"} />}</>
          : proposal ? <button type="button" className="text-ui-primary" disabled={busy || running || blocked || readState !== "ready"}
            onClick={() => confirmResearch(message)}>确认并创建研究工作</button> : null}
        {embedded?.objectRef && message.sender.kind === "EMPLOYEE" && message.task_ref && message.provenance?.execution_selection?.purpose === "CONVERSATION_REPLY" && <div><button type="button" disabled={busy || blocked || !embedded.receiveReady || received[message.message_id]} onClick={() => receiveResult(message)}>{received[message.message_id] ? "已送回业务候选" : "送回当前工作候选"}</button><p>送回后请在候选中核对；明确采用将以这条回复替换当前正文或歌词。接收版本不是生成依据。</p></div>}
        {message.task_ref && message.sender.kind === "EMPLOYEE" && fullConversationHref && <a href={`${fullConversationHref}#${encodeURIComponent(message.message_id)}`}>打开这次回复</a>}
        {message.references?.map((reference) => ["RESULT", "ARTIFACT", "EVIDENCE"].includes(reference.kind)
          ? <button type="button" key={reference.reference_id} onClick={() => setResult(resultSelection(reference.workspace_id, reference.reference_id))} className="mr-3 text-ui-primary">{reference.title || "查看来源"} ▸</button>
          : <a key={reference.reference_id} className="mr-3 text-ui-primary" href={reference.kind === "KNOWLEDGE"
            ? `/ceo-office/knowledge/entries/${encodeURIComponent(reference.reference_id)}?return_to=${encodeURIComponent(`${conversationHref}#${message.message_id}`)}`
            : `/ceo-office/workspace?workspace_id=${encodeURIComponent(reference.workspace_id)}&return_to=${encodeURIComponent(`${conversationHref}#${message.message_id}`)}${reference.kind === "WORK" ? `#work-${encodeURIComponent(reference.reference_id)}` : ""}`}>{reference.title || "查看来源"} ▸</a>)}
      </article>;
      })}
      {embedded && !topic && uncertain && request.current?._phase === "CREATING" && <button type="button" disabled={busy} onClick={recoverTopic}>恢复原讨论入口</button>}
      {running ? <p role="status" className="text-ui-2 text-ui-txt-2">{runningNotice}</p> : null}
      {latest?.status === "FAILED" ? <p role="alert" className="text-ui-2 text-ui-red">员工这次未能回复。原消息仍保留，请检查当前模型与公司文字许可。</p> : null}
      {canRetry ? <button type="button" disabled={busy} onClick={(event) => send(event, true)} className="text-ui-primary">修复后重试原消息</button> : null}
      {unresolved || uncertain ? <p role="alert" className="text-ui-2 text-ui-amber">上次回复过程已中断，结果尚未确认；系统不会自动重复调用模型。</p> : null}
      {error ? <p role="alert" className="text-ui-2 text-ui-red">{error}</p> : null}
      <button type="button" onClick={async () => {
        const generation = epoch.current;
        await load();
        if (generation === epoch.current) await embedded?.onReload?.();
      }} className="text-ui-primary">重新读取</button>
      {result ? <ResultReferenceView companyId={companyId} selection={result} conversationReturn={businessReturn?.href || conversationHref} businessReturn={businessReturn} onClose={() => setResult(null)} /> : null}
    </div>
    {employeeRef && (!embedded || (view?.assignments?.length || 0) !== 1) ? <label className="block px-4 pb-3 text-ui-1">本次讨论的责任范围<select aria-label="本次讨论的责任范围" value={assignment} onChange={(event) => setAssignment(event.target.value)} className="ml-2 border border-ui-line bg-ui-surface p-2"><option value="">请选择当前责任</option>{view?.assignments?.map((item) => <option key={item.assignment_ref} value={item.assignment_ref}>{item.responsibility || "当前责任"}</option>)}</select></label> : null}
    {!agentMode && employeeRef && executionModels.length > 0 ? <label className="block px-4 pb-3 text-ui-1">本次回复使用的模型<select aria-label="本次回复使用的模型" value={modelBinding} onChange={(event) => chooseModel(event.target.value)} className="ml-2 max-w-80 border border-ui-line bg-ui-surface p-2"><option value="">{embedded ? "选择可用模型" : "员工默认绑定（不指定）"}</option>{executionModels.map((item) => <option key={modelKey(item)} value={modelKey(item)}>{item.display_name || item.label || item.model_key}</option>)}</select></label> : null}
    {!agentMode && employeeRef && executionModels.length === 0 && assignment ? <p className="px-4 pb-3 text-ui-1 text-ui-amber">暂无符合当前全局资格的模型，请到模型设置检查连接和启用状态；输入会保留。</p> : null}
    {!agentMode && employeeRef && view?.execution_agents?.length > 0 && <section className="px-4 pb-3 text-ui-1" aria-label="外部 Agent 执行状态"><p>已登记的外部 Agent：{view.execution_agents.map((item) => item.display_name).join("、")}</p><p className="text-ui-amber">{view.agent_execution_readiness?.reason} 当前讨论仍使用已选择的模型。</p><a href="/ceo-office/capabilities">核对执行能力</a></section>}
    {!agentMode && modelStale ? <p role="alert" className="px-4 pb-3 text-ui-1 text-ui-red">之前选择的模型绑定已失效，已恢复为员工默认绑定；如需指定请重新选择。</p> : null}
    {!agentMode && (permissionNotice?.message || readyReason || (companyText && error)) && <p role="status" className="px-4 pb-3 text-ui-1 text-ui-amber">{permissionNotice?.message || readyReason} <a href={permissionHref} onClick={keepDraftForRenewal}>核对公司文字许可</a></p>}
    {businessReturn?.href && <a className="block px-4 pb-3 text-ui-primary" href={businessReturn.href}>返回当前工作与结果</a>}
    {hasAgent && <label className="block px-4 pb-3 text-ui-1">本次与员工协作方式<select aria-label="本次与员工协作方式" value={agentMode ? "agent" : "discussion"} disabled={busy || running || uncertain || unresolved || blocked} onChange={(event) => { const mode = event.target.value; if (mode === "discussion" || (mode === "agent" && !missingAgentSource)) { modeRef.current = mode; setWorkMode(mode); } }} className="ml-2 border border-ui-line bg-ui-surface p-2"><option value="discussion">讨论与建议</option><option value="agent" disabled={missingAgentSource}>{missingAgentSource ? "正式执行请从具体对象发起" : "交给 Agent 完成工作"}</option></select></label>}
    {embedded && <aside aria-label={missingAgentSource ? "当前讨论范围" : "本次工作的当前依据"} className="mx-4 mb-3 rounded-ui-sm bg-ui-surface-2 p-3 text-ui-1"><p>{embedded.title || "当前讨论范围"}</p>{embedded.agentSource?.selection?.excerpt && <blockquote className="max-h-32 overflow-y-auto whitespace-pre-wrap">{embedded.agentSource.selection.excerpt}</blockquote>}<p>{missingAgentSource ? "当前入口用于讨论，无需选择文字范围。正式执行请进入具体对象，核对保存版本与执行依据。" : !agentMode ? "讨论不要求先选择范围；正式执行将另行核对对象依据。" : embedded.agentSourceReady ? `已准备${sourceLabel}；执行能力与许可仍需核对。` : sourceNotice}</p>{businessReturn?.href && <a href={businessReturn.href} className="text-ui-primary">{missingAgentSource ? "返回当前工作空间" : "查看原对象与版本"}</a>}</aside>}
    <ConversationComposer value={input} onChange={setInput} onSubmit={(event) => { if (modeRef.current === "agent") { event.preventDefault(); return; } return send(event); }} showSubmit={!agentMode} placeholder={agentMode ? `说明希望${employeeName}完成什么工作…` : employeeRef ? `想和${employeeName}讨论什么？` : "先写下问题，之后再邀请员工"} showVoice={!agentMode} busy={busy || running} disabled={(Boolean(employeeRef) && (readState !== "ready" || !assignment)) || unresolved || uncertain || blocked || (!agentMode && Boolean(embedded) && (!modelBinding || Boolean(readyReason)))}
      access={view?.computer_access || (employeeRef ? null : { state: "MODEL_EXECUTOR_NOT_APPLICABLE" })}
      referenceControl={<><select aria-label="选择当前工作来源" value="" disabled={selected.length >= 8} onChange={(event) => { const ref = options.find((item) => item.reference_id === event.target.value); if (ref && !selected.some((item) => item.reference_id === ref.reference_id)) setSelected([...selected, ref]); }} className="max-w-64 border border-ui-line bg-ui-surface text-ui-1"><option value="">引用当前工作或结果</option>{options.map((ref) => <option key={ref.reference_id} value={ref.reference_id}>{ref.title}</option>)}</select>{selected.map((ref) => <button key={ref.reference_id} type="button" onClick={() => setSelected(selected.filter((item) => item.reference_id !== ref.reference_id))} className="text-ui-1">{ref.title} ×</button>)}</>}
      notice={agentMode ? "输入与引用保留。请在下方核对执行能力和期望成果，再明确交给 Agent。" : !employeeRef ? "只保存你的讨论，不会自动调用模型。" : assignmentNotice} />
    {employeeRef && assignment && view?.execution_agents?.length > 0 && <div hidden={!agentMode} aria-label="正式工作与成果"><AgentWorkControl companyId={companyId}
      tenantId={view.tenant_id} workspaceId={workspaceId || view.assignments?.find((item) => item.assignment_ref === assignment)?.workspace_id}
      assignmentRef={assignment} agents={view.execution_agents} readiness={view.agent_execution_readiness} body={input}
      contextKey={contextKey || view.conversation_id}
      source={embedded?.agentSource
        ? { ...embedded.agentSource, ...(Array.isArray(embedded.agentSource.references) ? { references: [...embedded.agentSource.references, ...selected] } : {}) }
        : { kind: "references", references: selected }}
      disabled={!agentMode || blocked || busy || running || uncertain || unresolved || (Boolean(embedded) && (!embedded.agentSourceReady || (embedded.agentSource?.kind === "writing" && selected.length > 0)))}
      returnHref={businessReturn?.href || conversationHref} businessReturn={businessReturn} onCandidate={embedded?.onAgentCandidate} /></div>}
    {embedded?.agentSource?.kind === "writing" && selected.length > 0 && <p role="status">章节 Agent 使用原选段已保存的知识依据；请先移除讨论中另选的引用，避免遗漏来源。</p>}
  </section></>;
}
