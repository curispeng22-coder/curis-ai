"use client";

import { useEffect, useMemo, useState } from "react";

const LABELS = {
  CREATED: "准备交接",
  SENT: "等待接收员工确认",
  COMPLETED: "责任已交接",
  RETURNED: "已退回原负责人",
  REJECTED: "接收员工未接管",
};

export default function RdResponsibilityHandoff({ cycle, employees, busy, onSubmit }) {
  const handoff = cycle.data?.responsibilityHandoff;
  const holderRef = cycle.data?.workContext?.responsibilityEmployeeRef;
  const targets = useMemo(
    () => (employees || []).filter((item) => item.entity_id !== holderRef),
    [employees, holderRef],
  );
  const [targetRef, setTargetRef] = useState(targets[0]?.entity_id || "");

  useEffect(() => {
    if (!targets.some((item) => item.entity_id === targetRef)) setTargetRef(targets[0]?.entity_id || "");
  }, [targetRef, targets]);

  if (!handoff && cycle.data?.artifactReview?.status !== "APPROVED") return null;
  if (!handoff) return <section className="mt-4 border-t border-ui-line pt-3">
    <p className="text-ui-1 font-semibold text-ui-txt">责任交接</p>
    <p className="mt-1 text-ui-1 text-ui-txt-3">代码送审不会转移责任；只有这里确认的后续责任才会交给另一名员工。</p>
    {targets.length ? <div className="mt-3 flex flex-wrap items-center gap-2">
      <label className="text-ui-1 text-ui-txt-2" htmlFor={`handoff-${cycle.entity_id}`}>接收员工</label>
      <select id={`handoff-${cycle.entity_id}`} value={targetRef} onChange={(event) => setTargetRef(event.target.value)} className="rounded-ui-sm border border-ui-line bg-ui-surface px-2 py-2 text-ui-1 text-ui-txt">
        {targets.map((employee) => <option key={employee.entity_id} value={employee.entity_id}>{employee.data?.name || "未命名员工"}</option>)}
      </select>
      <button type="button" disabled={busy || !targetRef} onClick={() => onSubmit(targetRef)} className="rounded-ui-sm border border-ui-line px-3 py-2 text-ui-1 font-semibold text-ui-txt disabled:opacity-50">{busy ? "正在发送…" : "交接后续责任"}</button>
    </div> : <p className="mt-2 text-ui-1 text-ui-txt-3">当前没有可接收责任的另一名员工。</p>}
  </section>;

  const source = (employees || []).find((item) => item.entity_id === handoff.fromEmployeeRef);
  const target = (employees || []).find((item) => item.entity_id === handoff.toEmployeeRef);
  return <section className="mt-4 border-t border-ui-line pt-3">
    <p className="text-ui-1 font-semibold text-ui-txt">⇄ 责任交接 · {LABELS[handoff.status] || handoff.status}</p>
    <p className="mt-1 text-ui-1 text-ui-txt-2">{source?.data?.name || "原负责人"} → {handoff.responsibilitySummary} → {target?.data?.name || "接收员工"}</p>
    <p className="mt-1 text-ui-1 text-ui-txt-3">{handoff.status === "SENT" ? "当前负责人尚未改变，当前也没有员工在执行。" : handoff.status === "COMPLETED" ? "接收员工已成为负责人；开始真实工作前 Current Executor 仍为 none。" : handoff.responseReason || handoff.reason}</p>
  </section>;
}
