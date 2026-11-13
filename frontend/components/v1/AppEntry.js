"use client";
import { AVATAR_PRESETS } from "../../lib/avatarPresets.mjs";

import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { CEO_ID } from "../../lib/api.js";
import { createFoundingRun, getFoundingRun, getRuntimeCompany, materializeFoundingCompany, transitionRuntimeEntity } from "../../lib/runtimeApi.js";
import { getV1Presentation, saveV1Presentation } from "../../lib/v1FrontendApi.js";
import { useRuntime } from "../runtime/RuntimeProvider.js";
import TerraShell from "../terra/TerraShell.js";

const SETUP_KEY = "curis.company-setup.v1";
const SETUP_API = { createFoundingRun, getFoundingRun, getRuntimeCompany, materializeFoundingCompany, transitionRuntimeEntity, saveV1Presentation };
const AVATAR_BYTES = 194_000;
function inputError(message) { return Object.assign(new Error(message), { setupInputRejected: true }); }
export function validateSetupValues(value) {
  const display_name = String(value.display_name || "").trim(), company_name = String(value.company_name || "").trim(), avatar_ref = value.avatar_ref || "";
  if (!display_name || [...display_name].length > 80 || /[\u0000-\u001f\u007f]/.test(display_name)) throw inputError("称呼需为1–80字，不能包含换行或控制字符。");
  if (!company_name || [...company_name].length > 120 || /[\u0000-\u001f\u007f]/.test(company_name)) throw inputError("公司名称需为1–120字，不能包含换行或控制字符。");
  if (typeof avatar_ref !== "string" || avatar_ref.length > 260_000 || (avatar_ref && !avatar_ref.startsWith("preset:") && !/^data:image\/(png|jpeg|webp);base64,/.test(avatar_ref))) throw inputError("头像过大或格式不支持。请选择194KB以内图片，或移除头像后继续。");
  return { display_name, company_name, avatar_ref };
}
// A lost initial run response may leave an empty run. It cannot create a Company.
// Once the server assigns a run ID, every retry queries that same run first.
export async function completeCompanySetup(operation, checkpoint, api = SETUP_API) {
  validateSetupValues(operation.values);
  if (!operation.runId && !operation.runRequested) {
    try { await api.saveV1Presentation({ welcome_dismissed: true, display_name: operation.values.display_name, avatar_ref: operation.values.avatar_ref }); }
    catch (reason) { if ([400, 413, 422].includes(reason.status)) reason.setupInputRejected = true; throw reason; }
  }
  if (!operation.runId) {
    operation.runRequested = true; checkpoint(operation);
    const run = await api.createFoundingRun({ owner_ref: CEO_ID, intent_ref: "company-setup", org_version: "org-v1", blueprint_version: "" });
    operation.runId = run.entity_id; checkpoint(operation);
  }
  let current = await api.getFoundingRun(operation.runId);
  if (current.entity_id !== operation.runId || current.owner_ref !== CEO_ID) throw new Error("原建公司记录身份不一致，请保留记录并核对。");
  const steps = [["ARRIVED", "INTENT_CAPTURED", "capture_intent"], ["INTENT_CAPTURED", "CLARIFYING", "request_clarification"], ["CLARIFYING", "PROPOSED", "propose_company"], ["PROPOSED", "CEO_CONFIRMED", "confirm_company"]];
  for (const [from, target, trigger] of steps) {
    if (current.lifecycle_status !== from) continue;
    await api.transitionRuntimeEntity(operation.runId, { target, actor: "CEO", trigger, reason: "CEO 确认公司最小设定", evidenceRefs: [], context: {} });
    current = await api.getFoundingRun(operation.runId);
    if (current.lifecycle_status !== target) throw new Error("公司步骤尚未确认，请查询原记录后重试。");
  }
  if (current.lifecycle_status === "COMPANY_CREATED") {
    if (current.company_id !== operation.companyId) throw new Error("原建公司记录对应另一家公司，请核对。");
    const snapshot = await api.getRuntimeCompany(operation.companyId);
    const company = snapshot.company || snapshot;
    if (company.company_id !== operation.companyId || company.name !== operation.values.company_name) throw new Error("原公司设定尚未核实，请保留记录。");
    return snapshot;
  }
  if (current.lifecycle_status !== "CEO_CONFIRMED") throw new Error("原建公司步骤不可继续，请核对原记录。");
  return api.materializeFoundingCompany(operation.runId, { company_id: operation.companyId, ceo_id: CEO_ID, name: operation.values.company_name });
}

