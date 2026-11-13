"use client";

/**
 * 业务（business）· /ceo-office/projects
 *
 * 结构严格对齐 UI 原型 curis-ui-prototype/business.html + 规格 §5：
 *   页头 + 计数条 → 过滤 Tab → 业务卡网格（空态）
 *   → 业务推进过程（5 步）→ 投入与结果 → 高影响动作
 *
 * 数据纪律：业务卡全部来自真实 projects 列表。后端未提供的事实
 * （健康度、外部结果、下一检查点、投入产出）显示「—」或空态，不编造数字。
 */

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import TerraShell from "../../../components/terra/TerraShell.js";
import { TerraIcon } from "../../../components/terra/TerraIcons.js";
import {
  TerraEmpty,
  TerraPageHead,
  TerraTag,
} from "../../../components/terra/TerraPrimitives.js";
import {
  getDepartments,
  getOperatingDay,
  getProjects,
} from "../../../lib/api.js";

/** 事实缺失占位 */
const NO_DATA = "—";

/** 过滤 Tab（原型 data-filter → 卡片 data-stage） */
const STAGE_TABS = [
  { key: "all", label: "全部" },
  { key: "operating", label: "运行中" },
  { key: "experiment", label: "实验中" },
  { key: "paused", label: "暂停" },
];

/** 业务阶段徽章 */
const STAGE_META = {
  operating: { label: "运行中", color: "green" },
  experiment: { label: "实验中", color: "cyan" },
  paused: { label: "暂停", color: "amber" },
  unknown: { label: "未记录", color: "grey" },
};

/** 后端 project.status → 原型业务阶段 data-stage */
function toStage(status) {
  if (status === "active" || status === "in_progress" || status === "operating") return "operating";
  if (status === "planned" || status === "experiment") return "experiment";
  if (status === "paused" || status === "blocked" || status === "archived" || status === "completed") {
    return "paused";
  }
  return "unknown";
}

/** 业务推进过程 5 步（原型静态流程说明，非数据） */
const PROCESS_STEPS = [
  { title: "确定方向", desc: "说清业务想法、目标结果和验收标准，安排 AI 员工与预算。" },
  { title: "开始执行", desc: "工作空间运行产出交付物：代码、内容、信号、客户互动。" },
  { title: "真实反馈", desc: "真实世界返回证据：用户行为、平台数据、CEO 验收、市场信号。" },
  { title: "决定下一步", desc: "CEO 判断继续、扩大、暂停或关闭，并记录决策依据。" },
  { title: "下一 bet", desc: "根据结果调整想法，进入下一周期或把资源收回来。" },
];

/** 高影响动作（原型抽屉分区，动作说明为界面文案） */
const HIGH_IMPACT_ACTIONS = [
  { title: "扩大投入", desc: "只有「已验证」等级的外部结果才能解冻扩大权限。" },
  { title: "暂停业务", desc: "保留数据与承诺，停止新周期启动。" },
  { title: "关闭业务", desc: "归档所有证据与决策记录，释放资源。" },
];

const PRIMARY_LINK =
  "inline-flex items-center justify-center gap-1.5 h-9 px-4 rounded-ui-sm bg-ui-primary-light text-xs font-bold text-ui-primary no-underline transition-colors hover:opacity-80";

const CARD_ACTION =
  "inline-flex items-center h-8 px-3 rounded-ui-sm border border-ui-line bg-ui-surface-2 text-xs font-bold text-ui-txt-2 no-underline transition-colors hover:text-ui-primary";

/** 原型 section-card */
function SectionCard({ title, extra, children }) {
  return (
    <section className="bg-ui-surface border border-ui-line rounded-ui-md">
      <header className="flex items-center justify-between gap-3 px-4 py-3 border-b border-ui-line">
        <h2 className="text-sm font-bold text-ui-txt">{title}</h2>
        {extra}
      </header>
      <div className="p-4">{children}</div>
    </section>
  );
}

