"use client";

import { useMemo, useState } from "react";
import { ConversationComposer } from "../v1/SharedConversation.js";
import { EmployeeAvatar } from "../v1/EmployeeAvatar.js";


function initials(name = "") {
  return name.trim().slice(0, 2) || "AI";
}

function accessLabel(access = {}) {
  if (access.effective_state && access.effective_state !== "UNKNOWN") return "权限已验证";
  if (access.configured_state === "CONFIGURED") return "已按允许范围配置，实际权限待确认";
  return "访问权限尚未确认";
}

function ResultReferences({ refs = [], onOpenResult }) {
  if (!refs.length) return <p className="text-ui-1 text-ui-txt-3">尚无可回访结果。</p>;
  return (
    <div className="flex flex-wrap gap-2" aria-label="工作结果">
      {refs.map((ref) => (
        <button key={ref} type="button" onClick={() => onOpenResult?.(ref)} className="rounded-ui-sm border border-ui-line px-2 py-1 text-ui-1 text-ui-accent hover:bg-ui-surface-2">
          查看结果 ▸
        </button>
      ))}
    </div>
  );
}

function Composer({ employee, onSend }) {
  const [instruction, setInstruction] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const capabilities = employee.composer?.capabilities || [];
  const enabled = typeof onSend === "function" && capabilities.some((item) => item.status === "AVAILABLE");
  async function send(event) {
    event.preventDefault();
    if (!enabled || busy || !instruction.trim()) return;
    setBusy(true); setError("");
    try { await onSend(employee, instruction.trim()); setInstruction(""); }
    catch { setError("消息尚未送达，输入已保留。请检查员工能力后重试。"); }
    finally { setBusy(false); }
  }
  const composer = employee.composer || {};
  return <><ConversationComposer value={instruction} onChange={setInstruction} onSubmit={send} busy={busy} disabled={!enabled}
    placeholder={enabled ? `告诉${employee.name}接下来要处理什么` : "当前员工尚未接入可验证的指令发送"}
    access={composer.computer_access || null}
    accessExecutor={{ modelBacked: Boolean(composer.model_backed), agentBacked: Boolean(composer.agent_backed) }}
    controls={<span className="text-ui-1 text-ui-txt-2">{composer.agent_backed ? "Agent 执行" : composer.model_backed ? "模型辅助" : "未绑定执行能力"}</span>} />
    {error ? <p role="alert" className="text-ui-1 text-ui-red">{error}</p> : null}</>;
}

export function SharedEmployeeDetail({ employee, onOpenResult }) {
  if (!employee) return <p className="text-ui-2 text-ui-txt-2">选择员工后查看详情。</p>;
  const organization = employee.organization || {};
  const companyEmployee = organization.exact_company_employee;
  const capabilities = employee.composer?.capabilities || [];
  return (
    <section aria-label={`${employee.name}员工详情`} className="space-y-4">
      <header className="flex items-center gap-3">
        <EmployeeAvatar employee={{ ...companyEmployee, ...employee }} />
        <div><h2 className="text-ui-3 font-semibold">{employee.name}</h2><p className="text-ui-2 text-ui-txt-2">{employee.role}</p></div>
      </header>
      <dl className="space-y-3 text-ui-2">
        <div><dt className="text-ui-txt-3">组织关系</dt><dd>{organization.company?.name || "当前公司"} · {companyEmployee?.primary_department?.name || organization.workspace?.name || "当前工作空间"}</dd></div>
        <div><dt className="text-ui-txt-3">长期责任</dt><dd>{employee.responsibility || "尚未记录"}</dd></div>
        <div><dt className="text-ui-txt-3">当前责任</dt><dd>{employee.current_responsibilities?.at(-1)?.activity || "当前没有进行中的责任"}</dd></div>
        <div><dt className="text-ui-txt-3">能力与工作方式</dt><dd>{capabilities.length ? capabilities.map((item) => item.name).join("、") : "尚未绑定可用能力"}</dd></div>
        <div><dt className="text-ui-txt-3">访问边界</dt><dd>{accessLabel(employee.composer?.computer_access)}</dd></div>
        <div><dt className="text-ui-txt-3">最近结果</dt><dd className="mt-1"><ResultReferences refs={employee.recent_result_refs} onOpenResult={onOpenResult} /></dd></div>
      </dl>
    </section>
  );
}

function readableResult(result) {
  const content = result.content;
  if (typeof content !== "string") return result.summary || "请展开证据与执行详情查看原始结果。";
  try {
    const structured = JSON.parse(content);
    return (typeof structured?.summary === "string" && structured.summary) || result.summary || "请展开证据与执行详情查看原始结果。";
  } catch {
    return content || result.summary || "暂无结果正文。";
  }
}

