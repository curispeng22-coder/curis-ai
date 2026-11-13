"use client";
import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { eventByRef, packageForEntry } from "../../lib/writingState.mjs";
import { formalMarkdownFilename, formalSnapshotText, formalVersionNumber } from "../../lib/writingTextExport.mjs";
import { writingApi } from "../../lib/writingApi.js";
import { saveNativeWritingPackage, writingSaveFailureMessage } from "../../lib/nativeWritingExport.js";
import useWritingSurface from "./useWritingSurface.js";
import styles from "./Writing.module.css";

// Chapter event writes use SQLite current_timestamp (UTC); do not reinterpret other formats.
export function writingEventTime(value) {
  if (typeof value !== "string" || !value) return "时间未记录";
  if (/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/.test(value)) {
    const parsed = new Date(value.replace(" ", "T") + "Z");
    if (Number.isFinite(parsed.getTime()) && parsed.toISOString().slice(0, 19).replace("T", " ") === value) return `${value} UTC`;
  }
  return value;
}

export default function WritingPublishingMain({ state, entry, workspaceId, chapterTitle, command, busy, onNavigate }) {
  const surface = useWritingSurface(state.scope.company_id, workspaceId);
  const currentVersion = useRef("");
  const currentPackage = useRef("");
  const intro = useRef(null); const creditInput = useRef(null);
  const [introduction, setIntroduction] = useState(""); const [credits, setCredits] = useState(""); const [rights, setRights] = useState(false);
  const [errors, setErrors] = useState({}); const [notice, setNotice] = useState("");
  const [saving, setSaving] = useState(false);
  const [downloadFile, setDownloadFile] = useState(null);
  const formal = eventByRef(state.events, "formal.confirmed", entry.formal);
  const prepared = packageForEntry(state.events, entry);
  useEffect(() => { setRights(false); setErrors({}); setNotice(""); setDownloadFile(null); }, [formal?.ref]);
  useLayoutEffect(() => { currentVersion.current = formal?.ref || ""; currentPackage.current = prepared?.ref || ""; }, [formal?.ref, prepared?.ref]);
  const prepare = async (event) => {
    event.preventDefault(); if (!formal || busy || state.read_only) return; const token = surface.capture(), originalFormal = formal.ref; const next = {};
    if (!introduction.trim()) next.introduction = "请填写作品介绍。";
    if (!credits.trim()) next.credits = "请填写署名。";
    if (!rights) next.rights = "请确认这是作者权利声明。";
    setErrors(next);
    if (Object.keys(next).length) { if (next.introduction) intro.current.focus(); else if (next.credits) creditInput.current.focus(); return; }
    try { const result = await command("package.prepared", { formal_ref: formal.ref, introduction, credits, rights_declared: rights, target: "LOCAL_DOWNLOAD" }); if (!surface.live(token) || currentVersion.current !== originalFormal) return; onNavigate({ package: result.ref }); setNotice("本地发布包已保存。尚未发布到任何平台。"); }
    catch (reason) { if (surface.live(token) && currentVersion.current === originalFormal) setNotice(reason.message); }
  };
  const download = async () => {
    if (!prepared || saving) return;
    const token = surface.capture(), originalFormal = currentVersion.current, originalPackage = prepared.ref;
    setSaving(true); setNotice("");
    let savingStage = "FETCH_BEGIN";
    try {
      const blob = await writingApi.download(state.scope.company_id, workspaceId, entry, prepared.ref);
      savingStage = "BYTES_RECEIVED";
      if (!surface.live(token) || currentVersion.current !== originalFormal || currentPackage.current !== originalPackage) return;
      const outcome = await saveNativeWritingPackage(blob, prepared, state.scope, globalThis.window?.__TAURI_INTERNALS__, () => surface.live(token) && currentVersion.current === originalFormal && currentPackage.current === originalPackage);
      if (!surface.live(token) || currentVersion.current !== originalFormal || currentPackage.current !== originalPackage) return;
      if (outcome.status === "CANCELLED") { setNotice("已取消保存，未写入发布包文件。"); return; }
      if (outcome.status === "UNSUPPORTED") { setNotice("当前环境不支持原生保存；未完成文件下载。"); return; }
      setDownloadFile({ ref: prepared.ref, path: outcome.path, sha256: outcome.sha256 });
      setNotice("发布包文件已保存并核对字节。尚未发布到平台。");
    } catch (reason) { if (surface.live(token) && currentVersion.current === originalFormal) setNotice(writingSaveFailureMessage(reason, savingStage)); }
    finally { if (surface.live(token)) setSaving(false); }
  };
  // W-09: copy and Markdown export stay verbatim to the selected formal snapshot; candidates never render these actions.
  const copyFormal = async () => {
    if (!formal) return;
    const token = surface.capture(), originalFormal = formal.ref;
    const clipboard = globalThis.navigator?.clipboard;
    if (!clipboard || typeof clipboard.writeText !== "function") { if (currentVersion.current === originalFormal) setNotice("当前环境不支持一键复制，请直接选中正文手动复制。"); return; }
    try {
      await clipboard.writeText(formalSnapshotText(formal));
      if (surface.live(token) && currentVersion.current === originalFormal) setNotice("已复制所选正式稿正文，内容与快照逐字一致。");
    } catch { if (surface.live(token) && currentVersion.current === originalFormal) setNotice("复制未完成，请重试；正式稿快照未改动。"); }
  };
  const exportFormalMarkdown = () => {
    if (!formal) return;
    const originalFormal = formal.ref;
    try {
      const text = formalSnapshotText(formal);
      const filename = formalMarkdownFilename(chapterTitle, formalVersionNumber(state.events, formal.ref));
      const url = URL.createObjectURL(new Blob([text], { type: "text/markdown;charset=utf-8" }));
      const link = document.createElement("a"); link.href = url; link.download = filename;
      link.click(); setTimeout(() => URL.revokeObjectURL(url), 10000);
      if (currentVersion.current === originalFormal) setNotice(`已导出 Markdown 文件：${filename}。本地文件，未发布到平台。`);
    } catch { if (currentVersion.current === originalFormal) setNotice("导出未完成，请重试；正式稿快照未改动。"); }
  };

  return <div className={styles.publishing}><button onClick={() => onNavigate({ mode: "chapter" })}>← 返回同一章节</button><div className={styles.operatingHero}><div><span className={styles.badge}>本地交付</span><h2>从正式稿，准备独立发布包</h2><p>作者确认的正文快照单独保留；本地下载不等于平台发布。</p></div><span className={styles.opBadge}>平台未连接</span></div>
    <div className={styles.deliverySteps}><span>① 作者检查</span><span>② 明确确认正式稿</span><span>③ 准备本地包</span><span>④ 本地下载 · 未上线</span></div>
    <div className={styles.formalPicker}><label>选择已确认正式稿<select aria-label="已确认正式稿版本" disabled={busy} value={formal?.ref || ""} onChange={(event) => onNavigate({ formal: event.target.value, package: "" })}><option value="">请选择版本</option>{state.events.filter((event) => event.action === "formal.confirmed").map((event, index) => <option key={event.ref} value={event.ref}>正式稿 {index + 1} · {writingEventTime(event.created_at)}</option>)}</select></label><button onClick={() => onNavigate({ mode: "review" })}>前往作者检查</button></div>
    {!formal ? <section><p>{entry.formal ? "指定正式稿不存在于当前章节。" : "请选择已确认的正式稿，或返回章节完成作者检查。"}</p>{state.events.filter((e) => e.action === "formal.confirmed").map((e) => <button key={e.ref} onClick={() => onNavigate({ formal: e.ref, package: "" })}>选择正式稿 · {writingEventTime(e.created_at)}</button>)}</section> : <><section className={styles.formalSnapshot}><h3>当前选中的正式稿</h3><p>作者人工检查 · 正式稿未发布</p><details><summary>查看正式稿来源</summary><p>{formal.ref}</p></details><pre>{formal.snapshot.text}</pre><div className={styles.opActions}><button onClick={copyFormal}>复制正文</button><button onClick={exportFormalMarkdown}>导出 Markdown</button></div></section><form className={styles.packageForm} onSubmit={prepare} noValidate><fieldset disabled={busy || state.read_only} className={styles.packageFields}><label>作品介绍<textarea ref={intro} aria-label="作品介绍" aria-invalid={Boolean(errors.introduction)} aria-describedby={errors.introduction ? "writing-intro-error" : undefined} maxLength={2000} value={introduction} onChange={(e) => setIntroduction(e.target.value)} /></label>{errors.introduction && <p id="writing-intro-error" className={styles.error}>{errors.introduction}</p>}<label>署名<input ref={creditInput} aria-label="署名" maxLength={1000} aria-invalid={Boolean(errors.credits)} value={credits} onChange={(e) => setCredits(e.target.value)} /></label>{errors.credits && <p className={styles.error}>{errors.credits}</p>}<label className={styles.check}><input type="checkbox" checked={rights} onChange={(e) => setRights(e.target.checked)} />我确认已核对署名、引用及所需权利（作者声明）</label>{errors.rights && <p className={styles.error}>{errors.rights}</p>}<p>目标：本地下载。平台能力、账号和平台许可尚未验证。</p><button className={styles.primary} disabled={busy || state.read_only}>生成并保存本地发布包</button></fieldset></form></>}
    {entry.package && !prepared && <p role="alert">指定发布包不存在于当前章节，或与所选正式稿不匹配。请从历史发布包明确选择。</p>}
    {prepared && <section className={styles.section}><h3>已保存的本地发布包</h3><p>{prepared.package.metadata.introduction}</p><p>署名：{prepared.package.metadata.credits}</p><details><summary>查看发布包来源</summary><p>{prepared.formal_ref}</p></details><p>尚未发布 · 平台能力未验证 · 权利为作者声明</p><button disabled={saving} onClick={download}>{saving ? "正在选择保存位置…" : "保存本地发布包文件"}</button>{downloadFile?.ref === prepared.ref && <details><summary>已保存文件</summary><p>{downloadFile.path}</p><p>SHA256：{downloadFile.sha256}</p></details>}</section>}
    <section className={styles.section}><h3>历史发布包</h3>{state.events.filter((e) => e.action === "package.prepared").map((e) => <button key={e.ref} onClick={() => onNavigate({ package: e.ref, formal: e.formal_ref })}>打开发布包 · {writingEventTime(e.created_at)}</button>)}</section>{notice && <p role="status">{notice}</p>}
  </div>;
}
