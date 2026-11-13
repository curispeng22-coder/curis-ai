"use client";

import Link from "next/link";
import { roleLabel } from "../../../lib/theme.js";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import TerraShell, { TerraPaneContent } from "../../../components/terra/TerraShell.js";
import { useRuntime } from "../../../components/runtime/RuntimeProvider.js";
import {
  EMPLOYEE_AVATAR_PRESETS,
  EmployeeAvatar,
} from "../../../components/v1/EmployeeAvatar.js";
import { TerraIcon } from "../../../components/terra/TerraIcons.js";
import {
  TerraButton,
  TerraEmpty,
  TerraPageHead,
  TerraSearch,
  TerraTag,
} from "../../../components/terra/TerraPrimitives.js";
import {
  TerraErrorState,
  TerraLoadingSkeleton,
} from "../../../components/terra/TerraState.js";
import {
  assignSkill,
  unassignSkill,
  removeSkill,
  getSkillAssignments,
  getEmployeeAbilitySummary,
  getTalentMarketData,
  installSkill,
  previewSkillPackage,
  installSkillPackage,
  productStateFor,
  recruitExpert,
  resolveTalentReturnPath,
  uploadEmployeeAvatar,
} from "../../../lib/talentMarket.js";

const TABS = [
  { key: "experts", label: "专家", icon: "i-groups" },
  { key: "skills", label: "技能", icon: "i-auto_awesome" },
  { key: "connectors", label: "连接器", icon: "i-extension" },
];

export function RepositorySkillImport({ onInstalled }) {
  const [source, setSource] = useState({ repo_url: "" });
  const [preview, setPreview] = useState(null);
  const [accepted, setAccepted] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const current = useRef(0);
  useEffect(() => () => { current.current += 1; }, []);
  const change = (value) => { current.current += 1; setSource({ repo_url: value }); setPreview(null); setAccepted(false); setError(""); };
  const perform = async (install = false, choice = null) => {
    if (busy || (install && (!preview || preview.selection_required || !accepted))) return;
    const generation = ++current.current;
    setBusy(true); setError("");
    try {
      if (install) {
        const result = await installSkillPackage({ repo_url: preview.repo_url, commit: preview.commit,
          subdirectory: preview.subdirectory, expected_package_sha256: preview.package_sha256, license_accepted: true });
        if (generation === current.current) { setPreview(null); setAccepted(false); await onInstalled(result); }
      } else {
        const input = choice ? { repo_url: preview.repo_url, commit: preview.commit, subdirectory: choice.directory } : source;
        const result = await previewSkillPackage(input);
        if (generation === current.current) { setPreview(result); setAccepted(false); }
      }
    } catch (failure) { if (generation === current.current) setError(failure.message || "技能来源未能核对。输入已保留。"); }
    finally { if (generation === current.current) setBusy(false); }
  };
  return <section className="rounded-ui-md border border-ui-line p-4" aria-label="添加技能">
    <h3 className="font-semibold">添加技能</h3>
    <p className="my-3 text-ui-2 text-ui-txt-2">粘贴公开技能链接，自动识别来源、完整文件和运行条件。</p>
    <div className="grid gap-3">
      <label>技能链接<input aria-label="技能链接" disabled={busy} value={source.repo_url} onChange={(e) => change(e.target.value)} placeholder="https://github.com/…" className="block w-full rounded border border-ui-line bg-ui-surface p-2" /></label>
      <TerraButton disabled={busy || !source.repo_url} onClick={() => perform(false)}>{busy ? "正在核对…" : "识别技能"}</TerraButton>
      {preview?.selection_required && <section aria-label="选择技能"><p>此链接包含多个技能，请选择：</p>{preview.choices.map(choice => <TerraButton key={choice.directory} disabled={busy} onClick={() => perform(false, choice)}>{choice.name}</TerraButton>)}</section>}
      {preview && !preview.selection_required && <section aria-label="技能包核对"><h4>{preview.name || "已识别技能"}</h4><p>{preview.files.length} 个完整文件</p><p>{preview.dependency_status?.message}</p><details><summary>查看来源、许可和文件清单</summary><p className="break-all">{preview.repo_url} · {preview.commit} · {preview.package_sha256}</p><pre className="max-h-64 overflow-auto whitespace-pre-wrap">{preview.license_text}</pre><ul>{preview.files.map((file) => <li key={file.path}>{file.path} · {file.bytes} 字节</li>)}</ul></details><label><input type="checkbox" disabled={busy} checked={accepted} onChange={(e) => setAccepted(e.target.checked)} />同意此技能的来源和许可</label><TerraButton disabled={busy || !accepted} onClick={() => perform(true)}>安装技能</TerraButton></section>}
      {error && <p role="alert">{error}</p>}
    </div>
  </section>;
}

const SOURCE_LABEL = {
  official: "Curis 官方",
  tenant_private: "公司已有",
  marketplace: "公开资源",
  curis: "Curis 官方",
  external: "公开资源",
};

