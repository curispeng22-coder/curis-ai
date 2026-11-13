"use client";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { contentGrowthApi as api } from "../../lib/contentGrowthApi.js";
import { contentHref, cgScopedRead } from "../../lib/contentGrowthState.mjs";
import styles from "./ContentGrowth.module.css";

// Platform chain S1 (contract CURIS_PLATFORM_ACCOUNT_LOCAL_CHAIN_CONTRACT §2/§4.1):
// local ChannelAccount CRUD with honest NOT_CONNECTED projection. No connection,
// no publishing, no outbound. connection_status is server-owned and never sent.
const PLATFORM_LABELS = { xhs: "小红书", douyin: "抖音", wechat_oa: "公众号", tiktok: "TikTok", youtube: "YouTube", bilibili: "bilibili" };
const GROWTH_STAGE_LABELS = { cold_start: "冷启动", growing: "成长期", mature: "成熟期", declining_transforming: "衰退/转型" };
const STATUS_LABELS = { active: "经营中", dormant: "休眠", banned: "封禁/受限" };
const EMPTY_FORM = { platform_ref: "", name: "", positioning: "", audience: "", content_mix: "", cadence: "", voice: "", responsibility: "", growth_stage: "cold_start", status: "active" };

const statusClass = (status) => status === "active" ? styles.statusDone : status === "banned" ? styles.statusWarn : styles.statusMuted;