/** 业务卡（原型 biz-card） */
function BusinessCard({ project, stage, subtitle }) {
  const meta = STAGE_META[stage] || STAGE_META.unknown;
  return (
    <article className="bg-ui-surface border border-ui-line rounded-ui-md flex flex-col">
      {/* 卡头：名称 + 副标题 + 阶段徽章 + 健康行 */}
      <div className="p-4 border-b border-ui-line">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0">
            <h3 className="text-sm font-bold text-ui-txt truncate">
              {project.name || "未命名业务"}
            </h3>
            <p className="text-xs text-ui-txt-3 mt-1">{subtitle}</p>
          </div>
          <TerraTag color={meta.color}>{meta.label}</TerraTag>
        </div>

        <div className="grid grid-cols-2 gap-2 mt-3">
          <div className="rounded-ui-sm bg-ui-surface-2 border border-ui-line px-2.5 py-2">
            <div className="text-xs text-ui-txt-3">价值健康</div>
            <div className="text-xs font-bold text-ui-txt-2 mt-0.5">{NO_DATA}</div>
          </div>
          <div className="rounded-ui-sm bg-ui-surface-2 border border-ui-line px-2.5 py-2">
            <div className="text-xs text-ui-txt-3">执行健康</div>
            <div className="text-xs font-bold text-ui-txt-2 mt-0.5">{NO_DATA}</div>
          </div>
        </div>
      </div>

      {/* 卡身：目标结果 / 外部结果 / 下一检查点 */}
      <div className="p-4 flex-1 flex flex-col gap-3.5">
        <div>
          <div className="text-xs font-bold text-ui-txt-3 mb-1">目标结果</div>
          <p className="text-xs text-ui-txt-2 leading-relaxed">{project.goal || NO_DATA}</p>
        </div>

        <div>
          <div className="text-xs font-bold text-ui-txt-3 mb-1">外部结果</div>
          <div className="rounded-ui-sm bg-ui-surface-2 border border-ui-line px-2.5 py-2 text-xs text-ui-txt-3">
            暂无外部结果回传
          </div>
        </div>

        <div>
          <div className="text-xs font-bold text-ui-txt-3 mb-1">下一检查点</div>
          <div className="flex items-center justify-between gap-2 rounded-ui-sm bg-ui-surface-2 border border-ui-line px-2.5 py-2">
            <span className="text-xs text-ui-txt-2">{NO_DATA}</span>
            <span className="text-xs text-ui-txt-3">{NO_DATA}</span>
          </div>
        </div>
      </div>

      {/* 卡脚：操作 */}
      <div className="flex flex-wrap gap-2 px-4 pb-4">
        <Link href="/ceo-office/decisions" className={CARD_ACTION}>
          扩大
        </Link>
        <Link href={`/ceo-office/projects/${project.project_id}`} className={CARD_ACTION}>
          查看详情
        </Link>
        <Link href="/ceo-office/decisions" className={CARD_ACTION}>
          暂停
        </Link>
      </div>
    </article>
  );
}

/** 投入与结果小卡 */
function RoiCard({ label, value, hint }) {
  return (
    <div className="rounded-ui-sm bg-ui-surface-2 border border-ui-line p-3">
      <div className="text-xs text-ui-txt-3">{label}</div>
      <div className="text-lg font-bold text-ui-txt mt-1 leading-none">{value}</div>
      <div className="text-xs text-ui-txt-3 mt-1.5">{hint}</div>
    </div>
  );
}