const PILOT_EXPERT_TITLES = {
  product_feedback_synth: "产品反馈分析专家",
  product_trend_researcher: "产品趋势研究专家",
  product_nudge_engine: "产品行为引导专家",
  marketing_growth_hacker: "营销增长实验专家",
  marketing_content_creator: "营销内容创作专家",
  marketing_social_strategist: "社交媒体策略专家",
  sales_pipeline_analyst: "销售机会分析专家",
  sales_discovery_coach: "销售需求访谈专家",
  support_responder: "客户支持专家",
  support_legal_compliance: "客服合规检查专家",
  finance_analyst: "财务分析专家",
  finance_tax_strategist: "税务策略专家",
};
const PILOT_EXPERT_NAMES = {
  product_feedback_synth: "Product Feedback Synthesizer",
  product_trend_researcher: "Product Trend Researcher",
  product_nudge_engine: "Product Behavioral Nudge Engineer",
  marketing_growth_hacker: "Marketing Growth Hacker",
  marketing_content_creator: "Marketing Content Creator",
  marketing_social_strategist: "Marketing Social Media Strategist",
  sales_pipeline_analyst: "Sales Pipeline Analyst",
  sales_discovery_coach: "Sales Discovery Coach",
  support_responder: "Support Responder",
  support_legal_compliance: "Support Legal Compliance Checker",
  finance_analyst: "Finance Financial Analyst",
  finance_tax_strategist: "Finance Tax Strategist",
};
const KNOWN_OFFICIAL_NAMES = {
  et_product_manager: ["Product Manager", "product_manager"],
  et_architect: ["Architect", "architect"],
  et_frontend_engineer: ["Frontend Engineer", "frontend_engineer"],
  et_backend_engineer: ["Backend Engineer", "backend_engineer"],
  et_qa_engineer: ["QA Engineer", "qa_engineer"],
};
const AGENCY_EXPERT_PATHS = {
  product_feedback_synth: "product/product-feedback-synth.md",
  product_trend_researcher: "product/product-trend-researcher.md",
  product_nudge_engine: "product/product-behavioral-nudge-engine.md",
  marketing_growth_hacker: "marketing/marketing-growth-hacker.md",
  marketing_content_creator: "marketing/marketing-content-creator.md",
  marketing_social_strategist: "marketing/marketing-social-media-strategist.md",
  sales_pipeline_analyst: "sales/sales-pipeline-analyst.md",
  sales_discovery_coach: "sales/sales-discovery-coach.md",
  support_responder: "support/support-support-responder.md",
  support_legal_compliance: "support/support-legal-compliance-checker.md",
  finance_analyst: "finance/finance-financial-analyst.md",
  finance_tax_strategist: "finance/finance-tax-strategist.md",
};
export function resourceTitle(item) {
  const raw = item?.display_name || item?.label || item?.name || "";
  if (item?.market_kind === "company_employee") return raw || (item?.role ? roleLabel(item.role) : "未命名资源");
  const knownOfficial = KNOWN_OFFICIAL_NAMES[item?.id];
  if (item?.market_kind === "curis_ready" && (item?.source === "official" || item?.source === "curis")
    && knownOfficial && item.role === knownOfficial[1] && item.name === knownOfficial[0]
    && raw === knownOfficial[0] && (!item.canonicalName || item.canonicalName === knownOfficial[0])) {
    return roleLabel(item.role);
  }
  const officialSeed = item?.source === "official" && (!raw || raw === item.role || raw === PILOT_EXPERT_NAMES[item.role]);
  const agencySource = item?.source === "external" && item?.market_kind === "external_candidate"
    && item?.source_url === "https://github.com/jnMetaCode/agency-agents-zh"
    && item?.source_path === AGENCY_EXPERT_PATHS[item.role] && raw === PILOT_EXPERT_NAMES[item.role]
    && item?.id?.startsWith(`resource:agent:${raw.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "")}:`);
  return PILOT_EXPERT_TITLES[item?.role] && (officialSeed || agencySource)
    ? PILOT_EXPERT_TITLES[item.role] : raw || (item?.role ? roleLabel(item.role) : "未命名资源");
}
function resourceDescription(item) {
  return String(item.responsibility || item.description || item.summary || "暂无说明")
    .replace(/financial modeling/gi, "财务建模")
    .replace(/tax planning/gi, "税务筹划")
    .replace(/content drafting/gi, "内容起草")
    .replace(/growth experiments/gi, "增长实验");
}

function firstLetter(value) {
  return String(value || "?").trim().slice(0, 1).toUpperCase();
}

export function skillDisplayName(item) {
  const label = item.display_name || item.label || item.name || "未命名资源";
  const repository = String(item.package?.repo_url || "").replace(/\/+$/, "").split("/").pop()?.replace(/\.git$/i, "");
  if (!repository) return label;
  return /^(skill|skills|未命名资源)$/i.test(label) || label.toLowerCase() === repository.toLowerCase()
    ? repository : repository + " · " + label;
}

export function SearchResultCard({ item, kind, selected, onSelect }) {
  const name = kind === "experts" ? resourceTitle(item) : kind === "skills" ? skillDisplayName(item) : item.display_name || item.label || item.name || "未命名资源";
  const description = kind === "experts" ? resourceDescription(item) : item.responsibility || item.description || item.summary || "暂无说明";
  const source = SOURCE_LABEL[item.source] || item.source || "来源未记录";
  const state = productStateFor(item, kind);
  return (
    <button
      type="button"
      onClick={() => onSelect({ kind, item })}
      className={`w-full rounded-ui-md border p-3 pb-4 text-left transition-colors hover:border-ui-primary focus-visible:outline focus-visible:outline-2 focus-visible:outline-ui-primary ${
        selected ? "border-ui-primary bg-ui-primary-light" : "border-ui-line bg-ui-surface"
      }`}
      aria-pressed={selected}
    >
      <div className="flex items-start gap-3">
        {item.market_kind === "company_employee" ? (
          <EmployeeAvatar employee={item} className="h-10 w-10 text-ui-3" />
        ) : (
          <span className="grid h-10 w-10 shrink-0 place-items-center rounded-full bg-ui-primary text-ui-primary-fg text-ui-3 font-bold">
            {firstLetter(name)}
          </span>
        )}
        <span className="min-w-0 flex-1">
          <span className="flex items-start justify-between gap-2">
            <span className="break-words font-semibold text-ui-3 leading-6 text-ui-txt">{name}</span>
            <TerraTag color={state === "可招聘" || state === "已加入公司" || state === "已安装" || state === "已连接" ? "green" : state === "连接异常" || state === "暂不可用" ? "red" : "amber"}>{state}</TerraTag>
          </span>
          <span className="mt-1.5 block text-ui-2 leading-5 text-ui-txt-2 line-clamp-2">{description}</span>
          <span className="mt-2 flex flex-wrap gap-1.5">
            <TerraTag color="grey">{source}</TerraTag>
            {item.market_kind === "external_candidate" && <TerraTag color="amber">尚未开放招聘</TerraTag>}
            {kind === "connectors" && item.mock_only && <TerraTag color="amber">暂不可用于真实业务</TerraTag>}
            {kind === "experts" && item.role && <TerraTag color="primary">{PILOT_EXPERT_TITLES[item.role] || roleLabel(item.role)}</TerraTag>}
            {item.market_kind === "company_employee" && <TerraTag color="grey">{item.department_name}</TerraTag>}
          </span>
        </span>
      </div>
    </button>
  );
}

