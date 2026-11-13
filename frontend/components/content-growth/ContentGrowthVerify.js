"use client";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { TENANT_ID } from "../../lib/api.js";
import { contentGrowthApi as api } from "../../lib/contentGrowthApi.js";
import { contentHref, cgScopedRead, stableRequest } from "../../lib/contentGrowthState.mjs";
import { cgExportSelection, saveNativeContentGrowthExport } from "../../lib/nativeContentGrowthExport.js";
import styles from "./ContentGrowth.module.css";

// Platform chain S2 (contract CURIS_PLATFORM_ACCOUNT_LOCAL_CHAIN_CONTRACT §4.2, D4):
// no-send per-account publish verification + minimal LOCAL export. There is no send,
// queue or schedule control anywhere in this view; external status is always 未连接.
const PLATFORM_LABELS = { xhs: "小红书", douyin: "抖音", wechat_oa: "公众号", tiktok: "TikTok", youtube: "YouTube", bilibili: "bilibili" };

export function verifySourceContent(contents, reference, scope) {
  if (!reference || !scope?.tenant_id || !scope.company_id || !scope.workspace_id) return null;
  const matches = (contents || []).filter((item) => item.content?.entity_id === reference);
  if (matches.length !== 1) return null;
  const item = matches[0];
  if (typeof item.version?.entity_id !== "string" || !item.version.entity_id.trim()) return null;
  return [item.content, item.version].every((row) => row?.tenant_id === scope.tenant_id
    && row.company_id === scope.company_id && row.workspace_id === scope.workspace_id)
    ? item : null;
}

