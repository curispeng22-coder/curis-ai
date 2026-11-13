"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useRuntime } from "../runtime/RuntimeProvider.js";
import { getRecentConversations, dismissConversation } from "../../lib/v1FrontendApi.js";
import styles from "../workspace/WorkspacePaneShell.module.css";

export function recentRows(rows, expanded) {
  return [...(Array.isArray(rows) ? rows : [])].sort((a, b) => (Date.parse(b.activity_at) || 0) - (Date.parse(a.activity_at) || 0)).slice(0, expanded ? undefined : 3);
}
export default function ConversationQuickAccess() {
  const { companyId } = useRuntime();
  const pathname = usePathname();
  const request = useRef(null);
  const [snapshot, setSnapshot] = useState({ companyId: null, rows: [], loading: true, error: false });
  const [expanded, setExpanded] = useState(false);
  const visible = snapshot.companyId === companyId ? snapshot : { rows: [], loading: Boolean(companyId), error: false };
  useEffect(() => {
    const token = { active: true, sequence: 0, inFlight: false, dismissed: new Set() }; request.current = token;
    setSnapshot({ companyId, rows: [], loading: Boolean(companyId), error: false }); setExpanded(false);
    if (!companyId) return () => { token.active = false; };
    const load = () => {
      if (token.inFlight) return;
      token.inFlight = true;
      const sequence = ++token.sequence;
      getRecentConversations(companyId).then((value) => {
        if (token.active && sequence === token.sequence) setSnapshot({ companyId,
          rows: (value.conversations || []).filter((row) => !token.dismissed.has(row.conversation_id)), loading: false, error: false });
      }).catch(() => { if (token.active && sequence === token.sequence) setSnapshot((old) => ({ ...old, loading: false, error: true })); })
        .finally(() => { token.inFlight = false; });
    };
    load(); const timer = setInterval(load, 5000);
    return () => { token.active = false; clearInterval(timer); };
  }, [companyId, pathname]);
  async function hide(id) {
    const token = request.current, targetCompany = companyId;
    if (!targetCompany || !token?.active) return;
    try {
      await dismissConversation(targetCompany, id);
      if (request.current !== token || !token.active) return;
      token.dismissed.add(id); ++token.sequence;
      setSnapshot((old) => old.companyId === targetCompany ? { ...old, rows: old.rows.filter((row) => row.conversation_id !== id), error: false } : old);
    } catch { if (request.current === token && token.active) setSnapshot((old) => ({ ...old, error: true })); }
  }
  return <section aria-label="最近对话" className={styles.recentConversations}>
    <div className={styles.recentHeading}><h2>最近对话</h2><Link href="/ceo-office/conversation">新对话</Link></div>
    {visible.loading ? <p role="status" className={styles.recentState}>正在读取最近对话…</p> : null}
    {visible.error ? <p role="status" className={styles.recentState}>最近对话暂时无法读取，正在重试。</p> : null}
    {!visible.rows.length && !visible.error && !visible.loading ? <p className={styles.recentState}>暂无最近对话</p> : null}
    <div>{recentRows(visible.rows, expanded).map((row) => <div key={row.conversation_id} className={styles.recentRow}>
      <Link href={"/ceo-office/conversation?conversation_id=" + encodeURIComponent(row.conversation_id)} className={styles.recentLink}>
        <span title={row.title}>{row.title || "未命名对话"}</span><span className={styles.recentMeta}>{row.employee_name || "员工"} · {new Date(row.activity_at).toLocaleDateString("zh-CN", { month: "numeric", day: "numeric" })}</span>
      </Link><button type="button" aria-label={"从最近对话移除：" + row.title} title="只移除快捷入口，不删除记录" onClick={() => hide(row.conversation_id)} className={styles.recentDismiss}>×</button>
    </div>)}</div>
    {visible.rows.length > 3 && <button type="button" aria-expanded={expanded} className={styles.recentExpand} onClick={() => setExpanded((value) => !value)}>{expanded ? "收起对话" : "展开全部对话"}</button>}
  </section>;
}
