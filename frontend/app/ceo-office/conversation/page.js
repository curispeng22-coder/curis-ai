"use client";

import { Suspense, useEffect, useRef, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import TerraShell from "../../../components/terra/TerraShell.js";
import { useRuntime } from "../../../components/runtime/RuntimeProvider.js";
import EmployeeConversation from "../../../components/v1/EmployeeConversation.js";
import D1Surface from "../../../components/delivery/d1/D1Surface.js";
import { createConversation, getConversation, getConversationEmployees, joinConversation } from "../../../lib/v1FrontendApi.js";

function ConversationSurface() {
  const { companyId } = useRuntime();
  const params = useSearchParams();
  const router = useRouter();
  const id = params.get("conversation_id");
  const [view, setView] = useState(null);
  const [employees, setEmployees] = useState([]);
  const [employee, setEmployee] = useState(params.get("employee_ref") || "");
  const [title, setTitle] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const request = useRef(null);
  useEffect(() => {
    let active = true;
    setView(null); setError("");
    if (!companyId) return undefined;
    getConversationEmployees(companyId).then((value) => active && setEmployees(value.employees)).catch(() => active && setError("暂时无法读取员工，请重新打开对话。"));
    if (id) getConversation(companyId, id).then((value) => active && setView(value)).catch(() => active && setError("这段对话暂时无法打开，请从所在公司重新进入。"));
    return () => { active = false; };
  }, [companyId, id]);
  async function start(event) {
    event.preventDefault();
    if (busy || !companyId) return;
    setBusy(true); setError("");
    try {
      if (id) setView(await joinConversation(companyId, id, employee));
      else {
        if (!request.current || request.current.title !== title || request.current.employee_ref !== (employee || null)) request.current = { request_id: crypto.randomUUID(), title, employee_ref: employee || null };
        const created = await createConversation(companyId, request.current);
        router.replace(`/ceo-office/conversation?conversation_id=${encodeURIComponent(created.conversation_id)}`);
      }
    } catch { setError("操作尚未确认完成，已有对话会保留，可以重试。"); }
    finally { setBusy(false); }
  }
  return <TerraShell topCrumb="对话"><div className="mx-auto max-w-4xl space-y-4">
    <h1 className="text-ui-6 font-semibold">{view?.title || (id ? "对话" : "新对话")}</h1>
    {error ? <p role="alert">{error}</p> : null}
    {(!id || (view && !view.employee)) ? <form onSubmit={start} className="space-y-3">
      {!id ? <label className="block">想讨论什么？<input value={title} maxLength={120} onChange={(event) => setTitle(event.target.value)} className="mt-1 block w-full rounded-ui-sm border border-ui-line bg-ui-surface p-2" /></label> : <p className="text-ui-txt-2">讨论已保存。选择员工后，可以使用其当前工作背景继续。</p>}
      <label className="block">与谁讨论<select value={employee} onChange={(event) => setEmployee(event.target.value)} className="ml-3 border border-ui-line bg-ui-surface p-2"><option value="">稍后选择员工</option>{employees.map((item) => <option key={item.employee_ref} value={item.employee_ref}>{item.name}</option>)}</select></label>
      <button disabled={busy || !companyId || (Boolean(id) && !employee)} className="rounded-ui-sm bg-ui-primary px-4 py-2 text-ui-primary-fg disabled:opacity-50">{busy ? "正在保存…" : id ? "邀请员工继续" : "开始对话"}</button>
    </form> : null}
    {id && !view && !error ? <p role="status">正在读取对话…</p> : null}
    {view ? <EmployeeConversation key={`${id}:${view.owner_ref}`} companyId={companyId} employee={view.employee} conversationId={id} /> : null}
  </div></TerraShell>;
}

export default function ConversationPage() {
  return <Suspense fallback={<p>正在读取对话…</p>}><D1Surface initialView="conversation" legacyEntry={<ConversationSurface />} /></Suspense>;
}
