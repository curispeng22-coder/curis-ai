"use client";

import Link from "next/link";
import { d1Href, lifecycleActions, workControlKey, readWorkControl, saveWorkControl, controlTarget, controlReadbackMatches } from "../../lib/d1State.mjs";
import { useCallback, useEffect, useRef, useState } from "react";

import { RuntimeError, RuntimeLoading } from "../runtime/RuntimeStates.js";
import { TerraCard, TerraPageHead, TerraTag } from "../terra/TerraPrimitives.js";
import { TerraPaneContent } from "../terra/TerraShell.js";
import SharedConversation from "./SharedConversation.js";
import ResultReferenceView, { resultSelection, rememberResultSelection, restoreResultSelection, generalResultTitleContext } from "./ResultReferenceView.js";
import { conversationError, getConversation } from "../../lib/v1FrontendApi.js";
import {
  assignGeneralWorkspaceEmployee,
  chooseGeneralWorkspaceDecision,
  controlGeneralWorkspaceWork,
  createGeneralWorkspaceWork,
  executeGeneralWorkspaceWork,
  getGeneralWorkspace,
  getGeneralWorkspaceTeamCandidates,
  materializeGeneralWorkspaceTeam,
  reviewGeneralWorkspaceDecision,
  runtimeErrorMessage,
} from "../../lib/runtimeApi.js";

function employeeDisplayName(employee, name, fallback = "未命名员工") {
  const current = typeof name === "string" ? name.trim() : "";
  if (current && current !== "未命名员工") return name;
  const organization = employee?.organization_record;
  const verified = employee?.identity_status === "VERIFIED_EXPLICIT_BRIDGE"
    && employee.identity_bridge?.status === "VERIFIED"
    && Boolean(employee.company_employee_ref)
    && employee.identity_bridge.companyEmployeeRef === employee.company_employee_ref
    && organization?.identity_status === "VERIFIED_EXPLICIT_BRIDGE";
  return verified && typeof organization.name === "string" && organization.name.trim()
    ? organization.name : current || fallback;
}

const STATUS = {
  PLANNED: ["计划已创建", "grey"],
  READY: ["准备就绪", "grey"],
  BLOCKED: ["等待修复", "amber"],
  ACTIVE: ["责任已接续", "green"],
  RUNNING: ["正在处理", "green"],
  EXECUTING: ["正在处理", "green"],
  WAITING: ["等待核对", "amber"],
  WAITING_DECISION: ["等待你的决定", "amber"],
  PAUSED: ["已暂停", "amber"],
  FAILED: ["需要恢复", "red"],
  COMPLETED: ["已完成", "green"],
  CANCELLED: ["已停止", "grey"],
  ARCHIVED: ["已归档", "grey"],
};
const PROVENANCE = { FACT: "事实", POLICY: "规则", EVIDENCE: "证据", EST: "员工估计", UNK: "未知" };

function newKey() {
  return globalThis.crypto?.randomUUID?.() || `general-${Date.now()}`;
}

