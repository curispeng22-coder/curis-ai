"use client";

import { Suspense, useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useParams, useSearchParams } from "next/navigation";
import TerraShell, { TerraPaneContent } from "../../../../../components/terra/TerraShell.js";
import { EmployeeAvatar } from "../../../../../components/v1/EmployeeAvatar.js";
import styles from "./EmployeeWorkstation.module.css";
import {
  TerraButton,
  TerraTag,
  TerraBackLink,
} from "../../../../../components/terra/TerraPrimitives.js";
import {
  DATA_COPY,
  TerraErrorState,
  TerraLoadingSkeleton,
} from "../../../../../components/terra/TerraState.js";
import {
  getCapabilitySelector,
  getDepartments,
  getEmployee,
  getEmployeeCapabilities,
  getEmployeeSkills,
  getEmployeeTools,
  getEmployeeTemplates,
} from "../../../../../lib/api.js";
import { roleLabel } from "../../../../../lib/theme.js";
import EmployeeEditDrawer from "./EmployeeEditDrawer.js";
import EmployeeConversation from "../../../../../components/v1/EmployeeConversation.js";
import { useRuntime } from "../../../../../components/runtime/RuntimeProvider.js";
import { businessReturnInput, validateBusinessReturn } from "../../../../../lib/businessReturnApi.js";
import { getOrganizationProjection } from "../../../../../lib/runtimeApi.js";
import { buildOrganizationProjection } from "../../../../../lib/organizationProjection.js";
import { businessCatalogHref } from "../../../../../components/v1/BusinessCatalogSurface.js";

export function employeeBusinessReturn(params, companyId, employee, organization) {
  if (!params.has("company_id") && !params.has("business_id")) return null;
  if (params.has("return_to") || params.has("return_kind") || params.getAll("company_id").length !== 1
      || params.getAll("business_id").length !== 1 || params.get("company_id") !== companyId
      || employee.company_id !== companyId || organization?.company?.company_id !== companyId) throw new Error("无法确认当前公司或原业务，请从业务入口重新进入。");
  const business = buildOrganizationProjection(organization).businessById.get(params.get("business_id"));
  if (!business?.assignments.some((assignment) => assignment.employeeRef === employee.id)) throw new Error("这位员工的当前责任不属于原业务，请重新核对。");
  return businessCatalogHref(companyId, { businessId: business.id });
}

export function employeeConversationReturn(query, verifiedQuery, status, employee, id, targets) {
  if (query !== verifiedQuery || status !== "ready" || !employee || employee.id !== id) return null;
  try {
    const input = businessReturnInput(new URLSearchParams(query), { allowConversation: true });
    const target = input && targets[input.kind];
    return target && target.href === input.value && target.company === employee.company_id
      ? { kind: input.kind, href: target.href, label: target.label } : null;
  } catch { return null; }
}

export function employeeCurrentDuties(companyId, employee, organization) {
  if (employee.company_id !== companyId || organization?.company?.company_id !== companyId) throw new Error("当前职责不属于当前公司。");
  return buildOrganizationProjection(organization).employees.find((item) => item.id === employee.id)?.assignments || [];
}

const STATUS = {
  idle: { label: "空闲", color: "grey" },
  assigned: { label: "已有工作安排", color: "cyan" },
  working: { label: "工作中", color: "cyan" },
  completed: { label: "已完成", color: "green" },
  error: { label: "异常", color: "red" },
  disabled: { label: "已暂停", color: "amber" },
};

const OFFICIAL_CG_AUTHOR_RESPONSIBILITY = "目标与合法账号上下文中的创作、事实与规格自检、Publishing交付准备与真实回执、Analytics口径与缺失事实复盘；自检不是独立审核";
const OFFICIAL_CG_AUTHOR_DISPLAY = "目标与合法账号上下文中的创作、事实与规格自检、发布交付准备与真实回执、数据分析口径与缺失事实复盘；自检不是独立审核";
const displayResponsibility = (value) => value === OFFICIAL_CG_AUTHOR_RESPONSIBILITY ? OFFICIAL_CG_AUTHOR_DISPLAY : value;

function selectorKey(item) {
  return `${item.source}:${item.capability_type}:${item.capability_id}`;
}

function bindingKey(item) {
  return `${item.capability_source}:${item.capability_type}:${item.capability_id}`;
}

function uniqueCapabilities(items = []) {
  const result = [];
  const seen = new Set();
  for (const item of items) {
    if (!item?.enabled || !["model", "tool", "connector", "agent"].includes(item.capability_type)) continue;
    const key = selectorKey(item);
    if (seen.has(key)) continue;
    seen.add(key);
    result.push(item);
  }
  return result;
}