export default function ContentGrowthVerify({ company, workspaceId, onInspect, title, sourceRef = "" }) {
  const [listAccount, setListAccount] = useState("");
  const [records, setRecords] = useState([]), [contents, setContents] = useState([]), [accounts, setAccounts] = useState([]);
  const [panelRequest, setPanelRequest] = useState(0);
  const alive = useRef(true), readSequence = useRef(0), mutation = useRef(false), readInfo = useRef(null), commandIdentity = useRef({});
  const [loaded, setLoaded] = useState(false);
  const [readScope, setReadScope] = useState(null);
  const [returnNotice, setReturnNotice] = useState("");
  const restored = useRef(false);
  const returnKey = useCallback((ref) => `curis.cg.verifyReturn:${JSON.stringify([TENANT_ID, company, workspaceId, ref || ""])}`, [company, workspaceId]);
  const requestId = (action, base, data) => { const next = stableRequest(commandIdentity.current[action], action, base, data, () => crypto.randomUUID()); commandIdentity.current[action] = next; return next.request_id; };
  useEffect(() => { alive.current = true; return () => { alive.current = false; readSequence.current += 1; }; }, []);
  const [error, setError] = useState(""), [busy, setBusy] = useState(false);
  const [mode, setMode] = useState("list"); // list | create | detail
  const [selected, setSelected] = useState(null);
  const [contentRef, setContentRef] = useState(""), [accountRef, setAccountRef] = useState("");
  const templateSequence = useRef(0);
  const [receiptDrafts, setReceiptDrafts] = useState(new Map());
  const [template, setTemplate] = useState(null), [checks, setChecks] = useState([]);
  const [downloads, setDownloads] = useState({});
  const [saveResult, setSaveResult] = useState(null);
  const exportContext = useRef(null);
  exportContext.current = { company, workspaceId, mode, selected };
  const [receipts, setReceipts] = useState([]);
  const [receiptForm, setReceiptForm] = useState({ published_at: "", platform_post_url: "", note: "" });

  const load = useCallback(async () => {
    const ticket = ++readSequence.current;
    setError(""); setLoaded(false);
    try {
      const [verifyResult, contentResult, accountResult] = await Promise.all([
        api.verifications(company, workspaceId),
        api.collection(company, workspaceId),
        api.accounts(company, workspaceId),
      ]);
      [verifyResult, contentResult, accountResult].forEach((value) => cgScopedRead(value, company, workspaceId)); if (!alive.current || ticket !== readSequence.current) return;
      readInfo.current = verifyResult.entry; setReadScope(verifyResult.entry.scope); setLoaded(true);
      setRecords(verifyResult.verifications || []);
      setContents(contentResult.contents || []);
      setAccounts(accountResult.accounts || []);
      if (!restored.current) {
        restored.current = true;
        try {
          const saved = JSON.parse(window.sessionStorage.getItem(returnKey(sourceRef)) || "null");
          if (saved) {
            window.sessionStorage.removeItem(returnKey(sourceRef));
            const original = verifySourceContent(contentResult.contents, saved.contentRef, contentResult.entry.scope);
            if (saved.tenant === TENANT_ID && saved.company === company && saved.workspace === workspaceId && saved.explicit === true
              && saved.contentRef === sourceRef && original && original.version.entity_id === saved.versionRef) {
              setContentRef(saved.contentRef); setMode("create"); setPanelRequest((value) => value + 1);
              setReturnNotice("已保留你明确选择的内容。请选择本地账号并逐项核对，尚未保存核验。");
            } else setReturnNotice("原内容或版本已变化，请重新明确选择；没有自动替换或保存核验。");
          }
        } catch { setReturnNotice("未能恢复原选择，请重新选择内容；没有自动保存核验。"); }
      }
    } catch (reason) { if (alive.current && ticket === readSequence.current) setError(reason.message); }
  }, [company, workspaceId, sourceRef, returnKey]);

  useEffect(() => { load(); return () => {
    setDownloads((current) => { Object.values(current).forEach((url) => URL.revokeObjectURL(url)); return {}; });
  }; }, [load]);

  const pickedAccount = accounts.find((item) => item.entity_id === accountRef) || null;
  const sourceContent = loaded ? verifySourceContent(contents, sourceRef, readScope) : null;
  const selectedContent = verifySourceContent(contents, contentRef, readScope);
  const accountReturnRef = selectedContent ? contentRef : sourceContent?.content.entity_id || "";
  const keepChoiceForAccounts = (event) => {
    if (busy || !loaded || accounts.length) { event.preventDefault(); return; }
    if (!contentRef) return;
    if (!selectedContent) { event.preventDefault(); setError("当前内容无法唯一确认，请重新选择。"); return; }
    try {
      window.sessionStorage.setItem(returnKey(contentRef), JSON.stringify({ tenant: TENANT_ID, company, workspace: workspaceId,
        contentRef, versionRef: selectedContent.version.entity_id, explicit: true }));
    } catch { event.preventDefault(); setError("暂时无法保留原内容选择，请重试；当前表单未关闭。"); }
  };


  const startCreate = () => {
    if (mutation.current) return;
    setPanelRequest((value) => value + 1); setMode("create");
  };

  const chooseAccount = async (ref) => {
    const ticket = ++templateSequence.current;
    setAccountRef(ref); setTemplate(null); setChecks([]);
    if (!ref) return;
    const account = accounts.find((item) => item.entity_id === ref);
    if (!account) return;
    setBusy(true); setError("");
    try {
      const result = await api.verificationTemplate(company, workspaceId, account.data.platform_ref);
      cgScopedRead(result, company, workspaceId); if (!alive.current || ticket !== templateSequence.current) return;
      if (result.platform !== account.data.platform_ref) throw new Error("检查模板与当前账号平台不一致，请重新选择。");
      setTemplate(result);
      setChecks(result.checks.map((item) => ({ ...item, checked: false, note: "" })));
    } catch (reason) { if (alive.current && ticket === templateSequence.current) setError(reason.message); } finally { if (alive.current && ticket === templateSequence.current) setBusy(false); }
  };

  const toggleCheck = (key) => setChecks((prev) => prev.map((item) => item.key === key ? { ...item, checked: !item.checked } : item));
  const setNote = (key) => (event) => setChecks((prev) => prev.map((item) => item.key === key ? { ...item, note: event.target.value } : item));

  const save = async () => {
    if (mutation.current || !alive.current || !loaded) return;
    if (!verifySourceContent(contents, contentRef, readScope)) { setError("请显式选择一篇当前工作空间的既有内容。"); return; }
    if (!accountRef) { setError("请选择目标经营账号。"); return; }
    if (!template?.checks?.length) { setError("检查模板尚未就绪。"); return; }
    const data = { content_ref: contentRef, account_ref: accountRef, checks: checks.map(({ key, checked, note }) => ({ key, checked, note: note.trim() })) };
    mutation.current = true; setBusy(true); setError("");
    try {
      await api.verificationCreate(company, workspaceId, requestId("save-verification", "", data), data);
      if (!alive.current) return;
      setReturnNotice("");
      commandIdentity.current["save-verification"] = null; setContentRef(""); setAccountRef(""); setTemplate(null); setChecks([]);
      setMode("list");
      await load();
    } catch (reason) { if (alive.current) setError(reason.message); } finally { mutation.current = false; if (alive.current) setBusy(false); }
  };

  const openDetail = async (ref) => {
    if (mutation.current) return;
    const ticket = ++readSequence.current; setBusy(true); setError("");
    try {
      const [detail, receiptResult] = await Promise.all([
        api.verification(company, workspaceId, ref),
        api.receipts(company, workspaceId, ref),
      ]);
      if (!alive.current || ticket !== readSequence.current) return;
      if (detail.entity_id !== ref || detail.company_id !== company || detail.data.business_ref !== readInfo.current?.scope.business_id) throw new Error("核验范围已变化，请重新选择。");
      cgScopedRead(receiptResult, company, workspaceId);
      setSelected(detail);
      setReceipts(receiptResult.receipts || []);
      setReceiptForm(receiptDrafts.get(ref) || { published_at: "", platform_post_url: "", note: "" });
      setPanelRequest((value) => value + 1); setMode("detail");
    } catch (reason) { if (alive.current && ticket === readSequence.current) setError(reason.message); } finally { if (alive.current && ticket === readSequence.current) setBusy(false); }
  };

  const setReceiptField = (key) => (event) => { const next = { ...receiptForm, [key]: event.target.value }; if (selected) setReceiptDrafts((current) => { const saved = new Map(current); saved.set(selected.entity_id, next); return saved; }); setReceiptForm(next); };

  const saveReceipt = async () => {
    if (mutation.current || !alive.current || !loaded) return;
    const data = {
      published_at: receiptForm.published_at.trim(),
      platform_post_url: receiptForm.platform_post_url.trim(),
      note: receiptForm.note.trim(),
    };
    if (!data.published_at && !data.platform_post_url && !data.note) { setError("请至少回填一项（发布时间、平台链接或备注）。"); return; }
    mutation.current = true; setBusy(true); setError("");
    try {
      await api.receiptCreate(company, workspaceId, selected.entity_id, requestId("save-receipt", selected.entity_id, data), data);
      const receiptResult = await api.receipts(company, workspaceId, selected.entity_id);
      cgScopedRead(receiptResult, company, workspaceId); if (!alive.current) return;
      commandIdentity.current["save-receipt"] = null;
      setReceiptDrafts((current) => { const saved = new Map(current); saved.delete(selected.entity_id); return saved; });
      setReceipts(receiptResult.receipts || []);
      setReceiptForm({ published_at: "", platform_post_url: "", note: "" });
    } catch (reason) { if (alive.current) setError(reason.message); } finally { mutation.current = false; if (alive.current) setBusy(false); }
  };

  const exportFile = async (ref) => {
    if (mutation.current || !alive.current || !loaded || mode !== "detail" || selected?.entity_id !== ref) return;
    const record = selected, ticket = readSequence.current;
    const isCurrent = () => alive.current && ticket === readSequence.current
      && exportContext.current?.company === company && exportContext.current?.workspaceId === workspaceId
      && exportContext.current?.mode === "detail" && exportContext.current?.selected === record;
    if (!isCurrent()) return;
    mutation.current = true; setBusy(true); setError(""); setSaveResult(null);
    try {
      const selection = cgExportSelection(record, company, readInfo.current?.scope.business_id);
      const blob = await api.verificationExport(company, workspaceId, ref);
      if (!isCurrent()) return;
      if (globalThis.window?.__TAURI_INTERNALS__) {
        const outcome = await saveNativeContentGrowthExport(blob, selection, undefined, isCurrent);
        if (isCurrent()) setSaveResult({ ref, company, workspaceId, ...outcome });
      } else {
        setDownloads((current) => {
          if (current[ref]) URL.revokeObjectURL(current[ref]);
          return { ...current, [ref]: URL.createObjectURL(blob) };
        });
      }
    } catch (reason) { if (isCurrent()) setError(reason.message); }
    finally { mutation.current = false; if (alive.current) setBusy(false); }
  };

  const passedCount = (items) => items.filter((item) => item.checked).length;

  const panel = useMemo(() => mode === "list" ? null : <section className={`${styles.main} ${styles.utility}`}><fieldset disabled={busy}><button disabled={busy} className={styles.formDismiss} onClick={() => setMode("list")}>← 返回列表</button>{error && <p className={styles.error} role="alert">{error}</p>}
      {mode === "create" && (
        <>
          <h2>新建发布核验</h2><p className={styles.sub}>先选择正文与账号，再按原平台模板人工核对。</p>
          {sourceRef && loaded && <section aria-label="核验来源" className={styles.notice}>
            {sourceContent ? <><p>来源内容：{sourceContent.version.data.title || "未命名内容"}</p><button type="button" disabled={busy} onClick={() => setContentRef(sourceContent.content.entity_id)}>使用这篇内容</button><Link href={contentHref(workspaceId, { content: sourceContent.content.entity_id })}>返回来源内容</Link></> : <p>原内容无法唯一确认，请从当前工作空间重新选择；没有自动选择其他内容。</p>}
          </section>}
          <div className={styles.fields} style={{ gridTemplateColumns: "1fr" }}>
            <label>核验内容（当前工作空间的既有内容）
              <select value={contentRef} onChange={(event) => setContentRef(event.target.value)}>
                <option value="">选择内容</option>
                {contents.map((item) => <option key={item.content.entity_id} value={item.content.entity_id}>{item.version.data.title || "未命名内容"}</option>)}
              </select>
            </label>
            <label>目标经营账号（本业务可见）
              <select value={accountRef} onChange={(event) => chooseAccount(event.target.value)}>
                <option value="">选择账号</option>
                {accounts.map((item) => <option key={item.entity_id} value={item.entity_id}>{PLATFORM_LABELS[item.data.platform_ref] || item.data.platform_ref} · {item.data.name}（未连接）</option>)}
              </select>
            </label>
          </div>
          {loaded && !accounts.length && <section aria-label="本地账号前置条件" className={styles.notice}>
            <p>当前业务还没有本地账号。先登记账号资料，再回来选择并逐项核对；登记不会连接或发布到平台。</p>
            <Link href={contentHref(workspaceId, { view: "accounts", object: accountReturnRef })} onClick={keepChoiceForAccounts}>先登记本地账号</Link>
          </section>}
          {pickedAccount && <p className={styles.materialMeta}>{pickedAccount.data.name} 连接状态：<span className={styles.statusMuted}>未连接</span>；核验仅在本地进行。</p>}
          <div className={styles.actions}><button disabled={busy} onClick={() => setMode("list")}>取消，保留输入</button></div>
          {template && (
            <>
              <div className={styles.materialList}>
                {checks.map((item) => (
                  <label key={item.key} className={styles.materialItem}>
                    <span className={styles.row} style={{ justifyContent: "flex-start", gap: "8px" }}>
                      <input type="checkbox" checked={item.checked} onChange={() => toggleCheck(item.key)} />
                      <span className={styles.selectionTitle}>{item.label}</span>
                    </span>
                    <input value={item.note} placeholder="核对备注（可选）" onChange={setNote(item.key)} />
                  </label>
                ))}
              </div>
              <p className={styles.notice}>未勾选项也会如实记录为未通过；记录保存后不可修改。平台连接与发布能力在当前版本不存在。</p>
              <div className={styles.actions}>
                <button className={styles.primary} disabled={busy || !loaded} onClick={save}>保存核验记录</button>
                <button disabled={busy} onClick={() => setMode("list")}>取消</button>
              </div>
            </>
          )}
        </>
      )}

      {mode === "detail" && selected && (
        <>
          <h2>{selected.data.content_title || "未命名内容"}</h2>
          <p className={styles.materialMeta}>
            {selected.data.platform_name} · {selected.data.account_name} · {selected.created_at} · 连接状态：<span className={styles.statusMuted}>未连接</span> ·
            <span className={styles.statusMuted}> 人工核对 · 未验证</span>
          </p>
          <div className={styles.materialList}>
            {selected.data.checks.map((item) => (
              <div key={item.key} className={styles.materialItem}>
                <div className={styles.row} style={{ justifyContent: "flex-start", gap: "8px" }}>
                  <span className={item.checked ? styles.statusDone : styles.statusWarn}>{item.checked ? "已核对" : "未通过"}</span>
                  <span className={styles.selectionTitle}>{item.label}</span>
                </div>
                {item.note && <p className={styles.materialMeta}>{item.note}</p>}
              </div>
            ))}
          </div>
          <p className={styles.notice}>本记录为时点不可变的人工核验证据（未验证），不构成已发布事实。</p>
          <div className={styles.actions}>
            <button className={styles.primary} disabled={busy || !loaded} onClick={() => exportFile(selected.entity_id)}>导出本地文件</button>
            {!globalThis.window?.__TAURI_INTERNALS__ && downloads[selected.entity_id] && <a href={downloads[selected.entity_id]} download={`cg-local-verification-${selected.entity_id.replace("cg-verify-", "").slice(0, 8)}.json`}>保存 JSON 文件</a>}
          </div>

          {saveResult?.ref === selected.entity_id && saveResult.company === company && saveResult.workspaceId === workspaceId && (
            <p role="status">{saveResult.status === "SAVED" ? "本地文件已保存并读回核验；未发布到平台。" : "已取消保存，原核验记录保留。"}</p>
          )}

          <h2 style={{ marginTop: "24px" }}>人工发布回执</h2>
          <p className={styles.sub}>你在平台手动发布后，可在此人工回填；系统不访问链接、不验证结果，回执恒为「人工回填 · 未验证」。</p>
          {!receipts.length && <p className={styles.notice}>还没有回执。回填不等于已验证发布；无发送、无排队、无定时。</p>}
          <div className={styles.materialList}>
            {receipts.map((item) => (
              <div key={item.entity_id} className={styles.materialItem}>
                <div className={styles.row} style={{ justifyContent: "flex-start", gap: "8px" }}>
                  <span className={styles.statusWarn}>人工回填 · 未验证</span>
                  <span className={styles.statusMuted}>未连接</span>
                  {item.data.published_at && <span className={styles.selectionTitle}>{item.data.published_at}</span>}
                </div>
                {item.data.platform_post_url && (
                  <p className={styles.materialMeta}>平台链接（人工回填 · 未验证，系统不访问）：<br />{item.data.platform_post_url}</p>
                )}
                {item.data.note && <p className={styles.materialMeta}>{item.data.note}</p>}
                <p className={styles.statusMuted}>{item.created_at}</p>
              </div>
            ))}
          </div>
          <div className={styles.fields} style={{ gridTemplateColumns: "1fr", marginTop: "12px" }}>
            <label>发布时间（可选，手工填写）
              <input value={receiptForm.published_at} maxLength={200} placeholder="例如：2026-10-08 20:15" onChange={setReceiptField("published_at")} />
            </label>
            <label>平台链接（可选，http/https；仅留档，系统不会访问）
              <input value={receiptForm.platform_post_url} maxLength={2000} placeholder="https://…" onChange={setReceiptField("platform_post_url")} />
            </label>
            <label>备注（可选）
              <textarea rows={3} value={receiptForm.note} maxLength={2000} placeholder="人工回填备注" onChange={setReceiptField("note")} />
            </label>
          </div>
          <div className={styles.actions}>
            <button disabled={busy} onClick={saveReceipt}>保存回执</button>
          </div>
        </>
      )}

  </fieldset></section>, [company, workspaceId, mode, selected, contents, accounts, contentRef, accountRef, template, checks, pickedAccount, receiptForm, receipts, downloads, saveResult, busy, error, panelRequest, loaded, sourceRef, returnNotice, readScope]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { onInspect?.(panel ? { id: JSON.stringify([company, workspaceId, "ContentGrowthVerify.js", mode, selected?.entity_id || "new"]), title: mode === "create" ? "填写资料" : selected?.data.name || selected?.data.title || selected?.data.content_title || "原始资料", content: panel, request: panelRequest } : null); }, [onInspect, panel, company, workspaceId, mode, selected, panelRequest]);
  return (
    <div className={styles.main}>
      <div className={styles.row}>
        <div>
          <h1>发布核验</h1>
          <p className={styles.sub}>逐项人工勾核 · 本地保存时点记录 · 不发送、不排队、不定时 · 平台未连接</p>
        </div>
        <div className={styles.actions}>
          {mode !== "list" && <button disabled={busy} onClick={() => { if (!mutation.current) { setMode("list"); setSelected(null); } }}>返回列表</button>}
          <Link href={contentHref(workspaceId, { view: "production" })}>← 制作目录</Link>
        </div>
      </div>
      {error && <p className={styles.error} role="alert">{error}</p>}
      {returnNotice && <p role="status" className={styles.notice}>{returnNotice}</p>}
      {loaded && sourceRef && mode === "list" && <section aria-label="核验来源" className={styles.notice}>{sourceContent ? <><p>来源内容：{sourceContent.version.data.title || "未命名内容"}。新建核验后请明确选用。</p><Link href={contentHref(workspaceId, { content: sourceRef })}>返回来源内容</Link></> : <p>原内容无法唯一确认，请重新选择当前工作空间的内容。</p>}</section>}
      {!loaded && !error && <p role="status" className={styles.sub}>正在读取本工作区资料…</p>}

      {(
        <>
          <div className={styles.actions}>
            <button className={styles.primary} disabled={busy || !loaded} onClick={startCreate}>新建核验</button>
          </div>
          <p className={styles.notice}>核验记录与本地导出不构成发布；当前版本没有任何平台连接、发送或定时能力，外部状态恒为「未连接」。</p>
          {loaded && !records.length && <p className={styles.notice}>还没有核验记录。选择一篇既有内容与一个经营账号，逐项核对后保存。</p>}
          <div className={styles.toolbar}><select aria-label="核验账号筛选" value={listAccount} onChange={(event) => setListAccount(event.target.value)}><option value="">全部经营账号</option>{accounts.map((item) => <option key={item.entity_id} value={item.entity_id}>{item.data.name} · 未连接</option>)}</select></div>
          <div className={styles.denseRows}>
            {records.filter((item) => !listAccount || item.data.account_ref === listAccount).map((record) => (
              <div key={record.entity_id} className={styles.observationRow}>
                <div className={styles.row} style={{ justifyContent: "flex-start", gap: "12px" }}>
                  <button disabled={busy} onClick={() => openDetail(record.entity_id)}>查看</button>
                  <span className={styles.selectionTitle}>{record.data.content_title || "未命名内容"}</span>
                  <span className={styles.statusMuted}>未连接</span>
                </div>
                <p className={styles.materialMeta}>
                  {record.data.platform_name} · {record.data.account_name} · 核对通过 {passedCount(record.data.checks)}/{record.data.checks.length} · {record.created_at}
                </p>
              </div>
            ))}
          </div>
        </>
      )}

    </div>
  );
}