const PRESETS = AVATAR_PRESETS;

function PrimaryButton({ children, className = "", ...props }) {
  return <button {...props} className={`rounded-xl bg-ui-primary px-5 py-3 text-sm font-semibold text-ui-primary-fg shadow-ui transition hover:bg-ui-primary-dark disabled:cursor-not-allowed disabled:opacity-50 ${className}`}>{children}</button>;
}

function Welcome({ onCreate, onSkip, busy, error }) {
  return <main className="grid min-h-screen place-items-center bg-ui-bg px-6 text-ui-txt"><section className="w-full max-w-[680px] text-center"><div className="mx-auto grid h-14 w-14 place-items-center rounded-2xl bg-ui-primary text-xl font-bold text-ui-primary-fg">C</div><span className="mt-7 inline-flex rounded-full border border-ui-line bg-ui-primary-soft px-3 py-1 text-xs font-semibold text-ui-primary-text">AI 公司操作系统</span><h1 className="mt-5 text-4xl font-semibold tracking-[-0.035em] sm:text-5xl">从今天开始，和 AI 一起经营公司</h1><p className="mx-auto mt-5 max-w-[560px] text-base leading-7 text-ui-txt-2">Curis 帮你建立公司、组织 AI 员工、经营业务，并把真正需要你决定的事情带回来。</p><div className="mt-9 flex flex-col justify-center gap-3 sm:flex-row"><PrimaryButton onClick={onCreate} disabled={busy}>创建我的 AI 公司</PrimaryButton><button onClick={onSkip} disabled={busy} className="rounded-xl border border-ui-line bg-ui-surface px-5 py-3 text-sm font-semibold text-ui-txt-2 hover:bg-ui-surface-2 disabled:opacity-50">先看看 Curis</button></div>{error && <p role="alert" className="mt-4 text-sm text-ui-danger">{error}</p>}<p className="mt-8 text-xs text-ui-txt-3">本机优先 · 经营数据由你掌控</p></section></main>;
}

function EmptyCuris({ onCreate }) {
  return <TerraShell topCrumb="CEO 工作台" assistantContext={{ page: "ceo-office" }}><div className="grid min-h-full place-items-center"><section className="max-w-lg rounded-2xl border border-ui-line bg-ui-surface p-10 text-center shadow-ui-2"><div className="mx-auto grid h-11 w-11 place-items-center rounded-xl bg-ui-primary-soft text-ui-primary-text">✦</div><h1 className="mt-5 text-2xl font-semibold text-ui-txt">这里还没有公司</h1><p className="mt-3 text-sm leading-6 text-ui-txt-2">你可以继续浏览 Curis。准备好以后，只需填写你的称呼和公司名称。</p><PrimaryButton onClick={onCreate} className="mt-6">创建我的 AI 公司</PrimaryButton></section></div></TerraShell>;
}

