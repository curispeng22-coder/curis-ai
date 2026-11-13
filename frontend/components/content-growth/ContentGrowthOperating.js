"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { contentGrowthApi as api } from "../../lib/contentGrowthApi.js";
import { cgScopedRead, contentHref } from "../../lib/contentGrowthState.mjs";
import styles from "./ContentGrowth.module.css";

export function useGrowthFacts(company, workspaceId) {
  const [state, setState] = useState({ status: "loading", data: null, error: "" });
  useEffect(() => {
    let active = true; setState({ status: "loading", data: null, error: "" });
    Promise.all([api.accounts(company, workspaceId), api.verifications(company, workspaceId), api.observations(company, workspaceId), api.operatingContext(company, workspaceId)])
      .then((values) => { values.forEach((value) => cgScopedRead(value, company, workspaceId)); if (active) setState({ status: "ready", data: { accounts: values[0].accounts, catalog: values[0].catalog, verifications: values[1].verifications, observations: values[2].observations, reports: values[3].records.filter(r=>r.kind==="Report") }, error: "" }); })
      .catch((reason) => { if (active) setState({ status: "error", data: null, error: reason.message }); });
    return () => { active = false; };
  }, [company, workspaceId]);
  return state;
}

export default function ContentGrowthOperating({ company, workspaceId, collection, onInspect }) {
  const state = useGrowthFacts(company, workspaceId), [platform, setPlatform] = useState("");
  const data = state.data;
  const accounts = data?.accounts.filter((account) => !platform || account.data.platform_ref === platform) || [];

  return <section><header className={styles.pageHeader}><div><h1>内容增长 / 经营</h1><p className={styles.sub}>从账号、内容与经营记录，决定下一步。</p></div><Link href={contentHref(workspaceId, { view: "production" })}>进入内容制作 →</Link></header>
    {state.error && <p className={styles.error} role="alert">{state.error}</p>}
    <section className={styles.factBand}><div><span>本地内容</span><strong>{collection.contents.length}</strong></div><div><span>经营账号</span><strong>{data ? data.accounts.length : "—"}</strong></div><div><span>人工核验</span><strong>{data ? data.verifications.length : "—"}</strong></div><div><span>人工观察</span><strong>{data ? data.observations.length : "—"}</strong></div></section>
    <section className={styles.operatingSummary}><section><h2>经营结果</h2><p className={styles.sub}>平台未连接，触达、增长与收入暂不可核验。</p><Link href={contentHref(workspaceId, { view: "observe" })}>查看原观察 →</Link></section><section><h2>判断与下一步</h2><p className={styles.sub}>{data?.observations.length ? "已有人工观察，先核对账号、周期与依据，再判断下一步。" : "尚无足够观察，经营判断待形成。"}</p><div className={styles.actions}><Link href={contentHref(workspaceId, { view: "analysis" })}>核对判断依据</Link><Link href={contentHref(workspaceId, { view: "production" })}>继续制作</Link></div></section></section>
    {data?.reports.length > 0 && <section className={styles.operatingSummary}><h2>原期间的人工判断</h2>{data.reports.slice(-3).map(record=><article key={record.ref}><h3>{record.payload.title}</h3><p>原期间：{record.payload.period} · 人工未验证</p><p>{record.payload.next_decision || "下一步尚未明确"}</p><Link href={contentHref(workspaceId,{view:"analysis",object:record.ref})}>查看原报告与观察 →</Link></article>)}</section>}
    <header className={styles.sectionHeader}><h2>平台与账号</h2><Link href={contentHref(workspaceId, { view: "accounts" })}>维护经营账号</Link></header>
    {state.status === "loading" && <p role="status" className={styles.sub}>正在读取经营记录…</p>}
    {data && <><div className={styles.platforms}>{data.catalog.map((item) => <button key={item.platform} className={`${styles.platform} ${platform === item.platform ? styles.selected : ""}`} aria-pressed={platform === item.platform} onClick={() => setPlatform(platform === item.platform ? "" : item.platform)}><strong>{item.name}</strong><span>{data.accounts.filter((account) => account.data.platform_ref === item.platform).length} 个本地账号</span><small>未连接</small></button>)}</div><div className={styles.denseRows}>{accounts.map((account) => <button key={account.entity_id} className={styles.objectRow} onClick={() => { onInspect({ id: `account:${account.entity_id}`, title: account.data.name, request: Date.now(), content: <section className={`${styles.main} ${styles.utility}`}><h2>{account.data.name}</h2><p className={styles.sub}>账号经营资料 · 未连接</p><dl className={styles.definition}>{[["定位", account.data.positioning], ["受众", account.data.audience], ["内容配比", account.data.content_mix], ["发布节奏", account.data.cadence], ["责任说明", account.data.responsibility]].map(([label, value]) => <div key={label}><dt>{label}</dt><dd>{value || "未填写"}</dd></div>)}</dl><Link href={contentHref(workspaceId, { view: "accounts" })}>进入账号工作台 →</Link></section> }); }}><strong>{account.data.name}</strong><span>{account.data.positioning || "定位待填写"}</span><span>未连接 · 查看经营资料 →</span></button>)}</div>{!accounts.length && <p className={styles.emptyRow}>当前平台还没有本地账号。登记后可在本业务内维护账号资料，尚未连接外部平台。</p>}</>}
    <section className={styles.nextStep}><h2>继续经营</h2><div className={styles.actions}><Link href={contentHref(workspaceId, { view: "market" })}>核对市场依据</Link><Link href={contentHref(workspaceId, { view: "verify" })}>准备逐账号核验</Link><Link href={contentHref(workspaceId, { view: "learning" })}>回看内容经验</Link></div></section>
  </section>;
}
