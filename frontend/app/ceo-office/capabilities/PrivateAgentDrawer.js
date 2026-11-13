"use client";

import { useEffect, useRef, useState } from "react";
import {
  TerraButton,
  TerraDrawer,
  TerraInput,
} from "../../../components/terra/TerraPrimitives.js";
import { createPrivateCapability, getPrivateCapabilities, getAgentAllowanceCompanies, getAgentAllowance, saveAgentAllowance, revokeAgentAllowance, createAgentAuthorization, controlAgentBrowser, getAgentCodexAuth, controlAgentCodexAuth, discoverLocalAgents, getLocalAgentEmployees, getEmployeeCapabilities, addEmployeeAgentBinding, updateDshAgentAccount } from "../../../lib/capabilities.js";

export function AgentAllowancePanel() {
  const [companies, setCompanies] = useState([]), [company, setCompany] = useState("");
  const [value, setValue] = useState(null), [selected, setSelected] = useState([]);
  const [browserStates, setBrowserStates] = useState({});
  const [authStates, setAuthStates] = useState({}), [authUnknown, setAuthUnknown] = useState({});
  const authEpoch = useRef(0), authReads = useRef(new Set()), allowanceCompany = useRef("");
  const [companyRead, setCompanyRead] = useState(0), [unknown, setUnknown] = useState(false);
  const pending = useRef(false);
  const allowanceRead = useRef(0);
  const companyScope = useRef(company);
  useEffect(() => { companyScope.current = company; authEpoch.current++; setBrowserStates({}); setAuthStates({}); setAuthUnknown({}); allowanceCompany.current = ""; return () => { companyScope.current = ""; authEpoch.current++; }; }, [company]);
  const [consent, setConsent] = useState(false), [busy, setBusy] = useState(false), [error, setError] = useState("");
  const [unlimitedConsent, setUnlimitedConsent] = useState(false);
  useEffect(() => {
    let active = true;
    getAgentAllowanceCompanies().then((response) => {
      if (!active) return;
      const rows = Array.isArray(response) ? response : response.companies || [];
      setCompanies(rows);
      if (rows.length === 1) setCompany(rows[0].company_id);
    }).catch(() => { if (active) setError("公司清单暂时无法读取。"); });
    return () => { active = false; };
  }, [companyRead]);
  useEffect(() => {
    const ticket = ++allowanceRead.current;
    let active = true; setValue(null); setSelected([]); setConsent(false); setUnlimitedConsent(false); setUnknown(false);
    if (company) getAgentAllowance(company).then((next) => {
      if (active && ticket === allowanceRead.current) { allowanceCompany.current = company; setValue(next); setSelected((next.policy?.bindings || []).map((item) => item.binding_ref)); setError(""); }
    }).catch((reason) => { if (active && ticket === allowanceRead.current) setError(reason.message || "许可暂时无法读取。"); });
    return () => { active = false; };
  }, [company]);
  async function readAuth(bindingRef) {
    const originalCompany = company, epoch = authEpoch.current, key = epoch + ":" + bindingRef;
    if (!company || pending.current || authReads.current.has(key)) return;
    authReads.current.add(key);
    try {
      const next = await getAgentCodexAuth(originalCompany, bindingRef);
      if (companyScope.current === originalCompany && authEpoch.current === epoch) {
        setAuthStates((rows) => ({ ...rows, [bindingRef]: next }));
        setAuthUnknown((rows) => ({ ...rows, [bindingRef]: false }));
      }
    } catch {
      if (companyScope.current === originalCompany && authEpoch.current === epoch) {
        setAuthStates((rows) => ({ ...rows, [bindingRef]: null }));
        setAuthUnknown((rows) => ({ ...rows, [bindingRef]: true }));
      }
    } finally { authReads.current.delete(key); }
  }
  useEffect(() => {
    if (allowanceCompany.current === company) value?.binding_options.filter(item => !item.agent_kind || item.agent_kind === "codex-cli").forEach((item) => readAuth(item.binding_ref));
  }, [company, value]);
  useEffect(() => {
    const refs = Object.keys(authStates).filter((ref) => !authUnknown[ref] && ["STARTING", "WAITING_FOR_LOGIN", "DISCONNECTING", "IN_USE"].includes(authStates[ref]?.state));
    if (!refs.length) return;
    const timer = window.setInterval(() => refs.forEach(readAuth), 1000);
    return () => window.clearInterval(timer);
  }, [company, authStates, authUnknown]);
  async function auth(bindingRef, action) {
    if (pending.current || !company || authUnknown[bindingRef] || !authStates[bindingRef]) return;
    const originalCompany = company, epoch = ++authEpoch.current, generation = authStates[bindingRef].generation;
    pending.current = true; setBusy(true);
    setAuthStates((rows) => ({ ...rows, [bindingRef]: null }));
    try {
      const next = await controlAgentCodexAuth(originalCompany, bindingRef, action, { request_id: crypto.randomUUID(), expected_generation: generation });
      if (companyScope.current === originalCompany && authEpoch.current === epoch) setAuthStates((rows) => ({ ...rows, [bindingRef]: next }));
    } catch {
      if (companyScope.current === originalCompany && authEpoch.current === epoch) setAuthUnknown((rows) => ({ ...rows, [bindingRef]: true }));
    } finally { pending.current = false; if (companyScope.current) setBusy(false); }
  }
  async function read() {
    if (!company || pending.current) return;
    const originalCompany = company;
    const ticket = ++allowanceRead.current;
    pending.current = true;
    setBusy(true);
    try { const next = await getAgentAllowance(originalCompany); if (companyScope.current === originalCompany && ticket === allowanceRead.current) { setValue(next); setSelected((next.policy?.bindings || []).map((item) => item.binding_ref)); setConsent(false); setUnlimitedConsent(false); setUnknown(false); setBrowserStates({}); setError(""); } }
    catch (reason) { if (companyScope.current === originalCompany && ticket === allowanceRead.current) { setUnknown(true); setError(reason.message || "许可暂时无法读取。"); } }
    finally { pending.current = false; if (companyScope.current) setBusy(false); }
  }
  async function save(enabled, newAuthorization = false) {
    if (!value || pending.current || unknown) return;
    const originalCompany = company;
    allowanceRead.current++;
    pending.current = true;
    setBusy(true); setError("");
    try {
      const payload = { request_id: crypto.randomUUID(), expected_revision: value.revision, authorization_ref: value.authorization_ref, enabled,
        consent: enabled && consent, binding_refs: enabled ? selected : [], unlimited_consent: enabled && unlimitedConsent };
      const next = newAuthorization ? await createAgentAuthorization(company, {
        request_id: payload.request_id, previous_authorization_ref: value.authorization_ref,
        expected_revision: payload.expected_revision, binding_refs: selected, consent,
      }) : await (enabled ? saveAgentAllowance : revokeAgentAllowance)(company, payload);
      if (companyScope.current === originalCompany) { setValue(next); setConsent(false); setUnlimitedConsent(false); }
    } catch (reason) { if (companyScope.current === originalCompany) { setUnknown(true); setConsent(false); setUnlimitedConsent(false); setError((reason.message || "保存结果待核验。") + " 请读取当前许可；不会自动重复提交。"); } }
    finally { pending.current = false; if (companyScope.current) setBusy(false); }
  }
  async function browser(bindingRef, action) {
    if (pending.current || !company || unknown) return;
    const originalCompany = company;
    pending.current = true;
    setBusy(true); setError("");
    setBrowserStates((rows) => ({ ...rows, [bindingRef]: null }));
    try {
      const result = await controlAgentBrowser(originalCompany, bindingRef, action);
      if (companyScope.current !== originalCompany) return;
      if (result.company_id !== originalCompany || result.binding_ref !== bindingRef) throw new Error("浏览器回执不属于当前员工。");
      const safe = ["UNAVAILABLE", "STOPPED"].includes(result.state)
        ? result : { ...result, state: "UNAVAILABLE", reason: "只读环境尚未核验，不能使用旧浏览器连接。" };
      setBrowserStates((rows) => ({ ...rows, [bindingRef]: safe }));
    } catch (reason) { if (companyScope.current === originalCompany) setError(reason.message || "浏览器连接尚未核验。"); }
    finally { pending.current = false; if (companyScope.current) setBusy(false); }
  }
  const differentAgent = Boolean(value?.authorization_subject && selected.some(ref => {
    const item = value.binding_options.find(option => option.binding_ref === ref);
    return item?.authorization_subject && JSON.stringify(item.authorization_subject) !== JSON.stringify(value.authorization_subject);
  }));
  return <section className="space-y-3 border-t border-ui-line pt-4" aria-label="Agent 额度许可">
    <h3>允许员工使用所选 Agent 的额度</h3>
    <label>公司<select value={company} disabled={busy} onChange={(event) => setCompany(event.target.value)}>
      <option value="">选择公司</option>{companies.map((item) => <option key={item.company_id} value={item.company_id}>{item.name}</option>)}
    </select></label>
    <button type="button" disabled={busy} onClick={() => setCompanyRead((n) => n + 1)}>刷新公司列表</button>
    <TerraButton type="button" disabled={busy || !company} onClick={read}>读取当前许可</TerraButton>
    {value && <>
      <p>{value.limit_mode === "UNLIMITED" ? "当前公司许可不设调用次数上限" : "当前许可最多 4 次"}，每次最多 90 秒。已占用 {value.used_calls} 次{value.limit_mode === "UNLIMITED" ? "。" : `，剩余 ${value.remaining_calls} 次。`}</p>
      <p>重开应用、变更绑定或再次确认不会重置次数。历史用量会保留。</p>
      {value.authorization_history?.length > 0 && <p>此前 {value.authorization_history.length} 次授权共占用 {value.authorization_history.reduce((sum, item) => sum + item.used_calls, 0)} 次调用，仍可核对原结果。</p>}
      <p>使用现有订阅或已购额度，不购买、不充值。停止、失败和结果未知的调用仍占用次数，不自动重试；实际折算费用尚未核验。</p>
      {value.binding_options.some(item => !item.agent_kind || item.agent_kind === "codex-cli") && <p>Codex 通过官方服务登录，连接按当前公司和 Agent 隔离。登录不等于执行许可；公开网页只读环境仍需独立验证，网页账号登录、实时接管和发布不可用。</p>}
      {value.binding_options.map((item) => <div key={item.binding_ref}>
        <label className="block"><input type="checkbox" disabled={busy} checked={selected.includes(item.binding_ref)} onChange={(event) => { setSelected((rows) => event.target.checked ? [...rows, item.binding_ref] : rows.filter((ref) => ref !== item.binding_ref)); setConsent(false); setUnlimitedConsent(false); }} /> {item.employee_name} · {item.agent_name}</label>
        {(!item.agent_kind || item.agent_kind === "codex-cli") ? <>
        <div className="flex gap-2">
          <button type="button" disabled={busy} onClick={() => readAuth(item.binding_ref)}>读取 Codex 连接</button>
          <button type="button" disabled={busy || authUnknown[item.binding_ref] || !["DISCONNECTED", "HELD"].includes(authStates[item.binding_ref]?.state)} onClick={() => auth(item.binding_ref, "connect")}>登录 Codex</button>
          <button type="button" disabled={busy || authUnknown[item.binding_ref] || !["CONNECTED", "IN_USE", "STARTING", "WAITING_FOR_LOGIN"].includes(authStates[item.binding_ref]?.state)} onClick={() => auth(item.binding_ref, "disconnect")}>断开 Codex</button>
        </div>
        <p role="status">{authUnknown[item.binding_ref] ? "连接结果尚未确认，请读取当前连接；不会自动重复提交。" : ({ CONNECTED: "Codex 已连接。", DISCONNECTED: "Codex 尚未连接。", STARTING: "正在准备官方登录。", WAITING_FOR_LOGIN: "请在官方页面输入临时代码。", DISCONNECTING: "正在停止原执行并断开连接。", IN_USE: "当前连接正在使用。", HELD: "原连接尚未通过核验；重新登录会建立新连接。", UNAVAILABLE: "Codex 连接环境尚未通过核验。" }[authStates[item.binding_ref]?.state] || "正在读取 Codex 连接。")}</p>
        {authStates[item.binding_ref]?.state === "WAITING_FOR_LOGIN" && <p><a href={authStates[item.binding_ref].verification_url} target="_blank" rel="noopener noreferrer">打开 Codex 官方登录页</a> · 临时代码：<code>{authStates[item.binding_ref].user_code}</code></p>}
        <div className="flex gap-2"><button type="button" disabled={busy || unknown} onClick={() => browser(item.binding_ref, "prepare")}>准备公开网页只读</button>
          <button type="button" disabled={busy || unknown} onClick={() => browser(item.binding_ref, "")}>核对只读环境</button>
          <button type="button" disabled={busy || unknown} onClick={() => browser(item.binding_ref, "stop")}>停止准备窗口</button></div>
        {browserStates[item.binding_ref] && <p role="status">{browserStates[item.binding_ref].reason}</p>}
        </> : <p role="status">{item.agent_name} 已登记配置；连接、认证、费用和真实执行仍待核验。不使用 Codex 登录或授权。</p>}
      </div>)}
      <p>断开会先停止使用该连接的原执行。本地断开不代表官方账号远程撤销；需撤销远程授权时请使用官方账号设置。</p>
      <p>执行被停止或连接结果无法确认时，会暂停使用该连接，需要重新登录。</p>
      {!value.binding_options.length && <p>请先在<a href="/ceo-office/organization">员工资料</a>中绑定已登记的 Agent。</p>}
      <label className="block"><input type="checkbox" checked={consent} disabled={busy} onChange={(event) => setConsent(event.target.checked)} /> 我确认以上范围，并允许选中员工使用既有额度。</label>
      <label className="block"><input type="checkbox" checked={unlimitedConsent} disabled={busy} onChange={(event) => setUnlimitedConsent(event.target.checked)} /> 我明确允许当前公司选中员工使用既有订阅或已购额度，不设调用次数上限。</label>
      {differentAgent && <p role="status">所选 Agent 或安装版本不属于当前授权。另行授权将创建独立的 4 次调用；旧授权与用量保留，不转移费用或次数，当前活动授权将切换。</p>}
      <p role="status">{unknown ? "许可状态尚未确认，请读取当前许可后再操作。" : value.reason}</p>
      <div className="flex gap-3"><TerraButton type="button" disabled={busy || unknown || differentAgent || !consent || !selected.length || (!(value.remaining_calls > 0) && !unlimitedConsent)} onClick={() => save(true)}>确认许可</TerraButton>
      <TerraButton type="button" disabled={busy || unknown || !value.policy?.enabled} onClick={() => save(false)}>撤销许可</TerraButton>
      {(value.new_authorization_allowed || differentAgent) && <TerraButton type="button" disabled={busy || unknown || !consent || !selected.length} onClick={() => save(true, true)}>另行授权 4 次新调用</TerraButton>}</div>
    </>}
    {error && <p role="alert">{error}</p>}
  </section>;
}

