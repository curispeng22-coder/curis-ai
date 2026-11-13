"use client";
import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { contentGrowthApi as api } from "../../lib/contentGrowthApi.js";
import { contentHref, cgScopedRead, stableRequest } from "../../lib/contentGrowthState.mjs";
import styles from "./ContentGrowth.module.css";

// Platform chain S3 (contract CURIS_PLATFORM_ACCOUNT_LOCAL_CHAIN_CONTRACT §4.4):
// CEO manual account performance observations. Immutable point-in-time records,
// forced UNVERIFIED / CEO_MANUAL / NOT_CONNECTED; free text only — there is no
// metrics ingestion, analytics, comparison, or platform connection.
const PLATFORM_LABELS = { xhs: "小红书", douyin: "抖音", wechat_oa: "公众号", tiktok: "TikTok", youtube: "YouTube", bilibili: "bilibili" };

export default function ContentGrowthObserve({ company, workspaceId, onInspect, onSaved, title, embedded = false }) {
  const view = useMemo(() => ({ company, workspaceId }), [company, workspaceId]), scope = useRef(null);
  const [accountFilter, setAccountFilter] = useState(""), [periodFilter, setPeriodFilter] = useState("");
  const [records, setRecords] = useState([]), [accounts, setAccounts] = useState([]);
  const [panelRequest, setPanelRequest] = useState(0);
  const alive = useRef(true), readSequence = useRef(0), mutation = useRef(false), readInfo = useRef(null), commandIdentity = useRef({});
  const [loaded, setLoaded] = useState(false);
  const requestId = (action, base, data) => { const next = stableRequest(commandIdentity.current[action], action, base, data, () => crypto.randomUUID()); commandIdentity.current[action] = next; return next.request_id; };
  const [error, setError] = useState(""), [busy, setBusy] = useState(false);
  const [mode, setMode] = useState("list"); // list | create | detail
  const [selected, setSelected] = useState(null);
  const [accountRef, setAccountRef] = useState("");
  const [form, setForm] = useState({ title: "", body: "", period: "" });

  useLayoutEffect(() => {
    scope.current = view; alive.current = true; mutation.current = false; readInfo.current = null; commandIdentity.current = {};
    setLoaded(false); setBusy(false); setRecords([]); setAccounts([]); setSelected(null); setMode("list");
    setAccountRef(""); setForm({ title: "", body: "", period: "" }); setAccountFilter(""); setPeriodFilter("");
    return () => { scope.current = null; alive.current = false; readSequence.current += 1; };
  }, [view]);

  const load = useCallback(async () => {
    if (scope.current !== view) return;
    const ticket = ++readSequence.current;
    setError("");
    try {
      const [obsResult, accountResult] = await Promise.all([
        api.observations(company, workspaceId),
        api.accounts(company, workspaceId),
      ]);
      [obsResult, accountResult].forEach((value) => cgScopedRead(value, company, workspaceId)); if (!alive.current || scope.current !== view || ticket !== readSequence.current) return;
      readInfo.current = obsResult.entry; setLoaded(true);
      setRecords(obsResult.observations || []);
      setAccounts(accountResult.accounts || []);
    } catch (reason) { if (alive.current && scope.current === view && ticket === readSequence.current) setError(reason.message); }
  }, [company, workspaceId, view]);

  useEffect(() => { load(); }, [load]);

  const startCreate = () => {
    setPanelRequest((value) => value + 1); setMode("create");
  };
  const setField = (key) => (event) => { if (scope.current === view && !mutation.current) setForm((prev) => ({ ...prev, [key]: event.target.value })); };

  const save = async () => {
    if (mutation.current || !alive.current || scope.current !== view || !loaded) return;
    if (!accountRef) { setError("请选择观察账号（须为本业务经营账号）。"); return; }
    if (!form.title.trim() || !form.body.trim() || !form.period.trim()) { setError("标题、观察正文与观察周期都需要填写。"); return; }
    const data = { title: form.title.trim(), body: form.body.trim(), period: form.period.trim(), scope_ref: accountRef };
    mutation.current = true; setBusy(true); setError("");
    try {
      await api.observationCreate(company, workspaceId, requestId("save-observation", "", data), data);
      if (!alive.current || scope.current !== view) return;
      commandIdentity.current["save-observation"] = null; setForm({ title: "", body: "", period: "" }); setAccountRef("");
      setMode("list");
      onSaved?.({ company, workspaceId });
      await load();
    } catch (reason) { if (alive.current && scope.current === view) setError(reason.message); } finally { if (alive.current && scope.current === view) { mutation.current = false; setBusy(false); } }
  };

  const openDetail = async (ref) => {
    if (!alive.current || scope.current !== view) return;
    const ticket = ++readSequence.current; setBusy(true); setError("");
    try { const value = await api.observation(company, workspaceId, ref); if (!alive.current || scope.current !== view || ticket !== readSequence.current) return; if (value.entity_id !== ref || value.company_id !== company || value.data.business_ref !== readInfo.current?.scope.business_id) throw new Error("观察范围已变化，请重新选择。"); setSelected(value); setPanelRequest((value) => value + 1); setMode("detail"); }
    catch (reason) { if (alive.current && scope.current === view && ticket === readSequence.current) setError(reason.message); } finally { if (alive.current && scope.current === view && ticket === readSequence.current) setBusy(false); }
  };

  const periods = [...new Set(records.map((item) => item.data.period))];
  const visibleRecords = records.filter((item) => (!accountFilter || item.data.scope_ref === accountFilter) && (!periodFilter || item.data.period === periodFilter));
  const panel = useMemo(() => mode === "list" ? null : <section className={`${styles.main} ${styles.utility}`}><fieldset disabled={busy}><button disabled={busy} className={styles.formDismiss} onClick={() => setMode("list")}>← 返回列表</button>{error && <p className={styles.error} role="alert">{error}</p>}
      {mode === "create" && (
        <>
          <h2>新建表现观察</h2>
          <div className={styles.fields} style={{ gridTemplateColumns: "1fr" }}>
            <label>观察账号（本业务经营账号）
              <select value={accountRef} onChange={(event) => setAccountRef(event.target.value)}>
                <option value="">选择账号</option>
                {accounts.map((item) => <option key={item.entity_id} value={item.entity_id}>{PLATFORM_LABELS[item.data.platform_ref] || item.data.platform_ref} · {item.data.name}（未连接）</option>)}
              </select>
            </label>
            <label>观察标题
              <input value={form.title} maxLength={2000} placeholder="例如：首周评论区反馈" onChange={setField("title")} />
            </label>
            <label>观察周期
              <input value={form.period} maxLength={200} placeholder="例如：2026-10 第一周" onChange={setField("period")} />
            </label>
            <label>观察正文（手工记录，不填平台采集数字）
              <textarea rows={8} value={form.body} maxLength={20000} placeholder="记录你人工看到的现象与判断；样本不足不下结论。" onChange={setField("body")} />
            </label>
          </div>
          <p className={styles.notice}>保存后为时点不可变记录（人工观察 · 未验证），不能修改；系统不采集、不比对、不推导平台数据。</p>
          <div className={styles.actions}>
            <button className={styles.primary} disabled={busy || !loaded} onClick={save}>保存观察记录</button>
            <button disabled={busy} onClick={() => setMode("list")}>取消</button>
          </div>
        </>
      )}

      {mode === "detail" && selected && (
        <>
          <h2>{selected.data.title}</h2>
          <p className={styles.materialMeta}>
            {PLATFORM_LABELS[selected.data.platform_ref] || selected.data.platform_ref} · {selected.data.account_name} · {selected.data.period} · {selected.created_at} · 连接状态：<span className={styles.statusMuted}>未连接</span> · <span className={styles.statusMuted}>人工观察 · 未验证</span>
          </p>
          <p className={styles.sub} style={{ whiteSpace: "pre-wrap" }}>{selected.data.body}</p>
          <p className={styles.notice}>{selected.data.notice}</p>
        </>
      )}

  </fieldset></section>, [mode, selected, form, accounts, accountRef, busy, error, panelRequest, loaded, view, onSaved]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { onInspect?.(panel ? { id: JSON.stringify([company, workspaceId, "ContentGrowthObserve.js", mode, selected?.entity_id || "new"]), title: mode === "create" ? "填写资料" : selected?.data.name || selected?.data.title || selected?.data.content_title || "原始资料", content: panel, request: panelRequest } : null); }, [onInspect, panel, company, workspaceId, mode, selected, panelRequest]);
  return (
    <div className={styles.main}>
      <div className={styles.row}>
        <div>
          {embedded ? <h2>{title || "原观察与依据"}</h2> : <h1>{title || "表现与归因"}</h1>}
          {!embedded && <p className={styles.sub}>人工观察 · 未验证 · 平台未连接</p>}
        </div>
        <div className={styles.actions}>
          {mode !== "list" && <button onClick={() => { setMode("list"); setSelected(null); }}>返回列表</button>}
          <Link href={contentHref(workspaceId, { view: "production" })}>← 制作目录</Link>
        </div>
      </div>
      {error && <p className={styles.error} role="alert">{error}</p>}
      {!loaded && !error && <p role="status" className={styles.sub}>正在读取本工作区资料…</p>}

      {(
        <>
          <div className={styles.actions}>
            <button className={styles.primary} disabled={busy || !loaded} onClick={startCreate}>新建观察</button>
          </div>
          <p className={styles.sub}>人工观察 · 未验证；保留原账号与周期，证据不足时不作平台或因果结论。</p>
          {loaded && !records.length && <p className={styles.notice}>还没有表现观察。选择本业务账号，按观察周期手工记录你的观察。</p>}
          <div className={styles.toolbar}><select aria-label="观察账号筛选" value={accountFilter} onChange={(event) => setAccountFilter(event.target.value)}><option value="">全部账号</option>{accounts.map((item) => <option key={item.entity_id} value={item.entity_id}>{item.data.name}</option>)}</select><select aria-label="原观察周期筛选" value={periodFilter} onChange={(event) => setPeriodFilter(event.target.value)}><option value="">全部原周期</option>{periods.map((period) => <option key={period} value={period}>{period}</option>)}</select></div>
          {loaded && !visibleRecords.length && (accountFilter || periodFilter) && <p className={styles.emptyRow}>此账号与原周期下没有观察，不补数据。</p>}
          <div className={styles.denseRows}>
            {visibleRecords.map((record) => (
              <div key={record.entity_id} className={styles.observationRow}>
                <div className={styles.row} style={{ justifyContent: "flex-start", gap: "12px" }}>
                  <button disabled={busy} onClick={() => openDetail(record.entity_id)}>查看</button>
                  <span className={styles.selectionTitle}>{record.data.title}</span>
                  <span className={styles.statusMuted}>未连接</span>
                </div>
                <p className={styles.materialMeta}>
                  {PLATFORM_LABELS[record.data.platform_ref] || record.data.platform_ref} · {record.data.account_name} · {record.data.period} · {record.created_at}
                </p>
              </div>
            ))}
          </div>
        </>
      )}

    </div>
  );
}
