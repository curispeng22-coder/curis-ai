"use client";

/**
 * 经营（operating）· /ceo-office/analytics
 *
 * 结构严格对齐 UI 原型 curis-ui-prototype/operating.html + 规格 §4：
 *   筛选 Tab 条 → 公司脉搏（六维 + 证据链）→ 经营分析（4 图表卡）
 *   → 关注·风险·阻塞 → 决策队列 → 异常队列 → 机会雷达 → 公司约束
 *
 * 数据纪律：全部取自真实后端（getOperatingDay / getProjects / getEmployees）。
 * 后端未提供的事实（外部结果回传、注意力占用、平台授权、机会信号、已关闭事项）
 * 一律显示空态或「—」，不填任何演示数字。
 */

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import TerraShell from "../../../components/terra/TerraShell.js";
import { TerraIcon } from "../../../components/terra/TerraIcons.js";
import {
  TerraCard,
  TerraEmpty,
  TerraPageHead,
  TerraTable,
  TerraTag,
} from "../../../components/terra/TerraPrimitives.js";
import { getEmployees, getOperatingDay, getProjects } from "../../../lib/api.js";
import OperatingIntelligence from "./OperatingIntelligence.js";

/** 事实缺失占位（禁止用估算值填充） */
const NO_DATA = "—";

/** 筛选 Tab 条（原型 data-filter，联动下方带类型的卡片/行） */
const FILTER_TABS = [
  { key: "all", label: "全部" },
  { key: "decision", label: "待决策" },
  { key: "exception", label: "异常" },
  { key: "opportunity", label: "机会" },
  { key: "closed", label: "已关闭" },
];

/** 后端 metric_key → 中文标签（不暴露裸英文键） */
const METRIC_LABEL = {
  active_projects: "活跃业务",
  tasks_total: "任务总数",
  tasks_completed: "已完成任务",
  blocked_tasks: "受阻任务",
  task_completion_rate: "任务完成率",
  artifacts_count: "累计成果",
  employees_active: "在岗 AI 员工",
  workflow_runs: "自动运行次数",
  estimated_cost: "AI 运行成本",
};

/** 脉搏状态 → 徽章色（原型 pulse-ontrack / attention / risk / unknown） */
const PULSE_STATUS_COLOR = {
  正常: "green",
  需关注: "amber",
  有风险: "red",
  未知: "grey",
};

/** 次级文字入口（32px 命中高度） */
const SECONDARY_LINK =
  "inline-flex items-center h-8 px-2 rounded-ui-sm text-xs font-bold text-ui-primary no-underline transition-colors hover:bg-ui-surface-2";

/** 卡内次级按钮（无真实动作端点时统一指向决策室 / 相关页面） */
const CARD_ACTION =
  "inline-flex items-center h-8 px-3 rounded-ui-sm border border-ui-line bg-ui-surface-2 text-xs font-bold text-ui-txt-2 no-underline transition-colors hover:text-ui-primary";

/** 原型 section.card：标题 + 副标题 + body */
function SectionCard({ title, subtitle, extra, children, bodyClassName = "p-4" }) {
  return (
    <section className="bg-ui-surface border border-ui-line rounded-ui-md mb-4">
      <header className="flex items-start justify-between gap-3 px-4 py-3 border-b border-ui-line">
        <div className="min-w-0">
          <h2 className="text-sm font-bold text-ui-txt">{title}</h2>
          {subtitle && <p className="text-xs text-ui-txt-3 mt-0.5">{subtitle}</p>}
        </div>
        {extra}
      </header>
      <div className={bodyClassName}>{children}</div>
    </section>
  );
}