export default function GeneralWorkspaceOperating({ companyId, workspaceId, parentPath, assistant }) {
  const [view, setView] = useState({ status: "loading", data: null, error: "" });
  const [problem, setProblem] = useState("");
  const [expectedResult, setExpectedResult] = useState("");
  const [otherBusy, setBusy] = useState(false);
  const [controlBusy, setControlBusy] = useState("");
  const activeControlScope = JSON.stringify([companyId, workspaceId]);
  const busy = otherBusy || controlBusy === activeControlScope;
  const [executingWork, setExecutingWork] = useState("");
  const executionPending = useRef(false);
  const controlLock = useRef(null);
  const controlScope = useRef({ key: activeControlScope, generation: 0 });
  const [limitedWorks, setLimitedWorks] = useState(() => {
    try { const saved = JSON.parse(window.sessionStorage.getItem("curis.general.executionLimits") || "{}"); return saved && typeof saved === "object" && !Array.isArray(saved) ? saved : {}; } catch { return {}; }
  });
  const limitScope = (ref) => JSON.stringify([companyId, workspaceId, ref]);
  const [actionError, setActionError] = useState("");
  const [idempotencyKey, setIdempotencyKey] = useState(newKey);
  const [selectedResult, setSelectedResult] = useState(null);
  const [utilityRequestKey, setUtilityRequestKey] = useState(0);
  const [candidates, setCandidates] = useState([]);
  const [selectedEmployee, setSelectedEmployee] = useState("");
  const [responsibility, setResponsibility] = useState("");
  const teamAttempted = useRef(false);
  const [returnConversation, setReturnConversation] = useState(null);
  // Invalidate old network callbacks during scope render, before passive effects run.
  /* eslint-disable react-hooks/refs */
  if (controlScope.current.key !== activeControlScope) {
    controlScope.current = { key: activeControlScope, generation: controlScope.current.generation + 1 };
  }
  /* eslint-enable react-hooks/refs */
  useEffect(() => {
    let active = true;
    const href = new URLSearchParams(window.location.search).get("return_to") || "";
    if (href.startsWith("/ceo-office/conversation?conversation_id=")) {
      const id = new URL(href, window.location.origin).searchParams.get("conversation_id");
      getConversation(companyId, id).then((value) => active && setReturnConversation({ href, employee: value.owner_ref })).catch(() => {});
    }
    return () => { active = false; };
  }, [companyId, workspaceId]);

  // React setters are stable; the scope ref is intentionally captured when the request starts.
  // eslint-disable-next-line react-hooks/preserve-manual-memoization
  const refresh = useCallback(async () => {
    const context = controlScope.current;
    const current = () => controlScope.current === context;
    setView((current) => ({ ...current, status: "loading", error: "" }));
    try {
      let data = await getGeneralWorkspace(companyId, workspaceId);
      if (!current() || data.company?.company_id !== companyId || data.workspace?.workspace_id !== workspaceId) return;
      if (data.operating_readiness?.status === "NEEDS_DECISION" && !teamAttempted.current) {
        teamAttempted.current = true;
        try {
          await materializeGeneralWorkspaceTeam(companyId, workspaceId);
          data = await getGeneralWorkspace(companyId, workspaceId);
        } catch {
          // Existing truth is intentionally preserved: no role, employee or capability is invented here.
        }
      }
      if (!current()) return;
      if (data.operating_readiness?.status === "NEEDS_DECISION") {
        const candidatePayload = await getGeneralWorkspaceTeamCandidates(companyId, workspaceId);
        if (!current()) return;
        setCandidates(candidatePayload.employees || []);
        setSelectedEmployee((current) => current || candidatePayload.employees?.[0]?.employee_id || "");
      } else {
        setCandidates([]);
      }
      if (current()) setView({ status: "ready", data, error: "" });
    } catch (error) {
      if (current()) setView({ status: "error", data: null, error: conversationError(error, "当前工作暂时无法读取，请重新读取。") });
    }
  }, [companyId, workspaceId]);

  useEffect(() => { refresh(); }, [refresh]);
  useEffect(() => { setSelectedResult(restoreResultSelection()); }, [workspaceId]);

  const observing = Boolean(executingWork) || Boolean(view.data?.current_work.some((work) => ["RUNNING", "EXECUTING"].includes(work.status)));
  useEffect(() => {
    if (!observing) return undefined;
    let active = true;
    let reading = false;
    const read = async () => {
      if (reading) return;
      reading = true;
      try {
        const data = await getGeneralWorkspace(companyId, workspaceId);
        if (active) setView({ status: "ready", data, error: "" });
      } catch {
        if (active) setActionError("暂时无法读取最新进展；工作状态以重新读取的结果为准。");
      } finally { reading = false; }
    };
    read();
    const timer = window.setInterval(read, 1500);
    return () => { active = false; window.clearInterval(timer); };
  }, [companyId, workspaceId, observing]);

  async function createWork(event) {
    event.preventDefault();
    const readiness = view.data?.operating_readiness;
    if (readiness?.status !== "READY_FOR_WORK") {
      setActionError(`${readiness?.reason || "当前责任尚未明确"}。${readiness?.next_action || "请先完成准备"}。`);
      return;
    }
    setBusy(true); setActionError("");
    try {
      await createGeneralWorkspaceWork(companyId, workspaceId, {
        problem: problem.trim(), expected_result: expectedResult.trim(), constraints: [], references: [],
        idempotency_key: idempotencyKey,
      });
      setProblem(""); setExpectedResult(""); setIdempotencyKey(newKey());
      await refresh();
    } catch (error) {
      setActionError(runtimeErrorMessage(error));
    } finally {
      setBusy(false);
    }
  }

  async function execute(workRef) {
    if (readWorkControl(workControlKey(companyId, { workspaceId, work_ref: workRef }))?.pending) return;
    if (executionPending.current) return;
    executionPending.current = true;
    setExecutingWork(workRef); setActionError("");
    try {
      const selectedLimits = limitedWorks[limitScope(workRef)];
      if (selectedLimits?.held) return;
      if (selectedLimits?.selected) {
        const held = { ...limitedWorks, [limitScope(workRef)]: { selected: true, held: true } };
        setLimitedWorks(held);
        try { window.sessionStorage.setItem("curis.general.executionLimits", JSON.stringify(held)); } catch { /* Server marker still prevents replay. */ }
      }
      await executeGeneralWorkspaceWork(workRef, undefined, selectedLimits?.selected ? { max_prompt_bytes: 4096, max_output_tokens: 2048 } : null);
      await refresh();
    } catch (error) {
      setActionError(conversationError(error, "暂时没有收到处理结果，请重新读取工作进展。"));
      await refresh();
    } finally {
      executionPending.current = false;
      setExecutingWork("");
    }
  }

  async function assignEmployee(event) {
    event.preventDefault();
    if (!selectedEmployee || !responsibility.trim()) return;
    setBusy(true); setActionError("");
    try {
      await assignGeneralWorkspaceEmployee(companyId, workspaceId, {
        employee_id: selectedEmployee,
        responsibility: responsibility.trim(),
      });
      setResponsibility("");
      teamAttempted.current = true;
      await refresh();
    } catch (error) {
      setActionError(error?.message || runtimeErrorMessage(error));
    } finally { setBusy(false); }
  }

  function openResult(referenceId) {
    setActionError("");
    const selection = resultSelection(workspaceId, referenceId);
    setSelectedResult(selection); rememberResultSelection(selection);
    setUtilityRequestKey((current) => current + 1);
  }

  async function reviewDecision(workRef) {
    setBusy(true); setActionError("");
    try {
      await reviewGeneralWorkspaceDecision(companyId, workspaceId, workRef);
      await refresh();
    } catch (error) {
      setActionError(runtimeErrorMessage(error));
    } finally {
      setBusy(false);
    }
  }

async function chooseDecision(workRef, choice, reason) {
    setBusy(true); setActionError("");
    try {
      const response = await chooseGeneralWorkspaceDecision(companyId, workspaceId, workRef, { choice, reason });
      if (response.work?.data?.responsibilityRouting?.status === "ACTIVE") {
        setBusy(false);
        await execute(workRef);
      }
      await refresh();
    } catch (error) {
      setActionError(runtimeErrorMessage(error));
      await refresh();
    } finally {
      setBusy(false);
    }
  }

  async function controlWork(workRef, action, readOnly = false) {
    if (controlLock.current?.scope === activeControlScope) return;
    const original = { ...view.data?.current_work.find((item) => item.work_ref === workRef), companyId, workspaceId };
    if (!original.work_ref) return;
    const key = workControlKey(companyId, original), scope = JSON.stringify([companyId, workspaceId]);
    let pending = readWorkControl(key)?.pending;
    if (!readOnly && (pending || !lifecycleActions(original).includes(action))) return;
    const request = { scope, context: controlScope.current };
    controlLock.current = request; setControlBusy(scope); setActionError("");
    try {
      if (!readOnly) {
        const reason = { pause: "CEO 暂停当前工作", cancel: "CEO 停止当前工作", resume: "CEO 恢复原工作", archive: "CEO 归档当前工作", restore: "恢复查看原工作" }[action];
        pending = { action, reason, target: controlTarget(original, action) };
        saveWorkControl(key, { action, reason, pending });
        await controlGeneralWorkspaceWork(companyId, workspaceId, workRef, action, { reason });
      }
      // Control readback never materializes a team or checks/configures models.
      const data = await getGeneralWorkspace(companyId, workspaceId);
      if (controlScope.current !== request.context || data.company?.company_id !== companyId || data.workspace?.workspace_id !== workspaceId) throw new Error("工作来源已变化");
      const fresh = data.current_work.find((item) => item.work_ref === workRef);
      if (!fresh) throw new Error("原工作未返回");
      setView({ status: "ready", data, error: "" });
      if (pending && !controlReadbackMatches(companyId, original, { ...fresh, companyId, workspaceId }, pending)) throw new Error("原控制效果尚未匹配");
      saveWorkControl(key, null);
    } catch {
      if (controlScope.current === request.context) setActionError("控制结果尚未确认；原对象与原因已保留。只重新读取原工作，不会重复提交。");
    } finally {
      if (controlLock.current === request) {
        controlLock.current = null; setControlBusy("");
      }
    }
  }

  if (view.status === "loading" || (view.data && (view.data.company?.company_id !== companyId || view.data.workspace?.workspace_id !== workspaceId))) return <RuntimeLoading label="正在读取业务运行状态…" />;
  if (view.status === "error") return <RuntimeError message={view.error} onRetry={refresh} />;

  const data = view.data;
  const readiness = data.operating_readiness;
  const employee = assistant?.data || assistant || { name: "CEO 助理", role: "公司级协调与经营跟进" };
  const messages = [{
    role: "assistant",
    text: data.current_work.length
      ? "我会按当前责任与执行事实跟进这些工作；结果与证据会保留在同一工作空间。"
      : "告诉我这项业务现在要解决什么，以及你希望得到什么结果。",
  }];

  return <>
    <TerraPaneContent contextPane={data.current_work.length ? <nav aria-label="当前工作目录">{data.current_work.map((work) => <a key={work.work_ref} href={`#work-${work.work_ref}`} className="mb-3 block text-ui-primary">{work.problem || "当前工作"}</a>)}</nav> : null}
      utilityRequestKey={utilityRequestKey}
      utilityRequestTabId={selectedResult ? "current" : ""}
      utilityPane={selectedResult ? <ResultReferenceView companyId={companyId} selection={selectedResult} generalTitleContext={generalResultTitleContext(companyId, workspaceId, data, selectedResult)} onClose={() => { setSelectedResult(null); rememberResultSelection(null); }} /> : null} />
    <TerraPageHead
      title={data.workspace.name}
      subtitle={`${parentPath.company.name} / ${parentPath.department.name} / ${parentPath.business.name}`}
      facts={[
        { value: data.current_work.length, label: "当前工作" },
        { value: data.team.employees.length, label: "负责员工" },
        { value: data.results.length, label: "结果" },
      ]}
    />
    <div className="space-y-4">
      <div className="space-y-4">
        <TerraCard>
          <p className="text-ui-1 font-bold text-ui-primary">业务目标</p>
          <h2 className="mt-2 text-ui-5 font-semibold text-ui-txt">{data.goal || "目标尚未确认"}</h2>
          <p className="mt-2 text-ui-2 text-ui-txt-2">{data.business.positioning || "先从当前问题开始，后续再补充业务定位。"}</p>
        </TerraCard>

        <SharedConversation
          scopeKey={`${companyId}:${workspaceId}`}
          employee={employee}
          messages={messages}
          value={problem}
          onChange={setProblem}
          onSubmit={createWork}
          submitLabel="交给负责员工"
          allowWithoutModel
          busy={busy}
        >
          <label className="block rounded-xl border border-ui-line bg-ui-bg p-3 text-xs font-bold text-ui-txt-2">
            期望结果
            <textarea
              value={expectedResult}
              onChange={(event) => setExpectedResult(event.target.value)}
              rows={2}
              placeholder="例如：形成三条有证据支持的改进建议"
              className="mt-2 w-full resize-none bg-transparent text-sm font-normal text-ui-txt outline-none"
            />
          </label>
          {actionError ? <p role="alert" className="rounded-lg bg-ui-red-soft px-3 py-2 text-sm text-ui-red">{actionError}</p> : null}
        </SharedConversation>

        <section className="space-y-3" aria-label="当前工作">
          {data.current_work.map((work) => {
            const holders = work.responsibility_holder_ref
              ? data.team.employees.filter((item) => item.employee_ref === work.responsibility_holder_ref) : [];
            const holderName = employeeDisplayName(holders.length === 1 ? holders[0] : null, work.responsibility_holder_name, "尚未明确");
            const [label, color] = STATUS[work.status] || ["状态未知", "grey"];
            const scopedWork = { ...work, companyId, workspaceId };
            const controlPending = readWorkControl(workControlKey(companyId, scopedWork))?.pending;
            const terminal = ["COMPLETED", "CANCELLED", "ARCHIVED"].includes(work.status);
            const humanActive = work.human_input && !["CLOSED", "INVALIDATED"].includes(work.human_input.state);
            return <div key={work.work_ref} id={`work-${work.work_ref}`}><TerraCard>
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0 flex-1"><p className="text-ui-1 font-bold text-ui-primary">当前工作</p><h3 className="mt-1 break-words text-ui-4 font-semibold text-ui-txt">{work.problem}</h3></div>
                <TerraTag color={color} className="shrink-0 whitespace-nowrap">{label}</TerraTag>
              </div>
              <dl className="mt-4 grid gap-3 text-ui-1 sm:grid-cols-3">
                <div><dt className="text-ui-txt-3">负责人</dt><dd className="mt-1 font-bold text-ui-txt">{holderName}</dd></div>
                <div><dt className="text-ui-txt-3">当前进展</dt><dd className="mt-1 font-bold text-ui-txt">{work.current_executor_ref ? (work.execution_status === "RUNNING" ? "员工正在处理" : "员工已接手") : "当前没有员工执行"}</dd></div>
                <div><dt className="text-ui-txt-3">下一步</dt><dd className="mt-1 font-bold text-ui-txt">{work.recovery_action}</dd></div>
              </dl>
              {work.reason ? <p className="mt-3 text-ui-2 text-ui-txt-2">{work.reason}</p> : null}
              {humanActive ? <p className="mt-3 rounded-ui-sm border border-ui-amber/30 bg-ui-amber-soft p-3 text-ui-2 text-ui-txt">这项原工作正等待必要输入。请进入工作详情查看请求并报告；外部动作目前仍待核实。</p> : null}
              {work.handoffs?.map((handoff) => <p key={handoff.handoff_ref} className="mt-3 rounded-ui-sm bg-ui-surface-2 px-3 py-2 text-ui-1 text-ui-txt-2">{handoff.from_employee_name}（{handoff.from_responsibility}）已转交给 {handoff.to_employee_name}（{handoff.to_responsibility}）· {["ACKNOWLEDGED", "COMPLETED"].includes(handoff.status) ? "已接手" : "等待接手"}</p>)}
              {work.decision?.status === "WAITING_CEO" ? <section className="mt-3 rounded-ui-sm border border-ui-amber/30 bg-ui-amber-soft p-3" aria-label="CEO 决策">
                <p className="text-ui-1 font-bold text-ui-amber">需要你的决定</p>
                <p className="mt-1 text-ui-2 text-ui-txt">{work.decision.event}</p>
                <p className="mt-1 text-ui-1 text-ui-txt-2">{work.decision.cannotDecideReason}</p>
                <div className="mt-3 flex flex-wrap gap-2">
                  {work.decision.complexity === "LOW_RISK" ? <button type="button" disabled={busy} onClick={() => chooseDecision(work.work_ref, work.decision.recommendation.optionId, "按员工建议处理")} className="rounded-ui-sm bg-ui-primary px-3 py-1.5 text-ui-1 font-bold text-ui-primary-fg">按建议处理</button> : null}
                  <button type="button" disabled={busy} onClick={() => reviewDecision(work.work_ref)} className="rounded-ui-sm border border-ui-line px-3 py-1.5 text-ui-1 font-bold text-ui-txt">查看方案</button>
                  <button type="button" disabled={busy} onClick={() => chooseDecision(work.work_ref, "DEFER", "CEO 暂缓决定")} className="rounded-ui-sm border border-ui-line px-3 py-1.5 text-ui-1 font-bold text-ui-txt-2">暂缓</button>
                </div>
                {work.decision.layer1ReviewedAt ? <div className="mt-3 space-y-2 border-t border-ui-line pt-3">
                  <p className="text-ui-2 font-bold text-ui-txt">{work.decision.ceoChoicePrompt}</p>
                  {work.decision.options.map((option) => <div key={option.optionId} className="rounded-ui-sm bg-ui-bg p-3 text-ui-1">
                    <p className="font-bold text-ui-txt">{option.label}</p>
                    <p className="mt-1 text-ui-txt-2">影响：{option.impact.value}（{PROVENANCE[option.impact.provenance] || "未知"}）</p>
                    <p className="text-ui-txt-2">风险：{option.risk.value}（{PROVENANCE[option.risk.provenance] || "未知"}）</p>
                    <p className="text-ui-txt-2">代价：{option.cost.value}（{PROVENANCE[option.cost.provenance] || "未知"}）</p>
                    <button type="button" disabled={busy} onClick={() => chooseDecision(work.work_ref, option.optionId, `CEO 选择：${option.label}`)} className="mt-2 rounded-ui-sm border border-ui-line px-3 py-1.5 font-bold text-ui-primary">选择此方案</button>
                  </div>)}
                  <p className="text-ui-1 text-ui-txt-2">员工建议：{work.decision.options.find((option) => option.optionId === work.decision.recommendation.optionId)?.label} · {work.decision.recommendationReason.value}（{PROVENANCE[work.decision.recommendationReason.provenance] || "未知"}）</p>
                  <p className="text-ui-1 text-ui-txt-2">选择后：{work.decision.continuationPlan}</p>
                </div> : null}
              </section> : null}
              <div className="mt-4 flex flex-wrap items-center gap-3">
                {!terminal && !humanActive && <label className="inline-flex items-center gap-2 text-ui-1 text-ui-txt-2"><input type="checkbox" checked={Boolean(limitedWorks[limitScope(work.work_ref)]?.selected)} disabled={busy || Boolean(executingWork) || Boolean(limitedWorks[limitScope(work.work_ref)]?.held)} onChange={(event) => setLimitedWorks((current) => ({ ...current, [limitScope(work.work_ref)]: { selected: event.target.checked, held: false } }))} />仅尝试一次 · 限制模型输出长度</label>}
                {limitedWorks[limitScope(work.work_ref)]?.held && <span role="status" className="text-ui-1 text-ui-txt-2">单次请求已锁定；结果未确认时只重新读取，不再执行。</span>}
                {work.status === "ACTIVE" && !humanActive && !controlPending ? <button type="button" disabled={busy || Boolean(executingWork) || Boolean(limitedWorks[limitScope(work.work_ref)]?.held)} onClick={() => execute(work.work_ref)} className="rounded-ui-sm bg-ui-primary px-4 py-2 text-ui-1 font-bold text-ui-primary-fg disabled:opacity-40">开始处理</button> : null}
                {lifecycleActions(scopedWork).map((action) => <button key={action} type="button" disabled={busy || Boolean(controlPending)} onClick={() => controlWork(work.work_ref, action)} className="rounded-ui-sm border border-ui-line px-3 py-1.5 text-ui-1 font-bold text-ui-txt disabled:opacity-40">{{ pause: "暂停", resume: "继续工作", cancel: "停止", archive: "归档", restore: "恢复查看" }[action]}</button>)}
                {controlPending && <><span role="status">控制结果待核对 · {controlPending.reason}</span><button type="button" disabled={busy} onClick={() => controlWork(work.work_ref, controlPending.action, true)}>重新读取原工作</button></>}
                <Link href={`/ceo-office/knowledge?${new URLSearchParams({ pick_for: work.work_ref, return_to: `/ceo-office/workspace?workspace_id=${encodeURIComponent(workspaceId)}#work-${work.work_ref}` })}`} className="rounded-ui-sm border border-ui-line px-3 py-1.5 text-ui-1 font-bold text-ui-txt-2 no-underline">添加参考资料</Link>
                <Link href={d1Href({ view: "work", workRef: work.work_ref, workspaceId })} className="rounded-ui-sm border border-ui-line px-3 py-1.5 text-ui-1 font-bold text-ui-primary">查看工作详情</Link>
                <span className="text-ui-1 text-ui-txt-3">结果 {work.result_refs.length} · 证据 {work.evidence_refs.length} · 附件 {work.artifact_refs.length}</span>
              </div>
              {work.result_summaries?.length ? <div className="mt-3 flex flex-wrap gap-2">{work.result_summaries.map((result) => <button key={result.reference_id} type="button" onClick={() => openResult(result.reference_id)} className="rounded-ui-sm border border-ui-line px-3 py-1.5 text-ui-1 font-bold text-ui-primary">{result.kind === "EVIDENCE" ? "查看证据" : result.kind === "ARTIFACT" ? "查看成果" : "查看结果"} ▸</button>)}</div> : null}
            </TerraCard></div>;
          })}
        </section>
      </div>

      <section aria-label="团队与工作准备" className="space-y-4">
        <TerraCard>
          <div className="flex items-start justify-between gap-3"><div><p className="text-ui-1 font-bold text-ui-primary">运行准备</p><h2 className="mt-1 text-ui-4 font-semibold text-ui-txt">{readiness.reason}</h2></div><TerraTag color={readiness.status === "READY_FOR_WORK" ? "green" : "amber"}>{readiness.status === "READY_FOR_WORK" ? "可以开始" : "需要准备"}</TerraTag></div>
          <p className="mt-3 text-ui-2 text-ui-txt-2">负责人：{readiness.owner || "已由团队承担"}</p>
          <p className="mt-1 text-ui-2 font-bold text-ui-txt">下一步：{readiness.next_action}</p>
        </TerraCard>
        <TerraCard>
          <p className="text-ui-1 font-bold text-ui-primary">业务团队</p>
          {data.team.employees.length ? <ul className="mt-3 space-y-3">{data.team.employees.map((item) => <li key={item.employee_ref}><p className="font-bold text-ui-txt">{item.identity_status === "VERIFIED_EXPLICIT_BRIDGE" ? <Link href={returnConversation?.employee === item.employee_ref ? returnConversation.href : `/ceo-office/organization/employees/${encodeURIComponent(item.company_employee_ref)}#employee-conversation`} className="text-ui-primary hover:underline">{employeeDisplayName(item, item.name)} · 对话</Link> : employeeDisplayName(item, item.name)}</p><p className="text-ui-1 text-ui-txt-3">{item.role_name || item.responsibility || "工作空间员工"}</p></li>)}</ul> : <><p className="mt-3 text-ui-2 text-ui-txt-2">选择已招募员工并确认他在当前业务中的责任。系统只使用已验证的默认模型，不会编造能力。</p>{candidates.length ? <form onSubmit={assignEmployee} className="mt-4 space-y-3"><label className="block text-ui-1 font-bold text-ui-txt-2">员工<select value={selectedEmployee} onChange={(event) => setSelectedEmployee(event.target.value)} className="mt-1 w-full rounded-ui-sm border border-ui-line bg-ui-bg px-3 py-2 text-ui-2 font-normal text-ui-txt">{candidates.map((item) => <option key={item.employee_id} value={item.employee_id}>{item.name} · {item.role}</option>)}</select></label><label className="block text-ui-1 font-bold text-ui-txt-2">当前责任<textarea value={responsibility} onChange={(event) => setResponsibility(event.target.value)} rows={3} placeholder="例如：整理客户反馈并形成有证据的改进建议" className="mt-1 w-full resize-none rounded-ui-sm border border-ui-line bg-ui-bg px-3 py-2 text-ui-2 font-normal text-ui-txt" /></label><button type="submit" disabled={busy || !selectedEmployee || !responsibility.trim()} className="w-full rounded-ui-sm bg-ui-primary px-3 py-2 text-ui-1 font-bold text-ui-primary-fg disabled:opacity-40">加入业务团队</button></form> : <p className="mt-3 text-ui-1 text-ui-amber">尚无可选择的在岗员工。请先到人才与能力招募员工。</p>}</>}
        </TerraCard>
      </section>
    </div>
  </>;
}
