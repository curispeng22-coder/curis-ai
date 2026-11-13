"use client";

import { workspaceEntryHref } from "../../../lib/runtimeApi.js";
import styles from "./D1.module.css";

const stateCopy = { WAITING_CEO: "需要你判断", WAITING_DECISION: "等待当前决定", EXECUTING: "员工正在执行", RUNNING: "正在执行", READY: "准备就绪", ARCHIVED: "已归档", FAILED: "执行遇到问题", BLOCKED: "等待修复", PAUSED: "已暂停", WAITING: "等待下一步", COMPLETED: "已完成", CANCELLED: "已停止", ACTIVE: "责任已接续", PLANNED: "计划已创建", INVALIDATED: "依据需要核对" };
export function workState(value) { return stateCopy[value] || "状态待核对"; }

const sourceCopy = { DECISION_PACKET: "待决定", HANDOFF: "责任接续", RESULT: "工作结果", OUTCOME: "经营结果", EVIDENCE: "依据", ACCEPTANCE: "验收", CYCLE: "工作周期", RESPONSIBILITY_ASSIGNMENT: "责任安排", WORK: "工作" };

export default function CeoMatterView({ company, attention, businesses = [], businessesKnown = true, organization, organizationError, selected, onMatter, onWork, onResult, onDiscuss }) {
  const items = attention?.company?.company_id && attention.company.company_id !== company?.company_id ? [] : attention?.items || [];
  const matter = selected ? items.find((item) => item.source_ref === selected.sourceRef && item.source_type === selected.sourceType) : null;
  if (selected && !matter) return <section className={styles.empty}><h1>这项事项当前未返回</h1><p>来源可能已变化，请重新读取公司事实。不会用另一项事项替代。</p></section>;
  if (matter) return <div className={styles.matterReading}>
    <header className={styles.pageTitle}><div><p className={styles.crumb}>{company?.name} / {sourceCopy[matter.source_type] || "经营事项"}</p><h1>{matter.summary}</h1></div><span className={styles.badge}>{workState(matter.status)}</span></header>
    <section className={styles.readingSection}><h2>当前事实与责任</h2><p>{matter.summary}</p><p>{matter.reason || "原因尚未记录，请核对原来源。"}</p><dl className={styles.meta}><dt>当前状态</dt><dd>{workState(matter.status)}</dd><dt>负责人</dt><dd>{matter.owner_name || "负责人姓名未记录"}</dd><dt>下一步</dt><dd>{matter.recovery_action || "回到原来源核对"}</dd><dt>下一次检查</dt><dd>{matter.next_check_at || "时间未记录"}</dd><dt>更新时间</dt><dd>{matter.updated_at || "时间未记录"}</dd></dl></section>
    <section className={styles.readingSection}><h2>回到原工作继续</h2><div className={styles.actions}>
      {(matter.work_ref || matter.source_type === "WORK") && matter.workspace_id && <button className={styles.primary} onClick={() => onWork(matter.work_ref || matter.source_ref, matter.workspace_id)}>打开原工作</button>}
      {["RESULT", "OUTCOME"].includes(matter.source_type) && matter.workspace_id && <button className={styles.primary} onClick={() => onResult(matter.source_ref, matter.workspace_id)}>打开结果</button>}
      {matter.owner_ref && <button onClick={() => onDiscuss(matter.owner_ref, matter.workspace_id)}>一起讨论</button>}
      {matter.workspace_id && <a href={workspaceEntryHref(matter.workspace_id)}>返回原工作空间</a>}
    </div><p className={styles.limit}>{matter.workspace_id ? "正式处理在原工作中进行；这里保留事项与责任，不改变决定状态。" : "当前来源未提供可用的处理入口，请先核对原责任。"}</p></section>
    <details className={styles.sourceDetails}><summary>查看事项来源详情</summary><dl className={styles.meta}><dt>来源类型</dt><dd>{matter.source_type}</dd><dt>来源标识</dt><dd>{matter.source_ref}</dd><dt>责任标识</dt><dd>{matter.responsibility_ref || "未记录"}</dd><dt>负责人来源标识</dt><dd>{matter.owner_ref || "未记录"}</dd></dl></details>
  </div>;
  const scopedBusinesses = businesses.filter((business) => business.company_id === company?.company_id);
  const currentOrganization = organization?.company?.id === company?.company_id ? organization : null;
  return <div className={styles.companyOverview}>
    <header className={styles.pageTitle}><div><p className={styles.crumb}>{company?.name || "公司"} / 公司经营全景</p><h1>CEO 工作台</h1></div><span className={styles.subtle}>当前公司事实</span></header>
    <section className={styles.brief}><span className={styles.briefMark} aria-hidden="true">☼</span><div><h2>{items.length ? "先看需要你判断和推进的事情。" : attention?.state === "QUIET" ? "当前没有需要你处理的事项。" : "先核对当前可读取的公司事实。"}</h2><p>{attention?.state === "QUIET" ? "当前来源没有返回待处理项；外部经营效果仍需各业务核对。" : "保留来源与责任，回到同一项工作继续。"}</p></div></section>
    <section className={styles.portfolio} aria-labelledby="business-progress-title">
      <header className={styles.sectionHeading}><h2 id="business-progress-title">业务进展</h2><a href="/ceo-office/business">查看业务空间 →</a></header>
      {organizationError && <p role="status" className={styles.limit}>{organizationError}</p>}
      <div className={styles.portfolioHead} aria-hidden="true"><span>业务与目标</span><span>当前状态</span><span>已返回的关注 / 变化</span><span>负责人</span><span>下一步</span></div>
      {scopedBusinesses.length ? scopedBusinesses.map((business) => {
        const facts = currentOrganization?.businessById.get(business.business_id);
        const workspaces = new Set((facts?.workspaces || []).map((workspace) => workspace.id));
        const related = items.filter((item) => item.workspace_id && workspaces.has(item.workspace_id));
        const next = related[0];
        const leader = facts?.leaderAssignment?.enabled ? facts.leader : null;
        const href = `/ceo-office/business?${new URLSearchParams({ company_id: company.company_id, business_id: business.business_id })}`;
        return <article className={styles.portfolioRow} key={business.business_id}>
          <div><a href={href}><strong>{business.name || business.business_name || "未命名业务"}</strong></a><p>{facts?.goal || business.goal || business.target_outcome || "目标尚未记录"}</p></div>
          <div><span className={styles.badge}>{facts?.status || "状态尚未读取"}</span><small>{facts ? `${facts.workspaces.length} 个工作空间` : "工作空间尚未确认"}</small></div>
          <div>{next ? <><strong>{next.summary}</strong><small>{sourceCopy[next.source_type] || "经营事实"} · {workState(next.status)}</small></> : <p>{facts && attention ? "当前来源未返回关注事项" : "关联事实尚未确认"}</p>}</div>
          <div><strong>{leader?.name || "负责人尚未确认"}</strong><small>{leader ? "当前业务责任" : "以组织记录为准"}</small></div>
          <div>{next ? <button onClick={() => onMatter(next)}>查看原事项 →</button> : <a href={href}>查看业务现场 →</a>}{next?.next_check_at && <small>{next.next_check_at}</small>}</div>
        </article>;
      }) : <p className={styles.portfolioEmpty}>{businessesKnown ? "当前公司没有已建立的业务。" : "业务目录暂不可读取，已读取事项仍保留。"}</p>}
    </section>
    <div className={styles.companyBottom}>
      <section><header className={styles.sectionHeading}><h2>需要 CEO 关注</h2><span className={styles.subtle}>{attention ? `${items.length} 项已读取事项` : "事项尚未读取"}</span></header><div>{items.length ? items.map((item) => <button key={`${item.source_type}:${item.source_ref}`} className={styles.attentionRow} id={`matter-${item.source_ref}`} onClick={() => onMatter(item)}><span className={styles.badge}>{sourceCopy[item.source_type] || "经营事项"}</span><span><strong>{item.summary}</strong><small>{workState(item.status)} · {item.next_check_at || "检查时间未记录"}</small></span><span aria-hidden="true">→</span></button>) : <p className={styles.subtle}>{attention ? "当前来源未返回待处理项。" : "事项暂不可读取，请重新读取公司事实。"}</p>}</div></section>
      <section><header className={styles.sectionHeading}><h2>已返回的结果与来源</h2></header>{items.filter((item) => ["RESULT", "OUTCOME", "EVIDENCE"].includes(item.source_type)).length ? items.filter((item) => ["RESULT", "OUTCOME", "EVIDENCE"].includes(item.source_type)).map((item) => <button key={`${item.source_type}:${item.source_ref}`} className={styles.matterRow} onClick={() => onMatter(item)}><span><strong>{item.summary}</strong><small>{item.updated_at || "来源时间未记录"}</small></span><span aria-hidden="true">→</span></button>) : <p className={styles.subtle}>当前事项来源没有返回结果动态；不代表业务没有成果。</p>}<a href="/ceo-office/organization">查看组织与责任 →</a></section>
    </div>
  </div>;
}