/** 公司脉搏单维卡（可点开证据链） */
function PulseCard({ dim, expanded, onToggle }) {
  return (
    <article className="bg-ui-surface-2 border border-ui-line rounded-ui-md p-3">
      <button
        type="button"
        onClick={onToggle}
        aria-expanded={expanded}
        className="w-full text-left cursor-pointer"
      >
        <div className="flex items-center justify-between gap-2">
          <span className="text-sm font-bold text-ui-txt">{dim.name}</span>
          <TerraTag color={PULSE_STATUS_COLOR[dim.status] || "grey"} icon>
            {dim.status}
          </TerraTag>
        </div>
        <p className="text-xs text-ui-txt-2 mt-2 leading-relaxed">{dim.summary}</p>
        <p className="text-xs text-ui-primary mt-2">
          {expanded ? "收起证据链" : "点击展开证据链"}
        </p>
      </button>

      {expanded && (
        <div className="mt-3 pt-3 border-t border-ui-line">
          <p className="text-xs font-bold text-ui-txt-3 mb-2">证据链</p>
          {dim.evidence.length === 0 ? (
            <TerraEmpty>暂无可引用的证据记录</TerraEmpty>
          ) : (
            <div className="flex flex-col gap-2">
              {dim.evidence.map((item, index) => (
                <div key={index} className="flex items-start gap-2">
                  <span className="w-1.5 h-1.5 rounded-ui-sm bg-ui-primary mt-1.5 flex-shrink-0" />
                  <div className="min-w-0">
                    <p className="text-xs text-ui-txt leading-relaxed">{item.name}</p>
                    <p className="text-xs text-ui-txt-3 mt-0.5">{item.source}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </article>
  );
}

/** 经营事项卡（异常 / 机会 / 已关闭 共用，原型 matter-card） */
function MatterCard({ badge, badgeColor, title, summary, meta = [], recovery, actions }) {
  return (
    <article className="bg-ui-surface-2 border border-ui-line rounded-ui-md p-3.5 flex flex-col">
      <div className="mb-2">
        <TerraTag color={badgeColor}>{badge}</TerraTag>
      </div>
      <h3 className="text-sm font-bold text-ui-txt leading-snug">{title}</h3>
      <p className="text-xs text-ui-txt-2 mt-1.5 leading-relaxed">{summary}</p>
      {meta.length > 0 && (
        <dl className="grid grid-cols-2 gap-2 mt-3">
          {meta.map((cell) => (
            <div key={cell.label}>
              <dt className="text-xs text-ui-txt-3">{cell.label}</dt>
              <dd className="text-xs font-bold text-ui-txt mt-0.5">{cell.value}</dd>
            </div>
          ))}
        </dl>
      )}
      {recovery && (
        <div className="mt-3 rounded-ui-sm border border-ui-line bg-ui-surface p-2.5">
          <div className="text-xs font-bold text-ui-txt-3">恢复计划</div>
          <p className="text-xs text-ui-txt-2 mt-1 leading-relaxed">{recovery}</p>
        </div>
      )}
      {actions && <div className="flex flex-wrap gap-2 mt-3">{actions}</div>}
    </article>
  );
}

/** 经营分析图表卡（标题 + 数值区，数值为真实值或 —） */
function AnalyticsCard({ label, value, unit, delta, children }) {
  return (
    <TerraCard className="flex flex-col">
      <div className="text-xs font-bold text-ui-txt-3">{label}</div>
      <div className="flex items-end gap-1.5 mt-2">
        <span className="text-2xl font-bold leading-none text-ui-txt">{value}</span>
        {unit && <span className="text-xs text-ui-txt-3 pb-0.5">{unit}</span>}
      </div>
      {delta && <div className="text-xs text-ui-txt-3 mt-1.5">{delta}</div>}
      {children && <div className="mt-3">{children}</div>}
    </TerraCard>
  );
}

export function LegacyOperatingPage() {
  const [operatingDay, setOperatingDay] = useState(null);
  const [projects, setProjects] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState("");
  const [filter, setFilter] = useState("all");
  const [openPulse, setOpenPulse] = useState("");
  const [syncedAt, setSyncedAt] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    let failure = "";
    try {
      setOperatingDay(await getOperatingDay());
    } catch (err) {
      setOperatingDay(null);
      failure = err?.message || "经营指标读取失败，以下分区显示空态。";
    }
    try {
      const payload = await getProjects();
      setProjects(payload?.projects || []);
    } catch {
      setProjects([]);
    }
    try {
      const payload = await getEmployees();
      setEmployees(payload?.employees || []);
    } catch {
      setEmployees([]);
    }
    setSyncedAt(
      new Date().toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" })
    );
    setNotice(failure);
    setLoading(false);
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  /** 后端 pulse 数组 → metric_key 索引 */
  const facts = useMemo(() => {
    const rows = operatingDay?.pulse || [];
    const map = Object.fromEntries(rows.map((row) => [row.metric_key, row]));
    const get = (key) => (map[key] ? Number(map[key].value) : null);
    return {
      hasMetrics: rows.length > 0,
      activeProjects: get("active_projects"),
      tasksTotal: get("tasks_total"),
      tasksCompleted: get("tasks_completed"),
      blockedTasks: get("blocked_tasks"),
      completionRate: get("task_completion_rate"),
      artifacts: get("artifacts_count"),
      employeesActive: get("employees_active"),
      workflowRuns: get("workflow_runs"),
      cost: get("estimated_cost"),
    };
  }, [operatingDay]);

  /**
   * 经营事项分类（原型 data-type）：
   * - decision  ← 后端 matters.level=risk（需 CEO 处理）
   * - exception ← 后端 matters.level=attention
   * - opportunity / closed ← 尚无事实源，保留分区骨架 + 空态
   */
  const buckets = useMemo(() => {
    const matters = operatingDay?.matters || [];
    return {
      decision: matters.filter((item) => item.level === "risk"),
      exception: matters.filter((item) => item.level === "attention"),
      opportunity: [],
      closed: [],
    };
  }, [operatingDay]);

  const counts = useMemo(
    () => ({
      decision: buckets.decision.length,
      exception: buckets.exception.length,
      opportunity: buckets.opportunity.length,
      closed: buckets.closed.length,
      all:
        buckets.decision.length +
        buckets.exception.length +
        buckets.opportunity.length +
        buckets.closed.length,
    }),
    [buckets]
  );

  /** 公司脉搏六维：状态与摘要全部由真实指标推导，无指标即「未知」 */
  const pulseDimensions = useMemo(() => {
    const matters = operatingDay?.matters || [];
    const timeline = operatingDay?.timeline || [];
    const evidenceOf = (keys) =>
      matters
        .filter((item) => keys.includes(item.metric_key))
        .map((item) => ({
          name: item.message,
          source: `来源：经营指标 · ${METRIC_LABEL[item.metric_key] || item.metric_key}`,
        }));

    const {
      hasMetrics,
      activeProjects,
      tasksTotal,
      tasksCompleted,
      blockedTasks,
      completionRate,
      artifacts,
      employeesActive,
      workflowRuns,
    } = facts;

    const unknown = (name, hint) => ({
      key: name,
      name,
      status: "未知",
      summary: hint,
      evidence: [],
    });

    if (!hasMetrics) {
      return [
        unknown("价值", "尚未读取到经营指标，价值维度未知。"),
        unknown("执行", "尚未读取到经营指标，执行维度未知。"),
        unknown("供给", "尚未读取到经营指标，供给维度未知。"),
        unknown("风险", "尚未读取到经营指标，风险维度未知。"),
        unknown("方向", "尚未读取到经营指标，方向维度未知。"),
        unknown("连续性", "尚未读取到经营指标，连续性维度未知。"),
      ];
    }

    return [
      {
        key: "价值",
        name: "价值",
        status: artifacts > 0 ? "正常" : "需关注",
        summary:
          artifacts > 0
            ? `已记录 ${artifacts} 项可复用成果；外部结果回传尚未接入，金额口径显示为 ${NO_DATA}。`
            : "尚未产生可验证成果，价值口径无法确认。",
        evidence: evidenceOf(["artifacts_count", "estimated_cost"]),
      },
      {
        key: "执行",
        name: "执行",
        status:
          tasksTotal === 0 ? "未知" : blockedTasks > 0 ? "需关注" : completionRate >= 80 ? "正常" : "需关注",
        summary:
          tasksTotal === 0
            ? "尚无任务记录，执行节奏未知。"
            : `任务完成率 ${completionRate}%（完成 ${tasksCompleted} / 共 ${tasksTotal}），受阻 ${blockedTasks} 项。`,
        evidence: evidenceOf(["task_completion_rate", "tasks_total", "tasks_completed"]),
      },
      {
        key: "供给",
        name: "供给",
        status: employeesActive > 0 ? "正常" : "需关注",
        summary:
          employeesActive > 0
            ? `${employeesActive} 名 AI 员工在岗；单员工负载明细尚未接入容量数据源。`
            : "尚未启用 AI 员工，供给能力为空。",
        evidence: evidenceOf(["employees_active"]),
      },
      {
        key: "风险",
        name: "风险",
        status: blockedTasks > 0 ? "有风险" : "正常",
        summary:
          blockedTasks > 0
            ? `${blockedTasks} 个任务处于受阻/失败状态，需要 CEO 处理。`
            : "当前无受阻任务；外部授权到期风险尚未接入登记源。",
        evidence: evidenceOf(["blocked_tasks"]),
      },
      {
        key: "方向",
        name: "方向",
        status: activeProjects > 0 ? "正常" : "未知",
        summary:
          activeProjects > 0
            ? `${activeProjects} 个业务方向在运行；是否扩大投入需真实结果回传后判断。`
            : "尚无活跃业务方向，方向判断缺少依据。",
        evidence: evidenceOf(["active_projects"]),
      },
      {
        key: "连续性",
        name: "连续性",
        status: workflowRuns > 0 ? "正常" : "需关注",
        summary:
          workflowRuns > 0
            ? `已记录 ${workflowRuns} 次自动运行；AI 交接记录随运行时间线归档。`
            : "尚无自动运行记录，经营连续性未建立。",
        evidence:
          timeline.length === 0
            ? evidenceOf(["workflow_runs"])
            : timeline.slice(0, 3).map((event) => ({
                name: event.title || NO_DATA,
                source: `来源：${event.type || "运行记录"} · ${event.at || NO_DATA}`,
              })),
      },
    ];
  }, [facts, operatingDay]);

  const showType = useCallback((type) => filter === "all" || filter === type, [filter]);

  const decisionRows = useMemo(
    () =>
      (showType("decision") ? buckets.decision : []).map((item, index) => ({
        id: `${item.metric_key || "decision"}-${index}`,
        message: item.message,
        scope: METRIC_LABEL[item.metric_key] || NO_DATA,
      })),
    [buckets.decision, showType]
  );

  const decisionColumns = useMemo(
    () => [
      {
        key: "matter",
        label: "决策事项",
        render: (row) => (
          <div className="min-w-0">
            <div className="text-xs font-bold text-ui-txt">{row.message}</div>
            <div className="text-xs text-ui-txt-3 mt-0.5">来源：经营指标聚合</div>
          </div>
        ),
      },
      {
        key: "scope",
        label: "影响范围",
        render: (row) => (
          <div>
            <div className="text-xs font-bold text-ui-txt">{row.scope}</div>
            <div className="text-xs text-ui-txt-3 mt-0.5">预算与资源口径 {NO_DATA}</div>
          </div>
        ),
      },
      {
        key: "due",
        label: "截止时间",
        render: () => (
          <div>
            <div className="text-xs font-bold text-ui-txt">{NO_DATA}</div>
            <div className="text-xs text-ui-txt-3 mt-0.5">尚未设置截止</div>
          </div>
        ),
      },
      {
        key: "recommend",
        label: "推荐动作",
        render: () => (
          <div>
            <div className="text-xs font-bold text-ui-txt">{NO_DATA}</div>
            <div className="text-xs text-ui-txt-3 mt-0.5">需在决策室补齐事实后给出</div>
          </div>
        ),
      },
      {
        key: "action",
        label: "操作",
        render: () => (
          <Link href="/ceo-office/decisions" className={CARD_ACTION}>
            决策
          </Link>
        ),
      },
    ],
    []
  );

  const attentionItems = showType("exception") ? buckets.exception : [];
  const blockedItems = showType("decision") ? buckets.decision : [];
  const exceptionItems = showType("exception") ? buckets.exception : [];
  const opportunityItems = showType("opportunity") ? buckets.opportunity : [];

  const taskAttention =
    facts.tasksTotal === null
      ? null
      : Math.max(0, facts.tasksTotal - (facts.tasksCompleted || 0) - (facts.blockedTasks || 0));

  return (
    <TerraShell topCrumb="经营 · Curis" assistantContext={{ page: "operating" }}>
      <TerraPageHead
        title="经营"
        subtitle={operatingDay?.brief?.summary || "尚未读取到经营简报，以下分区显示真实空态。"}
        facts={[
          { value: counts.decision, label: "待决策" },
          { value: counts.exception, label: "异常" },
          { value: facts.blockedTasks === null ? NO_DATA : facts.blockedTasks, label: "受阻任务" },
        ]}
      />

      {/* 页头元信息（原型 page-meta） */}
      <div className="flex flex-wrap items-center gap-x-2 gap-y-1 text-xs text-ui-txt-3 mb-3.5">
        <span>{operatingDay?.date || NO_DATA}</span>
        <span>|</span>
        <span>
          公司阶段：<strong className="text-ui-txt-2">{NO_DATA}</strong>
        </span>
        <span>|</span>
        <span>
          最近决策：<strong className="text-ui-txt-2">{NO_DATA}</strong>
        </span>
        <span>|</span>
        <span>
          待处理：<strong className="text-ui-txt-2">{counts.decision} 项待决策</strong> ·{" "}
          <strong className="text-ui-txt-2">
            {facts.blockedTasks === null ? NO_DATA : facts.blockedTasks} 项阻塞
          </strong>
        </span>
        <span>|</span>
        <span>上次同步：{syncedAt || NO_DATA}</span>
      </div>

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

      {/* 1 · 筛选 Tab 条 */}
      <nav className="flex flex-wrap items-center gap-1.5 mb-4" aria-label="经营事项过滤">
        {FILTER_TABS.map((tab) => {
          const active = filter === tab.key;
          return (
            <button
              key={tab.key}
              type="button"
              aria-pressed={active}
              onClick={() => setFilter(tab.key)}
              className={`inline-flex items-center gap-1.5 h-8 px-3.5 rounded-ui-sm border text-xs font-bold transition-colors ${
                active
                  ? "bg-ui-primary-light text-ui-primary border-ui-line"
                  : "bg-ui-surface-2 text-ui-txt-2 border-ui-line hover:text-ui-txt"
              }`}
            >
              <span>{tab.label}</span>
              <span className="text-xs opacity-70">{counts[tab.key]}</span>
            </button>
          );
        })}
      </nav>

      {/* 2 · 公司脉搏 */}
      <SectionCard title="公司脉搏" subtitle="六维经营状态 · 点击任一维度展开证据链">
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
          {pulseDimensions.map((dim) => (
            <PulseCard
              key={dim.key}
              dim={dim}
              expanded={openPulse === dim.key}
              onToggle={() => setOpenPulse(openPulse === dim.key ? "" : dim.key)}
            />
          ))}
        </div>
      </SectionCard>

      {/* 3 · 经营分析 */}
      <SectionCard title="经营分析" subtitle="趋势、完成率、AI 运行成本与业务贡献">
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-3">
          <AnalyticsCard
            label="近 30 天外部结果趋势"
            value={NO_DATA}
            delta="外部结果回传未接入，金额不做估算"
          >
            <div className="text-xs text-ui-txt-3">
              累计成果 <span className="font-bold text-ui-txt-2">{facts.artifacts ?? NO_DATA}</span> 项
            </div>
          </AnalyticsCard>

          <AnalyticsCard
            label="本周任务状态"
            value={facts.completionRate === null ? NO_DATA : `${facts.completionRate}%`}
            delta="完成率 = 已完成任务 ÷ 任务总数"
          >
            <div className="flex flex-col gap-1.5 text-xs text-ui-txt-3">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-ui-sm bg-ui-primary" />
                完成 {facts.tasksCompleted ?? NO_DATA}
              </div>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-ui-sm bg-ui-surface-2 border border-ui-line" />
                关注 {taskAttention ?? NO_DATA}
              </div>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-ui-sm bg-ui-red" />
                阻塞 {facts.blockedTasks ?? NO_DATA}
              </div>
            </div>
          </AnalyticsCard>

          <AnalyticsCard
            label="AI 运行成本"
            value={facts.cost === null ? NO_DATA : facts.cost}
            unit={facts.cost === null ? "" : "USD"}
            delta="按 AI 用量记录聚合 · 环比口径未接入"
          >
            <div className="text-xs text-ui-txt-3">
              用量分布 <span className="font-bold text-ui-txt-2">{NO_DATA}</span>
            </div>
          </AnalyticsCard>

          <AnalyticsCard
            label="业务价值贡献"
            value={projects.length}
            unit="个业务"
            delta="按业务归集的外部结果尚未回传"
          >
            {projects.length === 0 ? (
              <div className="text-xs text-ui-txt-3">暂无业务</div>
            ) : (
              <div className="flex flex-col gap-1.5">
                {projects.slice(0, 4).map((project) => (
                  <div
                    key={project.project_id}
                    className="flex items-center justify-between gap-2 text-xs"
                  >
                    <span className="text-ui-txt-2 truncate">{project.name || NO_DATA}</span>
                    <span className="text-ui-txt-3 flex-shrink-0">{NO_DATA}</span>
                  </div>
                ))}
              </div>
            )}
          </AnalyticsCard>
        </div>
      </SectionCard>

      {/* 4 · 关注 · 风险 · 阻塞 */}
      <SectionCard
        title="关注 · 风险 · 阻塞"
        subtitle={`按升级状态分组的经营异常 · 共 ${counts.decision + counts.exception} 项`}
      >
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <div>
            <div className="flex items-center justify-between gap-2 mb-2.5">
              <span className="text-xs font-bold text-ui-txt-2">需要关注</span>
              <span className="text-xs text-ui-txt-3">{attentionItems.length}</span>
            </div>
            {attentionItems.length === 0 ? (
              <TerraEmpty>暂无需要关注的事项</TerraEmpty>
            ) : (
              <div className="flex flex-col gap-3">
                {attentionItems.map((item, index) => (
                  <MatterCard
                    key={`attention-${index}`}
                    badge="需要关注"
                    badgeColor="amber"
                    title={item.message}
                    summary={`指标来源：${METRIC_LABEL[item.metric_key] || NO_DATA}`}
                    meta={[
                      { label: "负责人", value: NO_DATA },
                      { label: "影响", value: NO_DATA },
                    ]}
                    actions={
                      <Link href="/ceo-office/decisions" className={CARD_ACTION}>
                        决策
                      </Link>
                    }
                  />
                ))}
              </div>
            )}
          </div>

          <div>
            <div className="flex items-center justify-between gap-2 mb-2.5">
              <span className="text-xs font-bold text-ui-txt-2">当前阻塞</span>
              <span className="text-xs text-ui-txt-3">{blockedItems.length}</span>
            </div>
            {blockedItems.length === 0 ? (
              <TerraEmpty>暂无阻塞事项</TerraEmpty>
            ) : (
              <div className="flex flex-col gap-3">
                {blockedItems.map((item, index) => (
                  <MatterCard
                    key={`blocked-${index}`}
                    badge="当前阻塞"
                    badgeColor="red"
                    title={item.message}
                    summary={`指标来源：${METRIC_LABEL[item.metric_key] || NO_DATA}`}
                    meta={[
                      { label: "负责人", value: NO_DATA },
                      { label: "影响", value: NO_DATA },
                    ]}
                    actions={
                      <>
                        <Link href="/ceo-office/execution" className={CARD_ACTION}>
                          查看
                        </Link>
                        <Link href="/ceo-office/decisions" className={CARD_ACTION}>
                          生成决策包
                        </Link>
                      </>
                    }
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </SectionCard>

      {/* 5 · 决策队列 */}
      <SectionCard
        title="决策队列"
        subtitle="等待 CEO 决定的事项 · 按截止优先级排序"
        bodyClassName="p-0"
      >
        <TerraTable
          columns={decisionColumns}
          rows={decisionRows}
          caption="决策队列"
          empty="暂无待决策事项"
        />
      </SectionCard>

      {/* 6 · 异常队列 */}
      <SectionCard title="异常队列" subtitle="已升级的经营异常 · 含负责人、遏制状态与恢复计划">
        {exceptionItems.length === 0 ? (
          <TerraEmpty icon="i-check_circle">暂无已升级的经营异常</TerraEmpty>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
            {exceptionItems.map((item, index) => (
              <MatterCard
                key={`exception-${index}`}
                badge="活跃异常"
                badgeColor="red"
                title={item.message}
                summary={`指标来源：${METRIC_LABEL[item.metric_key] || NO_DATA}`}
                meta={[
                  { label: "负责人", value: NO_DATA },
                  { label: "遏制状态", value: NO_DATA },
                ]}
                recovery="恢复计划尚未登记，需在决策室补齐负责人与时间点。"
                actions={
                  <>
                    <Link href="/ceo-office/execution" className={CARD_ACTION}>
                      查看工单
                    </Link>
                    <Link href="/ceo-office/decisions" className={CARD_ACTION}>
                      升级
                    </Link>
                  </>
                }
              />
            ))}
          </div>
        )}
      </SectionCard>

      {/* 7 · 机会雷达 */}
      <SectionCard title="机会雷达" subtitle="新信号与待调查机会 · 按信号强度排序">
        {opportunityItems.length === 0 ? (
          <TerraEmpty icon="i-lightbulb">
            暂无机会信号。机会需由 AI 团队提交带来源的评估后出现在这里。
          </TerraEmpty>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
            {opportunityItems.map((item, index) => (
              <MatterCard
                key={`opportunity-${index}`}
                badge="机会"
                badgeColor="green"
                title={item.message}
                summary={`指标来源：${METRIC_LABEL[item.metric_key] || NO_DATA}`}
                meta={[
                  { label: "来源", value: NO_DATA },
                  { label: "预期影响", value: NO_DATA },
                  { label: "验证方式", value: NO_DATA },
                  { label: "检查点", value: NO_DATA },
                ]}
              />
            ))}
          </div>
        )}
      </SectionCard>

      {/* 8 · 公司约束 */}
      <SectionCard title="公司约束" subtitle="容量 · 授权 · 注意力瓶颈">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div className="bg-ui-surface-2 border border-ui-line rounded-ui-md p-3.5">
            <div className="text-xs text-ui-txt-3">CEO 注意力容量</div>
            <div className="text-2xl font-bold text-ui-txt mt-1.5 leading-none">{NO_DATA}</div>
            <p className="text-xs text-ui-txt-2 mt-2 leading-relaxed">
              注意力占用尚未接入日历与决策记录，不做估算。
            </p>
            <Link href="/ceo-office/calendar" className={`${SECONDARY_LINK} mt-2 -ml-2`}>
              查看注意力日历
            </Link>
          </div>

          <div className="bg-ui-surface-2 border border-ui-line rounded-ui-md p-3.5">
            <div className="text-xs text-ui-txt-3">外部平台授权</div>
            <div className="text-2xl font-bold text-ui-txt mt-1.5 leading-none">{NO_DATA}</div>
            <p className="text-xs text-ui-txt-2 mt-2 leading-relaxed">
              平台授权清单尚未登记，授权到期风险无法核对。
            </p>
            <Link href="/ceo-office/capabilities" className={`${SECONDARY_LINK} mt-2 -ml-2`}>
              查看授权清单
            </Link>
          </div>

          <div className="bg-ui-surface-2 border border-ui-line rounded-ui-md p-3.5">
            <div className="text-xs text-ui-txt-3">AI 团队容量瓶颈</div>
            <div className="text-2xl font-bold text-ui-txt mt-1.5 leading-none">
              {employees.length === 0 ? NO_DATA : `在岗 ${employees.length} 人`}
            </div>
            <p className="text-xs text-ui-txt-2 mt-2 leading-relaxed">
              单员工负载百分比尚未接入容量数据源，仅显示在岗人数事实。
            </p>
            <Link href="/ceo-office/organization" className={`${SECONDARY_LINK} mt-2 -ml-2`}>
              调配容量
            </Link>
          </div>
        </div>
      </SectionCard>
    </TerraShell>
  );
}

export default function OperatingPage() {
  return <OperatingIntelligence />;
}