function Setup({ value, setValue, onSubmit, onBack, busy, error, recovering }) {
  const [avatarError, setAvatarError] = useState(""), [reading, setReading] = useState(false);
  const generation = useRef(0), reader = useRef(null), live = useRef(true), locked = useRef(busy || recovering);
  useLayoutEffect(() => { locked.current = busy || recovering; if (locked.current) { generation.current++; reader.current?.abort(); setReading(false); } }, [busy, recovering]);
  useEffect(() => { live.current = true; return () => { live.current = false; generation.current++; reader.current?.abort(); }; }, []);
  const selectAvatar = avatar_ref => {
    if (locked.current) return;
    generation.current++; reader.current?.abort(); setReading(false); setAvatarError(""); setValue(current => ({ ...current, avatar_ref }));
  };
  const chooseFile = event => {
    const file = event.target.files?.[0]; event.target.value = "";
    if (!file || locked.current) return;
    const token = ++generation.current; reader.current?.abort(); setReading(false);
    if (!file.size || file.size > AVATAR_BYTES || !["image/png", "image/jpeg", "image/webp"].includes(file.type)) { setAvatarError("请选择194KB以内的 PNG、JPEG 或 WebP 图片；原头像已保留，也可移除后继续。"); return; }
    const next = new FileReader(); reader.current = next; setReading(true); setAvatarError("");
    const current = () => live.current && generation.current === token && !locked.current;
    next.onload = () => {
      if (!current()) return;
      setReading(false);
      try { const avatar_ref = String(next.result || "");
        if (!avatar_ref.startsWith(`data:${file.type};base64,`)) throw inputError("头像读取格式不一致，请重新选择。");
        validateSetupValues({ display_name: "头像校验", company_name: "头像校验", avatar_ref });
        setValue(value => ({ ...value, avatar_ref }));
      } catch (reason) { setAvatarError(reason.message); }
    };
    next.onerror = () => { if (current()) { setReading(false); setAvatarError("图片读取失败，原头像已保留，请重新选择。"); } };
    next.readAsDataURL(file);
  };
  return <main className="grid min-h-screen place-items-center bg-ui-bg px-5 py-10"><form onSubmit={event => { if (reading) { event.preventDefault(); setAvatarError("头像尚未读取完成，请稍后再提交。"); } else onSubmit(event); }} className="w-full max-w-[500px] rounded-2xl border border-ui-line bg-ui-surface p-7 shadow-ui-3"><span className="text-xs font-semibold text-ui-primary-text">建立你的公司</span><h1 className="mt-2 text-2xl font-semibold text-ui-txt">先告诉 Curis 怎么称呼你</h1><p className="mt-2 text-sm text-ui-txt-2">只需要最少信息。业务会在公司建立后单独开始。</p><fieldset disabled={busy || recovering}><label className="mt-6 block text-sm font-medium text-ui-txt">你的称呼<input autoFocus value={value.display_name} onChange={(event) => setValue({ ...value, display_name: event.target.value })} maxLength={80} placeholder="例如：一鸣" className="mt-2 h-11 w-full rounded-xl border border-ui-line bg-ui-surface px-3 outline-none focus:border-ui-primary" /></label><div className="mt-5"><span className="text-sm font-medium text-ui-txt">头像（可选）</span><div className="mt-2 flex flex-wrap items-center gap-2">{PRESETS.map(([key, text, bg, color]) => <button type="button" aria-label={`选择头像 ${key}`} key={key} onClick={() => selectAvatar(`preset:${key}`)} style={{ background: bg, color }} className={`grid h-11 w-11 place-items-center rounded-full text-xs font-bold ${value.avatar_ref === `preset:${key}` ? "ring-2 ring-ui-primary ring-offset-2" : ""}`}>{text}</button>)}<label className="cursor-pointer rounded-lg border border-ui-line px-3 py-2 text-xs text-ui-txt-2"><input type="file" accept="image/png,image/jpeg,image/webp" className="hidden" onChange={chooseFile} />上传</label>{value.avatar_ref && <button type="button" onClick={() => selectAvatar("")}>移除头像</button>}</div>{avatarError && <p role="alert" className="mt-2 text-sm text-ui-danger">{avatarError}</p>}<p className="mt-2 text-[11px] text-ui-txt-3">图片只保存在当前 Curis 本机数据中，最大194KB。</p></div><label className="mt-5 block text-sm font-medium text-ui-txt">公司名称<input value={value.company_name} onChange={(event) => setValue({ ...value, company_name: event.target.value })} maxLength={120} placeholder="例如：山海科技" className="mt-2 h-11 w-full rounded-xl border border-ui-line bg-ui-surface px-3 outline-none focus:border-ui-primary" /></label></fieldset>{recovering && <p role="status" className="mt-4 text-sm text-ui-txt-2">保留原设定，先查询同一建公司记录；不会重新建另一家公司。</p>}{error ? <p role="alert" className="mt-4 rounded-lg border border-[color-mix(in_srgb,var(--ui-danger)_28%,var(--ui-line))] bg-[color-mix(in_srgb,var(--ui-danger)_8%,var(--ui-surface-2))] px-3 py-2 text-sm text-ui-txt">{error}</p> : null}<PrimaryButton type="submit" className="mt-6 w-full" disabled={busy || reading || !value.display_name.trim() || !value.company_name.trim()}>{reading ? "正在读取头像…" : busy ? "正在核对并建立…" : recovering ? "查询并继续原记录" : "建立公司"}</PrimaryButton><button type="button" disabled={busy || recovering} onClick={onBack} className="mt-3 w-full text-sm text-ui-txt-2">返回</button></form></main>;
}