// 自定义 Agent 接入类型（仅作 UI 选项，落进 metadata.kind；后端不强制）。
const AGENT_KINDS = [
  ["codex-cli", "Codex（执行前核验连接、授权与费用）"],
  ["openai-compatible", "OpenAI 兼容对话 Agent"],
  ["mcp", "MCP 工具型 Agent"],
  ["http", "HTTP / 自定义协议 Agent"],
];

const EMPTY = {
  capability_id: "",
  display_name: "",
  kind: "openai-compatible",
  endpoint: "",
  credential_ref: "",
  browser_skill_path: "",
};

export default function PrivateAgentDrawer({ open, onClose, onSuccess, editingAgent = null, companyId = "" }) {
  const [form, setForm] = useState(EMPTY);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [uncertain, setUncertain] = useState(false);
  const pending = useRef(false);
  const [localAgents, setLocalAgents] = useState(null), [localAgent, setLocalAgent] = useState(null);
  const [registered, setRegistered] = useState(null), [companies, setCompanies] = useState([]), [employees, setEmployees] = useState([]);
  const [company, setCompany] = useState(""), [employee, setEmployee] = useState("");
  const [bindingUnknown, setBindingUnknown] = useState(false), [bound, setBound] = useState(false);
  const [installationPath, setInstallationPath] = useState("");
  const [sharedAccount, setSharedAccount] = useState(false);
  const [editSnapshot, setEditSnapshot] = useState(null);
  const epoch = useRef(0);

  useEffect(() => {
    if (!open) return;
    setForm(EMPTY);
    setError("");
    setSubmitting(false);
    setUncertain(false);
    pending.current = false;
    setInstallationPath("");
    setSharedAccount(editingAgent?.metadata?.dsh_shared_account === true);
    setEditSnapshot(editingAgent);
    setLocalAgents(null); setLocalAgent(null); setRegistered(null); setCompanies([]); setEmployees([]);
    setCompany(""); setEmployee(""); setBindingUnknown(false); setBound(false);
    epoch.current++;
    return () => { epoch.current++; };
  }, [open, editingAgent, companyId]);

  async function discover(manual = false) {
    if (pending.current || registered || uncertain) return;
    const token = epoch.current;
    pending.current = true; setSubmitting(true); setError("");
    try {
      const value = await discoverLocalAgents(manual === true ? installationPath.trim() : "");
      if (token !== epoch.current) return;
      if (!Array.isArray(value.agents)) throw new Error("发现结果格式无效。");
      setLocalAgents(value.agents); setLocalAgent(null);
    } catch (reason) { if (token === epoch.current) setError(reason.message || "本机安装暂时无法读取。"); }
    finally { if (token === epoch.current) { pending.current = false; setSubmitting(false); } }
  }

  async function acceptRegistration(value) {
    if (!localAgent) return onSuccess?.(value);
    if (value.capability_id !== form.capability_id || value.metadata?.local_agent_ref !== localAgent.discovery_ref) throw new Error("登记回执与所选安装不一致。");
    if (localAgent.agent_id === "deepseek_harness" && value.metadata?.dsh_shared_account !== sharedAccount) throw new Error("登记回执未确认所选账号配置。");
    setRegistered(value); setUncertain(false);
    if (value.status !== "active") return;
    try { await loadEmployees(); }
    catch (reason) { setError("Agent 已登记；" + (reason.message || "员工列表暂时无法读取。")); }
  }

  async function loadEmployees() {
    const token = epoch.current;
    const [companyRows, employeeRows] = await Promise.all([getAgentAllowanceCompanies(), getLocalAgentEmployees()]);
    if (token !== epoch.current) return;
    if (!Array.isArray(companyRows.companies) || !Array.isArray(employeeRows.employees)) throw new Error("公司或员工列表格式无效，请重新读取。");
    setCompanies(companyRows.companies); setEmployees(employeeRows.employees);
  }

  async function bind(readOnly = false) {
    if (pending.current || !registered || !company || !employee || bound || (bindingUnknown && !readOnly)) return;
    if (!employees.some(item => item.id === employee && item.company_id === company && item.enabled !== false)) return setError("员工不属于当前公司。");
    const token = epoch.current;
    pending.current = true; setSubmitting(true); setError("");
    let wrote = false;
    try {
      const value = await getEmployeeCapabilities(employee);
      if (token !== epoch.current) return;
      if (value.employee_id !== employee || !Array.isArray(value.bindings)) throw new Error("员工绑定回执不一致。");
      const matches = value.bindings.filter(item => item.capability_source === "tenant_private" && item.capability_type === "agent" && item.capability_id === registered.capability_id);
      if (matches.length > 1) throw new Error("员工绑定不唯一，请在员工资料中核对。");
      if (matches.length === 1 && matches[0].enabled === true) { setBound(true); setBindingUnknown(false); return; }
      if (readOnly) { setBindingUnknown(false); setError("本次读取未确认启用绑定，可核对员工资料后明确重试。"); return; }
      if (matches.length) throw new Error("已有绑定已禁用，请在员工资料中明确处理；不会自动重新启用。");
      wrote = true;
      await addEmployeeAgentBinding(employee, company, registered.capability_id);
      const confirmed = await getEmployeeCapabilities(employee);
      if (token !== epoch.current) return;
      const current = confirmed.bindings?.filter(item => item.capability_source === "tenant_private" && item.capability_type === "agent" && item.capability_id === registered.capability_id && item.enabled === true);
      if (confirmed.employee_id !== employee || current?.length !== 1) throw new Error("绑定结果尚未确认。");
      setBound(true); setBindingUnknown(false);
    } catch (reason) {
      if (token === epoch.current) { if (wrote) setBindingUnknown(true); setError((reason.message || "绑定失败") + (wrote ? "。请读取绑定结果，不会自动重复提交。" : "")); }
    } finally { if (token === epoch.current) { pending.current = false; setSubmitting(false); } }
  }

  function update(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  async function submit(event) {
    event.preventDefault();
    if (pending.current || uncertain) return;
    if (!form.capability_id.trim()) return setError("请输入 Agent 标识（如 agent.my-agent）");
    if (!form.display_name.trim()) return setError("请输入 Agent 显示名称");
    setSubmitting(true);
    pending.current = true;
    const token = epoch.current;
    setError("");
    try {
      const created = await createPrivateCapability({
        capability_type: "agent",
        capability_id: form.capability_id.trim(),
        display_name: form.display_name.trim(),
        metadata: {
          ...(localAgent ? { local_agent_ref: localAgent.discovery_ref, ...(localAgent.agent_id === "deepseek_harness" ? { dsh_shared_account: sharedAccount } : {}), ...(localAgent.manual_selection ? { local_installation_path: localAgent.installation_path } : {}) } : { kind: form.kind,
          ...(form.kind === "codex-cli" ? { computer_access_intent: "ASK_WHEN_NEEDED",
            ...(form.browser_skill_path.trim() ? { browser_skill_path: form.browser_skill_path.trim() } : {}) }
            : { endpoint: form.endpoint.trim(), credential_ref: form.credential_ref.trim() }) }),
        },
      });
      if (token !== epoch.current) return;
      await acceptRegistration(created);
    } catch (err) {
      if (token !== epoch.current) return;
      setUncertain(true);
      setError((err?.message || "保存结果待核验") + "。请先读取登记结果，避免重复保存。");
    } finally {
      if (token === epoch.current) { pending.current = false; setSubmitting(false); }
    }
  }

  async function editAccount(readOnly = false) {
    if (pending.current || !editingAgent || !companyId || !editSnapshot?.revision || (uncertain && !readOnly)) return;
    const token = epoch.current;
    pending.current = true; setSubmitting(true); setError("");
    try {
      const value = readOnly
        ? (await getPrivateCapabilities("agent")).capabilities?.find(item => item.capability_id === editingAgent.capability_id)
        : await updateDshAgentAccount(editingAgent.capability_id, { company_id: companyId,
          expected_revision: editSnapshot.revision, dsh_shared_account: sharedAccount, consent: true });
      if (token !== epoch.current) return;
      if (!value || value.capability_id !== editingAgent.capability_id || !/^[0-9a-f]{64}$/.test(value.revision || "")
        || value.metadata?.agent_id !== "deepseek_harness"
        || value.metadata?.installation_ref !== editSnapshot.metadata?.installation_ref) throw Error("配置回执不一致，请保留现场核对。");
      if (value.metadata.dsh_shared_account === sharedAccount) { onSuccess?.(value); return; }
      if (!readOnly) throw Error("保存回执未确认所选配置。");
      setEditSnapshot(value); setUncertain(false); setError("本次读取未确认变更。请重新核对选择，再明确保存。");
    } catch (reason) {
      if (token === epoch.current) { setUncertain(true); setError((reason.message || "配置结果未知") + "。请读取配置结果，不会自动重复提交。"); }
    } finally { if (token === epoch.current) { pending.current = false; setSubmitting(false); } }
  }

  async function verify() {
    if (pending.current) return;
    pending.current = true; setSubmitting(true);
    const token = epoch.current;
    try {
      const result = await getPrivateCapabilities("agent");
      if (token !== epoch.current) return;
      const found = (result.capabilities || []).find((item) => item.capability_id === form.capability_id.trim());
      if (!found) { setUncertain(false); setError("本次读取未发现这个标识。请核对保留的输入后明确保存。"); }
      else if (localAgent && found.display_name === form.display_name.trim() && found.metadata?.local_agent_ref === localAgent.discovery_ref
        && (localAgent.agent_id !== "deepseek_harness" || found.metadata?.dsh_shared_account === sharedAccount)) await acceptRegistration(found);
      else if (!localAgent && found.display_name === form.display_name.trim() && found.metadata?.kind === form.kind
        && (form.kind === "codex-cli" ? (found.metadata.browser_skill_path || "") === form.browser_skill_path.trim()
          : found.metadata.endpoint === form.endpoint.trim() && found.metadata.credential_ref === form.credential_ref.trim())) onSuccess?.(found);
      else setError("这个标识已有不同配置。请关闭并核对已登记 Agent，不会覆盖原配置。");
    } catch (reason) { if (token === epoch.current) setError(reason.message || "登记结果仍无法确认，请稍后重新读取。"); }
    finally { if (token === epoch.current) { pending.current = false; setSubmitting(false); } }
  }

  return (
    <TerraDrawer
      open={open}
      title={editingAgent ? "编辑 DSH 账号配置" : "注册自定义 Agent"}
      description={editingAgent ? "调整原 Agent 的账号配置选择，保留员工绑定和历史记录；不会发起执行。" : "登记供员工选择的 Agent。Codex 登记后需在公司员工绑定中通过官方页面登录，不需要填写服务地址或凭证。登记不会发起执行。"}
      onClose={submitting ? undefined : onClose}
    >
      <div className="space-y-3">
        {editingAgent ? <form onSubmit={event => { event.preventDefault(); editAccount(); }} className="space-y-4">
          <p>{editingAgent.display_name} · {editingAgent.capability_id}</p>
          <label><input type="checkbox" checked={sharedAccount} disabled={submitting || uncertain} onChange={event => setSharedAccount(event.target.checked)} /> 使用此电脑默认 DSH 账号与配置</label>
          <p>由 DSH 自行使用已有登录及配置，Curis 不读取或复制密钥。已有插件和设置会加载，任务会写入 DSH 会话记录。</p>
          <p>运行中不能修改。员工绑定和历史成果保留；保存后需重新确认执行许可，已用次数不会重置。保存不代表连接、权限或费用已验证。</p>
          {!companyId && <p role="alert">请先选择当前公司。</p>}
          {error && <p role="alert">{error}</p>}
          <TerraButton type="button" variant="ghost" disabled={submitting} onClick={onClose}>取消</TerraButton>
          {uncertain && <TerraButton type="button" disabled={submitting} onClick={() => editAccount(true)}>读取配置结果</TerraButton>}
          <TerraButton type="submit" disabled={submitting || uncertain || !companyId || !editSnapshot?.revision || sharedAccount === (editSnapshot.metadata?.dsh_shared_account === true)}>确认变更账号配置</TerraButton>
        </form> : <>
        {!registered && <section aria-label="本机已有 Agent">
          <TerraButton type="button" disabled={submitting || uncertain} onClick={() => discover()}>发现本机 Agent</TerraButton>
          <label>其他应用路径<input aria-label="其他应用路径" placeholder="/Applications/应用名称.app" value={installationPath} disabled={submitting || uncertain} onChange={event => setInstallationPath(event.target.value)} /></label>
          <TerraButton type="button" disabled={submitting || uncertain || !installationPath.trim()} onClick={() => discover(true)}>读取所选应用安装</TerraButton>
          <p>仅检查公共应用目录的安装信息，不运行应用。其他品牌可登记为待核验。</p>
          {localAgents && (localAgents.length ? <ul>{localAgents.map(item => <li key={item.discovery_ref}>
            <button type="button" disabled={submitting || uncertain} onClick={() => { setLocalAgent(item); setSharedAccount(false); setForm({ ...EMPTY, capability_id: item.capability_id, display_name: item.name }); setError(""); }}>{item.name} · 选择添加</button>
            <p>{item.installation_path} · 仅发现安装</p><p>{item.limitation}</p>
          </li>)}</ul> : <p>未发现支持识别的本机安装。可继续使用下方自定义登记；未检测到不代表未安装。</p>)}
          {localAgent && <><p role="status">已选择 {localAgent.name}。{localAgent.limitation}</p><button type="button" disabled={submitting || uncertain} onClick={() => { setLocalAgent(null); setSharedAccount(false); setForm(EMPTY); }}>改为自定义登记</button></>}
          {localAgent?.agent_id === "deepseek_harness" && <div>
            <label><input type="checkbox" checked={sharedAccount} disabled={submitting || uncertain} onChange={event => setSharedAccount(event.target.checked)} /> 使用此电脑默认 DSH 账号与配置</label>
            <p>由 DeepSeek Harness 自行使用已有登录；Curis 不读取或复制密钥。已有插件和设置也会加载，任务会写入 DSH 会话记录。执行前自动选择并确认可用账号模型，不回退到 API Key。自定义配置位置暂不支持；未登录请先在 DSH 中登录。实际连接、权限和费用仍需核验。</p>
          </div>}
        </section>}
        {registered ? <section aria-label="绑定现有员工">
          <p role="status">{registered.display_name} 已登记。{registered.metadata?.limitation} 保存不代表连接或实际执行已验证。</p>
          {registered.status === "active" ? <>
            <TerraButton type="button" disabled={submitting || bindingUnknown || bound} onClick={async () => { try { await loadEmployees(); } catch (reason) { setError(reason.message); } }}>读取公司与员工</TerraButton>
            <label>公司<select aria-label="绑定公司" disabled={submitting || bindingUnknown || bound} value={company} onChange={event => { setCompany(event.target.value); setEmployee(""); setError(""); }}><option value="">请选择公司</option>{companies.map(item => <option key={item.company_id} value={item.company_id}>{item.name}</option>)}</select></label>
            <label>员工<select aria-label="绑定员工" disabled={submitting || bindingUnknown || bound || !company} value={employee} onChange={event => setEmployee(event.target.value)}><option value="">请选择员工</option>{employees.filter(item => item.company_id === company && item.enabled !== false).map(item => <option key={item.id} value={item.id}>{item.name}</option>)}</select></label>
            <TerraButton type="button" disabled={submitting || bindingUnknown || bound || !employee || !company} onClick={() => bind(false)}>绑定所选员工</TerraButton>
            {bindingUnknown && <TerraButton type="button" disabled={submitting} onClick={() => bind(true)}>读取绑定结果</TerraButton>}
            {bound && <p role="status">员工绑定已读回确认。实际执行仍需核验授权与当前工作条件。</p>}
            <a href="/ceo-office/organization">前往员工资料核对能力与执行许可</a>
          </> : <p>当前机器接口尚未验证，登记已保留，暂不能绑定执行。</p>}
          {error && <p role="alert">{error}</p>}
          <TerraButton type="button" disabled={submitting} onClick={() => onSuccess?.(registered)}>完成登记</TerraButton>
        </section> : <form onSubmit={submit} className="space-y-4">
        <fieldset disabled={submitting || uncertain} className="space-y-4">
        <TerraInput
          label="Agent 标识"
          readOnly={Boolean(localAgent)}
          required
          value={form.capability_id}
          onChange={(event) => update("capability_id", event.target.value)}
          hint="稳定标识，例如 agent.my-research-agent"
          autoFocus
        />
        <TerraInput
          label="显示名称"
          required
          value={form.display_name}
          onChange={(event) => update("display_name", event.target.value)}
        />
        {!localAgent && <div>
          <label htmlFor="pa-kind" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            接入类型
          </label>
          <select
            id="pa-kind"
            value={form.kind}
            onChange={(event) => update("kind", event.target.value)}
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
          >
            {AGENT_KINDS.map(([value, label]) => (
              <option key={value} value={value}>{label}</option>
            ))}
          </select>
        </div>}
        {!localAgent && form.kind === "codex-cli" && <TerraInput label="BrowserSkill 可执行文件（可选）"
          value={form.browser_skill_path} onChange={(event) => update("browser_skill_path", event.target.value)}
          placeholder="留空使用应用内置版本"
          hint="公开网页只读环境尚需独立验证；网页账号登录、实时接管与发布不可用。"/>}
        {!localAgent && form.kind !== "codex-cli" && <TerraInput
          label="接入地址 / 命令"
          value={form.endpoint}
          onChange={(event) => update("endpoint", event.target.value)}
          placeholder="https://agent.example.com 或 npx -y @my/agent"
          hint="Agent 的服务地址或启动命令"
        />}
        {!localAgent && form.kind !== "codex-cli" && <TerraInput
          label="凭证引用（不填明文）"
          value={form.credential_ref}
          onChange={(event) => update("credential_ref", event.target.value)}
          hint="仅填 scheme:reference，密钥放环境变量。格式 env:YOUR_ENV_VAR / vault:xxx / kms:xxx"
          placeholder="env:AGENT_API_KEY"
        />}
        <p className="text-xs text-ui-txt-3 bg-ui-surface-2 rounded-ui-sm p-3">
          登记后需要绑定到具体员工。保存配置不代表连接、技能或实际执行已验证。
        </p>
        </fieldset>
        {error && <p role="alert" className="text-xs text-ui-red">{error}</p>}
        <div className="flex justify-end gap-3 pt-2">
          <TerraButton type="button" variant="ghost" disabled={submitting} onClick={onClose}>取消</TerraButton>
          {uncertain && <TerraButton type="button" disabled={submitting} onClick={verify}>读取登记结果</TerraButton>}
          <TerraButton type="submit" disabled={submitting || uncertain}>
            {submitting ? "保存中…" : "保存自定义 Agent"}
          </TerraButton>
        </div>
      </form>}
        </>}
      </div>
    </TerraDrawer>
  );
}