export function SharedResultUtility({ result, displayTitle }) {
  if (!result) return <p className="text-ui-2 text-ui-txt-2">从工作过程选择一个结果。</p>;
  return (
    <article className="space-y-3" aria-label="结果详情">
      <header><p className="text-ui-1 text-ui-txt-3">{{ RESULT: "工作结果", ARTIFACT: "工作成果", EVIDENCE: "证据", OUTCOME: "业务结果" }[result.kind] || "工作记录"}</p><h2 className="text-ui-3 font-semibold">{displayTitle ?? (result.title || result.summary || "工作结果")}</h2></header>
      <p className="text-ui-2 text-ui-txt-2">{{ COMPLETED: "执行已结束", FAILED: "执行未成功", AVAILABLE: "可查看" }[String(result.status).toUpperCase()] || "以原工作状态为准"} · {result.verification_status === "VERIFIED" ? "已有验证记录" : "尚未验证"}</p>
      <p className="text-ui-1 text-ui-txt-3">查看不会代替业务验收；结果与证据会保留。</p>
      <p className="max-h-[55vh] overflow-auto whitespace-pre-wrap text-ui-2 leading-relaxed">{readableResult(result)}</p>
      <details><summary className="cursor-pointer text-ui-1 text-ui-txt-2">证据与执行详情</summary><pre className="max-h-[55vh] overflow-auto whitespace-pre-wrap rounded-ui-sm bg-ui-surface-2 p-3 text-ui-1">{JSON.stringify(displayTitle === undefined ? result : { ...result, title: displayTitle, ...(Array.isArray(result.artifacts) ? { artifacts: result.artifacts.map((item) => ({ ...item, title: "工作成果" })) } : {}) }, null, 2)}</pre></details>
    </article>
  );
}

export default function SharedEmployeeWorkArea({ employees = [], onOpenEmployee, onOpenResult, onSend }) {
  const initial = useMemo(() => {
    const working = employees.filter((item) => item.ui_status?.code === "working");
    return working.length === 1 ? working[0].employee_ref : null;
  }, [employees]);
  const [expanded, setExpanded] = useState(initial);

  if (!employees.length) return <p className="py-5 text-ui-2 text-ui-txt-2">当前工作空间还没有已任命的 AI 员工。</p>;
  return (
    <section aria-label="工作区" className="divide-y divide-ui-line border-y border-ui-line">
      {employees.map((employee) => {
        const open = expanded === employee.employee_ref;
        const work = employee.current_execution || employee.current_responsibilities?.at(-1);
        return (
          <article key={employee.employee_ref}>
            <div className="grid grid-cols-[auto_minmax(0,1fr)_auto_auto] items-center gap-3 py-3">
              <button type="button" aria-label={`查看${employee.name}详情`} onClick={() => onOpenEmployee?.(employee.employee_ref)} className="row-span-2 grid h-8 w-8 place-items-center rounded-full bg-ui-surface-3 text-ui-1 font-semibold">{initials(employee.name)}</button>
              <button type="button" onClick={() => onOpenEmployee?.(employee.employee_ref)} className="min-w-0 text-left"><strong className="text-ui-2">{employee.name}</strong><span className="ml-2 text-ui-1 text-ui-txt-3">{employee.role}</span><span className="block truncate text-ui-1 text-ui-txt-2">{employee.responsibility || "尚未记录当前职责"}</span></button>
              <span className="rounded-ui-pill bg-ui-surface-2 px-2 py-0.5 text-ui-1 text-ui-txt-2">{employee.ui_status?.label || "空闲"}</span>
              <button type="button" aria-expanded={open} aria-label={`${open ? "收起" : "展开"}${employee.name}工作过程`} onClick={() => setExpanded(open ? null : employee.employee_ref)} className="h-8 w-8 text-ui-2 text-ui-txt-2">{open ? "▾" : "▸"}</button>
            </div>
            {open ? (
              <div className="mx-auto max-w-3xl resize-y overflow-auto pb-4 pl-11 pr-2">
                <div className="space-y-3 text-ui-2">
                  <p>{work?.activity || "当前没有新的工作过程。"}</p>
                  <ResultReferences refs={work?.result_refs || employee.recent_result_refs} onOpenResult={onOpenResult} />
                </div>
                <a className="block text-ui-primary" href={`/ceo-office/organization/employees/${encodeURIComponent(employee.company_employee_ref || employee.employee_ref)}#employee-conversation`}>与{employee.name}对话 ▸</a>
                <Composer employee={employee} onSend={onSend} />
              </div>
            ) : null}
          </article>
        );
      })}
    </section>
  );
}