export default function EmployeeDetailPage() {
  return <Suspense fallback={<TerraLoadingSkeleton />}><EmployeeDetailContent /></Suspense>;
}

function EmployeeDetailContent() {
  const runtime = useRuntime();
  const returnQuery = useSearchParams().toString();
  const [returnQueryVerified, setReturnQueryVerified] = useState("");
  const [writingReturn, setWritingReturn] = useState(null);
  const [cgReturn, setCgReturn] = useState(null);
  const [cgReturnNotice, setCgReturnNotice] = useState("");

  const [musicReturn, setMusicReturn] = useState(null);
  const [musicReturnNotice, setMusicReturnNotice] = useState("");

  const [returnNotice, setReturnNotice] = useState("");
  const params = useParams();
  const id = params?.id || "";
  const [conversationId, setConversationId] = useState(null);
  useEffect(() => {
    const target = new URLSearchParams(returnQuery).get("return_to") || "";
    setConversationId(target.startsWith("/ceo-office/conversation?conversation_id=")
      ? new URL(target, window.location.origin).searchParams.get("conversation_id") : null);
  }, [id, returnQuery]);
  const [employee, setEmployee] = useState(null);
  const [businessReturn, setBusinessReturn] = useState(null);
  const [currentDuties, setCurrentDuties] = useState(null);
  const loadSequence = useRef(0);
  useEffect(() => {
    let current = true;
    setReturnQueryVerified("");
    setCgReturn(null); setCgReturnNotice("");
    setMusicReturn(null); setMusicReturnNotice("");
    setWritingReturn(null); setReturnNotice("");
    let input;
    try {
      input = businessReturnInput(new URLSearchParams(returnQuery), { allowConversation: true });
    } catch {
      setReturnNotice("无法确认原工作台，请从业务入口重新进入。");
      return;
    }
    if (!input || runtime.status !== "ready" || !employee || employee.id !== id) return;
    const receivers = {
      cg: [setCgReturn, setCgReturnNotice, "原图文内容暂时无法确认，请从内容入口重新进入。"],
      music: [setMusicReturn, setMusicReturnNotice, "原歌曲内容暂时无法确认，请从歌曲入口重新进入。"],
      writing: [setWritingReturn, setReturnNotice, "暂时无法确认原章节，请从写作入口重新进入。"],
    };
    const [save, notice, message] = receivers[input.kind];
    validateBusinessReturn(input.kind, input.value, { employeeCompany: employee.company_id })
      .then((target) => { if (current) { save(target); setReturnQueryVerified(returnQuery); } })
      .catch(() => { if (current) notice(message); });
    return () => { current = false; };
  }, [runtime.status, runtime.companyId, employee, id, returnQuery]);
  const [departments, setDepartments] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [capabilities, setCapabilities] = useState([]);
  const [bindings, setBindings] = useState([]);
  const [executionPermission, setExecutionPermission] = useState(null);
  const [skills, setSkills] = useState([]);
  const [tools, setTools] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [detailRequest, setDetailRequest] = useState({ scope: "", serial: 0 });

  const load = useCallback(async () => {
    if (!id) return;
    const sequence = ++loadSequence.current;
    setEmployee(null); setBusinessReturn(null); setCurrentDuties(null);
    setLoading(true);
    setError("");
    try {
      const [employeeRow, departmentPayload, templatePayload, capabilityPayload, profilePayload, skillPayload, toolPayload] = await Promise.all([
        getEmployee(id),
        getDepartments(),
        getEmployeeTemplates(),
        getCapabilitySelector(),
        getEmployeeCapabilities(id),
        getEmployeeSkills(id),
        getEmployeeTools(id),
      ]);
      if (sequence !== loadSequence.current) return;
      if (!runtime.companyId || employeeRow.company_id !== runtime.companyId) throw new Error("员工不属于当前公司，请从当前业务重新进入。");
      const params = new URLSearchParams(returnQuery);
      try {
        const organization = await getOrganizationProjection(runtime.companyId);
        if (sequence !== loadSequence.current) return;
        setCurrentDuties(employeeCurrentDuties(runtime.companyId, employeeRow, organization));
        if (params.has("company_id") || params.has("business_id")) setBusinessReturn({ href: employeeBusinessReturn(params, runtime.companyId, employeeRow, organization), query: returnQuery });
      } catch (scopeError) {
        if (params.has("company_id") || params.has("business_id")) throw scopeError;
        if (sequence !== loadSequence.current) return;
        setCurrentDuties(null);
      }
      setEmployee(employeeRow);
      setDepartments(departmentPayload?.departments || []);
      setTemplates(templatePayload?.employee_templates || []);
      setCapabilities(uniqueCapabilities(capabilityPayload?.capabilities));
      setBindings(profilePayload?.bindings || []);
      setExecutionPermission(profilePayload?.execution_permission || null);
      setSkills(skillPayload?.bindings || []);
      setTools(toolPayload?.bindings || []);
      return true;
    } catch (err) {
      if (sequence !== loadSequence.current) return;
      setError(err?.message || "员工详情读取失败");
    } finally {
      if (sequence === loadSequence.current) setLoading(false);
    }
  }, [id, runtime.companyId, returnQuery]);

  useEffect(() => { load(); return () => { loadSequence.current += 1; }; }, [load]);

  const department = departments.find((item) => item.id === employee?.department_id);
  const template = templates.find((item) => item.id === employee?.template_id);
  const status = STATUS[employee?.status] || {
    label: "状态待确认",
    color: "grey",
  };
  const capabilityMap = useMemo(
    () => Object.fromEntries(capabilities.map((item) => [selectorKey(item), item])),
    [capabilities]
  );
  const profile = bindings.map((binding) => ({
    ...binding,
    selector: capabilityMap[bindingKey(binding)],
  }));

  if (loading) {
    return (
      <TerraShell topCrumb="组织中心 / AI 员工 / 员工详情">
        <TerraLoadingSkeleton variant="page" />
      </TerraShell>
    );
  }

  if (error || !employee || employee.company_id !== runtime.companyId) {
    return (
      <TerraShell topCrumb="组织中心 / AI 员工 / 员工详情">
        <TerraBackLink href="/ceo-office/organization/employees">返回 AI 员工</TerraBackLink>
        <TerraErrorState message={error || "员工不存在"} onRetry={load} />
      </TerraShell>
    );
  }

  const utilityTabId = JSON.stringify([employee.company_id, employee.id, "detail"]);
  const openDetail = () => {
    if (employee.id !== id || employee.company_id !== runtime.companyId) return;
    setDetailRequest((current) => ({ scope: utilityTabId, serial: current.scope === utilityTabId ? current.serial + 1 : 1 }));
  };
  const detail = <article className={styles.detail} aria-label="员工档案">
    <header><EmployeeAvatar employee={employee} className={styles.detailAvatar} /><h2>{employee.name}</h2><p>{roleLabel(employee.role) || template?.name || "岗位尚未提供"}</p><TerraTag color={status.color}>{status.label}</TerraTag></header>
    <section><h3>组织与当前责任</h3><p>所属部门：{department?.name || "直属公司"}</p>{currentDuties === null ? <p>当前职责资料暂不可读取</p> : currentDuties.length ? currentDuties.map((item, index) => <div key={index}><strong>{item.businessName || item.scopeName || "当前工作"} · {item.roleName}</strong><p>{displayResponsibility(item.responsibility) || "责任说明暂不可读取"}</p></div>) : <p>当前尚未安排工作职责</p>}<p className={styles.note}>工作安排不代表员工此刻正在执行；具体进展请查看当前工作。</p></section>
    <section><h3>工作能力</h3>{profile.length ? <ul>{profile.map((item) => <li key={item.id || bindingKey(item)}>{item.selector?.label || "已配置能力"} · {{ model: "模型", tool: "工具", connector: "连接", agent: "Agent" }[item.capability_type] || "能力"}{item.enabled === false || item.enabled === 0 ? " · 已停用" : ""}</li>)}</ul> : <p>尚未配置能力档案</p>}<p className={styles.note}>这里只展示已保存配置，实际可用性以当前会话为准。</p></section>
    <section><h3>技能与工具</h3>{skills.length ? <ul>{skills.map((item) => <li key={item.binding_id || item.skill_template_id}>{item.skill_name || "已分配技能"}</li>)}</ul> : <p>尚未分配技能</p>}{tools.length ? <ul>{tools.map((item) => <li key={item.id || item.capability_id}>{item.name || "已分配工具"}</li>)}</ul> : <p>尚未分配工具</p>}</section>
    <section><h3>档案与工作说明</h3><dl><dt>创建时间</dt><dd>{employee.created_at || DATA_COPY.noData}</dd><dt>员工模板</dt><dd>{template?.name || (employee.template_id || employee.created_from_template_id ? "模板详情暂不可读取" : "尚未关联模板")}</dd></dl>{template?.responsibility && <p>模板说明：{template.responsibility}</p>}{employee.instructions_override && <p>自定义工作说明：{employee.instructions_override}</p>}</section>
    <details><summary>查看技术详情</summary><p>员工标识：{employee.id}</p></details>
  </article>;
  return (
    <TerraShell topCrumb="组织中心 / 员工工作位" assistantContext={{ page: "employee", employee_id: id, company_id: employee.company_id }}>
      <TerraPaneContent utilityTabs={employee.id === id ? [{ id: utilityTabId, title: employee.name, content: detail }] : []} utilityLabel="员工档案" utilityRequestKey={detailRequest.scope === utilityTabId ? detailRequest.serial : 0} utilityRequestTabId={utilityTabId} />
      {businessReturn?.query === returnQuery && employee.company_id === runtime.companyId && <TerraBackLink href={businessReturn.href}>返回当前业务</TerraBackLink>}
      <div className={styles.page}>
        <nav className={styles.returns} aria-label="返回原工作">
          <TerraBackLink href="/ceo-office/organization/employees">返回 AI 员工</TerraBackLink>
          {cgReturn && returnQueryVerified === returnQuery && runtime.status === "ready" && cgReturn.company === employee?.company_id && employee?.id === id && <a className="mb-3 block text-sm font-semibold text-ui-primary" href={cgReturn.href}>{cgReturn.label}</a>}{cgReturnNotice && <p role="status" className="mb-3 text-sm">{cgReturnNotice}</p>}{musicReturn && returnQueryVerified === returnQuery && runtime.status === "ready" && musicReturn.company === employee?.company_id && employee?.id === id && <a className="mb-3 block text-sm font-semibold text-ui-primary" href={musicReturn.href}>{musicReturn.label}</a>}{musicReturnNotice && <p role="status" className="mb-3 text-sm">{musicReturnNotice}</p>}{writingReturn && returnQueryVerified === returnQuery && runtime.status === "ready" && writingReturn.company === employee?.company_id && employee?.id === id && <TerraBackLink href={writingReturn.href}>{writingReturn.label}</TerraBackLink>}
          {returnNotice && <p role="status">{returnNotice}</p>}
        </nav>
        <header className={styles.header}>
          <button type="button" className={styles.avatarButton} onClick={openDetail} aria-label={`打开${employee.name}的档案`}><EmployeeAvatar employee={employee} className={styles.avatar} /></button>
          <div className={styles.identity}><h1><button type="button" onClick={openDetail} aria-label={`打开${employee.name}的档案`}>{employee.name}</button></h1><div className={styles.metadata}>{(roleLabel(employee.role) || template?.name) !== employee.name && <span>{roleLabel(employee.role) || template?.name || "岗位尚未提供"}</span>}<span>{department?.name || "直属公司"}</span><TerraTag color={status.color}>{status.label}</TerraTag></div></div>
          <TerraButton icon="i-checklist" onClick={async () => { if (await load()) setDrawerOpen(true); }}>编辑员工</TerraButton>
        </header>
        {notice && <p role="status" className={styles.notice}>{notice}</p>}
        <section className={styles.duties} aria-labelledby="employee-duty-title"><h2 id="employee-duty-title">当前职责</h2>{currentDuties === null ? <p className={styles.note}>当前职责资料暂不可读取</p> : currentDuties.length ? <ul>{currentDuties.map((item, index) => <li key={index}><div><strong>{item.roleName}</strong><span>{item.businessName || item.scopeName || "当前工作"}</span></div><p>{displayResponsibility(item.responsibility) || "责任说明暂不可读取"}</p></li>)}</ul> : <p className={styles.note}>当前尚未安排工作职责</p>}<p className={styles.note}>{profile.length ? `已保存 ${profile.length} 项能力配置；实际可用性以当前会话为准。` : "尚未配置能力档案；当前可用模型请在会话中核对。"}</p></section>
        <div className={styles.conversation}><EmployeeConversation key={`${employee.company_id}:${employee.id}:${conversationId}`} companyId={employee.company_id} employee={employee} conversationId={conversationId} businessReturn={employeeConversationReturn(returnQuery, returnQueryVerified, runtime.status, employee, id, { cg: cgReturn, music: musicReturn, writing: writingReturn })} /></div>
        <a className={styles.businessEntry} href="/ceo-office/business">查看业务空间 →</a>
        <EmployeeEditDrawer
          open={drawerOpen}
          employee={employee}
          roleLabel={roleLabel(employee.role) || template?.name}
          capabilities={capabilities}
          bindings={bindings}
          executionPermission={executionPermission}
          onClose={(state) => {
            setDrawerOpen(false);
            if (state?.unknown) setNotice("保存结果尚未确认；再次编辑时将读取当前配置。");
          }}
          onSuccess={(saved, profilePayload, options) => {
            setEmployee(saved);
            setBindings(profilePayload?.bindings || []);
            setExecutionPermission(profilePayload?.execution_permission || null);
            setNotice(options?.readback ? "已读取当前员工配置，请核对授权与能力状态。" : "已更新员工「" + saved.name + "」");
            setDrawerOpen(false);
          }}
        />
      </div>
    </TerraShell>
  );
}