export function Inspector({ selected, data, ability, onRecruit, onInstall, onAssign, onUnassign, onRemove, assignments, returnPath, busy }) {
  if (!selected) {
    return <TerraEmpty icon="i-search">选择一位专家、一项技能或一个连接，查看它能为公司做什么。</TerraEmpty>;
  }
  const { kind, item } = selected;
  const name = kind === "experts" ? resourceTitle(item) : kind === "skills" ? skillDisplayName(item) : item.display_name || item.label || item.name || "未命名资源";
  const source = SOURCE_LABEL[item.source] || item.source || "来源未记录";
  const installedSkill = kind === "skills" && item.source === "tenant_private";
  const employees = data.employees || [];
  const hasEmployees = employees.length > 0;
  const externalCandidate = kind === "experts" && item.market_kind === "external_candidate";
  const companyEmployee = kind === "experts" && item.market_kind === "company_employee";
  const state = productStateFor(item, kind);
  const installableSkill = kind === "skills" && state === "可安装";
  const capabilityCount = (ability?.capabilities || []).filter((binding) => binding.enabled).length;
  const employeeSkills = ability?.skills || [];

  return (
    <div className="space-y-4">
      <div className="flex items-start gap-3">
        {companyEmployee ? (
          <EmployeeAvatar employee={item} className="h-12 w-12 text-ui-4" />
        ) : (
          <span className="grid h-12 w-12 shrink-0 place-items-center rounded-full bg-ui-primary text-ui-primary-fg text-ui-4 font-bold">
            {firstLetter(name)}
          </span>
        )}
        <div className="min-w-0">
          <h2 className="text-ui-5 font-semibold text-ui-txt">{name}</h2>
          <p className="mt-1 text-ui-2 text-ui-txt-3">{item.role ? PILOT_EXPERT_TITLES[item.role] || roleLabel(item.role) : item.skill_type || item.connector_type || "公司资源"}</p>
        </div>
      </div>

      <div className="flex flex-wrap gap-1.5">
        <TerraTag color={state === "可招聘" || state === "已加入公司" || state === "已安装" || state === "已连接" ? "green" : state === "连接异常" || state === "暂不可用" ? "red" : "amber"}>{state}</TerraTag>
        <TerraTag color="grey">{source}</TerraTag>
      </div>

      <section className="border-t border-ui-line pt-4">
        <h3 className="font-semibold text-ui-3 text-ui-txt">能为公司做什么</h3>
        <p className="mt-2 text-ui-2 leading-relaxed text-ui-txt-2">
          {kind === "experts" ? resourceDescription(item) : item.responsibility || item.description || "该资源尚未提供更详细的能力说明。"}
        </p>
      </section>

      {!companyEmployee && (
        <details className="border-t border-ui-line pt-4 text-ui-1 text-ui-txt-3">
          <summary className="cursor-pointer font-semibold text-ui-txt-2">查看来源与使用条件</summary>
          <p className="mt-2 break-all">来源：{item.source_url || "Curis 官方"}</p>
          <p className="mt-1">许可：{item.license || item.license_spdx || "尚未记录"}</p>
          <p className="mt-1">安全检查：{item.security_status === "pass" ? "已完成基础检查" : "尚未完成完整检查"}</p>
        </details>
      )}

      {kind === "experts" && (
        <>
          {companyEmployee ? (
            <>
              <section className="border-t border-ui-line pt-4">
                <h3 className="font-semibold text-ui-3 text-ui-txt">当前归属</h3>
                <p className="mt-2 text-ui-2 text-ui-txt-2">{item.company_name} · {item.department_name}</p>
                <p className="mt-1 text-ui-1 text-ui-txt-3">岗位：{item.role ? roleLabel(item.role) : "尚未设置"}</p>
              </section>
              <section className="border-t border-ui-line pt-4">
                <h3 className="font-semibold text-ui-3 text-ui-txt">已具备的能力</h3>
                {!ability && <p className="mt-2 text-ui-1 text-ui-txt-3">正在读取员工能力…</p>}
                {ability && (
                  <>
                    <p className="mt-2 text-ui-2 text-ui-txt-2">已分配技能 {employeeSkills.length} 项 · 已绑定执行能力 {capabilityCount} 项</p>
                    {employeeSkills.length > 0 && <p className="mt-1 text-ui-1 text-ui-txt-3">技能：{employeeSkills.map((binding) => binding.skill_name).filter(Boolean).join("、")}</p>}
                    {!ability.complete && <p className="mt-1 text-ui-1 text-ui-amber">部分能力信息暂时无法读取，可到员工详情重试。</p>}
                    {!employeeSkills.length && !capabilityCount && <p className="mt-1 text-ui-1 text-ui-txt-3">尚未分配可用技能或执行能力。</p>}
                  </>
                )}
              </section>
              <Link href={`/ceo-office/organization/employees/${encodeURIComponent(item.id)}`} className="block rounded-ui-sm bg-ui-primary px-4 py-2.5 text-center text-ui-1 font-bold text-ui-primary-fg hover:opacity-90">
                查看员工详情
              </Link>
            </>
          ) : externalCandidate ? (
            <div className="rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3 text-ui-1 text-ui-txt-2">
              这位专家仍在完成来源、权限和实际工作验证，目前不会创建公司员工。
            </div>
          ) : (
            <>
              <section className="border-t border-ui-line pt-4">
                <h3 className="font-semibold text-ui-3 text-ui-txt">加入后的准备情况</h3>
                <p className="mt-2 text-ui-2 text-ui-txt-2">招聘后会带入岗位职责和默认技能；工具、连接和授权会继续按真实状态检查。</p>
              </section>
              <TerraButton onClick={onRecruit} disabled={busy} icon="i-add">
                {busy ? "正在准备…" : "招聘这位专家"}
              </TerraButton>
            </>
          )}
          {!companyEmployee && <Link href="/ceo-office/organization" className="block text-center text-ui-1 font-semibold text-ui-accent hover:underline">查看公司员工</Link>}
        </>
      )}

      {kind === "skills" && (
        <>
          <section className="border-t border-ui-line pt-4">
            <h3 className="font-semibold text-ui-3 text-ui-txt">适用员工与条件</h3>
            <p className="mt-2 text-ui-2 text-ui-txt-2">{item.package ? `完整文件包 · 固定版本 ${item.package.commit}` : "当前保存的是技能说明，未安装完整文件包。"}</p>
            <p className="mt-2 text-ui-2 text-ui-txt-2">可分配给公司中的 AI 员工。</p>
            <p className="mt-1 text-ui-1 text-ui-txt-3">{(item.default_capability_types || []).length ? "运行前还需要公司具备相应的 AI 执行能力。" : "当前没有记录额外的执行条件。"}</p>
          </section>
          <TerraButton
            onClick={onInstall}
            disabled={busy || installedSkill || !installableSkill}
            icon={installedSkill ? "i-check_circle" : "i-download"}
          >
            {installedSkill ? "已安装" : !installableSkill ? "当前不可安装" : busy ? "正在安装…" : "安装到公司"}
          </TerraButton>
          {installedSkill && <><p role="status">{item.dependency_status?.message || "仅保存技能资料，运行条件尚未核验。"}</p>
            {item.dependency_status?.preparation === "existing_browser_connection" && <Link href="/ceo-office/capabilities#employee-agents">准备现有浏览器连接与授权</Link>}
            <p className="text-ui-1 text-ui-txt-3">解绑或移除后，新工作不再使用该技能；已开始的任务请回原工作核对或停止，历史成果保留。</p>
            {assignments === null ? <p>正在核对使用员工…</p> : (assignments || []).map(employee => <div key={employee.id}>{employee.name}<TerraButton disabled={busy} onClick={() => onUnassign?.(employee.id)}>解除与{employee.name}的绑定</TerraButton></div>)}
            <TerraButton disabled={busy} onClick={onRemove}>从公司移除技能</TerraButton></>}
          {installedSkill && hasEmployees && (
            <div className="border-t border-ui-line pt-4">
              <label htmlFor="talent-skill-employee" className="mb-1.5 block text-ui-1 font-bold text-ui-txt-2">分配给员工</label>
              <select id="talent-skill-employee" className="w-full rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-ui-2 text-ui-txt" onChange={(event) => onAssign(event.target.value)} defaultValue="">
                <option value="">选择员工</option>
                {employees.map((employee) => <option key={employee.id} value={employee.id}>{employee.name} · {roleLabel(employee.role)}</option>)}
              </select>
            </div>
          )}
          {!hasEmployees && <p className="text-ui-1 text-ui-txt-3">招募员工后，这里可以直接分配技能。</p>}
        </>
      )}

      {kind === "connectors" && (
        <>
          <section className="border-t border-ui-line pt-4">
            <h3 className="font-semibold text-ui-3 text-ui-txt">连接状态</h3>
            <p className="mt-2 text-ui-2 text-ui-txt-2">{state === "已连接" ? "已经完成授权和可用性检查。" : state === "连接异常" ? "连接已保存，但当前无法正常使用。" : state === "待验证" ? "授权已存在，仍需重新检查是否可用。" : "当前尚未授权，不能用于真实业务。"}</p>
            {item.mock_only && <p className="mt-2 text-ui-1 text-ui-amber">当前版本只提供本地演示能力，不会连接或写入真实外部平台。</p>}
          </section>
          {state === "已连接" ? <p className="rounded-ui-sm bg-ui-green-soft px-3 py-2.5 text-ui-1 text-ui-green">连接可用；是否分配给员工或工作空间仍需单独确认。</p> : <p className="rounded-ui-sm bg-ui-surface-2 px-3 py-2.5 text-ui-1 text-ui-txt-2">当前尚未提供安全的授权入口。连接功能开放后，可从这里继续配置。</p>}
        </>
      )}

      {returnPath && <Link href={returnPath} className="block border-t border-ui-line pt-4 text-center text-ui-1 font-semibold text-ui-accent hover:underline">返回原来的工作位置</Link>}
    </div>
  );
}