export default function AppEntry() {
  const runtime = useRuntime();
  const pending = useRef(false), operation = useRef(null);
  const [recovering, setRecovering] = useState(false);
  const [presentation, setPresentation] = useState(null);
  const [stage, setStage] = useState("loading");
  const [form, setForm] = useState({ display_name: "", avatar_ref: "", company_name: "" });
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  useEffect(() => {
    let active = true;
    try { const saved = JSON.parse(sessionStorage.getItem(SETUP_KEY) || "null");
      if (saved !== null && (!saved || typeof saved.companyId !== "string" || !saved.companyId || typeof saved.runId !== "string" || !saved.values || typeof saved.values.company_name !== "string" || !saved.values.company_name.trim() || typeof saved.values.display_name !== "string" || !saved.values.display_name.trim() || typeof saved.values.avatar_ref !== "string")) throw new Error("原建公司记录不完整。");
      if (saved) { operation.current = saved; setForm(saved.values); setRecovering(true); setStage("setup"); }
    } catch { setError("暂时无法读取原建公司记录，请保留本机数据并恢复存储后重试。"); setStage("recovery-error"); return; }
    getV1Presentation().then(value => { if (!active) return; setPresentation(value); if (!operation.current) { setForm(current => ({ ...current, display_name: value.display_name || "", avatar_ref: value.avatar_ref || "" })); setStage("empty"); } }).catch(() => { if (active && !operation.current) setStage("empty"); });
    return () => { active = false; };
  }, []);
  useEffect(() => { if (!operation.current && runtime.status === "ready" && runtime.snapshot?.company) window.location.replace("/ceo-office"); }, [runtime.snapshot, runtime.status]);
  const skip = async () => {
    if (pending.current) return; pending.current = true; setBusy(true); setError("");
    try { const next = { ...(presentation || {}), welcome_dismissed: true }; await saveV1Presentation(next); setPresentation(next); setStage("empty"); }
    catch (caught) { setError(caught?.message || "暂时无法保存，仍可重试或创建公司。"); }
    finally { pending.current = false; setBusy(false); }
  };
  const createCompany = async event => {
    event.preventDefault(); if (pending.current) return; pending.current = true; setBusy(true); setError("");
    try {
      const checkpoint = value => { sessionStorage.setItem(SETUP_KEY, JSON.stringify(value)); operation.current = value; setRecovering(true); };
      if (!operation.current) checkpoint({ companyId: `company-${crypto.randomUUID()}`, runId: "", values: validateSetupValues(form) });
      await completeCompanySetup(operation.current, checkpoint);
      await runtime.refresh(); sessionStorage.removeItem(SETUP_KEY); operation.current = null; window.location.replace("/ceo-office");
    } catch (caught) {
      if (caught?.setupInputRejected && !operation.current?.runId && !operation.current?.runRequested) {
        try { if (operation.current) sessionStorage.removeItem(SETUP_KEY); operation.current = null; setRecovering(false); setError(`${caught.message} 请修改输入后再提交。`); }
        catch { setError("本机保存的设定暂时无法更新，请保留记录并恢复存储后重试。"); }
      } else setError(`${caught?.message || "请求结果暂时无法确认。"} ${operation.current ? "原设定已保留；重试会先核对原记录。" : "尚未提交公司创建，请恢复本机存储后重试。"}`);
    }
    finally { pending.current = false; setBusy(false); }
  };
  if (runtime.status === "error" || runtime.status === "forbidden") return <main className="grid min-h-screen place-items-center bg-ui-bg px-6"><section className="max-w-md rounded-2xl border border-ui-line bg-ui-surface p-7"><h1 className="text-xl font-semibold text-ui-txt">暂时无法读取 Curis</h1><p className="mt-2 text-sm text-ui-txt-2">{runtime.error}</p><button onClick={runtime.refresh} className="mt-5 text-sm font-semibold text-ui-primary-text">重新读取</button></section></main>;
  if (stage === "recovery-error") return <main className="grid min-h-screen place-items-center bg-ui-bg px-6"><section role="alert"><h1>原建公司记录暂不可读取</h1><p>{error}</p><button onClick={() => window.location.reload()}>重新读取</button></section></main>;
  if (stage === "loading" || runtime.status === "loading") return <main className="grid min-h-screen place-items-center bg-ui-bg text-sm text-ui-txt-2">正在打开 Curis…</main>;
  if (stage === "setup") return <Setup value={form} setValue={value => { if (!pending.current && !operation.current) setForm(value); }} onSubmit={createCompany} busy={busy} error={error} recovering={recovering} onBack={() => setStage("empty")} />;
  if (stage === "empty") return <EmptyCuris onCreate={() => setStage("setup")} />;
  return <EmptyCuris onCreate={() => setStage("setup")} />;
}
