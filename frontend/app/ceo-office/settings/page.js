"use client";

import { Suspense, useEffect, useLayoutEffect, useRef, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import TerraShell, { TerraPaneContent } from "../../../components/terra/TerraShell.js";
import { TerraIcon } from "../../../components/terra/TerraIcons.js";
import { useRuntime } from "../../../components/runtime/RuntimeProvider.js";
import { TENANT_ID, CEO_ID } from "../../../lib/api.js";
import { getV1Presentation, saveV1Presentation, getAIProviders, getModelPreference, getCompanyTextPolicy, saveCompanyTextPolicy } from "../../../lib/v1FrontendApi.js";
import { validateBusinessReturn } from "../../../lib/businessReturnApi.js";
import { nativeRecovery } from "../../../lib/nativeBackup.js";
import { SETTINGS_CATEGORIES as TABS, PRESENTATION_CHANGED, THEME_CHANGED, applySettingsTheme, themeValue,
  settingsCategory, settingsReturn, settingsModelHref, settingsEntryIdentity, presentationSubmission,
  samePresentationDraft, savedPresentationDraft, settingsDraftKey, readSettingsDraft, readSettingsModels } from "../../../lib/settingsEntryState.mjs";
import styles from "./Settings.module.css";

const EMPTY = { display_name: "", avatar_ref: "" };
const AVATARS = [["iris", "CEO"], ["violet", "C"], ["amber", "Y"], ["mint", "AI"]];
function Group({ title, children }) { return <section className={styles.group}><h2>{title}</h2>{children}</section>; }
function Row({ label, description, children }) {
  return <div className={styles.row}><div><strong>{label}</strong>{description && <p>{description}</p>}</div>{children}</div>;
}
function Unsupported({ label, description }) { return <Row label={label} description={description}><span>暂不可设置</span></Row>; }
function companyRefs(identity) {
  if (!Array.isArray(identity) || !identity.length) return "原资料受损/缺失，当前公司待恢复";
  const refs = identity.slice(0, 8).map((row) => String(row?.company_id || "").slice(0, 128)).filter(Boolean);
  return refs.join("、") + (identity.length > 8 ? ` 等共 ${identity.length} 个公司` : "");
}

export function CompanyTextConsent({ companyId }) {
  const [view, setView] = useState(null), [error, setError] = useState("");
  const [workspaces, setWorkspaces] = useState([]), [models, setModels] = useState([]);
  const [budget, setBudget] = useState(""), [hours, setHours] = useState(24), [consent, setConsent] = useState(false);
  const [trial, setTrial] = useState(false), [continuous, setContinuous] = useState(false);
  const [busy, setBusy] = useState(false), [unknown, setUnknown] = useState(false), [notice, setNotice] = useState("");
  const [clock, setClock] = useState(Date.now());
  const expiresAt = Date.parse(view?.policy?.expires_at);
  const expired = Number.isFinite(expiresAt) && clock >= expiresAt;
  const pricePending = view?.price_status === "VERIFICATION_REQUIRED" || view?.policy?.execution_state === "AWAITING_PRICE_VERIFICATION";
  const priceNoticeBody = (view?.price_notice || "许可范围和预算已保存，但尚不能进行付费模型执行；请由维护者更新经核验的价格依据后，重新核对并确认公司许可。原输入会保留，不会自动调用或计费。").replace(/^价格待核实[：:]\s*/, "");
  const ceiling = view?.per_request_ceiling_cny;
  const ceilingKnown = typeof ceiling === "number" ? Number.isFinite(ceiling) : typeof ceiling === "string" && ceiling.trim() !== "";
  const ceilingText = ceilingKnown
    ? `含保守封装预留的单次准入上限 ¥${view.per_request_ceiling_cny}；超限会保留输入并要求缩小范围。`
    : "价格待核实，暂无经核验的单次准入上限；超限会保留输入并要求缩小范围。";
  useEffect(() => {
    if (!view?.policy?.enabled || !Number.isFinite(expiresAt) || expired) return;
    const timer = setTimeout(() => setClock(Date.now()), Math.max(0, expiresAt - Date.now()));
    return () => clearTimeout(timer);
  }, [view?.policy?.enabled, expiresAt, expired]);
  const generation = useRef(0), pending = useRef(null), sending = useRef(false);
  const read = async (hydrate = false) => {
    const current = generation.current;
    try {
      const next = await getCompanyTextPolicy(companyId);
      if (current !== generation.current || next.company_id !== companyId) return;
      setView(next); setClock(Date.now()); setError(""); setConsent(false);
      if (hydrate || next.policy?.trial_authorization_ref) setTrial(Boolean(next.policy?.trial_authorization_ref));
      if (hydrate || next.policy?.test_authorization_ref) setContinuous(Boolean(next.policy?.test_authorization_ref));
      if (next.continuity?.needs_reconfirmation) {
        if (next.continuity.token !== view?.continuity?.token) setBudget("");
        if (pending.current) { pending.current = null; setUnknown(false); setNotice("旧许可保存请求已失效；请核对历史费用提示后明确保存新的后续许可。"); }
      }
      if (hydrate) { setWorkspaces(next.policy?.workspace_ids || []); setModels(next.policy?.models?.map((m) => m.model_key) || []); setBudget(!next.continuity?.needs_reconfirmation && next.policy?.budget_micro_cny ? String(next.policy.budget_micro_cny / 1000000) : ""); }
      if (pending.current && !next.continuity?.needs_reconfirmation && next.policy?.request_id === pending.current.request_id) {
        pending.current = null; setUnknown(false); setConsent(false); setNotice(next.policy.enabled ? "文字许可已保存。每次执行仍会核对范围、价格与执行限制。" : "许可已撤销；原请求和占额记录保留。");
      }
    } catch { if (current === generation.current) setError("公司许可暂时无法读取，请重试；没有自动授权。"); }
  };
  useEffect(() => { generation.current += 1; setView(null); setConsent(false); setTrial(false); setContinuous(false); pending.current = null; setUnknown(false); read(true); return () => { generation.current += 1; }; }, [companyId]);
  const save = async (enabled, retry = false) => {
    if (sending.current || !view || (unknown && !retry)) return;
    const value = retry ? pending.current : { request_id: crypto.randomUUID(), expected_revision: view.policy?.revision || "", enabled,
      consent: enabled && consent, history_acknowledged: enabled && consent && Boolean(view.continuity?.needs_reconfirmation), workspace_ids: enabled ? workspaces : [], model_keys: enabled ? models : [],
      budget_cny: enabled ? budget : "", valid_hours: Number(hours), preview_token: view.preview_token,
      ...(enabled && continuous ? { authorization_mode: "synthetic_continuous" } : enabled && trial ? { authorization_mode: "synthetic_trial" } : {}) };
    if (!value) return;
    const current = generation.current; pending.current = value; sending.current = true; setBusy(true); setError("");
    try {
      const saved = await saveCompanyTextPolicy(companyId, value);
      if (current !== generation.current) return;
      if (saved?.policy?.request_id !== value.request_id) throw new Error("Unconfirmed consent request");
      pending.current = null; setUnknown(false); setConsent(false);
      setNotice("原许可操作已确认；下方显示最新公司许可。撤销不会取消已开始的远端执行。");
      await read();
    }
    catch (reason) { if (current === generation.current) { setUnknown(!reason?.status || reason.status >= 500); setError(reason?.status === 409 ? "范围、价格或许可已变化，请重新读取后确认；输入已保留。" : "许可保存未确认；请查询或重试同一保存请求。"); } }
    finally { if (current === generation.current) { sending.current = false; setBusy(false); } }
  };
  const toggle = (values, set, key) => set(values.includes(key) ? values.filter((v) => v !== key) : [...values, key]);
  return <Group title="专业文字执行：预算与数据外发">
    <p>明确同意后，所选工作空间的负责员工可将当前讨论中已发送的文字、员工回复和主动选择的引用发给下列模型。对话上下文只取最近六条、每条最多1500字符；未保存的正文不会自动发送；音频生成、文件上传与外部发布不在本许可内。</p>
    {!view && !error && <p role="status">正在读取公司许可…</p>}{error && <p role="alert">{error}</p>}{notice && <p role="status">{notice}</p>}
    {view && <>{pricePending && <p role="alert">价格待核实：{priceNoticeBody}</p>}
      {view.continuity?.history_incomplete && <p role="alert">资料状态曾发生变化，历史费用不可完整核实；下方不会把历史未知费用显示为零。{view.continuity.needs_reconfirmation ? "旧费用授权已失效；重新核对范围并填写新的后续额度后，才能明确保存新许可。" : "当前额度只适用于明确重新确认后的执行，不代表历史费用已结清。"}</p>}
      {view.continuity?.can_confirm === false && <p role="alert">本机许可状态文件无法核验，已停止执行。请保留现场处理；不会自动修复或重新授权。</p>}
      <p role="status">{view.policy?.enabled && !view.continuity?.needs_reconfirmation
        ? expired ? `文字许可已过期（${view.policy.expires_at}）。请核对范围、费用和有效期后重新同意并保存。`
          : `已保存许可，有效至 ${view.policy.expires_at}；执行时再次核验`
        : "当前未授权文字执行"}</p>
      {view.continuity?.needs_reconfirmation ? <p>历史估算及占额：无法完整核实。没有恢复全额预算，也没有取消已发出的外部执行。</p> : <p>{view.continuity?.history_incomplete ? "重新确认后累计估算" : "本功能累计估算"}：¥{(view.totals.estimated_micro_cny / 1000000).toFixed(6)}；保留占额：¥{(view.totals.reserved_micro_cny / 1000000).toFixed(6)}。实付未知；未知结果不退回额度。</p>}
      <fieldset disabled={busy || unknown}><legend>允许的工作空间</legend>{view.workspaces.map((w) => <label className="block" key={w.workspace_id}><input type="checkbox" checked={workspaces.includes(w.workspace_id)} onChange={() => toggle(workspaces, setWorkspaces, w.workspace_id)} /> {w.name}</label>)}{!view.workspaces.length && <p>当前没有可授权的专业工作空间。</p>}</fieldset>
      <fieldset disabled={busy || unknown}><legend>文字发送目的地与模型</legend>{view.models.map((m) => <label className="block" key={m.model_key}><input type="checkbox" checked={models.includes(m.model_key)} onChange={() => toggle(models, setModels, m.model_key)} /> {m.display_name} · {m.destination}</label>)}{!view.models.length && <p>当前没有同时具备合法模型资格、明确目的地及有效价格依据的模型。</p>}</fieldset>
      <p>价格核对：{view.price.checked_at}；有效至 {view.price.valid_until}。峰值每百万输入 ¥{view.price.input_cny_per_million} / 输出 ¥{view.price.output_cny_per_million}，为估算依据。</p>
      <a href={view.price.source_cny} target="_blank" rel="noreferrer">查看官方人民币价格</a>
      <p>每次完整文字输入最多 {view.max_input_bytes} 字节，输出最多 {view.max_output_tokens} tokens，{ceilingText}</p>
      <Row label={continuous ? "本轮费用参考（人民币，不自动停止）" : view.continuity?.needs_reconfirmation ? "新的后续预算（人民币）" : "本功能累计预算（人民币）"} description={continuous ? "参考金额不作为停止阈值；历史用量、估算与占额保留。" : view.continuity?.needs_reconfirmation ? "这是新的后续费用许可，不是历史额度恢复；历史费用仍不可完整核实。" : "本许可期已有估算和未知结果占额都计入此上限；正常重新保存不会归零。"}><input aria-label="专业文字累计预算（人民币）" type="number" min="0.000001" max={trial && !continuous ? "0.1" : "100000"} step="0.000001" value={budget} disabled={busy || unknown} onChange={(event) => setBudget(event.target.value)} /></Row>
      <Row label="许可有效期"><select aria-label="文字许可有效期" value={hours} disabled={busy || unknown} onChange={(event) => setHours(Number(event.target.value))}>{[[1,"1小时"],[24,"24小时"],[72,"3天"]].map(([value,label]) => <option key={value} value={value}>{label}</option>)}</select></Row>
      <label className="block"><input aria-label="本轮合成验收受限授权" type="checkbox" checked={trial} disabled={busy || unknown || continuous || Boolean(view.policy?.trial_authorization_ref)} onChange={(event) => { setTrial(event.target.checked); setConsent(false); }} />本轮合成验收受限授权（仅验收候选）</label>
      {trial && !continuous && <p role="status">仅用于独立合成公司和单一工作空间、模型：最多两次，累计不超过 ¥0.10；实际费用未知时停止后续调用。次数不会因结算、撤销或重新保存恢复。{view.policy?.trial_authorization_ref && "已保存本轮限制；可撤销后续执行，不能改为普通授权解除限制。"}</p>}
      <label className="block"><input aria-label="本轮持续合成验收授权" type="checkbox" checked={continuous} disabled={busy || unknown || Boolean(view.policy?.test_authorization_ref)} onChange={(event) => { setContinuous(event.target.checked); setConsent(false); }} />明确采用本轮持续合成验收授权</label>
      {continuous && <p role="status">仅限本公司明确勾选的合规工作空间和原批准模型。取消两次及 ¥0.10 限制，¥10 仅作参考；正常小额费用、缺少逐笔实付账单或达到参考金额不会自动停止。保留历史用量和估算；异常重复、未核实执行、失控并发或异常费用时停止受影响调用链。不得充值、购买新服务或切换未批准付费模型。</p>}
      <label className="block"><input type="checkbox" checked={consent} disabled={busy || unknown} onChange={(event) => setConsent(event.target.checked)} />我同意以上工作范围、文字外发目的地、{continuous ? "本轮持续验收费用规则" : "费用上限"}与有效期。{view.continuity?.needs_reconfirmation && "我理解历史费用不可完整核实，此次明确授权新的后续额度。"}</label>
      <div className={styles.actions}><button type="button" disabled={busy || unknown || view.continuity?.can_confirm === false || !consent || !workspaces.length || !models.length || !budget || ((trial || continuous) && ((!continuous && workspaces.length !== 1) || models.length !== 1 || !Number.isFinite(Number(budget)) || Number(budget) <= 0 || (!continuous && Number(budget) > 0.1)))} onClick={() => save(true)}>保存文字许可</button><button type="button" disabled={busy || unknown || !view.policy?.enabled} onClick={() => save(false)}>撤销后续文字执行</button>{unknown && <button type="button" disabled={busy} onClick={() => save(false, true)}>重试原保存请求</button>}</div>
    </>}
    <button type="button" disabled={busy} onClick={() => read()}>重新读取文字许可</button>
  </Group>;
}

function SettingsInner() {
  const router = useRouter(), searchParams = useSearchParams(), runtime = useRuntime();
  const query = searchParams.toString(), category = settingsCategory(searchParams.get("tab"));
  let entryIdentity;
  try { entryIdentity = settingsEntryIdentity(new URLSearchParams(query)); } catch { entryIdentity = "invalid-entry"; }
  const scopeKey = settingsDraftKey(TENANT_ID, CEO_ID, runtime.companyId, entryIdentity);
  const identityReady = runtime.status === "ready" || runtime.status === "empty";
  const [profile, setProfile] = useState({ key: "", status: "loading", saved: null });
  const [draft, setDraft] = useState(EMPTY), [profileError, setProfileError] = useState("");
  const [saveStatus, setSaveStatus] = useState("idle"), [reload, setReload] = useState(0);
  const [theme, setTheme] = useState("system"), [returnState, setReturnState] = useState(null);
  const [returnError, setReturnError] = useState(""), [returnBusy, setReturnBusy] = useState(false);
  const [modelState, setModelState] = useState({ status: "idle" });
  const [recovery, setRecovery] = useState({ status: "idle" });
  const [recoveryBusy, setRecoveryBusy] = useState(false), [restoreConfirmed, setRestoreConfirmed] = useState(false);
  const alive = useRef(true), profileGeneration = useRef(0), saveGeneration = useRef(0), saving = useRef(false);
  const draftRef = useRef(draft), scopeRef = useRef(scopeKey), modelGeneration = useRef(0);
  const modelHeading = useRef(null), modelReadButton = useRef(null), categories = useRef([]);
  const returnKey = query + "|" + runtime.companyId + "|" + runtime.status;
  const returnKeyRef = useRef(returnKey);
  useLayoutEffect(() => {
    draftRef.current = draft; scopeRef.current = scopeKey; returnKeyRef.current = returnKey;
  }, [draft, scopeKey, returnKey]);

  useEffect(() => {
    alive.current = true;
    return () => { alive.current = false; saveGeneration.current += 1; modelGeneration.current += 1; };
  }, []);
  useEffect(() => {
    if (!identityReady) return;
    const generation = ++profileGeneration.current;
    saveGeneration.current += 1; saving.current = false;
    setProfile({ key: scopeKey, status: "loading", saved: null }); setDraft(EMPTY);
    setProfileError(""); setSaveStatus("idle");
    getV1Presentation().then((value) => {
      if (!alive.current || generation !== profileGeneration.current || scopeRef.current !== scopeKey) return;
      const saved = presentationSubmission(value, value);
      let pending = null;
      try { pending = readSettingsDraft(window.sessionStorage, scopeKey); } catch { /* Optional temporary storage. */ }
      setProfile({ key: scopeKey, status: "ready", saved }); setDraft(pending || saved);
    }).catch(() => {
      if (alive.current && generation === profileGeneration.current && scopeRef.current === scopeKey) {
        setProfile({ key: scopeKey, status: "error", saved: null }); setProfileError("个人资料暂时无法读取，请重试。");
      }
    });
    return () => { profileGeneration.current += 1; };
  }, [scopeKey, reload, identityReady]);
  useEffect(() => {
    if (profile.key !== scopeKey || profile.status !== "ready") return;
    try {
      if (samePresentationDraft(draft, profile.saved)) window.sessionStorage.removeItem(scopeKey);
      else window.sessionStorage.setItem(scopeKey, JSON.stringify({ display_name: draft.display_name, avatar_ref: draft.avatar_ref }));
    } catch { /* The mounted draft remains available. */ }
  }, [draft, profile, scopeKey]);
  useEffect(() => {
    const update = () => { try { setTheme(themeValue(window.localStorage.getItem("curis.theme"))); } catch { setTheme(themeValue(document.documentElement.dataset.theme)); } };
    update(); window.addEventListener(THEME_CHANGED, update); return () => window.removeEventListener(THEME_CHANGED, update);
  }, []);
  useEffect(() => {
    let current = true;
    setReturnState(null); setReturnError(""); setReturnBusy(false);
    let target;
    try { target = settingsReturn(new URLSearchParams(query)); }
    catch { setReturnError("无法确认原页面，请从业务入口重新进入。"); return; }
    if (!target) return;
    if (!target.business) { setReturnState({ key: returnKey, ...target }); return; }
    if (runtime.status !== "ready") return;
    validateBusinessReturn(target.business.kind, target.business.value).then((verified) => {
      if (current) setReturnState({ key: returnKey, href: verified.href, label: verified.label, business: target.business });
    }).catch(() => { if (current) setReturnError("原工作暂时无法确认，请从业务入口重新进入。"); });
    return () => { current = false; };
  }, [query, returnKey, runtime.status]);
  useEffect(() => {
    modelGeneration.current += 1; setModelState({ status: "idle" });
    if (category === "models" && new URLSearchParams(query).get("settings_entry") === "models") modelHeading.current?.focus();
  }, [category, runtime.companyId, query]);
  useEffect(() => {
    setRecovery((current) => ["RESTORED", "RECOVERY_HOLD"].includes(current.status)
      && Array.isArray(current.identity)
      && (!runtime.companyId || current.identity.some((row) => row.company_id === runtime.companyId))
      ? current : { status: "idle" });
    setRestoreConfirmed(false);
  }, [runtime.companyId]);

  const changeCategory = (key, focusIndex) => {
    const next = new URLSearchParams(query); next.set("tab", key); next.delete("settings_entry");
    router.replace("/ceo-office/settings?" + next, { scroll: false });
    if (focusIndex !== undefined) categories.current[focusIndex]?.focus();
  };
  const categoryKey = (event, index) => {
    const next = event.key === "ArrowDown" ? (index + 1) % TABS.length : event.key === "ArrowUp" ? (index + TABS.length - 1) % TABS.length
      : event.key === "Home" ? 0 : event.key === "End" ? TABS.length - 1 : null;
    if (next !== null) { event.preventDefault(); changeCategory(TABS[next][0], next); }
  };
  const save = async (event) => {
    event.preventDefault();
    if (!identityReady || profile.key !== scopeKey || profile.status !== "ready" || saving.current) return;
    const submittedDraft = { display_name: draftRef.current.display_name, avatar_ref: draftRef.current.avatar_ref };
    let submitted;
    try { submitted = presentationSubmission(profile.saved, submittedDraft); } catch (error) { setProfileError(error.message); return; }
    const generation = ++saveGeneration.current, key = scopeKey;
    saving.current = true; setSaveStatus("saving"); setProfileError("");
    try {
      const response = await saveV1Presentation(submitted);
      if (!alive.current || scopeRef.current !== key || saveGeneration.current !== generation) return;
      const saved = presentationSubmission(response, response);
      setProfile({ key, status: "ready", saved });
      setDraft((current) => savedPresentationDraft(current, submittedDraft, saved));
      setSaveStatus("saved"); window.dispatchEvent(new Event(PRESENTATION_CHANGED));
    } catch {
      if (alive.current && scopeRef.current === key && saveGeneration.current === generation) {
        setSaveStatus("error"); setProfileError("更改尚未保存，请重试。你的输入仍会保留。");
      }
    } finally { if (saveGeneration.current === generation) saving.current = false; }
  };
  const back = async () => {
    if (!returnState || returnState.key !== returnKey || returnBusy) return;
    const key = returnKey; setReturnBusy(true); setReturnError("");
    try {
      const target = returnState.business ? await validateBusinessReturn(returnState.business.kind, returnState.business.value) : returnState;
      if (alive.current && returnKeyRef.current === key) router.push(target.href);
    } catch { if (alive.current && returnKeyRef.current === key) setReturnError("原工作已变化，暂时无法返回。请从业务入口重新进入。"); }
    finally { if (alive.current && returnKeyRef.current === key) setReturnBusy(false); }
  };
  const readModels = async () => {
    const generation = ++modelGeneration.current, key = scopeKey;
    setModelState({ status: "loading" }); modelHeading.current?.focus();
    const value = await readSettingsModels({ readProviders: getAIProviders, readPreference: getModelPreference,
      isCurrent: () => alive.current && modelGeneration.current === generation && scopeRef.current === key });
    if (value) setModelState(value);
  };
  const cancelModels = () => { modelGeneration.current += 1; setModelState({ status: "idle" }); modelReadButton.current?.focus(); };
  const runRecovery = async (command) => {
    const safePreflight = command === "preflight_curis_restore" && recovery.status === "RECOVERY_REQUIRED" && recovery.nextAction === "CHOOSE_VERIFIED_BACKUP";
    const safeConfirmation = ["commit_curis_restore", "cancel_curis_restore"].includes(command) && recovery.status === "PREFLIGHT_OK";
    if (recoveryBusy || (command !== "read_curis_recovery_status" && runtime.status !== "ready" && !safePreflight && !safeConfirmation)) return;
    setRecoveryBusy(true);
    if (command !== "commit_curis_restore") setRestoreConfirmed(false);
    const current = recovery;
    try {
      const value = await nativeRecovery(command, command === "commit_curis_restore" ? { confirmationId: current.confirmationId } : {});
      setRecovery(value.status === "CANCELLED" ? { status: "idle" } : value);
      if (value.status === "RESTORED") {
        profileGeneration.current += 1;
        await runtime.refresh();
        setReload((previous) => previous + 1);
        window.dispatchEvent(new Event(PRESENTATION_CHANGED));
      }
    } finally { setRecoveryBusy(false); }
  };
  const ready = identityReady && profile.key === scopeKey && profile.status === "ready";
  const dirty = ready && !samePresentationDraft(draft, profile.saved);
  let modelHref = "/ceo-office/capabilities";
  try { modelHref = settingsModelHref(new URLSearchParams(query)); } catch { /* Safe entry without an invalid return. */ }

  const settingsContext = <nav className={styles.categories} aria-label="设置分类">{TABS.map(([key, label, icon], index) => <button key={key} ref={(element) => { categories.current[index] = element; }} type="button"
    aria-current={category === key ? "page" : undefined} aria-controls="settings-main" onClick={() => changeCategory(key)} onKeyDown={(event) => categoryKey(event, index)}><TerraIcon name={icon} className="h-4 w-4" />{label}</button>)}</nav>;
  const settingsHelp = <aside className={styles.note}><h2>关于此设置</h2><p>个人偏好只影响你的使用体验；公司默认值用于团队协作。</p><p>AI 连接由公司统一管理，供不同业务和员工使用。</p><button type="button" className={styles.button} onClick={() => changeCategory("models", 2)}>查看模型管理入口</button><p>暂不可设置的项目会保留说明；未保存的更改不会生效。</p></aside>;

  return <TerraShell topCrumb="设置" assistantContext={{ page: "settings" }}>
    <TerraPaneContent contextPane={settingsContext} contextLabel="设置分类" initialContextOpen
      utilityTabs={[{ id: "settings-help", title: "设置帮助", content: settingsHelp }]} utilityLabel="设置帮助" initialUtilityOpen />
    <main className={styles.settings}>
      <div className={styles.main} id="settings-main">
        <h1>{TABS.find(([key]) => key === category)[1]}</h1><p className={styles.intro}>管理个人偏好、公司默认值和 AI 连接。</p>
        {returnState?.key === returnKey && <div className={styles.return}><button type="button" className={styles.button} onClick={back} disabled={returnBusy}>{returnBusy ? "正在确认原工作…" : returnState.label || "返回原工作"}</button></div>}
        {returnError && <p role="status" className={styles.status}>{returnError} <Link href="/ceo-office/business">查看业务空间</Link></p>}
        {category === "personal" && <>
          <Group title="个人资料"><form onSubmit={save}>
            {!ready && <p role="status" className={styles.status}>{!identityReady ? ["error", "forbidden"].includes(runtime.status) ? "当前公司身份暂时无法确认，请重新读取。" : "正在确认当前公司…" : profile.key === scopeKey && profile.status === "error" ? profileError : "正在读取个人资料…"}</p>}
            <Row label="显示名称" description="用于展示你的个人身份。"><input aria-label="显示名称" className={styles.field} maxLength={80} value={ready ? draft.display_name : ""} disabled={!ready} onChange={(event) => { setDraft((value) => ({ ...value, display_name: event.target.value })); setSaveStatus((value) => value === "saving" ? value : "idle"); }} /></Row>
            <Row label="头像" description="保留已有头像，或选择预置头像。"><div className={styles.avatars}>{AVATARS.map(([key, label]) => <button key={key} className={styles.button} type="button" disabled={!ready} aria-label={"选择头像 " + key} aria-pressed={ready && draft.avatar_ref === "preset:" + key} onClick={() => { setDraft((value) => ({ ...value, avatar_ref: "preset:" + key })); setSaveStatus((value) => value === "saving" ? value : "idle"); }}>{label}</button>)}</div></Row>
            {ready && profileError && <p role="alert" className={styles.status}>{profileError}</p>}
            <div className={styles.actions}>{!identityReady && ["error", "forbidden"].includes(runtime.status) && <button type="button" className={styles.button} onClick={runtime.refresh}>重新读取</button>}{profile.status === "error" && <button type="button" className={styles.button} onClick={() => setReload((value) => value + 1)}>重新读取</button>}
              <button type="submit" className={styles.button} disabled={!dirty || saveStatus === "saving"}>{saveStatus === "saving" ? "正在保存…" : "保存个人资料"}</button>
              <span role="status" className={styles.status}>{dirty ? "更改尚未保存" : saveStatus === "saved" ? "个人资料已保存" : ""}</span></div>
          </form></Group>
          <Group title="外观"><Row label="主题模式" description="调整界面的显示风格。"><select aria-label="主题模式" className={styles.select} value={theme} onChange={(event) => setTheme(applySettingsTheme(event.target.value))}><option value="system">跟随系统</option><option value="light">浅色</option><option value="dark">深色</option></select></Row></Group>
          <Group title="语言与地区"><Unsupported label="界面语言" description="选择你习惯的显示语言。" /><Unsupported label="显示时区" description="用于显示日期与时间。" /></Group>
          <Group title="通知">{["应用内通知", "邮件通知", "会议提醒"].map((label) => <Unsupported key={label} label={label} description="通知偏好暂不可设置。" />)}</Group>
        </>}
        {category === "company" && <><Group title="公司资料">
          {runtime.status === "ready" && runtime.snapshot?.company ? <Row label="公司名称"><span>{runtime.snapshot.company.name || "名称未提供"}</span></Row>
            : <p role="status" className={styles.status}>{runtime.status === "empty" ? "尚未创建公司。创建后可以在这里查看公司资料。" : runtime.status === "forbidden" ? "无权读取当前公司，或公司已不存在。" : runtime.status === "error" ? "公司资料暂时无法读取，请重试。" : runtime.status === "ready" ? "公司资料尚未提供。" : "正在读取公司资料…"}</p>}
          {["error", "forbidden"].includes(runtime.status) && <button className={styles.button} type="button" onClick={runtime.refresh}>重新读取</button>}
        </Group><Group title="公司默认值">{["经营时区", "用途默认", "备份"].map((label) => <Unsupported key={label} label={label} description="公司默认值暂不可设置。" />)}</Group>{runtime.status === "ready" && runtime.companyId && <CompanyTextConsent key={runtime.companyId} companyId={runtime.companyId} />}</>}
        {category === "models" && <section onKeyDown={(event) => { if (event.key === "Escape" && modelState.status === "loading") { event.preventDefault(); cancelModels(); } }}>
          <Group title="模型与 AI 提供方"><h2 ref={modelHeading} tabIndex={-1}>模型管理</h2><p>公司统一管理 AI 连接，供不同业务和员工使用。</p>
            <p role="status" className={styles.status}>{modelState.status === "idle" ? "连接状态尚未读取" : modelState.status === "loading" ? "正在读取模型信息…" : modelState.status === "error" ? "无法读取模型信息。请重试，你的输入仍会保留。" : modelState.configured ? "已配置 " + modelState.configured + " 个提供方，连接状态仍需验证。" : "尚未配置模型提供方。"}</p>
            {modelState.status === "ready" && modelState.defaultName && <Row label="已保存的默认选择" description="实际可用性以模型管理验证为准。"><span>{modelState.defaultName}</span></Row>}
            <div className={styles.actions}><button ref={modelReadButton} type="button" className={styles.button} onClick={readModels} disabled={modelState.status === "loading"}>{modelState.status === "error" ? "重试读取" : "读取模型信息"}</button>
              {modelState.status === "loading" && <button type="button" className={styles.button} onClick={cancelModels}>取消等待</button>}<Link className={styles.link} href={modelHref}>查看模型管理</Link></div>
          </Group><Group title="当前能力与作用范围"><p>可登记外部 Agent、绑定员工并确认执行许可；保存配置不代表连接或实际执行已验证。</p><Link className={styles.link} href="/ceo-office/capabilities#employee-agents">配置外部 Agent 与员工执行</Link></Group>
        </section>}
        {category === "security" && <Group title="权限与安全"><Unsupported label="电脑访问与授权" description="相关授权须以实际可用能力为准。" /><Unsupported label="安全偏好" description="安全偏好暂不可设置。" /></Group>}
        {category === "data" && <Group title="应用与数据"><div className={styles.backup}>
          <h2>备份与恢复</h2>
          <p>完整备份包含当前公司的数据库和 Curis 管理的头像、已安装工作空间包及本机导出文件。凭据、Cookie、钥匙串、浏览器资料、外部知识目录和服务不包含在内；恢复后需要重新连接与核验。</p>
          <p>备份保存在你选择的本机位置，包含敏感经营内容，目前不提供加密。旧版仅数据库备份不能用于这里的完整恢复。</p>
          <div className={styles.backupActions}>
            <button type="button" className={styles.button} disabled={recoveryBusy || runtime.status !== "ready"} onClick={() => runRecovery("create_curis_backup")}>创建完整备份</button>
            <button type="button" className={styles.button} disabled={recoveryBusy || (runtime.status !== "ready" && !(recovery.status === "RECOVERY_REQUIRED" && recovery.nextAction === "CHOOSE_VERIFIED_BACKUP"))} onClick={() => runRecovery("preflight_curis_restore")}>选择备份并预检</button>
            <button type="button" className={styles.button} disabled={recoveryBusy} onClick={() => runRecovery("read_curis_recovery_status")}>查看恢复状态</button>
          </div>
          {recoveryBusy && <p role="status">正在核验本机数据，请勿重复操作。</p>}
          {recovery.status === "PREFLIGHT_OK" && <section className={styles.restoreReview} aria-label="恢复影响确认">
            <h3>恢复预检通过</h3><p>备份摘要：<code>{recovery.archiveSha256}</code></p>
            <p>备份来源公司：<code>{companyRefs(recovery.identity)}</code>；创建时间（UTC）：{recovery.createdAt}；应用版本：{recovery.appVersion}；数据库结构版本：{recovery.schemaVersion}；备份协议：{recovery.backupProtocol}。</p>
            <p>当前目标公司：<code>{companyRefs(recovery.targetIdentity)}</code>；当前状态：{recovery.currentMode}。{["sameRoot", "company", "appVersion", "schema"].every((key) => recovery.compatibility?.[key] === "MATCHED") ? "同一数据目录、公司身份、应用版本和数据库结构兼容性均已核对。" : "兼容性回证不完整，请勿确认恢复。"}</p>
            <p>{recovery.impact}。备份包含 {recovery.files} 个文件；已核对可用空间。确认仅在 5 分钟内有效，备份或当前数据变化后须重新预检。</p>
            <p>恢复前会保全当前数据；恢复后凭据、权限、能力、外部文件及外部效果仍须逐项重连或核验，不会自动重放外部动作。</p>
            <label className={styles.restoreConfirm}><input type="checkbox" checked={restoreConfirmed} onChange={(event) => setRestoreConfirmed(event.target.checked)} />我理解这会替换当前本机数据，并已核对备份摘要</label>
            <div className={styles.backupActions}>
              <button type="button" className={styles.button} disabled={!restoreConfirmed || recoveryBusy || !["sameRoot", "company", "appVersion", "schema"].every((key) => recovery.compatibility?.[key] === "MATCHED")} onClick={() => runRecovery("commit_curis_restore")}>确认恢复</button>
              <button type="button" className={styles.button} disabled={recoveryBusy} onClick={() => runRecovery("cancel_curis_restore")}>取消</button>
            </div>
          </section>}
          {recovery.status === "BACKUP_VERIFIED" && <p role="status">完整备份已核验。保存在：<code>{recovery.localDestination}</code>；文件数：{recovery.files}；SHA-256：<code>{recovery.archiveSha256}</code></p>}
          {recovery.status === "RESTORED" && <p role="status">同一公司数据已恢复并读回。请重新连接凭据、权限、能力和外部文件，先核验未确定的外部效果，再决定是否继续原工作。</p>}
          {recovery.status === "RECOVERY_HOLD" && <p role="alert">数据已恢复并读回，但存在待核验的工作或外部效果。业务服务保持停止；请联系维护人员逐项核验后，再安排恢复运行。</p>}
          {recovery.status === "RECOVERY_REQUIRED" && <p role="alert">当前本机资料受损或缺失，业务服务保持停止。{recovery.nextAction === "CHOOSE_VERIFIED_BACKUP" ? "请选择同一数据目录原有的完整备份并预检；原始现场会在恢复前保全。" : "本机原有身份依据尚不能核验，请联系维护人员核对恢复记录。"}</p>}
          {recovery.status === "ROLLED_BACK" && <p role="status">中断恢复已回退并核验旧数据；请检查原工作后再操作。</p>}
          {recovery.status === "UNKNOWN" && <p role="alert">恢复状态未能证明；原数据与安全点已保留。请暂停新的写入并联系维护人员核对。</p>}
          {recovery.status === "FAILED" && <p role="alert">{recovery.message} 支持码：{recovery.code}</p>}
          {recovery.status === "UNSUPPORTED" && <p role="status">当前环境不支持本机完整备份与恢复，请在 Curis Desktop 中打开。</p>}
        </div><Unsupported label="缓存与维护" description="数据维护暂不可执行。" /></Group>}
        {category === "help" && <Group title="账户与帮助"><Unsupported label="账户信息" description="账户状态尚未读取。" /><Unsupported label="帮助与反馈" description="帮助与反馈入口暂不可使用。" /><Link className={styles.link} href="/ceo-office/analytics">查看用量</Link></Group>}
      </div>
    </main>
  </TerraShell>;
}

export default function SettingsPage() {
  return <Suspense fallback={<p role="status" className="p-6 text-ui-txt-2">正在打开设置…</p>}><SettingsInner /></Suspense>;
}
