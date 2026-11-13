"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import TerraShell from "../../../../components/terra/TerraShell.js";
import {
  TerraButton,
  TerraInput,
  TerraPageHead,
} from "../../../../components/terra/TerraPrimitives.js";
import { RuntimeEmpty, RuntimeError, RuntimeLoading } from "../../../../components/runtime/RuntimeStates.js";
import { useRuntime } from "../../../../components/runtime/RuntimeProvider.js";
import { CEO_ID } from "../../../../lib/api.js";
import {
  createRuntimeWorkspace,
  getCanonicalBusinesses,
  runtimeErrorMessage,
  workspaceOfficeHref,
} from "../../../../lib/runtimeApi.js";

const STUDIO_LIFECYCLE = [
  ["Discover", "分析业务", true],
  ["Blueprint", "定义结构", true],
  ["Compose", "组装阶段", true],
  ["Bind", "绑定能力", true],
  ["Staff", "安排岗位", true],
  ["Simulate", "运行验证", false],
  ["Approve", "CEO 批准", false],
  ["Operate", "开始经营", false],
];

const TEMPLATES = {
  RD: {
    label: "研发工作台",
    description: "以 Cycle、八阶段、工程证据和 CEO 验收交付软件结果。",
    stages: ["INTAKE", "DESIGN", "IMPLEMENT", "VERIFY", "ACCEPT", "REVIEW", "IMPROVE", "ARCHIVE"],
    stageLabels: ["受理", "设计", "实现", "验证", "验收", "复盘", "改进", "归档"],
    stageOwners: ["CEO Assistant", "Product AI", "Engineering AI", "QA AI", "CEO", "CEO Assistant", "Engineering AI", "CEO Assistant"],
    roleSlots: [
      { role: "Product AI", responsibility: "把经营意图转成可验证的设计与验收边界", capability: "知识与规范 · 证据归档", capabilityRefs: ["requirement:knowledge-context", "requirement:evidence-archive"] },
      { role: "Engineering AI", responsibility: "实现被批准的变更并提交可追溯证据", capability: "代码仓库 · 测试运行器", capabilityRefs: ["requirement:code-repository", "requirement:test-runner"] },
      { role: "QA AI", responsibility: "验证正常、失败和恢复路径，不替 CEO 验收", capability: "测试运行器 · 证据归档", capabilityRefs: ["requirement:test-runner", "requirement:evidence-archive"] },
    ],
    capabilities: [
      { capabilityRef: "requirement:code-repository", capability: "代码仓库" },
      { capabilityRef: "requirement:test-runner", capability: "测试运行器" },
      { capabilityRef: "requirement:knowledge-context", capability: "知识与规范" },
      { capabilityRef: "requirement:evidence-archive", capability: "证据归档" },
    ],
    simulationScenarios: ["正常交付", "工程 AI 缺席", "测试失败", "证据冲突", "CEO 退回"],
    externalResultSource: "CODE_AND_TEST_EVIDENCE_OR_CEO_MANUAL",
  },
  XHS: {
    label: "小红书运营工作台",
    description: "以内容版本、发布回执、互动反馈与 CEO 审核经营小红书业务。",
    stages: ["INTAKE", "PRODUCE", "DELIVER", "COLLECT", "ACCEPT", "REVIEW", "IMPROVE", "ARCHIVE"],
    stageLabels: ["受理", "生产", "发布", "回收", "验收", "复盘", "改进", "归档"],
    stageOwners: ["CEO Assistant", "内容 AI", "发布执行 AI", "互动回收 AI", "CEO", "数据复盘 AI", "策略 AI", "CEO Assistant"],
    roleSlots: [
      { role: "策略 AI", responsibility: "基于有来源的信号提出内容方向", capability: "内容知识 · 互动与结果回流", capabilityRefs: ["requirement:content-knowledge", "requirement:result-feedback"] },
      { role: "内容 AI", responsibility: "形成可审阅的平台版本，不承诺外部结果", capability: "内容知识 · 平台连接器", capabilityRefs: ["requirement:content-knowledge", "requirement:platform-connector"] },
      { role: "数据复盘 AI", responsibility: "关联发布回执与互动证据形成下一轮建议", capability: "发布回执 · 互动与结果回流", capabilityRefs: ["requirement:publication-receipt", "requirement:result-feedback"] },
    ],
    capabilities: [
      { capabilityRef: "requirement:platform-connector", capability: "平台连接器" },
      { capabilityRef: "requirement:content-knowledge", capability: "内容知识" },
      { capabilityRef: "requirement:publication-receipt", capability: "发布回执" },
      { capabilityRef: "requirement:result-feedback", capability: "互动与结果回流" },
    ],
    simulationScenarios: ["正常发布", "账号未授权", "平台适配失败", "互动风险", "结果延迟", "CEO 退回"],
    externalResultSource: "PLATFORM_API_OR_CEO_MANUAL",
  },
  TTK: {
    label: "抖音 / TikTok 工作台",
    description: "以短视频版本、发布回执、互动反馈与 CEO 审核经营视频内容。",
    stages: ["INTAKE", "PRODUCE", "DELIVER", "COLLECT", "ACCEPT", "REVIEW", "IMPROVE", "ARCHIVE"],
    stageLabels: ["受理", "生产", "发布", "回收", "验收", "复盘", "改进", "归档"],
    stageOwners: ["CEO Assistant", "内容 AI", "发布执行 AI", "互动回收 AI", "CEO", "数据复盘 AI", "策略 AI", "CEO Assistant"],
    roleSlots: [
      { role: "策略 AI", responsibility: "从有来源的趋势形成短视频方向", capability: "脚本与素材知识 · 互动与结果回流", capabilityRefs: ["requirement:video-knowledge", "requirement:result-feedback"] },
      { role: "内容 AI", responsibility: "形成可审阅的脚本与视频版本", capability: "脚本与素材知识 · 平台连接器", capabilityRefs: ["requirement:video-knowledge", "requirement:platform-connector"] },
      { role: "数据复盘 AI", responsibility: "关联回执、互动和结果形成改进建议", capability: "发布回执 · 互动与结果回流", capabilityRefs: ["requirement:publication-receipt", "requirement:result-feedback"] },
    ],
    capabilities: [
      { capabilityRef: "requirement:platform-connector", capability: "平台连接器" },
      { capabilityRef: "requirement:video-knowledge", capability: "脚本与素材知识" },
      { capabilityRef: "requirement:publication-receipt", capability: "发布回执" },
      { capabilityRef: "requirement:result-feedback", capability: "互动与结果回流" },
    ],
    simulationScenarios: ["正常发布", "账号未授权", "素材适配失败", "互动风险", "结果延迟", "CEO 退回"],
    externalResultSource: "PLATFORM_API_OR_CEO_MANUAL",
  },
};