export default function ContentGrowthAccounts({ company, workspaceId, onInspect, title, sourceRef = "", sourceContent = null }) {
  const [platformFilter, setPlatformFilter] = useState(""), [query, setQuery] = useState("");
  const [catalog, setCatalog] = useState([]), [accounts, setAccounts] = useState([]);
  const [panelRequest, setPanelRequest] = useState(0);
  const alive = useRef(true), readSequence = useRef(0), mutation = useRef(false), readInfo = useRef(null);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => { alive.current = true; return () => { alive.current = false; readSequence.current += 1; }; }, []);
  const [error, setError] = useState(""), [busy, setBusy] = useState(false);
  const [mode, setMode] = useState("list"); // list | create | detail | edit
  const [selected, setSelected] = useState(null);
  const [form, setForm] = useState({ ...EMPTY_FORM });
  const [drafts, setDrafts] = useState({ create: { ...EMPTY_FORM }, edits: new Map() });

  const load = useCallback(async () => {
    const ticket = ++readSequence.current;
    setError("");
    try {
      const result = await api.accounts(company, workspaceId);
      cgScopedRead(result, company, workspaceId); if (!alive.current || ticket !== readSequence.current) return;
      readInfo.current = result.entry; setLoaded(true);
      setCatalog(result.catalog || []);
      setAccounts(result.accounts || []);
      return result;
    } catch (reason) { if (alive.current && ticket === readSequence.current) setError(reason.message); }
  }, [company, workspaceId]);

  useEffect(() => { load(); }, [load]);

  const setField = (key) => (event) => { const next = { ...form, [key]: event.target.value }; setDrafts((current) => { if (mode !== "edit" || !selected) return { ...current, create: next }; const edits = new Map(current.edits); edits.set(selected.entity_id, next); return { ...current, edits }; }); setForm(next); };

  const formPayload = () => ({
    name: form.name.trim(), positioning: form.positioning.trim(), audience: form.audience.trim(),
    content_mix: form.content_mix.trim(), cadence: form.cadence.trim(), voice: form.voice.trim(),
    growth_stage: form.growth_stage, responsibility: form.responsibility.trim(), status: form.status,
  });

  const create = async () => {
    if (mutation.current || !alive.current || !loaded) return;
    if (!form.platform_ref || !form.name.trim()) { setError("请选择平台并填写账号名。"); return; }
    mutation.current = true; setBusy(true); setError("");
    try {
      await api.accountCreate(company, workspaceId, { platform_ref: form.platform_ref, ...formPayload() });
      if (!alive.current) return;
      setDrafts((current) => ({ ...current, create: { ...EMPTY_FORM } })); setForm({ ...EMPTY_FORM }); setMode("list");
      await load();
    } catch (reason) { if (alive.current) setError(reason.message); } finally { mutation.current = false; if (alive.current) setBusy(false); }
  };

  const edit = async () => {
    if (mutation.current || !alive.current || !loaded) return;
    if (!form.name.trim()) { setError("账号名不能为空。"); return; }
    mutation.current = true; setBusy(true); setError("");
    try {
      await api.accountEdit(company, workspaceId, selected.entity_id, formPayload());
      if (!alive.current) return;
      setDrafts((current) => { const edits = new Map(current.edits); edits.delete(selected.entity_id); return { ...current, edits }; }); setMode("list"); setSelected(null);
      await load();
    } catch (reason) { if (alive.current) setError(reason.message); } finally { mutation.current = false; if (alive.current) setBusy(false); }
  };

  const openDetail = async (ref) => {
    const ticket = ++readSequence.current; setBusy(true); setError("");
    try {
      const value = await api.account(company, workspaceId, ref);
      if (!alive.current || ticket !== readSequence.current) return;
      if (value.entity_id !== ref || value.company_id !== company || value.data.business_ref !== readInfo.current?.scope.business_id) throw new Error("账号范围已变化，请重新选择。");
      setSelected(value);
      setPanelRequest((value) => value + 1); setMode("detail");
    } catch (reason) { if (alive.current && ticket === readSequence.current) setError(reason.message); } finally { if (alive.current && ticket === readSequence.current) setBusy(false); }
  };

  const startEdit = (account) => {
    const data = account.data;
    setForm(drafts.edits.get(account.entity_id) || { platform_ref: data.platform_ref, name: data.name, positioning: data.positioning || "", audience: data.audience || "",
      content_mix: data.content_mix || "", cadence: data.cadence || "", voice: data.voice || "",
      growth_stage: data.growth_stage, responsibility: data.responsibility || "", status: data.status });
    setSelected(account); setPanelRequest((value) => value + 1); setMode("edit");
  };

  const platformName = (ref) => catalog.find((item) => item.platform === ref)?.name || PLATFORM_LABELS[ref] || ref;
  const textFields = [["positioning", "定位"], ["audience", "受众画像"], ["content_mix", "内容结构配比"], ["cadence", "发布节奏"], ["voice", "语感"], ["responsibility", "经营责任归属"]];

  const visibleAccounts = accounts.filter((item) => (!platformFilter || item.data.platform_ref === platformFilter) && `${item.data.name} ${item.data.positioning || ""}`.includes(query));
  const panel = useMemo(() => mode === "list" ? null : <section className={`${styles.main} ${styles.utility}`}><fieldset disabled={busy}><button disabled={busy} className={styles.formDismiss} onClick={() => setMode("list")}>← 返回列表</button>{error && <p className={styles.error} role="alert">{error}</p>}
      {(mode === "create" || mode === "edit") && (
        <>
          <h2>{mode === "create" ? "登记本地账号" : "编辑账号"}</h2>
          <div className={styles.fields} style={{ gridTemplateColumns: "1fr" }}>
            <label>平台
              <select value={form.platform_ref} disabled={mode === "edit"} onChange={setField("platform_ref")}>
                <option value="">选择平台</option>
                {catalog.map((item) => <option key={item.platform} value={item.platform}>{item.name}</option>)}
              </select>
            </label>
            <label>账号名<input value={form.name} onChange={setField("name")} /></label>
            {textFields.map(([key, label]) => (
              <label key={key}>{label}{key === "positioning" || key === "responsibility"
                ? <textarea rows={2} value={form[key]} onChange={setField(key)} />
                : <input value={form[key]} onChange={setField(key)} />}</label>
            ))}
            <label>经营阶段
              <select value={form.growth_stage} onChange={setField("growth_stage")}>
                {Object.entries(GROWTH_STAGE_LABELS).map(([value, label]) => <option key={value} value={value}>{label}</option>)}
              </select>
            </label>
            <label>账号状态
              <select value={form.status} onChange={setField("status")}>
                {Object.entries(STATUS_LABELS).map(([value, label]) => <option key={value} value={value}>{label}</option>)}
              </select>
            </label>
          </div>
          <p className={styles.notice}>平台连接与发布能力在当前版本不存在；账号信息仅本地保存，外部状态恒为「未连接」。</p>
          <div className={styles.actions}>
            <button className={styles.primary} disabled={busy || !loaded} onClick={mode === "create" ? create : edit}>{mode === "create" ? "登记本地账号" : "保存修改"}</button>
            <button disabled={busy} onClick={() => { setMode("list"); setSelected(null); }}>取消</button>
          </div>
        </>
      )}
      {mode === "detail" && selected && (
        <>
          <h2>{selected.data.name}</h2>
          <p className={styles.materialMeta}>
            {platformName(selected.data.platform_ref)} · {GROWTH_STAGE_LABELS[selected.data.growth_stage] || selected.data.growth_stage} ·
            <span className={statusClass(selected.data.status)}> {STATUS_LABELS[selected.data.status] || selected.data.status}</span> · 连接状态：<span className={styles.statusMuted}>未连接</span>
          </p>
          <div className={styles.fields} style={{ gridTemplateColumns: "1fr" }}>
            {textFields.map(([key, label]) => (
              <label key={key}>{label}<input readOnly value={selected.data[key] || "未填写"} /></label>
            ))}
          </div>
          <div className={styles.actions}>
            <button className={styles.primary} disabled={busy || !loaded} onClick={() => startEdit(selected)}>编辑</button>
          </div>
        </>
      )}

  </fieldset></section>, [mode, selected, form, catalog, busy, error, panelRequest, loaded]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { onInspect?.(panel ? { id: JSON.stringify([company, workspaceId, "ContentGrowthAccounts.js", mode, selected?.entity_id || "new"]), title: mode === "create" ? "填写资料" : selected?.data.name || selected?.data.title || selected?.data.content_title || "原始资料", content: panel, request: panelRequest } : null); }, [onInspect, panel, company, workspaceId, mode, selected, panelRequest]);
  return (
    <div className={styles.main}>
      <div className={styles.row}>
        <div>
          <h1>经营账号</h1>
          <p className={styles.sub}>同业务跨工作区持续经营 · 本地维护，平台未连接</p>
        </div>
        <div className={styles.actions}>
          {mode !== "list" && <button onClick={() => { setMode("list"); setSelected(null); }}>返回列表</button>}
          <Link href={contentHref(workspaceId, { view: "production" })}>← 制作目录</Link>
        </div>
      </div>
      {error && <p className={styles.error} role="alert">{error}</p>}
      <section aria-label="返回发布核验" className={styles.notice}>
        {sourceRef ? sourceContent?.content.entity_id === sourceRef ? <p>来源内容：{sourceContent.version.data.title || "未命名内容"}。登记仅保存在本地，不会连接或发布到平台。</p> : <p>原内容无法唯一确认。返回后请重新选择当前工作空间的内容。</p> : <p>登记仅保存在本地。完成后可返回发布核验，显式选择内容与账号。</p>}
        <Link href={contentHref(workspaceId, { view: "verify", object: sourceContent?.content.entity_id === sourceRef ? sourceRef : undefined })}>返回发布核验</Link>
      </section>
      {(
        <>
          <div className={styles.actions}>
            <button className={styles.primary} disabled={busy || !loaded} onClick={() => { setForm(drafts.create); setPanelRequest((value) => value + 1); setMode("create"); }}>登记本地账号</button>
          </div>
          {loaded && !accounts.length && <p className={styles.notice}>还没有账号。登记后可在本业务内跨内容工作区复用；平台连接在当前版本不可用，账号恒显示「未连接」。</p>}
          {loaded && <div className={styles.platforms}>{catalog.map((item) => <button key={item.platform} className={`${styles.platform} ${platformFilter === item.platform ? styles.selected : ""}`} aria-pressed={platformFilter === item.platform} onClick={() => setPlatformFilter(platformFilter === item.platform ? "" : item.platform)}><strong>{item.name}</strong><span>{accounts.filter((account) => account.data.platform_ref === item.platform).length} 个账号</span><small>未连接</small></button>)}</div>}
          <div className={styles.toolbar}><input aria-label="搜索经营账号" placeholder="搜索账号与定位" value={query} onChange={(event) => setQuery(event.target.value)} />{(query || platformFilter) && <button onClick={() => { setPlatformFilter(""); setQuery(""); }}>清除筛选</button>}</div>
          {loaded && !visibleAccounts.length && (query || platformFilter) && <p className={styles.emptyRow}>没有匹配的账号，调整筛选后再试。</p>}
          <div className={styles.denseRows}>
            {visibleAccounts.map((account) => (
              <div key={account.entity_id} className={styles.observationRow}>
                <div className={styles.row} style={{ justifyContent: "flex-start", gap: "12px" }}>
                  <button disabled={busy} onClick={() => openDetail(account.entity_id)}>查看</button>
                  <button disabled={busy} onClick={() => startEdit(account)}>编辑</button>
                  <span className={styles.selectionTitle}>{account.data.name}</span>
                  <span className={styles.statusMuted}>未连接</span>
                </div>
                <p className={styles.materialMeta}>
                  {platformName(account.data.platform_ref)} · {GROWTH_STAGE_LABELS[account.data.growth_stage] || account.data.growth_stage} ·
                  <span className={statusClass(account.data.status)}> {STATUS_LABELS[account.data.status] || account.data.status}</span>
                </p>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