export default function BusinessPage() {
  const [projects, setProjects] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [operatingDay, setOperatingDay] = useState(null);
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState("");
  const [filter, setFilter] = useState("all");

  const load = useCallback(async () => {
    setLoading(true);
    let failure = "";
    try {
      const payload = await getProjects();
      setProjects(payload?.projects || []);
    } catch (err) {
      setProjects([]);
      failure = err?.message || "业务列表读取失败，下方显示空态。";
    }
    try {
      const payload = await getDepartments();
      setDepartments(payload?.departments || []);
    } catch {
      setDepartments([]);
    }
    try {
      setOperatingDay(await getOperatingDay());
    } catch {
      setOperatingDay(null);
    }
    setNotice(failure);
    setLoading(false);
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const departmentNames = useMemo(
    () => Object.fromEntries(departments.map((item) => [item.id, item.name])),
    [departments]
  );

  /** 真实 projects → 业务卡视图（含 data-stage） */
  const businesses = useMemo(
    () =>
      projects.map((project) => ({
        project,
        stage: toStage(project.status),
        subtitle:
          departmentNames[project.department_id] || project.project_type || NO_DATA,
      })),
    [departmentNames, projects]
  );

  /** 顶部计数条：全部从真实业务计算，空时全 0 */
  const summary = useMemo(
    () => ({
      operating: businesses.filter((item) => item.stage === "operating").length,
      experiment: businesses.filter((item) => item.stage === "experiment").length,
      paused: businesses.filter((item) => item.stage === "paused").length,
      total: businesses.length,
    }),
    [businesses]
  );

  const visibleBusinesses = useMemo(
    () => (filter === "all" ? businesses : businesses.filter((item) => item.stage === filter)),
    [businesses, filter]
  );

  /** 投入与结果：AI 成本取真实聚合，其余口径未接入 → — */
  const cost = useMemo(() => {
    const rows = operatingDay?.pulse || [];
    const row = rows.find((item) => item.metric_key === "estimated_cost");
    return row ? Number(row.value) : null;
  }, [operatingDay]);

  return (
    <TerraShell topCrumb="业务 · Curis" assistantContext={{ page: "business" }}>
      <TerraPageHead
        title="业务"
        subtitle="CEO 正在经营哪些业务，以及每项业务的真实结果和下一步安排。"
        facts={[
          { value: summary.operating, label: "运行中" },
          { value: summary.experiment, label: "实验中" },
          { value: summary.paused, label: "暂停" },
          { value: summary.total, label: "总业务数" },
        ]}
        actions={
          <Link href="/onboarding" className={PRIMARY_LINK}>
            <TerraIcon name="i-add" className="w-4 h-4" />
            创建业务
          </Link>
        }
      />

      {notice && (
        <div className="mb-3.5 flex items-center gap-2 rounded-ui-sm border border-ui-line bg-ui-surface-2 px-3 py-2 text-xs text-ui-txt-2">
          <TerraIcon name="i-warning" className="w-4 h-4 text-ui-txt-3" />
          <span>{notice}</span>
          <button
            type="button"
            onClick={load}
            className="ml-auto inline-flex items-center h-8 px-2 rounded-ui-sm text-xs font-bold text-ui-primary"
          >
            重试
          </button>
        </div>
      )}

      {/* 过滤 Tab（原型 filter-bar） */}
      <div className="flex flex-wrap items-center gap-1.5 mb-4" role="tablist" aria-label="业务过滤">
        {STAGE_TABS.map((tab) => {
          const active = filter === tab.key;
          return (
            <button
              key={tab.key}
              type="button"
              role="tab"
              aria-selected={active}
              onClick={() => setFilter(tab.key)}
              className={`inline-flex items-center h-8 px-3.5 rounded-ui-sm border text-xs font-bold transition-colors ${
                active
                  ? "bg-ui-primary-light text-ui-primary border-ui-line"
                  : "bg-ui-surface-2 text-ui-txt-2 border-ui-line hover:text-ui-txt"
              }`}
            >
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* 业务卡网格 / 空态 */}
      {visibleBusinesses.length === 0 ? (
        <div className="mb-4">
          <TerraEmpty icon="i-folder_off">
            <div>该过滤条件下暂无业务。</div>
            <Link href="/onboarding" className={`${PRIMARY_LINK} mt-3`}>
              <TerraIcon name="i-add" className="w-4 h-4" />
              创建第一个业务
            </Link>
          </TerraEmpty>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3.5 mb-4">
          {visibleBusinesses.map((item) => (
            <BusinessCard
              key={item.project.project_id}
              project={item.project}
              stage={item.stage}
              subtitle={item.subtitle}
            />
          ))}
        </div>
      )}

      {/* 业务推进过程 + 右侧栏（投入与结果 / 高影响动作） */}
      <div className="grid grid-cols-12 gap-4">
        <div className="col-span-12 lg:col-span-8">
          <SectionCard
            title="业务推进过程"
            extra={<TerraTag color="grey">当前周期 {NO_DATA}</TerraTag>}
          >
            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-5 gap-3">
              {PROCESS_STEPS.map((step, index) => (
                <div
                  key={step.title}
                  className="rounded-ui-sm bg-ui-surface-2 border border-ui-line p-3"
                >
                  <div className="w-6 h-6 rounded-ui-sm bg-ui-primary-light text-ui-primary grid place-items-center text-xs font-bold">
                    {index + 1}
                  </div>
                  <h4 className="text-xs font-bold text-ui-txt mt-2">{step.title}</h4>
                  <p className="text-xs text-ui-txt-3 mt-1 leading-relaxed">{step.desc}</p>
                </div>
              ))}
            </div>
          </SectionCard>
        </div>

        <div className="col-span-12 lg:col-span-4 flex flex-col gap-4">
          <SectionCard title="投入与结果" extra={<TerraTag color="grey">本周期</TerraTag>}>
            <div className="grid grid-cols-2 gap-3">
              <RoiCard
                label="AI 成本"
                value={cost === null ? NO_DATA : cost}
                hint={cost === null ? "成本聚合未读取" : "USD · 按用量记录聚合"}
              />
              <RoiCard label="CEO 注意力" value={NO_DATA} hint="注意力口径未接入" />
              <RoiCard label="外部结果总值" value={NO_DATA} hint="外部结果回传未接入" />
              <RoiCard label="投入产出" value={NO_DATA} hint="需外部结果后才可计算" />
            </div>
            <div className="mt-3 rounded-ui-sm bg-ui-surface-2 border border-ui-line px-3 py-2.5">
              <div className="text-xs font-bold text-ui-txt-3">下一步建议</div>
              <p className="text-xs text-ui-txt-2 mt-1 leading-relaxed">
                外部结果未回传前不给出「继续运营 / 扩大投入」建议。
              </p>
            </div>
          </SectionCard>

          <SectionCard title="高影响动作">
            <div className="flex flex-col gap-2">
              {HIGH_IMPACT_ACTIONS.map((action) => (
                <div
                  key={action.title}
                  className="rounded-ui-sm bg-ui-surface-2 border border-ui-line px-3 py-2.5"
                >
                  <div className="text-xs font-bold text-ui-txt">{action.title}</div>
                  <p className="text-xs text-ui-txt-3 mt-1 leading-relaxed">{action.desc}</p>
                </div>
              ))}
            </div>
            <Link href="/ceo-office/decisions" className={`${PRIMARY_LINK} mt-3 w-full`}>
              去决策室提交
            </Link>
          </SectionCard>
        </div>
      </div>
    </TerraShell>
  );
}