function blueprintFor(type, outcome, acceptanceRule, fallbackPath) {
  const template = TEMPLATES[type];
  return {
    schemaVersion: "workspace-blueprint-draft-v1",
    studioLifecycle: "STAFF_READY",
    lifecycleMode: "STUDIO_DRAFT",
    businessType: type,
    stages: template.stages,
    stageContracts: template.stages.map((stage, index) => ({
      stage,
      label: template.stageLabels[index],
      ownerRole: template.stageOwners[index],
      input: index === 0 ? "CEO_BUSINESS_INTENT" : `${template.stages[index - 1]}_OUTPUT`,
      output: `${stage}_OUTPUT`,
      evidenceRule: index === 4 ? acceptanceRule : "PERSISTED_RUNTIME_EVIDENCE_REQUIRED",
      failureExit: "ESCALATE_TO_CEO_ASSISTANT",
    })),
    outcomeRef: outcome,
    intentRef: outcome,
    ownerRole: "CEO Assistant",
    roleSlots: template.roleSlots.map((slot) => ({ ...slot, staffingStatus: "PLANNED_NOT_MATERIALIZED" })),
    capabilityBindings: template.capabilities.map((capability) => ({ ...capability, bindingStatus: "REQUIRED_NOT_AUTHORIZED" })),
    evidenceRule: {
      acceptance: acceptanceRule,
      approver: "CEO",
      externalResultSource: template.externalResultSource,
      missingEvidence: "BLOCK_AND_ESCALATE",
    },
    failurePolicy: {
      manualFallback: fallbackPath,
      owner: "CEO Assistant",
      silentSuccessForbidden: true,
    },
    simulationScenarios: template.simulationScenarios,
    approvalGate: "CEO_EXPLICIT_APPROVAL_REQUIRED",
    platform: type === "RD" ? undefined : type,
  };
}

function StudioField({ id, label, value, onChange, placeholder, rows = 3 }) {
  return (
    <div>
      <label htmlFor={id} className="mb-1.5 block text-ui-1 font-bold text-ui-txt-2">{label}</label>
      <textarea
        id={id}
        rows={rows}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="w-full resize-none rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-ui-2 leading-relaxed text-ui-txt outline-none focus:ring-2 focus:ring-ui-accent"
        required
      />
    </div>
  );
}

