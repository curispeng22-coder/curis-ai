"use client";
import { useCallback, useLayoutEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { contentHref } from "../../lib/contentGrowthState.mjs";
import { GrowthRecordPanel } from "./ContentGrowthMarket.js";
import ContentGrowthObserve from "./ContentGrowthObserve.js";
import styles from "./ContentGrowth.module.css";

export default function ContentGrowthAnalysis({ company, workspaceId, onInspect, collection, entry }) {
  const scope = useMemo(() => ({ company, workspaceId }), [company, workspaceId]);
  const active = useRef(null), [observationRevision, setObservationRevision] = useState(0);
  useLayoutEffect(() => { active.current = scope; return () => { active.current = null; }; }, [scope]);
  const observationSaved = useCallback((saved) => {
    if (active.current === scope && saved.company === scope.company && saved.workspaceId === scope.workspaceId) setObservationRevision(value => value + 1);
  }, [scope]);
  return <section><header className={styles.pageHeader}><div><h1>经营分析</h1><p className={styles.sub}>把原观察、期间与账号放在一起核对，区分事实与判断。</p></div><Link href={contentHref(workspaceId, { view: "learning" })}>回看内容经验 →</Link></header><GrowthRecordPanel company={company} workspaceId={workspaceId} kinds={["Report"]} observationRevision={observationRevision} collection={collection} selectedRef={entry?.object} onInspect={onInspect} /><section className={styles.operatingResult}><h2>平台结果与归因</h2><p>平台未连接，触达、收入与内容贡献暂不可核验。</p></section><section className={styles.analysisBasis}><h2>判断与来源</h2><p className={styles.sub}>保留每个账号的原周期与人工记录；证据不足时不推定增长、收益或因果。</p></section><ContentGrowthObserve company={company} workspaceId={workspaceId} onInspect={onInspect} title="原观察与依据" onSaved={observationSaved} embedded /></section>;
}
