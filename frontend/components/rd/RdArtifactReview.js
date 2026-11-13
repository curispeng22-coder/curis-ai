"use client";

import { useEffect, useMemo, useState } from "react";

const COPY = {
  REQUESTED: ["待审核", "审核请求已保存，正在交给审核员工。"],
  REVIEWING: ["审核中", "审核员工正在检查代码变化与验证证据。"],
  APPROVED: ["审核通过", "审核意见已经保存，原研发负责人继续持有这项责任。"],
  CHANGES_REQUESTED: ["需要修改", "审核员工已提出修改意见，原研发负责人继续处理。"],
  FAILED: ["审核未完成", "失败事实已经保留，原研发责任没有转移。"],
};

export default function RdArtifactReview({ cycle, employees, busy, onSubmit, onOpenResult }) {
  const holderRef = cycle.data?.workContext?.responsibilityEmployeeRef;
  const review = cycle.data?.artifactReview;
  const reviewers = useMemo(
    () => (employees || []).filter((item) => item.entity_id !== holderRef && item.lifecycle_status === "AVAILABLE"),
    [employees, holderRef],
  );
  const [reviewerRef, setReviewerRef] = useState(reviewers[0]?.entity_id || "");

  useEffect(() => {
    if (!reviewers.some((item) => item.entity_id === reviewerRef)) setReviewerRef(reviewers[0]?.entity_id || "");
  }, [reviewerRef, reviewers]);

  if (cycle.data?.executionStatus !== "COMPLETED") return null;
  if (!review) return <section className="mt-4 rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3">
    <p className="text-ui-1 font-semibold text-ui-txt">代码审核</p>
    <p className="mt-1 text-ui-1 leading-relaxed text-ui-txt-2">选择另一名真实员工检查当前代码结果；研发负责人不会因此转移。</p>
    {reviewers.length ? <div className="mt-3 flex flex-wrap items-center gap-2">
      <label className="text-ui-1 text-ui-txt-2" htmlFor={`reviewer-${cycle.entity_id}`}>审核员工</label>
      <select id={`reviewer-${cycle.entity_id}`} value={reviewerRef} onChange={(event) => setReviewerRef(event.target.value)} className="rounded-ui-sm border border-ui-line bg-ui-surface px-2 py-2 text-ui-1 text-ui-txt">
        {reviewers.map((employee) => <option key={employee.entity_id} value={employee.entity_id}>{employee.data?.name || "未命名审核员工"}</option>)}
      </select>
      <button type="button" disabled={busy || !reviewerRef} onClick={() => onSubmit(reviewerRef)} className="rounded-ui-sm border border-ui-line px-3 py-2 text-ui-1 font-semibold text-ui-txt disabled:opacity-50">{busy ? "正在送审…" : "送交代码审核"}</button>
    </div> : <p className="mt-3 text-ui-1 text-ui-txt-3">当前还没有可用的第二名审核员工；不会把研发负责人伪装成 Reviewer。</p>}
  </section>;

  const [label, summary] = COPY[review.status] || [review.status || "状态未知", "当前审核状态无法解释，请刷新后重试。"];
  const reviewer = (employees || []).find((item) => item.entity_id === review.reviewerEmployeeRef);
  return <section className="mt-4 rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3">
    <div className="flex flex-wrap items-center justify-between gap-2">
      <div><p className="text-ui-1 font-semibold text-ui-txt">代码审核 · {label}</p><p className="mt-1 text-ui-1 text-ui-txt-3">{reviewer?.data?.name || "审核员工"}</p></div>
      {review.currentExecutorRef ? <span className="text-ui-1 font-semibold text-ui-success">正在检查</span> : <span className="text-ui-1 text-ui-txt-3">当前无人执行</span>}
    </div>
    <p className="mt-2 text-ui-1 leading-relaxed text-ui-txt-2">{cycle.data?.reviewConversation?.summary || summary}</p>
    {(review.resultRefs || []).length ? <button type="button" onClick={() => onOpenResult("review")} className="mt-2 text-ui-1 font-semibold text-ui-accent">📎 查看审核结果 ▸</button> : null}
    <details className="mt-3 border-t border-ui-line pt-3 text-ui-1 text-ui-txt-2"><summary className="cursor-pointer font-semibold">查看审核技术引用</summary><dl className="mt-3 grid gap-2"><div><dt>Review Request</dt><dd className="break-all">{review.requestRef}</dd></div><div><dt>Reviewer Task</dt><dd className="break-all">{review.reviewTaskRef || "尚未创建"}</dd></div></dl></details>
  </section>;
}
