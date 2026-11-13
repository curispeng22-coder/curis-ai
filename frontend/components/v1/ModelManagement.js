"use client";

import { Suspense, useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import { TENANT_ID, workspaceFetch } from "../../lib/api.js";
import { useSearchParams } from "next/navigation";
import TerraShell from "../terra/TerraShell.js";
import { useRuntime } from "../runtime/RuntimeProvider.js";
import { businessReturnInput, validateBusinessReturn } from "../../lib/businessReturnApi.js";
import { settingsModelHref } from "../../lib/settingsEntryState.mjs";
import {
  connectAIProvider,
  createSessionCredential,
  getAIProviders,
  getEnabledModels,
  getModelPreference,
  setModelPreference,
  updateCredential,
} from "../../lib/v1FrontendApi.js";

const COPY = {
  openai: ["OpenAI", "通用对话、推理与多模态模型"], anthropic: ["Anthropic", "Claude 系列对话与推理模型"],
  gemini: ["Google Gemini", "Google 多模态与长上下文模型"], deepseek: ["DeepSeek", "DeepSeek 对话与推理模型"],
  alibaba_qwen: ["通义千问", "阿里云百炼模型服务"], moonshot_kimi: ["Kimi", "Moonshot 长文本模型"],
  zhipu: ["智谱 GLM", "智谱对话与推理模型"], minimax: ["MiniMax", "MiniMax 通用模型服务"],
  volcengine_doubao: ["火山 / 豆包", "火山方舟模型服务"], ollama: ["Ollama", "本机运行的开放模型"],
  openai_compatible: ["OpenAI 兼容接口", "连接兼容 OpenAI 协议的服务"],
};

function statusLabel(provider, verified) {
  if (verified === true) return "本次连接验证通过";
  if (verified === false) return "本次连接验证未通过";
  return provider.configured ? "已保存配置 · 本次未验证" : "尚未配置";
}

const UNKNOWN_SAVE = "凭据保存结果尚未确认，已停止后续连接。请先确认原保存结果。";
const LOCAL_GUARD_UNAVAILABLE = "本地会话保护不可用，本次未发送凭据请求；已停止连接。";
const WRITE_NOT_STARTED = "服务端确认本次凭据写入未开始；已停止后续连接。";
const NATIVE_WRITE_UNCONFIRMED = "本机凭据写入阶段返回错误，保存结果无法确认；已停止连接。";
const METADATA_UNCONFIRMED = "本机保存调用已返回成功，但凭据资料登记失败；可能存在未关联凭据，已停止连接。";
const METADATA_ONLY_UNCONFIRMED = "凭据资料更新失败，本次未提交新的凭据写入；已停止连接。";
const AUDIT_FAILED = "凭据资料已登记，但完成记录失败；已停止连接，请先确认保存结果。";
const LOCAL_RECEIPT_FAILED = "服务端已返回有效保存结果，但本地保护回执失败；已停止连接，请先确认原保存结果。";
const markerKey = (scope) => `curis.modelCredentialAttempt:${JSON.stringify([TENANT_ID, scope.provider])}`;
function probeSessionGuard(scope) {
  let key;
  try {
    key = `${markerKey(scope)}:probe:${crypto.randomUUID()}`;
    sessionStorage.setItem(key, "ready");
    const ready = sessionStorage.getItem(key) === "ready";
    sessionStorage.removeItem(key);
    return ready;
  } catch {
    if (key) { try { sessionStorage.removeItem(key); } catch {} }
    return false;
  }
}
function readAttempt(scope) {
  try {
    const raw = sessionStorage.getItem(markerKey(scope));
    if (raw === null) return null;
    const value = JSON.parse(raw);
    if (!value || value.tenant !== TENANT_ID || value.provider !== scope.provider || typeof value.company !== "string" || typeof value.endpoint_hash !== "string" || !["PENDING", "KNOWN", "UNKNOWN", "BLOCKED"].includes(value.state) || typeof value.ref !== "string" || typeof value.storage !== "string" || Object.keys(value).some((key) => !["tenant", "company", "provider", "endpoint_hash", "state", "ref", "storage"].includes(key))) return { state: "UNKNOWN" };
    if (!/^[0-9a-f]{64}$/.test(value.endpoint_hash) || !["", "macos_keychain", "process_memory"].includes(value.storage) || (value.ref && !validCredential({ tenant_id: TENANT_ID, provider: scope.provider, status: "active", credential_id: value.ref.split("/").pop(), credential_ref: value.ref, storage: value.ref.startsWith("vault://") ? "macos_keychain" : "process_memory" }, scope.provider))) return { state: "UNKNOWN" };
    return value;
  } catch { return { state: "UNKNOWN" }; }
}
function writeAttempt(scope, state, ref = "", storage = "") {
  const value = { tenant: TENANT_ID, company: scope.company, provider: scope.provider, endpoint_hash: scope.endpoint_hash, state, ref, storage };
  try { sessionStorage.setItem(markerKey(scope), JSON.stringify(value)); } catch { return { state: "UNKNOWN" }; }
  return value;
}
function validCredential(value, provider, ref = "") {
  if (!value || value.tenant_id !== TENANT_ID || value.provider !== provider || value.status !== "active" || typeof value.credential_id !== "string" || !/^cred-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/.test(value.credential_id)) return false;
  const scheme = value.storage === "macos_keychain" ? "vault" : value.storage === "process_memory" ? "local-dev" : "";
  return Boolean(scheme && value.credential_ref === `${scheme}://tenant/${TENANT_ID}/credential/${value.credential_id}` && (!ref || value.credential_ref === ref));
}

export default function ModelManagement({ children }) {
  return <Suspense fallback={<p role="status" className="p-6 text-sm">正在确认模型入口…</p>}><ModelManagementContent>{children}</ModelManagementContent></Suspense>;
}

function ModelManagementContent({ children }) {
  const runtime = useRuntime();
  const returnQuery = useSearchParams().toString();
  let settingsBack = null;
  const settingsParams = new URLSearchParams(returnQuery);
  if (settingsParams.get("settings_entry") === "models") {
    try { settingsBack = settingsModelHref(settingsParams, { returning: true }); } catch { /* Invalid return cannot become a redirect. */ }
  }
  const [returnQueryVerified, setReturnQueryVerified] = useState("");
  const [writingReturn, setWritingReturn] = useState(null);
  const [cgReturn, setCgReturn] = useState(null);
  const [cgReturnNotice, setCgReturnNotice] = useState("");
  const [musicReturn, setMusicReturn] = useState(null);
  const [musicReturnNotice, setMusicReturnNotice] = useState("");
  const [returnNotice, setReturnNotice] = useState("");
  useEffect(() => {
    let current = true;
    setReturnQueryVerified("");
    setCgReturn(null); setCgReturnNotice("");
    setMusicReturn(null); setMusicReturnNotice("");
    setWritingReturn(null); setReturnNotice("");
    let input;
    try {
      input = businessReturnInput(new URLSearchParams(returnQuery));
    } catch {
      setReturnNotice("无法确认原工作台，请从业务入口重新进入。");
      return;
    }
    if (!input || runtime.status !== "ready") return;
    const receivers = {
      cg: [setCgReturn, setCgReturnNotice, "原图文内容暂时无法确认，请从内容入口重新进入。"],
      music: [setMusicReturn, setMusicReturnNotice, "原歌曲内容暂时无法确认，请从歌曲入口重新进入。"],
      writing: [setWritingReturn, setReturnNotice, "暂时无法确认原章节，请从写作入口重新进入。"],
    };
    const [save, notice, message] = receivers[input.kind];
    validateBusinessReturn(input.kind, input.value)
      .then((target) => { if (current) { save(target); setReturnQueryVerified(returnQuery); } })
      .catch(() => { if (current) notice(message); });
    return () => { current = false; };
  }, [runtime.status, runtime.companyId, returnQuery]);
  const [providers, setProviders] = useState([]);
  const [models, setModels] = useState([]);
  const [preference, setPreference] = useState(null);
  const [availableModels, setAvailableModels] = useState({ company: "", scope: null, models: [] });
  const [selectedId, setSelectedId] = useState("deepseek");
  const [endpoint, setEndpoint] = useState("");
  const [secret, setSecret] = useState("");
  const [curatedModels, setCuratedModels] = useState("");
  const [verified, setVerified] = useState({});
  const [discovered, setDiscovered] = useState([]);
  const [chosenModel, setChosenModel] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [credentialStorage, setCredentialStorage] = useState("");
  const [attempt, setAttempt] = useState(null);
  const [preparedScope, setPreparedScope] = useState(null);
  const flight = useRef(null);
  const currentScope = useRef("");

  const metadataScope = useRef(null);
  const metadataRequest = useRef(0);
  useLayoutEffect(() => {
    metadataScope.current = runtime.status === "ready" ? { company: runtime.companyId || "" } : null;
    return () => { metadataScope.current = null; };
  }, [runtime.status, runtime.companyId]);
  const load = useCallback(async () => {
    const scope = metadataScope.current;
    if (!scope) return;
    const request = ++metadataRequest.current;
    const providerPayload = await getAIProviders();
    if (metadataScope.current !== scope || metadataRequest.current !== request) return;
    const [modelResult, preferenceResult] = await Promise.allSettled([getEnabledModels(), getModelPreference()]);
    if (metadataScope.current !== scope || metadataRequest.current !== request) return;
    const loadedModels = modelResult.status === "fulfilled" ? modelResult.value.models || [] : [];
    const preferencePayload = preferenceResult.status === "fulfilled" ? preferenceResult.value : {};
    setProviders(providerPayload.providers || []);
    setModels(loadedModels);
    setPreference(preferencePayload.preference || null);
    setAvailableModels({ company: scope.company, scope, models: preferencePayload.available_models || [] });
  }, []);
  useEffect(() => {
    if (runtime.status !== "ready") return;
    const scope = metadataScope.current;
    const pending = load();
    const request = metadataRequest.current;
    pending.catch((caught) => {
      if (metadataScope.current === scope && metadataRequest.current === request) setError(caught?.message || "模型信息暂时无法读取。");
    });
  }, [runtime.status, runtime.companyId, load]);
  const selected = useMemo(() => providers.find((item) => item.provider_id === selectedId) || providers[0], [providers, selectedId]);
  const selectedProviderId = selected?.provider_id;
  const selectedBaseUrl = selected?.base_url;
  useEffect(() => { if (selectedProviderId) { setEndpoint(selectedBaseUrl || ""); setDiscovered([]); setChosenModel(""); setError(""); } }, [selectedProviderId, selectedBaseUrl]);
  const scopeInput = JSON.stringify([runtime.companyId || "", selectedProviderId, endpoint]);
  useLayoutEffect(() => { currentScope.current = scopeInput; }, [scopeInput]);
  useEffect(() => {
    let active = true;
    setPreparedScope(null); setAttempt({ state: "CHECKING" }); setSecret("");
    setVerified((current) => { if (!(selectedProviderId in current)) return current; const next = { ...current }; delete next[selectedProviderId]; return next; });
    setDiscovered([]); setChosenModel("");
    if (runtime.status !== "ready" || !selectedProviderId) return () => { active = false; };
    (async () => {
      const bytes = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(endpoint));
      const scope = { company: runtime.companyId || "", provider: selectedProviderId, endpoint_hash: Array.from(new Uint8Array(bytes), (v) => v.toString(16).padStart(2, "0")).join("") };
      if (!active) return;
      if (!probeSessionGuard(scope)) { setAttempt({ state: "LOCAL_GUARD_UNAVAILABLE" }); setError(""); return; }
      setPreparedScope({ ...scope, input: scopeInput });
      const receipt = readAttempt(scope);
      if (receipt && (receipt.company !== scope.company || receipt.endpoint_hash !== scope.endpoint_hash)) { setAttempt({ state: "UNKNOWN" }); return; }
      if (receipt?.state === "KNOWN") {
        const metadata = await workspaceFetch("/api/workspace/credentials");
        if (!active) return;
        if (!metadata?.credentials?.some((value) => validCredential(value, scope.provider, receipt.ref))) { setAttempt(writeAttempt(scope, "UNKNOWN", receipt.ref)); return; }
      }
      if (active) setAttempt(receipt?.state === "PENDING" ? { ...receipt, state: "UNKNOWN" } : receipt);
    })().catch(() => { if (active) setAttempt({ state: "UNKNOWN" }); });
    return () => { active = false; };
  }, [runtime.status, runtime.companyId, selectedProviderId, endpoint, scopeInput]);
  const providerModels = models.filter((item) => item.provider_type === selected?.provider_id);
  const requiresKey = selected && !["none", "optional_bearer"].includes(selected.auth);
  const savedCredentialRef = providerModels.find((item) => item.credential_ref)?.credential_ref || "";
  const credentialHint = credentialStorage === "process_memory" || savedCredentialRef.startsWith("local-dev://")
    ? "当前开发环境仅在本次进程保留。"
    : "安装版由本机 macOS Keychain 保管。";

  const held = attempt && attempt.state !== "KNOWN";
  // Only the existing server-validated metadata can offer a saved default choice.
  const choiceModels = runtime.status !== "ready" || held || !preparedScope || preparedScope.input !== scopeInput
    || availableModels.scope !== metadataScope.current
    || availableModels.company !== (runtime.companyId || "") ? [] : availableModels.models
      .filter((model) => model.source === "tenant_private" && model.provider_id === selectedProviderId
        && providerModels.some((saved) => saved.tenant_id === TENANT_ID && saved.enabled
          && saved.model_name === model.model_name
          && saved.base_url?.replace(/\/+$/, "") === endpoint.replace(/\/+$/, "")))
      .map((model) => ({ capability_id: model.model_key, model_id: model.model_name, display_name: model.display_name || model.model_name }));
  const selectedChoices = choiceModels.filter((model) => model.capability_id === (chosenModel || preference?.model_key));
  const choiceId = selectedChoices.length === 1 ? selectedChoices[0].capability_id : "";
  const connect = async () => {
    if (!selected || flight.current || held || !preparedScope || preparedScope.input !== currentScope.current) return;
    const scope = preparedScope;
    const fresh = readAttempt(scope);
    if (fresh && (fresh.state !== "KNOWN" || fresh.company !== scope.company || fresh.endpoint_hash !== scope.endpoint_hash || fresh.ref !== attempt?.ref)) { setAttempt({ state: "UNKNOWN" }); setError(UNKNOWN_SAVE); return; }
    let credentialRef = attempt?.state === "KNOWN" ? attempt.ref : savedCredentialRef;
    if (requiresKey && !secret.trim() && !credentialRef) { setError("请输入这个提供方的 API Key。"); return; }
    flight.current = scope.input;
    setBusy(true); setError("");
    let phase = "metadata";
    const isCurrent = () => currentScope.current === scope.input;
    try {
      if (requiresKey && credentialRef && !attempt) {
        const metadata = await workspaceFetch("/api/workspace/credentials");
        const value = metadata?.credentials?.find((item) => validCredential(item, scope.provider, credentialRef));
        if (!value) throw new Error("Credential metadata unavailable");
        const receipt = writeAttempt(scope, "KNOWN", credentialRef, value.storage);
        if (receipt.state !== "KNOWN") throw new Error("Credential receipt unavailable");
        if (isCurrent()) setAttempt(receipt);
      }
      if (!isCurrent()) return;
      if (requiresKey && secret.trim()) {
        const pending = writeAttempt(scope, "PENDING", credentialRef);
        if (pending.state !== "PENDING") { setAttempt({ state: "LOCAL_GUARD_UNAVAILABLE" }); setSecret(""); setError(""); return; }
        setAttempt(pending);
        phase = "storage";
        const existingCredentialId = credentialRef.split("/").pop() || "";
        const credential = existingCredentialId
          ? await updateCredential(existingCredentialId, scope.provider, secret)
          : await createSessionCredential(scope.provider, secret);
        if (!validCredential(credential, scope.provider, credentialRef)) throw new Error("Credential response unavailable");
        credentialRef = credential.credential_ref;
        const receipt = writeAttempt(scope, "KNOWN", credentialRef, credential.storage);
        if (isCurrent()) { setSecret(""); setCredentialStorage(credential.storage); setAttempt(receipt); if (receipt.state !== "KNOWN") setError(LOCAL_RECEIPT_FAILED); }
        if (receipt.state !== "KNOWN" || !isCurrent()) return;
      }
      phase = "provider";
      const modelIds = curatedModels.split(/[\n,]/).map((item) => item.trim()).filter(Boolean);
      const result = await connectAIProvider(scope.provider, { credential_ref: credentialRef, base_url: endpoint, model_ids: modelIds, save: true });
      if (!isCurrent()) return;
      setVerified((current) => ({ ...current, [scope.provider]: result.health === "healthy" }));
      setDiscovered(result.models || []); setChosenModel(""); setSecret("");
      await load();
    } catch (caught) {
      if (phase !== "provider") {
        const notStarted = phase === "storage" && [404, 422].includes(caught?.status) && caught?.code === "CREDENTIAL_WRITE_NOT_STARTED" && ["validation", "preflight"].includes(caught?.phase) && caught?.certainty === "not_started";
        const receipt = writeAttempt(scope, notStarted ? "BLOCKED" : "UNKNOWN", credentialRef);
        if (isCurrent()) {
          setAttempt(receipt); setSecret("");
          let message = UNKNOWN_SAVE;
          if (notStarted) message = receipt.state === "BLOCKED" ? WRITE_NOT_STARTED : "服务端确认本次写入未开始，但本地保护回执失败；已停止连接。";
          else if (phase === "storage" && [404, 422].includes(caught?.status) && caught?.code === "CREDENTIAL_NATIVE_WRITE_UNCONFIRMED" && caught?.phase === "native_store" && caught?.certainty === "unknown") message = NATIVE_WRITE_UNCONFIRMED;
          else if (phase === "storage" && caught?.status === 500 && caught?.code === "CREDENTIAL_METADATA_UNCONFIRMED" && caught?.phase === "metadata" && caught?.certainty === "native_returned_success") message = METADATA_UNCONFIRMED;
          else if (phase === "storage" && caught?.status === 500 && caught?.code === "CREDENTIAL_METADATA_UNCONFIRMED" && caught?.phase === "metadata" && caught?.certainty === "not_started") message = METADATA_ONLY_UNCONFIRMED;
          else if (phase === "storage" && caught?.status === 500 && caught?.code === "CREDENTIAL_AUDIT_FAILED" && caught?.phase === "audit" && caught?.certainty === "metadata_returned_success") message = AUDIT_FAILED;
          setError(message);
        }
      } else if (isCurrent()) { setVerified((current) => ({ ...current, [scope.provider]: false })); setError(requiresKey ? "凭据已保存；模型尚未验证。请先确认服务地址与连接权限。" : "本地模型尚未验证，请确认本地服务。"); }
    } finally { flight.current = null; setBusy(false); }
  };

  const choose = async () => {
    const model = choiceModels.find((item) => item.capability_id === choiceId);
    if (!model || flight.current || !preparedScope || preparedScope.input !== currentScope.current
      || availableModels.scope !== metadataScope.current) return;
    const fresh = readAttempt(preparedScope);
    if (fresh && (fresh.state !== "KNOWN" || fresh.company !== preparedScope.company
      || fresh.endpoint_hash !== preparedScope.endpoint_hash || fresh.ref !== attempt?.ref)) {
      setAttempt({ state: "UNKNOWN" }); setError(UNKNOWN_SAVE); return;
    }
    const scope = preparedScope.input;
    const owner = metadataScope.current;
    flight.current = scope; setBusy(true); setError("");
    try {
      const result = await setModelPreference(model.capability_id);
      if (currentScope.current !== scope || metadataScope.current !== owner) return;
      setPreference(result.preference);
      sessionStorage.setItem("curis.v1.conversationModel", JSON.stringify({ capability_id: model.capability_id, model_id: model.model_id, provider_id: selected.provider_id }));
    } catch {
      if (currentScope.current === scope && metadataScope.current === owner) setError("默认模型选择尚未确认，请先重新读取当前配置；不要重复测试连接。");
    } finally { flight.current = null; setBusy(false); }
  };

  return <TerraShell topCrumb="设置 · 模型" assistantContext={{ page: "models" }}><div className="mx-auto max-w-[1120px] text-ui-txt"><header className="mb-6">{settingsBack && <a className="mb-3 block text-sm font-semibold text-ui-primary" href={settingsBack}>← 返回模型设置</a>}{cgReturn && returnQueryVerified === returnQuery && runtime.status === "ready" && cgReturn.company && <a className="mb-3 block text-sm font-semibold text-ui-primary" href={cgReturn.href}>{cgReturn.label}</a>}{cgReturnNotice && <p role="status" className="mb-3 text-sm">{cgReturnNotice}</p>}{musicReturn && returnQueryVerified === returnQuery && runtime.status === "ready" && musicReturn.company && <a className="mb-3 block text-sm font-semibold text-ui-primary" href={musicReturn.href}>{musicReturn.label}</a>}{musicReturnNotice && <p role="status" className="mb-3 text-sm">{musicReturnNotice}</p>}{writingReturn && returnQueryVerified === returnQuery && runtime.status === "ready" && writingReturn.company && <a className="mb-3 block text-sm font-semibold text-ui-primary" href={writingReturn.href}>{writingReturn.label}</a>}{returnNotice && <p role="status" className="mb-3 text-sm">{returnNotice}</p>}<span className="text-xs font-semibold text-ui-primary">模型与 AI 提供方</span><h1 className="mt-2 text-3xl font-semibold tracking-[-0.025em]">模型管理</h1><p className="mt-2 max-w-2xl text-sm leading-6 text-ui-txt-2">查看已保存的模型配置，管理提供方与默认模型。连接测试需由你主动发起。</p></header>{children}<div className="grid gap-4 lg:grid-cols-[300px_minmax(0,1fr)]"><aside className="rounded-2xl border border-ui-line bg-ui-surface p-2"><p className="px-3 py-2 text-xs font-semibold text-ui-txt-3">模型提供方</p>{providers.map((provider) => <button key={provider.provider_id} disabled={busy} onClick={() => setSelectedId(provider.provider_id)} className={`mb-1 flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left ${provider.provider_id === selected?.provider_id ? "bg-ui-primary-soft" : "hover:bg-ui-surface-2"}`}><span className="grid h-9 w-9 place-items-center rounded-lg border border-ui-line bg-ui-surface text-xs font-bold text-ui-txt-2">{(COPY[provider.provider_id]?.[0] || provider.name).slice(0, 2)}</span><span className="min-w-0 flex-1"><strong className="block truncate text-sm">{COPY[provider.provider_id]?.[0] || provider.name}</strong><small className={`mt-0.5 block text-[11px] ${verified[provider.provider_id] ? "text-ui-green" : "text-ui-txt-3"}`}>{statusLabel(provider, verified[provider.provider_id])}</small></span></button>)}</aside>{selected ? <section className="rounded-2xl border border-ui-line bg-ui-surface p-6"><div className="flex flex-wrap items-start justify-between gap-4"><div><h2 className="text-xl font-semibold">{COPY[selected.provider_id]?.[0] || selected.name}</h2><p className="mt-2 text-sm text-ui-txt-2">{COPY[selected.provider_id]?.[1] || "模型提供方"}</p></div><a href={selected.documentation || "#"} target="_blank" rel="noreferrer" className="text-sm font-semibold text-ui-primary-text">官方文档 ↗</a></div><div className="mt-6 grid gap-4"><label className="text-sm font-medium">服务地址<input disabled={busy} value={endpoint} onChange={(event) => setEndpoint(event.target.value)} className="mt-2 h-11 w-full rounded-xl border border-ui-line bg-ui-surface px-3" /></label>{requiresKey ? <label className="text-sm font-medium">API Key<input disabled={busy || Boolean(held)} type="password" autoComplete="off" value={secret} onChange={(event) => setSecret(event.target.value)} placeholder={savedCredentialRef ? "留空可重新验证已保存凭证" : "输入 API Key"} className="mt-2 h-11 w-full rounded-xl border border-ui-line bg-ui-surface px-3" /><span className="mt-1 block text-[11px] font-normal text-ui-txt-3">明文不会写入 SQLite。{credentialHint}</span></label> : <p className="rounded-xl bg-ui-surface-2 p-3 text-sm text-ui-txt-2">本地提供方不需要 API Key，请先启动本地模型服务。</p>}{selected.discovery_mode === "curated" ? <label className="text-sm font-medium">模型名称<textarea disabled={busy} value={curatedModels} onChange={(event) => setCuratedModels(event.target.value)} placeholder="每行一个模型名称" className="mt-2 min-h-20 w-full rounded-xl border border-ui-line bg-ui-surface p-3" /></label> : null}<button onClick={connect} disabled={busy || Boolean(held) || !preparedScope} className="w-fit rounded-xl bg-ui-primary px-4 py-2.5 text-sm font-semibold text-ui-primary-fg disabled:opacity-50">{busy ? "正在测试…" : "测试连接并发现模型"}</button>{choiceModels.length ? <div className="rounded-xl border border-ui-line p-4"><p role="status" className="mb-3 text-sm text-ui-txt-2">{discovered.length && verified[selectedProviderId] ? "连接成功，请选择模型并设为默认。" : "已读取可用的已保存模型；未重新测试连接。"}</p><label className="text-sm font-medium">选择模型<select disabled={busy} value={choiceId} onChange={(event) => setChosenModel(event.target.value)} className="mt-2 h-11 w-full rounded-lg border border-ui-line bg-ui-surface px-3"><option value="" disabled>请选择模型</option>{choiceModels.map((model) => <option key={model.capability_id} value={model.capability_id}>{model.display_name}</option>)}</select></label><button onClick={choose} disabled={busy || !choiceId} className="mt-3 rounded-lg border border-ui-primary px-3 py-2 text-sm font-semibold text-ui-primary-text">设为默认</button></div> : null}{providerModels.length ? <div><h3 className="text-sm font-semibold">已保存模型</h3><ul className="mt-2 space-y-2">{providerModels.map((model) => <li key={`${model.provider_type}:${model.model_name}`} className="rounded-lg bg-ui-surface-2 px-3 py-2 text-sm">{model.model_name || model.name}<span className="ml-2 text-xs text-ui-txt-3">{choiceModels.some((choice) => choice.model_id === model.model_name) ? "可选择" : "等待重新验证"}</span></li>)}</ul></div> : null}{preference ? <p className="text-xs text-ui-txt-3">当前租户默认：{preference.model_name}</p> : null}{held && attempt.state !== "CHECKING" && !error ? <p role="status" className="text-sm text-ui-amber">{attempt.state === "LOCAL_GUARD_UNAVAILABLE" ? LOCAL_GUARD_UNAVAILABLE : attempt.state === "BLOCKED" ? WRITE_NOT_STARTED : UNKNOWN_SAVE}</p> : null}{error ? <p role="status" className="rounded-lg bg-ui-amber-soft px-3 py-2 text-sm text-ui-amber">{error}</p> : null}<details className="text-xs text-ui-txt-3"><summary className="cursor-pointer font-semibold">查看连接详情</summary><dl className="mt-2 grid gap-1"><div>认证方式：{selected.auth}</div><div>模型发现：{selected.discovery_mode}</div><div>协议：{selected.protocol}</div></dl></details></div></section> : null}</div></div></TerraShell>;
}