export function RecruitPanel({ expert, data, onClose, onSuccess, open = true }) {
  const companies = data.companies || [];
  const [companyId, setCompanyId] = useState(companies[0]?.company_id || "");
  const [departmentId, setDepartmentId] = useState("");
  const [name, setName] = useState(expert.name || "");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [selectedPreset, setSelectedPreset] = useState("");
  const [avatarFile, setAvatarFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [createdEmployee, setCreatedEmployee] = useState(null);
  const panel = useRef(null), alive = useRef(true);
  useEffect(() => { alive.current = true; return () => { alive.current = false; }; }, []);
  useEffect(() => {
    if (!open) return;
    const origin = document.activeElement;
    panel.current?.querySelector("input")?.focus();
    return () => origin?.focus();
  }, [open]);
  useEffect(() => {
    if (!open) return;
    const closeOnEscape = (event) => { if (event.key === "Escape" && !busy) onClose(); };
    window.addEventListener("keydown", closeOnEscape);
    return () => window.removeEventListener("keydown", closeOnEscape);
  }, [open, busy, onClose]);
  const departments = useMemo(
    () => (data.departments || []).filter((item) => item.company_id === companyId && item.enabled),
    [data.departments, companyId]
  );

  useEffect(() => {
    setDepartmentId(departments[0]?.id || "");
  }, [departments]);

  useEffect(() => {
    if (!avatarFile) {
      setPreviewUrl("");
      return undefined;
    }
    const url = URL.createObjectURL(avatarFile);
    setPreviewUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [avatarFile]);

  function chooseAvatarFile(event) {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file) return;
    if (!["image/png", "image/jpeg", "image/webp"].includes(file.type)) {
      setError("请选择 PNG、JPEG 或 WebP 图片。原来的头像选择没有改变。");
      return;
    }
    if (file.size > 2 * 1024 * 1024) {
      setError("头像图片不能超过 2 MB。原来的头像选择没有改变。");
      return;
    }
    setError("");
    setSelectedPreset("");
    setAvatarFile(file);
  }

  function selectPreset(presetId) {
    setError("");
    setAvatarFile(null);
    setSelectedPreset(presetId);
  }

  function skipAvatar() {
    setError("");
    setAvatarFile(null);
    setSelectedPreset("");
  }

  async function submit(event) {
    event.preventDefault();
    if (!expert.recruitable) return;
    setError("");
    setBusy(true);
    try {
      const result = createdEmployee
        ? { employee: createdEmployee, tool_status: "not_required" }
        : await recruitExpert({
          company_id: companyId,
          department_id: departmentId || null,
          template_id: expert.id,
          name,
          avatar_ref: avatarFile ? "" : selectedPreset ? `preset:${selectedPreset}` : "",
        });
      let employee = result?.employee;
      if (!alive.current) return;
      if (avatarFile) {
        try {
          employee = await uploadEmployeeAvatar(employee.id, avatarFile);
          if (!alive.current) return;
        } catch (uploadError) {
          if (!alive.current) return;
          setCreatedEmployee(employee);
          setError(`员工已经加入公司，但头像上传失败：${uploadError?.message || "请重试"}。当前使用默认头像，你可以保留这张图片并再次提交。`);
          return;
        }
      }
      const needsCapability = result?.tool_status === "blocked_required_capability";
      onSuccess(`「${name || expert.name}」已加入公司并获得默认技能。${needsCapability ? "仍有工具尚未准备好，可先查看员工详情。" : ""}`, employee);
    } catch (err) {
      if (!alive.current) return;
      setError(err?.message || "招募失败，员工未创建");
    } finally {
      if (alive.current) setBusy(false);
    }
  }

  if (!open) return null;
  return (
    <div className="fixed inset-0 z-[80] flex justify-end bg-black/25" onClick={() => { if (!busy) onClose(); }}>
      <aside ref={panel} role="dialog" aria-modal="true" aria-label="招聘专家" className="h-full w-full max-w-[520px] overflow-y-auto border-l border-ui-line bg-ui-surface p-5 shadow-ui-3" onClick={(event) => event.stopPropagation()} onKeyDown={(event) => {
        if (event.key !== "Tab") return;
        const controls = [...panel.current.querySelectorAll('button:not(:disabled), input:not(:disabled), select:not(:disabled), a[href]')].filter((item) => item.getClientRects().length);
        const first = controls[0], last = controls.at(-1);
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
      }}>
        <div className="flex items-start justify-between gap-3">
          <div className="flex min-w-0 items-start gap-3"><EmployeeAvatar employee={{ name, avatar_ref: selectedPreset ? `preset:${selectedPreset}` : "" }} previewUrl={previewUrl} className="h-12 w-12 text-ui-4" /><div><p className="text-ui-1 font-bold text-ui-accent">招聘专家</p><h2 className="mt-1 text-ui-5 font-semibold text-ui-txt">{resourceTitle(expert)}</h2><p className="mt-1 text-ui-2 text-ui-txt-3">{expert.role ? PILOT_EXPERT_TITLES[expert.role] || roleLabel(expert.role) : "公司专家"} · 头像可选</p></div></div>
          <button type="button" disabled={busy} onClick={onClose} className="rounded-ui-sm p-1.5 hover:bg-ui-surface-2" aria-label="关闭招聘"><TerraIcon name="i-close" className="h-5 w-5 text-ui-txt-3" /></button>
        </div>
        <form className="mt-6 space-y-4" onSubmit={submit}>
          <section className="rounded-ui-sm bg-ui-surface-2 p-3"><h3 className="text-ui-1 font-bold text-ui-txt-2">主要职责</h3><p className="mt-1 text-ui-2 leading-relaxed text-ui-txt-2">{expert.responsibility || expert.description || "职责说明尚未补充。"}</p></section>
          <label className="block text-ui-1 font-bold text-ui-txt-2">员工姓名<input className="mt-1.5 w-full rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2.5 text-ui-2 text-ui-txt" value={name} onChange={(event) => setName(event.target.value)} required /></label>
          <label className="block text-ui-1 font-bold text-ui-txt-2">公司<select className="mt-1.5 w-full rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2.5 text-ui-2 text-ui-txt" value={companyId} onChange={(event) => setCompanyId(event.target.value)} required><option value="">选择公司</option>{companies.map((company) => <option key={company.company_id} value={company.company_id}>{company.name}</option>)}</select></label>
          <label className="block text-ui-1 font-bold text-ui-txt-2">部门（可选）<select className="mt-1.5 w-full rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2.5 text-ui-2 text-ui-txt" value={departmentId} onChange={(event) => setDepartmentId(event.target.value)}><option value="">暂不归属部门（后续归入或成立部门）</option>{departments.map((department) => <option key={department.id} value={department.id}>{department.name}</option>)}</select></label>
          <fieldset className="border-t border-ui-line pt-4">
            <legend className="text-ui-1 font-bold text-ui-txt-2">员工头像（可选）</legend>
            <p className="mt-1 text-ui-1 text-ui-txt-3">上传本地图片、选择 Curis 卡通头像，或跳过使用姓名首字。</p>
            <div className="mt-3 grid grid-cols-4 gap-2 sm:grid-cols-8">
              {EMPLOYEE_AVATAR_PRESETS.map((preset) => (
                <button
                  key={preset.id}
                  type="button"
                  aria-label={`选择${preset.label}头像`}
                  aria-pressed={selectedPreset === preset.id}
                  onClick={() => selectPreset(preset.id)}
                  className={`rounded-full p-0.5 ${selectedPreset === preset.id ? "ring-2 ring-ui-accent ring-offset-2 ring-offset-ui-surface" : "hover:ring-2 hover:ring-ui-line"}`}
                >
                  <EmployeeAvatar employee={{ name: preset.label, avatar_ref: `preset:${preset.id}` }} className="h-10 w-10" />
                </button>
              ))}
            </div>
            <div className="mt-3 flex flex-wrap items-center gap-2">
              <label className="cursor-pointer rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-ui-1 font-semibold text-ui-txt-2 hover:bg-ui-surface-2">
                <input type="file" accept="image/png,image/jpeg,image/webp" className="sr-only" onChange={chooseAvatarFile} />
                上传图片
              </label>
              <button type="button" onClick={skipAvatar} className="rounded-ui-sm px-3 py-2 text-ui-1 font-semibold text-ui-txt-3 hover:bg-ui-surface-2">暂不设置</button>
              {avatarFile && <span className="max-w-full truncate text-ui-1 text-ui-txt-3">已选择：{avatarFile.name}</span>}
              {!avatarFile && selectedPreset && <span className="text-ui-1 text-ui-txt-3">已选择：{EMPLOYEE_AVATAR_PRESETS.find((item) => item.id === selectedPreset)?.label}</span>}
            </div>
            <p className="mt-2 text-ui-1 text-ui-txt-3">支持 PNG、JPEG、WebP，最大 2 MB；图片保存在当前 Curis 本机数据中。</p>
          </fieldset>
          <div className="rounded-ui-sm bg-ui-surface-2 p-3 text-ui-1 text-ui-txt-2">确认后将创建真实公司员工并带入默认技能。尚未准备好的工具、连接或授权会继续显示为待处理，不会伪装成可用。</div>
          {error && <p className="text-ui-1 text-ui-red" role="alert">{error}</p>}
          {!companies.length && <TerraEmpty icon="i-warning">尚未建立公司，请先到组织中心完成公司设置。</TerraEmpty>}
          {!!companies.length && !departments.length && <p className="text-ui-1 text-ui-txt-3">当前公司尚无可用部门，员工将先以公司成员身份加入。</p>}
          <TerraButton type="submit" disabled={busy || !companyId}>{busy ? "正在加入公司…" : createdEmployee ? "重新上传头像并完成" : "确认加入公司"}</TerraButton>
        </form>
      </aside>
    </div>
  );
}

export function TalentMarketSurface({ companyId }) {
  const [data, setData] = useState(null);
  const [tab, setTab] = useState("experts");
  const [expertView, setExpertView] = useState("discover");
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("");
  const [selected, setSelected] = useState(null);
  const [ability, setAbility] = useState(null);
  const [assignments, setAssignments] = useState(null);
  const [returnPath, setReturnPath] = useState("");
  const [recruiting, setRecruiting] = useState(null);
  const [recruitOpen, setRecruitOpen] = useState(false);
  const [detailRequest, setDetailRequest] = useState(0);
  const alive = useRef(true), generation = useRef(0);
  useEffect(() => { alive.current = true; return () => { alive.current = false; generation.current += 1; }; }, []);
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    const ticket = ++generation.current;
    setError("");
    try {
      const next = await getTalentMarketData();
      if (!alive.current || ticket !== generation.current) return;
      const scoped = { ...next, companies: next.companies.filter((item) => item.company_id === companyId), departments: next.departments.filter((item) => item.company_id === companyId), employees: next.employees.filter((item) => item.company_id === companyId), companyEmployees: next.companyEmployees.filter((item) => item.company_id === companyId) };
      setData(scoped);
      return scoped;
    } catch (err) {
      if (!alive.current || ticket !== generation.current) return;
      setError(err?.message || "人才市场读取失败");
    }
  }, [companyId]);

  useEffect(() => { load(); }, [load]);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const params = new URLSearchParams(window.location.search);
    setReturnPath(resolveTalentReturnPath({
      returnTo: params.get("returnTo") || "",
      source: params.get("source") || "",
      origin: window.location.origin,
    }));
  }, []);

  useEffect(() => {
    let cancelled = false;
    if (selected?.kind !== "experts" || selected.item?.market_kind !== "company_employee") {
      setAbility(null);
      return undefined;
    }
    setAbility(null);
    getEmployeeAbilitySummary(selected.item.id).then((summary) => {
      if (!cancelled) setAbility(summary);
    });
    return () => { cancelled = true; };
  }, [selected]);

  useEffect(() => {
    let cancelled = false;
    setAssignments(null);
    if (selected?.kind === "skills" && selected.item?.source === "tenant_private" && data) {
      getSkillAssignments(data.employees, selected.item.skill_template_id).then(value => {
        if (!cancelled) setAssignments(value);
      }).catch(() => { if (!cancelled) setError("技能使用员工未能核对，请刷新后再操作。"); });
    }
    return () => { cancelled = true; };
  }, [selected, data, detailRequest]);

  const selectTab = useCallback((nextTab) => {
    setTab(nextTab);
    setQuery("");
    setCategory("");
    setSelected(null);
  }, []);

  const selectExpertView = useCallback((nextView) => {
    setExpertView(nextView);
    setQuery("");
    setCategory("");
    setSelected(null);
  }, []);

  const items = useMemo(() => {
    if (!data) return [];
    const source = tab === "experts"
      ? (expertView === "employees" ? data.companyEmployees : data.experts)
      : tab === "skills" ? data.skills : data.connectors;
    const term = query.trim().toLowerCase();
    const filtered = category ? source.filter((item) => item.category === category) : source;
    if (!term) return filtered;
    return filtered.filter((item) => [item.name, item.display_name, item.label, item.role, item.role ? roleLabel(item.role) : "", item.description, item.responsibility, item.connector_type, item.package?.repo_url, item.package?.subdirectory].some((value) => String(value || "").toLowerCase().includes(term)));
  }, [data, query, tab, category, expertView]);

  async function handleInstall() {
    if (busy || selected?.kind !== "skills" || productStateFor(selected.item, "skills") !== "可安装") return;
    setBusy(true);
    setError(""); setNotice("");
    try {
      const installed = await installSkill(selected.item.skill_template_id);
      if (!alive.current) return;
      setNotice(`技能「${installed.name}」已安装到公司。`);
      await load();
      setSelected({ kind: "skills", item: installed });
    } catch (err) {
      if (!alive.current) return;
      setError(err?.message || "技能纳入失败");
    } finally {
      if (alive.current) setBusy(false);
    }
  }

  async function handleAssign(employeeId) {
    if (busy || !data.employees.some((item) => item.id === employeeId) || !selected?.item?.skill_template_id) return;
    setBusy(true);
    setError(""); setNotice("");
    try {
      await assignSkill(employeeId, selected.item.skill_template_id);
      if (!alive.current) return;
      setNotice("技能已分配给员工；原有技能保持不变。运行前仍核对依赖与当前授权。");
      setDetailRequest(value => value + 1);
    } catch (err) {
      if (!alive.current) return;
      setError(err?.message || "技能分配失败");
    } finally {
      if (alive.current) setBusy(false);
    }
  }

  async function handleSkillRemoval(employeeId = null) {
    if (busy || selected?.kind !== "skills" || selected.item.source !== "tenant_private") return;
    setBusy(true); setError(""); setNotice("");
    try {
      if (employeeId) {
        await unassignSkill(employeeId, selected.item.skill_template_id);
        if (alive.current) { setNotice("已解除绑定，其他技能和历史成果保留。"); setDetailRequest(value => value + 1); }
      } else {
        await removeSkill(selected.item.skill_template_id, companyId);
        if (alive.current) { setSelected(null); await load(); setNotice("已从公司资源移除，历史成果和包凭据保留。"); }
      }
    } catch (failure) { if (alive.current) setError(failure.message || "操作未能确认，请刷新核对。"); }
    finally { if (alive.current) setBusy(false); }
  }

  const choose = (value) => { setSelected(value); setDetailRequest((current) => current + 1); };

  async function handleRepositoryInstalled(receipt) {
    const refreshed = await load();
    if (!alive.current || !refreshed) return;
    const id = receipt?.skill_template_id;
    const matches = id ? refreshed.skills.filter(item => item.skill_template_id === id
      && item.source === "tenant_private" && item.package) : [];
    if (matches.length !== 1) {
      setSelected(null);
      setNotice("");
      setError("安装请求已返回，但刷新列表中无法唯一核对该技能。请刷新核对，不要重复安装。");
      return;
    }
    const installed = matches[0];
    if (receipt.package?.package_sha256 && installed.package.package_sha256 !== receipt.package.package_sha256) {
      setSelected(null);
      setNotice("");
      setError("已安装技能的版本回读不一致，请刷新核对，不要重复安装。");
      return;
    }
    setTab("skills");
    setQuery("");
    setCategory("");
    choose({ kind: "skills", item: installed });
    setNotice("完整技能包已安装，请明确分配给需要的员工。执行仍需当前工作授权。");
  }

  const visibleSelection = selected && items.some((item) => (item.id || item.skill_template_id || item.name) === (selected.item.id || selected.item.skill_template_id || selected.item.name)) ? selected : null;
  const closeRecruit = useCallback(() => setRecruitOpen(false), []);
  const categoryCounts = data ? { experts: data.experts.length, skills: data.skills.length, connectors: data.connectors.length } : {};
  const context = useMemo(() => data ? <nav aria-label="能力目录" className="grid auto-rows-max content-start gap-1 text-ui-2">
    {TABS.map((item) => <button key={item.key} type="button" onClick={() => selectTab(item.key)}
      aria-current={tab === item.key ? "page" : undefined} className={`rounded-ui-sm px-3 py-2 text-left hover:bg-ui-surface-2 ${tab === item.key ? "bg-ui-primary-light font-semibold text-ui-primary" : "text-ui-txt-2"}`}>
      {item.label} · {item.key === "experts" ? data.experts.length : item.key === "skills" ? data.skills.length : data.connectors.length}
    </button>)}
    {tab === "experts" && <div className="mt-2 grid auto-rows-max content-start gap-1 border-t border-ui-line pt-2">
      <button type="button" onClick={() => selectExpertView("discover")} aria-current={expertView === "discover" ? "page" : undefined} className="rounded-ui-sm px-3 py-2 text-left text-ui-txt-2 hover:bg-ui-surface-2">可招聘与准备中</button>
      <button type="button" onClick={() => selectExpertView("employees")} aria-current={expertView === "employees" ? "page" : undefined} className="rounded-ui-sm px-3 py-2 text-left text-ui-txt-2 hover:bg-ui-surface-2">公司员工 · {data.companyEmployees.length}</button>
    </div>}
  </nav> : null, [data, tab, expertView, selectTab, selectExpertView]);
  if (!data && !error) return <TerraShell topCrumb="人才与能力"><TerraLoadingSkeleton variant="page" /></TerraShell>;
  if (error && !data) return <TerraShell topCrumb="人才与能力"><TerraErrorState message="无法加载人才与能力" onRetry={load} /></TerraShell>;

  return <TerraShell topCrumb="人才与能力" assistantContext={{ page: "talent", companyId }}>
    <TerraPageHead title="人才与能力" subtitle="发现适合的专家，为公司补充技能和连接能力。" actions={<Link href="/ceo-office/organization" className="inline-flex h-9 items-center rounded-ui-sm border border-ui-line px-4 text-ui-2 font-semibold text-ui-txt">查看岗位与责任</Link>} />
    {tab === "skills" && <RepositorySkillImport onInstalled={handleRepositoryInstalled} />}
    {returnPath && <div className="mb-4 flex flex-wrap items-center justify-between gap-3 border-b border-ui-line pb-3 text-ui-2 text-ui-txt-2"><span>为原来的工作补充能力</span><Link href={returnPath} className="font-semibold text-ui-primary hover:underline">返回原来的工作位置</Link></div>}
    {(notice || error) && <div className={`mb-4 rounded-ui-sm px-4 py-3 text-ui-2 ${error ? "bg-ui-red-soft text-ui-red" : "bg-ui-green-soft text-ui-green"}`} role={error ? "alert" : "status"}>{error || notice}{notice && returnPath && <Link href={returnPath} className="ml-3 font-semibold underline">返回继续工作</Link>}</div>}
    <TerraPaneContent contextPane={context} contextLabel="能力目录" initialContextOpen utilityRequestTabId="current" utilityLabel="能力详情" utilityRequestKey={detailRequest} utilityPane={visibleSelection ? <div className="p-5"><Inspector assignments={assignments} onUnassign={handleSkillRemoval} onRemove={() => handleSkillRemoval()} selected={visibleSelection} data={data} ability={ability} onRecruit={() => { setRecruiting(visibleSelection.item); setRecruitOpen(true); }} onInstall={handleInstall} onAssign={handleAssign} returnPath={returnPath} busy={busy} /></div> : null} />
    <nav aria-label="能力类型" className="mb-5 flex flex-wrap border-b border-ui-line">{TABS.map((item) => <button key={item.key} type="button" onClick={() => selectTab(item.key)} aria-pressed={tab === item.key} className={`flex min-w-[120px] flex-1 items-center justify-center gap-2 border-b-2 px-4 py-4 text-ui-3 font-semibold focus-visible:outline focus-visible:outline-2 focus-visible:outline-ui-primary ${tab === item.key ? "border-ui-primary text-ui-primary" : "border-transparent text-ui-txt-2 hover:bg-ui-surface-2"}`}><TerraIcon name={item.icon} className="h-5 w-5" />{item.label}<span className="text-ui-1 text-ui-txt-3">{categoryCounts[item.key]}</span></button>)}</nav>
    <section aria-label={`${TABS.find((item) => item.key === tab)?.label}集合`}>
      {tab === "experts" && <div className="mb-4 flex flex-wrap items-center gap-3"><button type="button" onClick={() => selectExpertView("discover")} aria-pressed={expertView === "discover"} className={`rounded-ui-sm px-3 py-2 text-ui-2 font-semibold ${expertView === "discover" ? "bg-ui-primary-light text-ui-primary" : "text-ui-txt-2"}`}>可招聘与准备中</button><button type="button" onClick={() => selectExpertView("employees")} aria-pressed={expertView === "employees"} className={`rounded-ui-sm px-3 py-2 text-ui-2 font-semibold ${expertView === "employees" ? "bg-ui-primary-light text-ui-primary" : "text-ui-txt-2"}`}>公司员工 · {data.companyEmployees.length}</button></div>}
      <div className="mb-5 flex flex-wrap items-center gap-3"><TerraSearch ariaLabel={`搜索${TABS.find((item) => item.key === tab)?.label}或能力关键词`} placeholder={`搜索${TABS.find((item) => item.key === tab)?.label}或能力关键词…`} value={query} onChange={(value) => { setQuery(value); setSelected(null); }} className="min-w-[200px] flex-1" />{tab === "experts" && expertView === "discover" && <select aria-label="专业领域" value={category} onChange={(event) => { setCategory(event.target.value); setSelected(null); }} className="h-9 rounded-ui-sm border border-ui-line bg-ui-surface px-3 text-ui-2 text-ui-txt"><option value="">全部领域</option>{data.expertCategories.map((item) => <option key={item} value={item}>{item}</option>)}</select>}<span className="text-ui-1 text-ui-txt-3">{items.length} 项{tab === "skills" ? ` · ${data.skills.filter((item) => item.source === "tenant_private").length} 项已安装` : ""}</span></div>
      {items.length ? <div className="grid max-w-[1240px] auto-rows-max grid-cols-[repeat(auto-fill,minmax(min(100%,300px),1fr))] items-stretch gap-4">{items.map((item) => <SearchResultCard key={item.id || item.skill_template_id || item.name} item={item} kind={tab} selected={visibleSelection?.item === item} onSelect={choose} />)}</div> : <div className="border-t border-ui-line py-12"><TerraEmpty icon="i-search">{query || category ? "没有匹配的能力，调整搜索或筛选后再试。" : tab === "experts" && expertView === "employees" ? "公司还没有员工。可以从可招聘专家开始。" : tab === "connectors" ? "当前没有可连接的外部服务。" : "当前没有可用的技能。"}</TerraEmpty></div>}
    </section>
    {recruiting && <RecruitPanel key={recruiting.id} open={recruitOpen} expert={recruiting} data={data} onClose={closeRecruit} onSuccess={async (message, employee) => { if (!alive.current) return; setRecruitOpen(false); setRecruiting(null); setNotice(message); setExpertView("employees"); const next = await load(); if (!alive.current) return; const created = next?.companyEmployees.find((item) => item.id === employee?.id); if (created) choose({ kind: "experts", item: created }); }} />}
  </TerraShell>;
}

export default function TalentMarketPage() {
  const runtime = useRuntime();
  return <TalentMarketSurface key={runtime.companyId || "no-company"} companyId={runtime.companyId || ""} />;
}