export default function WorkspaceStudioPage() {
  const runtime = useRuntime();
  const [type, setType] = useState("RD");
  const [name, setName] = useState("");
  const [outcome, setOutcome] = useState("");
  const [acceptanceRule, setAcceptanceRule] = useState("");
  const [fallbackPath, setFallbackPath] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [businesses, setBusinesses] = useState([]);
  const [businessId, setBusinessId] = useState("");
  useEffect(() => {
    if (!runtime.companyId) return;
    let active = true;
    getCanonicalBusinesses(runtime.companyId).then((payload) => {
      if (!active) return;
      const items = payload.businesses || [];
      setBusinesses(items);
      const requested = new URLSearchParams(window.location.search).get("business_id");
      setBusinessId(items.find((item) => item.business_id === requested)?.business_id || "");
    }).catch(() => { if (active) setError("暂时无法读取所属业务，请稍后重试。"); });
    return () => { active = false; };
  }, [runtime.companyId]);

  if (runtime.status === "idle" || runtime.status === "loading") {
    return <TerraShell topCrumb="工作空间 / Workspace Studio"><RuntimeLoading label="正在准备 Workspace Studio…" /></TerraShell>;
  }
  if (runtime.status === "error" || runtime.status === "forbidden") {
    return <TerraShell topCrumb="工作空间 / Workspace Studio"><RuntimeError message={runtime.error} onRetry={runtime.refresh} forbidden={runtime.status === "forbidden"} /></TerraShell>;
  }
  if (!runtime.snapshot?.company) {
    return (
      <TerraShell topCrumb="工作空间 / Workspace Studio">
        <RuntimeEmpty
          title="先建立公司，再装修业务空间"
          description="Studio 只能为真实 Company 保存 Workspace Blueprint Draft。请先完成 CEO 创办引导。"
          action={<Link href="/onboarding" className="font-bold text-ui-primary">开始创办公司</Link>}
        />
      </TerraShell>
    );
  }

  const template = TEMPLATES[type];
  const readiness = [
    ["所属业务", businesses.some((item) => item.business_id === businessId)],
    ["办公室名称", Boolean(name.trim())],
    ["目标结果", Boolean(outcome.trim())],
    ["验收证据", Boolean(acceptanceRule.trim())],
    ["失败与人工备用路径", Boolean(fallbackPath.trim())],
    ["岗位责任", template.roleSlots.length > 0],
    ["能力供给", template.capabilities.length > 0],
  ];
  const readyCount = readiness.filter(([, ready]) => ready).length;
  const canSave = readyCount === readiness.length && !saving;

  async function handleSubmit(event) {
    event.preventDefault();
    if (!canSave) {
      setError("请先补齐配置检查中的缺项，再保存 Blueprint Draft。");
      return;
    }
    setSaving(true);
    setError("");
    try {
      const result = await createRuntimeWorkspace(runtime.companyId, {
        ceo_id: CEO_ID,
        business_ref: businessId,
        business_type: type,
        name: name.trim(),
        blueprint_version: "v1",
        blueprint: blueprintFor(type, outcome.trim(), acceptanceRule.trim(), fallbackPath.trim()),
      });
      window.location.href = workspaceOfficeHref(result.workspace || result);
    } catch (requestError) {
      setSaving(false);
      setError(requestError?.message || runtimeErrorMessage(requestError));
    }
  }

  const clearError = () => setError("");

  return (
    <TerraShell topCrumb="工作空间 / Workspace Studio">
      <TerraPageHead
        title="Workspace Studio"
        subtitle={`${runtime.snapshot.company.name} · 装修模式只保存 Blueprint Draft；未模拟、未批准，不影响经营中的 Workspace。`}
        pill="Studio / 装修模式"
      />

      <ol aria-label="Workspace Studio 生命周期" className="mb-5 flex gap-1 overflow-x-auto rounded-ui-md border border-ui-line bg-ui-surface p-2">
        {STUDIO_LIFECYCLE.map(([stage, label, inDraft], index) => (
          <li key={stage} className={`min-w-[112px] flex-1 rounded-ui-sm px-3 py-2 ${inDraft ? "bg-ui-surface-2" : "opacity-55"}`}>
            <span className="block text-ui-0 font-bold text-ui-txt-3">{index + 1}</span>
            <strong className="block text-ui-1 text-ui-txt">{stage}</strong>
            <span className="text-ui-0 text-ui-txt-3">{inDraft ? label : `${label} · 后续门禁`}</span>
          </li>
        ))}
      </ol>

      <form onSubmit={handleSubmit} className="grid gap-4 xl:grid-cols-[minmax(240px,0.85fr)_minmax(420px,1.65fr)_minmax(260px,0.9fr)]">
        <section aria-labelledby="studio-structure-title" className="rounded-ui-md border border-ui-line bg-ui-surface p-4">
          <div className="mb-4">
            <h2 id="studio-structure-title" className="text-ui-4 font-semibold text-ui-txt">业务结构</h2>
            <p className="mt-1 text-ui-1 leading-relaxed text-ui-txt-3">先定义结果与边界，再选择 AI 和能力。</p>
          </div>

          <fieldset>
            <label className="mb-4 block">所属业务
              <select aria-label="所属业务" className="mt-2 block w-full border border-ui-line bg-ui-surface p-2" value={businessId} onChange={(event) => setBusinessId(event.target.value)} required>
                <option value="">请选择已有业务</option>
                {businesses.map((business) => <option key={business.business_id} value={business.business_id}>{business.name}</option>)}
              </select>
            </label>
            <legend className="mb-2 text-ui-1 font-bold text-ui-txt-2">业务空间模板</legend>
            <div className="grid gap-2">
              {Object.entries(TEMPLATES).map(([key, item]) => (
                <button
                  key={key}
                  type="button"
                  aria-pressed={key === type}
                  onClick={() => { setType(key); clearError(); }}
                  className={`rounded-ui-sm border p-3 text-left transition-colors ${key === type ? "border-ui-primary bg-ui-primary-soft" : "border-ui-line bg-ui-surface hover:bg-ui-surface-2"}`}
                >
                  <strong className="block text-ui-2 text-ui-txt">{item.label}</strong>
                  <span className="mt-1 block text-ui-1 leading-relaxed text-ui-txt-3">{item.description}</span>
                </button>
              ))}
            </div>
          </fieldset>

          <div className="mt-4 grid gap-4 border-t border-ui-line pt-4">
            <TerraInput
              label="办公室名称"
              placeholder={`例如：${template.label}`}
              value={name}
              onChange={(event) => { setName(event.target.value); clearError(); }}
              required
            />
            <StudioField
              id="studio-outcome"
              label="目标结果"
              value={outcome}
              onChange={(event) => { setOutcome(event.target.value); clearError(); }}
              placeholder="这间办公室要持续交付什么外部或经营结果？"
            />
            <StudioField
              id="studio-acceptance"
              label="CEO 验收证据"
              value={acceptanceRule}
              onChange={(event) => { setAcceptanceRule(event.target.value); clearError(); }}
              placeholder="什么真实证据出现后，CEO 才能判断结果成立？"
            />
            <StudioField
              id="studio-fallback"
              label="失败与人工备用路径"
              value={fallbackPath}
              onChange={(event) => { setFallbackPath(event.target.value); clearError(); }}
              placeholder="AI、工具或平台不可用时，由谁接手并如何安全退出？"
            />
          </div>
        </section>

        <section aria-labelledby="studio-canvas-title" className="rounded-ui-md border border-ui-line bg-ui-surface p-4">
          <div className="flex flex-wrap items-start justify-between gap-3 border-b border-ui-line pb-4">
            <div>
              <h2 id="studio-canvas-title" className="text-ui-4 font-semibold text-ui-txt">Blueprint Canvas</h2>
              <p className="mt-1 text-ui-1 text-ui-txt-3">Draft v1 · {template.label} · Owner：CEO Assistant</p>
            </div>
            <span className="rounded-full bg-ui-surface-2 px-3 py-1 text-ui-0 font-bold text-ui-txt-2">未模拟 · 未批准</span>
          </div>

          <div className="py-4">
            <p className="text-ui-0 font-bold text-ui-txt-3">目标结果</p>
            <p className="mt-1 max-w-[70ch] text-ui-2 leading-relaxed text-ui-txt">{outcome.trim() || "等待 CEO 定义目标结果"}</p>
          </div>

          <ol className="grid gap-2 sm:grid-cols-2 lg:grid-cols-4" aria-label="业务阶段与责任">
            {template.stages.map((stage, index) => (
              <li key={stage} className="rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3">
                <span className="text-ui-0 font-bold text-ui-txt-3">{index + 1} · {stage}</span>
                <strong className="mt-1 block text-ui-2 text-ui-txt">{template.stageLabels[index]}</strong>
                <span className="mt-2 block text-ui-0 leading-relaxed text-ui-txt-3">Owner · {template.stageOwners[index]}</span>
              </li>
            ))}
          </ol>

          <div className="mt-5 border-t border-ui-line pt-4">
            <div className="flex items-baseline justify-between gap-3">
              <h3 className="text-ui-3 font-semibold text-ui-txt">AI 岗位与汇报责任</h3>
              <span className="text-ui-0 text-ui-txt-3">Blueprint 计划，尚未物化</span>
            </div>
            <div className="mt-3 divide-y divide-ui-line rounded-ui-sm border border-ui-line">
              {template.roleSlots.map((slot) => (
                <article key={slot.role} className="grid gap-2 p-3 sm:grid-cols-[140px_1fr_150px] sm:items-start">
                  <div>
                    <strong className="block text-ui-2 text-ui-txt">{slot.role}</strong>
                    <span className="text-ui-0 text-ui-txt-3">向 CEO Assistant 汇报</span>
                  </div>
                  <p className="text-ui-1 leading-relaxed text-ui-txt-2">{slot.responsibility}</p>
                  <p className="text-ui-0 leading-relaxed text-ui-txt-3">能力 · {slot.capability}</p>
                </article>
              ))}
            </div>
          </div>

          <div className="mt-5 border-t border-ui-line pt-4">
            <h3 className="text-ui-3 font-semibold text-ui-txt">Simulation 场景草案</h3>
            <div className="mt-3 flex flex-wrap gap-2">
              {template.simulationScenarios.map((scenario) => (
                <span key={scenario} className="rounded-full border border-ui-line px-2.5 py-1 text-ui-0 text-ui-txt-2">{scenario}</span>
              ))}
            </div>
            <p className="mt-3 text-ui-1 leading-relaxed text-ui-txt-3">这些场景只随 Blueprint 保存；必须进入真实运行对象后创建 SimulationRun。</p>
          </div>
        </section>

        <aside aria-labelledby="studio-check-title" className="self-start rounded-ui-md border border-ui-line bg-ui-surface p-4 xl:sticky xl:top-4">
          <div className="flex items-baseline justify-between gap-3">
            <h2 id="studio-check-title" className="text-ui-4 font-semibold text-ui-txt">配置检查</h2>
            <span className="text-ui-1 font-bold text-ui-txt-2">{readyCount}/{readiness.length}</span>
          </div>
          <ul className="mt-3 divide-y divide-ui-line">
            {readiness.map(([label, ready]) => (
              <li key={label} className="flex items-center justify-between gap-3 py-2.5 text-ui-1">
                <span className="text-ui-txt-2">{label}</span>
                <span className={ready ? "font-bold text-ui-green" : "text-ui-txt-3"}>{ready ? "已定义" : "缺少"}</span>
              </li>
            ))}
          </ul>

          <div className="mt-5 border-t border-ui-line pt-4">
            <h3 className="text-ui-2 font-semibold text-ui-txt">能力供给</h3>
            <ul className="mt-2 grid gap-2">
              {template.capabilities.map((capability) => (
                <li key={capability.capabilityRef} className="flex items-center justify-between gap-2 rounded-ui-sm bg-ui-surface-2 px-3 py-2 text-ui-1">
                  <span className="text-ui-txt-2">{capability.capability}</span>
                  <span className="text-ui-0 text-ui-txt-3">待授权</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="mt-5 border-t border-ui-line pt-4">
            <h3 className="text-ui-2 font-semibold text-ui-txt">交付门禁</h3>
            <dl className="mt-2 grid gap-2 text-ui-1">
              <div className="flex justify-between gap-3"><dt className="text-ui-txt-3">Simulation</dt><dd className="font-bold text-ui-txt-2">未运行</dd></div>
              <div className="flex justify-between gap-3"><dt className="text-ui-txt-3">CEO Approve</dt><dd className="font-bold text-ui-txt-2">未提交</dd></div>
              <div className="flex justify-between gap-3"><dt className="text-ui-txt-3">Runtime</dt><dd className="font-bold text-ui-txt-2">未生效</dd></div>
            </dl>
          </div>

          {error && <p role="alert" className="mt-4 rounded-ui-sm border border-ui-red bg-ui-red/10 px-3 py-2 text-ui-1 text-ui-red">{error}</p>}
          <div className="mt-5 grid gap-2">
            <TerraButton type="submit" variant="primary" disabled={!canSave}>
              {saving ? "保存 Draft 与岗位方案中…" : "保存 Draft 并形成候选岗位方案"}
            </TerraButton>
            <Link href="/ceo-office/workspace" className="inline-flex min-h-9 items-center justify-center rounded-ui-sm px-3 text-ui-1 font-bold text-ui-txt-2 no-underline">返回 Workspace Portal</Link>
          </div>
          <p className="mt-3 text-ui-0 leading-relaxed text-ui-txt-3">保存后会形成 DRAFT 岗位、PROPOSED 候选员工与未授权能力需求；仍需 Simulation 与 CEO 明确批准。</p>
        </aside>
      </form>
    </TerraShell>
  );
}
